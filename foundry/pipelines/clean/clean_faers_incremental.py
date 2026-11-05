# FAERS (silver), incremental (build-order step 10, A015): the same three outputs as clean_faers.py, but each build reads only
# the quarter files it has not processed yet and merges them into a kept state. Reading the ~690 MB of quarter files is the
# expensive part; the D023 fold needs every current case at once, so it is redone from the state each build (cheap).
# Rules are the same functions as clean_faers.py: D022 upsert + deletes, D020/D021 suspects, D023 fold.
#   - One new quarter per build, oldest first (MAX_NEW_QUARTERS): a backfill and a new FAERS release use the same path.
#   - If the drug identity changes (hash of clean_drug_identity), the state is rebuilt from every quarter ("replay").
#   - clean_faers_inc_log keeps one row per quarter processed: rows read, deletes, seconds, mode.
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/clean_faers_incremental.py
import hashlib
import time
from datetime import datetime, timezone

import polars as pl
from transforms.api import Input, Output, incremental, transform

try:
    from myproject.datasets.clean_faers import DEMO_COLS, finish, quarter_files, read_deletes, read_table, resolver, suspects
except ImportError:  # local run: the module sits next to this file
    import importlib.util, os
    _spec = importlib.util.spec_from_file_location("clean_faers", os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean_faers.py"))
    _mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
    DEMO_COLS, finish, quarter_files, read_deletes, read_table, resolver, suspects = (
        _mod.DEMO_COLS, _mod.finish, _mod.quarter_files, _mod.read_deletes, _mod.read_table, _mod.resolver, _mod.suspects)

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
MAX_NEW_QUARTERS = 1
LOG_SCHEMA = {"quarter": pl.Utf8, "generation": pl.Int64, "mode": pl.Utf8, "identity_hash": pl.Utf8, "built_at": pl.Utf8,
              "rows_demo": pl.Int64, "rows_drug_current": pl.Int64, "rows_reac_current": pl.Int64, "deletes": pl.Int64,
              "cases_replaced": pl.Int64, "cases_deleted": pl.Int64, "cases_after": pl.Int64, "seconds": pl.Float64}


def previous(out):
    try:
        return out.polars(mode="previous")
    except Exception:  # first build: no previous output
        return None


def identity_hash(identity):
    rows = identity.polars().filter(pl.col("matched")).select("lookup_string", "ingredient_rxcui").sort("lookup_string").rows()
    return hashlib.sha256(repr(rows).encode()).hexdigest()[:16]


def add_quarter(q, paths, fs, resolve, cases, susp, reac):
    """Merge one quarter into the state with the D022 rule; returns the new state and counts for the log."""
    demo = read_table(fs, paths["DEMO"], DEMO_COLS).unique("primaryid", keep="last", maintain_order=True).with_columns(
        pl.col("caseversion").cast(pl.Int64, strict=False).fill_null(0), pl.lit(q).alias("quarter"))
    before = set() if cases is None else set(cases["caseid"].to_list())
    merged = demo if cases is None else pl.concat([cases.drop("n_drug_rows"), demo])
    # Highest caseversion wins; ties go to the newer quarter (quarter strings sort in time order: 2025q4 < 2026q1).
    merged = merged.sort(["caseversion", "quarter"], maintain_order=True).unique("caseid", keep="last", maintain_order=True)
    deletes = read_deletes(fs, paths["DELETE"]) if "DELETE" in paths else set()
    merged = merged.filter(~pl.col("caseid").is_in(list(deletes)))
    now_here = merged.filter(pl.col("quarter") == q).select("primaryid", "caseid")
    drug = read_table(fs, paths["DRUG"], ["primaryid", "role_cod", "drugname", "prod_ai"]).join(now_here, on="primaryid")
    reac_q = read_table(fs, paths["REAC"], ["primaryid", "pt"]).join(now_here, on="primaryid").filter(pl.col("pt") != "").unique(["caseid", "pt"])
    n_q = drug.group_by("caseid").agg(pl.len().cast(pl.Int64).alias("n_drug_rows"))  # Int64: the kept state reads back as Int64
    susp_q = suspects(drug, resolve)
    # Cases still current from an earlier quarter keep their rows; replaced or deleted cases lose theirs.
    kept = merged.filter(pl.col("quarter") != q).select("caseid")
    if cases is None:
        n_all, susp, reac = n_q, susp_q, reac_q.select("caseid", "pt")
    else:
        n_all = pl.concat([cases.select("caseid", "n_drug_rows").join(kept, on="caseid", how="semi"), n_q])
        susp = pl.concat([susp.join(kept, on="caseid", how="semi"), susp_q])
        reac = pl.concat([reac.join(kept, on="caseid", how="semi"), reac_q.select("caseid", "pt")])
    new_cases = merged.join(n_all, on="caseid", how="left").with_columns(pl.col("n_drug_rows").fill_null(0).cast(pl.Int64))
    after = set(new_cases["caseid"].to_list())
    counts = {"rows_demo": demo.height, "rows_drug_current": drug.height, "rows_reac_current": reac_q.height, "deletes": len(deletes),
              "cases_replaced": len(before & set(now_here["caseid"].to_list())), "cases_deleted": len(before - after),
              "cases_after": new_cases.height}
    return new_cases, susp, reac, counts


@incremental(semantic_version=1, snapshot_inputs=["files", "identity"])
@transform.using(state_cases=Output(CLEAN + "clean_faers_inc_state_cases"), state_suspect=Output(CLEAN + "clean_faers_inc_state_suspects"),
                 state_reac=Output(CLEAN + "clean_faers_inc_state_reactions"), log=Output(CLEAN + "clean_faers_inc_log"),
                 files=Input(RAW + "raw_faers_quarter_files"), identity=Input(CLEAN + "clean_drug_identity"))
def compute_state(state_cases, state_suspect, state_reac, log, files, identity):
    fs, quarters = quarter_files(files)
    resolve = resolver(identity)
    id_hash = identity_hash(identity)
    old_log = previous(log)
    old_log = pl.DataFrame(schema=LOG_SCHEMA) if old_log is None else old_log.select(list(LOG_SCHEMA)).cast(LOG_SCHEMA)
    generation = old_log["generation"].max() if old_log.height else 0
    current = old_log.filter(pl.col("generation") == generation)
    replay = old_log.height > 0 and current["identity_hash"][-1] != id_hash
    if replay or old_log.height == 0:
        generation = (generation or 0) + 1
        cases = susp = reac = None
        done = set()
    else:
        cases, susp, reac = previous(state_cases), previous(state_suspect), previous(state_reac)
        done = set(current["quarter"].to_list())
    todo = [q for q in quarters if q not in done]
    # A replay rebuilds every quarter at once (the state must be whole); otherwise one new quarter per build, oldest first.
    todo = todo if replay else todo[:MAX_NEW_QUARTERS]
    rows = []
    for q in todo:
        t0 = time.time()
        cases, susp, reac, counts = add_quarter(q, quarters[q], fs, resolve, cases, susp, reac)
        rows.append({"quarter": q, "generation": generation, "mode": "replay" if replay else "incremental", "identity_hash": id_hash,
                     "built_at": datetime.now(timezone.utc).isoformat(), **counts, "seconds": round(time.time() - t0, 1)})
    for out in (state_cases, state_suspect, state_reac, log):
        out.set_mode("replace")
    if cases is not None:
        state_cases.write_table(cases)
        state_suspect.write_table(susp)
        state_reac.write_table(reac)
    log.write_table(pl.concat([old_log, pl.DataFrame(rows, schema=LOG_SCHEMA)]))


@transform.using(cases_out=Output(CLEAN + "clean_faers_inc_cases_current"), reactions_out=Output(CLEAN + "clean_faers_inc_case_reactions"),
                 drug_reaction_out=Output(CLEAN + "clean_faers_inc_drug_reaction"), state_cases=Input(CLEAN + "clean_faers_inc_state_cases"),
                 state_suspect=Input(CLEAN + "clean_faers_inc_state_suspects"), state_reac=Input(CLEAN + "clean_faers_inc_state_reactions"))
def compute_outputs(cases_out, reactions_out, drug_reaction_out, state_cases, state_suspect, state_reac):
    # Same shapes as clean_faers.py outputs, so the two can be compared row for row (step 10 gate) and swapped later.
    st = state_cases.polars()
    n_drugs = st.select("caseid", pl.col("n_drug_rows").cast(pl.UInt32))  # same type as the full rebuild's count
    cases, reactions, drug_reaction = finish(st.drop("n_drug_rows"), n_drugs, state_suspect.polars(), state_reac.polars())
    cases_out.write_table(cases)
    reactions_out.write_table(reactions)
    drug_reaction_out.write_table(drug_reaction)
