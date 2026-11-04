# FAERS (silver): current case versions, every case's reactions (PRR background), and formulary suspect drug x reaction rows.
# Contract: docs/04-architecture/dataset-contracts-v1.md §2. Rules: D022 (upsert by caseid, max caseversion, then that quarter's
# deletes), D021 (suspect = PS + SS + I, each ingredient once per case), D023 (cross-case duplicate fold: flagged, not dropped),
# D020 (drug strings resolved through clean_drug_identity; exact after salt strip, never substring).
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/clean_faers.py
import io
import re

import polars as pl
from transforms.api import Input, Output, transform

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
SUSPECT_ROLES = ["PS", "SS", "I"]
FOLD_MIN_DRUGS, FOLD_MIN_REPORTS = 30, 50  # D023
SALTS = ["HYDROCHLORIDE", "HCL", "BITARTRATE", "TARTRATE", "SULFATE", "CITRATE", "PHOSPHATE", "MYRISTATE", "TEREPHTHALATE", "ACETATE", "MESYLATE", "SODIUM", "MALEATE", "BROMIDE"]
DEMO_COLS = ["primaryid", "caseid", "caseversion", "i_f_code", "event_dt", "init_fda_dt", "fda_dt", "rept_cod", "age", "age_cod", "sex", "occp_cod", "occr_country"]


def norm(name):
    return re.sub(r"\s+", " ", (name or "").upper()).strip()


def strip_salt(name):
    words = norm(name).split(" ")
    while len(words) > 1 and words[-1] in SALTS:
        words.pop()
    return " ".join(words)


def quarter_files(files):
    # {quarter: {"DEMO": path, "DRUG": path, "REAC": path, "DELETE": path}} from paths like 2026q1/ASCII/DEMO26Q1.txt
    fs = files.filesystem()
    out = {}
    for f in fs.ls():
        m = re.match(r"(\d{4}q\d)/.*?/(DEMO|DRUG|REAC|DELETE)\d\dQ\d\.txt$", f.path, re.I)
        if m:
            out.setdefault(m.group(1).lower(), {})[m.group(2).upper()] = f.path
    return fs, dict(sorted(out.items()))


def read_table(fs, path, cols):
    # '$'-separated, no quoting, latin-1 text; read as strings, keep only the columns we use.
    with fs.open(path, "rb") as f:
        data = f.read()
    df = pl.read_csv(io.BytesIO(data), separator="$", quote_char=None, infer_schema=False, encoding="utf8-lossy", truncate_ragged_lines=True)
    df = df.rename({c: c.strip().lower() for c in df.columns})
    return df.select([pl.col(c).str.strip_chars().fill_null("").alias(c) for c in cols])


def read_deletes(fs, path):
    with fs.open(path, "rb") as f:
        return {line.strip() for line in f.read().decode("latin-1").splitlines() if line.strip()}


def resolver(identity):
    names = {r["lookup_string"]: r["ingredient_rxcui"] for r in identity.polars().filter(pl.col("matched")).to_dicts()}

    def resolve(s):
        s = norm(s)
        if s in names:
            return names[s], "identity_exact"
        if strip_salt(s) in names:
            return names[strip_salt(s)], "salt_stripped"
        return None, None
    return resolve


@transform.using(cases_out=Output(CLEAN + "clean_faers_cases_current"), reactions_out=Output(CLEAN + "clean_faers_case_reactions"),
                 drug_reaction_out=Output(CLEAN + "clean_faers_drug_reaction"), files=Input(RAW + "raw_faers_quarter_files"),
                 identity=Input(CLEAN + "clean_drug_identity"))
