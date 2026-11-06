# Sample — AI review backed by papers: semaglutide + NAION

| | |
|---|---|
| **Date** | 2026-11-05 |
| **Status** | Exploration only (one sample). Not a pharmacist review. |
| **Stage** | Prototype |
| **Source** | PubMed, through NCBI's free public search API (E-utilities). The PubMed connector is not connected yet, but it reads the same database. |

## The flag being reviewed
| Field | Our value |
|---|---|
| Drug | Semaglutide |
| FAERS term | Optic ischaemic neuropathy (NAION = non-arteritic anterior ischemic optic neuropathy, a sudden loss of blood flow to the optic nerve) |
| Our result | **Not in label.** Ranked #1 for semaglutide (a = 394 reports). |
| Why "not in label" | No mention in any of the 36 safety sections across the semaglutide labels in DailyMed ([A014](../../../05-approaches/A014-label-faers-synonym-table.md)) |

Reviewer questions: (1) Is this a real safety concern, or noise? (2) Is "not in label" right?

## What the papers say (113 PubMed hits; 9 read at abstract level)
| PMID | Year · type | Finding | Direction |
|---|---|---|---|
| 38958939 | 2024 · cohort, 1 US centre (Hathaway) | First report. Hazard ratio (HR, how much higher the risk is) 4.28 in diabetes, 7.64 in obesity | ↑ risk |
| 40098249 | 2025 · Danish–Norwegian national cohort | HR 2.81 vs SGLT-2 inhibitors. Absolute risk low (~2–3 per 10,000 person-years) | ↑ risk, small |
| 41217382 | 2026 · large US cohort (1.2 M) | Odds ratio 0.36 in diabetes (lower risk). No link in obesity | ↓ / none |
| 41475544 | 2026 · meta-analysis, 8 trials + 8 cohorts | HR 1.85 in diabetes cohorts. **Not confirmed by randomised trials** | ↑ in cohorts only |
| 41692115 | 2026 · meta-analysis, 6 cohorts (4.8 M) | No consistent rise overall (aHR 1.63, CI crosses 1). Very low to low certainty | Unclear |
| 42132708 | 2026 · **consensus statement**, NANOS + AAO (US eye-doctor societies) | Small possible rise in risk; absolute risk low; shared decision-making | Expert view |
| 42259643 | 2026 · **FAERS** analysis | Semaglutide strong signal (355 reports, ROR 94). Also tirzepatide and liraglutide; none for dulaglutide, exenatide, lixisenatide. Notes **EMA (European regulator) has taken action** | Matches our signal |
| 42871459 | 2026 · FAERS analysis by indication | NAION signal for semaglutide (ROR 4.42) | Matches our signal |
| 41144820 | 2025 · *Retina* | **Retracted.** Excluded | — |

## AI review verdict
| Question | Verdict | Confidence | Basis |
|---|---|---|---|
| 1. Real concern or noise? | **Real concern worth showing.** Not proven causal. | Medium | Two independent FAERS analyses find the same signal. Cohorts are mixed. Trials don't confirm it. Expert consensus says "small possible risk". |
| 2. "Not in label" correct? | **Can't be settled by papers.** Keep our DailyMed check as the answer. | — | PubMed tells us about the science, not what is on the US label. One paper says EMA acted. That points to the EU label, not the US one (unverified here). |
| Action for the safety officer | Keep it ranked #1. Add a note: "EU regulator acted; US label had no mention at capture date; evidence mixed." Re-check DailyMed at each label refresh. | — | — |

## What this sample teaches about the method
1. **Papers answer "is it real?", not "is it on the label?"** Label status must come from DailyMed, as it already does. The AI review checks the clinical side and leaves the label side to DailyMed.
2. **It caught a trap.** One hit was a retracted paper. Any automated version must drop retractions.
3. **It gave a cross-check we didn't have.** A published FAERS study finds the same drug–event signal and the same class pattern. Our pipeline didn't invent it.
4. **Its limits.** I read abstracts, not full texts. One reviewer (Claude), with no second opinion. And the "is it on the label?" judgement still needs a pharmacist. So: *AI review backed by papers; pharmacist sign-off still open.*

## Effort
About 6 API calls, around 10 minutes. A real pharmacist reading this page could agree or disagree in about 2 minutes.
