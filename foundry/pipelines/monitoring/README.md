# foundry/pipelines/monitoring/ — monitoring datasets (Part D)

Mirror of [monitoring.py](monitoring.py), Foundry repo `Pipelines/pipelines_clean` (`transforms-python/src/myproject/datasets/monitoring.py`), writing to `Data/monitoring`. Decision D046, approach [A017](../../../docs/05-approaches/A017-monitoring-and-health-checks.md). Foundry's own Data Health checks are recorded in [foundry/monitoring](../../monitoring/README.md).

| Output | Grain | What it holds |
|---|---|---|
| `monitoring_checks` (incremental: every build appends) | `run_at` + `check_id` | 21 checks per build: key unique / not null and row count (drop > 20% vs last build = warn) for signals, recalls, labels, change events · freshness of openFDA (≤ 14 days), DailyMed (≤ 7), FAERS (≤ 200 days after quarter end) · quarters in the incremental FAERS state · AI grounded rate (≥ 0.95), sections not parsed, cache hit rate · FAERS reporter-type blank share (DQ38) · ranked signals with no reference label (must be 0) |
| `monitoring_drift` (replaced each build) | `series` + `period` | **Historical replay** (D009): weekly counts for 12 weeks from source dates (recalls reported, label versions effective, change events) and per FAERS quarter (cases, reporter-type blank, mass-report share, duplicate share). Last 4 weeks vs the 4 before: ratio > 2 or < 0.5 = warn |

First Foundry run (2026-11-05): all key/row/freshness checks pass; AI grounded 448 of 448; **warn** on FAERS reporter type blank (72% in 2026Q2 vs 34% in Q1, DQ38) and on recalls reported in the last 4 weeks (10 vs 3 the 4 weeks before). Both are real.

Why replay: the brief's drift window is 3–4 weeks (D009) and the pilot cannot wait that long for live builds. The replay uses dates the sources carry, so it is honest about what it is (`kind = historical_replay`). Live drift starts accumulating in `monitoring_checks` with every scheduled build.

Run locally: `.venv/bin/python foundry/tools/local_run/run_local.py foundry/pipelines/monitoring/monitoring.py` (needs `ai_label_section_extractions.jsonl`; the local AI run is not stored, so make a small stand-in file or skip the AI checks).
