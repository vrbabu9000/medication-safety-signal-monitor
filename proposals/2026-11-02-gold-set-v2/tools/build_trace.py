"""Build one cross-source trace in three separate stages.

    python3 build_trace.py capture   T01   # fetch all 8 sources, run identity guards, write evidence + manifest rows
    python3 build_trace.py questions T01   # write and hash the fixed-template questions (needs the S4 input in traces.json)
    python3 build_trace.py answers   T01   # derive answers from the frozen evidence (+ Claude's S4 annotation)

Inputs: ../traces.json (one row per trace), ../claude/s4-annotations.json (Claude's label judgement).
Every stage reads only files written by the earlier stage; answers never refetch.
FAERS evidence is aggregate count responses only (no report records are requested or stored).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
import v2lib as L

NS = {"v3": "urn:hl7-org:v3"}
# LOINC section codes counted as "the label mentions it" for this dataset (dataset rule, see findings.md).
IN_SCOPE = {"34066-1": "Boxed Warning", "34070-3": "Contraindications", "43685-7": "Warnings and Precautions",
            "34071-1": "Warnings", "42232-9": "Precautions", "34084-4": "Adverse Reactions"}
CLASSES = ["reaction_or_warning", "underlying_condition_or_risk_factor", "symptom_of_other_condition",
           "administration_instruction", "contraindicated_population", "exposure_factor", "co_medication_risk_factor"]

TRACES = {t["trace_id"]: t for t in json.loads((L.ROOT / "traces.json").read_text())["traces"]}


def tdir(tid):
    p = L.EVIDENCE / tid
    p.mkdir(parents=True, exist_ok=True)
    return p


def manifest():
    return json.loads(L.MANIFEST.read_text()) if L.MANIFEST.exists() else {"sources": {}}


def save_manifest(m):
    L.MANIFEST.write_text(json.dumps(m, indent=1, sort_keys=True) + "\n")


# ----------------------------------------------------------------------------- capture
def capture(tid, key, u, kind, guard, m, data=None, browser=False):
    """Fetch, apply the identity guard, store bytes. A failed guard is stored under shared/rejected/, never as evidence."""
    f = L.fetch(u, data=data, browser=browser)
    sid = f"{tid}.{key}"
    row = {"source_id": sid, "trace_id": tid, "step_key": key, "kind": kind, "requested_url": f.requested_url,
           "method": "POST" if data else "GET", "post_form": data, "http_status": f.status, "http_headers": f.headers,
           "retrieved_at_utc": f.retrieved_at_utc, "openfda_api_key_used": bool(L.api_key()) and u.startswith(L.OPENFDA)}
    if not f.ok:
        row.update(status="fetch_failed", error=f.error)
        m["sources"][sid] = row
        raise SystemExit(f"{sid}: fetch failed ({f.error}) — trace not built; nothing is inferred from a failure")
    ok, detail = guard(f.body)
    ext = {"json": "json", "xml": "xml", "html": "html"}[kind]
    if not ok:
        rej = L.SHARED / "rejected" / tid
        rej.mkdir(parents=True, exist_ok=True)
        (rej / f"{key}.{ext}").write_bytes(f.body)
        row.update(status="rejected_identity_guard", identity_guard=detail, sha256=L.sha256(f.body))
        m["sources"][sid] = row
        raise SystemExit(f"{sid}: identity guard failed: {detail}")
    path = tdir(tid) / f"{key}.{ext}"
    path.write_bytes(f.body)
    row.update(status="captured", identity_guard=detail, evidence_file=str(path.relative_to(L.SHARED)),
               sha256=L.sha256(f.body), bytes=len(f.body))
    if kind == "json":
        meta = json.loads(f.body).get("meta") if isinstance(json.loads(f.body), dict) else None
        if meta:
            row["source_metadata"] = {k: v for k, v in meta.items() if k in ("last_updated", "results")}
    m["sources"][sid] = row
    print(f"  captured {sid}: {len(f.body)} bytes — guard: {detail}")
    return f.body


def jguard(test):
    def g(body):
        try:
            return test(json.loads(body))
        except Exception as e:
            return False, f"guard error {type(e).__name__}: {e}"
    return g


def label_sections(xml_bytes):
    """Every <section> in document order: ordinal, code, title, ancestor codes, direct text, full text."""
    root = ET.fromstring(xml_bytes)
    out = []

    def walk(el, anc):
        for comp in el.findall("v3:component", NS):
            s = comp.find("v3:section", NS)
            if s is None:
                continue
            code = s.find("v3:code", NS)
            c = code.get("code") if code is not None else None
            title = s.find("v3:title", NS)
            sid = s.find("v3:id", NS)
            out.append({"ordinal": len(out), "section_id": sid.get("root") if sid is not None else None, "code": c,
                        "display": code.get("displayName") if code is not None else None,
                        "title": L.norm("".join(title.itertext())) if title is not None else "",
                        "ancestor_codes": anc,
                        "direct_text": L.norm(" ".join("".join(t.itertext()) for t in s.findall("v3:text", NS))),
                        "full_text": L.norm(" ".join(x for x in s.itertext()))})
            walk(s, anc + [c])
    body = root.find("v3:component/v3:structuredBody", NS)
    walk(body, [])
    return root, out


def stage_capture(tid):
    t = TRACES[tid]
    m = manifest()
    brand, app = t["brand"], t["application_number"]
    print(f"[{tid}] {brand} {app}")
    # S1 RxNorm
    b = capture(tid, "s1_rx_brand", L.url(L.RXNAV + "/rxcui.json", {"name": brand, "search": "0"}), "json",
                jguard(lambda d: (bool(d["idGroup"].get("rxnormId")), f"rxnormId={d['idGroup'].get('rxnormId')}")), m)
    bn = json.loads(b)["idGroup"]["rxnormId"][0]
    capture(tid, "s1_rx_brand_props", f"{L.RXNAV}/rxcui/{bn}/properties.json", "json",
            jguard(lambda d: (d["properties"]["name"].lower() == brand.lower(), f"name={d['properties']['name']} tty={d['properties']['tty']}")), m)
    # related.json returns relatedGroup.rxcui = null, so the body does not name the brand it answers for.
    # Guard = non-empty IN list here, plus a reverse capture per ingredient whose BN list must contain this brand.
    b = capture(tid, "s1_rx_ingredients", f"{L.RXNAV}/rxcui/{bn}/related.json?tty=IN", "json",
                jguard(lambda d: (bool(d["relatedGroup"]["conceptGroup"][0].get("conceptProperties")),
                                  f"{len(d['relatedGroup']['conceptGroup'][0]['conceptProperties'])} IN concepts (body rxcui is null; see reverse check)")), m)
    for p in json.loads(b)["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
        capture(tid, f"s1_rx_reverse_{p['rxcui']}", f"{L.RXNAV}/rxcui/{p['rxcui']}/related.json?tty=BN", "json",
                jguard(lambda d: (any(c["rxcui"] == bn for g in d["relatedGroup"]["conceptGroup"] for c in g.get("conceptProperties") or []),
                                  f"brand {bn} listed among BN concepts of ingredient {p['rxcui']}")), m)
    # S2 NDC
    pn = t["product_ndc"]
    capture(tid, "s2_ndc", L.url(L.OPENFDA + "/ndc.json", {"search": f'product_ndc:"{pn}"', "limit": "1"}), "json",
            jguard(lambda d: (d["results"][0]["product_ndc"] == pn and d["results"][0]["application_number"] == app
                              and d["results"][0]["brand_name"].lower() == brand.lower(),
                              f"product_ndc={d['results'][0]['product_ndc']} app={d['results'][0]['application_number']} brand={d['results'][0]['brand_name']}")), m)
    # S3 Drugs@FDA
    capture(tid, "s3_drugsfda", L.url(L.OPENFDA + "/drugsfda.json", {"search": f'application_number:"{app}"', "limit": "1"}), "json",
            jguard(lambda d: (d["results"][0]["application_number"] == app, f"application_number={d['results'][0]['application_number']}")), m)
    # S4 DailyMed (current version of the set id the NDC listing points to)
    setid = t["spl_set_id"]

    def g4(body):
        root = ET.fromstring(body)
        sid = root.find("v3:setId", NS).get("root")
        title = L.norm("".join(root.find("v3:title", NS).itertext()))
        ver = root.find("v3:versionNumber", NS).get("value")
        return sid == setid and brand.lower() in title.lower(), f"setId={sid} version={ver} brand_in_title={brand.lower() in title.lower()}"
    xb = capture(tid, "s4_label", f"{L.DAILYMED}/spls/{setid}.xml", "xml", g4, m)
    root, secs = label_sections(xb)
    meta = {k: root.find(f"v3:{k}", NS).attrib for k in ("setId", "versionNumber", "effectiveTime")}
    view = {"source_id": f"{tid}.s4_label", "original_sha256": L.sha256(xb), "spl": meta, "sections": secs,
            "note": "Deterministic parsing aid. The XML is authoritative."}
    (tdir(tid) / "s4_label.sections.json").write_text(json.dumps(view, indent=1, ensure_ascii=False))
    m["sources"][f"{tid}.s4_label"]["source_metadata"] = meta
    # S5 SrLC (session cookie + browser UA); guard = the detail page's own header names this application
    L.srlc_session()
    capture(tid, "s5_srlc_search", L.SRLC + "?event=searchResult.page", "html",
            lambda body: (any(r["drug_name_id"] == t["srlc_drug_name_id"] and r["appl_no"].lstrip("0") == app[3:].lstrip("0")
                              for r in L.srlc_search_rows(body.decode("utf-8", "replace"))),
                          f"row DrugNameID={t['srlc_drug_name_id']} with appl_no {app[3:]} present"),
            m, data={"drug_name": brand, "TextSearch": ""}, browser=True)

    def g5(body):
        h = L.srlc_header(body.decode("utf-8", "replace"))
        ok = bool(h) and h["appl_no"].lstrip("0") == app[3:].lstrip("0") and h["brand"].lower() == brand.lower()
        return ok, f"page header={h}"
    capture(tid, "s5_srlc_detail", f"{L.SRLC}?event=searchdetail.page&DrugNameID={t['srlc_drug_name_id']}", "html", g5, m, browser=True)
    # S6 FAERS (aggregate counts only)
    lo, hi = L.FAERS_WINDOW
    b = capture(tid, "s6_faers_substance", L.url(L.OPENFDA + "/event.json", {
        "search": f'patient.drug.medicinalproduct.exact:"{brand.upper()}" AND receivedate:[{lo} TO {hi}]',
        "count": "patient.drug.activesubstance.activesubstancename.exact", "limit": "5"}), "json",
        jguard(lambda d: (bool(d.get("results")), f"top coded substance={d['results'][0]['term']}")), m)
    sub = json.loads(b)["results"][0]["term"]
    q = L.faers_substance_query(sub)
    # limit=0 returns meta.results.total with an empty results list: the exact total, no report records.
    # (Count queries with limit>100 need an API key; that 403 was the v1 failure.)
    capture(tid, "s6_faers_total", L.url(L.OPENFDA + "/event.json", {"search": q, "limit": "0"}), "json",
            jguard(lambda d: (d["results"] == [] and "total" in d["meta"]["results"], f"total={d['meta']['results']['total']}, no records returned")), m)
    # Pilot finding (T01): the substance code also covers other products (varenicline nasal spray), so the
    # label comparison uses reports that name this brand; the substance total is kept as a scope contrast.
    qb = L.faers_brand_query(brand)
    capture(tid, "s6_faers_brand_total", L.url(L.OPENFDA + "/event.json", {"search": qb, "limit": "0"}), "json",
            jguard(lambda d: (d["results"] == [] and "total" in d["meta"]["results"], f"brand total={d['meta']['results']['total']}, no records returned")), m)
    capture(tid, "s6_faers_brand_reactions", L.url(L.OPENFDA + "/event.json", {"search": qb, "count": "patient.reaction.reactionmeddrapt.exact", "limit": "10"}), "json",
            jguard(lambda d: (len(d["results"]) == 10, "10 reaction terms")), m)
    # S7 Enforcement: application level first, else ingredient level
    b = capture(tid, "s7_recall_app", L.url(L.OPENFDA + "/enforcement.json", {"search": f'openfda.application_number:"{app}"', "limit": "100", "sort": "report_date:desc"}), "json",
                lambda body: (True, "application-level query (an empty result is allowed)"), m)
    if not json.loads(b).get("results"):
        ins = [p["name"] for p in json.loads((tdir(tid) / "s1_rx_ingredients.json").read_text())["relatedGroup"]["conceptGroup"][0]["conceptProperties"]]
        capture(tid, "s7_recall_ingredient", L.url(L.OPENFDA + "/enforcement.json", {"search": " AND ".join(f'openfda.generic_name:"{n}"' for n in ins), "limit": "100", "sort": "report_date:desc"}), "json",
                jguard(lambda d: (bool(d.get("results")), f"{len(d['results'])} ingredient-level records")), m)
    # S8 ClinicalTrials.gov: interventional, completed, with results; largest enrollment first
    ins = [p["name"] for p in json.loads((tdir(tid) / "s1_rx_ingredients.json").read_text())["relatedGroup"]["conceptGroup"][0]["conceptProperties"]]
    b = capture(tid, "s8_trials_search", L.url(L.CTGOV + "/studies", {"query.intr": " AND ".join(ins), "filter.overallStatus": "COMPLETED",
                                                                     "aggFilters": "results:with,studyType:int", "sort": "EnrollmentCount:desc", "pageSize": "25",
                                                                     # only the fields the selection rule reads (full record is captured separately)
                                                                     "fields": "NCTId,OverallStatus,EnrollmentCount,EventGroup"}), "json",
                jguard(lambda d: (bool(d.get("studies")), f"{len(d['studies'])} studies returned")), m)
    nct = pick_study(json.loads(b), t, ins)[0]
    capture(tid, "s8_trial", f"{L.CTGOV}/studies/{nct}", "json",
            jguard(lambda d: (d["protocolSection"]["identificationModule"]["nctId"] == nct, f"nctId={nct}")), m)
    capture(tid, "s8_trials_version", f"{L.CTGOV}/version", "json", jguard(lambda d: ("dataTimestamp" in d, f"dataTimestamp={d.get('dataTimestamp')}")), m)
    save_manifest(m)
    print("  S4 sections in scope (pick the S4 passage from these):")
    for s in secs:
        if s["code"] in IN_SCOPE or any(a in IN_SCOPE for a in s["ancestor_codes"]):
            print(f"    [{s['ordinal']}] {s['code']} {s['title'][:90]} ({len(s['direct_text'])} chars)")


def drug_terms(t, ins):
    return [t["brand"].lower()] + [n.lower() for n in ins]


def pick_study(search, t, ins):
    """First study (search order) with an adverse-event group whose title names the drug and has serious-AE at-risk > 0."""
    terms = drug_terms(t, ins)
    for s in search["studies"]:
        groups = s.get("resultsSection", {}).get("adverseEventsModule", {}).get("eventGroups", [])
        for i, g in enumerate(groups):
            title = (g.get("title") or "").lower()
            if any(x in title for x in terms) and (g.get("seriousNumAtRisk") or 0) > 0:
                return s["protocolSection"]["identificationModule"]["nctId"], i
    raise SystemExit("S8: no study in the captured search names the drug in an AE group — trace not built")


# ----------------------------------------------------------------------------- questions
def stage_questions(tid):
    t = TRACES[tid]
    if not t.get("s4"):
        raise SystemExit(f"{tid}: set traces.json s4 {{ordinal, target}} first")
    ndc = load(tid, "s2_ndc")["results"][0]
    pkg = sorted(p["package_ndc"] for p in ndc["packaging"])[0]
    view = json.loads((tdir(tid) / "s4_label.sections.json").read_text())
    sec = view["sections"][t["s4"]["ordinal"]]
    v = view["spl"]
    rec = "s7_recall_app" if load(tid, "s7_recall_app").get("results") else "s7_recall_ingredient"
    lo, hi = L.FAERS_WINDOW
    qs = [
        {"step": "S1", "source": "RxNorm", "question": f"For the exact brand name '{t['brand']}', which brand RxCUI and term type does RxNorm return, which ingredient (IN) concepts are related to it, and is it a multi-ingredient product?",
         "answer_format": "{brand_rxcui, brand_tty, ingredients:[{rxcui,name}] sorted by name, multi_ingredient}"},
        {"step": "S2", "source": "NDC Directory", "question": f"For NDC product {t['product_ndc']}, what are the labeler, marketing category, application number and the description of package {pkg}? Does the listing's spl_set_id equal the S4 label set ID {t['spl_set_id']}?",
         "answer_format": "{labeler_name, marketing_category, application_number, package_ndc, package_description, spl_set_id_matches_s4}", "inputs": {"package_ndc": pkg}},
        {"step": "S3", "source": "Drugs@FDA", "question": "For the application number recorded in S2, what sponsor name does Drugs@FDA give, and which product numbers, dosage forms and strengths are listed?",
         "answer_format": "{application_number, sponsor_name, products:[{product_number, dosage_form, route, active_ingredients}] sorted by product_number}"},
        {"step": "S4", "source": "DailyMed", "question": f"In SPL set {v['setId']['root']} version {v['versionNumber']['value']}, section '{sec['title']}' (direct text only), classify '{t['s4']['target']}'.",
         "answer_format": "One of " + ", ".join(CLASSES), "inputs": {"section_ordinal": sec["ordinal"], "section_id": sec["section_id"], "target": t["s4"]["target"]}},
        {"step": "S5", "source": "SrLC", "question": "On the SrLC page for this application, which is the most recent entry with underlined (added/revised) text in Boxed Warning or sections 4, 5 or 6? Give its date, supplement and first such subsection, and the longest underlined passage in that subsection. Is that passage present in the S4 label version (letters and digits only, case-insensitive)?",
         "answer_format": "{entry_date, supplement, section, subsection, underlined_passage, present_in_s4_label}"},
        {"step": "S6", "source": "FAERS (openFDA)", "question": f"For FAERS reports received {lo}–{hi}: how many name the product '{t['brand'].upper()}' exactly, and how many list its most frequent FAERS-coded active substance (any product)? For the brand-named reports, what are the 10 most frequent reaction terms with counts, and is each term found in the S4 label's in-scope sections (Boxed Warning, Contraindications, Warnings and Precautions, Warnings, Precautions, Adverse Reactions)?",
         "answer_format": "{brand_query, brand_report_count, substance_query, active_substance, substance_report_count, top_terms_brand:[{term,count,found_in_label_scope}]}",
         "template_version": "v2 (pilot T01 showed substance-level reports mix products)"},
        {"step": "S7", "source": "FDA enforcement", "question": f"Among openFDA enforcement records for this {'application' if rec == 's7_recall_app' else 'ingredient (no application-level record exists)'}, take the most recent by report_date. What are its recall number, classification, reason, reported status and report date? Does that record's own product_description or code_info name package {pkg}?",
         "answer_format": "{query_level, records_found, recall_number, classification, reason_for_recall, status_as_reported, report_date, package_named_in_record, package_in_openfda_harmonized_list}", "inputs": {"package_ndc": pkg, "record_file": rec}},
        {"step": "S8", "source": "ClinicalTrials.gov", "question": "From the captured search (interventional, completed, with results, largest enrollment first, 25 studies), take the first study with an adverse-event group whose title names the drug. Report the NCT ID, overall status, group ID and title, serious adverse events affected and at risk.",
         "answer_format": "{nct_id, overall_status, group_id, group_title, seriousNumAffected, seriousNumAtRisk}"},
    ]
    out = {"trace_id": tid, "brand": t["brand"], "class": t["class"], "questions": qs,
           "frozen_before_answers": True, "created_at_utc": L.now_utc()}
    p = L.SHARED / "questions"
    p.mkdir(exist_ok=True)
    b = json.dumps(out, indent=1, ensure_ascii=False).encode()
    (p / f"{tid}.json").write_bytes(b)
    print(f"[{tid}] questions frozen sha256={L.sha256(b)}")


# ----------------------------------------------------------------------------- answers
def load(tid, key, ext="json"):
    b = (tdir(tid) / f"{key}.{ext}").read_bytes()
    return json.loads(b) if ext == "json" else b.decode("utf-8", "replace")


def alnum(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def window(text, start, end, pad=70):
    """Verbatim text around a match (label tables have no sentence breaks, so a fixed window is used)."""
    return text[max(0, start - pad):min(len(text), end + pad)]


def label_term_match(term, secs):
    """Dataset string rule: exact MedDRA term, or US spelling (oe/ae -> e), as a whole phrase, case-insensitive."""
    variants = {term.lower(), term.lower().replace("oe", "e").replace("ae", "e")}
    for s in secs:
        if s["code"] in IN_SCOPE:  # top-level in-scope section; full_text includes its subsections
            for v in sorted(variants):
                hit = re.search(r"(?<![a-z])" + re.escape(v) + r"(?![a-z])", s["full_text"].lower())
                if hit:
                    return {"found": True, "section": s["title"], "section_code": s["code"], "matched": v,
                            "quote": window(s["full_text"], hit.start(), hit.end()),
                            # One-word terms (e.g. PAIN) can match inside a different concept ("abdominal pain"): reviewer must check.
                            "single_word_term": " " not in term.strip()}
    return {"found": False, "searched_sections": sorted({s["title"] for s in secs if s["code"] in IN_SCOPE})}


def stage_answers(tid):
    t = TRACES[tid]
    qdoc = json.loads((L.SHARED / "questions" / f"{tid}.json").read_text())
    q = {x["step"]: x for x in qdoc["questions"]}
    m = manifest()["sources"]
    ann = json.loads((L.ROOT / "claude" / "s4-annotations.json").read_text())[tid]
    rows = []

    def add(step, answer, sources, locators, evidence, rationale, uncertainty, check_type, links=None, review="pending"):
        rows.append({"case_id": f"{tid}-{step}", "trace_id": tid, "step": step, "category": q[step]["source"],
                     "question": q[step]["question"], "answer": answer, "answer_status": "resolved",
                     "source_ids": [f"{tid}.{s}" for s in sources], "evidence_locators": locators,
                     "supporting_quote_or_value": evidence,
                     "source_sha256": {f"{tid}.{s}": m[f"{tid}.{s}"]["sha256"] for s in sources},
                     "source_effective_or_updated_at": {f"{tid}.{s}": m[f"{tid}.{s}"].get("source_metadata") for s in sources if m[f"{tid}.{s}"].get("source_metadata")},
                     "retrieved_at_utc": {f"{tid}.{s}": m[f"{tid}.{s}"]["retrieved_at_utc"] for s in sources},
                     "link_checks": links or {}, "rationale": rationale, "uncertainty": uncertainty,
                     "check_type": check_type, "human_review_status": review, "annotator": "claude"})

    # S1
    props = load(tid, "s1_rx_brand_props")["properties"]
    ings = sorted(({"rxcui": p["rxcui"], "name": p["name"]} for p in load(tid, "s1_rx_ingredients")["relatedGroup"]["conceptGroup"][0]["conceptProperties"]), key=lambda x: x["name"])
    rev = [f"s1_rx_reverse_{i['rxcui']}" for i in ings]
    add("S1", {"brand_rxcui": props["rxcui"], "brand_tty": props["tty"], "ingredients": ings, "multi_ingredient": len(ings) > 1},
        ["s1_rx_brand", "s1_rx_brand_props", "s1_rx_ingredients"] + rev,
        {"s1_rx_brand": "/idGroup/rxnormId/0", "s1_rx_brand_props": "/properties/rxcui; /properties/tty",
         "s1_rx_ingredients": "/relatedGroup/conceptGroup/0/conceptProperties/*"} | {r: f"/relatedGroup/conceptGroup/*/conceptProperties[rxcui={props['rxcui']}]" for r in rev},
        {"brand": props["name"], "tty": props["tty"], "IN": ings},
        "Exact-name lookup returns the brand concept; its tty=IN relations are the active ingredients.",
        "RxNorm identifies the medicine only; it says nothing about safety or label applicability. Strength, dose form and package are not part of this step.",
        "source_lookup")
    # S2
    nd = load(tid, "s2_ndc")["results"][0]
    pkg = q["S2"]["inputs"]["package_ndc"]
    pk = next(p for p in nd["packaging"] if p["package_ndc"] == pkg)
    setmatch = (nd.get("openfda", {}).get("spl_set_id") or [None])[0] == t["spl_set_id"]
    add("S2", {"labeler_name": nd["labeler_name"], "marketing_category": nd["marketing_category"], "application_number": nd["application_number"],
               "package_ndc": pkg, "package_description": pk["description"], "spl_set_id_matches_s4": setmatch},
        ["s2_ndc"], {"s2_ndc": f"/results/0/labeler_name; /results/0/marketing_category; /results/0/application_number; /results/0/packaging[package_ndc={pkg}]/description; /results/0/openfda/spl_set_id/0"},
        {"package": pk, "spl_set_id": nd.get("openfda", {}).get("spl_set_id")},
        "Values read from the NDC listing; the spl_set_id link ties this package to the S4 label.",
        "An NDC listing is not FDA approval. The listing can change daily.",
        "source_lookup", links={"S2.spl_set_id == S4.setId": setmatch})
    # S3
    df = load(tid, "s3_drugsfda")["results"][0]
    prods = sorted(({"product_number": p["product_number"], "dosage_form": p.get("dosage_form"), "route": p.get("route"),
                     "active_ingredients": p.get("active_ingredients")} for p in df.get("products", [])), key=lambda x: x["product_number"])
    add("S3", {"application_number": df["application_number"], "sponsor_name": df["sponsor_name"], "products": prods},
        ["s3_drugsfda"], {"s3_drugsfda": "/results/0/application_number; /results/0/sponsor_name; /results/0/products/*"},
        {"sponsor_name": df["sponsor_name"], "n_products": len(prods)},
        "Application facts read from Drugs@FDA for the application number the NDC listing names.",
        f"Drugs@FDA wording can differ from NDC (sponsor '{df['sponsor_name']}' vs labeler '{nd['labeler_name']}'; dosage-form strings differ by source). Join on application number, not on strings.",
        "source_lookup", links={"S3.application_number == S2.application_number": df["application_number"] == nd["application_number"]})
    # S4 (Claude's judgement, quote-anchored)
    view = json.loads((tdir(tid) / "s4_label.sections.json").read_text())
    sec = view["sections"][q["S4"]["inputs"]["section_ordinal"]]
    assert ann["class"] in CLASSES and ann["quote"] in sec["direct_text"], f"{tid} S4 quote not verbatim in passage"
    v = view["spl"]
    add("S4", ann["class"], ["s4_label"],
        {"s4_label": {"xml_path": f"//section[id/@root='{sec['section_id']}']/text", "heading": sec["title"], "section_code": sec["code"],
                      "derived_ordinal": sec["ordinal"], "derived_view": f"evidence/{tid}/s4_label.sections.json"}},
        ann["quote"], ann["rationale"], ann["uncertainty"] + f" Scoped to SPL {v['setId']['root']} v{v['versionNumber']['value']} (effectiveTime {v['effectiveTime']['value']}) and this passage only.",
        "label_interpretation")
    # S5
    html_ = load(tid, "s5_srlc_detail", "html")
    head = L.srlc_header(html_)
    chosen = None
    for e in L.srlc_entries(html_):
        for s in e["sections"]:
            if s["section"][:1] in ("4", "5", "6") or s["section"].startswith("Boxed"):
                for ss in s["subsections"]:
                    if ss["underlined"]:
                        chosen = (e, s, ss)
                        break
            if chosen: break
        if chosen: break
    e, s, ss = chosen
    passage = max(ss["underlined"], key=len)
    full_label = alnum(" ".join(x["full_text"] for x in view["sections"]))
    present = alnum(passage) in full_label
    add("S5", {"entry_date": e["date"], "supplement": e["supplement"], "section": s["section"], "subsection": ss["subsection"],
               "underlined_passage": passage, "present_in_s4_label": present},
        ["s5_srlc_search", "s5_srlc_detail"],
        {"s5_srlc_detail": f"{head['brand']} ({head['appl_type']}-{head['appl_no']}) > {e['date']} ({e['supplement']}) > {s['section']} > {ss['subsection']} > <u> text",
         "s5_srlc_search": f"result row DrugNameID={t['srlc_drug_name_id']}"},
        passage, "The most recent SrLC entry with underlined text in Boxed/4/5/6 was read from the detail page, whose header names this application.",
        "SrLC covers safety-related changes since 2016 for NDA/BLA labels only. An entry date is the supplement approval date, not the date every product label changed. Presence uses a letters-and-digits comparison against the whole S4 label.",
        "source_lookup", links={"S5.page_header.appl_no == S2.application_number": head["appl_no"].lstrip("0") == nd["application_number"][3:].lstrip("0"),
                                "S5.underlined_passage present in S4 label": present})
    # S6
    sub = load(tid, "s6_faers_substance")["results"][0]["term"]
    total = load(tid, "s6_faers_total")["meta"]["results"]["total"]
    btotal = load(tid, "s6_faers_brand_total")["meta"]["results"]["total"]
    rx = load(tid, "s6_faers_brand_reactions")
    terms = [{"term": r["term"], "count": r["count"], "label_match": label_term_match(r["term"], view["sections"])} for r in rx["results"]]
    add("S6", {"brand_query": L.faers_brand_query(t["brand"]), "brand_report_count": btotal,
               "substance_query": L.faers_substance_query(sub), "active_substance": sub, "substance_report_count": total,
               "top_terms_brand": [{"term": x["term"], "count": x["count"], "found_in_label_scope": x["label_match"]["found"]} for x in terms]},
        ["s6_faers_substance", "s6_faers_total", "s6_faers_brand_total", "s6_faers_brand_reactions"],
        {"s6_faers_substance": "/results/0/term", "s6_faers_total": "/meta/results/total", "s6_faers_brand_total": "/meta/results/total",
         "s6_faers_brand_reactions": "/results/0..9"},
        {"meta.last_updated": rx["meta"]["last_updated"], "label_matches": {x["term"]: x["label_match"] for x in terms}},
        "Brand-named reports are compared with this brand's label; the substance-level total shows how much wider an ingredient query is. All values come from aggregate count or total-only queries.",
        "Counts are reports matching each saved query (any drug role), not patients, incidence or causation, and not deduplicated here. A brand-name query misses reports that name only the generic; a substance query can include other products with the same substance. "
        "Label matching is a string rule (exact term or US spelling); 'not found' means that string is absent from the in-scope sections of this label version, not that the label never covers the concept. Synonyms and non-clinical terms need pharmacist review.",
        "source_lookup", links={"S6.top_terms checked against S4 in-scope sections": True,
                                "S6 brand-named reports are a subset-scope of substance reports (counts differ)": btotal != total})
    # S7
    rk = q["S7"]["inputs"]["record_file"]
    rd = load(tid, rk)
    r0 = rd["results"][0]
    own = (r0.get("product_description") or "") + " " + (r0.get("code_info") or "")
    named = pkg in own or pkg.replace("-", "") in own.replace("-", "")
    harmonized = pkg in (r0.get("openfda", {}).get("package_ndc") or [])
    add("S7", {"query_level": "application" if rk == "s7_recall_app" else "ingredient", "records_found": rd["meta"]["results"]["total"],
               "recall_number": r0["recall_number"], "classification": r0["classification"], "reason_for_recall": r0["reason_for_recall"],
               "status_as_reported": r0["status"], "report_date": r0["report_date"],
               "package_named_in_record": named, "package_in_openfda_harmonized_list": harmonized},
        [rk] + (["s7_recall_app"] if rk != "s7_recall_app" else []),
        {rk: "/results/0 (sorted report_date desc): recall_number, classification, reason_for_recall, status, report_date, product_description, code_info, openfda/package_ndc"},
        {"product_description": r0.get("product_description"), "code_info": r0.get("code_info")},
        "Most recent record for the query level; package match uses the record's own text, not openFDA harmonization.",
        "Reported status is not current recall lifecycle status (FDA does not update it after classification). openfda.package_ndc is attached at application/product level, so a listed package there does not prove the recall covers it. Hospital exposure needs inventory and lot data.",
        "cross_source_comparison", links={"S7 package named in record text": named, "S7 package in openfda harmonized list (not proof)": harmonized})
    # S8
    st = load(tid, "s8_trial")
    nct = st["protocolSection"]["identificationModule"]["nctId"]
    ins = [i["name"] for i in ings]
    _, gi = pick_study(load(tid, "s8_trials_search"), t, ins)
    g = st["resultsSection"]["adverseEventsModule"]["eventGroups"][gi]
    add("S8", {"nct_id": nct, "overall_status": st["protocolSection"]["statusModule"]["overallStatus"], "group_id": g["id"], "group_title": g["title"],
               "seriousNumAffected": g.get("seriousNumAffected"), "seriousNumAtRisk": g.get("seriousNumAtRisk")},
        ["s8_trials_search", "s8_trial", "s8_trials_version"],
        {"s8_trial": f"/resultsSection/adverseEventsModule/eventGroups/{gi}", "s8_trials_search": "/studies (selection order)"},
        {k: g.get(k) for k in ("id", "title", "seriousNumAffected", "seriousNumAtRisk")} | {"timeFrame": st["resultsSection"]["adverseEventsModule"].get("timeFrame")},
        "First study in the captured search order whose AE group title names the drug; counts read from that group.",
        "Specific to this study, arm, denominator and follow-up. Not a population risk estimate.",
        "source_lookup", links={"S8 group title names S1 brand or ingredient": any(x in g["title"].lower() for x in drug_terms(t, ins))})
    out = L.ROOT / "claude" / "traces"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{tid}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"[{tid}] {len(rows)} answers written")


if __name__ == "__main__":
    stage, tid = sys.argv[1], sys.argv[2]
    {"capture": stage_capture, "questions": stage_questions, "answers": stage_answers}[stage](tid)
