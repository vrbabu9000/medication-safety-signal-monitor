"""R01 Foundry from scratch: a primer on Palantir Foundry, taught through this project.

Build:  .venv/bin/python tools/handin/build_report.py R01-foundry-from-scratch
Output: docs/11-handin/reports/pdf/R01-foundry-from-scratch.pdf

Sources: foundry/README.md, foundry/pipelines/*/README.md, foundry/ontology/README.md,
foundry/monitoring/README.md, docs/06-decisions/DECISIONS.md (learnings), A009-A017, numbers.json.
Evidence labels follow the standard legend in tools/handin/style.py (printed in chapter 3).
Phase D (2026-11-05): drug-safety primer (ch. 2), codes and steps key (ch. 3), Dana callout, diagram 30 v2,
readable figures (crops and sideways pages), quoted-records table.
"""

META = {
    "id": "R01",
    "title": "Foundry from scratch",
    "short": "Foundry from scratch",
    "subtitle": "a primer on Palantir Foundry, taught through one real project",
    "version": "1.1",
    "date": "5 November 2026",
}

SCREENS = "docs/11-handin/screens/"
PNG = "docs/diagrams/png/"

# ---------------------------------------------------------------------- readable figures
# Phase D: diagrams printed at page width came out at about 3-4 pt. These two helpers keep each
# report self-contained: crop_figure() prints only the part of a screenshot or diagram the caption
# talks about, and landscape_figure() turns a wide diagram sideways onto its own page.
import io  # noqa: E402
from pathlib import Path  # noqa: E402

import style as S  # noqa: E402  (tools/handin is on sys.path when build_report.py runs)
from PIL import Image as _PIL  # noqa: E402
from reportlab.platypus import Flowable, Image, KeepTogether, Table, TableStyle  # noqa: E402

_ROOT = Path(__file__).resolve().parents[4]


def _img(path, box=None, maxpx=3200):
    im = _PIL.open(_ROOT / path)
    if box:
        W, H = im.size
        im = im.crop((round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H)))
    if im.width > maxpx:
        im = im.resize((maxpx, round(im.height * maxpx / im.width)), _PIL.LANCZOS)
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG")
    buf.seek(0)
    return buf, im.size


def _framed(buf, w, h):
    t = Table([[Image(buf, width=w, height=h)]], colWidths=[w + 2], hAlign="LEFT")
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), .5, S.C["rule"])] +
                          [(k, (0, 0), (-1, -1), 1) for k in ("LEFTPADDING", "RIGHTPADDING", "TOPPADDING", "BOTTOMPADDING")]))
    return t


def crop_figure(r, path, parts, caption, source, max_height=430):
    """One figure made of one or more crops (boxes as fractions x0, y0, x1, y1) of one image."""
    r._fig += 1
    items = []
    for box in parts:
        buf, (iw, ih) = _img(path, box)
        w = S.FRAME_W - 2
        h = w * ih / iw
        if h > max_height:
            h, w = max_height, max_height * iw / ih
        items += [_framed(buf, w, h), S.spacer(3)]
    items += [S.para(f"**Figure {r._fig}.** " + r._t(caption), "caption"), S.para("Source: " + r._t(source), "source")]
    r.flow.append(KeepTogether(items))


class _Landscape(Flowable):
    """A figure turned 90 degrees so a wide diagram uses the page height. Turn the page clockwise to read."""

    def __init__(self, buf, size, caption, source, long_side):
        super().__init__()
        self.buf, (self.iw, self.ih), self.L = buf, size, long_side
        self.cap, self.src = S.para(caption, "caption"), S.para(source, "source")

    def wrap(self, aW, aH):
        L = self.L
        ch, sh = self.cap.wrap(L, 1000)[1], self.src.wrap(L, 1000)[1]
        avail = min(aW, S.FRAME_W) - ch - sh - 12
        w = L - 2
        h = w * self.ih / self.iw
        if h > avail:
            h, w = avail, avail * self.iw / self.ih
        self.buf.seek(0)
        self.fr = _framed(self.buf, w, h)
        fh = self.fr.wrap(L, 1000)[1]
        self.parts = [(self.fr, fh + 6), (self.cap, ch + 4), (self.src, sh)]
        self.H = sum(x for _, x in self.parts)
        return self.H, L

    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(self.H, 0)
        c.rotate(90)
        y = self.H
        for f, h in self.parts:
            y -= h
            f.drawOn(c, 0, y + (h - f.wrap(self.L, 1000)[1]))
        c.restoreState()


def landscape_figure(r, path, caption, source, box=None):
    """A wide diagram on its own page, turned sideways (about 35% larger text than at page width)."""
    r._fig += 1
    buf, size = _img(path, box)
    r.flow.append(_Landscape(buf, size, f"**Figure {r._fig}.** " + r._t(caption) + " (Printed sideways on its own "
                             "page so the labels can be read.)", "Source: " + r._t(source), S.FRAME_H - 4))


def where(r, rows):
    """Standard 'where it lives in our project' table."""
    r.table(["In our project", "Exact name or path"], rows, widths=[150, 354])


def click(r, steps):
    r.h("What to click", 3)
    r.bullets(steps, numbered=True)


# Figures from the NAION statistics row that are not in numbers.json: quoted from diagram 32 v2
# (docs/diagrams/src/32-handin-signal-pipeline-v2.mmd, box B1), which prints the ontology_ae_stats row.
NAION_C = 128        # other drugs + NAION (diagram 32)
NAION_D = 763308     # other drugs, other reactions (diagram 32)


