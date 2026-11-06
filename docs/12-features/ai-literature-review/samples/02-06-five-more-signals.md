# Samples 02–06 — five more signals (2026-11-05)

Same method as [sample 01](01-semaglutide-naion.md). Evidence was fetched by [fetch_evidence.py](../../../../tools/lit_review/fetch_evidence.py). Raw results and abstracts are in [evidence/](../evidence/). These are **AI reviews (Claude, abstracts only), not pharmacist reviews.**

Why these five: each one tests a different kind of signal. A GI syndrome (02), a vague context term (03), a sensory event (04), a cancer (05) and a tiny count (06).

---

## 02 · Semaglutide · Cyclic vomiting syndrome (rank 3, a = 145)
| | |
|---|---|
| Search | semaglutide or GLP-1 + cyclic vomiting / cannabinoid hyperemesis → **1 hit** |
| Evidence | PMID 42481928 (2026, FAERS study of GLP-1 drugs): cyclic vomiting syndrome is a **headline FAERS signal, mainly for semaglutide (ROR 64.8)**. It holds after their stricter method. No clinical studies found. |
| Label | "Vomiting" appears in Warnings and Precautions and in Adverse Reactions (9 sections each). "Cyclic vomiting" appears in none. |
| **Verdict** | **Plausible. Backed only by FAERS data.** Our signal matches a published FAERS study. Open question for a pharmacist: is a recurring vomiting syndrome covered by the label's "vomiting"? |
| Suggested action | Keep ranked. Add the note "FAERS-only evidence; label lists vomiting". Candidate **medium** synonym row (CVS → "vomiting"), for a pharmacist to decide. |

## 03 · Fentanyl · Anaesthetic complication neurological (rank 1, a = 244)
| | |
|---|---|
| Search | fentanyl + anaesthesia + neurological complication → 38 hits |
| Evidence | **None specific.** The hits are general anaesthesia papers: nerve blocks, spinal anaesthesia case reports, two veterinary studies. |
| **Verdict** | **Literature can't review this one.** The term describes a setting (a problem during anaesthesia), not a drug effect. Fentanyl is given *during* anaesthesia, so the setting explains the reports. |
| Suggested action | Mark "not reviewable by literature: context term". A pharmacist should decide if the term belongs in a "procedure/context" bucket (like D016's non-clinical buckets). |

## 04 · Tirzepatide · Allodynia (rank 5, a = 55) ⭐
| | |
|---|---|
| Search | tirzepatide + allodynia / dysesthesia / hyperesthesia / skin sensitivity / skin pain → **9 hits** |
| Evidence | Case series of cutaneous allodynia on tirzepatide (PMID 42101979). Case reports with semaglutide and tirzepatide (41210042). A FAERS mining study plus literature review of GLP-1 dysesthesia (42168638). A systematic review of 101 studies: dysesthesia is **dose-dependent**, most often during dose increases (42930571). |
| Label | The **Zepbound label (setid 487cd7e7…, v40), Adverse Reactions, says:** *"dysesthesia occurred more frequently among patients receiving ZEPBOUND"* (0.2–0.4% vs 0.1% placebo). |
| **Verdict** | **Real effect, and probably already in the label under a different word.** The papers group allodynia with dysesthesia. Our synonym table has no Allodynia → "dysesthesia" row. syn_v2 rejected the "allodynia" lead because that word itself isn't in the label. |
| Suggested action | **Propose a synonym row: Allodynia → "dysesthesia", band medium.** The signal would move to "possibly in label". This is a likely false positive in our ranked list, found by reading papers. |

## 05 · Morphine · Ewing's sarcoma (rank 1, a = 26)
| | |
|---|---|
| Search | morphine + Ewing → 8 hits |
| Evidence | Every relevant paper is about **treating Ewing's sarcoma pain** (lignocaine for intractable pain, end-of-life pain in a child, cannabis for sarcoma pain). One 1964 hit matched an unrelated scorpion species with "Ewing" in its name. |
| **Verdict** | **Likely noise: confounding by indication.** The disease causes the morphine use, not the other way round. |
| Suggested action | Demote. Idea: a new caution `indication_confounding` for cancer terms on opioids. This needs a pharmacist rule, not an AI call per signal. |

## 06 · Buprenorphine · Superior mesenteric artery syndrome (rank 2, a = 11)
| | |
|---|---|
| Search | buprenorphine or any opioid + SMA syndrome → **1 hit** |
| Evidence | One Japanese case report (PMID 27004394): SMA syndrome after scoliosis surgery, on **fentanyl** pain relief, not buprenorphine. Surgery is the known cause. |
| **Verdict** | **Not enough evidence.** Small count, and the only paper points to surgery. |
| Suggested action | Keep visible but low priority. Re-check only if new papers appear. |

## Run metrics
| Sample | Hits | API calls | Seconds | Abstract tokens (≈) | Retracted dropped |
|---|---|---|---|---|---|
| 02 | 1 | 3 | 2.0 | 688 | 0 |
| 03 | 38 | 3 | 2.1 | 4,209 | 0 |
| 04 | 9 | 3 | 2.1 | 5,871 | 0 |
| 05 | 8 | 3 | 2.1 | 3,761 | 0 |
| 06 | 1 | 3 | 2.0 | 437 | 0 |
