# A018 — AI review backed by papers (PubMed) for watched signals

| | |
|---|---|
| **Date** | 2026-11-05 |
| **Design-thinking stage** | Ideate → Prototype |
| **Area** | AI / App |
| **Status** | Trying (6 samples; not in pilot scope; not built) |
| **Replaces** | none (adds context to ranked signals; partly covers the missing pharmacist reviewer) |

## What changed
| Before | Now | Why |
|---|---|---|
| A ranked flag = "reported a lot, not in the label"; nobody checks it against published evidence | For the signals the officer watches, an AI reads PubMed abstracts and writes a cited verdict; a pharmacist signs it | No pharmacist reviewer available; the officer needs to know which flags matter; every opinion must trace to a source |

## The idea in 3 lines
1. The officer picks a watch list (drugs × top K ranked `not_in_label` signals).
2. Code fetches PubMed evidence (3 free calls, ~2 s), drops retractions and off-topic papers. The model writes a verdict where every reason cites a PMID.
3. Code checks the citations; a pharmacist agrees or disagrees in Workshop.

## How we tested it
6 top-ranked signals across 5 drugs, reviewed by Claude from abstracts ([feature folder](../12-features/ai-literature-review/README.md)).

## Result
2 real · 1 plausible (FAERS evidence only) · 3 noise or not enough evidence. Found 1 likely synonym miss (tirzepatide Allodynia ↔ label "dysesthesia"). ~$0.09 per review on Opus 5.5 (estimate); 25-signal watch list ≈ $2.20 + ~50 pharmacist minutes ([cost-estimate](../12-features/ai-literature-review/cost-estimate.md)).

**Run v2 (+ Europe PMC, FDA Potential Signals, OnSIDES):** no verdict flipped. 01 and 04 gained FDA Potential-Signal listings (NAION Q4 2024, Dysaesthesia Q1 2024) and foreign-label evidence. Europe PMC added 0 new on-topic papers. Cost per review unchanged or lower ([run v2](../12-features/ai-literature-review/samples/rerun-v2-multi-source.md)).

## Verdict
**Trying.** Promising as a second AI use case and as QA for the label check. Not proven: n = 6, hand-picked, Claude-judged. Next test: ~30 random ranked signals with a pharmacist answer key.

## Persona check
- 🩺 PV SME: The right split. Papers judge plausibility; DailyMed judges label status. Confounding by indication (sample 05) should become a rule, not an AI call.
- 💊 Safety Officer: Useful if it is short and cited. The "noise" verdicts save the most time.
- 🧐 Evaluator: A good story for "AI reliability", but only after a real eval. Until then, call it "AI review backed by papers; pharmacist sign-off open".
