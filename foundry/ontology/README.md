# foundry/ontology/ — what exists in the Foundry Ontology

These types were built by hand in Ontology Manager (step 6, 2026-11-04). This file is their written record, because Foundry holds the only "source". Approach: [A010](../../docs/05-approaches/A010-first-ontology-path.md). Target contract: [conventions §5–6](../../docs/04-architecture/foundry-conventions/conventions-v1.md#5-ontology-contract-grain-and-keys-before-objects).

Ontology: `kestrel Ontology` (shared with Palantir's example types, hence the `MSSM` prefix). Saved in `Ontology/Objects` and `Ontology/Links`. All types are status Experimental.

## Object types

Object counts as of the baseline gate, 2026-11-05 (13-drug formulary).

| Object type | Backing dataset (`Data/curated`) | Primary key | Title | Objects | Edits |
|---|---|---|---|---|---|
| MSSM Drug | `ontology_drug_drugs` | `ingredient_rxcui` | `display_name` (e.g. Oxycodone) | 13 | off |
| MSSM Product | `ontology_product_products` | `product_key` (application number, or `labeler:` key) | `display_name` (e.g. OXYCONTIN (NDA022272)) | 658 | off |
| MSSM Label | `ontology_label_labels` | `label_key` = `setid|v<version>` | `display_name` (title · v44) | 1,321 | off |
| MSSM Recall | `ontology_recall_recalls` | `recall_number` | `display_name` (D-0338-2026 · Class II · Ongoing) | 900 | off |
| MSSM Labeled Reaction | `ontology_labeled_reactions` (built by the AI transform, step 7) | `labeled_reaction_key` | `reaction_text` | 745 (5 labels: 2 oxycodone pilot + 3 semaglutide, D041 v2, prompt p2) | off |
| MSSM AE Stat | `ontology_ae_stats` (step 8) | `stat_key` | `display_name` | 14,921 | off |
| MSSM Signal | `ontology_signal_signals` (step 8) | `signal_key` (`rxcui|reaction|rule`) | `display_name` (Oxycodone · Myoclonus) | 1,952 (1,073 ranked) | off |
| MSSM Change Event | `ontology_change_events` (step 11, D045) | `event_id` (hash of type, key, drug, change, detail, date) | `display_name` | 2,898 at first build | off |
| MSSM Source Status | `ontology_source_status` (step 11, D045) | `source` | `source` | 4 | off |
| MSSM Triage Decision | `ontology_triage_decisions` (empty on purpose) | `decision_id` (generated UUID) | `subject_key` | created by the Action only | **on** |

## Link types

| Link | Kind | Backed by | Names (each side) |
|---|---|---|---|
| Drug ↔ Product | many-to-many | `ontology_link_drug_product` | MSSM Products / MSSM Drugs |
| Product ↔ Label | many-to-many | `ontology_link_product_label` (every approval id in the label XML) | MSSM Labels / MSSM Products |
| Product → Label | many-to-one, foreign key `reference_label_key` | product dataset | Reference Label (`referenceLabel`) / Reference For Products (`referenceForProducts`) |
| Recall ↔ Product | many-to-many | `ontology_link_recall_product` (high/medium-confidence NDC matches) | MSSM Products / MSSM Recalls |
| Labeled Reaction → Label | many-to-one, foreign key `label_key` | labeled reactions dataset | MSSM Label / MSSM Labeled Reactions |
| Signal → Drug | many-to-one, foreign key `ingredient_rxcui` | signal dataset | MSSM Drug / MSSM Signals |
| AE Stat → Drug | many-to-one, foreign key `ingredient_rxcui` | AE stat dataset | MSSM Drug / MSSM AE Stats |
| Signal → AE Stat | many-to-one, foreign key `stat_key` | signal dataset | MSSM AE Stat / MSSM Signals |
| Triage Decision → Signal | many-to-one, foreign key `subject_key` | triage dataset | MSSM Signal / MSSM Triage Decisions |
| Recall ↔ Drug | many-to-many | `ontology_link_recall_drug` (ingredient named in the recall text) | MSSM Drugs / MSSM Recalls |

A duplicate Signal → Drug link type ("Signals of drug" / "Drug of signal", added by mistake on 2026-11-05) was **deleted on 2026-11-06** with the owner's OK. Before deleting, we checked that no Workshop variable used it (the page 1 "Reference labels searched" panel uses the original Signal → Drug link) and that its usage log showed only one Object Explorer read. The Ontology now has **10 MSSM link types**.

## Action types

| Action | Rule | Inputs | Set by the system | Who can submit |
|---|---|---|---|---|
| Create MSSM Triage Decision (`create-mssm-triage-decision`) | Create object | Subject Type, Subject Key, Evaluation Id, Decision (reviewing / dismissed / escalated / monitoring), Rationale | Decision Id = Unique Identifier · Reviewer = Current User · Decided At = Current Time | the project owner only (for now) |

How to apply it: in **Object Explorer**, open MSSM Triage Decision → **Actions** → Create. The form preview in Ontology Manager runs a **test run only** and saves nothing.

**Save test (2026-11-04):** 1 decision (`D-0338-2026`, monitoring, rationale "STEP 6 ACTION SAVE TEST") survived a forced rebuild of `ontology_triage_decisions` plus a reload. Leave it in place as evidence, or delete it before the demo.

**Workshop test (2026-11-04, step 8):** 1 decision on signal `7804|Myoclonus|prr_evans_v2` (reviewing, rationale "STEP 8 WORKSHOP TEST …", evaluation id `cbcd091262d23bd6`) submitted from the Workshop screen; still there after a full reload. Delete it before the demo, or keep it as evidence.

## Workshop module

**MSSM Safety Officer** (header title "MSSM · Morning safety review"; `ri.workshop.main.module.5468606b-d94b-4f0a-b257-a22b207de88d`, project folder `Workshop/`, published v0.6+; **v0.10.0** on 2026-11-06). Approaches: [A012](../../docs/05-approaches/A012-signal-statistics-and-workshop.md) (page 1), [A016](../../docs/05-approaches/A016-three-question-screen.md) (pages 0, 2, 3) · decisions D042, D045.

Four pages, switched by a **Tabs** widget in the module header (each tab's on-click event = *Switch to page*). Page names sort alphabetically in the editor, so they carry a number.

| Page (tab) | Answers | Built from |
|---|---|---|
| **0 · Morning brief** (default) | All three questions at a glance, plus how fresh each source is | One **Metric card** widget, three metrics, each an *Object set aggregation* (Count) variable: *Count ranked signals* over *Ranked signals* (1,073) · *Count active recalls* over *Active recalls* = *All recalls* where Is Active = true (126) · *Count changes last 30 days* over *Changes last 30 days* = *All changes* where Event Date is from 30 days ago, relative to today (26 on 2026-11-05). Below: object table on MSSM Source Status (source, feeds, as of, refresh, pulled at, rows) |
| **1 · Not in label** | Q1 | Unchanged from step 8/9: drug filter → ranked signals table → triage button → decisions → full signal record (see below) |
| **2 · Recalls** | Q2 | Filter list (Pills) on *All recalls* (MSSM Recall, 900): **Drug** = linked MSSM Drug's Display Name (uses the Recall ↔ Drug link, so a recall that names two drugs shows under both) · Is Active · Classification. Table *Recalls for chosen drugs* (recall, class, status, reported, firm, reason, product, matched products, found by drug search), sorted Report Date ↓. Right: property list of the selected recall (15 fields in reading order, "Class (I = most serious)") |
| **3 · What changed** | Q3 | Left (300 px): filter list on *All changes* (MSSM Change Event): Ingredient Name · **Event Date** (histogram + start/end date = "since my last review") · Entity Type · Change. Right: table *Changes for chosen filters* (date, drug, what, change, detail, item, source, found by), sorted Event Date ↓ |

How it was built fast: object-table columns and property-list fields were written straight into each widget's JSON (`</>` → edit → *Validate and save*). Column entries are `{"type":"property","property":{"propertyType":{"objectTypeId":<type id>,"propertyTypeId":<column name>}}}`; the type id is in the object type's URL in Ontology Manager. Typing into the JSON box by accident edits it: close it without *Validate and save* to discard.

### Page 1 detail (step 8, unchanged)

| Part | Built from |
|---|---|
| Left top: **drug filter** (pill "Ingredient Name", 2026-11-05) | Filter list on *Ranked signals*, showing ranked counts per drug; its output filters *Ranked signals for chosen drugs*. Row height Absolute 64 px |
| Left: **Ranked signals (not in label)** table | Variable *Ranked signals for chosen drugs* = *Ranked signals* + the drug filter. *Ranked signals* = MSSM Signal where Is Ranked = true. Columns: signal, reaction, rank, reports, from mass reports (30+ drugs), PRR, PRR 95% CI low, Chi² (Yates), caution. Default sort rank ↑ |
| Right top: button **Triage this signal** | Action Create MSSM Triage Decision. Defaults: Subject Type = static "signal"; Subject Key = *Selected signal key* (object property of the table's active object); Evaluation Id = *Selected evaluation id*. All three locked (Disabled); the officer picks Decision and writes Rationale |
| Right middle: decisions for this signal | Variable *Decisions for selected signal* = MSSM Triage Decision where Subject Key = Selected signal key |
| Right bottom: full signal record | Property list of the active signal: 22 properties in reading order with plain labels. Why flagged → label check → trace |
| Right, below the record: **Reference labels searched** (step 11) | Variable *Reference labels searched for selected signal* = active signal → MSSM Drug (original Signal → Drug link) → MSSM Product → Reference Label. Columns: label, version, effective, safety sections, DailyMed link |
| Right, last: **What the AI read in these labels** (2026-11-06, v0.10.0, D041 v2) | Variable *AI reactions quoted from labels searched* = *Reference labels searched…* → MSSM Labeled Reaction. Columns: reaction text, section, quote (word for word from the label), label key. For NAION: 297 rows from the 3 semaglutide labels; no optic-nerve term among them. The **Evidence and triage** section has *Enable scrolling* on, so the triage button keeps its height (a fixed-height table had squeezed it) |

**Polish (2026-11-04, v0.3):** number format on MSSM Signal properties in Ontology Manager (Display → Numeric formatting → Maximum fraction digits: PRR 1, CI low/high 2, χ² 1, mass share 2). Decisions table: row height Absolute 160 px.

Still open: reviewer shows a user ID; section titles on page 2 still read "Section"; no dedicated Signal → Label link type (the panels walk existing links); a Health page for `monitoring_checks` (needs a key column and an object type).

Why two variables on page 1: the filter list must read the unfiltered set, or the filter would feed back into itself and every other drug would disappear from its own choices. Pages 2 and 3 follow the same pattern (*All recalls* → *Recalls for chosen drugs*, *All changes* → *Changes for chosen filters*).
