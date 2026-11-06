# Shared brief for every hand-in agent (Phase C/D)

Read this first. It keeps the reports, the deck, the demo and the diagrams one story.

## The reader and the judge
- **Reader:** a capable engineer who has never seen Palantir Foundry, drug safety (pharmacovigilance) or this project. Explain every term the first time: Foundry, dataset, transform, Code Repository, Data Lineage, Ontology, object type, link type, Action, Workshop, AIP, FAERS, PRR, Evans rule, MedDRA preferred term (PT), DailyMed / SPL, openFDA, RxNorm / RxCUI, NDC.
- **End user:** the hospital pharmacy safety officer and her three morning questions: (1) unlabeled adverse events, (2) active recalls, (3) what changed since yesterday; trust rule: every flag traces to its source.
- **Judges** ("What we will look at", brief §5): Architecture · Optimization · Data judgment · The application · AI reliability · Communication. Brief §4 hand-ins: working build; one-page architecture note; optimization log; 20-minute demo + questions. Brief summary: `docs/00-brief/brief-summary.md`. Original: `docs/00-brief/Soragence-Technical-Build-Brief.pdf`.
- Key quote from the brief: a partial build with clear reasoning beats a complete one you cannot explain.

## Sources of truth (never invent)
- Numbers: **`docs/11-handin/numbers.json`** only (captured from Foundry at the baseline gate, `baseline-gate.md`). In ReportLab reports use `{{n:key.path}}`. If a number you need is missing, say "not measured" — do not compute or guess one.
- What was built: `foundry/README.md`, `foundry/pipelines/*/README.md`, `foundry/ontology/README.md`, `foundry/monitoring/README.md`.
- Why: `docs/06-decisions/DECISIONS.md` (decisions D001–D047, decision changes, learnings), `docs/05-approaches/A000–A017` (what we tried, kept, dropped), `docs/07-data-quality/data-issues-register.md` (DQ01–DQ42), `docs/08-optimization-log/optimization-log.md` (O1–O3a), `eval/ai-eval-v1.md`, `docs/09-roadmap/` (pilot-to-production, ideas, another-month research), `COMPASS.md`, `ACTIVITY-LOG.md`.
- Pictures: diagrams `docs/diagrams/png/30…38-handin-*` — use the newest version listed in `docs/diagrams/README-handin.md` (v2 for 30, 32, 33, 36, 37) (+ pdf, + drawio for 30/31/36), index `docs/diagrams/README-handin.md`; screenshots `docs/11-handin/screens/*.jpg`.
- Style: `tools/handin/README.md` (ReportLab builder `tools/handin/build_report.py`, style `tools/handin/style.py`), BlueJay reference `/Users/vigneshrbabu/Documents/Git/bluejay-night-ride-optimizer`.

## Honesty rules (they are part of the grade)
- Label evidence: OBSERVED (measured in Foundry), DERIVED (computed from observed), ASSUMED, DESIGNED (a choice).
- Say what did not work: O2 incremental FAERS was **slower** (88 s vs 32 s); O3a column pruning did not help; the AI does not change the signal list today; the answer key is Claude-written, pharmacist pending; drift is a historical replay; the duplicate Signal→Drug link type is a mistake left for the owner.
- "1,073 ranked signals" is a review queue, not 1,073 findings. A signal is disproportionate reporting + not found in the label, not proof of causation.
- Proposed decisions (D045–D047) are labelled proposed.

## The 20-minute demo (one agenda for deck, script and navigation guide)
| Time | Part | Where | Proves (rubric row) |
|---|---|---|---|
| 0:00–1:30 | The officer's problem: 3 questions, trust rule, 13 drugs (8 opioids + 5 GLP-1s), public data only | slides | Communication |
| 1:30–3:00 | **Morning brief**: three numbers + "data as of" | app page 0 | Application |
| 3:00–6:00 | **1 · Not in label**: drug filter → semaglutide → NAION #1 → evidence panel (PRR, CI, labels searched, method) → *Triage this signal* (Action, write-back) | app page 1 | Application, AI reliability (trace) |
| 6:00–7:30 | **2 · Recalls**: active filter, newest D-0040-2027 (compounded tirzepatide, matches none of our products — said honestly) ; **3 · What changed**: date range = since my last review | app pages 2–3 | Application |
| 7:30–9:30 | Architecture in one picture: sources → raw → clean (identity resolved once) → curated → ontology → app; then Data Lineage live | diagram 30, Data Lineage | Architecture |
| 9:30–11:30 | Ontology: objects, links, the create-only Action; Object Explorer on the NAION signal | diagram 31, Ontology Manager, Object Explorer | Architecture |
| 11:30–13:30 | From one FAERS report to a ranked signal: D022 versions/deletes, D021 roles, D020 identity, D023 v2 duplicates, PRR/Evans, 3-step label check (AI term → exact text → synonyms, code order), buckets | diagram 32, code repo | Data judgment, AI reliability |
| 13:30–15:30 | AI reliability: grounded 448/448, F1 0.97 on a small Claude-written key vs target 0.85, cache = 0 model calls on rebuild; monitoring catches regressions | eval, monitoring datasets | AI reliability |
| 15:30–17:30 | Optimization log: O1 cache (helped), O2 incremental FAERS (did not, and why), O3 DailyMed XML reuse (3 m 23 s → 1 m 23 s, 1,321 → 2 downloads), O3a (did not) | diagram 33, optimization log | Optimization |
| 17:30–19:00 | Data judgment + what we chose not to do: phantom rows (DQ36), mass polypharmacy cluster (D023 v2), reporter type 34%→72% (DQ38), DailyMed "None" (DQ42); no MedDRA licence, no patient data | slides, monitoring | Data judgment |
| 19:00–20:00 | Another month: pharmacist review loop (+ sources researched), schedules, live drift, health page | slides | Communication |
Backups for Q&A: one per rubric row; ripple map (diagram 37); change feed (34); monitoring (35).

## Output places
- Reports: `docs/11-handin/reports/src/R0x-*.py` → `docs/11-handin/reports/pdf/R0x-*.pdf` (build with `.venv/bin/python tools/handin/build_report.py <name>`; check pages with `--preview`).
- Architecture note: `docs/11-handin/architecture-note/`.
- Deck: `docs/11-handin/deck/` (.pptx + PDF preview + `content_storyboard.md`, `speaking_script.md`, `slide_explanations.md`).
- Demo: `docs/11-handin/demo/` (navigation guide .md + PDF, ripple table, rehearsal timing).
- Reviews: `docs/11-handin/reviews/`.
- Never run git commands that change anything. Never edit `foundry/`, COMPASS, DECISIONS or ACTIVITY-LOG (the lead does). Never sign up or log in anywhere. Use `.venv/bin/python`.
