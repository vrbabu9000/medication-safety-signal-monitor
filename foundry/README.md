# foundry/

Mirrors of the code that runs in Palantir Foundry, plus the map of what exists there. **Foundry is the runtime; this folder is the reviewed record.** When a file here changes, the same change must be pasted into the Foundry Code Repository, committed there, and built (see [How a change reaches Foundry](#how-a-change-reaches-foundry)).

Reference: [Foundry conventions](../docs/04-architecture/foundry-conventions/README.md) · [12-step build order](../docs/04-architecture/foundry-conventions/project-build-order-v1.md) · [dataset contracts](../docs/04-architecture/dataset-contracts-v1.md). Layers: `raw` = bronze, `clean` = silver (incl. shared identity), `pipelines/ontology` = gold object-backing datasets.

| Folder | Holds | Brief part | Status |
|---|---|---|---|
| `pipelines/raw/` | Ingestion transforms (one file per pull) | A | ✅ 6 files, [README](pipelines/raw/README.md) |
| `pipelines/clean/` | Cleaning, dedup, **shared drug identity** (resolved once) | A | ✅ identity (step 4) + FAERS, labels, recalls (step 5), [README](pipelines/clean/README.md) |
| `pipelines/ontology/` | Datasets that back Ontology objects | A | ✅ step 6 + 8, [ontology_objects.py](pipelines/ontology/ontology_objects.py), [ontology_signals.py](pipelines/ontology/ontology_signals.py) (run in repo `pipelines_clean`) |
| `ontology/` | Object types, links, Actions (definitions + notes) | A, C | ✅ [README](ontology/README.md) |
| `ai-function/` | Label-extraction prompts, AIP Logic notes, grounding check | B | superseded by `pipelines/ai/` |
| `pipelines/ai/` | AI label extraction transform (Claude Sonnet 5.5, cached, grounded) | B | ✅ pilot step 7, [README](pipelines/ai/README.md) |
| `app/` | Workshop layout notes and screenshots | C | 🟡 module **MSSM Safety Officer** built (step 8); notes in [ontology README](ontology/README.md#workshop-module) |
| `monitoring/` | Data expectations, health checks, drift checks | D | ⚪ |
| `tools/local_run/` | Run a transform on your machine with stand-ins for Foundry's library | — | ✅ [README](tools/local_run/README.md) |

Naming: `<layer>_<source>_<thing>`, e.g. `clean_faers_cases_current`.

## Foundry resource map

Project: `/kestrel-01f4ab/Medication Safety Signal Monitor` (Developer Tier). Folders: `AIP/{Logic,Evals}`, `Analysis`, `Data/{raw,clean,curated,quarantine}`, `Documentation`, `Monitoring`, `Ontology/{Objects,Links,Actions}`, `Pipelines`, `Scratch`, `Workshop`.

### Sources (all in `Data/raw`, REST API type, no auth unless noted)

| Source | API name | Host (egress policy, self-approved) | RID | Secrets |
|---|---|---|---|---|
| `src_openfda_api` | `OpenFdaApi` | api.fda.gov:443 | `ri.magritte..source.e46a0898-be14-401d-92d1-f9c20afa7f94` | `OpenFdaApiKey` (added 2026-11-04, **not yet used in code**) |
| `src_dailymed_api` | `DailyMedApi` | dailymed.nlm.nih.gov:443 | `ri.magritte..source.cce69842-52cc-4201-9053-7519dfed6613` | — |
| `src_rxnav_api` | `RxNavApi` | rxnav.nlm.nih.gov:443 | `ri.magritte..source.79ca01f9-95d0-43c6-8e28-cc9681a2ed5f` | — |
| `src_faers_files` | `FaersFiles` | fis.fda.gov:443 | `ri.magritte..source.dc0c031f-19db-470e-8e7b-df48be315e04` | — |

Every source: exports **off**; "import into code repositories" **on**; compute modules and pipeline UDFs **off** (D038, least privilege).

### Code repositories

| Repo | Path | RID | Holds |
|---|---|---|---|
| `pipelines_raw_ingest` | `Pipelines/` | `ri.stemma.main.repository.5c896743-fd13-41bf-a44f-30df020df319` | Python transforms; library `transforms-external-systems` 0.1399.0; all 4 sources imported. Files under `transforms-python/src/myproject/datasets/` |
| `pipelines_clean` | `Pipelines/` | `ri.stemma.main.repository.a93194bd-2c3a-452d-bc8d-da642ae64be0` | Python lightweight (polars) transforms; dataset inputs only, no sources |

### Raw datasets built

All in `Data/raw`, full snapshot each build, **13-drug formulary since step 9** (2026-11-04; was the oxycodone slice). "Check" = the count we compared against the source, per drug in Foundry SQL.

| Dataset | Rows | Check | RID |
|---|---|---|---|
| `raw_openfda_enforcement` | 930 (900 distinct recalls) | = openFDA total for each of 13 drugs; 0 error rows | `ri.foundry.main.dataset.467890f6-bd3a-4088-b3ce-b6645498e65d` |
| `raw_openfda_drugsfda` | 663 | = openFDA total for each of 13 drugs; 0 error rows | `ri.foundry.main.dataset.23a81f16-a77e-40ad-bb1b-4548bf5ded23` |
| `raw_openfda_ndc` | 1,824 | = openFDA total for each of 13 drugs; 0 error rows | `ri.foundry.main.dataset.8c02f006-233d-4d81-a6a8-f5e432cecb37` |
| `raw_dailymed_spl_index` | 1,321 setids | = DailyMed total for each of 13 drugs | `ri.foundry.main.dataset.3c7c4178-33b8-4061-bdcd-a8f600ecb26c` |
| `raw_dailymed_spl_xml` | 1,321 | 0 HTTP errors, 0 version mismatches; **2 replies are the text "None" with HTTP 200** (tramadol repackager labels, DQ42) | `ri.foundry.main.dataset.72097730-4717-4853-a711-4be8e27efb13` |
| `raw_rxnorm_lookup` | 13 ingredients + 1 salt string | widened at step 9; not re-counted row by row | (see `Data/raw`) |
| `raw_rxnorm_related` | (13 ingredients) | widened at step 9; identity result checked downstream (39 lookup strings) | (see `Data/raw`) |
| `raw_faers_quarter_files` | 37 files | files dataset (not a table) | `ri.foundry.main.dataset.de0e0c09-28ee-480c-9296-e96f127f9532` |
| `raw_faers_quarter_manifest` | 37 | Q1 352,984,542 B / Q2 337,724,653 B; sha256 = local copies | `ri.foundry.main.dataset.539ccd4c-55b3-48cc-924e-baf55d5da0ce` |
| `raw_openfda_enforcement_access_test` | 1 | access test only; can be deleted later | `ri.foundry.main.dataset.b1b1999d-7d65-4010-b2ff-28449a50cf1e` |

### Clean datasets built (`Data/clean`, step 4, 2026-11-04)

Checked in Foundry SQL: **0 duplicate keys in each**; the OxyContin chain (7804 → NDA022272 → 59011-410-10 → label `bfdfe235…` v44 reference) returns 1 row.

| Dataset | Rows | Key | RID |
|---|---|---|---|
| `clean_drug_ingredients` | 13 | `ingredient_rxcui` | `ri.foundry.main.dataset.13768528-5de2-41f7-8847-640f721b15fc` |
| `clean_drug_identity` | 39 (step 9) | `lookup_string` | `ri.foundry.main.dataset.fb64198f-7b8b-4c95-a26b-580a347071fa` |
| `clean_drug_product_map` | 658 (step 9) | `ingredient_rxcui` + `product_key` | `ri.foundry.main.dataset.39544a6a-e39a-40ef-8da4-012f7322723b` |
| `clean_drug_package_map` | 4,293 (step 9) | `package_ndc11` | `ri.foundry.main.dataset.7a29f351-8847-47ac-b7e8-22c21d9a6a69` |
| `clean_label_product_map` | 1,386 (step 9) | `setid` + `spl_version` + `application_number` | `ri.foundry.main.dataset.9f37f742-13b7-4f79-bdc3-4d08f0527f40` |

### Clean baseline built (`Data/clean`, step 5, 2026-11-04)

Checked in Foundry SQL: **0 duplicate keys in each**; every count equals the local run, and the FAERS counts equal the Oct 20 prototype.

| Dataset | Rows | Key | RID |
|---|---|---|---|
| `clean_faers_cases_current` | 792,346 (1,530 `dup_suppressed`) | `caseid` | `ri.foundry.main.dataset.cf4d8b32-006e-42ab-8a4b-8b02b5a9fe56` |
| `clean_faers_case_reactions` | 2,554,017 | `caseid` + `pt` | `ri.foundry.main.dataset.e2bbab66-b5ce-4a85-a5b4-e095731da488` |
| `clean_faers_drug_reaction` | 373,522 for 13 drugs (step 9; oxycodone unchanged 4,464 → 3,408 cases; semaglutide 21,034 = Oct 20 walkthrough) | `caseid` + `ingredient_rxcui` + `pt` | `ri.foundry.main.dataset.ee3b0d07-4751-4402-80db-2c6d9b3d8667` |
| `clean_label_versions` | 1,321 (2 without usable XML, DQ42) | `setid` + `spl_version` | `ri.foundry.main.dataset.e87ac84a-8b77-4c8f-938d-9e0d3559c1ce` |
| `clean_label_sections` | 5,431 | `setid` + `spl_version` + `section_code` | `ri.foundry.main.dataset.11d2cc25-d4c8-4f24-b5de-0ac4cdfddd22` |
| `clean_recalls_current` | 900 (126 ongoing) | `recall_number` | `ri.foundry.main.dataset.3f5dce51-9412-4892-85b5-436e97f64e15` |
| `clean_recall_product_match` | 1,933 | `recall_number` + `match_target` + `match_key` | `ri.foundry.main.dataset.4144615f-e80b-491f-ae26-b4a8d2023f6d` |

### Curated datasets built (`Data/curated`, step 6, 2026-11-04)

They back the Ontology ([foundry/ontology](ontology/README.md)). Built by [ontology_objects.py](pipelines/ontology/ontology_objects.py) in repo `pipelines_clean`. Keys: 0 null, 0 duplicate (checked locally; object counts in Foundry equal the rows).

| Dataset | Rows | Key | RID |
|---|---|---|---|
| `ontology_drug_drugs` | 13 | `ingredient_rxcui` | `ri.foundry.main.dataset.5f757c65-2871-4287-a626-36cb105085a6` |
| `ontology_product_products` | 658 (182 with a reference label) | `product_key` | `ri.foundry.main.dataset.33f79c11-4199-4b6b-9b5e-89c413921bba` |
| `ontology_label_labels` | 1,321 | `label_key` | `ri.foundry.main.dataset.42a0f5f1-c37f-4b45-ae0d-a6cdf40410da` |
| `ontology_recall_recalls` | 900 | `recall_number` | `ri.foundry.main.dataset.c13cd5e7-ec0a-4497-8aa3-9f1663908080` |
| `ontology_link_drug_product` | 658 | `link_key` | `ri.foundry.main.dataset.8d1377f5-954c-49e7-abf8-8e5a053c27ef` |
| `ontology_link_product_label` | 1,293 | `link_key` | `ri.foundry.main.dataset.4db5d0d7-e786-461b-b664-429b4a92d3b7` |
| `ontology_link_recall_product` | 85 | `link_key` | `ri.foundry.main.dataset.53604667-d496-47cd-9fb1-033ede3b6f84` |
| `ontology_link_recall_drug` | 930 | `link_key` | `ri.foundry.main.dataset.a49f8d73-8f31-43e2-b1bd-027b769a2d25` |
| `ontology_triage_decisions` | 0 in the dataset; 2 decisions live as Action edits | `decision_id` | `ri.foundry.main.dataset.88c5b012-c746-47ea-b6fd-230c18d7da70` |
| `ai_label_section_extractions` | 9 (pilot, step 7) | `cache_key` | `ri.foundry.main.dataset.48f642bc-e242-429d-ae71-f93cb5400b02` |
| `ontology_labeled_reactions` | 448 (prompt p2; all quotes grounded) | `labeled_reaction_key` | `ri.foundry.main.dataset.407104e1-6078-4eb9-b2b5-d02933261cbf` |
| `ontology_ae_stats` | 14,921 for 13 drugs (label check `text+ai_v1+syn_v1` since A014) | `stat_key` | `ri.foundry.main.dataset.1c1d39d3-c423-471c-9822-52c2a7db1093` |
| `ontology_signal_signals` | 1,959, 1,115 ranked (D016 v3), 72 possibly in label (A014; was 2,047 / 1,355 at step 9) | `signal_key` | `ri.foundry.main.dataset.1ece78d5-f17c-4b18-96cd-2b7ae43dafd7` |
| `ontology_label_synonyms` | 233 (syn_v1: high, medium, rejected) | `faers_pt` + `label_phrase` | (see `Data/curated`) |

## How a change reaches Foundry

1. Edit the mirror file here and test it with [tools/local_run](tools/local_run/README.md).
2. In Foundry, open the code repository → `transforms-python/src/myproject/datasets/` → open or create the file with the **same name**.
3. Replace its contents with the mirror file **minus** the two `# Mirror of …` comment lines. **Paste**; don't type. The editor's auto-indent breaks typed Python.
4. Click **Commit** (Foundry's own git, not GitHub), then **Build**.
5. Check the result on the **dataset page → SQL console**. The repo's SQL panel is slow. Compare row counts against the source total.
6. Record counts in [ACTIVITY-LOG](../ACTIVITY-LOG.md) and this README.

Gotchas we hit (full list: [DECISIONS learnings](../docs/06-decisions/DECISIONS.md)):
- openFDA OR searches need parentheses, or the first term is silently dropped.
- openFDA `openfda.*` fields are sparse. Always also search the source's own ingredient field.
- A source shows "Pending approval" after self-approval. Check the Control Panel policy page instead.
- Importing a source into a repo can show an error yet succeed. Reload before retrying.
- Use one editor per branch. A new repo opens a VS Code workspace that auto-commits ("Sync remote branch") for ~30 min, which conflicts with Code Repositories edits. Commit right after each paste. If a commit is rejected ("sync first"), reload and check the file still exists before building.
- An Action's form preview in Ontology Manager is a **test run only**. Apply real edits from Object Explorer → Actions. A new object type needs ~1 min of indexing first.
- An AIP model must be imported into the project before a transform can use it: type its RID inline inside the model Input call, pick it, click Import.
- The repo's Build button skips an unchanged incremental transform even after upstream rebuilds; use the dataset page Build and check History.
- A dataset that hasn't changed won't rebuild: use Build ▾ → **Force**.
- Raw transforms take **no Foundry dataset inputs**. A transform that uses an external source together with dataset inputs needs source exports enabled, which we keep off. Clean transforms read raw datasets and use **no** external source.
