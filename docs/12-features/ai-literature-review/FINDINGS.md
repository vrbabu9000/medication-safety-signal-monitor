# F01 — What 6 sample reviews found (2026-11-05)

**TL;DR:** Of 6 top-ranked "not in label" signals, the AI review backed by papers rated **2 real**, **1 plausible (FAERS evidence only)** and **3 noise or not enough evidence**. It also caught **1 likely false positive in our own pipeline**: tirzepatide · Allodynia, where the Zepbound label lists "dysesthesia". Caveat: n = 6, picked by Claude, judged by Claude from abstracts only.

| # | Signal (rank, a) | Papers | AI verdict | Effect on the officer's queue |
|---|---|---|---|---|
| 01 | Semaglutide · Optic ischaemic neuropathy (1, 394) | 113 | **Real concern**: mixed cohorts; 2 FAERS studies agree; EMA acted | Keep #1, add a context note |
| 02 | Semaglutide · Cyclic vomiting syndrome (3, 145) | 1 | **Plausible**: one FAERS study agrees (ROR 64.8); label lists "vomiting" | Keep; pharmacist decides on a synonym |
| 03 | Fentanyl · Anaesthetic complication neurological (1, 244) | 38, none specific | **Not reviewable**: a setting term, not a drug effect | Mark "context term" |
| 04 | Tirzepatide · Allodynia (5, 55) | 9 | **Real AND probably in the label** as "dysesthesia" | Propose synonym → "possibly in label" |
| 05 | Morphine · Ewing's sarcoma (1, 26) | 8 | **Noise**: confounding by indication (morphine treats the cancer pain) | Demote |
| 06 | Buprenorphine · SMA syndrome (2, 11) | 1 (fentanyl, surgery) | **Not enough evidence** | Low priority |

Details: [sample 01](samples/01-semaglutide-naion.md) · [samples 02–06](samples/02-06-five-more-signals.md) · raw evidence in [evidence/](evidence/).

## Run v2: + Europe PMC, FDA Potential Signals, OnSIDES ([details](samples/rerun-v2-multi-source.md))
- **No verdict flipped.** Samples 01 and 04 got **regulator-level** support: FDA listed NAION (Q4 2024) and Dysaesthesia (Q1 2024) for the GLP-1 class. The UK labels list NAION and the EU tirzepatide label lists dysaesthesia (OnSIDES).
- **Europe PMC added 0 new on-topic papers.** Its bigger counts were full-text noise that the gate removed.
- **Best add-on: FDA Potential Signals.** One cached scrape per quarter, $0 per review, and it answers "is FDA already on this?".
- OnSIDES is good for "yes, labeled abroad" but weak for "no" (tirzepatide has 0 US labels in it).

## What we learned
1. **It splits the queue.** Half of these top signals turned out to be noise or unreviewable. That is the officer's first question ("which flags matter?"), now with a citation per answer.
2. **It finds pipeline bugs.** Sample 04 exposed a missing synonym row that exact-text matching can't see. The review is a QA tool for the label check as well as a triage aid.
3. **Papers answer "is it real?", never "is it on the label?".** Label status stays with DailyMed (D037). The review may only *propose* a synonym row, and a person accepts it (D043).
4. **Some signals need a rule, not an AI.** Sample 05 (cancer terms on opioids) and 03 (anaesthesia-setting terms) point to two cheap rule-based cautions. One rule handles many signals for $0.
5. **Search quality matters most.** 03 returned 38 off-topic papers, and 05 matched a scorpion. A deployed version must (a) check that the drug *and* the event both appear in the abstract, and (b) say "no specific evidence" when they don't.
6. **Cost is not the constraint.** ~$0.09 per review on Opus 5.5 and ~2 s of PubMed time. The constraint is pharmacist minutes ([cost-estimate](cost-estimate.md)).

## What this does not prove
- 6 hand-picked signals is not an accuracy measure. A real eval needs ~30 random ranked signals with a pharmacist answer key (like [A008](../../05-approaches/A008-gold-set-v2-cross-source-traces.md)).
- The "AI" here was Claude in a chat session, not a deployed AIP function. The prompt and output format are not built yet.
- Abstracts only. One reviewer.

## Not changed yet (needs your OK)
- The Allodynia → "dysesthesia" synonym row (syn_v3) is **not** added. It would go through the normal A014 review.
- No decision logged. This stays an exploration until you choose to build it.
