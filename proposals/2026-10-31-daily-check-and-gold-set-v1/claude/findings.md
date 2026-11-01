# MSSM-30-v1 — Claude's independent answers: findings

**Annotator:** claude · **Pack:** `MSSM-30-v1` (READY `pack_sha256` 2652cbbe…be481) · **Answers frozen:** 2026-10-31T22:21:11Z
**Freeze hash:** `answers.jsonl` sha256 = `d33088a1dce3d6825da82e1e6099a7d53f45c292c510c8c33d6ee6e8a6216965`

**What this is:** a candidate reference set for testing the system. Nobody independent has checked it yet. It is **not** a clinician-approved gold standard, and **not** a 30-item label-extraction benchmark. Only 12 items test label reading. The rest check source lookups and when to abstain. All rows have `human_review_status = pending`. The checks below are my own checks of my own work, not an independent evaluation.

**What I did not look at:** `codex/`, the task README, the patch file, old gold drafts, past model annotations, and `capture_sources.py`. I also made no live lookups, so no freshness or drift check was done (see §6).

---

## 1. Result in one look

| | |
|---|---|
| Cases in `cases.json` / answered | 30 / 30. IDs match exactly, in order, with no duplicates and none invented. |
| Hashes | READY: 45/45 files match. Manifest: 26/26 captured sources match. |
| Resolved / unresolved | 30 / 0 |
| Answers that are deliberately "unknown" | 2 (G23 current recall status, G24 hospital exposure). Both count as resolved, because "unknown" is the correct conclusion from this evidence. |
| Capture failures | 2 FAERS oxycodone-filtered requests failed: HTTP 403 with `API_KEY_MISSING`. No case depends on them for its answer. G19 treats them as a gap, not a zero. |

No row came out unresolved, because every question can be answered from the captured bytes. The two failed FAERS captures were never case sources. The caveats in G14 and G16 stay as stated uncertainty. They don't change the answers.

## 2. Answer table

**Two kinds of check.** *Label interpretation* (G01–G12) means classifying a phrase inside one bounded label passage. *Source lookup* means reading an exact field value. *Cross-source* and *evidence interpretation* rows compare sources or decide what the evidence allows us to conclude.

### 2a. Label interpretation checks (DailyMed, 12)

| ID | Label (SPL set · version · effectiveTime) | Passage | Target | Answer |
|---|---|---|---|---|
| G01 | OxyContin `bfdfe235` · v44 · 20260624 | 5.2 | respiratory depression | reaction_or_warning |
| G02 | OxyContin | 5.13 | opioid-induced esophageal dysfunction | reaction_or_warning |
| G03 | OxyContin | 5.12 | esophageal cancer | underlying_condition_or_risk_factor |
| G04 | OxyContin | 5.9 | nausea | symptom_of_other_condition |
| G05 | OxyContin | 5.12 | don't pre-soak/lick/wet | administration_instruction |
| G06 | OxyContin | 5.7 | opioid-induced hyperalgesia | reaction_or_warning |
| G07 | Fentanyl TDS `e15a7e9b` · v58 · 20260430 | 5.8 | external heat exposure | exposure_factor |
| G08 | Fentanyl TDS | 5.2 | respiratory depression | reaction_or_warning |
| G09 | Fentanyl TDS | 4 | not opioid-tolerant | contraindicated_population |
| G10 | Fentanyl TDS | 5.11 | listed serotonergic drugs | co_medication_risk_factor |
| G11 | Tramadol ER `83367367` · v8 · 20261012 | 5.9 | serotonin syndrome | reaction_or_warning |
| G12 | Tramadol ER | 5.10 | seizures | reaction_or_warning |

How I checked each passage: I re-parsed the original HL7 XML and found exactly one section with that title. Its direct text matched the derived view (ignoring whitespace), and the quote is an exact substring of that passage.

### 2b. Source lookup, cross-source and interpretation checks (18)

