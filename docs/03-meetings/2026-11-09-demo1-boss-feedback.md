# Boss meeting — Demo 1 debrief (feedback log)

| | |
|---|---|
| **Date of demo** | _likely Mon 2026-11-09 (the slot asked for on 6 Nov) — please confirm_ |
| **Who** | Boss · Etter (outside reviewer, who flagged the PRR outlier) · you (presenter) |
| **Design-thinking stage** | Test → back to Empathize (for the UI) |
| **Status** | Logged. Demo 2 plan: [demo2-plan-v1.md](../10-delivery/demo2-plan-v1.md) |

## The one-line takeaway
Under all five points the boss asked one thing: **"Do you own this system like the person who designed it?"** He probed three things an FDE (Forward Deployed Engineer) is judged on:
1. **Cost and operability.** What does it cost to run, and can you prove that from logs?
2. **Metric trust.** Can you defend every number on screen, including the odd ones?
3. **User workflow.** Does the tool fit how the officer actually works?

## What the boss said (as you reported it)
| # | Feedback | Our gap today |
|---|---|---|
| 1 | Asked right at the start: how is the incremental pipeline set up, where are the compute logs, and what does it cost? If one dataset changes, how much compute does that cost, estimated from logs? | We have wall-clock seconds and AI tokens ([optimization log](../08-optimization-log/optimization-log.md) O1–O3) but no compute-seconds or cost figures. No "dataset X changes → these builds rerun → cost Y" table. Incremental is 2.75× slower at 2 quarters (O2) |
| 2 | Explain the data ontology in depth, with every decision behind it. Check whether a refactor can cut cost | No single doc that walks through every ontology decision. No cost per object type. No refactor tried |
| 3 | We sorted PRR in descending order on the home screen; Etter said the top value looked like an outlier. He asked how it was calculated in the backend, how I will handle outliers, and how I know the metrics are accurate. I answered with compute logs and where they are stored, since only the system's designer would know this | Small counts are not handled: PRR blows up when very few other drugs report the reaction. The ranking uses χ², but sorting by PRR brings these rows to the top. No outlier rule. No "why is this number big" trace on screen |
| 4 | Needs much more data-engineering cost thinking to develop the project further | No cost model per build, per month or at scale |
| 5 | Not enough thought about workflow. How would a safety officer actually use this? The screen is pale: no colours for ranking or outliers. It should show progress ("2 of 126 recalls reviewed", "100 of 1,040 not-in-label records reviewed") and flag critical items. Treat this as its own exercise: research the officer's real workflow from online sources, then design the UI around it, with good colours, few clicks and a clear statement of time saved. Add a "?" icon that explains each part. Outlier handling, compute cost and data lineage must be reachable from the UI. React is fine but it must be linked to Palantir | Workshop, 4 pages, metric cards, triage button. No colour, no progress counters, no critical flags, no help, no lineage, cost or outlier panels. Workflow never researched |
| 7 | Next demo must be much stronger, with every loose end tied up | — |

_Point 6 was not given (numbering kept as you sent it)._

## Our reflection
- 🩺 **PV SME view (drug-safety expert):** Point 3 is the most urgent. One silly top number makes a reviewer doubt all of them. There are standard fixes:
  - Rank by the lower 95% bound of PRR, not PRR itself.
  - Or use a shrinkage score, which pulls small-count values toward normal. EBGM is the FDA's version; IC is the WHO's.
  - Show a small-count badge on screen.
- 🔧 **Data Engineer view:** "Compute logs" means two things:
  - Foundry's own build history. Whether Developer Tier shows it is unverified.
  - Our own run-log dataset, written by every transform. We control this one and can show it in the UI.
- 🏗️ **Architect view:** Explain incremental honestly. Show the point where it starts to win and the cost curve at 8 and 20 quarters.
- 💊 **Safety-officer view:** Her morning is a **queue to work down**, not a dashboard to look at.

## Your choices (2026-11-09)
| Question | Answer |
|---|---|
| UI path | **React + OSDK** (Palantir's Ontology SDK, a coding library that reads and writes our Foundry data). Step one is checking that Developer Tier allows it. Workshop v2 is the fallback |
| Demo 2 date | **No fixed date.** Plan by milestones (in line with D031 v4) |
| Which row was the outlier | Not remembered. Claude finds the highest-PRR row in Foundry and traces it end to end |

## Draft workstreams for Demo 2 (to become the task plan)
| WS | Name | Boss point | Order |
|---|---|---|---|
| W3 | Metric trust and outlier handling | 3 | 1 |
| W1 | Compute and cost logs, plus "change ripple cost" | 1, 4 | 2 |
| W4 | Research on the officer's workflow | 5 | 3 |
| W2 | Ontology decision walk-through and cost refactor | 2 | 4 |
| W5 | New UI (React + OSDK) | 5 | 5 |
| W6 | Demo 2 story and cue card | 7 | 6 |
