# T19 · Cipro (fluoroquinolone)

**Status:** verified against sources (116/116 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:40Z – 2026-11-02T18:40Z · questions sha256 `fd10ef9ac76d…`

## The trace in one line
Cipro → RxNorm 203563 (ciprofloxacin (2551)) → package 50419-754-01 under NDA019537 → DailyMed label 888dc7f9-ad9c-4c00-8d50-8ddfd9bd27c0 v32 (effective 20260302) → SrLC 09/20/2024 → 402 FAERS reports name it in 2025 → recall D-0626-2025 → trial NCT03354598.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 203563 (BN); ingredient(s) ciprofloxacin (2551); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 50419-754-01: 100 TABLET, FILM COATED in 1 BOTTLE, PLASTIC (50419-754-01); labeler Bayer HealthCare Pharmaceuticals Inc.; category NDA; application NDA019537 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor BAYER HLTHCARE; 3 product(s): 002 TABLET EQ 250MG BASE; 003 TABLET EQ 500MG BASE; 004 TABLET EQ 750MG BASE **Federal Register determination that product was not discontinued or withdrawn for safety or effectiveness reasons** | Same application number as S2 |
| S4 | DailyMed | In '5.14 Photosensitivity/Phototoxicity', what role does 'sun or UV light exposure' play? | **exposure_factor** | Quote: "can be associated with the use of quinolones including CIPRO after sun or UV light exposure" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 09/20/2024 SUPPL-95, 5.7 Hypersensitivity Reactions | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 402 reports name CIPRO; 1061 list CIPROFLOXACIN HYDROCHLORIDE (any product) | Top-10 terms checked against S4 label: 7 found, 3 not found |
| S7 | FDA enforcement | Any recall? | D-0626-2025 (Class II, reported status 'Ongoing', 20250917): Temperature Abuse | Record text names package 50419-754-01: **False** (ingredient-level query, 9 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT03354598 (COMPLETED), EG001 'Ciprofloxacin': serious AEs 2 of 827 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, FATIGUE, DRUG INTOLERANCE. Found in label: HEADACHE, DIARRHOEA, NAUSEA, DYSPNOEA, PAIN, ARTHRALGIA, HYPERSENSITIVITY.
- **Recall:** D-0626-2025 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (09/20/2024) is reflected in the captured DailyMed label.

## Traps this trace shows
- The reaction is photosensitivity/phototoxicity; 'avoid excessive exposure' is the related instruction.
- Query scope changes the count: 402 brand-named vs 1061 substance-level reports.
- Sponsor 'BAYER HLTHCARE' (Drugs@FDA) vs labeler 'Bayer HealthCare Pharmaceuticals Inc.' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T19.s1_rx_brand` | `1f4189ce959a873b…` | 2026-11-02T18:40:34 |
| `T19.s1_rx_brand_props` | `8f24c21109cb71e0…` | 2026-11-02T18:40:35 |
| `T19.s1_rx_ingredients` | `8a6dabb65555919f…` | 2026-11-02T18:40:35 |
| `T19.s1_rx_reverse_2551` | `6f6e66b3041a781f…` | 2026-11-02T18:40:36 |
| `T19.s2_ndc` | `0179ecf99bc0f745…` | 2026-11-02T18:40:36 |
| `T19.s3_drugsfda` | `68e10cf9b0faa19b…` | 2026-11-02T18:40:37 |
| `T19.s4_label` | `e4f88d00e95859c7…` | 2026-11-02T18:40:38 |
| `T19.s5_srlc_detail` | `1216bdb1e5b5afde…` | 2026-11-02T18:40:40 |
| `T19.s5_srlc_search` | `5c934cf06225706e…` | 2026-11-02T18:40:39 |
| `T19.s6_faers_brand_reactions` | `2c7ce2067f91097a…` | 2026-11-02T18:40:45 |
| `T19.s6_faers_brand_total` | `56eade3df73bfbb9…` | 2026-11-02T18:40:44 |
| `T19.s6_faers_substance` | `a9dc0bd6872d55a1…` | 2026-11-02T18:40:41 |
| `T19.s6_faers_total` | `e2cfd9802cea64e9…` | 2026-11-02T18:40:42 |
| `T19.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:40:45 |
| `T19.s7_recall_ingredient` | `45502f2c6364aef9…` | 2026-11-02T18:40:46 |
| `T19.s8_trial` | `083bd2d41f80fe6c…` | 2026-11-02T18:40:47 |
| `T19.s8_trials_search` | `4633dc32e718cc9c…` | 2026-11-02T18:40:47 |
| `T19.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:40:48 |

Full records: [claude/traces/T19.jsonl](../claude/traces/T19.jsonl) · checks: [verification/T19.json](../verification/T19.json) · questions: [shared/questions/T19.json](../shared/questions/T19.json)
