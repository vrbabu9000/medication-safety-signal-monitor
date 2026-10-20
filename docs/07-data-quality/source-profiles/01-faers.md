# FAERS: adverse event reports: hand profile

_Status: ⚪ Not started · How to access: [00-source-access-guide.md](00-source-access-guide.md) · Samples: run `python3 prototypes/explore/pull_samples.py` → `prototypes/data/oxycodone/` (faers_sample_reports.json, faers_top_reactions.json, faers_by_receivedate.json)_

## What to look at by hand
- [ ] Open one report. Find: `safetyreportid`, `receivedate`, `serious`, `patient.drug[]` (with `drugcharacterization`: 1 = suspect, 2 = concomitant, 3 = interacting), `patient.reaction[].reactionmeddrapt`
- [ ] How many drugs per report? How often is oxycodone the *suspect* vs a bystander?
- [ ] How are drug names written in `medicinalproduct`? Count spellings and brands
- [ ] How many reports have empty `openfda` blocks (so no clean drug ID)?
- [ ] Top 20 reactions: which are abuse/overdose/litigation terms vs clinical reactions?
- [ ] Duplicates: are there reports with the same patient, dates and drugs?
- [ ] Report types: `primarysource.qualification` (doctor, consumer, lawyer?)

## Profile (fill in as you explore)
| Item | Finding |
|---|---|
| Access (URL, auth, limits, size) | |
| Update clock (documented vs seen) | |
| Record shape (key fields) | |
| Categories found | |
| How drugs are named / identified | |
| Mess found (with counts) | |
| Freshness seen | |

## Decisions
| What | Fix / accept | Why |
|---|---|---|
| | | |

New problems → add to [data-issues-register.md](../data-issues-register.md).
