"""R04 Application: how the safety officer uses the Workshop app, click by click, and how it was built.

Build:  .venv/bin/python tools/handin/build_report.py R04-application-workshop
Output: docs/11-handin/reports/pdf/R04-application-workshop.pdf

Sources: foundry/ontology/README.md (Workshop module section, Action types), docs/05-approaches/A012 and A016,
docs/02-design-thinking/design-thinking-canvas.md, DECISIONS D006 / D023 v2 / D042 / D045 / D046 and the learnings
table, docs/11-handin/screens/README.md and the app-* screenshots, reviews/phase-d-fix-brief.md (wording).
Numbers via {{n:...}} from docs/11-handin/numbers.json; other figures cite their record inline and in the
"Figures quoted from project records" table in the appendix.
Phase D (2026-11-05): fact-check W1, S8-S11, S17, U3, X1, X2, X4 and first-time-reader R04 items fixed.
"""

META = {
    "id": "R04",
    "title": "The application",
    "short": "Application",
    "subtitle": "the safety officer's morning in Workshop, click by click, and how it was built",
    "version": "1.1",
    "date": "5 November 2026",
}

SHOT = "docs/11-handin/screens/"


def step(r, title):
    """Step heading that starts a new page unless its screenshot fits below it."""
    from reportlab.platypus import CondPageBreak
    r.flow.append(CondPageBreak(340))
    r.h(title)


