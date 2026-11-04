# Shared drug identity (silver), resolved once: formulary ingredients, drug-string -> ingredient, ingredient <-> product, package -> product.
# Contract: docs/04-architecture/dataset-contracts-v1.md §2. Rules: D020 (exact match after salt strip, never substring),
# D027/D039 G2 (product = application number), D-R6 (no application number -> labeler:product key, tagged), G4 (unmatched kept with a reason).
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/clean_drug_identity.py
import json
import re

import polars as pl
from transforms.api import Input, Output, transform

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
# D018 formulary (13 ingredient RxCUIs). in_slice = pulled into raw today (D039 G1: widen after the oxycodone slice works).
FORMULARY = [
    ("4337", "fentanyl", "opioid", False), ("7052", "morphine", "opioid", False), ("3423", "hydromorphone", "opioid", False),
    ("7804", "oxycodone", "opioid", True), ("5489", "hydrocodone", "opioid", False), ("6813", "methadone", "opioid", False),
    ("1819", "buprenorphine", "opioid", False), ("10689", "tramadol", "opioid", False), ("1991302", "semaglutide", "glp1", False),
    ("2601723", "tirzepatide", "glp1", False), ("475968", "liraglutide", "glp1", False), ("1551291", "dulaglutide", "glp1", False),
    ("60548", "exenatide", "glp1", False),
]
SALTS = ["HYDROCHLORIDE", "HCL", "BITARTRATE", "TARTRATE", "SULFATE", "CITRATE", "PHOSPHATE", "MYRISTATE", "TEREPHTHALATE", "ACETATE", "MESYLATE", "SODIUM", "MALEATE", "BROMIDE"]


def norm(name):
    return re.sub(r"\s+", " ", (name or "").upper()).strip()


def strip_salt(name):
    words = norm(name).split(" ")
    while len(words) > 1 and words[-1] in SALTS:
        words.pop()
    return " ".join(words)


def records(dataset):
    return dataset.polars().filter(pl.col("http_status") == 200).to_dicts()


def ingredient_names(rec):
    return [norm(a.get("name")) for a in rec.get("active_ingredients") or [] if a.get("name")]


def resolver(related):
    # RxNorm names for each formulary ingredient: IN (ingredient) and PIN (precise ingredient, i.e. salt form).
    names = {}
    for r in related:
        if r["tty"] in ("IN", "PIN"):
            names[norm(r["name"])] = (r["ingredient_rxcui"], "exact_" + r["tty"].lower(), r["rxnorm_version"])

    def resolve(s):
        if s in names:
            return names[s]
        base = strip_salt(s)
        if base in names:
            rxcui, _, version = names[base]
            return rxcui, "salt_stripped", version
        return None, "no_formulary_match", None
    return resolve


def ndc11(code):
    # 4-4-2 -> pad labeler, 5-3-2 -> pad product, 5-4-1 -> pad package; anything else is left for review.
    parts = (code or "").split("-")
    if len(parts) != 3:
        return None
    widths = [len(p) for p in parts]
    pad = {(4, 4, 2): 0, (5, 3, 2): 1, (5, 4, 1): 2}.get(tuple(widths))
    if pad is None:
        return None
    parts[pad] = "0" + parts[pad]
    return "".join(parts)


@transform.using(out=Output(CLEAN + "clean_drug_ingredients"))
def compute_ingredients(out):
    out.write_table(pl.DataFrame(FORMULARY, schema=["ingredient_rxcui", "ingredient_name", "drug_class", "in_slice"], orient="row"))


