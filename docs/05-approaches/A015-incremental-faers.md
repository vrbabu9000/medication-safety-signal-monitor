# A015 — Incremental FAERS (step 10)

| | |
|---|---|
| **Date** | 2026-11-05 |
| **Design-thinking stage** | Test |
| **Area** | Pipelines |
| **Status** | Kept (correctness gate passed); speed gain **not** shown at 2 quarters |
| **Replaces** | none (runs next to the full rebuild `clean_faers.py`, which stays the baseline and still feeds signals) |

## What changed
| Before | Now | Why |
|---|---|---|
| `clean_faers.py` reads every quarter file on every build | New [clean_faers_incremental.py](../../foundry/pipelines/clean/clean_faers_incremental.py): reads only quarters it has not processed, merges them into a kept **state**, logs each quarter | Brief asks for at least one incremental pipeline; build-order step 10 |
| The D020–D023 rules lived inside one function | `clean_faers.py` now exposes `suspects()` and `finish()`; both pipelines call the same functions | One copy of each rule, so the two paths cannot drift apart |
| No record of what each build processed | `clean_faers_inc_log`: one row per quarter (rows read, deletes, cases replaced/deleted, seconds, mode, identity hash, generation) | "What changed since yesterday" needs a trail; also the evidence for this test |

## The idea in 3 lines
1. **State step (incremental):** each build adds the oldest unprocessed quarter. D022 merge: highest `caseversion` wins, ties go to the newer quarter, then that quarter's deletes. Cases kept from earlier quarters keep their drug and reaction rows.
2. **Outputs step (plain):** rebuild the 3 output tables from the state with the shared `finish()` (the D023 fold needs every current case at once, and it is cheap).
3. **Replay:** if the drug identity changes (hash of `clean_drug_identity`), the state is rebuilt from every quarter as a new generation, because old suspect matches may now be wrong.

## How we tested it
- **Locally first** (runner): build 1 = Q1, build 2 = Q2, build 3 = no new quarter (no-op). Outputs compared with the full rebuild by sorted row hashes. Then changed the identity to force a replay, and changed it back.
- **In Foundry:** build 1 (Q1), forced build 2 (Q2), outputs step, then a fresh full rebuild. Compared with SQL in the repo's SQL panel: `count(*)` and `EXCEPT ALL` **in both directions** for all 3 outputs.

## Result
**Correctness: identical.**

| Output | Incremental rows | Full-rebuild rows | Only in incremental | Only in full |
|---|---|---|---|---|
| `cases_current` | 792,346 | 792,346 | 0 | 0 |
| `case_reactions` | 2,554,017 | 2,554,017 | 0 | 0 |
| `drug_reaction` | 373,522 | 373,522 | 0 | 0 |

**Replace and delete behaviour (from the log, Foundry):**

| Quarter | Mode | DEMO rows read | Deletes in file | Cases replaced | Cases deleted | Cases after |
|---|---|---|---|---|---|---|
| 2026q1 | incremental (gen 1) | 397,224 | 6,135 | 0 | 0 | 397,224 |
| 2026q2 | incremental (gen 1) | 422,459 | 4,217 | 26,681 | 655 | 792,346 |

**Replay (local only):** identity changed → suspects 79,270 → 77,677; identity restored → back to 79,270 and equal to the full rebuild again. Not yet run in Foundry.

**Speed: no gain yet (measured, Foundry builds page).**

| Path | What it reads | Build time |
|---|---|---|
| Full rebuild (`clean_faers.py`), 2 quarters | 2 quarters of files (819,683 DEMO rows + their DRUG/REAC) | **32 s** |
| Incremental, adding Q2 | 1 quarter of files (422,459 DEMO rows, 52%) + the saved state | 1 m 2 s (state) + 26 s (outputs) = **88 s** |

Why slower: with only 2 quarters, the saving (one quarter's files, ~half the parsing) is smaller than the fixed cost of reading back and rewriting 4 state datasets, plus a second build for the outputs step. Each Foundry build also has start-up time (not measured separately), and the incremental path pays it twice.

## Verdict
**Keep** as the proof that incremental works and is correct (replace, delete, no-op and replay all equal the full rebuild). **Do not switch** signals to the incremental outputs yet: at 2 quarters it is 2.75× slower. Saving one quarter out of N saves roughly (N−1)/N of the file reading, so the trade turns over at a longer history. Measure again at 4+ quarters before switching (O2 in the [optimization log](../08-optimization-log/optimization-log.md)).

Ideas to lower the fixed cost, not tried: write the outputs in the same build as the state (one start-up); keep the state as a single table instead of 3.

## Diagram (if structure changed)
No new diagram: two datasets-in-a-row steps beside the existing FAERS step; the lineage graph in Foundry shows it.

## Persona check
- 🔧 Data Engineer: Correctness first was the right order. The honest result is that incremental costs more than it saves on a 2-quarter pilot. Do not claim a speed-up.
- 🩺 PV SME: The log makes FAERS's quirks visible: 26,681 Q1 cases were updated by Q2 follow-ups, and 655 were deleted. That is 6.9% of Q1 cases changing in one quarter, which supports D022 (upsert, never append).
- 💊 Safety Officer: Nothing changes on her screen. The log is the base for "what changed since the last FAERS quarter".
- 🧐 Evaluator: Meets "prove at least one incremental pipeline" with row-level evidence. The 88 s vs 32 s result must be shown, not hidden; it is good evidence of measured, not asserted.
