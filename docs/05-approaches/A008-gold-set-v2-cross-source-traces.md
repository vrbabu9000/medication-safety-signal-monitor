# A008 — Reference set v2: 30 verified cross-source drug traces

| | |
|---|---|
| **Date** | 2026-11-02 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | AI / Monitoring / Process |
| **Status** | Kept (pharmacist review pending) |
| **Replaces** | The v1 30-case pack (`proposals/2026-10-31-daily-check-and-gold-set-v1/`), now superseded |

## What changed
| Before (v1) | Now (v2) | Why |
|---|---|---|
| One question per source; 12 opioid label passages | Each case follows one drug through all 8 sources (30 drugs × 8 steps = 240 answers) | To show how every source is used, and how the sources link to each other |
| Questions and expected answers written in the same pass (Codex) | Fixed question templates, frozen and hashed **before** answers; lookup answers derived by code; S4 label calls by Claude | Removes hint leakage and the case-setter-answers-own-question problem |
| FAERS oxycodone requests failed (HTTP 403) | Real cause: openFDA count queries with `limit>100` need a key. v2 uses the key, plus `limit=0` totals (no report records) | Fixes the gap; aggregate-only evidence |
| `srlc_oxy` file actually held the Ozempic page | Every capture has an **identity guard** (application no., brand, setId, NCT ID); a mismatch is rejected, never stored as evidence | Trust rule: every flag traces to the *right* source |
| No live check | `live_check.py` re-fetches every source and re-derives every answer; drift goes in a separate report | Frozen answers stay the reference; freshness is visible |
| Self-check only | Independent verifier (`verify_trace.py`, separate code) re-reads raw bytes: 3,403 checks | "Measured, not asserted" |

## The idea in 3 lines
1. Pick products that have usable evidence in **all 8 sources**: screen 62, keep 35 eligible, choose 30 across 21 classes (3 combination products).
2. For each product: capture → guard → freeze questions → derive answers → verify → case card.
3. A pharmacist reviews only the judgement steps (S4 label class, S6 "not in label" synonyms). The code proves everything else matches the source.

## How we tested it
- Automated: `verify_trace.py all`, 30 traces, every hash, value, quote and selection rule re-derived from the bytes.
- Pilot first (T01 Chantix), then 29 more. Pilot findings changed the template **before** scaling up (logged below).
- Live re-check after freeze (`drift-report.json`).

## Result
- 240/240 answers resolved; 0 unresolved; 0 deliberate "unknown" answers (recall status is reported *as reported*, not as current).
- 3,403/3,403 automated checks pass; 270 link checks evaluated.
- S4 classes: 7 reaction, 7 risk factor, 3 symptom of another condition, 3 instruction, 4 contraindicated population, 2 exposure, 4 co-medication.
- Findings worth demoing: FAERS product mixing (Chantix tablet vs varenicline nasal spray: 127 vs 527 reports); openFDA's harmonized package list ≠ recall scope (8 traces); **Lyrica label lag** (DailyMed SPL effective 2020-06-15 lacks a 04/25/2025 SrLC addition).

**What the pilot changed (template v1 → v2, before T02–T30):**
| Change | Trigger |
|---|---|
| FAERS: label comparison uses brand-named reports; substance total kept as contrast | Varenicline substance code mixed Chantix with Tyrvaya nasal spray |
| FAERS totals via `limit=0` (no records) | `limit=1` returns a report record |
| RxNorm: reverse check (ingredient → brand) | `related.json` body has `rxcui: null` |
| Recall match uses the record's own text, not `openfda.package_ndc` | Harmonized list covers the whole application |
| Trial search widened 10 → 25 studies, field-limited | Zoloft: no sertraline arm in top 10; 0.9 MB per capture |
| SrLC parser accepts headings with markup | Verifier caught Farxiga 06/03/2026 entry skipped |

## Verdict
**Keep** as the project's candidate reference set. Not a clinician-adjudicated gold standard and not a label-extraction benchmark: no "AI clinical accuracy" claim from it until the pharmacist review is done.

Note on scope: D031 v3 cut ClinicalTrials.gov from the **pilot build**. This set uses trials only as reference evidence; it does not put trials back into pilot scope.

## Diagram
📊 [20-gold-trace-v1.png](../diagrams/png/20-gold-trace-v1.png) · [PDF](../diagrams/pdf/20-gold-trace-v1.pdf) · _source: [20-gold-trace-v1.mmd](../diagrams/src/20-gold-trace-v1.mmd)_

## Where it lives
[proposals/2026-11-02-gold-set-v2/](../../proposals/2026-11-02-gold-set-v2/): `cards/` (30 one-page walkthroughs), `claude/answers.jsonl`, `claude/findings.md`, `claude/validation.json`, `claude/review-notes.md`, `drift-report.json`, `tools/`.

## Persona check
- 🩺 PV SME: string-matching a MedDRA term against label text misses synonyms (stroke vs CEREBROVASCULAR ACCIDENT); the "not in label" lists are review candidates, not signals. Litigation-shaped FAERS profiles (Truvada) need D016 tagging.
- 💊 Safety Officer: every card answers her three questions with a clickable source; "reported recall status" is clearly not today's status.
- 🧐 Evaluator: the 240 answers are verified against sources, but only 30 (S4) are judgement calls. Score AI extraction only on S4-type items, and only after review.
