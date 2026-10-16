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
| jev-jev-latest | jev-1.13.0 | 465 | 266 ms | $0.0219 | 0 |
| jev-jev-preview | jev-1.14.0 | 465 | 258 ms | $0.0219 | 0 |
| jev-jev-preview+no-approved | jev-1.14.0 | 465 | 259 ms | $0.0210 | 0 |
| jev-jev-preview+no-renderings | jev-1.14.0 | 465 | 254 ms | $0.0214 | 0 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 465 | 2555 ms | $0.1471 | 0 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 34% | 218 | 99% | 100% | 0.964 | 0.050 |
| jev-jev-preview | 182 | 32% | 218 | 99% | 100% | 0.971 | 0.060 |
| jev-jev-preview+no-approved | 182 | 30% | 218 | 99% | 100% | 0.975 | 0.089 |
| jev-jev-preview+no-renderings | 182 | 40% | 218 | 99% | 100% | 0.955 | 0.103 |
| openrouter-claude-haiku-5.5 | 182 | 34% | 218 | 100% | 100% | 0.996 | 0.084 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 97% / 0.28 | 100% / 0.08 | 34% / 0.83 | 100% / 0.07 |
| jev-jev-preview | 98% / 0.25 | 100% / 0.08 | 32% / 0.85 | 100% / 0.04 |
| jev-jev-preview+no-approved | 97% / 0.34 | 100% / 0.12 | 30% / 0.87 | 100% / 0.06 |
| jev-jev-preview+no-renderings | 98% / 0.25 | 99% / 0.30 | 40% / 0.84 | 100% / 0.04 |
| openrouter-claude-haiku-5.5 | 100% / 0.10 | 100% / 0.05 | 34% / 0.83 | 100% / 0.03 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 26% | 62 | 97% | 100% | 0.984 | 0.067 |
| jev-jev-preview | 31 | 29% | 62 | 100% | 100% | 0.986 | 0.067 |
| jev-jev-preview+no-approved | 31 | 32% | 62 | 100% | 100% | 0.986 | 0.067 |
| jev-jev-preview+no-renderings | 31 | 48% | 62 | 97% | 100% | 0.968 | 0.086 |
| openrouter-claude-haiku-5.5 | 31 | 84% | 62 | 98% | 100% | 0.975 | 0.109 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.08 | 10% / 0.94 | 94% / 0.46 | 3% / 0.97 | 3% / 0.97 | 26% / 0.91 | 100% / 0.02 |
| jev-jev-preview | 100% / 0.07 | 26% / 0.92 | 100% / 0.40 | 13% / 0.95 | 16% / 0.94 | 29% / 0.88 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.07 | 26% / 0.92 | 100% / 0.40 | 13% / 0.95 | 16% / 0.94 | 32% / 0.88 | 100% / 0.02 |
| jev-jev-preview+no-renderings | 97% / 0.18 | 26% / 0.90 | 97% / 0.48 | 26% / 0.91 | 19% / 0.93 | 48% / 0.87 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.10 | 58% / 0.88 | 97% / 0.41 | 55% / 0.87 | 16% / 0.92 | 84% / 0.82 | 100% / 0.05 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 87%, jev-jev-preview 85%, jev-jev-preview+no-approved 85%, jev-jev-preview+no-renderings 74%, openrouter-claude-haiku-5.5 90%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 61% | 62 | 100% | 100% | 0.952 | 0.102 |
| jev-jev-preview | 31 | 71% | 62 | 100% | 100% | 0.961 | 0.100 |
| jev-jev-preview+no-approved | 31 | 74% | 62 | 100% | 100% | 0.961 | 0.099 |
| jev-jev-preview+no-renderings | 31 | 84% | 62 | 100% | 100% | 0.932 | 0.107 |
| openrouter-claude-haiku-5.5 | 31 | 84% | 62 | 100% | 100% | 0.978 | 0.103 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.07 | 58% / 0.83 | 100% / 0.38 | 35% / 0.91 | 87% / 0.68 | 61% / 0.78 | 100% / 0.02 |
| jev-jev-preview | 100% / 0.08 | 55% / 0.82 | 100% / 0.35 | 39% / 0.89 | 94% / 0.68 | 71% / 0.75 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.08 | 55% / 0.82 | 100% / 0.35 | 39% / 0.89 | 94% / 0.68 | 74% / 0.75 | 100% / 0.02 |
| jev-jev-preview+no-renderings | 100% / 0.18 | 81% / 0.77 | 100% / 0.38 | 55% / 0.84 | 94% / 0.69 | 84% / 0.71 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.09 | 58% / 0.88 | 100% / 0.48 | 32% / 0.91 | 61% / 0.87 | 84% / 0.83 | 100% / 0.08 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=315, said 0.07, was 0.02; 0.2–0.4: n=68, said 0.28, was 0.16; 0.4–0.6: n=28, said 0.48, was 0.46; 0.6–0.8: n=13, said 0.67, was 0.85; 0.8–1.0: n=147, said 0.94, was 0.96

