# Rubric check — the build as of the baseline gate (2026-11-05)

_Evaluator / Red Team view · Stage: **Test** (design thinking) · Reviewer: Claude as the Evaluator persona · Read-only review: nothing in Foundry was opened or changed._

**TL;DR**
- The build is real and honest. The baseline gate passed, and the trail of data problems and failed optimizations is better than most reviewers will expect. **Data judgment and Architecture are the strongest rows.**
- The weakest point is where the brief's core idea meets the screen. The brief asks for an AI that reads labels, compared with FAERS, and a drill-down that shows the **label passage beside the extraction**. Today the AI has read 2 oxycodone labels. The hero signal (semaglutide · NAION) shows "Labels also read by AI: 0". The screen has no "passage beside extraction" view.
- Two of the four hand-ins do not exist yet: the **one-page architecture note** and the **demo** (no script, deck, rehearsal or timed run).
- One recommendation: **before writing the deck, close the AI ↔ screen gap.** Run the cached extractor on the semaglutide reference labels and add a drill-down panel (Labeled Reactions: reaction · quote · section · label version). Then a human hand-scores a 30-item sample from the long sections. Together these lift two rows (Application and AI reliability) and give the demo its strongest 3 minutes.

Scale used: **strong / adequate / weak**, with a 1–5 number in brackets (5 = a reviewer would hold it up as an example).

---

## 1. "What to hand in" (brief §4)

| # | Hand-in | Status today | Score | Evidence | What is missing |
|---|---|---|---|---|---|
| 1 | **Working build** ("Pipelines, ontology, AI function and application, running in Foundry") | Built, rebuilt end to end and traced | **Strong (4)** | [baseline-gate.md](../baseline-gate.md): full downstream rebuild, counts unchanged, 5/5 random flags re-derived from FAERS rows, 2 triage decisions survive; [foundry/README.md](../../../foundry/README.md) | AI function covers 2 labels / 9 sections only. Ontology types are "Experimental". No schedules, so nothing refreshes by itself. D045–D047 still proposed. Two triage rows have "TEST" rationales and will show in the demo. |
| 2 | **One-page architecture note** ("diagram … plus the three or four decisions that mattered most and what you chose not to do") | **Not written** (`docs/11-handin/architecture-note/` does not exist) | **Weak (1)** | Ingredients exist: [diagram 30](../../diagrams/png/30-handin-data-flow-v1.png), [diagram 31](../../diagrams/png/31-handin-ontology-v1.png), D020/D027 identity, D022 upsert, D023 v2 mass reports, D041/D005 cached AI, D043 synonyms | The note itself. It is a required hand-in, and it is short, so this is the cheapest point on the whole sheet. |
| 3 | **Optimization log** ("measure it, improve it … before and after … what you tried that did not help") | Written, 4 entries | **Adequate (3)** | [optimization-log.md](../../08-optimization-log/optimization-log.md): O1 cache (70,776 → 0 tokens), O2 incremental slower (32 s vs 88 s), O3 XML reuse (203 s → 83 s, 1,321 → 2 downloads), O3a no help | Each timing is one run. The O3 baseline is "from an earlier build, not back-to-back". No compute-seconds or cost. **Partitioning is not mentioned once.** See row Optimization. |
| 4 | **20-minute demo + questions** ("as the safety officer would use it, then go under the hood") | Agenda only | **Weak (2)** | Agenda in [AGENT-BRIEF.md](../AGENT-BRIEF.md), [demo map (diagram 36)](../../diagrams/png/36-handin-demo-map-v1.png), [screens/](../screens/) | No script, deck, rehearsal or timing yet. The **timed morning flow** (A016, ACTIVITY-LOG "next actions") was never run. The agenda packs 11 parts into 20 minutes, with 13 minutes under the hood, which is tight for a live Foundry session that the Compass calls slow. |

---

## 2. "What we will look at" (brief §5), row by row

### 2.1 Architecture — **Strong (4)**
> Rubric: "A clear raw-to-ontology structure. Drug identity resolved once, in the right place. An ontology that a second engineer could extend without asking you how."

