# R2 — Industry need: where is this use case real and required?

Stage: **Empathize / Define** (discovery). Researched 2026-10-19. Web sources only; every fact is cited `[n]`.
Confidence tags: **V** = verified on the source page (or its full text) · **I** = inferred, or taken from a summary / secondary source / vendor claim.

---

## TL;DR

1. **The recall half is required.** US hospital rules expect pharmacies to watch drug alerts and recalls and to pull recalled stock (CMS [14], Joint Commission [16][18]). Today this work is manual, done by 1–2 people, and slow [6][9].
2. **The "FAERS vs label" half is required for drug makers and the FDA, not for hospitals.** Drug makers must review all adverse event data by law [20][22]. The FDA's own reviewers check FAERS reports against the label by hand [31]. We found no rule or common practice that makes hospitals do this (I). That makes it our new idea, not a compliance box.
3. **The pitch:** one morning screen that turns slow, scattered FDA feeds into a short, sourced to-do list for the safety officer. We sell it on time-to-awareness and staff hours. It is not a regulatory signal-detection system.

---

## Jargon used once

| Term | Plain meaning |
|---|---|
| MSO | Medication Safety Officer: usually a pharmacist who leads medication-error prevention in a hospital |
| P&T committee | Pharmacy & Therapeutics committee: the doctors and pharmacists who decide which drugs are on the hospital's list (the **formulary**) |
| CMS CoP | Centers for Medicare & Medicaid Services *Conditions of Participation*: rules a hospital must meet to be paid by Medicare |
| SOM Appendix A | CMS's guidance that tells inspectors how to check those hospital rules |
| Joint Commission (TJC) | The main US hospital accreditor. Its *Medication Management (MM)* chapter covers drugs |
| FAERS / AEMS | The FDA's database of reported side effects. In March 2026 the FDA folded it into a new system called **AEMS** (Adverse Event Monitoring System) [24][26] |
| Pharmacovigilance (PV) | Watching medicines for safety problems after they are on the market |
| Signal | Information suggesting a new, possibly causal, link between a drug and a side effect, strong enough to check further [23] |
| GVP Module IX | The EU's rulebook for how drug makers and regulators manage signals [21][22] |
| Sentinel | The FDA's system that studies insurance and health-record data to check safety questions [25] |
| Class I recall | The most serious FDA recall level: a real chance of serious harm or death |
| MedWatch | The FDA's safety alert and reporting program. Its e-mail list sends recalls and safety notices [5] |

---

## Who needs this and why

| Who | What they must do | Is it required? | How it is done today | Our fit | Conf. |
|---|---|---|---|---|---|
| **Hospital MSO / pharmacy safety team** | Know about new safety alerts and recalls for drugs the hospital uses. Act on them. | **Yes for recalls and alerts.** CMS expects a way to monitor drug alerts and recalls [14]. ASHP says every hospital should have an ongoing way to react to safety updates [2]. | MedWatch e-mails, ISMP newsletters, wholesaler notices, state board listservs, vendor recall tools [2][5][6][11] | **Strong.** Recall list + "what changed" | V |
| **Pharmacy buyer / inventory staff** | Find and pull recalled lots from every shelf, cabinet, kit and tray | Yes. Recalled drugs count as "unusable" and must not be available for patients [14][16] | Manual searches. Vendor tools match recalls to inventory [9][10][11] | **Partial.** We flag the recall; we do not track lots on shelves | V |
| **P&T committee** | Keep the formulary safe. Review drugs and their safety | The formulary is required [15][16]. Safety review uses FDA/ISMP info [2][19] | Drug monographs and yearly reviews, built by hand [2][19] | **Medium.** "Not-on-label" flags feed the safety section of a review | V / I |
| **Drug makers (label holders)** | Review all adverse event information promptly. Detect and report signals | **Yes, by law.** US 21 CFR 314.80 [20]; EU GVP Module IX [22] | Large PV databases and signal tools (Oracle Argus, ArisGlobal LifeSphere, Veeva) [42] | **Same method, different buyer.** Not our pilot user | V |
| **FDA** | Screen the adverse event database regularly. Post potential signals every quarter | **Yes, by law** (FDAAA §921, FD&C Act 505(k)(5)) [24]. Sentinel built under FDAAA §905 [25] | Reviewers read label text by hand to see if a reported reaction is already listed [31]. Now testing LLM tools [32][33][35] | Shows the "is it on the label?" check is a real, hard task | V |

