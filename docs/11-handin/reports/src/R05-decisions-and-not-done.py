"""R05 Decisions and what we chose not to do.

Build:  .venv/bin/python tools/handin/build_report.py R05-decisions-and-not-done
Output: docs/11-handin/reports/pdf/R05-decisions-and-not-done.pdf

Sources: docs/06-decisions/DECISIONS.md (decisions, decision changes, learnings), docs/05-approaches/INDEX.md and the
A-files, docs/07-data-quality/data-issues-register.md (DQ ids), docs/08-optimization-log/optimization-log.md,
eval/ai-eval-v1.md, docs/09-roadmap/. Numbers via {{n:...}} from docs/11-handin/numbers.json; evidence that is not
in numbers.json is described in words and cited by its DQ / learning id, and listed in the appendix table
"Figures quoted from project records".
Phase D (2026-11-05): fact-check W2, S4, S5, S6, S8, X1-X4 and first-time-reader R05 items fixed; diagram 32 v2.
"""

META = {
    "id": "R05",
    "title": "Decisions, and what we did not do",
    "short": "Decisions",
    "subtitle": "the choices that shaped the build, how they changed, and what we left out on purpose",
    "version": "1.2",
    "date": "6 November 2026",
}

D = "docs/diagrams/png/"


def _mmss(sec):
    m, s = divmod(int(sec), 60)
    return f"{m} m {s:02d} s"


