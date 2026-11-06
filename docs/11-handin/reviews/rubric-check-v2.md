# Rubric check v2: the hand-in after the Phase D fix pass (2026-11-05)

_🧐 Evaluator / Red Team view · Stage: **Test** · Strict-professor scoring, 1–5 · Read-only: Foundry not opened · Compares with [rubric-check.md](rubric-check.md) (v1)_

**TL;DR.** The paperwork gap is closed. The note, deck, script and guide now exist, and they are honest. Communication goes up a full point. The build itself barely moved. The AI still reads 2 oxycodone labels. The "label passage beside the extraction" drill-down is still missing. The AI error rate is still self-scored on 35 items. The demo is scripted but **not rehearsed**. Application, AI reliability and Optimization stay at 3. **One recommendation:** take the D041 v2 decision now and close the AI ↔ screen gap on semaglutide before anything else. No wording fix can earn that point.

## 1. Scores (v1 → v2)

| Item | v1 | v2 | One-line reason | Evidence |
|---|---|---|---|---|
| **Hand-in 1 · Working build** | 4 | **4** | Added the labels-searched panel and machine timings, and fixed "No value". The AI scope, the "Experimental" ontology status, the missing schedules and the duplicate link are unchanged | deck p3, p6; [numbers.json](../numbers.json) `app` |
| **Hand-in 2 · Architecture note** | 1 | **4** | One page: a diagram, 4 decisions each with "why" and evidence, a "not done" list and a glossary. Lost a point because decision #1 rests on proposed D027, it has no "another month" line and no partitioning line, and the type is tiny | architecture-note.pdf p1 |
| **Hand-in 3 · Optimization log** | 3 | **3** | Partitioning now has a "why not" (D048). Still every timing is one run, O3's baseline is not back to back, and there are no compute-seconds. The required `.md` log still has no partitioning row | R06 p10, p12; [optimization-log.md](../../08-optimization-log/optimization-log.md) |
| **Hand-in 4 · 20-min demo** | 2 | **3** | Deck, script and click guide are strong, and the safety officer's fixes are applied. But the script says "estimate, not yet rehearsed". Checklist #8–10 are blank (DailyMed `optic` check, Class I count, human stopwatch). Part H packs 12.5 minutes | speaking_script.md header; guide checklist #8–10; R09 p16 |
| **Architecture** | 4 | **4** | The B1 "how to extend" table and the Signal → Drug → Products → Reference Label path help. Still no direct Signal → Label link. The formulary list is still copied 5×. The duplicate link stays. D027 is proposed | deck p18, p7; R03 p4, p7 |
| **Optimization** | 3 | **3** | The O2 story is still the best slide. Partitioning is addressed, but "mostly start-up" is asserted, not measured (see §4) | deck p12–13; R06 p12 |
| **Data judgment** | 4 | **4** | Noise is now named on screen before the reviewer finds it (Ewing's sarcoma, liraglutide). NAION is framed as a known positive. DQ04/DQ06 are marked "known gap". But DQ01/02/05 still say Suspected, and NAION's reporter split is not measured | deck p4, p14; data-issues-register DQ01–06 |
| **The application** | 3 | **3** | The trace now reaches DailyMed (the strongest moment of the demo). Still missing: the brief's "label passage beside the extraction". The 394 reports cannot be opened. The recall link is a tab the presenter opens, not a link in the app. No person has timed it | deck p4–5; R04 p4; guide A4, A6 |
| **AI reliability** | 3 | **3** | Nothing new was measured. Same 35-item key that Claude wrote, scored on a Claude model. Long sections (~411 of 448 items) unscored. Drift after a model change is designed, not run. The honesty is good, but honesty is not evidence | eval/ai-eval-v1.md; deck p9; R08 p3 |
| **Communication** | 3 | **4** | The note and demo exist, one definition per term, limits said aloud, an "another month" slide. Lost a point for 4 overclaims (§4), about 200 pages of reports, and a stray `R00-sample.pdf` stamped "NUMBERS PROVISIONAL" | deck p14–15; R00-sample p1 |

## 2. What improved, what did not

**Improved:** the architecture note now exists. Deck, script and guide exist. The labels-searched panel has DailyMed links. Machine timing is measured (11.5 s, 0.8–2.4 s). The "No value" cells are gone. Partitioning is decided (D048). NAION is framed as a known positive (EMA PRAC, WHO, with links). Noise is named before filtering. The recall wording no longer claims inventory. The PRR is explained as "a reporting pattern, not risk". "Found 35 of 35" replaces "recall 35/35". The 12 proposed decisions are listed openly.

**Did not move (all from the v1 top 10):** #2 the AI ↔ screen gap (no D041 v2). #3 the human AI sample. #4 rehearsal and a human timing. #5 case ids and the recall URL on the record. #6 repeat timings and compute. #9 an untriaged or new count. #10 ontology hygiene. Also not done: the DQ status refresh and NAION's reporter-type split.

## 3. Holes a reviewer finds in the demo and Q&A (worst first)

| # | Hole | Smallest fix | Type |
|---|---|---|---|
| 1 | **"Show me the label passage next to what the AI extracted, for semaglutide."** The brief's Part C asks for this by name. The answer is "AI read 0", on the hero drug | Write **D041 v2**: widen to the 3 semaglutide reference labels only. Run the cached extractor. Add a Labeled Reactions table (reaction · quote · section · version) under the labels panel | Owner decision + Foundry |
| 2 | **"How often is it wrong where it matters, and who besides Claude decided?"** | A person (not Claude) scores a random sample of 30 long-section items for precision, with an interval. Takes 1–2 h. Report it as "human-checked, not a pharmacist" | Owner time + doc |
| 3 | **The demo is not rehearsed.** One live failure (a slow page, or `optic` landing on the retinopathy warning) costs more than any slide gains | Do one timed run-through. Fill checklist #8–10. Capture the missing A4/A6 fallback screenshots | Owner |
| 4 | **"Open one of the 394 reports."** "By query today" is honest but weak in the demo's trust moment | Add `example_case_ids` to the Signal and an `openfda_url` to the Recall in the ontology build files. About 30 min | Foundry |
| 5 | **"Is 88 s vs 32 s outside the noise? What is start-up?"** | Re-run O2 and O3 twice each, back to back, and report ranges. Then either measure an empty build or delete "mostly start-up" | Foundry (no code) + doc |
| 6 | **"Your signal rule (D006) and your headline identity decision (D027) are still *proposed*?"** | Accept the 12 proposed decisions in one batch before the demo, or say why each is still open | Owner decision |
| 7 | **A pharmacovigilance reviewer reads the rank-1 list aloud.** Already pre-empted in A2, so the damage is limited. Still, 1,073 has no "new" or "untriaged" count | Optional: tag reactions found in the label's Indications section as an `indication` bucket | Foundry (optional) |
| 8 | **Hygiene on screen:** the duplicate link, "Experimental" status, and possibly TEST rationales on the 2 saved decisions _(unverified)_ | Clean up in Ontology Manager, about 15 min | Foundry UI |

## 4. Overclaims and inconsistencies (quote both places)

1. **Trace.** The close says "every flag opens to its source" (deck p1, p15; script s01, s16; R09 p26). The same deck says "the 394 reports do not open from her screen yet" (deck p4; script s04). **Fix:** "every flag opens to the label it was checked against, and its counts trace to FAERS rows."
2. **Freshness.** "So that is her morning today: recalls and labels daily, signals quarterly" (guide A7, R09 p16), and "Labels are daily" (script s03). Against: "No … schedules … yet" (note p1) and "Not built: health page, schedules" (deck p26). Nothing refreshes unless someone runs a build. **Fix:** "the sources publish daily; our builds are run by hand in the pilot."
3. **Start-up.** "clean builds take at most 32 seconds, mostly start-up" (script s12). D048 says "Measured: … most time is container start-up". Against: "Foundry start-up time on its own — Not measured" (R06 p12). This contradicts the project's own rule, "measured, not asserted".
4. **AI target.** "Result: Met for the pilot: F1 0.97" (R08 p3) sits beside "only on 35 items … Claude-written key" (deck p9) and D015, which is still **Proposed** and wanted a TAC 2017 / OnSIDES benchmark that was never run. **Fix:** "met on the pilot key; not independent."
5. **Label counts.** "1,321 label versions" (note p1) vs "1,231 label versions effective" (deck p5, script s05). Both are right (pulled vs dated events), but they read like a typo. Name the difference once.
6. **Where partitioning lives.** D048 appears in the deck (p12) and R06 (p10), but the required hand-in file [optimization-log.md](../../08-optimization-log/optimization-log.md) has no partitioning entry.

## Weakest point and the demo question
**Weakest point:** Parts B and C still do not meet. The AI is an evidence layer that the officer never sees for the drug in the demo.
> "Your AI read two labels for a drug you don't demo, and the signal list is the same without it. What is it for, and how often is it wrong on the sections that decide 'not in label'?"

The scripted answer (deck p9) is defensible under the brief's "partial build with clear reasoning" line. It is the same answer as in v1, though, and a strict reviewer will notice that the fix pass changed the words, not the evidence.

**Assumptions:** I did not open Foundry. I did not check whether the 2 saved decisions still carry TEST rationales, or whether the object-type descriptions were filled. I did not re-check the EMA/WHO facts myself; they are taken from DECISIONS learning 2026-11-05. Page numbers are PDF pages.
**What I'd check next:** (1) after hole 1 and hole 2, re-score Application and AI reliability (both can reach 4); (2) one timed rehearsal against live Foundry; (3) a fact-check of the §4 fixes across deck, script, guide and R09 together.

**Compass:** 📍 Phase 2 → hand-in Phase D · review loop · Next: D041 v2 decision + rehearsal · Blockers: pharmacist not named; AI ↔ screen gap (unchanged since v1)
