"""R02 Pipelines, raw to ontology: the data pipeline end to end.

Build:  .venv/bin/python tools/handin/build_report.py R02-pipelines-raw-to-ontology
Output: docs/11-handin/reports/pdf/R02-pipelines-raw-to-ontology.pdf

Sources: foundry/README.md, foundry/pipelines/*/README.md, foundry/ontology/README.md, DECISIONS.md
(D016-D047 and learnings), A010-A017, optimization log O1-O3a, data-issues register, numbers.json.
Numbers come from numbers.json via {{n:...}}. A few figures from earlier project records (not in
numbers.json) are typed with their source named next to them and listed in the last table.
Phase D (2026-11-05): diagrams 30 v2, 32 v2, 33 v2; label-check order AI -> text -> synonym; one meaning
for signal / ranked / active recall; Dana callout; readable figures (crops and sideways pages).
"""

META = {
    "id": "R02",
    "title": "Pipelines: raw to ontology",
    "short": "Pipelines",
    "subtitle": "how four public sources become a ranked, traceable review queue",
    "version": "1.1",
    "date": "5 November 2026",
}

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
               "How does raw public data become the ranked signals, recalls and changes the safety officer sees, "
               "and how would another engineer change it?"),
              ("One-line answer",
               "Four public sources land as raw copies; drug identity is resolved once; FAERS, labels and recalls "
               "are cleaned by written rules; curated datasets back the Ontology; a statistics step and a 3-step "
               "label check (AI terms, exact text, reviewed synonyms) produce {{n:signals.ranked}} ranked signals to review. Every rule lives in one file, "
               "so a change has a known ripple.")],
        is_=["The pipeline end to end, in the order data flows",
             "The rules (decisions D0xx) and why each one exists, with real examples: oxycodone and semaglutide",
             "A guide for an engineer who must add a drug, add a source or change a rule"],
        is_not=["A Foundry primer (see R01 for datasets, transforms, Ontology and Workshop)",
                "A list of every data problem (see R07, data judgment)",
                "A medical finding: a signal is disproportionate reporting plus *not found in the label*, not proof that the drug causes the reaction",
                "Reviewed by a pharmacist (pending)"],
        how_to_read="Chapter 1 is the whole pipeline on one page. Chapters 2 to 7 follow the data from source to "
                    "curated datasets. Chapter 8 is the signal statistics. Chapters 9 and 10 cover what runs "
                    "incrementally, the change feed and monitoring. Chapter 11 is for the next engineer. Each "
                    "chapter ends with *how we know*. The evidence labels are printed at the end of chapter 1. "
                    "Codes (D### decision, A### approach, DQ## data issue, O# optimization) and *step N* (a step of "
                    "the 12-step build order; step 9 = first full 13-drug build) are explained in R01 chapter 3. "
                    "Four wide diagrams are printed sideways on their own page so they can be read.",
    )

    # ------------------------------------------------------------------ 01 summary
    r.chapter("The pipeline in one page")
    r.p("The safety officer watches {{n:scope.drugs_formulary}} drugs: {{n:scope.opioids}} opioids and "
        "{{n:scope.glp1}} GLP-1 drugs (diabetes and weight loss). Opioids: oxycodone, hydrocodone, morphine, "
        "fentanyl, hydromorphone, methadone, buprenorphine, tramadol. GLP-1 drugs: semaglutide, liraglutide, "
        "dulaglutide, tirzepatide, exenatide. She asks three questions each morning: which drugs have side "
        "effects reported that the label does not mention; which have an active recall; and what changed since "
        "yesterday. Every flag must trace back to its source.")
    r.table(["Stage", "What happens", "Main output", "Size"], [
        ("1 · Raw", "Pull 4 public sources exactly as received, with request, status and time",
         "`raw_*`", "{{n:raw.dailymed_labels}} labels, {{n:raw.recalls}} recalls"),
        ("2 · Identity", "Resolve drug names to one ingredient key, once, for every later step",
         "`clean_drug_identity`", "{{n:scope.drugs_formulary}} ingredients"),
        ("3 · Clean", "FAERS versions, deletes, roles, duplicates; label safety sections; recalls and NDC matches",
         "`clean_faers_*`, `clean_label_*`, `clean_recall*`", "{{n:faers.cases_current}} current cases"),
        ("4 · Curated", "One row per object; link tables; AI label reading (pilot)", "`ontology_*`", "10 object types"),
        ("5 · Signals", "2×2 counts, PRR, Evans rule, 3-step label check, buckets, rank",
         "`ontology_signal_signals`", "{{n:signals.total}} signals, {{n:signals.ranked}} ranked"),
        ("6 · Change + health", "Dated change events; source as-of; {{n:monitoring.checks_per_build}} checks per build",
         "`ontology_change_events`, `monitoring_*`", "{{n:changes.total}} events"),
    ], widths=[70, 210, 130, 94])
    r.p("Three ideas hold it together [[DESIGNED]]:")
    r.bullets(["**Resolve drug identity once, in clean.** Every count, label and recall joins on the same "
               "ingredient key (RxNorm RxCUI), so no step re-guesses a drug name.",
               "**Write each rule down and give it a version.** The signal rule is `prr_evans_v2`; the label "
               "check is `text+ai_v1+syn_v2`. A decision the officer makes is tied to the exact computation she saw "
               "(an `evaluation_id`).",
               "**Keep what you cannot use.** Unmatched names, error replies, mass reports and uncertain label "
               "matches are kept with a reason, never dropped silently."])
    r.key(["A **signal** ({{n:signals.total}}) is a drug–reaction pair that meets the Evans rule (at least 3 "
           "reports, PRR at least 2, chi-squared at least 4; D006, proposed) **and** whose reaction is not found in any "
           "reference label of that drug ({{n:signals.not_in_label}} *not in label*) or is found only through a "
           "medium-band synonym ({{n:signals.possibly_in_label}} *possibly in label*).",
           "**Ranked** ({{n:signals.ranked}}) is the review queue: signals that are *not in label*, in the "
           "clinical bucket (D016 v3) and less than half carried by mass-polypharmacy reports (D023 v2). It is a "
           "review queue, not {{n:signals.ranked}} findings, and it does not show that a drug causes a reaction. "
           "It was {{n:signals.ranked_history.step9}} at step 9 (the first full build); chapter 11 shows how it fell."],
          title="How to read the headline numbers")
    r.note(["**Signals move only with a new FAERS quarter.** FAERS arrives as quarterly files; at the baseline "
            "gate the newest data was about {{n:monitoring.faers_age_days}} days old (monitoring check "
            "`faers_age_days`). So *what changed since yesterday* almost never contains a new signal; it is mostly "
            "recalls and label versions. FAERS moved to the FDA's new AEMS system in March 2026; the future feed is "
            "not verified (DQ20).",
            "**The Morning brief change card counts the last 30 days** ({{n:changes.last_30_days}} events), not "
            "since yesterday. Page 3's date range narrows it to *since my last review*.",
            "**The AI does not touch her top signal.** The AI read only {{n:ai.pilot_labels}} oxycodone pilot labels; "
            "for semaglutide × NAION it read none, so *not in label* there comes from the exact-text and synonym "
            "checks (chapter 8). NAION is a *known positive*, not a discovery: EMA PRAC (6 Jun 2025) and a WHO "
            "alert (27 Jun 2025) named it, and our 3 US labels do not mention it (DECISIONS learning 2026-11-05). "
            "Only the project owner can submit a triage decision today."],
           title="What this means for Dana (the safety officer)")
    r.gate("Chapter 1: the pipeline answers the three questions", [
        ("Required evidence", "Each question is fed by a named dataset with a count from `numbers.json`."),
        ("Result", "Met: Q1 {{n:signals.ranked}} ranked signals, Q2 {{n:recalls.active}} active recalls, Q3 "
                   "{{n:changes.last_30_days}} changes in the last 30 days (baseline gate, 5 Nov 2026) [[OBSERVED]]."),
        ("If it fails", "The baseline gate (`docs/11-handin/baseline-gate.md`) is re-run before any hand-in."),
    ], status="TESTED")
    r.pill_legend()
    landscape_figure(r, PNG + "30-handin-data-flow-v2.png",
                     "Data flow as built (v2, O3 measured): public sources → `Data/raw` → `Data/clean` (identity "
                     "resolved once) → `Data/curated` → Ontology → Workshop. Dashed borders are incremental or cached "
                     "steps. The product count in the identity box comes from the README, not from `numbers.json`.",
                     "docs/diagrams/png/30-handin-data-flow-v2.png (source docs/diagrams/src/30-handin-data-flow-v2.mmd)")

    # ------------------------------------------------------------------ 02 sources
    r.chapter("Four sources and the raw contract")
    r.p("Figure 1 (the sideways page before this chapter) shows the whole flow from the four sources to the screen.")
    r.table(["Source", "What it is", "Raw datasets", "Rows [[OBSERVED]]"], [
        ("**FAERS** quarterly files", "FDA Adverse Event Reporting System: spontaneous reports of suspected side "
         "effects. Bulk text files, 2026 Q1 and Q2", "`raw_faers_quarter_files`, `_manifest`", "files + manifest"),
        ("**DailyMed** (NLM)", "Official drug labels as SPL XML (Structured Product Labeling), with versions",
         "`raw_dailymed_spl_index`, `_xml`", "{{n:raw.dailymed_labels}} labels"),
        ("**openFDA** (FDA API)", "Recalls (enforcement reports); Drugs@FDA applications; NDC package directory",
         "`raw_openfda_enforcement`, `_drugsfda`, `_ndc`",
         "{{n:raw.recall_rows}} · {{n:raw.drugsfda_rows}} · {{n:raw.ndc_rows}}"),
        ("**RxNorm** (RxNav API)", "US standard drug vocabulary: names, ingredients, salts, related concepts",
         "`raw_rxnorm_lookup`, `_related`", "13 ingredients"),
    ], widths=[95, 200, 129, 80])
    r.h("The raw contract", 3)
    r.bullets(["Keep the original reply (JSON, XML or file) beside a few parsed columns.",
               "Save request parameters, HTTP status, retrieval time and the source's own *last updated*.",
               "A non-200 reply is an **error row**, never a silent gap.",
               "Scope is one `INGREDIENTS` list at the top of each pull file (13 names since step 9).",
               "After every build: row count = the source's own total (`meta.results.total`, file bytes), per drug."])
    r.how_we_know(["All raw counts equal the source totals for each of the 13 drugs, with 0 error rows (A013).",
                   "The count check caught two bugs that raise no error: an openFDA OR search without parentheses "
                   "returned 11 oxycodone recalls instead of 25, and searching only the harmonised `openfda.*` "
                   "field found 47 Drugs@FDA applications instead of 141 (DECISIONS learnings, 2026-11-04)."])

    # ------------------------------------------------------------------ 03 identity
    r.chapter("Drug identity, resolved once", new_page=False)
    r.p("FAERS names drugs in free text: brands, misspellings, doses inside the name. Labels and recalls belong "
        "to *products*, not ingredients. So identity is built once, in `clean_drug_identity.py`, and every later "
        "step joins on its outputs [[DESIGNED]] (D020; D027, proposed).")
    r.table(["Output", "Key", "Rule"], [
        ("`clean_drug_ingredients`", "`ingredient_rxcui`", "The D018 formulary: 13 ingredient RxCUIs (an explicit list, because ATC "
                                                           "classes miss methadone and hydrocodone, DQ31)"),
        ("`clean_drug_identity`", "`lookup_string`", "D020: exact RxNorm ingredient name, then strip salt words "
                                                     "(HYDROCHLORIDE, CITRATE …). **Never substring.** Unmatched names kept"),
        ("`clean_drug_product_map`", "`ingredient_rxcui` + `product_key`", "Product = FDA application number (D039 G2, a check inside decision D039); "
                                                                           "combination products flagged"),
        ("`clean_drug_package_map`", "`package_ndc11`", "11-digit NDC (National Drug Code); no application → `labeler:` key"),
        ("`clean_label_product_map`", "`setid` + `spl_version` + `application_number`",
         "Approval ids read from the label XML; one *reference label* per product = the application owner's label (G3)"),
    ], widths=[130, 120, 254])
    r.p("**Why never substring** [[OBSERVED]]: matching *morphine* as a substring also catches apomorphine and "
        "diamorphine (heroin). In the October prototype (local Python scripts that applied the same rules to the "
        "same FAERS files on 20 October, before we had Foundry) that made morphine rows about 50% too high (DQ34).")
    r.p("**The two levels** (D027, proposed): counts belong to the ingredient (Drug); labels and recalls belong to the "
        "product (application) and package (NDC). Bulk FAERS carries an application number (`nda_num`), so a "
        "report can reach the right label (D024): for example, injected semaglutide and the oral tablet have "
        "different labels (DQ33).")
    r.code("Oxycodone chain (trace T13):\n"
           "RxCUI 7804 → application NDA022272 (OXYCONTIN) → package 59011-410-10\n"
           "          → reference label bfdfe235…, version 44")
    r.how_we_know("Each identity dataset has 0 duplicate keys (Foundry SQL). The OxyContin chain above returns "
                  "exactly one row. The local check `foundry/tools/local_run/check_identity.py` repeats both tests.")

    # ------------------------------------------------------------------ 04 FAERS
    r.chapter("Cleaning FAERS", new_page=False)
    r.p("`clean_faers.py` reads both quarters and writes three outputs [[OBSERVED]]: "
        "`clean_faers_cases_current` ({{n:faers.cases_current}} cases), `clean_faers_case_reactions` "
        "({{n:faers.case_reactions}} rows, every current case, needed as the background for PRR) and "
        "`clean_faers_drug_reaction` ({{n:faers.drug_reaction_rows}} rows for our 13 drugs). Four rules, in order:")
    r.table(["Rule", "What it does", "Why (evidence)"], [
        ("**D022** versions and deletes",
         "Per quarter: keep the highest `caseversion` per `caseid` (newer quarter wins ties), then apply that "
         "quarter's delete list to *all* history",
         "FAERS sends follow-ups in later quarters. Q2 replaced {{n:faers.q2_cases_replaced}} Q1 cases and "
         "deleted {{n:faers.q2_cases_deleted}}. Appending would double count (DQ36) [[OBSERVED]]"),
        ("**D021** suspect roles",
         "Count a drug when it is primary suspect (PS), secondary suspect (SS) or interacting (I); once per "
         "case; never when only concomitant",
         "For oxycodone, primary suspect only would miss 56% of cases; SS often repeats PS (DQ35)"),
        ("**D020** identity", "Split `prod_ai` on `\\`, resolve each part through `clean_drug_identity`; "
                              "blank → whole `drugname`", "One identity rule for every source (chapter 3)"),
        ("**D023 v2** duplicates and mass reports",
         "Fold the same person filed by many companies; then leave every report listing **30 or more drugs** "
         "out of the main count, but keep it as `a_mass_reports`",
         "A Canadian mass-polypharmacy cluster: 465 of 3,408 oxycodone cases, median 122 drugs, ages changing "
         "between filings. It put pemphigus at the top of the list (A012)"),
    ], widths=[95, 200, 209])
    r.p("**Example: oxycodone** [[OBSERVED]]. 4,464 suspect cases before the duplicate fold, 3,408 after "
        "(foundry/README). The ≥30-drug cut then sets 465 of those aside as mass reports.")
    r.how_we_know(["Counts equal the October prototype exactly ({{n:faers.cases_current}} cases; oxycodone 4,464 → 3,408; "
                   "DECISIONS learnings, 2026-11-04). The prototype is our own earlier code, so agreement shows the "
                   "Foundry port is faithful. It does not show the rules are right; the rules are argued in D020 to D023.",
                   "The incremental path (chapter 9) applies the same rules quarter by quarter and gives identical "
                   "rows, which tests D022 independently."])

    # ------------------------------------------------------------------ 05 labels
    r.chapter("Labels and the AI reader", new_page=False)
    r.p("DailyMed is the label source of truth (D019): openFDA's label copy lags it (DQ28). `clean_labels.py` "
        "writes `clean_label_versions` (one row per setid + version, effective date from the XML, modern PLR "
        "format flag) and `clean_label_sections`.")
    r.table(["Safety section", "LOINC code", "Note"], [
        ("Boxed Warning", "34066-1", ""),
        ("Contraindications", "34070-3", ""),
        ("Warnings and Precautions", "43685-7", "Modern (PLR) labels"),
        ("Warnings / Precautions", "34071-1 / 42232-9", "Older labels use two separate sections (DQ19)"),
        ("Adverse Reactions", "34084-4", "Sub-sections 6.1/6.2 use a generic code, so everything nested is folded in (DQ40)"),
    ], widths=[150, 110, 244])
    r.p("**DQ42: a 200 that is not a label** [[OBSERVED]]. For two tramadol repackager labels DailyMed answered "
        "HTTP 200 with the text `None`. The parser crashed. Now raw keeps the reply as received; clean keeps only "
        "text that starts with `<`; the version stays listed with `has_xml = false`.")
    r.h("The AI reader (pilot)", 3)
    r.p("`ai_label_extraction.py` sends each safety section to Claude Sonnet 5.5 through AIP and asks for every "
        "reaction with an **exact quote**. Code checks the quote is in the section text. Results: "
        "{{n:ai.pilot_labels}} labels, {{n:ai.sections}} sections, {{n:ai.reactions}} reactions, "
        "{{n:ai.grounded}} grounded [[OBSERVED]]. The cache key is setid + version + section + text hash + "
        "prompt, parser and model version, so an unchanged label costs {{n:ai.model_calls_on_rebuild}} model calls (O1).")
    r.warning("The AI is a pilot on 2 oxycodone labels and does not change the signal list today: the text check "
              "already covers its terms. It read no semaglutide label, and its quote is not on the officer's screen "
              "yet. Widening it waits for a pharmacist-checked answer key (D041).")
    r.how_we_know(["Grounding: {{n:ai.grounded}} of {{n:ai.reactions}} quotes found word for word, across all "
                   "{{n:ai.sections}} sections [[OBSERVED]].",
                   "Accuracy is a smaller test: F1 {{n:ai.gold_f1}} (proposed D015 target {{n:ai.d015_target_f1}}) on a 35-item "
                   "answer key, the Boxed Warning and Contraindications of the 2 oxycodone labels, written by Claude "
                   "and frozen before the run, no pharmacist yet. The model found " + r.n("ai.gold_recall_strict").replace("/", " of ") + " "
                   "answer-key items (`eval/ai-eval-v1.md`).",
                   "Label versions: {{n:labels.total}}, 0 version mismatches against the DailyMed index."])

    # ------------------------------------------------------------------ 06 recalls
    r.chapter("Recalls", new_page=False)
    r.p("`clean_recalls.py` writes `clean_recalls_current` ({{n:recalls.total}} recalls; the latest pull wins; "
        "status must be Ongoing, Completed or Terminated) and `clean_recall_product_match`. A recall is "
        "**active** when its status is Ongoing: {{n:recalls.active}} today [[OBSERVED]].")
    r.p("**NDCs come from the recall's own text** [[DESIGNED]]. openFDA attaches every package of an application "
        "to every recall record, so its `openfda.package_ndc` field over-matches. We parse NDCs from the "
        "product description and code info instead, and grade each match:")
    r.table(["Confidence", "Meaning", "Used for the Recall ↔ Product link?"], [
        ("high", "A full package NDC printed in the recall, found in the NDC directory", "yes"),
        ("medium", "A product NDC, or a 10-digit NDC resolved to one package", "yes"),
        ("low", "Only the ingredient name appears in the text", "no (feeds Recall ↔ Drug instead)"),
        ("none", "No NDC in text, NDC not in the directory, or an ambiguous 10-digit NDC; kept with a reason", "no"),
    ], widths=[70, 300, 134])
    r.p("Example: the newest recall, {{n:recalls.newest}} (reported {{n:recalls.newest_reported}}), is a compounded "
        "tirzepatide product. It names our drug, so it shows under tirzepatide, but it matches none of our "
        "products, and the screen says so (*Matched to our products: 0*). A 2027 number with a 2026 date is "
        "not a typo: we take the year to be the FDA's fiscal year, which starts on 1 October [[ASSUMED]].")
    r.how_we_know("Every recall has an ingredient-level row, so none disappears for lack of an NDC. In the oxycodone "
                  "pilot, 20 of 31 printed package NDCs were no longer in the NDC directory, but all 4 active "
                  "recalls matched a listed package (DECISIONS learnings, 2026-11-04).")

    # ------------------------------------------------------------------ 07 curated
    r.chapter("Curated datasets: what backs the Ontology", new_page=False)
    r.p("`ontology_objects.py` turns clean data into one row per object and one row per link, in `Data/curated`. "
        "Keys are checked for nulls and duplicates before Foundry indexes them [[OBSERVED]].")
    r.table(["Curated dataset", "Object or link", "Key"], [
        ("`ontology_drug_drugs`", "MSSM Drug ({{n:scope.drugs_formulary}})", "`ingredient_rxcui`"),
        ("`ontology_product_products`", "MSSM Product, with its reference label", "`product_key`"),
        ("`ontology_label_labels`", "MSSM Label ({{n:labels.total}}), with DailyMed URL", "`label_key` = setid|v<version>"),
        ("`ontology_recall_recalls`", "MSSM Recall ({{n:recalls.total}})", "`recall_number`"),
        ("`ontology_link_*` (4 tables)", "Drug↔Product, Product↔Label, Recall↔Product, Recall↔Drug", "`link_key`"),
        ("`ontology_labeled_reactions`", "MSSM Labeled Reaction ({{n:ai.reactions}}, AI)", "`labeled_reaction_key`"),
        ("`ontology_ae_stats`", "MSSM AE Stat ({{n:signals.ae_stats}})", "`stat_key`"),
        ("`ontology_signal_signals`", "MSSM Signal ({{n:signals.total}})", "`signal_key` = rxcui|reaction|rule"),
        ("`ontology_change_events`, `ontology_source_status`", "MSSM Change Event, MSSM Source Status", "`event_id`, `source`"),
        ("`ontology_triage_decisions`", "MSSM Triage Decision: empty; rows come from the Action", "`decision_id`"),
    ], widths=[170, 210, 124])
    r.p("The curated layer is where *grain* is fixed: one signal per drug × reaction × rule; one label per setid × "
        "version. The Ontology adds nothing the dataset does not hold, except the officer's decisions [[DESIGNED]] (D040).")
    r.how_we_know("Object counts in Foundry equal the dataset rows; 0 null and 0 duplicate keys in all curated tables (A013).")

    # ------------------------------------------------------------------ 08 signals
    r.chapter("Signal statistics and the label check", new_page=False)
    r.p("Figure 2 (after step D) follows one FAERS report to a ranked signal in four stages: clean the "
        "reports (A), count and test (B), check the label (C), sort the queue (D). It is printed in two parts so "
        "the boxes can be read.")
    r.h("Step B: count and test", 3)
    r.p("For each drug × reaction, `ontology_signals.py` builds a 2×2 table: *a* = reports with this drug and this "
        "reaction; *b* = this drug, other reactions; *c* = other drugs, this reaction; *d* = the rest. "
        "**PRR** (proportional reporting ratio) = (a / all reports for the drug) ÷ (c / all reports for other "
        "drugs), with a 95% confidence interval and a Yates chi-squared. The **Evans rule** flags a ≥ 3, PRR ≥ 2 "
        "and chi-squared ≥ 4 (D006, proposed). Output: {{n:signals.ae_stats}} drug × reaction rows (*stats*) in "
        "`ontology_ae_stats`; diagram 32 counts 2,533 of them meeting Evans.")
    r.h("Step C: is it in the label? Three checks", 3)
    r.p("Every stat is checked against the safety sections of the drug's **reference labels** (one per product, "
        "the application owner's label; D039 G3). The code tries the checks in the order below and stops at the "
        "first hit (`ontology_signals.py` l.163–176). The outcome would be the same in any order; only the "
        "recorded `label_match_method` differs. The version string `text+ai_v1+syn_v2` names the rule versions, "
        "not the order.")
    r.table(["Check", "Rule", "Outcome"], [
        ("1 · AI terms (D041)", "An atomic term the AI extracted, with a quote the code found word for word, equals "
                                "the FAERS term. Only the {{n:ai.pilot_labels}} oxycodone pilot labels have AI terms", "in label"),
        ("2 · Text (D037, proposed)", "The exact FAERS term or its US spelling appears in a safety section of the "
                                      "drug's reference labels", "in label"),
        ("3 · Synonyms (D043)", "A reviewed phrase for the term appears in those sections. Band **high** → in label; "
                                "**medium** → *possibly in label* (kept, not ranked); **rejected** rows kept for audit", "in / possibly"),
    ], widths=[110, 320, 74])
    r.p("The synonym table `label_synonyms.py` (version {{n:synonyms.version}}) has {{n:synonyms.rows}} rows: "
        "{{n:synonyms.high}} high, {{n:synonyms.medium}} medium, {{n:synonyms.rejected}} rejected. A script "
        "proposes leads; a person sets the band (so far Claude; pharmacist pending).")
    r.h("Step D: from 1,952 signals to 1,073 ranked", 3)
    r.table(["Group", "Count", "Rule (`ontology_signals.py` l.194–200)"], [
        ("Signals", "{{n:signals.total}}", "Evans **and** (not in label **or** possibly in label)"),
        ("· not in label", "{{n:signals.not_in_label}}", "No check found the term in any reference label"),
        ("· possibly in label", "{{n:signals.possibly_in_label}}", "Found only through a medium-band synonym: kept with a caution, never ranked"),
        ("Ranked (the review queue)", "{{n:signals.ranked}}", "Not in label **and** clinical bucket **and** mass-report share under 0.5"),
        ("Not in label but not ranked", f"{r.n('signals.not_in_label') - r.n('signals.ranked'):,} [[DERIVED]]",
         "In a tagged bucket (D016 v3: abuse/overdose, product use and errors, efficacy, pregnancy, social/legal, "
         "administrative) or mostly from mass reports (diagram 32 counts 231 signals with that caution)"),
    ], widths=[150, 70, 284])
    r.p("**Buckets** are keyword groups (D016 v3), a stand-in for MedDRA groupings we cannot license. The "
        "**mass-report share** is a_mass ÷ (a + a_mass), where a_mass counts reports listing 30 or more drugs, "
        "which were left out of *a* (D023 v2, `ontology_signals.py` l.196). A share of 0.5 or more means the "
        "reaction is mostly carried by those re-filed reports, so it gets a caution instead of a rank.")
    r.p("Ranked signals are ordered by chi-squared within each drug (D042). D042 records the choice, not a "
        "comparison: chi-squared grows with both the size and the strength of the excess, while ordering by the "
        "PRR's lower confidence bound is an alternative we have not tested [[DESIGNED]]. Every signal carries an "
        "`evaluation_id`, a hash of its key, count, PRR, label check, window, number of labels searched and "
        "number of AI-read labels, so a decision is pinned to what the officer saw [[DESIGNED]].")
    crop_figure(r, PNG + "32-handin-signal-pipeline-v2.png", [(0, 0.04, 0.505, 0.99), (0.515, 0.345, 0.99, 0.685)],
                "From one FAERS report to a ranked signal (v2), with real numbers for semaglutide × NAION. Top: "
                "stages A to C. Bottom: stage D. Read two units with care. **Stats** in stage C are all "
                "{{n:signals.ae_stats}} drug × reaction rows, flagged or not (for example *possibly (211 stats)*). "
                "**Signals** in stage D are only the Evans rows that are not, or only possibly, in the label (for "
                "example *possibly in label · {{n:signals.possibly_in_label}}*). The NAION box counts the 3 "
                "*reference labels* searched; the text below also quotes a wider manual look at all 36 safety "
                "sections of every semaglutide label in DailyMed (A014).",
                "docs/diagrams/png/32-handin-signal-pipeline-v2.png (source docs/diagrams/src/32-handin-signal-pipeline-v2.mmd)",
                max_height=400)
    r.h("Worked example: semaglutide × NAION", 3)
    r.table(["Item", "Value", "Evidence"], [
        ("Reaction (MedDRA preferred term)", "{{n:signals.naion.reaction}} (NAION)", "[[OBSERVED]]"),
        ("a: reports with semaglutide and NAION", "{{n:signals.naion.a}} of {{n:signals.naion.all_reports_drug}} semaglutide reports", "[[OBSERVED]]"),
        ("PRR (95% CI)", "{{n:signals.naion.prr}} ({{n:signals.naion.prr_ci_low}} – {{n:signals.naion.prr_ci_high}})", "[[DERIVED]]"),
        ("Chi-squared (Yates)", "{{n:signals.naion.chi2_yates|,.1f}}", "[[DERIVED]]"),
        ("Label check", "Not found in the {{n:app.labels_searched_naion}} reference labels searched (Ozempic v20, "
                        "Wegovy v19, oral Ozempic v14). The AI read none of them, so this comes from the text and "
                        "synonym checks. A wider manual look found NAION in none of the 36 safety sections of any "
                        "semaglutide label in DailyMed (A014)", "[[OBSERVED]]"),
        ("Rank for semaglutide", "{{n:signals.naion.rank}}", "[[DERIVED]]"),
    ], widths=[170, 270, 64])
    crop_figure(r, SCREENS + "app-1c-labels-searched-naion.jpg", [(0.555, 0.34, 1, 1)],
                "The same signal on page 1 of the app (right panel, cropped): {{n:signals.naion.a}} reports, PRR "
                "{{n:signals.naion.prr}}, label status not_in_label, and the panel *Reference labels searched* with "
                "the {{n:app.labels_searched_naion}} labels and their DailyMed links.",
                "docs/11-handin/screens/app-1c-labels-searched-naion.jpg (Foundry, 2026-11-05)", max_height=330)
    r.how_we_know(["PRR equals the October prototype on the same quarters (A012).",
                   "Baseline gate: 5 random ranked signals re-derived by hand; `a` recounted from FAERS rows matched "
                   "5/5, and the term was in no reference-label safety section (`baseline-gate.md`)."])

    # ------------------------------------------------------------------ 09 incremental
    r.chapter("What runs incrementally, and what it saved", new_page=False)
    r.p("Figure 4 (sideways, after chapter 10) draws both pieces: full vs incremental FAERS, and DailyMed XML reuse.")
    r.table(["#", "Pipeline", "Before", "After", "Helped?"], [
        ("O1", "AI extraction cache", "{{n:optimization.O1.before_calls}} model calls, {{n:optimization.O1.before_tokens}} tokens",
         "{{n:optimization.O1.after_calls}} calls, {{n:optimization.O1.after_tokens}} tokens on rebuild", "Yes"),
        ("O2", "Incremental FAERS (A015, D044)", "Full rebuild {{n:optimization.O2.full_rebuild_s}} s",
         "Adding Q2: {{n:optimization.O2.state_s}} s state + {{n:optimization.O2.outputs_s}} s outputs = "
         "{{n:optimization.O2.incremental_add_q2_s}} s", "**No**"),
        ("O3", "DailyMed XML reuse (D047, proposed)", "{{n:optimization.O3.before_downloads}} downloads, {{n:optimization.O3.before_s}} s",
         "{{n:optimization.O3.after_downloads}} downloads ({{n:optimization.O3.reused}} reused), {{n:optimization.O3.after_s}} s", "Yes"),
        ("O3a", "FAERS column pruning", "local {{n:optimization.O3a.local_run_before_s}} s", "local {{n:optimization.O3a.local_run_after_s}} s", "**No**"),
    ], widths=[30, 130, 120, 170, 54])
    r.p("**Incremental FAERS** (`clean_faers_incremental.py`) keeps a *state* (current cases, suspects, reactions) "
        "and a per-quarter log. Each build adds the oldest new quarter with the D022 rule; if drug identity changes, "
        "it replays every quarter as a new generation. It shares `suspects()` and `finish()` with the full rebuild, "
        "so the two paths cannot drift. Its outputs are identical to the full rebuild (EXCEPT ALL both ways = 0 rows), "
        "but at two quarters it is slower: reading back and rewriting the state costs more than parsing one quarter "
        "saves. So **signals still read the full rebuild** [[OBSERVED]] (O2). Re-measure at 4+ quarters.")
    r.p("**DailyMed reuse** reads its own previous output and downloads only new versions and non-XML replies "
        "(the 2 DQ42 labels, re-tried on purpose). The index is still pulled every build, so a new version is "
        "fetched the same day. The baseline came from an earlier build, not back to back (O3).")
    r.p("**FAERS column pruning** (O3a) read fewer columns from the FAERS files. Locally it did not change the "
        "run time, so it was reverted.")
    r.how_we_know("Build times from the Foundry Builds page; row equality from SQL; see "
                  "`docs/08-optimization-log/optimization-log.md`. The two *No* rows stay in the log on purpose.")

    # ------------------------------------------------------------------ 10 changes + monitoring
    r.chapter("Change feed and monitoring", new_page=False)
    r.status("PROPOSED", "D045 (change feed) and D046 (monitoring) are built and tested but still await the project "
                         "owner's OK (the person accountable for this build). Until then they are working pilot features.")
    r.p("Figure 5 (sideways, after Figure 4) shows the two ways a change is found.")
    r.p("`ontology_changes.py` writes one row per change to a signal, recall or label. **Source-dated** events give "
        "real history from the first build: {{n:changes.recall_reported}} recalls reported, "
        "{{n:changes.recall_terminated}} terminated, {{n:changes.label_version_effective}} label versions effective "
        "(the {{n:changes.label_version_effective}} of {{n:labels.total}} label versions that carry an effective "
        "date) = {{n:changes.source_date}} events. **Snapshot-diff** events compare watched fields (label status, ranked, "
        "bucket, caution; recall status and class; label version) with the previous build. A rebuild with the same "
        "data added {{n:changes.snapshot_diff_after_rebuild}} events, as it should [[OBSERVED]]. *Since her last "
        "review* is a date filter on page 3, not a stored bookmark [[DESIGNED]]. The Morning brief card counts the "
        "last 30 days ({{n:changes.last_30_days}} events).")
    r.p("`monitoring.py` appends {{n:monitoring.checks_per_build}} checks per build to `monitoring_checks` (keys, "
        "row-count drops over 20%, freshness per source, AI grounded rate ≥ 0.95, cache hits, FAERS reporter-type "
        "blanks, ranked signals with no reference label) and rebuilds `monitoring_drift` as a **historical replay** "
        "from source dates (last 4 weeks vs the 4 before). Foundry Data Health adds "
        "{{n:monitoring.data_health_checks}} checks. Two real warnings so far: reporter type blank "
        "{{n:monitoring.reporter_type_blank_q1|.0%}} → {{n:monitoring.reporter_type_blank_q2|.0%}}, and recalls "
        "{{n:monitoring.recalls_last4w}} vs {{n:monitoring.recalls_prev4w}}.")
    r.how_we_know(["Locally, a planted change (one signal edited, one recall removed) produced exactly 3 events (A016). "
                   "Monitoring has run {{n:monitoring.runs}} times in Foundry (A017).",
                   "Freshness at the gate: openFDA {{n:monitoring.openfda_age_days}} days, FAERS "
                   "{{n:monitoring.faers_age_days}} days. For openFDA that is normal for a weekly feed. For FAERS it "
                   "is the normal lag of a quarterly file, and it means the signal list is about four months old "
                   "on any given morning."])
    landscape_figure(r, PNG + "33-handin-incremental-faers-v2.png",
                     "Full vs incremental FAERS (top) and DailyMed XML reuse (bottom), v2 with O3 measured. "
                     "*DEMO* is the FAERS case file (one row per case version, with the patient's age and sex).",
                     "docs/diagrams/png/33-handin-incremental-faers-v2.png (source docs/diagrams/src/33-handin-incremental-faers-v2.mmd)")
    landscape_figure(r, PNG + "34-handin-change-feed-v1.png",
                     "Two ways to know something changed: dates the source carries (A) and comparing this build with "
                     "the last (B). Both feed MSSM Change Event, page 3 and the Morning brief.",
                     "docs/diagrams/png/34-handin-change-feed-v1.png")

    # ------------------------------------------------------------------ 11 extend
    r.chapter("How another engineer extends this")
    r.p("Every rule lives in one file. Change it in the GitHub mirror (`foundry/`), test with the local runner, "
        "paste into Foundry, commit, then build **in dependency order**. The ripple map (Figure 6, the sideways "
        "page after the table) shows what moves.")
    r.table(["Change", "Edit this", "Rebuild, in order", "What else moves"], [
        ("**Add a drug**", "`INGREDIENTS` in the 4 API pull files (`raw_openfda_enforcement.py`, `raw_openfda_products.py`, "
                           "`raw_dailymed_spl.py`, `raw_rxnorm.py`) and `FORMULARY` (RxCUI, name, class) in `clean_drug_identity.py`",
         "raw pulls → identity → labels, FAERS, recalls → `ontology_objects` → signals → changes → monitoring",
         "Check raw totals per drug. If the drug has no reference label, nothing is shown as *not in label* (G4)"),
        ("**Add a source**", "New Data Connection source + egress policy; a raw transform in `pipelines_raw_ingest`; a clean "
                             "transform in `pipelines_clean` that joins on `ingredient_rxcui` or `product_key`",
         "new raw → new clean → the curated or signal step that uses it",
         "Write its contract (grain, key, refresh) first; add a freshness check in `monitoring.py`"),
        ("**Change a synonym**", "A row in `label_synonyms.py`; bump `SYN_VERSION`",
         "`ontology_signals` → changes → monitoring", "Label check string changes → every `evaluation_id` changes; old "
         "decisions keep the old id. The past-decisions table shows that id, so a mismatch is visible, but the screen "
         "does not flag it yet [[PLANNED]]"),
        ("**Change a bucket**", "The regex in `BUCKETS` in `ontology_signals.py`", "`ontology_signals` → changes",
         "Only the ranked queue moves; evaluation ids stay, so decisions stay linked"),
        ("**Change a threshold**", "`MAX_DRUG_ROWS` or the Evans test in `ontology_signals.py`; bump `RULE`",
         "`ontology_signals` → changes", "New rule → new `signal_key`s; record a new decision version"),
        ("**Change identity**", "A salt word or name rule in `clean_drug_identity.py`",
         "identity → FAERS (full; the incremental state replays) → signals", "Suspect rows change for every quarter"),
    ], widths=[70, 170, 140, 124])
    r.warning(["Data Lineage *build all ancestors* re-runs every raw pull and the 700 MB FAERS download. Build file by file.",
               "The repository Build button may skip an unchanged incremental transform: build from the dataset page "
               "(Build ▾ → Force) and check History.",
               "Record a changed rule as a new decision version in DECISIONS.md; never edit one in place."],
              title="Three habits that save an afternoon")
    landscape_figure(r, PNG + "37-handin-ripple-v2.png",
                     "Ripple map v2: nine changes, each traced to what moves downstream, whether the evaluation id moves, "
                     "what the officer sees, and existing triage decisions (they stay linked in every row; there is no "
                     "stale flag yet, a known gap). Checked against the code (docs/11-handin/demo/ripple-table.md).",
                     "docs/diagrams/png/37-handin-ripple-v2.png")
    r.gate("Chapter 11: another engineer can extend it without asking", [
        ("Required evidence", "Each common change names the file to edit, the rebuild order and its side effects."),
        ("Result", "Met for six changes. The ranked queue was {{n:signals.ranked_history.step9}} at step 9; the "
                   "first synonym table took it to {{n:signals.ranked_history.syn_v1}}; two later changes were done "
                   "for real with this guide: buckets D016 v3 ({{n:signals.ranked_history.syn_v1}} → "
                   "{{n:signals.ranked_history.d016_v3}}) and synonyms syn_v2 ({{n:signals.ranked_history.d016_v3}} → "
                   "{{n:signals.ranked_history.syn_v2}}) [[OBSERVED]]."),
        ("If it fails", "Add the missing step to `foundry/README.md` (How a change reaches Foundry)."),
    ], status="TESTED")

    r.chapter("Where the numbers come from", label="A", new_page=False)
    r.h("Figures quoted from project records (not in numbers.json)")
    r.p("These come from earlier measured records, not from the baseline-gate capture. They are quoted with their source.", style="small")
    r.table(["Figure", "Source"], [
        ("openFDA OR search 11 vs 25 recalls; `openfda.*` 47 vs 141 applications", "DECISIONS learnings, 2026-11-04"),
        ("Morphine substring match about +50% rows", "DQ34, data-issues register (prototype, 2026-10-20)"),
        ("Oxycodone 4,464 → 3,408 cases after fold; 465 mass reports, median 122 drugs", "foundry/README.md; D023 v2; A012"),
        ("Primary-suspect-only would miss 56% of oxycodone cases", "DECISIONS learnings, 2026-11-04"),
        ("NAION: 36 semaglutide safety sections, none mention it", "A014; DECISIONS learnings, 2026-11-05"),
        ("20 of 31 printed oxycodone recall NDCs not in the directory", "DECISIONS learnings, 2026-11-04"),
        ("Planted change → exactly 3 events", "A016"),
        ("Oxycodone 4,464 → 3,408 equals the October prototype", "DECISIONS learnings, 2026-11-04"),
        ("2,533 stats meet Evans; 1,427 / 8 / 163 stats in label by text / AI / synonym; 211 stats possibly; "
         "231 signals with the mass-report caution", "Diagram 32 v2 (docs/diagrams/src/32-handin-signal-pipeline-v2.mmd)"),
        ("Ozempic v20, Wegovy v19, oral Ozempic v14 (NAION reference labels)", "screens/README.md (app-1c); diagram 32 v2"),
    ], widths=[300, 204])
    r.numbers_appendix()