**Key insight (I):** the hospital need is real, but it is split. Recalls and alerts are a compliance duty. The FAERS-vs-label gap is a *drug-maker and FDA* duty that hospitals do not have to do. For a hospital it is a "nice early warning", not a rule. Say this plainly in the demo.

---

## 1. The hospital side: who the MSO is and how news reaches her

### 1a. The role

| Finding | Source | Conf. |
|---|---|---|
| ASHP (American Society of Health-System Pharmacists) published a formal statement on the medication safety leader in 2020. It covers leadership, safety expertise, change management, research and education. | [1] | V |
| ASHP's 2018 error-prevention guideline says a safety program needs a medication safety leader, preferably a pharmacist. | [2] | V |
| ASHP says each hospital should have an ongoing way to react to medication safety updates. It names the ISMP newsletters, MedWatch e-mails and the National Alert Network as the feeds to watch. | [2] | V |
| ASHP says safety alerts should be handled by the medication safety committee or the P&T committee. | [2] | V |
| ISMP (Institute for Safe Medication Practices) has repeated its call for an MSO in every organization (2021). | [3] | V (summary only) |
| MSO duties vary a lot between hospitals. | [4] | I (trade press) |

### 1b. How hospitals learn about recalls and safety news today

| Channel | What it gives | Weakness | Source | Conf. |
|---|---|---|---|---|
| FDA MedWatch e-mail list / RSS | Recalls and FDA safety notices as they are posted | Covers all products. Pushes everything; no link to *our* formulary | [5] | V |
| FDA Recall Alert System / Enforcement Report | All recalls FDA monitors, once classified. Weekly | Listed only after FDA classifies the recall [29] | [29] | V |
| ISMP newsletters, National Alert Network | Error stories and urgent alerts | Narrative. Must be read and judged by hand | [2] | V |
| Wholesaler / distributor notices | Recall notices passed on from manufacturers | Go to the buyer. Can sit unread during leave or busy weeks | [6] | V |
| State board of pharmacy listservs | Local alerts | Another inbox | [6] | V |
| Vendor recall services (Inmar OneRecall, Staritas/ECRI Alerts, Bluesight) | Early alerts, matching to inventory, workflow | Paid. Focus on recalls, not label gaps | [9][10][11] | V / I |

### 1c. Pain points (with numbers)

| Pain point | Evidence | Source | Conf. |
|---|---|---|---|
| **FDA alerts miss some serious recalls.** | Of 91 Class I drug recalls (2004–2011), FDA's Recall Alert System sent no notice for 36 (about 40%). About 1 in 5 Class I recalls (18) went out through neither the Recall Alert System nor MedWatch. | [7][8] | V (abstract + press summary) |
| **Serious recalls are lost in noise.** | The same alert channel mixes in minor items such as veterinary recalls. | [8] | V |
| **Few people, many recalls.** | A hospital pharmacy usually has 1–2 people watching recall notices. Finding all affected stock can take weeks. | [6] | V (industry interview, Cencora) |
| **High volume.** | At least 267 different drug NDCs (product codes) were recalled in 2023 across Bluesight's ~300 hospital pharmacies: more than one per weekday. | [9] | I (vendor data) |
| **Manual searching is wasteful.** | In one recall, 97% of checked kits did not contain the recalled drug. | [9] | I (vendor data) |
| **Matching saves time.** | One hospital's recall review fell from about 2–2.5 hours to about 10 minutes once alerts were matched to inventory. In one month only 6 of 117 alerts matched one facility's stock. | [10] | V (2013 news; vendor-reported) |
| **Recalled drugs stay on shelves.** | ISMP (2008) reported recalled drugs still found in hospital pharmacies. | [12] | V (summary only) |
| **Harm is real but hard to prove from reports.** | In the 2008 heparin contamination crisis, FDA reviewed 94 death reports but could not link any adverse event to the contaminated heparin. Only 13 reports listed lot numbers. | [13] | V |
| **Recalls rank as a top worry.** | 42% of Bluesight survey respondents rated recall problems important or very important (2024). Patient safety (86%) and compliance (82%) drive tech budgets. | [9] | I (vendor survey) |

