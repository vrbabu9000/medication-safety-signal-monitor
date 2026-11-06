# A017 — Monitoring: computed checks, drift replay, Foundry Data Health (step 11)

| | |
|---|---|
| **Date** | 2026-11-05 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Monitoring |
| **Status** | Kept (first version) |
| **Replaces** | none (`foundry/monitoring/` was empty) |

## What changed
| Before | Now | Why |
|---|---|---|
| No monitoring; D008 said it is a must-have | `monitoring_checks` (21 checks per build, kept over builds) + `monitoring_drift` (weekly / quarterly replay) | Brief Part D + D008: notice when the pipeline or the AI gets worse |
| No Foundry Data Health checks | 4 checks: build status + primary key on signals and on current FAERS cases | Foundry's own alerting; failures notify the owner |
| DailyMed 429s turned into error rows only | Retry with back-off (Retry-After, else 2–16 s, max 5 tries) in `raw_dailymed_spl.py` | The 744-label 429 burst seen locally (learning 2026-11-04) |

## The idea in 3 lines
1. **Checks as data:** every check is a row (value, threshold, status, detail) appended each build, so history is queryable and a row-count drop is measured against the last build.
2. **Drift as replay:** D009 asks for a 3–4 week window; the sources carry dates, so the window is rebuilt from them and labelled `historical_replay`.
3. **Two layers:** computed checks explain *what* looks wrong; Foundry Data Health checks *alert* when a build or key breaks.

## How we tested it
Local run twice (second run compares row counts with the first: "1952 -> 1952"); Foundry build, then SQL on `monitoring_checks`.

## Result
| Check | Foundry, 2026-11-05 |
|---|---|
| Keys (signals, recalls, labels, change events) | 0 duplicates, 0 nulls |
| Freshness | openFDA 8 days · DailyMed 0 days · FAERS 130 days after 2026Q2 end — all pass |
| AI grounded rate | **448 / 448** quotes found verbatim (pass ≥ 0.95) |
| AI cache | sections served from cache; model calls this build reported per run |
| FAERS reporter type blank (DQ38) | **warn**: 72% in 2026Q2 vs 34% in Q1 (×2.1) |
| Recalls reported, last 4 weeks vs 4 before | **warn**: 10 vs 3 (×3.3) |
| Ranked signals with no reference label | 0 (pass) |

## Verdict
**Keep.** Two real warnings on the first run show it works. Not yet done: a Health page in Workshop (needs a key column + object type), schedules (so freshness checks fire on their own), and an AI check against the pharmacist-reviewed gold set (accuracy, not just grounding).

## Diagram (if structure changed)
Monitoring layer added to the v1 data-flow diagram in the hand-in set.

## Persona check
- 🤖 AI Engineer: Grounding 100% says the model quotes the label; it does not say the extraction is complete. Recall on the gold set (A011: 0.91 → 1.00 strict on 4 sections) is the accuracy number.
- 🔧 Data Engineer: Appending checks each build is cheap (21 rows); the drift table is small. Schedules are the missing piece.
- 🧐 Evaluator: Meets "you would notice if it got worse" for pipeline and grounding; label for drift must say replay, not live.
