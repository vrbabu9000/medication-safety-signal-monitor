# Speaking script — MSSM hand-in demo (20:00)

_🖼️ Deck Designer view · v1, 2026-11-05 · estimate, not yet rehearsed_

**Deck:** [MSSM-demo-deck.pptx](MSSM-demo-deck.pptx) (16 main slides; backups B1–B12 = slides 18–29). **Agenda:** [AGENT-BRIEF.md](../AGENT-BRIEF.md) "The 20-minute demo" (binding). **Click-by-click path in Foundry:** the demo navigation guide in [../demo/](../demo/) (demo director). This script gives the words; the guide gives every click.

**How to read this file**
- Each slide has a time slot, the **spoken** words (quoted, `>`), and **cues** in bold: **[SWITCH TO APP]**, **[CLICK …]**, **[BACK TO DECK]**.
- Only quoted text is said aloud. Background, evidence and likely questions are in [slide_explanations.md](slide_explanations.md) under the same anchor.
- Numbers said aloud are the ones on the slide (from [numbers.json](../numbers.json)). Say "about" only where the slide says so.

**Timing.** About 2,250 spoken words at ~125 words per minute ≈ 18 min, plus ~2 min of clicking, page loads and pauses (mostly in the app parts, slides 3–7; measured page switches are 0.8–2.4 s, the brief loads in 11.5 s) = **about 20 min**. The tightest slots are slides 8–16 (spoken words nearly fill each slot); slides 4–7 have the most slack for slow page loads. A timed rehearsal should replace this estimate. Each slot below ends at the agenda time. If the app is slow, stay on the slide: its screenshot shows the same screen; say "here is the same screen captured this morning".

**Words to say the same way every time**
| Say | Not |
|---|---|
| "signal" = reported more often than for other drugs **and** not found in the label, or only possibly in label (108: found only through a close synonym) | "side effect caused by" |
| "review queue" for the 1,073 | "1,073 findings / problems" |
| "the officer" / "she" | "the user" |
| "decision" (Triage Decision object) | "comment", "note" |
| "proposed" for the 12 open decisions (D006, D015, D025–D029, D037, D045–D048) | "decided" |
| "active recall" = status Ongoing | "not terminated" |
| "matches none of the 658 FDA-listed products we track for our 13 drugs (we have no purchasing or inventory data)" | "products we carry", "our products" |
| "built to answer three questions in one screen; machine load 11.5 s" | "answers three questions in under two minutes" |
| "found 35 of 35 answer-key items" | "recall 35/35" (confusable with FDA recalls) |
| "1,355 at step 9" when quoting where the queue started | "1,355 originally" |

| Time | Slide | Where |
|---|---|---|
| 0:00–1:30 | 1–2 | slides |
| 1:30–7:30 | 3–5 | **app** (Workshop pages 0–3) |
| 7:30–11:30 | 6–7 | slides + Data Lineage, Ontology Manager, Object Explorer |
| 11:30–13:30 | 8–9 | slides (optional code repo) |
| 13:30–15:30 | 10–11 | slides (+ optional SQL) |
| 15:30–17:30 | 12–13 | slides |
| 17:30–19:00 | 14 | slide (+ optional monitoring row) |
| 19:00–20:00 | 15–16 | slides, then Q&A |

---

<a id="s01"></a>
## Slide 1 · Medication Safety Signal Monitor — 0:00–0:20
> Good morning. This is the Medication Safety Signal Monitor: one screen that a hospital pharmacy safety officer opens each morning. It answers three questions, and every flag on it traces to its source: the label versions searched and the FDA recall record open in one click; the FAERS case reports are reachable by query, not yet from her screen.

<a id="s02"></a>
## Slide 2 · Her three morning questions, and one trust rule — 0:20–1:30
> Today she hears about drug safety problems late, from FDA emails or from colleagues. Each morning she wants three answers. One: which drugs have side effects being reported that their label does not mention? Two: which of my drugs are under an active recall? Three: what changed since I last looked?
>
> And one rule above all: she has to trust it. Every flag must trace back to its source — the label text we searched, the recall record, and, by query today, the reports behind it.
>
> We kept the scope narrow so it works end to end: 13 drugs, 8 opioids and 5 GLP-1 drugs like semaglutide. Public data only, no patient data. Four sources: FAERS, the FDA's database of side-effect reports; DailyMed, the official labels; openFDA for recalls; and RxNorm, the standard drug names that join them all.
>
> Let me show you her morning first, in the app.