| ID | Source | Answer | Check type |
|---|---|---|---|
| G13 | RxNorm `name=oxycodone` | `"7804"` | lookup |
| G14 | RxNorm `name=morphine` | `"7052"` (the term type isn't in the response) | lookup |
| G15 | RxNorm apomorphine vs morphine | `false` (1043 ≠ 7052) | cross-source |
| G16 | RxNorm Percocet 42844 → IN | acetaminophen 161; oxycodone 7804 | lookup |
| G17 | openFDA FAERS meta | `"2026-07-30"` | lookup |
| G18 | FAERS unfiltered, limit=1 | DRUG INEFFECTIVE, 1,299,274 *reports* (all drugs) | lookup |
| G19 | FAERS unfiltered | `false`: no drug filter in the query | interpretation |
| G20 | openFDA FAERS docs | `false`: no causation, no incidence | interpretation |
| G21 | Enforcement D-0338-2026 | blister card seal defects (exact string in JSONL) | lookup |
| G22 | Enforcement D-0338-2026 | `"Ongoing"` (as reported) | lookup |
| G23 | Enforcement + docs | `"unknown"` current active status | interpretation |
| G24 | Enforcement | `"unknown"` hospital exposure | interpretation |
| G25 | Drugs@FDA NDA022272 | `"KNOA PHARMA"` | lookup |
| G26 | Drugs@FDA product 001 | OXYCONTIN · TABLET, EXTENDED RELEASE · ORAL · OXYCODONE HYDROCHLORIDE 10MG | lookup |
| G27 | NDC 59011-410-10 | `100 TABLET, FILM COATED, EXTENDED RELEASE in 1 BOTTLE (59011-410-10)` | lookup |
| G28 | Recall carton vs NDC | `false` (68084-354-01 ≠ 59011-410-10) | cross-source |
| G29 | SrLC OxyContin SUPPL-52 §5.13 | `true` (OIED text is underlined, meaning added or revised) | lookup |
| G30 | CT.gov NCT01162304 EG000 | Extended Release Oxycodone: serious 0 / at risk 18 | lookup |

The full evidence locators, quotes, hashes and retrieval times are in [answers.jsonl](answers.jsonl).

## 3. Source coverage

| Family | Sources used | Cases | Publisher date shown in the source (not our fetch time) |
|---|---|---|---|
| DailyMed SPL | dm_oxy, dm_fentanyl_patch, dm_tramadol | 12 | SPL effectiveTime 20260624 / 20260430 / 20261012 |
| RxNorm | rx_oxycodone, rx_morphine, rx_apomorphine, rx_percocet, rx_percocet_ingredients | 4 | Not in these responses. A separate capture, `rx_version`, says 05-Oct-2026. |
| FAERS (openFDA) | faers_counts_unfiltered, docs_faers | 4 | meta.last_updated 2026-07-30 |
| FDA enforcement | recall_0338, docs_recalls | 4 | meta.last_updated 2026-10-21; report_date 20260218 |
| Drugs@FDA | drugsfda_oxy | 2 | meta.last_updated 2026-10-30 |
| NDC | ndc_oxy, recall_0338 | 2 | meta.last_updated 2026-10-30 |
| SrLC | srlc_oxy_verified | 1 | Entry date 12/22/2025 (SUPPL-52). The page's own update time isn't given. |
| ClinicalTrials.gov | trial_oxy | 1 | lastUpdatePostDate 2015-07-17 (ESTIMATED) |

Every capture time is between 2026-10-31T22:04Z and 22:12Z (from the manifest). That is when the file was fetched, not when it was published.

**Captured but not used by any case:** `srlc_oxy` (DrugNameID=2183). Despite its name, it holds an **OZEMPIC (NDA-209637)** page, not OxyContin. Anyone who relies on that file's name would be misled.

## 4. Context traps (the reason these cases exist)

| Trap | Cases | What a naive system would do |
|---|---|---|
| A disease named inside a warning section | G03 | Flag "esophageal cancer" as an OxyContin reaction |
| A symptom of a different condition | G04 | Flag nausea as a direct reaction, when here it's how adrenal insufficiency shows up |
| An instruction, not an event | G05 | Treat "pre-soak/lick" as a finding |
| One section mixing several classes | G02 (contraindication + risk group + reaction), G12 (seizures as an outcome *and* "history of seizures" as a risk factor) | Give the whole section a single class |
| An exposure vs the instruction to avoid it | G07 | Pick administration_instruction or reaction |
| Co-medication vs the syndrome it causes | G10 vs G11 | Merge the two |
| Look-alike names | G15 | Join apomorphine to morphine |
| A combination product | G16 | Treat Percocet as oxycodone only |
| An all-drug count read as one drug's count | G18, G19 | Call 1.3M "oxycodone drug-ineffective reports" |
| A failed fetch read as zero | G19 | Report "no oxycodone reports" |
| Reported recall status read as current | G22, G23 | Show the recall as "Active" today |
| Same ingredient, different product or package | G28 | Link an IR 5 mg blister recall to OxyContin ER 10 mg bottles |
| String mismatches across FDA sources | G25, G26/G27 | "KNOA PHARMA" vs "Knoa Pharma LLC"; "TABLET, EXTENDED RELEASE" vs "TABLET, FILM COATED, EXTENDED RELEASE" |
| A trial arm read as population risk | G30 | Report "0% serious AE risk" from 0/18 in a terminated open-label trial |

## 5. Limitations

- **Small, chosen sample.** These are 12 passages from 3 opioid labels. That can't support claims about full-label recall or "AI clinical accuracy". It shows only whether specific context traps are handled.
- **Bounded passages only.** Each label answer covers one section of one captured SPL version. A term may mean something different elsewhere in the same label (e.g. nausea in section 6). I didn't check other sections. DailyMed is company-submitted labeling in use, which isn't necessarily the latest FDA-approved wording.
- **FAERS** counts *reports* that match the saved query. They aren't patients, incidence or causation, the pack doesn't deduplicate them independently, and they aren't limited to suspect drugs. A term missing from a top-N list means "unknown", not zero. Successive snapshots must not be added together.
- **The FAERS drug-filtered evidence is missing** (the API key wasn't supplied). Any oxycodone-specific FAERS claim is unanswerable from this pack.
- **Recalls.** The status shown is the status at classification. The pack has no inventory, so exposure is unknown.
- **The NDC listing** isn't FDA approval. Drugs@FDA facts don't automatically match every label or package.
- **SrLC** is a dated regulatory entry with limited coverage. It doesn't mean every label changed on that date.
- **The ClinicalTrials.gov docs** text view is almost empty (176 bytes; the page is script-rendered), so I couldn't confirm the publisher's cadence from the pack.
- **The MedDRA preferred term** "DRUG INEFFECTIVE" appears only as a value from the public openFDA response. No MedDRA files were used. OnSIDES wasn't used.

## 6. Freshness (separate from the answers)

**No live checks were done in this run.** All answers come from the frozen pack. If someone checks the live sources later, they should record any drift in a separate file and leave these frozen answers unchanged. Drift is likely on: FAERS (the next quarterly refresh), enforcement (weekly), NDC and Drugs@FDA (daily or weekdays), and the DailyMed SPL versions.

## 7. Morning workflow (proposed design, **not implemented**)

1. **Check every source's version first.** Read each source's manifest or version signal (SPL setId+version, openFDA `meta.last_updated`, RxNorm `version`, CT.gov `dataTimestamp`, the Drugs@FDA "Data Last Updated" line).
2. **Process only real changes.** If a version or hash hasn't moved, skip the rebuild and record "no change".
3. **Keep the last complete, successful data.** A failed or partial fetch (like the 403s here) never replaces good data, and a failure is never shown as zero.
4. **Show a state for each source:** *changed*, *no change*, *stale vs expected cadence*, or *fetch failed*, with the source's own date and our fetch time shown separately.
5. **Keep unresolved reviews visible** (pending human review, unknown recall status, unknown exposure) until a person closes them.

A daily review doesn't need daily FAERS data. FAERS changes about once a quarter, so on most mornings it should just say "no change, last_updated 2026-07-30".

| Source | Publisher cadence (from captured docs) | Exact release time / time zone | Seen in pack | Our proposed polling (proposal only) |
|---|---|---|---|---|
| FAERS (openFDA) | "Quarterly", with a lag of "3 months or more" | Not published/not verified | last_updated 2026-07-30 | Daily version check; rebuild only when last_updated changes |
| Enforcement (openFDA) | "Weekly" | Not published/not verified | last_updated 2026-10-21 | Daily version check |
| NDC Directory | FDA says the directory "is updated daily" (the openFDA endpoint's cadence isn't in the pack) | Not published/not verified | openFDA last_updated 2026-10-30 | Daily |
| Drugs@FDA | Data file "updated each morning, Monday through Friday" | "Morning" only; no clock time or time zone | Page says last updated October 30th, 2026; openFDA 2026-10-30 | Daily on weekdays |
| DailyMed | Daily, weekly, monthly and other update files are offered | Not published/not verified | Per-SPL effectiveTime (above) | Daily setId/version check for the chosen products |
| RxNorm | Full release on the first Monday of each month; weekly updates on Wednesdays; the API updates after each monthly release | Dates published; clock time not published/not verified | 05-Oct-2026 (next scheduled: Nov 2) | Weekly; plus the day after each monthly release |
| SrLC | Not stated in captured text (only "since January 2016") | Not published/not verified | Entry 12/22/2025 | Weekly (proposal) |
| ClinicalTrials.gov | Not verifiable from the pack (docs view is empty) | Not published/not verified | dataTimestamp 2026-10-30T09:00:04 (no time zone given) | Weekly for the chosen studies |

The polling column is our own proposal. It isn't a publisher schedule, and none of this workflow is built yet.
