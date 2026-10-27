"""Identity atlas: how well RxNorm and Drugs@FDA reach Drug and Product for our 13 ingredients.

Measures (all on the 2 bulk FAERS quarters, 2026 Q1 + Q2):
  1. RxNorm   : every prod_ai string for our 13 -> ingredient RxCUI (exact, raw and after salt strip).
  2. Drugs@FDA: FAERS nda_num -> application -> brand / product / sponsor. Reach rate, misses, by ingredient.
  3. Labels   : application number -> DailyMed label setid(s). % of our applications with a label.
  4. Cadence  : how often RxNorm and Drugs@FDA change (version stamps + submission dates).

Every number in docs/07-data-quality/atlas/rxnorm.html and drugsatfda.html comes from this script.

Input : prototypes/data/_faers_bulk/2026q1, 2026q2          (FAERS quarterly ASCII, unzipped)
        prototypes/data/_identity/drugsatfda_raw/*.txt        (fda.gov "Drugs@FDA Data Files", unzipped)
        prototypes/data/_identity/openfda_raw/*.json          (openFDA drug/drugsfda bulk, for comparison)
        RxNav REST + DailyMed REST (live; every response cached in _identity/cache/*.json)
Output: prototypes/data/_identity/facts.json
Run   : python3 -I prototypes/explore/identity_atlas.py
"""
import collections as C, csv, datetime as dt, importlib.util, json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IDN = os.path.join(ROOT, "data", "_identity")
FDA = os.path.join(IDN, "drugsatfda_raw")
CACHE = os.path.join(IDN, "cache")

# Reuse the FAERS reader and the walkthrough's identity rules exactly (python -I drops the script dir from sys.path).
_spec = importlib.util.spec_from_file_location("walk", os.path.join(HERE, "faers_bulk_walkthrough.py"))
walk = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(walk)
OURS, SALTS, BRANDS, QUARTERS = walk.OURS, walk.SALTS, walk.BRANDS, walk.QUARTERS
RXCUI = {"buprenorphine": "1819", "fentanyl": "4337", "hydrocodone": "5489", "hydromorphone": "3423",
         "methadone": "6813", "morphine": "7052", "oxycodone": "7804", "tramadol": "10689",
         "semaglutide": "1991302", "liraglutide": "475968", "dulaglutide": "1551291", "exenatide": "60548",
         "tirzepatide": "2601723"}
BY_RXCUI = {v: k for k, v in RXCUI.items()}


# ---------------------------------------------------------------- HTTP with a disk cache
_cache = {}


def get_json(service, url, pause=0.06):
    path = os.path.join(CACHE, f"{service}.json")
    if service not in _cache:
        _cache[service] = json.load(open(path)) if os.path.exists(path) else {}
    c = _cache[service]
    if url not in c:
        for attempt in range(4):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "msm-atlas/1"}),
                                            timeout=40) as r:
                    c[url] = json.loads(r.read().decode("utf-8"))
                break
            except Exception as e:  # network blip or 404
                if getattr(e, "code", None) == 404:
                    c[url] = None; break
                time.sleep(2 * (attempt + 1))
        else:
            raise RuntimeError(f"failed: {url}")
        time.sleep(pause)
    return c[url]


def save_cache():
    os.makedirs(CACHE, exist_ok=True)
    for k, v in _cache.items():
        json.dump(v, open(os.path.join(CACHE, f"{k}.json"), "w"))


RX = "https://rxnav.nlm.nih.gov/REST"
DM = "https://dailymed.nlm.nih.gov/dailymed/services/v2"


def rx_ids(name):
    d = get_json("rxnav", f"{RX}/rxcui.json?name={urllib.parse.quote(name)}&search=0")
    return (d or {}).get("idGroup", {}).get("rxnormId", []) or []


def rx_props(rxcui):
    d = get_json("rxnav", f"{RX}/rxcui/{rxcui}/properties.json")
    return (d or {}).get("properties") or {}


def rx_to_in(rxcui):
    """Any RxCUI -> list of (IN rxcui, IN name)."""
    p = rx_props(rxcui)
    if p.get("tty") == "IN":
        return [(rxcui, p["name"])]
    d = get_json("rxnav", f"{RX}/rxcui/{rxcui}/related.json?tty=IN")
    out = []
    for g in (d or {}).get("relatedGroup", {}).get("conceptGroup", []) or []:
        for cp in g.get("conceptProperties", []) or []:
            out.append((cp["rxcui"], cp["name"]))
    return out


