# Optimization log (required deliverable)

Rule: **measured, not asserted.** Every entry has a baseline, a change and an after number. Failed attempts stay in.

## Candidate targets
| Target | Metric | Lever to try |
|---|---|---|
| FAERS ingest + dedup | Build time, compute-seconds | Incremental by quarter; partition by quarter; filter to formulary early |
| LLM extraction | Tokens, cost, time | Only new versions; send relevant sections only; batch; cache by hash |
| Signal stats | Build time | Pre-aggregate counts; recompute only affected drugs |

## Entries
| # | Date | Pipeline | Baseline | Change | After | Helped? | Notes |
|---|---|---|---|---|---|---|---|
| O1 | | | | | | | |
