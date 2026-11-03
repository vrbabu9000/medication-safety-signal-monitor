# T15 · Lamictal (antiepileptic)

**Status:** verified against sources (112/112 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:39Z – 2026-11-02T18:39Z · questions sha256 `2135fba3bd69…`

## The trace in one line
Lamictal → RxNorm 196502 (lamotrigine (28439)) → package 0173-0594-02 under NDA020241 → DailyMed label d7e3572d-56fe-4727-2bb4-013ccca22678 v45 (effective 20251010) → SrLC 10/10/2025 → 2383 FAERS reports name it in 2025 → recall D-1329-2022 → trial NCT00277212.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 196502 (BN); ingredient(s) lamotrigine (28439); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0173-0594-02: 1 BLISTER PACK in 1 PACKAGE, COMBINATION (0173-0594-02)  / 1 KIT in 1 BLISTER PACK; labeler GlaxoSmithKline LLC; category NDA; application NDA020241 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor GLAXOSMITHKLINE LLC; 6 product(s): 001 TABLET 100MG; 002 TABLET 150MG; 003 TABLET 200MG; 004 TABLET 250MG **Federal Register determination that product was not discontinued or withdrawn for safety or effectiveness reasons**; 005 TABLET 25MG; 006 TABLET 50MG **Federal Register determination that product was not discontinued or withdrawn for safety or effectiveness reasons** | Same application number as S2 |
| S4 | DailyMed | In '5.9 Concomitant Use with Estrogen-Containing Products, Including Oral Contraceptives', what role does 'estrogen-containing oral contraceptives' play? | **co_medication_risk_factor** | Quote: "Some estrogen-containing oral contraceptives have been shown to decrease serum concentrations of lamotrigine" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 10/10/2025 SUPPL-68, 5.1 Serious Skin Rashes [see Boxed Warning] | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 2383 reports name LAMICTAL; 7913 list LAMOTRIGINE (any product) | Top-10 terms checked against S4 label: 3 found, 7 not found |
| S7 | FDA enforcement | Any recall? | D-1329-2022 (Class III, reported status 'Terminated', 20220817): Labeling: Label Error on Declared Strength | Record text names package 0173-0594-02: **False** (ingredient-level query, 5 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00277212 (COMPLETED), EG000 'Phase 1: Single-Blind Treatment, Lamotrigine + Aripiprazole': serious AEs 32 of 787 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, MATERNAL EXPOSURE DURING PREGNANCY, DRUG INEFFECTIVE, PEMPHIGUS, SWELLING, TYPE 2 DIABETES MELLITUS, PERICARDITIS. Found in label: RASH, PAIN, SYSTEMIC LUPUS ERYTHEMATOSUS.
- **Recall:** D-1329-2022 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (10/10/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- Dizziness, ataxia and diplopia in the same passage are reactions to raised lamotrigine levels, a different class.
- Query scope changes the count: 2383 brand-named vs 7913 substance-level reports.
- Sponsor 'GLAXOSMITHKLINE LLC' (Drugs@FDA) vs labeler 'GlaxoSmithKline LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T15.s1_rx_brand` | `144bfd21e70105c6…` | 2026-11-02T18:39:42 |
| `T15.s1_rx_brand_props` | `cbff8d1b81e9d4fa…` | 2026-11-02T18:39:42 |
| `T15.s1_rx_ingredients` | `e5b6435b960ecb40…` | 2026-11-02T18:39:43 |
| `T15.s1_rx_reverse_28439` | `9c7f3826ec9a2a87…` | 2026-11-02T18:39:43 |
| `T15.s2_ndc` | `a2c283404fb8adc0…` | 2026-11-02T18:39:44 |
| `T15.s3_drugsfda` | `579038cce8b0922c…` | 2026-11-02T18:39:45 |
| `T15.s4_label` | `8f685ccbdae66691…` | 2026-11-02T18:39:45 |
| `T15.s5_srlc_detail` | `0579963a0db80279…` | 2026-11-02T18:39:49 |
| `T15.s5_srlc_search` | `5a808a7b7040eb58…` | 2026-11-02T18:39:48 |
| `T15.s6_faers_brand_reactions` | `6d8bd9771d9d10cf…` | 2026-11-02T18:39:52 |
| `T15.s6_faers_brand_total` | `ae18c7e87c03b4da…` | 2026-11-02T18:39:51 |
| `T15.s6_faers_substance` | `cd0671b94ebeb4ae…` | 2026-11-02T18:39:50 |
| `T15.s6_faers_total` | `73f09a83574b1254…` | 2026-11-02T18:39:51 |
| `T15.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:39:53 |
| `T15.s7_recall_ingredient` | `11a66ac08ef810fa…` | 2026-11-02T18:39:54 |
| `T15.s8_trial` | `77573228334d5a8e…` | 2026-11-02T18:39:55 |
| `T15.s8_trials_search` | `a7e01ffa15ee34de…` | 2026-11-02T18:39:54 |
| `T15.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:39:55 |

Full records: [claude/traces/T15.jsonl](../claude/traces/T15.jsonl) · checks: [verification/T15.json](../verification/T15.json) · questions: [shared/questions/T15.json](../shared/questions/T15.json)
