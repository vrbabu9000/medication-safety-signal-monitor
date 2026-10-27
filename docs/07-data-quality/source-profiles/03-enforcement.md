# FDA enforcement reports: recalls — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Access: [00-source-access-guide.md](00-source-access-guide.md)_

## In one line
One record = **one recalled product** (one recall event can contain several products). The record is **flat**, but the drug is named only in **free text**.

## How to navigate
| Step | Browser | API |
|---|---|---|
| 1. Search | accessdata.fda.gov Enforcement Report → product "fentanyl" | `…/drug/enforcement.json?search=product_description:"fentanyl"&limit=5` |
| 2. Active only | filter Status = Ongoing | add `+AND+status:"Ongoing"` |
| 3. Summaries | — | `count=classification.exact`, `count=status.exact` |

**Local:** `prototypes/data/<drug>/recalls_sample.json`.

## Record shape
```
recall
├── recall_number        ← e.g. D-0646-2023 (our key)
├── event_id             ← groups products from one recall event
├── status               ← Ongoing / Completed / Terminated
├── classification       ← Class I (serious harm) / II / III
├── recalling_firm
├── product_description  ← FREE TEXT: drug, strength, maker, often an NDC inside
├── reason_for_recall    ← free text
├── code_info            ← lots, expiry dates
├── recall_initiation_date, report_date, termination_date
└── openfda              ← EMPTY in 99 of 100 samples
```

## Real example (fentanyl, Ongoing)
```json
{ "recall_number": "D-0646-2023", "status": "Ongoing", "classification": "Class II",
  "recalling_firm": "Apollo Care, LLC",
  "product_description": "FentaNYL 500 mcg (2mcg/mL) and Ropivacaine HCL 250 mg (0.1%) added to 250 mL 0.9% Sodium Chloride Injection ... NDC 71170-950-25",
  "reason_for_recall": "Lack of Assurance of Sterility",
  "code_info": "Lot #: AC-016644, Exp. Date 05/08/2023; ...",
  "report_date": "20230524", "openfda": {} }
```
**What to notice:**
1. It's a **combination** product (fentanyl + ropivacaine) from a **compounding** firm.
2. Its NDC is **not in RxNorm** (status UNKNOWN). Only text matching finds the ingredients.
3. It's "Ongoing" since 2023.

## Categories (fentanyl sample of 100 / semaglutide sample of 54)
| | fentanyl | semaglutide |
|---|---|---|
| Status | 8 Ongoing · 92 Terminated | **47 Ongoing** · 3 Completed · 4 Terminated |
| Class | 7 I · 91 II · 2 III | 54 II |
| Reason: sterility/contamination | 82 | 40 |
| Reason: potency | 8 | 3 |
| Compounding/outsourcing mentioned | 37 | 12 |
| NDC-like code in text | 75 | 32 |

## Join keys
- **NDC parsed from text** → RxNorm `ndcstatus` → RxCUI (fails for many compounded NDCs).
- Fallback: product text → RxNorm `approximateTerm` → ingredients (worked for the example: 1009056).
- No direct link to FAERS or labels.

## Mess found
| Issue | Register |
|---|---|
| `openfda` empty in 99% of records | DQ11 |
| Compounded NDCs unknown to RxNorm | DQ29 |
| Combination products → several ingredients | DQ16 |
| "Ongoing" can last years: does it mean "active" for the officer? | DQ30 (needs a rule) |

## How to use it well
1. Pull weekly: an **incremental** load by `report_date`.
2. Identity: NDC first, then text match. Put anything unmatched on a **review list**, never drop it silently.
3. Show "Ongoing" with its age, and highlight Class I.

## ✅ Your hand-verification
- [ ] Find recall D-0646-2023 in the FDA web search
- [ ] Pick 5 recalls and check by eye: does the text match the drug?
- [ ] Look up one recall NDC in RxNav

---

## Additions 2026-10-20 — full measurement (recalls atlas session)
_Atlas page: [enforcement.html](../atlas/enforcement.html) · artifact: https://claude.ai/artifact/FzVavqD4ppzksPT1uodbgQ · Companion: [08-ndc-directory.md](08-ndc-directory.md)_
_Every number below comes from [`prototypes/explore/recalls_ndc_atlas.py`](../../../prototypes/explore/recalls_ndc_atlas.py) on the openFDA **bulk** file (export 2026-10-14, all 18,010 drug recalls since 2012). Results: `prototypes/data/_recalls/atlas_results.json` (git-ignored)._

### Corrections to the sample-based profile above
| Above (100-row samples) | Measured on all rows | Why it moved |
|---|---|---|
| `openfda` empty in 99 of 100 | Filled on **74 of 890** (8.3%); 18 of 116 Ongoing; 17.4% for all drugs | Larger base; Fresenius / big-manufacturer rows have it |
| NDC in text: 75/100 fentanyl, 32/54 semaglutide | **527 of 890 (59.2%)** overall; fentanyl 248/357, semaglutide 30/54 | Full history incl. 2015 PharMEDium "product codes" |

