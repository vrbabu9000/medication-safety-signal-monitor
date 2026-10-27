# 🧭 COMPASS — Where we are, where we're going

**Compass v10** · _Last updated: 2026-10-27_ · History: [docs/00-compass/history](docs/00-compass/history/) · Tracker: [BACKLOG](docs/10-delivery/BACKLOG.md) (run the ⏱️ Delivery Lead to refresh)

## North Star
_Purpose (boss, 2026-10-13): an exploratory showcase of design thinking, system design and usefulness. The reasoning trail is half the deliverable._

A hospital pharmacy safety officer opens one screen each morning and, in under 2 minutes, knows:
**(1) which drugs show unlabeled adverse events, (2) which have active recalls, (3) what changed since yesterday,**
and can click any flag to see the exact source behind it.

## Right now
| | |
|---|---|
| 📍 **Phase** | 1 → 2 · Define done in practice; Pilot build starts **Thu Oct 29** |
| 🔨 **Step** | Claude builds the ready-to-run kit (Oct 27–28) · you approve decisions + 1 h Foundry smoke test (Oct 28, optional) |
| 🎯 **Next milestone** | **Demo Wed Nov 4** (asked of boss; Nov 3 = Election Day) · feature freeze Mon Nov 2, 8 pm |
| ⛔ **Blockers** | Boss OK on Nov 4 · Foundry Developer Tier untested hands-on · AIP on Developer Tier unverified |
| ⏱️ **Time** | 7 days lost (Oct 21–27, no work). Your time ~54 h (Oct 29–Nov 3) vs ~41 h left after cuts = **~76% Green** → [Game plan](docs/10-delivery/game-plan-v1-oct27-to-nov4.md) |
| ⚠️ **Top risk** | Foundry speed (first build). Second: Part B needs AIP. |

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

## Schedule to the demo (D031 v3) — detail in [game plan v1](docs/10-delivery/game-plan-v1-oct27-to-nov4.md)
| Dates | Focus | Exit check |
|---|---|---|
| Tue Oct 27–Wed Oct 28 | Claude: kit (transforms, click guides, approve sheet, diagrams) · you: text boss, approve, smoke test | Foundry + AIP proven to work |
| Thu Oct 29 | FAERS raw + drug identity (B1, B2) | Identity built |
| Fri Oct 30 | FAERS clean incremental + PRR, labels, recalls (B3–B5) | 4 sources clean |
| Sat Oct 31 | Ontology + Part B in AIP (B6, B7) | Ontology browsable |
| Sun Nov 1 | Gold set F1, signal logic, ChangeEvent, Workshop start (B8–B10) | F1 measured |
| Mon Nov 2 | Workshop + write-back, monitoring, optimization log (B10–B12) | Feature freeze 8 pm |
| Tue Nov 3 | Note + 1 rehearsal (B13, B14) · Election Day | Demo-ready |
| Wed Nov 4 | **Demo** | — |

**Cut list v3: all 6 cuts applied now** (Trials, OnSIDES, gold set 6, 1 rehearsal, no daily FAERS/SrLC backtest, 11 drugs) **+ decision review 5 h → 1 h + gold-set draft check folded into B8.** **Never cut:** identity · Part B accuracy · recalls · write-back · monitoring.

## Key decisions so far
See [docs/06-decisions/DECISIONS.md](docs/06-decisions/DECISIONS.md). Count: 31 (+D031 v3) · Changes: see "Decision changes" at the top of DECISIONS (5 changed on 2026-10-20). Latest: D026 add Drugs@FDA/NDC/SrLC · D027 two-level identity · D028 "since last review" · D029 FAERS quarterly · D030 tracking · D031 freeze + cuts · D016 focus rule · D017 diagrams as PNG/PDF · D018 formulary = 13 RxCUIs · D019 DailyMed = label truth · D014 hybrid class (accepted) · D015 AI F1 ≥ 0.85 target (proposed) · D007 opioids · D008 monitoring must · D009 3–4 wk drift · D010 Developer Tier · D011 showcase purpose · D012 profile sources first.

## Active approach
[A005 — Source selection + merge](docs/05-approaches/A005-source-selection-and-merge.md) (trying) · [A002 — Source profiling](docs/05-approaches/A002-source-profiling.md) (Claude done; your hand-check pending) · [A003 — Class: 8 opioids + 5 GLP-1](docs/05-approaches/A003-class-choice-hybrid.md) (kept) · **[Data walkthrough (real bulk FAERS, every stage)](docs/04-architecture/data-walkthrough-v1.html)** — [A004](docs/05-approaches/A004-faers-to-ontology-mapping.md) · [Merge walkthrough](docs/04-architecture/merge-walkthrough-v1.md) · Diagrams: [diagram-book.pdf](docs/diagrams/diagram-book.pdf)

## Change log of the compass
| Ver | Date | What moved | Decisions changed |
|---|---|---|---|
| v10 | 2026-10-27 | No work Oct 21–27. Demo moved to Wed Nov 4 (asked). All cuts applied; build Oct 29–Nov 2; Claude pre-builds the kit Oct 27–28. Load 76%. | D031 v2 → v3 |
| v9 | 2026-10-20 | Atlas E1–E4 done (9 pages, gold-set draft 264 rows). Key: Product reach opioids ~40% → signals stay at Drug level; "active recall" needs lot expiry; OnSIDES weak benchmark; no daily FAERS API. Proposals await your approval. | none yet (all proposed) |
| v8 | 2026-10-20 | Versioning + ⏱️ Delivery Lead + BACKLOG started. Demo ~Nov 3, freezes Oct 23/24, cut list. Sources: +Drugs@FDA, NDC Directory, SrLC; OnSIDES = benchmark. "Since yesterday" = since last review. 4 atlas sessions proposed. | D003→D027, D004 v2, D021, D024, D025; new D026–D031 |
| v7 | 2026-10-20 | Real bulk FAERS 2026 Q1+Q2 run through every stage; 8 data-forced decisions proposed (D020–D025, DQ34–DQ41). Next: label (Part B) + recalls walk, then build. | — |
| v6 | 2026-10-20 | FAERS → ontology + Part B explained with real semaglutide example (A004, DQ33). | — |
| v5 | 2026-10-20 | Hybrid class accepted. All 5 sources profiled + volumes + 2 worked merges. Diagrams now PNG/PDF (D017). | — |
| v4 | 2026-10-19 | Source access guide + sampler done. Research R1–R3 done → hybrid class proposed. FAERS→AEMS switch found. | — |
| v3 | 2026-10-13 | Boss meeting done → Phase 1. Class = opioids. Monitoring = must. Developer Tier. Next: source profiling. | — |
| v2 | 2026-10-13 | Added class-vs-impact options + "own Developer Tier?" question (M3a). Unblock path: free Foundry Developer Tier for prototyping. | — |
| v1 | 2026-10-13 | Project created. Phase 0 started. Boss meeting prep ready. | — |
