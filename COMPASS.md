# 🧭 COMPASS — Where we are, where we're going

**Compass v39** · _Last updated: 2026-11-06_ · History: [docs/00-compass/history](docs/00-compass/history/) · Tracker: [BACKLOG](docs/10-delivery/BACKLOG.md) (run the ⏱️ Delivery Lead to refresh)

## North Star
_Purpose (boss, 2026-10-13): an exploratory showcase of design thinking, system design and usefulness. The reasoning trail is half the deliverable._

A hospital pharmacy safety officer opens one screen each morning and, in under 2 minutes, knows:
**(1) which drugs show unlabeled adverse events, (2) which have active recalls, (3) what changed since yesterday,**
and can click any flag to see the exact source behind it.

## Right now
| | |
|---|---|
| 📍 **Phase** | 2 · Pilot build (started 2026-11-04, built with Claude over Claude in Chrome) |
| 🔨 **Step** | **Owner batch decision applied (2026-11-06):** 12 decisions accepted (D006, D015 target only, D025–D029, D037, D045–D048); **D041 v2 built** ([A019](docs/05-approaches/A019-widen-ai-to-semaglutide.md)): the AI now reads the 3 semaglutide labels too (5 labels, 21 sections, **745/745 quotes grounded**; 12 model calls, then 0 on rebuild); NAION shows *Labels also read by AI = 3* and the AI found retinopathy but no optic-nerve term; page 1 has a new **"What the AI read in these labels"** table (Workshop v0.10.0). Signals unchanged (1,952 / 1,073). Duplicate Signal→Drug link type **deleted**. Hand-in set being refreshed. Earlier: Phase D review loop done (v37); step 11 + baseline gate (v36) |
| 🎯 **Next milestone** | Rehearsal against live Foundry with the 3 checks (DailyMed "optic" search, active Class I count, a human stopwatch walk-through), then one commit |
| ⛔ **Blockers** | Pharmacist reviewer not named (answer key, long label sections, synonym bands) — kept as a documented gap · Your call: push syn_v3 to Foundry now or after the hand-in (repo mirror is ahead of Foundry) · Outside reviewer: invite via Control Panel → Add new user (5-user plan, default Viewer on the project) — [sharing guide](docs/10-delivery/sharing-with-reviewers.md) |
| ⏱️ **Time** | **No fixed demo date** (D031 v4, 2026-11-04): build at our own pace. Old Nov 4 plan is historical → [prior game plan](docs/10-delivery/game-plan-v1-oct27-to-nov4.md). BACKLOG hours not yet re-estimated |
| ⚠️ **Top risk** | The AI is still self-scored: the 35-item answer key was written by Claude and the long sections (and all semaglutide sections) are unscored. Second: the queue is noisy (indication terms DQ06, e.g. liraglutide rank 1; stimulated reporting DQ04), shown as "review queue, not findings". Earlier risk (AI never met the screen) closed by D041 v2 |

## Phase map
📊 **Diagram:** [00-compass-phase-map-v1.png](docs/diagrams/png/00-compass-phase-map-v1.png) · [PDF](docs/diagrams/pdf/00-compass-phase-map-v1.pdf) · _source: [00-compass-phase-map-v1.mmd](docs/diagrams/src/00-compass-phase-map-v1.mmd)_

| Phase | Done when | Status |
|---|---|---|
| 0 · Discover | Brief understood, questions asked, users understood | ✅ Done (2026-10-13) |
| 1 · Define | Scope, formulary, signal rule, "label mentions" definition decided; sources profiled | 🟡 In progress |
| 2 · Pilot build | 4+ sources raw→clean→ontology, 1 incremental pipeline, AI extraction, Workshop app with write-back | 🟡 Started 2026-11-04 — raw ✅ clean ✅ ontology + write-back ✅ AI extraction ✅ (pilot) statistics ✅ Workshop ✅ (first screen) 13-drug formulary ✅ incremental FAERS ✅ (correct; not yet faster) recalls + what-changed + as-of on screen ✅ monitoring ✅ (first version) |
| 3 · Harden + Monitor | Gold set labeled, hallucination rate measured, 1 pipeline optimized; **full monitoring live (pipeline + AI + 3–4 wk drift)** | ⚪ |
| 4 · Demo + Note | Demo rehearsed, architecture note done | 🟡 Note ✅ · reports R00–R09 ✅ · deck + script ✅ · demo guide ✅ · reviews ✅ · rehearsal ⚪ |
| 5 · Scale | Production roadmap written (not built) | ⚪ |

