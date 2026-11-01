# Daily checks and 30-case independent reference set

_October 31, 2026 · Prototype → Test · All work isolated here. No existing project file, Foundry resource, schedule, Git state or other project's skill was modified._

## Start with the Claude prompt

1. Open [CLAUDE-PROMPT.md](CLAUDE-PROMPT.md) and paste its fenced prompt into Claude Code.
2. Claude should read **only the prompt and [shared/](shared/)** for this independent run. The input pack is complete: [READY.json](shared/READY.json).
3. Claude writes its independent outputs to `claude/`. That folder is intentionally absent until Claude runs.
4. Do not give Claude `codex/`, this folder's build script or the answer summary before its output is frozen.

[Claude-only input ZIP](claude-inputs.zip) contains the prompt and common evidence/questions, with no expected answers. For a web chat, upload/extract that pack in a file-capable environment and adapt only the local paths; do not assume chat has filesystem access. The prompt was drafted with the read-only [Claude bridge skill](../../../captain-claude-bridge/.agents/skills/claude-prompting/SKILL.md); no prompt was automatically sent.

The repository ignores ZIP files. This local convenience bundle can be recreated after cloning with `python3 proposals/2026-10-31-daily-check-and-gold-set-v1/package_claude_inputs.py`; the original shared inputs remain the authoritative artifacts.

## What is delivered

| Artifact | Purpose |
|---|---|
| [DAILY-CHECKS.md](DAILY-CHECKS.md) | Publisher frequencies/time limits, proposed morning polling, no-change behavior and failure recovery. Includes Mermaid and [editable draw.io](diagrams/20-daily-check-v1.drawio). |
| [shared/cases.json](shared/cases.json) | Exactly 30 fixed questions; source IDs and input scope; **no answers**. |
| [shared/source-manifest.json](shared/source-manifest.json) | Original requests, capture times, source metadata, hashes and real fetch failures. |
| [shared/evidence/](shared/evidence/) | Original public evidence plus deterministic text views for both annotators. |
| [codex/answers.jsonl](codex/answers.jsonl) | Codex's independently produced candidate answers with source locators and rationale. |
| [codex/findings.md](codex/findings.md) | Readable table of all 30 answers. Keep this away from Claude until its answers are frozen. |
| [codex/validation.json](codex/validation.json) | Actual counts and limits; all human review pending. |
| [human-review-template.jsonl](human-review-template.jsonl) | Empty approve/correct/uncertain review slots for a person. |
| [compare_answers.py](compare_answers.py) | Checks the frozen input hashes and compares both answer files after Claude finishes. |
| [CHECKS.json](CHECKS.json) | Checks actually run. Comparison boundary tests used temporary synthetic fixtures, not actual Claude answers. |

## Exactly what the 30 cases cover

| Source family | Cases | What is tested |
|---|---|---|
| DailyMed | G01–G12: **12** | Six explicit reaction/warning contexts and six context traps, drawn from three opioid product labels. |
| RxNorm | G13–G16: **4** | Ingredient identifiers, apomorphine vs morphine, and both ingredients of Percocet. |
| FAERS | G17–G20: **4** | Captured source date, a real global aggregate term/count, correct query scope, and limits on causal/incidence inference. |
| FDA enforcement | G21–G24: **4** | Actual recall reason/status; current lifecycle and hospital exposure correctly left unknown. |
| Drugs@FDA | G25–G26: **2** | Application sponsor and the specified product/form/strength. |
| NDC Directory | G27–G28: **2** | Package description and a real nonmatch between recall and selected OxyContin package. |
| SrLC | G29: **1** | Specific OxyContin regulatory change entry and safety concept. |
| ClinicalTrials.gov | G30: **1** | Actual study-arm serious-event numerator and denominator. |
| **Total** | **30** | Mixed system reference cases, not 30 clinical discoveries. |

**Candidate, not final gold.** Codex checked source evidence and literal quote anchors. No independent human/clinical adjudication has occurred. All 30 records are marked human review pending. Two expected answers are intentionally unknown, not unresolved source failures. Agreement with Claude is not itself a gold-standard verdict.

**Not a full extraction benchmark.** Twelve cases classify specified concepts in bounded passages. They do not enumerate every reaction in full labels, so they cannot establish full-label recall/F1. The other 18 cases are source-data/identity/interpretation tests. Score categories separately; do not advertise a 30-case clinical AI accuracy number. The sample is small, purposive and correlated; no population-generalization claim is justified.

## Real limitations found while capturing sources

- **Drug-filtered FAERS queries failed.** Two requests returned HTTP 403 with `API_KEY_MISSING`; exact failure bodies are saved. No patient reports were requested. G17–G19 use the successful **unfiltered** aggregate, whose metadata reports July 30, 2026. The count is never relabeled as oxycodone-specific. Live drug-specific count refresh remains blocked until access is resolved.
- **Do not fabricate freshness.** Each response's publisher metadata and retrieval timestamp remain separate. ClinicalTrials.gov returned a `dataTimestamp` without a time zone; it is preserved verbatim. No fake exact publication time is supplied.
- **Entity check matters.** An initial unused SrLC candidate capture (`srlc_oxy`) actually resolves to Ozempic. It is retained as unused capture evidence. G29 uses the independently checked **OxyContin NDA-022272 page, DrugNameID 685**, source ID `srlc_oxy_verified`. Never trust a local filename as proof of entity identity.
- The chosen trial is an older **terminated** study with reported summary outcomes. The denominator is meaningful for that arm, not population risk or proof of safety.
- OnSIDES is excluded from the truth set: it is model-derived, not independent primary evidence, and terminology licensing needs separate review. No licensed MedDRA hierarchy or term dump is added.
- No runtime, cost, Foundry deployment, live daily-monitoring or production-safety claim follows from these artifacts.

## Compare after Claude finishes

From the repository root, run this read-only-input/local-output command. It does not send anything or modify the source packs:

```bash
python3 proposals/2026-10-31-daily-check-and-gold-set-v1/compare_answers.py
```

It expects `claude/answers.jsonl`, verifies identical case IDs and common evidence hashes, then creates a new `comparison/` folder. It refuses duplicate IDs, missing/extra cases or changed shared inputs. It does not overwrite an existing comparison.

Review disagreements **and** a sample of agreements against original evidence. Separate exact-format differences, interpretation differences and genuine source drift. A human can mark an answer approved/corrected/uncertain. Do not modify either original annotation file after comparison; adjudicated truth belongs in a new version with the reviewer/date recorded.

## Reproduction and checks

`capture_sources.py` retrieves public sources into this folder; `build_reference.py` assembles case inputs and Codex answers from the captures. **Do not rerun either against the frozen v1 shared pack.** Make a new version/folder if sources or questions need to change. Claude must not inspect the builder before freezing its answers because it contains Codex's annotations.

Observed checks: exactly 30 unique IDs, eight source families, 26 captured original-source hashes verified, all supplied short quote anchors verified, no answers in the Claude ZIP, and comparison duplicate/missing-ID/mismatch behavior checked with synthetic fixtures. No independent Claude run or human clinical review has been performed.

## Session note and editing boundary

This task did not edit the active root COMPASS, ACTIVITY-LOG or decision files, per the user's earlier instruction. This isolated task adds a prompt, shared evidence/question pack, Codex candidate annotations, daily-check explanation, comparison helper and diagrams. Concurrent Foundry-convention changes appeared elsewhere during the task and were left untouched. The project's root Compass remains the source of its official phase/status; these artifacts are supporting evaluation work only.
