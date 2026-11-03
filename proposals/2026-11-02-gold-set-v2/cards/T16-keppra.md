# T16 · Keppra (antiepileptic)

**Status:** verified against sources (116/116 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:39Z – 2026-11-02T18:40Z · questions sha256 `4b697257cfff…`

## The trace in one line
Keppra → RxNorm 261547 (levetiracetam (114477)) → package 50474-594-40 under NDA021035 → DailyMed label 3ca9df05-a506-4ec8-a4fe-320f1219ab21 v36 (effective 20260128) → SrLC 08/17/2023 → 2431 FAERS reports name it in 2025 → recall D-0365-2025 → trial NCT00537238.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 261547 (BN); ingredient(s) levetiracetam (114477); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 50474-594-40: 120 TABLET, FILM COATED in 1 BOTTLE, PLASTIC (50474-594-40); labeler UCB, Inc.; category NDA; application NDA021035 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor UCB INC; 4 product(s): 001 TABLET 250MG; 002 TABLET 500MG; 003 TABLET 750MG; 004 TABLET 1GM | Same application number as S2 |
| S4 | DailyMed | In '5.3 Somnolence and Fatigue', what role does 'somnolence' play? | **reaction_or_warning** | Quote: "KEPPRA may cause somnolence and fatigue." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 08/17/2023 SUPPL-112, 6.2 Postmarketing Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 2431 reports name KEPPRA; 8907 list LEVETIRACETAM (any product) | Top-10 terms checked against S4 label: 7 found, 3 not found |
| S7 | FDA enforcement | Any recall? | D-0365-2025 (Class I, reported status 'Ongoing', 20250423): LABELING: LABEL MIX-UP: The infusion bag is incorrectly labeled as Levetiracetam in 0.82% Sodium Chloride Injection 500 mg/100 mL, while the… | Record text names package 50474-594-40: **False** (ingredient-level query, 9 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00537238 (COMPLETED), EG001 'Levetiracetam': serious AEs 24 of 255 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** OFF LABEL USE, PRODUCT DOSE OMISSION ISSUE, DRUG INEFFECTIVE. Found in label: SEIZURE, FATIGUE, SOMNOLENCE, VOMITING, DIARRHOEA, FALL, DIZZINESS.
- **Recall:** D-0365-2025 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (08/17/2023) is reflected in the captured DailyMed label.

## Traps this trace shows
- Low ambiguity. The driving advice in the same passage is an instruction.
- Query scope changes the count: 2431 brand-named vs 8907 substance-level reports.
- Sponsor 'UCB INC' (Drugs@FDA) vs labeler 'UCB, Inc.' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T16.s1_rx_brand` | `78325cae3f2b0e5f…` | 2026-11-02T18:39:57 |
| `T16.s1_rx_brand_props` | `4ecb772d7d0e8e64…` | 2026-11-02T18:39:57 |
| `T16.s1_rx_ingredients` | `cfe18c0458655dd3…` | 2026-11-02T18:39:57 |
| `T16.s1_rx_reverse_114477` | `e8974cac9bb152ed…` | 2026-11-02T18:39:59 |
| `T16.s2_ndc` | `ab1635ab25aaddbb…` | 2026-11-02T18:40:00 |
| `T16.s3_drugsfda` | `882b8c271447415b…` | 2026-11-02T18:40:00 |
| `T16.s4_label` | `388d152c93883563…` | 2026-11-02T18:40:01 |
| `T16.s5_srlc_detail` | `0947f46882e961d6…` | 2026-11-02T18:40:03 |
| `T16.s5_srlc_search` | `4c7def85fd6253f7…` | 2026-11-02T18:40:03 |
| `T16.s6_faers_brand_reactions` | `bf48671a11220f9b…` | 2026-11-02T18:40:07 |
| `T16.s6_faers_brand_total` | `f5e1d572917d68a4…` | 2026-11-02T18:40:07 |
| `T16.s6_faers_substance` | `360bc323f39cf4c5…` | 2026-11-02T18:40:05 |
| `T16.s6_faers_total` | `d6eff1ba5fddab08…` | 2026-11-02T18:40:06 |
| `T16.s7_recall_app` | `57b1e7534d003e42…` | 2026-11-02T18:40:08 |
| `T16.s7_recall_ingredient` | `cd0bcdc3863b1fd0…` | 2026-11-02T18:40:09 |
| `T16.s8_trial` | `c2861f2380d0242c…` | 2026-11-02T18:40:10 |
| `T16.s8_trials_search` | `3e4d84fc5ba198c8…` | 2026-11-02T18:40:09 |
| `T16.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:40:10 |

Full records: [claude/traces/T16.jsonl](../claude/traces/T16.jsonl) · checks: [verification/T16.json](../verification/T16.json) · questions: [shared/questions/T16.json](../shared/questions/T16.json)
