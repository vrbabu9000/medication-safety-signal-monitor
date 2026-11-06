"""R00 sample: shows every element of the hand-in style kit once.

Build:  .venv/bin/python tools/handin/build_report.py R00-sample
Output: docs/11-handin/reports/pdf/R00-sample.pdf

Copy this file to start a new report (R01-..., R02-...). Text accepts **bold**, *italic*, `code`,
[[OBSERVED]]-style pills and {{n:key.path}} numbers from docs/11-handin/numbers.json.
The content below is a style demonstration, not a hand-in: numbers are provisional placeholders.
"""

META = {
    "id": "R00",
    "title": "Style kit sample",
    "short": "Style kit sample",          # used in the running header
    "subtitle": "every element of a hand-in report, once",
    "version": "0.1",
    "date": "5 November 2026",
}


def build(r):
    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "What does a hand-in report look like, and which building blocks can an author use?"),
              ("One-line answer",
               "A cover, a plain summary, chapters that end with a gate, navy tables, labelled evidence, "
               "figures with a source line, and numbers that come from one file.")],
        is_=["A style demonstration for the hand-in reports",
             "A template to copy for R01 onwards",
             "Built from `docs/11-handin/reports/src/R00-sample.py`"],
        is_not=["A project result: the numbers are provisional placeholders",
                "A replacement for the architecture note or the optimization log",
                "Reviewed by a pharmacist"],
        how_to_read="Read chapter 1 for the summary. Chapter 2 shows each building block with a short "
                    "explanation of when to use it. Every number is looked up from `numbers.json`; the "
                    "table at the end lists them.",
    )

    # ------------------------------------------------------------------ chapter 1
    r.chapter("Summary in plain language")
    r.p("The **Medication Safety Signal Monitor** helps a hospital pharmacy safety officer answer three "
        "morning questions: which drugs have side effects reported that the label does not mention, which "
        "drugs have an active recall, and what changed since yesterday. It runs on **Palantir Foundry** "
        "(a data platform where pipelines, a data model and apps live together).")
    r.p("In the current build, FAERS (the FDA's adverse event report database) gives "
        "{{n:faers.cases_current}} current cases, which become {{n:faers.drug_reaction_rows}} "
        "drug-reaction rows for our drugs. From these, the pipeline produces {{n:signals.total}} "
        "signals, of which {{n:signals.ranked}} are ranked for review and {{n:signals.possibly_in_label}} "
        "are marked *possibly in label*.")
    r.table(["Morning question", "What the screen shows", "Count", "Evidence"], [
        ("1. Side effects not on the label", "Ranked signal queue, label passage next to the AI extraction",
         "{{n:signals.ranked}} ranked", "[[DERIVED]]"),
        ("2. Active recalls", "Recall status per drug, with the FDA enforcement report",
         "{{n:recalls.active}} of {{n:recalls.total}}", "[[OBSERVED]]"),
        ("3. What changed", "Change events since the last review",
         "{{n:changes.events_first_build}} at first build", "[[DERIVED]]"),
    ], widths=[150, 200, 84, 70])
    r.key("Every flag on the screen links back to its source: the FAERS query and report IDs, or the "
          "label set ID, version and section.", title="The trust rule")
    r.gate("Summary is complete", [
        ("Required evidence", "Each of the three questions has a count from `numbers.json` and a source."),
        ("Result", "Met for this sample. The counts are provisional until the baseline gate."),
        ("If it fails", "Do not hand in. Capture the missing number in Foundry SQL first."),
    ], status="PLANNED")

    # ------------------------------------------------------------------ chapter 2
    r.chapter("The building blocks")
    r.p("Each block below has one job. Use the smallest block that does the job.")

    r.h("Evidence labels and status bands")
    r.p("Every claim carries a label that says what kind of claim it is. Labels can sit in a row, inside "
        "a sentence such as this one [[ASSUMED]], or inside a table cell.")
    r.pills(["OBSERVED", "DERIVED", "ASSUMED", "DESIGNED"])
    r.pill_legend()
    r.status("TESTED", "Incremental FAERS gives the same rows as a full rebuild (both directions checked).")
    r.status("PLANNED", "Recall status and *changed since last review* on the Workshop screen.")
    r.status("PROPOSED", "A pharmacist reviews the synonym table before the gold-set run.")

    r.h("Callouts")
    r.note("Use a note for context the reader needs but could skip on a first read.")
    r.warning("Use *watch out* for a known limit, for example: FAERS counts reports, not patients, and "
              "reporting rises after media attention.")
    r.how_we_know(["Use *how we know* to show the evidence behind a claim.",
                   "Example: the incremental and full builds were compared row by row with two "
                   "`EXCEPT` queries; both returned zero rows."])

    r.h("Figures")
    r.p("Figures are PNG files from `docs/diagrams/png/` (decision D017: diagrams are files, never inline "
        "code). The helper scales the image to the page width, keeps its shape, and adds a numbered "
        "caption and a source line.")
    r.figure("docs/diagrams/png/01-architecture-data-flow-v0.png",
             "Data flow from public sources to the safety officer's screen (version 0).",
             source="docs/diagrams/png/01-architecture-data-flow-v0.png (Mermaid source in docs/diagrams/src)")

    r.h("Code and lists")
    r.p("Short code blocks stay on one page:")
    r.code("SELECT drug_rxcui, meddra_pt, COUNT(*) AS n\n"
           "FROM faers_drug_reaction\n"
           "GROUP BY drug_rxcui, meddra_pt   -- one row per drug → reaction")
    r.bullets(["Bulleted lists for things without an order.",
               "Symbols such as →, ≥ and · are drawn by the registered font."])
    r.bullets(["Numbered lists for steps.", "The second step.", "The third step."], numbered=True)

    r.gate("Building blocks render", [
        ("Required evidence", "This PDF builds with no layout problems and every page was looked at."),
        ("Result", "Met: see the hand-in style kit README for what was checked."),
        ("If it fails", "Fix the style kit before writing R01."),
    ], status="TESTED")

    r.numbers_appendix()
