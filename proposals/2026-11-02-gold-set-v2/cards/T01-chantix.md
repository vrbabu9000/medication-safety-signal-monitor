# T01 · Chantix (smoking cessation)

**Status:** verified against sources (113/113 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:36Z – 2026-11-02T18:37Z · questions sha256 `13057e000886…`

## The trace in one line
Chantix → RxNorm 636230 (varenicline (591622)) → package 0069-0468-56 under NDA021928 → DailyMed label f0ff4f27-5185-4881-a749-c6b7a0ca5696 v49 (effective 20260123) → SrLC 06/01/2018 → 127 FAERS reports name it in 2025 → recall D-0809-2021 → trial NCT01456936.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 636230 (BN); ingredient(s) varenicline (591622); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0069-0468-56: 56 TABLET, FILM COATED in 1 BOTTLE (0069-0468-56); labeler Pfizer Laboratories Div Pfizer Inc; category NDA; application NDA021928 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor PF PRISM CV; 2 product(s): 001 TABLET EQ 0.5MG BASE; 002 TABLET EQ 1MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.2 Seizures', what role does 'a history of seizures' play? | **underlying_condition_or_risk_factor** | Quote: "Weigh this potential risk against the potential benefits before prescribing CHANTIX in patients with a history of seizures or other factors that can lower the seizure threshold." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 06/01/2018 SUPPL-46, 6.1 Clinical Trials Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 127 reports name CHANTIX; 527 list VARENICLINE TARTRATE (any product) | Top-10 terms checked against S4 label: 8 found, 2 not found |
| S7 | FDA enforcement | Any recall? | D-0809-2021 (Class II, reported status 'Ongoing', 20210929): CGMP Deviations: Presence of the N-nitroso-varenicline impurity above FDA s acceptable interim acceptable intake limit | Record text names package 0069-0468-56: **True** (application-level query, 7 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01456936 (COMPLETED), EG000 'Varenicline 1.0 mg BID': serious AEs 39 of 2016 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** DRUG INEFFECTIVE, PRODUCT DOSE OMISSION ISSUE. Found in label: DYSPNOEA, NAUSEA, DIARRHOEA, FATIGUE, CONSTIPATION, HEADACHE, PAIN, DIZZINESS.
- **Recall:** D-0809-2021 names this exact package. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (06/01/2018) is reflected in the captured DailyMed label.

## Traps this trace shows
- Context trap: the same passage reports seizures as an adverse event in patients treated with Chantix (a reaction). Not a contraindication: the label says 'weigh this potential risk', not 'contraindicated'.
- Query scope changes the count: 127 brand-named vs 527 substance-level reports.
- Sponsor 'PF PRISM CV' (Drugs@FDA) vs labeler 'Pfizer Laboratories Div Pfizer Inc' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T01.s1_rx_brand` | `df295a12217cf245…` | 2026-11-02T18:36:56 |
| `T01.s1_rx_brand_props` | `ba691047a4ad8f6b…` | 2026-11-02T18:36:57 |
| `T01.s1_rx_ingredients` | `4ee3848e97bb9588…` | 2026-11-02T18:36:57 |
| `T01.s1_rx_reverse_591622` | `0dbd1eb0c573868f…` | 2026-11-02T18:36:58 |
| `T01.s2_ndc` | `8b619586c61df419…` | 2026-11-02T18:36:58 |
| `T01.s3_drugsfda` | `2ba7314f6f1e3da2…` | 2026-11-02T18:36:59 |
| `T01.s4_label` | `0d7da9aa9246612b…` | 2026-11-02T18:37:00 |
| `T01.s5_srlc_detail` | `afeb2bd9444d54c3…` | 2026-11-02T18:37:02 |
| `T01.s5_srlc_search` | `1e585832eca3e4a4…` | 2026-11-02T18:37:01 |
| `T01.s6_faers_brand_reactions` | `9f7d7173662bcf59…` | 2026-11-02T18:37:05 |
| `T01.s6_faers_brand_total` | `b2d058058905ab54…` | 2026-11-02T18:37:04 |
| `T01.s6_faers_substance` | `c63ec600c0c48940…` | 2026-11-02T18:37:03 |
| `T01.s6_faers_total` | `dd5e09103a6a231e…` | 2026-11-02T18:37:03 |
| `T01.s7_recall_app` | `339983313f929ee6…` | 2026-11-02T18:37:06 |
| `T01.s8_trial` | `50b68321d54ffaeb…` | 2026-11-02T18:37:07 |
| `T01.s8_trials_search` | `6a57d7e11fc25ba7…` | 2026-11-02T18:37:07 |
| `T01.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:37:08 |

Full records: [claude/traces/T01.jsonl](../claude/traces/T01.jsonl) · checks: [verification/T01.json](../verification/T01.json) · questions: [shared/questions/T01.json](../shared/questions/T01.json)