| | |
|---|---|
| **Best evidence** | [Diagram 30](../../diagrams/png/30-handin-data-flow-v1.png) and the layer tables in [foundry/README.md](../../../foundry/README.md) (raw → clean → curated → ontology, every dataset with key, rows and RID). Identity is resolved once, in `clean_drug_identity` (D020, D027: Drug → Product → Package), and every pipeline reads from it. [foundry/ontology/README.md](../../../foundry/ontology/README.md) records every object, link and Action. |
| **Biggest hole** | "A second engineer could extend it **without asking**" is the weak clause. (a) The ontology was built by hand in the UI. Every object type's **Description is blank** in Foundry ([screenshot](../screens/hood-ontology-manager-signal.jpg); A010 known gap). (b) The formulary list is **copied 5 times**: `INGREDIENTS` in 4 raw files plus `FORMULARY` in `clean_drug_identity.py`. Adding a drug means knowing to edit all five. (c) A Signal links only to Drug and AE Stat. **No link reaches the labels that were searched or the FAERS reports** ([Object Explorer screenshot](../screens/hood-object-explorer-naion-links.jpg)), so the trace needs SQL. (d) The duplicate Signal → Drug link is visible in that same screenshot. (e) The brief names an "Adverse Event" object. The build has AE Stat (one aggregate per drug × reaction) and no case-level object. That is a reasonable choice, but no decision records it. |
| **Tough question** | "I'm your second engineer. Add dulaglutide's sister drug and a ClinicalTrials.gov source. Which files do I touch, and how would I know about the other four lists?" Follow-up: "From the NAION signal, click to one of the 394 reports **without** SQL." |
| **Cheapest fix** | **Build, ~30 min:** fill in the object-type descriptions in Ontology Manager and delete the duplicate link. **Doc, ~30 min:** a short "how to add a drug / a source" checklist that names the 5 lists and explains why they are copied (raw transforms take no dataset inputs while source exports stay off; D038 least privilege). Add a one-line decision: "no case-level AE object; cases stay in `clean_faers_drug_reaction`". **Present:** show diagram 30 and say "identity once, here" before anything else. |

### 2.2 Optimization — **Adequate (3)**
> Rubric: "Deliberate choices about incremental versus full rebuilds, partitioning, and where the LLM step sits so it is not re-run needlessly. Measured, not asserted."

| | |
|---|---|
| **Best evidence** | O1: the LLM sits after `clean_labels`, cached by text hash + prompt/model version. A rebuild costs 0 calls and 0 tokens (from 9 calls / 70,776 tokens). O2: incremental FAERS is **identical** to the full rebuild (EXCEPT ALL both ways = 0) yet **slower** (88 s vs 32 s), so signals keep the full rebuild (D044). That is the deliberate choice the rubric asks for, with the number that drove it. O3: 1,321 → 2 downloads, 3 m 23 s → 1 m 23 s. |
| **Biggest hole** | **Partitioning is named in the rubric and absent from every file.** No decision, no measurement, no "why not". Also: (a) every timing is **n = 1**, and O3's baseline is not back-to-back; (b) no compute-seconds or cost, only wall time and tokens; (c) the O2 plan ("re-measure at 4+ quarters"; "one build for state + outputs") was not tried, so the only incremental pipeline has no path to being faster. |
| **Tough question** | "Partitioning is on our list. What did you partition, and if nothing, why not? Give me a number." Then: "Is 32 s vs 88 s outside the noise of Foundry start-up? How many runs?" |
| **Cheapest fix** | **Doc + 2 builds, ~1 h:** add an O4 "partitioning: not done, and why". Cite the sizes already measured (373,522 drug-reaction rows, 2 quarters ≈ 690 MB of files per the manifest), say where it would go (FAERS state by quarter, signals by ingredient), and give the trigger (N quarters or drugs). **Build, no code change:** re-run O2 and O3 two more times each, back to back, and report a range. **Present:** lead the optimization part with O2 ("we built it, proved it equal, measured it slower, and kept the full rebuild"). That is the most credible slide in the log. |

### 2.3 Data judgment — **Strong (4)**
> Rubric: "You found the problems in the data, handled the ones that matter, and were honest about the ones you left."

