# Curated (gold): datasets that back the first Ontology path (step 6): Drug, Product, Label, Recall, their link (join) datasets,
# and an empty TriageDecision dataset for the Action save test.
# Contract: docs/04-architecture/dataset-contracts-v1.md §3 and conventions §5. Rules: one row per object, key never null;
# many-to-many links as join datasets (no multiplied objects); one reference label per product (D039 G3, LD1);
# recall links only for package/product matches with high or medium confidence (low = ingredient name in text, kept as Drug link).
#
# Mirror of Foundry repo Pipelines/pipelines_clean,
#   transforms-python/src/myproject/datasets/ontology_objects.py
import polars as pl
from transforms.api import Input, Output, transform

CLEAN = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/clean/"
CURATED = "/kestrel-01f4ab/Medication Safety Signal Monitor/Data/curated/"
DAILYMED = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid="


def label_key(setid, version):
    # Composite key in fixed order: setid, then version (D039 contracts: "setid + version").
    return pl.concat_str([setid, pl.lit("|v"), version.cast(pl.Utf8)])


def reference_labels(label_map):
    # Owner (reference) label per product: the newest owner label; how many owner labels there were is kept for review.
    ref = label_map.filter(pl.col("is_reference_label")).sort(["effective_time", "setid"])
    return ref.group_by("application_number").agg(
        pl.col("setid").last().alias("reference_setid"), pl.col("spl_version").last().alias("reference_spl_version"),
        pl.len().alias("n_owner_labels")).with_columns(label_key(pl.col("reference_setid"), pl.col("reference_spl_version")).alias("reference_label_key"))


@transform.using(drugs=Output(CURATED + "ontology_drug_drugs"), ingredients=Input(CLEAN + "clean_drug_ingredients"),
                 product_map=Input(CLEAN + "clean_drug_product_map"), recall_match=Input(CLEAN + "clean_recall_product_match"),
                 drug_reaction=Input(CLEAN + "clean_faers_drug_reaction"))
def compute_drugs(drugs, ingredients, product_map, recall_match, drug_reaction):
    pm = product_map.polars()
    rm = recall_match.polars().filter(pl.col("match_target") == "ingredient")
    dr = drug_reaction.polars().filter(~pl.col("dup_suppressed"))
    counts = [
        pm.group_by("ingredient_rxcui").agg(pl.len().alias("n_products"), pl.col("any_marketed").sum().cast(pl.Int64).alias("n_marketed_products")),
        rm.group_by("match_key").agg(pl.len().alias("n_recalls"), pl.col("is_active").sum().cast(pl.Int64).alias("n_active_recalls")).rename({"match_key": "ingredient_rxcui"}),
        dr.group_by("ingredient_rxcui").agg(pl.col("caseid").n_unique().alias("n_faers_cases")),
    ]
    out = ingredients.polars().with_columns(pl.col("ingredient_name").str.to_titlecase().alias("display_name"))
    for c in counts:
        out = out.join(c, on="ingredient_rxcui", how="left")
    drugs.write_table(out.with_columns(pl.col(c).fill_null(0) for c in ["n_products", "n_marketed_products", "n_recalls", "n_active_recalls", "n_faers_cases"]))


@transform.using(products=Output(CURATED + "ontology_product_products"), drug_product=Output(CURATED + "ontology_link_drug_product"),
                 product_map=Input(CLEAN + "clean_drug_product_map"), label_map=Input(CLEAN + "clean_label_product_map"))
def compute_products(products, drug_product, product_map, label_map):
    pm = product_map.polars()
    # One Product per application (D039 G2); a combination product appears under each of its formulary ingredients in the map.
    p = pm.sort("ingredient_rxcui").unique("product_key", keep="first").drop(["ingredient_rxcui", "products_json"])
    p = p.join(reference_labels(label_map.polars()), left_on="product_key", right_on="application_number", how="left").with_columns(
        pl.col("reference_label_key").is_not_null().alias("has_reference_label"), pl.col("n_owner_labels").fill_null(0),
        pl.concat_str([pl.col("brand_names").fill_null(pl.col("product_key")), pl.lit(" ("), pl.col("product_key"), pl.lit(")")]).alias("display_name"))
    products.write_table(p)
    drug_product.write_table(pm.select("ingredient_rxcui", "product_key").unique().with_columns(
        pl.concat_str(["ingredient_rxcui", pl.lit("|"), "product_key"]).alias("link_key")))