@transform.using(out=Output(CLEAN + "clean_drug_identity"), related=Input(RAW + "raw_rxnorm_related"), drugsfda=Input(RAW + "raw_openfda_drugsfda"), ndc=Input(RAW + "raw_openfda_ndc"))
def compute_identity(out, related, drugsfda, ndc):
    resolve = resolver(records(related))
    seen = {}
    for source, recs in (("drugsfda", records(drugsfda)), ("ndc", records(ndc))):
        for row in recs:
            rec = json.loads(row["record_json"])
            products = rec.get("products") if source == "drugsfda" else [rec]
            for p in products:
                for s in ingredient_names(p):
                    seen.setdefault(s, {"drugsfda": 0, "ndc": 0})[source] += 1
    rows = []
    for s, counts in sorted(seen.items()):
        rxcui, method, version = resolve(s)
        rows.append({"lookup_string": s, "ingredient_rxcui": rxcui, "matched": rxcui is not None, "match_method": method, "rxnorm_version": version, "n_drugsfda_products": counts["drugsfda"], "n_ndc_products": counts["ndc"]})
    out.write_table(pl.DataFrame(rows))


@transform.using(out=Output(CLEAN + "clean_drug_product_map"), related=Input(RAW + "raw_rxnorm_related"), drugsfda=Input(RAW + "raw_openfda_drugsfda"))
def compute_product_map(out, related, drugsfda):
    resolve = resolver(records(related))
    groups = {}
    for row in records(drugsfda):
        rec = json.loads(row["record_json"])
        for p in rec.get("products") or []:
            names = ingredient_names(p)
            for s in names:
                rxcui = resolve(s)[0]
                if rxcui is None:
                    continue
                g = groups.setdefault((rxcui, rec["application_number"]), {"sponsor_name": rec.get("sponsor_name"), "products": []})
                g["products"].append({"product_number": p.get("product_number"), "brand_name": p.get("brand_name"), "dosage_form": p.get("dosage_form"), "route": p.get("route"), "marketing_status": p.get("marketing_status"), "n_ingredients": len(names)})
    rows = []
    for (rxcui, app), g in sorted(groups.items()):
        ps = g["products"]
        rows.append({
            "ingredient_rxcui": rxcui, "product_key": app, "product_key_type": "application_number", "application_type": re.sub(r"\d", "", app),
            "sponsor_name": g["sponsor_name"], "n_products": len(ps), "is_combination": any(p["n_ingredients"] > 1 for p in ps),
            "brand_names": "; ".join(sorted({p["brand_name"] or "" for p in ps})), "dosage_forms": "; ".join(sorted({p["dosage_form"] or "" for p in ps})),
            "routes": "; ".join(sorted({p["route"] or "" for p in ps})), "any_marketed": any((p["marketing_status"] or "").startswith("Prescription") or p["marketing_status"] == "Over-the-counter" for p in ps),
            "products_json": json.dumps(ps),
        })
    out.write_table(pl.DataFrame(rows))


@transform.using(out=Output(CLEAN + "clean_drug_package_map"), related=Input(RAW + "raw_rxnorm_related"), ndc=Input(RAW + "raw_openfda_ndc"))
def compute_package_map(out, related, ndc):
    resolve = resolver(records(related))
    rows = []
    for row in records(ndc):
        rec = json.loads(row["record_json"])
        rxcuis = sorted({r for r in (resolve(s)[0] for s in ingredient_names(rec)) if r})
        app = rec.get("application_number")
        for pkg in rec.get("packaging") or []:
            rows.append({
                "package_ndc11": ndc11(pkg.get("package_ndc")), "package_ndc_printed": pkg.get("package_ndc"), "product_ndc": rec.get("product_ndc"),
                "product_id": rec.get("product_id"), "product_key": app or "labeler:" + (rec.get("product_ndc") or ""),
                "product_key_type": "application_number" if app else "labeler_product", "marketing_category": rec.get("marketing_category"),
                "is_finished": rec.get("finished"), "brand_name": rec.get("brand_name"), "labeler_name": rec.get("labeler_name"),
                "ingredient_rxcuis": "; ".join(rxcuis), "package_description": pkg.get("description"),
                "marketing_end_date": pkg.get("marketing_end_date"), "listing_expiration_date": rec.get("listing_expiration_date"),
            })
    out.write_table(pl.DataFrame(rows))
