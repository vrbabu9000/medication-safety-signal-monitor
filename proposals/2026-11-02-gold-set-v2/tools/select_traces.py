"""Turn the screening report into ../traces.json: 30 eligible products, at most 3 per class, Chantix first (pilot).

Kept S4 inputs ({ordinal, target}) already present in traces.json are preserved on re-run.
"""
import json
import v2lib as L

PILOT = "Chantix"
# Eligible but left out, with the reason (recorded in traces.json).
LEFT_OUT = {"Actos": "weakest SrLC evidence (1 entry with underlined text) and fewest FAERS reports",
            "Zestril": "weakest SrLC evidence (1 entry with underlined text)",
            "Invokana": "third SGLT2; fewest FAERS reports in class",
            "Latuda": "third antipsychotic; fewest FAERS reports in class",
            "Zocor": "simvastatin is already covered by Vytorin; Lipitor covers statins"}

rep = json.loads((L.ROOT / "screening" / "screening-report.json").read_text())
old = {}
p = L.ROOT / "traces.json"
if p.exists():
    old = {t["brand"]: t for t in json.loads(p.read_text())["traces"]}
el = [c for c in rep["candidates"] if c["eligible"] and c["brand"] not in LEFT_OUT]
el.sort(key=lambda c: (c["brand"] != PILOT,))
assert len(el) == 30, len(el)
traces = []
for i, c in enumerate(el, 1):
    k = c["checks"]
    t = {"trace_id": f"T{i:02d}", "brand": c["brand"], "class": c["class"],
         "application_number": k["ndc"]["application_number"], "product_ndc": k["ndc"]["product_ndc"],
         "spl_set_id": k["ndc"]["spl_set_id"], "srlc_drug_name_id": k["srlc"]["drug_name_id"]}
    if c["brand"] in old and old[c["brand"]].get("s4"):
        t["s4"] = old[c["brand"]]["s4"]
    traces.append(t)
p.write_text(json.dumps({"dataset_id": "MSSM-30-v2", "selection_rule": "Eligible in screening (all 8 sources usable), at most 3 per class; pilot first",
                         "left_out_eligible": LEFT_OUT, "traces": traces}, indent=1) + "\n")
print("\n".join(f"{t['trace_id']} {t['brand']:10} {t['class']}" for t in traces))
