# Ripple table: change this here → this changes there

_🎬 Demo Director view · 2026-11-05 (Phase D fix pass: every row re-checked against `foundry/pipelines/**`), refreshed 2026-11-06 for D041 v2 (the AI reads 5 labels, 21 sections) · stage: **Test** · picture: [diagram 37 v3](../../diagrams/png/37-handin-ripple-v3.png) ([PDF](../../diagrams/pdf/37-handin-ripple-v3.pdf)) · newcomers start at [R00 "Start here"](../reports/pdf/R00-start-here.pdf)_

**TL;DR.** Nine edits a judge might ask about. For each one: where you make it, every downstream thing that moves, which builds to run in order, what the officer sees, and how to show it. **Nothing here is changed live in the demo.** The triage form is opened and cancelled (A5) unless the owner chooses Submit, and the page 3 date filter is the only live "change" (A7). Everything else is shown from evidence already on screen (the change feed, the dataset columns, the code constants), because most build times are not measured and a live rebuild could overrun the slot.

**How to read the "how long" column.** Only times in [numbers.json](../numbers.json) or the [optimization log](../../08-optimization-log/optimization-log.md) are given. Everything else says *not measured*: time it in rehearsal pass 1 ([rehearsal-plan.md](rehearsal-plan.md)) before you promise it.

