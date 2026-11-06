# Phase D fix brief: one wording for every hand-in piece

Read with `AGENT-BRIEF.md`, `phase-d-todo.md`, `fact-check.md` and `first-time-reader.md` in this folder.
Every report, the deck, the speaking script, the demo guide and the architecture note must use **these exact meanings**.

**Updated 2026-11-06** for the owner's batch decision: the 12 proposed decisions and D041 v2 are accepted; the AI reads 5 labels (745/745 grounded); NAION's labels are also read by the AI; Workshop v0.10.0; the duplicate link type is deleted. Rows changed on 6 Nov are marked *(6 Nov)*.

## Fixed by the lead already (do not redo)
- `tools/handin/style.py` legend: **DESIGNED** = a design choice we made and wrote down (may be built; the status band says how far). **ASSUMED** = not verified, taken as true for now. Re-tag text so it matches: built-and-checked things get TESTED; not built yet = PLANNED; a choice = DESIGNED; a guess = ASSUMED.
- `tools/handin/build_report.py` numbers appendix now says "Every number in the table below…; figures quoted from other records name that record where they appear". So every non-numbers.json figure must cite its record inline (e.g. "(DQ36)", "(O2)", "(learning 2026-11-04)").
- *(6 Nov)* Current diagrams: **30 v3, 31 v2, 32 v3, 33 v3, 35 v2, 36 v3, 37 v3, 38 v2** (`docs/diagrams/README-handin.md`). Point every figure at these. (On 5 Nov this line said 30 v2 and 33 v2; both are kept on disk as history.)
- Architecture note fixed (decision 3 wording, label-check order) and rebuilt. *(6 Nov)* D027 and D037 are now accepted; the note is v1.1 with diagram 38 v2.

## One definition each (copy the wording)
| Term | Meaning (source) |
|---|---|
| **Signal** ({{n:signals.total}} = 1,952) | A drug–reaction pair that meets the Evans rule (at least 3 reports, PRR ≥ 2, χ² ≥ 4; D006) **and** whose reaction term is not found in any reference label of that drug (1,844 "not in label") or is found only through a medium-band synonym (108 "possibly in label"). `ontology_signals.py` l.194–195 |
| **Ranked** ({{n:signals.ranked}} = 1,073) | The review queue: signals that are "not in label", in the **clinical** bucket (D016 v3), and less than half carried by mass-polypharmacy reports (D023 v2). `ontology_signals.py` l.199–200. A review queue, not 1,073 findings |
| **Ranked history** | 1,355 at step 9 (first full build) → 1,210 (syn_v1) → 1,115 (D016 v3) → 1,073 (syn_v2). Always say "1,355 at step 9" when quoting the start |
| **Active recall** ({{n:recalls.active}} = 126) | openFDA enforcement status = **Ongoing** (`clean_recalls.py` l.69). Not "not terminated" (that would add Completed) |
| **Label check order** | (1) AI term with a code-found quote → (2) exact text in a safety section → (3) reviewed synonym. Outcome is the same in any order; only `label_match_method` differs (`ontology_signals.py` l.163–176). *(6 Nov)* First-match counts over 14,921 stats (Foundry, {{n:signals.label_check_stats.*}}): AI 188 (131 oxycodone, 57 semaglutide), text 1,252, synonym high 163, medium 210, none 13,108 |
| **F1 0.97** | On a 35-item answer key: Boxed Warning + Contraindications of **2 oxycodone labels**, written by Claude, frozen before the run, no pharmacist yet. *(6 Nov)* Grounding **745/745** covers all 21 extracted sections of 5 labels (448/448 over 9 sections was the v1 pilot; use it only as history). The 12 semaglutide sections are **not scored** (no answer key). Never print F1 next to 745/745 without this scope |
| **"Recall 35/35"** | Write "found 35 of 35 answer-key items" (statistical recall) so it is never confused with FDA recalls |
| **AI on the hero signal** | *(6 Nov, D041 v2)* The AI reads the **3** semaglutide labels (Ozempic v20, Wegovy v19, oral Ozempic/Rybelsus v14). It found diabetic-retinopathy terms and **no** optic-nerve or NAION term: an independent check that agrees with "not in label" (text + synonyms + AI). The AI still does not change the signal list; its value is the quoted evidence on screen. NAION's evaluation id is now `c4b5da0b64d1e1e6` |
| **Labels searched (NAION)** | Page 1 panel "Reference labels searched": Ozempic v20, Wegovy v19, oral Ozempic v14 ({{n:app.labels_searched_naion}}), with DailyMed links. Path: Signal → Drug → Products → Reference Label. No dedicated link type yet. *(6 Nov)* Below it, the table **What the AI read in these labels (every line is quoted word for word from the label)**: reaction · section · quote · label key ({{n:app.ai_quotes_panel_rows_naion}} = 297 rows for semaglutide); *Labels also read by AI* = {{n:app.labels_read_by_ai_naion}} = 3 |
| **Timing** | Machine timing ({{n:app.timing_s.*}}): brief 11.5 s, switches 0.8–2.4 s (browser script, View mode), **timed on v0.9.0**; v0.10.0 adds one table below the fold on page 1, not re-timed. A human two-minute walk-through has **not** been run |
| **Workshop** | {{n:app.workshop_version}} = v0.10.0 *(6 Nov)*, 4 pages |
| **Morning brief "changes" card** | Counts change events in the **last 30 days** (26), not "since yesterday". Page 3 date range is how the officer narrows to "since my last review" |
| **Accepted decisions** *(6 Nov)* | The owner accepted all 12 formerly proposed decisions in one batch on 2026-11-06: D006, D015 (the F1 ≥ 0.85 target only; its TAC 2017 / OnSIDES benchmark stays cut by D031), D025, D026, D027, D028, D029, D037, D045, D046, D047, D048; plus D041 v2. Never write "proposed" next to them. D001–D048 is the full log (D031 v3 superseded; D043 syn_v3 is still proposed and not in the hand-in numbers) |
| **D048** | No partitioning in the pilot (accepted 6 Nov); revisit at 8+ FAERS quarters or a build over 5 minutes |
| **O3** | XML **downloads** 1,321 → 2 per build (the ~30 index pages are still pulled); build 3 m 23 s → 1 m 23 s |
| **O2** | Incremental FAERS equals the full rebuild row for row but is **slower**: 88 s vs 32 s. Three state datasets + one quarter log |
| **DQ06** | Indication terms are **not handled** (left as a known gap): liraglutide's rank-1 signal is "Diabetic metabolic decompensation" |
| **DQ38** | Reporter type blank 34% (Q1) → 72% (Q2) from Foundry at the gate; the Oct 20 profile said 35% |
| **Who can triage** | Only the project owner can submit a Triage Decision today (Action permission). The officer role is a production step |
| **Ontology links** *(6 Nov)* | {{n:ontology.link_types_mssm}} = 10 MSSM link types. The duplicate Signal → Drug link type was deleted on 6 Nov after checking nothing used it; mention it only as a one-line history note |
| **Evaluator holes** *(6 Nov)* | Hole #1 (AI and screen barely meet) is addressed by D041 v2. Hole #2 (self-scored key, no pharmacist) stays open; the pharmacist reviewer stays a documented gap. "Another month": score long sections with a pharmacist; widen the AI to other drugs (no longer "widen to semaglutide") |
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
