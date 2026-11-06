# A016 — The three-question screen: recalls, "what changed", source as-of (step 11)

| | |
|---|---|
| **Date** | 2026-11-05 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Ontology / App / Pipelines |
| **Status** | Kept |
| **Replaces** | the one-page screen that answered only question 1 (A012) |

## What changed
| Before | Now | Why |
|---|---|---|
| Screen answered question 1 only; recalls and changes were in the Ontology but not on screen | Four pages behind header tabs: **0 · Morning brief**, 1 · Not in label, 2 · Recalls, 3 · What changed | The brief's three questions must be answered quickly, from one place |
| No change history (D028 proposed, `ChangeEvent` postponed) | `ontology_change_events` + object type MSSM Change Event (D045) | "What has changed since yesterday?" needs a dated record, not a guess |
| No "as of" anywhere | `ontology_source_status` + MSSM Source Status, shown on the Morning brief | Sources update on different clocks (DQ14, D029): FAERS quarterly, openFDA weekly, DailyMed daily |

## The idea in 3 lines
1. **Two ways to know something changed.** Many changes are dated by the source itself (a recall's report date, a label's effective date), so the feed has real history on day one. Everything else (a signal appearing, a label status flipping) is found by comparing this build with the last one.
2. **"Since my last review" = a date filter**, not a stored per-user bookmark: the officer picks a start date on page 3; the Morning brief shows the last 30 days.
3. **Same pattern on every page:** an unfiltered set feeds a filter list; the filtered set feeds the table; the selected row feeds a detail panel.

## How we tested it
- Locally: first build → 2,898 events; second build with no change → still 2,898; then a planted change (one signal's label status and rank edited in the saved snapshot, one recall removed) → exactly 3 new events: "is ranked: false → true", "label status: possibly_in_label → not_in_label", "new recall".
- Foundry: same counts (SQL: 900 reported, 767 terminated, 1,231 label versions; snapshot 1,952 + 900 + 1,231); a second Foundry build added nothing.
- Screen: tested in View mode — tabs switch pages; recall filter by linked drug; change table sorted newest first; metric cards 1,073 · 126 · 26.

## Result
| Question | On screen | Numbers on 2026-11-05 |
|---|---|---|
| 1 Unlabeled AEs | page 1 (ranked, with triage) | 1,073 ranked signals |
| 2 Active recalls | page 2 (drug / active / class filters, detail panel) | 126 active of 900; newest D-0040-2027 (tirzepatide/niacinamide, Houston Rx, Oct 21) |
| 3 What changed | page 3 (date range = since last review) | 26 events in the last 30 days (label versions and recalls) |
| As of | Morning brief table | FAERS through 2026Q2 · openFDA updated 2026-10-28 · DailyMed newest version 2026-10-30 · RxNorm 02-Nov-2026 |

**Timed (machine side, 2026-11-05):** Morning brief fully loaded 11.5 s after opening the app (includes Foundry start-up); page switches 1.1 s (recalls), 0.8 s (what changed), 2.4 s (signals + labels panel). All three answers are on screen within ~16 s; the 2-minute target leaves the rest for reading. Human reading time not measured.

**Trace panel added (2026-11-05, after the rubric check):** page 1 now lists the *reference labels searched* for the selected signal (Signal → Drug → Products → Reference Label, existing links), with version, effective date, safety sections and a DailyMed link. For NAION: Ozempic v20, Wegovy v19, oral Ozempic v14 — the officer can open the exact label the check read.

## Verdict
**Keep.** All three questions are on screen with source dates. Known gaps: signal "changes" will only appear after the next data refresh (the first build has nothing to compare with); a recall that matches no product we hold (e.g. compounded tirzepatide) shows "Matched to our products: 0" — correct but needs a word of explanation on screen.

## Diagram (if structure changed)
New objects MSSM Change Event and MSSM Source Status; the v1 ontology and data-flow diagrams are redrawn in the hand-in diagram set (Phase C).

## Persona check
- 💊 Safety Officer: The Morning brief is the screen she asked for: three numbers and "as of" dates. The date picker on page 3 is how she says "since my last review".
- 🩺 PV SME: Source-dated history is honest; the build-diff part must say "found on <date>" because FAERS changes arrive quarterly, not daily.
- 🧐 Evaluator: Strong for the Application row. Watch the wording: 26 "changes" are mostly label version updates, not safety findings.
