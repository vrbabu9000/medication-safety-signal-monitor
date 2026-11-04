# Recalls (silver): one current row per recall, and every recall matched to packages / products / ingredients.
# Contract: docs/04-architecture/dataset-contracts-v1.md §2. Rules: NDCs come from the record's own text, not openfda.* (D037 learning);
# match method + confidence on every row; unmatched kept with a reason (G4). Change history (ChangeEvent) is step 10.
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/clean_recalls.py
import json
import re

import polars as pl
from transforms.api import Input, Output, transform

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
STATUSES = {"Ongoing", "Completed", "Terminated"}
# 3-segment NDC with dashes (any FDA shape), and NDC-keyword forms (10/11 digits, or 2-segment product code).
DASH3 = re.compile(r"(?<![\d-])(\d{4,5})-(\d{3,4})-(\d{1,2})(?![\d-])")
NDC_WORD = re.compile(r"NDC[\s#:.,No()]*", re.I)


def ymd(s):
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if s and len(s) == 8 and s.isdigit() else None


def norm3(a, b, c):
    shape = (len(a), len(b), len(c))
    return {(4, 4, 2): "0" + a + b + c, (5, 3, 2): a + "0" + b + c, (5, 4, 1): a + b + "0" + c, (5, 4, 2): a + b + c}.get(shape)


def norm_prod(a, b):
    return {(4, 4): "0" + a + b, (5, 3): a + "0" + b, (5, 4): a + b}.get((len(a), len(b)))


def extract_ndcs(text):
    # Returns (kind, printed, candidates): "package" with one 11-digit key, "package_10" with 3 possible keys, "product" with a 9-digit key.
    out, used = [], []
    for m in DASH3.finditer(text):
        key = norm3(*m.groups())
        if key:
            out.append(("package", m.group(0), [key]))
        used.append((m.start(), m.end()))
    for m in NDC_WORD.finditer(text):
        if any(s <= m.end() < e for s, e in used):
            continue
        rest = text[m.end():m.end() + 20]
        mm = re.match(r"(\d{10,11})(?!\d)", rest)
        if mm:
            s = mm.group(1)
            out.append(("package", s, [s]) if len(s) == 11 else ("package_10", s, ["0" + s, s[:5] + "0" + s[5:], s[:9] + "0" + s[9]]))
            continue
        mm = re.match(r"(\d{4,5})-(\d{3,4})(?![\d-])", rest)
        if mm and norm_prod(*mm.groups()):
            out.append(("product", mm.group(0), [norm_prod(*mm.groups())]))
    return out


@transform.using(out=Output(CLEAN + "clean_recalls_current"), enforcement=Input(RAW + "raw_openfda_enforcement"))
def compute_recalls_current(out, enforcement):
    # Latest pull wins: the raw dataset is a full snapshot, so one row per recall_number after dropping repeats across searches.
    rows, seen = [], set()
    for r in enforcement.polars().filter(pl.col("http_status") == 200).sort("retrieved_at", descending=True).to_dicts():
        if r["recall_number"] in seen:
            continue
        seen.add(r["recall_number"])
        rec = json.loads(r["record_json"])
        text = " ".join([rec.get("product_description") or "", rec.get("code_info") or ""])
        rows.append({
            "recall_number": r["recall_number"], "event_id": rec.get("event_id"), "status": rec.get("status"),
            "status_valid": rec.get("status") in STATUSES, "is_active": rec.get("status") == "Ongoing",
            "classification": rec.get("classification"), "product_type": rec.get("product_type"),
            "recalling_firm": rec.get("recalling_firm"), "product_description": rec.get("product_description"),
            "reason_for_recall": rec.get("reason_for_recall"), "code_info": rec.get("code_info"),
            "product_quantity": rec.get("product_quantity"), "distribution_pattern": rec.get("distribution_pattern"),
            "voluntary_mandated": rec.get("voluntary_mandated"),
            "recall_initiation_date": ymd(rec.get("recall_initiation_date")), "center_classification_date": ymd(rec.get("center_classification_date")),
            "report_date": ymd(rec.get("report_date")), "termination_date": ymd(rec.get("termination_date")),
            "n_ndcs_in_text": len(extract_ndcs(text)), "search_ingredient": r["search_ingredient"],
            "source_last_updated": r["source_last_updated"], "retrieved_at": r["retrieved_at"],
        })
    out.write_table(pl.DataFrame(rows, infer_schema_length=None))


@transform.using(out=Output(CLEAN + "clean_recall_product_match"), recalls=Input(CLEAN + "clean_recalls_current"), packages=Input(CLEAN + "clean_drug_package_map"), ingredients=Input(CLEAN + "clean_drug_ingredients"))
def compute_recall_product_match(out, recalls, packages, ingredients):
    pkgs = {p["package_ndc11"]: p for p in packages.polars().to_dicts()}
    by_prod9 = {}
    for p in pkgs.values():
        a, b = (p["product_ndc"] or "-").split("-", 1)
        by_prod9.setdefault(norm_prod(a, b), set()).add(p["product_key"])
    names = [(i["ingredient_rxcui"], re.compile(r"\b" + re.escape(i["ingredient_name"]) + r"\b", re.I)) for i in ingredients.polars().to_dicts()]
    rows = []

    def add(rec, target, key, method, confidence, printed=None, product_key=None, reason=None):
        rows.append({"recall_number": rec["recall_number"], "match_target": target, "match_key": key, "match_method": method,
                     "confidence": confidence, "ndc_as_printed": printed, "product_key": product_key, "unmatched_reason": reason,
                     "is_active": rec["is_active"], "classification": rec["classification"]})

    for rec in recalls.polars().to_dicts():
        # Ingredient row for every recall that names a formulary ingredient (so the drug page shows it even with no NDC).
        for rxcui, rx in names:
            if rx.search(rec["product_description"] or ""):
                add(rec, "ingredient", rxcui, "ingredient_name_in_text", "low")
        found = extract_ndcs(" ".join([rec["product_description"] or "", rec["code_info"] or ""]))
        if not found:
            add(rec, "none", "-", "no_ndc_in_text", "none", reason="no_ndc_in_text")
        done = set()
        for kind, printed, cands in found:
            if kind == "product":
                keys = by_prod9.get(cands[0], set())
                for pk in sorted(keys):
                    if ("product", pk) not in done:
                        done.add(("product", pk))
                        add(rec, "product", pk, "product_ndc_in_text", "medium", printed, pk)
                if not keys and ("product_ndc", cands[0]) not in done:
                    done.add(("product_ndc", cands[0]))
                    add(rec, "product_ndc", cands[0], "product_ndc_in_text", "none", printed, reason="ndc_not_in_ndc_directory")
                continue
            hits = [c for c in cands if c in pkgs]
            key = hits[0] if len(hits) == 1 else cands[0] if kind == "package" else None
            if key is None or ("package", key) in done:
                if key is None and ("package", printed) not in done:
                    done.add(("package", printed))
                    add(rec, "package", printed, "ndc_10digit_ambiguous", "none", printed, reason="ambiguous_10_digit_ndc")
                continue
            done.add(("package", key))
            if key in pkgs:
                add(rec, "package", key, "ndc_in_text" if kind == "package" else "ndc_10digit_resolved", "high" if kind == "package" else "medium", printed, pkgs[key]["product_key"])
            else:
                add(rec, "package", key, "ndc_in_text", "none", printed, reason="ndc_not_in_ndc_directory")
    out.write_table(pl.DataFrame(rows, infer_schema_length=None))
