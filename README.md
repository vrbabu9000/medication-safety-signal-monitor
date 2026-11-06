# Medication Safety Signal Monitor

A product built in **Palantir Foundry + AIP** that tells a hospital pharmacy safety officer
which drugs show adverse events **not on the label**, which have **active recalls**, and **what changed since her last review**, with every flag traceable to its source.

Public data only (FDA, NLM). No patient-level data, no PHI.

## 👋 Reviewing this project? Start here

The pilot is built end to end in Foundry. It is **not yet rehearsed as a demo**, and **no pharmacist has reviewed the findings yet** (see [Known gaps](#known-gaps-read-before-judging-the-results)).

**30-minute path (PDFs, no setup needed):**

| # | Read | What you get |
|---|---|---|
| 1 | [R00 Start here](docs/11-handin/reports/pdf/R00-start-here.pdf) | The problem, the user, what was built, how to read the rest |
| 2 | [Architecture note (1 page)](docs/11-handin/architecture-note/architecture-note.pdf) | Data flow from 4 public sources → ontology → app, on one page |
| 3 | [R02 Pipelines: raw → ontology](docs/11-handin/reports/pdf/R02-pipelines-raw-to-ontology.pdf) | **Data engineering:** medallion layers, drug identity, FAERS dedup, incremental build |
| 4 | [R06 Optimization log](docs/11-handin/reports/pdf/R06-optimization-log.pdf) | **Data engineering:** before/after timings, including what did *not* help |
| 5 | [R07 Data judgment](docs/11-handin/reports/pdf/R07-data-judgment.pdf) | **Data engineering:** data issues found, and the call made on each |
| 6 | [R09 Demo navigation guide](docs/11-handin/reports/pdf/R09-demo-navigation-guide.pdf) | Click-by-click tour of the Foundry app |

**Deeper:** [R01 Foundry from scratch](docs/11-handin/reports/pdf/R01-foundry-from-scratch.pdf) · [R03 Ontology](docs/11-handin/reports/pdf/R03-ontology.pdf) · [R04 Workshop app](docs/11-handin/reports/pdf/R04-application-workshop.pdf) · [R05 Decisions and what was not done](docs/11-handin/reports/pdf/R05-decisions-and-not-done.pdf) · [R08 AI reliability](docs/11-handin/reports/pdf/R08-ai-reliability.pdf) · [demo deck (PDF)](docs/11-handin/deck/MSSM-demo-deck.pdf) · [all diagrams in one PDF](docs/diagrams/diagram-book.pdf)

**Every number** in the reports, deck and note comes from one file: [numbers.json](docs/11-handin/numbers.json) (captured with Foundry SQL).

## Headline numbers (from [numbers.json](docs/11-handin/numbers.json))

| Area | Number |
|---|---|
| Scope | 13 drugs (8 opioids + 5 GLP-1), FAERS 2026 Q1–Q2 |
| FAERS (the FDA's adverse event report database) | 792,346 current cases after version/delete handling |
| Signals | 1,952 drug–reaction signals · 1,073 ranked for review · 1,844 not found in the label · 108 possibly in the label |
| Recalls | 900 recalls · 126 active |
| Labels | 1,321 DailyMed labels |
| AI label reading | 5 labels, 21 sections, 745 reactions extracted, **745/745 quotes found word-for-word in the label** |
| What changed | 2,898 change events in the feed |
| Ontology | 10 object types, 10 link types, 1 write-back Action (triage) |
| App | Workshop module, 4 pages, v0.10.0 |
| Monitoring | 21 computed checks per build + 4 Foundry Data Health checks |

## Data engineering at a glance

| Topic | What we did | Read |
|---|---|---|
| Layers | raw → clean → curated → ontology, one Foundry folder per layer | [R02](docs/11-handin/reports/pdf/R02-pipelines-raw-to-ontology.pdf) · [conventions](docs/04-architecture/foundry-conventions/README.md) |
| Contracts | Grain and key written down per dataset before building | [dataset-contracts-v1.md](docs/04-architecture/dataset-contracts-v1.md) |
| Drug identity | Every drug name, product and package resolved **once** to an RxNorm ingredient ID (RxCUI) | [clean_drug_identity.py](foundry/pipelines/clean/clean_drug_identity.py) |
| FAERS dedup | Latest case version wins, FDA delete files applied, mass-polypharmacy re-filings folded | [clean_faers.py](foundry/pipelines/clean/clean_faers.py) · D022, D023 v2 in [DECISIONS](docs/06-decisions/DECISIONS.md) |
| Incremental | Incremental FAERS proven **identical** to the full rebuild, but slower at 2 quarters (88 s vs 32 s), so signals still use the full rebuild | [clean_faers_incremental.py](foundry/pipelines/clean/clean_faers_incremental.py) · [A015](docs/05-approaches/A015-incremental-faers.md) |
| Optimization | Measured before/after: AI cache (9 → 0 model calls on rebuild), DailyMed XML reuse (203 s → 83 s); column pruning did not help | [optimization-log.md](docs/08-optimization-log/optimization-log.md) |
| Data quality | Issues register (DQ01–DQ43) with the decision taken on each | [data-issues-register.md](docs/07-data-quality/data-issues-register.md) |
| Monitoring | Pipeline counts, AI grounded rate, cache hits, freshness, drift replay | [foundry/pipelines/monitoring](foundry/pipelines/monitoring/README.md) · [A017](docs/05-approaches/A017-monitoring-and-health-checks.md) |

## Run it yourself (no Foundry account needed)

Foundry is where the pipelines run. Every transform is mirrored in [foundry/](foundry/README.md) and can run on a laptop with a small stand-in for Foundry's library. Raw transforms call the real public APIs.

```bash
pip install requests polars
```

```bash
python foundry/tools/local_run/run_local.py foundry/pipelines/raw/raw_rxnorm.py
```

Full guide, flags and limits: [foundry/tools/local_run/README.md](foundry/tools/local_run/README.md). Notes:
- It is not a Foundry emulator. Spark-only code must be tested in Foundry.
- `raw_faers_quarters.py` downloads about 127 MB and writes about 690 MB.
- DailyMed rate-limits fast pulls (HTTP 429). Re-run, or fetch slowly.

## Known gaps (read before judging the results)

| Gap | Why it matters |
|---|---|
| **No pharmacist review yet** | The 35-item AI answer key was written by Claude, and the synonym bands were not checked by a clinician. The AI scores are self-scored. |
| **The ranked list is a review queue, not findings** | Some top rows are indication terms (DQ06) or stimulated reporting (DQ04). |
| Long label sections are unscored | Including all semaglutide sections ([R08](docs/11-handin/reports/pdf/R08-ai-reliability.pdf)). |
| Synonym table v3 is ahead of Foundry | The repo mirror [label_synonyms.py](foundry/pipelines/ontology/label_synonyms.py) holds proposed **syn_v3** (local only: ranked 1,073 → 1,072). Foundry and every hand-in number still use **syn_v2**. |
| Demo not rehearsed | Rehearsal plan: [rehearsal-plan.md](docs/11-handin/demo/rehearsal-plan.md). |

Full list of what was cut and why: [R05](docs/11-handin/reports/pdf/R05-decisions-and-not-done.pdf).

## Status (2026-11-06 · Compass v39)

| | |
|---|---|
| **Phase** | 2 · Pilot build done → 4 · Demo + note (no fixed demo date, D031 v4) |
| **Done** | Build-order steps 1–11. Hand-in set: reports R00–R09, architecture note, optimization log, deck, demo guide, reviews |
| **Next** | Rehearsal against live Foundry, then one commit |
| **Open** | Pharmacist reviewer not named · push syn_v3 now or after the hand-in |

Live status: [COMPASS.md](COMPASS.md) · session log: [ACTIVITY-LOG.md](ACTIVITY-LOG.md).

## The requirement (from the brief)

The user is a hospital pharmacy safety officer. Each morning she asks:
1. Which drugs have adverse events being reported that **the label does not mention**?
2. Which drugs have an **active recall**?
3. **What changed** since I last looked?

…and she trusts nothing she can't trace to its source.

| Part | What | Status |
|---|---|---|
| **A. Pipelines** | 4+ public sources (≥1 unstructured) → raw → clean → Ontology (Drug, Label, Adverse Event, Recall, Signal); ≥1 incremental pipeline | ✅ 4 sources, 10 object types; incremental FAERS proven equal to the full rebuild |
| **B. AI function** | LLM extracts labeled reactions from DailyMed label text; compare with FAERS; flag frequent-but-unlabeled reactions | ✅ Claude Sonnet 5.5 in Foundry, 5 labels, 745/745 grounded, cached; feeds the label check |
| **C. App** | Workshop: ranked signals, drug drill-down (label passage beside AI extraction), recall alerts, **triage button that writes back** | ✅ 4-page "Morning brief" (signals, recalls, what changed, signals with labels) + triage Action |
| **D. Monitoring** | Pipeline health + AI health (gold set, drift), decided as must-have (D008) | ✅ first version: 21 checks per build, 4 Data Health checks, drift replay |

Deliverables: working Foundry build · one-page architecture note · optimization log (measured before/after) · 20-minute demo. Full detail: [brief summary](docs/00-brief/brief-summary.md) · [requirements deep-dive](docs/01-discovery/requirements-deep-dive.md) · [original brief PDF](docs/00-brief/Soragence-Technical-Build-Brief.pdf).

**Pilot scope:** 13 ingredients (D014, D018, D031 v5).
Opioids: fentanyl 4337, morphine 7052, hydromorphone 3423, oxycodone 7804, hydrocodone 5489, methadone 6813, buprenorphine 1819, tramadol 10689. GLP-1: semaglutide 1991302, tirzepatide 2601723, liraglutide 475968, dulaglutide 1551291, exenatide 60548 (RxNorm ingredient RxCUIs).

## The plan: 12-step build order

Source: [project-build-order-v1.md](docs/04-architecture/foundry-conventions/project-build-order-v1.md). Each step has a proof gate.

| # | Step | Status |
|---|---|---|
| 1 | Confirm scope; check Foundry, AIP, Action access | ✅ |
| 2 | Folder layout; dataset grain/key contracts | ✅ [contracts v1](docs/04-architecture/dataset-contracts-v1.md) |
| 3 | Land raw samples for every source | ✅ |
| 4 | Shared drug identity + product/label mapping | ✅ |
| 5 | Clean baseline: FAERS case versions/deletes, label sections, recall normalisation | ✅ |
| 6 | First Ontology path: Drug, Product, Label, Recall (+ test Action save) | ✅ [A010](docs/05-approaches/A010-first-ontology-path.md) |
| 7 | AI label extraction on a few sections; gold set | ✅ [A011](docs/05-approaches/A011-ai-label-extraction-pilot.md), widened in [A019](docs/05-approaches/A019-widen-ai-to-semaglutide.md) |
| 8 | Statistics + one explainable signal in Workshop with a triage Action | ✅ [A012](docs/05-approaches/A012-signal-statistics-and-workshop.md) |
| 9 | Widen to the full formulary | ✅ [A013](docs/05-approaches/A013-widen-to-formulary.md) |
| 10 | Prove an incremental pipeline (vs full rebuild) | ✅ correct, not yet faster: [A015](docs/05-approaches/A015-incremental-faers.md) |
| 11 | Finish the three-question screen + monitoring | ✅ [A016](docs/05-approaches/A016-three-question-screen.md), [A017](docs/05-approaches/A017-monitoring-and-health-checks.md) |
| 12 | Architecture note, optimization log, rehearsal | 🟡 note ✅ log ✅ · rehearsal ⚪ |

## What exists in Foundry today

All under project `/kestrel-01f4ab/Medication Safety Signal Monitor` (Palantir AIP Developer Tier). Code mirrors live in [foundry/](foundry/README.md). Foundry is the runtime; the GitHub copy is the reviewed record.

| Kind | Name (path) | Notes |
|---|---|---|
| Sources (`Data/raw`) | `src_openfda_api`, `src_dailymed_api`, `src_rxnav_api`, `src_faers_files` | REST API sources; egress self-approved; exports **off**; code-repo import only (D038) |
| Code repositories | `Pipelines/pipelines_raw_ingest`, `Pipelines/pipelines_clean` | Python transforms. Mirrors: [raw](foundry/pipelines/raw/README.md), [clean](foundry/pipelines/clean/README.md), [ontology](foundry/pipelines/ontology/README.md), [AI](foundry/pipelines/ai/README.md), [monitoring](foundry/pipelines/monitoring/README.md) |
| Datasets | `Data/raw`, `Data/clean`, `Data/curated`, monitoring | Counts and RIDs: [foundry/README.md](foundry/README.md) |
| Ontology | 10 `MSSM` object types, 10 link types, 1 Action; Claude Sonnet 5.5 imported for AI extraction | Map: [foundry/ontology](foundry/ontology/README.md) |
| Workshop | Module **MSSM Safety Officer** v0.10.0, 4 pages | Tour: [demo-navigation-guide.md](docs/11-handin/demo/demo-navigation-guide.md) · screenshots: [screens/](docs/11-handin/screens/README.md) |

## Where things live

| Folder | What's in it | Open this first |
|---|---|---|
| `docs/11-handin/` | **Hand-in set:** reports R00–R09, architecture note, deck, demo guide, reviews, numbers.json | [R00 Start here](docs/11-handin/reports/pdf/R00-start-here.pdf) |
| `foundry/` | Mirrors of Foundry code + resource map + local test harness | [foundry/README.md](foundry/README.md) |
| `ACTIVITY-LOG.md` | Session-by-session log + "pick up here" box | — |
| `COMPASS.md` | Current phase, next milestone, blockers, version history | — |
| `CLAUDE.md` / `AGENTS.md` | How Claude / Codex respond (rules, personas, diagrams, git rule) | — |
| `docs/00-brief/` | Original brief PDF + plain-language summary | [brief-summary.md](docs/00-brief/brief-summary.md) |
| `docs/00-compass/history/` | Every past COMPASS version | — |
| `docs/01-discovery/` | Requirements deep-dive, research (class choice, industry need, prior art) | [requirements-deep-dive.md](docs/01-discovery/requirements-deep-dive.md) |
| `docs/02-design-thinking/` | Personas, empathy map, problem statement | [design-thinking-canvas.md](docs/02-design-thinking/design-thinking-canvas.md) |
| `docs/03-meetings/` | Meeting prep, questions, notes | — |
| `docs/04-architecture/` | Architecture, **dataset contracts**, Foundry conventions + build order, data walkthroughs | [dataset-contracts-v1.md](docs/04-architecture/dataset-contracts-v1.md) · [foundry-conventions/](docs/04-architecture/foundry-conventions/README.md) |
| `docs/05-approaches/` | One .md per approach tried (kept even if dropped) | [INDEX.md](docs/05-approaches/INDEX.md) |
| `docs/06-decisions/` | Decision log + decision changes + learnings | [DECISIONS.md](docs/06-decisions/DECISIONS.md) |
| `docs/07-data-quality/` | Data issues register, source profiles, data atlas | [data-issues-register.md](docs/07-data-quality/data-issues-register.md) · [source-profiles/](docs/07-data-quality/source-profiles/README.md) |
| `docs/08-optimization-log/` | Before/after measurements (a required deliverable) | [optimization-log.md](docs/08-optimization-log/optimization-log.md) |
| `docs/09-roadmap/` | Pilot → production path + parked ideas | [pilot-to-production.md](docs/09-roadmap/pilot-to-production.md) |
| `docs/10-delivery/` | Backlog, access results, cloud session guide, reviewer access | [BACKLOG.md](docs/10-delivery/BACKLOG.md) · [sharing-with-reviewers.md](docs/10-delivery/sharing-with-reviewers.md) |
| `docs/12-features/` | Exploratory features (F01: AI literature review) | [ai-literature-review](docs/12-features/ai-literature-review/README.md) |
| `docs/diagrams/` | All diagrams as PNG + PDF (+ one-PDF book), Mermaid sources, draw.io | [diagram-book.pdf](docs/diagrams/diagram-book.pdf) |
| `eval/`, `proposals/2026-11-02-gold-set-v2/` | AI evaluation + reference set v2 (30 cross-source traces) | [ai-eval-v1.md](eval/ai-eval-v1.md) · [A008](docs/05-approaches/A008-gold-set-v2-cross-source-traces.md) |
| `prototypes/` | Local experiments (bulk data git-ignored under `prototypes/data/`) | — |
| `tools/` | `render_diagrams.sh`; `handin/` = hand-in PDF + diagram style kit; `lit_review/` | [tools/handin/README.md](tools/handin/README.md) |
| `.claude/agents/` | Persona definitions (Architect, Data Eng, AI Eng, PV SME, Safety Officer, Design Lead, Compliance, Evaluator, Delivery Lead, hand-in agents) | — |

Other `proposals/` folders are drafts that were **not adopted** (see COMPASS). Don't build from them.

> **Working on this repo with Claude or Codex?** Read [ACTIVITY-LOG.md](ACTIVITY-LOG.md) → [COMPASS.md](COMPASS.md) → [cloud-session-guide.md](docs/10-delivery/cloud-session-guide.md) → [CLAUDE.md](CLAUDE.md) ([AGENTS.md](AGENTS.md) for Codex).

## Diagrams → Visio
Every diagram is a PNG + PDF in `docs/diagrams/` ([diagram-book.pdf](docs/diagrams/diagram-book.pdf)). Re-render with `bash tools/render_diagrams.sh`. Editable `.drawio` files: open in [draw.io](https://www.drawio.com) → *File → Export as → VSDX*.
