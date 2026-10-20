# AGENTS.md — How Codex works in this project

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

**Do next** — numbered, concrete actions. Mark who acts: (you) / (Codex) / (boss).

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

## 0. GROUND RULE: Git and GitHub are manual. Codex never commits.

- Codex **never** runs git or GitHub commands that change anything: no `add`, `commit`, `push`, `pull`, `merge`, `rebase`, `reset`, `tag`, `branch`, `checkout`, `remote`, `config`, and no `gh`. This is also enforced by deny rules in `.Codex/settings.json`.
- Codex may run **read-only** git commands (`git status`, `git diff`, `git log`) to write accurate commit messages.
- At the end of any change, Codex gives the user: **(1)** a ready-to-paste commit message, and **(2)** the exact commands, in `bash` code blocks, one command per block. The user runs them.
- **GitHub account: `vrbabu9000` only. Never `vrajesh9000`.** Remote = `git@github.com-personal:vrbabu9000/<repo>.git` (the SSH alias for the personal key). Repo-local identity = `vrbabu9000 <vrb.canada@gmail.com>`. Before any push command, Codex tells the user to run `git config user.name` to confirm.
- Commit messages: Conventional Commits style (`docs:`, `feat:`, `chore:` …), short subject, bullet body. No AI co-author trailer unless the user asks.

## 2b. Activity log (keep it current)

`ACTIVITY-LOG.md` lets the user restart after days away. At the end of every working session:
- Update the **Pick up here** box (last session, where we are, next 3 actions, waiting on).
- Add a dated entry at the top of the log: what was done, decisions made, files created (linked).

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

Whenever architecture, data flow, ontology or a process is discussed, produce a diagram:
- **Mermaid** inside the .md file (renders on GitHub and in VS Code) for quick views.
- **draw.io source** (`docs/04-architecture/diagrams/*.drawio`) for editable, presentation-grade diagrams.
  These open in diagrams.net / draw.io desktop and export to **Visio (.vsdx)** via *File → Export as → VSDX*.
- Name diagrams `NN-topic-vX.drawio`. Bump the version on change and keep the old one.

## 6. Personas (agent lenses)

Persona definitions live in `.Codex/agents/`. By default Codex applies the relevant lenses **inline**
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

## 7. Project guardrails (from the brief)

- Public sources only. Never use patient-level or proprietary data.
- Narrow and working beats broad and half-working. Cut breadth before depth.
- Measured, not asserted: every optimization claim needs before/after numbers.
- Where the brief is silent: decide, then write the decision down (`DECISIONS.md`).
- Pilot first, but design so it can scale. Scale ideas go in `docs/09-roadmap/`, not into pilot scope.

## 8. Folder map

See `README.md` → "Where things live".
