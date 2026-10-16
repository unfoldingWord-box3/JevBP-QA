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

Cost and latency are those of the call that produced each answer (re-runs are served from cache). Unanswered = questions with no answer (API error or partial reply); they are left out of every score below.

| run | model version | calls | median latency | total cost | unanswered |
|---|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 465 | 263 ms | $0.0218 | 0 |
| jev-jev-preview | jev-1.14.0 | 465 | 258 ms | $0.0218 | 0 |
| jev-jev-preview+no-approved | jev-1.14.0 | 465 | 262 ms | $0.0210 | 0 |
| jev-jev-preview+no-renderings | jev-1.14.0 | 465 | 257 ms | $0.0213 | 0 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 465 | 2539 ms | $0.1470 | 0 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 32% | 218 | 98% | 100% | 0.965 | 0.052 |
| jev-jev-preview | 182 | 31% | 218 | 99% | 100% | 0.972 | 0.058 |
| jev-jev-preview+no-approved | 182 | 30% | 218 | 99% | 100% | 0.975 | 0.089 |
| jev-jev-preview+no-renderings | 182 | 36% | 218 | 98% | 100% | 0.957 | 0.096 |
| openrouter-claude-haiku-5.5 | 182 | 35% | 218 | 100% | 100% | 0.996 | 0.082 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 96% / 0.29 | 100% / 0.08 | 32% / 0.83 | 100% / 0.07 |
| jev-jev-preview | 97% / 0.26 | 100% / 0.08 | 31% / 0.86 | 100% / 0.04 |
| jev-jev-preview+no-approved | 97% / 0.34 | 100% / 0.12 | 30% / 0.87 | 100% / 0.06 |
| jev-jev-preview+no-renderings | 97% / 0.26 | 99% / 0.29 | 36% / 0.85 | 100% / 0.04 |
| openrouter-claude-haiku-5.5 | 100% / 0.10 | 100% / 0.05 | 35% / 0.83 | 100% / 0.03 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 26% | 62 | 97% | 100% | 0.984 | 0.067 |
| jev-jev-preview | 31 | 29% | 62 | 100% | 100% | 0.988 | 0.067 |
| jev-jev-preview+no-approved | 31 | 32% | 62 | 100% | 100% | 0.986 | 0.067 |
| jev-jev-preview+no-renderings | 31 | 42% | 62 | 97% | 100% | 0.968 | 0.089 |
| openrouter-claude-haiku-5.5 | 31 | 84% | 62 | 98% | 100% | 0.972 | 0.107 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.08 | 10% / 0.94 | 94% / 0.46 | 3% / 0.97 | 3% / 0.97 | 26% / 0.91 | 100% / 0.02 |
| jev-jev-preview | 100% / 0.07 | 26% / 0.92 | 100% / 0.40 | 13% / 0.95 | 16% / 0.94 | 29% / 0.89 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.07 | 26% / 0.92 | 100% / 0.40 | 13% / 0.95 | 16% / 0.94 | 32% / 0.88 | 100% / 0.02 |
| jev-jev-preview+no-renderings | 97% / 0.18 | 26% / 0.90 | 97% / 0.48 | 26% / 0.91 | 19% / 0.93 | 42% / 0.87 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.10 | 58% / 0.88 | 97% / 0.41 | 55% / 0.87 | 16% / 0.92 | 84% / 0.81 | 100% / 0.06 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 87%, jev-jev-preview 85%, jev-jev-preview+no-approved 85%, jev-jev-preview+no-renderings 74%, openrouter-claude-haiku-5.5 90%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 61% | 62 | 100% | 100% | 0.953 | 0.103 |
| jev-jev-preview | 31 | 71% | 62 | 100% | 100% | 0.962 | 0.092 |
| jev-jev-preview+no-approved | 31 | 74% | 62 | 100% | 100% | 0.961 | 0.099 |
| jev-jev-preview+no-renderings | 31 | 87% | 62 | 100% | 100% | 0.933 | 0.106 |
| openrouter-claude-haiku-5.5 | 31 | 77% | 62 | 100% | 100% | 0.979 | 0.108 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.07 | 58% / 0.83 | 100% / 0.38 | 35% / 0.91 | 87% / 0.68 | 61% / 0.78 | 100% / 0.02 |
| jev-jev-preview | 100% / 0.08 | 55% / 0.82 | 100% / 0.35 | 39% / 0.89 | 94% / 0.68 | 71% / 0.75 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.08 | 55% / 0.82 | 100% / 0.35 | 39% / 0.89 | 94% / 0.68 | 74% / 0.75 | 100% / 0.02 |
| jev-jev-preview+no-renderings | 100% / 0.18 | 81% / 0.77 | 100% / 0.38 | 55% / 0.84 | 94% / 0.69 | 87% / 0.72 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.09 | 58% / 0.88 | 100% / 0.48 | 32% / 0.91 | 61% / 0.87 | 77% / 0.83 | 100% / 0.10 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=321, said 0.08, was 0.02; 0.2–0.4: n=60, said 0.28, was 0.15; 0.4–0.6: n=29, said 0.48, was 0.55; 0.6–0.8: n=12, said 0.67, was 0.67; 0.8–1.0: n=149, said 0.94, was 0.96

