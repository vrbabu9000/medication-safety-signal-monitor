# Drugs@FDA: approved applications (the Product bridge) — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Atlas page: [drugsatfda.html](../atlas/drugsatfda.html) ([online](https://claude.ai/artifact/6tbBfCLe1SfWDmgV7unKsY)) · Script: [identity_atlas.py](../../../prototypes/explore/identity_atlas.py) · Numbers: `prototypes/data/_identity/facts.json`_

## In one line
FDA's list of every approved **application** (NDA brand · ANDA generic · BLA biologic), with its products, strengths and sponsor. FAERS `nda_num` points at it, so it is the bridge **FAERS row → Product → label**.

## Access
| | fda.gov "Drugs@FDA Data Files" (use this) | openFDA `drug/drugsfda` |
|---|---|---|
| Format | 1 zip, 12 tab-separated tables, CRLF | 1 JSON file, nested, + `openfda` block |
| Size | 6.1 MB (`datdaf20261020.zip`) | 8.8 MB zip / 124 MB JSON, 29,390 records |
| Update | "each morning, Monday through Friday" (FDA page); files stamped 2026-10-19 | last_updated 2026-10-16 (≥4 days behind) |
| Auth | none | none |

Tables we need: `Applications` 29,405 (NDA 5,905 · ANDA 23,015 · BLA 485) · `Products` 51,904 · `MarketingStatus` 52,513 · `Submissions` 194,236 · `ApplicationDocs` 81,303.

## Record shape
```
Application  ApplNo 209637 · NDA · sponsor NOVO
 ├── Product 001…007   form, strength, DrugName OZEMPIC, ActiveIngredient SEMAGLUTIDE
 │     └── MarketingStatus   Prescription / OTC / Discontinued / Tentative
 └── Submission        ORIG or SUPPL n · class (LABELING, REMS…) · status AP/TA · date
```
FAERS gives only the application, so **Product = application**, not strength.

## Measured (2026 Q1 + Q2 FAERS, suspect rows PS/SS/I of our 13, rows not reports)
| Measure | Result |
|---|---|
| Suspect rows | 142,035 |
| Reach a Product via `nda_num` (pad to 6, ingredient must match) | **103,349 (72.8%)** |
| `nda_num` blank | 38,228 (26.9%) |
| + unique-brand fallback for blank rows | +14,009 → **82.6%** |
| 8 opioids / 5 GLP-1 | **37.4% (40.2% with brand)** / 82.4% (94.1%) |
| Worst | hydromorphone 18.9%, morphine 29.6%, tramadol 30.8% |
| Unknown number (incl. `99` placeholder 263 rows) | 387 rows |
| Number holds another ingredient (e.g. 050273 tetracycline on buprenorphine) | 64 rows |
| **ZEPBOUND rows carrying Mounjaro's 215866** | **40,597 suspect rows** (all Zepbound rows: 40,610 on 215866, 1 on its own 217806) |
| Applications for our 13 in Drugs@FDA / reached from FAERS | 664 / 241 |
| Reached applications with a DailyMed label | 201/241 (83.4%) · **99.1% of rows** · 35 of 40 missing are discontinued |
| Still-marketed applications with a label | 237/256 (92.6%) |
| Applications with >1 label (repackagers) | 128 of 201 |
| openFDA `openfda.spl_set_id` filled (reached apps) | 161/241 — empty for Ozempic, Wegovy, Hysingla, Actiq |
| Label XML carries the application number in `<approval><id extension=…>` | 6/6 checked; Wegovy label lists 2 applications |

## Mess found
1. **Opioid reports rarely name the product.** Blank `nda_num` 62–81% for 5 of 8 opioids; blank rows use generic names that fit dozens of generic applications.
2. **`nda_num` ≠ product used:** Zepbound → Mounjaro (40,597), Victoza → Saxenda (58), Subutex → Suboxone (13).
3. **Leading zeros dropped** in FAERS (61,336 five-digit numbers match only after padding).
4. **Ingredient spellings** the walkthrough salt list misses: `EXENATIDE SYNTHETIC` (all exenatide), `HYDROCODONE POLISTIREX`.
5. **One brand → many applications** (OZEMPIC = injection 209637 + tablet 213051; WEGOVY = 215256 + 218316). **One label → many applications** (Wegovy).
6. **openFDA harmonised fields empty** for our biggest products; openFDA label search by application misses Novo's own Ozempic label.
7. **Tentative approvals** (status TA) look like new applications but can't be sold (e.g. generic semaglutide ANDA 220314).

## How often it changes (measured)
- Our 13: **715 FDA actions in 365 days** on 349 applications (396 labeling, 284 REMS, 17 new applications, 1 tentative).
- Comes in **waves**: 22 Dec 2025 (195 opioid labeling approvals in a day) and 18 Jun 2026 (255 REMS approvals in a day). Normal month: 4–35.
- One lag example: Ozempic labeling supplement 44 approved 2026-08-27; DailyMed still shows Novo label v20 of 2026-06-10. **Unverified as a pattern** (labels session).

