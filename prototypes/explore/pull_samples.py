"""Pull small samples from each public source for hand exploration.

Usage:
    python3 prototypes/explore/pull_samples.py               # default drug: oxycodone
    python3 prototypes/explore/pull_samples.py fentanyl

Writes JSON/XML to prototypes/data/<drug>/ (git-ignored). Standard library only.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

DRUG = (sys.argv[1] if len(sys.argv) > 1 else "oxycodone").lower()
OUT = Path(__file__).resolve().parents[1] / "data" / DRUG
OUT.mkdir(parents=True, exist_ok=True)

FDA = "https://api.fda.gov/drug"
DM = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
RX = "https://rxnav.nlm.nih.gov/REST"
q = urllib.parse.quote


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def save(name, url, is_json=True):
    try:
        body = fetch(url)
    except Exception as e:  # keep going; note the failure
        print(f"  FAIL {name}: {e}")
        return None
    path = OUT / name
    if is_json:
        data = json.loads(body)
        path.write_text(json.dumps(data, indent=2))
    else:
        data = body
        path.write_bytes(body)
    print(f"  ok   {name}")
    time.sleep(0.3)  # be polite to public APIs
    return data


gen = f'patient.drug.openfda.generic_name:"{q(DRUG)}"'
print(f"FAERS ({DRUG})")
save("faers_top_reactions.json", f"{FDA}/event.json?search={gen}&count=patient.reaction.reactionmeddrapt.exact&limit=100")
save("faers_sample_reports.json", f"{FDA}/event.json?search={gen}&limit=100")
save("faers_by_receivedate.json", f"{FDA}/event.json?search={gen}&count=receivedate")

print("Enforcement (recalls)")
pd = f'product_description:"{q(DRUG)}"'
save("recalls_by_class.json", f"{FDA}/enforcement.json?search={pd}&count=classification.exact")
save("recalls_by_status.json", f"{FDA}/enforcement.json?search={pd}&count=status.exact")
save("recalls_sample.json", f"{FDA}/enforcement.json?search={pd}&limit=100")

print("DailyMed (labels)")
labels = save("dailymed_labels.json", f"{DM}/spls.json?drug_name={q(DRUG)}&pagesize=100")
if labels and labels.get("data"):
    setid = labels["data"][0]["setid"]
    save("dailymed_first_label.xml", f"{DM}/spls/{setid}.xml", is_json=False)
    save("dailymed_first_label_history.json", f"{DM}/spls/{setid}/history.json")
save("openfda_label_sample.json", f'{FDA}/label.json?search=openfda.generic_name:"{q(DRUG)}"&limit=5')

print("RxNorm")
ids = save("rxnorm_rxcui.json", f"{RX}/rxcui.json?name={q(DRUG)}")
rxcui = (ids or {}).get("idGroup", {}).get("rxnormId", [None])[0]
if rxcui:
    save("rxnorm_related.json", f"{RX}/rxcui/{rxcui}/related.json?tty=IN+PIN+BN+SCD+SBD")
save("rxclass_opioids_atc_N02A.json", f"{RX}/rxclass/classMembers.json?classId=N02A&relaSource=ATC")

print("ClinicalTrials.gov")
save("trials_with_results.json", f"https://clinicaltrials.gov/api/v2/studies?query.intr={q(DRUG)}&aggFilters=results:with&pageSize=20")

print(f"\nDone. Files in {OUT}")
