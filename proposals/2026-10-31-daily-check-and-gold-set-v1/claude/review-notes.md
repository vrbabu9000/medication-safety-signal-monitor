# MSSM-30-v1 — review notes for human adjudication (Claude)

These are the places where the source's meaning is open to more than one reasonable reading. I expect these are where independent annotators could disagree. I'm basing that only on how ambiguous each source is; I haven't seen any other model's answers. Every row is still **pending** human review. When two models agree, that does not make the answer true.

**Suggested reviewers:** a pharmacovigilance (PV) pharmacist for G01–G12 and G18–G20; a pharmacy operations or inventory lead for G23, G24 and G28; a data engineer for the identity lookups (G13–G16, G25–G27).

## 1. Disagreements I expect (most likely first)

| ID | My answer | Plausible alternative | Why it's ambiguous | Evidence a reviewer needs |
|---|---|---|---|---|
| G04 | symptom_of_other_condition | reaction_or_warning | Nausea is listed as one way adrenal insufficiency can present, and adrenal insufficiency is itself opioid-related. Is nausea then a drug effect at one remove? | A written rule in the class definitions: does "symptom of a warned reaction" count as a reaction or as a symptom? |
| G07 | exposure_factor | administration_instruction | The passage says heat *increases absorption* (an exposure) and also *warns patients to avoid* heat (an instruction). | Whether the class goes with the phrase itself ("external heat exposure") or with the sentence's job |
| G11 | reaction_or_warning | co_medication_risk_factor or "interaction reaction" | For tramadol, serotonin syndrome is reported "particularly" with serotonergic drugs, but not only with them. | Whether the scheme needs an interaction-dependent qualifier |
| G12 | reaction_or_warning | underlying_condition_or_risk_factor | "Seizures" appears both as the outcome and in "history of seizures". This matters if the scorer works at mention level, not concept level. | Whether scoring is by mention or by concept within a passage |
| G03 | underlying_condition_or_risk_factor | contraindicated_population | Patients with esophageal cancer are at higher risk, and the label says "consider ... alternative analgesic". That is a caution, not a contraindication. | Confirm that contraindicated_population needs explicit "contraindicated" wording |
| G02 | reaction_or_warning | (no real alternative) | Low risk. The same section also has a contraindicated group and a risk group that an annotator might confuse with OIED. | None beyond the passage |
| G14 | "7052" resolved | unresolved | The question says "ingredient RxCUI", but the captured response has no term type. | A captured `rxcui/7052/properties.json` showing tty=IN |
| G16 | resolved | unresolved | `relatedGroup.rxcui` is null, so the link from 42844 to its ingredients rests on the request URL in the manifest. | Agree that the manifest URL counts as evidence, or capture `rxcui/42844/properties.json` |
| G23 | "unknown" | "no" or "yes" | Someone might read "Ongoing" as active, or might argue an old Class II recall has probably ended. Neither is supported by the evidence. | A current FDA or firm termination notice, or the latest weekly Enforcement Report |
| G29 | true | true, plus "added in this supplement" | The OIED text is underlined (added or revised) in the HTML. The plain-text view loses that markup. | Decide whether the case needs "included" or "newly added", and whether the HTML is the locator of record |
| G30 | 0 / 18 | (no real alternative on the value) | The risk is in how it's used: 0/18 must not be shown as a 0% rate. The AE time frame isn't in the captured module. | The time frame field from the full record, if the app will show this number |

## 2. Rules that need a human decision

1. **Class definitions (G01–G12).** Write a one-line definition and a tie-break rule for each of the 7 classes. The one that matters most: is "a symptom of a warned-about reaction" counted as a reaction, or as a symptom of another condition? Without that rule, G04-type disagreements are a gap in the scheme, not mistakes.
2. **Mention vs concept scoring.** G12 depends on it.
3. **Counting "unknown" as a correct answer.** G23 and G24 are resolved, and "unknown" is the right answer. The scorer must credit "unknown" here and must not treat it as abstaining.
4. **What counts as evidence for lookups.** Is a request URL in the manifest acceptable evidence (G16, G19), or does it have to be a field in the response body?
5. **Missing FAERS drug-filtered data.** Decide whether to recapture with an API key, which would allow new oxycodone-specific cases. The current FAERS cases must not be quietly swapped out.

## 3. Pack issues to fix before the next version (not answer disagreements)

| Issue | Effect |
|---|---|
| `evidence/srlc_oxy.*` (DrugNameID=2183) holds an **OZEMPIC** page | The file name is misleading. Rename it or drop it. No case uses it. |
| Two FAERS oxycodone captures failed: 403 `API_KEY_MISSING` | There's no drug-specific FAERS evidence. The manifest records them correctly as fetch_failed. |
| `docs_trials.text.txt` is 176 bytes (a script-rendered page) | The ClinicalTrials.gov cadence can't be checked from the pack |
| The manifest has no sha256 for failed fetches; only READY covers their error files | Small. Worth adding for completeness. |
| `docs_dailymed` contains unrelated site banner text | Ignore it as page chrome. Not used. |

## 4. What a reviewer should record per row

`human_review_status` (approved / changed / rejected), the reviewer's role, the date, the corrected answer if any, and which rule from §2 they applied. If a reviewer changes an answer, add a new versioned record. Don't edit the frozen `answers.jsonl`; its freeze hash is in [findings.md](findings.md).
