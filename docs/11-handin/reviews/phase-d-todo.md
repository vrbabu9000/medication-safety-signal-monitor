# Phase D fix list (lead's running list)

Changes made AFTER some agents wrote their pieces — every hand-in item must reflect them:
1. Page 1 now has a **"Reference labels searched" panel** (Signal → Drug → Products → Reference Label; for NAION: Ozempic v20, Wegovy v19, oral Ozempic v14, with DailyMed links). Screenshot `screens/app-1c-labels-searched-naion.jpg`. Affects R03 (trace), R04 (app), demo guide, deck, diagram 36.
2. **Timed flow done** (numbers.json `app.timing_s`): brief 11.5 s load, page switches 0.8–2.4 s. R04/R05 say "not run" — update.
3. Morning brief "We pulled it at" no longer shows "No value" (FAERS = "quarterly file (no pull time)", RxNorm = pull time). R04 mentions No value — update.
4. Workshop is v0.9.0.
5. Diagram 30 (and anything else) saying O3 "being measured" → measured (33 v2 exists).
6. DECISIONS status cells refreshed: D005, D020–D024 Accepted; new D048 (no partitioning, proposed). D037 is still Proposed → in the user's batch-accept list with D045–D048.
7. Architecture note footer says "reports R0-R7" → reports R01–R09.
8. Rubric-check findings to answer in deck/demo (docs/11-handin/reviews/rubric-check.md): AI↔screen gap (honest answer + D041 v2 as "another month" / user decision), indication terms (liraglutide "Diabetic metabolic decompensation" #1 — DQ06), stimulated reporting (DQ04).
