# R3 — Prior art: has this been built already?

Stage: **Empathize / Define** (discovery). Researched 2026-10-19. Web sources only; every fact is cited `[n]`.
Confidence tags: **V** = verified on the source page · **I** = inferred / from a summary or secondary source.

---

## TL;DR

1. **The pieces exist; the whole does not.** Label-extracted side effects (OnSIDES, SIDER), "in FAERS but not on the label" signals (OFFSIDES), disproportionality tools (OpenVigil, Empirica) and hospital recall tools (Inmar OneRecall) are all built [1][5][21][25][33].
2. **We found no public tool that joins all three for a hospital pharmacist:** label vs FAERS gap + active recalls + "what changed since yesterday", with every flag traced to its source. We also found no public Palantir Foundry build for this (I — absence of evidence).
3. **Our edge is the user and the trust layer, not the algorithm.** Reuse OnSIDES and the TAC 2017 gold set as benchmarks. Do not try to beat them at extraction.

---

## Jargon used once

| Term | Plain meaning |
|---|---|
| FAERS | FDA Adverse Event Reporting System — public reports of suspected drug side effects |
| SPL | Structured Product Label — the drug label in XML, published on DailyMed |
| MedDRA / PT | Medical dictionary for side effects. PT = "Preferred Term", its standard level. Licensed, not free |
| PRR / ROR | Disproportionality ratios: is this side effect reported more often with this drug than with all others? |
| MGPS / EBGM | A Bayesian version of PRR that is steadier when counts are small (used by FDA, Oracle) |
| F1 | One accuracy score that balances precision (how many flags are right) and recall (how many true items we found). 1.0 = perfect |
| Gold set | Hand-checked answer key used to score the AI |

---

## 1. Comparison table

### 1a. Academic and open datasets / tools

