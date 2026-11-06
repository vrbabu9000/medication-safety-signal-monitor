"""Editable draw.io versions (Visio-ready) of the three key hand-in diagrams (30 v3, 31 v2, 36 v3).

Writes, for each diagram:
  docs/diagrams/drawio/<name>.drawio            open in draw.io; File > Export as > VSDX for Visio
  docs/diagrams/drawio/preview/<name>.png|pdf   preview of the same layout (ReportLab, or the draw.io CLI if installed)

The rendered PNG/PDF used in reports come from the Mermaid sources with the same name
(docs/diagrams/src/<name>.mmd -> docs/diagrams/png|pdf via tools/render_diagrams.sh). The previews live in
drawio/preview/ so they never overwrite the Mermaid renders and do not enter diagram-book.pdf twice.

Run:  .venv/bin/python tools/handin/build_handin_diagrams.py
Numbers: as of 2026-11-06 (D041 v2: AI reads 5 labels, 745 / 745 grounded; duplicate Signal -> Drug link
deleted, 10 MSSM link types; Workshop v0.10.0); see docs/diagrams/README-handin.md for sources.
Older versions (30 v2, 31 v1, 36 v2) stay on disk; this script no longer writes them.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawio import DIAGRAMS, Diagram  # noqa: E402

OUT = DIAGRAMS / "drawio"
PREVIEW = OUT / "preview"


def save(d: Diagram):
    problems = d.check()
    for p in problems:
        print("DIAGRAM", d.name, p)
    if problems:
        raise SystemExit(f"{d.name}: {len(problems)} layout problem(s)")
    dio = d.write_drawio(OUT / f"{d.name}.drawio")
    PREVIEW.mkdir(parents=True, exist_ok=True)
    how = d.render(PREVIEW / f"{d.name}.png", PREVIEW / f"{d.name}.pdf", dio)
    print(f"{d.name}: {dio.relative_to(DIAGRAMS.parents[1])} + preview png/pdf ({how})")


def legend(d, y, items, x0=30, gap=14, h=36):
    """One row of small legend boxes: items = [(text, kind, dashed)]."""
    from drawio import SUB_SIZE, _tw  # noqa: PLC0415
    x = x0
    for i, (text, kind, dashed) in enumerate(items):
        w = int(_tw(text, 13, True) * 1.12 + 24)
        d.box(f"leg{i}", x, y, w, h, text, kind=kind, dashed=dashed, sw=2 if dashed else 1)
        x += w + gap
    return x


# ----------------------------------------------------------------------------------------------------- 30 data flow
def data_flow():
    d = Diagram("30-handin-data-flow-v3", 1760, 820, title="Data flow as built v3 (pilot, 13 drugs, 2026-11-06)")
    H = 80
    r = {0: 70, 1: 180, 2: 290, 3: 400, 4: 510}          # row tops
    C0, C1, C2, C3, C4, C5, C6 = 25, 245, 490, 755, 1005, 1270, 1515
    d.group("g_src", 15, 30, 200, 570, "Public sources")
    d.group("g_raw", 235, 30, 220, 570, "Data/raw")
    d.group("g_cln", 480, 30, 240, 570, "Data/clean")
    d.group("g_cur", 745, 30, 490, 570, "Data/curated + Data/monitoring")
    d.group("g_use", 1260, 30, 485, 570, "Ontology + Workshop")
    d.group("g_alert", 1260, 612, 485, 100, "Foundry Data Health (alerts)")
    d.group("g_leg", 15, 730, 1730, 72, "Legend")

    d.box("faers", C0, r[0], 180, H, "FAERS", ["quarterly files", "2026Q1 + Q2"], kind="source")
    d.box("rxnorm", C0, r[2], 180, H, "RxNorm", ["RxNav API"], kind="source")
    d.box("openfda", C0, r[3], 180, H, "openFDA", ["recalls · Drugs@FDA", "NDC"], kind="source")
    d.box("dailymed", C0, r[4], 180, H, "DailyMed", ["label SPL XML"], kind="source")

    d.box("rf", C1, r[0], 200, H, "raw_faers_quarter_*", ["37 files + manifest"], kind="pipeline")
    d.box("rrx", C1, r[2], 200, H, "raw_rxnorm_*", ["13 ingredients"], kind="pipeline")
    d.box("rof", C1, r[3], 200, H, "raw_openfda_*", ["930 · 663 · 1,824 rows"], kind="pipeline")
    d.box("rdm", C1, r[4], 200, H, "raw_dailymed_spl_*", ["1,321 labels", "O3 XML reuse: 2 downloads"],
          kind="pipeline", dashed=True, sw=2)

    d.box("ff", C2, r[0], 220, H, "clean_faers (full)", ["792,346 current cases", "feeds signals (D044)"], kind="pipeline")
    d.box("fi", C2, r[1], 220, H, "clean_faers_incremental", ["state + per-quarter log", "= full rebuild, row for row",
                                                               "replays on identity change"], kind="pipeline", dashed=True, sw=2)
    d.box("id", C2, r[2], 220, H, "clean_drug_identity", ["identity resolved ONCE", "39 names → 13 ingredients",
                                                          "658 products"], kind="pipeline", sw=2)
    d.box("rc", C2, r[3], 220, H, "clean_recalls", ["900 recalls · 126 active", "+ product match"], kind="pipeline")
    d.box("lb", C2, r[4], 220, H, "clean_labels", ["1,321 versions", "5,431 safety sections"], kind="pipeline")

    d.box("sy", C3, r[1], 220, H, "label_synonyms", ["syn_v2 · 258 reviewed rows"], kind="pipeline")
    d.box("obj", C3, r[3], 220, H, "ontology_objects", ["drugs · products · labels", "recalls · link tables"], kind="pipeline")
    d.box("ai", C3, r[4], 220, H, "AI label extraction", ["Sonnet 5.5, cached · 5 labels", "745 / 745 quotes grounded"],
          kind="ai", dashed=True, sw=2)

    d.box("sg", C4, r[1] - 5, 220, 90, "ontology_signals", ["reads FAERS, label sections,", "AI terms, synonyms",
                                                           "1,952 signals · 1,073 ranked"], kind="pipeline")
    d.box("ce", C4, r[3], 220, H, "ontology_changes", ["2,898 change events", "+ source as-of"], kind="pipeline",
          dashed=True, sw=2)
    d.box("mo", C4, r[4], 220, H, "monitoring", ["21 checks per build", "+ drift replay"], kind="pipeline", dashed=True, sw=2)

    d.box("on", C5, 175, 210, 415, "Ontology", ["10 MSSM object types:", "Drug · Product · Label", "Recall · Labeled Reaction",
                                              "AE Stat · Signal", "Change Event", "Source Status", "Triage Decision",
                                              "+ 10 MSSM link types"], kind="ontology")
    d.box("dh", C5, 640, 180, 60, "Data Health: 4 checks", ["build status + primary key"], kind="neutral")
    d.box("ws", C6, 190, 220, 110, "Workshop v0.10.0", ["MSSM Safety Officer", "0 Morning brief",
                                                         "1 Not in label + AI quotes", "2 Recalls · 3 What changed"],
          kind="app")
    d.box("ac", C6, r[3], 220, H, "Action", ["Create Triage Decision", "write-back: new object"], kind="ontology", sw=2)
    d.box("own", C6, 640, 220, 60, "Project owner", ["Foundry notification"], kind="app")

    # sources -> raw -> clean
    for s, t in (("faers", "rf"), ("rxnorm", "rrx"), ("openfda", "rof"), ("dailymed", "rdm"),
                 ("rf", "ff"), ("rrx", "id"), ("rof", "rc"), ("rdm", "lb")):
        d.arrow(s, t)
    d.arrow("rf", "fi", via=[(468, 100), (468, 220)])
    d.arrow("rof", "id", via=[(468, 430), (468, 345)])
    # identity, resolved once, used by every clean step and the objects
    d.arrow("id", "fi", dashed=True)
    d.arrow("id", "ff", via=[(737, 315), (737, 125)])
    d.arrow("id", "rc")
    d.arrow("id", "lb", via=[(737, 345), (737, 570)])
    d.arrow("id", "obj", via=[(745, 330), (745, 425)])
    # clean -> curated
    d.arrow("rc", "obj", via=[(745, 455)])
    d.arrow("lb", "ai", via=[(745, 530)])
    d.arrow("ff", "sg", via=[(988, 95), (988, 200)])
    d.arrow("sy", "sg")
    d.arrow("ai", "sg", via=[(995, 550), (995, 240)])
    d.arrow("ai", "mo")
    d.arrow("sg", "ce")
    d.arrow("obj", "ce")
    d.arrow("sg", "mo", dashed=True, via=[(1242, 255), (1242, 560)])
    d.arrow("sg", "dh", dashed=True, via=[(1250, 245), (1250, 670)])
    # curated -> Ontology -> Workshop
    d.arrow("sg", "on")
    d.arrow("ce", "on")
    d.arrow("obj", "on", via=[(865, 345)])
    d.arrow("ai", "on", via=[(880, 605), (1330, 605)])
    d.arrow("on", "ws")
    d.arrow("ws", "ac")
    d.arrow("ac", "on", dashed=True)
    d.arrow("dh", "own", label="alert")

    legend(d, 755, [("public source", "source", False), ("Foundry dataset", "pipeline", False),
                    ("incremental or cached (dashed)", "pipeline", True), ("AI step, cached", "ai", True),
                    ("Ontology", "ontology", False), ("Workshop / person alerted", "app", False)])
    save(d)


# ----------------------------------------------------------------------------------------------------- 31 ontology
def ontology():
    d = Diagram("31-handin-ontology-v2", 1500, 860, title="Ontology as built v2: 10 object types, 10 link types, one Action")
    W, H = 230, 92
    d.box("ac", 30, 30, W, 110, "Action", ["Create MSSM Triage Decision", "create-only", "officer: decision + rationale",
                                          "system: id, reviewer, time"], kind="app")
    d.box("td", 30, 230, W, H, "Triage Decision", ["key: decision_id (UUID)", "subject_key · evaluation_id",
                                                   "edits ON · Action only"], kind="ontology", sw=3)
    d.box("sg", 30, 470, W, H, "Signal", ["key: signal_key", "rxcui | reaction | rule", "1,952 · 1,073 ranked"], kind="ontology")
    d.box("st", 400, 470, W, H, "AE Stat", ["key: stat_key", "a, b, c, d · PRR · chi²", "14,921"], kind="ontology")
    d.box("dr", 400, 680, W, H, "Drug", ["key: ingredient_rxcui", "13 formulary ingredients"], kind="ontology")
    d.box("re", 770, 470, W, H, "Recall", ["key: recall_number", "900 · 126 active"], kind="ontology")
    d.box("pr", 770, 680, W, H, "Product", ["key: product_key", "= application number", "658"], kind="ontology")
    d.box("la", 1150, 680, W, H, "Label", ["key: label_key", "setid | version", "1,321"], kind="ontology")
    d.box("lr", 1150, 470, W, H, "Labeled Reaction", ["key: labeled_reaction_key", "AI term + exact quote",
                                                      "745 (5 labels read by AI)"], kind="ai")
    d.box("cap", 400, 250, 610, 110, "How to read this", ["counts = rows in the backing dataset (13 drugs, 2026-11-06)",
                                                       "many : 1 = a foreign key on the 'many' side",
                                                       "many : many = a link dataset (ontology_link_*)",
                                                       "plain lines: links have no direction"], kind="neutral")
    d.group("g_free", 400, 30, 610, 160, "No link types (filtered by drug name on screen)")
    d.box("ce", 420, 70, 270, 100, "Change Event", ["key: event_id (hash)", "2,898 at first build"], kind="ontology")
    d.box("ss", 715, 70, 270, 100, "Source Status", ["key: source", "4 sources, as-of dates"], kind="ontology")

    d.arrow("ac", "td", label="creates")
    d.arrow("td", "sg", label="many : 1 (subject_key)", arrow=False)
    d.arrow("sg", "st", label="many : 1", arrow=False)
    d.arrow("sg", "dr", label="many : 1", arrow=False, via=[(145, 726)])
    d.arrow("st", "dr", label="many : 1", arrow=False)
    d.arrow("re", "dr", label="many : many", arrow=False, via=[(700, 516), (700, 705)])
    d.arrow("re", "pr", label="many : many", arrow=False)
    d.arrow("dr", "pr", label="many : many", arrow=False)
    d.arrow("pr", "la", label="many : many", arrow=False, via=[(1145, 705)])
    d.arrow("pr", "la", label="1 ref. label : many", arrow=False, via=[(1145, 750)], id="ref")
    d.arrow("lr", "la", label="many : 1", arrow=False)

    d.group("g_leg", 30, 795, 1440, 56, "")
    legend(d, 808, [("object type", "ontology", False), ("object built by AI", "ai", False),
                    ("written by people (thick border)", "ontology", False), ("Action", "app", False)], x0=45)
    d.by_id["leg2"].sw = 3
    save(d)


# ----------------------------------------------------------------------------------------------------- 36 demo map
# v3 (2026-11-06): stop codes A0-A7 / H1-H15 and timings from docs/11-handin/demo/demo-navigation-guide.md
# (1,200 s in all); A4 now ends on the AI-quotes table. Same content as docs/diagrams/src/36-handin-demo-map-v3.mmd.
# The v1 and v2 .drawio files stay on disk.
DEMO_ROWS = [
    ("Part A · the safety officer's morning in the Workshop app (0:00–6:00)", [
        ("A0 · Her 3 questions", "0:00–1:30 · 90 s", "Deck slides 1–2", "Communication", "neutral"),
        ("A1 · Morning brief", "1:30–3:00 · 90 s", "Workshop · 3 cards", "Application · trust", "app"),
        ("A2 · One drug", "3:00–3:40 · 40 s", "Page 1 · semaglutide", "Application", "app"),
        ("A3 · Why NAION", "3:40–4:30 · 50 s", "Page 1 · evidence panel", "Application (trace)", "app"),
        ("A4 · Labels searched", "4:30–5:20 · 50 s", "3 labels → DailyMed → AI quotes", "Application · AI reliability", "app"),
        ("A5 · Triage this signal", "5:20–6:00 · 40 s", "open form → Cancel (default)", "Application · trust", "write"),
    ]),
    ("Part A ends (6:00–7:30) · Part H · under the hood begins (7:30–10:45)", [
        ("A6 · Recalls", "6:00–6:50 · 50 s", "Page 2 · 126 → openFDA · Class I", "Application · Data judgment", "app"),
        ("A7 · What changed", "6:50–7:30 · 40 s", "Page 3 · past month", "Application", "app"),
        ("H1 · Architecture", "7:30–8:30 · 60 s", "Slide 6 · diagram 38", "Architecture", "neutral"),
        ("H2 · Data Lineage", "8:30–9:30 · 60 s", "Foundry lineage, live", "Architecture", "pipeline"),
        ("H3 · Ontology picture", "9:30–10:15 · 45 s", "Slide 7 · diagram 31", "Architecture", "neutral"),
        ("H4 · Ontology Manager", "10:15–10:45 · 30 s", "MSSM Signal, live", "Architecture", "pipeline"),
    ]),
    ("Part H · under the hood (10:45–15:30)", [
        ("H5 · Object Explorer", "10:45–11:30 · 45 s", "NAION links, live", "Application · trace", "pipeline"),
        ("H6 · FAERS → signal", "11:30–12:30 · 60 s", "Slide 8 · diagram 32 v3", "Data judgment", "neutral"),
        ("H7 · Signal code", "12:30–12:50 · 20 s", "Code Repo (optional)", "Architecture", "pipeline"),
        ("H8 · Review queue", "12:50–13:30 · 40 s", "Slide 9", "Data judgment", "neutral"),
        ("H9 · AI reliability", "13:30–14:45 · 75 s", "Slide 10 (+ SQL)", "AI · Optimization", "neutral"),
        ("H10 · Monitoring", "14:45–15:30 · 45 s", "Slide 11 (+ SQL)", "AI · Data judgment", "neutral"),
    ]),
    ("Part H (cont.) · optimization, judgment, close (15:30–20:00)", [
        ("H11 · Optimization", "15:30–16:45 · 75 s", "Slide 12 · O1-O3", "Optimization", "neutral"),
        ("H12 · Incremental", "16:45–17:30 · 45 s", "Slide 13 (+ inc log)", "Optimization", "neutral"),
        ("H13 · Data judgment", "17:30–19:00 · 90 s", "Slide 14", "Data judgment", "neutral"),
        ("H14 · Another month", "19:00–19:40 · 40 s", "Slide 15", "Communication", "neutral"),
        ("H15 · Take away", "19:40–20:00 · 20 s", "Slide 16", "Communication", "neutral"),
    ]),
]


def demo_map():
    d = Diagram("36-handin-demo-map-v3", 1560, 660,
                title="Demo map v3: 23 stops, 1,200 s = 20 min (A0-A7 in the app, H1-H15 under the hood)")
    W, H, X0, GAP = 232, 82, 30, 22
    xs = [X0 + i * (W + GAP) for i in range(6)]
    gys = [20, 160, 300, 440]
    prev = None
    for r, (label, stops) in enumerate(DEMO_ROWS):
        gy = gys[r]
        d.group(f"g{r + 1}", 15, gy, 1530, 125, label)
        ids = []
        for c, (title, slot, screen, rubric, kind) in enumerate(stops):
            bid = title.split(" ")[0].lower()
            write = kind == "write"
            d.box(bid, xs[c], gy + 32, W, H, title, [slot, screen, rubric],
                  kind="ontology" if write else kind, sw=3 if write else 1)
            ids.append(bid)
        for a, b in zip(ids, ids[1:]):
            d.arrow(a, b)
        if prev:   # last stop of the row above -> first stop of this row: through the gap, down the left margin
            d.arrow(prev, ids[0], via=[(xs[5] + W / 2, gy - 8), (22, gy - 8), (22, gy + 32 + H / 2)])
        prev = ids[-1]
    d.box("total", xs[5], gys[3] + 32, W, H, "Total 1,200 s", ["Part A 450 s + Part H 750 s", "= 20 minutes"],
          kind="risk", sw=2)
    d.group("g_leg", 15, 578, 1530, 70, "Legend (box colour = what is on screen)")
    legend(d, 602, [("Workshop app, live", "app", False), ("Foundry tool, live", "pipeline", False),
                    ("Action form: Cancel by default", "ontology", False), ("Deck slide (+ optional switch)", "neutral", False)],
           x0=30)
    d.by_id["leg2"].sw = 3
    save(d)


if __name__ == "__main__":
    data_flow()
    ontology()
    demo_map()
