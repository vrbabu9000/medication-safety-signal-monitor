"""Combine the 30 trace files into ../claude/answers.jsonl and write ../claude/validation.json.

Run after every trace verifies. Prints a compact per-trace summary used by findings.md.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
traces = json.loads((ROOT / "traces.json").read_text())["traces"]
ids = [t["trace_id"] for t in traces]
rows = []
for tid in ids:
    rows += [json.loads(l) for l in (ROOT / "claude" / "traces" / f"{tid}.jsonl").read_text().splitlines()]
out = ROOT / "claude" / "answers.jsonl"
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
ans_sha = hashlib.sha256(out.read_bytes()).hexdigest()

man = json.loads((ROOT / "shared" / "source-manifest.json").read_text())["sources"]
ver = {tid: json.loads((ROOT / "verification" / f"{tid}.json").read_text()) for tid in ids}
qsha = {tid: hashlib.sha256((ROOT / "shared" / "questions" / f"{tid}.json").read_bytes()).hexdigest() for tid in ids}
hash_ok = all(hashlib.sha256((ROOT / "shared" / m["evidence_file"]).read_bytes()).hexdigest() == m["sha256"] for m in man.values())
links = [(r["case_id"], k, v) for r in rows for k, v in r["link_checks"].items()]
case_ids = [r["case_id"] for r in rows]
val = {
    "dataset_id": "MSSM-30-v2", "annotator": "claude", "answers_jsonl_sha256": ans_sha,
    "traces": len(ids), "steps_answered": len(rows), "unique_case_ids": len(set(case_ids)),
    "duplicate_case_ids": [c for c, n in Counter(case_ids).items() if n > 1],
    "every_trace_has_S1_to_S8": all(sorted(r["step"] for r in rows if r["trace_id"] == t) == [f"S{i}" for i in range(1, 9)] for t in ids),
    "evidence_files": len(man), "all_manifest_hashes_match": hash_ok,
    "all_captures_status_captured": all(m["status"] == "captured" for m in man.values()),
    "identity_guards_passed": sum(1 for m in man.values() if m["status"] == "captured"),
    "identity_guards_rejected": sum(1 for m in man.values() if m["status"] == "rejected_identity_guard"),
    "api_key_in_any_saved_url": any("api_key=" in m["requested_url"] and "REDACTED" not in m["requested_url"] for m in man.values()),
    "openfda_requests_with_key": sum(m["openfda_api_key_used"] for m in man.values()),
    "resolved": sum(r["answer_status"] == "resolved" for r in rows),
    "unresolved": sum(r["answer_status"] != "resolved" for r in rows),
    "intentional_abstentions": [r["case_id"] for r in rows if r["answer"] == "unknown"],
    "per_source_totals": dict(Counter(r["category"] for r in rows)),
    "per_check_type_totals": dict(Counter(r["check_type"] for r in rows)),
    "s4_class_totals": dict(Counter(r["answer"] for r in rows if r["step"] == "S4")),
    "link_checks_evaluated": len(links), "link_checks_true": sum(1 for *_, v in links if v is True),
    "link_checks_false": [f"{c}: {k}" for c, k, v in links if v is False],
    "automated_verification": {tid: {"passed": v["passed"], "total": len(v["checks"]), "failed": len(v["failed"])} for tid, v in ver.items()},
    "automated_checks_total": sum(len(v["checks"]) for v in ver.values()),
    "automated_checks_failed": sum(len(v["failed"]) for v in ver.values()),
    "questions_sha256": qsha,
    "all_human_review_pending": all(r["human_review_status"] == "pending" for r in rows),
    "notes": ["Self-verification by code against source bytes; not an independent human or clinical evaluation.",
              "Candidate reference set; not a clinician-adjudicated gold standard and not a label-extraction benchmark.",
              "FAERS evidence is aggregate counts only (limit=0 totals and count queries); no report records are stored."]}
(ROOT / "claude" / "validation.json").write_text(json.dumps(val, indent=1, ensure_ascii=False) + "\n")
print(json.dumps({k: val[k] for k in ("steps_answered", "unique_case_ids", "all_manifest_hashes_match", "unresolved", "automated_checks_total",
                                       "automated_checks_failed", "link_checks_evaluated", "link_checks_false", "api_key_in_any_saved_url")}, indent=0))
print("answers sha256", ans_sha)
by = {}
for r in rows:
    by.setdefault(r["trace_id"], {})[r["step"]] = r["answer"]
for t in traces:
    a = by[t["trace_id"]]
    nf = [x["term"] for x in a["S6"]["top_terms_brand"] if not x["found_in_label_scope"]]
    print(f"{t['trace_id']}|{t['brand']}|{t['class']}|{a['S1']['multi_ingredient']}|{a['S3']['sponsor_name']}|{a['S4']}|{a['S5']['entry_date']}|{a['S5']['present_in_s4_label']}|"
          f"{a['S6']['brand_report_count']}|{a['S6']['substance_report_count']}|{';'.join(nf)}|{a['S7']['query_level']}|{a['S7']['recall_number']}|{a['S7']['classification']}|"
          f"{a['S7']['status_as_reported']}|{a['S7']['package_named_in_record']}|{a['S7']['package_in_openfda_harmonized_list']}|{a['S8']['nct_id']}|{a['S8']['seriousNumAffected']}/{a['S8']['seriousNumAtRisk']}")
