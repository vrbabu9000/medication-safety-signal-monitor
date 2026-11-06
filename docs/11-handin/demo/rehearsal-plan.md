# Rehearsal plan: 20:00, two passes, questions, plan B

_🎬 Demo Director view · 2026-11-05 (Phase D fix pass), refreshed 2026-11-06 for D041 v2 and the batch decision · stage: **Test** · goes with [demo-navigation-guide.md](demo-navigation-guide.md), [ripple-table.md](ripple-table.md) and the deck's [speaking_script.md](../deck/speaking_script.md) · newcomers start at [R00 "Start here"](../reports/pdf/R00-start-here.pdf)_

**TL;DR.** The timing table adds to exactly 20:00, follows the binding agenda in [AGENT-BRIEF.md](../AGENT-BRIEF.md), and uses the same slot per slide as the speaking script. Rehearse twice: a tech run the day before (click everything, time everything, decide live or screenshot for each stop) and a dress run on the day (no stopping, with questions). The triage form is **opened and cancelled** in rehearsal and, by default, in the demo. The 5 riskiest moments each have a plan B with a screenshot that already exists. Machine timings exist (brief 11.5 s, page switches 0.8–2.4 s, timed on Workshop v0.9.0; v0.10.0 adds one table below the fold on page 1 and was not re-timed); a human two-minute walk-through has not been run.

## 1. Timing (adds to 20:00)

| Stop | Start | End | Seconds | Deck slide | Where | Rubric row | Live or slide |
|---|---|---|---|---|---|---|---|
| A0 Officer's problem | 0:00 | 1:30 | 90 | 1–2 | deck | Communication | slide |
| A1 Morning brief | 1:30 | 3:00 | 90 | 3 | Workshop, Morning brief | Application (trust) | live |
| A2 Noise, then filter to semaglutide | 3:00 | 3:40 | 40 | 4 | page 1 | Application | live |
| A3 Evidence (NAION, a known positive) | 3:40 | 4:30 | 50 | 4 | page 1 right panel | Application (trace) | live |
| A4 Labels searched + DailyMed `optic` search + AI quotes table | 4:30 | 5:20 | 50 | 4 | page 1 panels, DailyMed tab | Application, AI reliability | live (one more scroll: time it in the tech run) |
| A5 Triage form (Cancel) | 5:20 | 6:00 | 40 | 4 | Action form | Application (trust) | live (no write by default) |
| A6 Recalls + FDA record + Class I | 6:00 | 6:50 | 50 | 5 | page 2, openFDA tab | Application, Data judgment | live |
| A7 What changed | 6:50 | 7:30 | 40 | 5 | page 3, Past month | Application | live |
| H1 Architecture picture | 7:30 | 8:30 | 60 | 6 | diagram 38 v2 (detail: 30 v3) | Architecture | slide |
| H2 Data Lineage | 8:30 | 9:30 | 60 | 6 | lineage tab | Architecture | live |
| H3 Ontology picture | 9:30 | 10:15 | 45 | 7 | diagram 31 v2 | Architecture | slide |
| H4 Ontology Manager | 10:15 | 10:45 | 30 | 7 | MSSM Signal | Architecture | live |
| H5 Object Explorer trace | 10:45 | 11:30 | 45 | 7 | NAION links | Application (trace) | live |
| H6 One report → ranked signal | 11:30 | 12:30 | 60 | 8 | diagram 32 v3 | Data judgment | slide |
| H7 Signal code | 12:30 | 12:50 | 20 | 8 | `ontology_signals.py` | Architecture | optional live |
| H8 Review queue, not findings | 12:50 | 13:30 | 40 | 9 | funnel | Data judgment | slide |
| H9 AI reliability | 13:30 | 14:45 | 75 | 10 | slide (+ AI code and SQL) | AI reliability, Optimization | slide + optional live |
| H10 Monitoring | 14:45 | 15:30 | 45 | 11 | slide (+ monitoring SQL or Health) | AI reliability, Data judgment | slide + optional live |
| H11 Optimization log | 15:30 | 16:45 | 75 | 12 | slide | Optimization | slide |
| H12 Incremental FAERS | 16:45 | 17:30 | 45 | 13 | diagram 33 FAERS panel, full v3 in B2 (+ inc log) | Optimization | slide + optional live |
| H13 Data judgment | 17:30 | 19:00 | 90 | 14 | slide (+ monitoring row) | Data judgment | slide + optional live |
| H14 Another month | 19:00 | 19:40 | 40 | 15 | slide | Communication | slide |
| H15 What to take away | 19:40 | 20:00 | 20 | 16 | slide | Communication | slide |
| **Total** | | | **1,200** | | | | |

