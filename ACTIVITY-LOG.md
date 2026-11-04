# 📒 Activity log — read this first when you come back

## ⏩ Pick up here (always current)
| | |
|---|---|
| **Last session** | 2026-11-04 — Step 5 clean baseline built in Foundry: FAERS, labels, recalls; 0 duplicate keys; FAERS counts equal the prototype (Compass v17) |
| **Where we are** | Phase 2, build-order steps 1–5 done. Raw: 10 datasets. Clean (`Data/clean`): identity 5 datasets + FAERS cases 792,346 · case reactions 2,554,017 · oxycodone drug×reaction 75,006 (3,408 cases after fold) · label versions 263 · label sections 1,160 · recalls 25 (4 active) · recall match 58. Action save not tested yet. [foundry/README](foundry/README.md) · [contracts](docs/04-architecture/dataset-contracts-v1.md) |
| **Next 3 actions** | 1. (Claude) Step 6: Ontology object types Drug, Product, Label, Recall from the clean datasets · 2. (Claude + you) Step 6: create a test Action and prove the write-back saves · 3. (Claude) Wire `OpenFdaApiKey` before widening (step 9) |
| **Waiting on** | Pharmacist reviewer for the reference set · tell boss the demo date is open |
| **Say this to Claude to restart** | _"Read ACTIVITY-LOG and COMPASS, connect Chrome, open Foundry, and continue at build-order step 6 (first Ontology path + Action save)."_ (Cloud: on hold, see [guide](docs/10-delivery/cloud-session-guide.md).) |

---

## Log (newest first)

