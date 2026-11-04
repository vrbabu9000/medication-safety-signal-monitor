# foundry/pipelines/ontology/ — gold: datasets that back Ontology objects

Mirror of [ontology_objects.py](ontology_objects.py). It lives in Foundry repo `Pipelines/pipelines_clean` (`transforms-python/src/myproject/datasets/ontology_objects.py`) and writes to `Data/curated`. Object and link types built on these datasets: [foundry/ontology](../../ontology/README.md).

| Transform | Outputs | Key |
|---|---|---|
| `compute_drugs` | `ontology_drug_drugs` (counts of products, recalls, FAERS cases after fold) | `ingredient_rxcui` |
| `compute_products` | `ontology_product_products` (+ reference label per product, LD1) · `ontology_link_drug_product` | `product_key` · `link_key` |
| `compute_labels` | `ontology_label_labels` (+ DailyMed URL, safety section list) · `ontology_link_product_label` | `label_key` · `link_key` |
| `compute_recalls` | `ontology_recall_recalls` · `ontology_link_recall_product` (high/medium matches) · `ontology_link_recall_drug` | `recall_number` · `link_key` |
| `compute_triage_seed` | `ontology_triage_decisions`: empty, the schema only; rows come from the Action | `decision_id` |

Run locally: `.venv/bin/python foundry/tools/local_run/run_local.py foundry/pipelines/ontology/ontology_objects.py` (after the clean transforms).
