# JevBP-QA: can a fast decision model check Bible translations?

An R&D test of [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), TypeSafe AI's
"System One" model, as a first-pass translation checker. Jev does not write text. You give it a
block of facts and a set of typed questions (yes/no, multiple choice, or a score), and it returns a
probability for each answer in about a quarter of a second.

The idea under test came from the team: for each verse, give Jev the Greek, the translation with its
word alignment, the relevant unfoldingWord Translation Notes and Translation Words entries, ask
several checking questions in one call, then route the answers by confidence. Confident passes are
logged automatically, doubtful items get a short explanation from a small language model, and what
remains goes to human checkers.

We ran it on the letter to Titus in three settings:

| Phase | Translation | Language model support | Word-aligned to the Greek? |
|---|---|---|---|
| 0 | BSB (Berean Standard Bible) | English: strong | yes |
| 1 | IRV (Indian Revised Version) and NAV (New Arabic Version, Ketab El Hayat) | Hindi, Arabic: good | yes |
| 2 | Masalit Titus draft | Masalit: none | no |

## Short version

- **Jev catches planted errors in languages it can read.** When we planted a wrong key term or
  deleted one, Jev sent 97–100% of those items to review in English, Hindi, and Arabic. When we
  rewrote a figure of speech so its meaning was lost or distorted, it caught 98–100%. Detection
  holds when the aligned words are left out of the request, so Jev is reading the verse.
- **It also flags some good text.** On the published translations (which we assume are mostly
  right), Jev sent 17% of English key-term items to review, and 31% of Hindi and Arabic ones, at
  our default cut-off of 0.9. A looser cut-off trades these: in English at 0.8, 8% of good items
  were flagged and 98% of planted errors still caught.
- **Many English key-term flags are not about the English.** Of the 31 BSB key terms Jev flagged,
  25 were also flagged in Hindi or Arabic, and 17 in both. These point at the checking agenda (for
  example a Translation Words link whose article does not fit the verse), not at the translation.
  Only 6 BSB key-term flags were unique to the BSB, against 17 for Hindi and 16 for Arabic. Flags
  unique to one translation are the ones worth a checker's time first.
- **An ordinary LLM catches errors as well, and ranks slightly better, but is a poor router.**
  Claude Haiku 5.5, asked the same questions, caught the same planted errors. On real verses it took
  about 14 times as long (3.6–3.9 s against 0.26 s) and cost about 7 times as much. On real figures of
  speech it spread its answer across several options and sent 84–97% of them to review, against
  13–48% for Jev.
- **On Masalit, Jev knows it can't read the text.** Its answers sit near 50/50 and 99–100% of items
  go to human review. It barely tells a real Masalit verse from a different verse pasted in its
  place, and adding the English source text the translators used does not help. Zero-shot
  checking of a language with no model support does not work this way. Jev needs something it
  can read: an alignment, a key-term glossary, or a human back-translation.
- **Cost is negligible.** The published results took 5,355 distinct Jev calls costing $0.24, about
  $0.00007–0.00008 per real verse (a real verse asks up to 11 questions in one call).

## How it works

For each verse the pipeline builds one Jev request:

1. **State** (the facts): the Greek verse from the unfoldingWord Greek New Testament (UGNT); the
   translation's verse text; and for each checking item, the Greek words, the target words aligned
   to them, and the matching Translation Notes or Translation Words entry.
