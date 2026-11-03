# T18 · Zoloft (SSRI)

**Status:** verified against sources (117/117 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:40Z – 2026-11-02T18:40Z · questions sha256 `46e54a3a91ca…`

## The trace in one line
Zoloft → RxNorm 82728 (sertraline (36437)) → package 58151-574-93 under NDA019839 → DailyMed label fda754f6-d0f3-4dce-a17a-927d64f912f7 v7 (effective 20230808) → SrLC 08/18/2023 → 2312 FAERS reports name it in 2025 → recall D-0227-2026 → trial NCT00666757.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 82728 (BN); ingredient(s) sertraline (36437); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 58151-574-93: 30 TABLET, FILM COATED in 1 BOTTLE (58151-574-93); labeler Viatris Specialty LLC; category NDA; application NDA019839 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor VIATRIS; 5 product(s): 001 TABLET EQ 50MG BASE; 002 TABLET EQ 100MG BASE; 003 TABLET EQ 150MG BASE **Federal Register determination that product was not discontinued or withdrawn for safety or effectiveness reasons**; 004 TABLET EQ 200MG BASE **Federal Register determination that product was not discontinued or withdrawn for safety or effectiveness reasons**; 005 TABLET EQ 25MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.7 Angle-Closure Glaucoma', what role does 'anatomically narrow angles' play? | **underlying_condition_or_risk_factor** | Quote: "may trigger an angle closure attack in a patient with anatomically narrow angles who does not have a patent iridectomy" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 08/18/2023 SUPPL-108, 5.2 Serotonin Syndrome | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 2312 reports name ZOLOFT; 14104 list SERTRALINE HYDROCHLORIDE (any product) | Top-10 terms checked against S4 label: 8 found, 2 not found |
| S7 | FDA enforcement | Any recall? | D-0227-2026 (Class II, reported status 'Ongoing', 20251217): Defective container - seal not adhering to bottles | Record text names package 58151-574-93: **False** (ingredient-level query, 2 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00666757 (COMPLETED), EG004 'Sertraline': serious AEs 2 of 119 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, DRUG INEFFECTIVE. Found in label: NAUSEA, FATIGUE, HEADACHE, DIARRHOEA, ANXIETY, DIZZINESS, VOMITING, PAIN.
- **Recall:** D-0227-2026 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (08/18/2023) is reflected in the captured DailyMed label.

## Traps this trace shows
- Could be read as contraindicated_population ('Avoid use ... in patients with untreated anatomically narrow angles'), but the label says 'avoid', not 'contraindicated'.
- Query scope changes the count: 2312 brand-named vs 14104 substance-level reports.
- Sponsor 'VIATRIS' (Drugs@FDA) vs labeler 'Viatris Specialty LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T18.s1_rx_brand` | `a088321edcebc5a3…` | 2026-11-02T18:40:23 |
| `T18.s1_rx_brand_props` | `8595756921c8a6bb…` | 2026-11-02T18:40:23 |
| `T18.s1_rx_ingredients` | `da55acaa7f68609b…` | 2026-11-02T18:40:23 |
| `T18.s1_rx_reverse_36437` | `162eac143c3a7b34…` | 2026-11-02T18:40:24 |
| `T18.s2_ndc` | `0e0351a86340bdb6…` | 2026-11-02T18:40:24 |
| `T18.s3_drugsfda` | `f51bb651f7f5aac2…` | 2026-11-02T18:40:25 |
| `T18.s4_label` | `42dcbaf853ab7a47…` | 2026-11-02T18:40:26 |
| `T18.s5_srlc_detail` | `f6d9090873f66cc5…` | 2026-11-02T18:40:28 |
| `T18.s5_srlc_search` | `1f3be08718f5947d…` | 2026-11-02T18:40:27 |
| `T18.s6_faers_brand_reactions` | `944b8414e684f28a…` | 2026-11-02T18:40:31 |
| `T18.s6_faers_brand_total` | `950f52bca18c01b8…` | 2026-11-02T18:40:30 |
| `T18.s6_faers_substance` | `94b68c8454691b76…` | 2026-11-02T18:40:29 |
| `T18.s6_faers_total` | `2a98caf5adf1014d…` | 2026-11-02T18:40:30 |
| `T18.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:40:32 |
| `T18.s7_recall_ingredient` | `c0a6564f7669362a…` | 2026-11-02T18:40:32 |
| `T18.s8_trial` | `9bc8114e41159439…` | 2026-11-02T18:40:33 |
| `T18.s8_trials_search` | `d55fad81599e0db5…` | 2026-11-02T18:40:33 |
| `T18.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:40:34 |

Full records: [claude/traces/T18.jsonl](../claude/traces/T18.jsonl) · checks: [verification/T18.json](../verification/T18.json) · questions: [shared/questions/T18.json](../shared/questions/T18.json)
