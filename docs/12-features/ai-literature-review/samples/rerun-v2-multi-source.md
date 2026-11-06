# F01 run v2: the same 6 signals with 3 more sources (2026-11-05)

**TL;DR:** No verdict flipped. Two verdicts got stronger with **regulator-level** evidence: FDA itself listed **NAION** (Q4 2024) and **Dysaesthesia** (Q1 2024) as potential signals for the whole GLP-1 class. **Europe PMC added no new on-topic paper.** Its larger hit counts were full-text noise that the relevance gate removed. Rank of value: **FDA Potential Signals > OnSIDES > Europe PMC**.

| | |
|---|---|
| **Stage** | Prototype → Test |
| **Sources** | Europe PMC REST API (live) · FDA "Potential Signals of Serious Risks" quarterly pages, 70 pages / 785 rows, 2015 → Apr–Jun 2026 (cached once) · OnSIDES v3.1.1 data, Apr 2026, CC BY 4.0, 85 MB zip (cached once) |
| **Code** | [research_sources.py](../../../../tools/lit_review/research_sources.py) (`fda-cache`, `onsides-cache`, `run`) |
| **Evidence** | `evidence/<id>-v2.json` (one per sample) |
| **Judge** | Claude in this session, from the fetched evidence. Not a pharmacist. |

## Verdicts: v1 (PubMed only) → v2 (+3 sources)
| # | Signal | Europe PMC: hits → kept after gate | FDA Potential Signals | OnSIDES (labels US/EU/UK/JP) | v1 verdict | v2 verdict |
|---|---|---|---|---|---|---|
| 01 | Semaglutide · Optic ischaemic neuropathy | 276 → 8 (8 preprints, none kept) | ✅ **Oct–Dec 2024: NAION, whole GLP-1 class**, "evaluating the need for regulatory action" | On **UK** labels (3 of 3). Not found on the EU or US labels in OnSIDES | Real concern | **Real concern, stronger**: FDA, EMA and the UK all flag it |
| 02 | Semaglutide · Cyclic vomiting syndrome | 70 → 1 (same FAERS study) | Not listed | Only "Vomiting" (no cyclic vomiting anywhere) | Plausible (FAERS only) | **Unchanged** |
| 03 | Fentanyl · Anaesthetic complication neurological | 280 → 0 | Not listed | Not listed | Not reviewable | **Unchanged** (now 0 papers instead of 38 off-topic ones) |
| 04 | Tirzepatide · Allodynia | 72 → 5 (all already in PubMed) | ✅ **Jan–Mar 2024: Dysaesthesia, GLP-1 class incl. Mounjaro** | **Dysaesthesia** on the EU label. The only tirzepatide label in OnSIDES | Real, probably in label as "dysesthesia" | **Real, stronger**. The synonym row Allodynia → "dysesthesia" is better supported, but still a pharmacist call (allodynia ≠ dysaesthesia exactly) |
| 05 | Morphine · Ewing's sarcoma | 231 → 1 (cannabis for Ewing pain) | Not listed | Not listed | Noise (confounding by indication) | **Unchanged**. The one paper fits confounding |
| 06 | Buprenorphine · SMA syndrome | 76 → 0 | Not listed | Not listed | Not enough evidence | **Unchanged** |

The FDA status text is as of each quarterly page. FDA may have acted since. Not checked here.

## What each source added
| Source | Added | Did not add | Verdict |
|---|---|---|---|
| **FDA Potential Signals** | Answers "is FDA already looking at it?" with a dated, official row. 2 of 2 real signals were on the list | Opioids barely appear (1 class row, "Hypoglycemia" 2023). Rows are free text in US spelling and often name a class, not a drug | **Keep: highest value.** One scrape per quarter, $0 per review |
| **OnSIDES** | "Labeled abroad" evidence (UK NAION, EU dysaesthesia) | Thin GLP-1 coverage: tirzepatide has 1 EU label and **0 US labels**, semaglutide has 2 US. EU semaglutide labels did not show NAION although EMA acted in 2025 (extraction miss or older label version, unverified) | **Keep as "yes" evidence only.** A "not found" from OnSIDES means nothing |
| **Europe PMC** | Preprint counts; open-access flags; the same API covers PubMed | **0 new on-topic papers** vs PubMed. The bigger counts were full-text mentions (e.g. retatrutide reviews) that fail the drug + event in abstract gate | **Optional.** Use it as the single paper API if convenient. It does not change answers |

## Formulary-wide check (free by-product)
FDA's list names a formulary drug in **21 rows**, giving **66 drug–event pairs** for our 13 drugs (mostly GLP-1 class rows expanded to each drug). Automatic word matching against our 1,952 signals was **not reliable**. FDA writes "Non-arteritic anterior ischemic optic neuropathy (NAION)"; our MedDRA term is "Optic ischaemic neuropathy". FDA also writes "Dysaesthesia" where our signal says "Allodynia". To make this a real check, we need a small mapping from FDA wording to MedDRA terms, the same kind of reviewed table as [A014](../../../05-approaches/A014-label-faers-synonym-table.md). Not built.

## Cost and speed (measured)
| | v1 PubMed | v2 Europe PMC + FDA + OnSIDES |
|---|---|---|
| Live API calls per review | 3 | 2 (FDA and OnSIDES read local caches) |
| Seconds per review | ~2.0 | ~1.6 |
| Abstract tokens sent to the model | ~3.5k mean | ~0.9k mean (the gate drops off-topic papers) |
| One-off cache cost | — | FDA: 70 pages, ~1 min. OnSIDES: 85 MB download, ~1 min to filter |

Model cost per review stays **at or below ~$0.09** (Opus 5.5, estimate). The earlier ~$0.11 guess in [sources-beyond-pubmed.md](../sources-beyond-pubmed.md) was too high, because the gate shrinks the input.

## What this does not prove
- Still 6 hand-picked signals, judged by Claude. This is not an accuracy measure.
- The relevance gate is a plain substring test on title and abstract. It may drop a relevant paper that uses another word for the event.
- OnSIDES labels are an ML extraction (their stated F1 ≈ 0.90). Our label status still comes only from DailyMed (D037).
