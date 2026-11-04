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
| MSSM Triage Decision | `ontology_triage_decisions` (empty on purpose) | `decision_id` (generated UUID) | `subject_key` | created by the Action only | **on** |

## Link types

| Link | Kind | Backed by | Names (each side) |
|---|---|---|---|
| Drug ↔ Product | many-to-many | `ontology_link_drug_product` | MSSM Products / MSSM Drugs |
| Product ↔ Label | many-to-many | `ontology_link_product_label` (every approval id in the label XML) | MSSM Labels / MSSM Products |
| Product → Label | many-to-one, foreign key `reference_label_key` | product dataset | Reference Label (`referenceLabel`) / Reference For Products (`referenceForProducts`) |
| Recall ↔ Product | many-to-many | `ontology_link_recall_product` (high/medium-confidence NDC matches) | MSSM Products / MSSM Recalls |
| Recall ↔ Drug | many-to-many | `ontology_link_recall_drug` (ingredient named in the recall text) | MSSM Drugs / MSSM Recalls |

## Action types

| Action | Rule | Inputs | Set by the system | Who can submit |
|---|---|---|---|---|
| Create MSSM Triage Decision (`create-mssm-triage-decision`) | Create object | Subject Type, Subject Key, Evaluation Id, Decision (reviewing / dismissed / escalated / monitoring), Rationale | Decision Id = Unique Identifier · Reviewer = Current User · Decided At = Current Time | the project owner only (for now) |

How to apply it: in **Object Explorer**, open MSSM Triage Decision → **Actions** → Create. The form preview in Ontology Manager runs a **test run only** and saves nothing.

**Save test (2026-11-04):** 1 decision (`D-0338-2026`, monitoring, rationale "STEP 6 ACTION SAVE TEST") survived a forced rebuild of `ontology_triage_decisions` plus a reload. Leave it in place as evidence, or delete it before the demo.
