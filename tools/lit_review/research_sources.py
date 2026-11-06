"""Multi-source evidence for one drug–event signal (AI literature review F01, run v2).

Adds three public sources to the PubMed fetcher (fetch_evidence.py):
  1. Europe PMC  — papers + preprints, free REST API, no key.          Q1 "is there published evidence?"
  2. FDA Potential Signals (AEMS/FAERS quarterly postings), HTML pages. Q2 "is FDA already looking at it?"
  3. OnSIDES v3.1.1 (CC BY 4.0) — label side effects, US/EU/UK/JP.      Q4 "is it on a label anywhere?"

    python3 tools/lit_review/research_sources.py fda-cache   <dir>        # once: all quarterly pages → <dir>/fda_signals.json
    python3 tools/lit_review/research_sources.py onsides-cache <csv_dir> <dir>  # once: our 13 drugs → <dir>/onsides_13.json
    python3 tools/lit_review/research_sources.py run <cache_dir>          # every sample in SAMPLES → evidence/<id>-v2.json
"""
import csv
import html
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/12-features/ai-literature-review/evidence"
FORMULARY = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol",
             "semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]  # D018, same list as raw_dailymed_spl.py
BRANDS = {"semaglutide": ["ozempic", "wegovy", "rybelsus"], "tirzepatide": ["mounjaro", "zepbound"],
          "liraglutide": ["victoza", "saxenda"], "dulaglutide": ["trulicity"], "exenatide": ["byetta", "bydureon"],
          "buprenorphine": ["suboxone", "sublocade", "brixadi", "butrans", "belbuca"], "fentanyl": ["duragesic", "actiq", "fentora"]}
CLASS = {"glp1": ["glp-1", "glucagon-like peptide"], "opioid": ["opioid"]}
GLP1 = {"semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"}

# id, drug, FAERS preferred term, terms that count as "the event" (match is case-insensitive substring), Europe PMC query
SAMPLES = [
    ("01-semaglutide-naion", "semaglutide", "Optic ischaemic neuropathy",
     ["optic ischaemic neuropathy", "optic ischemic neuropathy", "ischemic optic neuropathy", "ischaemic optic neuropathy", "naion"],
     'semaglutide AND ("ischemic optic neuropathy" OR "ischaemic optic neuropathy" OR NAION)'),
    ("02-semaglutide-cyclic-vomiting", "semaglutide", "Cyclic vomiting syndrome", ["cyclic vomiting", "cyclical vomiting"],
     '(semaglutide OR "GLP-1") AND ("cyclic vomiting" OR "cyclical vomiting")'),
    ("03-fentanyl-anaesthetic-neuro", "fentanyl", "Anaesthetic complication neurological",
     ["anaesthetic complication neurological", "anesthetic complication neurological"],
     'fentanyl AND (anesthesia OR anaesthesia) AND ("neurological complication" OR "neurologic complication")'),
    ("04-tirzepatide-allodynia", "tirzepatide", "Allodynia",
     ["allodynia", "dysaesthesia", "dysesthesia", "hyperaesthesia", "hyperesthesia", "skin pain", "skin sensitivity"],
     'tirzepatide AND (allodynia OR dysesthesia OR dysaesthesia OR hyperesthesia OR hyperaesthesia OR "skin pain" OR "skin sensitivity")'),
    ("05-morphine-ewing", "morphine", "Ewing's sarcoma", ["ewing"], 'morphine AND "Ewing sarcoma"'),
    ("06-buprenorphine-sma-syndrome", "buprenorphine", "Superior mesenteric artery syndrome",
     ["superior mesenteric artery syndrome"], '(buprenorphine OR opioid) AND "superior mesenteric artery syndrome"'),
]


def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; medication-safety-signal-monitor)"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2)


def text(cell):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", cell)).split())


# ---------- 2. FDA Potential Signals ----------
FDA_INDEX = ["https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/new-safety-information-or-potential-signals-serious-risks-identified-fda-adverse-event-monitoring",
             "https://www.fda.gov/drugs/fda-adverse-event-reporting-system-faers/potential-signals-serious-risksnew-safety-information-identified-fda-adverse-event-reporting-system-0"]


