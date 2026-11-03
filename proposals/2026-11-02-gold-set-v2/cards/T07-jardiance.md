# T07 · Jardiance (SGLT2)

**Status:** verified against sources (108/108 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:38Z – 2026-11-02T18:38Z · questions sha256 `d9def5b43a39…`

## The trace in one line
Jardiance → RxNorm 1545659 (empagliflozin (1545653)) → package 0597-0152-07 under NDA204629 → DailyMed label faf3dd6a-9cd0-39c2-0d2e-232cb3f67565 v31 (effective 20260130) → SrLC 10/24/2025 → 7741 FAERS reports name it in 2025 → recall D-0185-2024 → trial NCT01131676.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 1545659 (BN); ingredient(s) empagliflozin (1545653); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0597-0152-07: 1 BOTTLE in 1 CARTON (0597-0152-07)  / 7 TABLET, FILM COATED in 1 BOTTLE; labeler Boehringer Ingelheim Pharmaceuticals, Inc.; category NDA; application NDA204629 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor BOEHRINGER INGELHEIM; 2 product(s): 001 TABLET 10MG; 002 TABLET 25MG | Same application number as S2 |
| S4 | DailyMed | In '5.2 Volume Depletion', what role does 'elderly patients' play? | **underlying_condition_or_risk_factor** | Quote: "Patients with impaired renal function (eGFR less than 60 mL/min/1.73 m2), elderly patients, or patients on loop diuretics may be at increased risk for volume depletion or hypotension." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 10/24/2025 SUPPL-63, 5.3 Genitourinary Infections, including Urosepsis, Pyelonephritis, Necrotizing Fasciitis of the Perineum (Fournier’s Gangrene), and Genital Mycotic Infections | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 7741 reports name JARDIANCE; 9604 list EMPAGLIFLOZIN (any product) | Top-10 terms checked against S4 label: 3 found, 7 not found |
| S7 | FDA enforcement | Any recall? | D-0185-2024 (Class II, reported status 'Terminated', 20240103): CGMP Deviations: Products were exposed to temperatures outside of the products labeled storage conditions. | Record text names package 0597-0152-07: **False** (application-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01131676 (COMPLETED), EG001 'Empagliflozin 10 mg': serious AEs 876 of 2345 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DIARRHOEA, FATIGUE, OFF LABEL USE, DYSPNOEA, IMPAIRED GASTRIC EMPTYING, DIZZINESS, HEADACHE. Found in label: NAUSEA, VOMITING, CONSTIPATION.
- **Recall:** D-0185-2024 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (10/24/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- Loop diuretics in the same sentence are a co-medication risk factor, a different class.
- Query scope changes the count: 7741 brand-named vs 9604 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'BOEHRINGER INGELHEIM' (Drugs@FDA) vs labeler 'Boehringer Ingelheim Pharmaceuticals, Inc.' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T07.s1_rx_brand` | `c2e5d52666d775db…` | 2026-11-02T18:38:09 |
| `T07.s1_rx_brand_props` | `2105ea9a2b387897…` | 2026-11-02T18:38:09 |
| `T07.s1_rx_ingredients` | `49bca59ed18ed010…` | 2026-11-02T18:38:09 |
| `T07.s1_rx_reverse_1545653` | `8e09593b17cbd603…` | 2026-11-02T18:38:10 |
| `T07.s2_ndc` | `01730596d7031d73…` | 2026-11-02T18:38:11 |
| `T07.s3_drugsfda` | `a49c65512a89e6d8…` | 2026-11-02T18:38:11 |
| `T07.s4_label` | `ec88bb9aa0eee51a…` | 2026-11-02T18:38:12 |
| `T07.s5_srlc_detail` | `f75d513fe21a1e0e…` | 2026-11-02T18:38:14 |
| `T07.s5_srlc_search` | `0292eef5c089d8f6…` | 2026-11-02T18:38:13 |
| `T07.s6_faers_brand_reactions` | `453d998d18d05fde…` | 2026-11-02T18:38:17 |
| `T07.s6_faers_brand_total` | `96cfa7e62a9ec89e…` | 2026-11-02T18:38:16 |
| `T07.s6_faers_substance` | `4130248c18e72f2e…` | 2026-11-02T18:38:15 |
| `T07.s6_faers_total` | `d04731795e47bf66…` | 2026-11-02T18:38:16 |
| `T07.s7_recall_app` | `362fa8043d3007fb…` | 2026-11-02T18:38:18 |
| `T07.s8_trial` | `42ff56b66215105e…` | 2026-11-02T18:38:19 |
| `T07.s8_trials_search` | `f0277430c8682c26…` | 2026-11-02T18:38:18 |
| `T07.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:38:19 |

Full records: [claude/traces/T07.jsonl](../claude/traces/T07.jsonl) · checks: [verification/T07.json](../verification/T07.json) · questions: [shared/questions/T07.json](../shared/questions/T07.json)
