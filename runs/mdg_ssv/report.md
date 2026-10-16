# Masalit Titus draft: Titus checked against the Greek

Target `mdg_ssv` (Masalit). Headline threshold: an item is auto-logged as a pass when its pass probability is at least 0.9; anything lower goes to review.

Sources (pinned commits):

- `ugnt`: unfoldingWord/el-x-koine_ugnt @ `fc95b2b8aa` (CC BY-SA 4.0)
- `en_tn`: unfoldingWord/en_tn @ `a0959d790f` (CC BY-SA 4.0)
- `en_twl`: unfoldingWord/en_twl @ `d880052cb7` (CC BY-SA 4.0)
- `en_tw`: unfoldingWord/en_tw @ `6e3900f8c2` (CC BY-SA 4.0)
- `mdg_ssv`: Nhial/mdg_ssv_tit_book @ `d9e0dafb84` (CC BY-SA 4.0)

## Speed and cost

Cost and latency are those of the call that produced each answer (re-runs are served from cache). Unanswered = questions with no answer (API error or partial reply); they are left out of every score below.

| run | model version | calls | median latency | total cost | unanswered |
|---|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 92 | 269 ms | $0.0060 | 0 |
| jev-jev-latest+ult | jev-1.13.0 | 92 | 264 ms | $0.0063 | 0 |
| jev-jev-preview | jev-1.14.0 | 92 | 274 ms | $0.0060 | 0 |
| jev-jev-preview+ult | jev-1.14.0 | 92 | 286 ms | $0.0063 | 0 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 92 | 4545 ms | $0.0579 | 0 |
| openrouter-claude-haiku-5.5+ult | anthropic/claude-haiku-5.5 | 92 | 4674 ms | $0.0580 | 0 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 100% | 0 | – | 100% | 0.719 | 0.074 |
| jev-jev-latest+ult | 182 | 99% | 0 | – | 100% | 0.730 | 0.066 |
| jev-jev-preview | 182 | 99% | 0 | – | 100% | 0.676 | 0.064 |
| jev-jev-preview+ult | 182 | 99% | 0 | – | 100% | 0.704 | 0.088 |
| openrouter-claude-haiku-5.5 | 182 | 99% | 0 | – | 100% | 0.640 | 0.047 |
| openrouter-claude-haiku-5.5+ult | 182 | 100% | 0 | – | 100% | 0.634 | 0.057 |

By case type: share sent to review / mean pass probability.

| run | original | verse_swap |
|---|---|---|
| jev-jev-latest | 100% / 0.51 | 100% / 0.42 |
| jev-jev-latest+ult | 99% / 0.57 | 100% / 0.48 |
| jev-jev-preview | 99% / 0.57 | 100% / 0.50 |
| jev-jev-preview+ult | 99% / 0.62 | 100% / 0.54 |
| openrouter-claude-haiku-5.5 | 99% / 0.54 | 100% / 0.47 |
| openrouter-claude-haiku-5.5+ult | 100% / 0.54 | 100% / 0.47 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 100% | 0 | – | 100% | 0.750 | 0.160 |
| jev-jev-latest+ult | 31 | 100% | 0 | – | 100% | 0.750 | 0.135 |
| jev-jev-preview | 31 | 100% | 0 | – | 100% | 0.749 | 0.142 |
| jev-jev-preview+ult | 31 | 100% | 0 | – | 100% | 0.722 | 0.083 |
| openrouter-claude-haiku-5.5 | 31 | 100% | 0 | – | 100% | 0.554 | 0.190 |
| openrouter-claude-haiku-5.5+ult | 31 | 100% | 0 | – | 100% | 0.632 | 0.131 |

By case type: share sent to review / mean pass probability.

| run | original | verse_swap |
|---|---|---|
| jev-jev-latest | 100% / 0.48 | 100% / 0.35 |
| jev-jev-latest+ult | 100% / 0.51 | 100% / 0.38 |
| jev-jev-preview | 100% / 0.56 | 100% / 0.46 |
| jev-jev-preview+ult | 100% / 0.60 | 100% / 0.50 |
| openrouter-claude-haiku-5.5 | 100% / 0.68 | 100% / 0.66 |
| openrouter-claude-haiku-5.5+ult | 100% / 0.67 | 100% / 0.59 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest –, jev-jev-latest+ult –, jev-jev-preview –, jev-jev-preview+ult –, openrouter-claude-haiku-5.5 –, openrouter-claude-haiku-5.5+ult –

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 100% | 0 | – | 100% | 0.711 | 0.290 |
| jev-jev-latest+ult | 31 | 100% | 0 | – | 100% | 0.725 | 0.228 |
| jev-jev-preview | 31 | 100% | 0 | – | 100% | 0.710 | 0.162 |
| jev-jev-preview+ult | 31 | 100% | 0 | – | 100% | 0.677 | 0.106 |
| openrouter-claude-haiku-5.5 | 31 | 100% | 0 | – | 100% | 0.662 | 0.121 |
| openrouter-claude-haiku-5.5+ult | 31 | 100% | 0 | – | 100% | 0.666 | 0.074 |

