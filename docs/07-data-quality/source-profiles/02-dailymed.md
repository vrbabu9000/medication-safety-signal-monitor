# DailyMed: drug labels (SPL XML): hand profile

_Status: ⚪ Not started · How to access: [00-source-access-guide.md](00-source-access-guide.md) · Samples: run `python3 prototypes/explore/pull_samples.py` → `prototypes/data/oxycodone/` (dailymed_labels.json, dailymed_first_label.xml, dailymed_first_label_history.json, openfda_label_sample.json)_

## What to look at by hand
- [ ] Open the XML in a browser. Find the sections by LOINC code (34066-1 Boxed Warning, 34071-1 / 43685-7 Warnings, 34084-4 Adverse Reactions, 34070-3 Contraindications)
- [ ] Are adverse reactions written as prose, bullet lists or tables? (Tables matter for the LLM; see DQ10)
- [ ] Of the ~263 oxycodone labels: how many are the brand (innovator) vs generics vs repackagers vs combinations?
- [ ] Pick one label: how often does it change (history.json)? What changed between two versions?
- [ ] Compare the openFDA pre-parsed label with the XML. What's lost?

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
