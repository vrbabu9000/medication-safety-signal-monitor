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
| O2 | 2026-11-05 | FAERS clean (2 quarters, 13 drugs) | Full rebuild `clean_faers.py`: reads both quarters (819,683 DEMO rows + DRUG/REAC), **32 s** build | Incremental by quarter ([A015](../05-approaches/A015-incremental-faers.md)): read only the new quarter, merge into a kept state, then rebuild outputs from the state | Adding Q2: reads 1 quarter (422,459 DEMO rows, 52%) + state; **88 s** (state 1 m 2 s + outputs 26 s). Outputs identical (EXCEPT ALL both ways = 0 rows) | **No** (2.75× slower) | Fixed cost of reading/writing 4 state datasets and a second build outweighs one quarter's parsing at N = 2. Re-measure at 4+ quarters; try one build for state + outputs |
