# foundry/pipelines/ontology/ — gold: datasets that back Ontology objects

Mirrors of [ontology_objects.py](ontology_objects.py) (step 6), [ontology_signals.py](ontology_signals.py) (step 8) and [label_synonyms.py](label_synonyms.py) (A014: the reviewed synonym table, a plain Python list imported by the signals transform). It lives in Foundry repo `Pipelines/pipelines_clean` (`transforms-python/src/myproject/datasets/ontology_objects.py`) and writes to `Data/curated`. Object and link types built on these datasets: [foundry/ontology](../../ontology/README.md).

| Transform | Outputs | Key |
|---|---|---|
| `compute_drugs` | `ontology_drug_drugs` (counts of products, recalls, FAERS cases after fold) | `ingredient_rxcui` |
| `compute_products` | `ontology_product_products` (+ reference label per product, LD1) · `ontology_link_drug_product` | `product_key` · `link_key` |
| `compute_labels` | `ontology_label_labels` (+ DailyMed URL, safety section list) · `ontology_link_product_label` | `label_key` · `link_key` |
| `compute_recalls` | `ontology_recall_recalls` · `ontology_link_recall_product` (high/medium matches) · `ontology_link_recall_drug` | `recall_number` · `link_key` |
| `compute_triage_seed` | `ontology_triage_decisions`: empty, the schema only; rows come from the Action | `decision_id` |

| `ontology_signals.compute` (step 8; buckets D016 v3, [A012](../../../docs/05-approaches/A012-signal-statistics-and-workshop.md)) | `ontology_ae_stats`: per drug × reaction a/b/c/d, PRR, 95% CI, Yates χ², Evans flag (D006), label status + match evidence (D037 text + AI terms) · `ontology_signal_signals`: Evans **and** not in label, bucket (D016 v2), `is_ranked`, `rank_in_bucket`, caution, `evaluation_id` | `stat_key` · `signal_key` |

Label check `text+ai_v1+syn_v2`: (1) AI atomic term, (2) exact term or US spelling in a safety section (D037), (3) reviewed synonym phrase (D043): high → `in_label`, medium → `possibly_in_label` (signal kept, not ranked). The table is also written to `ontology_label_synonyms`.

Rule `prr_evans_v2`: reports with ≥30 drugs (`MAX_DRUG_ROWS`) are left out of the primary population and counted in `a_mass_reports` (D023 v2, accepted).

Run locally: `.venv/bin/python foundry/tools/local_run/run_local.py foundry/pipelines/ontology/ontology_objects.py` (after the clean transforms).
