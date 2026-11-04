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
| O1 | 2026-11-04 | AI label extraction (2 labels, 9 sections) | Run 1: 9 model calls, 41,704 prompt + 29,072 completion tokens, 143 s model time, job 2 m 43 s | Cache by content hash + prompt/model version (D005), via incremental previous output | Rebuild after an upstream refresh with unchanged text: **0 model calls, 0 tokens**, 9/9 from cache, same 403 rows | Yes | Measured in Foundry (`from_cache`, `called_at` unchanged). Job wall time not yet compared like-for-like |
