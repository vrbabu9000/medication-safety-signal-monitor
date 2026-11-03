# T03 · Plavix (antiplatelet)

**Status:** verified against sources (112/112 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:37Z – 2026-11-02T18:37Z · questions sha256 `0d564f5f8eab…`

## The trace in one line
Plavix → RxNorm 174742 (clopidogrel (32968)) → package 0024-1171-90 under NDA020839 → DailyMed label de8b0b67-eb25-4684-83b5-7ad785314227 v5 (effective 20250530) → SrLC 09/16/2022 → 2201 FAERS reports name it in 2025 → recall D-0787-2021 → trial NCT00335452.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 174742 (BN); ingredient(s) clopidogrel (32968); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0024-1171-90: 90 TABLET, FILM COATED in 1 BOTTLE (0024-1171-90); labeler Sanofi-Aventis U.S. LLC; category NDA; application NDA020839 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor SANOFI AVENTIS US; 2 product(s): 001 TABLET EQ 75MG BASE; 002 TABLET EQ 300MG BASE | Same application number as S2 |
| S4 | DailyMed | In '5.1 Diminished Antiplatelet Activity in Patients with Impaired CYP2C19 Function', what role does 'genetic variations in CYP2C19' play? | **underlying_condition_or_risk_factor** | Quote: "The metabolism of clopidogrel to its active metabolite can be impaired by genetic variations in CYP2C19" |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 09/16/2022 SUPPL-78, 5.2 General Risk of Bleeding | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 2201 reports name PLAVIX; 9064 list CLOPIDOGREL BISULFATE (any product) | Top-10 terms checked against S4 label: 3 found, 7 not found |
| S7 | FDA enforcement | Any recall? | D-0787-2021 (Class II, reported status 'Terminated', 20210908): Presence of foreign matter | Record text names package 0024-1171-90: **False** (ingredient-level query, 3 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00335452 (COMPLETED), EG000 'Clopidogrel 300/75/75 mg + ASA Low Dose': serious AEs 322 of 6312 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** FATIGUE, DYSPNOEA, NAUSEA, OFF LABEL USE, DIZZINESS, ASTHENIA, PRODUCT DOSE OMISSION ISSUE. Found in label: DIARRHOEA, DEATH, HEADACHE.
- **Recall:** D-0787-2021 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (09/16/2022) is reflected in the captured DailyMed label.

## Traps this trace shows
- Context trap: omeprazole and esomeprazole in the same passage are co-medication risk factors, a different class. The outcome is reduced effect, not a reaction.
- Query scope changes the count: 2201 brand-named vs 9064 substance-level reports.
- Sponsor 'SANOFI AVENTIS US' (Drugs@FDA) vs labeler 'Sanofi-Aventis U.S. LLC' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T03.s1_rx_brand` | `a1bfbfa10a8519cf…` | 2026-11-02T18:37:20 |
| `T03.s1_rx_brand_props` | `32703fdf30a66548…` | 2026-11-02T18:37:20 |
| `T03.s1_rx_ingredients` | `1b4c2cfcca473419…` | 2026-11-02T18:37:21 |
| `T03.s1_rx_reverse_32968` | `6ec1a78b1bd71261…` | 2026-11-02T18:37:21 |
| `T03.s2_ndc` | `85d7eb04083a9f75…` | 2026-11-02T18:37:22 |
| `T03.s3_drugsfda` | `c0be71b199e28f64…` | 2026-11-02T18:37:23 |
| `T03.s4_label` | `e2fa73bd4988cdad…` | 2026-11-02T18:37:23 |
| `T03.s5_srlc_detail` | `0199646769852203…` | 2026-11-02T18:37:26 |
| `T03.s5_srlc_search` | `43921aaac5db4aa0…` | 2026-11-02T18:37:25 |
| `T03.s6_faers_brand_reactions` | `8ba68068a517a80c…` | 2026-11-02T18:37:29 |
| `T03.s6_faers_brand_total` | `153011f4ab08333a…` | 2026-11-02T18:37:28 |
| `T03.s6_faers_substance` | `7fb7727087464aa4…` | 2026-11-02T18:37:26 |
| `T03.s6_faers_total` | `7c3ba3aa2e3add21…` | 2026-11-02T18:37:27 |
| `T03.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:37:29 |
| `T03.s7_recall_ingredient` | `b2602b960db88834…` | 2026-11-02T18:37:30 |
| `T03.s8_trial` | `4a6174385aef580a…` | 2026-11-02T18:37:31 |
| `T03.s8_trials_search` | `5679a8f0723342bc…` | 2026-11-02T18:37:31 |
| `T03.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:37:32 |

Full records: [claude/traces/T03.jsonl](../claude/traces/T03.jsonl) · checks: [verification/T03.json](../verification/T03.json) · questions: [shared/questions/T03.json](../shared/questions/T03.json)
