# BSB (Berean Standard Bible): Titus checked against the Greek

Target `bsb` (English). Headline threshold: an item is auto-logged as a pass when its pass probability is at least 0.9; anything lower goes to review.

Sources (pinned commits):

- `ugnt`: unfoldingWord/el-x-koine_ugnt @ `fc95b2b8aa` (CC BY-SA 4.0)
- `en_tn`: unfoldingWord/en_tn @ `a0959d790f` (CC BY-SA 4.0)
- `en_twl`: unfoldingWord/en_twl @ `d880052cb7` (CC BY-SA 4.0)
- `en_tw`: unfoldingWord/en_tw @ `6e3900f8c2` (CC BY-SA 4.0)
- `bsb`: Worldview/en_bsb @ `21bca0199a` (Public domain (BSB); alignment CC BY-SA 4.0)

## Speed and cost

| run | model version | calls | median latency | total cost |
|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 455 | 264 ms | $0.0188 |
| jev-jev-latest+no-approved | jev-1.13.0 | 409 | 261 ms | $0.0151 |
| jev-jev-preview | jev-1.14.0 | 455 | 265 ms | $0.0188 |
| jev-jev-preview+no-approved | jev-1.14.0 | 409 | 262 ms | $0.0151 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 455 | 2370 ms | $0.1242 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 19% | 208 | 98% | 100% | 0.973 | 0.069 |
| jev-jev-latest+no-approved | 182 | 18% | 208 | 98% | – | 0.980 | 0.094 |
| jev-jev-preview | 182 | 15% | 208 | 99% | 100% | 0.983 | 0.076 |
| jev-jev-preview+no-approved | 182 | 16% | 208 | 99% | – | 0.984 | 0.093 |
| openrouter-claude-haiku-5.5 | 182 | 23% | 208 | 99% | 98% | 0.989 | 0.068 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 96% / 0.34 | 100% / 0.07 | 19% / 0.90 | 100% / 0.16 |
| jev-jev-latest+no-approved | 95% / 0.39 | 100% / 0.08 | 18% / 0.92 | – |
| jev-jev-preview | 97% / 0.32 | 100% / 0.07 | 15% / 0.92 | 100% / 0.13 |
| jev-jev-preview+no-approved | 97% / 0.35 | 100% / 0.08 | 16% / 0.92 | – |
| openrouter-claude-haiku-5.5 | 98% / 0.08 | 100% / 0.05 | 23% / 0.86 | 98% / 0.07 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 16% | 54 | 100% | 100% | 0.995 | 0.054 |
| jev-jev-latest+no-approved | 31 | 16% | 54 | 100% | – | 0.995 | 0.048 |
| jev-jev-preview | 31 | 10% | 54 | 100% | 100% | 0.994 | 0.053 |
| jev-jev-preview+no-approved | 31 | 16% | 54 | 100% | – | 0.994 | 0.053 |
| openrouter-claude-haiku-5.5 | 31 | 74% | 54 | 100% | 100% | 0.989 | 0.126 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.03 | 13% / 0.94 | 84% / 0.43 | 13% / 0.96 | 13% / 0.95 | 16% / 0.94 | 100% / 0.02 |
| jev-jev-latest+no-approved | 100% / 0.03 | 13% / 0.94 | 84% / 0.43 | 13% / 0.96 | 13% / 0.95 | 16% / 0.94 | – |
| jev-jev-preview | 100% / 0.03 | 19% / 0.94 | 87% / 0.46 | 6% / 0.96 | 13% / 0.94 | 10% / 0.93 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.03 | 19% / 0.94 | 87% / 0.46 | 6% / 0.96 | 13% / 0.94 | 16% / 0.93 | – |
| openrouter-claude-haiku-5.5 | 100% / 0.10 | 71% / 0.84 | 100% / 0.45 | 58% / 0.87 | 32% / 0.90 | 74% / 0.81 | 100% / 0.06 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 90%, jev-jev-latest+no-approved 90%, jev-jev-preview 90%, jev-jev-preview+no-approved 90%, openrouter-claude-haiku-5.5 86%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 52% | 54 | 100% | 100% | 0.985 | 0.130 |
| jev-jev-latest+no-approved | 31 | 48% | 54 | 100% | – | 0.985 | 0.131 |
| jev-jev-preview | 31 | 55% | 54 | 100% | 100% | 0.992 | 0.118 |
| jev-jev-preview+no-approved | 31 | 55% | 54 | 100% | – | 0.992 | 0.119 |
| openrouter-claude-haiku-5.5 | 31 | 81% | 54 | 100% | 100% | 0.992 | 0.135 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.02 | 68% / 0.82 | 100% / 0.30 | 32% / 0.89 | 84% / 0.64 | 52% / 0.85 | 100% / 0.03 |
| jev-jev-latest+no-approved | 100% / 0.02 | 68% / 0.82 | 100% / 0.30 | 32% / 0.89 | 84% / 0.64 | 48% / 0.85 | – |
| jev-jev-preview | 100% / 0.04 | 58% / 0.81 | 100% / 0.33 | 39% / 0.90 | 74% / 0.72 | 55% / 0.84 | 100% / 0.02 |
| jev-jev-preview+no-approved | 100% / 0.04 | 58% / 0.81 | 100% / 0.33 | 39% / 0.90 | 74% / 0.72 | 55% / 0.84 | – |
| openrouter-claude-haiku-5.5 | 100% / 0.09 | 74% / 0.82 | 100% / 0.42 | 26% / 0.90 | 77% / 0.80 | 81% / 0.82 | 100% / 0.08 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=270, said 0.09, was 0.01; 0.2–0.4: n=84, said 0.26, was 0.02; 0.4–0.6: n=22, said 0.50, was 0.41; 0.6–0.8: n=29, said 0.68, was 0.41; 0.8–1.0: n=167, said 0.96, was 0.93

