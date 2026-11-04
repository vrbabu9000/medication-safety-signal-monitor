# Dataset contracts v1 — grain, key, source, refresh

**Date:** 2026-11-04 · **Stage:** Define · Build-order [step 2](foundry-conventions/project-build-order-v1.md) · **Status:** accepted 2026-11-04 (all gate defaults, D039)

**Grain** = what one row means. **Key** = the columns that make a row unique. Every dataset also carries `retrieved_at` (UTC), `source_as_of_date` and a `source_url` or request-params column, so every flag can be traced back to its source.

**Scope** (D031 v4 default = cut list v3): 11 ingredients. The 8 opioids are fentanyl 4337, morphine 7052, hydromorphone 3423, oxycodone 7804, hydrocodone 5489, methadone 6813, buprenorphine 1819 and tramadol 10689. The 3 GLP-1s are semaglutide 1991302, liraglutide 475968 and dulaglutide 1551291. Exenatide 60548 and tirzepatide 2601723 are cut for now (G1).

**First slice:** oxycodone only (reference case T13, OxyContin). Prove each layer for one drug, then widen.

---

## 1. Raw (bronze): source exactly as received, append-only

| Dataset | Grain (one row =) | Key | Source / host | How we get it | Refresh |
|---|---|---|---|---|---|
| `raw_openfda_enforcement` | one recall record as returned, per pull | `recall_number` + `retrieved_at` | openFDA `drug/enforcement.json` (api.fda.gov) ✅ egress | External transform, paged (`limit` 1000 + `skip`), search on the 11 ingredients | Weekly full snapshot (D-R1: no modified date; closures land on old rows) |
| `raw_openfda_drugsfda` | one application record (with its nested products) | `application_number` + `retrieved_at` | openFDA `drug/drugsfda.json` ✅ egress | Same source, search by ingredient | Weekly |
| `raw_openfda_ndc` | one product listing (with packages nested) | `product_ndc` + `retrieved_at` | openFDA `drug/ndc.json` ✅ egress | Same source, search by ingredient | Weekly |
| `raw_dailymed_spl_index` | one SPL (label) version seen in the index | `setid` + `version` | DailyMed `services/v2/spls.json` (dailymed.nlm.nih.gov) ✅ egress | **As built:** search by `drug_name` per ingredient (no Foundry inputs needed); application-number filtering moves to `clean` | Weekly; only new `(setid, version)` pairs fetched (incremental: step 10) |
| `raw_dailymed_spl_xml` | one full label XML document | `setid` + `version` | DailyMed `services/v2/spls/{setid}.xml` ✅ same egress | **As built:** current XML for every indexed label; version read from inside the XML | On new version (D005: LLM runs only then; incremental: step 10) |
| `raw_rxnorm_lookup` | one name or code string looked up once | `lookup_string` + `rxnorm_version` | RxNav REST (rxnav.nlm.nih.gov) ✅ egress | **As built:** exact lookup (`search=0`) of formulary names + salt forms | Monthly, after the RxNorm release |
| `raw_rxnorm_related` _(added 2026-11-04)_ | one concept related to one ingredient (BN, SCD, SBD, MIN …) | `ingredient_rxcui` + `rxcui` + `rxnorm_version` | RxNav `rxcui/{id}/allrelated.json` | One call per ingredient RxCUI found by the lookup | Monthly, after the RxNorm release |
| `raw_faers_quarter_files` | one ASCII file from a quarterly ZIP (DEMO, DRUG, REAC, OUTC, …) | `quarter` + `file_name` | FAERS / AEMS quarterly ZIP (fis.fda.gov/content/Exports/faers_ascii_{q}.zip) ✅ egress, ~63 MB each | **As built:** files dataset (not a table); every ZIP member stored unchanged under `<quarter>/`; parse step in `clean` | Quarterly (D029) |
| `raw_faers_quarter_manifest` _(added 2026-11-04)_ | one file from one quarterly ZIP | `quarter` + `file_name` | same | Same transform: size, sha256 and ZIP timestamp per file | Quarterly |
| `raw_srlc_changes` | one dated safety-labeling change | `application_number` + `change_date` + `section` | SrLC (accessdata.fda.gov) — **parked** (cut v3) | — | — |

**Raw rules:** never change a row once written; store the original payload text (JSON or XML) beside the parsed columns; keep HTTP status and request params as columns; failures become rows with an error status, never a silent gap.

## 2. Clean (silver): checked, typed, deduplicated, one meaning per row

