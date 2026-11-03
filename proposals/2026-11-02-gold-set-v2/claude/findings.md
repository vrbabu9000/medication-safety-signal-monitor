# MSSM-30-v2: what we built and what it shows

**What it is:** a candidate reference set. It is **verified against its sources by code** and **not yet reviewed by a pharmacist**. It isn't a clinician-adjudicated gold standard or a label-extraction benchmark. Don't report "AI clinical accuracy" from it until the review is done.

**Shape:** 30 brand-name products × 8 public sources = 240 answers. Each product is one *trace* that follows the medicine from its name to its package, label, safety changes, reports, recalls and a trial.

📊 How one trace works: [20-gold-trace-v1.png](../../../docs/diagrams/png/20-gold-trace-v1.png) · [PDF](../../../docs/diagrams/pdf/20-gold-trace-v1.pdf) · One-page walkthrough per drug: [cards/](../cards/)

## 1. Headline numbers

| Check | Result |
|---|---|
| Products screened → eligible (all 8 sources usable) → used | 62 → 35 → 30 ([screening report](../screening/screening-report.json); every rejection has a reason) |
| Classes covered | 21 (3 combination products: Vytorin, Janumet, Truvada) |
| Answers | 240 · **0 unresolved** · 0 deliberate "unknown" answers |
| Automated checks ([verify_trace.py](../tools/verify_trace.py), separate code re-reading raw bytes) | **3,403 / 3,403 pass** |
| Evidence files, sha256 match | 530 / 530 |
| Identity guards (right drug, right application, right label, right trial) | 530 passed, 0 rejected in the final capture |
| openFDA key | Used on every openFDA call; stored as `api_key=REDACTED` in every saved URL |
| FAERS evidence | Aggregate only: `limit=0` totals and count queries. No report records stored |
| Questions frozen before answers | Yes; per-trace sha256 in [validation.json](validation.json) |
| Human review | **Pending** on all 240 |

## 2. What each source was used for

| Step | Source | Question type | Check type | Judgement needed? |
|---|---|---|---|---|
| S1 | RxNorm | Brand → ingredient RxCUI(s), plus a reverse check | Lookup | No |
| S2 | NDC Directory | Package, labeler, application number; link to label set ID | Lookup + link | No |
| S3 | Drugs@FDA | Sponsor, products, strengths; link to the NDC application | Lookup + link | No |
| S4 | DailyMed label | Classify one phrase in one passage (7 classes) | **Label interpretation** | **Yes: pharmacist** |
| S5 | SrLC | Latest safety-label change with added text; is it in the label? | Lookup + link | No |
| S6 | FAERS | Brand vs substance report counts; top-10 terms vs label | Lookup + string check | **Yes: synonym review** |
| S7 | FDA enforcement | Latest recall; does its own text name the package? | Cross-source | Light: ops check |
| S8 | ClinicalTrials.gov | One arm's serious adverse events, affected / at risk | Lookup | No |

## 3. Results by trace (S4 = my label call; S5 ✔ = SrLC change found in the label; S7 ✔ = recall text names the package)