Calibration, figure handling (choice): 0.0–0.2: n=72, said 0.03, was 0.00; 0.2–0.4: n=7, said 0.32, was 0.00; 0.4–0.6: n=6, said 0.53, was 0.50; 0.6–0.8: n=11, said 0.73, was 0.73; 0.8–1.0: n=121, said 0.96, was 1.00

Calibration, figure clarity (score): 0.0–0.2: n=79, said 0.04, was 0.04; 0.2–0.4: n=13, said 0.30, was 0.54; 0.4–0.6: n=15, said 0.51, was 0.87; 0.6–0.8: n=26, said 0.70, was 0.96; 0.8–1.0: n=84, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 5% / 87% | 10% / 94% | 14% / 95% | 19% / 98% | 28% / 99% |
| Figure handling (choice) | 0% / 91% | 6% / 94% | 6% / 100% | 16% / 100% | 19% / 100% |
| Figure clarity (score) | 6% / 96% | 13% / 100% | 23% / 100% | 52% / 100% | 68% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 38 | 0 | 1 | 0 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 4 | 0 | 1 | 11 | 7 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 56. Lowest ten: 1:9 kt_nngz (0.11); 2:13 kt_eqaj (0.15); 3:2 kt_xrq8 (0.15); 1:10 fig_pu74_clarity (0.25); 2:5 kt_rhfd (0.26); 1:9 kt_ss39 (0.31); 3:5 fig_k1a6_clarity (0.40); 1:7 kt_rfj7 (0.41); 3:13 kt_v462 (0.44); 2:3 kt_khhe (0.49)


## Detail: jev-jev-latest+no-approved

Calibration, key terms (noul): 0.0–0.2: n=122, said 0.06, was 0.01; 0.2–0.4: n=48, said 0.27, was 0.04; 0.4–0.6: n=14, said 0.48, was 0.14; 0.6–0.8: n=28, said 0.71, was 0.43; 0.8–1.0: n=178, said 0.94, was 0.93

Calibration, figure handling (choice): 0.0–0.2: n=41, said 0.04, was 0.00; 0.2–0.4: n=7, said 0.32, was 0.00; 0.4–0.6: n=6, said 0.53, was 0.50; 0.6–0.8: n=11, said 0.73, was 0.73; 0.8–1.0: n=121, said 0.96, was 1.00

Calibration, figure clarity (score): 0.0–0.2: n=48, said 0.04, was 0.06; 0.2–0.4: n=13, said 0.30, was 0.54; 0.4–0.6: n=16, said 0.51, was 0.88; 0.6–0.8: n=25, said 0.71, was 0.96; 0.8–1.0: n=84, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 3% / 84% | 5% / 90% | 9% / 94% | 18% / 98% | 35% / 100% |
| Figure handling (choice) | 3% / 91% | 3% / 94% | 6% / 100% | 16% / 100% | 19% / 100% |
| Figure clarity (score) | 6% / 96% | 13% / 100% | 23% / 100% | 48% / 100% | 68% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 38 | 0 | 1 | 0 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 4 | 0 | 1 | 11 | 7 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 53. Lowest ten: 1:9 kt_nngz (0.19); 3:2 kt_xrq8 (0.20); 1:10 fig_pu74_clarity (0.22); 2:13 kt_eqaj (0.24); 1:9 kt_ss39 (0.41); 2:5 kt_rhfd (0.41); 3:5 fig_k1a6_clarity (0.45); 1:10 fig_pu74_handling (0.49); 3:15 fig_f4vc_clarity (0.57); 3:5 kt_sqsf (0.64)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=284, said 0.08, was 0.01; 0.2–0.4: n=71, said 0.27, was 0.01; 0.4–0.6: n=19, said 0.47, was 0.16; 0.6–0.8: n=24, said 0.69, was 0.33; 0.8–1.0: n=174, said 0.96, was 0.96

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.02, was 0.00; 0.2–0.4: n=6, said 0.28, was 0.00; 0.4–0.6: n=10, said 0.48, was 0.40; 0.6–0.8: n=11, said 0.72, was 0.73; 0.8–1.0: n=121, said 0.96, was 0.99

