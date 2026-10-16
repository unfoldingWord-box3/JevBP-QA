# IRV (Indian Revised Version): Titus checked against the Greek

Target `hi_irv` (Hindi). Headline threshold: an item is auto-logged as a pass when its pass probability is at least 0.9; anything lower goes to review.

Sources (pinned commits):

- `ugnt`: unfoldingWord/el-x-koine_ugnt @ `fc95b2b8aa` (CC BY-SA 4.0)
- `en_tn`: unfoldingWord/en_tn @ `a0959d790f` (CC BY-SA 4.0)
- `en_twl`: unfoldingWord/en_twl @ `d880052cb7` (CC BY-SA 4.0)
- `en_tw`: unfoldingWord/en_tw @ `6e3900f8c2` (CC BY-SA 4.0)
- `hi_irv`: Door43-Catalog/hi_irv @ `d72ad2a8f9` (CC BY-SA 4.0)
- `hi_tw`: Door43-Catalog/hi_tw @ `64be591fa4` (CC BY-SA 4.0)

## Speed and cost

Cost and latency are those of the call that produced each answer (re-runs are served from cache). Unanswered = questions with no answer (API error or partial reply); they are left out of every score below.

| run | model version | calls | median latency | total cost | unanswered |
|---|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 445 | 267 ms | $0.0200 | 0 |
| jev-jev-preview | jev-1.14.0 | 445 | 265 ms | $0.0200 | 0 |
| jev-jev-preview+no-approved | jev-1.14.0 | 445 | 267 ms | $0.0190 | 0 |
| jev-jev-preview+no-renderings | jev-1.14.0 | 445 | 266 ms | $0.0196 | 0 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 445 | 2565 ms | $0.1395 | 0 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 33% | 198 | 99% | 100% | 0.955 | 0.052 |
| jev-jev-preview | 182 | 31% | 198 | 99% | 100% | 0.961 | 0.058 |
| jev-jev-preview+no-approved | 182 | 36% | 198 | 99% | 100% | 0.965 | 0.097 |
| jev-jev-preview+no-renderings | 182 | 36% | 198 | 98% | 100% | 0.956 | 0.109 |
| openrouter-claude-haiku-5.5 | 182 | 33% | 198 | 99% | 100% | 0.978 | 0.067 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 99% / 0.29 | 99% / 0.11 | 33% / 0.82 | 100% / 0.06 |
| jev-jev-preview | 99% / 0.29 | 99% / 0.10 | 31% / 0.84 | 100% / 0.04 |
| jev-jev-preview+no-approved | 99% / 0.37 | 100% / 0.14 | 36% / 0.85 | 100% / 0.05 |
| jev-jev-preview+no-renderings | 99% / 0.29 | 98% / 0.31 | 36% / 0.85 | 100% / 0.04 |
| openrouter-claude-haiku-5.5 | 99% / 0.10 | 100% / 0.09 | 33% / 0.81 | 100% / 0.04 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 42% | 62 | 97% | 100% | 0.967 | 0.042 |
| jev-jev-preview | 31 | 48% | 62 | 98% | 100% | 0.968 | 0.071 |
| jev-jev-preview+no-approved | 31 | 45% | 62 | 98% | 100% | 0.970 | 0.071 |
| jev-jev-preview+no-renderings | 31 | 52% | 62 | 95% | 100% | 0.947 | 0.062 |
| openrouter-claude-haiku-5.5 | 31 | 97% | 62 | 100% | 100% | 0.975 | 0.084 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.04 | 23% / 0.91 | 94% / 0.43 | 6% / 0.95 | 0% / 0.98 | 42% / 0.81 | 100% / 0.01 |
| jev-jev-preview | 100% / 0.04 | 35% / 0.89 | 97% / 0.41 | 13% / 0.93 | 6% / 0.96 | 48% / 0.81 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.04 | 35% / 0.89 | 97% / 0.41 | 13% / 0.93 | 6% / 0.96 | 45% / 0.82 | 100% / 0.01 |
| jev-jev-preview+no-renderings | 100% / 0.18 | 23% / 0.90 | 90% / 0.52 | 29% / 0.91 | 16% / 0.95 | 52% / 0.84 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.11 | 71% / 0.82 | 100% / 0.32 | 39% / 0.88 | 26% / 0.91 | 97% / 0.73 | 100% / 0.06 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 87%, jev-jev-preview 86%, jev-jev-preview+no-approved 86%, jev-jev-preview+no-renderings 79%, openrouter-claude-haiku-5.5 88%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 74% | 62 | 98% | 100% | 0.944 | 0.124 |
| jev-jev-preview | 31 | 81% | 62 | 100% | 100% | 0.953 | 0.133 |
| jev-jev-preview+no-approved | 31 | 84% | 62 | 100% | 100% | 0.954 | 0.146 |
| jev-jev-preview+no-renderings | 31 | 94% | 62 | 98% | 100% | 0.922 | 0.116 |
| openrouter-claude-haiku-5.5 | 31 | 84% | 62 | 100% | 100% | 0.970 | 0.107 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.04 | 77% / 0.72 | 97% / 0.34 | 29% / 0.88 | 100% / 0.69 | 74% / 0.69 | 100% / 0.01 |
| jev-jev-preview | 100% / 0.04 | 81% / 0.72 | 100% / 0.33 | 39% / 0.86 | 100% / 0.71 | 81% / 0.68 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.04 | 81% / 0.72 | 100% / 0.33 | 39% / 0.86 | 100% / 0.71 | 84% / 0.68 | 100% / 0.01 |
| jev-jev-preview+no-renderings | 100% / 0.13 | 84% / 0.72 | 97% / 0.41 | 58% / 0.84 | 90% / 0.67 | 94% / 0.69 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.11 | 87% / 0.80 | 100% / 0.34 | 32% / 0.91 | 74% / 0.82 | 84% / 0.75 | 100% / 0.08 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=296, said 0.07, was 0.02; 0.2–0.4: n=67, said 0.28, was 0.22; 0.4–0.6: n=27, said 0.48, was 0.44; 0.6–0.8: n=27, said 0.70, was 0.67; 0.8–1.0: n=134, said 0.95, was 0.99

