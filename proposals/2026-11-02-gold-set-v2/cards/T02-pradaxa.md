# T02 · Pradaxa (anticoagulant)

**Status:** verified against sources (112/112 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:37Z – 2026-11-02T18:37Z · questions sha256 `e22e2d316edd…`

## The trace in one line
Pradaxa → RxNorm 1037046 (dabigatran etexilate (1037042)) → package 0597-0425-78 under NDA214358 → DailyMed label 9ac0a64a-8666-45f7-9d4f-40fd894f7e6d v7 (effective 20250627) → SrLC 11/14/2023 → 533 FAERS reports name it in 2025 → recall D-0738-2026 → trial NCT02239120.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 1037046 (BN); ingredient(s) dabigatran etexilate (1037042); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0597-0425-78: 1 BAG in 1 CARTON (0597-0425-78)  / 60 PELLET in 1 BAG; labeler Boehringer Ingelheim Pharmaceuticals, Inc.; category NDA; application NDA214358 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor BOEHRINGER INGELHEIM; 6 product(s): 001 PELLETS EQ 20MG BASE/PACKET; 002 PELLETS EQ 30MG BASE/PACKET; 003 PELLETS EQ 40MG BASE/PACKET; 004 PELLETS EQ 50MG BASE/PACKET; 005 PELLETS EQ 110MG BASE/PACKET; 006 PELLETS EQ 150MG BASE/PACKET | Same application number as S2 |
| S4 | DailyMed | In '5.5 Effect of P-gp Inducers and Inhibitors on Dabigatran Exposure', what role does 'P-gp inducers' play? | **co_medication_risk_factor** | Quote: "The concomitant use of PRADAXA with P-gp inducers (e.g., rifampin) reduces exposure to dabigatran and should generally be avoided" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 11/14/2023 SUPPL-7, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 533 reports name PRADAXA; 680 list DABIGATRAN ETEXILATE MESYLATE (any product) | Top-10 terms checked against S4 label: 3 found, 7 not found |
| S7 | FDA enforcement | Any recall? | D-0738-2026 (Class III, reported status 'Ongoing', 20260805): Failed impurity/degradation specification: an OOS result observed in Related substance test analysis w.r.t Impurity II, Impurity III and Tot… | Record text names package 0597-0425-78: **False** (ingredient-level query, 9 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT02239120 (COMPLETED), EG000 'Dabigatran Etexilate 110 or 150 Milligram (mg)': serious AEs 724 of 2676 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** FATIGUE, HEADACHE, CEREBROVASCULAR ACCIDENT, DIZZINESS, DYSPNOEA, ARTHRALGIA, PAIN IN EXTREMITY. Found in label: FALL, RASH, BACK PAIN.
- **Recall:** D-0738-2026 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (11/14/2023) is reflected in the captured DailyMed label.

## Traps this trace shows
- The risk is loss of effect (lower exposure), not a new adverse reaction. Same passage names impaired renal function, a patient factor, which is a different class.
- Query scope changes the count: 533 brand-named vs 680 substance-level reports.
- Sponsor 'BOEHRINGER INGELHEIM' (Drugs@FDA) vs labeler 'Boehringer Ingelheim Pharmaceuticals, Inc.' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T02.s1_rx_brand` | `85252e32204cd7a6…` | 2026-11-02T18:37:08 |
| `T02.s1_rx_brand_props` | `3e467a52583d9e26…` | 2026-11-02T18:37:09 |
| `T02.s1_rx_ingredients` | `97cbf6d431b772bd…` | 2026-11-02T18:37:09 |
| `T02.s1_rx_reverse_1037042` | `62f9443f4c9b129d…` | 2026-11-02T18:37:09 |
| `T02.s2_ndc` | `93a655b0fe6e6802…` | 2026-11-02T18:37:10 |
| `T02.s3_drugsfda` | `d63d20557f6c90c2…` | 2026-11-02T18:37:11 |
| `T02.s4_label` | `1cceb269a5b3a699…` | 2026-11-02T18:37:11 |
| `T02.s5_srlc_detail` | `ebcf085f5ae99160…` | 2026-11-02T18:37:13 |
| `T02.s5_srlc_search` | `5b66ef95ca372a33…` | 2026-11-02T18:37:13 |
| `T02.s6_faers_brand_reactions` | `8102414c299f0065…` | 2026-11-02T18:37:16 |
| `T02.s6_faers_brand_total` | `81d0b2350e6930a9…` | 2026-11-02T18:37:16 |
| `T02.s6_faers_substance` | `a5c62cb057a35b8a…` | 2026-11-02T18:37:14 |
| `T02.s6_faers_total` | `351927fae2223469…` | 2026-11-02T18:37:15 |
| `T02.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:37:17 |
| `T02.s7_recall_ingredient` | `4280740e20d63f0f…` | 2026-11-02T18:37:18 |
| `T02.s8_trial` | `c304ded947761993…` | 2026-11-02T18:37:19 |
| `T02.s8_trials_search` | `f7ac3c1f47c11dd4…` | 2026-11-02T18:37:18 |
| `T02.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:37:19 |

Full records: [claude/traces/T02.jsonl](../claude/traces/T02.jsonl) · checks: [verification/T02.json](../verification/T02.json) · questions: [shared/questions/T02.json](../shared/questions/T02.json)
