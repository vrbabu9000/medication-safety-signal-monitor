# ClinicalTrials.gov: trial adverse events — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **Gate A run 2026-10-20 → KEEP-NARROW (GLP-1 snapshot) / PARK (opioids), your approval pending** · your hand-verification pending · Access: [00-source-access-guide.md](00-source-access-guide.md)_

📄 **Atlas pages:** [atlas/clinicaltrials.html](../atlas/clinicaltrials.html) ([online](https://claude.ai/artifact/2EtXRb4NjveGX1qBEm7ixd)) · daily FAERS check [atlas/aems-daily.html](../atlas/aems-daily.html) ([online](https://claude.ai/artifact/QNBnDFQRxCZs98PkuRah5x)) · script: [ctgov_gate.py](../../../prototypes/explore/ctgov_gate.py)

## In one line
One record = **one study**. If results are posted, it lists side effects **per arm** (drug vs placebo) with **how many people were at risk**. That's a real denominator, which FAERS doesn't have.

## How to navigate
| Step | Browser | API (v2) |
|---|---|---|
| Find studies | clinicaltrials.gov → Intervention "semaglutide" → filter "With results" | `api/v2/studies?query.intr=semaglutide&aggFilters=results:with` |
| Read side effects | Study page → "Results" tab → "Adverse Events" | `resultsSection.adverseEventsModule` |
| Count only | — | add `&countTotal=true&pageSize=1` |

**Local:** `prototypes/data/<drug>/trials_with_results.json` (20 studies per drug).

## Record shape
```
study
├── protocolSection
│   ├── identificationModule.nctId, briefTitle
│   └── armsInterventionsModule.interventions[].name   ← drug NAME only (text)
└── resultsSection.adverseEventsModule
    ├── timeFrame, frequencyThreshold
    ├── eventGroups[]            ← arms: title, numAtRisk, seriousNumAffected, otherNumAffected
    ├── seriousEvents[]          ← term, organSystem, sourceVocabulary, stats[] per arm
    └── otherEvents[]            ← same shape
```

## Real example (semaglutide, NCT04251156)
| Arm | At risk | Serious AE | Other AE |
|---|---|---|---|
| Sema 2.4 mg | 249 | 14 | 180 |
| Placebo | 126 | 8 | 57 |

Event row: `"Abdominal distension"` · Gastrointestinal disorders · **MedDRA 25** · sema 25/249 vs placebo 1/126.
**What to notice:** the terms are **MedDRA**, the same vocabulary as FAERS. Matching trial events to FAERS reactions is a direct string match.

## Volumes
morphine 543 · fentanyl 299 · oxycodone 224 · buprenorphine 223 · liraglutide 144 · methadone 140 · exenatide 128 · hydromorphone 113 · semaglutide 109 · hydrocodone 72 · tramadol 67 · dulaglutide 61 · tirzepatide 47 (studies with results).

## Mess found
| Issue | Register |
|---|---|
| Many hits are not about safety of *our* drug (bioequivalence, anaesthesia comparisons where the opioid is background) | DQ32 |
| Drug identity is text only → RxNorm approximateTerm | DQ02 |
| `frequencyThreshold` (often 5%) hides rare events in "otherEvents" | DQ32 |

## How to use it well
1. Use as a **second opinion** on a signal: "Was this reaction also seen in trials, and more than placebo?"
2. Keep only studies where our drug is an **experimental arm**.
3. Low priority for the pilot: first to cut if time runs short (G8).

## ✅ Your hand-verification
- [ ] Open NCT04251156 → Adverse Events tab and find "Abdominal distension"
- [ ] Find one opioid study where the opioid is just background

---

## Gate A result (2026-10-20, timebox 2 h, used ~1.5 h)

**TL;DR:** The gate passes for GLP-1s and fails for opioids. Trials confirm both semaglutide signals (NAION 5 useful trials, gastric emptying 8). Oxycodone signals get 0 to 1 useful trials each. **Recommend: KEEP-NARROW** = one-time GLP-1 snapshot (about 2 h), still cut #1. **PARK** opioid trials.

Run: `python3 -I prototypes/explore/ctgov_gate.py <scratch_dir>` (13.1 s, 33 MB raw, cache kept out of the repo).

### Funnel (all 13 drugs, measured)
| Step | Studies |
|---|---|
| Studies with posted results (search hits) | 2,170 |
| …that name our drug in an arm or intervention | 1,615 |
| …not a bioequivalence / PK / abuse-liability study | 1,494 |
| …drug not given to every arm | 1,162 |
| …drug is the one being tested (not only the comparator) | 754 |
| …side effects can be tied to the drug arm | **687** ("about our drug's safety") |
| …and there is a control arm | 505 |

GLP-1: 301 of 489 hits are about the drug's safety (62%). Opioids: 386 of 1,681 (23%). Morphine is worst: 62 of 543 (11%).

### Signal test (unique trials)
"Useful" = trial tests our drug, the term appears in the drug arm, and the drug-arm rate is higher than control.

| FAERS signal | Trials naming term | Test our drug, case in drug arm | **Useful** |
|---|---|---|---|
| semaglutide · Optic ischaemic neuropathy (NAION) | 7 | 6 | **5** |
| semaglutide · Impaired gastric emptying | 9 | 8 | **8** |
| oxycodone · Pain | 16 | 2 | 0 |
| oxycodone · Rash | 14 | 2 | 1 |
| oxycodone · Hypersensitivity (+ Drug hypersensitivity) | 3 | 2 | 1 |
| oxycodone · Joint swelling | 5 | 0 | 0 |
| oxycodone · Hypertension (+ Blood pressure increased) | 15 | 4 | 1 |

Crude sums across controlled semaglutide trials (not a meta-analysis): NAION **8 / 13,836 vs 1 / 12,170**. Gastric emptying **14 / 20,161 vs 1 / 19,606**.
Class check, useful trials: NAION in tirzepatide 1, dulaglutide 1. Gastric emptying in liraglutide 3, dulaglutide 3, exenatide 2, tirzepatide 1.
Why oxycodone fails: its top FAERS terms (rash, joint swelling) look driven by co-medicated rheumatology patients, so trials cannot confirm them.

### New mess found (adds to DQ32)
| Issue | Measured |
|---|---|
| Search expands to other drugs | 288 / 543 morphine hits never name morphine (hydromorphone 69, oxymorphone 14) |
| Placebo arms carry the drug name ("Placebo (semaglutide)") | Naïve match put 43 semaglutide trials in "drug in every arm"; 8 after the fix |
| Arm titles abbreviated ("Sema 2.4 mg", "Group A") | 108 drug-tested studies with no side-effect group tied to our drug |
| `sourceVocabulary` is free text | 201 spellings; 7,851 rows blank; 2,095 CTCAE; 202 COSTART; MedDRA versions 2.0–29.0 |
| 5% threshold for non-serious events | 851 studies; serious events are always listed |
| Changes slowly | Results first posted: 3 in last 30 days, 149 in last year (all 2,170 studies) |

### 🩺 PV SME / 💊 Safety officer lens
- 🩺 Trials are a fair second opinion for **serious, rare** events, because serious events are always listed. Show counts per trial. Never show a pooled rate as an incidence.
- 💊 "Also seen in 5 controlled trials (8 on drug vs 1 on control)", with each trial clickable, makes the NAION flag easier to trust.

---

## Proposed for the logs (not applied: needs your OK)
_This session does not edit DECISIONS.md, the data-issues register, BACKLOG or COMPASS. Copy these rows in if you agree. Numbers are suggestions; use the next free ones._

**Decision (DECISIONS.md)**
| # | Date | Decision | Why | Rejected | Status |
|---|---|---|---|---|---|
| D032 | 2026-10-20 | ClinicalTrials.gov: **KEEP-NARROW** as a one-time GLP-1 snapshot of serious events, shown as "Seen in trials" evidence on a Signal (`TrialEvidence`: signal · NCT · drug n/N · control n/N · link). **PARK** opioid trials. Still cut #1. | Gate A: NAION 5 useful trials, gastric emptying 8; oxycodone 0–1; only 23% of opioid hits about the drug | Weekly or daily pipeline (3 new result postings a month); opioid trials | Proposed |
| D033 | 2026-10-20 | Daily FAERS: **option (b)**. FAERS stays quarterly (D029 holds). Optional manual one-day dashboard export for the demo, shown as "not yet in signal math". Roadmap: daily feed once FDA documents an AEMS API. | No documented API or export URL; dashboard is UI-only behind a disclaimer; openFDA stalled at 2026-07-30 | (a) daily feed stretch goal (would need scraping) | Proposed |

**Learnings (DECISIONS.md → Learnings)**
| Date | What we realised | What it changed |
|---|---|---|
| 2026-10-20 | Placebo arms are named after the drug ("Placebo (semaglutide)"); naïve matching hides placebo-controlled trials | D032 arm rules; DQ42 |
| 2026-10-20 | CT.gov search expands to other drugs (morphine → hydromorphone); 53% of morphine hits never name morphine | D032; DQ43 |
| 2026-10-20 | Trial MedDRA terms match FAERS PTs exactly for both semaglutide signals | D032 (no term mapping needed) |
| 2026-10-20 | FDA publishes FAERS daily, but only inside the dashboard; no API documented 7 months after AEMS launch | D033 |

**Data issues (data-issues-register.md)**
| ID | Source | Issue | Impact | Handling | Status |
|---|---|---|---|---|---|
| DQ42 | Trials | Placebo arms and interventions carry the drug name; arm titles abbreviated ("Sema 2.4 mg") | Wrong arm attribution (43 → 8 "all arms" for semaglutide) | Strip "placebo (drug)" patterns; use group description as fallback; PLACEBO_COMPARATOR arms are never drug arms | ✅ Seen 2026-10-20 |
| DQ43 | Trials | `query.intr` expands to other drugs (hydromorphone, oxymorphone) | 288/543 morphine hits not about morphine | Re-check our drug by name + brand in arms/interventions | ✅ Seen 2026-10-20 |
| DQ44 | Trials | `sourceVocabulary` free text: 201 spellings, 7,851 blank, CTCAE/COSTART mixed in | Cannot rely on the field | Match on term text only; keep MedDRA-PT exact matches | ✅ Seen 2026-10-20 |
| DQ45 | FAERS | Daily dashboard data has no documented API; export is manual, "limited set" of columns | No automated daily feed | D033: quarterly in pipeline; manual snapshot only for show | ✅ Seen 2026-10-20 |

**Backlog (BACKLOG.md)**
| ID | Task | Owner | Hours | Due | Status |
|---|---|---|---|---|---|
| E4 | Trials gate + AEMS check | Claude | 2 (of 3 budgeted) | Oct 22 | ✅ Done 2026-10-20 |
| B-new | GLP-1 TrialEvidence snapshot: CSV export (Claude 0.25 h) + Foundry upload + link to Signal (you ~1.5 h) | Claude + you | ~2 | Oct 28 | ⚪ (cut #1) |
| B-new | Optional: manual one-day AEMS dashboard export for the demo | You | 0.5 | Nov 1 | ⚪ (optional) |

**Compass:** blocker "AEMS: openFDA API stuck" → resolved as "no daily API; quarterly + optional manual snapshot (D033)".
