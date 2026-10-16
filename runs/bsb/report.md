# BSB (Berean Standard Bible): Titus checked against the Greek

Target `bsb` (English). Headline threshold: an item is auto-logged as a pass when its pass probability is at least 0.9; anything lower goes to review.

Sources (pinned commits):

- `ugnt`: unfoldingWord/el-x-koine_ugnt @ `fc95b2b8aa` (CC BY-SA 4.0)
- `en_tn`: unfoldingWord/en_tn @ `a0959d790f` (CC BY-SA 4.0)
- `en_twl`: unfoldingWord/en_twl @ `d880052cb7` (CC BY-SA 4.0)
- `en_tw`: unfoldingWord/en_tw @ `6e3900f8c2` (CC BY-SA 4.0)
- `bsb`: Worldview/en_bsb @ `21bca0199a` (Public domain (BSB); alignment CC BY-SA 4.0)

## Speed and cost

Cost and latency are those of the call that produced each answer (re-runs are served from cache). Unanswered = questions with no answer (API error or partial reply); they are left out of every score below.

| run | model version | calls | median latency | total cost | unanswered |
|---|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 453 | 261 ms | $0.0187 | 0 |
| jev-jev-preview | jev-1.14.0 | 453 | 257 ms | $0.0187 | 0 |
| jev-jev-preview+no-approved | jev-1.14.0 | 453 | 258 ms | $0.0181 | 0 |
| jev-jev-preview+no-renderings | jev-1.14.0 | 453 | 260 ms | $0.0185 | 0 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 453 | 2276 ms | $0.1236 | 0 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 19% | 206 | 98% | 100% | 0.975 | 0.066 |
| jev-jev-preview | 182 | 17% | 206 | 99% | 100% | 0.984 | 0.080 |
| jev-jev-preview+no-approved | 182 | 15% | 206 | 99% | 100% | 0.985 | 0.094 |
| jev-jev-preview+no-renderings | 182 | 21% | 206 | 99% | 100% | 0.979 | 0.129 |
| openrouter-claude-haiku-5.5 | 182 | 22% | 206 | 100% | 100% | 0.995 | 0.068 |

By case type: share sent to review / mean pass probability.

| run | kt_omit | kt_wrong | original | verse_swap |
|---|---|---|---|---|
| jev-jev-latest | 96% / 0.34 | 100% / 0.07 | 19% / 0.90 | 100% / 0.13 |
| jev-jev-preview | 98% / 0.31 | 100% / 0.07 | 17% / 0.92 | 100% / 0.11 |
| jev-jev-preview+no-approved | 97% / 0.35 | 100% / 0.08 | 15% / 0.93 | 100% / 0.13 |
| jev-jev-preview+no-renderings | 98% / 0.31 | 99% / 0.28 | 21% / 0.91 | 100% / 0.11 |
| openrouter-claude-haiku-5.5 | 99% / 0.07 | 100% / 0.05 | 22% / 0.87 | 100% / 0.04 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 16% | 54 | 100% | 100% | 0.995 | 0.063 |
| jev-jev-preview | 31 | 13% | 54 | 100% | 100% | 0.993 | 0.042 |
| jev-jev-preview+no-approved | 31 | 16% | 54 | 100% | 100% | 0.993 | 0.043 |
| jev-jev-preview+no-renderings | 31 | 16% | 54 | 98% | 100% | 0.976 | 0.076 |
| openrouter-claude-haiku-5.5 | 31 | 97% | 54 | 100% | 100% | 0.990 | 0.132 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.03 | 19% / 0.94 | 84% / 0.44 | 10% / 0.96 | 13% / 0.95 | 16% / 0.94 | 100% / 0.02 |
| jev-jev-preview | 100% / 0.03 | 19% / 0.94 | 90% / 0.48 | 10% / 0.95 | 13% / 0.94 | 13% / 0.93 | 100% / 0.01 |
| jev-jev-preview+no-approved | 100% / 0.03 | 19% / 0.94 | 90% / 0.48 | 10% / 0.95 | 13% / 0.94 | 16% / 0.93 | 100% / 0.02 |
| jev-jev-preview+no-renderings | 100% / 0.13 | 26% / 0.91 | 77% / 0.59 | 32% / 0.91 | 19% / 0.93 | 16% / 0.92 | 100% / 0.01 |
| openrouter-claude-haiku-5.5 | 100% / 0.11 | 74% / 0.84 | 100% / 0.43 | 55% / 0.87 | 23% / 0.89 | 97% / 0.80 | 100% / 0.06 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest 88%, jev-jev-preview 90%, jev-jev-preview+no-approved 90%, jev-jev-preview+no-renderings 83%, openrouter-claude-haiku-5.5 86%

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 52% | 55 | 100% | 100% | 0.985 | 0.119 |
| jev-jev-preview | 31 | 52% | 55 | 100% | 100% | 0.990 | 0.122 |
| jev-jev-preview+no-approved | 31 | 61% | 55 | 100% | 100% | 0.990 | 0.122 |
| jev-jev-preview+no-renderings | 31 | 65% | 55 | 100% | 100% | 0.968 | 0.112 |
| openrouter-claude-haiku-5.5 | 31 | 74% | 55 | 100% | 100% | 0.987 | 0.113 |

