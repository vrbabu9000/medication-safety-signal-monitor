# A019 — Widen the AI label reading to the demo drug (D041 v2)

| | |
|---|---|
| **Date** | 2026-11-06 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | AI / App |
| **Status** | Kept |
| **Replaces** | none (extends A011 pilot, D041 → D041 v2) |

## What changed
| Before | Now | Why |
|---|---|---|
| The AI (Claude Sonnet 5.5 through AIP) read 2 oxycodone pilot labels, 9 sections. The hero signal (semaglutide × NAION) had **0** AI-read labels, and no AI quote was on the officer's screen | The AI also reads the **3 semaglutide reference labels** (Ozempic v20, Wegovy v19, oral Ozempic/Rybelsus v14): 21 sections. Page 1 has a new table, **"What the AI read in these labels"**, with every AI-extracted reaction and its word-for-word quote for the selected signal's drug (Workshop v0.10.0) | Evaluator v2's top hole: "the AI and the screen barely meet" ([rubric-check-v2](../11-handin/reviews/rubric-check-v2.md)). Semaglutide is the drug we demo |

## The idea in 3 lines
1. Add the 3 semaglutide setids to `PILOT_SETIDS`; nothing else in the code changes (same model, prompt p2, parser, cache key, grounding).
2. The cache means only the 12 new sections call the model; the 9 old ones are reused.
3. A Workshop variable walks Signal → Drug → Products → Reference Label → Labeled Reactions, and a table shows reaction · section · quote · label.

## How we tested it
Foundry SQL (repo SQL panel) on `ai_label_section_extractions`, `ontology_labeled_reactions`, `ontology_signal_signals`, `ontology_ae_stats`, `ontology_change_events`, `monitoring_checks`; then the screen in View mode with NAION selected; then a forced rebuild of the AI dataset to measure the cache.

## Result
| Measure | Before (v1 pilot) | After (D041 v2) |
|---|---|---|
| Labels / sections read by the AI | 2 / 9 | **5 / 21** |
| Extracted reactions, quote found word for word | 448 / 448 | **745 / 745** |
| Model calls in the widening build | — | **12** (9 sections from cache) · 44,869 prompt + 26,226 completion tokens |
| Model calls on a forced rebuild, text unchanged | 0 (9/9 cached) | **0 (21/21 cached)** |
| Signals · ranked · not in label · possibly in label | 1,952 · 1,073 · 1,844 · 108 | **unchanged** (change feed: 0 signal changes) |
| AE stats matched in the label first by an AI term | 8 (local run, older order) | **188** (131 oxycodone, 57 semaglutide); text 1,252, synonym high 163, medium 210 |
| NAION: labels also read by AI | 0 | **3**; still *not in label*, rank 1; evaluation id changed to `c4b5da0b64d1e1e6` |
| Optic-nerve or NAION terms the AI found in the 3 semaglutide labels | — | **0** (it did find diabetic-retinopathy terms) |

## Verdict
**Keep.** The AI now independently confirms the hero signal is not in the label, and the officer sees the AI's quotes on page 1. It still does **not** change the signal list (text matching already finds what the AI finds); its value is the quoted evidence. F1 0.97 is unchanged because the answer key covers only the oxycodone sections; the semaglutide sections are **not scored** (no answer key yet).

## Side effects (as the ripple table predicts)
- Every semaglutide signal's `evaluation_id` changed (274 signals; the AI-label count is hashed). No triage decision exists on a semaglutide signal, so nothing was left on an old id.
- The first version of the page-1 table took a fixed 260 px and squeezed the column so the **Triage this signal** button was cut off. Fix: *Enable scrolling* on the Evidence and triage section (published as v0.10.0).
- The repository Build button skipped the unchanged AI dataset ("already up to date"); the cache was measured with Build ▾ → Force on the dataset page.

## Persona check
- 🩺 PV SME: good that the AI found the retinopathy warning and nothing on optic neuropathy. That is the right negative. The long sections are still unscored.
- 💊 Safety Officer: now I can see what the label *does* say about the eyes, next to the signal. That makes "not in label" believable.
- 🧐 Evaluator: closes hole #1 in part (AI meets the screen); hole #2 (self-scored, no pharmacist) is still open.
