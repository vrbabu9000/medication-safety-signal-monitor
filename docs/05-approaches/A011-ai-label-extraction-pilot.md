# A011 — AI label extraction pilot (Claude Sonnet 5.5 in a cached, grounded Python transform)

| | |
|---|---|
| **Date** | 2026-11-04 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | AI |
| **Status** | Kept (pilot, D041 accepted); prompt p2 needed before widening |
| **Replaces** | none (implements [conventions §8](../04-architecture/foundry-conventions/conventions-v1.md#8-ai-extraction-and-evidence-contract) and D005) |

## What changed
| Before | Now | Why |
|---|---|---|
| AIP access proven only (step 1 test) | A Foundry transform asks an AIP model for every reaction in each safety section, with an exact quote; checks each quote against the text; caches by content | Brief Part B: the LLM reads the label so FAERS can be compared with it |

## The idea in 3 lines
1. One model call per **section** (not per label), with an exact-quote rule. Code checks each quote against the section text, so an invented quote shows as `not_found`.
2. Cache key = setid + version + section + text hash + parser/prompt/model version. A rebuild with the same text makes **0 model calls** (D005). Failures (`parse_error`, `model_error`) are kept visible and retried; they never mean "the label doesn't mention it".
3. Pilot sample first: 2 reference labels (OxyContin v44, modern format; one older-format oxycodone/acetaminophen generic), 9 sections. Gold set frozen before scoring.

## How we tested it
- Local logic test with a fake model: [check_extraction.py](../../foundry/tools/local_run/check_extraction.py), 10/10 pass (cache, made-up quote, broken JSON, retry, dedup).
- Foundry run 1 against the AIP model; then an upstream rebuild with unchanged text.
- Score vs the [gold set](../../eval/gold-set/step7-pilot-gold-v1.json) with [check_gold.py](../../foundry/tools/local_run/check_gold.py).

## Result
| Measure | Value |
|---|---|
| Sections | 9 of 9 `ok` (0 parse errors, 0 model errors) |
| Reactions extracted | 403 (OxyContin: 146 AR, 29 W&P, 12 boxed, 4 contraindications; generic: 127, 39, 29, 12, 5) |
| Grounding | **403/403 quotes found exactly** in the section text (0 not_found, 0 case-only) |
| Recall vs gold (4 short sections) | **32/35 = 0.91**. Missed: paralytic ileus ×2 (folded into "gastrointestinal obstruction"), hepatotoxicity (given as "acute liver failure" + "liver injury") |
| Cost, run 1 | 41,704 prompt + 29,072 completion tokens; 143 s of model time; job 2 m 43 s |
| Cache | After the upstream rebuild: **9/9 sections from cache, 0 model calls**, output unchanged |

## Verdict
Keep the design. Two things to fix before widening:
- **Atomic terms.** The model groups items, e.g. "addiction, abuse, and misuse" and "overdose and death". Recall above counts a grouped term as finding each part (lenient). FAERS needs one term per item, so prompt **p2** must say "one reaction per item".
- **Long sections need a hand check.** Warnings/Precautions and Adverse Reactions (366 of 403 items) are not in the gold set yet. They go into the pharmacist packet.

## Persona check
- 🤖 AI Engineer: grounding is a string check, not a meaning check. A real quote can still be paired with the wrong term. Next: a "term is in quote" rate (stored as `term_in_quote`) and a pharmacist sample.
- 🩺 PV SME: compound terms and population qualifiers (neonates) matter for FAERS matching. Population is stored; atomicity is the p2 fix.
- 💊 Safety Officer: every AI line links to the exact quote and label version (LabeledReaction → Label), which is the trust rule.
- 🧐 Evaluator: n = 4 short sections is a pilot, not proof. Report it as such, and keep the D015 target (F1 ≥ 0.85) for the widened set.
