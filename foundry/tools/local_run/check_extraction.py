"""Test the step 7 extraction logic without a real model: cache reuse, grounding, and explicit failures.

    .venv/bin/python foundry/tools/local_run/check_extraction.py

Uses the real OxyContin v44 sections from out/clean_label_sections.jsonl and a fake model that returns:
one true quote, one paraphrased (made-up) quote, and, for one section, broken JSON.
"""
import importlib.util
import json
import os
import sys
import types

import polars as pl

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# Stand-ins for the Foundry-only imports (the logic under test does not use them).
for name in ["language_model_service_api", "language_model_service_api.languagemodelservice_api_completion_v3", "palantir_models",
             "palantir_models.transforms", "transforms", "transforms.api"]:
    sys.modules[name] = types.ModuleType(name)
m = sys.modules
m["language_model_service_api.languagemodelservice_api_completion_v3"].__dict__.update(GenericCompletionRequest=object)
m["palantir_models.transforms"].GenericCompletionLanguageModelInput = lambda rid: rid
m["transforms.api"].__dict__.update(Input=lambda p: p, Output=lambda p: p, incremental=lambda **kw: (lambda f: f),
                                    transform=type("T", (), {"using": staticmethod(lambda **kw: (lambda f: f))}))

spec = importlib.util.spec_from_file_location("ai", os.path.join(ROOT, "foundry/pipelines/ai/ai_label_extraction.py"))
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)

sections = pl.read_ndjson(os.path.join(HERE, "out", "clean_label_sections.jsonl")).filter(pl.col("setid").is_in(ai.PILOT_SETIDS[:1])).to_dicts()
calls = []


def fake_call(system, user):
    calls.append(user[:60])
    if "(34070-3)" in user:  # Contraindications: broken JSON -> parse_error, must be retried next run
        return "Sure! Here are the reactions: [", 10, 5
    text = user.split("<<<", 1)[1]
    true_quote = " ".join(text.split()[5:15])
    return json.dumps({"reactions": [
        {"reaction": "respiratory depression", "quote": true_quote, "assertion_type": "warning_risk", "population": None},
        {"reaction": "made-up reaction", "quote": "this sentence is not in the label at all", "assertion_type": "adverse_reaction"},
        {"reaction": "Respiratory Depression.", "quote": true_quote, "assertion_type": "warning_risk"},  # duplicate after normalising
    ]}), 1000, 200


ext1, rx1 = ai.extract_sections(sections, {}, {}, fake_call, "run1")
n1 = len(calls)
prev = {r["cache_key"]: r for r in ext1}
ext2, rx2 = ai.extract_sections(sections, {}, prev, fake_call, "run2")
n2 = len(calls) - n1

status = {r["section_name"]: r["status"] for r in ext1}
ok = True


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail else ""))


check("one row per section", len(ext1) == len(sections), f"{len(ext1)} sections")
check("first run calls the model once per section", n1 == len(sections), f"{n1} calls")
check("broken JSON is a parse_error, not 'no reactions'", status.get("Contraindications") == "parse_error", str(status))
check("second run: only the failed section is called again", n2 == 1, f"{n2} fresh calls")
check("cached rows are marked from_cache", sum(r["from_cache"] for r in ext2) == len(sections) - 1)
g = pl.DataFrame(rx1)
check("made-up quote is flagged not_found", g.filter(pl.col("normalized_term") == "made-up reaction")["grounding"].to_list() == ["not_found"] * 3)
check("true quote is grounded exactly", set(g.filter(pl.col("normalized_term") == "respiratory depression")["grounding"]) == {"exact"})
check("duplicate terms fold into one row", g.filter(pl.col("normalized_term") == "respiratory depression")["n_mentions"].to_list() == [2, 2, 2])
check("reaction keys unique", g["labeled_reaction_key"].n_unique() == g.height, f"{g.height} rows")
check("schemas match", set(ext1[0]) == set(ai.EXTRACTION_SCHEMA) and set(rx1[0]) == set(ai.REACTION_SCHEMA))
pl.DataFrame(ext1, schema=ai.EXTRACTION_SCHEMA), pl.DataFrame(rx1, schema=ai.REACTION_SCHEMA)
sys.exit(0 if ok else 1)