By case type: share sent to review / mean pass probability.

| run | fig_distorted | fig_kept_clear | fig_lost | fig_plain | fig_simile | original | verse_swap |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 100% / 0.02 | 61% / 0.82 | 100% / 0.30 | 32% / 0.89 | 84% / 0.64 | 52% / 0.84 | 100% / 0.03 |
| jev-jev-preview | 100% / 0.04 | 65% / 0.82 | 100% / 0.34 | 35% / 0.90 | 77% / 0.72 | 52% / 0.84 | 100% / 0.02 |
| jev-jev-preview+no-approved | 100% / 0.04 | 65% / 0.82 | 100% / 0.34 | 35% / 0.90 | 77% / 0.72 | 61% / 0.84 | 100% / 0.03 |
| jev-jev-preview+no-renderings | 100% / 0.10 | 71% / 0.78 | 100% / 0.41 | 48% / 0.86 | 90% / 0.69 | 65% / 0.80 | 100% / 0.02 |
| openrouter-claude-haiku-5.5 | 100% / 0.08 | 68% / 0.81 | 100% / 0.36 | 35% / 0.89 | 68% / 0.81 | 74% / 0.80 | 100% / 0.09 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=272, said 0.09, was 0.01; 0.2–0.4: n=76, said 0.26, was 0.03; 0.4–0.6: n=24, said 0.50, was 0.38; 0.6–0.8: n=20, said 0.69, was 0.45; 0.8–1.0: n=167, said 0.96, was 0.95

Calibration, figure handling (choice): 0.0–0.2: n=70, said 0.03, was 0.00; 0.2–0.4: n=9, said 0.30, was 0.00; 0.4–0.6: n=6, said 0.52, was 0.50; 0.6–0.8: n=12, said 0.72, was 0.75; 0.8–1.0: n=120, said 0.97, was 1.00

Calibration, figure clarity (score): 0.0–0.2: n=78, said 0.03, was 0.04; 0.2–0.4: n=15, said 0.30, was 0.47; 0.4–0.6: n=16, said 0.52, was 0.88; 0.6–0.8: n=23, said 0.70, was 0.96; 0.8–1.0: n=85, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 4% / 88% | 10% / 94% | 13% / 96% | 19% / 98% | 29% / 99% |
| Figure handling (choice) | 0% / 91% | 6% / 94% | 10% / 100% | 16% / 100% | 23% / 100% |
| Figure clarity (score) | 6% / 98% | 13% / 98% | 23% / 100% | 52% / 100% | 65% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 37 | 0 | 1 | 1 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 5 | 0 | 0 | 9 | 9 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 55. Lowest ten: 1:9 kt_nngz (0.10); 3:2 kt_xrq8 (0.14); 2:13 kt_eqaj (0.15); 1:10 fig_pu74_clarity (0.24); 2:5 kt_rhfd (0.25); 1:9 kt_ss39 (0.26); 3:5 fig_k1a6_clarity (0.39); 3:13 kt_v462 (0.40); 1:7 kt_rfj7 (0.45); 2:4 kt_m7kb (0.46)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=284, said 0.08, was 0.01; 0.2–0.4: n=68, said 0.27, was 0.01; 0.4–0.6: n=15, said 0.47, was 0.20; 0.6–0.8: n=21, said 0.69, was 0.38; 0.8–1.0: n=171, said 0.96, was 0.98

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.02, was 0.00; 0.2–0.4: n=6, said 0.30, was 0.00; 0.4–0.6: n=11, said 0.52, was 0.45; 0.6–0.8: n=9, said 0.69, was 0.67; 0.8–1.0: n=122, said 0.96, was 0.99

