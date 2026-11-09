# Demo 2 plan v1 — tie every loose end from Demo 1

| | |
|---|---|
| **Made** | 2026-11-09 · Compass v42 |
| **Source** | [Demo 1 feedback](../03-meetings/2026-11-09-demo1-boss-feedback.md) |
| **Date of Demo 2** | No fixed date. We plan by **milestone gates**, not by calendar |
| **Design-thinking stage** | Test (Demo 1) → back to Empathize (officer workflow) → Prototype → Test |
| **Tracker** | Task rows also in [BACKLOG](BACKLOG.md) (IDs T1.x–T6.x) |

📊 **Diagram:** [40-demo2-plan-v1.png](../diagrams/png/40-demo2-plan-v1.png) · [PDF](../diagrams/pdf/40-demo2-plan-v1.pdf)

## The goal in one line
At Demo 2 you can answer, from the screen and from memory, **what it costs, why each number is right, and how the officer works through her morning**, because you designed all three.

## Order and why
| Milestone | Workstream | Boss point | Why this order |
|---|---|---|---|
| **M1 Trust** | W3 Metric trust and outliers | 3 | A wrong-looking top number undermines everything else. It's cheap to fix and changes what the UI shows |
| **M2 Cost** | W1 Compute and cost logs | 1, 4 | The UI needs the run log and ripple-cost data to exist before it can show them |
| **M3 Workflow** | W4 Officer workflow research | 5 | No Foundry needed, so it **can run in parallel with M1/M2**. Must finish before the UI is designed |
| **M4 Ontology** | W2 Ontology walk-through and cost refactor | 2 | Any refactor changes object types, so it must land before the React app is wired to them |
| **M5 UI** | W5 React + OSDK app | 5 | Built on top of M1–M4 |
| **M6 Demo** | W6 Demo 2 story | 7 | Last |

**Your learning thread (every milestone):** the boss is testing ownership. Each milestone ends with a **"teach it back"** task: you explain it to Claude in 2 minutes and Claude asks the boss-style follow-ups.

## Tasks
Hours are rough guesses. "You h" means your own time; "Claude h" means Claude's working time, much of it spent in Foundry through the browser.

### M1 · Trust — W3 metric trust and outlier handling
| ID | Task | Owner | You h | Claude h |
|---|---|---|---|---|
| T3.1 | Find the highest-PRR rows in Foundry (read-only SQL). Trace the top one end to end: the 2×2 counts a, b, c, d, the PRR formula, the CI, χ², the label check and the cases behind it | Claude | 0.25 | 1.5 |
| T3.2 | 🩺 PV SME note: the kinds of outliers we have (small c, small a, mass reports, indication terms, stimulated reporting) and the standard defences (lower CI bound of PRR, shrinkage via EBGM or IC, minimum-count rules) | Claude | — | 2 |
| T3.3 | Local prototype: add `prr_lower95`, a shrinkage score, a `small_count` flag and an `outlier_reason` column. Compare the top 20 before and after. **NAION must stay ranked** | Claude | — | 4 |
| T3.4 | Approach file A021 + a new decision on the ranking metric (supersedes nothing; D006 Evans stays the signal rule) | Claude → you approve | 0.5 | 0.5 |
| T3.5 | Push to `ontology_signals.py` in Foundry, rebuild, refresh numbers.json | Claude | 0.5 | 2 |
| T3.L | Teach it back: "Why is this PRR so big, and why do I trust the ranking?" | You | 1 | 0.25 |

**Gate M1:** the outlier is explained, a ranking that resists small counts is live, NAION is still ranked, and you can explain it in 2 minutes.

