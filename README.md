# Medication Safety Signal Monitor

A product built in **Palantir Foundry + AIP** that tells a hospital pharmacy safety officer
which drugs show adverse events **not on the label**, which have **active recalls**, and **what changed since her last review**, with every flag traceable to its source.

Public data only (FDA, NLM). No patient-level data, no PHI.

> **New session (local or cloud)? Read in this order:**
> 1. [ACTIVITY-LOG.md](ACTIVITY-LOG.md) → "Pick up here" box (last session, next 3 actions)
> 2. [COMPASS.md](COMPASS.md) → phase, step, blockers, decisions
> 3. [docs/10-delivery/cloud-session-guide.md](docs/10-delivery/cloud-session-guide.md) → how to work from a cloud session, and the prompt for the next step
> 4. [CLAUDE.md](CLAUDE.md) → how Claude must respond and the git ground rule (Codex: [AGENTS.md](AGENTS.md))

## Status (2026-11-04 · Compass v22)

| | |
|---|---|
| **Phase** | 2 · Pilot build (no fixed demo date, D031 v4) |
| **Done** | Build-order steps 1–4: Foundry access proven (AIP, outbound internet), folder layout, [dataset contracts](docs/04-architecture/dataset-contracts-v1.md) accepted (D039), **raw layer for the oxycodone slice (10 datasets = source totals)**, **shared drug identity (5 clean datasets, 0 duplicate keys, OxyContin chain resolves)**, **clean baseline (FAERS 792k current cases, oxycodone 3,408 after duplicate fold; 1,160 label sections; 25 recalls matched to packages)**, **first Ontology path (Drug, Product, Label, Recall, Triage Decision; 5 link types) with a working triage Action**, **AI label extraction pilot (Claude Sonnet 5.5, prompt p2: 448 reactions, every quote grounded, strict recall 1.00 on short gold sections, cached)** |
| **Next** | Step 8: FAERS statistics + one explainable oxycodone signal in Workshop with the triage Action |
| **Open** | openFDA key stored in Foundry but not yet used in code · pharmacist reviewer not named |

## The requirement (from the brief)

The user is a hospital pharmacy safety officer. Each morning she asks:
1. Which drugs have adverse events being reported that **the label does not mention**?
2. Which drugs have an **active recall**?
3. **What changed** since I last looked?

…and she trusts nothing she can't trace to its source.

| Part | What | Status |
|---|---|---|
| **A. Pipelines** | 4+ public sources (≥1 unstructured) → raw → clean → Ontology (Drug, Label, Adverse Event, Recall, Signal); ≥1 incremental pipeline | 🟡 raw, clean and first Ontology path done (4 object types + links); Signal / AE stats objects in step 8 |
| **B. AI function** | LLM extracts labeled reactions from DailyMed label text; compare with FAERS; flag frequent-but-unlabeled reactions | 🟡 extraction pilot live (2 labels); FAERS comparison in step 8 |
| **C. App** | Workshop: ranked signals, drug drill-down (label passage beside AI extraction), recall alerts, **triage button that writes back** | 🟡 triage Action write-back proven; Workshop not started |
| **D. Monitoring** | Pipeline health + AI health (gold set, drift) — decided as must-have (D008) | ⚪ |

Deliverables: working Foundry build · one-page architecture note · optimization log (measured before/after) · 20-minute demo. Full detail: [brief summary](docs/00-brief/brief-summary.md) · [requirements deep-dive](docs/01-discovery/requirements-deep-dive.md) · [original brief PDF](docs/00-brief/Soragence-Technical-Build-Brief.pdf).

**Pilot scope:** 13 ingredients (D014, D018), built one drug at a time. Oxycodone first, then widen (D039 G1).
Opioids: fentanyl 4337, morphine 7052, hydromorphone 3423, oxycodone 7804, hydrocodone 5489, methadone 6813, buprenorphine 1819, tramadol 10689. GLP-1: semaglutide 1991302, tirzepatide 2601723, liraglutide 475968, dulaglutide 1551291, exenatide 60548 (RxNorm ingredient RxCUIs).

## The plan: 12-step build order

Source: [project-build-order-v1.md](docs/04-architecture/foundry-conventions/project-build-order-v1.md). Each step has a proof gate. Don't skip a failed gate.

