"""Run a Foundry transform file on your machine, with stand-ins for Foundry's libraries.

Raw transforms call the real public APIs through a plain `requests` session; outputs are saved as JSON Lines
(tables) or files under --out, so clean transforms can be tested on them next.

    python foundry/tools/local_run/run_local.py foundry/pipelines/raw/raw_rxnorm.py
    python foundry/tools/local_run/run_local.py foundry/pipelines/raw/raw_openfda_enforcement.py --limit-rows 3

Stand-ins cover what this repo uses: @external_systems/Source, @transform, @transform_df, transform.using,
Input/Output, ctx.spark_session.createDataFrame(rows, schema), output.write_dataframe / write_table / filesystem(),
and input.polars() / input.pandas() reading earlier local outputs. Not a Foundry emulator: check results in Foundry too.
"""
import argparse
import importlib.util
import inspect
import json
import os
import sys
import types

# Source RID -> base URL, so raw files run without extra flags (see foundry/README.md resource map).
SOURCE_URLS = {
    "ri.magritte..source.e46a0898-be14-401d-92d1-f9c20afa7f94": "https://api.fda.gov",
    "ri.magritte..source.cce69842-52cc-4201-9053-7519dfed6613": "https://dailymed.nlm.nih.gov",
    "ri.magritte..source.79ca01f9-95d0-43c6-8e28-cc9681a2ed5f": "https://rxnav.nlm.nih.gov",
    "ri.magritte..source.dc0c031f-19db-470e-8e7b-df48be315e04": "https://fis.fda.gov",
}


def install_stubs(out_dir):
    def decorate(attr, value):
        def wrap(f):
            setattr(f, attr, value)
            return f
        return wrap

    class Path(str):
        pass

    def Output(path, *a, **kw):
        return ("output", path)

    def Input(path, *a, **kw):
        return ("input", path)

    class _Transform:
        def __call__(self, **io):
            return decorate("_io", io)

        def using(self, **io):
            return decorate("_io", io)

    def transform_df(output, **inputs):
        return decorate("_df", (output, inputs))

    api = types.ModuleType("transforms.api")
    api.transform, api.transform_df, api.Output, api.Input = _Transform(), transform_df, Output, Input
    api.lightweight = lambda *a, **kw: (a[0] if a and callable(a[0]) else (lambda f: f))
    ext = types.ModuleType("transforms.external.systems")
    ext.external_systems = lambda **src: decorate("_sources", src)
    ext.Source = lambda rid: rid
    ext.ResolvedSource = object
    for name, mod in [("transforms", types.ModuleType("transforms")), ("transforms.api", api), ("transforms.external", types.ModuleType("transforms.external")), ("transforms.external.systems", ext)]:
        sys.modules[name] = mod

    try:
        import pyspark.sql.types  # noqa: F401  (real types are fine: we only read field names)
    except ImportError:
        class _Type:
            def __init__(self, *a, **kw):
                pass

        class StructField:
            def __init__(self, name, dtype=None, nullable=True):
                self.name = name

        class StructType:
            def __init__(self, fields=None):
                self.fields = list(fields or [])

        t = types.ModuleType("pyspark.sql.types")
        t.StructField, t.StructType = StructField, StructType
        for n in ["StringType", "IntegerType", "LongType", "DoubleType", "BooleanType", "TimestampType", "DateType"]:
            setattr(t, n, _Type)
        sql = types.ModuleType("pyspark.sql")
        sql.types = t
        sql.Row = lambda **kw: kw
        for name, mod in [("pyspark", types.ModuleType("pyspark")), ("pyspark.sql", sql), ("pyspark.sql.types", t)]:
            sys.modules[name] = mod


class Table:
    def __init__(self, rows, schema):
        names = [f.name for f in schema.fields] if schema is not None else None
        self.records = [r if isinstance(r, dict) else dict(zip(names, r)) for r in rows]


class Ctx:
    class spark_session:
        @staticmethod
        def createDataFrame(rows, schema=None):
            return Table(rows, schema)


class FakeSource:
    def __init__(self, url):
        self.url = url

    def get_https_connection(self):
        import requests
        src = self

        class Conn:
            url = src.url

            def get_client(self):
                return requests.Session()
        return Conn()


