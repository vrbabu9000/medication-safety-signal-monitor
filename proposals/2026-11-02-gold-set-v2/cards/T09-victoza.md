# T09 · Victoza (GLP-1)

**Status:** verified against sources (110/110 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:38Z – 2026-11-02T18:38Z · questions sha256 `2e3ec3c97d07…`

## The trace in one line
Victoza → RxNorm 897123 (liraglutide (475968)) → package 0169-4060-12 under NDA022341 → DailyMed label 5a9ef4ea-c76a-4d34-a604-27c5b505f5a4 v31 (effective 20251014) → SrLC 10/14/2025 → 1117 FAERS reports name it in 2025 → recall D-0622-2021 → trial NCT01179048.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 897123 (BN); ingredient(s) liraglutide (475968); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0169-4060-12: 2 SYRINGE, PLASTIC in 1 CARTON (0169-4060-12)  / 3 mL in 1 SYRINGE, PLASTIC; labeler Novo Nordisk; category NDA; application NDA022341 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor NOVO NORDISK INC; 1 product(s): 001 SOLUTION 18MG/3ML (6MG/ML) | Same application number as S2 |
| S4 | DailyMed | In '5.3 Never Share a VICTOZA Pen Between Patients', what role does 'must never be shared between patients' play? | **administration_instruction** | Quote: "VICTOZA pens must never be shared between patients, even if the needle is changed." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 10/14/2025 SUPPL-46, 5.2 Acute Pancreatitis | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 1117 reports name VICTOZA; 1992 list LIRAGLUTIDE (any product) | Top-10 terms checked against S4 label: 5 found, 5 not found |
| S7 | FDA enforcement | Any recall? | D-0622-2021 (Class II, reported status 'Terminated', 20210421): Temperature Abuse: product samples were stored at temperatures below 32* F which is not in accordance with storage requirements that could c… | Record text names package 0169-4060-12: **False** (application-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT01179048 (COMPLETED), EG000 'Liraglutide': serious AEs 2320 of 4668 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** IMPAIRED GASTRIC EMPTYING, OFF LABEL USE, GASTROINTESTINAL HYPOMOTILITY, ABDOMINAL PAIN UPPER, BLOOD GLUCOSE INCREASED. Found in label: NAUSEA, VOMITING, DIARRHOEA, ABDOMINAL PAIN, CONSTIPATION.
- **Recall:** D-0622-2021 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (10/14/2025) is reflected in the captured DailyMed label.

## Traps this trace shows
- Low ambiguity.
- Query scope changes the count: 1117 brand-named vs 1992 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'NOVO NORDISK INC' (Drugs@FDA) vs labeler 'Novo Nordisk' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T09.s1_rx_brand` | `876a14767eda7574…` | 2026-11-02T18:38:32 |
| `T09.s1_rx_brand_props` | `496b5ab364bd47c7…` | 2026-11-02T18:38:32 |
| `T09.s1_rx_ingredients` | `2e6a033f6588a76b…` | 2026-11-02T18:38:33 |
| `T09.s1_rx_reverse_475968` | `7e0a3257e2c1e21a…` | 2026-11-02T18:38:33 |
| `T09.s2_ndc` | `cf0cbf910e56b83b…` | 2026-11-02T18:38:34 |
| `T09.s3_drugsfda` | `1b36befa5eb20ccb…` | 2026-11-02T18:38:35 |
| `T09.s4_label` | `b14adc782ac8eaf1…` | 2026-11-02T18:38:35 |
| `T09.s5_srlc_detail` | `42fb245a9a743667…` | 2026-11-02T18:38:37 |
| `T09.s5_srlc_search` | `17bbca29d6eb2196…` | 2026-11-02T18:38:36 |
| `T09.s6_faers_brand_reactions` | `cf0614fe687e8f7b…` | 2026-11-02T18:38:40 |
| `T09.s6_faers_brand_total` | `dd4760801d03fb8e…` | 2026-11-02T18:38:39 |
| `T09.s6_faers_substance` | `55c6c0caab30a7da…` | 2026-11-02T18:38:38 |
| `T09.s6_faers_total` | `a9188b7425322ff6…` | 2026-11-02T18:38:39 |
| `T09.s7_recall_app` | `de682a7818355b18…` | 2026-11-02T18:38:41 |
| `T09.s8_trial` | `b571ea5f82c7006c…` | 2026-11-02T18:38:42 |
| `T09.s8_trials_search` | `e5d6c700d8662f41…` | 2026-11-02T18:38:41 |
| `T09.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:38:42 |

Full records: [claude/traces/T09.jsonl](../claude/traces/T09.jsonl) · checks: [verification/T09.json](../verification/T09.json) · questions: [shared/questions/T09.json](../shared/questions/T09.json)
