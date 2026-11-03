# T28 · Singulair (leukotriene antagonist)

**Status:** verified against sources (117/117 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:42Z – 2026-11-02T18:42Z · questions sha256 `54b92f09b3f4…`

## The trace in one line
Singulair → RxNorm 153889 (montelukast (88249)) → package 78206-170-01 under NDA020830 → DailyMed label 482dcc92-b47f-4ea6-854a-f5ac2aea7842 v5 (effective 20250430) → SrLC 02/22/2021 → 4162 FAERS reports name it in 2025 → recall D-0086-2024 → trial NCT04885530.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 153889 (BN); ingredient(s) montelukast (88249); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 78206-170-01: 30 TABLET, CHEWABLE in 1 BOTTLE (78206-170-01); labeler Organon LLC; category NDA; application NDA020830 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ORGANON; 2 product(s): 001 TABLET, CHEWABLE EQ 5MG BASE; 002 TABLET, CHEWABLE EQ 4MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.6 Risk in Patients with Phenylketonuria', what role does 'phenylketonuria' play? | **underlying_condition_or_risk_factor** | Quote: "Phenylalanine can be harmful to patients with phenylketonuria (PKU)." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 02/22/2021 SUPPL-76, 5.6 Risk in Patients with Phenylketonuria | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 4162 reports name SINGULAIR; 7702 list MONTELUKAST SODIUM (any product) | Top-10 terms checked against S4 label: 8 found, 2 not found |
| S7 | FDA enforcement | Any recall? | D-0086-2024 (Class II, reported status 'Terminated', 20231115): Presence of Foreign Tablet(s)/Capsule(s): A foreign tablet was found in a bottle of Montelukast Sodium Tablets, USP 10mg, identified as meto… | Record text names package 78206-170-01: **False** (ingredient-level query, 6 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT04885530 (COMPLETED), EG005 'Arm F - Montelukast': serious AEs 0 of 1453 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DYSPNOEA, DRUG INEFFECTIVE. Found in label: ASTHMA, PNEUMONIA, COUGH, WHEEZING, PAIN, HEADACHE, FATIGUE, VOMITING.
- **Recall:** D-0086-2024 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (02/22/2021) is reflected in the captured DailyMed label.

## Traps this trace shows
- Applies to the chewable tablet forms; the label asks prescribers to consider total phenylalanine intake, not 'contraindicated'.
- Query scope changes the count: 4162 brand-named vs 7702 substance-level reports.
- Sponsor 'ORGANON' (Drugs@FDA) vs labeler 'Organon LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T28.s1_rx_brand` | `baa80852f541c06c…` | 2026-11-02T18:42:28 |
| `T28.s1_rx_brand_props` | `621b984a396a072f…` | 2026-11-02T18:42:28 |
| `T28.s1_rx_ingredients` | `d6dd61cb703f73d9…` | 2026-11-02T18:42:29 |
| `T28.s1_rx_reverse_88249` | `39460f2feeddf488…` | 2026-11-02T18:42:29 |
| `T28.s2_ndc` | `e1a54c8f07f0b886…` | 2026-11-02T18:42:30 |
| `T28.s3_drugsfda` | `33b833a5d7489896…` | 2026-11-02T18:42:30 |
| `T28.s4_label` | `ad63983d29aa05ec…` | 2026-11-02T18:42:31 |
| `T28.s5_srlc_detail` | `c3b6b61b7c5e3bd8…` | 2026-11-02T18:42:33 |
| `T28.s5_srlc_search` | `aeb3210b0bb0aa21…` | 2026-11-02T18:42:32 |
| `T28.s6_faers_brand_reactions` | `55c251c9116cd6b9…` | 2026-11-02T18:42:36 |
| `T28.s6_faers_brand_total` | `c0c6f59718caf012…` | 2026-11-02T18:42:35 |
| `T28.s6_faers_substance` | `3d2344e3ececf82e…` | 2026-11-02T18:42:34 |
| `T28.s6_faers_total` | `0bf97fc0cb41f174…` | 2026-11-02T18:42:35 |
| `T28.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:42:37 |
| `T28.s7_recall_ingredient` | `fbaf3e4201c553a4…` | 2026-11-02T18:42:38 |
| `T28.s8_trial` | `41a292d646e56eb0…` | 2026-11-02T18:42:38 |
| `T28.s8_trials_search` | `502cc05575c8d6a5…` | 2026-11-02T18:42:38 |
| `T28.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:42:39 |

Full records: [claude/traces/T28.jsonl](../claude/traces/T28.jsonl) · checks: [verification/T28.json](../verification/T28.json) · questions: [shared/questions/T28.json](../shared/questions/T28.json)
