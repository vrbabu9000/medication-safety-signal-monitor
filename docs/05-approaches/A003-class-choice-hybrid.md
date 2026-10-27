# A003 — Class choice: opioid-led hybrid (opioids + GLP-1)

| | |
|---|---|
| **Date** | 2026-10-19 |
| **Design-thinking stage** | Define |
| **Area** | Scope |
| **Status** | **Kept** (accepted by user 2026-10-20) |
| **Replaces** | Opioids-only scope in A001 (D007) |

## What changed
| Before | Now | Why |
|---|---|---|
| ~12 opioids only | **8 opioids + 5 GLP-1 drugs = 13 ingredients** | Opioids alone score 22/30. Their FAERS data is swamped by lawsuits/abuse, and label changes come in waves. GLP-1s add steady change and a clean "not on the US label" story. Hybrid scores 27/30 ([R1](../01-discovery/research/R1-therapeutic-class.md)) |
| Drift shown via new signals | Drift shown via **label churn + label lag across generics + recalls** | Opioids: ~15–20 new label versions per 3–4 weeks; generic labels lag brand updates |

## The list
| Group | Ingredients |
|---|---|
| Opioids (8) | fentanyl, morphine, hydromorphone, oxycodone, hydrocodone, methadone, buprenorphine, tramadol |
| GLP-1 receptor agonists (5) | semaglutide, tirzepatide, liraglutide, dulaglutide, exenatide |
| Formulary definition | RxNorm/RxClass (ATC N02A for opioids; GLP-1 class via RxClass), so it's reproducible |

## Rules that come with it
1. Separate out **lawyer-reported** FAERS cases and **abuse/overdose/dependence** terms from the opioid ranking, and say so on screen.
2. Limit opioid labels to **brand (reference) labels + hospital IV products**; track generic label lag as a drift metric.
3. GLP-1 wording: "**reported, not on the US label**", never "caused by". Flag news-driven spikes (e.g., NAION).

## Trade-off to say out loud
Two classes is slightly broader than "one therapeutic class". It's still 13 ingredients, well inside "sane scope". If the boss wants strict single-class, fall back to **opioids-only with rules 1–2** (A001).

## Focus rule (added 2026-10-20, D016)
Rank what matters to the safety officer: **clinical side effects** and **recalls**. Tag, but don't rank, these buckets:
| Bucket | Mainly hits | Example terms |
|---|---|---|
| Lawyer-filed (reporter = 4) | hydrocodone, hydromorphone (51%), oxycodone (29%) | — |
| Abuse/overdose | opioids | Drug dependence, Overdose, Withdrawal |
| Product-use/dose error | GLP-1s (tirzepatide 64k mentions) | Incorrect dose administered, Off label use |
| Pregnancy/neonatal | hydrocodone, methadone | Neonatal withdrawal, Foetal exposure |

## Verdict
Kept. Formulary = 13 explicit RxCUIs (D018). Volumes: [06-data-volume](../07-data-quality/source-profiles/06-data-volume-13-ingredients.md).
