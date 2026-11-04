# A009 — openFDA ingestion via REST API source + Python external transform

| | |
|---|---|
| **Date** | 2026-11-04 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Pipelines |
| **Status** | Kept |
| **Replaces** | none (manual file upload stays the fallback) |

## What changed
| Before | Now | Why |
|---|---|---|
| No proven path from openFDA into Foundry; plan assumed manual upload of downloaded files (B1) | REST API source `src_openfda_api` + self-approved egress policy + Python external transform writes the raw reply to `Data/raw` | A real build pulled a live recall (HTTP 200). Repeatable, schedulable, and every row keeps its retrieval time |

## The idea in 3 lines
1. One Data Connection source per external host, least privilege: no exports, code-repository import only.
2. A Python transform (`@external_systems` + `@transform_df`) calls the endpoint and stores the raw JSON text, the HTTP status and the retrieval time.
3. Parsing happens later in `clean`; raw stays untouched for traceability ("every flag traces back to its source").

## How we tested it
One 1-record query, `drug/enforcement.json?search=openfda.generic_name:"oxycodone"&limit=1`, built once from `Pipelines/pipelines_raw_ingest`. We checked the output dataset in the build preview.

## Result
1 row · HTTP 200 · `meta.results.total` = 11 · record D-0338-2026 (oxycodone HCl 5 mg, Class II, Ongoing). Build ~4 min end to end (mostly queue and Spark start). Details: [access results](../10-delivery/2026-11-04-foundry-access-results.md).

## Verdict
**Keep** for openFDA endpoints (enforcement, labels, NDC, Drugs@FDA). Before bulk pulls: add the key as source secret `OpenFdaApiKey`, paginate (`skip`/`limit` ≤ 1000), store request params in their own column, and consider a lightweight (non-Spark) transform to cut start-up time. Still open: DailyMed SPL ZIPs, RxNorm and FAERS quarterly ZIPs (separate hosts, so new sources and egress policies).

## Diagram (if structure changed)
No new structure. Fits the raw layer of [18-foundry-medallion-v1](../diagrams/png/18-foundry-medallion-v1.png) ([PDF](../diagrams/pdf/18-foundry-medallion-v1.pdf)).

## Persona check
- 🩺 PV SME: Raw JSON kept whole, so recall class, status and `product_description` stay available. The "active recall" rule (lot expiry) is applied later in `clean`.
- 💊 Safety Officer: The source link and retrieval time travel with every row, which is what she needs to trust a flag.
- 🧐 Evaluator: One record proves the path works, not scale. Scale claims need measured pagination runs.
- 🛡️ Compliance: Public data only, no PHI. Exports off. The key will be held as an encrypted source secret and never written in code.
