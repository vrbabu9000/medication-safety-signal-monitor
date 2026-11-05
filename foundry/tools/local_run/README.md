# foundry/tools/local_run/ — test a transform without Foundry

`run_local.py` loads a transform file, swaps Foundry's libraries for small stand-ins, and runs it.
- **Raw transforms** call the real public APIs (openFDA, DailyMed, RxNav, FDA downloads) with a plain `requests` session.
- **Outputs** are saved to `out/` (git-ignored): tables as `<dataset>.jsonl`, files datasets as folders.
- **Clean transforms** read those files as their inputs via `input.polars()` / `input.pandas()`. So you can test raw → clean on your machine or in a cloud session.

```bash
pip install requests polars
```

```bash
python foundry/tools/local_run/run_local.py foundry/pipelines/raw/raw_rxnorm.py
```

| Flag | Meaning |
|---|---|
| `--limit-rows N` | sample rows printed per output (default 2) |
| `--func NAME` | run only one transform in a file |
| `--out DIR` | where outputs go (default `foundry/tools/local_run/out/`) |

Verified 2026-11-04: local counts equal the Foundry builds (`raw_rxnorm_lookup` 2, `raw_rxnorm_related` 271, `raw_openfda_enforcement` 25, `raw_openfda_drugsfda` 141, `raw_openfda_ndc` 313).

Also here: [synonym_candidates.py](synonym_candidates.py) finds label wording that may match an unlabeled FAERS term (A014).

Limits:
- This is **not** a Foundry emulator. Spark functions such as `df.withColumn` are not available. Write clean transforms with polars (`transform.using` + lightweight) to test them here, or test Spark logic in Foundry.
- `raw_dailymed_spl.py` makes 266 web calls (~2 min). `raw_faers_quarters.py` downloads ~127 MB and writes ~690 MB.
- DailyMed rate-limits fast pulls (HTTP 429 for 744 of 1,321 labels on 2026-11-04): they become error rows; re-run or refetch slowly.
- Outbound internet must be allowed (a cloud environment may block some hosts).
- Results here never replace the Foundry check: row count = source total, on the dataset page.
