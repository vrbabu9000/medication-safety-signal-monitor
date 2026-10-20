# Boss meeting — 2026-10-13 · Kickoff questions

**Goal of the meeting:** leave with answers to the 🔴 questions, so we can lock the pilot scope this week.
**Time needed:** ~30 min. If you only get 10 minutes, ask 🔴 M1–M6 only.

## How this sheet works
| Tier | Meaning | What you do |
|---|---|---|
| 🔴 **Must ask** | We can't start, or would build the wrong thing, without the answer | Ask every one |
| 🟡 **Should ask** | Changes the design, but we have a sensible default | Ask if time allows. Otherwise use our default |
| 🟢 **We'll decide** | Brief says "decide and write it down". Don't ask. **State it and ask for a veto.** | Read the list out; note any pushback |

> 💡 The brief says *"what you ask tells us something."* Asking things the brief already answers looks weak.
> Asking about definitions, trust and scale looks strong. Every question below is one the brief does **not** answer.

---

## 🎤 60-second opener (say this first)
> "I've read the brief. Here's what I think we're building: one morning screen for a pharmacy safety officer that answers three questions:
> unlabeled side effects, active recalls, and what changed. Every flag links to its source. I'm planning to go narrow and deep:
> one drug class, end to end, with measured AI accuracy. Before I lock scope I need a few answers from you,
> and I'll tell you the defaults I'm assuming so you can veto them."

---

## 🔴 Must ask (blocking)

| # | Question | Why it matters | Our default if no answer | Answer |
|---|---|---|---|---|
| M1 | **What is this for?** An evaluation, a client pitch, an internal accelerator, or a real customer pilot? **Who sits in the demo?** | Decides polish vs depth, and whether "production scale" is in scope or only on paper | Treat as evaluation + pitch-ready pilot. Production path documented, not built | |
| M2 | **Dates:** kickoff date, demo date, and how many hours a week is "part-time"? | The 3-week clock starts at kickoff. We need a real plan | Kickoff this week, ~15 hrs/week | |
| M3a | **Is it OK if I start in my own free Foundry Developer Tier** to learn and prototype before kickoff, using public data only? (Final build moves to your environment) | Lets work start now. Personal-tier work does not transfer automatically, so he should know | Yes, prototype only. Code kept portable in git | |
| M3 | **Foundry access:** when, which environment, and which tools can I use? (Code Repositories, Pipeline Builder, Ontology Manager, Workshop, AIP Logic, Actions) Can I create object types and write-back Actions myself? | Without ontology + Actions rights we can't build Parts A and C | Need full builder rights in a sandbox project | |
| M4 | **Can Foundry call the internet?** (openFDA, RxNav, DailyMed APIs) Or must I upload bulk files? | Decides the whole ingestion design and how "incremental" works | Bulk files uploaded on a schedule + API calls if allowed | |
| M5 | **AIP models and budget:** which LLMs are available, and is there a token or compute limit? | LLM cost is a named optimization target. Model choice affects accuracy | Use the best available model on new/changed labels only | |
| M6 | **Scope / impact:** "Where do you want the impact to show: patient harm inside the hospital, a story people already care about, or proof the AI works?" Any class a client cares about? | Everything downstream depends on it. His answer maps to a class → [therapeutic-class-options.md](../01-discovery/therapeutic-class-options.md) | **GLP-1 agonists** (see 🟢 G1). Hospital harm → anticoagulants | |
| M7 | **What counts as "on the label"?** Only the *Adverse Reactions* section, or also *Boxed Warning*, *Warnings & Precautions*, *Contraindications*? | This defines what "unlabeled" means. Get it wrong and every flag is wrong | Any of those 4 sections counts as "labeled" | |
| M8 | **Is there a real health system behind this?** If yes, can I talk to a real pharmacy safety officer for 30 min? | Design thinking starts with empathy. A real user interview is the strongest demo story | Use a persona built from public sources | |
| M9 | **Who can review clinical accuracy?** I need someone with pharmacy/clinical knowledge to check ~30 hand-labeled label extractions (the "gold set") | AI reliability is graded. A gold set I labeled alone is weaker | I label it, with a documented guideline | |
| M10 | **What does "wow" look like for you?** Beyond the rubric, what would make you say this is excellent? | Tells you where to over-invest | Depth on AI reliability + traceability | |

