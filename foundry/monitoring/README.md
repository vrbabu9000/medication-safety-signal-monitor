# foundry/monitoring/ — health checks configured in Foundry

Foundry Data Health checks are set in the UI (dataset → **Health** tab → **Add checks**), so this file is their written record. The computed checks and drift series live in [foundry/pipelines/monitoring](../pipelines/monitoring/README.md). Decision D046, approach [A017](../../docs/05-approaches/A017-monitoring-and-health-checks.md).

| Dataset | Check | Rule | Why (note saved with the check) |
|---|---|---|---|
| `Data/curated/ontology_signal_signals` | Build status | most recent build succeeded | Signals feed question 1; a failed build means the ranked list is stale |
| `Data/curated/ontology_signal_signals` | Primary key | `signal_key` 100% unique and non-null | A duplicate would double-count a signal on the screen |
| `Data/clean/clean_faers_cases_current` | Build status | most recent build succeeded | Full FAERS rebuild is the baseline for signals (D044) |
| `Data/clean/clean_faers_cases_current` | Primary key | `caseid` 100% unique and non-null | D022: one current version per case |

Added 2026-11-05. Each check subscribes the creator to failures (Foundry notification). Checks report after the next build of the dataset.

Same pattern to add next (not done yet): `ontology_recall_recalls` primary key `recall_number`; `raw_openfda_enforcement` *Time since last updated* ≤ 8 days; `raw_dailymed_spl_xml` *Build status*; `ai_label_section_extractions` *Build status*. Production would add schedules (daily raw pulls, quarterly FAERS) so freshness checks have something to watch.
