"""R00 Start here: the front door to the Medication Safety Signal Monitor hand-in.

Build:  .venv/bin/python tools/handin/build_report.py R00-start-here
Output: docs/11-handin/reports/pdf/R00-start-here.pdf

Answers first-time-reader blocker X1 (no front door), and lifts X3/X5/X8 material to the front:
what the project is, what to read in which order, one glossary, a key to the ID codes, the evidence
legend, five headline numbers with one meaning each, and the facts that change Dana's morning.
Definitions are copied from docs/11-handin/reviews/phase-d-fix-brief.md. Every number comes from
docs/11-handin/numbers.json via {{n:...}}; figures from other records name that record inline.
Kept to three pages on purpose: sections are headings, not chapters, and tables are compact.
"""

import style as S  # tools/handin/style.py (on sys.path when built by build_report.py)

META = {
    "id": "R00",
    "title": "Start here",
    "short": "Start here",
    "subtitle": "what this is, what to read first, and what the words mean",
    "version": "1.1",
    "date": "6 November 2026",
}

TIGHT = dict(pad=2.2, font=7.5)   # compact tables: this page is a look-up sheet


def build(r):
    found, key_size = r.n("ai.gold_recall_strict").split("/")   # "35/35": items found / answer-key size

    # ------------------------------------------------------------------ cover
    r.cover(
        is_=["The front door to the hand-in set",
             "One glossary, one code key, one evidence legend"],
        is_not=["A results report (the evidence is in R01 to R08)",
                "Clinical advice: a signal is a lead, not proof of harm"],
        how_to_read="Read sections 1 and 2 first. Keep sections 3 to 5 open as look-up tables while you read "
                    "the other reports. Section 6 and the dark box are the facts to remember.",
        contents=False,
    )

    # ------------------------------------------------------------------ 1 what this is
    r.h("1 · What this project is")
    r.table(["", "In one line"], [
        ("The user and her questions",
         "**Dana**, a hospital pharmacy safety officer (fictional persona, R04 ch. 2), asks each morning: (1) Which "
         "drugs have side effects reported that the label does not mention? (2) Which have an active recall? "
         "(3) What has changed since yesterday?"),
        ("The trust rule", "Every flag traces to its source: the label versions searched (DailyMed) and the FDA "
                           "recall record open in one click; the FAERS case reports are reachable by query, not "
                           "yet from her screen."),
        ("The {{n:scope.drugs_formulary}} drugs",
         "**{{n:scope.opioids}} opioids:** oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, "
         "buprenorphine, tramadol. **{{n:scope.glp1}} GLP-1 drugs** (diabetes and weight loss): semaglutide, "
         "liraglutide, dulaglutide, tirzepatide, exenatide. Exenatide has no reference label, so signals exist "
         "for {{n:scope.drugs_with_signals}} of {{n:scope.drugs_formulary}} (D018, D031 v5)."),
        ("Data and platform", "Public data only, no patient records. Built on **Palantir Foundry** with its AI "
                              "layer **AIP**. The app is one Workshop module of {{n:app.pages}} pages "
                              "({{n:app.workshop_version}})."),
    ], widths=[118, 386], **TIGHT)

    # ------------------------------------------------------------------ 2 reading order
    r.h("2 · The hand-in set, in the order to read it")
    r.table(["#", "Read", "It answers"], [
        ("1", "Architecture note: picture and build facts", "What is the whole system? (Skip its decision boxes at first.)"),
        ("2", "R07 Data judgment, chapter 1", "What would messy public data do to the officer's morning?"),
        ("3", "R04 The application, chapters 1–4", "How does the officer use the app, and what does each number mean?"),
        ("4", "R01 Foundry from scratch", "What is Foundry, which parts did we use, and where do I click?"),
        ("5", "R02 Pipelines: raw to ontology", "How does raw public data become signals, recalls and changes?"),
        ("6", "R03 The Ontology (ch. 6 = NAION trace)", "How does a flag link back to its source?"),
        ("7", "R06 Optimization · R08 AI reliability · R07 rest",
         "What did we measure? How often is the AI wrong? Which data problems did we fix or leave?"),
        ("8", "R05 Decisions, and what we did not do", "Why each choice, and what we left out. Read last, as the index."),
        ("+", "Deck and R09 Demo navigation guide", "What the 20-minute demo shows, click by click, and what each stop proves."),
    ], widths=[22, 200, 282], **TIGHT)
    r.p("Files: `docs/11-handin/architecture-note/architecture-note.pdf` · `docs/11-handin/deck/MSSM-demo-deck.pdf` "
        "· `docs/11-handin/reports/pdf/R01…R09`. Order from `docs/11-handin/reviews/first-time-reader.md` §6.",
        style="small")

    # ------------------------------------------------------------------ 3 glossary
    r.h("3 · Glossary")
    foundry = [
        ("Palantir Foundry", "A data platform holding data, the code that cleans it, a model of real things "
                             "and the apps, with version history."),
        ("Dataset", "A versioned table in Foundry. Ours run raw → clean → curated."),
        ("Transform", "Python code that reads datasets and writes one. One run = a *build*."),
        ("Code Repository", "A git repository in Foundry holding the transforms."),
        ("Data Lineage", "The graph of which dataset feeds which, with build status."),
        ("Ontology", "Foundry's layer of objects, links and Actions on curated datasets."),
        ("Object (type)", "One real thing / its kind (Drug); one dataset row each."),
        ("Link type", "A named relationship between two object types, e.g. Signal → Drug."),
        ("Action", "A form that writes to the Ontology: ours saves a Triage Decision (*write-back*)."),
        ("Workshop", "Foundry's point-and-click app builder; Dana's screen is one."),
        ("AIP", "Palantir's AI Platform: language models in pipelines. Ours reads label sections."),
        ("F1", "One test score balancing *found every right item* (recall) and *added no wrong ones* "
               "(precision). 1.0 is perfect."),
        ("NAION", "Sudden sight loss from optic-nerve damage; semaglutide × NAION is our worked example. It is a "
                  "*known positive*, not a discovery: EMA PRAC (6 Jun 2025) and a WHO alert (27 Jun 2025) named it; "
                  "our 3 US labels do not mention it (DECISIONS learning 2026-11-05)."),
    ]
    safety = [
        ("FAERS", "FDA Adverse Event Reporting System: voluntary reports of suspected side effects, "
                  "quarterly. Moved to **AEMS** in March 2026 (DQ20)."),
        ("Case", "One FAERS report of one patient event; only its latest version counts (D022)."),
        ("Suspect drug", "A drug the reporter suspects (primary, secondary, interacting); drugs only *also "
                         "taken* do not count (D021)."),
        ("MedDRA PT", "Preferred term: the standard word for a reaction. Its groupings need a licence we lack."),
        ("2×2 table", "For a drug and reaction: *a* = both; *b* = drug, other reactions; *c* = other drugs, "
                      "this reaction; *d* = the rest."),
        ("PRR", "Proportional reporting ratio = (a ÷ the drug's reports) ÷ (c ÷ other drugs' reports): how "
                "much more often the reaction comes with this drug."),
        ("Evans rule", "A common screen: 3+ reports, PRR ≥ 2, chi-squared ≥ 4 (D006)."),
        ("DailyMed / SPL", "The official US label site / its XML format (Structured Product Labeling). Our "
                           "label truth (D019)."),
        ("Label section", "A titled part of a label. We search Boxed Warning, Contraindications, Warnings "
                          "(and Precautions), Adverse Reactions."),
        ("openFDA", "The FDA's public web API: recall, Drugs@FDA and NDC data."),
        ("Recall", "FDA enforcement report of a product withdrawn or corrected; Class I most serious. "
                   "*Active* = Ongoing."),
        ("RxNorm / RxCUI", "US standard drug vocabulary / its concept id. Our drug key = ingredient RxCUI, "
                           "resolved once (D020)."),
        ("NDC", "National Drug Code: the US code for one package."),
        ("Reference label", "The label versions searched for a drug (Drug → Products → label)."),
    ]
    from itertools import zip_longest
    rows = [(f"**{a[0]}**" if a else "", a[1] if a else "", f"**{b[0]}**" if b else "", b[1] if b else "")
            for a, b in zip_longest(foundry, safety)]
    r.table(["Term", "Plain meaning (Foundry and general)", "Term", "Plain meaning (drug safety)"], rows,
            widths=[64, 188, 64, 188], **TIGHT)

    # ------------------------------------------------------------------ 4 ID codes
    r.h("4 · Key to the ID codes")
    r.table(["Code", "Means", "Look it up in"], [
        ("D###", "A decision (where the brief is silent). `D016 v3` = third version; old ones kept. The owner "
                 "accepted the last 12 open ones in one batch on 6 Nov 2026 (D006, D015, D025–D029, D037, "
                 "D045–D048), plus D041 v2 (the AI also reads the semaglutide labels).", "`docs/06-decisions/DECISIONS.md` (D001–D048)"),
        ("A###", "An approach we tried, with its verdict: kept, dropped or parked.",
         "`docs/05-approaches/INDEX.md` (A000–A019)"),
        ("DQ##", "A data-quality issue found in the public data.",
         "`docs/07-data-quality/data-issues-register.md` (DQ01–DQ43)"),
        ("O#", "An optimization, measured before and after (O1, O1b, O2, O3, O3a).",
         "`docs/08-optimization-log/optimization-log.md`"),
        ("G1–G6", "Gate defaults in the dataset contracts, accepted via D039.",
         "`docs/04-architecture/dataset-contracts-v1.md`"),
        ("Step N", "12-step build order; each step ends with a proof (*gate*). 6–8 = first slice; 9 = all "
                   "13 drugs; 10 = incremental FAERS; 11 = screen + health checks; 12 = hand-in.",
         "`docs/04-architecture/foundry-conventions/project-build-order-v1.md`"),
        ("Baseline gate", "The full rebuild where every hand-in number was frozen.",
         "`docs/11-handin/baseline-gate.md`"),
        ("R##", "A hand-in report, R00 (this page) to R09.", "`docs/11-handin/reports/pdf/`"),
        ("30–38", "Diagrams: 30 data flow (v3), 31 ontology (v2), 32 signal pipeline (v3), 33 incremental (v3), "
                  "34 change feed, 35 monitoring (v2), 36 demo map (v3), 37 ripple map (v3), 38 one-page "
                  "architecture (v2). Older versions are kept.",
         "`docs/diagrams/README-handin.md`"),
    ], widths=[44, 222, 238], **TIGHT)

    # ------------------------------------------------------------------ 5 legend
    r.h("5 · Evidence labels and status bands")
    r.p("Each claim carries an evidence label (what kind of claim); each chapter-closing box a status band (how "
        "far along). Text read live from `tools/handin/style.py`, so it matches every report.", style="small")
    ev, st = list(S.EVIDENCE), list(S.STATUSES) + [None]
    r.table(["Evidence", "Meaning", "Status", "Meaning"],
            [(f"[[{e}]]", S.PILLS[e][3], f"[[{s}]]" if s else "", S.PILLS[s][3] if s else "")
             for e, s in zip(ev, st)],
            widths=[64, 222, 58, 160], **TIGHT)

    # ------------------------------------------------------------------ 6 five numbers
    r.h("6 · Five numbers and what they mean")
    r.table(["Number", "What it means", "Do not read it as", ""], [
        ("**{{n:signals.total}}** signals",
         "Drug–reaction pairs that meet the Evans rule **and** whose reaction is not found in any reference "
         "label of the drug ({{n:signals.not_in_label}} *not in label*) or only via a medium-band synonym "
         "({{n:signals.possibly_in_label}} *possibly in label*).",
         "Proven side effects. It means more reports than expected, not cause.", "[[DERIVED]]"),
        ("**{{n:signals.ranked}}** ranked",
         "The **review queue**: signals *not in label*, in the clinical bucket (D016 v3), under half from mass "
         "reports of 30+ drugs (D023 v2). {{n:signals.ranked_history.step9}} at step 9; synonyms and buckets "
         "cut it.",
         "{{n:signals.ranked}} findings.", "[[DERIVED]]"),
        ("**{{n:recalls.active}}** active recalls",
         "openFDA recalls with status **Ongoing**, out of {{n:recalls.total}} recalls pulled for our ingredients.",
         "*Not terminated* (that would add Completed).", "[[OBSERVED]]"),
        ("**{{n:changes.last_30_days}}** changes",
         "Change events (signal, recall, label) in the **last 30 days** (Morning brief card). Page 3's date "
         "range gives *since my last review* (D045).",
         "Changes since yesterday.", "[[DERIVED]]"),
        ("**F1 {{n:ai.gold_f1}}**",
         "AI label reading on a " + key_size + "-item answer key (Boxed Warning + Contraindications of "
         "{{n:ai.v1_pilot.labels}} oxycodone labels; written by Claude, frozen before the run, no pharmacist yet); "
         "found " + found + " of " + key_size + " items; target {{n:ai.d015_target_f1}} (D015). Separately "
         "**{{n:ai.grounded}}/{{n:ai.reactions}}** extracted terms are grounded (quote found) over all "
         "{{n:ai.sections}} sections of {{n:ai.pilot_labels}} labels (2 oxycodone, 3 semaglutide).",
         "A score for all {{n:ai.reactions}} terms, or for the semaglutide labels (not scored).", "[[DERIVED]]"),
    ], widths=[70, 270, 104, 60], **TIGHT)

    r.key([
        "**FAERS is about {{n:monitoring.faers_age_days}} days behind.** Signals change only when a new FAERS "
        "quarter arrives (here {{n:scope.faers_quarters|raw}}), so *what changed* is mostly recalls and labels.",
        "**FAERS moved to AEMS in March 2026** (DQ20). Where future quarters will come from is not verified yet.",
        "**Only the project owner can submit a Triage Decision today** (R03 ch. 5); giving Dana that right "
        "is a production step.",
        "**The AI's quotes are on her screen** (page 1, *What the AI read in these labels*, Workshop "
        "{{n:app.workshop_version|raw}}; R04 ch. 7).",
        "**Three checks agree NAION is not in the label.** Exact text and synonyms found nothing in the "
        "{{n:app.labels_searched_naion}} semaglutide labels, and the AI, which read all "
        "{{n:app.labels_read_by_ai_naion}}, found diabetic-retinopathy terms but no optic-nerve term.",
        "**The Morning brief *changes* card is the last 30 days**, not since yesterday. Use page 3's date range.",
    ], title="What this means for Dana (the safety officer)")

    r.gate("How we know this page is right", [
        ("Required evidence", f"All {len(r.N.used)} numbers are `docs/11-handin/numbers.json` lookups (captured "
                              + str(r.N.meta.get("captured_at")) + "; keys listed in this page's source file); "
                              "definitions copied from the Phase D fix brief; each code names a real file."),
        ("Result", "Met: builds with no layout problems; every page looked at."),
        ("If it fails", "Fix this page first: the other reports rely on its meanings."),
    ], status="TESTED")
