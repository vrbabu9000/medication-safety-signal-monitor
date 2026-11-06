# MSSM-30-v1 — comparison analysis (Claude, after freeze)

**Inputs:** the script output is in [comparison.json](comparison.json) and [comparison.md](comparison.md), made by `compare_answers.py` on 2026-11-01T20:10:59Z. The shared pack's hashes were checked again before comparing.
**Frozen files:** Claude `answers.jsonl` sha256 `d33088a1…16965` (frozen 2026-10-31T22:21:11Z, before codex/ was opened). Codex `answers.jsonl` sha256 `f22e804b…2a8ce`. Neither file was changed.

## 1. Result

| | |
|---|---|
| Exact answer agreement | **29 / 30** |
| The 1 mismatch | **G26**, a formatting difference only. I added a `product_number: "001"` key that the case format didn't ask for. All four values the case asked for are identical. Codex's shape follows the case format more closely. |
| Agreement on substance | 30 / 30 |
| answer_status | Same for all 30 (all resolved; G23 and G24 are deliberately "unknown") |
| source_ids · source_sha256 · retrieved_at_utc | Same for all 30 |

## 2. What the agreement does **not** show

- **The two annotators weren't fully independent.** `build_reference.py` says it builds "a frozen question pack and Codex's independent candidate answers". It writes `shared/cases.json` and `codex/answers.jsonl` in the same pass, and each case is defined together with its answer. So Codex set the questions knowing the answers it intended.
- **The questions carry hints.** For example, G23's locator text says "status not updated after classification". G26 points straight at `/products/1`. G23 and G24 list "unknown" as an option. My agreement with Codex mostly shows that I read the case-setter's intent the same way. It is weaker evidence than two blind annotators would give.
- **Agreement isn't truth.** Both models are self-checked, and every row is still `human_verdict: pending`. Nothing here supports a claim of "AI clinical accuracy".

## 3. Differences beyond the answer value

These don't change any answer, but they matter for traceability and for how a human reviews.

| Topic | Codex | Claude | Why it matters |
|---|---|---|---|
| Quote length | Usually just the target phrase (G01, G03, G07, G08, G10, G11, e.g. "serotonin syndrome") | The full sentence that gives the context | A bare phrase shows the word appears, not what role it plays. The trust rule is that every flag traces to evidence, so the context is the evidence. |
| Uncertainty filled in | 10 of 30 rows | 30 of 30 | The empty ones include G14, G16 and G23, where real caveats exist |
| Source dates | Copies the whole metadata block (disclaimer, title). RxNorm, SrLC and CT.gov are `{}` | Picks the specific date field. Gives the SrLC entry date and the CT.gov lastUpdatePostDate (ESTIMATED) | The CT.gov and SrLC dates *are* in the source, so leaving them empty under-reports them |
| G14 term type | Not mentioned | The response doesn't state tty=IN for 7052 | The question says "ingredient RxCUI" |
| G16 link | Not mentioned | `relatedGroup.rxcui` is null, so the link rests on the request URL | This changes what counts as evidence |
| G25/G26 vs G27 strings | Not mentioned | "KNOA PHARMA" vs "Knoa Pharma LLC"; the two dosage-form strings differ | Joining sources on exact string equality will fail |
| `srlc_oxy` file | Not mentioned | It's an **OZEMPIC** page (DrugNameID=2183) | A pack error; anyone trusting the file name is misled |
| Alternative readings (G04, G07, G11, G12) | Each answer treated as settled | Alternatives listed for human review | These are where human reviewers are most likely to disagree |

## 4. Recommended human review order

Because the two model answers agree everywhere, review by risk, not by disagreement.

1. **G04, G07, G11, G12.** These are the class-boundary calls. First decide the class tie-break rules in [review-notes.md](../claude/review-notes.md) §2.
2. **G23, G24.** Confirm the scorer gives full credit for "unknown".
3. **G14, G16.** Decide whether a manifest request URL counts as evidence, or capture the `properties.json` responses.
4. **G26.** Choose the canonical answer shape (with or without `product_number`) before scoring a system against it.
5. All other rows: a quick spot-check against the locator.

## 5. Suggested pack fixes for v2 (to be done by the pack owner)

- Have a third party write the questions, or blind both annotators to whoever wrote them. Remove hint wording from the locators.
- Rename or drop `evidence/srlc_oxy.*` (OZEMPIC).
- Recapture the FAERS oxycodone-filtered counts with an API key, and add them as new cases rather than replacing existing ones.
- Record the case format for each object answer, with no extra keys allowed.
