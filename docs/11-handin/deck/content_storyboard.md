# Content storyboard — MSSM hand-in demo deck (v2, 2026-11-06)

_🖼️ Deck Designer view · Stage: **Prototype → Test** (design thinking) · v2: D041 v2 (AI reads the semaglutide labels; page-1 AI quotes, Workshop v0.10.0), 12 decisions accepted 6 Nov, duplicate link deleted, diagrams bumped_

This is the brief behind [MSSM-demo-deck.pptx](MSSM-demo-deck.pptx) ([PDF preview](MSSM-demo-deck.pdf)). For each slide it gives the purpose, the evidence, the rubric row it proves and its time slot. The spoken words are in [speaking_script.md](speaking_script.md); the newcomer's notes are in [slide_explanations.md](slide_explanations.md). The slide ids link to the handbook; the script uses the same anchors (`#s01` … `#s16`, `#b01` … `#b12`).

**Binding agenda:** [AGENT-BRIEF.md](../AGENT-BRIEF.md) "The 20-minute demo". The deck carries the slide parts. For the app parts it shows a navy **LIVE IN THE APP** band (what to click) and a screenshot as a fallback. Under-the-hood stops show a smaller **▶ SWITCH** cue.

**Numbers:** every number on a slide is read from [numbers.json](../numbers.json) by [build_deck.js](build_deck.js). Ratios and percentages (×2.75, −59%, 21%, ×3.3, F1) are computed in the script from two json numbers and carry a DERIVED pill. Numbers printed *inside* diagram images come from the diagram set (they match numbers.json where both exist; see the note on diagram 33 below).

## Narrative spine
The officer's three questions → she answers them live in the app, and one flag traces to its evidence → how the data gets there (architecture, ontology, one report to one signal) → how far to trust it (AI, monitoring) → what we sped up and what we did not → the mess we found and what we chose not to do → another month → what to take away.

## Visual language
| Element | Meaning | Look |
|---|---|---|
| Evidence pill | **OBSERVED** = measured in Foundry · **DERIVED** = computed from observed numbers · **ASSUMED** = not verified, taken as true for now · **DESIGNED** = a design choice we made and wrote down (may be built; the status band says how far) | Soft filled pill, dark text (teal / grey-blue / amber / stone) |
| Status band | **BUILT · TESTED IN FOUNDRY** (solid green) · **PLANNED — NOT BUILT** (dashed amber) · **DECISIONS ACCEPTED · 6 NOV 2026** (solid green, B6); the dashed red *proposed* band is no longer used | White band, coloured border, square corners |
| LIVE band | The presenter leaves the deck for the Workshop app | Full-width navy band under the lead |
| ▶ SWITCH cue | Optional or short under-the-hood stop in Foundry | Small navy block |
| Chips (top right) | Rubric row this slide proves · its time slot in the agenda | Teal pill · outlined pill |
| Cards | teal = fact · green = works / proven · amber = limit or caveat · stone = choice / context | Rounded boxes, hand-in palette ([style.py](../../../tools/handin/style.py)) |
| Charts | Native, editable pptx charts; direct labels; no legend unless two series | teal / navy / rule grey |

Palette: navy `#13324B`, teal `#087F8C`, light `#EAF3F5`, ink `#263746` (same as reports and diagrams). Font: Arial.

