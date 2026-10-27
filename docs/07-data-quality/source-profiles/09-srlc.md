# SrLC: FDA Safety-related Labeling Changes — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Atlas page: [srlc.html](../atlas/srlc.html) ([artifact](https://claude.ai/artifact/YG8DZckTruyALGUkiiycZK)) · Script: [label_atlas.py](../../../prototypes/explore/label_atlas.py) steps `srlc`, `srlcan`_

## In one line
One record = **one approved safety supplement for one product** (NDA/BLA), dated, listing the label sections it touched, with the added text **underlined**. It is the only source that says "this reaction joined the label on this date". Coverage: Jan 2016 onward.

## How to navigate
| Step | Browser | Script |
|---|---|---|
| 1. Find a product | accessdata.fda.gov/scripts/cder/safetylabelingchanges → "Drug Name Search" | POST `drug_name=semaglutide` to `index.cfm?event=searchResult.page` |
| 2. See its history | Click the product → entries by date, "Expand all" | GET `?event=searchdetail.page&DrugNameID=2183` |
| 3. Changes in a period | "Date Search" + section boxes | POST `date_range_from`, `date_range_to`, `section=BW,C,WP,AR,DI,USP,MG` |
| 4. Download | "Download Data" on the product page | GET `?event=downloadDetails.page&DrugNameID=2183` (CSV, broken — see below) |

No API. Scripted requests need a browser User-Agent and the session cookie from the start page (otherwise: "abuse detection" redirect).

**Local:** `prototypes/data/_labels/srlc/details.json` (104 products parsed), `date_search_90d.json`.

## Record shape
```
product (DrugNameID)  drug name · ingredient(s) · application no. · NDA/BLA
└── entry[]           approval date · SUPPL-n · label PDF link
    └── section[]     "6 Adverse Reactions" / "5 Warnings and Precautions" / "17 PCI/PI/MG" …
        └── text      HTML; additions in <u>…</u>; "…" marks omitted text
```

## Real example (Ozempic, NDA 209637, 11 entries)
| Approved | Supplement | Underlined in §6.2 | DailyMed version (days later) |
|---|---|---|---|
| 2023-09-22 | SUPPL-20 | Ileus | v14 (17) |
| 2025-01-28 | SUPPL-25 | cholecystitis, cholecystectomy · dysesthesia · alopecia | v16 (13) |
| 2025-10-14 | SUPPL-35 / 37 | intestinal obstruction, severe constipation incl. fecal impaction · acute kidney injury · headache | v17 (34) |
| 2026-06-01 | SUPPL-38 | acute pancreatitis and necrotizing pancreatitis | v20 (9) |

## Numbers (measured)
| Measure | Value |
|---|---|
| Products for our 13 (exact ingredient) | 101 (102 NDA + 2 BLA among all 104 found; 0 ANDA) |
| Entries since 2016 (de-duplicated) | 534 |
| 2025 entries / distinct approval dates | 70 / 9 (46 on Dec 22: opioid class update) |
| 2026 entries so far / dates | 13 / 8 |
| Our 13 in the last 90 days | 1 (Mounjaro, Aug 27) |
| All drugs, last 90 days | 146 entries, 21 database update dates |
| Approval → in SrLC | median 7 days (1–22) |
| Approval → new DailyMed version (80 reference entries) | median 13.5 days, 90% ≤ 34 |

## Join keys
- Application number = DailyMed `application_number` = FAERS `nda_num`. Found for 10 of 13 reference labels; the 3 generic references (fentanyl, methadone, tramadol) have no SrLC entries of their own.

## Mess found
| Issue | Seen |
|---|---|
| Name search is substring | "morphine" → apomorphine; "hydrocodone" → benzhydrocodone |
| Combination products | hydrocodone: 14 products, 3 single-ingredient |
| CSV broken | blank first line; stray quote in embedded HTML splits rows: 31 of 68 lines parse; SUPPL-12 lost; no date column |
| Underline ≠ reaction | fragments like "acute", "or", "Renal:", whole trial paragraphs |
| "Added" ≠ new | necrotizing pancreatitis underlined in §6.2 (2026) but in §5.2 since 2025; cholecystitis underlined 2022 and 2025 |
| History gap | hydromorphone 2016 change → next DailyMed version 726 days later (history missing versions; unverified) |

## How to use it well
1. Parse the HTML detail page, never the CSV.
2. Filter on the exact ingredient after the search.
3. ChangeEvent "FDA approved a safety label change": twice-weekly date search (last 30 days), then link the DailyMed version when it lands (~2 weeks).
4. Backtest: first appearance of a reaction anywhere in the 4 safety sections, not per section. Needs 2023–2025 FAERS quarters (~12 zips × ~60 MB) — stays on the cut list.

## Proposed for the logs
_Temporary IDs; assign the next D / DQ numbers when merging (sibling atlas sessions also propose D032+, DQ42+)._

| ID | Type | Proposal | Evidence |
|---|---|---|---|
| LD4 | Decision | SrLC drives a "safety change approved" ChangeEvent (twice-weekly date search + detail parse) | 21 update dates / 90 days; 7 d to SrLC, 13.5 d to DailyMed |
| LD5 | Decision | Backtest = first appearance in any of the 4 sections, from SrLC dates; needs 2023–2025 FAERS; stays cut item | Ozempic SUPPL-25/38 |
| LQ6 | Data issue | SrLC name search is substring | apomorphine, benzhydrocodone |
| LQ7 | Data issue | SrLC CSV: blank first line, broken rows, no date | 31/68 lines parse |
| LQ8 | Data issue | SrLC has NDA/BLA only → generic references have no history | 0 ANDA of 104 |
| LQ9 | Data issue | Underlines are edit-level; additions repeat across sections/years | Ozempic |
| Learning | — | A SrLC "addition" is a section edit, not a new reaction; the backtest must look at the whole label | this profile |

## ✅ Your hand-verification
- [ ] Open the Ozempic SrLC page, expand 06/01/2026, and confirm the underlined pancreatitis text
- [ ] Download the Ozempic CSV and open it in a spreadsheet: see the broken rows
- [ ] Search "morphine" and spot apomorphine in the results
