"""draw.io diagrams in the hand-in palette, from Python (adapted from BlueJay's archlib.py).

One model (boxes, groups, arrows with absolute coordinates in px) feeds three writers:
  * write_drawio(): an uncompressed .drawio file (open in draw.io; File > Export as > VSDX for Visio)
  * render():       PNG + PDF. Uses the draw.io desktop CLI when it is installed; otherwise draws a
                    faithful preview with ReportLab (same boxes, colours, text and arrow routes).
  * check():        geometry tests before anything is written (overlaps, text that does not fit,
                    arrows that cross a box, things outside the canvas).

Example:
    from drawio import Diagram
    d = Diagram("21-example-v1", 900, 300, title="Raw to ontology")
    d.box("faers", 40, 80, 200, 70, "FAERS", ["quarterly files"], kind="source")
    d.box("clean", 340, 80, 200, 70, "faers_clean", ["one row per case"], kind="pipeline")
    d.arrow("faers", "clean", label="parse")
    d.save()          # docs/diagrams/drawio/21-example-v1.drawio + png/ + pdf/

Units are draw.io px; the PDF preview uses 1 px = 1 pt. Run tools/handin/examples/drawio_example.py
for a worked example.
"""
from __future__ import annotations

import math
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xesc

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas as rl_canvas

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import style as S  # noqa: E402  (fonts, glyph check, palette)

ROOT = HERE.parents[1]
DIAGRAMS = ROOT / "docs/diagrams"

# ----------------------------------------------------------------------------- palette (matches style.py and the Mermaid theme)
KINDS = {
    # kind: fill, stroke, font
    "source":   ("#EAF3F5", "#087F8C", "#13324B"),   # public data sources
    "pipeline": ("#FFFFFF", "#13324B", "#263746"),   # Foundry datasets / transforms
    "ontology": ("#E1F5EE", "#0F6E56", "#085041"),   # ontology objects, links, actions
    "ai":       ("#EEEDFE", "#534AB7", "#3C3489"),   # LLM / AIP steps
    "app":      ("#13324B", "#13324B", "#FFFFFF"),   # Workshop screen, the user-facing end
    "risk":     ("#FFF3D6", "#B7791F", "#7A4B00"),   # warnings, assumptions, open issues
    "neutral":  ("#F1EFE8", "#5F5E5A", "#444441"),
    # status kinds (same as the PDF status bands)
    "done":     ("#E1F5EE", "#0F6E56", "#085041"),
    "next":     ("#FFF3D6", "#B7791F", "#7A4B00"),
    "planned":  ("#F1EFE8", "#5F5E5A", "#444441"),
}
GROUP_STROKE, GROUP_FONT = "#B4B2A9", "#607080"
EDGE_COLOR, LABEL_COLOR = "#5F5E5A", "#444441"
FONT_FAMILY = "Helvetica"
TITLE_SIZE, SUB_SIZE, GROUP_SIZE, EDGE_SIZE = 13, 11, 12, 10
PITCH = 1.2          # line height / font size
RADIUS = 8           # corner radius (px)
SAFETY = 1.12        # text must fit with 12% slack (renderers differ slightly)
PAD = 8              # inner text padding (px)
ARROW_L, ARROW_W = 7.5, 3.5


def _num(v):
    v = round(float(v), 3)
    return str(int(v)) if v == int(v) else f"{v:.3f}".rstrip("0").rstrip(".")


def _tw(text, size, bold=False):
    return pdfmetrics.stringWidth(text, "Helvetica-Bold" if bold else "Helvetica", size)