# Words the walkthrough's SALTS list does not cover, found by this script (Drugs@FDA + FAERS spellings).
EXTRA = r"\b(synthetic|polistirex|trihydrate)\b"


def strip_salt(s, extra=True):
    out = re.sub(SALTS, "", s.lower())
    if extra:
        out = re.sub(EXTRA, "", out)
    return re.sub(r"\s+", " ", out).strip()


def has_ours(s):
    low = s.lower()
    return [i for i in OURS if i in low]


# ---------------------------------------------------------------- Step 0: read FAERS DRUG rows that could be ours
def load_candidates():
    """Candidate = any DRUG row whose prod_ai/drugname contains one of our 13 words (the naive net) or a brand."""
    rows = []
    totals = C.Counter()
    for q in QUARTERS:
        for d in walk.read(q, "DRUG"):
            totals[q] += 1
            text = (d["prod_ai"] + " " + d["drugname"]).lower()
            if not (has_ours(text) or any(re.search(rf"\b{b}\b", d["drugname"].lower()) for b in BRANDS)):
                continue
            rule, via = walk.ingredients(d["prod_ai"], d["drugname"])
            rows.append({"q": q, "pid": d["primaryid"], "role": d["role_cod"], "drugname": d["drugname"],
                         "prod_ai": d["prod_ai"].strip(), "nda": d["nda_num"].strip(), "rule": rule, "via": via})
    return rows, totals


