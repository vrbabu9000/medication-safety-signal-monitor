# A004 — FAERS → ontology mapping, explained as "two lists"

| | |
|---|---|
| **Date** | 2026-10-20 |
| **Design-thinking stage** | Define → Prototype (on paper) |
| **Area** | Ontology / AI |
| **Status** | Trying |
| **Replaces** | none (makes the merge walkthrough concrete) |

## What changed
| Before | Now | Why |
|---|---|---|
| v1 explainer built on openFDA API samples (100 reports/drug) | **v2: real bulk quarters 2026 Q1+Q2 (819,683 reports) run through a plain-Python prototype of every stage** → [data-walkthrough-v1.html](../04-architecture/data-walkthrough-v1.html) · script [faers_bulk_walkthrough.py](../../prototypes/explore/faers_bulk_walkthrough.py) | You could not follow v1; the pipeline input (D004) is bulk files, which have a different shape (no openfda block) |
| FAERS fields and Part B described in the abstract | One real report (14891719) and one real label (semaglutide v14) walked end to end | You asked for clearer, concrete examples |
| Ontology objects listed by name only | Each object has a "one object =" grain and a real example | Grain decides what we count and link |

## The idea in 3 lines
1. List 1 = FAERS counts per drug × reaction × quarter (AdverseEventStat). Plain code.
2. List 2 = side effects on the label, extracted by the LLM with a quote each (LabeledReaction). This is Part B.
3. Compare on Drug + MedDRA term → Signal. Individual FAERS reports stay as dataset rows, not objects (proposal).

## How we tested it
On paper with local samples: report explode/filter, label keyword checks for 20 top FAERS reactions.

## Result
1 report → 8 rows → 2 kept. Found 3 traps a plain text search gets wrong ("blurred vision", "gastroparesis", US/UK spelling). New issue DQ33 (wrong reference label for semaglutide).

## Result v2 (measured)
Append vs upsert +8.7% phantom rows · substring identity +50% false morphine rows · 7 mass-duplicate patients, oxycodone −24% · reporter field blank 35% → 72% · semaglutide NAION 394 reports, PRR 112, absent from tablet and injection labels. DQ34–DQ41, D020–D025 (proposed).

## Verdict
Keep as the working model. Revisit the "report is not an object" choice when building the drill-down.

## Diagram
[16-faers-to-signal-v1.png](../diagrams/png/16-faers-to-signal-v1.png) · [PDF](../diagrams/pdf/16-faers-to-signal-v1.pdf) · full explainer: [faers-and-part-b-explained-v1.md](../04-architecture/faers-and-part-b-explained-v1.md)

## Persona check
- 🩺 PV SME: count suspect only; "Impaired gastric emptying" and "Visual impairment" need a rule, not just a match.
- 💊 Safety Officer: the compare table (section 4C) is the screen I want.
- 🧐 Evaluator: shows why an LLM is needed, not just used. Good for the demo.