class FakeOutput:
    def __init__(self, path, out_dir, limit):
        self.name, self.out_dir, self.limit = os.path.basename(path), out_dir, limit

    def write_dataframe(self, df):
        self._save(df.records)

    def write_table(self, df):
        if hasattr(df, "collect"):
            df = df.collect()
        null_cols = [c for c, t in getattr(df, "schema", {}).items() if str(t) == "Null"]
        if null_cols:
            print(f"[{self.name}] WARNING all-null (untyped) columns, Foundry may reject them: {null_cols}")
        self._save(df.to_dicts() if hasattr(df, "to_dicts") else df.to_dict("records"))

    def filesystem(self):
        root = os.path.join(self.out_dir, self.name)

        class FS:
            def open(self, rel, mode="r"):
                full = os.path.join(root, rel)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                return open(full, mode)
        print(f"[{self.name}] files -> {root}")
        return FS()

    def _save(self, records):
        os.makedirs(self.out_dir, exist_ok=True)
        path = os.path.join(self.out_dir, self.name + ".jsonl")
        with open(path, "w") as f:
            for r in records:
                f.write(json.dumps(r, default=str) + "\n")
        print(f"[{self.name}] {len(records)} rows -> {path}")
        for r in records[: self.limit]:
            print("   ", {k: (str(v)[:60] if v is not None else None) for k, v in r.items()})


class FakeInput:
    def __init__(self, path, out_dir):
        self.file = os.path.join(out_dir, os.path.basename(path) + ".jsonl")
        self.root = os.path.join(out_dir, os.path.basename(path))
        if not os.path.exists(self.file) and not os.path.isdir(self.root):
            raise SystemExit(f"Input {path} not found locally: run its raw transform first ({self.file})")

    def filesystem(self):
        # Files dataset: a folder under --out (e.g. raw_faers_quarter_files/<quarter>/ASCII/DEMO26Q1.txt).
        root = self.root

        class FileStatus:
            def __init__(self, path):
                self.path = path

        class FS:
            def ls(self, glob=None, regex=None):
                for d, _, names in os.walk(root, followlinks=True):
                    for n in names:
                        yield FileStatus(os.path.relpath(os.path.join(d, n), root))

            def open(self, rel, mode="r"):
                return open(os.path.join(root, rel), mode)
        return FS()

    def polars(self, lazy=False):
        import polars as pl
        df = pl.read_ndjson(self.file)
        return df.lazy() if lazy else df

    def pandas(self):
        import pandas as pd
        return pd.read_json(self.file, lines=True)


def run(path, out_dir, limit, only):
    install_stubs(out_dir)
    spec = importlib.util.spec_from_file_location("transform_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    funcs = [f for n, f in vars(mod).items() if callable(f) and (hasattr(f, "_io") or hasattr(f, "_df")) and (not only or n == only)]
    if not funcs:
        raise SystemExit("No transform found in " + path)
    for f in funcs:
        print(f"== {f.__name__}")
        sources = getattr(f, "_sources", {})
        io = dict(getattr(f, "_io", {}))
        df_out = None
        if hasattr(f, "_df"):
            df_out, inputs = f._df
            io.update(inputs)
        kwargs = {}
        for p in inspect.signature(f).parameters:
            if p in sources:
                kwargs[p] = FakeSource(SOURCE_URLS.get(sources[p], sources[p]))
            elif p == "ctx":
                kwargs[p] = Ctx()
            elif p in io:
                kind, ds = io[p]
                kwargs[p] = FakeOutput(ds, out_dir, limit) if kind == "output" else FakeInput(ds, out_dir)
            else:
                raise SystemExit(f"Don't know how to fill parameter '{p}'")
        result = f(**kwargs)
        if df_out is not None:
            out = FakeOutput(df_out[1], out_dir, limit)
            out.write_dataframe(result) if isinstance(result, Table) else out.write_table(result)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "out"))
    ap.add_argument("--limit-rows", type=int, default=2, help="sample rows to print per output")
    ap.add_argument("--func", help="run only this transform function")
    a = ap.parse_args()
    run(a.file, a.out, a.limit_rows, a.func)
