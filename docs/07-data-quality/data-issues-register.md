# Data issues register

"Data judgment" is graded: find the problems, fix the ones that matter, be honest about the rest.
Status: 🔍 Suspected (not yet seen in our data) · ✅ Confirmed · 🛠️ Handled · 🏳️ Accepted (documented, not fixed)

| ID | Source | Issue | Why it matters | Plan | Status |
|---|---|---|---|---|---|
| DQ01 | FAERS | Duplicate reports: same case sent in follow-up versions | Inflates counts → false signals | Keep latest version per case ID | 🔍 |
| DQ02 | FAERS | Drug names are free text (brand, misspellings, doses inside the name) | Breaks joins | Normalize → RxNorm (approximate match) → ingredient RxCUI; keep unmatched list | 🔍 |
| DQ03 | FAERS | Reports ≠ incidence; no denominator | "Frequent" is misleading | Disproportionality (PRR/ROR) + careful wording | 🔍 |
| DQ04 | FAERS | Stimulated reporting after news, lawsuits or FDA warnings | Spikes that aren't new risk | Flag spikes near known events (idea P3) | 🔍 |
| DQ05 | FAERS | Primary-suspect vs concomitant drug role | Counting every listed drug blames bystanders | Count primary/secondary suspect only (decision pending) | 🔍 |
| DQ06 | FAERS | Indication terms show up as reactions (e.g. "diabetes" for a GLP-1) | False "unlabeled" signals | Exclude reactions that match the drug's indication | 🔍 |
| DQ07 | Labels | Multiple labels per ingredient (brands, generics, repackagers) | Which label is "the" label? | Pick reference label per ingredient (innovator/RLD); document | 🔍 |
| DQ08 | Labels | Version history; reactions added over time | Needed for "since" and for backtest | Store per (setid, version) | 🔍 |
| DQ09 | Labels | Prose vs MedDRA terms ("GI upset" vs "Nausea") | Matching errors → false unlabeled flags | LLM normalizes to PT + synonym list; measure on gold set | 🔍 |
| DQ10 | Labels | Tables of reaction percentages inside XML | Extraction must handle tables | Test on gold set | 🔍 |
| DQ11 | Recalls | Product named in free text; NDCs inconsistent or missing | Joining recall → drug | Parse NDCs → RxNorm; fallback text match; manual review list | 🔍 |
| DQ12 | Recalls | Compounded products (not FDA-approved) recalled | Do they count for "our" drug? | Show, tagged "compounded" | 🔍 |
| DQ13 | RxNorm | Ingredient vs salt forms (e.g. "liraglutide" vs salt names) | Split identities | Map to base ingredient (IN, not PIN) | 🔍 |
| DQ14 | All | Different update clocks | "Since yesterday" ambiguity | Show freshness per source | 🔍 |
| DQ15 | FAERS | Opioids: abuse, misuse and overdose reports dominate | Swamp clinical signals | Tag abuse/misuse/overdose terms; analyze separately (A001) | ✅ Seen 2026-10-19 (dependence 102k, overdose 55k) |
| DQ16 | All | Opioid combination products (e.g. oxycodone + acetaminophen) | Which ingredient gets the blame? | Map each ingredient via RxNorm; flag combos | 🔍 |
| DQ17 | FAERS | Polydrug reports (benzodiazepines, alcohol) | Confounding | Suspect-role filter (DQ05); note in signal | 🔍 |
| DQ18 | FAERS | "Emotional distress" is a top-5 oxycodone reaction (~50k) — likely litigation-driven reports | Fake 'signals' from lawsuits | Tag reporter type (lawyer/consumer); flag litigation-style terms | ✅ Seen 2026-10-19 |
| DQ19 | Labels | Older labels use "Warnings" (34071-1), newer use "Warnings and Precautions" (43685-7) | Section-based logic misses text | Treat both codes as the warnings section | ✅ Seen 2026-10-19 |
| DQ20 | FAERS | FDA replaced FAERS with **AEMS** on 11 Mar 2026; openFDA FAERS API last updated 2026-07-30 | Source may be frozen or moved; affects ingestion and freshness | Check AEMS public data access before building ingestion | ✅ Confirmed (press) 2026-10-19 |
| DQ21 | FAERS | Lawyers filed most 2021 oxycodone reports: ~58% of reports with a reporter type (35,660 / 61,817, Claude) or ~55% of all reports (40,008 / 72,909, R1; different query/denominator) | Ranking would measure lawsuits | Separate lawyer-reported cases (qualification = 4) | ✅ Seen 2026-10-19 |
| DQ22 | FAERS | "Hyperalgesia" term = 0 reports despite the 2023 opioid label change | Plain term matching misses real signals | Group related terms; find how FDA coded its cases | ✅ Seen 2026-10-19 |