def build(r):
    a = r.n("signals.naion.a")
    nd = r.n("signals.naion.all_reports_drug")
    b = nd - a
    prr_calc = (a / nd) / (NAION_C / (NAION_C + NAION_D))

    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "What is Palantir Foundry, which parts of it did this project use, and where do I click to see each one?"),
              ("One-line answer",
               "Foundry keeps data, the code that cleans it, a model of real-world things (the Ontology) and the apps "
               "people use in one place. We used about a dozen of its parts. Each chapter takes one part, says what it "
               "is in one line, shows where it sits in our project, and gives the clicks to find it.")],
        is_=["A primer for an engineer who has never opened Foundry",
             "A one-page primer on drug safety data (chapter 2), so the later reports make sense",
             "The key to the codes (D###, A###, DQ##, O#) and build steps used in every report (chapter 3)",
             "A map of what to click for each part, ready for a live walk-through"],
        is_not=["Palantir's official documentation: we explain only the parts we used",
                "A full tour of Foundry (no Pipeline Builder, Contour, Quiver, Slate)",
                "Proof of how Foundry behaves at large scale: our project is a 13-drug pilot on the free Developer Tier",
                "A report on the drug-safety results (see R02 and R07)"],
        how_to_read="Read chapter 1 for the whole picture on one page. Chapter 2 teaches the drug-safety words "
                    "(FAERS, PRR, label, recall) in one page. Chapter 3 is the key to the codes and the evidence "
                    "labels. Chapters 4 to 13 each cover one part of Foundry in the order data flows: from where "
                    "things live, through data and code, to the Ontology, the app and its health checks. Each "
                    "chapter ends with a box that says how we know it works. Chapter 14 is a glossary and the "
                    "numbers. The data-flow diagram is printed sideways on its own page so it can be read.",
    )

    # ------------------------------------------------------------------ 01 summary
    r.chapter("Foundry in one page")
    r.p("**Palantir Foundry** is a data platform. In one web application it holds the data, the code that "
        "transforms the data, a model of the real-world things the data describes, and the apps people use to "
        "act on it. Everything has a version history and a lineage (where each piece came from).")
    r.p("**Our project** is a pilot for a hospital pharmacy safety officer. Each morning she asks three "
        "questions: (1) which drugs have side effects reported that the label does not mention, (2) which drugs "
        "have an active recall, and (3) what has changed since yesterday. Her trust rule: every flag must trace "
        "back to its source. We watch {{n:scope.drugs_formulary}} drugs ({{n:scope.opioids}} opioids and "
        "{{n:scope.glp1}} GLP-1 diabetes and weight-loss drugs, named in chapter 2) using public data only.")
    r.p("The table maps each Foundry part to what it does for us. Read it top to bottom: it is also the path the "
        "data takes.")
    r.table(["Foundry part", "One line", "In our project", "Ch."], [
        ("Project and folders", "A shared space with permissions", "`Medication Safety Signal Monitor`, 9 folders", "04"),
        ("Dataset", "A versioned table (or set of files)", "`raw_*`, `clean_*`, `ontology_*`, `monitoring_*`", "05"),
        ("Code Repository + transform", "Git repo whose Python functions turn datasets into datasets",
         "`pipelines_raw_ingest`, `pipelines_clean`", "06"),
        ("Build, Data Lineage, branch", "Run the code; see the graph; keep changes apart", "`master` branch, builds per file", "07"),
        ("Source + egress", "A permitted connection to an outside system", "4 sources: openFDA, DailyMed, RxNav, FAERS files", "08"),
        ("Ontology", "Objects, links and Actions on top of datasets", "10 `MSSM` object types, 1 Action", "09"),
        ("Object Explorer", "Search and browse objects and their links", "Signal → AE Stat → Drug → Label", "10"),
        ("Workshop", "Point-and-click app builder", "Module **MSSM Safety Officer**, {{n:app.pages}} pages", "11"),
        ("AIP", "Language models inside pipelines and apps", "Claude Sonnet 5.5 reads label sections", "12"),
        ("Data Health", "Checks and alerts on datasets", "{{n:monitoring.data_health_checks}} checks + our own monitoring", "13"),
    ], widths=[110, 150, 200, 30])
    r.key("Foundry is the runtime. The GitHub folder `foundry/` is the reviewed copy (a *mirror*) of every file "
          "that runs there. A change is made and tested in the mirror, pasted into Foundry, committed and built.",
          title="Two copies of the code, on purpose")
    r.note(["The screen answers her three questions, with four limits she should know on day one:",
            "**Question 1 moves only every quarter.** Signals change only when a new FAERS quarter arrives. At the "
            "baseline gate the newest FAERS data was about {{n:monitoring.faers_age_days}} days old (monitoring "
            "check `faers_age_days`). FAERS moved to a new FDA system (AEMS) in March 2026; how the feed continues "
            "is not verified yet (DQ20).",
            "**Question 3 card = last 30 days.** The Morning brief counts {{n:changes.last_30_days}} change events in "
            "the **last 30 days**, not since yesterday. On page 3 she sets the date range to *since my last review*.",
            "**Only the project owner can triage today.** The *Triage this signal* form is limited to the owner's "
            "account. Giving her role that permission is a production step.",
            "**The AI quote is not on her screen.** The AI read only {{n:ai.pilot_labels}} oxycodone pilot labels. "
            "For the top signal (semaglutide × NAION) it read 0 labels, so *not in label* there comes from the "
            "exact-text and synonym checks alone. NAION is a *known positive*, not a discovery: EMA PRAC (6 Jun "
            "2025) and a WHO alert (27 Jun 2025) named it, and our 3 US labels do not mention it (DECISIONS "
            "learning 2026-11-05)."],
          title="What this means for Dana (the safety officer)")
    r.gate("Chapter 1: the reader has the map", [
        ("Required evidence", "Every Foundry part in this report is tied to a real object in our project."),
        ("Result", "Met: each row above names a dataset, repository, object type or module that exists [[OBSERVED]]."),
        ("If it fails", "Remove the part from the report rather than describe it in general terms."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 02 drug safety primer
    r.chapter("Drug safety in one page", new_page=False)
    r.p("Foundry is the tool. This page is the subject. Every later report uses these words.")
    r.table(["Term", "What it means here"], [
        ("**FAERS**", "The FDA Adverse Event Reporting System. Doctors, patients, lawyers and drug companies send "
                      "**reports** of a suspected side effect (an *adverse event*). Anyone can report; nothing is "
                      "proven. The FDA publishes them as quarterly files. We use 2026 Q1 and Q2."),
        ("**Report, case, version**", "One **case** is one patient's event. Later follow-ups send a new *version* "
                                      "of the same case. We keep only the latest version and apply the FDA's "
                                      "delete lists (D022). We hold {{n:faers.cases_current}} current cases."),
        ("**Suspect vs concomitant**", "Each drug on a report has a role: *primary suspect* (PS), *secondary "
                                       "suspect* (SS), *interacting* (I), or *concomitant* (C: taken at the same "
                                       "time, not suspected). We count a drug only as PS, SS or I (D021)."),
        ("**MedDRA preferred term (PT)**", "The standard medical word for a reaction, for example *Optic ischaemic "
                                           "neuropathy*. FAERS uses it. MedDRA's groupings need a licence we do not "
                                           "have, so we group terms with our own keyword *buckets* (D016 v3)."),
        ("**Label (SPL)**", "The drug's official prescribing information, published on **DailyMed** as XML "
                            "(SPL, Structured Product Labeling). Its safety sections are Boxed Warning, "
                            "Contraindications, Warnings and Precautions, and Adverse Reactions. Each product has "
                            "one **reference label** we compare against: the application owner's label for that "
                            "route (D039 G3)."),
        ("**Recall**", "An FDA enforcement report: a product taken off the market or fixed. Class I is the most "
                       "serious (could cause serious harm), Class II may cause temporary harm, Class III is "
                       "unlikely to cause harm. **Active recall** = openFDA status **Ongoing** "
                       "({{n:recalls.active}} of {{n:recalls.total}}). Completed and Terminated recalls are not active."),
    ], widths=[120, 384])
    r.h("PRR in one worked line", 3)
    r.p("For each drug and reaction we fill a 2×2 table of reports. Example: semaglutide and NAION (a sudden "
        "loss of blood flow to the optic nerve; FAERS term *{{n:signals.naion.reaction}}*):")
    r.table(["", "Reaction = NAION", "Any other reaction"], [
        ("**Semaglutide**", f"a = {a:,}", f"b = {b:,}"),
        ("**All other drugs**", f"c = {NAION_C:,}", f"d = {NAION_D:,}"),
    ], widths=[150, 177, 177])
    r.p(f"**PRR** (proportional reporting ratio) = (a ÷ (a + b)) ÷ (c ÷ (c + d)) = ({a:,} ÷ {nd:,}) ÷ "
        f"({NAION_C:,} ÷ {NAION_C + NAION_D:,}) = {prr_calc:.1f}. In words: {a / nd:.1%} of semaglutide reports "
        f"mention NAION, against {NAION_C / (NAION_C + NAION_D):.3%} for all other drugs, so NAION is reported "
        "about {{n:signals.naion.prr}} times more often with semaglutide. a and a + b are in `numbers.json`; c "
        "and d are quoted from diagram 32 v2, which prints the `ontology_ae_stats` row [[DERIVED]].")
    r.p("The **Evans rule** (D006, proposed) is the screening test: at least 3 reports (a ≥ 3), PRR at least 2 and "
        "chi-squared (a test that the excess is not just noise in the counts) at least 4. NAION passes easily: "
        "chi-squared {{n:signals.naion.chi2_yates|,.1f}}.")
    r.h("Signal and ranked: one meaning each", 3)
    r.table(["Word", "Meaning (used the same way in every report)"], [
        ("**Signal** ({{n:signals.total}})", "A drug–reaction pair that meets the Evans rule **and** whose reaction "
                                             "is not found in any reference label of that drug "
                                             "({{n:signals.not_in_label}} *not in label*) or is found only through "
                                             "a medium-band synonym ({{n:signals.possibly_in_label}} *possibly in "
                                             "label*). A reason to look, not proof that the drug causes it."),
        ("**Ranked** ({{n:signals.ranked}})", "The review queue: signals that are *not in label*, in the "
                                             "**clinical** bucket (D016 v3), and less than half carried by "
                                             "mass-polypharmacy reports (reports listing 30 or more drugs, D023 "
                                             "v2). A review queue, not {{n:signals.ranked}} findings. It was "
                                             "{{n:signals.ranked_history.step9}} at step 9 (the first full build) "
                                             "and fell as the label check improved."),
    ], widths=[110, 394])
    r.p("**The 13 drugs.** Opioids (8): oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, "
        "buprenorphine, tramadol. GLP-1 drugs (5): semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide. "
        "Exenatide has no reference label in our data, so signals exist for {{n:scope.drugs_with_signals}} of "
        "the {{n:scope.drugs_formulary}} (D018, D031 v5).")

    # ------------------------------------------------------------------ 03 codes, steps, labels
    r.chapter("Codes, steps and evidence labels", new_page=False)
    r.p("The reports point to project records by short codes. You do not need to open them to follow the "
        "text, but every claim can be checked there.")
    r.table(["Code", "What it is", "Where it lives"], [
        ("**D###** (D006, D016 v3)", "A decision: what we chose, why, and the alternative we rejected. A changed "
                                    "decision gets a new version (v2, v3), never an edit. D001 to D048; some are "
                                    "still *proposed*: 12 of them, D006, D015, D025 to D029, D037, D045 to D048", "`docs/06-decisions/DECISIONS.md`"),
        ("**A###** (A010)", "An approach: something we tried, with its result and verdict (keep, drop, park)",
         "`docs/05-approaches/`"),
        ("**DQ##** (DQ34)", "A data issue found in a public source, and how we handled it", "`docs/07-data-quality/data-issues-register.md`"),
        ("**O#** (O1 to O3a)", "An optimization: before and after numbers, and whether it helped", "`docs/08-optimization-log/optimization-log.md`"),
        ("**G1 to G6**", "Checks inside decision D039 (for example G3: one reference label per product)", "D039"),
        ("**Step N** (1 to 12)", "A step of our build order. Step 6 = first Ontology path; step 8 = first signal "
                                "and app screen; step 9 = all 13 drugs (first full build); step 10 = incremental "
                                "FAERS; step 11 = the three-question screen and monitoring. A step is done when "
                                "its *gate* (a written check) passes",
         "`docs/04-architecture/foundry-conventions/project-build-order-v1.md`"),
        ("**Baseline gate**", "The full rebuild on 5 November 2026 whose counts were frozen into `numbers.json`",
         "`docs/11-handin/baseline-gate.md`"),
    ], widths=[105, 254, 145])
    r.p("Every claim carries a label. They mean the same thing in every report:")
    r.pill_legend()

    # ------------------------------------------------------------------ 04 projects
    r.chapter("Projects and folders", new_page=False)
    r.p("**What it is.** A Foundry *project* is a shared space with its own permissions. Inside it, *folders* "
        "hold every resource: datasets, code repositories, Ontology types, apps. A resource keeps a permanent "
        "ID called an **RID** (resource identifier, for example `ri.foundry.main.dataset.…`), so moving or "
        "renaming it does not break anything that uses it [[ASSUMED]].")
    r.p("We work in one project on the free **Developer Tier** (D010) [[OBSERVED]]. The folders follow the "
        "path the data takes [[DESIGNED]]:")
    where(r, [
        ("Project", "`/kestrel-01f4ab/Medication Safety Signal Monitor`"),
        ("Data", "`Data/raw` (as received), `Data/clean` (checked, one meaning per row), `Data/curated` "
                 "(backs the Ontology), `Data/quarantine`, plus `Data/monitoring`"),
        ("Code", "`Pipelines/` holds both code repositories"),
        ("Ontology", "`Ontology/Objects`, `Ontology/Links`, `Ontology/Actions`"),
        ("App", "`Workshop/` holds the module MSSM Safety Officer"),
        ("Other", "`AIP/{Logic,Evals}`, `Analysis`, `Documentation`, `Monitoring`, `Scratch`"),
    ])
    r.p("Three layers carry the data. People call them *bronze, silver, gold* (the *medallion* pattern). We "
        "keep the plainer names **raw, clean, curated** [[DESIGNED]] (D036):")
    r.table(["Layer", "Rule", "Example"], [
        ("raw (bronze)", "Exactly what the source sent, plus when and how we asked", "`raw_openfda_enforcement`"),
        ("clean (silver)", "Typed, checked, deduplicated; drug identity resolved once here", "`clean_drug_identity`"),
        ("curated (gold)", "One row per real-world object; backs the Ontology", "`ontology_signal_signals`"),
    ], widths=[90, 260, 154])
    r.p("Names follow `<layer>_<source>_<thing>`, for example `clean_faers_cases_current`. The Ontology types "
        "all start with `MSSM`, because the Developer Tier Ontology is shared with Palantir's example types "
        "[[DESIGNED]].")
    click(r, ["Left bar → **Projects** (folder icon) → *Medication Safety Signal Monitor*.",
              "Open `Data` → `curated` to see the datasets the app reads.",
              "Any resource: the breadcrumb at the top (Medication Safe… › Data › curated › name) shows where it lives."])
    r.how_we_know("The folder layout and paths are recorded in `foundry/README.md` (\"Foundry resource map\"; 9 "
                  "top-level folders) and visible in the breadcrumb of every screenshot in this report.")

    # ------------------------------------------------------------------ 05 datasets
    r.chapter("Datasets and transactions", new_page=False)
    r.p("**What it is.** A *dataset* is a table (or a folder of files) with a full version history. Each time "
        "something writes to it, Foundry records a **transaction** [[ASSUMED]]. A *snapshot* transaction "
        "replaces all the rows. An *append* transaction adds rows. Update and delete transactions change files "
        "in place. You can look at any past version.")
    r.p("How we use the transaction types [[OBSERVED]]:")
    r.table(["Pattern", "Our dataset", "Why"], [
        ("Snapshot every build", "All `raw_*` API pulls, e.g. `raw_openfda_enforcement` ({{n:raw.recall_rows}} rows: "
                                 "one per recall per drug it names, so {{n:raw.recalls}} distinct recalls; foundry/README)",
         "Each build is a full, comparable copy of what the source said"),
        ("Files, not a table", "`raw_faers_quarter_files` (FAERS quarterly ZIP members)",
         "FAERS comes as text files; a manifest dataset records their sizes and checksums"),
        ("Append, kept forever", "`monitoring_checks` ({{n:monitoring.checks_per_build}} rows per build)",
         "History of every health check, so a drop can be compared with last time"),
        ("Read own previous version", "`raw_dailymed_spl_xml`, `ai_label_section_extractions`, `ontology_change_snapshot`",
         "Reuse work already done (chapter 6, *incremental*)"),
        ("Empty on purpose", "`ontology_triage_decisions`",
         "Its rows come only from the officer's Action. Action edits are stored in the Ontology, not in this "
         "dataset, so it stays empty while {{n:app.triage_decisions}} decisions exist (chapter 9)"),
    ], widths=[110, 220, 174])
    crop_figure(r, SCREENS + "hood-dataset-signals-preview.jpg", [(0.035, 0, 0.75, 0.62)],
                "The dataset page for `ontology_signal_signals` (cropped): Preview tab with the first rows, the About "
                "panel (location, RID, size, *Updated via pipelines_clean*), and tabs for History, Health and Time Travel.",
                "docs/11-handin/screens/hood-dataset-signals-preview.jpg (Foundry, 2026-11-05)", max_height=300)
    click(r, ["Open a dataset → **Preview** shows rows; **Columns** shows the schema.",
              "**SQL console** (bottom) runs a query on this dataset. It answered in about 1.5 s for us; the code "
              "repository's SQL panel once gave no answer in 90 s (DECISIONS learnings, 2026-11-04) [[OBSERVED]].",
              "**History** lists every transaction and the build that wrote it. **Time Travel** shows an older version."])
    r.how_we_know("Every count in `numbers.json` was read with SQL in the code repository's SQL panel at the "
                  "baseline gate (`docs/11-handin/baseline-gate.md`). Raw row counts were compared with each "
                  "source's own total, drug by drug, after every pull.")

    # ------------------------------------------------------------------ 06 code repos
    r.chapter("Code Repositories and transforms", new_page=False)
    r.p("**What it is.** A *Code Repository* is a git repository that lives inside Foundry, with a web editor, "
        "checks and a build button. A **transform** is a Python function that reads one or more datasets "
        "(*Inputs*) and writes one or more datasets (*Outputs*). Foundry runs it on its own compute.")
    where(r, [
        ("Ingest repository", "`Pipelines/pipelines_raw_ingest`: Spark transforms that call outside APIs; "
                              "library `transforms-external-systems`"),
        ("Clean + curated repository", "`Pipelines/pipelines_clean`: lightweight polars transforms; datasets in, "
                                       "datasets out, no outside calls"),
        ("Files", "`transforms-python/src/myproject/datasets/` (e.g. `clean_faers.py`, `ontology_signals.py`)"),
        ("Mirror in GitHub", "`foundry/pipelines/{raw,clean,ontology,ai,monitoring}/` (same file names)"),
    ])
    crop_figure(r, SCREENS + "hood-code-repo-ontology-signals.jpg", [(0.03, 0.08, 0.66, 0.67)],
                "Code Repository `pipelines_clean` on branch `master` (cropped), file `ontology_signals.py` open. Left: "
                "the files; right: the code. Commit and Build sit further right on the same bar; the SQL scratchpad is below.",
                "docs/11-handin/screens/hood-code-repo-ontology-signals.jpg (Foundry, 2026-11-05)")
    r.h("Three kinds of transform we used")
    r.table(["Kind", "What it means", "Where we use it"], [
        ("Spark (`@transform`, `@transform_df`)", "Runs on a Spark cluster; good for very large data",
         "Raw pulls that call APIs (they need `@external_systems`)"),
        ("Lightweight (`@transform.using`, polars)", "Runs on one machine with the polars library; starts fast",
         "Every clean and curated transform. Builds took about 1 minute vs about 4 for Spark, most likely start-up "
         "(not measured separately; an observation, not a like-for-like test; DECISIONS learnings, 2026-11-04) [[OBSERVED]]"),
        ("Incremental (`@incremental`)", "The transform can read its own previous output and only do new work",
         "AI cache, DailyMed XML reuse, incremental FAERS, change feed, monitoring history"),
    ], widths=[130, 170, 204])
    r.p("The shape of every clean transform is the same. A shortened example:")
    r.code("from transforms.api import Input, Output, transform\n"
           "\n"
           "@transform.using(out=Output(CLEAN + \"clean_recalls_current\"),\n"
           "                 enforcement=Input(RAW + \"raw_openfda_enforcement\"))\n"
           "def compute(out, enforcement):\n"
           "    df = enforcement.polars()          # read the input as a polars table\n"
           "    ...                                # clean it\n"
           "    out.write_table(df)                # one output transaction")
    r.warning(["**Incremental is not automatically faster.** Our incremental FAERS path gives exactly the same rows "
               "as the full rebuild, but at two quarters it took {{n:optimization.O2.incremental_add_q2_s}} s against "
               "{{n:optimization.O2.full_rebuild_s}} s [[OBSERVED]] (O2). Reading back and rewriting the saved state "
               "costs more than it saves on a short history. R02 and R06 explain this."], title="Watch out")
    click(r, ["**Pipelines** → `pipelines_clean` → **Code** tab → `transforms-python/src/myproject/datasets/`.",
              "Edit, then **Commit** (top right). This is Foundry's own git, not GitHub.",
              "**Build** builds the file you have open. **Branches** shows the branch list (we use `master`)."])
    r.how_we_know("Both repositories run the code that is mirrored in `foundry/pipelines/`. The local runner "
                  "(`foundry/tools/local_run`) runs the same lightweight files on a laptop and gave the same counts "
                  "as Foundry (A014), so a change can be tested before it is pasted in.")

    # ------------------------------------------------------------------ 07 builds, lineage, branches
    r.chapter("Builds, lineage and branches", new_page=False)
    r.p("**What it is.** A **build** runs a transform and writes its outputs as new transactions. **Data "
        "Lineage** is Foundry's graph of which dataset feeds which. A **branch** is a separate line of change, "
        "as in git; a **commit** saves the code on that branch. Figure 3 (next page, sideways) is our data flow; "
        "Data Lineage shows the same graph live.")
    r.h("How a change reaches Foundry")
    r.bullets(["Edit the mirror file in GitHub `foundry/` and test it with the local runner.",
               "In the Foundry repository, open the file with the same name and paste the new text. Paste, do not "
               "type: the editor's auto-indent breaks typed Python.",
               "**Commit**, then **Build**.",
               "Check the result with SQL and compare the row count with the source total.",
               "Record the counts in the project log."], numbered=True)
    r.h("Build habits we learned the hard way", 3)
    r.table(["What happened", "What we do now"], [
        ("The repository Build button skipped an unchanged incremental transform, even after its input was rebuilt",
         "Build from the dataset page; check its **History** for a new job [[OBSERVED]]"),
        ("A dataset whose code and inputs had not changed did not rebuild", "Build ▾ → **Force build**"),
        ("Data Lineage *build all ancestors* re-ran every raw pull and the 700 MB FAERS download "
         "(DECISIONS learnings, 2026-11-04)", "Build file by file, in dependency order"),
        ("A new repository opened a VS Code workspace that auto-committed for about 30 minutes and conflicted with "
         "edits (DECISIONS learnings, 2026-11-04)", "One editor per branch; commit right after each paste"),
    ], widths=[260, 244])
    r.p("**Branches.** We worked on one branch, `master` in the code repositories (Ontology Manager shows its "
        "branch as *Main*, top right of Figure 4 in chapter 9) [[OBSERVED]]. A team would make a branch per change and merge "
        "after review [[ASSUMED]]. For this pilot, review happens in GitHub on the mirror instead [[DESIGNED]].")
    click(r, ["On any dataset page: **Explore pipeline** (or *Explore data lineage*) opens Data Lineage.",
              "In the graph, select a node to see its build history; colours show stale or failed builds.",
              "Dataset page **Build** ▾ → **Force** → *Only this dataset* rebuilds one step."])
    r.how_we_know("The baseline gate rebuilt the whole chain from the DailyMed pull to monitoring, in order, and "
                  "every count matched the earlier values. The change feed found {{n:changes.snapshot_diff_after_rebuild}} "
                  "changes between the two builds, which is right because the data was the same.")
    landscape_figure(r, PNG + "30-handin-data-flow-v2.png",
                     "Our data flow as built (v2, O3 measured): 4 public sources → `Data/raw` → `Data/clean` (drug "
                     "identity resolved once in `clean_drug_identity`) → `Data/curated` → Ontology → Workshop. "
                     "Dashed borders are incremental or cached steps. The product count printed in the identity box "
                     "comes from the README, not from `numbers.json`.",
                     "docs/diagrams/png/30-handin-data-flow-v2.png (Mermaid source docs/diagrams/src/30-handin-data-flow-v2.mmd)")

    # ------------------------------------------------------------------ 08 sources and egress
    r.chapter("External sources and egress")
    r.p("**What it is.** Foundry does not let code call the internet freely. A **source** (in *Data Connection*) "
        "describes one outside system. An **egress policy** allows network traffic to one host and port. Code "
        "can only use a source that has been imported into its repository.")
    r.table(["Source", "API name", "Host (egress policy)", "Brings in"], [
        ("`src_openfda_api`", "`OpenFdaApi`", "api.fda.gov:443", "Recalls, Drugs@FDA applications, NDC packages"),
        ("`src_dailymed_api`", "`DailyMedApi`", "dailymed.nlm.nih.gov:443", "Drug labels (SPL XML)"),
        ("`src_rxnav_api`", "`RxNavApi`", "rxnav.nlm.nih.gov:443", "RxNorm drug identity"),
        ("`src_faers_files`", "`FaersFiles`", "fis.fda.gov:443", "FAERS quarterly ZIP files"),
    ], widths=[100, 80, 130, 194])
    r.p("All four are REST API sources in `Data/raw` with no login. Settings: exports **off**; *import into code "
        "repositories* **on**; compute modules and pipeline functions **off** (least privilege, D038). "
        "The source secret `OpenFdaApiKey` is not used yet, because the pull needs only about "
        "{{n:raw.openfda_requests_approx}} requests, well under the no-key daily limit [[DESIGNED]].")
    r.p("A raw transform uses the source like this (shortened):")
    r.code("@external_systems(openfdaapi=Source(\"ri.magritte..source.e46a…\"))\n"
           "@transform_df(Output(\".../Data/raw/raw_openfda_enforcement\"))\n"
           "def compute(openfdaapi):\n"
           "    ...  # paged search; every reply kept with its HTTP status and time")
    r.table(["Rule every raw transform follows [[DESIGNED]]", "Why"], [
        ("Keep the original reply (JSON, XML or file) next to a few parsed columns", "Every flag can be traced to what the source said"),
        ("Save request parameters, HTTP status, retrieval time and the source's own 'last updated'", "Freshness and audit"),
        ("A non-200 reply becomes an **error row**, never a silent gap", "A missing label must not look like 'not in label'"),
        ("Row count must equal the source's own total, per drug", "Caught two silent search bugs (R07)"),
    ], widths=[300, 204])
    click(r, ["**Data Connection** → *Sources* → `src_openfda_api` → Overview, Network egress, Code import.",
              "**Control Panel** → egress policies: check the policy shows *Approved*. The source page kept "
              "saying *Pending approval* after self-approval [[OBSERVED]].",
              "In the repository: left bar → *Sources* → import the source; reload if it shows an error."])
    r.how_we_know("The first access test (D038) wrote one real recall, D-0338-2026, with HTTP 200 into "
                  "`raw_openfda_enforcement_access_test`. Today the 13-drug pulls give {{n:raw.recalls}} distinct recalls, "
                  "{{n:raw.drugsfda_rows}} Drugs@FDA rows, {{n:raw.ndc_rows}} NDC rows and {{n:raw.dailymed_labels}} "
                  "DailyMed labels, each equal to the source total.")

    # ------------------------------------------------------------------ 09 ontology
    r.chapter("The Ontology", new_page=False)
    r.p("**What it is.** The **Ontology** is a layer of real-world *things* on top of datasets. An **object type** "
        "(for example Drug) is backed by one dataset: one row becomes one *object*, one column becomes one "
        "**property**. A **link type** connects two object types (a Drug has many Products). An **Action** is a "
        "form that writes to the Ontology, so a person's decision is saved next to the data. Diagram 31 (printed sideways as "
        "Figure 2 in R03) shows the whole Ontology; R03 explains it in depth.")
    r.table(["Object type", "Backing dataset (`Data/curated`)", "Primary key", "Objects"], [
        ("MSSM Drug", "`ontology_drug_drugs`", "`ingredient_rxcui`", "{{n:scope.drugs_formulary}}"),
        ("MSSM Product", "`ontology_product_products`", "`product_key`", "not captured at the gate"),
        ("MSSM Label", "`ontology_label_labels`", "`label_key`", "{{n:labels.total}}"),
        ("MSSM Recall", "`ontology_recall_recalls`", "`recall_number`", "{{n:recalls.total}}"),
        ("MSSM Labeled Reaction", "`ontology_labeled_reactions` (from the AI step)", "`labeled_reaction_key`", "{{n:ai.reactions}}"),
        ("MSSM AE Stat", "`ontology_ae_stats`", "`stat_key`", "{{n:signals.ae_stats}}"),
        ("MSSM Signal", "`ontology_signal_signals`", "`signal_key`", "{{n:signals.total}}"),
        ("MSSM Change Event", "`ontology_change_events`", "`event_id`", "{{n:changes.total}}"),
        ("MSSM Source Status", "`ontology_source_status`", "`source`", "4 (one per source)"),
        ("MSSM Triage Decision", "`ontology_triage_decisions` (empty; edits on)", "`decision_id`", "{{n:app.triage_decisions}}"),
    ], widths=[115, 210, 115, 64])
    r.p("**Links** are built in two ways, by design [[DESIGNED]]. The many-to-many links (Drug ↔ Product, Product ↔ Label, Recall ↔ "
        "Product, Recall ↔ Drug) are backed by their own join datasets, such as `ontology_link_drug_product`. "
        "Many-to-one links use a foreign-key column, such as `ingredient_rxcui` on Signal pointing at Drug.")
    r.h("The one Action: Create MSSM Triage Decision", 3)
    r.p("The officer fills in **Decision** (reviewing, dismissed, escalated or monitoring) and a **Rationale**. "
        "Subject type, subject key and **evaluation id** (a fingerprint of the exact computation she is looking "
        "at: count, PRR, label check, data window) come from the selected signal and are locked. The system "
        "sets decision id, reviewer and time. The Action can only *create*, never edit or delete, so the "
        "decisions form an append-only audit trail [[DESIGNED]] (D040). Only the project owner can submit it today.")
    crop_figure(r, SCREENS + "hood-ontology-manager-signal.jpg", [(0.24, 0, 1, 0.56)],
                "Ontology Manager, object type MSSM Signal (cropped): {{n:signals.total}} objects, 25 properties, status "
                "Experimental, index status Indexed, edits disabled (only Triage Decision allows edits). Top right: "
                "the branch selector shows *Main*.",
                "docs/11-handin/screens/hood-ontology-manager-signal.jpg (Foundry, 2026-11-05)", max_height=260)
    r.warning("A second Signal → Drug link type was created by mistake on 2026-11-05, before checking the record. "
              "Nothing uses it. Deleting it is the owner's call, so it is still there and is marked on diagram 31 (R03).",
              title="A mistake left visible")
    click(r, ["**Ontology Manager** → search `MSSM` → open an object type → *Properties*, *Datasources*, *Link types*.",
              "Number display (decimals) is set once on the property (*Display → Numeric formatting*); every app uses it.",
              "Action types → *Create MSSM Triage Decision*. Its form preview here is a **test run only** and saves nothing."])
    r.how_we_know(["Object counts equal the backing dataset rows (checked at the baseline gate).",
                   "A test decision survived a forced rebuild of its empty backing dataset and a page reload: Action "
                   "edits live in the Ontology, not in the dataset (D040). {{n:app.triage_decisions}} decisions exist today."])

    # ------------------------------------------------------------------ 10 object explorer
    r.chapter("Object Explorer", new_page=False)
    r.p("**What it is.** *Object Explorer* is Foundry's search and browse tool for Ontology objects. You search "
        "by title or property, open an object, and follow its links. It is the fastest way to check the trust "
        "rule by hand.")
    crop_figure(r, SCREENS + "hood-object-explorer-naion-links.jpg", [(0.24, 0.17, 1, 0.45)],
                "Object Explorer (cropped): search for *Semaglutide · Optic ischaemic neuropathy*, the MSSM Signal "
                "selected, Links tab open: Drug of signal (the duplicate link), MSSM AE Stat, MSSM Drug.",
                "docs/11-handin/screens/hood-object-explorer-naion-links.jpg (Foundry, 2026-11-05)")
    r.p("The trace path we use [[OBSERVED]]:")
    r.bullets(["Search the signal name, e.g. *Semaglutide · Optic ischaemic neuropathy* (NAION).",
               "**Links → MSSM AE Stat**: the 2×2 counts behind the statistic (chapter 2: a = {{n:signals.naion.a}} "
               "reports with this drug and this reaction; PRR {{n:signals.naion.prr}}).",
               "**Links → MSSM Drug → MSSM Products → Reference Label**: the exact label versions that were searched, "
               "with DailyMed links. The app's page 1 now lists these too (panel *Reference labels searched*: "
               "{{n:app.labels_searched_naion}} labels for NAION).",
               "The FAERS case ids behind `a` can be listed with SQL on `clean_faers_drug_reaction`."], numbered=True)
    click(r, ["Left bar → **Search** (or Object Explorer) → type the object title.",
              "Filter by object type on the left; open the object; tabs **Details** and **Links**.",
              "To submit a real triage decision outside the app: open MSSM Triage Decision → **Actions** → Create."])
    r.how_we_know("At the baseline gate, 5 random ranked signals were traced this way. For all 5, the count `a` "
                  "recounted from FAERS rows equalled the signal, and the reaction term was not in any safety "
                  "section of the reference labels searched (`baseline-gate.md`).")

    # ------------------------------------------------------------------ 11 workshop
    r.chapter("Workshop", new_page=False)
    r.p("**What it is.** *Workshop* builds apps on the Ontology without front-end code. A **module** (an app) has "
        "**pages**. Each page holds **widgets** (tables, filters, charts, buttons). **Variables** carry data "
        "between widgets, for example *the set of ranked signals* or *the signal the user selected*. **Events** "
        "say what happens on a click, such as *switch to page 2*.")
    where(r, [
        ("Module", "**MSSM Safety Officer** (header *MSSM · Morning safety review*), folder `Workshop/`, published {{n:app.workshop_version}}"),
        ("Pages", "0 · Morning brief · 1 · Not in label · 2 · Recalls · 3 · What changed (a Tabs widget switches them)"),
    ])
    crop_figure(r, SCREENS + "app-0-morning-brief.jpg", [(0.035, 0.07, 1, 0.24), (0.035, 0.27, 0.53, 0.56)],
                "Page 0 · Morning brief (two crops): one Metric card with three numbers ({{n:signals.ranked}} ranked "
                "signals, {{n:recalls.active}} active recalls, {{n:changes.last_30_days}} changes in the **last 30 "
                "days**), and below it the table of how fresh each source is (*Data as of*).",
                "docs/11-handin/screens/app-0-morning-brief.jpg (Foundry, 2026-11-05)")
    r.table(["Workshop idea", "Our example"], [
        ("Widget: Metric card", "Three counts on page 0, each an *Object set aggregation* (Count) variable"),
        ("Widget: Object table", "*Ranked signals (not in label)* on page 1; recalls on page 2; changes on page 3"),
        ("Widget: Filter list", "Drug filter (pills with counts per drug); Event Date histogram with start and end date"),
        ("Widget: Property list", "The full signal record: 22 of the 25 signal properties in reading order with "
                                  "plain labels (foundry/ontology/README.md)"),
        ("Widget: Button group", "*Triage this signal* runs the Action"),
        ("Variable: object set", "*Ranked signals* = MSSM Signal where Is Ranked = true"),
        ("Variable: filtered object set", "*Ranked signals for chosen drugs* = *Ranked signals* + the drug filter"),
        ("Variable: object property", "*Selected signal key*, *Selected evaluation id* from the table's active row"),
        ("Event", "Each tab's on-click = *Switch to page*"),
    ], widths=[150, 354])
    crop_figure(r, SCREENS + "app-1-not-in-label-naion.jpg", [(0.035, 0, 1, 1)],
                "Page 1 · Not in label: ranked signals on the left (semaglutide × NAION at rank 1, {{n:signals.naion.a}} "
                "reports), the Triage button, past decisions, and the full signal record on the right.",
                "docs/11-handin/screens/app-1-not-in-label-naion.jpg (Foundry, 2026-11-05)")
    r.note(["**Why two variables per page.** A filter list must read the *unfiltered* set. If it read the filtered "
            "set, picking one drug would remove every other drug from its own choices. So: unfiltered set → filter "
            "list → filtered set → table → selected row → detail panel. Pages 2 and 3 use the same pattern.",
            "**A shortcut.** Table columns and property-list fields can be pasted into the widget's JSON "
            "(`</>` → edit → *Validate and save*). Reordering and relabelling the 22 properties took one paste "
            "instead of about 60 clicks (DECISIONS learnings, 2026-11-04) [[OBSERVED]]. The JSON box is live: close "
            "it without saving if you typed into it by mistake."])
    click(r, ["**Workshop** folder → *MSSM Safety Officer* → **View** to use it, **Edit** to change it.",
              "In Edit: the left panel lists pages and widgets; the right panel shows the selected widget's data "
              "source (a variable) and its events.",
              "Name pages with a number (0 ·, 1 ·): the editor sorts them alphabetically."])
    r.how_we_know("In View mode: select a signal → *Triage this signal* → the form opens with subject and "
                  "evaluation id filled and locked → Submit → reload → the decision is listed under the signal "
                  "(D042). The three Morning brief numbers equal SQL counts in `numbers.json`.")

    # ------------------------------------------------------------------ 12 AIP
    r.chapter("AIP: models in a pipeline", new_page=False)
    r.p("**What it is.** **AIP** (Palantir's Artificial Intelligence Platform) gives Foundry access to large "
        "language models (LLMs) from several vendors through a *Model Catalog*. Models can be used in apps, in "
        "*AIP Logic* functions, or, as we did, inside a Code Repository transform.")
    r.table(["Step", "What we did [[OBSERVED]]"], [
        ("Access test", "An AIP Logic test replied in 2.9 s; Claude, Gemini and Grok models were listed "
                        "(`docs/10-delivery/2026-11-04-foundry-access-results.md`)"),
        ("Pick a model", "Claude Sonnet 5.5 (`ri.language-model-service..language-model.anthropic-claude-5-5-sonnet`), D041"),
        ("Import it into the project", "Without this the build fails with `AccessWithoutImportDenied`. The Import button "
                                       "appears only when the model RID is typed inline in `GenericCompletionLanguageModelInput(\"…\")`"),
        ("Call it from a transform", "`ai_label_extraction.py` in `pipelines_clean`: one call per label safety section"),
        ("Check it", "Code checks that every quote the model returns is found word for word in the section text"),
        ("Cache it", "`@incremental`: the cache key is label + version + section + text hash + prompt, parser and model version"),
    ], widths=[120, 384])
    r.p("Results on the pilot ({{n:ai.pilot_labels}} oxycodone labels, {{n:ai.sections}} sections): {{n:ai.reactions}} "
        "reactions extracted, {{n:ai.grounded}} quotes found word for word in all {{n:ai.sections}} sections. A "
        "rebuild with unchanged text made {{n:ai.model_calls_on_rebuild}} model calls ({{n:ai.from_cache_on_rebuild}} "
        "of {{n:ai.sections}} sections from cache) [[OBSERVED]].")
    r.p("**Accuracy is a separate, smaller test.** F1 (a score that balances missed and wrong items) was "
        "{{n:ai.gold_f1}} against the proposed D015 target of {{n:ai.d015_target_f1}}, on a 35-item answer key: the Boxed Warning "
        "and Contraindications sections of the 2 oxycodone labels. The model found " + r.n("ai.gold_recall_strict").replace("/", " of ") + " "
        "answer-key items [[DERIVED]] (`eval/ai-eval-v1.md`).")
    r.warning(["The answer key was written by Claude and frozen before the model ran; a pharmacist has not checked it yet.",
               "Grounding shows the model did not invent quotes. It does not show the item is the right one.",
               "Today the AI does not change the signal list: text matching already covers its terms for the 2 pilot "
               "labels. Its quote is not shown on the officer's screen yet, and it read no semaglutide label."],
              title="What this does not show")
    click(r, ["**AIP** / Model Catalog: browse available models.",
              "Dataset `Data/curated/ai_label_section_extractions`: one row per section with status, tokens, latency and `from_cache`.",
              "Dataset `ontology_labeled_reactions` (object type MSSM Labeled Reaction): each reaction with its exact quote."])
    r.how_we_know("Optimization log O1: run 1 made {{n:optimization.O1.before_calls}} model calls "
                  "({{n:optimization.O1.before_tokens}} tokens); the rebuild made {{n:optimization.O1.after_calls}} "
                  "with {{n:optimization.O1.after_tokens}} tokens. AI evaluation: `eval/ai-eval-v1.md`.")

    # ------------------------------------------------------------------ 13 data health
    r.chapter("Data Health and monitoring", new_page=False)
    r.p("**What it is.** *Data Health* is Foundry's built-in checking on a dataset: did the last build succeed, is "
        "a key unique, is the data fresh. A failing check notifies its subscribers. We add our own computed "
        "checks for things Foundry cannot know, such as whether the AI's quotes are grounded.")
    crop_figure(r, SCREENS + "hood-data-health-signals.jpg", [(0.035, 0, 0.70, 0.51)],
                "Health tab of `ontology_signal_signals` (cropped): two checks (Build status, Primary key on "
                "`signal_key`), both Passed on 5 November 2026.",
                "docs/11-handin/screens/hood-data-health-signals.jpg (Foundry, 2026-11-05)", max_height=260)
    r.table(["Layer", "What", "Where"], [
        ("Foundry Data Health", "{{n:monitoring.data_health_checks}} checks: build status + primary key on "
                                "`ontology_signal_signals` and `clean_faers_cases_current`", "Dataset → **Health** tab"),
        ("Computed checks", "{{n:monitoring.checks_per_build}} checks appended every build: keys, row-count drops, "
                            "freshness, AI grounded rate, cache hits, reporter-type blanks", "`Data/monitoring/monitoring_checks`"),
        ("Drift replay", "Weekly and per-quarter series rebuilt from source dates; last 4 weeks vs the 4 before",
         "`Data/monitoring/monitoring_drift`"),
    ], widths=[110, 274, 120])
    r.p("The first runs raised two warnings, and both are real [[OBSERVED]]. (1) FAERS reports with a blank "
        "*reporter type* (who sent it: doctor, consumer, lawyer…) rose from "
        "{{n:monitoring.reporter_type_blank_q1|.0%}} in 2026 Q1 to {{n:monitoring.reporter_type_blank_q2|.0%}} in "
        "Q2. That matters to the officer because a report from a doctor and one from a lawyer weigh differently, "
        "and she can no longer tell them apart for most Q2 reports (DQ38). (2) Recalls reported for our drugs in "
        "the last 4 weeks were {{n:monitoring.recalls_last4w}} against {{n:monitoring.recalls_prev4w}} the 4 weeks before.")
    r.status("PLANNED", "Schedules (so freshness checks fire on their own), a Health page in Workshop, and "
                        "Data Health checks on recalls, DailyMed and the AI dataset.")
    click(r, ["Dataset → **Health** → **Add checks** → pick *Build status* or *Primary key*; write why in the note.",
              "Monitoring results: dataset `monitoring_checks` → SQL console, filter on the latest `run_at`."])
    r.gate("Chapters 4 to 13: every part can be found and checked", [
        ("Required evidence", "For each Foundry part: a name or path in our project, a picture or diagram, and the clicks."),
        ("Result", "Met for all ten parts. Screens were captured on 5 November 2026; counts come from `numbers.json`."),
        ("If it fails", "If a name has changed in Foundry, the mirror README in `foundry/` is the place to correct first."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 14 glossary
    r.chapter("Glossary and numbers", new_page=False)
    r.table(["Term", "Meaning in plain words"], [
        ("2×2 table (a, b, c, d)", "Report counts for one drug and one reaction: a = drug + reaction, b = drug + other "
                                   "reactions, c = other drugs + reaction, d = the rest (chapter 2)."),
        ("Action", "A form that writes to the Ontology. Ours creates a Triage Decision."),
        ("Active recall", "An openFDA recall with status Ongoing."),
        ("AIP", "Palantir's Artificial Intelligence Platform: language models usable inside Foundry."),
        ("Baseline gate / gate", "A gate is a written check that must pass before the next build step. The baseline "
                                 "gate is the 5 November 2026 rebuild whose counts are in `numbers.json`."),
        ("Bucket", "Our keyword group for a reaction term (clinical, efficacy, abuse/overdose, product use, pregnancy, "
                   "social/legal, administrative), a stand-in for licensed MedDRA groupings (D016 v3)."),
        ("Build", "One run of a transform; it writes new transactions to its output datasets."),
        ("Chi-squared (χ²)", "A test of whether a 2×2 table differs from what chance would give; Evans needs at least 4."),
        ("Code Repository", "A git repository inside Foundry, holding transforms."),
        ("Data Health", "Foundry's built-in checks and alerts on a dataset."),
        ("Data Lineage", "The graph of which dataset feeds which, with build status."),
        ("Dataset", "A versioned table (or set of files) in Foundry."),
        ("DailyMed / SPL", "The US National Library of Medicine site for drug labels; SPL (Structured Product Labeling) is their XML format."),
        ("Egress policy", "Permission for Foundry to send traffic to one outside host."),
        ("evaluation_id", "A fingerprint (hash) of the inputs behind a signal; a triage decision stores it, so it "
                          "records exactly what the officer saw."),
        ("Evans rule", "A common screening rule for a signal: at least 3 reports, PRR at least 2, chi-squared at least 4."),
        ("F1", "A score from 0 to 1 that balances missed items and wrong items; ours ({{n:ai.gold_f1}}) covers a 35-item answer key only."),
        ("FAERS", "The FDA Adverse Event Reporting System: spontaneous reports of suspected side effects."),
        ("GLP-1 drug", "A newer diabetes and weight-loss medicine (semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide)."),
        ("Incremental transform", "A transform that reads its own previous output and only processes new input."),
        ("Lightweight transform", "A transform that runs on one machine (we use polars) instead of Spark."),
        ("Mass report", "A FAERS report listing 30 or more drugs; kept out of the main count (D023 v2)."),
        ("Medallion", "The usual names bronze / silver / gold for the raw / clean / curated layers."),
        ("MedDRA preferred term (PT)", "The standard medical word FAERS uses for a reaction, e.g. *Optic ischaemic neuropathy*. MedDRA's groupings need a licence we do not have."),
        ("NAION", "Non-arteritic anterior ischaemic optic neuropathy: sudden vision loss from poor blood flow to the "
                  "optic nerve. Our top semaglutide signal."),
        ("NDC", "National Drug Code: the US code for a drug package."),
        ("Object / object type", "One real-world thing (a drug) / the kind of thing (Drug), backed by a dataset."),
        ("Object Explorer", "Foundry's search and browse tool for objects and links."),
        ("Ontology", "Foundry's layer of objects, links and Actions on top of datasets."),
        ("openFDA", "FDA's public API; we use its recall, Drugs@FDA and NDC endpoints."),
        ("PRR", "Proportional reporting ratio: how much more often a reaction is reported with this drug than with all other drugs."),
        ("Project / folder", "The shared space with permissions, and its folders."),
        ("Ranked", "A signal in the review queue: not in label, clinical bucket, under half from mass reports."),
        ("Reference label", "The one label per product we compare against: the application owner's label for that route."),
        ("RID", "Resource identifier: a resource's permanent ID in Foundry."),
        ("RxNorm / RxCUI", "The US standard drug vocabulary / its concept id. Our drug key is the ingredient RxCUI."),
        ("Signal", "A drug and reaction that meets the Evans rule and is not found in any reference label (or only "
                   "through a medium-band synonym: *possibly in label*). A lead to review, not proof."),
        ("Source", "A Data Connection record for one outside system, used by code."),
        ("Suspect role", "How a report names a drug: primary suspect, secondary suspect, interacting, or concomitant (not suspected)."),
        ("Transaction", "One write to a dataset: snapshot (replace), append, update or delete."),
        ("Transform", "A Python function that reads datasets and writes datasets."),
        ("Workshop", "Foundry's app builder: modules, pages, widgets, variables and events."),
    ], widths=[130, 374])
    r.h("Figures quoted from project records (not in numbers.json)")
    r.p("These come from measured project records, not from the baseline-gate capture. Each is cited where it "
        "appears.", style="small")
    r.table(["Figure", "Source"], [
        ("NAION c = 128, d = 763,308 (other drugs)", "Diagram 32 v2 (prints the `ontology_ae_stats` row)"),
        ("9 top-level folders", "foundry/README.md (resource map); ACTIVITY-LOG"),
        ("930 raw recall rows = 900 distinct recalls (one row per recall per drug named)", "foundry/README.md raw table"),
        ("SQL console about 1.5 s; repository SQL panel no answer in 90 s", "DECISIONS learnings, 2026-11-04"),
        ("Lightweight builds about 1 min vs about 4 min for Spark", "DECISIONS learnings, 2026-11-04"),
        ("700 MB FAERS download; VS Code auto-commit for about 30 minutes", "DECISIONS learnings, 2026-11-04; foundry/README.md"),
        ("MSSM Signal: 25 properties; 22 shown in the property list; one paste vs about 60 clicks",
         "screens/README.md (Figure 4); foundry/ontology/README.md; DECISIONS learnings, 2026-11-04"),
        ("AIP access test 2.9 s", "docs/10-delivery/2026-11-04-foundry-access-results.md"),
        ("Answer key of 35 items (Boxed Warning + Contraindications, 2 labels)", "eval/ai-eval-v1.md"),
        ("5 random ranked signals traced", "docs/11-handin/baseline-gate.md"),
    ], widths=[300, 204])
    r.numbers_appendix()
