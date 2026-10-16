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

| run | model version | calls | median latency | total cost |
|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 453 | 267 ms | $0.0203 |
| jev-jev-preview | jev-1.14.0 | 453 | 257 ms | $0.0203 |
| jev-jev-preview+no-approved | jev-1.14.0 | 453 | 259 ms | $0.0192 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 453 | 2662 ms | $0.1423 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 32% | 206 | 98% | 99% | 0.947 | 0.046 |
| jev-jev-preview | 182 | 32% | 206 | 98% | 99% | 0.954 | 0.054 |
| jev-jev-preview+no-approved | 182 | 36% | 206 | 99% | 100% | 0.961 | 0.080 |
| openrouter-claude-haiku-5.5 | 182 | 32% | 206 | 99% | 99% | 0.972 | 0.057 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 97% / 0.31 | 99% / 0.11 | 32% / 0.82 | 99% / 0.10 |
| jev-jev-preview | 97% / 0.31 | 99% / 0.11 | 32% / 0.84 | 99% / 0.08 |
| jev-jev-preview+no-approved | 97% / 0.39 | 100% / 0.11 | 36% / 0.85 | 100% / 0.09 |
| openrouter-claude-haiku-5.5 | 97% / 0.12 | 100% / 0.09 | 32% / 0.81 | 99% / 0.07 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 42% | 62 | 97% | 100% | 0.969 | 0.063 |
| jev-jev-preview | 31 | 48% | 62 | 98% | 100% | 0.971 | 0.069 |
| jev-jev-preview+no-approved | 31 | 48% | 62 | 98% | 100% | 0.971 | 0.070 |
| openrouter-claude-haiku-5.5 | 31 | 94% | 62 | 100% | 100% | 0.966 | 0.102 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.04 | 26% / 0.91 | 94% / 0.40 | 6% / 0.95 | 0% / 0.98 | 42% / 0.82 | 100% / 0.01 |
| jev-jev-preview | 100% / 0.04 | 35% / 0.89 | 97% / 0.39 | 13% / 0.93 | 13% / 0.96 | 48% / 0.82 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.04 | 35% / 0.89 | 97% / 0.39 | 13% / 0.93 | 13% / 0.96 | 48% / 0.82 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.09 | 71% / 0.83 | 100% / 0.35 | 55% / 0.86 | 29% / 0.92 | 94% / 0.74 | 100% / 0.06 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 86%, jev-jev-preview 86%, jev-jev-preview+no-approved 86%, openrouter-claude-haiku-5.5 87%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 77% | 62 | 98% | 100% | 0.948 | 0.113 |
| jev-jev-preview | 31 | 84% | 62 | 100% | 100% | 0.954 | 0.142 |
| jev-jev-preview+no-approved | 31 | 87% | 62 | 100% | 100% | 0.955 | 0.142 |
| openrouter-claude-haiku-5.5 | 31 | 90% | 62 | 100% | 100% | 0.973 | 0.098 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.04 | 74% / 0.71 | 97% / 0.30 | 26% / 0.89 | 100% / 0.69 | 77% / 0.69 | 100% / 0.01 |
| jev-jev-preview | 100% / 0.05 | 81% / 0.72 | 100% / 0.32 | 42% / 0.86 | 100% / 0.71 | 84% / 0.68 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.05 | 81% / 0.72 | 100% / 0.32 | 42% / 0.86 | 100% / 0.71 | 87% / 0.68 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.08 | 84% / 0.79 | 100% / 0.36 | 48% / 0.89 | 77% / 0.83 | 90% / 0.75 | 100% / 0.08 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=297, said 0.07, was 0.02; 0.2–0.4: n=71, said 0.28, was 0.20; 0.4–0.6: n=32, said 0.49, was 0.44; 0.6–0.8: n=28, said 0.70, was 0.57; 0.8–1.0: n=142, said 0.95, was 0.94

