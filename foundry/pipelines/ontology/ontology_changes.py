# Curated (gold), step 11: question 3, "what has changed since my last review?" (D028, D045). Two outputs feed the screen:
#   - ontology_change_events: one row per change to a signal, recall or label. Two ways a change is found:
#       source_date   = the source itself dates the event (recall reported / terminated, label version effective). Real history,
#                       so the feed is useful from the first build.
#       snapshot_diff = this build compared with the previous build's snapshot (signal new / gone / label status or rank changed,
#                       recall status or class changed, label new version). Dated by the build.
#   - ontology_source_status: one row per source with its "as of" date, because sources update on different clocks (DQ14, D029).
# The snapshot is kept as an incremental output (same pattern as clean_faers_incremental.py, A015).
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/ontology_changes.py
import hashlib
from datetime import datetime, timezone

import polars as pl
from transforms.api import Input, Output, incremental, transform

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
CURATED = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/"
# What counts as a change, per entity: the fields compared between builds.
WATCH = {"signal": ["label_status", "is_ranked", "bucket", "caution"], "recall": ["status", "classification"], "label": ["spl_version"]}
EVENT_SCHEMA = {"event_id": pl.Utf8, "entity_type": pl.Utf8, "entity_key": pl.Utf8, "change": pl.Utf8, "display_name": pl.Utf8,
                "ingredient_name": pl.Utf8, "detail": pl.Utf8, "old_value": pl.Utf8, "new_value": pl.Utf8, "event_date": pl.Date,
                "source": pl.Utf8, "found_by": pl.Utf8, "detected_at": pl.Utf8, "link_url": pl.Utf8}
SNAP_SCHEMA = {"entity_type": pl.Utf8, "entity_key": pl.Utf8, "display_name": pl.Utf8, "ingredient_name": pl.Utf8, "fingerprint": pl.Utf8,
               "fields": pl.Utf8, "link_url": pl.Utf8}
RECALL_URL = "https://api.fda.gov/drug/enforcement.json?search=recall_number:%22{}%22"


def previous(out):
    try:
        return out.polars(mode="previous")
    except Exception:  # first build: no previous output
        return None


def event_id(*parts):
    return hashlib.sha256("|".join("" if p is None else str(p) for p in parts).encode()).hexdigest()[:16]


def snapshot(signals, recalls, labels, label_drugs):
    """Current state of every watched entity: key, a readable name, its drug, and the watched fields as text."""
    def rows(df, kind, key, name, drug, url):
        cols = WATCH[kind]
        return df.select(pl.lit(kind).alias("entity_type"), pl.col(key).cast(pl.Utf8).alias("entity_key"), pl.col(name).alias("display_name"),
                         pl.col(drug).alias("ingredient_name"),
                         pl.concat_str([pl.col(c).cast(pl.Utf8).fill_null("") for c in cols], separator="|").alias("fingerprint"),
                         pl.lit("|".join(cols)).alias("fields"), url.alias("link_url"))
    s = rows(signals, "signal", "signal_key", "display_name", "ingredient_name", pl.lit(None, pl.Utf8))
    r = rows(recalls, "recall", "recall_number", "display_name", "search_ingredient",
             pl.lit(RECALL_URL.split("{}")[0]) + pl.col("recall_number") + pl.lit(RECALL_URL.split("{}")[1]))
    # Labels: one row per setid (the version is a watched field), once per formulary drug the label belongs to.
    lab = labels.join(label_drugs, on="label_key", how="inner")
    l = rows(lab, "label", "setid", "display_name", "ingredient_name", pl.col("dailymed_url"))
    return pl.concat([s, r, l]).unique(["entity_type", "entity_key", "ingredient_name"]).cast(SNAP_SCHEMA)


