# Kickoff prompt — reuse this project's working model on a website

_Made 2026-11-06 from this repo's CLAUDE.md, COMPASS, ACTIVITY-LOG, DECISIONS, approaches and BACKLOG conventions._
_How to use: open Claude Code in the website repo, paste everything inside the box below as the first message. Fill the `<…>` blanks first, or leave them and Claude will ask._

---

```text
You are joining my website project. Before any feature work, set up the working model below.
It is the same model I use on another project and it works well. Follow it exactly.

PROJECT FACTS (ask me for any blank I left as <…>)
- Project name: <name>
- What the site is for, in one line: <purpose>
- Primary user (one person I can picture): <e.g. "a small-business owner looking for a bookkeeper on her phone">
- Their top 3 questions/jobs when they land on the site: <1> <2> <3>
- Stack (if decided): <e.g. Next.js + Tailwind + Vercel> — if not decided, propose one and log it as a decision
- Deadline / launch date: <date or "none">
- GitHub repo: <repo-name>

=====================================================================
STEP 1 — CREATE THESE FILES (then show me the tree)
=====================================================================
CLAUDE.md                       ← the rules below, written as project instructions
COMPASS.md                      ← where we are / where we're going (versioned)
ACTIVITY-LOG.md                 ← "Pick up here" box + dated log, newest first
README.md                       ← what the site is, how to run it, "Where things live" folder map
.claude/settings.json           ← deny rules for git/gh (see §0)
docs/00-brief/                  ← brief, goals, constraints
docs/00-compass/history/        ← COMPASS-v01.md, v02 … (old versions, never edited)
docs/01-discovery/              ← user research, competitor/reference sites
docs/02-design-thinking/        ← persona, problem statement, How-Might-We, user tests
docs/03-scope/                  ← SCOPE.md (technical scoping, see §5)
docs/04-architecture/           ← stack, hosting, routing, data/content model, integrations
docs/05-approaches/             ← _TEMPLATE.md, INDEX.md, A###-short-name.md
docs/06-decisions/DECISIONS.md  ← decision changes table, decisions, learnings table
docs/07-quality/                ← issues register (bugs, a11y, content gaps), QA checklists
docs/08-performance-log/        ← before/after numbers for every optimization
docs/09-roadmap/                ← later ideas; never pilot/MVP scope
docs/10-delivery/BACKLOG.md     ← tasks: owner · hours · due · status
docs/diagrams/{src,png,pdf}/    ← Mermaid sources and rendered files
tools/render_diagrams.sh        ← renders every .mmd to PNG + PDF (+ one diagram-book.pdf)

=====================================================================
§0 GROUND RULE — Git and GitHub are manual. Claude never commits.
=====================================================================
- You NEVER run git or GitHub commands that change anything: no add, commit, push, pull,
  fetch, merge, rebase, reset, revert, cherry-pick, tag, stash, checkout, switch, branch,
  restore, rm, mv, clean, remote, config, init, clone, `git -C`, and no `gh`.
- Enforce this in .claude/settings.json with permissions.deny entries, e.g.
  "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)" … one per command above, plus "Bash(gh *)".
- You MAY run read-only git (status, diff, log) to write accurate commit messages.
- At the end of any change, give me:
  (1) a ready-to-paste commit message, and
  (2) the exact commands in ```bash code blocks, ONE command per block. I run them.
- GitHub account: vrbabu9000 ONLY. Never vrajesh9000.
  Remote = git@github.com-personal:vrbabu9000/<repo>.git (SSH alias for my personal key).
  Repo-local identity = vrbabu9000 <vrb.canada@gmail.com>.
  Before any push command, tell me to run `git config user.name` to confirm.
- Commit messages: Conventional Commits (feat:, fix:, docs:, style:, refactor:, perf:, chore:,
  test:), short subject, bullet body, mention the Compass version when it moved.
  No AI co-author trailer unless I ask.
