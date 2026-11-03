# T12 · Janumet (DPP-4 combination)

**Status:** verified against sources (114/114 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:39Z – 2026-11-02T18:39Z · questions sha256 `5f4e69582ca1…`

## The trace in one line
Janumet → RxNorm 1372738 (metformin (6809), sitagliptin (593411)) → package 0006-0575-03 under NDA022044 → DailyMed label d19c7ed0-ad5c-426e-b2df-722508f97d67 v61 (effective 20260811) → SrLC 08/11/2026 → 505 FAERS reports name it in 2025 → recall D-0746-2022 → trial NCT01709305.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 1372738 (BN); ingredient(s) metformin (6809), sitagliptin (593411); multi-ingredient: True | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0006-0575-03: 2 BOTTLE in 1 CARTON (0006-0575-03)  / 14 TABLET, FILM COATED in 1 BOTTLE (0006-0575-02); labeler Merck Sharp & Dohme LLC; category NDA; application NDA022044 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor MSD SUB MERCK; 2 product(s): 001 TABLET 500MG, EQ 50MG BASE; 002 TABLET 1GM, EQ 50MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.5 Vitamin B12 Deficiency', what role does 'inadequate vitamin B12 or calcium intake or absorption' play? | **underlying_condition_or_risk_factor** | Quote: "Certain individuals (those with inadequate vitamin B12 or calcium intake or absorption) appear to be predisposed to developing subnormal vitamin B12 levels." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 08/11/2026 SUPPL-58, 5.1 Lactic Acidosis | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 505 reports name JANUMET; 704 list METFORMIN HYDROCHLORIDE\SITAGLIPTIN PHOSPHATE (any product) | Top-10 terms checked against S4 label: 5 found, 5 not found |
| S7 | FDA enforcement | Any recall? | D-0746-2022 (Class II, reported status 'Terminated', 20220413): Presence of foreign substance: Presence of stainless steel particulates in tablets. | Record text names package 0006-0575-03: **True** (application-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01709305 (COMPLETED), EG000 'Phase 1: Sitagliptin + Metformin': serious AEs 63 of 5527 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** PRODUCT DOSE OMISSION ISSUE, ACUTE KIDNEY INJURY, FATIGUE, OFF LABEL USE, BLOOD GLUCOSE INCREASED. Found in label: LACTIC ACIDOSIS, DIARRHOEA, NAUSEA, VOMITING, HYPOGLYCAEMIA.
- **Recall:** D-0746-2022 names this exact package. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (08/11/2026) is reflected in the captured DailyMed label.

## Traps this trace shows
- The reaction in this passage is the vitamin B12 decrease; the target is the predisposing factor. Applies to the metformin component of this combination product.
- Query scope changes the count: 505 brand-named vs 704 substance-level reports.
- Sponsor 'MSD SUB MERCK' (Drugs@FDA) vs labeler 'Merck Sharp & Dohme LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T12.s1_rx_brand` | `bf83812011591e93…` | 2026-11-02T18:39:07 |
| `T12.s1_rx_brand_props` | `9f7b43b2355cdc32…` | 2026-11-02T18:39:07 |
| `T12.s1_rx_ingredients` | `d2f35a280fc4cd27…` | 2026-11-02T18:39:07 |
| `T12.s1_rx_reverse_593411` | `805aed3051e2ee1f…` | 2026-11-02T18:39:08 |
| `T12.s1_rx_reverse_6809` | `56477ed1d66e9c87…` | 2026-11-02T18:39:08 |
| `T12.s2_ndc` | `b6d99cae1f91242a…` | 2026-11-02T18:39:09 |
| `T12.s3_drugsfda` | `0201ba4c1acd102e…` | 2026-11-02T18:39:10 |
| `T12.s4_label` | `431643511f3d4e94…` | 2026-11-02T18:39:10 |
| `T12.s5_srlc_detail` | `cdc4b568645b3191…` | 2026-11-02T18:39:12 |
| `T12.s5_srlc_search` | `d06ea1617856c5f2…` | 2026-11-02T18:39:12 |
| `T12.s6_faers_brand_reactions` | `0feb41e6e674809b…` | 2026-11-02T18:39:16 |
| `T12.s6_faers_brand_total` | `4c5f451d8b8e19ae…` | 2026-11-02T18:39:15 |
| `T12.s6_faers_substance` | `26af5298536df7b3…` | 2026-11-02T18:39:13 |
| `T12.s6_faers_total` | `cb96bc9b25ec02d6…` | 2026-11-02T18:39:14 |
| `T12.s7_recall_app` | `75886c19f8cde8fa…` | 2026-11-02T18:39:16 |
| `T12.s8_trial` | `ad2211c7fe4d7631…` | 2026-11-02T18:39:17 |
| `T12.s8_trials_search` | `3e51045bb6675cf1…` | 2026-11-02T18:39:17 |
| `T12.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:39:18 |

Full records: [claude/traces/T12.jsonl](../claude/traces/T12.jsonl) · checks: [verification/T12.json](../verification/T12.json) · questions: [shared/questions/T12.json](../shared/questions/T12.json)
