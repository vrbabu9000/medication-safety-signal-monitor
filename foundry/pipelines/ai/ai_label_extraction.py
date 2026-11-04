# AI label extraction (step 7): an AIP language model lists the reactions each safety section of a label mentions, with an exact quote.
# Contract: docs/04-architecture/foundry-conventions/conventions-v1.md §8. Rules: D005 (call the model only for a new cache key),
# grounding = the quote must occur in the exact section text, failures stay explicit and retryable, nothing here means "label does not mention it".
# Pilot sample (step 7): the labels in PILOT_SETIDS only; widen after the gold set check.
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/ai_label_extraction.py
import hashlib
import json
import re
import time
from datetime import datetime, timezone

import polars as pl
from language_model_service_api.languagemodelservice_api_completion_v3 import GenericCompletionRequest
from palantir_models.transforms import GenericCompletionLanguageModelInput
from transforms.api import Input, Output, incremental, transform

CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
CURATED = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/"
MODEL_ID = "claude-sonnet-5.5"
PROMPT_VERSION = "p1"
PARSER_VERSION = "x1"
# OxyContin v44 (modern PLR label, reference trace T13) and one older-format oxycodone/acetaminophen generic reference label.
PILOT_SETIDS = ["bfdfe235-d717-4855-a3c8-a13d26dadede", "cc966d57-7cdc-4de3-bbcf-718e2fce9cb7"]
ASSERTION_TYPES = {"adverse_reaction", "warning_risk", "contraindication_condition", "other"}
CACHEABLE = {"ok", "empty"}  # parse_error and model_error are retried on the next build

SYSTEM = (
    "You extract safety information from ONE section of a US drug label (FDA SPL). "
    "Use only the text given. Never add knowledge from outside the text. Answer with JSON only."
)
USER = """Label section: {section_name} ({section_code}) of "{title}".

List every adverse reaction, adverse event or safety risk that this section says the drug can cause, or that is
reported with the drug. In a Contraindications section, list the patient conditions instead.

For each item return:
- "reaction": the reaction or condition, worded as in the text, as short as possible (e.g. "respiratory depression").
- "quote": an exact copy of the words in the text that state it (max 300 characters). Copy, do not paraphrase.
- "assertion_type": one of "adverse_reaction" (observed/reported reaction, e.g. trial or postmarketing lists),
  "warning_risk" (a risk the label warns about), "contraindication_condition", "other".
- "population": who it affects if the text names someone other than the patient (e.g. "neonates"), else null.

List each distinct reaction once. If the section mentions none, return an empty list.
Return exactly: {{"reactions": [{{"reaction": "...", "quote": "...", "assertion_type": "...", "population": null}}]}}

SECTION TEXT:
<<<
{text}
>>>"""

EXTRACTION_SCHEMA = {"cache_key": pl.Utf8, "setid": pl.Utf8, "spl_version": pl.Int64, "label_key": pl.Utf8, "section_code": pl.Utf8,
                     "section_name": pl.Utf8, "content_sha256": pl.Utf8, "model_id": pl.Utf8, "prompt_version": pl.Utf8, "parser_version": pl.Utf8,
                     "status": pl.Utf8, "error_text": pl.Utf8, "n_reactions": pl.Int64, "n_grounded": pl.Int64, "raw_response": pl.Utf8,
                     "prompt_tokens": pl.Int64, "completion_tokens": pl.Int64, "latency_ms": pl.Int64, "called_at": pl.Utf8,
                     "from_cache": pl.Boolean, "built_at": pl.Utf8}
REACTION_SCHEMA = {"labeled_reaction_key": pl.Utf8, "cache_key": pl.Utf8, "label_key": pl.Utf8, "setid": pl.Utf8, "spl_version": pl.Int64,
                   "section_code": pl.Utf8, "section_name": pl.Utf8, "normalized_term": pl.Utf8, "reaction_text": pl.Utf8,
                   "assertion_type": pl.Utf8, "population": pl.Utf8, "quote": pl.Utf8, "quote_start": pl.Int64, "grounding": pl.Utf8,
                   "term_in_quote": pl.Boolean, "n_mentions": pl.Int64, "model_id": pl.Utf8, "prompt_version": pl.Utf8}

_PUNCT = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def flat(s):
    return re.sub(r"\s+", " ", (s or "").translate(_PUNCT)).strip()


def norm_term(s):
    return re.sub(r"[^a-z0-9]+$|^[^a-z0-9]+", "", flat(s).lower())


def cache_key(setid, version, section_code, content_sha256):
    parts = [setid, str(version), section_code, content_sha256, PARSER_VERSION, PROMPT_VERSION, MODEL_ID]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


def parse_response(text):
    """Return (status, items, error). Strict: JSON object with a 'reactions' list of dicts."""
    body = re.sub(r"^```(?:json)?\s*|\s*```$", "", (text or "").strip())
    try:
        data = json.loads(body)
        items = data["reactions"]
        if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
            raise ValueError("reactions is not a list of objects")
    except (ValueError, KeyError, TypeError) as e:
        return "parse_error", [], str(e)[:500]
    return ("ok" if items else "empty"), items, None