Calibration, figure handling (choice): 0.0–0.2: n=65, said 0.03, was 0.00; 0.2–0.4: n=9, said 0.27, was 0.00; 0.4–0.6: n=10, said 0.50, was 0.30; 0.6–0.8: n=11, said 0.73, was 0.36; 0.8–1.0: n=122, said 0.96, was 0.96

Calibration, figure clarity (score): 0.0–0.2: n=69, said 0.04, was 0.00; 0.2–0.4: n=13, said 0.27, was 0.54; 0.4–0.6: n=22, said 0.49, was 0.50; 0.6–0.8: n=36, said 0.71, was 0.83; 0.8–1.0: n=77, said 0.92, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 14% / 94% | 19% / 97% | 21% / 97% | 32% / 98% | 45% / 100% |
| Figure handling (choice) | 3% / 77% | 3% / 84% | 13% / 92% | 26% / 97% | 39% / 100% |
| Figure clarity (score) | 10% / 84% | 26% / 94% | 45% / 98% | 61% / 100% | 74% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 28 | 0 | 3 | 0 | 0 |
| simile | 2 | 29 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 7 | 17 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 85. Lowest ten: 2:12 kt_trje (0.08); 2:13 kt_eqaj (0.11); 1:9 kt_ss39 (0.15); 1:9 kt_nngz (0.16); 1:11 kt_bjyb (0.18); 2:12 kt_e5gn (0.19); 1:10 fig_pu74_clarity (0.20); 3:13 kt_v462 (0.24); 3:2 kt_kjtc (0.28); 1:6 kt_nsxd (0.29)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=332, said 0.06, was 0.01; 0.2–0.4: n=51, said 0.28, was 0.14; 0.4–0.6: n=23, said 0.50, was 0.57; 0.6–0.8: n=17, said 0.72, was 0.82; 0.8–1.0: n=148, said 0.95, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.03, was 0.00; 0.2–0.4: n=4, said 0.24, was 0.00; 0.4–0.6: n=16, said 0.50, was 0.31; 0.6–0.8: n=14, said 0.72, was 0.50; 0.8–1.0: n=114, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=65, said 0.03, was 0.00; 0.2–0.4: n=18, said 0.28, was 0.28; 0.4–0.6: n=28, said 0.50, was 0.64; 0.6–0.8: n=29, said 0.70, was 0.86; 0.8–1.0: n=77, said 0.90, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 9% / 95% | 16% / 97% | 21% / 98% | 31% / 99% | 38% / 99% |
| Figure handling (choice) | 3% / 81% | 10% / 92% | 19% / 97% | 29% / 100% | 55% / 100% |
| Figure clarity (score) | 16% / 85% | 29% / 97% | 45% / 98% | 71% / 100% | 84% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 26 | 0 | 5 | 0 | 0 |
| simile | 4 | 27 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 7 | 17 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 87. Lowest ten: 2:12 kt_trje (0.06); 2:13 kt_eqaj (0.08); 3:13 kt_v462 (0.11); 1:11 kt_bjyb (0.17); 1:9 kt_nngz (0.20); 1:9 kt_ss39 (0.22); 2:12 kt_e5gn (0.23); 1:10 fig_pu74_clarity (0.26); 3:2 kt_kjtc (0.29); 1:11 kt_n4aq (0.31)


## Detail: jev-jev-preview+no-approved

Calibration, key terms (noul): 0.0–0.2: n=290, said 0.07, was 0.00; 0.2–0.4: n=67, said 0.28, was 0.13; 0.4–0.6: n=33, said 0.49, was 0.18; 0.6–0.8: n=27, said 0.71, was 0.67; 0.8–1.0: n=154, said 0.94, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.03, was 0.00; 0.2–0.4: n=4, said 0.24, was 0.00; 0.4–0.6: n=16, said 0.49, was 0.31; 0.6–0.8: n=13, said 0.71, was 0.46; 0.8–1.0: n=115, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=65, said 0.03, was 0.00; 0.2–0.4: n=18, said 0.28, was 0.28; 0.4–0.6: n=28, said 0.49, was 0.64; 0.6–0.8: n=29, said 0.71, was 0.86; 0.8–1.0: n=77, said 0.90, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 7% / 89% | 11% / 95% | 18% / 98% | 30% / 99% | 49% / 100% |
| Figure handling (choice) | 6% / 81% | 13% / 92% | 16% / 97% | 32% / 100% | 61% / 100% |
| Figure clarity (score) | 19% / 85% | 29% / 97% | 45% / 98% | 74% / 100% | 84% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 26 | 0 | 5 | 0 | 0 |
| simile | 4 | 27 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 7 | 17 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 87. Lowest ten: 1:9 kt_nngz (0.21); 2:13 kt_eqaj (0.21); 2:12 kt_trje (0.28); 1:9 kt_ss39 (0.29); 1:10 fig_pu74_clarity (0.30); 1:10 fig_w9kk_clarity (0.30); 3:13 kt_v462 (0.32); 1:11 kt_n4aq (0.33); 1:10 kt_k8ta (0.34); 2:14 kt_xhp7 (0.35)