def fda_cache(cache):
    links = {}
    for idx in FDA_INDEX:
        for href, label in re.findall(r'href="([^"]+)"[^>]*>\s*([A-Z][a-z]+\s*-\s*[A-Z][a-z]+\s*20\d\d)\s*<', fetch(idx)):
            links[" ".join(label.split())] = urllib.parse.urljoin("https://www.fda.gov", href)
    rows = []
    for quarter, url in sorted(links.items()):
        time.sleep(0.5)
        page = fetch(url)
        for table in re.findall(r"<table.*?</table>", page, re.S):
            for tr in re.findall(r"<tr.*?</tr>", table, re.S):
                cells = [text(c) for c in re.findall(r"<td.*?</td>", tr, re.S)]
                if len(cells) >= 2:
                    rows.append({"quarter": quarter, "product": cells[0], "signal": cells[1],
                                 "status": cells[2] if len(cells) > 2 else "", "url": url})
    pathlib.Path(cache).mkdir(parents=True, exist_ok=True)
    (pathlib.Path(cache) / "fda_signals.json").write_text(json.dumps({"pages": len(links), "rows": rows}, indent=1))
    print(f"FDA: {len(links)} quarterly pages, {len(rows)} rows")


def drug_names(drug):
    return [drug] + BRANDS.get(drug, []) + CLASS["glp1" if drug in GLP1 else "opioid"]


def fda_lookup(rows, drug, terms):
    names = drug_names(drug)
    for_drug = [r for r in rows if any(n in r["product"].lower() for n in names)]
    hits = [r for r in for_drug if any(t in r["signal"].lower() for t in terms)]
    return {"rows_for_drug_or_class": len(for_drug), "event_hits": hits,
            "drug_or_class_rows": [f'{r["quarter"]}: {r["product"][:60]} → {r["signal"][:90]}' for r in for_drug]}


# ---------- 3. OnSIDES ----------
def onsides_cache(csv_dir, cache):
    d = pathlib.Path(csv_dir)
    rd = lambda f: csv.DictReader(open(d / f, encoding="utf-8"))
    ingr = {r["rxnorm_id"]: r["rxnorm_name"].lower() for r in rd("vocab_rxnorm_ingredient.csv") if r["rxnorm_name"].lower() in FORMULARY}
    prod2drug = {}
    for r in rd("vocab_rxnorm_ingredient_to_product.csv"):
        if r["ingredient_id"] in ingr:
            prod2drug.setdefault(r["product_id"], set()).add(ingr[r["ingredient_id"]])
    label2drug = {}
    for r in rd("product_to_rxnorm.csv"):
        for g in prod2drug.get(r["rxnorm_product_id"], ()):
            label2drug.setdefault(r["label_id"], set()).add(g)
    region = {r["label_id"]: r["source"] for r in rd("product_label.csv") if r["label_id"] in label2drug}
    meddra = {r["meddra_id"]: r["meddra_name"] for r in rd("vocab_meddra_adverse_effect.csv")}
    out = {g: {} for g in FORMULARY}  # drug → effect → {region: n_labels, sections}
    for r in rd("product_adverse_effect.csv"):
        lid = r["product_label_id"]
        if lid not in label2drug:
            continue
        name = meddra.get(r["effect_meddra_id"], r["effect_meddra_id"])
        for g in label2drug[lid]:
            e = out[g].setdefault(name, {"regions": {}, "sections": []})
            e["regions"][region[lid]] = e["regions"].get(region[lid], 0) + 1
            if r["label_section"] not in e["sections"]:
                e["sections"].append(r["label_section"])
    labels = {g: {} for g in FORMULARY}
    for lid, gs in label2drug.items():
        for g in gs:
            labels[g][region.get(lid, "?")] = labels[g].get(region.get(lid, "?"), 0) + 1
    high = {(ingr[r["ingredient_id"]], meddra.get(r["effect_meddra_id"], "")) for r in rd("high_confidence.csv") if r["ingredient_id"] in ingr}
    pathlib.Path(cache).mkdir(parents=True, exist_ok=True)
    (pathlib.Path(cache) / "onsides_13.json").write_text(json.dumps(
        {"version": "v3.1.1", "labels": labels, "effects": out, "high_confidence": sorted(map(list, high))}, indent=1))
    print("OnSIDES labels per drug:", {g: labels[g] for g in FORMULARY})


