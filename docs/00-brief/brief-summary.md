# The brief in plain language

Source: [Soragence-Technical-Build-Brief.pdf](Soragence-Technical-Build-Brief.pdf) (Soragence, Oct 2026)

## One sentence
Build a working app in **Palantir Foundry** that warns a hospital pharmacy safety officer about drug safety problems
(side effects missing from the label, and recalls) **before** she hears about them late from FDA emails or hallway talk.

## The user and her problem
- **Who:** a pharmacy safety officer at a health system. She watches a formulary (the hospital's list of approved drugs) of a few hundred drugs.
- **Pain today:** she learns about safety problems late and from scattered places.
- **What she wants each morning:**
  1. Which drugs have side effects being reported that **the label doesn't mention**?
  2. Which drugs have an **active recall**?
  3. **What changed since yesterday?**
- **Must-have:** she has to **trust** it. Every flag must link back to the source.

## What to build (4 parts)
| Part | What | Required? |
|---|---|---|
| **A. Pipelines** | 4+ sources (at least 1 unstructured) → raw → clean → **ontology** (Drug, Label, Adverse Event, Recall, Signal). At least 1 pipeline runs **incrementally**. | ✅ |
| **B. AI function** | An LLM reads drug labels and pulls out the listed side effects. Compare them with FAERS reports → flag reactions that are **frequent but not on the label**. | ✅ |
| **C. App** | Workshop app: ranked signal list, drug drill-down (label passage shown next to what the AI extracted), recall alerts, and a **triage button that writes back** to the ontology. | ✅ |
| **D. Monitoring** | Pipeline health (freshness, row counts, schema, build time) + AI health (hallucination check against a hand-labeled gold set; drift across label versions or model changes). | ⭐ Stretch |

**Scope rule:** one drug class **or** 50–200 drugs. Narrow and working beats broad and broken.

## Data (all public, free)
| Source | Gives you | Format |
|---|---|---|
| **FAERS** (FDA Adverse Event Reporting System) | Millions of side-effect reports by drug + reaction | JSON API, quarterly bulk files |
| **DailyMed** | Official drug labels + version history. *The unstructured source; the AI's input.* | PDF, SPL XML |
| **FDA enforcement reports** | Recalls: class, reason, product | JSON API, weekly |
| **RxNorm** | Standard drug IDs linking brand ↔ generic ↔ ingredient | REST API, bulk |
| **ClinicalTrials.gov** | Side effects seen in trials ("second opinion") | JSON API v2 |
| _Optional:_ PubMed, Medicare Part D spending, FDA Drug Safety Communications | Evidence, usage weighting, ground truth | Various |

⚠️ The brief warns: *the data is messier than its documentation says. Spotting and handling the mess is part of the test.*

## What you hand in
1. Working build in Foundry
2. One-page architecture note (diagram + 3–4 key decisions + what you didn't do)
3. Optimization log (measure → improve → before/after; include what didn't help)
4. 20-minute demo (as the safety officer first, then under the hood) + questions

## How it is judged
| Area | "Good" means |
|---|---|
| Architecture | Clear raw→ontology. **Drug identity resolved once, in the right place.** Another engineer could extend it without asking. |
| Optimization | Deliberate incremental vs full rebuild, partitioning, LLM not re-run needlessly. **Measured.** |
| Data judgment | Found the data problems, fixed the ones that matter, honest about the rest. |
| Application | Answers the 3 questions fast; every flag traces to source. |
| AI reliability | Can say how often extraction is wrong and how you know. (Stretch: notice if it gets worse.) |
| Communication | Plain trade-offs, incl. "what I'd do with another month". |

> "A partial build with clear reasoning is a better result than a complete one you cannot explain."

## Ground rules
- Foundry access sorted at kickoff · AI coding assistants allowed (you must be able to explain everything) · Public data only
- **Ask questions** ("what you ask tells us something") · **Where silent, decide and write it down** · **Cut breadth before depth**
- Timeline: **3 weeks from kickoff, part-time**
