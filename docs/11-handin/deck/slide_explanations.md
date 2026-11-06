# Slide explanations — a newcomer's handbook to the MSSM demo deck

_🖼️ Deck Designer view · v1, 2026-11-05_

For someone who has never seen Palantir Foundry, drug safety or this project. **New here? Read R00 "Start here" first** (`docs/11-handin/reports/pdf/R00-start-here.pdf`): it says which report answers which question. For every slide of [MSSM-demo-deck.pptx](MSSM-demo-deck.pptx): **purpose**, **what you need to know**, **evidence**, **how to read it**, **limits**. The spoken words are in [speaking_script.md](speaking_script.md) (same anchors); the slide-by-slide plan is in [content_storyboard.md](content_storyboard.md).

**Labels used on slides**
- **OBSERVED** — measured in Foundry and frozen in [numbers.json](../numbers.json) at the [baseline gate](../baseline-gate.md) (2026-11-05).
- **DERIVED** — computed from two observed numbers (ratio, percentage, F1). The formula is in the slide's source line.
- **ASSUMED** — not verified, taken as true for now (effort days, "fit" ratings).
- **DESIGNED** — a design choice we made and wrote down; it may be built (the status band says how far). Things not built yet carry the PLANNED band, never DESIGNED alone.
- Status bands: **BUILT · TESTED IN FOUNDRY** (it runs and was checked), **PLANNED — NOT BUILT**, **DECISION PROPOSED — NOT YET ACCEPTED**.

## Glossary (first use on the slides)
| Term | Plain meaning |
|---|---|
| Palantir Foundry | A data platform: stores tables, runs the code that builds them, and hosts apps on top |
| Dataset | A versioned table in Foundry |
| Transform | The Python code that builds a dataset from other datasets |
| Code Repository | Where transforms live (like a Git repo inside Foundry); ours: `pipelines_raw_ingest`, `pipelines_clean` |
| Data Lineage | Foundry's picture of which dataset feeds which |
| Ontology | A layer of business objects (Drug, Signal …) on top of datasets, which apps read |
| Object type / link type | A kind of object, backed by one dataset / a typed relation between two object types (e.g. many signals : 1 drug) |
| Action | The controlled way to write into the Ontology; ours creates a Triage Decision |
| Workshop | Foundry's app builder; our app is the module *MSSM Safety Officer* |
| AIP | Foundry's AI platform; it lets a transform call a large language model (here Claude Sonnet 5.5) |
| FAERS | FDA Adverse Event Reporting System: voluntary side-effect reports, released as quarterly files |
| PRR | Proportional reporting ratio: how much more often a reaction is reported with this drug than with all others |
| Evans rule | A common screening threshold: at least 3 reports, PRR ≥ 2, chi-square ≥ 4 |
| MedDRA preferred term (PT) | The standard term FAERS uses for a reaction (e.g. "Optic ischaemic neuropathy"). The MedDRA dictionary and its groupings need a licence |
| DailyMed / SPL | NLM's site of official drug labels / Structured Product Labeling, the XML format of those labels |
| openFDA | FDA's public API; we use recalls (enforcement), Drugs@FDA and the NDC directory |
| RxNorm / RxCUI | NLM's standard drug names / the id of one concept, e.g. one ingredient |
| NDC | National Drug Code: the id of one package |
| Signal (in this project, 1,952) | A drug–reaction pair that meets the Evans rule (D006, proposed) **and** whose reaction term is not found in any reference label of that drug (1,844 "not in label") or is found only through a medium-band synonym (108 "possibly in label"). A reason to look, not proof of harm |
| Ranked (1,073) | The review queue: signals that are "not in label", in the clinical bucket (D016 v3), and less than half carried by mass-polypharmacy reports (D023 v2). Not 1,073 findings |
| Active recall (126) | openFDA enforcement status = **Ongoing** (`clean_recalls.py`). Not "not terminated", which would also count Completed |
| The 13 drugs | Opioids (8): oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, buprenorphine, tramadol. GLP-1s (5): semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide (exenatide has no reference label, so signals exist for 12 of 13) |

---

