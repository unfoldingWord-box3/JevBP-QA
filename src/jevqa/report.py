"""runs/<target>/report.md: every backend run so far, side by side."""

import json
import statistics
from pathlib import Path

from jevqa import agenda, evaluate as ev, sources

ROOT = Path(__file__).resolve().parents[2]
T = 0.9  # routing threshold the headline numbers use
KINDS = {"key_term": "Key terms (noul)", "figure_handling": "Figure handling (choice)", "figure_clarity": "Figure clarity (score)"}


def _load(d: Path) -> list[dict]:
    return [json.loads(line) for line in (d / "results.jsonl").open()]


def _pct(x: float | None) -> str:
    return "–" if x is None else f"{100 * x:.0f}%"


def _num(x: float | None, nd: int = 3) -> str:
    return "–" if x is None else f"{x:.{nd}f}"


def headline(results: list[dict]) -> dict:
    rows = ev.scored_rows(results)
    out = {}
    for kind in KINDS:
        rs = [r for r in rows if r.kind == kind]
        real = [r for r in rs if r.source == "original"]
        swaps = [r for r in rs if r.source == "verse_swap"]
        faults = [r for r in rs if not r.gold_pass and r.source != "verse_swap"]
        if not rs:
            continue
        scored = [r for r in rs if r.source != "verse_swap"] if faults else rs  # AUROC on item faults when we have them
        out[kind] = {
            "real_n": len(real), "fault_n": len(faults),
            "real_flagged": sum(r.p_pass < T for r in real) / len(real) if real else None,
            "faults_caught": sum(r.p_pass < T for r in faults) / len(faults) if faults else None,
            "swaps_caught": sum(r.p_pass < T for r in swaps) / len(swaps) if swaps else None,
            "auroc": ev.auroc(scored), "ece": ev.ece(scored),
            "by_source": {src: (sum(r.p_pass < T for r in rs if r.source == src) / n, sum(r.p_pass for r in rs if r.source == src) / n)
                          for src in sorted({r.source for r in rs}) for n in [sum(r.source == src for r in rs)]},
        }
    _, acc = ev.handling_confusion(rows)
    out["handling_accuracy"] = acc
    lat = [r["latency_ms"] for r in results if r["latency_ms"]]
    out["median_latency_ms"] = statistics.median(lat) if lat else None
    out["cost_usd"] = sum(r["cost_usd"] or 0 for r in results)
    out["calls"] = len(results)
    out["models"] = sorted({r["model"] for r in results})
    return out


def write(target: str) -> Path:
    base = ROOT / "runs" / target
    runs = {d.name: _load(d) for d in sorted(base.iterdir()) if (d / "results.jsonl").exists()}
    heads = {n: headline(r) for n, r in runs.items()}
    t = agenda.TARGETS[target]
    lock = json.loads(sources.LOCK.read_text())
    L = [f"# {t.version}: Titus checked against the Greek", ""]
    L += [f"Target `{target}` ({t.language}). Headline threshold: an item is auto-logged as a pass when its pass "
          f"probability is at least {T}; anything lower goes to review.", ""]
    L += ["Sources (pinned commits):", ""]
    for k in dict.fromkeys(("ugnt", "en_tn", "en_twl", "en_tw", t.key, t.tw)):
        if k and k in lock:
            L.append(f"- `{k}`: {lock[k]['repo']} @ `{lock[k]['sha'][:10]}` ({lock[k]['license']})")
    L += ["", "## Speed and cost", "", "| run | model version | calls | median latency | total cost |", "|---|---|---|---|---|"]
    for n, h in heads.items():
        L.append(f"| {n} | {', '.join(h['models'])} | {h['calls']} | {h['median_latency_ms']:.0f} ms | ${h['cost_usd']:.4f} |")
    for kind, title in KINDS.items():
        L += ["", f"## {title}", "",
              "Real flagged = share of the published translation's items sent to review (lower is better if the text is good). "
              "Faults caught = share of seeded item errors sent to review (higher is better). "
              "Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).", "",
              "| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |",
              "|---|---|---|---|---|---|---|---|"]
        for n, h in heads.items():
            k = h.get(kind)
            if k:
                L.append(f"| {n} | {k['real_n']} | {_pct(k['real_flagged'])} | {k['fault_n']} | {_pct(k['faults_caught'])} | {_pct(k['swaps_caught'])} | {_num(k['auroc'])} | {_num(k['ece'])} |")
        srcs = sorted({src for h in heads.values() for src in h.get(kind, {}).get("by_source", {})})
        if srcs:
            L += ["", "By case type: share sent to review / mean pass probability.", "",
                  "| run | " + " | ".join(srcs) + " |", "|---" * (len(srcs) + 1) + "|"]
            for n, h in heads.items():
                bs = h.get(kind, {}).get("by_source", {})
                L.append(f"| {n} | " + " | ".join(f"{_pct(bs[s][0])} / {bs[s][1]:.2f}" if s in bs else "–" for s in srcs) + " |")
        if kind == "figure_handling":
            L += ["", "Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): " +
                  ", ".join(f"{n} {_pct(h['handling_accuracy'])}" for n, h in heads.items())]
    for n, results in runs.items():
        rows = ev.scored_rows(results)
        L += ["", f"## Detail: {n}", ""]
        for kind, title in KINDS.items():
            cal = ev.calibration([r for r in rows if r.kind == kind])
            if cal:
                L += [f"Calibration, {title.lower()}: " + "; ".join(
                    f"{c['bin']}: n={c['n']}, said {c['mean_p']:.2f}, was {c['observed']:.2f}" for c in cal), ""]
        L += ["Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):", "",
              "| question | " + " | ".join(f"t={t}" for t in ev.THRESHOLDS) + " |", "|---" * (len(ev.THRESHOLDS) + 1) + "|"]
        for kind, title in KINDS.items():
            real = [r for r in rows if r.kind == kind and r.source == "original"]
            bad = [r for r in rows if r.kind == kind and not r.gold_pass and r.source != "verse_swap"]
            if real and bad:
                L.append(f"| {title} | " + " | ".join(
                    f"{_pct(sum(r.p_pass < t for r in real) / len(real))} / {_pct(sum(r.p_pass < t for r in bad) / len(bad))}"
                    for t in ev.THRESHOLDS) + " |")
        L.append("")
        table, _ = ev.handling_confusion(rows)
        if table:
            labels = ["kept_clear", "simile", "plain", "lost", "distorted"]
            L += ["Figure handling, gold label (rows) vs answer (columns):", "", "| gold \\ answer | " + " | ".join(labels) + " |",
                  "|---" * (len(labels) + 1) + "|"]
            for g in labels:
                L.append(f"| {g} | " + " | ".join(str(table.get(g, {}).get(a, 0)) for a in labels) + " |")
            L.append("")
        flagged = sorted(((a["p_pass"], r["ref"], q) for r in results if "~" not in r["case_id"]
                          for q, a in r["answers"].items() if a["p_pass"] < T))
        L += [f"Real items flagged at {T}: {len(flagged)}. Lowest ten: " +
              "; ".join(f"{ref} {q} ({p:.2f})" for p, ref, q in flagged[:10]), ""]
    out = base / "report.md"
    out.write_text("\n".join(L) + "\n")
    return out
