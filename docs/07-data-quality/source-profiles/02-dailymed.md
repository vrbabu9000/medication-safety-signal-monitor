# DailyMed: drug labels — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Access: [00-source-access-guide.md](00-source-access-guide.md)_

## In one line
One record = **one label document** (SPL XML) for one product from one company. It has a permanent **setid**, and every edit creates a new **version**. This is our **unstructured** source, and it's what the LLM reads.

## How to navigate
| Step | Browser | API |
|---|---|---|
| 1. Find labels | dailymed.nlm.nih.gov → search "fentanyl" (46 labels) | `services/v2/spls.json?drug_name=fentanyl` |
| 2. Read one | Click a label → sections listed on the left | `services/v2/spls/{setid}.xml` |
| 3. See history | Label page → "Label RSS / History" | `services/v2/spls/{setid}/history.json` |
| 4. Bulk | "SPL resources" → full + daily/weekly update zips | — |

**Local:** `prototypes/data/<drug>/dailymed_first_label.xml` (open it in a browser), `dailymed_labels.json`, `dailymed_first_label_history.json`.

## Record shape
```
label (SPL XML)
├── setId                     ← permanent label ID (= FAERS openfda.spl_set_id)
├── versionNumber             ← 1, 2, 3 … (e.g. fentanyl Hospira v35; values up to 3,540 seen)
├── effectiveTime
└── component/structuredBody/section[]   ← each tagged with a LOINC code
    ├── 34066-1 Boxed Warning
    ├── 34070-3 Contraindications
    ├── 43685-7 Warnings and Precautions   (newer labels)
    ├── 34071-1 Warnings                   (older labels)
    ├── 34084-4 Adverse Reactions          ← prose + tables of % by arm
    └── … 20+ other sections (dosage, abuse, overdose …)
```

## Real examples (2026-10-20)
| | Fentanyl Citrate Inj. (Hospira) | Ozempic/Rybelsus (Novo Nordisk) |
|---|---|---|
| Version / date | v35 · Aug 25 2026 | v14 · Aug 19 2026 |
| Versions in history | 28 | 15 |
| Boxed Warning | 5,696 chars | 2,714 chars |
| Warnings & Precautions | 23,486 chars | 14,153 chars |
| Adverse Reactions | 5,420 chars, 0 tables | 26,643 chars, **2 tables** |
| Mentions of our test term | "respiratory depression" × 55 | "optic" / "NAION" × **0** |

## Categories
- **Labels per ingredient:** brand (innovator), generics, repackagers (e.g. "A-S Medication"), combinations (oxycodone + acetaminophen).
- **Section types:** by LOINC code (above).
- **Label age:** older "Warnings" vs newer "Warnings and Precautions" format (DQ19).

## Join keys
- `setid` ← FAERS `openfda.spl_set_id` (direct link).
- openFDA label `openfda.rxcui` → RxNorm → ingredient.

## Mess found
| Issue | Seen | Register |
|---|---|---|
| Many labels per ingredient | hydrocodone 357, oxycodone 263, tramadol 237 | DQ07 |
| Version numbers not comparable across labels | values from 1 to 3,540 | DQ27 |
| Two section codes for "warnings" | Percocet uses 34071-1 | DQ19 |
| openFDA's label copy lags DailyMed | openFDA Ozempic effective 2026-01-30 vs DailyMed v14 Aug 2026 | DQ28 |
| Odd titles | "OZEMPIC (ORAL SEMAGLUTIDE) TABLET RYBELSUS…" in one document | DQ07 |

## How to use it well
1. Pick **one reference label per ingredient** (brand/innovator). Track generic **label lag** as a drift metric.
2. Extract only 4 sections (Boxed, Contraindications, Warnings/W&P, Adverse Reactions). This cuts LLM cost.
3. Store every extraction keyed by **(setid, version, section)**, and re-extract only on a new version (D005).
4. Use DailyMed, not the openFDA label copy, when freshness matters.

## ✅ Your hand-verification
- [ ] Open the fentanyl XML in a browser and find the 4 sections
- [ ] Open Ozempic on DailyMed and search the page for "optic". Confirm it's absent
- [ ] Compare two versions of one label in its history

---

