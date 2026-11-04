# Label version -> product (application number), parsed from DailyMed SPL XML, with the reference label flagged per product.
# One row per (setid, version, application_number); a label with no approval id keeps one row with a reason (G4).
# Contract: docs/04-architecture/dataset-contracts-v1.md §2 (clean_label_product_map). Reference rule: D039 G3 / LD1 (owner's label, same route).
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/clean_label_product_map.py
import json
import re

import polars as pl
from transforms.api import Input, Output, transform

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
SUFFIXES = {"LLC", "INC", "LP", "LTD", "CORP", "CORPORATION", "CO", "COMPANY", "USA", "US"}


def org_words(name):
    words = re.sub(r"[^A-Z0-9 ]", " ", (name or "").upper()).split()
    return [w for w in words if w not in SUFFIXES]


def owner_match(labeler, sponsor):
    a, b = org_words(labeler), org_words(sponsor)
    if not a or not b:
        return None
    if a == b:
        return "exact"
    if a[0] == b[0]:
        return "first_word"
    return None


def first(pattern, text):
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else None


@transform.using(out=Output(CLEAN + "clean_label_product_map"), xml=Input(RAW + "raw_dailymed_spl_xml"), drugsfda=Input(RAW + "raw_openfda_drugsfda"))
def compute(out, xml, drugsfda):
    sponsors = {}
    for row in drugsfda.polars().filter(pl.col("http_status") == 200).to_dicts():
        sponsors[row["application_number"]] = row["sponsor_name"]
    rows = []
    for row in xml.polars().filter(pl.col("http_status") == 200).to_dicts():
        text = row["xml_text"]
        labeler = first(r"<representedOrganization>\s*<id[^>]*/>\s*<name>([^<]+)</name>", text)
        route = first(r'<routeCode[^>]*displayName="([^"]+)"', text)
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", first(r"<title>(.*?)</title>", text) or "")).strip()
        apps = sorted(set(re.findall(r'<approval>\s*<id extension="([^"]+)"', text)))
        base = {"setid": row["setid"], "spl_version": row["xml_version_number"], "effective_time": row["effective_time"], "title": title[:300], "labeler_name": labeler, "route": route}
        if not apps:
            rows.append({**base, "application_number": None, "in_drugsfda": False, "sponsor_name": None, "owner_match": None, "match_status": "no_approval_id"})
            continue
        for app in apps:
            sponsor = sponsors.get(app)
            match = owner_match(labeler, sponsor) if sponsor else None
            rows.append({**base, "application_number": app, "in_drugsfda": sponsor is not None, "sponsor_name": sponsor, "owner_match": match, "match_status": "matched" if sponsor else "application_not_in_drugsfda_pull"})
    df = pl.DataFrame(rows)
    # Reference label (LD1): the owner's label for the application, one per route; products with no owner label are flagged, not guessed.
    df = df.with_columns(is_reference_label=pl.col("owner_match").is_not_null())
    has_ref = df.group_by("application_number").agg(pl.col("is_reference_label").any().alias("product_has_owner_label"))
    out.write_table(df.join(has_ref, on="application_number", how="left"))
