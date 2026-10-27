"""Label atlas: measure DailyMed, SrLC and OnSIDES for our 13 ingredients (Part B risk area).

Every number on docs/07-data-quality/atlas/{dailymed,srlc,onsides}.html comes from this script.

Steps (run in order; each caches its HTTP calls and merges its numbers into facts.json):
    refs      FAERS nda_num -> DailyMed application_number -> one reference label per ingredient
    sections  section sizes, tables, nesting, LOINC codes of each reference label
    census    label versions published per day / week over the last 90 days (ChangeEvent input)
    dailyzip  what is inside one DailyMed daily update zip, and how many of ours
    srlc      FDA Safety-related Labeling Changes for our 13 ingredients (search + detail pages + 90-day date search)
    srlcan    exact-ingredient filter, reference products, underlined additions, lag SrLC date -> DailyMed version
    onsides   OnSIDES v3.1.1 layout, link key, snapshot age, terms vs the current label
    textdump  plain text of the 4 safety sections of the 2 gold-set labels (for hand annotation)
    goldcheck verify every quote in the gold-set draft CSV exists word for word in the label

Input : prototypes/data/_faers_bulk/2026q1|q2 (FAERS), prototypes/data/_onsides/v3.1.1/csv (OnSIDES release),
        prototypes/data/_labels/daily_zip/*.zip (one DailyMed daily update), network (DailyMed, SrLC)
Output: prototypes/data/_labels/facts.json (+ cache/, xml/, text/, srlc/)
Run   : python3 -I prototypes/explore/label_atlas.py refs sections census dailyzip srlc srlcan onsides textdump goldcheck
Standard library only.
"""
import collections as C, csv, datetime as dt, hashlib, html, io, json, os, re, sys, time, zipfile
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "_labels")
CACHE = os.path.join(OUT, "cache")
REPO = os.path.dirname(ROOT)
GOLD = os.path.join(REPO, "docs", "07-data-quality", "atlas", "gold-set-draft-v1.csv")
for d in (OUT, CACHE, os.path.join(OUT, "xml"), os.path.join(OUT, "text")):
    os.makedirs(d, exist_ok=True)

TODAY = dt.date(2026, 10, 20)          # fixed so reruns give the same window
WINDOW_START = TODAY - dt.timedelta(days=90)
OURS = ["buprenorphine", "fentanyl", "hydrocodone", "hydromorphone", "methadone", "morphine",
        "oxycodone", "tramadol", "semaglutide", "liraglutide", "dulaglutide", "exenatide", "tirzepatide"]
SALTS = r"\b(hydrochloride|hcl|bitartrate|citrate|sulfate|sulphate|terephthalate|tartrate|acetate|" \
        r"phosphate|myristate|propanediol|sodium|anhydrous)\b"
DM = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
SRLC = "https://www.accessdata.fda.gov/scripts/cder/safetylabelingchanges/index.cfm"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
NS = {"v3": "urn:hl7-org:v3"}
PARENTS = {"34066-1": "Boxed Warning", "34070-3": "Contraindications", "43685-7": "Warnings and Precautions",
           "34071-1": "Warnings", "34084-4": "Adverse Reactions"}
FACTS_PATH = os.path.join(OUT, "facts.json")
FACTS = json.load(open(FACTS_PATH)) if os.path.exists(FACTS_PATH) else {}

# SrLC needs a session cookie and a browser user agent (plain curl gets an "abuse detection" redirect).
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
_opener.addheaders = [("User-Agent", UA)]


_STEP_KEYS = {"refs": "refs", "sections": "sections", "census": "census", "dailyzip": "dailyzip",
              "srlc": "srlc", "srlcan": "srlcan", "onsides": "onsides", "goldcheck": "gold"}


def save_facts():
    """Merge into facts.json, re-reading it first so steps can run in parallel processes."""
    disk = json.load(open(FACTS_PATH)) if os.path.exists(FACTS_PATH) else {}
    for step in sys.argv[1:]:
        k = _STEP_KEYS.get(step)
        if k and k in FACTS:
            disk[k] = FACTS[k]
    json.dump(disk, open(FACTS_PATH, "w"), indent=1, sort_keys=True, default=str)


def fetch(url, data=None, cache=True, sleep=0.3):
    """GET (or POST when data is a dict). Cached on disk by URL+body so reruns are free and stable."""
    body = urllib.parse.urlencode(data, doseq=True).encode() if data else None
    key = hashlib.sha1((url + "|" + (body or b"").decode()).encode()).hexdigest()
    path = os.path.join(CACHE, key)
    if cache and os.path.exists(path):
        return open(path, "rb").read()
    for attempt in range(4):
        try:
            with _opener.open(urllib.request.Request(url, data=body), timeout=90) as r:
                raw = r.read()
            break
        except Exception as e:
            if attempt == 3:
                raise
            print(f"  retry {url[:90]} ({e})"); time.sleep(3 * (attempt + 1))
    open(path, "wb").write(raw)
    time.sleep(sleep)
    return raw


def jget(url):
    return json.loads(fetch(url))


def dm_date(s):
    return dt.datetime.strptime(s, "%b %d, %Y").date()


def dm_all(url):
    """All pages of a DailyMed v2 list endpoint."""
    rows, page = [], 1
    while True:
        d = jget(f"{url}&pagesize=100&page={page}")
        rows += d["data"]
        if page >= int(d["metadata"]["total_pages"] or 1):
            return rows, d["metadata"]
        page += 1


def maker(title):
    m = re.search(r"\[([^\]]+)\]\s*$", title)
    return m.group(1) if m else ""


# --------------------------------------------------------------------------- refs
def faers_rows():
    for q in ("2026q1", "2026q2"):
        path = os.path.join(DATA, "_faers_bulk", q, "ASCII", f"DRUG{q[2:4]}{q[4:].upper()}.txt")
        with open(path, encoding="latin-1", newline="") as f:
            r = csv.reader((l.replace("\r", "") for l in f), delimiter="$", quoting=csv.QUOTE_NONE)
            head = next(r)
            for row in r:
                yield dict(zip(head, row))


