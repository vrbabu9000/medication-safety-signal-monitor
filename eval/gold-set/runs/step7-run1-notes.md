# Step 7 run 1 — pilot extraction vs frozen gold (2026-11-04)

Config: model `claude-sonnet-5.5`, prompt `p1`, parser `x1`. Labels: OxyContin `bfdfe235…|v44`, oxycodone/APAP generic `cc966d57…|v19`. Gold: [step7-pilot-gold-v1.json](../step7-pilot-gold-v1.json) (written before scoring; pharmacist review pending).

Short-section terms, as read from Foundry SQL: [step7-run1-short-sections.jsonl](step7-run1-short-sections.jsonl). A few long terms are shortened to their visible prefix; this does not affect matching. Score: `check_gold.py` → **recall 32/35 = 0.91**, 33/33 grounded.

| Label | Section | Recall | Missed | Extra (not reactions: mechanism/process) |
|---|---|---|---|---|
| OxyContin | Boxed Warning | 10/10 | — | increased oxycodone plasma concentration ×2 |
| OxyContin | Contraindications | 5/6 | paralytic ileus | — |
| Generic | Boxed Warning | 12/13 | hepatotoxicity (given as acute liver failure + liver injury) | increased oxycodone plasma concentration ×2 |
| Generic | Contraindications | 5/6 | paralytic ileus | — |

Caveat: recall is lenient. A grouped term ("addiction, abuse, and misuse") counts for each of its parts. With atomic matching, the Boxed Warning results would be lower until prompt p2 splits lists.

Not yet scored: Warnings and Precautions, Warnings, Precautions and Adverse Reactions (366 of 403 items). They go into the pharmacist packet.

## Run 2 — prompt p2 (2026-11-04)

Terms: [step7-run2-p2-short-sections.jsonl](step7-run2-p2-short-sections.jsonl). `check_gold.py --strict` gives **35/35 = 1.00** (run 1 strict: 11/35 = 0.31). All 4 sections are now at full recall. Extras: "adverse drug effects" (OxyContin boxed warning, too generic) and "liver transplant" (generic boxed warning, an outcome). Whole run: 448 reactions, 448/448 quotes exact.