## Prior schedule to the demo (D031 v3 — historical; superseded by D031 v4 "no fixed date", 2026-11-04) — detail in [game plan v1](docs/10-delivery/game-plan-v1-oct27-to-nov4.md)
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

**Cut list v3 stays the default scope under D031 v4; any cut can be restored later by a new decision.** Original wording: **all 6 cuts applied now** (Trials, OnSIDES, gold set 6, 1 rehearsal, no daily FAERS/SrLC backtest, 11 drugs) **+ decision review 5 h → 1 h + gold-set draft check folded into B8.** **Never cut:** identity · Part B accuracy · recalls · write-back · monitoring.

## Key decisions so far
See [docs/06-decisions/DECISIONS.md](docs/06-decisions/DECISIONS.md). Active decision IDs: D001–D031 + D036–D048 (D032–D035 reserved in the non-adopted proposal) · Changes: see "Decision changes" at the top of DECISIONS (5 changed on 2026-10-20). Latest: D041 v2 AI reads the semaglutide labels (accepted, built) · batch 2026-11-06: D006, D015, D025–D029, D037, D045–D048 accepted · D048 no partitioning (accepted) · D047 DailyMed XML reuse (accepted) · D046 monitoring (accepted) · D045 change feed (accepted) · D044 incremental FAERS (accepted) · D016 v3 wider buckets (accepted) · D043 synonym table (accepted) · D031 v5 13-drug scope (accepted via G1) · D042 step 8 signal + Workshop · D023 v2 ≥30-drug reports out of main count · D016 v2 wider buckets (all accepted 2026-11-04) · D041 AI extraction · D040 Ontology path · D038 openFDA via REST API source + Python external transform (kept) · D031 v4 no fixed demo date · D037 reference set v2 + dataset "label mentions" rule (accepted) · D036 conventions reference + dependency roadmap (documentation only) · D026 add Drugs@FDA/NDC/SrLC · D027 two-level identity · D028 "since last review" · D029 FAERS quarterly · D030 tracking · D031 freeze + cuts · D016 focus rule · D017 diagrams as PNG/PDF · D018 formulary = 13 RxCUIs · D019 DailyMed = label truth · D014 hybrid class (accepted) · D015 AI F1 ≥ 0.85 target (accepted, target only) · D007 opioids · D008 monitoring must · D009 3–4 wk drift · D010 Developer Tier · D011 showcase purpose · D012 profile sources first.

## Active approach
[A016 — Three-question screen](docs/05-approaches/A016-three-question-screen.md) and [A017 — Monitoring](docs/05-approaches/A017-monitoring-and-health-checks.md) (kept). Hand-in plan: [approved plan](docs/11-handin/README.md) (Phase A build → B baseline gate → C agents → D review).

[A015 — Incremental FAERS](docs/05-approaches/A015-incremental-faers.md) (kept; identical to the full rebuild, slower at 2 quarters: re-measure at 4+).

[A014 — Label ↔ FAERS synonym table](docs/05-approaches/A014-label-faers-synonym-table.md) (kept; pharmacist review pending).

[A013 — Widen to the 13-drug formulary](docs/05-approaches/A013-widen-to-formulary.md) (kept; step 9 gate passed).

[A012 — Signal statistics + first Workshop screen](docs/05-approaches/A012-signal-statistics-and-workshop.md) (kept; step 8 gate passed).

[A009 — openFDA ingestion via REST API source + Python external transform](docs/05-approaches/A009-openfda-rest-ingestion.md) (kept; 1-record access test passed 2026-11-04) · [access results](docs/10-delivery/2026-11-04-foundry-access-results.md).

[A008 — Reference set v2: 30 verified cross-source drug traces](docs/05-approaches/A008-gold-set-v2-cross-source-traces.md) (kept; pharmacist review pending) · [case cards](proposals/2026-11-02-gold-set-v2/cards/) · v1 30-case pack superseded.

[A007 — Foundry medallion + ontology conventions](docs/05-approaches/A007-foundry-medallion-conventions.md) (kept as reference; runtime validation pending) · **[Start here](docs/04-architecture/foundry-conventions/README.md)** · [12-step build order](docs/04-architecture/foundry-conventions/project-build-order-v1.md). The six-day draft in `proposals/` remains non-adopted.