## 🟡 Should ask (shapes the design)

| # | Question | Why it matters | Our default | Answer |
|---|---|---|---|---|
| S1 | **MedDRA license:** do we (or the client) have one? FAERS codes reactions in MedDRA, a licensed medical dictionary. Its full hierarchy needs a license | Without it we can't group "nausea" and "vomiting" under one parent term. Affects matching quality | Use the MedDRA Preferred Term (PT) strings that FAERS already contains, plus LLM-assisted matching. Note it as a limitation | |
| S2 | **"Active recall":** only status = *Ongoing*? All classes (I, II, III)? Include drug shortages? | Defines Question 2 | Ongoing, all classes, Class I highlighted. No shortages | |
| S3 | **"Since yesterday":** FAERS data updates only **quarterly**. Recalls update weekly, labels daily. Is it OK if daily changes come mainly from recalls, label updates and triage actions? | Sets honest expectations about the 3rd question | Yes. Show "last refreshed" per source in the app | |
| S4 | **Triage workflow:** what states should a signal move through, and who else is involved (P&T committee, medication safety committee)? Notifications needed? | Defines the write-back Action and Signal object | New → Under review → Escalated / Dismissed / Monitoring, with a required note | |
| S5 | **Drug level:** track by ingredient ("semaglutide") or by product (Ozempic vs Wegovy vs compounded)? | "Resolve drug identity once" is graded | Ingredient level (RxNorm IN), with products underneath | |
| S6 | **Signal method:** is a standard statistical method expected (PRR/ROR, the methods FDA and EMA use), or are simple count thresholds fine? | Credibility with a clinical audience | PRR with Evans criteria (N≥3, PRR≥2, χ²≥4) | |
| S7 | **Unstructured source:** is DailyMed SPL XML (label text in tagged sections) acceptable, or do you want PDF parsing too? Can I use openFDA's pre-parsed label API? | The pre-parsed API makes the AI step easier but may look like a shortcut | SPL XML from DailyMed, so we keep version history | |
| S8 | **Backtesting OK?** Can I show signals my system would have caught *before* FDA added them to the label? | The strongest proof of value (see idea P1) | Yes, using DailyMed label history | |
| S9 | **Check-ins:** weekly sync with you? Do questions go to you or to Soragence (Etter Hoang)? | Keeps the loop tight | Weekly 30-min sync | |
| S10 | **Code and IP:** can the code also live in my Git repo? Can I reuse it after? | Portfolio and future reuse | Ask first, assume Foundry-only | |

## 🟢 We'll decide — state these, ask for a veto

| # | Our decision | One-line reason |
|---|---|---|
| G1 | **Pilot class: GLP-1 receptor agonists** (semaglutide, tirzepatide, liraglutide, dulaglutide, exenatide, lixisenatide). Backup: anticoagulants | Heavy reporting volume, recent label changes (good for backtest), compounded-product recalls, and inpatient relevance (aspiration risk around anesthesia). *To verify with a quick data pull* |
| G2 | **Drug identity resolved once**, in one clean step, keyed on RxNorm ingredient ID (RxCUI). Every other dataset joins to it | It's an explicit grading point |
| G3 | **FAERS from quarterly bulk files**, deduplicated (keep latest version of each case). This is our **incremental** pipeline: append one quarter at a time | Bulk files allow dedup; the API gives counts only |
| G4 | **LLM runs only on new or changed label versions** (keyed by label set ID + version), and results are cached | Main LLM cost lever; "don't re-run needlessly" is graded |
| G5 | **Every Signal stores its evidence trail:** FAERS counts and quarter, label version, exact passage, model + prompt version | "Every flag traces to source" |
| G6 | **App wording says "disproportionate reporting", not "causes"** | FAERS shows reports, not proof. Clinicians will check this |
| G7 | **Gold set:** ~30 label sections hand-labeled; hallucination check = "is each extracted reaction actually in the source text?" | Lets us say how often the AI is wrong, with numbers |
| G8 | **Cut order if late:** monitoring (D) → ClinicalTrials.gov → extra polish. Never cut traceability or the gold set | "Cut breadth before depth" |

