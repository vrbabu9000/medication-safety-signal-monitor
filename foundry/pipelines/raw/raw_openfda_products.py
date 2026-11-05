# Raw openFDA product bridges for the formulary: Drugs@FDA applications and NDC product listings.
# One row per source record per pull, payload kept whole. Full snapshot each build.
# Contract: docs/04-architecture/dataset-contracts-v1.md (raw_openfda_drugsfda, raw_openfda_ndc).
#
# Mirror of Foundry repo Pipelines/pipelines_raw_ingest,
#   transforms-python/src/myproject/datasets/raw_openfda_products.py
import json
from datetime import datetime, timezone
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from transforms.api import transform_df, Output
from transforms.external.systems import external_systems, Source

INGREDIENTS = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol", "semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]  # D018 formulary; widened at step 9 (D039 G1)
PAGE_SIZE = 1000
DRUGSFDA_FIELDS = ["application_number", "sponsor_name"]
NDC_FIELDS = ["product_ndc", "product_id", "application_number", "generic_name", "brand_name", "labeler_name", "marketing_category", "dosage_form", "product_type", "finished"]


def schema_for(fields):
    return StructType(
        [StructField("search_ingredient", StringType()), StructField("request_params", StringType()), StructField("http_status", IntegerType()), StructField("result_total", IntegerType()), StructField("source_last_updated", StringType()), StructField("retrieved_at", StringType())]
        + [StructField(f, StringType()) for f in fields]
        + [StructField("record_json", StringType()), StructField("error_text", StringType())]
    )


def as_text(value):
    return None if value is None else value if isinstance(value, str) else json.dumps(value)


def pull(source, endpoint, search_for, fields):
    # Pages through one openFDA endpoint per ingredient; a non-200 reply becomes an error row, never a silent gap.
    conn = source.get_https_connection()
    client = conn.get_client()
    url = conn.url.rstrip("/") + endpoint
    retrieved_at = datetime.now(timezone.utc).isoformat()
    rows = []
    for ingredient in INGREDIENTS:
        skip = 0
        while True:
            params = {"search": search_for(ingredient), "limit": PAGE_SIZE, "skip": skip}
            resp = client.get(url, params=params, timeout=60)
            if resp.status_code != 200:
                rows.append((ingredient, json.dumps(params), resp.status_code, None, None, retrieved_at) + (None,) * len(fields) + (None, resp.text[:2000]))
                break
            payload = resp.json()
            meta = payload.get("meta", {})
            total = meta.get("results", {}).get("total", 0)
            for rec in payload.get("results", []):
                rows.append((ingredient, json.dumps(params), 200, total, meta.get("last_updated"), retrieved_at) + tuple(as_text(rec.get(f)) for f in fields) + (json.dumps(rec), None))
            skip += PAGE_SIZE
            if skip >= total:
                break
    return rows


# Parentheses are required on OR searches (see DECISIONS learnings, 2026-11-04).
# Drugs@FDA: openfda.generic_name alone finds 47 of 141 oxycodone applications, so the ingredient field is included.
@external_systems(openfdaapi=Source("ri.magritte..source.e46a0898-be14-401d-92d1-f9c20afa7f94"))
@transform_df(Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_openfda_drugsfda"))
def compute_drugsfda(openfdaapi, ctx):
    rows = pull(openfdaapi, "/drug/drugsfda.json", lambda i: f'(openfda.generic_name:"{i}" products.active_ingredients.name:"{i}")', DRUGSFDA_FIELDS)
    return ctx.spark_session.createDataFrame(rows, schema_for(DRUGSFDA_FIELDS))


@external_systems(openfdaapi=Source("ri.magritte..source.e46a0898-be14-401d-92d1-f9c20afa7f94"))
@transform_df(Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_openfda_ndc"))
def compute_ndc(openfdaapi, ctx):
    rows = pull(openfdaapi, "/drug/ndc.json", lambda i: f'(generic_name:"{i}" active_ingredients.name:"{i}")', NDC_FIELDS)
    return ctx.spark_session.createDataFrame(rows, schema_for(NDC_FIELDS))