# ---------------------------------------------------------------- Step 1: RxNorm
def rxnorm_resolve(rows, facts):
    comps = C.Counter()          # component string -> rows
    for r in rows:
        if r["prod_ai"]:
            for p in r["prod_ai"].split("\\"):
                if has_ours(p):
                    comps[p.strip()] += 1
    res = {}
    for c in comps:
        raw = rx_ids(c)
        strip = rx_ids(strip_salt(c, extra=False)) if strip_salt(c, extra=False) != c.lower() else raw
        ext = rx_ids(strip_salt(c)) if strip_salt(c) != strip_salt(c, extra=False) else strip
        ids = raw or strip or ext
        ins = sorted({x for i in ids for x in rx_to_in(i)})
        res[c] = {"raw_hit": bool(raw), "strip_hit": bool(strip), "ext_hit": bool(ext), "ids": ids, "ins": ins,
                  "ours": sorted({BY_RXCUI[i] for i, _ in ins if i in BY_RXCUI})}
    f = facts["rxnorm"] = {}
    f["distinct_components"] = len(comps)
    f["component_rows"] = sum(comps.values())
    f["raw_exact_hit"] = [sum(1 for c in comps if res[c]["raw_hit"]), sum(k for c, k in comps.items() if res[c]["raw_hit"])]
    f["strip_exact_hit"] = [sum(1 for c in comps if res[c]["strip_hit"]), sum(k for c, k in comps.items() if res[c]["strip_hit"])]
    f["ext_strip_hit"] = [sum(1 for c in comps if res[c]["ext_hit"]), sum(k for c, k in comps.items() if res[c]["ext_hit"])]
    f["only_ext_found"] = sorted([[c, k] for c, k in comps.items() if res[c]["ext_hit"] and not (res[c]["raw_hit"] or res[c]["strip_hit"])], key=lambda x: -x[1])
    f["any_hit"] = [sum(1 for c in comps if res[c]["ids"]), sum(k for c, k in comps.items() if res[c]["ids"])]
    f["hit_ours"] = [sum(1 for c in comps if res[c]["ours"]), sum(k for c, k in comps.items() if res[c]["ours"])]
    f["only_strip_found"] = sorted([[c, k] for c, k in comps.items() if res[c]["strip_hit"] and not res[c]["raw_hit"]],
                                   key=lambda x: -x[1])[:15]
    f["misses"] = sorted([[c, k, strip_salt(c)] for c, k in comps.items() if not res[c]["ids"]], key=lambda x: -x[1])
    f["resolved_not_ours"] = sorted([[c, k, [n for _, n in res[c]["ins"]]] for c, k in comps.items()
                                     if res[c]["ids"] and not res[c]["ours"]], key=lambda x: -x[1])
    f["multi_in_component"] = sorted([[c, k, [n for _, n in res[c]["ins"]]] for c, k in comps.items()
                                      if len(res[c]["ins"]) > 1], key=lambda x: -x[1])[:10]
    f["top_components"] = [[c, k, res[c]["ids"][:2], [n for _, n in res[c]["ins"]], res[c]["raw_hit"]]
                           for c, k in comps.most_common(25)]
    f["spellings_per_ingredient"] = {i: sum(1 for c in comps if i in res[c]["ours"]) for i in OURS}
    # rows: RxNorm verdict vs the walkthrough's hand rule
    agree = C.Counter(); per_ing = C.Counter(); combos = C.Counter(); combo_rows = C.Counter(); diffs = C.Counter()
    for r in rows:
        if not r["prod_ai"]:
            r["rx"] = None
            continue
        parts = [p.strip() for p in r["prod_ai"].split("\\")]
        rx = set()
        for p in parts:
            if p in res:
                rx |= set(res[p]["ours"])
        r["rx"] = rx
        key = ("both" if rx and r["rule"] and rx == r["rule"] else "differ" if rx and r["rule"] else
               "rxnorm_only" if rx else "rule_only" if r["rule"] else "neither_not_ours")
        agree[key] += 1
        if key in ("differ", "rxnorm_only", "rule_only"):
            diffs[(key, r["prod_ai"], ",".join(sorted(rx)), ",".join(sorted(r["rule"])))] += 1
        for i in rx:
            per_ing[i] += 1
            if len(parts) > 1:
                combo_rows[i] += 1; combos[r["prod_ai"]] += 1
    f["row_agreement_vs_rule"] = dict(agree)
    f["row_diffs"] = [[*k, v] for k, v in diffs.most_common(15)]
    f["rows_by_ingredient"] = {i: per_ing[i] for i in OURS}
    f["combo_rows_by_ingredient"] = {i: combo_rows[i] for i in OURS}
    f["top_combos"] = combos.most_common(15)
    f["compounded_like"] = sorted([[k, v] for k, v in combos.items()
                                   if re.search(r"cyanocobalamin|pyridoxine|glycine|niacinamide|l-carnitine|levocarnitine", k.lower())],
                                  key=lambda x: -x[1])[:10]
    # blank prod_ai: drugname -> approximateTerm
    blank = C.Counter(r["drugname"].strip().upper() for r in rows if not r["prod_ai"])
    br = {}
    for name, k in blank.items():
        d = get_json("rxnav", f"{RX}/approximateTerm.json?term={urllib.parse.quote(name)}&maxEntries=1")
        cand = ((d or {}).get("approximateGroup", {}).get("candidate") or [])
        rc = cand[0]["rxcui"] if cand else None
        ins = rx_to_in(rc) if rc else []
        ours = sorted({BY_RXCUI[i] for i, _ in ins if i in BY_RXCUI})
        rule = sorted(walk.ingredients("", name)[0])
        br[name] = {"rows": k, "rxcui": rc, "ours": ours, "rule": rule}
    for r in rows:
        if not r["prod_ai"]:
            r["rx"] = set(br[r["drugname"].strip().upper()]["ours"])
    f["blank_prod_ai"] = {
        "rows": sum(blank.values()), "distinct_names": len(blank),
        "approx_ours_rows": sum(v["rows"] for v in br.values() if v["ours"]),
        "rule_ours_rows": sum(v["rows"] for v in br.values() if v["rule"]),
        "agree_rows": sum(v["rows"] for v in br.values() if v["ours"] == v["rule"] and v["ours"]),
        "disagree": sorted([[n, v["rows"], v["ours"], v["rule"]] for n, v in br.items() if v["ours"] != v["rule"]],
                           key=lambda x: -x[1])[:15],
        "top": sorted([[n, v["rows"], v["ours"]] for n, v in br.items()], key=lambda x: -x[1])[:12]}
    # our 13 IN concepts: still active?
    f["in_status"] = {}
    for ing, rc in RXCUI.items():
        h = get_json("rxnav", f"{RX}/rxcui/{rc}/historystatus.json")
        md = (h or {}).get("rxcuiStatusHistory", {}).get("metaData", {})
        at = (h or {}).get("rxcuiStatusHistory", {}).get("attributes", {})
        f["in_status"][ing] = [rc, md.get("status"), at.get("tty"), md.get("activeStartDate"), at.get("name")]
    return res


