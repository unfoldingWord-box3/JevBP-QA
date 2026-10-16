# NAV (New Arabic Version, Ketab El Hayat): Titus checked against the Greek

Target `ar_nav` (Arabic). Headline threshold: an item is auto-logged as a pass when its pass probability is at least 0.9; anything lower goes to review.

Sources (pinned commits):

- `ugnt`: unfoldingWord/el-x-koine_ugnt @ `fc95b2b8aa` (CC BY-SA 4.0)
- `en_tn`: unfoldingWord/en_tn @ `a0959d790f` (CC BY-SA 4.0)
- `en_twl`: unfoldingWord/en_twl @ `d880052cb7` (CC BY-SA 4.0)
- `en_tw`: unfoldingWord/en_tw @ `6e3900f8c2` (CC BY-SA 4.0)
- `ar_nav`: BSOJ/ar_nav @ `62e82b95ee` (CC BY-SA 4.0 (Biblica open license; repo LICENSE.md is uW boilerplate))
- `ar_tw`: BSOJ/ar_tw @ `672197ba44` (CC BY-SA 4.0)

## Speed and cost

| run | model version | calls | median latency | total cost |
|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 465 | 267 ms | $0.0219 |
| jev-jev-preview | jev-1.14.0 | 465 | 257 ms | $0.0219 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 465 | 2553 ms | $0.1464 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 36% | 218 | 99% | 100% | 0.963 | 0.054 |
| jev-jev-preview | 182 | 32% | 218 | 99% | 100% | 0.973 | 0.057 |
| openrouter-claude-haiku-5.5 | 182 | 33% | 218 | 100% | 99% | 0.996 | 0.081 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 97% / 0.29 | 100% / 0.08 | 36% / 0.83 | 100% / 0.10 |
| jev-jev-preview | 98% / 0.26 | 100% / 0.08 | 32% / 0.85 | 100% / 0.07 |
| openrouter-claude-haiku-5.5 | 100% / 0.09 | 100% / 0.05 | 33% / 0.83 | 99% / 0.06 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 26% | 62 | 98% | 100% | 0.985 | 0.070 |
| jev-jev-preview | 31 | 29% | 62 | 98% | 100% | 0.987 | 0.067 |
| openrouter-claude-haiku-5.5 | 31 | 87% | 62 | 100% | 100% | 0.988 | 0.113 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.08 | 13% / 0.94 | 97% / 0.43 | 10% / 0.97 | 3% / 0.97 | 26% / 0.91 | 100% / 0.01 |
| jev-jev-preview | 100% / 0.08 | 23% / 0.92 | 97% / 0.38 | 13% / 0.95 | 13% / 0.95 | 29% / 0.88 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.11 | 55% / 0.86 | 100% / 0.38 | 52% / 0.88 | 16% / 0.92 | 87% / 0.80 | 100% / 0.06 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 87%, jev-jev-preview 86%, openrouter-claude-haiku-5.5 92%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 58% | 62 | 100% | 100% | 0.956 | 0.086 |
| jev-jev-preview | 31 | 71% | 62 | 100% | 100% | 0.967 | 0.108 |
| openrouter-claude-haiku-5.5 | 31 | 84% | 62 | 100% | 100% | 0.987 | 0.132 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.07 | 58% / 0.84 | 100% / 0.35 | 35% / 0.91 | 81% / 0.68 | 58% / 0.78 | 100% / 0.01 |
| jev-jev-preview | 100% / 0.08 | 65% / 0.81 | 100% / 0.33 | 45% / 0.89 | 90% / 0.69 | 71% / 0.75 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.10 | 58% / 0.85 | 100% / 0.41 | 35% / 0.91 | 87% / 0.85 | 84% / 0.82 | 100% / 0.08 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=316, said 0.07, was 0.02; 0.2–0.4: n=73, said 0.28, was 0.14; 0.4–0.6: n=28, said 0.47, was 0.54; 0.6–0.8: n=18, said 0.69, was 0.61; 0.8–1.0: n=147, said 0.94, was 0.95

Calibration, figure handling (choice): 0.0–0.2: n=70, said 0.04, was 0.00; 0.2–0.4: n=6, said 0.32, was 0.00; 0.4–0.6: n=7, said 0.49, was 0.29; 0.6–0.8: n=11, said 0.70, was 0.55; 0.8–1.0: n=123, said 0.96, was 0.94

