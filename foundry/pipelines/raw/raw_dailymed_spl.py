# Raw DailyMed labels (SPL) for the formulary: the label index and each label's current XML, kept whole.
# One row per (setid, version) seen in the index, and one row per XML document. Full snapshot each build, but an XML already
# fetched for the same setid + version is reused from the previous output instead of downloaded again (O3: ~1,300 downloads
# per build become the handful of new label versions).
# Contract: docs/04-architecture/dataset-contracts-v1.md (raw_dailymed_spl_index, raw_dailymed_spl_xml).
#
# Mirror of Foundry repo Pipelines/pipelines_raw_ingest,
#   transforms-python/src/myproject/datasets/raw_dailymed_spl.py
import json
import re
import time
from datetime import datetime, timezone
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from transforms.api import incremental, transform, Output
from transforms.external.systems import external_systems, Source

API = "/dailymed/services/v2"
INGREDIENTS = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol", "semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]  # D018 formulary; widened at step 9 (D039 G1)
PAGE_SIZE = 100
INDEX_SCHEMA = StructType([StructField(c, IntegerType() if c in ("http_status", "spl_version", "result_total") else StringType()) for c in ["search_ingredient", "request_params", "http_status", "result_total", "source_published", "retrieved_at", "setid", "spl_version", "title", "published_date", "record_json", "error_text"]])
XML_SCHEMA = StructType([StructField(c, IntegerType() if c in ("http_status", "index_spl_version", "xml_version_number", "xml_bytes") else StringType()) for c in ["setid", "index_spl_version", "xml_version_number", "effective_time", "http_status", "source_url", "retrieved_at", "xml_bytes", "xml_text", "error_text"]])


RETRY_STATUS, MAX_TRIES = (429, 502, 503, 504), 5  # DailyMed rate-limits fast pulls (HTTP 429, 2026-11-04 learning)


def get(client, url, **kw):
    """GET with back-off: on 429/5xx wait (Retry-After if given, else 2, 4, 8, 16 s) and try again; the last reply is returned either way."""
    for attempt in range(MAX_TRIES):
        resp = client.get(url, **kw)
        if resp.status_code not in RETRY_STATUS or attempt == MAX_TRIES - 1:
            return resp
        wait = resp.headers.get("Retry-After", "")
        time.sleep(min(int(wait), 60) if wait.isdigit() else 2 ** (attempt + 1))


def first(pattern, text):
    m = re.search(pattern, text)
    return m.group(1) if m else None


@incremental(semantic_version=1)  # only to read the previous output; both outputs are replaced every build
@external_systems(dailymedapi=Source("ri.magritte..source.cce69842-52cc-4201-9053-7519dfed6613"))
@transform(index_out=Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_dailymed_spl_index"), xml_out=Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_dailymed_spl_xml"))
def compute(dailymedapi, ctx, index_out, xml_out):
    conn = dailymedapi.get_https_connection()
    client = conn.get_client()
    base = conn.url.rstrip("/") + API
    retrieved_at = datetime.now(timezone.utc).isoformat()
    index_rows, xml_rows, seen = [], [], {}
    for ingredient in INGREDIENTS:
        page = 1
        while True:
            params = {"drug_name": ingredient, "pagesize": PAGE_SIZE, "page": page}
            resp = get(client, base + "/spls.json", params=params, timeout=60)
            if resp.status_code != 200:
                index_rows.append((ingredient, json.dumps(params), resp.status_code, None, None, retrieved_at, None, None, None, None, None, resp.text[:2000]))
                break
            payload = resp.json()
            meta = payload.get("metadata", {})
            for rec in payload.get("data", []):
                index_rows.append((ingredient, json.dumps(params), 200, int(meta.get("total_elements", 0)), meta.get("db_published_date"), retrieved_at, rec.get("setid"), rec.get("spl_version"), rec.get("title"), rec.get("published_date"), json.dumps(rec), None))
                seen[rec.get("setid")] = rec.get("spl_version")
            if page >= int(meta.get("total_pages", 1)):
                break
            page += 1
    # XML we already hold for this exact setid + version (a 200 that really is XML) is reused, not downloaded again.
    try:
        previous = xml_out.dataframe("previous", XML_SCHEMA).filter("http_status = 200 AND xml_text LIKE '<%'")
        have = {(r["setid"], r["index_spl_version"]) for r in previous.select("setid", "index_spl_version").collect()}
    except Exception:  # first build, or a local run with no previous output
        previous, have = None, set()
    reuse = [(k, v) for k, v in seen.items() if (k, v) in have]
    # The XML endpoint serves the current version only; the version inside the XML is recorded to catch a change mid-pull.
    for setid, version in seen.items():
        if (setid, version) in have:
            continue
        url = f"{base}/spls/{setid}.xml"
        resp = get(client, url, timeout=60)
        if resp.status_code != 200:
            xml_rows.append((setid, version, None, None, resp.status_code, url, retrieved_at, None, None, resp.text[:2000]))
            continue
        text = resp.text
        xml_version = first(r'<versionNumber value="(\d+)"', text)
        xml_rows.append((setid, version, int(xml_version) if xml_version else None, first(r'<effectiveTime value="(\d+)"', text), 200, url, retrieved_at, len(resp.content), text, None))
    xml_df = ctx.spark_session.createDataFrame(xml_rows, XML_SCHEMA)
    if reuse:
        keys = ctx.spark_session.createDataFrame(reuse, StructType([StructField("setid", StringType()), StructField("index_spl_version", IntegerType())]))
        xml_df = previous.join(keys, ["setid", "index_spl_version"], "inner").select(*XML_SCHEMA.fieldNames()).unionByName(xml_df)
    index_out.set_mode("replace")
    xml_out.set_mode("replace")
    index_out.write_dataframe(ctx.spark_session.createDataFrame(index_rows, INDEX_SCHEMA))
    xml_out.write_dataframe(xml_df)
