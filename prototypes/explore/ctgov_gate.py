"""Gate A: is ClinicalTrials.gov worth a pipeline for the pilot? (timeboxed keep/park test)

Usage: python3 -I prototypes/explore/ctgov_gate.py <cache_dir> [--refresh]
  cache_dir  where raw API pages and the summary JSON go (not the repo; use a scratch folder)

Steps:
  1. Pull every study with posted results for the 13 pilot ingredients (API v2, public, no key).
  2. Sort each study: does it really test OUR drug's safety, or is our drug background
     (bioequivalence/PK, given to every arm, only named in passing)?
  3. Look for the top FAERS signals in the trial adverse-event tables.
Output: <cache_dir>/summary.json (numbers used by docs/07-data-quality/atlas/clinicaltrials.html).
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

OPIOIDS = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol"]
GLP1 = ["semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]  # keep in sync with pull_all.py

# Brand names, so a study that only says "Ozempic" still counts as semaglutide.
BRANDS = {
    "fentanyl": ["duragesic", "actiq", "fentora", "sublimaze", "abstral", "subsys", "ionsys"],
    "morphine": ["ms contin", "kadian", "duramorph", "infumorph", "avinza", "embeda"],
    "hydromorphone": ["dilaudid", "exalgo", "palladone"],
    "oxycodone": ["oxycontin", "roxicodone", "percocet", "xtampza", "targiniq", "troxyca", "oxaydo", "roxybond"],
    "hydrocodone": ["norco", "vicodin", "zohydro", "hysingla", "lortab", "vicoprofen"],
    "methadone": ["dolophine", "methadose"],
    "buprenorphine": ["suboxone", "subutex", "zubsolv", "butrans", "belbuca", "sublocade", "brixadi", "probuphine", "buprenex", "bunavail"],
    "tramadol": ["ultram", "ultracet", "conzip", "ryzolt"],
    "semaglutide": ["ozempic", "wegovy", "rybelsus"],
    "tirzepatide": ["mounjaro", "zepbound"],
    "liraglutide": ["victoza", "saxenda", "xultophy"],
    "dulaglutide": ["trulicity"],
    "exenatide": ["byetta", "bydureon"],
}

# Top FAERS signals to look for (from prototypes/data/_walkthrough/stage5_prr_*.csv, after dedup).
# "exact" = the MedDRA preferred term FAERS uses; "near" = a close clinical neighbour, reported separately.
SIGNALS = {
    "semaglutide": {
        "Optic ischaemic neuropathy (NAION)": {
            "exact": ["optic ischaemic neuropathy", "optic ischemic neuropathy"],
            "near": ["ischaemic optic neuropathy", "ischemic optic neuropathy", "naion",
                     "non-arteritic anterior ischaemic optic neuropathy", "non-arteritic anterior ischemic optic neuropathy",
                     "optic neuropathy", "optic nerve infarction", "optic disc oedema", "optic disc edema"],
        },
        "Impaired gastric emptying": {
            "exact": ["impaired gastric emptying"],
            "near": ["gastroparesis", "delayed gastric emptying", "gastric emptying delayed"],
        },
    },
    # Oxycodone: the 5 most-reported clinical PTs that pass the Evans rule (PRR>=2, chi2>=4, n>=3).
    "oxycodone": {
        "Pain": {"exact": ["pain"], "near": []},
        "Rash": {"exact": ["rash"], "near": []},
        "Hypersensitivity": {"exact": ["hypersensitivity"], "near": ["drug hypersensitivity"]},
        "Joint swelling": {"exact": ["joint swelling"], "near": []},
        "Hypertension": {"exact": ["hypertension"], "near": ["blood pressure increased"]},
    },
}
# Also check the NAION / gastric-emptying terms in the other GLP-1 trials (class view).
CLASS_CHECK = {d: SIGNALS["semaglutide"] for d in GLP1 if d != "semaglutide"}

PK_RX = re.compile(r"bioequivalen|bioavailab|pharmacokinetic|\bpk\b|food effect|\bfed\b|fasted|fasting condition|"
                   r"drug[- ]drug interaction|\bddi\b|relative bioavailab|abuse potential|abuse liability|"
                   r"human abuse|likeability|drug liking", re.I)
PLACEBO_RX = re.compile(r"placebo|sham|vehicle|saline|standard of care|usual care|no treatment|no intervention|control", re.I)

API = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = ",".join([
    "protocolSection.identificationModule",
    "protocolSection.statusModule",
    "protocolSection.designModule",
    "protocolSection.armsInterventionsModule",
    "protocolSection.conditionsModule",
    "resultsSection.adverseEventsModule",
    "hasResults",
])


def drug_rx(drug):
    names = [drug] + BRANDS.get(drug, [])
    return re.compile(r"\b(" + "|".join(re.escape(n) for n in names) + r")\b", re.I)


def strip_placebo(drug, text):
    """Remove "placebo (semaglutide)", "semaglutide placebo", "placebo matched to semaglutide" ...
    so a placebo arm is not mistaken for a drug arm (first run counted STEP 1 as 'drug in all arms')."""
    names = "|".join(re.escape(n) for n in [drug] + BRANDS.get(drug, []))
    text = re.sub(r"placebo\s*(?:\(|for|to|matched to|matching|of)?\s*\(?\s*(?:" + names + r")\b\)?", " ", text, flags=re.I)
    return re.sub(r"\b(?:" + names + r")[- ]?(?:matched |matching )?placebo", " ", text, flags=re.I)


def has_drug(drug, text):
    return bool(drug_rx(drug).search(strip_placebo(drug, text)))


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "signal-monitor-research/0.1"}), timeout=60) as r:
                return json.load(r)
        except Exception as e:  # network blips / 429: back off and retry
            print(f"  retry {attempt + 1}: {e}", flush=True)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"failed: {url}")


def pull(drug, cache, refresh):
    f = cache / f"{drug}.json"
    if f.exists() and not refresh:
        return json.loads(f.read_text())
    studies, token, t0, total = [], None, time.time(), None
    while True:
        q = {"query.intr": drug, "aggFilters": "results:with", "pageSize": 200, "fields": FIELDS, "countTotal": "true"}
        if token:
            q["pageToken"] = token
        page = get(API + "?" + urllib.parse.urlencode(q))
        studies += page.get("studies", [])
        total = total if total is not None else page.get("totalCount")  # only the first page carries it
        token = page.get("nextPageToken")
        if not token:
            break
        time.sleep(1.3)  # stay well under the ~50 requests/minute courtesy limit
    out = {"drug": drug, "pulled": date.today().isoformat(), "seconds": round(time.time() - t0, 1),
           "totalCount": total, "studies": studies}
    f.write_text(json.dumps(out))
    return out


def arm_text(a):
    return " ".join([a.get("label", ""), a.get("description", ""), " ".join(a.get("interventionNames", []))])


def classify(study, drug):
    """Return (category, detail). Categories, checked in this order:
    not_named   - query hit via synonym/other text; our drug is not in any intervention or arm
    pk_be       - bioequivalence / PK / food-effect / DDI / abuse-liability study (not a safety question)
    all_arms    - our drug is given in every arm, so it is background (e.g. rescue analgesia)
    comparator  - our drug is only the active comparator for something else
    experimental- our drug is (part of) an experimental arm
    """
    rx = drug_rx(drug)
    p = study.get("protocolSection", {})
    ai = p.get("armsInterventionsModule", {})
    ident = p.get("identificationModule", {})
    title = " ".join([ident.get("briefTitle", ""), ident.get("officialTitle", "")])
    interventions = ai.get("interventions", [])
    in_iv = any(has_drug(drug, " ".join([i.get("name", ""), " ".join(i.get("otherNames", []))])) for i in interventions)
    arms = ai.get("armGroups", [])
    drug_arms = [a for a in arms if a.get("type") not in ("PLACEBO_COMPARATOR", "SHAM_COMPARATOR") and has_drug(drug, arm_text(a))]
    if not in_iv and not drug_arms:
        return "not_named", {}
    if PK_RX.search(title):
        return "pk_be", {}
    if len(arms) >= 2 and len(drug_arms) == len(arms):
        return "all_arms", {}
    types = {a.get("type", "") for a in drug_arms}
    if drug_arms and types <= {"ACTIVE_COMPARATOR", "PLACEBO_COMPARATOR", "SHAM_COMPARATOR", "NO_INTERVENTION"}:
        return "comparator", {}
    return "experimental", {}


def ae_groups(study, drug):
    """Split AE event groups into ones that got our drug and ones that did not (by group title/description)."""
    rx = drug_rx(drug)
    ae = study.get("resultsSection", {}).get("adverseEventsModule", {})
    groups = ae.get("eventGroups", [])
    with_drug, without = set(), set()
    for g in groups:
        title, desc = g.get("title", ""), g.get("description", "")
        if has_drug(drug, title):
            hit = True
        elif PLACEBO_RX.search(title):
            hit = False  # "Placebo" group whose description names the drug it mimics
        else:
            hit = has_drug(drug, desc)
        (with_drug if hit else without).add(g.get("id"))
    # single-group studies titled "All participants" etc.: the one group got the drug
    if len(groups) == 1 and not with_drug and classify(study, drug)[0] == "experimental":
        with_drug, without = set(without), set()
    return ae, groups, with_drug, without


def find_terms(ae, terms):
    rows = []
    for kind in ("seriousEvents", "otherEvents"):
        for ev in ae.get(kind, []):
            t = ev.get("term", "").strip().lower()
            if t in terms:
                rows.append((kind, ev))
    return rows


def signal_hits(study, drug, sig_name, spec, category):
    ae, groups, with_drug, without = ae_groups(study, drug)
    out = []
    for level in ("exact", "near"):
        for kind, ev in find_terms(ae, set(spec[level])):
            st = {s.get("groupId"): s for s in ev.get("stats", [])}
            def rate(ids):
                aff = sum(st[i].get("numAffected", 0) or 0 for i in ids if i in st)
                risk = sum(st[i].get("numAtRisk", 0) or 0 for i in ids if i in st)
                return aff, risk
            da, dr = rate(with_drug)
            ca, cr = rate(without)
            ctrl_titles = [g.get("title", "") for g in groups if g.get("id") in without]
            out.append({
                "nct": study["protocolSection"]["identificationModule"]["nctId"],
                "title": study["protocolSection"]["identificationModule"].get("briefTitle", ""),
                "category": category, "signal": sig_name, "level": level, "kind": kind,
                "term": ev.get("term"), "vocab": ev.get("sourceVocabulary") or ae.get("sourceVocabulary"),
                "drug_affected": da, "drug_at_risk": dr, "ctrl_affected": ca, "ctrl_at_risk": cr,
                "ctrl_is_placebo": any(PLACEBO_RX.search(t) for t in ctrl_titles),
                "threshold": ae.get("frequencyThreshold"),
            })
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cache = Path(sys.argv[1]).expanduser()
    cache.mkdir(parents=True, exist_ok=True)
    refresh = "--refresh" in sys.argv
    today = date.today()

    per_drug, hits, class_hits, extras = {}, [], [], defaultdict(Counter)
    examples = {}
    for drug in OPIOIDS + GLP1:
        data = pull(drug, cache, refresh)
        cats = Counter()
        n_ae, n_terms, useful_safety = 0, 0, 0
        for s in data["studies"]:
            cat, _ = classify(s, drug)
            cats[cat] += 1
            ae, groups, with_drug, without = ae_groups(s, drug)
            has_ae = bool(groups)
            n_ae += has_ae
            n_terms += len(ae.get("seriousEvents", [])) + len(ae.get("otherEvents", []))
            # "about our drug's safety": our drug is tested (experimental), not PK/BE, and an AE group is attributable to it
            safety = cat == "experimental" and has_ae and bool(with_drug)
            useful_safety += safety
            if safety and without:
                extras["safety_with_control"][drug] += 1
            # data-shape facts
            thr = ae.get("frequencyThreshold")
            extras["threshold"][str(thr)] += 1
            for kind in ("seriousEvents", "otherEvents"):
                for ev in ae.get(kind, []):
                    v = (ev.get("sourceVocabulary") or ae.get("sourceVocabulary") or "").strip()
                    extras["vocab"][re.sub(r"\s+", " ", v.upper())[:20] or "(blank)"] += 1
            if has_ae and not with_drug and cat in ("experimental", "comparator"):
                extras["ae_group_unattributable"][drug] += 1
            st = s.get("protocolSection", {}).get("statusModule", {})
            lu = st.get("lastUpdatePostDateStruct", {}).get("date", "")
            rf = st.get("resultsFirstPostDateStruct", {}).get("date", "")
            for label, d in (("last_update", lu), ("results_first", rf)):
                if len(d) >= 7:
                    yr = int(d[:4])
                    extras[label + "_year"][str(yr)] += 1
                    try:
                        days = (today - date.fromisoformat(d if len(d) == 10 else d + "-01")).days
                        for win in (30, 90, 365):
                            if days <= win:
                                extras[f"{label}_within_{win}d"][drug] += 1
                    except ValueError:
                        pass
            # one example per category for the page
            key = (drug, cat)
            if key not in examples and drug in ("semaglutide", "morphine", "oxycodone"):
                examples[key] = {"nct": s["protocolSection"]["identificationModule"]["nctId"],
                                 "title": s["protocolSection"]["identificationModule"].get("briefTitle", ""),
                                 "arms": [(a.get("type"), a.get("label")) for a in s["protocolSection"].get("armsInterventionsModule", {}).get("armGroups", [])][:4]}
            for sig_name, spec in SIGNALS.get(drug, {}).items():
                hits += signal_hits(s, drug, sig_name, spec, cat)
            for sig_name, spec in CLASS_CHECK.get(drug, {}).items():
                class_hits += [dict(h, drug=drug) for h in signal_hits(s, drug, sig_name, spec, cat)]
        per_drug[drug] = {"with_results": data["totalCount"], "pulled": len(data["studies"]),
                          "seconds": data["seconds"], "categories": dict(cats), "with_ae_module": n_ae,
                          "ae_term_rows": n_terms, "about_our_drug_safety": useful_safety}
        print(f"{drug:14} {data['totalCount']:4} studies  safety={useful_safety:4}  {dict(cats)}", flush=True)

    def listed(h):  # level 1: trial tests our drug and lists the term in a drug arm
        return h["category"] == "experimental" and h["drug_affected"] > 0

    def useful(h):  # level 2 (the gate): ... AND there is a control arm AND the drug arm rate is higher
        return (listed(h) and h["ctrl_at_risk"] > 0
                and h["drug_affected"] / max(h["drug_at_risk"], 1) > h["ctrl_affected"] / h["ctrl_at_risk"])

    def tally(hs, sig, level):
        uniq = lambda f: len({h["nct"] for h in hs if h["signal"] == sig and h["level"] == level and f(h)})
        return {"any_category": uniq(lambda h: True), "listed": uniq(listed), "useful": uniq(useful)}

    summary = {
        "run_date": today.isoformat(), "per_drug": per_drug,
        "totals": {k: sum(v[k] for v in per_drug.values()) for k in ("with_results", "with_ae_module", "ae_term_rows", "about_our_drug_safety")},
        "category_totals": dict(sum((Counter(v["categories"]) for v in per_drug.values()), Counter())),
        "signal_hits": hits, "class_hits": class_hits,
        "signal_tally": {f"{d}|{sg}": {lvl: tally(hits, sg, lvl) for lvl in ("exact", "near")}
                         for d, sigs in SIGNALS.items() for sg in sigs},
        "class_tally": {f"{d}|{sg}": tally([h for h in class_hits if h["drug"] == d], sg, "exact")
                        for d in CLASS_CHECK for sg in CLASS_CHECK[d]},
        "extras": {k: dict(v) for k, v in extras.items()},
        "examples": {f"{d}|{c}": v for (d, c), v in examples.items()},
    }
    (cache / "summary.json").write_text(json.dumps(summary, indent=1))
    print("\nTotals:", summary["totals"])
    print("Categories:", summary["category_totals"])
    print("Signal hits (unique trials): any_category / listed in tested drug arm / useful = higher than control")
    for k, v in summary["signal_tally"].items():
        print(f"  {k:45} exact={v['exact']}  near={v['near']}")
    for k, v in summary["class_tally"].items():
        print(f"  class {k:39} {v}")


if __name__ == "__main__":
    main()
