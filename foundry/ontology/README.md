# foundry/ontology/ — what exists in the Foundry Ontology

These types were built by hand in Ontology Manager (step 6, 2026-11-04). This file is their written record, because Foundry holds the only "source". Approach: [A010](../../docs/05-approaches/A010-first-ontology-path.md). Target contract: [conventions §5–6](../../docs/04-architecture/foundry-conventions/conventions-v1.md#5-ontology-contract-grain-and-keys-before-objects).

Ontology: `kestrel Ontology` (shared with Palantir's example types, hence the `MSSM` prefix). Saved in `Ontology/Objects` and `Ontology/Links`. All types are status Experimental.

## Object types

| Object type | Backing dataset (`Data/curated`) | Primary key | Title | Objects | Edits |
|---|---|---|---|---|---|
| MSSM Drug | `ontology_drug_drugs` | `ingredient_rxcui` | `display_name` (e.g. Oxycodone) | 13 | off |
| MSSM Product | `ontology_product_products` | `product_key` (application number, or `labeler:` key) | `display_name` (e.g. OXYCONTIN (NDA022272)) | 141 | off |
| MSSM Label | `ontology_label_labels` | `label_key` = `setid|v<version>` | `display_name` (title · v44) | 263 | off |
| MSSM Recall | `ontology_recall_recalls` | `recall_number` | `display_name` (D-0338-2026 · Class II · Ongoing) | 25 | off |
| MSSM Labeled Reaction | `ontology_labeled_reactions` (built by the AI transform, step 7) | `labeled_reaction_key` | `reaction_text` | 403 (pilot: 2 labels) | off |
| MSSM AE Stat | `ontology_ae_stats` (step 8) | `stat_key` | `display_name` | 1,382 | off |
| MSSM Signal | `ontology_signal_signals` (step 8) | `signal_key` (`rxcui|reaction|rule`) | `display_name` (Oxycodone · Myoclonus) | 271 (125 ranked) | off |
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

## Action types

| Action | Rule | Inputs | Set by the system | Who can submit |
|---|---|---|---|---|
| Create MSSM Triage Decision (`create-mssm-triage-decision`) | Create object | Subject Type, Subject Key, Evaluation Id, Decision (reviewing / dismissed / escalated / monitoring), Rationale | Decision Id = Unique Identifier · Reviewer = Current User · Decided At = Current Time | the project owner only (for now) |

How to apply it: in **Object Explorer**, open MSSM Triage Decision → **Actions** → Create. The form preview in Ontology Manager runs a **test run only** and saves nothing.

**Save test (2026-11-04):** 1 decision (`D-0338-2026`, monitoring, rationale "STEP 6 ACTION SAVE TEST") survived a forced rebuild of `ontology_triage_decisions` plus a reload. Leave it in place as evidence, or delete it before the demo.

**Workshop test (2026-11-04, step 8):** 1 decision on signal `7804|Myoclonus|prr_evans_v2` (reviewing, rationale "STEP 8 WORKSHOP TEST …", evaluation id `cbcd091262d23bd6`) submitted from the Workshop screen; still there after a full reload. Delete it before the demo, or keep it as evidence.

## Workshop module

**MSSM Safety Officer** (`ri.workshop.main.module.5468606b-d94b-4f0a-b257-a22b207de88d`, project folder `Workshop/`, published v0.2.0). Approach: [A012](../../docs/05-approaches/A012-signal-statistics-and-workshop.md) · decision D042 (accepted).

| Part | Built from |
|---|---|
| Left: **Ranked signals (not in label)** table | Variable *Ranked signals* = MSSM Signal where Is Ranked = true (125). Columns: signal, reaction, rank, reports, from mass reports (30+ drugs), PRR, PRR 95% CI low, Chi² (Yates), caution. Default sort rank ↑ |
| Right top: button **Triage this signal** | Action Create MSSM Triage Decision. Defaults: Subject Type = static "signal"; Subject Key = *Selected signal key* (object property of the table's active object); Evaluation Id = *Selected evaluation id*. All three locked (Disabled); the officer picks Decision and writes Rationale |
| Right middle: decisions for this signal | Variable *Decisions for selected signal* = MSSM Triage Decision where Subject Key = Selected signal key |
| Right bottom: full signal record | Property list of the active signal: 22 properties in reading order with plain labels. Why flagged (reaction, reports, PRR + 95% CI, χ², caution, mass reports set aside) → label check (status, reference labels searched, labels also read by AI, method) → trace (rank, bucket, FAERS window, rule version, evaluation id, signal key, stat key, RxCUI) |

**Polish (2026-11-04, v0.3):** number format on MSSM Signal properties in Ontology Manager (Display → Numeric formatting → Maximum fraction digits: PRR 1, CI low/high 2, χ² 1, mass share 2). Decisions table: row height Absolute 160 px, fit columns, 5 columns. Evidence list reordered and relabelled. The last two were done in each widget's JSON config (`</>` → edit → *Validate and save*).

Still open: reviewer shows a user ID; links from a signal to the labels that were searched.
