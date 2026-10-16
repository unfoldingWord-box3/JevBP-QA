"""Seeded faults: copies of verses with one known error, so we can measure detection.

A published translation is (nearly) all passes, so "the checker said pass" tells
us nothing on its own. Each mutant changes one checking item and carries the
answer the checker should give.

- kt_wrong: the key term's rendering replaced by another article's approved term.
- kt_omit: the key term's rendering deleted.
- fig_<label>: an LLM rewrites the figure's rendering in one of the five handling
  styles; the requested style is the gold label. These are generated once and
  saved to data/mutants/<target>.json so the test set is fixed and reviewable.
"""

import json
import random
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

from jevqa import backends
from jevqa.model import PASSING_HANDLING, Case, Gold
from jevqa.questions import HANDLING

ROOT = Path(__file__).resolve().parents[2]
MUTANTS = ROOT / "data" / "mutants"
GENERATOR = "anthropic/claude-sonnet-5.5"


def _first_term(approved: str | None, fallback: str) -> str:
    return (approved or fallback).split(",")[0].strip()


# Leading function words that alignment groups carry along with the content word ("of God", "an apostle").
# Mutants replace only the content, so the fault is a wrong word, not broken grammar.
_LEADING = {
    "English": {"a", "an", "the", "of", "to", "for", "in", "by", "with", "his", "her", "their", "our", "my", "your", "its", "and"},
    "Russian": {"в", "во", "на", "с", "со", "к", "ко", "по", "о", "об", "от", "для", "из", "у", "за", "и"},
}


def _core(rendering: str, language: str) -> str:
    words = rendering.split()
    while len(words) > 1 and words[0].lower() in _LEADING.get(language, set()):
        words = words[1:]
    return " ".join(words)


def _replace_once(text: str, old: str, new: str) -> str | None:
    """Replace the first whole-word occurrence; None if not found."""
    m = re.search(rf"(?<!\w){re.escape(old)}(?!\w)", text)
    if not m:
        return None
    out = text[:m.start()] + new + text[m.end():]
    return re.sub(r"\s+", " ", re.sub(r"\s+([,.;:!?])", r"\1", out)).strip()


def key_term_mutants(cases: list[Case], seed: int = 7) -> list[Case]:
    rng = random.Random(seed)
    pool = sorted({(k.article, _first_term(k.approved, k.term)) for c in cases for k in c.key_terms if k.article.startswith("kt/")})
    out = []
    for c in cases:
        for k in c.key_terms:
            if not k.rendering or "…" in k.rendering or not k.article.startswith("kt/"):
                continue
            core = _core(k.rendering, c.language)
            others = [t for a, t in pool if a != k.article and t.lower() not in k.rendering.lower()]
            wrong = rng.choice(others)
            for kind, new, rendering in (("kt_wrong", wrong, k.rendering.replace(core, wrong)), ("kt_omit", "", "")):
                text = _replace_once(c.target, core, new)
                if not text or text == c.target:
                    continue
                out.append(replace(
                    c, id=f"{c.id}~{kind}~{k.id}", target=text, figures=(),
                    key_terms=(replace(k, rendering=rendering),),
                    gold=(Gold(k.id, False),),
                    mutation=f"{k.id}: {core!r} -> {new!r}",
                ))
    return out


_GEN_PROMPT = """You help build a test set for a Bible translation checker. Given one verse \
(Greek, a {language} translation, a figure of speech in the Greek, and a translator note that \
explains it), write five versions of the {language} verse. Each version changes ONLY the part that \
renders the figure (currently: {rendering!r}); keep everything else word for word.

Versions:
{styles}

Return only JSON: {{"<style>": {{"verse": "<full verse>", "rendering": "<the words that now render the figure, or empty if removed>"}}, ...}} \
with the five keys kept_clear, simile, plain, lost, distorted."""


def _generate(case: Case, fig) -> dict:
    styles = "\n".join(f"- {k}: {v}" for k, v in HANDLING.items())
    body = {
        "model": GENERATOR,
        "messages": [{"role": "user", "content": _GEN_PROMPT.format(language=case.language, rendering=fig.rendering, styles=styles) +
                      "\n\n" + json.dumps({"greek": case.greek, "translation": case.target, "figure": fig.kind,
                                           "greek_quote": fig.quote, "translator_note": fig.note}, ensure_ascii=False)}],
        "response_format": {"type": "json_object"},
        "temperature": 0.3,
    }
    for attempt in range(3):
        r = backends._post(backends.OPENROUTER_URL, body, {"Authorization": f"Bearer {backends.key('OPENROUTER_API_KEY')}"})
        try:
            got = backends.parse_json(r["choices"][0]["message"]["content"])
            if set(HANDLING) <= set(got):
                return got
        except ValueError:
            pass
    raise RuntimeError(f"generator gave no usable variants for {fig.id}")


def figure_mutants(target: str, cases: list[Case]) -> list[Case]:
    path = MUTANTS / f"{target}.json"
    saved = json.loads(path.read_text()) if path.exists() else {}
    todo = [(c, f) for c in cases for f in c.figures if f.id not in saved and f.rendering]
    if todo:
        with ThreadPoolExecutor(8) as pool:
            for (c, f), got in zip(todo, pool.map(lambda cf: _generate(*cf), todo)):
                saved[f.id] = {"ref": c.ref, "original": c.target, "variants": got, "generator": GENERATOR}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + "\n")
    out = []
    for c in cases:
        for f in c.figures:
            for label, v in saved.get(f.id, {}).get("variants", {}).items():
                if label not in HANDLING or not v.get("verse") or v["verse"] == c.target and label in ("lost", "distorted"):
                    continue
                passes = label in PASSING_HANDLING
                out.append(replace(
                    c, id=f"{c.id}~fig_{label}~{f.id}", target=v["verse"], key_terms=(),
                    figures=(replace(f, rendering=v.get("rendering", "")),),
                    gold=(Gold(f"{f.id}_handling", passes, label), Gold(f"{f.id}_clarity", passes)),
                    mutation=f"{f.id}: rewritten as {label}",
                ))
    return out
