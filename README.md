# Medication Safety Signal Monitor

A product built in **Palantir Foundry + AIP** that tells a hospital pharmacy safety officer
which drugs show adverse events **not on the label**, which have **active recalls**, and **what changed since yesterday**, with every flag traceable to its source.

> Coming back after a break? → [ACTIVITY-LOG.md](ACTIVITY-LOG.md) ("Pick up here") · [COMPASS.md](COMPASS.md) (where we're going)

## Where things live

| Folder | What's in it | Open this first |
|---|---|---|
| `ACTIVITY-LOG.md` | What happened, session by session + "pick up here" box | — |
| `COMPASS.md` | Current phase, next milestone, blockers | — |
| `CLAUDE.md` | How Claude responds in this project (rules, personas, diagrams) | — |
| `docs/00-brief/` | Original brief PDF + plain-language summary | [brief-summary.md](docs/00-brief/brief-summary.md) |
| `docs/01-discovery/` | Deep-dive on requirements, value, data sources, hidden traps | [requirements-deep-dive.md](docs/01-discovery/requirements-deep-dive.md) |
| `docs/02-design-thinking/` | Personas, empathy map, problem statement, "How might we" | [design-thinking-canvas.md](docs/02-design-thinking/design-thinking-canvas.md) |
| `docs/03-meetings/` | Meeting prep, questions, notes, answers | [2026-10-13-boss-kickoff-questions.md](docs/03-meetings/2026-10-13-boss-kickoff-questions.md) |
| `docs/04-architecture/` | Architecture notes + diagrams (Mermaid + draw.io → Visio) | [architecture-v0.md](docs/04-architecture/architecture-v0.md) |
| `docs/05-approaches/` | One .md per approach tried (kept even if dropped) | [INDEX.md](docs/05-approaches/INDEX.md) |
| `docs/06-decisions/` | Decision log: what we chose and why | [DECISIONS.md](docs/06-decisions/DECISIONS.md) |
| `docs/07-data-quality/` | Known data problems + hand profiling of each source | [data-issues-register.md](docs/07-data-quality/data-issues-register.md) · [source-profiles/](docs/07-data-quality/source-profiles/README.md) |
| `docs/08-optimization-log/` | Before/after measurements (a required deliverable) | [optimization-log.md](docs/08-optimization-log/optimization-log.md) |
| `docs/09-roadmap/` | Pilot → production scale path + parked ideas | [pilot-to-production.md](docs/09-roadmap/pilot-to-production.md) · [ideas-parking-lot.md](docs/09-roadmap/ideas-parking-lot.md) |
| `foundry/` | Code that will live in Foundry: pipelines, ontology, AI function, app, monitoring | [foundry/README.md](foundry/README.md) |
| `eval/gold-set/` | Hand-labeled label extractions for measuring AI accuracy | — |
| `prototypes/` | Local throwaway experiments (e.g. pulling openFDA data before Foundry access) | — |
| `.claude/agents/` | Persona definitions (Architect, Data Eng, AI Eng, PV SME, Safety Officer, Design Lead, Compliance, Evaluator) | — |

## Deliverables (from the brief)
1. Working build in Foundry (pipelines, ontology, AI function, app)
2. One-page architecture note (diagram + 3–4 key decisions + what we chose not to do)
3. Optimization log (before/after, including what didn't help)
4. 20-minute demo + Q&A

## Diagrams → Visio
Editable diagrams are `.drawio` files in `docs/04-architecture/diagrams/`. Open them in [draw.io / diagrams.net](https://www.drawio.com) (free, desktop or web) → *File → Export as → VSDX* to get a Visio file.
