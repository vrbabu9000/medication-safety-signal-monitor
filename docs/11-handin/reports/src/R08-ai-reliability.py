"""R08 AI reliability: what the AI does, how often it is wrong, how we know, how we would notice it getting worse.

Build:  .venv/bin/python tools/handin/build_report.py R08-ai-reliability
Output: docs/11-handin/reports/pdf/R08-ai-reliability.pdf

Sources: eval/ai-eval-v1.md, eval/gold-set/step7-pilot-gold-v1.json, foundry/pipelines/ai/README.md,
foundry/pipelines/ai/ai_label_extraction.py, A011, A012, A017, A019, D015, D041 (v2), D046, O1b,
foundry/pipelines/monitoring/README.md, docs/09-roadmap/another-month-sources-and-pharmacist-review.md.
Every measured number is a {{n:...}} lookup in docs/11-handin/numbers.json, or computed here from lookups
(marked DERIVED in the text).
"""

META = {
    "id": "R08",
    "title": "AI reliability",
    "short": "AI reliability",
    "subtitle": "how often the label extraction is wrong, and how we know",
    "version": "1.2",
    "date": "6 November 2026",
}


def _frac(s):
    a, b = (int(x) for x in str(s).split("/"))
    return a / b


def build(r):
    recall = _frac(r.n("ai.gold_recall_strict"))
    recall_p1 = _frac(r.n("ai.gold_recall_strict_p1"))
    prec = _frac(r.n("ai.gold_precision_upper"))
    f1_calc = 2 * prec * recall / (prec + recall)
    assert abs(f1_calc - r.n("ai.gold_f1")) < 0.01  # numbers.json F1 must agree with its parts
    grounded = r.n("ai.grounded") / r.n("ai.reactions")
    one_miss = 1 / int(str(r.n("ai.gold_recall_strict")).split("/")[1])  # DERIVED
    run1_tokens = r.n("ai.run1_tokens_prompt") + r.n("ai.run1_tokens_completion")
    widen_tokens = r.n("ai.d041_v2.new_prompt_tokens") + r.n("ai.d041_v2.new_completion_tokens")  # DERIVED
    found, key_items = (int(x) for x in str(r.n("ai.gold_recall_strict")).split("/"))
    found_p1 = int(str(r.n("ai.gold_recall_strict_p1")).split("/")[0])
    key_txt = f"{found} of {key_items} answer-key items"  # statistical recall, not an FDA recall

    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "The brief asks: can you say how often the AI extraction is wrong, and how you know? "
               "Stretch: would you notice if it got worse?"),
              ("One-line answer",
               f"On a small answer key ({key_items} items: the Boxed Warning and Contraindications of "
               "{{n:ai.v1_pilot.labels}} oxycodone labels, written by Claude and frozen before the run) it "
               f"found {key_txt} and added 2 extra terms (precision at worst {{{{n:ai.gold_precision_upper}}}}), "
               "so F1 = {{n:ai.gold_f1}} against the D015 target of {{n:ai.d015_target_f1}} (met on this pilot key "
               "only; the benchmark comparison was not run). Separately, across all "
               "{{n:ai.sections}} sections it read in {{n:ai.pilot_labels}} labels (2 oxycodone, 3 semaglutide), "
               "every one of its {{n:ai.reactions}} quotes is found word for word in the label. The semaglutide "
               "sections are not scored (no answer key). No pharmacist has checked the key, so this is a pilot "
               "result, not proof.")],
        is_=["How the AI label extraction works and where it sits in the pipeline",
             "The two checks we run (grounding and a frozen answer key) and their results",
             "What the results do not show, how we would notice a drop, and what the AI costs"],
        is_not=["A pharmacist-validated accuracy figure: no pharmacist has reviewed the answer key yet",
                "A score for the long label sections or the semaglutide labels: they are not scored",
                "A claim that the AI changes which signals are ranked: today it does not"],
        how_to_read="Chapter 1 is the one-page answer. Chapter 2 explains what the AI does. Chapter 3 gives "
                    "the measurements, chapter 4 their limits. Chapter 5 is the monitoring, chapter 6 the "
                    "cost, chapter 7 the next steps. Numbers from `numbers.json` are listed in the table at the "
                    "end. Figures from other project records cite that record where they appear and are listed "
                    "in *Figures quoted from project records*.",
    )

    # ------------------------------------------------------------------ 1 summary
    r.chapter("Summary in plain language")
    r.p("A drug **label** (the official prescribing information, published on **DailyMed** as SPL XML, a "
        "structured format) lists the side effects the maker knows about. Our app flags side effects that "
        "people report to **FAERS** (the FDA's adverse event report database) but that the label does not "
        "mention. To know what the label mentions, an **LLM** (a large language model; here Claude Sonnet, "
        "called through **AIP**, Palantir Foundry's AI service) reads each safety section of the label and "
        "lists every reaction it names, each with an **exact quote** from the text. The pilot covers "
        "{{n:scope.drugs_formulary}} drugs: {{n:scope.opioids}} opioids (oxycodone, hydrocodone, morphine, "
        "fentanyl, hydromorphone, methadone, buprenorphine, tramadol) and {{n:scope.glp1}} GLP-1 drugs "
        "(semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide). **The AI reads "
        "{{n:ai.pilot_labels}} of their labels: 2 for oxycodone (the first pilot) and, since 6 November "
        "(decision D041 v2), the {{n:ai.d041_v2.semaglutide_labels}} semaglutide labels behind our demo "
        "signal.**")
    r.p("Each claim carries a label. Evidence labels say what kind of claim it is; status labels say how far "
        "the work has got:", style="small")
    r.pill_legend()
    r.table(["Question", "Answer", "Evidence"], [
        ("Does it invent text?", "No invented quotes found: {{n:ai.grounded}} of {{n:ai.reactions}} quotes "
         f"appear word for word in the section ({grounded:.0%})", "[[OBSERVED]]"),
        ("Does it miss reactions?", f"On the scored sections it found {key_txt} (strict recall "
         f"{recall:.2f})", "[[OBSERVED]]"),
        ("Does it add wrong ones?", f"At most 2 extras: precision {{{{n:ai.gold_precision_upper}}}} ({prec:.2f}), "
         "counting both extras as errors", "[[OBSERVED]]"),
        ("Overall", f"F1 {{{{n:ai.gold_f1}}}} on the {key_items}-item key (2 short sections × "
         "{{n:ai.v1_pilot.labels}} oxycodone labels) against the target of {{n:ai.d015_target_f1}} (D015)",
         "[[DERIVED]]"),
        ("Did it read the demo drug?", "Yes, since 6 Nov: {{n:ai.d041_v2.semaglutide_labels}} semaglutide "
         "labels. It found diabetic-retinopathy terms and **{{n:ai.d041_v2.optic_or_naion_terms_found_by_ai}}** "
         "optic-nerve or NAION terms, so it agrees NAION is not in the label", "[[OBSERVED]]"),
        ("How sure are we?", "Not very, yet: small answer key, written by Claude, long sections and "
         "semaglutide sections unscored",
         "[[OBSERVED]] limits (ch. 4)"),
        ("Would we notice a drop?", "Grounding, errors and cache are checked every build; a model or prompt "
         "change forces re-extraction, then a manual re-score", "[[TESTED]]"),
    ], widths=[110, 300, 80])
    r.key(["The AI's job today is **evidence**, not decisions. Every reaction it lists links to the exact "
           "quote and label version, which is the trust rule: every flag traces back to its source. Since "
           "Workshop {{n:app.workshop_version|raw}} the quotes for the selected drug's labels are on the "
           "officer's screen (page 1, *What the AI read in these labels*).",
           "The headline is honest only with its limits: it is a pilot score on the short sections of "
           "{{n:ai.v1_pilot.labels}} oxycodone labels, against an answer key that Claude wrote and froze before "
           "the run."],
          title="The short version")
    r.callout("note", [
        "**The AI also checked the flag she sees first.** It read the {{n:app.labels_read_by_ai_naion}} "
        "semaglutide labels behind the hero signal (semaglutide × NAION). It found diabetic-retinopathy "
        "terms and no optic-nerve or NAION term. So three checks agree NAION is *not in label*: exact text, "
        "synonyms and the AI. The AI still does not change her signal list. NAION is a *known positive*, not "
        "a discovery: EMA PRAC (6 Jun 2025) and a WHO alert (27 Jun 2025) named it, and our 3 US labels do "
        "not mention it (DECISIONS learning 2026-11-05).",
        "**The AI's quotes are on her screen.** Page 1 has a table *What the AI read in these labels*: "
        "reaction, section, the word-for-word quote and the label (Workshop {{n:app.workshop_version|raw}}, "
        "report R04). She can see what the label *does* say about the eyes next to the signal.",
        "**Signals move only with a new FAERS quarter.** FAERS is about {{n:monitoring.faers_age_days}} days "
        "behind (monitoring `faers_age_days`), and the FDA replaced FAERS with AEMS in March 2026, so the "
        "future feed is unverified (DQ20).",
        "**Only the project owner can submit a triage decision today**, and monitoring alerts go to the "
        "owner, not to her. Both are production steps.",
    ], title="What this means for Dana (the safety officer)")
    r.gate("Summary answers the brief", [
        ("Required evidence", "A rate of wrong answers, how it was measured, and its limits."),
        ("Result", f"Met against the D015 target ({{{{n:ai.d015_target_f1}}}}) on the pilot key only: "
                   f"F1 {{{{n:ai.gold_f1}}}} on the {key_items}-item key; the benchmark comparison D015 asks for "
                   "(TAC 2017 / OnSIDES) was not run, so this is not independent. Separately, "
                   "grounded {{n:ai.grounded}}/{{n:ai.reactions}} across all {{n:ai.sections}} sections; limits "
                   "in chapter 4."),
        ("If it fails", "Say \"not measured\" for the long sections rather than extend the number."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 2 what it does
    r.chapter("What the AI does")
    r.p("The extraction is one Foundry **transform** (Python code that reads datasets and writes new ones). "
        "Decision D041 records the design; approach A011 records how it was tested. D041 v2 (accepted "
        "6 November, approach A019) added the 3 semaglutide labels with the same model, prompt, parser and "
        "cache; only the list of labels changed.")
    r.bullets([
        "**One call per safety section**, not per label: for example Boxed Warning, Contraindications, "
        "Warnings and Precautions, and Adverse Reactions.",
        "**Exact quote rule.** For every reaction the model must return the exact words from the section. "
        "Code then searches the section for that quote. A quote that is not there is marked `not_found`, so "
        "an invented quote cannot pass silently.",
        "**One reaction per item** (prompt p2). \"Addiction, abuse, and misuse\" becomes three items, because "
        "FAERS records one reaction term per row and matching needs single terms.",
        "**Extra fields.** An **assertion type** (what kind of statement it is: an adverse reaction seen in "
        "patients, a warned risk, a contraindicated condition, or other) and the population it applies to "
        "(for example neonates) are stored with each item.",
        "**Failures are visible.** A broken reply is `parse_error`, a failed call is `model_error`; both are "
        "kept and retried. A failure never counts as \"the label does not mention it\".",
        "**Cached.** The same text is never sent twice (see chapter 6 and report R06, entry O1).",
    ])
    r.table(["Output dataset", "One row per", "Holds"], [
        ("`ai_label_section_extractions`", "label section",
         "status, raw model reply, tokens, time, `from_cache`, cache key"),
        ("`ontology_labeled_reactions`", "reaction in a section",
         "reaction text, assertion type, population, **exact quote** and position, grounding result"),
    ], widths=[150, 90, 240])
    r.h("Where it sits, and what it changes today")
    r.p("The AI reads the cleaned label sections and writes to the curated layer, before the signal step. "
        "The signal step checks each FAERS reaction against the label in three ways: (1) an AI term whose "
        "quote code found in the text, (2) the exact term in a safety section, (3) the reviewed synonym "
        "table (A012, D037, D043). The outcome is the same in any order; only the recorded match method "
        "(`label_match_method`) differs. The table counts every drug × reaction statistic by the check that "
        "matched it first, in code order (Foundry, after D041 v2).")
    r.table(["First match", "Drug × reaction stats", "Evidence"], [
        ("1 · AI term (quote found by code)", "{{n:signals.label_check_stats.ai_term_exact}} "
         "({{n:ai.d041_v2.stats_matched_by_ai_oxycodone}} oxycodone, "
         "{{n:ai.d041_v2.stats_matched_by_ai_semaglutide}} semaglutide)", "[[OBSERVED]]"),
        ("2 · Exact text in a safety section", "{{n:signals.label_check_stats.label_text}}", "[[OBSERVED]]"),
        ("3 · Synonym, high band (in label)", "{{n:signals.label_check_stats.synonym_high}}", "[[OBSERVED]]"),
        ("3 · Synonym, medium band (possibly in label)", "{{n:signals.label_check_stats.synonym_medium}}",
         "[[OBSERVED]]"),
        ("None (not in label)", "{{n:signals.label_check_stats.none}}", "[[OBSERVED]]"),
    ], widths=[220, 190, 80])
    r.warning("**The AI does not change the signal list today.** For the {{n:ai.pilot_labels}} labels it "
              "reads, plain text matching already finds every term the AI finds (A012; re-checked after "
              "D041 v2: signals {{n:signals.total}} / ranked {{n:signals.ranked}}, "
              "{{n:ai.d041_v2.signals_changed}} signal changes). The {{n:signals.label_check_stats.ai_term_exact}} "
              "AI matches above would also match on text. The AI's value now is the exact quote, kept as "
              "evidence and shown on page 1. Its value for matching would come from other drugs' labels, "
              "which waits for the pharmacist check.", title="Said plainly")
    r.gate("The design is clear", [
        ("Required evidence", "Input, output, failure handling and the AI's effect on signals are written down."),
        ("Result", "Met (D041 and D041 v2 accepted; A011, A012, A019)."),
        ("If it fails", "A reviewer cannot tell whether a flag rests on the AI or on text matching."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 3 measured
    r.chapter("How we know how often it is wrong")
    r.table(["Check", "Catches", "Misses", "Result"], [
        ("**Grounding**: is each quote really in the section text?", "Invented text (hallucination)",
         "A real quote paired with the wrong item, and anything left out",
         "{{n:ai.grounded}} / {{n:ai.reactions}} exact [[OBSERVED]]"),
        ("**Answer key**: does the list match a hand-made list?", "Missed reactions (recall) and wrong extras "
         "(precision)", "Only covers the sections in the key",
         f"F1 {{{{n:ai.gold_f1}}}} on {key_items} items [[DERIVED]]"),
    ], widths=[130, 110, 130, 110])
    r.h("The answer key")
    r.p("The answer key (file `eval/gold-set/step7-pilot-gold-v1.json`) lists every reaction, risk or "
        "contraindicated condition that the section text itself states, with accepted spellings. It covers "
        "the Boxed Warning and Contraindications sections of the {{n:ai.v1_pilot.labels}} oxycodone pilot labels: "
        "OxyContin (modern label format) and an older-format oxycodone/acetaminophen generic. It was "
        "**frozen before the model ran**, so it could not be tuned to the output. The "
        "{{n:ai.d041_v2.new_sections}} semaglutide sections added on 6 November are **not in the key** and "
        "are not scored; F1 is unchanged and says nothing about them.")
    r.h("Results")
    r.table(["Measure", "Prompt p1", "Prompt p2 (in use)", "Evidence"], [
        ("Recall, strict (term must equal an accepted spelling)", f"{found_p1} of {key_items} items "
         f"({recall_p1:.2f})", f"**{key_txt}** ({recall:.2f})", "[[OBSERVED]]"),
        ("Precision, upper bound (both extras counted wrong)", "not scored",
         f"**{{{{n:ai.gold_precision_upper}}}}** ({prec:.2f})", "[[OBSERVED]]"),
        ("F1 (balance of recall and precision)", "not scored",
         "**{{n:ai.gold_f1}}** (target {{n:ai.d015_target_f1}}, D015)", "[[DERIVED]]"),
        ("Grounding, all {{n:ai.sections}} sections (not only the key's)", "all exact",
         "**{{n:ai.grounded}} / {{n:ai.reactions}}**", "[[OBSERVED]]"),
    ], widths=[170, 90, 130, 90])
    r.p("**Why strict recall.** FAERS reaction terms are MedDRA preferred terms (PT: the standard medical "
        "word list the FDA codes reports with). Matching works on single terms, so \"addiction, abuse, and "
        "misuse\" as one item would fail to match \"abuse\". Prompt p2 asks for one reaction per item; "
        f"that is why the items found rose from {found_p1} to {found} of {key_items} while grounding stayed "
        "complete.")
    r.p("**The two extras.** \"Adverse drug effects\" (too generic: a real false positive) and \"liver "
        "transplant\" (an outcome; arguably correct). Counting both as errors gives the precision upper bound.")
    r.how_we_know("Scoring is a script, not a judgement: `check_gold.py --strict` compares the run-2 terms "
                  "with the frozen key. Grounding is a column on every output row; the monitoring check "
                  "`ai.grounded_rate` reads it each build.")
    r.gate("Error rate measured", [
        ("Required evidence", "Recall, precision and grounding from a key frozen before the run."),
        ("Result", f"Met on the pilot key: F1 {{{{n:ai.gold_f1}}}} (recomputed here from its parts: {f1_calc:.2f}); not an independent benchmark."),
        ("If it fails", "Re-score after any model, prompt or parser change before trusting the output."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 4 limits
    r.chapter("What this does not show")
    r.p("These limits are part of the result. The F1 of {{n:ai.gold_f1}} should never be quoted without them.")
    r.key(["**The AI now reads the demo drug's labels** ({{n:ai.d041_v2.semaglutide_labels}} semaglutide "
           "labels, D041 v2). It found diabetic-retinopathy terms and no optic-nerve or NAION term: an "
           "independent check that agrees NAION is not in the label.",
           "**The AI does not change the signal list today.** Exact text already finds every term it finds on "
           "those labels (A012, A019).",
           "**The semaglutide sections are not scored.** The answer key covers only the short oxycodone "
           "sections. Scoring the long sections needs a pharmacist."], title="Three facts to say out loud")
    r.table(["Limit", "Why it matters", "What would fix it"], [
        (f"**Small key.** Only the short sections of {{{{n:ai.v1_pilot.labels}}}} oxycodone labels; "
         f"the answer key has {key_items} items.",
         f"One miss moves recall by about {one_miss:.0%}. The number is evidence for the prompt change, "
         "not a stable rate.", "A larger, stratified sample (chapter 7)."),
        ("**Claude wrote the key.** Frozen first, but not reviewed by a pharmacist.",
         "The same kind of model wrote the key and the answers; shared blind spots would not show.",
         "A pharmacist labels the key, part of it blind."),
        ("**Long sections are not scored.** Warnings and Precautions and Adverse Reactions hold most of the "
         "{{n:ai.reactions}} items.", "Long sections are where lists are longest and misses are likeliest.",
         "Score a sample of long-section items."),
        ("**The semaglutide labels are not scored.** {{n:ai.d041_v2.new_sections}} sections, "
         "{{n:ai.d041_v2.new_reactions}} items, no answer key.", "Grounding shows each quote is real; only a "
         "key would show a missed term. *No optic-nerve term* rests on grounding plus the text check.",
         "A pharmacist adds semaglutide items to the key."),
        ("**Grounding is not correctness.** A quote can be real and the item still wrong (for example a "
         "mechanism, not a reaction).", "{{n:ai.grounded}}/{{n:ai.reactions}} says \"no invented text\", "
         "not \"no errors\".", "Answer-key checks; a \"term is in its quote\" rate."),
        ("**The AI does not change signals today.**", "So an AI error cannot yet move the ranked queue; "
         "this also means the AI's matching value is unproven.", "Widen to more labels after the review."),
        ("**One model, one prompt.** Claude Sonnet with prompt p2 only.", "We cannot say another model "
         "would be better or worse.", "Re-score other AIP models on the same key."),
    ], widths=[170, 170, 140])
    r.gate("Limits stated", [
        ("Required evidence", "Each limit named, with its effect and the fix."),
        ("Result", "Met. The pilot score is labelled as a pilot score throughout."),
        ("If it fails", "The number reads as a validated accuracy, which it is not."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 5 monitoring
    r.chapter("How we would notice if it got worse")
    r.p("The brief's stretch goal is to notice when the AI gets worse. We have three layers; the first two "
        "are built, the third is planned.")
    r.table(["Layer", "What it does", "Status"], [
        ("**1. Checks every build**", "The monitoring transform appends {{n:monitoring.checks_per_build}} "
         "checks per build to `monitoring_checks`. Three are about the AI: grounded rate (fail below 0.95), "
         "sections not parsed, and cache hit rate. First run (2 oxycodone labels): grounded "
         "{{n:ai.v1_pilot.grounded}}/{{n:ai.v1_pilot.reactions}}, pass. After D041 v2: "
         "{{n:ai.grounded}}/{{n:ai.reactions}}, pass; cache hit rate {{n:monitoring.ai_cache_hit_rate_d041_v2_build}} "
         "in the widening build (only the new sections were sent).", "[[TESTED]]"),
        ("**2. Re-score on any change**", "The cache key includes the model, prompt and parser version. "
         "Changing any of them changes every key, so every section is extracted again (automatic). The new "
         "output is then scored against the answer key with `check_gold.py` before it is accepted (a manual "
         "script run today). Seen working when prompt p1 moved to p2 (A011 run 2).", "[[TESTED]] (re-score "
         "manual)"),
        ("**3. Pharmacist-labelled sample**", "With another month: a pharmacist labels a stratified sample "
         "of long sections; it is scored the same way each release. Drift = F1 falling by more than 0.05 "
         "between releases.", "[[PLANNED]]"),
    ], widths=[120, 290, 70])
    r.warning(["**Drift today is a replay, not live.** The pipeline drift table is rebuilt from dates the "
               "sources carry (`historical_replay`), because the pilot has not run for weeks. Live drift "
               "builds up only once builds run on a schedule, which is not set up yet.",
               "**No AI accuracy check runs every build yet.** Grounding runs every build; accuracy against "
               "the answer key runs when the model, prompt or parser changes."])
    r.gate("A drop would be noticed", [
        ("Required evidence", "AI checks run each build; a model or prompt change forces a re-score."),
        ("Result", "Met for invented quotes and failures. Accuracy drift waits for the pharmacist sample."),
        ("If it fails", "A silent model update could lower recall without any check firing."),
    ], status="TESTED")

    r.figure("docs/diagrams/png/35-handin-monitoring-v2.png",
             "Monitoring: the checks per build (the AI group is in green, centre), drift replay and Foundry "
             "Data Health, and who finds out.",
             source="docs/diagrams/png/35-handin-monitoring-v2.png (source: docs/diagrams/src/35-handin-monitoring-v2.mmd)", width=400)

    # ------------------------------------------------------------------ 6 cost
    r.chapter("What the AI costs")
    r.table(["Run", "Model calls", "Tokens", "Evidence"], [
        ("Run 1 (prompt p1, {{n:ai.v1_pilot.sections}} oxycodone sections)", "{{n:optimization.O1.before_calls}}",
         "{{n:ai.run1_tokens_prompt}} prompt + {{n:ai.run1_tokens_completion}} completion = "
         f"{run1_tokens:,}", "[[OBSERVED]]"),
        ("Run 2 (prompt p2)", "a fresh call per section", "about 55% more output tokens than p1: more, "
         "shorter items (A011 run 2; learning 2026-11-04); exact count not in `numbers.json`", "[[OBSERVED]] in A011"),
        ("D041 v2: add {{n:ai.d041_v2.semaglutide_labels}} semaglutide labels (O1b)",
         "{{n:ai.d041_v2.model_calls}} (only the new sections; {{n:ai.d041_v2.cached_sections_in_that_build}} "
         "from cache)", "{{n:ai.d041_v2.new_prompt_tokens}} prompt + {{n:ai.d041_v2.new_completion_tokens}} "
         f"completion = {widen_tokens:,}", "[[OBSERVED]]"),
        ("Forced rebuild with unchanged text", "{{n:ai.model_calls_on_rebuild}}",
         "{{n:optimization.O1.after_tokens}} ({{n:ai.from_cache_on_rebuild}} of {{n:ai.sections}} sections "
         "from cache)", "[[OBSERVED]]"),
    ], widths=[150, 90, 170, 70])
    r.bullets([
        "**Dollar cost: not measured.** We recorded tokens, not the AIP price per token.",
        "**Cost when widened further: not measured.** One data point: adding 3 labels cost "
        "{{n:ai.d041_v2.model_calls}} calls once, then 0 on rebuild. Extracting every label for all "
        "{{n:scope.drugs_formulary}} drugs would be a one-time cost per label version, then near zero thanks "
        "to the cache [[ASSUMED]]. We have not estimated it with numbers.",
        "The cache key is the cost control: a label refresh with the same text costs nothing; only a new "
        "label version or a model or prompt change costs calls (report R06, O1).",
    ])
    r.gate("Cost known", [
        ("Required evidence", "Tokens per run and calls on rebuild."),
        ("Result", "Met for tokens and calls, including the D041 v2 widening. Dollars and the cost of a "
                   "formulary-wide run are not measured."),
        ("If it fails", "Widening the AI could cost more than expected."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 7 next
    r.chapter("What we would do next")
    r.table(["Step", "Why", "Status"], [
        ("A named pharmacist labels the answer key and a stratified sample of long-section items; "
         "Claude's draft is hidden on a blind part of the sample", "Turns the pilot score into the "
         "pharmacist-labelled F1 per section that D015 asks for; the blind part guards against simply "
         "agreeing with Claude", "[[PROPOSED]]"),
        ("Compare with OnSIDES (a public, CC BY 4.0 table of label-listed side effects)", "An outside "
         "benchmark, not one we wrote", "[[PROPOSED]]"),
        ("Store and report a \"term is in its quote\" rate", "Catches a real quote paired with the wrong "
         "term", "[[PROPOSED]]"),
        ("Score other AIP models on the same key", "Model choice can be measured, not assumed", "[[PROPOSED]]"),
        ("Widen the AI to the other drugs' reference labels, after the pharmacist check", "Quoted evidence "
         "for every drug, not only oxycodone and semaglutide", "[[PROPOSED]]"),
        ("Schedule builds; add an AI tile to a Health page", "Live drift instead of replay", "[[PLANNED]]"),
    ], widths=[200, 210, 70])
    r.key("We can say how often the AI is wrong on the part we scored, and how we know: two different "
          "checks, a key frozen before the run, and every number reproducible by a script. We cannot yet "
          "say it for the long sections or the semaglutide labels, and we say so.", title="Take-away")

    r.h("Figures quoted from project records (not in numbers.json)")
    r.table(["Figure", "Source"], [
        ("2 extra terms (\"adverse drug effects\", \"liver transplant\")", "eval/ai-eval-v1.md"),
        (f"Recall and precision as decimals; one miss = about {one_miss:.0%}; grounded share",
         "DERIVED here from `numbers.json` fractions"),
        ("Diabetic-retinopathy terms found in the semaglutide labels; page-1 table of AI quotes",
         "A019; eval/ai-eval-v1.md (D041 v2 update); foundry/ontology/README.md"),
        ("Grounded-rate check fails below 0.95", "D046; monitoring README; A017"),
        ("Three AI checks among the per-build checks", "foundry/pipelines/monitoring/README.md"),
        ("Drift = F1 drop of more than 0.05 between releases", "eval/ai-eval-v1.md (another month)"),
        ("Prompt p2: about 55% more output tokens", "A011 run 2; DECISIONS learning 2026-11-04"),
        ("OnSIDES licence CC BY 4.0", "docs/09-roadmap/another-month-sources-and-pharmacist-review.md"),
    ], widths=[300, 204])
    r.numbers_appendix()
