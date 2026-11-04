# Raw RxNorm identity for the formulary (RxNav REST): exact-name lookups and every concept related to each ingredient.
# One row per looked-up string, and one row per (ingredient, related concept). Stamped with the RxNorm version. Full snapshot each build.
# Contract: docs/04-architecture/dataset-contracts-v1.md (raw_rxnorm_lookup, raw_rxnorm_related).
#
# Mirror of Foundry repo Pipelines/pipelines_raw_ingest,
#   transforms-python/src/myproject/datasets/raw_rxnorm.py
import json
from datetime import datetime, timezone
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from transforms.api import transform, Output
from transforms.external.systems import external_systems, Source

API = "/REST"
INGREDIENTS = ["oxycodone"]
# Salt forms are looked up too, so the clean layer can show why exact ingredient matching strips salts (D020).
EXTRA_STRINGS = ["oxycodone hydrochloride"]
LOOKUP_SCHEMA = StructType([StructField(c, IntegerType() if c in ("http_status", "rxcui_count") else StringType()) for c in ["lookup_string", "rxnorm_version", "api_version", "request_params", "http_status", "rxcui_list", "rxcui_count", "retrieved_at", "record_json", "error_text"]])
RELATED_SCHEMA = StructType([StructField(c, IntegerType() if c == "http_status" else StringType()) for c in ["ingredient_rxcui", "rxnorm_version", "tty", "rxcui", "name", "synonym", "suppress", "http_status", "retrieved_at", "error_text"]])


@external_systems(rxnavapi=Source("ri.magritte..source.79ca01f9-95d0-43c6-8e28-cc9681a2ed5f"))
@transform(lookup_out=Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_rxnorm_lookup"), related_out=Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_rxnorm_related"))
def compute(rxnavapi, ctx, lookup_out, related_out):
    conn = rxnavapi.get_https_connection()
    client = conn.get_client()
    base = conn.url.rstrip("/") + API
    retrieved_at = datetime.now(timezone.utc).isoformat()
    version = client.get(base + "/version.json", timeout=60).json()
    rxnorm_version, api_version = version.get("version"), version.get("apiVersion")
    lookup_rows, related_rows, ingredient_ids = [], [], []
    for name in INGREDIENTS + EXTRA_STRINGS:
        params = {"name": name, "search": 0}
        resp = client.get(base + "/rxcui.json", params=params, timeout=60)
        if resp.status_code != 200:
            lookup_rows.append((name, rxnorm_version, api_version, json.dumps(params), resp.status_code, None, None, retrieved_at, None, resp.text[:2000]))
            continue
        payload = resp.json()
        ids = payload.get("idGroup", {}).get("rxnormId", [])
        lookup_rows.append((name, rxnorm_version, api_version, json.dumps(params), 200, json.dumps(ids), len(ids), retrieved_at, json.dumps(payload), None))
        if name in INGREDIENTS:
            ingredient_ids.extend(ids)
    for rxcui in ingredient_ids:
        resp = client.get(f"{base}/rxcui/{rxcui}/allrelated.json", timeout=60)
        if resp.status_code != 200:
            related_rows.append((rxcui, rxnorm_version, None, None, None, None, None, resp.status_code, retrieved_at, resp.text[:2000]))
            continue
        for group in resp.json().get("allRelatedGroup", {}).get("conceptGroup", []):
            for c in group.get("conceptProperties") or []:
                related_rows.append((rxcui, rxnorm_version, c.get("tty"), c.get("rxcui"), c.get("name"), c.get("synonym"), c.get("suppress"), 200, retrieved_at, None))
    lookup_out.write_dataframe(ctx.spark_session.createDataFrame(lookup_rows, LOOKUP_SCHEMA))
    related_out.write_dataframe(ctx.spark_session.createDataFrame(related_rows, RELATED_SCHEMA))
