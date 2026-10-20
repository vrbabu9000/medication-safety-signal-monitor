# foundry/

Code and configs that will live in Palantir Foundry. Empty until access is set up (see COMPASS blockers).

| Folder | Will hold | Brief part |
|---|---|---|
| `pipelines/raw/` | Ingestion transforms (FAERS, DailyMed, Enforcement, RxNorm, CT.gov) | A |
| `pipelines/clean/` | Cleaning, dedup, **drug_identity** (resolved once) | A |
| `pipelines/ontology/` | Datasets that back ontology objects | A |
| `ontology/` | Object types, links and Actions (exported definitions + notes) | A, C |
| `ai-function/` | Label-extraction prompts, AIP Logic notes, grounding check | B |
| `app/` | Workshop app layout notes and screenshots | C |
| `monitoring/` | Data expectations, health checks, drift checks | D |

Naming: `<layer>_<source>_<thing>`, e.g. `clean_faers_cases_dedup`.
Local experiments before Foundry access go in `/prototypes`, not here.
