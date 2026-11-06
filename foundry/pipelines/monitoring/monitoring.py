# Monitoring (Part D, D008 must-have, D009 3-4 week window), step 11. Two outputs:
#   - monitoring_checks: one row per check per build (pipeline, data, AI, freshness). Kept over builds (incremental), so a
#     check's history is visible and a row-count drop is measured against the previous build, not guessed.
#   - monitoring_drift: weekly / quarterly series rebuilt from source dates ("historical replay", D009: we cannot wait 3-4 weeks
#     of live builds in the pilot, so the window is replayed from dates the sources carry). Last 4 weeks vs the 4 before.
# Status: pass / warn / fail. A check never stops a build here; Foundry Data Health checks on the key datasets do that (A016).
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/monitoring.py
from datetime import date, datetime, timedelta, timezone

import polars as pl
from transforms.api import Input, Output, incremental, transform

CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
CURATED = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/"
MONITOR = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/monitoring/"
CHECK_SCHEMA = {"run_at": pl.Utf8, "check_id": pl.Utf8, "area": pl.Utf8, "dataset": pl.Utf8, "metric": pl.Utf8, "value": pl.Float64,
                "previous": pl.Float64, "threshold": pl.Utf8, "status": pl.Utf8, "detail": pl.Utf8}
DRIFT_SCHEMA = {"series": pl.Utf8, "grain": pl.Utf8, "period": pl.Utf8, "value": pl.Float64, "window_now": pl.Float64,
                "window_before": pl.Float64, "ratio": pl.Float64, "status": pl.Utf8, "kind": pl.Utf8, "run_at": pl.Utf8}
ROW_DROP_WARN = 0.20  # a key dataset losing >20% of rows since the last build is a warning
DRIFT_HIGH, DRIFT_LOW = 2.0, 0.5  # D009: last 4 weeks vs the 4 before; a doubling or halving is worth a look


def previous(out):
    try:
        return out.polars(mode="previous")
    except Exception:  # first build
        return None


def days_since(day, today):
    try:
        return (today - date.fromisoformat(str(day)[:10])).days
    except ValueError:
        return None


def check(rows, run_at, check_id, area, dataset, metric, value, threshold, status, detail, prev=None):
    rows.append({"run_at": run_at, "check_id": check_id, "area": area, "dataset": dataset, "metric": metric,
                 "value": None if value is None else float(value), "previous": prev, "threshold": threshold, "status": status, "detail": detail})


def key_checks(rows, run_at, name, df, key, last):
    n, dups, nulls = df.height, df.height - df.select(key).n_unique(), df.filter(pl.col(key).is_null()).height
    check(rows, run_at, f"{name}.key_unique", "data", name, "duplicate keys", dups, "= 0", "pass" if dups == 0 else "fail", f"{key} unique")
    check(rows, run_at, f"{name}.key_not_null", "data", name, "null keys", nulls, "= 0", "pass" if nulls == 0 else "fail", f"{key} not null")
    before = last.get(f"{name}.rows")
    drop = (before - n) / before if before else 0.0
    status = "fail" if n == 0 else ("warn" if drop > ROW_DROP_WARN else "pass")
    check(rows, run_at, f"{name}.rows", "pipeline", name, "rows", n, f"> 0; drop <= {ROW_DROP_WARN:.0%} vs last build", status,
          "first build" if before is None else f"{before:.0f} -> {n} ({-drop:+.1%})", before)


