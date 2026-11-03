# T08 · Farxiga (SGLT2)

**Status:** verified against sources (113/113 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:38Z – 2026-11-02T18:38Z · questions sha256 `e05fb6707c1f…`

## The trace in one line
Farxiga → RxNorm 1486972 (dapagliflozin (1488564)) → package 0310-6205-30 under NDA202293 → DailyMed label 72ad22ae-efe6-4cd6-a302-98aaee423d69 v49 (effective 20260603) → SrLC 06/03/2026 → 3063 FAERS reports name it in 2025 → recall D-0435-2021 → trial NCT01137474.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 1486972 (BN); ingredient(s) dapagliflozin (1488564); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0310-6205-30: 30 TABLET, FILM COATED in 1 BOTTLE, PLASTIC (0310-6205-30); labeler AstraZeneca Pharmaceuticals LP; category NDA; application NDA202293 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ASTRAZENECA AB; 2 product(s): 001 TABLET 5MG; 002 TABLET 10MG | Same application number as S2 |
| S4 | DailyMed | In '5.1 Diabetic Ketoacidosis in Patients with Type 1 Diabetes Mellitus and Other Ketoacidosis', what role does 'abdominal pain' play? | **symptom_of_other_condition** | Quote: "Signs and symptoms are consistent with dehydration and severe metabolic acidosis and include nausea, vomiting, abdominal pain, generalized malaise, and shortness of breath." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 06/03/2026 SUPPL-35, 5.3 Genitourinary Infections, including Urosepsis, Pyelonephritis, Necrotizing Fasciitis of the Perineum (Fournier’s Gangrene), and Genital Mycotic Infections | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 3063 reports name FARXIGA; 3258 list DAPAGLIFLOZIN PROPANEDIOL (any product) | Top-10 terms checked against S4 label: 4 found, 6 not found |
| S7 | FDA enforcement | Any recall? | D-0435-2021 (Class II, reported status 'Terminated', 20210602): CGMP Deviations: Intermittent exposure to temperature excursion during storage. | Record text names package 0310-6205-30: **False** (ingredient-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01137474 (COMPLETED), EG001 'Dapagliflozin, 2.5 mg (Randomized Before Protocol Amendment 8)': serious AEs 3 of 166 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DIARRHOEA, FATIGUE, PRODUCT DOSE OMISSION ISSUE, DIZZINESS, OFF LABEL USE, HEADACHE. Found in label: NAUSEA, VOMITING, CONSTIPATION, DEATH.
- **Recall:** D-0435-2021 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (06/03/2026) is reflected in the captured DailyMed label.

## Traps this trace shows
- Debatable: ketoacidosis itself is the drug-related warning, so a reviewer may treat its symptoms as reactions. Pancreatic disorders in the same passage are risk factors.
- Query scope changes the count: 3063 brand-named vs 3258 substance-level reports.
- Sponsor 'ASTRAZENECA AB' (Drugs@FDA) vs labeler 'AstraZeneca Pharmaceuticals LP' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T08.s1_rx_brand` | `13666533fa4d3a22…` | 2026-11-02T18:38:20 |
| `T08.s1_rx_brand_props` | `0b7dcfff517700c5…` | 2026-11-02T18:38:20 |
| `T08.s1_rx_ingredients` | `e0a35072ce29c051…` | 2026-11-02T18:38:21 |
| `T08.s1_rx_reverse_1488564` | `fa6b799fae18f803…` | 2026-11-02T18:38:21 |
| `T08.s2_ndc` | `c92e9fd5091a90f8…` | 2026-11-02T18:38:22 |
| `T08.s3_drugsfda` | `f3750ceab34e8c60…` | 2026-11-02T18:38:23 |
| `T08.s4_label` | `e712d0df42d5bb52…` | 2026-11-02T18:38:23 |
| `T08.s5_srlc_detail` | `26162ac5880a35ae…` | 2026-11-02T18:38:25 |
| `T08.s5_srlc_search` | `a912977bb3d11ccd…` | 2026-11-02T18:38:25 |
| `T08.s6_faers_brand_reactions` | `86fa547a129aa6eb…` | 2026-11-02T18:38:29 |
| `T08.s6_faers_brand_total` | `29f0ebea601131cf…` | 2026-11-02T18:38:28 |
| `T08.s6_faers_substance` | `d763b9a0084e5a0b…` | 2026-11-02T18:38:26 |
| `T08.s6_faers_total` | `4a4180445e6fbdfc…` | 2026-11-02T18:38:27 |
| `T08.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:38:29 |
| `T08.s7_recall_ingredient` | `e1d721923ed60f72…` | 2026-11-02T18:38:30 |
| `T08.s8_trial` | `e5067b32cd7b3bab…` | 2026-11-02T18:38:31 |
| `T08.s8_trials_search` | `595264fac395c47d…` | 2026-11-02T18:38:31 |
| `T08.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:38:31 |

Full records: [claude/traces/T08.jsonl](../claude/traces/T08.jsonl) · checks: [verification/T08.json](../verification/T08.json) · questions: [shared/questions/T08.json](../shared/questions/T08.json)
