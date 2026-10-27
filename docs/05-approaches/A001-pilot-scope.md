# A001 — Pilot scope: opioids, monitoring-first, showcase of reasoning

| | |
|---|---|
| **Date** | 2026-10-13 |
| **Design-thinking stage** | Define |
| **Area** | Scope |
| **Status** | Trying (confirm ingredient list next session) |
| **Replaces** | Default G1 (GLP-1) in the meeting sheet |

## What changed
| Before | Now | Why |
|---|---|---|
| Pilot class = GLP-1 agonists | Pilot class = **opioids (narcotics)** _(superseded 2026-10-20 by A003: 8 opioids + 5 GLP-1)_ | Boss suggested it. Strong hospital relevance. Clean backtest available |
| Monitoring = stretch goal | Monitoring = **must-have, demo centerpiece** | Boss: "monitoring is the beauty"; show production-side use |
| Drift = compare label versions / model changes | Drift judged over a **3–4 week window**; ignore 3–4 day swings | Boss guidance (our reading, to confirm) |
| Goal = working build | Goal = **working build + visible reasoning trail** | Project is a showcase of thinking |
| Foundry access unknown | **Palantir free Developer Tier** | Boss instruction |

## The idea in 3 lines
1. Go deep on ~12 opioid ingredients, end to end.
2. Make monitoring (pipeline health + AI health + drift) look like real production operations.
3. Every choice is written down. The docs are half the deliverable.

## Proposed opioid list (confirm)
| Group | Ingredients |
|---|---|
| Core hospital opioids | morphine, hydromorphone, fentanyl, oxycodone, hydrocodone, methadone |
| Partial / atypical | buprenorphine, tramadol, tapentadol |
| Others | oxymorphone, codeine, meperidine |
| _Maybe (not a narcotic, but opioid-related)_ | naloxone, the reversal agent. Useful context, keep out of signals |

## Why opioids work well (🩺 PV SME + 💊 safety officer views)
- **Hospital relevance:** on the ISMP high-alert medication list. Respiratory depression and dosing errors are real inpatient risks. 💊 *"These are the drugs I worry about every day."*
- **Backtest material:** FDA has added opioid label safety changes over the years. Example: a 2023 class-wide labeling update that included opioid-induced hyperalgesia (pain that gets worse with opioids). ⚠️ _Exact dates and wording to verify against DailyMed label history._ That gives a natural "would we have caught it?" test.
- **Recalls:** expected (e.g. fentanyl patches, compounded injectables). ⚠️ _Unverified. Check in source profiling._

## Opioid-specific traps to plan for (feeds the data-issues register)
| Trap | Why it matters | Plan |
|---|---|---|
| Abuse, misuse and overdose reports dominate FAERS | Swamp real clinical signals | Tag or separate abuse/misuse/overdose terms; analyze clinical use separately |
| Labels are already long (boxed warnings for addiction, respiratory depression…) | Many reactions are "labeled" → fewer unlabeled signals | Fine. Fewer, better flags. Show the label passage that covers each one |
| Combination products (oxycodone + acetaminophen, etc.) | Which ingredient gets the blame? | Map to each ingredient via RxNorm; flag combos |
| Polydrug reports (with benzodiazepines, alcohol) | Confounding | Use suspect-role filter (DQ05); note it in the signal |
| Many generics / repackagers | Many labels per ingredient (DQ07) | Reference label per ingredient |

## Monitoring scope (now a must)
| Layer | What we watch | Example alert |
|---|---|---|
| Pipeline: freshness | Last successful update per source vs. expected clock | "Recalls not refreshed in 9 days (expected weekly)" |
| Pipeline: row counts | Unusual jumps or drops | "FAERS quarter rows −40% vs previous" |
| Pipeline: schema | Columns added, removed or changed type | "Enforcement API added field X" |
| Pipeline: build time + cost | Duration, compute, LLM tokens per run | "LLM step cost 3× usual" |
| AI: hallucination | % of extracted reactions not found in the source passage, on the gold set | "Grounding rate dropped below 95%" |
| AI: drift | Change in extraction output and signal ranks over a **3–4 week rolling window**; short 3–4 day swings ignored | "20% of labeled reactions changed vs 4 weeks ago with no new label version" |

⚠️ **Timing risk:** we have only ~3 weeks, and FAERS updates quarterly. To *show* drift over weeks, we'll need either (a) daily runs from kickoff, plus (b) **replaying history**: feed past label versions and FAERS quarters in as if they were arriving over time. Decide in a later approach (A00x Monitoring design).

## Verdict
Trying. Lock once you confirm the ingredient list and the drift reading.
