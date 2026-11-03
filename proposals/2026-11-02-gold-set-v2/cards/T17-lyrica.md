# T17 · Lyrica (antiepileptic)

**Status:** verified against sources (112/112 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:40Z – 2026-11-02T18:40Z · questions sha256 `811ecb7bebe1…`

## The trace in one line
Lyrica → RxNorm 593441 (pregabalin (187832)) → package 0071-1018-68 under NDA021446 → DailyMed label 60185c88-ecfd-46f9-adb9-b97c6b00a553 v59 (effective 20200615) → SrLC 04/25/2025 → 3458 FAERS reports name it in 2025 → recall D-0649-2016 → trial NCT02187471.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 593441 (BN); ingredient(s) pregabalin (187832); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0071-1018-68: 90 CAPSULE in 1 BOTTLE (0071-1018-68); labeler Parke-Davis Div of Pfizer Inc; category NDA; application NDA021446 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor UPJOHN; 8 product(s): 001 CAPSULE 25MG; 002 CAPSULE 50MG; 003 CAPSULE 75MG; 004 CAPSULE 100MG; 005 CAPSULE 150MG; 006 CAPSULE 200MG; 007 CAPSULE 225MG; 008 CAPSULE 300MG | Same application number as S2 |
| S4 | DailyMed | In '5.4 Respiratory Depression', what role does 'central nervous system (CNS) depressants' play? | **co_medication_risk_factor** | Quote: "associating LYRICA with serious, life-threatening, or fatal respiratory depression when co-administered with central nervous system (CNS) depressants, including opioids" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 04/25/2025 SUPPL-46, 5.3 Suicidal Behavior and Ideation | Underlined text present in S4 label: **False** |
| S6 | FAERS | What do 2025 reports say? | 3458 reports name LYRICA; 12995 list PREGABALIN (any product) | Top-10 terms checked against S4 label: 7 found, 3 not found |
| S7 | FDA enforcement | Any recall? | D-0649-2016 (Class II, reported status 'Terminated', 20160210): FAILED TABLET/CAPSULE SPECIFICATIONS: Firm is recalling specific lots of pregabalin capsules due to the potential presence of deformed or da… | Record text names package 0071-1018-68: **False** (application-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT02187471 (COMPLETED), EG001 'Pregabalin 150 mg BID': serious AEs 2 of 319 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, DRUG INEFFECTIVE, PYREXIA. Found in label: FATIGUE, PAIN, HEADACHE, NAUSEA, VOMITING, RASH, ARTHRALGIA.
- **Recall:** D-0649-2016 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (04/25/2025) is **not** reflected in the captured DailyMed label.

## Traps this trace shows
- Underlying respiratory impairment in the same sentence is a patient risk factor, a different class. The label also notes more limited evidence without either factor.
- Query scope changes the count: 3458 brand-named vs 12995 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'UPJOHN' (Drugs@FDA) vs labeler 'Parke-Davis Div of Pfizer Inc' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T17.s1_rx_brand` | `8915747c4c7f9127…` | 2026-11-02T18:40:11 |
| `T17.s1_rx_brand_props` | `f85f8d575c23e7d2…` | 2026-11-02T18:40:11 |
| `T17.s1_rx_ingredients` | `b84cf3c28b9a05a1…` | 2026-11-02T18:40:12 |
| `T17.s1_rx_reverse_187832` | `99d27f6373988449…` | 2026-11-02T18:40:12 |
| `T17.s2_ndc` | `3ef47edfb5e91bbd…` | 2026-11-02T18:40:13 |
| `T17.s3_drugsfda` | `ea9117ab81672ec7…` | 2026-11-02T18:40:14 |
| `T17.s4_label` | `a2c497684bac5c56…` | 2026-11-02T18:40:14 |
| `T17.s5_srlc_detail` | `dead65a14d61c33f…` | 2026-11-02T18:40:16 |
| `T17.s5_srlc_search` | `98999fbba2ae42be…` | 2026-11-02T18:40:16 |
| `T17.s6_faers_brand_reactions` | `95619a7fd37cbc02…` | 2026-11-02T18:40:20 |
| `T17.s6_faers_brand_total` | `5c0fd9a19a7b4f6f…` | 2026-11-02T18:40:19 |
| `T17.s6_faers_substance` | `685e47df62f21cea…` | 2026-11-02T18:40:17 |
| `T17.s6_faers_total` | `f510a1bc66b424f3…` | 2026-11-02T18:40:18 |
| `T17.s7_recall_app` | `434255276a2b1935…` | 2026-11-02T18:40:21 |
| `T17.s8_trial` | `df469779b4bb3f72…` | 2026-11-02T18:40:22 |
| `T17.s8_trials_search` | `ac94188861bf7d29…` | 2026-11-02T18:40:21 |
| `T17.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:40:22 |

Full records: [claude/traces/T17.jsonl](../claude/traces/T17.jsonl) · checks: [verification/T17.json](../verification/T17.json) · questions: [shared/questions/T17.json](../shared/questions/T17.json)
