# NDC Directory (FDA): structure report

_Status: 🟡 Profiled by Claude 2026-10-20 (recalls atlas session) · **your hand-verification pending** · Design-thinking stage: **Define**_
_Atlas page: [ndc-directory.html](../atlas/ndc-directory.html) · artifact: https://claude.ai/artifact/S7DoYxF8ySdgqmdy7JzNqB · Companion: [enforcement.html](../atlas/enforcement.html)_
_Every number below comes from [`prototypes/explore/recalls_ndc_atlas.py`](../../../prototypes/explore/recalls_ndc_atlas.py) (results: `prototypes/data/_recalls/atlas_results.json`, git-ignored)._

## In one line
An NDC (National Drug Code) is the code on every US drug package. The NDC Directory is FDA's list of them, in **four separate files**. We use it for one job: turn a recalled package code into a **Product** (application number) and an **ingredient**.

## Access
| File | URL | One row = | Rows | Dated | Lines not UTF-8 |
|---|---|---|---|---|---|
| Listed products | `accessdata.fda.gov/cder/ndctext.zip` → product.txt | product | 116,501 | 2026-10-20 | 342 |
| Listed packages | same zip → package.txt | package | 219,045 | 2026-10-20 | 0 |
| Excluded | `…/cder/ndc_excluded.zip` → Products_/Packages_excluded.txt | removed product / package | 206,937 / 385,271 | 2026-10-20 | 694 / 0 |
| Unfinished | `…/cder/ndc_unfinished.zip` | bulk product / package | 21,701 / 37,612 | 2026-10-20 | 97 / 0 |
| Compounders (503B) | `…/cder/compounders_ndc_directory.zip` | package per half-year report | 4,836 | 2026-09-18 | 0 |
| openFDA copy | `download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip` | product + packages | 138,319 | 2026-10-16 | — |

- Tab-separated, header row, **Latin-1** (not UTF-8). No login. All six zips ≈ 78 MB.
- FDA rebuilds the text files daily (time stamp 04:12). The openFDA JSON = listed + unfinished only.
- Exclude-flag meanings (FDA product file definitions): **D** discontinued by firm · **I** inactivated by FDA · **U** listing certification expired · **E** removed for not fixing errors.

## Record shape
```
product.txt                         package.txt
├── PRODUCTID  (NDC _ SPL doc id)   ├── PRODUCTID  → product
├── PRODUCTNDC  e.g. 0169-4130      ├── NDCPACKAGECODE  e.g. 0169-4130-13
├── PROPRIETARYNAME / NONPROPRIETARY├── PACKAGEDESCRIPTION (names inner codes too)
├── DOSAGEFORM, ROUTE               ├── START/ENDMARKETINGDATE
├── MARKETINGCATEGORYNAME (NDA/ANDA/BLA/…)  └── NDC_EXCLUDE_FLAG, SAMPLE_PACKAGE
├── APPLICATIONNUMBER  ← Product key (D027)
├── LABELERNAME, SUBSTANCENAME (";"-separated), strength, unit
├── PHARM_CLASSES, DEASCHEDULE
└── NDC_EXCLUDE_FLAG, LISTING_RECORD_CERTIFIED_THROUGH
```
Compounder file: same idea, one flat row per package, **no APPLICATIONNUMBER**, strength as free text (`ACTIVEINGREDIENTSINFO`), plus `REPORTINGPERIOD` (e.g. 2026-1).

## Real example (Ozempic)
```
0169-4130  Ozempic  semaglutide  INJECTION, SOLUTION  SUBCUTANEOUS  NDA  NDA209637
Novo Nordisk Pharmaceutical Industries, LP  SEMAGLUTIDE  1.34 mg/mL  flag N  certified through 20271231
package 0169-4130-13  "1 SYRINGE, PLASTIC in 1 CARTON (0169-4130-13) / 3 mL in 1 SYRINGE, PLASTIC (0169-4130-01)"
```
More real rows (503B semaglutide, excluded hydrocodone/APAP, bulk semaglutide powder) are on the atlas page, part 2.

## Categories (our 13 ingredients)
| | Products | Notes |
|---|---|---|
| Listed | 1,344 (3,182 packages) | ANDA 1,064 · NDA 227 · NDA AG 26 · unapproved 15 · BLA 12 · 141 labelers · 246 application numbers |
| Excluded | 2,408+ (7,164 packages) | name match only (no ingredient column) → lower bound · D 1,803 · I 602 · U 3 |
| 503B compounded | 224 (287 packages, 720 rows) | 33 firms · fentanyl 85, semaglutide 38, hydromorphone 36, tirzepatide 33, morphine 23 |
| Unfinished (bulk) | 464 | bulk ingredient 270 · bulk for compounding 105 · further processing 86 · export 3 · semaglutide 119, tirzepatide 114 |

Per ingredient (listed / excluded / 503B / unfinished): oxycodone 298/476/1/15 · hydrocodone 244/761/0/18 · buprenorphine 211/109/1/45 · morphine 154/277/23/13 · tramadol 143/360/0/22 · hydromorphone 74/97/36/19 · fentanyl 54/257/85/30 · tirzepatide 54/0/33/114 · methadone 50/71/3/12 · semaglutide 24/0/38/119 · liraglutide 23/0/4/40 · dulaglutide 11/0/0/8 · exenatide 4/0/0/9.

