# How much data do we have? — 13 pilot ingredients

_Run live on **2026-10-20** with [volume_check.py](../../../prototypes/explore/volume_check.py) · raw numbers: `prototypes/data/_volume.json` (git-ignored) · chart: [14-data-volume-v1.png](../../diagrams/png/14-data-volume-v1.png) · [PDF](../../diagrams/pdf/14-data-volume-v1.pdf) · ongoing recalls: [15-recalls-ongoing-v1.png](../../diagrams/png/15-recalls-ongoing-v1.png)_

## TL;DR
- **FAERS is big:** 1.46M reports across our 13 drugs (of 20.7M in all FAERS). openFDA was last refreshed **2026-07-30**.
- **Recalls favour opioids:** fentanyl, morphine and hydromorphone have 189–357 recalls each, mostly compounded IV bags. **Semaglutide has 47 recalls still Ongoing.**
- **Labels:** opioids have hundreds of labels each (generics and repackagers). GLP-1s have 3–23. Label churn shows up as 0–5 updates per drug in the last 30 days.
- **FAERS through the API is fine for counts, but not enough for analysis.** The API can't filter "this drug was the suspect", and it can page through only about 26k records per query. **The real pipeline needs the quarterly bulk files** (decision D004 confirmed).

## FAERS (adverse event reports)
| Drug | Class | RxCUI | Reports (total) | 2025 | 2026 (to Jul) | Serious % | Lawyer-filed % |
|---|---|---|---|---|---|---|---|
| oxycodone | opioid | 7804 | 330,925 | 12,544 | 5,749 | 86 | **29** |
| morphine | opioid | 7052 | 191,639 | 6,625 | 2,857 | 86 | 25 |
| buprenorphine | opioid | 1819 | 124,273 | 6,100 | 2,267 | 61 | 24 |
| fentanyl | opioid | 4337 | 114,884 | 6,593 | 2,696 | 85 | 5 |
| hydrocodone | opioid | 5489 | 96,249 | 999 | 501 | 86 | **51** |
| hydromorphone | opioid | 3423 | 91,455 | 1,745 | 719 | 93 | **51** |
| methadone | opioid | 6813 | 45,992 | 2,086 | 891 | 87 | 9 |
| tramadol | opioid | 10689 | 38,296 | 2,834 | 1,188 | 90 | 4 |
| tirzepatide | GLP-1 | 2601723 | 160,663 | **62,302** | **39,348** | 18 | 0 |
| dulaglutide | GLP-1 | 1551291 | 88,160 | 5,872 | 2,469 | 26 | 1 |
| semaglutide | GLP-1 | 1991302 | 73,001* | 20,013 | 12,003 | 50 | 1 |
| exenatide | GLP-1 | 60548 | 52,314 | 75 | 8 | 28 | 2 |
| liraglutide | GLP-1 | 475968 | 50,704 | 2,203 | 1,293 | 49 | 2 |

\* Searching semaglutide by the active-ingredient field gives **100,679**. Which field you search changes the count by 38% (DQ25).

**What kinds of reactions?** These are mentions among each drug's top-100 terms, and one report can have several reactions.

| Drug | Clinical | Abuse/overdose | Litigation-style | Product-use/error | Top clinical terms |
|---|---|---|---|---|---|
| oxycodone | 479k | **272k** | **148k** | 21k | Nausea, Fatigue, Diarrhoea, Vomiting, Depression |
| hydrocodone | 77k | **108k** | 41k | 1k | Depression, *Neonatal withdrawal*, Nausea, *Foetal exposure* |
| fentanyl | 132k | 54k | 21k | 8k | Nausea, Vomiting, Fatigue, **Hypotension**, Dyspnoea |
| tirzepatide | 180k | 3k | 10k | **64k** | Nausea, **Injection site pain**, Diarrhoea, Vomiting |
| semaglutide | 125k | 0.5k | 5k | 20k | Nausea, Vomiting, Diarrhoea, Decreased appetite |
| liraglutide | 75k | 0.5k | 3k | 5k | Nausea, Blood glucose increased, Vomiting, **Pancreatitis** |

