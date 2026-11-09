# 📒 Activity log — read this first when you come back

## ⏩ Pick up here (always current)
| | |
|---|---|
| **Last session** | 2026-11-09 — Demo 1 debrief logged; Demo 2 plan v1 made (Compass v42) |
| **Where we are** | Demo 1 done. Boss feedback in the [meeting note](docs/03-meetings/2026-11-09-demo1-boss-feedback.md). Demo 2 = 6 gates in [demo2-plan-v1](docs/10-delivery/demo2-plan-v1.md) ([diagram](docs/diagrams/png/40-demo2-plan-v1.png)) |
| **Next 3 actions** | 1. (you) Confirm the Demo 1 date and add any missing boss points to the meeting note · 2. (you) Commit on `demo2` (branch created 2026-11-09, D051) · 3. (Claude) Start M1: trace the top-PRR outlier in Foundry (read-only SQL) and, in parallel, M3 officer-workflow research |
| **Waiting on** | D050 OK after the T5.0 OSDK spike · pharmacist reviewer |
| **Say this to Claude to restart** | _"Read ACTIVITY-LOG and the Demo 2 plan; start M1: find and trace the top-PRR outlier."_ |

---

### Previous pick-up box (2026-11-08)
| | |
|---|---|
| **Last session** | 2026-11-08 — grand tutorial book + live SQL cookbook on local branch `demo-prep` (Compass v41) |
| **Where we are** | Hand-in set unchanged on main. On `demo-prep`: [cue card](docs/12-demo-prep/cuecard.html) (open on 2nd screen, ← →), [narrative](docs/12-demo-prep/narrative.md), [tutorial](docs/12-demo-prep/tutorial.pdf), skill `foundry-demo` |
| **Next 3 actions** | 0. (you) Read the [book](docs/12-demo-prep/book/book.pdf) track by track; decide the 5 open items in [00-review.md](docs/12-demo-prep/book/00-review.md) · 1. (you) Rehearse once with the cue card against live Foundry (the 3 checks: DailyMed "optic", Class I count, stopwatch) · 2. (you) Fix the Foundry project description ("opioids" → 13 drugs) · 3. (you) Commit on `demo-prep` (local only); main still needs its own commit + push |
| **Waiting on** | A rehearsal against live Foundry · pharmacist reviewer |
| **Say this to Claude to restart** | _"Use the foundry-demo skill: rehearse the demo with me, one stop at a time."_ |

---|---|
| **Last session** | 2026-11-06 — README rewritten for outside reviewers, repo-wide link/number check, reviewer sharing guide (Compass v39) |
| **Where we are** | Pilot built and refreshed: the AI now reads the demo drug's labels and its quotes are on page 1 (Workshop v0.10.0). Hand-in set: [R00 Start here](docs/11-handin/reports/pdf/R00-start-here.pdf) → [architecture note](docs/11-handin/architecture-note/architecture-note.pdf) → [deck](docs/11-handin/deck/MSSM-demo-deck.pdf) + [script](docs/11-handin/deck/speaking_script.md) → [demo guide](docs/11-handin/demo/demo-navigation-guide.md) → reports R01–R09 |
| **Next 3 actions** | 1. (you) Invite Etter in Foundry ([guide](docs/10-delivery/sharing-with-reviewers.md)), then send Etter the repo + resume email, ask for Mon Nov 9, 12 PM · 2. (you) One commit + push · 3. (you + Claude) Rehearsal with the 3 checks |
| **Waiting on** | A rehearsal against live Foundry · pharmacist reviewer |
| **Say this to Claude to restart** | _"Read ACTIVITY-LOG and COMPASS; help me rehearse the demo against live Foundry."_ |

---

## Log (newest first)

### 2026-11-09 — Demo 1 debrief + Demo 2 plan v1 (Compass v42)
- **Logged:** boss feedback ([meeting note](docs/03-meetings/2026-11-09-demo1-boss-feedback.md)): incremental setup + compute cost per change; ontology in depth + cost refactor; PRR outlier (sorted by PRR) and how we know metrics are right; data-engineering cost; officer workflow UI (colours, "X of Y reviewed", critical flags, "?" help, outlier/cost/lineage reachable, React linked to Palantir).
- **Decided (your answers):** UI = React + OSDK (new **D050**, proposed until the T5.0 spike); no fixed Demo 2 date; Claude finds the outlier row.
- **Made:** [demo2-plan-v1.md](docs/10-delivery/demo2-plan-v1.md) (6 gates, ~18 h you, ~80 h Claude) · diagram [40 v1](docs/diagrams/png/40-demo2-plan-v1.png) · BACKLOG v5 (Demo 2 rows; H2 superseded) · 2 learnings in DECISIONS · Compass v42 (history v41 saved).
- **Branch (D051):** Demo 2 work on `demo2` from main; the project record (Compass, decisions, logs, approaches, diagrams) copied over from `demo-prep`; the demo-prep pack itself stays on local `demo-prep`. Links into `docs/12-demo-prep/` only work on that branch.
- **Git gotcha:** after `git switch` was refused (dirty files), `git checkout demo-prep -- <files>` silently overwrote the uncommitted D051 edits; Claude re-applied them on `demo2`.
- **Not changed:** Foundry, numbers.json, hand-in set.

### 2026-11-08 (2) — Grand tutorial book + live SQL (Compass v41)
- **Book** ([book.html](docs/12-demo-prep/book/book.html) · [book.pdf](docs/12-demo-prep/book/book.pdf), 263 pages): 01 ground zero · 02 data sources attempt by attempt · 03 every transform · 04 ontology in depth · 05 how our thinking changed · 06 AIP/LLM before vs after · 07 SQL cookbook. Written by 7 parallel agents; 1 reviewer fixed 25 issues and left 5 open ([00-review.md](docs/12-demo-prep/book/00-review.md)). Builder [build_book.py](tools/demo_prep/build_book.py) (markdown 3.7 added to .venv).
- **SQL live (read-only, Claude in Chrome):** 20 queries, screenshots in `docs/12-demo-prep/shots/sql/`. All match numbers.json except: Class I active = 6 (new), 20 vs 22 change events (time zone?), `method` reserved alias.
- **Cue card:** timer and Start button removed; shows stop N / 23. A6 now says 6 Class I.