| ID | Product | Class | S4 class | S5 | FAERS 2025 brand / substance | Latest recall (as reported) | S7 | Trial arm SAE |
|---|---|---|---|---|---|---|---|---|
| T01 | Chantix | smoking cessation | risk factor | ✔ | 127 / 527 | D-0809-2021 Class II, Ongoing | ✔ | 39/2016 |
| T02 | Pradaxa | anticoagulant | co-medication | ✔ | 533 / 680 | D-0738-2026 Class III, Ongoing | ✘ | 724/2676 |
| T03 | Plavix | antiplatelet | risk factor | ✔ | 2201 / 9064 | D-0787-2021 Class II, Terminated | ✘ | 322/6312 |
| T04 | Brilinta | antiplatelet | reaction | ✔ | 539 / 1700 | D-0433-2021 Class II, Terminated | ✔ | 1853/6958 |
| T05 | Lipitor | statin | reaction | ✔ | 3727 / 11221 | D-0020-2026 Class II, Ongoing | ✘ | 3/298 |
| T06 | Vytorin | statin combination | contraindicated | ✔ | 77 / 291 | D-0462-2025 Class III, Ongoing | ✘ | 3640/9067 |
| T07 | Jardiance | SGLT2 | risk factor | ✔ | 7741 / 9604 | D-0185-2024 Class II, Terminated | ✘ | 876/2345 |
| T08 | Farxiga | SGLT2 | symptom of other | ✔ | 3063 / 3258 | D-0435-2021 Class II, Terminated | ✘ | 3/166 |
| T09 | Victoza | GLP-1 | instruction | ✔ | 1117 / 1992 | D-0622-2021 Class II, Terminated | ✘ | 2320/4668 |
| T10 | Rybelsus | GLP-1 | exposure | ✔ | 1567 / 27462 | D-0536-2021 Class II, Terminated | ✘ | 2941/8803 |
| T11 | Januvia | DPP-4 | reaction | ✔ | 1636 / 1817 | D-0746-2022 Class II, Terminated | ✘ | 928/7266 |
| T12 | Janumet | DPP-4 combination | risk factor | ✔ | 505 / 704 | D-0746-2022 Class II, Terminated | ✔ | 63/5527 |
| T13 | OxyContin | opioid | reaction | ✔ | 1114 / 5323 | D-0338-2026 Class II, Ongoing | ✘ | 9/223 |
| T14 | Belbuca | opioid | instruction | ✔ | 384 / 898 | D-0448-2021 Class II, Terminated | ✘ | 38/727 |
| T15 | Lamictal | antiepileptic | co-medication | ✔ | 2383 / 7913 | D-1329-2022 Class III, Terminated | ✘ | 32/787 |
| T16 | Keppra | antiepileptic | reaction | ✔ | 2431 / 8907 | D-0365-2025 Class I, Ongoing | ✘ | 24/255 |
| T17 | Lyrica | antiepileptic | co-medication | **✘** | 3458 / 12995 | D-0649-2016 Class II, Terminated | ✘ | 2/319 |
| T18 | Zoloft | SSRI | risk factor | ✔ | 2312 / 14104 | D-0227-2026 Class II, Ongoing | ✘ | 2/119 |
| T19 | Cipro | fluoroquinolone | exposure | ✔ | 402 / 1061 | D-0626-2025 Class II, Ongoing | ✘ | 2/827 |
| T20 | Zithromax | macrolide | symptom of other | ✔ | 408 / 545 | D-0997-2022 Class II, Terminated | ✘ | 3273/97047 |
| T21 | Seroquel | antipsychotic | symptom of other | ✔ | 1628 / 5052 | D-1000-2020 Class III, Terminated | ✘ | 1/100 |
| T22 | Abilify | antipsychotic | reaction | ✔ | 1453 / 5887 | D-0468-2024 Class III, Ongoing | ✘ | 56/505 |
| T23 | Nexium | PPI | risk factor | ✔ | 2328 / 3841 | D-0443-2025 Class II, Ongoing | ✘ | 8/2156 |
| T24 | Prilosec | PPI | co-medication | ✔ | 1174 / 1737 | D-0466-2021 Class II, Terminated | ✔ | 61/2237 |
| T25 | Diovan | ARB | reaction | ✔ | 371 / 4192 | D-0746-2026 Class II, Ongoing | ✘ | 1031/2297 |
| T26 | Cozaar | ARB | contraindicated | ✔ | 603 / 5713 | D-0498-2024 Class II, Ongoing | ✘ | 691/1913 |
| T27 | Synthroid | thyroid | instruction | ✔ | 6794 / 16477 | D-0088-2024 Class III, Ongoing | ✘ | 4/339 |
| T28 | Singulair | leukotriene antagonist | risk factor | ✔ | 4162 / 7702 | D-0086-2024 Class II, Terminated | ✘ | 0/1453 |
| T29 | Truvada | antiretroviral combination | contraindicated | ✔ | 1333 / 1506 | D-0013-2015 Class III, Terminated | ✔ | 118/1584 |
| T30 | Ambien | hypnotic | contraindicated | ✔ | 1268 / 5046 | D-0272-2024 Class II, Completed | ✘ | 4/263 |

How to read the numbers:
- **FAERS** counts are *reports* matching each saved query (received 1 Jan–31 Dec 2025, any drug role). They are not patients, rates or causes.
- **Trial** numbers are serious adverse events in one arm, as affected / at risk. They are not population risk.
- **Recall status** is the status in the FDA record. FDA doesn't update it after classification, so it is not today's status.