<a id="s01"></a>
## 1 · Medication Safety Signal Monitor
- **Purpose:** name the product; put the officer's three questions on screen in the first 20 seconds.
- **Know:** the "end user" is a hospital pharmacy safety officer. "Pilot" = the narrow scope we built end to end.
- **Evidence:** scope from numbers.json (`scope`: 13 drugs, 8 opioids, 5 GLP-1, FAERS 2026Q1–2026Q2); capture date from `_meta.captured_at`.
- **Limits:** none on this slide.

<a id="s02"></a>
## 2 · Her three morning questions, and one trust rule
- **Purpose:** the user, her pain, and the test every feature must pass ("every flag traces back to its source").
- **Know:** the brief allows "one drug class or 50–200 drugs". We chose 8 opioids + 5 GLP-1 drugs as one hand-picked formulary (D014 hybrid class, D018 explicit RxCUI list) because opioids and GLP-1s cover each other's gaps (recalls, label changes, volume).
- **Evidence:** [brief-summary.md](../../00-brief/brief-summary.md); DECISIONS D014, D018. DESIGNED pill = a scope choice.
- **Read it as:** the three cards map to app pages 1–3; the Morning brief (page 0) shows all three at once. The lead says only what was measured: one screen built to answer the three questions; machine load 11.5 s (`app.timing_s`). "Under two minutes" for a person has **not** been measured; a human walk-through will be timed in rehearsal.
- **Limits:** 13 drugs is far below a real formulary of a few hundred; scale ideas are in `docs/09-roadmap/`.

<a id="s03"></a>
## 3 · Morning brief (LIVE, page 0)
- **Purpose:** prove the application answers all three questions fast, and is honest about freshness.
- **Know:** sources update on different clocks: FAERS quarterly, openFDA recalls weekly, DailyMed daily, RxNorm monthly. So the screen shows "data as of" per source instead of pretending everything is daily (D028, D045 proposed). The "changes" card counts change events in the **last 30 days** (26), not "since yesterday"; page 3's date range narrows to "since my last review". FAERS is about 130 days behind, and signals change only when a new FAERS quarter arrives; FAERS moved to AEMS in March 2026 and the future feed is unverified.
- **Evidence (OBSERVED):** 1,073 ranked signals (`signals.ranked`), 126 active recalls (status Ongoing) of 900 (`recalls`), 26 changes in 30 days (`changes.last_30_days`), FAERS freshness 130 days and openFDA 8 days old (`monitoring.faers_age_days`, `openfda_age_days`). Screenshot `screens/app-0-morning-brief.jpg`.
- **Read it as:** three counts, each a door to a page. **Fast (OBSERVED, `app.timing_s`):** the brief was on screen in 11.5 s and page switches took 0.8–2.4 s, timed by a browser script in View mode (time until the expected text appears; human reading time not included).
- **Limits:** the 30-day count is live, so on a later day the screen will not show 26. 1,073 is a **review queue**, not 1,073 findings (slide 9). The "We pulled it at" column shows "quarterly file (no pull time)" for FAERS on the current screenshot: the FAERS files are loaded by hand, so no automatic pull time is recorded (assumption; not checked further). D045 (change feed + source status) is still **proposed**.

