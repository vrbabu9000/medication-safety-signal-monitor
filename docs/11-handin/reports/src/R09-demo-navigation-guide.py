"""R09 Demo navigation guide: the 20-minute demo, stop by stop, with screenshots.

Build:  .venv/bin/python tools/handin/build_report.py R09-demo-navigation-guide
Output: docs/11-handin/reports/pdf/R09-demo-navigation-guide.pdf

Markdown twin: docs/11-handin/demo/demo-navigation-guide.md (same stops, same words).
Agenda (binding): docs/11-handin/AGENT-BRIEF.md. Spoken words: docs/11-handin/deck/speaking_script.md.
Numbers: docs/11-handin/numbers.json only; other figures cite their record inline.
Phase D fix pass (2026-11-05): labels-searched stop (A4), triage Cancel by default, H-codes aligned to deck slides 6-16,
machine timings, 'We pulled it at' values, v0.9.0, diagrams 30/32/33 v2, proposed decisions, rubric-check Q&A.
"""

META = {
    "id": "R09",
    "title": "Demo navigation guide",
    "short": "Demo navigation guide",
    "subtitle": "the 20-minute demo, click by click",
    "version": "1.2",
    "date": "5 November 2026",
}

from reportlab.platypus import KeepTogether

S = "docs/11-handin/screens/"
D = "docs/diagrams/png/"


def stop(r, code, title, when, secs, rows, fig=None, caption=None, level=2, fig_h=270):
    """One demo stop: heading, the screenshot (if any), then a two-column table; kept on one page when it fits."""
    start = len(r.flow)
    r.h(f"{code} · {title}  ({when}, {secs} s)", level)
    if fig:
        r.figure(fig, caption or title, source=fig, max_height=fig_h)
    r.table(["What", "Detail"], rows, widths=[1, 5.2])
    block = r.flow[start:]
    del r.flow[start:]
    r.flow.append(KeepTogether(block))