## ✅ Your hand-verification
- [ ] Open Drugs@FDA for [215866](https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=215866) (Mounjaro) and [217806](https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=217806) (Zepbound): separate applications
- [ ] In DailyMed, search "Ozempic": 1 Novo label + 5 A-S Medication repackager labels on NDA209637
- [ ] Open the Wegovy label XML and find both NDA215256 and NDA218316 in `<approval>`

---

## Proposed for the logs
_For the main session to merge into DECISIONS.md and the data-issues register. Numbers are placeholders (Dxxx / DQxx); assign real ones on merge._

### Proposed decisions
| # | Decision | Why (evidence) | Rejected |
|---|---|---|---|
| Dp1 | **Product = one FDA application** (`ApplType+ApplNo`, e.g. NDA209637), sourced from the fda.gov Drugs@FDA zip | FAERS carries only the application; zip is fresher than openFDA (Oct 19 vs Oct 16) | Strength-level product (not reachable); openFDA drugsfda (staler, empty harmonised fields) |
| Dp2 | **FAERS → Product rule:** pad `nda_num` to 6; accept only if application ingredient = row's RxNorm ingredient; else Product unknown, Drug still known | 61,336 short numbers; 64 rows point at another ingredient; `99` placeholder 263 rows | Trust `nda_num` blindly |
| Dp3 | **Brand beats number:** if drugname is a brand owned by exactly one application of the same ingredient and `nda_num` disagrees, use the brand's application; tag `nda_overridden` | 40,597 Zepbound rows on Mounjaro's 215866 | Keep the reported number (wrong product + wrong label for 54% of tirzepatide rows) |
| Dp4 | **Blank `nda_num`:** unique-brand fallback only; never guess a generic maker | +14,009 rows (GLP-1 82→94%); opioids barely move (37→40%) | Pick "most common ANDA" (invents provenance) |
| Dp5 | **Signals at Drug level; Product is a drill-down** showing "% of reports with a known product" (refines D027) | Opioids reach a Product for only ~40% of rows | Product-level signals |
| Dp6 | **Application ↔ label link from the label's own `<approval>` block**, DailyMed `application_number` search as cross-check; many-to-many; reference label = sponsor's own, else newest | 6/6 labels carry it; Wegovy label has 2 apps; openFDA misses Novo's Ozempic label | openFDA `spl_set_id` (empty for Ozempic, Wegovy) |
| Dp7 | **Ingest:** reload the 6 MB zip in full each weekday; diff `Submissions` for ChangeEvents grouped by day + class; ignore status TA as "new product" | Waves of 195 / 255 actions in one day; TA = not marketable | Incremental logic (not needed at this size) |

### Proposed data issues
| # | Source | Issue | Impact | Fix |
|---|---|---|---|---|
| DQp1 | FAERS × Drugs@FDA | `nda_num` blank on 26.9% of our suspect rows; opioids 62% (hydromorphone 81%) | Product unknown for most opioid reports | Dp4, Dp5 |
| DQp2 | FAERS × Drugs@FDA | ZEPBOUND rows carry Mounjaro's 215866 (40,610 vs 1 on 217806); also Victoza→Saxenda, Subutex→Suboxone | Wrong product + wrong reference label | Dp3 |
| DQp3 | FAERS | Leading zeros dropped from `nda_num`; `99` placeholder; 7 numbers > 6 digits | Join misses | Pad to 6; `99` = unknown |
| DQp4 | Drugs@FDA | Ingredient spellings `SYNTHETIC` (exenatide), `POLISTIREX` (hydrocodone) not in salt list | Exenatide had 0 applications before the fix | Add to salt list |
| DQp5 | openFDA | `openfda` harmonised block empty for Ozempic, Wegovy, Hysingla, Actiq; label search by application misses Novo's Ozempic label | Silent label misses | Dp6 |
| DQp6 | Drugs@FDA × DailyMed | Label ↔ application many-to-many (Wegovy label = 2 apps; Ozempic app = 6 labels incl. 5 repackagers) | Wrong label picked | Dp6 reference-label rule |
| DQp7 | Drugs@FDA | Class-wide waves (195 / 255 actions in one day) | Alert flood on "what changed" | Group ChangeEvents (Dp7) |

### Learnings
| Date | Realised | Changes |
|---|---|---|
| 2026-10-20 | `nda_num` is the reporter's application number, not proof of the product used (Zepbound case) | Product rule needs a brand override (Dp3) |
| 2026-10-20 | Product reach is very different by class: GLP-1 ~94%, opioids ~40% | Product can't carry signals (Dp5) |
