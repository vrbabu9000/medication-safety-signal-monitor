# Pilot → production roadmap

The pilot proves the pattern on one drug class. Production makes it safe, multi-tenant and supported.
**Nothing here enters pilot scope.** It feeds the "what I'd do with another month" part of the demo.

📊 **Diagram:** [05-pilot-to-production-v1.png](../diagrams/png/05-pilot-to-production-v1.png) · [PDF](../diagrams/pdf/05-pilot-to-production-v1.pdf) · _source: [05-pilot-to-production-v1.mmd](../diagrams/src/05-pilot-to-production-v1.mmd)_

| Dimension | Pilot (3 weeks) | Beta | Production |
|---|---|---|---|
| Drugs | 1 class (~6–10 ingredients) | Hospital's full formulary (upload) | Many hospitals, each with its own formulary |
| Refresh | Scheduled daily + quarterly FAERS | Same + failure alerts | SLAs, on-call, backfills |
| Reaction matching | MedDRA PT strings + LLM | + synonym tables tuned by pharmacists | MedDRA license, full hierarchy (SMQs) |
| AI reliability | Gold set ~30, hallucination check | Gold set ~200, drift checks on each model change | Validation protocol, human review for high-risk flags |
| Users | 1 persona | Safety team | Role-based access, committee workflows |
| Notifications | In-app | Email digest | Integrations (EHR alerts, ticketing) |
| Governance | Decision log | Change control | Audit trail, validation docs, security review |
| Cost | Measured once | Budget per tenant | Cost monitoring + optimization loop |
