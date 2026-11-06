"""Build hand-in report PDFs from report modules.

A report is one Python file in docs/11-handin/reports/src/ (for example R00-sample.py) with:

    META = {"id": "R00", "title": "...", "subtitle": "...", "version": "0.1", "date": "2026-11-05"}
    def build(r):            # r is a Report (below)
        r.cover(...)
        r.chapter("Summary")
        r.p("FAERS has {{n:faers.cases_current}} current cases.")
        ...

Output: docs/11-handin/reports/pdf/<file stem>.pdf

Run (from the project root):
    .venv/bin/python tools/handin/build_report.py R00-sample            # one report
    .venv/bin/python tools/handin/build_report.py --all                 # every report in src/
    .venv/bin/python tools/handin/build_report.py R00-sample --preview /some/dir   # also PNG per page

Numbers: write {{n:key.path}} in any text; it is replaced from docs/11-handin/numbers.json.
A missing key or a null value stops the build. Optional format: {{n:key.path|,.1f}} (Python format spec),
{{n:key.path|raw}} (no thousands separator). Integers get thousands separators by default.
In Python code, r.n("key.path") returns the raw value (for a computed ratio, say).

The build runs in passes (normally two) so the contents table on the cover can print the page
where each chapter landed. After the build, style.check_pdf() looks for text or images outside
the frame, blank pages and replacement characters; any problem stops the build (exit 1).
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import style as S  # noqa: E402
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate  # noqa: E402

ROOT = HERE.parents[1]
HANDIN = ROOT / "docs/11-handin"
SRC = HANDIN / "reports/src"
OUT = HANDIN / "reports/pdf"
NUMBERS = HANDIN / "numbers.json"
PROJECT = "MEDICATION SAFETY SIGNAL MONITOR"

_NUM = re.compile(r"\{\{n:([A-Za-z0-9_.\-]+)(?:\|([^}]*))?\}\}")


class NumberError(KeyError):
    pass


class Numbers:
    """docs/11-handin/numbers.json, looked up by dotted path. Records every key used."""

    def __init__(self, path=NUMBERS):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.meta = self.data.get("_meta", {})
        self.used = {}

    @property
    def provisional(self):
        return bool(self.meta.get("provisional")) or self.meta.get("captured_at") in (None, "")

    def get(self, key):
        cur = self.data
        for part in key.split("."):
            if not isinstance(cur, dict) or part not in cur:
                raise NumberError(f"numbers.json has no key {key!r} (stopped at {part!r}); add it to {self.path}")
            cur = cur[part]
        if cur is None:
            raise NumberError(f"numbers.json key {key!r} is null: capture the value before using it")
        if isinstance(cur, (dict, list)):
            raise NumberError(f"numbers.json key {key!r} is a {type(cur).__name__}, not a number or text")
        self.used[key] = cur
        return cur

    def fmt(self, key, spec=None):
        v = self.get(key)
        if spec == "raw":
            return str(v)
        if spec:
            return format(v, spec)
        if isinstance(v, bool):
            return str(v)
        if isinstance(v, int):
            return f"{v:,}"
        return str(v)

    def sub(self, text):
        return _NUM.sub(lambda m: self.fmt(m.group(1), m.group(2)), text)

    def deep(self, obj):
        """Substitute inside strings, lists, tuples and dicts (cell lists, callout lists...)."""
        if isinstance(obj, str):
            return self.sub(obj)
        if isinstance(obj, (list, tuple)):
            return type(obj)(self.deep(x) for x in obj)
        if isinstance(obj, dict):
            return {k: self.deep(v) for k, v in obj.items()}
        return obj


class Report:
    """What a report module's build(r) calls. Every text argument accepts the inline markup of
    style.rich() and {{n:...}} number lookups."""

    def __init__(self, meta, numbers, pages=None):
        self.meta, self.N, self.pages = meta, numbers, pages or {}
        self.flow, self.chapters, self._fig, self._chap = [], [], 0, 0

    # numbers --------------------------------------------------------------
    def n(self, key):
        return self.N.get(key)

    def _t(self, x):
        return self.N.deep(x)

    # structure ------------------------------------------------------------
    def cover(self, lead=None, is_=(), is_not=(), how_to_read=None, contents=True, kicker=None):
        m = self.meta
        kick = kicker or f"{PROJECT} · HAND-IN {m['id']}"
        sub = f"Version {m.get('version', '0.1')}, {m.get('date', '')}" + (f": {m['subtitle']}" if m.get("subtitle") else "")
        self.flow += S.cover(self._t(kick), self._t(m["title"]), self._t(sub), self._t(list(is_)), self._t(list(is_not)),
                             self._t(how_to_read), self._t(lead))
        if contents:
            self.flow.append(_Contents(self))

    def chapter(self, title, label=None, new_page=True):
        """Start a chapter. label defaults to the next number ('01', '02', ...)."""
        self._chap += 1
        label = label or f"{self._chap:02d}"
        key = f"ch{len(self.chapters) + 1}"
        self.chapters.append((key, label, self._t(title)))
        # no page break before the very first flowable (it would leave page 1 blank)
        self.flow += S.chapter_start(label, self._t(title), key=key, new_page=new_page and bool(self.flow))

    def h(self, text, level=2):
        self.flow += S.heading(self._t(text), level)

    def p(self, text, style="body"):
        self.flow.append(S.para(self._t(text), style))

    def bullets(self, items, numbered=False):
        self.flow.append(S.bullets(self._t(list(items)), numbered))

    def table(self, head, rows, widths=None, **kw):
        self.flow.append(S.table(self._t(head), self._t([list(r) for r in rows]), widths, **kw))

    def figure(self, path, caption, source=None, **kw):
        self._fig += 1
        self.flow.append(S.figure(path, self._t(caption), self._t(source or str(path)), number=self._fig, root=ROOT, **kw))

    def callout(self, kind, text, title=None):
        self.flow.append(S.callout(kind, self._t(text), self._t(title)))

    def note(self, text, title=None):
        self.callout("note", text, title)

    def warning(self, text, title=None):
        self.callout("warning", text, title)

    def how_we_know(self, text, title=None):
        self.callout("how", text, title)

    def key(self, text, title=None):
        self.callout("key", text, title)

    def gate(self, name, rows, status=None):
        self.flow.append(S.gate(self._t(name), self._t(list(rows)), status))

    def status(self, status, text):
        self.flow.append(S.status_band(status, self._t(text)))

    def pills(self, labels):
        self.flow.append(S.pill_row(list(labels)))

    def pill_legend(self, labels=None):
        self.flow.append(S.pill_legend(labels or S.EVIDENCE + S.STATUSES))

    def code(self, text):
        self.flow.append(S.code(self._t(text)))

    def space(self, h=8):
        self.flow.append(S.spacer(h))

    def page_break(self):
        self.flow.append(PageBreak())

    def numbers_appendix(self, title="Numbers used in this report"):
        """Table of every {{n:...}} key used so far, its value, and where numbers.json says they came from."""
        self.h(title)
        src = self.N.meta.get("source", "not stated")
        when = self.N.meta.get("captured_at") or "not captured yet"
        self.p(f"Every number in the table below is looked up from `docs/11-handin/numbers.json` at build time. "
               f"Source: {src.rstrip('.')}. Captured: {when}. Figures quoted from other project records "
               f"(decision log, data-issues register, optimization log) name that record where they appear.")
        rows = [(f"`{k}`", f"{v:,}" if isinstance(v, int) and not isinstance(v, bool) else str(v))
                for k, v in sorted(self.N.used.items())]
        self.flow.append(S.table(["Key", "Value"], rows or [("(none)", "")], widths=[3, 1]))


class _Contents(S.Flowable):
    """Placeholder replaced at build time by the contents table (chapter, page)."""

    def __init__(self, report):
        super().__init__()
        self.report = report

    def wrap(self, aW, aH):
        self._t = S.table(["Contents", "Page"],
                          [(f"{lab} · {t}", str(self.report.pages.get(k, "00"))) for k, lab, t in self.report.chapters],
                          widths=[9, 1], pad=4)
        return self._t.wrap(aW, aH)

    def drawOn(self, canv, x, y, _sW=0):
        self._t.drawOn(canv, x, y, _sW)

    def split(self, aW, aH):
        return []


class _Doc(BaseDocTemplate):
    def __init__(self, target, **kw):
        super().__init__(target, pagesize=(S.PAGE_W, S.PAGE_H), leftMargin=S.MARGIN_L, rightMargin=S.MARGIN_R,
                         topMargin=S.MARGIN_T, bottomMargin=S.MARGIN_B, **kw)
        frame = Frame(S.MARGIN_L, S.MARGIN_B, S.FRAME_W, S.FRAME_H, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0, id="body")
        self.addPageTemplates([PageTemplate(id="page", frames=[frame])])
        self.found = {}

    def afterFlowable(self, f):
        k = getattr(f, "_hd_key", None)
        if k:
            self.found.setdefault(k, self.canv.getPageNumber())


def load_module(path):
    spec = importlib.util.spec_from_file_location(f"handin_report_{path.stem.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for need in ("META", "build"):
        if not hasattr(mod, need):
            raise SystemExit(f"{path}: report module must define {need}")
    for k in ("id", "title"):
        if k not in mod.META:
            raise SystemExit(f"{path}: META needs {k!r}")
    return mod


def build_one(path, preview=None):
    mod = load_module(path)
    meta = mod.META
    pages, buf = {}, None
    for _ in range(4):
        numbers = Numbers()
        r = Report(meta, numbers, pages)
        mod.build(r)
        flag = "NUMBERS PROVISIONAL" if numbers.provisional and numbers.used else None
        canvas_cls = S.make_canvas(
            header_left=f"{PROJECT}  /  {meta['id']} {meta.get('short', meta['title'])}  /  v{meta.get('version', '0.1')}",
            footer_left=f"Soragence technical build · public data only, no PHI · {meta.get('date', '')}",
            footer_flag=flag)
        buf = io.BytesIO()
        doc = _Doc(buf, title=f"{meta['id']} {meta['title']}", author=meta.get("author", "Medication Safety Signal Monitor team"),
                   subject=meta.get("subtitle", ""))
        doc.build(r.flow, canvasmaker=canvas_cls)
        if doc.found == pages:
            break
        pages = doc.found
    else:
        raise RuntimeError("contents page numbers did not settle after 4 passes")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{path.stem}.pdf"
    out.write_bytes(buf.getvalue())
    problems = S.check_pdf(out)
    print(f"{out.relative_to(ROOT)}  ({len(pages)} chapters; numbers used: {len(numbers.used)}"
          f"{'; PROVISIONAL' if flag else ''})")
    if problems is None:
        print("  layout check skipped: pymupdf not installed")
    elif problems:
        for pr in problems:
            print("  LAYOUT", pr)
        raise SystemExit(f"{out.name}: {len(problems)} layout problem(s)")
    else:
        print("  layout check: OK (nothing outside the frame, no blank pages)")
    if preview:
        _preview(out, Path(preview) / path.stem)
    return out


def _preview(pdf, folder, dpi=80):
    import pymupdf
    folder.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(str(pdf)) as d:
        for i, page in enumerate(d, 1):
            page.get_pixmap(dpi=dpi).save(str(folder / f"page-{i:02d}.png"))
    print(f"  preview PNGs -> {folder}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="*", help="report file stems in docs/11-handin/reports/src (or paths)")
    ap.add_argument("--all", action="store_true", help="build every report in src/")
    ap.add_argument("--preview", help="also write a PNG per page into this folder")
    a = ap.parse_args(argv)
    if a.all:
        paths = sorted(p for p in SRC.glob("*.py") if not p.name.startswith("_"))
    else:
        paths = [Path(n) if n.endswith(".py") else SRC / f"{n}.py" for n in a.names]
    if not paths:
        ap.error("name a report (e.g. R00-sample) or pass --all")
    for p in paths:
        if not p.exists():
            raise SystemExit(f"no such report: {p}")
        build_one(p.resolve(), a.preview)


if __name__ == "__main__":
    main()
