# foundry/pipelines/clean/ — silver: checked, typed, one meaning per row

Mirrors of Foundry repo `Pipelines/pipelines_clean` (`transforms-python/src/myproject/datasets/`). Outputs go to `Data/clean`. Contract: [dataset-contracts-v1.md §2](../../../docs/04-architecture/dataset-contracts-v1.md#2-clean-silver-checked-typed-deduplicated-one-meaning-per-row).

Clean transforms read **raw datasets only**: no external sources, no web calls. They are written with **polars** (`@transform.using`, lightweight), so they also run on your machine with [tools/local_run](../../tools/local_run/README.md).

| File | Outputs | Key | Rule |
|---|---|---|---|
| [clean_drug_identity.py](clean_drug_identity.py) | `clean_drug_ingredients` | `ingredient_rxcui` | D018 formulary (13), `in_slice` = pulled today (all 13 since step 9) |
| | `clean_drug_identity` | `lookup_string` | D020: exact RxNorm IN/PIN name, then salt strip; never substring; unmatched kept |
| | `clean_drug_product_map` | `ingredient_rxcui` + `product_key` | D039 G2: product = application number; combination flag |
| | `clean_drug_package_map` | `package_ndc11` | 11-digit NDC (4-4-2/5-3-2/5-4-1 padded); no application number → `labeler:<product_ndc>` (D-R6) |
| [clean_label_product_map.py](clean_label_product_map.py) | `clean_label_product_map` | `setid` + `spl_version` + `application_number` | Approval ids parsed from SPL XML; reference label = owner's label (LD1, D039 G3); no approval id → kept with a reason |

| [clean_faers.py](clean_faers.py) | `clean_faers_cases_current` | `caseid` | D022: per quarter, upsert by caseid (max caseversion, newer quarter wins ties), then that quarter's deletes; D023 fold flagged as `dup_suppressed` |
| | `clean_faers_case_reactions` | `caseid` + `pt` | All current cases (PRR background) |
| | `clean_faers_drug_reaction` | `caseid` + `ingredient_rxcui` + `pt` | D021: PS + SS + I, each ingredient once per case; `prod_ai` parts resolved through `clean_drug_identity` (exact, then salt strip; blank `prod_ai` → whole `drugname`) |
| [clean_labels.py](clean_labels.py) | `clean_label_versions` | `setid` + `spl_version` | Index + XML; effective date from the XML; PLR flag |
| | `clean_label_sections` | `setid` + `spl_version` + `section_code` | 6 safety LOINC codes (D037 list); first safety section on each branch, sub-sections folded in |
| [clean_recalls.py](clean_recalls.py) | `clean_recalls_current` | `recall_number` | Latest pull wins; status checked against {Ongoing, Completed, Terminated} |
| | `clean_recall_product_match` | `recall_number` + `match_target` + `match_key` | NDCs from the record's own text (D037 learning); ingredient row for every recall; unmatched kept with a reason |

FAERS locally: link the unzipped quarters first, `ln -sfn "$PWD/prototypes/data/_faers_bulk" foundry/tools/local_run/out/raw_faers_quarter_files`.

Checks: `python foundry/tools/local_run/check_identity.py` (key uniqueness, match counts, OxyContin chain T13).
