# A012 — Signal statistics (PRR) + first Workshop screen with triage

| | |
|---|---|
| **Date** | 2026-11-04 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Pipelines / Ontology / App |
| **Status** | Kept (step 8 gate passed; D023 v2, D016 v2 and D042 waiting on your OK) |
| **Replaces** | none (prototype PRR from Oct 20 is now in Foundry) |

## What changed
| Before | Now | Why |
|---|---|---|
| PRR (proportional reporting ratio: how much more often a reaction is reported with this drug than with all other drugs) only in a local prototype | `ontology_signals.py` in Foundry → `ontology_ae_stats` (1,382 rows) + `ontology_signal_signals` (271) | Brief needs statistics inside the platform, traceable to rows |
| D023 duplicate fold only (same person key) | **D023 v2 (proposed):** reports listing **30 or more drugs** leave the primary population; their count is kept as `a_mass_reports` | A Canadian mass-polypharmacy cluster (465 of 3,408 oxycodone cases, median 122 drugs, ages change between filings) put pemphigus, rheumatic fever etc. at the top. The person key cannot catch it |
| D016 buckets: abuse/overdose, product use, pregnancy, lawyer tag | **D016 v2 (proposed):** + social/legal, efficacy, administrative, counterfeit and developmental terms | Top of the first list was "Child neglect", "Homicide", "Imprisonment" — real reports, but not drug side effects |
| No screen | Workshop module **MSSM Safety Officer** (ranked list → evidence → triage button → past decisions) | Safety officer question 1 + the trust rule |

## The idea in 3 lines
1. Count each drug × reaction once per report (D021 roles, D022 current versions, D023 fold), compute PRR + 95% CI + Yates χ², flag Evans (a ≥ 3, PRR ≥ 2, χ² ≥ 4).
2. A signal = Evans **and** not found in any reference label (D037 text check + the step 7 AI terms). Rank only clinical reactions with < 50% mass-report share; others stay visible with a bucket or a caution.
3. One screen: pick a signal, see every number and key behind it, record a decision whose `subject_key` + `evaluation_id` pin it to that exact computation.

## How we tested it
- PRR against the Oct 20 prototype (same quarters): Drug dependence a=506, PRR 114.7; Drug diversion a=467, PRR 297.2 → equal.
- Keys: 0 duplicate `stat_key`, 0 duplicate `signal_key`.
- Hand read of the top 40 before and after D023 v2 / D016 v2 (🩺 PV SME lens).
- Workshop end-to-end in **View** mode: select *Oxycodone · Myoclonus* (rank 15) → form opens with Subject Type `signal`, Subject Key `7804|Myoclonus|prr_evans_v2`, Evaluation Id `cbcd091262d23bd6` filled and locked → choose *reviewing* + rationale → Submit → full page reload → decision row shown under the signal.

## Result
| Measure | Value |
|---|---|
| Drug × reaction stats | 1,382 (329 meet Evans) |
| Label matches | 87 by text, 127 by AI terms (AI adds no new coverage here; its value is the quote) |
| Signals (Evans + not in label) | 271 → **125 ranked**, 80 with caution "mostly_mass_reports" |
| Workshop gate | Submit → "Edits successfully applied" → after reload the row is there: decided 2026-11-04 8:19 PM, decision id `d1f7474f…`, reviewer = current user ✅ |
| Plausible ranked candidates for the demo | myoclonus, hyperaesthesia (synonym case: label says "hyperalgesia/allodynia"), pupillary reflex impaired, unresponsive to stimuli, pulmonary granuloma |

## Verdict
**Keep.** Statistics match the prototype and the screen closes the loop "flag → evidence → decision → stored". Not yet polished:
- PRR / χ² show 12 decimals (fix: number format on the property in Ontology Manager).
- Past-decisions table is very short (fix: give that section a fixed height).
- The signal title repeats "Oxycodone ·" (fine while only one drug is in the pilot).
- Some ranked terms are still noise for a pharmacist (e.g. "Toothache" is ranked 107). They need a synonym table (label ↔ FAERS term, high/medium/low bands) and pharmacist review.

## Diagram (if structure changed)
No new structure beyond conventions §5 (AdverseEventStat, Signal). Screen layout: left = ranked table, right = triage button, decisions for the selected signal, full signal record.

## Persona check
- 🩺 PV SME: PRR on spontaneous reports measures reporting, not risk. The 30-drug cut is a blunt tool, so it keeps `a_mass_reports` visible rather than deleting. The label check is exact-term, so synonyms (hyperaesthesia vs hyperalgesia) will show as "not in label" until a synonym table exists.
- 💊 Safety Officer: "I can see why it is on the list and I can write down what I did about it." She will want the label quote next to "not in label", and fewer decimals.
- 🧐 Evaluator: Strong on traceability (evaluation id ties a decision to one computation). Weak on false positives: only a pharmacist read can say how many of the 125 are real.
