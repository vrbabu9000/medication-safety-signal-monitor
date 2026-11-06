"""R07 Data judgment: the data problems we found, what we did about each, and what we left.

Build:  .venv/bin/python tools/handin/build_report.py R07-data-judgment
Output: docs/11-handin/reports/pdf/R07-data-judgment.pdf

Sources: docs/07-data-quality/data-issues-register.md (DQ01-DQ42), DECISIONS.md (decisions, changes,
learnings), A012-A017, eval/ai-eval-v1.md, docs/09-roadmap/*, numbers.json.
Numbers from numbers.json via {{n:...}}; differences computed from two looked-up numbers are DERIVED.
Figures from the October prototype or earlier steps are typed with their source and listed in appendix A.
"""

META = {
    "id": "R07",
    "title": "Data judgment",
    "short": "Data judgment",
    "subtitle": "the problems we found in public drug-safety data, what we fixed, and what we left",
    "version": "1.2",
    "date": "6 November 2026",
}

PNG = "docs/diagrams/png/"
SCREENS = "docs/11-handin/screens/"


def build(r):
    h = lambda k: r.n("signals.ranked_history." + k)
    d1, d2, d3 = h("step9") - h("syn_v1"), h("syn_v1") - h("d016_v3"), h("d016_v3") - h("syn_v2")
    total_cut = h("step9") - h("syn_v2")
    q2_changed = r.n("faers.q2_cases_replaced") + r.n("faers.q2_cases_deleted")
    q2_share = q2_changed / r.n("faers.q1_cases")

    # ------------------------------------------------------------------ cover
    r.cover(
        lead=[("The question this report answers",
               "Which problems did we find in the public data, which did we fix and how, which did we leave, and why?"),
              ("One-line answer",
               "We logged 42 data issues. The ones that would put a wrong number or a wrong label in front of the "
               "safety officer are fixed by written rules with before/after evidence. The ones that only add noise "
               "are tagged rather than hidden. The ones we could not fix (no MedDRA licence, no pharmacist yet, "
               "only two FAERS quarters) are stated plainly below.")],
        is_=["An honest account of data problems, grouped by what they would do to the officer's morning",
             "Before/after numbers for each fix, with the rule (decision) that made it",
             "A list of what we left and why, and what another month would change"],
        is_not=["A complete clinical review: no pharmacist has checked the synonym bands, the AI answer key or the ranked signals yet",
                "A claim that the ranked signals are real side effects: they are a review queue",
                "The pipeline description (see R02) or a Foundry primer (see R01)"],
        how_to_read="Chapter 1 is the summary, with what it means for the officer. Chapters 2 to 6 group the problems by their effect on "
                    "the officer: wrong counts, wrong label, noise in the queue, silent breaks, and recalls. "
                    "Chapter 7 is what we left. Chapter 8 is what we would do with more time. Appendix A lists all "
                    "42 register entries. DQ numbers refer to `docs/07-data-quality/data-issues-register.md`; D "
                    "numbers to `docs/06-decisions/DECISIONS.md`. Labels: [[OBSERVED]] measured, [[DERIVED]] "
                    "computed from measured numbers, [[DESIGNED]] a choice we made (it may be built), "
                    "[[ASSUMED]] not verified, [[TESTED]] built, run and checked.",
    )

    # ------------------------------------------------------------------ 01 summary
    r.chapter("Data judgment in one page")
    r.p("The brief warned that the data is messier than its documentation says. It was. We profiled every "
        "source by hand before building (D012) and kept a register of every problem: **42 entries**, DQ01 to "
        "DQ42. We sorted them by one question: *what would this do to the safety officer's morning?* The pilot "
        "covers {{n:scope.drugs_formulary}} drugs: {{n:scope.opioids}} opioids (oxycodone, hydrocodone, morphine, "
        "fentanyl, hydromorphone, methadone, buprenorphine, tramadol) and {{n:scope.glp1}} GLP-1 drugs "
        "(semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide).")
    r.table(["Effect on the officer", "Examples", "What we did", "Status"], [
        ("**Wrong counts**: a drug looks riskier or safer than the reports say",
         "Case versions and deletes (DQ36), substring names (DQ34), suspect roles (DQ35), one patient filed hundreds of times (DQ37)",
         "Four written rules in clean FAERS: D022, D020, D021, D023 v2", "Fixed"),
        ("**Wrong label**: a reaction looks *not in label* because we read the wrong one",
         "Tablet vs injection label (DQ33), openFDA label lag (DQ28), HTTP 200 with no label (DQ42), no reference label (exenatide)",
         "Reference label per product; DailyMed as truth; no label → no claim (G4)", "Fixed"),
        ("**Noise at the top of the queue**",
         "Homicide, child neglect; efficacy terms; label synonyms; a spelling bug",
         "Keyword buckets (tag, don't rank); reviewed synonym table", "Reduced"),
        ("**Silent breaks**: a feed changes and nothing errors",
         "Reporter type blank {{n:monitoring.reporter_type_blank_q1|.0%}} → {{n:monitoring.reporter_type_blank_q2|.0%}} (DQ38); "
         "openFDA search quirks; DailyMed rate limits", "Row-count checks; {{n:monitoring.checks_per_build}} monitoring checks per build", "Watched"),
        ("**Things we cannot fix in a pilot**",
         "No MedDRA groupings; reports are not incidence; stimulated reporting; indication terms; no pharmacist",
         "Stated, labelled, planned", "Left"),
    ], widths=[130, 170, 150, 54])
    r.p("The ranked review queue shows the effect of the noise work on identical data [[OBSERVED]]:")
    r.table(["Step", "Ranked signals", "Change", "What it removed"], [
        ("Step 9 (first full build): 13 drugs, exact text + AI label check", "{{n:signals.ranked_history.step9}}", "", "baseline"),
        ("+ spelling fix + synonym table syn_v1 (D043)", "{{n:signals.ranked_history.syn_v1}}", f"−{d1:,}", "label wording the exact check missed"),
        ("+ wider buckets D016 v3", "{{n:signals.ranked_history.d016_v3}}", f"−{d2:,}", "efficacy, product complaints, procedures"),
        ("+ synonym table syn_v2", "{{n:signals.ranked_history.syn_v2}}", f"−{d3:,}", "more wording misses, top 12 per drug"),
    ], widths=[210, 80, 60, 154])
    r.p(f"In all {total_cut:,} items left the ranked queue [[DERIVED]]. None was deleted: each is still a signal "
        "with a bucket, a caution or a *possibly in label* status, so the officer can still find it.")
    r.key("The known positive survived every step: semaglutide × NAION (optic ischaemic neuropathy, a sudden loss of "
          "blood flow to the optic nerve), {{n:signals.naion.a}} reports, PRR {{n:signals.naion.prr}}, now rank "
          "{{n:signals.naion.rank}} for semaglutide. None of the semaglutide labels in DailyMed mention it. It is a "
          "*known positive*, not a discovery: EMA PRAC (6 Jun 2025) and a WHO alert (27 Jun 2025) named it "
          "(DECISIONS learning 2026-11-05).",
          title="What the cleaning kept")
    r.callout("note", [
        "**New signals arrive only with a new FAERS quarter.** FAERS is about {{n:monitoring.faers_age_days}} "
        "days behind (monitoring `faers_age_days`), so *what changed since yesterday* is about recalls and "
        "labels, not new signals.",
        "**The FAERS feed itself is changing.** The FDA replaced FAERS with AEMS (its new adverse event "
        "system) in March 2026 (DQ20). We use the published quarterly files; how the future feed will arrive "
        "is **unverified**. The reporter-type field already went from {{n:monitoring.reporter_type_blank_q1|.0%}} "
        "to {{n:monitoring.reporter_type_blank_q2|.0%}} blank (DQ38), which we watch every build.",
        "**Only the project owner can submit a triage decision today.** Giving the officer that permission is "
        "a production step.",
        "**The AI's quotes are on her screen, for two drugs.** The AI reads {{n:ai.pilot_labels}} labels "
        "(oxycodone and semaglutide); page 1 shows what it quoted. For the other drugs the label check she sees "
        "rests on exact text and the reviewed synonym table (report R08).",
    ], title="What this means for Dana (the safety officer)")
    r.gate("Chapter 1: problems sorted by what they would do to the officer", [
        ("Required evidence", "Every fix has a rule (D number) and a before/after count on the same data."),
        ("Result", "Met for the rows marked Fixed and Reduced. *Left* rows say why."),
        ("If it fails", "A fix without numbers is moved to chapter 7 (left) until measured."),
    ], status="TESTED")

    # ------------------------------------------------------------------ 02 counts
    r.chapter("Problems that change the counts", new_page=False)
    r.p("FAERS (the FDA Adverse Event Reporting System) is a database of spontaneous reports. Its bulk quarterly "
        "files are the only way to filter by a drug's role in a report, but they are messy. Four problems would "
        "have changed every count; all four are fixed in `clean_faers.py`.")
    r.h("DQ36: phantom rows from case versions (fixed by D022)", 3)
    r.p("A report (case) gets follow-up versions in later quarters, and a later version can change the drug "
        "list. Delete lists point at any past quarter. In the October prototype, simply appending two quarters "
        "gave **8.7% phantom rows** (422,872 vs 389,074) [[OBSERVED]] (register, 2026-10-20).")
    r.p(f"**Rule D022:** keep the highest case version per case id (newer quarter wins ties), then apply that "
        f"quarter's deletes to all history. In Foundry, Q2 replaced {{{{n:faers.q2_cases_replaced}}}} Q1 cases "
        f"and deleted {{{{n:faers.q2_cases_deleted}}}}: {q2_share:.1%} of Q1's {{{{n:faers.q1_cases}}}} cases "
        f"changed in one quarter [[DERIVED]]. Result: {{{{n:faers.cases_current}}}} current cases.")
    r.h("DQ34: substring drug names (fixed by D020)", 3)
    r.p("Matching *morphine* as a substring also matched apomorphine and diamorphine (heroin): about 50% extra "
        "morphine rows in the prototype [[OBSERVED]]. **Rule D020:** exact RxNorm ingredient name after "
        "splitting combination names and stripping salt words; never substring; unmatched names kept for review.")
    r.h("DQ35 and DQ23: who is a suspect (fixed by D021)", 3)
    r.p("A report lists every drug the patient took. Our drug is often only *concomitant* (taken at the same "
        "time, not suspected). But counting only the *primary* suspect drops real reports: for oxycodone it "
        "would miss 56% of cases (Foundry, 2026-11-04) [[OBSERVED]]. **Rule D021:** primary suspect, secondary "
        "suspect or interacting; each ingredient once per case.")
    r.h("DQ37 and the mass-polypharmacy cluster (fixed by D023 v2)", 3)
    r.p("One patient can be filed by many companies under different case ids. A fold on age, sex, country and "
        "event date (D023 v1) removed most of it. Then the first ranked oxycodone list was led by pemphigus and "
        "rheumatic fever. Behind them: a Canadian cluster of **465 of 3,408** oxycodone cases listing a median "
        "of **122 drugs**, with ages that change between filings, so the person key misses them (A012) [[OBSERVED]].")
    r.p("**Rule D023 v2** [[DESIGNED]]: every report with 30 or more drugs leaves the main count but is kept as "
        "`a_mass_reports`. A signal that is at least half mass reports gets the caution *mostly mass reports* "
        "and is not ranked. We chose to set aside, not delete: the evidence stays visible on the signal record.")
    r.how_we_know(["Counts equal the October prototype exactly; the incremental path, which applies the rules "
                   "quarter by quarter, gives identical rows (EXCEPT ALL both ways = 0).",
                   "Baseline gate: for 5 random ranked signals, the count was recounted from FAERS rows: 5/5 equal."])

    # ------------------------------------------------------------------ 03 labels
    r.chapter("Problems that give the wrong label", new_page=False)
    r.p("A signal needs two things: more reports than expected, and *not found in the label*. If we read the "
        "wrong label, or no label, a reaction looks unlabeled when it is not. That is the most damaging false "
        "positive, because it looks like a finding.")
    r.table(["Problem", "What we saw", "Rule"], [
        ("DQ33 wrong product's label", "openFDA tagged injection-era semaglutide reports as the oral tablet and linked the tablet label; "
                                       "injection-site pain then looked unlabeled", "Reference label per product (application), D024 / D027"),
        ("DQ07 many labels per drug", "Brands, generics, repackagers each have labels", "One reference label per product = the application owner's (G3)"),
        ("DQ28 stale label copy", "openFDA's label copy lagged DailyMed by months (Ozempic)", "DailyMed is the label source of truth (D019)"),
        ("DQ19, DQ40 section codes", "Old labels use separate Warnings/Precautions; sub-sections use a generic code",
         "Six safety section codes; fold everything nested (D037)"),
        ("DQ27 version numbers", "Version numbers run from 1 to 3,540 and mean nothing across labels", "Compare versions only within one label (setid)"),
    ], widths=[110, 230, 164])
    r.h("DQ42: an HTTP 200 that is not a label (handled)", 3)
    r.p("For two tramadol repackager labels, DailyMed answered **HTTP 200 with the text `None`** instead of XML "
        "[[OBSERVED]]. A 200 is not proof of a document. The parser crashed the label build. Now raw keeps the "
        "reply as received; clean keeps only text starting with `<`; the version stays listed with "
        "`has_xml = false`. The DailyMed reuse step re-tries those two on every build on purpose "
        "({{n:optimization.O3.after_downloads}} downloads per build).")
    r.h("Exenatide: no reference label, so no claim (D039 G4)", 3)
    r.p("Exenatide has reports but no product with the owner's label in DailyMed. Rather than compare it with "
        "some other label, the rule says **uncertain is shown as uncertain**, never as *not in label*. So "
        "signals exist for {{n:scope.drugs_with_signals}} of our {{n:scope.drugs_formulary}} drugs [[OBSERVED]], "
        "and a monitoring check makes sure no ranked signal lacks a reference label (it is 0).")
    r.how_we_know("Baseline gate trace: for each of 5 random ranked signals, the reference labels searched were "
                  "listed (for example 19 labels, 76 sections for morphine) and the reaction term was in none of "
                  "their safety sections (`baseline-gate.md`).")

    # ------------------------------------------------------------------ 04 noise
    r.chapter("Problems that fill the queue with noise", new_page=False)
    r.p("With the counts and labels right, the ranked list was still not what a pharmacist would want to read "
        "first. These items are *real reports* and *really not in the label*, but most are not new side effects. "
        "We **tag** them instead of deleting them [[DESIGNED]].")
    r.table(["Noise", "Example at the top of the list", "Fix", "Effect"], [
        ("Social and legal terms", "Child neglect, Homicide, Imprisonment led the first oxycodone list (A012)",
         "D016 v2: keyword buckets; only *clinical* is ranked", "Moved off the top"),
        ("Abuse, overdose, pregnancy", "Dependence and overdose dominate opioid reports (DQ15); neonatal withdrawal (DQ26)",
         "Tagged buckets, visible but not ranked (D016)", "Tagged"),
        ("Label wording (synonyms)", "\"Impaired gastric emptying\" for all 4 GLP-1s; the labels say \"delays gastric emptying\" (A014)",
         "D043: reviewed synonym table; medium match → *possibly in label*", f"−{d1:,} with the spelling fix"),
        ("A spelling bug", "British spellings `-noea`, `-rrhoea`, `-ised` were missing from the US-spelling list: 9 hits wrongly unlabeled",
         "Fixed in `ontology_signals.py`", "part of the above"),
        ("Efficacy and product complaints", "Weight loss poor, Hunger, Increased appetite; \"Product …\" complaints (A013)",
         "D016 v3: wider efficacy, product-use and administrative buckets", f"−{d2:,}"),
        ("More wording misses", "Gastrointestinal hypomotility; injection-site terms; QT prolongation wording",
         "Synonym table syn_v2 from the top 12 per drug", f"−{d3:,}"),
    ], widths=[95, 185, 150, 74])
    r.p("The synonym table now has {{n:synonyms.rows}} rows: {{n:synonyms.high}} high (same idea → in label), "
        "{{n:synonyms.medium}} medium (close idea → *possibly in label*, {{n:signals.possibly_in_label}} signals) "
        "and {{n:synonyms.rejected}} rejected (kept, so the same lead is not argued twice). Every phrase was "
        "checked to appear in that drug's own label.")
    r.warning(["The bands were set by Claude, not yet by a pharmacist. Medium matches are never ranked, so an error "
               "there hides a signal from the top of the list but not from the screen.",
               "Keyword buckets are a stand-in for MedDRA groupings (the standard medical term hierarchy), which "
               "need a licence we do not have. They will leak: D016 v3 deliberately keeps *weight increased* and "
               "eating-behaviour terms as clinical."], title="Limits of this fix")
    r.how_we_know(["Each step was measured on identical data, locally and then in Foundry, with equal results (A013, A014).",
                   "Bucket changes do not change a signal's `evaluation_id`, so decisions already made stay linked. "
                   "Synonym changes do change it, by design: the label check is part of what the officer saw."])

    # ------------------------------------------------------------------ 05 silent breaks
    r.chapter("Problems that break silently", new_page=False)
    r.p("The worst data problems raise no error. A field empties, a search drops a term, a server answers "
        "politely with nothing. We found these by comparing counts with each source's own total, and we now "
        "watch for them every build.")
    r.table(["Problem", "What happened", "How we catch it now"], [
        ("**DQ38** reporter type", "FAERS reports with no reporter type: {{n:monitoring.reporter_type_blank_q1|.1%}} in 2026 Q1, "
                                   "{{n:monitoring.reporter_type_blank_q2|.1%}} in Q2. Likely the FDA's switch from FAERS to AEMS (DQ20) [[ASSUMED]]",
         "Monitoring check per quarter: **warn**. We show *unknown* and never guess the reporter"),
        ("openFDA OR search", "Without parentheses the first term was silently dropped: 11 oxycodone recalls instead of 25",
         "Row count must equal `meta.results.total` and the profile"),
        ("openFDA sparse fields", "Searching only the harmonised `openfda.*` field found 47 Drugs@FDA applications instead of 141",
         "Every search also uses the source's own ingredient field"),
        ("DailyMed rate limit", "A fast local pull got HTTP 429 for 744 of 1,321 labels; each became an error row, not a gap",
         "Retry with back-off; XML reuse cuts XML downloads to {{n:optimization.O3.after_downloads}} per build "
         "(the index is still pulled, O3)"),
        ("Recall volume", "Recalls reported for our drugs: {{n:monitoring.recalls_last4w}} in the last 4 weeks vs "
                          "{{n:monitoring.recalls_prev4w}} the 4 before", "Drift check: **warn**; the rise is real (A017)"),
    ], widths=[95, 245, 164])
    r.p("Note on DQ38: {{n:monitoring.reporter_type_blank_q1|.0%}} is the Foundry value at the baseline gate "
        "(`monitoring_checks`). The register's first profile on 20 October said 35%; this report uses the "
        "Foundry value.", style="small")
    r.figure(PNG + "35-handin-monitoring-v2.png",
             "Monitoring (v2): {{n:monitoring.checks_per_build}} computed checks per build, the drift replay, and "
             "{{n:monitoring.data_health_checks}} Foundry Data Health checks, with first-run results (AI row "
             "updated after D041 v2).",
             source="docs/diagrams/png/35-handin-monitoring-v2.png")
    r.how_we_know("Both warnings on the first Foundry run are real, which is the best evidence the checks work. "
                  "The drift series is a **historical replay** from source dates, not weeks of live builds; live "
                  "history accumulates with each build; there is no build schedule yet (D046).")

    # ------------------------------------------------------------------ 06 recalls
    r.chapter("Recall problems", new_page=False)
    r.p("Recalls (FDA enforcement reports) name products in free text. Linking a recall to *our* products is "
        "the hard part.")
    r.table(["Problem", "What we saw", "What we did"], [
        ("Over-attached packages", "openFDA attaches every package of an application to every recall record",
         "Parse NDCs from the recall's own text; grade high / medium / low / none"),
        ("DQ11, DQ29 NDCs missing or unknown", "In the oxycodone pilot, 20 of 31 printed package NDCs were no longer in the NDC directory",
         "Keep unmatched with a reason; every recall also gets an ingredient row"),
        ("DQ12 compounded products", "Newest recall {{n:recalls.newest}}: compounded tirzepatide, no FDA product",
         "Shown under tirzepatide; *Matched to our products: 0*, said plainly"),
        ("DQ30 *Ongoing* for years", "Some recalls stay Ongoing long after they matter", "Active = Ongoing ({{n:recalls.active}} of "
                                                                                       "{{n:recalls.total}}); sorted newest first; not tuned further"),
    ], widths=[120, 210, 174])
    r.figure(SCREENS + "app-2-recalls.jpg",
             "Page 2 · Recalls: active recalls for the chosen drugs, newest first; the detail panel shows "
             "{{n:recalls.newest}} with *Matched to our products: 0*.",
             source="docs/11-handin/screens/app-2-recalls.jpg (Foundry, 2026-11-05)", width=420)

    # ------------------------------------------------------------------ 07 left
    r.chapter("What we left, and why", new_page=False)
    r.p("These are known and written down. Each one is a choice, not an oversight.")
    r.table(["Left as is", "Why", "Risk to the officer"], [
        ("**Reports are not incidence** (DQ03)", "FAERS has no denominator; PRR compares reporting, not risk",
         "Wording on screen: *review queue*, not findings"),
        ("**Stimulated reporting** (DQ04)", "Spikes after news or lawsuits need event dates and more quarters than our two",
         "A media-driven term can rank high. The hero signal NAION is the kind it can inflate; its "
         "reporter-type split is **not measured**"),
        ("**Indication terms** (DQ06)", "No rule yet to drop reactions that match the drug's own use "
         "(its Indications section)", "Liraglutide's rank-1 signal is \"Diabetic metabolic decompensation\", "
         "a worsening of the diabetes it treats, not a new side effect"),
        ("**Lawyer-filed reports** (DQ18, DQ21)", "Tagging needs the reporter type, which went {{n:monitoring.reporter_type_blank_q2|.0%}} blank (DQ38)",
         "Litigation-style terms not separated"),
        ("**No MedDRA groupings** (DQ22, DQ41)", "Licence not available for a public pilot", "One idea split over many terms (NAION spans about 10 optic terms); a grouped signal can be missed"),
        ("**Residue in the duplicate fold** (DQ37)", "The same patient with age 43 in one filing and 44 in another is not folded",
         "Small double counts remain; the 30-drug cut catches the worst"),
        ("**Polydrug confounding** (DQ17)", "No adjustment model; role filter and mass-report cut only", "A co-prescribed drug's effect can show up"),
        ("**AI long sections not scored** (DQ10)", "Answer key covers only Boxed Warning + Contraindications of {{n:ai.v1_pilot.labels}} oxycodone labels "
         "(4 short sections); Claude-written, pharmacist pending. The {{n:ai.d041_v2.new_sections}} semaglutide sections are not scored",
         "Unknown accuracy on Adverse Reactions tables; the AI does not change the list today"),
        ("**Synonym bands not reviewed**", "No pharmacist named yet", "A wrong *high* band hides a real signal"),
        ("**Only two FAERS quarters** (2026 Q1–Q2)", "Pilot scope; enough for PRR, not for trends", "No *new this quarter* trend yet"),
    ], widths=[140, 200, 164])
    r.note("History, not data: a duplicate Signal → Drug link type created by mistake on 2026-11-05 was deleted "
           "on 6 Nov after checking nothing used it.", title="One modelling mistake, fixed")

    # ------------------------------------------------------------------ 08 more time
    r.chapter("What we would do with more time", new_page=False)
    r.table(["Next step", "Fixes", "Why first"], [
        ("**A pharmacist review loop**: Claude prepares an evidence packet; the pharmacist decides; the decision "
         "is saved by a create-only Foundry Action", "Synonym bands ({{n:synonyms.rows}} rows), the AI answer key, the top ranked signals",
         "The biggest gap is not data but a named reviewer"),
        ("**MedDRA licence** (or standard query groups)", "DQ22, DQ41; replaces keyword buckets", "Removes the largest source of leakage"),
        ("**More FAERS quarters**", "DQ04 stimulated reporting; *new this quarter* trends; re-measure incremental FAERS at 4+ quarters",
         "Trends need history"),
        ("**Schedules and live drift**", "Freshness checks fire on their own; 3–4 week live drift window (D009)", "Replay becomes real monitoring"),
        ("**Widen the AI** to the other drugs' reference labels (today oxycodone and semaglutide)", "DQ10; quotes for every *in label* decision", "Only after the answer key is signed off"),
        ("**Score the long sections with a pharmacist**", "DQ10; the semaglutide and Adverse Reactions sections are unscored", "Turns grounding into accuracy"),
        ("**Second opinions**", "SrLC label changes, FDA Drug Safety Communications, OnSIDES, PubMed and ClinicalTrials.gov in the packet",
         "Researched in `docs/09-roadmap/another-month-sources-and-pharmacist-review.md`"),
    ], widths=[170, 210, 124])
    r.gate("Data judgment: found, fixed what matters, honest about the rest", [
        ("Required evidence", "A register of every issue; a rule and before/after numbers for each fix; a reason for each item left."),
        ("Result", f"Met. 42 issues logged; wrong-count and wrong-label problems fixed by rule; queue noise cut by "
                   f"{total_cut:,} ranked items without deleting any; silent breaks watched; ten items left with reasons."),
        ("If it fails", "Any new issue goes into the register first, with its effect on the officer."),
    ], status="TESTED")

    # ------------------------------------------------------------------ appendix
    r.chapter("The register, DQ01 to DQ42", label="A")
    r.p("The register's own status column was set when each issue was first logged; many rows still say "
        "*Suspected* although a later decision handled them. The right-hand column reads the decisions log.", style="small")
    reg = [
        ("DQ01", "FAERS follow-up versions duplicate cases", "Suspected", "Handled by D022 (see DQ36)"),
        ("DQ02", "Drug names are free text", "Suspected", "Handled: D020 exact identity, unmatched kept"),
        ("DQ03", "Reports are not incidence", "Suspected", "Accepted: PRR + careful wording"),
        ("DQ04", "Stimulated reporting after news", "Suspected", "Left (chapter 7)"),
        ("DQ05", "Suspect vs concomitant role", "Suspected", "Handled: D021"),
        ("DQ06", "Indication terms reported as reactions", "Suspected",
         "Left (known gap): indication terms still rank (liraglutide #1 \"Diabetic metabolic decompensation\")"),
        ("DQ07", "Many labels per ingredient", "Suspected", "Handled: reference label per product (G3)"),
        ("DQ08", "Label version history", "Suspected", "Handled: per setid + version; change feed"),
        ("DQ09", "Label prose vs FAERS terms", "Handled partly", "Text + US spelling + synonyms syn_v2; pharmacist pending"),
        ("DQ10", "Reaction tables inside label XML", "Suspected", "Left: long sections not scored"),
        ("DQ11", "Recall product in free text", "Suspected", "Handled: NDC from text + confidence"),
        ("DQ12", "Compounded products recalled", "Suspected", "Shown under the drug; 0 product matches"),
        ("DQ13", "Ingredient vs salt names", "Suspected", "Handled: salt strip (D020)"),
        ("DQ14", "Sources on different clocks", "Suspected", "Handled: as-of per source (D045)"),
        ("DQ15", "Abuse/overdose dominate opioid reports", "Confirmed", "Tagged, not ranked (D016)"),
        ("DQ16", "Combination products", "Suspected", "Flagged; each ingredient counted"),
        ("DQ17", "Polydrug confounding", "Suspected", "Left: role filter + mass cut only"),
        ("DQ18", "Litigation-style terms", "Confirmed", "Left: reporter type unreliable (DQ38)"),
        ("DQ19", "Old vs new Warnings section codes", "Confirmed", "Handled: both codes (D037)"),
        ("DQ20", "FAERS replaced by AEMS (Mar 2026)", "Confirmed", "Quarterly files used; future feed unverified"),
        ("DQ21", "Lawyers filed most 2021 oxycodone reports", "Confirmed", "Left: D025 monitors fill rate"),
        ("DQ22", "\"Hyperalgesia\" has 0 reports", "Confirmed", "Left: needs MedDRA grouping"),
        ("DQ23", "Our drug often only concomitant", "Confirmed", "Handled: bulk files + D021"),
        ("DQ24", "openFDA enrichment is a name match", "Confirmed", "Avoided: bulk files + own identity"),
        ("DQ25", "Search field changes counts", "Confirmed", "Handled: one identity rule"),
        ("DQ26", "Pregnancy/neonatal terms rank high", "Confirmed", "Tagged, not ranked (D016)"),
        ("DQ27", "Version numbers not comparable", "Confirmed", "Compared within one setid only"),
        ("DQ28", "openFDA label copy lags DailyMed", "Confirmed", "Handled: DailyMed is truth (D019)"),
        ("DQ29", "Compounded NDCs unknown", "Confirmed", "Kept with a reason; ingredient row"),
        ("DQ30", "Recalls Ongoing for years", "Confirmed", "Active = Ongoing; newest first"),
        ("DQ31", "ATC class misses our drugs", "Confirmed", "Handled: explicit 13-RxCUI list (D018)"),
        ("DQ32", "Trials data noisy for safety", "Confirmed", "Source cut from the pilot (D031)"),
        ("DQ33", "Tablet vs injection label", "Confirmed", "Handled: product-level label (D024; D027)"),
        ("DQ34", "Substring drug matching", "Measured", "Handled: D020"),
        ("DQ35", "SS role repeats PS", "Measured", "Handled: D021, once per case"),
        ("DQ36", "Case versions and deletes: phantom rows", "Measured", "Handled: D022"),
        ("DQ37", "Same patient under many case ids", "Measured", "Handled: D023 v1 + v2; residue left"),
        ("DQ38", "Reporter type blank jumps", "Measured", "Watched: monitoring warn"),
        ("DQ39", "Bulk FAERS has no openfda block", "Measured", "Handled: `nda_num` → application (D024)"),
        ("DQ40", "Sub-section codes; repeated version", "Measured", "Handled: fold nested; text hash in cache key"),
        ("DQ41", "One idea over many terms (NAION)", "Measured", "Left: no MedDRA grouping"),
        ("DQ42", "HTTP 200 with \"None\"", "Handled", "Handled: clean keeps only XML"),
    ]
    r.table(["ID", "Issue", "Register says", "Where it stands"], reg, widths=[40, 200, 80, 184])

    r.h("Figures quoted from project records (not in numbers.json)")
    r.table(["Figure", "Source"], [
        ("Append = 8.7% phantom rows (422,872 vs 389,074)", "DQ36, register (prototype, 2026-10-20)"),
        ("Morphine substring about +50% rows", "DQ34, register (prototype)"),
        ("Primary-suspect-only misses 56% of oxycodone cases", "DECISIONS learnings, 2026-11-04"),
        ("465 of 3,408 oxycodone cases, median 122 drugs", "D023 v2; A012"),
        ("Ranked removals by bucket; gastric emptying; 9 spelling hits", "A013, A014"),
        ("openFDA 11 vs 25 recalls; 47 vs 141 applications", "DECISIONS learnings, 2026-11-04"),
        ("DailyMed 429 for 744 of 1,321 labels (local pull)", "DECISIONS learnings, 2026-11-04"),
        ("20 of 31 printed recall NDCs not in the directory", "DECISIONS learnings, 2026-11-04"),
        ("Version numbers 1 to 3,540", "DQ27, register"),
        ("Morphine trace: 19 labels, 76 sections", "baseline-gate.md"),
        ("Liraglutide rank-1 \"Diabetic metabolic decompensation\"", "DQ06; Workshop page 1 (screen app-1, 2026-11-05)"),
        ("Reporter type blank 35% (first profile)", "DQ38, register (profile 2026-10-20)"),
        ("AEMS replaced FAERS in March 2026", "DQ20, register"),
        ("About 30 DailyMed index pages still pulled per build", "O3, optimization log"),
    ], widths=[300, 204])
    r.numbers_appendix()
