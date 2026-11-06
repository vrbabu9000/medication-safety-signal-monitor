# Independent annotation comparison

{
  "created_at_utc": "2026-11-01T20:10:59.378216+00:00",
  "shared_pack_sha256": "2652cbbe5a08210cc9268b956401f21fd169a05c3647035ac7b83caf345be481",
  "codex_file_sha256": "f22e804bd532e16b97f382c4f3cba8e7172096606d8a6b2f4b2b8a8a9ed2a8ce",
  "claude_file_sha256": "d33088a1dce3d6825da82e1e6099a7d53f45c292c510c8c33d6ee6e8a6216965",
  "case_count": 30,
  "exact_agreements": 29,
  "disagreements": [
    "G26"
  ],
  "interpretation": "Agreement only; not gold-standard accuracy. Independently check evidence, even where answers agree."
}

| ID | Category | Codex | Claude | Exact agreement | Human verdict |
|---|---|---|---|---|---|
| G01 | DailyMed | "reaction_or_warning" | "reaction_or_warning" | True | pending |
| G02 | DailyMed | "reaction_or_warning" | "reaction_or_warning" | True | pending |
| G03 | DailyMed | "underlying_condition_or_risk_factor" | "underlying_condition_or_risk_factor" | True | pending |
| G04 | DailyMed | "symptom_of_other_condition" | "symptom_of_other_condition" | True | pending |
| G05 | DailyMed | "administration_instruction" | "administration_instruction" | True | pending |
| G06 | DailyMed | "reaction_or_warning" | "reaction_or_warning" | True | pending |
| G07 | DailyMed | "exposure_factor" | "exposure_factor" | True | pending |
| G08 | DailyMed | "reaction_or_warning" | "reaction_or_warning" | True | pending |
| G09 | DailyMed | "contraindicated_population" | "contraindicated_population" | True | pending |
| G10 | DailyMed | "co_medication_risk_factor" | "co_medication_risk_factor" | True | pending |
| G11 | DailyMed | "reaction_or_warning" | "reaction_or_warning" | True | pending |
| G12 | DailyMed | "reaction_or_warning" | "reaction_or_warning" | True | pending |
| G13 | RxNorm | "7804" | "7804" | True | pending |
| G14 | RxNorm | "7052" | "7052" | True | pending |
| G15 | RxNorm | false | false | True | pending |
| G16 | RxNorm | [{"rxcui": "161", "name": "acetaminophen"}, {"rxcui": "7804", "name": "oxycodone"}] | [{"rxcui": "161", "name": "acetaminophen"}, {"rxcui": "7804", "name": "oxycodone"}] | True | pending |
| G17 | FAERS | "2026-07-30" | "2026-07-30" | True | pending |
| G18 | FAERS | {"term": "DRUG INEFFECTIVE", "count": 1299274} | {"term": "DRUG INEFFECTIVE", "count": 1299274} | True | pending |
| G19 | FAERS | false | false | True | pending |
| G20 | FAERS | false | false | True | pending |
| G21 | FDA enforcement | "Defective container: card seal defects (weak/non-existent seals), leading to the tablets falling out of their cavities." | "Defective container: card seal defects (weak/non-existent seals), leading to the tablets falling out of their cavities." | True | pending |
| G22 | FDA enforcement | "Ongoing" | "Ongoing" | True | pending |
| G23 | FDA enforcement | "unknown" | "unknown" | True | pending |
| G24 | FDA enforcement | "unknown" | "unknown" | True | pending |
| G25 | Drugs@FDA | "KNOA PHARMA" | "KNOA PHARMA" | True | pending |
| G26 | Drugs@FDA | {"brand_name": "OXYCONTIN", "dosage_form": "TABLET, EXTENDED RELEASE", "route": "ORAL", "active_ingredients": [{"name": "OXYCODONE HYDROCHLORIDE", "strength": "10MG"}]} | {"product_number": "001", "brand_name": "OXYCONTIN", "dosage_form": "TABLET, EXTENDED RELEASE", "route": "ORAL", "active_ingredients": [{"name": "OXYCODONE HYDROCHLORIDE", "strength": "10MG"}]} | False | pending |
| G27 | NDC Directory | "100 TABLET, FILM COATED, EXTENDED RELEASE in 1 BOTTLE (59011-410-10)" | "100 TABLET, FILM COATED, EXTENDED RELEASE in 1 BOTTLE (59011-410-10)" | True | pending |
| G28 | NDC Directory | false | false | True | pending |
| G29 | SrLC | true | true | True | pending |
| G30 | ClinicalTrials.gov | {"group_id": "EG000", "group_title": "Extended Release Oxycodone", "seriousNumAffected": 0, "seriousNumAtRisk": 18} | {"group_id": "EG000", "group_title": "Extended Release Oxycodone", "seriousNumAffected": 0, "seriousNumAtRisk": 18} | True | pending |
