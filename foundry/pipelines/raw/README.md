# foundry/pipelines/raw/ — bronze ingestion

One file per pull. Each file is a mirror of the same-named file in Foundry repo `Pipelines/pipelines_raw_ingest` (`transforms-python/src/myproject/datasets/`). Contract for every output: [dataset-contracts-v1.md §1](../../../docs/04-architecture/dataset-contracts-v1.md#1-raw-bronze-source-exactly-as-received-append-only).

| File | Source | Outputs | Pattern |
|---|---|---|---|
| [raw_openfda_enforcement.py](raw_openfda_enforcement.py) | `src_openfda_api` | `raw_openfda_enforcement` | `@transform_df`, paged openFDA search |
| [raw_openfda_products.py](raw_openfda_products.py) | `src_openfda_api` | `raw_openfda_drugsfda`, `raw_openfda_ndc` | two `@transform_df` sharing a `pull()` helper |
| [raw_dailymed_spl.py](raw_dailymed_spl.py) | `src_dailymed_api` | `raw_dailymed_spl_index`, `raw_dailymed_spl_xml` | `@transform` with two outputs |
| [raw_rxnorm.py](raw_rxnorm.py) | `src_rxnav_api` | `raw_rxnorm_lookup`, `raw_rxnorm_related` | `@transform` with two outputs |
| [raw_faers_quarters.py](raw_faers_quarters.py) | `src_faers_files` | `raw_faers_quarter_files` (files), `raw_faers_quarter_manifest` | `@transform`, streams ZIP to temp file, writes members via `filesystem()` |
| [raw_openfda_enforcement_access_test.py](raw_openfda_enforcement_access_test.py) | `src_openfda_api` | `raw_openfda_enforcement_access_test` | first access test (1 record); keep for history |

Rules every raw transform follows:
- Keep the original payload (JSON, XML or file) next to a few parsed columns.
- Save `request_params`, `http_status`, `retrieved_at` and the source's own "last updated" field.
- A non-200 reply becomes an **error row**, never a silent gap.
- Scope is the `INGREDIENTS` list at the top of each file: all 13 formulary ingredients since step 9 (D039 G1, D031 v5).
- Verify each build: row count = the source's own total (`meta.results.total`, `total_elements`, manifest bytes).

Open items: secret `OpenFdaApiKey` is still unused. The 13-drug pull needs about 50 openFDA requests, well under the no-key limit (1,000/day); add the key before daily refreshes or more drugs. Make DailyMed and FAERS incremental at build-order step 10.