| | |
|---|---|
| **Best evidence** | [data-issues-register.md](../../07-data-quality/data-issues-register.md): 42 issues, many measured, not guessed. Examples: substring matching inflates morphine rows by 50% (DQ34), appending quarters adds 8.7% phantom rows (DQ36), the duplicate fold cuts oxycodone by 24% (DQ37), reporter type goes from 35% to 72% blank (DQ38), DailyMed returns HTTP 200 with the text "None" (DQ42). The mass-polypharmacy cluster drives D023 v2. The baseline gate's 5/5 hand trace re-derives `a` from FAERS rows. |
| **Biggest hole** | (a) **The register undersells the work.** DQ01 (duplicates), DQ02 (free-text names) and DQ05 (suspect role) still say "Suspected", even though D020–D022 handle them in the build. DQ34–DQ37 say "Measured", not "Handled". A reviewer skimming the statuses sees an unfinished list. (b) **DQ06 (indication terms counted as reactions) is not handled**, and it shows on page 1: liraglutide's rank-1 signal is "Diabetic metabolic decompensation" ([screen](../screens/app-1-not-in-label-naion.jpg)). (c) **DQ04 (stimulated reporting) is not handled**, and the hero signal NAION is exactly the kind of signal it affects. (d) Other rank-1 items look odd to a pharmacist (morphine · Ewing's sarcoma, hydrocodone · subchorionic haemorrhage at a = 3). |
| **Tough question** | "Liraglutide's top 'unlabeled' signal is the disease it treats. And how much of NAION's 394 reports were filed by lawyers or after the news?" |
| **Cheapest fix** | **Doc, ~30 min:** update the DQ statuses to Handled with decision links, and mark DQ04/DQ06 "Accepted: not handled", with the reason. **SQL, ~20 min:** measure NAION's reporter-type split (lawyer / consumer / health professional / blank) and keep it as a Q&A number. It is **not measured** today. **Present:** one slide, "noise we can see in our own top list, and why we left it" (indication, stimulated reporting, no MedDRA grouping). Optional build (~1 h): tag reactions found in the label's Indications section as an `indication` bucket. |

### 2.4 The application — **Adequate (3)**
> Rubric: "It answers the safety officer's three questions quickly, and every flag traces to its source. It proves the pipelines work."

| | |
|---|---|
| **Best evidence** | [Morning brief](../screens/app-0-morning-brief.jpg): 3 numbers (1,073 · 126 · 26) plus an "as of" date per source. Pages 1–3 answer each question ([not in label](../screens/app-1-not-in-label-naion.jpg), [recalls](../screens/app-2-recalls.jpg), [what changed](../screens/app-3-what-changed.jpg)). The triage Action is create-only and pinned to `evaluation_id`, and it survived a rebuild. |
| **Biggest hole** | (a) **The brief's "drug drill-down showing the source label passage beside the extraction" is not on screen.** A012 argues that a signal has no quote, which is true. But the brief asks for a *drug* drill-down, and for the hero drug the AI read 0 labels. (b) **The trace stops at numbers.** The signal record shows "Reference labels searched: 3" but not which labels, no DailyMed link and no example case ids. The 5/5 trace in the gate needed SQL. (c) **"Quickly" is not measured:** the timed morning flow was never run. (d) The headline "1,073" is a queue nobody can work through in a morning. Nothing on screen shows which signals are untriaged or new. (e) Page 3 has no signal changes yet: all 26 are label-version and recall dates. A label change says "version 11 effective", not what changed in it. (f) "We pulled it at" shows **No value** for FAERS and RxNorm on the first screen of the demo. |
| **Tough question** | "Show me the label passage next to what your AI extracted, for the drug you just flagged." Then: "Liraglutide label version 11 became effective on Oct 30. Did it add or remove a warning? How would she know?" |
| **Cheapest fix** | **Build, ~1–2 h:** add a drill-down panel on page 1: for the selected signal's drug → reference label → Labeled Reactions table (reaction · exact quote · section · label version, with a DailyMed link). Run the cached extractor on the semaglutide reference labels (add their setids to `PILOT_SETIDS`; this needs a D041 v2, because D041 said widen only after the pharmacist check), so the hero signal can show "AI read N labels, NAION in none". **Build, ~30 min:** add `example_case_ids` and `labels_searched` (keys + DailyMed URL) to the signal record in `ontology_signals.py`. Fill the two "No value" cells. **Run:** the timed morning flow, and quote the time. **Present:** call 1,073 "the review queue" every time; never "1,073 findings". |

### 2.5 AI reliability — **Adequate, at the low end (3)**
> Rubric: "You can say how often the extraction is wrong and how you know. Stretch: you would notice if it got worse."

