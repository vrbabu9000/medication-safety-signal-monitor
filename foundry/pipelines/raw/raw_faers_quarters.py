# Raw FAERS quarterly ASCII exports: every file of each quarterly ZIP stored unchanged, plus a manifest.
# Files dataset: one file per ZIP member under <quarter>/. Manifest: one row per (quarter, file) with size and sha256.
# Contract: docs/04-architecture/dataset-contracts-v1.md (raw_faers_quarter_files). Full snapshot each build (D029: quarterly).
#
# Mirror of Foundry repo Pipelines/pipelines_raw_ingest,
#   transforms-python/src/myproject/datasets/raw_faers_quarters.py
import hashlib
import tempfile
import zipfile
from datetime import datetime, timezone
from pyspark.sql.types import IntegerType, LongType, StringType, StructField, StructType
from transforms.api import transform, Output
from transforms.external.systems import external_systems, Source

QUARTERS = ["2026q1", "2026q2"]
MANIFEST_SCHEMA = StructType([StructField("quarter", StringType()), StructField("zip_url", StringType()), StructField("http_status", IntegerType()), StructField("zip_bytes", LongType()), StructField("file_name", StringType()), StructField("file_bytes", LongType()), StructField("file_sha256", StringType()), StructField("zip_modified", StringType()), StructField("retrieved_at", StringType()), StructField("error_text", StringType())])


@external_systems(faersfiles=Source("ri.magritte..source.dc0c031f-19db-470e-8e7b-df48be315e04"))
@transform(files_out=Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_faers_quarter_files"), manifest_out=Output("/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/raw_faers_quarter_manifest"))
def compute(faersfiles, ctx, files_out, manifest_out):
    conn = faersfiles.get_https_connection()
    client = conn.get_client()
    retrieved_at = datetime.now(timezone.utc).isoformat()
    fs = files_out.filesystem()
    rows = []
    for quarter in QUARTERS:
        url = f"{conn.url.rstrip('/')}/content/Exports/faers_ascii_{quarter}.zip"
        with tempfile.TemporaryFile() as tmp:
            resp = client.get(url, stream=True, timeout=600)
            if resp.status_code != 200:
                rows.append((quarter, url, resp.status_code, None, None, None, None, None, retrieved_at, resp.text[:2000]))
                continue
            for chunk in resp.iter_content(chunk_size=1 << 20):
                tmp.write(chunk)
            zip_bytes = tmp.tell()
            tmp.seek(0)
            with zipfile.ZipFile(tmp) as zf:
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    digest = hashlib.sha256()
                    with zf.open(info) as src, fs.open(f"{quarter}/{info.filename}", "wb") as dst:
                        while True:
                            block = src.read(1 << 20)
                            if not block:
                                break
                            digest.update(block)
                            dst.write(block)
                    rows.append((quarter, url, 200, zip_bytes, info.filename, info.file_size, digest.hexdigest(), "%04d-%02d-%02dT%02d:%02d:%02d" % info.date_time, retrieved_at, None))
    manifest_out.write_dataframe(ctx.spark_session.createDataFrame(rows, MANIFEST_SCHEMA))