### 1. All recalls for our 13 (whole-word match on `product_description`)
- **890 rows, 238 events.** Brands add 1 row (Percocet). 2 apomorphine rows correctly excluded.
- Status: Terminated 767 · **Ongoing 116** · Completed 7. Class: II 780 · III 62 · **I 48** (6 Ongoing).
- Year started: peaks 2015 (158), 2016 (134); 2019 108 · 2023 93 · 2025 52 · 2026 34.
- Reason: sterility/contamination **608 (68%)** · potency 69 · particulate 57 · labeling 52 · impurity 34 · cGMP/container/dissolution/other 70.
- **Compounded 557 (63%)**: 527 by text, 82 by NDC labeler on FDA's 503B list, 52 both. 64 of 116 Ongoing.
- Combinations: 297 rows mix one of ours with another drug; 30 rows name two of our 13.
- Events: max 103 rows (The Compounding Pharmacy of America); 140 events have 1 row. All "Voluntary: Firm initiated".

| Ingredient | Rows | Events | Ongoing | Class I | Compounded | With NDC |
|---|---|---|---|---|---|---|
| fentanyl | 357 | 90 | 22 | 18 | 258 | 248 |
| hydromorphone | 189 | 54 | 3 | 12 | 140 | 84 |
| morphine | 189 | 68 | 7 | 15 | 127 | 65 |
| semaglutide | 54 | 20 | 47 | 0 | 33 | 30 |
| buprenorphine | 32 | 26 | 6 | 0 | 7 | 24 |
| oxycodone | 25 | 23 | 4 | 1 | 0 | 24 |
| hydrocodone | 22 | 20 | 1 | 4 | 0 | 22 |
| tirzepatide | 21 | 8 | 21 | 1 | 10 | 8 |
| tramadol | 12 | 12 | 2 | 0 | 1 | 11 |
| methadone | 11 | 6 | 1 | 0 | 7 | 4 |
| liraglutide | 4 | 2 | 1 | 1 | 0 | 4 |
| dulaglutide | 3 | 2 | 0 | 0 | 0 | 3 |
| exenatide | 1 | 1 | 1 | 0 | 0 | 1 |

### 2. NDC extraction from free text
- 527 / 890 rows (59.2%) have an NDC; 529 contain the word "NDC" (3 unparsed: "ALL NDCs", lettered lists).
- Shapes: 5-3-2 **313** · 5-4-2 (11-digit) **158** · 4-4-2 **91** · 5-4-1 **63** · 11 digits no dashes 6 · 10 digits no dashes 4 (ambiguous, 3 possible splits) · product code only 1.
- 63 rows list 2+ NDCs. 552 distinct NDCs.
- Compounded rows: 283 / 557 have an NDC (51%); not compounded 244 / 333 (73%). Worst year 2015: 14 / 158.

### 3. Match rates (527 rows with an NDC)
| Route | Rows | Share |
|---|---|---|
| RxNorm `ndcstatus` → any RxCUI | 396 | 75% (ALIEN 207 · ACTIVE 114 · OBSOLETE 75) |
| …RxNorm name confirms our ingredient | 315 | 60% (78 named "PROPRIETARY") |
| NDC Directory (package 182 + product 11) | 193 | 37% (listed 89 · excluded 75 · 503B 24 · unfinished 5) |
| …with application number | 150 | 28% |
| RxNorm **or** directory | 414 | 79% |
| **Fails everywhere** | **113** | 21% · 106 NDCs · 81 compounded · **28 Ongoing** |

- Compounded: RxNorm 190/283 (67%), directory 26/283 (9%). Not compounded: 206/244 (84%), 167/244 (68%).
- Ongoing: 116 → 80 with NDC → 36 RxCUI → **52 any match (45%)**.
- Fail-everywhere firms: Pharmakon 27 · ProRx 14 · SCA 9 · Apollo Care 8 (all 8 Ongoing examples are Apollo Care semaglutide vials, `71170-8xx`/`71170-7xx`).
- **Text-only fallback** (494 rows without an RxNorm NDC hit): whole-word ingredient match 494/494 (by construction). RxNorm `approximateTerm` top answer: right ingredient 386 (78%), right strength only **96 / 239 (40%)**, 175 answers are retired concepts. → text gets us to the Drug, never to a strength or Product.
- NDC reuse: D-0153-2017 printed `0409-4093-32` (Hospira fentanyl); that code is a chromium product today.

### 4. "Active": how long Ongoing lasts
- 116 Ongoing. Age from initiation: < 3 mo 16 · 3–6 mo 3 · 6–12 mo 20 · **1–2 y 48** · 2–3 y 15 · > 3 y 14. Median **459 days**; oldest D-057-2013 (started 2012-09-10).
- Closed recalls took a median **591 days** to terminate (p75 707, p90 1,046). "Ongoing" mostly means "FDA paperwork not done".
- Expiry/BUD dates parsed from `code_info` on 65% of all rows. Ongoing: every lot expired **50** · a lot unexpired 28 · "all lots" 18 · none found 20.
- 💊 Safety officer lens (persona, not an interview): "If every lot expired, it's not on my shelf; don't count it, but don't hide it."
- **Proposed rule:** Active = Ongoing **and** (a lot unexpired, or "all lots", or no expiry found). "Ongoing · lots expired" = collapsed list below. Terminated/Completed = closed.
- Result: **66 Active rows = 29 events** (semaglutide 31, tirzepatide 12, fentanyl 7, buprenorphine 5, oxycodone 3, hydromorphone 2, morphine 2, 1 each methadone/tramadol/liraglutide/exenatide); 2 Class I. 3 Active rows are > 3 years old (2 Akorn "all lots", 1 Apollo Care no expiry) → hand-check.