| Dataset | Grain | Key | Built from | Key rule (decision) | Check before publish |
|---|---|---|---|---|---|
| `clean_drug_identity` | one raw string → one ingredient | `lookup_string` | `raw_rxnorm_lookup` | Exact match after splitting `prod_ai` and stripping salts; never substring match (D020) | 0 duplicate keys; match-method counts saved; unmatched strings listed |
| `clean_drug_ingredients` | one formulary ingredient | `ingredient_rxcui` | identity + formulary list | Explicit RxCUI list (D018) | Exactly 11 rows |
| `clean_drug_product_map` | one ingredient ↔ one product | `ingredient_rxcui` + `product_key` | Drugs@FDA + NDC | Many-to-many, so combination products are allowed | **G2**: product key must pass the uniqueness profile |
| `clean_drug_package_map` | one package NDC → one product | `package_ndc11` | NDC | NDC stored as a string; 11-digit normalized form kept next to the printed form | 0 duplicate `package_ndc11`; compounded products get `labeler + product code` (D-R6) |
| `clean_label_versions` | one label version | `setid` + `version` | DailyMed index + XML | DailyMed is label truth (D019) | Every version has its XML; effective date not null |
| `clean_label_product_map` | one label version ↔ one product | `setid` + `version` + `product_key` | label XML `<approval><id>` | One label can list more than one application (Wegovy) | Reference label per product chosen by LD1; generic fallbacks flagged |
| `clean_label_sections` | one section of one label version | `setid` + `version` + `section_code` | label XML | Nested under the 4 parent section codes | Section text not empty; LOINC (section ID) codes from the allowed list |
| `clean_recalls_current` | one recall record, current state | `recall_number` | latest `raw_openfda_enforcement` pull | Upsert: latest pull wins; diff kept for ChangeEvent | 0 duplicate keys; status in {Ongoing, Completed, Terminated} |
| `clean_recall_product_match` | one recall ↔ one product or package | `recall_number` + `match_target` + `match_key` | recalls + NDC + Drugs@FDA | NDC from the record's own text, not `openfda.package_ndc` (D037 learning) | Match method + confidence column; unmatched kept with a reason |
| `clean_faers_cases_current` | one case, latest version | `caseid` | FAERS DEMO, all quarters | Max `caseversion` per `caseid`; deletes applied to full history (D022) | Count parity: incremental vs full rebuild (step 10) |
| `clean_faers_drug_reaction` | one case × ingredient × reaction (PT) | `caseid` + `ingredient_rxcui` + `pt` | DRUG + REAC + identity | Suspect = PS + SS + I, once per case (D021); duplicate fold (D023) | Oxycodone before/after-fold counts saved |

## 3. Curated (gold): object backing datasets

Same objects and keys as [conventions §5](foundry-conventions/conventions-v1.md#5-ontology-contract-grain-and-keys-before-objects): `ontology_drug_drugs` (key `ingredient_rxcui`), `ontology_product_products` (key `product_key`, G2), `ontology_label_labels` (`setid` + `version`), `ontology_recall_recalls` (`recall_number`), `ontology_ae_stats`, `ontology_signal_signals`, plus Action-owned `TriageDecision`. These are built at steps 6–8 and are not changed here.

---

## 4. Gates: things you need to decide

| Gate | Question | Default if you say nothing | Evidence |
|---|---|---|---|
| **G1** Scope | Stay at 11 ingredients, or bring back exenatide and tirzepatide (13) now that time is open? | **Restore to 13** once the oxycodone slice works. Tirzepatide is the biggest GLP-1 by reports (62k) | Volume table; D031 v4 |
| **G2** Product key | Product = application number (D027) or application + product number (strength/form)? | **Application number** for the pilot. FAERS only gives `nda_num`, so a finer key cannot be reached from FAERS. Profile it in Foundry before objects exist | 07-drugsatfda: "Product = application, not strength"; OZEMPIC = 2 applications |
| **G3** Label per product | One reference label per product (LD1), or show all repackager labels? | **One reference label** (owner's label, same route); others are kept, not shown | 128 of 201 applications have >1 label |
| **G4** Uncertain matches | Shown to the officer, or hidden? | **Shown as "uncertain"**, never as "not in label" (conventions §4) | Trust rule |
| **G5** New egress hosts | OK to self-approve `dailymed.nlm.nih.gov`, `rxnav.nlm.nih.gov`, `fis.fda.gov`? (You click; Claude never approves) | Needed for steps 3–4 | A009 pattern |
| **G6** Proposed decisions | D020–D024 (identity, suspect roles, FAERS upsert, duplicate fold, label link) are still "Proposed" | **Accept as written** for the pilot; revisit with evidence | Data walkthrough DQ34–DQ39 |

## 5. Step 3 plan: first real raw pulls (oxycodone slice)

| Order | Dataset | Needs | Proof |
|---|---|---|---|
| 1 | `raw_openfda_enforcement` (oxycodone, all pages) | openFDA key secret (you) | Row count = openFDA `meta.results.total` |
| 2 | `raw_openfda_drugsfda` + `raw_openfda_ndc` (oxycodone) | Same source | OxyContin NDA in the result; package count saved |
| 3 | `raw_dailymed_spl_index` + `raw_dailymed_spl_xml` (OxyContin) | G5 egress for DailyMed | XML stored; version matches the reference set's T13 |
| 4 | `raw_rxnorm_lookup` (strings seen in steps 1–3) | G5 egress for RxNav | oxycodone → 7804 |
| 5 | `raw_faers_quarter_files` (2026 Q1 + Q2) | G5 egress for fis.fda.gov | 2 quarters landed; file sizes match download |

Each pull gets its own transform file in `pipelines_raw_ingest` and a mirror in [foundry/pipelines/raw/](../../foundry/pipelines/raw/).