Calibration, figure clarity (score): 0.0–0.2: n=76, said 0.04, was 0.03; 0.2–0.4: n=8, said 0.31, was 0.12; 0.4–0.6: n=20, said 0.49, was 0.75; 0.6–0.8: n=27, said 0.73, was 1.00; 0.8–1.0: n=86, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 3% / 90% | 5% / 95% | 8% / 98% | 17% / 99% | 25% / 99% |
| Figure handling (choice) | 3% / 87% | 6% / 96% | 10% / 98% | 13% / 100% | 26% / 100% |
| Figure clarity (score) | 6% / 98% | 13% / 100% | 29% / 100% | 52% / 100% | 68% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 39 | 0 | 0 | 0 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 1 | 0 | 30 | 0 | 0 |
| lost | 8 | 0 | 2 | 8 | 5 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 51. Lowest ten: 1:9 kt_nngz (0.14); 3:2 kt_xrq8 (0.17); 2:13 kt_eqaj (0.18); 3:13 kt_v462 (0.23); 1:10 fig_pu74_clarity (0.24); 1:9 kt_ss39 (0.41); 2:5 kt_rhfd (0.42); 1:10 fig_pu74_handling (0.44); 3:15 fig_f4vc_clarity (0.48); 3:5 fig_k1a6_clarity (0.54)


## Detail: jev-jev-preview+no-approved

Calibration, key terms (noul): 0.0–0.2: n=260, said 0.09, was 0.00; 0.2–0.4: n=80, said 0.26, was 0.03; 0.4–0.6: n=24, said 0.47, was 0.12; 0.6–0.8: n=22, said 0.73, was 0.41; 0.8–1.0: n=173, said 0.95, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=69, said 0.02, was 0.00; 0.2–0.4: n=6, said 0.30, was 0.00; 0.4–0.6: n=11, said 0.52, was 0.45; 0.6–0.8: n=10, said 0.70, was 0.70; 0.8–1.0: n=121, said 0.96, was 0.99

Calibration, figure clarity (score): 0.0–0.2: n=76, said 0.04, was 0.03; 0.2–0.4: n=8, said 0.31, was 0.12; 0.4–0.6: n=20, said 0.50, was 0.75; 0.6–0.8: n=26, said 0.72, was 1.00; 0.8–1.0: n=87, said 0.92, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 2% / 89% | 4% / 93% | 8% / 97% | 15% / 99% | 29% / 99% |
| Figure handling (choice) | 3% / 87% | 6% / 96% | 13% / 98% | 16% / 100% | 29% / 100% |
| Figure clarity (score) | 3% / 98% | 16% / 100% | 26% / 100% | 61% / 100% | 68% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 39 | 0 | 0 | 0 | 0 |
| simile | 0 | 31 | 0 | 0 | 0 |
| plain | 1 | 0 | 30 | 0 | 0 |
| lost | 8 | 0 | 2 | 8 | 5 |
| distorted | 0 | 0 | 0 | 0 | 31 |

Real items flagged at 0.9: 51. Lowest ten: 1:9 kt_nngz (0.15); 1:10 fig_pu74_clarity (0.25); 3:2 kt_xrq8 (0.25); 2:13 kt_eqaj (0.36); 1:9 kt_ss39 (0.46); 1:10 fig_pu74_handling (0.47); 3:15 fig_f4vc_clarity (0.52); 2:5 kt_mguz (0.56); 3:5 fig_k1a6_clarity (0.56); 2:5 kt_rhfd (0.59)


## Detail: jev-jev-preview+no-renderings

Calibration, key terms (noul): 0.0–0.2: n=233, said 0.10, was 0.00; 0.2–0.4: n=91, said 0.26, was 0.02; 0.4–0.6: n=39, said 0.49, was 0.05; 0.6–0.8: n=36, said 0.70, was 0.58; 0.8–1.0: n=160, said 0.96, was 0.97

