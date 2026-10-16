"""Run a checker over a target's cases and write results; route the real (unmutated) verses."""

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, replace
from pathlib import Path

from dataclasses import dataclass

from jevqa import agenda, backends, mutate
from jevqa import questions as qs
from jevqa.model import Case, CallResult

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs"
EXPLAIN_MODEL = "google/gemma-4-26b-a4b-it"  # the "small language model" tier


@dataclass(frozen=True)
class Condition:
    """What goes into the state. Each non-default choice gets its own run directory."""

    mutants: bool = True  # add planted faults
    approved: bool = True  # target-language tW headwords as approved terms
    renderings: bool = True  # aligned target words for each item
    source: bool = False  # the English ULT verse (the Masalit team's source text)

    def suffix(self) -> str:
        return ("" if self.mutants else "+no-mutants") + ("" if self.approved else "+no-approved") + \
            ("" if self.renderings else "+no-renderings") + ("+ult" if self.source else "")


def label(backend: backends.Backend, cond: Condition = Condition()) -> str:
    base = f"{backend.name}-{backend.model.split('/')[-1]}" if backend.model else backend.name
    return base + cond.suffix()


def cases_for(target: str, cond: Condition = Condition()) -> list[Case]:
    # Faults are always built from the full state, so every condition is scored on the same fault set;
    # the condition then removes fields from real and planted cases alike.
    cases = agenda.assume_good(agenda.build_cases(target))
    if cond.source:
        from jevqa import sources, usfm
        ult = usfm.parse_target(sources.fetch("en_ult"))
        cases = [replace(c, source_text=ult[c.ref].text) for c in cases]
    if cond.mutants:
        faults = mutate.verse_swaps(cases)
        if any(k.rendering for c in cases for k in c.key_terms):  # seeded item faults need an aligned translation
            faults += mutate.key_term_mutants(cases) + mutate.figure_mutants(target, cases)
        cases = cases + faults
    if not cond.approved:
        cases = [replace(c, key_terms=tuple(replace(k, approved=None) for k in c.key_terms)) for c in cases]
    if not cond.renderings:
        cases = [replace(c, key_terms=tuple(replace(k, rendering=None) for k in c.key_terms),
                         figures=tuple(replace(f, rendering=None) for f in c.figures)) for c in cases]
    return cases


def _row(case: Case, res: CallResult) -> dict:
    return {
        "case_id": case.id, "ref": case.ref, "mutation": case.mutation, "target": case.target,
        "gold": [asdict(g) for g in case.gold],
        "answers": {n: {"raw": a.raw, "p_pass": a.p_pass} for n, a in res.answers.items()},
        "model": res.model, "latency_ms": res.latency_ms, "input_tokens": res.input_tokens,
        "cost_usd": res.cost_usd, "error": res.error,
    }


def run(target: str, backend: backends.Backend, cond: Condition = Condition(), workers: int = 8) -> Path:
    cases = cases_for(target, cond)
    out = RUNS / target / label(backend, cond)
    out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(backend.ask, cases))
    with (out / "results.jsonl").open("w") as f:
        for c, r in zip(cases, results):
            f.write(json.dumps(_row(c, r), ensure_ascii=False) + "\n")
    errors = [r for r in results if r.error]
    print(f"{target} {out.name}: {len(results)} calls, {len(errors)} with errors -> {out}")
    for r in errors[:5]:
        print("  error", r.case_id, r.error[:200])
    return out


_EXPLAIN_PROMPT = """You help a human Bible translation checker. A checking tool flagged items in this verse \
as possibly wrong or uncertain. For each flagged item, write ONE short sentence saying what the translation \
does with it and why a checker might worry (or why it is probably fine). {bt}Return only JSON: \
{{{bt_key}"reasons": {{"<item id>": "<one sentence>", ...}}}}"""


