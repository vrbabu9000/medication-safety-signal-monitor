"""How much data does each source have for the 13 pilot ingredients?

Usage: python3 -I prototypes/explore/volume_check.py
Live calls to openFDA, DailyMed, ClinicalTrials.gov, RxNav. Standard library only.
Writes prototypes/data/_volume.json (git-ignored) and prints markdown tables.
"""
import datetime as dt
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path


# Pilot ingredients (D014). Keep in sync with pull_all.py.
OPIOIDS = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol"]
GLP1 = ["semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]
FDA = "https://api.fda.gov/drug"
TODAY = dt.date.today()
q = urllib.parse.quote

# MedDRA preferred terms we keep OUT of the clinical ranking (decision D014 focus rule).
ABUSE = {"DRUG DEPENDENCE", "OVERDOSE", "DRUG ABUSE", "INTENTIONAL OVERDOSE", "ACCIDENTAL OVERDOSE",
         "DRUG WITHDRAWAL SYNDROME", "TOXICITY TO VARIOUS AGENTS", "SUBSTANCE USE DISORDER",
         "OPIOID USE DISORDER", "DEPENDENCE", "DRUG ABUSER", "INTENTIONAL PRODUCT MISUSE",
         "DRUG DIVERSION", "COMPLETED SUICIDE", "DEATH", "ACCIDENTAL DEATH"}
LITIGATION = {"EMOTIONAL DISTRESS", "ANHEDONIA", "INJURY", "ANXIETY", "LOSS OF EMPLOYMENT",
              "DRUG INEFFECTIVE", "PAIN"}
PRODUCT_USE = ("PRODUCT ", "OFF LABEL USE", "INCORRECT DOSE", "WRONG ", "EXTRA DOSE", "MEDICATION ERROR",
               "DRUG DOSE OMISSION", "INAPPROPRIATE SCHEDULE", "NO ADVERSE EVENT", "UNDERDOSE")
REPORTER = {"1": "physician", "2": "pharmacist", "3": "other HCP", "4": "lawyer", "5": "consumer"}


def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                time.sleep(0.3)
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:  # openFDA: no matches
                return {}
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None  # failed after retries


def total(d):
    return (d or {}).get("meta", {}).get("results", {}).get("total", 0) if d is not None else None


def counts(d):
    return {str(r["term"]): r["count"] for r in (d or {}).get("results", [])}


def bucket(term):
    if term in ABUSE:
        return "abuse/overdose"
    if term in LITIGATION:
        return "litigation-style"
    if term.startswith(PRODUCT_USE) or any(p in term for p in PRODUCT_USE):
        return "product-use/error"
    return "clinical"


def faers(drug):
    s = f'patient.drug.openfda.generic_name:"{q(drug)}"'
    out = {"total": total(get(f"{FDA}/event.json?search={s}&limit=1"))}
    out["suspect_any"] = total(get(f"{FDA}/event.json?search={s}+AND+patient.drug.drugcharacterization:1&limit=1"))
    out["serious"] = counts(get(f"{FDA}/event.json?search={s}&count=serious"))
    rep = counts(get(f"{FDA}/event.json?search={s}&count=primarysource.qualification"))
    out["reporter"] = {REPORTER.get(k, k): v for k, v in rep.items()}
    days = get(f"{FDA}/event.json?search={s}&count=receivedate") or {}
    years = Counter()
    for r in days.get("results", []):
        years[r["time"][:4]] += r["count"]
    out["by_year"] = dict(sorted(years.items()))
    rx = counts(get(f"{FDA}/event.json?search={s}&count=patient.reaction.reactionmeddrapt.exact&limit=100"))
    b = Counter()
    for term, n in rx.items():
        b[bucket(term)] += n
    out["top100_buckets"] = dict(b)
    out["top_clinical"] = [(t, n) for t, n in rx.items() if bucket(t) == "clinical"][:10]
    return out


def recalls(drug):
    s = f'product_description:"{q(drug)}"'
    since = (TODAY - dt.timedelta(days=365)).strftime("%Y%m%d")
    return {
        "total": total(get(f"{FDA}/enforcement.json?search={s}&limit=1")),
        "status": counts(get(f"{FDA}/enforcement.json?search={s}&count=status.exact")),
        "class": counts(get(f"{FDA}/enforcement.json?search={s}&count=classification.exact")),
        "last_12m": total(get(f"{FDA}/enforcement.json?search={s}+AND+report_date:[{since}+TO+{TODAY:%Y%m%d}]&limit=1")),
    }


def labels(drug):
    base = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={q(drug)}&pagesize=100"
    first = get(base + "&page=1") or {}
    meta = first.get("metadata", {})
    n, pages = meta.get("total_elements"), int(meta.get("total_pages") or 1)
    rows = list(first.get("data", []))
    for p in range(2, min(pages, 15) + 1):
        rows += (get(f"{base}&page={p}") or {}).get("data", [])
    cutoff = TODAY - dt.timedelta(days=30)
    recent = 0
    for r in rows:
        try:
            if dt.datetime.strptime(r["published_date"], "%b %d, %Y").date() >= cutoff:
                recent += 1
        except (KeyError, ValueError):
            pass
    maxv = max((int(r.get("spl_version") or 0) for r in rows), default=0)
    return {"total": n, "scanned": len(rows), "updated_last_30d": recent, "max_version": maxv}


def trials(drug):
    d = get(f"https://clinicaltrials.gov/api/v2/studies?query.intr={q(drug)}&aggFilters=results:with&countTotal=true&pageSize=1")
    return {"with_results": (d or {}).get("totalCount")}


def rxcui(drug):
    d = get(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={q(drug)}") or {}
    return (d.get("idGroup", {}).get("rxnormId") or [None])[0]


def main():
    res = {}
    for drug in OPIOIDS + GLP1:
        print(f"checking {drug} ...", flush=True)
        res[drug] = {"class": "opioid" if drug in OPIOIDS else "GLP-1", "rxcui": rxcui(drug),
                     "faers": faers(drug), "recalls": recalls(drug), "labels": labels(drug), "trials": trials(drug)}
    meta = get(f"{FDA}/event.json?limit=1") or {}
    res["_meta"] = {"run_date": str(TODAY), "faers_last_updated": meta.get("meta", {}).get("last_updated"),
                    "faers_all_reports": total(meta)}
    out = Path(__file__).resolve().parents[1] / "data" / "_volume.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2))
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
