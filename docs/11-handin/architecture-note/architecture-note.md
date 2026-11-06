# Architecture note (hand-in 2): text version

**Medication Safety Signal Monitor: how the data becomes a flag you can trust**

This is the plain-text twin of the one-page PDF. The PDF is the hand-in: [architecture-note.pdf](architecture-note.pdf) (one page, US Letter landscape). Page preview: [architecture-note.png](architecture-note.png).
Built by [architecture_note.py](architecture_note.py). Every number comes from [numbers.json](../numbers.json), captured 2026-11-05T07:50Z.

It is built for the hospital pharmacy safety officer's three morning questions:
1. Which adverse events are reported that the label does not mention?
2. Which drugs have an active recall?
3. What changed?

Trust rule: every flag traces to its source: the label versions searched (DailyMed) and the FDA recall record open in one click; the FAERS case reports are reachable by query, not yet from her screen.

## The picture: data flow and ontology

Diagram 38: [PNG](../../diagrams/png/38-handin-architecture-onepage-v1.png) · [PDF](../../diagrams/pdf/38-handin-architecture-onepage-v1.pdf) · [draw.io](../../diagrams/drawio/38-handin-architecture-onepage-v1.drawio) (to get a Visio file, open it in draw.io, then *File → Export as → VSDX*). The detailed versions are diagram 30 (data flow) and diagram 31 (ontology, with the cardinality of each link): see [README-handin](../../diagrams/README-handin.md).

- **Part 1, data flow.** Four public sources (DailyMed, FAERS, RxNorm, openFDA) land in Data/raw as they are received. Every drug name, salt, product and NDC package then goes through **one** identity dataset (`clean_drug_identity`) to an ingredient RxCUI. From there it moves into clean, then curated (signals, AI extraction, synonyms, change feed, monitoring).
- **Part 2, ontology.** There are 10 object types, each backed by a curated dataset: Drug, Product, Label, Labeled Reaction, Recall, AE Stat, Signal, Triage Decision, Change Event and Source Status. The lines between them are link types. The Workshop app's triage button runs the one Action, and that Action creates a Triage Decision.

Glossary:

| Term | Meaning |
|---|---|
| FAERS | The FDA's database of adverse event reports |
| DailyMed | Official drug labels (SPL is the label's XML format) |
| RxCUI | RxNorm's ID for a drug |
| NDC | The code for a drug package |
| PRR | Proportional reporting ratio: how much more often a reaction is reported for this drug than for others |
| Ontology | Foundry's layer of objects and links that the app reads |
| Workshop | Foundry's app builder |
| Action | A form that writes to the Ontology |

## Four decisions that mattered most

**Why these four:** each one decides whether a flag can be trusted, and each answers one judging row of the brief: Architecture, Data judgment, AI reliability and Application. The runners-up were keeping the full FAERS rebuild as the input to signals (D044, optimization log O2) and the focus buckets (D016 v3).

| # | Decision | What we chose | Why | Evidence |
|---|---|---|---|---|
| 1 | **Drug identity is resolved once, in the clean layer** (D020; D027 proposed) | One dataset, `clean_drug_identity`, maps every drug name, salt, product and NDC package to an exact ingredient RxCUI. Every later step joins it, so nothing matches names again. | Counts belong to ingredients; labels and recalls belong to products. One fix reaches every number. | Substring matching ("morphine" also hit apomorphine and diamorphine) added 50% false morphine rows (DQ34). OBSERVED |
| 2 | **FAERS counts each current case once, suspects only** (D021, D022, D023 v2) | The latest case version wins, and FDA deletes apply to all history. Only suspect drugs count, once per report. Duplicate patients are folded, and reports that list 30+ drugs leave the main count. | FAERS re-files and deletes cases, and mass re-filings create fake signals. | Appending quarters gave +8.7% phantom rows (DQ36). Q2 replaced 26,681 cases and deleted 655. OBSERVED |
| 3 | **"Not in label" is a 3-step check, and the AI must quote** (D037 proposed; D041, D043) | A FAERS term is in the label if (1) an AI-extracted term matches it and the code finds its quote in that section; else (2) its exact text is in a safety section; else (3) a synonym that a person banded. | Every "not in label" must name the exact label versions searched, and every AI match must quote its passage. | 448/448 quotes grounded. F1 0.97 vs the proposed D015 target of 0.85, on a 35-item answer key (2 labels) written by Claude (pharmacist review pending). Synonyms plus wider buckets cut the ranked queue from 1,355 at step 9 to 1,073. OBSERVED |
| 4 | **Triage is its own write-back object; changes are dated** (D040, D042; D045 proposed) | Each decision is its own object, made only by an Action and tied to the signal and its `evaluation_id` (a hash of the evidence). A change feed dates each change to a signal, recall or label. | A status column on Signal would be wiped by the next rebuild, and the sources update on different clocks. | A decision survived a full rebuild (step 6 gate). There are 2,898 change events, and 0 false ones appeared after a rebuild. OBSERVED |

## What we chose not to do

- **No MedDRA licence** (MedDRA is the paid dictionary of reaction terms). Keyword buckets (D016 v3) and a reviewed synonym table stand in for it.
- **No causality, no patient data.** A signal means a reaction is reported more often than expected (Evans rule; D006 proposed) and is not in the label, or only possibly in label (108: found only through a medium-band synonym). The 1,073 ranked signals are a review queue, not findings.
- **Signals do not read incremental FAERS yet.** It matches the full rebuild row for row, but it took 88 s vs 32 s at 2 quarters (O2). Re-measure at 4+ quarters.
- **AI is kept to 2 pilot labels, and there is no AI judge per signal,** until a pharmacist checks the answer key.
- **No ClinicalTrials.gov, OnSIDES, daily FAERS scraping or label-change backtest** (D031 cut list; D029 proposed).
- **No build schedule yet** (we refresh when a build runs), no per-user "last reviewed" bookmark, no live drift. Drift is a historical replay for now. Known flaw: an unused duplicate Signal → Drug link type.

## Build facts

| Item | Value |
|---|---|
| Drugs | 13 (8 opioids + 5 GLP-1s) |
| Public sources | 4: FAERS 2026Q1–2026Q2, DailyMed, openFDA, RxNorm |
| Current FAERS cases | 792,346 |
| Label versions | 1,321 (1,231 carry an effective date) |
| Recalls | 900 (126 active) |
| Signals | 1,952 (1,073 ranked) |
| Ontology | 10 object types, 1 Action |
| App | Workshop v0.9.0, 4 pages |
| Monitoring | 21 checks per build |

For more detail, see diagrams 30–38, reports R01–R09 and [DECISIONS.md](../../06-decisions/DECISIONS.md).
