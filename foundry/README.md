# foundry/

Mirrors of the code that runs in Palantir Foundry, plus the map of what exists there. **Foundry is the runtime; this folder is the reviewed record.** When a file here changes, the same change must be pasted into the Foundry Code Repository, committed there, and built (see [How a change reaches Foundry](#how-a-change-reaches-foundry)).

Reference: [Foundry conventions](../docs/04-architecture/foundry-conventions/README.md) · [12-step build order](../docs/04-architecture/foundry-conventions/project-build-order-v1.md) · [dataset contracts](../docs/04-architecture/dataset-contracts-v1.md). Layers: `raw` = bronze, `clean` = silver (incl. shared identity), `pipelines/ontology` = gold object-backing datasets.

| Folder | Holds | Brief part | Status |
|---|---|---|---|
| `pipelines/raw/` | Ingestion transforms (one file per pull) | A | ✅ 6 files, [README](pipelines/raw/README.md) |
| `pipelines/clean/` | Cleaning, dedup, **shared drug identity** (resolved once) | A | ⏭️ step 4 |
| `pipelines/ontology/` | Datasets that back Ontology objects | A | ⚪ |
| `ontology/` | Object types, links, Actions (definitions + notes) | A, C | ⚪ |
| `ai-function/` | Label-extraction prompts, AIP Logic notes, grounding check | B | ⚪ |
| `app/` | Workshop layout notes and screenshots | C | ⚪ |
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

### Raw datasets built

All in `Data/raw`, full snapshot each build, oxycodone slice (2026-11-04). "Check" = the count we compared against the source.

| Dataset | Rows | Check | RID |
|---|---|---|---|
| `raw_openfda_enforcement` | 25 | = openFDA total 25 | `ri.foundry.main.dataset.467890f6-bd3a-4088-b3ce-b6645498e65d` |
| `raw_openfda_drugsfda` | 141 | = openFDA total 141; OxyContin NDA022272 present | `ri.foundry.main.dataset.23a81f16-a77e-40ad-bb1b-4548bf5ded23` |
| `raw_openfda_ndc` | 313 | = openFDA total 313; 8 products under NDA022272 | `ri.foundry.main.dataset.8c02f006-233d-4d81-a6a8-f5e432cecb37` |
| `raw_dailymed_spl_index` | 263 | = DailyMed total 263 | `ri.foundry.main.dataset.3c7c4178-33b8-4061-bdcd-a8f600ecb26c` |
| `raw_dailymed_spl_xml` | 263 (14.2 MB) | 0 errors, 0 version mismatches; OxyContin `bfdfe235…` v44 = reference trace T13 | `ri.foundry.main.dataset.72097730-4717-4853-a711-4be8e27efb13` |
| `raw_rxnorm_lookup` | 2 | oxycodone → 7804; oxycodone hydrochloride → 82063 | (see `Data/raw`) |
| `raw_rxnorm_related` | 271 | = local run 271 (RxNorm 02-Nov-2026) | (see `Data/raw`) |
| `raw_faers_quarter_files` | 37 files | files dataset (not a table) | `ri.foundry.main.dataset.de0e0c09-28ee-480c-9296-e96f127f9532` |
| `raw_faers_quarter_manifest` | 37 | Q1 352,984,542 B / Q2 337,724,653 B; sha256 = local copies | `ri.foundry.main.dataset.539ccd4c-55b3-48cc-924e-baf55d5da0ce` |
| `raw_openfda_enforcement_access_test` | 1 | access test only; can be deleted later | `ri.foundry.main.dataset.b1b1999d-7d65-4010-b2ff-28449a50cf1e` |

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
- Use one editor per branch. Opening VS Code workspaces makes its own commit, which conflicts with the lock file.
- Raw transforms take **no Foundry dataset inputs**. A transform that uses an external source together with dataset inputs needs source exports enabled, which we keep off. Clean transforms read raw datasets and use **no** external source.
