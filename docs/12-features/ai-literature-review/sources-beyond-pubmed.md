# F01 — Public sources beyond PubMed (2026-11-05)

**Question:** which free, public sources, *not* among our 8, could feed an "evidence research" review of a signal?
**Our 8** (A008 reference set): RxNorm · NDC Directory · Drugs@FDA · DailyMed · SrLC · FAERS · FDA recalls (enforcement) · ClinicalTrials.gov. The Foundry pipeline uses 6 of them. SrLC and ClinicalTrials.gov are used only in the reference set.
**Builds on:** [another-month research](../../09-roadmap/another-month-sources-and-pharmacist-review.md) (C7). That file already covers OnSIDES, FDA Drug Safety Communications, LiverTox, LactMed, Orange Book, DrugBank, SIDER, MedDRA and the Claude connectors. Its licence notes are not repeated here.

Legend: ✅ live-checked today · 📄 in the C7 research (with links) · ❔ from memory, not verified yet.

## The idea: one review asks 5 questions, each from a different kind of source
| Question about a signal | Best public source | Status |
|---|---|---|
| 1. Is there published evidence? | **Europe PMC** (PubMed + preprints + open-access full text, one free API) | ✅ tirzepatide + allodynia: **64 hits vs 9 in PubMed** (full-text search); preprint filter works (6 for semaglutide + NAION) |
| 2. Is the US regulator already looking at it? | **FDA "Potential Signals of Serious Risks" (quarterly FAERS/AEMS postings)**: FDA's own list of drug–event pairs under evaluation | ✅ page live, last update 2026-09-30 (HTML tables; FAERS is now also called "AEMS") |
| 3. Has a regulator warned or acted? | **FDA Drug Safety Communications** 📄 · **EMA PRAC signal recommendations** (monthly) ❔ | NAION shows why: EMA acted in Jun 2025 before any US label change (DECISIONS learning) |
| 4. Is it on a label anywhere? | **OnSIDES** (label side effects, US/EU/UK/JP, CC BY 4.0) 📄 · **EMA EPAR product information** (EU SmPC) ❔ | ✅ OnSIDES latest release v3.2.1 (2026-07-20) |
| 5. Do other countries' reports show it too? | **Canada Vigilance** (bulk extract) ❔ · **UK MHRA Yellow Card iDAPs** (per-drug PDFs) ❔ · **WHO VigiAccess** (aggregate only; terms limit automated use ❔) | Canada site didn't respond from here; check again |

## Other candidates (lower priority)
| Source | What it adds | Fit | Status |
|---|---|---|---|
| **OFFSIDES** (Tatonetti lab, FAERS-derived signals) | An outside signal list to compare our ranked list against | Medium (benchmark) | ❔ licence |
| **ChEMBL drug warnings** (boxed warnings, withdrawals; Claude connector exists) | "Known serious risk" flag per drug | Medium | ❔ CC BY-SA |
| **Open Targets** (Claude connector) | Includes FAERS-based adverse-event scores per drug | Low (same data as ours) | ❔ |
| **MeSH** (NLM, public domain) | Free term hierarchy. Could help the synonym problem without MedDRA | Medium for A014 | ❔ |
| **Drugs@FDA review documents** (approval-package PDFs) | Was the event seen in the pre-approval trials? | Medium, heavy to parse | ❔ |
| **TGA DAEN** (Australia), **PMDA JADER** (Japan) | More country replication | Low (format/language) | ❔ |
| DrugBank, SIDER, MedDRA, NIDA | See C7: licence or fit problems | Skip for F01 | 📄 |

> **Update after run v2 (same day):** tested on the 6 samples ([results](samples/rerun-v2-multi-source.md)). FDA Potential Signals and OnSIDES added real evidence. Europe PMC added no new on-topic paper. The cost guess below (~$0.11) was too high: the gate shrinks the input, so it stays ≤ ~$0.09.

## Best chances (recommendation)
**Add 3 sources to PubMed, in this order:**
1. **Europe PMC instead of plain PubMed.** Same papers, plus preprints and full text, free, no key. Swap the fetcher; zero new risk.
2. **FDA Potential Signals postings.** One small scrape per quarter. It answers the officer's sharpest question: "is FDA already on this?" It also gives us a free check: how many of our ranked signals FDA lists.
3. **OnSIDES.** One quarterly CSV. It answers "is it labeled in the EU/UK/JP even if not in the US?", which is exactly the NAION case.

Then, if time allows: EMA PRAC recommendations, and Canada Vigilance for replication across countries.

## What "Claude research" looks like here
- **In this repo (now):** a research run per signal fans out to the 5 questions above and writes the one-pager with a citation per line. Same as samples 01–06, with more sources.
- **In Foundry (later):** each source becomes a REST source plus a small transform (the A009 pattern). The AIP review function gets the evidence as input, never browses freely. Every citation is checked by code (the A011 pattern). This keeps it auditable and cheap.
- Cost stays small. All 5 sources are free. The model input grows from ~6.5k to roughly ~10k tokens, so a review is about **$0.11 instead of $0.09** on Opus 5.5 (estimate).

## Next check (Researcher, read-only)
Verify the ❔ rows: EMA PRAC format and terms, Canada Vigilance licence and format, VigiAccess terms, OFFSIDES licence, MeSH fit.
