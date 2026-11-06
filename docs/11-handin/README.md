# Hand-in plan (approved 2026-11-05) — build → baseline gate → agents → review

> **Status 2026-11-06:** the plan below is done. The owner's batch decision happened on 6 Nov: the 12 proposed decisions (D006, D015, D025–D029, D037, D045–D048) were accepted, plus D041 v2 (the AI also reads the 3 semaglutide labels; page 1 shows its quotes, Workshop v0.10.0). The duplicate Signal → Drug link type was deleted the same day. The hand-in set (R00–R09, architecture note, deck, demo files, diagrams 30 v3 · 31 v2 · 32 v3 · 33 v3 · 35 v2 · 36 v3 · 37 v3 · 38 v2) was refreshed to match. The text below is the original plan, kept as written.

## Context
Steps 1–10 are done in Foundry (Compass v34). The brief asks for four hand-ins: the working build, a one-page architecture note, an optimization log, and a 20-minute demo. It also lists six things the reviewers will judge. Your request, organised:

| # | Your idea | Where it lands below |
|---|---|---|
| 0 | Keep going through steps 11 and 12 without stopping | Phase A |
| 4 | Workshop: how to use it, better UI | Phase A (A4) + report R4 |
| — | "Confident about the baseline" before fanning out | Phase B gate |
| 1 | Reports in the BlueJay style, a presentation, a cohesive 20-min demo, agent personas | Phase C (C1–C5) |
| 2 | Click-by-click demo path with "change here → changes there" | Phase C (C6) |
| 3 | Demo is the main target; judged against "What we will look at" | Rubric map + Phase D reviews |
| 5 | Pharmacist review + ClinicalTrials.gov, DrugBank, Orange Book, NIDA, Claude healthcare connectors → "another month" | Phase C (C7); can start now |

**What I learned from BlueJay (the style we copy):**
- **Guide:** ReportLab Python builder (`docs/technical/build_team_guide.py`). Navy `#13324B`, teal `#087F8C`, light `#EAF3F5`, ink `#263746`, Helvetica. Navy header rows. Cover with a "what this is / is not" box and a "how to read this" note. Parts: Think → Build (each chapter ends with a gate) → Reference.
- **Deck:** pptxgenjs builder. Every number comes from one `numbers.json`. Evidence pills (OBSERVED / DERIVED / ASSUMED). Status bands (TESTED / PLANNED). Ships with `speaking_script.md`, `slide_explanations.md`, `content_storyboard.md`, and a PDF preview.
- **Diagrams:** a Python generator for draw.io + SVG with a fixed palette; matplotlib for charts.
- **Reviews:** saved as .md files (professor review, first-time reader, factual accuracy, cohesion), then fixed.

**Hard limits:**
- Only I drive Chrome/Foundry, one browser, one agent at a time. Agents work on files and research only.
- No git writes. You commit everything at the end.
- No sign-ups or log-ins to new services. The research is read-only web.

---

## Phase A — Finish the build in Foundry (me, in order)
**A1 · Recalls on the screen (question 2).**
- Recall objects already link to Drug (`ontology_link_recall_drug`), and Drug already has `n_active_recalls`.
- Add a recalls panel to the Workshop module: active recalls for the chosen drugs (class, status, date, reason, product match + confidence, link to the openFDA record).

