# foundry/pipelines/clean/ — silver: checked, typed, one meaning per row

Mirrors of Foundry repo `Pipelines/pipelines_clean` (`transforms-python/src/myproject/datasets/`). Outputs go to `Data/clean`. Contract: [dataset-contracts-v1.md §2](../../../docs/04-architecture/dataset-contracts-v1.md#2-clean-silver-checked-typed-deduplicated-one-meaning-per-row).

Clean transforms read **raw datasets only**: no external sources, no web calls. They are written with **polars** (`@transform.using`, lightweight), so they also run on your machine with [tools/local_run](../../tools/local_run/README.md).

| File | Outputs | Key | Rule |
|---|---|---|---|
| [clean_drug_identity.py](clean_drug_identity.py) | `clean_drug_ingredients` | `ingredient_rxcui` | D018 formulary (13), `in_slice` marks what is pulled today |
| | `clean_drug_identity` | `lookup_string` | D020: exact RxNorm IN/PIN name, then salt strip; never substring; unmatched kept |
| | `clean_drug_product_map` | `ingredient_rxcui` + `product_key` | D039 G2: product = application number; combination flag |
| | `clean_drug_package_map` | `package_ndc11` | 11-digit NDC (4-4-2/5-3-2/5-4-1 padded); no application number → `labeler:<product_ndc>` (D-R6) |
| [clean_label_product_map.py](clean_label_product_map.py) | `clean_label_product_map` | `setid` + `spl_version` + `application_number` | Approval ids parsed from SPL XML; reference label = owner's label (LD1, D039 G3); no approval id → kept with a reason |

Checks: `python foundry/tools/local_run/check_identity.py` (key uniqueness, match counts, OxyContin chain T13).
