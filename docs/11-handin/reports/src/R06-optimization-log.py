"""R06 Optimization log: what we measured, what we changed, what helped and what did not.

Build:  .venv/bin/python tools/handin/build_report.py R06-optimization-log
Output: docs/11-handin/reports/pdf/R06-optimization-log.pdf

Sources: docs/08-optimization-log/optimization-log.md (O1, O1b, O2, O3, O3a), A011, A015, A017, A019, D041 (v2), D044, D047,
eval/ai-eval-v1.md, docs/04-architecture/foundry-conventions/project-build-order-v1.md.
Every number is a {{n:...}} lookup in docs/11-handin/numbers.json, or computed here from two lookups
(marked DERIVED in the text).
"""

META = {
    "id": "R06",
    "title": "Optimization log",
    "short": "Optimization log",
    "subtitle": "measure, change, measure again, and say what did not help",
    "version": "1.2",
    "date": "6 November 2026",
}


def _mmss(s):
    """203 -> '3 m 23 s' (DERIVED display of a seconds value from numbers.json)."""
    s = int(s)
    return f"{s // 60} m {s % 60:02d} s" if s >= 60 else f"{s} s"


def build(r):
    o2_full, o2_inc = r.n("optimization.O2.full_rebuild_s"), r.n("optimization.O2.incremental_add_q2_s")
    o2_ratio = o2_inc / o2_full
    o3_before, o3_after = r.n("optimization.O3.before_s"), r.n("optimization.O3.after_s")
    o3_cut = (o3_before - o3_after) / o3_before
    o3_dl_b, o3_dl_a = r.n("optimization.O3.before_downloads"), r.n("optimization.O3.after_downloads")
    o3_dl_cut = (o3_dl_b - o3_dl_a) / o3_dl_b
    demo_all = r.n("faers.q1_cases") + r.n("faers.q2_demo_rows")
    q2_share = r.n("faers.q2_demo_rows") / demo_all
    o1_tokens = r.n("ai.run1_tokens_prompt") + r.n("ai.run1_tokens_completion")
    assert o1_tokens == r.n("optimization.O1.before_tokens")  # the two keys must agree

    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "The brief asks us to pick at least one pipeline, measure it, improve it, and show before and "
               "after (build time, compute, or the cost of the LLM step), and to say what we tried that did not "
               "help. What did we measure, and what happened?"),
              ("One-line answer",
               "Two changes helped: the AI cache (model calls {{n:optimization.O1.before_calls}} to "
               "{{n:optimization.O1.after_calls}} on a rebuild) and DailyMed XML reuse "
               f"({_mmss(o3_before)} to {_mmss(o3_after)}). Two did not: incremental FAERS was correct but "
               f"{o2_ratio:.2f} times slower, and column pruning made no real difference.")],
        is_=["The optimization log the brief asks for (hand-in item 3), written out in full",
             "Four entries, O1 to O3a (O1 re-checked as O1b after D041 v2), each with baseline, change, after, method and threats to validity",
             "The deliberate choices behind them: incremental or full rebuild, partitioning, where the LLM step sits"],
        is_not=["A claim that the pilot is fast or cheap at production scale",
                "A cost report in dollars: we measured tokens and seconds, not invoices",
                "A record of compute-seconds: Foundry build times are wall-clock times"],
        how_to_read="Chapter 1 is the one-page answer. Chapter 2 says how we measured and what can make a "
                    "measurement wrong. Chapters 3 to 6 are one entry each. Chapter 7 is the design choices the "
                    "judges look for. Chapter 8 says what we would measure next. Numbers from `numbers.json` "
                    "are listed in the table at the end. Figures from other project records cite that record "
                    "where they appear and are listed in *Figures quoted from project records*.",
    )

    # ------------------------------------------------------------------ 1 summary
    r.chapter("Summary in plain language")
    r.p("This project runs on **Palantir Foundry**, a data platform where data pipelines, a data model and "
        "apps live together. A **dataset** is a table stored in Foundry. A **transform** is a piece of Python "
        "code that reads datasets and writes a new one; running it is a **build**. A transform can be "
        "**incremental**: it remembers what it wrote last time and only does the new work. **AIP** is "
        "Foundry's way of calling a large language model (an **LLM**, here Claude) from a pipeline.")
    r.p("We tried four optimizations on three pipelines. The sources are FAERS (the FDA's database of "
        "adverse event reports, published as quarterly files) and DailyMed (the official drug labels, as "
        "SPL XML, a structured label format). The pilot covers {{n:scope.drugs_formulary}} drugs: "
        "{{n:scope.opioids}} opioids (oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, "
        "buprenorphine, tramadol) and {{n:scope.glp1}} GLP-1 drugs (semaglutide, liraglutide, dulaglutide, "
        "tirzepatide, exenatide).")
    r.p("Each claim carries a label. Evidence labels say what kind of claim it is; status labels say how far "
        "the work has got:", style="small")
    r.pill_legend()
    r.table(["#", "Pipeline", "Before", "After", "Helped?", "Evidence"], [
        ("O1", "AI label extraction (LLM step)",
         "{{n:optimization.O1.before_calls}} model calls, {{n:optimization.O1.before_tokens}} tokens",
         "{{n:optimization.O1.after_calls}} calls, {{n:optimization.O1.after_tokens}} tokens on rebuild",
         "**Yes**", "[[OBSERVED]]"),
        ("O1b", "Same cache after D041 v2 ({{n:ai.pilot_labels}} labels)",
         "Without a cache: all {{n:ai.sections}} sections re-sent each build",
         "Widening build {{n:ai.d041_v2.model_calls}} calls (new sections only); forced rebuild "
         "{{n:ai.model_calls_on_rebuild}} calls", "**Yes**", "[[OBSERVED]]"),
        ("O2", "FAERS clean: incremental by quarter",
         "Full rebuild {{n:optimization.O2.full_rebuild_s}} s",
         "Incremental {{n:optimization.O2.incremental_add_q2_s}} s (same rows)",
         "**No**", "[[OBSERVED]]"),
        ("O3", "DailyMed raw pull: reuse XML",
         f"{_mmss(o3_before)}, {{{{n:optimization.O3.before_downloads}}}} downloads",
         f"{_mmss(o3_after)}, {{{{n:optimization.O3.after_downloads}}}} downloads",
         "**Yes**", "[[OBSERVED]]"),
        ("O3a", "FAERS clean: parse fewer columns",
         "Local run {{n:optimization.O3a.local_run_before_s}} s",
         "Local run {{n:optimization.O3a.local_run_after_s}} s",
         "**No** (reverted)", "[[OBSERVED]] locally"),
    ], widths=[32, 106, 104, 110, 58, 74])
    r.key(["**What helped:** not doing work twice. The LLM is not called again for a label section it has "
           "already read (O1), and a label XML is not downloaded again if we already hold that exact "
           "version (O3).",
           f"**What did not:** incremental FAERS is correct row for row but {o2_ratio:.2f} times slower at two "
           "quarters (O2), and parsing fewer columns saved a fraction of a second (O3a). Both are kept in "
           "the log on purpose."], title="The short version")
    r.callout("note", [
        "**Faster builds do not make her flags fresher.** Signals change only when a new FAERS quarter "
        "arrives, and FAERS is about {{n:monitoring.faers_age_days}} days behind (monitoring `faers_age_days`). "
        "FAERS was replaced by AEMS (the FDA's new adverse event system) in March 2026, so how the future "
        "feed will arrive is unverified (DQ20).",
        "**A new label still reaches her the same day.** XML reuse (O3) keeps pulling the DailyMed index "
        "every build, so a new label version is fetched as soon as it is listed.",
        "**The AI cache (O1, O1b) costs her nothing and hides nothing.** The AI's exact quotes are on her "
        "page 1 since 6 Nov, and a label refresh with the same text costs no model call. The AI does not "
        "change her signal list (report R08).",
        "**Only the project owner can submit a triage decision today.** Giving the officer that permission "
        "is a production step (report R04).",
    ], title="What this means for Dana (the safety officer)")
    r.gate("Brief requirement met", [
        ("Required evidence", "At least one pipeline measured, improved, with before and after; failures shown."),
        ("Result", "Met twice (O1 LLM cost, re-checked as O1b at 2.3 times the size; O3 build time). Two "
                   "non-gains reported with their reasons (O2, O3a)."),
        ("If it fails", "Re-run O3 back-to-back before quoting it as the headline number (chapter 5)."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 2 method
    r.chapter("How we measured")
    r.p("Our rule, taken from the brief's judging notes: **measured, not asserted**. Every entry has a "
        "baseline, one change, and an after number taken the same way.")
    r.table(["What", "How we read it", "Used for"], [
        ("Build time", "Duration on the Foundry **Builds** page (wall-clock time of the job)", "O2, O3"),
        ("Model calls and tokens", "Columns written by the AI transform: `from_cache`, `called_at`, "
         "`prompt_tokens`, `completion_tokens` in `ai_label_section_extractions`", "O1"),
        ("Same output", "Foundry SQL: row counts, and `EXCEPT ALL` in **both** directions (rows in A not "
         "in B, and B not in A); both must return 0", "O2"),
        ("Same output (local)", "Sorted row hashes from the local runner, a copy of each transform that "
         "runs on a laptop and equals Foundry (A014)", "O3a"),
        ("Download count", "Label rows fetched in the build vs rows carried over from the previous output", "O3"),
    ], widths=[90, 300, 60])
    r.h("Threats to validity that apply to every entry")
    r.table(["Threat", "What it means here", "Effect"], [
        ("One run each", "Each before and after is a single build. We did not repeat builds to get a spread.",
         "Small differences (a few seconds) are noise. Only large gaps are claimed."),
        ("Foundry start-up overhead", "Every Foundry build spends time starting before the code runs. "
         "We did not measure it separately.", "Hurts any design with more builds (O2 pays it twice)."),
        ("Wall-clock, not compute", "The Builds page shows elapsed time, not compute-seconds (machine time "
         "used). We did not capture compute-seconds.", "We cannot state a compute or money saving."),
        ("Pilot size", "Two FAERS quarters, {{n:scope.drugs_formulary}} drugs, "
         "{{n:labels.total}} labels, {{n:ai.pilot_labels}} labels read by the AI ({{n:ai.sections}} sections).",
         "Results may change at scale; chapter 8 says what to re-measure."),
    ], widths=[95, 245, 140])
    r.gate("Method written down", [
        ("Required evidence", "Each number has a named place it was read from."),
        ("Result", "Met. Compute-seconds and repeated runs are **not measured** and are said so."),
        ("If it fails", "Treat the number as a guess and leave it out of the demo."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 3 O1
    r.chapter("O1 · The AI cache")
    r.status("TESTED", "Helped. A rebuild with unchanged label text made "
             "{{n:optimization.O1.after_calls}} model calls (was {{n:optimization.O1.before_calls}}).")
    r.p("**The pipeline.** The AI transform sends each safety section of a drug label to Claude Sonnet "
        "(through AIP) and gets back every reaction it names, each with an exact quote (decision D041). O1 was "
        "measured on the first pilot: {{n:ai.v1_pilot.labels}} oxycodone labels, {{n:ai.v1_pilot.sections}} "
        "sections. Since D041 v2 it reads {{n:ai.pilot_labels}} labels, {{n:ai.sections}} sections (O1b below). "
        "Calling an LLM costs tokens "
        "(pieces of text the model reads and writes) and time, so doing it twice for the same text is pure waste.")
    r.table(["", "Value", "Evidence"], [
        ("**Baseline** (run 1)", f"{{{{n:optimization.O1.before_calls}}}} model calls; "
         "{{n:ai.run1_tokens_prompt}} prompt + {{n:ai.run1_tokens_completion}} completion = "
         "{{n:optimization.O1.before_tokens}} tokens", "[[OBSERVED]]"),
        ("**Change**", "A cache. Each section gets a **cache key**: label setid + version + section + a hash "
         "of the section text + parser, prompt and model version (D005, D041). Before calling the model, "
         "the transform looks the key up in its own previous output (an incremental transform).", "[[DESIGNED]]"),
        ("**After** (rebuild after an upstream refresh, same text)",
         "{{n:optimization.O1.after_calls}} model calls, {{n:optimization.O1.after_tokens}} tokens; "
         "all {{n:ai.v1_pilot.sections}} sections served from cache; same output rows",
         "[[OBSERVED]]"),
        ("**O1b** (6 Nov, D041 v2: add {{n:ai.d041_v2.semaglutide_labels}} semaglutide labels)",
         "Widening build: {{n:ai.d041_v2.model_calls}} model calls, only the new sections "
         "({{n:ai.d041_v2.new_prompt_tokens}} prompt + {{n:ai.d041_v2.new_completion_tokens}} completion tokens); "
         "{{n:ai.d041_v2.cached_sections_in_that_build}} old sections reused. Forced rebuild with unchanged "
         "text: {{n:ai.model_calls_on_rebuild}} calls, {{n:ai.from_cache_on_rebuild}} of {{n:ai.sections}} "
         "sections from cache", "[[OBSERVED]]"),
        ("**Method**", "`from_cache` = true and `called_at` unchanged on every section row after the "
         "rebuild", "[[OBSERVED]]"),
    ], widths=[120, 300, 64])
    r.h("Threats to validity")
    r.bullets([
        "The job's wall time was **not** compared like for like, so we claim calls and tokens saved, not "
        "seconds saved.",
        "Cost is in tokens, not dollars. We did not record the AIP price per token, so a money figure is "
        "**not measured**.",
        "Run 1 used prompt p1. The current prompt p2 was a fresh run; it used about 55% more output tokens "
        "(A011 run 2; decision-log learning 2026-11-04). The exact p2 count is not in `numbers.json`. The "
        "cache behaviour is the same for both.",
    ])
    r.how_we_know(["The cache key includes the prompt and model version. When we moved from prompt p1 to "
                   "p2, the key changed and all sections were extracted again (A011, run 2). So the cache "
                   "saves calls when nothing changed, and does **not** hide a change that should be re-scored.",
                   "O1b needed a **forced** build: the repository Build button and the dataset Build button both "
                   "skipped the unchanged AI dataset as 'already up to date' (DECISIONS learning 2026-11-06). "
                   "Build ▾ → Force ran it, and every section came from the cache."],
                  title="How we know the cache is safe, not just cheap")
    r.gate("O1 closed", [
        ("Required evidence", "Model calls and tokens before and after, same output."),
        ("Result", "Met: {{n:optimization.O1.before_tokens}} tokens to {{n:optimization.O1.after_tokens}} on "
                   "rebuild; O1b confirms it at {{n:ai.sections}} sections."),
        ("Measure next", "Job wall time, back-to-back; dollars per label before widening the AI to other drugs."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 4 O2
    r.chapter("O2 · Incremental FAERS")
    r.status("TESTED", f"Did not help at two quarters: {o2_inc} s incremental vs {o2_full} s full rebuild "
             f"({o2_ratio:.2f} times slower). Outputs identical.")
    r.p("**The pipeline.** `clean_faers` turns FAERS quarter files into three clean tables: current cases, "
        "case reactions, and drug-reaction rows for our drugs. FAERS sends follow-up versions of a case in "
        "later quarters and also deletes cases, so a new quarter can change old rows (decision D022).")
    r.table(["", "Value", "Evidence"], [
        ("**Baseline**", f"Full rebuild reads both quarters ({demo_all:,} DEMO rows, the case file, plus "
         "their drug and reaction files): **{{n:optimization.O2.full_rebuild_s}} s**. DEMO rows count every "
         "case version; after rule D022 keeps one version per case and applies deletes, "
         "{{n:faers.cases_current}} current cases remain", "[[OBSERVED]] [[DERIVED]]"),
        ("**Change**", "Incremental by quarter (A015, D044): read only the new quarter, merge it into a kept "
         "**state** with the D022 rule (highest case version wins, then the quarter's deletes), log each "
         "quarter, then rebuild the three outputs from the state", "[[DESIGNED]]"),
        ("**After** (adding Q2)", f"Reads one quarter ({{{{n:faers.q2_demo_rows}}}} DEMO rows, {q2_share:.0%}) "
         "plus the state: **{{n:optimization.O2.incremental_add_q2_s}} s** = state step "
         "{{n:optimization.O2.state_s}} s + outputs step {{n:optimization.O2.outputs_s}} s", "[[OBSERVED]]"),
        ("**Correct?**", "Yes. {{n:faers.cases_current}} cases, {{n:faers.case_reactions}} reactions, "
         "{{n:faers.drug_reaction_rows}} drug-reaction rows in both; `EXCEPT ALL` both ways = 0. Q2 replaced "
         "{{n:faers.q2_cases_replaced}} Q1 cases and deleted {{n:faers.q2_cases_deleted}}", "[[OBSERVED]]"),
        ("**Method**", "Foundry Builds page durations; Foundry SQL for equality", "[[OBSERVED]]"),
    ], widths=[80, 340, 64])
    r.h("Why it was slower")
    r.p("The saving is one quarter of file parsing. The cost is fixed: read back the saved state, write the "
        "three state datasets and the quarter log again, and run a **second** build for the outputs. Each Foundry build also pays its "
        "start-up time, and the incremental path pays it twice. At two quarters the fixed cost is bigger than "
        "the saving.")
    r.h("When it would win")
    r.p("Adding one quarter out of N saves roughly (N - 1)/N of the file reading. FAERS has many years of "
        "quarters, so with a long history the saving grows and the fixed cost does not. We expect the trade "
        "to turn over somewhere past a handful of quarters [[ASSUMED]]; the crossover point is **not measured**.")
    r.bullets(["Re-measure with 4 or more quarters before switching signals to the incremental outputs (D044).",
               "Cut the fixed cost (not tried): write the outputs in the same build as the state (one start-up), "
               "and keep the state as one table instead of three."])
    r.figure("docs/diagrams/png/33-handin-incremental-faers-v3.png",
             "Full vs incremental FAERS (top) and DailyMed XML reuse (bottom), with the measured results.",
             source="docs/diagrams/png/33-handin-incremental-faers-v3.png (source: docs/diagrams/src/33-handin-incremental-faers-v3.mmd)")
    r.gate("O2 closed", [
        ("Required evidence", "Same rows both ways; build time for both paths."),
        ("Result", f"Correct, not faster ({o2_ratio:.2f} times slower). Signals stay on the full rebuild (D044)."),
        ("Measure next", "4+ quarters; one-build variant; start-up time on its own."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 5 O3
    r.chapter("O3 · DailyMed XML reuse")
    r.status("TESTED", f"Helped: {_mmss(o3_before)} to {_mmss(o3_after)} ({o3_cut:.0%} less build time), "
             "{{n:optimization.O3.before_downloads}} to {{n:optimization.O3.after_downloads}} downloads.")
    r.p("**The pipeline.** `raw_dailymed_spl` first pulls the DailyMed index (which label versions exist for "
        "our drugs), then downloads each label's XML. Before this change it downloaded all "
        "{{n:labels.total}} XML files on every build, even though almost none had changed. This was our "
        "slowest build. Decision D047 records the change; the owner accepted it on 6 November 2026.")
    r.table(["", "Value", "Evidence"], [
        ("**Baseline**", f"Full pull every build: {{{{n:optimization.O3.before_downloads}}}} XML downloads, "
         f"**{_mmss(o3_before)}** ({{{{n:optimization.O3.before_s}}}} s)", "[[OBSERVED]]"),
        ("**Change**", "Read the previous output; if the same setid + version is already held as XML, reuse it. "
         "Download only new versions and earlier replies that were not XML. The index (about 30 pages, O3) is still pulled every "
         "build, and both outputs are still replaced as a full snapshot", "[[DESIGNED]]"),
        ("**After**", f"{{{{n:optimization.O3.after_downloads}}}} downloads, {{{{n:optimization.O3.reused}}}} "
         f"reused; **{_mmss(o3_after)}** ({{{{n:optimization.O3.after_s}}}} s); same "
         "{{n:labels.total}} rows", "[[OBSERVED]]"),
        ("**Reduction**", f"Build time {o3_cut:.0%} lower; downloads {o3_dl_cut:.1%} lower", "[[DERIVED]]"),
        ("**Method**", "Foundry Builds page; reused vs fetched rows in the output", "[[OBSERVED]]"),
    ], widths=[80, 340, 64])
    r.p("The {{n:optimization.O3.after_downloads}} remaining downloads are the two labels where DailyMed "
        "answers \"HTTP 200\" with the text \"None\" instead of XML (data issue DQ42). They are re-tried on "
        "purpose, in case DailyMed fixes them.")
    r.h("Side benefits")
    r.bullets(["**Fewer HTTP 429 replies** (\"too many requests\"). We saw a burst of them in a local run; "
               "fewer calls means less chance of hitting the limit. The pull also retries 429 with back-off.",
               "**Freshness unchanged.** Because the index is pulled every build, a new label version is still "
               "fetched the same day."])
    r.h("Threats to validity")
    r.warning(["**The baseline is from an earlier build** (the step 9 build, same scope), not run back-to-back "
               "with the after build. Platform load on that day may differ.",
               "One run each, wall-clock only. The gap (two minutes) is large enough that we believe the "
               "direction, but the exact percentage should be re-measured."])
    r.gate("O3 closed", [
        ("Required evidence", "Build time and download count before and after, same rows."),
        ("Result", f"Met: {_mmss(o3_before)} to {_mmss(o3_after)}; {{{{n:optimization.O3.reused}}}} labels reused."),
        ("Measure next", "Back-to-back runs (with and without reuse); count of 429 replies per build."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 6 O3a
    r.chapter("O3a · Column pruning")
    r.status("TESTED", "No real gain. Reverted.")
    r.table(["", "Value", "Evidence"], [
        ("**Baseline**", "The FAERS clean step parses every column of the case, drug and reaction files, then "
         "keeps the few it needs. Whole local run {{n:optimization.O3a.local_run_before_s}} s", "[[OBSERVED]]"),
        ("**Change**", "Parse only the needed columns (`read_csv(columns=...)`)", "[[DESIGNED]]"),
        ("**After**", "The drug-file parse itself got faster, but the whole local run took "
         "{{n:optimization.O3a.local_run_after_s}} s; outputs identical (sorted row hashes)", "[[OBSERVED]]"),
        ("**Method**", "Local runner timings (not Foundry); the baseline is a range over runs", "[[OBSERVED]]"),
    ], widths=[80, 340, 64])
    r.p("**Why it did not help:** parsing is not the bottleneck. Where the time does go was not profiled. "
        "We reverted it so the Foundry code and the local runner stay identical, which matters "
        "more for trust than a fraction of a second.")
    r.p("**Threat to validity:** measured on a laptop, not in Foundry. We did not try it in Foundry because the "
        "local gain was already within noise.", style="small")
    r.gate("O3a closed", [
        ("Required evidence", "Before and after timing, same output."),
        ("Result", "Measured, no gain, reverted. Kept in the log as \"what did not help\"."),
        ("Measure next", "Nothing; profile where the FAERS build really spends its time first."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 7 choices
    r.chapter("Deliberate choices")
    r.p("The judges look for deliberate choices on incremental vs full rebuild, partitioning, and not "
        "re-running the LLM needlessly. Here is each one, with the reason.")
    r.h("Incremental or full rebuild, per pipeline")
    r.table(["Pipeline", "Mode", "Why"], [
        ("Most raw and clean steps (openFDA recalls, NDC, Drugs@FDA; labels; identity)",
         "Full rebuild", "Small (about {{n:raw.openfda_requests_approx}} openFDA requests). Full is simple and "
         "always correct."),
        ("FAERS clean, used by signals", "Full rebuild",
         f"Faster at two quarters ({o2_full} s vs {o2_inc} s, O2). Correct by construction."),
        ("FAERS clean, incremental path", "Incremental, beside the full one",
         "Proven equal (O2). Switch only when it is measured faster (D044). Replays all quarters if drug "
         "identity changes, because old drug matches may then be wrong."),
        ("DailyMed raw pull", "Full snapshot, reusing held XML",
         "Fast (O3) but keeps the full-snapshot contract: every build lists every label version (D047)."),
        ("AI label extraction", "Incremental (cache)", "The expensive step. Never re-call for the same text (O1)."),
        ("Change feed (`ontology_changes`)", "Incremental (keeps last snapshot)",
         "Needs yesterday's state to say \"what changed since yesterday\"."),
        ("Monitoring checks", "Incremental (appends)", "History of checks is the point: a drop is measured "
         "against the last build."),
    ], widths=[150, 100, 230])
    r.h("Partitioning: we did not partition, on purpose")
    r.p("Partitioning splits a dataset into pieces (for example one per FAERS quarter) so a query or build "
        "can skip pieces it does not need. We did not add it [[DESIGNED]]:")
    r.bullets([
        "**Size.** The largest clean FAERS table has {{n:faers.case_reactions}} rows and the full FAERS rebuild "
        "takes {{n:optimization.O2.full_rebuild_s}} s. At this size the extra files and tuning cost more "
        "than they save [[ASSUMED]].",
        "**The raw files are already split by quarter.** FAERS lands as one set of files per quarter, and "
        "the incremental path reads only the new one. That is the useful kind of split at pilot size.",
        "**Signals need every case.** The PRR (proportional reporting ratio, the signal statistic) compares "
        "our drug with the background of *all* reports, so a split by drug would not let the signal step "
        "skip anything.",
        "**Scoped out on purpose.** The build plan puts partition tuning after the pilot, with its own "
        "measurements (project build order v1, section 4).",
    ])
    r.note("Recorded as decision D048 (accepted 6 Nov 2026): every dataset is written "
           "unpartitioned in the pilot. Revisit (partition FAERS by quarter, signals by drug) when FAERS holds "
           "8+ quarters or a single build passes 5 minutes. The same choice is a row in the hand-in log "
           "`docs/08-optimization-log/optimization-log.md` (D048). How much of each build is Foundry "
           "start-up is not measured separately.", title="Decision record")
    r.h("Where the LLM step sits, so it is not re-run")
    r.p("The AI transform sits **after** the labels are cleaned and split into sections, and **before** the "
        "signal step. It reads `clean_label_sections` and writes to the curated layer. Its cache key is built "
        "only from what changes the answer:")
    r.code("cache_key = sha256(setid | version | section_code | sha256(section_text)\n"
           "                  | parser_version | prompt_version | model_id)")
    r.bullets([
        "**A label refresh with the same text** gives the same key, so 0 calls (O1).",
        "**A new label version** or **changed section text** gives a new key, so only that section is read.",
        "**A new prompt or model** changes the key for every section, so everything is re-read and re-scored "
        "against the answer key before it is trusted.",
        "**Failures** (`parse_error`, `model_error`) are kept visible and retried; they never count as "
        "\"the label does not mention it\".",
    ])
    r.gate("Choices are explained", [
        ("Required evidence", "Each pipeline has a mode and a reason; partitioning and LLM placement explained."),
        ("Result", "Met (D048, accepted). Partitioning is recorded with its revisit trigger."),
        ("If it fails", "A reviewer cannot tell a deliberate choice from a default."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 8 next
    r.chapter("What we would measure next")
    r.table(["Measure", "Why", "Status"], [
        ("Compute-seconds per build (not just wall-clock)", "The brief names compute; wall-clock hides "
         "start-up and queueing", "Not measured"),
        ("O2 at 4+ FAERS quarters", "Find the point where incremental beats the full rebuild", "Not measured"),
        ("O2 in one build (state + outputs together)", "Removes one start-up and one read-back", "Not tried"),
        ("O3 back-to-back, with and without reuse", "Remove the earlier-build baseline doubt", "Not measured"),
        ("429 replies per DailyMed build", "Show the rate-limit benefit with a number", "Not measured"),
        ("O1 job wall time, like for like", "Turn \"tokens saved\" into \"time saved\"", "Not measured"),
        ("LLM cost in dollars, per label", "Needed before widening the AI past "
         "{{n:ai.pilot_labels}} labels to other drugs", "Not measured"),
        ("Foundry start-up time on its own", "Explains part of O2's gap", "Not measured"),
    ], widths=[170, 230, 80])
    r.key("Two optimizations helped and two did not, and each claim has a before and after number. The "
          "biggest lesson: incremental is not automatically faster. It must be measured at the data size "
          "you actually have.", title="Take-away")

    r.h("Figures quoted from project records (not in numbers.json)")
    r.table(["Figure", "Source"], [
        (f"{demo_all:,} DEMO rows; Q2 share {q2_share:.0%}; {o2_ratio:.2f} times slower; build time "
         f"{o3_cut:.0%} lower; downloads {o3_dl_cut:.1%} lower", "DERIVED here from two `numbers.json` values each"),
        ("Prompt p2 used about 55% more output tokens than p1", "A011 run 2; DECISIONS learning 2026-11-04"),
        ("O2 state = three state datasets + one quarter log", "`foundry/pipelines/clean/README.md`; O2"),
        ("Re-measure O2 at 4+ quarters", "O2; D044"),
        ("About 30 DailyMed index pages still pulled every build", "O3, optimization log"),
        ("2 remaining downloads are DailyMed \"None\" replies", "DQ42; O3"),
        ("O3 baseline from the step 9 build (not back-to-back)", "O3, optimization log"),
        ("Partition revisit at 8+ FAERS quarters or a build over 5 minutes", "D048"),
        ("O1b: 2.3 times the size; Build button skips an unchanged incremental dataset", "Optimization log O1b; "
         "DECISIONS learning 2026-11-06"),
        ("Partition tuning after the pilot", "project build order v1, section 4"),
    ], widths=[300, 204])
    r.numbers_appendix()
