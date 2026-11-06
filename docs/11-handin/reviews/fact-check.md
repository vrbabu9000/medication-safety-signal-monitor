# Fact check: reports R01–R08 and the architecture note

🔍 Fact Checker, 2026-11-05. Read-only review. No other file was edited.

**Scope.** `docs/11-handin/reports/src/R01…R08-*.py` and their PDFs in `reports/pdf/`, plus `architecture-note/architecture-note.md` and `.pdf`.
**Sources checked against (in this order).** `numbers.json` (captured 07:50Z; `app.workshop_version` and `app.timing_s` were added later, file time 03:06) · `baseline-gate.md` · `DECISIONS.md` (current status cells) · `optimization-log.md` · `data-issues-register.md` · `eval/ai-eval-v1.md` · `foundry/**/README.md` and the mirrored code · A010–A017 · `screens/README.md` · `reviews/phase-d-todo.md`. Anything that contradicts phase-d-todo is marked STALE.
**Locations.** "p" = PDF page. "l." = line in the `.py` source.
**Verdicts.** WRONG = the source says something else. STALE = was true, now superseded. INCONSISTENT = two places state one fact differently. UNSOURCED = no record found. OK = matches its source.

## Totals

| Verdict | Count |
|---|---|
| WRONG | 6 |
| STALE | 17 |
| INCONSISTENT | 7 (2 doc-specific + 5 cross-report) |
| UNSOURCED | 3 |
| OK (rows written below; every `{{n:…}}` key also resolved) | 61 |

Every `{{n:…}}` key used in R01–R09 resolves in numbers.json (script check). The only bad match was the literal `{{n:...}}` in a code example. **The PDFs were built before numbers.json last changed (03:06).** Rebuild all of them after the fixes (`--all`).

---

## WRONG (fix first)