<a id="s04"></a>
## 4 · Not in label (LIVE, page 1)
- **Purpose:** the trust rule in action: from one flag to its numbers, to the label search, to the label itself on DailyMed, to a recorded decision.
- **Know:** NAION (non-arteritic anterior ischaemic optic neuropathy) is sudden vision loss from poor blood flow to the optic nerve; its FAERS term is "Optic ischaemic neuropathy". **Rank is within each drug** (by Yates chi-square, clinical bucket only), so many drugs have a "rank 1".
- **Name the noise first:** before filtering, the presenter points at the unfiltered rank-1 rows. Some are not plausible drug effects: Morphine · Ewing's sarcoma (a bone cancer) **likely** reflects the patients who receive morphine, not the drug (an interpretation, not checked). Some rank-1 rows are the condition the drug treats (DQ06, a known gap, not handled). That is why 1,073 is a review queue.
- **Known positive (verified, DECISIONS learning 2026-11-05):** EMA's PRAC concluded on 6 June 2025 that NAION is a very rare side effect of semaglutide; WHO issued an alert on 27 June 2025. The 3 US label versions we search do not mention it. So NAION is **not a discovery**: the method found, from FAERS alone, a signal a regulator has already acted on. It is a check that the monitor works.
- **Evidence (OBSERVED, `signals.naion`):** a = 394 reports with semaglutide + NAION, 20,892 semaglutide reports in all, PRR 112.5, 95% CI 92.19–137.24, chi-square (Yates) 10,653.8, rank 1. **Trace:** the "Reference labels searched" panel lists the 3 labels (`app.labels_searched_naion`): Ozempic v20, Wegovy v19, oral Ozempic v14, each with a DailyMed link (names and versions read from `screens/app-1c-labels-searched-naion.jpg`). Label check method `text+ai_v1+syn_v2` names all three checks, but the AI read **0** semaglutide labels (the pilot covers 2 oxycodone labels): NAION is "not in label" from the exact-text and synonym checks only. The Action form: `screens/app-1b-triage-action-form.jpg`.
- **Read it as:** PRR 112.5 means NAION is about 112 times more common among semaglutide's reports than among other drugs' reports: a reporting pattern, not 112 times the risk. The CI's lower bound (92) is far above 2, so it is not a small-number fluke, but news coverage can still inflate it (DQ04). The label check found no mention in semaglutide's reference labels.
- **Trace to the source (mandatory, not optional):** the presenter clicks the Ozempic v20 DailyMed link in the "Reference labels searched" panel and searches the page for "optic". **Rehearsal check:** the search must not land on the diabetic retinopathy warning; if it does, search "ischemic optic" instead. The 394 FAERS reports **cannot be opened from her screen yet** (case ids are pulled by SQL today); the presenter says so.
- **Limits:** FAERS is voluntary reporting: publicity, lawsuits and duplicate filings all raise counts. A signal means "look at this", not "the drug causes this". Whether NAION should be escalated is a pharmacist's call, not ours. The Action form is shown; whether to **submit** a decision live is the presenter's choice (submitting adds a real Triage Decision object). Only the project owner can submit a Triage Decision today (Action permission); the officer role is a production step.

<a id="s05"></a>
## 5 · Recalls and what changed (LIVE, pages 2–3)
- **Purpose:** questions 2 and 3, an honest "no match", and a recall traced to the FDA's own record.
- **Know:** a recall names products in free text. We match it by NDC (package code) to the **658 FDA-listed products we track for our 13 drugs** (MSSM Product objects, `foundry/ontology/README.md`; not in numbers.json). We have **no purchasing or inventory data**, so "Matched to our products: 0" means "none of those FDA-listed products", not "not on her shelves". Never say "products we carry". The presenter pre-opens the openFDA enforcement record for D-0040-2027 (`api.fda.gov/drug/enforcement.json?search=recall_number:"D-0040-2027"`) so the recall traces to its source, and clicks the Classification column to show Class I first. **The Class I count is a rehearsal check, not measured.** "Since my last review" = the start-date filter on page 3 (a per-user saved bookmark is not built).
- **Evidence (OBSERVED):** 126 active (status Ongoing) of 900 (`recalls`); newest D-0040-2027 reported 2026-10-21 (`recalls.newest`, `newest_reported`); 2,898 events = 900 reported + 767 terminated + 1,231 label versions effective (`changes`; the 1,231 of 1,321 label versions that carry an effective date, `ontology_changes.py` l.90); a rebuild with no new data added 0 events (`changes.snapshot_diff_after_rebuild`). Product text "Tirzepatide/Niacinamide … vial" and "matched 0" are read from the screenshot. Page 3 screenshot `app-3b-what-changed-past-month.jpg`: the "past month" preset shows 26 events (15 label + 11 recall), equal to the brief's `changes.last_30_days`.
- **Read it as:** most events are dated by the source (recall dates, label effective dates), so the feed had real history on its first build. A label row says a new version took effect, **not what changed in it** (she opens the label on DailyMed for that). Signals change only with each FAERS quarter, about 130 days behind (`monitoring.faers_age_days`).
- **Limits:** signal changes are found by comparing builds; that part has only been tested with a planted change (locally) and a no-change rebuild. D045 is **proposed**.

