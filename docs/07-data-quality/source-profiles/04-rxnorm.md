# RxNorm / RxNav: drug IDs — structure report

_Status: 🟡 Profiled by Claude 2026-10-20 · **your hand-verification pending** · Access: [00-source-access-guide.md](00-source-access-guide.md) · Join diagram: [13-join-keys-v1.png](../../diagrams/png/13-join-keys-v1.png)_

## In one line
Not "data about safety". It's the **dictionary that gives every drug one ID**. It's the glue that lets the other four sources join.

## How to navigate
| Step | Browser (RxNav) | API |
|---|---|---|
| Name → ID | Type "fentanyl" | `REST/rxcui.json?name=fentanyl` → **4337** |
| Messy name → best guess | (search box tolerates typos) | `REST/approximateTerm.json?term=oxycontin` |
| See the family | Click the concept → graph | `REST/rxcui/4337/related.json?tty=IN+PIN+BN+SCD+SBD` |
| NDC → ID | — | `REST/ndcstatus.json?ndc=…` |
| Class members | RxClass | `REST/rxclass/classMembers.json?classId=N02A&relaSource=ATC` |

## Record shape (a concept graph, not rows)
```
IN   ingredient          fentanyl (4337)            ← OUR KEY
 ├── PIN precise ingr.   fentanyl citrate, fentanyl hydrochloride
 ├── BN  brand           Abstral, Subsys, Ionsys, Actiq, Fentora
 ├── SCD clinical drug   47, e.g. "fentanyl 0.1 MG Sublingual Tablet"
 └── SBD branded drug    22, e.g. "… [Abstral]"
        └── NDCs (package codes) link to SCD/SBD
```

## Our 13 ingredient IDs (verified 2026-10-20)
fentanyl 4337 · morphine 7052 · hydromorphone 3423 · oxycodone 7804 · hydrocodone 5489 · methadone 6813 · buprenorphine 1819 · tramadol 10689 · semaglutide 1991302 · tirzepatide 2601723 · liraglutide 475968 · dulaglutide 1551291 · exenatide 60548

## Mess found
| Issue | Register |
|---|---|
| **ATC class N02A ("opioids") doesn't cleanly hold our list.** Methadone is filed only under opioid-dependence drugs (N07BC). Hydrocodone appears only in combination products (N02AJ) and cough medicines (R05DA), not as a single ingredient in N02A (verified 2026-10-20). The class code alone can't define our list | DQ31 |
| FAERS/openfda `rxcui` lists are product-level (8–35 IDs per drug) → must roll up to IN | DQ13 |
| Compounded-product NDCs are unknown to RxNorm | DQ29 |

## How to use it well
1. Build **one `drug_identity` table**: every name, NDC, product RxCUI and setid → ingredient RxCUI. Do it once and reuse it everywhere (architecture decision D003).
2. Define the formulary as an **explicit list of 13 RxCUIs**, not a class code.
3. Bulk "Current Prescribable Content" needs no license; the full release needs a free UMLS account.

## ✅ Your hand-verification
- [ ] In RxNav, open fentanyl and click through IN → BN → SCD
- [ ] Look up "OXYCONTIN" with approximateTerm
- [ ] Open the N02A class list: methadone absent, hydrocodone only as a combination

---

## Measured on real FAERS (added 2026-10-20)
_Atlas page: [rxnorm.html](../atlas/rxnorm.html) ([online](https://claude.ai/artifact/LGif4paMHMqWxtUBifxHZS)) · Script: [identity_atlas.py](../../../prototypes/explore/identity_atlas.py) · RxNorm release 05-Oct-2026 · FAERS 2026 Q1 + Q2 bulk · all roles, rows not reports_

| Measure | Result |
|---|---|
| FAERS rows in the wide net (name contains one of our 13 words or brands) | 174,654 |
| Distinct `prod_ai` ingredient strings containing our words | **41** (FDA-coded field is clean) |
| Strings found in RxNorm by exact name | 30 of 41; salt strip added **none**; adding "trihydrate" added 1 |
| Rows mapped to one of our 13 | **171,171** (171,166 by plain exact lookup = 99.997%) |
| Rows mapped to a different drug (correctly out) | 2,773: apomorphine 2,478 · heroin (DIAMORPHINE) 282 · levomethadone 8 · benzhydrocodone 3 · ethylmorphine 2 |
| Rows RxNorm doesn't know | 43: street analogues / metabolites (parafluorofentanyl 15, nicomorphine 8, desmetramadol 6, norbuprenorphine 5…) — none ours |
| RxNorm vs the walkthrough's hand rule | Same answer on every row except 5 (`OXYCODONE HYDROCHLORIDE TRIHYDRATE`) |
| Combination share | hydrocodone 75% · buprenorphine 24% · oxycodone 21% · tramadol 13% · liraglutide 6% (Xultophy) |
| Compounded mixes | ≥90 rows (cyanocobalamin / pyridoxine / glycine + semaglutide or tirzepatide) |
| Blank `prod_ai` (free text only) | 667 rows · `approximateTerm` finds ours for 77% · word + brand rule 98% |
| Our 13 IN RxCUIs | All Active, never remapped (opioids since 04/2005, tirzepatide since 06/2022) |
| Release clock | Monthly full release (03 Aug, 08 Sep, 05 Oct 2026) + weekly updates |

**So what:** matching is not the hard part (FAERS `prod_ai` is already coded). RxNorm's value is the stable ID, the graph to packages and labels, and a safe answer for new spellings. The hard part is Product, see [07-drugsatfda.md](07-drugsatfda.md).

## Proposed for the logs
_For the main session to merge. Placeholder numbers; assign real ones on merge._

### Proposed decisions
| # | Decision | Why (evidence) | Rejected |
|---|---|---|---|
| Dr1 | **`drug_identity` keyed by raw string:** raw string → IN RxCUI, match method, RxNorm version; look up only unseen strings; refresh monthly after the release | 41 strings cover 173,987 rows; IN IDs never changed | Re-match every row each run |
| Dr2 | **Match order:** RxNorm exact → RxNorm after salt strip (+ "trihydrate") → blank `prod_ai`: word + brand rule → `approximateTerm` | Exact gets 99.997%; rule beats approximateTerm on free text (98% vs 77%) | approximateTerm first |
| Dr3 | **Unresolved strings are tagged** (`analogue/metabolite`, `unresolved`), and monitoring counts new ones per quarter | 43 rows of street analogues fall out silently today | Silent drop |
| Dr4 | Pilot uses the RxNav API (cached); scale uses the no-licence monthly "Current Prescribable Content" zip | 1,046 API calls cover the pilot | Full UMLS release (licence, not needed) |

### Proposed data issues
| # | Source | Issue | Impact | Fix |
|---|---|---|---|---|
| DQr1 | FAERS × RxNorm | `OXYCODONE HYDROCHLORIDE TRIHYDRATE` not in RxNorm and not in the salt list (5 rows) | Tiny miss | Add "trihydrate" to salt list |
| DQr2 | FAERS × RxNorm | Benzhydrocodone (hydrocodone prodrug) is a separate IN (3 rows) | Count as hydrocodone? | PV call (open) |
| DQr3 | FAERS × RxNorm | 11 analogue/metabolite strings unknown to RxNorm (43 rows) | Fall out as unknown | Dr3 tag |
| DQr4 | FAERS | 667 rows with blank `prod_ai`; free text cut off / hyphenated | Needs fallback | Dr2 order |
