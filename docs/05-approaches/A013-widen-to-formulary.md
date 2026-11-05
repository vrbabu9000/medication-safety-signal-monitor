# A013 — Widen the working path to the 13-drug formulary (step 9)

| | |
|---|---|
| **Date** | 2026-11-04 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Pipelines / Ontology / Scope |
| **Status** | Kept (step 9 gate passed) |
| **Replaces** | the oxycodone slice (A010–A012 ran on 1 drug) |

## What changed
| Before | Now | Why |
|---|---|---|
| Raw pulls for oxycodone only (`INGREDIENTS = ["oxycodone"]`) | All 13 D018 ingredients in the 4 API pulls; `in_slice` true for all 13 | D039 G1: restore 13 once the slice works (it did, steps 6–8). Recorded as D031 v5 |
| Clean labels trusted any HTTP 200 | Clean keeps only replies that start with `<` | DailyMed sent the text "None" with HTTP 200 for 2 tramadol labels (DQ42) |
| AI extraction | Unchanged: still the 2 pilot labels | D041: widen AI only after the pharmacist gold-set check. The text label check covers all 13 drugs |

## The idea in 3 lines
1. Change one list per raw file; everything downstream is already drug-agnostic (checked by searching the code for one-drug assumptions).
2. Build in dependency order: raw → identity → labels / FAERS / recalls → ontology objects → AI (cache) → signals.
3. Reconcile every layer against the source totals and against the oxycodone results we already trust.

## How we tested it
Foundry SQL on each dataset, per drug.

## Result
| Check | Result |
|---|---|
| Raw vs source totals (recalls, Drugs@FDA, NDC, DailyMed), per drug | All 13 equal; 0 error rows. DailyMed 1,321 labels, 0 version mismatches |
| openFDA requests | ~50 for 13 drugs, no API key needed (limit 1,000/day without key) |
| FAERS | 373,522 drug-reaction rows. Oxycodone unchanged (4,464 → 3,408 cases); semaglutide 21,034 = Oct 20 walkthrough |
| Keys | 0 duplicates, 0 nulls in all 10 curated tables |
| Oxycodone signals | Unchanged: 271 signals, 125 ranked, 80 caution; Myoclonus `evaluation_id` unchanged, so the step 8 decision still points at a live signal |
| All drugs | 14,921 statistics → 2,047 signals for 12 drugs, 1,355 ranked. Exenatide: 20 cases, no reference label → nothing shown as "not in label" (D039 G4) |
| AI cache at scale | 9/9 sections from cache, **0 model calls** (O1 holds) |
| Ontology | Re-indexed without changes to types: Signal ≈2K, AE Stat ≈15K, Label 1.3K, Recall 900 objects |
| Wall time | Raw 4 builds in parallel (DailyMed 3 m 23 s, longest); clean + ontology + signals ~5 min of builds |

## Verdict
**Keep.** The path widened with one bug, found and fixed (DQ42), and every count reconciled. Two weaknesses grow with scope and are now the main risk:
- **Synonyms.** Semaglutide's top-ranked "not in label" item is "Impaired gastric emptying"; the label says "delayed gastric emptying". A label ↔ FAERS synonym table is needed.
- **Efficacy terms ranked as clinical.** "Weight loss poor", "Hunger", "Increased appetite" and "Food craving" sit near the top for GLP-1s. D016 needs an efficacy update for GLP-1 terms (a new version, so it needs your OK).

There is also one real lead: "Optic ischaemic neuropathy" (NAION) is ranked 3rd for semaglutide (a = 394). This matches DQ41 and the public safety discussion.

## Diagram (if structure changed)
No structural change; same graph, more rows.

## Persona check
- 🩺 PV SME: GLP-1 reports are dominated by efficacy and product-use terms. Without MedDRA groupings the keyword buckets will keep leaking. The synonym table is the higher-value fix.
- 💊 Safety Officer: The ranked list now mixes 12 drugs, so she needs a drug filter on the screen.
- 🧐 Evaluator: Strong reconciliation evidence. The claim "1,355 ranked signals" must not be presented as 1,355 findings; it is a review queue.

## Follow-up (2026-11-05): D016 v3 buckets
The A013 verdict named efficacy terms ranked as clinical. After the synonym table (A014), the ranked list still led with GLP-1 efficacy and product complaints, so D016 v3 (accepted 2026-11-05) widens the buckets. Measured locally, then in Foundry (identical):

| | Before (syn_v1) | After (D016 v3) |
|---|---|---|
| Signals | 1,959 | 1,959 (tagged, not removed) |
| Ranked | 1,210 | **1,115** (−95, −7.9%) |
| Moved out of the ranked queue | — | 95: first pass product use 44 · efficacy 26 · administrative 12 · social 6 · abuse 3; then 4 more from "hyperphagia" and "corrective lens user" |
| Semaglutide NAION rank | #2 | **#1** |

Evaluation ids did not change (buckets are not part of the hash), so existing decisions stay linked. Next candidate for synonym table v2: "Gastrointestinal hypomotility" (now 2nd for semaglutide), which matches the labels' "delays gastric emptying".
