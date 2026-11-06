# Another month: outside sources + a pharmacist review loop

_🔎 Researcher view, with a 🛡️ Compliance lens · Scan date: 2026-11-05 · Read-only web scan (no sign-ups, no logins, no downloads) · Stage: **Ideate** (design thinking)_

Feeds the brief's "what would you do with another month" ([brief summary](../00-brief/brief-summary.md)). **Nothing here enters pilot scope** ([pilot-to-production](pilot-to-production.md)).

How to read this file:
- **Fact** = stated on the linked page. **Inference** = my reading, marked _(inference)_.
- "(search summary)" = the fact came from a search-result summary. I could not open the page itself (often HTTP 403). Treat it as less sure.

---

## TL;DR

1. The biggest gap is not data. It is a **named pharmacist** who signs off the synonym bands (258 rows), the AI gold set, and the top ranked signals. Today only Claude has reviewed them ([A014](../05-approaches/A014-label-faers-synonym-table.md), [A011](../05-approaches/A011-ai-label-extraction-pilot.md)).
2. With another month: build a **review loop**. Claude prepares an evidence packet with links (label quote, PubMed, FDA safety notices). The pharmacist decides. The decision is saved through a **create-only Foundry Action**, so it is audited.
3. Best tools for that loop: Anthropic's free **PubMed** and **ClinicalTrials.gov** connectors, plus FDA's **SrLC** and **Drug Safety Communications**, plus **OnSIDES** (open label-side-effect data, CC BY 4.0) as a second opinion. Palantir's **Ontology MCP** could let Claude read our signals directly.
4. **Orange Book** is a cheap, useful add (free, joins on our application-number key). **DrugBank** is strong but its API is commercial-only and academic downloads are paused. **NIDA** data is about population drug misuse, not label gaps: low fit. **"ClinHub"** is most likely a commercial trial-data platform (ThoughtSphere): not relevant.
5. Compliance: no patient data anywhere in the loop. Anthropic's BAA does **not** cover connectors/MCP, so the loop must stay PHI-free. Watch licences: MedDRA, DrugBank (non-commercial), SIDER (non-commercial, share-alike).

---

## 1. Per source

### 1.1 "clin org" → most likely **ClinicalTrials.gov**

