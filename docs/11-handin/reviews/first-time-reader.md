# 🧑‍🎓 First-Time Reader review of the hand-in PDFs

**Reviewer lens:** a capable engineer who has never seen Palantir Foundry, pharmacovigilance or this project.
**Read on:** 5 Nov 2026, in this order: architecture note → R01 → R02 → R03 → R04 → R05 → R06 → R07 → R08 (118 pages).
**Method:** every page rendered to PNG and looked at at roughly print size, plus extracted text. Page numbers are the PDF page numbers (the "n / N" in the footer).
**Scope:** this is a report only. Nothing was rewritten.

Severity key:
- **Blocker**: I could not follow the argument, or I came away believing something false.
- **Major**: I could follow it, but only by guessing, flipping to another report, or trusting a number I could not check.
- **Minor**: friction, polish, or time wasted.

---

## TL;DR

The engineering is clearly careful and unusually honest. As a newcomer, though, I had a hard time with four things:

1. **There is no front door.** The architecture note looks like the place to start, but it is the densest page in the set (about 30 ID codes on one page). It also points to "reports R0-R7" when the files are R01-R08.
2. **The trust labels (OBSERVED / DESIGNED / ASSUMED …) mean different things in different reports.** In R03-R05, DESIGNED means "not built yet". R01, R02, R07 and R08 use it for things that are built. These labels are the set's trust device, so this matters.
3. **The drug-safety domain is never taught before it is used.** R01 teaches Foundry only. R02 then opens with PRR, 2×2 tables, suspect roles and MedDRA, all wrapped in D/DQ/A codes. The 13 drugs are never listed by name anywhere.
4. **The headline numbers drift in meaning between reports.** Examples: what a "signal" is (1,952 or 1,073), what "active recall" means, where the ranked queue started (1,355 or 1,210), the Workshop version (v0.8.0 or v0.9.0), and what the F1 of 0.97 covers.

R06 (optimization) and R07 (data judgment) are the easiest to read. R07 chapter 1 is the best "why this matters to the officer" page in the set, and it comes eighth.

---

## 1. Cross-set issues (ranked)

### Blockers