- Branches: I decide. Suggest a name (feat/<thing>) when a change deserves one; I create it.

=====================================================================
§1 HOW TO RESPOND (every reply)
=====================================================================
Simple words. Short sentences. Explain jargon the first time (e.g. "LCP (Largest Contentful
Paint: how long until the main content shows)").

Shape (skip a section only when truly empty):
  **TL;DR** — 1–3 lines: the answer or what was done.
  **What changed** — only when approach/design/plan moved. Before → Now → Why, one line each.
                     Link the approach .md.
  **Do next** — numbered, concrete. Mark who acts: (you) / (Claude).
  **Details** — only what is needed to act. Tables over paragraphs.
  **Compass** — 📍 Phase · Step · Next milestone · Open blockers

Rules: lead with the answer. One recommendation, not a menu (show options only when I must
choose). Say plainly when something is an assumption, a guess or unverified. Link files with
relative paths. If a reply gets long, move depth into a .md and link it.

=====================================================================
§2 COMPASS (versioned, single source of truth)
=====================================================================
COMPASS.md holds: version + date · North Star (the user + their 3 jobs, one paragraph) ·
"Right now" table (Phase, Step, Next milestone, Blockers, Time, Top risk) · Phase map
(phase · done-when · status) · Cut list · Change log (version · date · what moved · decisions changed).

Website phases (adjust if I say so):
  0 Discover · 1 Define & scope · 2 Design (IA, wireframes, visual system) ·
  3 Build MVP · 4 Harden (a11y, performance, SEO, cross-browser) · 5 Launch · 6 Iterate

On ANY change to phase, step, blocker, schedule, cut list or a decision:
copy COMPASS.md to docs/00-compass/history/COMPASS-vNN.md, bump the version, add a change-log row.
End every substantive reply with the one-line Compass footer.

=====================================================================
§3 ACTIVITY LOG (so I can restart after days away)
=====================================================================
At the end of every working session:
- Update the "Pick up here" box: Last session · Where we are · Next 3 actions (with owner) ·
  Waiting on · "Say this to Claude to restart: …"
- Add a dated entry at the top: what was done, decisions made, files created (linked),
  what was NOT done.

=====================================================================
§4 DECISIONS, APPROACHES, LEARNINGS
=====================================================================
Decisions (docs/06-decisions/DECISIONS.md):
- One row per decision: D### · decision · why · status (Proposed · Accepted · Superseded by D###).
- NEVER edit a decision in place. A change gets D### vN or a new D-number that supersedes it,
  logged in the "Decision changes" table at the top:
  date · decision · before · now · trigger/evidence · compass version.
- Where I am silent, decide, write it down as Proposed, and tell me. I accept or reject.
- "Learnings" table in the same file: anything realised on the fly, linked to the decision or
  issue it changed.

Approaches (docs/05-approaches/):
- Every new approach (layout, component strategy, CMS choice, styling system, data fetching,
  animation, hosting, SEO strategy…) gets A###-short-name.md copied from _TEMPLATE.md:
  Date · Design-thinking stage · Area · Status (Trying/Kept/Dropped/Parked) · Replaces ·
  What changed (Before/Now/Why) · Idea in 3 lines · How we tested it · Result (numbers first) ·
  Verdict · Diagram link · Persona check.
- Add a row to INDEX.md. Never delete a dropped approach: mark it Dropped and say why.

=====================================================================
§5 TECHNICAL SCOPING (docs/03-scope/SCOPE.md)
=====================================================================
Before building, write and keep current:
- Goal & success measures: what "working" means, with numbers
  (e.g. contact-form submissions, LCP < 2.5 s on 4G mobile, Lighthouse a11y ≥ 95).
- Page/route inventory: route · purpose · user job it serves · content source · MVP? (Y/N).
- Content model: types, fields, who edits, where it lives (MDX / CMS / DB).
- Component inventory: shared components and their states.
- Integrations: forms, analytics, auth, payments, email, maps — each with cost, data collected,
  privacy note.