---

<a id="s03"></a>
## Slide 3 · Morning brief — 1:30–3:00 · **[SWITCH TO APP]**
**[SWITCH TO APP]** Workshop module *MSSM Safety Officer*, tab **Morning brief**.
> This is page zero, the morning brief. Three numbers, one per question. 1,073 signals not in the label, ranked. 126 active recalls across our 13 drugs — active means the recall's status is Ongoing. 26 change events in the last 30 days; on page 3 she narrows that to "since my last review".
>
> One word on the first number: 1,073 is a review queue, not 1,073 findings. I will come back to that.
>
> **[POINT at the "Data as of" table]** How fresh is each source? They run on different clocks. FAERS comes out quarterly, so the newest reports end with 2026 Q2; our freshness check puts that at 130 days old. Recalls from openFDA were 8 days old. DailyMed publishes labels daily and openFDA updates recalls weekly; our pipeline refreshes when a build runs, and there is no schedule yet. So the screen does not pretend everything is fresh: it says how old each source is.
>
> And it is quick: in a timed run the brief was on screen in 11.5 seconds, and each page switch took between 0.8 and 2.4 seconds. That is machine timing; a human walk-through will be timed in rehearsal.
>
> Now question one.

<a id="s04"></a>
## Slide 4 · Not in label — 3:00–6:00 · app page 1
**[CLICK tab 1 · Not in label]** (unfiltered: each drug's rank 1 is visible)
> Before I filter, look at the top rows. Some are not plausible drug effects. **[POINT: row 5]** Morphine's rank 1 is Ewing's sarcoma, a bone cancer — most likely that reflects the patients who get morphine, not the drug. Some others are the disease the drug treats; that is a known gap we have not handled. This is why 1,073 is a review queue.
>
> **[CLICK drug filter → semaglutide]** Now semaglutide, sold as Ozempic and Wegovy. **[CLICK the NAION row]** Its top signal is NAION — sudden vision loss from poor blood flow to the optic nerve.
>
> The evidence: 394 of 20,892 semaglutide reports name NAION. The PRR is 112.5: NAION is about 112 times more common among semaglutide's reports than among other drugs' reports. That is a reporting pattern, not 112 times the risk, and news coverage can inflate it.
>
> And NAION is not a discovery. Europe's safety committee, PRAC, concluded in June 2025 that NAION is a very rare side effect of semaglutide, and WHO issued an alert that month. We lead with it because a monitor that missed it would be broken. From FAERS alone, ours ranks it first — and the three US labels she uses still do not mention it.
>
> **[SCROLL to “Reference labels searched”]** These are the three labels we searched: Ozempic version 20, Wegovy version 19, oral Ozempic version 14. Our exact-text check and reviewed synonyms find NAION in none. **[POINT: Labels also read by AI: 0]** The AI has not read these labels, so it did not clear this one. **[CLICK the Ozempic v20 DailyMed link → Cmd+F “optic”]** This is Ozempic's label on DailyMed itself. I search for "optic": no optic neuropathy. She can repeat that check in ten seconds.
>
> What she cannot do yet is open the 394 reports from this screen. We pull their case ids by query today; that is the first thing to add.
>
> **[BACK to the app → CLICK Triage this signal]** To decide, she clicks "Triage this signal": the signal is locked, she picks a decision and writes why. It is saved with the user and the time (the user shows as an ID, not a name), never overwritten. Today only the project owner can submit. **[CLICK Cancel — or Submit only if agreed]**

**Rehearsal check (must pass before the demo):** on the Ozempic v20 page, the "optic" search must not land on the diabetic retinopathy warning. If it does, search "ischemic optic" instead and say so.

<a id="s05"></a>
## Slide 5 · Recalls and what changed — 6:00–7:30 · app pages 2–3
**Before the demo:** open a browser tab with the openFDA enforcement record for D-0040-2027: `https://api.fda.gov/drug/enforcement.json?search=recall_number:"D-0040-2027"` (the same record the pipeline reads).

**[CLICK tab 2 · Recalls]** (check the filter shows Is Active = Yes; click it if not)
> Question two. 126 open FDA recalls — status Ongoing — name one of our 13 ingredients. Most are compounded products. **[CLICK D-0040-2027]** The newest, D-0040-2027 from October 21, is a compounded tirzepatide vial. It matches none of the 658 FDA-listed products we track for our 13 drugs. We have no purchasing or inventory data, so if she buys compounded GLP-1s, she checks her own records. **[SWITCH to the openFDA tab]** Here is the FDA's own record: same number, same product. **[BACK → CLICK the Classification column]** And Class I, the most serious, comes first when she sorts.

**Rehearsal check (not measured):** count the active Class I rows after sorting, and say the number only if it was counted in rehearsal.

**[CLICK tab 3 · What changed]**
> Question three. Every change is an event with a date: 900 recalls reported, 767 terminated, 1,231 label versions taking effect — the 1,231 of 1,321 label versions that carry an effective date — all dated by the source. **[SET Start date = the day of the last review, or the “past month” preset]** "Since my last review" is this start date; the past month gives 26 events, the same as the morning brief.
>
> Two limits. A label row says a new version took effect, not what changed in it; she opens the label on DailyMed for that. And signals change only with each FAERS quarter, about 130 days behind.
>
> **[BACK TO DECK]** That is her morning. Now, how does the data get there?

---

<a id="s06"></a>
## Slide 6 · Architecture — 7:30–9:30 · **[SWITCH: Data Lineage]**
> This is the one-page picture from our architecture note. Four public sources come in on the left. Foundry — Palantir's data platform — stores each as a dataset, a versioned table, built by a transform, which is Python code in a Code Repository.
>
> There are four layers. Raw keeps each reply exactly as the source sent it. Clean is where the important decision lives: drug identity is resolved once, in one dataset, clean_drug_identity. Every drug name in FAERS is mapped to an RxNorm ingredient id, then to products and packages. Every later step joins on that, so no one matches drug names twice. Curated holds the statistics, signals, change events and monitoring. On top sits the Ontology, and the app reads only the Ontology.
>
> Below, the Ontology, which I show next. Dashed boxes are the incremental or cached parts; I will come back to them under optimization.
>
> **[SWITCH: Data Lineage on ontology_signal_signals]** Here is the same thing live: Foundry draws which dataset feeds which. From the raw FAERS quarter files and the DailyMed XML, through clean_drug_identity, to the signals the officer just saw.
>
> **[BACK TO DECK]** (Fallback: backup B12 has this lineage screenshot.)

<a id="s07"></a>
## Slide 7 · Ontology — 9:30–11:30 · **[SWITCH: Ontology Manager → Object Explorer]**
> The Ontology turns tables into things the officer understands. An object type is a business thing backed by one dataset: Drug, Product, Label, Recall, Signal, and so on — ten in all. A link type is a typed relation: many signals belong to one drug; a signal has one statistics record. And an Action is the only way to write.
>
> Our one Action creates a Triage Decision. It is create-only, so past decisions are never edited. Decisions live in their own object type, so rebuilding the signals does not erase them. Two have been saved so far, and both survived a full rebuild.
>
> One honest note: in step 11 I added a second Signal-to-Drug link by mistake. Nothing uses it. It is flagged on the diagram and left for the owner to delete.
>
> **[SWITCH: Ontology Manager → MSSM Signal]** Here is the Signal type: 1,952 objects, its properties. **[SWITCH: Object Explorer → search the NAION signal → Links]** And here is the NAION signal again, from the other side: linked to its statistics record and to its drug. That is the trust rule as data.
>
> **[BACK TO DECK]**

<a id="s08"></a>
## Slide 8 · From one FAERS report to a ranked signal — 11:30–12:50
> How do we get from one FAERS report to that signal? Four columns.
>
> A: clean the reports. FAERS sends new versions of old cases in later quarters, so we keep only the latest version and apply deletes to the whole history. We count only drugs marked as suspects, never drugs the patient just happened to take. Drug names match an exact ingredient, never a substring — "morphine" must not match apomorphine. And duplicate reports of the same patient, plus mass reports listing thirty or more drugs, leave the main count.
>
> B: a two-by-two table for each drug and reaction, then the PRR and the Evans rule.
>
> C: is it in the label? Three checks. In code the order is: an AI term with a quote, then the exact text, then the reviewed synonym table.
>
> D: sort. Only clinical reactions are ranked. Things like "product use error" or "drug ineffective" stay visible, tagged, but not ranked.
>
> **[Optional SWITCH: Code Repository → ontology_signals.py, first lines]** Each rule is a written decision with a number, in the code header too.

<a id="s09"></a>
## Slide 9 · A review queue, not findings — 12:50–13:30
> Here is the funnel: 14,921 drug-reaction statistics, 1,952 signals, 1,073 ranked. On the right, the ranked queue after each label-check or bucket change: 1,355 at step 9, our first full build, then 1,210, 1,115, and 1,073 — 21% shorter. Nothing was deleted; each signal keeps its status. 108 are "possibly in label" and kept, never ranked.
>
> The synonym table has 258 rows. Claude drafted the bands; a pharmacist has not reviewed them. We used it because the proper dictionary, MedDRA, needs a licence we do not have.

---

<a id="s10"></a>
## Slide 10 · AI reliability — 13:30–14:45
> The AI part. Claude Sonnet 5.5, through Foundry's AIP, read 9 label sections from 2 pilot labels and listed each side effect with an exact quote.
>
> Grounding: code checks every quote is in the label text — 448 of 448 are. Accuracy, on a small answer key only — 35 items from the short sections of the two oxycodone labels, written by Claude before the model ran: it found 35 of 35 answer-key items, so F1 is 0.97 against our proposed target of 0.85 (D015) — met on this pilot key only; the benchmark comparison was not run.
>
> Now the honest part. No pharmacist has checked that key, and the long sections are not scored. And the AI does not yet meet the screen: it read only the two oxycodone pilot labels, so for NAION the record says "labels also read by AI: 0", and it does not change the signal list. We chose not to widen a model we cannot yet score independently. Widening it and adding a quote panel is the next decision.

**[Optional SWITCH: Code Repository → ai_label_extraction.py, cache key lines; or the AI-cache SQL]** (fallback screenshot `screens/hood-code-ai-label-extraction.jpg`; guide stop H9)

<a id="s11"></a>
## Slide 11 · Monitoring — 14:45–15:30
> Every build appends 21 checks to a monitoring table: keys, row counts, freshness, AI grounding, cache hits. Plus 4 Foundry Data Health checks that alert the owner.
>
> A rebuild with no new data added zero change events, so the pipeline makes no false alarms of its own. On its first runs it caught two real shifts. FAERS reports with no reporter type jumped from 34% in Q1 to 72% in Q2, so we show "unknown" instead of guessing. And recalls for our drugs more than tripled: 10 in the last four weeks against 3 before. Honest limit: that drift is a replay from source dates, not weeks of live builds.
>
> **[Optional SWITCH: monitoring_checks in SQL, or the signals dataset → Health tab]**

<a id="s12"></a>
## Slide 12 · Optimization log — 15:30–16:45
> Optimization. Our rule: measured, not asserted. Four tries, every one with a before and an after.
>
> O1, the AI cache: 9 model calls and about 71 thousand tokens became zero on a rebuild. Helped.
>
> O2, incremental FAERS: 88 seconds against 32 for the full rebuild — 2.75 times slower. Did not help. Next slide says why.
>
> O3, reusing DailyMed label XML we already hold: 3 minutes 23 down to 1 minute 23, and 1,321 XML downloads down to 2 — the index pages are still pulled every build. Helped.
>
> O3a, parsing fewer columns: 12.3 to 13 seconds became 12.2, locally. Not worth it; reverted.
>
> The pattern: skipping work whose input did not change pays. And partitioning: we chose not to. The largest table has 2.55 million rows and clean builds take at most 32 seconds, most likely start-up (not measured separately). We revisit at eight quarters or a five-minute build. Caveat: each timing is one run.

<a id="s13"></a>
## Slide 13 · Incremental FAERS — 16:45–17:30
> The incremental path reads only the new quarter and merges it into a kept state: three state datasets and one quarter log. It is correct: its output equals the full rebuild row for row — 792,346 cases, zero differences both ways. But at two quarters it is slower: 62 seconds for the state plus 26 for the outputs, against 32 for re-reading everything. The fixed cost is bigger than the work saved. So it runs beside the full rebuild, and signals keep reading the full rebuild. We re-measure at four or more quarters.

**[Optional SWITCH: clean_faers_inc_log preview — one row per quarter]** (fallback screenshot `screens/hood-faers-inc-log-sql.png`; guide stop H12)

---

<a id="s14"></a>
## Slide 14 · Data judgment — 17:30–19:00
> The brief warned that the data is messier than its documentation. Four messes would have changed her answers.
>
> One: FAERS updates and deletes old cases in later quarters. In Q2 alone, 26,681 Q1 cases were replaced and 655 deleted. Simply appending quarters would have counted phantom rows.
>
> Two: the same patient filed by many companies, and reports listing dozens of drugs. They made odd signals. They now leave the main count but stay as evidence.
>
> Three: reporter type went blank — 34% to 72%. We show "unknown".
>
> Four: DailyMed sometimes answers "success" with the word "None" instead of a label — 2 of 1,321. We keep the reply, mark it, and retry.
>
> And noise we left, said plainly: some "reactions" are the disease the drug treats — liraglutide's top signal is diabetic metabolic decompensation — and reports spike after news or lawsuits. We did not filter these; the pharmacist's triage decides.
>
> What we chose not to do: no MedDRA licence, so a reviewed synonym table instead. No patient data. And we cut ClinicalTrials.gov, OnSIDES and daily FAERS to go deep, not wide.
>
> **[Optional SWITCH: monitoring_checks row faers.reporter_type_blank]**

<a id="s15"></a>
## Slide 15 · Another month — 19:00–19:40
> With another month, the biggest gap is not data. It is a named pharmacist. Today only Claude has checked the synonym bands, the answer key and the ranked signals. So: Claude prepares an evidence packet with links; the pharmacist decides; a create-only Action records who, when and which evidence; the pipelines rebuild. Then schedules, live drift over three to four weeks, and a health page.

<a id="s16"></a>
## Slide 16 · What to take away — 19:40–20:00
> Three things. It answers her three questions, and every flag traces to its source: the label versions searched and the FDA recall record open in one click; the FAERS case reports are reachable by query, not yet from her screen. It is built to be extended, and we sped up only what we measured. And we say what is not proven yet — including that the AI has not read the hero drug's labels. Thank you — happy to take questions.

---

## Q&A jump table
In PowerPoint slide show, type the number and press Enter. Type 16 and Enter to return to the close.

| Question is about | Go to |
|---|---|
| Where to add a drug, source, synonym, check | B1 (18) |
| Full incremental design; O1 tokens | B2 (19) |
| Identity and counting rules (D020–D023) | B3 (20) |
| How a flag is traced; write-back safety | B4 (21) |
| AI scoring; noticing it getting worse | B5 (22) |
| Which decisions are final | B6 (23) |
| "If I change X, what changes?" | B7 (24) |
| How "what changed" is computed | B8 (25) |
| Who is alerted, what is not built | B9 (26) |
| Why not DrugBank / MedDRA / ClinicalTrials.gov | B10 (27) |
| The demo order | B11 (28) |
| "Isn't NAION already known?" | Yes — say so: EMA/PRAC called it a very rare side effect of semaglutide on 6 Jun 2025; WHO alert 27 Jun 2025. The 3 US labels we search do not mention it. Finding it from FAERS alone checks that the monitor works; it is not a discovery (slide 4) |
| "Where do I start reading?" | R00 "Start here" (`docs/11-handin/reports/pdf/R00-start-here.pdf`), named on slides 16 and 17 |
| Live Foundry is down | B12 (29) |

## If time runs short
Cut in this order (agenda slots stay intact): the optional SWITCH stops on slides 8, 10, 11, 14 → the Object Explorer half of slide 7 (say "backup B4 shows it") → slide 13 to one sentence ("correct, slower at two quarters, so not switched on").