def ground(items, section_text):
    """One row per distinct normalized term. Grounding: exact (after whitespace/quote cleanup), case_insensitive, or not_found."""
    text = flat(section_text)
    low = text.lower()
    out = {}
    for it in items:
        reaction, quote = flat(str(it.get("reaction") or "")), flat(str(it.get("quote") or ""))
        term = norm_term(reaction)
        if not term:
            continue
        pos = text.find(quote) if quote else -1
        grounding = "exact" if pos >= 0 else ("case_insensitive" if quote and low.find(quote.lower()) >= 0 else "not_found")
        if grounding == "case_insensitive":
            pos = low.find(quote.lower())
        a_type = it.get("assertion_type") if it.get("assertion_type") in ASSERTION_TYPES else "other"
        row = out.get(term)
        if row is None or (row["grounding"] == "not_found" and grounding != "not_found"):
            out[term] = {"normalized_term": term, "reaction_text": reaction, "assertion_type": a_type,
                         "population": it.get("population") or None, "quote": quote, "quote_start": pos if pos >= 0 else None,
                         "grounding": grounding, "term_in_quote": term in quote.lower(), "n_mentions": (row or {}).get("n_mentions", 0) + 1}
        else:
            row["n_mentions"] += 1
    return list(out.values())


def complete(model, system, user):
    # Generic completion API, as in the Model Catalog sample for this model: one prompt string in, completion text out.
    resp = model.create_completion(GenericCompletionRequest(system + "\n\n" + user))
    usage = getattr(resp, "token_usage", None)
    return resp.completion, getattr(usage, "prompt_tokens", None), getattr(usage, "completion_tokens", None)


def extract_sections(sections, titles, previous, call, built_at):
    """Pure logic (tested locally): reuse cached results for unchanged cache keys, call the model for the rest, ground every quote."""
    ext_rows, rx_rows = [], []
    for s in sorted(sections, key=lambda r: (r["setid"], r["section_code"])):
        sha = hashlib.sha256(s["section_text"].encode()).hexdigest()
        key = cache_key(s["setid"], s["spl_version"], s["section_code"], sha)
        label_key = f"{s['setid']}|v{s['spl_version']}"
        prev = previous.get(key)
        if prev and prev["status"] in CACHEABLE:
            row = dict(prev, from_cache=True, built_at=built_at)
        else:
            started, err, raw, ptok, ctok = time.time(), None, None, None, None
            try:
                raw, ptok, ctok = call(SYSTEM, USER.format(section_name=s["section_name"], section_code=s["section_code"],
                                                           title=titles.get(s["setid"], ""), text=s["section_text"]))
            except Exception as e:  # model or quota errors stay visible and are retried on the next build
                err = f"{type(e).__name__}: {e}"[:1000]
            row = {"cache_key": key, "setid": s["setid"], "spl_version": int(s["spl_version"]), "label_key": label_key,
                   "section_code": s["section_code"], "section_name": s["section_name"], "content_sha256": sha, "model_id": MODEL_ID,
                   "prompt_version": PROMPT_VERSION, "parser_version": PARSER_VERSION, "raw_response": raw, "prompt_tokens": ptok,
                   "completion_tokens": ctok, "latency_ms": int((time.time() - started) * 1000), "called_at": built_at,
                   "from_cache": False, "built_at": built_at, "status": "model_error" if err else None, "error_text": err}
        if row["status"] == "model_error":
            status, items, perr = "model_error", [], row["error_text"]
        else:
            status, items, perr = parse_response(row["raw_response"])
        grounded = ground(items, s["section_text"])
        row.update(status=status, error_text=perr, n_reactions=len(grounded), n_grounded=sum(g["grounding"] != "not_found" for g in grounded))
        ext_rows.append(row)
        for g in grounded:
            rx_rows.append(dict(g, labeled_reaction_key=f"{label_key}|{s['section_code']}|{g['normalized_term']}|{MODEL_ID}.{PROMPT_VERSION}",
                                cache_key=key, label_key=label_key, setid=s["setid"], spl_version=int(s["spl_version"]),
                                section_code=s["section_code"], section_name=s["section_name"], model_id=MODEL_ID, prompt_version=PROMPT_VERSION))
    return ext_rows, rx_rows


@incremental(semantic_version=1, snapshot_inputs=["sections", "versions"])
@transform.using(extractions=Output(CURATED + "ai_label_section_extractions"), reactions=Output(CURATED + "ontology_labeled_reactions"),
                 sections=Input(CLEAN + "clean_label_sections"), versions=Input(CLEAN + "clean_label_versions"),
                 model=GenericCompletionLanguageModelInput("ri.language-model-service..language-model.anthropic-claude-5-5-sonnet"))
def compute(extractions, reactions, sections, versions, model):
    built_at = datetime.now(timezone.utc).isoformat()
    titles = dict(versions.polars(mode="current").select("setid", "title").iter_rows())
    try:
        previous = {r["cache_key"]: r for r in extractions.polars(mode="previous").to_dicts()}
    except Exception:  # first build: there is no previous output yet, so nothing is cached
        previous = {}
    todo = sections.polars(mode="current").filter(pl.col("setid").is_in(PILOT_SETIDS)).to_dicts()
    ext_rows, rx_rows = extract_sections(todo, titles, previous, lambda sy, us: complete(model, sy, us), built_at)
    extractions.set_mode("replace")
    reactions.set_mode("replace")
    extractions.write_table(pl.DataFrame(ext_rows, schema=EXTRACTION_SCHEMA))
    reactions.write_table(pl.DataFrame(rx_rows, schema=REACTION_SCHEMA))