Calibration, figure handling (choice): 0.0–0.2: n=71, said 0.03, was 0.01; 0.2–0.4: n=8, said 0.32, was 0.38; 0.4–0.6: n=12, said 0.47, was 0.42; 0.6–0.8: n=10, said 0.69, was 0.40; 0.8–1.0: n=116, said 0.96, was 0.96

Calibration, figure clarity (score): 0.0–0.2: n=74, said 0.03, was 0.07; 0.2–0.4: n=19, said 0.30, was 0.32; 0.4–0.6: n=21, said 0.50, was 0.76; 0.6–0.8: n=38, said 0.71, was 0.87; 0.8–1.0: n=65, said 0.91, was 0.98

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 13% / 93% | 21% / 97% | 27% / 99% | 33% / 99% | 48% / 99% |
| Figure handling (choice) | 16% / 77% | 26% / 89% | 29% / 92% | 42% / 97% | 52% / 98% |
| Figure clarity (score) | 26% / 89% | 35% / 98% | 55% / 98% | 74% / 98% | 87% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 30 | 0 | 0 | 1 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 9 | 0 | 5 | 16 | 1 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 96. Lowest ten: 2:15 kt_rvsu (0.06); 3:3 kt_strs (0.07); 2:13 kt_eqaj (0.11); 3:15 fig_f4vc_clarity (0.11); 3:5 fig_k1a6_clarity (0.11); 3:15 fig_f4vc_handling (0.12); 2:3 kt_khhe (0.15); 1:10 fig_pu74_clarity (0.16); 1:9 kt_nngz (0.17); 1:3 kt_yu3w (0.20)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=294, said 0.06, was 0.02; 0.2–0.4: n=60, said 0.28, was 0.17; 0.4–0.6: n=31, said 0.47, was 0.35; 0.6–0.8: n=24, said 0.69, was 0.71; 0.8–1.0: n=142, said 0.95, was 0.98

