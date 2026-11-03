# T24 · Prilosec (PPI)

**Status:** verified against sources (112/112 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:41Z – 2026-11-02T18:41Z · questions sha256 `5daaba4d89d8…`

## The trace in one line
Prilosec → RxNorm 203345 (omeprazole (7646)) → package 70515-610-01 under NDA022056 → DailyMed label b6761f84-53ac-4745-a8c8-1e5427d7e179 v8 (effective 20240319) → SrLC 07/18/2023 → 1174 FAERS reports name it in 2025 → recall D-0466-2021 → trial NCT00141102.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 203345 (BN); ingredient(s) omeprazole (7646); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 70515-610-01: 30 GRANULE, DELAYED RELEASE in 1 CARTON (70515-610-01); labeler Covis Pharma US, Inc; category NDA; application NDA022056 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor AZURITY; 2 product(s): 001 FOR SUSPENSION, DELAYED RELEASE EQ 2.5MG BASE/PACKET; 002 FOR SUSPENSION, DELAYED RELEASE EQ 10MG BASE/PACKET | Same application number as S2 |
| S4 | DailyMed | In '5.10 Interaction with St. John’s Wort or Rifampin', what role does 'St. John’s Wort' play? | **co_medication_risk_factor** | Quote: "Drugs which induce CYP2C19 or CYP3A4 (such as St. John’s Wort or rifampin) can substantially decrease omeprazole concentrations" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 07/18/2023 SUPPL-26, 6.3 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1174 reports name PRILOSEC; 1737 list OMEPRAZOLE MAGNESIUM (any product) | Top-10 terms checked against S4 label: 7 found, 3 not found |
| S7 | FDA enforcement | Any recall? | D-0466-2021 (Class II, reported status 'Terminated', 20210602): CGMP Deviations: Intermittent exposure to temperature excursion during storage. | Record text names package 70515-610-01: **True** (application-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00141102 (COMPLETED), EG001 'Oral Diclofenac Plus Omeprazole': serious AEs 61 of 2237 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, DRUG INEFFECTIVE, DYSPNOEA. Found in label: FATIGUE, NAUSEA, DIARRHOEA, VOMITING, HEADACHE, PAIN, DIZZINESS.
- **Recall:** D-0466-2021 names this exact package. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (07/18/2023) is reflected in the captured DailyMed label.

## Traps this trace shows
- The risk is reduced effect, not a new reaction. The source uses a curly apostrophe.
- Query scope changes the count: 1174 brand-named vs 1737 substance-level reports.
- Sponsor 'AZURITY' (Drugs@FDA) vs labeler 'Covis Pharma US, Inc' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T24.s1_rx_brand` | `63de492f330be521…` | 2026-11-02T18:41:39 |
| `T24.s1_rx_brand_props` | `2e93ad8b03cfa857…` | 2026-11-02T18:41:40 |
| `T24.s1_rx_ingredients` | `bc5b497893467485…` | 2026-11-02T18:41:40 |
| `T24.s1_rx_reverse_7646` | `e0f792f67a93894e…` | 2026-11-02T18:41:41 |
| `T24.s2_ndc` | `ea19d788eec8eab1…` | 2026-11-02T18:41:41 |
| `T24.s3_drugsfda` | `09dcac4c377ff8ad…` | 2026-11-02T18:41:42 |
| `T24.s4_label` | `e0cab1df07d66440…` | 2026-11-02T18:41:43 |
| `T24.s5_srlc_detail` | `0101c1b7e22da2bb…` | 2026-11-02T18:41:45 |
| `T24.s5_srlc_search` | `b541e0fbb80a30ba…` | 2026-11-02T18:41:44 |
| `T24.s6_faers_brand_reactions` | `fa65901656ca74cc…` | 2026-11-02T18:41:48 |
| `T24.s6_faers_brand_total` | `2f591c770edf4588…` | 2026-11-02T18:41:47 |
| `T24.s6_faers_substance` | `3c19096431361516…` | 2026-11-02T18:41:46 |
| `T24.s6_faers_total` | `06aa7e5bbc416726…` | 2026-11-02T18:41:47 |
| `T24.s7_recall_app` | `e32f14e9bc93d625…` | 2026-11-02T18:41:49 |
| `T24.s8_trial` | `3430253130e4ddd7…` | 2026-11-02T18:41:50 |
| `T24.s8_trials_search` | `682d2b41ddffdfe1…` | 2026-11-02T18:41:49 |
| `T24.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:41:50 |

Full records: [claude/traces/T24.jsonl](../claude/traces/T24.jsonl) · checks: [verification/T24.json](../verification/T24.json) · questions: [shared/questions/T24.json](../shared/questions/T24.json)
