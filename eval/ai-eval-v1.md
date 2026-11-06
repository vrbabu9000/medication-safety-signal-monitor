# AI evaluation v1 — how often is the label extraction wrong, and how do we know? (step 11)

**Short answer.** On the 4 sections we can score against a frozen answer key, the extraction finds every reaction (recall 35/35) and adds 2 extra terms (precision 35/37), so **F1 = 0.97 against the D015 target of 0.85**. Across the whole pilot run, **448 of 448 quotes** are found word-for-word in the label text (no invented quotes). This is a small, Claude-reviewed check: the pharmacist review and the long sections are still to do.

## What was measured
| Measure | What it tells you | Result | Source |
|---|---|---|---|
| Grounding | Every extracted item carries a quote; code checks the quote is in the section text | **448 / 448** exact (run 2, all 9 sections) | Foundry `ai_label_section_extractions`; `monitoring_checks` `ai.grounded_rate` |
| Recall (strict, atomic terms) | Share of answer-key reactions the model found | **35 / 35 = 1.00** (prompt p1 was 11/35 = 0.31) | `check_gold.py --strict` on [run 2 terms](gold-set/runs/step7-run2-p2-short-sections.jsonl) |
| Precision (upper bound) | Share of extracted terms that are answer-key reactions | **35 / 37 = 0.95** if both extras count as errors | same |
| F1 | Balance of the two | **0.97** (target D015 ≥ 0.85) | computed |
| Cache / cost | Re-runs on unchanged text | 0 model calls, 0 tokens on rebuild (O1) | optimization log |

## Per section (answer key: [step7-pilot-gold-v1.json](gold-set/step7-pilot-gold-v1.json), frozen before the model ran)
| Label | Section | Recall | Extracted | Extra terms | Precision | F1 |
|---|---|---|---|---|---|---|
| OxyContin (`bfdfe235…`, v44) | Boxed Warning | 10/10 | 11 | "adverse drug effects" (too generic) | 0.91 | 0.95 |
| OxyContin | Contraindications | 6/6 | 6 | — | 1.00 | 1.00 |
| Oxycodone/APAP generic (`cc966d57…`, v19) | Boxed Warning | 13/13 | 14 | "liver transplant" (an outcome, arguably correct) | 0.93 | 0.96 |
| Oxycodone/APAP generic | Contraindications | 6/6 | 6 | — | 1.00 | 1.00 |

## What this does NOT show (said plainly)
- **Small and short.** 4 sections, 35 answer-key items, 2 labels. The long sections (Warnings and Precautions, Adverse Reactions: ~411 of 448 items) are not scored.
- **The answer key was written by Claude**, frozen before the model ran, but not yet checked by a pharmacist (D041; [another-month plan](../docs/09-roadmap/another-month-sources-and-pharmacist-review.md)).
- **Grounding ≠ correctness.** A quote can be real and still be the wrong item (e.g. a mechanism, not a reaction). Grounding catches invented text; the answer key catches wrong or missing items.
- **The AI does not change the signal list today.** Text matching already covers the AI's terms for the 2 pilot labels (A012). Its value now is the exact quote shown as evidence.

## How we would notice if it got worse (stretch goal)
1. Every build: `ai.grounded_rate` (fail < 0.95), `ai.section_errors`, `ai.cache_hit_rate` in `monitoring_checks` (A017).
2. Any change to model, prompt or parser changes the cache key, so every section is re-extracted and re-scored with `check_gold.py` before it is accepted.
3. With another month: a pharmacist-labelled stratified sample of long sections (e.g. 10 per section type), scored the same way each release; drift = F1 drop > 0.05 between releases.
