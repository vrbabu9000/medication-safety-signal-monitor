# Curated (gold), step 8: reaction statistics per drug (PRR, D006) and signal candidates = statistically disproportionate AND
# not found in the drug's labels. Contract: conventions §5 (AdverseEventStat, Signal). Rules: D006 (PRR, Evans N>=3, PRR>=2, chi2>=4),
# D021/D022/D023 already applied in clean FAERS (suspect roles, current case versions, duplicate fold: suppressed cases excluded),
# D037 (a FAERS term "is in the label" when the exact term or its US spelling appears in a safety section; AI extraction adds a
# second check on atomic terms), D016 (rank clinical reactions; tag abuse/overdose, product-use, pregnancy/neonatal, litigation-style).
# A signal is a candidate for human review, not a proven causal effect.
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/ontology_signals.py
import hashlib
import math
import re

import polars as pl
from transforms.api import Input, Output, transform

try:
    from myproject.datasets.label_synonyms import SYN_VERSION, SYNONYMS
except ImportError:  # local run: the module sits next to this file
    import importlib.util, os
    _spec = importlib.util.spec_from_file_location("label_synonyms", os.path.join(os.path.dirname(os.path.abspath(__file__)), "label_synonyms.py"))
    _mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
    SYN_VERSION, SYNONYMS = _mod.SYN_VERSION, _mod.SYNONYMS

CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
CURATED = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/"
RULE = "prr_evans_v2"  # v2: mass-polypharmacy reports (>= MAX_DRUG_ROWS drugs) left out of the primary population (D023 v2)
MAX_DRUG_ROWS = 30
LABEL_CHECK = "text+ai_v1+" + SYN_VERSION  # + reviewed label <-> FAERS synonyms (A014, D043)
WINDOW = "FAERS 2026Q1-2026Q2"
# D016 buckets: tag, don't rank. First match wins; everything else is "clinical".
BUCKETS = [  # keyword stand-in for MedDRA groupings (no MedDRA licence); reviewed by hand, see A012
    ("product_use_error", r"off label|unapproved indication|wrong technique|dose omission|incorrect dose|inappropriate schedule|expired product|"
                          r"device |product use|medication error|product dose|underdose|extra dose|wrong drug|product storage|product quality|"
                          r"product substitution|product prescribing|intercepted|counterfeit|product tampering|prescription form|"
                          r"contraindicated product|product administered|product formulation|product physical|product container|packaging|"
                          r"drug-drug interaction|drug interaction|labelled drug"),
    ("efficacy", r"drug ineffective|therapeutic product effect|drug effect less|therapy non-responder|treatment failure|inadequate analgesia|"
                 r"drug effect decreased|therapeutic response decreased|drug tolerance"),
    ("abuse_overdose", r"overdose|drug abuse|abuse|dependence|withdrawal|misuse|intentional|toxicity to various|diversion|drug use disorder|"
                       r"substance use|addiction|drug screen|blood drug level|drug level increased|postmortem|pharmaceutical nomadism|"
                       r"drug seeking|accidental exposure|accidental poisoning|poisoning|without a prescription|detoxification"),
    ("pregnancy_neonatal", r"pregnancy|foetal|fetal|neonatal|maternal|exposure via breast|premature|congenital|malformation|developmental|"
                           r"learning disability|cerebral ventricle dilatation|in utero|birth"),
    ("social_legal", r"homicide|assault|victim|neglect|imprisonment|incarceration|arrest|legal problem|high risk sexual|impaired driving|"
                     r"road traffic|completed suicide|suicid|death of relative|domestic|homeless|social problem|criminal|gun shot|stab wound"),
    ("litigation_style", r"emotional distress|injury$|loss of employment|anxiety$|impaired quality of life|economic problem|"
                         r"loss of personal independence"),
    ("administrative", r"medical observation|hospitalisation|hospitalization|no adverse event|unevaluable|general physical health deterioration"),
]
_US = [("oesophag", "esophag"), ("oedema", "edema"), ("diarrhoea", "diarrhea"), ("haem", "hem"), ("anaem", "anem"), ("aemia", "emia"),
       ("oestr", "estr"), ("foet", "fet"), ("paed", "ped"), ("isation", "ization"), ("ise ", "ize "), ("yse ", "yze "), ("leukaem", "leukem"),
       ("tumour", "tumor"), ("colour", "color"), ("behaviour", "behavior"), ("centre", "center"), ("noea", "nea"), ("rrhoea", "rrhea"),
       ("ised ", "ized "), ("ae", "e")]  # noea/rrhoea/ised added at A014 (dyspnoea, rhinorrhoea, generalised were missed)


