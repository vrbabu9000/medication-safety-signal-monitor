# T05 · Lipitor (statin)

**Status:** verified against sources (113/113 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:37Z – 2026-11-02T18:37Z · questions sha256 `4a1fd2b82b7a…`

## The trace in one line
Lipitor → RxNorm 153165 (atorvastatin (83367)) → package 58151-155-77 under NDA020702 → DailyMed label a60cc18b-0631-4cf0-b021-9f52224ece65 v8 (effective 20240415) → SrLC 04/02/2024 → 3727 FAERS reports name it in 2025 → recall D-0020-2026 → trial NCT00289900.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 153165 (BN); ingredient(s) atorvastatin (83367); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 58151-155-77: 90 TABLET, FILM COATED in 1 BOTTLE (58151-155-77); labeler Viatris Specialty LLC; category NDA; application NDA020702 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor UPJOHN; 4 product(s): 001 TABLET EQ 10MG BASE; 002 TABLET EQ 20MG BASE; 003 TABLET EQ 40MG BASE; 004 TABLET EQ 80MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.1 Myopathy and Rhabdomyolysis', what role does 'rhabdomyolysis' play? | **reaction_or_warning** | Quote: "LIPITOR may cause myopathy (muscle pain, tenderness, or weakness associated with elevated creatine kinase [CK]) and rhabdomyolysis." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 04/02/2024 SUPPL-81, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 3727 reports name LIPITOR; 11221 list ATORVASTATIN CALCIUM (any product) | Top-10 terms checked against S4 label: 4 found, 6 not found |
| S7 | FDA enforcement | Any recall? | D-0020-2026 (Class II, reported status 'Ongoing', 20251022): Failed Dissolution Specifications | Record text names package 58151-155-77: **False** (ingredient-level query, 41 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00289900 (COMPLETED), EG002 'Atorvastatin 10 mg': serious AEs 3 of 298 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, HEADACHE, DYSPNOEA, ASTHENIA, DRUG INEFFECTIVE, PNEUMONIA. Found in label: FATIGUE, DIARRHOEA, NAUSEA, PAIN.
- **Recall:** D-0020-2026 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (04/02/2024) is reflected in the captured DailyMed label.

## Traps this trace shows
- Muscle pain in the same sentence is part of the definition of myopathy (a symptom of it), not the target.
- Query scope changes the count: 3727 brand-named vs 11221 substance-level reports.
- Sponsor 'UPJOHN' (Drugs@FDA) vs labeler 'Viatris Specialty LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T05.s1_rx_brand` | `62672131d5b4f06f…` | 2026-11-02T18:37:43 |
| `T05.s1_rx_brand_props` | `be26ce556267053e…` | 2026-11-02T18:37:44 |
| `T05.s1_rx_ingredients` | `553ca19fa0e5909d…` | 2026-11-02T18:37:44 |
| `T05.s1_rx_reverse_83367` | `8840f28358a210f3…` | 2026-11-02T18:37:45 |
| `T05.s2_ndc` | `12b9d2bb84ed6455…` | 2026-11-02T18:37:45 |
| `T05.s3_drugsfda` | `c4ebfa760c462c6a…` | 2026-11-02T18:37:46 |
| `T05.s4_label` | `c6748f079a3cf15a…` | 2026-11-02T18:37:47 |
| `T05.s5_srlc_detail` | `a040f730024d0f08…` | 2026-11-02T18:37:49 |
| `T05.s5_srlc_search` | `1960f79feca07dac…` | 2026-11-02T18:37:48 |
| `T05.s6_faers_brand_reactions` | `09a6668292df3615…` | 2026-11-02T18:37:52 |
| `T05.s6_faers_brand_total` | `59d35b0c21524d4d…` | 2026-11-02T18:37:51 |
| `T05.s6_faers_substance` | `2d5432315b77581d…` | 2026-11-02T18:37:50 |
| `T05.s6_faers_total` | `56ff09a3fa20c0bd…` | 2026-11-02T18:37:50 |
| `T05.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:37:53 |
| `T05.s7_recall_ingredient` | `49f5c146aae44e0b…` | 2026-11-02T18:37:54 |
| `T05.s8_trial` | `05fca257601df045…` | 2026-11-02T18:37:55 |
| `T05.s8_trials_search` | `fb6c47bb0a6f2c45…` | 2026-11-02T18:37:54 |
| `T05.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:37:55 |

Full records: [claude/traces/T05.jsonl](../claude/traces/T05.jsonl) · checks: [verification/T05.json](../verification/T05.json) · questions: [shared/questions/T05.json](../shared/questions/T05.json)