**Not found:** a peer-reviewed study of how many hours a hospital spends per recall. An often-repeated figure (about 5 hours per recall) comes from one vendor and we could not open it. Do not quote it.

---

## 2. Rules and accreditation that drive the need

| Driver | What it says (paraphrased) | What it means for us | Source | Conf. |
|---|---|---|---|---|
| **CMS CoP 42 CFR 482.25** | The medical staff must set up a formulary. Drug errors and adverse drug reactions must be reported at once. Drug information must be available to staff. Outdated, mislabeled or unusable drugs must not be available for patients. | Formulary + reporting + drug info are federal rules for Medicare hospitals | [15] | V |
| **CMS SOM Appendix A, tag A-0491** | A pharmacy's error-prevention policies should cover **monitoring drug alerts and/or recalls**. The hospital should have a way to bring in alerts from ISMP, the FDA and MedWatch for review. | **The strongest "required" hook for our recall feature.** | [14] | V (2015 version; not re-checked for later edits) |
| **CMS SOM Appendix A, tags A-0500 / A-0505** | Drugs are retrieved when recalled for safety reasons. Recalled drugs count as "unusable". Surveyors ask: does the hospital pull recalled drugs once told? | Recall response is inspected | [14] | V |
| **Joint Commission MM chapter (until end of 2025)** | MM.05.01.17: written policy to retrieve recalled drugs, carry it out, tell prescribers and dispensers, tell patients when required. MM.02.01.01: drugs selected using criteria incl. adverse drug events; formulary reviewed at least yearly. | Shows long-standing recall and formulary-safety duties | [18] | V (secondary training text) |
| **Joint Commission "Accreditation 360" (from 1 Jan 2026)** | All MM standards renumbered into 9 standards. MM.12.01.01 = maintain a formulary. MM.13.01.01 EP 4 = remove expired, mislabeled, contaminated or unusable drugs. MM.17.01.01 = report adverse drug events and errors. | **We did not find the old recall-retrieval wording in the 2026 hospital list.** The duty still applies through the CMS rules TJC maps to (§482.25(b)(3)). | [16][17] | V (text checked) / I (that recall now sits under EP 4) |
| **ASHP P&T / formulary guideline (2021)** | Formularies are a system of policies for safe, cost-effective drug use. | P&T is a natural second user | [19] | I (summary) |
| **ASHP error-prevention guideline (2018)** | Formulary reviews should include a safety section using ISMP and FDA MedWatch reports. | "Not-on-label" flags can feed this section | [2] | V |

**Bottom line (I):** no US rule tells a hospital to mine FAERS. The rules do tell it to (a) watch alerts and recalls, (b) pull recalled drugs, and (c) think about safety when choosing formulary drugs.

---

## 3. The drug-maker and regulator side

| Actor | Legal duty | Method | Source | Conf. |
|---|---|---|---|---|
| US drug makers | Must promptly review all adverse drug experience information from any source and keep written procedures for it (21 CFR 314.80) | Case processing + signal detection in PV databases | [20] | V |
| EU drug makers | GVP Module IX Rev 1 (in force 22 Nov 2017): monitor EudraVigilance data and report validated signals | Signal detection, validation, assessment | [21][22] | V |
| FDA | Regularly screen the adverse event database and post a quarterly list of potential serious-risk signals (FDAAA §921). A listing does not mean FDA has found the drug causes the risk. | Disproportionality screening + reviewer judgement | [24] | V |
| FDA reviewers | Read the label by hand to see if a reported reaction is already listed | Manual; this drove the TAC 2017 label-extraction challenge | [31] | V |
| FDA Sentinel | Active surveillance using health data, required by FDAAA §905 | Distributed database queries | [25] | V |

### Same or different from our hospital use case?

| Aspect | Drug maker / FDA | Hospital MSO (us) |
|---|---|---|
| Required by law? | Yes [20][22][24] | Recalls: yes [14]. FAERS gap: no (I) |
| Scope | All their products, worldwide | Only drugs on *this* formulary |
| Output | Validated signal → label change, regulator report | Awareness → local action (alert staff, P&T review, pull stock) |
| Data | Full private case data + public data | Public data only (FAERS/AEMS, DailyMed, recalls) |
| Validation bar | Formal, audited, regulated | Decision support. A human judges every flag |
| Shared core | "Is this reported reaction already on the label?" | Same question [31] |

