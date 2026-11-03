# T11 · Januvia (DPP-4)

**Status:** verified against sources (113/113 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:38Z – 2026-11-02T18:39Z · questions sha256 `2dc15d248a6c…`

## The trace in one line
Januvia → RxNorm 638596 (sitagliptin (593411)) → package 0006-0112-28 under NDA021995 → DailyMed label f85a48d0-0407-4c50-b0fa-7673a160bf01 v71 (effective 20241114) → SrLC 06/21/2022 → 1636 FAERS reports name it in 2025 → recall D-0746-2022 → trial NCT00790205.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 638596 (BN); ingredient(s) sitagliptin (593411); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0006-0112-28: 100 BLISTER PACK in 1 CARTON (0006-0112-28)  / 1 TABLET, FILM COATED in 1 BLISTER PACK (0006-0112-01); labeler Merck Sharp & Dohme LLC; category NDA; application NDA021995 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor MSD; 3 product(s): 001 TABLET EQ 25MG BASE; 002 TABLET EQ 50MG BASE; 003 TABLET EQ 100MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.1 Pancreatitis', what role does 'acute pancreatitis' play? | **reaction_or_warning** | Quote: "There have been postmarketing reports of acute pancreatitis, including fatal and non-fatal hemorrhagic or necrotizing pancreatitis, in patients taking JANUVIA." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 06/21/2022 SUPPL-50, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1636 reports name JANUVIA; 1817 list SITAGLIPTIN PHOSPHATE (any product) | Top-10 terms checked against S4 label: 4 found, 6 not found |
| S7 | FDA enforcement | Any recall? | D-0746-2022 (Class II, reported status 'Terminated', 20220413): Presence of foreign substance: Presence of stainless steel particulates in tablets. | Record text names package 0006-0112-28: **False** (ingredient-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00790205 (COMPLETED), EG000 'Sitagliptin': serious AEs 928 of 7266 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** FATIGUE, OFF LABEL USE, IMPAIRED GASTRIC EMPTYING, PRODUCT DOSE OMISSION ISSUE, PNEUMONIA, COUGH. Found in label: NAUSEA, DIARRHOEA, VOMITING, HEADACHE.
- **Recall:** D-0746-2022 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (06/21/2022) is reflected in the captured DailyMed label.

## Traps this trace shows
- Context trap: 'history of pancreatitis' in the same passage is a possible risk factor, but the label says it is unknown whether it increases risk.
- Query scope changes the count: 1636 brand-named vs 1817 substance-level reports.
- Sponsor 'MSD' (Drugs@FDA) vs labeler 'Merck Sharp & Dohme LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T11.s1_rx_brand` | `a82bb71549c05d6c…` | 2026-11-02T18:38:55 |
| `T11.s1_rx_brand_props` | `7aa802a9da03047a…` | 2026-11-02T18:38:55 |
| `T11.s1_rx_ingredients` | `3c62435b1e1e7c85…` | 2026-11-02T18:38:56 |
| `T11.s1_rx_reverse_593411` | `805aed3051e2ee1f…` | 2026-11-02T18:38:56 |
| `T11.s2_ndc` | `b798282e936f2983…` | 2026-11-02T18:38:57 |
| `T11.s3_drugsfda` | `35261f1e105abcfa…` | 2026-11-02T18:38:58 |
| `T11.s4_label` | `fc8b2d3ff3a71c84…` | 2026-11-02T18:38:58 |
| `T11.s5_srlc_detail` | `31df5b0405a23c83…` | 2026-11-02T18:39:00 |
| `T11.s5_srlc_search` | `9af8ac2171f422c4…` | 2026-11-02T18:39:00 |
| `T11.s6_faers_brand_reactions` | `066899d91edd664a…` | 2026-11-02T18:39:03 |
| `T11.s6_faers_brand_total` | `df86aa7edbe4a93c…` | 2026-11-02T18:39:03 |
| `T11.s6_faers_substance` | `5fb40bc394fa46cb…` | 2026-11-02T18:39:01 |
| `T11.s6_faers_total` | `677e368a960f72ed…` | 2026-11-02T18:39:02 |
| `T11.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:39:04 |
| `T11.s7_recall_ingredient` | `75886c19f8cde8fa…` | 2026-11-02T18:39:05 |
| `T11.s8_trial` | `d9dd18199150722f…` | 2026-11-02T18:39:06 |
| `T11.s8_trials_search` | `9666bb9bb3dd483a…` | 2026-11-02T18:39:05 |
| `T11.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:39:06 |

Full records: [claude/traces/T11.jsonl](../claude/traces/T11.jsonl) · checks: [verification/T11.json](../verification/T11.json) · questions: [shared/questions/T11.json](../shared/questions/T11.json)
