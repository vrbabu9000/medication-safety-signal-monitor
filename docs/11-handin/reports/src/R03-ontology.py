"""R03 Ontology: the MSSM object types, links and the triage Action, and how they make
"every flag traces to its source" possible.

Build:  .venv/bin/python tools/handin/build_report.py R03-ontology
Output: docs/11-handin/reports/pdf/R03-ontology.pdf

Sources: foundry/ontology/README.md, docs/05-approaches/A010, A012, A016, DECISIONS D040 / D042 / D045,
docs/11-handin/baseline-gate.md, diagram 31 v2 (docs/diagrams/png/31-handin-ontology-v2.png), A019 (D041 v2).
Numbers come from docs/11-handin/numbers.json via {{n:...}}; the few figures from other records are cited
where they appear and listed in the appendix.
Phase D (2026-11-05): NAION not AI-checked (W3); page 1 "Reference labels searched" panel (S12-S14, app-1c);
diagram 30 reprint replaced by a pointer to R01/R02 (v2); diagram 31 printed sideways; Dana callout; legend re-tags.
"""

META = {
    "id": "R03",
    "title": "The Ontology",
    "short": "Ontology",
    "subtitle": "ten object types, their links and the one write-back Action",
    "version": "1.2",
    "date": "6 November 2026",
}

ONT = "foundry/ontology/README.md"
PNG = "docs/diagrams/png/"
SCREENS = "docs/11-handin/screens/"

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


