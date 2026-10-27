# Source access guide — where and how to get each source

_Stage: Define · Every link and API call below was **tested live on 2026-10-19** (all returned HTTP 200). No login or key is needed for any of them._

## Map
📊 **Diagram:** [04-source-map-v1.png](../../diagrams/png/04-source-map-v1.png) · [PDF](../../diagrams/pdf/04-source-map-v1.pdf) · _source: [04-source-map-v1.mmd](../../diagrams/src/04-source-map-v1.mmd)_

## Three ways into each source
| Way | When to use | Tool |
|---|---|---|
| 🌐 **Browse** | First look, by hand. Learn what a record looks like | Web browser |
| 🔌 **API** | Small, targeted samples (one drug at a time) | Browser address bar, `curl`, or [pull_samples.py](../../../prototypes/explore/pull_samples.py) |
| 📦 **Bulk** | Full data for the real pipeline in Foundry | Download files, then upload to Foundry |

> 💡 **Tip:** paste any API link straight into your browser. Firefox shows JSON nicely; Chrome needs a JSON viewer extension.

---

## 1. FAERS: FDA Adverse Event Reporting System (side-effect reports)
| | |
|---|---|
| 🌐 Browse | **FAERS Public Dashboard**: search "FAERS Public Dashboard" on fda.gov (point-and-click counts by drug and reaction) |
| 🔌 API | `https://api.fda.gov/drug/event.json` · docs: [open.fda.gov/apis/drug/event](https://open.fda.gov/apis/drug/event/) |
| 📦 Bulk | Quarterly ASCII/XML files: [fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html) · openFDA JSON dumps: [open.fda.gov/data/downloads](https://open.fda.gov/data/downloads/) |
| Updates | **Quarterly.** openFDA showed `last_updated = 2026-07-30` on 2026-10-19 |
| Limits | No key: 240 requests/min, 1,000/day. A free key raises this to 120,000/day ([get key](https://open.fda.gov/apis/authentication/)). Max 1,000 results per call |

**Try these (copy into the browser):**
- Top reactions reported for oxycodone:
  `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:"oxycodone"&count=patient.reaction.reactionmeddrapt.exact&limit=20`
- One full report, to see its shape:
  `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:"oxycodone"&limit=1`
- Reports over time:
  `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:"oxycodone"&count=receivedate`

**👀 First real finding (2026-10-19):** oxycodone has ~331k reports. The top reactions are **drug dependence (102k), pain (65k), overdose (55k), emotional distress (50k)**, withdrawal (38k) and death (31k). "Emotional distress" is a classic sign of **litigation-driven reporting** (reports filed as part of lawsuits). This confirms DQ15 and DQ04 in the [data-issues register](../data-issues-register.md).

## 2. DailyMed: official drug labels (our unstructured source)
| | |
|---|---|
| 🌐 Browse | [dailymed.nlm.nih.gov](https://dailymed.nlm.nih.gov/dailymed/) → search "oxycodone" → open a label → "Label RSS / History" |
| 🔌 API | List labels: `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=oxycodone` · full label XML: `…/services/v2/spls/{SETID}.xml` · version history: `…/services/v2/spls/{SETID}/history.json` |
| 📦 Bulk | [All drug labels (zip)](https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-drug-labels.cfm). Full sets plus daily/weekly/monthly update files. Good for **incremental** loads |
| Shortcut | openFDA pre-parsed labels: `https://api.fda.gov/drug/label.json?search=openfda.generic_name:"oxycodone"&limit=1` (has no version history) |
| Updates | **Daily** |

**Key words:** *SPL* = Structured Product Labeling, the XML format of a label. *setid* = one label's permanent ID. *version* = its revision number.
**Label sections are tagged with LOINC codes** (seen live in the Percocet XML):

| Section | Code |
|---|---|
| Boxed Warning | 34066-1 |
| Contraindications | 34070-3 |
| Warnings (older labels) | 34071-1 |
| Warnings and Precautions (newer labels) | 43685-7 |
| Adverse Reactions | 34084-4 |
| Abuse / Controlled Substance | 34086-9 / 34085-1 |

**👀 Finding:** "oxycodone" matches **263 labels** (brands, generics, repackagers, combinations). The Percocet label is on **version 66** and changed **3 times in 2 months** (Aug 13, Sep 28, Oct 8 2026). That's good material for drift and "what changed". The live check also showed this older label uses "Warnings" (34071-1), not "Warnings and Precautions", so section codes vary by label age.

**Try:** Percocet XML `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/4dd36cf5-8f73-404a-8b1d-3bd53bd90c25.xml` · its history `…/4dd36cf5-8f73-404a-8b1d-3bd53bd90c25/history.json`

## 3. FDA drug enforcement reports (recalls)
| | |
|---|---|
| 🌐 Browse | [FDA Enforcement Report search](https://www.accessdata.fda.gov/scripts/ires/index.cfm) |
| 🔌 API | `https://api.fda.gov/drug/enforcement.json` · docs: [open.fda.gov/apis/drug/enforcement](https://open.fda.gov/apis/drug/enforcement/) |
| 📦 Bulk | [open.fda.gov/data/downloads](https://open.fda.gov/data/downloads/) (drug enforcement JSON) |
| Updates | **Weekly.** `last_updated = 2026-10-07` |

**Try:**
- Oxycodone recalls by class: `https://api.fda.gov/drug/enforcement.json?search=product_description:"oxycodone"&count=classification.exact`
- Active ones only: `https://api.fda.gov/drug/enforcement.json?search=product_description:"oxycodone"+AND+status:"Ongoing"&limit=10`

**👀 Finding:** oxycodone has 25 recall records: Class I = 1, II = 12, III = 12. Status: 4 Ongoing, 21 Terminated. The drug is matched only by **free text in `product_description`**, so expect messy joins (DQ11).
_Recall classes: I = could cause serious harm or death · II = temporary or reversible harm · III = unlikely to cause harm._

## 4. RxNorm / RxNav: standard drug IDs (the join key)
| | |
|---|---|
| 🌐 Browse | [RxNav](https://mor.nlm.nih.gov/RxNav/): type a drug, see brand ↔ generic ↔ ingredient |
| 🔌 API | Base `https://rxnav.nlm.nih.gov/REST/` · docs: [RxNorm API](https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html) |
| 📦 Bulk | [RxNorm files](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html). The full release needs a **free UMLS account**; the "Current Prescribable Content" subset needs none |
| Updates | Weekly / monthly |

**Try:**
- Name → ID: `https://rxnav.nlm.nih.gov/REST/rxcui.json?name=oxycodone` → **7804**
- Messy name → best match: `https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=oxycontin&maxEntries=3` → 218986 (brand OxyContin)
- **All opioids by class (ATC N02A):** `https://rxnav.nlm.nih.gov/REST/rxclass/classMembers.json?classId=N02A&relaSource=ATC`. This gives an official, reproducible definition of "opioids" for our formulary

## 5. ClinicalTrials.gov (trial side effects: "second opinion")
| | |
|---|---|
| 🌐 Browse | [clinicaltrials.gov](https://clinicaltrials.gov) → search drug → filter "With results" → "Results" tab → "Adverse Events" |
| 🔌 API | v2: `https://clinicaltrials.gov/api/v2/studies` · docs: [data-api](https://clinicaltrials.gov/data-api/api) |
| 📦 Bulk | Full JSON download linked from the data-api page |
| Updates | Daily |

**Try:** `https://clinicaltrials.gov/api/v2/studies?query.intr=oxycodone&aggFilters=results:with&pageSize=5`. Adverse events sit under `resultsSection.adverseEventsModule`.
**👀 Note:** the first hit was a bioequivalence study (healthy volunteers). Many trials won't be useful for safety; filtering matters.

## Optional sources (later)
| Source | Use | Where | Tested |
|---|---|---|---|
| **FDA Safety-related Labeling Changes (SrLC)** | **Ground truth for the backtest:** when FDA added each safety change | [accessdata.fda.gov/scripts/cder/safetylabelingchanges](https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/) | ✅ 200 |
| FDA Drug Safety Communications | Published warnings to check our signals against | [fda.gov/…/drug-safety-communications](https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications) | ✅ 200 |
| PubMed (E-utilities) | Case reports as evidence | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=oxycodone[mh]+AND+case+reports[pt]&retmode=json` (288 hits) | ✅ 200 |
| Medicare Part D spending | Weight signals by how widely a drug is used | [data.cms.gov Part D spending by drug](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug) | ✅ 200 |

## How to explore by hand (order)
1. FAERS → 2. DailyMed → 3. Enforcement → 4. RxNorm → 5. ClinicalTrials.gov.
For each, fill its profile file (`01-faers.md` … `05-clinicaltrials.md`) using the checklist in [README.md](README.md).
