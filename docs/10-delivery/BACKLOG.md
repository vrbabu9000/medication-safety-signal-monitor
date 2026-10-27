# Backlog — every task to the demo

_Owner of this file: ⏱️ Delivery Lead ([.claude/agents/delivery-lead.md](../../.claude/agents/delivery-lead.md)). Updated: 2026-10-20 · Compass v9_

**Demo: Wed 2026-11-04** (asked of boss; was ~Nov 3). Build Thu Oct 29 → Mon Nov 2 (feature freeze 8 pm). Note + rehearsal Tue Nov 3. _(Oct 21–27: no work.)_
Status: ⚪ Not started · 🟡 In progress · ✅ Done · ✂️ Cut

## Capacity (your hours) — v3, 2026-10-27
| | Hours |
|---|---|
| Your time Oct 29 → Nov 2 (5 days × ~10 h) + Nov 3 (~4 h) | **~54** |
| Your work left: 55 h − all 6 cuts (8 h) − E5 5→1 h (4 h) − E6 folded into B8 (2 h) | **~41** |
| **Load** | **~76% · Green** (buffer ~13 h for Foundry surprises) |

Was 110% Amber on Oct 20. Green now only because every cut is applied and Claude pre-builds the code Oct 27–28.

## Explore (finish by Thu Oct 23)
| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| E0 | Tracker: Delivery Lead, BACKLOG, compass versioning, decision-change log | Claude | 0 | 1 | Oct 20 | ✅ |
| E1 | Atlas: identity (RxNorm + Drugs@FDA), match rates | Claude (session) | 0 | 3 | Oct 22 | ✅ Oct 20 |
| E2 | Atlas: labels (DailyMed + SrLC + OnSIDES), change census, 2 gold-set drafts | Claude (session) | 0 | 5 | Oct 23 | ✅ Oct 20 |
| E3 | Atlas: recalls (Enforcement + NDC Directory), "active" rule | Claude (session) | 0 | 3 | Oct 22 | ✅ Oct 20 |
| E4 | Trials gate (2 h) + daily FAERS / AEMS check (1 h) | Claude (session) | 0 | 3 | Oct 22 | ✅ Oct 20 |
| E5 | Approve decisions from a one-page sheet (default = accept) | You | 1 | 1 | Oct 28 | ⚪ |
| E6 | Hand-check the 2 gold-set drafts | You | 0 | 0 | — | ✂️ folded into B8 |

## Freeze (Fri Oct 24)
| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| F1 | Hub atlas page + architecture v1 (Drug → Product → Package) + ontology v1 diagrams | Claude | 0 | 3 | Oct 28 | ⚪ |
| F2 | Merge the sessions' "Proposed for the logs" (after E5) | Claude | 0 | 1 | Oct 28 | ⚪ |

## Build (Oct 21 → Nov 3)
| ID | Task | Owner | You h | Claude h | Due | Status |
|---|---|---|---|---|---|---|
| B1 | Developer Tier hands-on: upload FAERS raw quarters + parse (explicit schema) | You | 6 | 1 | Oct 29 | ⚪ |
| B2 | `drug_identity` (RxNorm + Drugs@FDA + NDC → Drug / Product / Package) | You + Claude | 3 | 3 | Oct 29 | ⚪ |
| B3 | FAERS clean: upsert by caseid + deletes, duplicate fold, explode, buckets, counts, PRR (incremental) | You + Claude | 3 | 3 | Oct 30 | ⚪ |
| B4 | Labels: raw SPL + section parse (nested under the 4 parent codes) | You + Claude | 2 | 2 | Oct 30 | ⚪ |
| B5 | Recalls pipeline + NDC parse + "active" rule | You + Claude | 2 | 2 | Oct 30 | ⚪ |
| B6 | Ontology objects + links (Drug, Product, Label, LabeledReaction, AdverseEventStat, Recall, Signal, TriageDecision, ChangeEvent) | You + Claude | 3 | 2 | Oct 31 | ⚪ |
| B7 | Part B: LLM extraction in AIP + cache by (setid, version, section, prompt, model) + grounding check | You + Claude | 4 | 4 | Oct 31 | ⚪ |
| B8 | Gold set: hand-label 6 labels (pre-filled from the draft); precision / recall / F1 | You | 3 | 1 | Nov 1 | ⚪ |
| B9 | Signal logic (PRR + Evans + label match) + ChangeEvent feed | You + Claude | 2 | 2 | Nov 1 | ⚪ |
| B10 | Workshop app: ranked signals, drill-down (label quote next to extraction), recalls, "since last review", triage write-back | You + Claude | 6 | 3 | Nov 2 | ⚪ |
| B11 | Monitoring: freshness, row counts, field fill rates, AI accuracy, drift replay | You + Claude | 4 | 3 | Nov 2 | ⚪ |
| B12 | Optimization log with before/after (append vs upsert, LLM cache) | You + Claude | 1 | 1 | Nov 2 | ⚪ |
| B13 | One-page architecture note | You + Claude | 2 | 2 | Nov 3 | ⚪ |
| B14 | Demo script + 1 rehearsal | You | 2 | 1 | Nov 3 | ⚪ |

## Cut list — **all 6 applied 2026-10-27 (D031 v3)** ✂️

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

**Never cut:** drug identity · Part B accuracy (gold set + grounding) · recalls · triage write-back · monitoring.
