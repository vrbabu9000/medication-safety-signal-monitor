# T23 · Nexium (PPI)

**Status:** verified against sources (114/114 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:41Z – 2026-11-02T18:41Z · questions sha256 `a62d0813954c…`

## The trace in one line
Nexium → RxNorm 284799 (esomeprazole (283742)) → package 0186-4020-01 under NDA021957 → DailyMed label f4853677-1622-4037-688b-fdf533a11d96 v74 (effective 20251219) → SrLC 07/18/2023 → 2328 FAERS reports name it in 2025 → recall D-0443-2025 → trial NCT00444275.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 284799 (BN); ingredient(s) esomeprazole (283742); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0186-4020-01: 30 GRANULE, DELAYED RELEASE in 1 CARTON (0186-4020-01); labeler AstraZeneca Pharmaceuticals LP; category NDA; application NDA021957 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ASTRAZENECA; 4 product(s): 001 FOR SUSPENSION, DELAYED RELEASE EQ 20MG BASE/PACKET; 002 FOR SUSPENSION, DELAYED RELEASE EQ 40MG BASE/PACKET; 003 FOR SUSPENSION, DELAYED RELEASE EQ 2.5MG BASE/PACKET; 004 FOR SUSPENSION, DELAYED RELEASE EQ 5MG BASE/PACKET | Same application number as S2 |
| S4 | DailyMed | In '5.1 Presence of Gastric Malignancy', what role does 'gastric malignancy' play? | **underlying_condition_or_risk_factor** | Quote: "symptomatic response to therapy with NEXIUM does not preclude the presence of gastric malignancy" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 07/18/2023 SUPPL-27, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 2328 reports name NEXIUM; 3841 list ESOMEPRAZOLE MAGNESIUM (any product) | Top-10 terms checked against S4 label: 5 found, 5 not found |
| S7 | FDA enforcement | Any recall? | D-0443-2025 (Class II, reported status 'Ongoing', 20250528): Failed Impurities/Degradation Specifications: Out-of-Specification test results obtained for any individual unknown degradation product duri… | Record text names package 0186-4020-01: **False** (ingredient-level query, 11 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00444275 (COMPLETED), EG000 'Esomeprazole 20 mg Once Daily (Initial Phase)': serious AEs 8 of 2156 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DRUG INEFFECTIVE, OFF LABEL USE, HYPOACUSIS, GASTRIC CANCER, PRODUCT DOSE OMISSION ISSUE. Found in label: TINNITUS, NAUSEA, FATIGUE, HEADACHE, DIARRHOEA.
- **Recall:** D-0443-2025 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (07/18/2023) is reflected in the captured DailyMed label.

## Traps this trace shows
- Not a classic risk factor for a reaction; it is a condition that may be hidden. The class list has no 'masked condition' option, so this is the closest fit.
- Query scope changes the count: 2328 brand-named vs 3841 substance-level reports.
- Sponsor 'ASTRAZENECA' (Drugs@FDA) vs labeler 'AstraZeneca Pharmaceuticals LP' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T23.s1_rx_brand` | `7c68b78ba559e566…` | 2026-11-02T18:41:27 |
| `T23.s1_rx_brand_props` | `09eb0993a01f3985…` | 2026-11-02T18:41:27 |
| `T23.s1_rx_ingredients` | `c9baa61556021647…` | 2026-11-02T18:41:27 |
| `T23.s1_rx_reverse_283742` | `80ebbd0732808766…` | 2026-11-02T18:41:28 |
| `T23.s2_ndc` | `26e5b00fdf506028…` | 2026-11-02T18:41:29 |
| `T23.s3_drugsfda` | `693c4f3b66f4adbb…` | 2026-11-02T18:41:29 |
| `T23.s4_label` | `514a5297aa9f5284…` | 2026-11-02T18:41:30 |
| `T23.s5_srlc_detail` | `45486c5171534f25…` | 2026-11-02T18:41:33 |
| `T23.s5_srlc_search` | `0cf3b6c4b1fc8b8f…` | 2026-11-02T18:41:32 |
| `T23.s6_faers_brand_reactions` | `339b3ba709365b46…` | 2026-11-02T18:41:36 |
| `T23.s6_faers_brand_total` | `dccfd61a41503d77…` | 2026-11-02T18:41:35 |
| `T23.s6_faers_substance` | `88ad49acd5009c92…` | 2026-11-02T18:41:34 |
| `T23.s6_faers_total` | `f1e63df44b759ae6…` | 2026-11-02T18:41:34 |
| `T23.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:41:37 |
| `T23.s7_recall_ingredient` | `15ddb5ee1c8851ef…` | 2026-11-02T18:41:38 |
| `T23.s8_trial` | `0fccb216d9075c7c…` | 2026-11-02T18:41:38 |
| `T23.s8_trials_search` | `4e46f454c6130e7a…` | 2026-11-02T18:41:38 |
| `T23.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:41:39 |

Full records: [claude/traces/T23.jsonl](../claude/traces/T23.jsonl) · checks: [verification/T23.json](../verification/T23.json) · questions: [shared/questions/T23.json](../shared/questions/T23.json)
