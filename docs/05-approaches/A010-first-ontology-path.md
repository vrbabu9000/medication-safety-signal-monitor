# A010 — First Ontology path (Drug, Product, Label, Recall) + triage write-back

| | |
|---|---|
| **Date** | 2026-11-04 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Ontology |
| **Status** | Kept |
| **Replaces** | none (implements the [conventions §5–6](../04-architecture/foundry-conventions/conventions-v1.md#5-ontology-contract-grain-and-keys-before-objects) target) |

## What changed
| Before | Now | Why |
|---|---|---|
| Ontology was a target contract on paper; Action save untested since step 1 | 5 object types, 5 link types and 1 Action live in Foundry; write-back proven to survive a rebuild | Build-order step 6 gate; the triage button is a brief requirement (Part C) |

## The idea in 3 lines
1. Every object type is backed by one curated dataset with one row per object (`Data/curated/ontology_*`), built by [ontology_objects.py](../../foundry/pipelines/ontology/ontology_objects.py). Keys are checked before Foundry sees them.
2. Many-to-many relationships use join datasets (Drug↔Product, Product↔Label, Recall↔Product, Recall↔Drug). The one-label-per-product choice (LD1) is a separate foreign-key link, "Reference Label".
3. Triage decisions are their own objects, created only by an Action. Decision ID, reviewer and time come from the system, not from typed text.

## How we tested it
The step 6 gate from the [build order](../04-architecture/foundry-conventions/project-build-order-v1.md), checked in Object Explorer, plus the conventions §6 acceptance check for the Action.

## Result
| Check | Result |
|---|---|
| Object counts = dataset rows | Drug 13 · Product 141 · Label 263 · Recall 25 (keys checked: 0 null, 0 duplicate) |
| Drug searchable by readable title | "Oxycodone" is the first hit for the keyword |
| Links do not multiply records | Oxycodone → 141 products, 25 recalls (= source counts) |
| Correct label version opens | OxyContin (NDA022272) → Reference Label → 1 label, v44, PLR format (trace T13) |
| Action save persists | 1 test decision created (`D-0338-2026`, monitoring); still present after a forced rebuild of the backing dataset and a reload |

## Verdict
Keep (D040 accepted 2026-11-04). The gate passed. The Ontology path is the base for step 7 (LabeledReaction) and step 8 (Signal, with the triage link moved from recall to signal).

## Design choices made on the way
- **`MSSM` name prefix** on every type. The enrollment Ontology is shared with Palantir's example types, so the prefix keeps ours easy to find and avoids name clashes.
- **TriageDecision backed by an empty curated dataset with edits on**, not by "empty datasource". That way the rebuild test means something, and the schema lives in code.
- **Action = create only** (no modify or delete). The decision history is append-only, as the conventions say. Only my user can submit for now.
- **Test decision points at a recall.** Signals don't exist yet (step 8), so `subject_type` = `recall`. The real link to Signal comes in step 8.
- **Backing transforms live in the `pipelines_clean` repo** (outputs go to `Data/curated`). That avoids a second new repository and its VS Code auto-sync problem.

## Known gaps
- No edit history on TriageDecision (warning on save). The decision objects are the audit trail. Turn edit history on if reviewers want observability views.
- The `reference label` link type was saved in the `Data/curated` folder instead of `Ontology/Links`. Cosmetic; move it.
- There is no idempotency token on the Action yet (conventions §6). Add it in step 8, with the real signal form.
- Object type descriptions are blank in Foundry. The description typed in the wizard was not kept.

## Diagram (if structure changed)
_The structure follows the existing conventions diagram ([PNG](../diagrams/png/19-foundry-ontology-conventions-v1.png) · [PDF](../diagrams/pdf/19-foundry-ontology-conventions-v1.pdf)). There is no new diagram until Signal is added in step 8._

## Persona check
- 🩺 PV SME: Products with no owner label have no Reference Label link, so step 7 can't silently compare against a generic label (G4 holds).
- 💊 Safety Officer: one click from Oxycodone to its 4 active recalls, and from OxyContin to the exact label version, is the trace she asked for. The decision form has only the fields she fills.
- 🧐 Evaluator: the gate evidence is in Foundry, not just asserted. The open item is the idempotency token.
