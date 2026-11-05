# A014 — Label ↔ FAERS synonym table (reviewed, banded)

| | |
|---|---|
| **Date** | 2026-11-04 |
| **Design-thinking stage** | Ideate → Prototype → Test |
| **Area** | AI / Ontology / Monitoring |
| **Status** | Kept (built and measured; D043 proposed, pharmacist review pending) |
| **Replaces** | none (adds a third label check after D037 text and the step 7 AI terms) |

## What changed
| Before | Now | Why |
|---|---|---|
| A FAERS term is "in the label" only if the exact term (or its US spelling) appears in a safety section | Also when a **reviewed synonym phrase** for that term appears there | Exact matching misses the label's own wording ("delayed gastric emptying" vs FAERS "Impaired gastric emptying"); at 13 drugs these misses top the list (A013) |
| Two outcomes: in label / not in label | Three: in label · **possibly in label** · not in label | A close-but-not-same idea (hyperaesthesia vs hyperalgesia) is neither proof nor absence. D039 G4: uncertain is shown as uncertain |

## The idea in 3 lines
1. A script finds **leads**: sentences in the same drug's reference-label safety sections that share word stems with an unlabeled FAERS term ([synonym_candidates.py](../../foundry/tools/local_run/synonym_candidates.py); review sheet [leads-v1.txt](../../eval/synonyms/leads-v1.txt)).
2. A reviewer decides each lead: **high** (same idea → in label), **medium** (close or broader → possibly in label, not ranked), **rejected** (kept so it is not reviewed twice). v1 = Claude draft; pharmacist review pending.
3. The table ([label_synonyms.py](../../foundry/pipelines/ontology/label_synonyms.py)) is applied by the signals transform with the same text rule as D037. Every match records its phrase, label and section (`label_match_*`), and the table itself is published as `ontology_label_synonyms`.

## Why not MedDRA or an LLM judge on every signal
- MedDRA groupings (the standard answer) need a licence we do not have for a public pilot.
- An LLM reading every label for every signal (~1,300 ranked × long sections) is costly. Its answers would be ungrounded unless quoted, and they would change between model versions. A small reviewed table is cheap, deterministic, versioned and auditable. AI can propose rows later, but a person accepts them.

## How we tested it
1. Rebuilt the whole 13-drug pipeline **locally** (raw pulls from the live APIs → signals) and confirmed it equals Foundry (signals 2,047, FAERS 373,522, label sections 5,431).
2. Leads: 1,550 flagged clinical terms not in label → **232 terms with a lead**, 209 with a short matching phrase (≤ 6 words) → all 209 reviewed.
3. Measured three runs on the same data: baseline → + US-spelling fix → + synonym table. Then deployed and compared Foundry with local.

## Result
| Run | Signals | Ranked | Possibly in label | Statistical hits found in label |
|---|---|---|---|---|
| Baseline (exact text + AI terms) | 2,047 | 1,355 | 0 | 478 |
| + US-spelling fix (`noea`, `rrhoea`, `ised` were missing) | 2,038 | 1,346 | 0 | 487 |
| + synonym table syn_v1 | **1,959** | **1,210** | **72** | 566 (79 by a high synonym) |

- **Ranked queue −145 (−10.7%)**: 81 ranked items are now in the label, and 72 signals moved to "possibly in label" (visible, not ranked).
- Table v1: 48 FAERS terms with high phrases (64 rows), 43 with medium (54 rows), 115 rejected leads (233 rows in all).
- Removed false positives include "Impaired gastric emptying" for all 4 GLP-1s (a = 1,789 for semaglutide; label: "delays gastric emptying"), "Drug hypersensitivity" (tramadol), "Faecaloma", "Small intestinal obstruction" and "Post lumbar puncture syndrome".
- **Real finding kept**: "Optic ischaemic neuropathy" (NAION) stays ranked 2nd for semaglutide (a = 394). None of the 36 safety sections in any semaglutide label in DailyMed mention it, so it is a genuine "not in label" signal, not a synonym miss.
- Foundry equals local exactly (1,959 / 1,210 / 72; 0 duplicate keys). New dataset `ontology_label_synonyms` (233 rows) makes the table visible in Foundry.
- Side effect: `label_check` changed, so every signal has a new `evaluation_id`. The step 8 test decision keeps its old id, which is correct: it was made on the earlier evaluation.
- Also found: a local DailyMed pull got HTTP 429 for 744 of 1,321 labels (rate limit). It was recorded as error rows, not hidden; refetched slowly for the local copy.

## Verdict
**Keep.** A small reviewed table removes 1 in 10 ranked items, every match carries its phrase, label and section, and real signals are left alone. Limits: v1 covers only leads that share words. Pure synonyms with no shared words (e.g. "Hyperhidrosis" → "sweating") rely on reviewer knowledge (9 terms marked "knowledge"), and a pharmacist must confirm the bands.

## Persona check
- 🩺 PV SME: The bands are sensible. "Parent term = high" (intestinal obstruction covers small intestinal obstruction) is the main judgement call to confirm. Rejected rows are as valuable as accepted ones: they stop the same lead being re-argued.
- 💊 Safety Officer: The gastric-emptying noise is gone from the top of every GLP-1 list. "Possibly in label" tells her to check the label rather than escalate.
- 🧐 Evaluator: Good before/after evidence on identical data, plus a Foundry = local check. Still Claude-reviewed; say so until the pharmacist signs.
