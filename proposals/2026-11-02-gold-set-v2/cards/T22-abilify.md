# T22 · Abilify (antipsychotic)

**Status:** verified against sources (113/113 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:41Z – 2026-11-02T18:41Z · questions sha256 `296a369d4390…`

## The trace in one line
Abilify → RxNorm 352393 (aripiprazole (89013)) → package 59148-006-13 under NDA021436 → DailyMed label c040bd1d-45b7-49f2-93ea-aed7220b30ac v73 (effective 20250129) → SrLC 01/22/2025 → 1453 FAERS reports name it in 2025 → recall D-0468-2024 → trial NCT01421342.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 352393 (BN); ingredient(s) aripiprazole (89013); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 59148-006-13: 30 TABLET in 1 BOTTLE, PLASTIC (59148-006-13); labeler Otsuka America Pharmaceutical, Inc.; category NDA; application NDA021436 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor OTSUKA; 6 product(s): 001 TABLET 10MG; 002 TABLET 15MG; 003 TABLET 20MG; 004 TABLET 30MG; 005 TABLET 5MG; 006 TABLET 2MG | Same application number as S2 |
| S4 | DailyMed | In '5.7 Pathological Gambling and Other Compulsive Behaviors', what role does 'urges, particularly for gambling' play? | **reaction_or_warning** | Quote: "patients can experience intense urges, particularly for gambling, and the inability to control these urges while taking aripiprazole" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 01/22/2025 SUPPL-50, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1453 reports name ABILIFY; 5887 list ARIPIPRAZOLE (any product) | Top-10 terms checked against S4 label: 8 found, 2 not found |
| S7 | FDA enforcement | Any recall? | D-0468-2024 (Class III, reported status 'Ongoing', 20240501): Cross Contamination with Other Products | Record text names package 59148-006-13: **False** (application-level query, 5 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01421342 (COMPLETED), EG002 'Augmenting: Antidepressant + Aripiprazole': serious AEs 56 of 505 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, DRUG INEFFECTIVE. Found in label: FATIGUE, WEIGHT INCREASED, NAUSEA, HEADACHE, DIARRHOEA, DIZZINESS, INSOMNIA, TREMOR.
- **Recall:** D-0468-2024 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (01/22/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- The label notes impulse-control symptoms can be associated with the underlying disorder, so causality is not certain in every case.
- Query scope changes the count: 1453 brand-named vs 5887 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'OTSUKA' (Drugs@FDA) vs labeler 'Otsuka America Pharmaceutical, Inc.' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T22.s1_rx_brand` | `9b18d68320aae049…` | 2026-11-02T18:41:14 |
| `T22.s1_rx_brand_props` | `c411550e458347a2…` | 2026-11-02T18:41:14 |
| `T22.s1_rx_ingredients` | `ab8c34b958aef711…` | 2026-11-02T18:41:15 |
| `T22.s1_rx_reverse_89013` | `e69add2d7fc9abf5…` | 2026-11-02T18:41:15 |
| `T22.s2_ndc` | `39f9f449b62940a1…` | 2026-11-02T18:41:16 |
| `T22.s3_drugsfda` | `6d1623460ff9042b…` | 2026-11-02T18:41:17 |
| `T22.s4_label` | `4c35eade13c4f67d…` | 2026-11-02T18:41:18 |
| `T22.s5_srlc_detail` | `fe82d55a58ed1665…` | 2026-11-02T18:41:21 |
| `T22.s5_srlc_search` | `081d822b9699694d…` | 2026-11-02T18:41:19 |
| `T22.s6_faers_brand_reactions` | `104c3c7ecfbc9586…` | 2026-11-02T18:41:24 |
| `T22.s6_faers_brand_total` | `9aa8a3bc512b4ff5…` | 2026-11-02T18:41:23 |
| `T22.s6_faers_substance` | `a8a60aaaf30a8a2e…` | 2026-11-02T18:41:22 |
| `T22.s6_faers_total` | `3b5edb14075335bd…` | 2026-11-02T18:41:22 |
| `T22.s7_recall_app` | `aeda8034a6d18bec…` | 2026-11-02T18:41:25 |
| `T22.s8_trial` | `6774c063da1d53b3…` | 2026-11-02T18:41:26 |
| `T22.s8_trials_search` | `11121abbd53ab432…` | 2026-11-02T18:41:25 |
| `T22.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:41:26 |

Full records: [claude/traces/T22.jsonl](../claude/traces/T22.jsonl) · checks: [verification/T22.json](../verification/T22.json) · questions: [shared/questions/T22.json](../shared/questions/T22.json)