def words(s):
    return " " + re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip() + " "


def spellings(term):
    """The term and its US spelling (D037), both as padded word strings."""
    w = words(term)
    us = w
    for gb, am in _US:
        us = us.replace(gb, am)
    return {w, us}


def bucket(pt):
    low = pt.lower()
    for name, rx in BUCKETS:
        if re.search(rx, low):
            return name
    return "clinical"


def prr_row(a, n_drug, c, n_other):
    """2x2 table: a = drug & reaction, b = drug & other, c = other drugs & reaction, d = other & other. chi2 with Yates (Evans)."""
    b, d = n_drug - a, n_other - c
    n = a + b + c + d
    prr = (a / n_drug) / (c / n_other) if c and n_other else None
    den = (a + b) * (c + d) * (a + c) * (b + d)
    chi2 = n * max(abs(a * d - b * c) - n / 2, 0) ** 2 / den if den else None
    lo = hi = None
    if prr and a and c and b and d:  # 95% CI of PRR (log method)
        se = math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
        lo, hi = math.exp(math.log(prr) - 1.96 * se), math.exp(math.log(prr) + 1.96 * se)
    evans = a >= 3 and (c == 0 or (prr is not None and prr >= 2 and chi2 is not None and chi2 >= 4))
    return b, d, prr, chi2, lo, hi, evans


def label_texts(ingredient_products, products, sections):
    """Per ingredient: the safety-section text of each product's reference label (LD1), as padded word strings."""
    ref = ingredient_products.join(products.select("product_key", "reference_label_key"), on="product_key").drop_nulls("reference_label_key")
    secs = sections.with_columns(pl.concat_str([pl.col("setid"), pl.lit("|v"), pl.col("spl_version").cast(pl.Utf8)]).alias("label_key"))
    j = ref.join(secs.select("label_key", "section_name", "section_text"), left_on="reference_label_key", right_on="label_key")
    out = {}
    for r in j.iter_rows(named=True):
        out.setdefault(r["ingredient_rxcui"], []).append((r["reference_label_key"], r["section_name"], words(r["section_text"])))
    return out


@transform.using(stats_out=Output(CURATED + "ontology_ae_stats"), signals_out=Output(CURATED + "ontology_signal_signals"),
                 synonyms_out=Output(CURATED + "ontology_label_synonyms"),
                 cases=Input(CLEAN + "clean_faers_cases_current"), reactions=Input(CLEAN + "clean_faers_case_reactions"),
                 drug_reaction=Input(CLEAN + "clean_faers_drug_reaction"), ingredients=Input(CLEAN + "clean_drug_ingredients"),
                 drug_product=Input(CURATED + "ontology_link_drug_product"), products=Input(CURATED + "ontology_product_products"),
                 sections=Input(CLEAN + "clean_label_sections"), labeled=Input(CURATED + "ontology_labeled_reactions"))