**Checkpoints to glance at your watch:** 3:00 (leaving the Morning brief), 6:00 (leaving page 1), 7:30 (leaving the app), 11:30 (leaving the Ontology), 15:30 (leaving AI and monitoring), 19:00 (last slide). If you are more than 30 s late at a checkpoint, take the cuts below.

**Cuts if late (in this order, same as the speaking script):** drop the optional switches (H7, H9, H10, H12, H13) → skip the Object Explorer half of H5 (say "backup B4 shows it") → shorten H12 to one sentence ("correct, slower at two quarters, so not switched on"). Never cut A4 (labels searched and the DailyMed search), A5 (the Action form), H2 (lineage) or the honest limits in H9.

## 2. Two rehearsal passes

| | Pass 1 · tech run | Pass 2 · dress run |
|---|---|---|
| When | The day before | Demo day, at least 2 hours before |
| Goal | Every click works; real seconds per stop; choose live or screenshot per stop | 20:00 without stopping; practise answers and two fallbacks |
| Setup | Full pre-demo checklist (navigation guide §1) | Same tabs, same zoom, deck in presenter view |
| Triage | Open the form on NAION, read the locked fields, press **Cancel**. Never Submit: the Action is create-only and nothing can be deleted | Same. Ask the owner for the Cancel / Submit choice and write it in checklist #4 |
| Safety-officer checks | (a) DailyMed: click the Ozempic v20 link from page 1, Cmd+F `optic`; the first hit must not be the retinopathy warning (else use `ischemic optic`); note which version DailyMed shows; screenshot it. (b) Page 2: count the active **Class I** recalls and read D-0788-2026's *Matched to our products*; write both in navigation guide checklist #9 (both **not measured** today). (c) A person times the three morning questions with a stopwatch, reading included (checklist #10) | (b) and (c) numbers are said aloud only if measured here |
| Also check | Open the form on **Oxycodone · Myoclonus** and read its evaluation id; compare with the stored test decision `cbcd091262d23bd6`. If they differ, that is a live Q&A example of a decision on older evidence. Cancel | — |
| Measure | Write the actual seconds and load time next to each stop. **Rule: a page that takes more than 10 s to load in rehearsal is shown as a screenshot in the demo.** Compare with the machine timings (the only measured speed numbers so far): brief 11.5 s, page switches 0.8–2.4 s | Time at each checkpoint |
| Also time (optional) | One build each of `ontology_signal_signals` and `ontology_change_events` (dataset page → Build), so the ripple table's "how long" column can be filled | — |
| Fallbacks | Open each fallback screenshot once, so you know where it is | Deliberately use 2 fallbacks: Object Explorer (H5) and Lineage (H2) |
| Questions | Read the question bank (§3) aloud once, clicking each "where to show it" | A listener asks 3 questions from §3, including at least one of the three rubric-check questions (§3.1); answer in 2 sentences each |
| Done when | Every stop has a measured time and a live/screenshot choice | Finished within 20:00 ± 20 s and all 3 answers under 30 s each |

## 3. Likely questions

Each answer is two to four sentences. Source in brackets. "Show" = where to click (tab numbers from the navigation guide §1) and the fallback screenshot.

### 3.1 The three rubric-check questions (prepare these first)

From [rubric-check.md](../reviews/rubric-check.md). A reviewer is likely to ask each of them.

