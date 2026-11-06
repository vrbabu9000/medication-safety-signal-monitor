# Demo navigation guide: 20 minutes, stop by stop

_🎬 Demo Director view · 2026-11-05, refreshed 2026-11-06 for D041 v2 (A4 ends on the page-1 AI-quotes table; Workshop v0.10.0; timings were measured on v0.9.0) (Phase D fix pass + 💊 safety-officer review, [safety-officer-demo.md](../reviews/safety-officer-demo.md)) · design-thinking stage: **Test** · PDF: [R09-demo-navigation-guide.pdf](../reports/pdf/R09-demo-navigation-guide.pdf)_

**New to the project? Start with [R00 "Start here"](../reports/pdf/R00-start-here.pdf)**, then come back.

**TL;DR.** Part A (0:00–7:30) is the safety officer's morning in the Workshop app: three numbers, the noise in the queue named first, the NAION signal (a known positive) with its evidence, the 3 reference labels searched, a live search of the Ozempic label on DailyMed and what the AI read in those labels, the triage form (Cancel by default), recalls traced to the FDA's own record with Class I first, what changed. Part H (7:30–20:00) goes under the hood in the deck's slide order (slides 6–16). Every stop has the click, what you will see, the words to say, the rubric row it proves, a seconds budget and a screenshot to fall back on. Stop codes are **A0–A7** and **H1–H15**, so they never clash with the deck's backup slides B1–B12.

The agenda is binding: [AGENT-BRIEF.md](../AGENT-BRIEF.md) "The 20-minute demo". The spoken words are in [speaking_script.md](../deck/speaking_script.md); this guide gives the clicks and a short key line per stop. Map of stops: [diagram 36 v3](../../diagrams/png/36-handin-demo-map-v3.png). Change → effect map: [ripple-table.md](ripple-table.md). Timing, rehearsal and Q&A: [rehearsal-plan.md](rehearsal-plan.md). Every number: [numbers.json](../numbers.json) (frozen at the [baseline gate](../baseline-gate.md), 2026-11-05 07:50 UTC); other figures name their record in brackets.

**The 13 formulary drugs.** Opioids (8): oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, buprenorphine, tramadol. GLP-1s (5): semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide. Exenatide has no reference label, so signals exist for 12 of 13 (A013).

**What this means for Dana (the safety officer).**
- **The 1,073 is a review queue, not 1,073 findings.** A signal = reported more often than for other drugs (Evans rule, D006) **and** not found in the drug's reference labels, or only possibly in label (108: found only through a medium-band synonym).
- **NAION is a known positive, not a discovery.** EMA's safety committee (PRAC) concluded on 6 June 2025 that NAION is a very rare side effect of semaglutide (WHO alert 27 June 2025). The 3 US label versions we search still do not mention it (DECISIONS learning 2026-11-05). We lead with it because a monitor that missed it would be broken.
- **The AI checked NAION too.** Since 6 Nov (D041 v2) the AI reads the 3 semaglutide labels. It found diabetic-retinopathy terms and no optic-nerve or NAION term, so exact text, synonyms and the AI agree: not in label. Its quotes are on page 1 (*What the AI read in these labels*). The method code `text+ai_v1+syn_v2` names the rule version, not which check found what.
- **"Matched to our products" means the 658 FDA-listed products we track, not her shelves.** We have no inventory or purchasing data.
- **She cannot open the 394 reports from her screen yet.** Their case IDs come from a query today.
- **Card 3 counts the last 30 days**, not "since yesterday". Page 3's date range is how she narrows to "since my last review".
- **Only the project owner can submit a triage decision today.** Giving her that role is a production step. In the demo the form is opened and **cancelled** unless the owner decides otherwise.
- **New signals arrive only with a new FAERS quarter**, and FAERS is about 130 days behind (`monitoring.faers_age_days`).

**Words you will hear** (say them this simply the first time):

| Term | Say |
|---|---|
| Foundry | Palantir's data platform: pipelines, a data model and apps in one place |
| Dataset / transform | A table in Foundry / the Python code that builds one table from others |
| Code Repository | Foundry's built-in code editor + git + build button |
| Data Lineage | Foundry's live graph of which dataset is built from which |
| Ontology / object type / link / Action | The business layer on top of datasets: "Drug", "Signal", "Recall" as things with links between them; an Action is a form that writes a change back |
| Workshop | Foundry's app builder; our app is the module *MSSM Safety Officer* (v0.10.0, 4 pages) |
| AIP | Foundry's AI platform; we call Claude Sonnet 5.5 through it |
| FAERS | The FDA's database of adverse event reports (quarterly files) |
| PRR | Proportional reporting ratio: how much more often this reaction is reported with this drug than with all other drugs |
| Evans rule | A signal needs at least 3 reports, PRR ≥ 2 and chi-square ≥ 4 (D006) |
| MedDRA preferred term (PT) | The standard medical term FAERS uses for a reaction, e.g. "Optic ischaemic neuropathy" |
| DailyMed / SPL | NIH's site for official drug labels / the XML format they come in |
| openFDA | The FDA's public API; we use its recall (enforcement), Drugs@FDA and NDC endpoints |
| RxNorm / RxCUI | NIH's drug naming standard / its ID for one ingredient |
| NDC | National Drug Code: the ID printed on a package |
| Evaluation id | A fingerprint of the evidence behind a signal (report count, PRR, label-check version, FAERS window, labels searched, labels read by AI). It changes when any of those change |

---

## 1. Pre-demo checklist

### The day before (allow 60 minutes, then run rehearsal pass 1)