**Timing context (I):** in a 10-year study of 22 new drugs approved in 2008, FAERS reports were the main trigger for new safety issues in the first year after approval (69%) [43]. FDA posts label safety changes in its SrLC database [44]. So a hospital that watches FAERS against the label may see a possible issue months before a label update. This is a hypothesis, not a measured lead time.

---

## 4. Market

| Market | Size (as published) | Growth | Buyers | Source | Conf. |
|---|---|---|---|---|---|
| PV / drug safety software (low estimate) | ~US$229 M (2025) | 7.2% a year to 2034 | Pharma, CROs (contract research firms) | [39] | I (paid report summary) |
| PV / drug safety software (high estimate) | ~US$1.62 B (2025) | 10.4% a year to 2034 | Same | [40] | I |
| Medical device recall management services | ~US$1.68 B (2025) | 7.8% a year to 2034 | Device makers; hospitals are one segment | [41] | I |
| Hospital drug recall software | **No clean public figure found** | — | Hospital pharmacy, supply chain | — | — |

Estimates differ about 7x because firms define "PV software" differently. Use them only as "a real, growing market".

**Named players:**

| Segment | Vendors | Source | Conf. |
|---|---|---|---|
| Pharma PV databases | Oracle Argus, ArisGlobal LifeSphere, Veeva Vault Safety | [42] | I |
| Hospital recall tools | Inmar OneRecall (vendor claims ~60% of US hospitals), Staritas / ECRI Alerts (early alerts, inventory matching), Bluesight (RFID kit tracking), older: RASMAS, National Recall Alert Center. Kit Check (now Bluesight) surveys list recalls among top pharmacy priorities | [9][11][45][46][48] | I (vendor claims) |

**Budgets:** we found no public hospital budget line for recall or safety-signal software. Bluesight's survey says patient safety and compliance are the top reasons hospitals buy pharmacy tech [9] (I).

---

## 5. Who would pay in a hospital, and what they would measure

All rows are **inferred (I)** from the roles and rules above, unless a source is shown.

| Role | Why they care | Budget power |
|---|---|---|
| Director of Pharmacy | Owns recall compliance and pharmacy tech spend [6][14] | **Main buyer** |
| Medication Safety Officer | Daily user. Owns alert review [1][2] | Champion, not budget holder |
| Chief Quality / Patient Safety Officer | Accreditation and survey results | Co-sponsor |
| P&T committee chair | Formulary safety reviews [2][19] | Influencer |
| Health-system / GPO level (group purchasing) | One tool across many hospitals | Scale buyer |

### Value metrics they would track

| Metric | How to measure in the pilot | Baseline we have |
|---|---|---|
| **Time-to-awareness** (FDA posts → MSO sees it) | Timestamp of source record vs. time it shows on the morning screen | None public. Measure it ourselves |
| **Recall response time** | Flag shown → "reviewed / actioned" | None public |
| **Missed-recall rate** | Class I recalls for formulary drugs vs. recalls our feed caught | Historic gap: about 1 in 5 Class I recalls had no FDA alert [7] |
| **Staff minutes per morning** | Time to review today's list vs. reading e-mails | 2–2.5 h → ~10 min per recall review with matching (vendor case) [10] |
| **Noise cut** | Alerts received vs. alerts relevant to the formulary | 6 of 117 alerts relevant in one vendor case [10] |
| **Traceability** | % of flags with a working link to the FDA / DailyMed source | Target 100% |
| **Harm avoided** | Hard to prove; report as "near-misses caught" only | Heparin shows how hard causal proof is [13] |

---

## 6. AI / LLM trends in pharmacovigilance (2023–2026)