### 2026-11-08 — Demo-prep pack on local branch `demo-prep` (Compass v40)
- **Made** ([A020](docs/05-approaches/A020-demo-prep-skill-and-cue-card.md), D049): skill [foundry-demo](.claude/skills/foundry-demo/SKILL.md); single content file [content.py](tools/demo_prep/content.py) + builder [build_all.py](tools/demo_prep/build_all.py); [cuecard.html](docs/12-demo-prep/cuecard.html) (23 stops, timer); [tutorial.html](docs/12-demo-prep/tutorial.html) / [.pdf](docs/12-demo-prep/tutorial.pdf) (12 chapters); [narrative.md](docs/12-demo-prep/narrative.md) + 5 [explainers](docs/12-demo-prep/explainers/); diagram [39 v1](docs/diagrams/png/39-demo-prep-pack-v1.png).
- **Foundry (read-only, Claude in Chrome):** 32 captures; triage form opened and cancelled; nothing built, saved or edited.
- **Seen:** card 3 = 22 (was 26 on 5 Nov; rolling 30 days); project description still says "Pilot focus: opioids"; 2 object types at project root. 3 learnings added.
- **Not changed:** numbers.json, hand-in PDFs, deck.

### 2026-11-06 (13) — README for outside reviewers + repo check (Compass v39)
- **README rewritten** ([README.md](README.md)): "Reviewing this project? Start here" path (R00 → note → R02 → R06 → R07 → R09), headline numbers from [numbers.json](docs/11-handin/numbers.json), a data engineering table, "Run it yourself", known gaps (pharmacist, self-scored AI, syn_v3 ahead of Foundry). Old status was Compass v22.
- **Repo check:** every relative link in .md files resolves, except in the archived `proposals/2026-10-28-codex-draft/` (not adopted; left as is) and COMPASS history snapshots (root-relative links; archival). Stale numbers fixed: [rehearsal-plan.md](docs/11-handin/demo/rehearsal-plan.md) "AI on 2 labels" → 5; [foundry/README.md](foundry/README.md) status table; COMPASS "(proposed)" labels on decisions accepted 6 Nov, and a duplicate v38 change-log row (now v39).
- **New:** [sharing-with-reviewers.md](docs/10-delivery/sharing-with-reviewers.md). Checked in Foundry: plan allows 5 users; invite via Control Panel → Manage users → Add new user; org `kestrel` gets Viewer on the project by default; Workshop link recorded.
- **Not changed:** numbers.json, hand-in PDFs, Foundry.

### 2026-11-06 — Reusable kickoff prompt for a website project
- **Made:** [website-project-kickoff-prompt.md](docs/13-reuse/website-project-kickoff-prompt.md): paste-ready prompt that carries this project's rules (manual git, Compass, activity log, decisions vN, approaches, diagrams, personas, backlog) to a website repo, plus a new technical-scoping section (SCOPE.md).
- **Not changed:** Compass, decisions, hand-in set. Outside the Soragence hand-in.

### 2026-11-06 — Batch decision: 12 accepted, D041 v2 built, duplicate link deleted (Compass v38)
- **Decisions:** you accepted D006, D015 (target only; benchmark stays cut), D025–D029, D037, D045–D048, and D041 v2 ([DECISIONS](docs/06-decisions/DECISIONS.md) change rows). Pharmacist stays a documented gap.
- **D041 v2 in Foundry** ([A019](docs/05-approaches/A019-widen-ai-to-semaglutide.md)): `PILOT_SETIDS` + 3 semaglutide labels → 21 sections, 745/745 quotes grounded; 12 model calls (44,869 + 26,226 tokens), then a forced rebuild made 0 calls (21/21 cached, O1b). Signals unchanged (1,952 / 1,073; change feed 0 signal changes). NAION: labels also read by AI = 3; the AI found retinopathy terms but no optic-nerve term. Monitoring run 3: grounded 1.0, 0 section errors.
- **Workshop v0.10.0:** page 1 has a new table "What the AI read in these labels" (reaction · section · word-for-word quote · label). First version squeezed the triage button; fixed with *Enable scrolling* on the evidence section. Screens: [app-1d](docs/11-handin/screens/app-1d-naion-ai-read-3.jpg), [app-1e](docs/11-handin/screens/app-1e-ai-quotes-panel-naion.jpg).
- **Ontology:** duplicate Signal → Drug link type deleted after checking no Workshop variable used it; 10 MSSM link types.
- **Docs:** [numbers.json](docs/11-handin/numbers.json) updated (D041 v2 keys), optimization log O1b, [eval](eval/ai-eval-v1.md) D041 v2 section, ontology/AI READMEs, 4 learnings; hand-in reports, deck, demo guide and diagrams refreshed by one agent.

