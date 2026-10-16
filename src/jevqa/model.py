"""Data shapes. Everything else passes these around.

Verse-level text comes from USFM; checking items come from unfoldingWord
Translation Words Links (key terms) and Translation Notes (figures of speech),
both anchored to Greek words, so they attach to any translation aligned to
the Greek.
"""

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class GreekWord:
    surface: str
    lemma: str
    strong: str
    occurrence: int  # nth time this surface form appears in the verse, from 1


@dataclass(frozen=True)
class Alignment:
    """One aligned group: Greek words (by surface + occurrence) to target words."""

    greek: tuple[tuple[str, int], ...]
    target: tuple[int, ...]  # indexes into TargetVerse.words


@dataclass(frozen=True)
class GreekVerse:
    ref: str  # "1:5"
    words: tuple[GreekWord, ...]

    @property
    def text(self) -> str:
        return " ".join(w.surface for w in self.words)


@dataclass(frozen=True)
class TargetVerse:
    ref: str
    text: str
    words: tuple[str, ...]
    alignments: tuple[Alignment, ...] = ()  # empty when the translation is not aligned


@dataclass(frozen=True)
class KeyTerm:
    """A Translation Words Links row: a Greek word or phrase tied to a tW article."""

    id: str
    ref: str
    greek: str  # OrigWords
    occurrence: int
    article: str  # "kt/repent"
    term: str  # English tW headword line, e.g. "repent, repentance"
    definition: str  # English tW definition, first paragraph
    approved: str | None  # headword of the tW article in the target language, if one exists
    rendering: str | None  # target words aligned to the Greek, if aligned


@dataclass(frozen=True)
class Figure:
    """A Translation Notes row about a figure of speech."""

    id: str
    ref: str
    kind: str  # "metaphor", "personification", ...
    quote: str  # Greek
    occurrence: int
    note: str
    rendering: str | None


Handling = Literal["kept_clear", "simile", "plain", "lost", "distorted"]
PASSING_HANDLING: frozenset[str] = frozenset({"kept_clear", "simile", "plain"})


@dataclass(frozen=True)
class Gold:
    """Known correct answer for one question, for evaluation."""

    question: str
    passes: bool
    handling: Handling | None = None  # for figure-handling questions


@dataclass(frozen=True)
class Case:
    """One call to the checker: a verse (possibly mutated) and its checking items."""

    id: str  # "1:5" for an original verse, "1:5~kt_wrong~zfgc" for a mutant
    ref: str
    language: str
    version: str
    greek: str
    target: str
    key_terms: tuple[KeyTerm, ...]
    figures: tuple[Figure, ...]
    gold: tuple[Gold, ...] = ()
    mutation: str | None = None  # what was changed, in words, for mutants
    back_translation: str | None = None  # added by the explain tier before a recheck


@dataclass
class Answer:
    """One question's answer in Jev's wire shape, plus the pass probability we route on."""

    question: str
    raw: dict  # {"type": "noul", "noul": 0.93} etc., exactly as the backend returned it
    p_pass: float


@dataclass
class CallResult:
    case_id: str
    backend: str
    model: str
    answers: dict[str, Answer]
    latency_ms: float
    input_tokens: int | None
    cost_usd: float | None
    error: str | None = None
    meta: dict = field(default_factory=dict)
