# FAERS and Part B, explained with one real drug

> ⚠️ **Superseded by [data-walkthrough-v1.html](data-walkthrough-v1.html)** (real bulk files, every stage measured). Kept for history. Note: the `openfda` fields used below exist only in the API copy, not in the bulk files (DQ39).

_Stage: Define → Prototype (on paper) · Drug used throughout: **semaglutide** (Ozempic / Rybelsus) · All examples are real data from `prototypes/data/semaglutide/` (pulled 2026-10-20) · Approach: [A004](../05-approaches/A004-faers-to-ontology-mapping.md)_
_Diagram (open this first): [16-faers-to-signal-v1.png](../diagrams/png/16-faers-to-signal-v1.png) · [PDF](../diagrams/pdf/16-faers-to-signal-v1.pdf)_

---

## 1. The whole project is just two lists, compared

For each drug, we build two lists and compare them.

| List | Question it answers | Comes from | Built by |
|---|---|---|---|
| **List 1: "What people report"** | Which side effects do patients and doctors report for this drug, and how often? | FAERS | Counting (plain pipeline code, no AI) |
| **List 2: "What the label says"** | Which side effects does the official label already warn about? | DailyMed label | **The LLM (this is Part B)** |
| **Compare** | Which reactions are in List 1 (often) but **not** in List 2? | both | Matching + a statistic |

Anything in List 1, reported often, and missing from List 2 = a **Signal**. That answers the safety officer's question 1.

---

## 2. Part B, in plain words

**Why do we need an LLM at all?** Because List 2 is hidden inside long prose. The label is a document, not a table. You cannot just "search for the word".

### The input: a real passage from the semaglutide label (setid `27f15fac…`, version 14)
Section 6, Adverse Reactions (trimmed):
> "Most common adverse reactions (incidence ≥5%) are nausea, abdominal pain, diarrhea, decreased appetite, vomiting and constipation."

Section 6.2, Postmarketing Experience (trimmed, paraphrased):
> Gastrointestinal: acute pancreatitis, necrotizing pancreatitis, ileus, intestinal obstruction … Hepatobiliary: cholecystitis, cholelithiasis … Skin: alopecia.

### The output: what we ask the LLM to return (one row per reaction)
| reaction (as written) | MedDRA term (normalized) | section | evidence quote (must exist in the label) |
|---|---|---|---|
| nausea | Nausea | 6 Adverse Reactions | "Most common adverse reactions … are nausea, …" |
| abdominal pain | Abdominal pain | 6 Adverse Reactions | same sentence |
| decreased appetite | Decreased appetite | 6 Adverse Reactions | same sentence |
| acute pancreatitis | Pancreatitis acute | 5.2 Warnings & Precautions | "Acute Pancreatitis: Has been observed in patients treated with GLP-1…" |
| cholecystitis | Cholecystitis | 5.8 W&P + 6.2 | "If cholelithiasis or cholecystitis are suspected…" |
| ileus | Ileus | 6.2 Postmarketing | "ileus, intestinal obstruction…" |
| alopecia | Alopecia | 6.2 Postmarketing | "Skin and subcutaneous tissue: alopecia" |
| … ~60–100 rows per label | | | |

> **MedDRA term** = the standard medical word list FAERS uses (e.g. the label says "diarrhea", FAERS says "Diarrhoea"). Normalizing both to the same word is what makes the comparison possible.

### Why "just search the text" fails: 3 real traps from this label
| Trap | What a plain text search does | What the LLM must do |
|---|---|---|
| "**blurred vision**" appears once | Says "on the label" ✅ | It's in a list of **symptoms of low blood sugar**, not a side effect of the drug. Should **not** count as labeled. |
| "**gastroparesis**" appears twice | Says "on the label" ✅ | It says "not recommended in patients **with** severe gastroparesis". That is a pre-existing condition, not a side effect. |
| "**diarrhea**" (US spelling) | FAERS term "Diarrhoea" → no match ❌ | Normalize both to MedDRA "Diarrhoea". |

That is the whole expectation for Part B: **read the label sections, return the side-effect list with a quote for each, in the same vocabulary as FAERS.**

