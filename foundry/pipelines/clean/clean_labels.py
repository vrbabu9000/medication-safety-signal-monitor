# Labels (silver): one row per label version, and the safety sections of each version as plain text.
# Contract: docs/04-architecture/dataset-contracts-v1.md §2. Rules: DailyMed is label truth (D019); sections = the D037 safety
# sections (Boxed Warning, Contraindications, Warnings and Precautions, Warnings, Precautions, Adverse Reactions) by LOINC code.
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/clean_labels.py
import re
import xml.etree.ElementTree as ET

import polars as pl
from transforms.api import Input, Output, transform

RAW = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/raw/"
CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
NS = {"v3": "urn:hl7-org:v3"}
# LOINC section codes. 43685-7 is the modern (PLR) label; 34071-1 + 42232-9 are older (non-PLR) labels.
SECTIONS = {"34066-1": "Boxed Warning", "34070-3": "Contraindications", "43685-7": "Warnings and Precautions",
            "34071-1": "Warnings", "42232-9": "Precautions", "34084-4": "Adverse Reactions"}


def ymd(s):
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if s and len(s) >= 8 and s[:8].isdigit() else None


def clean_text(el):
    return re.sub(r"\s+", " ", " ".join(el.itertext())).strip()


def code_of(sec):
    c = sec.find("v3:code", NS)
    return c.get("code") if c is not None else None


def walk(sec, depth=1):
    yield sec, depth
    for sub in sec.findall("v3:component/v3:section", NS):
        yield from walk(sub, depth + 1)


def good_xml(df):  # DailyMed can answer 200 with the text "None" (2 tramadol repackager labels, step 9): not XML, so left out; has_xml shows it
    return df.filter((pl.col("http_status").cast(pl.Utf8) == "200") & pl.col("xml_text").is_not_null() & pl.col("xml_text").str.starts_with("<"))


@transform.using(out=Output(CLEAN + "clean_label_versions"), index=Input(RAW + "raw_dailymed_spl_index"), xml=Input(RAW + "raw_dailymed_spl_xml"))
def compute_label_versions(out, index, xml):
    idx = index.polars().filter(pl.col("http_status") == 200).unique(subset=["setid"], keep="first")
    rows = []
    xml_by_setid = {r["setid"]: r for r in good_xml(xml.polars()).to_dicts()}
    for r in idx.to_dicts():
        x = xml_by_setid.get(r["setid"])
        root = ET.fromstring(x["xml_text"]) if x else None
        eff = root.find("v3:effectiveTime", NS).get("value") if root is not None else None
        rows.append({"setid": r["setid"], "spl_version": int(r["spl_version"]), "title": r["title"],
                     "published_date": r["published_date"], "effective_date": ymd(eff), "has_xml": x is not None,
                     "xml_version_matches": x is not None and str(x["xml_version_number"]) == str(r["spl_version"]),
                     "xml_bytes": int(x["xml_bytes"]) if x else None, "is_plr_format": root is not None and root.find(".//v3:code[@code='43685-7']", NS) is not None,
                     "source_url": x["source_url"] if x else None, "retrieved_at": x["retrieved_at"] if x else r["retrieved_at"]})
    out.write_table(pl.DataFrame(rows, infer_schema_length=None))


def safety_sections(sec, depth=1):
    # Yield (section, depth) for the first safety section on each branch; its sub-sections stay inside its text.
    if code_of(sec) in SECTIONS:
        yield sec, depth
        return
    for sub in sec.findall("v3:component/v3:section", NS):
        yield from safety_sections(sub, depth + 1)


@transform.using(out=Output(CLEAN + "clean_label_sections"), xml=Input(RAW + "raw_dailymed_spl_xml"))
def compute_label_sections(out, xml):
    # One row per safety section of each label version. Nested sub-sections are folded into their parent's text
    # (counted, not repeated), because a reaction is "in the label" if it is anywhere under the parent (D037 dataset rule).
    # A code that appears twice in one label (rare) is kept as one row with both texts and n_occurrences = 2.
    rows = []
    for x in good_xml(xml.polars()).to_dicts():
        root = ET.fromstring(x["xml_text"])
        version = int(root.find("v3:versionNumber", NS).get("value"))
        found = {}
        for top in root.findall("v3:component/v3:structuredBody/v3:component/v3:section", NS):
            for sec, depth in safety_sections(top):
                code = code_of(sec)
                t = sec.find("v3:title", NS)
                e = found.setdefault(code, {"setid": x["setid"], "spl_version": version, "section_code": code,
                                            "section_name": SECTIONS[code], "titles": [], "ids": [], "nesting_depth": depth,
                                            "n_occurrences": 0, "n_subsections": 0, "n_tables": 0, "parts": []})
                e["n_occurrences"] += 1
                e["titles"].append(clean_text(t) if t is not None else "")
                e["ids"].append(sec.get("ID") or "")
                e["n_subsections"] += sum(1 for _, d in walk(sec) if d > 1)
                e["n_tables"] += len(sec.findall(".//v3:table", NS))
                e["parts"].append(clean_text(sec))
        for e in found.values():
            text = "\n\n".join(e.pop("parts"))
            rows.append({**e, "titles": None, "ids": None, "section_title": " | ".join(e["titles"]), "section_xml_id": " | ".join(e["ids"]),
                         "section_text": text, "n_chars": len(text), "text_is_empty": not text.strip(),
                         "source_url": x["source_url"], "retrieved_at": x["retrieved_at"]})
    out.write_table(pl.DataFrame(rows, infer_schema_length=None).drop(["titles", "ids"]))