Calibration, figure handling (choice): 0.0–0.2: n=66, said 0.03, was 0.00; 0.2–0.4: n=8, said 0.28, was 0.00; 0.4–0.6: n=10, said 0.50, was 0.30; 0.6–0.8: n=12, said 0.73, was 0.42; 0.8–1.0: n=121, said 0.96, was 0.96

Calibration, figure clarity (score): 0.0–0.2: n=69, said 0.04, was 0.00; 0.2–0.4: n=14, said 0.28, was 0.57; 0.4–0.6: n=21, said 0.49, was 0.48; 0.6–0.8: n=36, said 0.71, was 0.83; 0.8–1.0: n=77, said 0.92, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 13% / 94% | 20% / 97% | 23% / 97% | 34% / 99% | 47% / 100% |
| Figure handling (choice) | 3% / 77% | 10% / 84% | 16% / 92% | 26% / 97% | 39% / 100% |
| Figure clarity (score) | 13% / 84% | 26% / 94% | 45% / 98% | 61% / 100% | 77% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 28 | 0 | 3 | 0 | 0 |
| simile | 2 | 29 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 7 | 17 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 89. Lowest ten: 2:12 kt_trje (0.08); 2:13 kt_eqaj (0.11); 1:9 kt_nngz (0.14); 1:9 kt_ss39 (0.14); 1:11 kt_bjyb (0.18); 2:12 kt_e5gn (0.19); 3:13 kt_v462 (0.23); 1:10 fig_pu74_clarity (0.24); 3:2 kt_kjtc (0.28); 1:15 kt_mn4k (0.29)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=327, said 0.06, was 0.02; 0.2–0.4: n=57, said 0.28, was 0.11; 0.4–0.6: n=22, said 0.50, was 0.55; 0.6–0.8: n=18, said 0.71, was 0.83; 0.8–1.0: n=147, said 0.95, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.03, was 0.00; 0.2–0.4: n=4, said 0.24, was 0.00; 0.4–0.6: n=15, said 0.49, was 0.27; 0.6–0.8: n=14, said 0.70, was 0.50; 0.8–1.0: n=115, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=65, said 0.03, was 0.00; 0.2–0.4: n=18, said 0.28, was 0.28; 0.4–0.6: n=28, said 0.50, was 0.64; 0.6–0.8: n=30, said 0.70, was 0.87; 0.8–1.0: n=76, said 0.91, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 9% / 95% | 17% / 98% | 21% / 98% | 32% / 99% | 42% / 100% |
| Figure handling (choice) | 6% / 81% | 13% / 92% | 16% / 97% | 29% / 100% | 55% / 100% |
| Figure clarity (score) | 16% / 85% | 32% / 97% | 48% / 98% | 71% / 100% | 84% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 26 | 0 | 5 | 0 | 0 |
| simile | 4 | 27 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 7 | 0 | 7 | 17 | 0 |
| distorted | 1 | 0 | 0 | 0 | 30 |

Real items flagged at 0.9: 89. Lowest ten: 2:12 kt_trje (0.06); 2:13 kt_eqaj (0.08); 3:13 kt_v462 (0.13); 1:9 kt_nngz (0.15); 1:11 kt_bjyb (0.17); 1:9 kt_ss39 (0.19); 2:12 kt_e5gn (0.23); 2:10 kt_bn72 (0.27); 3:2 kt_kjtc (0.29); 1:10 fig_pu74_clarity (0.29)


## Detail: jev-jev-preview+no-approved

