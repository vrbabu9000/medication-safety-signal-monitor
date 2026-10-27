# FAERS: adverse event reports — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Access: [00-source-access-guide.md](00-source-access-guide.md) · Volumes: [06-data-volume](06-data-volume-13-ingredients.md) · Shape diagram: [10-source-structures-v1.png](../../diagrams/png/10-source-structures-v1.png)_

## In one line
One record = **one report** from one person: a patient took **several drugs** and had **several reactions**. It does not prove the drug caused the reaction.

## How to navigate
| Step | Browser | API |
|---|---|---|
| 1. Get a feel | FAERS Public Dashboard → search drug → "Reactions" tab | `count=patient.reaction.reactionmeddrapt.exact` |
| 2. See one report | (dashboard shows case lists) | `…/drug/event.json?search=patient.drug.openfda.generic_name:"fentanyl"&limit=1` |
| 3. Slice it | Filters: serious, reporter, year | `count=serious`, `count=primarysource.qualification`, `count=receivedate` |
| 4. Full history | Download quarterly files from fis.fda.gov | (bulk only) |

**Local:** `prototypes/data/<drug>/faers_sample_reports.json` (100 reports per drug). Field fill rates: `python3 -I prototypes/explore/describe_structure.py prototypes/data/fentanyl/faers_sample_reports.json`

## Record shape (fields that matter)
```
report
├── safetyreportid            ← report ID
├── receivedate               ← YYYYMMDD
├── serious                   ← 1 serious / 2 not
├── duplicate                 ← "1" in 70–98% of samples (FDA dedup flag; still dedup ourselves)
├── primarysource.qualification ← 1 doctor · 2 pharmacist · 3 other HCP · 4 LAWYER · 5 consumer
└── patient
    ├── patientsex, patientonsetage
    ├── reaction[]            ← many per report
    │   └── reactionmeddrapt  ← MedDRA term, e.g. "Respiratory depression"
    └── drug[]                ← MANY per report (median 6–10, max 138)
        ├── medicinalproduct   ← FREE TEXT as reported ("OXYCONTIN", "FENTANYL.")
        ├── drugcharacterization ← 1 suspect · 2 concomitant · 3 interacting
        ├── drugindication
        └── openfda            ← FDA's enrichment (missing for 17–35% of drug entries)
            ├── generic_name, brand_name, route
            ├── rxcui[]        ← PRODUCT-level IDs (8–35 per drug), not ingredient
            ├── spl_set_id[]   ← direct link to DailyMed labels
            └── product_ndc[]
```

## Real example (fentanyl, report 10007491, trimmed)
```json
{ "safetyreportid": "10007491", "receivedate": "20140312", "serious": "1",
  "primarysource": { "qualification": "3" },                    // other health professional
  "patient": {
    "reaction": [ {"reactionmeddrapt": "Respiratory depression"},
                  {"reactionmeddrapt": "Oxygen saturation decreased"} ],
    "drug": [
      { "medicinalproduct": "VERSED",   "drugcharacterization": "1" },   // midazolam = SUSPECT
      { "medicinalproduct": "FENTANYL", "drugcharacterization": "2",     // fentanyl = only concomitant
        "openfda": { "generic_name": ["FENTANYL"], "route": ["TRANSDERMAL"], "rxcui": ["…8 IDs…"] } } ] } }
```
**What to notice:**
1. Fentanyl was **not** the suspect here. Midazolam was.
2. openFDA guessed the route as **TRANSDERMAL** (patch) from the name alone, but this looks like a procedure where fentanyl would be given by injection. **The enrichment is a name match, not the truth** (DQ24).

## Categories
| Dimension | Values |
|---|---|
| Seriousness | serious (61–93% for opioids; 18–50% for GLP-1) / non-serious |
| Reporter | doctor, pharmacist, other HCP, lawyer, consumer |
| Drug role | suspect, concomitant, interacting |
| Reaction buckets (ours) | clinical · abuse/overdose · litigation-style · product-use/error · pregnancy/neonatal (to add) |

## Join keys
> ⚠️ 2026-10-20: the `openfda` keys below exist **only in the API**. Bulk quarterly files (our pipeline input) have none; use `prod_ai` → RxNorm and `nda_num` → label (DQ39). Full bulk walkthrough: [data-walkthrough-v1.html](../../04-architecture/data-walkthrough-v1.html).
- `openfda.rxcui` → roll up to **RxNorm ingredient (IN)**.
- `openfda.spl_set_id` → DailyMed `setid` (direct link to label).
- `medicinalproduct` → RxNorm `approximateTerm` when `openfda` is missing.

## Mess found (counts from 100-report samples)
| Issue | Seen | Register |
|---|---|---|
| Target drug is only concomitant | oxycodone 103 of 118 entries; fentanyl 58 of 107; semaglutide 54 of 113 | DQ23 |
| Drug entries without `openfda` | 26% (oxycodone), 35% (fentanyl), 17% (semaglutide) | DQ02 |
| Name spellings for one drug | oxycodone 6 (OXYCODONE, OXYCONTIN, ROXICODONE, ENDOCET …); fentanyl 4 incl. "FENTANYL." | DQ02 |
| Lawyer-filed reports | hydrocodone/hydromorphone 51%, oxycodone 29% | DQ21 |
| Field choice changes counts | semaglutide 73,001 (generic_name) vs 100,679 (active substance) | DQ25 |

## How to use it well
1. **API for exploring and counts. Bulk quarterly files for the pipeline** (role per drug, case versions for dedup, incremental by quarter).
2. Filter early: our 13 ingredients, suspect role only, latest case version.
3. Tag (don't delete): lawyer-filed, abuse/overdose, product-use/error, pregnancy/neonatal.
4. Always store the query and quarter with every count, for traceability.

## ✅ Your hand-verification
- [ ] Open one report in the browser and find the drug roles
- [ ] Find a report where our drug is only concomitant
- [ ] Compare `medicinalproduct` with `openfda.generic_name` on 5 entries
- [ ] Check the lawyer share for one opioid with `count=primarysource.qualification`
