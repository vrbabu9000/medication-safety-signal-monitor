# Diagram style for hand-in material

Hand-in diagrams use the same palette as the hand-in PDFs ([style.py](style.py)), copied from the BlueJay technical guide.
Diagrams stay **separate PNG + PDF files** (decision D017). Reports only insert the PNG with `r.figure(...)`.

## Palette

| Role | Fill | Border | Text | Use for |
|---|---|---|---|---|
| `source` | `#EAF3F5` | `#087F8C` teal | `#13324B` navy | Public data sources (FAERS, DailyMed, openFDA, RxNorm) |
| `pipeline` | `#FFFFFF` | `#13324B` navy | `#263746` ink | Foundry datasets and transforms |
| `ontology` | `#E1F5EE` | `#0F6E56` | `#085041` | Ontology objects, links, Actions |
| `ai` | `#EEEDFE` | `#534AB7` | `#3C3489` | LLM / AIP steps |
| `app` | `#13324B` | `#13324B` | `#FFFFFF` | The Workshop screen (the user-facing end) |
| `risk` | `#FFF3D6` | `#B7791F` | `#7A4B00` | Assumptions, warnings, open issues |
| `neutral` | `#F1EFE8` | `#5F5E5A` | `#444441` | Anything else |
| group / subgraph | `#FFFFFF` | `#B4B2A9` | `#607080` | Lanes such as "Public sources" |
| arrows | | `#5F5E5A` | `#444441` | All edges; dashed = optional or assumed |

Status colours (same as the PDF status bands): **done/TESTED** = `ontology` green, **next/PROPOSED** = `risk` amber, **planned** = `neutral` stone.
Chart series order: teal `#087F8C`, navy `#13324B`, amber `#B7791F`, violet `#534AB7`, green `#0F6E56`, gray `#607080`.

Font: Helvetica / Arial. Box titles bold. Keep text inside boxes to 2–3 short lines.

## Mermaid (the default way, rendered by `tools/render_diagrams.sh`)

1. Create `docs/diagrams/src/NN-topic-v1.mmd` as usual.
2. Add the line `%% handin-theme` right after the diagram type line (after any `---` front matter).
   `render_diagrams.sh` then uses [`docs/diagrams/src/_handin-theme.json`](../../docs/diagrams/src/_handin-theme.json) instead of `_config.json`.
   Files without that line render exactly as before.
3. Paste the class definitions and tag nodes with `:::source`, `:::pipeline`, ...

```
flowchart LR
%% handin-theme
  classDef source fill:#EAF3F5,stroke:#087F8C,color:#13324B
  classDef pipeline fill:#FFFFFF,stroke:#13324B,color:#263746
  classDef ontology fill:#E1F5EE,stroke:#0F6E56,color:#085041
  classDef ai fill:#EEEDFE,stroke:#534AB7,color:#3C3489
  classDef app fill:#13324B,stroke:#13324B,color:#FFFFFF
  classDef risk fill:#FFF3D6,stroke:#B7791F,color:#7A4B00
  F["<b>FAERS</b><br/>quarterly files"]:::source --> C["<b>faers_clean</b>"]:::pipeline
```

4. Charts (`xychart-beta`) pick up the series colours from the theme. Do **not** set `plotColorPalette`
   in the file's front matter: front matter wins over the theme file (`14-data-volume-v1.mmd` does this today).
5. Render: `bash tools/render_diagrams.sh`, then **open the PNG** before using it.

Tested on 2026-11-05 with mermaid-cli 11.4.2: a flowchart (classes, subgraph, dashed edge, `≥` and `→` in labels)
and an xychart (bar + line) rendered in this palette. No existing `.mmd` file opts in, so the current diagrams are unchanged.

## draw.io (when you need exact placement, or a Visio file)

Use [`drawio.py`](drawio.py) (adapted from BlueJay's `archlib.py`). You place boxes in px; it checks the layout
(overlaps, text that does not fit, arrows through boxes, arrow labels with no room), then writes:

- `docs/diagrams/drawio/<name>.drawio` — open in draw.io; *File → Export as → VSDX* for Visio.
- `docs/diagrams/png/<name>.png` and `docs/diagrams/pdf/<name>.pdf`.

PNG/PDF come from the **draw.io desktop CLI** if it is installed (`drawio` on PATH or `/Applications/draw.io.app`).
It is **not installed on this Mac today**, so `drawio.py` draws a ReportLab preview instead: same boxes, colours,
text and arrow routes, but not pixel-identical to draw.io. For a pixel-exact export, install draw.io desktop
(`brew install --cask drawio`) and run `save()` again, or open the `.drawio` file and use *File → Export as → PNG / PDF*
(PNG: zoom 300 %, border 10; PDF: tick "Crop").

Worked example (writes to a temp folder, not to `docs/diagrams`):

```
.venv/bin/python tools/handin/examples/drawio_example.py
```

## Rules (from CLAUDE.md §5 and D017)

- Never put diagram code inside a `.md` file; link the PNG and PDF.
- Bump the version in the file name on change (`-v1` → `-v2`); keep the old one.
- Look at the rendered PNG before saying a diagram is done.