def build(r):
    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "How is the data shaped so that the safety officer can click from any flag back to its "
               "source, and so that her decisions survive every rebuild?"),
              ("One-line answer",
               "Ten object types, each backed by one curated dataset with one row per object and a checked key. "
               "Links mirror real relationships (drug, product, label, recall, statistic, signal). One "
               "create-only Action writes each triage decision as its own object, pinned to the exact "
               "computation it reviewed by an `evaluation_id`.")],
        is_=["A tour of the MSSM Ontology as built in Foundry (5 November 2026; updated 6 November)",
             "Written for an engineer who has never used Palantir Foundry",
             "Each object type: backing dataset, key, title and why that grain",
             "Each link type with its cardinality, and one mistake we fixed",
             "A worked trace of the top signal (NAION) back to its sources"],
        is_not=["The pipeline design (how the curated datasets are computed)",
                "A statistics lesson: PRR and the Evans rule are explained only as far as needed here",
                "The Workshop app guide (see R04)",
                "Reviewed by a pharmacist: no pharmacist has reviewed the signals yet"],
        how_to_read="Chapter 1 is the plain-language summary and the word list; read it first if Foundry is "
                    "new to you. Chapters 2 to 5 describe the parts. Chapter 6 walks one signal back to its "
                    "sources, which is the point of the whole design. Chapter 7 lists what a second engineer "
                    "should add next. Each chapter ends with a gate box: what evidence we needed, what we "
                    "found, and what would make it fail. Numbers are looked up from `numbers.json`; the few "
                    "figures from other project records name their record. Codes (D### decision, A### approach, DQ## "
                    "data issue) and *step N* (build-order step) are explained in the word list and in R01 chapter 3.",
    )

    # ------------------------------------------------------------------ 01 summary
    r.chapter("Summary in plain language")
    r.p("**The problem.** A hospital pharmacy safety officer asks three questions each morning: which drugs "
        "have side effects reported that the label does not mention, which drugs have an active recall, and "
        "what changed since yesterday. She trusts an answer only if she can see where it came from. Our "
        "rule: **every flag traces back to its source.**")
    r.p("**The Ontology is how we keep that promise.** In Palantir Foundry, the *Ontology* is a layer of "
        "business objects (a drug, a label, a recall, a signal) on top of plain tables. Each object can link "
        "to other objects. An app then shows objects, not rows, and a user can follow the links by clicking.")
    r.p("A {{n:app.pages}}-page Workshop app sits on top of **ten object types** (all named with the "
        "prefix `MSSM`), **{{n:ontology.link_types_mssm}} link types** and **one Action**. The scope is {{n:scope.drugs_formulary}} "
        "drugs: {{n:scope.opioids}} opioids (oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, "
        "buprenorphine, tramadol) and {{n:scope.glp1}} GLP-1 medicines, the newer diabetes and weight-loss drugs "
        "(semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide).")

    r.h("Words used in this report")
    r.table(["Term", "Meaning in one line"], [
        ("Foundry", "Palantir's data platform: storage, pipelines, data model and apps in one place."),
        ("Dataset", "A table stored in Foundry, with a version history for every build."),
        ("Transform", "Code (Python here) that reads datasets and writes a new dataset."),
        ("Curated dataset", "The last pipeline layer: one row per future object, key checked by code."),
        ("Object type", "A kind of business object (for example MSSM Drug), backed by one dataset."),
        ("Primary key / title", "The column that makes each object unique / the name a person sees."),
        ("Link type", "A named relationship between two object types, with a cardinality."),
        ("Cardinality", "How many objects on each side: many-to-one or many-to-many."),
        ("Action", "A form that changes the Ontology (here: creates a triage decision)."),
        ("Ontology Manager", "Where object types, links and Actions are defined."),
        ("Object Explorer", "Where a person searches objects and follows their links."),
        ("Workshop", "Foundry's app builder; the officer's screen is a Workshop module."),
        ("FAERS", "The FDA Adverse Event Reporting System: public side-effect reports."),
        ("DailyMed / SPL", "The official US label library; labels are XML files called SPL."),
        ("RxNorm / RxCUI", "The US drug naming system; an RxCUI is the ID of one ingredient."),
        ("PRR", "Proportional reporting ratio: how much more often a reaction is reported with this drug than "
                "with all other drugs."),
        ("Evans rule", "The screening test for a signal: at least 3 reports, PRR at least 2, chi-squared at least 4 (D006)."),
        ("Signal", "A drug–reaction pair that meets the Evans rule and whose reaction is not found in any reference "
                   "label of the drug ({{n:signals.not_in_label}} *not in label*) or only through a medium-band synonym "
                   "({{n:signals.possibly_in_label}} *possibly in label*): {{n:signals.total}} in all."),
        ("Ranked", "The review queue ({{n:signals.ranked}}): not in label, clinical bucket, under half from "
                   "mass-polypharmacy reports. It was {{n:signals.ranked_history.step9}} at step 9."),
        ("Reference label", "The one label per product we compare against: the application owner's label for that route."),
        ("evaluation_id", "A fingerprint (hash) of the inputs behind a signal, stored with each triage decision."),
        ("Recall class", "FDA severity: Class I most serious, Class II may cause temporary harm, Class III unlikely to "
                         "cause harm. *Active* = status Ongoing."),
        ("Codes", "D### = decision, A### = approach tried, DQ## = data issue (each in the project records). "
                  "*Step N* = a step of the 12-step build order (step 6 = first Ontology, step 8 = first signal "
                  "screen, step 9 = all 13 drugs, step 11 = three-question screen). A *gate* is the check that ends a step."),
    ], widths=[1.2, 4])

    r.key("A signal is a reason to look, not proof that the drug causes the reaction. The "
          "{{n:signals.ranked}} ranked signals are a review queue, not {{n:signals.ranked}} findings.",
          title="Read every count this way")
    r.note(["**She cannot triage yet.** Only the project owner's account can submit a Triage Decision today. "
            "Giving the officer's role that permission is a production step.",
            "**Her trace ends at label versions and what they do say.** A *not in label* signal has no matching "
            "quote. Page 1 lists the reference labels that were searched, with DailyMed links, and below them "
            "what the AI read in those labels, quoted word for word (chapter 6).",
            "**The AI read her top signal's labels.** Since 6 Nov (D041 v2) the AI reads the "
            "{{n:app.labels_read_by_ai_naion}} semaglutide labels. For semaglutide × NAION it found "
            "diabetic-retinopathy terms and no optic-nerve term, which agrees with the exact-text and synonym "
            "checks: *not in label*. NAION is a *known positive*, not a discovery: EMA PRAC (6 Jun 2025) and a WHO alert (27 Jun 2025) "
            "named it, and our 3 US labels do not mention it (DECISIONS learning 2026-11-05).",
            "**Signals change once a quarter.** New FAERS data arrives quarterly (about {{n:monitoring.faers_age_days}} "
            "days old at the gate), so most *changes* she sees are recalls and label versions."],
           title="What this means for Dana (the safety officer)")
    r.pill_legend()

    r.gate("Summary", [
        ("Required evidence", "The reader can say what an object, a link and an Action are, and why the triage "
                              "decision is its own object."),
        ("Result", "The rest of this report shows each part with Foundry screenshots and counts from "
                   "`numbers.json`."),
        ("If it fails", "Read the word list again, then chapter 6 (the worked trace)."),
    ])

    # ------------------------------------------------------------------ 02 where it sits
    r.chapter("Where the Ontology sits", new_page=False)
    r.p("**The Ontology is the last step before the screen. Nothing is computed in it; it only names, keys "
        "and links what the pipelines have already prepared.**")
    r.p("Data moves in four layers (diagram 30 v3, printed full page as R01 Figure 3 and R02 Figure 1; file "
        "`docs/diagrams/png/30-handin-data-flow-v3.png`). Public sources are pulled into `Data/raw` as received. "
        "`Data/clean` parses and fixes them, and resolves drug identity **once**, in `clean_drug_identity`. "
        "`Data/curated` holds one dataset per object type and one per many-to-many link. The Ontology reads "
        "the curated datasets. The Workshop app reads the Ontology and writes triage decisions back to it.")
    r.h("Three rules we kept")
    r.table(["Rule", "Why", "Evidence"], [
        ("One curated dataset per object type, one row per object.",
         "Foundry can then index it directly; the object count equals the dataset row count.",
         "[[OBSERVED]] Step 6 gate (A010): object counts = dataset rows, 0 null and 0 duplicate keys."),
        ("Keys are checked in code before Foundry sees them.",
         "A duplicate key would make two objects collide; better to fail the build.",
         "[[TESTED]] `ontology_objects.py` and `ontology_signals.py` check keys (A010, D042); the build fails on a duplicate."),
        ("Many-to-many links are join datasets; many-to-one links are a foreign-key column.",
         "A many-to-many hidden in an array cannot be followed by a click and cannot be filtered on.",
         "[[DESIGNED]] D040 (alternative rejected: arrays inside one object). Built and used by every link below."),
    ], widths=[2.2, 2.4, 2.4])
    r.note("All types carry the prefix `MSSM` (Medication Safety Signal Monitor). The Foundry Ontology we use "
           "is shared with Palantir's example types, so the prefix keeps ours easy to find and avoids name "
           "clashes (A010). All types are status *Experimental*.")
    r.gate("Placement", [
        ("Required evidence", "Every object type is backed by a curated dataset; no business logic lives only in "
                              "the Ontology."),
        ("Result", "Met. The only data written in the Ontology is the triage decision (chapter 5)."),
        ("If it fails", "A computed value that exists only in an app would not be traceable: move it into a "
                        "transform."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 03 object types
    r.chapter("The ten object types")
    r.p("**Each object type answers one question: what is one thing here? That choice (the grain) decides "
        "what can be counted, linked and traced.**")
    r.p("The table lists each type as recorded in `" + ONT + "`. Counts are from the baseline gate on "
        "5 November 2026. *Edits* = whether a user can change objects of that type from an app.")
    r.table(["Object type", "Backing dataset (Data/curated)", "Primary key", "Title shown", "Objects", "Edits"], [
        ("MSSM Drug", "`ontology_drug_drugs`", "`ingredient_rxcui`", "Oxycodone", "{{n:scope.drugs_formulary}}", "off"),
        ("MSSM Product", "`ontology_product_products`", "`product_key` (application number)", "OXYCONTIN (NDA022272)",
         "see note", "off"),
        ("MSSM Label", "`ontology_label_labels`", "`label_key` = setid|v<version>", "title · v44", "{{n:labels.total}}", "off"),
        ("MSSM Recall", "`ontology_recall_recalls`", "`recall_number`", "D-0338-2026 · Class II · Ongoing",
         "{{n:recalls.total}}", "off"),
        ("MSSM Labeled Reaction", "`ontology_labeled_reactions`", "`labeled_reaction_key`", "reaction text",
         "{{n:ai.reactions}}", "off"),
        ("MSSM AE Stat", "`ontology_ae_stats`", "`stat_key`", "drug · reaction", "{{n:signals.ae_stats}}", "off"),
        ("MSSM Signal", "`ontology_signal_signals`", "`signal_key` = rxcui|reaction|rule", "Oxycodone · Myoclonus",
         "{{n:signals.total}}", "off"),
        ("MSSM Change Event", "`ontology_change_events`", "`event_id` (hash)", "display name",
         "{{n:changes.total}}", "off"),
        ("MSSM Source Status", "`ontology_source_status`", "`source`", "source name", "one per source", "off"),
        ("MSSM Triage Decision", "`ontology_triage_decisions` (empty on purpose)", "`decision_id` (generated UUID)",
         "`subject_key`", "{{n:app.triage_decisions}}", "**on**"),
    ], widths=[1.3, 1.9, 1.7, 1.4, 0.75, 0.6])
    r.p("Notes: Product count is recorded in the ontology README and diagram 31 but was not captured into "
        "`numbers.json`, so it is not quoted here. Labeled Reaction covers only the labels the AI reads "
        "({{n:ai.pilot_labels}} labels: 2 oxycodone + 3 semaglutide, {{n:ai.sections}} sections; D041 v2). Triage Decision count is the decisions "
        "present at the baseline gate (two test decisions).", "small")

    r.h("Why each grain")
    r.table(["Object type", "One object is", "Why this grain (and not another)", "Source"], [
        ("Drug", "one active ingredient (RxNorm ingredient RxCUI)",
         "Side-effect counts belong to the ingredient: FAERS reports name products loosely, and the officer thinks "
         "in ingredients. The formulary is an explicit list of ingredient IDs.", "D018, D027"),
        ("Product", "one FDA application (NDA / ANDA / BLA number)",
         "Labels and recalls belong to products, not ingredients: an injection and a tablet have different labels. "
         "FAERS bulk files carry the application number, so this is the finest key FAERS can reach.", "D027, D039 G2"),
        ("Label", "one version of one label (setid + version)",
         "A label changes over time; a flag must name the exact version that was searched.", "D019, A010"),
        ("Recall", "one FDA enforcement record",
         "The recall number is the FDA's own ID; the officer can quote it.", "A010"),
        ("Labeled Reaction", "one reaction the AI found in one label section, with its exact quote",
         "Keeps the AI output inspectable item by item, with the quote that grounds it.", "D041 v2"),
        ("AE Stat", "one drug × reaction count table for one FAERS window and rule version",
         "Holds the 2×2 numbers (a, b, c, d), PRR, confidence interval and χ² for every pair, flagged or not.", "D042"),
        ("Signal", "one drug × reaction that meets the Evans rule and is not found in the label",
         "The unit the officer reviews. The key includes the rule version, so a new rule gives new signals instead "
         "of silently changing old ones.", "D042"),
        ("Change Event", "one dated change to a signal, recall or label",
         "Answers question 3 as a list of facts with dates, not a guess.", "D045"),
        ("Source Status", "one public source", "Shows the as-of date of each source; they update on different clocks.",
         "D045"),
        ("Triage Decision", "one decision by one person at one time",
         "Decisions are history: never overwritten, so they are separate objects (chapter 5).", "D040, D042"),
    ], widths=[1.1, 1.8, 3.6, 0.9])
    r.how_we_know(["Object counts were captured from Foundry SQL at the baseline gate "
                   "(`docs/11-handin/baseline-gate.md`) and stored in `numbers.json` [[OBSERVED]].",
                   "Key checks: 0 duplicate `stat_key` and 0 duplicate `signal_key` at step 8 (A012); monitoring "
                   "re-checks keys of signals, recalls, labels and change events on every build (A017) [[OBSERVED]]."])
    crop_figure(r, SCREENS + "hood-ontology-manager-signal.jpg", [(0.24, 0.05, 1, 0.93)],
                "MSSM Signal in Ontology Manager (cropped): {{n:signals.total}} objects, 25 properties (screens "
                "README), Display Name as title, Signal Key as primary key, status Experimental, edits disabled.",
                "docs/11-handin/screens/hood-ontology-manager-signal.jpg (Foundry, 2026-11-05)", max_height=360)
    r.gate("Object types", [
        ("Required evidence", "Each type has one backing dataset, a unique key, a readable title and a written "
                              "reason for its grain."),
        ("Result", "Met for all 10. Object type descriptions are blank in Foundry (the wizard did not keep them); "
                   "this report and the README are the written record."),
        ("If it fails", "A type with two rows per key would fail its build: the key check stops it first."),
    ], status="TESTED")

    landscape_figure(r, PNG + "31-handin-ontology-v2.png",
                     "The Ontology as built (v2, 6 Nov): 10 MSSM object types with keys and row counts, the "
                     "{{n:ontology.link_types_mssm}} link types with their cardinality, and the create-only Action. "
                     "The Product count printed in the diagram comes from the README; it was not captured at the gate.",
                     "docs/diagrams/png/31-handin-ontology-v2.png · draw.io copy docs/diagrams/drawio/31-handin-ontology-v2.drawio")

    # ------------------------------------------------------------------ 04 links
    r.chapter("The link types")
    r.p("**Links are what turn ten tables into something a person can walk through. Each link below is a "
        "real relationship in the data, with the cardinality the data actually has.**")
    r.p("Figure 2 (the sideways page just before this chapter) draws every object type and link below.")
    r.table(["Link", "Cardinality", "Backed by", "What it means"], [
        ("Drug ↔ Product", "many : many", "`ontology_link_drug_product`",
         "A combination product has several ingredients; an ingredient is in many products."),
        ("Product ↔ Label", "many : many", "`ontology_link_product_label`",
         "Every approval number printed in the label XML. Repackagers make this wide."),
        ("Product → Reference Label", "many : 1", "foreign key `reference_label_key`",
         "The one label we compare against for that product (route-specific). See below."),
        ("Recall ↔ Product", "many : many", "`ontology_link_recall_product`",
         "High or medium-confidence NDC (package code) matches from the recall text."),
        ("Recall ↔ Drug", "many : many", "`ontology_link_recall_drug`",
         "The ingredient is named in the recall text. Catches recalls that match none of our products."),
        ("Labeled Reaction → Label", "many : 1", "foreign key `label_key`", "Which label version the AI read."),
        ("AE Stat → Drug", "many : 1", "foreign key `ingredient_rxcui`", "Each count table belongs to one drug."),
        ("Signal → AE Stat", "many : 1 (1 : 1 in data)", "foreign key `stat_key`",
         "The statistics behind the signal: the 2×2 counts, PRR, χ²."),
        ("Signal → Drug", "many : 1", "foreign key `ingredient_rxcui`", "The drug of the signal."),
        ("Triage Decision → Signal", "many : 1", "foreign key `subject_key`",
         "Every decision taken on that signal, oldest to newest."),
    ], widths=[1.6, 1.1, 1.9, 2.6])

    r.h("Two design choices worth explaining")
    r.p("**Reference Label is a separate link.** A product can be linked to many labels (the owner's label, "
        "repackagers, old versions). If the label check searched all of them, one repackager's extra sentence "
        "could hide a real gap, and the officer could not say which label was meant. So each product has "
        "exactly one *Reference Label* (the owner's label for that route), as a many-to-one foreign key. The "
        "many-to-many link stays for browsing. Products with no owner label get no reference label, so the "
        "check cannot silently compare against a generic one (D039 G3 and G4, A010) [[DESIGNED]].")
    r.p("**Recalls link two ways.** The NDC match (Recall ↔ Product) is precise but misses recalls whose "
        "package codes are not in the NDC directory (old or compounded products). The ingredient match "
        "(Recall ↔ Drug) catches those. The newest recall at the gate, {{n:recalls.newest}}, is a compounded "
        "tirzepatide product: it shows under tirzepatide through Recall ↔ Drug and has 0 matched products, "
        "which is correct (A016) [[OBSERVED]].")
    r.p("**Change Event and Source Status have no link type.** The change feed is filtered by drug name on "
        "screen. That is simpler, but it is a gap: a Change Event → Drug link would let the officer jump from "
        "a change to the drug's other objects (chapter 7).")

    r.note(["**History: a duplicate Signal → Drug link, now deleted.** On 5 November, during step 11, a second "
            "Signal → Drug link type (`drugOfSignal` / `signalsOfDrug`) was created without first checking "
            "the ontology README. One already existed. It was deleted on 6 Nov after checking nothing used it: no "
            "Workshop variable used it, and its usage log showed one Object Explorer read. Ontology Manager only "
            "warns that apps *may* break; it does not list them, so that check was done by hand (DECISIONS "
            "learnings, 2026-11-05 and 2026-11-06). Lesson: check the README before creating a link type."],
           title="A mistake, fixed")
    r.gate("Links", [
        ("Required evidence", "Links do not multiply records; counts reached through a link equal source counts."),
        ("Result", "Met at the step 6 gate: oxycodone reached the same number of products and recalls through "
                   "the links as in the source (A010) [[OBSERVED]]. The duplicate link type was deleted on 6 Nov; "
                   "{{n:ontology.link_types_mssm}} MSSM link types remain."),
        ("If it fails", "A wrong many-to-many join would show a drug with more recalls than the FDA lists: "
                        "compare link counts with source counts after every scope change."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 05 triage
    r.chapter("Triage decisions: the one write-back", new_page=False)
    r.p("**The officer's decision is the only thing the app writes. It is stored as its own object, created "
        "by a create-only Action, so a rebuild of the data can never erase it.**")
    r.h("The Action")
    r.table(["Part", "As built"], [
        ("Name", "Create MSSM Triage Decision (`create-mssm-triage-decision`)"),
        ("Rule", "Create object only. No modify, no delete: the decision history is append-only."),
        ("The officer fills in", "Decision (reviewing / dismissed / escalated / monitoring) and Rationale (free text)."),
        ("Filled from the screen, locked", "Subject Type = `signal`, Subject Key = the selected signal's key, "
                                           "Evaluation Id = the selected signal's evaluation id."),
        ("Set by the system", "Decision Id = unique identifier, Reviewer = current user, Decided At = current time."),
        ("Who can submit", "The project owner only, for now. The officer cannot submit until her role is given "
                           "the Action permission (a production step)."),
    ], widths=[1.6, 5])

    r.h("Why a separate object, and why `evaluation_id`")
    r.p("Signals are recomputed on every build. If the decision were an editable *status* field on the "
        "Signal object, it would live in a table that the next build replaces. Foundry keeps Action edits in "
        "the Ontology, not in the backing dataset, so a separate Triage Decision object survives any rebuild of "
        "the signals. It also gives a full history: several decisions on one signal stay side by side.")
    r.p("The `evaluation_id` is a hash of the inputs that produced the signal (counts, rule version, label "
        "check method). It answers the question an auditor will ask: *what exactly did she look at when she "
        "decided?* If new FAERS data or a new synonym row changes the signal, the evaluation id changes too. "
        "The old decision still points at the old computation (D042) [[DESIGNED]]. Today the past-decisions table "
        "shows the evaluation id each decision was made on, so a change can be seen by comparing ids; the screen "
        "does not yet flag *evidence moved since your decision* [[PLANNED]].")
    r.table(["Option considered", "Why rejected"], [
        ("Editable status property on Signal", "Lost on every rebuild; no history of who decided what."),
        ("Free-text subject key typed by the officer", "One typo breaks the trace; the key is filled and locked instead."),
        ("Triage Decision with no backing dataset (Foundry's 'empty datasource' option)",
         "Then there is nothing to force-rebuild, so the test *decisions survive a rebuild* could not be run. An empty "
         "curated dataset can be rebuilt, and it keeps the schema in code."),
        ("Modify and delete on the Action", "An audit trail must be append-only; a new decision supersedes the old one."),
    ], widths=[2.4, 4])
    r.how_we_know(["**Save test (step 6):** signals did not exist yet, so the first test decision used the Action's "
                   "Subject Type field to point at recall D-0338-2026. It survived a forced rebuild of "
                   "`ontology_triage_decisions` and a page reload (A010) [[OBSERVED]]. Only the Triage Decision → "
                   "Signal link exists today (item 6 in chapter 7).",
                   "**Workshop test (step 8):** a decision submitted from the screen on *Oxycodone · Myoclonus*, "
                   "with the evaluation id filled and locked, was still there after a full reload (A012) [[OBSERVED]].",
                   "**Baseline gate:** after the whole downstream chain was rebuilt, the "
                   "{{n:app.triage_decisions}} triage decisions were still present (baseline-gate.md) [[OBSERVED]]."])
    r.warning("Known gaps: no idempotency token yet (a double click could create two decisions); no edit history "
              "switched on (the decision objects themselves are the audit trail); the reviewer shows as a user ID, "
              "not a name; only the owner can submit. The two test decisions should be deleted before a real "
              "pilot, or kept as evidence.")
    r.gate("Write-back", [
        ("Required evidence", "A decision submitted from the app survives a rebuild of the data and a reload."),
        ("Result", "Met three times (step 6, step 8, baseline gate)."),
        ("If it fails", "If decisions vanished after a rebuild, the officer would lose her history and stop "
                        "trusting the tool: rerun the forced-rebuild test after any change to the Action."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 06 NAION trace
    r.chapter("Walking one flag back to its source: NAION")
    r.p("**The trust rule in practice. Take the top signal for semaglutide and follow the links until you "
        "reach FAERS rows and the DailyMed label.**")
    r.p("NAION (non-arteritic anterior ischaemic optic neuropathy, a sudden loss of vision from poor blood "
        "flow to the optic nerve) is reported in FAERS as *{{n:signals.naion.reaction}}*. With the drug filter "
        "set to {{n:signals.naion.drug}}, it is rank {{n:signals.naion.rank}} on the *Not in label* page.")
    crop_figure(r, SCREENS + "app-1c-labels-searched-naion.jpg", [(0.555, 0.34, 1, 1)],
                "Page 1 of the app with NAION selected (right panel, cropped): the signal record (reports, PRR, CI, "
                "chi-squared, label status) and the panel *Reference labels searched*: Ozempic v20, Wegovy v19 and "
                "oral Ozempic v14, each with its effective date, the safety sections searched and a DailyMed link.",
                "docs/11-handin/screens/app-1c-labels-searched-naion.jpg (Workshop, 2026-11-05)", max_height=330)
    r.h("The trace, one hop at a time")
    r.table(["#", "Object and link", "What you see", "Evidence"], [
        ("1", "**MSSM Signal** `…|Optic ischaemic neuropathy|prr_evans_v2`",
         "Rank {{n:signals.naion.rank}}, label status not_in_label, label check method `text+ai_v1+syn_v2`, "
         "bucket clinical, no caution.", "[[OBSERVED]]"),
        ("2", "→ **MSSM AE Stat** (Signal → AE Stat)",
         "a = {{n:signals.naion.a}} reports with this drug and reaction, out of {{n:signals.naion.all_reports_drug}} "
         "for the drug. PRR {{n:signals.naion.prr}} (95% CI {{n:signals.naion.prr_ci_low}} to "
         "{{n:signals.naion.prr_ci_high}}), χ² {{n:signals.naion.chi2_yates}}. Window FAERS {{n:scope.faers_quarters}}.",
         "[[OBSERVED]]"),
        ("3", "→ **MSSM Drug** (Signal → Drug)", "Semaglutide, keyed by its ingredient RxCUI.", "[[OBSERVED]]"),
        ("4", "→ **MSSM Products** (Drug ↔ Product)", "Every semaglutide application (injection and tablet).",
         "[[OBSERVED]]"),
        ("5", "→ **Reference Label** (Product → Label)",
         "The exact label version searched for each product: Ozempic v20, Wegovy v19, oral Ozempic v14 "
         "({{n:app.labels_searched_naion}} labels). Page 1 shows them in the panel *Reference labels searched*, "
         "walking the same links.", "[[OBSERVED]]"),
        ("5b", "→ **MSSM Labeled Reactions** (Labeled Reaction → Label)",
         "What the AI read in those {{n:app.labels_read_by_ai_naion}} labels, each with its word-for-word quote "
         "(page 1 table *What the AI read in these labels*). Diabetic retinopathy is there; no optic-nerve or "
         "NAION term is.", "[[OBSERVED]]"),
        ("6", "→ DailyMed", "The setid opens the label on DailyMed; the version number says which one.",
         "[[OBSERVED]]"),
        ("7", "→ FAERS case ids", "`clean_faers_drug_reaction` (SQL by drug and reaction) gives the report ids "
                                  "behind a: reachable by query, not yet from her screen.", "[[OBSERVED]]"),
    ], widths=[0.35, 2.2, 3.6, 0.9])
    crop_figure(r, SCREENS + "hood-object-explorer-naion-links.jpg", [(0.26, 0.19, 1, 0.45)],
                "Object Explorer (cropped), NAION signal, Links tab: MSSM AE Stat (1) and MSSM Drug (1). The extra row "
                "'Drug of signal' is the duplicate link type from chapter 4, deleted on 6 Nov after this screenshot.",
                "docs/11-handin/screens/hood-object-explorer-naion-links.jpg (Foundry, 2026-11-05)")
    r.p("**What the trace proves.** NAION is not a wording miss. It was not found in the 3 reference labels by "
        "the exact-term and synonym checks, and the AI, which read all 3, found diabetic-retinopathy terms but "
        "no optic-nerve or NAION term. "
        "A wider look at all 36 safety sections of every semaglutide label in DailyMed found no mention either "
        "(A014; DECISIONS learnings, 2026-11-05) [[OBSERVED]]. So it is a *not in label* signal in our data, and "
        "outside our data a *known positive*, not a discovery (EMA PRAC, 6 Jun 2025; WHO alert, 27 Jun 2025; "
        "DECISIONS learning 2026-11-05). It is still not "
        "proof that semaglutide causes NAION: FAERS counts reports, and reporting rises after media attention "
        "[[ASSUMED]]. The count may also be low: the idea is spread over about 10 related optic terms, and this "
        "signal counts only one (DQ41).")
    r.how_we_know(["At the baseline gate, five ranked signals were drawn at random (seed recorded) and re-derived "
                   "by hand: the count *a* recounted from FAERS rows, and the term searched in every safety section "
                   "of the drug's reference labels. All five matched (baseline-gate.md) [[OBSERVED]]. The click path above is written there for a reviewer to repeat."])
    crop_figure(r, SCREENS + "app-1e-ai-quotes-panel-naion.jpg", [(0.42, 0.53, 1, 1)],
                "Page 1, NAION selected, right column scrolled down (cropped): *Reference labels searched* (3 labels "
                "with DailyMed links) and, below it, *What the AI read in these labels*: reaction, section, the quote "
                "word for word, and the label key. For semaglutide the table has {{n:app.ai_quotes_panel_rows_naion}} "
                "rows; none is an optic-nerve term.",
                "docs/11-handin/screens/app-1e-ai-quotes-panel-naion.jpg (Workshop {{n:app.workshop_version|raw}}, 2026-11-06)",
                max_height=300)
    r.warning("A *not in label* signal has no matching label quote (there is nothing to match). What the officer "
              "gets instead is the list of label versions searched, with DailyMed links, and what the AI read in "
              "them, by walking Signal → Drug → Products → Reference Label → Labeled Reactions. There is still no "
              "dedicated Signal → Label link type (item 1 in chapter 7).", title="Watch out")
    r.gate("Trace to source", [
        ("Required evidence", "From a flag on screen, reach the FAERS rows and the exact label version by following "
                              "links, with no step that needs a developer."),
        ("Result", "Met for NAION and for five random signals. The labels searched and the AI's quotes from them "
                   "are on page 1 (panels *Reference labels searched* and *What the AI read in these labels*), "
                   "through existing links."),
        ("If it fails", "Any flag that cannot be traced is noise to the officer: fix the link, do not hide the flag."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 07 next
    r.chapter("What a second engineer would add next")
    r.p("**The brief asks that another engineer could extend this without asking. Here is the list we would "
        "hand them, in order, with the reason for each.**")
    r.table(["#", "Add or fix", "Why", "Effort guess"], [
        ("1", "Optional: a dedicated Signal → searched Labels link type (join dataset written by `ontology_signals.py`)",
         "Page 1 already shows the labels searched through existing links; a dedicated link would make the "
         "trace one hop in Object Explorer too.", "half a day"),
        ("2", "Idempotency token on the triage Action", "Stops a double click from creating two decisions "
                                                        "(project conventions, section 6 on Actions; open since A010).", "hours"),
        ("3", "Link Change Event → Drug (and → Signal / Recall / Label by key)",
         "Today the change feed is filtered by drug name; a link lets the officer jump to the changed object.",
         "half a day"),
        ("4", "Object type for `monitoring_checks` (needs a key column)",
         "Enables a Health page in the app (R04; D046).", "half a day"),
        ("5", "Triage on recalls, not only signals", "The Action already has a Subject Type; a Triage Decision → "
                                                     "Recall link would make it usable.", "hours"),
        ("6", "A per-user 'last reviewed' marker", "Turns the date filter on page 3 into 'since my last review' "
                                                   "automatically (an alternative named in D045).", "a day"),
        ("7", "Object descriptions, edit history on Triage Decision, move the Reference Label link into "
              "`Ontology/Links`, promote types from Experimental", "Housekeeping that a production owner expects "
                                                                  "(A010 known gaps).", "hours"),
        ("8", "Widen Labeled Reaction to the other drugs' reference labels (today {{n:ai.pilot_labels}} labels: "
              "oxycodone and semaglutide)",
         "Only after a pharmacist checks the answer key (D041 v2; scope decision D031 v5).", "days, mostly review"),
    ], widths=[0.3, 2.6, 3, 1])
    r.h("How to add an object type without asking anyone")
    r.bullets([
        "Write a transform that outputs one row per object to `Data/curated/ontology_<name>`, and check the key in code.",
        "Create the type in Ontology Manager with the `MSSM` prefix, a readable title and a description.",
        "Many-to-many relationships: add a join dataset. Many-to-one: a foreign-key column on the many side.",
        "Add a row to the tables in `foundry/ontology/README.md` **before** creating anything (the lesson of the "
        "deleted duplicate link).",
        "Prove it: object count = dataset rows, a link count equals the source count, and a forced rebuild keeps "
        "every triage decision.",
    ], numbered=True)
    r.gate("Ready to extend", [
        ("Required evidence", "A written record of every type, link and Action, and a repeatable test for each."),
        ("Result", "Met: `foundry/ontology/README.md`, this report and diagram 31 v2 (with an editable draw.io copy)."),
        ("If it fails", "If the README and Foundry disagree, Foundry wins: update the README the same day."),
    ], status="TESTED")

    r.chapter("Reference", label="A")
    r.h("Figures quoted from project records (not in numbers.json)")
    r.table(["Figure", "Source"], [
        ("MSSM Signal has 25 properties", "screens/README.md (Figure 1)"),
        ("NAION reference labels: Ozempic v20, Wegovy v19, oral Ozempic v14", "screens/README.md (app-1c); diagram 32 v3"),
        ("AI found diabetic-retinopathy terms, no optic-nerve term (semaglutide labels)", "A019; eval/ai-eval-v1.md"),
        ("Duplicate link deleted 6 Nov; usage log showed one Object Explorer read", "foundry/ontology/README.md; DECISIONS learning 2026-11-06"),
        ("NAION: 36 semaglutide safety sections, none mention it", "A014; DECISIONS learnings, 2026-11-05"),
        ("NAION spread over about 10 optic terms", "DQ41, data-issues register"),
        ("Five random ranked signals traced, all matched", "docs/11-handin/baseline-gate.md"),
        ("Test decision on recall D-0338-2026 (step 6)", "A010"),
    ], widths=[300, 204])
    r.numbers_appendix()
