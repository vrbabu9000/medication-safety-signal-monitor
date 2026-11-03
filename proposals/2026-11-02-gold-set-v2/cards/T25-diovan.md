# T25 · Diovan (ARB)

**Status:** verified against sources (111/111 automated checks passed) · pharmacist review **pending** · captured 2026-11-02T18:41Z – 2026-11-02T18:42Z · questions sha256 `af4e354adbf6…`

## The trace in one line
Diovan → RxNorm 216652 (valsartan (69749)) → package 0078-0358-34 under NDA021283 → DailyMed label 5ddba454-f3e6-43c2-a7a6-58365d297213 v32 (effective 20260811) → SrLC 04/19/2021 → 371 FAERS reports name it in 2025 → recall D-0746-2026 → trial NCT00097786.

## How each source was used

| Step | Source | What we asked | Answer | How it links |
|---|---|---|---|---|
| S1 | RxNorm | Which medicine is this? | Brand RxCUI 216652 (BN); ingredient(s) valsartan (69749); multi-ingredient: False | Reverse check: each ingredient lists this brand |
| S2 | NDC Directory | Which package and who lists it? | 0078-0358-34: 90 TABLET in 1 BOTTLE (0078-0358-34); labeler Novartis Pharmaceuticals Corporation; category NDA; application NDA021283 | Listing's label set ID = S4 label: **True** |
| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor NOVARTIS; 4 product(s): 001 TABLET 80MG; 002 TABLET 160MG; 003 TABLET 320MG; 004 TABLET 40MG | Same application number as S2 |
| S4 | DailyMed | In '5.2 Hypotension', what role does 'symptomatic hypotension' play? | **reaction_or_warning** | Quote: "In patients with an activated renin-angiotensin system, such as volume- and/or salt-depleted patients receiving high doses of diuretics, symptomatic hypotension may occur." |
| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | 04/19/2021 SUPPL-58, 6.1 Clinical Trials Experience | Underlined text present in S4 label: **True** |
| S6 | FAERS | What do 2025 reports say? | 371 reports name DIOVAN; 4192 list VALSARTAN (any product) | Top-10 terms checked against S4 label: 6 found, 4 not found |
| S7 | FDA enforcement | Any recall? | D-0746-2026 (Class II, reported status 'Ongoing', 20260819): Failed Dissolution Specifications | Record text names package 0078-0358-34: **False** (application-level query, 1 records) |
| S8 | ClinicalTrials.gov | What did a trial arm report? | NCT00097786 (COMPLETED), EG000 'Valsartan 160 mg od + Nateglinide 60 mg ac': serious AEs 1031 of 2297 | Group title names the drug |

## What the safety officer can say from this trace
- **Not in the label (string check, needs pharmacist review):** BLOOD PRESSURE INCREASED, DYSPNOEA, OFF LABEL USE, DRUG INEFFECTIVE. Found in label: NAUSEA, DIARRHOEA, FATIGUE, COUGH, DIZZINESS, PAIN.
- **Recall:** D-0746-2026 does not name this package in its own text. Reported status is not today's status; hospital exposure needs inventory and lot data.
- **Label currency:** the latest SrLC change (04/19/2021) is reflected in the captured DailyMed label.

## Traps this trace shows
- Context trap: the volume- or salt-depleted patients in the same sentence are a risk factor, a different class.
- Query scope changes the count: 371 brand-named vs 4192 substance-level reports.
- openFDA's harmonized package list includes this package, but the recall's own text does not name it.
- Sponsor 'NOVARTIS' (Drugs@FDA) vs labeler 'Novartis Pharmaceuticals Corporation' (NDC): join on application number, not names.

## Evidence files

| Source ID | sha256 | Retrieved (UTC) |
|---|---|---|
| `T25.s1_rx_brand` | `3b39064630fc3164…` | 2026-11-02T18:41:52 |
| `T25.s1_rx_brand_props` | `e2b30b04c4264ceb…` | 2026-11-02T18:41:52 |
| `T25.s1_rx_ingredients` | `3d70c483984f2e7c…` | 2026-11-02T18:41:54 |
| `T25.s1_rx_reverse_69749` | `86111a081a076ffb…` | 2026-11-02T18:41:54 |
| `T25.s2_ndc` | `b4cd3ad7946c00ca…` | 2026-11-02T18:41:55 |
| `T25.s3_drugsfda` | `9c462d8f2d3cead4…` | 2026-11-02T18:41:55 |
| `T25.s4_label` | `50597951429ed414…` | 2026-11-02T18:41:56 |
| `T25.s5_srlc_detail` | `07a954d745c695b1…` | 2026-11-02T18:41:58 |
| `T25.s5_srlc_search` | `01fdab531c06d05b…` | 2026-11-02T18:41:57 |
| `T25.s6_faers_brand_reactions` | `574867fdd74d75dd…` | 2026-11-02T18:42:01 |
| `T25.s6_faers_brand_total` | `5018f59fd4476cc5…` | 2026-11-02T18:42:00 |
| `T25.s6_faers_substance` | `178307c5ccf1d091…` | 2026-11-02T18:41:59 |
| `T25.s6_faers_total` | `3d89ce9f6ebe0cd1…` | 2026-11-02T18:41:59 |
| `T25.s7_recall_app` | `2fb395d585c45bf0…` | 2026-11-02T18:42:02 |
| `T25.s8_trial` | `005f116c8c2f413e…` | 2026-11-02T18:42:03 |
| `T25.s8_trials_search` | `e5a03824cfa32d31…` | 2026-11-02T18:42:02 |
| `T25.s8_trials_version` | `4dd1c3ebf1e7c002…` | 2026-11-02T18:42:03 |

Full records: [claude/traces/T25.jsonl](../claude/traces/T25.jsonl) · checks: [verification/T25.json](../verification/T25.json) · questions: [shared/questions/T25.json](../shared/questions/T25.json)
