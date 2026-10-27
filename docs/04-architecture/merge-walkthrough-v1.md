# Merge walkthrough v1 — how different sources become one picture

_Stage: Prototype (on paper) · All facts from live queries on 2026-10-20 · Diagrams (open these): [10 source shapes](../diagrams/png/10-source-structures-v1.png) · [11 Example A](../diagrams/png/11-merge-fentanyl-v1.png) · [12 Example B](../diagrams/png/12-merge-semaglutide-naion-v1.png) · [13 join keys](../diagrams/png/13-join-keys-v1.png) · all in one PDF: [diagram-book.pdf](../diagrams/diagram-book.pdf) · editable for Visio: [02-merge-example-v1.drawio](../diagrams/drawio/02-merge-example-v1.drawio)_

## The big idea in 3 steps
| Step | What happens | Why |
|---|---|---|
| **1. Raw** | Each source arrives in its own shape. FAERS is nested JSON, labels are XML documents, recalls are flat JSON with free text | We keep raw untouched for traceability |
| **2. Identity** | Every drug mention (name, NDC, brand, product ID) is mapped to **one ingredient RxCUI** in a single `drug_identity` step | "Drug identity resolved once, in the right place" is graded |
| **3. Ontology** | Join on RxCUI → `Drug` with linked `Label`, `Recall`, `AdverseEventStat`, `Signal` | The app reads objects, not tables |

## The same drug, four ways (why identity is hard)
| Source | How fentanyl appears | Field |
|---|---|---|
| FAERS | `"FENTANYL"`, `"FENTANYL."`, `"FENTANYL CITRATE"` + 8 product RxCUIs | `medicinalproduct`, `openfda.rxcui` |
| Recall | `"FentaNYL 500 mcg … and Ropivacaine … NDC 71170-950-25"` | `product_description` (free text) |
| Label | `"FENTANYL CITRATE INJECTION, SOLUTION [HOSPIRA, INC.]"`, setid v35 | `title`, `setid` |
| RxNorm | **IN 4337 "fentanyl"** ← everything maps here | `rxcui` |

## Example A — fentanyl: recall + label + reports → one Drug
📊 [11-merge-fentanyl-v1.png](../diagrams/png/11-merge-fentanyl-v1.png) · [PDF](../diagrams/pdf/11-merge-fentanyl-v1.pdf)

| Input | Raw fact | Identity result |
|---|---|---|
| Recall D-0646-2023 | Ongoing · Class II · compounded fentanyl + ropivacaine bag · sterility | NDC unknown to RxNorm → text match → 1009056 → **fentanyl 4337** (+ ropivacaine) |
| FAERS report 10007491 | Respiratory depression · fentanyl was **concomitant** (midazolam was the suspect) | openfda.rxcui → roll up → **4337** · role filter drops it from fentanyl's signal counts |
| Label (Hospira v35) | Boxed Warning mentions respiratory depression (55 mentions in the label) | openfda.rxcui → **4337** |

**What the safety officer sees:** fentanyl has **1 active recall** (alert). Respiratory depression is **on the label**, so **no new signal**.
**Lesson:** the join works on RxCUI, but each source needs a different path to get there.

## Example B — semaglutide + NAION: "reported, but not on the US label"
📊 [12-merge-semaglutide-naion-v1.png](../diagrams/png/12-merge-semaglutide-naion-v1.png) · [PDF](../diagrams/pdf/12-merge-semaglutide-naion-v1.pdf)

| Input | Raw fact (2026-10-20) |
|---|---|
| FAERS | 869 semaglutide reports with "Optic ischaemic neuropathy" (of 100,679). **By year: 2023: 1 → 2024: 94 → 2025: 429 → 2026: 340** |
| Statistic | PRR ≈ 67 (any role, not deduplicated). **Illustrative only.** The real number needs bulk files |
| Label | Ozempic/Rybelsus v14 (Aug 19 2026): "optic" / "NAION" appear **0 times** in the label |
| Match | Same Drug (semaglutide, RxCUI 1991302); reaction **not found** in extracted label reactions |
| Output | `Signal` (New) with evidence: FAERS query + counts, label setid + version, sections searched |

**Caveats shown on the signal:**
- The 2024 jump follows published studies and media coverage (stimulated reporting).
- The wording is "reported, not on the US label", never "caused by".

🩺 **PV SME view:** this is a textbook disproportionality signal. 💊 **Safety officer view:** "Show me the 869 and the label search, and I'd take it to P&T."

## How the merge is built (preview of Phase 2)
| Layer | Dataset | Key |
|---|---|---|
| Raw | `raw_faers_*` (quarterly), `raw_labels_spl`, `raw_recalls`, `raw_rxnorm`, `raw_trials` | as landed |
| Clean | `drug_identity` (name/NDC/product RxCUI/setid → IN RxCUI) | **IN RxCUI** |
| Clean | `faers_drug_reaction` (dedup, suspect only, tagged buckets) | case + IN RxCUI + PT |
| Clean | `label_sections` → LLM → `labeled_reactions` | setid + version + section |
| Clean | `recalls_clean` (NDC parsed, ingredients) | recall_number + IN RxCUI |
| Ontology | Drug · Label · LabeledReaction · AdverseEventStat · Recall · Signal · TriageDecision | IN RxCUI links them all |
