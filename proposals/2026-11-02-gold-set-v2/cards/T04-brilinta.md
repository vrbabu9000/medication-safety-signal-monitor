# T04 · Brilinta (antiplatelet)

**Status:** verified against sources (110/110 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:37Z – 2026-11-02T18:37Z · questions sha256 `7a09958f4f8a…`

## The trace in one line
Brilinta → RxNorm 1116636 (ticagrelor (1116632)) → package 0186-0776-60 under NDA022433 → DailyMed label f7b3f443-e83d-4bf2-0e96-023448fed9a8 v56 (effective 20260507) → SrLC 11/05/2020 → 539 FAERS reports name it in 2025 → recall D-0433-2021 → trial NCT01225562.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 1116636 (BN); ingredient(s) ticagrelor (1116632); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0186-0776-60: 60 TABLET in 1 BOTTLE (0186-0776-60); labeler AstraZeneca Pharmaceuticals LP; category NDA; application NDA022433 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ASTRAZENECA; 2 product(s): 001 TABLET 90MG; 002 TABLET 60MG | Same application number as S2 |
| S4 | DailyMed | In '5.3 Dyspnea', what role does 'dyspnea' play? | **reaction_or_warning** | Quote: "of patients treated with BRILINTA developed dyspnea" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 11/05/2020 SUPPL-29, 5.1 Risk of Bleeding | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 539 reports name BRILINTA; 1700 list TICAGRELOR (any product) | Top-10 terms checked against S4 label: 5 found, 5 not found |
| S7 | FDA enforcement | Any recall? | D-0433-2021 (Class II, reported status 'Terminated', 20210602): CGMP Deviations: Intermittent exposure to temperature excursion during storage. | Record text names package 0186-0776-60: **True** (application-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01225562 (COMPLETED), EG001 'Ticagrelor 60mg bd': serious AEs 1853 of 6958 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** FATIGUE, CHEST DISCOMFORT, COUGH, CONTUSION, ASTHENIA. Found in label: DYSPNOEA, DIZZINESS, MYOCARDIAL INFARCTION, NAUSEA, DIARRHOEA.
- **Recall:** D-0433-2021 names this exact package. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (11/05/2020) is reflected in the captured DailyMed label.

## Traps this trace shows
- Low ambiguity. Pulmonary function testing in the same passage found no adverse effect on lung function; that does not change the class.
- Query scope changes the count: 539 brand-named vs 1700 substance-level reports.
- Sponsor 'ASTRAZENECA' (Drugs@FDA) vs labeler 'AstraZeneca Pharmaceuticals LP' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T04.s1_rx_brand` | `06f9954abcefb00f…` | 2026-11-02T18:37:32 |
| `T04.s1_rx_brand_props` | `e46180830d4a79ee…` | 2026-11-02T18:37:32 |
| `T04.s1_rx_ingredients` | `21ec5a30fa94ef10…` | 2026-11-02T18:37:33 |
| `T04.s1_rx_reverse_1116632` | `46189d6f0bc0684b…` | 2026-11-02T18:37:33 |
| `T04.s2_ndc` | `c485fe78b6a75ddc…` | 2026-11-02T18:37:34 |
| `T04.s3_drugsfda` | `3f649adee83b0a5c…` | 2026-11-02T18:37:35 |
| `T04.s4_label` | `42556186f3b281e7…` | 2026-11-02T18:37:35 |
| `T04.s5_srlc_detail` | `2429e4fbe7bcfc1c…` | 2026-11-02T18:37:38 |
| `T04.s5_srlc_search` | `8c03200d6fc155ce…` | 2026-11-02T18:37:37 |
| `T04.s6_faers_brand_reactions` | `7b291ad2e57cc69e…` | 2026-11-02T18:37:41 |
| `T04.s6_faers_brand_total` | `863a0ae9ffb5771e…` | 2026-11-02T18:37:40 |
| `T04.s6_faers_substance` | `cb125451d1feee00…` | 2026-11-02T18:37:38 |
| `T04.s6_faers_total` | `fbf0defde628575e…` | 2026-11-02T18:37:39 |
| `T04.s7_recall_app` | `e48cf3e40ec88d67…` | 2026-11-02T18:37:41 |
| `T04.s8_trial` | `aedd64a329d8f2ca…` | 2026-11-02T18:37:43 |
| `T04.s8_trials_search` | `ec99570822cf3cb2…` | 2026-11-02T18:37:42 |
| `T04.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:37:43 |

Full records: [claude/traces/T04.jsonl](../claude/traces/T04.jsonl) · checks: [verification/T04.json](../verification/T04.json) · questions: [shared/questions/T04.json](../shared/questions/T04.json)