# ---------------------------------------------------------------- Step 2: Drugs@FDA
def read_tab(name):
    with open(os.path.join(FDA, name), encoding="latin-1", newline="") as fh:
        r = csv.reader((l.replace("\r", "") for l in fh), delimiter="\t", quoting=csv.QUOTE_NONE)
        head = next(r)
        for row in r:
            yield dict(zip(head, [x.strip() for x in row]))


def load_fda():
    apps = {a["ApplNo"]: a for a in read_tab("Applications.txt")}
    prods = C.defaultdict(list)
    for p in read_tab("Products.txt"):
        prods[p["ApplNo"]].append(p)
    ms_lookup = {m["MarketingStatusID"]: m["MarketingStatusDescription"] for m in read_tab("MarketingStatus_Lookup.txt")}
    ms = {(m["ApplNo"], m["ProductNo"]): ms_lookup.get(m["MarketingStatusID"]) for m in read_tab("MarketingStatus.txt")}
    return apps, prods, ms


def app_ings(prods_of_app):
    """Ingredients of an application = union over its products, salt-stripped, exact names."""
    out = set()
    for p in prods_of_app:
        for part in re.split(r";|\\|,", p["ActiveIngredient"]):
            s = strip_salt(part)
            if s in OURS:
                out.add(s)
    return out


def norm_nda(v):
    v = v.strip()
    if not v:
        return None, "blank"
    if not v.isdigit():
        return None, "not_digits"
    if len(v) > 6:
        return None, "too_long"
    return v.zfill(6), "ok"


