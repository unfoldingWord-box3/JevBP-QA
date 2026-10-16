# Masalit Titus draft: Titus checked against the Greek

Target `mdg_ssv` (Masalit). Headline threshold: an item is auto-logged as a pass when its pass probability is at least 0.9; anything lower goes to review.

Sources (pinned commits):

- `ugnt`: unfoldingWord/el-x-koine_ugnt @ `fc95b2b8aa` (CC BY-SA 4.0)
- `en_tn`: unfoldingWord/en_tn @ `a0959d790f` (CC BY-SA 4.0)
- `en_twl`: unfoldingWord/en_twl @ `d880052cb7` (CC BY-SA 4.0)
- `en_tw`: unfoldingWord/en_tw @ `6e3900f8c2` (CC BY-SA 4.0)
- `mdg_ssv`: Nhial/mdg_ssv_tit_book @ `d9e0dafb84` (CC BY-SA 4.0)

## Speed and cost

| run | model version | calls | median latency | total cost |
|---|---|---|---|---|
| jev-jev-latest | jev-1.13.0 | 92 | 271 ms | $0.0060 |
| jev-jev-latest+ult | jev-1.13.0 | 92 | 262 ms | $0.0063 |
| jev-jev-preview | jev-1.14.0 | 92 | 257 ms | $0.0060 |
| jev-jev-preview+ult | jev-1.14.0 | 92 | 262 ms | $0.0063 |
| openrouter-claude-haiku-5.5 | anthropic/claude-haiku-5.5 | 92 | 4537 ms | $0.0573 |
| openrouter-claude-haiku-5.5+ult | anthropic/claude-haiku-5.5 | 92 | 4666 ms | $0.0585 |

## Key terms (noul)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 182 | 100% | 0 | – | 100% | 0.699 | 0.053 |
| jev-jev-latest+ult | 182 | 99% | 0 | – | 100% | 0.729 | 0.055 |
| jev-jev-preview | 182 | 99% | 0 | – | 100% | 0.678 | 0.059 |
| jev-jev-preview+ult | 182 | 99% | 0 | – | 100% | 0.682 | 0.092 |
| openrouter-claude-haiku-5.5 | 182 | 99% | 0 | – | 100% | 0.640 | 0.041 |
| openrouter-claude-haiku-5.5+ult | 182 | 100% | 0 | – | 100% | 0.614 | 0.064 |

By case type: share sent to review / mean pass probability.

| run | original | verse_swap |
|---|---|---|
| jev-jev-latest | 100% / 0.51 | 100% / 0.42 |
| jev-jev-latest+ult | 99% / 0.57 | 100% / 0.48 |
| jev-jev-preview | 99% / 0.57 | 100% / 0.50 |
| jev-jev-preview+ult | 99% / 0.62 | 100% / 0.55 |
| openrouter-claude-haiku-5.5 | 99% / 0.54 | 100% / 0.48 |
| openrouter-claude-haiku-5.5+ult | 100% / 0.54 | 100% / 0.47 |

## Figure handling (choice)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 100% | 0 | – | 100% | 0.752 | 0.180 |
| jev-jev-latest+ult | 31 | 100% | 0 | – | 100% | 0.764 | 0.174 |
| jev-jev-preview | 31 | 100% | 0 | – | 100% | 0.729 | 0.117 |
| jev-jev-preview+ult | 31 | 100% | 0 | – | 100% | 0.722 | 0.089 |
| openrouter-claude-haiku-5.5 | 31 | 100% | 0 | – | 100% | 0.517 | 0.178 |
| openrouter-claude-haiku-5.5+ult | 31 | 100% | 0 | – | 100% | 0.574 | 0.160 |

By case type: share sent to review / mean pass probability.

| run | original | verse_swap |
|---|---|---|
| jev-jev-latest | 100% / 0.47 | 100% / 0.34 |
| jev-jev-latest+ult | 100% / 0.52 | 100% / 0.38 |
| jev-jev-preview | 100% / 0.57 | 100% / 0.47 |
| jev-jev-preview+ult | 100% / 0.60 | 100% / 0.49 |
| openrouter-claude-haiku-5.5 | 100% / 0.68 | 100% / 0.67 |
| openrouter-claude-haiku-5.5+ult | 100% / 0.67 | 100% / 0.62 |

Exact-label accuracy on rewritten figures (kept / simile / plain / lost / distorted): jev-jev-latest –, jev-jev-latest+ult –, jev-jev-preview –, jev-jev-preview+ult –, openrouter-claude-haiku-5.5 –, openrouter-claude-haiku-5.5+ult –

## Figure clarity (score)

Real flagged = share of the published translation's items sent to review (lower is better if the text is good). Faults caught = share of seeded item errors sent to review (higher is better). Swaps caught = share of items sent to review when the verse text is swapped for a different verse (a floor test).

