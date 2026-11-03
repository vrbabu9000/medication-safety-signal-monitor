"""Write ../cards/<Txx>-<brand>.md: a one-page walkthrough of how each source was used for one trace.

    python3 make_card.py T01 [T02 ...]   |   python3 make_card.py all
Generated only from answers, manifest and verification output, so a card cannot drift from the evidence.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def card(tid):
    rows = {r["step"]: r for r in (json.loads(l) for l in (ROOT / "claude" / "traces" / f"{tid}.jsonl").read_text().splitlines())}
    q = json.loads((ROOT / "shared" / "questions" / f"{tid}.json").read_text())
    ver = json.loads((ROOT / "verification" / f"{tid}.json").read_text())
    man = json.loads((ROOT / "shared" / "source-manifest.json").read_text())["sources"]
    s1, s2, s3, s4, s5, s6, s7, s8 = (rows[f"S{i}"]["answer"] for i in range(1, 9))
    loc4 = next(iter(rows["S4"]["evidence_locators"].values()))
    ings = ", ".join(f"{i['name']} ({i['rxcui']})" for i in s1["ingredients"])
    nf = [x["term"] for x in s6["top_terms_brand"] if not x["found_in_label_scope"]]
    found = [x["term"] for x in s6["top_terms_brand"] if x["found_in_label_scope"]]
    times = sorted(m["retrieved_at_utc"] for m in man.values() if m["trace_id"] == tid)
    spl_meta = man[f"{tid}.s4_label"]["source_metadata"]
    spl_txt = f"{spl_meta['setId']['root']} v{spl_meta['versionNumber']['value']} (effective {spl_meta['effectiveTime']['value']})"
    lines = [
        f"# {tid} · {q['brand']} ({q['class']})",
        "",
        f"**Status:** verified against sources ({ver['passed']}/{len(ver['checks'])} automated checks passed) · pharmacist review **pending** · "
        f"captured {times[0][:16]}Z – {times[-1][:16]}Z · questions sha256 `{ver['questions_sha256'][:12]}…`",
        "",
        "## The trace in one line",
        f"{q['brand']} → RxNorm {s1['brand_rxcui']} ({ings}) → package {s2['package_ndc']} under {s2['application_number']} → "
        f"DailyMed label {spl_txt} → SrLC {s5['entry_date']} → {s6['brand_report_count']} FAERS reports name it in 2025 → "
        f"recall {s7['recall_number']} → trial {s8['nct_id']}.",
        "",
        "## How each source was used",
        "",
        "| Step | Source | What we asked | Answer | How it links |",
        "|---|---|---|---|---|",
        f"| S1 | RxNorm | Which medicine is this? | Brand RxCUI {s1['brand_rxcui']} ({s1['brand_tty']}); ingredient(s) {ings}; multi-ingredient: {s1['multi_ingredient']} | Reverse check: each ingredient lists this brand |",
        f"| S2 | NDC Directory | Which package and who lists it? | {s2['package_ndc']}: {s2['package_description']}; labeler {s2['labeler_name']}; category {s2['marketing_category']}; application {s2['application_number']} | Listing's label set ID = S4 label: **{s2['spl_set_id_matches_s4']}** |",
        f"| S3 | Drugs@FDA | Who holds the application, which strengths? | Sponsor {s3['sponsor_name']}; {len(s3['products'])} product(s): " +
        "; ".join(f"{p['product_number']} {p['dosage_form']} {', '.join(i['strength'] for i in (p['active_ingredients'] or []))}" for p in s3["products"]) +
        " | Same application number as S2 |",
        f"| S4 | DailyMed | In '{loc4['heading']}', what role does '{q['questions'][3]['inputs']['target']}' play? | **{s4}** | Quote: \"{rows['S4']['supporting_quote_or_value']}\" |",
        f"| S5 | SrLC | Latest change with underlined (added/revised) text in Boxed Warning or sections 4/5/6? | {s5['entry_date']} {s5['supplement']}, {s5['subsection']} | Underlined text present in S4 label: **{s5['present_in_s4_label']}** |",
        f"| S6 | FAERS | What do 2025 reports say? | {s6['brand_report_count']} reports name {q['brand'].upper()}; {s6['substance_report_count']} list {s6['active_substance']} (any product) | Top-10 terms checked against S4 label: {len(found)} found, {len(nf)} not found |",
        f"| S7 | FDA enforcement | Any recall? | {s7['recall_number']} ({s7['classification']}, reported status '{s7['status_as_reported']}', {s7['report_date']}): {s7['reason_for_recall'][:140]}{'…' if len(s7['reason_for_recall']) > 140 else ''} | Record text names package {s2['package_ndc']}: **{s7['package_named_in_record']}** ({s7['query_level']}-level query, {s7['records_found']} records) |",
        f"| S8 | ClinicalTrials.gov | What did a trial arm report? | {s8['nct_id']} ({s8['overall_status']}), {s8['group_id']} '{s8['group_title']}': serious AEs {s8['seriousNumAffected']} of {s8['seriousNumAtRisk']} | Group title names the drug |",
        "",
        "## What the safety officer can say from this trace",
        f"- **Not in the label (string check, needs pharmacist review):** {', '.join(nf) if nf else 'none of the top 10 terms'}. "
        f"Found in label: {', '.join(found) if found else 'none'}.",
        f"- **Recall:** {s7['recall_number']} " + ("names this exact package." if s7["package_named_in_record"] else "does not name this package in its own text.") +
        " Reported status is not today's status; hospital exposure needs inventory and lot data.",
        f"- **Label currency:** the latest SrLC change ({s5['entry_date']}) " + ("is" if s5["present_in_s4_label"] else "is **not**") + " reflected in the captured DailyMed label.",
        "",
        "## Traps this trace shows",
    ]
    traps = [rows["S4"]["uncertainty"].split(" Scoped to")[0]]
    if s6["brand_report_count"] != s6["substance_report_count"]:
        traps.append(f"Query scope changes the count: {s6['brand_report_count']} brand-named vs {s6['substance_report_count']} substance-level reports.")
    if s7["package_in_openfda_harmonized_list"] and not s7["package_named_in_record"]:
        traps.append("openFDA's harmonized package list includes this package, but the recall's own text does not name it.")
    traps.append(f"Sponsor '{s3['sponsor_name']}' (Drugs@FDA) vs labeler '{s2['labeler_name']}' (NDC): join on application number, not names.")
    lines += [f"- {t}" for t in traps]
    lines += ["", "## Evidence files", "",
              "| Source ID | sha256 | Retrieved (UTC) |", "|---|---|---|"]
    lines += [f"| `{sid}` | `{m['sha256'][:16]}…` | {m['retrieved_at_utc'][:19]} |" for sid, m in sorted(man.items()) if m["trace_id"] == tid]
    lines += ["", f"Full records: [claude/traces/{tid}.jsonl](../claude/traces/{tid}.jsonl) · checks: [verification/{tid}.json](../verification/{tid}.json) · questions: [shared/questions/{tid}.json](../shared/questions/{tid}.json)", ""]
    out = ROOT / "cards" / f"{tid}-{q['brand'].lower().replace(' ', '-')}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines))
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    ids = sys.argv[1:]
    if ids == ["all"]:
        ids = sorted(p.stem for p in (ROOT / "verification").glob("T*.json"))
    for t in ids:
        card(t)