<a id="s06"></a>
## 6 · Architecture
- **Purpose:** the brief's first architecture test: "drug identity resolved once, in the right place".
- **Know:** raw → clean → curated → Ontology → Workshop. Identity = FAERS drug name → RxNorm ingredient (RxCUI) → product (application number) → package (NDC), built once in `clean_drug_identity` (D020 exact ingredient match; D027 two-level identity, **proposed** — built and running, owner acceptance pending).
- **Evidence:** diagram 38, the compact data flow + ontology from the [one-page architecture note](../architecture-note/) (numbers in it match numbers.json); the detailed flow is diagram 30 v2 (O3 measured). [foundry/README.md](../../../foundry/README.md). Live: Data Lineage on `ontology_signal_signals`; fallback screenshot in B12.
- **Read it as:** every arrow into signals, recalls and labels passes through the identity dataset.
- **Limits:** a second engineer still has to know that the formulary list is also copied in 4 raw pull files (raw pulls take no dataset inputs; D038); B1 says so. Object-type descriptions in Ontology Manager are blank (A010 gap).

<a id="s07"></a>
## 7 · Ontology
- **Purpose:** show the object model the app reads, and the safe write-back.
- **Know:** 10 MSSM object types. The Triage Decision is its own object, created only by the Action (create-only; decision id, reviewer and time set by the system), so rebuilding signals cannot erase decisions.
- **Evidence:** diagram 31; [foundry/ontology/README.md](../../../foundry/ontology/README.md); 2 triage decisions (`app.triage_decisions`), both still there after the baseline-gate rebuild.
- **Limits:** the 2 saved decisions are test decisions from steps 6 and 8, not real reviews. A duplicate Signal → Drug link type was added by mistake in step 11; unused; left for the owner to delete. All object types are status "Experimental". Only the project owner may submit the Action today.

<a id="s08"></a>
## 8 · From one FAERS report to a ranked signal
- **Purpose:** the data-judgment core in one picture.
- **Know:** (A) D022 keep the latest case version, apply deletes to all history; D021 suspects = primary + secondary + interacting, each ingredient once per report; D020 exact ingredient, never substring; D023 v2 fold duplicate filings and take reports with 30+ drugs out of the main count. (B) 2×2 table → PRR + Evans (D006, proposed). (C) label check, in code order: (1) AI term with a code-found quote (D041) → (2) exact text or US spelling in 6 safety sections (D037, proposed: built and running, owner acceptance pending) → (3) reviewed synonym (D043). The outcome is the same in any order; only `label_match_method` differs. Diagram 32 v2 draws them in this code order (1 AI → 2 Text → 3 Synonyms). (D) buckets (D016 v3): only clinical reactions are ranked.
- **Evidence:** diagram 32 v2. Its NAION box: 3 reference labels searched (Ozempic v20 · Wegovy v19 · oral v14), 0 safety sections mention it, and the AI read none of them. Its NAION 2×2 (b, c, d), the 2,533 Evans count and the 231 mass-report cautions come from the local run of `ontology_signals.py`, which equals Foundry (A014); they are not in numbers.json.
- **Limits:** buckets are keyword rules (a MedDRA stand-in), reviewed by hand, not by a pharmacist.

<a id="s09"></a>
## 9 · A review queue, not findings
- **Purpose:** stop the audience reading 1,073 as 1,073 problems; show the label checks reduced false positives.
- **Evidence (OBSERVED):** 14,921 drug × reaction stats, 1,952 signals, 1,073 ranked; ranked history 1,355 at step 9 (first full build) → 1,210 (synonyms v1) → 1,115 (buckets D016 v3) → 1,073 (synonyms v2); 1,844 not in label + 108 possibly in label = 1,952; 12 of 13 drugs have signals (exenatide has no reference label); synonym table syn_v2: 258 rows = 69 high + 72 medium + 117 rejected. **DERIVED:** −21% = (1,355 − 1,073) / 1,355.
- **Read it as:** the queue shrank because more FAERS terms were recognised as "already in the label" (synonyms) or as non-clinical (buckets). No signal was deleted.
- **Limits:** the synonym bands were drafted by Claude; no pharmacist has reviewed them (top blocker in COMPASS). We have no outside measure of how many of the 1,073 are worth action (planned: precision@10 per drug, slide 15).

