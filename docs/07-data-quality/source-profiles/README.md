# Source profiling — look at each source by hand

Boss guidance (2026-10-13): look at each source manually, see how it looks and what categories it falls into, **before** building pipelines.
One file per source: `NN-source-name.md`. New problems go into [data-issues-register.md](../data-issues-register.md).

## Order (biggest risk first)
| # | Source | File | Status |
|---|---|---|---|
| 0 | **Where + how to access every source** | [00-source-access-guide.md](00-source-access-guide.md) | ✅ Done (tested 2026-10-19) |
| 1 | FAERS (adverse event reports) | [01-faers.md](01-faers.md) | ⚪ Not started |
| 2 | DailyMed labels (SPL XML) | [02-dailymed.md](02-dailymed.md) | ⚪ |
| 3 | FDA enforcement (recalls) | [03-enforcement.md](03-enforcement.md) | ⚪ |
| 4 | RxNorm (drug IDs) | [04-rxnorm.md](04-rxnorm.md) | ⚪ |
| 5 | ClinicalTrials.gov | [05-clinicaltrials.md](05-clinicaltrials.md) | ⚪ |

## Checklist per source (copy into each file)
1. **Access:** URL, format, auth, rate limits, file size, update clock.
2. **Sample:** pull ~100 opioid records. Save them in `prototypes/data/` (git-ignored).
3. **Shape:** fields, types, nesting, one record shown as an example.
4. **Categories:** what kinds of records exist (e.g. recall Class I/II/III; report types; label sections).
5. **Identity:** how drugs are named here, and how we'll map them to RxNorm.
6. **Mess found:** missing values, duplicates, free text, odd codes, contradictions. Count them.
7. **Freshness:** last update date seen vs. documented.
8. **Decision:** what we fix, what we accept, and why.