| Trend | Detail | Source | Conf. |
|---|---|---|---|
| **FDA uses LLMs internally** | Elsa launched June 2025, runs in a secure cloud, not trained on industry submissions [34]. By Dec 2025 >70% of staff used it; agentic AI added for tasks incl. post-market surveillance, "with human oversight" [35]. | [34][35] | V |
| **FDA research on label extraction** | AskFDALabel (FDA/NCTR, 2025): Llama 3.1-70B + retrieval over FDA labels. F1 0.911 for adverse event annotation. Says manual extraction is slow and hard to keep current. | [32] | V |
| **FDA label-change detection** | LabelComp (2024): finds changed adverse event terms between label versions. Recall 0.997, precision 0.66–0.88. Authors keep a human in the loop. | [33] | V |
| **Benchmark exists** | TAC 2017: FDA/NLM gold set of labels with annotated adverse reactions, mapped to MedDRA. | [31] | V |
| **Faster, noisier data** | FDA began daily FAERS publishing (Aug 2025) [27]. AEMS replaced FAERS on 11 Mar 2026 [24][26]. openFDA's FAERS API still says quarterly updates, lag of 3+ months [28]. | [24][26][27][28] | V |
| **Literature screening with LLMs** | One 2024 study: GPT-4-class models had 97% sensitivity but 67% specificity. | [47] | I (snippet) |

### Regulatory cautions

| Caution | Source | Conf. |
|---|---|---|
| FDA draft guidance (Jan 2025): judge AI by a risk-based "credibility" plan for its *context of use*. Applies to AI used for regulatory decisions, not hospital tools, but is a good design model. | [36] | V |
| EMA reflection paper on AI (Sept 2024): risk-based approach, human-centred, active steps against bias. | [37] | I (law-firm summary) |
| CIOMS Working Group XIV report on AI in PV (final Dec 2025): principles incl. human oversight, validity, transparency. | [38] | I (secondary on principles) |
| FAERS reports do not prove a drug caused the event. Report counts cannot give rates. | [30] | V |
| openFDA recall data should not be used to issue public alerts or track a recall's lifecycle. Status is frozen at publication. | [29] | V |

**Design meaning (I):** keep the LLM to one narrow job (label extraction), score it on a gold set (TAC 2017), keep a human in the loop, link every flag to its source, and label FAERS flags as "reported, not proven".

---

## Value story for the demo

- **"Rules already ask us to do this."** CMS tells hospital pharmacies to monitor drug alerts and recalls and to pull recalled drugs [14]. Today one or two people do it by hand from many inboxes [6].
- **"FDA alerts are not enough on their own."** A Harvard study found about 1 in 5 of the most serious drug recalls went out with no FDA alert at all [7]. A formulary-filtered daily feed closes that gap.
- **"Less noise, faster action."** Matching alerts to what we actually stock cut one hospital's recall review from about 2 hours to about 10 minutes [10]. We do the same for recalls *and* safety reports, and show only what changed since yesterday.
- **"An early look the FDA itself does by hand."** FDA reviewers check by hand whether a reported reaction is on the label [31]. We automate that check for our formulary, with a link to the source on every flag. It is a prompt to look, not proof of harm [30].
- **"Built the way regulators want AI built."** Narrow LLM task, measured on an FDA/NLM answer key, human sign-off, full audit trail [31][36][38].

---

## Open questions / gaps

| Gap | Why it matters | Next step |
|---|---|---|
| Where exactly the recall-retrieval duty sits in TJC's 2026 manual | Accuracy of the compliance claim | Ask a TJC-accredited pharmacist or read the full 2026 MM chapter |
| No public hours-per-recall study | Weakens the ROI number | Measure our own baseline in the pilot |
| AEMS public data feed vs. openFDA | Pipeline may need a new source | Data Engineer to check AEMS download/API (see `docs/07-data-quality/`) |
| No evidence hospitals mine FAERS today | This is our novelty *and* our adoption risk | Test with the safety officer persona |

---

## Sources

All accessed 2026-10-19.

