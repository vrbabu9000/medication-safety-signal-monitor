# T10 · Rybelsus (GLP-1)

**Status:** verified against sources (111/111 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:38Z – 2026-11-02T18:38Z · questions sha256 `54925005a6fe…`

## The trace in one line
Rybelsus → RxNorm 2200645 (semaglutide (1991302)) → package 0169-4303-30 under NDA213051 → DailyMed label 27f15fac-7d98-4114-a2ec-92494a91da98 v14 (effective 20260130) → SrLC 01/30/2026 → 1567 FAERS reports name it in 2025 → recall D-0536-2021 → trial NCT03574597.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 2200645 (BN); ingredient(s) semaglutide (1991302); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0169-4303-30: 30 TABLET in 1 BOTTLE, PLASTIC (0169-4303-30); labeler Novo Nordisk Pharmaceutical Industries, LP; category NDA; application NDA213051 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor NOVO; 6 product(s): 001 TABLET 3MG; 002 TABLET 7MG; 003 TABLET 14MG; 004 TABLET 1.5MG; 005 TABLET 4MG; 006 TABLET 9MG | Same application number as S2 |
| S4 | DailyMed | In '5.9 Pulmonary Aspiration During General Anesthesia or Deep Sedation', what role does 'general anesthesia or deep sedation' play? | **exposure_factor** | Quote: "undergoing elective surgeries or procedures requiring general anesthesia or deep sedation" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 01/30/2026 SUPPL-30, 5.2 Acute Pancreatitis | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1567 reports name RYBELSUS; 27462 list SEMAGLUTIDE (any product) | Top-10 terms checked against S4 label: 6 found, 4 not found |
| S7 | FDA enforcement | Any recall? | D-0536-2021 (Class II, reported status 'Terminated', 20210602): CGMP Deviations: Intermittent exposure to temperature excursion during storage. | Record text names package 0169-4303-30: **False** (application-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT03574597 (COMPLETED), EG000 'Semaglutide': serious AEs 2941 of 8803 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** IMPAIRED GASTRIC EMPTYING, OFF LABEL USE, WEIGHT DECREASED, FATIGUE. Found in label: NAUSEA, VOMITING, DIARRHOEA, CONSTIPATION, DECREASED APPETITE, ABDOMINAL PAIN.
- **Recall:** D-0536-2021 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (01/30/2026) is reflected in the captured DailyMed label.

## Traps this trace shows
- Pulmonary aspiration is the outcome (a reaction); the procedure is the exposure. The label says data are insufficient to recommend mitigation.
- Query scope changes the count: 1567 brand-named vs 27462 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'NOVO' (Drugs@FDA) vs labeler 'Novo Nordisk Pharmaceutical Industries, LP' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T10.s1_rx_brand` | `9c10ef31af5e8d30…` | 2026-11-02T18:38:43 |
| `T10.s1_rx_brand_props` | `bbd08d47d0ab0cc7…` | 2026-11-02T18:38:43 |
| `T10.s1_rx_ingredients` | `93284efd4bb6a2fb…` | 2026-11-02T18:38:44 |
| `T10.s1_rx_reverse_1991302` | `c78e014967cb4c7d…` | 2026-11-02T18:38:45 |
| `T10.s2_ndc` | `5ad25f97bf703b3a…` | 2026-11-02T18:38:46 |
| `T10.s3_drugsfda` | `d117d48b587eefd2…` | 2026-11-02T18:38:47 |
| `T10.s4_label` | `fb90194667fc6232…` | 2026-11-02T18:38:47 |
| `T10.s5_srlc_detail` | `41dc5f685fc3388f…` | 2026-11-02T18:38:49 |
| `T10.s5_srlc_search` | `79bd221711652cf4…` | 2026-11-02T18:38:48 |
| `T10.s6_faers_brand_reactions` | `d2cfbc1f0457f684…` | 2026-11-02T18:38:52 |
| `T10.s6_faers_brand_total` | `b89fe800a422f266…` | 2026-11-02T18:38:51 |
| `T10.s6_faers_substance` | `c3a00a9cfde68770…` | 2026-11-02T18:38:50 |
| `T10.s6_faers_total` | `5133c0c214f90fac…` | 2026-11-02T18:38:51 |
| `T10.s7_recall_app` | `e343611761dfdeb6…` | 2026-11-02T18:38:53 |
| `T10.s8_trial` | `226cc3e2646747f9…` | 2026-11-02T18:38:54 |
| `T10.s8_trials_search` | `c136c32bc237c716…` | 2026-11-02T18:38:53 |
| `T10.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:38:54 |

Full records: [claude/traces/T10.jsonl](../claude/traces/T10.jsonl) · checks: [verification/T10.json](../verification/T10.json) · questions: [shared/questions/T10.json](../shared/questions/T10.json)
