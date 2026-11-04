"""Score step 7 extraction output against the frozen pilot gold set.

    .venv/bin/python foundry/tools/local_run/check_gold.py path/to/labeled_reactions.jsonl [--strict]

Input: rows of ontology_labeled_reactions (label_key, section_code, normalized_term, grounding), e.g. exported from Foundry SQL.
Recall = gold items found / gold items. "Extra" = extracted terms that match no gold item; they are listed for a human to judge
(a true reaction the gold set missed, a process item such as REMS, or a wrong extraction), so precision here is an upper bound.
"""
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
gold = json.load(open(os.path.join(ROOT, "eval/gold-set/step7-pilot-gold-v1.json")))
rows = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
STRICT = "--strict" in sys.argv  # strict: the extracted term must equal a variant (atomic terms, as FAERS matching needs)
by_section = defaultdict(list)
for r in rows:
    by_section[(r["label_key"], r["section_code"])].append(r)


def matches(term, variants):
    if STRICT:
        return term in variants
    return any(v == term or v in term or term in v for v in variants)


tot_gold = tot_found = 0
for label_key, lab in gold["labels"].items():
    for code, sec in lab["sections"].items():
        got = by_section.get((label_key, code), [])
        terms = [g["normalized_term"] for g in got]
        found = [it["id"] for it in sec["items"] if any(matches(t, it["variants"]) for t in terms)]
        missed = [it["id"] for it in sec["items"] if it["id"] not in found]
        extra = [t for t in terms if not any(matches(t, it["variants"]) for it in sec["items"])]
        ungrounded = [g["normalized_term"] for g in got if g["grounding"] == "not_found"]
        tot_gold += len(sec["items"])
        tot_found += len(found)
        print(f"{label_key[:8]} {sec['name']:<18} recall {len(found)}/{len(sec['items'])}  extracted {len(terms)}  ungrounded {len(ungrounded)}")
        if missed:
            print("    missed:", missed)
        if extra:
            print("    extra (judge by hand):", extra)
        if ungrounded:
            print("    ungrounded:", ungrounded)
print(f"\nOverall recall on gold sections: {tot_found}/{tot_gold} = {tot_found / tot_gold:.2f}")
print(f"Grounding over ALL extracted rows: {sum(r['grounding'] != 'not_found' for r in rows)}/{len(rows)}")
