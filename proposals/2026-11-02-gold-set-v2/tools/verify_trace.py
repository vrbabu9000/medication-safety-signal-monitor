"""Independently re-check one or more traces against the frozen evidence bytes.

    python3 verify_trace.py T01 [T02 ...]   |   python3 verify_trace.py all

Deliberately does not import build_trace.py: values are re-read from the raw files by their locators.
Writes ../verification/<trace>.json. Exit code 1 if any check fails.
"""
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SH = ROOT / "shared"
NS = {"v3": "urn:hl7-org:v3"}
SCOPE = {"34066-1", "34070-3", "43685-7", "34071-1", "42232-9", "34084-4"}


def ws(s): return re.sub(r"\s+", " ", s).strip()
def alnum(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def raw(tid, key, ext="json"): return (SH / "evidence" / tid / f"{key}.{ext}").read_bytes()
def js(tid, key): return json.loads(raw(tid, key))


def verify(tid):
    checks = []

    def ck(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    man = json.loads((SH / "source-manifest.json").read_text())["sources"]
    rows = {r["step"]: r for r in (json.loads(l) for l in (ROOT / "claude" / "traces" / f"{tid}.jsonl").read_text().splitlines())}
    qb = (SH / "questions" / f"{tid}.json").read_bytes()
    ck("8 steps answered", sorted(rows) == [f"S{i}" for i in range(1, 9)], sorted(rows))
    for sid, m in man.items():
        if m["trace_id"] == tid:
            ok = m["status"] == "captured" and hashlib.sha256((SH / m["evidence_file"]).read_bytes()).hexdigest() == m["sha256"]
            ck(f"hash {sid}", ok, m["status"])
            ck(f"no api key stored {sid}", "api_key=" not in m["requested_url"] or "api_key=REDACTED" in m["requested_url"])
    for r in rows.values():
        for s, h in r["source_sha256"].items():
            ck(f"{r['case_id']} cites manifest hash for {s}", man[s]["sha256"] == h)
        ck(f"{r['case_id']} resolved and pending review", r["answer_status"] == "resolved" and r["human_review_status"] == "pending")

    # S1
    a = rows["S1"]["answer"]
    bn = js(tid, "s1_rx_brand")["idGroup"]["rxnormId"][0]
    pr = js(tid, "s1_rx_brand_props")["properties"]
    ins = sorted((p["rxcui"], p["name"]) for p in js(tid, "s1_rx_ingredients")["relatedGroup"]["conceptGroup"][0]["conceptProperties"])
    ck("S1 brand rxcui", a["brand_rxcui"] == bn == pr["rxcui"], bn)
    ck("S1 tty", a["brand_tty"] == pr["tty"] == "BN", pr["tty"])
    ck("S1 ingredients", sorted((i["rxcui"], i["name"]) for i in a["ingredients"]) == ins, ins)
    ck("S1 multi flag", a["multi_ingredient"] == (len(ins) > 1))
    for rc, _ in ins:
        rv = js(tid, f"s1_rx_reverse_{rc}")
        ck(f"S1 reverse IN {rc} -> brand", any(c["rxcui"] == bn for g in rv["relatedGroup"]["conceptGroup"] for c in g.get("conceptProperties") or []))
    # S2
    a = rows["S2"]["answer"]
    n = js(tid, "s2_ndc")["results"][0]
    pk = [p for p in n["packaging"] if p["package_ndc"] == a["package_ndc"]]
    xml = raw(tid, "s4_label", "xml")
    setid = re.search(rb'<setId root="([^"]+)"', xml).group(1).decode()
    ck("S2 labeler/category/app", (a["labeler_name"], a["marketing_category"], a["application_number"]) == (n["labeler_name"], n["marketing_category"], n["application_number"]))
    ck("S2 package description", len(pk) == 1 and pk[0]["description"] == a["package_description"])
    ck("S2 set id link", a["spl_set_id_matches_s4"] == ((n.get("openfda", {}).get("spl_set_id") or [None])[0] == setid), setid)
    # S3
    a = rows["S3"]["answer"]
    d = js(tid, "s3_drugsfda")["results"][0]
    ck("S3 sponsor", a["sponsor_name"] == d["sponsor_name"], d["sponsor_name"])
    ck("S3 products", sorted(p["product_number"] for p in a["products"]) == sorted(p["product_number"] for p in d["products"]))
    ck("S3 app link", d["application_number"] == rows["S2"]["answer"]["application_number"])
    # S4
    r4 = rows["S4"]
    loc = r4["evidence_locators"][f"{tid}.s4_label"] if f"{tid}.s4_label" in r4["evidence_locators"] else r4["evidence_locators"]["s4_label"]
    sec_id = re.search(r"@root='([^']+)'", loc["xml_path"]).group(1)
    root = ET.fromstring(xml)
    sec = [s for s in root.iter(f"{{{NS['v3']}}}section") if (s.find("v3:id", NS) is not None and s.find("v3:id", NS).get("root") == sec_id)]
    ck("S4 section found once by id", len(sec) == 1, sec_id)
    direct = ws(" ".join("".join(t.itertext()) for t in sec[0].findall("v3:text", NS)))
    title = ws("".join(sec[0].find("v3:title", NS).itertext()))
    ck("S4 heading matches", title == loc["heading"], title)
    ck("S4 quote verbatim in passage", r4["supporting_quote_or_value"] in direct)
    q4 = json.loads(qb)["questions"][3]
    ck("S4 target phrase in passage", q4["inputs"]["target"].lower() in direct.lower(), q4["inputs"]["target"])
    ck("S4 class allowed", r4["answer"] in q4["answer_format"])
    # S5
    a = rows["S5"]["answer"]
    h = raw(tid, "s5_srlc_detail", "html").decode("utf-8", "replace")
    flat = ws(html.unescape(re.sub(r"<[^>]+>", " ", h)))
    app = rows["S2"]["answer"]["application_number"]
    ck("S5 page header names application", re.search(r"\((NDA|BLA)-0*" + app[3:].lstrip("0") + r"\)", flat) is not None, app)
    unders = [ws(html.unescape(re.sub(r"<[^>]+>", " ", u))) for u in re.findall(r"<u>(.*?)</u>", h, flags=re.S)]
    ck("S5 passage is underlined text on the page", a["underlined_passage"] in unders)
    ck("S5 entry date + supplement on page", f"{a['entry_date']}" in flat and a["supplement"].split("-")[1] in flat)
    # Selection rule: no newer entry has underlined text under Boxed Warning or a section 4/5/6 heading.
    import datetime as _dt
    chunks = re.split(r"<h3[^>]*accordion-header[^>]*>", h)[1:]
    chosen = _dt.datetime.strptime(a["entry_date"], "%m/%d/%Y")
    newer_hits = []
    for c in chunks:
        dm = re.match(r"\s*(\d\d/\d\d/\d{4})", c)
        if not dm or _dt.datetime.strptime(dm.group(1), "%m/%d/%Y") <= chosen:
            continue
        for hm in re.finditer(r"<h4>(.*?)</h4>(.*?)(?=<h4>|$)", c, flags=re.S):
            name = ws(html.unescape(re.sub(r"<[^>]+>", " ", hm.group(1))))
            if (name[:1] in "456" or name.startswith("Boxed")) and "<u>" in hm.group(2):
                newer_hits.append((dm.group(1), name))
    ck("S5 no newer entry with underlined Boxed/4/5/6 text", not newer_hits, newer_hits)
    labeltext = alnum(" ".join(root.itertext()))
    ck("S5 presence in S4 label", a["present_in_s4_label"] == (alnum(a["underlined_passage"]) in labeltext))
    # S6
    a = rows["S6"]["answer"]
    ck("S6 substance", a["active_substance"] == js(tid, "s6_faers_substance")["results"][0]["term"])
    ck("S6 substance total", a["substance_report_count"] == js(tid, "s6_faers_total")["meta"]["results"]["total"])
    ck("S6 brand total", a["brand_report_count"] == js(tid, "s6_faers_brand_total")["meta"]["results"]["total"])
    for k in ("s6_faers_total", "s6_faers_brand_total"):
        ck(f"S6 {k} holds no report records", js(tid, k)["results"] == [])
    rx = js(tid, "s6_faers_brand_reactions")["results"]
    ck("S6 terms and counts", [(x["term"], x["count"]) for x in a["top_terms_brand"]] == [(x["term"], x["count"]) for x in rx])
    scope = " ".join(ws(" ".join(s.itertext())) for s in root.iter(f"{{{NS['v3']}}}section")
                     if s.find("v3:code", NS) is not None and s.find("v3:code", NS).get("code") in SCOPE).lower()
    lm = rows["S6"]["supporting_quote_or_value"]["label_matches"]
    for x in a["top_terms_brand"]:
        t = x["term"].lower()
        vs = {t, t.replace("oe", "e").replace("ae", "e")}
        found = any(re.search(r"(?<![a-z])" + re.escape(v) + r"(?![a-z])", scope) for v in vs)
        ck(f"S6 label match '{x['term']}'", x["found_in_label_scope"] == found)
        if found:
            ck(f"S6 quote verbatim '{x['term']}'", ws(lm[x["term"]]["quote"]).lower() in scope)
    # S7
    a = rows["S7"]["answer"]
    rk = "s7_recall_app" if a["query_level"] == "application" else "s7_recall_ingredient"
    rd = js(tid, rk)
    r0 = rd["results"][0]
    ck("S7 most recent record", r0["report_date"] == max(x["report_date"] for x in rd["results"]))
    ck("S7 fields", (a["recall_number"], a["classification"], a["reason_for_recall"], a["status_as_reported"], a["report_date"]) ==
       (r0["recall_number"], r0["classification"], r0["reason_for_recall"], r0["status"], r0["report_date"]))
    own = (r0.get("product_description") or "") + " " + (r0.get("code_info") or "")
    pkg = rows["S2"]["answer"]["package_ndc"]
    ck("S7 package named in record text", a["package_named_in_record"] == (pkg.replace("-", "") in own.replace("-", "")), pkg)
    if a["query_level"] == "ingredient":
        ck("S7 application-level query was empty", not js(tid, "s7_recall_app").get("results"))
    # S8
    a = rows["S8"]["answer"]
    st = js(tid, "s8_trial")
    gi = int(rows["S8"]["evidence_locators"][f"{tid}.s8_trial"].rsplit("/", 1)[1]) if f"{tid}.s8_trial" in rows["S8"]["evidence_locators"] else int(rows["S8"]["evidence_locators"]["s8_trial"].rsplit("/", 1)[1])
    g = st["resultsSection"]["adverseEventsModule"]["eventGroups"][gi]
    ck("S8 nct + status", (a["nct_id"], a["overall_status"]) == (st["protocolSection"]["identificationModule"]["nctId"], st["protocolSection"]["statusModule"]["overallStatus"]))
    ck("S8 group values", (a["group_id"], a["group_title"], a["seriousNumAffected"], a["seriousNumAtRisk"]) == (g["id"], g["title"], g.get("seriousNumAffected"), g.get("seriousNumAtRisk")))
    srch = [s["protocolSection"]["identificationModule"]["nctId"] for s in js(tid, "s8_trials_search")["studies"]]
    ck("S8 study is in captured search", a["nct_id"] in srch, srch.index(a["nct_id"]) if a["nct_id"] in srch else None)
    terms = [rows["S1"]["answer"]["ingredients"][i]["name"].lower() for i in range(len(rows["S1"]["answer"]["ingredients"]))] + [json.loads(qb)["brand"].lower()]
    ck("S8 group title names drug", any(x in g["title"].lower() for x in terms), g["title"])
    earlier = []
    for s in js(tid, "s8_trials_search")["studies"]:
        if s["protocolSection"]["identificationModule"]["nctId"] == a["nct_id"]:
            break
        for eg in s.get("resultsSection", {}).get("adverseEventsModule", {}).get("eventGroups", []):
            if any(x in (eg.get("title") or "").lower() for x in terms) and (eg.get("seriousNumAtRisk") or 0) > 0:
                earlier.append(s["protocolSection"]["identificationModule"]["nctId"])
    ck("S8 no earlier study in search order qualifies", not earlier, earlier)

    out = {"trace_id": tid, "questions_sha256": hashlib.sha256(qb).hexdigest(), "checks": checks,
           "passed": sum(c["pass"] for c in checks), "failed": [c for c in checks if not c["pass"]]}
    (ROOT / "verification").mkdir(exist_ok=True)
    (ROOT / "verification" / f"{tid}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{tid}: {out['passed']}/{len(checks)} checks passed" + (f" — FAILED: {[c['check'] for c in out['failed']]}" if out["failed"] else ""))
    return not out["failed"]


if __name__ == "__main__":
    ids = sys.argv[1:]
    if ids == ["all"]:
        ids = sorted(p.stem for p in (ROOT / "claude" / "traces").glob("T*.jsonl"))
    sys.exit(0 if all([verify(t) for t in ids]) else 1)
