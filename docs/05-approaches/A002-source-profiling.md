# A002 — Source profiling: look at every source by hand before building

| | |
|---|---|
| **Date** | 2026-10-19 |
| **Design-thinking stage** | Define |
| **Area** | Data |
| **Status** | Trying (in progress) |
| **Replaces** | none |

## What changed
| Before | Now | Why |
|---|---|---|
| Data problems were *suspected* from general knowledge (register DQ01–DQ17) | Every source has a tested access path, a sample puller and a hand-profile file | Boss: "look at each source manually". Data judgment is graded |
| Opioid scope chosen on the boss's suggestion | Class choice is being tested by 3 parallel research tracks (R1–R3) | User unsure narcotics is right. Decide with evidence |

## The idea in 3 lines
1. Tested links for browse / API / bulk for each source → [00-source-access-guide.md](../07-data-quality/source-profiles/00-source-access-guide.md).
2. One script pulls ~100 records per source for any drug → [pull_samples.py](../../prototypes/explore/pull_samples.py).
3. Fill one profile file per source; every new problem goes to the register.

## First results (2026-10-19, oxycodone)
| Source | Quick fact | So what |
|---|---|---|
| FAERS | ~331k reports. Top reactions: drug dependence, pain, overdose, **emotional distress** | Litigation/abuse terms dominate (DQ15, DQ18) |
| DailyMed | 263 labels; Percocet at version 66, 3 changes in 2 months | Lots of label churn → good for "what changed" and drift |
| Recalls | 25 records; 4 Ongoing; drug named only in free text | Join is the hard part (DQ11) |
| RxNorm | oxycodone = RxCUI 7804; ATC N02A lists all opioids | Official, reproducible formulary definition |
| CT.gov | First result = bioequivalence study | Needs filtering to be useful |

## Verdict
Trying. Complete when all 5 profile files are filled.

## Update 2026-10-20
| Before | Now | Why |
|---|---|---|
| Empty profile files with checklists | **Structure reports for all 5 sources** (shape, real example, categories, join keys, mess, how to use) + volumes for 13 drugs + 2 worked merges | User: understand structure, navigation, volumes and joins before building |

Reports: [01 FAERS](../07-data-quality/source-profiles/01-faers.md) · [02 DailyMed](../07-data-quality/source-profiles/02-dailymed.md) · [03 Recalls](../07-data-quality/source-profiles/03-enforcement.md) · [04 RxNorm](../07-data-quality/source-profiles/04-rxnorm.md) · [05 Trials](../07-data-quality/source-profiles/05-clinicaltrials.md) · [06 Volumes](../07-data-quality/source-profiles/06-data-volume-13-ingredients.md) · [Merge walkthrough](../04-architecture/merge-walkthrough-v1.md). New data issues DQ23–DQ32.
