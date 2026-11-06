"""Hand-in style kit (ReportLab): one look for every hand-in PDF.

Visual style copied from the BlueJay Team Technical Guide (build_team_guide.py):
navy #13324B, teal #087F8C, light #EAF3F5, ink #263746, gray #607080, Helvetica-like sans,
navy table header rows with zebra shading, a cover with "what this is / is not" and
"how to read this", gate boxes that close a chapter, running header and "n / total" footer.

Everything here returns flowables; tools/handin/build_report.py assembles them into a report.

Text helpers take a light inline markup (see rich()):
  **bold**  *italic*  `code`  [text](url)  [[OBSERVED]] (inline pill)  and ReportLab tags (<b>, <br/>, <font ...>).
Plain '<', '>' and '&' are escaped for you, so "PRR >= 2" and "A & B" are safe.

Glyphs: the built-in PDF Helvetica cannot draw -> . >= etc. (they print as black boxes).
We register Arial (macOS) or DejaVu Sans (Linux) as the body font, fall back per character
to Arial Unicode for symbols such as a check mark, and fail loudly on anything still missing
(emoji, for example). Self-test: .venv/bin/python tools/handin/style.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (CondPageBreak, Flowable, Image, KeepTogether, ListFlowable, ListItem,
                                Paragraph, Spacer, Table, TableStyle, XPreformatted)

# ----------------------------------------------------------------------------- page geometry
PAGE_W, PAGE_H = letter            # 612 x 792 pt (US Letter, as BlueJay)
MARGIN_L = MARGIN_R = 54
MARGIN_T, MARGIN_B = 54, 58
FRAME_W = PAGE_W - MARGIN_L - MARGIN_R   # 504 pt; the frame has zero padding, so tables and text share it
FRAME_H = PAGE_H - MARGIN_T - MARGIN_B   # 680 pt

# ----------------------------------------------------------------------------- palette
HEX = {
    "navy": "#13324B", "teal": "#087F8C", "light": "#EAF3F5", "ink": "#263746", "gray": "#607080",
    "rule": "#C9D6DC", "white": "#FFFFFF",
    # status family (from the BlueJay project-map palette)
    "green_fill": "#E1F5EE", "green_edge": "#0F6E56", "green_ink": "#085041",
    "amber_fill": "#FFF3D6", "amber_edge": "#B7791F", "amber_ink": "#7A4B00",
    "stone_fill": "#F1EFE8", "stone_edge": "#5F5E5A", "stone_ink": "#444441",
    "violet_fill": "#EEEDFE", "violet_edge": "#534AB7", "violet_ink": "#3C3489",
    "tealpill_fill": "#D7EEF0", "tealpill_ink": "#05606A",
}
C = {k: colors.HexColor(v) for k, v in HEX.items()}
NAVY, TEAL, LIGHT, INK, GRAY = C["navy"], C["teal"], C["light"], C["ink"], C["gray"]

# Evidence labels (what kind of claim) and status bands (how far along).
PILLS = {
    # label: (fill, edge, ink, meaning)
    "OBSERVED": ("tealpill_fill", "teal", "tealpill_ink",
                 "Read directly from a public source (FAERS, DailyMed, openFDA, RxNorm), with the query that produced it."),
    "DERIVED": ("light", "navy", "navy",
                "Computed by our pipeline from observed data, for example a PRR or a count per drug and reaction."),
    "ASSUMED": ("amber_fill", "amber_edge", "amber_ink",
                "Not verified: taken as true for now because the data or the brief is silent. It could be wrong."),
    "DESIGNED": ("violet_fill", "violet_edge", "violet_ink",
                 "A design choice we made and wrote down (the decision log says why). It may be built; the status band says how far."),
    "TESTED": ("green_fill", "green_edge", "green_ink", "Built, run, and checked against evidence."),
    "PLANNED": ("stone_fill", "stone_edge", "stone_ink", "On the plan; not built yet."),
    "PROPOSED": ("amber_fill", "amber_edge", "amber_ink", "Suggested; waiting for a decision."),
}
EVIDENCE = ("OBSERVED", "DERIVED", "ASSUMED", "DESIGNED")
STATUSES = ("TESTED", "PLANNED", "PROPOSED")

# ----------------------------------------------------------------------------- fonts and glyphs
_FONT_CANDIDATES = [
    # (regular, bold, italic, bold italic, mono, mono bold)
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
     "/System/Library/Fonts/Supplemental/Arial Italic.ttf", "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
     "/System/Library/Fonts/Supplemental/Courier New.ttf", "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
]
_SYMBOL_CANDIDATES = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/Library/Fonts/Arial Unicode.ttf"]

# Characters no font here can draw, with a safe stand-in. Anything else missing stops the build.
REPLACE = {
    "️": "", "︎": "", "‍": "", "​": "",   # emoji variation selectors, zero-width joiners
    " ": " ",
}


class GlyphError(ValueError):
    pass


class _Fonts:
    """Registers the fonts once and answers 'can this font draw that character?'."""

    def __init__(self):
        self.mode = None
        self._sym_cmap = None
        for reg, bold, ital, boldit, mono, monob in _FONT_CANDIDATES:
            if all(Path(p).exists() for p in (reg, bold, ital, boldit, mono, monob)):
                for name, path in (("HandinSans", reg), ("HandinSans-Bold", bold), ("HandinSans-Italic", ital),
                                   ("HandinSans-BoldItalic", boldit), ("HandinMono", mono), ("HandinMono-Bold", monob)):
                    pdfmetrics.registerFont(TTFont(name, path))
                pdfmetrics.registerFontFamily("HandinSans", normal="HandinSans", bold="HandinSans-Bold",
                                              italic="HandinSans-Italic", boldItalic="HandinSans-BoldItalic")
                pdfmetrics.registerFontFamily("HandinMono", normal="HandinMono", bold="HandinMono-Bold",
                                              italic="HandinMono", boldItalic="HandinMono-Bold")
                self.sans, self.bold, self.italic, self.mono = "HandinSans", "HandinSans-Bold", "HandinSans-Italic", "HandinMono"
                faces = [pdfmetrics.getFont(n).face.charToGlyph for n in ("HandinSans", "HandinSans-Bold", "HandinSans-Italic")]
                self._sans_cmap = set(faces[0]) & set(faces[1]) & set(faces[2])
                self._mono_cmap = set(pdfmetrics.getFont("HandinMono").face.charToGlyph)
                self.mode = Path(reg).stem
                break
        if self.mode is None:  # last resort: the 14 built-in fonts, which only draw cp1252
            self.sans, self.bold, self.italic, self.mono = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"
            self._sans_cmap = self._mono_cmap = None
            self.mode = "builtin-cp1252"
        self._sym_path = next((p for p in _SYMBOL_CANDIDATES if Path(p).exists()), None)

    def has(self, ch, mono=False):
        if ch in "\n\t\x00":   # \x00 marks code-span placeholders inside rich()
            return True
        cmap = self._mono_cmap if mono else self._sans_cmap
        if cmap is None:
            try:
                ch.encode("cp1252")
                return True
            except UnicodeEncodeError:
                return False
        return ord(ch) in cmap

    def sym_has(self, ch):
        """True if the symbol fallback font can draw ch (registered lazily: it is a 20 MB font)."""
        if not self._sym_path:
            return False
        if self._sym_cmap is None:
            pdfmetrics.registerFont(TTFont("HandinSym", self._sym_path))
            self._sym_cmap = set(pdfmetrics.getFont("HandinSym").face.charToGlyph)
        return ord(ch) in self._sym_cmap


FONTS = _Fonts()


def _glyph_fix(text, mono=False, where="", allow_sym=True):
    """Return text (already XML-escaped) with every character drawable: kept, wrapped in the symbol
    font, or replaced from REPLACE. Raise GlyphError naming the characters that cannot be drawn."""
    out, bad = [], set()
    for ch in text:
        if FONTS.has(ch, mono):
            out.append(ch)
        elif ch in REPLACE:
            out.append(REPLACE[ch])
        elif allow_sym and FONTS.sym_has(ch):
            out.append(f'<font name="HandinSym">{ch}</font>')
        else:
            bad.add(ch)
    if bad:
        names = ", ".join(f"U+{ord(c):04X} {c!r}" for c in sorted(bad))
        raise GlyphError(f"cannot draw {names} (font mode {FONTS.mode}){' in ' + where if where else ''}: {text[:80]!r}. "
                         f"Rewrite it, or add a stand-in to style.REPLACE.")
    return "".join(out)


def plain_safe(text, where="page furniture"):
    """For canvas.drawString text (header, footer): no markup and no font switching possible."""
    return _glyph_fix(text, where=where, allow_sym=False)


# ----------------------------------------------------------------------------- inline markup
_ALLOWED_TAG = re.compile(r"</?(?:b|i|u|br|font|span|super|sup|sub|strike|link|a|seq|seqreset)(?:\s[^<>]*)?/?>", re.I)
_ENTITY = re.compile(r"&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);")
_CODE = re.compile(r"`([^`\n]+)`")
_PILL = re.compile(r"\[\[([A-Z]+)\]\]")
_LINK = re.compile(r"\[([^\]\[]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
_ITAL = re.compile(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", re.S)


def _escape_piece(s):
    parts, last = [], 0
    for m in _ENTITY.finditer(s):
        parts.append(html.escape(s[last:m.start()], quote=False))
        parts.append(m.group(0))
        last = m.end()
    parts.append(html.escape(s[last:], quote=False))
    return "".join(parts)


def pill_markup(label, size=6.8):
    """Inline pill for use inside a paragraph or table cell."""
    if label not in PILLS:
        raise KeyError(f"unknown pill [[{label}]]; use one of {', '.join(PILLS)}")
    fill, _edge, ink, _ = PILLS[label]
    return (f'<font name="{FONTS.bold}" size="{size}" color="{HEX[ink]}" backColor="{HEX[fill]}">'
            f'&nbsp;{label}&nbsp;</font>')


def rich(text, where=""):
    """Turn the light inline markup into ReportLab paragraph markup, escaping stray < > & and checking glyphs."""
    text = str(text)
    codes = []

    def _code(m):
        codes.append(f'<font name="{FONTS.mono}">{_glyph_fix(_escape_piece(m.group(1)), mono=True, where=where)}</font>')
        return f"\x00{len(codes) - 1}\x00"

    text = _CODE.sub(_code, text)
    pieces, last = [], 0
    for m in _ALLOWED_TAG.finditer(text):
        pieces.append(_glyph_fix(_escape_piece(text[last:m.start()]), where=where))
        pieces.append(m.group(0))
        last = m.end()
    pieces.append(_glyph_fix(_escape_piece(text[last:]), where=where))
    out = "".join(pieces)
    out = _PILL.sub(lambda m: pill_markup(m.group(1)), out)
    out = _LINK.sub(lambda m: f'<link href="{m.group(2)}" color="{HEX["teal"]}">{m.group(1)}</link>', out)
    out = _BOLD.sub(r"<b>\1</b>", out)
    out = _ITAL.sub(r"<i>\1</i>", out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], out)
    if _PILL.fullmatch(text.strip()):
        out += "&nbsp;"   # a full-size space so a pill alone in a cell sits on the same baseline as its row
    return out.replace("\n", "<br/>")


# ----------------------------------------------------------------------------- paragraph styles
def _ps(name, size, leading, color=INK, font=None, **kw):
    return ParagraphStyle(name=name, fontName=font or FONTS.sans, fontSize=size, leading=leading,
                          textColor=color, alignment=TA_LEFT, **kw)


ST = {
    "kicker": _ps("kicker", 11, 15, TEAL, FONTS.bold, spaceAfter=10),
    "title": _ps("title", 28, 33, NAVY, FONTS.bold, spaceAfter=14),
    "subtitle": _ps("subtitle", 12.5, 18, GRAY, spaceAfter=14),
    "chap_label": _ps("chap_label", 10.5, 14, TEAL, FONTS.bold, spaceBefore=18, spaceAfter=2),
    "h1": _ps("h1", 20, 25, NAVY, FONTS.bold, spaceAfter=12),
    "h2": _ps("h2", 12, 15.5, TEAL, FONTS.bold, spaceBefore=10, spaceAfter=5),
    "h3": _ps("h3", 10, 13, NAVY, FONTS.bold, spaceBefore=6, spaceAfter=3),
    "body": _ps("body", 9.5, 13.2, spaceAfter=8, allowWidows=0),
    "small": _ps("small", 8.2, 11, spaceAfter=6),
    "cell": _ps("cell", 8.1, 10.6),
    "head": _ps("head", 8.4, 11.2, colors.white, FONTS.bold),
    "caption": _ps("caption", 8.5, 11.5, INK, spaceBefore=5, spaceAfter=1),
    "source": _ps("source", 7.4, 9.8, GRAY, spaceAfter=10),
    "code": _ps("code", 8.0, 10.8, INK, FONTS.mono, spaceAfter=8),
    "bullet": _ps("bullet", 9.5, 13.2, spaceAfter=2),
    "box": _ps("box", 9.3, 12.9, spaceAfter=3),
    "box_title": _ps("box_title", 9.5, 13, NAVY, FONTS.bold, spaceAfter=2),
}


def para(text, style="body", where=""):
    return Paragraph(rich(text, where), ST[style] if isinstance(style, str) else style)


def spacer(h=6):
    return Spacer(1, h)


# ----------------------------------------------------------------------------- lists
def bullets(items, numbered=False, style="bullet"):
    flow = [ListItem(para(it, style), leftIndent=14, value=(i + 1) if numbered else None) for i, it in enumerate(items)]
    kw = dict(bulletType="1", bulletFormat="%s.") if numbered else dict(bulletType="bullet", start="•")
    return ListFlowable(flow, leftIndent=14, bulletFontName=FONTS.sans, bulletFontSize=9, bulletColor=TEAL,
                        spaceAfter=8, **kw)


# ----------------------------------------------------------------------------- tables
def table(head, rows, widths=None, pad=5, keep_ends=True, font=None, zebra=True):
    """Navy header row, zebra body rows, wrapped cells. widths are relative weights (any units);
    they are scaled to the full 504 pt frame. Cells accept the inline markup."""
    ncol = len(head) if head else len(rows[0])
    for r in rows:
        if len(r) != ncol:
            raise ValueError(f"table row has {len(r)} cells, header has {ncol}: {r}")
    w = widths or [1] * ncol
    if len(w) != ncol:
        raise ValueError(f"{len(w)} widths for {ncol} columns")
    w = [FRAME_W * x / sum(w) for x in w]
    cell = ST["cell"] if font is None else ParagraphStyle("cellx", parent=ST["cell"], fontSize=font, leading=font * 1.3)
    data = []
    if head:
        data.append([Paragraph(rich(h), ST["head"]) for h in head])
    data += [[Paragraph(rich(c), cell) for c in r] for r in rows]
    t = Table(data, colWidths=w, repeatRows=1 if head else 0, hAlign="LEFT", spaceAfter=9)
    first = 1 if head else 0
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if head:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("LINEBELOW", (0, 0), (-1, 0), .5, NAVY)]
    if zebra:
        cmds.append(("ROWBACKGROUNDS", (0, first), (-1, -1), [colors.white, LIGHT]))
    cmds.append(("LINEBELOW", (0, -1), (-1, -1), .5, C["rule"]))
    last = len(data) - 1
    if keep_ends and last - first >= 3:  # never leave one body row alone at a page break
        cmds += [("NOSPLIT", (0, first), (-1, first + 1)), ("NOSPLIT", (0, last - 1), (-1, last))]
    t.setStyle(TableStyle(cmds))
    return t


# ----------------------------------------------------------------------------- boxes
CALLOUTS = {
    # kind: (title, fill, border, left bar, title colour)
    "note": ("Note", "light", "teal", None, "navy"),
    "warning": ("Watch out", "amber_fill", "amber_edge", "amber_edge", "amber_ink"),
    "how": ("How we know", "white", "navy", "teal", "navy"),
    "key": ("Key point", "navy", "navy", None, "white"),
}


def _box(paragraphs, fill, border, bar=None, bw=.6, space_before=2):
    t = Table([[paragraphs]], colWidths=[FRAME_W], spaceBefore=space_before, spaceAfter=9)
    cmds = [("BACKGROUND", (0, 0), (-1, -1), C[fill]), ("BOX", (0, 0), (-1, -1), bw, C[border]),
            ("LEFTPADDING", (0, 0), (-1, -1), 14 if bar else 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]
    if bar:
        cmds.append(("LINEBEFORE", (0, 0), (0, -1), 4, C[bar]))
    t.setStyle(TableStyle(cmds))
    return t


def callout(kind, text, title=None):
    """kind: note | warning | how ("How we know") | key. text may be a string or a list of strings (paragraphs)."""
    if kind not in CALLOUTS:
        raise KeyError(f"callout kind {kind!r}; use one of {', '.join(CALLOUTS)}")
    default, fill, border, bar, tcol = CALLOUTS[kind]
    body = ParagraphStyle(f"box_{kind}", parent=ST["box"], textColor=colors.white if kind == "key" else INK)
    head = ParagraphStyle(f"boxt_{kind}", parent=ST["box_title"], textColor=C[tcol])
    texts = [text] if isinstance(text, str) else list(text)
    ps = [Paragraph(rich(title or default), head)] + [Paragraph(rich(x), body) for x in texts]
    return _box(ps, fill, border, bar)


def gate(name, rows, status=None):
    """Box that closes a chapter: 'Gate: <name>' then (label, text) rows such as
    ('Required evidence', ...), ('Result', ...), ('If it fails', ...). status adds a pill."""
    title = f"Gate: {name}" + (f"  [[{status}]]" if status else "")
    ps = [Paragraph(rich(title), ST["box_title"])]
    ps += [Paragraph(rich(f"**{lab}:** {txt}"), ST["box"]) for lab, txt in rows]
    return _box(ps, "light", "navy", bar="teal", space_before=4)


def status_band(status, text):
    """Full-width band: coloured status label on the left, the statement on the right."""
    if status not in PILLS:
        raise KeyError(f"unknown status {status!r}")
    fill, edge, ink, _ = PILLS[status]
    lab = Paragraph(f'<font name="{FONTS.bold}" color="{HEX[ink]}">{status}</font>',
                    ParagraphStyle("band_l", parent=ST["cell"], fontSize=8.6, leading=11))
    t = Table([[lab, Paragraph(rich(text), ST["box"])]], colWidths=[78, FRAME_W - 78], spaceAfter=8, spaceBefore=2)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), C[fill]), ("BACKGROUND", (1, 0), (1, 0), colors.white),
                           ("BOX", (0, 0), (-1, -1), .8, C[edge]), ("LINEAFTER", (0, 0), (0, 0), .8, C[edge]),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def pill_row(labels, gap=6):
    """A row of pills as small boxed cells, left aligned (for a legend or a 'this section is' strip)."""
    cells, widths, cmds = [], [], [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]
    sty = ParagraphStyle("pill", parent=ST["cell"], fontName=FONTS.bold, fontSize=7.4, leading=9, alignment=1)
    for i, lab in enumerate(labels):
        if lab not in PILLS:
            raise KeyError(f"unknown pill {lab!r}")
        fill, edge, ink, _ = PILLS[lab]
        col = 2 * i
        cells.append(Paragraph(f'<font color="{HEX[ink]}">{lab}</font>', sty))
        widths.append(pdfmetrics.stringWidth(lab, FONTS.bold, 7.4) + 16)
        cmds += [("BACKGROUND", (col, 0), (col, 0), C[fill]), ("BOX", (col, 0), (col, 0), .7, C[edge])]
        if i < len(labels) - 1:
            cells.append("")
            widths.append(gap)
    t = Table([cells], colWidths=widths, hAlign="LEFT", spaceAfter=8)
    t.setStyle(TableStyle(cmds))
    return t


def pill_legend(labels=EVIDENCE + STATUSES):
    """Two-column table: pill, meaning. The standard key for evidence labels and status bands."""
    rows = [(f"[[{lab}]]", PILLS[lab][3]) for lab in labels]
    return table(["Label", "Meaning"], rows, widths=[90, 414])


# ----------------------------------------------------------------------------- code, figures
def code(text):
    """Monospaced block, kept on one page (keep code blocks short)."""
    x = XPreformatted(_glyph_fix(_escape_piece(text.rstrip("\n")), mono=True, where="code block"), ST["code"])
    return _box([x], "light", "rule", bw=.5)


class FigureCounter:
    def __init__(self):
        self.n = 0


def figure(path, caption, source, width=None, max_height=430, number=None, root=None):
    """PNG/JPG at full frame width (or `width` pt), aspect kept, capped at `max_height` pt,
    with a hairline frame, 'Figure N. caption' and a gray 'Source: ...' line. Kept on one page."""
    p = Path(path)
    if not p.is_absolute() and root:
        p = Path(root) / p
    if not p.exists():
        raise FileNotFoundError(f"figure not found: {p}")
    iw, ih = ImageReader(str(p)).getSize()
    w = min(width or FRAME_W, FRAME_W) - 2   # 1 pt frame each side
    h = w * ih / iw
    if h > max_height:
        h = max_height
        w = h * iw / ih
    img = Image(str(p), width=w, height=h)
    frame = Table([[img]], colWidths=[w + 2], hAlign="LEFT")
    frame.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), .5, C["rule"]), ("LEFTPADDING", (0, 0), (-1, -1), 1),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (-1, -1), 1),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    lab = f"**Figure {number}.** " if number is not None else ""
    return KeepTogether([frame, para(lab + caption, "caption"), para("Source: " + source, "source")])


# ----------------------------------------------------------------------------- cover
def cover(kicker, title, subtitle, is_=(), is_not=(), how_to_read=None, lead=None):
    """Cover flowables: kicker, title, subtitle, optional lead box (list of (label, text)),
    the 'What this is / What this is not' table and a 'How to read this' paragraph."""
    out = [para(kicker, "kicker"), para(title, "title"), para(subtitle, "subtitle")]
    if lead:
        ps = []
        for lab, txt in lead:
            ps.append(Paragraph(rich(f"**{lab}**"), ST["box_title"]))
            ps.append(Paragraph(rich(txt), ST["box"]))
        out.append(_box(ps, "light", "teal"))
    if is_ or is_not:
        def cell(items):
            return "<br/>".join(f"• {x}" for x in items)
        out.append(table(["What this is", "What this is not"], [(cell(is_), cell(is_not))], widths=[1, 1], pad=7))
    if how_to_read:
        out.append(para(f"**How to read this.** {how_to_read}"))
    return out


# ----------------------------------------------------------------------------- chapters and page furniture
class ChapterMark(Flowable):
    """Zero-size marker: the running header names the chapter in force at the top of each page."""

    def __init__(self, label):
        super().__init__()
        self.label = label

    def wrap(self, aW, aH):
        return 0, 0

    def draw(self):
        f = getattr(self, "_frame", None)
        if f is not None and getattr(f, "_atTop", False):
            self.canv._hd_chap = self.label
        else:
            self.canv._hd_next = self.label


def chapter_start(label, title, key=None, new_page=False, min_space=210):
    """Chapter label (teal, e.g. '01 · SUMMARY') + big navy title. Starts a new page when asked,
    or when less than `min_space` pt is left (so a chapter never opens at a page foot)."""
    from reportlab.platypus import PageBreak
    out = [PageBreak()] if new_page else [CondPageBreak(min_space)]
    out.append(ChapterMark(f"{label} · {title}"))
    out.append(para(label, "chap_label"))
    t = para(title, "h1")
    t._hd_key = key
    out.append(t)
    return out


def heading(text, level=2, min_space=96):
    """Section heading with a conditional page break so it is never stranded at a page foot."""
    return [CondPageBreak(min_space), para(text, f"h{level}")]


def make_canvas(header_left, footer_left, footer_flag=None):
    """Canvas class drawing the BlueJay header (title left, chapter right, teal rule) and footer
    (text left, 'n / total' right). footer_flag, if given, is printed in amber (e.g. provisional numbers)."""
    header_left = plain_safe(header_left)
    footer_left = plain_safe(footer_left)
    footer_flag = plain_safe(footer_flag) if footer_flag else None

    class HandinCanvas(rl_canvas.Canvas):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self._states = []

        def showPage(self):
            self._states.append(dict(self.__dict__))
            if getattr(self, "_hd_next", None):
                self._hd_chap, self._hd_next = self._hd_next, None
            self._startPage()

        def save(self):
            total = len(self._states)
            for st in self._states:
                self.__dict__.update(st)
                top = PAGE_H - 26
                self.setStrokeColor(TEAL)
                self.setLineWidth(1.2)
                self.line(MARGIN_L, top - 12, PAGE_W - MARGIN_R, top - 12)
                self.setFont(FONTS.sans, 7.8)
                self.setFillColor(GRAY)
                self.drawString(MARGIN_L, top, header_left)
                chap = st.get("_hd_chap")
                if chap and self._pageNumber > 1:
                    self.drawRightString(PAGE_W - MARGIN_R, top, plain_safe(chap.upper()))
                self.setLineWidth(.6)
                self.line(MARGIN_L, 43, PAGE_W - MARGIN_R, 43)
                self.drawString(MARGIN_L, 29, footer_left)
                if footer_flag:
                    x = MARGIN_L + pdfmetrics.stringWidth(footer_left, FONTS.sans, 7.8) + 8
                    self.setFont(FONTS.bold, 7.8)
                    self.setFillColor(C["amber_edge"])
                    self.drawString(x, 29, footer_flag)
                    self.setFont(FONTS.sans, 7.8)
                    self.setFillColor(GRAY)
                self.drawRightString(PAGE_W - MARGIN_R, 29, f"{self._pageNumber} / {total}")
                super().showPage()
            super().save()

    return HandinCanvas


# ----------------------------------------------------------------------------- post-build check
def check_pdf(path, tol=0.6):
    """Open the finished PDF (needs pymupdf) and return a list of problems:
    text or images outside the 504 x 680 pt body frame (header/footer bands excepted),
    replacement characters, and pages with no body content. Returns None if pymupdf is missing."""
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            return None
    problems = []
    x0, x1 = MARGIN_L - tol, PAGE_W - MARGIN_R + tol
    y0, y1 = MARGIN_T - tol, PAGE_H - MARGIN_B + tol      # top-left origin in pymupdf
    with pymupdf.open(str(path)) as doc:
        for i, page in enumerate(doc, 1):
            body = 0
            for b in page.get_text("dict")["blocks"]:
                for line in b.get("lines", []):
                    for sp in line["spans"]:
                        if not sp["text"].strip():
                            continue
                        bx0, by0, bx1, by1 = sp["bbox"]
                        if by1 < MARGIN_T - 8 or by0 > PAGE_H - 50:   # header / footer band
                            continue
                        body += 1
                        if "�" in sp["text"]:
                            problems.append(f"p{i}: replacement character in {sp['text'][:40]!r}")
                        if bx0 < x0 or bx1 > x1 or by0 < y0 - 3 or by1 > y1 + 3:
                            problems.append(f"p{i}: text outside frame {tuple(round(v) for v in sp['bbox'])}: {sp['text'][:40]!r}")
            for im in page.get_image_info():
                bx0, by0, bx1, by1 = im["bbox"]
                body += 1
                if bx0 < x0 or bx1 > x1 or by0 < y0 or by1 > y1:
                    problems.append(f"p{i}: image outside frame {tuple(round(v) for v in im['bbox'])}")
            if body == 0:
                problems.append(f"p{i}: page has no body content (blank page)")
    return problems


# ----------------------------------------------------------------------------- self-test
def _selftest():
    import tempfile
    from reportlab.platypus import SimpleDocTemplate
    print("font mode:", FONTS.mode)
    s = rich("FAERS → signal · PRR ≥ 2 ≤ x — ok ✓ **bold** *ital* `code →` [[OBSERVED]] a < b & c")
    assert "HandinSym" in s or FONTS.mode == "builtin-cp1252", s   # the check mark needs the symbol font
    assert "&lt; b &amp; c" in s and "<b>bold</b>" in s and "<i>ital</i>" in s, s
    try:
        rich("pin \U0001F4CD")
        raise AssertionError("emoji should fail loudly")
    except GlyphError as e:
        print("emoji refused as expected:", str(e)[:70], "...")
    out = Path(tempfile.gettempdir()) / "handin_glyph_test.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=letter)
    doc.build([para("Glyph test: FAERS → signal · PRR ≥ 2 · ≤ · ≈ · × · ✓ · ✗ · — – “quoted”"),
               para("Pills inline: [[OBSERVED]] [[DERIVED]] [[ASSUMED]] [[DESIGNED]] [[TESTED]] [[PLANNED]] [[PROPOSED]]")])
    try:
        import pymupdf
        with pymupdf.open(str(out)) as d:
            txt = d[0].get_text()
            fonts = sorted({f[3] for f in d[0].get_fonts()})
        for ch in "→≥≤✓·":
            assert ch in txt, f"{ch!r} not in extracted text"
        print("glyphs extracted back from the PDF: OK; fonts embedded:", ", ".join(fonts))
    except ImportError:
        print("pymupdf missing: PDF written but not read back")
    print("wrote", out)


if __name__ == "__main__":
    _selftest()
