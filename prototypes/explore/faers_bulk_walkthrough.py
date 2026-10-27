"""FAERS bulk walkthrough: run the real pipeline stages on 2 quarters, print what each stage looks like.

Paper prototype of Part A for FAERS (no Foundry). Every number in
docs/04-architecture/data-walkthrough-v1.html comes from this script.

Input : prototypes/data/_faers_bulk/2026q1, 2026q2  (unzipped FDA quarterly ASCII files)
Output: prototypes/data/_walkthrough/facts.json  + small CSV samples per stage
Run   : python3 -I prototypes/explore/faers_bulk_walkthrough.py
"""
import csv, collections as C, json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BULK = os.path.join(ROOT, "data", "_faers_bulk")
OUT = os.path.join(ROOT, "data", "_walkthrough")
QUARTERS = ["2026q1", "2026q2"]

OURS = ["buprenorphine", "fentanyl", "hydrocodone", "hydromorphone", "methadone", "morphine",
        "oxycodone", "tramadol", "semaglutide", "liraglutide", "dulaglutide", "exenatide", "tirzepatide"]
# Salt / form words to strip so "OXYCODONE HYDROCHLORIDE" -> "oxycodone". In Foundry this is RxNorm's job.
SALTS = r"\b(hydrochloride|hcl|bitartrate|citrate|sulfate|sulphate|terephthalate|tartrate|acetate|" \
        r"phosphate|myristate|propanediol|sodium|anhydrous)\b"
# Brand -> ingredient, only used when prod_ai is blank (fallback). In Foundry: RxNorm approximateTerm.
BRANDS = {"ozempic": "semaglutide", "wegovy": "semaglutide", "rybelsus": "semaglutide",
          "victoza": "liraglutide", "saxenda": "liraglutide", "trulicity": "dulaglutide",
          "mounjaro": "tirzepatide", "zepbound": "tirzepatide", "byetta": "exenatide", "bydureon": "exenatide",
          "oxycontin": "oxycodone", "percocet": "oxycodone", "roxicodone": "oxycodone", "norco": "hydrocodone",
          "vicodin": "hydrocodone", "dilaudid": "hydromorphone", "duragesic": "fentanyl", "suboxone": "buprenorphine",
          "ultram": "tramadol", "ms contin": "morphine", "dolophine": "methadone"}

# Reaction buckets (D016): tag, don't rank. Simple word rules for the prototype.
BUCKETS = [
    ("product_use_error", r"off label|unapproved indication|wrong technique|dose omission|incorrect dose|"
                          r"inappropriate schedule|expired product|device |product use|medication error|"
                          r"product dose|underdose|extra dose|wrong drug|product storage|drug dose omission"),
    ("efficacy", r"drug ineffective|weight loss poor|therapeutic product effect|drug effect less"),
    ("abuse_overdose", r"overdose|drug abuse|dependence|withdrawal|misuse|intentional|toxicity to various|diversion"),
    ("pregnancy_neonatal", r"pregnancy|foetal|fetal|neonatal|maternal"),
    ("litigation_style", r"emotional distress|injury$|loss of employment|anxiety$"),
]


def read(q, table):
    """Yield dict rows from one FAERS ASCII table. '$'-separated, CRLF, latin-1."""
    path = os.path.join(BULK, q, "ASCII", f"{table}{q[2:4]}{q[4:].upper()}.txt")
    with open(path, encoding="latin-1", newline="") as f:
        r = csv.reader((line.replace("\r", "") for line in f), delimiter="$", quoting=csv.QUOTE_NONE)
        head = next(r)
        for row in r:
            yield dict(zip(head, row))


def deletes(q):
    path = os.path.join(BULK, q, "Deleted", f"DELETE{q[2:4]}{q[4:].upper()}.txt")
    return {l.strip() for l in open(path) if l.strip()}  # file starts with a blank line