**How sure:** about 80% _(inference)_. The brief lists ClinicalTrials.gov as a source ([brief summary](../00-brief/brief-summary.md)). The search for "clin.org" / "clinicaltrials.org" found nothing else; results pointed back to clinicaltrials.gov ([arXiv CTG-DB](https://arxiv.org/html/2603.15936v1)).
Other candidates checked:
- **ClinPGx.org** (the new name of PharmGKB, a pharmacogenomics knowledge base). Data is CC BY-SA 4.0 ([data.gov](https://catalog.data.gov/dataset/clinpgx), [CASRAI](https://www.casrai.org/dictionary/term/pharmgkb-clinpgx-pharmacogenomics-knowledgebase)). About genes and drug response, not label gaps. ~10% likely, low fit.
- **AACT** (aact.ctti-clinicaltrials.org): a relational database copy of ClinicalTrials.gov ([AACT docs](https://aact.ctti-clinicaltrials.org/documentation/329)). Same data, easier SQL. Possible "org" the user meant.

| | |
|---|---|
| **What it is** | The US registry of clinical studies, run by NLM (National Library of Medicine) at NIH ([Claude tutorial](https://academy.claude.com/tutorials/using-the-clinicaltrials-gov-connector-in-claude)). |
| **What it offers us** | Trial **results include adverse events** (the field path `resultsSection.adverseEventsModule…` exists per [AACT](https://aact.ctti-clinicaltrials.org/documentation/329)). The brief calls this a "second opinion": was the reaction seen in trials, and vs placebo? |
| **Access** | REST API v2 (JSON), updated daily ([Claude tutorial](https://academy.claude.com/tutorials/using-the-clinicaltrials-gov-connector-in-claude)). Rate limit about 50 requests/min per IP — third-party docs only, **not verified** ([BioMCP reference](https://glama.ai/mcp/servers/@genomoncology/biomcp/blob/a5e305a87586baa77435cfd12128f56cfdf16069/docs/backend-services-reference/04-clinicaltrials-gov.md)). Also an Anthropic connector (section 1.6). |
| **Licence & cost** | Free. Terms of use page **not opened** in this scan (the API pages returned no content). |
| **PHI risk** | None. Summary results only. |
| **Known mess** | Only 58.3% of FDA-reviewed trials posted safety results there; AE terms are free text, not standard codes ([PMC9378423 via search](https://pmc.ncbi.nlm.nih.gov/articles/PMC9378423/)). |
| **Fit** | **Medium.** Good second opinion for a pharmacist ("seen in trials at X% vs placebo"). We cut it from the pilot (D031 cut list), and matching free-text AE terms to FAERS terms is its own synonym problem. |

### 1.2 "clinhub" → several products; **none clearly drug-safety for us**

**How sure:** low (about 50% for the first row) _(inference)_. Ask the user.

| Product | What it is | Relevant to drug safety? |
|---|---|---|
| **ClinHUB (ThoughtSphere)** | Clinical-trial data hub for sponsors. Pulls trial data from many systems (EDC, labs, imaging), maps it with ML; base for their risk-based monitoring tools ([CB Insights](https://www.cbinsights.com/investor/thoughtsphere), [Clinical Research News](https://www.clinicalresearchnewsonline.com/news/2017/08/02/thoughtsphere-builds-a-data-lake-for-clinical-trials)). ThoughtSphere also lists safety case processing as a service (CB Insights). | Indirect. It is for a drug company's own trial data. Commercial, not public. **Low fit.** |
| **ClinicalTrialsHub** (research paper) | A research system linking trial registries with published literature ([arXiv 2512.08193](https://arxiv.org/html/2512.08193v1)). | Somewhat (trials + papers). A paper, not a service we can use. **Low.** |
| **navify Clinical Hub (Roche)** | Care-team disease management ([Roche](https://navify.roche.com/us/en-us/marketplace/products/navify-clinical-hub)). | No. |
| **The Clinical Hub (HealthStream)** | Manages student clinical rotations ([HealthStream](https://www.healthstream.com/theclinicalhub)). | No. |
| **ClinicHub (Zapath, Japan)** | AI marketing for private clinics ([IT Business Today](https://itbusinesstoday.com/health-tech/zapath-launches-clinichub-a-service-that-uses-ai-to-help-private-clinics-attract-patients-more-efficiently/)). | No. |

No hospital-pharmacy product called "ClinHub" was found (search). PHI risk: ThoughtSphere ClinHUB handles trial participant data; we would not touch it.

### 1.3 DrugBank (drugbank.com)

| | |
|---|---|
| **What it is** | A curated drug knowledge base (drugs, targets, interactions, clinical data). |
| **What it offers us** | A structured **adverse effects** module: incidence, evidence type, patient group; mostly taken from product labeling ([DrugBank blog](https://blog.drugbank.com/leverage-the-clinical-api-adverse-effects/), [data package](https://go.drugbank.com/data_packages/clinical_insights/data_modules/structured_adverse_effects)). Could cross-check our AI label extraction. |
| **Access** | Clinical API with adverse-effect search endpoints ([dev guide](https://dev.drugbank.com/guides/implementation/adverse_effects)). API, MCP and GraphQL access sit in the commercial tier (search summary of [pricing](https://go.drugbank.com/pricing/); page returned 403). No official Claude connector found; unofficial MCP servers exist ([lobehub](https://lobehub.com/mcp?q=drug), [glama](https://glama.ai/mcp/servers/nu4jzr0tse)) — avoid. |
| **Licence & cost** | **Academic:** free, CC BY-NC 4.0 (non-commercial), only for students/staff at an academic institution whose work is not mainly for a commercial third party. **Academic downloads are paused** (release 5.1.22, 2026-06-27) ([release page](https://go.drugbank.com/releases/5-1-22)). **Commercial:** price not published; usage-based (search summary of pricing page). |
| **PHI risk** | None. |
| **Fit** | **Low for now, medium for production.** _(inference)_ A build for a company is likely "commercial use", so the academic licence probably does not apply. Downloads are paused anyway. Its labeling-derived data overlaps what we already pull from DailyMed. |

### 1.4 FDA Orange Book

| | |
|---|---|
| **What it is** | FDA's list of approved drug products with **therapeutic equivalence** ratings (which generics can substitute for a brand), plus **patents** and **exclusivity**. |
| **What it offers us** | `Products.txt`: ingredient, form/route, trade name, applicant, strength, approval date, Rx/OTC/discontinued, **TE code**, **RLD** (reference listed drug) and **RS** (reference standard) flags. `Patent.txt`: patent number, expiry, use code. `Exclusivity.txt`: code + expiry date ([FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files)). |
| **Access** | Monthly ZIP of three tilde-separated (`~`) text files ([FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files)). Also an openFDA `orangebook` JSON endpoint ([openFDA drug APIs](https://open.fda.gov/apis/drug/)) — fits our existing openFDA REST source (D038). |
| **How it joins to our keys** | Key = **Appl_Type** (N = NDA brand, A = ANDA generic) + **Appl_No** (6 digits) + **Product_No** (3 digits, one per strength) ([FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files)). _(inference)_ Our product key is the application number (D039), so: strip the `NDA`/`ANDA` prefix, zero-pad to 6 → join. **NDC** (National Drug Code): via the openFDA NDC record's application number. **RxCUI** (RxNorm concept ID): via openFDA's harmonised `openfda` block or RxNorm NDC→RxCUI. Harmonisation needs exact matches and some records have none ([openFDA fields](https://open.fda.gov/apis/openfda-fields/)). |
| **Licence & cost** | Free. No terms stated on the page ([FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files)); US government data _(inference: public domain)_. |
| **PHI risk** | None. |
| **Fit** | **Medium.** _(inference)_ Two real uses: (1) the **RLD flag** tells us which label FDA treats as the reference — a defensible way to pick our "one reference label" per ingredient; (2) **TE codes** show which generics are interchangeable, so the officer sees that a recall or signal touches substitutable products. Overlaps Drugs@FDA, which we already use (D026). |

### 1.5 NIDA (National Institute on Drug Abuse)

| Resource | What it offers | Access & terms | Fit |
|---|---|---|---|
| **NDEWS** (National Drug Early Warning System) | NIDA-funded early warning on emerging drugs; run by University of Florida. Uses sentinel sites, wastewater, 911-dispatch data, poison centres, drug seizures (search summary of [NDEWS](https://ndews.org/about/), [NIDA](https://drugabuse.gov/node/18874)). | Weekly Briefing by subscription; no public raw-data download found. Contact `ndews-cc@ufl.edu` (search summary). | **Low.** Street-drug trends (e.g. fentanyl analogues), not label gaps. |
| **Monitoring the Future (MTF)** | Annual survey of youth/young adults, incl. prescription opioid misuse items (search summary of [ICPSR](https://www.icpsr.umich.edu/web/ICPSR/studies/39699/staff)). | Public-use files via NAHDAP/ICPSR, free, no member institution needed; for aggregated statistics only. Restricted files need a data use agreement + virtual enclave (search summary of [MTF data access](https://monitoringthefuture.org/results/data-access/), page returned 403). | **Low.** Yearly, population-level. Context only. |
| **NIDA Data Share / NAHDAP** | Data from completed NIDA trials; addiction research archive ([NIDA resources](https://nida.nih.gov/research/research-data-measures-resources), [NAHDAP](https://nida.nih.gov/research/nida-research-programs-activities/nahdap-data-repository-for-drug-addiction-and-HIV-research)). | Public-use and restricted files. | **Low.** |
| **NSDUH** (run by SAMHSA, not NIDA) | Annual national survey incl. prescription drug misuse ([NIDA resources](https://nida.nih.gov/research/research-data-measures-resources)). | Public. | **Low.** |

PHI risk: public-use files are de-identified; restricted files are person-level → **do not use**. _(inference)_ Possible later use: context next to FAERS "abuse / overdose" signals for our 8 opioids. Not a label check.

### 1.6 Claude connectors for healthcare and life sciences

A **connector** is a plug-in (built on MCP, the Model Context Protocol) that lets Claude query an outside system and cite what it found.

**What exists (verified on Anthropic pages):**

| Connector | What it does | Source |
|---|---|---|
| **PubMed** | Search 35M+ citations; abstracts; **full text from PMC** when available; related articles; PMID/PMC/DOI conversion. Free for all Claude users; rate-limited; "may not reflect the most current" NLM data. | [Anthropic](https://www.anthropic.com/news/healthcare-life-sciences), [tutorial](https://academy.claude.com/tutorials/using-the-pubmed-connector-in-claude) |
| **ClinicalTrials.gov** | 6 tools: search_trials, get_trial_details, search_by_sponsor, search_investigators, analyze_endpoints, search_by_eligibility. **AE results not mentioned.** | [tutorial](https://academy.claude.com/tutorials/using-the-clinicaltrials-gov-connector-in-claude) |
| **CMS Coverage Database** | Medicare coverage rules (LCD/NCD) for prior auth and appeals | [Anthropic](https://www.anthropic.com/news/healthcare-life-sciences) |
| **ICD-10** | Diagnosis/procedure code lookup (CMS, CDC) | same |
| **NPI Registry** | Provider identity checks | same |
| **Medidata** | Trial enrollment and site performance data; **Medidata Study Feasibility customers only**; tutorial says it starts with help docs only | same, [tutorial](https://claude.com/resources/tutorials/using-the-medidata-connector-in-claude) |
| **ChEMBL, bioRxiv/medRxiv, Open Targets, ToolUniverse, Owkin** | Drug/compound data, preprints, drug targets, 600+ science tools, pathology | [Anthropic](https://www.anthropic.com/news/healthcare-life-sciences) |
| **Benchling, BioRender, Scholar Gateway (Wiley), Synapse.org, 10x Genomics** | Lab R&D data, figures, journals, data sharing, single-cell analysis (launched Oct 20, 2025) | [Claude for Life Sciences](https://www.anthropic.com/news/claude-for-life-sciences) |
| **Claude Science "Drug Regulatory" connector** | FDA drug data and **openFDA**, read-only, no key needed; off by default in HIPAA orgs | [Claude Science docs](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Agent Skills** | FHIR development; prior-authorization review (sample); clinical trial protocol draft (sample) | [Anthropic](https://www.anthropic.com/news/healthcare-life-sciences) |

- Plans: connectors and skills are "generally available to all Claude subscribers" (Pro, Max, Team, Enterprise). Team/Enterprise admins must add directory connectors first ([Anthropic](https://www.anthropic.com/news/healthcare-life-sciences), [Claude Science docs](https://claude.com/docs/claude-science/connectors-and-skills)).
- **Not found:** an official DailyMed or DrugBank connector. _(inference)_ The openFDA connector covers label text (openFDA `label` endpoint), and our own DailyMed links already sit in Foundry.

**Palantir side — Ontology MCP:** Foundry can expose ontology object types, **action types** and query functions as MCP tools, so an outside agent can "read objects, execute actions, and query data". Only predefined actions; access is limited by application restrictions. Palantir warns this makes Foundry data available to an external MCP client ([Palantir OMCP](https://palantir.com/docs/foundry/ontology-mcp)). Palantir's docs name Claude Cowork as a client (search summary of the same docs).

**Limits (PHI, BAA, HIPAA):**
- A **BAA** (Business Associate Agreement — the HIPAA contract that lets a vendor handle patient data) is available only on HIPAA-ready Claude Enterprise after the owner turns it on, or on the API after signing ([Anthropic privacy](https://privacy.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers)).
- **Connectors and MCP servers are not covered** by Anthropic's BAA (third-party data flows). Skills are not covered either. Claude in Chrome is not covered (same page).
- So: _(inference)_ the review loop is fine **because it never contains PHI**. If a pharmacist used it with patient data, connectors would be off-limits regardless of plan.

**Fit: High** for the review loop. The loop needs grounded, cited lookups, and these are free and read-only.

### 1.7 Other public sources a pharmacist reviewer would use

| Source | What it answers | Access · licence | PHI | Fit |
|---|---|---|---|---|
| **DailyMed** (already used, D019) | Is the term in the current label? | Already in Foundry | None | — (our label truth) |
| **OnSIDES** | Label-listed side effects for 4,097 ingredients from 51,460 labels (US, EU, UK, Japan), quarterly, data current to April 2026 | CSV / SQLite downloads; data **CC BY 4.0**, code MIT; pipeline matches label text to MedDRA terms ([GitHub](https://github.com/tatonetti-lab/onsides)) | None | **High** as a second opinion for "is it labeled?" and for the gold set (D015 benchmark). MedDRA question below |
| **SIDER 4.1** | Older label side effects with frequencies | Last release 2015-10-21, no funding; CC BY-NC-SA 4.0 ([SIDER](https://sideeffects.embl.de/), [re3data](https://www.re3data.org/repository/r3d100012791), [SIDER4 repo](https://github.com/dhimmel/SIDER4)) | None | **Low.** Stale, misses GLP-1s; non-commercial |
| **FDA Drug Safety Communications** | Has FDA publicly warned about this risk? | Web pages by year ([FDA](https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications)) | None | **High.** "Known risk" ground truth for ranked signals |
| **FDA SrLC** (Safety-related Labeling Changes) | Was a safety change added to the label since 2016, and in which section? NDA/BLA only, no generics | Searchable database ([FDA overview](https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-related-labeling-changes-srlc-database-overview-updates-safety-information-fda-approved), [SrLC](https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/)) | None | **High.** Already chosen (D026), not yet built |
| **FAERS Public Dashboard** | Quick report counts by product/reaction; export to Excel; quarterly; "a report does not establish causation" ([FDA dashboard](https://fis.fda.gov/extensions/fpdwidgets/2e01da82-13fe-40e0-8c38-4da505737e36.html)). FDA pages now also say "AEMS" ([FDA](https://www.fda.gov/drugs/surveillance/fdas-adverse-event-reporting-system-faers)) | Free, web | None | **Medium.** Lets the pharmacist sanity-check our counts independently |
| **LiverTox** (NIDDK) | Drug-induced liver injury, by drug | Public domain, copyright free ([NCBI](https://www.ncbi.nlm.nih.gov/books/NBK547852/)) | None | **Medium** for liver signals |
| **LactMed** (NLM) | Drugs in breastfeeding | Free; bulk via NLM Open Access subset under NLM terms ([NCBI](https://www.ncbi.nlm.nih.gov/books/NBK547439/)) | None | **Low** (narrow population) |
| **MedDRA** (the standard dictionary of adverse-event terms; FAERS uses it) | Term hierarchy and **SMQs** (standard groupings of related terms) — the "proper" fix for our synonym problem | Licence needed. **$0 for non-commercial / non-profit** orgs (academia, public hospitals); commercial fee by company turnover; one subscription per organisation, yearly; **sharing MedDRA with a non-subscriber violates the licence** (search summary of [MSSO rates](https://www.meddra.org/subscription-rates), [fact sheet](https://files.meddra.org/www/Website%20Files/Fact%20Sheets/meddra_factsheet1_accessing_meddra-10%20May%202026.pdf), [data-sharing statement](https://files.meddra.org/www/Website%20Files/Welcome%20Pages/001301%20Statement%20on%20MedDRA%20Data%20Sharing.pdf)) | None | **High for production, not pilot** (D043 already rejected it for licence reasons) |

---

## 2. Comparison table

| Source | Gives us | Access | Licence / cost | PHI | Fit | Main use |
|---|---|---|---|---|---|---|
| ClinicalTrials.gov | Trial AEs vs placebo | API v2, connector | Free (terms not verified) | None | Medium | Second opinion on a signal |
| "ClinHub" (ThoughtSphere) | Sponsor trial-data hub | Commercial | Paid | Trial participant data | Low | None for us |
| DrugBank | Structured label AEs + incidence | Commercial API; academic downloads paused | CC BY-NC (academic) / paid | None | Low (pilot), Medium (prod) | Cross-check AI extraction |
| Orange Book | TE codes, RLD, patents, exclusivity | Monthly ZIP; openFDA endpoint | Free | None | Medium | Pick reference label; group interchangeable generics |
| NIDA (NDEWS, MTF) | Population misuse trends | Briefings; ICPSR public files | Free; restricted needs DUA | Restricted = person-level | Low | Opioid context only |
| Claude connectors (PubMed, CT.gov, openFDA) | Cited lookups in chat | Claude plans; free connectors | Free connectors; Claude plan cost | None if we keep it PHI-free; **not under BAA** | **High** | Pharmacist review packets |
| Palantir Ontology MCP | Claude reads our signals, calls predefined Actions | Developer Console app | Part of Foundry | Data leaves Foundry to the client | Medium-High | Ask Claude about a live signal |
| OnSIDES | Label AEs, 4 regions, quarterly | Download | CC BY 4.0 | None | **High** | "Is it labeled?" second opinion; D015 benchmark |
| FDA DSC + SrLC | FDA-known risks, label change dates | Web / database | Free | None | **High** | Ground truth for "known" |
| FAERS Public Dashboard | Independent count check | Web, Excel export | Free | None | Medium | Sanity check |
| LiverTox / LactMed | Liver injury / lactation | NCBI Bookshelf | Public domain / NLM terms | None | Medium / Low | Specialist checks |
| SIDER 4.1 | Old label AEs | Download | CC BY-NC-SA, 2015 | None | Low | Skip |
| MedDRA | Term hierarchy, SMQs | Subscription | $0 non-profit; paid commercial | None | High (prod) | Replace hand synonyms |

**🔎 One recommendation:** with another month, build the **pharmacist review loop** (section 3) using PubMed + ClinicalTrials.gov connectors, FDA DSC/SrLC and OnSIDES. Add Orange Book only if a day is left. Skip DrugBank, NIDA and "ClinHub" for now.

---

## 3. Pharmacist review loop with another month

### 3.1 Who does what

| Who | Does | Never does |
|---|---|---|
| **Pharmacist reviewer** (licensed; ideally PV or drug-information background) | Decides each item: confirm, change band, reject. Writes a one-line reason. Opens at least one evidence link. | Pastes patient data into any tool |
| **Claude** (in Foundry via AIP, and in Claude chat with connectors) | Drafts a band/label call and builds an **evidence packet**: label quote + DailyMed setid/version/section, FAERS counts, OnSIDES row, DSC/SrLC hit, top PubMed/trial links. Every claim has a link. | Submits a decision. Claude has no write access to the decision object |
| **Foundry** | Holds the review queue, the packets and the decisions. Rebuilds synonym table, gold set and signals from decisions. | Lets anyone edit or delete a past decision |
| **You** | Recruit the pharmacist, run the agreement numbers, present results | — |

### 3.2 Flow

1. **Queue.** Foundry builds a `ReviewItem` object for each thing to review: 258 synonym rows (syn_v2: 69 high / 72 medium / 117 rejected, [A014](../05-approaches/A014-label-faers-synonym-table.md)); the AI extraction items from long label sections (366 of 403 items not yet in the gold set, [A011](../05-approaches/A011-ai-label-extraction-pilot.md)); the top 10 ranked signals per drug (~130).
2. **Packet.** A Foundry transform (cached, like D041) attaches the evidence packet. Claude's draft decision is stored **separately** and hidden for a blind sample (see risks).
3. **Ask.** The pharmacist works in a Workshop review screen. For hard items she opens Claude (Team/Enterprise with the PubMed and ClinicalTrials.gov connectors; optionally Ontology MCP so Claude can read the signal directly). Example: "For semaglutide, is FAERS 'Wheezing' the same idea as the label's 'bronchospasm'? Cite the label section and any PubMed evidence." Claude answers with links; she checks them.
4. **Decide.** She clicks **Submit review** — a **create-only Foundry Action** (same pattern as TriageDecision, [A010](../05-approaches/A010-first-ontology-path.md)). It writes a `ReviewDecision` object:

| Field | Filled by |
|---|---|
| decision_id, reviewer (Foundry user), submitted_at | System (not typed) |
| item_type (synonym / gold_item / signal), item_id | System (from the row clicked) |
| claude_draft, draft_model_version, packet_version | System (copied from the packet) |
| decision (confirm / high / medium / rejected / in_label / not_in_label / worth_action / noise) | Pharmacist |
| evidence_url (required, at least 1) | Pharmacist (picks from packet or pastes) |
| rationale (one line) | Pharmacist |
| blind (was Claude's draft hidden?) | System |
| idempotency key | System (stops double-clicks) |

5. **Rebuild.** Pipelines read the latest decision per item: synonym table **syn_v3 (pharmacist-reviewed)**, gold set **v3 (pharmacist-labelled)**, triage labels on signals. Old versions stay for before/after.
6. **Restrict.** If Ontology MCP is used, the Developer Console app exposes **read** tools only. The Submit Action stays a human click in Workshop. _(inference: this keeps "who decided" unambiguous.)_

### 3.3 Effort (estimates, not measured)

| Task | Owner | Days |
|---|---|---|
| Find and brief a pharmacist (1 page + 30-min walkthrough) | you | 1–5 elapsed (unknown) |
| `ReviewItem` + `ReviewDecision` objects, create-only Action, Workshop review screen | Claude + you | 2 |
| Evidence packet transform (label quote, FAERS, OnSIDES, DSC/SrLC links; PubMed via connector or E-utilities) | Claude | 2 |
| Connector set-up (PubMed, ClinicalTrials.gov) + optional Ontology MCP read-only app | you | 0.5–1 |
| Pharmacist time: 258 synonym rows (~1 min each ≈ 4–5 h) + ~366 gold items (~1–2 min ≈ 6–12 h) + ~130 signals (~3–5 min ≈ 7–11 h) | pharmacist | **≈ 3–4** |
| Rebuild syn_v3, gold v3, recompute metrics, write A0xx + decision | Claude | 1.5 |
| **Total** | | **≈ 7–8 build days + 3–4 pharmacist days** — fits in a month |

### 3.4 What it changes in our metrics

| Metric | Today | After the loop |
|---|---|---|
| **Synonym bands** | Claude only. 69 / 72 / 117. Ranked 1,073, possibly-in-label 108 | Pharmacist bands. New: **Claude–pharmacist agreement** (% and Cohen's kappa — agreement beyond chance) per band. Ranked count and possibly-in-label recomputed on identical data (before/after) |
| **AI extraction (D015, F1 ≥ 0.85)** | F1 ≈ 0.97 on **4 short sections, 35 items, Claude-written gold** — "a pilot, not proof" ([A011](../05-approaches/A011-ai-label-extraction-pilot.md)) | First **pharmacist-labelled F1 per section, including long sections**. That is the number D015 actually asks for. Plus an OnSIDES agreement rate as an outside benchmark |
| **Ranked queue** | No outside check of usefulness | **Precision@10 per drug** (share of each drug's top 10 the pharmacist calls "worth action"), a list of false-positive types, and % of top signals already in an FDA DSC/SrLC ("known") |
| **Trust rule** | Every flag links to its source | Every *review* also links to its evidence and a named reviewer |

---

## 4. Risks & compliance notes (🛡️)

| Risk | Why it matters | Mitigation |
|---|---|---|
| PHI creeps in | A hospital pharmacist may paste a patient case. Anthropic's BAA does **not** cover connectors/MCP ([Anthropic](https://privacy.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers)) | Written rule in the brief to the pharmacist: public data only. Packets contain no free-text case narratives. Use a non-hospital Claude workspace |
| Automation bias (pharmacist just agrees with Claude) | Agreement numbers become meaningless | Hide Claude's draft on a random 30% "blind" sample; compare agreement blind vs shown |
| Hallucinated evidence | A citation may not say what Claude claims | Evidence link required; pharmacist must open it; quotes checked by code as in D041 |
| MedDRA licence | FAERS terms are MedDRA terms; the hierarchy/SMQs need a subscription; sharing with non-subscribers breaks the licence ([MSSO statement](https://files.meddra.org/www/Website%20Files/Welcome%20Pages/001301%20Statement%20on%20MedDRA%20Data%20Sharing.pdf)) | Keep using PT strings only (as now). Ask who would be the subscriber (open question) |
| OnSIDES uses MedDRA matching | OnSIDES data is CC BY 4.0, but its repo does not say whether users need a MedDRA licence ([GitHub](https://github.com/tatonetti-lab/onsides)) | Use as a benchmark; confirm before redistributing |
| Non-commercial licences | DrugBank academic (CC BY-NC) and SIDER (CC BY-NC-SA) likely do not fit a company build _(inference)_ | Do not ingest without a decision |
| Ontology MCP data egress | Palantir warns data becomes available to the outside client ([Palantir](https://palantir.com/docs/foundry/ontology-mcp)) | Our data is public, so low risk; still read-only tools and a scoped app; log it as a decision |
| Unofficial MCP servers | Unknown code, unclear data licences ([glama](https://glama.ai/mcp/servers/nu4jzr0tse)) | Use only Anthropic-directory or Palantir connectors |
| Audit | Reviews must be traceable | Create-only Action, system-filled reviewer and time, no edits/deletes, idempotency key (A010 open item) |
| NIDA restricted data | Person-level, needs a data use agreement | Out of scope |
| Reviewer identity | Naming a pharmacist publicly | Show name in the demo only with consent; store Foundry user ID |

---

## 5. Demo slide: "Another month"

> Today, every synonym band, gold-set label and ranked signal has been checked only by Claude — and we say so. With another month, a licensed pharmacist reviews them in Foundry: Claude prepares a cited evidence packet from the label, PubMed, ClinicalTrials.gov and FDA safety notices, she decides, and a create-only Action records who decided, what, and which evidence. That turns our numbers into real ones: a pharmacist-labelled F1 against the 0.85 target, Claude-vs-pharmacist agreement on synonyms, and precision of the top 10 per drug. No patient data enters the loop, so it works without a HIPAA agreement.

---

## 6. Open questions for you

1. **"clin org"**: is it ClinicalTrials.gov (my best guess), its AACT database copy, or ClinPGx.org?
2. **"clinhub"**: which product did you mean? Where did you hear of it? ThoughtSphere's ClinHUB is the best match, but it is a sponsor trial-data tool.
3. **Who is the pharmacist?** Do they have a Claude Team/Enterprise seat, or would we give them a separate workspace?
4. **Commercial or not?** Is this build counted as commercial work (Soragence)? That decides DrugBank, SIDER and MedDRA licence options.
5. **Ontology MCP:** OK to let Claude read our Foundry signals from outside AIP (public data only, read-only)? It needs a decision entry.
6. Is opioid **misuse context** (NIDA/NDEWS) something the safety officer asked for, or out of scope?