def drugsatfda(rows, facts):
    apps, prods, ms = load_fda()
    f = facts["drugsatfda"] = {}
    f["applications"] = len(apps)
    f["by_type"] = dict(C.Counter(a["ApplType"] for a in apps.values()))
    f["products"] = sum(len(v) for v in prods.values())
    # our 13 inside Drugs@FDA
    ours_apps = {a: app_ings(prods[a]) for a in apps if app_ings(prods[a])}
    f["our_apps"] = len(ours_apps)
    per = {}
    for ing in OURS:
        aa = [a for a, s in ours_apps.items() if ing in s]
        status = C.Counter()
        for a in aa:
            st = {ms.get((a, p["ProductNo"])) for p in prods[a]}
            status["marketed" if st & {"Prescription", "Over-the-counter"} else "discontinued_or_other"] += 1
        per[ing] = {"apps": len(aa), "types": dict(C.Counter(apps[a]["ApplType"] for a in aa)),
                    "combo_apps": sum(1 for a in aa if any(";" in p["ActiveIngredient"] for p in prods[a])),
                    "sponsors": len({apps[a]["SponsorName"] for a in aa}), **status}
    f["our_apps_by_ingredient"] = per
    # FAERS suspect rows that are ours (RxNorm verdict) -> application
    outcome = C.Counter(); by_ing = C.defaultdict(C.Counter); unmatched = C.Counter(); wrong = C.Counter()
    reached_apps = C.Counter(); app_rows_by_ing = C.defaultdict(C.Counter); brand_check = C.Counter()
    fmt = C.Counter(); brand_diff = C.Counter()
    by_name = C.defaultdict(set)
    for a, ps in prods.items():
        for p in ps:
            by_name[p["DrugName"].upper()].add(a)
    recover = C.Counter(); recover_ing = C.defaultdict(C.Counter); recover_ex = C.Counter()
    for r in rows:
        if r["role"] not in ("PS", "SS", "I") or not r["rx"]:
            continue
        key, how = norm_nda(r["nda"])
        fmt[how if how != "ok" else f"len{len(r['nda'])}"] += 1
        if key is None:
            o = how
            if how == "blank":
                hits = {a for a in by_name.get(r["drugname"].strip().upper(), set()) if r["rx"] & app_ings(prods[a])}
                v = "one_application" if len(hits) == 1 else "many_applications" if hits else "no_name_match"
                recover[v] += 1
                for i in r["rx"]:
                    recover_ing[i][v] += 1
                recover_ex[(r["drugname"].strip().upper(), v, len(hits))] += 1
        elif key not in apps:
            o = "unknown_application"
        elif not (r["rx"] & app_ings(prods[key])):
            o = "ingredient_mismatch"
            wrong[(r["nda"], apps[key]["ApplType"], prods[key][0]["DrugName"], prods[key][0]["ActiveIngredient"],
                   ",".join(sorted(r["rx"])))] += 1
        else:
            o = "reached_product"
            reached_apps[key] += 1
            for i in r["rx"]:
                app_rows_by_ing[i][key] += 1
            names = {p["DrugName"].lower() for p in prods[key]}
            dn = r["drugname"].lower()
            ok = any(n.split()[0] in dn for n in names if n) or any(i in dn for i in r["rx"])
            brand_check["drugname_agrees" if ok else "differs"] += 1
            if not ok:
                brand_diff[(r["drugname"].upper(), key, sorted(names)[0].upper())] += 1
        outcome[o] += 1
        for i in r["rx"]:
            by_ing[i][o] += 1
        if o in ("unknown_application", "not_digits", "too_long"):
            unmatched[(r["nda"], ",".join(sorted(r["rx"])))] += 1
    f["suspect_rows"] = sum(outcome.values())
    f["outcome"] = dict(outcome)
    f["nda_format"] = dict(fmt)
    f["by_ingredient"] = {i: dict(by_ing[i]) for i in OURS}
    f["top_unmatched"] = [[a, b, k] for (a, b), k in unmatched.most_common(15)]
    f["top_mismatch"] = [[*k, v] for k, v in wrong.most_common(12)]
    f["brand_check"] = dict(brand_check)
    f["brand_diff_top"] = [[*k, v] for k, v in brand_diff.most_common(12)]
    f["blank_recovery_by_name"] = dict(recover)
    f["blank_recovery_by_ingredient"] = {i: dict(recover_ing[i]) for i in OURS}
    f["blank_recovery_examples"] = [[*k, v] for k, v in recover_ex.most_common(15)]
    f["reached_apps"] = len(reached_apps)
    f["reached_apps_by_type"] = dict(C.Counter(apps[a]["ApplType"] for a in reached_apps))
    f["rows_by_type"] = dict(C.Counter({t: sum(k for a, k in reached_apps.items() if apps[a]["ApplType"] == t)
                                        for t in ("NDA", "ANDA", "BLA")}))
    f["top_apps_by_ingredient"] = {}
    for i in OURS:
        tot = sum(app_rows_by_ing[i].values()) or 1
        top = app_rows_by_ing[i].most_common(4)
        f["top_apps_by_ingredient"][i] = {
            "apps": len(app_rows_by_ing[i]),
            "top": [[a, apps[a]["ApplType"], apps[a]["SponsorName"], sorted({p["DrugName"] for p in prods[a]})[:2],
                     sorted({p["Form"] for p in prods[a]})[:2], k, round(100 * k / tot, 1)] for a, k in top],
            "top1_share": round(100 * top[0][1] / tot, 1) if top else None}
    # examples: the real raw rows for the record section
    f["raw_app_example"] = {"application": apps["209637"], "products": prods["209637"][:3],
                            "marketing": {p["ProductNo"]: ms.get(("209637", p["ProductNo"])) for p in prods["209637"]}}
    f["products_per_app"] = dict(C.Counter(min(len(prods[a]), 10) for a in reached_apps))
    return apps, prods, ms, reached_apps, ours_apps


