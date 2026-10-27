# OnSIDES: public label side-effect extractions — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Atlas page: [onsides.html](../atlas/onsides.html) ([artifact](https://claude.ai/artifact/Fvgky8ZaUkoaBY2xajeg9J)) · Script: [label_atlas.py](../../../prototypes/explore/label_atlas.py) step `onsides`_

## In one line
One record = **one MedDRA term found in one section (AR / BW / WP) of one label**, scored by a fine-tuned PubMedBERT model. Built by the Tatonetti lab (github.com/tatonetti-lab/onsides). Planned role: **benchmark** for our Part B extractor. Measured result: **too thin on our labels to be a second accuracy number.**

## How to get it
| | |
|---|---|
| Data release | v3.1.1 (2026-04-22), labels "as of April 2026". v3.2.x (Jul 2026) is code-only. |
| Size | 85 MB zip → 430 MB of CSV (7 tables + SQL schemas) |
| Local | `prototypes/data/_onsides/v3.1.1/csv/` (git-ignored) |
| Licence | Data **CC BY 4.0** (cite Tanaka et al., Med 2025) · code MIT · term names are **MedDRA** → compare only, never republish |
| Warning in README | Research resource; not for patient or clinical decisions |

## Record shape
```
product_label           label_id · source (US/UK/EU/JP) · name · source_product_id (= setid.version for US) · url
product_adverse_effect  product_label_id · effect_id · label_section (AR/BW/WP/NA) · effect_meddra_id · match_method (PMB/SM) · pred0 · pred1
vocab_meddra_adverse_effect   meddra_id · name · term type (PT 3,550 / LLT 2,873)
product_to_rxnorm, vocab_rxnorm_*   label → RxNorm product → ingredient
high_confidence         342 rows (not defined in the release)
```

## Numbers (measured)
| Measure | Value |
|---|---|
| Labels | 41,119 (US 35,340 · UK 2,874 · JP 1,884 · EU 1,021) |
| Effect rows | 6,928,666, of which **5,693,345 (82%) repeat** a (label, term, section) |
| Our 1,324 DailyMed labels present | 952 (713 at today's version, 172 one behind, 67 further) |
| Our 13 reference labels present | **4** (Hysingla v13, hydromorphone v16, tramadol v5, methadone v11) |
| Ozempic stand-in | A-S Medication repackager v1 (Jan 2021): 16 terms |
| OxyContin stand-in | generic oxycodone ER v4 (Jan 2022): 25 terms |
| Our gold draft (unique counted terms) | semaglutide 44 · oxycodone 147 |
| Exact name overlap with gold | 9 · 17 |
| Gold phrases present in the stand-in's text | 34/49 · 148/155 |
| OnSIDES published hold-out F1 (AR / WP / BW) | 0.85 / 0.76 / 0.74 |

## Join keys
- US `source_product_id` = DailyMed `setid` + "." + `version` (35,340 / 35,340). One version per setid; no history.
- Terms = MedDRA IDs, but levels are mixed (31% LLT on both stand-ins) and we have no MedDRA hierarchy to roll LLT → PT.

## Mess found
| Issue | Seen |
|---|---|
| 82% repeated effect rows | Hysingla: 1,848 rows = 30 unique terms |
| Brand reference labels missing | 9 of 13, incl. Ozempic, OxyContin, Mounjaro |
| Old / wrong stand-ins | Ozempic 2021, OxyContin generic 2022, MS Contin 2010; fentanyl rule picked an injection for a patch |
| Headings as reactions | "Cardiac disorder", "Gastrointestinal disorder" |
| Matches inside words | "TEN" from "EXTENDED"/"THREATENING"; "Diabetic" alone |
| Section "NA" | 388,407 rows |
| Undocumented scores | `pred0`, `pred1` (docs use `pred1` as confidence) |

## How to use it well
1. Gold set = the only accuracy number for Part B (D015).
2. Optional (cut #2): precision cross-check on the 4 labels OnSIDES has, at the **same version** (fetch that version from DailyMed). Never score recall against OnSIDES.
3. Feed its error types into our prompt's "do not extract" list and the grounding check (quote must be whole words).
4. Never ship OnSIDES term lists; term-level comparison files stay in git-ignored `prototypes/data/_labels/onsides_terms_*.csv`.

## Proposed for the logs
_Temporary IDs; assign the next D / DQ numbers when merging._

| ID | Type | Proposal | Evidence |
|---|---|---|---|
| LD6 | Decision (changes plan Q2 / A005 "second accuracy number") | OnSIDES downgraded to an optional precision cross-check on 4 labels; gold set is the only accuracy number | 4/13 references; 16 & 25 terms vs 44 & 147 |
| LQ10 | Data issue | 82% repeated effect rows | 5,693,345 / 6,928,666 |
| LQ11 | Data issue | Brand reference labels missing; stand-ins old or wrong route | 9/13 missing |
| LQ12 | Data issue | False terms: headings, in-word matches, adjectives | "Cardiac disorder", "TEN", "Diabetic" |
| Learning | — | A public extraction set is only a benchmark if it covers the same label versions we read | this profile |
| Compliance | Question | Does CC BY on OnSIDES cover the MedDRA term names inside? | 🛡️ lens, unverified |

## ✅ Your hand-verification
- [ ] `grep -c "adec4fd2" prototypes/data/_onsides/v3.1.1/csv/product_label.csv` → 0 (Ozempic Novo label absent)
- [ ] Open `prototypes/data/_labels/onsides_terms_oxycodone.csv` and find "TEN" and "Cardiac disorder"
