# Safety officer review of the 20-minute demo (Part A, 0:00–7:30)

_Pharmacy Safety Officer view (Dana, PharmD) · 2026-11-05 · design-thinking stage: **Test** · read: [speaking script](../deck/speaking_script.md), [deck](../deck/MSSM-demo-deck.pdf) slides 1–5 and 14–16, [demo guide](../demo/demo-navigation-guide.md) A0–A7, [screens](../screens/), [R04](../reports/pdf/R04-application-workshop.pdf) ch. 1–3, [fix brief](phase-d-fix-brief.md)_

**TL;DR.** The demo is honest, which I respect. But as scripted it shows me three counts I cannot act on. Only one drug gets the full trace, and the trace stops one click short of the source both times. The FAERS reports behind NAION never open. The recall never opens at the FDA. The fixes are mostly words and two extra browser tabs. None needs a Foundry rebuild.

## 1. Does Part A answer each question in under 2 minutes?

| Q | What I see | What I'd do next | What makes me stop trusting it | Under 2 min? |
|---|---|---|---|---|
| 1 Not in label | Card "1073". On page 1 (unfiltered) each drug's rank 1: **Morphine · Ewing's sarcoma**, **Hydrocodone · Subchorionic haemorrhage** (3 reports), **Oxycodone · Shrinking lung syndrome**, **Tirzepatide · Weight increased**, **Dulaglutide · Early satiety**, Liraglutide · Diabetic metabolic decompensation | Filter to one drug, open NAION, read 394 / 20,892 / PRR / labels searched | Rank 1 for morphine is a childhood bone cancer. Two of the GLP-1 rank 1s are the drug's mechanism or the disease it treats. If 2–3 of 12 top flags pass my sniff test, I stop scanning the other 1,061 | **No.** I get one drug in about 45 s. All 12 drugs × ~89 ranked each is not a morning job |
| 2 Recalls | Card "126". The list is newest first. The newest is a compounded tirzepatide vial with "Matched to our products 0". At least one **Class I** (D-0788-2026, Fresenius Kabi, labeling mix-up) sits below 13 Class II rows | Filter Class I, check lots against my stock | The screen says "for my drugs" but has no purchasing data. "Matched to our products" means FDA-approved products, not my shelves. Class I should never sit below Class II | **No.** I see the count in 5 s, but I cannot answer "which recalls touch my stock" |
| 3 What changed | Past month: 26 events (15 label versions, 11 recalls). Columns `version_effective`, `source_date` | Open each new label version to see what changed | "Label version 11 effective" does not say what changed. Did they add a boxed warning? No signal changes ever appear | **Partly.** About 20 s to the list. Each label row costs a trip to DailyMed |

The 11.5 s load is fine. The real risk is reading time, and nobody has timed it (R04 ch. 2 "Human walk-through not run").

## 2. Wording a pharmacist would flag

| Where | Says now | Problem | Say instead |
|---|---|---|---|
| Script s04 | "reported about 112 times more often with semaglutide than with all other drugs" | Sounds like 112× the risk | "NAION is about 112 times more common **among semaglutide's reports** than among other drugs' reports. That is a reporting pattern, not 112 times the risk." |
| Guide A3 | "so it is not chance" | The interval does not rule out publicity-driven reporting (DQ04) | "so it is not a small-numbers fluke. It can still be inflated by news coverage." |
| Script s05 | "matches none of the products we carry" | We have no inventory data. It is an overclaim | "it matches none of the FDA-approved products we track for this drug. If you buy compounded GLP-1s from an outsourcing facility, check your purchasing records." |
| Script s05 / card 2 | "126 of the 900 recalls for our drugs are active" | Alarming. Most look like compounded products | "126 open FDA recalls name one of our 13 ingredients. Most are compounded products, not branded ones." |
| Screen, page 1 | `text+ai_v1+syn_v2` | Reads as "the AI checked it". It did not (0 labels) | Say aloud: "Ignore the 'ai' in that code. The AI has not read these labels." |
| Screen, page 1 | `not_in_label`, "Caution: No value", "Chi² (Yates)", "Bucket clinical" | Engineering labels | Do not read them out. Point only at reports, PRR and labels searched |
| Screen, form | "Subject Key 1991302\|…\|prr_evans_v2", "Evaluation Id f55055e199e8e9d3" | Means nothing to me | "The form locks which signal and which version of the numbers you are deciding on." |
| Script s04 | "This is a Foundry Action", "Triage Decision object" | Platform jargon in my part | "Your decision is saved with your name and the time, and it is never overwritten." |
| Script s05 | "rebuilt with no new data, it added zero events" | Engineer proof in the user segment | Move it to slide 11 |
| Deck slide 2 | "We built one screen that answers three questions in under two minutes" | Not measured | "…designed to answer three questions in under two minutes (not yet timed with a person)." |