Calibration, figure handling (choice): 0.0–0.2: n=71, said 0.03, was 0.01; 0.2–0.4: n=9, said 0.28, was 0.44; 0.4–0.6: n=10, said 0.46, was 0.40; 0.6–0.8: n=16, said 0.69, was 0.38; 0.8–1.0: n=111, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=72, said 0.03, was 0.04; 0.2–0.4: n=21, said 0.31, was 0.29; 0.4–0.6: n=24, said 0.50, was 0.75; 0.6–0.8: n=34, said 0.70, was 0.94; 0.8–1.0: n=66, said 0.89, was 0.98

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 12% / 94% | 18% / 97% | 24% / 98% | 31% / 99% | 41% / 99% |
| Figure handling (choice) | 13% / 79% | 23% / 89% | 29% / 97% | 48% / 98% | 65% / 98% |
| Figure clarity (score) | 19% / 90% | 35% / 98% | 68% / 98% | 81% / 100% | 94% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 0 | 2 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 2 | 0 | 28 | 1 | 0 |
| lost | 7 | 0 | 6 | 17 | 1 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 97. Lowest ten: 2:15 kt_rvsu (0.05); 3:3 kt_strs (0.06); 2:13 kt_eqaj (0.10); 1:9 kt_nngz (0.12); 2:10 kt_d9wq (0.15); 3:15 fig_f4vc_clarity (0.15); 3:15 fig_f4vc_handling (0.17); 1:10 fig_pu74_clarity (0.18); 2:3 kt_khhe (0.21); 1:3 kt_yu3w (0.25)


## Detail: jev-jev-preview+no-approved

Calibration, key terms (noul): 0.0–0.2: n=273, said 0.06, was 0.01; 0.2–0.4: n=55, said 0.29, was 0.09; 0.4–0.6: n=43, said 0.50, was 0.30; 0.6–0.8: n=37, said 0.71, was 0.57; 0.8–1.0: n=143, said 0.93, was 0.98

Calibration, figure handling (choice): 0.0–0.2: n=71, said 0.03, was 0.01; 0.2–0.4: n=8, said 0.27, was 0.38; 0.4–0.6: n=11, said 0.48, was 0.45; 0.6–0.8: n=16, said 0.70, was 0.38; 0.8–1.0: n=111, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=71, said 0.03, was 0.03; 0.2–0.4: n=21, said 0.30, was 0.29; 0.4–0.6: n=25, said 0.50, was 0.76; 0.6–0.8: n=32, said 0.70, was 0.94; 0.8–1.0: n=68, said 0.89, was 0.99

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 5% / 85% | 15% / 94% | 23% / 98% | 36% / 99% | 57% / 100% |
| Figure handling (choice) | 10% / 79% | 19% / 89% | 29% / 97% | 45% / 98% | 61% / 98% |
| Figure clarity (score) | 19% / 90% | 35% / 98% | 61% / 98% | 84% / 100% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 0 | 2 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 2 | 0 | 28 | 1 | 0 |
| lost | 7 | 0 | 6 | 17 | 1 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 106. Lowest ten: 2:15 kt_rvsu (0.12); 3:3 kt_strs (0.12); 1:9 kt_nngz (0.16); 3:15 fig_f4vc_clarity (0.17); 3:15 fig_f4vc_handling (0.20); 1:10 fig_pu74_clarity (0.21); 2:12 fig_qy8k_clarity (0.26); 3:5 fig_k1a6_clarity (0.26); 2:13 kt_eqaj (0.29); 2:8 fig_xy14_clarity (0.29)


## Detail: jev-jev-preview+no-renderings

