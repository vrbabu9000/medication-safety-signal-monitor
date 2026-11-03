# T21 · Seroquel (antipsychotic)

**Status:** verified against sources (115/115 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:41Z – 2026-11-02T18:41Z · questions sha256 `a99b312a56c6…`

## The trace in one line
Seroquel → RxNorm 83553 (quetiapine (51272)) → package 0310-0271-10 under NDA020639 → DailyMed label 0584dda8-bc3c-48fe-1a90-79608f78e8a0 v50 (effective 20250122) → SrLC 01/22/2025 → 1628 FAERS reports name it in 2025 → recall D-1000-2020 → trial NCT01727726.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 83553 (BN); ingredient(s) quetiapine (51272); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0310-0271-10: 100 TABLET, FILM COATED in 1 BOTTLE (0310-0271-10); labeler AstraZeneca Pharmaceuticals LP; category NDA; application NDA020639 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor CHEPLAPHARM; 7 product(s): 001 TABLET EQ 25MG BASE; 002 TABLET EQ 100MG BASE; 003 TABLET EQ 200MG BASE; 004 TABLET EQ 150MG BASE **Federal Register determination that product was not discontinued or withdrawn for safety or effectiveness reasons**; 005 TABLET EQ 300MG BASE; 006 TABLET EQ 400MG BASE; 007 TABLET EQ 50MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.4 Neuroleptic Malignant Syndrome (NMS)', what role does 'muscle rigidity' play? | **symptom_of_other_condition** | Quote: "Clinical manifestations of NMS are hyperpyrexia, muscle rigidity, altered mental status, and evidence of autonomic instability" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 01/22/2025 SUPPL-74, 5.15 Hyperprolactinemia | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1628 reports name SEROQUEL; 5052 list QUETIAPINE FUMARATE (any product) | Top-10 terms checked against S4 label: 6 found, 4 not found |
| S7 | FDA enforcement | Any recall? | D-1000-2020 (Class III, reported status 'Terminated', 20200318): Labeling; Incorrect or Missing Package Insert: Product was packaged with the package insert for Quetiapine Fumarate Tablets not Quetiapine F… | Record text names package 0310-0271-10: **False** (ingredient-level query, 5 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01727726 (COMPLETED), EG001 'Seroquel XR + ADT': serious AEs 1 of 100 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DRUG INEFFECTIVE, HALLUCINATION, OFF LABEL USE, PRODUCT DOSE OMISSION ISSUE. Found in label: NAUSEA, DEATH, FATIGUE, FALL, INSOMNIA, ANXIETY.
- **Recall:** D-1000-2020 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (01/22/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- NMS itself is the reaction; a reviewer may class its manifestations as reactions.
- Query scope changes the count: 1628 brand-named vs 5052 substance-level reports.
- Sponsor 'CHEPLAPHARM' (Drugs@FDA) vs labeler 'AstraZeneca Pharmaceuticals LP' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T21.s1_rx_brand` | `ec4fd7c86c3947d4…` | 2026-11-02T18:41:01 |
| `T21.s1_rx_brand_props` | `81c81fca27207c36…` | 2026-11-02T18:41:01 |
| `T21.s1_rx_ingredients` | `746f297b4786924e…` | 2026-11-02T18:41:02 |
| `T21.s1_rx_reverse_51272` | `1d44d2cfc28aa3ba…` | 2026-11-02T18:41:02 |
| `T21.s2_ndc` | `cf797ed3161f1332…` | 2026-11-02T18:41:03 |
| `T21.s3_drugsfda` | `f7c3bc55ac2b3ad9…` | 2026-11-02T18:41:04 |
| `T21.s4_label` | `399ff8781d779c9e…` | 2026-11-02T18:41:04 |
| `T21.s5_srlc_detail` | `5d6a630fe01713aa…` | 2026-11-02T18:41:07 |
| `T21.s5_srlc_search` | `8dbd649cd8fc79c8…` | 2026-11-02T18:41:06 |
| `T21.s6_faers_brand_reactions` | `c8b2b7578f3b9edd…` | 2026-11-02T18:41:10 |
| `T21.s6_faers_brand_total` | `ccc67aa1b74d667b…` | 2026-11-02T18:41:10 |
| `T21.s6_faers_substance` | `91a095d5709f7fce…` | 2026-11-02T18:41:08 |
| `T21.s6_faers_total` | `ec18b952d9123e37…` | 2026-11-02T18:41:09 |
| `T21.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:41:11 |
| `T21.s7_recall_ingredient` | `c222f62d1538367b…` | 2026-11-02T18:41:12 |
| `T21.s8_trial` | `411343a3083eb9af…` | 2026-11-02T18:41:13 |
| `T21.s8_trials_search` | `cbfb6b0ed454e15e…` | 2026-11-02T18:41:13 |
| `T21.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:41:13 |

Full records: [claude/traces/T21.jsonl](../claude/traces/T21.jsonl) · checks: [verification/T21.json](../verification/T21.json) · questions: [shared/questions/T21.json](../shared/questions/T21.json)
