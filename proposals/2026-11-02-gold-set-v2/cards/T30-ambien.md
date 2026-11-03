# T30 · Ambien (hypnotic)

**Status:** verified against sources (117/117 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:42Z – 2026-11-02T18:43Z · questions sha256 `8889c370938e…`

## The trace in one line
Ambien → RxNorm 131725 (zolpidem (39993)) → package 0024-5401-31 under NDA019908 → DailyMed label c36cadf4-65a4-4466-b409-c82020b42452 v26 (effective 20250415) → SrLC 02/23/2022 → 1268 FAERS reports name it in 2025 → recall D-0272-2024 → trial NCT02783729.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 131725 (BN); ingredient(s) zolpidem (39993); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0024-5401-31: 100 TABLET, FILM COATED in 1 BOTTLE (0024-5401-31); labeler Sanofi-Aventis U.S. LLC; category NDA; application NDA019908 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor COSETTE; 2 product(s): 001 TABLET 5MG; 002 TABLET 10MG | Same application number as S2 |
| S4 | DailyMed | In '4 CONTRAINDICATIONS', what role does 'patients who have experienced complex sleep behaviors after taking AMBIEN' play? | **contraindicated_population** | Quote: "AMBIEN is contraindicated in patients who have experienced complex sleep behaviors after taking AMBIEN" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 02/23/2022 SUPPL-40, 5.7 Respiratory Depression | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1268 reports name AMBIEN; 5046 list ZOLPIDEM TARTRATE (any product) | Top-10 terms checked against S4 label: 8 found, 2 not found |
| S7 | FDA enforcement | Any recall? | D-0272-2024 (Class II, reported status 'Completed', 20240131): CGMP Deviations: Microbial contamination was reported in stagnant water in the duct of the manufacturing equipment. | Record text names package 0024-5401-31: **False** (ingredient-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT02783729 (COMPLETED), EG001 'Zolpidem Tartrate Extended Release 6.25 mg': serious AEs 4 of 263 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DRUG INEFFECTIVE, OFF LABEL USE. Found in label: NAUSEA, FATIGUE, DIARRHOEA, HEADACHE, DIZZINESS, INSOMNIA, DYSPNOEA, PAIN.
- **Recall:** D-0272-2024 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (02/23/2022) is reflected in the captured DailyMed label.

## Traps this trace shows
- Context trap: complex sleep behaviors are themselves a reaction (boxed warning); here the target is the population defined by a past reaction.
- Query scope changes the count: 1268 brand-named vs 5046 substance-level reports.
- Sponsor 'COSETTE' (Drugs@FDA) vs labeler 'Sanofi-Aventis U.S. LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T30.s1_rx_brand` | `b2d0178d42714b61…` | 2026-11-02T18:42:53 |
| `T30.s1_rx_brand_props` | `33f1ceb34d1d6578…` | 2026-11-02T18:42:53 |
| `T30.s1_rx_ingredients` | `23ccf16bbff2f127…` | 2026-11-02T18:42:54 |
| `T30.s1_rx_reverse_39993` | `47361fa546aa95c9…` | 2026-11-02T18:42:54 |
| `T30.s2_ndc` | `48cb0120e9fec315…` | 2026-11-02T18:42:55 |
| `T30.s3_drugsfda` | `970b7c780e489155…` | 2026-11-02T18:42:56 |
| `T30.s4_label` | `9ff6dc4e5fbf3dae…` | 2026-11-02T18:42:56 |
| `T30.s5_srlc_detail` | `89f4db973e6fdb51…` | 2026-11-02T18:42:58 |
| `T30.s5_srlc_search` | `11a4f41995089e97…` | 2026-11-02T18:42:57 |
| `T30.s6_faers_brand_reactions` | `3caede40504a896f…` | 2026-11-02T18:43:01 |
| `T30.s6_faers_brand_total` | `3969e5c68ee4465d…` | 2026-11-02T18:43:01 |
| `T30.s6_faers_substance` | `b34e746092fec1dc…` | 2026-11-02T18:42:59 |
| `T30.s6_faers_total` | `0e7e84d3117aa8af…` | 2026-11-02T18:43:00 |
| `T30.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:43:02 |
| `T30.s7_recall_ingredient` | `8ee8312966c41902…` | 2026-11-02T18:43:03 |
| `T30.s8_trial` | `ac377872470f4d97…` | 2026-11-02T18:43:04 |
| `T30.s8_trials_search` | `2a87ee4051a6a710…` | 2026-11-02T18:43:03 |
| `T30.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:43:04 |

Full records: [claude/traces/T30.jsonl](../claude/traces/T30.jsonl) · checks: [verification/T30.json](../verification/T30.json) · questions: [shared/questions/T30.json](../shared/questions/T30.json)