def explain(case: Case, flagged: list[str], state: dict) -> dict:
    """Small-model tier: back-translation (non-English only) and a short reason per flagged item."""
    english = case.language == "English"
    prompt = _EXPLAIN_PROMPT.format(
        bt="" if english else "Also give a literal back-translation of the whole verse into English. ",
        bt_key="" if english else '"back_translation": "<English>", ',
    )
    body = {
        "model": EXPLAIN_MODEL,
        "messages": [{"role": "user", "content": prompt + "\n\n" + json.dumps({"verse": state, "flagged_items": flagged}, ensure_ascii=False)}],
        "response_format": {"type": "json_object"}, "temperature": 0, "usage": {"include": True},
    }
    r = backends._post(backends.OPENROUTER_URL, body, {"Authorization": f"Bearer {backends.key('OPENROUTER_API_KEY')}"})
    got = backends.parse_json(r["choices"][0]["message"]["content"])
    got["cost_usd"] = r.get("usage", {}).get("cost")
    return got


def route(target: str, backend: backends.Backend, cond: Condition = Condition(), t_auto: float = 0.9) -> Path:
    """Three tiers on the real verses: auto-log, small-model explanation (+ recheck), human queue.

    Items the checker gave no answer for (API error, partial reply) go straight to the human queue.
    """
    out = RUNS / target / label(backend, cond)
    rows = [json.loads(line) for line in (out / "results.jsonl").open()]
    originals = {c.id: c for c in cases_for(target, replace(cond, mutants=False))}
    tiers, queue = {"auto": 0, "cleared_after_back_translation": 0, "human": 0}, []

    def one(row):
        case = originals[row["case_id"]]
        flagged = [n for n in qs.question_names(case) if n not in row["answers"] or row["answers"][n]["p_pass"] < t_auto]
        if not flagged:
            return row, case, flagged, None, None
        try:
            ex = explain(case, flagged, qs.state(case))
        except Exception as e:  # the human still gets the item, just without an explanation
            ex = {"error": str(e)[:200]}
        recheck = None
        if ex.get("back_translation"):
            recheck = backend.ask(replace(case, back_translation=ex["back_translation"]))
        return row, case, flagged, ex, recheck

    with ThreadPoolExecutor(8) as pool:
        done = list(pool.map(one, [r for r in rows if "~" not in r["case_id"]]))
    for row, case, flagged, ex, recheck in done:
        tiers["auto"] += len(qs.question_names(case)) - len(flagged)
        for n in flagged:
            # an item the checker never answered goes to a human; a recheck cannot clear it
            p2 = recheck.answers[n].p_pass if recheck and n in recheck.answers and n in row["answers"] else None
            if p2 is not None and p2 >= t_auto:
                tiers["cleared_after_back_translation"] += 1
                continue
            tiers["human"] += 1
            a = row["answers"].get(n)
            queue.append({
                "ref": case.ref, "item": n, "p_pass": round(a["p_pass"], 3) if a else 0.0,
                "p_pass_after_bt": None if p2 is None else round(p2, 3),
                "answer": (a["raw"].get("choice") or a["raw"].get("score") or a["raw"].get("noul")) if a else f"no answer: {row.get('error')}",
                "greek": next((k.greek for k in case.key_terms if k.id == n), None) or next((f.quote for f in case.figures if n.startswith(f.id)), ""),
                "rendering": next((k.rendering for k in case.key_terms if k.id == n), None) or next((f.rendering for f in case.figures if n.startswith(f.id)), ""),
                "verse": case.target, "back_translation": (ex or {}).get("back_translation", ""),
                "reason": (ex or {}).get("reasons", {}).get(n) or (ex or {}).get("reasons", {}).get(n.rsplit("_", 1)[0], "")
                or (f"explanation failed: {ex['error']}" if ex and "error" in ex else ""),
            })
    queue.sort(key=lambda q: q["p_pass"])
    (out / "routing.json").write_text(json.dumps({"t_auto": t_auto, "tiers": tiers, "explain_model": EXPLAIN_MODEL}, indent=1) + "\n")
    with (out / "human_queue.tsv").open("w") as f:
        cols = list(queue[0]) if queue else ["ref"]
        f.write("\t".join(cols) + "\n")
        for q in queue:
            f.write("\t".join(str(q[c] if q[c] is not None else "").replace("\t", " ").replace("\n", " ") for c in cols) + "\n")
    print(f"routing {target} {out.name} at {t_auto}: {tiers}")
    return out