### 2026-11-06 (12) — syn_v3: Allodynia → "dysesthesia" (Compass v38)
- **Changed:** [label_synonyms.py](foundry/pipelines/ontology/label_synonyms.py): new medium row, Allodynia removed from the rejected list, `SYN_VERSION = "syn_v3"`. Local only.
- **Measured (local re-run):** signals 1,952 (same) · ranked 1,073 → 1,072 · possibly in label 108 → 109. Only Tirzepatide · Allodynia (#5) changed status ([A014 update](docs/05-approaches/A014-label-faers-synonym-table.md)).
- **Found:** 27 ranked signals in other drugs swapped rank because of tied chi² (no tie-break) → [DQ43](docs/07-data-quality/data-issues-register.md), learning in DECISIONS.
- **Not done:** Foundry push and re-freezing [numbers.json](docs/11-handin/numbers.json). The hand-in set still quotes syn_v2 numbers on purpose.

### 2026-11-05 (evening, 11) — F01 run v2: 3 more public sources
- **Re-ran the 6 samples** with Europe PMC, FDA "Potential Signals of Serious Risks" (70 quarterly pages, 785 rows) and OnSIDES v3.1.1 (85 MB, CC BY 4.0). New tool [research_sources.py](tools/lit_review/research_sources.py). Results: [rerun-v2-multi-source.md](docs/12-features/ai-literature-review/samples/rerun-v2-multi-source.md).
- **Result:** no verdict flipped. FDA listed NAION (Q4 2024) and Dysaesthesia (Q1 2024) for the GLP-1 class, so samples 01 and 04 are stronger. Europe PMC: 0 new on-topic papers.
- **Learned:** FDA's list is the best add-on. FDA wording ≠ MedDRA terms, so a formulary-wide check needs a mapping table (like A014). OnSIDES has thin GLP-1 coverage (tirzepatide: 0 US labels).
- Compass not bumped (exploration only).

### 2026-11-05 (evening, 10) — Exploring F01: AI review backed by papers
- **Idea:** no pharmacist reviewer is available, so: an AI reads PubMed for the officer's watch list and writes a cited verdict; a pharmacist signs it later. New [feature folder](docs/12-features/ai-literature-review/README.md), [A018](docs/05-approaches/A018-ai-literature-review.md) (Trying, not in pilot scope).
- **Samples (6):** 2 real (semaglutide NAION, tirzepatide allodynia) · 1 plausible, FAERS evidence only (semaglutide cyclic vomiting) · 3 noise or not enough evidence (fentanyl anaesthesia-context term, morphine Ewing's = confounding by indication, buprenorphine SMA syndrome). [FINDINGS](docs/12-features/ai-literature-review/FINDINGS.md).
- **Learned:** tirzepatide · Allodynia is probably a synonym miss (Zepbound label lists "dysesthesia"); syn_v3 row proposed, not added (DECISIONS learning).
- **Cost:** ~$0.09/review on Opus 5.5 (estimate); 25-signal watch list ≈ $2.20 + ~50 pharmacist minutes ([cost-estimate](docs/12-features/ai-literature-review/cost-estimate.md)).
- **New tool:** [tools/lit_review/fetch_evidence.py](tools/lit_review/fetch_evidence.py) (NCBI E-utilities, free). PubMed connector not connected; same database.
- Compass not bumped (exploration only; no phase, scope or decision change).

### 2026-11-05 (day, 9) — Hand-in Phase D: review → fix loop (Compass v37)
- **Reviews** (all in [docs/11-handin/reviews](docs/11-handin/reviews/)): first-time reader (no front door, mixed label meanings, no drug-safety primer); fact-check (6 wrong · 17 stale · 7 inconsistent · 3 unsourced); 💊 safety officer (traces stopped one click short of the source; recall wording implied inventory data; unmeasured "under two minutes"); cohesion check (17 wording mismatches, all numbers consistent); evaluator re-score v2.
- **Fixed:** one wording for every term ([phase-d-fix-brief](docs/11-handin/reviews/phase-d-fix-brief.md)); new [R00 Start here](docs/11-handin/reports/pdf/R00-start-here.pdf); R01 drug-safety primer; R04 now a click-by-click user guide + editor guide; label legend fixed in the style kit; architecture note corrected (still 1 page); deck: DailyMed click + openFDA tab are now required trace stops; demo guide: ripple table checked against the code.
- **Diagrams v2:** 30 (O3 measured), 32 (label checks in code order), 36 (demo map, 23 stops), 37 (ripple map: decisions stay linked, no stale flag = known gap).
- **Learned:** NAION is a known positive — EMA PRAC (6 Jun 2025) and WHO (27 Jun 2025) call it a very rare semaglutide side effect; our 3 US labels do not mention it (DECISIONS learning). The real proposed list is 12 decisions, not 6. An existing triage decision gets no "stale" flag when its evidence changes.
- **Register:** DQ04 and DQ06 marked "left as a known gap"; DQ38 34% (Foundry) vs 35% (profile) noted. Optimization log: partitioning row (D048, proposed).
- **Moved:** style sample PDF to [tools/handin/sample](tools/handin/sample/R00-sample.pdf), out of the hand-in folder.

### 2026-11-05 (morning, 8) — Baseline gate passed; O3; hand-in agents (Compass v36)
- **O3 (D047):** DailyMed pull reuses XML already held for the same setid + version → 1 m 23 s (was 3 m 23 s), 2 downloads (was 1,321). O3a column pruning tried, no real gain, reverted. [Optimization log](docs/08-optimization-log/optimization-log.md).
- **AI eval:** [eval/ai-eval-v1.md](eval/ai-eval-v1.md): strict recall 35/35, precision ≤ 35/37, F1 0.97 (target 0.85), grounded 448/448; limits stated.
- **Gate:** full downstream rebuild (8 builds) → counts equal, 0 new change events, AI 0 model calls, 2 triage decisions survive, Data Health checks passed; 5/5 random flags traced to FAERS rows and label text. [baseline-gate.md](docs/11-handin/baseline-gate.md), [numbers.json](docs/11-handin/numbers.json), 13 [screenshots](docs/11-handin/screens/README.md).
- **Workshop v0.8.0:** module title MSSM, page 2 section titles.
- **Agents:** style kit done ([tools/handin](tools/handin/README.md)); diagram set v1 done ([README-handin](docs/diagrams/README-handin.md), 30–37 + draw.io); running: rubric check, reports R01–R08, architecture note, deck, demo guide ([shared brief](docs/11-handin/AGENT-BRIEF.md)).

### 2026-11-05 (early, 7) — Step 11: three-question screen + monitoring (Compass v35)
- **Change feed (D045):** [ontology_changes.py](foundry/pipelines/ontology/ontology_changes.py) → 2,898 dated events (recalls reported/terminated, label versions) + build-to-build diff of signals/recalls/labels; `ontology_source_status`. No-change build adds 0; planted change gives exactly 3 events. New objects MSSM Change Event, MSSM Source Status.
- **Screen:** pages 0 · Morning brief (metric cards 1,073 · 126 · 26 + as-of table), 2 · Recalls (filter through the Recall↔Drug link), 3 · What changed (date range = since my last review); header tabs. [foundry/ontology README](foundry/ontology/README.md).
- **Monitoring (D046):** [monitoring.py](foundry/pipelines/monitoring/monitoring.py): 21 checks per build + drift replay; grounded 448/448; warnings: reporter type blank 34%→72% (DQ38), recalls ×3.3 in 4 weeks. 4 Foundry Data Health checks ([record](foundry/monitoring/README.md)). DailyMed pull retries 429s (committed in Foundry, not yet rebuilt).
- **Mistake:** a duplicate Signal→Drug link type was created; recorded, not deleted.
- **Agents:** research on sources + pharmacist review done → [another-month file](docs/09-roadmap/another-month-sources-and-pharmacist-review.md); style kit running. New persona files in `.claude/agents/` (researcher, report-writer, deck-designer, demo-director, first-time-reader, fact-checker).

### 2026-11-05 (early, 6) — D044 accepted (Compass v34)
- You accepted D044 (incremental FAERS beside the full rebuild; signals keep the full rebuild until incremental is measured faster). No code change.

### 2026-11-05 (early, 5) — Step 10: incremental FAERS (Compass v33)
- **Built:** [clean_faers_incremental.py](foundry/pipelines/clean/clean_faers_incremental.py) (state + per-quarter log; one new quarter per build; replay on identity change). [clean_faers.py](foundry/pipelines/clean/clean_faers.py) now shares its rules as `suspects()` and `finish()`; its output is unchanged. Local runner reads "previous" outputs ([run_local.py](foundry/tools/local_run/run_local.py)).
- **Gate (Foundry SQL, EXCEPT ALL both ways):** 0 differences in all 3 outputs (792,346 / 2,554,017 / 373,522 rows). Q2 replaced 26,681 cases and deleted 655. Replay tested locally only.
- **Measured:** full rebuild 32 s; incremental add-Q2 88 s (state 62 s + outputs 26 s). Not faster at 2 quarters → signals keep the full rebuild (O2).
- **Decided:** D044 proposed. Docs: [A015](docs/05-approaches/A015-incremental-faers.md), DECISIONS (5 learnings), optimization log O2, READMEs, Compass v32 snapshot → v33.

### 2026-11-05 (early, 4) — Synonym table syn_v2 (Compass v32)
- **Review:** top 12 ranked signals per drug; each candidate phrase checked in that drug's reference labels before banding. 3 high, 18 medium, 2 rejected ([label_synonyms.py](foundry/pipelines/ontology/label_synonyms.py), A014 update).
- **Result (local = Foundry):** ranked 1,115 → **1,073**; possibly-in-label 72 → 108; signals 1,959 → 1,952; 0 duplicate keys; label check `syn_v2`.

### 2026-11-05 (early, 3) — Drug filter on the screen (Compass v31)
- **Built:** filter list (pill "Ingredient Name", ranked counts per drug) above the table; new variable *Ranked signals for chosen drugs* = *Ranked signals* + filter; table re-pointed (columns and sort kept). Published.
- **Tested in View mode:** choosing semaglutide shows only semaglutide in rank order: NAION #1, Gastrointestinal hypomotility #2, Weight increased #3. Notes in [foundry/ontology README](foundry/ontology/README.md#workshop-module), A012 update.

### 2026-11-05 (early, 2) — D016 v3 buckets (Compass v29)
- **Changed:** wider efficacy / product-use / abuse / social / administrative patterns in [ontology_signals.py](foundry/pipelines/ontology/ontology_signals.py) (list in DECISIONS, D016 v3, accepted by you). Kept clinical on purpose: weight increased, eating-behaviour terms, fall.
- **Result (local = Foundry):** ranked 1,210 → **1,115**; signals 1,959 unchanged; 0 duplicate keys; evaluation ids unchanged. NAION is now #1 for semaglutide; "Gastrointestinal hypomotility" (#2) is a synonym-v2 candidate.
- **Docs:** A013 follow-up section, DECISIONS (D016 v3 + learning), READMEs, Compass v28 snapshot → v29.

### 2026-11-05 (early) — Label ↔ FAERS synonym table (Compass v27)
- **Local replica:** the whole 13-drug pipeline now runs on this machine and equals Foundry. Found on the way: DailyMed rate-limited the local pull (HTTP 429 for 744 labels, recorded as error rows, refetched slowly); the runner's reader needed full-row type scanning.
- **Leads → table:** [synonym_candidates.py](foundry/tools/local_run/synonym_candidates.py) found leads for 232 of 1,550 unlabeled clinical terms; I reviewed 209 into [label_synonyms.py](foundry/pipelines/ontology/label_synonyms.py) (64 high rows, 54 medium, 115 rejected; [leads-v1.txt](eval/synonyms/leads-v1.txt)). Also fixed 3 missing US spellings.
- **Result (same data):** ranked 1,355 → 1,346 (spelling) → **1,210** (synonyms); 72 "possibly in label". Foundry equals local exactly. New dataset `ontology_label_synonyms`.
- **Finding:** NAION is in no semaglutide label (0 of 36 safety sections) and stays ranked 2nd, so it is a real unlabeled signal.
- **Decided:** D043, accepted by you (Compass v28). Docs: [A014](docs/05-approaches/A014-label-faers-synonym-table.md), DECISIONS (4 learnings), READMEs, DQ09 updated.

### 2026-11-04 (night, 8) — Step 9: 13-drug formulary end to end (Compass v26)
- **Changed:** `INGREDIENTS` in the 4 raw API pulls → 13 drugs; `in_slice` true for all 13 ([clean_drug_identity.py](foundry/pipelines/clean/clean_drug_identity.py)). Edited in Foundry with find-and-replace, committed in both repos.
- **Raw = source** for every drug: recalls 930 rows (900 recalls), Drugs@FDA 663, NDC 1,824, DailyMed 1,321 labels; 0 error rows; ~50 openFDA calls, so no API key needed yet.
- **Bug found:** DailyMed answered HTTP 200 with the text "None" for 2 tramadol labels, and the label build crashed. Fixed in [clean_labels.py](foundry/pipelines/clean/clean_labels.py) (DQ42).
- **Result:** FAERS 373,522 drug-reaction rows; 14,921 stats → 2,047 signals (1,355 ranked). Oxycodone identical to step 8 (the test decision still matches). Semaglutide reports 21,034 = Oct 20 walkthrough. 0 duplicate keys; AI cache 0 calls; Ontology re-indexed.
- **Seen:** for GLP-1s, synonym misses and efficacy terms top the list; NAION is ranked 3rd for semaglutide. Decided: D031 v5 (13 drugs, via G1). Docs: [A013](docs/05-approaches/A013-widen-to-formulary.md), DECISIONS, READMEs, DQ42.

### 2026-11-04 (night, 7) — Workshop polish v0.3 (Compass v25)
- **Numbers:** PRR 1 decimal, CI 2, χ² 1, mass share 2. Set as number format on the MSSM Signal properties in Ontology Manager; the stored values are unchanged.
- **Decisions table:** fixed 160 px height (it was collapsed); columns Decided at · Decision · Reviewer · Rationale · Evaluation id.
- **Evidence list:** 22 rows in reading order with plain labels (why flagged → label check → trace). Edited through the widget JSON config (learning logged).
- **Checked in View mode:** Myoclonus shows PRR 15.2 (CI 9.36–24.8), χ² 201, 33 labels searched, and the step 8 test decision.
- **Not done:** the label quote does not apply to "not in label" signals; the plan is to link each signal to the labels searched. Reviewer shows a user ID.

### 2026-11-04 (night, 6) — Step 8 done: Workshop screen + triage (Compass v23)
- **Built:** Workshop module **MSSM Safety Officer** in `Workshop/` (published v0.2.0). Left: ranked signals (125, sorted by rank, plain column names). Right: *Triage this signal* button → Create MSSM Triage Decision with Subject Type / Subject Key / Evaluation Id filled from the selected signal and locked; decisions for that signal; full signal record. Details: [foundry/ontology README](foundry/ontology/README.md#workshop-module).
- **Gate:** selected *Oxycodone · Myoclonus* → submitted "reviewing" (rationale marked STEP 8 WORKSHOP TEST) → "Edits successfully applied" → full reload → row still there (decided 8:19 PM, evaluation id `cbcd091262d23bd6`) ✅.
- **Accepted by you:** D023 v2, D016 v2, D042 (Compass v24).
- **Docs:** [A012](docs/05-approaches/A012-signal-statistics-and-workshop.md); DECISIONS: **D042**, **D023 v2**, **D016 v2** (all proposed, need your OK) + 4 learnings; foundry READMEs (curated RIDs, new object types and links, Workshop); Compass v22 snapshot → v23.
- **Open polish:** PRR shows 12 decimals; decisions table too short; "Toothache"-type noise still ranked → synonym table + pharmacist read.

### 2026-11-04 (night, 5) — Step 8 started (not finished)
- **Built:** [ontology_signals.py](foundry/pipelines/ontology/ontology_signals.py) in `pipelines_clean` → `ontology_ae_stats` 1,382 rows, `ontology_signal_signals` 271 (125 ranked, 80 with "mostly_mass_reports" caution). PRR matches the Oct 20 prototype (Drug dependence a=506, PRR 114.7). Label check: 127 AI-term matches, 87 text matches.
- **Found:** a Canadian mass-polypharmacy cluster (465 of 3,408 oxycodone cases have ≥30 drugs; median 122 drugs, ages changing) put pemphigus, rheumatic fever etc. at the top. D023's exact-person rule misses it. Fix in code (proposed **D023 v2**, needs your OK): reports with ≥30 drugs leave the primary population; their counts stay visible. D016 buckets widened (social/legal, counterfeit, developmental, administrative).
- **Ontology:** object types MSSM Signal, MSSM AE Stat; links Signal→Drug, AE Stat→Drug, Signal→AE Stat, Triage Decision→Signal (on subject_key). Saved.
- **Incident:** the browser resized mid-step and the signals code was pasted into `ai_label_extraction.py`; restored to p2 before any build (master verified clean).
- **Not done:** Workshop screen; docs (A012, D023 v2, Compass bump); mirror READMEs.

### 2026-11-04 (night, 4) — Prompt p2: one reaction per item (Compass v22)
- **Changed:** `PROMPT_VERSION` p1 → **p2** in [ai_label_extraction.py](foundry/pipelines/ai/ai_label_extraction.py). New rules: split lists, name included sub-conditions, list risk headings, drop severity words, no mechanisms or programmes. The new cache key meant 9 fresh calls, as intended.
- **Result:** 448 reactions, **448/448 quotes exact**. Strict recall on the 4 short gold sections: **0.31 → 1.00**; extras: "adverse drug effects", "liver transplant". 44.6k prompt / 45.2k completion tokens, 202 s. Scorer now has `--strict` ([check_gold.py](foundry/tools/local_run/check_gold.py)); details in [A011](docs/05-approaches/A011-ai-label-extraction-pilot.md) and the [run notes](eval/gold-set/runs/step7-run1-notes.md).

### 2026-11-04 (night, 3) — Step 7: AI label extraction pilot (Compass v20)
- **Built:** [ai_label_extraction.py](foundry/pipelines/ai/ai_label_extraction.py) in `pipelines_clean` (lightweight, incremental). Libraries `palantir_models` + `language-model-service-api` added. Model **Claude Sonnet 5.5** imported into the project (your OK). Outputs `ai_label_section_extractions` (9) and `ontology_labeled_reactions` (403). New object type **MSSM Labeled Reaction**, linked to MSSM Label.
- **Run 1:** 9/9 sections `ok`, 403 reactions, **403/403 quotes found exactly**. 41.7k prompt + 29.1k completion tokens, 143 s model time.
- **Gold:** [step7-pilot-gold-v1.json](eval/gold-set/step7-pilot-gold-v1.json), frozen before scoring. Recall **32/35 = 0.91** on the 4 short sections ([notes](eval/gold-set/runs/step7-run1-notes.md)). Misses: paralytic ileus ×2, hepatotoxicity. The model groups terms ("addiction, abuse, and misuse"), so prompt p2 will split them.
- **Cache (gate):** after forcing an upstream rebuild with the same text, 9/9 came from cache with **0 model calls** (optimization log O1).
- **Problems met:** `AccessWithoutImportDenied` (fixed by importing the model via the inline RID picker) · `polars(mode="previous", schema=dict)` error (read without schema) · the repo Build button skipped the incremental job (used the dataset page Build) · the VS Code workspace was stale and is not used. All logged as learnings.
- **Decided:** D041, **accepted by you**. Approach [A011](docs/05-approaches/A011-ai-label-extraction-pilot.md). Snapshot [Compass v19](docs/00-compass/history/COMPASS-v19.md).

### 2026-11-04 (late night, 2) — Step 6: first Ontology path + Action save (Compass v18)
- **Built:** [ontology_objects.py](foundry/pipelines/ontology/ontology_objects.py) (in repo `pipelines_clean`), giving 9 curated datasets in `Data/curated`: 4 object tables, 4 join tables and 1 empty Action-owned table. Keys: 0 null, 0 duplicate.
- **Ontology (built by hand in Ontology Manager; record in [foundry/ontology](foundry/ontology/README.md)):** object types MSSM Drug 13 · Product 141 · Label 263 · Recall 25 · Triage Decision. Link types: Drug↔Product, Product↔Label, Product→Reference Label (foreign key), Recall↔Product, Recall↔Drug. Action "Create MSSM Triage Decision" (create only; ID, reviewer and time set by the system; 4 allowed decisions).
- **Gate (Object Explorer):** "Oxycodone" is the first hit by title · Oxycodone → 141 products, 25 recalls (no multiplied records) · OxyContin NDA022272 → Reference Label → v44 PLR (T13) ✅.
- **Action save proven:** submitted 1 test decision (recall D-0338-2026, "monitoring", rationale marked as a test). Forced a rebuild of the backing dataset and reloaded: the decision is still there ✅. Closes the blocker open since step 1.
- **Learned:** the Ontology Manager form preview is a test run only; apply from Object Explorer → Actions. New object and link types need ~30–60 s of indexing. An unchanged dataset needs Force build.
- **Decided:** D040 (Ontology path v1), **accepted by you**. Approach [A010](docs/05-approaches/A010-first-ontology-path.md). Snapshot [Compass v17](docs/00-compass/history/COMPASS-v17.md).
- **Small follow-ups:** move the Reference Label link type from `Data/curated` to `Ontology/Links`; add object type descriptions; idempotency token on the Action (step 8).

### 2026-11-04 (late night) — Step 5: clean baseline (Compass v17)
- **Built** in `Pipelines/pipelines_clean` (polars lightweight), three new mirrors: [clean_faers.py](foundry/pipelines/clean/clean_faers.py), [clean_labels.py](foundry/pipelines/clean/clean_labels.py), [clean_recalls.py](foundry/pipelines/clean/clean_recalls.py).
- **FAERS (Foundry = local = Oct 20 prototype):** `clean_faers_cases_current` 792,346 cases (D022: upsert by caseid, max caseversion, then each quarter's deletes) · `clean_faers_case_reactions` 2,554,017 case × reaction rows (background for PRR in step 8; **new dataset, contract addition**) · `clean_faers_drug_reaction` 75,006 oxycodone rows. Oxycodone suspect cases 4,464 → **3,408 after the D023 fold** (1,530 cases suppressed in 7 clusters across all drugs). Roles: SS 2,459 · PS 1,511 · PS+SS 451 · I 43 (D021). Built with Foundry's default memory; ~12 s and 2.9 GB peak locally.
- **Labels:** `clean_label_versions` 263 (all have XML and an effective date; 109 modern PLR format) · `clean_label_sections` 1,160 safety sections (Boxed Warning, Contraindications, Warnings and Precautions, Warnings, Precautions, Adverse Reactions; the D037 list), sub-sections folded into the parent text, 0 empty. OxyContin v44 has its 4 PLR sections.
- **Recalls:** `clean_recalls_current` 25 (4 Ongoing, 21 Terminated) · `clean_recall_product_match` 58 rows: every recall gets an ingredient row; 11 package matches with high confidence; **all 4 active recalls match a listed package**; 20 NDCs no longer in the NDC directory kept with a reason (G4).
- **Checks in Foundry SQL:** 0 duplicate keys in all 7 datasets; all counts equal the local run.
- **Problem met again:** the VS Code auto-sync rejected one commit; "Update" kept the file this time (it had been auto-committed). Committed each file right after pasting.
- **Tools:** local harness reads files datasets (`filesystem().ls()/open()`); `out/raw_faers_quarter_files` is a link to `prototypes/data/_faers_bulk`. Snapshot [Compass v16](docs/00-compass/history/COMPASS-v16.md).

### 2026-11-04 (night) — Step 4: shared drug identity (Compass v16)
- **Built:** new Foundry repo `Pipelines/pipelines_clean` (polars lightweight transforms; no external sources). Mirrors: [clean_drug_identity.py](foundry/pipelines/clean/clean_drug_identity.py), [clean_label_product_map.py](foundry/pipelines/clean/clean_label_product_map.py), [README](foundry/pipelines/clean/README.md).
- **Results (Foundry = local):** `clean_drug_ingredients` 13 (D018; oxycodone `in_slice`) · `clean_drug_identity` 8 strings: OXYCODONE → 7804 `exact_in`, OXYCODONE HYDROCHLORIDE / TEREPHTHALATE → 7804 `exact_pin`, 5 combination partners (acetaminophen, aspirin, ibuprofen, naloxone, naltrexone) kept as `no_formulary_match` · `clean_drug_product_map` 141 applications (127 ANDA, 14 NDA; 83 combination; 51 marketed) · `clean_drug_package_map` 937 packages (895 by application, 42 bulk/unapproved by `labeler:` key; all 11-digit normalised) · `clean_label_product_map` 269 rows (265 matched, 3 application not in the Drugs@FDA pull, 1 label with no approval id; 35 owner labels = 15 exact + 20 first-word name matches).
- **Checks in Foundry SQL:** 0 duplicate keys in all 5 datasets; OxyContin chain 7804 → NDA022272 (KNOA PHARMA) → 59011-410-10 (`59011041010`) → label `bfdfe235…` v44 reference = **1 row** (reference trace T13).
- **Found:** only 71 of 141 oxycodone applications have any DailyMed label (most others discontinued ANDAs); 34 have the owner's (reference) label. Products with no owner label are flagged `product_has_owner_label = false`, not guessed (G4).
- **Problem met:** the VS Code workspace (opened automatically when the repo was created) kept auto-committing "Sync remote branch". One commit was rejected, and "Update then build" then dropped an uncommitted file; re-added and committed. Lesson logged.
- **Tools:** local harness now warns about all-null columns; new [check_identity.py](foundry/tools/local_run/check_identity.py). Snapshot [Compass v15](docs/00-compass/history/COMPASS-v15.md).

### 2026-11-04 (evening) — Repo made cloud-ready
- **Why:** you'll continue from a cloud session linked to GitHub, which has no access to Foundry, this laptop, or chat memory.
- **Updated:** [README](README.md) (status, requirements, 12-step plan with progress, Foundry map) · [foundry/README](foundry/README.md) (every source/repo/dataset with RID and counts, how a change reaches Foundry, gotchas) · new [pipelines/raw/README](foundry/pipelines/raw/README.md) · new local test harness [foundry/tools/local_run](foundry/tools/local_run/README.md) (reproduces the Foundry counts 2/271/25/141/313) · new [cloud session guide](docs/10-delivery/cloud-session-guide.md) with the step 4 prompt.
- **Cloud on hold (your call):** cloud sessions can't drive the browser/Foundry, which was the main reason for using them. Work continues locally with Claude in Chrome. The guide stays for later; git option (guide §2) not chosen. Pharmacist review packet discussed, not built (plan: after step 7, ~45–60 min ask).

### 2026-11-04 (later) — Contracts accepted, first real raw pull (Compass v14)
- **Step 2:** [dataset contracts v1](docs/04-architecture/dataset-contracts-v1.md) written and accepted with all gate defaults (D039; D020–D024 now Accepted).
- **Step 3, pull 1:** `Data/raw/raw_openfda_enforcement` built from [raw_openfda_enforcement.py](foundry/pipelines/raw/raw_openfda_enforcement.py): 25 oxycodone recalls, 15 columns, `result_total` 25, source updated 2026-10-28. Matches the 25 in the [volume profile](docs/07-data-quality/source-profiles/06-data-volume-13-ingredients.md).
- **Bug caught:** the first build gave 11 rows. Without parentheses, openFDA silently dropped the first OR term. Fixed and rebuilt (learning logged).
- **Step 3, pull 2:** [raw_openfda_products.py](foundry/pipelines/raw/raw_openfda_products.py) builds `raw_openfda_drugsfda` (141 applications) and `raw_openfda_ndc` (313 products), both equal to openFDA totals. OxyContin NDA022272 (sponsor KNOA PHARMA) present, with 8 linked NDC products. Drugs@FDA needed `products.active_ingredients.name`: `openfda.generic_name` alone finds 47 of 141.
- **Step 3, pull 3:** new source `src_dailymed_api` (dailymed.nlm.nih.gov, egress approved by you, code import on, exports off). [raw_dailymed_spl.py](foundry/pipelines/raw/raw_dailymed_spl.py) writes `raw_dailymed_spl_index` (263 oxycodone labels = DailyMed total) and `raw_dailymed_spl_xml` (263 XML, 14.2 MB, 0 errors, 0 version mismatches). OxyContin `bfdfe235…` v44, effective 20260624, matches reference trace T13.
- **Step 3, pull 4:** new source `src_rxnav_api` (rxnav.nlm.nih.gov, egress approved by you, code import on, exports off). [raw_rxnorm.py](foundry/pipelines/raw/raw_rxnorm.py) writes `raw_rxnorm_lookup` (oxycodone → 7804; oxycodone hydrochloride → 82063, the salt, showing why D020 strips salts) and `raw_rxnorm_related` (271 concepts: BN 10, SCD 56, SBD 37, MIN 5 …), RxNorm 02-Nov-2026. Tested locally with stand-ins for the Foundry library before building. Contracts updated with the as-built search methods and the new `raw_rxnorm_related`.
- **Step 3, pull 5:** new source `src_faers_files` (fis.fda.gov, egress approved by you, code import on, exports off). [raw_faers_quarters.py](foundry/pipelines/raw/raw_faers_quarters.py) stores every file of the 2026 Q1 and Q2 ZIPs unchanged in `raw_faers_quarter_files` (files dataset), plus `raw_faers_quarter_manifest`: Q1 19 files / 352,984,542 bytes, Q2 18 files / 337,724,653 bytes, 0 errors. ZIP sizes and the DRUG26Q1 sha256 equal the copies downloaded on 2026-10-20. Tested locally on those ZIPs first. **Step 3 complete; snapshot [Compass v14](docs/00-compass/history/COMPASS-v14.md) → v15.**
- **Also:** you added secret `OpenFdaApiKey` (not yet used in code). Secret names must be alphanumeric, so the key secret is `OpenFdaApiKey`. Code is now pasted into the Foundry editor (auto-indent mangled typed code).

### 2026-11-04 — Foundry access proven, first dataset built (Compass v13)
- **How:** you logged in to Foundry in Chrome; Claude worked through Claude in Chrome. You did the security clicks yourself (egress approval, code-import toggle).
- **Built in Foundry:** 9 top-level folders + subfolders (`Data/raw|clean|curated|quarantine`, `Ontology/Objects|Links|Actions`, `AIP/Logic|Evals`) · `AIP/Logic/scratch_aip_access_test` · source `Data/raw/src_openfda_api` · Code Repository `Pipelines/pipelines_raw_ingest` · dataset `Data/raw/raw_openfda_enforcement_access_test` (1 row, HTTP 200, recall D-0338-2026, oxycodone 5 mg, Class II, Ongoing).
- **Proven:** AIP model replies (GPT-5.6 Sol, "AIP OK" in 2.9 s); openFDA reachable from a Foundry build. **Not proven:** Action save.
- **Decided:** D031 v4 (no fixed demo date; cut list v3 stays default scope) · D038 (openFDA via REST API source + external transform). Approach [A009](docs/05-approaches/A009-openfda-rest-ingestion.md). 4 learnings. Record: [access results](docs/10-delivery/2026-11-04-foundry-access-results.md). Code mirror: [raw_openfda_enforcement_access_test.py](foundry/pipelines/raw/raw_openfda_enforcement_access_test.py). Snapshot: [Compass v12](docs/00-compass/history/COMPASS-v12.md).
- **Not done:** openFDA key secret; `request_url` loses the query string (store params in their own column next time); BACKLOG hours not re-estimated; Delivery Lead not run.

### 2026-11-02 — Reference set v2: 30 cross-source drug traces (Compass v12)
- **Why:** the v1 30-case pack wasn't defensible. Codex wrote the questions and its own answers in one pass, the FAERS oxycodone capture failed, and one SrLC file was really Ozempic.
- **Built:** [proposals/2026-11-02-gold-set-v2/](proposals/2026-11-02-gold-set-v2/). 62 drugs screened → 35 eligible → 30 traced through RxNorm, NDC, Drugs@FDA, DailyMed, SrLC, FAERS, enforcement and ClinicalTrials.gov (240 answers). Questions frozen before answers; identity guard on every capture; independent verifier (3,403/3,403 checks pass); live re-check (530/530 identical, 30/30 answers unchanged); 30 [case cards](proposals/2026-11-02-gold-set-v2/cards/); diagram [20-gold-trace-v1](docs/diagrams/png/20-gold-trace-v1.png).
- **Found:** the v1 403 was openFDA requiring a key for count queries with `limit>100`. The key now lives in your shell profile and is redacted in saved URLs. Other findings: FAERS substance queries mix products (Chantix vs Tyrvaya); the recall `openfda.package_ndc` list is application-wide; Lyrica's DailyMed label (effective 2020) lags a 2025 SrLC change.
- **Decided (proposed):** D037 plus the dataset's "label mentions" rule; 4 learnings. Approach [A008](docs/05-approaches/A008-gold-set-v2-cross-source-traces.md). v1 superseded. Snapshot: [Compass v11](docs/00-compass/history/COMPASS-v11.md).
- **Not done:** pharmacist review of S4 calls and S6 synonyms; BACKLOG hours not updated; Delivery Lead not run.

### 2026-10-31 — Foundry conventions and project learning/build roadmap (Compass v11)
- **Research:** inspected Data Forge's 11-video introductory playlist; read auto-generated transcripts for episodes 3 (folders), 6 (medallion pipeline), and 9 (Ontology Manager); cross-checked official Palantir docs. Other video content is not claimed reviewed.
- **Created:** [reference entry point](docs/04-architecture/foundry-conventions/README.md), [conventions](docs/04-architecture/foundry-conventions/conventions-v1.md), [12-step build order](docs/04-architecture/foundry-conventions/project-build-order-v1.md), [source/timestamp notes](docs/04-architecture/foundry-conventions/tutorial-research-2026-10-31.md), [A007](docs/05-approaches/A007-foundry-medallion-conventions.md), medallion and ontology diagrams (Mermaid, PNG/PDF, editable draw.io).
- **Decided:** D036 — keep the existing local raw/clean/ontology layout; explain bronze/silver/gold responsibilities; use explicit naming and grain/key contracts and a dependency roadmap. This is a documentation standard, not approval of proposed clinical/source/scope decisions.
- **Status:** no Foundry build performed; no speed/cost result claimed. Oct 27 capacity estimate marked historical. Parked A006 / D032–D035 are not adopted. Snapshot: [Compass v10](docs/00-compass/history/COMPASS-v10.md).

### 2026-10-27 — Restart after a lost week (Compass v10)
- **Status:** no work Oct 21–26. Exploration was finished early, so the thinking is intact; the Foundry build has not started.
- **Decided (proposed):** D031 v3. Demo Wed Nov 4 (Nov 3 = Election Day); build Oct 29–Nov 2; all 6 cuts applied now; decision review 5→1 h; load ~76%.
- **Files:** [game plan v1](docs/10-delivery/game-plan-v1-oct27-to-nov4.md) · [BACKLOG](docs/10-delivery/BACKLOG.md) re-dated · [COMPASS v9 snapshot](docs/00-compass/history/COMPASS-v09.md).

### 2026-10-20 (night) — Plan to the demo, tracker live (Compass v8)
- **Answered:** source choices, merge design, "FAERS is the spine?", what "since yesterday" means, daily FAERS. Plan: `~/.claude/plans/i-need-help-in-valiant-quasar.md` (approved).
- **Decided:** +Drugs@FDA, NDC Directory, SrLC as bridges; OnSIDES = Part B benchmark (D026). Two-level identity (D027, supersedes D003). "Since last review" + ChangeEvent + per-source as-of (D028). FAERS quarterly in pilot; daily only via an official API (D029). Demo ~Nov 3, freezes Oct 23/24, cut list (D031).
- **Tracking:** ⏱️ [Delivery Lead](.claude/agents/delivery-lead.md) agent · [BACKLOG](docs/10-delivery/BACKLOG.md) (load 55 h / ~50 h = 110% Amber) · decisions versioned with "Decision changes" + "Learnings" tables (D030) · COMPASS versioned, [history](docs/00-compass/history/) · CLAUDE.md §2c.
- **New approach:** [A005](docs/05-approaches/A005-source-selection-and-merge.md). 4 atlas sessions proposed (cards in the app).

### 2026-10-20 (evening) — Real bulk FAERS walked through every stage
- Downloaded FAERS bulk 2026 Q1+Q2 (63 MB each, git-ignored in `prototypes/data/_faers_bulk/`). Prototype of the whole FAERS pipeline: [faers_bulk_walkthrough.py](prototypes/explore/faers_bulk_walkthrough.py) (36 s, plain Python).
- **Walkthrough page:** [data-walkthrough-v1.html](docs/04-architecture/data-walkthrough-v1.html) (also published as a private artifact). Supersedes the v1 explainer.
- **Found:** bulk has no openfda (link via `nda_num`); substring matching +50% false morphine rows; append vs upsert +8.7%; one Canadian patient filed 700× (oxycodone −24% after fold); reporter field blank 35% → 72% at the AEMS switch; NAION PRR 112, not on tablet or injection label. DQ34–DQ41, D020–D025 proposed.

### 2026-10-20 (later) — FAERS and Part B explained with one real drug
- **Explainer:** [faers-and-part-b-explained-v1.md](docs/04-architecture/faers-and-part-b-explained-v1.md): the project as two lists (FAERS counts vs LLM label list), one real report walked row by row, keep/drop table for FAERS fields, ontology objects with examples.
- **Diagram:** [16-faers-to-signal-v1.png](docs/diagrams/png/16-faers-to-signal-v1.png). **Approach:** [A004](docs/05-approaches/A004-faers-to-ontology-mapping.md). **New issue:** DQ33 (semaglutide FAERS linked to the tablets label, not the injection label).
- Found 3 label traps that break plain text search ("blurred vision", "gastroparesis", spelling).

### 2026-10-20 — Class locked, sources profiled, merges shown
- **Class accepted:** 8 opioids + 5 GLP-1 ([A003](docs/05-approaches/A003-class-choice-hybrid.md), D014). Focus rule: rank clinical side effects + recalls; tag lawyer/abuse/product-error/pregnancy (D016).
- **Structure reports** for every source: [01 FAERS](docs/07-data-quality/source-profiles/01-faers.md) · [02 DailyMed](docs/07-data-quality/source-profiles/02-dailymed.md) · [03 Recalls](docs/07-data-quality/source-profiles/03-enforcement.md) · [04 RxNorm](docs/07-data-quality/source-profiles/04-rxnorm.md) · [05 Trials](docs/07-data-quality/source-profiles/05-clinicaltrials.md).
- **Volumes** for 13 drugs: [06-data-volume](docs/07-data-quality/source-profiles/06-data-volume-13-ingredients.md) (1.46M FAERS reports, 116 ongoing recalls, 1,324 labels).
- **Worked merges:** [merge-walkthrough-v1](docs/04-architecture/merge-walkthrough-v1.md) (fentanyl recall; semaglutide NAION signal).
- **Diagrams moved out of .md into PNG + PDF** (D017): [docs/diagrams](docs/diagrams/diagram-book.pdf), render with `bash tools/render_diagrams.sh`.
- New scripts: [pull_all.py](prototypes/explore/pull_all.py), [volume_check.py](prototypes/explore/volume_check.py), [describe_structure.py](prototypes/explore/describe_structure.py). New data issues DQ23–DQ32. Decisions D016–D019.

### 2026-10-19 — Sources mapped, research done
- **Source access guide** (browse / API / bulk for every source, all links tested live): [00-source-access-guide.md](docs/07-data-quality/source-profiles/00-source-access-guide.md). Sampler script [pull_samples.py](prototypes/explore/pull_samples.py) ran OK for oxycodone. Profile files 01–05 created with checklists.
- **3 parallel research agents** → [research synthesis](docs/01-discovery/research/README.md): [R1 class](docs/01-discovery/research/R1-therapeutic-class.md) · [R2 industry need](docs/01-discovery/research/R2-industry-need.md) · [R3 prior art](docs/01-discovery/research/R3-prior-art.md). 140 sources retained.
- **Proposed:** opioid-led hybrid class ([A003](docs/05-approaches/A003-class-choice-hybrid.md), D014); AI target F1 ≥ 0.85 (D015).
- **Found:** FDA replaced FAERS with AEMS (Mar 2026) (DQ20); ~58% of 2021 oxycodone reports from lawyers (DQ21); "hyperalgesia" has 0 FAERS reports (DQ22). New approach A002 (source profiling).
- You set up the Palantir Developer Tier and are learning the tools.

### 2026-10-14 — Git ground rule set
- **Rule:** Claude never commits or pushes. It gives commit messages and commands; you run them ([CLAUDE.md §0](CLAUDE.md)). Enforced by deny rules in [.claude/settings.json](.claude/settings.json) (tested: blocked).
- **GitHub account: vrbabu9000 only.** Use SSH alias `github.com-personal`. Repo-local identity `vrbabu9000 <vrb.canada@gmail.com>`. Your global git identity is vrajesh9000, so the local override is required.
- Decision D013 logged.

### 2026-10-13 — Boss meeting done, scope reset
- **Meeting outcomes** logged in [the meeting file](docs/03-meetings/2026-10-13-boss-kickoff-questions.md#-meeting-summary--held-2026-10-13).
- **Purpose clarified:** exploratory showcase of thinking, design and usefulness → the reasoning trail is half the deliverable.
- **Class changed:** GLP-1 → opioids ([A001](docs/05-approaches/A001-pilot-scope.md), D002 superseded by D007).
- **Monitoring promoted** to must-have; drift judged over 3–4 weeks (D008, D009).
- **Foundry:** use the free Developer Tier (D010).
- **New files:** [A001 pilot scope](docs/05-approaches/A001-pilot-scope.md) · [source profiling plan](docs/07-data-quality/source-profiles/README.md) · [ideas parking lot](docs/09-roadmap/ideas-parking-lot.md) (health "OS" idea).

### 2026-10-13 — Pre-meeting prep
- Added [therapeutic class options](docs/01-discovery/therapeutic-class-options.md) and the "own Developer Tier?" question (M3a).

### 2026-10-13 — Project created
- Repo set up: [COMPASS](COMPASS.md), [CLAUDE.md](CLAUDE.md) response rules, 8 personas, brief summary, requirements deep-dive, design-thinking canvas, architecture v0 (+ draw.io), data-issues register, approach/decision/optimization templates, pilot→production roadmap, [boss questions](docs/03-meetings/2026-10-13-boss-kickoff-questions.md).