# When FAERS's most-reported product is a generic (ANDA), the innovator (reference listed drug) of the SAME
# route. Hand-made from Drugs@FDA; used only if that innovator's own label is still on DailyMed.
RLD = {"fentanyl": "NDA019813",     # Duragesic patch (Janssen)
       "methadone": "NDA006134",    # Dolophine tablet
       "tramadol": "NDA020281",     # Ultram tablet
       "exenatide": "NDA021773"}    # Byetta injection (AstraZeneca)


def pick_label(appl):
    """(label, candidates, sponsor, matched) for one application number, preferring the sponsor's own label."""
    rows, _ = dm_all(f"{DM}/spls.json?application_number={appl}")
    if not rows:
        return None, 0, "", False
    sponsor = ""
    try:
        sponsor = jget(f"https://api.fda.gov/drug/drugsfda.json?search=application_number:{appl}&limit=1")["results"][0]["sponsor_name"]
    except Exception:
        pass
    key = sponsor.split()[0].lower() if sponsor else ""
    own = [c for c in rows if key and key in maker(c["title"]).lower()]
    pick = sorted(own or rows, key=lambda c: -c["spl_version"])[0]
    return dict(pick, appl=appl), len(rows), sponsor, bool(own)


def step_refs():
    """Reference label: the product FAERS names most often as primary suspect -> its innovator label.
    If that product is a generic, use the same-route innovator label when it is still on DailyMed,
    otherwise keep the generic's own label (flagged)."""
    nda = {i: C.Counter() for i in OURS}
    single = C.Counter(); combo = C.Counter(); blank = C.Counter()
    for d in faers_rows():
        if d["role_cod"] != "PS" or not d["prod_ai"].strip():
            continue
        parts = {re.sub(SALTS, "", p.lower()).strip() for p in d["prod_ai"].split("\\")}
        hit = parts & set(OURS)
        if len(hit) != 1:
            continue
        ing = hit.pop()
        if len(parts) > 1:
            combo[ing] += 1; continue
        single[ing] += 1
        n = d["nda_num"].strip()
        if not n:
            blank[ing] += 1; continue
        nda[ing][n.lstrip("0")] += 1
    refs = {}
    for ing in OURS:
        top = nda[ing].most_common(8)
        chosen = None; tried = []
        for n, k in top:
            # FAERS nda_num has no prefix; application numbers are unique across NDA/BLA/ANDA, so try each.
            for prefix in ("NDA", "BLA", "ANDA"):
                lab, ncand, sponsor, matched = pick_label(f"{prefix}{n.zfill(6)}")
                if lab:
                    break
            tried.append({"nda_num": n, "reports": k, "labels": ncand, "appl": lab["appl"] if lab else None})
            if not lab:
                continue
            chosen = dict(lab, nda_num=n, faers_reports=k, sponsor=sponsor, n_labels_same_appl=ncand,
                          sponsor_matched=matched, rule="most-reported product, innovator label")
            if lab["appl"].startswith("ANDA") and ing in RLD:
                inn, ninn, isp, imatch = pick_label(RLD[ing])
                chosen["innovator_checked"] = {"appl": RLD[ing], "labels": ninn, "sponsor": isp,
                                               "sponsor_label_found": imatch,
                                               "only_other_labels": [maker(x["title"]) for x in
                                                                     dm_all(f"{DM}/spls.json?application_number={RLD[ing]}")[0]]}
                if inn and imatch:
                    chosen = dict(inn, nda_num=n, faers_reports=k, sponsor=isp, n_labels_same_appl=ninn,
                                  sponsor_matched=True, rule="generic most reported -> same-route innovator label",
                                  generic_label=lab["setid"])
                else:
                    chosen["rule"] = "generic most reported; innovator label no longer on DailyMed -> generic label"
            break
        tot = sum(nda[ing].values())
        refs[ing] = {"ref": chosen, "tried": tried, "ps_single": single[ing], "ps_combo": combo[ing],
                     "ps_blank_nda": blank[ing], "top_nda": top[:5],
                     "top_share": round(100 * top[0][1] / tot, 1) if tot else None}
        r = chosen or {}
        print(f"{ing:14} {r.get('appl','-'):10} v{r.get('spl_version','-'):<4} {r.get('published_date','-'):13} "
              f"{r.get('title','NONE')[:70]}  (sponsor match {r.get('sponsor_matched')})")
    FACTS["refs"] = refs
    save_facts()


# --------------------------------------------------------------------------- sections
def get_xml(setid):
    path = os.path.join(OUT, "xml", f"{setid}.xml")
    if not os.path.exists(path):
        open(path, "wb").write(fetch(f"{DM}/spls/{setid}.xml", cache=False))
    return ET.parse(path).getroot()


def code_of(sec):
    c = sec.find("v3:code", NS)
    return c.get("code") if c is not None else None


def title_of(sec):
    t = sec.find("v3:title", NS)
    return re.sub(r"\s+", " ", "".join(t.itertext())).strip() if t is not None else ""


def text_of(el):
    return re.sub(r"\s+", " ", " ".join(el.itertext())).strip()


def walk(sec, depth=1):
    """Yield (section, depth) for this section and every nested section."""
    yield sec, depth
    for sub in sec.findall("v3:component/v3:section", NS):
        yield from walk(sub, depth + 1)


def top_sections(root):
    return root.findall("v3:component/v3:structuredBody/v3:component/v3:section", NS)