### 5. How often it changes (input to the ChangeEvent feed)
- Our 13, last 52 weeks: **49 new rows / 22 new events**; mean 0.9 rows a week; **33 of 53 weeks with nothing new**; max 11 in one week (one Apollo Care event, week of 2026-08-17). 3 years: 125 rows in 157 weeks.
- Terminations in the last 52 weeks: **4** (D-0296/0304/0308-2023, D-0385-2025). All were reported in 2023/2025 and closed in 2026: **updates land on old rows and `report_date` doesn't move**.
- No "last modified" field. API pull (485 rows, data 2026-10-07) vs bulk (2026-10-14): **0 rows changed**.
- All drugs: 809 new rows in 52 weeks (15.3 a week). Every `report_date` is a Wednesday. Initiation → report median 42 days. Newest report in the file 2026-10-07 (13 days before today).

## Proposed for the logs
_Not yet in DECISIONS.md or the register (this session may not edit them). IDs are placeholders: renumber after the sibling atlas sessions (they used D032–D033, DQ42–DQ45)._

**Decisions**
| ID | Decision | Evidence | Alternative |
|---|---|---|---|
| D-R1 | Recalls load = **weekly full snapshot + diff** on `recall_number` (status, class, termination date) | terminations land on old rows; no modified date; file is 28 MB | Append by `report_date` (misses every closure) |
| D-R2 | Recall identity order: NDC → NDC Directory (Product) → RxNorm (RxCUI) → whole-word text (Drug). Link to Drug always, Product when found. RxNorm ALIEN accepted only if its name confirms the ingredient; "PROPRIETARY" = no match. Never derive strength/Product from text. Unmatched → review list | 79% NDC match; 28 Ongoing fail everywhere; approximateTerm strength right 40% | Text → RxNorm approximateTerm for everything |
| D-R3 | **"Active recall"** = Ongoing and (lot unexpired, or "all lots", or no expiry found). "Ongoing · lots expired" shown collapsed, not counted. Show class, age, newest lot expiry | 50 / 116 Ongoing have every lot expired; median closure 591 days | Active = status Ongoing (116 rows, many years stale) |
| D-R4 | Show recall **events** (29) with product rows inside; Class I first; ChangeEvent types `RecallNew`, `RecallStatusChanged`, `RecallClassChanged` (~1 a week, bursts of 10+) | 890 rows = 238 events; 11-row single-event bursts | One card per row |

**Data issues**
| ID | Source | Issue | Impact | Fix |
|---|---|---|---|---|
| DQ-R1 | Recalls / NDC Dir | NDC reused for another product (`0409-4093-32` fentanyl → chromium) | wrong Product | resolve as of recall date; ingredient must agree with text |
| DQ-R2 | Recalls / RxNorm | RxNorm returns "PROPRIETARY" names (78 hits) and ALIEN status (207 of 396 hits) | unverifiable RxCUI | accept only name-confirmed hits |
| DQ-R3 | Recalls | Status changes land on old rows; no modified date | append-only load misses closures | snapshot + diff (D-R1) |
| DQ-R4 | Recalls | Bulk data 13 days behind (newest report 2026-10-07 on 2026-10-20) | "as of" date matters | show source "as of" (D028) |
| DQ-R5 | Recalls | Expiry parsed by regex, unverified; 3 Active rows > 3 years old | wrong Active/expired split | hand-check 5 rows + the 3 old ones |
| DQ11 update | Recalls | Measured: 59.2% of rows carry an NDC; 5 shapes; 4 ambiguous 10-digit | — | — |
| DQ29 update | Recalls | Measured: 113 rows / 106 NDCs fail RxNorm and the directory; 81 compounded; 28 Ongoing | — | review list |
| DQ30 update | Recalls | Rule proposed (D-R3); median Ongoing age 459 days | — | — |

**Learnings**
- Recalls are mostly a **compounding** story for our 13 (63% of rows; 64 of 116 Ongoing). The approved-product path (NDC → RxNorm/Directory) works well (84%); the compounded path doesn't (directory 9%).
- `code_info` expiry dates are a better "still on the shelf?" signal than recall status or age.

### ✅ Your hand-verification (additions)
- [ ] Open D-0788-2026 and D-0748-2026 on the FDA Enforcement Report site
- [ ] Check 5 "lots expired" rows by eye
- [ ] Look up `71170-811-02` in RxNav (expect UNKNOWN)