| | |
|---|---|
| **Best evidence** | [eval/ai-eval-v1.md](../../../eval/ai-eval-v1.md): 448/448 quotes found word for word (the hallucination check). Strict recall 35/35, precision 35/37, F1 0.97 vs the D015 target of 0.85, against an answer key frozen before the model ran. The p1 → p2 history (strict recall 0.31 → 1.00) shows that the scoring catches a real change. `ai.grounded_rate` is checked every build (A017). The file says plainly what it does not show. |
| **Biggest hole** | (a) **Small and narrow:** 35 items from 4 short sections of 2 labels, all for one drug. The long sections (Warnings and Precautions, Adverse Reactions) hold **about 411 of the 448 items and are unscored**, and they are the sections that decide "not in label". (b) **Circular:** Claude wrote the answer key, and the extractor is Claude Sonnet 5.5. "Frozen first" helps, but it is not independent. (c) **The AI does not change the signal list** (A012, eval file), so its error rate does not yet affect what the officer sees. (d) **Stretch drift:** the brief means drift "across label versions or model changes". The drift replay covers recalls and FAERS, not extraction. The cache-key re-extract is a design, not a run. |
| **Tough question** | "How often is it wrong on the Adverse Reactions section? Who, other than Claude, decided what 'right' is?" |
| **Cheapest fix** | **Eval, no build, ~1–2 h of a human's time:** (1) draw a random 30-item sample from the long-section extractions. A person (you, not Claude) marks each "real reaction for this label: yes/no" from its quote, giving a precision with an interval. (2) Hand-label one long section (OxyContin Warnings and Precautions, 29 items extracted) for recall. Label the result "human-checked, not a pharmacist". **Present:** use p1 → p2 as the "we would notice if it got worse" story: a prompt change moved strict recall from 0.31 to 1.00, and the gold check caught it. Say clearly that model-change drift is designed, not yet run. |

### 2.6 Communication — **Adequate (3)**
> Rubric: "The note and the demo explain trade-offs plainly, including what you would do with another month."

| | |
|---|---|
| **Best evidence** | The reasoning trail is unusually complete. 17 approach files (dropped and failed ones kept), a decision log with a change table, and the honesty rules in [AGENT-BRIEF.md](../AGENT-BRIEF.md) (O2 slower, O3a no help, Claude-written key, duplicate link left in). [another-month-sources-and-pharmacist-review.md](../../09-roadmap/another-month-sources-and-pharmacist-review.md) answers "another month" with sources, licences and PHI risk. |
| **Biggest hole** | (a) **The two artefacts this row names, "the note and the demo", do not exist yet.** (b) **Too much to read.** 47 decisions, 42 issues and 17 approaches are a strength only if someone distils them. (c) **Stale or inconsistent files a fact-checker will catch:** COMPASS v35 still says "Step 11 in progress", names the baseline gate as the next milestone (it has passed) and gives the top risk as "1,355 ranked items" (now 1,073). The DECISIONS change table logs D047 at "Compass v36", which does not exist yet. The diagram index says diagram 33 shows O3 as "being measured", but O3 is measured. D020–D023 still read "Proposed" in the "All decisions" table, although the change table records them as accepted via D039 G6. |
| **Tough question** | "In two minutes, with no slides: the three or four decisions that mattered most, and what you chose not to do." |
| **Cheapest fix** | **Doc, ~2 h:** write the one-page note first. It forces the "3–4 decisions" choice (suggested: D020/D027 identity once; D022 upsert + D023 v2 mass reports; D041/D005 cached, grounded AI with a quote; D043 reviewed synonym table instead of an LLM judge). Not done: MedDRA, ClinicalTrials.gov, case-level objects, switching to incremental, widening the AI. **Lead's job:** refresh the Compass and fix the stale labels above before any agent copies them into the deck. |

---

## 3. Ranked top-10 gaps (fix in this order)

