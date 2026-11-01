# Independent 30-case reference dataset — Claude prompt

Prepared using the read-only `claude-prompting` bridge skill. This prompt does not send anything to Claude. Run it in Claude Code after `shared/READY.json` exists. Give Claude the shared folder, not Codex's answers.

```text
Create an independent, evidence-backed candidate gold dataset for the Medication Safety Signal Monitor. This is a bounded data/evaluation task, not permission to rebuild the application or edit existing project files.

Project: /Users/vigneshrbabu/Documents/Git/medication-safety-signal-monitor
Task folder: /Users/vigneshrbabu/Documents/Git/medication-safety-signal-monitor/proposals/2026-10-31-daily-check-and-gold-set-v1
Your output folder: the task folder's claude/ subfolder only.

The product is a Palantir Foundry + AIP pilot for a hospital pharmacy safety officer. Her morning questions are: which drugs have reported reactions not mentioned in the selected label coverage, which recall records need attention, and what changed since the last review? Every flag must trace to evidence. The original brief requires at least four sources including unstructured documents, a real incremental pipeline, label-reading AI, an app with triage write-back, a one-page architecture note, measured optimization and a 20-minute demo. Monitoring became required in the recorded boss meeting. There is no clinically validated product yet.

The user wants your answers independently from Codex, followed by comparison. Shared cases and immutable evidence are allowed; shared expected answers are not. Do NOT read codex/, the task README if it summarizes answers, existing-files-changes.patch, old gold drafts, historical model annotations, or another model's answer files. Do not import an answer from an existing project document. Agreement between models does not establish truth. Your initial answers must be frozen before you inspect a later comparison.

Inputs:
- shared/READY.json confirms the common input pack is complete. If absent, stop: the capture is not ready.
- shared/cases.json contains exactly 30 fixed questions, case IDs, task categories, source references and any bounded passage instructions. It contains no expected answers.
- shared/source-manifest.json records actual source URLs, requests, retrieval timestamps, SHA-256 hashes, metadata and capture failures.
- shared/evidence/ contains the original public source responses and shared, deterministic text views. These files must not be changed.

Work from the frozen pack so you and Codex answer identical evidence despite changing live data. Verify the hashes before use. You may independently check the official live URLs; keep such freshness checks separate. If live data differs, report snapshot drift without silently changing the common-input answer.

Exactly 30 cases cover:
- 12 DailyMed passage/label interpretation cases, including positive evidence and context traps;
- 4 RxNorm identity cases, including combination products and look-alike names;
- 4 FAERS aggregate evidence cases, including exact query scope and interpretation;
- 4 FDA enforcement recall cases, including explicit unknown/current-status/applicability decisions;
- 2 Drugs@FDA product/application facts;
- 2 NDC Directory facts or interpretation checks;
- 1 Safety-related Labeling Changes database case;
- 1 ClinicalTrials.gov study-results case.

Do not invent a finding to fill a quota. A source-fetch failure is not a clinical negative. A missing field or inconclusive evidence gets status=unresolved, with a reason. An intentional answer of unknown can be a fully resolved case when the question asks what the evidence permits us to conclude. If the shared pack has fewer than 30 usable cases, report that; do not quietly replace cases.

For every case, independently produce:
case_id, category, question, answer (a JSON scalar/object as requested by the case), answer_status (resolved/unresolved), source_ids, evidence_locators (JSON Pointer, XML path or exact heading/paragraph), short supporting quotation or source value, source_sha256, source_effective_or_updated_at when actually supplied, retrieved_at_utc from the manifest, concise rationale, uncertainty, human_review_status=pending, and annotator=claude. Preserve source units, group IDs, denominators and qualifiers. A live lookup timestamp is not the source publication time.

Constraints:
- Public data only. No patient-level records, demographics, patient reconstruction, or proprietary data. FAERS inputs must be aggregate responses.
- RxNorm identifies medicines; it does not prove a product's safety or label applicability. Ingredient, brand, strength, formulation, route and package are distinct.
- DailyMed is company-submitted in-use labeling, not proof of the latest FDA-approved wording. Scope claims to the exact captured label version and passage. Distinguish reactions, symptoms of another condition, pre-existing risk factors, instructions and contraindications. A word appearing in a label is not enough to classify it as an adverse reaction. Absence outside a bounded passage is not proven by an empty extraction.
- FAERS counts are reports matching the saved query, not unique patients, incidence, causality, independently deduplicated counts, or guaranteed suspect-only evidence. Top-N absence is unknown, not zero. Do not add successive full snapshots together.
- FDA enforcement's reported status does not establish current recall lifecycle status. Product/lot matching is separate from ingredient matching. Without inventory evidence, hospital exposure is unknown.
- NDC listing is not FDA approval. Drugs@FDA application/product facts do not establish every label or package match automatically.
- SrLC is a regulatory labeling-change source with limited coverage; a dated entry does not mean all product labels changed then.
- ClinicalTrials.gov outcomes are specific to the captured study, arm, denominator and follow-up. Do not generalize a trial event rate into population risk.
- OnSIDES, if mentioned at all, is a model-derived optional benchmark, not independent clinical truth; do not substitute it for primary evidence or redistribute licensed terminology.
- Use only observed numbers. Do not manufacture source timestamps, hashes, update schedules, confidence percentages or clinical certainty.

Deliverables, only under claude/:
1. answers.jsonl — exactly one record for each of the 30 supplied case IDs, including unresolved rows.
2. findings.md — readable answer table, source coverage, context traps and limitations; distinguish source lookup checks from label interpretation checks.
3. validation.json — actual case count, unique IDs, hash verification result, unresolved count and per-category totals.
4. review-notes.md — disagreements you anticipate from ambiguous source meaning and the evidence needed for human adjudication; no reference to unseen Codex answers.

Also explain the morning workflow briefly: check source manifests/versions every day; process only actual changes; preserve the last complete successful data; publish no-change/freshness/failure states; keep unresolved reviews visible. Separate actual publisher cadence and any published release time/time zone from our proposed polling times. Say 'not published/not verified' when no exact clock time is established. Do not imply that a daily review requires daily FAERS updates, or claim this workflow is implemented.

Success checks: IDs match shared/cases.json exactly; no duplicate or invented cases; hashes agree; each resolved answer has a source locator and evidence; counts retain query/arm scope; unresolvable clinical/recall claims abstain; human approval remains pending. This mixed 30-case pack is a candidate system reference set, not an independently clinician-adjudicated gold standard and not a 30-item label-extraction benchmark. Do not report 'AI clinical accuracy' from all 30 items or call self-checking an independent human evaluation.

Do not run git/gh mutations, send messages, modify project settings, edit COMPASS or the activity log, or look at Codex's answers. Start by checking the shared pack. Finish with a short plain-language summary and links to your four output files. If required tools or sources are unavailable, state the exact gap and preserve unresolved records honestly.
```