---

## 💡 Perspectives and ideas to pitch (shows you're thinking ahead)

| # | Idea | Why it impresses |
|---|---|---|
| P1 | **Backtest:** "Would we have caught it?" Replay older FAERS quarters against older label versions and see if we flagged reactions FDA later added | Turns "it works" into a measured claim |
| P2 | **Usage weighting:** rank signals by how widely the drug is used (Medicare Part D) | Officer sees what affects the most patients first |
| P3 | **Bias flags:** mark signals that spiked right after news or an FDA warning (stimulated reporting) | Shows PV maturity. Builds trust |
| P4 | **Morning digest:** a "what changed" panel driven by daily snapshots of signal state | Answers Q3 directly |
| P5 | **Second opinion:** ClinicalTrials.gov side effects shown next to FAERS for the same reaction | Corroboration raises confidence |
| P6 | **Pilot → production path:** multi-hospital formularies (upload your own list), alerting, MedDRA license, validation, SLAs. Documented, not built | Shows scale thinking without scope creep |

## ❌ Don't ask (the brief already answers these)
Which data sources to use · what to hand in · whether AI coding tools are allowed (yes) · whether PHI is allowed (no) · demo length (20 min).

---

## 📝 Meeting summary — held 2026-10-13

### What he told us
| # | Topic | What was said | What it means for us |
|---|---|---|---|
| 1 | **Purpose** (M1) | Exploratory project. A showcase of my design thinking, system design, the questions I ask, how thoughtful I am, and how useful the tool can be | **The reasoning trail is the product.** Docs, decisions and approach files matter as much as the build. Polish the *why* |
| 2 | **Drug class** (M6) | Pick any category that is convenient. He suggested **narcotics (opioids)** as a good use case | Switch pilot class from GLP-1 → **opioids** (see [A001](../05-approaches/A001-pilot-scope.md)) |
| 3 | **Monitoring** (Part D) | Monitoring is "the beauty". Must show **production-side use** with **all aspects of monitoring** from the brief | Monitoring moves from ⭐ Stretch → ✅ **Must**, and becomes a demo centerpiece |
| 4 | **Drift window** | Drift seen over **3–4 days is bad** (too short / noisy); he prefers judging drift over **3–4 weeks** | Drift alerts use a 3–4 week window, not day-to-day swings. ⚠️ _Our reading. Confirm at next check-in_ |
| 5 | **Foundry access** (M3, M3a) | Use the **Palantir free Developer Tier** | Unblocks us. You sign up; build there |
| 6 | **Messy data** | Look at each source manually: what it looks like, what categories it falls into | Next step = **source profiling**, one file per source ([plan](../07-data-quality/source-profiles/README.md)) |
| 7 | **Side idea: health OS** | He described an Epic-like, health-specific "OS": multi-vendor, fast, lightweight, very efficient. I proposed a fine-tuned Linux distro | Parked. Out of pilot scope. Notes in [ideas parking lot](../09-roadmap/ideas-parking-lot.md) |

### Not discussed → our defaults stand
M2 dates · M4 internet access from Foundry (check on the Developer Tier) · M5 AIP models/budget (check on the Developer Tier) · M7 "on the label" · M8 real user interview · M9 clinical reviewer · all 🟡 questions. Defaults are in the tables above and in [DECISIONS.md](../06-decisions/DECISIONS.md).

### Follow-ups
| Item | Owner | Due |
|---|---|---|
| Sign up for Palantir Developer Tier | you | ASAP (approval may take time) |
| Confirm drift reading (3–4 week window) at next check-in | you → boss | next sync |
| Profile each data source by hand | you + Claude | next session |
| Lock opioid ingredient list | Claude (proposed in A001) → you confirm | next session |
