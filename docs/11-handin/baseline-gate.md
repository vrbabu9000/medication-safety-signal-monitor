# Baseline gate (Phase B) — 2026-11-05

**Result: PASS.** Every check below was run on 2026-11-05 after the step 11 build. Numbers are frozen in [numbers.json](numbers.json) (single source for reports, deck, demo and diagrams).

| Check | Pass when | Result |
|---|---|---|
| 3 questions on one screen | each answered from the app | ✅ Morning brief: 1,073 ranked signals · 126 active recalls · 26 changes in 30 days, plus as-of per source; detail pages 1–3 ([screens](screens/)) |
| Rebuild | downstream chain rebuilt; counts unchanged; decisions survive | ✅ DailyMed pull (with XML reuse) → clean_labels → clean_label_product_map → ontology_objects → ai_label_extraction (9/9 from cache, 0 model calls) → ontology_signals → ontology_changes → monitoring. All counts equal the pre-gate values; the change feed found **0** build-to-build changes (correct: same data); the 2 triage decisions are still there |
| Trace | 5 random flags traced to source rows and label text by hand | ✅ 5/5 (table below) |
| Numbers | numbers.json from Foundry SQL | ✅ captured 07:50 UTC (query below) |
| Screenshots | every demo screen captured | ✅ app pages 0–3, Ontology Manager, Object Explorer (signal links), dataset preview; more under-the-hood shots taken during the demo-path work |
| Monitoring | checks pass or warn for a known reason | ✅ 21 checks: 19 pass, 1 warn (FAERS reporter type blank 72%, DQ38 — real), drift warn on recalls ×3.3 (real) |
| Rubric | Evaluator scores each "What we will look at" row | Run as the 🧐 evaluator agent at the start of Phase C → [rubric-check.md](reviews/rubric-check.md) |

## Trace: 5 random ranked signals (seed 20261105) re-derived from source rows
Count `a` = distinct current FAERS cases (not duplicate-suppressed, fewer than 30 drugs) where the drug is a suspect and the reaction is reported. Label check = is the exact reaction term in any safety section of the drug's reference labels (the synonym table and spelling variants are the pipeline's extra steps; none applied here). Local data, which equals Foundry (A014).

| # | Signal | a in signal | a recounted from FAERS rows | Example case ids | Reference labels searched | Term found in their safety sections? |
|---|---|---|---|---|---|---|
| 1 | Morphine · Symmetrical drug-related intertriginous and flexural exanthema | 4 | 4 | 24540774, 24545788, 24557293 | 19 labels, 76 sections | no |
| 2 | Fentanyl · Post procedural haemorrhage | 11 | 11 | 16863183, 18794884, 18858356 | 6 labels, 24 sections | no |
| 3 | Methadone · Mydriasis | 8 | 8 | 25956893, 26027773, 26382147 | 23 labels, 96 sections | no |
| 4 | Morphine · Hepatic cytolysis | 9 | 9 | 15464104, 20141240, 23754954 | 19 labels, 76 sections | no |
| 5 | Morphine · Greater trochanteric pain syndrome | 3 | 3 | 23830555, 25610636, 26759731 | 19 labels, 76 sections | no |

How to open one in Foundry: Object Explorer → search the signal name → Links → MSSM AE Stat (the 2×2 counts) and MSSM Drug → MSSM Products → Reference Label → DailyMed link. Case ids can be checked in `clean_faers_drug_reaction` with SQL.

## Numbers query (Foundry repo SQL panel)
One `UNION ALL` query of `(key, value)` pairs over `ontology_signal_signals`, `ontology_ae_stats`, `clean_faers_*`, `ontology_recall_recalls`, `ontology_label_labels`, `ontology_change_events`, `ai_label_section_extractions` and the latest run of `monitoring_checks`. Saved as text: [baseline-gate-query.sql](baseline-gate-query.sql).