@transform.using(labels=Output(CURATED + "ontology_label_labels"), product_label=Output(CURATED + "ontology_link_product_label"),
                 versions=Input(CLEAN + "clean_label_versions"), sections=Input(CLEAN + "clean_label_sections"),
                 label_map=Input(CLEAN + "clean_label_product_map"), product_map=Input(CLEAN + "clean_drug_product_map"))
def compute_labels(labels, product_label, versions, sections, label_map, product_map):
    secs = sections.polars().group_by(["setid", "spl_version"]).agg(pl.len().alias("n_safety_sections"),
                                                                     pl.col("section_name").sort().str.join(", ").alias("safety_sections"))
    lv = versions.polars().join(secs, on=["setid", "spl_version"], how="left").with_columns(
        label_key(pl.col("setid"), pl.col("spl_version")).alias("label_key"), (pl.lit(DAILYMED) + pl.col("setid")).alias("dailymed_url"),
        pl.concat_str([pl.col("title"), pl.lit(" · v"), pl.col("spl_version").cast(pl.Utf8)]).alias("display_name"))
    labels.write_table(lv)
    keys = set(product_map.polars()["product_key"].to_list())
    lm = label_map.polars().filter(pl.col("application_number").is_in(list(keys))).with_columns(
        label_key(pl.col("setid"), pl.col("spl_version")).alias("label_key"))
    product_label.write_table(lm.select(pl.col("application_number").alias("product_key"), "label_key", "is_reference_label", "owner_match", "match_status")
                              .unique(["product_key", "label_key"]).with_columns(pl.concat_str(["product_key", pl.lit("|"), "label_key"]).alias("link_key")))


@transform.using(recalls=Output(CURATED + "ontology_recall_recalls"), recall_product=Output(CURATED + "ontology_link_recall_product"),
                 recall_drug=Output(CURATED + "ontology_link_recall_drug"), current=Input(CLEAN + "clean_recalls_current"),
                 match=Input(CLEAN + "clean_recall_product_match"))
def compute_recalls(recalls, recall_product, recall_drug, current, match):
    m = match.polars()
    linked = m.filter(pl.col("product_key").is_not_null() & pl.col("confidence").is_in(["high", "medium"]))
    best = linked.with_columns(pl.col("confidence").replace({"high": "1", "medium": "2"}).alias("rank")).sort("rank").unique(
        ["recall_number", "product_key"], keep="first").drop("rank")
    r = current.polars().join(linked.group_by("recall_number").agg(pl.col("product_key").n_unique().alias("n_matched_products")), on="recall_number", how="left")
    r = r.with_columns(pl.col("n_matched_products").fill_null(0), pl.concat_str([pl.col("recall_number"), pl.lit(" · "), pl.col("classification"),
                       pl.lit(" · "), pl.col("status")]).alias("display_name"))
    recalls.write_table(r)
    recall_product.write_table(best.select("recall_number", "product_key", "match_method", "confidence", "ndc_as_printed").with_columns(
        pl.concat_str(["recall_number", pl.lit("|"), "product_key"]).alias("link_key")))
    recall_drug.write_table(m.filter(pl.col("match_target") == "ingredient").select("recall_number", pl.col("match_key").alias("ingredient_rxcui"), "match_method", "confidence")
                            .with_columns(pl.concat_str(["recall_number", pl.lit("|"), "ingredient_rxcui"]).alias("link_key")))


@transform.using(decisions=Output(CURATED + "ontology_triage_decisions"))
def compute_triage_seed(decisions):
    # Empty on purpose: TriageDecision objects are created only by the Action (write-back). This dataset gives the object type its schema.
    schema = {"decision_id": pl.Utf8, "subject_type": pl.Utf8, "subject_key": pl.Utf8, "evaluation_id": pl.Utf8, "decision": pl.Utf8,
              "rationale": pl.Utf8, "reviewer": pl.Utf8, "decided_at": pl.Datetime("us", "UTC")}
    decisions.write_table(pl.DataFrame(schema=schema))