def onsides_lookup(db, drug, terms):
    eff = db["effects"][drug]
    hits = {name: v for name, v in eff.items() if any(t in name.lower() for t in terms)}
    high = [e for g, e in db["high_confidence"] if g == drug and any(t in e.lower() for t in terms)]
    return {"labels_by_region": db["labels"][drug], "matching_effects": hits, "high_confidence_matches": high}


# ---------- 1. Europe PMC ----------
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def epmc(query, drug, terms, top=10):
    q = lambda extra, size, kind: json.loads(fetch(EPMC + "?" + urllib.parse.urlencode(
        {"query": query + extra, "format": "json", "pageSize": size, "resultType": kind})))
    core = q("", top, "core")
    pre = q(" AND SRC:PPR", 1, "lite")["hitCount"]
    papers = []
    names = [drug] + BRANDS.get(drug, [])
    for r in core["resultList"]["result"]:
        types = r.get("pubTypeList", {}).get("pubType", [])
        ab = (r.get("abstractText") or "")
        blob = (r.get("title", "") + " " + ab).lower()
        papers.append({"id": r.get("pmid") or r.get("id"), "source": r.get("source"), "year": r.get("pubYear"),
                       "title": r.get("title", "")[:200], "pubtype": types, "open_access": r.get("isOpenAccess") == "Y",
                       "retracted": any("retract" in t.lower() for t in types),
                       "drug_and_event_in_abstract": any(n in blob for n in names) and any(t in blob for t in terms),
                       "abstract": re.sub(r"<[^>]+>", "", ab)[:1500]})
    return {"query": query, "hits": core["hitCount"], "preprints": pre, "papers": papers}


def run(cache):
    fda = json.loads((pathlib.Path(cache) / "fda_signals.json").read_text())
    ons = json.loads((pathlib.Path(cache) / "onsides_13.json").read_text())
    for sid, drug, pt, terms, query in SAMPLES:
        t0 = time.time()
        old = OUT / f"{sid}.json"
        pubmed = json.loads(old.read_text()) if old.exists() else None
        e = epmc(query, drug, terms)
        kept = [p for p in e["papers"] if p["drug_and_event_in_abstract"] and not p["retracted"]]
        res = {"id": sid, "drug": drug, "faers_pt": pt, "event_terms": terms,
               "pubmed_v1": {"hits": pubmed["hits"], "pmids": [p["pmid"] for p in pubmed["papers"]]} if pubmed else "see sample 01 page",
               "europe_pmc": e,
               "new_vs_pubmed": [p["id"] for p in kept if pubmed and p["id"] not in {x["pmid"] for x in pubmed["papers"]}],
               "fda_potential_signals": fda_lookup(fda["rows"], drug, terms),
               "onsides": onsides_lookup(ons, drug, terms),
               "metrics": {"seconds": round(time.time() - t0, 1), "api_calls": 2,
                           "abstract_chars_kept": sum(len(p["abstract"]) for p in kept),
                           "approx_tokens_kept": sum(len(p["abstract"]) for p in kept) // 4,
                           "papers_kept": len(kept), "papers_dropped_gate": len(e["papers"]) - len(kept)}}
        (OUT / f"{sid}-v2.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        f, o = res["fda_potential_signals"], res["onsides"]
        print(f"\n== {sid}  EPMC hits={e['hits']} preprints={e['preprints']} kept={len(kept)} new_vs_pubmed={len(res['new_vs_pubmed'])}"
              f"  FDA rows(drug/class)={f['rows_for_drug_or_class']} FDA event hits={len(f['event_hits'])}"
              f"  OnSIDES matches={ {k: v['regions'] for k, v in o['matching_effects'].items()} } high={o['high_confidence_matches']}")
        for p in kept[:6]:
            print("  ", p["id"], p["source"], p["year"], "|", p["title"][:100])
        for h in f["event_hits"]:
            print("   FDA:", h["quarter"], h["product"][:60], "→", h["signal"][:100], "|", h["status"][:80])


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"fda-cache": lambda: fda_cache(sys.argv[2]), "onsides-cache": lambda: onsides_cache(sys.argv[2], sys.argv[3]),
     "run": lambda: run(sys.argv[2])}[cmd]()
