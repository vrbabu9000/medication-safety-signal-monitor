# F01 — AI review backed by papers (feature folder)

| | |
|---|---|
| **Status** | Exploring. 6 samples done, re-run with 3 more sources (v2), nothing built in Foundry. Not in pilot scope ([A018](../../05-approaches/A018-ai-literature-review.md)) |
| **Stage** | Ideate → Prototype |
| **One line** | For the signals the officer watches, an AI reads PubMed and writes a short, cited verdict ("real / plausible / noise / not enough evidence"). A pharmacist agrees or disagrees in about 2 minutes. |

## Files here
| File | What it is |
|---|---|
| [FINDINGS.md](FINDINGS.md) | Summary of the 6 sample reviews: **start here** |
| [cost-estimate.md](cost-estimate.md) | Cost per review, per watch list, at scale |
| [sources-beyond-pubmed.md](sources-beyond-pubmed.md) | Public sources outside our 8 that could feed the review (best: Europe PMC, FDA Potential Signals, OnSIDES) |
| [samples/](samples/) | One-page reviews ([01 NAION](samples/01-semaglutide-naion.md), [02–06](samples/02-06-five-more-signals.md)) and the [run v2 with 3 more sources](samples/rerun-v2-multi-source.md) |
| [evidence/](evidence/) | Raw PubMed results and abstracts per sample (JSON + text) |
| [fetch_evidence.py](../../../tools/lit_review/fetch_evidence.py) | PubMed evidence fetcher (run v1) |
| [research_sources.py](../../../tools/lit_review/research_sources.py) | Europe PMC + FDA Potential Signals + OnSIDES (run v2) |

## Why (the officer's view)
💊 Today a ranked flag says "reported a lot, not in the label". It doesn't say whether anyone else has seen it. The review adds that context, with a paper behind every sentence. That keeps the trust rule: **every flag traces back to its source**, and now so does every opinion about the flag.

## How the watch list works (proposal)
1. **The officer picks the drugs** in Workshop (a `WatchList` write-back, like `TriageDecision`). Default: 5 drugs × top 5 = 25 signals.
2. **Per drug, take the top K** ranked signals in the clinical bucket with status `not_in_label`, in our existing rank order (`rank_in_bucket`). K defaults to 5; the officer can raise it (max 12).
3. **Pinned signals:** the officer can pin any single signal so it is always reviewed.
4. **When it runs:** a signal enters the top K · a new PubMed paper appears (weekly date-filtered search, free) · the officer presses "Review again". Daily cap: 50 reviews.
5. **Cheap gates before the model:** 0 PubMed hits → "No literature found" written by code ($0). The drug and the event must both appear in the abstract, or the paper is dropped. Retractions are dropped.

## What one review produces (a `LiteratureReview` object linked to the Signal)
| Field | Example |
|---|---|
| verdict | real concern · plausible (FAERS only) · likely noise · not reviewable · insufficient evidence |
| confidence | low / medium / high |
| reasons | 2–4 short sentences, **each citing a PMID** |
| cited_pmids | checked by code: each one was fetched, is not retracted, and mentions drug + event |
| suggested_action | e.g. "propose synonym Allodynia → dysesthesia (medium)" |
| model, prompt_version, run_date | for audit and drift checks (same pattern as A011) |
| pharmacist_verdict, note, signed_by, signed_at | write-back; empty until a human signs |

## Guardrails
- Never changes `label_status`. Label truth stays with DailyMed (D037). Synonym ideas go to the reviewed table (D043).
- The screen shows **"AI review: not a pharmacist opinion"** until signed.
- Public sources only (PubMed abstracts). No PHI.
- Grounding check in code: an uncited claim fails the review, the same as the A011 label extraction.

## How to market it
"AI that reads the literature for you, and shows its work." It's a second AI use case next to label extraction (A011). It is cheap (~$0.09 a review) and auditable (every sentence has a PMID), and it already found a real bug in our label check (sample 04).