### How we prove the LLM is right (graded: "AI reliability")
| Check | How | Catches |
|---|---|---|
| **Grounding** | The evidence quote must be found word-for-word in the label text (simple code check) | Made-up reactions (hallucination) |
| **Gold set** | You hand-list the reactions for ~10 labels. Compare LLM vs you → precision / recall / F1 (target F1 ≥ 0.85, D015) | Missed reactions, wrong ones |
| **Cache** | Store results by (setid, version, section, prompt version, model). Re-run only on a new label version | Wasted LLM cost (graded: "optimization") |

---

## 3. FAERS: what we take, what we leave

One FAERS record = one report. It has **many drugs** and **many reactions**. We keep only what the comparison and the trust rule need.

| Field | Keep? | Why |
|---|---|---|
| `safetyreportid`, `safetyreportversion` | ✅ | Trace back to source; keep latest version only (dedup) |
| `receivedate` | ✅ | Group by quarter; "what changed since…"; trends |
| `serious`, `seriousness*` | ✅ | Rank serious signals higher |
| `primarysource.qualification` | ✅ | Tag lawyer (4) and consumer (5) reports (DQ21) |
| `patient.reaction[].reactionmeddrapt` | ✅ | **List 1 itself** |
| `patient.drug[].medicinalproduct` | ✅ | Raw name; fallback for drug identity |
| `patient.drug[].drugcharacterization` | ✅ | 1 = suspect. We count suspect only (DQ05/DQ23) |
| `patient.drug[].openfda.rxcui`, `.spl_set_id` | ✅ | Link to RxNorm ingredient and to the label |
| `patient.drug[].drugindication` | ✅ (light) | Drop reactions that are really the disease being treated (DQ06) |
| `patientsex`, `patientonsetage` | ⚪ keep raw, don't use yet | Not needed for the 3 questions; possible later filter |
| `occurcountry` | ⚪ keep raw | Possible US-only filter later |
| Dosage, lot number, narrative fields | ❌ | Not needed; adds size and risk |

---

## 4. One real report, step by step

**Report 14891719** (received 2018-05-14, serious, reported by "other health professional"):

| Drugs in the report | Role |
|---|---|
| OZEMPIC (semaglutide) | 1 · suspect |
| HUMALOG MIX75/25 (insulin lispro) | 1 · suspect |
| METFORMIN | 2 · concomitant |
| INVOKANA (canagliflozin) | 2 · concomitant |

Reactions: **Hypoglycaemia**, **Road traffic accident**.

### Step A: explode into rows (drug × reaction)
4 drugs × 2 reactions = **8 rows**. Each row gets the ingredient RxCUI from `drug_identity`.

| report | drug (ingredient) | role | reaction | keep? |
|---|---|---|---|---|
| 14891719 | semaglutide | suspect | Hypoglycaemia | ✅ ours + suspect |
| 14891719 | semaglutide | suspect | Road traffic accident | ✅ ours + suspect |
| 14891719 | insulin lispro | suspect | Hypoglycaemia | ❌ not in our 13 drugs |
| 14891719 | insulin lispro | suspect | Road traffic accident | ❌ not ours |
| 14891719 | metformin | concomitant | … (2 rows) | ❌ not ours |
| 14891719 | canagliflozin | concomitant | … (2 rows) | ❌ not ours |

**8 rows in → 2 rows out.** This is the clean dataset `faers_drug_reaction`.

> Note: insulin is very likely the real cause of the low blood sugar. FAERS can't tell us that. This is why the label says hypoglycemia is a risk "with concomitant use of insulin", and why our wording is always "reported", never "caused by".

### Step B: count (aggregate)
Add up all clean rows by **drug × reaction × quarter**. Real totals for semaglutide (openFDA, all roles, not deduplicated, so **illustrative only**):

| drug | reaction | reports |
|---|---|---|
| semaglutide | Nausea | 10,674 |
| semaglutide | Off label use | 7,325 |
| semaglutide | Impaired gastric emptying | 3,558 |
| semaglutide | Pancreatitis | 1,302 |
| semaglutide | Visual impairment | 1,449 |
| semaglutide | Depression | 1,122 |
| semaglutide | Optic ischaemic neuropathy | 869 |

