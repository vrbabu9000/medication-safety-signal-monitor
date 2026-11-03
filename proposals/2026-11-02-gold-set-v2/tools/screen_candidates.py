"""Screen candidate NDA brand products: does every one of the 8 sources return usable evidence?

Usage: python3 screen_candidates.py <cache_dir>
Writes ../screening/screening-report.json (every candidate, kept or rejected, with the reason).
Screening reads live sources through a disk cache; it does not create frozen evidence.
"""
import json
import sys
import v2lib as L

CACHE = sys.argv[1]

# (brand, class). A purposive pool across classes; NDA small molecules only (Drugs@FDA does not hold BLAs).
POOL = [
    ("Xarelto", "anticoagulant"), ("Eliquis", "anticoagulant"), ("Pradaxa", "anticoagulant"), ("Plavix", "antiplatelet"), ("Brilinta", "antiplatelet"),
    ("Lipitor", "statin"), ("Crestor", "statin"), ("Zocor", "statin"), ("Vytorin", "statin combination"),
    ("Jardiance", "SGLT2"), ("Farxiga", "SGLT2"), ("Invokana", "SGLT2"),
    ("Ozempic", "GLP-1"), ("Victoza", "GLP-1"), ("Rybelsus", "GLP-1"), ("Januvia", "DPP-4"), ("Janumet", "DPP-4 combination"),
    ("Glucophage", "biguanide"), ("Actos", "thiazolidinedione"),
    ("OxyContin", "opioid"), ("Percocet", "opioid combination"), ("Ultram", "opioid"), ("Nucynta", "opioid"), ("Belbuca", "opioid"),
    ("Lamictal", "antiepileptic"), ("Keppra", "antiepileptic"), ("Topamax", "antiepileptic"), ("Depakote", "antiepileptic"), ("Lyrica", "antiepileptic"),
    ("Zoloft", "SSRI"), ("Lexapro", "SSRI"), ("Paxil", "SSRI"), ("Cymbalta", "SNRI"), ("Effexor XR", "SNRI"), ("Wellbutrin XL", "antidepressant"),
    ("Cipro", "fluoroquinolone"), ("Levaquin", "fluoroquinolone"), ("Avelox", "fluoroquinolone"), ("Augmentin", "antibiotic combination"), ("Zithromax", "macrolide"),
    ("Seroquel", "antipsychotic"), ("Abilify", "antipsychotic"), ("Zyprexa", "antipsychotic"), ("Risperdal", "antipsychotic"), ("Latuda", "antipsychotic"),
    ("Nexium", "PPI"), ("Protonix", "PPI"), ("Prilosec", "PPI"),
    ("Diovan", "ARB"), ("Cozaar", "ARB"), ("Benicar", "ARB"), ("Entresto", "ARB combination"), ("Zestril", "ACE inhibitor"), ("Norvasc", "calcium channel blocker"),
    ("Lasix", "loop diuretic"), ("Synthroid", "thyroid"), ("Singulair", "leukotriene antagonist"), ("Chantix", "smoking cessation"),
    ("Truvada", "antiretroviral combination"), ("Xeljanz", "JAK inhibitor"), ("Ambien", "hypnotic"), ("Adderall XR", "stimulant"),
]


def jget(u, **kw):
    f = L.fetch(u, cache_dir=CACHE, **kw)
    return (f.json() if f.ok and f.status == 200 else None), f


