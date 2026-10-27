# CLAUDE.md — How Claude works in this project

Project: **Medication Safety Signal Monitor** (Soragence technical build brief, Oct 2026).
Platform: Palantir Foundry + AIP. Public data only, no PHI.
Source brief: `docs/00-brief/Soragence-Technical-Build-Brief.pdf` (plain-language summary in `docs/00-brief/brief-summary.md`).

---

## 1. How to respond (applies to every reply)

Write in simple terms. Short sentences. Explain any jargon the first time you use it (e.g. "FAERS (the FDA's adverse event report database)").

Use this shape. Skip a section only when it is truly empty.

```
**TL;DR** — 1–3 lines: the answer or what was done.

**What changed** — only when the approach, design or plan moved.
  Before → Now → Why. One line each. Link the approach .md file.

**Do next** — numbered, concrete actions. Mark who acts: (you) / (Claude) / (boss).

**Details** — only what is needed to act. Tables over paragraphs.

**Compass** — 📍 Phase · Step · Next milestone · Open blockers
```

Rules:
- Lead with the answer, not the reasoning.
- One recommendation, not a list of options. Show alternatives only when the user must choose.
- Say plainly when something is an assumption, a guess, or unverified.
- Link files with relative paths so they are clickable.
- No walls of text. If a reply is getting long, move the depth into a .md file and link it.

## 2. The Compass (keep it current)

`COMPASS.md` is the single source of truth for "where are we and where are we going".
- Update it whenever the phase, step, a key decision, a blocker or the next milestone changes.
- End every substantive reply with the one-line **Compass** footer drawn from it.

## 0. GROUND RULE: Git and GitHub are manual. Claude never commits.

- Claude **never** runs git or GitHub commands that change anything: no `add`, `commit`, `push`, `pull`, `merge`, `rebase`, `reset`, `tag`, `branch`, `checkout`, `remote`, `config`, and no `gh`. This is also enforced by deny rules in `.claude/settings.json`.
- Claude may run **read-only** git commands (`git status`, `git diff`, `git log`) to write accurate commit messages.
- At the end of any change, Claude gives the user: **(1)** a ready-to-paste commit message, and **(2)** the exact commands, in `bash` code blocks, one command per block. The user runs them.
- **GitHub account: `vrbabu9000` only. Never `vrajesh9000`.** Remote = `git@github.com-personal:vrbabu9000/<repo>.git` (the SSH alias for the personal key). Repo-local identity = `vrbabu9000 <vrb.canada@gmail.com>`. Before any push command, Claude tells the user to run `git config user.name` to confirm.
- Commit messages: Conventional Commits style (`docs:`, `feat:`, `chore:` …), short subject, bullet body. No AI co-author trailer unless the user asks.

## 2b. Activity log (keep it current)

`ACTIVITY-LOG.md` lets the user restart after days away. At the end of every working session:
- Update the **Pick up here** box (last session, where we are, next 3 actions, waiting on).
- Add a dated entry at the top of the log: what was done, decisions made, files created (linked).

## 2c. Decisions, learnings and compass versions (mandatory)

- **Never edit a decision in place.** A changed decision gets a new version (`D### vN`) or a superseding D-number. Log it in the **Decision changes** table at the top of `docs/06-decisions/DECISIONS.md` (date · before · now · trigger/evidence · compass version).
- Anything realised on the fly goes in the **Learnings** table in the same file, linked to the decision or data issue it changed.
- **COMPASS is versioned.** On any change to phase, step, blocker, schedule, cut list or a decision: copy COMPASS.md to `docs/00-compass/history/COMPASS-vNN.md`, bump the version, and add a change-log row (version · date · what moved · decisions changed).
- **Time is tracked** in `docs/10-delivery/BACKLOG.md` (owner · hours · due · status). Run the ⏱️ Delivery Lead (`.claude/agents/delivery-lead.md`) at the end of each working session, or when the user asks.