## Addendum 2026-10-20: labels atlas (Part B deep dive)
_Atlas page: [dailymed.html](../atlas/dailymed.html) ([artifact](https://claude.ai/artifact/UD3a4VGadvPB6e14N3YvGj)) · Script: [label_atlas.py](../../../prototypes/explore/label_atlas.py) steps `refs`, `sections`, `census`, `dailyzip`, `textdump`, `goldcheck` · Gold-set draft: [gold-set-draft-v1.csv](../atlas/gold-set-draft-v1.csv)_

### Reference label per ingredient (rule tested on 2026 Q1+Q2 FAERS)
Rule: the most-reported primary-suspect application (`nda_num`) → its owner's label (DailyMed `spls.json?application_number=`). If that is a generic and the brand label still exists, use the brand label for the same route.

| Ingredient | Reference label | Application | Version · date | Note |
|---|---|---|---|---|
| buprenorphine | Brixadi injection | NDA210136 | v6 · 2026-01-06 | |
| fentanyl | Fentanyl patch (Mylan) | ANDA076258 | v27 · 2026-02-25 | Duragesic label gone (2011 repackager only) |
| hydrocodone | Hysingla ER | NDA206627 | v17 · 2026-06-18 | |
| hydromorphone | Hydromorphone tab + solution (Rhodes) | NDA019892 | v20 · 2026-05-20 | |
| methadone | Methadone tablet (Ascend) | ANDA090635 | v11 · **2022-06-15** | **Stale**: lacks the Dec 2023 + Dec 2025 opioid class additions |
| morphine | MS Contin | NDA019516 | v18 · 2026-08-19 | |
| oxycodone | OxyContin | NDA022272 | v44 · 2026-06-26 | Gold-set label |
| tramadol | Tramadol tablet (Teva) | ANDA075977 | v6 · 2026-01-29 | Ultram label gone |
| semaglutide | Ozempic injection | NDA209637 | v20 · 2026-06-10 | Gold-set label |
| liraglutide | Victoza | NDA022341 | v31 · 2025-11-17 | |
| dulaglutide | Trulicity | BLA125469 | v62 · 2026-08-10 | |
| exenatide | Byetta | NDA021773 | v26 · 2025-09-08 | Only 4 FAERS PS rows in 6 months |
| tirzepatide | Mounjaro | NDA215866 | v40 · 2026-09-02 | |

### Structure (13 reference labels, 4 safety sections)
- Size: 20,655 (Ozempic) to 51,600 chars (tramadol); opioids ≈ 2× GLP-1s.
- Subsection codes come 3 ways: generic 42229-5 (13/13), specific 90374-0 / 90375-7 (7/13), parent code repeated (Ozempic, Byetta). → Never filter by child code.
- All 13 use 43685-7 (no old 34071-1). Byetta has no Boxed Warning (correct).
- Tables 0–5; merged cells up to 11 (Trulicity, Byetta); nesting up to 6 levels (Mounjaro).

### Change census (Jul 22 → Oct 20, 2026, 1,324 labels)
- 102 versions, 94 labels touched; 50 of 91 days with none; max 10/day; **0 on weekends**.
- Reference labels: 3 of 13 changed (Trulicity, MS Contin, Mounjaro). SrLC safety changes in the same window: **1**.
- Oct 19 daily file: 381 labels (207 Rx), 3 ours = API census for that day ✓.
- API: `published_date=X` alone = exactly that day; add `published_date_comparison=gte` for "since". Sees current versions only.
- Download page lists only the latest daily file (plus 3 weekly Mon–Fri, 7 monthly).

### Gold-set draft (for you to verify)
[gold-set-draft-v1.csv](../atlas/gold-set-draft-v1.csv): 264 rows. Ozempic v20: 73 rows (58 count as labeled, 44 unique PTs). OxyContin v44: 191 rows (165 count, 147 unique PTs). Every quote is verified word for word against the label XML (`goldcheck`: 0 not found). Contexts: adverse_reaction / symptom_of_other / pre_existing_condition / mechanism. PT names are checked against FAERS 2026 H1 strings: all seen except "Gastroparesis" and "Hyperalgesia" (0 reports; probably valid PTs, unverified without MedDRA). Fill `user_verdict` (ok / wrong / unsure) and `user_note`.

### Proposed for the logs
_Temporary IDs; assign the next D / DQ numbers when merging (sibling atlas sessions also propose D032+, DQ42+)._

| ID | Type | Proposal | Evidence |
|---|---|---|---|
| LD1 | Decision | Reference label = owner's label of the most-reported FAERS application; generic fallback flagged on screen | 13/13 resolved; 3 brand labels gone |
| LD2 | Decision | Label ChangeEvent only when a safety-section hash changes on a reference label | 102 versions vs 1 SrLC change in 90 d |
| LD3 | Decision | Reference freshness flag: older than the latest SrLC change for the ingredient | Methadone 2022 label lacks 2023 + 2025 additions |
| LQ1 | Data issue | Subsection coding varies 3 ways | 13/13, 7/13, 2/13 |
| LQ2 | Data issue | Brand labels missing (Duragesic, Dolophine, Ultram) | application lookups |
| LQ3 | Data issue | API date filter = exact day by default; current versions only | probe calls |
| LQ4 | Data issue | Only the latest daily update file is listed | download page |
| LQ5 | Data issue | History version numbers skip and repeat (Trulicity 39 listed up to v62; MS Contin v16 twice) | history.json |
| Learning | — | Most label versions are not safety changes; "new version" ≠ "what changed" for the officer | census vs SrLC |
