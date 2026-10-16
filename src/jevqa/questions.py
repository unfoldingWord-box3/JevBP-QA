"""Turn a Case into a Jev request (state + typed questions), and answers into pass probabilities.

The wire format is TypeSafe's /v1/systemone: `state` is any JSON value,
`questions` maps a name to {type: noul|choice|score, instructions, criteria}.
"""

from jevqa.model import PASSING_HANDLING, Case

HANDLING = {
    "kept_clear": "The same image or figure is kept, and a reader would understand the intended meaning.",
    "simile": "The figure is turned into an explicit comparison (like, as), and the meaning is clear.",
    "plain": "The image is dropped and the intended meaning is stated plainly and correctly.",
    "lost": "The intended meaning is missing or unclear: the figure is left out, or kept so literally that a reader would not get the meaning.",
    "distorted": "The translation says something different from the intended meaning, or the opposite.",
}
CLARITY = [
    "Wrong or misleading: a reader would take a meaning the Greek does not have.",
    "Unclear or awkward: a reader would struggle to get the intended meaning.",
    "Clear, but unnatural or wordy.",
    "Clear and natural: a reader gets the intended meaning easily.",
]
CLARITY_PASS_FROM = 2  # scores at or above this level count as passing


def question_names(case: Case) -> list[str]:
    return [k.id for k in case.key_terms] + [n for f in case.figures for n in (f"{f.id}_handling", f"{f.id}_clarity")]


def state(case: Case) -> dict:
    s = {
        "task": "Bible translation check: compare the translation of one verse against the Greek source text.",
        "reference": f"Titus {case.ref}",
        "greek": case.greek,
        "translation": {"language": case.language, "version": case.version, "text": case.target},
    }
    if case.source_text:
        s["translators_source_text"] = {"version": "ULT (English, the text the translators worked from)", "text": case.source_text}
    if case.back_translation:
        s["translation"]["back_translation_to_english"] = case.back_translation
    if case.key_terms:
        s["key_terms"] = {
            k.id: {
                "greek": k.greek,
                "term": k.term,
                "definition": k.definition,
                **({"approved_terms": k.approved} if k.approved else {}),
                **({"rendering": k.rendering} if k.rendering is not None else {}),
            }
            for k in case.key_terms
        }
    if case.figures:
        s["figures_of_speech"] = {
            f.id: {
                "greek": f.quote,
                "figure": f.kind,
                "translator_note": f.note,
                **({"rendering": f.rendering} if f.rendering is not None else {}),
            }
            for f in case.figures
        }
    return s


def questions(case: Case) -> dict:
    q = {}
    for k in case.key_terms:
        approved = "the approved term (key_terms.{0}.approved_terms)".format(k.id) if k.approved else "a term"
        q[k.id] = {
            "type": "noul",
            "instructions": (
                f"Key term key_terms.{k.id}: the Greek {k.greek!r} means what its definition says. "
                f"In this verse, is it translated with {approved} or an acceptable equivalent that carries "
                f"the same meaning in context?"
            ),
            "criteria": {
                "true": "Translated with the approved term or an acceptable equivalent with the same meaning.",
                "false": "Translated with a wrong term, a term with a different meaning, or left out.",
            },
        }
    for f in case.figures:
        q[f"{f.id}_handling"] = {
            "type": "choice",
            "instructions": (
                f"Figure of speech figures_of_speech.{f.id} ({f.kind}) in the Greek {f.quote!r}; the translator "
                f"note explains its meaning. How does the translation handle it?"
            ),
            "criteria": HANDLING,
        }
        q[f"{f.id}_clarity"] = {
            "type": "score",
            "instructions": (
                f"For figures_of_speech.{f.id}: how clearly and naturally does the translation convey the "
                f"meaning the translator note explains, for an ordinary reader of {case.language}?"
            ),
            "criteria": CLARITY,
        }
    return q


def p_pass(question: str, raw: dict) -> float:
    """Probability that this answer means the check passed."""
    match raw["type"]:
        case "noul":
            return float(raw["noul"])
        case "choice":
            return sum(p for label, p in raw["probabilities"].items() if label in PASSING_HANDLING)
        case "score":
            return sum(p for level, p in raw["probabilities"].items() if int(level) >= CLARITY_PASS_FROM)
    raise ValueError(f"unknown answer type for {question}: {raw}")
