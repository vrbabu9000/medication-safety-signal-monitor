# Git handoff — Foundry conventions, 2026-10-31

Codex did not stage, commit, or push. Run these commands yourself from the repository root. The explicit file list excludes the older, non-adopted `proposals/` folder.

## Ready-to-paste commit message

```text
docs: add Foundry conventions and project build roadmap

- Research Data Forge medallion and ontology tutorials against official docs
- Add naming, key, evidence and refresh conventions with a 12-step build order
- Add editable diagrams and update Compass, decisions and session log
```

## Commands — one command per block

Review the tracked edits:

```bash
git diff --check
```

Stage only this session's files:

```bash
git add README.md COMPASS.md ACTIVITY-LOG.md foundry/README.md docs/00-compass/history/COMPASS-v10.md docs/04-architecture/foundry-conventions docs/04-architecture/diagrams/18-foundry-medallion-v1.drawio docs/04-architecture/diagrams/19-foundry-ontology-conventions-v1.drawio docs/05-approaches/A007-foundry-medallion-conventions.md docs/05-approaches/INDEX.md docs/06-decisions/DECISIONS.md docs/diagrams/src/18-foundry-medallion-v1.mmd docs/diagrams/src/19-foundry-ontology-conventions-v1.mmd docs/diagrams/png/18-foundry-medallion-v1.png docs/diagrams/png/19-foundry-ontology-conventions-v1.png docs/diagrams/pdf/18-foundry-medallion-v1.pdf docs/diagrams/pdf/19-foundry-ontology-conventions-v1.pdf docs/10-delivery/2026-10-31-foundry-conventions-git-handoff.md
```

Review the staged changes, including the new documents:

```bash
git diff --cached --stat
```

```bash
git diff --cached --check
```

```bash
git diff --cached
```

Commit:

```bash
git commit -m 'docs: add Foundry conventions and project build roadmap' -m '- Research Data Forge medallion and ontology tutorials against official docs
- Add naming, key, evidence and refresh conventions with a 12-step build order
- Add editable diagrams and update Compass, decisions and session log'
```

No push command is included. Before any later push, run `git config user.name` and confirm `vrbabu9000`. The project requires the personal SSH remote and local identity documented in AGENTS.md.

## Validation

- Three tutorial transcripts reviewed; source links and timestamps recorded.
- New reference/approach local links checked.
- Both Mermaid diagrams rendered; PNGs visually inspected; PDF headers and draw.io XML checked.
- `git diff --check` passed. No Foundry deployment or runtime tests performed.
