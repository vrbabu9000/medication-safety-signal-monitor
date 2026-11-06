"""Hand-in #2: the one-page architecture note (brief section 4).

Builds, in order:
  1. Diagram 38 (data flow + ontology on one canvas, sized for print):
       docs/diagrams/drawio/38-handin-architecture-onepage-v2.drawio  (open in draw.io; File > Export as > VSDX)
       docs/diagrams/png/38-handin-architecture-onepage-v2.png
       docs/diagrams/pdf/38-handin-architecture-onepage-v2.pdf
     (v2, 2026-11-06: AI box shows the D041 v2 scope, 5 labels; v1 files stay on disk.)
  2. The note itself, exactly one page, US Letter landscape:
       docs/11-handin/architecture-note/architecture-note.pdf
       docs/11-handin/architecture-note/architecture-note.png   (preview of the page, 150 dpi)

Run from the project root:
    .venv/bin/python docs/11-handin/architecture-note/architecture_note.py

Numbers: every number comes from docs/11-handin/numbers.json through N() below (a missing key stops the build).
Style: tools/handin/style.py (palette, fonts, glyph check) and tools/handin/drawio.py (diagram + layout check).
The script fails if the page content does not fit on one page, if any text leaves the page box,
or if the PDF has more than one page.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools/handin"))

import drawio as DIO  # noqa: E402
import style as S  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import landscape, letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.platypus import Frame, KeepInFrame, Paragraph, Spacer, Table, TableStyle  # noqa: E402

NUMBERS = json.loads((ROOT / "docs/11-handin/numbers.json").read_text())
DIAGRAM = "38-handin-architecture-onepage-v2"
OUT_PDF = HERE / "architecture-note.pdf"
OUT_PNG = HERE / "architecture-note.png"


def N(key, spec=None):
    """Look a number up in numbers.json by dotted path; integers get thousands separators."""
    cur = NUMBERS
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise SystemExit(f"numbers.json has no key {key!r}")
        cur = cur[part]
    if cur is None:
        raise SystemExit(f"numbers.json key {key!r} is null")
    if spec:
        return format(cur, spec)
    if isinstance(cur, int):
        return f"{cur:,}"
    return str(cur)


# ============================================================================ 1. diagram 38
def build_diagram():
    # Slightly larger sub-text and edge labels than the default: this diagram is printed at ~0.66 scale.
    DIO.SUB_SIZE, DIO.EDGE_SIZE = 12, 11
    W, H = 740, 678
    d = DIO.Diagram(DIAGRAM, W, H, title="Architecture on one page: data flow + ontology (pilot, 13 drugs)")

    # ---------------------------------------------------------------- part 1: data flow
    d.group("g_flow", 4, 4, 732, 358, "1 · Data flow: public sources → Data/raw → Data/clean → Data/curated")
    C1, C2, C3, C4 = 14, 212, 368, 562
    W1, W2, W3, W4 = 176, 138, 172, 170
    r = [34, 102, 170, 238]        # row tops (h 58, gap 10)
    h = 58

    d.box("dm", C1, r[0], W1, h, "DailyMed", ["labels, SPL XML", "raw_dailymed_spl"], kind="source")
    d.box("faers", C1, r[1], W1, h, "FAERS", [f"{N('scope.faers_quarters')}", "raw_faers_quarter_*"], kind="source")
    d.box("rx", C1, r[2], W1, h, "RxNorm", ["RxNav API", "raw_rxnorm_*"], kind="source")
    d.box("ofda", C1, r[3], W1, h, "openFDA", ["recalls, Drugs@FDA, NDC", "raw_openfda_*"], kind="source")

    d.box("ident", C2, r[0], W2, r[3] + h - r[0], "Drug identity",
          ["clean_drug_identity", "", "resolved ONCE:", "drug names, salts,", "products, NDC", "packages", "→ ingredient RxCUI",
           "", f"{N('scope.drugs_formulary')} formulary drugs", "(D020, D027)"], kind="pipeline", sw=2.5)

    d.box("labels", C3, r[0], W3, h, "clean_labels", [f"{N('labels.total')} label versions", "safety sections"], kind="pipeline")
    d.box("cfaers", C3, r[1], W3, h, "clean_faers", [f"{N('faers.cases_current')} current cases", "rules D021-D023 v2"], kind="pipeline")
    d.box("incr", C3, r[2], W3, h, "FAERS incremental", ["= full rebuild, row by row", "not used yet: slower"],
          kind="pipeline", dashed=True)
    d.box("recalls", C3, r[3], W3, h, "clean_recalls", [f"{N('recalls.total')} · {N('recalls.active')} active",
                                                       "NDC → product match"], kind="pipeline")

    d.box("ai", C4, r[0], W4, h, "AI label extraction", [f"Claude via AIP · {N('ai.pilot_labels')} labels",
                                                          f"{N('ai.grounded')}/{N('ai.reactions')} quotes grounded"],
          kind="ai", dashed=True)
    d.box("sig", C4, r[1], W4, r[2] + h - r[1], "ontology_signals",
          ["PRR + Evans rule", "label check:", "AI → text → synonyms", f"{N('signals.total')} signals",
           f"{N('signals.ranked')} ranked"], kind="pipeline")
    d.box("syn", C4, r[3], W4, h, "label_synonyms", [f"{N('synonyms.version')}: {N('synonyms.rows')} rows",
                                                     "band set by a person"], kind="pipeline")

    d.box("mon", C1, 306, C2 + W2 - C1, 46, "monitoring", [f"{N('monitoring.checks_per_build')} checks per build + "
                                                          f"{N('monitoring.data_health_checks')} Data Health checks"],
          kind="pipeline", dashed=True)
    d.box("chg", C3, 306, C4 + W4 - C3, 46, "ontology_changes",
          [f"{N('changes.total')} dated change events + as-of per source"], kind="pipeline", dashed=True)

    for s in ("dm", "faers", "rx", "ofda"):
        d.arrow(s, "ident")
    d.arrow("ident", "labels")
    d.arrow("ident", "cfaers")
    d.arrow("ident", "incr", dashed=True)
    d.arrow("ident", "recalls")
    d.arrow("labels", "ai")
    d.arrow("cfaers", "sig")
    d.arrow("ai", "sig")
    d.arrow("syn", "sig")
    d.arrow("recalls", "chg")

    # ---------------------------------------------------------------- part 2: ontology + app
    d.group("g_onto", 4, 374, 732, 258, "2 · Ontology: 10 object types backed by the datasets above; lines = link types")
    X = [14, 199, 384, 569]        # columns (w 157, gap 28)
    OW, OH = 157, 46
    Y = [404, 482, 560]            # rows (gap 32); cardinality is in diagram 31

    d.box("o_lr", X[0], Y[0], OW, OH, "Labeled Reaction", [f"{N('ai.reactions')} · AI term + quote"], kind="ai")
    d.box("o_label", X[1], Y[0], OW, OH, "Label", [f"{N('labels.total')} versions"], kind="ontology")
    d.box("o_prod", X[2], Y[0], OW, OH, "Product", ["application number"], kind="ontology")
    d.box("o_recall", X[3], Y[0], OW, OH, "Recall", [f"{N('recalls.total')} · {N('recalls.active')} active"], kind="ontology")

    d.box("o_stat", X[0], Y[1], OW, OH, "AE Stat", [f"{N('signals.ae_stats')} · a, b, c, d, PRR"], kind="ontology")
    d.box("o_sig", X[1], Y[1], OW, OH, "Signal", [f"{N('signals.total')} · {N('signals.ranked')} ranked"], kind="ontology")
    d.box("o_drug", X[2], Y[1], OW, OH, "Drug", [f"{N('scope.drugs_formulary')} · ingredient RxCUI"], kind="ontology", sw=2.5)
    d.box("o_chg", X[3], Y[1], OW, OH, "Change Event", [f"{N('changes.total')} · no link type"], kind="ontology")

    d.box("o_src", X[0], Y[2], OW, OH, "Source Status", ["4 sources · as-of date"], kind="ontology")
    d.box("o_tri", X[1], Y[2], OW, 60, "Triage Decision", ["create-only", "+ evaluation_id"], kind="ontology", sw=2.5)
    d.box("o_act", X[2], Y[2], OW, OH, "Action", ["Create Triage Decision"], kind="app")
    d.box("o_app", X[3], Y[2], OW, OH, "Workshop", [f"{N('app.pages')} pages + triage button"], kind="app")

    d.arrow("o_lr", "o_label", arrow=False)
    d.arrow("o_label", "o_prod", arrow=False)
    d.arrow("o_prod", "o_recall", arrow=False)
    d.arrow("o_prod", "o_drug", arrow=False)
    d.arrow("o_recall", "o_drug", arrow=False)
    d.arrow("o_sig", "o_drug", arrow=False)
    d.arrow("o_sig", "o_stat", arrow=False)
    d.arrow("o_stat", "o_drug", arrow=False, via=[(60, 466), (420, 466)])
    d.arrow("o_tri", "o_sig", arrow=False)
    d.arrow("o_act", "o_tri")
    d.arrow("o_app", "o_act")

    # ---------------------------------------------------------------- legend
    items = [("source", "source", False, 1), ("dataset", "pipeline", False, 1),
             ("dashed: incremental/cached", "pipeline", True, 1), ("AI step", "ai", False, 1),
             ("object type", "ontology", False, 1), ("thick: key or human input", "ontology", False, 2.5),
             ("app, Action", "app", False, 1)]
    x = 6
    for i, (text, kind, dashed, sw) in enumerate(items):
        w = int(DIO._tw(text, DIO.SUB_SIZE) * 1.12 + 2 * DIO.PAD + 2)
        d.box(f"leg{i}", x, 642, w, 30, "", [text], kind=kind, dashed=dashed, sw=sw)
        x += w + 5
    if x > W:
        raise SystemExit(f"legend too wide: {x} > {W}")
    d.save()
    return ROOT / "docs/diagrams/png" / f"{DIAGRAM}.png"


# ============================================================================ 2. the page
PAGE_W, PAGE_H = landscape(letter)          # 792 x 612 pt
ML, MR, MT, MB = 26, 26, 22, 20
DIAG_W = 464                                 # left column: the diagram
GAP = 16
COL_X = ML + DIAG_W + GAP                    # right column: decisions + not done
COL_W = PAGE_W - MR - COL_X

sans, bold = S.FONTS.sans, S.FONTS.bold
P_BODY = ParagraphStyle("nb", fontName=sans, fontSize=7.35, leading=9.05, textColor=S.INK)
P_DTITLE = ParagraphStyle("nt", fontName=bold, fontSize=8.1, leading=9.9, textColor=S.NAVY, spaceAfter=1.2)
P_H = ParagraphStyle("nh", fontName=bold, fontSize=9.6, leading=12, textColor=S.TEAL, spaceAfter=3)
P_BUL = ParagraphStyle("nbul", parent=P_BODY, leftIndent=7, bulletIndent=0, spaceAfter=1.0, bulletFontName=sans, bulletFontSize=7.35)
P_CAP = ParagraphStyle("ncap", fontName=sans, fontSize=6.9, leading=8.5, textColor=S.INK)
P_FOOT = ParagraphStyle("nfoot", fontName=sans, fontSize=6.9, leading=8.6, textColor=S.GRAY)
P_WHY = ParagraphStyle("nwhy", fontName=S.FONTS.italic, fontSize=7.0, leading=8.6, textColor=S.GRAY)
P_SUB = ParagraphStyle("nsub", fontName=sans, fontSize=8.0, leading=10, textColor=S.GRAY)


def para(text, style):
    return Paragraph(S.rich(text), style)


DECISIONS = [
    ("1", "Drug identity is resolved once, in the clean layer", "D020, D027",
     "one dataset, `clean_drug_identity`, maps every drug name, salt, product and NDC package to an exact "
     "ingredient RxCUI. Every later step joins it.",
     "counts belong to ingredients, labels and recalls to products.",
     "substring matching (\"morphine\" also hit apomorphine and diamorphine) added 50% false morphine rows "
     "(DQ34) [[OBSERVED]]"),
    ("2", "FAERS counts each current case once, suspects only", "D021, D022, D023 v2",
     "the latest case version wins and FDA deletes apply to all history; suspect drugs only, once per report; "
     "duplicate patients folded; reports listing 30+ drugs leave the main count.",
     "FAERS re-files and deletes cases; mass re-filings fake signals.",
     f"appending quarters gave +8.7% phantom rows (DQ36). Q2 replaced {N('faers.q2_cases_replaced')} cases and "
     f"deleted {N('faers.q2_cases_deleted')} [[OBSERVED]]"),
    ("3", "\"Not in label\" is a 3-step check, and the AI must quote", "D037, D041 v2, D043",
     "a FAERS term is in the label if (1) an AI term with a code-found quote matches it, else (2) its exact "
     "text is in a safety section, else (3) a person-banded synonym.",
     "each \"not in label\" names the label versions searched; each AI match quotes its passage.",
     f"{N('ai.grounded')}/{N('ai.reactions')} quotes grounded in {N('ai.pilot_labels')} labels; F1 {N('ai.gold_f1')} vs D015 target "
     f"{N('ai.d015_target_f1')} (35-item Claude key, {N('ai.v1_pilot.labels')} oxycodone labels, pharmacist pending); "
     f"no optic-nerve term in the 3 semaglutide labels; "
     f"synonyms + wider buckets: ranked {N('signals.ranked_history.step9')} at step 9 → {N('signals.ranked')} [[OBSERVED]]"),
    ("4", "Triage is its own write-back object; changes are dated", "D040, D042, D045",
     "a decision is its own object, made only by an Action, tied to the signal and its `evaluation_id` "
     "(a hash of the evidence). A change feed dates each signal, recall and label change.",
     "a status column on Signal would be wiped by the next rebuild; sources run on different clocks.",
     f"a decision survived a full rebuild (step 6 gate); {N('changes.total')} change events, "
     f"{N('changes.snapshot_diff_after_rebuild')} false ones after a rebuild [[OBSERVED]]"),
]

WHY_THESE = ("**Why these four:** each decides whether a flag can be trusted, and each answers one judging row: "
             "Architecture, Data judgment, AI reliability, Application. Runners-up: the full FAERS rebuild kept as the "
             "signal input (D044, O2) and the focus buckets (D016 v3).")

NOT_DONE = [
    "**No MedDRA licence** (the paid dictionary of reaction terms): keyword buckets (D016 v3) and a reviewed "
    "synonym table stand in.",
    f"**No causality, no patient data.** A signal = more reports than expected (Evans; D006) and not "
    f"in the label, or only possibly ({N('signals.possibly_in_label')}). {N('signals.ranked')} ranked = a review queue, not findings.",
    f"**Signals do not read incremental FAERS yet:** equal row for row, but {N('optimization.O2.incremental_add_q2_s')} s "
    f"vs {N('optimization.O2.full_rebuild_s')} s at 2 quarters (O2). Re-measure at 4+.",
    f"**AI reads only {N('ai.pilot_labels')} labels; no AI judge per signal,** until a pharmacist checks the answer key.",
    "**No ClinicalTrials.gov, OnSIDES, daily FAERS scraping or label-change backtest** (D031 cut list; D029).",
    "**No build schedule** (we refresh when a build runs), **per-user bookmark or live drift** yet (drift is a "
    "replay).",
]



def decision_block(num, title, ids, chose, why, evidence):
    badge = Table([[Paragraph(f'<font name="{bold}" color="white" size="8.5">{num}</font>',
                              ParagraphStyle("bd", fontName=bold, fontSize=8.5, leading=10, alignment=1))]],
                  colWidths=[13], rowHeights=[13])
    badge.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), S.NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    body = [para(title, P_DTITLE),
            para(f"**Chose** <font color=\"{S.HEX['gray']}\">({ids})</font>**:** {chose}", P_BODY),
            para(f"**Why:** {why}", P_BODY),
            para(f"**Evidence:** {evidence}", P_BODY)]
    t = Table([[badge, body]], colWidths=[17, COL_W - 17 - 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("LEFTPADDING", (1, 0), (1, 0), 4)]))
    return t


def rule(c, x0, x1, y, color=S.TEAL, w=1.0):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)


def build_page(png):
    c = rl_canvas.Canvas(str(OUT_PDF), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Architecture note: Medication Safety Signal Monitor")
    c.setAuthor("vrbabu9000")
    c.setSubject("Hand-in 2: one-page architecture note (Soragence technical build brief)")

    # ---------------------------------------------------------------- header
    top = PAGE_H - MT
    c.setFillColor(S.TEAL)
    c.setFont(bold, 7.6)
    c.drawString(ML, top - 7.6, S.plain_safe("HAND-IN 2 · ONE-PAGE ARCHITECTURE NOTE"))
    c.setFillColor(S.GRAY)
    c.setFont(sans, 7.6)
    c.drawRightString(PAGE_W - MR, top - 7.6,
                      S.plain_safe("Palantir Foundry + AIP · pilot as built · numbers captured 5-6 Nov 2026 · v1.1"))
    c.setFillColor(S.NAVY)
    c.setFont(bold, 15.5)
    c.drawString(ML, top - 26, S.plain_safe("Medication Safety Signal Monitor: how the data becomes a flag you can trust"))
    sub = para("Built for the hospital pharmacy safety officer's three morning questions: (1) adverse events the label does not "
               "mention, (2) active recalls, (3) what changed. Trust rule: every flag traces to its source: the label versions "
               "searched (DailyMed) and the FDA recall record open in one click; the FAERS case reports are reachable by "
               "query, not yet from her screen.", P_SUB)
    _, sh = sub.wrap(PAGE_W - ML - MR, 40)
    sub.drawOn(c, ML, top - 31 - sh)
    head_bottom = top - 31 - sh - 4
    rule(c, ML, PAGE_W - MR, head_bottom, S.TEAL, 1.2)

    # ---------------------------------------------------------------- footer (build facts)
    foot = para(
        f"**Build facts.** {N('scope.drugs_formulary')} drugs ({N('scope.opioids')} opioids + {N('scope.glp1')} GLP-1s) · "
        f"4 public sources (FAERS {N('scope.faers_quarters')}, DailyMed, openFDA, RxNorm) · "
        f"{N('faers.cases_current')} current FAERS cases · {N('labels.total')} label versions "
        f"({N('changes.label_version_effective')} carry an effective date) · "
        f"{N('recalls.total')} recalls ({N('recalls.active')} active) · {N('signals.total')} signals, {N('signals.ranked')} ranked · "
        f"10 object types, {N('ontology.link_types_mssm')} link types, 1 Action · Workshop {N('app.workshop_version')}, {N('app.pages')} pages · "
        f"{N('monitoring.checks_per_build')} monitoring checks per build. "
        f"Numbers: docs/11-handin/numbers.json (captured {N('_meta.captured_at')}). "
        "Detail: diagrams 30-38, reports R01–R09, docs/06-decisions/DECISIONS.md.", P_FOOT)
    fw, fh = foot.wrap(PAGE_W - ML - MR, 40)
    foot.drawOn(c, ML, MB)
    rule(c, ML, PAGE_W - MR, MB + fh + 3, S.C["rule"], 0.6)
    body_bottom = MB + fh + 9
    body_top = head_bottom - 7

    # ---------------------------------------------------------------- left: diagram + caption
    cap = para(
        "**Figure.** Four public sources land in Data/raw as received. Every drug name passes through one identity dataset, "
        "then clean, curated and the Ontology (Foundry's layer of objects and links the app reads). "
        "**Glossary:** FAERS = FDA adverse event reports · DailyMed = official labels (SPL = the label XML) · "
        "RxCUI = RxNorm drug ID · NDC = package code · PRR = proportional reporting ratio · "
        "Workshop = Foundry's app builder · Action = a form that writes to the Ontology.", P_CAP)

    def why_box(width):
        t = Table([[para(WHY_THESE, P_BODY)]], colWidths=[width])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), S.LIGHT), ("LINEBEFORE", (0, 0), (0, -1), 3, S.TEAL),
                               ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        return t

    from reportlab.lib.utils import ImageReader
    img = ImageReader(str(png))
    iw, ih = img.getSize()
    dw = DIAG_W
    for _ in range(4):        # caption and box are as wide as the diagram; settle the size
        _, ch = cap.wrap(dw, 80)
        why = why_box(dw)
        _, wh = why.wrap(dw, 200)
        avail_h = body_top - (body_bottom + ch + 4 + wh + 6)
        scale = min(DIAG_W / iw, avail_h / ih)
        dw = iw * scale
    dh = ih * scale
    c.drawImage(img, ML, body_top - dh, width=dw, height=dh)
    c.setStrokeColor(S.C["rule"])
    c.setLineWidth(0.5)
    c.rect(ML, body_top - dh, dw, dh, stroke=1, fill=0)
    cap.drawOn(c, ML, body_top - dh - 4 - ch)
    why.drawOn(c, ML, body_bottom)
    if body_top - dh - 4 - ch < body_bottom + wh + 2:
        raise SystemExit("left column: caption and 'why these four' box overlap")
    print(f"diagram on page: {dw:.0f} x {dh:.0f} pt (scale {dw / 740:.3f} of the 740 px canvas; "
          f"12 px text prints at {12 * dw / 740:.1f} pt)")

    # ---------------------------------------------------------------- right: decisions + not done
    flow = [para("Four decisions that mattered most", P_H)]
    for i, dec in enumerate(DECISIONS):
        flow.append(decision_block(*dec))
        flow.append(Spacer(1, 4))
    flow.append(Spacer(1, 1))
    flow.append(para("What we chose not to do", P_H))
    for b in NOT_DONE:
        flow.append(Paragraph(S.rich(b), P_BUL, bulletText="•"))
    frame = Frame(COL_X, body_bottom, COL_W, body_top - body_bottom, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0, showBoundary=0)
    used = 0
    for f in flow:
        _, fh2 = f.wrap(COL_W, 1000)
        used += fh2 + getattr(getattr(f, "style", None), "spaceAfter", 0)
    print(f"right column ({COL_W:.0f} pt wide): needs ~{used:.0f} pt, has {body_top - body_bottom:.0f} pt")
    left = list(flow)
    frame.addFromList(left, c)
    if left:
        raise SystemExit(f"right column overflows: {len(left)} flowable(s) did not fit on the page")
    c.showPage()
    c.save()


def check_one_page():
    import pymupdf
    problems = []
    with pymupdf.open(str(OUT_PDF)) as doc:
        if doc.page_count != 1:
            problems.append(f"{doc.page_count} pages, expected exactly 1")
        page = doc[0]
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for sp in line["spans"]:
                    if not sp["text"].strip():
                        continue
                    x0, y0, x1, y1 = sp["bbox"]
                    if x0 < ML - 1 or x1 > PAGE_W - MR + 1 or y0 < MT - 2 or y1 > PAGE_H - MB + 3:
                        problems.append(f"text outside the page box: {sp['text'][:40]!r} {tuple(round(v) for v in sp['bbox'])}")
                    if "�" in sp["text"]:
                        problems.append(f"replacement character in {sp['text'][:40]!r}")
        page.get_pixmap(dpi=150).save(str(OUT_PNG))
    return problems


if __name__ == "__main__":
    png = build_diagram()
    build_page(png)
    probs = check_one_page()
    for p in probs:
        print("PAGE", p)
    if probs:
        raise SystemExit(f"{len(probs)} problem(s)")
    print(f"ok: {OUT_PDF.relative_to(ROOT)} (1 page) + {OUT_PNG.relative_to(ROOT)}")
