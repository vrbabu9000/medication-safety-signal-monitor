# T20 · Zithromax (macrolide)

**Status:** verified against sources (117/117 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:40Z – 2026-11-02T18:41Z · questions sha256 `d5eecdfa9c41…`

## The trace in one line
Zithromax → RxNorm 196474 (azithromycin (18631)) → package 0069-3120-19 under NDA050710 → DailyMed label db52b91e-79f7-4cc1-9564-f2eee8e31c45 v49 (effective 20260724) → SrLC 07/13/2026 → 408 FAERS reports name it in 2025 → recall D-0997-2022 → trial NCT02047981.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 196474 (BN); ingredient(s) azithromycin (18631); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0069-3120-19: 1 BOTTLE in 1 CARTON (0069-3120-19)  / 15 mL in 1 BOTTLE; labeler Pfizer Laboratories Div Pfizer Inc; category NDA; application NDA050710 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor PFIZER; 2 product(s): 001 FOR SUSPENSION EQ 100MG BASE/5ML; 002 FOR SUSPENSION EQ 200MG BASE/5ML | Same application number as S2 |
| S4 | DailyMed | In '5.3 Infantile Hypertrophic Pyloric Stenosis (IHPS)', what role does 'vomiting or irritability with feeding' play? | **symptom_of_other_condition** | Quote: "Direct parents and caregivers to contact their physician if vomiting or irritability with feeding occurs." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 07/13/2026 SUPPL-54, 6.1 Clinical Trials Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 408 reports name ZITHROMAX; 545 list AZITHROMYCIN DIHYDRATE (any product) | Top-10 terms checked against S4 label: 8 found, 2 not found |
| S7 | FDA enforcement | Any recall? | D-0997-2022 (Class II, reported status 'Terminated', 20220615): cGMP deviations: Temperature abuse | Record text names package 0069-3120-19: **False** (ingredient-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT02047981 (COMPLETED), EG000 'Biannual Mass Oral Azithromycin': serious AEs 3273 of 97047 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, DYSPNOEA. Found in label: FATIGUE, COUGH, HEADACHE, PNEUMONIA, DIARRHOEA, NAUSEA, ASTHENIA, PRURITUS.
- **Recall:** D-0997-2022 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (07/13/2026) is reflected in the captured DailyMed label.

## Traps this trace shows
- Debatable like G04-type cases: IHPS is the azithromycin-associated event, so a reviewer may class its signs as reactions.
- Query scope changes the count: 408 brand-named vs 545 substance-level reports.
- Sponsor 'PFIZER' (Drugs@FDA) vs labeler 'Pfizer Laboratories Div Pfizer Inc' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T20.s1_rx_brand` | `e49cfb04c2b68529…` | 2026-11-02T18:40:48 |
| `T20.s1_rx_brand_props` | `0d12057f6ea1090f…` | 2026-11-02T18:40:48 |
| `T20.s1_rx_ingredients` | `794403580a1038e9…` | 2026-11-02T18:40:49 |
| `T20.s1_rx_reverse_18631` | `d2e3c258ef5a0203…` | 2026-11-02T18:40:49 |
| `T20.s2_ndc` | `3042ee69620b09ab…` | 2026-11-02T18:40:50 |
| `T20.s3_drugsfda` | `1c6dec5da7c223ca…` | 2026-11-02T18:40:51 |
| `T20.s4_label` | `29cbeff145cf9791…` | 2026-11-02T18:40:51 |
| `T20.s5_srlc_detail` | `1ea710816330c4fb…` | 2026-11-02T18:40:54 |
| `T20.s5_srlc_search` | `190b960a5151e86e…` | 2026-11-02T18:40:53 |
| `T20.s6_faers_brand_reactions` | `ce5e304404c2f9be…` | 2026-11-02T18:40:57 |
| `T20.s6_faers_brand_total` | `271f3a8f7010fb53…` | 2026-11-02T18:40:56 |
| `T20.s6_faers_substance` | `dc669b1f2ac8c522…` | 2026-11-02T18:40:55 |
| `T20.s6_faers_total` | `44a416a4c859f528…` | 2026-11-02T18:40:55 |
| `T20.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:40:58 |
| `T20.s7_recall_ingredient` | `22bc76f42e34397f…` | 2026-11-02T18:40:59 |
| `T20.s8_trial` | `eeb84e1f9e342d7d…` | 2026-11-02T18:41:00 |
| `T20.s8_trials_search` | `66184438165910e5…` | 2026-11-02T18:41:00 |
| `T20.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:41:00 |

Full records: [claude/traces/T20.jsonl](../claude/traces/T20.jsonl) · checks: [verification/T20.json](../verification/T20.json) · questions: [shared/questions/T20.json](../shared/questions/T20.json)
