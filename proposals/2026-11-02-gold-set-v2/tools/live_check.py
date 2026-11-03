"""Freshness check after the answers are frozen: re-fetch every captured source and re-derive the answers.

    python3 live_check.py <scratch_dir>

Frozen files are never modified. Live bytes go to <scratch_dir>/live-root (a throwaway copy of the
inputs); answers are re-derived there with the same code and compared with the frozen answers.
Writes ../drift-report.json.
"""
import json
import shutil
import sys
from pathlib import Path
import v2lib as L

FROZEN = L.ROOT
LIVE = Path(sys.argv[1]) / "live-root"
if LIVE.exists():
    shutil.rmtree(LIVE)
(LIVE / "claude").mkdir(parents=True)
shutil.copytree(FROZEN / "shared", LIVE / "shared")
shutil.copy(FROZEN / "traces.json", LIVE / "traces.json")
shutil.copy(FROZEN / "claude" / "s4-annotations.json", LIVE / "claude" / "s4-annotations.json")

# Point the shared helpers at the throwaway copy before build_trace reads any path.
L.ROOT, L.SHARED, L.EVIDENCE, L.MANIFEST = LIVE, LIVE / "shared", LIVE / "shared" / "evidence", LIVE / "shared" / "source-manifest.json"
import build_trace as B  # noqa: E402

man = json.loads(L.MANIFEST.read_text())
started = L.now_utc()
rows = []
L.srlc_session()
for sid, m in sorted(man["sources"].items()):
    f = L.fetch(m["requested_url"].replace("api_key=REDACTED", ""), data=m.get("post_form"), browser="safetylabelingchanges" in m["requested_url"])
    row = {"source_id": sid, "frozen_sha256": m["sha256"], "frozen_retrieved_at_utc": m["retrieved_at_utc"],
           "live_retrieved_at_utc": f.retrieved_at_utc, "live_http_status": f.status}
    if not f.ok:
        row.update(state="live_fetch_failed", error=f.error)  # a failed re-fetch says nothing about the source content
    else:
        h = L.sha256(f.body)
        row.update(live_sha256=h, state="identical" if h == m["sha256"] else "bytes_changed")
        if h != m["sha256"]:
            (LIVE / "shared" / m["evidence_file"]).write_bytes(f.body)
            m["sha256"], m["retrieved_at_utc"] = h, f.retrieved_at_utc
            if m["kind"] == "json":
                meta = json.loads(f.body).get("meta") if isinstance(json.loads(f.body), dict) else None
                if meta:
                    row["live_meta"] = {k: v for k, v in meta.items() if k in ("last_updated", "results")}
                    row["frozen_meta"] = m.get("source_metadata")
    rows.append(row)
L.MANIFEST.write_text(json.dumps(man, indent=1))

# Re-derive answers from live bytes (S4 label view is rebuilt if the label XML changed).
answer_drift = {}
for tid in sorted(B.TRACES):
    if any(r["state"] == "bytes_changed" and r["source_id"] == f"{tid}.s4_label" for r in rows):
        root, secs = B.label_sections((L.EVIDENCE / tid / "s4_label.xml").read_bytes())
        view = json.loads((L.EVIDENCE / tid / "s4_label.sections.json").read_text())
        view["sections"] = secs
        (L.EVIDENCE / tid / "s4_label.sections.json").write_text(json.dumps(view, ensure_ascii=False))
    try:
        B.stage_answers(tid)
        live = {json.loads(l)["step"]: json.loads(l)["answer"] for l in (LIVE / "claude" / "traces" / f"{tid}.jsonl").read_text().splitlines()}
        frozen = {json.loads(l)["step"]: json.loads(l)["answer"] for l in (FROZEN / "claude" / "traces" / f"{tid}.jsonl").read_text().splitlines()}
        diff = {s: {"frozen": frozen[s], "live": live[s]} for s in frozen if frozen[s] != live[s]}
        answer_drift[tid] = {"state": "answers_changed" if diff else "answers_unchanged", "changed_steps": diff}
    except (AssertionError, SystemExit, StopIteration, KeyError, IndexError) as e:
        answer_drift[tid] = {"state": "rederivation_failed", "error": f"{type(e).__name__}: {e}"}

from collections import Counter
rep = {"checked_at_utc": started, "frozen_answers_modified": False,
       "source_states": dict(Counter(r["state"] for r in rows)), "answer_states": dict(Counter(v["state"] for v in answer_drift.values())),
       "note": "Live lookup time is not source publication time. Changed bytes do not always change an answer (e.g. page tokens, list order). "
               "Frozen answers stay as the reference; drift is reported here only.",
       "sources": rows, "answers": answer_drift}
(FROZEN / "drift-report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
print(json.dumps({k: rep[k] for k in ("source_states", "answer_states")}))
for tid, v in answer_drift.items():
    if v["state"] != "answers_unchanged":
        print(tid, v["state"], list(v.get("changed_steps", {})) or v.get("error"))
