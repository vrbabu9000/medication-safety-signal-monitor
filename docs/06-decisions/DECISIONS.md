# Decision log

Where the brief is silent, we decide and write it down. One row per decision. Newest at the bottom.
Status: Proposed (waiting on boss veto) · Accepted · Superseded by D### (vN)

**Rules (CLAUDE.md §2c):** a decision is never edited in place. When it changes, it gets a new version: either a new row `D### vN`, or a new D-number that supersedes it. The change is logged in the table below with its trigger and evidence. Every change bumps the COMPASS version.

## Decision changes (newest first)
| Date | Decision | Before (v1) | Now | Trigger / evidence | Compass |
|---|---|---|---|---|---|
| 2026-10-27 | D031 v2 → v3 (dates + cuts) | Demo ~Nov 3; freezes Oct 23/24; cuts applied only if Red | Demo Wed Nov 4 (asked of boss); build Oct 29–Nov 2; all 6 cuts applied now + decision review 5→1 h + gold-set check folded into B8 | No work Oct 21–27; Nov 3 = Election Day; you can lock in only from Oct 29 | v10 |
| 2026-10-20 | D031 v1 → v2 (cut list) | 5 cuts, hours not tied to tasks | 6 cuts, each tied to a BACKLOG task with your/Claude hours; adds gold set 10→6 and rehearsals 2→1 | ⏱️ Delivery Lead first run: v1 cuts saved almost none of *your* hours | v8 |
| 2026-10-20 | D003 → D027 | One join key: ingredient RxCUI | Two levels: Drug (RxCUI) → Product (application no.) → Package (NDC) | Labels and recalls belong to products (tablet vs injection label, DQ33); bulk FAERS carries `nda_num` | v8 |
| 2026-10-20 | FAERS→label link (merge walkthrough v1) → D024 | FAERS `openfda.spl_set_id` → label setid | `nda_num` → Drugs@FDA → label | Bulk files have no openfda block (DQ39) | v8 |
| 2026-10-20 | D004 v1 → v2 (via D022) | "Incremental by quarter" (append) | Upsert by caseid (max version) + deletes against all history | Append = +8.7% phantom rows in 2 quarters (DQ36) | v8 |
| 2026-10-20 | DQ05 "primary/secondary suspect only (pending)" → D021 | Pending; "PS only" considered | PS + SS + I, once per report | 69% of SS rows repeat the PS drug; tirzepatide SS > PS (DQ35) | v8 |
| 2026-10-20 | D016 (lawyer tag) — scope narrowed by D025 | Tag lawyer-filed via `occp_cod` | Tag only where filled; show "unknown"; monitor fill rate | `occp_cod` blank 35% → 72% at the AEMS switch (DQ38) | v8 |

## Learnings (realised on the fly; newest first)
| Date | What we realised | What it changed |
|---|---|---|
| 2026-10-27 | A lost week hurts the build, not the thinking: exploration was finished 3 days early, so the design trail is intact | D031 v3: Claude pre-builds code so your hours go only to Foundry hands-on |
| 2026-10-20 | Bulk FAERS ≠ API FAERS: different shape, no enrichment | D024, DQ39; FAERS profile join keys corrected |
| 2026-10-20 | caseid dedup misses one patient filed ~700× by many companies | D023, DQ37 (oxycodone −24%) |
| 2026-10-20 | Substring drug matching is wrong (apomorphine, heroin) | D020, DQ34 |
| 2026-10-20 | FAERS raw files are quarterly; FDA dashboard is near real time but has no confirmed API | D029; "since yesterday" redefined (D028) |
| 2026-10-20 | Brief's 5 sources lack the bridges for the joins (application no., NDC) | D026: add Drugs@FDA, NDC Directory, SrLC |
| 2026-10-20 | Demo is ~Nov 3 with ~50 of your hours; load already ~110% | D031: freeze dates + cut list |

## All decisions

