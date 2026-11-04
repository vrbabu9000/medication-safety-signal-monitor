# Project build order v1 — learn, build, prove

**Date:** 2026-10-31 · **Stage:** Define → Prototype → Test · **Status:** dependency roadmap, not a new dated delivery commitment.

**Recommendation:** build one complete path first: one ingredient → correct product/label → grounded extraction → source-linked candidate → saved triage decision. Then expand to the agreed pilot scope. Do not wait to finish every dataset before testing one screen.

The [Compass](../../../COMPASS.md) and [Backlog](../../10-delivery/BACKLOG.md) remain the status records. Their Oct 29–30 build tasks have no completion evidence in the active repository. This document does not infer that those tasks ran. The Nov 4 demo remains pending boss confirmation. The former 76% capacity estimate is historical and has not been recalculated.

## 1. First, second, and next

**How to use:** execute in numeric order. Each row has a proof requirement; do not advance past a failed gate. “You” means hands-on in your Foundry enrollment; “Codex” means preparation and review in this repository. No Foundry build is performed by this document.

| # | Stage / owner | Do this | Learn just before doing it | Done when / evidence | Backlog |
|---|---|---|---|---|---|
| **1** | Define · you + Codex | Confirm active scope/decisions. Check Foundry access, Pipeline Builder, Ontology Manager, Workshop, AIP Logic/model access, and permission to submit an Action. | [Setup, ep. 2](https://www.youtube.com/watch?v=N-YJXvGmQGM) | Record access results, actual resource links, quotas/errors, and unresolved decisions. AIP or Action failure is a blocker, not an assumed feature. | E5, B1 |
| **2** | Define · you + Codex | Create the minimal [folder layout](conventions-v1.md#3-foundry-folders-and-local-repository-folders). Write dataset grains and object/key contracts before publishing objects. | [Organization, ep. 3](https://www.youtube.com/watch?v=LgmhVY-_rlE) | Resource names and ownership agreed; Product grain and label matching ambiguity explicitly identified. | F1, B2 |
| **3** | Prototype · you; Codex prepares schemas | Land small public samples for FAERS, DailyMed, FDA enforcement, and RxNorm. Add Drugs@FDA/NDC bridge samples where required. Preserve original label text/XML and retrieval metadata. | [Data Connection, ep. 4](https://www.youtube.com/watch?v=DlMaltp6w-A); [Dataset Preview, ep. 5](https://www.youtube.com/watch?v=z60OBU8dFbw) | Four core sources inspectable in raw; source manifests and explicit schemas captured. Retain the unstructured label content, not only extracted fields. No AWS/S3 account is required just to copy the tutorial. | B1, B4, B5 |
| **4** | Prototype · you + Codex | Build the shared drug identity and product/label mapping. Resolve exact ingredients once. Validate route/formulation and combination-product cases. | [Pipeline Builder, ep. 6](https://www.youtube.com/watch?v=t4Db6n5hpCI); identity [A005](../../05-approaches/A005-source-selection-and-merge.md) | Uniqueness and join-cardinality checks pass; match/ambiguous/unmatched counts saved. Application number alone is not accepted as a product key without profiling. | B2 |
| **5** | Prototype · you + Codex | Build a small, correct silver baseline: FAERS case versions/deletes, label sections, recall normalization. Carry evidence references into curated outputs. | [Code Repositories, ep. 7](https://www.youtube.com/watch?v=_H6JISpq2DQ), [ep. 8](https://www.youtube.com/watch?v=95FtWxv5-qg) if custom state logic is needed | Full-rebuild reference results saved. Quarter two can correct quarter one. Unknown recall applicability is visible. A small FAERS sample is labelled plumbing-only; it cannot validate production signal rates. | B3–B5 |
| **6** | Prototype · you + Codex | Publish the first small Ontology path: Drug, validated Product, versioned Label, Recall where matched. Check both ends of each link. | [Ontology Manager, ep. 9](https://www.youtube.com/watch?v=b-oxw_CP8p8) | Drug is searchable by readable title; correct label version/route opens; links do not multiply records; keys have no nulls or duplicates. | B6 |
| **7** | Prototype → Test · you + Codex | Run label extraction on a few sections. Save exact quotes and configuration. Add `LabeledReaction`. Hand-check outputs and define the gold set before broad execution. | [AIP Evals official guide](https://www.palantir.com/docs/foundry/aip-evals/overview) | Grounded assertions and failures are distinct; unchanged input triggers zero fresh model calls; sample metrics and errors saved. | B7, start B8 |
| **8** | Prototype · you + Codex | Add aggregate statistics and one explainable signal candidate, then show it in Workshop with source evidence and a triage Action. | [Workshop, ep. 10](https://www.youtube.com/watch?v=QOG3VoN1mXU) | One complete flow works: inspect → open label passage → compare reaction evidence → submit decision → reload and see it persist. Fixture signals must be visibly identified as fixtures. | B6, B9, early B10 |
| **9** | Prototype → Test · you + Codex | Expand the same path to the confirmed pilot formulary and required source periods. Apply the selected suspect-role, identity, duplicate, and label-comparison rules. | Our [conventions](conventions-v1.md#5-ontology-contract-grain-and-keys-before-objects) | Counts reconcile, mapping coverage is reported, and denominator/reference population is preserved. The working cut plan is 11 drugs; the accepted baseline was 13. Resolve the proposed cut before claiming final scope. | B2–B10 |
| **10** | Test · you + Codex | Prove at least one incremental pipeline. Test FAERS replacement/deletion/replay behavior against the saved full-rebuild baseline. Measure extraction cache behavior too. | [Official incremental tutorial](https://www.palantir.com/docs/foundry/building-pipelines/create-incremental-pipeline-pb) | Identical current state/counts across incremental and full runs; changed lookup replay covered; rows processed and build time recorded. An “incremental” badge alone is insufficient. | B3, B12 |
| **11** | Test · you + Codex | Finish the three-question screen: signals, recall status/applicability, changes since last review. Add all health checks and finish human-reviewed AI evaluation. | [Health checks](https://www.palantir.com/docs/foundry/health-checks/check-types), [Action testing](https://www.palantir.com/docs/foundry/action-types/getting-started) | Officer completes the morning flow in under two minutes; source as-of dates visible; triage survives rebuild; evaluation metrics and failure cases shown. For a 3–4 week drift replay, label it historical replay unless live observation truly exists. | B8, B10, B11 |
| **12** | Test · you; Codex prepares evidence | Assemble architecture note, measured optimization log, known gaps, and one demo rehearsal. | [Brief summary](../../00-brief/brief-summary.md) | Another engineer can follow raw→object→flag→source; four brief deliverables are linked; no unverified performance claims. | B12–B14 |

Steps 6–8 are the first complete working slice. Step 10 is mandatory before describing the incremental requirement as met. Health checks begin with the first source; step 11 completes their coverage.

## 2. Decisions that must remain visible

| Gate | Current record | What to resolve |
|---|---|---|
| Final pilot scope / deadline | D031 v3 proposed; D014/D018 accepted baseline | Confirm the reduced 11-drug scope, evaluation size, and demo date without assuming approval |
| Product identity | D027 proposed | Show real source rows proving the chosen product grain/key; app number is a join aid, not a proven unique product key |
| FAERS processing | D020–D023 proposed | Approve exact identity, included roles, latest-case/delete handling, and any extra duplicate-fold rule separately |
| Label comparison | D024 proposed | Validate route/form and reference labels; incomplete extraction/matching means uncertain, not unlabeled |
| Signal rule | D006 proposed | Confirm formula, population, threshold, and rule version before ranking real candidates |
| AI acceptance | D015 proposed | Confirm target and sampling; report actual results and limitations |
| Changes and freshness | D028/D029 proposed | Confirm “since last review” semantics and quarterly FAERS cadence |

These are domain decision gates. Naming conventions do not settle them. See [Decisions](../../06-decisions/DECISIONS.md).

## 3. What to learn now, and what to park

| Priority | Tutorial / topic | Project use |
|---|---|---|
| Now | Introduction playlist, episodes 2–6 | Setup, organization, ingestion, inspect data, transform |
| Just before building objects/app | Episodes 9–10 | Ontology contracts, links, Actions, Workshop |
| When complex state logic is needed | Episodes 7–8 | Code-authored transformations; do not implement the same pipeline twice just to practice both tools |
| Later | Episode 11: Contour | Optional analysis; Workshop remains the operational app |
| Park pending a specific need | Advanced Foundry, SkyOps masterclass, interview series, full PySpark course | Avoid adding tutorial breadth to the pilot; these playlist contents were not reviewed in this research |
| Official docs now | Incremental modes, output write modes, AIP Evals, health checks | Fill platform details that the three reviewed introductory transcripts do not prove |

The tutorial's example sources and business objects are learning examples. Use the public medication sources and aggregate objects defined for this project.

## 4. Pilot and scale boundary

| Pilot | After the pilot |
|---|---|
| One project, separated folders and documented contracts | Split source/transform projects when ownership and reuse justify it |
| Minimal validated object model and controlled triage Action | Shared interfaces, richer match-review objects, broader workflow |
| Measured incremental case handling + extraction cache | Partition tuning and broader cost optimization with measurements |
| Small human-reviewed evaluation and honest gaps | Larger representative evaluation, terminology/licensing work, sustained monitoring |

Scale ideas belong in [pilot-to-production](../../09-roadmap/pilot-to-production.md), not in the next build step. That older roadmap contains pre-cut quantities; current scope comes from Decisions and the Compass.

**Next concrete action:** you complete step 1; Codex can then prepare the exact schemas and build instructions for the capabilities that were verified.
