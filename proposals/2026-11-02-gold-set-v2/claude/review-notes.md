# MSSM-30-v2 — review notes for the pharmacist and data reviewers

Every row is still `human_review_status = pending`. Code checks prove each answer **matches its source**. They can't prove the clinical **judgement** is right. That needs a person. This page lists where that judgement sits, roughly most important first.

**Who should review what**

| Reviewer | Steps | About |
|---|---|---|
| PV pharmacist (pharmacovigilance: drug-safety monitoring) | S4 (30 label calls), S6 "not in label" lists (30) | ~2 h |
| Pharmacy operations / inventory lead | S7 recall-to-package results (30) | ~30 min |
| Data engineer | S1–S3 identity chain, S5 selection, S8 arm choice | ~30 min, spot check |

## 1. Label calls most likely to be challenged (S4)

The 7 classes need written tie-break rules (§3). Until those exist, these are judgement calls, not errors:

| Trace | Target | My class | Plausible alternative | Why it's debatable |
|---|---|---|---|---|
| T08 Farxiga | abdominal pain | symptom_of_other_condition | reaction_or_warning | It's a sign of ketoacidosis, and ketoacidosis is itself drug-related |
| T20 Zithromax | vomiting or irritability with feeding | symptom_of_other_condition | reaction_or_warning | Signs of IHPS (infantile hypertrophic pyloric stenosis), which is the azithromycin-associated event |
| T21 Seroquel | muscle rigidity | symptom_of_other_condition | reaction_or_warning | A manifestation of NMS (neuroleptic malignant syndrome), which is the reaction |
| T23 Nexium | gastric malignancy | underlying_condition_or_risk_factor | (no class fits well) | A condition the drug may *mask*. The 7 classes have no "masked condition" option |
| T18 Zoloft | anatomically narrow angles | underlying_condition_or_risk_factor | contraindicated_population | The label says "avoid", not "contraindicated" |
| T06 Vytorin | decompensated cirrhosis | contraindicated_population | underlying_condition_or_risk_factor | A condition, but listed under CONTRAINDICATIONS |
| T07 Jardiance | elderly patients | underlying_condition_or_risk_factor | — | Low risk. Shown because loop diuretics sit in the same sentence |
| T02 Pradaxa, T24 Prilosec | P-gp inducers, St. John's Wort | co_medication_risk_factor | — | The risk is *loss of effect*, not a new reaction. Is that still a "risk factor"? |
| T13 OxyContin | neonatal opioid withdrawal syndrome | reaction_or_warning | — | The person affected is the newborn, not the patient taking the drug |
| T29 Truvada | unknown or positive HIV-1 status | contraindicated_population | — | Applies only to the PrEP (HIV prevention) use |

## 2. "Not in the label" lists (S6) need a synonym check

S6 says whether each of the top-10 FAERS terms appears **as a string** in the label's in-scope sections. That's a fact about text, not about meaning. Likely misses:

| Trace | FAERS term (MedDRA preferred term) | Probably covered in the label as… |
|---|---|---|
| T02 Pradaxa | CEREBROVASCULAR ACCIDENT | stroke |
| T23 Nexium | GASTRIC CANCER | gastric malignancy (5.1, a *masked condition*, not a reaction) |
| T29 Truvada | BONE DENSITY DECREASED, OSTEOPENIA | decreases in bone mineral density (5.5) |
| T05 Lipitor, T11 Januvia | PNEUMONIA | not expected in label; check |
| T15 Lamictal | PEMPHIGUS, TYPE 2 DIABETES MELLITUS, PERICARDITIS | unusual for lamotrigine; may come from duplicate or mass-filed reports (DQ37) |

**Non-clinical terms** (OFF LABEL USE, DRUG INEFFECTIVE, PRODUCT DOSE OMISSION ISSUE, PRODUCT ADHESION ISSUE) appear in most traces. D016 says to tag these, not rank them.

**Reporting artefacts to watch for:**
- T29 Truvada's top terms (bone loss, tooth loss, fractures) match the pattern of litigation-driven reporting. That's what D016's "lawyer-filed" tag is for.
- T13 OxyContin shows DRUG DEPENDENCE and DRUG DIVERSION. Under D016 those are abuse terms, to tag rather than rank.

**Single-word terms** (PAIN, COUGH, SWELLING) can match inside a longer phrase ("abdominal pain"). Each match record carries `single_word_term: true` and the exact text window, so the reviewer can see the context.

## 3. Rules a human must decide (these affect scoring)

1. **A symptom of a drug-caused condition:** is it a reaction or a symptom of another condition? This affects T08, T20 and T21. Without a rule, disagreement here is a gap in the scheme, not an error.
2. **"Avoid in patients with X":** is that contraindicated_population or a risk factor? (T18)
3. **A masked pre-existing condition:** add a class, or keep the closest fit? (T23)
4. **The synonym list for S6.** Should a pharmacist-made term-group list be added (D016 / DQ41 hand groups) before S6 is used in scoring?

## 4. Recall answers need a second pair of eyes (S7)

- `package_named_in_record = false` in 25 of 30 traces. Most of these are recalls of *generic* products with the same ingredient. That's correct, and it's the point: an ingredient match is not a package match.
- In 8 traces (T07, T09, T10, T14, T17, T22, T25, T27) the package appears in openFDA's harmonized list but **not** in the recall's own text. Please confirm the recall's text really excludes the selected package.
- `status_as_reported` is what the enforcement record says. It's never today's status. Examples: T30 Ambien "Completed", T01 Chantix "Ongoing" (2021).

## 5. Finding to confirm: label lag (S5)

**T17 Lyrica:** the DailyMed label behind NDC product 0071-1018 has effectiveTime **2020-06-15**, while SrLC shows a **04/25/2025** addition to 5.3 that isn't in the label. Please check whether a newer Lyrica SPL exists under another set ID.

## 6. What a reviewer records per row

`human_review_status` (approved / changed / rejected), the reviewer's role, the date, the corrected answer, and which rule from §3 was applied. Don't edit `claude/answers.jsonl`; add a new versioned record instead. Its freeze hash is in [validation.json](validation.json).