def weekly(df, date_col, series, today, run_at, weeks=12):
    """Counts per ISO week for the last `weeks` weeks, then last 4 weeks vs the 4 before (D009)."""
    start = today - timedelta(weeks=weeks)
    d = df.select(pl.col(date_col).cast(pl.Utf8).str.slice(0, 10).str.to_date("%Y-%m-%d", strict=False).alias("d")).drop_nulls()
    d = d.filter((pl.col("d") >= start) & (pl.col("d") <= today)).with_columns(pl.col("d").dt.truncate("1w").alias("week"))
    counts = {r["week"]: r["n"] for r in d.group_by("week").agg(pl.len().alias("n")).to_dicts()}
    first = start - timedelta(days=start.weekday())
    weeks_list = [first + timedelta(weeks=i) for i in range(weeks + 1)]
    vals = [float(counts.get(w, 0)) for w in weeks_list]
    now, before = sum(vals[-4:]), sum(vals[-8:-4])
    ratio = now / before if before else None
    status = "pass" if ratio is None or DRIFT_LOW <= ratio <= DRIFT_HIGH else "warn"
    return [{"series": series, "grain": "week", "period": w.isoformat(), "value": v, "window_now": now, "window_before": before,
             "ratio": ratio, "status": status, "kind": "historical_replay", "run_at": run_at} for w, v in zip(weeks_list, vals)]


def quarterly(cases, run_at):
    """FAERS has quarters, not weeks: per quarter, the share of reports with known quality problems (DQ38, D023 v2)."""
    q = cases.group_by("quarter").agg(pl.len().alias("cases"), (pl.col("occp_cod") == "").mean().alias("reporter_type_blank"),
                                      (pl.col("n_drug_rows") >= 30).mean().alias("mass_report_share"),
                                      pl.col("dup_suppressed").mean().alias("duplicate_share")).sort("quarter")
    out = []
    for name in ["cases", "reporter_type_blank", "mass_report_share", "duplicate_share"]:
        vals = q[name].to_list()
        ratio = vals[-1] / vals[-2] if len(vals) > 1 and vals[-2] else None
        status = "pass" if ratio is None or DRIFT_LOW <= ratio <= DRIFT_HIGH else "warn"
        out += [{"series": f"faers.{name}", "grain": "quarter", "period": p, "value": float(v), "window_now": float(vals[-1]),
                 "window_before": float(vals[-2]) if len(vals) > 1 else None, "ratio": ratio, "status": status, "kind": "historical_replay",
                 "run_at": run_at} for p, v in zip(q["quarter"].to_list(), vals)]
    return out


@incremental(semantic_version=1, snapshot_inputs=["signals", "recalls", "labels", "changes", "extractions", "cases", "faers_log"])
@transform.using(checks_out=Output(MONITOR + "monitoring_checks"), drift_out=Output(MONITOR + "monitoring_drift"),
                 signals=Input(CURATED + "ontology_signal_signals"), recalls=Input(CURATED + "ontology_recall_recalls"),
                 labels=Input(CURATED + "ontology_label_labels"), changes=Input(CURATED + "ontology_change_events"),
                 extractions=Input(CURATED + "ai_label_section_extractions"), cases=Input(CLEAN + "clean_faers_cases_current"),
                 faers_log=Input(CLEAN + "clean_faers_inc_log"))
