# 📒 Activity log — read this first when you come back

## ⏩ Pick up here (always current)
| | |
|---|---|
| **Last session** | 2026-10-27 (planning only; nothing done Oct 21–26) |
| **Where we are** | Exploration + design done. **Nothing built in Foundry yet.** New plan: build Thu Oct 29 → Mon Nov 2, demo **Wed Nov 4** → [game plan v1](docs/10-delivery/game-plan-v1-oct27-to-nov4.md) |
| **Next 3 actions** | 1. (you) Text boss: demo Wed Nov 4 · 2. (Claude) Build the ready-to-run kit Oct 27–28 · 3. (you, Oct 28, optional 1 h) approve sheet + Foundry/AIP smoke test |
| **Waiting on** | Boss OK on Nov 4 · AIP on Developer Tier (unverified) |
| **Say this to Claude to restart** | _"Read ACTIVITY-LOG and COMPASS, then run the delivery lead."_ |

---

## Log (newest first)

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
