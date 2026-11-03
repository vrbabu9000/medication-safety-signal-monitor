# T29 · Truvada (antiretroviral combination)

**Status:** verified against sources (113/113 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:42Z – 2026-11-02T18:42Z · questions sha256 `9e8370910349…`

## The trace in one line
Truvada → RxNorm 495430 (emtricitabine (276237), tenofovir disoproxil (300195)) → package 61958-0701-1 under NDA021752 → DailyMed label 54e82b13-a037-49ed-b4b3-030b37c0ecdd v32 (effective 20250716) → SrLC 06/23/2020 → 1333 FAERS reports name it in 2025 → recall D-0013-2015 → trial NCT00557245.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 495430 (BN); ingredient(s) emtricitabine (276237), tenofovir disoproxil (300195); multi-ingredient: True | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 61958-0701-1: 30 TABLET, FILM COATED in 1 BOTTLE, PLASTIC (61958-0701-1); labeler Gilead Sciences, Inc; category NDA; application NDA021752 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor GILEAD; 4 product(s): 001 TABLET 200MG, 300MG; 002 TABLET 100MG, 150MG; 003 TABLET 133MG, 200MG; 004 TABLET 167MG, 250MG | Same application number as S2 |
| S4 | DailyMed | In '4 CONTRAINDICATIONS', what role does 'individuals with unknown or positive HIV-1 status' play? | **contraindicated_population** | Quote: "TRUVADA for HIV-1 PrEP is contraindicated in individuals with unknown or positive HIV-1 status" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 06/23/2020 SUPPL-61, 5.1 Severe Acute Exacerbation of Hepatitis B in Individuals with HBV Infection | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1333 reports name TRUVADA; 1506 list EMTRICITABINE\TENOFOVIR DISOPROXIL FUMARATE (any product) | Top-10 terms checked against S4 label: 4 found, 6 not found |
| S7 | FDA enforcement | Any recall? | D-0013-2015 (Class III, reported status 'Terminated', 20141015): Presence of Foreign Substance: Truvada was found to contain small red silicone rubber particulates. | Record text names package 61958-0701-1: **True** (application-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00557245 (COMPLETED), EG000 'Tenofovir Disoproxil Fumarate (TDF)': serious AEs 118 of 1584 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** BONE DENSITY DECREASED, TOOTH LOSS, OSTEONECROSIS, MULTIPLE FRACTURES, OSTEOPENIA, ACUTE KIDNEY INJURY. Found in label: RENAL FAILURE, CHRONIC KIDNEY DISEASE, BONE LOSS, OSTEOPOROSIS.
- **Recall:** D-0013-2015 names this exact package. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (06/23/2020) is reflected in the captured DailyMed label.

## Traps this trace shows
- Scoped to the PrEP indication only; Truvada is used for HIV-1 treatment in positive patients.
- Query scope changes the count: 1333 brand-named vs 1506 substance-level reports.
- Sponsor 'GILEAD' (Drugs@FDA) vs labeler 'Gilead Sciences, Inc' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T29.s1_rx_brand` | `bda676407106f4ed…` | 2026-11-02T18:42:41 |
| `T29.s1_rx_brand_props` | `644b9db082fb92aa…` | 2026-11-02T18:42:42 |
| `T29.s1_rx_ingredients` | `04b2310659e9b7ca…` | 2026-11-02T18:42:42 |
| `T29.s1_rx_reverse_276237` | `0878306baf994020…` | 2026-11-02T18:42:43 |
| `T29.s1_rx_reverse_300195` | `aef98782a1831b69…` | 2026-11-02T18:42:43 |
| `T29.s2_ndc` | `0c153960fca55a4f…` | 2026-11-02T18:42:44 |
| `T29.s3_drugsfda` | `9879b796871a782c…` | 2026-11-02T18:42:45 |
| `T29.s4_label` | `7a2ebb2b5d89aab8…` | 2026-11-02T18:42:45 |
| `T29.s5_srlc_detail` | `47b28f9185af3bc9…` | 2026-11-02T18:42:47 |
| `T29.s5_srlc_search` | `3968a3d49771ad27…` | 2026-11-02T18:42:47 |
| `T29.s6_faers_brand_reactions` | `23a462b289d63050…` | 2026-11-02T18:42:50 |
| `T29.s6_faers_brand_total` | `5464c9e628dab381…` | 2026-11-02T18:42:49 |
| `T29.s6_faers_substance` | `af0bc685ab0ffde9…` | 2026-11-02T18:42:48 |
| `T29.s6_faers_total` | `d9c134e8fd43b721…` | 2026-11-02T18:42:49 |
| `T29.s7_recall_app` | `fd1d12501c960f13…` | 2026-11-02T18:42:51 |
| `T29.s8_trial` | `82a1ddf9d8ad3772…` | 2026-11-02T18:42:52 |
| `T29.s8_trials_search` | `4737c66d55bca9d6…` | 2026-11-02T18:42:51 |
| `T29.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:42:52 |

Full records: [claude/traces/T29.jsonl](../claude/traces/T29.jsonl) · checks: [verification/T29.json](../verification/T29.json) · questions: [shared/questions/T29.json](../shared/questions/T29.json)