# ---------------------------------------------------------------- Step 3: application -> DailyMed label
def labels(apps, prods, ms, reached_apps, ours_apps, facts):
    f = facts["labels"] = {}
    marketed = {a for a in ours_apps if {ms.get((a, p["ProductNo"])) for p in prods[a]} & {"Prescription", "Over-the-counter"}}
    targets = sorted(set(reached_apps) | marketed)
    found = {}
    for a in targets:
        appno = apps[a]["ApplType"] + a
        d = get_json("dailymed", f"{DM}/spls.json?application_number={appno}&pagesize=100", pause=0.15)
        found[a] = (d or {}).get("data", []) or []
    def sponsor_match(a, title):
        m = re.search(r"\[([^\]]+)\]\s*$", title)
        lab = (m.group(1) if m else "").lower()
        sp = apps[a]["SponsorName"].lower().split()
        return bool(sp) and sp[0][:5] in lab
    def stats(group, weight=None):
        n = len(group); w = sum((weight or {}).get(a, 1) for a in group) or 1
        has = [a for a in group if found[a]]
        return {"apps": n, "with_label": len(has), "pct": round(100 * len(has) / max(n, 1), 1),
                "rows_pct": round(100 * sum((weight or {}).get(a, 1) for a in has) / w, 1) if weight else None,
                "multi_label": sum(1 for a in group if len(found[a]) > 1),
                "sponsor_label_found": sum(1 for a in has if any(sponsor_match(a, x["title"]) for x in found[a])),
                "labels_total": sum(len(found[a]) for a in group)}
    f["reached_from_faers"] = stats(sorted(reached_apps), reached_apps)
    f["marketed_in_drugsatfda"] = stats(sorted(marketed))
    f["by_type_reached"] = {t: stats([a for a in reached_apps if apps[a]["ApplType"] == t], reached_apps)
                            for t in ("NDA", "ANDA", "BLA")}
    def mstat(a):
        st = {ms.get((a, p["ProductNo"])) for p in prods[a]}
        return "marketed" if st & {"Prescription", "Over-the-counter"} else "discontinued"
    nol = [a for a in reached_apps if not found[a]]
    f["no_label_status"] = dict(C.Counter(mstat(a) for a in nol))
    f["no_label_rows"] = sum(reached_apps[a] for a in nol)
    f["no_label_top"] = sorted([[a, apps[a]["ApplType"], apps[a]["SponsorName"], prods[a][0]["DrugName"],
                                 reached_apps[a], mstat(a)] for a in reached_apps if not found[a]], key=lambda x: -x[4])[:12]
    f["most_labels"] = sorted([[a, apps[a]["ApplType"], prods[a][0]["DrugName"], len(found[a]), reached_apps.get(a, 0)]
                               for a in targets], key=lambda x: -x[3])[:8]
    f["ozempic_labels"] = found.get("209637", [])
    # openFDA drugsfda harmonised setids, for comparison
    ofda = json.load(open(os.path.join(IDN, "openfda_raw", "drug-drugsfda-0001-of-0001.json")))["results"]
    oset = {x["application_number"]: (x.get("openfda") or {}).get("spl_set_id", []) for x in ofda}
    f["openfda_drugsfda_total"] = [len(ofda), sum(1 for v in oset.values() if v)]
    reached_keys = [apps[a]["ApplType"] + a for a in reached_apps]
    f["openfda_setid_for_reached"] = [len(reached_keys), sum(1 for k in reached_keys if oset.get(k))]
    f["openfda_empty_examples"] = [k for k in sorted(reached_keys, key=lambda k: -reached_apps[k.lstrip("ANDBL")])
                                   if not oset.get(k)][:8]
    # SPL itself carries the application number: check the label XML of 6 apps
    checks = []
    for a in sorted(reached_apps, key=lambda a: -reached_apps[a])[:6]:
        if not found[a]:
            continue
        sid = found[a][0]["setid"]
        try:
            with urllib.request.urlopen(f"{DM}/spls/{sid}.xml", timeout=60) as r:
                xml = r.read().decode("utf-8", "replace")
            ids = sorted(set(re.findall(r'<approval>\s*<id extension="([^"]+)"', xml)))
        except Exception as e:
            ids = [f"error {e}"]
        checks.append([apps[a]["ApplType"] + a, sid, ids])
        time.sleep(0.3)
    f["spl_approval_check"] = checks
    return found


