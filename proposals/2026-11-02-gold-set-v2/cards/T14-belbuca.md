# T14 · Belbuca (opioid)

**Status:** verified against sources (110/110 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:39Z – 2026-11-02T18:39Z · questions sha256 `a392fc324038…`

## The trace in one line
Belbuca → RxNorm 1716058 (buprenorphine (1819)) → package 59385-021-60 under NDA207932 → DailyMed label bc2b7a3d-72cf-497c-95b0-ba2b71f63c64 v18 (effective 20260102) → SrLC 12/22/2025 → 384 FAERS reports name it in 2025 → recall D-0448-2021 → trial NCT00315341.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 1716058 (BN); ingredient(s) buprenorphine (1819); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 59385-021-60: 60 POUCH in 1 CARTON (59385-021-60)  / 1 FILM, SOLUBLE in 1 POUCH (59385-021-01); labeler BioDelivery Sciences International Inc; category NDA; application NDA207932 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor BDSI; 7 product(s): 001 FILM EQ 0.075MG BASE; 002 FILM EQ 0.15MG BASE; 003 FILM EQ 0.3MG BASE; 004 FILM EQ 0.45MG BASE; 005 FILM EQ 0.6MG BASE; 006 FILM EQ 0.75MG BASE; 007 FILM EQ 0.9MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.14 Dental Adverse Events', what role does 'wait for at least one hour after taking BELBUCA before brushing teeth' play? | **administration_instruction** | Quote: "Advise patients to wait for at least one hour after taking BELBUCA before brushing teeth" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 12/22/2025 SUPPL-29, 5.1 Addiction, Abuse, and Misuse | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 384 reports name BELBUCA; 898 list BUPRENORPHINE HYDROCHLORIDE (any product) | Top-10 terms checked against S4 label: 5 found, 5 not found |
| S7 | FDA enforcement | Any recall? | D-0448-2021 (Class II, reported status 'Terminated', 20210602): CGMP Deviations: Intermittent exposure to temperature excursion during storage. | Record text names package 59385-021-60: **False** (application-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00315341 (COMPLETED), EG000 'Buprenorphine/Nx': serious AEs 38 of 727 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** PRODUCT ADHESION ISSUE, PRODUCT SOLUBILITY ABNORMAL, DRUG INEFFECTIVE, THERAPEUTIC RESPONSE DECREASED, OFF LABEL USE. Found in label: DENTAL CARIES, NAUSEA, PAIN, FATIGUE, HEADACHE.
- **Recall:** D-0448-2021 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (12/22/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- Context trap: dental caries, tooth fracture and tooth loss in the same passage are reactions; the instruction is not.
- Query scope changes the count: 384 brand-named vs 898 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'BDSI' (Drugs@FDA) vs labeler 'BioDelivery Sciences International Inc' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T14.s1_rx_brand` | `6eee79b8b5c552be…` | 2026-11-02T18:39:30 |
| `T14.s1_rx_brand_props` | `4b827e4bd478d714…` | 2026-11-02T18:39:30 |
| `T14.s1_rx_ingredients` | `120dd4a0c93f51cc…` | 2026-11-02T18:39:31 |
| `T14.s1_rx_reverse_1819` | `ccc41541d6651e1e…` | 2026-11-02T18:39:32 |
| `T14.s2_ndc` | `e54c4729864f25db…` | 2026-11-02T18:39:33 |
| `T14.s3_drugsfda` | `df3de8b5611af00a…` | 2026-11-02T18:39:34 |
| `T14.s4_label` | `724c69111fd420cb…` | 2026-11-02T18:39:34 |
| `T14.s5_srlc_detail` | `fdd617bc8a32f1ef…` | 2026-11-02T18:39:36 |
| `T14.s5_srlc_search` | `91f80f9d64f4454a…` | 2026-11-02T18:39:35 |
| `T14.s6_faers_brand_reactions` | `3a9657c0cbf445a8…` | 2026-11-02T18:39:39 |
| `T14.s6_faers_brand_total` | `11e5c12fa046c803…` | 2026-11-02T18:39:38 |
| `T14.s6_faers_substance` | `375cf5b450684b4d…` | 2026-11-02T18:39:37 |
| `T14.s6_faers_total` | `b59fcb547738955c…` | 2026-11-02T18:39:38 |
| `T14.s7_recall_app` | `e46a6f162144ea65…` | 2026-11-02T18:39:40 |
| `T14.s8_trial` | `e718e3417226854b…` | 2026-11-02T18:39:41 |
| `T14.s8_trials_search` | `0a98d4dc97509b4e…` | 2026-11-02T18:39:41 |
| `T14.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:39:41 |

Full records: [claude/traces/T14.jsonl](../claude/traces/T14.jsonl) · checks: [verification/T14.json](../verification/T14.json) · questions: [shared/questions/T14.json](../shared/questions/T14.json)
