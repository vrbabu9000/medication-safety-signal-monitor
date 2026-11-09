# A020 — Demo-prep skill, cue card and build tutorial (local branch)

| | |
|---|---|
| **Date** | 2026-11-08 |
| **Design-thinking stage** | Prototype → Test |
| **Area** | Process |
| **Status** | Kept (local branch `demo-prep`, not for main) |
| **Replaces** | none (sits on top of the hand-in demo guide, does not replace it) |

## What changed
| Before | Now | Why |
|---|---|---|
| Demo prep = reading a 348-line [navigation guide](../11-handin/demo/demo-navigation-guide.md) and a speaking script | A **cue card** for the second screen: one stop per screen, annotated screenshot, 3 talk points, number, trap, timer | The presenter can't sit and read long text; pictures with red boxes are faster |
| No "how I built it" walk-through with screens | **Tutorial** (12 chapters, HTML + PDF) following the build order: goal, data seen, problem → fix, insight, redo steps | Rebuild the tool in a new instance and explain the data-engineering story |
| No skill | Project skill **`foundry-demo`** (`.claude/skills/foundry-demo/`) | "Prep me for stop H6", "teach me step 4" answered from one source |

## The idea in 3 lines
1. One content file ([content.py](../../tools/demo_prep/content.py)) holds shots + red boxes, 23 stops, 12 chapters.
2. One builder ([build_all.py](../../tools/demo_prep/build_all.py)) makes annotated PNGs, JSON for the skill, cue card, tutorial HTML + PDF.
3. Screens captured read-only from Foundry with Claude in Chrome (the app's browser pane had no Foundry session).

## How we tested it
32 fresh captures on 2026-11-08 (+ 5 reused from the hand-in screens), contact sheets checked for box alignment, cue card and tutorial rendered with headless Brave, tutorial PDF pages viewed, fact-checker pass on numbers.

## Result
36 annotated screens · 23 stops · 12 chapters · tutorial PDF ~16 MB. New facts seen: Morning brief card 3 = **22** (was 26 on 5 Nov; rolling 30 days); project description still says "Pilot focus: opioids".

## Update 2026-11-08 (2): grand tutorial book
7 writer agents (one per track) + 1 reviewer produced [book/](../12-demo-prep/book/book.html) (263-page PDF). SQL cookbook (20 queries) run live, read-only; results and screenshots pasted under each query. Reviewer fixed 25 issues; 5 open items in `00-review.md`. Cue card timer removed by request (learn first, cut later).

## Verdict
Keep, on the local branch. It's presenter tooling, not part of the hand-in.

## Diagram
[39 v1 PNG](../diagrams/png/39-demo-prep-pack-v1.png) · [PDF](../diagrams/pdf/39-demo-prep-pack-v1.pdf)

## Persona check
- 🎬 Demo Director: stops, budgets and fallbacks copied from the guide; the cue card adds timing per stop.
- 💊 Safety Officer: the A-stops still lead with her three questions and the trust rule.
- 🧐 Evaluator: every number traces to numbers.json or is marked "seen 2026-11-08"; F1 always said with "self-scored".