## 4. Traps the set exposes (what a naive system would get wrong)

| Trap | Where | What we found |
|---|---|---|
| A substance query mixes products | T01 | Varenicline reports: 527 for the substance, 127 naming Chantix. 274 named Tyrvaya nasal spray, which pushed sneezing and eye pain into the top terms |
| Brand vs generic scope | All | Brand-named counts are 6%–94% of the substance counts (Rybelsus 1,567 of 27,462, because Ozempic shares the substance) |
| Recall "package list" is application-wide | 8 traces | `openfda.package_ndc` lists the package, but the recall's own text names a different strength or pack |
| Ingredient recall ≠ brand recall | 17 traces | The latest recall was found only at ingredient level, and it covers generic products |
| Label lag | T17 Lyrica | DailyMed label effective **2020-06-15** lacks the **04/25/2025** SrLC addition on suicidal behaviour after discontinuation |
| Publication date ≠ effective date | T17 | DailyMed "published Sep 29, 2025", but the label's own effectiveTime is 2020 |
| RxNorm body doesn't name its subject | All | `related.json` returns `rxcui: null`, so a reverse lookup is needed to prove the link |
| Names differ across FDA sources | All | e.g. sponsor "PF PRISM CV" vs labeler "Pfizer Laboratories Div Pfizer Inc". Join on application number |
| Context in a label passage | S4 ×30 | 11 of the 30 S4 targets sit next to a different-class phrase in the same passage (e.g. Belbuca instruction vs dental-decay reaction) |
| Synonyms defeat string matching | S6 | CEREBROVASCULAR ACCIDENT vs "stroke"; GASTRIC CANCER vs "gastric malignancy" |
| Reporting artefacts | T29, T13, T15 | Litigation-shaped Truvada profile; abuse terms for OxyContin; odd Lamictal terms |

## 5. Lookup checks vs label-interpretation checks

- **Source lookups (S1, S2, S3, S5, S6 counts, S7, S8): 210 answers.** These are facts read from a field. The verifier re-derives each one from the raw bytes, so they are as strong as the source itself.
- **Label interpretation (S4): 30 answers.** Each is my judgement, anchored to a verbatim quote. These are the only items fit for scoring an AI label reader, and only after pharmacist review.
- **String checks (S6 "found in label"): 300 term checks.** True or false as text facts. Their clinical meaning needs the synonym review.

## 6. Freshness: live re-check (separate from the frozen answers)

| | |
|---|---|
| Frozen capture | 2026-11-02 18:36–18:43 UTC (530 requests) |
| Live re-check started | 2026-11-02 18:46 UTC ([drift-report.json](../drift-report.json)) |
| Sources byte-identical | **530 / 530** |
| Traces whose answers re-derive the same from live bytes | **30 / 30** |

No drift so soon after capture is expected. What this run proves is that the re-check works end to end: re-fetch → hash compare → re-derive answers in a throwaway copy → report, with the frozen files untouched. Run it again (`python3 tools/live_check.py <scratch_dir>`) before any demo or scoring. The sources likely to move first are FAERS (next quarterly refresh), enforcement (weekly), NDC and Drugs@FDA (daily or weekdays) and the DailyMed label versions.

The re-check times above are our own fetch times, not when the publisher released the data.

## 7. Limits (stated, not hidden)

- **Purposive sample:** 30 well-documented brand-name products (New Drug Applications only, since Drugs@FDA doesn't hold biologics). Not representative of a hospital formulary. Only 4 overlap the pilot formulary (OxyContin, Belbuca, Victoza, Rybelsus).
- **FAERS:** the openFDA API can't restrict counts to "suspect drug only" for one drug. Each answer states its query. No deduplication beyond openFDA's own.
- **S4 classes** have no written tie-break rules yet ([review-notes.md](review-notes.md) §3).
- **ClinicalTrials.gov:** the arm is chosen by a fixed rule (largest completed interventional study whose adverse-event group names the drug). That is one example, not the best evidence.
- **Pilot template changes** were made after T01 and before T02–T30, and are logged in [A008](../../../docs/05-approaches/A008-gold-set-v2-cross-source-traces.md). T01 was rebuilt with the final template.
- **Screening** used live sources through a temporary cache, which was deleted afterwards. The screening report keeps totals only.
