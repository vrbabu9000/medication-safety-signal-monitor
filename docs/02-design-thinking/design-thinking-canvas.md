# Design-thinking canvas

_Stage tracker:_ **Empathize 🟡** → Define ⚪ → Ideate ⚪ → Prototype ⚪ → Test ⚪

## 1. Empathize — who is she?
**Persona: "Dana", Medication Safety Officer (PharmD), 600-bed health system** _(fictional; replace with real interview findings if M8 = yes)_

| Says | Thinks |
|---|---|
| "I found out about that recall from a nurse." | "Am I missing something right now?" |
| "I don't have time to read FAERS." | "If I escalate a false alarm, I lose credibility with P&T." |
| **Does** | **Feels** |
| Scans FDA emails, MedWatch alerts, ISMP newsletters, vendor notices | Anxious about being late. Skeptical of black-box tools |
| Brings safety issues to the P&T / Medication Safety committee | Wants to be the one who caught it first |

**Her day:** 15 minutes in the morning for safety review, between other duties.
**Her bar for trust:** "Show me where it says that." Any flag without a source is noise.

## 2. Define — the problem statement (POV)
> **Dana**, a hospital medication safety officer, **needs** a fast, trustworthy morning view of emerging drug risks on her formulary,
> **because** today she learns about them late and scattered, and can't defend an escalation without evidence.

## 3. Ideate — "How might we…"
- HMW show only what's **new or worse** so she isn't re-reading yesterday's list?
- HMW make "**not on the label**" provable in one click?
- HMW signal **how confident** we are (report count, stats, trials corroboration) without a stats lecture?
- HMW let her **record a decision** so the next morning reflects it?
- HMW warn her when the **AI might be wrong**?

## 4. Prototype — what we'll show her first
Paper / Workshop wireframe with 3 panels: **New today** · **Ranked signals** · **Active recalls**. Drill-down = label passage | AI extraction | FAERS counts.
_(Prototype file will go here as `prototype-v1.md` + screenshots.)_

## 5. Test — how we'll know it works
| Test | Pass if |
|---|---|
| "Morning in 2 minutes" walk-through | Persona answers all 3 questions in ≤2 min |
| Trust check | Every flag → source in ≤2 clicks |
| Backtest (idea P1) | We flag ≥1 reaction before FDA added it to the label |
| AI check | Hallucination rate measured on gold set and shown |

## Assumptions to validate
| # | Assumption | How to validate | Status |
|---|---|---|---|
| AS1 | She thinks at ingredient level, not product | Boss / interview (S5) | Open |
| AS2 | Warnings sections count as "labeled" | Boss (M7) | Open |
| AS3 | Daily cadence is enough (no real-time) | Interview | Open |