def profile_label(root):
    secs = top_sections(root)
    out = {"top_level_sections": len(secs), "parents": [], "all_codes": C.Counter(), "version":
           root.find("v3:versionNumber", NS).get("value"), "effective": root.find("v3:effectiveTime", NS).get("value")}
    for s in secs:
        for sub, _ in walk(s):
            out["all_codes"][code_of(sub)] += 1
    out["all_codes"] = dict(out["all_codes"])
    for s in secs:
        c = code_of(s)
        if c not in PARENTS:
            continue
        nested = list(walk(s))
        tables = s.findall(".//v3:table", NS)
        spans = sum(1 for t in tables for td in t.iter() if td.get("rowspan") or td.get("colspan"))
        txt = text_of(s)
        out["parents"].append({
            "code": c, "name": PARENTS[c], "title": title_of(s), "chars": len(txt), "words": len(txt.split()),
            "subsections": len(nested) - 1, "max_depth": max(d for _, d in nested),
            "sub_codes": dict(C.Counter(code_of(x) for x, d in nested if d > 1)),
            "sub_titles": [title_of(x) for x, d in nested if d == 2][:20],
            "tables": len(tables), "table_rows": sum(len(t.findall(".//v3:tr", NS)) for t in tables),
            "merged_cells": spans, "footnotes": len(s.findall(".//v3:footnote", NS)),
            "cross_refs": len(re.findall(r"\[see [^\]]+\]", txt)),
            "lists": len(s.findall(".//v3:list", NS)),
        })
    return out


def step_sections():
    refs = FACTS["refs"]
    prof = {}
    for ing in OURS:
        r = refs[ing]["ref"]
        if not r:
            continue
        p = profile_label(get_xml(r["setid"]))
        prof[ing] = p
        size = {x["name"]: x["chars"] for x in p["parents"]}
        print(f"{ing:14} parents={[x['code'] for x in p['parents']]} tables={sum(x['tables'] for x in p['parents'])} "
              f"chars={sum(size.values()):,} sub42229={sum(x['sub_codes'].get('42229-5',0) for x in p['parents'])}")
    # Staleness probe: does each opioid reference label carry the two latest class-wide additions seen in SrLC?
    probes = {"hyperalgesia (SrLC Dec 2023)": r"hyperalgesia", "esophageal dysfunction (SrLC Dec 2025)": r"esophageal dysfunction"}
    for ing in OURS[:8]:
        r = refs[ing]["ref"]
        txt = text_of(get_xml(r["setid"])).lower()
        prof[ing]["class_update_probe"] = {k: bool(re.search(v, txt)) for k, v in probes.items()}
        print(f"{ing:14} {r['published_date']:13} {prof[ing]['class_update_probe']}")
    FACTS["sections"] = prof
    save_facts()


# --------------------------------------------------------------------------- census
def history(setid):
    """All versions of one label: [{spl_version, published_date}], newest first."""
    rows, page = [], 1
    while True:
        d = jget(f"{DM}/spls/{setid}/history.json?pagesize=100&page={page}")
        rows += d["data"]["history"]
        if page >= int(d["metadata"]["total_pages"] or 1):
            return rows
        page += 1


def step_census():
    per_ing = {}; all_setids = {}
    day = C.Counter(); week = C.Counter(); ref_day = C.Counter()
    ref_ids = {FACTS["refs"][i]["ref"]["setid"] for i in OURS if FACTS["refs"][i]["ref"]}
    dup_versions = []
    for ing in OURS:
        labels, meta = dm_all(f"{DM}/spls.json?drug_name={ing}")
        for l in labels:
            all_setids.setdefault(l["setid"], set()).add(ing)
        recent, _ = dm_all(f"{DM}/spls.json?drug_name={ing}&published_date={WINDOW_START}&published_date_comparison=gte")
        versions = 0; touched = 0
        for l in recent:
            h = history(l["setid"])
            inwin = [v for v in h if dm_date(v["published_date"]) >= WINDOW_START]
            seen = C.Counter(v["spl_version"] for v in h)
            if any(k > 1 for k in seen.values()):
                dup_versions.append([l["setid"], [v for v, k in seen.items() if k > 1]])
            if inwin:
                touched += 1
            for v in inwin:
                dd = dm_date(v["published_date"]); versions += 1
                day[(str(dd), ing)] += 1
                week[(dd.isocalendar()[1], ing)] += 1
                if l["setid"] in ref_ids:
                    ref_day[(str(dd), ing)] += 1
        per_ing[ing] = {"labels_now": len(labels), "labels_touched_90d": touched, "versions_90d": versions}
        print(f"{ing:14} labels={len(labels):4}  touched in 90d={touched:3}  versions in 90d={versions:3}")
    days = [str(WINDOW_START + dt.timedelta(days=i)) for i in range(91)]
    per_day = {d: sum(v for (dd, _), v in day.items() if dd == d) for d in days}
    FACTS["census"] = {
        "window": [str(WINDOW_START), str(TODAY)], "per_ingredient": per_ing, "per_day": per_day,
        "per_day_by_ing": {f"{d}|{i}": v for (d, i), v in day.items()},
        "per_week": {f"{w}": sum(v for (ww, _), v in week.items() if ww == w) for w in sorted({w for w, _ in week})},
        "ref_versions": {f"{d}|{i}": v for (d, i), v in ref_day.items()},
        "unique_setids_all_13": len(all_setids),
        "setids_in_2plus_ingredients": sum(1 for v in all_setids.values() if len(v) > 1),
        "duplicate_version_numbers": dup_versions[:20], "n_duplicate_version_setids": len(dup_versions),
    }
    json.dump({k: sorted(v) for k, v in all_setids.items()}, open(os.path.join(OUT, "our_setids.json"), "w"))
    vals = list(per_day.values())
    print("days with 0 versions:", sum(1 for v in vals if v == 0), " max/day:", max(vals),
          " mean/day:", round(sum(vals) / len(vals), 2), " total:", sum(vals))
    save_facts()