def ingredients(prod_ai, drugname):
    """Return (set of our ingredients, how matched). Exact token match after salt strip, never substring."""
    if prod_ai.strip():
        parts = [re.sub(SALTS, "", p.lower()).strip() for p in prod_ai.split("\\")]
        return {p for p in parts if p in OURS}, "prod_ai"
    name = drugname.lower()
    hits = {ing for b, ing in BRANDS.items() if re.search(rf"\b{b}\b", name)}
    hits |= {i for i in OURS if re.search(rf"\b{i}\b", name)}
    return hits, "drugname_fallback"


def bucket(pt):
    low = pt.lower()
    for name, rx in BUCKETS:
        if re.search(rx, low):
            return name
    return "clinical"


def load_quarter(q, facts):
    """Stage 1 + 2: raw tables -> per-report records, ALL reports kept (PRR needs the background)."""
    f = facts.setdefault("raw", {}).setdefault(q, {})
    demo = {}
    for d in read(q, "DEMO"):
        demo[d["primaryid"]] = d
    f["demo_rows"] = len(demo)
    drugs = C.defaultdict(list); n = 0
    naive = C.Counter(); exact = C.Counter(); how = C.Counter(); false_hits = C.Counter()
    for d in read(q, "DRUG"):
        n += 1
        ings, via = ingredients(d["prod_ai"], d["drugname"])
        sub = {i for i in OURS if i in (d["prod_ai"] + " " + d["drugname"]).lower()}  # the naive way
        for i in sub: naive[i] += 1
        for i in ings: exact[i] += 1
        if ings: how[via] += 1
        for i in sub - ings: false_hits[(i, d["drugname"], d["prod_ai"])] += 1
        d["_ings"] = ings
        drugs[d["primaryid"]].append(d)
    f["drug_rows"] = n
    f["naive_vs_exact_rows"] = {i: [naive[i], exact[i]] for i in OURS}
    f["match_via"] = dict(how)
    f["top_false_hits"] = [[a, b, c, k] for (a, b, c), k in false_hits.most_common(10)]
    reac = C.defaultdict(list); n = 0
    for d in read(q, "REAC"):
        n += 1; reac[d["primaryid"]].append(d["pt"])
    f["reac_rows"] = n
    occ = C.Counter(d["occp_cod"] for d in demo.values())
    f["reporter_type"] = dict(occ.most_common())
    return demo, drugs, reac


def to_case_records(q, demo, drugs, reac):
    """One record per report (primaryid) -> keyed by caseid, with version, for dedup."""
    recs = {}
    for pid, dm in demo.items():
        ds = drugs.get(pid, [])
        suspect = set(); concomitant = set()
        for d in ds:
            (suspect if d["role_cod"] in ("PS", "SS", "I") else concomitant).update(d["_ings"])
        recs[dm["caseid"]] = {
            "caseid": dm["caseid"], "primaryid": pid, "caseversion": int(dm["caseversion"] or 0),
            "quarter": q, "fda_dt": dm["fda_dt"], "occp_cod": dm["occp_cod"], "serious": None,
            "suspect": sorted(suspect), "concomitant": sorted(concomitant - suspect),
            "pts": sorted(set(reac.get(pid, []))), "n_drug_rows": len(ds),
            # cross-case duplicate key: same person reported by many companies under different caseids
            "person_key": (dm["age"], dm["age_cod"], dm["sex"], dm["occr_country"], dm["event_dt"]),
            "all_suspect_names": sorted({d["prod_ai"] or d["drugname"] for d in ds if d["role_cod"] in ("PS", "SS")}),
        }
    return recs


def merge_incremental(state, new, dels):
    """Stage 3: upsert by caseid, keep highest caseversion, then drop deleted cases. Returns change log."""
    log = {"new": 0, "replaced": 0, "older_version_ignored": 0, "deleted": 0, "examples_replaced": []}
    for cid, rec in new.items():
        old = state.get(cid)
        if old is None:
            state[cid] = rec; log["new"] += 1
        elif rec["caseversion"] >= old["caseversion"]:
            if (old["suspect"] or rec["suspect"]) and (old["suspect"] != rec["suspect"] or old["pts"] != rec["pts"]):
                log["examples_replaced"].append((old, rec))
            state[cid] = rec; log["replaced"] += 1
        else:
            log["older_version_ignored"] += 1
    for cid in dels:
        if state.pop(cid, None) is not None:
            log["deleted"] += 1
    return log