## 3. Three questions a real safety officer will ask

| Question | Ready answer? | Where |
|---|---|---|
| **"NAION has been in the news since 2024. Europe's regulator (EMA's safety committee, PRAC) called it a very rare side effect of semaglutide in 2025. What did this tool tell me that I didn't know?"** _(ASSUMED: the EMA fact comes from my own knowledge and is not in the repo. Verify it before saying it.)_ | **No.** The script presents NAION as a find. The only nearby answers are "is it caused" ([rehearsal-plan](../demo/rehearsal-plan.md) l.106) and stimulated reporting (l.67). The backtest was cut (D031). | Answer: "It is a known positive. We use it because the pipeline should find it, and it does, at rank 1. It also shows the US labels she relies on still do not list it. Whether we would have flagged it *earlier* is unproven: we cut the backtest." |
| **"Which of the 126 touch product on my shelves, and how many are Class I?"** | **No.** There is no Class I count and no inventory link. Guide A6 only explains Ongoing and NDC matching. | Answer: "We cannot know your shelves without purchasing data. Today the Classification filter gives you Class I first." Rehearse that count. |
| **"Can I see the 394 reports before I take this to P&T: dates, seriousness, country, who reported?"** | **Partly.** Guide H5: case IDs only by SQL, "The screen does not link to case rows yet". Reporter type is 72% blank (DQ38). | Say it plainly in A3, not only in Q&A (see change 1). |

## 4. Trust rule: can she trace NAION and one recall live?

- **NAION, partly.** The labels-searched panel is the best thing in the demo. But the DailyMed click is marked **"Optional"** (guide A4), so as scripted the trace may never reach a source. The 394 reports cannot be opened from her screen. The 2×2 table appears only in Part H (Object Explorer, 10:45) as an engineer view. The method code also wrongly suggests the AI checked the labels.
- **Recall, no.** The panel copies openFDA fields and an "as of" date. It has no link to the FDA record, so she must trust our copy. That fails "show me where it says that".
- **Missing:** the FAERS case list. A one-click link to the recall record. Any line on *what* changed in a new label version.

## 5. Top 5 changes (no rebuild), ranked

1. **Finish the NAION trace on DailyMed itself (A4, make it mandatory).** Click the Ozempic v20 link. Cmd+F "optic". Rehearse first: the retinopathy warning must not give a false hit. Say: _"This is Ozempic's label, version 20, on DailyMed itself. I search for 'optic': no optic neuropathy. She can repeat this check in ten seconds. What she cannot do yet is open the 394 reports from this screen. We pull their case IDs by query today, and that is the first thing we would add before anyone takes this to P&T."_
2. **Frame NAION as a known positive (A3, after the PRR).** Say: _"NAION is not new. It has been published and discussed since 2024. We lead with it because a monitor that missed it would be broken. Ours ranks it first, and the three US labels she uses still do not mention it."_ (Verify the EMA fact before adding it.)
3. **Name the noise before she sees it (A2, before filtering).** Say: _"Look at morphine's rank 1: Ewing's sarcoma, a bone cancer. That is almost surely the patients, not the drug. This is why 1,073 is a review queue. She dismisses that in one click. Now one drug."_
4. **Fix the recall wording and trace it to the FDA (A6).** Before the demo, open a tab with `https://api.fda.gov/drug/enforcement.json?search=recall_number:"D-0040-2027"`: the same openFDA record the pipeline reads. Say: _"126 open FDA recalls name one of our 13 ingredients. Most are compounded products. This one matches none of the FDA-approved products we track. We have no purchasing data, so if you buy compounded GLP-1s, check your records. Here is the FDA's own record of it: same number, same lot."_ Then click **Classification → Class I** and say how many there are (count in rehearsal).
5. **Say only what was measured, and what Q3 cannot do (slide 2, A7, s05 close).** Slide 2 subtitle: _"designed to answer three questions in under two minutes (not yet timed with a person)"_. Then run one stopwatch walk-through in rehearsal and quote the number. In A7 add: _"A label row tells her a new version took effect, not what changed. On DailyMed she opens the label's 'Recent Major Changes' section. And new signals arrive only with a FAERS quarter, about 130 days behind."_ Replace "That is her morning" with _"That is her morning today: recalls and labels daily, signals quarterly."_

**What I'd check next:** a timed walk-through by a real pharmacist on all 12 drugs' rank-1 rows (how many survive?), and the active Class I count with each one's product match.