def compute(checks_out, drift_out, signals, recalls, labels, changes, extractions, cases, faers_log):
    now = datetime.now(timezone.utc)
    run_at, today = now.isoformat(), now.date()
    old = previous(checks_out)
    last = {}
    if old is not None and old.height:
        latest = old.filter(pl.col("run_at") == old["run_at"].max())
        last = {r["check_id"]: r["value"] for r in latest.to_dicts()}
    sig, rec, lab, chg = signals.polars(), recalls.polars(), labels.polars(), changes.polars()
    ext, cas = extractions.polars(), cases.polars().select("quarter", "occp_cod", "n_drug_rows", "dup_suppressed", "fda_dt")
    rows = []

    # Pipeline + data: keys and row counts on what the screen reads.
    for name, df, key in [("ontology_signal_signals", sig, "signal_key"), ("ontology_recall_recalls", rec, "recall_number"),
                          ("ontology_label_labels", lab, "label_key"), ("ontology_change_events", chg, "event_id")]:
        key_checks(rows, run_at, name, df, key, last)

    # Freshness: each source on its own clock (D028).
    age = days_since(rec["source_last_updated"].max(), today)
    check(rows, run_at, "openfda.freshness", "freshness", "ontology_recall_recalls", "days since openFDA update", age, "<= 14",
          "pass" if age is not None and age <= 14 else "warn", f"source_last_updated {rec['source_last_updated'].max()}")
    age = days_since(lab["retrieved_at"].max(), today)
    check(rows, run_at, "dailymed.freshness", "freshness", "ontology_label_labels", "days since DailyMed pull", age, "<= 7",
          "pass" if age is not None and age <= 7 else "warn", f"retrieved_at {lab['retrieved_at'].max()}")
    latest_q = cas["quarter"].max()
    q_end = date(int(latest_q[:4]), int(latest_q[-1]) * 3, 28)
    age = (today - q_end).days
    check(rows, run_at, "faers.freshness", "freshness", "clean_faers_cases_current", "days since end of latest FAERS quarter", age,
          "<= 200 (FDA publishes ~2-3 months after a quarter)", "pass" if age <= 200 else "warn", f"latest quarter {latest_q}")
    log = faers_log.polars()
    check(rows, run_at, "faers.incremental_quarters", "pipeline", "clean_faers_inc_log", "quarters in incremental state",
          log.filter(pl.col("generation") == log["generation"].max()).height, "= quarters in raw files", "pass", "A015 / D044")

    # AI: is the extraction still grounded, and is the cache doing its job (D041, O1)?
    ok = ext.filter(pl.col("status").is_in(["ok", "empty"]))  # the extraction's cacheable statuses
    n_rx, n_gr = ext["n_reactions"].sum() or 0, ext["n_grounded"].sum() or 0
    rate = n_gr / n_rx if n_rx else None
    check(rows, run_at, "ai.grounded_rate", "ai", "ai_label_section_extractions", "quotes found verbatim in the label", rate, ">= 0.95",
          "pass" if rate is not None and rate >= 0.95 else "fail", f"{n_gr} of {n_rx} items grounded")
    errors = ext.height - ok.height
    check(rows, run_at, "ai.section_errors", "ai", "ai_label_section_extractions", "sections not parsed ok", errors, "= 0",
          "pass" if errors == 0 else "warn", f"{ok.height} of {ext.height} sections ok")
    cached = ext["from_cache"].mean()
    check(rows, run_at, "ai.cache_hit_rate", "ai", "ai_label_section_extractions", "sections served from cache", cached,
          "info (1.0 when no label text changed)", "pass", f"model calls this build: {ext.filter(~pl.col('from_cache')).height}")

    # Data judgment made visible: known FAERS weaknesses (DQ38 reporter type, D023 v2 mass reports).
    blank = (cas.filter(pl.col("quarter") == latest_q)["occp_cod"] == "").mean()
    check(rows, run_at, "faers.reporter_type_blank", "data", "clean_faers_cases_current", "share of latest-quarter reports with no reporter type",
          blank, "info; > 0.5 means lawyer/consumer tags are unreliable", "warn" if blank > 0.5 else "pass", "DQ38")
    nolabel = sig.filter(pl.col("is_ranked") & (pl.col("n_reference_labels") == 0)).height
    check(rows, run_at, "signals.ranked_without_label", "data", "ontology_signal_signals", "ranked signals with no reference label",
          nolabel, "= 0 (D039 G4: no label means unknown, not 'not in label')", "pass" if nolabel == 0 else "fail", "label coverage")

    checks = pl.DataFrame(rows, schema=CHECK_SCHEMA)
    history = checks if old is None else pl.concat([old.select(list(CHECK_SCHEMA)).cast(CHECK_SCHEMA), checks])
    drift = (weekly(rec, "report_date", "recalls.reported_per_week", today, run_at)
             + weekly(lab, "effective_date", "labels.versions_effective_per_week", today, run_at)
             + weekly(chg, "event_date", "changes.events_per_week", today, run_at) + quarterly(cas, run_at))
    checks_out.set_mode("replace")
    checks_out.write_table(history)
    drift_out.set_mode("replace")
    drift_out.write_table(pl.DataFrame(drift, schema=DRIFT_SCHEMA))
