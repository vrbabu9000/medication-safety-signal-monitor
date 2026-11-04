# Data Forge tutorial research — 2026-10-31

**Requested source:** [Data Forge playlists](https://www.youtube.com/@DataForge2026/playlists).

**Method:** inspected the channel and introductory playlist in YouTube. Read the English auto-generated transcripts for episodes 3, 6, and 9. Cross-checked technical rules in Palantir's official documentation. Auto-captions can mishear technical words. Notes below are paraphrases; full transcripts are not copied into the repository.

**Coverage limit:** this is a focused conventions review, not a claim to have watched every video. Other episode titles/links were verified in the playlist; their content was not reviewed. Enrollment features and permissions were not tested. The advanced/masterclass playlist contents were not reviewed.

## 1. Playlist inventory and useful study order

The channel page exposed five playlists: **Introduction to Palantir Foundry**, **Advance Palantir Foundry**, **Palantir Foundry Masterclass: SkyOps Control Tower**, **Palantir Foundry Developer Interview Series**, and **PySpark Mastery: From Terminal to Terabytes**. Some non-introductory playlist identifiers were abbreviated in the page; use the channel link to open them rather than guessing identifiers.

[Introduction to Palantir Foundry](https://www.youtube.com/playlist?list=PLmcRGjEJbMTU0hmxv4BESA-R9iAqY-afj) contained 11 videos at inspection:

| Episode | Topic / direct source | Research status |
|---|---|---|
| 1 | [What is Palantir Foundry?](https://www.youtube.com/watch?v=CkfYya_a21k) | Title/link verified |
| 2 | [Free setup / AIP Developer Tier](https://www.youtube.com/watch?v=N-YJXvGmQGM) | Title/link verified |
| 3 | [Organize your first project](https://www.youtube.com/watch?v=LgmhVY-_rlE) | Transcript + description reviewed |
| 4 | [Data Connection / AWS S3](https://www.youtube.com/watch?v=DlMaltp6w-A) | Title/link verified |
| 5 | [Dataset Preview](https://www.youtube.com/watch?v=z60OBU8dFbw) | Title/link verified |
| 6 | [Pipeline Builder](https://www.youtube.com/watch?v=t4Db6n5hpCI) | Transcript reviewed |
| 7 | [Code Repositories part 1](https://www.youtube.com/watch?v=_H6JISpq2DQ) | Title/link verified |
| 8 | [Code Repositories part 2](https://www.youtube.com/watch?v=95FtWxv5-qg) | Title/link verified |
| 9 | [Ontology Manager: objects, links, Actions](https://www.youtube.com/watch?v=b-oxw_CP8p8) | Transcript reviewed |
| 10 | [Workshop](https://www.youtube.com/watch?v=QOG3VoN1mXU) | Title/link verified |
| 11 | [Contour](https://www.youtube.com/watch?v=t8BPjKaKcIc) | Title/link verified |

## 2. Reviewed passages and our application

### Episode 3 — organization

| Timestamp | Lesson, paraphrased | Our use |
|---|---|---|
| [1:36](https://www.youtube.com/watch?v=LgmhVY-_rlE&t=96s) | Establish resource organization before building | Minimal folder layout before ingestion |
| [2:03](https://www.youtube.com/watch?v=LgmhVY-_rlE&t=123s) | Raw is bronze; cleaned data is silver | Keep raw/clean names and explain the medallion mapping |
| [2:48](https://www.youtube.com/watch?v=LgmhVY-_rlE&t=168s) | Separate transformation resources from datasets | Pipelines holds logic; Data holds outputs |
| [3:55](https://www.youtube.com/watch?v=LgmhVY-_rlE&t=235s) | Group ontology, app, analysis, and AI resources | Separate object/link/Action notes and operational app resources |

The description and spoken folder labels differ slightly. The transcript also mishears an AI validation folder near 6:51. Our `AIP/Evals` name is an explicit project choice, corroborated by Palantir's Evals product; it is not a verbatim transcript label.

### Episode 6 — medallion pipeline

| Timestamp | Lesson, paraphrased | Our use |
|---|---|---|
| [1:28](https://www.youtube.com/watch?v=t4Db6n5hpCI&t=88s) | Preserve incoming data before transforming it | Versioned raw payloads and manifests |
| [2:43](https://www.youtube.com/watch?v=t4Db6n5hpCI&t=163s) | Silver applies cleaning transformations | Typed source tables with visible rejection reasons |
| [3:28](https://www.youtube.com/watch?v=t4Db6n5hpCI&t=208s) | Gold adds useful domain features for downstream use | Aggregate reaction facts and object-ready datasets |
| [17:16](https://www.youtube.com/watch?v=t4Db6n5hpCI&t=1036s) | Publish pipeline outputs for later object mapping | Inspect curated datasets before object publication |

The example is introductory batch processing. It does not establish a correct algorithm for FAERS corrections, deletions, or historical denominators. Its empty-transaction setting is a demonstration choice, not our universal default. Consult official incremental documentation before setting it.

### Episode 9 — ontology conventions

| Timestamp | Lesson, paraphrased | Our use |
|---|---|---|
| [3:03](https://www.youtube.com/watch?v=b-oxw_CP8p8&t=183s) | Prepare clean data and valid keys first | Full key checks before mapping datasets |
| [4:19](https://www.youtube.com/watch?v=b-oxw_CP8p8&t=259s) | Distinguish API/display/plural names; keep API contracts stable | Explicit name mapping table |
| [7:26](https://www.youtube.com/watch?v=b-oxw_CP8p8&t=446s) | Choose meaningful titles and search fields | Ingredient names instead of opaque IDs in search |
| [9:04](https://www.youtube.com/watch?v=b-oxw_CP8p8&t=544s) | Curate properties and document them | Publish only useful business facts |

Two cautions: the spoken claim that API names are fixed overstates the platform restriction; Palantir documents editing them, though changing consumers requires care. The live example selects an ID as title despite earlier advice; we use a readable title. Its broad Action permissions are not copied into this project.

## 3. Official sources checked

| Source | What it verifies |
|---|---|
| [Recommended project structure](https://www.palantir.com/docs/foundry/building-pipelines/recommended-project-structure) | Source cleanup separated from reusable transformation projects and Ontology hydration |
| [Ontology structural guidance](https://www.palantir.com/docs/foundry/ontology/ontology-structural-guidance) | Business nouns, meaningful directional links, relationship metadata |
| [Create object type](https://www.palantir.com/docs/foundry/object-link-types/create-object-type) | API casing, unique keys, title keys, type IDs, API-name editing |
| [Pipeline Builder core concepts](https://www.palantir.com/docs/foundry/pipeline-builder/core-concepts) | Datasets, transformations, and deployment concepts |
| [Incremental input modes](https://www.palantir.com/docs/foundry/pipeline-builder/datasets-computation-modes-for-batch) | Additive input restrictions; transaction-scoped aggregates; snapshot-lookup replay caveat |
| [Output write modes](https://www.palantir.com/docs/foundry/pipeline-builder/outputs-add-dataset-output) | Replace/remove behavior; deterministic dedup must precede output |
| [Create incremental pipeline](https://www.palantir.com/docs/foundry/building-pipelines/create-incremental-pipeline-pb) | Incremental setup and replay |
| [Action getting started](https://www.palantir.com/docs/foundry/action-types/getting-started) | Action configuration and test runs |
| [Action permissions](https://www.palantir.com/docs/foundry/action-types/permissions) | Submission permissions and object editing access |
| [Allow editing](https://www.palantir.com/docs/foundry/object-link-types/allow-editing) | Ontology edits and backing data distinction |
| [AIP Evals](https://www.palantir.com/docs/foundry/aip-evals/overview), [suite setup](https://www.palantir.com/docs/foundry/aip-evals/create-suite) | Version comparisons, custom evaluators, test cases |
| [Health check types](https://www.palantir.com/docs/foundry/health-checks/check-types) | Different freshness meanings and build-time expectations |

## 4. What comes from us

The `mssm` resource prefix, existing `raw/clean/ontology` repository layout, proposed object grains/composite keys, separate human decision history, expanded extraction cache key, source manifests, and numbered build gates are project adaptations. They are not attributed to the instructor or presented as mandatory Palantir defaults.

Domain rules come from our [decision log](../../06-decisions/DECISIONS.md), [source profiles](../../07-data-quality/source-profiles/README.md), and [brief](../../00-brief/brief-summary.md). Proposed decisions remain proposed.
