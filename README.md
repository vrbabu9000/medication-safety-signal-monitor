# Medication Safety Signal Monitor

A pilot application built on Palantir Foundry and AIP. It helps a hospital pharmacy safety officer answer three questions each morning:

1. Which drugs have adverse events reported that the drug label does not mention?
2. Which drugs have an active recall?
3. What has changed since the last review?

Every flag links back to its source record. The project uses public data only (FDA and NLM). It contains no patient-level data and no protected health information.

## Contents

- [Status](#status)
- [Scope](#scope)
- [Architecture](#architecture)
- [Data sources](#data-sources)
- [Pipelines](#pipelines)
- [Ontology](#ontology)
- [AI label extraction](#ai-label-extraction)
- [Application](#application)
- [Monitoring](#monitoring)
- [Results](#results)
- [Running locally](#running-locally)
- [Limitations](#limitations)
- [Documentation](#documentation)
- [Repository structure](#repository-structure)

## Status

As of 2026-11-06:

| Area | Status |
|---|---|
| Pipelines (raw, clean, curated, ontology) | Complete for 13 drugs |
| Incremental pipeline | Complete. Output matches the full rebuild. Not yet faster at two quarters of data |
| AI label extraction | Complete for 5 labels |
| Workshop application | Complete (4 pages, version 0.10.0) |
| Monitoring | First version complete |
| Architecture note, optimization log, reports | Complete |
| Demo rehearsal | Not started |
| Pharmacist review of findings | Not started |

Build progress follows a 12-step plan: [project-build-order-v1.md](docs/04-architecture/foundry-conventions/project-build-order-v1.md). Steps 1 to 11 are complete. Step 12 is partly complete; the rehearsal is still outstanding.

## Scope

13 drug ingredients, identified by RxNorm ingredient ID (RxCUI):

| Class | Ingredients (RxCUI) |
|---|---|
| Opioids | fentanyl 4337, morphine 7052, hydromorphone 3423, oxycodone 7804, hydrocodone 5489, methadone 6813, buprenorphine 1819, tramadol 10689 |
| GLP-1 agonists | semaglutide 1991302, tirzepatide 2601723, liraglutide 475968, dulaglutide 1551291, exenatide 60548 |

FAERS data covers 2026 Q1 and Q2.

## Architecture

Data moves through four layers in Foundry: raw, clean, curated, and ontology. Every drug name, product, and package code is resolved once to an RxNorm ingredient ID in a single identity dataset. All downstream datasets join on that ID.

- One-page architecture note: [PDF](docs/11-handin/architecture-note/architecture-note.pdf), [text](docs/11-handin/architecture-note/architecture-note.md)
- Dataset contracts (grain and keys): [dataset-contracts-v1.md](docs/04-architecture/dataset-contracts-v1.md)
- Foundry conventions: [foundry-conventions/README.md](docs/04-architecture/foundry-conventions/README.md)
- Diagrams: [diagram-book.pdf](docs/diagrams/diagram-book.pdf)

## Data sources

| Source | Content | Access in Foundry |
|---|---|---|
| FAERS quarterly files (FDA) | Adverse event reports | REST API source `src_faers_files` |
| DailyMed (NLM) | Drug label text (SPL XML) | REST API source `src_dailymed_api` |
| openFDA | Recalls (enforcement), Drugs@FDA, NDC directory | REST API source `src_openfda_api` |
| RxNav (NLM) | RxNorm drug identifiers | REST API source `src_rxnav_api` |

Data exports are disabled on all sources. Sources are imported only into code repositories.

## Pipelines

Python transforms in two Foundry code repositories: `pipelines_raw_ingest` and `pipelines_clean`. Mirrors of the code are kept in this repository under [foundry/](foundry/README.md).

| Layer | Code | Description |
|---|---|---|
| Raw | [foundry/pipelines/raw](foundry/pipelines/raw/README.md) | One transform per source pull. Row counts are checked against source totals |
| Clean | [foundry/pipelines/clean](foundry/pipelines/clean/README.md) | Drug identity, FAERS case versioning and deletes, label sections, recall normalization |
| Ontology | [foundry/pipelines/ontology](foundry/pipelines/ontology/README.md) | Datasets that back ontology objects: signals, change events, label synonym table |
| AI | [foundry/pipelines/ai](foundry/pipelines/ai/README.md) | Label reaction extraction with an LLM |
| Monitoring | [foundry/pipelines/monitoring](foundry/pipelines/monitoring/README.md) | Pipeline and AI health checks |

Main design choices:

- **FAERS deduplication.** The latest case version is kept, FDA delete files are applied, and reports that list 30 or more drugs are excluded from the main signal count. See D022 and D023 v2 in [DECISIONS.md](docs/06-decisions/DECISIONS.md).
- **Incremental FAERS.** [clean_faers_incremental.py](foundry/pipelines/clean/clean_faers_incremental.py) processes one quarter per build. Its output is identical to the full rebuild. At two quarters it took 88 s against 32 s for the full rebuild, so signals still use the full rebuild. See [A015](docs/05-approaches/A015-incremental-faers.md).
- **Signal statistics.** Each drug and reaction pair is counted once per report. A signal is flagged when it has at least 3 reports, a proportional reporting ratio (PRR) of 2 or more, and a Yates chi-square of 4 or more (Evans criteria). See [A012](docs/05-approaches/A012-signal-statistics-and-workshop.md).

## Ontology

10 object types, 10 link types, and 1 action. Drug, Product, Label, Labeled Reaction, Recall, AE Stat, Signal, Change Event, Source Status, Triage Decision. The triage action writes a Triage Decision object back to Foundry.

Details: [foundry/ontology/README.md](foundry/ontology/README.md)

## AI label extraction

An LLM (Claude Sonnet 5.5, run through AIP) reads label sections and lists the adverse reactions they mention. Each extracted reaction must include a quote that appears word for word in the label text. Reactions without a matching quote are rejected. Results are cached, so a rebuild makes no new model calls.

- Coverage: 5 labels, 21 sections, 745 reactions, all 745 grounded in the label text
- Evaluation: [eval/ai-eval-v1.md](eval/ai-eval-v1.md)
- Report: [R08 AI reliability](docs/11-handin/reports/pdf/R08-ai-reliability.pdf)

## Application

Workshop module **MSSM Safety Officer** (version 0.10.0), 4 pages:

1. Morning brief: summary counts for the three questions
2. Not in label: ranked signals, with the label sections searched and the AI quotes
3. Recalls: active recalls by drug, with a link to the FDA record
4. What changed: new, changed, and removed signals, recalls, and label versions

Each signal shows its FAERS counts, the label sections searched, and any matching quote. A triage button records the officer's decision.

- Walkthrough: [demo-navigation-guide.md](docs/11-handin/demo/demo-navigation-guide.md)
- Screenshots: [docs/11-handin/screens](docs/11-handin/screens/README.md)

## Monitoring

Each build computes 21 checks (row counts, freshness, AI grounded rate, cache hits) and records a drift replay. Four Foundry Data Health checks run on key datasets. See [A017](docs/05-approaches/A017-monitoring-and-health-checks.md).

## Results

All figures come from [numbers.json](docs/11-handin/numbers.json), captured with Foundry SQL.

| Measure | Value |
|---|---|
| FAERS current cases | 792,346 |
| Signals | 1,952 |
| Signals ranked for review | 1,073 |
| Signals not found in the label | 1,844 |
| Signals possibly in the label | 108 |
| Recalls (active) | 900 (126) |
| DailyMed labels | 1,321 |
| Change events | 2,898 |

Optimization results (before and after) are in [optimization-log.md](docs/08-optimization-log/optimization-log.md). Examples: caching AI results reduced model calls on rebuild from 9 to 0. Reusing DailyMed XML reduced build time from 203 s to 83 s. Column pruning gave no measurable gain.

## Running locally

The transforms can be run outside Foundry with a small stand-in for the Foundry transforms library. Raw transforms call the public APIs directly.

```bash
pip install requests polars
```

```bash
python foundry/tools/local_run/run_local.py foundry/pipelines/raw/raw_rxnorm.py
```

Notes:

- This is not a Foundry emulator. Spark-specific code must be tested in Foundry.
- `raw_faers_quarters.py` downloads about 127 MB and writes about 690 MB.
- DailyMed may return HTTP 429 (rate limit) on fast pulls. Re-run or reduce the request rate.

Full instructions: [foundry/tools/local_run/README.md](foundry/tools/local_run/README.md)

## Limitations

- **No pharmacist review.** The 35-item AI answer key and the label synonym table have not been reviewed by a pharmacist. AI accuracy figures are self-assessed.
- **The ranked list is a review queue, not confirmed findings.** Some ranked signals are indication terms or the result of stimulated reporting (data issues DQ06 and DQ04).
- **Long label sections are not scored.** This includes all semaglutide sections.
- **Synonym table version.** The code in this repository uses synonym table version syn_v3 (proposed). Foundry and all reported figures use syn_v2.
- **FAERS case reports** can be reached by query, but not yet directly from the application.

Items deliberately left out of scope: [R05 Decisions and what was not done](docs/11-handin/reports/pdf/R05-decisions-and-not-done.pdf).

## Documentation

Reports (PDF):

| Report | Topic |
|---|---|
| [R00](docs/11-handin/reports/pdf/R00-start-here.pdf) | Overview |
| [R01](docs/11-handin/reports/pdf/R01-foundry-from-scratch.pdf) | Foundry setup |
| [R02](docs/11-handin/reports/pdf/R02-pipelines-raw-to-ontology.pdf) | Pipelines, raw to ontology |
| [R03](docs/11-handin/reports/pdf/R03-ontology.pdf) | Ontology |
| [R04](docs/11-handin/reports/pdf/R04-application-workshop.pdf) | Workshop application |
| [R05](docs/11-handin/reports/pdf/R05-decisions-and-not-done.pdf) | Decisions and out-of-scope items |
| [R06](docs/11-handin/reports/pdf/R06-optimization-log.pdf) | Optimization log |
| [R07](docs/11-handin/reports/pdf/R07-data-judgment.pdf) | Data quality decisions |
| [R08](docs/11-handin/reports/pdf/R08-ai-reliability.pdf) | AI reliability |
| [R09](docs/11-handin/reports/pdf/R09-demo-navigation-guide.pdf) | Application walkthrough |

Other references:

- Decision log: [DECISIONS.md](docs/06-decisions/DECISIONS.md)
- Approaches tried, including dropped ones: [docs/05-approaches/INDEX.md](docs/05-approaches/INDEX.md)
- Data issues register: [data-issues-register.md](docs/07-data-quality/data-issues-register.md)
- Pilot to production: [pilot-to-production.md](docs/09-roadmap/pilot-to-production.md)
- Original brief: [brief-summary.md](docs/00-brief/brief-summary.md), [PDF](docs/00-brief/Soragence-Technical-Build-Brief.pdf)

## Repository structure

| Path | Content |
|---|---|
| `foundry/` | Mirrors of Foundry code, resource map, local test runner |
| `docs/00-brief/` | Project brief |
| `docs/01-discovery/` | Requirements and background research |
| `docs/02-design-thinking/` | User research and problem definition |
| `docs/03-meetings/` | Meeting notes |
| `docs/04-architecture/` | Architecture, dataset contracts, Foundry conventions |
| `docs/05-approaches/` | One file per approach tried |
| `docs/06-decisions/` | Decision log and learnings |
| `docs/07-data-quality/` | Data issues register and source profiles |
| `docs/08-optimization-log/` | Performance measurements |
| `docs/09-roadmap/` | Production roadmap |
| `docs/10-delivery/` | Backlog and delivery notes |
| `docs/11-handin/` | Reports, architecture note, deck, demo guide |
| `docs/12-features/` | Exploratory features |
| `docs/diagrams/` | Diagrams (PNG, PDF, Mermaid and draw.io sources) |
| `eval/` | AI evaluation |
| `prototypes/` | Local experiments |
| `tools/` | Diagram rendering and report build scripts |
| `proposals/` | Draft proposals. Only those referenced in the decision log were adopted |

Project working files: [COMPASS.md](COMPASS.md) (current status), [ACTIVITY-LOG.md](ACTIVITY-LOG.md) (session log), [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md) (instructions for AI coding assistants).

Diagrams are rendered with `bash tools/render_diagrams.sh`. The `.drawio` files can be opened in draw.io and exported to Visio (VSDX).