| # | Step | Status |
|---|---|---|
| 1 | Confirm scope; check Foundry, AIP, Action access | ✅ (Action save proven in 6) |
| 2 | Folder layout; dataset grain/key contracts | ✅ [contracts v1](docs/04-architecture/dataset-contracts-v1.md) |
| 3 | Land raw samples for every source | ✅ oxycodone slice |
| 4 | Shared drug identity + product/label mapping | ✅ |
| 5 | Clean baseline: FAERS case versions/deletes, label sections, recall normalisation | ✅ |
| 6 | First Ontology path: Drug, Product, Label, Recall (+ test Action save) | ✅ [A010](docs/05-approaches/A010-first-ontology-path.md) |
| 7 | AI label extraction on a few sections; gold set | ✅ pilot [A011](docs/05-approaches/A011-ai-label-extraction-pilot.md) |
| 8 | Statistics + one explainable signal in Workshop with a triage Action | ⏭️ **next** |
| 9 | Widen to the full formulary | ⚪ |
| 10 | Prove an incremental pipeline (vs full rebuild) | ⚪ |
| 11 | Finish the three-question screen + monitoring | ⚪ |
| 12 | Architecture note, optimization log, rehearsal | ⚪ |

## What exists in Foundry today

All under project `/kestrel-01f4ab/Medication Safety Signal Monitor`. Code mirrors live in [foundry/](foundry/README.md). Foundry is the runtime; the GitHub copy is the reviewed record.

| Kind | Name (path) | Notes |
|---|---|---|
| Sources (`Data/raw`) | `src_openfda_api`, `src_dailymed_api`, `src_rxnav_api`, `src_faers_files` | REST API sources; egress self-approved; exports **off**; code-repo import only (D038) |
| Code repositories | `Pipelines/pipelines_raw_ingest`, `Pipelines/pipelines_clean` | Python transforms; mirrors: [raw](foundry/pipelines/raw/README.md), [clean](foundry/pipelines/clean/README.md) |
| Datasets | 10 in `Data/raw`, 12 in `Data/clean`, 11 in `Data/curated` |
| Ontology | 6 `MSSM` object types, 6 link types, 1 Action; Claude Sonnet 5.5 imported for AI extraction | Map: [foundry/ontology](foundry/ontology/README.md) | Counts + RIDs in [foundry/README.md](foundry/README.md#raw-datasets-built) |
| AIP | `AIP/Logic/scratch_aip_access_test` | Access test only |

## Where things live

| Folder | What's in it | Open this first |
|---|---|---|
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
| `docs/10-delivery/` | Backlog, access results, **cloud session guide** | [cloud-session-guide.md](docs/10-delivery/cloud-session-guide.md) · [BACKLOG.md](docs/10-delivery/BACKLOG.md) |
| `docs/diagrams/` | All diagrams as PNG + PDF (+ one-PDF book), Mermaid sources, draw.io | [diagram-book.pdf](docs/diagrams/diagram-book.pdf) |
| `foundry/` | Mirrors of Foundry code + resource map + local test harness | [foundry/README.md](foundry/README.md) |
| `eval/`, `proposals/2026-11-02-gold-set-v2/` | Reference set v2 (30 cross-source traces) for evaluation | [A008](docs/05-approaches/A008-gold-set-v2-cross-source-traces.md) |
| `prototypes/` | Local experiments (bulk data git-ignored under `prototypes/data/`) | — |
| `tools/` | `render_diagrams.sh`; `handin/` = hand-in PDF + diagram style kit | [tools/handin/README.md](tools/handin/README.md) |
| `.claude/agents/` | Persona definitions (Architect, Data Eng, AI Eng, PV SME, Safety Officer, Design Lead, Compliance, Evaluator, Delivery Lead) | — |

Other `proposals/` folders are drafts that were **not adopted** (see COMPASS). Don't build from them.

## Diagrams → Visio
Every diagram is a PNG + PDF in `docs/diagrams/` ([diagram-book.pdf](docs/diagrams/diagram-book.pdf)). Re-render with `bash tools/render_diagrams.sh`. Editable `.drawio` files: open in [draw.io](https://www.drawio.com) → *File → Export as → VSDX*.