### M2 · Cost — W1 compute and cost logs
| ID | Task | Owner | You h | Claude h |
|---|---|---|---|---|
| T1.1 | Check what Developer Tier shows: build history, job duration, compute-seconds, usage or cost pages (read-only). **Unverified today** | Claude | 0.25 | 1.5 |
| T1.2 | **Run-log dataset** `monitor_run_log`: every transform appends rows in and out, duration, model calls, tokens and cache hits | Claude | 0.5 | 4 |
| T1.3 | **Ripple-cost table**: for each raw source, which builds rerun when it changes, plus their measured seconds or compute. This answers "if one dataset changes, what does it cost?" | Claude | — | 3 |
| T1.4 | **Incremental crossover**: replay 2 → 4 → 6 → 8 FAERS quarters, incremental vs full, and find where incremental starts to win. _Assumes older quarters can be downloaded; check first_ | Claude | 0.5 | 4 |
| T1.5 | **Cost model**, pilot vs scale: compute-seconds × rate (rate flagged as an assumption if Foundry doesn't show it) plus LLM tokens × price. Per build, per day, per month, at 13 drugs and at 500 | Claude | — | 2 |
| T1.L | Teach it back: "How is the incremental set up, and what does one change cost?" | You | 1 | 0.25 |

**Gate M2:** run log live in Foundry; ripple-cost table and crossover measured and in the optimization log; a monthly cost estimate with its assumptions stated.

### M3 · Workflow — W4 officer workflow research (runs in parallel with M1/M2)
| ID | Task | Owner | You h | Claude h |
|---|---|---|---|---|
| T4.1 | Online research on the medication safety officer's real day: ISMP and ASHP role descriptions, recall handling in hospital pharmacy, FDA safety communications, MedWatch | Claude (🔎 researcher) | — | 3 |
| T4.2 | Journey map (a day in the life), jobs to be done, pain points; diagram | Claude (🎨 design lead) | — | 2 |
| T4.3 | Feature list, scored by **clicks** and **minutes saved**: review-progress counters ("2 of 126 recalls reviewed"), critical flag rules, colour meaning, "?" help text for each part | Claude | 1 | 2 |
| T4.4 | 💊 Safety-officer persona test of the wireframe | Claude | — | 1 |
| T4.L | Teach it back: "Walk me through her morning with the tool" | You | 1 | 0.25 |

**Gate M3:** journey map and scored feature list, approved by you.

### M4 · Ontology — W2 decision walk-through and cost refactor
| ID | Task | Owner | You h | Claude h |
|---|---|---|---|---|
| T2.1 | Ontology decision walk-through: every object type, key, link and Action, with the why (reuse book track 04) + diagram v2 | Claude (🏗️ architect) | — | 3 |
| T2.2 | Cost view per object type: rows, properties, sync or index time from Foundry | Claude | 0.25 | 2 |
| T2.3 | Try 1–2 refactors and measure before/after (e.g. drop unused properties, fold AE Stat into Signal, index only ranked rows). Keep, drop or park each one | Claude | 0.5 | 4 |
| T2.L | Teach it back: "Why is the ontology shaped this way, and what would you change at scale?" | You | 1 | 0.25 |

**Gate M4:** decision walk-through published; at least one refactor measured (kept or dropped, with numbers).

### M5 · UI — W5 React + OSDK app
| ID | Task | Owner | You h | Claude h |
|---|---|---|---|---|
| T5.0 | **Feasibility spike**: on Developer Tier, can we create a Developer Console app, generate the OSDK, host the app in Foundry, and call the triage Action? **Go → React; no-go → Workshop v2** | Claude + you (approvals) | 1 | 2 |
| T5.1 | Design system and wireframes: severity colours, outlier badge, progress counters, "?" icons; checked in light and dark | Claude | 1 | 3 |
| T5.2 | Build the worklist pages: Morning brief, Not-in-label queue, Recalls, What changed | Claude | — | 12 |
| T5.3 | Panels the officer can open: **why this number** (outlier), **where it came from** (lineage), **what it costs and how healthy it is** (run log + checks) | Claude | — | 6 |
| T5.4 | Review tracking for recalls too (new Action), so "X of Y reviewed" counts are real | Claude | 0.5 | 3 |
| T5.5 | Test: click count and stopwatch vs today's Workshop; persona test | Claude + you | 1 | 2 |
| T5.L | Teach it back: "Show me the morning in under 2 minutes" | You | 1 | 0.25 |

**Gate M5:** app live inside Foundry with counters, colours, "?" help and the 3 panels; clicks and minutes measured against today's screen.

### M6 · Demo — W6 the Demo 2 story
| ID | Task | Owner | You h | Claude h |
|---|---|---|---|---|
| T6.1 | New narrative that opens with the officer's morning and answers cost and trust before anyone asks | Claude (🎬 demo director) | — | 2 |
| T6.2 | Update the cue card, the `foundry-demo` skill and the deck slides | Claude | — | 4 |
| T6.3 | Red team (🧐 evaluator) + a **hard-question drill**: the boss's Demo 1 questions and the likely next ones | Claude | 1 | 2 |
| T6.4 | Two rehearsals against live Foundry | You + Claude | 3 | 1 |
| T6.5 | Commit | You | 0.25 | — |

**Gate M6:** two clean rehearsals; every hard question has an answer you can give from the screen.

## Totals
| | You h | Claude h |
|---|---|---|
| M1 Trust | 2.25 | 10.25 |
| M2 Cost | 2.25 | 14.75 |
| M3 Workflow | 2 | 8.25 |
| M4 Ontology | 1.75 | 9.25 |
| M5 UI | 5.5 | 28.25 |
| M6 Demo | 4.25 | 9 |
| **Total** | **~18 h** | **~80 h** |

At ~25 h a week of your time, your part is under a week. Claude's part is spread over several sessions and limited by Foundry build time. **Biggest risk:** T5.0, if Developer Tier can't host an OSDK app. The fallback (Workshop v2) costs about 10 h less but gives less visual freedom.

## Open items
- Debrief date and any missing boss points (meeting note says "to confirm").
- Branch (settled, D051): Demo 2 work lives on branch `demo2`, cut from main. The project record came over from `demo-prep`; the demo-prep pack (cue card, tutorial, book, skill) stays on local `demo-prep`.