1. AHRQ PSNet — "ASHP Statement on the Role of the Medication Safety Leader" (AJHP 2020;77(4):308-312). https://psnet.ahrq.gov/issue/ashp-statement-role-medication-safety-leader
2. ASHP — "ASHP Guidelines on Preventing Medication Errors in Hospitals" (2018, PDF copy). https://wwwtest.sop.pharmacy.wisc.edu/wp-content/uploads/sites/3/728-742-ASHPguidlinesPreventMedErrors.pdf
3. AHRQ PSNet — "A recurring call to action: every healthcare organization needs a medication safety officer!" (ISMP, 2021). https://psnet.ahrq.gov/issue/recurring-call-action-every-healthcare-organization-needs-medication-safety-officer
4. Drug Topics — "ASHP pushes for a medication safety officer in every hospital". https://drugtopics.com/view/medication-safety-officer-new-breed-pharmacist
5. FDA — "Stay Informed: Subscribe to MedWatch Safety Alerts". https://www.fda.gov/safety/medwatch-fda-safety-information-and-adverse-event-reporting-program/subscribe-medwatch-safety-alerts
6. Pharmaceutical Executive — "Drug Recalls: Q&A with Beth Riggio" (2024). https://www.pharmexec.com/view/drug-recalls-beth-riggio
7. PubMed — Wang B, Gagne JJ, Choudhry NK. "The epidemiology of drug recalls in the United States", Arch Intern Med 2012. https://pubmed.ncbi.nlm.nih.gov/22664942/
8. Pharmacy Times — "FDA Falls Short in Communicating Drug Recalls" (2012). https://www.pharmacytimes.com/view/fda-falls-short-in-communicating-drug-recalls
9. Bluesight — "Does Your Medication Recall Process Need to Be Recalled?". https://bluesight.com/news/does-your-medication-recall-process-need-to-be-recalled/
10. Infection Control Today — "ECRI Institute System Automatically Finds Recalled Products in Hospital's Inventory" (2013). https://www.infectioncontroltoday.com/view/ecri-institute-system-automatically-finds-recalled-products-hospitals-inventory
11. Staritas — "Recall Management". https://staritas.com/recall-management/
12. AHRQ PSNet — "Collaboration focused on priority issues promotes safety" (ISMP, 2008). https://psnet.ahrq.gov/issue/collaboration-focused-priority-issues-promotes-safety
13. GAO — GAO-11-95, "FDA: Response to Heparin Contamination Helped Protect Public Health…" (2010). https://www.gao.gov/assets/a311883.html
14. CMS — State Operations Manual Appendix A, Transmittal 151 (Pharmaceutical Services, 2015). https://www.cms.gov/regulations-and-guidance/guidance/transmittals/downloads/r151soma.pdf
15. Cornell LII — 42 CFR 482.25, Condition of participation: Pharmaceutical services. https://www.law.cornell.edu/cfr/text/42/482.25
16. The Joint Commission — "Joint Commission Requirements for Hospital Programs" (report generated 30 Sept 2025). https://digitalassets.jointcommission.org/api/public/content/6af7e77646254ef89894bdb37ad730c7?v=e89f4141
17. The Joint Commission — "Accreditation 360 – Updated Accreditation Manual: Medication Management and Information Management Chapters" (webinar transcript, Oct 2025). https://digitalassets.jointcommission.org/api/public/content/03b59f35a60f4558a4948e48ccb2d415
18. Creative Training Solutions / Guerbet — "Joint Commission Medication Management Standards in Radiology, 4th ed." (2022). https://www.guerbet-us-ce.com/courses/4618/PDF/JCMM_4th_Ed_010423.pdf
19. ASPR TRACIE — "ASHP Guidelines on the Pharmacy and Therapeutics Committee and the Formulary System". https://asprtracie.hhs.gov/technical-resources/resource/13370/ashp-guidelines-on-the-pharmacy-and-therapeutics-committee-and-the-formulary-system
20. Cornell LII — 21 CFR 314.80, Postmarketing reporting of adverse drug experiences. https://www.law.cornell.edu/cfr/text/21/314.80
21. EMA — "Good pharmacovigilance practices (GVP)". https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/good-pharmacovigilance-practices-gvp
22. EMA — "Guideline on GVP Module IX – Signal management (Rev 1)". https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf
23. EMA — Presentation: "Good pharmacovigilance practice Module IX: signal management". https://www.ema.europa.eu/en/documents/presentation/presentation-good-pharmacovigilance-practice-module-ix-signal-management_en.pdf
24. FDA — "New Safety Information or Potential Signals of Serious Risks Identified from the FDA Adverse Event Monitoring System (AEMS)". https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/new-safety-information-or-potential-signals-serious-risks-identified-fda-adverse-event-monitoring
25. FDA — "FDA's Sentinel Initiative – Background". https://www.fda.gov/safety/fdas-sentinel-initiative/fdas-sentinel-initiative-background
26. RAPS — "FDA consolidates adverse events reporting systems" (Mar 2026). https://www.raps.org/news-and-articles/news-articles/2026/3/fda-consolidates-adverse-events-reporting-systems
27. European Pharmaceutical Review — "FDA starts publishing daily adverse event data" (Aug 2025). https://www.europeanpharmaceuticalreview.com/news/fda-starts-publishing-daily-adverse-event-data/264977.article
28. openFDA — "Drug Adverse Event Overview". https://open.fda.gov/apis/drug/event/
29. openFDA — "Drug Recall Enforcement Reports Overview". https://open.fda.gov/apis/drug/enforcement/
30. FDA — "FDA Adverse Event Reporting System (FAERS) Public Dashboard" (PDF). https://www.fda.gov/files/about%20fda/published/FDA-Adverse-Events-Reporting-System-(FAERS)-Public-Dashboard-(PDF---4.13MB).pdf
31. NLM — "TAC 2017: Adverse Drug Reaction Extraction from Drug Labels". https://bionlp.nlm.nih.gov/tac2017adversereactions
32. PMC — Wu L et al. "Leveraging FDA Labeling Documents and Large Language Model … AskFDALabel", Drug Safety 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12098182/
33. PMC — Neyarapally GA et al. "Description and Validation of a Novel AI Tool, LabelComp …", Drug Safety 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11554693/
34. FDA — "FDA Launches Agency-Wide AI Tool to Optimize Performance for the American People" (June 2025). https://www.fda.gov/news-events/press-announcements/fda-launches-agency-wide-ai-tool-optimize-performance-american-people
35. FDA — "FDA Expands Artificial Intelligence Capabilities with Agentic AI Deployment" (Dec 2025). https://www.fda.gov/news-events/press-announcements/fda-expands-artificial-intelligence-capabilities-agentic-ai-deployment
36. FDA — "Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products" (draft guidance, Jan 2025). https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological
37. LexBlog (Arnold & Porter) — "EMA adopts reflection paper on the use of artificial intelligence (AI)" (Oct 2024). https://www.lexblog.com/2024/10/03/ema-adopts-reflection-paper-on-the-use-of-artificial-intelligence-ai/
38. CIOMS — "Working Group XIV: Artificial Intelligence in Pharmacovigilance". https://cioms.ch/working_groups/working-group-xiv-artificial-intelligence-in-pharmacovigilance/
39. Fortune Business Insights — "Pharmacovigilance Software Market". https://www.fortunebusinessinsights.com/pharmacovigilance-software-market-117584
40. DelveInsight — "Pharmacovigilance and Drug Safety Software Market Forecast 2034". https://www.delveinsight.com/report-store/Pharmacovigilance-and-Drug-Safety-Software-Market
41. Fortune Business Insights — "Medical Device Recall Management Services Market". https://www.fortunebusinessinsights.com/medical-device-recall-management-services-market-119299
42. IntuitionLabs — "Pharmacovigilance Databases: Argus vs. LifeSphere vs. Veeva". https://intuitionlabs.ai/articles/argus-vs-lifesphere-vs-veeva-safety-database
43. Springer / Drug Safety — Croteau et al. (2022), new safety issues for NMEs approved in 2008. https://link.springer.com/article/10.1007/s40264-021-01142-3
44. FDA — "Drug Safety-related Labeling Changes (SrLC) Database". https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-labeling-changes-slc-database
45. Business Wire — "Kit Check Hospital Pharmacy Operations Report Reveals…" (2020). https://www.businesswire.com/news/home/20200421005021/en/Kit-Check-Hospital-Pharmacy-Operations-Report-Reveals
46. MedCity News — "ECRI automates system to help hospitals respond to medical product recalls faster" (2013). https://medcitynews.com/2013/08/ecri-automates-system-to-help-hospitals-respond-to-medical-product-recalls-faster/
47. PMC — "Assessing the performance of large language models in literature screening for pharmacovigilance: a comparative study". https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12443093/
48. Inmar — "OneRecall overview" (page blocked to fetch; claim from search snippet). https://inmar.com/solutions/healthcare/onerecall-recall-management/onerecall-overview
