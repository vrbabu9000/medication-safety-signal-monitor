# Raw openFDA drug recalls (enforcement): one row per recall record per pull, payload kept whole.
# Contract: docs/04-architecture/dataset-contracts-v1.md (raw_openfda_enforcement). Full snapshot each build.
#
# Mirror of Foundry repo Pipelines/pipelines_raw_ingest,
#   transforms-python/src/myproject/datasets/raw_openfda_enforcement.py
import json
from datetime import datetime, timezone
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from transforms.api import transform_df, Output
from transforms.external.systems import external_systems, Source

ENDPOINT = "/drug/enforcement.json"
INGREDIENTS = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol", "semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]  # D018 formulary; widened at step 9 (D039 G1)
PAGE_SIZE = 1000
FIELDS = ["recall_number", "event_id", "status", "classification", "report_date", "recall_initiation_date", "termination_date"]
SCHEMA = StructType(
    [StructField("search_ingredient", StringType()), StructField("request_params", StringType()), StructField("http_status", IntegerType()), StructField("result_total", IntegerType()), StructField("source_last_updated", StringType()), StructField("retrieved_at", StringType())]
    + [StructField(f, StringType()) for f in FIELDS]
    + [StructField("record_json", StringType()), StructField("error_text", StringType())]
)


def search_for(ingredient):
    # Parentheses are required: without them openFDA silently drops the first OR term (oxycodone 11 vs 25).
    return f'(product_description:"{ingredient}" openfda.generic_name:"{ingredient}")'


@external_systems(openfdaapi=Source("ri.magritte..source.e46a0898-be14-401d-92d1-f9c20afa7f94"))
@transform_df(Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_openfda_enforcement"))
def compute(openfdaapi, ctx):
    conn = openfdaapi.get_https_connection()
    client = conn.get_client()
    url = conn.url.rstrip("/") + ENDPOINT
    retrieved_at = datetime.now(timezone.utc).isoformat()
    rows = []
    for ingredient in INGREDIENTS:
        skip = 0
        while True:
            params = {"search": search_for(ingredient), "limit": PAGE_SIZE, "skip": skip}
            resp = client.get(url, params=params, timeout=60)
            if resp.status_code != 200:
                rows.append((ingredient, json.dumps(params), resp.status_code, None, None, retrieved_at) + (None,) * len(FIELDS) + (None, resp.text[:2000]))
                break
            payload = resp.json()
            meta = payload.get("meta", {})
            total = meta.get("results", {}).get("total", 0)
            for rec in payload.get("results", []):
                rows.append((ingredient, json.dumps(params), 200, total, meta.get("last_updated"), retrieved_at) + tuple(rec.get(f) for f in FIELDS) + (json.dumps(rec), None))
            skip += PAGE_SIZE
            if skip >= total:
                break
    return ctx.spark_session.createDataFrame(rows, SCHEMA)
