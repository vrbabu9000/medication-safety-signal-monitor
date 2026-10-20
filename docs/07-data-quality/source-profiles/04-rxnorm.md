# RxNorm / RxNav: drug IDs: hand profile

_Status: ⚪ Not started · How to access: [00-source-access-guide.md](00-source-access-guide.md) · Samples: run `python3 prototypes/explore/pull_samples.py` → `prototypes/data/oxycodone/` (rxnorm_rxcui.json, rxnorm_related.json, rxclass_opioids_atc_N02A.json)_

## What to look at by hand
- [ ] Term types: IN (ingredient), PIN (precise ingredient, e.g. salt), BN (brand), SCD/SBD (clinical/branded drug). Which do we key on? (plan: IN)
- [ ] ATC N02A members: is this our formulary list? What's included that we don't want (e.g. combos with naloxone)?
- [ ] Test messy FAERS names with approximateTerm. What's the hit rate on 50 real names?
- [ ] Can recall NDCs be mapped with `ndcstatus` / `ndcproperties`?

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