Calibration, figure handling (choice): 0.0–0.2: n=62, said 0.04, was 0.00; 0.2–0.4: n=6, said 0.29, was 0.00; 0.4–0.6: n=8, said 0.49, was 0.38; 0.6–0.8: n=20, said 0.70, was 0.50; 0.8–1.0: n=121, said 0.94, was 0.98

Calibration, figure clarity (score): 0.0–0.2: n=70, said 0.05, was 0.03; 0.2–0.4: n=14, said 0.33, was 0.36; 0.4–0.6: n=21, said 0.53, was 0.76; 0.6–0.8: n=38, said 0.72, was 0.89; 0.8–1.0: n=74, said 0.91, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 2% / 83% | 5% / 95% | 14% / 98% | 21% / 99% | 31% / 99% |
| Figure handling (choice) | 3% / 74% | 10% / 83% | 10% / 96% | 16% / 98% | 39% / 100% |
| Figure clarity (score) | 6% / 87% | 23% / 98% | 42% / 100% | 65% / 100% | 71% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 36 | 0 | 2 | 1 | 0 |
| simile | 1 | 28 | 1 | 0 | 1 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 10 | 0 | 1 | 8 | 4 |
| distorted | 1 | 0 | 2 | 0 | 28 |

Real items flagged at 0.9: 63. Lowest ten: 1:9 kt_nngz (0.05); 1:10 fig_pu74_clarity (0.18); 2:13 kt_eqaj (0.31); 3:2 kt_xrq8 (0.37); 1:10 fig_pu74_handling (0.43); 2:8 fig_xy14_clarity (0.44); 2:5 kt_rhfd (0.56); 3:15 fig_f4vc_clarity (0.58); 1:12 fig_y3zb_clarity (0.58); 1:15 kt_mn4k (0.59)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=368, said 0.04, was 0.01; 0.2–0.4: n=13, said 0.28, was 0.54; 0.4–0.6: n=13, said 0.45, was 0.77; 0.6–0.8: n=10, said 0.66, was 0.90; 0.8–1.0: n=155, said 0.94, was 0.99

Calibration, figure handling (choice): 0.0–0.2: n=68, said 0.08, was 0.00; 0.2–0.4: n=7, said 0.29, was 0.00; 0.4–0.6: n=10, said 0.47, was 0.40; 0.6–0.8: n=33, said 0.71, was 0.88; 0.8–1.0: n=99, said 0.89, was 1.00

Calibration, figure clarity (score): 0.0–0.2: n=68, said 0.08, was 0.00; 0.2–0.4: n=16, said 0.30, was 0.31; 0.4–0.6: n=15, said 0.50, was 0.67; 0.6–0.8: n=19, said 0.72, was 0.89; 0.8–1.0: n=99, said 0.89, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|
| Key terms (noul) | 8% / 99% | 12% / 100% | 15% / 100% | 22% / 100% | 40% / 100% |
| Figure handling (choice) | 6% / 87% | 6% / 94% | 35% / 100% | 97% / 100% | 100% / 100% |
| Figure clarity (score) | 6% / 89% | 13% / 100% | 26% / 100% | 74% / 100% | 97% / 100% |

Figure handling, gold label (rows) vs answer (columns):

| gold \ answer | kept_clear | simile | plain | lost | distorted |
|---|---|---|---|---|---|
| kept_clear | 38 | 0 | 1 | 0 | 0 |
| simile | 5 | 24 | 1 | 1 | 0 |
| plain | 2 | 0 | 29 | 0 | 0 |
| lost | 6 | 0 | 0 | 13 | 4 |
| distorted | 0 | 0 | 1 | 1 | 29 |

Real items flagged at 0.9: 93. Lowest ten: 3:2 kt_xrq8 (0.10); 1:9 kt_ss39 (0.15); 1:6 kt_nsxd (0.25); 2:5 kt_rhfd (0.25); 1:9 kt_nngz (0.30); 3:11 kt_sqgk (0.30); 3:13 kt_v462 (0.30); 1:10 fig_pu74_clarity (0.35); 2:13 kt_eqaj (0.35); 2:3 kt_khhe (0.35)