By case type: share sent to review / mean pass probability.

| run | original | verse_swap |
|---|---|---|
| jev-jev-latest | 100% / 0.27 | 100% / 0.19 |
| jev-jev-latest+ult | 100% / 0.32 | 100% / 0.24 |
| jev-jev-preview | 100% / 0.40 | 100% / 0.34 |
| jev-jev-preview+ult | 100% / 0.43 | 100% / 0.37 |
| openrouter-claude-haiku-5.5 | 100% / 0.63 | 100% / 0.56 |
| openrouter-claude-haiku-5.5+ult | 100% / 0.62 | 100% / 0.53 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=7, said 0.13, was 0.14; 0.2–0.4: n=79, said 0.33, was 0.28; 0.4–0.6: n=223, said 0.48, was 0.54; 0.6–0.8: n=39, said 0.65, was 0.87; 0.8–1.0: n=5, said 0.83, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=5, said 0.08, was 0.20; 0.2–0.4: n=18, said 0.30, was 0.22; 0.4–0.6: n=32, said 0.48, was 0.66; 0.6–0.8: n=7, said 0.65, was 0.71

Calibration, figure clarity (score): 0.0–0.2: n=24, said 0.12, was 0.29; 0.2–0.4: n=33, said 0.27, was 0.64; 0.4–0.6: n=5, said 0.47, was 0.60

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 244. Lowest ten: 3:5 fig_k1a6_clarity (0.08); 1:9 kt_nngz (0.12); 3:3 fig_qt8f_clarity (0.12); 1:10 fig_pu74_clarity (0.13); 1:13 fig_je3r_clarity (0.14); 3:15 fig_f4vc_clarity (0.15); 2:11 fig_n08x_clarity (0.17); 1:10 fig_pu74_handling (0.19); 2:14 fig_gxe7_clarity (0.19); 1:3 fig_swi9_clarity (0.20)


## Detail: jev-jev-latest+ult

Calibration, key terms (noul): 0.0–0.2: n=4, said 0.14, was 0.25; 0.2–0.4: n=32, said 0.33, was 0.16; 0.4–0.6: n=236, said 0.51, was 0.48; 0.6–0.8: n=74, said 0.65, was 0.74; 0.8–1.0: n=7, said 0.83, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=4, said 0.10, was 0.00; 0.2–0.4: n=17, said 0.31, was 0.24; 0.4–0.6: n=29, said 0.48, was 0.66; 0.6–0.8: n=12, said 0.66, was 0.67

Calibration, figure clarity (score): 0.0–0.2: n=14, said 0.14, was 0.36; 0.2–0.4: n=43, said 0.30, was 0.53; 0.4–0.6: n=5, said 0.50, was 0.60

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 3:5 fig_k1a6_clarity (0.12); 1:10 fig_pu74_clarity (0.15); 3:3 fig_qt8f_clarity (0.16); 1:9 kt_nngz (0.17); 1:13 fig_je3r_clarity (0.18); 3:15 fig_f4vc_clarity (0.19); 1:13 fig_je3r_handling (0.21); 2:11 fig_n08x_clarity (0.22); 1:10 fig_pu74_handling (0.24); 3:7 fig_q1cm_clarity (0.24)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=5, said 0.13, was 0.20; 0.2–0.4: n=27, said 0.32, was 0.19; 0.4–0.6: n=229, said 0.52, was 0.50; 0.6–0.8: n=85, said 0.65, was 0.64; 0.8–1.0: n=7, said 0.85, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=4, said 0.12, was 0.00; 0.2–0.4: n=8, said 0.33, was 0.50; 0.4–0.6: n=35, said 0.55, was 0.43; 0.6–0.8: n=15, said 0.64, was 0.80