class Box:
    def __init__(self, id, x, y, w, h, title, subs=(), kind="neutral", dashed=False, align="center", group=None, sw=1):
        if kind not in KINDS:
            raise KeyError(f"box {id}: kind {kind!r}; use one of {', '.join(KINDS)}")
        self.id, self.x, self.y, self.w, self.h = id, x, y, w, h
        self.title, self.subs = title, [subs] if isinstance(subs, str) else list(subs)
        self.kind, self.dashed, self.align, self.group, self.sw = kind, dashed, align, group, sw

    @property
    def rect(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def lines(self):
        out = [(self.title, TITLE_SIZE, True)] if self.title else []
        return out + [(s, SUB_SIZE, False) for s in self.subs]

    def html(self):
        parts = [f"<b>{xesc(self.title)}</b>"] if self.title else []
        if self.subs:
            parts.append(f'<font style="font-size:{SUB_SIZE}px">' + "<br>".join(xesc(s) for s in self.subs) + "</font>")
        return "<br>".join(parts)


class Group:
    def __init__(self, id, x, y, w, h, label, dashed=False):
        self.id, self.x, self.y, self.w, self.h, self.label, self.dashed = id, x, y, w, h, label, dashed

    @property
    def rect(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)


class Arrow:
    def __init__(self, id, src, dst, label=None, via=(), dashed=False, arrow=True):
        self.id, self.src, self.dst, self.label = id, src, dst, label
        self.via, self.dashed, self.arrow = [tuple(p) for p in via], dashed, arrow
        self.pts = []


def _port(b, toward, horizontal):
    """Point on box b's border facing `toward` (a point). horizontal: leave by the left/right side."""
    tx, ty = toward
    if horizontal:
        x = b.x + b.w if tx >= b.cx else b.x
        y = min(max(ty, b.y + 6), b.y + b.h - 6)
        return (x, y)
    y = b.y + b.h if ty >= b.cy else b.y
    x = min(max(tx, b.x + 6), b.x + b.w - 6)
    return (x, y)


class Diagram:
    def __init__(self, name, w, h, title=None):
        self.name, self.w, self.h, self.title = name, w, h, title
        self.boxes, self.groups, self.arrows, self.by_id = [], [], [], {}

    # model -------------------------------------------------------------------
    def _add(self, obj):
        if obj.id in self.by_id:
            raise ValueError(f"duplicate id {obj.id!r}")
        self.by_id[obj.id] = obj
        return obj

    def box(self, id, x, y, w, h, title, subs=(), kind="neutral", **kw):
        b = self._add(Box(id, x, y, w, h, title, subs, kind, **kw))
        self.boxes.append(b)
        return b

    def group(self, id, x, y, w, h, label, dashed=False):
        g = self._add(Group(id, x, y, w, h, label, dashed))
        self.groups.append(g)
        return g

    def arrow(self, src, dst, label=None, via=(), dashed=False, arrow=True, id=None):
        a = self._add(Arrow(id or f"e{len(self.arrows) + 1}", src, dst, label, via, dashed, arrow))
        self.arrows.append(a)
        return a

    # routing -----------------------------------------------------------------
    def _route(self, a):
        s, d = self.by_id[a.src], self.by_id[a.dst]
        if a.via:
            first, last = a.via[0], a.via[-1]
            h0 = abs(first[1] - s.cy) < abs(first[0] - s.cx) * (s.h / s.w) or not (s.x <= first[0] <= s.x + s.w)
            h1 = abs(last[1] - d.cy) < abs(last[0] - d.cx) * (d.h / d.w) or not (d.x <= last[0] <= d.x + d.w)
            p0, p1 = _port(s, first, h0), _port(d, last, h1)
            return [p0] + a.via + [p1]
        horizontal = d.x >= s.x + s.w or s.x >= d.x + d.w          # side by side
        p0 = _port(s, (d.cx, d.cy), horizontal)
        p1 = _port(d, (s.cx, s.cy), horizontal)
        if horizontal and abs(p0[1] - p1[1]) > 0.5:
            # straight if the boxes share a horizontal band, else one elbow at mid x
            lo, hi = max(s.y, d.y) + 6, min(s.y + s.h, d.y + d.h) - 6
            if lo <= hi:
                y = (lo + hi) / 2
                return [(p0[0], y), (p1[0], y)]
            mx = (p0[0] + p1[0]) / 2
            return [p0, (mx, p0[1]), (mx, p1[1]), p1]
        if not horizontal and abs(p0[0] - p1[0]) > 0.5:
            lo, hi = max(s.x, d.x) + 6, min(s.x + s.w, d.x + d.w) - 6
            if lo <= hi:
                x = (lo + hi) / 2
                return [(x, p0[1]), (x, p1[1])]
            my = (p0[1] + p1[1]) / 2
            return [p0, (p0[0], my), (p1[0], my), p1]
        return [p0, p1]

    def _layout(self):
        for a in self.arrows:
            for end in (a.src, a.dst):
                if end not in self.by_id or not isinstance(self.by_id[end], Box):
                    raise KeyError(f"arrow {a.id}: {end!r} is not a box")
            a.pts = self._route(a)

    # checks ------------------------------------------------------------------
    def check(self):
        """Return a list of problems (empty = fine)."""
        self._layout()
        out = []
        for b in self.boxes:
            if b.x < 0 or b.y < 0 or b.x + b.w > self.w or b.y + b.h > self.h:
                out.append(f"{b.id}: outside the {self.w}x{self.h} canvas")
            ls = b.lines()
            need_w = max((_tw(t, sz, bold) for t, sz, bold in ls), default=0) * SAFETY + 2 * PAD
            need_h = sum(sz * PITCH for _, sz, _ in ls) + 2 * PAD - 4
            if need_w > b.w:
                out.append(f"{b.id}: text needs {need_w:.0f} px wide, box is {b.w}")
            if need_h > b.h:
                out.append(f"{b.id}: text needs {need_h:.0f} px high, box is {b.h}")
            for t, _, _ in ls:
                try:
                    S.plain_safe(t, where=f"box {b.id}")
                except S.GlyphError as e:
                    out.append(str(e))
        for i, b1 in enumerate(self.boxes):
            for b2 in self.boxes[i + 1:]:
                r1, r2 = b1.rect, b2.rect
                if r1[0] < r2[2] and r2[0] < r1[2] and r1[1] < r2[3] and r2[1] < r1[3]:
                    out.append(f"boxes {b1.id} and {b2.id} overlap")
        for g in self.groups:
            if g.x < 0 or g.y < 0 or g.x + g.w > self.w or g.y + g.h > self.h:
                out.append(f"group {g.id}: outside the canvas")
            if _tw(g.label, GROUP_SIZE, True) * SAFETY + 2 * PAD > g.w:
                out.append(f"group {g.id}: label too wide")
        for a in self.arrows:
            if a.label:
                longest = max(math.dist(p, q) for p, q in zip(a.pts[:-1], a.pts[1:]))
                need = _tw(a.label, EDGE_SIZE) + 2 * ARROW_L + 16
                if need > longest:
                    out.append(f"arrow {a.id} ({a.src}->{a.dst}): label {a.label!r} needs {need:.0f} px of straight line, "
                               f"longest segment is {longest:.0f}")
            for p, q in zip(a.pts[:-1], a.pts[1:]):
                for b in self.boxes:
                    if b.id in (a.src, a.dst):
                        continue
                    if _seg_hits(p, q, b.rect):
                        out.append(f"arrow {a.id} ({a.src}->{a.dst}) crosses box {b.id}")
        return out

    # writers -----------------------------------------------------------------
    def write_drawio(self, path):
        self._layout()
        root = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "tools/handin/drawio.py (edit freely in draw.io)",
                                     "modified": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     "version": "24.7.0", "type": "device"})
        d = ET.SubElement(root, "diagram", {"id": self.name, "name": self.title or self.name})
        m = ET.SubElement(d, "mxGraphModel", {
            "dx": "0", "dy": "0", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1",
            "arrows": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": str(self.w),
            "pageHeight": str(self.h), "math": "0", "shadow": "0", "background": "#FFFFFF"})
        r = ET.SubElement(m, "root")
        ET.SubElement(r, "mxCell", {"id": "0"})
        ET.SubElement(r, "mxCell", {"id": "1", "parent": "0"})
        for g in self.groups:
            st = ("rounded=1;arcSize=%s;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=%s;fontColor=%s;"
                  "fontStyle=1;fontSize=%d;fontFamily=%s;verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;%s"
                  % (_arc(g), GROUP_STROKE, GROUP_FONT, GROUP_SIZE, FONT_FAMILY, "dashed=1;dashPattern=6 4;" if g.dashed else ""))
            c = ET.SubElement(r, "mxCell", {"id": g.id, "value": xesc(g.label), "style": st, "vertex": "1", "parent": "1"})
            ET.SubElement(c, "mxGeometry", {"x": _num(g.x), "y": _num(g.y), "width": _num(g.w), "height": _num(g.h), "as": "geometry"})
        for b in self.boxes:
            fill, stroke, font = KINDS[b.kind]
            st = ("rounded=1;arcSize=%s;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=%s;strokeWidth=%s;"
                  "fontSize=%d;fontFamily=%s;align=%s;verticalAlign=middle;spacingLeft=%d;spacingRight=%d;%s"
                  % (_arc(b), fill, stroke, font, _num(b.sw), TITLE_SIZE, FONT_FAMILY, b.align, PAD, PAD,
                     "dashed=1;dashPattern=6 4;" if b.dashed else ""))
            c = ET.SubElement(r, "mxCell", {"id": b.id, "value": b.html(), "style": st, "vertex": "1", "parent": "1"})
            ET.SubElement(c, "mxGeometry", {"x": _num(b.x), "y": _num(b.y), "width": _num(b.w), "height": _num(b.h), "as": "geometry"})
        for a in self.arrows:
            s, t = self.by_id[a.src], self.by_id[a.dst]
            (x0, y0), (x1, y1) = a.pts[0], a.pts[-1]
            st = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=%s;"
                  "strokeWidth=1;fontSize=%d;fontColor=%s;fontFamily=%s;labelBackgroundColor=#FFFFFF;"
                  "exitX=%s;exitY=%s;exitDx=0;exitDy=0;entryX=%s;entryY=%s;entryDx=0;entryDy=0;%s%s"
                  % (EDGE_COLOR, EDGE_SIZE, LABEL_COLOR, FONT_FAMILY, _num((x0 - s.x) / s.w), _num((y0 - s.y) / s.h),
                     _num((x1 - t.x) / t.w), _num((y1 - t.y) / t.h),
                     "endArrow=block;endFill=1;endSize=6;" if a.arrow else "endArrow=none;",
                     "dashed=1;dashPattern=4 3;" if a.dashed else ""))
            c = ET.SubElement(r, "mxCell", {"id": a.id, "value": xesc(a.label or ""), "style": st, "edge": "1",
                                            "parent": "1", "source": a.src, "target": a.dst})
            g = ET.SubElement(c, "mxGeometry", {"relative": "1", "as": "geometry"})
            inner = a.pts[1:-1]
            if inner:
                arr = ET.SubElement(g, "Array", {"as": "points"})
                for x, y in inner:
                    ET.SubElement(arr, "mxPoint", {"x": _num(x), "y": _num(y)})
        ET.indent(root, space="  ")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")
        return Path(path)

    def preview_pdf(self, path):
        """Draw the diagram with ReportLab (1 px = 1 pt). Used when the draw.io CLI is not installed."""
        self._layout()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        c = rl_canvas.Canvas(str(path), pagesize=(self.w, self.h))
        c.setTitle(self.title or self.name)
        H = self.h
        sans, bold = S.FONTS.sans, S.FONTS.bold
        c.setFillColor(colors.white)
        c.rect(0, 0, self.w, self.h, stroke=0, fill=1)
        for g in self.groups:
            c.setStrokeColor(colors.HexColor(GROUP_STROKE))
            c.setFillColor(colors.white)
            c.setLineWidth(1)
            c.setDash(6, 4) if g.dashed else c.setDash()
            c.roundRect(g.x, H - g.y - g.h, g.w, g.h, RADIUS, stroke=1, fill=1)
            c.setDash()
            c.setFillColor(colors.HexColor(GROUP_FONT))
            c.setFont(bold, GROUP_SIZE)
            c.drawString(g.x + 10, H - g.y - 4 - GROUP_SIZE, S.plain_safe(g.label))
        for b in self.boxes:
            fill, stroke, font = KINDS[b.kind]
            c.setFillColor(colors.HexColor(fill))
            c.setStrokeColor(colors.HexColor(stroke))
            c.setLineWidth(b.sw)
            c.setDash(6, 4) if b.dashed else c.setDash()
            c.roundRect(b.x, H - b.y - b.h, b.w, b.h, RADIUS, stroke=1, fill=1)
            c.setDash()
            ls = b.lines()
            total = sum(sz * PITCH for _, sz, _ in ls)
            y = H - (b.cy - total / 2)
            c.setFillColor(colors.HexColor(font))
            for t, sz, isb in ls:
                y -= sz * PITCH
                c.setFont(bold if isb else sans, sz)
                t = S.plain_safe(t)
                base = y + sz * (PITCH - 1) / 2 + sz * 0.18
                if b.align == "left":
                    c.drawString(b.x + PAD, base, t)
                else:
                    c.drawCentredString(b.cx, base, t)
        for a in self.arrows:
            pts = [(x, H - y) for x, y in a.pts]
            c.setStrokeColor(colors.HexColor(EDGE_COLOR))
            c.setLineWidth(1)
            c.setDash(4, 3) if a.dashed else c.setDash()
            end = pts[-1]
            if a.arrow:   # stop the line at the base of the arrow head
                (px, py) = pts[-2]
                L = math.dist((px, py), end) or 1
                ux, uy = (end[0] - px) / L, (end[1] - py) / L
                pts = pts[:-1] + [(end[0] - ux * ARROW_L, end[1] - uy * ARROW_L)]
            p = c.beginPath()
            p.moveTo(*pts[0])
            for q in pts[1:]:
                p.lineTo(*q)
            c.drawPath(p, stroke=1, fill=0)
            c.setDash()
            if a.arrow:
                bx, by = end[0] - ux * ARROW_L, end[1] - uy * ARROW_L
                h = c.beginPath()
                h.moveTo(*end)
                h.lineTo(bx - uy * ARROW_W, by + ux * ARROW_W)
                h.lineTo(bx + uy * ARROW_W, by - ux * ARROW_W)
                h.close()
                c.setFillColor(colors.HexColor(EDGE_COLOR))
                c.drawPath(h, stroke=0, fill=1)
            if a.label:
                mx, my = _midpoint([(x, H - y) for x, y in a.pts])
                t = S.plain_safe(a.label)
                w = pdfmetrics.stringWidth(t, sans, EDGE_SIZE)
                c.setFillColor(colors.white)
                c.rect(mx - w / 2 - 3, my - EDGE_SIZE * 0.45, w + 6, EDGE_SIZE * 1.25, stroke=0, fill=1)
                c.setFillColor(colors.HexColor(LABEL_COLOR))
                c.setFont(sans, EDGE_SIZE)
                c.drawCentredString(mx, my - EDGE_SIZE * 0.1, t)
        c.showPage()
        c.save()
        return Path(path)

    def render(self, png, pdf, drawio_file=None, scale=3):
        """PNG + PDF: through the draw.io CLI if present, else the ReportLab preview."""
        cli = find_drawio_cli()
        if cli and drawio_file:
            subprocess.run([cli, "-x", "-f", "pdf", "--crop", "-o", str(pdf), str(drawio_file)], check=True)
            subprocess.run([cli, "-x", "-f", "png", "-s", str(scale), "-o", str(png), str(drawio_file)], check=True)
            return "drawio-cli"
        self.preview_pdf(pdf)
        _pdf_to_png(pdf, png, scale)
        return "reportlab-preview"

    def save(self, folder=DIAGRAMS, strict=True):
        """Check, then write <folder>/drawio/<name>.drawio, png/<name>.png and pdf/<name>.pdf."""
        problems = self.check()
        for p in problems:
            print("DIAGRAM", self.name, p)
        if problems and strict:
            raise SystemExit(f"{self.name}: {len(problems)} layout problem(s); fix them or save(strict=False)")
        folder = Path(folder)
        dio = self.write_drawio(folder / "drawio" / f"{self.name}.drawio")
        (folder / "png").mkdir(parents=True, exist_ok=True)
        (folder / "pdf").mkdir(parents=True, exist_ok=True)
        how = self.render(folder / "png" / f"{self.name}.png", folder / "pdf" / f"{self.name}.pdf", dio)
        print(f"{self.name}: {dio} + png + pdf ({how})")
        return dio


