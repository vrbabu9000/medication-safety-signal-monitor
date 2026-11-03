# T13 · OxyContin (opioid)

**Status:** verified against sources (114/114 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:39Z – 2026-11-02T18:39Z · questions sha256 `d5f1b13a1a00…`

## The trace in one line
OxyContin → RxNorm 218986 (oxycodone (7804)) → package 59011-410-10 under NDA022272 → DailyMed label bfdfe235-d717-4855-a3c8-a13d26dadede v44 (effective 20260624) → SrLC 12/22/2025 → 1114 FAERS reports name it in 2025 → recall D-0338-2026 → trial NCT00361504.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 218986 (BN); ingredient(s) oxycodone (7804); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 59011-410-10: 100 TABLET, FILM COATED, EXTENDED RELEASE in 1 BOTTLE (59011-410-10); labeler Knoa Pharma LLC; category NDA; application NDA022272 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor KNOA PHARMA; 7 product(s): 001 TABLET, EXTENDED RELEASE 10MG; 002 TABLET, EXTENDED RELEASE 15MG; 003 TABLET, EXTENDED RELEASE 20MG; 004 TABLET, EXTENDED RELEASE 30MG; 005 TABLET, EXTENDED RELEASE 40MG; 006 TABLET, EXTENDED RELEASE 60MG; 007 TABLET, EXTENDED RELEASE 80MG | Same application number as S2 |
| S4 | DailyMed | In '5.4 Neonatal Opioid Withdrawal Syndrome', what role does 'Neonatal opioid withdrawal syndrome' play? | **reaction_or_warning** | Quote: "Neonatal opioid withdrawal syndrome, unlike opioid withdrawal syndrome in adults, may be life-threatening if not recognized and treated" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 12/22/2025 SUPPL-52, 5.1 Addiction, Abuse, and Misuse | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1114 reports name OXYCONTIN; 5323 list OXYCODONE HYDROCHLORIDE (any product) | Top-10 terms checked against S4 label: 5 found, 5 not found |
| S7 | FDA enforcement | Any recall? | D-0338-2026 (Class II, reported status 'Ongoing', 20260218): Defective container: card seal defects (weak/non-existent seals), leading to the tablets falling out of their cavities. | Record text names package 59011-410-10: **False** (ingredient-level query, 11 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00361504 (COMPLETED), EG001 'Oxycodone': serious AEs 9 of 223 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DRUG DEPENDENCE, IMPAIRED QUALITY OF LIFE, DRUG DIVERSION, TOXICITY TO VARIOUS AGENTS, EMOTIONAL DISTRESS. Found in label: OVERDOSE, DRUG ABUSE, PAIN, DEATH, NAUSEA.
- **Recall:** D-0338-2026 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (12/22/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- The affected person is the neonate, not the patient taking the drug; a reviewer may want that qualifier kept.
- Query scope changes the count: 1114 brand-named vs 5323 substance-level reports.
- Sponsor 'KNOA PHARMA' (Drugs@FDA) vs labeler 'Knoa Pharma LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T13.s1_rx_brand` | `7201985a79ccbc7b…` | 2026-11-02T18:39:18 |
| `T13.s1_rx_brand_props` | `ee671cd9406df823…` | 2026-11-02T18:39:18 |
| `T13.s1_rx_ingredients` | `fc92ba57ee251f8e…` | 2026-11-02T18:39:19 |
| `T13.s1_rx_reverse_7804` | `c3eaa9bad72c4974…` | 2026-11-02T18:39:19 |
| `T13.s2_ndc` | `a96fc427e66408aa…` | 2026-11-02T18:39:20 |
| `T13.s3_drugsfda` | `af5b96dfd46b0f90…` | 2026-11-02T18:39:21 |
| `T13.s4_label` | `9bda5469e52f775c…` | 2026-11-02T18:39:21 |
| `T13.s5_srlc_detail` | `0b711647c0f3300c…` | 2026-11-02T18:39:23 |
| `T13.s5_srlc_search` | `801c48d19b44b641…` | 2026-11-02T18:39:23 |
| `T13.s6_faers_brand_reactions` | `923708b162865d53…` | 2026-11-02T18:39:26 |
| `T13.s6_faers_brand_total` | `48c6aecc16af9c3b…` | 2026-11-02T18:39:26 |
| `T13.s6_faers_substance` | `fbcddde3746d165c…` | 2026-11-02T18:39:24 |
| `T13.s6_faers_total` | `da116a3adfcbe058…` | 2026-11-02T18:39:25 |
| `T13.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:39:27 |
| `T13.s7_recall_ingredient` | `1f77ca19f386172c…` | 2026-11-02T18:39:28 |
| `T13.s8_trial` | `a7cf015627b862fd…` | 2026-11-02T18:39:29 |
| `T13.s8_trials_search` | `a65f182b2c62e087…` | 2026-11-02T18:39:28 |
| `T13.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:39:29 |

Full records: [claude/traces/T13.jsonl](../claude/traces/T13.jsonl) · checks: [verification/T13.json](../verification/T13.json) · questions: [shared/questions/T13.json](../shared/questions/T13.json)