[A005 — Source selection + merge](docs/05-approaches/A005-source-selection-and-merge.md) (trying) · [A002 — Source profiling](docs/05-approaches/A002-source-profiling.md) (Claude done; your hand-check pending) · [A003 — Class: 8 opioids + 5 GLP-1](docs/05-approaches/A003-class-choice-hybrid.md) (kept) · **[Data walkthrough (real bulk FAERS, every stage)](docs/04-architecture/data-walkthrough-v1.html)** — [A004](docs/05-approaches/A004-faers-to-ontology-mapping.md) · [Merge walkthrough](docs/04-architecture/merge-walkthrough-v1.md) · Diagrams: [diagram-book.pdf](docs/diagrams/diagram-book.pdf)

## Change log of the compass
| Ver | Date | What moved | Decisions changed |
|---|---|---|---|
| v39 | 2026-11-06 | README rewritten for outside reviewers (start-here path, headline numbers, data engineering summary, local run, known gaps); repo-wide link and number check; reviewer sharing guide (Developer Tier sign-ups paused 23 Oct 2026, so live Foundry access for outsiders is unconfirmed). Also logged here: syn_v3 proposed (Allodynia → "dysesthesia", medium), found by the F01 literature review; local only: ranked 1,073 → 1,072, possibly in label 108 → 109. Hand-in numbers stay frozen at syn_v2. New DQ43 (tied chi² ranks swap between builds). New blocker: push syn_v3 now or after the hand-in. | D043 table data syn_v2 → syn_v3 (proposed) |
| v38 | 2026-11-06 | Your batch decision: 12 decisions accepted, D041 v2 built (AI reads semaglutide labels; page-1 AI quotes table; Workshop v0.10.0), duplicate link deleted, pharmacist stays a gap. Next: rehearsal, commit. | D006, D015, D025–D029, D037, D045–D048 → Accepted; new D041 v2 (accepted, built) |
| v37 | 2026-11-05 | Phase D done: 5 reviews run and fixed across R00–R09, note, deck, demo guide; diagrams 30/32/36/37 v2; NAION framed as a known positive; true proposed list is 12 decisions. Next: rehearsal checks, your batch decision, one commit. | New D048 (proposed) |
| v36 | 2026-11-05 | Baseline gate passed; O3 measured (helped); numbers.json frozen; Phase C agents launched (reports, note, deck, demo guide). Next: Phase D reviews. | New D047 (proposed) |
| v35 | 2026-11-05 | Step 11 mostly built: 4-page screen, change feed, source as-of, monitoring + Data Health checks, DailyMed retry. Next: finish step 11, baseline gate, hand-in agents. | New D045, D046 (proposed) |
| v34 | 2026-11-05 | D044 accepted by you. No change to step or plan. | D044 → Accepted |
| v33 | 2026-11-05 | Step 10 done: incremental FAERS identical to the full rebuild; 88 s vs 32 s at 2 quarters (O2), so signals keep the full rebuild. Next: step 11. | New D044 (proposed) |
| v32 | 2026-11-05 | Synonym table syn_v2 live: ranked 1,115 → 1,073, possibly-in-label 108. Next: step 10 incremental FAERS. | D043 data v2 (no rule change) |
| v31 | 2026-11-05 | Drug filter on the Workshop screen (ranked list per drug). Next: synonym v2, then step 10. | none |
| v30 | 2026-11-05 | D016 v3 accepted by you. No change to step or plan. | D016 v3 → Accepted |
| v29 | 2026-11-05 | D016 v3 buckets live in Foundry: ranked 1,210 → 1,115; signals unchanged. Next: your OK on D016 v3, drug filter, step 10. | D016 v2 → v3 (proposed) |
| v28 | 2026-11-05 | D043 (synonym table) accepted by you. No change to step or plan. | D043 → Accepted |
| v27 | 2026-11-05 | Synonym table syn_v1 live in Foundry: ranked 1,355 → 1,210, 72 possibly-in-label; US-spelling fix; NAION confirmed unlabeled. Next: your OK on D043, D016 efficacy update, drug filter, step 10. | New D043 (proposed); D037 spelling list extended (bug fix) |
| v26 | 2026-11-04 | Step 9 done: 13-drug formulary end to end, all counts reconciled; 2,047 signals (1,355 ranked); DQ42 handled. Top risk: false positives at scale. Next: synonym table, D016 efficacy update, drug filter; then step 10 incremental. | D031 v4 → v5 (via D039 G1) |
| v25 | 2026-11-04 | Workshop polish v0.3: rounded numbers, readable decisions table, evidence list in reading order. Next: step 9. | none (learning only) |
| v24 | 2026-11-04 | D023 v2, D016 v2, D042 accepted by you. No change to step or plan. | D023 v2, D016 v2, D042 → Accepted |
| v23 | 2026-11-04 | Step 8 done: PRR stats + 271 signals (125 ranked) in Foundry; Workshop module MSSM Safety Officer with triage Action, decision persists after reload. Top risk now false positives (synonyms). Next: your OK on the 3 proposals, then step 9 widen to formulary. | New D042 (proposed); D023 v1 → v2 (proposed); D016 v1 → v2 (proposed) |
| v22 | 2026-11-04 | Prompt p2 live: atomic terms; strict recall 0.31 → 1.00 on short gold sections, 448/448 grounded. Next: step 8. | none (learning only) |
| v21 | 2026-11-04 | D041 (AI label extraction) accepted by you. No change to step or plan. | D041 → Accepted |
| v20 | 2026-11-04 | Step 7 pilot done: AI extraction in Foundry (Claude Sonnet 5.5, 9 sections, 403 grounded reactions, recall 0.91 on gold, cache = 0 calls on rebuild). Model imported into the project with your OK. LabeledReaction object added. Next: step 8 signal + Workshop; prompt p2 for atomic terms. | New D041; first optimization-log entry O1 |
| v19 | 2026-11-04 | D040 (first Ontology path) accepted by you. No change to step or plan. | D040 → Accepted |
| v18 | 2026-11-04 | Step 6 done: first Ontology path (4 object types + TriageDecision, 5 link types, create-only Action). Gate passed in Object Explorer; Action save proven (survives rebuild). Blocker "Action save untested" closed. Next: step 7 AI label extraction. | New D040 |
| v17 | 2026-11-04 | Step 5 done: 7 clean baseline datasets (FAERS cases/reactions/drug×reaction, label versions/sections, recalls/recall match), 0 duplicate keys; FAERS numbers equal the Oct 20 prototype (792,346 cases; oxycodone 4,464 → 3,408 after fold). New background dataset `clean_faers_case_reactions` (contract addition). Next: step 6 Ontology + Action save. | none (learnings only) |
| v16 | 2026-11-04 | Step 4 done: 5 identity datasets in Data/clean, 0 duplicate keys, OxyContin chain resolves in Foundry. Clean layer uses polars lightweight transforms (~1 min builds). VS Code workspace auto-sync lost one uncommitted file once (re-added). | none (learnings only) |
| v15 | 2026-11-04 | Step 3 done: 5 pulls, 4 sources (openFDA, DailyMed, RxNav, FAERS files), 10 raw datasets, all equal to source totals. Bugs caught by count checks: openFDA OR needs parentheses (11→25); Drugs@FDA needs the ingredient field (47→141). Next: step 4 identity. | none (learnings only) |
| v14 | 2026-11-04 | Step 2 done: dataset contracts v1 accepted with all gate defaults (13 ingredients after the slice, product = application number, one reference label, uncertain shown, 3 new egress hosts, D020–D024 accepted). Step 3 starts with oxycodone. | New D039; D020–D024 → Accepted |
| v13 | 2026-11-04 | Phase 2 started. Foundry access proven: AIP Logic test reply in 2.9 s (GPT-5.6 Sol; Claude/Gemini/Grok listed); openFDA REST source + self-approved egress + Python external transform landed 1 real oxycodone recall (HTTP 200). 9-folder layout created. Demo date dropped ("no rush"). Action save still untested. | D031 v3 → v4; new D038; 4 learnings |
| v12 | 2026-11-02 | Reference set v2 built: 62 drugs screened, 30 traced through 8 sources (240 answers, 3,403 automated checks pass; live re-check: 530/530 sources identical, 30/30 answers unchanged). v1 FAERS failure explained (openFDA key needed for `limit>100`); key now in user's shell. Pharmacist review pending. Foundry status unchanged (unverified). | New D037 (proposed); 4 learnings |
| v11 | 2026-10-31 | Data Forge episodes 3/6/9 + official docs researched; conventions, two diagrams and 12-step build order published. Build status remains unverified; historical capacity estimate marked stale. | D036 (documentation only) |
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