def build(r):
    # computed values (DERIVED from numbers.json)
    q1 = r.n("faers.q1_cases")
    touched = r.n("faers.q2_cases_replaced") + r.n("faers.q2_cases_deleted")
    follow_share = f"{touched / q1:.1%}"
    h = {k: r.n(f"signals.ranked_history.{k}") for k in ("step9", "syn_v1", "d016_v3", "syn_v2")}
    syn1_drop = f"{(h['step9'] - h['syn_v1']) / h['step9']:.1%}"
    o2_ratio = f"{r.n('optimization.O2.incremental_add_q2_s') / r.n('optimization.O2.full_rebuild_s'):.2f}"
    o3_before, o3_after = _mmss(r.n("optimization.O3.before_s")), _mmss(r.n("optimization.O3.after_s"))
    o3_cut = f"{1 - r.n('optimization.O3.after_s') / r.n('optimization.O3.before_s'):.0%}"

    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "Which decisions shaped the build, why did we make them, how did they change as the data taught us, "
               "and what did we deliberately leave out?"),
              ("One-line answer",
               "About a dozen decisions carry the design: an explicit formulary, DailyMed as label truth, drug "
               "identity resolved once, strict FAERS counting rules, a three-step label check (AI terms, exact text, "
               "reviewed synonyms), a cached and grounded "
               "AI step, and an incremental pipeline we kept but did not switch on. Several changed version as the "
               "data showed us problems. We left out licensed vocabularies, patient data, AI judging signals and "
               "anything we could not finish properly.")],
        is_=["An explanation of the decisions that mattered most, each with options, reasons and evidence",
             "A history of how decisions changed (we never edit a decision in place)",
             "A list of what we chose not to do, and why",
             "The approaches we replaced or reverted, kept as part of the record"],
        is_not=["The full decision log: that is `docs/06-decisions/DECISIONS.md` (D001 to D048)",
                "A pipeline manual (see the pipeline and Ontology reports)",
                "A list of open decisions: the last 12 proposed ones (D006, D015, D025, D026, D027, D028, D029, "
                "D037, D045, D046, D047, D048) were accepted in one batch on 6 November 2026, with D041 v2",
                "Reviewed by a pharmacist"],
        how_to_read="Chapter 1 is the summary and the method. Chapters 2 to 6 each take one theme and explain its "
                    "decisions: options considered, why, evidence, and status. Chapter 7 is the decision-change "
                    "history. Chapters 8 and 9 are what we chose not to do and the approaches we replaced. Codes: "
                    "D### is a decision in the decision log, DQ## a data issue in the data-issues register, A### an "
                    "approach file (something we tried), O# an entry in the optimization log. Numbers come from "
                    "`numbers.json`; where a piece of evidence was not captured there, we cite its record (see the "
                    "appendix table).",
    )

    # ------------------------------------------------------------------ 01 summary
    r.chapter("Summary and method")
    r.p("**The brief says: where it is silent, decide and write it down.** We did, in one decision log. A "
        "decision has an id, a date, a reason, the alternatives we rejected and a status (Proposed, Accepted or "
        "Superseded). A decision is **never edited in place**: when it changes, it gets a new version (D016 v2, "
        "v3) or a new id, and a row in a *decision changes* table records the before, the after and the evidence "
        "that triggered it. Small realisations go in a *learnings* table.")
    r.p("**What the pilot covers.** {{n:scope.drugs_formulary}} drugs on a hospital formulary: {{n:scope.opioids}} "
        "opioids (oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, buprenorphine, tramadol) and "
        "{{n:scope.glp1}} GLP-1 medicines (semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide). Four public "
        "sources: FAERS (the FDA's adverse event reports), DailyMed (official label text), openFDA recalls and RxNorm "
        "(drug names and IDs). A *signal* is a drug and reaction reported unusually often (PRR, the proportional "
        "reporting ratio, with the Evans rule; D006) that is not found in the drug's label.")
    r.p("**Status words.** *Accepted* = the owner has agreed. *Proposed* = written down and usually built, waiting "
        "for the owner's OK. *Superseded* = replaced by a newer version or decision. D039 is the dataset-contracts decision; its gates G1 to G6 settled several earlier "
        "decisions during the build (for example G6 accepted D020 to D024 for the pilot).")
    r.p("**Twelve decisions were accepted in one batch on 6 November 2026** (the owner's words: \"Accept all "
        "12\"): D006 (the Evans signal rule), D015 (the AI target, F1 0.85 or more; only the target: its TAC 2017 / "
        "OnSIDES benchmark stays cut by D031), D025 (fill-rate monitoring), D026 (the bridge sources Drugs@FDA and "
        "NDC Directory), D027 (two-level identity), D028 ('since yesterday' = since last review), D029 (FAERS is "
        "quarterly), D037 (the exact-text label check), D045 (change feed), D046 (monitoring), D047 (DailyMed XML "
        "reuse) and D048 (no partitioning). All were already built and running. The same day the owner accepted "
        "**D041 v2**: the AI also reads the 3 semaglutide labels, and page 1 shows its quotes. D031 v3 (an old "
        "schedule) is superseded.")
    r.h("The decisions this report explains")
    r.table(["Theme", "Decision", "In one line", "Status"], [
        ("Scope", "D018", "Formulary = an explicit list of {{n:scope.drugs_formulary}} ingredient IDs, not a drug class",
         "Accepted"),
        ("Sources", "D019", "DailyMed is the source of truth for labels", "Accepted"),
        ("Identity", "D020, D027", "Exact ingredient matching; two levels: ingredient → product (→ package)",
         "D020 accepted (via D039 G6); D027 accepted 6 Nov (product key confirmed by D039 G2)"),
        ("FAERS", "D021, D022, D023", "Which drugs count; which case version counts; fold duplicates", "Accepted"),
        ("Label check", "D041, D037, D043, D016", "AI terms with a quote, exact text, then a reviewed synonym table; "
                                                  "tag non-harm terms", "Accepted (D037 on 6 Nov)"),
        ("AI", "D041, D041 v2", "One cached, grounded model call per label section; v2 adds the 3 semaglutide labels",
         "Accepted (v2 on 6 Nov)"),
        ("Pipelines", "D044, D047, D048", "Incremental FAERS built and proven, not switched on; DailyMed XML reuse; "
                                          "no partitioning in the pilot", "Accepted (D047, D048 on 6 Nov)"),
        ("Product", "D045, D046", "Change feed for 'what changed'; monitoring as data", "Accepted 6 Nov"),
    ], widths=[0.9, 1.3, 3.7, 1.3])
    r.key("Narrow and working beats broad and half-working. Each time we had to choose between breadth and "
          "depth, we cut breadth: fewer drugs for AI, fewer sources, a replay instead of live drift.",
          title="The rule behind most choices")
    r.key([
        "**The core rules are built and accepted.** D006 (the signal rule), D037 (the exact-text label check) and "
        "D045 (the change feed) run in every build; the owner accepted them on 6 November.",
        "**What we left out shapes her screen.** No MedDRA licence, so synonyms come from a small reviewed table "
        "whose bands no pharmacist has checked yet. FAERS is quarterly, so signals move once a quarter (FAERS is "
        "about {{n:monitoring.faers_age_days}} days behind). The AI reads {{n:ai.pilot_labels}} labels (oxycodone "
        "and semaglutide), so for the other drugs 'not in label' comes from the text and synonym checks. For "
        "NAION all three checks agree: the AI found diabetic-retinopathy terms and no optic-nerve term.",
        "**Every 'no' has a reason and a trigger.** Chapter 8 lists what would make us add each missing piece.",
    ], title="What this means for Dana (the safety officer)")
    r.gate("Summary", [
        ("Required evidence", "Each decision below names its options, its reason, its evidence and its status."),
        ("Result", "Met for the decisions chosen here; the full log runs from D001 to D048."),
        ("If it fails", "A decision without evidence is an opinion: mark it ASSUMED."),
    ])

    # ------------------------------------------------------------------ 02 scope and sources
    r.chapter("Scope and sources")
    r.p("**Two early decisions fixed what we watch and which text counts as 'the label'.**")
    r.h("D018 · The formulary is an explicit list of ingredient IDs")
    r.table(["Part", "Detail"], [
        ("Decision", "The formulary is {{n:scope.drugs_formulary}} RxNorm ingredient IDs (RxCUIs): "
                     "{{n:scope.opioids}} opioids and {{n:scope.glp1}} GLP-1 medicines (D014 chose this opioid-led mix, A003)."),
        ("Options", "(a) a drug class code (ATC N02A: the opioid group in the WHO's Anatomical Therapeutic Chemical "
                    "classification); (b) an explicit list of ingredient IDs."),
        ("Why (b)", "Class codes do not hold our list cleanly: methadone sits in a different class, and hydrocodone "
                    "appears only through combination codes (DQ31). A list is explicit and auditable."),
        ("Evidence", "[[OBSERVED]] DQ31, seen while profiling RxNorm on 2026-10-20."),
        ("Cost", "A new drug must be added by hand. That is acceptable for a hospital formulary, which is a list anyway."),
    ], widths=[1, 5.5])
    r.h("D019 · DailyMed is the source of truth for labels")
    r.table(["Part", "Detail"], [
        ("Decision", "Label text comes from DailyMed SPL XML (the official US label library), not from the openFDA "
                     "copy of labels."),
        ("Options", "(a) openFDA label API (easy JSON); (b) DailyMed XML (harder to parse, but the original)."),
        ("Why (b)", "The openFDA copy lags: for Ozempic it was months behind DailyMed (DQ28). A stale label gives wrong "
                    "'not in label' flags."),
        ("Evidence", "[[OBSERVED]] DQ28 (2026-10-20). We pull {{n:labels.total}} label versions for our drugs."),
        ("Caveats we found later", "DailyMed can itself lag the FDA's SrLC database (Safety-related Labeling "
                                   "Changes) (learning, "
                                   "2026-11-02); and it can answer 'HTTP 200' with the text 'None' instead of XML "
                                   "(DQ42). Raw keeps the reply; clean keeps only real XML."),
    ], widths=[1, 5.5])
    r.gate("Scope and sources", [
        ("Required evidence", "Each choice is backed by a data issue found while profiling, before building (D012: "
                              "profile every source by hand first)."),
        ("Result", "Met: DQ31 and DQ28 were found by hand on real data."),
        ("If it fails", "If a drug the hospital uses is missing, add its RxCUI to the list and rebuild."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 03 identity
    r.chapter("Drug identity, resolved once")
    r.p("**The brief judges whether drug identity is 'resolved once, in the right place'. Ours is resolved in one "
        "clean dataset, `clean_drug_identity`, and every other step joins to it.**")
    r.h("D020 · Exact ingredient matching, never substrings")
    r.table(["Part", "Detail"], [
        ("Decision", "Split FAERS's active-ingredient text on its separator, strip salt names (hydrochloride, "
                     "sulfate ...), and match the result exactly to an RxNorm ingredient."),
        ("Options", "(a) substring or fuzzy name match; (b) exact ingredient after cleaning."),
        ("Why (b)", "A substring match for 'morphine' also hits apomorphine (a Parkinson's drug) and diamorphine "
                    "(heroin); 'fentanyl' hits a fentanyl analogue. That inflated morphine rows by about half (DQ34)."),
        ("Evidence", "[[OBSERVED]] DQ34, measured on the 2026Q2 FAERS file while profiling on 2026-10-20."),
    ], widths=[1, 5.5])
    r.h("D027 · Two levels: ingredient and product (D003 v1 → v2)")
    r.table(["Part", "Detail"], [
        ("Decision", "Drug = ingredient RxCUI. Product = FDA application number. Package = NDC code. All built once "
                     "in the identity step."),
        ("Before", "D003 v1: one join key, the ingredient RxCUI."),
        ("Why it changed", "Counts belong to ingredients, but labels and recalls belong to products: a semaglutide "
                           "injection and a semaglutide tablet have different labels, and linking reports to the wrong "
                           "one created false 'not in label' flags (DQ33). Bulk FAERS has no harmonised label link, but "
                           "it does carry the application number (DQ39, D024)."),
        ("Evidence", "[[OBSERVED]] DQ33 and DQ39. The product key was confirmed as the application number by D039 G2."),
        ("Status", "Accepted on 6 November 2026 (batch). The two levels are built and used by every label and "
                   "recall join."),
    ], widths=[1, 5.5])
    r.gate("Identity", [
        ("Required evidence", "One dataset maps every name we see to an ingredient and a product; nothing downstream "
                              "matches names on its own."),
        ("Result", "Met. When identity changes, incremental FAERS replays all quarters as a new generation (D044), "
                   "so old counts never mix two identity versions."),
        ("If it fails", "A drug appearing twice under two names would split its counts: check distinct RxCUIs per "
                        "name after every identity change."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 04 FAERS rules
    r.chapter("Counting FAERS reports honestly")
    r.p("**FAERS (the FDA Adverse Event Reporting System) is messy. Three rules decide what one report is, and "
        "which drugs in it count.**")
    r.table(["Decision", "Rule", "Option rejected", "Why", "Evidence"], [
        ("D021 suspect roles", "Count a drug if it is primary suspect, secondary suspect or interacting, once per "
                               "report; never concomitant", "Primary suspect only",
         "Primary-only would drop more than half of oxycodone cases (learning 2026-11-04); secondary often repeats "
         "the primary (DQ35)", "[[OBSERVED]]"),
        ("D022 versions and deletes", "Keep the latest version of each case; apply deletes to all history; raw "
                                      "quarters stay append-only", "Append each quarter",
         "Follow-up versions arrive in later quarters and change the drug list; appending double-counts them (DQ36)",
         "[[OBSERVED]]"),
        ("D023 duplicate fold (v1 → v2)", "Fold the same person filed by many companies; v2 also sets aside every "
                                          "report listing 30 or more drugs", "Delete those reports",
         "A mass-polypharmacy cluster (one patient re-filed hundreds of times, ages changing) topped the list with "
         "unrelated reactions", "[[OBSERVED]]"),
    ], widths=[1.3, 2, 1.1, 2.2, 0.9])
    r.how_we_know(["**D022, measured in Foundry:** the 2026Q2 files replaced {{n:faers.q2_cases_replaced}} cases "
                   "and deleted {{n:faers.q2_cases_deleted}} cases from 2026Q1. That is " + follow_share +
                   " of the {{n:faers.q1_cases}} cases in the 2026Q1 file touched in one quarter [[DERIVED]]. Appending quarters "
                   "would have counted those as new reports.",
                   "After all three rules: {{n:faers.cases_current}} current cases, {{n:faers.drug_reaction_rows}} "
                   "drug-reaction rows for our drugs [[OBSERVED]]."])
    r.p("**Why D023 v2 keeps the mass reports visible.** Deleting them would hide evidence. Instead each signal "
        "carries how many of its reports came from mass reports, and a signal that is mostly mass reports gets a "
        "caution and is not ranked. A blunt cut, kept visible, is easier to audit than a silent delete [[DESIGNED]].")
    r.figure(D + "32-handin-signal-pipeline-v3.png",
             "From one FAERS report to a ranked signal: case version (D022), roles (D021), identity (D020), duplicate "
             "and mass-report fold (D023 v2), then statistics, the three label checks in code order (AI, text, "
             "synonyms) and the buckets.",
             source=D + "32-handin-signal-pipeline-v3.png", max_height=360)
    r.gate("FAERS rules", [
        ("Required evidence", "Counts equal an independent prototype; the follow-up effect is measured."),
        ("Result", "Met: Foundry counts equal the 20 October Python prototype exactly (learning 2026-11-04); five "
                   "random signals re-counted by hand at the baseline gate."),
        ("If it fails", "If a count moves without new data, a rule changed: check the rule version in the signal key."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 05 label check
    r.chapter("Is it in the label? Three checks and the buckets", new_page=False)
    r.p("**A signal is only interesting if the label does not already mention it. Deciding 'mentioned' is the "
        "hardest judgment in the project, and the one that changed most.**")
    r.table(["Step", "Decision", "What it does", "Outcome"], [
        ("1 · AI terms", "D041 v2", "Is it among the reactions the AI extracted, with a quote that code found in the "
                                 "label? (the {{n:ai.pilot_labels}} AI-read labels only)", "in label / not"),
        ("2 · Text", "D037", "Is the exact FAERS term (or its US spelling) in a safety section of "
                                               "the drug's reference label version?", "in label / not"),
        ("3 · Synonyms", "D043", "Does a reviewed synonym phrase for that term appear in the label?",
         "in label (high) / possibly in label (medium)"),
    ], widths=[1, 1, 3.5, 1.6])
    r.p("The code runs the checks in this order (`ontology_signals.py` l.163-176). The outcome is the same in any "
        "order; only the recorded match method (`label_match_method`) differs. First matches over all "
        "{{n:signals.ae_stats}} stats (Foundry, after D041 v2): AI {{n:signals.label_check_stats.ai_term_exact}}, "
        "text {{n:signals.label_check_stats.label_text}}, synonym high {{n:signals.label_check_stats.synonym_high}}, "
        "medium {{n:signals.label_check_stats.synonym_medium}}, none {{n:signals.label_check_stats.none}}.", style="small")
    r.p("**Why a reviewed synonym table and not MedDRA or an LLM judge (D043).** MedDRA (the standard medical "
        "terminology, whose groupings would solve most synonym cases) needs a licence we do not have for a public "
        "pilot. An LLM reading every label for every signal is costly, ungrounded unless it quotes, and would drift "
        "between model versions. A small table is cheap, deterministic, versioned and auditable. Synonym version "
        "{{n:synonyms.version}} has {{n:synonyms.rows}} rows: {{n:synonyms.high}} high, {{n:synonyms.medium}} medium "
        "and {{n:synonyms.rejected}} rejected (kept so they are not reviewed twice). The bands are Claude's draft; a "
        "pharmacist has not reviewed them [[ASSUMED]].")
    r.p("**Why buckets (D016).** Without MedDRA's groupings we tag reactions with keyword buckets. Only *clinical* "
        "reactions are ranked; efficacy complaints, product-use errors, abuse and overdose, pregnancy, social and "
        "legal terms, and administrative terms stay visible with their bucket but are not ranked.")
    r.h("How the ranked queue moved, on identical data")
    r.table(["Step", "Change", "Ranked signals", "Evidence"], [
        ("Step 9", "First full build: 13-drug formulary, exact text + AI", "{{n:signals.ranked_history.step9}}",
         "[[OBSERVED]]"),
        ("D043 syn_v1", "Synonym table v1 + US-spelling fix (" + syn1_drop + " fewer)",
         "{{n:signals.ranked_history.syn_v1}}", "[[OBSERVED]]"),
        ("D016 v3", "Wider efficacy and product-use buckets (tagged, not removed)", "{{n:signals.ranked_history.d016_v3}}",
         "[[OBSERVED]]"),
        ("D043 syn_v2", "Synonym table v2 (top-12-per-drug review)", "{{n:signals.ranked_history.syn_v2}}",
         "[[OBSERVED]]"),
    ], widths=[1.2, 3.4, 1.2, 0.9])
    r.p("Today: {{n:signals.total}} signals, {{n:signals.not_in_label}} not in label and "
        "{{n:signals.possibly_in_label}} possibly in label; {{n:signals.ranked}} ranked ('step' = a stage in our numbered "
        "build order). Bucket changes only re-tag, "
        "so signal keys and evaluation ids stay the same and saved triage decisions still match (learning 2026-11-05).")
    r.warning("The ranked queue is still a review queue. Each step removed known false positives (wording misses, "
              "efficacy complaints), but nobody has measured how many of the remaining signals a pharmacist would "
              "call real.")
    r.gate("Label check", [
        ("Required evidence", "Each step is versioned (`text+ai_v1+syn_v2`) and its effect measured on the same data."),
        ("Result", "Met; Foundry equals the local runner for every version (A014)."),
        ("If it fails", "A synonym row that hides a real gap would be a false negative: every row records the phrase, "
                        "label and section it matched, so it can be reviewed."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 06 AI and pipelines
    r.chapter("The AI step, incremental builds and the new pieces", new_page=False)
    r.h("D041 and D041 v2 · AI label extraction: cached and grounded")
    r.table(["Part", "Detail"], [
        ("Decision", "A Python transform calls Claude Sonnet 5.5 (through Foundry AIP) once per label safety section. "
                     "Each reaction comes with an exact quote, and code checks the quote is in the section text. "
                     "Results are cached by setid + version + section + text hash + prompt and model version."),
        ("Options", "AIP Logic function per label; Pipeline Builder's 'Use LLM' block; other models (GPT, Claude Opus)."),
        ("Why", "Per section keeps prompts short and failures local; the quote check catches invented text; the cache "
                "means an unchanged label never costs a second call (D005)."),
        ("v2 (6 Nov)", "Same model, prompt and cache; the AI also reads the 3 semaglutide reference labels (Ozempic "
                       "v20, Wegovy v19, oral Ozempic v14): {{n:ai.pilot_labels}} labels, {{n:ai.sections}} sections. "
                       "Trigger: evaluator v2 found the AI and the screen barely met; semaglutide is the demo drug "
                       "(A019)."),
        ("Evidence", "[[OBSERVED]] {{n:ai.grounded}} of {{n:ai.reactions}} quotes found word for word (5 labels). "
                     "The widening build made {{n:ai.d041_v2.model_calls}} model calls (new sections only); a forced "
                     "rebuild made {{n:ai.model_calls_on_rebuild}} (O1b). O1: a rebuild "
                     "went from {{n:optimization.O1.before_calls}} model calls and {{n:optimization.O1.before_tokens}} "
                     "tokens to {{n:optimization.O1.after_calls}} and {{n:optimization.O1.after_tokens}}. F1 "
                     "{{n:ai.gold_f1}} against the target of {{n:ai.d015_target_f1}} (D015), on a 35-item answer key "
                     "(Boxed Warning and Contraindications of the {{n:ai.v1_pilot.labels}} oxycodone labels, written by "
                     "Claude and frozen before the run, no pharmacist yet)."),
        ("Honest limits", "Only {{n:ai.pilot_labels}} labels and {{n:ai.sections}} sections. The answer key is "
                          "small (the AI found " + r.n("ai.gold_recall_strict").replace("/", " of ") + " answer-key items), "
                          "covers only oxycodone, and a pharmacist has not checked it; the semaglutide sections are "
                          "not scored. The AI does not change the signal list today: text matching already covers its "
                          "terms on all 5 labels (signals unchanged after v2). Its value is the exact quote, now on the "
                          "officer's screen (page 1), and an independent 'no optic-nerve term' reading for NAION."),
    ], widths=[1, 5.5])
    r.h("D044 · Incremental FAERS: built, proven equal, not switched on")
    r.p("The brief asks for at least one incremental pipeline. We built one that adds a quarter to a kept state "
        "with the same rules as the full rebuild. It produces exactly the same rows (EXCEPT ALL both ways = 0). "
        "But at two quarters it is **slower**: {{n:optimization.O2.incremental_add_q2_s}} s against "
        "{{n:optimization.O2.full_rebuild_s}} s for a full rebuild (" + o2_ratio + " times) [[OBSERVED]]. Reading and "
        "rewriting the state costs more than parsing one quarter. So the full rebuild stays the input to signals "
        "until the incremental path is measured faster, probably at four or more quarters [[ASSUMED]].")
    r.figure(D + "33-handin-incremental-faers-v3.png",
             "Full and incremental FAERS side by side: state and log, replay when identity changes, EXCEPT ALL = 0.",
             source=D + "33-handin-incremental-faers-v3.png", max_height=235)
    r.h("D047 · Reuse DailyMed XML that has not changed")
    r.p("The slowest build re-downloaded every label XML. Reusing XML for an unchanged setid and version cut "
        "downloads from {{n:optimization.O3.before_downloads}} to {{n:optimization.O3.after_downloads}} and the build "
        "from " + o3_before + " to " + o3_after + " (" + o3_cut + " less), with the same rows. The index (about 30 "
        "pages) is still pulled every build, so a new label version still arrives the same day [[OBSERVED]]. Caveat: "
        "the 'before' time comes from the step 9 build of the same scope, not a back-to-back run (O3).")
    r.h("D045 · A change feed for 'what changed'")
    r.p("'Since yesterday' means 'since my last review', because sources update on different clocks (DQ14). Many "
        "changes are already dated by the source (a recall's report date, a label's effective date); the rest are "
        "found by comparing this build with the last. The first build gave {{n:changes.events_first_build}} events; "
        "a rebuild on unchanged data added {{n:changes.snapshot_diff_after_rebuild}} [[OBSERVED]]. The Morning brief "
        "card counts the last 30 days ({{n:changes.last_30_days}}); page 3's date range is how the officer narrows "
        "it to 'since my last review'.")
    r.figure(D + "34-handin-change-feed-v1.png",
             "Change feed: source-dated events and build-to-build differences flow into MSSM Change Event and page 3.",
             source=D + "34-handin-change-feed-v1.png", max_height=260)
    r.h("D046 · Monitoring as data")
    r.p("Every build appends {{n:monitoring.checks_per_build}} checks (keys, row-count drops, freshness, AI grounded "
        "rate, cache hits, field fill rates) to a dataset, and rebuilds a drift view as a **historical replay** from "
        "source dates, labelled as such. {{n:monitoring.data_health_checks}} Foundry Data Health checks alert the "
        "owner. The first run found two real shifts: FAERS reports with no reporter type rose from "
        "{{n:monitoring.reporter_type_blank_q1|.0%}} to {{n:monitoring.reporter_type_blank_q2|.0%}} between quarters "
        "(DQ38), and recalls for our drugs in the last four weeks were {{n:monitoring.recalls_last4w}} against "
        "{{n:monitoring.recalls_prev4w}} before [[OBSERVED]].")
    r.h("D048 · No partitioning in the pilot")
    r.p("Every dataset is written unpartitioned. The largest table has {{n:faers.case_reactions}} rows, and most "
        "build time is most likely container start-up (not measured separately), not data. We revisit (FAERS by quarter, signals by drug) when FAERS "
        "holds 8 or more quarters or a single build passes 5 minutes (D048) [[DESIGNED]].")
    r.gate("AI and pipelines", [
        ("Required evidence", "Every optimization claim has a before and after number, including the ones that failed."),
        ("Result", "Met: O1 and O3 helped; O2 (incremental) and O3a (column pruning) did not, and both are logged."),
        ("If it fails", "If incremental is switched on without a new measurement, the claim is unproven: re-measure first."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 07 changes over time
    r.chapter("How decisions changed over time", new_page=False)
    r.p("**Most changes were triggered by the data, not by opinion. Each row below is a decision that got a new "
        "version, with what triggered it.**")
    r.table(["Decision", "Before", "After", "Trigger (evidence)"], [
        ("D002 → D007 → D014 class", "GLP-1 only, then opioids only", "{{n:scope.opioids}} opioids + {{n:scope.glp1}} GLP-1",
         "Project sponsor's suggestion, then research scoring the hybrid higher (A003)"),
        ("D003 → D027 identity", "One key: ingredient", "Ingredient → product → package",
         "Labels and recalls belong to products (DQ33)"),
        ("D004 v1 → v2 (D022)", "Incremental = append each quarter", "Upsert latest version + deletes on all history",
         "Phantom rows from appending (DQ36)"),
        ("D016 v1 → v2", "Tag abuse, product use, pregnancy, lawyer-filed", "Add social/legal, efficacy, administrative",
         "First ranked list led by child neglect, homicide, imprisonment (A012)"),
        ("D016 v2 → v3", "GLP-1 efficacy and 'Product ...' complaints ranked", "Wider efficacy and product-use buckets",
         "GLP-1 lists topped by hunger and 'weight loss poor' (A013); ranked {{n:signals.ranked_history.syn_v1}} → "
         "{{n:signals.ranked_history.d016_v3}}"),
        ("D023 v1 → v2", "Fold same-person duplicates", "Also set aside reports with 30+ drugs",
         "Mass-polypharmacy cluster the person key missed (A012)"),
        ("D031 v1 → v5 schedule and scope", "Demo date, cut list, 11 drugs", "No fixed date; 13-drug formulary restored",
         "The schedule slipped a week and the fixed date was dropped; the one-drug slice passed build steps 6 to 8, "
         "so gate D039 G1 restored all 13 drugs"),
        ("D043 data syn_v1 → syn_v2", "Synonym table v1", "{{n:synonyms.rows}} rows",
         "Top-12-per-drug review; ranked {{n:signals.ranked_history.d016_v3}} → {{n:signals.ranked_history.syn_v2}}"),
        ("D028 → D045", "'Since last review' as an idea (D028)", "A built change feed (D045)",
         "Step 11 build (A016)"),
        ("D041 → D041 v2", "AI reads 2 oxycodone labels; 0 for the demo drug", "Also the 3 semaglutide labels; page-1 "
         "table of AI quotes", "Evaluator v2: the AI and the screen barely met (A019); owner, 6 Nov"),
        ("12 decisions Proposed → Accepted", "Built and measured, awaiting the owner", "Accepted as built (D015: "
         "the target only)", "Owner's batch decision, 6 Nov 2026"),
    ], widths=[1.6, 1.7, 1.8, 2.5])
    r.note("D031 (schedule) went through five versions: a demo date, a re-ordered cut list tied to hours, a "
           "one-week slip that forced all cuts, 'no fixed date', and finally the full {{n:scope.drugs_formulary}}-drug "
           "formulary restored. The cuts that stayed are in chapter 8.")
    r.gate("Change history", [
        ("Required evidence", "Every changed decision has a dated row with before, after and trigger."),
        ("Result", "Met in the *Decision changes* table of DECISIONS.md; each change also bumped the Compass version."),
        ("If it fails", "A decision edited in place loses its history: restore it from git and add a version row."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 08 not done
    r.chapter("What we chose not to do")
    r.p("**A partial build with clear reasoning beats a complete one you cannot explain (the brief). These are "
        "the things we left out on purpose, and what would change our mind.**")
    r.table(["Not done", "Why", "What it costs us", "What would change our mind"], [
        ("MedDRA (licensed medical terminology)", "Licence not available for a public pilot", "Keyword buckets and a "
                                                                                              "synonym table instead",
         "A licence: replace buckets with MedDRA groupings"),
        ("Patient-level or private data", "Brief: public data only; no PHI", "No outcome data, only reports",
         "Never in this project"),
        ("An LLM judging each signal", "Cost; ungrounded unless it quotes; drifts with model versions (D043)",
         "Synonyms need human review", "AI proposes synonym rows, a pharmacist accepts them"),
        ("Live drift alerts", "Drift needs 3 to 4 weeks of builds (D009); we had days", "Drift is a historical replay, "
                                                                                       "labelled as one", "Scheduled builds for a month"),
        ("Scheduled builds", "Pilot built by hand, step by step", "Freshness checks do not fire on their own",
         "Production hand-over"),
        ("AI on all labels", "Answer key not reviewed by a pharmacist (D031 v5)", "Only {{n:ai.pilot_labels}} labels "
                                                                                  "(oxycodone, semaglutide) have AI quotes",
         "A reviewed gold set on long sections"),
        ("ClinicalTrials.gov, OnSIDES (open label side-effect data, CC BY 4.0)", "D031 cut list (v3 cuts, kept by v5): breadth after "
         "depth", "No 'seen in trials' or second 'is it labelled?' opinion", "Another month (roadmap)"),
        ("Daily FAERS", "No confirmed official daily API (D029). FAERS moved to AEMS (the FDA's new adverse event "
                        "system) in March 2026 (DQ20); the future feed is unverified", "FAERS is quarterly, about "
         "{{n:monitoring.faers_age_days}} days behind", "An official AEMS export"),
        ("SrLC (FDA Safety-related Labeling Changes) backtest", "D031 cut list (v3 cuts, kept by v5)",
         "Cannot show 'we would have flagged it first'", "Another month"),
        ("Medicare Part D prescribing data, PubMed, other countries' data, shortages", "Parked in A005: re-weighting, a second AI problem, a second "
                                                            "identity system, outside the three questions",
         "Narrower evidence", "A user need that one of them answers"),
        ("Signals from the incremental FAERS path", "Slower at two quarters (O2)", "Full rebuild each time",
         "A faster measurement at 4+ quarters"),
        ("Spark for the clean layer", "Polars on one machine is enough at this size", "Not tested at scale",
         "Data that outgrows one machine"),
    ], widths=[1.6, 2, 1.7, 1.8])
    r.how_we_know("Each row traces to a decision or cut: D009, D029, D031 v3 to v5 (v3 superseded; its cuts kept by v5), D043, A005 and the optimization "
                  "log. The 'another month' plan (`docs/09-roadmap/another-month-sources-and-pharmacist-review.md`) "
                  "puts a named pharmacist reviewer first, ahead of any new source.")
    r.gate("Scope discipline", [
        ("Required evidence", "Every exclusion has a reason and a condition for revisiting it."),
        ("Result", "Met for the twelve exclusions above."),
        ("If it fails", "An exclusion with no reason looks like something we forgot."),
    ])

    # ------------------------------------------------------------------ 09 replaced approaches
    r.chapter("Approaches we replaced or reverted", new_page=False)
    r.p("**Every approach we try gets a file, including the ones that did not last. An honest note first: no "
        "approach file is marked 'Dropped' in the index today. The approaches below were replaced, reverted or "
        "never adopted, and their files are kept.**")
    r.table(["What we tried", "What happened", "Replaced by", "Where"], [
        ("Opioids-only pilot class", "Research scored a hybrid class higher", "{{n:scope.opioids}} opioids + {{n:scope.glp1}} GLP-1",
         "A001 → A003, D014"),
        ("v1 reference pack (30 cases, one source each)", "Questions and answers written in one pass; capture errors",
         "Reference set v2: frozen questions, independent verifier", "A008, D037"),
        ("Six-day build proposal", "Not adopted; its ids (A006, D032 to D035) are reserved", "12-step build order",
         "A007, D036"),
        ("One-page screen (question 1 only)", "Did not answer recalls or changes", "Four-page module",
         "A012 → A016"),
        ("Exact-term label matching alone", "Synonym misses topped the GLP-1 lists", "Three-step label check",
         "A013 → A014, D043"),
        ("Person-key duplicate fold alone", "Missed one patient re-filed with changing ages", "D023 v2 mass-report cut",
         "A012"),
        ("Incremental FAERS as the signals input (O2)", "Correct but slower", "Full rebuild stays the input", "A015, D044"),
        ("Column pruning in FAERS parsing (O3a)", "Faster parse, no visible gain overall; reverted",
         "Nothing (not the bottleneck)", "Optimization log"),
        ("A separate monitoring design (an unnumbered 'A00x' placeholder row in the index)", "Parked as 'later'",
         "A017 monitoring", "INDEX.md"),
    ], widths=[2, 2.2, 1.8, 1.2])
    r.how_we_know("O2 and O3a are in the optimization log with their numbers, under 'Helped? No'. Keeping them is the "
                  "point: the brief asks for what did not help, and a reviewer can check that each claim of 'faster' "
                  "is backed by a measurement.")
    r.gate("Record of what did not work", [
        ("Required evidence", "Replaced approaches keep their files, with the reason they were replaced."),
        ("Result", "Met. Gap: the index uses 'Kept', 'Trying' and 'Replaces' instead of a 'Dropped' status, so the "
                   "replaced approaches are spread across rows; a cleanup would mark A001 and the v1 pack as Dropped."),
        ("If it fails", "If a dropped idea comes back without its history, we repeat the mistake."),
    ], status="TESTED")

    r.chapter("Reference", label="A")
    r.h("Evidence and status labels")
    r.pill_legend()
    r.h("Figures quoted from project records (not in numbers.json)")
    r.p("These come from project records, not from the baseline-gate capture. Each is also cited where it appears.",
        style="small")
    r.table(["Figure", "Source"], [
        ("Morphine substring match about +50% rows", "DQ34 (2026Q2 file, profiled 2026-10-20)"),
        ("Primary-suspect-only drops more than half of oxycodone cases", "DECISIONS learnings, 2026-11-04"),
        ("Mass reports: 30 or more drugs per report; share 0.5 or more is not ranked", "D023 v2"),
        ("Foundry counts equal the 20 October prototype; five signals re-counted by hand", "Learning 2026-11-04; "
                                                                                          "baseline-gate.md"),
        ("Ozempic label: openFDA copy months behind DailyMed", "DQ28"),
        ("F1 answer key: 35 items, Boxed Warning + Contraindications of 2 labels", "eval/ai-eval-v1.md"),
        ("DailyMed index about 30 pages per build; 'before' from the step 9 build", "Optimization log O3"),
        ("Drift needs a 3 to 4 week window", "D009"),
        ("Partitioning trigger: 8+ FAERS quarters or a build over 5 minutes", "D048"),
        ("Batch acceptance of 12 decisions; D041 v2 accepted (6 Nov 2026)", "DECISIONS.md, decision changes"),
        ("AI found diabetic-retinopathy terms, no optic-nerve term (semaglutide)", "A019; eval/ai-eval-v1.md"),
        ("FAERS replaced by AEMS on 11 March 2026", "DQ20"),
        ("Hybrid class scored higher than opioids only", "D014; A003"),
    ], widths=[300, 204])
    r.numbers_appendix()
