# T26 · Cozaar (ARB)

**Status:** verified against sources (118/118 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:42Z – 2026-11-02T18:42Z · questions sha256 `d86ccc0b3110…`

## The trace in one line
Cozaar → RxNorm 151558 (losartan (52175)) → package 78206-121-01 under NDA020386 → DailyMed label 9949448f-c3b9-44ee-94ed-c1aca8c90f39 v9 (effective 20260120) → SrLC 06/20/2025 → 603 FAERS reports name it in 2025 → recall D-0498-2024 → trial NCT00090259.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 151558 (BN); ingredient(s) losartan (52175); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 78206-121-01: 90 TABLET, FILM COATED in 1 BOTTLE (78206-121-01); labeler Organon LLC; category NDA; application NDA020386 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ORGANON; 3 product(s): 001 TABLET 25MG; 002 TABLET 50MG; 003 TABLET 100MG | Same application number as S2 |
| S4 | DailyMed | In '4 CONTRAINDICATIONS', what role does 'patients who are hypersensitive to any component of this product' play? | **contraindicated_population** | Quote: "COZAAR is contraindicated: In patients who are hypersensitive to any component of this product." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 06/20/2025 SUPPL-69, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 603 reports name COZAAR; 5713 list LOSARTAN POTASSIUM (any product) | Top-10 terms checked against S4 label: 9 found, 1 not found |
| S7 | FDA enforcement | Any recall? | D-0498-2024 (Class II, reported status 'Ongoing', 20240522): Presence of foreign substance: plastic-like substance. | Record text names package 78206-121-01: **False** (ingredient-level query, 35 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00090259 (COMPLETED), EG000 'Losartan 50 mg': serious AEs 691 of 1913 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE. Found in label: NAUSEA, DIARRHOEA, FATIGUE, DYSPNOEA, HEADACHE, ARTHRALGIA, DIZZINESS, VOMITING, BACK PAIN.
- **Recall:** D-0498-2024 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (06/20/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- The second item (aliskiren in patients with diabetes) combines a co-medication and a population; it is not the target.
- Query scope changes the count: 603 brand-named vs 5713 substance-level reports.
- Sponsor 'ORGANON' (Drugs@FDA) vs labeler 'Organon LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T26.s1_rx_brand` | `dd2bed989e7de15d…` | 2026-11-02T18:42:04 |
| `T26.s1_rx_brand_props` | `fcefad029d280f02…` | 2026-11-02T18:42:04 |
| `T26.s1_rx_ingredients` | `e6d061fe0c5ecc0a…` | 2026-11-02T18:42:04 |
| `T26.s1_rx_reverse_52175` | `828ab47e90b55e5f…` | 2026-11-02T18:42:05 |
| `T26.s2_ndc` | `851f504d7891dc29…` | 2026-11-02T18:42:06 |
| `T26.s3_drugsfda` | `0c51fc85be7b9da5…` | 2026-11-02T18:42:06 |
| `T26.s4_label` | `855caab1c9ba60a0…` | 2026-11-02T18:42:07 |
| `T26.s5_srlc_detail` | `ce1718cfc9b3f61f…` | 2026-11-02T18:42:09 |
| `T26.s5_srlc_search` | `8bf9e3e01bb0f452…` | 2026-11-02T18:42:08 |
| `T26.s6_faers_brand_reactions` | `d1ff44556c8804b6…` | 2026-11-02T18:42:12 |
| `T26.s6_faers_brand_total` | `2f29fd122ff15758…` | 2026-11-02T18:42:11 |
| `T26.s6_faers_substance` | `f4becd25e2ecf7f0…` | 2026-11-02T18:42:10 |
| `T26.s6_faers_total` | `63a8abcb360810e5…` | 2026-11-02T18:42:10 |
| `T26.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:42:13 |
| `T26.s7_recall_ingredient` | `f17e3760e3e68b8f…` | 2026-11-02T18:42:14 |
| `T26.s8_trial` | `2745374c90a6be8a…` | 2026-11-02T18:42:15 |
| `T26.s8_trials_search` | `be6b179308c8a306…` | 2026-11-02T18:42:14 |
| `T26.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:42:15 |

Full records: [claude/traces/T26.jsonl](../claude/traces/T26.jsonl) · checks: [verification/T26.json](../verification/T26.json) · questions: [shared/questions/T26.json](../shared/questions/T26.json)
