# Approaches index

Every approach we try gets a file here, including the ones we drop. New file = copy [_TEMPLATE.md](_TEMPLATE.md).

| ID | Name | Stage | Area | Status | Replaces | Date |
|---|---|---|---|---|---|---|
| [A000](A000-project-setup.md) | Project setup and working conventions | Empathize | Process | Kept | — | 2026-10-13 |
| [A001](A001-pilot-scope.md) | Pilot scope: opioids, monitoring-first, showcase of reasoning | Define | Scope | Trying | G1 (GLP-1 default) | 2026-10-13 |
| [A002](A002-source-profiling.md) | Source profiling: by hand, before building | Define | Data | Trying (Claude profiles done; your hand-check pending) | — | 2026-10-19 |
| [A003](A003-class-choice-hybrid.md) | Class choice: opioid-led hybrid (8 opioids + 5 GLP-1) | Define | Scope | **Kept** | A001 class (opioids only) | 2026-10-19 |
| [A004](A004-faers-to-ontology-mapping.md) | FAERS → ontology, every stage on real bulk data (v2: data walkthrough) | Define | Ontology / AI | Trying | — | 2026-10-20 |
| [A005](A005-source-selection-and-merge.md) | Source selection (+Drugs@FDA, NDC Directory, SrLC; OnSIDES benchmark) and two-level merge | Define | Pipelines / Ontology | Trying | D003 v1 | 2026-10-20 |
| [A007](A007-foundry-medallion-conventions.md) | Foundry medallion, ontology conventions and numbered build order | Define → Prototype | Pipelines / Ontology / Process | Kept (reference; deployment validation pending) | — (A006 reserved in non-adopted proposal) | 2026-10-31 |
| [A008](A008-gold-set-v2-cross-source-traces.md) | Reference set v2: 30 verified cross-source drug traces (8 sources each) | Prototype → Test | AI / Monitoring / Process | Kept (pharmacist review pending) | v1 30-case pack (superseded) | 2026-11-02 |
| [A009](A009-openfda-rest-ingestion.md) | openFDA ingestion via REST API source + Python external transform | Prototype → Test | Pipelines | Kept (1-record test passed) | — (manual upload = fallback) | 2026-11-04 |
| [A010](A010-first-ontology-path.md) | First Ontology path: Drug, Product, Label, Recall + TriageDecision write-back | Prototype → Test | Ontology | Kept (step 6 gate passed) | — | 2026-11-04 |
| [A011](A011-ai-label-extraction-pilot.md) | AI label extraction pilot: Claude Sonnet 5.5 in a cached, grounded transform; 2 labels / 9 sections | Prototype → Test | AI | Kept (pilot; prompt p2 before widening) | — | 2026-11-04 |
| [A012](A012-signal-statistics-and-workshop.md) | Signal statistics (PRR, Evans, mass-report cut) + first Workshop screen with triage write-back | Prototype → Test | Pipelines / Ontology / App | Kept (step 8 gate passed) | — | 2026-11-04 |
| [A013](A013-widen-to-formulary.md) | Widen the working path to the 13-drug formulary (step 9) | Prototype → Test | Pipelines / Ontology / Scope | Kept (all layers reconciled) | the oxycodone slice | 2026-11-04 |
| A00x | Monitoring design (incl. how to show 3–4 week drift in a 3-week project) | Ideate | Monitoring | _Later_ | — | — |