<a id="s10"></a>
## 10 · AI reliability
- **Purpose:** the brief asks "can you say how often extraction is wrong and how you know?"
- **Know:** Claude Sonnet 5.5 via AIP reads each safety section of the 2 pilot labels (OxyContin and a generic oxycodone/APAP) and returns reaction + exact quote. Code checks every quote is in the section text (grounding). A separate answer key, frozen before the model ran, measures how many answer-key items were found and how many extra terms were added.
- **Evidence:** `ai` in numbers.json: grounded 448/448 (all 9 sections); on the 35-item key (Boxed Warning + Contraindications of 2 oxycodone labels, Claude-written, frozen first, no pharmacist yet): found 35 of 35 answer-key items (first prompt 11 of 35); precision ≥ 35/37 (both extras counted as errors); F1 0.97 (DERIVED) vs the proposed D015 target 0.85 (met on this pilot key only; the benchmark comparison was not run) — never quote the F1 without this scope; 0 model calls and 9/9 sections from cache on rebuild. [eval/ai-eval-v1.md](../../../eval/ai-eval-v1.md).
- **Read it as:** grounding catches invented text; the key catches wrong or missing items.
- **Limits:** 35 items, short sections only (Boxed Warning, Contraindications); the long sections (most of the 448 items) are not scored; the key was written by Claude, and the model is also Claude, so the check is not independent; D015 (the target) is **proposed**.
- **The AI ↔ screen gap (rubric-check finding, answered on the slide):** the AI has read only the 2 oxycodone pilot labels. The demo's hero signal (semaglutide · NAION) shows "Labels also read by AI: 0", the AI does not change the signal list, and there is no "label passage beside the extraction" panel yet. Our reason: we would not widen a model we cannot yet score independently (D041). Widening to the reference labels plus a quote panel would need a D041 v2: a decision for the owner, listed as "another month".

<a id="s11"></a>
## 11 · Monitoring
- **Purpose:** the stretch goal "notice if it gets worse", for both data and AI.
- **Evidence (OBSERVED):** 21 checks per build, 2 runs so far, 4 Foundry Data Health checks; reporter type blank 34.3% (Q1) → 72.1% (Q2); recalls reported 10 in the last 4 weeks vs 3 in the 4 before (×3.3 DERIVED). Screenshot: crop of `hood-monitoring-checks-sql.jpg`.
- **Read it as:** both warnings are real changes in the sources, not pipeline bugs. Note: 34% is Foundry at the gate; the Oct 20 profile (DQ38) said 35%. The reporter-type jump is probably FDA's switch to a new intake system (DQ38; an inference).
- **Limits:** drift is a historical replay from source dates, not weeks of live builds (D009 asks for 3–4 weeks). Only Data Health alerts the owner; the computed checks are read by the builder. No schedules, no health page. D046 is **proposed**.

<a id="s12"></a>
## 12 · Optimization log
- **Purpose:** "measured, not asserted", including what did not help.
- **Evidence (OBSERVED, `optimization`):** O1 9 → 0 model calls, 70,776 → 0 tokens; O2 32 s full vs 88 s incremental; O3 203 s → 83 s, 1,321 → 2 XML downloads per build (the ~30 index pages are still pulled), 1,319 reused; O3a 12.3–13.0 s → 12.2 s (local). **DERIVED:** ×2.75 = 88 / 32; −59% = (203 − 83) / 203. [optimization-log.md](../../08-optimization-log/optimization-log.md).
- **Read it as:** skipping unchanged input paid twice (O1, O3); adding machinery to save little did not (O2, O3a).
- **Partitioning (rubric names it):** not done on purpose — D048, **proposed**: largest table 2,554,017 rows (`faers.case_reactions`), clean builds ≤ 32 s, most likely start-up (not measured separately); revisit at 8+ quarters or a 5-minute build (thresholds from D048).
- **Limits:** each timing is one run (n = 1); O3's baseline is an earlier build, not back-to-back; O3a timed locally only; O1's job wall time not compared like-for-like. D047 (XML reuse) is **proposed**.