### 2026-11-04 (late night) — Step 5: clean baseline (Compass v17)
- **Built** in `Pipelines/pipelines_clean` (polars lightweight), three new mirrors: [clean_faers.py](foundry/pipelines/clean/clean_faers.py), [clean_labels.py](foundry/pipelines/clean/clean_labels.py), [clean_recalls.py](foundry/pipelines/clean/clean_recalls.py).
- **FAERS (Foundry = local = Oct 20 prototype):** `clean_faers_cases_current` 792,346 cases (D022: upsert by caseid, max caseversion, then each quarter's deletes) · `clean_faers_case_reactions` 2,554,017 case × reaction rows (background for PRR in step 8; **new dataset, contract addition**) · `clean_faers_drug_reaction` 75,006 oxycodone rows. Oxycodone suspect cases 4,464 → **3,408 after the D023 fold** (1,530 cases suppressed in 7 clusters across all drugs). Roles: SS 2,459 · PS 1,511 · PS+SS 451 · I 43 (D021). Built with Foundry's default memory; ~12 s and 2.9 GB peak locally.
- **Labels:** `clean_label_versions` 263 (all have XML and an effective date; 109 modern PLR format) · `clean_label_sections` 1,160 safety sections (Boxed Warning, Contraindications, Warnings and Precautions, Warnings, Precautions, Adverse Reactions; the D037 list), sub-sections folded into the parent text, 0 empty. OxyContin v44 has its 4 PLR sections.
- **Recalls:** `clean_recalls_current` 25 (4 Ongoing, 21 Terminated) · `clean_recall_product_match` 58 rows: every recall gets an ingredient row; 11 package matches with high confidence; **all 4 active recalls match a listed package**; 20 NDCs no longer in the NDC directory kept with a reason (G4).
- **Checks in Foundry SQL:** 0 duplicate keys in all 7 datasets; all counts equal the local run.
- **Problem met again:** the VS Code auto-sync rejected one commit; "Update" kept the file this time (it had been auto-committed). Committed each file right after pasting.
- **Tools:** local harness reads files datasets (`filesystem().ls()/open()`); `out/raw_faers_quarter_files` is a link to `prototypes/data/_faers_bulk`. Snapshot [Compass v16](docs/00-compass/history/COMPASS-v16.md).

### 2026-11-04 (night) — Step 4: shared drug identity (Compass v16)
- **Built:** new Foundry repo `Pipelines/pipelines_clean` (polars lightweight transforms; no external sources). Mirrors: [clean_drug_identity.py](foundry/pipelines/clean/clean_drug_identity.py), [clean_label_product_map.py](foundry/pipelines/clean/clean_label_product_map.py), [README](foundry/pipelines/clean/README.md).
- **Results (Foundry = local):** `clean_drug_ingredients` 13 (D018; oxycodone `in_slice`) · `clean_drug_identity` 8 strings: OXYCODONE → 7804 `exact_in`, OXYCODONE HYDROCHLORIDE / TEREPHTHALATE → 7804 `exact_pin`, 5 combination partners (acetaminophen, aspirin, ibuprofen, naloxone, naltrexone) kept as `no_formulary_match` · `clean_drug_product_map` 141 applications (127 ANDA, 14 NDA; 83 combination; 51 marketed) · `clean_drug_package_map` 937 packages (895 by application, 42 bulk/unapproved by `labeler:` key; all 11-digit normalised) · `clean_label_product_map` 269 rows (265 matched, 3 application not in the Drugs@FDA pull, 1 label with no approval id; 35 owner labels = 15 exact + 20 first-word name matches).
- **Checks in Foundry SQL:** 0 duplicate keys in all 5 datasets; OxyContin chain 7804 → NDA022272 (KNOA PHARMA) → 59011-410-10 (`59011041010`) → label `bfdfe235…` v44 reference = **1 row** (reference trace T13).
- **Found:** only 71 of 141 oxycodone applications have any DailyMed label (most others discontinued ANDAs); 34 have the owner's (reference) label. Products with no owner label are flagged `product_has_owner_label = false`, not guessed (G4).
- **Problem met:** the VS Code workspace (opened automatically when the repo was created) kept auto-committing "Sync remote branch". One commit was rejected, and "Update then build" then dropped an uncommitted file; re-added and committed. Lesson logged.
- **Tools:** local harness now warns about all-null columns; new [check_identity.py](foundry/tools/local_run/check_identity.py). Snapshot [Compass v15](docs/00-compass/history/COMPASS-v15.md).

### 2026-11-04 (evening) — Repo made cloud-ready
- **Why:** you'll continue from a cloud session linked to GitHub, which has no access to Foundry, this laptop, or chat memory.
- **Updated:** [README](README.md) (status, requirements, 12-step plan with progress, Foundry map) · [foundry/README](foundry/README.md) (every source/repo/dataset with RID and counts, how a change reaches Foundry, gotchas) · new [pipelines/raw/README](foundry/pipelines/raw/README.md) · new local test harness [foundry/tools/local_run](foundry/tools/local_run/README.md) (reproduces the Foundry counts 2/271/25/141/313) · new [cloud session guide](docs/10-delivery/cloud-session-guide.md) with the step 4 prompt.
- **Cloud on hold (your call):** cloud sessions can't drive the browser/Foundry, which was the main reason for using them. Work continues locally with Claude in Chrome. The guide stays for later; git option (guide §2) not chosen. Pharmacist review packet discussed, not built (plan: after step 7, ~45–60 min ask).

### 2026-11-04 (later) — Contracts accepted, first real raw pull (Compass v14)
- **Step 2:** [dataset contracts v1](docs/04-architecture/dataset-contracts-v1.md) written and accepted with all gate defaults (D039; D020–D024 now Accepted).
- **Step 3, pull 1:** `Data/raw/raw_openfda_enforcement` built from [raw_openfda_enforcement.py](foundry/pipelines/raw/raw_openfda_enforcement.py): 25 oxycodone recalls, 15 columns, `result_total` 25, source updated 2026-10-28. Matches the 25 in the [volume profile](docs/07-data-quality/source-profiles/06-data-volume-13-ingredients.md).
- **Bug caught:** the first build gave 11 rows. Without parentheses, openFDA silently dropped the first OR term. Fixed and rebuilt (learning logged).
- **Step 3, pull 2:** [raw_openfda_products.py](foundry/pipelines/raw/raw_openfda_products.py) builds `raw_openfda_drugsfda` (141 applications) and `raw_openfda_ndc` (313 products), both equal to openFDA totals. OxyContin NDA022272 (sponsor KNOA PHARMA) present, with 8 linked NDC products. Drugs@FDA needed `products.active_ingredients.name`: `openfda.generic_name` alone finds 47 of 141.
- **Step 3, pull 3:** new source `src_dailymed_api` (dailymed.nlm.nih.gov, egress approved by you, code import on, exports off). [raw_dailymed_spl.py](foundry/pipelines/raw/raw_dailymed_spl.py) writes `raw_dailymed_spl_index` (263 oxycodone labels = DailyMed total) and `raw_dailymed_spl_xml` (263 XML, 14.2 MB, 0 errors, 0 version mismatches). OxyContin `bfdfe235…` v44, effective 20260624, matches reference trace T13.
- **Step 3, pull 4:** new source `src_rxnav_api` (rxnav.nlm.nih.gov, egress approved by you, code import on, exports off). [raw_rxnorm.py](foundry/pipelines/raw/raw_rxnorm.py) writes `raw_rxnorm_lookup` (oxycodone → 7804; oxycodone hydrochloride → 82063, the salt, showing why D020 strips salts) and `raw_rxnorm_related` (271 concepts: BN 10, SCD 56, SBD 37, MIN 5 …), RxNorm 02-Nov-2026. Tested locally with stand-ins for the Foundry library before building. Contracts updated with the as-built search methods and the new `raw_rxnorm_related`.
- **Step 3, pull 5:** new source `src_faers_files` (fis.fda.gov, egress approved by you, code import on, exports off). [raw_faers_quarters.py](foundry/pipelines/raw/raw_faers_quarters.py) stores every file of the 2026 Q1 and Q2 ZIPs unchanged in `raw_faers_quarter_files` (files dataset), plus `raw_faers_quarter_manifest`: Q1 19 files / 352,984,542 bytes, Q2 18 files / 337,724,653 bytes, 0 errors. ZIP sizes and the DRUG26Q1 sha256 equal the copies downloaded on 2026-10-20. Tested locally on those ZIPs first. **Step 3 complete; snapshot [Compass v14](docs/00-compass/history/COMPASS-v14.md) → v15.**
- **Also:** you added secret `OpenFdaApiKey` (not yet used in code). Secret names must be alphanumeric, so the key secret is `OpenFdaApiKey`. Code is now pasted into the Foundry editor (auto-indent mangled typed code).

### 2026-11-04 — Foundry access proven, first dataset built (Compass v13)
- **How:** you logged in to Foundry in Chrome; Claude worked through Claude in Chrome. You did the security clicks yourself (egress approval, code-import toggle).
- **Built in Foundry:** 9 top-level folders + subfolders (`Data/raw|clean|curated|quarantine`, `Ontology/Objects|Links|Actions`, `AIP/Logic|Evals`) · `AIP/Logic/scratch_aip_access_test` · source `Data/raw/src_openfda_api` · Code Repository `Pipelines/pipelines_raw_ingest` · dataset `Data/raw/raw_openfda_enforcement_access_test` (1 row, HTTP 200, recall D-0338-2026, oxycodone 5 mg, Class II, Ongoing).
- **Proven:** AIP model replies (GPT-5.6 Sol, "AIP OK" in 2.9 s); openFDA reachable from a Foundry build. **Not proven:** Action save.
- **Decided:** D031 v4 (no fixed demo date; cut list v3 stays default scope) · D038 (openFDA via REST API source + external transform). Approach [A009](docs/05-approaches/A009-openfda-rest-ingestion.md). 4 learnings. Record: [access results](docs/10-delivery/2026-11-04-foundry-access-results.md). Code mirror: [raw_openfda_enforcement_access_test.py](foundry/pipelines/raw/raw_openfda_enforcement_access_test.py). Snapshot: [Compass v12](docs/00-compass/history/COMPASS-v12.md).
- **Not done:** openFDA key secret; `request_url` loses the query string (store params in their own column next time); BACKLOG hours not re-estimated; Delivery Lead not run.

### 2026-11-02 — Reference set v2: 30 cross-source drug traces (Compass v12)
- **Why:** the v1 30-case pack wasn't defensible. Codex wrote the questions and its own answers in one pass, the FAERS oxycodone capture failed, and one SrLC file was really Ozempic.
- **Built:** [proposals/2026-11-02-gold-set-v2/](proposals/2026-11-02-gold-set-v2/). 62 drugs screened → 35 eligible → 30 traced through RxNorm, NDC, Drugs@FDA, DailyMed, SrLC, FAERS, enforcement and ClinicalTrials.gov (240 answers). Questions frozen before answers; identity guard on every capture; independent verifier (3,403/3,403 checks pass); live re-check (530/530 identical, 30/30 answers unchanged); 30 [case cards](proposals/2026-11-02-gold-set-v2/cards/); diagram [20-gold-trace-v1](docs/diagrams/png/20-gold-trace-v1.png).
- **Found:** the v1 403 was openFDA requiring a key for count queries with `limit>100`. The key now lives in your shell profile and is redacted in saved URLs. Other findings: FAERS substance queries mix products (Chantix vs Tyrvaya); the recall `openfda.package_ndc` list is application-wide; Lyrica's DailyMed label (effective 2020) lags a 2025 SrLC change.
- **Decided (proposed):** D037 plus the dataset's "label mentions" rule; 4 learnings. Approach [A008](docs/05-approaches/A008-gold-set-v2-cross-source-traces.md). v1 superseded. Snapshot: [Compass v11](docs/00-compass/history/COMPASS-v11.md).
- **Not done:** pharmacist review of S4 calls and S6 synonyms; BACKLOG hours not updated; Delivery Lead not run.

### 2026-10-31 — Foundry conventions and project learning/build roadmap (Compass v11)
- **Research:** inspected Data Forge's 11-video introductory playlist; read auto-generated transcripts for episodes 3 (folders), 6 (medallion pipeline), and 9 (Ontology Manager); cross-checked official Palantir docs. Other video content is not claimed reviewed.
- **Created:** [reference entry point](docs/04-architecture/foundry-conventions/README.md), [conventions](docs/04-architecture/foundry-conventions/conventions-v1.md), [12-step build order](docs/04-architecture/foundry-conventions/project-build-order-v1.md), [source/timestamp notes](docs/04-architecture/foundry-conventions/tutorial-research-2026-10-31.md), [A007](docs/05-approaches/A007-foundry-medallion-conventions.md), medallion and ontology diagrams (Mermaid, PNG/PDF, editable draw.io).
- **Decided:** D036 — keep the existing local raw/clean/ontology layout; explain bronze/silver/gold responsibilities; use explicit naming and grain/key contracts and a dependency roadmap. This is a documentation standard, not approval of proposed clinical/source/scope decisions.
- **Status:** no Foundry build performed; no speed/cost result claimed. Oct 27 capacity estimate marked historical. Parked A006 / D032–D035 are not adopted. Snapshot: [Compass v10](docs/00-compass/history/COMPASS-v10.md).

### 2026-10-27 — Restart after a lost week (Compass v10)
- **Status:** no work Oct 21–26. Exploration was finished early, so the thinking is intact; the Foundry build has not started.
- **Decided (proposed):** D031 v3. Demo Wed Nov 4 (Nov 3 = Election Day); build Oct 29–Nov 2; all 6 cuts applied now; decision review 5→1 h; load ~76%.
- **Files:** [game plan v1](docs/10-delivery/game-plan-v1-oct27-to-nov4.md) · [BACKLOG](docs/10-delivery/BACKLOG.md) re-dated · [COMPASS v9 snapshot](docs/00-compass/history/COMPASS-v09.md).

### 2026-10-20 (night) — Plan to the demo, tracker live (Compass v8)
- **Answered:** source choices, merge design, "FAERS is the spine?", what "since yesterday" means, daily FAERS. Plan: `~/.claude/plans/i-need-help-in-valiant-quasar.md` (approved).
- **Decided:** +Drugs@FDA, NDC Directory, SrLC as bridges; OnSIDES = Part B benchmark (D026). Two-level identity (D027, supersedes D003). "Since last review" + ChangeEvent + per-source as-of (D028). FAERS quarterly in pilot; daily only via an official API (D029). Demo ~Nov 3, freezes Oct 23/24, cut list (D031).
- **Tracking:** ⏱️ [Delivery Lead](.claude/agents/delivery-lead.md) agent · [BACKLOG](docs/10-delivery/BACKLOG.md) (load 55 h / ~50 h = 110% Amber) · decisions versioned with "Decision changes" + "Learnings" tables (D030) · COMPASS versioned, [history](docs/00-compass/history/) · CLAUDE.md §2c.
- **New approach:** [A005](docs/05-approaches/A005-source-selection-and-merge.md). 4 atlas sessions proposed (cards in the app).

### 2026-10-20 (evening) — Real bulk FAERS walked through every stage
- Downloaded FAERS bulk 2026 Q1+Q2 (63 MB each, git-ignored in `prototypes/data/_faers_bulk/`). Prototype of the whole FAERS pipeline: [faers_bulk_walkthrough.py](prototypes/explore/faers_bulk_walkthrough.py) (36 s, plain Python).
- **Walkthrough page:** [data-walkthrough-v1.html](docs/04-architecture/data-walkthrough-v1.html) (also published as a private artifact). Supersedes the v1 explainer.
- **Found:** bulk has no openfda (link via `nda_num`); substring matching +50% false morphine rows; append vs upsert +8.7%; one Canadian patient filed 700× (oxycodone −24% after fold); reporter field blank 35% → 72% at the AEMS switch; NAION PRR 112, not on tablet or injection label. DQ34–DQ41, D020–D025 proposed.

### 2026-10-20 (later) — FAERS and Part B explained with one real drug
- **Explainer:** [faers-and-part-b-explained-v1.md](docs/04-architecture/faers-and-part-b-explained-v1.md): the project as two lists (FAERS counts vs LLM label list), one real report walked row by row, keep/drop table for FAERS fields, ontology objects with examples.
- **Diagram:** [16-faers-to-signal-v1.png](docs/diagrams/png/16-faers-to-signal-v1.png). **Approach:** [A004](docs/05-approaches/A004-faers-to-ontology-mapping.md). **New issue:** DQ33 (semaglutide FAERS linked to the tablets label, not the injection label).
- Found 3 label traps that break plain text search ("blurred vision", "gastroparesis", spelling).

### 2026-10-20 — Class locked, sources profiled, merges shown
- **Class accepted:** 8 opioids + 5 GLP-1 ([A003](docs/05-approaches/A003-class-choice-hybrid.md), D014). Focus rule: rank clinical side effects + recalls; tag lawyer/abuse/product-error/pregnancy (D016).
- **Structure reports** for every source: [01 FAERS](docs/07-data-quality/source-profiles/01-faers.md) · [02 DailyMed](docs/07-data-quality/source-profiles/02-dailymed.md) · [03 Recalls](docs/07-data-quality/source-profiles/03-enforcement.md) · [04 RxNorm](docs/07-data-quality/source-profiles/04-rxnorm.md) · [05 Trials](docs/07-data-quality/source-profiles/05-clinicaltrials.md).
- **Volumes** for 13 drugs: [06-data-volume](docs/07-data-quality/source-profiles/06-data-volume-13-ingredients.md) (1.46M FAERS reports, 116 ongoing recalls, 1,324 labels).
- **Worked merges:** [merge-walkthrough-v1](docs/04-architecture/merge-walkthrough-v1.md) (fentanyl recall; semaglutide NAION signal).
- **Diagrams moved out of .md into PNG + PDF** (D017): [docs/diagrams](docs/diagrams/diagram-book.pdf), render with `bash tools/render_diagrams.sh`.
- New scripts: [pull_all.py](prototypes/explore/pull_all.py), [volume_check.py](prototypes/explore/volume_check.py), [describe_structure.py](prototypes/explore/describe_structure.py). New data issues DQ23–DQ32. Decisions D016–D019.

### 2026-10-19 — Sources mapped, research done
- **Source access guide** (browse / API / bulk for every source, all links tested live): [00-source-access-guide.md](docs/07-data-quality/source-profiles/00-source-access-guide.md). Sampler script [pull_samples.py](prototypes/explore/pull_samples.py) ran OK for oxycodone. Profile files 01–05 created with checklists.
- **3 parallel research agents** → [research synthesis](docs/01-discovery/research/README.md): [R1 class](docs/01-discovery/research/R1-therapeutic-class.md) · [R2 industry need](docs/01-discovery/research/R2-industry-need.md) · [R3 prior art](docs/01-discovery/research/R3-prior-art.md). 140 sources retained.
- **Proposed:** opioid-led hybrid class ([A003](docs/05-approaches/A003-class-choice-hybrid.md), D014); AI target F1 ≥ 0.85 (D015).
- **Found:** FDA replaced FAERS with AEMS (Mar 2026) (DQ20); ~58% of 2021 oxycodone reports from lawyers (DQ21); "hyperalgesia" has 0 FAERS reports (DQ22). New approach A002 (source profiling).
- You set up the Palantir Developer Tier and are learning the tools.

### 2026-10-14 — Git ground rule set
- **Rule:** Claude never commits or pushes. It gives commit messages and commands; you run them ([CLAUDE.md §0](CLAUDE.md)). Enforced by deny rules in [.claude/settings.json](.claude/settings.json) (tested: blocked).
- **GitHub account: vrbabu9000 only.** Use SSH alias `github.com-personal`. Repo-local identity `vrbabu9000 <vrb.canada@gmail.com>`. Your global git identity is vrajesh9000, so the local override is required.
- Decision D013 logged.

### 2026-10-13 — Boss meeting done, scope reset
- **Meeting outcomes** logged in [the meeting file](docs/03-meetings/2026-10-13-boss-kickoff-questions.md#-meeting-summary--held-2026-10-13).
- **Purpose clarified:** exploratory showcase of thinking, design and usefulness → the reasoning trail is half the deliverable.
- **Class changed:** GLP-1 → opioids ([A001](docs/05-approaches/A001-pilot-scope.md), D002 superseded by D007).
- **Monitoring promoted** to must-have; drift judged over 3–4 weeks (D008, D009).
- **Foundry:** use the free Developer Tier (D010).
- **New files:** [A001 pilot scope](docs/05-approaches/A001-pilot-scope.md) · [source profiling plan](docs/07-data-quality/source-profiles/README.md) · [ideas parking lot](docs/09-roadmap/ideas-parking-lot.md) (health "OS" idea).

### 2026-10-13 — Pre-meeting prep
- Added [therapeutic class options](docs/01-discovery/therapeutic-class-options.md) and the "own Developer Tier?" question (M3a).

### 2026-10-13 — Project created
- Repo set up: [COMPASS](COMPASS.md), [CLAUDE.md](CLAUDE.md) response rules, 8 personas, brief summary, requirements deep-dive, design-thinking canvas, architecture v0 (+ draw.io), data-issues register, approach/decision/optimization templates, pilot→production roadmap, [boss questions](docs/03-meetings/2026-10-13-boss-kickoff-questions.md).
