# Foundry access results — 2026-11-04

**Stage:** Define → Prototype · Build-order [step 1](../04-architecture/foundry-conventions/project-build-order-v1.md) (access) and step 2 (folders, part).
**How:** user logged in to Foundry (`kestrel.usw-16.palantirfoundry.com`, Developer Tier) in Chrome; Claude drove the browser through Claude in Chrome. Security settings were clicked by the user.

## Result

| Capability | Status | Evidence |
|---|---|---|
| Project `Medication Safety Signal Monitor` | ✅ Owner | Was empty before this session |
| Tools in New menu (Pipeline Builder, Code repository, Data source, Object type, Action type, Workshop module, AIP Logic) | ✅ Present | New menu, project root |
| AIP model answers | ✅ | `AIP/Logic/scratch_aip_access_test` preview run: prompt "Reply with exactly: AIP OK" → `AIP OK`, 2.9 s, GPT-5.6 Sol (default). Listed: Claude Opus 4.8, Claude Sonnet 4.6, Gemini 3.5 Flash, Gemini 3.1 Flash Lite, Gemini 3 Flash (Preview), GPT-5.6 Luna, GPT-5.4 mini, Grok 4.5 |
| Outbound internet to openFDA | ✅ | Egress policy `api.fda.gov (Port 443)`, direct connection, **Approved** (self-approved by user) |
| openFDA call from a build | ✅ | Dataset `Data/raw/raw_openfda_enforcement_access_test`: 1 row, `http_status` 200, `meta.results.total` = 11 oxycodone recalls, record D-0338-2026 (Oxycodone HCl 5 mg tablets, Class II, Ongoing, American Health Packaging, card-seal defect), openFDA `last_updated` 2026-10-28 |
| Action submit / persist | ❓ Not tested | Needs an object type first (build-order step 6) |

## Resources created

| Resource | Path | Notes |
|---|---|---|
| Folders | `Data/{raw,clean,curated,quarantine}`, `Pipelines`, `Ontology/{Objects,Links,Actions}`, `Workshop`, `AIP/{Logic,Evals}`, `Monitoring`, `Analysis`, `Documentation`, `Scratch` | Per [conventions §3](../04-architecture/foundry-conventions/conventions-v1.md#3-foundry-folders-and-local-repository-folders) |
| AIP Logic `scratch_aip_access_test` | `AIP/Logic` | Not published; test only |
| Source `src_openfda_api` (API name `OpenFdaApi`) | `Data/raw` | REST API, `https://api.fda.gov`, no auth, no secrets yet. Exports off. Code import: code repositories **on**; compute modules and pipeline UDFs **off** |
| Code Repository `pipelines_raw_ingest` | `Pipelines` | Python Transforms template; `transforms-external-systems` 0.1399.0 added; source imported |
| Transform `raw_openfda_enforcement_access_test.py` | repo `datasets/` | Mirror: [foundry/pipelines/raw/](../../foundry/pipelines/raw/raw_openfda_enforcement_access_test.py) |
| Dataset `raw_openfda_enforcement_access_test` | `Data/raw` | Columns: `retrieved_at_utc`, `request_url`, `http_status`, `response_json` |

## Issues met (and what we did)

| Issue | Fix / status |
|---|---|
| Self-approve click first did not save | User clicked again in Claude's tab; policy then attached |
| Source page still said "Pending approval" | Control Panel policy page showed **Approved**; stale view |
| REST API source has no batch sync | Ingest through code (external transform) — D038 |
| `transforms-external-systems` missing in new repo | Installed from External systems panel |
| Lock-file merge conflict (VS Code workspace had committed) | Kept our side (adds `transforms-external-systems`, `retrying`); checks passed |
| `request_url` saved without the query string | Open: store request params in their own column in real pipelines |

## Timing (rough, wall clock)

| Step | Time |
|---|---|
| Folder layout (17 folders) | ~4 min |
| AIP test | ~2 min |
| Source + egress (incl. 2 approval attempts) | ~10 min |
| Repo creation, library install, conflict, source import | ~15 min |
| First build (checks + queue + Spark start + run) | ~4 min |

## Not covered
Action persistence · openFDA key secret · DailyMed, RxNorm and FAERS bulk ingestion methods · incremental behaviour.
