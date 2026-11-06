# Screenshots (captured 2026-11-05, after the baseline gate)

| File | What it shows | How to reach it live |
|---|---|---|
| app-0-morning-brief.jpg | Morning brief: 1,073 · 126 · 26 + data as-of table | Workshop "MSSM Safety Officer" → tab Morning brief |
| app-1-not-in-label-naion.jpg | Ranked signals, NAION (semaglutide) #1 selected, evidence panel | tab 1 · Not in label |
| app-1b-triage-action-form.jpg | Create MSSM Triage Decision form, locked subject + evaluation id (cancelled, nothing saved) | tab 1 → Triage this signal |
| app-2-recalls.jpg | Recalls newest first, D-0040-2027 detail | tab 2 · Recalls |
| app-3-what-changed.jpg | Change feed with filters (drug, date, type, change) | tab 3 · What changed |
| hood-data-lineage-signals.jpg | Data Lineage: sources → raw → clean → curated → ontology_signal_signals | dataset ontology_signal_signals → Explore pipeline → Explore data lineage → expand parents 3 levels |
| hood-dataset-signals-preview.jpg | Dataset preview, backing object MSSM Signal, Data Health summary | Data/curated/ontology_signal_signals |
| hood-data-health-signals.jpg | Data Health: Build status + Primary key, both passed | same dataset → Health tab |
| hood-ontology-manager-signal.jpg | Ontology Manager: MSSM Signal, 1,952 objects, 25 properties | Ontology Manager → MSSM Signal |
| hood-object-explorer-naion-links.jpg | Object Explorer search, NAION signal links (AE Stat, Drug) | Object Explorer → search signal name → Links |
| hood-code-repo-ontology-signals.jpg | Code repo pipelines_clean, ontology_signals.py, file tree | Pipelines/pipelines_clean |
| hood-ai-extractions-cache-sql.jpg | AI extraction rows: 9 sections, n_reactions = n_grounded, from_cache true, tokens | repo SQL panel on ai_label_section_extractions |
| hood-monitoring-checks-sql.jpg | Latest monitoring checks (warn: reporter type blank; AI checks pass) | repo SQL panel on Data/monitoring/monitoring_checks |
| app-1c-labels-searched-naion.jpg | NAION evidence + the 3 reference labels searched (Ozempic v20, Wegovy v19, oral Ozempic v14) with DailyMed links | tab 1 → select signal → panel "Reference labels searched" |
| app-3b-what-changed-past-month.jpg | Page 3 with the "Past month" preset (Oct 6 – Nov 5): 26 events = 15 label versions + 11 recalls, same as Morning brief card 3 | tab 3 → Start date → Past month |
| hood-code-ai-label-extraction.jpg | ai_label_extraction.py: MODEL_ID claude-sonnet-5.5, PROMPT_VERSION p2, PARSER x1, PILOT_SETIDS, CACHEABLE | pipelines_clean → ai_label_extraction.py |
| hood-labeled-reactions-quotes-sql.jpg | AI output rows: term, assertion type, grounding = exact, the quote | repo SQL on ontology_labeled_reactions |
| hood-monitoring-drift-sql.png | Drift replay: reporter type blank ×2.1 (warn), recalls ×3.33 (warn), others pass, kind = historical_replay | repo SQL on monitoring_drift |
| hood-faers-inc-log-sql.png | Incremental FAERS log: 2026q1 397,224 cases; 2026q2 replaced 26,681, deleted 655 → 792,346 | repo SQL on clean_faers_inc_log |
Note (2026-11-05 later): app-0-morning-brief.jpg was re-captured after the source-status fix — 'We pulled it at' now filled (FAERS: quarterly file; RxNorm/openFDA/DailyMed: pull time).