def diff(old, new, today, now):
    """Snapshot-diff events: new, gone, and changed (one event per changed field)."""
    k = ["entity_type", "entity_key", "ingredient_name"]
    j = old.join(new, on=k, how="full", suffix="_new", coalesce=True)
    out = []
    for r in j.to_dicts():
        name = r["display_name_new"] or r["display_name"]
        base = dict(entity_type=r["entity_type"], entity_key=r["entity_key"], display_name=name, ingredient_name=r["ingredient_name"],
                    event_date=today, source=None, found_by="snapshot_diff", detected_at=now, link_url=r["link_url_new"] or r["link_url"])
        if r["fingerprint"] is None:
            out.append(dict(base, change="new", detail=f"new {r['entity_type']}", old_value=None, new_value=r["fingerprint_new"]))
        elif r["fingerprint_new"] is None:
            out.append(dict(base, change="gone", detail=f"{r['entity_type']} no longer present", old_value=r["fingerprint"], new_value=None))
        elif r["fingerprint"] != r["fingerprint_new"]:
            for f, a, b in zip(r["fields_new"].split("|"), r["fingerprint"].split("|"), r["fingerprint_new"].split("|")):
                if a != b:
                    out.append(dict(base, change="changed", detail=f"{f.replace('_', ' ')}: {a or '-'} → {b or '-'}", old_value=a, new_value=b))
    return out


def history(recalls, labels, label_drugs, now):
    """Source-dated events: the sources say when these happened, so the feed has real history from the first build."""
    out = []
    for r in recalls.to_dicts():
        url = RECALL_URL.format(r["recall_number"])
        for change, day, what in (("reported", r["report_date"], "recall reported"), ("terminated", r["termination_date"], "recall terminated")):
            if day:
                out.append(dict(entity_type="recall", entity_key=r["recall_number"], change=change, display_name=r["display_name"],
                                ingredient_name=r["search_ingredient"], detail=f"{what} ({r['classification']})", old_value=None,
                                new_value=r["status"], event_date=day, found_by="source_date", detected_at=now, link_url=url))
    for r in labels.join(label_drugs, on="label_key", how="inner").to_dicts():
        if r["effective_date"]:
            out.append(dict(entity_type="label", entity_key=r["setid"], change="version_effective", display_name=r["display_name"],
                            ingredient_name=r["ingredient_name"], detail=f"label version {r['spl_version']} effective", old_value=None,
                            new_value=str(r["spl_version"]), event_date=r["effective_date"], found_by="source_date", detected_at=now,
                            link_url=r["dailymed_url"]))
    return out


SOURCE_OF = {"signal": "FAERS (quarterly files)", "recall": "openFDA drug enforcement", "label": "DailyMed SPL"}


def to_events(rows):
    if not rows:
        return pl.DataFrame(schema=EVENT_SCHEMA)
    df = pl.DataFrame(rows, infer_schema_length=None).with_columns(
        pl.col("entity_type").replace_strict(SOURCE_OF, default=None).alias("source"),
        pl.col("event_date").cast(pl.Utf8).str.slice(0, 10).str.to_date("%Y-%m-%d", strict=False))
    df = df.with_columns(pl.struct(["entity_type", "entity_key", "ingredient_name", "change", "detail", "event_date"]).map_elements(
        lambda s: event_id(*s.values()), return_dtype=pl.Utf8).alias("event_id"))
    return df.select(list(EVENT_SCHEMA)).cast(EVENT_SCHEMA)


@incremental(semantic_version=1, snapshot_inputs=["signals", "recalls", "labels", "drug_product", "product_label", "drugs"])
@transform.using(events_out=Output(CURATED + "ontology_change_events"), snap_out=Output(CURATED + "ontology_change_snapshot"),
                 signals=Input(CURATED + "ontology_signal_signals"), recalls=Input(CURATED + "ontology_recall_recalls"),
                 labels=Input(CURATED + "ontology_label_labels"), drug_product=Input(CURATED + "ontology_link_drug_product"),
                 product_label=Input(CURATED + "ontology_link_product_label"), drugs=Input(CURATED + "ontology_drug_drugs"))
