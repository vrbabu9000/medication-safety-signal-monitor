# FDA enforcement reports: recalls: hand profile

_Status: ⚪ Not started · How to access: [00-source-access-guide.md](00-source-access-guide.md) · Samples: run `python3 prototypes/explore/pull_samples.py` → `prototypes/data/oxycodone/` (recalls_sample.json, recalls_by_class.json, recalls_by_status.json)_

## What to look at by hand
- [ ] Fields: `recall_number`, `classification`, `status`, `reason_for_recall`, `product_description`, `recall_initiation_date`, `report_date`, `openfda` (often empty?)
- [ ] How is the drug named in `product_description`? Can we pull NDC codes out of it?
- [ ] Group `reason_for_recall` into categories (contamination, potency, labeling, cGMP, etc.)
- [ ] What does 'Ongoing' vs 'Terminated' vs 'Completed' really mean for 'active'?
- [ ] Are compounded / outsourcing-facility products in here? How do we spot them?

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
