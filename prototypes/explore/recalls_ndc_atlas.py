"""Recalls + NDC Directory atlas: measure the recall data and the NDC files for our 13 ingredients.

Every number in docs/07-data-quality/atlas/enforcement.html and ndc-directory.html comes from this script.

Input : downloaded with --download into prototypes/data/_recalls/dl (zips) and x (unzipped)
        - openFDA bulk drug/enforcement (all drug recalls) and drug/ndc
        - FDA NDC Directory text files: ndctext, ndc_unfinished, ndc_excluded, compounders_ndc_directory
        - earlier API samples in prototypes/data/<drug>/recalls_sample.json (snapshot compare)
Calls : RxNav ndcstatus (NDC -> RxNorm) and approximateTerm (text fallback). Cached in _recalls/rxnav_cache.json.
Output: prototypes/data/_recalls/atlas_results.json (+ printed summary)
Run   : python3 -I prototypes/explore/recalls_ndc_atlas.py [--download]
"""
import collections as C, concurrent.futures as cf, csv, datetime as dt, json, os, re, statistics, sys
import time, urllib.parse, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "data", "_recalls")
DL, X = os.path.join(BASE, "dl"), os.path.join(BASE, "x")
CACHE = os.path.join(BASE, "rxnav_cache.json")
OUT = os.path.join(BASE, "atlas_results.json")
AS_OF = dt.date(2026, 10, 20)  # day of this run; ages are measured to here

OURS = ["buprenorphine", "fentanyl", "hydrocodone", "hydromorphone", "methadone", "morphine",
        "oxycodone", "tramadol", "semaglutide", "liraglutide", "dulaglutide", "exenatide", "tirzepatide"]
# Word-boundary match: keeps apomorphine out of morphine, levomethadone out of methadone.
ING_RX = re.compile(r"\b(" + "|".join(OURS) + r")\b", re.I)
BRANDS = {"ozempic": "semaglutide", "wegovy": "semaglutide", "rybelsus": "semaglutide", "victoza": "liraglutide",
          "saxenda": "liraglutide", "trulicity": "dulaglutide", "mounjaro": "tirzepatide", "zepbound": "tirzepatide",
          "byetta": "exenatide", "bydureon": "exenatide", "oxycontin": "oxycodone", "percocet": "oxycodone",
          "roxicodone": "oxycodone", "norco": "hydrocodone", "vicodin": "hydrocodone", "dilaudid": "hydromorphone",
          "duragesic": "fentanyl", "suboxone": "buprenorphine", "subutex": "buprenorphine", "ultram": "tramadol",
          "dolophine": "methadone"}
BRAND_RX = re.compile(r"\b(" + "|".join(BRANDS) + r")\b", re.I)
COMPOUND_RX = re.compile(r"compound|outsourc|503\s*b|admixture|pharmacy|pharmedium|quva|nephron sterile", re.I)
REASONS = [  # first match wins; order = clinical severity, then the rest
    ("sterility / contamination", r"steril|microb|contamin|mold|fung|bacteri|endotoxin|yeast"),
    ("particulate / foreign matter", r"particul|glass|foreign|fiber"),
    ("potency (sub/super)", r"potenc|subpotent|superpotent|assay|content uniformity|strength"),
    ("impurity / degradation", r"impurit|nitrosamin|degrad|unknown peak"),
    ("dissolution", r"dissolution"),
    ("labeling / mix-up", r"label|mix.?up|wrong|incorrect|missing"),
    ("container / packaging", r"leak|seal|container|packag|crack|closure|vial"),
    ("cGMP deviations", r"cgmp|good manufacturing"),
]
FILES = {
    "drug-enforcement-0001-of-0001.json.zip": "https://download.open.fda.gov/drug/enforcement/drug-enforcement-0001-of-0001.json.zip",
    "drug-ndc-0001-of-0001.json.zip": "https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip",
    "ndctext.zip": "https://www.accessdata.fda.gov/cder/ndctext.zip",
    "ndc_unfinished.zip": "https://www.accessdata.fda.gov/cder/ndc_unfinished.zip",
    "ndc_excluded.zip": "https://www.accessdata.fda.gov/cder/ndc_excluded.zip",
    "compounders_ndc_directory.zip": "https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip",
}


def download():
    os.makedirs(DL, exist_ok=True); os.makedirs(X, exist_ok=True)
    for name, url in FILES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (signal-monitor research)"})
        with urllib.request.urlopen(req, timeout=600) as r, open(os.path.join(DL, name), "wb") as f:
            f.write(r.read())
        with zipfile.ZipFile(os.path.join(DL, name)) as z:
            for m in z.namelist():
                if not m.endswith(".xls"):
                    z.extract(m, X)
        print("downloaded", name)


def pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def d8(s):
    try:
        return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except (ValueError, TypeError, IndexError):
        return None