Calibration, key terms (noul): 0.0–0.2: n=232, said 0.06, was 0.00; 0.2–0.4: n=97, said 0.28, was 0.11; 0.4–0.6: n=45, said 0.47, was 0.27; 0.6–0.8: n=33, said 0.65, was 0.58; 0.8–1.0: n=144, said 0.94, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=58, said 0.03, was 0.00; 0.2–0.4: n=11, said 0.29, was 0.09; 0.4–0.6: n=12, said 0.48, was 0.42; 0.6–0.8: n=18, said 0.70, was 0.44; 0.8–1.0: n=118, said 0.93, was 0.93

Calibration, figure clarity (score): 0.0–0.2: n=62, said 0.04, was 0.03; 0.2–0.4: n=19, said 0.29, was 0.26; 0.4–0.6: n=34, said 0.51, was 0.65; 0.6–0.8: n=45, said 0.71, was 0.89; 0.8–1.0: n=57, said 0.88, was 0.96

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 8% / 88% | 20% / 96% | 23% / 98% | 36% / 98% | 52% / 99% |
| Figure handling (choice) | 10% / 68% | 13% / 81% | 23% / 87% | 52% / 95% | 74% / 98% |
| Figure clarity (score) | 13% / 81% | 39% / 97% | 65% / 97% | 94% / 98% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 27 | 0 | 2 | 2 | 0 |
| simile | 2 | 27 | 2 | 0 | 0 |
| plain | 3 | 0 | 28 | 0 | 0 |
| lost | 10 | 0 | 8 | 13 | 0 |
| distorted | 2 | 0 | 1 | 0 | 28 |

Real items flagged at 0.9: 111. Lowest ten: 1:10 fig_pu74_clarity (0.13); 1:11 kt_bjyb (0.21); 1:9 kt_nngz (0.22); 2:15 kt_rvsu (0.22); 2:13 kt_eqaj (0.25); 2:10 kt_d9wq (0.28); 3:3 kt_strs (0.30); 1:6 kt_evqx (0.33); 2:12 kt_trje (0.34); 1:10 fig_pu74_handling (0.37)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=353, said 0.04, was 0.02; 0.2–0.4: n=30, said 0.26, was 0.43; 0.4–0.6: n=8, said 0.48, was 0.75; 0.6–0.8: n=20, said 0.69, was 0.85; 0.8–1.0: n=140, said 0.93, was 0.99

Calibration, figure handling (choice): 0.0–0.2: n=73, said 0.08, was 0.01; 0.2–0.4: n=14, said 0.27, was 0.21; 0.4–0.6: n=5, said 0.48, was 0.40; 0.6–0.8: n=30, said 0.74, was 0.83; 0.8–1.0: n=95, said 0.89, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=67, said 0.08, was 0.00; 0.2–0.4: n=19, said 0.27, was 0.21; 0.4–0.6: n=8, said 0.47, was 0.62; 0.6–0.8: n=26, said 0.71, was 0.81; 0.8–1.0: n=97, said 0.88, was 0.97

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 13% / 97% | 18% / 97% | 24% / 99% | 33% / 99% | 60% / 99% |
| Figure handling (choice) | 13% / 87% | 16% / 92% | 48% / 97% | 97% / 100% | 100% / 100% |
| Figure clarity (score) | 13% / 87% | 19% / 94% | 32% / 95% | 84% / 100% | 100% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 28 | 0 | 2 | 1 | 0 |
| simile | 7 | 24 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 6 | 0 | 0 | 24 | 1 |
| distorted | 0 | 0 | 1 | 1 | 29 |

Real items flagged at 0.9: 116. Lowest ten: 2:15 kt_rvsu (0.04); 3:13 kt_v462 (0.05); 1:9 kt_ss39 (0.08); 2:15 kt_pnzt (0.08); 2:10 kt_d9wq (0.10); 2:3 kt_khhe (0.10); 3:3 kt_strs (0.10); 1:10 kt_p8yj (0.15); 3:15 fig_f4vc_handling (0.20); 1:6 kt_evqx (0.20)