def build(r):
    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "How does a hospital pharmacy safety officer use the app each morning, what does each number "
               "mean, and how was the app built (and how is it changed) in Palantir Workshop?"),
              ("One-line answer",
               "One Workshop module with {{n:app.pages}} pages behind header tabs: a Morning brief with three "
               "numbers and the as-of date of each source, then one page per question. On the first question "
               "she can open the exact label versions that were searched, and record a triage decision that is "
               "written back to the Ontology and survives every rebuild.")],
        is_=["A click-by-click guide to the officer's morning, page 0 to page 3, with screenshots of the live app",
             "A plain explanation of every number on the screen, and what it does not mean",
             "A guide to the widgets on the screen and how an editor changes them (Edit mode, variables, "
             "widget config)",
             "An honest list of the gaps and the next UI improvements"],
        is_not=["A user study: the persona is fictional. Load and page-switch times were measured by a script; "
                "a human two-minute walk-through has not been run",
                "The data model behind the screen (see R03, the Ontology)",
                "Proof of drug harm: a signal is a reason to look, not a finding",
                "Reviewed by a pharmacist"],
        how_to_read="Chapter 1 is the one-page summary, with the words you need and what the app means for the "
                    "officer. Chapter 2 introduces her and her three questions. Chapter 3 is the user guide: the "
                    "morning routine, click by click, with screenshots. Chapter 4 explains every number. Chapter 5 "
                    "is for editors: the widgets, the variables, and how to change them. Chapter 6 shows what we "
                    "changed for usability and why. Chapter 7 lists the gaps and the next UI improvements. Each "
                    "chapter ends with a gate box: what we required, what we found, and what to do if it fails.",
    )

    # ------------------------------------------------------------------ 01 summary
    r.chapter("Summary in plain language")
    r.p("**Who and why.** A hospital pharmacy safety officer has about fifteen minutes each morning for safety "
        "review (design-thinking canvas; an assumption, not a measurement). She asks three questions: (1) which "
        "drugs have side effects being reported that the label does not mention, (2) which drugs have an active "
        "recall, (3) what has changed since yesterday. She trusts a flag only if she can see its source.")
    r.p("**Which drugs.** Her formulary in this pilot is {{n:scope.drugs_formulary}} drugs: {{n:scope.opioids}} "
        "opioids (oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, buprenorphine, tramadol) "
        "and {{n:scope.glp1}} GLP-1 medicines (semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide).")
    r.h("Words used in this report")
    r.table(["Word", "Meaning"], [
        ("Foundry", "Palantir's data platform. Our data, pipelines, data model and app all live in one Foundry project."),
        ("Ontology, object, link", "Foundry's business layer on top of the data tables. An *object* is one thing "
         "(a drug, a recall, a signal); a *link* connects two objects (a signal to its drug)."),
        ("Action", "A form that writes to the Ontology. Ours creates a *Triage Decision* object."),
        ("Workshop", "Foundry's app builder. An app is a *module*; it shows objects in widgets."),
        ("FAERS", "The FDA Adverse Event Reporting System: public reports of suspected side effects, released "
                  "quarterly."),
        ("PRR", "Proportional reporting ratio: how much more often a reaction is reported with this drug than "
                "with all other drugs."),
        ("Reference label", "The official US label text, from DailyMed (the National Library of Medicine's label "
                            "library). One reference label version per product."),
        ("Signal", "A drug and reaction pair that is reported unusually often (the Evans rule: 3+ reports, PRR 2+, "
                   "chi-squared 4+; D006, proposed) and is not found in the drug's reference labels, or only "
                   "possibly in label ({{n:signals.possibly_in_label}}: found only through a medium-band synonym)."),
        ("Ranked signal", "A signal in the review queue: not in label, a clinical reaction (not, for example, an "
                          "efficacy complaint), and not mostly from mass reports."),
    ], widths=[1.4, 5])
    r.h("What she gets")
    r.p("A Workshop module called **MSSM Safety Officer**, published as {{n:app.workshop_version}}. It has "
        "{{n:app.pages}} pages, switched by tabs in the header:")
    r.table(["Page", "Answers", "What she sees on 5 November 2026"], [
        ("0 · Morning brief", "All three, at a glance",
         "{{n:signals.ranked}} ranked signals · {{n:recalls.active}} active recalls · {{n:changes.last_30_days}} "
         "changes in the last 30 days, plus an as-of date for each source"),
        ("1 · Not in label", "Question 1", "Ranked signals per drug; the evidence record; the label versions that "
                                           "were searched, with DailyMed links; the button *Triage this signal*"),
        ("2 · Recalls", "Question 2", "{{n:recalls.total}} recalls for our drugs, filterable to active; detail of "
                                      "the selected recall"),
        ("3 · What changed", "Question 3", "Dated changes to labels and recalls (and signals, after a data refresh); "
                                           "a date range means 'since my last review'"),
    ], widths=[1.3, 1.2, 4.5])
    r.p("**The write-back.** On page 1 a user selects a signal and clicks *Triage this signal*. They pick a decision "
        "(reviewing, dismissed, escalated, monitoring) and write a reason. Foundry stores it as a new "
        "*Triage Decision* object, with the user, the time, and the exact computation that was reviewed. It is "
        "still there after a full rebuild of the data [[TESTED]].")
    r.key("The {{n:signals.ranked}} ranked signals are a review queue, not {{n:signals.ranked}} findings. A signal "
          "means a reaction is reported unusually often with this drug and was not found in its label. It does not "
          "prove the drug causes it.", title="Read the first number this way")
    r.key([
        "**Fast to open.** Measured by a script in View mode: the Morning brief is fully loaded in "
        "{{n:app.timing_s.morning_brief_load}} s (including Foundry start-up), and each page switch takes "
        "{{n:app.timing_s.switch_what_changed}} to {{n:app.timing_s.switch_signals_with_labels}} s. Her reading "
        "time was not measured.",
        "**Card 3 is not 'since yesterday'.** It counts changes in the last 30 days. For 'since my last review' "
        "she sets the start date on page 3.",
        "**Signals move once a quarter.** New signals appear only when a new FAERS quarter arrives, and FAERS is "
        "about {{n:monitoring.faers_age_days}} days behind. Day to day, page 3 shows new label versions and recalls.",
        "**She can check 'not in label' herself.** For NAION she sees the {{n:app.labels_searched_naion}} label "
        "versions that were searched and can open each in DailyMed. The AI read 0 semaglutide labels (its pilot "
        "covered {{n:ai.pilot_labels}} oxycodone labels), so NAION is 'not in label' from the exact-text and "
        "synonym checks only. AI quotes are not on her screen today. NAION is a *known positive*, not a "
        "discovery: EMA PRAC (6 Jun 2025) and a WHO alert (27 Jun 2025) named it, and our 3 US labels do not "
        "mention it (DECISIONS learning 2026-11-05).",
        "**She cannot triage yet.** Only the project owner can submit a Triage Decision today. Giving her role "
        "that permission is a production step.",
    ], title="What this means for Dana (the safety officer)")
    r.pill_legend()
    r.gate("Summary", [
        ("Required evidence", "All three questions answered from one module; one decision written back and kept."),
        ("Result", "Met on 5 November 2026 (baseline gate). Machine timing done (brief "
                   "{{n:app.timing_s.morning_brief_load}} s, switches {{n:app.timing_s.switch_what_changed}} to "
                   "{{n:app.timing_s.switch_signals_with_labels}} s). A human two-minute walk-through has not been run."),
        ("If it fails", "If a question needs another tool, the app has not done its job: add it to a page."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 02 the officer
    r.chapter("The officer and her three questions")
    r.p("**We designed for one person. Every page had to pass her test: does it answer one of her questions, "
        "and can she see where the answer came from?**")
    r.p("We used *design thinking* (Empathize, Define, Ideate, Prototype, Test). With no real officer to "
        "interview. Problem: she needs a fast, trustworthy morning view of drug risks, because today she learns of "
        "them late and cannot defend an escalation without evidence. The persona is **fictional**, built from the "
        "brief [[ASSUMED]].")
    r.table(["Persona", "Dana, medication safety officer, PharmD (Doctor of Pharmacy), in a large health system "
                        "(fictional)"], [
        ("Says", "\"I found out about that recall from a nurse.\" · \"I don't have time to read FAERS.\""),
        ("Thinks", "\"Am I missing something right now?\" · \"If I escalate a false alarm, I lose credibility.\""),
        ("Does", "Scans FDA emails, MedWatch alerts (the FDA's safety-alert service) and newsletters; brings issues "
                 "to the safety committee."),
        ("Feels / trust bar", "Anxious about being late; sceptical of black boxes. \"Show me where it says that.\""),
    ], widths=[1, 5])
    r.h("From 'how might we' to a page")
    r.p("Status here means built and checked by us in View mode (the user's view). No real officer has tested it.",
        style="small")
    r.table(["How might we ...", "What we built", "Status"], [
        ("show only what is new or worse?", "Page 3 (What changed) with a date range; the Morning brief counts the "
                                            "last 30 days", "[[TESTED]]"),
        ("make 'not on the label' provable in one click?", "Page 1: label status, check method, and the panel "
         "*Reference labels searched* (version, effective date, sections, DailyMed link)", "[[TESTED]]"),
        ("show how confident we are without a statistics lecture?", "Plain labels: 'PRR (x more often than other "
                                                                     "drugs)', CI low, caution flags", "[[TESTED]]"),
        ("let her record a decision?", "Triage button, decision list under the signal (owner-only today)",
         "[[TESTED]]"),
        ("warn her when the AI might be wrong?", "Not on screen yet. Measured: {{n:ai.grounded}} of "
         "{{n:ai.reactions}} AI quotes found in the label text; monitoring checks it each build (D046, proposed)", "[[PLANNED]]"),
    ], widths=[2.4, 3.4, 0.9])
    r.h("Her test, and where we stand")
    r.table(["Test (from our design canvas)", "Pass if", "Result"], [
        ("Morning in two minutes", "She answers all three questions in two minutes or less",
         "Machine side: brief loads in {{n:app.timing_s.morning_brief_load}} s, page switches "
         "{{n:app.timing_s.switch_what_changed}} to {{n:app.timing_s.switch_signals_with_labels}} s [[OBSERVED]]. "
         "Human walk-through not run [[PLANNED]]"),
        ("Trust check", "Every flag reaches its source in two clicks or less",
         "Met on page 1: click a signal for the evidence and the labels searched; click again to open the "
         "label in DailyMed [[TESTED]]. The FAERS case reports behind a signal are reachable by query, not yet "
         "from her screen"),
    ], widths=[1.5, 2, 3.5])
    r.gate("User fit", [
        ("Required evidence", "Each page maps to one of the three questions; the trust rule is visible on screen."),
        ("Result", "Met: four pages, one per question plus the brief; the labels-searched panel puts the trust rule "
                   "on page 1. Not validated with a real officer."),
        ("If it fails", "A page that answers no question should be removed, not polished."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 03 morning routine
    r.chapter("The morning routine, click by click", new_page=False)
    r.p("**This chapter is the user guide. Four stops, left to right across the header tabs. The 20-minute demo "
        "follows the same path.**")
    r.h("Step 0 · Open the app")
    r.bullets([
        "In Foundry, open the project folder `Workshop/` and click the module *MSSM Safety Officer* (its header "
        "reads 'MSSM').",
        "It opens on the tab *Morning brief* in **View mode**, the mode every user sees. (Editors switch to Edit "
        "mode; see chapter 5.)",
    ], numbered=True)

    step(r, "Step 1 · Page 0, Morning brief: three numbers and 'data as of'")
    r.figure(SHOT + "app-0-morning-brief.jpg",
             "Page 0, Morning brief. Three metric cards answer the three questions; the table below says how fresh "
             "each source is. FAERS shows 'quarterly file (no pull time)' on purpose.",
             source=SHOT + "app-0-morning-brief.jpg (Workshop, 2026-11-05)", max_height=300)
    r.bullets([
        "Read card 1: {{n:signals.ranked}} ranked signals not in the label. This is the review queue for question 1.",
        "Read card 2: {{n:recalls.active}} active recalls across all {{n:scope.drugs_formulary}} drugs. Active means "
        "the openFDA status is *Ongoing*.",
        "Read card 3: {{n:changes.last_30_days}} changes in the last 30 days. It is a 30-day window, not 'since "
        "yesterday'; page 3 narrows it to her last review.",
        "Read the table *Data as of*. Each source updates on its own clock: FAERS quarterly (here through 2026Q2), "
        "openFDA recalls weekly, DailyMed labels daily, RxNorm monthly. *We pulled it at* shows when our pipeline "
        "fetched RxNorm, openFDA and DailyMed. For FAERS it says 'quarterly file (no pull time)' on purpose: we "
        "load the FDA's quarterly files, so the useful date is the quarter, not a clock time "
        "(`ontology_changes.py` l.152). These are the sources' own clocks; our pipeline refreshes only when a build runs, and there is no schedule yet (another month). A 'nothing changed' is only as fresh as the oldest source.",
        "Click a tab in the header to go deeper.",
    ], numbered=True)

    step(r, "Step 2 · Page 1, Not in label: pick a drug and read the evidence")
    r.figure(SHOT + "app-1-not-in-label-naion.jpg",
             "Page 1 with semaglutide's top signal selected: NAION (FAERS term 'Optic ischaemic neuropathy'). "
             "Left: the drug filter and the ranked signals. Right: the triage button, past decisions and the "
             "signal record.",
             source=SHOT + "app-1-not-in-label-naion.jpg (Workshop, 2026-11-05)", max_height=300)
    r.bullets([
        "Click the tab *1 · Not in label*.",
        "Click the pill *Ingredient Name* (the drug filter). It lists the drugs with the number of ranked signals "
        "each has. Tick {{n:signals.naion.drug}}. The table now shows only that drug.",
        "The table is sorted by rank within each drug. Rank 1 for {{n:signals.naion.drug}} is "
        "*{{n:signals.naion.reaction}}* (NAION, a sudden loss of vision in one eye).",
        "Click the row. The right side, *Evidence and triage*, shows the signal record: {{n:signals.naion.a}} "
        "reports, PRR {{n:signals.naion.prr}} (reported about that many times more often than with other drugs), "
        "lower 95% bound {{n:signals.naion.prr_ci_low}}, label status *not_in_label*, *Reference labels searched* "
        "{{n:app.labels_searched_naion}}, *Labels also read by AI* 0, and the label check method.",
    ], numbered=True)

    step(r, "Step 3 · Page 1: open the labels that were searched")
    r.figure(SHOT + "app-1c-labels-searched-naion.jpg",
             "Page 1, lower right: the panel 'Reference labels searched' for NAION. Three semaglutide label "
             "versions, each with its effective date, the safety sections searched and a DailyMed link.",
             source=SHOT + "app-1c-labels-searched-naion.jpg (Workshop, 2026-11-05)", max_height=300)
    r.bullets([
        "Scroll the right side down to the panel *Reference labels searched*. For NAION it lists "
        "{{n:app.labels_searched_naion}} label versions: Ozempic v20 (effective 2026-06-01), Wegovy v19 "
        "(2026-06-18) and oral Ozempic v14 (2026-01-30) (A016; screenshot above).",
        "Read the columns: label (product and firm), version, effective date, safety sections searched, and "
        "*Open in DailyMed*.",
        "Click a DailyMed link. The exact label version opens on the DailyMed site. This is the trust rule on "
        "screen: the flag says 'not found in these three labels', and she can check it herself.",
    ], numbered=True)
    r.note("How the panel finds the labels: it follows existing Ontology links from the selected signal, "
           "Signal → Drug → Products → Reference Label (A016). There is no dedicated Signal → Label link type yet. "
           "*Labels also read by AI* is 0 here because the AI pilot read only {{n:ai.pilot_labels}} oxycodone labels.",
           title="Behind the panel")

    step(r, "Step 4 · Page 1: record a triage decision")
    r.figure(SHOT + "app-1b-triage-action-form.jpg",
             "The form 'Create MSSM Triage Decision'. Subject Type, Subject Key and Evaluation Id are filled from "
             "the selected signal and locked. (This capture was cancelled, so nothing was saved.)",
             source=SHOT + "app-1b-triage-action-form.jpg (Workshop, 2026-11-05)", max_height=300)
    r.bullets([
        "With the signal still selected, click *Triage this signal* (top of the right side).",
        "The form opens. Subject Type ('signal'), Subject Key (drug, reaction and rule version) and Evaluation Id "
        "(a fingerprint of the numbers she is looking at) are filled in and cannot be changed.",
        "Pick a *Decision*: reviewing, dismissed, escalated or monitoring. Write a *Rationale*. Click *Submit*. "
        "(*Cancel* saves nothing.)",
        "The decision appears in the table above the signal record: decided at, decision, reviewer, rationale, "
        "evaluation id. The system sets the reviewer and the time.",
    ], numbered=True)
    r.warning("Today only the project owner can submit this Action (`foundry/ontology/README.md`, Action types). "
              "The officer's role needs that permission before a pilot with real users.")

    step(r, "Step 5 · Page 2, Recalls")
    r.figure(SHOT + "app-2-recalls.jpg",
             "Page 2, Recalls, newest first. The selected recall, D-0040-2027, is the newest one at the baseline gate.",
             source=SHOT + "app-2-recalls.jpg (Workshop, 2026-11-05)", max_height=300)
    r.bullets([
        "Click the tab *2 · Recalls*.",
        "Use the three filter pills: *Drug: Display Name* (works through the Recall-to-Drug link, so a recall that "
        "names two drugs shows under both), *Is Active* (Yes = status Ongoing), *Classification* (Class I is the "
        "most serious, then II, then III).",
        "The table is sorted by FDA report date, newest first. Click a recall to see 15 fields in reading order on "
        "the right (`foundry/ontology/README.md`): product as written by the FDA, firm, reason, lots, dates, and "
        "the openFDA as-of date.",
        "Read *Matched to our products* with care. The newest recall, {{n:recalls.newest}} (reported "
        "{{n:recalls.newest_reported}}), is a compounded tirzepatide product. It names our ingredient but matches "
        "none of our products, so it shows 0. That is correct, not a bug, but the screen does not yet say so.",
    ], numbered=True)

    step(r, "Step 6 · Page 3, What changed since my last review")
    r.figure(SHOT + "app-3b-what-changed-past-month.jpg",
             "Page 3 with the start date set by the 'Past month' preset (6 Oct to 5 Nov 2026). Left: filters with "
             "counts. Right: the dated changes, newest first.",
             source=SHOT + "app-3b-what-changed-past-month.jpg (Workshop, 2026-11-05)", max_height=300)
    r.bullets([
        "Click the tab *3 · What changed*.",
        "Under *Event Date*, click the start-date box and pick the day of your last review (or a preset such as "
        "*Past month*). That is what 'since yesterday' means here: since *my* last look, because the sources do "
        "not all update daily (D045, proposed).",
        "Check the count. With *Past month* the table holds {{n:changes.last_30_days}} events, 15 label versions "
        "and 11 recalls (`screens/README.md`): the same number as card 3 on the Morning brief.",
        "Narrow with the other filters: *Ingredient Name*, *Entity Type* (label, recall, signal) and *Change* "
        "(version effective, reported, terminated).",
        "Read *Found by*: `source_date` means the source itself carries the date (a recall's report date, a "
        "label's effective date). `snapshot_diff` means we found it by comparing this build with the last one.",
    ], numbered=True)
    r.gate("Morning routine", [
        ("Required evidence", "Each step works in View mode (as a user, not as the editor)."),
        ("Result", "Met: tabs switch pages, the drug filter narrows page 1, the labels panel lists the searched "
                   "labels with working DailyMed links, recalls filter by linked drug, changes sort newest first, "
                   "the cards read {{n:signals.ranked}} · {{n:recalls.active}} · {{n:changes.last_30_days}} (A016). "
                   "Times: brief {{n:app.timing_s.morning_brief_load}} s; switches {{n:app.timing_s.switch_recalls}}, "
                   "{{n:app.timing_s.switch_what_changed}} and {{n:app.timing_s.switch_signals_with_labels}} s "
                   "[[OBSERVED]]."),
        ("If it fails", "If a card and its page disagree, the card's object set and the page's object set have "
                        "drifted apart: they must start from the same set."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 04 numbers
    r.chapter("What each number means")
    r.p("**Every number on the screen is a count of objects or a property of one object. Here is what each one "
        "means, and what it must not be read as.**")
    r.p("One limit applies to all of them: FAERS counts **reports**, not patients or users, and reporting rises "
        "after news coverage, lawsuits or FDA warnings (stimulated reporting, DQ04, a known gap left to the "
        "reviewer). A high PRR says 'look here', not 'this is dangerous'.")
    r.h("Morning brief")
    r.table(["Number", "Definition", "Do not read it as", "Evidence"], [
        ("{{n:signals.ranked}} ranked signals",
         "MSSM Signals with Is Ranked = true: clinical reactions that meet the Evans rule, are not found in any "
         "reference label, and come mostly from normal reports (not mass reports).",
         "{{n:signals.ranked}} side effects caused by our drugs. It is a review queue.", "[[DERIVED]]"),
        ("{{n:recalls.active}} active recalls",
         "MSSM Recalls for our drugs with Is Active = true, which means openFDA status *Ongoing* "
         "(`clean_recalls.py` l.69), out of {{n:recalls.total}}.",
         "Recalls of products on our shelves: some match none of our products.", "[[OBSERVED]]"),
        ("{{n:changes.last_30_days}} changes in 30 days",
         "MSSM Change Events whose event date is in the last 30 days, relative to today.",
         "'Since yesterday', or new safety problems. Most are new label versions and recalls.", "[[DERIVED]]"),
    ], widths=[1.3, 2.9, 2, 0.8])
    r.h("Page 1 signal record (selected rows)")
    r.table(["Field on screen", "Meaning", "NAION value"], [
        ("Reports: this drug + reaction", "a: current FAERS reports naming this drug as a suspect and this reaction",
         "{{n:signals.naion.a}}"),
        ("All reports for this drug", "Every current report naming this drug as a suspect",
         "{{n:signals.naion.all_reports_drug}}"),
        ("PRR (x more often than other drugs)", "Share of this reaction among this drug's reports, divided by its "
                                                "share among all other drugs' reports", "{{n:signals.naion.prr}}"),
        ("PRR 95% CI low / high", "The range the PRR is likely in, given the counts. A low bound well above 1 means "
         "the excess is not a small-numbers accident. It does not rule out reporting bias.",
         "{{n:signals.naion.prr_ci_low}} / {{n:signals.naion.prr_ci_high}}"),
        ("Chi² (Yates)", "How surprising the count is. Evans rule (D006, proposed): 3+ reports, PRR 2+, chi² 4+",
         "{{n:signals.naion.chi2_yates}}"),
        ("Label status", "not_in_label, possibly_in_label (found only through a medium synonym) or in_label",
         "not_in_label"),
        ("Reference labels searched", "How many reference label versions of this drug were searched; the panel "
         "below lists them", "{{n:app.labels_searched_naion}}"),
        ("Labels also read by AI", "How many of those labels the AI pilot also read", "0"),
        ("Label check method", "The rule versions in force (AI v1, text, synonyms v2); it does not say which "
         "checks found or ran on this signal (for NAION the AI ran on 0 labels)", "text+ai_v1+syn_v2"),
        ("Bucket", "Only clinical is ranked; efficacy, product use, abuse and others are tagged (D016 v3). Reports "
                   "with 30+ drugs are set aside and counted separately (D023 v2)", "clinical"),
    ], widths=[2, 3.6, 1.4])
    r.gate("Numbers explained", [
        ("Required evidence", "Each number on screen has a definition and a 'do not read it as'."),
        ("Result", "Met in this chapter. On screen, the labels are plain but there is no help text yet."),
        ("If it fails", "If the officer quotes '{{n:signals.ranked}} problems' to her committee, the screen needs a "
                        "sub-title under the card that says 'to review'."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 05 how it was built
    r.chapter("For editors: the widgets and how to change them")
    r.p("**The whole module is built from six kinds of widget and a handful of shared variables. This chapter "
        "says what each one does for the officer and where an editor changes it.**")
    r.table(["Workshop term", "Meaning"], [
        ("Module", "One Workshop app. Ours: MSSM Safety Officer, in the project folder `Workshop/`."),
        ("Page", "A screen inside the module. Ours are named 0 to 3."),
        ("Widget", "A building block on a page: tabs, filter list, object table, property list, metric card, button."),
        ("Variable", "A named value the widgets share: an object set, a selected object, a string, a count."),
        ("Object set", "A list of Ontology objects, for example 'MSSM Signal where Is Ranked = true'."),
        ("Event", "What a click does, for example 'switch to page'."),
        ("View mode / Edit mode", "View mode is what users see. Edit mode is the builder: the same pages, plus a "
                                  "configuration panel for the selected widget and a list of variables."),
        ("Version", "Editors save and publish numbered versions; users see the published one "
                    "({{n:app.workshop_version}} today)."),
    ], widths=[1.4, 5])

    r.h("The widgets on the screen")
    r.table(["Widget", "Where", "What it does for her", "How an editor changes it"], [
        ("Tabs", "Header", "Switches between the four pages",
         "Select the tabs widget; each tab's on-click event is *Switch to page*. Page names carry a number because "
         "the editor sorts pages alphabetically (learning 2026-11-05)"),
        ("Filter list", "Left side of pages 1 to 3", "Narrows the table by drug, active, class, date, type",
         "Set its input to the **unfiltered** object set, pick the properties to filter on (or a linked object's "
         "property, as for Drug on page 2) and the display (pills, or a list with counts and a histogram)"),
        ("Object table", "Pages 0 to 3", "Lists signals, recalls, changes, sources, decisions, labels searched",
         "Set the input variable, the columns and their order, the default sort, and the row height (use "
         "*Absolute*: *Flex* collapses in a crowded section, learning 2026-11-04)"),
        ("Property list", "Right side of pages 1 and 2", "Shows every field of the selected signal or recall",
         "Set the input to the selected-object variable; choose fields, order and plain labels. Number format "
         "(decimals) is set on the Ontology property in Ontology Manager, so every app shares it"),
        ("Metric card", "Page 0", "The three morning numbers",
         "Each metric is a *Count* variable over an object set; change the set's filter to change what is counted"),
        ("Button (Action)", "Page 1", "*Triage this signal* opens the decision form",
         "Choose the Action, then set each field's default from a variable and lock it (Disabled). Who may submit "
         "is set on the Action type in the Ontology, not on the button"),
    ], widths=[1, 1.1, 1.8, 3.1])

    r.h("The variables behind them")
    r.table(["Variable", "Defined as", "Read by"], [
        ("Ranked signals", "MSSM Signal where Is Ranked = true", "Drug filter, card 1"),
        ("Ranked signals for chosen drugs", "Ranked signals + the drug filter's output", "Page 1 table"),
        ("Selected signal key / evaluation id", "Properties of the table's selected signal",
         "Triage button defaults; decision list; labels panel"),
        ("Decisions for selected signal", "MSSM Triage Decision where Subject Key = Selected signal key",
         "Decisions table"),
        ("All recalls → Recalls for chosen drugs", "MSSM Recall ({{n:recalls.total}}) → + the recall filters",
         "Page 2 filter, then table"),
        ("Active recalls", "All recalls where Is Active = true", "Card 2"),
        ("All changes → Changes for chosen filters", "MSSM Change Event ({{n:changes.total}}) → + the change filters",
         "Page 3 filter, then table"),
        ("Changes last 30 days", "All changes where Event Date is from 30 days ago, relative to today", "Card 3"),
    ], widths=[2.1, 2.9, 1.9])
    r.p("Source for both tables: `foundry/ontology/README.md` (Workshop module) and A016.", style="small")

    r.h("How an editor makes a change, step by step")
    r.bullets([
        "Open the module and switch to Edit mode (only editors of the project can).",
        "Click the widget on the page. Its configuration opens on the side: input variable, columns or fields, "
        "sort, display.",
        "To change *what* is shown everywhere at once, edit the **variable**, not the widget: every widget that "
        "reads it follows. Example: adding a filter to *Ranked signals* changes card 1, the drug filter and the "
        "page 1 table together.",
        "For many columns at once, use the widget's JSON config (`</>` → edit → *Validate and save*), shown below.",
        "Switch back to View mode and click through the page as the officer would.",
        "Publish a new version. Users see it on their next load.",
    ], numbered=True)
    r.note("Two places, two scopes. A change on the **Ontology** (a property's display name or number format) shows "
           "in every app that uses that object type. A change on a **widget** affects that widget only.",
           title="Where a change ripples")

    r.h("Three patterns worth copying")
    r.p("**Two object sets per page.** An unfiltered set feeds the filter list; the filter's output makes a "
        "second, filtered set; that set feeds the table; the table's selected row feeds the detail panel. If the "
        "filter read the filtered set, it would feed back into itself, and every other drug would disappear from "
        "its own choices.")
    r.p("**Cards count the same sets the pages show.** Card 1 counts *Ranked signals*, the set behind page 1; card 2 "
        "counts *All recalls* where active; card 3 counts *All changes* in the last 30 days. So a card and its page "
        "cannot disagree.")
    r.p("**The Action button with locked defaults.** *Triage this signal* runs the Action *Create MSSM Triage "
        "Decision*. Subject Type is a static 'signal'; Subject Key and Evaluation Id come from the selected-signal "
        "variables. All three are locked, so a decision can only be saved against the exact signal and numbers on "
        "screen. The decision list refreshes after submit (D042).")

    r.h("The JSON config shortcut")
    r.p("Writing table columns and property-list fields straight into a widget's JSON replaced roughly ten clicks "
        "per column with one paste (learning 2026-11-05); reordering and relabelling the 22 signal properties took "
        "one paste instead of about 60 clicks (learning 2026-11-04). A column entry looks like this (the type id is "
        "in the object type's web address in Ontology Manager):")
    r.code('{"type": "property",\n'
           ' "property": {"propertyType": {"objectTypeId": "<object type id>",\n'
           '                               "propertyTypeId": "<column name>"}}}')
    r.warning("The JSON box is live: typing into it by accident edits the widget. Close it without *Validate and "
              "save* to discard (learning 2026-11-05).")
    r.gate("Editor guide", [
        ("Required evidence", "Another editor can rebuild or change the module from this chapter and "
                              "`foundry/ontology/README.md`."),
        ("Result", "Met: every page's widgets, variables, filters, cards and Action defaults are written down. The "
                   "module itself lives only in Foundry (no export in the repo)."),
        ("If it fails", "If a widget's configuration is lost, the README tables give its columns and order."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 06 usability changes
    r.chapter("What we changed for usability, and why")
    r.p("**Each change came from looking at the screen as the officer would. The trigger is written next to "
        "every change.** 'Step' is a stage in our numbered build order: step 8 built the first screen, step 9 "
        "widened it to all {{n:scope.drugs_formulary}} drugs, step 11 added the Morning brief, recalls and changes.")
    r.table(["When", "Before", "Now", "Why (her view)", "Source"], [
        ("Step 8", "PRR and chi² with 12 decimals", "PRR 1 decimal, CI 2, chi² 1 (set on the Ontology property)",
         "Precision she cannot use is noise", "A012"),
        ("Step 8", "All signal properties in no useful order", "22 rows in reading order with plain labels",
         "Read top to bottom: why flagged, label check, trace", "A012; README"),
        ("Step 8", "Past-decisions table collapsed (row height Flex)", "Row height Absolute 160 px; columns time · "
         "decision · reviewer · rationale · evaluation id", "She must see her history",
         "Learning 2026-11-04; README"),
        ("Step 9", "One ranked list mixing {{n:scope.drugs_with_signals}} drugs (exenatide has no reference label, "
                   "so no signals; R07)", "Drug filter pill with counts per drug",
         "She reviews one drug at a time", "A012 update"),
        ("Step 11", "One page: question 1 only", "Morning brief plus one page per question",
         "All three questions, from one place", "A016"),
        ("Step 11", "No freshness anywhere", "'Data as of' table per source", "'Nothing changed' needs a date",
         "A016, D045 (proposed)"),
        ("Step 11", "Pull time blank for FAERS and RxNorm", "FAERS: 'quarterly file (no pull time)'; RxNorm: the "
                    "pull time", "A blank cell looks like a fault", "`ontology_changes.py` l.152, l.158"),
        ("Step 11", "Recall class as a code", "\"Class (I = most serious)\"", "No lookup needed", "A016"),
        ("Step 11", "'Since yesterday' undefined", "Start date on page 3 = since my last review",
         "Sources are not daily", "D045 (proposed)"),
        ("Step 11", "Record showed only how many labels were searched", "Panel *Reference labels searched* with "
                    "version, date, sections and DailyMed link", "\"Show me where it says that\"", "A016"),
    ], widths=[0.7, 1.6, 2, 1.6, 0.9])
    r.p("The ranking itself also changed for her sake. Non-harm terms (efficacy complaints, product handling, "
        "procedures) moved out of the ranked queue into tagged buckets, and a reviewed synonym table removed "
        "label wording misses. The queue went from {{n:signals.ranked_history.step9}} at step 9 (first full build) "
        "to {{n:signals.ranked_history.syn_v1}} (synonym table v1), {{n:signals.ranked_history.d016_v3}} (wider "
        "buckets, D016 v3) and {{n:signals.ranked_history.syn_v2}} (synonym table v2). R05 explains each step "
        "[[OBSERVED]].")
    r.gate("Usability changes", [
        ("Required evidence", "Each change has a before, an after and a reason tied to the officer."),
        ("Result", "Met for the ten changes above. None was tested with a real officer."),
        ("If it fails", "If a change cannot be tied to one of her questions or the trust rule, revert it."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 07 gaps and next
    r.chapter("Known gaps and the next UI improvements")
    r.p("**What a careful reviewer will notice on the screen today, and what we would build next.**")
    r.h("Known gaps")
    r.table(["Gap", "Where", "Effect", "Fix"], [
        ("Human 'morning in two minutes' walk-through not run (machine timings done)", "all",
         "Her reading time is unmeasured", "Run it with the safety-officer persona, then a real officer"),
        ("Only the owner can submit a decision", "page 1", "The officer cannot use the write-back yet",
         "Grant the officer role on the Action"),
        ("AI evidence not on screen", "page 1", "AI quotes are only in Object Explorer, and only for "
         "{{n:ai.pilot_labels}} oxycodone labels", "Show AI quotes for labels that have them"),
        ("Reviewer shows a user ID, not a name", "page 1 decisions", "Harder to read the history",
         "Show the user's display name"),
        ("No help text ('Matched to our products: 0', what the cards count)", "pages 0, 2",
         "A compounded-product recall looks like a bug; a card can be read as findings",
         "One line of help text under each card and field"),
        ("No dedicated Signal → Label link type", "page 1", "None for her: the panel walks existing links. A "
         "builder cannot ask 'which signals did this label clear?' directly", "A join dataset and a link type"),
        ("Signal changes only appear after the next FAERS quarter", "page 3",
         "Today's feed is labels and recalls; the build-to-build diff found {{n:changes.snapshot_diff_after_rebuild}} "
         "changes on unchanged data", "Expected; say so on the page"),
    ], widths=[2.1, 1, 2, 1.9])
    r.h("Next UI improvements")
    r.p("None of these is built. They are listed in the order we would build them.", style="small")
    r.table(["Improvement", "Why (her view)", "What it needs", "Status"], [
        ("Help text under each card and tricky field", "'{{n:signals.ranked}} to review', not '{{n:signals.ranked}} "
         "problems'; 'Matched 0' explained", "Text only, in the widgets", "[[PLANNED]]"),
        ("Officer permission on the triage Action", "She can record her own decisions",
         "A role for the officer on the Action type", "[[PLANNED]]"),
        ("Reviewer display name", "She can read the history at a glance", "Show the user's name, not the ID",
         "[[PLANNED]]"),
        ("'Evidence changed since your decision' flag", "A decision made on old numbers should be re-looked at",
         "Compare the decision's evaluation id with the signal's current one (both are on screen today)",
         "[[PLANNED]]"),
        ("AI quotes on page 1", "'Show me where it says that' for labels the AI read",
         "A table of AI terms and quotes for the selected drug's labels; more labels read by the AI", "[[PLANNED]]"),
        ("Health page", "She (and IT) see a stale source or a failed check before trusting the numbers",
         "A key column and an object type for `monitoring_checks` ({{n:monitoring.checks_per_build}} checks per "
         "build)", "[[PLANNED]]"),
        ("Per-user 'last reviewed'", "Page 3 opens at her last review; the brief counts 'new since you last looked'",
         "Per-user state, or the time of her latest triage decision", "[[PLANNED]]"),
        ("Triage on recalls", "Recalls need decisions too", "A Triage Decision → Recall link", "[[PLANNED]]"),
    ], widths=[1.7, 2.2, 2.3, 0.8])
    r.gate("Ready for a pilot user", [
        ("Required evidence", "A real officer completes the morning routine unaided in two minutes and can trace "
                              "a flag to its source."),
        ("Result", "Not yet: the module answers all three questions and the machine timings are fast (brief "
                   "{{n:app.timing_s.morning_brief_load}} s, switches {{n:app.timing_s.switch_what_changed}} to "
                   "{{n:app.timing_s.switch_signals_with_labels}} s), but the human timed test and the real-user "
                   "test are still to do, and she cannot submit a decision yet."),
        ("If it fails", "Fix the step where she stops, before adding any new feature."),
    ], status="PLANNED")

    r.chapter("Reference", label="A")
    r.h("Figures quoted from project records (not in numbers.json)")
    r.p("These come from project records, not from the baseline-gate capture. Each is also cited where it appears.",
        style="small")
    r.table(["Figure", "Source"], [
        ("About fifteen minutes each morning; persona quotes", "docs/02-design-thinking/design-thinking-canvas.md "
                                                               "(fictional persona)"),
        ("Ozempic v20 (2026-06-01), Wegovy v19 (2026-06-18), oral Ozempic v14 (2026-01-30)",
         "A016; screenshot app-1c-labels-searched-naion.jpg"),
        ("26 events = 15 label versions + 11 recalls (Past month)", "screens/README.md; app-3b screenshot"),
        ("22 signal properties; 15 recall fields", "foundry/ontology/README.md (Workshop module)"),
        ("PRR 1 decimal, CI 2, chi² 1 (was 12 decimals)", "A012; foundry/ontology/README.md (Polish, v0.3)"),
        ("Decisions table row height Absolute 160 px; Flex collapses", "foundry/ontology/README.md; learning 2026-11-04"),
        ("About 10 clicks per column; about 60 clicks for 22 properties", "Learnings 2026-11-05 and 2026-11-04"),
        ("Evans rule: 3+ reports, PRR 2+, chi² 4+", "D006 (proposed)"),
        ("Mass reports: 30+ drugs per report", "D023 v2"),
        ("Labels also read by AI: 0 (NAION)", "Screenshot app-1-not-in-label-naion.jpg; rubric-check"),
    ], widths=[300, 204])
    r.numbers_appendix()
