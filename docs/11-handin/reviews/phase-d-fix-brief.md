# Phase D fix brief: one wording for every hand-in piece

Read with `AGENT-BRIEF.md`, `phase-d-todo.md`, `fact-check.md` and `first-time-reader.md` in this folder.
Every report, the deck, the speaking script, the demo guide and the architecture note must use **these exact meanings**.

## Fixed by the lead already (do not redo)
- `tools/handin/style.py` legend: **DESIGNED** = a design choice we made and wrote down (may be built; the status band says how far). **ASSUMED** = not verified, taken as true for now. Re-tag text so it matches: built-and-checked things get TESTED; not built yet = PLANNED; a choice = DESIGNED; a guess = ASSUMED.
- `tools/handin/build_report.py` numbers appendix now says "Every number in the table below…; figures quoted from other records name that record where they appear". So every non-numbers.json figure must cite its record inline (e.g. "(DQ36)", "(O2)", "(learning 2026-11-04)").
- Diagram **30 v2** (O3 measured) exists: `docs/diagrams/png/30-handin-data-flow-v2.png` (+ pdf, drawio). Point every figure at v2. Diagram **33 v2** also exists; never use 33 v1.
- Architecture note fixed (decision 3 wording, label-check order, D027/D037 marked proposed) and rebuilt.

## One definition each (copy the wording)
| Term | Meaning (source) |
|---|---|
| **Signal** ({{n:signals.total}} = 1,952) | A drug–reaction pair that meets the Evans rule (at least 3 reports, PRR ≥ 2, χ² ≥ 4; D006) **and** whose reaction term is not found in any reference label of that drug (1,844 "not in label") or is found only through a medium-band synonym (108 "possibly in label"). `ontology_signals.py` l.194–195 |
| **Ranked** ({{n:signals.ranked}} = 1,073) | The review queue: signals that are "not in label", in the **clinical** bucket (D016 v3), and less than half carried by mass-polypharmacy reports (D023 v2). `ontology_signals.py` l.199–200. A review queue, not 1,073 findings |
| **Ranked history** | 1,355 at step 9 (first full build) → 1,210 (syn_v1) → 1,115 (D016 v3) → 1,073 (syn_v2). Always say "1,355 at step 9" when quoting the start |
| **Active recall** ({{n:recalls.active}} = 126) | openFDA enforcement status = **Ongoing** (`clean_recalls.py` l.69). Not "not terminated" (that would add Completed) |
| **Label check order** | (1) AI term with a code-found quote → (2) exact text in a safety section → (3) reviewed synonym. Outcome is the same in any order; only `label_match_method` differs (`ontology_signals.py` l.163–176) |
| **F1 0.97** | On a 35-item answer key: Boxed Warning + Contraindications of **2 oxycodone labels**, written by Claude, frozen before the run, no pharmacist yet. Grounding 448/448 covers all 9 extracted sections. Never print F1 next to 448/448 without this scope |
| **"Recall 35/35"** | Write "found 35 of 35 answer-key items" (statistical recall) so it is never confused with FDA recalls |
| **AI on the hero signal** | The AI read **0** semaglutide labels (pilot = 2 oxycodone labels). NAION is "not in label" from the exact-text and synonym checks only |
| **Labels searched (NAION)** | Page 1 panel "Reference labels searched": Ozempic v20, Wegovy v19, oral Ozempic v14 ({{n:app.labels_searched_naion}}), with DailyMed links. Path: Signal → Drug → Products → Reference Label. No dedicated link type yet |
| **Timing** | Machine timing ({{n:app.timing_s.*}}): brief 11.5 s, switches 0.8–2.4 s (browser script, View mode). A human two-minute walk-through has **not** been run |
| **Workshop** | {{n:app.workshop_version}} = v0.9.0, 4 pages |
| **Morning brief "changes" card** | Counts change events in the **last 30 days** (26), not "since yesterday". Page 3 date range is how the officer narrows to "since my last review" |
| **Proposed decisions** | 12 status cells still say **Proposed**: D006, D015, D025, D026, D027, D028, D029, D037, D045, D046, D047, D048 (D031 v3 is superseded). Many are built and running; the owner accepts them in one batch. D001–D048 is the full log. Where a report names "the proposed ones", list all 12 or say "12 proposed, see DECISIONS" |
| **D048** | No partitioning in the pilot (proposed); revisit at 8+ FAERS quarters or a build over 5 minutes |
| **O3** | XML **downloads** 1,321 → 2 per build (the ~30 index pages are still pulled); build 3 m 23 s → 1 m 23 s |
| **O2** | Incremental FAERS equals the full rebuild row for row but is **slower**: 88 s vs 32 s. Three state datasets + one quarter log |
| **DQ06** | Indication terms are **not handled** (left as a known gap): liraglutide's rank-1 signal is "Diabetic metabolic decompensation" |
| **DQ38** | Reporter type blank 34% (Q1) → 72% (Q2) from Foundry at the gate; the Oct 20 profile said 35% |
| **Who can triage** | Only the project owner can submit a Triage Decision today (Action permission). The officer role is a production step |
| **FAERS freshness** | Signals change only when a new FAERS quarter arrives; FAERS is ~130 days behind (monitoring `faers_age_days`). FAERS moved to AEMS in March 2026; the future feed is unverified |

## The 13 formulary drugs (name them once in every report's glossary or first chapter)
Opioids (8): oxycodone, hydrocodone, morphine, fentanyl, hydromorphone, methadone, buprenorphine, tramadol.
GLP-1s (5): semaglutide, liraglutide, dulaglutide, tirzepatide, exenatide (exenatide has no reference label → signals for 12 of 13).
*(Verified: `foundry/pipelines/raw/raw_rxnorm*.py` INGREDIENTS, D018 / D039 G1.)*

## Rules for fixers
- Edit only the files you were assigned. No git. No edits to foundry/, COMPASS, DECISIONS, ACTIVITY-LOG, numbers.json, style.py, build_report.py.
- Rebuild each report (`.venv/bin/python tools/handin/build_report.py <name>`), render pages (`pdftoppm -r 60`), and look at every page you changed.
- Keep honesty rules. Do not invent numbers; "not measured" when missing.
- Add a short "What this means for Dana (the safety officer)" callout to each report's first chapter.
- End with a list of what you changed per fact-check / first-time-reader item ID.
