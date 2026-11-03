# T06 · Vytorin (statin combination)

**Status:** verified against sources (119/119 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:37Z – 2026-11-02T18:38Z · questions sha256 `867ce6c18a4f…`

## The trace in one line
Vytorin → RxNorm 495215 (ezetimibe (341248), simvastatin (36567)) → package 78206-174-01 under NDA021687 → DailyMed label 89b860d2-de83-468e-b7e8-76aeec2edca2 v9 (effective 20260121) → SrLC 03/28/2024 → 77 FAERS reports name it in 2025 → recall D-0462-2025 → trial NCT00202878.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 495215 (BN); ingredient(s) ezetimibe (341248), simvastatin (36567); multi-ingredient: True | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 78206-174-01: 30 TABLET in 1 BOTTLE (78206-174-01); labeler Organon LLC; category NDA; application NDA021687 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor ORGANON; 4 product(s): 001 TABLET 10MG, 10MG; 002 TABLET 10MG, 20MG; 003 TABLET 10MG, 40MG; 004 TABLET 10MG, 80MG | Same application number as S2 |
| S4 | DailyMed | In '4 CONTRAINDICATIONS', what role does 'decompensated cirrhosis' play? | **contraindicated_population** | Quote: "Acute liver failure or decompensated cirrhosis [see Warnings and Precautions (5.3)]." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 03/28/2024 SUPPL-66, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 77 reports name VYTORIN; 291 list EZETIMIBE\SIMVASTATIN (any product) | Top-10 terms checked against S4 label: 6 found, 4 not found |
| S7 | FDA enforcement | Any recall? | D-0462-2025 (Class III, reported status 'Ongoing', 20250618): Failed Impurities/Degradation Specifications: Out of Specification (OOS) for related substances test for Anhydro Simvastatin at the 06-month… | Record text names package 78206-174-01: **False** (ingredient-level query, 9 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00202878 (COMPLETED), EG000 'Ezetimide/Simvastatin': serious AEs 3640 of 9067 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, PRODUCT DOSE OMISSION ISSUE, HOT FLUSH, SLEEP DEFICIT. Found in label: FATIGUE, DIARRHOEA, DYSPNOEA, PAIN, CONSTIPATION, MALAISE.
- **Recall:** D-0462-2025 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (03/28/2024) is reflected in the captured DailyMed label.

## Traps this trace shows
- Could be read as an underlying condition; it is classed by the section's explicit 'contraindicated' wording. Strong CYP3A4 inhibitors in the same list are contraindicated co-medications, a different class.
- Query scope changes the count: 77 brand-named vs 291 substance-level reports.
- Sponsor 'ORGANON' (Drugs@FDA) vs labeler 'Organon LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T06.s1_rx_brand` | `fd51a3b798c36a2b…` | 2026-11-02T18:37:56 |
| `T06.s1_rx_brand_props` | `69c75f0a161f7c16…` | 2026-11-02T18:37:56 |
| `T06.s1_rx_ingredients` | `cf9c542371cf5736…` | 2026-11-02T18:37:57 |
| `T06.s1_rx_reverse_341248` | `11c0a35371cf68bf…` | 2026-11-02T18:37:57 |
| `T06.s1_rx_reverse_36567` | `3713560ad7831d14…` | 2026-11-02T18:37:57 |
| `T06.s2_ndc` | `748699d1fb1ff8a1…` | 2026-11-02T18:37:58 |
| `T06.s3_drugsfda` | `0a7d157bd4d9b607…` | 2026-11-02T18:37:59 |
| `T06.s4_label` | `dc2905f23a8db2db…` | 2026-11-02T18:37:59 |
| `T06.s5_srlc_detail` | `bcb7f0402860a077…` | 2026-11-02T18:38:02 |
| `T06.s5_srlc_search` | `9a073a84c52440db…` | 2026-11-02T18:38:01 |
| `T06.s6_faers_brand_reactions` | `2a970ce49a8f1fe6…` | 2026-11-02T18:38:05 |
| `T06.s6_faers_brand_total` | `5d8eb3be08bc3409…` | 2026-11-02T18:38:04 |
| `T06.s6_faers_substance` | `ecadf407a636cc42…` | 2026-11-02T18:38:03 |
| `T06.s6_faers_total` | `1088a28f91d8c2b8…` | 2026-11-02T18:38:04 |
| `T06.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:38:06 |
| `T06.s7_recall_ingredient` | `bc662ce28011361c…` | 2026-11-02T18:38:07 |
| `T06.s8_trial` | `b46bef768d49a426…` | 2026-11-02T18:38:08 |
| `T06.s8_trials_search` | `26561cac6d867955…` | 2026-11-02T18:38:07 |
| `T06.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:38:08 |

Full records: [claude/traces/T06.jsonl](../claude/traces/T06.jsonl) · checks: [verification/T06.json](../verification/T06.json) · questions: [shared/questions/T06.json](../shared/questions/T06.json)
