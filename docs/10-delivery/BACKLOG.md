# Backlog — every task to the demo

_Owner of this file: ⏱️ Delivery Lead ([.claude/agents/delivery-lead.md](../../.claude/agents/delivery-lead.md)). Updated: 2026-11-05 · Compass v37_

**Demo: no fixed date** (D031 v4, 2026-11-04: build at our own pace). The old Wed Nov 4 plan is historical → [game plan v1](game-plan-v1-oct27-to-nov4.md).
Status: ⚪ Not started · 🟡 In progress · ✅ Done · ✂️ Cut · ⏸️ Waiting on a decision

## Capacity (your hours) — v4, 2026-11-05
| | Hours |
|---|---|
| Your time | ~25 h / week. No demo date, so "hours left to the demo" cannot be computed |
| Your work left (open items below) | **~4.3 h** (~3.8 h if D041 v2 is declined) |
| Claude work left | **~7 h** (~2 h if D041 v2 is declined) |
| **Load** | **Not computable** (no date). Against one week of your time: 4.3 / 25 h ≈ **17% · Green** _(assumption: the demo is at least a week away)_ |

Historical: v3 (2026-10-27) was ~41 h of your work against ~54 h = 76% Green. v2 (2026-10-20) was 110% Amber.

## Open — to finish the hand-in (added 2026-11-05)
Estimates are rough. Order = do-in order.

| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| H1 | **Batch decision:** accept or reject the 12 proposed decisions (D006, D015, D025–D029, D037, D045–D048) · D041 v2 (widen the AI) yes / no · delete the duplicate Signal→Drug link type in Ontology Manager (~15 min) · name a pharmacist reviewer or keep it as a documented gap. Claude then logs each outcome in DECISIONS and bumps the Compass | You (Claude logs) | 1.5 | 0.5 | — | ✅ Done 2026-11-06 (Compass v38) |
| H2 | **Rehearsal with the 3 checks:** (8) DailyMed Ozempic v20, Cmd+F `optic`; (9) count of active Class I recalls on page 2; (10) a person walks the morning flow with a stopwatch. One timed run of the 20-minute script; fill checklist #8–10 in the [demo guide](../11-handin/demo/demo-navigation-guide.md); capture the missing fallback screenshots (A4 DailyMed search, A6 openFDA record, A6 Class I sort) | You + Claude | 2 | 1.5 | — | ⚪ |
| H3 | **If D041 v2 is accepted:** run the cached AI extractor on the 3 semaglutide reference labels (Ozempic v20, Wegovy v19, oral Ozempic v14); add a Labeled Reactions panel (reaction · quote · section · version) beside the labels-searched panel; rebuild; refresh numbers.json and the deck / R04 / R08 / note / script wording | Claude (you approve model calls) | 0.5 | 5 | — | ✅ Done 2026-11-06 (Compass v38) |
| H4 | **One commit** of everything (message and commands from Claude's last reply) | You | 0.25 | 0 | after H2 (or now) | ⚪ |
| | **Total open** | | **4.25** | **7** | | |

Not scheduled, for your call (from [rubric-check-v2](../11-handin/reviews/rubric-check-v2.md) §3, not requested yet): a person scores 30 long-section AI items (1–2 h you; strengthens "never cut" Part B accuracy) · `example_case_ids` on Signal + `openfda_url` on Recall (~0.5 h Claude) · repeat O2/O3 timings twice (Claude, Foundry time).

## Done — build steps 1–12 (the 12-step [build order](../04-architecture/foundry-conventions/project-build-order-v1.md), run Nov 4–5)
| Step | What | Old IDs | Done | Evidence |
|---|---|---|---|---|
| 1 | Foundry + AIP access proven | E5 (part), B1 | ✅ 2026-11-04 | Compass v13 · [access results](2026-11-04-foundry-access-results.md) |
| 2 | Dataset contracts v1 | F1, B2 | ✅ 2026-11-04 | Compass v14 · D039 |
| 3 | Raw pulls: 4 sources, 10 raw datasets | B1, B4, B5 | ✅ 2026-11-04 | Compass v15 |
| 4 | Drug identity (5 datasets) | B2 | ✅ 2026-11-04 | Compass v16 |
| 5 | Clean baseline (FAERS, labels, recalls) | B3–B5 | ✅ 2026-11-04 | Compass v17 |
| 6 | First Ontology path + triage Action | B6 | ✅ 2026-11-04 | Compass v18 · D040 |
| 7 | AI label extraction + cache + grounding | B7, B8 (start) | ✅ 2026-11-04 | Compass v20 · D041 |
| 8 | Signal statistics + first Workshop screen | B9, B10 (start) | ✅ 2026-11-04 | Compass v23 · D042 |
| 9 | 13-drug formulary end to end | B2–B10 | ✅ 2026-11-04 | Compass v26 · [A013](../05-approaches/A013-widen-to-formulary.md) |
| 10 | Incremental FAERS = full rebuild | B3, B12 | ✅ 2026-11-05 | Compass v33 · [A015](../05-approaches/A015-incremental-faers.md) · D044 |
| 11 | Three-question screen, change feed, monitoring + Data Health checks, AI eval, O3 | B8, B10, B11 | ✅ 2026-11-05 | Compass v35–v36 · [A016](../05-approaches/A016-three-question-screen.md) · [A017](../05-approaches/A017-monitoring-and-health-checks.md) · [ai-eval-v1](../../eval/ai-eval-v1.md) |
| 12 | Architecture note + measured optimization log + known gaps | B12, B13 | ✅ 2026-11-05 (paper part) | Compass v37 · [note](../11-handin/architecture-note/architecture-note.pdf) · [optimization log](../08-optimization-log/optimization-log.md) · rehearsal part → **H2** |

_Flags:_ step 11's "officer under two minutes" and step 12's "one demo rehearsal" are **not** done; both moved to H2. Step 11's AI eval is Claude-reviewed, not human-reviewed (pharmacist pending, H1).

## Done — hand-in Phases B–D ([approved plan](../11-handin/README.md))
| ID | Task | Owner | Done | Evidence |
|---|---|---|---|---|
| HB | Baseline gate: rebuild equal, 5/5 traces, numbers frozen, screenshots | Claude | ✅ 2026-11-05 | [baseline-gate.md](../11-handin/baseline-gate.md) · [numbers.json](../11-handin/numbers.json) · [screens](../11-handin/screens/README.md) |
| C1 | Style kit | Claude (report-writer) | ✅ 2026-11-05 | [tools/handin](../../tools/handin/README.md) |
| C2 | Reports R00–R09 (PDF) | Claude (report-writer) | ✅ 2026-11-05 | [reports/pdf](../11-handin/reports/pdf/) (R00 Start here … R09 demo guide) |
| C3 | Hand-in diagrams 30–37 (30, 32, 33, 36, 37 at v2) | Claude (architect) | ✅ 2026-11-05 | [README-handin](../diagrams/README-handin.md) |
| C4 | One-page architecture note | Claude (architect) | ✅ 2026-11-05 | [architecture-note.pdf](../11-handin/architecture-note/architecture-note.pdf) |
| C5 | Deck (29 slides) + speaking script + storyboard + slide explanations | Claude (deck-designer) | ✅ 2026-11-05 | [MSSM-demo-deck.pdf](../11-handin/deck/MSSM-demo-deck.pdf) · [speaking_script.md](../11-handin/deck/speaking_script.md) |
| C6 | Demo navigation guide (23 stops) + ripple table + rehearsal plan | Claude (demo-director) | ✅ 2026-11-05 | [demo guide](../11-handin/demo/demo-navigation-guide.md) · [ripple-table](../11-handin/demo/ripple-table.md) · [rehearsal-plan](../11-handin/demo/rehearsal-plan.md) |
| C7 | "Another month" research (sources + pharmacist review) | Claude (researcher) | ✅ 2026-11-05 | [another-month file](../09-roadmap/another-month-sources-and-pharmacist-review.md) |
| D1 | Phase D reviews: first-time reader, fact-check, safety officer, cohesion, evaluator v1 + v2 | Claude (personas) | ✅ 2026-11-05 | [reviews](../11-handin/reviews/) |
| D2 | Phase D fixes applied, PDFs and deck rebuilt | Claude | ✅ 2026-11-05 | [phase-d-fix-brief](../11-handin/reviews/phase-d-fix-brief.md) · ACTIVITY-LOG 2026-11-05 (day, 9) |

---

## Historical — Oct 20 plan (superseded by the 12-step build order)
_The ⚪ marks below are the Oct 20 snapshot. B1–B14 were delivered through steps 1–12 above (see "Old IDs"); B14 rehearsal is now H2; E5 is now H1._

### Explore (finish by Thu Oct 23)
| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| E0 | Tracker: Delivery Lead, BACKLOG, compass versioning, decision-change log | Claude | 0 | 1 | Oct 20 | ✅ |
| E1 | Atlas: identity (RxNorm + Drugs@FDA), match rates | Claude (session) | 0 | 3 | Oct 22 | ✅ Oct 20 |
| E2 | Atlas: labels (DailyMed + SrLC + OnSIDES), change census, 2 gold-set drafts | Claude (session) | 0 | 5 | Oct 23 | ✅ Oct 20 |
| E3 | Atlas: recalls (Enforcement + NDC Directory), "active" rule | Claude (session) | 0 | 3 | Oct 22 | ✅ Oct 20 |
| E4 | Trials gate (2 h) + daily FAERS / AEMS check (1 h) | Claude (session) | 0 | 3 | Oct 22 | ✅ Oct 20 |
| E5 | Approve decisions from a one-page sheet (default = accept) | You | 1 | 1 | Oct 28 | → H1 |
| E6 | Hand-check the 2 gold-set drafts | You | 0 | 0 | — | ✂️ folded into B8 |

### Freeze (Fri Oct 24)
| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| F1 | Hub atlas page + architecture v1 (Drug → Product → Package) + ontology v1 diagrams | Claude | 0 | 3 | Oct 28 | ⚪ (not re-checked) |
| F2 | Merge the sessions' "Proposed for the logs" (after E5) | Claude | 0 | 1 | Oct 28 | ⚪ (not re-checked) |

### Build (Oct 21 → Nov 3)
| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| B1 | Developer Tier hands-on: upload FAERS raw quarters + parse (explicit schema) | You | 6 | 1 | Oct 29 | → steps 1, 3 |
| B2 | `drug_identity` (RxNorm + Drugs@FDA + NDC → Drug / Product / Package) | You + Claude | 3 | 3 | Oct 29 | → step 4 |
| B3 | FAERS clean: upsert by caseid + deletes, duplicate fold, explode, buckets, counts, PRR (incremental) | You + Claude | 3 | 3 | Oct 30 | → steps 5, 10 |
| B4 | Labels: raw SPL + section parse (nested under the 4 parent codes) | You + Claude | 2 | 2 | Oct 30 | → steps 3, 5 |
| B5 | Recalls pipeline + NDC parse + "active" rule | You + Claude | 2 | 2 | Oct 30 | → steps 3, 5 |
| B6 | Ontology objects + links (Drug, Product, Label, LabeledReaction, AdverseEventStat, Recall, Signal, TriageDecision, ChangeEvent) | You + Claude | 3 | 2 | Oct 31 | → steps 6–8, 11 |
| B7 | Part B: LLM extraction in AIP + cache by (setid, version, section, prompt, model) + grounding check | You + Claude | 4 | 4 | Oct 31 | → step 7 |
| B8 | Gold set: hand-label 6 labels (pre-filled from the draft); precision / recall / F1 | You | 3 | 1 | Nov 1 | → steps 7, 11 (Claude-written key; pharmacist pending) |
| B9 | Signal logic (PRR + Evans + label match) + ChangeEvent feed | You + Claude | 2 | 2 | Nov 1 | → steps 8, 11 |
| B10 | Workshop app: ranked signals, drill-down (label quote next to extraction), recalls, "since last review", triage write-back | You + Claude | 6 | 3 | Nov 2 | → steps 8, 11 (label passage beside extraction: H3) |
| B11 | Monitoring: freshness, row counts, field fill rates, AI accuracy, drift replay | You + Claude | 4 | 3 | Nov 2 | → step 11 |
| B12 | Optimization log with before/after (append vs upsert, LLM cache) | You + Claude | 1 | 1 | Nov 2 | → steps 10–12 |
| B13 | One-page architecture note | You + Claude | 2 | 2 | Nov 3 | → step 12 / C4 |
| B14 | Demo script + 1 rehearsal | You | 2 | 1 | Nov 3 | script ✅ (C5) · rehearsal → H2 |

## Cut list — **all 6 applied 2026-10-27 (D031 v3)** ✂️ · still the default scope under D031 v4

## Cut list (apply in this order) — v2: each cut names the task and hours it removes
| # | Cut | Removes from | You h saved | Claude h saved | Keeps |
|---|---|---|---|---|---|
| 1 | Trials as a source | E4 (gate still runs) | 0 | ~1 | "Explored, parked" line in the note |
| 2 | OnSIDES comparison | B8 | 1 | 1 | Gold-set F1 |
| 3 | Gold set 10 → 6 labels | B8 | 2 | 0 | F1 still measured, wider error bars (say so) |
| 4 | Demo rehearsals 2 → 1 | B14 | 2 | 0 | One full run |
| 5 | Daily FAERS + SrLC backtest | E4, B11 | 1 | 2 | Quarterly FAERS + SrLC change alerts |
| 6 | Exenatide + tirzepatide (11 drugs) | B3, B8, B10 | 2 | 1 | Opioid-led hybrid still holds |
| | **All cuts** | | **8** | **5** | Load 55 → 47 h = 94% |

Cuts 1–2 cost you almost nothing but also save you almost nothing. **Cuts 3–4 are the ones that actually move your load.**
_Note 2026-11-05: cut 6 was later reversed by D031 v5 (13 drugs, accepted via G1). Cut 4 still holds, so H2 is one rehearsal, though the [rehearsal plan](../11-handin/demo/rehearsal-plan.md) suggests two._

**Never cut:** drug identity · Part B accuracy (gold set + grounding) · recalls · triage write-back · monitoring.