Calibration, figure clarity (score): 0.0–0.2: n=76, said 0.04, was 0.03; 0.2–0.4: n=8, said 0.29, was 0.25; 0.4–0.6: n=21, said 0.49, was 0.76; 0.6–0.8: n=25, said 0.72, was 1.00; 0.8–1.0: n=87, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 3% / 89% | 5% / 94% | 8% / 97% | 15% / 99% | 24% / 99% |
| Figure handling (choice) | 0% / 89% | 6% / 93% | 10% / 98% | 10% / 100% | 29% / 100% |
| Figure clarity (score) | 6% / 98% | 10% / 100% | 26% / 100% | 55% / 100% | 68% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 38 | 0 | 1 | 0 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 1 | 0 | 30 | 0 | 0 |
| lost | 6 | 0 | 2 | 9 | 6 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 48. Lowest ten: 1:9 kt_nngz (0.12); 3:2 kt_xrq8 (0.17); 2:13 kt_eqaj (0.19); 3:13 kt_v462 (0.20); 1:10 fig_pu74_clarity (0.27); 1:9 kt_ss39 (0.42); 2:5 kt_rhfd (0.43); 3:15 fig_f4vc_clarity (0.46); 2:5 kt_mguz (0.51); 1:10 fig_pu74_handling (0.52)


## Detail: jev-jev-preview+no-approved

Calibration, key terms (noul): 0.0–0.2: n=127, said 0.07, was 0.01; 0.2–0.4: n=46, said 0.28, was 0.04; 0.4–0.6: n=23, said 0.50, was 0.13; 0.6–0.8: n=20, said 0.74, was 0.45; 0.8–1.0: n=174, said 0.95, was 0.96

Calibration, figure handling (choice): 0.0–0.2: n=38, said 0.03, was 0.00; 0.2–0.4: n=6, said 0.28, was 0.00; 0.4–0.6: n=10, said 0.48, was 0.40; 0.6–0.8: n=11, said 0.72, was 0.73; 0.8–1.0: n=121, said 0.96, was 0.99

Calibration, figure clarity (score): 0.0–0.2: n=45, said 0.05, was 0.04; 0.2–0.4: n=8, said 0.29, was 0.25; 0.4–0.6: n=21, said 0.49, was 0.76; 0.6–0.8: n=25, said 0.71, was 1.00; 0.8–1.0: n=87, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 2% / 86% | 4% / 93% | 8% / 97% | 16% / 99% | 31% / 99% |
| Figure handling (choice) | 0% / 89% | 6% / 93% | 10% / 98% | 16% / 100% | 26% / 100% |
| Figure clarity (score) | 6% / 98% | 16% / 100% | 26% / 100% | 55% / 100% | 68% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 38 | 0 | 1 | 0 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 1 | 0 | 30 | 0 | 0 |
| lost | 6 | 0 | 2 | 9 | 6 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 52. Lowest ten: 1:9 kt_nngz (0.14); 1:10 fig_pu74_clarity (0.26); 2:13 kt_eqaj (0.32); 3:2 kt_xrq8 (0.32); 3:15 fig_f4vc_clarity (0.43); 1:9 kt_ss39 (0.48); 3:5 fig_k1a6_clarity (0.51); 1:10 fig_pu74_handling (0.54); 2:5 kt_mguz (0.55); 2:5 kt_rhfd (0.57)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=367, said 0.04, was 0.00; 0.2–0.4: n=18, said 0.25, was 0.44; 0.4–0.6: n=13, said 0.45, was 0.69; 0.6–0.8: n=14, said 0.66, was 0.86; 0.8–1.0: n=160, said 0.94, was 0.95

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.08, was 0.00; 0.2–0.4: n=7, said 0.28, was 0.00; 0.4–0.6: n=5, said 0.51, was 0.40; 0.6–0.8: n=35, said 0.72, was 0.86; 0.8–1.0: n=101, said 0.89, was 0.99

Calibration, figure clarity (score): 0.0–0.2: n=65, said 0.08, was 0.00; 0.2–0.4: n=13, said 0.27, was 0.00; 0.4–0.6: n=13, said 0.50, was 0.62; 0.6–0.8: n=30, said 0.71, was 0.93; 0.8–1.0: n=96, said 0.89, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 8% / 98% | 13% / 99% | 16% / 99% | 23% / 99% | 42% / 99% |
| Figure handling (choice) | 0% / 87% | 13% / 96% | 42% / 98% | 74% / 100% | 97% / 100% |
| Figure clarity (score) | 6% / 91% | 16% / 98% | 19% / 100% | 81% / 100% | 100% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 38 | 0 | 1 | 0 | 0 |
| simile | 4 | 26 | 1 | 0 | 0 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 7 | 0 | 1 | 12 | 3 |
| distorted | 0 | 0 | 0 | 2 | 29 |

Real items flagged at 0.9: 89. Lowest ten: 3:2 kt_xrq8 (0.08); 1:8 kt_qfud (0.20); 2:5 kt_rhfd (0.20); 3:13 kt_v462 (0.20); 1:9 kt_ss39 (0.25); 1:6 kt_nsxd (0.30); 1:15 kt_mn4k (0.35); 1:15 kt_nvgm (0.35); 2:13 kt_eqaj (0.35); 1:9 kt_nngz (0.40)

