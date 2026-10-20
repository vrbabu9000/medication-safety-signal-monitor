# Architecture v0 — first draft (before Foundry access)

_Status: Draft · Approach: [A000](../05-approaches/A000-project-setup.md) · Editable diagram: [diagrams/01-data-flow-v0.drawio](diagrams/01-data-flow-v0.drawio) (open in draw.io → Export as VSDX for Visio)_

## Data flow: raw → clean → ontology → app
```mermaid
flowchart LR
  subgraph SRC[Public sources]
    FAERS[FAERS quarterly files]
    DM[DailyMed SPL XML]
    ENF[openFDA Enforcement]
    RXN[RxNorm API / RRF]
    CTG[ClinicalTrials.gov v2]
  end
  subgraph RAW[Raw layer · as-landed, immutable]
    r1[faers_raw]:::inc
    r2[labels_raw]:::inc
    r3[recalls_raw]:::inc
    r4[rxnorm_raw]
    r5[trials_raw]
  end
  subgraph CLEAN[Clean layer]
    ID[[drug_identity<br/>resolved ONCE on RxCUI]]:::key
    c1[faers_cases_dedup]
    c2[label_sections]
    c3[recalls_clean]
    c5[trial_aes]
  end
  subgraph AI[AI layer]
    X[LLM extraction<br/>new/changed label versions only]:::llm
    G[Grounding check<br/>is reaction in passage?]
  end
  subgraph ONT[Ontology]
    D((Drug)) --- LB((Label)) --- AE((Adverse Event))
    D --- RC((Recall))
    D --- SG((Signal))
  end
  APP[Workshop app<br/>Signals · Drill-down · Recalls · Triage]
  FAERS-->r1-->c1; DM-->r2-->c2; ENF-->r3-->c3; RXN-->r4-->ID; CTG-->r5-->c5
  ID-->c1 & c2 & c3 & c5
  c2-->X-->G-->LB
  c1-->STAT[Disproportionality<br/>PRR / ROR]-->SG
  G-->SG
  c3-->RC; c5-.->SG
  ONT-->APP
  APP-->|Action: triage writes back|SG
  classDef inc fill:#d1fae5,stroke:#059669
  classDef key fill:#fde68a,stroke:#b45309,stroke-width:2px
  classDef llm fill:#e0e7ff,stroke:#4338ca
```
Green = incremental. Yellow = the single drug-identity step. Blue = the expensive LLM step.

## Ontology v0
```mermaid
erDiagram
  DRUG ||--o{ LABEL : "has versions"
  DRUG ||--o{ RECALL : "affected by"
  DRUG ||--o{ SIGNAL : "has"
  LABEL ||--o{ LABELED_REACTION : "extracted (LLM)"
  DRUG ||--o{ ADVERSE_EVENT_STAT : "reported in FAERS"
  SIGNAL }o--|| ADVERSE_EVENT_STAT : "evidence"
  SIGNAL }o--o| LABELED_REACTION : "absent from label"
  SIGNAL ||--o{ TRIAGE_DECISION : "write-back"
  DRUG { string rxcui_ingredient PK string name string class }
  LABEL { string setid_version PK string setid int version date effective }
  LABELED_REACTION { string id PK string reaction_text string meddra_pt string section string passage int char_start string model_version bool grounded }
  ADVERSE_EVENT_STAT { string id PK string meddra_pt string quarter int n_reports float prr float chi2 }
  RECALL { string recall_number PK string classification string status date report_date string reason }
  SIGNAL { string id PK string meddra_pt string status float score date first_seen }
  TRIAGE_DECISION { string id PK string user string new_status string note datetime at }
```

## The 4 decisions that will matter most (candidates for the 1-page note)
1. **Where drug identity is resolved:** one `drug_identity` dataset on RxNorm ingredient, used by everything.
2. **What runs incrementally:** FAERS by quarter; labels by set ID + version; recalls by report date. Signal stats are recomputed (small) on top.
3. **Where the LLM sits:** after the label clean step, only on new versions, cached by (setid, version, prompt version, model).
4. **How "unlabeled" is matched:** MedDRA PT from FAERS vs. extracted label reactions normalized to PT (LLM-assisted, then exact/synonym match).

## Chose not to do (draft)
Real-time streaming · full MedDRA hierarchy (licensing) · causality scoring · all drugs.
