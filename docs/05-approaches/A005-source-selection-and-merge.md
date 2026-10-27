# A005 — Source selection and how the sources merge

| | |
|---|---|
| **Date** | 2026-10-20 |
| **Design-thinking stage** | Define |
| **Area** | Pipelines / Ontology / Scope |
| **Status** | Trying (atlas explorations E1–E4 measure it; freeze Oct 24) |
| **Replaces** | D003 v1 (single ingredient key) |

## What changed
| Before | Now | Why |
|---|---|---|
| Core 5 sources, all joined on one ingredient RxCUI | Core 5 + 3 bridges (Drugs@FDA, NDC Directory, SrLC); OnSIDES as a benchmark only; two-level identity Drug → Product → Package (D026, D027) | Labels and recalls belong to products, not ingredients (DQ33); bulk FAERS has `nda_num` but no openfda link (DQ39); recalls hide NDCs in free text (DQ11, DQ29) |
| "FAERS is the spine" | **Drug identity is the spine.** FAERS + labels answer Q1, recalls answer Q2, every source's changes answer Q3 | Each source answers a question; identity holds them together |
| "Since yesterday" = daily data | Since the officer's last review: ChangeEvent feed + per-source "as of" date (D028); FAERS quarterly in pilot (D029) | Sources update on different clocks; raw FAERS is quarterly |

## The idea in 3 lines
1. Every source joins at the level it naturally belongs to: ingredient (FAERS counts, trials), product (labels, Drugs@FDA, SrLC, FAERS `nda_num`) or package (recalls, NDC Directory).
2. Bridges are explored inside the source they serve, not on their own: identity = RxNorm + Drugs@FDA; labels = DailyMed + SrLC + OnSIDES; recalls = Enforcement + NDC Directory; trials = 2-hour gate.
3. A source is either used, or parked with a measured reason. Both go in the architecture note.

## Merge map
| Source | Own key | → Product | → Drug |
|---|---|---|---|
| FAERS (bulk) | prod_ai, nda_num | nda_num → Drugs@FDA | prod_ai → RxNorm (exact, salt-stripped) |
| DailyMed label | setid + version | application no. in SPL | via Product |
| SrLC | application no. + date | itself | via Product |
| Enforcement (recall) | recall_number; NDC in free text | NDC → NDC Directory | NDC → RxNorm, else text match |
| Drugs@FDA | application no. | itself | ingredient → RxNorm |
| ClinicalTrials.gov | intervention name | — | name → RxNorm |
| OnSIDES (benchmark) | label id (to verify) | via label | — |

## Parked, with reasons
Medicare Part D (re-weights ranking only) · PubMed (a second LLM problem) · Canada Vigilance / EudraVigilance / WHO VigiBase (a second identity system; VigiBase not free) · drug shortages (outside the 3 questions). All → roadmap.

## How we test it
Atlas sessions E1–E4 measure the match rates per arrow in the merge map. Target to keep the design: ≥ 90% of our suspect FAERS rows reach a Drug, ≥ 70% reach a Product, ≥ 80% of recalls reach a Drug. (Targets are assumptions; adjust at the freeze.)

## Result
_Pending E1–E4._

## Verdict
_At the Oct 24 freeze._

## Persona check
- 🏗️ Architect: two levels keep "resolved once, in the right place" true, with three levels in one table.
- 💊 Safety Officer: "as of" dates per source is what makes me trust a "nothing changed".
- 🧐 Evaluator: adding sources is encouraged by the brief *if you say why*. The merge map is that why.