| Rank | Gap | Rows hit | Type of fix | Rough effort (guess) |
|---|---|---|---|---|
| 1 | **Architecture note not written.** It is a required hand-in. | Hand-in 2, Communication, Architecture | Doc | 2 h |
| 2 | **No "label passage beside extraction" drill-down**, and the AI has not read the hero drug's labels ("Labels also read by AI: 0" on NAION). | Application, AI reliability | Build (Workshop panel + run the cached extractor on semaglutide reference labels; D041 v2) | 2–3 h + one model run |
| 3 | **AI error rate is self-scored and tiny.** 35 items, short sections only, Claude key vs Claude model; about 411 of 448 items unscored. | AI reliability | Eval by a human (30-item precision sample + one long section) | 1–2 h of your time |
| 4 | **Demo not scripted, rehearsed or timed**; morning flow never timed; no deck. | Hand-in 4, Application, Communication | Doc + rehearsal | Phase C plan |
| 5 | **Trace stops at numbers on screen.** No case ids, no list of labels searched, no DailyMed link on the signal; the Signal object has no link to Label. | Application, Architecture | Build (2 properties in `ontology_signals.py`; optional link type) | 30–60 min |
| 6 | **Partitioning never addressed; all timings n = 1;** no compute or cost figure. | Optimization | Doc (O4 "why not") + 4 repeat builds | 1 h |
| 7 | **Visible noise in the top list** (indication terms DQ06, stimulated reporting DQ04 on NAION, odd rank-1 items), not named anywhere the reviewer will look. | Data judgment, Application | Present (one slide) + SQL (NAION reporter-type split; optional indication bucket) | 30 min–1 h |
| 8 | **Stale or inconsistent docs** (Compass v35 text, DQ statuses, D047 "v36", diagram 33 O3 label, D020–D023 status cells). A fact-checker will find them before the reviewer does. | Communication, Data judgment | Doc (lead only for Compass/DECISIONS) | 45 min |
| 9 | **"What changed" is thin.** No signal changes yet; label changes do not say what changed; the 1,073 headline is not actionable (no "untriaged" or "new" count); "No value" cells on the Morning brief. | Application | Build (small) + present (show the local planted-change test: exactly 3 events) | 1 h |
| 10 | **Ontology and ops hygiene.** Blank descriptions, duplicate link, "Experimental" status, TEST triage rows, formulary list copied 5×, no schedules (freshness checks never fire on their own); Part D lacks build-time and schema checks. | Architecture, Monitoring (stretch) | Build (UI clean-up) + doc | 1 h |

---

## 4. The weakest point and the demo question

**Weakest point:** the AI function and the screen do not yet meet. The brief's central idea (Part B and Part C together) is that an LLM reads the label, its output is compared with FAERS, and the officer sees the label passage beside the extraction. Today the AI has read 2 oxycodone labels. It does not change the signal list. The drill-down that shows its work is not on the screen. The demo's hero signal is semaglutide, which the AI has never read.

**The question a reviewer will ask in Q&A:**
> "Your AI read two labels for one drug, and you say the signal list would be the same without it. What is the AI function actually doing in this product, and how often is it wrong where it matters?"

**A good answer today (presentation only):** "On purpose, the AI is the *evidence* layer, not the *decision* layer. The 'not in label' call is a deterministic text + reviewed-synonym check that we can audit (D037, D043). The AI gives the exact quote, and the quote is verified word for word (448/448). We did not widen it past 2 labels because our only answer key is Claude-written, and we would not scale a model we cannot score independently (D041). With another month: a pharmacist-scored sample of the long sections, then widen." That answer is defensible, and it fits the brief's line that "a partial build with clear reasoning" beats a complete one you cannot explain. It is far stronger if fixes 2 and 3 are done first.

---

## 5. Risks if nothing changes

| Risk | Likelihood (guess) | Impact |
|---|---|---|
| The reviewer opens the Morning brief and the change count is no longer 26 (it is "last 30 days, relative to today"), so the screen and the deck disagree | High if the demo is on a later day | Low–medium: say it on the slide ("live number; 26 on 2026-11-05") |
| Live Foundry is slow during the 13 minutes under the hood | Medium (Compass top risk #2) | Medium: keep screenshot fallbacks in the deck |
| A PV-literate reviewer reads the rank-1 list aloud (Ewing's sarcoma, diabetic metabolic decompensation) | Medium | Medium: pre-empt with the "noise we can see" slide |
| TEST triage rationales appear on screen during the triage demo | High unless cleaned | Low, but looks unready |

---

## Assumptions (said plainly)
- I did **not** open Foundry. Scores rest on the repo files, [numbers.json](../numbers.json) and the 7 screenshots in [screens/](../screens/). Where a file says something was checked in Foundry, I took it as true.
- I did **not** check whether any FDA or EMA document now lists NAION for semaglutide. The build says no DailyMed semaglutide label mentions it (A014). Checking FDA Drug Safety Communications (an optional source in the brief) is a good Q&A preparation step.
- Effort figures are guesses, not measurements.
- "Strong / adequate / weak" is my judgment against the brief's wording. The reviewers' own weighting is unknown.

## What I would check next
1. After fixes 2–3: re-score Application and AI reliability. Both could reach 4.
2. Once the note and deck exist: run the fact-checker against `numbers.json`, and run this check again on the note and the demo script.
3. Do a timed dry run of the 20-minute agenda against live Foundry, with stops recorded.

**Compass:** Phase 2 · Pilot build → hand-in Phase C · Baseline gate passed (2026-11-05) · Next milestone: architecture note, deck and demo path · Open blockers: pharmacist reviewer not named; AI ↔ screen gap (this review)