| # | Doc · location | Claim | Source | Fix |
|---|---|---|---|---|
| W1 | R04 p9, l.215 | "126 active recalls: Is Active = true **(status not terminated)**" | `clean_recalls.py` l.69: `is_active = status == "Ongoing"`; statuses are Ongoing / Completed / Terminated. R02 p7 and R07 p7 say "Ongoing" | "(status Ongoing)". "Not terminated" would also count Completed recalls |
| W2 | R05 p2, l.79–80 | "D020, D027 … **Accepted (via D039)**" | DECISIONS status cells: D020 Accepted (via D039 G6). **D027 Proposed.** D039 G2 only confirmed the product key | "D020 accepted (via D039 G6); D027 proposed (product key confirmed by D039 G2)" |
| W3 | R03 p14, l.353 | NAION is in no semaglutide label "after the exact-term, **AI** and synonym checks" | The AI pilot read only 2 oxycodone labels (eval, D031 v5). rubric-check: the NAION record shows "Labels also read by AI: 0". A014: 0 of 36 safety sections mention it | "…after the exact-term and synonym checks (the AI pilot has not read semaglutide labels)" |
| W4 | Arch note decision 3 "Why" (md l.43; `architecture_note.py` l.205; PDF) | "every 'not in label' must show the **label passage** that was searched" | A not-in-label signal has nothing to quote (R03 p14; A012). The screen shows the label **versions** searched, with DailyMed links (phase-d #1) | "every 'not in label' must name the exact label versions that were searched, and every AI term must quote its passage" |
| W5 | R07 p6, l.204 | "XML reuse cuts **calls** to 2 per build" | Optimization log O3: the about-30 index pages are still pulled every build. Only the **XML downloads** fall from 1,321 to 2 | "cuts XML downloads to 2 per build (the index is still pulled)" |
| W6 | R01 p5, l.153 | "Every count in numbers.json was read with SQL **on these dataset pages**" | numbers.json `_meta.source` and baseline-gate.md: "Foundry SQL (**repo SQL panel**)" | "…read with SQL in the code repository's SQL panel at the baseline gate" |

## STALE

| # | Doc · location | Claim | Source (what superseded it) | Fix |
|---|---|---|---|---|
| S1 | R01 p13 + p18 (numbers table) | Workshop "published **v0.8.0**" | phase-d #4; numbers.json `app.workshop_version` = v0.9.0 (R04 and the arch note already say v0.9.0) | Rebuild R01. The text uses `{{n:app.workshop_version}}` |
| S2 | R01 p7 Fig 3 (l.209), R02 p3 Fig 1 (l.90), R03 p4 Fig 1 (l.109) | Diagram 30 v1 shows "XML reuse: O3, **measuring**" (`src/30-handin-data-flow-v1.mmd` l.26) | phase-d #5; O3 measured (3 m 23 s → 1 m 23 s) | Draw diagram 30 v2 with the measured O3 and point all three figures at it. This needs a diagram change, not a report change |
| S3 | R02 p11 Fig 4, l.292–295 | Uses `33-handin-incremental-faers-v1.png`. Caption: "drawn before O3 was measured" | phase-d #5; `33-handin-incremental-faers-v2.png` exists (README-handin); R06 already uses v2 | Point to v2 and drop the caveat sentence |
| S4 | R05 p8 Fig 2, l.271–274 | Same v1 diagram. Caption: "still marks … O3 as being measured" | Same as S3 | Same as S3 |
| S5 | R05 p1 is-not (l.55) + p2 gate (l.94) | Full log "**D001 to D047**" | phase-d #6; DECISIONS now ends at D048 (no partitioning, proposed) | "D001 to D048" |
| S6 | R05 p1 is-not, l.57 | "Final: **D045, D046 and D047** are still proposed" | phase-d #6: D037 and D048 are also Proposed, in the user's batch-accept list | "D037, D045, D046, D047 and D048 are still proposed (awaiting the owner's batch accept)" |
| S7 | R06 p9 note (l.317) + p10 gate (l.336) | "Our decision log has **no separate decision record** for 'no partitioning'… It should be logged" | D048 (2026-11-05, proposed): unpartitioned; revisit at 8+ FAERS quarters or a build over 5 min | "Recorded as D048 (proposed): …revisit when FAERS holds 8+ quarters or a build passes 5 minutes." Gate: "Met (D048, proposed)" |
| S8 | R04 p1 is-not (l.37), p2 gate (l.78), p3 test table (l.111–112), p3 gate (l.118–119), p13 gap row 1 + gate (l.380) | "the timed two-minute test **has not been run** / Not run / still to do" | phase-d #2; numbers.json `app.timing_s`: brief 11.5 s, recalls 1.1 s, what changed 0.8 s, signals + labels 2.4 s (browser script, View mode, human reading time not included); A016 | "Timed on the machine side: Morning brief loads in 11.5 s, page switches take 0.8–2.4 s ({{n:app.timing_s.*}}). A human two-minute walk-through has not been run." Use the `{{n:}}` keys |
| S9 | R04 p3 HMW row (l.100) + trust check (l.114); p13 gap "No link from a signal to the labels searched" (l.355); p13 idea "Signal → label links · PLANNED" (l.373) | "reaching the label version takes Object Explorer"; "Trace needs Object Explorer" | phase-d #1: page 1 has a **"Reference labels searched"** panel (Signal → Drug → Products → Reference Label). For NAION: Ozempic v20, Wegovy v19, oral Ozempic v14, with DailyMed links; `app.labels_searched_naion` = 3; screens/README | Trust check: "Met on page 1: the evidence and the reference labels searched (with DailyMed links) in one click." Gap row: drop it, or reword to "no dedicated Signal → Label link type yet (the panel walks existing links)". Idea status: partly done |
| S10 | R04 p5 step 3 + Fig 2 caption (l.155) | Record shows "the number of reference labels searched"; no panel, no screenshot | phase-d #1; `screens/app-1c-labels-searched-naion.jpg` | Add a step: "The panel *Reference labels searched* lists the 3 labels read ({{n:app.labels_searched_naion}}), with version and DailyMed link." Add the app-1c figure |
| S11 | R04 p13 gap row (l.353) | "'We pulled it at' is **empty** for FAERS and RxNorm" | phase-d #3; `ontology_changes.py` l.152 (FAERS = "quarterly file (no pull time)") and l.158 (RxNorm = pull time) | Remove the row. Optionally note that FAERS now says "quarterly file (no pull time)" on purpose |
| S12 | R03 p14 Watch out (l.360–362) + gate result (l.367) | "there is **no direct link** from the signal to the labels searched; a reviewer goes through Drug and Products" | phase-d #1 (as S9) | "Page 1 now lists the reference labels searched (same Signal → Drug → Products → Reference Label path) with DailyMed links; there is still no dedicated link type." Gate: Met |
| S13 | R03 p13 trace step 5 (l.342) | "The exact label version searched for each product" (no labels named) | phase-d #1; numbers.json `app.labels_searched_naion` = 3 | Add "Ozempic v20, Wegovy v19, oral Ozempic v14 (shown on page 1, panel *Reference labels searched*)" |
| S14 | R03 p15 ch.7 item 2 (l.377) | "Link Signal → searched Labels … closes the last trace hop" | phase-d #1 | Reword: "Optional: a dedicated link type (the page 1 panel already shows the labels via existing links)" |
| S15 | R07 Appendix DQ06 (l.288); ch.7 table | DQ06 "**Partly**: efficacy bucket D016 v3"; DQ06 is missing from "What we left" | phase-d #8 + rubric-check: DQ06 is **not handled**. Liraglutide's rank-1 signal is "Diabetic metabolic decompensation", an indication term | Appendix: "Left (accepted): indication terms still rank (liraglutide #1 'Diabetic metabolic decompensation')". Add a DQ06 row to ch.7 (that makes ten items left; update the gate "nine items" on p9) |
| S16 | Arch note **PDF** footer (+ `architecture-note.png`) | "reports **R0-R7**" | phase-d #7; `architecture_note.py` l.295 and the .md already say R01–R09 | Rebuild the PDF and PNG. The source is already fixed |
| S17 | R04 p13 "Next UI ideas" gate (l.383) | "the **timed test** and the real-user test are still to do" | phase-d #2 | "the human timed test and the real-user test are still to do (machine timings: …)" |


## INCONSISTENT

| # | Where | Statement A | Statement B | Source | Fix |
|---|---|---|---|---|---|
| X1 | Evidence-label legend: R03 p3, R04 p2, R05 p13 (`tools/handin/style.py` l.65–67) vs R01 p1, R02 p1, R07 p1 | DESIGNED = "Designed and written down, **but not built or run yet**"; ASSUMED = "A choice we made" | DESIGNED = "our choice / a choice"; ASSUMED = "not verified" | AGENT-BRIEF honesty rules: DESIGNED (a choice), ASSUMED. R03 p5 tags *built* key checks DESIGNED; R08 p6 says "DESIGNED built" | Change `style.py` l.65–67 to: DESIGNED = "a choice we made (may be built)"; ASSUMED = "not verified". Rebuild |
| X2 | Numbers appendix boilerplate (`build_report.py` l.200), all reports; cover text of R03, R06, R08 | "**Every number** in this report is looked up from numbers.json" | R01 quotes 2.9 s, about 1.5 s, 700 MB, about 1 vs 4 min, 25/22 properties, about 60 clicks. R03/R04 quote 22 properties and 15 fields. R05 quotes 56%, about 50%, 10.7%. R06 quotes 819,683 DEMO rows and 52%. None of these is in numbers.json | R02 and R07 already carry a "Figures quoted from project records" table | Reword to "Every number **in the table below** comes from numbers.json; other figures cite their record". Add the quoted-records table to R01, R03–R06 and R08 |
| X3 | Label-check order: R02 p9 ("Three checks, **in order**: 1 Text, 2 AI, 3 Synonyms", l.255), R05 p7, R08 p3, arch note decision 3 | text → AI → synonyms | Code checks **AI first, then text, then synonyms** | `ontology_signals.py` l.163–176; `foundry/pipelines/ontology/README.md` "(1) AI atomic term, (2) exact term…, (3) synonym" | Reorder to AI → text → synonym, or drop "in order". The outcome is the same; only `label_match_method` differs |
| X4 | Gate status vs result: R03 p15 "Ready to extend" (l.410), R05 p12 "Record of what did not work" (l.406), R04 p3 "User fit" (l.121) | status **PLANNED** | Result: "**Met**" (R04: "Met for the mapping") | — | Set status to TESTED, or change the result to "Not yet" |
| X5 | R06 p5 (l.200 vs l.209) | "write **four** state datasets again" | "keep the state as one table instead of **three**" | `foundry/pipelines/clean/README.md`: 3 state datasets + 1 quarter log; optimization log O2: "4 state datasets" | "write three state datasets and the quarter log again" and "one table instead of three" |
| X6 | Arch note decision 1 and decision 3 (md l.41/43, PDF) | "(D020, **D027**)" and "(**D037**, D041, D043)" carry no status, while "D045 **proposed**" does | — | DECISIONS: D027 Proposed, D037 Proposed; AGENT-BRIEF: proposed decisions are labelled | "(D020; D027 proposed)" and "(D037 proposed, D041, D043)" |
| X7 | DQ38 reporter type blank: every report (34% → 72%, from numbers.json 0.343/0.721) vs source docs | 34% → 72% | **35%** → 72% in data-issues-register DQ38, DECISIONS D025, and the D016 decision-change row | The register value is the Oct 20 profile; numbers.json is Foundry at the gate | Reports are right to use 34%. The lead should note the profile vs Foundry difference in the register (outside this agent's write scope). Optional R07 footnote |

Also seen across reports and **consistent** (OK): 1,073 / 126 / 26; 1,952 = 1,844 + 108; NAION a = 394, PRR 112.5, CI 92.19–137.24, χ² 10,653.8, 20,892; 88 s vs 32 s; O3 203 s → 83 s, 1,321 → 2; 448/448; F1 0.97 vs 0.85; 70,776 tokens; 21 checks; 4 Data Health checks; 10 vs 3 recalls; 2 triage decisions; D-0040-2027 reported 2026-10-21. Cosmetic: every numbers appendix prints "baseline-gate.md.." (a double period, from `_meta.source` + f-string). It goes away on rebuild if the source has no trailing period.

## UNSOURCED

| # | Doc · location | Claim | Searched | Fix |
|---|---|---|---|---|
| U1 | R01 p3, l.104 | "`Data/quarantine` (**empty so far**)" | foundry/README and ACTIVITY-LOG list the folder only | Drop "(empty so far)", or verify in Foundry |
| U2 | R01 p8 | "Ontology Manager calls its branch **Main**" | No record in docs/ or foundry/ | Cannot verify. Drop it, or add a screenshot or note |
| U3 | R04 p12 usability table | "25 raw properties in **A to Z order**"; "Past-decisions table **a few pixels high**" | A012 records 12 decimals only; ontology README records "row height Absolute 160 px"; nothing records A-to-Z or the original height | Cite the learning (Flex collapses, 2026-11-04) for the table height. Drop "A to Z", or cite a record |

---

## Per-document OK rows (verified)

### R01 Foundry from scratch
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p2 | 9 folders; 10 MSSM object types, 1 Action; 4 sources; 4 Data Health checks | foundry/README resource map; ACTIVITY-LOG "9 top-level folders"; ontology README | OK |
| p4 | monitoring_checks 21 rows per build; self-reading datasets (DailyMed XML, AI extractions, change snapshot) | pipelines/monitoring README; raw README; ontology pipelines README | OK |
| p6 | Lightweight about 1 min vs Spark about 4 min (observation); incremental 88 s vs 32 s | DECISIONS learnings 2026-11-04; O2 | OK |
| p8 | "Build all ancestors" re-runs the 700 MB FAERS download; VS Code auto-commit about 30 min | DECISIONS learnings | OK |
| p9 | 900 recalls, 663 Drugs@FDA, 1,824 NDC, 1,321 labels = source totals; about 50 requests, no key needed | numbers.json raw.*; raw README | OK |
| p11 | MSSM Signal 25 properties; create-only Action (D040); 2 decisions | screens/README; ontology README; numbers.json | OK |
| p12 | a = 394, PRR 112.5; 5/5 trace | numbers.json; baseline-gate | OK |
| p14 | One paste replaced about 60 clicks | DECISIONS learning 2026-11-04 (22 properties, about 60 clicks) | OK |
| p15 | AIP test 2.9 s, GPT-5.6 Sol default; 448/448; 9/9 cache, 0 calls; F1 0.97 vs 0.85; 70,776 tokens | `docs/10-delivery/2026-11-04-foundry-access-results.md`; eval; O1 | OK |
| p16 | 34% → 72%; 10 vs 3; both checks passed on the Health tab | numbers.json; screens/README | OK |

### R02 Pipelines
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p4 | OR-search 11 vs 25; openfda.* 47 vs 141; 0 error rows | DECISIONS learnings; foundry README | OK |
| p4 | Morphine substring about 50% (DQ34); OxyContin chain 7804 → NDA022272 → 59011-410-10 → bfdfe235 v44 | DQ34; foundry README | OK |
| p5 | 792,346 / 2,554,017 / 373,522; 26,681 replaced, 655 deleted; PS-only misses 56%; 465 of 3,408, median 122; 4,464 → 3,408 | numbers.json; learnings; D023 v2; foundry README | OK |
| p6 | LOINC 34066-1, 34070-3, 43685-7, 34071-1/42232-9, 34084-4; DQ42; 1,321 versions, 0 mismatches | `clean_labels.py` l.17–18; DQ40/42; foundry README | OK |
| p7 | 900 recalls, 126 Ongoing; NDC confidence bands; 20 of 31 NDCs, 4 active matched | `clean_recalls.py` l.69, l.102–129; learnings | OK |
| p9 | PRR / Evans (D006); 14,921; syn_v2 258 = 69/72/117; 1,952 = 1,844 + 108; rank per drug by χ²; evaluation_id inputs | numbers.json; `ontology_signals.py` l.204–208 | OK |
| p9 | NAION: 36 sections, none mention it | A014 l.41 | OK |
| p11–12 | O1–O3a table; 2,898 = 900 + 767 + 1,231; 0 after rebuild; planted change → 3 events; runs 2; openFDA 8 d, FAERS 130 d | numbers.json; A016; A017 | OK |
| p14 | Six changes; syn_v2 1,115 → 1,073; D016 v3 1,210 → 1,115 | DECISIONS change table | OK |

### R03 Ontology
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p2 | 10 object types, 11 link types (incl. the duplicate), 1 Action | ontology README | OK |
| p6 | Counts 13 / 1,321 / 900 / 448 / 14,921 / 1,952 / 2,898 / 2; Product count deliberately not quoted | numbers.json; ontology README | OK |
| p10 | D-0040-2027 compounded tirzepatide, 0 matched; step 6 links = source counts (141 products, 25 recalls) | A016; A010 | OK |
| p11 | Action fields, system-set fields, owner-only; rejected options | ontology README; D040; A010 | OK |
| p11 | Write-back survived step 6, step 8, baseline gate | A010; ontology README; baseline-gate | OK |
| p13 | NAION trace values (a 394 of 20,892, PRR, CI, χ², window 2026Q1–Q2) | numbers.json | OK |

### R04 Application
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p2 | v0.9.0, 4 pages; 1,073 · 126 · 26 | numbers.json; A016 | OK |
| p3 | Persona Dana, quotes, 15 minutes | design-thinking-canvas.md | OK |
| p4 | Refresh clocks: FAERS quarterly, openFDA weekly, DailyMed daily, RxNorm monthly | `ontology_changes.py` l.152–158 | OK |
| p9 | NAION record values; Evans thresholds | numbers.json; D006 | OK |
| p11 | 22 signal properties, 15 recall fields; decimals PRR 1 / CI 2 / χ² 1; about 10 clicks per column | ontology README; A012 l.41; learning 2026-11-05 | OK |
| p12 | 12 decimals → formatted; 12 drugs; 1,355 → 1,073; eight changes | A012; numbers.json `drugs_with_signals` | OK |

### R05 Decisions
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p2 | Status cells D018, D019, D021–D023, D041, D043, D016 v3, D044 Accepted; D037, D045, D046, D047 Proposed | DECISIONS | OK |
| p3 | DQ31 (methadone, hydrocodone); DQ28 openFDA lag; SrLC lag learning; DQ42 | register; learnings | OK |
| p5 | 6.9% of 397,224 Q1 cases ((26,681 + 655) / 397,224 = 6.88%) | numbers.json (DERIVED) | OK |
| p7 | 1,355 → 1,210 (−10.7%) → 1,115 → 1,073; bucket change keeps evaluation ids | numbers.json; DECISIONS | OK |
| p9 | D047 59% less; D045 2,898 / 0; D046 34% → 72%, 10 vs 3 | numbers.json; O3 | OK |
| p10–12 | Decision-change rows; twelve exclusions; A006 / D032–D035 reserved; no "Dropped" status in INDEX | DECISIONS; INDEX.md; D036 | OK |

### R06 Optimization log
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p4 | 41,704 + 29,072 = 70,776; 9 → 0 calls; cache-key parts | O1; `ai_label_extraction.py` l.85–87 | OK |
| p5 | 819,683 DEMO rows; 422,459 = 52% (51.5%); 88 = 62 + 26; 2.75×; EXCEPT ALL = 0 | O2; numbers.json | OK |
| p7 | 203 → 83 s (−59.1%); downloads −99.8%; 1,319 reused; baseline from the step 9 build | O3; numbers.json | OK |
| p8 | O3a 12.3–13.0 → 12.2 s, reverted | O3a | OK |
| p9 | Largest table 2,554,017; partition tuning after the pilot | numbers.json; project-build-order-v1 l.63 | OK |

### R07 Data judgment
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p2 | 42 issues; −145 / −95 / −42 = 282 = 1,355 − 1,073 | register; numbers.json | OK |
| p3 | 8.7% (422,872 vs 389,074); 6.9%; 56%; 465 / 3,408 / 122 | DQ36; numbers.json; learnings; D023 v2 | OK |
| p4 | Exenatide has no reference label → signals for 12 of 13 drugs | A013 l.34; numbers.json | OK |
| p4 | Morphine 19 labels, 76 sections | baseline-gate | OK |
| p5 | Gastric emptying for 4 GLP-1s; 9 spelling hits; syn_v2 examples (hypomotility, injection-site, QT) | A014 l.40, l.64–65; learnings | OK |
| p6 | 34.3% / 72.1%; 744 of 1,321 HTTP 429 | numbers.json; learnings | OK |
| p8–9 | Nine items left (ten after S15); NAION about 10 optic terms | DQ41; register | OK |

### R08 AI reliability
| Location | Claim | Source | Verdict |
|---|---|---|---|
| p2–4 | 448/448; 35/35; 35/37; F1 0.97 (recomputed 0.972); p1 11/35 | eval; numbers.json | OK |
| p4 | Answer key covers Boxed Warning + Contraindications of 2 labels; extras "adverse drug effects", "liver transplant" | eval per-section table | OK |
| p5 | One miss moves recall by about 3% (1/35 = 2.9%); long sections hold most items (about 411 of 448) | eval | OK |
| p6–7 | 3 AI checks of 21; diagram 35 AI group green, centre (AI 3 + freshness 3 + data judgment 3 + keys 12 = 21) | monitoring README; diagram 35 PNG viewed | OK |
| p9 | OnSIDES CC BY 4.0 | docs/09-roadmap/another-month… l.126 | OK |
| Advisory | Not stated: the hero signal's drug (semaglutide) has "Labels also read by AI: 0" | rubric-check; phase-d #8 (AI↔screen gap) | OK (advisory: add one line to ch.4 "Limits") |

### Architecture note (md + PDF)
| Location | Claim | Source | Verdict |
|---|---|---|---|
| Build facts | 13 (8 + 5); 4 sources; 792,346; 1,321; 900 (126); 1,952 (1,073); 10 types, 1 Action; v0.9.0; 21 checks | numbers.json | OK |
| Decision 1 | 50% false morphine rows (DQ34) | DQ34 | OK |
| Decision 2 | +8.7% (DQ36); 26,681 replaced, 655 deleted | DQ36; numbers.json | OK |
| Decision 3 | 448/448; F1 0.97 vs 0.85; 0 model calls; 1,355 → 1,073 | numbers.json | OK |
| Decision 4 | Decision survived rebuild; 2,898 events, 0 after rebuild | A010; numbers.json | OK |
| Not done | 88 s vs 32 s; D031 cut list; D029 | O2; DECISIONS | OK |