This table is the **AdverseEventStat** object (one row = one drug + one reaction + one period, with count and PRR).

> **PRR** (proportional reporting ratio) = "is this reaction reported more often with this drug than with all other drugs?" PRR 1 = normal. PRR above 2 with at least 3 reports = the classic signal threshold.

### Step C: compare with the label (List 1 vs List 2)
| FAERS reaction | Reports | On label? (LLM list) | Result | Why |
|---|---|---|---|---|
| Nausea | 10,674 | ✅ Section 6 | No signal | Known, labeled |
| Pancreatitis | 1,302 | ✅ Section 5.2 | No signal | Known, labeled |
| Off label use | 7,325 | n/a | **Tagged, not ranked** | Not a medical reaction (product-use bucket, D016) |
| Impaired gastric emptying | 3,558 | ⚠️ Label says drug "delays gastric emptying" (mechanism, section 7) | **Judgment case** | Shows why the LLM must say *where* and *how* a term appears. Decide a rule. |
| Visual impairment | 1,449 | ❌ (only "blurred vision" as a low-sugar symptom; "changes in vision" under diabetic retinopathy) | **Candidate signal** | Borderline: related to labeled retinopathy. PV SME review. |
| Depression | 1,122 | ❌ 0 mentions | **Candidate signal** | Needs PRR; obesity patients have a high background rate |
| Optic ischaemic neuropathy (NAION) | 869 | ❌ 0 mentions | **Signal** | Rising sharply 2024–2026. See [merge walkthrough](merge-walkthrough-v1.md) Example B |

This one table is what the safety officer's screen shows, ranked, with links.

---

## 5. What goes into the ontology from FAERS

> **Ontology** = the "objects" the app works with (Drug, Label, Signal …) and the links between them. Datasets hold rows; the ontology turns key rows into things you can click.

| Object | One object = | Example | Built from | Links to |
|---|---|---|---|---|
| **Drug** | one ingredient | semaglutide · RxCUI 1991302 | RxNorm (`drug_identity`) | everything |
| **AdverseEventStat** | drug × reaction × quarter | semaglutide · NAION · year 2025 · 429 reports (real API count; PRR comes later from bulk files) | FAERS `faers_drug_reaction`, counted | Drug, (Signal) |
| **Label** | one label version | Rybelsus/Ozempic · setid 27f15fac · v14 | DailyMed | Drug, LabeledReaction |
| **LabeledReaction** | one reaction found on one label | Pancreatitis acute · section 5.2 · quote | LLM (Part B) | Label |
| **Signal** | drug × reaction flagged as "reported, not on label" | semaglutide · NAION · status New | Compare step | Drug, AdverseEventStat, Label, TriageDecision |
| **TriageDecision** | the safety officer's click | "Escalate to P&T" + note + who + when | Workshop write-back | Signal |

**Not an object:** the individual FAERS report. It stays as rows in the clean dataset. The Signal links to the exact query and a sample of report IDs, so "show me the 869" still works (trust rule). _Proposal, confirm when building._

---

## 6. What to do with this
1. **(you)** Open the diagram [16-faers-to-signal-v1.png](../diagrams/png/16-faers-to-signal-v1.png) and walk report 14891719 through it.
2. **(you)** Open `prototypes/data/semaglutide/dailymed_first_label.xml` in a browser. Find the "blurred vision" sentence. See why a plain search lies.
3. **(you)** Pick 1 label and list its side effects by hand. That is your first **gold set** entry, and it shows you exactly what the LLM must do.
4. **(Claude, when you say go)** Same walkthrough for DailyMed → Label/LabeledReaction, then Recalls, RxNorm, Trials.

## New data issue found while writing this
**DQ33:** openFDA tags 2018 OZEMPIC reports (injection era) as "ORAL SEMAGLUTIDE" and links them to the **tablets** label (setid 27f15fac). So the label we compare against may be the wrong product. Example: "Injection site pain" (1,023 reports) is not on the tablets label, but would be on the injection label. Fix: choose a reference label per ingredient on purpose (DQ07), and pick the injection label for semaglutide. See [register](../07-data-quality/data-issues-register.md).