## Detail: jev-jev-preview+no-renderings

Calibration, key terms (noul): 0.0–0.2: n=264, said 0.07, was 0.02; 0.2–0.4: n=95, said 0.29, was 0.03; 0.4–0.6: n=40, said 0.49, was 0.40; 0.6–0.8: n=24, said 0.71, was 0.75; 0.8–1.0: n=148, said 0.94, was 0.95

Calibration, figure handling (choice): 0.0–0.2: n=59, said 0.04, was 0.00; 0.2–0.4: n=10, said 0.27, was 0.10; 0.4–0.6: n=13, said 0.51, was 0.08; 0.6–0.8: n=20, said 0.71, was 0.70; 0.8–1.0: n=115, said 0.93, was 0.94

Calibration, figure clarity (score): 0.0–0.2: n=62, said 0.05, was 0.03; 0.2–0.4: n=18, said 0.31, was 0.17; 0.4–0.6: n=29, said 0.50, was 0.62; 0.6–0.8: n=42, said 0.70, was 0.90; 0.8–1.0: n=66, said 0.89, was 0.95

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 7% / 89% | 15% / 95% | 23% / 97% | 36% / 98% | 52% / 99% |
| Figure handling (choice) | 3% / 66% | 10% / 85% | 19% / 89% | 42% / 97% | 71% / 100% |
| Figure clarity (score) | 10% / 81% | 39% / 94% | 65% / 95% | 87% / 100% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 25 | 0 | 5 | 1 | 0 |
| simile | 7 | 22 | 2 | 0 | 0 |
| plain | 3 | 0 | 28 | 0 | 0 |
| lost | 9 | 0 | 8 | 14 | 0 |
| distorted | 4 | 0 | 0 | 1 | 26 |

Real items flagged at 0.9: 105. Lowest ten: 1:9 kt_nngz (0.12); 2:13 kt_eqaj (0.12); 1:10 fig_pu74_clarity (0.15); 2:12 kt_e5gn (0.18); 2:12 kt_trje (0.18); 1:9 kt_ss39 (0.24); 1:11 kt_bjyb (0.27); 3:2 kt_xrq8 (0.32); 1:10 fig_pu74_handling (0.35); 1:15 kt_mn4k (0.40)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=369, said 0.04, was 0.00; 0.2–0.4: n=31, said 0.27, was 0.39; 0.4–0.6: n=11, said 0.46, was 0.82; 0.6–0.8: n=17, said 0.68, was 1.00; 0.8–1.0: n=143, said 0.93, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.08, was 0.00; 0.2–0.4: n=11, said 0.31, was 0.00; 0.4–0.6: n=5, said 0.47, was 0.20; 0.6–0.8: n=22, said 0.71, was 0.73; 0.8–1.0: n=110, said 0.90, was 0.97

Calibration, figure clarity (score): 0.0–0.2: n=56, said 0.08, was 0.00; 0.2–0.4: n=22, said 0.26, was 0.00; 0.4–0.6: n=2, said 0.48, was 0.50; 0.6–0.8: n=22, said 0.70, was 0.55; 0.8–1.0: n=115, said 0.89, was 0.97

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 11% / 100% | 16% / 100% | 21% / 100% | 35% / 100% | 55% / 100% |
| Figure handling (choice) | 3% / 82% | 16% / 87% | 35% / 95% | 84% / 98% | 100% / 100% |
| Figure clarity (score) | 3% / 76% | 6% / 85% | 23% / 94% | 77% / 100% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 2 | 0 | 0 |
| simile | 3 | 28 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 8 | 0 | 3 | 20 | 0 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 113. Lowest ten: 2:12 kt_trje (0.10); 1:9 kt_ss39 (0.20); 2:13 kt_eqaj (0.20); 3:5 kt_f8tn (0.20); 3:2 kt_xrq8 (0.25); 1:3 kt_bgv4 (0.30); 1:6 kt_nsxd (0.30); 3:8 kt_dxb8 (0.30); 1:11 kt_bjyb (0.35); 1:7 kt_g6v8 (0.35)

