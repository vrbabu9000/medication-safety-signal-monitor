# A007 — Foundry medallion and ontology conventions

| | |
|---|---|
| **Date** | 2026-10-31 |
| **Design-thinking stage** | Define → Prototype |
| **Area** | Pipelines / Ontology / Process |
| **Status** | Kept — reference standard; deployment validation pending |
| **Replaces** | None; consolidates existing conventions. A006 is reserved by a non-adopted proposal. |

## What changed

| Before | Now | Why |
|---|---|---|
| Raw→clean→ontology names and scattered learning notes | [One reference folder](../04-architecture/foundry-conventions/README.md) maps bronze/silver/gold to the existing layout and adds naming/key rules | A learner needs clear boundaries and reusable examples |
| Dated backlog without a learning sequence | Dependency-based build order with proof required at every step | Makes first/second/next explicit without inventing completion or deadline approval |

## The idea in 3 lines

1. Preserve sources, validate shared identity, then publish curated object backing datasets.
2. Define object meaning, grain, keys, and links before building the app.
3. Learn each tool immediately before using it; prove one complete workflow before expanding.

## How we tested it

Read three Data Forge auto-generated transcripts (episodes 3, 6, 9), inspected the 11-video introductory playlist, and cross-checked platform claims with official Palantir documentation. Reviewed consistency against active Decisions/Compass/Backlog. Checked new local links and diagram sources. See [research record](../04-architecture/foundry-conventions/tutorial-research-2026-10-31.md).

## Result

Before: no consolidated tutorial-based reference. Now: conventions, 12-step project roadmap, source notes, and two diagrams. No Foundry deployment or performance measurement was performed. All runtime gains remain unmeasured.

## Verdict

**Keep** as the working reference. Verify actual resource capabilities, keys, matching, and Action persistence during the build. This does not accept D020–D029/D031 v3 or adopt the parked six-day proposal.

## Diagram

[Medallion PNG](../diagrams/png/18-foundry-medallion-v1.png) · [ontology PNG](../diagrams/png/19-foundry-ontology-conventions-v1.png). Mermaid is included in the convention document and saved in `docs/diagrams/src/`; editable draw.io is in `docs/04-architecture/diagrams/`. New documentation follows the current AGENTS.md request for inline Mermaid while retaining image/PDF views.

## Persona check

- 🏗️ Architect: keep data responsibilities separate from business objects; validate product grain before keys.
- 🔧 Data engineer: append-only raw is different from current case state; test corrections, deletes, replays, and changed lookups.
- 🩺 PV SME: incomplete label evidence remains uncertain; a candidate signal does not establish causation.
- 💊 Safety officer: readable titles, source dates, exact passages, and persistent triage support the morning workflow.
- 🧐 Evaluator: clear learning order and checkable gates; no deployment or speed claim without evidence.