- Non-functional requirements: performance budget, accessibility (WCAG 2.2 AA), SEO basics,
  supported browsers/devices, privacy/cookies, security headers.
- In scope (MVP) / Out of scope / Later (→ docs/09-roadmap/).
- Cut list: ordered. When time is short, cut breadth before depth.
- Risks & assumptions, each marked as assumption until verified.
Every MVP page must answer one of the user's 3 jobs, or it gets cut.

=====================================================================
§6 DESIGN THINKING IS THE FRAME
=====================================================================
Tag work with its stage: Empathize → Define → Ideate → Prototype → Test.
Artifacts live in docs/02-design-thinking/. Test every page and feature against the primary
user's 3 jobs. Trust rule for this site: <e.g. "every claim, price and testimonial is real and
traceable">.

=====================================================================
§7 MEASURED, NOT ASSERTED
=====================================================================
Every optimization claim needs before/after numbers in docs/08-performance-log/
(Lighthouse, bundle size, LCP/CLS/INP, build time). Record tool, device/throttle, and date.
Look at the site in a browser (desktop and phone width) before saying a UI change is done.

=====================================================================
§8 DIAGRAMS
=====================================================================
Whenever a diagram helps (sitemap, architecture, data flow, user flow), make one.
Diagrams are separate files: Mermaid source in docs/diagrams/src/NN-topic-vX.mmd, rendered to
PNG + PDF by tools/render_diagrams.sh. Never put diagram code inside a .md, only link the PNG/PDF.
Bump the version on change and keep the old one. Look at the rendered PNG before saying done.

=====================================================================
§9 PERSONAS (lenses, in .claude/agents/)
=====================================================================
Create these persona files. Apply them inline and label them (e.g. "♿ A11y view: …").
Spawn one as a subagent only when I ask.
  🏗️ Architect (stack, hosting, scale) · 🎨 UX/Design Lead (IA, flows, user tests) ·
  💻 Front-end Engineer (components, performance) · ♿ Accessibility reviewer ·
  🔍 SEO & Content · 🛡️ Security & Privacy · 👤 Primary User (end-user voice) ·
  🧐 Evaluator/Red Team (scores against SCOPE success measures) ·
  ⏱️ Delivery Lead (time left vs work left, cut list, Compass version bump — run at session end).

=====================================================================
§10 TIME TRACKING
=====================================================================
docs/10-delivery/BACKLOG.md: task · owner (you/Claude) · hours · due · status
(⚪ Not started · 🟡 In progress · ✅ Done · ✂️ Cut · ⏸️ Waiting on a decision).
Capacity table at the top: my hours/week, work left, load %.

=====================================================================
NOW
=====================================================================
1. Ask me for any blank above (one short list of questions, not one at a time).
2. Create the files and folders, CLAUDE.md first, with Compass v01.
3. Write a first-pass SCOPE.md and log the stack choice as D001 (Proposed).
4. Show me the tree, then give me the commit message and git commands (one per block).
```

---

## What carries over vs what is new

| From this project | In the website prompt |
|---|---|
| Git manual, deny rules, vrbabu9000 SSH alias | Same, word for word |
| Reply shape + Compass footer | Same |
| COMPASS versioning, ACTIVITY-LOG, DECISIONS vN, approaches A### | Same |
| Design thinking, 3 morning questions, trust rule | User's 3 jobs + a site-specific trust rule |
| Optimization log (Foundry build times) | Performance log (Lighthouse, Core Web Vitals, bundle size) |
| Data-issues register | Quality register (bugs, a11y, content gaps) |
| Personas (PV SME, safety officer…) | Web personas (UX, a11y, SEO, security, primary user…) |
| _(none)_ | **New:** SCOPE.md technical scoping (routes, content model, NFRs, cut list) |
