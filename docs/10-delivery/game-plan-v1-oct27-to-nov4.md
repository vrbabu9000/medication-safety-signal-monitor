# Game plan v1 — Oct 27 → demo Wed Nov 4

_Written 2026-10-27 · Compass v10 · Decision D031 v3 · Tracker: [BACKLOG](BACKLOG.md)_

## Where we are (one paragraph)
Exploration and design are **done** (9 atlas pages, all sources profiled, real FAERS run end to end in plain Python, ~30 decisions proposed).
**Nothing is built in Foundry yet.** No work happened Oct 21–27 (7 days). The original plan had Foundry pipelines finished by Oct 28. So we are ~1 week behind on the build, but not on the thinking.

## The deal
| Who | When | What |
|---|---|---|
| Claude | Oct 27–28 (while you are away) | Builds a **ready-to-run kit**: every Foundry transform written, click-by-click guides, approval sheet, diagrams, gold set pre-filled, demo + note skeletons. |
| You | Oct 29 → Nov 3 | Only hands-on Foundry work, checking, labelling, rehearsing. No reading of long docs. |
| Boss | Today | Agree to move the demo to **Wed Nov 4** (Nov 3 = Election Day). |

## Capacity (D031 v3)
| | Hours |
|---|---|
| Your time Oct 29–Nov 2 (5 days × ~10 h) + Nov 3 (~4 h) | **~54** |
| Your work left after cuts | **~41** |
| Load | **~76% · Green** — the ~13 h gap is the buffer for Foundry surprises (Developer Tier is new to you) |

## Day by day
| Day | Focus (BACKLOG IDs) | Exit check by night |
|---|---|---|
| **Tue Oct 27** (today) | (you) Text boss — 5 min · (Claude) start the kit | Boss replied · kit started |
| **Wed Oct 28** | (you, optional 1 h) Approve decisions sheet (E5) + log in to Developer Tier, upload 1 FAERS file, check AIP is enabled · (Claude) finish the kit | You know Foundry + AIP work before lock-in |
| **Thu Oct 29** 🔒 | B1 FAERS raw upload + parse · B2 drug identity | `drug_identity` + FAERS Q1 raw in Foundry |
| **Fri Oct 30** | B3 FAERS clean (incremental: load Q1, then add Q2) + PRR · B4 labels · B5 recalls | All 4 sources clean |
| **Sat Oct 31** | B6 ontology objects + links · B7 Part B LLM extraction in AIP + cache + grounding | Ontology browsable; extractions on 11 drugs |
| **Sun Nov 1** | B8 gold set 6 labels → F1 · B9 signal logic + ChangeEvent · B10 Workshop start · send boss 3-line progress text | F1 number exists; signal list exists |
| **Mon Nov 2** | B10 Workshop finish + triage write-back · B11 monitoring · B12 optimization log | **Feature freeze 8 pm.** Officer flow works end to end |
| **Tue Nov 3** 🗳️ | B13 one-page note · B14 demo script + 1 rehearsal · vote | Demo-ready |
| **Wed Nov 4** | **Demo (20 min)** | — |

_Dates checked against the 2026 calendar: Oct 29 = Thu, Nov 2 = Mon (last build day), Nov 3 = Tue (Election Day), Nov 4 = Wed._

## What was cut (D031 v3 — all 6 cuts applied now, plus 2)
| Cut | Saves you |
|---|---|
| Trials as a source · OnSIDES comparison · daily FAERS + SrLC backtest | ~2 h |
| Gold set 10 → 6 labels (say "wider error bars") | 2 h |
| Rehearsals 2 → 1 | 2 h |
| Exenatide + tirzepatide → **11 drugs** (8 opioids + semaglutide, liraglutide, dulaglutide) | 2 h |
| **New:** decision review 5 h → 1 h (Claude makes a one-page approve sheet, default = accept) | 4 h |
| **New:** gold-set draft check folded into B8 (same labels) | 2 h |

**Never cut:** drug identity · Part B accuracy (gold set + grounding) · recalls · triage write-back · monitoring.

## If things go wrong
| Trigger | Do this |
|---|---|
| End of Fri Oct 30 and sources not clean | Drop SrLC + NDC Directory bridges' extras; recalls match on application no. only |
| AIP not on Developer Tier | Stop and tell Claude same day. Decide then (don't guess now) |
| End of Sun Nov 1 and no signal list | Workshop = 2 screens only (signals + drill-down); recalls shown as a table on the drug page |
| Boss says Nov 2 or Nov 3 | Demo what works + the reasoning trail. Brief: "a partial build with clear reasoning is better than a complete one you cannot explain." |

## Risks (honest)
- **Foundry speed is the unknown.** You have not built in the Developer Tier yet. The Wed Oct 28 test (1 h) is the cheapest way to find out.
- **AIP on Developer Tier is unverified.** Part B depends on it.
- The 10 h/day assumption is yours ("all in"). If it is 7 h/day, load goes to ~100% and we apply the "if things go wrong" rows early.