Calibration, figure clarity (score): 0.0–0.2: n=70, said 0.04, was 0.00; 0.2–0.4: n=14, said 0.29, was 0.43; 0.4–0.6: n=21, said 0.49, was 0.62; 0.6–0.8: n=33, said 0.70, was 0.79; 0.8–1.0: n=79, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 14% / 94% | 20% / 97% | 23% / 97% | 36% / 99% | 49% / 100% |
| Figure handling (choice) | 3% / 76% | 6% / 85% | 16% / 89% | 26% / 98% | 39% / 100% |
| Figure clarity (score) | 13% / 87% | 26% / 95% | 42% / 100% | 58% / 100% | 84% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 28 | 0 | 3 | 0 | 0 |
| simile | 3 | 28 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 6 | 18 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 91. Lowest ten: 2:12 kt_trje (0.07); 2:13 kt_eqaj (0.11); 1:9 kt_nngz (0.12); 1:11 kt_bjyb (0.15); 1:9 kt_ss39 (0.15); 2:12 kt_e5gn (0.19); 1:10 fig_pu74_clarity (0.20); 3:2 kt_kjtc (0.23); 3:13 kt_v462 (0.24); 3:2 kt_xrq8 (0.29)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=328, said 0.06, was 0.02; 0.2–0.4: n=59, said 0.27, was 0.12; 0.4–0.6: n=23, said 0.48, was 0.48; 0.6–0.8: n=22, said 0.69, was 0.64; 0.8–1.0: n=150, said 0.95, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=68, said 0.03, was 0.00; 0.2–0.4: n=8, said 0.26, was 0.00; 0.4–0.6: n=13, said 0.49, was 0.38; 0.6–0.8: n=13, said 0.72, was 0.46; 0.8–1.0: n=115, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=66, said 0.03, was 0.00; 0.2–0.4: n=19, said 0.28, was 0.21; 0.4–0.6: n=25, said 0.50, was 0.72; 0.6–0.8: n=32, said 0.71, was 0.84; 0.8–1.0: n=75, said 0.91, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 9% / 95% | 16% / 97% | 20% / 98% | 32% / 99% | 43% / 100% |
| Figure handling (choice) | 3% / 82% | 10% / 90% | 23% / 97% | 29% / 98% | 55% / 100% |
| Figure clarity (score) | 16% / 85% | 29% / 97% | 48% / 100% | 71% / 100% | 84% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 25 | 0 | 5 | 1 | 0 |
| simile | 4 | 27 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 6 | 0 | 5 | 20 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 89. Lowest ten: 2:12 kt_trje (0.07); 2:13 kt_eqaj (0.10); 3:13 kt_v462 (0.12); 1:11 kt_bjyb (0.17); 1:9 kt_nngz (0.17); 2:12 kt_e5gn (0.24); 1:9 kt_ss39 (0.25); 1:10 fig_pu74_clarity (0.27); 3:2 kt_kjtc (0.28); 2:10 kt_bn72 (0.31)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=374, said 0.04, was 0.01; 0.2–0.4: n=28, said 0.27, was 0.43; 0.4–0.6: n=17, said 0.47, was 0.65; 0.6–0.8: n=18, said 0.69, was 0.83; 0.8–1.0: n=145, said 0.93, was 0.98

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.08, was 0.00; 0.2–0.4: n=12, said 0.34, was 0.00; 0.4–0.6: n=5, said 0.47, was 0.40; 0.6–0.8: n=30, said 0.72, was 0.70; 0.8–1.0: n=101, said 0.90, was 1.00

Calibration, figure clarity (score): 0.0–0.2: n=60, said 0.08, was 0.00; 0.2–0.4: n=21, said 0.27, was 0.00; 0.4–0.6: n=9, said 0.50, was 0.67; 0.6–0.8: n=16, said 0.73, was 0.50; 0.8–1.0: n=111, said 0.89, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 10% / 100% | 17% / 100% | 22% / 100% | 33% / 100% | 59% / 100% |
| Figure handling (choice) | 0% / 85% | 13% / 90% | 42% / 100% | 87% / 100% | 97% / 100% |
| Figure clarity (score) | 3% / 82% | 6% / 87% | 26% / 98% | 84% / 100% | 100% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 2 | 0 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 2 | 22 | 0 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 113. Lowest ten: 2:12 kt_trje (0.15); 2:13 kt_eqaj (0.15); 3:2 kt_xrq8 (0.20); 3:5 kt_f8tn (0.20); 1:11 kt_bjyb (0.25); 1:9 kt_ss39 (0.25); 1:9 kt_x67x (0.25); 1:3 kt_bgv4 (0.30); 2:3 kt_qkdt (0.30); 3:13 kt_v462 (0.30)

