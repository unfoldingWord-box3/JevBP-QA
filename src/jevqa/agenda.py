"""Build checking Cases: one per verse, with its key terms and figures attached."""

import csv
import io
import re
from dataclasses import dataclass

from jevqa import sources, usfm
from jevqa.model import Case, Figure, Gold, KeyTerm

# Translation Notes support references that are figures of speech (imagery), the
# ones the "how is this figure handled?" question makes sense for.
FIGURES = {
    "figs-metaphor": "metaphor", "figs-simile": "simile", "figs-personification": "personification",
    "figs-metonymy": "metonymy", "figs-synecdoche": "synecdoche", "figs-idiom": "idiom",
    "figs-hyperbole": "hyperbole", "figs-euphemism": "euphemism", "figs-irony": "irony",
}


@dataclass(frozen=True)
class Target:
    key: str  # source key in sources.SOURCES
    language: str
    version: str
    tw: str | None  # source key of tW in this language, for approved terms


TARGETS = {
    "bsb": Target("bsb", "English", "BSB (Berean Standard Bible)", "en_tw"),
    "hi_irv": Target("hi_irv", "Hindi", "IRV (Indian Revised Version)", "hi_tw"),
    "ar_nav": Target("ar_nav", "Arabic", "NAV (New Arabic Version, Ketab El Hayat)", "ar_tw"),
    "ru_rsob": Target("ru_rsob", "Russian", "RSOB (Russian Simplified Open Bible)", "ru_tw"),
    "ru_rsb": Target("ru_rsb", "Russian", "Russian Synodal Bible (1876)", "ru_tw"),
    "mdg_ssv": Target("mdg_ssv", "Masalit", "Masalit Titus draft", None),
}
PHASES = {"0": ["bsb"], "1": ["hi_irv", "ar_nav"], "1-extra": ["ru_rsob", "ru_rsb"], "2": ["mdg_ssv"]}


def _tsv(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE))


def _article(key: str, slug: str) -> tuple[str, str] | None:
    """(headword line, first paragraph of definition) of a tW article, or None if missing."""
    md = sources.fetch_optional(key, f"bible/{slug}.md")
    if md is None:
        return None
    lines = md.splitlines()
    head = lines[0].lstrip("# ").strip() if lines else ""
    body, started = [], False
    for line in lines[1:]:
        if line.startswith("## "):
            if started:
                break
            started = True
        elif started and line.strip():
            body.append(line.strip())
        elif started and body:
            break
    return head, " ".join(body)


def _note(text: str) -> str:
    return text.replace("\\n", "\n").strip()


def _aligned(verse, words) -> str | None:
    """Aligned rendering, or None. An aligned verse with no words on these Greek words also gives None:
    the checker then has to find the term in the text itself, as it would in an unaligned translation."""
    return usfm.rendering(verse, words) or None if verse else None


def build_cases(target_key: str) -> list[Case]:
    t = TARGETS[target_key]
    greek = usfm.parse_ugnt(sources.fetch("ugnt"))
    verses = usfm.parse_target(sources.fetch(t.key))
    twl = _tsv(sources.fetch("en_twl"))
    tn = _tsv(sources.fetch("en_tn"))

    terms: dict[str, list[KeyTerm]] = {}
    for row in twl:
        ref = row["Reference"]
        if ref not in greek:
            continue
        slug = row["TWLink"].split("/bible/")[-1]
        en = _article("en_tw", slug)
        if en is None:
            continue
        local = (_article(t.tw, slug) if t.tw != "en_tw" else en) if t.tw else None
        words = usfm.find_phrase(greek[ref], row["OrigWords"], int(row["Occurrence"]))
        terms.setdefault(ref, []).append(KeyTerm(
            id=f"kt_{row['ID']}", ref=ref, greek=row["OrigWords"], occurrence=int(row["Occurrence"]),
            article=slug, term=en[0], definition=en[1][:500],
            approved=local[0] if local else None,
            rendering=_aligned(verses.get(ref), words),
        ))

    figures: dict[str, list[Figure]] = {}
    for row in tn:
        kind = FIGURES.get(row["SupportReference"].split("/")[-1])
        ref = row["Reference"]
        if not kind or ref not in greek or not row["Quote"]:
            continue
        words = usfm.find_phrase(greek[ref], row["Quote"], int(row["Occurrence"]))
        figures.setdefault(ref, []).append(Figure(
            id=f"fig_{row['ID']}", ref=ref, kind=kind, quote=row["Quote"], occurrence=int(row["Occurrence"]),
            note=_note(row["Note"]), rendering=_aligned(verses.get(ref), words),
        ))

    cases = []
    for ref, gv in greek.items():
        if ref not in verses:
            continue
        kts, figs = tuple(terms.get(ref, ())), tuple(figures.get(ref, ()))
        cases.append(Case(
            id=ref, ref=ref, language=t.language, version=t.version, greek=gv.text, target=verses[ref].text,
            key_terms=kts, figures=figs,
        ))
    return sorted(cases, key=lambda c: tuple(int(x) for x in re.findall(r"\d+", c.ref)))


def assume_good(cases: list[Case]) -> list[Case]:
    """Attach 'passes' gold to every question: for a published translation we assume it is right.

    This is an assumption, not ground truth. It lets us measure how often the
    checker raises an alarm on text that is (very probably) fine.
    """
    from dataclasses import replace

    from jevqa.questions import question_names

    return [replace(c, gold=tuple(Gold(q, True) for q in question_names(c))) for c in cases]