<a id="s13"></a>
## 13 · Incremental FAERS
- **Purpose:** a deliberate "incremental vs full rebuild" choice, backed by numbers (brief: optimization).
- **Evidence (OBSERVED):** outputs identical (EXCEPT ALL both ways = 0): 792,346 cases, 2,554,017 reactions, 373,522 drug-reaction rows; state 62 s + outputs 26 s = 88 s vs 32 s. Picture: diagram 33 v2, FAERS panel only (cropped).
- **Read it as:** with two quarters, re-reading everything is cheap; the fixed cost of reading and writing the kept state (three state datasets + one quarter log) dominates. With many quarters the balance should flip.
- **Limits:** the identity-change replay was tested locally only. D044 (accepted) keeps signals on the full rebuild until incremental is faster.

<a id="s14"></a>
## 14 · Data judgment
- **Purpose:** the brief says spotting and handling the mess is part of the test.
- **Evidence (OBSERVED):** Q2 replaced 26,681 Q1 cases and deleted 655 (`faers`); reporter type blank 34% → 72% (`monitoring`); DailyMed "None" replies: 2 of 1,321 (`optimization.O3.after_downloads`, `raw.dailymed_labels` — the 2 re-tried downloads are exactly the 2 "None" replies). Register: [data-issues-register.md](../../07-data-quality/data-issues-register.md) DQ36, DQ37, DQ38, DQ42.
- **Read it as:** each mess has an id, a measured effect, a rule, and a decision number.
- **Noise we left (amber row):** indication terms counted as reactions (DQ06; liraglutide's rank-1 signal "Diabetic metabolic decompensation" is the condition it treats, visible on page 1) and stimulated reporting after news or lawsuits (DQ04). Neither is handled; the pharmacist's triage decides. NAION's reporter-type split is **not measured**.
- **Limits:** the DQ37 row shows no number on the slide (its measured effects are in the register and diagram 32, not in numbers.json). The person-key fold leaves a residue (ages off by one year). "Chose not to do" items are cuts, not failures: D031 cut list, no MedDRA licence (D043), public data only.

<a id="s15"></a>
## 15 · Another month
- **Purpose:** the brief's "what would you do with another month", in plain trade-offs.
- **Know:** today every synonym band, answer-key item and ranked signal has been checked only by Claude. The loop keeps a human (licensed pharmacist) as the only one who can submit a decision, through a create-only Action, with evidence links.
- **Evidence:** [another-month-sources-and-pharmacist-review.md](../../09-roadmap/another-month-sources-and-pharmacist-review.md) §3 (loop), §3.3 (effort ≈ 7–8 build days + 3–4 pharmacist days — **ASSUMED**, an estimate), §4 (risks). 258 synonym rows from numbers.json.
- **Limits:** no pharmacist is named yet (COMPASS blocker). Nothing here is built.

<a id="s16"></a>
## 16 · What to take away
- **Purpose:** three takeaways, the "did not work" list, and links to backups.
- **Evidence:** as on slides 12, 7, 10 and DECISIONS (D045–D047 proposed).
- **Limits:** the list is the honest summary the brief asks for; repeat it if asked "what would you change?".

---

<a id="backups"></a>
# Backups

<a id="b01"></a>
## B1 (slide 18) · How another engineer would extend it
One place per kind of change, with one honest exception: the formulary list lives in `clean_drug_identity` **and** is copied in the 4 raw pull files (raw pulls take no dataset inputs while source exports stay off, D038), so adding a drug touches 5 files; new sources as a raw pull + clean transform; synonyms in `label_synonyms.py`; buckets and the statistical rule in `ontology_signals.py`; checks in `monitoring.py`; new screens via object type → Workshop. Sources: foundry READMEs, A007 / D036 conventions. Limit: the repos have no automated tests beyond count checks and the local runner (A014).

<a id="b02"></a>
## B2 (slide 19) · Incremental pieces in full (diagram 33)
Diagram 33 v2: both panels measured in Foundry. O3: 1,321 → 2 XML downloads (1,319 reused; index still pulled), 3 m 23 s → 1 m 23 s; D047 proposed. O1 tokens: first run 41,704 prompt + 29,072 completion = 70,776; 0 on rebuild.

<a id="b03"></a>
## B3 (slide 20) · Drug identity and FAERS counting rules
D020–D023 and the label check (D037 **proposed** — built and running, owner acceptance pending; D043 accepted). The table gives the code order: AI term → exact text → synonym. D020–D024 were accepted for the pilot through gate G6 (D039); the slide says "Accepted (G6)". Q2 numbers from numbers.json.

<a id="b04"></a>
## B4 (slide 21) · Trace and write-back
Triage form (locked subject and evaluation id) and Object Explorer links. "5 random ranked signals re-counted from FAERS rows, all matched" is from [baseline-gate.md](../baseline-gate.md) (the count 5 is a method detail, not in numbers.json). App: 4 pages, Workshop v0.9.0 (`app.workshop_version`).

<a id="b05"></a>
## B5 (slide 22) · AI evaluation details
Prompt p1 → p2 (answer-key items found: 11 of 35 → 35 of 35); the SQL view of `ai_label_section_extractions` (status ok, n_reactions = n_grounded, from_cache true); how a regression would be noticed (grounded rate < 0.95 fails; cache key includes model and prompt version; planned pharmacist sample with F1 drop > 0.05 = drift).

<a id="b06"></a>
## B6 (slide 23) · Decisions and status
Accepted vs proposed, and the reading order of the reasoning trail (starting with R00 "Start here", then the one-page architecture note). Proposed: 12 decisions, D006, D015, D025–D029, D037, D045–D048 (many built and running; owner batch-accept pending). D005 and D020–D024 are accepted. The full log is D001–D048.

<a id="b07"></a>
## B7 (slide 24) · Ripple map (diagram 37 v2)
"Change this here → this changes there" for 9 changes, checked against the code: a synonym row, a bucket keyword, a new FAERS quarter, adding a drug, a new label version, a recall status change, an officer decision, a prompt or model version, a Workshop variable. Key idea: the evaluation id hashes the evidence inputs (signal key, a, PRR, label check, window, labels searched, labels read by AI), not the bucket or the prompt. **Existing triage decisions stay linked in every row**, because they link by signal key (`subject_key`), not by the evaluation id; after some changes they simply sit on an older evaluation id. **Known gap (PLANNED):** there is no "stale" flag telling her a decision's evidence has since moved.

<a id="b08"></a>
## B8 (slide 25) · Change feed (diagram 34)
Two ways to know something changed: dated by the source (900 + 767 + 1,231) or found by comparing builds (signals; 0 after a no-change rebuild). D045 proposed.

<a id="b09"></a>
## B9 (slide 26) · Monitoring (diagram 35)
What is watched, the four check groups, drift replay, Data Health, who finds out, what is not built.

<a id="b10"></a>
## B10 (slide 27) · Sources researched for another month
A summary of the roadmap's comparison table. Licence facts are as found on the linked pages during a read-only scan on 2026-11-05; "fit" is our judgment (ASSUMED). "ClinHub" identity is uncertain (open question in the roadmap).

<a id="b11"></a>
## B11 (slide 28) · Demo map (diagram 36 v2)
23 stops, 1,200 s. A0–A7 are the officer's morning (slides 1–5, mostly live in the app); H1–H15 are under the hood (slides 6–16, with live Foundry switches). The demo director's navigation guide sets the exact clicks. Note: the diagram's H1 box says "Slide 6 · diagram 30 v2"; slide 6 actually shows diagram 38 (the one-page architecture picture), with diagram 30 v2 named in its source line.

<a id="b12"></a>
## B12 (slide 29) · Fallback screenshots
Data Lineage (cropped to the graph), Ontology Manager, Data Health, Code Repository. Use them if Foundry is slow.

---

## Assets (made for the deck, from existing files)
| File | Made from | Why |
|---|---|---|
| `assets/33v2-faers-panel-crop.png` | `docs/diagrams/png/33-handin-incremental-faers-v2.png`, rows 120–1545 px | Show only the FAERS panel on slide 13 (the full v2 diagram is B2) |
| `assets/monitoring-checks-sql-crop.png` | `screens/hood-monitoring-checks-sql.jpg`, box (515, 545, 1370, 765) | Result table only |
| `assets/ai-cache-sql-crop.png` | `screens/hood-ai-extractions-cache-sql.jpg`, box (515, 545, 1512, 735) | Result table only |
| `assets/data-lineage-crop.png` | `screens/hood-data-lineage-signals.jpg`, box (48, 48, 960, 712) | Graph only |

Crops were made with Pillow (`.venv/bin/python`); no pixels were edited.