Calibration, figure handling (choice): 0.0–0.2: n=72, said 0.03, was 0.01; 0.2–0.4: n=10, said 0.31, was 0.40; 0.4–0.6: n=9, said 0.51, was 0.44; 0.6–0.8: n=12, said 0.69, was 0.50; 0.8–1.0: n=114, said 0.96, was 0.96

Calibration, figure clarity (score): 0.0–0.2: n=75, said 0.03, was 0.07; 0.2–0.4: n=23, said 0.31, was 0.35; 0.4–0.6: n=17, said 0.53, was 0.82; 0.6–0.8: n=38, said 0.71, was 0.89; 0.8–1.0: n=64, said 0.91, was 0.98

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 13% / 90% | 23% / 95% | 27% / 98% | 32% / 98% | 48% / 99% |
| Figure handling (choice) | 16% / 77% | 23% / 92% | 29% / 92% | 42% / 97% | 55% / 98% |
| Figure clarity (score) | 19% / 90% | 35% / 97% | 55% / 98% | 77% / 98% | 87% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 1 | 1 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 1 | 0 | 30 | 0 | 0 |
| lost | 8 | 0 | 7 | 15 | 1 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 96. Lowest ten: 2:15 kt_rvsu (0.06); 3:3 kt_strs (0.07); 3:5 fig_k1a6_clarity (0.09); 2:13 kt_eqaj (0.11); 3:15 fig_f4vc_clarity (0.11); 3:15 fig_f4vc_handling (0.14); 2:3 kt_khhe (0.14); 1:10 fig_pu74_clarity (0.18); 1:9 kt_nngz (0.19); 2:10 kt_d9wq (0.20)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=295, said 0.06, was 0.02; 0.2–0.4: n=65, said 0.28, was 0.15; 0.4–0.6: n=37, said 0.48, was 0.35; 0.6–0.8: n=24, said 0.70, was 0.58; 0.8–1.0: n=149, said 0.95, was 0.94

Calibration, figure handling (choice): 0.0–0.2: n=72, said 0.02, was 0.00; 0.2–0.4: n=9, said 0.30, was 0.56; 0.4–0.6: n=11, said 0.50, was 0.36; 0.6–0.8: n=15, said 0.71, was 0.47; 0.8–1.0: n=110, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=72, said 0.03, was 0.04; 0.2–0.4: n=20, said 0.30, was 0.30; 0.4–0.6: n=24, said 0.50, was 0.67; 0.6–0.8: n=36, said 0.70, was 0.97; 0.8–1.0: n=65, said 0.89, was 0.98

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 12% / 91% | 18% / 97% | 23% / 98% | 32% / 98% | 42% / 99% |
| Figure handling (choice) | 13% / 76% | 19% / 89% | 29% / 97% | 48% / 98% | 65% / 98% |
| Figure clarity (score) | 23% / 90% | 35% / 98% | 61% / 98% | 84% / 100% | 94% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 0 | 2 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 1 | 0 | 29 | 1 | 0 |
| lost | 8 | 0 | 6 | 16 | 1 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 100. Lowest ten: 2:15 kt_rvsu (0.05); 3:3 kt_strs (0.06); 2:13 kt_eqaj (0.10); 1:9 kt_nngz (0.11); 3:15 fig_f4vc_clarity (0.15); 2:10 kt_d9wq (0.18); 1:10 fig_pu74_clarity (0.19); 2:3 kt_khhe (0.20); 3:15 fig_f4vc_handling (0.21); 2:8 kt_zdzc (0.23)


## Detail: jev-jev-preview+no-approved

Calibration, key terms (noul): 0.0–0.2: n=278, said 0.06, was 0.01; 0.2–0.4: n=59, said 0.29, was 0.07; 0.4–0.6: n=44, said 0.50, was 0.32; 0.6–0.8: n=36, said 0.70, was 0.56; 0.8–1.0: n=153, said 0.93, was 0.92