def explode(state):
    """Stage 4: case -> rows of (ingredient, PT) for OUR suspect drugs only. Also background counts for PRR."""
    rows = []
    for rec in state.values():
        for ing in rec["suspect"]:
            for pt in rec["pts"]:
                rows.append((rec["caseid"], ing, pt, bucket(pt), rec["quarter"]))
    return rows


def flag_mass_duplicates(state, min_drugs=30, min_reports=50):
    """Stage 3b: cross-case dedup. Reports with many drugs that share one person_key >= min_reports times
    are one patient filed again and again. Keep one (the latest) per cluster, mark the rest."""
    keys = C.Counter(r["person_key"] for r in state.values() if r["n_drug_rows"] >= min_drugs and r["person_key"][0])
    clusters = {k for k, v in keys.items() if v >= min_reports}
    keep = {}
    for r in state.values():
        r["dup_cluster"] = r["person_key"] in clusters and r["n_drug_rows"] >= min_drugs
        if r["dup_cluster"]:
            best = keep.get(r["person_key"])
            if best is None or r["fda_dt"] > best["fda_dt"]:
                keep[r["person_key"]] = r
    kept_ids = {r["caseid"] for r in keep.values()}
    for r in state.values():
        r["dup_suppressed"] = r["dup_cluster"] and r["caseid"] not in kept_ids
    return {"clusters": [[list(k), keys[k]] for k in clusters],
            "suppressed": sum(r["dup_suppressed"] for r in state.values())}


def prr_table(state, ing, skip_dups=False):
    """Stage 5: PRR for one ingredient vs ALL other reports in the window. a,b,c,d = 2x2 table."""
    with_drug = C.Counter(); without = C.Counter(); n_drug = n_other = 0
    for rec in state.values():
        if skip_dups and rec.get("dup_suppressed"):
            continue
        if ing in rec["suspect"]:
            n_drug += 1
            for pt in rec["pts"]: with_drug[pt] += 1
        else:
            n_other += 1
            for pt in rec["pts"]: without[pt] += 1
    out = []
    for pt, a in with_drug.items():
        b = n_drug - a; c = without[pt]; d = n_other - c
        prr = (a / n_drug) / (c / n_other) if c else float("inf")
        # chi-square with Yates correction (Evans criteria use chi2 >= 4)
        n = a + b + c + d
        chi = (n * (abs(a * d - b * c) - n / 2) ** 2) / ((a + b) * (c + d) * (a + c) * (b + d)) if c else float("inf")
        out.append({"pt": pt, "a": a, "b": b, "c": c, "d": d, "prr": round(prr, 1) if c else None,
                    "chi2": round(chi, 1) if c else None, "bucket": bucket(pt),
                    "evans": a >= 3 and (c == 0 or (prr >= 2 and chi >= 4))})
    return n_drug, sorted(out, key=lambda r: -r["a"])