def build(r):
    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this guide answers",
               "What exactly do I click, show and say in each minute of the 20-minute demo, and what do I do "
               "when Foundry is slow?"),
              ("One-line answer",
               "Part A walks the safety officer's morning in the app (0:00 to 7:30). Part H goes under the hood "
               "in the deck's slide order (7:30 to 20:00). Every stop has a click path, a screenshot, a key line, "
               "the rubric row it proves, a seconds budget and a fallback.")],
        is_=["The presenter's click path for the live demo, in the binding agenda order",
             "A pre-demo checklist: tabs, zoom, what to rebuild (nothing), the triage choice (Cancel by default)",
             "A fallback screenshot for each live stop, and prepared answers to the three rubric-check questions"],
        is_not=["The deck or its full spoken words (see `docs/11-handin/deck/speaking_script.md`)",
                "The full ripple map or question bank: `demo/ripple-table.md` and `demo/rehearsal-plan.md`",
                "A claim that any signal is caused by a drug"],
        how_to_read="New to the project? Read **R00 Start here** first (`docs/11-handin/reports/pdf/R00-start-here.pdf`). "
                    "Chapter 1 is the whole demo at a glance. Chapter 2 is the setup, done before anyone joins. "
                    "Chapters 3 and 4 are the stops: grey labels on the left, what to do on the right; the "
                    "**Say** row is the key line (full words in the speaking script). Chapter 5 is for when something "
                    "breaks and for the hardest questions. Numbers come from `numbers.json`, captured in Foundry at the "
                    "baseline gate [[OBSERVED]]; other figures name their record in brackets.",
    )

    # ------------------------------------------------------------------ 1
    r.chapter("The 20 minutes at a glance")
    r.p("The agenda is fixed in the hand-in brief, and the deck, the speaking script and this guide all follow it. "
        "The user is the hospital pharmacy safety officer (we call her Dana). She has three morning questions: which "
        "drugs have side effects reported that the label does not mention, which have an active recall, and what "
        "changed since her last review. Her one rule: every flag must trace back to its source.")
    r.p("**The 13 formulary drugs.** Opioids ({{n:scope.opioids}}): oxycodone, hydrocodone, morphine, fentanyl, "
        "hydromorphone, methadone, buprenorphine, tramadol. GLP-1s ({{n:scope.glp1}}): semaglutide, liraglutide, "
        "dulaglutide, tirzepatide, exenatide. Exenatide has no reference label, so signals exist for "
        "{{n:scope.drugs_with_signals}} of {{n:scope.drugs_formulary}} (A013).")
    r.key([
        "**{{n:signals.ranked}} is a review queue, not {{n:signals.ranked}} findings.** A signal = reported more often "
        "than for other drugs (Evans rule) **and** not found in the drug's reference labels, or only possibly in label "
        "({{n:signals.possibly_in_label}}: found only through a medium-band synonym).",
        "**NAION is a known positive, not a discovery.** EMA's safety committee (PRAC) concluded on 6 June 2025 that "
        "NAION is a very rare side effect of semaglutide (WHO alert 27 June 2025); the "
        "{{n:app.labels_searched_naion}} US label versions we search still do not mention it (DECISIONS learning "
        "2026-11-05). A monitor that missed it would be broken.",
        "**NAION was not checked by the AI.** The AI has read 0 semaglutide labels (the pilot is "
        "{{n:ai.pilot_labels}} oxycodone labels). The method code `text+ai_v1+syn_v2` names the rule version, not "
        "which checks ran.",
        "**'Matched to our products' means the 658 FDA-listed products we track (foundry README), not her shelves.** "
        "We have no inventory data. And she cannot open the {{n:signals.naion.a}} reports from her screen yet.",
        "**Card 3 counts the last 30 days**, not since yesterday. Page 3's date range narrows it to "
        "\"since my last review\".",
        "**Only the project owner can submit a triage decision today.** In the demo the form is opened and "
        "**cancelled** unless the owner decides otherwise.",
        "**New signals arrive only with a new FAERS quarter**, and FAERS is about {{n:monitoring.faers_age_days}} days "
        "behind (monitoring `faers_age_days`).",
    ], title="What this means for Dana (the safety officer)")

    r.table(["Stop", "Time", "s", "Deck", "Proves (rubric row)"], [
        ("A0 The officer's problem", "0:00–1:30", "90", "1–2", "Communication"),
        ("A1 Morning brief", "1:30–3:00", "90", "3", "Application (trust)"),
        ("A2 Noise, then semaglutide", "3:00–3:40", "40", "4", "Application"),
        ("A3 Evidence (NAION)", "3:40–4:30", "50", "4", "Application (trace)"),
        ("A4 Labels searched + DailyMed", "4:30–5:20", "50", "4", "Application, AI reliability"),
        ("A5 Triage form (Cancel)", "5:20–6:00", "40", "4", "Application (trust)"),
        ("A6 Recalls + FDA record", "6:00–6:50", "50", "5", "Application, Data judgment"),
        ("A7 What changed", "6:50–7:30", "40", "5", "Application"),
        ("H1 Architecture picture", "7:30–8:30", "60", "6", "Architecture"),
        ("H2 Data Lineage", "8:30–9:30", "60", "6", "Architecture"),
        ("H3 Ontology picture", "9:30–10:15", "45", "7", "Architecture"),
        ("H4 Ontology Manager", "10:15–10:45", "30", "7", "Architecture"),
        ("H5 Object Explorer trace", "10:45–11:30", "45", "7", "Application (trace)"),
        ("H6 One report to a signal", "11:30–12:30", "60", "8", "Data judgment"),
        ("H7 Signal code (optional)", "12:30–12:50", "20", "8", "Architecture"),
        ("H8 Review queue, not findings", "12:50–13:30", "40", "9", "Data judgment"),
        ("H9 AI reliability", "13:30–14:45", "75", "10", "AI reliability, Optimization"),
        ("H10 Monitoring", "14:45–15:30", "45", "11", "AI reliability, Data judgment"),
        ("H11 Optimization log", "15:30–16:45", "75", "12", "Optimization"),
        ("H12 Incremental FAERS", "16:45–17:30", "45", "13", "Optimization"),
        ("H13 Data judgment", "17:30–19:00", "90", "14", "Data judgment"),
        ("H14 Another month", "19:00–19:40", "40", "15", "Communication"),
        ("H15 What to take away", "19:40–20:00", "20", "16", "Communication"),
        ("**Total**", "", "**1,200**", "", ""),
    ], widths=[2.4, 1.3, 0.6, 0.6, 2.4])
    r.note("Stop codes are A0–A7 (the app) and H1–H15 (under the hood), so they never clash with the deck's backup "
           "slides B1–B12. Checkpoints: 3:00, 6:00, 7:30, 11:30, 15:30, 19:00. More than 30 s late: drop the optional "
           "switches (H7, H9, H10, H12, H13), then the Object Explorer half of H5, then shorten H12 to one sentence. "
           "Never cut A4 (labels searched and the DailyMed search), A5 (the Action form), H2 (lineage) or the honest limits in H9.",
           title="Staying on time")
    r.figure(D + "36-handin-demo-map-v2.png", "The demo map (diagram 36 v2): the officer's path first, then the stops under the hood. Its slot times and rubric rows match the table above.",
             source="docs/diagrams/png/36-handin-demo-map-v2.png", max_height=330)

    r.h("Words to explain the first time you use them")
    r.table(["Term", "Say"], [
        ("Foundry", "Palantir's data platform: pipelines, a data model and apps in one place"),
        ("Dataset, transform", "A table in Foundry; the Python code that builds one table from others"),
        ("Code Repository", "Foundry's built-in code editor, with git and a Build button"),
        ("Data Lineage", "Foundry's live graph of which dataset is built from which"),
        ("Ontology, object type, link, Action", "The business layer on top of datasets: Drug, Signal, Recall as "
         "things with links between them. An Action is a form that writes a change back"),
        ("Workshop", "Foundry's app builder; our app is the module MSSM Safety Officer "
         "({{n:app.workshop_version|raw}}, {{n:app.pages}} pages)"),
        ("AIP", "Foundry's AI platform; we call Claude Sonnet 5.5 through it"),
        ("FAERS", "The FDA's database of adverse event reports, published as quarterly files"),
        ("PRR", "Proportional reporting ratio: how much more often a reaction is reported with this drug "
         "than with all other drugs"),
        ("Evans rule", "A signal needs at least 3 reports, PRR at least 2 and chi-square at least 4 (D006, proposed)"),
        ("MedDRA preferred term (PT)", "The standard medical term FAERS uses for a reaction"),
        ("DailyMed, SPL", "The NIH site for official drug labels; the XML format they come in"),
        ("openFDA", "The FDA's public API: recalls (enforcement), Drugs@FDA and NDC"),
        ("RxNorm, RxCUI", "The NIH drug naming standard; its ID for one ingredient"),
        ("NDC", "National Drug Code: the ID printed on a package"),
        ("Evaluation id", "A fingerprint of the evidence behind a signal (report count, PRR, label-check version, "
         "FAERS window, labels searched, labels read by AI). It changes when any of those change"),
    ], widths=[1.6, 4.6])

    # ------------------------------------------------------------------ 2
    r.chapter("Before the demo")
    r.h("The day before (then run rehearsal pass 1)")
    r.table(["#", "Check", "Pass when", "If not"], [
        ("1", "**Do not rebuild the raw pulls.** The demo uses the frozen baseline data",
         "Morning brief shows {{n:signals.ranked}} and {{n:recalls.active}}",
         "If someone rebuilt, the lead re-captures numbers.json before the slides change"),
        ("2", "Data Health on `ontology_signal_signals` (Health tab)", "Build status and Primary key both Passed",
         "Dataset page: Build, then Force, Only this dataset; check again"),
        ("3", "AI cache rows (SQL on `ai_label_section_extractions`)",
         "{{n:ai.sections}} rows, all `from_cache` true, `n_reactions` = `n_grounded`",
         "Use the screenshot. Do not rebuild the AI transform on demo day"),
        ("4", "**Owner's choice for the triage form: Cancel (default) or Submit**",
         "The owner has said which, before the demo",
         "No answer means Cancel. Submit creates a permanent object: the Action is create-only, with no delete"),
        ("5", "If Submit was chosen: logged in as the **project owner**", "Triage form opens",
         "Only the owner can submit today. Otherwise Cancel"),
        ("6", "Keep the {{n:app.triage_decisions}} test decisions", "Still in Object Explorer",
         "See the note below"),
        ("7", "Rehearse the form by **opening it and pressing Cancel**; never Submit in rehearsal",
         "NAION's decisions table is still empty", "If a decision landed by mistake: keep it, tell the lead"),
        ("8", "**DailyMed check (A4):** click the Ozempic v20 link on page 1, Cmd+F `optic`",
         "First hit is not the retinopathy warning; no optic neuropathy found. Note the version DailyMed shows",
         "Use `ischemic optic`. Newer version shown: say so. Screenshot the search as the fallback"),
        ("9", "**Class I count (A6):** page 2, Is Active = Yes, click the Class column",
         "Active Class I count and D-0788-2026's product match written down (**not measured** today)",
         "Not counted: say no number"),
        ("10", "**Stopwatch walk-through by a person** of the three questions, reading included",
         "Time written down. 'Under two minutes' is a target until then",
         "Say 'designed for under two minutes, not yet timed with a person'"),
    ], widths=[0.4, 2.4, 2.1, 2.1])
    r.note("The Action is create-only, so there is no delete Action; removing the test decisions would mean adding "
           "one. They are audit evidence that a decision survives a rebuild. Their rationales say STEP 6 ACTION "
           "SAVE TEST (recall D-0338-2026) and STEP 8 WORKSHOP TEST (Oxycodone · Myoclonus). Neither is on NAION, "
           "so neither appears in Part A. Worth checking in rehearsal (not verified): the Myoclonus decision stores "
           "evaluation id cbcd091262d23bd6 from step 8 (A012); the label check has changed twice since, so the "
           "signal's current id should differ. If it does, it is a live example of a decision on older evidence.",
           title="Why keep the two test decisions")

    r.h("Thirty minutes before: windows and tabs")
    r.p("Window 1: Chrome with Foundry. Window 2: the deck in presenter view. Window 3 (backup): every image "
        "in `docs/11-handin/screens/` open in Preview. Hide the bookmarks bar, turn on Do Not Disturb, close "
        "chat and email. Browser zoom 110% for the app and dataset tabs, 125% for the code tabs. Cmd+1 to Cmd+8 "
        "jump straight to tabs 1 to 8; Cmd+9 jumps to the last tab (the openFDA record).")
    r.table(["Tab", "Open", "Leave it showing", "At"], [
        ("1", "Workshop module **MSSM Safety Officer** {{n:app.workshop_version|raw}}, View mode (folder `Workshop/`)",
         "Morning brief. Click all 4 tabs once to warm them, then come back", "1:30"),
        ("2", "`Data/curated/ontology_signal_signals`, Explore pipeline, Explore data lineage; expand parents 3 levels",
         "The graph laid out as in the H2 screenshot. Do not press Layout again", "8:30"),
        ("3", "Ontology Manager, **MSSM Signal**", "Overview", "10:15"),
        ("4", "Object Explorer, search `Semaglutide · Optic ischaemic neuropathy`",
         "First result selected, Links tab", "10:45"),
        ("5", "Repo `Pipelines/pipelines_clean`, file `ontology_signals.py`",
         "Lines 22 to 29 (Foundry numbering); SQL panel with the **monitoring** query already run",
         "12:30, 14:45, 17:30"),
        ("6", "Same repo, second tab, `ai_label_extraction.py`",
         "Lines 16 to 25; SQL panel with the **AI cache** query already run", "13:30"),
        ("7", "`Data/curated/ontology_signal_signals`", "Health tab", "14:45"),
        ("8", "`Data/clean/clean_faers_inc_log` (optional)", "Preview", "16:45"),
        ("9", "Last tab. The FDA's own record: `https://api.fda.gov/drug/enforcement.json?search=recall_number:\"D-0040-2027\"` "
         "(the openFDA record the pipeline reads)", "The JSON: number, class, status, product, lots. Cmd+9 jumps here",
         "6:20"),
    ], widths=[0.4, 3.0, 2.6, 0.8])
    r.warning("The code repository is slow to start ('Starting Python server'). Open tabs 5 and 6 at least 10 minutes "
              "early. **Never type in the editor** during the demo: an accidental edit can be committed. The SQL "
              "panel is slow, so run the queries during setup and leave the results showing.")
    r.code("-- tab 6: AI cache rows (H9)\n"
           "SELECT label_key, section_name, status, n_reactions, n_grounded, from_cache,\n"
           "       prompt_tokens, completion_tokens, called_at\n"
           "FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/ai_label_section_extractions`\n"
           "ORDER BY label_key, section_name")
    r.code("-- tab 5: latest monitoring run (H10, H13)\n"
           "SELECT check_id, area, value, previous, threshold, status, detail\n"
           "FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/monitoring/monitoring_checks`\n"
           "WHERE run_at = (SELECT MAX(run_at) FROM\n"
           "`/kestrel-01f4ab/Medication Safety Signal Monitor/Data/monitoring/monitoring_checks`)\n"
           "ORDER BY status DESC, area")
    r.code("-- Q&A only: what the AI output looks like (term, assertion type, grounding, quote)\n"
           "SELECT section_name, normalized_term, assertion_type, grounding, quote\n"
           "FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/ontology_labeled_reactions`\n"
           "WHERE section_name = 'Boxed Warning' ORDER BY label_key, normalized_term LIMIT 12")
    r.p("**Signal to pre-select:** none. Leave page 1 unfiltered, and choose semaglutide live, so the room sees the "
        "filter work. NAION is then row 1.")
    r.key("\"The numbers are frozen from our baseline build on 5 November. FAERS runs through 2026 Q2, the latest "
          "quarter the FDA has published; our freshness check puts it at about {{n:monitoring.faers_age_days}} days "
          "old. openFDA recalls were last updated by the FDA on 28 October. DailyMed and RxNorm were pulled on 5 "
          "November. Each source has its own clock, and the screen shows each one.\" Never say 'live' or 'real "
          "time'. Card 3 is a sliding 30-day window: {{n:changes.last_30_days}} on 5 November, a different number "
          "on another day. Say so before anyone asks. Our pipeline refreshes only when a build runs: there is no "
          "schedule yet (another month).", title="Data freshness: the exact words")
    r.how_we_know("Machine timing (`app.timing_s`; browser script, time until the expected text is on screen, View "
                  "mode, 2026-11-05): Morning brief loads in {{n:app.timing_s.morning_brief_load}} s; page switches "
                  "take {{n:app.timing_s.switch_what_changed}} s (what changed), {{n:app.timing_s.switch_recalls}} s "
                  "(recalls) and {{n:app.timing_s.switch_signals_with_labels}} s (signals with the labels panel). "
                  "Human reading time is not included. These are the **only measured speed numbers**. 'Under two "
                  "minutes' for her three questions is a design target, timed by a person with a stopwatch in "
                  "rehearsal (checklist 10); until then say 'designed for under two minutes, not yet timed with a "
                  "person'. The first load is why tab 1 is warmed up before the demo [[OBSERVED]].",
                  title="Speed: what was measured")

    # ------------------------------------------------------------------ 3
    r.chapter("Part A: as the safety officer (0:00 to 7:30)")
    r.p("The app is the Workshop module **MSSM Safety Officer** ({{n:app.workshop_version|raw}}, header MSSM). It has "
        "four tabs: Morning brief, 1 · Not in label, 2 · Recalls, 3 · What changed. Deck slides 3 to 5 cover this "
        "part; the speaking script's **[CLICK]** cues match the clicks below.")

    stop(r, "A0", "The officer's problem", "0:00–1:30", 90, [
        ("Click", "Deck: slides 1 and 2"),
        ("Say", "\"Every morning she has three questions: which drugs have side effects being reported that the "
                "label does not mention, which have an active recall, and what changed since she last looked. One "
                "rule: she trusts only a flag she can trace to its source. {{n:scope.drugs_formulary}} drugs, "
                "{{n:scope.opioids}} opioids and {{n:scope.glp1}} GLP-1s, public data only, no patient data.\""),
        ("Proves", "Communication"),
    ])

    stop(r, "A1", "Morning brief", "1:30–3:00", 90, [
        ("Click", "SWITCH TO APP: Cmd+1 (Workshop). Tab **Morning brief** is open and warmed up"),
        ("On screen", "Cards: 1 · Signals not in the label (ranked) **{{n:signals.ranked|raw}}**; 2 · Active "
                      "recalls **{{n:recalls.active}}**; 3 · Changes in the last 30 days **{{n:changes.last_30_days}}**. "
                      "Below, 'Data as of' per source. Column *We pulled it at*: FAERS = 'quarterly file (no pull "
                      "time)'; RxNorm, openFDA and DailyMed = the pull time on 2026-11-05"),
        ("Say", "\"One number per question. {{n:signals.ranked}} is her review queue, not {{n:signals.ranked}} "
                "findings. {{n:recalls.active}} recalls are active, meaning status Ongoing. "
                "{{n:changes.last_30_days}} things changed in the last 30 days. Below is the trust part: how fresh "
                "each source is.\""),
        ("Proves", "Application (three questions, one screen); trust (as-of per source)"),
        ("Fallback", "Cards spin over 10 s: backup window, app-0, keep talking"),
        ("If asked", "Why no pull time for FAERS? It arrives as quarterly files, so the screen says 'quarterly file "
                     "(no pull time)' on purpose. Fast enough? The only measured numbers are machine timings "
                     "({{n:app.timing_s.morning_brief_load}} s first load); 'under two minutes' is a target until a "
                     "person times it"),
    ], S + "app-0-morning-brief.jpg", "Morning brief: three numbers and the as-of date and pull time of each source.")

    stop(r, "A2", "The noise first, then one drug", "3:00–3:40", 40, [
        ("Click", "Tab **1 · Not in label**. **Before filtering**, point at row 5, **Morphine · Ewing's sarcoma**. Then "
                  "pill **Ingredient Name**, tick **semaglutide**"),
        ("On screen", "Unfiltered: each drug's rank 1, including Morphine · Ewing's sarcoma and Liraglutide · Diabetic "
                      "metabolic decompensation. After the filter, **Semaglutide · Optic ischaemic neuropathy** is rank 1"),
        ("Say", "\"Look at morphine's rank 1: Ewing's sarcoma, a bone cancer. That is almost surely about the "
                "patients, not the drug. This is why {{n:signals.ranked}} is a review queue, not a list of findings: "
                "she dismisses that in one click. Liraglutide's rank 1 is the disease it treats (DQ06). Now one drug: "
                "semaglutide, sold as Ozempic and Wegovy. Number one is NAION: sudden vision loss from poor blood flow "
                "to the optic nerve.\""),
        ("Proves", "Application (one drug; the noise is named, not hidden)"),
        ("Fallback", "The A3 screenshot (unfiltered: morphine row 5, NAION row 1)"),
        ("If asked", "Why rank per drug? She reviews drug by drug, and the size of the statistic depends on how many "
                     "reports a drug has. One overall ranking would let the busiest drug fill the top"),
    ])

    stop(r, "A3", "The evidence: why NAION is flagged", "3:40–4:30", 50, [
        ("Click", "The NAION row. The right panel 'Evidence and triage' fills"),
        ("On screen", "Reports {{n:signals.naion.a}} · all reports for the drug {{n:signals.naion.all_reports_drug|raw}} · "
                      "PRR {{n:signals.naion.prr}} · 95% CI {{n:signals.naion.prr_ci_low}} to "
                      "{{n:signals.naion.prr_ci_high}} · Chi² {{n:signals.naion.chi2_yates|raw}} · mass reports 0 · "
                      "label status not_in_label · reference labels searched {{n:app.labels_searched_naion}} · labels "
                      "also read by AI 0 · method text+ai_v1+syn_v2 · bucket clinical. The decisions table is empty"),
        ("Say", "\"{{n:signals.naion.a}} reports name semaglutide and NAION, out of "
                "{{n:signals.naion.all_reports_drug}} semaglutide reports. NAION is about 112 times more common among "
                "semaglutide's reports than among other drugs' reports: a reporting pattern, not 112 times the risk. "
                "The interval runs from 92 to 137, so it is not a small-numbers fluke, but news coverage can still "
                "inflate it (DQ04). And NAION is not new: EMA's safety committee concluded in June 2025 that it is a "
                "very rare side effect of semaglutide. We lead with it because a monitor that missed it would be "
                "broken. Ours ranks it first.\""),
        ("Point", "Do not read out the engineering fields. At *Label check method* text+ai_v1+syn_v2 say: \"That code "
                  "names the rule version, not which checks ran. The AI has not read these labels: look at *Labels "
                  "also read by AI: 0*.\""),
        ("Proves", "Application (trace on screen)"),
        ("Fallback", "This screenshot"),
        ("If asked", "Caused by semaglutide? We do not claim that: 'reported, not on the US label' (A003). Isn't NAION "
                     "already known? Yes: EMA's PRAC, 6 June 2025; WHO alert, 27 June 2025; the 3 US label versions "
                     "we search do not mention it (DECISIONS learning 2026-11-05). A known positive that the pipeline "
                     "finds at rank 1 from FAERS alone; whether it would have flagged it earlier is unproven (backtest "
                     "cut, D031)"),
    ], S + "app-1-not-in-label-naion.jpg", "Page 1: ranked signals with the NAION evidence open.")

    stop(r, "A4", "Reference labels searched, then DailyMed itself", "4:30–5:20", 50, [
        ("Click", "Scroll the right panel to **Reference labels searched**. **Mandatory:** click the **Ozempic v20** "
                  "DailyMed link; Cmd+F `optic` (or `ischemic optic`, per checklist 8); show no optic neuropathy; "
                  "Cmd+W back to the app"),
        ("On screen", "{{n:app.labels_searched_naion}} rows: **Ozempic v20** (2026-06-01), **Wegovy v19** "
                      "(2026-06-18), **oral Ozempic v14** (2026-01-30); safety sections searched; a DailyMed link each"),
        ("Say", "\"These are the three labels we searched, by exact version. Our exact-text check and reviewed "
                "synonym table find NAION in none of them; the AI has not read them. This is Ozempic's label on "
                "DailyMed itself. I search for 'optic': no optic neuropathy. She can repeat this check in ten seconds. "
                "What she cannot do yet is open the {{n:signals.naion.a}} reports from this screen: we pull their case "
                "IDs by query today, and that is the first thing we would add before anyone takes this to P&T.\""),
        ("Proves", "Application (every flag traces to its source); AI reliability (says what the AI did not do)"),
        ("Fallback", "This screenshot; the DailyMed search screenshot from rehearsal (checklist 8)"),
        ("If asked", "How does the panel find them? Signal → Drug → Products → Reference Label; no dedicated link "
                     "type yet. Check order? In code: (1) an AI term with a code-found quote, (2) the exact term or "
                     "US spelling in a safety section, (3) a reviewed synonym. Same outcome in any order; only the "
                     "recorded method differs (`ontology_signals.py` l.163–176). For NAION only (2) and (3) ran. "
                     "Really missing? None of the 36 safety sections in any semaglutide label in DailyMed mention it "
                     "(A014)"),
    ], S + "app-1c-labels-searched-naion.jpg",
        "Page 1: the reference labels searched for NAION, by version, with DailyMed links.")

    stop(r, "A5", "Triage this signal: the Action form", "5:20–6:00", 40, [
        ("Click", "**Triage this signal**; point at the locked fields; **Cancel** (default). Only if the owner chose "
                  "Submit: Decision **reviewing**, a one-line rationale, **Submit**; the row appears above the record"),
        ("On screen", "Form Create MSSM Triage Decision. Subject Type, Subject Key and Evaluation Id f55055e199e8e9d3 "
                      "are filled and locked; Decision (reviewing, dismissed, escalated, monitoring) and Rationale "
                      "are hers"),
        ("Say", "\"This is a Foundry Action. The signal and its evaluation id are filled in and locked; she picks a "
                "decision and writes why. Who and when are set by the system. Submitting creates a new Triage "
                "Decision object; it never edits an old one, and it survives every rebuild. Today only the project "
                "owner can submit, so I will cancel.\""),
        ("Proves", "Application (a triage button that writes back); trust (audit)"),
        ("Fallback", "Form not open within 10 s: this screenshot, same words"),
        ("If asked", "Evidence changes later? The decision keeps the id it was made on and stays linked to the signal "
                     "(the link uses the signal key). The signal gets a new id. The screen does not flag the mismatch "
                     "yet: she compares the id in the decisions table with the id the form shows. A bucket change "
                     "does not change the id (ripple table)"),
    ], S + "app-1b-triage-action-form.jpg", "The triage form: subject and evaluation id locked (captured and cancelled, nothing saved).")

    stop(r, "A6", "Recalls, traced to the FDA's own record", "6:00–6:50", 50, [
        ("Click", "Tab **2 · Recalls**. Is Active = Yes should be preset (deck script); if not, click the pill. "
                  "Click the top row **{{n:recalls.newest|raw}}**; **Cmd+9** (the openFDA record, pre-opened): same "
                  "number, same lot; **Cmd+1** back; click the **Class** column so Class I comes first"),
        ("On screen", "Recalls newest first. Detail: Class II · Ongoing · tirzepatide/niacinamide 2 mL vial · Houston Rx "
                      "LLC · lack of assurance of sterility · reported {{n:recalls.newest_reported|raw}} · "
                      "**matched to our products 0**"),
        ("Say", "\"{{n:recalls.active}} open FDA recalls, status Ongoing, name one of our 13 ingredients. The "
                "newest is a compounded tirzepatide vial, reported 21 October. It matches none of the 658 FDA-listed "
                "products we track: we have no inventory data, so if she buys compounded GLP-1s, she checks her "
                "purchasing records. Here is the FDA's own record of it: same number, same lot. Sorted by class, the "
                "Class I recalls come first.\" (Say the Class I count only if checklist 9 measured it)"),
        ("Proves", "Application (question 2); Data judgment (honest matching); trust (FDA record)"),
        ("Fallback", "This screenshot (D-0788-2026, Class I, lower in the list). openFDA tab fails: skip it"),
        ("If asked", "Which touch my shelves? We cannot know without purchasing data; 'matched' means the 658 "
                     "FDA-listed products, via NDC codes in the recall text. Class I count and D-0788-2026's match: "
                     "not measured unless checklist 9 was done. Active = openFDA status Ongoing (`clean_recalls.py` l.69); Completed and Terminated are not "
                     "active. Recall to drug: the ingredient named in the recall text. Recall to product: NDC codes in "
                     "the recall's own text, high or medium confidence"),
    ], S + "app-2-recalls.jpg", "Page 2: recalls for the formulary, newest first, with the openFDA detail.")

    stop(r, "A7", "What changed", "6:50–7:30", 40, [
        ("Click", "Tab **3 · What changed**; Start date box, preset **Past month** (or the date of her last review)"),
        ("On screen", "Oct 6 to Nov 5: label versions effective (liraglutide v11, 30 Oct), recall D-0040-2027 reported "
                      "(21 Oct). Entity type: label 15, recall 11 = {{n:changes.last_30_days}}, the same as card 3"),
        ("Say", "\"Every change is an event, dated by the source itself. 'Since my last review' is simply this start "
                "date: the past month gives {{n:changes.last_30_days}} events, the same as the morning brief. A label "
                "row tells her a new version took effect, not what changed in it; on DailyMed she opens Recent Major "
                "Changes. And new signals arrive only with each FAERS quarter, about "
                "{{n:monitoring.faers_age_days}} days behind. So that is her morning today: the sources publish daily "
                "(DailyMed) and weekly (openFDA); our pipeline refreshes when a build runs, with no schedule yet; "
                "signals move once a quarter.\""),
        ("Proves", "Application (question 3)"),
        ("Fallback", "This screenshot (or app-3, unfiltered)"),
        ("If asked", "False alarms? A rebuild with no new data added {{n:changes.snapshot_diff_after_rebuild}} "
                     "events. No signal changes yet: they come only from comparing builds, so they appear after the next "
                     "FAERS quarter or synonym edit. The start date does not fill itself from her last decision "
                     "yet (D045, proposed)"),
    ], S + "app-3b-what-changed-past-month.jpg", "Page 3 with the Past month preset: 26 events, the same as card 3.")

    # ------------------------------------------------------------------ 4
    r.chapter("Part H: under the hood (7:30 to 20:00)")
    r.p("One stop per deck slide (6 to 16), plus the live switches the speaking script cues. Switches marked "
        "optional are the first cuts when late.")

    stop(r, "H1", "Architecture in one picture", "7:30–8:30", 60, [
        ("Click", "BACK TO DECK: slide 6, diagram 38 (the one-page architecture picture). Detailed fallback if asked: "
                  "diagram 30 v2 (`docs/diagrams/png/30-handin-data-flow-v2.png`, every dataset, O3 measured)"),
        ("Say", "\"Four public sources. Raw keeps exactly what each source sent. Clean checks and de-duplicates it, "
                "and resolves drug identity once, in one dataset: clean_drug_identity. Curated holds the statistics, "
                "signals, change events and monitoring. The Ontology sits on top, and the app reads only the "
                "Ontology.\""),
        ("Proves", "Architecture"),
    ])

    stop(r, "H2", "Data Lineage, live", "8:30–9:30", 60, [
        ("Click", "SWITCH: Cmd+2 (graph already laid out)"),
        ("On screen", "Yellow raw transforms (raw_dailymed_spl_xml, raw_openfda_drugsfda, raw_rxnorm_related, "
                      "raw_openfda_ndc, raw_faers_quarter_files from source src_faers_files), pink clean "
                      "transforms, ending in ontology_signal_signals"),
        ("Say", "\"This is Foundry's own graph, not a drawing. Follow RxNorm into clean_drug_identity. Everything "
                "after it, FAERS, labels and products, joins on one ingredient ID. That is 'drug identity resolved "
                "once, in the right place'.\""),
        ("Proves", "Architecture"),
        ("Fallback", "This screenshot (deck backup B12), or diagram 30 v2"),
        ("If asked", "Why polars, not Spark? Lightweight transforms took about 1 min against about 4 min for Spark "
                     "(learning 2026-11-04), and the same code runs on a laptop, which is how we test it (A014)"),
    ], S + "hood-data-lineage-signals.jpg", "Data Lineage: sources, raw, clean and curated, ending in ontology_signal_signals.")

    stop(r, "H3", "The Ontology in one picture", "9:30–10:15", 45, [
        ("Click", "BACK TO DECK: slide 7, diagram 31 (ontology)"),
        ("Say", "\"Ten object types: Drug, Product, Label, Recall, Labeled Reaction, AE Stat, Signal, Change Event, "
                "Source Status, Triage Decision. Only Triage Decision is written, and only through one create-only "
                "Action. One mistake is on the picture on purpose: a duplicate Signal-to-Drug link added by "
                "accident. Nothing uses it; it is left for the owner to delete.\""),
        ("Proves", "Architecture"),
    ])

    stop(r, "H4", "Ontology Manager", "10:15–10:45", 30, [
        ("Click", "SWITCH: Cmd+3"),
        ("On screen", "MSSM Signal · {{n:signals.total}} objects · 25 properties · Edits disabled · Experimental"),
        ("Say", "\"Each object type is backed by one curated dataset. Signal has {{n:signals.total}} objects. Edits are "
                "off: signals come only from the pipeline. The Action lives on Triage Decision, which points at the "
                "signal.\""),
        ("Proves", "Architecture"),
        ("Fallback", "This screenshot"),
    ], S + "hood-ontology-manager-signal.jpg", "Ontology Manager: the MSSM Signal object type.")

    stop(r, "H5", "Object Explorer: follow one flag to its source", "10:45–11:30", 45, [
        ("Click", "SWITCH: Cmd+4 (search done, NAION selected, Links tab); MSSM AE Stat; back; MSSM Drug, MSSM "
                  "Products, Reference Label (DailyMed link)"),
        ("On screen", "Links: Drug of signal 1 (the duplicate) · MSSM AE Stat 1 · MSSM Drug 1. No Triage Decisions "
                      "link, because the form was cancelled (with Submit: MSSM Triage Decisions 1)"),
        ("Say", "\"The trust rule as data. From the signal to its statistics, the 2-by-2 table of counts. From the "
                "drug to its products and the reference label, with the DailyMed link: the same path the page 1 "
                "panel walks.\""),
        ("Proves", "Application (trace: every flag traces to its source)"),
        ("Fallback", "This screenshot (deck backup B4); the baseline-gate trace (5 of 5 random flags re-counted by hand)"),
        ("If asked", "FAERS case IDs: SQL on clean_faers_drug_reaction (the baseline gate lists examples); the "
                     "screen does not link to case rows yet"),
    ], S + "hood-object-explorer-naion-links.jpg", "Object Explorer: the NAION signal and its links.")

    stop(r, "H6", "One FAERS report to a ranked signal", "11:30–12:30", 60, [
        ("Click", "BACK TO DECK: slide 8, diagram 32 v2 (signal pipeline, label checks in code order)"),
        ("Say", "\"A: keep only the latest version of each case and apply deletes to all history; appending quarters "
                "gave 8.7% phantom rows. Count only suspect drugs. Match names exactly through RxNorm; substring "
                "matching added 50% false morphine rows. Set aside reports listing 30 or more drugs. B: the 2-by-2 "
                "table, PRR and the Evans rule. C: in the label? In code: an AI term with a quote, then the exact "
                "text, then the reviewed synonym table. D: only clinical reactions are ranked; the rest is "
                "tagged.\""),
        ("Proves", "Data judgment"),
        ("Sources", "DQ36 and D022 (versions, deletes), D021 (roles), DQ34 and D020 (identity), D023 v2 (mass "
                    "reports), D006 (Evans, proposed), D043 (synonyms), D016 v3 (buckets)"),
    ], D + "32-handin-signal-pipeline-v2.png", "Diagram 32 v2: from one FAERS report to a ranked signal.", fig_h=200)

    stop(r, "H7", "The signal code (optional)", "12:30–12:50", 20, [
        ("Click", "Optional SWITCH: Cmd+5 (ontology_signals.py, lines 22 to 29). First cut if late"),
        ("On screen", "RULE = \"prr_evans_v2\" · MAX_DRUG_ROWS = 30 · LABEL_CHECK = \"text+ai_v1+\" + SYN_VERSION · "
                      "WINDOW = \"FAERS 2026Q1-2026Q2\" · BUCKETS: keyword stand-in for MedDRA groupings (no MedDRA "
                      "licence)"),
        ("Say", "\"Each rule is a named constant with a decision number. The buckets are keyword lists because we "
                "have no MedDRA licence, and the code says so.\""),
        ("Proves", "Architecture (another engineer can extend it)"),
        ("Fallback", "This screenshot"),
    ], S + "hood-code-repo-ontology-signals.jpg", "Code Repository pipelines_clean: ontology_signals.py and the file tree.")

    stop(r, "H8", "A review queue, not findings", "12:50–13:30", 40, [
        ("Click", "BACK TO DECK: slide 9"),
        ("Say", "\"{{n:signals.ae_stats}} drug-reaction statistics, {{n:signals.total}} signals, {{n:signals.ranked}} "
                "ranked. The queue after each label-check or bucket change: {{n:signals.ranked_history.step9}} at step 9, our "
                "first full build, then {{n:signals.ranked_history.syn_v1}}, {{n:signals.ranked_history.d016_v3}} and "
                "{{n:signals.ranked_history.syn_v2}}. {{n:signals.possibly_in_label}} are 'possibly in label', kept "
                "but never ranked. The {{n:synonyms.rows}}-row synonym table was drafted by Claude; no pharmacist has "
                "reviewed it yet.\""),
        ("Proves", "Data judgment"),
    ])

    stop(r, "H9", "AI reliability", "13:30–14:45", 75, [
        ("Click", "Slide 10. Optional SWITCH: Cmd+6, ai_label_extraction.py lines 16 to 25, then the SQL panel "
                  "(AI cache query already run)"),
        ("On screen", "MODEL_ID \"claude-sonnet-5.5\" · PROMPT_VERSION \"p2\" · PARSER_VERSION \"x1\" · PILOT_SETIDS "
                      "({{n:ai.pilot_labels}} oxycodone labels). SQL: {{n:ai.sections}} rows, n_reactions = n_grounded, "
                      "from_cache true"),
        ("Say", "\"Claude Sonnet 5.5 read {{n:ai.sections}} safety sections of {{n:ai.pilot_labels}} oxycodone pilot "
                "labels and returned each reaction with an exact quote. Code finds every quote word for word: "
                "{{n:ai.grounded}} of {{n:ai.reactions}}. On a small answer key, 35 items from the Boxed Warning and "
                "Contraindications of those 2 labels, written by Claude before the run, it found 35 of 35 answer-key "
                "items: F1 {{n:ai.gold_f1}} against a target of {{n:ai.d015_target_f1}}. No pharmacist has checked "
                "the key, and the long sections are not scored. The AI has not read semaglutide labels, and today it "
                "does not change the signal list. On the last rebuild: {{n:ai.model_calls_on_rebuild}} model "
                "calls.\""),
        ("Proves", "AI reliability; Optimization (O1)"),
        ("Fallback", "This screenshot and hood-code-ai-label-extraction (also deck/assets/ai-cache-sql-crop.png)"),
    ], S + "hood-ai-extractions-cache-sql.jpg", "SQL on ai_label_section_extractions: every section grounded and served from cache.")

    stop(r, "H10", "Monitoring", "14:45–15:30", 45, [
        ("Click", "Slide 11. Optional SWITCH: Cmd+5, SQL panel (monitoring query already run), or Cmd+7, Health tab"),
        ("On screen", "faers.reporter_type_blank **warn**; ai.grounded_rate 1 pass; ai.section_errors 0 pass; "
                      "ai.cache_hit_rate 1; key checks pass. Health tab: Build status and Primary key Passed"),
        ("Say", "\"Every build appends {{n:monitoring.checks_per_build}} checks: keys, row counts, freshness, AI "
                "grounding, cache hits; plus {{n:monitoring.data_health_checks}} Foundry Data Health checks. It "
                "caught two real shifts: reporter type blank went from {{n:monitoring.reporter_type_blank_q1|.0%}} to "
                "{{n:monitoring.reporter_type_blank_q2|.0%}}, and recalls for our drugs from "
                "{{n:monitoring.recalls_prev4w}} to {{n:monitoring.recalls_last4w}} in four weeks. The drift is a "
                "replay from source dates, not weeks of live builds.\""),
        ("Proves", "AI reliability (stretch goal: notice if it gets worse); Data judgment"),
        ("Fallback", "This screenshot; hood-data-health-signals; hood-monitoring-drift-sql"),
    ], S + "hood-monitoring-checks-sql.jpg", "SQL on monitoring_checks: the latest run, one real warning (DQ38).")

    stop(r, "H11", "Optimization log", "15:30–16:45", 75, [
        ("Click", "Slide 12"),
        ("Say", "\"O1, the AI cache: {{n:optimization.O1.before_calls}} model calls and "
                "{{n:optimization.O1.before_tokens}} tokens became zero on a rebuild. Helped. O2, incremental FAERS: "
                "{{n:optimization.O2.incremental_add_q2_s}} seconds against {{n:optimization.O2.full_rebuild_s}}. Did "
                "not help. O3, reusing DailyMed XML we already hold: 3 minutes 23 to 1 minute 23, and "
                "{{n:optimization.O3.before_downloads}} XML downloads to {{n:optimization.O3.after_downloads}}; the "
                "index pages are still pulled every build. Helped. O3a, parsing fewer columns: "
                "{{n:optimization.O3a.local_run_before_s|raw}} s to {{n:optimization.O3a.local_run_after_s}} s, "
                "locally; reverted. Partitioning: none in the pilot (D048, proposed); we revisit at 8 FAERS quarters "
                "or a 5-minute build. Each timing is one run.\""),
        ("Proves", "Optimization (measured, failures included)"),
    ])

    stop(r, "H12", "Incremental FAERS", "16:45–17:30", 45, [
        ("Click", "Slide 13 (diagram 33 v2). Optional SWITCH: Cmd+8, clean_faers_inc_log preview"),
        ("On screen", "2026q1: {{n:faers.q1_cases}} cases; 2026q2: {{n:faers.q2_cases_replaced}} replaced, "
                      "{{n:faers.q2_cases_deleted}} deleted, {{n:faers.cases_current}} after"),
        ("Say", "\"The incremental path reads only the new quarter into a kept state: three state datasets and one "
                "quarter log. Its output equals the full rebuild row for row. But at two quarters it is slower: "
                "{{n:optimization.O2.state_s}} s for the state plus {{n:optimization.O2.outputs_s}} s for the outputs, "
                "against {{n:optimization.O2.full_rebuild_s}} s. So signals keep reading the full rebuild (D044), and "
                "we re-measure at four or more quarters.\""),
        ("Proves", "Optimization (incremental against full, measured)"),
        ("Fallback", "This screenshot"),
    ], S + "hood-faers-inc-log-sql.png", "SQL on clean_faers_inc_log: one row per quarter, with cases replaced and deleted.")

    stop(r, "H13", "Data judgment and what we chose not to do", "17:30–19:00", 90, [
        ("Click", "Slide 14. Optional SWITCH: Cmd+5, SQL panel, point at faers.reporter_type_blank **warn**"),
        ("Say", "\"Four messes that would have changed her answers. FAERS updates and deletes old cases: Q2 replaced "
                "{{n:faers.q2_cases_replaced}} Q1 cases and deleted {{n:faers.q2_cases_deleted}}. Mass reports listing "
                "dozens of drugs: out of the main count, kept as evidence. Reporter type went from "
                "{{n:monitoring.reporter_type_blank_q1|.0%}} to {{n:monitoring.reporter_type_blank_q2|.0%}} blank: we "
                "show 'unknown'. DailyMed sometimes answers 'success' with the word 'None' (2 of 1,321, DQ42): kept, "
                "marked, retried. Noise we left: indication terms, like liraglutide's top signal 'Diabetic metabolic "
                "decompensation' (DQ06), and stimulated reporting after news or lawsuits (DQ04); the pharmacist's "
                "triage decides. Not done: no MedDRA licence, no patient data.\""),
        ("Proves", "Data judgment"),
        ("Sources", "DQ36, D022, D023 v2, DQ38, DQ42, DQ06, DQ04"),
        ("Fallback", "The H10 screenshot (also deck/assets/monitoring-checks-sql-crop.png)"),
    ])

    stop(r, "H14", "Another month", "19:00–19:40", 40, [
        ("Click", "Slide 15"),
        ("Say", "\"The biggest gap is a named pharmacist. Today only Claude has checked the synonym bands, the answer "
                "key and the ranked signals. Claude prepares an evidence packet; the pharmacist decides; a "
                "create-only Action records who, when and on which evidence. Then schedules, live drift over three "
                "to four weeks, and a health page. Widening the AI to the semaglutide labels is the owner's next "
                "decision (D041 v2, not written yet).\""),
        ("Proves", "Communication"),
    ])

    stop(r, "H15", "What to take away", "19:40–20:00", 20, [
        ("Click", "Slide 16"),
        ("Say", "\"It answers her three questions, and every flag traces to its source: the label versions searched "
                "and the FDA recall record open in one click; the FAERS case reports are reachable by query, not yet "
                "from her screen. It is built to be extended, and "
                "we sped up only what we measured. And we say what is not proven yet, including that the AI has not "
                "read the hero drug's labels.\""),
        ("Proves", "Communication"),
    ])

    # ------------------------------------------------------------------ 5
    r.chapter("Plan B and hard questions")
    r.p("Rule from rehearsal: a page that takes more than 10 seconds to load in rehearsal is shown as a screenshot "
        "in the demo. The backup window holds every screenshot in this guide.")
    r.table(["#", "Moment", "What can go wrong", "Plan B"], [
        ("1", "1:30 Morning brief first load", "Cards spin; session timed out",
         "Warm all 4 tabs 5 minutes before. Over 10 s: the A1 screenshot, keep talking, rejoin the live app at A2"),
        ("2", "5:20 Triage form", "Slow to open; Submit pressed by mistake",
         "Default is Cancel. Slow: the A5 screenshot, same words. A Submit by mistake cannot be undone: say so "
         "plainly ('this is what create-only means') and move on"),
        ("3", "8:30 Data Lineage", "Slow, or re-laid-out into a tangle",
         "Lay out during setup; never press Layout. Messy: the H2 screenshot"),
        ("4", "12:30 to 17:30 Code and SQL", "Repo still starting; SQL slow; accidental keystroke",
         "Open 10 minutes early, pre-run the queries, never type in the editor (close the tab without "
         "committing if you do). Slow: stay on the slide"),
        ("5", "Any time: numbers differ from slides", "Card 3 slides with the date; someone rebuilt raw",
         "Say it first: '{{n:changes.last_30_days}} on 5 November; it is a sliding window'. If cards 1 or 2 moved: "
         "'the data refreshed since our baseline; the slides are from 5 November'"),
    ], widths=[0.3, 1.5, 1.8, 3.4])

    r.h("The three rubric-check questions, prepared")
    r.p("A reviewer is likely to ask these (from `reviews/rubric-check.md`). Each answer is said honestly, and each "
        "has a place to click.")
    r.table(["Question", "Answer", "Where to show it"], [
        ("Your AI read two labels and does not change the list. What is it doing, and how often is it wrong?",
         "On purpose, the AI is the evidence layer today, not the decision layer. It has read 0 semaglutide labels, "
         "so NAION is not in label from the exact-text and synonym checks. Every AI quote is found word for word "
         "({{n:ai.grounded}} of {{n:ai.reactions}}); on the 35-item Claude-written key (2 oxycodone labels, Boxed "
         "Warning + Contraindications, no pharmacist yet) it found 35 of 35 answer-key items, F1 {{n:ai.gold_f1}}. "
         "Widening to semaglutide is a D041 v2 decision for the owner: first a pharmacist-scored sample of the long "
         "sections, then widen",
         "Page 1 NAION: labels also read by AI 0. Tab 6: PILOT_SETIDS (line 22). Q&A SQL on "
         "ontology_labeled_reactions: term, grounding, quote. Deck slide 10"),
        ("Liraglutide's top 'unlabeled' signal is the disease it treats.",
         "Yes: 'Diabetic metabolic decompensation', an indication term (DQ06), left and named. D016 v3 tags some "
         "efficacy words, not this one. With another month: an indication-term list per drug; until then the "
         "pharmacist's triage dismisses it",
         "Page 1 unfiltered, row 2 (A3 screenshot), or filter liraglutide. Tab 5: BUCKETS, efficacy line"),
        ("How many of NAION's {{n:signals.naion.a}} reports came after news or from lawyers?",
         "Not measured. Stimulated reporting (DQ04) is a known gap we left; triage judges it. A reporter split is "
         "weak anyway: reporter type is blank for {{n:monitoring.reporter_type_blank_q1|.0%}} (Q1) and "
         "{{n:monitoring.reporter_type_blank_q2|.0%}} (Q2) of reports (DQ38). With another month: NAION's "
         "reporter-type split, and a spike flag near known events",
         "Tab 5 SQL: faers.reporter_type_blank warn; drift replay screenshot (reporter type blank x2.1). Deck "
         "slide 14"),
    ], widths=[1.6, 3.2, 1.8])

    r.h("Change here, changes there (summary)")
    r.p("Judges often ask \"what happens if …\". The full table, checked against the code, is "
        "`docs/11-handin/demo/ripple-table.md`. Nothing is changed live; build times not in numbers.json are not "
        "measured, so do not promise them.")
    r.table(["Change this here", "This changes there", "Evaluation id", "Show"], [
        ("Synonym row (+ SYN_VERSION)", "label status, ranked queue, build-dated change events", "every signal",
         "history: {{n:signals.ranked_history.step9}} to {{n:signals.ranked}}"),
        ("Bucket regex", "bucket, is_ranked, change events", "unchanged", "the code"),
        ("New FAERS quarter (+ WINDOW)", "counts, PRR, every AE Stat key, signals, freshness", "yes", "inc log"),
        ("Drug added (5 formulary lists)", "every layer; FAERS state replays all quarters", "new signals", "no"),
        ("New DailyMed label version", "one download; label check; one build-dated 'spl version' event",
         "only if label counts change", "page 3 history"),
        ("Recall status change", "card 2, page 2; one build-dated 'status' event", "n/a", "page 3 history"),
        ("Triage decision", "one Ontology object; nothing else; cannot be deleted", "stores it", "form, Cancel"),
        ("Prompt or model version", "cache key; all pilot sections re-sent", "only if AI label count changes", "code"),
        ("Workshop variable", "that card only; no build", "n/a", "definition only"),
    ], widths=[1.8, 2.6, 1.3, 1.3])
    r.note("The decision is not edited and stays linked to its signal (the link uses the signal key). It keeps the "
           "old evaluation id, so it still shows on page 1 under the signal. Nothing on screen flags the mismatch, "
           "and the change feed does not watch the evaluation id. A bucket change keeps the id. If the signal leaves "
           "(now in the label), the decision stays in Object Explorer but no longer shows on page 1.",
           title="What happens to an existing triage decision when the evaluation id changes")
    r.figure(D + "37-handin-ripple-v2.png", "Ripple map (diagram 37 v2): change here, changes there.",
             source="docs/diagrams/png/37-handin-ripple-v2.png", max_height=300)

    r.gate("Demo ready", [
        ("Required evidence", "Two rehearsal passes done (tech run, dress run) with measured seconds per stop; every "
                              "live stop has a fallback screenshot open in the backup window; the owner's Cancel or "
                              "Submit choice is written down."),
        ("Result", "Guide, ripple table and rehearsal plan written and aligned with the speaking script. Machine "
                   "timings measured (brief {{n:app.timing_s.morning_brief_load}} s). Rehearsals and a human timed "
                   "walk-through not yet run."),
        ("If it fails", "Use screenshots for every stop slower than 10 s, and take the cuts in chapter 1."),
    ], status="PLANNED")

    r.numbers_appendix()