| Name | Type | What it does | Overlap with us | Gap / our differentiator | Reusable? + license |
|---|---|---|---|---|---|
| **OnSIDES** (Tatonetti lab, Cedars-Sinai) [1][2][3][47] | Open dataset + model | Fine-tuned PubMedBERT extracts side effects from label sections (Adverse Reactions, Boxed Warning, Warnings & Precautions). US + EU + UK + Japan labels. ~51,460 labels, 4,097 ingredients, 7.1M drug–ADE pairs as of Apr 2026; quarterly updates planned [1] (V) | **High** — same task as our LLM label extraction | Not an LLM; no FAERS comparison; no recalls; no hospital workflow; no per-flag source sentence in UI | **Yes.** Code MIT, data CC BY 4.0 [1] (V). Best candidate for cross-check / second gold set |
| **OFFSIDES / TWOSIDES / nSIDES** (Tatonetti lab) [5][6] | Open dataset | OFFSIDES = side effects found in FAERS but **not on the label** (1,332 drugs, 10,097 events). TWOSIDES = drug-pair effects, uses PRR [5] (V) | **Very high** — this is our core "frequent but unlabeled" idea | Static snapshot (file named 2019-11-13 [6], I); research resource, not a daily monitor; no recalls; no "what changed" | Download yes [6]. **License not stated** on page [5][6] (V) — cite Tatonetti 2012; ask before redistribution |
| **SIDER 4.1** (EMBL) [7][8] | Open dataset | Side effects + frequencies text-mined from package inserts. 1,430 drugs, 140,064 drug–ADR pairs [7] (V) | Medium | Frozen since 21 Oct 2015 [7] (V); outdated vs current labels [18] | CC BY 4.0 on Zenodo [7] (V). Useful only as a legacy reference |
| **TAC 2017 ADR track** (NLM + FDA) [9][10][11] | Benchmark | 200 SPLs hand-annotated for adverse reactions + MedDRA PTs (101 train / 99 test; 26,488 reaction mentions) [9] (V) | **High** — ready-made gold set for our exact task | Labels are ~2017 versions; covers 3 label sections only | Downloadable [10] (V). No formal license stated; MedDRA was supplied separately to participants [10] (V) |
| **ADE Eval** (MITRE + FDA, 2021) [13] | Benchmark / shared task | 13 teams, 23 runs; best MedDRA coding F1 0.79, best mention F1 0.89 [13] (I — abstract via search) | Medium | Conclusion: NLP not good enough to run unattended; use with human review [13] | Paper only; supports our "human-in-the-loop" design |
| **AskFDALabel** (FDA NCTR, 2025) [14] | Research method (LLM + RAG) | Llama 3.1-70B + database lookup of the current FDA label; returns cited set-IDs [14] (V) | **High** — closest to our "LLM reads label, cites source" | FDA-internal research; no FAERS comparison; no recall view | Prompts/SQL in supplement; **no public code repo** [14] (V) |
| **Gisladottir et al. 2025** (Tatonetti lab, *Drug Safety*) [15][16][17] | Paper | GPT-4 vs Llama vs Mixtral vs BERT baselines for SPL adverse-reaction extraction; GPT-4 matches/beats prior state of the art with no fine-tuning [15][16] (V) | High — validates our LLM approach | Numbers not visible to us (paywall) | Method only |
| **PVLens** (Painter, Powell, Bate 2025) [18] | Research system | Extracts label safety info, maps to MedDRA, web review tool for experts [18] (V) | High — label extraction + human review | No code/data link found [18] (V) | Paper CC BY 4.0; system not reusable |
| **SIDEKICK** (2025/26 preprint) [19] | Knowledge graph | LLM extracts indications, contraindications, adverse reactions from 50,000+ SPLs; maps to HPO/MONDO/RxNorm [19] (V) | Medium | Repurposing focus; no accuracy numbers on abstract page [19] (V) | Dataset license / link not found [19] (V) |
| **FDA FAERS Public Dashboard** [20] | Free gov tool | Query FAERS by drug, age, event, date; charts [20] (V) | Medium — FAERS view | No label comparison, no PRR, no recalls (I) | Free to use; not reusable code |
| **OpenVigil 2.1** [21][22] | Free web tool | Cleans FAERS; computes PRR, ROR, RRR [21][22] (V) | High — our disproportionality step | No label gap view; one study shows data to Mar 2023 only [22] (I) | Free web tool; use as a **cross-check for our PRR numbers** |
| **AERSMine** (Cincinnati Children's, 2016) [23][24] | Free web tool | FAERS mining with MedDRA aggregation; WHO signal algorithms [23][24] (I) | Medium | No evidence of updates since 2016 (I) | Free access; not reusable code |

### 1b. Commercial products

| Name | Type | What it does | Overlap | Gap / differentiator | Reusable? |
|---|---|---|---|---|---|
| **Oracle Empirica Signal** [25][26] | Commercial PV software | MGPS/EBGM, PRR, ROR on FAERS, VAERS, VigiBase; stratified runs [25] (V) | High on stats | Built for pharma/regulator safety teams, not hospital pharmacy (I); no LLM label gap shown | No (licensed). Copy its idea: **use EBGM/EB05 alongside PRR** |
| **TriNetX EVIDEX** (ex-Advera Health, RxSignal) [27][28] | Commercial SaaS | FAERS + VigiBase + EVDAS + trial data + real-world data; background rates [27][28] (I — vendor/review) | High | Subscription, pharma-focused (I) | No |
| **UMC VigiLyze** (WHO) [29] | Signal tool on VigiBase | Signal detection for national PV centres [29] (V) | Medium | Only for WHO-programme national centres [29] (V) | No |
| **ArisGlobal LifeSphere Signal** [30][31] | Commercial PV suite | AI signal management; FAERS + private data in one workspace [30] (I) | Medium | Vendor-run study claims 42% fewer false positives (VigiBase, not peer-reviewed) [31] (I) | No |
| **IQVIA Vigilance Detect** [32] | Commercial | Automated signal detection, AI/ML, agentic AI roadmap [32] (I — vendor) | Medium | Pharma sponsor focus | No |
| **Inmar OneRecall** (formerly Noblis **RASMAS**) [33][34][35] | Hospital recall tool | Recall alert feed, filtering, routing, audit trail; used by VA [33][34][35] (V/I) | **High on recalls** | Recalls only — no FAERS signal, no label gap (I) | No. Learn: **inventory matching + documented response** is what hospitals pay for |
| **Epic (SlicerDicer, MyChart)** [36][37] | EHR features | Find affected patients after a recall; UCSF+FDA pilot of automated patient recall notices [36][37] (V/I) | Low–medium | Patient-level (PHI) — out of our scope | No. Note as a "scale" integration in roadmap |

### 1c. Palantir-specific

| Item | What it is | Relevance |
|---|---|---|
| FDA–Palantir contract, Dec 2020 [38] | $44.4M, 3-year, CDER + Oncology Center of Excellence, drug review and safety data platform [38] (I — news) | Shows Palantir is used inside FDA drug review. No public detail on FAERS signal work |
| FDA "21 Forward" (2022) [39] | Food supply-chain analytics, $22M [39] (I) | Not drug safety |
| Palantir blog demo, 2012 [40] | "Using Palantir to Explore Prescription Drug Safety" — simvastatin demo [40] (V) | Old canned demo. No data or code. Shows the idea has been pitched before |
| Cardinal Health + Palantir [41]; Tampa General [42] | Pharmacy purchasing tool on Foundry; hospital ops [41][42] (I) | Hospital pharmacy on Foundry exists, but for **supply/ops**, not safety signals |
| Merck KGaA Foundry DevTools [43] | Open-source Foundry dev library [43] (V) | Possibly useful tooling, not PV |
| **Public Foundry + FAERS/openFDA repos** | None found in GitHub search [44][45][46] | (I — absence of evidence) |

### 1d. GitHub / open-source

| Repo | What it does | Overlap | Notes |
|---|---|---|---|
| WangLabCSU/faers (R) [44] | FAERS ingest, dedup, MedDRA mapping, ROR/PRR/BCPNN/EBGM (I) | High (stats) | Most mature; 54 stars; use as **reference for dedup + stats** |
| yism/faerscope-opencore [44] | PRR, ROR, IC engine with MedDRA mapping | High (stats) | Very new, 1 star |
| drvvek/faers_mcp [44] | openFDA FAERS MCP server with ROR/PRR/EBGM | Medium | LLM-tool style |
| guptaprakhariitr/fda-approvals-mcp [44] | openFDA approvals + recalls + adverse events | Medium | Closest "events + recalls" combo found; no label gap |
| nglebm19/pharmviginet [44] | FAERS signal benchmark with SIDER labels, time-split | Medium | Good idea: **time-split evaluation** |
| Krishna200608/PharmaGuard [44] | FAERS disproportionality + ChEMBL + PubMed, Streamlit | Medium | No labels/recalls |
| cyanheads/openfda-mcp-server [46] | openFDA drug, recall data for LLMs | Low–medium | — |
| KarelDO/BioDEX [45] | Large ADE extraction dataset from literature | Low | Literature, not labels |

None of the repos we saw combine **FAERS + LLM label extraction + recalls + daily change** (V for the pages listed; only first 20 results per topic were visible).

---

## 2. Published accuracy numbers for label extraction (our benchmark)

| System | Method | Dataset | Metric | Score | Conf. |
|---|---|---|---|---|---|
| TAC 2017 best (UTH_CCB) [9][12] | Neural NER | TAC 99 test labels | Task 1 mention F1 (exact) | **82.48** | V |
| TAC 2017 best (UTH_CCB) [9] | Neural | TAC test | Task 3 doc-level reactions, macro F1 | **82.19** | V |
| TAC 2017 best (UTH_CCB) [9] | Neural | TAC test | Task 4 MedDRA PT, macro F1 | **85.33** (micro 86.91) | V |
| TAC 2017 Oracle Health Sciences [9] | — | TAC test | Task 3 macro F1 | 79.67 | V |
| ADE Eval best [13] | Various | FDA labels | MedDRA coding F1 / mention F1 | 0.79 / 0.89 | I |
| **OnSIDES** [1] | Fine-tuned PubMedBERT | Internal test split | Adverse Reactions F1 | 0.942 (P 0.962, R 0.922) | V |
| **OnSIDES** [1] | same | Independent 30-label hold-out | Adverse Reactions / Boxed Warning / W&P F1 | **0.847 / 0.736 / 0.756** | V |
| **OnSIDES v3.2.0** [1] | same | TAC benchmark | F1 (P / R) | **89.87** (85.52 / 94.68) | V |
| **AskFDALabel** [14] | Llama 3.1-70B + RAG | TAC 476 sections | Exact F1 / semantic F1 | 0.827 / **0.911** | V |
| AskFDALabel [14] | same | 188 whole labels | Semantic F1 / exact F1 | 0.870 / 0.753 | V |
| PVLens [18] | Automated + review | 97 labels | F1 (P / R) | 0.882 (0.799 / 0.983) | V |
| Gisladottir 2025 (GPT-4) [15] | Zero-shot LLM | ~1,000+ SPLs [17] | "Matches or exceeds" prior SOTA | numbers not accessible | I |

**Benchmark we propose (I — our recommendation):** on the TAC 2017 test set, target **MedDRA-PT macro F1 ≥ 0.85** (matches TAC best 85.33 and OnSIDES ~0.90). Report exact **and** semantic match separately — AskFDALabel shows a ~0.08–0.12 gap between them [14]. Report Boxed Warning and Warnings & Precautions separately; they are harder (OnSIDES hold-out 0.74–0.76) [1].

---

## 3. Known pitfalls others reported

| Pitfall | Evidence | What we do about it |
|---|---|---|
| **FAERS duplicates** inflate signals | 39% of 2,297 reviewed reports were duplicates; only 29% of duplicate sets agreed on PTs [48] (V). A PARP-inhibitor study with weak dedup produced an ROR of 471 that critics flagged [49] (I) | Dedup by FDA case ID + latest version; log counts before/after; flag tiny-count high-ROR signals |
| Reporting biases (notoriety, stimulated reporting) | Listed as known biases in FAERS mining [50] (I) | Show "newly in the news?" caveat; never call a flag a confirmed reaction |
| FAERS ≠ causation | FDA states reports do not prove the drug caused the event [20] (V) | Wording rule in UI: "signal to review", not "side effect" |
| **MedDRA is licensed** | Commercial subscription; free for non-commercial via BioPortal, no redistribution [52] (I) | Already a compliance item — store PT names from FAERS only; do not ship the dictionary |
| Label **section** matters | Boxed Warning / W&P extraction much weaker than Adverse Reactions [1] (V); section and context drive LLM accuracy [15] (V) | Score each section separately in the gold set |
| **Negation / hypothetical** text | TAC annotates negated, animal-only and drug-class mentions as *not* positive reactions [9] (V) | Prompt + gold set must include "not observed", "in animals", "class effect" cases |
| Label **versions** change | AskFDALabel "errors" were often correct against the newer label [14] (V) | Pin SPL set-ID + version on every extracted reaction |
| Wrong product picked by drug name | AskFDALabel picked topical clotrimazole instead of oral [14] (V) | Resolve drug via RxNorm + route/dosage form before label lookup |
| LLM output limits / irrelevant output | Long labels exceeded 1,024 output tokens [14] (V); models sometimes return irrelevant text [17] (I) | Chunk by section; validate every term against the source sentence (grounding check) |
| NLP not safe unattended | ADE Eval conclusion [13] (I); TAC asked "Will ~0.85 F1 be sufficient?" [9] (V) | Human review queue for new flags |
| Stale public tools | SIDER frozen 2015 [7]; OFFSIDES ~2019 [6]; OpenVigil data to 2023 in one study [22] | Our "daily refresh + what changed" is a real gap |

---

## 4. What we should reuse

| Reuse | How | Why |
|---|---|---|
| **TAC 2017 gold set** [10] | Primary gold set for the hallucination / accuracy check | Free, FDA-made, MedDRA-coded, directly comparable to published F1s |
| **OnSIDES** (CC BY 4.0) [1] | Second opinion: compare our LLM's extracted list per drug with OnSIDES; disagreements go to review | Current (2026), large, permissive license |
| **OFFSIDES** [5][6] | Sanity check: our "unlabeled but frequent" flags should overlap for older drugs | Same idea, peer-reviewed; check license first |
| **OpenVigil** / WangLabCSU **faers** [21][44] | Recompute PRR/ROR for 3–5 pilot drugs and compare to ours | "Measured, not asserted" — independent check of our math |
| **MGPS/EBGM** as second statistic [25][26] | Add EB05 next to PRR if time allows | Standard at FDA/Oracle; steadier on small counts |
| AskFDALabel pattern [14] | Fetch label by database query (not by LLM); LLM only reads; return set-ID + quote | Proven way to reduce hallucination and keep traceability |
| openFDA data (CC0) [51] | FAERS, labels, enforcement via openFDA | Public domain; attribution requested |

---

## 5. How we differentiate

1. **Built for one user: the hospital pharmacy safety officer.** Commercial PV tools target pharma and regulators [25][27][30][32]; recall tools target supply chain [33]. We answer her three morning questions on one screen.
2. **Signals + recalls + "what changed since yesterday" together.** We found no public tool that joins these (I). Inmar does recalls, OFFSIDES does label gaps — no one does both, daily.
3. **Every flag traces to its source.** Each flag links to: FAERS case counts and quarter, the SPL set-ID + version + section + sentence, and the recall number. AskFDALabel cites set-IDs [14]; OnSIDES does not show this in a workflow (I).
4. **Measured AI.** Public scorecard on the TAC gold set vs published numbers (Section 2), plus drift checks on new label versions. Most vendors publish only claims [31][32].
5. **Built on Foundry/AIP with an ontology** (Drug, Label, Reaction, Signal, Recall). No public Foundry PV build exists (I) — so the pilot doubles as a reusable pattern.

---

## Sources (accessed 2026-10-19)

1. tatonetti-lab/onsides — GitHub README. https://github.com/tatonetti-lab/onsides
2. Tanaka Y. et al. "OnSIDES Database: Extracting Adverse Drug Events from Drug Labels using NLP Models" — medRxiv. https://www.medrxiv.org/content/10.1101/2024.03.22.24304724v1.full
3. Cedars-Sinai Newsroom — "Artificial Intelligence Spotlights Medication Risks, Improves Drug Safety". https://www.cedars-sinai.org/newsroom/artificial-intelligence-spotlights-medication-risks-improves-drug-safety/
4. tatonettilab/onsides-bert — Hugging Face model card. https://huggingface.co/tatonettilab/onsides-bert
5. Tatonetti Lab — "Off-label and polypharmacy side effect databases". https://tatonettilab.org/resources/tatonetti-stm.html
6. Tatonetti Lab — "OffSIDES and TwoSIDES". https://tatonettilab.org/offsides/
7. SIDER 4.1 — Zenodo record. https://zenodo.org/records/7877720
8. Kuhn M. et al. "The SIDER database of drugs and side effects" — NAR/PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4702794/
9. Roberts K., Demner-Fushman D., Tonning J. "Overview of the TAC 2017 Adverse Reaction Extraction from Drug Labels Track" (slides). https://tac.nist.gov/publications/2017/presentations/TAC2017.ADR.overview.presentation.pdf
10. NLM BioNLP — TAC 2017 Adverse Drug Reaction Extraction from Drug Labels (data page). https://bionlp.nlm.nih.gov/tac2017adversereactions
11. Demner-Fushman D. et al. "A dataset of 200 structured product labels annotated for adverse drug reactions" — Sci Data/PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5789866/
12. UTH_CCB — TAC 2017 participant paper. https://tac.nist.gov/publications/2017/participant.papers/TAC2017.UTH_CCB.proceedings.pdf
13. Bayer S. et al. "ADE Eval: An Evaluation of Text Processing Systems for Adverse Event Extraction from Drug Labels for Pharmacovigilance" — Drug Safety 2021 (PubMed). https://pubmed.ncbi.nlm.nih.gov/33006728/
14. Wu L. et al. "Leveraging FDA Labeling Documents and Large Language Model to Enhance Annotation, Profiling, and Classification of Drug Adverse Events with AskFDALabel" — Drug Safety 2025/PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC12098182/
15. Gisladottir U. et al. "Leveraging Large Language Models in Extracting Drug Safety Information from Prescription Drug Labels" — Drug Safety 2025. https://link.springer.com/article/10.1007/s40264-025-01594-x
16. Broad Institute publication page for [15]. https://www.broadinstitute.org/publications/broad1365771
17. UBC CBR — "Facilitated Access to Drug Safety Information via the Use of Generative Artificial Intelligence". https://cbr.ubc.ca/?p=25960
18. Painter J.L., Powell G.E., Bate A. "PVLens: Enhancing Pharmacovigilance Through Automated Label Extraction" — arXiv 2503.20639. https://arxiv.org/abs/2503.20639
19. Ashhad M. et al. "SIDEKICK: A Semantically Integrated Resource for Drug Effects, Indications, and Contraindications" — arXiv 2602.19183. https://arxiv.org/abs/2602.19183
20. FDA — FAERS Public Dashboard FAQ. https://fis.fda.gov/extensions/FPD-FAQ/FPD-FAQ.html
21. OpenVigil — "What is OpenVigil?". https://openvigil.sourceforge.net/
22. "Drug-induced torsades de pointes: Disproportionality analysis of FAERS" — Front Cardiovasc Med/PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9639787/
23. Sarangdhar M. et al. AERSMine — Nature Biotechnology 2016. https://www.nature.com/articles/nbt.3623
24. Cincinnati Children's — AERSMine news release (2016). https://www.cincinnatichildrens.org/news/release/2016/drug-safety-07-08-2016
25. Oracle — "About the Oracle Empirica Signal application" (user guide 9.1). https://docs.oracle.com/en/industries/health-sciences/empirica-signal/9.1/userguide/empirica-signal-application.html
26. FDA — data mining / MGPS document. https://fda.gov/media/91848/download
27. TriNetX — Drug Safety / EVIDEX. https://trinetx.com/drug-safety
28. "Evidex" resource review — J Med Libr Assoc/PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6466506/
29. Uppsala Monitoring Centre — VigiLyze. https://who-umc.org/vigibase/vigilyze
30. ArisGlobal — LifeSphere Signal and Risk Management factsheet. https://arisglobal.com/factsheet-lifesphere-signal-and-risk-management
31. ArisGlobal — "New study confirms power of real world data in proactive signal detection". https://www.arisglobal.com/media/press-release/new-study-confirms-power-of-real-world-data-in-proactive-signal-detection-improving-patient-safety/
32. IQVIA — Vigilance Detect fact sheet. https://www.iqvia.com/library/fact-sheets/iqvia-vigilance-signal-detection
33. Inmar — "Inmar Intelligence rebrands RASMAS as OneRecall". https://inmar.com/blog/press/inmar-intelligence-rebrands-rasmas-onerecalltm-and-introduces-new-features-making-it
34. Inmar — OneRecall solution page. https://inmar.com/solutions/healthcare/supply-chain-solutions/onerecall
35. PSQH — "Noblis Awarded Department of Veterans Affairs Contract to Provide RASMAS". https://psqh.com/news/noblis-awarded-department-of-veterans-affairs-contract-to-provide-rasmas
36. Epic — "Rapid Response for Medication Recalls with Epic". https://epic.com/epic/post/rapid-response-medication-recalls-epic
37. JMIRx Med 2026 — automated patient-specific drug recall notification (UCSF/FDA). https://xmed.jmir.org/2026/1/e68345
38. BNN Bloomberg — "Palantir wins FDA contract to power drug review, inspections". https://www.bnnbloomberg.ca/palantir-wins-fda-contract-to-power-drug-review-inspections-1.1532930
39. Federal Times — "Palantir wins FDA contract to bolster US food supply chain resilience" (2022). https://www.federaltimes.com/govcon/2022/10/25/palantir-wins-fda-contract-to-bolster-us-food-supply-chain-resilience
40. Durusau P. — "Using Palantir to Explore Prescription Drug Safety" (2012). https://tm.durusau.net/?p=27505
41. IoT M2M Council — "Cardinal, Palantir to integrate clinical supply chain". https://iotm2mcouncil.org/iot-library/news/connected-health-news/cardinal-palantir-to-integrate-clinical-supply-chain/
42. HealthITAnalytics — "Tampa General Strikes Partnership to Build Data Analytics Platform". https://healthitanalytics.com/news/tampa-general-strikes-partnership-to-build-data-analytics-platform
43. Merck KGaA — open-source library for Palantir Foundry (2023). https://www.emdgroup.com/en/news/ace-palantir-07-03-2023.html
44. GitHub topic: faers. https://github.com/topics/faers
45. GitHub topic: pharmacovigilance. https://github.com/topics/pharmacovigilance
46. GitHub topic: openfda. https://github.com/topics/openfda
47. Becker's Hospital Review — "Cedars-Sinai unveils drug safety resource" (OnSIDES). https://www.beckershospitalreview.com/pharmacy/cedars-sinai-unveils-drug-safety-resource
48. Janiczak S. et al. "An Evaluation of Duplicate Adverse Event Reports Characteristics in FAERS" — Drug Safety 2025/PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC12423208/
49. "Commentary: Adverse event profiles of PARP inhibitors: analysis of spontaneous reports submitted to FAERS" — PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10468970/
50. ISPOR 2021 — "Overview of Biases Affecting the Interpretation of Signals Identified in Drug Safety Surveillance Systems". https://www.ispor.org/heor-resources/presentations-database/presentation/intl2021-3338/110773
51. openFDA — Terms of Service. https://open.fda.gov/terms/
52. BioPortal — MedDRA ontology page. https://bioportal.bioontology.org/ontologies/MEDDRA

**Limits of this review:** GitHub topic pages showed only the first 20 repos each. The Gisladottir 2025 F1 values sat behind a paywall. Vendor capabilities come from vendor pages, not tests. "Not found" means we did not find it, not that it does not exist.
