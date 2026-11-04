# Working from a cloud session

**Date:** 2026-11-04 · **For:** you, plus any Claude/Codex session that opens this repo from GitHub.

> **Status: on hold (2026-11-04).** Work continues in the local desktop session, because only that session can drive Foundry through Claude in Chrome. Use this guide when cloud sessions are picked up again.

## 1. What a cloud session can and cannot do

| | Cloud session (Claude Code on the web, repo linked) | Local desktop session (this laptop) |
|---|---|---|
| Read all project docs and code | ✅ everything committed to GitHub | ✅ |
| Write and test transform code | ✅ with [foundry/tools/local_run](../../foundry/tools/local_run/README.md), if outbound internet is allowed | ✅ |
| See or click in **Foundry** | ❌ Claude in Chrome runs in *your* Chrome, not in the cloud | ✅ via Claude in Chrome |
| Local-only files | ❌ `prototypes/data/` (FAERS ZIPs, atlas results) and `.claude/settings.local.json` are git-ignored | ✅ |
| Claude's memory from past chats | ❌ only what's written in the repo | ✅ |
| Save work | ⚠️ only by pushing to GitHub. **Blocked by the current git rule (§2)** | ✅ you commit by hand |

All the context a session needs is in the repo: [README](../../README.md) → [ACTIVITY-LOG](../../ACTIVITY-LOG.md) → [COMPASS](../../COMPASS.md) → [contracts](../04-architecture/dataset-contracts-v1.md) → [foundry/README](../../foundry/README.md) (resource map with every RID).

## 2. Decision needed: git in the cloud

The ground rule (CLAUDE.md §0, D013) says Claude never commits or pushes, and `.claude/settings.json` blocks git commands. In a cloud session you have no terminal of your own, and the session's changes vanish when it ends unless they are pushed. So under today's rule, cloud work can't be saved.

| Option | How it works | Trade-off |
|---|---|---|
| **A (recommended)** Cloud-only exception | In cloud sessions only, Claude may commit to a **new branch** and open a **pull request**. It may never push to `main`, merge, or force-push. You review and merge on GitHub. Local rule unchanged | Small rule change (D013 v2) plus settings edit |
| B Keep the rule | Cloud Claude writes the change as a patch or file content in chat; you copy it to your laptop and commit | No rule change, but tedious and error-prone |
| C Docs-only cloud | Use cloud only for reading and planning; all edits stay local | Wastes the cloud session |

Nothing changes until you choose. If you pick A, a local session will update CLAUDE.md §0, `.claude/settings.json`, and log D013 v2.

## 3. The working loop (one build-order step)

1. **(cloud Claude)** Read the pick-up box, write or modify mirror files in `foundry/`, and test with `run_local.py`.
2. **(cloud Claude)** Update ACTIVITY-LOG, COMPASS, DECISIONS and contracts, then push a branch + PR (option A).
3. **(you, GitHub)** Review and merge the PR.
4. **(you, Foundry)** Put the code into Foundry. Either:
   - by hand: follow [foundry/README → How a change reaches Foundry](../../foundry/README.md#how-a-change-reaches-foundry); or
   - from the **local desktop session** with Claude in Chrome: say *"Deploy the files changed in the last PR to Foundry and build them."*
5. **(you)** Check row counts on the dataset page's SQL console, and paste the numbers back into the cloud session (or let the local session record them).

### Doing step 4 by hand in Foundry (if no local session)

| # | Click path |
|---|---|
| 1 | Files → Medication Safety Signal Monitor → `Pipelines` → New → Code repository → Pipelines → **Python Transforms** → name `pipelines_clean` → Create. (Clean transforms use no external source, so no source import is needed.) |
| 2 | Code view → Files → `transforms-python/src/myproject/datasets/` → right-click → New file → same name as the mirror file |
| 3 | Paste the file (without the two `# Mirror of` lines) → **Commit** → **Build** |
| 4 | Open each output in `Data/clean` → SQL console → run the checks listed in the PR |

## 4. Prompt to start step 4

Paste this into the cloud session as the first message:

```text
Read README.md, ACTIVITY-LOG.md (Pick up here), COMPASS.md, CLAUDE.md, docs/04-architecture/dataset-contracts-v1.md,
docs/04-architecture/foundry-conventions/project-build-order-v1.md (step 4) and foundry/README.md before doing anything.

Task: build-order step 4 — shared drug identity for the oxycodone slice, as Foundry clean transforms (mirrors in
foundry/pipelines/clean/), tested locally with foundry/tools/local_run/run_local.py.

First run the raw transforms locally to get inputs:
  raw_rxnorm.py, raw_openfda_products.py, and raw_dailymed_spl.py (the last makes ~266 calls; fine).

Build these datasets (contracts §2; keys must be unique; uncertain matches stay visible with a reason, never dropped):
1. clean_drug_ingredients — the formulary ingredient(s) in scope (today: oxycodone 7804). Key ingredient_rxcui.
2. clean_drug_identity — one row per raw drug string seen in raw_openfda_drugsfda products.active_ingredients.name and
   raw_openfda_ndc active_ingredients.name -> ingredient_rxcui, match_method, rxnorm_version. Exact match only (D020):
   upper/trim, split combinations, map salt forms via RxNorm PIN names in raw_rxnorm_related (OXYCODONE HYDROCHLORIDE,
   OXYCODONE TEREPHTHALATE -> 7804); non-formulary partners (ACETAMINOPHEN, NALOXONE...) get matched=false, not dropped.
3. clean_drug_product_map — ingredient_rxcui <-> product_key (= application_number, D039 G2) from Drugs@FDA, plus
   product_number, brand_name, dosage_form, route, marketing_status, is_combination. Many-to-many allowed.
4. clean_drug_package_map — package_ndc11 (11-digit normalised, keep printed form too) -> product_ndc, application_number
   (blank for bulk/compounded: key = labeler + product code, tag per D-R6), from raw_openfda_ndc packaging[].
5. clean_label_product_map — (setid, version) -> application_number(s) parsed from <approval><id extension> in
   raw_dailymed_spl_xml; flag reference label per product (owner's label, same route; D039 G3 / LD1).

Checks to save as numbers in the PR description and ACTIVITY-LOG: uniqueness of every key; match / ambiguous /
unmatched counts; OxyContin chain resolves: oxycodone 7804 -> NDA022272 -> package 59011-410-10 -> label
bfdfe235-d717-4855-a3c8-a13d26dadede v44 (reference trace T13, proposals/2026-11-02-gold-set-v2/cards/T13-oxycontin.md).

Write clean transforms with polars (transform.using + lightweight inputs/outputs, as in the repo template examples.py)
so they run in run_local.py; if that API is unclear, say so and propose the Spark alternative instead of guessing.
Clean transforms take dataset Inputs only — no external sources (exports stay off).
Then update foundry/README.md, the contracts (as-built notes), DECISIONS learnings, ACTIVITY-LOG and COMPASS,
and follow the git rule in CLAUDE.md §0 (or D013 v2 if adopted).
```

## 5. Before the first cloud session

1. **(you)** Commit and push this README/guide update (commands in the chat that produced this file).
2. **(you)** Choose the git option in §2.
3. **(you)** In claude.ai/code, start a session on `vrbabu9000/medication-safety-signal-monitor` and paste the §4 prompt.
4. **(you)** Keep the laptop session available for Foundry clicks, or plan to paste files by hand.