def read_tsv(name):
    # FDA NDC text files are tab-separated and NOT valid UTF-8 (stray Latin-1 bytes); read as Latin-1.
    with open(os.path.join(X, name), encoding="latin-1", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def bad_utf8_lines(name):
    n = 0
    with open(os.path.join(X, name), "rb") as f:
        for line in f:
            try:
                line.decode("utf-8")
            except UnicodeDecodeError:
                n += 1
    return n


# ---------- NDC parsing ----------
SHAPES = {(4, 4, 2): "4-4-2 (10-digit)", (5, 3, 2): "5-3-2 (10-digit)", (5, 4, 1): "5-4-1 (10-digit)",
          (5, 4, 2): "5-4-2 (11-digit)"}
DASH3 = re.compile(r"(?<![\d-])(\d{4,5})-(\d{3,4})-(\d{1,2})(?![\d-])")
NDC_CTX = re.compile(r"NDC[\s#:.,No()]*", re.I)


def norm3(a, b, c):
    shape = (len(a), len(b), len(c))
    if shape == (4, 4, 2): return "0" + a + b + c
    if shape == (5, 3, 2): return a + "0" + b + c
    if shape == (5, 4, 1): return a + b + "0" + c
    if shape == (5, 4, 2): return a + b + c
    return None


def norm_prod(a, b):
    shape = (len(a), len(b))
    if shape == (4, 4): return "0" + a + b
    if shape == (5, 3): return a + "0" + b
    if shape == (5, 4): return a + b
    return None


def extract_ndcs(text):
    """Return list of dicts: {raw, shape, keys(list of 11-digit candidates) or prod9, ctx(bool NDC keyword)}."""
    out, used = [], []
    for m in DASH3.finditer(text):
        a, b, c = m.groups()
        shape = SHAPES.get((len(a), len(b), len(c)), "odd %d-%d-%d" % (len(a), len(b), len(c)))
        k = norm3(a, b, c)
        ctx = bool(re.search(r"NDC", text[max(0, m.start() - 25):m.start()], re.I))
        out.append({"raw": m.group(0), "shape": shape, "keys": [k] if k else [], "prod9": None, "ctx": ctx})
        used.append((m.start(), m.end()))
    for m in NDC_CTX.finditer(text):  # forms only trusted after the word NDC
        rest = text[m.end():m.end() + 20]
        if any(s <= m.end() < e for s, e in used):
            continue
        mm = re.match(r"(\d{10,11})(?!\d)", rest)
        if mm:
            s = mm.group(1)
            if len(s) == 11:
                out.append({"raw": s, "shape": "11 digits, no dashes", "keys": [s], "prod9": None, "ctx": True})
            else:
                out.append({"raw": s, "shape": "10 digits, no dashes (ambiguous)",
                            "keys": ["0" + s, s[:5] + "0" + s[5:], s[:9] + "0" + s[9]], "prod9": None, "ctx": True})
            continue
        mm = re.match(r"(\d{4,5})-(\d{3,4})(?![\d-])", rest)
        if mm and not any(s <= m.end() + 1 < e for s, e in used):
            p = norm_prod(*mm.groups())
            out.append({"raw": mm.group(0), "shape": "product code only (2 segments)", "keys": [],
                        "prod9": p, "ctx": True})
    return out


# ---------- expiry parsing in code_info ----------
MON = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
EXP_RX = re.compile(r"(?:exp\w*|bud|beyond use date|use by)\.?\s*(?:date|dates)?\s*[:#.\-]?\s*", re.I)


def parse_date_token(s):
    s = s.strip()
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", s)
    if m:
        mo, d, y = map(int, m.groups()); y += 2000 if y < 100 else 0
        try: return dt.date(y, mo, d)
        except ValueError: return None
    m = re.match(r"(\d{1,2})/(\d{2,4})(?!\d)", s)
    if m:
        mo, y = map(int, m.groups()); y += 2000 if y < 100 else 0
        if 1 <= mo <= 12 and 2000 <= y <= 2040:
            return (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1))
        return None
    m = re.match(r"(\d{4})-(\d{1,2})(?:-(\d{1,2}))?", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return dt.date(y, mo, int(m.group(3))) if m.group(3) else dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1)
    m = re.match(r"(\d{1,2})[\- ]([A-Za-z]{3})[a-z]*[\- ,]+(\d{2,4})", s)
    if m and m.group(2).lower() in MON:
        y = int(m.group(3)); y += 2000 if y < 100 else 0
        try: return dt.date(y, MON[m.group(2).lower()], int(m.group(1)))
        except ValueError: return None
    m = re.match(r"([A-Za-z]{3})[a-z]*\.?[\s,]+(\d{4})", s)
    if m and m.group(1).lower() in MON:
        mo, y = MON[m.group(1).lower()], int(m.group(2))
        return dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1)
    return None


def expiries(code_info):
    out = []
    for m in EXP_RX.finditer(code_info or ""):
        tail = code_info[m.end():m.end() + 40]
        for tok in re.split(r"\s*(?:-|to|and|through|,)\s*(?=\d|[A-Z][a-z]{2})", tail)[:2]:
            d = parse_date_token(tok)
            if d and 2005 <= d.year <= 2040:
                out.append(d)
    return out


# ---------- RxNav ----------
def load_cache():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def rxnav(cache, key, url):
    if key in cache:
        return cache[key]
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                cache[key] = json.load(r)
                return cache[key]
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    cache[key] = {"error": True}
    return cache[key]


def ndcstatus_many(cache, ndcs):
    todo = [n for n in sorted(set(ndcs)) if "ndc:" + n not in cache]
    print(f"  RxNav ndcstatus: {len(ndcs)} NDCs, {len(todo)} not cached", flush=True)

    def one(n):
        time.sleep(0.25)
        return rxnav(cache, "ndc:" + n, "https://rxnav.nlm.nih.gov/REST/ndcstatus.json?ndc=" + n)
    with cf.ThreadPoolExecutor(4) as ex:
        list(ex.map(one, todo))
    with open(CACHE, "w") as f:
        json.dump(cache, f)


def ndc_rx(cache, n):
    s = (cache.get("ndc:" + n) or {}).get("ndcStatus") or {}
    return {"status": s.get("status") or "ERROR", "rxcui": s.get("rxcui") or "", "name": s.get("conceptName") or ""}


