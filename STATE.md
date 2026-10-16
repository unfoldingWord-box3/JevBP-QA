# STATE

What this project is, durable lessons, blockers. Not a session log.

## Goal
Measure how well Jev (typesafe.ai "System One" model: typed questions in,
calibrated probabilities out) checks a translation verse by verse against the
Greek (UGNT), driven by unfoldingWord Translation Notes (figures of speech) and
Translation Words Links (key terms). README.md has the method and results.

## Gotchas
- Jev wire format (verified 2026-10-16): POST https://api.typesafe.ai/v1/systemone,
  body {model, state, questions:{name:{type: noul|choice|score, instructions, criteria}}}.
  noul answers are a bare float; choice/score carry probabilities and confidence.
  The Python SDK (typesafe-sdk) pulls in httpx2 and has broken question types
  between minor versions; plain HTTP is used instead.
- `jev-latest` / `jev-preview` are moving aliases (1.13.0 / 1.14.0 on 2026-10-16).
  The response cache key includes the alias, so cached answers can be from an
  older version; each result row records the real version in `model`.
- OpenRouter's `typesafe/jev-router` is a model router, not the systemone endpoint.
- Door43 aligned USFM only carries Greek words that were aligned; the full Greek
  verse must come from UGNT. Occurrence counts are per exact surface form on both
  sides, so alignment matching uses NFC surfaces, not casefolded ones.
- Hindi IRV is aligned to UGNT 0.13, but Titus has zero drift against 0.34.
- BSOJ/ar_nav LICENSE.md is unfoldingWord boilerplate; the manifest and Biblica's
  own repo give CC BY-SA 4.0.
- The Masalit repo uses language code `mdg` (that is Massalat); Masalit is `mls`.
  Its translationCore data has only spelling edits, no checker selections.
- Small-model back-translations can import the remembered Bible text (Hindi 2:15).
- Jev is near-deterministic, not exact: identical requests drift ~0.01 in p (max 0.10
  in English and Hindi, both model versions), and 1-12 of 244 items cross 0.9 between
  runs. On a 31-item question one crossing is ~3 points; treat <5-point gaps as noise.
- BSOJ/ar_tw still has some articles titled in English (circumcise, faith, jew, purify,
  trust); agenda.py treats an ASCII headword in a non-English tW as missing.
- Planted faults must be built once from the full state and shared by every run
  condition (run.cases_for); building them per condition made the ablation unfair.

## Durable lessons
- Measure with planted errors, not just the published text: a checker that always
  says "pass" looks perfect on a good translation.
- Flags that recur across translations point at the checking agenda (TWL links),
  not the translation.

## Paused
- Phase 2b (letter-ciphered BSB as a zero-resource test, issue #4) is paused: a fellow
  developer already did it with Jev + mDeBERTa and reports 66-69% checker time savings on a
  fully ciphered language (cipher by character so patterns still match). Not reproduced here.
  Resume only to compare setups with that developer.

## Blockers
- Real precision needs human labels on a sample of Hindi/Arabic flags.