## Join keys
- **Package NDC (11-digit)** → product → `APPLICATIONNUMBER` (98.9% filled on our listed products; the 15 blanks are all "unapproved drug other") → Product object → label.
- `SUBSTANCENAME` → RxNorm ingredient → Drug object.
- RxNorm coverage (one package per product): listed **1,329 / 1,332 (99.8%)**, 503B **147 / 287 (51%, all ALIEN)**, unfinished **50 / 463 (11%)**.
- openFDA JSON adds `openfda.rxcui` (95.5%) and `spl_set_id` (95.8%) on our 1,344 finished products; 56 have an empty block.
- Recalls: 193 of 527 recall rows with an NDC are placed by the directory: listed 89 · excluded 75 · 503B 24 · unfinished 5 (183 agree on ingredient, 150 carry an application number).

## Mess found
| Issue | Measured | Register |
|---|---|---|
| Files are not valid UTF-8 | 342 / 694 / 97 lines | proposed DQ-R6 |
| Excluded file has no ingredient, generic name or form | 100% blank of 206,937 | proposed DQ-R7 |
| 503B codes not in the main file and mostly unknown to RxNorm | 0 / 287 in main file; 140 UNKNOWN, 146 ALIEN | DQ29 (now measured) |
| Same 503B package repeated each half-year | 720 rows → 287 packages | proposed DQ-R8 |
| NDC codes reused for a different product | `0409-4093-32`: Hospira fentanyl (recall D-0153-2017) → chromium today | proposed DQ-R1 |
| Three 10-digit shapes vs the 11-digit billing form | 4-4-2 / 5-3-2 / 5-4-1 | DQ11 |
| Combination products | 483 of 1,344 listed | DQ16 |

## Freshness and change rate
- FDA text files daily; openFDA JSON lags (2026-10-16 vs 2026-10-20). Compounder list half-yearly (file 2026-09-18, periods 2024-2 → 2026-1).
- JSON (Oct 16) vs text (Oct 20), all drugs: 514 product IDs appeared, 631 gone. By product code: **91 new, 208 gone**. The rest are new label versions (product ID = NDC + SPL document ID). Our 13: 6 appeared, 6 gone.
- New packages for our 13 in the last 52 weeks: **393** (7.6 a week, 44 of 52 weeks had one).
- 315 of our listed products are certified only to 2026-12-31; 30 have a (future) end date.

## How to use it well
1. Load all four FDA text files weekly with the recall load. Latin-1, all columns text.
2. Build one `ndc_reference` table: 11-digit NDC, code as printed, product NDC, application number, ingredients, labeler, list (listed / excluded D·I·U·E / 503B / unfinished), start/end dates.
3. Keep weekly snapshots so a recall NDC resolves **as of its recall date** (reuse).
4. Compounded = a Product with no application number (key = labeler + product code), tagged compounded.
5. Never show unfinished (bulk) products to the officer; keep them for lookups.

## Proposed for the logs
_Not yet in DECISIONS.md or the register (this session may not edit them). IDs are placeholders: renumber after the sibling atlas sessions (they used D032–D033, DQ42–DQ45)._

**Decisions**
| ID | Decision | Evidence | Alternative |
|---|---|---|---|
| D-R5 | Add the FDA NDC Directory (4 text files) as an **identity reference** for Package → Product. Weekly load, snapshots kept. | 193 of 527 recall NDCs placed only through it; 75 of those only in the excluded file | openFDA JSON only (lacks excluded + 503B lists; older) |
| D-R6 | **Compounded products are Products** without an application number (key = labeler + product code), tagged `compounded`, linked to Drug by ingredient name | 0 / 287 503B codes in main file; RxNorm UNKNOWN 140 / 287 | Drop compounded recalls (would lose 64 of 116 Ongoing) |
| D-R7 | Keep excluded listings, marked "no longer marketed"; keep unfinished (bulk) for lookups only | old recalls point to excluded codes (75 hits) | Main file only |

**Data issues**
| ID | Source | Issue | Impact | Fix |
|---|---|---|---|---|
| DQ-R1 | NDC Dir / Recalls | NDC codes reused across products (`0409-4093-32` fentanyl → chromium) | wrong product on a recall | resolve as of recall date from snapshots; check ingredient agrees with text |
| DQ-R6 | NDC Dir | Not valid UTF-8 (342 / 694 / 97 lines) | default parse fails | read Latin-1 |
| DQ-R7 | NDC Dir | Excluded file: ingredient / generic / form blank on 100% | can't select by ingredient | match by NDC only; name match is a lower bound |
| DQ-R8 | NDC Dir | 503B rows repeat each half-year (720 → 287 packages) | double counts | dedupe on package code, keep latest period |
| DQ29 update | NDC Dir / RxNorm | Now measured: 503B 140 / 287 UNKNOWN to RxNorm; recall NDCs failing everywhere 113 rows | — | see 03-enforcement |

**Learnings**
- The application number is filled on 98.9% of our listed products → it really can be the Product key (supports D027).
- The NDC Directory is four lists, not one. "Not in the NDC Directory" usually means "not in the main file".

## ✅ Your hand-verification
- [ ] Search `0169-4130` on FDA's NDC Directory web search: Ozempic, NDA209637?
- [ ] Search `0409-4093`: what product is it today?
- [ ] Open compounders_ndc_directory.txt and find `81375-600-03` (PQ Pharmacy semaglutide)