Calibration, figure clarity (score): 0.0–0.2: n=5, said 0.11, was 0.20; 0.2–0.4: n=26, said 0.33, was 0.35; 0.4–0.6: n=31, said 0.44, was 0.68

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 1:9 kt_nngz (0.14); 1:10 fig_pu74_clarity (0.15); 1:13 fig_je3r_handling (0.21); 1:13 fig_je3r_clarity (0.23); 3:5 fig_k1a6_clarity (0.24); 3:6 kt_h9fu (0.25); 1:10 fig_pu74_handling (0.28); 3:6 fig_fby9_clarity (0.28); 1:11 kt_bjyb (0.31); 3:15 fig_f4vc_clarity (0.31)


## Detail: jev-jev-preview+ult

Calibration, key terms (noul): 0.0–0.2: n=4, said 0.15, was 0.25; 0.2–0.4: n=14, said 0.34, was 0.14; 0.4–0.6: n=159, said 0.53, was 0.41; 0.6–0.8: n=169, said 0.66, was 0.63; 0.8–1.0: n=7, said 0.85, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=2, said 0.10, was 0.00; 0.2–0.4: n=8, said 0.31, was 0.25; 0.4–0.6: n=17, said 0.52, was 0.41; 0.6–0.8: n=35, said 0.64, was 0.63

Calibration, figure clarity (score): 0.0–0.2: n=4, said 0.13, was 0.25; 0.2–0.4: n=21, said 0.34, was 0.38; 0.4–0.6: n=37, said 0.46, was 0.59

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 1:9 kt_nngz (0.17); 1:10 fig_pu74_clarity (0.19); 1:13 fig_je3r_handling (0.21); 1:13 fig_je3r_clarity (0.22); 3:5 fig_k1a6_clarity (0.29); 1:10 fig_pu74_handling (0.32); 1:14 kt_we3r (0.33); 2:12 fig_qy8k_clarity (0.34); 3:6 fig_fby9_clarity (0.36); 1:13 kt_s5qd (0.37)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.0–0.2: n=2, said 0.14, was 0.00; 0.2–0.4: n=31, said 0.31, was 0.16; 0.4–0.6: n=227, said 0.47, was 0.51; 0.6–0.8: n=84, said 0.64, was 0.63; 0.8–1.0: n=9, said 0.84, was 1.00

Calibration, figure handling (choice): 0.4–0.6: n=11, said 0.50, was 0.45; 0.6–0.8: n=44, said 0.69, was 0.50; 0.8–1.0: n=7, said 0.82, was 0.57

Calibration, figure clarity (score): 0.2–0.4: n=1, said 0.35, was 1.00; 0.4–0.6: n=24, said 0.51, was 0.38; 0.6–0.8: n=36, said 0.65, was 0.56; 0.8–1.0: n=1, said 0.85, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 1:16 kt_frhh (0.30); 1:13 fig_je3r_clarity (0.35); 1:13 kt_dsy8 (0.35); 2:13 kt_eqaj (0.35); 2:3 kt_jfdu (0.35); 3:3 kt_p9ch (0.35); 1:1 kt_f44k (0.40); 1:1 kt_pmq8 (0.40); 1:10 kt_k8ta (0.40); 1:10 kt_ucvu (0.40)


## Detail: openrouter-claude-haiku-5.5+ult

Calibration, key terms (noul): 0.0–0.2: n=4, said 0.07, was 0.00; 0.2–0.4: n=25, said 0.32, was 0.20; 0.4–0.6: n=224, said 0.47, was 0.51; 0.6–0.8: n=89, said 0.63, was 0.58; 0.8–1.0: n=11, said 0.82, was 1.00

Calibration, figure handling (choice): 0.2–0.4: n=3, said 0.23, was 0.00; 0.4–0.6: n=18, said 0.50, was 0.44; 0.6–0.8: n=33, said 0.69, was 0.55; 0.8–1.0: n=8, said 0.81, was 0.62

Calibration, figure clarity (score): 0.2–0.4: n=3, said 0.25, was 0.00; 0.4–0.6: n=25, said 0.48, was 0.40; 0.6–0.8: n=32, said 0.66, was 0.62; 0.8–1.0: n=2, said 0.82, was 0.50

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 244. Lowest ten: 1:16 kt_rjjt (0.35); 1:9 kt_x67x (0.35); 2:13 kt_eqaj (0.35); 2:15 kt_rvsu (0.35); 3:2 kt_sq5t (0.35); 1:1 kt_qktr (0.40); 1:1 kt_tr4u (0.40); 1:10 kt_p8yj (0.40); 1:11 kt_bjyb (0.40); 1:11 kt_wjg8 (0.40)