2. **Questions** (asked together in one call):
   - **Key terms** (yes/no, Jev's "noul" type), one per Translation Words Links entry: "Is this term
     translated with the approved term or an acceptable equivalent that carries the same meaning
     in context?" The "approved term" is the Translation Words article's headword in that language
     (English, Hindi, or Arabic tW), where one exists.
   - **Figure handling** (choice), one per figure-of-speech note (metaphor, personification,
     metonymy, synecdoche, idiom, hyperbole, and similar): kept and clear / changed to a simile /
     meaning stated plainly / meaning lost / meaning distorted.
   - **Figure clarity** (score 0–3): from "wrong or misleading" to "clear and natural".
3. **Routing**: each answer becomes a probability that the item passes. At 0.9 or above it is
   logged as a pass. Below that, a small model (Gemma 4, 26B) writes a one-line reason and, for
   non-English text, an English back-translation. Jev then re-checks with the back-translation
   added. Items that still fall short, and any item the checker failed to answer, go to the human
   queue (`runs/<target>/<run>/human_queue.tsv`).

Titus has 46 verses, 182 Translation Words Links entries, and 31 figure-of-speech notes, so a run
over the real text asks 244 questions in 46 calls.

Here is the Titus 1:1 state, cut down:

```json
{
  "reference": "Titus 1:1",
  "greek": "Παῦλος δοῦλος Θεοῦ ἀπόστολος δὲ Ἰησοῦ Χριστοῦ κατὰ πίστιν ...",
  "translation": {"language": "English", "version": "BSB", "text": "Paul, a servant of God and an apostle of Jesus Christ ..."},
  "key_terms": {
    "kt_zfgc": {"greek": "δοῦλος", "term": "servant, serve, ...", "definition": "...", "approved_terms": "servant, serve, ...", "rendering": "a servant"}
  }
}
```

## How we measured

A published translation is nearly all passes, so "Jev said pass" proves nothing on its own: a checker
that always says pass would score perfectly. We built test cases with known answers:

| Case type | What it is | Correct answer |
|---|---|---|
| Real verse | The published text, unchanged | Assumed pass. This is an assumption: some flags on real text may be real problems. |
| Wrong term | The aligned rendering of a key term swapped for another Translation Words headword in the same language (e.g. "Savior" → "good"); tW articles still titled in English are left out of the pool | Fail |
| Omitted term | The rendering of a key term deleted | Fail |
| Figure rewrite | Claude Sonnet 5.5 rewrote each figure five ways (kept clear, simile, plain, lost, distorted) in the target language | Pass for the first three, fail for lost and distorted |
| Verse swap | The translation text of a far-away verse placed under this verse's Greek | Fail, except key terms whose Translation Words article is also linked in the swapped-in verse, which are not scored |

Wrong and omitted terms are planted only where the rendering occurs once in the verse, so the edit
always hits the aligned word. Every run condition below uses the same set of planted cases.

Each case is scored at a cut-off: below 0.9 means "sent to review". The tables report:

- **Real flagged**: share of real items sent to review (lower is better, if the text is good).
- **Faults caught**: share of planted errors sent to review (higher is better).
- **AUROC**: the chance a random good item gets a higher pass probability than a random bad one
  (1.0 is perfect, 0.5 is a coin flip). This measures ranking regardless of cut-off.
- **ECE** (expected calibration error): how far stated probabilities are from observed rates. When
  Jev says 0.8, about 80% of those items should pass. Lower is better.

Caveats on the planted cases:

- **The figure rewrites were audited only where checkers disagreed.** All three checkers agreed that
  11 of the 31 English "lost" rewrites still kept the image clearly, so I (Claude) re-read those 11:
  8 do keep the image, and 3 are genuine misses. Those labels are overridden in
  [`data/mutants/bsb.audit.json`](data/mutants/bsb.audit.json) and need a human second look.
  Because only items the checkers got "wrong" were re-read, the audit can only raise their scores:
  before it, Jev caught 92–95% of English figure-handling faults at 0.9; after it, 100%. The Hindi
  and Arabic rewrites have not been audited.
- **Planted cases carry one checking item per call**, while real verses carry up to 11.
- **Some planted cases arrive with no aligned words**: every omitted term, every verse swap, and
  the "lost" rewrites that delete the figure (1 of 31 English, 12 Hindi, 15 Arabic). Real items
  always have aligned words, so a model could use the gap as a hint. The "no renderings" condition
  removes aligned words from every case: key-term detection stayed at 98–99%, but lost-figure
  detection fell from 97% to 90% in Hindi and from 100% to 97% in Arabic, so the hint helped a
  little there.
- **Planted terms sometimes break grammar.** English omissions leave stray words ("an of Jesus
  Christ"); Arabic attaches "and", "to", and "the" to the word, and multi-word renderings are
  replaced whole. Broken grammar makes a fault easier to spot.

## Results

Numbers are for `jev-preview` (version 1.14.0) unless noted; `jev-latest` (1.13.0) is close
throughout. Full tables, threshold sweeps, calibration bins, and confusion matrices are in each
report: [BSB](runs/bsb/report.md), [Hindi IRV](runs/hi_irv/report.md),
[Arabic NAV](runs/ar_nav/report.md), [Masalit](runs/mdg_ssv/report.md).

Jev is close to deterministic but not exactly. In English and Hindi, sending identical requests
twice moved pass probabilities by about 0.01 on average (at most 0.10), and 1–12 of the 244 real
items crossed the 0.9 cut-off between runs. A figure question has only 31 real items, so one
crossing moves its rate by about 3 points. Treat differences under about 5 points as noise.

### Phase 0: English (BSB)

| Question | Real flagged | Faults caught | Verse swaps caught | AUROC |
|---|---|---|---|---|
| Key terms | 17% of 182 | 99% of 206 (wrong term 100%, omitted 98%) | 100% | 0.98 |
| Figure handling | 13% of 31 | 100% of 54 | 100% | 0.99 |
| Figure clarity | 52% of 31 | 100% of 55 | 100% | 0.99 |

Jev picked the exact handling label (kept / simile / plain / lost / distorted) for 90% of figure
rewrites.

The cut-off trades false alarms for misses. For key terms: at 0.8, 8% of real items flagged and
98% of planted errors caught; at 0.95, 25% and 99%. The clarity score ranks well (AUROC 0.99), but
0.9 is too strict for it: at 0.7 it flags 13% of real figures and still catches 100% of faults.

**Baseline comparison (same 453 cases):**

| Checker | Median time per real verse | Cost for 453 calls | Real key terms flagged | Real figures flagged (handling) | Key-term faults caught | Key-term AUROC |
|---|---|---|---|---|---|---|
| jev-preview | 260 ms | $0.019 | 17% | 13% | 99% | 0.984 |
| jev-latest | 279 ms | $0.019 | 19% | 16% | 98% | 0.975 |
| Claude Haiku 5.5 | 3,569 ms | $0.124 | 22% | 97% | 100% | 0.995 |

**What the state needs.** Two ablations, run on the same planted cases:

| Condition | BSB key terms: real flagged / faults caught | Hindi | Arabic |
|---|---|---|---|
| Full state | 17% / 99% | 31% / 99% | 31% / 99% |
| No approved terms (local tW headwords left out) | 15% / 99% | 36% / 99% | 30% / 99% |
| No renderings (aligned words left out) | 21% / 99% | 36% / 98% | 36% / 98% |

For Hindi and Arabic, removing the local headwords moved the flag rate by +5 and −1 points, so the
headword list does not explain their higher flag rate (see F2). For English the ablation tests
little: the English headword is also the term name, which stays in the state. Removing the
alignment raised false alarms by 4–5 points in each language and lowered figure-label accuracy
(English 90% → 83%, Hindi 86% → 79%, Arabic 85% → 74%), but key-term detection held: Jev reads the
verse, and the alignment mainly helps it locate the term.

### Phase 1: Hindi (IRV) and Arabic (NAV)

| Question | Hindi real flagged | Hindi faults caught | Arabic real flagged | Arabic faults caught |
|---|---|---|---|---|
| Key terms | 31% | 99% of 198 | 31% | 99% of 218 |
| Figure handling | 48% | 98% of 62 | 29% | 100% of 62 |
| Figure clarity | 81% | 100% of 62 | 71% | 100% of 62 |

Verse swaps were caught 100% in both. Exact handling label: 86% Hindi, 85% Arabic.

Claude Haiku 5.5 flagged about the same share of real key terms (33–35%), and removing the Hindi
and Arabic headwords barely moved Jev's rate. So the doubled flag rate against English is probably
more about these two translations (both are freer than the BSB) and the checking agenda than about
Jev reading Hindi or Arabic badly. That is an inference; human labels would settle it.

**Back-translation tier.** Jev flagged 97 Hindi items and 87 Arabic ones. After Gemma
back-translated each flagged verse, Jev re-checked and cleared 5 Hindi and 6 Arabic items. The
rest went to the human queue. One warning sign: for Hindi 2:15, the back-translation said
"rebuke", but the Hindi aligned to ἔλεγχε ("rebuke") is सिखाता रह, "keep teaching". The small model
filled in the word from the Bible it remembers. Jev kept the item flagged, which was right.

Examples from the human queues that look worth a checker's time:

- Hindi 2:15, ἔλεγχε ("rebuke") → सिखाता रह ("keep teaching"): the correction is softened.
- Arabic 2:12, τὴν ἀσέβειαν ("ungodliness") → الإباحية ("permissiveness, licentiousness"): the
  meaning is narrowed.

### Phase 2: Masalit (no model support)

The Masalit Titus draft (Door43 `Nhial/mdg_ssv_tit_book`, translated from the English ULT) is not
word-aligned, so the state has no renderings and no approved terms. We ran two conditions: Greek +
Masalit, and Greek + Masalit + the English ULT verse the translators worked from.

| Run | Key terms: mean pass probability, real verses | Same, swapped verses | AUROC real vs swap (key terms) |
|---|---|---|---|
| jev-latest | 0.51 | 0.42 | 0.72 |
| jev-latest + ULT | 0.57 | 0.48 | 0.73 |
| jev-preview | 0.57 | 0.50 | 0.68 |
| jev-preview + ULT | 0.62 | 0.54 | 0.70 |
| Claude Haiku 5.5 | 0.54 | 0.47 | 0.64 |

In every run, 99–100% of items went to review. Jev's probabilities collapse toward 50/50, which is
the right behavior when it cannot read the text: the routing design depends on the model admitting
doubt instead of guessing confidently. There is a faint signal (it may come from names such as
"Bulis" for Paul and "Taytus" for Titus), but nothing usable for checking.

We looked for human checking results to compare against. The repo's translationCore data has 133
verse edits, almost all tagged "spelling", and no checker selections. So there is no human gold
standard for Masalit Titus yet.

The repo labels the language `mdg`. The ISO 639-3 code for Masalit is `mls`; `mdg` is Massalat, a
different language in Chad. The manifest names the language "Masalit", so we treat it as Masalit.

## Findings

- **F1. Jev works as a fast first-pass screen for aligned translations in languages it reads.**
  Detection of planted errors is 98–100% across English, Hindi, and Arabic, at $0.00007–0.00008 and
  0.26 s per real verse.
- **F2. Many key-term false alarms come from the checking agenda, not the translation.** 25 of the
  BSB's 31 key-term flags recur in Hindi or Arabic (17 in all three). Examples: προσδεχόμενοι in
  2:13 is linked to the "receive, welcome" article, but every translation correctly says "await";
  παρακαλεῖν in 1:9 is linked to the "courage" article. Only 6 BSB key-term flags were unique to
  the BSB, against 17 for Hindi and 16 for Arabic. (All 16 BSB clarity flags also recur, but that
  is the strict cut-off in F5, not the agenda.)
- **F3. Jev's confident answers are trustworthy; its middling ones are not well calibrated.** When
  Jev puts an item at 0.8 or above, 97–100% of those items pass, and below 0.2 almost none do. In
  between, English key terms are over-optimistic (items Jev put at 0.6–0.8 passed 38% of the
  time). Calibration here is measured on a mix of real and planted items, so it depends on that
  mix. For routing, this means the high cut-off is safe and the middle band belongs with humans.
- **F4. A general LLM detects as well but is a poor router.** Haiku ranked good and bad items
  slightly better (key-term AUROC 0.98–1.00 against Jev's 0.96–0.98), but on real figures it spread
  its probability across several answers and flagged 84–97% of them.
- **F5. Figure clarity needs its own cut-off.** It ranks well but flags 52–81% of real figures at
  0.9. At 0.7 it flags 13% (English), 35% (Hindi), and 29% (Arabic), and still catches 97–100% of
  faults.
- **F6. Back-translation by a small model added little and carries a known risk.** It cleared 5–7%
  of flagged items, and in at least one case it imported the remembered Bible text instead of
  translating what was written.
- **F7. Zero-shot checking of an unsupported language does not work, and Jev says so.** On Masalit,
  answers sit near 50/50 and everything routes to humans.

## Limits of this test

- **The real-text baseline is assumed, not checked.** "Real flagged" counts items Jev doubted in
  published translations. Some of those may be real problems (see the Hindi and Arabic examples).
  True precision needs a human to label a sample of flagged and auto-passed items.
- **Planted errors are cleaner than real ones.** A swapped-in wrong word is easier to spot than a
  subtle shift in meaning. Detection rates on real errors will be lower.
- **Figure rewrites were written by an LLM.** We audited part of the English "lost" set; Hindi and
  Arabic are unaudited.
- **One book.** Titus is short (46 verses). The pipeline is book-agnostic in design, but source
  paths currently point at Titus.
- **The model alias moves.** `jev-latest` and `jev-preview` point at whatever TypeSafe releases.
  Each result records the exact version it came from (1.13.0 and 1.14.0 here).

## What next

1. **Human-label a sample in Hindi and Arabic.** About 100 flagged and 100 auto-passed items each,
   labeled by editors, would turn "real flagged" into a measured false-alarm rate. This is the
   single most useful next step, and it needs people, not code.
2. **Rank flags by how specific they are to one translation.** An item flagged across many
   translations is likely an agenda problem; send those to the Translation Words Links
   maintainers instead of the translation team.
3. **Test zero-resource checking on a language with known answers.** Cipher a known translation
   letter by letter (so word patterns still repeat) and run it like Masalit. A fellow developer
   reports 66–69% checker time savings on a fully ciphered language using Jev together with
   mDeBERTa; we have not reproduced that yet.
4. **Give Jev something to read for Masalit-type languages.** Options, from cheapest: statistical
   word alignment across the Masalit New Testament books already on Door43 (about 25 of them),
   which would supply renderings; a key-term glossary from the translation team; a human
   back-translation for Titus.
5. **Set the clarity cut-off separately** (around 0.7) and check it on more books.
6. **Run Russian.** RSOB (Russian Simplified Open Bible) and the Synodal are both aligned and
   configured (`--target ru_rsob`, `--target ru_rsb`) but not run, since Hindi and Arabic came first.

## Run it yourself

Requires [uv](https://docs.astral.sh/uv/). Keys are read from the environment or
`~/.config/ai-keys.env`: `TYPESAFE_API_KEY` for Jev, `OPENROUTER_API_KEY` for the baseline,
the small-model tier, and generating figure rewrites.

```bash
uv run jevqa run --target bsb --backend jev:jev-preview       # real verses + planted errors
uv run jevqa run --target bsb --backend openrouter:anthropic/claude-haiku-5.5
uv run jevqa run --target bsb --backend jev:jev-preview --no-renderings   # ablation
uv run jevqa run --target mdg_ssv --backend jev --with-ult    # Masalit, with the English source text
uv run jevqa route --target hi_irv --backend jev:jev-preview  # auto / explain + recheck / human queue
uv run jevqa report --target bsb                              # writes runs/bsb/report.md
uv run jevqa run --target bsb --backend dryrun                # write the requests without sending them
uv run pytest
```

Targets: `bsb`, `hi_irv`, `ar_nav`, `mdg_ssv`, `ru_rsob`, `ru_rsb`. Each condition flag
(`--no-approved`, `--no-renderings`, `--with-ult`, `--no-mutants`) writes to its own run directory,
and `route` takes the same flags. Responses are cached in `runs/cache/` (not committed), so
re-running costs nothing unless the request changes.

## Repo layout

| Path | What it holds |
|---|---|
| `src/jevqa/sources.py` | Door43 sources, pinned to commits in `data/sources.json` |
| `src/jevqa/usfm.py` | USFM parser: Greek words, aligned translation text, alignment groups |
| `src/jevqa/agenda.py` | Builds one case per verse from Translation Words Links and Translation Notes |
| `src/jevqa/questions.py` | Jev state and questions; turns answers into pass probabilities |
| `src/jevqa/backends.py` | Jev, OpenRouter baseline, dry run; response cache |
| `src/jevqa/mutate.py` | Planted errors: wrong and omitted terms, figure rewrites, verse swaps |
| `src/jevqa/run.py` | Run conditions, running a checker over a target, three-tier routing |
| `src/jevqa/evaluate.py`, `report.py` | Scoring and the per-target reports |
| `data/raw/` | Cached copies of the source texts (licenses below) |
| `data/mutants/` | Generated figure rewrites, fixed so every run uses the same test set |
| `runs/<target>/<run>/` | `results.jsonl` (every answer), `routing.json`, `human_queue.tsv` |

## Sources and licenses

| Source | Door43 repo | License |
|---|---|---|
| unfoldingWord Greek New Testament (v0.34) | `unfoldingWord/el-x-koine_ugnt` | CC BY-SA 4.0 |
| Translation Notes, Translation Words, Translation Words Links | `unfoldingWord/en_tn`, `en_tw`, `en_twl` | CC BY-SA 4.0 |
| Berean Standard Bible, aligned | `Worldview/en_bsb` | Text public domain; alignment CC BY-SA 4.0 |
| Indian Revised Version (Hindi), aligned; Hindi tW | `Door43-Catalog/hi_irv`, `hi_tw` | CC BY-SA 4.0 |
| New Arabic Version (Ketab El Hayat), aligned; Arabic tW | `BSOJ/ar_nav`, `BSOJ/ar_tw` | CC BY-SA 4.0 (Biblica open license) |
| Masalit Titus draft | `Nhial/mdg_ssv_tit_book` | CC BY-SA 4.0 |
| unfoldingWord Literal Text (ULT) | `unfoldingWord/en_ult` | CC BY-SA 4.0 |
| Russian Simplified Open Bible; Russian Synodal; Russian tW | `ru_gl/ru_rsob`, `Door43-Catalog/ru_rsb`, `ru_gl/ru_tw` | CC BY-SA 4.0 |

Exact commits are in [`data/sources.json`](data/sources.json).

## Glossary

- **Jev**: TypeSafe AI's "System One" model. It answers typed questions with probabilities and does
  not generate text. API: `POST https://api.typesafe.ai/v1/systemone`.
- **noul**: Jev's name for a yes/no question; the answer is the probability of "yes".
- **UGNT**: unfoldingWord Greek New Testament, the Greek text everything here is anchored to.
- **tN / Translation Notes**: verse notes keyed to Greek phrases; we use the figure-of-speech notes.
- **tW / Translation Words**: articles on key biblical terms. **TWL / Translation Words Links**
  ties each Greek word in a verse to its tW article.
- **Alignment**: a word-by-word link between the Greek and the translation, made in translationCore.
- **Gateway / Strategic Language**: a widely used language that other translations are made from.