def compute_faers(cases_out, reactions_out, drug_reaction_out, files, identity):
    fs, quarters = quarter_files(files)
    resolve = resolver(identity)

    # D022: upsert each quarter in order (highest caseversion wins; ties go to the newer quarter), then apply its deletes.
    state = None
    for order, (q, paths) in enumerate(quarters.items()):
        demo = read_table(fs, paths["DEMO"], DEMO_COLS).unique("primaryid", keep="last", maintain_order=True).with_columns(
            pl.col("caseversion").cast(pl.Int64, strict=False).fill_null(0), pl.lit(q).alias("quarter"), pl.lit(order).alias("q_order"))
        state = demo if state is None else pl.concat([state, demo])
        state = state.sort(["caseversion", "q_order"], maintain_order=True).unique("caseid", keep="last", maintain_order=True)
        if "DELETE" in paths:
            state = state.filter(~pl.col("caseid").is_in(list(read_deletes(fs, paths["DELETE"]))))

    # Drug and reaction rows, only for the report (primaryid) that is current for each case.
    drugs, reacs = [], []
    for q, paths in quarters.items():
        keep = state.filter(pl.col("quarter") == q).select("primaryid", "caseid")
        drugs.append(read_table(fs, paths["DRUG"], ["primaryid", "role_cod", "drugname", "prod_ai"]).join(keep, on="primaryid"))
        reacs.append(read_table(fs, paths["REAC"], ["primaryid", "pt"]).join(keep, on="primaryid"))
    drug = pl.concat(drugs)
    reac = pl.concat(reacs).filter(pl.col("pt") != "").unique(["caseid", "pt"])

    # D020: split prod_ai on '\', resolve each part; if prod_ai is blank fall back to the whole drugname (same exact rules).
    parts = drug.with_columns(pl.when(pl.col("prod_ai") != "").then(pl.col("prod_ai").str.split("\\")).otherwise(pl.concat_list([pl.col("drugname")])).alias("part"),
                              (pl.col("prod_ai") == "").alias("via_drugname")).explode("part")
    lookup = {s: resolve(s) for s in parts["part"].unique().to_list()}
    lk = pl.DataFrame({"part": list(lookup), "ingredient_rxcui": [v[0] for v in lookup.values()], "method": [v[1] for v in lookup.values()]},
                      schema={"part": pl.Utf8, "ingredient_rxcui": pl.Utf8, "method": pl.Utf8})
    resolved = parts.join(lk, on="part", how="left").filter(pl.col("ingredient_rxcui").is_not_null()).with_columns(
        pl.when(pl.col("via_drugname")).then(pl.lit("drugname_") + pl.col("method")).otherwise(pl.col("method")).alias("method"))
    # D021: suspect roles only, each ingredient once per case; concomitant (C) never counts.
    suspect = resolved.filter(pl.col("role_cod").is_in(SUSPECT_ROLES)).group_by(["caseid", "ingredient_rxcui"]).agg(
        pl.col("role_cod").unique().sort().str.join("+").alias("roles"), pl.col("method").min().alias("ingredient_match"))

    # D023: one person filed again and again under different caseids. Flag the cluster, keep the latest filing un-suppressed.
    n_drugs = drug.group_by("caseid").agg(pl.len().alias("n_drug_rows"))
    cases = state.join(n_drugs, on="caseid", how="left").with_columns(pl.col("n_drug_rows").fill_null(0)).with_columns(
        pl.concat_str(["age", "age_cod", "sex", "occr_country", "event_dt"], separator="|").alias("person_key"))
    eligible = (pl.col("n_drug_rows") >= FOLD_MIN_DRUGS) & (pl.col("age") != "")
    cases = cases.with_columns(pl.when(eligible).then(pl.len().over(pl.when(eligible).then(pl.col("person_key")))).otherwise(0).alias("person_key_reports"))
    cases = cases.with_columns((pl.col("person_key_reports") >= FOLD_MIN_REPORTS).alias("dup_cluster"))
    keeper = cases.filter(pl.col("dup_cluster")).sort(["fda_dt", "caseid"]).group_by("person_key").agg(pl.col("caseid").last().alias("keeper"))
    cases = cases.join(keeper, on="person_key", how="left").with_columns(
        (pl.col("dup_cluster") & (pl.col("caseid") != pl.col("keeper"))).alias("dup_suppressed")).drop(["keeper", "q_order"])
    n_susp = suspect.group_by("caseid").agg(pl.len().alias("n_formulary_suspects"))
    cases = cases.join(n_susp, on="caseid", how="left").with_columns(pl.col("n_formulary_suspects").fill_null(0))

    cases = cases.with_columns(pl.col("fda_dt").str.strptime(pl.Date, "%Y%m%d", strict=False).alias("fda_date"))
    flags = cases.select("caseid", "quarter", "fda_date", "dup_suppressed")
    cases_out.write_table(cases)
    reactions_out.write_table(reac.select("caseid", "pt").join(flags, on="caseid"))
    drug_reaction_out.write_table(suspect.join(reac.select("caseid", "pt"), on="caseid").join(flags, on="caseid")
                                  .select("caseid", "ingredient_rxcui", "pt", "roles", "ingredient_match", "quarter", "fda_date", "dup_suppressed"))
