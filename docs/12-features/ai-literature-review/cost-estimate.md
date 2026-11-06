# F01 — Cost estimate (approximate)

**Bottom line:** the computer cost is pennies per review. **The real cost is pharmacist minutes.** The watch list exists to cap human time, not dollars.

## 1. What one review costs
Measured on the 6 samples ([FINDINGS](FINDINGS.md)), using [fetch_evidence.py](../../../tools/lit_review/fetch_evidence.py):

| Step | Measured | Cost |
|---|---|---|
| PubMed search + summaries + abstracts | **3 API calls, ~2 s** per signal | Free (NCBI E-utilities; 3 calls/s, or 10/s with a free key) |
| Abstract text sent to the model (≤ 8 abstracts) | 0.4k–6.0k tokens, **mean ~3.5k** | — |
| Model input (instructions ~1.5k + signal card ~0.5k + label excerpt ~1k + abstracts) | **~6.5k tokens** (worst ~11k) | estimate |
| Model output (verdict + one-pager ~1.2k + thinking ~2k) | **~3k tokens** (worst ~4k) | estimate |

Price per review (Anthropic list prices; token counts are **estimates**, not from a real model call):

| Model | $ / 1M in · out | Typical review | Worst case | With Batch API (−50%) |
|---|---|---|---|---|
| Claude Opus 5.5 | $4 · $20 | **~$0.09** | ~$0.12 | ~$0.045 |
| Claude Sonnet 5.5 | $2 · $10 | ~$0.04 | ~$0.06 | ~$0.02 |
| Claude Haiku 5.5 | $0.10 · $0.50 | ~$0.002 | ~$0.003 | ~$0.001 |

Recommendation: **Opus 5.5 for the review** (it's a judgement task, and the cost is trivial at this volume). Haiku could do the cheap pre-filter later, if volume grows.

## 2. Volume: how many reviews
| Scope | Reviews | Opus 5.5 | Sonnet 5.5 | Pharmacist sign-off (2 min each) |
|---|---|---|---|---|
| **Officer watch list (default): 5 drugs × top 5** | **25** | **~$2.20** | ~$1.10 | **~50 min** |
| Pilot, every drug: 12 drugs × top 12 | 144 | ~$12 | ~$6 | ~4.8 h |
| Every ranked clinical signal in the pilot | 1,073 | ~$92 | ~$46 | ~36 h |
| Scale idea: 500 drugs × top 10 | 5,000 | ~$430 | ~$215 | ~167 h |

(12 drugs, not 13: one pilot drug has no ranked clinical signal in this window.)

## 3. Running cost after the first pass
- A review is redone **only** when (a) a signal newly enters a drug's top K, (b) PubMed has a new paper since the last review (a date-filtered search: 1 free call, no model), or (c) the officer presses "Review again".
- Pilot watch list: guess **0–3 re-reviews a day → under $0.30/day** on Opus 5.5. A guess, not measured.
- **No papers → no model call.** If PubMed returns 0 hits, the review is written by code as "No literature found" ($0).

## 4. Assumptions and unknowns
| # | Assumption | Risk |
|---|---|---|
| 1 | Prices are Anthropic list prices. **Foundry AIP bills LLM use under Palantir's own terms**, so the Foundry cost may differ. | Medium: check AIP usage pricing |
| 2 | Token counts are estimated from measured abstract size. No model call was made. In the samples, Claude in this session did the review. | Low: re-measure on the first real run |
| 3 | Calling PubMed from Foundry needs a REST source with egress to `eutils.ncbi.nlm.nih.gov` (same pattern as openFDA, [A009](../../05-approaches/A009-openfda-rest-ingestion.md)) | Low |
| 4 | "2 minutes" of pharmacist time per review is a guess from reading one one-pager | Medium: time it with a real reviewer |
| 5 | Abstracts only. Full text would raise input ~5–10× (still under $1 a review) | Low |