## Main slides (20:00)
| # | Title (takeaway) | Purpose | Evidence on the slide | Rubric row | Slot | Min |
|---|---|---|---|---|---|---|
| [s01](slide_explanations.md#s01) | Medication Safety Signal Monitor | Name the product and the three questions | scope (13 drugs, 8 + 5), FAERS 2026Q1–Q2, capture date | Communication | 0:00–0:20 | 0.33 |
| [s02](slide_explanations.md#s02) | Her three morning questions, and one trust rule | The user, her pain, the trust rule, the scope (13 drugs named); define the 4 sources; only measured claims (machine load 11.5 s; human walk-through to be timed) | brief summary; D014, D018 (DESIGNED) | Communication | 0:20–1:30 | 1.17 |
| [s03](slide_explanations.md#s03) | Morning brief: three numbers, and how fresh each source is | **LIVE page 0.** All three answers at once + source ages | 1,073 ranked · 126 active (status Ongoing) of 900 · 26 change events in the last 30 days (not "since yesterday") · FAERS freshness 130 d · openFDA 8 d; timed: brief 11.5 s, switches 0.8–2.4 s (OBSERVED); screenshot | Application | 1:30–3:00 | 1.5 |
| [s04](slide_explanations.md#s04) | Not in label: from one flag to its evidence to a saved decision | **LIVE page 1.** Name the noise (unfiltered rank 1s) → filter → NAION → evidence → **known positive** (EMA/PRAC 6 Jun 2025; WHO 27 Jun 2025) → open Ozempic v20 on DailyMed, find "optic" (rehearsal check) → scroll to the AI table (retinopathy yes, optic nerve no) → Triage; 394 reports not openable yet | NAION a = 394 of 20,892, PRR 112.5 (92.19–137.24), rank 1; 3 reference labels searched with DailyMed links, also read by the AI (3; OBSERVED); screenshot app-1e; PRR/Evans defined | Application · AI reliability (trace) | 3:00–6:00 | 3.0 |
| [s05](slide_explanations.md#s05) | Recalls, and what changed since my last review | **LIVE pages 2–3.** Newest recall matches none of the 658 FDA-listed products we track (no inventory data); openFDA record tab; Class I first (count = rehearsal check); date filter = since my last review; label rows say a version took effect, not what changed; signals move only per FAERS quarter | 126/900, D-0040-2027 (2026-10-21); 2,898 events = 900 + 767 + 1,231 (the 1,231 of 1,321 label versions that carry an effective date); past month = 26; 658 products from foundry/ontology/README.md (OBSERVED) | Application | 6:00–7:30 | 1.5 |
| [s06](slide_explanations.md#s06) | Architecture: drug identity resolved once, reused everywhere | Raw → clean → curated → Ontology → Workshop; where identity lives; **SWITCH Data Lineage** | Diagram 38 v2 (one-page architecture note); D020, D027; status TESTED | Architecture | 7:30–9:30 | 2.0 |
| [s07](slide_explanations.md#s07) | Ontology: objects, links, and one create-only Action | Object / link / Action explained; decisions survive rebuilds; 10 link types (the duplicate link, deleted 6 Nov, as a one-line history note); **SWITCH Ontology Manager, Object Explorer** | Diagram 31 v2; 2 triage decisions (OBSERVED) | Architecture | 9:30–11:30 | 2.0 |
| [s08](slide_explanations.md#s08) | From one FAERS report to a ranked signal | Four cleaning rules, the 2×2 test, three label checks, the buckets | Diagram 32 v3 (NAION 2×2 from the local run = Foundry, A014; label-check counts from Foundry: AI 188, text 1,252, synonym 163 / 210) | Data judgment · AI reliability | 11:30–12:50 | 1.33 |
| [s09](slide_explanations.md#s09) | 1,073 ranked signals is a review queue, not 1,073 findings | Funnel 14,921 → 1,952 → 1,073; queue 1,355 at step 9 → 1,210 → 1,115 → 1,073 (−21%); synonym bands; why no MedDRA | numbers.json signals, synonyms (OBSERVED); −21% (DERIVED) | Data judgment | 12:50–13:30 | 0.67 |
| [s10](slide_explanations.md#s10) | AI extraction: quotes are real; accuracy on a small key | Grounding, answer-key items found, F1 (with its 35-item scope) vs target, cache; what it does not show; **where the AI meets the screen** (D041 v2: retinopathy yes, optic nerve no; quotes on page 1) | 745/745 (all 21 sections, 5 labels); found 35 of 35 answer-key items (p1 11 of 35) on 2 oxycodone labels, Claude-written key, ≥35/37, F1 0.97 vs 0.85; semaglutide sections not scored; 12 calls to add semaglutide, 0 calls / 21 of 21 cached on forced rebuild; TESTED + PLANNED | AI reliability | 13:30–14:45 | 1.25 |
| [s11](slide_explanations.md#s11) | Monitoring: 21 checks per build caught two real shifts | Check rows, Data Health, two real warnings, honest limit | 21 / 4 / 3 runs; 34% → 72%; 10 vs 3 (×3.3 DERIVED); SQL screenshot | AI reliability · monitoring | 14:45–15:30 | 0.75 |
| [s12](slide_explanations.md#s12) | Optimization log: four measured tries, two helped, two did not | Before/after table + bar chart; where it paid, where not; partitioning not done on purpose (D048); caveats | O1 9 → 0 calls, 70,776 → 0 tokens; O2 32 s vs 88 s (×2.75); O3 3 m 23 s → 1 m 23 s, 1,321 → 2 XML downloads (index still pulled) (−59%); O3a 12.3–13.0 → 12.2 s local | Optimization | 15:30–16:45 | 1.25 |
| [s13](slide_explanations.md#s13) | Incremental FAERS: proven correct, but slower at two quarters | Why it is not switched on (D044) | Diagram 33 FAERS panel (crop of v2; unchanged in v3); 792,346 / 2,554,017 / 373,522; state (three state datasets + one quarter log) 62 s + outputs 26 s = 88 s vs 32 s | Optimization | 16:45–17:30 | 0.75 |
| [s14](slide_explanations.md#s14) | Data judgment: what we found, and what we chose not to do | Four messes (DQ36, DQ37, DQ38, DQ42), noise we left (DQ06 indication terms, DQ04 stimulated reporting), three "chose not to" | 26,681 replaced / 655 deleted; 34% → 72%; 2 of 1,321 "None" replies (OBSERVED) | Data judgment | 17:30–19:00 | 1.5 |
| [s15](slide_explanations.md#s15) | With another month: a pharmacist review loop first | The loop (Claude prepares → pharmacist decides → Action records → rebuild); then schedules, live drift, health page, scoring long sections, AI on other drugs | 258 synonym rows; estimate 7–8 + 3–4 days (ASSUMED); PLANNED | Communication | 19:00–19:40 | 0.67 |
| [s16](slide_explanations.md#s16) | What to take away | Three takeaways; R00 "Start here" pointer; what did not work; Q&A jump links | 88 s vs 32 s; semaglutide sections not scored; timings from v0.9.0 | Communication | 19:40–20:00 | 0.33 |
| | | | | | **Total** | **20.0** |

## Backup slides (Q&A, one per rubric row + extras)
| # | Slide | Title | Answers the question | Rubric row |
|---|---|---|---|---|
| [b01](slide_explanations.md#b01) | 18 | How another engineer would extend it | "Where would I add a drug / source / synonym / check?" | Architecture |
| [b02](slide_explanations.md#b02) | 19 | Incremental pieces in full (diagram 33 v2) | "Show the whole incremental design"; O3 numbers; O1 tokens | Optimization |
| [b03](slide_explanations.md#b03) | 20 | Drug identity and FAERS counting rules | "Why these counts?" D020–D023, D037 + D043 | Data judgment |
| [b04](slide_explanations.md#b04) | 21 | Trace and write-back: the trust rule in practice | "How do I know a flag is real? Is the write-back safe?" | Application |
| [b05](slide_explanations.md#b05) | 22 | AI evaluation details | "How was the AI scored? How would you notice it getting worse?" | AI reliability |
| [b06](slide_explanations.md#b06) | 23 | Where the reasoning lives, and what was accepted | "Which decisions are final?" | Communication |
| [b07](slide_explanations.md#b07) | 24 | Ripple map (diagram 37 v2) | "If I change X, what changes on screen?" | Architecture |
| [b08](slide_explanations.md#b08) | 25 | Change feed (diagram 34) | "How do you know what changed since my last review?" | Application |
| [b09](slide_explanations.md#b09) | 26 | Monitoring (diagram 35) | "Who finds out when something breaks?" | AI reliability · monitoring |
| [b10](slide_explanations.md#b10) | 27 | Another month: sources researched | "Why not DrugBank / ClinicalTrials.gov / MedDRA?" | Communication |
| [b11](slide_explanations.md#b11) | 28 | Demo map (diagram 36 v2, 23 stops) | "What did you show, in what order?" | Communication |
| [b12](slide_explanations.md#b12) | 29 | Under the hood: fallback screenshots | Live Foundry is slow or down | Architecture |

Slide 16 and the backup divider (slide 17) link to every backup. In slide show, type the slide number and press Enter.

## Rubric coverage (brief §5 "What we will look at")
| Rubric row | Main slides | Backups |
|---|---|---|
| Architecture | 6, 7 | B1, B7, B12 |
| Optimization | 12, 13 | B2 |
| Data judgment | 8, 9, 14 | B3 |
| The application | 3, 4, 5 | B4, B8 |
| AI reliability | 4 (trace), 8, 10, 11 | B5, B9 |
| Communication | 1, 2, 15, 16 | B6, B10, B11 |

## Pictures used
| Slide | Picture | Note |
|---|---|---|
| 3, 4, 5 | `screens/app-0-morning-brief.jpg`, `app-1e-ai-quotes-panel-naion.jpg` (1512 × 806), `app-2-recalls.jpg`, `app-3b-what-changed-past-month.jpg` | Fallback for the live app |
| 6 | `diagrams/png/38-handin-architecture-onepage-v2.png` (2220 × 2034) | Same picture as the one-page architecture note; the detailed flow (diagram 30 **v3**) is in the reports |
| 7 | `31-handin-ontology-v2.png` (4752 × 3162) | No duplicate-link box |
| 8 | `32-handin-signal-pipeline-v3.png` (4752 × 1941) | Label checks in code order (1 AI → 2 Text → 3 Synonyms), Foundry counts |
| 11 | `assets/monitoring-checks-sql-crop.png` | Crop of `screens/hood-monitoring-checks-sql.jpg` (result table only) |
| 13 | `assets/33v2-faers-panel-crop.png` | Crop of diagram 33 v2, FAERS panel only (unchanged in v3) |
| B2 | full diagram 33 v3 (4752 × 2910) | |
| B4 | `app-1b-triage-action-form.jpg`, `hood-object-explorer-naion-links.jpg` | Captured 5 Nov: old NAION evaluation id; shows the since-deleted duplicate link |
| B5 | `assets/ai-cache-sql-crop.png` | Crop of `hood-ai-extractions-cache-sql.jpg` (5 Nov, 9 v1-pilot sections) |
| B7–B9, B11 | diagrams 37 v3 (4752 × 2361), 34 v1 (4752 × 2415), 35 v2 (4752 × 1956), 36 v3 (4752 × 2964) | |
| B12 | `assets/data-lineage-crop.png` + 3 `hood-*.jpg` | Lineage crop of `hood-data-lineage-signals.jpg` |

## How to rebuild
```bash
# once, outside the repo
cd <scratch dir> && npm install pptxgenjs@3.12.0
# build + preview
NODE_PATH=<scratch dir>/node_modules node docs/11-handin/deck/build_deck.js
cd docs/11-handin/deck && soffice --headless --convert-to pdf MSSM-demo-deck.pptx
```
If numbers.json changes, rebuild: every slide number follows. The three .md files carry the numbers as text and must be re-checked by hand (fact-checker).