| ID | Date | Decision | Why | Alternatives rejected | Status |
|---|---|---|---|---|---|
| D001 | 2026-10-13 | Repo conventions: COMPASS, one .md per approach, Mermaid + draw.io diagrams, persona lenses | Traceable reasoning is graded; keeps us oriented | Ad-hoc notes | Accepted |
| D002 | 2026-10-13 | Pilot class = GLP-1 receptor agonists | Volume, recent label changes, recalls, inpatient relevance | Anticoagulants (backup), random 100-drug formulary | Superseded by D007 |
| D003 | 2026-10-13 | Drug identity resolved once on RxNorm ingredient RxCUI | Graded explicitly; one join key | Per-dataset name matching | Superseded by D027 (v2) |
| D004 | 2026-10-13 | FAERS from quarterly bulk files, deduped, incremental by quarter | Dedup needs case-level data | openFDA API counts only | **Confirmed need 2026-10-20** (API can't filter role, ~26k record cap); recheck against Developer Tier limits |
| D005 | 2026-10-13 | LLM runs only on new/changed label versions, cached | Cost; "don't re-run needlessly" | Re-extract every build | Proposed (G4) |
| D006 | 2026-10-13 | Signal = PRR with Evans criteria (N≥3, PRR≥2, χ²≥4) | Standard, explainable | Raw counts | Proposed (S6) |
| D007 | 2026-10-13 | Pilot class = **opioids** (~12 ingredients, see A001) | Boss suggestion; ISMP high-alert drugs; label-change backtest | GLP-1 (D002) | Accepted (list to confirm) |
| D008 | 2026-10-13 | Monitoring (pipeline + AI health + drift) is **must-have** and a demo centerpiece | Boss: "monitoring is the beauty", show production-side use | Keep as stretch | Accepted |
| D009 | 2026-10-13 | Drift is judged over a **3–4 week rolling window**; 3–4 day swings are not alerts | Boss guidance; short windows are noisy | Daily drift alerts | Accepted (our reading; confirm) |
| D010 | 2026-10-13 | Build on **Palantir free Developer Tier** | Boss instruction; unblocks work now | Wait for company access | Accepted |
| D011 | 2026-10-13 | Project purpose = showcase of thinking; docs and reasoning trail are a first-class deliverable | Boss: exploratory, show thought process | Build-only focus | Accepted |
| D012 | 2026-10-13 | Profile every source by hand before building pipelines | Boss heads-up on messy data | Build first, fix later | Accepted |
| D013 | 2026-10-14 | Git/GitHub fully manual by user; Claude never commits (CLAUDE.md §0 + settings deny rules). Account **vrbabu9000** only, via `github.com-personal` SSH alias | User ground rule; avoid commits under the wrong account (vrajesh9000) | Claude-run commits | Accepted |
| D014 | 2026-10-19 | Pilot class = **opioid-led hybrid**: 8 opioids + 5 GLP-1 RAs (A003) | Research R1: hybrid 27/30 vs opioids-only 22/30; covers each other's gaps | Opioids only (fallback), GLP-1 only | **Accepted 2026-10-20** (user) |
| D015 | 2026-10-19 | AI extraction target: F1 ≥ 0.85, reported per label section; benchmark vs TAC 2017 / OnSIDES | Public benchmarks exist (R3); "measured, not asserted" | Self-made gold set only | Proposed |
| D016 | 2026-10-20 | Focus rule: rank **clinical side effects + recalls**; tag (don't rank) lawyer-filed, abuse/overdose, product-use/error, pregnancy/neonatal | User direction; data shows these buckets dominate | Rank everything | Accepted |
| D017 | 2026-10-20 | Diagrams are **separate PNG + PDF files** (Mermaid source → `tools/render_diagrams.sh`), never code blocks in .md; draw.io kept for Visio | User: wants images/PDFs to look at | Mermaid inside .md | Accepted |
| D018 | 2026-10-20 | Formulary = explicit list of 13 ingredient RxCUIs (not an ATC class) | DQ31: class codes miss methadone/hydrocodone | ATC N02A membership | Accepted |
| D019 | 2026-10-20 | Labels: DailyMed is the source of truth (not openFDA label copy) | DQ28: openFDA copy lags | openFDA label API | Accepted |
| D020 | 2026-10-20 | Drug identity: exact ingredient via RxNorm after splitting prod_ai and stripping salts; never substring match | DQ34: morphine +50% false rows | Substring / fuzzy name match | Proposed |
| D021 | 2026-10-20 | Suspect = PS + SS + I; each ingredient counted once per report; concomitant never counts | DQ35 | PS only; all roles | Proposed |
| D022 | 2026-10-20 | FAERS incremental = upsert by caseid (max caseversion) + deletes applied to full history; raw quarters append-only | DQ36: append = +8.7% phantom rows in 2 quarters | Append each quarter | Proposed |
| D023 | 2026-10-20 | Cross-case duplicate fold (person key + ≥30 drugs + ≥50 filings) before counting | DQ37: oxycodone −24%, removes pemphigus/hand-deformity artefacts | caseid dedup only | Proposed |
| D024 | 2026-10-20 | FAERS → label via nda_num → application number; one reference label per product (route-specific) | DQ33, DQ39: bulk has no openfda | openFDA spl_set_id | Proposed |
| D025 | 2026-10-20 | Monitoring tracks per-quarter fill rate of key fields and alerts on jumps | DQ38: occp_cod blank 35% → 72% | Row counts only | Proposed |
| D026 | 2026-10-20 | Add 3 public sources as bridges: **Drugs@FDA** (application no. → product), **NDC Directory** (package → product), **SrLC** (dated label safety changes). OnSIDES used only as a Part B accuracy benchmark | They close the joins the core 5 can't make (DQ39, DQ29); SrLC gives label-change alerts + backtest | Part D, PubMed, Canada/EU/WHO data, drug shortages (parked, reasons in A005) | Proposed |
| D027 | 2026-10-20 | Two-level drug identity: Drug (ingredient RxCUI) → Product (application no.) → Package (NDC), built once in `drug_identity` (= D003 v2) | Counts belong to ingredients, labels and recalls to products | Single ingredient key (D003 v1) | Proposed |
| D028 | 2026-10-20 | "Since yesterday" = since the officer's last review: a ChangeEvent feed across all sources + an "as of" date per source on screen | Sources update on different clocks (DQ14) | Pretend everything is daily | Proposed |
| D029 | 2026-10-20 | FAERS is quarterly in the pilot; daily FAERS only if an official AEMS API/export is confirmed (gate E4) | Raw files are quarterly; dashboard has no confirmed API; scraping is fragile | Scrape the dashboard; build an MCP (wrong tool for a Foundry pipeline) | Proposed |
| D030 | 2026-10-20 | Tracking: decisions versioned + Decision changes / Learnings tables; COMPASS versioned with snapshots in docs/00-compass/history; ⏱️ Delivery Lead agent + BACKLOG | Reasoning trail is half the deliverable; time-critical | Edit decisions in place | Accepted |
| D031 | 2026-10-20 | Demo ~Nov 3; exploration freeze Oct 23; decision freeze Oct 24; cut list order: Trials → OnSIDES → daily FAERS → SrLC backtest → exenatide/tirzepatide | ~50 of your hours vs ~55 h of work | Open-ended exploration | Accepted |
| D031 v2 | 2026-10-20 | Cut list re-ordered and tied to BACKLOG tasks: Trials → OnSIDES → gold set 10→6 → rehearsals 2→1 → daily FAERS + SrLC backtest → exenatide/tirzepatide (−8 of your hours) | v1 cuts didn't reduce your load | D031 v1 list | Accepted |
| D031 v3 | 2026-10-27 | Demo **Wed Nov 4** (pending boss OK). Build Oct 29–Nov 2, feature freeze Nov 2 8 pm, note + rehearsal Nov 3. All 6 cuts applied now (11 drugs, gold set 6, 1 rehearsal, no Trials/OnSIDES/daily FAERS/SrLC backtest) + decision review 5→1 h + gold-set check folded into B8 → ~41 of your h vs ~54 available | 7 days lost; Election Day Nov 3 | Keep Nov 3 and cut monitoring; apply cuts only when Red | Proposed (your OK + boss OK on Nov 4) |
