# Research — synthesis (2026-10-19)

Three research tracks were run in parallel. Each report keeps its full numbered source list (140 sources in total, all accessed 2026-10-19) and tags every claim as verified or inferred.

| # | Question | Report | Sources |
|---|---|---|---|
| R1 | Which therapeutic class? (constant change, need, data) | [R1-therapeutic-class.md](R1-therapeutic-class.md) | 40 |
| R2 | Is this use case real and required in industry? | [R2-industry-need.md](R2-industry-need.md) | 48 |
| R3 | Has this been built already? | [R3-prior-art.md](R3-prior-art.md) | 52 |

## The answers in plain words
| Question | Answer | Confidence |
|---|---|---|
| **Is narcotics (opioids) right?** | **Good anchor, weak alone.** Hospitals care most about opioids, but their FAERS data is dominated by lawsuits and abuse reports. Best pick: **opioid-led hybrid, 8 opioids + 5 GLP-1 drugs** (score 27/30 vs 22 for opioids alone) | Scoring = judgment; facts verified |
| **Which class changes constantly?** | GLP-1s: steady label changes (13 safety-label entries in 2026 so far). Opioids: big class-wide waves (Dec 2023, Dec 2025) plus heavy day-to-day label churn (18 of 1,274 labels revised in 30 days) | Verified (FDA SrLC, DailyMed) |
| **Is the need real?** | **Recall monitoring: yes, required.** CMS hospital rules expect pharmacies to monitor recalls and remove recalled drugs. **Unlabeled-side-effect monitoring: no, not a hospital duty today.** It's done by drug makers and FDA. That's our novelty *and* our adoption risk | Verified (CMS SOM App. A) |
| **Pain point with numbers** | ~1 in 5 Class I recalls (2004–2011) went out with no FDA alert notice (Arch Intern Med 2012). One hospital cut recall review from ~2.5 hrs → ~10 min with inventory matching (vendor-reported) | Verified / vendor claim |
| **Has it been done?** | **Pieces exist, the combination doesn't (that we found).** OFFSIDES = FAERS side effects not on labels (static, ~2019). OnSIDES = label extraction (BERT, MIT/CC-BY). FDA's AskFDALabel = LLM over labels. Commercial tools serve pharma, not hospital safety officers | "Not found" = inferred |
| **Benchmark for our AI** | Published label-extraction scores: F1 ≈ 0.85–0.91 (TAC 2017, OnSIDES, AskFDALabel). Warnings sections are harder (~0.74–0.76). **Target: F1 ≥ 0.85, reported per section** | Verified (papers) |

## 🚨 Three surprises that change the design
| # | Surprise | Impact | Verified by Claude? |
|---|---|---|---|
| 1 | **FDA replaced FAERS with AEMS (Adverse Event Monitoring System) on 11 Mar 2026**, with near-real-time reporting. openFDA's FAERS API is still on `last_updated = 2026-07-30` | The brief names FAERS. We must check whether AEMS has a public bulk feed/API. This could change ingestion, and "since yesterday" for adverse events | ✅ Confirmed in trade press (RAPS, ASCO Post). FDA's own feed details still open |
| 2 | **Lawyers filed most oxycodone reports in 2021**: 35,660 of 61,817 reports with a reporter type (~58%) | Signals must exclude or separate lawyer-reported cases, or the ranking measures lawsuits | ✅ Re-ran openFDA query |
| 3 | **"Hyperalgesia" returns 0 FAERS reports** even though FDA added it to opioid labels in 2023. FDA's cases are coded under other terms | A plain term match would miss our best opioid backtest. We need term grouping | ✅ Re-ran openFDA query |

## Demo-ready value story (from R2)
1. Recalls are a **required** hospital duty, and alerts can be missed or late. We put them on one screen, matched to the formulary.
2. Unlabeled-signal monitoring is **new for hospitals**: we bring a pharma/FDA-grade method to the safety officer.
3. Every flag links to the FDA/NLM source. openFDA's own terms say not to use its recall data alone for public alerts, so source links are a must.
4. AI accuracy is measured against public benchmarks, not asserted.

## Open checks (carried into A003)
AEMS public data access · opioid hyperalgesia term mapping · NAION status on US semaglutide labels (R1 says absent; openFDA label search also found no match) · ISMP high-alert list from the primary PDF · lawyer-report share after dedup from bulk files.
