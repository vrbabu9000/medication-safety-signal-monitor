"""Step 4 checks on local outputs: key uniqueness, match counts, and the OxyContin chain (reference trace T13).

    python foundry/tools/local_run/check_identity.py
"""
import collections
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "out")
KEYS = {
    "clean_drug_ingredients": ["ingredient_rxcui"],
    "clean_drug_identity": ["lookup_string"],
    "clean_drug_product_map": ["ingredient_rxcui", "product_key"],
    "clean_drug_package_map": ["package_ndc11"],
    "clean_label_product_map": ["setid", "spl_version", "application_number"],
}


def load(name):
    with open(os.path.join(OUT, name + ".jsonl")) as f:
        return [json.loads(line) for line in f]


data = {name: load(name) for name in KEYS}
print("== key uniqueness")
for name, cols in KEYS.items():
    keys = collections.Counter(tuple(r[c] for c in cols) for r in data[name])
    dupes = [k for k, n in keys.items() if n > 1]
    nulls = sum(1 for k in keys if any(v is None for v in k))
    print(f"  {name}: {len(data[name])} rows, {len(dupes)} duplicate keys, {nulls} keys with nulls" + (f"  e.g. {dupes[:2]}" if dupes else ""))

print("== identity match methods")
for r in data["clean_drug_identity"]:
    print(f"  {r['lookup_string']:<28} -> {r['ingredient_rxcui']!s:<6} {r['match_method']:<20} drugsfda={r['n_drugsfda_products']} ndc={r['n_ndc_products']}")

pm = data["clean_drug_product_map"]
print("== product map:", len(pm), "applications;", collections.Counter(r["application_type"] for r in pm), "; combination:", sum(r["is_combination"] for r in pm), "; marketed:", sum(r["any_marketed"] for r in pm))
pk = data["clean_drug_package_map"]
print("== package map:", collections.Counter(r["product_key_type"] for r in pk), "; ndc11 not normalised:", sum(1 for r in pk if r["package_ndc11"] is None), "; no formulary ingredient:", sum(1 for r in pk if not r["ingredient_rxcuis"]))
lm = data["clean_label_product_map"]
print("== label map:", collections.Counter(r["match_status"] for r in lm), "; owner match:", collections.Counter(r["owner_match"] for r in lm))
apps_with_labels = {r["application_number"] for r in lm if r["application_number"]}
apps = {r["product_key"] for r in pm}
print("   applications with any label:", len(apps & apps_with_labels), "of", len(apps), "; with owner (reference) label:", len({r["application_number"] for r in lm if r["is_reference_label"]} & apps))

print("== OxyContin chain (T13: 7804 -> NDA022272 -> 59011-410-10 -> bfdfe235… v44)")
p = [r for r in pm if r["ingredient_rxcui"] == "7804" and r["product_key"] == "NDA022272"]
k = [r for r in pk if r["package_ndc_printed"] == "59011-410-10"]
lab = [r for r in lm if r["application_number"] == "NDA022272"]
print("  product:", [(r["product_key"], r["sponsor_name"], r["brand_names"]) for r in p])
print("  package:", [(r["package_ndc11"], r["product_key"], r["ingredient_rxcuis"]) for r in k])
print("  labels:", [(r["setid"][:8], r["spl_version"], r["labeler_name"], r["owner_match"], r["is_reference_label"]) for r in lab])
ok = bool(p) and bool(k) and k[0]["product_key"] == "NDA022272" and any(r["setid"].startswith("bfdfe235") and r["spl_version"] == 44 and r["is_reference_label"] for r in lab)
print("  CHAIN OK" if ok else "  CHAIN BROKEN")
