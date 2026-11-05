"""Find label wording that may mean the same as a FAERS term, for human review (label <-> FAERS synonym table, A014).

    .venv/bin/python foundry/tools/local_run/synonym_candidates.py [out_dir]

Input: the local pipeline outputs in out/ (ontology_ae_stats, clean_label_sections, ontology_product_products,
ontology_link_drug_product). For every statistically flagged, clinical FAERS term that the exact label check did NOT find,
it looks in the same drug's reference-label safety sections for sentences that share word stems with the term.
Output: eval/synonyms/candidates-v1.jsonl (~5 MB, not committed), one row per (FAERS term, sentence), with the drugs it came from.
The committed review sheet is eval/synonyms/leads-v1.txt (one line per term, short matching phrases).
A candidate is only a lead: a person decides the band (high / medium / rejected) in label_synonyms.py.
"""
import json
import os
import re
import sys
from collections import defaultdict

import polars as pl

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "foundry/tools/local_run/out")
DEST = os.path.join(ROOT, "eval/synonyms/candidates-v1.jsonl")
# Words that say little on their own; a match on these alone is not a lead.
STOP = {"disorder", "syndrome", "increased", "decreased", "abnormal", "increase", "decrease", "level", "levels", "test", "positive",
        "negative", "acute", "chronic", "severe", "nos", "condition", "aggravated", "general", "other", "site", "drug", "product",
        "with", "without", "the", "and", "from", "type", "count", "blood", "disease", "failure", "injury", "pain", "infection",
        "system", "function", "reaction", "symptom", "symptoms", "body", "total", "normal", "low", "high"}
_US = [("oesophag", "esophag"), ("oedema", "edema"), ("diarrhoea", "diarrhea"), ("haem", "hem"), ("anaem", "anem"), ("aemia", "emia"),
       ("oestr", "estr"), ("foet", "fet"), ("paed", "ped"), ("isation", "ization"), ("leukaem", "leukem"), ("tumour", "tumor"),
       ("behaviour", "behavior"), ("ae", "e")]


def us(s):
    s = s.lower()
    for gb, am in _US:
        s = s.replace(gb, am)
    return s


def stems(term):
    return sorted({w[:5] for w in re.findall(r"[a-z]+", us(term)) if len(w) >= 4 and w not in STOP})


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.;])\s+", text or "") if 20 <= len(s.strip()) <= 600]


def main():
    stats = pl.read_ndjson(f"{OUT}/ontology_ae_stats.jsonl", infer_schema_length=None)
    todo = stats.filter(pl.col("meets_evans") & (pl.col("label_status") == "not_in_label") & (pl.col("bucket") == "clinical"))
    prods = pl.read_ndjson(f"{OUT}/ontology_product_products.jsonl", infer_schema_length=None).select("product_key", "reference_label_key")
    link = pl.read_ndjson(f"{OUT}/ontology_link_drug_product.jsonl", infer_schema_length=None).select("ingredient_rxcui", "product_key")
    secs = pl.read_ndjson(f"{OUT}/clean_label_sections.jsonl", infer_schema_length=None).with_columns(
        pl.concat_str([pl.col("setid"), pl.lit("|v"), pl.col("spl_version").cast(pl.Utf8)]).alias("label_key"))
    ref = link.join(prods, on="product_key").drop_nulls("reference_label_key").select("ingredient_rxcui", "reference_label_key").unique()
    j = ref.join(secs.select("label_key", "section_name", "section_text"), left_on="reference_label_key", right_on="label_key")
    sent_by_drug = defaultdict(list)  # rxcui -> [(label_key, section, sentence, us(sentence))]
    for r in j.iter_rows(named=True):
        for s in sentences(r["section_text"]):
            sent_by_drug[r["ingredient_rxcui"]].append((r["reference_label_key"], r["section_name"], s, us(s)))

    found = {}  # (pt, sentence) -> row
    for r in todo.iter_rows(named=True):
        st = stems(r["pt"])
        if not st:
            continue
        for lab, sec, s, su in sent_by_drug.get(r["ingredient_rxcui"], []):
            hit = [x for x in st if re.search(r"\b" + x, su)]
            # Lead = all stems of a one- or two-stem term, or at least two stems of a longer term.
            if len(hit) < min(len(st), 2):
                continue
            key = (r["pt"], s)
            row = found.setdefault(key, {"pt": r["pt"], "stems": st, "stems_hit": hit, "sentence": s, "section": sec,
                                         "label_key": lab, "drugs": [], "a_total": 0})
            if r["ingredient_name"] not in row["drugs"]:
                row["drugs"].append(r["ingredient_name"])
                row["a_total"] += r["a_drug_reaction"]
    rows = sorted(found.values(), key=lambda x: (-x["a_total"], x["pt"], len(x["sentence"])))
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    print(f"{todo.height} flagged clinical terms not in label; {len({r['pt'] for r in rows})} terms have a lead; {len(rows)} sentences -> {DEST}")


if __name__ == "__main__":
    main()