**A2 · "Changed since last review" (question 3, D028).**
- New `ontology_change_events` dataset, built incrementally: each build compares today's signals, recalls and label versions with the previous snapshot. Kinds: new / gone / changed, with old → new values and source as-of dates.
- New object type MSSM Change Event, plus a panel on the screen ("since my last decision" = after the officer's latest triage time).
- New decision **D045** (proposed at the time; accepted in the 6 Nov batch). I keep building on it and you accept it at the end.

**A3 · Source as-of dates + health checks + monitoring.**
- As-of date per source on the screen.
- Foundry Data Health checks on key datasets: row count, freshness, primary key, schema.
- A `monitoring_*` dataset: pipeline counts, AI grounded rate, cache hits, a historical drift replay (clearly labelled replay, per D009).
- Fill `foundry/monitoring/`.

**A4 · Workshop UI pass.**
- Restructure into a "Morning brief": 3 sections that answer the 3 questions, KPI metric cards on top, the drug filter shared by all three, a signal detail with its trace to source (FAERS counts → label sections searched → quote), and triage.
- Explore the widgets: metric card, chart, tabs, object view, links.
- 💊 Safety-officer test: the morning flow in under 2 minutes, timed.

**A5 · AI evaluation (honest version).**
- Re-run the gold-set scoring and record precision, recall and F1 against D015.
- Mark it "Claude-reviewed, pharmacist pending".
- Grounding failure cases shown.

**A6 · Small fixes.**
- DailyMed retry with back-off (a 429 means "too many requests"; wait and retry).
- One optimization that helps (O3). The leading candidate is filtering FAERS to formulary cases early, measured before and after.
- Re-run the signals to confirm nothing moved.

**Docs for each:** A### approach files, DECISIONS, Compass bumps, activity log, READMEs (same routine as steps 1–10).

## Phase B — Baseline gate (before fanning out)
Every check must pass, recorded in `docs/11-handin/baseline-gate.md`:

| Check | Pass when |
|---|---|
| 3 questions on screen | each answered, from one screen |
| Trace | 5 random flags traced to source rows/quotes by hand |
| Rebuild | full chain rebuilt; counts equal the saved numbers; triage decisions survive |
| Numbers | `docs/11-handin/numbers.json` captured from Foundry SQL (single source for every report and slide) |
| Screenshots | a captured set of every demo screen (`docs/11-handin/screens/`) for the agents to use |
| Rubric | 🧐 Evaluator scores each "What we will look at" row; no row "weak" without a fix or an honest gap note |

## Phase C — Parallel agents (after the gate; C7 can start right away)
New persona files in `.claude/agents/`: `report-writer.md`, `deck-designer.md`, `demo-director.md`, `first-time-reader.md`, `fact-checker.md`, `researcher.md` (existing personas reused as reviewers).

| Agent | Persona | Produces (in `docs/11-handin/`) |
|---|---|---|
| C1 Style kit | report-writer | `tools/handin/style.py` (BlueJay palette, tables, callouts, evidence pills) + `build_reports.py` (ReportLab) + diagram palette for draw.io/mermaid |
| C2 Reports | report-writer ×(2–3) + 🩺/🔧/🤖 lenses | **R0** Foundry from scratch (a primer for a newcomer) · **R1** Pipelines (raw → clean → incremental) · **R2** Ontology · **R3** AI function (extraction, cache, grounding, eval) · **R4** Application (Workshop: how to use it, the 3 questions, triage) · **R5** Design decisions and what we did not do · **R6** Optimization log (O1–O3, including the failure) · **R7** Data judgment (42+ data issues: handled vs left). Each PDF opens with a plain-language summary, uses diagrams, and ends with a gate or "how we know" section |
| C3 Diagrams | architect | v1 set reflecting the real build: data flow, ontology, incremental FAERS, label check, change feed, demo path map. Mermaid + draw.io (Visio-ready), rendered PNG/PDF, diagram book refreshed |
| C4 Architecture note | architect | the one-page note: diagram + the 3–4 decisions that mattered + what we chose not to do (PDF) |
| C5 Deck | deck-designer + demo-director | 20-minute deck (pptxgenjs → .pptx + PDF preview), `content_storyboard.md`, `speaking_script.md` (timed), `slide_explanations.md`, Q&A backup slides tied to each rubric row |
| C6 Demo path | demo-director | `demo-navigation-guide` (PDF + .md): every click in Foundry in order (Workshop as the officer → under the hood: Lineage → Code repo → Ontology Manager → Object Explorer → Action → AIP), what to say at each stop, which rubric row it proves, and a **ripple table** "change this here → this changes there" (for example, a synonym row → label status → ranked queue → screen) |
| C7 Research | researcher + 🛡️ compliance | Read-only web scan of ClinicalTrials.gov ("clin org"), "clinhub" (identify what it is), DrugBank, FDA Orange Book, NIDA, and Claude healthcare/life-sciences connectors. For each: what it offers, licence/cost, PHI risk, how it could support a pharmacist review loop. Output: `docs/09-roadmap/another-month.md` + a slide |

**Rubric map** (every row must be shown in the deck and the demo):

| Row | Main evidence |
|---|---|
| Architecture | R1/R2, note, lineage stop |
| Optimization | R6, O1–O3 |
| Data judgment | R7, data-issue examples |
| Application | live Workshop flow |
| AI reliability | R3, eval + monitoring |
| Communication | note, deck, "another month" |

## Phase D — Review and fix loop
- Run reviewers in parallel: 🧐 evaluator (scores the rubric, as a professor would), first-time-reader (can a newcomer follow it?), fact-checker (every number against `numbers.json`), 💊 safety officer (demo flow), and a cohesion review (deck ↔ reports ↔ demo tell one story).
- Save the reviews as .md, fix, re-render, and look at every PDF and slide before calling it done.
- A dry-run rehearsal script with timings.

## Where I would stop and ask you
- Foundry permissions I can't grant myself (for example Data Health checks).
- Any password or sign-in.
- New decisions (D045 onward) are built as Proposed. I list them for one batch "accept" at the end. (Done 6 Nov: all accepted.)
- No pharmacist is named, so this stays a documented gap.

## Verification
- **Foundry:** SQL counts and EXCEPT checks for each new dataset; the screen tested in View mode; a timed morning flow.
- **Docs:** every number traced to `numbers.json`; every PDF and slide opened and looked at (rendered); the diagram book rebuilt.
- **End:** one list of files plus one commit message and commands for you.