| # | Check | Pass when | If not |
|---|---|---|---|
| 1 | **Do not rebuild raw pulls.** The demo uses the frozen baseline data so the screen matches the deck and numbers.json | Morning brief shows 1,073 and 126 | If someone rebuilt: re-capture numbers.json before any slide changes (lead) |
| 2 | Data Health results on `Data/curated/ontology_signal_signals` → Health tab | Build status and Primary key both **Passed** ([screen](../screens/hood-data-health-signals.jpg)) | Dataset page → Build ▾ → Force → *Only this dataset*, then re-check (build time not measured; do it the day before) |
| 3 | AI cache rows | SQL on `ai_label_section_extractions` gives 21 rows (5 labels), all `from_cache = true`, `n_reactions = n_grounded` (the [screen](../screens/hood-ai-extractions-cache-sql.jpg) is from 5 Nov and shows the 9 v1-pilot rows) | Use the screenshot; do not rebuild the AI transform on demo day |
| 4 | **Owner's choice for the triage form: Cancel (default) or Submit.** Write it here: ______ | The owner has said which, before the demo | No answer = Cancel. Submit creates a permanent object: the Action is create-only and there is no delete Action |
| 5 | If Submit was chosen: logged in as the **project owner** | Triage form opens (only the owner can submit, [ontology README](../../../foundry/ontology/README.md#action-types)) | Present from the owner's account, or Cancel |
| 6 | Triage decisions: **keep the 2 test decisions** | They are still there (Object Explorer → MSSM Triage Decision) | See note below |
| 7 | Rehearse the triage form by **opening it and pressing Cancel**. Never Submit in rehearsal | NAION's decisions table is still empty | If a rehearsal decision landed anywhere: keep it (cannot be deleted) and tell the lead |
| 8 | **DailyMed check for A4.** From page 1, click the Ozempic v20 DailyMed link, then Cmd+F `optic` | The first hit is **not** the diabetic retinopathy warning, and no optic neuropathy text is found. Note which version DailyMed shows (the link opens the setid, which shows the newest version). Then scroll page 1 to *What the AI read in these labels*: retinopathy rows, no optic-nerve row | If `optic` lands on the retinopathy warning first, search `ischemic optic` instead. If DailyMed shows a version newer than v20, say "DailyMed now shows version N; we searched v20". Capture a screenshot of the search as the A4 fallback (none exists yet) |
| 9 | **Class I count for A6.** Page 2, Is Active = Yes, click the **Class** column header (or pill Classification → Class I) | Write the active Class I count here: ____ (**not measured**). Open D-0788-2026 (Class I, Fresenius Kabi) and write its *Matched to our products*: ____ (**not measured**) | If you cannot count it, do not say a number |
| 10 | **Stopwatch walk-through by a person** of the three morning questions (A1–A7 clicks, reading included) | Time written here: ____ . "Under two minutes" is a **target** (COMPASS North Star); only this person-timed number may be quoted as "timed" | Not done = say "designed for under two minutes, not yet timed with a person" |

**Why keep the two test decisions.** The Action is create-only by design: there is no delete Action, so removing them would mean adding one. They are audit evidence that a decision survives a rebuild (baseline gate). Their rationales say "STEP 6 ACTION SAVE TEST" (on recall D-0338-2026) and "STEP 8 WORKSHOP TEST" (on Oxycodone · Myoclonus), so nobody mistakes them for clinical calls. Neither sits on NAION, so neither appears on screen in Part A.

**One check worth making in rehearsal (not verified yet).** The Myoclonus test decision stores evaluation id `cbcd091262d23bd6`, made at step 8 on 2026-11-04 (A012). The label check has changed twice since (`syn_v1`, then `syn_v2`), so that signal's current id should be different. If it is (open the triage form on Oxycodone · Myoclonus, read the locked id, Cancel), it is a live example of a decision made on older evidence. Use it only in Q&A.

### 30 minutes before

One Chrome window for Foundry, one separate window for the deck (presenter view). Hide the bookmarks bar, turn on Do Not Disturb, close Slack and email. Browser zoom **110%** for the Workshop and dataset tabs, **125%** for the code repository tab (Cmd + / Cmd −). Tabs 1–8 can be reached with **Cmd+1 … Cmd+8**; **Cmd+9** jumps to the last tab (the openFDA record). Third window: **backup** — open all images in `docs/11-handin/screens/` in Preview (sorted by name), so any fallback is one Cmd+Tab away.

| Tab | Open | Leave it showing | Used at |
|---|---|---|---|
| 1 | Workshop module **MSSM Safety Officer** v0.10.0, View mode (project folder `Workshop/`) | Tab **Morning brief**. Then click each of the 4 tabs once to warm them up, and come back | 1:30 |
| 2 | Dataset `Data/curated/ontology_signal_signals` → **Explore pipeline ▾ → Explore data lineage**, expand parents 3 levels | The lineage graph laid out as in the [screen](../screens/hood-data-lineage-signals.jpg) | 8:30 |
| 3 | **Ontology Manager → MSSM Signal** | Overview (1,952 objects) | 10:15 |
| 4 | **Object Explorer**, search `Semaglutide · Optic ischaemic neuropathy` | First result clicked, **Links** tab open | 10:45 |
| 5 | Code Repository `Pipelines/pipelines_clean` → `ontology_signals.py` | Lines 22–29 in view (Foundry line numbers) (RULE, MAX_DRUG_ROWS, LABEL_CHECK, WINDOW, BUCKETS). SQL panel with the **monitoring** query already run. Dismiss the VS Code banner | 12:30, 14:45, 17:30 |
| 6 | Same repo, second tab, `ai_label_extraction.py` | The constants block in view (MODEL_ID, PROMPT_VERSION, PARSER_VERSION, PILOT_SETIDS with 5 setids; lines 21–26 in the GitHub mirror, check the Foundry line numbers in rehearsal). SQL panel with the **AI cache** query already run | 13:30 |
| 7 | Dataset `Data/curated/ontology_signal_signals` | **Health** tab | 14:45 (alternative) |
| 8 | Dataset `Data/clean/clean_faers_inc_log` (optional) | Preview: one row per quarter | 16:45 |
| 9 (last tab, Cmd+9) | The FDA's own record of the newest recall: `https://api.fda.gov/drug/enforcement.json?search=recall_number:"D-0040-2027"` (the same openFDA record the pipeline reads, `ontology_changes.py` RECALL_URL) | The JSON with recall_number, classification, status, product_description, code_info (lots) | 6:20 |

The code repository takes a while to start ("Starting Python server", "Running Gradle task"). Open tabs 5 and 6 at least 10 minutes early. **Never type in the editor** during the demo: an accidental edit can be committed. The SQL panel is slow, so run the queries during setup and leave the results on screen:

```sql
-- tab 6: AI cache rows (H9)
SELECT label_key, section_name, status, n_reactions, n_grounded, from_cache, prompt_tokens, completion_tokens, called_at
FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/ai_label_section_extractions`
ORDER BY label_key, section_name
```

```sql
-- tab 5: latest monitoring run (H10, H13)
SELECT check_id, area, value, previous, threshold, status, detail
FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/monitoring/monitoring_checks`
WHERE run_at = (SELECT MAX(run_at) FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/monitoring/monitoring_checks`)
ORDER BY status DESC, area
```

```sql
-- Q&A only (AI quote rows; run live only if asked)
SELECT section_name, normalized_term, assertion_type, grounding, quote
FROM `/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/ontology_labeled_reactions`
WHERE section_name = 'Boxed Warning' ORDER BY label_key, normalized_term LIMIT 12
```

### Which signal to pre-select

None. Leave page 1 with no drug filter. You will click the **Ingredient Name** pill and choose *semaglutide* live (it shows the filter works). NAION is then row 1.

### Data freshness: the exact words

"The numbers are frozen from our baseline build on 5 November. FAERS runs through 2026 Q2, the latest quarter the FDA has published; our freshness check puts it at about 130 days old. openFDA recalls were last updated by the FDA on 28 October. DailyMed and RxNorm were pulled on 5 November. Each source has its own clock, and the screen shows each one."

Do not say "live" or "real time". The third card ("Changes in the last 30 days") is a sliding window. It was **26 on 5 November** and will read a different number on another day. Say so before anyone asks.

### Speed: what was measured

Machine timing (numbers.json `app.timing_s`; browser script, time until the expected text is on screen, View mode, 2026-11-05): Morning brief loads in **11.5 s**; page switches take **0.8–2.4 s** (recalls 1.1 s, what changed 0.8 s, signals with the labels panel 2.4 s). Human reading time is not included. These machine timings are the **only measured speed numbers**. "Under two minutes" for her three questions is a **design target**, to be timed by a person with a stopwatch in rehearsal (checklist #10); until then say "designed for under two minutes, not yet timed with a person". The 11.5 s first load is why tab 1 is warmed up before the demo.

---

## 2. Part A — as the safety officer (0:00–7:30)

Stop format: **Click** → **On screen** → **Say** (key line; full words in the [speaking script](../deck/speaking_script.md)) → **Proves** (rubric row) → **Budget** → **Fallback** → **If asked**.

### A0 · The officer's problem (0:00–1:30, 90 s) — deck slides 1–2

- **Click:** deck window, title slide → slide 2.
- **Say:** "Every morning she has three questions: which drugs have side effects being reported that the label does not mention, which have an active recall, and what changed since she last looked. One rule: she trusts only a flag she can trace to its source. 13 drugs, 8 opioids and 5 GLP-1s, public data only, no patient data."
- **Proves:** Communication.
- **Fallback:** none needed (slides).

### A1 · Morning brief (1:30–3:00, 90 s) — deck slide 3, SWITCH TO APP

- **Click:** Cmd+1 (Workshop). Tab **Morning brief** is already open (warmed up: the first load took 11.5 s in the timed run).
- **On screen** ([app-0-morning-brief.jpg](../screens/app-0-morning-brief.jpg)): "Good morning: your three questions". Three cards: **1 · Signals not in the label (ranked) 1073**, **2 · Active recalls (all 13 drugs) 126**, **3 · Changes in the last 30 days 26**. Below, "Data as of: each source updates on its own clock": FAERS through 2026Q2 · RxNorm release 02-Nov-2026 · openFDA source updated 2026-10-28 · DailyMed newest label version. Column **We pulled it at**: FAERS = "quarterly file (no pull time)"; RxNorm, openFDA and DailyMed = the pull time on 2026-11-05.
- **Say:** "One number per question. 1,073 is her review queue, not 1,073 findings: a signal means the reaction is reported unusually often with this drug and we could not find it in the label. 126 recalls are active, meaning status Ongoing. 26 things changed in the last 30 days. Below is the trust part: how fresh each source is."
- **Proves:** Application (three questions, one screen); trust (as-of per source).
- **Fallback:** if the cards spin for more than 10 s, switch to the backup Preview window (app-0) and keep talking.
- **If asked** "why does FAERS have no pull time?": FAERS comes as quarterly files, so the screen says "quarterly file (no pull time)" on purpose; its date is the quarter (`ontology_changes.py`, source status).
- **If asked** "is it fast enough for her morning?": the only measured numbers are machine timings: 11.5 s first load, 0.8–2.4 s per page. "Under two minutes" is a target; quote a time only if a person timed it in rehearsal (checklist #10).

### A2 · Page 1: the noise first, then one drug (3:00–3:40, 40 s) — deck slide 4

- **Click:** tab **1 · Not in label**. **Before filtering**, point at row 5, **Morphine · Ewing's sarcoma** (rank 1 for morphine). Then pill **Ingredient Name** → tick **semaglutide**.
- **On screen** ([app-1-not-in-label-naion.jpg](../screens/app-1-not-in-label-naion.jpg), unfiltered): "Ranked signals (not in label)", columns Signal · Reaction · Rank · Reports · From mass reports (30+ drugs) · PRR · CI low · Chi² · Caution. After the filter: semaglutide only, **Semaglutide · Optic ischaemic neuropathy** at rank 1.
- **Say (before the filter):** "Look at morphine's rank 1: Ewing's sarcoma, a bone cancer. That is almost surely about the patients, not the drug. This is why 1,073 is a review queue, not a list of findings: she dismisses that in one click. Two GLP-1 rank 1s are the drug's own effect or the disease it treats, such as liraglutide's 'Diabetic metabolic decompensation' (DQ06)."
- **Say (after the filter):** "Now one drug: semaglutide, sold as Ozempic and Wegovy. Rank is within each drug. Number one is NAION, optic ischaemic neuropathy: sudden vision loss from poor blood flow to the optic nerve."
- **Proves:** Application.
- **Fallback:** app-1 screenshot (unfiltered: Morphine · Ewing's sarcoma is row 5, NAION row 1).
- **If asked** "why rank per drug?": she reviews drug by drug, and the size of the statistic depends on how many reports a drug has. One ranking across all drugs would let the busiest drug fill the top.

### A3 · The evidence: why NAION is flagged (3:40–4:30, 50 s)

- **Click:** the NAION row. The right panel "Evidence and triage" fills.
- **On screen** ([app-1d-naion-ai-read-3.jpg](../screens/app-1d-naion-ai-read-3.jpg), v0.10.0): Reports: this drug + reaction **394** · All reports for this drug **20892** · PRR **112.5** · 95% CI **92.19–137.24** · Chi² (Yates) **10653.8** · Set aside, mass reports **0** · Label status **not_in_label** · Reference labels searched **3** · Labels also read by AI **3** · Label check method **text+ai_v1+syn_v2** · Rank **1** · Bucket **clinical** · Evaluation id **c4b5da0b64d1e1e6**. The decisions table above it is **empty**: nobody has triaged NAION.
- **Say:** "394 reports name semaglutide and NAION, out of 20,892 semaglutide reports. NAION is about 112 times more common among semaglutide's reports than among other drugs' reports: a reporting pattern, not 112 times the risk. The 95% interval runs from 92 to 137, so it is not a small-numbers fluke, but news coverage can still inflate it (DQ04). And NAION is not new: Europe's regulator, EMA's safety committee, concluded in June 2025 that it is a very rare side effect of semaglutide. We lead with it because a monitor that missed it would be broken. Ours ranks it first."
- **Point, do not read out:** the engineering fields (`not_in_label`, Caution, Chi² (Yates), Bucket). At **Labels also read by AI: 3**, say: "The AI read all three of these labels too. I will show you what it found in a moment."
- **Proves:** Application (trace on screen).
- **Fallback:** app-1d screenshot (same panel, v0.10.0).
- **If asked** "is NAION caused by semaglutide?": we do not claim that. A signal is disproportionate reporting plus "not found in the label"; we say "reported, not on the US label" (A003).
- **If asked** "isn't NAION already known?": yes. EMA's PRAC concluded on 6 June 2025 that NAION is a very rare side effect of semaglutide; WHO issued an alert on 27 June 2025. The 3 US label versions we search (Ozempic v20, Wegovy v19, oral Ozempic v14) still do not mention it (DECISIONS learning 2026-11-05). So it is a known positive: the pipeline should find it, and it does, at rank 1, from FAERS alone. Whether we would have flagged it *earlier* is unproven: the backtest was cut (D031).

### A4 · Reference labels searched, DailyMed itself, then what the AI read (4:30–5:20, 50 s)

- **Click:** scroll the right panel down to **Reference labels searched (click DailyMed link to read the label)**. **Mandatory:** click the **Ozempic v20** DailyMed link → the label opens in a new tab → **Cmd+F** `optic` (or `ischemic optic`, whichever passed checklist #8) → show "no optic neuropathy" → close the tab (Cmd+W) to return to the app → keep scrolling the right panel to **What the AI read in these labels (every line is quoted word for word from the label)**.
- **On screen** ([app-1e-ai-quotes-panel-naion.jpg](../screens/app-1e-ai-quotes-panel-naion.jpg), v0.10.0): three rows, columns Label (product · firm) · Version · Effective · Safety sections searched · Open in DailyMed: **Ozempic v20** (2026-06-01), **Wegovy v19** (2026-06-18), **oral Ozempic v14** (2026-01-30), each with a DailyMed link. Below them the AI table: Reaction Text · Section Name · Quote · Label Key, 297 rows for semaglutide.
- **Say:** "These are the three labels we searched, by exact version, each with a link. Our exact-text check and our reviewed synonym table find NAION in none of them. This is Ozempic's label on DailyMed itself. I search for 'optic': no optic neuropathy. She can repeat this check in ten seconds. Back in the app, this table is what the AI read in the same three labels, every line quoted word for word. It found diabetic retinopathy, which the label does warn about, and nothing about the optic nerve. So three independent checks agree. What she cannot do yet is open the 394 reports from this screen: we pull their case IDs by query today, and that is the first thing we would add before anyone takes this to P&T."
- **Proves:** Application (every flag traces to its source); AI reliability (the AI's quoted evidence on screen).
- **Fallback:** app-1e screenshot (labels + AI table; app-1c shows the labels alone); for the DailyMed search, the screenshot captured in rehearsal (checklist #8). If DailyMed is slow, say the same words over app-1e.
- **If asked** "how does the panel find the labels?": it walks existing links: Signal → Drug → Products → Reference Label, then Label → Labeled Reactions for the AI table. There is no dedicated Signal → Label link type yet.
- **If asked** "how is the label check done?": three checks; in code the order is (1) an AI term with a code-found quote, (2) the exact term or its US spelling in a safety section, (3) a reviewed synonym. The outcome is the same in any order; only the recorded method differs (`ontology_signals.py` l.163–176). For NAION all three ran and none found it.
- **If asked** "is NAION really missing from every label?": across every semaglutide label in DailyMed, none of the 36 safety sections mention it (A014).
- **If asked** "is the AI scored on these labels?": grounding only (745 of 745 quotes found word for word); the answer key covers oxycodone, so the semaglutide sections are not scored.

### A5 · Triage this signal: the Action form (5:20–6:00, 40 s)

- **Click:** **Triage this signal** → form *Create MSSM Triage Decision* opens → point at the locked fields → **Cancel** (default). Only if the owner chose Submit (checklist #4): Decision ▾ **reviewing** → Rationale `Demo: 394 reports, PRR 112.5, not in 3 reference labels. Check FDA safety communications.` → **Submit**, and the row appears in the decisions table above the record.
- **On screen** ([app-1b-triage-action-form.jpg](../screens/app-1b-triage-action-form.jpg), captured and cancelled, nothing saved): Subject Type `signal`, Subject Key `1991302|Optic ischaemic neuropathy|prr_evans_v2`, Evaluation Id `c4b5da0b64d1e1e6` live (the screenshot is from 5 Nov and shows the id before D041 v2, `f55055e199e8e9d3`), filled and locked. Decision (reviewing / dismissed / escalated / monitoring) and Rationale are hers.
- **Say:** "If she decides, she clicks Triage this signal. This is a Foundry Action. The signal and its evaluation id are filled in and locked; she picks a decision and writes why. Who and when are set by the system. Submitting creates a new Triage Decision object; it never edits an old one, and it survives every rebuild. Today only the project owner can submit, so I will cancel."
- **Proves:** Application (a triage button that writes back); trust (audit).
- **Fallback:** form does not open within 10 s: show app-1b and say the same words.
- **If asked** "what happens to her decision when the evidence changes?": the decision keeps the evaluation id it was made on. A later build that changes the counts, PRR, label-check version, window, labels searched or labels read by AI gives the signal a **new** id. The old decision is not edited and stays linked to the signal (the link uses the signal key, not the id), so it still shows in the decisions table. **The screen does not flag it as out of date yet**: she sees it by comparing the id in the decisions table with the id the triage form shows. A bucket change does not change the id ([ripple table](ripple-table.md#what-happens-to-an-existing-triage-decision)).
- **If asked** "has a decision survived a rebuild?": yes: 2 test decisions survived the full baseline-gate rebuild ([baseline gate](../baseline-gate.md)).
- **If asked** "who can submit?": today only the project owner (Action permission). Giving the safety team a role is a production step.

### A6 · Page 2, Recalls (6:00–6:50, 50 s) — deck slide 5

- **Click:** tab **2 · Recalls**. The deck script says Is Active = Yes is preset; check the **Is Active** pill shows it (if not, click it → Yes). Click top row **D-0040-2027** → **Cmd+9** (the FDA's own record, pre-opened) → point at the same recall number and lot → **Cmd+1** back → click the **Class** column header so **Class I** rows come first.
- **On screen** ([app-2-recalls.jpg](../screens/app-2-recalls.jpg)): "Recalls for my drugs (newest first; filter Is Active = Yes)". Right panel "Recall details (from openFDA)": D-0040-2027 · Class II · Ongoing · *Tirzepatide/Niacinamide 2mL vial* · Houston Rx LLC · reason *Lack of assurance of sterility* · FDA report date 2026-10-21 · **Matched to our products 0** · openFDA as of 2026-10-28.
- **Say:** "126 open FDA recalls, status Ongoing, name one of our 13 ingredients. The newest is a compounded tirzepatide vial, reported 21 October. It matches none of the 658 FDA-listed products we track for our drugs: we have no inventory data, so if she buys compounded GLP-1s, she checks her purchasing records. Here is the FDA's own record of it: same number, same lot. And sorted by class, the Class I recalls come first: there are [count from checklist #9] of them." (Say no number if checklist #9 was not done.)
- **Proves:** Application (question 2); Data judgment (honest matching).
- **Fallback:** app-2 screenshot (D-0788-2026, Class I, is visible lower in the list). If the openFDA tab fails, skip it and say "the panel's 'openFDA as of' date is the record we copied".
- **If asked** "which of the 126 touch product on my shelves?": we cannot know without purchasing data. *Matched to our products* means the 658 FDA-listed products (applications) we track, through NDC codes found in the recall text. The Class I count and D-0788-2026's product match are **not measured** unless checklist #9 was done.
- **If asked** "what counts as active?": openFDA status **Ongoing** (`clean_recalls.py` l.69). Completed and Terminated recalls are not active.
- **If asked** "how do you link a recall to a drug?": the ingredient named in the recall text links it to the drug. NDC codes found in the recall's own text link it to products, with high or medium confidence ([clean README](../../../foundry/pipelines/clean/README.md)).

### A7 · Page 3, What changed (6:50–7:30, 40 s)

- **Click:** tab **3 · What changed** → left panel, **Start date** box → preset **Past month** (or the date of her last review). Leave the end date as today.
- **On screen** ([app-3b-what-changed-past-month.jpg](../screens/app-3b-what-changed-past-month.jpg)): "Since my last review: pick dates", Oct 6 – Nov 5, 2026. Table "What changed (newest first)": liraglutide label version 11 effective (Oct 30), fentanyl label versions (Oct 23), recall D-0040-2027 reported (Oct 21) … Entity type counts: **label 15, recall 11** = 26, the same as card 3.
- **Say:** "Every change is an event with a date, dated by the source itself. 'Since my last review' is simply this start date: the past month gives 26 events, the same number as the morning brief. A label row tells her a new version took effect, not what changed in it; on DailyMed she opens the label's Recent Major Changes section. And new signals arrive only with each FAERS quarter, about 130 days behind. So that is her morning today: the sources publish daily (DailyMed) and weekly (openFDA); our pipeline refreshes when a build runs, with no schedule yet; signals move once a quarter."
- **Proves:** Application (question 3).
- **Fallback:** app-3b screenshot (or [app-3-what-changed.jpg](../screens/app-3-what-changed.jpg), unfiltered).
- **If asked** "how do you know the feed has no false alarms?": a rebuild with no new data added 0 events (moved here from the spoken part; H10 / slide 11 territory).
- **If asked** "why no signal changes?": signal changes come only from comparing builds, and nothing has changed between builds yet. They appear after the next FAERS quarter or the next synonym edit ([ripple table](ripple-table.md)).
- **If asked** "could the start date fill itself from her last decision?": not yet. It is a hand-set filter today (D045).

---

## 3. Part H — under the hood (7:30–20:00)

### H1 · Architecture in one picture (7:30–8:30, 60 s) — deck slide 6

- **Click:** BACK TO DECK → slide 6, [diagram 38 v2](../../diagrams/png/38-handin-architecture-onepage-v2.png) (the one-page architecture picture). Detailed fallback if asked: [diagram 30 v3](../../diagrams/png/30-handin-data-flow-v3.png) (every dataset).
- **Say:** "Four public sources. Raw keeps exactly what each source sent. Clean checks and de-duplicates it, and resolves drug identity once, in one dataset: `clean_drug_identity`. Curated holds the statistics, signals, change events and monitoring. The Ontology sits on top, and the app reads only the Ontology."
- **Proves:** Architecture.

### H2 · Data Lineage, live (8:30–9:30, 60 s) — SWITCH: Data Lineage

- **Click:** Cmd+2 (lineage tab, already laid out).
- **On screen** ([hood-data-lineage-signals.jpg](../screens/hood-data-lineage-signals.jpg)): yellow raw nodes (`raw_dailymed_spl_xml`, `raw_openfda_drugsfda`, `raw_rxnorm_related`, `raw_openfda_ndc`, `raw_faers_quarter_files`, source `src_faers_files`) → pink clean nodes → `ontology_signal_signals`.
- **Say:** "This is Foundry's own graph, not a drawing. Follow RxNorm into `clean_drug_identity`. Everything after it, FAERS, labels and products, joins on one ingredient ID. That is 'drug identity resolved once, in the right place'."
- **Proves:** Architecture.
- **Fallback:** the lineage screenshot (deck backup B12), or diagram 30 v3.
- **If asked** "why polars, not Spark?": the clean layer is small enough for lightweight Python transforms (about 1 min vs about 4 min for Spark in our observation, learning 2026-11-04), and the same code runs on a laptop, which is how we test it (A014: Foundry = local).

### H3 · The Ontology in one picture (9:30–10:15, 45 s) — deck slide 7

- **Click:** BACK TO DECK → slide 7, [diagram 31 v2](../../diagrams/png/31-handin-ontology-v2.png).
- **Say:** "Ten object types: Drug, Product, Label, Recall, Labeled Reaction, AE Stat, Signal, Change Event, Source Status, Triage Decision. Only Triage Decision is written, and only through one create-only Action. Ten link types. One we added by mistake, a duplicate Signal-to-Drug link, was deleted on 6 November after we checked nothing used it."
- **Proves:** Architecture.

### H4 · Ontology Manager (10:15–10:45, 30 s) — SWITCH: Ontology Manager

- **Click:** Cmd+3.
- **On screen** ([hood-ontology-manager-signal.jpg](../screens/hood-ontology-manager-signal.jpg)): MSSM Signal · 1,952 objects · 25 properties · Edits disabled · Status Experimental.
- **Say:** "Each object type is backed by one curated dataset. Signal has 1,952 objects. Edits are off: signals come only from the pipeline. The Action lives on Triage Decision, which points at the signal."
- **Proves:** Architecture.
- **Fallback:** screenshot.

### H5 · Object Explorer: follow one flag to its source (10:45–11:30, 45 s) — SWITCH: Object Explorer

- **Click:** Cmd+4 (search already run, NAION selected, **Links** tab) → click **MSSM AE Stat** (the 2×2 counts) → back → **MSSM Drug** → MSSM Products → Reference Label (DailyMed link).
- **On screen** ([hood-object-explorer-naion-links.jpg](../screens/hood-object-explorer-naion-links.jpg)): Links: MSSM AE Stat 1 · MSSM Drug 1 (the 5 Nov screenshot also shows *Drug of signal*, the duplicate link type deleted on 6 Nov). No Triage Decisions link, because the form was cancelled (if the owner chose Submit at A5, **MSSM Triage Decisions 1** also shows).
- **Say:** "The trust rule as data. From the signal to its statistics, the 2-by-2 table of counts. From the drug to its products and the reference label, with the DailyMed link: the same path the page 1 panel walks."
- **Proves:** Application (trace: every flag traces to its source).
- **Fallback:** the Object Explorer screenshot (deck backup B4); the baseline-gate trace table (5 of 5 random flags re-counted by hand from FAERS rows).
- **If asked** "can I see the FAERS case IDs?": with SQL on `clean_faers_drug_reaction` (the baseline gate lists example case IDs). The screen does not link to case rows yet.

### H6 · One FAERS report to a ranked signal (11:30–12:30, 60 s) — deck slide 8

- **Click:** BACK TO DECK → slide 8 ([diagram 32 v3](../../diagrams/png/32-handin-signal-pipeline-v3.png)).
- **Say:** "A: clean the reports. Keep only the latest version of each case and apply deletes to all history; appending quarters gave 8.7% phantom rows (DQ36, D022). Count only suspect drugs (D021). Match names exactly through RxNorm; substring matching added 50% false morphine rows (DQ34, D020). Set aside reports listing 30 or more drugs (D023 v2). B: the 2-by-2 table, PRR and the Evans rule. C: is it in the label? In code: an AI term with a quote, then the exact text, then the reviewed synonym table. D: only clinical reactions are ranked; the rest is tagged (D016 v3)."
- **Proves:** Data judgment.

### H7 · The signal code (12:30–12:50, 20 s) — optional SWITCH: Code Repository

- **Click:** Cmd+5 (`ontology_signals.py`, lines 22–29). First to cut if late.
- **On screen** ([hood-code-repo-ontology-signals.jpg](../screens/hood-code-repo-ontology-signals.jpg)): `RULE = "prr_evans_v2"`, `MAX_DRUG_ROWS = 30`, `LABEL_CHECK = "text+ai_v1+" + SYN_VERSION`, `WINDOW = "FAERS 2026Q1-2026Q2"`, `BUCKETS = [ # keyword stand-in for MedDRA groupings (no MedDRA licence)`.
- **Say:** "Each rule is a named constant with a decision number. The buckets are keyword lists because we have no MedDRA licence, and the code says so."
- **Proves:** Architecture (another engineer can extend it).
- **Fallback:** screenshot.

### H8 · A review queue, not findings (12:50–13:30, 40 s) — deck slide 9

- **Click:** BACK TO DECK → slide 9.
- **Say:** "14,921 drug-reaction statistics, 1,952 signals, 1,073 ranked. The ranked queue after each label-check or bucket change: 1,355 at step 9, our first full build, then 1,210, 1,115 and 1,073. 108 are 'possibly in label', kept but never ranked. The 258-row synonym table was drafted by Claude; no pharmacist has reviewed it yet."
- **Proves:** Data judgment.

### H9 · AI reliability (13:30–14:45, 75 s) — deck slide 10, optional SWITCH: AI code + SQL

- **Click:** slide 10. Optional (if on time): Cmd+6 → `ai_label_extraction.py` constants block (MODEL_ID … PILOT_SETIDS), then the SQL panel (AI cache query already run).
- **On screen** ([hood-code-ai-label-extraction.jpg](../screens/hood-code-ai-label-extraction.jpg), [hood-ai-extractions-cache-sql.jpg](../screens/hood-ai-extractions-cache-sql.jpg)): `MODEL_ID = "claude-sonnet-5.5"`, `PROMPT_VERSION = "p2"`, `PARSER_VERSION = "x1"`, `PILOT_SETIDS` (5 labels: 2 oxycodone + 3 semaglutide; the 5 Nov code screenshot still shows 2), `CACHEABLE`. SQL: 21 rows (the 5 Nov screenshot shows 9), `n_reactions` = `n_grounded` on every row, `from_cache` **true**.
- **Say:** "Claude Sonnet 5.5, through AIP, read 21 safety sections of 5 labels, two for oxycodone and the three semaglutide labels behind NAION, and returned each reaction with an exact quote. Code finds every quote word for word: 745 of 745. On a small answer key, 35 items from the Boxed Warning and Contraindications of the 2 oxycodone labels, written by Claude before the run, it found 35 of 35 answer-key items: F1 0.97 against a target of 0.85. No pharmacist has checked the key; the long sections and the semaglutide labels are not scored. The AI does not change the signal list; its value is the quotes you saw on page 1. The cache key is the label text plus the prompt, parser and model versions: adding the semaglutide labels cost 12 model calls once, and a forced rebuild made 0."
- **Proves:** AI reliability; Optimization (O1, O1b).
- **Fallback:** the two screenshots (also `deck/assets/ai-cache-sql-crop.png`).

### H10 · Monitoring (14:45–15:30, 45 s) — deck slide 11, optional SWITCH: monitoring SQL or Health tab

- **Click:** slide 11. Optional: Cmd+5 → SQL panel (monitoring query already run), or Cmd+7 → **Health** tab.
- **On screen** ([hood-monitoring-checks-sql.jpg](../screens/hood-monitoring-checks-sql.jpg)): `faers.reporter_type_blank` **warn**; `ai.grounded_rate` 1 pass; `ai.section_errors` 0 pass; `ai.cache_hit_rate` (info: 0.429 in the D041 v2 widening build, 1 when no label text changed); key checks pass. Health tab ([hood-data-health-signals.jpg](../screens/hood-data-health-signals.jpg)): Build status **Passed** · Primary key `signal_key` **Passed**.
- **Say:** "Every build appends 21 checks: keys, row counts, freshness, AI grounding, cache hits; plus 4 Foundry Data Health checks. It caught two real shifts: reporter type blank went from 34% to 72%, and recalls for our drugs went from 3 to 10 in four weeks. The drift is a replay from source dates, not weeks of live builds."
- **Proves:** AI reliability (stretch: notice if it gets worse); Data judgment.
- **Fallback:** the screenshots; drift replay [hood-monitoring-drift-sql.png](../screens/hood-monitoring-drift-sql.png).

### H11 · Optimization log (15:30–16:45, 75 s) — deck slide 12

- **Click:** slide 12.
- **Say:** "O1, the AI cache: 9 model calls and 70,776 tokens became zero on a rebuild. Helped. O2, incremental FAERS: 88 seconds against 32 for the full rebuild. Did not help. O3, reusing DailyMed XML we already hold: 3 minutes 23 to 1 minute 23, and 1,321 XML downloads to 2 (the index pages are still pulled every build). Helped. O3a, parsing fewer columns: 12.3–13.0 s to 12.2 s, locally; reverted. Partitioning: none in the pilot (D048); we revisit at 8 FAERS quarters or a 5-minute build. Each timing is one run."
- **Proves:** Optimization (measured, failures included).

### H12 · Incremental FAERS (16:45–17:30, 45 s) — deck slide 13 (diagram 33 FAERS panel; full diagram 33 v3 in B2), optional SWITCH: inc log

- **Click:** slide 13 ([diagram 33 v3](../../diagrams/png/33-handin-incremental-faers-v3.png)). Optional: Cmd+8, `clean_faers_inc_log` preview.
- **On screen** ([hood-faers-inc-log-sql.png](../screens/hood-faers-inc-log-sql.png)): 2026q1: 397,224 cases; 2026q2: 26,681 replaced, 655 deleted → 792,346.
- **Say:** "The incremental path reads only the new quarter into a kept state: three state datasets and one quarter log. Its output equals the full rebuild row for row. But at two quarters it is slower: 62 s for the state plus 26 s for the outputs, against 32 s. So signals keep reading the full rebuild (D044), and we re-measure at four or more quarters."
- **Proves:** Optimization (incremental vs full, measured).
- **Fallback:** the inc-log screenshot.

### H13 · Data judgment and what we chose not to do (17:30–19:00, 90 s) — deck slide 14, optional SWITCH: monitoring row

- **Click:** slide 14. Optional: Cmd+5 → SQL panel, point at `faers.reporter_type_blank` **warn**.
- **Say:** "Four messes that would have changed her answers. FAERS updates and deletes old cases: Q2 replaced 26,681 Q1 cases and deleted 655. Mass reports listing dozens of drugs: out of the main count, kept as evidence. Reporter type went from 34% to 72% blank: we show 'unknown'. DailyMed sometimes answers 'success' with the word 'None' (2 of 1,321, DQ42): kept, marked, retried. Noise we left: indication terms, like liraglutide's top signal 'Diabetic metabolic decompensation' (DQ06), and stimulated reporting after news or lawsuits (DQ04). The pharmacist's triage decides. Not done: no MedDRA licence, no patient data."
- **Proves:** Data judgment.
- **Fallback:** [hood-monitoring-checks-sql.jpg](../screens/hood-monitoring-checks-sql.jpg) (also `deck/assets/monitoring-checks-sql-crop.png`).

### H14 · Another month (19:00–19:40, 40 s) — deck slide 15

- **Click:** slide 15.
- **Say:** "The biggest gap is a named pharmacist. Today only Claude has checked the synonym bands, the answer key and the ranked signals. Claude prepares an evidence packet; the pharmacist decides; a create-only Action records who, when and on which evidence. Then schedules, live drift over three to four weeks, and a health page. Then score the long label sections with that pharmacist, and widen the AI to the other drugs' labels."
- **Proves:** Communication.

### H15 · What to take away (19:40–20:00, 20 s) — deck slide 16

- **Click:** slide 16.
- **Say:** "It answers her three questions, and every flag traces to its source: the label versions searched and the FDA recall record open in one click; the FAERS case reports are reachable by query, not yet from her screen. It is built to be extended, and we sped up only what we measured. And we say what is not proven yet, including that no pharmacist has scored the AI or the synonym table."
- **Proves:** Communication.

---

## 4. Screens: which stop uses which

| Screenshot ([screens/](../screens/README.md)) | Stop |
|---|---|
| app-0-morning-brief | A1 |
| app-1-not-in-label-naion | A2 (morphine row 5, liraglutide row 2); v0.9.0, AI = 0 (pre-D041 v2) |
| app-1d-naion-ai-read-3 | A3 (v0.10.0: labels also read by AI 3, new evaluation id) |
| app-1e-ai-quotes-panel-naion | A4 (labels searched + AI quotes table, v0.10.0) |
| app-1c-labels-searched-naion | A4 spare (labels table only) |
| app-1b-triage-action-form | A5 |
| app-2-recalls | A6 |
| app-3b-what-changed-past-month (app-3 as spare) | A7 |
| hood-data-lineage-signals | H2 |
| hood-ontology-manager-signal | H4 |
| hood-object-explorer-naion-links | H5 |
| hood-code-repo-ontology-signals | H7 |
| hood-code-ai-label-extraction | H9 (5 Nov: shows 2 setids, before D041 v2); Q&A AI |
| hood-ai-extractions-cache-sql | H9 (5 Nov: 9 v1-pilot rows; now 21) |
| hood-labeled-reactions-quotes-sql | Q&A AI |
| hood-monitoring-checks-sql | H10, H13; Q&A DQ04 |
| hood-data-health-signals | H10 |
| hood-monitoring-drift-sql | H10; Q&A DQ04 |
| hood-faers-inc-log-sql | H12 |
| hood-dataset-signals-preview | Q&A only ("what is behind the Signal object?") |

Still missing (fallbacks are weaker): the DailyMed Ozempic label with the `optic` search (A4, capture in rehearsal); the openFDA record for D-0040-2027 (A6); page 2 sorted with Class I first (A6); a saved decision row on NAION (only if the owner chooses Submit); page 1 filtered to semaglutide (A2); Object Explorer on MSSM AE Stat (the 2×2 counts) and on the Reference Label (H5); `def cache_key` (line 85) on screen (H9).