| Question | Answer | Show |
|---|---|---|
| **"Your AI reads five labels, and the signal list would be the same without it. What is the AI actually doing, and how often is it wrong where it matters?"** | "On purpose, the AI is the evidence layer today, not the decision layer. It reads 21 sections of 5 labels: 2 oxycodone labels and, since D041 v2, the 3 semaglutide labels behind NAION. For NAION it found diabetic-retinopathy terms and no optic-nerve term, so it agrees with the exact-text and synonym checks, and page 1 shows its quotes word for word. Every AI term carries a quote that code finds word for word, 745 of 745, and on a 35-item key (Boxed Warning + Contraindications of the 2 oxycodone labels, written by Claude, frozen before the run, no pharmacist yet) it found 35 of 35 answer-key items: F1 0.97. The semaglutide sections are not scored. With another month: a pharmacist-scored sample of the long sections, then the other drugs." | Page 1, NAION record → *Labels also read by AI* **3** ([app-1d](../screens/app-1d-naion-ai-read-3.jpg)) and the table *What the AI read in these labels* ([app-1e](../screens/app-1e-ai-quotes-panel-naion.jpg)). Tab 6 → `ai_label_extraction.py` `PILOT_SETIDS` (5 setids) ([hood-code-ai-label-extraction](../screens/hood-code-ai-label-extraction.jpg)). What the AI output looks like: run the Q&A query on `ontology_labeled_reactions` (term, assertion type, grounding = exact, quote) ([hood-labeled-reactions-quotes-sql](../screens/hood-labeled-reactions-quotes-sql.jpg)). Deck slide 10. Sources: eval/ai-eval-v1.md, D041 v2, A012, A019 |
| **"Liraglutide's top 'unlabeled' signal is the disease it treats."** | "Yes. 'Diabetic metabolic decompensation' is liraglutide's rank-1 signal, and it is an indication term (DQ06). We left it, on purpose and on the record: not handled in the pilot. Our D016 v3 buckets tag some efficacy words (HbA1c, 'inadequate control', appetite terms), but not this one. The fix with another month is an indication-term list per drug; until then the pharmacist's triage dismisses it, and we say so on slide 14." | Page 1, unfiltered: row 2, *Liraglutide · Diabetic metabolic decompensation*, rank 1 ([app-1](../screens/app-1-not-in-label-naion.jpg)); or the drug filter → liraglutide. Tab 5 `BUCKETS`, `efficacy` line, to show what is tagged. Sources: DQ06, D016 v3 |
| **"How much of NAION's 394 reports were filed after the news, or by lawyers?"** | "Not measured. Stimulated reporting after news, lawsuits or FDA warnings (DQ04) is a known gap we left; NAION is exactly the kind of signal it affects. We do not filter it; the pharmacist's triage judges it. A reporter-type split would be weak today anyway: reporter type is blank for 34% of Q1 reports and 72% of Q2 (DQ38), and monitoring warns on it. With another month: NAION's reporter-type split as one SQL query, and a flag for spikes near known events." | Tab 5 SQL (monitoring query) → `faers.reporter_type_blank` **warn** ([hood-monitoring-checks-sql](../screens/hood-monitoring-checks-sql.jpg)); drift replay: reporter type blank ×2.1 warn ([hood-monitoring-drift-sql](../screens/hood-monitoring-drift-sql.png)). Deck slide 14. Sources: DQ04, DQ38 |

### 3.2 Architecture

