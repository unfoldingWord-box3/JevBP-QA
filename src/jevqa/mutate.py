"""Seeded faults: copies of verses with one known error, so we can measure detection.

A published translation is (nearly) all passes, so "the checker said pass" tells
us nothing on its own. Each mutant changes one checking item and carries the
answer the checker should give.

- kt_wrong: the key term's rendering replaced by another article's approved term.
- kt_omit: the key term's rendering deleted.
- verse_swap: the translation text of a far-away verse under this verse's Greek.
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
    """First headword of a tW title: 'repent, repentance' -> 'repent' (Arabic titles use '،')."""
    return re.split(r"[,،;/(]", approved or fallback)[0].strip()


# Leading function words that alignment groups carry along with the content word ("of God", "an apostle").
# Mutants replace only the content, so the fault is a wrong word, not broken grammar.
_LEADING = {
    "English": {"a", "an", "the", "of", "to", "for", "in", "by", "with", "his", "her", "their", "our", "my", "your", "its", "and"},
    "Russian": {"в", "во", "на", "с", "со", "к", "ко", "по", "о", "об", "от", "для", "из", "у", "за", "и"},
}


# Hindi postpositions follow the noun ("परमेश्वर का").
_TRAILING = {"Hindi": {"का", "के", "की", "को", "से", "में", "ने", "पर", "तक", "और"}}


def _core(rendering: str, language: str) -> str:
    words = rendering.split()
    while len(words) > 1 and words[0].lower() in _LEADING.get(language, set()):
        words = words[1:]
    while len(words) > 1 and words[-1] in _TRAILING.get(language, set()):
        words = words[:-1]
    return " ".join(words)


def _replace_unique(text: str, old: str, new: str) -> str | None:
    """Replace a whole-word occurrence that appears exactly once; None if absent or ambiguous.

    With two matches we cannot tell which one the alignment points at, and editing the
    wrong one would leave the key term intact under a 'fail' label.
    """
    found = list(re.finditer(rf"(?<!\w){re.escape(old)}(?!\w)", text))
    if len(found) != 1:
        return None
    m = found[0]
    out = text[:m.start()] + new + text[m.end():]
    return re.sub(r"\s+", " ", re.sub(r"\s+([,.;:!?])", r"\1", out)).strip()


def key_term_mutants(cases: list[Case], seed: int = 7) -> list[Case]:
    """Needs cases built with approved terms, so wrong terms come from the target language's tW."""
    rng = random.Random(seed)
    pool = sorted({(k.article, _first_term(k.approved, k.term)) for c in cases for k in c.key_terms if k.article.startswith("kt/")})
    out = []
    for c in cases:
        for k in c.key_terms:
            if not k.rendering or "…" in k.rendering or not k.article.startswith("kt/"):
                continue
            core = _core(k.rendering, c.language)
            others = [t for a, t in pool if a != k.article and t.lower() not in k.rendering.lower()]
            if not others:
                continue
            wrong = rng.choice(others)
            for kind, new, rendering in (("kt_wrong", wrong, k.rendering.replace(core, wrong)), ("kt_omit", "", None)):
                text = _replace_unique(c.target, core, new)
                if not text or text == c.target:
                    continue
                out.append(replace(
                    c, id=f"{c.id}~{kind}~{k.id}", target=text, figures=(),
                    key_terms=(replace(k, rendering=rendering),),
                    gold=(Gold(k.id, False),),
                    mutation=f"{k.id}: {core!r} -> {new!r}",
                ))
    return out


def verse_swaps(cases: list[Case], offset: int = 23) -> list[Case]:
    """The translation text of a far-away verse under this verse's Greek: items should fail.

    A floor test. Key terms whose tW article also occurs in the swapped-in verse ("God our
    Savior" in both 1:3 and 2:10) may truly be present, so they get no gold answer.
    """
    out = []
    for i, c in enumerate(cases):
        other = cases[(i + offset) % len(cases)]
        if other.ref == c.ref:
            continue
        shared = {k.id for k in c.key_terms if k.article in {o.article for o in other.key_terms}}
        out.append(replace(
            c, id=f"{c.id}~verse_swap~{other.ref}", target=other.target,
            key_terms=tuple(replace(k, rendering=None) for k in c.key_terms),
            figures=tuple(replace(f, rendering=None) for f in c.figures),
            gold=tuple(Gold(g.question, False, "lost" if g.question.endswith("_handling") else None)
                       for g in c.gold if g.question not in shared),
            mutation=f"translation text replaced by {other.ref}",
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
        try:
            r = backends._post(backends.OPENROUTER_URL, body, {"Authorization": f"Bearer {backends.key('OPENROUTER_API_KEY')}"})
            got = backends.parse_json(r["choices"][0]["message"]["content"])
            if set(HANDLING) <= set(got):
                return got
        except (ValueError, KeyError, RuntimeError):
            pass
    return None


def figure_mutants(target: str, cases: list[Case]) -> list[Case]:
    path = MUTANTS / f"{target}.json"
    saved = json.loads(path.read_text()) if path.exists() else {}
    todo = [(c, f) for c in cases for f in c.figures if f.id not in saved and f.rendering]
    if todo:
        with ThreadPoolExecutor(8) as pool:
            for (c, f), got in zip(todo, pool.map(lambda cf: _generate(*cf), todo)):
                if got is None:
                    print(f"  generator failed for {f.id}; skipped (re-run to retry)")
                    continue
                saved[f.id] = {"ref": c.ref, "original": c.target, "variants": got, "generator": GENERATOR}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + "\n")
    audit_path = MUTANTS / f"{target}.audit.json"
    audit = json.loads(audit_path.read_text()) if audit_path.exists() else {}
    out = []
    for c in cases:
        for f in c.figures:
            if saved.get(f.id, {}).get("original", c.target) != c.target:
                raise RuntimeError(f"{path}: {f.id} was generated from different verse text; delete it to regenerate")
            for asked, v in saved.get(f.id, {}).get("variants", {}).items():
                if asked not in HANDLING or not v.get("verse") or v["verse"] == c.target and asked in ("lost", "distorted"):
                    continue
                case_id = f"{c.id}~fig_{asked}~{f.id}"
                fix = audit.get(case_id, {})  # a human/LLM audit can correct the generator
                label = fix.get("label", asked)
                passes = label in PASSING_HANDLING
                out.append(replace(
                    c, id=case_id, target=v["verse"], key_terms=(),
                    figures=(replace(f, rendering=v.get("rendering") or None),),  # empty -> absent, as for real text
                    gold=(Gold(f"{f.id}_handling", passes, label), Gold(f"{f.id}_clarity", fix.get("clarity_passes", passes))),
                    mutation=f"{f.id}: rewritten as {asked}" + (f" (audited: {label})" if label != asked else ""),
                ))
    return out
