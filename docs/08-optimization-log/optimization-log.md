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
| O2 | 2026-11-05 | FAERS clean (2 quarters, 13 drugs) | Full rebuild `clean_faers.py`: reads both quarters (819,683 DEMO rows + DRUG/REAC), **32 s** build | Incremental by quarter ([A015](../05-approaches/A015-incremental-faers.md)): read only the new quarter, merge into a kept state, then rebuild outputs from the state | Adding Q2: reads 1 quarter (422,459 DEMO rows, 52%) + state; **88 s** (state 1 m 2 s + outputs 26 s). Outputs identical (EXCEPT ALL both ways = 0 rows) | **No** (2.75× slower) | Fixed cost of reading/writing 3 state datasets + the quarter log and a second build outweighs one quarter's parsing at N = 2. Re-measure at 4+ quarters; try one build for state + outputs |
| O3 | 2026-11-05 | DailyMed raw pull (13 drugs, 1,321 labels) | Full pull every build: ~30 index pages + **1,321 XML downloads**, **3 m 23 s** (step 9 build, same scope) | Reuse XML already held for the same setid + version: read the previous output (`@incremental`, `dataframe("previous")`), download only new or non-XML replies, replace both outputs | **2 XML downloads** (the 2 DQ42 "None" replies, re-tried by design), 1,319 reused; **1 m 23 s** (−59%). Same 1,321 rows, all 200 | **Yes** | Also cuts the HTTP 429 risk (fewer calls). Freshness unchanged: the index is still pulled every build, so a new label version is still fetched the same day. Baseline from an earlier build, not back-to-back |
| O3a | 2026-11-05 | FAERS clean (full rebuild) | Parse every column of DEMO/DRUG/REAC, then keep 4–13 | Parse only the needed columns (`read_csv(columns=…)`) | DRUG file parse 0.17–0.27 s → 0.07–0.09 s locally, outputs identical (sorted hashes); whole local run 12.3–13.0 s → 12.2 s | **No** (not worth it) | Parsing is not the bottleneck; reverted so Foundry and local stay identical |
| O1b | 2026-11-06 | AI label extraction widened (D041 v2: 5 labels, 21 sections) | Without a cache, every build would send all 21 sections to the model (21 calls) | Same cache (D005) | Widening build: **12 model calls** (only the new sections; 44,869 + 26,226 tokens), 9 sections reused. Forced rebuild with unchanged text: **0 model calls, 21/21 from cache** | Yes | Measured in Foundry SQL (`from_cache`, `called_at`). Confirms O1 at 2.3× the size |

## Levers looked at and deliberately not used
| Lever | Decision | Evidence | Revisit when |
|---|---|---|---|
| Partitioning (e.g. FAERS by quarter) | Not used in the pilot: datasets are written unpartitioned (**D048, proposed**) | Largest table 2,554,017 rows (`clean_faers_case_reactions`); slowest clean build 32 s; O3a showed faster parsing does not move the build, so reading rows is not the bottleneck. How much of the 32 s is Spark/container start-up was **not measured** | FAERS holds 8+ quarters, or any build passes 5 minutes |