| Question | Answer | Source |
|---|---|---|
| Where is drug identity resolved, and why there? | Once, in `clean_drug_identity` in the clean layer: an exact RxNorm ingredient match after splitting the FAERS ingredient field and stripping salts, never a substring. Every later table joins on the same ingredient ID (RxCUI), so FAERS, labels, recalls and products agree on what "morphine" means. | D020, DQ34, D027, [clean README](../../../foundry/pipelines/clean/README.md) |
| How would another engineer add a drug? | Add it to the formulary list and rebuild raw → clean → curated; nothing downstream is drug-specific. Honest gap: that list is repeated in 5 files today, and production would make it one formulary dataset. | [ripple-table.md](ripple-table.md) row 4 |
| Why is triage an Action and not an editable column? | A create-only Action keeps a full audit trail: the system sets who and when, and nothing is overwritten. Decisions live as Ontology edits, so a pipeline rebuild cannot erase them; 2 test decisions survived the baseline-gate rebuild. | D040, [ontology README](../../../foundry/ontology/README.md#action-types), [baseline-gate](../baseline-gate.md) |
| What happens to her decision if the evidence changes? | The decision keeps the evaluation id it was made on and stays linked to the signal (the link uses the signal key). The signal gets a new id. The screen does not flag the mismatch yet; she compares the id in the decisions table with the one the triage form shows. | [ripple-table.md](ripple-table.md#what-happens-to-an-existing-triage-decision) |
| Was there a mistake in the Ontology? | Yes: a second Signal → Drug link added by mistake on 5 November. We checked no Workshop variable used it and deleted it on 6 November; 10 MSSM link types remain. | [ontology README](../../../foundry/ontology/README.md#link-types) |

### 3.3 Optimization

| Question | Answer | Source |
|---|---|---|
| Why keep an incremental pipeline that is slower? | It gives exactly the same rows as the full rebuild (EXCEPT ALL = 0 both ways), but at 2 quarters it took 88 s against 32 s, because writing three state datasets and a quarter log costs more than parsing one quarter. So signals still read the full rebuild, and we re-measure at 4 or more quarters. | O2, D044, A015 |
| How do you know the LLM is not re-run? | The cache key is the label text hash plus the setid, version, section, prompt, parser and model versions, and each row records `from_cache`. On the first rebuild, all 9 v1-pilot sections came from cache: 0 model calls, 0 tokens. After adding the 3 semaglutide labels (12 new sections, 12 calls), a forced rebuild took all 21 from cache: 0 calls (O1b). | O1, O1b, `ai_label_section_extractions` |
| Did you partition anything? | No, on purpose (D048): the largest table has 2,554,017 rows and clean builds take at most 32 s. We revisit, partitioning FAERS by quarter and signals by drug, when FAERS holds 8+ quarters or a build passes 5 minutes. | D048, numbers.json |
| What did O3 actually save? | XML **downloads** went from 1,321 to 2 per build (1,319 reused); the about 30 index pages are still pulled every build. The DailyMed build went from 3 m 23 s to 1 m 23 s. One run each, and the baseline is not back-to-back. | O3, D047 |
| What did not help? | Incremental FAERS (slower at 2 quarters) and reading fewer FAERS columns (12.3–13.0 s → 12.2 s locally, so we reverted it). Both stay in the log because a failed attempt is evidence too. | O2, O3a |

### 3.4 Data judgment

| Question | Answer | Source |
|---|---|---|
| What was the worst data problem? | FAERS re-sends cases as new versions and deletes old ones, so simply appending quarters gave 8.7% phantom rows. We keep the highest version of each case and apply deletes to all history: Q2 replaced 26,681 cases and deleted 655. | DQ36, D022, numbers.json |
| What did you leave unfixed? | Indication terms (DQ06: liraglutide's rank-1 signal) and stimulated reporting (DQ04) are left and named. Reporter type went from 34% to 72% blank between quarters (DQ38): we do not guess it, we monitor it and show "unknown". Two DailyMed labels answer "None" with HTTP 200, and we keep them flagged without XML (DQ42). | DQ04, DQ06, DQ38, DQ42 |
| Why no MedDRA groupings? | MedDRA needs a licence and this is a public-data build. Keyword buckets stand in for it: they tag, never delete, and they are reviewed by hand. | D016 v3 |
| What are "mass reports"? | Reports listing 30 or more drugs, often the same patient filed again and again. They are left out of the main count but counted separately, and a signal carried mostly by them gets a caution instead of a rank. | D023 v2 |
| What if the FAERS feed changes? | The FDA replaced FAERS with AEMS in March 2026. We use the published quarterly files; how future quarters will arrive is not verified. | DQ20 |

### 3.5 Application

| Question | Answer | Source |
|---|---|---|
| How does she know a flag is real? | Each signal shows its counts, PRR with confidence interval, and on page 1 the exact reference label versions searched, with DailyMed links (for NAION: Ozempic v20, Wegovy v19, oral Ozempic v14); she can open the label and search it herself, as in A4. At the gate we re-derived 5 random flags by hand from the FAERS rows and label text: 5 of 5 matched. | [baseline-gate](../baseline-gate.md) trace, [app-1c](../screens/app-1c-labels-searched-naion.jpg) |
| Isn't NAION already known? What did this tool tell me? | Yes, it is a known positive. EMA's PRAC concluded on 6 June 2025 that NAION is a very rare side effect of semaglutide, and WHO issued an alert on 27 June 2025; the 3 US label versions we search still do not mention it. We lead with it because a monitor that missed it would be broken: ours ranks it first from FAERS alone. Whether we would have flagged it earlier is unproven, because the backtest was cut (D031). | DECISIONS learning 2026-11-05, D031. Show: A3 panel, A4 DailyMed search |
| Can I see the 394 reports before I take this to P&T? | Not from her screen yet. Today their case IDs come from a SQL query on `clean_faers_drug_reaction` (the baseline gate lists examples), and reporter type is blank for 72% of Q2 reports (DQ38). A case list on the signal is the first thing we would add. | [baseline-gate](../baseline-gate.md), DQ38 |
| Which of the 126 recalls touch product on my shelves? How many are Class I? | We cannot know her shelves without purchasing data. *Matched to our products* means the 658 FDA-listed products we track (foundry README, `ontology_product_products`), matched through NDC codes in the recall text. Sorting by class puts Class I first; the active Class I count is [rehearsal count, or "not measured"]. | navigation guide A6 and checklist #9. Show: page 2, Class column; [app-2](../screens/app-2-recalls.jpg) shows D-0788-2026 (Class I) |
| 1,073 is far too many to review. | It is a review queue, ranked within each drug, not a list of findings. It came down from 1,355 at step 9 through the synonym table and buckets, and a pharmacist review is the next lever. | numbers.json `ranked_history` |
| Is the 2-minute morning target met? | "Under two minutes" is a design target. The only measured numbers are machine timings: the Morning brief loads in 11.5 s and each page switch takes 0.8–2.4 s (browser script, View mode, 2026-11-05). A person timing it with a stopwatch happens in rehearsal; quote that time only if it was done. | numbers.json `app.timing_s`, A016, COMPASS |
| Is NAION caused by semaglutide? | We do not claim that: a signal means disproportionate reporting plus "not found in the label". We say "reported, not on the US label", never "caused by". | A003 |
| Does card 3 mean "since yesterday"? | No: it counts the last 30 days (26 on 5 November). Page 3's date range is how she narrows to "since my last review". A label row says a version took effect, not what changed (she opens Recent Major Changes on DailyMed); signals change only with each FAERS quarter, about 130 days behind. | A016, D045, monitoring `faers_age_days` |

### 3.6 AI reliability

| Question | Answer | Source |
|---|---|---|
| How often is the extraction wrong? | Grounding: 745 of 745 quotes across all 21 sections (5 labels) are word for word in the label (448 of 448 on the 9 v1-pilot sections). Accuracy, on a 35-item answer key from the Boxed Warning and Contraindications of the 2 oxycodone labels (written by Claude, frozen before the run, no pharmacist yet): it found 35 of 35 answer-key items with at most 2 extras, F1 0.97, which meets the D015 target of 0.85 on this pilot key only; the benchmark comparison D015 asks for was not run (it stays cut, D031). The long sections and the semaglutide sections are not scored. | [eval](../../../eval/ai-eval-v1.md), D015 |
| Would you notice if it got worse? | Every build checks the grounded rate (fail below 0.95), parse errors and cache hits. A prompt or model change creates new cache keys, so every section is re-extracted and re-scored against the frozen key before we accept it. The drift series today is a historical replay, labelled as such. | A017, D046, D009 |
| Does the AI change the signal list? | Not today: for all 5 labels it reads, text matching already finds every term the AI finds (signals unchanged after D041 v2). Its value now is the exact quote as evidence, shown on page 1. | A012, A019, eval |
| What did prompt v1 get wrong? | It grouped terms, so it found only 11 of 35 answer-key items. Prompt v2 asks for one reaction per item, and it found 35 of 35. | eval, numbers.json |

### 3.7 Communication

| Question | Answer | Source |
|---|---|---|
| What would you do with another month? | Name a pharmacist who signs off the synonym table, the AI answer key and the top signals, through the same create-only Action. Then score the long label sections, widen the AI to the other drugs' labels, schedules, live drift, a health page, and second-opinion sources (PubMed, ClinicalTrials.gov, FDA safety communications, OnSIDES, Orange Book). | [another-month](../../09-roadmap/another-month-sources-and-pharmacist-review.md) |
| Which decisions are final? | The log runs D001–D048. On 6 November the owner accepted the last 12 open decisions in one batch: D006, D015 (the F1 ≥ 0.85 target only), D025, D026, D027, D028, D029, D037, D045, D046, D047 and D048, plus D041 v2. All were already built and running. | DECISIONS.md, deck backup B6 |
| What did you choose not to do? | No ClinicalTrials.gov ingest, no schedules, AI on 5 labels only (2 oxycodone, 3 semaglutide), no MedDRA, and no patient data. The brief says to cut breadth before depth, so we did. | D031 cut list, COMPASS |
| Why 13 drugs in two classes? | 8 opioids and 5 GLP-1s: the two classes cover each other's gaps, and 13 drugs keeps every flag traceable by hand. | D014, A003, D018 |
| Where do I start reading? | R00 "Start here" (`docs/11-handin/reports/pdf/R00-start-here.pdf`). | R00 |

## 4. The 5 riskiest moments and plan B

| # | Moment | What can go wrong | Plan B | Screenshot |
|---|---|---|---|---|
| 1 | **1:30 Morning brief first load** | Cards spin (first load took 11.5 s in the timed run on v0.9.0); the session has timed out | Pre-warm all 4 tabs 5 minutes before. If it still spins for more than 10 s, show the screenshot and keep talking; come back to the live app at A2 | [app-0](../screens/app-0-morning-brief.jpg) |
| 2 | **5:20 Triage form** | Form slow to open; someone presses Submit by mistake | Default is Cancel. If the form does not open in 10 s, show the screenshot and say the same words. A Submit by mistake cannot be undone: say so plainly ("it is now on record; this is what create-only means") and move on | [app-1b](../screens/app-1b-triage-action-form.jpg) |
| 3 | **8:30 Data Lineage** | Graph slow, or it re-lays itself out into a tangle | Lay it out during setup and do not touch Layout. If it is messy, switch to the screenshot, which has the same nodes | [hood-data-lineage](../screens/hood-data-lineage-signals.jpg) |
| 4 | **12:30–17:30 Code repo and SQL (optional switches)** | Repo still "Starting Python server"; SQL panel slow; an accidental keystroke edits code | Open 10 minutes early and pre-run both queries. Never type in the editor: if you do, close the tab without committing. If slow, stay on the slide | [hood-code-repo](../screens/hood-code-repo-ontology-signals.jpg), [hood-ai-extractions](../screens/hood-ai-extractions-cache-sql.jpg), [hood-monitoring](../screens/hood-monitoring-checks-sql.jpg) |
| 5 | **Numbers on screen differ from the slides** | Card 3 is a sliding 30-day window (26 on 5 Nov); someone rebuilt raw pulls, so card 1 or 2 moved | Say it first: "on 5 November this was 26; it is a sliding window". Do not rebuild raw on demo day. If cards 1 or 2 moved, say "the data refreshed since our baseline; the numbers on the slides are from 5 November" | numbers.json |

**Lesser risks (one line each):** Object Explorer search is slow → the search is pre-run in tab 4, fallback [hood-object-explorer](../screens/hood-object-explorer-naion-links.jpg). Health tab shows "No results yet" → force-build the day before, fallback [hood-data-health](../screens/hood-data-health-signals.jpg). DailyMed link opens slowly at A4 → say the same words over app-1c (the version and date are on screen) and use the rehearsal screenshot of the search. openFDA tab fails at A6 → skip it; the panel's "openFDA as of" date names the record we copied. Wi-Fi drops → switch to the backup Preview window with all screenshots (navigation guide §1) and finish from slides and screenshots.
