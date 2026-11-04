# Foundry conventions — start here

**Updated:** 2026-10-31 · **Stage:** Define → Prototype · **Status:** reference standard; not evidence of a deployed build.

Use this folder while learning and building Medication Safety Signal Monitor.

| Read in this order | Use it for |
|---|---|
| 1. [Conventions](conventions-v1.md) | Folder layout, bronze/silver/gold, dataset names, ontology names, keys, links, Actions, and checks |
| 2. [Project build order](project-build-order-v1.md) | What to do first, second, and next; stop conditions for each step |
| 3. [Tutorial notes and sources](tutorial-research-2026-10-31.md) | Verified Data Forge episodes, timestamps, official documentation, and limits of this research |

**Recommendation:** keep the existing `raw` → `clean` → `ontology` code layout. Use bronze, silver, and gold to explain the responsibilities of the data, then map curated datasets into the Ontology. An Ontology models business things, their relationships, and the actions users take.

**First hands-on task:** complete the access check in build step 1. Then build one drug through to one source-linked screen before expanding the pilot.

The [active Compass](../../../COMPASS.md) controls project status. [D031 v3](../../06-decisions/DECISIONS.md) is the working reduced-scope plan, but is still marked proposed. Documents in `proposals/` are not adopted. This guide does not approve those drafts or change clinical signal rules.

**Diagrams:** [data flow PNG](../../diagrams/png/18-foundry-medallion-v1.png) · [ontology PNG](../../diagrams/png/19-foundry-ontology-conventions-v1.png) · [editable draw.io sources](../diagrams/).