Calibration, figure handling (choice): 0.0–0.2: n=73, said 0.03, was 0.01; 0.2–0.4: n=8, said 0.32, was 0.50; 0.4–0.6: n=11, said 0.51, was 0.36; 0.6–0.8: n=15, said 0.72, was 0.47; 0.8–1.0: n=110, said 0.95, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=72, said 0.03, was 0.04; 0.2–0.4: n=19, said 0.30, was 0.26; 0.4–0.6: n=26, said 0.50, was 0.69; 0.6–0.8: n=34, said 0.70, was 0.97; 0.8–1.0: n=66, said 0.89, was 0.98

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 5% / 84% | 15% / 94% | 23% / 96% | 36% / 99% | 57% / 100% |
| Figure handling (choice) | 13% / 76% | 19% / 89% | 29% / 97% | 48% / 98% | 68% / 98% |
| Figure clarity (score) | 23% / 90% | 35% / 98% | 58% / 98% | 87% / 100% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 0 | 2 | 0 |
| simile | 1 | 29 | 1 | 0 | 0 |
| plain | 1 | 0 | 29 | 1 | 0 |
| lost | 8 | 0 | 6 | 16 | 1 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 108. Lowest ten: 3:3 kt_strs (0.10); 2:15 kt_rvsu (0.12); 3:15 fig_f4vc_clarity (0.15); 1:9 kt_nngz (0.16); 1:10 fig_pu74_clarity (0.19); 3:15 fig_f4vc_handling (0.19); 2:12 fig_qy8k_clarity (0.25); 3:5 fig_k1a6_clarity (0.27); 2:13 kt_eqaj (0.28); 2:8 fig_xy14_clarity (0.30)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=356, said 0.05, was 0.03; 0.2–0.4: n=35, said 0.26, was 0.31; 0.4–0.6: n=10, said 0.50, was 0.70; 0.6–0.8: n=22, said 0.66, was 0.73; 0.8–1.0: n=147, said 0.93, was 0.95

Calibration, figure handling (choice): 0.0–0.2: n=75, said 0.08, was 0.01; 0.2–0.4: n=9, said 0.31, was 0.33; 0.4–0.6: n=9, said 0.46, was 0.22; 0.6–0.8: n=23, said 0.72, was 0.91; 0.8–1.0: n=101, said 0.89, was 0.96

Calibration, figure clarity (score): 0.0–0.2: n=65, said 0.08, was 0.00; 0.2–0.4: n=20, said 0.26, was 0.15; 0.4–0.6: n=8, said 0.43, was 0.50; 0.6–0.8: n=25, said 0.70, was 0.84; 0.8–1.0: n=99, said 0.87, was 0.97

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 12% / 96% | 19% / 97% | 24% / 98% | 32% / 99% | 58% / 99% |
| Figure handling (choice) | 13% / 89% | 23% / 92% | 48% / 94% | 94% / 100% | 100% / 100% |
| Figure clarity (score) | 16% / 89% | 19% / 92% | 26% / 95% | 90% / 100% | 100% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 29 | 0 | 1 | 1 | 0 |
| simile | 9 | 22 | 0 | 0 | 0 |
| plain | 0 | 0 | 31 | 0 | 0 |
| lost | 6 | 0 | 1 | 23 | 1 |
| distorted | 0 | 0 | 0 | 1 | 30 |

Real items flagged at 0.9: 116. Lowest ten: 2:15 kt_rvsu (0.04); 2:15 kt_pnzt (0.08); 3:13 kt_v462 (0.08); 1:9 kt_ss39 (0.10); 2:10 kt_d9wq (0.10); 1:10 kt_p8yj (0.15); 1:11 kt_bjyb (0.15); 1:6 kt_evqx (0.15); 2:3 kt_khhe (0.15); 2:8 fig_xy14_handling (0.20)