| # | Issue | Where | Why it blocks |
|---|---|---|---|
| X1 | **No single starting point or reading guide.** No document says "start here, then read these in this order". The architecture note (the natural start) assumes you already know D020, DQ34, O2, D016 v3, PRR, Evans, F1, "step 6 gate", "banded", "suspect drugs" and "judging row". It also sends you to "reports R0-R7" and "diagrams 30-38", but the reports are numbered R01-R08 and the diagrams are not in the PDF set. | Arch p1 (build-facts footer, decision boxes 1-4, "Why these four" box) | My first page was the hardest page. I had nothing to orient by. |
| X2 | **Evidence and status labels change meaning between reports.** R01 p1: DESIGNED = "our choice", ASSUMED = "Foundry behaviour we read about". R02 p1 and R07 p1: DESIGNED = "a choice", ASSUMED = "not verified". R03 p3, R04 p2, R05 p13: DESIGNED = "designed … **not built or run yet**", ASSUMED = "a choice we made", OBSERVED = "read directly from a public source". R06 and R08 have no legend. Examples of the clash: R03 p5 tags the key checks in `ontology_objects.py` as DESIGNED (under R03's own legend that means not built, but they are built). R08 p6 says "DESIGNED built". R01 uses TESTED, DERIVED and PLANNED without defining them. Some gates contradict their own label: R03 p15 and R05 p12 are labelled PLANNED with Result "Met", while R04 p2 is labelled TESTED although the timed test "is not done yet". | R01 p1, p2, p15, p16; R02 p1; R03 p3, p5, p15; R04 p2, p3; R05 p12-13; R07 p1; R08 p6 | These labels are how the set asks to be trusted. When they are inconsistent, I cannot tell what is built, what is measured and what is planned. |
| X3 | **No domain primer.** R01 teaches Foundry and only Foundry. R02 starts using domain terms straight away: PRR, the 2×2 table (a, b, c, d), Evans, chi-squared, primary/secondary suspect, concomitant, MedDRA PT, LOINC section codes, PLR, setid, NDC, application number, reference label, buckets, mass reports. Most are defined somewhere, but they are spread over R01 p17, R02 p5 and p9, R03 p2, R04 p9 and R08 p4. The PRR formula first appears in R02 p9, yet R01 p12 already quotes "the 2×2 counts (a = 394 …; PRR 112.5)". **The 13 drugs are never listed by name.** Exenatide is first named on R07 p4, and dulaglutide, liraglutide, buprenorphine and hydromorphone appear only inside screenshots. | R01 p2, p12; R02 p2-p9; R07 p4 | A newcomer cannot judge any signal without knowing what PRR measures and which drugs are in scope. |
| X4 | **Headline numbers are defined differently in different places.** (a) *Signal*: "Evans and **not in label**" in Arch p1, R01 p18 and R03 p2/p7, but "Evans and not in label **(or possibly in label)**" in R02 p9. How 1,952 becomes 1,073 is only broken down in R02 p9 and in the R02 Fig 2 diagram. (b) *Active recall*: "status Ongoing" in R02 p7 and R07 p7, but "Is Active = true (**status not terminated**)" in R04 p9. The second reading would also count Completed. (c) *Ranked queue history*: "1,355 → 1,073" in Arch p1 and R04 p12, but "1,210 → 1,115 → 1,073" in R02 p14. 1,355 is not in the R01, R02 or R03 numbers tables; it only appears in R05 p7 and R07 p2. (d) *Workshop version*: v0.8.0 in R01 p13 and p18, but v0.9.0 in Arch p1, R04 p2 and numbers.json. R01 looks like it was built from an older numbers.json. (e) *F1 0.97*: Arch p1 and R01 p15 put it next to "448/448 grounded" as if it covered the 448 items. It actually covers 35 items in the Boxed Warning and Contraindications sections of 2 labels. That scope is stated only in R08 p4, R07 p8 ("4 short sections") and R05 p8. | Arch p1; R01 p13, p15, p18; R02 p7, p9, p14; R03 p2, p7; R04 p9, p12; R05 p7-8; R07 p2, p7, p8; R08 p4 | These are the numbers a reviewer will quote. I got different meanings depending on which report I read first. |

### Majors

| # | Issue | Where |
|---|---|---|
| X5 | **ID codes are used long before they are explained, and the files they point to are not in the PDF set.** D###, DQ##, A###, O#, G1-G4, "step 6 / step 8 / step 9 / step 11", "trace T13", "conventions §6", "project build order v1, section 4", "A00x". The first explanation of D/DQ/A is R05 p1 and R07 p1, after about 60 pages of use. "Step N" (a build timeline) is never explained, but it carries meaning ("step 9 build", "step 6 gate", "13 names since step 9"). | Arch p1; R01 p3, p7, p9; R02 p4, p11; R03 p4, p10, p15; R04 p12; R05 p10, p12; R06 p9 |
| X6 | **The key diagrams cannot be read at print size.** On paper, the box text in diagrams 30, 31, 32, 33, 34, 35 and 37 comes out at about 3-4 pt. The worst case is **R02 Fig 2** (p8), the signal pipeline and the most important picture in the set: it is squeezed into a third of the page with half the page left blank. It only became readable when I zoomed to 220 dpi. Foundry screenshots (R01 Figs 1, 2, 5, 6, 9; R03 Figs 2, 5; R04 Figs 1-4) cannot be read on paper either, so captions like "25 properties", "status Experimental" or "Labels also read by AI 0" cannot be checked against the picture. | R01 p4, p6, p7, p10, p11, p12, p16; R02 p3, p8, p11, p12, p13; R03 p4, p8, p9, p14; R05 p6, p8, p9; R06 p6; R07 p6; R08 p7 |
| X7 | **Wasted repetition** (detail in section 3). The same 6 diagrams and 4 screenshots are reprinted 2-4 times. The three questions, the "review queue, not findings" caveat, the AI caveats, the 88 s vs 32 s result and the duplicate-link confession each appear 4-7 times. Every report ends with 1-3 pages of raw `key = value` dumps from numbers.json. About 15-20 of the 118 pages are repeats. | see section 3 |
| X8 | **"Why does this matter to the safety officer?" goes unanswered for several facts that would change her morning.** Each one is buried in a gap table instead of being said up front. (a) Signals only move when a new FAERS quarter lands, and FAERS is 130 days behind (R02 p12). So "what changed since yesterday" never includes new signals in practice (R04 p13, a row in a table). (b) **Only the project owner can submit a triage decision**, so the officer herself cannot use the write-back (R03 p11, R04 p13). (c) The AI's stated value is "the exact quote as evidence", but the quote is not on her screen (R04 p13). A not-in-label signal has nothing to quote (R03 p14). So for question 1 the AI adds nothing she can see. (d) FAERS has been replaced by AEMS since Mar 2026, and the future feed is "unverified". That is only in the R07 appendix (p10, DQ20) and a "likely" in R07 p6. (e) What should she *do* about NAION? Is it already known elsewhere? No report says. (f) Monitoring alerts go to the "project owner" (R08 p7 diagram), not to her. | R02 p12; R03 p11, p14; R04 p13; R07 p6, p10; R08 p7 |
| X9 | **The October prototype is used as evidence but never described.** "Counts equal the October prototype exactly" is used as proof in R02 p5 and p10, R05 p6 and R07 p3. I never learn what it was, who built it, or why agreement with it proves anything (it could share the same bugs). | R02 p4, p5, p10; R05 p6; R07 p3 |
| X10 | **Diagrams contradict text or are stale.** R02 Fig 4 (p11) and R05 Fig 2 (p8) use diagram 33 **v1**, which still says O3 is "being measured". Both captions apologise for it, while R06 p6 already uses v2. More cases are listed per document below. | R02 p11; R05 p8; R06 p6 |

### Minors (cross-set)

- The running page header lags one chapter behind the content. R01 p5 is headed "03" but contains ch. 04. R01 p7 is headed 04 but contains ch. 05. R01 p17 is headed 11 but contains the glossary (ch. 12). R02 p4/p5/p12/p14 show the same pattern.
- Every numbers appendix says "baseline-gate.md.." (double full stop). R01 p18, R02 p15, R03 p16, and so on.
- The appendices say the numbers came from "Foundry SQL (repo SQL panel)". R01 p5 says they were read on the dataset-page SQL console and that the repo SQL panel was "much slower".
- Large blank areas: R02 p8 (bottom half), R02 p10 (two thirds), R04 p4-p7 (half of each page), R06 p6, R08 p7 (two thirds).
- Internal project process shows through: "boss suggestion", "lost week", "'no rush'" (R05 p10); "the demo director (Cl) sets the final order" (R04 p8, Fig 5); "Claude-written key" with no word on why an LLM wrote the key.

---

## 2. Per-document findings

### Architecture note (1 page, landscape)

| Sev | Where | Finding |
|---|---|---|
| Blocker | footer | "reports R0-R7", but the files are R01-R08 (plus R00-sample and R09). "Diagrams 30-38" are not in the hand-in PDFs. |
| Blocker | decision boxes 1-4 | About 30 codes on one page (D020, D027, DQ34, D021, D022, D023 v2, DQ36, D037, D041, D043, D040, D042, D045, D044, O2, D016 v3, D031, D029). A newcomer cannot decode any of them from this page. |
| Major | box 3, "Evidence" | "F1 0.97 vs target 0.85" is undefined (F1 is not in the glossary). The scope (35 items, 2 short sections × 2 labels) is missing. "Small Claude-written key" raises "an AI grading an AI?", and the note does not answer it. |
| Major | box 3 + "not to do" | "ranked 1,355 → 1,073" gives no starting point or reason. Is fewer better? Why? There is no source on the page, and R02 later gives 1,210 as the start. |
| Major | "What we chose not to do", bullet 2 | "A signal = reported more often than expected and not in the label", yet the build facts say "1,952 signals, 1,073 ranked". By this definition, what are the other 879? |
| Major | figure, AE Stat box | "a, b, c, d, PRR" is undefined. "Evans" (in ontology_signals) is undefined. The glossary names PRR but does not say what it measures. |
| Major | box 2 | "suspect drugs only" (suspect versus what?), "reports listing 30+ drugs leave the main count" (why 30?). "Q2 replaced 26,681 cases" has no denominator. |
| Major | box 4 | "step 6 gate" is undefined. "evaluation_id (a hash of the evidence)": why the officer cares is not said. |
| Minor | box 3 | "a synonym a person banded": "banded" is undefined, and the person was in fact Claude (R02 p9). |
| Minor | caption | The glossary sits in about 6 pt caption text *below* the figure. I only found it after struggling through the figure. |
| Minor | "Why these four" | "judging row" and "Runners-up" assume the reader knows the rubric. |
| Minor | "OBSERVED" badges | Undefined on this page. |

### R01 Foundry from scratch (19 pp)

Does R01 prepare me for R02? **For Foundry, yes, and well.** The "What it is / In our project / What to click / How we know" pattern is excellent. **For the domain, no.** R01 says it is "not a report on drug-safety results (see R02 and R07)". R02 is a pipeline report, so the domain falls between the two.

| Sev | Page | Finding |
|---|---|---|
| Blocker | p1 vs p2, p15, p16 | The legend defines OBSERVED/DESIGNED/ASSUMED only. TESTED (p2, p17), DERIVED (p15) and PLANNED (p16) are used without definition (see X2). |
| Major | p2 | "13 drugs (8 opioids and 5 GLP-1)": no names, here or anywhere in R01. |
| Major | p3, p7, p9, p11, p14, p15 | D010, D036, A014, D038, D040, D042, O1 are used with no explanation of what a D/A/O code is. |
| Major | p4 vs p10, p11 | `ontology_triage_decisions` is "Empty on purpose" (p4), yet the table on p10 says "(empty; edits on) … 2" objects. The explanation ("Action edits live in the Ontology, not in the dataset") only arrives on p11. |
| Major | p4 vs p9 | `raw_openfda_enforcement` has 930 rows (p4), but there are "900 distinct recalls" (p9). The 30-row gap is not explained in R01. |
| Major | p5, p8, p11, p12 | "baseline gate" is used as evidence four times. What a gate is is first explained in R03 p1. |
| Major | p6 "Watch out" | "Incremental FAERS 88 s vs 32 s" comes before I know what FAERS quarters are or why rows get replaced. |
| Major | p7 Fig 3; p10 Fig 4 | Diagram text is about 3-4 pt at print size. Fig 3 also contains "XML reuse: O3, measuring", "D044" and "identity change → replay", none explained. |
| Major | p10 table vs Fig 4 | Product count: the table says "see Fig. 4". The figure (zoomed) shows 658, and R03 p6 says the number was "not captured, so not quoted". Three different treatments of one number. |
| Major | p11 | "Subject type, subject key and evaluation id … are locked". evaluation_id is not defined in R01 or in its glossary. |
| Major | p12 | "the 2×2 counts behind the statistic (a = 394 …)": the 2×2 table, b, c and d are undefined in R01. "Reference Label" is undefined. |
| Major | p13 | Workshop "published v0.8.0" and appendix p18 `app.workshop_version v0.8.0`. Elsewhere it is v0.9.0. R01 looks stale against numbers.json. |
| Major | p13 Fig 7 | "26 changes in the last 30 days" sits next to 2,898 change events (p10) with no link between them, and does not match "since yesterday" (p2). |
| Major | p16 | "FAERS reports with no reporter type rose 34% → 72%". "Reporter type" is undefined, and so is why the officer should care. |
| Major | p17-18 glossary | Missing: evaluation_id, gate/baseline gate, suspect role, reference label, bucket, mass report, ranked, NAION, GLP-1, chi-squared, F1, 2×2 (a-d), medallion. The Signal entry ("not found in the label") disagrees with R02 p9. |
| Minor | p1 | The "What this is" column lists "Built from docs/…/R01-foundry-f rom-scratch.py", which breaks mid-word and is not a "what this is". |
| Minor | p5 | The 1.5 s SQL console figure and the "much slower" repo panel have no source. The p18 appendix says the numbers came from the repo SQL panel. |
| Minor | p6 | "about 1 minute vs about 4 for Spark": honestly hedged, but there is no source. |
| Minor | p14 vs R04 p11 | JSON paste "replaced about 60 clicks" here, "roughly ten clicks per column" in R04. The two are compatible, but read like two different claims. |
| Minor | p15 | "default model GPT-5.6 Sol" is trivia that does not help the reader. |
| Minor | p18-19 | Two pages of raw key/value dumps (`ai.d015_target_f1`, …). |

### R02 Pipelines: raw to ontology (17 pp)

| Sev | Page | Finding |
|---|---|---|
| Major | p1 vs p2 | The legend lists four labels. The p2 gate is labelled TESTED, which is not in the legend. |
| Major | p2 | "evaluation_id" gets one clause. "prr_evans_v2" and "text+ai_v1+syn_v2" are version strings shown before the reader knows what they version. |
| Major | p4 | "13 names since step 9", "A013", "DQ31", "D018", "ATC classes", "D039 G2", "G3", "labeler: key", "trace T13", "setid", "harmonised openfda.* field": six undefined codes or terms on one page. |
| Major | p4 | "In the October prototype": the first mention of a prototype, never described (X9). |
| Major | p5 | `prod_ai` is undefined. "pemphigus" is unexplained, and so is why a skin disease topping an oxycodone list is a red flag. |
| Major | p6 | "LOINC code" and "PLR" are undefined. "DQ19, DQ40, DQ42" are codes only. |
| Major | p8 Fig 2 | The most important diagram in the set is shrunk to a third of the page (box text about 3 pt) while half the page is empty. Read at 220 dpi, it shows things the text does not: "2,533 meet Evans", "1,427 stats in label", "211 stats possibly", "Caution, not ranked 231", "39 names → 13 ingredients". |
| Major | p8 Fig 2 vs p9 | The diagram says NAION was checked against "3 reference labels, 0 safety sections". The text says "none of the 36 safety sections in **any** semaglutide label". Those are different scopes, and the reader cannot tell which one the trust rule relies on. |
| Major | p8 Fig 2 vs p9 | The diagram says "medium → possibly (211 stats)". The text says "108 possibly in label" signals. Stats and signals are different units with no bridge between them. |
| Major | p9 | "A signal is ranked only when … under 50% from mass reports". p5 says mass reports (30+ drugs) leave the main count. So how can a signal be more than 50% mass reports? `a_mass_reports` is kept on the side, but the share's formula is never given. |
| Major | p9 | "Ranked signals are ordered by chi-squared within each drug". Why chi-squared and not PRR or its lower confidence bound? Not explained, though it decides what she sees first. |
| Major | p9 | 1,952 → 1,073: the breakdown (108 possibly, 231 caution, roughly 540 tagged) is only in the zoomed figure, never in text. |
| Major | p11 | "O3a FAERS column pruning" is in the table with no text about it in R02. "819,883 DEMO rows" in Fig 4 uses "DEMO" undefined. The O3 caveat ("baseline came from an earlier build, not back to back") is honest here but missing in R05 p9. |
| Major | p12 | The PROPOSED band: "awaiting the owner's OK". Who is the owner? A newcomer cannot tell whether the change feed (question 3) counts as delivered. |
| Major | p12 | "freshness: openFDA 8 days, FAERS 130 days after quarter end": is that acceptable? What does it mean for "since yesterday"? (X8a) |
| Major | p13 | "Change a synonym → every evaluation_id changes; old decisions keep the old id". What does the officer then see? Does her decision disappear from the signal? The answer is promised in R03 p11 ("the screen can show the evidence moved"), but R04 never shows it. |
| Minor | p7 | Recall "D-0040-2027 (reported 2026-10-21)": a 2027 id with a 2026 date looks like a typo. The FDA fiscal-year numbering is not explained. |
| Minor | p12 | "Since *my* last review": the voice switches to first person. |
| Minor | p3 Fig 1 | Same diagram as R01 Fig 3 and R03 Fig 1. |
| Minor | p15-17 | Three pages of key/value dump. |

### R03 The Ontology (17 pp)

The best-structured report. It explains gates (p1), has a real word list (p2) and a worked trace (ch. 6).

| Sev | Page | Finding |
|---|---|---|
| Blocker | p3 | This legend defines DESIGNED as "not built or run yet" and ASSUMED as "a choice we made". Both contradict R01, R02 and R07 (X2). Under this legend, p5 says the key checks are not built, p10 says the Reference Label design is not built, and p11 says evaluation_id is not built. |
| Major | p4, p10, p11, p12 | "Step 6 gate (A010)", "step 11", "step 8": the timeline is never explained. |
| Major | p6 | Recall title "D-0338-2026 · Class II · Ongoing": "Class II" is undefined here (R04 p6 says "Class I is the most serious"). |
| Major | p7 | Signal = "meets the Evans rule and is not found in the label". Same conflict with R02 p9 (X4a). |
| Major | p11 | "Who can submit: the project owner only, for now". This is buried in a table. It means the persona cannot use the feature (X8b). |
| Major | p11 | The save test was "a test decision on **recall** D-0338-2026", yet Triage Decision only links to Signal (p10) and "Triage on recalls" is future work (p15 item 6). That is confusing. |
| Major | p11 | "the screen can show that the evidence moved since her decision (D042) DESIGNED": it is never shown in R04. Does it exist? |
| Major | p11 options table | "Triage Decision backed by an 'empty datasource' / The rebuild test would mean nothing": I could not follow this reasoning. |
| Major | p14 | "a not in label signal has no label quote (there is nothing to quote)". This quietly means the AI quote never helps question 1 (X8c). |
| Minor | p6 note | "Product count … not captured into numbers.json" while diagram 31 (p9) prints 658. |
| Minor | p15 | The gate is labelled PLANNED with Result "Met". |
| Minor | p15 | "conventions §6" and "D031 v5" are undefined. |
| Minor | p4, p8, p9, p13, p14 | Every figure is a reprint from R01 or R02. |

### R04 The application (14 pp)

The best "user" report. Ch. 4 ("What each number means / Do not read it as") is excellent and should be borrowed by every other report.

| Sev | Page | Finding |
|---|---|---|
| Major | p2 vs p4 | The question is "what has changed **since yesterday**", but the Morning brief card counts "**26 changes in the last 30 days**". Neither page says how the card answers question 3. |
| Major | p3 | The HMW table marks "show how confident we are …" and "make 'not on the label' provable" as TESTED, while p2 and p12 say nothing was tested with a user. TESTED here seems to mean "built". |
| Major | p3 | "MedWatch", "Test (canvas)" and "Dana … (PharmD)" are undefined. "fifteen minutes each morning" (p2) has no source; the persona is fictional (p3). |
| Major | p4 | "FAERS is quarterly (here through 2026Q2)". On 5 Nov 2026 the signal list is a quarter-plus old, and nowhere does the report say what that means for her morning (X8a). |
| Major | p8 Fig 5 | The demo map: stops 8-14 are "under the hood", "Rubric rows in italics … the demo director (Cl) sets the final order". These are internal instructions and mean nothing to a reader. Box text is about 4 pt. |
| Major | p9 | "126 active recalls = Is Active = true (**status not terminated**)" conflicts with R02 p7 and R07 p7 ("Active = Ongoing"). |
| Major | p9 | "a low bound well above 1 means it is not chance" is a loose statistical claim. With PRR and FAERS, the bias is reporting bias, not chance. |
| Major | p12 | "One ranked list mixing **12** drugs": why 12 of 13? The answer (exenatide has no reference label) is only in R07 p4. |
| Major | p12 | "1,355 to 1,073 (R05 explains each step)": the number has no source in R01-R04. |
| Major | p13 | Two gaps that are really headline facts are rows in a gap table: "Only the owner can submit a decision" and "AI evidence not on screen" (X8b, X8c). |
| Minor | p4-p7 | Each step page is half blank under a screenshot that cannot be read on paper. |
| Minor | p11 | JSON snippet: helpful for builders, but "type id is in the object type's URL" is the only instruction. |

### R05 Decisions, and what we did not do (15 pp)

| Sev | Page | Finding |
|---|---|---|
| Major | p1 | This is the **first page in the set that explains what D###, DQ## and A### are**. It arrives after about 60 pages of use. |
| Major | p2 | "D037 **proposed**". D037 is step 1 of the label check, the core of question 1, and the architecture note presents it as chosen. A newcomer reads "the core rule is not yet accepted". |
| Major | p2 | "Accepted (via D039)": D039 is never explained in R05. |
| Major | p3 | "ATC N02A", "SrLC database", "D014 chose the mix", "D012" are undefined. |
| Major | p4 vs R02 p4, R07 p3 | DQ34 is "measured on the 2026Q2 FAERS files" here, but "in the October prototype" in R02 and R07. |
| Major | p5 | "397,224 Q1 cases" appears only here and in R07. No other report gives the Q1 total. |
| Major | p8 | "recall 35/35". **Recall** (the statistic) sits in a report full of **recalls** (FDA product withdrawals). I stumbled on it, and a short gloss would help. |
| Major | p9 | O3 "3 m 23 s to 1 m 23 s (59% less) … OBSERVED", with no mention of the not-back-to-back caveat given in R02 p11 and R06 p7. |
| Major | p10 | The decision-change table mixes design decisions with schedule history ("Boss suggestion", "Lost week, then 'no rush'; slice passed steps 6 to 8 (D039 G1)"). It means nothing to an outside reader. |
| Major | p11 | "AEMS export", "Part D", "OnSIDES" (defined only in R08 p9) and "SrLC" are undefined. |
| Minor | p12 | "A separate monitoring design (**A00x**)": a placeholder id left in. |
| Minor | p12 | The gate is labelled PLANNED with Result "Met". |
| Minor | p6, p8, p9 | Figures reprinted from R02, and Fig 2 is the stale v1 (X10). |
| Minor | p13 | The third full copy of the 7-label legend. |

### R06 Optimization log (12 pp)

The clearest report. It defines its terms on p2, has a method chapter (p3) and threats to validity for every entry. The "When it would win" note on p5 is good.

| Sev | Page | Finding |
|---|---|---|
| Major | p1-p11 | It uses OBSERVED/DERIVED/DESIGNED/ASSUMED/TESTED with no legend (X2). |
| Major | throughout | "Why does this matter to the officer?" is answered once (p7: "Freshness unchanged"). O1 (tokens) and O2 (seconds) are never tied to her morning. Example: does a faster DailyMed pull mean a label change reaches her the same day? |
| Major | p5 | "819,683 DEMO rows" versus 792,346 current cases. "DEMO" is half-explained ("the case file"). The roughly 27k gap is not explained here. |
| Minor | p4 | "prompt p1 / p2" and "A011": the p2 token count "is in A011, not in numbers.json", a number the reader cannot see. |
| Minor | p9 | "project build order v1, section 4" is a document the reader does not have. |
| Minor | p6 | The page is mostly blank under a 4 pt diagram. |

### R07 Data judgment (13 pp)

**Ch. 1 (p2) is the best page in the set for a newcomer.** It sorts problems by "what would this do to the safety officer's morning?". It should be near the front of the reading order, not eighth.

| Sev | Page | Finding |
|---|---|---|
| Major | p2 | "no reference label (exenatide)" is the first time a drug outside the examples is named. The full drug list is still missing. |
| Major | p3 | "8.7% phantom rows (422,872 vs 389,074)" in the prototype, against "397,224" Q1 cases in Foundry. Three different base numbers for the same idea, unreconciled. |
| Major | p4 | "So signals exist for 12 of our 13 drugs": this explains R04 p12 "12 drugs", but only here. |
| Major | p6 | "Likely the FDA's switch from FAERS to AEMS (DQ20) ASSUMED". The appendix (p10) says FAERS was **replaced by AEMS in Mar 2026; future feed unverified**. For a newcomer this is the biggest long-term risk in the project, and it sits in an appendix row (X8d). |
| Major | p6 | "Recalls 10 vs 3 … the rise is real". So what should the officer do with that? |
| Major | p8 | "NAION spans about 10 optic terms": so the flagship signal may be undercounted or split. That is not said where NAION is showcased (R02 p9, R03 ch. 6). |
| Major | p8 | "Answer key covers 4 short sections only" is the clearest statement of the F1 scope, and it sits in a "left as is" table (X4e). |
| Major | p10 | DQ21 "Lawyers filed most 2021 oxycodone reports" is big for an opioid reader and appears only as a register row. |
| Minor | p7 | The recalls screenshot is reprinted from R04. |
| Minor | p10-p11 | The register's own status column is stale ("Suspected" for handled items). This is acknowledged, but it is two pages to skim. |

### R08 AI reliability (10 pp)

Clear and honest. The p2 Q&A table is a model of plain language.

| Sev | Page | Finding |
|---|---|---|
| Major | p1-p9 | No label legend, yet p6 says "DESIGNED built" and "DESIGNED planned" in the same table (X2). |
| Major | p2, p3 | "The AI's job today is evidence, not decisions … the exact quote". This conflicts with R04 p13 (quote not on screen) and R03 p14 (a not-in-label signal has nothing to quote). The report never says that the officer does not currently see the AI's output. |
| Major | p4 | The key covers Boxed Warning and Contraindications of 2 labels, while "most of the 448 items" (p5) come from long sections. This is stated well here, but the earlier reports (Arch, R01, R02) quoted F1 next to 448 without it. |
| Minor | p3 | "assertion type" is undefined. |
| Minor | p7 | The page is two-thirds blank under a 4 pt monitoring diagram, a reprint of R07 Fig 1. |
| Minor | p8 | Run 2 tokens: "not in numbers.json", a number the reader cannot see. |
| Minor | p9 | OnSIDES is defined here for the first time, after Arch p1 and R05 p11 used it. |

---

## 3. Repetition that costs reading time

| Repeated item | Appears in | Suggest |
|---|---|---|
| Data-flow diagram 30 | R01 p7, R02 p3, R03 p4 | Print once (R01 or Arch); elsewhere, "see Fig X in R01" |
| Signal-pipeline diagram 32 | R02 p8, R05 p6 | Once, full page, in R02 |
| Incremental diagram 33 | R02 p11 (v1), R05 p8 (v1), R06 p6 (v2) | Once (v2) in R06 |
| Change-feed diagram 34 | R02 p12, R05 p9 | Once |
| Monitoring diagram 35 | R07 p6, R08 p7 | Once |
| Ontology diagram 31 | R01 p10, R03 p9 | Once, in R03 |
| NAION app screenshot | R01 p14, R02 p10, R03 p13, R04 p5 | Once, in R04 |
| Object Explorer / Ontology Manager / Recalls screenshots | R01 + R03; R01 + R03; R04 + R07 | Once each |
| The three questions + trust rule | Arch, R01 p2, R02 p2, R03 p2, R04 p2, R08 p2 | Once, in a front page |
| "1,073 is a review queue, not findings" | Arch, R02 p2, R03 p2, R04 p2 and p9, R05 p7, R07 p2 | Keep once plus a one-line reminder |
| AI caveats (2 labels, Claude key, no effect on list) | Arch, R01 p15, R02 p6, R05 p8, R07 p8, R08 throughout | Once, in R08 |
| 88 s vs 32 s incremental | Arch, R01 p6, R02 p11, R05 p8, R06 p5 | Once, in R06 |
| FAERS counting rules D021-D023 | Arch box 2, R02 ch. 4, R05 ch. 4, R07 ch. 2 (three full treatments) | Once, in R02, with R05/R07 pointing back |
| Ranked-queue history table | Arch, R02 p14, R04 p12, R05 p7, R07 p2 | Once, with the same start number everywhere |
| Duplicate Signal→Drug link confession | Arch, R01 p11, R03 p10, R07 p8 | Once, in R03 |
| Build habits (700 MB, Force build) | R01 p8, R02 p14 | Once |
| 7-label legend table | R03 p3, R04 p2, R05 p13 (plus different short legends in R01, R02, R07) | Once, identical everywhere |
| Raw numbers.json dumps | Every report's last 1-3 pages | Drop, or one shared appendix |

---

## 4. Reading-order problems across the set

1. **There is no front door.** No README PDF, reading guide or index ties the nine documents together. The architecture note links to the wrong report numbers.
2. **R01 does not prepare me for R02.** R01 is a Foundry primer. R02 needs a drug-safety primer (FAERS, PRR, suspect roles, labels, recalls, the 13 drugs). Neither R01 nor R02 provides one. The nearest equivalents are R03 p2 (word list), R04 ch. 2 and 4, and R07 ch. 1, all of which come later.
3. **Codes are explained last.** D/DQ/A codes are first explained in R05 p1 and R07 p1, after Arch, R01, R02, R03 and R04 have used them heavily.
4. **The "why it matters" material is in the wrong place.** R07 ch. 1 and R04 ch. 4 are the pages that make everything else make sense, and they come seventh and fourth. R02 asks me to care about suspect roles and case versions before anyone tells me what goes wrong for the officer without them.
5. **The same story is told four times.** R02, R05 and R07 each walk through FAERS rules, the label check and the ranked-queue history from a different angle (pipeline, decision, data issue). Read in order, the third pass feels like déjà vu, and small numeric differences between the passes (X4) make me doubt all three.
6. **Each report is self-contained, and that is the cost.** Each re-introduces the officer, the three questions, the labels and the caveats. That suits a reader who opens one report, but it is tiring for one who reads the set.

---

## 5. The 5 changes that would most improve the set

1. **Add a 2-page "Start here" front document (R00).** It should hold: the three questions; the **13 drugs by name**; one data-flow picture at full page width; a single glossary of both Foundry and drug-safety terms (PRR with the 2×2 table, Evans, suspect roles, reference label, bucket, mass report, ranked, evaluation_id, gate, baseline gate); a one-line key to the ID codes (D/DQ/A/O/G, and what "step N" means); one evidence-label legend; and the reading order below. Fix the architecture note's "R0-R7" to match.
2. **Make one evidence-label legend and use it identically everywhere.** Then re-tag: DESIGNED should not mean both "built" and "not built", and gate labels should agree with their Result line. Put the legend in R06 and R08 as well.
3. **Pin down the headline definitions once and reuse them word for word:** "signal" (does it include possibly-in-label?), "ranked" (with the 1,952 → 1,073 breakdown in text), "active recall" (Ongoing only?), the ranked-queue start point (1,355, explained as the step 9 baseline), the Workshop version (rebuild R01 from the current numbers.json), and the F1 scope ("35 items, short sections of 2 labels") wherever 0.97 appears.
4. **Print the key diagrams large enough to read on paper,** and print each one once. Signal pipeline (32), data flow (30) and ontology (31) each deserve a full page at 8 pt or larger. Replace the stale v1 of diagram 33. Crop screenshots to the part the caption talks about. Use the space this frees by dropping the repeated figures and the raw numbers.json dumps.
5. **Add a "What this means for Dana" box to each report,** and move four buried facts up front: (a) signals only change quarterly and FAERS is about 130 days behind; (b) only the owner can submit a triage decision today; (c) the AI quote is not on her screen, and not-in-label signals have nothing to quote; (d) FAERS was replaced by AEMS in Mar 2026, so the feed's future is unverified. Lift R07 ch. 1's "effect on the officer" framing into the front document.

---

## 6. Suggested reading guide (one paragraph)

Start with the one-page architecture note only for its picture and the build facts, and skip the decision boxes for now. Then read **R07 chapter 1** (p2) and **R04 chapters 1-4** (p2-p9). Together they tell you who the safety officer is, what she sees on screen, what each number means and what the messy public data would do to her morning without fixes. Read **R01** next as your Foundry primer, using its "What to click" boxes if you have Foundry open. Then read **R02** for how the pipeline actually computes a signal, with **R03 chapter 6** (the NAION trace) as the proof that a flag reaches its source. After that, the three "judging" reports can be read in any order: **R06** (optimization), **R08** (AI reliability) and the rest of **R07** (data judgment). Read **R05** last, as the index of decisions behind everything you have already seen. Keep R01's glossary (p17) and R03's word list (p2) open while you read, and skip every report's closing numbers table.

---

*Files reviewed:* `docs/11-handin/architecture-note/architecture-note.pdf`, `docs/11-handin/reports/pdf/R01…R08*.pdf`. Rendered pages used for this review are in the session scratchpad (not part of the repo).