## 3. Every new approach gets a .md file

Whenever we try a new approach (design, pipeline strategy, model/prompt, ontology shape, UI flow):
1. Copy `docs/05-approaches/_TEMPLATE.md` to `docs/05-approaches/A###-short-name.md` (next number).
2. Fill **Before / Now / Why**, the design-thinking stage, the result and the verdict (keep / drop / park).
3. Add a row to `docs/05-approaches/INDEX.md`.
4. If it settles a lasting choice, also log it in `docs/06-decisions/DECISIONS.md`.

Never delete a dropped approach. Mark it `Dropped` and say why. The history is part of the deliverable ("what we tried that did not help").

## 4. Design thinking is the frame

Tag work with its stage: **Empathize → Define → Ideate → Prototype → Test**.
Design-thinking artifacts live in `docs/02-design-thinking/`. The end user is the
**hospital pharmacy safety officer**. Test every feature against her three morning questions:
1. Which drugs have adverse events being reported that the label does not mention?
2. Which drugs have an active recall?
3. What has changed since yesterday?
…and the trust rule: **every flag traces back to its source.**

## 5. Diagrams (Visio-ready)

Whenever a diagram would help understanding (architecture, data flow, ontology, process, data shapes, numbers), make one.
**Diagrams are separate files the user can open: PNG + PDF. Never put diagram code inside a .md file** (D017).
- Source: `docs/diagrams/src/NN-topic-vX.mmd` (Mermaid; charts use `xychart-beta`).
- Render: `bash tools/render_diagrams.sh` → `docs/diagrams/png/`, `docs/diagrams/pdf/`, and `docs/diagrams/diagram-book.pdf` (all diagrams in one PDF).
- In .md files, only **link** to the PNG and PDF.
- Editable for Visio: `docs/diagrams/drawio/*.drawio` → open in draw.io → *File → Export as → VSDX*.
- Bump the version on change and keep the old one. Look at the rendered PNG before telling the user it's done.

## 6. Personas (agent lenses)

Persona definitions live in `.claude/agents/`. By default Claude applies the relevant lenses **inline**
and labels them (e.g. "🩺 PV SME view: …"). Spawn a persona as a separate subagent only when the
user asks (e.g. "ask the safety officer persona", "run the reviewer").

| Persona | File | Use for |
|---|---|---|
| 🏗️ Solution Architect | `architect.md` | Raw→ontology design, pilot→scale, trade-offs |
| 🔧 Data Engineer | `data-engineer.md` | Pipelines, incremental builds, partitioning, optimization log |
| 🤖 AI/LLM Engineer | `ai-engineer.md` | Label extraction, AIP, hallucination checks, drift, LLM cost |
| 🩺 Pharmacovigilance SME | `pv-sme.md` | Signal methods, MedDRA, FAERS quirks, label semantics |
| 💊 Pharmacy Safety Officer | `safety-officer.md` | End-user voice, workflow, trust, triage |
| 🎨 Design-Thinking Lead | `design-lead.md` | Empathy, problem framing, prototypes, user tests |
| 🛡️ Compliance & Security | `compliance.md` | No-PHI, data licensing (MedDRA!), audit, production readiness |
| 🧐 Evaluator / Red Team | `evaluator.md` | Scores work against the Soragence rubric; finds holes |
| ⏱️ Delivery Lead | `delivery-lead.md` | Time left vs work left, late tasks, cut list, compass version bumps (runs as a subagent at session end) |

## 7. Project guardrails (from the brief)

- Public sources only. Never use patient-level or proprietary data.
- Narrow and working beats broad and half-working. Cut breadth before depth.
- Measured, not asserted: every optimization claim needs before/after numbers.
- Where the brief is silent: decide, then write the decision down (`DECISIONS.md`).
- Pilot first, but design so it can scale. Scale ideas go in `docs/09-roadmap/`, not into pilot scope.

## 8. Folder map

See `README.md` → "Where things live".
