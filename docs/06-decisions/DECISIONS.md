# Decision log

Where the brief is silent, we decide and write it down. One row per decision. Newest at the bottom.
Status: Proposed (waiting on boss veto) · Accepted · Superseded by D###

| ID | Date | Decision | Why | Alternatives rejected | Status |
|---|---|---|---|---|---|
| D001 | 2026-10-13 | Repo conventions: COMPASS, one .md per approach, Mermaid + draw.io diagrams, persona lenses | Traceable reasoning is graded; keeps us oriented | Ad-hoc notes | Accepted |
| D002 | 2026-10-13 | Pilot class = GLP-1 receptor agonists | Volume, recent label changes, recalls, inpatient relevance | Anticoagulants (backup), random 100-drug formulary | Superseded by D007 |
| D003 | 2026-10-13 | Drug identity resolved once on RxNorm ingredient RxCUI | Graded explicitly; one join key | Per-dataset name matching | Proposed (G2) |
| D004 | 2026-10-13 | FAERS from quarterly bulk files, deduped, incremental by quarter | Dedup needs case-level data | openFDA API counts only | Proposed (G3); recheck against Developer Tier limits |
| D005 | 2026-10-13 | LLM runs only on new/changed label versions, cached | Cost; "don't re-run needlessly" | Re-extract every build | Proposed (G4) |
| D006 | 2026-10-13 | Signal = PRR with Evans criteria (N≥3, PRR≥2, χ²≥4) | Standard, explainable | Raw counts | Proposed (S6) |
| D007 | 2026-10-13 | Pilot class = **opioids** (~12 ingredients, see A001) | Boss suggestion; ISMP high-alert drugs; label-change backtest | GLP-1 (D002) | Accepted (list to confirm) |
| D008 | 2026-10-13 | Monitoring (pipeline + AI health + drift) is **must-have** and a demo centerpiece | Boss: "monitoring is the beauty", show production-side use | Keep as stretch | Accepted |
| D009 | 2026-10-13 | Drift is judged over a **3–4 week rolling window**; 3–4 day swings are not alerts | Boss guidance; short windows are noisy | Daily drift alerts | Accepted (our reading; confirm) |
| D010 | 2026-10-13 | Build on **Palantir free Developer Tier** | Boss instruction; unblocks work now | Wait for company access | Accepted |
| D011 | 2026-10-13 | Project purpose = showcase of thinking; docs and reasoning trail are a first-class deliverable | Boss: exploratory, show thought process | Build-only focus | Accepted |
| D012 | 2026-10-13 | Profile every source by hand before building pipelines | Boss heads-up on messy data | Build first, fix later | Accepted |
| D013 | 2026-10-14 | Git/GitHub fully manual by user; Claude never commits (CLAUDE.md §0 + settings deny rules). Account **vrbabu9000** only, via `github.com-personal` SSH alias | User ground rule; avoid commits under the wrong account (vrajesh9000) | Claude-run commits | Accepted |
| D014 | 2026-10-19 | Pilot class = **opioid-led hybrid**: 8 opioids + 5 GLP-1 RAs (A003) | Research R1: hybrid 27/30 vs opioids-only 22/30; covers each other's gaps | Opioids only (fallback), GLP-1 only | Proposed (needs user/boss yes) |
| D015 | 2026-10-19 | AI extraction target: F1 ≥ 0.85, reported per label section; benchmark vs TAC 2017 / OnSIDES | Public benchmarks exist (R3); "measured, not asserted" | Self-made gold set only | Proposed |