def _arc(n):
    return _num(round(RADIUS / min(n.w, n.h) * 100, 2))


def _midpoint(pts):
    segs = list(zip(pts[:-1], pts[1:]))
    total = sum(math.dist(p, q) for p, q in segs)
    acc = 0
    for p, q in segs:
        L = math.dist(p, q)
        if acc + L >= total / 2 and L:
            t = (total / 2 - acc) / L
            return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
        acc += L
    return pts[-1]


def _seg_hits(p, q, r, eps=1.0):
    """Does the axis-aligned (or general) segment p-q pass through the inside of rectangle r?"""
    x0, y0, x1, y1 = r[0] + eps, r[1] + eps, r[2] - eps, r[3] - eps
    for i in range(41):
        t = i / 40
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if x0 < x < x1 and y0 < y < y1:
            return True
    return False


def find_drawio_cli():
    for c in (shutil.which("drawio"), shutil.which("draw.io"), "/Applications/draw.io.app/Contents/MacOS/draw.io"):
        if c and Path(c).exists():
            return c
    return None


def _pdf_to_png(pdf, png, scale=3):
    try:
        import pymupdf
        with pymupdf.open(str(pdf)) as d:
            d[0].get_pixmap(dpi=72 * scale).save(str(png))
        return
    except ImportError:
        pass
    if shutil.which("pdftoppm"):
        stem = str(Path(png).with_suffix(""))
        subprocess.run(["pdftoppm", "-png", "-singlefile", "-r", str(72 * scale), str(pdf), stem], check=True)
        return
    raise SystemExit("PNG export needs pymupdf (pip install pymupdf) or pdftoppm (brew install poppler)")
