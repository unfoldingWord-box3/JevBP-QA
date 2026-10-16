"""Score a run against gold answers: detection, routing load, calibration."""

from dataclasses import dataclass

THRESHOLDS = (0.5, 0.7, 0.8, 0.9, 0.95)


@dataclass(frozen=True)
class Scored:
    case_id: str
    question: str
    kind: str  # key_term | figure_handling | figure_clarity
    source: str  # original | kt_wrong | kt_omit | fig_<label>
    gold_pass: bool
    p_pass: float
    gold_label: str | None = None
    choice: str | None = None


def kind_of(question: str) -> str:
    if question.endswith("_handling"):
        return "figure_handling"
    if question.endswith("_clarity"):
        return "figure_clarity"
    return "key_term"


def scored_rows(results: list[dict]) -> list[Scored]:
    out = []
    for r in results:
        source = r["case_id"].split("~")[1] if "~" in r["case_id"] else "original"
        for g in r["gold"]:
            a = r["answers"].get(g["question"])
            if a is None:
                continue
            out.append(Scored(r["case_id"], g["question"], kind_of(g["question"]), source, g["passes"], a["p_pass"],
                              g.get("handling"), a["raw"].get("choice")))
    return out


def auroc(rows: list[Scored]) -> float | None:
    """Probability a random passing item gets a higher p_pass than a random failing one."""
    good = [r.p_pass for r in rows if r.gold_pass]
    bad = [r.p_pass for r in rows if not r.gold_pass]
    if not good or not bad:
        return None
    wins = sum((g > b) + 0.5 * (g == b) for g in good for b in bad)
    return wins / (len(good) * len(bad))


def at_threshold(rows: list[Scored], t: float) -> dict:
    """Route: p_pass >= t is auto-logged as a pass; everything else goes on for explanation/human review."""
    good = [r for r in rows if r.gold_pass]
    bad = [r for r in rows if not r.gold_pass]
    return {
        "threshold": t,
        "auto_pass_good": sum(r.p_pass >= t for r in good) / len(good) if good else None,
        "escaped_bad": sum(r.p_pass >= t for r in bad) / len(bad) if bad else None,
        "sent_to_review": sum(r.p_pass < t for r in rows) / len(rows) if rows else None,
    }


def calibration(rows: list[Scored], bins: int = 5) -> list[dict]:
    """Predicted pass probability vs how often the item really passed, in equal-width bins."""
    out = []
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        b = [r for r in rows if lo <= r.p_pass < hi or (i == bins - 1 and r.p_pass == 1.0)]
        if b:
            out.append({"bin": f"{lo:.1f}–{hi:.1f}", "n": len(b), "mean_p": sum(r.p_pass for r in b) / len(b),
                        "observed": sum(r.gold_pass for r in b) / len(b)})
    return out


def ece(rows: list[Scored], bins: int = 10) -> float | None:
    if not rows:
        return None
    return sum(c["n"] * abs(c["mean_p"] - c["observed"]) for c in calibration(rows, bins)) / len(rows)


def brier(rows: list[Scored]) -> float | None:
    return sum((r.p_pass - r.gold_pass) ** 2 for r in rows) / len(rows) if rows else None


def handling_confusion(rows: list[Scored]) -> tuple[dict, float | None]:
    """Gold handling label -> predicted label counts, and exact-label accuracy."""
    h = [r for r in rows if r.kind == "figure_handling" and r.gold_label]
    table: dict[str, dict[str, int]] = {}
    for r in h:
        table.setdefault(r.gold_label, {}).setdefault(r.choice or "?", 0)
        table[r.gold_label][r.choice or "?"] += 1
    acc = sum(r.gold_label == r.choice for r in h) / len(h) if h else None
    return table, acc


def summary(rows: list[Scored]) -> dict:
    by_kind = {}
    for kind in ("key_term", "figure_handling", "figure_clarity"):
        rs = [r for r in rows if r.kind == kind]
        if not rs:
            continue
        by_kind[kind] = {
            "n": len(rs), "n_bad": sum(not r.gold_pass for r in rs),
            "auroc": auroc(rs), "brier": brier(rs), "ece": ece(rs),
            "thresholds": [at_threshold(rs, t) for t in THRESHOLDS],
            "calibration": calibration(rs),
            "by_source": {s: {"n": len([r for r in rs if r.source == s]),
                              "mean_p_pass": sum(r.p_pass for r in rs if r.source == s) / len([r for r in rs if r.source == s])}
                          for s in sorted({r.source for r in rs})},
        }
    table, acc = handling_confusion(rows)
    return {"by_kind": by_kind, "handling_confusion": table, "handling_accuracy": acc}
