# Hand-in style kit

One look for every hand-in PDF and diagram, copied from the BlueJay Team Technical Guide
(navy `#13324B`, teal `#087F8C`, light `#EAF3F5`, ink `#263746`, Helvetica-like sans).

## Build a report (one command)

```
.venv/bin/python tools/handin/build_report.py R00-sample
```

Output: `docs/11-handin/reports/pdf/R00-sample.pdf` when rebuilt; a copy is kept at [sample/R00-sample.pdf](sample/R00-sample.pdf) so the hand-in folder holds only real reports.
`--all` builds every report in `docs/11-handin/reports/src/`. `--preview DIR` also writes one PNG per page
(handy for checking the layout).

Needs `reportlab` and `pymupdf` in the project venv (installed 2026-11-05):
`.venv/bin/python -m pip install reportlab pymupdf`.

## Files

| File | What it does |
|---|---|
| [style.py](style.py) | Palette, fonts, paragraph styles, table, callouts, pills, status bands, cover, chapter start, gate box, figure, header/footer, glyph check, PDF layout check. Self-test: `.venv/bin/python tools/handin/style.py` |
| [build_report.py](build_report.py) | Turns a report module into a PDF; `{{n:...}}` number lookups; contents page numbers; layout check |
| [drawio.py](drawio.py) | draw.io diagrams in the same palette, with layout checks; writes `.drawio` + PNG + PDF |
| [diagram_style.md](diagram_style.md) | Palette table, Mermaid opt-in (`%% handin-theme`), draw.io export |
| [examples/drawio_example.py](examples/drawio_example.py) | Worked draw.io example |
| [../../docs/diagrams/src/_handin-theme.json](../../docs/diagrams/src/_handin-theme.json) | Mermaid theme in the hand-in palette |
| [../../docs/11-handin/numbers.json](../../docs/11-handin/numbers.json) | The only place report numbers come from |

## How a report is written

A report is **one Python file** in `docs/11-handin/reports/src/`, for example `R01-architecture.py`.
Why Python and not Markdown: no parser to break, tables and figures are plain lists, and a ratio can be
computed from two looked-up numbers. Copy [R00-sample.py](../../docs/11-handin/reports/src/R00-sample.py) to start.

```python
META = {"id": "R01", "title": "Architecture", "short": "Architecture", "subtitle": "raw to ontology",
        "version": "0.1", "date": "6 November 2026"}

def build(r):
    r.cover(lead=[("Question", "...")], is_=["..."], is_not=["..."], how_to_read="...")
    r.chapter("Summary")                      # numbered 01, 02, ... ; new page by default
    r.p("FAERS gives {{n:faers.cases_current}} current cases. **Bold**, *italic*, `code`.")
    r.table(["Col A", "Col B"], [("a", "[[OBSERVED]]")], widths=[3, 1])
    r.gate("Summary done", [("Required evidence", "..."), ("Result", "..."), ("If it fails", "...")], status="TESTED")
```

| Call | Gives |
|---|---|
| `r.cover(lead, is_, is_not, how_to_read)` | Kicker, title, version line, lead box, "What this is / is not" table, "How to read this", contents with page numbers |
| `r.chapter(title, label=None, new_page=True)` | Teal chapter label + navy title; sets the running header |
| `r.h(text, level=2)` | Section heading (level 2 teal, 3 navy); never stranded at a page foot |
| `r.p(text, style="body")` | Paragraph (`style="small"` for fine print) |
| `r.bullets(items, numbered=False)` | Bullet or numbered list |
| `r.table(head, rows, widths=None)` | Navy header row, zebra rows, wrapped cells; widths are relative weights |
| `r.figure(png, caption, source)` | Image at page width, "Figure N." caption, gray source line; kept on one page |
| `r.note / r.warning / r.how_we_know / r.key(text, title=None)` | Callout boxes (text may be a list of paragraphs) |
| `r.gate(name, rows, status=None)` | The box that closes a chapter |
| `r.pills([...])`, `r.pill_legend()` | Evidence pills in a row; the standard legend table |
| `r.status("TESTED"/"PLANNED"/"PROPOSED", text)` | Status band |
| `r.code(text)` | Short monospaced block |
| `r.page_break()`, `r.space(h)` | Layout |
| `r.n("key.path")` | Raw number, for computing in Python |
| `r.numbers_appendix()` | Table of every number used, with the `numbers.json` source line |

**Inline markup** in any text: `**bold**`, `*italic*`, `` `code` ``, `[text](url)`, `[[OBSERVED]]` (pill),
ReportLab tags such as `<br/>`. Plain `<`, `>` and `&` are escaped for you.

**Evidence pills:** OBSERVED, DERIVED, ASSUMED, DESIGNED. **Status:** TESTED, PLANNED, PROPOSED.

## Numbers

Write `{{n:signals.ranked}}`; the builder replaces it from `docs/11-handin/numbers.json`.
Integers get thousands separators (`1,073`). Options: `{{n:key|raw}}`, `{{n:key|.1%}}` (any Python format spec).
**A missing key or a `null` value stops the build.** While `_meta.provisional` is true (or `captured_at` is null),
every page footer says **NUMBERS PROVISIONAL**. The current file holds placeholders; re-capture from Foundry SQL
at the baseline gate.

## Checks the builder runs

| Check | When | On failure |
|---|---|---|
| Glyphs: every character can be drawn | while building | Stops, names the character (for example an emoji) |
| Number keys exist and are not null | while building | Stops, names the key |
| Figure file exists | while building | Stops |
| Contents page numbers settle | up to 4 passes | Stops |
| Text or images outside the 504 x 680 pt body frame, blank pages, replacement characters | after building (pymupdf) | Lists problems, exit 1 |

**Fonts and glyphs.** The built-in PDF Helvetica cannot draw `→ ≥ ≤ ≈` (they print as black boxes).
The kit registers macOS Arial (or DejaVu Sans on Linux) as the body font, Courier New as mono, and falls back per
character to Arial Unicode for symbols such as ✓ ✗. Emoji are refused: write words instead (the project's 📍 🩺 icons
do not belong in a PDF). Add a stand-in to `style.REPLACE` if a character must be mapped.

## Limits

- Callouts, gates and figures cannot split across pages: keep each under about half a page.
- A table row cannot split across pages; very long cells should be broken into rows.
- The layout check catches overflow outside the frame; it does not judge whether a page *looks* good.
  Use `--preview` and look at the pages before handing in.
- Fonts are found at macOS / Debian paths. On another machine with neither, the kit falls back to built-in
  Helvetica and refuses any character outside cp1252.
