"""Parser and scoring checks on small hand-written USFM, plus the pinned Titus data."""

from jevqa import agenda, questions, usfm
from jevqa.evaluate import Scored, auroc

UGNT = r"""\c 1
\p
\v 1
\w Παῦλος|lemma="Παῦλος" strong="G39720"\w*,
\w δοῦλος|lemma="δοῦλος" strong="G14010"\w*
\w Θεοῦ|lemma="θεός" strong="G23160"\w*,
\w καὶ|lemma="καί" strong="G25320"\w*
\w Θεοῦ|lemma="θεός" strong="G23160"\w*
"""

ALIGNED = r"""\c 1
\s1 A heading that is not verse text
\p
\v 1 \zaln-s |x-content="Παῦλος" x-occurrence="1"\*\w Paul|x-occurrence="1"\w*\zaln-e\*,
\zaln-s |x-content="δοῦλος" x-occurrence="1"\*\w a|x-occurrence="1"\w*
\w servant|x-occurrence="1"\w*\zaln-e\*
\zaln-s |x-content="Θεοῦ" x-occurrence="1"\*\zaln-s |x-content="καὶ" x-occurrence="1"\*\w of|x-occurrence="1"\w*
\w God|x-occurrence="1"\w*\zaln-e\*\zaln-e\* and
\zaln-s |x-content="Θεοῦ" x-occurrence="2"\*\w God|x-occurrence="2"\w*\zaln-e\*\f + \ft a footnote\f*.
"""


def test_ugnt_occurrences_count_per_surface():
    v = usfm.parse_ugnt(UGNT)["1:1"]
    assert [w.occurrence for w in v.words] == [1, 1, 1, 1, 2]


def test_aligned_text_skips_headings_and_footnotes():
    t = usfm.parse_target(ALIGNED)["1:1"]
    assert t.text == "Paul, a servant of God and God."
    assert len(t.alignments) == 4
    # nested zaln-s: both Greek words share the same target words
    assert t.alignments[2].greek == (("Θεοῦ", 1), ("καὶ", 1))


def test_rendering_respects_occurrence_and_gaps():
    g, t = usfm.parse_ugnt(UGNT)["1:1"], usfm.parse_target(ALIGNED)["1:1"]
    assert usfm.rendering(t, usfm.find_phrase(g, "δοῦλος", 1)) == "a servant"
    assert usfm.rendering(t, usfm.find_phrase(g, "Θεοῦ", 2)) == "God"
    assert usfm.rendering(t, usfm.find_phrase(g, "Παῦλος & Θεοῦ", 1)) == "Paul … of God"


def test_find_phrase_ignores_case_and_punctuation():
    g = usfm.parse_ugnt(UGNT)["1:1"]
    assert [w.surface for w in usfm.find_phrase(g, "θεοῦ καὶ", 1)] == ["Θεοῦ", "καὶ"]
    assert usfm.find_phrase(g, "Θεοῦ", 3) == []


def test_p_pass_per_answer_type():
    assert questions.p_pass("k", {"type": "noul", "noul": 0.8}) == 0.8
    assert questions.p_pass("f_handling", {"type": "choice", "probabilities": {"kept_clear": 0.5, "plain": 0.2, "lost": 0.3}}) == 0.7
    assert questions.p_pass("f_clarity", {"type": "score", "probabilities": {"0": 0.1, "1": 0.2, "2": 0.3, "3": 0.4}}) == 0.7


def test_auroc():
    rows = [Scored("a", "q", "key_term", "original", True, 0.9), Scored("b", "q", "key_term", "kt_wrong", False, 0.1)]
    assert auroc(rows) == 1.0


def test_titus_bsb_every_item_resolves():
    """On the pinned data, every key term and figure finds its Greek words and BSB rendering."""
    cases = agenda.build_cases("bsb")
    assert len(cases) == 46
    assert sum(len(c.key_terms) for c in cases) == 182
    assert all(k.rendering for c in cases for k in c.key_terms)
    assert all(f.rendering for c in cases for f in c.figures)


def test_planted_term_needs_a_unique_match():
    from jevqa.mutate import _replace_unique

    assert _replace_unique("God sent God's Son", "God", "grace") is None  # ambiguous: which one is aligned?
    assert _replace_unique("the grace of God", "grace", "wrath") == "the wrath of God"


def test_conditions_share_one_fault_set():
    """Ablations must be scored on the same planted cases, or the comparison means nothing."""
    from jevqa import run

    full = run.cases_for("hi_irv")
    for cond in (run.Condition(approved=False), run.Condition(renderings=False)):
        other = run.cases_for("hi_irv", cond)
        assert [(c.id, c.target) for c in other] == [(c.id, c.target) for c in full]
    assert not any(k.approved for c in run.cases_for("hi_irv", run.Condition(approved=False)) for k in c.key_terms)
    bare = run.cases_for("hi_irv", run.Condition(renderings=False))
    assert not any(k.rendering for c in bare for k in c.key_terms)
    assert not any(f.rendering for c in bare for f in c.figures)