| run | real items | real flagged | seeded faults | faults caught | swaps caught | AUROC | calibration error (ECE) |
|---|---|---|---|---|---|---|---|
| jev-jev-latest | 31 | 100% | 0 | – | 100% | 0.729 | 0.276 |
| jev-jev-latest+ult | 31 | 100% | 0 | – | 100% | 0.721 | 0.234 |
| jev-jev-preview | 31 | 100% | 0 | – | 100% | 0.697 | 0.143 |
| jev-jev-preview+ult | 31 | 100% | 0 | – | 100% | 0.684 | 0.117 |
| openrouter-claude-haiku-5.5 | 31 | 100% | 0 | – | 100% | 0.573 | 0.119 |
| openrouter-claude-haiku-5.5+ult | 31 | 100% | 0 | – | 100% | 0.527 | 0.143 |

By case type: share sent to review / mean pass probability.

| run | original | verse_swap |
|---|---|---|
| jev-jev-latest | 100% / 0.26 | 100% / 0.18 |
| jev-jev-latest+ult | 100% / 0.31 | 100% / 0.24 |
| jev-jev-preview | 100% / 0.40 | 100% / 0.34 |
| jev-jev-preview+ult | 100% / 0.43 | 100% / 0.37 |
| openrouter-claude-haiku-5.5 | 100% / 0.62 | 100% / 0.57 |
| openrouter-claude-haiku-5.5+ult | 100% / 0.60 | 100% / 0.58 |

## Detail: jev-jev-latest

Calibration, key terms (noul): 0.0–0.2: n=9, said 0.14, was 0.22; 0.2–0.4: n=84, said 0.33, was 0.30; 0.4–0.6: n=227, said 0.48, was 0.52; 0.6–0.8: n=39, said 0.65, was 0.85; 0.8–1.0: n=5, said 0.83, was 1.00

Calibration, figure handling (choice): 0.0–0.2: n=5, said 0.08, was 0.20; 0.2–0.4: n=22, said 0.30, was 0.23; 0.4–0.6: n=29, said 0.49, was 0.72; 0.6–0.8: n=6, said 0.66, was 0.67

Calibration, figure clarity (score): 0.0–0.2: n=25, said 0.12, was 0.32; 0.2–0.4: n=32, said 0.27, was 0.62; 0.4–0.6: n=5, said 0.46, was 0.60

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 244. Lowest ten: 3:5 fig_k1a6_clarity (0.08); 1:13 fig_je3r_clarity (0.09); 3:3 fig_qt8f_clarity (0.10); 1:9 kt_nngz (0.12); 1:10 fig_pu74_clarity (0.15); 2:11 fig_n08x_clarity (0.15); 3:7 fig_q1cm_clarity (0.15); 2:14 fig_gxe7_clarity (0.16); 3:15 fig_f4vc_clarity (0.16); 1:13 fig_je3r_handling (0.17)


## Detail: jev-jev-latest+ult

Calibration, key terms (noul): 0.0–0.2: n=3, said 0.13, was 0.33; 0.2–0.4: n=40, said 0.33, was 0.15; 0.4–0.6: n=235, said 0.51, was 0.48; 0.6–0.8: n=78, said 0.65, was 0.71; 0.8–1.0: n=8, said 0.83, was 0.88

Calibration, figure handling (choice): 0.0–0.2: n=5, said 0.11, was 0.20; 0.2–0.4: n=18, said 0.33, was 0.22; 0.4–0.6: n=28, said 0.49, was 0.68; 0.6–0.8: n=11, said 0.67, was 0.64

Calibration, figure clarity (score): 0.0–0.2: n=17, said 0.14, was 0.29; 0.2–0.4: n=39, said 0.30, was 0.59; 0.4–0.6: n=6, said 0.48, was 0.50

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 3:5 fig_k1a6_clarity (0.13); 1:13 fig_je3r_clarity (0.15); 1:9 kt_nngz (0.16); 1:10 fig_pu74_clarity (0.18); 1:13 fig_je3r_handling (0.18); 3:15 fig_f4vc_clarity (0.18); 3:3 fig_qt8f_clarity (0.19); 1:10 fig_pu74_handling (0.23); 2:11 fig_n08x_clarity (0.23); 3:7 fig_q1cm_clarity (0.24)


## Detail: jev-jev-preview

Calibration, key terms (noul): 0.0–0.2: n=4, said 0.12, was 0.25; 0.2–0.4: n=27, said 0.32, was 0.19; 0.4–0.6: n=232, said 0.51, was 0.47; 0.6–0.8: n=93, said 0.65, was 0.63; 0.8–1.0: n=8, said 0.85, was 0.88

Calibration, figure handling (choice): 0.0–0.2: n=4, said 0.14, was 0.00; 0.2–0.4: n=6, said 0.33, was 0.50; 0.4–0.6: n=33, said 0.54, was 0.42; 0.6–0.8: n=19, said 0.63, was 0.74

