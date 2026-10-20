# R1 — Which therapeutic class should the pilot use?

_Stage: Define · Lens: PV SME (pharmacovigilance subject-matter expert) · Researched 2026-10-19 · Status: Draft for decision (feeds A001 / D007)_

**Confidence tags used on every claim**
- **[V-API]** verified: we ran the query ourselves against a live FDA/NLM API on 2026-10-19. Exact query logic is in the Method section.
- **[V-src]** verified: read in an official source (FDA, MHRA, HHS, Joint Commission).
- **[2nd]** secondary source only (trade press, law firm, tracker). Probably right, but not checked against the primary source.
- **[Inf]** inferred: our judgement or reasoning, not a sourced fact.

---

## TL;DR

1. **Opioids are a defensible choice but not the best one on their own.** Hospitals care most about them, and there is lots of change. But opioid FAERS data is dominated by abuse, overdose and lawsuit reports, and there are 1,274 opioid labels to keep track of.
2. **GLP-1 receptor agonists change fastest and make the best demo.** They give a ready-made "label missed it" story: NAION (sudden vision loss) is on UK/EU labels but not on the current US labels [V-API].
3. **Recommendation: opioid-led hybrid.** Use about 8 core hospital opioids plus the 5 GLP-1 RAs (13 ingredients, inside the brief's 50–200-drug limit once counted as products). Opioids give hospital credibility and recall alerts. GLP-1s give fast label change and a clean backtest.

## Scoring table (1 = poor, 5 = best for this pilot)

"Data mess risk" is scored so that **5 = clean / low risk** and 1 = very messy.

| Class | Change frequency (labels + recalls) | FAERS volume | Hospital relevance | Backtest material | Data mess risk (5 = clean) | Demo story | **Total /30** |
|---|---|---|---|---|---|---|---|
| **GLP-1 RAs** (semaglutide, tirzepatide, liraglutide, dulaglutide, exenatide) | 5 | 5 | 3 | 5 | 2 | 5 | **25** |
| **Opioids** (fentanyl, morphine, hydromorphone, oxycodone, hydrocodone, methadone, buprenorphine, tramadol) | 4 | 5 | 5 | 3 | 1 | 4 | **22** |
| **Opioids + GLP-1 hybrid** (recommended) | 5 | 5 | 5 | 5 | 2 | 5 | **27** (both classes together cover each other's gaps) |
| Anticoagulants (DOACs, warfarin, heparin, enoxaparin) | 3 | 4 | 5 | 2 | 3 | 3 | 20 |
| Immune checkpoint inhibitors | 3 | 4 | 3 | 3 | 1 | 2 | 16 |
| JAK inhibitors | 3 | 3 | 2 | 4 | 3 | 2 | 17 |
| Fluoroquinolones | 1 | 3 | 4 | 4 | 3 | 2 | 17 |
| Gabapentinoids | 2 | 5 | 3 | 3 | 2 | 2 | 17 |

Scores are **[Inf]**: our judgement, based on the evidence tables below. The hybrid row is not a simple sum. It scores each column by the stronger of the two classes, and its messiness score stays at the weaker level.

---

## 1. Label change frequency

### 1a. FDA Safety-related Labeling Changes (SrLC) database, by class [V-API]

SrLC is FDA's list of approved safety label changes from Jan 2016 onward. It covers only NDAs/BLAs (brand and 505(b)(2) products). **It leaves out ANDAs (generics)** [1]. We searched it by ingredient and counted the dated supplement entries. We also tagged which label section each entry touched (BW = Boxed Warning, WP = Warnings and Precautions).

| Class | Applications found | Entries since 2016 | Entries since Jan 2023 | of which BW / WP | Entries since Oct 2025 | Entries in 2026 |
|---|---|---|---|---|---|---|
| Opioids | 98 | 456 | 121 | 39 / 101 | 49 | **0** |
| GLP-1 RAs | 13 | 124 | 65 | 0 / 46 | 23 | 13 |
| Anticoagulants | 36 | 141 | 59 | 0 / 50 | 12 | 2 |
| ICIs | 10 | 224 | 88 | 1 / 27 | 33 | 20 |
| JAK inhibitors | 10 | 84 | 41 | 2 / 24 | 21 | 17 |
| Fluoroquinolones | 17 | 63 | 5 | 0 / 4 | 0 | 0 |
| Gabapentinoids | 8 | 38 | 14 | 0 / 8 | 0 | 0 |

How to read this:
- Opioid changes come in **class-wide waves**: 2016, 2018–19, 2021, 2023, and late 2025. Between waves it is quiet. There were no SrLC opioid entries in 2026 to date [V-API].
- GLP-1 and JAK changes are **steady**: 13 and 17 entries so far in 2026 [V-API].
- Many ICI entries come with new cancer indications. They are not all new safety signals [Inf].
- Caveat: the opioid ingredient search also returns buprenorphine for opioid use disorder (OUD) and combination products [Inf].

### 1b. DailyMed label versions: what actually moves day to day [V-API]

DailyMed holds every SPL (Structured Product Labeling, the label file). Generics and repackagers each have their own SPL. We counted SPLs and how many had a new version published in the last 30, 90 and 365 days (up to the DailyMed build of 2026-10-16).

| Class | SPLs (labels) | New version ≤30 days | ≤90 days | ≤365 days |
|---|---|---|---|---|
| Opioids (8 ingredients) | 1,274 | **18** | 79 | 458 |
| Gabapentinoids | 880 | 24 | 107 | 320 |
| Fluoroquinolones | 579 | 12 | 36 | 160 |
| Anticoagulants | 295 | 11 | 30 | 124 |
| GLP-1 RAs | 50 | 2 | 14 | 30 |
| JAK inhibitors | 42 | 10 | 27 | 38 |
| ICIs | 9 | 2 | 8 | 9 |

Caveat: DailyMed `drug_name` search may double-count some labels (for example, combination products). Treat these as approximate [Inf].

**This matters for the monitoring requirement.** In any 3–4 week window, opioids will produce roughly 15–20 new label versions [Inf, extrapolated from the 30-day count]. That is real drift to watch. GLP-1s will produce only a few versions, but each one tends to carry meaningful safety text.

**Label lag is a feature, not a bug** [V-API]. In the openFDA label endpoint, 163 oxycodone-containing labels were found:
- 121 mention "hyperalgesia" (the 2023 class change).
- 52 mention "toxic leukoencephalopathy" (the 2025 class change).

So many generics still lag the class-wide updates. A monitor can show "label X has not caught up yet", which is a strong drift story [Inf].

### 1c. Concrete dated examples

| Date | Class | What changed | Section | Conf. |
|---|---|---|---|---|
| Jul 2016 | Fluoroquinolones | Boxed Warning revised for disabling, potentially permanent effects. Use restricted for uncomplicated infections. | BW | [V-src] [16] |
| Jul 2018 | Fluoroquinolones | Hypoglycemic coma and mental-health effects strengthened | WP | [2nd] [17] |
| 20 Dec 2018 | Fluoroquinolones | Aortic aneurysm/dissection warning | WP | [2nd] [17] |
| 19 Dec 2019 | Gabapentinoids | Respiratory depression warning (with opioids/CNS depressants, COPD, elderly) | WP | [V-src] [19] |
| 4 Mar 2020 | Montelukast | Boxed Warning for neuropsychiatric events | BW | [V-src] [2] |
| 1 Sep 2021 | JAK inhibitors | Boxed Warning: MACE, cancer, thrombosis, death. This came from the ORAL Surveillance **trial**, not FAERS. | BW | [V-src] [2], [2nd] [18] |
| Apr 2023 → 15 Dec 2023 | Opioids (IR + ER/LA) | Class-wide update announced Apr 2023, approved 15 Dec 2023. Overdose risk rises with dose. ER/LA reserved for severe persistent pain. New **opioid-induced hyperalgesia (OIH)** warning. | WP (OIH) | [V-src] [3] |
| OIH placement check | Opioids | OxyContin label (effective 2026-06-24): OIH is in **Warnings and Precautions, not the Boxed Warning**. Some press said "boxed warning", which is wrong. | WP | [V-API] [37] |
| Sep 2023 | GLP-1 (Ozempic) | Ileus added to postmarketing ADRs | AR 6.3 | [2nd, low confidence] [40] |
| 11 Jan 2024 | GLP-1 | FDA preliminary review: no evidence GLP-1s cause suicidal thoughts | none (DSC) | [V-src] [2], [9] |
| ~1–5 Nov 2024 | GLP-1 class | Pulmonary aspiration during anesthesia/deep sedation | WP | [2nd] [7]. Ozempic labels contain "pulmonary aspiration" [V-API] |
| 28 Jan 2025 / 14 Oct 2025 / 1 Jun 2026 | Ozempic | SrLC supplements: severe GI reactions, acute pancreatitis wording, postmarketing ADRs | WP, AR | [V-API] [39] |
| Jun 2025 (EU), 5 Feb 2026 (UK) | Semaglutide | NAION added as a "very rare" side effect in EU/UK labels | EU/UK SmPC | [V-src] [10], [2nd] [11] |
| Oct 2026 check | Semaglutide (US) | The current US Ozempic (Jun/Jul/Aug 2026) and Wegovy (Jun 2026) SPLs do **not** contain "optic" or "NAION" | — | [V-API] [38] |
| 31 Jul 2025 | Opioids | Long-term-use class update: risk estimates, "extended treatment period" removed from Indications, taper warning, gabapentinoid interaction, toxic leukoencephalopathy, opioid-induced esophageal dysfunction | Indications, WP, DI | [V-src] [4] |
| 22 Dec 2025 | Opioids | Safety labeling changes approved (per FDA letter) | — | [V-src] [5] |
| 19 Feb 2026 → 2026 | Opioids | Opioid Analgesic REMS modification: naloxone/nalmefene, updated FDA Education Blueprint (Mar 2026) | REMS | [V-src] [5] |
| 13 Jan 2026 | GLP-1 (Saxenda, Wegovy, Zepbound) | FDA asks makers to **remove** the suicidal behavior/ideation warning | WP removed | [V-src] [8] |
| 27 Jun 2025 | CAR-T (CBER) | REMS removed for 6 autologous CAR-T products | REMS | [2nd] [20] |

Note on the GLP-1 suicide warning: the Wegovy SPL dated 30 Jun 2026 still contains the word "suicidal" [V-API]. We have not checked whether this is leftover warning text or other wording. If it is leftover, it is a good live example of "label not yet updated after an FDA request" [Inf].

---

## 2. Recalls (openFDA drug enforcement reports) [V-API]

openFDA enforcement data was last updated 2026-10-07 and runs from 2012-06-20 to 2026-10-07. Search used `product_description:"<ingredient>"`.

### 2a. By class

| Class | All-time records | Last 12 months (Oct 2025–Oct 2026) | Distinct report dates, last 12 mo | Status "Ongoing" now |
|---|---|---|---|---|
| Opioids | 834 | 20 | 14 | 47 |
| GLP-1 RAs | 83 | 29 | 7 | **70** |
| Anticoagulants | 152 | 5 | 2 | 13 |
| Fluoroquinolones | 89 | 3 | 1 | 25 |
| Antipsychotics | 86 | 3 | 3 | 18 |
| Gabapentinoids | 35 | 2 | 1 | 8 |
| ICIs | 6 | 2 | 2 | 2 |
| JAK inhibitors | 0 (no matches) | 0 | 0 | 0 |

### 2b. By drug (all-time, by recall class: I = most serious)

| Drug | Class I | Class II | Class III | Since 2024 |
|---|---|---|---|---|
| Fentanyl | 18 | 320 | 19 | 29 |
| Hydromorphone | 12 | 174 | 3 | 9 |
| Morphine | 15 | 162 | 12 | 7 |
| Heparin | 22 | 96 | 0 | 1 |
| Semaglutide | 0 | 54 | 0 | 43 |
| Tirzepatide | 1 | 20 | 0 | 20 |
| Oxycodone | 1 | 12 | 12 | 3 |

### 2c. What the recalls actually are

- **Opioid recalls are mostly hospital IV products from 503B outsourcing facilities (compounders).** Top firms for fentanyl: PharMEDium (69), The Compounding Pharmacy of America (42), Central Admixture Pharmacy Services (35), QuVa (30), SCA (22+13) [V-API]. Typical reasons are "lack of assurance of sterility" and cGMP deviations.
  - Example: Leiters Health, Feb 2024, **Class I**. Fentanyl IV bags were superpotent because the bag-filling system could give a double dose [V-API].
  - This is *exactly* the product a hospital pharmacy buys. That gives strong relevance [Inf].
- **Fentanyl patch recall:** Alvogen 25 mcg/h transdermal, Class I, report date 2025-02-26. Patches could be stuck together ("multi-stacked") [V-API], [2nd] [31].
- **GLP-1 recalls are almost all compounded semaglutide/tirzepatide** from 503A/503B pharmacies. Examples: Apollo Care, ProRx, AEQUITA, Thrive. They are mostly "lack of assurance of sterility" [V-API].
  - One Class I label mix-up: product labeled tirzepatide actually contained testosterone cypionate (Revive Rx, 2024-06-05) [V-API].
  - These follow the end of the shortages: tirzepatide declared resolved 19 Dec 2024, semaglutide 21 Feb 2025 [2nd] [14], [15].
  - Hospital relevance is lower, because compounded GLP-1s are mostly outpatient or telehealth [Inf].
- **Rhythm for a 3–4 week window:** opioid recalls arrive on about 1–2 report dates a month. GLP-1 recalls cluster on few dates (7 in 12 months). Expect **0–3 new recall events** in a live 3–4 week window for either class [Inf, from counts above]. Recalls alone will not show drift. Label versions will.

### 2d. Shortages (context)

- Injectable opioid shortage in 2018: 98.4% of 343 ASHP survey respondents reported shortages of morphine, hydromorphone or fentanyl [2nd] [29].
- Hydromorphone injection was again in shortage in March 2025 [2nd] [30].
- Shortages drive compounding, and compounding drives recalls [Inf].

---

## 3. FAERS volume and known data problems [V-API]

FAERS is the FDA Adverse Event Reporting System. The openFDA event endpoint was last updated **2026-07-30**, with 20.69 M reports in total. Counts below use `patient.drug.activesubstance.activesubstancename`.

| Drug | 2021 | 2023 | 2025 | Trend |
|---|---|---|---|---|
| Oxycodone | 72,909 | 39,498 | 14,463 | falling fast |
| Fentanyl | 10,022 | 11,528 | 6,876 | falling |
| Tirzepatide | 35 | 20,803 | **62,342** | exploding |
| Semaglutide | 5,514 | 11,875 | 27,496 | rising |
| Pembrolizumab | 8,470 | 15,876 | 17,366 | steady rise |
| Apixaban | 34,941 | 26,476 | 23,830 | gently falling |
| Levofloxacin | 6,530 | 5,199 | 4,577 | flat/falling |

### Known problems by class

| Problem | Evidence | Conf. |
|---|---|---|
| **Opioids: lawsuit-stimulated reporting.** 40,008 of 72,909 oxycodone reports in 2021 (55%) came from reporter type "lawyer" (`primarysource.qualification = 4`). This fell to 812 in 2023 and 113 in 2025. Across all years, lawyers filed 100,997 oxycodone reports. | openFDA count | [V-API]. Litigation reports are known to mask other signals [32] |
| **Opioids: abuse/overdose dominance.** Top oxycodone PTs: Drug dependence (102k), Pain, Overdose (54k), Emotional distress (49k, typical of litigation), Withdrawal, Death. In 2023, 27,156 of 39,498 oxycodone reports (69%) carried at least one abuse/dependence/overdose/withdrawal/toxicity term. | openFDA count | [V-API] |
| **Opioids: how this hurts our signal rule.** These PTs *are* on opioid labels (Boxed Warning), so "unlabeled" filtering removes them. But they inflate the denominator and mask real ADRs in disproportionality maths (PRR/ROR). | — | [Inf] |
| **Opioids: OIH is hard to find by MedDRA term.** openFDA returned **zero** reports with PT "HYPERALGESIA" across all FAERS. Press reports say FDA used 46 FAERS cases [6], so those cases must be coded under other terms (e.g. "Allodynia": 123 opioid reports before Jul 2025). A naive PT match would miss this backtest. | openFDA count | [V-API] + [Inf] |
| **GLP-1: medication errors and consumer reports dominate.** Top tirzepatide PT is "Incorrect dose administered" (29,672), plus "Extra dose administered" (9,608). 146,863 of about 160k tirzepatide reports come from consumers (qualification 5), mostly via manufacturer patient-support programs [Inf]. | openFDA count | [V-API] |
| **GLP-1: stimulated reporting after news.** The PT "Optic ischaemic neuropathy" with GLP-1s went from 79 reports (to Oct 2024) to 1,028 (all time). This is a 13× jump after the 2024 publications and EU action. | openFDA count | [V-API]. Media/safety-action effect on FAERS is documented [33] |
| **GLP-1: compounded products.** FDA received 990 compounded-semaglutide and 730+ compounded-tirzepatide adverse event reports by 31 May 2026. These may be mixed with the branded drug under the same ingredient name. | press | [2nd] [13], FDA page [12] |
| **GLP-1: drug-name harmonisation gap.** Semaglutide gives 73,001 reports via `openfda.generic_name` but 100,679 via `activesubstancename`. Choose the field deliberately: drug identity resolution matters. | openFDA count | [V-API] |
| **ICIs: disease confounding.** The top pembrolizumab PT is "Malignant neoplasm progression" (12,012). | openFDA count | [V-API] |
| **Anticoagulants: indication confounding.** The top apixaban PTs are Atrial fibrillation (4,089) and Cerebrovascular accident (3,586). | openFDA count | [V-API] |
| **All classes: role not bound in openFDA.** A query like "drug X AND drugcharacterization:1" matches if *any* drug in the report is suspect, not X. The suspect-only filter must be done on the raw/bulk data. | test query returned ~same totals | [V-API] + [Inf] |
| **Freshness.** FDA moved the FAERS **Public Dashboard** to daily updates in late Aug 2025 [34]. But openFDA (our API) was last updated 2026-07-30, so it is still quarterly-ish. "What changed since yesterday" for FAERS needs the dashboard/bulk route, or a replay. | — | [2nd] [34], [V-API] |

---

## 4. Hospital relevance

| Source | What it says | Classes it favours | Conf. |
|---|---|---|---|
| HHS National Action Plan for ADE Prevention (2014) | Three priority classes: **anticoagulants, diabetes agents, opioids**. About 1 in 3 inpatient adverse events are ADEs, and about 2 in 3 of those involve these three classes. | Opioids, anticoagulants, (diabetes agents → GLP-1 partly) | [V-src] [21], [22] |
| ISMP High-Alert Medications, Acute Care (2024 edition) | Includes opioids (IV, oral, transdermal), antithrombotics, insulin, and chemotherapy. Tranexamic acid was added in Jan 2024. GLP-1 RAs and antibiotics are **not** on the list (to our knowledge). | Opioids, anticoagulants | [2nd] [24], [25], [26]. We could not open the ISMP PDF itself [23] |
| Joint Commission | NPSG.03.05.01 covers anticoagulant therapy. LD.04.03.13 covers pain management and safe opioid prescribing. | Anticoagulants, opioids | [V-src] [27], [2nd] [28] |
| Perioperative practice | GLP-1 aspiration risk under anesthesia (Nov 2024 label) makes GLP-1s a real inpatient/OR question | GLP-1 | [2nd] [7] |

---

## 5. Candidate notes

### Opioids: honest pros and cons

| Pros | Cons |
|---|---|
| Top hospital relevance: ISMP high-alert, HHS ADE priority, Joint Commission standard [21], [27] | FAERS is dominated by abuse, overdose and litigation reports (55% from lawyers in 2021) [V-API] |
| Biggest recall stream that hospitals actually buy (503B IV fentanyl/hydromorphone/morphine) [V-API] | Labels are huge and mature, so few truly "unlabeled" events remain. Most top PTs are already in the Boxed Warning [Inf] |
| Two recent class-wide label waves (Dec 2023, Jul–Dec 2025) plus a 2026 REMS change [3], [4], [5] | 1,274 SPLs, mostly generics/repackagers. Heavy drug-identity work [V-API] |
| Generic labels lag the class update, which gives a visible label-drift story [V-API] | Buprenorphine/methadone used for OUD mix indications. Combination products (APAP) add hepatotoxicity noise [Inf] |
| Backtest exists: leukoencephalopathy had 285 opioid reports and esophageal-motility PTs had 69 before the Jul 2025 label [V-API] | OIH backtest fails on a naive PT match (0 "Hyperalgesia" reports) [V-API] |
| — | No SrLC opioid entries yet in 2026. Change comes in waves, not steadily [V-API] |

**Verdict on opioids [Inf]:** a good **anchor**, a weak **solo** class. It passes "real-world need" with ease. It partly passes "constant change": many label versions and recalls, but few *new safety findings*. The demo risk is that the signal list looks like "overdose, dependence, death": known, labeled and not insightful. That needs an explicit filter (exclude abuse/misuse SMQ terms and lawyer reports, and say so).

### GLP-1 RAs
- Fastest-moving safety story: aspiration (2024), suicide warning added then removed (2024 → 2026), NAION (EU 2025 / UK 2026, **not on the US label**) [V-src], [V-API].
- Highest FAERS growth [V-API].
- Weaker on inpatient relevance and very messy: dose errors, compounded products, stimulated reporting.
- NAION is a ready-made demo case. **It must be worded carefully:** "reported, and on EU/UK labels, not on the US label". **Never** "caused by" [Inf].

### Others
- **Anticoagulants:** the most clinically serious, but labels are mature and recalls are rare (5 in 12 months). Bleeding and indication terms swamp the signal list.
- **ICIs:** frequent label edits, but cancer confounds FAERS and recalls are almost nil.
- **JAK inhibitors:** steady label change, but the 2021 boxed warning came from a trial, not FAERS. No recalls. Low hospital use.
- **Fluoroquinolones:** good *historical* backtest (2016–2018) but almost no change since 2023 (5 SrLC entries).
- **Gabapentinoids:** a natural add-on to opioids (2019 respiratory depression, 2025 opioid-label interaction), but slow-moving.
- **CAR-T:** regulated by CBER (FDA's biologics center), so it sits outside the CDER SrLC database. Too few products. Not recommended.

---

## 6. Recommendation

**PV SME view:** Use an **opioid-led hybrid: 8 hospital opioids + 5 GLP-1 RAs (13 ingredients)**.
- **Opioids** answer "what keeps a hospital safety officer up at night" and supply most recalls and label-version drift.
- **GLP-1s** supply steady safety-label change and the cleanest "would we have caught it?" backtests: aspiration 2024, NAION today.

This keeps the boss's choice, and fixes its two weak spots: few new signals, and noisy FAERS.

If only one class is allowed: **choose opioids, with three conditions.**
1. Drop lawyer-reported cases and the abuse/misuse/overdose terms from signal ranking, and show that you did.
2. Restrict to RLD/brand labels plus hospital IV products, so you are not tracking all 1,274 SPLs.
3. Demonstrate drift with label-version lag and recalls, not with "new" FAERS signals.

### Risks to state up front
- FAERS has no denominator, so counts are **reporting** patterns, not incidence or causation.
- Stimulated reporting: litigation (opioids) and media (GLP-1).
- Duplicates, and the suspect vs concomitant role must be handled in bulk data.
- MedDRA licensing applies if we use SMQs (Standardised MedDRA Queries) rather than our own term lists.

### Assumptions
- "Drug" for the 50–200 limit is counted at product/SPL level after RxNorm grouping [Inf].
- Hospital formulary includes GLP-1s. They are common, but mostly continued home medications [Inf].
- openFDA counts include all reported roles (suspect and concomitant). We did not check them against FAERS quarterly files.

### What I would check next
1. Get the ISMP 2024 PDF itself and confirm GLP-1s are absent.
2. Pull the FAERS bulk file and redo the oxycodone counts with **primary-suspect only + case-level dedup**.
3. Map the 46 OIH FAERS cases to MedDRA PTs, so the backtest does not miss them.
4. Check whether NAION is under FDA review (FDA "Potential Signals of Serious Risks" quarterly postings), so the demo wording is accurate.
5. Confirm the Wegovy Jun 2026 SPL text about suicidality (removed or still present).

---

## Method (so anyone can rerun this)

| Data | Query pattern | Run on |
|---|---|---|
| Recalls | `api.fda.gov/drug/enforcement.json?search=product_description:"X"[+AND+report_date:[A+TO+B]]&count=classification.exact` (also `count=recalling_firm.exact`, `count=status.exact`, `count=report_date`) | 2026-10-19 |
| FAERS volume | `api.fda.gov/drug/event.json?search=patient.drug.activesubstance.activesubstancename:"X"+AND+receivedate:[Y0101+TO+Y1231]&limit=1` (read `meta.results.total`) | 2026-10-19 |
| FAERS top PTs | `...&count=patient.reaction.reactionmeddrapt.exact` | 2026-10-19 |
| Reporter type | `...&count=primarysource.qualification` (1 physician, 2 pharmacist, 3 other HCP, 4 lawyer, 5 consumer) | 2026-10-19 |
| Labels | `api.fda.gov/drug/label.json?search=openfda.generic_name:"X"+AND+"term"&count=effective_time` | 2026-10-19 |
| SPL versions | `dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=X` and `/spls/{setid}/history.json`, `/spls/{setid}.xml` | 2026-10-19 (DailyMed build 2026-10-16) |
| SrLC | POST `drug_name=X` to the SrLC search page, then parse each `searchdetail.page&DrugNameID=` page (dates, supplement no., sections) | 2026-10-19 |

All API queries succeeded except "no matches" (HTTP 404). We report those as 0. The SrLC page has no API. Our scraper parsed the HTML, so section tagging may have small errors [Inf].

---

## Sources (all accessed 2026-10-19)

1. FDA — Drug Safety-related Labeling Changes (SrLC) database. https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/
2. FDA — Drug Safety Communications (index). https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications
3. FDA — FDA approves safety labeling changes for opioid pain medicines (Dec 15, 2023). http://www.fda.gov/drugs/drug-alerts-and-statements/fda-approves-safety-labeling-changes-opioid-pain-medicines
4. FDA — FDA is requiring opioid pain medicine manufacturers to update prescribing information regarding long-term use (Jul 31, 2025). https://www.fda.gov/drugs/drug-safety-communications/fda-requiring-opioid-pain-medicine-manufacturers-update-prescribing-information-regarding-long-term
5. FDA — Supplement approval letter NDA 022402/S-019 (OA REMS modification; references Dec 22, 2025 labeling changes). https://www.accessdata.fda.gov/drugsatfda_docs/appletter/2026/022402Orig1s019ltr.pdf
6. Drug Topics — FDA now requiring new warnings for prescription opioids (Apr 2023). https://www.drugtopics.com/view/fda-now-requiring-new-warnings-for-prescription-opioids
7. Becker's Hospital Review — FDA adds warning to Ozempic, Mounjaro and other GLP-1 labels. https://www.beckershospitalreview.com/pharmacy/fda-adds-warning-to-ozempic-mounjaro-and-other-glp-1-labels/
8. FDA — FDA requests removal of suicidal behavior and ideation warning from GLP-1 RA medications (Jan 13, 2026). https://www.fda.gov/drugs/drug-safety-communications/fda-requests-removal-suicidal-behavior-and-ideation-warning-glucagon-peptide-1-receptor-agonist-glp
9. FDA — Update on FDA's ongoing evaluation of reports of suicidal thoughts or actions (Jan 2024). https://www.fda.gov/drugs/drug-safety-and-availability/update-fdas-ongoing-evaluation-reports-suicidal-thoughts-or-actions-patients-taking-certain-type
10. MHRA — Semaglutide: risk of NAION (Drug Safety Update). https://www.gov.uk/drug-safety-update/semaglutide-wegovy-ozempic-and-rybelsus-risk-of-non-arteritic-anterior-ischemic-optic-neuropathy-naion
11. TCTMD — Eye condition a "very rare" side effect of semaglutide, EMA says. https://www.tctmd.com/news/eye-condition-very-rare-side-effect-semaglutide-ema-says
12. FDA — FDA's concerns with unapproved GLP-1 drugs used for weight loss. https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/fdas-concerns-unapproved-glp-1-drugs-used-weight-loss
13. Becker's Hospital Review — FDA warns clinicians on compounded GLP-1s amid 1,700+ safety reports. https://www.beckershospitalreview.com/glp-1s/fda-warns-on-compounded-glp-1s-amid-1700-safety-reports/
14. McDermott Will & Emery — Tirzepatide shortage resolved. https://www.mwe.com/?p=290932
15. McDermott Will & Emery — Semaglutide shortage resolved. https://www.mwe.com/?p=311415
16. FDA — Drug Safety Communication: FDA updates warnings for oral and injectable fluoroquinolone antibiotics (2016). https://www.fda.gov/drugs/drug-safety-and-availability/fda-drug-safety-communication-fda-updates-warnings-oral-and-injectable-fluoroquinolone-antibiotics
17. CIDRAP — FDA: Fluoroquinolones may cause aortic rupture in some (Dec 2018). https://www.cidrap.umn.edu/news-perspective/2018/12/fda-fluoroquinolones-may-cause-aortic-rupture-some
18. Healio — FDA adds black box warning to JAK inhibitors (Sep 1, 2021). https://www.healio.com/news/rheumatology/20210901/fda-adds-black-box-warning-to-jak-inhibitors-cites-heartrelated-issues-cancer-death
19. FDA — Gabapentin and pregabalin Drug Safety Communication: serious breathing problems (Dec 19, 2019). https://www.fda.gov/safety/medical-product-safety-information/neurontin-gralise-horizant-gabapentin-and-lyrica-lyrica-cr-pregabalin-drug-safety-communication
20. AABB — FDA eliminates REMS for approved CAR T-cell therapies (Jun 30, 2025). https://www.aabb.org/news-resources/news/article/2025/06/30/fda-eliminates-rems-for-approved-car-t-cell-therapies
21. HHS — National Action Plan for Adverse Drug Event Prevention (2014). https://health.gov/sites/default/files/2019-09/ADE-Action-Plan-508c.pdf
22. ODPHP — Improving patient safety through the National Action Plan for ADE Prevention. https://odphp.health.gov/news-archive/blog/2015/08/improving-patient-safety-through-the-national-action-plan-for-adverse-drug-event-prevention/index.html
23. ISMP/ECRI — High-alert medications in acute care settings. https://home.ecri.org/blogs/ismp-resources/high-alert-medications-in-acute-care-settings
24. AHRQ PSNet — ISMP's list of high-alert medications in acute care settings. https://psnet.ahrq.gov/issue/ismps-list-high-alert-medications-acute-care-settings
25. Ventura County Health Care Agency — High-alert medications policy (reproduces ISMP list). https://hospitals.vchca.org/images/pharmacy_hca/2022High_Alert_Medications.pdf
26. ISMP — High-alert medications in acute care settings (2018 copy). https://ajemjournal.com/sites/default/files/attachments/2018-08/highAlert2018-Acute-Final.pdf
27. The Joint Commission — Anticoagulation therapy: understanding the requirements (NPSG.03.05.01 FAQ). https://www.jointcommission.org/standards/standard-faqs/ambulatory/national-patient-safety-goals-npsg/000002244
28. Becker's ASC — Joint Commission proposes new pain standards with emphasis on opioid safety. https://www.beckersasc.com/asc-accreditation-and-patient-safety/the-joint-commission-proposes-new-pain-standards-with-emphasis-on-opioid-safety-3-key-changes/
29. Healio — Urgent action necessary to address opioid drug shortage (2018). https://www.healio.com/news/hematology-oncology/20180816/urgent-action-necessary-to-address-opioid-drug-shortage
30. University of Illinois Vet Med — Current drug shortages: hydromorphone (Mar 2025). https://vetmed.illinois.edu/2025/03/25/current-drug-shortages-hydromorphone/
31. Optum Rx — Drug recall: fentanyl transdermal (Feb 2025). https://prod-prorx.optum.com/content/dam/noindex-resources/business/support-documents/drug-recalls-availability/drugrecall_fentanyl_2025-0203.pdf
32. RAPS — FDA officials explain when litigation can impact disproportionality analyses. https://www.raps.org/resource/fda-officials-explain-when-litigation-can-impact-d.html
33. FDLI — Does attorney advertising stimulate adverse event reporting? https://www.fdli.org/2020/06/does-attorney-advertising-stimulate-adverse-event-reporting/
34. HealthDay — FDA now providing daily updates on adverse events (Aug 2025). https://www.healthday.com/healthpro-news/general-health/fda-now-providing-daily-updates-on-adverse-events
35. openFDA — Drug enforcement API (queried). https://api.fda.gov/drug/enforcement.json
36. openFDA — Drug adverse event (FAERS) API (queried). https://api.fda.gov/drug/event.json
37. openFDA — Drug label API (queried). https://api.fda.gov/drug/label.json
38. NLM DailyMed — Web services v2 (SPL list, history, XML; queried). https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json
39. FDA SrLC — Ozempic detail page. https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/index.cfm?event=searchdetail.page&DrugNameID=2183
40. The Rx Index — GLP-1 FDA label changes tracker (low confidence). https://therxindex.com/research/glp-1-fda-label-changes/