def main():
    os.makedirs(OUT, exist_ok=True)
    facts = {}
    state = {}
    q1_snapshot = None
    appended_rows = 0  # what a naive "append every quarter" pipeline would count
    for q in QUARTERS:
        demo, drugs, reac = load_quarter(q, facts)
        recs = to_case_records(q, demo, drugs, reac)
        f = facts["raw"][q]
        f["reports"] = len(recs)
        f["reports_ours"] = sum(1 for r in recs.values() if set(r["suspect"]) | set(r["concomitant"]))
        f["reports_ours_suspect"] = sum(1 for r in recs.values() if r["suspect"])
        f["caseversion_gt1"] = sum(1 for r in recs.values() if r["caseversion"] > 1)
        # same ingredient listed more than once as suspect in one report (titration, PS + SS of same drug)
        dup = 0; ss_same = 0; ss_total = 0
        for pid, ds in drugs.items():
            seen = C.Counter(i for d in ds if d["role_cod"] in ("PS", "SS") for i in d["_ings"])
            dup += sum(1 for v in seen.values() if v > 1)
            ps = {i for d in ds if d["role_cod"] == "PS" for i in d["_ings"]}
            for d in ds:
                if d["role_cod"] == "SS" and d["_ings"]:
                    ss_total += 1; ss_same += bool(d["_ings"] & ps)
        f["same_ingredient_repeated_in_report"] = dup
        f["ss_rows_ours"] = ss_total; f["ss_rows_same_as_ps"] = ss_same
        appended_rows += sum(len(r["suspect"]) * len(r["pts"]) for r in recs.values())
        dels = deletes(q)
        log = merge_incremental(state, recs, dels)
        log["delete_file_ids"] = len(dels)
        # keep one illustrative replaced case where our suspect set changed
        ex = log.pop("examples_replaced")
        log["n_replaced_ours_changed"] = len(ex)
        log["n_replaced_ours_suspect_changed"] = sum(1 for o, n in ex if o["suspect"] != n["suspect"])
        log["example"] = next(([o, n] for o, n in ex if o["caseid"] == "26412122"), ex[:1])
        facts.setdefault("incremental", {})[q] = log
        facts.setdefault("state_size", {})[q] = len(state)
        if q == QUARTERS[0]:
            q1_snapshot = {k: dict(v) for k, v in state.items() if v["suspect"]}
        del demo, drugs, reac, recs

    rows = explode(state)
    facts["exploded_rows_ours"] = len(rows)
    facts["append_vs_upsert_rows"] = [appended_rows, len(rows)]
    by_ing = C.Counter(r[1] for r in rows)
    facts["exploded_by_ingredient"] = dict(by_ing.most_common())
    facts["bucket_share"] = {ing: dict(C.Counter(r[3] for r in rows if r[1] == ing)) for ing in OURS}
    with open(os.path.join(OUT, "stage4_exploded_sample.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["caseid", "ingredient", "pt", "bucket", "quarter"])
        w.writerows([r for r in rows if r[1] == "semaglutide"][:200])

    # Effect of the Q2 update on counts: Q1-only state vs merged state, for one drug-reaction
    def count(st, ing, pt): return sum(1 for r in st.values() if ing in r["suspect"] and pt in r["pts"])
    facts["update_effect"] = {f"{i}|{p}": [count(q1_snapshot, i, p), count(state, i, p)]
                              for i, p in [("liraglutide", "Impaired gastric emptying"),
                                           ("semaglutide", "Impaired gastric emptying"),
                                           ("semaglutide", "Optic ischaemic neuropathy")]}

    before = {ing: prr_table(state, ing) for ing in ["semaglutide", "oxycodone"]}
    facts["mass_duplicates"] = flag_mass_duplicates(state)
    facts["cases_ours_suspect"] = sum(1 for r in state.values() if r["suspect"])
    facts["cases_ours_suspect_after_fold"] = sum(1 for r in state.values() if r["suspect"] and not r["dup_suppressed"])
    facts["dup_effect"] = {}
    for ing in OURS:
        n0 = sum(1 for r in state.values() if ing in r["suspect"])
        n1 = sum(1 for r in state.values() if ing in r["suspect"] and not r["dup_suppressed"])
        facts["dup_effect"][ing] = [n0, n1]
    facts["prr_before_dedup_top"] = {ing: [[r["pt"], r["a"], r["prr"]] for r in t[1][:15]] for ing, t in before.items()}
    for ing in ["semaglutide", "oxycodone"]:
        n_drug, tab = prr_table(state, ing, skip_dups=True)
        facts.setdefault("prr", {})[ing] = {"reports": n_drug, "top": tab[:40],
                                            "naion_family": [r for r in tab if re.search(r"optic|naion", r["pt"].lower())]}
        with open(os.path.join(OUT, f"stage5_prr_{ing}.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(tab[0].keys())); w.writeheader(); w.writerows(tab)

    json.dump(facts, open(os.path.join(OUT, "facts.json"), "w"), indent=1, default=str)
    print(json.dumps({k: facts[k] for k in ["state_size", "exploded_rows_ours", "append_vs_upsert_rows", "update_effect"]}, indent=1))
    print(json.dumps(facts["incremental"], indent=1, default=str)[:3000])


if __name__ == "__main__":
    sys.exit(main())