# ---------- main ----------
def main():
    if "--download" in sys.argv:
        download()
    R = {"as_of": str(AS_OF)}
    cache = load_cache()

    # ===== NDC Directory files =====
    prod = read_tsv("product.txt"); pkg = read_tsv("package.txt")
    unf_p = read_tsv("unfinished_product.txt"); unf_k = read_tsv("unfinished_package.txt")
    exc_p = read_tsv("Products_excluded.txt"); exc_k = read_tsv("Packages_excluded.txt")
    comp = read_tsv("compounders_ndc_directory.txt")
    with open(os.path.join(X, "drug-ndc-0001-of-0001.json")) as f:
        ofda_ndc = json.load(f)
    nd = R["ndc_dir"] = {}
    nd["files"] = {n: {"rows": len(r), "non_utf8_lines": bad_utf8_lines(f)} for n, r, f in [
        ("product.txt", prod, "product.txt"), ("package.txt", pkg, "package.txt"),
        ("unfinished_product.txt", unf_p, "unfinished_product.txt"), ("unfinished_package.txt", unf_k, "unfinished_package.txt"),
        ("Products_excluded.txt", exc_p, "Products_excluded.txt"), ("Packages_excluded.txt", exc_k, "Packages_excluded.txt"),
        ("compounders_ndc_directory.txt", comp, "compounders_ndc_directory.txt")]}
    nd["files"]["openFDA drug-ndc json"] = {"rows": len(ofda_ndc["results"]), "last_updated": ofda_ndc["meta"]["last_updated"]}

    def ours_in(*vals):
        return sorted({m.lower() for v in vals for m in ING_RX.findall(v or "")})

    # Index: 11-digit package NDC -> info; 9-digit product -> info; 5-digit labeler -> name.
    pk_idx, pr_idx, lab_idx = {}, {}, {}

    def add(prows, krows, src, flag_field=None):
        pinfo = {}
        for r in prows:
            a, b = r["PRODUCTNDC"].split("-") if "-" in r["PRODUCTNDC"] else (None, None)
            p9 = norm_prod(a, b) if a else None
            info = {"src": src, "product_ndc": r["PRODUCTNDC"], "appno": r.get("APPLICATIONNUMBER", ""),
                    "category": r.get("MARKETINGCATEGORYNAME", ""), "labeler": r.get("LABELERNAME", ""),
                    "substance": r.get("SUBSTANCENAME", ""), "name": r.get("PROPRIETARYNAME") or r.get("NONPROPRIETARYNAME", ""),
                    "flag": r.get(flag_field, "") if flag_field else "", "end": r.get("ENDMARKETINGDATE", "")}
            pinfo[r.get("PRODUCTID") or r["PRODUCTNDC"]] = info
            if p9:
                pr_idx.setdefault(p9, info); lab_idx.setdefault(p9[:5], info["labeler"])
        for k in krows:
            parts = k["NDCPACKAGECODE"].split("-")
            if len(parts) != 3:
                continue
            n11 = norm3(*parts)
            info = pinfo.get(k.get("PRODUCTID") or k["PRODUCTNDC"])
            if n11 and info:
                pk_idx.setdefault(n11, dict(info, pkg_flag=k.get("NDC_EXCLUDE_FLAG", ""), pkg_desc=k.get("PACKAGEDESCRIPTION", "")))
    add(prod, pkg, "NDC Directory (listed)", "NDC_EXCLUDE_FLAG")
    add(comp, comp, "Compounders list (503B)")  # one row = one package
    add(unf_p, unf_k, "Unfinished (bulk/API)")
    add(exc_p, exc_k, "Excluded / delisted", "NDC_EXCLUDE_FLAG")

    # Our 13 in each file
    def our_rows(rows):
        return [r for r in rows if ours_in(r.get("SUBSTANCENAME"), r.get("NONPROPRIETARYNAME"), r.get("PROPRIETARYNAME"))]
    op, ou, oe, oc = our_rows(prod), our_rows(unf_p), our_rows(exc_p), our_rows(comp)
    nd["ours"] = {"listed_products": len(op), "unfinished_products": len(ou), "excluded_products": len(oe),
                  "compounder_rows": len(oc), "compounder_products": len({r["PRODUCTNDC"] for r in oc}),
                  "compounder_labelers": len({r["LABELERNAME"] for r in oc})}
    op_ids = {r["PRODUCTID"] for r in op}
    nd["ours"]["listed_packages"] = sum(1 for k in pkg if k["PRODUCTID"] in op_ids)
    nd["ours"]["excluded_packages"] = sum(1 for k in exc_k if k["PRODUCTID"] in {r["PRODUCTID"] for r in oe})
    nd["excluded_name_fill"] = pct(sum(1 for r in exc_p if r.get("SUBSTANCENAME")), len(exc_p))
    nd["excluded_flags"] = C.Counter(r["NDC_EXCLUDE_FLAG"] for r in exc_p).most_common()
    nd["excluded_flags_ours"] = C.Counter(r["NDC_EXCLUDE_FLAG"] for r in oe).most_common()
    per = {}
    for ing in OURS:
        per[ing] = {"listed": sum(1 for r in op if ing in ours_in(r["SUBSTANCENAME"], r["NONPROPRIETARYNAME"])),
                    "unfinished": sum(1 for r in ou if ing in ours_in(r["SUBSTANCENAME"], r["NONPROPRIETARYNAME"])),
                    "excluded": sum(1 for r in oe if ing in ours_in(r["SUBSTANCENAME"], r["NONPROPRIETARYNAME"], r["PROPRIETARYNAME"])),
                    "compounded": len({r["PRODUCTNDC"] for r in oc if ing in ours_in(r["SUBSTANCENAME"], r["NONPROPRIETARYNAME"])})}
    nd["per_ingredient"] = per
    nd["categories_listed"] = C.Counter(r["MARKETINGCATEGORYNAME"] for r in op).most_common()
    nd["categories_unfinished"] = C.Counter(r["MARKETINGCATEGORYNAME"] for r in ou).most_common()
    nd["appno_fill_listed"] = pct(sum(1 for r in op if r["APPLICATIONNUMBER"].strip()), len(op))
    nd["appno_blank_by_cat"] = C.Counter(r["MARKETINGCATEGORYNAME"] for r in op if not r["APPLICATIONNUMBER"].strip()).most_common()
    nd["combo_listed"] = sum(1 for r in op if ";" in r["SUBSTANCENAME"])
    nd["combo_examples"] = C.Counter(r["SUBSTANCENAME"] for r in op if ";" in r["SUBSTANCENAME"]).most_common(6)
    nd["distinct_appnos_listed"] = len({r["APPLICATIONNUMBER"] for r in op if r["APPLICATIONNUMBER"]})
    nd["labelers_listed"] = len({r["LABELERNAME"] for r in op})
    nd["dea_listed"] = C.Counter(r["DEASCHEDULE"] for r in op).most_common()
    nd["listed_flag_ours"] = C.Counter(r["NDC_EXCLUDE_FLAG"] for r in op).most_common()
    nd["end_date_set_listed"] = sum(1 for r in op if r["ENDMARKETINGDATE"])
    nd["end_date_future_listed"] = sum(1 for r in op if r["ENDMARKETINGDATE"] and (d8(r["ENDMARKETINGDATE"]) or AS_OF) > AS_OF)
    nd["certified_through"] = C.Counter(r["LISTING_RECORD_CERTIFIED_THROUGH"][:4] for r in op).most_common()
    nd["comp_periods"] = C.Counter(r["REPORTINGPERIOD"] for r in oc).most_common()
    nd["comp_examples"] = [{k: r[k] for k in ("PRODUCTNDC", "NONPROPRIETARYNAME", "LABELERNAME", "ACTIVEINGREDIENTSINFO",
                                              "NDCPACKAGECODE", "PACKAGEDESCRIPTION", "REPORTINGPERIOD")} for r in oc[:3]]
    nd["sample_excluded"] = [r for r in oe if r["NDC_EXCLUDE_FLAG"] == "D" and "norco" in r["PROPRIETARYNAME"].lower()][:1] + \
                            [r for r in oe if r["NDC_EXCLUDE_FLAG"] == "I"][:1]
    nd["sample_unfinished"] = [r for r in ou if "SEMAGLUTIDE" in r["SUBSTANCENAME"] and "COMPOUNDING" in r["MARKETINGCATEGORYNAME"]][:1]
    nd["sample_compounder"] = [r for r in oc if "SEMAGLUTIDE" in r["SUBSTANCENAME"].upper()][:1]
    nd["comp_in_listed"] = sum(1 for r in oc if norm3(*r["NDCPACKAGECODE"].split("-")) in
                               {norm3(*k["NDCPACKAGECODE"].split("-")) for k in pkg if len(k["NDCPACKAGECODE"].split("-")) == 3})
    # sample real rows
    nd["sample_listed"] = [r for r in op if r["PROPRIETARYNAME"] == "Ozempic"][:2] + \
                          [r for r in op if r["SUBSTANCENAME"].startswith("OXYCODONE HYDROCHLORIDE") and r["MARKETINGCATEGORYNAME"] == "ANDA"][:1]
    nd["sample_packages"] = [k for k in pkg if k["PRODUCTID"] in {r["PRODUCTID"] for r in nd["sample_listed"][:1]}]

    # openFDA json vs FDA text: same data 4 days apart -> measured churn + openfda enrichment fill
    oj = ofda_ndc["results"]
    oj_ours = [r for r in oj if ours_in(r.get("generic_name"), " ".join(a.get("name", "") for a in r.get("active_ingredients", [])))]
    oj_fin = [r for r in oj_ours if r.get("finished")]
    nd["openfda_json"] = {"ours_total": len(oj_ours), "ours_finished": len(oj_fin),
                          "rxcui_fill_finished": pct(sum(1 for r in oj_fin if r.get("openfda", {}).get("rxcui")), len(oj_fin)),
                          "setid_fill_finished": pct(sum(1 for r in oj_fin if r.get("openfda", {}).get("spl_set_id")), len(oj_fin)),
                          "appno_fill_finished": pct(sum(1 for r in oj_fin if r.get("application_number")), len(oj_fin)),
                          "openfda_empty_finished": sum(1 for r in oj_fin if not r.get("openfda"))}
    txt_ids = {r["PRODUCTID"] for r in prod} | {r["PRODUCTID"] for r in unf_p}
    js_ids = {r["product_id"] for r in oj}
    nd["churn_json_vs_txt"] = {"json_date": ofda_ndc["meta"]["last_updated"], "txt_date": "2026-10-20",
                               "in_txt_not_json": len(txt_ids - js_ids), "in_json_not_txt": len(js_ids - txt_ids),
                               "ours_in_txt_not_json": sum(1 for r in op + ou if r["PRODUCTID"] not in js_ids),
                               "ours_in_json_not_txt": sum(1 for r in oj_ours if r["product_id"] not in txt_ids)}
    txt_ndc = {r["PRODUCTNDC"] for r in prod} | {r["PRODUCTNDC"] for r in unf_p}
    js_ndc = {r["product_ndc"] for r in oj}
    nd["churn_json_vs_txt"].update({"product_ndc_new": len(txt_ndc - js_ndc), "product_ndc_gone": len(js_ndc - txt_ndc)})
    # new packages per week (our 13, listed) from STARTMARKETINGDATE
    wk = C.Counter()
    for k in pkg:
        if k["PRODUCTID"] in op_ids:
            d = d8(k["STARTMARKETINGDATE"])
            if d and AS_OF - dt.timedelta(weeks=52) <= d <= AS_OF:
                wk[(d - dt.timedelta(days=d.weekday())).isoformat()] += 1
    nd["new_packages_52w"] = {"total": sum(wk.values()), "weeks_with_any": len(wk), "max_week": max(wk.values()) if wk else 0,
                              "per_week_mean": round(sum(wk.values()) / 52, 1)}

    # ===== Recalls =====
    with open(os.path.join(X, "drug-enforcement-0001-of-0001.json")) as f:
        enf = json.load(f)
    allrec = enf["results"]
    rec = [x for x in allrec if ING_RX.search(x["product_description"])]
    brand_only = [x for x in allrec if not ING_RX.search(x["product_description"]) and BRAND_RX.search(x["product_description"])]
    E = R["enforcement"] = {"meta_last_updated": enf["meta"]["last_updated"], "all_records": len(allrec),
                            "ours": len(rec), "events": len({x["event_id"] for x in rec}),
                            "brand_only_extra": len(brand_only),
                            "brand_only_examples": [x["product_description"][:140] for x in brand_only[:3]],
                            "apomorphine_excluded": sum(1 for x in allrec if re.search(r"apomorphine", x["product_description"], re.I)),
                            "report_date_range": [min(x["report_date"] for x in allrec), max(x["report_date"] for x in allrec)]}
    for x in rec:
        x["_ings"] = sorted({m.lower() for m in ING_RX.findall(x["product_description"])})
        x["_combo"] = bool(re.search(r"\band\b|/|\+|with", x["product_description"].split(",")[0], re.I)) and \
            bool(re.search(r"bupivacaine|ropivacaine|acetaminophen|naloxone|midazolam|ketamine|clonidine|cyanocobalamin|"
                           r"pyridoxine|glycine|ibuprofen|aspirin|promethazine|guaifenesin|homatropine|chlorpheniramine",
                           x["product_description"], re.I))
        x["_comp_text"] = bool(COMPOUND_RX.search(x["product_description"] + " " + x["recalling_firm"]))
        x["_reason"] = next((n for n, p in REASONS if re.search(p, x["reason_for_recall"], re.I)), "other")
        x["_init"] = d8(x["recall_initiation_date"]); x["_rep"] = d8(x["report_date"]); x["_term"] = d8(x.get("termination_date", ""))
        x["_ndcs"] = extract_ndcs(x["product_description"])
        x["_exp"] = expiries(x.get("code_info", "") + " " + x.get("more_code_info", ""))
    E["openfda_filled"] = sum(1 for x in rec if x["openfda"]); E["openfda_filled_all"] = sum(1 for x in allrec if x["openfda"])
    E["openfda_filled_ongoing"] = sum(1 for x in rec if x["openfda"] and x["status"] == "Ongoing")
    E["status"] = C.Counter(x["status"] for x in rec).most_common()
    E["class"] = C.Counter(x["classification"] for x in rec).most_common()
    E["class_by_status"] = {s: C.Counter(x["classification"] for x in rec if x["status"] == s).most_common() for s in ("Ongoing", "Completed", "Terminated")}
    E["year_init"] = sorted(C.Counter(x["_init"].year for x in rec if x["_init"]).items())
    E["reason"] = C.Counter(x["_reason"] for x in rec).most_common()
    E["reason_ongoing"] = C.Counter(x["_reason"] for x in rec if x["status"] == "Ongoing").most_common()
    E["voluntary"] = C.Counter(x["voluntary_mandated"] for x in rec).most_common()
    E["combo"] = sum(1 for x in rec if x["_combo"])
    E["multi_ing_ours"] = sum(1 for x in rec if len(x["_ings"]) > 1)
    E["top_firms"] = C.Counter(x["recalling_firm"] for x in rec).most_common(8)
    E["top_firms_ongoing"] = C.Counter(x["recalling_firm"] for x in rec if x["status"] == "Ongoing").most_common(8)
    E["products_per_event"] = {"max": max(C.Counter(x["event_id"] for x in rec).values()),
                               "events_with_1": sum(1 for v in C.Counter(x["event_id"] for x in rec).values() if v == 1),
                               "top": [(ev, n, next(x["recalling_firm"] for x in rec if x["event_id"] == ev))
                                       for ev, n in C.Counter(x["event_id"] for x in rec).most_common(3)],
                               "event_99505": sum(1 for x in rec if x["event_id"] == "99505")}

    # compounded: by text vs by NDC in compounders list vs labeler in compounders list
    comp_labelers = {norm3(*r["NDCPACKAGECODE"].split("-"))[:5] for r in comp if len(r["NDCPACKAGECODE"].split("-")) == 3}
    for x in rec:
        keys = [k for n in x["_ndcs"] for k in n["keys"]] + [n["prod9"] for n in x["_ndcs"] if n["prod9"]]
        x["_comp_lab"] = any(k[:5] in comp_labelers for k in keys)
        x["_compounded"] = x["_comp_text"] or x["_comp_lab"]
    E["compounded"] = {"by_text": sum(1 for x in rec if x["_comp_text"]), "by_labeler_in_503b_list": sum(1 for x in rec if x["_comp_lab"]),
                       "either": sum(1 for x in rec if x["_compounded"]), "both": sum(1 for x in rec if x["_comp_text"] and x["_comp_lab"]),
                       "ongoing_either": sum(1 for x in rec if x["_compounded"] and x["status"] == "Ongoing")}

    per_ing = {}
    for ing in OURS:
        rr = [x for x in rec if ing in x["_ings"]]
        per_ing[ing] = {"recalls": len(rr), "events": len({x["event_id"] for x in rr}),
                        "ongoing": sum(1 for x in rr if x["status"] == "Ongoing"),
                        "class1": sum(1 for x in rr if x["classification"] == "Class I"),
                        "compounded": sum(1 for x in rr if x["_compounded"]),
                        "with_ndc": sum(1 for x in rr if x["_ndcs"]),
                        "since_2024": sum(1 for x in rr if x["_init"] and x["_init"].year >= 2024)}
    E["per_ingredient"] = per_ing

    # ===== Q2 NDC extraction =====
    E["ndc"] = {"with_any": sum(1 for x in rec if x["_ndcs"]),
                "with_ndc_word": sum(1 for x in rec if re.search(r"NDC", x["product_description"], re.I)),
                "ndc_word_but_none_parsed": [x["product_description"][-120:] for x in rec
                                            if re.search(r"NDC", x["product_description"], re.I) and not x["_ndcs"]][:5],
                "ndc_word_but_none_parsed_n": sum(1 for x in rec if re.search(r"NDC", x["product_description"], re.I) and not x["_ndcs"]),
                "shapes": C.Counter(n["shape"] for x in rec for n in x["_ndcs"]).most_common(),
                "no_ndc_word_before": sum(1 for x in rec for n in x["_ndcs"] if not n["ctx"]),
                "ndcs_per_record": C.Counter(min(len(x["_ndcs"]), 5) for x in rec).most_common(),
                "distinct": len({tuple(n["keys"]) or n["prod9"] for x in rec for n in x["_ndcs"]}),
                "with_any_ongoing": sum(1 for x in rec if x["_ndcs"] and x["status"] == "Ongoing"),
                "by_compounded": {"compounded": [sum(1 for x in rec if x["_compounded"] and x["_ndcs"]), sum(1 for x in rec if x["_compounded"])],
                                  "not": [sum(1 for x in rec if not x["_compounded"] and x["_ndcs"]), sum(1 for x in rec if not x["_compounded"])]},
                "no_ndc_examples": [x["product_description"][:150] for x in rec if not x["_ndcs"]][:6],
                "by_year": sorted({y: [sum(1 for x in rec if x["_init"] and x["_init"].year == y and x["_ndcs"]),
                                       sum(1 for x in rec if x["_init"] and x["_init"].year == y)]
                                   for y in range(2012, 2027)}.items())}
    E["appno_in_text"] = sum(1 for x in rec if re.search(r"\b(A?NDA|BLA)\s*#?\s*\d{5,6}", x["product_description"]))

    # ===== Q3 match rates =====
    all_keys = set()
    for x in rec:
        for n in x["_ndcs"]:
            all_keys.update(n["keys"])
    ndcstatus_many(cache, all_keys)
    rx_status = C.Counter()
    for x in rec:
        best_dir, best_rx, hits = None, None, []
        for n in x["_ndcs"]:
            for k in n["keys"]:
                if k in pk_idx:
                    hits.append(("package", pk_idx[k], k))
                r = ndc_rx(cache, k)
                if r["rxcui"] and not best_rx:
                    best_rx = dict(r, ndc=k)
            p9 = n["prod9"] or (n["keys"][0][:9] if len(n["keys"]) == 1 else None)
            if p9 and p9 in pr_idx:
                hits.append(("product", pr_idx[p9], p9))
            elif n["keys"]:
                for k in n["keys"]:
                    if k[:9] in pr_idx:
                        hits.append(("product", pr_idx[k[:9]], k[:9])); break
            lab = (n["keys"][0][:5] if n["keys"] else (n["prod9"] or "")[:5])
            if lab in lab_idx:
                hits.append(("labeler", {"src": "labeler only", "labeler": lab_idx[lab]}, lab))
        order = {"package": 0, "product": 1, "labeler": 2}
        hits.sort(key=lambda h: order[h[0]])
        x["_dir"] = hits[0] if hits else None
        x["_rx"] = best_rx
        for n in x["_ndcs"]:
            for k in n["keys"][:1] if len(n["keys"]) == 1 else []:
                rx_status[ndc_rx(cache, k)["status"]] += 1
    withn = [x for x in rec if x["_ndcs"]]
    lvl = C.Counter((x["_dir"][0] if x["_dir"] else "none") for x in withn)
    src = C.Counter((x["_dir"][1]["src"] if x["_dir"] and x["_dir"][0] != "labeler" else "-") for x in withn)
    dir_ok = [x for x in withn if x["_dir"] and x["_dir"][0] in ("package", "product")]
    ing_agree = sum(1 for x in dir_ok if set(x["_ings"]) & set(ours_in(x["_dir"][1].get("substance"), x["_dir"][1].get("name"))))
    rx_ok = [x for x in withn if x["_rx"]]
    rx_agree = sum(1 for x in rx_ok if any(i in x["_rx"]["name"].lower() for i in x["_ings"]))
    E["match"] = {"records_with_ndc": len(withn),
                  "rxnorm_any_rxcui": len(rx_ok), "rxnorm_ingredient_agrees": rx_agree,
                  "rxnorm_status_per_ndc": rx_status.most_common(),
                  "dir_level": lvl.most_common(), "dir_source": src.most_common(),
                  "dir_ingredient_agrees": ing_agree, "dir_with_appno": sum(1 for x in dir_ok if x["_dir"][1].get("appno")),
                  "dir_appno_examples": C.Counter(x["_dir"][1].get("appno") for x in dir_ok if x["_dir"][1].get("appno")).most_common(5),
                  "rx_or_dir": sum(1 for x in withn if x["_rx"] or (x["_dir"] and x["_dir"][0] in ("package", "product"))),
                  "rx_only": sum(1 for x in withn if x["_rx"] and not (x["_dir"] and x["_dir"][0] in ("package", "product"))),
                  "dir_only": sum(1 for x in withn if not x["_rx"] and x["_dir"] and x["_dir"][0] in ("package", "product"))}
    rx_dis = [x for x in rx_ok if not any(i in x["_rx"]["name"].lower() for i in x["_ings"])]
    E["match"]["rxnorm_disagree_names"] = C.Counter("(blank name)" if not x["_rx"]["name"] else x["_rx"]["name"][:60] for x in rx_dis).most_common(8)
    E["match"]["rxnorm_disagree_blank_name"] = sum(1 for x in rx_dis if not x["_rx"]["name"])
    E["match"]["rxnorm_disagree_examples"] = [{"recall": x["recall_number"], "ndc": x["_rx"]["ndc"], "status": x["_rx"]["status"],
                                               "rxcui": x["_rx"]["rxcui"], "rx_name": x["_rx"]["name"], "text": x["product_description"][:90]}
                                              for x in rx_dis if x["_rx"]["name"]][:6]
    E["match"]["rxnorm_status_of_hit"] = C.Counter(x["_rx"]["status"] for x in rx_ok).most_common()
    dir_dis = [x for x in dir_ok if not set(x["_ings"]) & set(ours_in(x["_dir"][1].get("substance"), x["_dir"][1].get("name")))]
    E["match"]["dir_disagree_examples"] = [{"recall": x["recall_number"], "src": x["_dir"][1]["src"], "dir_name": x["_dir"][1].get("name"),
                                            "dir_sub": x["_dir"][1].get("substance"), "text": x["product_description"][:80]} for x in dir_dis][:6]
    fail = [x for x in withn if not x["_rx"] and not (x["_dir"] and x["_dir"][0] in ("package", "product"))]
    E["match"]["fail_distinct_ndcs"] = len({n["raw"] for x in fail for n in x["_ndcs"]})
    E["match"]["fail_everywhere"] = len(fail)
    E["match"]["fail_compounded"] = sum(1 for x in fail if x["_compounded"])
    E["match"]["fail_ongoing"] = sum(1 for x in fail if x["status"] == "Ongoing")
    E["match"]["fail_labeler_known"] = sum(1 for x in fail if x["_dir"])
    E["match"]["fail_firms"] = C.Counter(x["recalling_firm"] for x in fail).most_common(10)
    E["match"]["fail_examples"] = [{"recall": x["recall_number"], "status": x["status"], "firm": x["recalling_firm"],
                                    "ndc": x["_ndcs"][0]["raw"], "text": x["product_description"][:110]} for x in fail
                                   if x["status"] == "Ongoing"][:8]
    E["match"]["ongoing"] = {"n": sum(1 for x in rec if x["status"] == "Ongoing"),
                             "with_ndc": sum(1 for x in withn if x["status"] == "Ongoing"),
                             "rx": sum(1 for x in rx_ok if x["status"] == "Ongoing"),
                             "rx_or_dir": sum(1 for x in withn if x["status"] == "Ongoing" and (x["_rx"] or (x["_dir"] and x["_dir"][0] in ("package", "product"))))}
    # compounded match split
    E["match"]["by_compounded"] = {k: {"n": len(g), "rx": sum(1 for x in g if x["_rx"]),
                                       "dir": sum(1 for x in g if x["_dir"] and x["_dir"][0] in ("package", "product"))}
                                   for k, g in (("compounded", [x for x in withn if x["_compounded"]]),
                                                ("not compounded", [x for x in withn if not x["_compounded"]]))}

    # text-only fallback: RxNav approximateTerm on the product text (first ~10 words, before the first comma)
    fb = [x for x in rec if not x["_rx"]]
    def term(x):
        t = re.split(r",|\bRx\b|\bNDC\b|\(", x["product_description"])[0]
        return " ".join(t.split()[:10])
    todo = {term(x) for x in fb}
    def at(t):
        time.sleep(0.25)
        return rxnav(cache, "at:" + t, "https://rxnav.nlm.nih.gov/REST/approximateTerm.json?maxEntries=1&term=" + urllib.parse.quote(t))
    print(f"  RxNav approximateTerm: {len(todo)} terms", flush=True)
    with cf.ThreadPoolExecutor(4) as ex:
        list(ex.map(at, sorted(todo)))
    with open(CACHE, "w") as f:
        json.dump(cache, f)
    def at_rxcui(t):
        c = ((cache.get("at:" + t) or {}).get("approximateGroup") or {}).get("candidate") or []
        return c[0] if c else None
    fb_hit = [x for x in fb if at_rxcui(term(x))]
    # name check: resolve candidate rxcui -> name (cached) to see whether our ingredient is in it
    names, hist_status = {}, {}
    for x in fb_hit:
        rc = at_rxcui(term(x))["rxcui"]
        if rc not in names:
            # historystatus also names obsolete concepts (approximateTerm often returns them; property.json does not)
            j = rxnav(cache, "hist:" + rc, f"https://rxnav.nlm.nih.gov/REST/rxcui/{rc}/historystatus.json")
            h = j.get("rxcuiStatusHistory") or {}
            names[rc] = (h.get("attributes") or {}).get("name") or ""
            hist_status[rc] = (h.get("metaData") or {}).get("status") or ""
    with open(CACHE, "w") as f:
        json.dump(cache, f)
    fb_agree = sum(1 for x in fb_hit if any(i in names[at_rxcui(term(x))["rxcui"]].lower() for i in x["_ings"]))

    def first_num(s):
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*(mg|mcg|ml|%)", s, re.I)
        return m.group(1).replace(",", "") if m else None
    agree = [x for x in fb_hit if any(i in names[at_rxcui(term(x))["rxcui"]].lower() for i in x["_ings"])]
    with_num = [x for x in agree if first_num(term(x))]
    E["fallback_strength"] = {"agree_with_strength_in_text": len(with_num),
                              "strength_matches": sum(1 for x in with_num if re.search(r"(?<![\d.])" + re.escape(first_num(term(x))) + r"(?![\d])",
                                                                                         names[at_rxcui(term(x))["rxcui"]])),
                              "ingredient_only_answers": sum(1 for x in agree if names[at_rxcui(term(x))["rxcui"]].lower() in OURS)}
    E["fallback_wrong_examples"] = [{"term": term(x), "rx": names[at_rxcui(term(x))["rxcui"]]} for x in fb_hit
                                    if not any(i in names[at_rxcui(term(x))["rxcui"]].lower() for i in x["_ings"])][:6]
    E["fallback"] = {"records_without_rxnorm_ndc": len(fb), "approx_any": len(fb_hit), "approx_ingredient_agrees": fb_agree,
                     "ingredient_by_regex": sum(1 for x in fb if x["_ings"]),
                     "candidate_status": C.Counter(hist_status.get(at_rxcui(term(x))["rxcui"], "") for x in fb_hit).most_common(),
                     "candidate_source": C.Counter(at_rxcui(term(x)).get("source") for x in fb_hit).most_common(),
                     "examples": [{"term": term(x), "rx": names.get(at_rxcui(term(x))["rxcui"], "")} for x in fb_hit[:6]]}

    # ===== Q4 Active =====
    def age_bucket(days):
        for lim, name in ((90, "< 3 months"), (182, "3–6 months"), (365, "6–12 months"), (730, "1–2 years"),
                          (1095, "2–3 years"), (10 ** 6, "> 3 years")):
            if days < lim:
                return name
    og = [x for x in rec if x["status"] == "Ongoing"]
    ages = [(AS_OF - x["_init"]).days for x in og if x["_init"]]
    rep_ages = [(AS_OF - x["_rep"]).days for x in og if x["_rep"]]
    term_d = [(x["_term"] - x["_init"]).days for x in rec if x["status"] == "Terminated" and x["_term"] and x["_init"]]
    q = lambda v, p: sorted(v)[min(len(v) - 1, int(p * len(v)))] if v else None
    A = E["active"] = {"ongoing": len(og), "age_init_buckets": C.Counter(age_bucket(a) for a in ages).most_common(),
                       "age_report_buckets": C.Counter(age_bucket(a) for a in rep_ages).most_common(),
                       "age_median_days": statistics.median(ages) if ages else None, "age_max_days": max(ages) if ages else None,
                       "oldest": min((x for x in og if x["_init"]), key=lambda x: x["_init"])["recall_number"],
                       "term_days_median": statistics.median(term_d), "term_days_p75": q(term_d, .75), "term_days_p90": q(term_d, .90),
                       "term_days_n": len(term_d),
                       "completed": [{"rn": x["recall_number"], "init": x["recall_initiation_date"], "term": x.get("termination_date", "")}
                                     for x in rec if x["status"] == "Completed"]}
    exp_known = [x for x in og if x["_exp"]]
    all_expired = [x for x in exp_known if max(x["_exp"]) < AS_OF]
    A["expiry_parsed"] = len(exp_known); A["all_lots_expired"] = len(all_expired)
    A["expiry_parse_rate_all"] = pct(sum(1 for x in rec if x["_exp"]), len(rec))
    A["all_lots_text"] = sum(1 for x in og if re.search(r"all lots|all products|within expiry", x.get("code_info", ""), re.I))
    A["older_than_p90_close"] = sum(1 for a in ages if a > q(term_d, .90))
    # proposed rule applied
    def officer_view(x):
        if x["status"] != "Ongoing":
            return "Closed (" + x["status"] + ")"
        if re.search(r"all lots|within expiry", x.get("code_info", ""), re.I):
            return "Active"
        if x["_exp"] and max(x["_exp"]) < AS_OF:
            return "Ongoing, lots expired"
        return "Active"
    def why(x):
        if re.search(r"all lots|within expiry", x.get("code_info", ""), re.I): return "code_info says all lots"
        if x["_exp"]: return "a lot not yet expired" if max(x["_exp"]) >= AS_OF else "every lot expired"
        return "no expiry found"
    A["ongoing_why"] = C.Counter(why(x) for x in og).most_common()
    A["active_age"] = C.Counter(age_bucket((AS_OF - x["_init"]).days) for x in og if officer_view(x) == "Active" and x["_init"]).most_common()
    A["active_old_examples"] = [{"rn": x["recall_number"], "init": x["recall_initiation_date"], "why": why(x), "firm": x["recalling_firm"],
                                 "text": x["product_description"][:70]} for x in og
                                if officer_view(x) == "Active" and x["_init"] and (AS_OF - x["_init"]).days > 1046][:8]
    A["expired_age"] = C.Counter(age_bucket((AS_OF - x["_init"]).days) for x in og if officer_view(x) != "Active" and x["_init"]).most_common()
    A["rule_result"] = C.Counter(officer_view(x) for x in rec).most_common()
    A["rule_active_class1"] = sum(1 for x in rec if officer_view(x) == "Active" and x["classification"] == "Class I")
    A["rule_active_by_ing"] = {i: sum(1 for x in rec if officer_view(x) == "Active" and i in x["_ings"]) for i in OURS}
    A["rule_active_events"] = len({x["event_id"] for x in rec if officer_view(x) == "Active"})
    A["ongoing_examples"] = [{"rn": x["recall_number"], "cls": x["classification"], "init": x["recall_initiation_date"],
                              "firm": x["recalling_firm"], "maxexp": str(max(x["_exp"])) if x["_exp"] else "",
                              "view": officer_view(x), "text": x["product_description"][:90]}
                             for x in sorted(og, key=lambda x: x["_init"] or AS_OF)][:3] + \
                            [{"rn": x["recall_number"], "cls": x["classification"], "init": x["recall_initiation_date"],
                              "firm": x["recalling_firm"], "maxexp": str(max(x["_exp"])) if x["_exp"] else "",
                              "view": officer_view(x), "text": x["product_description"][:90]}
                             for x in sorted(og, key=lambda x: x["_init"] or AS_OF)][-3:]

    # ===== Q5 change rate =====
    def weekly(dates, weeks):
        start = AS_OF - dt.timedelta(weeks=weeks)
        c = C.Counter((d - dt.timedelta(days=d.weekday())) for d in dates if d and start <= d <= AS_OF)
        allw = [start + dt.timedelta(days=7 * i - start.weekday()) for i in range(weeks + 1)]
        series = [c.get(w, 0) for w in allw]
        return {"total": sum(series), "weeks": len(series), "zero_weeks": sum(1 for v in series if v == 0),
                "median": statistics.median(series), "mean": round(sum(series) / len(series), 2), "max": max(series),
                "series": series}
    ch = E["changes"] = {
        "new_52w": weekly([x["_rep"] for x in rec], 52), "new_156w": weekly([x["_rep"] for x in rec], 156),
        "term_52w": weekly([x["_term"] for x in rec], 52),
        "new_events_52w": weekly(list({x["event_id"]: x["_rep"] for x in rec}.values()), 52),
        "all_drugs_new_52w": weekly([d8(x["report_date"]) for x in allrec], 52),
        "report_weekday": C.Counter(x["_rep"].strftime("%a") for x in rec if x["_rep"]).most_common(),
        "lag_init_to_report_median": statistics.median([(x["_rep"] - x["_init"]).days for x in rec if x["_rep"] and x["_init"]]),
        "latest_report": max(x["report_date"] for x in allrec), "latest_report_ours": max(x["report_date"] for x in rec)}
    recent_term = [x for x in rec if x["_term"] and x["_term"] >= AS_OF - dt.timedelta(weeks=52)]
    ch["recent_terminations"] = [{"rn": x["recall_number"], "report_date": x["report_date"], "termination_date": x["termination_date"]}
                                 for x in recent_term]
    ch["terminated_no_date"] = sum(1 for x in rec if x["status"] == "Terminated" and not x["_term"])
    ch["completed_with_term_date"] = sum(1 for x in rec if x["status"] == "Completed" and x["_term"])
    ch["ongoing_with_term_date"] = sum(1 for x in rec if x["status"] == "Ongoing" and x["_term"])
    # snapshot compare: earlier API samples (pulled 2026-10-19/20, API data 2026-10-07) vs bulk (2026-10-14)
    bulk = {x["recall_number"]: x for x in allrec}
    diffs, seen = [], 0
    for ing in OURS:
        p = os.path.join(ROOT, "data", ing, "recalls_sample.json")
        if not os.path.exists(p):
            continue
        with open(p) as f:
            s = json.load(f)
        for r in s.get("results", []):
            seen += 1
            b = bulk.get(r["recall_number"])
            if not b:
                diffs.append((r["recall_number"], "missing in bulk"))
            elif (b["status"], b.get("termination_date", "")) != (r["status"], r.get("termination_date", "")):
                diffs.append((r["recall_number"], f'{r["status"]} -> {b["status"]}'))
    ch["snapshot_compare"] = {"api_records_seen": seen, "diffs": diffs[:20], "n_diffs": len(diffs)}

    # real rows for the page
    def pick(rn):
        x = bulk[rn]
        return {k: x.get(k) for k in ("recall_number", "event_id", "status", "classification", "recalling_firm",
                                      "product_description", "reason_for_recall", "code_info", "recall_initiation_date",
                                      "report_date", "termination_date", "voluntary_mandated", "distribution_pattern", "openfda")}
    sema_og = sorted([x for x in rec if "semaglutide" in x["_ings"] and x["status"] == "Ongoing"], key=lambda x: x["report_date"])
    E["examples"] = {"semaglutide_latest_ongoing": pick(sema_og[-1]["recall_number"]) if sema_og else None,
                     "class1_latest": pick(max((x for x in rec if x["classification"] == "Class I"), key=lambda x: x["report_date"])["recall_number"])}
    for k in ("semaglutide_latest_ongoing", "class1_latest"):
        x = bulk[E["examples"][k]["recall_number"]]
        xr = next(r for r in rec if r["recall_number"] == x["recall_number"])
        E["examples"][k + "_trace"] = {"ndcs": [n["raw"] for n in xr["_ndcs"]],
                                       "dir": (xr["_dir"][0], xr["_dir"][1].get("src"), xr["_dir"][1].get("appno"), xr["_dir"][1].get("labeler")) if xr["_dir"] else None,
                                       "rx": xr["_rx"], "exp": [str(d) for d in xr["_exp"]], "compounded": xr["_compounded"]}

    # NDC Directory -> RxNorm coverage (one package per listed product + every compounder package for our 13)
    listed_one = {}
    for k in pkg:
        if k["PRODUCTID"] in op_ids and k["PRODUCTID"] not in listed_one and len(k["NDCPACKAGECODE"].split("-")) == 3:
            listed_one[k["PRODUCTID"]] = norm3(*k["NDCPACKAGECODE"].split("-"))
    comp_n = {norm3(*r["NDCPACKAGECODE"].split("-")) for r in oc if len(r["NDCPACKAGECODE"].split("-")) == 3}
    unf_one = {}
    ou_ids = {r["PRODUCTID"] for r in ou}
    for k in unf_k:
        if k["PRODUCTID"] in ou_ids and k["PRODUCTID"] not in unf_one and len(k["NDCPACKAGECODE"].split("-")) == 3:
            unf_one[k["PRODUCTID"]] = norm3(*k["NDCPACKAGECODE"].split("-"))
    ndcstatus_many(cache, set(listed_one.values()) | comp_n | set(unf_one.values()))
    def cov(ndcs):
        st = C.Counter(ndc_rx(cache, n)["status"] for n in ndcs)
        return {"n": len(ndcs), "with_rxcui": sum(1 for n in ndcs if ndc_rx(cache, n)["rxcui"]), "status": st.most_common()}
    nd["rxnorm_coverage"] = {"listed (1 pkg per product)": cov(list(listed_one.values())),
                             "compounders (all pkgs)": cov(sorted(comp_n)),
                             "unfinished (1 pkg per product)": cov(list(unf_one.values()))}
    nd["recall_link"] = {"recall_records_ours": len(rec), "matched_to_listed": sum(1 for x in withn if x["_dir"] and x["_dir"][1].get("src") == "NDC Directory (listed)"),
                         "matched_to_compounders": sum(1 for x in withn if x["_dir"] and x["_dir"][1].get("src") == "Compounders list (503B)"),
                         "matched_to_excluded": sum(1 for x in withn if x["_dir"] and x["_dir"][1].get("src") == "Excluded / delisted"),
                         "matched_to_unfinished": sum(1 for x in withn if x["_dir"] and x["_dir"][1].get("src") == "Unfinished (bulk/API)")}

    with open(OUT, "w") as f:
        json.dump(R, f, indent=1, default=str)
    with open(CACHE, "w") as f:
        json.dump(cache, f)
    # printed summary (series trimmed)
    show = json.loads(json.dumps(R, default=str))
    for k in ("new_52w", "new_156w", "term_52w", "new_events_52w", "all_drugs_new_52w"):
        show["enforcement"]["changes"][k].pop("series")
    print(json.dumps(show, indent=1)[:60000])


if __name__ == "__main__":
    main()
