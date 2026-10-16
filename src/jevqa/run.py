"""Run a checker over a target's cases and write results; route the real (unmutated) verses."""

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, replace
from pathlib import Path

from jevqa import agenda, backends, mutate
from jevqa.model import Case, CallResult

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs"
EXPLAIN_MODEL = "google/gemma-4-26b-a4b-it"  # the "small language model" tier


def label(backend: backends.Backend, approved: bool = True, with_source: bool = False) -> str:
    base = f"{backend.name}-{backend.model.split('/')[-1]}" if backend.model else backend.name
    return base + ("" if approved else "+no-approved") + ("+ult" if with_source else "")


def cases_for(target: str, with_mutants: bool, approved: bool = True, with_source: bool = False) -> list[Case]:
    cases = agenda.assume_good(agenda.build_cases(target, approved))
    if with_source:
        from jevqa import sources, usfm
        ult = usfm.parse_target(sources.fetch("en_ult"))
        cases = [replace(c, source_text=ult[c.ref].text) for c in cases]
    if not with_mutants:
        return cases
    faults = mutate.verse_swaps(cases)
    if any(k.rendering for c in cases for k in c.key_terms):  # seeded item faults need an aligned translation
        faults += mutate.key_term_mutants(cases) + mutate.figure_mutants(target, cases)
    return cases + faults


def _row(case: Case, res: CallResult) -> dict:
    return {
        "case_id": case.id, "ref": case.ref, "mutation": case.mutation, "target": case.target,
        "gold": [asdict(g) for g in case.gold],
        "answers": {n: {"raw": a.raw, "p_pass": a.p_pass} for n, a in res.answers.items()},
        "model": res.model, "latency_ms": res.latency_ms, "input_tokens": res.input_tokens,
        "cost_usd": res.cost_usd, "error": res.error,
    }


def run(target: str, backend: backends.Backend, cases: list[Case], workers: int = 8, approved: bool = True,
        with_source: bool = False) -> Path:
    out = RUNS / target / label(backend, approved, with_source)
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


def route(target: str, backend: backends.Backend, t_auto: float = 0.9) -> Path:
    """Three tiers on the real verses: auto-log, small-model explanation (+ recheck), human queue."""
    from jevqa import questions as qs

    out = RUNS / target / label(backend)
    rows = [json.loads(line) for line in (out / "results.jsonl").open()]
    originals = {c.id: c for c in agenda.build_cases(target)}
    tiers, queue = {"auto": 0, "cleared_after_back_translation": 0, "human": 0}, []

    def one(row):
        case = originals[row["case_id"]]
        flagged = [n for n, a in row["answers"].items() if a["p_pass"] < t_auto]
        if not flagged:
            return row, case, flagged, None, None
        ex = explain(case, flagged, qs.state(case))
        recheck = None
        if ex.get("back_translation"):
            recheck = backend.ask(replace(case, back_translation=ex["back_translation"]))
        return row, case, flagged, ex, recheck

    with ThreadPoolExecutor(8) as pool:
        done = list(pool.map(one, [r for r in rows if "~" not in r["case_id"]]))
    for row, case, flagged, ex, recheck in done:
        tiers["auto"] += len(row["answers"]) - len(flagged)
        for n in flagged:
            p2 = recheck.answers[n].p_pass if recheck and n in recheck.answers else None
            if p2 is not None and p2 >= t_auto:
                tiers["cleared_after_back_translation"] += 1
                continue
            tiers["human"] += 1
            queue.append({
                "ref": case.ref, "item": n, "p_pass": round(row["answers"][n]["p_pass"], 3),
                "p_pass_after_bt": None if p2 is None else round(p2, 3),
                "answer": row["answers"][n]["raw"].get("choice") or row["answers"][n]["raw"].get("score") or row["answers"][n]["raw"].get("noul"),
                "greek": next((k.greek for k in case.key_terms if k.id == n), None) or next((f.quote for f in case.figures if n.startswith(f.id)), ""),
                "rendering": next((k.rendering for k in case.key_terms if k.id == n), None) or next((f.rendering for f in case.figures if n.startswith(f.id)), ""),
                "verse": case.target, "back_translation": (ex or {}).get("back_translation", ""),
                "reason": (ex or {}).get("reasons", {}).get(n) or (ex or {}).get("reasons", {}).get(n.rsplit("_", 1)[0], ""),
            })
    queue.sort(key=lambda q: q["p_pass"])
    (out / "routing.json").write_text(json.dumps({"t_auto": t_auto, "tiers": tiers, "explain_model": EXPLAIN_MODEL}, indent=1) + "\n")
    with (out / "human_queue.tsv").open("w") as f:
        cols = list(queue[0]) if queue else ["ref"]
        f.write("\t".join(cols) + "\n")
        for q in queue:
            f.write("\t".join(str(q[c] if q[c] is not None else "").replace("\t", " ").replace("\n", " ") for c in cols) + "\n")
    print(f"routing {target} {label(backend)} at {t_auto}: {tiers}")
    return out