# --------------------------------------------------------------------------- daily zip
def step_dailyzip():
    zdir = os.path.join(OUT, "daily_zip")
    ours = json.load(open(os.path.join(OUT, "our_setids.json")))
    res = {}
    for name in sorted(os.listdir(zdir)):
        if not name.endswith(".zip"):
            continue
        z = zipfile.ZipFile(os.path.join(zdir, name))
        inner = [i for i in z.infolist() if i.filename.endswith(".zip")]
        folders = C.Counter(i.filename.split("/")[0] for i in inner)
        dates = C.Counter(os.path.basename(i.filename)[:8] for i in inner)
        hits = []
        for i in inner:
            m = re.match(r"(\d{8})_([0-9a-f-]{36})\.zip", os.path.basename(i.filename))
            if m and m.group(2) in ours:
                iz = zipfile.ZipFile(io.BytesIO(z.read(i)))
                xmlname = [n for n in iz.namelist() if n.endswith(".xml")][0]
                root = ET.fromstring(iz.read(xmlname))
                hits.append({"file": i.filename, "setid": m.group(2), "ingredients": ours[m.group(2)],
                             "version": root.find("v3:versionNumber", NS).get("value"),
                             "effective": root.find("v3:effectiveTime", NS).get("value"),
                             "inner_files": len(iz.namelist()), "xml_kb": round(len(iz.read(xmlname)) / 1024)})
        res[name] = {"bytes": os.path.getsize(os.path.join(zdir, name)), "spl_zips": len(inner),
                     "folders": dict(folders), "file_date_prefix": dict(dates.most_common(5)), "ours": hits}
        print(name, len(inner), dict(folders), "ours:", len(hits))
        for h in hits:
            print("  ", h)
    # What the download page offers right now, and how big each file is (HEAD requests)
    page = fetch("https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-drug-labels.cfm", cache=False).decode("utf-8", "ignore")
    links = sorted(set(re.findall(r'https://dailymed-data\.nlm\.nih\.gov/public-release-files/(dm_spl_(?:daily|weekly|monthly)_update_[^"]+\.zip)', page)))
    offered = {}
    for name in links:
        req = urllib.request.Request("https://dailymed-data.nlm.nih.gov/public-release-files/" + name, method="HEAD")
        with _opener.open(req, timeout=60) as r:
            offered[name] = {"bytes": int(r.headers.get("Content-Length", 0)), "last_modified": r.headers.get("Last-Modified")}
    kinds = C.Counter(re.search(r"_(daily|weekly|monthly)_", n).group(1) for n in offered)
    print("offered update files:", dict(kinds))
    for n, v in offered.items():
        print(f"   {n:45} {v['bytes']/1e6:8.0f} MB  {v['last_modified']}")
    # API date filter: equality vs comparison
    eq = jget(f"{DM}/spls.json?drug_name=oxycodone&published_date=2026-10-12&pagesize=5")["metadata"]["total_elements"]
    gte = jget(f"{DM}/spls.json?drug_name=oxycodone&published_date=2026-10-12&published_date_comparison=gte&pagesize=5")["metadata"]["total_elements"]
    FACTS["dailyzip"] = {"zips": res, "offered": offered, "offered_kinds": dict(kinds),
                         "api_filter_equal_2026_10_12": eq, "api_filter_gte_2026_10_12": gte}
    print("published_date=2026-10-12 alone:", eq, " with comparison=gte:", gte)
    save_facts()


# --------------------------------------------------------------------------- SrLC
def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def srlc_search(name):
    fetch(SRLC, cache=False, sleep=0.5)  # session cookie
    t = fetch(f"{SRLC}?event=searchResult.page", data={"drug_name": name, "TextSearch": ""}).decode("utf-8", "ignore")
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", t, flags=re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        if len(tds) >= 6:
            idm = re.search(r"DrugNameID=(\d+)", tr)
            rows.append({"drug": strip_tags(tds[0]), "ingredient": strip_tags(tds[1]), "appl_no": strip_tags(tds[2]),
                         "appl_type": strip_tags(tds[3]), "supp_date": strip_tags(tds[4]),
                         "db_updated": strip_tags(tds[5]), "id": idm.group(1) if idm else None})
    return rows


def srlc_detail(did):
    t = fetch(f"{SRLC}?event=searchdetail.page&DrugNameID={did}").decode("utf-8", "ignore")
    head = re.search(r"\(NDA-(\d+)\)|\((BLA|ANDA)-(\d+)\)", t)
    parts = re.split(r"<h3[^>]*accordion-header[^>]*>", t)[1:]
    entries = []
    for p in parts:
        m = re.match(r"\s*(\d\d/\d\d/\d{4})\s*</a>\s*<small>\((\w+)-(\d+)\)</small>", p)
        if not m:
            continue
        pdf = re.search(r'href="([^"]+\.pdf)"', p)
        secs = []
        for sm in re.finditer(r"<h4>(.*?)</h4>(.*?)(?=<h4>|$)", p, flags=re.S):
            name = strip_tags(sm.group(1)); body = sm.group(2)
            und = [strip_tags(u) for u in re.findall(r"<u>(.*?)</u>", body, flags=re.S)]
            und = [u for u in und if u]
            secs.append({"section": name, "chars": len(strip_tags(body)), "underlined": und,
                         "new_subsection": "Newly added" in body or "newly added" in body,
                         "text": strip_tags(body)[:4000]})
        entries.append({"date": m.group(1), "supp": f"{m.group(2)}-{int(m.group(3))}",
                        "pdf": pdf.group(1) if pdf else None, "sections": secs})
    return entries