def screen(brand, klass):
    r = {"brand": brand, "class": klass, "checks": {}, "reasons": []}
    c = r["checks"]
    # S1 RxNorm: brand concept and its ingredients
    d, _ = jget(L.url(L.RXNAV + "/rxcui.json", {"name": brand, "search": "0"}))
    ids = (d or {}).get("idGroup", {}).get("rxnormId") or []
    if not ids:
        r["reasons"].append("RxNorm: brand name not found"); return r
    bn = ids[0]
    d, _ = jget(f"{L.RXNAV}/rxcui/{bn}/related.json?tty=IN")
    ins = sorted({(p["rxcui"], p["name"]) for g in (d or {}).get("relatedGroup", {}).get("conceptGroup", []) or []
                  for p in g.get("conceptProperties", []) or []}, key=lambda x: x[1])
    c["rxnorm"] = {"brand_rxcui": bn, "ingredients": ins}
    if not ins:
        r["reasons"].append("RxNorm: no IN relationship"); return r
    # S2 NDC: original-packager, finished, NDA listings for the brand
    d, _ = jget(L.url(L.OPENFDA + "/ndc.json", {"search": f'brand_name:"{brand}" AND marketing_category:"NDA" AND finished:true', "limit": "100"}))
    prods = [p for p in (d or {}).get("results", []) if (p.get("openfda", {}).get("is_original_packager") or [False])[0]
             and p.get("brand_name", "").lower() == brand.lower() and p.get("packaging")]
    if not prods:
        r["reasons"].append("NDC: no original-packager NDA listing with this exact brand"); return r
    apps = {}
    for p in prods:
        apps.setdefault(p["application_number"], []).append(p)
    app = max(apps, key=lambda a: len(apps[a]))
    prod = sorted(apps[app], key=lambda p: p["product_ndc"])[0]
    c["ndc"] = {"application_number": app, "product_ndc": prod["product_ndc"], "labeler": prod["labeler_name"],
                "spl_set_id": (prod.get("openfda", {}).get("spl_set_id") or [None])[0], "n_products": len(apps[app])}
    # S3 Drugs@FDA
    d, _ = jget(L.url(L.OPENFDA + "/drugsfda.json", {"search": f'application_number:"{app}"', "limit": "1"}))
    if not d or not d.get("results"):
        r["reasons"].append("Drugs@FDA: application not found"); return r
    c["drugsfda"] = {"sponsor": d["results"][0].get("sponsor_name"), "n_products": len(d["results"][0].get("products", []))}
    # S4 DailyMed
    sid = c["ndc"]["spl_set_id"]
    d, _ = jget(f"{L.DAILYMED}/spls/{sid}/history.json") if sid else (None, None)
    hist = ((d or {}).get("data") or {}).get("history") or []
    if not hist:
        r["reasons"].append("DailyMed: no SPL history for NDC spl_set_id"); return r
    c["dailymed"] = {"set_id": sid, "latest_version": hist[0].get("spl_version"), "published": hist[0].get("published_date")}
    # S5 SrLC: row whose application number matches; header guard on the detail page
    L.srlc_session()
    f = L.fetch(L.SRLC + "?event=searchResult.page", data={"drug_name": brand, "TextSearch": ""}, browser=True, cache_dir=CACHE)
    rows = [x for x in L.srlc_search_rows(f.text()) if x["appl_no"].lstrip("0") == app[3:].lstrip("0")] if f.ok else []
    if not rows:
        r["reasons"].append("SrLC: no row with matching application number"); return r
    f = L.fetch(f"{L.SRLC}?event=searchdetail.page&DrugNameID={rows[0]['drug_name_id']}", browser=True, cache_dir=CACHE)
    head = L.srlc_header(f.text()) if f.ok else None
    if not head or head["appl_no"].lstrip("0") != app[3:].lstrip("0"):
        r["reasons"].append(f"SrLC: identity guard failed (page says {head})"); return r
    ents = L.srlc_entries(f.text())
    with_und = [e for e in ents if any(ss["underlined"] for s in e["sections"] for ss in s["subsections"]
                                       if s["section"][:1] in ("4", "5", "6") or s["section"].startswith("Boxed"))]
    c["srlc"] = {"drug_name_id": rows[0]["drug_name_id"], "header": head, "n_entries": len(ents),
                 "n_entries_with_underlined_4_5_6": len(with_und), "latest": ents[0]["date"] if ents else None}
    if not with_und:
        r["reasons"].append("SrLC: no entry with underlined text in sections 4/5/6/Boxed"); return r
    # S6 FAERS: FAERS-coded active substance for reports naming the brand, then the saved-query total
    lo, hi = L.FAERS_WINDOW
    d, _ = jget(L.url(L.OPENFDA + "/event.json", {"search": f'patient.drug.medicinalproduct.exact:"{brand.upper()}" AND receivedate:[{lo} TO {hi}]',
                                                  "count": "patient.drug.activesubstance.activesubstancename.exact", "limit": "5"}))
    subs = (d or {}).get("results") or []
    if not subs:
        r["reasons"].append("FAERS: no reports naming the brand in window"); return r
    sub = subs[0]["term"]
    d, _ = jget(L.url(L.OPENFDA + "/event.json", {"search": L.faers_substance_query(sub), "limit": "0"}))  # total only, no records
    total = (d or {}).get("meta", {}).get("results", {}).get("total", 0)
    c["faers"] = {"active_substance": sub, "reports_in_window": total}
    if total < 100:
        r["reasons"].append(f"FAERS: only {total} reports in window"); return r
    # S7 Enforcement: application-level first, then ingredient-level
    d, _ = jget(L.url(L.OPENFDA + "/enforcement.json", {"search": f'openfda.application_number:"{app}"', "limit": "1"}))
    app_n = (d or {}).get("meta", {}).get("results", {}).get("total", 0)
    q = " AND ".join(f'openfda.generic_name:"{n}"' for _, n in ins)
    d, _ = jget(L.url(L.OPENFDA + "/enforcement.json", {"search": q, "limit": "1"}))
    ing_n = (d or {}).get("meta", {}).get("results", {}).get("total", 0)
    c["enforcement"] = {"app_level_records": app_n, "ingredient_level_records": ing_n}
    if not (app_n or ing_n):
        r["reasons"].append("Enforcement: no recall record for application or ingredient"); return r
    # S8 ClinicalTrials.gov: completed studies with posted results
    d, _ = jget(L.url(L.CTGOV + "/studies", {"query.intr": " AND ".join(n for _, n in ins), "filter.overallStatus": "COMPLETED",
                                             "aggFilters": "results:with", "countTotal": "true", "pageSize": "1", "fields": "NCTId"}))
    c["ctgov"] = {"studies_with_results": (d or {}).get("totalCount", 0)}
    if not c["ctgov"]["studies_with_results"]:
        r["reasons"].append("ClinicalTrials.gov: no completed study with results"); return r
    r["eligible"] = True
    return r


if __name__ == "__main__":
    out = []
    for brand, klass in POOL:
        try:
            r = screen(brand, klass)
        except Exception as e:
            r = {"brand": brand, "class": klass, "reasons": [f"screen error: {type(e).__name__}: {e}"]}
        r.setdefault("eligible", False)
        out.append(r)
        print(f"{'OK ' if r['eligible'] else 'NO '} {brand:14} {klass:22} {'; '.join(r['reasons'])}", flush=True)
    p = L.ROOT / "screening"
    p.mkdir(exist_ok=True)
    (p / "screening-report.json").write_text(json.dumps({
        "generated_at_utc": L.now_utc(), "openfda_api_key_used": bool(L.api_key()), "faers_window": L.FAERS_WINDOW,
        "rule": "Eligible only if all 8 sources return usable evidence; see screen() in tools/screen_candidates.py",
        "candidates": out}, indent=1))
    print("eligible:", sum(r["eligible"] for r in out), "of", len(out))
