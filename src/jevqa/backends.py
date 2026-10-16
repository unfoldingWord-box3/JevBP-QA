"""Checkers that answer a Case's typed questions.

- jev: TypeSafe's System One model, the thing under test.
- openrouter: an ordinary LLM asked the same questions and told to give
  probabilities. The baseline Jev has to beat on accuracy, calibration, speed and cost.
- dryrun: writes the request and answers nothing (for inspecting what would be sent).

All three return answers in Jev's wire shape, so routing and evaluation never
care which one ran. Responses are cached on disk by request hash.
"""

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from jevqa import questions as qs
from jevqa.model import Answer, CallResult, Case

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "runs" / "cache"
JEV_URL = "https://api.typesafe.ai/v1/systemone"
JEV_PRICE_PER_INPUT_TOKEN = 0.042 / 1_000_000  # typesafe.ai pricing page, Oct 2026; output is free
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def key(name: str) -> str:
    """API key from the environment, else from ~/.config/ai-keys.env."""
    if os.environ.get(name):
        return os.environ[name]
    env = Path.home() / ".config" / "ai-keys.env"
    if env.exists():
        for line in env.read_text().splitlines():
            k, _, v = line.removeprefix("export ").partition("=")
            if k.strip() == name and v.strip():
                return v.strip().strip("'\"")
    raise RuntimeError(f"{name} not set (environment or ~/.config/ai-keys.env)")


def _post(url: str, body: dict, headers: dict, tries: int = 4) -> dict:
    data = json.dumps(body, ensure_ascii=False).encode()
    for attempt in range(tries):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            raise RuntimeError(f"HTTP {e.code} from {url}: {e.read()[:500].decode(errors='replace')}") from e


def parse_json(text: str) -> dict:
    """First JSON object in a model's reply, ignoring fences or trailing text."""
    return json.JSONDecoder().raw_decode(text[text.find("{"):])[0]


class Backend:
    name = "base"
    model = ""

    def ask(self, case: Case) -> CallResult:
        st, q = qs.state(case), qs.questions(case)
        h = hashlib.sha256(json.dumps([self.name, self.model, st, q], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:24]
        path = CACHE / self.name / f"{h}.json"
        if path.exists():
            hit = json.loads(path.read_text())
        else:
            t0 = time.perf_counter()
            try:
                hit = self._call(st, q)
            except Exception as e:  # recorded per case so one bad call doesn't sink a run
                return CallResult(case.id, self.name, self.model, {}, 0.0, None, None, error=str(e))
            hit["latency_ms"] = (time.perf_counter() - t0) * 1000
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(hit, ensure_ascii=False, indent=1))
        answers = {name: Answer(name, raw, qs.p_pass(name, raw)) for name, raw in hit["answers"].items() if name in q}
        missing = sorted(set(q) - set(answers))
        return CallResult(
            case.id, self.name, hit.get("model", self.model), answers, hit["latency_ms"],
            hit.get("input_tokens"), hit.get("cost_usd"), error=f"no answer for {missing}" if missing else None,
        )

    def _call(self, state: dict, questions: dict) -> dict:
        raise NotImplementedError


class Jev(Backend):
    name = "jev"

    def __init__(self, model: str = "jev-latest"):
        self.model = model

    def _call(self, state, questions):
        r = _post(JEV_URL, {"model": self.model, "state": state, "questions": questions},
                  {"Authorization": f"Bearer {key('TYPESAFE_API_KEY')}"})
        tokens = r.get("usage", {}).get("input_tokens")
        return {"model": r["model"], "answers": r["answers"], "input_tokens": tokens,
                "cost_usd": tokens * JEV_PRICE_PER_INPUT_TOKEN if tokens else None}


class DryRun(Backend):
    name = "dryrun"

    def __init__(self, out: Path):
        self.out = out

    def ask(self, case):
        with self.out.open("a") as f:
            f.write(json.dumps({"case": case.id, "state": qs.state(case), "questions": qs.questions(case)}, ensure_ascii=False) + "\n")
        return CallResult(case.id, self.name, "", {}, 0.0, None, None)


_BASELINE_PROMPT = """You are a careful Bible translation checker. You get the state of one verse \
(Greek source, the translation, key-term entries and translator notes) and typed questions about it.

Answer every question with probabilities that reflect how sure you are. Return only JSON:
{"<question name>": <answer>, ...}
where <answer> is
- for "noul" (yes/no) questions: {"p_true": <probability the answer is yes/true>}
- for "choice" questions: {"probabilities": {"<label>": <p>, ...}} over all the question's labels, summing to 1
- for "score" questions: {"probabilities": {"0": <p>, "1": <p>, ...}} over all levels, summing to 1"""


class OpenRouter(Backend):
    name = "openrouter"

    def __init__(self, model: str = "anthropic/claude-haiku-5.5"):
        self.model = model

    def _call(self, state, questions):
        r = _post(OPENROUTER_URL, {
            "model": self.model,
            "messages": [
                {"role": "system", "content": _BASELINE_PROMPT},
                {"role": "user", "content": json.dumps({"state": state, "questions": questions}, ensure_ascii=False)},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0,
            "usage": {"include": True},
        }, {"Authorization": f"Bearer {key('OPENROUTER_API_KEY')}"})
        got = parse_json(r["choices"][0]["message"]["content"])
        answers = {}
        for name, q in questions.items():
            if name in got:
                answers[name] = _to_wire(q, got[name])
        usage = r.get("usage", {})
        return {"model": r.get("model", self.model), "answers": answers,
                "input_tokens": usage.get("prompt_tokens"), "cost_usd": usage.get("cost")}


def _to_wire(question: dict, got: dict) -> dict:
    """Convert a baseline LLM's verbal probabilities to Jev's answer shape."""
    if question["type"] == "noul":
        return {"type": "noul", "noul": min(1.0, max(0.0, float(got["p_true"])))}
    labels = list(question["criteria"]) if question["type"] == "choice" else [str(i) for i in range(len(question["criteria"]))]
    probs = {lab: max(0.0, float(got.get("probabilities", {}).get(lab, 0))) for lab in labels}
    total = sum(probs.values()) or 1.0
    probs = {lab: p / total for lab, p in probs.items()}
    best = max(probs, key=probs.get)
    if question["type"] == "choice":
        return {"type": "choice", "choice": best, "confidence": probs[best], "probabilities": probs}
    return {"type": "score", "score": sum(int(lab) * p for lab, p in probs.items()), "confidence": probs[best],
            "probabilities": probs}


def make(spec: str, out_dir: Path | None = None) -> Backend:
    """'jev', 'jev:jev-preview', 'openrouter', 'openrouter:<model id>', 'dryrun'."""
    kind, _, model = spec.partition(":")
    match kind:
        case "jev":
            return Jev(model or "jev-latest")
        case "openrouter":
            return OpenRouter(model or "anthropic/claude-haiku-5.5")
        case "dryrun":
            return DryRun((out_dir or ROOT / "runs") / "requests.jsonl")
    raise ValueError(f"unknown backend {spec!r}")