Calibration, key terms (noul): 0.0–0.2: n=293, said 0.07, was 0.00; 0.2–0.4: n=62, said 0.28, was 0.15; 0.4–0.6: n=35, said 0.49, was 0.17; 0.6–0.8: n=27, said 0.71, was 0.67; 0.8–1.0: n=154, said 0.94, was 0.97

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

Calibration, key terms (noul): 0.0–0.2: n=254, said 0.07, was 0.02; 0.2–0.4: n=99, said 0.28, was 0.03; 0.4–0.6: n=45, said 0.48, was 0.36; 0.6–0.8: n=27, said 0.70, was 0.74; 0.8–1.0: n=146, said 0.93, was 0.95

Calibration, figure handling (choice): 0.0–0.2: n=59, said 0.04, was 0.00; 0.2–0.4: n=10, said 0.28, was 0.10; 0.4–0.6: n=13, said 0.51, was 0.08; 0.6–0.8: n=20, said 0.71, was 0.70; 0.8–1.0: n=115, said 0.93, was 0.94

Calibration, figure clarity (score): 0.0–0.2: n=62, said 0.05, was 0.03; 0.2–0.4: n=18, said 0.31, was 0.17; 0.4–0.6: n=29, said 0.50, was 0.62; 0.6–0.8: n=41, said 0.70, was 0.90; 0.8–1.0: n=67, said 0.89, was 0.96

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 8% / 90% | 17% / 96% | 24% / 97% | 40% / 99% | 54% / 99% |
| Figure handling (choice) | 3% / 66% | 10% / 85% | 19% / 89% | 48% / 97% | 71% / 100% |
| Figure clarity (score) | 10% / 81% | 48% / 94% | 61% / 95% | 84% / 100% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 25 | 0 | 5 | 1 | 0 |
| simile | 7 | 22 | 2 | 0 | 0 |
| plain | 3 | 0 | 28 | 0 | 0 |
| lost | 9 | 0 | 8 | 14 | 0 |
| distorted | 4 | 0 | 0 | 1 | 26 |

Real items flagged at 0.9: 114. Lowest ten: 1:9 kt_nngz (0.08); 2:13 kt_eqaj (0.12); 1:10 fig_pu74_clarity (0.18); 2:12 kt_e5gn (0.18); 2:12 kt_trje (0.18); 1:9 kt_ss39 (0.23); 1:11 kt_bjyb (0.27); 3:2 kt_xrq8 (0.32); 1:10 fig_pu74_handling (0.40); 1:9 kt_x67x (0.40)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=366, said 0.04, was 0.00; 0.2–0.4: n=34, said 0.26, was 0.38; 0.4–0.6: n=9, said 0.46, was 0.67; 0.6–0.8: n=19, said 0.67, was 1.00; 0.8–1.0: n=143, said 0.93, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.08, was 0.00; 0.2–0.4: n=11, said 0.31, was 0.00; 0.4–0.6: n=6, said 0.51, was 0.33; 0.6–0.8: n=18, said 0.72, was 0.67; 0.8–1.0: n=113, said 0.89, was 0.97

Calibration, figure clarity (score): 0.0–0.2: n=58, said 0.07, was 0.00; 0.2–0.4: n=20, said 0.26, was 0.00; 0.4–0.6: n=2, said 0.55, was 0.50; 0.6–0.8: n=22, said 0.70, was 0.55; 0.8–1.0: n=115, said 0.89, was 0.97

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 10% / 100% | 16% / 100% | 21% / 100% | 34% / 100% | 57% / 100% |
| Figure handling (choice) | 0% / 82% | 13% / 87% | 26% / 95% | 84% / 98% | 100% / 100% |
| Figure clarity (score) | 0% / 76% | 6% / 85% | 23% / 94% | 84% / 100% | 100% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 2 | 0 | 0 |
| simile | 3 | 28 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 8 | 0 | 3 | 20 | 0 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 114. Lowest ten: 2:12 kt_trje (0.10); 2:13 kt_eqaj (0.20); 3:5 kt_f8tn (0.20); 3:2 kt_xrq8 (0.25); 1:3 kt_bgv4 (0.30); 1:6 kt_nsxd (0.30); 1:9 kt_ss39 (0.30); 1:9 kt_x67x (0.30); 3:10 kt_cf9q (0.30); 3:8 kt_dxb8 (0.30)

