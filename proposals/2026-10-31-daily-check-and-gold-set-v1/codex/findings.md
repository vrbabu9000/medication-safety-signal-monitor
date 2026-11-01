# Codex candidate answers — 30 cases

**Status:** source-anchored candidate reference set. Every human review is pending. No Claude answers were read.

**Coverage:** eight source families; 12 bounded interpretation cases from three opioid labels. Remaining cases test data facts and justified abstention. Do not combine these into a clinical AI accuracy score.

**FAERS limitation:** drug-filtered queries returned HTTP 403/API_KEY_MISSING. G17–G19 use a successful unfiltered aggregate, never an oxycodone-specific count. G20 tests documented interpretation. Failure responses are preserved.

| ID | Source | Question / target | Candidate answer | Evidence |
|---|---|---|---|---|
| G01 | DailyMed | In the specified passage only, classify respiratory depression. | "reaction_or_warning" | {"supporting_quote": "respiratory depression"} |
| G02 | DailyMed | In the specified passage only, classify opioid-induced esophageal dysfunction. | "reaction_or_warning" | {"supporting_quote": "opioid-induced esophageal dysfunction"} |
| G03 | DailyMed | In the specified passage only, classify esophageal cancer. | "underlying_condition_or_risk_factor" | {"supporting_quote": "esophageal cancer"} |
| G04 | DailyMed | In the specified passage only, classify nausea. | "symptom_of_other_condition" | {"supporting_quote": "Presentation of adrenal insufficiency"} |
| G05 | DailyMed | In the specified passage only, classify the direction not to pre-soak, lick or wet tablets. | "administration_instruction" | {"supporting_quote": "Instruct patients not to pre-soak"} |
| G06 | DailyMed | In the specified passage only, classify opioid-induced hyperalgesia. | "reaction_or_warning" | {"supporting_quote": "Opioid-Induced Hyperalgesia"} |
| G07 | DailyMed | In the specified passage only, classify external heat exposure. | "exposure_factor" | {"supporting_quote": "Exposure to heat"} |
| G08 | DailyMed | In the specified passage only, classify respiratory depression. | "reaction_or_warning" | {"supporting_quote": "respiratory depression"} |
| G09 | DailyMed | In the specified passage only, classify patients who are not opioid-tolerant. | "contraindicated_population" | {"supporting_quote": "patients who are not opioid-tolerant"} |
| G10 | DailyMed | In the specified passage only, classify the listed serotonergic drugs. | "co_medication_risk_factor" | {"supporting_quote": "serotonergic drugs"} |
| G11 | DailyMed | In the specified passage only, classify serotonin syndrome. | "reaction_or_warning" | {"supporting_quote": "serotonin syndrome"} |
| G12 | DailyMed | In the specified passage only, classify seizures. | "reaction_or_warning" | {"supporting_quote": "Seizures have been reported"} |
| G13 | RxNorm | What ingredient RxCUI does the captured exact-name request for oxycodone return? | "7804" | {"source_value": "7804"} |
| G14 | RxNorm | What ingredient RxCUI does the captured exact-name request for morphine return? | "7052" | {"source_value": "7052"} |
| G15 | RxNorm | Do the captured apomorphine and morphine requests return the same RxCUI? | false | {"apomorphine_rxcui": "1043", "morphine_rxcui": "7052"} |
| G16 | RxNorm | Which ingredient names and RxCUIs are returned for the captured Percocet brand relationship lookup? | [{"rxcui": "161", "name": "acetaminophen"}, {"rxcui": "7804", "name": "oxycodone"}] | {"source_value": [{"rxcui": "161", "name": "acetaminophen"}, {"rxcui": "7804", "name": "oxycodone"}]} |
| G17 | FAERS | What last_updated date does the captured unfiltered FAERS aggregate response report? | "2026-07-30" | {"source_value": "2026-07-30"} |
| G18 | FAERS | What term and count are returned by the captured unfiltered, limit=1 reaction-count request? | {"term": "DRUG INEFFECTIVE", "count": 1299274} | {"source_value": {"term": "DRUG INEFFECTIVE", "count": 1299274}} |
| G19 | FAERS | Does this unfiltered aggregate establish an oxycodone-specific count for the returned term? | false | {"scope": "Unfiltered; no search parameter"} |
| G20 | FAERS | Does a reported adverse-event count alone establish causation or an incidence rate? | false | {"supporting_quote": "cannot be used to estimate the incidence of these events"} |
| G21 | FDA enforcement | What reason_for_recall is recorded for D-0338-2026? | "Defective container: card seal defects (weak/non-existent seals), leading to the tablets falling out of their cavities." | {"source_value": "Defective container: card seal defects (weak/non-existent seals), leading to the tablets falling out of their cavities."} |
| G22 | FDA enforcement | What status is reported in the captured record D-0338-2026? | "Ongoing" | {"source_value": "Ongoing"} |
| G23 | FDA enforcement | Can current active recall status be established from the captured reported status alone? Answer yes/no/unknown for current active status. | "unknown" | {"reported_status": "Ongoing", "supporting_quote": "FDA does not update the status of a recall after the recall has been classified"} |
| G24 | FDA enforcement | With no hospital inventory or lot records supplied, is hospital exposure to D-0338-2026 established? Answer yes/no/unknown. | "unknown" | {"lot_codes": "Lots #: 1027932, Exp Date 06/30/2027, 1028360, Exp Date 08/31/2027"} |
| G25 | Drugs@FDA | What sponsor_name does the captured Drugs@FDA record for NDA022272 give? | "KNOA PHARMA" | {"source_value": "KNOA PHARMA"} |
| G26 | Drugs@FDA | For NDA022272 product_number 001, return brand, dosage form, route and active ingredient/strength. | {"brand_name": "OXYCONTIN", "dosage_form": "TABLET, EXTENDED RELEASE", "route": "ORAL", "active_ingredients": [{"name": "OXYCODONE HYDROCHLORIDE", "strength": "10MG"}]} | {"source_value": {"brand_name": "OXYCONTIN", "dosage_form": "TABLET, EXTENDED RELEASE", "route": "ORAL", "active_ingredients": [{"name": "OXYCODONE HYDROCHLORIDE", "strength": "10MG"}]}} |
| G27 | NDC Directory | What package description is recorded for package_ndc 59011-410-10? | "100 TABLET, FILM COATED, EXTENDED RELEASE in 1 BOTTLE (59011-410-10)" | {"source_value": "100 TABLET, FILM COATED, EXTENDED RELEASE in 1 BOTTLE (59011-410-10)"} |
| G28 | NDC Directory | Is carton NDC 68084-354-01 named in recall D-0338-2026 the same package as the selected OxyContin package 59011-410-10? | false | {"recall_carton_ndc": "68084-354-01", "selected_package_ndc": "59011-410-10"} |
| G29 | SrLC | Does the OXYCONTIN NDA-022272 entry dated 12/22/2025 (SUPPL-52), section 5.13, include opioid-induced esophageal dysfunction? | true | {"supporting_quote": "Cases of opioid-induced esophageal dysfunction (OIED)"} |
| G30 | ClinicalTrials.gov | For NCT01162304 adverse-event group EG000, what serious-adverse-event affected and at-risk counts are reported? Preserve the group title. | {"group_id": "EG000", "group_title": "Extended Release Oxycodone", "seriousNumAffected": 0, "seriousNumAtRisk": 18} | {"source_value": {"group_id": "EG000", "group_title": "Extended Release Oxycodone", "seriousNumAffected": 0, "seriousNumAtRisk": 18}, "study_status": "TERMINATED"} |

## Human adjudication checklist

Check the original source, label/product/version, bounded passage context, query or trial arm, and the exact answer. Mark approve/correct/uncertain. Keep uncertainty; do not force agreement.

A correct unknown is not missing work. Source-dependent counts may change live, so score the frozen evidence first and record source drift separately.

## What this set cannot establish

- Sensitivity/recall over all adverse reactions in full labels. Only selected terms/passages are tested.
- Accuracy for every drug class, route, table format or clinical question.
- Drug causation, adverse-event incidence, current active recall status or hospital lot exposure.
- Foundry/AIP runtime, cost, optimization or production validation; no Foundry execution occurred here.

## Freeze and comparison

Codex output is now fixed. Give Claude only CLAUDE-PROMPT.md and shared/. After Claude freezes its answers, compare IDs, answers, source locators and abstentions. Human review settles disagreements; agreement alone does not make gold.