**Common tail** (after any curated dataset changes): the Ontology re-indexes the object types backed by that dataset (time not measured; a brand-new object type needed about 1 minute, [foundry README](../../../foundry/README.md#how-a-change-reaches-foundry)). Then `ontology_changes.py` → `compute_changes` → `ontology_change_events` (+ `ontology_change_snapshot`), and `compute_source_status` → `ontology_source_status`. Then `monitoring.py` → `monitoring_checks` (appends 21 checks) and `monitoring_drift`. The Workshop (v0.10.0) reads the Ontology directly, so it needs no republish.

**Key fact 1: what is in the evaluation id.** `evaluation_id` = hash of `signal_key`, `a_drug_reaction`, `prr`, `label_check`, `window`, `n_reference_labels`, `ai_labels_checked` ([ontology_signals.py](../../../foundry/pipelines/ontology/ontology_signals.py) l.204–206). **Not** in the hash: `bucket`, `is_ranked`, `caution`, the label version or label text, and the AI prompt or model version.

**Key fact 2: what the change feed watches** (`WATCH`, [ontology_changes.py](../../../foundry/pipelines/ontology/ontology_changes.py) l.22): signal = `label_status`, `is_ranked`, `bucket`, `caution`; recall = `status`, `classification`; label = `spl_version`. A change to PRR, report counts or the evaluation id alone does **not** create a change event.

**Key fact 3: two kinds of change events** (`ontology_changes.py` l.126–133). `source_date` events (recall reported / terminated, label version effective) are written on the first build for everything, and later **only for a recall number or label setid the feed has never seen**. A change to something already seen becomes one `snapshot_diff` event per changed field (e.g. "status: Ongoing → Terminated"), dated **by the build day**, not by the source.

## What happens to an existing triage decision

When a later build gives a signal a new `evaluation_id` (row 1, 3, 4, 5 or 8 below), this is exactly what happens. Sources: [ontology README](../../../foundry/ontology/README.md) (Action, link and page 1 rows), A010, A012.

| | What happens | Why |
|---|---|---|
| The decision object | **Unchanged.** It keeps the old evaluation id, decision, rationale, reviewer and time | The Action is create-only (D040); nothing edits a decision. Decisions are Ontology edits, not pipeline output, so a rebuild does not touch them (baseline gate) |
| Link to the signal | **Still linked** | The Triage Decision → Signal link is the foreign key `subject_key` = `signal_key`. The signal key (drug, reaction, rule) does not contain the evaluation id |
| Page 1 decisions table | **Still listed** under the signal | The variable *Decisions for selected signal* filters on Subject Key, not on evaluation id |
| A "stale" warning | **None.** The screen does not compare the ids, and the change feed does not watch the evaluation id | No such check is built. She sees it only by comparing the id in the decisions table with the id the triage form shows (form opened, then Cancel) |
| If the signal is gone (now in the label) | The decision still exists in Object Explorer (MSSM Triage Decision), but its signal no longer appears on page 1, so neither does the decision. The change feed shows a `snapshot_diff` "gone" event for the signal | Signals are only "not in label" or "possibly in label" rows. What Object Explorer shows for a link whose target is gone is **not tested** |
| If only the bucket changed (row 2) | Nothing: the evaluation id stays the same | `bucket` is not hashed (DECISIONS learning 2026-11-05) |
| Possible live example (unverified) | The Myoclonus test decision stores `cbcd091262d23bd6` (step 8, 2026-11-04, A012). The label check changed twice since (`syn_v1`, `syn_v2`), so the signal's current id should differ | Check in rehearsal pass 1 by opening the form on Oxycodone · Myoclonus and pressing Cancel |

## Summary

| # | Change this here | This changes there | Builds, in order | Officer sees | Eval id moves? | Show live? | How long |
|---|---|---|---|---|---|---|---|
| 1 | Synonym row in `label_synonyms.py` (+ bump `SYN_VERSION`) | label status → signals in/out of the table and the ranked queue → change events | `ontology_signal_signals` → tail | Page 1 queue size; Morning brief card 1; page 3 signal events (build-dated) | **Yes, every signal** (the `label_check` string carries `SYN_VERSION`) | No: show history | not measured |
| 2 | Bucket regex in `BUCKETS`, `ontology_signals.py` | `bucket`, `is_ranked`, rank → ranked queue → change events | `ontology_signal_signals` → tail | Page 1 queue; card 1 | **No** (bucket not hashed) | No: show code | not measured |
| 3 | New FAERS quarter (`QUARTERS` in `raw_faers_quarters.py` + `WINDOW` in `ontology_signals.py`) | case versions, deletes, counts, PRR, every AE Stat key → signals → change events, freshness, drift | raw files → `clean_faers*` (full) and/or `clean_faers_inc_*` → AE stats/signals → tail | Everything on page 1; card 1; FAERS as-of row | **Yes** (a, PRR, window) | No: show the inc log | FAERS clean: 32 s full / 88 s incremental (O2); rest not measured |
| 4 | Identity: add a drug (`INGREDIENTS` in 4 raw files + `FORMULARY` in `clean_drug_identity.py`) | new RxCUI everywhere: products, labels, recalls, FAERS rows → new signals; incremental FAERS replays all quarters | all raw pulls → `clean_drug_identity` → clean FAERS, labels, recalls → `ontology_objects` → AI (only if a pilot label) → signals → tail | New drug in every drug filter; cards 1 and 2 | New signals get new ids; existing ones only if `prr` moves (the background counts change) | No | not measured (DailyMed pull alone: 1 m 23 s, O3) |
| 5 | DailyMed publishes a new label version | new XML downloaded (others reused) → sections → label object → label check re-run → a signal may leave | `raw_dailymed_spl` → `clean_labels` → `clean_label_product_map` → `ontology_objects` → `ai_label_extraction` → signals → tail | Page 3: one build-dated "spl version: n → n+1" event; maybe a signal gone from page 1 | Only if `n_reference_labels` or `ai_labels_checked` changes (**label version and text are not hashed**) | Show the existing version_effective events on page 3 | DailyMed pull 1 m 23 s (O3); rest not measured |
| 6 | openFDA changes a recall's status (Ongoing → Completed or Terminated) | `is_active` → active count → change events | `raw_openfda_enforcement` → `clean_recalls` → `ontology_objects` (`compute_recalls`, `compute_drugs`) → tail | Card 2 drops; page 2 (Is Active = Yes); page 3: one build-dated "status: Ongoing → …" event | n/a | Show the existing "terminated" events on page 3 | not measured |
| 7 | Officer submits a triage decision | new MSSM Triage Decision object (Ontology edit) | **none** | Decision row on page 1; link in Object Explorer | stores the current id | **Only if the owner chooses Submit (A5)**; default Cancel | seconds (not timed) |
| 8 | Prompt or model version (`PROMPT_VERSION`, `MODEL_ID`, `PARSER_VERSION` in `ai_label_extraction.py`) | cache key → all 21 AI sections (5 labels) re-sent to Claude → new extractions + labeled reactions → monitoring cache rate | `ai_label_extraction` (Force) → signals → tail; then `check_gold.py` | Nothing on screen unless the AI terms change a label status | Only if `ai_labels_checked` changes (`label_check` keeps `ai_v1`; the prompt version is not hashed) | No: show the code + `from_cache` | 21 model calls (not measured as one run; the 9 v1-pilot sections took 41,704 + 29,072 tokens, job 2 m 43 s, O1; the 12 semaglutide sections 44,869 + 26,226 tokens, O1b) |
| 9 | A Workshop variable (e.g. *Changes last 30 days*) | that card / table only | **none** (save + publish module) | Card 3 number | n/a | Show the definition only; do not save | seconds |

---

## 1 · A synonym row (D043, A014)

| | |
|---|---|
| **Edit** | `Pipelines/pipelines_clean` → `transforms-python/src/myproject/datasets/label_synonyms.py`: add or re-band a row in `_HIGH` / `_MEDIUM` / `_REJECTED`; bump `SYN_VERSION = "syn_v2"` → `"syn_v3"`. Mirror first in [foundry/pipelines/ontology/label_synonyms.py](../../../foundry/pipelines/ontology/label_synonyms.py), test locally, paste, Commit |
| **Ripple** | `ontology_signals.compute` imports the table → `ontology_label_synonyms` (258 rows today) rewritten → step 3 of the label check (after the AI term and the exact text, l.172–177) finds the label phrase → `ontology_ae_stats.label_status` flips (`high` → `in_label`, `medium` → `possibly_in_label`) → `ontology_signal_signals`: an `in_label` row leaves the signal table; a `possibly_in_label` row stays as a signal, `is_ranked` false, caution `possible_label_synonym` (or `mostly_mass_reports` if that applies first) → `label_check` becomes `text+ai_v1+syn_v3`, so **every** `evaluation_id` changes → MSSM Signal re-indexes → `ontology_change_events`: build-dated `snapshot_diff` events "label status: … → …", "is ranked: true → false", "caution: …", and "gone" for signals now in the label |
| **Builds** | Build `ontology_signal_signals` (writes `ontology_ae_stats`, `ontology_signal_signals`, `ontology_label_synonyms` together) → `ontology_change_events` → `monitoring_checks` |
| **Officer sees** | Card 1 and the page 1 queue shrink; page 3 shows signal events dated by the build; every past decision now carries an older evaluation id ([above](#what-happens-to-an-existing-triage-decision)) |
| **Watch out** | If `SYN_VERSION` is **not** bumped, `label_check` does not change, so the ids of signals whose counts did not move stay the same even though the label check changed. Always bump it |
| **Show it** | Do not rebuild. Show the history (numbers.json `ranked_history`): 1,355 at step 9 → 1,210 (syn_v1) → 1,115 (D016 v3) → 1,073 (syn_v2). On page 1, the record's *Label check method* reads `text+ai_v1+syn_v2` |
| **How long** | not measured |

## 2 · A bucket regex (D016 v3)

| | |
|---|---|
| **Edit** | `ontology_signals.py` → `BUCKETS` (mirror l.32–61): add a keyword to e.g. `efficacy` or `product_use_error`. First match wins; everything else is `clinical` |
| **Ripple** | `bucket` on AE stats and signals → `is_ranked` (ranked = `clinical` **and** mass share < 0.5 **and** `not_in_label`, l.199–200) → `rank_in_bucket` renumbers within each drug → **`evaluation_id` unchanged** → build-dated `snapshot_diff` events on `bucket` and `is_ranked` |
| **Builds** | `ontology_signal_signals` → `ontology_change_events` → `monitoring_checks` |
| **Officer sees** | Page 1 queue changes; signals are tagged, never removed (still in Object Explorer with their bucket). Past decisions keep matching the current evidence |
| **Show it** | H7: point at `BUCKETS` in the code repo. Evidence: D016 v3 took ranked 1,210 → 1,115 with the same signal count and ids (DECISIONS learning 2026-11-05) |
| **How long** | not measured |

## 3 · A new FAERS quarter (D022, D044)

| | |
|---|---|
| **Edit** | `Pipelines/pipelines_raw_ingest` → `raw_faers_quarters.py`: `QUARTERS = ["2026q1", "2026q2", "2026q3"]`. **Also** `ontology_signals.py` → `WINDOW = "FAERS 2026Q1-2026Q3"`: a hand-set constant (a scale gap worth saying) |
| **Ripple** | `raw_faers_quarter_files` + manifest → full path: `clean_faers.py` re-reads every quarter, keeps the highest caseversion per caseid, applies that quarter's deletes to all history (D022) → `clean_faers_cases_current`, `clean_faers_case_reactions`, `clean_faers_drug_reaction` → incremental path (proven equal, not read by signals): the state adds only the new quarter, one row in `clean_faers_inc_log` → `ontology_ae_stats`: new a/b/c/d, PRR, CI; **every `stat_key` changes** (the window is part of it), so all MSSM AE Stat objects are new → `ontology_signal_signals`: same `signal_key`s, new `evaluation_id`s; signals can be new or gone → change events for new / gone / label status / ranked / bucket / caution (not for PRR alone) → `ontology_source_status`: FAERS "through 2026Q3" → monitoring: `faers.freshness`, `faers.incremental_quarters`, `faers.reporter_type_blank`, quarterly drift series |
| **Builds** | `raw_faers_quarter_files` → `clean_faers_cases_current` (builds all 3 clean FAERS outputs) → `ontology_signal_signals` → tail. Incremental: dataset page Build ▾ → **Force** → *Only this dataset* on the state, then outputs (the repo Build skips an unchanged incremental transform) |
| **Officer sees** | Card 1, page 1 counts and ranks, page 3 signal events, the FAERS as-of row; every past decision now carries an older evaluation id |
| **Show it** | Not live. Show `clean_faers_inc_log` ([hood-faers-inc-log-sql.png](../screens/hood-faers-inc-log-sql.png)): "Q2 replaced 26,681 cases and deleted 655" |
| **How long** | Clean FAERS: 32 s full, 88 s incremental (O2). Raw download, signals and the tail: not measured |
| **Note** | FAERS moved to AEMS in March 2026 (DQ20). How future quarters will arrive is not verified |

## 4 · An identity row: a drug is added (D018, D020, D027)

| | |
|---|---|
| **Edit** | The formulary is a list in 5 files: `INGREDIENTS` in `raw_openfda_enforcement.py`, `raw_openfda_products.py`, `raw_dailymed_spl.py`, `raw_rxnorm.py` (repo `pipelines_raw_ingest`) and `FORMULARY` in `clean_drug_identity.py` (repo `pipelines_clean`). Production would make it one formulary dataset |
| **Ripple** | raw pulls gain the drug's recalls, products, NDCs, labels and RxNorm rows → `clean_drug_ingredients`, `clean_drug_identity` (new lookup strings), product and package maps → FAERS: `clean_faers_drug_reaction` gains the drug's suspect rows; the incremental state sees a new identity hash and **replays every quarter** (`clean_faers_incremental.py` l.90) → labels → `ontology_objects`: new MSSM Drug, Products, Labels, Recalls and links → `ontology_signal_signals`: the drug's signals; other drugs' PRR can shift because their "other drugs" counts change → change events: its recalls and labels are new to the feed, so they arrive with their **real source dates**; its signals arrive as build-dated `new` |
| **Builds** | all raw pulls → all clean → `ontology_objects` (all curated outputs) → `ontology_signal_signals` → tail. AI only if a new label is added to `PILOT_SETIDS` |
| **Officer sees** | A new value in every drug filter (pages 1, 2, 3); cards 1 and 2 grow |
| **Show it** | Not live. Diagram 37; local test: suspect rows 79,270 → 77,677 → 79,270 when identity was changed and restored (diagram 37 source) |
| **How long** | not measured (the DailyMed pull alone is 1 m 23 s after O3) |

## 5 · DailyMed publishes a new label version (D019, D047)

| | |
|---|---|
| **Edit** | none: it arrives from the source |
| **Ripple** | `raw_dailymed_spl_index` lists the new (setid, version) → `raw_dailymed_spl_xml` downloads only that XML (the rest is reused, O3) → `clean_label_versions` / `clean_label_sections` → `clean_label_product_map` (reference label per product) → `ontology_label_labels`: new `label_key` = `setid|v<new>` → if the setid is one of the 5 `PILOT_SETIDS` (2 oxycodone, 3 semaglutide): the version is part of the cache key, so **every** section of that label gets a new key and a model call, not only the changed ones (`ai_label_extraction.py` l.85–86, l.140) → `ontology_labeled_reactions` → `ontology_signals` re-runs the label check on the new text: a reaction now mentioned leaves the signal list → change events: one build-dated `snapshot_diff` event "spl version: n → n+1" for the setid. **No new source-dated "version_effective" event**, because the setid was already seen (key fact 3); a signal that leaves shows as `gone` |
| **Builds** | `raw_dailymed_spl` → `clean_labels` → `clean_label_product_map` → `ontology_objects` → `ai_label_extraction` → `ontology_signal_signals` → tail |
| **Officer sees** | Page 3: "spl version: n → n+1", dated the build day; maybe one signal fewer on page 1 |
| **Show it** | **Live, no build:** page 3 → Entity type = label, Change = version_effective (1,231 such events, all from the first build: the 1,231 of 1,321 label versions that carry an effective date, `ontology_changes.py` l.90). Point at "liraglutide label version 11 effective, Oct 30" |
| **Honest note** | The evaluation id does not include the label version or text. A signal whose label changed without changing its status keeps the same id, so a past decision on it looks current. Adding the reference label versions to the hash is a one-line change (proposal for the owner, not built) |
| **How long** | DailyMed pull 1 m 23 s (O3); rest not measured |

## 6 · A recall status change (openFDA)

| | |
|---|---|
| **Edit** | none: it arrives from the source |
| **Ripple** | `raw_openfda_enforcement` (full snapshot) → `clean_recalls_current` (latest pull wins; `is_active` = status **Ongoing**, `clean_recalls.py` l.69) → `ontology_recall_recalls`: `status`, `is_active`, termination date; `ontology_drug_drugs.n_active_recalls` → MSSM Recall re-indexes → change events: one build-dated `snapshot_diff` event "status: Ongoing → Terminated" (or Completed). **No source-dated "terminated" event**, because the recall number was already seen (key fact 3) → monitoring: openFDA freshness, recall row count, weekly recall drift |
| **Builds** | `raw_openfda_enforcement` → `clean_recalls_current` → `ontology_objects` → tail |
| **Officer sees** | Card 2 (126) drops by one; the recall leaves page 2 while Is Active = Yes; page 3 shows the status event on the build day |
| **Show it** | **Live, no build:** page 3 → Change = terminated (767 source-dated events from the first build) |
| **How long** | not measured |

## 7 · A triage decision (the Action)

| | |
|---|---|
| **Edit** | Workshop page 1 → **Triage this signal** → Decision + Rationale → Submit (Action `create-mssm-triage-decision`). **Demo default: Cancel**; Submit only if the owner chose it before the demo |
| **Ripple** | A new **MSSM Triage Decision** object stored as an Ontology edit (the backing dataset `ontology_triage_decisions` stays at 0 rows on purpose) with Subject Key, Evaluation Id, Decision, Rationale; Reviewer = current user, Decided At = current time (system-set) → *Decisions for selected signal* → page 1 decisions table → Object Explorer: the signal's link *MSSM Triage Decisions* |
| **Does not change** | The signal, its rank, the Morning brief cards or the change feed (the feed watches signals, recalls and labels only). Survives every rebuild (baseline gate) |
| **Cannot be undone** | Create-only: no edit or delete Action exists. A demo Submit leaves a permanent object |
| **Who** | Only the project owner can submit today |
| **Builds** | none |
| **Show it** | Form opened and cancelled (A5). Saved decisions: Object Explorer → MSSM Triage Decision (2 test decisions) |
| **How long** | seconds (not timed) |

## 8 · Prompt or model version (cache key, D005, O1)

| | |
|---|---|
| **Edit** | `ai_label_extraction.py`: `PROMPT_VERSION = "p2"` → `"p3"`, or `MODEL_ID`, or `PARSER_VERSION`. A new model also needs a new RID in `GenericCompletionLanguageModelInput(...)`, and the model must be **imported into the project** first (DECISIONS learning 2026-11-04) |
| **Ripple** | `cache_key` = setid, version, section, content hash, parser, prompt, model → every key is new → all 21 AI sections (5 labels) are sent to Claude again → `ai_label_section_extractions`: `from_cache = false`, new `called_at`, tokens → `ontology_labeled_reactions`: new keys (they end in `model.prompt`) → MSSM Labeled Reaction → `ontology_signals` re-reads AI terms (check 1) → `monitoring_checks`: `ai.cache_hit_rate` drops to 0 for that build (expected); `ai.grounded_rate` re-checked (fail < 0.95) |
| **Accept only after** | `check_gold.py` re-scores against the frozen answer key (35 items, Boxed Warning + Contraindications of the 2 oxycodone labels, [eval](../../../eval/ai-eval-v1.md)) |
| **Builds** | `ai_label_section_extractions` (dataset page, Build ▾ Force) → `ontology_signal_signals` → tail |
| **Officer sees** | Usually nothing: today the AI terms do not change any label status (A012) |
| **Honest note** | `label_check` says `ai_v1` whatever the prompt version, so a decision cannot tell which prompt's terms it saw |
| **Show it** | H9: `PROMPT_VERSION`, `MODEL_ID` in code ([hood-code-ai-label-extraction.jpg](../screens/hood-code-ai-label-extraction.jpg)), `from_cache = true` in the SQL result |
| **How long** | 21 model calls (not measured as one run). Measured parts: the 9 v1-pilot sections, first run 41,704 prompt + 29,072 completion tokens, job 2 m 43 s (O1); the 12 semaglutide sections, 44,869 + 26,226 tokens (O1b; numbers.json `ai.d041_v2`) |

## 9 · A Workshop variable

| | |
|---|---|
| **Edit** | Workshop module **MSSM Safety Officer** → Edit mode → Variables: e.g. *Changes last 30 days* (Event Date from 30 days ago, relative to today), *Ranked signals* (Is Ranked = true), *Active recalls* (Is Active = true) |
| **Ripple** | Only widgets reading that variable: card 3, or card 1 + page 1 table + drug filter, or card 2 + page 2. No data changes, no build |
| **Publish** | Save, then publish a new module version (v0.10.0 today) |
| **Show it** | Only if asked: open Edit mode and show the definition. **Do not save** a published module during the demo. The safe live version is the page 3 date filter (A7) |
| **How long** | seconds |
