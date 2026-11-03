# T27 · Synthroid (thyroid)

**Status:** verified against sources (111/111 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:42Z – 2026-11-02T18:42Z · questions sha256 `6eca768d2379…`

## The trace in one line
Synthroid → RxNorm 224920 (levothyroxine (10582)) → package 0074-3727-19 under NDA021402 → DailyMed label 1e11ad30-1041-4520-10b0-8f9d30d30fcc v1537 (effective 20240220) → SrLC 08/30/2022 → 6794 FAERS reports name it in 2025 → recall D-0088-2024 → trial NCT00388297.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 224920 (BN); ingredient(s) levothyroxine (10582); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0074-3727-19: 1000 TABLET in 1 BOTTLE (0074-3727-19); labeler AbbVie Inc.; category NDA; application NDA021402 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ABBVIE; 12 product(s): 001 TABLET 0.025MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 002 TABLET 0.05MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 003 TABLET 0.075MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 004 TABLET 0.088MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 005 TABLET 0.1MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 006 TABLET 0.112MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 007 TABLET 0.125MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 008 TABLET 0.137MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 009 TABLET 0.15MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 010 TABLET 0.175MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 011 TABLET 0.3MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium; 012 TABLET 0.2MG **See current Annual Edition, 1.8 Description of Special Situations, Levothyroxine Sodium | Same application number as S2 |
| S4 | DailyMed | In '5. 4 Acute Adrenal Crisis in Patients with Concomitant Adrenal Insufficiency', what role does 'replacement glucocorticoids prior to initiating treatment with SYNTHROID' play? | **administration_instruction** | Quote: "Treat patients with adrenal insufficiency with replacement glucocorticoids prior to initiating treatment with SYNTHROID" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 08/30/2022 SUPPL-36, 5.1 Serious Risks Related to Overtreatment or Undertreatment with SYNTHROID | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 6794 reports name SYNTHROID; 16477 list LEVOTHYROXINE SODIUM (any product) | Top-10 terms checked against S4 label: 6 found, 4 not found |
| S7 | FDA enforcement | Any recall? | D-0088-2024 (Class III, reported status 'Ongoing', 20231115): Labeling: Wrong Barcode- One (1) of every forty (40) unit dose blister will contain incorrect barcode information that causes a 125mcg unit … | Record text names package 0074-3727-19: **False** (application-level query, 5 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00388297 (COMPLETED), EG000 'Levothyroxine for Subclinical Hypothyroidism': serious AEs 4 of 339 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, DRUG INEFFECTIVE, ASTHENIA, DIZZINESS. Found in label: FATIGUE, NAUSEA, HEADACHE, DIARRHOEA, PAIN, ARTHRALGIA.
- **Recall:** D-0088-2024 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (08/30/2022) is reflected in the captured DailyMed label.

## Traps this trace shows
- Adrenal insufficiency in the same sentence is an underlying condition; acute adrenal crisis is the harm.
- Query scope changes the count: 6794 brand-named vs 16477 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'ABBVIE' (Drugs@FDA) vs labeler 'AbbVie Inc.' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T27.s1_rx_brand` | `2ffac8a7c1069357…` | 2026-11-02T18:42:17 |
| `T27.s1_rx_brand_props` | `dda1da498ec589e2…` | 2026-11-02T18:42:17 |
| `T27.s1_rx_ingredients` | `9868a7d0b383767c…` | 2026-11-02T18:42:17 |
| `T27.s1_rx_reverse_10582` | `799f6f32780fbb29…` | 2026-11-02T18:42:18 |
| `T27.s2_ndc` | `7e1a7cacde1cfeec…` | 2026-11-02T18:42:19 |
| `T27.s3_drugsfda` | `e894cd9dfc6e935f…` | 2026-11-02T18:42:19 |
| `T27.s4_label` | `de366bdd1a38c827…` | 2026-11-02T18:42:20 |
| `T27.s5_srlc_detail` | `26ac55ef6b2b88c8…` | 2026-11-02T18:42:22 |
| `T27.s5_srlc_search` | `43fdcca555a7e78a…` | 2026-11-02T18:42:21 |
| `T27.s6_faers_brand_reactions` | `70f8fd926420f109…` | 2026-11-02T18:42:25 |
| `T27.s6_faers_brand_total` | `b570ed116510927c…` | 2026-11-02T18:42:24 |
| `T27.s6_faers_substance` | `2d7549e29bd92190…` | 2026-11-02T18:42:23 |
| `T27.s6_faers_total` | `f16101a99a34ceac…` | 2026-11-02T18:42:24 |
| `T27.s7_recall_app` | `b5743c59323034d7…` | 2026-11-02T18:42:26 |
| `T27.s8_trial` | `cdc0d963014a994e…` | 2026-11-02T18:42:27 |
| `T27.s8_trials_search` | `9dd431ba13662205…` | 2026-11-02T18:42:26 |
| `T27.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:42:27 |

Full records: [claude/traces/T27.jsonl](../claude/traces/T27.jsonl) · checks: [verification/T27.json](../verification/T27.json) · questions: [shared/questions/T27.json](../shared/questions/T27.json)