def compute_changes(events_out, snap_out, signals, recalls, labels, drug_product, product_label, drugs):
    now = datetime.now(timezone.utc).isoformat()
    today = now[:10]
    label_drugs = (product_label.polars().join(drug_product.polars(), on="product_key").join(drugs.polars().select("ingredient_rxcui", "ingredient_name"),
                   on="ingredient_rxcui").select("label_key", "ingredient_name").unique())
    sig, rec, lab = signals.polars(), recalls.polars(), labels.polars()
    new = snapshot(sig, rec, lab, label_drugs)
    old = previous(snap_out)
    old_events = previous(events_out)
    if old is None or old_events is None:
        rows = history(rec, lab, label_drugs, now)  # first build: real history from source dates; no diff (nothing to compare)
        old_events = pl.DataFrame(schema=EVENT_SCHEMA)
    else:
        rows = diff(old.cast(SNAP_SCHEMA), new, today, now)
        # A recall or label that first appears now also gets its source-dated event.
        seen = set(old.filter(pl.col("entity_type") != "signal")["entity_key"].to_list())
        rows += [e for e in history(rec, lab, label_drugs, now) if e["entity_key"] not in seen]
    old_events = old_events.with_columns(pl.col("event_date").cast(pl.Utf8).str.slice(0, 10).str.to_date("%Y-%m-%d", strict=False))
    events = pl.concat([old_events.select(list(EVENT_SCHEMA)).cast(EVENT_SCHEMA), to_events(rows)]).unique("event_id", keep="first")
    events_out.set_mode("replace")
    snap_out.set_mode("replace")
    events_out.write_table(events.sort("event_date", descending=True, nulls_last=True))
    snap_out.write_table(new)


@transform.using(status_out=Output(CURATED + "ontology_source_status"), cases=Input(CLEAN + "clean_faers_cases_current"),
                 recalls=Input(CURATED + "ontology_recall_recalls"), labels=Input(CURATED + "ontology_label_labels"),
                 identity=Input(CLEAN + "clean_drug_identity"), rxnorm=Input(RAW + "raw_rxnorm_lookup"))
def compute_source_status(status_out, cases, recalls, labels, identity, rxnorm):
    # "As of" per source, shown on the screen next to each answer (D028): the newest date the source itself reports, and when we pulled it.
    c = cases.polars().select("quarter", "fda_dt")
    r, l = recalls.polars(), labels.polars()
    rx = identity.polars().filter(pl.col("rxnorm_version").is_not_null())
    rows = [
        {"source": "FAERS (quarterly files)", "answers": "Question 1: signals", "as_of": f"through {c['quarter'].max().upper()} (latest FDA receipt {c['fda_dt'].max()})",
         "refresh": "quarterly (FDA release)", "rows": c.height, "retrieved_at": "quarterly file (no pull time)"},
        {"source": "openFDA drug enforcement", "answers": "Question 2: recalls", "as_of": f"source updated {r['source_last_updated'].max()}; newest report {r['report_date'].max()}",
         "refresh": "weekly (FDA)", "rows": r.height, "retrieved_at": r["retrieved_at"].max()},
        {"source": "DailyMed SPL", "answers": "Question 1: label check", "as_of": f"newest label version effective {l['effective_date'].max()}",
         "refresh": "daily (NLM)", "rows": l.height, "retrieved_at": l["retrieved_at"].max()},
        {"source": "RxNorm", "answers": "drug identity", "as_of": f"RxNorm release {rx['rxnorm_version'].max() if rx.height else 'unknown'}",
         "refresh": "monthly (NLM)", "rows": rx.height, "retrieved_at": rxnorm.polars()["retrieved_at"].cast(pl.Utf8).max()},
    ]
    status_out.write_table(pl.DataFrame(rows, schema={"source": pl.Utf8, "answers": pl.Utf8, "as_of": pl.Utf8, "refresh": pl.Utf8,
                                                      "rows": pl.Int64, "retrieved_at": pl.Utf8}))
