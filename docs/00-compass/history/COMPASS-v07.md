> Snapshot of COMPASS.md at **v7** (2026-10-20, last version before versioning started; versions v1–v7 back-filled from its change log). Read-only history.

# 🧭 COMPASS — Where we are, where we're going

_Last updated: 2026-10-20_

## North Star
_Purpose (boss, 2026-10-13): an exploratory showcase of design thinking, system design and usefulness. The reasoning trail is half the deliverable._

A hospital pharmacy safety officer opens one screen each morning and, in under 2 minutes, knows:
**(1) which drugs show unlabeled adverse events, (2) which have active recalls, (3) what changed since yesterday,**
and can click any flag to see the exact source behind it.

## Right now
| | |
|---|---|
| 📍 **Phase** | 1 — Define (Design thinking: *Define*) |
| 🔨 **Step** | Class locked (8 opioids + 5 GLP-1) ✅ · Structure reports for all 5 sources ✅ · Volumes ✅ · Merge examples ✅ · **Your hand-verification** ⚪ |
| 🎯 **Next milestone** | You hand-verify the 5 sources + finish Developer Tier learning → Phase 2: build the first blocks (raw → drug_identity) |
| ⛔ **Blockers** | Developer Tier familiarity (you) · AEMS: openFDA API stuck at 2026-07-30, **but bulk files for 2026 Q1+Q2 exist** (eased) · Drift reading to confirm · Demo date unknown |
| ⚠️ **Top risk** | FAERS → AEMS switch may change ingestion. Showing 3–4 week drift in ~3 weeks (plan: label churn + replay history) |

## Phase map
📊 **Diagram:** [00-compass-phase-map-v1.png](docs/diagrams/png/00-compass-phase-map-v1.png) · [PDF](docs/diagrams/pdf/00-compass-phase-map-v1.pdf) · _source: [00-compass-phase-map-v1.mmd](docs/diagrams/src/00-compass-phase-map-v1.mmd)_

| Phase | Done when | Status |
|---|---|---|
| 0 · Discover | Brief understood, questions asked, users understood | ✅ Done (2026-10-13) |
| 1 · Define | Scope, formulary, signal rule, "label mentions" definition decided; sources profiled | 🟡 In progress |
| 2 · Pilot build | 4+ sources raw→clean→ontology, 1 incremental pipeline, AI extraction, Workshop app with write-back | ⚪ |
| 3 · Harden + Monitor | Gold set labeled, hallucination rate measured, 1 pipeline optimized; **full monitoring live (pipeline + AI + 3–4 wk drift)** | ⚪ |
| 4 · Demo + Note | Demo rehearsed, architecture note done | ⚪ |
| 5 · Scale | Production roadmap written (not built) | ⚪ |

## Proposed 3-week plan (draft — confirm dates with boss)
| Week | Focus | Exit check |
|---|---|---|
| Wk 0 (now) | Define: profile 5 sources by hand; get Developer Tier access | Scope + data understood |
| Wk 1 | Ingest FAERS, labels, recalls, RxNorm → clean → ontology. Drug identity resolved. | Ontology browsable |
| Wk 2 | LLM label extraction + signal logic + Workshop app + triage write-back | Safety officer flow works end-to-end |
| Wk 3 | Gold set + hallucination check, optimization log, **monitoring (must)**, note, demo rehearsal | Demo-ready |

## Key decisions so far
See [docs/06-decisions/DECISIONS.md](docs/06-decisions/DECISIONS.md). Count: 25 (D020–D025 proposed). Latest: D016 focus rule · D017 diagrams as PNG/PDF · D018 formulary = 13 RxCUIs · D019 DailyMed = label truth · D014 hybrid class (accepted) · D015 AI F1 ≥ 0.85 target (proposed) · D007 opioids · D008 monitoring must · D009 3–4 wk drift · D010 Developer Tier · D011 showcase purpose · D012 profile sources first.

## Active approach
[A002 — Source profiling](docs/05-approaches/A002-source-profiling.md) (Claude done; your hand-check pending) · [A003 — Class: 8 opioids + 5 GLP-1](docs/05-approaches/A003-class-choice-hybrid.md) (kept) · **[Data walkthrough (real bulk FAERS, every stage)](docs/04-architecture/data-walkthrough-v1.html)** — [A004](docs/05-approaches/A004-faers-to-ontology-mapping.md) · [Merge walkthrough](docs/04-architecture/merge-walkthrough-v1.md) · Diagrams: [diagram-book.pdf](docs/diagrams/diagram-book.pdf)

## Change log of the compass
| Date | What moved |
|---|---|
| 2026-10-13 | Project created. Phase 0 started. Boss meeting prep ready. |
| 2026-10-13 | Added class-vs-impact options + "own Developer Tier?" question (M3a). Unblock path: free Foundry Developer Tier for prototyping. |
| 2026-10-13 | Boss meeting done → Phase 1. Class = opioids. Monitoring = must. Developer Tier. Next: source profiling. |
| 2026-10-19 | Source access guide + sampler done. Research R1–R3 done → hybrid class proposed. FAERS→AEMS switch found. |
| 2026-10-20 | Real bulk FAERS 2026 Q1+Q2 run through every stage; 8 data-forced decisions proposed (D020–D025, DQ34–DQ41). Next: label (Part B) + recalls walk, then build. |
| 2026-10-20 | FAERS → ontology + Part B explained with real semaglutide example (A004, DQ33). |
| 2026-10-20 | Hybrid class accepted. All 5 sources profiled + volumes + 2 worked merges. Diagrams now PNG/PDF (D017). |