**So what:**
- Opioids need the lawyer and abuse filters (our focus rule). GLP-1s need a **product-use/dose-error** filter instead; tirzepatide has 64k such mentions.
- Pregnancy and neonatal terms (neonatal withdrawal, foetal exposure) need their own bucket (DQ26).

### How much can we pull from FAERS?
| Route | What you get | Limit |
|---|---|---|
| openFDA API `count=` | Totals by any field (reaction, year, reporter): instant | None that matters for counts |
| openFDA API records | Full reports | 1,000 per call, `skip` up to 25,000 → **~26k records per query**. Oxycodone has 331k |
| openFDA bulk JSON | All reports as zipped JSON | Whole dataset |
| **FAERS quarterly ASCII** (fis.fda.gov) | Case-level tables: DEMO, DRUG, REAC, OUTC, INDI, THER, RPSR. **Drug role per drug** and **case version for dedup** | Whole dataset, one quarter at a time → our incremental pipeline |

## Recalls (FDA enforcement)
| Drug | Total | Ongoing | Class I / II / III | Last 12 months |
|---|---|---|---|---|
| fentanyl | **357** | **22** | **18** / 320 / 19 | 9 |
| morphine | 189 | 7 | 15 / 162 / 12 | 2 |
| hydromorphone | 189 | 3 | 12 / 174 / 3 | 1 |
| buprenorphine | 32 | 6 | 0 / 27 / 5 | 4 |
| oxycodone | 25 | 4 | 1 / 12 / 12 | 3 |
| hydrocodone | 22 | 1 | 4 / 11 / 7 | 0 |
| tramadol | 12 | 2 | 0 / 9 / 3 | 1 |
| methadone | 11 | 1 | 0 / 10 / 1 | 0 |
| semaglutide | 54 | **47** | 0 / 54 / 0 | **24** |
| tirzepatide | 21 | **21** | 1 / 20 / 0 | 3 |
| liraglutide | 4 | 1 | 1 / 3 / 0 | 1 |
| dulaglutide | 3 | 0 | 0 / 3 / 0 | 0 |
| exenatide | 1 | 1 | 0 / 1 / 0 | 1 |

**So what:**
- **Question 2 ("active recall?") will always have answers:** 116 Ongoing recalls across our 13 drugs.
- Fentanyl recalls are mostly **compounded IV bags** (in the sample: 82 of 100 for sterility). That's hospital-relevant.
- Counting is done by free-text match on `product_description`, so some recalls could be missed or wrongly matched (DQ11).

## Labels (DailyMed)
| Drug | Labels | Updated in last 30 days | | Drug | Labels | Updated 30d |
|---|---|---|---|---|---|---|
| hydrocodone | 357 | 2 | | semaglutide | 9 | 0 |
| oxycodone | 263 | 3 | | tirzepatide | 8 | 0 |
| tramadol | 237 | 5 | | liraglutide | 23 | 4 |
| buprenorphine | 133 | 3 | | dulaglutide | 7 | 0 |
| morphine | 124 | 3 | | exenatide | 3 | 0 |
| methadone | 59 | 1 | | | | |
| hydromorphone | 55 | 0 | | | | |
| fentanyl | 46 | 0 | | | | |

**Total:** 1,324 labels, of which **21 were updated in the last 30 days** (17 opioid, 4 GLP-1). That's the base for "what changed" and the drift window. Some labels carry very large version numbers (e.g. 3,540), so version numbers are not comparable across labels (DQ27).

## ClinicalTrials.gov (trials with posted results)
morphine 543 · fentanyl 299 · oxycodone 224 · buprenorphine 223 · liraglutide 144 · methadone 140 · exenatide 128 · hydromorphone 113 · semaglutide 109 · hydrocodone 72 · tramadol 67 · dulaglutide 61 · tirzepatide 47.
Plenty of second-opinion data. Expect many studies to be small or anaesthesia studies; filter to the drug being the studied treatment.

## Honest caveats
- **The "suspect only" count doesn't work through the API.** It returned almost the same number as the total, because openFDA can't tie the role to *this* drug inside a report. In a hand sample of 100 oxycodone reports, oxycodone was the suspect in only **15 of 118** entries; the rest were concomitant (DQ23). Fix: bulk files.
- Counts are **not deduplicated**.
- Label "updated in 30 days" only scanned up to 1,500 labels per drug, which covers all of ours.
