# Access test: can Foundry call openFDA through src_openfda_api?
# Fetches 1 oxycodone recall (enforcement) record and stores the raw reply.
# Plumbing proof only, not pilot data.
#
# Mirror of Foundry repo Pipelines/pipelines_raw_ingest,
#   transforms-python/src/myproject/datasets/raw_openfda_enforcement_access_test.py
# Source: Data/raw/src_openfda_api (REST API, api.fda.gov:443, no auth, egress policy approved)
# First successful build: 2026-11-04, 1 row, HTTP 200 (recall D-0338-2026).
import json
from datetime import datetime, timezone
from pyspark.sql import Row
from transforms.api import transform_df, Output
from transforms.external.systems import external_systems, Source

ENDPOINT = "/drug/enforcement.json"
PARAMS = {"search": 'openfda.generic_name:"oxycodone"', "limit": 1}


@external_systems(openfdaapi=Source("ri.magritte..source.e46a0898-be14-401d-92d1-f9c20afa7f94"))
@transform_df(Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_openfda_enforcement_access_test"))
def compute(openfdaapi, ctx):
    conn = openfdaapi.get_https_connection()
    resp = conn.get_client().get(conn.url.rstrip("/") + ENDPOINT, params=PARAMS, timeout=30)
    body = json.dumps(resp.json()) if resp.ok else resp.text
    row = Row(retrieved_at_utc=datetime.now(timezone.utc).isoformat(), request_url=resp.url, http_status=resp.status_code, response_json=body)
    return ctx.spark_session.createDataFrame([row])