def step_srlc():
    os.makedirs(os.path.join(OUT, "srlc"), exist_ok=True)
    res = {}; ids = {}
    for ing in OURS:
        rows = srlc_search(ing)
        res[ing] = {"search_rows": rows}
        for r in rows:
            if r["id"]:
                ids[r["id"]] = r
        print(f"{ing:14} search rows={len(rows):3}  ids={len({r['id'] for r in rows})}")
    details = {}
    for did, r in ids.items():
        details[did] = {"meta": r, "entries": srlc_detail(did)}
    json.dump(details, open(os.path.join(OUT, "srlc", "details.json"), "w"), indent=1)
    # one CSV download, to record its columns
    csvb = fetch(f"{SRLC}?event=downloadDetails.page&DrugNameID=2183").decode("utf-8", "ignore")
    allrows = list(csv.reader(io.StringIO(csvb)))
    blank_lead = 0
    while allrows and not allrows[0]:
        allrows.pop(0); blank_lead += 1        # the file starts with an empty line
    cols = allrows[0]
    data = [r for r in allrows[1:] if len(r) == len(cols)]
    broken = [r for r in allrows[1:] if r and len(r) != len(cols)]   # a stray quote in embedded HTML splits rows
    ncsv = len(data)
    csv_supps = sorted({int(r[7]) for r in data if r[7].strip().isdigit()})
    # Last-90-days date search, all drugs, all sections
    t = fetch(f"{SRLC}?event=searchResult.page", data={
        "date_range_from": WINDOW_START.strftime("%m/%d/%Y"), "date_range_to": TODAY.strftime("%m/%d/%Y"),
        "section": ["BW", "C", "WP", "AR", "DI", "USP", "MG"], "Datesearch": ""}).decode("utf-8", "ignore")
    drows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", t, flags=re.S):
        tds = [strip_tags(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        if len(tds) >= 5:
            drows.append(tds)
    FACTS["srlc"] = {"per_ingredient": {i: summarize_srlc(i, res[i]["search_rows"], details) for i in OURS},
                     "csv_columns": cols, "csv_rows_ozempic": ncsv, "csv_blank_leading_lines": blank_lead,
                     "csv_broken_fragments": len(broken), "csv_row_widths": dict(C.Counter(len(r) for r in allrows[1:])),
                     "csv_supplements_ozempic": csv_supps, "csv_example_row": [x[:200] for x in data[0]], "date_search_90d_rows": len(drows),
                     "date_search_90d_sample": drows[:8], "date_search_header_guess": "see sample",
                     "n_ids": len(details)}
    json.dump(drows, open(os.path.join(OUT, "srlc", "date_search_90d.json"), "w"), indent=1)
    save_facts()
    for i in OURS:
        s = FACTS["srlc"]["per_ingredient"][i]
        print(f"{i:14} products={s['products']:2} entries={s['entries']:3} since={s['first']} last={s['last']} "
              f"AR/WP/BW entries={s['safety_entries']} with underlined terms={s['safety_entries_underlined']}")
    print("90-day date search rows (all drugs):", len(drows))


def summarize_srlc(ing, rows, details):
    ents = []
    for r in rows:
        if not r["id"]:
            continue
        # The name search is a substring search: keep products whose ingredient list holds our ingredient.
        for e in details[r["id"]]["entries"]:
            ents.append((r, e))
    dates = sorted(dt.datetime.strptime(e["date"], "%m/%d/%Y").date() for _, e in ents)
    safety = [(r, e) for r, e in ents if any(re.match(r"^(5|6|Boxed|BOXED)", s["section"]) or
                                              s["section"].startswith(("Boxed", "Warnings", "Adverse"))
                                              or re.search(r"Warnings|Adverse|Boxed", s["section"])
                                              for s in e["sections"])]
    und = [(r, e) for r, e in safety if any(s["underlined"] for s in e["sections"])]
    secs = C.Counter(re.sub(r"^\d+\s*", "", s["section"]) for _, e in ents for s in e["sections"])
    years = C.Counter(d.year for d in dates)
    return {"products": len({r["id"] for r in rows if r["id"]}),
            "single_ingredient_products": len({r["id"] for r in rows if r["id"] and r["ingredient"].lower().strip() == ing}),
            "entries": len(ents), "first": str(dates[0]) if dates else None, "last": str(dates[-1]) if dates else None,
            "entries_90d": sum(1 for d in dates if d >= WINDOW_START), "per_year": dict(sorted(years.items())),
            "sections": dict(secs.most_common()), "safety_entries": len(safety), "safety_entries_underlined": len(und),
            "appl_nos": sorted({r["appl_no"] for r in rows})}


SRLC_SALTS = SALTS[:-3] + r"|recombinant|synthetic|polistirex|maleate|methylbromide)\b"


def srlc_ings(s):
    return {re.sub(SRLC_SALTS, "", p.lower()).strip() for p in s.split(";")}


def sec_kind(name):
    n = name.lower()
    if "boxed" in n: return "BW"
    if re.match(r"^\s*4\b", n) or "contraindication" in n: return "CI"
    if re.match(r"^\s*5\b", n) or "warnings" in n: return "WP"
    if re.match(r"^\s*6\b", n) or "adverse reactions" in n: return "AR"
    if re.match(r"^\s*17\b", n) or "pci/pi/mg" in n: return "MG"
    return "other"


def step_srlcan():
    """Second pass on the SrLC pages: exact ingredient match, reference products, additions, lag to DailyMed."""
    det = json.load(open(os.path.join(OUT, "srlc", "details.json")))
    out = {}
    for ing in OURS:
        prods = {k: v for k, v in det.items() if ing in srlc_ings(v["meta"]["ingredient"])}
        false = {k: v["meta"]["ingredient"] for k, v in det.items()
                 if ing in v["meta"]["ingredient"].lower() and ing not in srlc_ings(v["meta"]["ingredient"])}
        single = {k for k, v in prods.items() if srlc_ings(v["meta"]["ingredient"]) == {ing}}
        ents = [(k, e) for k, v in prods.items() for e in v["entries"]]
        dates = [dt.datetime.strptime(e["date"], "%m/%d/%Y").date() for _, e in ents]
        kinds = C.Counter(sec_kind(s["section"]) for _, e in ents for s in e["sections"])
        ref = FACTS["refs"][ing]["ref"]
        ref_ids = [k for k, v in prods.items() if v["meta"]["appl_no"].lstrip("0") == ref["appl"].lstrip("ANDBLA").lstrip("0")]
        hist = history(ref["setid"])
        vers = sorted((dm_date(v["published_date"]), int(v["spl_version"])) for v in hist)
        ref_entries = []
        for k in ref_ids:
            for e in det[k]["entries"]:
                d = dt.datetime.strptime(e["date"], "%m/%d/%Y").date()
                nxt = next(((vd, vn) for vd, vn in vers if vd >= d), None)
                adds = {}
                for s in e["sections"]:
                    kd = sec_kind(s["section"])
                    if kd in ("BW", "WP", "AR", "CI") and s["underlined"]:
                        adds.setdefault(kd, []).extend(u[:160] for u in s["underlined"])
                ref_entries.append({"date": str(d), "supp": e["supp"], "kinds": sorted({sec_kind(s["section"]) for s in e["sections"]}),
                                    "additions": adds, "dailymed_next_version": [str(nxt[0]), nxt[1]] if nxt else None,
                                    "lag_days": (nxt[0] - d).days if nxt else None})
        ref_entries.sort(key=lambda x: x["date"], reverse=True)
        lags = [x["lag_days"] for x in ref_entries if x["lag_days"] is not None and x["date"] >= str(vers[0][0])]
        out[ing] = {"products_exact": len(prods), "single_ingredient_products": len(single),
                    "false_substring_hits": sorted(set(false.values())), "entries": len(ents),
                    "entries_since_2016": sum(1 for d in dates if d.year >= 2016),
                    "first": str(min(dates)) if dates else None, "last": str(max(dates)) if dates else None,
                    "entries_90d": sum(1 for d in dates if d >= WINDOW_START),
                    "per_year": dict(sorted(C.Counter(d.year for d in dates).items())),
                    "section_kinds": dict(kinds), "ref_appl": ref["appl"], "ref_products_found": len(ref_ids),
                    "ref_entries": ref_entries, "ref_lag_days": lags,
                    "ref_history_from": str(vers[0][0]) if vers else None,
                    "ref_versions_total": len(vers),
                    "ref_versions_last_365d": sum(1 for vd, _ in vers if vd >= TODAY - dt.timedelta(days=365)),
                    "ref_history_gaps": sorted(set(range(1, max(v for _, v in vers) + 1)) - {v for _, v in vers})[:30] if vers else []}
        print(f"{ing:14} exact={len(prods):2} single={len(single):2} false={len(false)} entries={len(ents):3} "
              f"last={out[ing]['last']} 90d={out[ing]['entries_90d']} ref_products={len(ref_ids)} ref_entries={len(ref_entries)} lags={lags[:8]}")
    # De-duplicated across ingredients (combination products appear under two of ours)
    keep = {k: v for k, v in det.items() if srlc_ings(v["meta"]["ingredient"]) & set(OURS)}
    uniq = {(k, e["date"], e["supp"]) for k, v in keep.items() for e in v["entries"]}
    by_year = C.Counter(e[1][-4:] for e in uniq)
    clusters = {y: {"entries": by_year[y], "dates": len({e[1] for e in uniq if e[1].endswith(y)}),
                    "top_date": C.Counter(e[1] for e in uniq if e[1].endswith(y)).most_common(1)[0]} for y in sorted(by_year)}
    print("products:", len(keep), "unique entries:", len(uniq), "2025:", clusters.get("2025"), "2026:", clusters.get("2026"))
    # 90-day date search across all drugs
    drows = json.load(open(os.path.join(OUT, "srlc", "date_search_90d.json")))
    ours = [r for r in drows if any(i in srlc_ings(r[1]) for i in OURS)]
    upd = C.Counter(r[5] for r in drows)
    lag = [(dt.datetime.strptime(r[5], "%m/%d/%Y") - dt.datetime.strptime(r[4], "%m/%d/%Y")).days for r in drows]
    wk = C.Counter(dt.datetime.strptime(r[4], "%m/%d/%Y").date().isocalendar()[1] for r in drows)
    FACTS["srlcan"] = {"per_ingredient": out, "products_ours": len(keep), "unique_entries": len(uniq),
                       "clusters_by_year": clusters, "date_search": {
        "rows": len(drows), "ours": ours, "distinct_db_update_dates": len(upd),
        "db_update_dates": sorted(upd, key=lambda s: dt.datetime.strptime(s, "%m/%d/%Y")),
        "approval_to_db_lag_days": {"min": min(lag), "median": sorted(lag)[len(lag) // 2], "max": max(lag)},
        "per_iso_week": dict(sorted(wk.items()))}}
    print("90d rows:", len(drows), "ours:", [(r[0], r[4]) for r in ours], "db update dates:", len(upd),
          "lag:", FACTS["srlcan"]["date_search"]["approval_to_db_lag_days"])
    save_facts()


# --------------------------------------------------------------------------- OnSIDES
def read_csv(name):
    path = os.path.join(DATA, "_onsides", "v3.1.1", "csv", name)
    with open(path, encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)


def label_sections_text(setid):
    """Plain text of the 4 safety parents (everything nested), per parent code."""
    root = get_xml(setid)
    out = {}
    for s in top_sections(root):
        if code_of(s) in PARENTS:
            out.setdefault(PARENTS[code_of(s)], []).append(text_of(s))
    return {k: " ".join(v) for k, v in out.items()}


def step_onsides():
    labels = list(read_csv("product_label.csv"))
    src = C.Counter(l["source"] for l in labels)
    us = [l for l in labels if l["source"] == "US"]
    key_ok = sum(1 for l in us if re.fullmatch(r"[0-9a-f-]{36}\.\d+", l["source_product_id"]))
    us_by_setid = {}
    for l in us:
        sid, _, ver = l["source_product_id"].rpartition(".")
        us_by_setid.setdefault(sid, []).append((int(ver), l["label_id"], l["source_product_name"]))
    ours = json.load(open(os.path.join(OUT, "our_setids.json")))
    found = {s: sorted(us_by_setid[s])[-1] for s in ours if s in us_by_setid}
    # Current DailyMed version of every one of our labels (cached list calls from the census step)
    current = {}
    for ing in OURS:
        for l in dm_all(f"{DM}/spls.json?drug_name={ing}")[0]:
            current[l["setid"]] = (l["spl_version"], l["published_date"], l["title"])
    behind = C.Counter()
    for sid, (ver, _, _) in found.items():
        cv = current.get(sid, (None,))[0]
        if cv is not None:
            gap = int(cv) - ver
            behind["0 (current)" if gap == 0 else "1" if gap == 1 else "2-4" if gap <= 4 else "5+" if gap > 0 else "negative"] += 1
    meddra = {r["meddra_id"]: (r["meddra_name"], r["meddra_term_type"]) for r in read_csv("vocab_meddra_adverse_effect.csv")}
    want_ids = {lid for _, lid, _ in found.values()}
    effects = C.defaultdict(list); n_eff = 0; sec_all = C.Counter(); meth = C.Counter()
    seen = set(); dup = 0; dup_labels = C.Counter()
    for r in read_csv("product_adverse_effect.csv"):
        n_eff += 1; sec_all[r["label_section"]] += 1; meth[r["match_method"]] += 1
        k = (r["product_label_id"], r["effect_meddra_id"], r["label_section"])
        if k in seen:
            dup += 1; dup_labels[r["product_label_id"]] += 1; continue
        seen.add(k)
        if r["product_label_id"] in want_ids:
            effects[r["product_label_id"]].append(r)
    refs = {i: FACTS["refs"][i]["ref"] for i in OURS if FACTS["refs"][i]["ref"]}
    ref_rows = {}
    for ing, r in refs.items():
        sid = r["setid"]; row = {"setid": sid, "ref_title": r["title"], "in_onsides": sid in found}
        use = sid if sid in found else None
        if not use:
            # Closest stand-in: an OnSIDES copy of the same brand/product (repackager or older setid).
            brand = re.split(r"[ (]", r["title"])[0].lower()
            cands = [s for s in found if ing in ours.get(s, []) and brand in found[s][2].lower()]
            row["proxy_rule"] = "same brand"
            if not cands:
                # No copy of the brand: same ingredient alone, same dosage form (e.g. "TABLET, FILM COATED, EXTENDED RELEASE")
                form = re.sub(r"\s*\[.*$", "", r["title"].split(")")[-1]).strip().lower()
                cands = [s for s in found if ours.get(s) == [ing] and form and form in found[s][2].lower()
                         and " and " not in found[s][2].lower()]
                row["proxy_rule"] = f"same ingredient + form '{form}'"
            if cands:
                dated = []
                for s in cands:
                    h = history(s)
                    d = next((dm_date(v["published_date"]) for v in h if int(v["spl_version"]) == found[s][0]), None)
                    dated.append((d or dt.date(1900, 1, 1), s))
                use = max(dated)[1]
                row["proxy_candidates"] = len(cands)
        if use:
            ver, lid, name = found[use]
            h = history(use)
            vdate = next((v["published_date"] for v in h if int(v["spl_version"]) == ver), None)
            effs = effects[lid]
            row.update({"used_setid": use, "used_name": name, "onsides_version": ver, "onsides_version_date": vdate,
                        "current_version_of_used": current.get(use, (None,))[0],
                        "n_effects": len(effs), "n_terms": len({e["effect_meddra_id"] for e in effs}),
                        "by_section": dict(C.Counter(e["label_section"] for e in effs)),
                        "by_term_type": dict(C.Counter(meddra.get(e["effect_meddra_id"], ("?", "?"))[1] for e in effs))})
        ref_rows[ing] = row
        print(f"{ing:14} in={row['in_onsides']!s:5} used={row.get('used_name','-')[:60]:60} v{row.get('onsides_version','-')} "
              f"({row.get('onsides_version_date','-')}) terms={row.get('n_terms','-')}")
    # Term-level comparison for the two gold-set drugs: OnSIDES vs current label text vs our gold-set draft
    gold = list(csv.DictReader(open(GOLD, newline="", encoding="utf-8"))) if os.path.exists(GOLD) else []
    compare = {}
    sec_map = {"AR": "Adverse Reactions", "WP": "Warnings and Precautions", "BW": "Boxed Warning"}
    for ing in ("semaglutide", "oxycodone"):
        rr = ref_rows.get(ing, {})
        if not rr.get("used_setid"):
            continue
        lid = found[rr["used_setid"]][1]
        cur = label_sections_text(rr["setid"])
        allcur = " ".join(cur.values()).lower()
        used_raw = " ".join(label_sections_text(rr["used_setid"]).values())  # current text of the stand-in label
        used_txt = used_raw.lower()
        gold_terms = {x["reaction_as_written"].lower() for x in gold if x["ingredient"] == ing and x["counts_as_labeled"] == "yes"}
        gold_in_used = sum(1 for t in gold_terms if re.search(r"\b" + re.escape(t) + r"\b", used_txt))
        g_yes = {x["faers_pt"].lower() for x in gold if x["ingredient"] == ing and x["counts_as_labeled"] == "yes" and x["faers_pt"]}
        g_no = {x["faers_pt"].lower() for x in gold if x["ingredient"] == ing and x["counts_as_labeled"] == "no" and x["faers_pt"]} - g_yes
        rows = []
        for e in effects[lid]:
            name, tt = meddra.get(e["effect_meddra_id"], ("?", "?"))
            sec_text = cur.get(sec_map.get(e["label_section"], ""), "")
            wb = re.compile(r"\b" + re.escape(name.lower()) + r"\b")
            rows.append({"meddra_id": e["effect_meddra_id"], "term": name, "term_type": tt, "section": e["label_section"],
                         "pred1": round(float(e["pred1"] or 0), 2), "method": e["match_method"],
                         "word_in_current_same_section": bool(wb.search(sec_text.lower())),
                         "word_in_current_4_sections": bool(wb.search(allcur)),
                         "word_in_used_label": bool(wb.search(used_txt)),
                         "case_sensitive_in_used_label": name in used_raw,
                         "in_gold_labeled": name.lower() in g_yes, "in_gold_trap_only": name.lower() in g_no})
        rows.sort(key=lambda x: (x["section"], x["term"]))
        # Kept in git-ignored data only: MedDRA term names are licensed (compare, never republish).
        with open(os.path.join(OUT, f"onsides_terms_{ing}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        terms = {r["term"].lower() for r in rows}
        compare[ing] = {"rows": len(rows), "unique_terms": len(terms),
                        "llt_share": round(100 * sum(r["term_type"] == "LLT" for r in rows) / len(rows), 1),
                        "word_in_current_same_section": sum(r["word_in_current_same_section"] for r in rows),
                        "word_in_current_4_sections": sum(r["word_in_current_4_sections"] for r in rows),
                        "word_in_used_label": sum(r["word_in_used_label"] for r in rows),
                        "acronym_case_mismatch": sorted({r["term"] for r in rows if r["term"].isupper() and not r["case_sensitive_in_used_label"]}),
                        "soc_heading_like": sorted({r["term"] for r in rows if r["term"].lower().endswith("disorder")}),
                        "gold_terms_as_written": len(gold_terms), "gold_terms_found_in_used_label_text": gold_in_used,
                        "used_label_chars": len(used_raw), "current_ref_chars": len(allcur),
                        "gold_labeled_pts": len(g_yes), "overlap_with_gold_labeled": len(terms & g_yes),
                        "onsides_terms_in_gold_trap_only": sorted(terms & g_no),
                        "gold_labeled_missing_from_onsides": len(g_yes - terms),
                        "onsides_not_in_gold": len(terms - g_yes)}
        print(ing, compare[ing])
    FACTS["onsides"] = {"labels_by_source": dict(src), "us_labels": len(us), "us_key_is_setid_dot_version": key_ok,
                        "us_unique_setids": len(us_by_setid),
                        "us_setids_with_2plus_versions": sum(1 for v in us_by_setid.values() if len(v) > 1),
                        "effects_rows": n_eff, "effects_exact_duplicates": dup, "labels_with_duplicates": len(dup_labels),
                        "effects_by_section": dict(sec_all), "match_method": dict(meth),
                        "meddra_vocab_rows": len(meddra), "meddra_by_type": dict(C.Counter(t for _, t in meddra.values())),
                        "our_setids_total": len(ours), "our_setids_in_onsides": len(found),
                        "our_versions_behind": dict(behind), "refs": ref_rows, "compare": compare,
                        "high_confidence_rows": sum(1 for _ in read_csv("high_confidence.csv"))}
    print("our setids in OnSIDES:", len(found), "/", len(ours), " versions behind:", dict(behind),
          " duplicate effect rows:", dup, "in", len(dup_labels), "labels")
    save_facts()


# --------------------------------------------------------------------------- gold set helpers
def step_textdump():
    """Write the 4 safety sections of the 2 gold-set labels as plain text, one paragraph per line."""
    for ing in ("semaglutide", "oxycodone"):
        r = FACTS["refs"][ing]["ref"]
        root = get_xml(r["setid"])
        lines = [f"# {r['title']}  setid={r['setid']} v{r['spl_version']} {r['published_date']}"]
        for s in top_sections(root):
            if code_of(s) not in PARENTS:
                continue
            for sub, depth in walk(s):
                lines.append(f"\n{'#' * (depth + 1)} [{code_of(sub)}] {title_of(sub)}")
                for el in sub.findall("v3:text/*", NS):
                    tag = el.tag.split("}")[1]
                    if tag == "table":
                        for tr in el.iter(f"{{{NS['v3']}}}tr"):
                            lines.append("| " + " | ".join(text_of(td) for td in tr if td.tag.endswith(("td", "th"))))
                    elif tag == "list":
                        for it in el.findall("v3:item", NS):
                            lines.append("- " + text_of(it))
                    else:
                        lines.append(text_of(el))
        open(os.path.join(OUT, "text", f"{ing}.txt"), "w").write("\n".join(lines))
        print(ing, len(lines), "lines ->", os.path.join(OUT, "text", f"{ing}.txt"))


def norm(s):
    """Whitespace/punctuation-insensitive form, so XML element joins ("Renal : acute") match the label as read."""
    s = s.replace("’", "'").replace("–", "-").replace("—", "-").replace("•", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:)\]])", r"\1", s)
    s = re.sub(r"([(\[])\s+", r"\1", s)
    return s.strip().lower()


def faers_pts():
    pts = C.Counter()
    for q in ("2026q1", "2026q2"):
        path = os.path.join(DATA, "_faers_bulk", q, "ASCII", f"REAC{q[2:4]}{q[4:].upper()}.txt")
        with open(path, encoding="latin-1") as f:
            next(f)
            for line in f:
                p = line.rstrip("\r\n").split("$")
                if len(p) > 2:
                    pts[p[2].strip().lower()] += 1
    return pts


def step_goldcheck():
    rows = list(csv.DictReader(open(GOLD, newline="", encoding="utf-8")))
    pts = faers_pts()
    res = {}
    for ing in ("semaglutide", "oxycodone"):
        r = FACTS["refs"][ing]["ref"]
        full = norm(text_of(get_xml(r["setid"])))
        mine = [x for x in rows if x["ingredient"] == ing]
        bad = [x for x in mine if norm(x["quote"]) not in full]
        term_missing = [x for x in mine if norm(x["reaction_as_written"]) not in norm(x["quote"])]
        pt_rows = [x for x in mine if x["faers_pt"]]
        pt_unseen = sorted({x["faers_pt"] for x in pt_rows if pts[x["faers_pt"].lower()] == 0})
        labeled = {x["faers_pt"] for x in mine if x["counts_as_labeled"] == "yes" and x["faers_pt"]}
        only_trap = {x["faers_pt"] for x in mine if x["counts_as_labeled"] == "no" and x["faers_pt"]} - labeled
        res[ing] = {"rows": len(mine), "quotes_not_found": len(bad), "term_not_in_quote": len(term_missing),
                    "by_context": dict(C.Counter(x["context"] for x in mine)),
                    "by_section": dict(C.Counter(x["section"] for x in mine)),
                    "rows_counting": sum(1 for x in mine if x["counts_as_labeled"] == "yes"),
                    "unique_labeled_pts": len(labeled), "trap_only_pts": sorted(only_trap),
                    "pts_not_seen_in_faers_2026h1": pt_unseen, "pts_checked": len({x["faers_pt"] for x in pt_rows})}
        for x in bad:
            print("  QUOTE NOT FOUND:", ing, x["reaction_as_written"], "|", x["quote"][:90])
        print(ing, json.dumps(res[ing], indent=1))
    FACTS["gold"] = res
    save_facts()


STEPS = {"refs": step_refs, "sections": step_sections, "census": step_census, "dailyzip": step_dailyzip,
         "srlc": step_srlc, "srlcan": step_srlcan, "onsides": step_onsides, "textdump": step_textdump, "goldcheck": step_goldcheck}

if __name__ == "__main__":
    for s in sys.argv[1:] or ["refs", "sections", "census", "dailyzip", "srlc", "onsides", "textdump"]:
        print(f"\n=== {s}")
        STEPS[s]()