def compute(stats_out, signals_out, synonyms_out, cases, reactions, drug_reaction, ingredients, drug_product, products, sections, labeled):
    # Reference population: every current, non-suppressed case (D022, D023), not only formulary cases. D023 v2: reports listing
    # MAX_DRUG_ROWS or more drugs (mass polypharmacy, e.g. one patient re-filed with changing ages) are left out of the primary
    # population; their count per drug-reaction is kept as a_mass_reports so the officer can see what was set aside.
    cs = cases.polars().filter(~pl.col("dup_suppressed"))
    mass = cs.filter(pl.col("n_drug_rows") >= MAX_DRUG_ROWS).select("caseid")
    primary = cs.filter(pl.col("n_drug_rows") < MAX_DRUG_ROWS).select("caseid")
    n_all = primary.height
    rx = reactions.polars().filter(~pl.col("dup_suppressed")).select("caseid", "pt").join(primary, on="caseid")
    pt_cases = rx.group_by("pt").agg(pl.len().alias("pt_cases"))
    dr_all = drug_reaction.polars().filter(~pl.col("dup_suppressed"))
    a_mass = dr_all.join(mass, on="caseid").group_by(["ingredient_rxcui", "pt"]).agg(pl.col("caseid").n_unique().alias("a_mass_reports"))
    dr = dr_all.join(primary, on="caseid")
    n_drug = dr.group_by("ingredient_rxcui").agg(pl.col("caseid").n_unique().alias("n_drug"))
    a_tab = dr.group_by(["ingredient_rxcui", "pt"]).agg(pl.col("caseid").n_unique().alias("a"))
    tab = a_tab.join(n_drug, on="ingredient_rxcui").join(pt_cases, on="pt").join(a_mass, on=["ingredient_rxcui", "pt"], how="left").join(ingredients.polars().select("ingredient_rxcui", "ingredient_name"), on="ingredient_rxcui")

    texts = label_texts(drug_product.polars(), products.polars(), sections.polars())
    lr = labeled.polars().select("label_key", "section_name", "normalized_term", "labeled_reaction_key", "quote")
    ai_terms = {}  # label_key -> {spelling: (labeled_reaction_key, section, quote)}
    for r in lr.iter_rows(named=True):
        for sp in spellings(r["normalized_term"]):
            ai_terms.setdefault(r["label_key"], {}).setdefault(sp, (r["labeled_reaction_key"], r["section_name"], r["quote"]))

    syn = {}  # FAERS term -> [(band, spellings of the label phrase, phrase)], high band first
    for pt, phrase, band, _ in SYNONYMS:
        if band in ("high", "medium"):
            syn.setdefault(pt, []).append((band, spellings(phrase), phrase))
    for v in syn.values():
        v.sort(key=lambda x: x[0] != "high")
    synonyms_out.write_table(pl.DataFrame([{"faers_pt": pt, "label_phrase": ph, "band": b, "note": n, "syn_version": SYN_VERSION}
                                           for pt, ph, b, n in SYNONYMS], schema={"faers_pt": pl.Utf8, "label_phrase": pl.Utf8, "band": pl.Utf8,
                                                                               "note": pl.Utf8, "syn_version": pl.Utf8}))

    rows = []
    for r in tab.iter_rows(named=True):
        a, nd, c = r["a"], r["n_drug"], r["pt_cases"] - r["a"]
        b, d, prr, chi2, lo, hi, evans = prr_row(a, nd, c, n_all - nd)
        labs = texts.get(r["ingredient_rxcui"], [])
        sp = spellings(r["pt"])
        method = lab_key = lab_sec = lr_key = quote = None
        ai_labels = {k for k, _, _ in labs} & set(ai_terms)
        for k in sorted(ai_labels):  # 1) AI check: an extracted atomic term equals the FAERS term (or its US spelling)
            hit = next((ai_terms[k][s] for s in sp if s in ai_terms[k]), None)
            if hit:
                method, lab_key, lr_key, lab_sec, quote = "ai_term_exact", k, hit[0], hit[1], hit[2]
                break
        if method is None:  # 2) D037 text check: the term appears in a safety section of a reference label
            hit = next(((k, n) for k, n, t in labs if any(s in t for s in sp)), None)
            if hit:
                method, lab_key, lab_sec = "label_text", hit[0], hit[1]
        if method is None:  # 3) synonym table (A014, D043): a reviewed label phrase for this term is in a safety section
            for band, ps, phrase in syn.get(r["pt"], []):
                hit = next(((k, n) for k, n, t in labs if any(s in t for s in ps)), None)
                if hit:
                    method, lab_key, lab_sec, quote = f"synonym_{band}", hit[0], hit[1], phrase
                    break
        n_mention = sum(1 for _, _, t in labs if any(s in t for s in sp))
        # A medium-band synonym is a close or broader idea: "possibly in label", kept visible but never ranked (D039 G4).
        status = ("no_reference_label" if not labs else "not_in_label" if method is None
                  else "possibly_in_label" if method == "synonym_medium" else "in_label")
        rows.append({"stat_key": f"{r['ingredient_rxcui']}|{r['pt']}|{WINDOW}|{RULE}", "ingredient_rxcui": r["ingredient_rxcui"],
                     "ingredient_name": r["ingredient_name"], "pt": r["pt"], "bucket": bucket(r["pt"]), "window": WINDOW, "rule": RULE,
                     "a_drug_reaction": a, "b_drug_other": b, "c_other_reaction": c, "d_other_other": d, "n_drug_cases": nd, "n_all_cases": n_all,
                     "a_mass_reports": r["a_mass_reports"] or 0,
                     "prr": prr, "prr_ci_low": lo, "prr_ci_high": hi, "chi2_yates": chi2, "meets_evans": evans,
                     "label_status": status, "label_match_method": method, "label_match_label_key": lab_key, "label_match_section": lab_sec,
                     "label_match_labeled_reaction_key": lr_key, "label_match_quote": quote, "n_reference_labels": len({k for k, _, _ in labs}),
                     "n_label_sections_mentioning": n_mention, "label_check": LABEL_CHECK,
                     "ai_labels_checked": len(ai_labels)})
    stats = pl.DataFrame(rows, infer_schema_length=None)
    stats_out.write_table(stats)

    # Signals: Evans + not found in any reference label (or only a medium synonym). Ranked inside D016 buckets (clinical first) by chi2.
    sig = stats.filter(pl.col("meets_evans") & pl.col("label_status").is_in(["not_in_label", "possibly_in_label"])).with_columns(
        pl.concat_str(["ingredient_rxcui", pl.lit("|"), "pt", pl.lit("|"), "rule"]).alias("signal_key"),
        (pl.col("a_mass_reports") / (pl.col("a_drug_reaction") + pl.col("a_mass_reports"))).alias("mass_report_share"))
    # A reaction mostly carried by mass-polypharmacy reports is likely the same re-filed patients: shown with a caution, not ranked.
    sig = sig.with_columns(((pl.col("bucket") == "clinical") & (pl.col("mass_report_share") < 0.5)
                            & (pl.col("label_status") == "not_in_label")).alias("is_ranked"),
        pl.when(pl.col("mass_report_share") >= 0.5).then(pl.lit("mostly_mass_reports"))
          .when(pl.col("label_status") == "possibly_in_label").then(pl.lit("possible_label_synonym")).otherwise(None).alias("caution"),
        pl.concat_str([pl.col("ingredient_name").str.to_titlecase(), pl.lit(" · "), "pt"]).alias("display_name"))
    sig = sig.with_columns(pl.struct(["signal_key", "a_drug_reaction", "prr", "label_check", "window", "n_reference_labels", "ai_labels_checked"])
                           .map_elements(lambda s: hashlib.sha256(repr(sorted(s.items())).encode()).hexdigest()[:16], return_dtype=pl.Utf8)
                           .alias("evaluation_id"))
    sig = sig.sort(["is_ranked", "chi2_yates"], descending=[True, True]).with_columns(
        pl.int_range(1, pl.len() + 1).over(["ingredient_rxcui", "is_ranked"]).alias("rank_in_bucket"))
    signals_out.write_table(sig.select("signal_key", "display_name", "ingredient_rxcui", "ingredient_name", "pt", "bucket", "is_ranked",
                                       "rank_in_bucket", "caution", "a_drug_reaction", "a_mass_reports", "mass_report_share", "n_drug_cases", "prr", "prr_ci_low", "prr_ci_high", "chi2_yates",
                                       "label_status", "n_reference_labels", "ai_labels_checked", "window", "rule", "label_check",
                                       "evaluation_id", "stat_key"))
