# foundry/pipelines/ai/ — AI label extraction (Part B)

Mirror of [ai_label_extraction.py](ai_label_extraction.py). It lives in Foundry repo `Pipelines/pipelines_clean` and writes to `Data/curated`. Approach: [A011](../../../docs/05-approaches/A011-ai-label-extraction-pilot.md). Contract: [conventions §8](../../../docs/04-architecture/foundry-conventions/conventions-v1.md#8-ai-extraction-and-evidence-contract).

| Output | Grain / key | What it holds |
|---|---|---|
| `ai_label_section_extractions` | one section extraction / `cache_key` | status (`ok`, `empty`, `parse_error`, `model_error`), raw model response, tokens, latency, `from_cache` |
| `ontology_labeled_reactions` | one reaction per label section / `labeled_reaction_key` = label key + section + term + model.prompt | reaction text, assertion type, population, **exact quote** + position, grounding (`exact` / `case_insensitive` / `not_found`) |

- **Model:** Claude Sonnet 5.5, `ri.language-model-service..language-model.anthropic-claude-5-5-sonnet`, via `GenericCompletionLanguageModelInput`. The model must be **imported into the project**: type the RID inline inside the Input call in Code Repositories, pick it from the dropdown, then click Import.
- **Libraries:** `palantir_models`, `language-model-service-api`.
- **Cache:** `@incremental` + previous output. Change `PROMPT_VERSION` / `PARSER_VERSION` / `MODEL_ID` to force fresh calls.
- **Local test:** `.venv/bin/python foundry/tools/local_run/check_extraction.py` (fake model). Gold score: `check_gold.py <labeled_reactions.jsonl>`.