# ---------------------------------------------------------------- Step 4: cadence
def cadence(apps, ours_apps, facts):
    f = facts["cadence"] = {}
    f["rxnav_version"] = get_json("rxnav_live", f"{RX}/version.json", pause=0)
    zips = [z for z in os.listdir(FDA) if z.endswith(".zip")]
    f["drugsatfda_zip"] = zips
    f["drugsatfda_file_mtime"] = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(FDA, "Applications.txt"))).isoformat()
    ofda = json.load(open(os.path.join(IDN, "openfda_raw", "drug-drugsfda-0001-of-0001.json")))["meta"]
    f["openfda_drugsfda_last_updated"] = ofda.get("last_updated")
    cls = {c["SubmissionClassCodeID"]: c["SubmissionClassCode"] for c in read_tab("SubmissionClass_Lookup.txt")}
    subs = list(read_tab("Submissions.txt"))
    dates = [s["SubmissionStatusDate"][:10] for s in subs if s["SubmissionStatusDate"]]
    last = max(dates)
    f["latest_submission_date"] = last
    end = dt.date.fromisoformat(last)
    def window(days, only=None):
        start = (end - dt.timedelta(days=days)).isoformat()
        sel = [s for s in subs if s["SubmissionStatusDate"][:10] > start and (only is None or s["ApplNo"] in only)]
        return sel
    all90 = window(90)
    f["all_last90"] = len(all90)
    per_week = C.Counter()
    for s in all90:
        d = dt.date.fromisoformat(s["SubmissionStatusDate"][:10])
        per_week[(d - dt.timedelta(days=d.weekday())).isoformat()] += 1
    f["all_last90_per_week"] = sorted(per_week.items())
    f["all_last90_weekdays"] = dict(C.Counter(dt.date.fromisoformat(s["SubmissionStatusDate"][:10]).strftime("%a") for s in all90))
    ours365 = window(365, set(ours_apps))
    f["ours_last365"] = len(ours365)
    f["ours_last365_apps"] = len({s["ApplNo"] for s in ours365})
    f["ours_last365_by_class"] = dict(C.Counter(cls.get(s["SubmissionClassCodeID"], s["SubmissionClassCodeID"]) for s in ours365).most_common(8))
    f["ours_last365_by_type"] = dict(C.Counter(s["SubmissionType"] for s in ours365))
    per_month = C.Counter(s["SubmissionStatusDate"][:7] for s in ours365)
    f["ours_last365_per_month"] = sorted(per_month.items())
    for m in [k for k, v in per_month.items() if v > 100]:
        sel = [s for s in ours365 if s["SubmissionStatusDate"][:7] == m]
        f.setdefault("spikes", {})[m] = {"actions": len(sel), "apps": len({s["ApplNo"] for s in sel}),
            "by_class": dict(C.Counter(cls.get(s["SubmissionClassCodeID"], "") for s in sel)),
            "by_ingredient": dict(C.Counter(i for s in sel for i in ours_apps[s["ApplNo"]])),
            "days": dict(C.Counter(s["SubmissionStatusDate"][:10] for s in sel).most_common(3))}
    f["ours_last365_examples"] = sorted([[s["SubmissionStatusDate"][:10], apps[s["ApplNo"]]["ApplType"] + s["ApplNo"],
                                          apps[s["ApplNo"]]["SponsorName"], s["SubmissionType"],
                                          cls.get(s["SubmissionClassCodeID"], ""), ",".join(sorted(ours_apps[s["ApplNo"]]))]
                                         for s in ours365], reverse=True)[:10]
    # new applications in the last year for our 13 (ORIG approvals)
    f["ours_new_apps_365"] = [x for x in f["ours_last365_examples"] if x[3] == "ORIG"]
    f["ours_last365_by_status"] = dict(C.Counter(s["SubmissionStatus"] for s in ours365))  # AP approved, TA tentative
    f["all_last90_by_status"] = dict(C.Counter(s["SubmissionStatus"] for s in all90))
    f["ours_orig_365"] = sorted([[s["SubmissionStatusDate"][:10], apps[s["ApplNo"]]["ApplType"] + s["ApplNo"],
                                  apps[s["ApplNo"]]["SponsorName"], ",".join(sorted(ours_apps[s["ApplNo"]])), s["SubmissionStatus"]]
                                 for s in ours365 if s["SubmissionType"] == "ORIG"], reverse=True)


def main():
    facts = {"run_at": dt.datetime.now().isoformat(timespec="seconds")}
    rows, totals = load_candidates()
    facts["faers"] = {"drug_rows_total": dict(totals), "candidate_rows": len(rows),
                      "candidate_rows_by_q": dict(C.Counter(r["q"] for r in rows))}
    print("candidates", len(rows), flush=True)
    rxnorm_resolve(rows, facts); save_cache(); print("rxnorm done", flush=True)
    apps, prods, ms, reached, ours_apps = drugsatfda(rows, facts); print("drugs@fda done", flush=True)
    labels(apps, prods, ms, reached, ours_apps, facts); save_cache(); print("labels done", flush=True)
    cadence(apps, ours_apps, facts); save_cache()
    json.dump(facts, open(os.path.join(IDN, "facts.json"), "w"), indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
    print(json.dumps({k: facts[k] for k in ("faers",)}, indent=1))
    print(json.dumps({k: facts["rxnorm"][k] for k in ("distinct_components", "raw_exact_hit", "strip_exact_hit", "any_hit", "hit_ours", "row_agreement_vs_rule")}, indent=1))
    print(json.dumps({k: facts["drugsatfda"][k] for k in ("suspect_rows", "outcome", "reached_apps")}, indent=1))
    print(json.dumps({k: facts["labels"][k] for k in ("reached_from_faers", "marketed_in_drugsatfda")}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