Calibration, figure clarity (score): 0.0–0.2: n=4, said 0.12, was 0.25; 0.2–0.4: n=31, said 0.33, was 0.35; 0.4–0.6: n=27, said 0.45, was 0.70

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 1:9 kt_nngz (0.11); 1:10 fig_pu74_clarity (0.16); 1:13 fig_je3r_clarity (0.24); 1:13 fig_je3r_handling (0.25); 3:6 kt_h9fu (0.25); 3:5 fig_k1a6_clarity (0.28); 1:14 kt_we3r (0.29); 3:6 fig_fby9_clarity (0.29); 1:10 fig_pu74_handling (0.30); 1:11 kt_bjyb (0.31)


## Detail: jev-jev-preview+ult

Calibration, key terms (noul): 0.0–0.2: n=4, said 0.14, was 0.25; 0.2–0.4: n=17, said 0.35, was 0.18; 0.4–0.6: n=173, said 0.53, was 0.40; 0.6–0.8: n=162, said 0.66, was 0.63; 0.8–1.0: n=8, said 0.86, was 0.88

Calibration, figure handling (choice): 0.0–0.2: n=3, said 0.13, was 0.00; 0.2–0.4: n=7, said 0.32, was 0.29; 0.4–0.6: n=19, said 0.52, was 0.37; 0.6–0.8: n=33, said 0.64, was 0.67

Calibration, figure clarity (score): 0.0–0.2: n=3, said 0.12, was 0.00; 0.2–0.4: n=22, said 0.33, was 0.41; 0.4–0.6: n=36, said 0.46, was 0.58; 0.6–0.8: n=1, said 0.62, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 1:9 kt_nngz (0.13); 1:10 fig_pu74_clarity (0.20); 1:13 fig_je3r_clarity (0.21); 1:13 fig_je3r_handling (0.22); 3:5 fig_k1a6_clarity (0.29); 1:10 fig_pu74_handling (0.31); 1:14 kt_we3r (0.35); 3:15 fig_f4vc_clarity (0.35); 1:13 kt_s5qd (0.36); 3:3 fig_qt8f_clarity (0.36)


## Detail: openrouter-claude-haiku-5.5

Calibration, key terms (noul): 0.2–0.4: n=24, said 0.33, was 0.17; 0.4–0.6: n=249, said 0.47, was 0.47; 0.6–0.8: n=75, said 0.63, was 0.60; 0.8–1.0: n=16, said 0.83, was 1.00

Calibration, figure handling (choice): 0.4–0.6: n=12, said 0.53, was 0.50; 0.6–0.8: n=46, said 0.70, was 0.48; 0.8–1.0: n=4, said 0.82, was 0.75

Calibration, figure clarity (score): 0.2–0.4: n=1, said 0.35, was 0.00; 0.4–0.6: n=21, said 0.49, was 0.43; 0.6–0.8: n=38, said 0.65, was 0.53; 0.8–1.0: n=2, said 0.80, was 1.00

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 243. Lowest ten: 1:9 kt_nngz (0.30); 1:1 kt_qktr (0.35); 3:3 kt_p9ch (0.35); 3:5 kt_sqsf (0.35); 1:1 kt_f44k (0.40); 1:1 kt_pmq8 (0.40); 1:10 kt_k8ta (0.40); 1:10 kt_p8yj (0.40); 1:15 kt_nvgm (0.40); 1:16 kt_frhh (0.40)


## Detail: openrouter-claude-haiku-5.5+ult

Calibration, key terms (noul): 0.0–0.2: n=4, said 0.06, was 0.00; 0.2–0.4: n=29, said 0.32, was 0.24; 0.4–0.6: n=229, said 0.47, was 0.49; 0.6–0.8: n=85, said 0.63, was 0.54; 0.8–1.0: n=17, said 0.81, was 0.94

Calibration, figure handling (choice): 0.2–0.4: n=6, said 0.31, was 0.33; 0.4–0.6: n=10, said 0.53, was 0.50; 0.6–0.8: n=39, said 0.69, was 0.51; 0.8–1.0: n=7, said 0.83, was 0.57

Calibration, figure clarity (score): 0.2–0.4: n=3, said 0.24, was 0.00; 0.4–0.6: n=22, said 0.48, was 0.55; 0.6–0.8: n=37, said 0.68, was 0.51

Threshold sweep (real items flagged / seeded faults caught, verse swaps excluded):

| question | t=0.5 | t=0.7 | t=0.8 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|

Real items flagged at 0.9: 244. Lowest ten: 2:13 kt_bpbw (0.25); 1:9 kt_nngz (0.30); 2:10 kt_pynk (0.30); 2:10 kt_rqa2 (0.35); 2:12 kt_wyfa (0.35); 2:13 kt_ctfv (0.35); 2:3 kt_khhe (0.35); 1:12 fig_xyz1_handling (0.35); 1:13 fig_je3r_handling (0.35); 1:1 kt_qktr (0.40)

