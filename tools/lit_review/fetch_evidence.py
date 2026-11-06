"""Fetch PubMed evidence for one drug–event signal (AI literature review, feature F01).

Uses NCBI E-utilities (public, free; 3 requests/s without a key).
Writes evidence/<id>.json (search, papers, retraction flags, metrics) and evidence/<id>-abstracts.txt.

    python tools/lit_review/fetch_evidence.py <id> "<pubmed query>" [--top 8]
"""
import argparse
import json
import pathlib
import time
import urllib.parse
import urllib.request

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/12-features/ai-literature-review/evidence"
calls = 0


def get(endpoint, **params):
    global calls
    calls += 1
    time.sleep(0.4)  # stay under 3 requests/s
    url = f"{BASE}/{endpoint}.fcgi?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("query")
    ap.add_argument("--top", type=int, default=8)
    a = ap.parse_args()
    t0 = time.time()

    search = json.loads(get("esearch", db="pubmed", retmode="json", sort="relevance", retmax=a.top * 2, term=a.query))["esearchresult"]
    ids = search["idlist"]
    papers = []
    if ids:
        summ = json.loads(get("esummary", db="pubmed", retmode="json", id=",".join(ids)))["result"]
        for i in ids:
            s = summ[i]
            types = s.get("pubtype", [])
            papers.append({"pmid": i, "year": s.get("pubdate", "")[:4], "journal": s.get("source"), "title": s.get("title"),
                           "pubtype": types, "retracted": any("Retract" in t for t in types)})
    keep = [p["pmid"] for p in papers if not p["retracted"]][: a.top]
    abstracts = get("efetch", db="pubmed", rettype="abstract", retmode="text", id=",".join(keep)) if keep else ""

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{a.id}-abstracts.txt").write_text(abstracts)
    result = {"id": a.id, "query": a.query, "hits": int(search["count"]), "papers": papers, "abstracts_kept": keep,
              "metrics": {"api_calls": calls, "seconds": round(time.time() - t0, 1), "abstract_chars": len(abstracts),
                          "approx_tokens": len(abstracts) // 4, "retracted_dropped": sum(p["retracted"] for p in papers)}}
    (OUT / f"{a.id}.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in ("id", "hits", "metrics")}))
    for p in papers:
        print(p["pmid"], p["year"], p["journal"], "|", p["title"][:110], "| RETRACTED" if p["retracted"] else "")


if __name__ == "__main__":
    main()
