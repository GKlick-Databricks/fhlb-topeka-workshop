# Databricks notebook source
# ============================================================================
#  00_LOAD_DATA — PORTABLE-MODE SETUP (admin runs ONCE)   ·  FHLB-Topeka workshop
# ============================================================================
# Stands the Session 3 hands-on up in ANY Databricks workspace (incl. Free Edition)
# with no outside access. Ships the 6 analyst tables as gzipped CSV in ../data/.
#
#   1. create catalog + fhlb_gold / fhlb_silver schemas + an upload volume
#   2. upload the 6 files from the zip's data/ folder into the volume
#   3. Run All: loads each table with its exact schema, then grants read access
#
# ONE knob: CATALOG. Set it, then set the SAME value in each notebook's CONFIG cell.
# See resources/GOTCHAS.md (from workshop-builder) for the CSV-casting rationale:
# we read with an explicit schema so decimals/dates survive the CSV round-trip.

# COMMAND ----------

# ---- CONFIG ----
CATALOG = "fhlb_workshop"     # <-- your workshop catalog (must match the notebooks' CONFIG)
GRANT_TO = "`account users`"  # <-- group that gets read access (or an individual user)
VOLUME_PATH = f"/Volumes/{CATALOG}/fhlb_gold/workshop_files"   # upload the .csv.gz here

# COMMAND ----------

# ---- 1. catalog + schemas + volume ----
spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
for s in ["fhlb_gold", "fhlb_silver"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{s}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.fhlb_gold.workshop_files")
print(f"👉 Upload the 6 files from the zip's data/ folder into:\n   {VOLUME_PATH}\n   then continue.")
# display(dbutils.fs.ls(VOLUME_PATH))

# COMMAND ----------

# ---- 2. load each shipped CSV, casting BY COLUMN NAME (order-independent) ----
# The shipped CSVs have header names but their column ORDER is alphabetical, so we read
# every column as string (header-keyed) and CAST by name — never by position. Casting
# from string handles decimals, ISO dates, true/false, and scientific-notation doubles.
# base (schema.table) -> {column: target_type}, captured from the source tables.
TABLES = {
  "fhlb_gold.member_advance_summary": {
    "member_id": "string", "member_name": "string", "charter_type": "string",
    "state": "string", "is_active": "boolean", "advance_count": "bigint",
    "total_outstanding_par": "decimal(28,2)", "weighted_avg_rate": "decimal(38,6)",
    "par_maturing_90d": "decimal(28,2)", "next_maturity_date": "date", "as_of_date": "date"},
  "fhlb_gold.portfolio_concentration": {
    "member_id": "string", "member_name": "string", "state": "string",
    "total_outstanding_par": "decimal(28,2)", "share_of_advance_book": "decimal(35,6)",
    "as_of_date": "date"},
  "fhlb_gold.member_collateral_capacity": {
    "member_id": "string", "position_count": "bigint", "total_market_value": "decimal(28,2)",
    "total_lendable_value": "double", "stale_market_value": "decimal(28,2)",
    "total_outstanding_par": "decimal(28,2)", "excess_capacity": "double",
    "collateral_utilization_pct": "double", "is_undercollateralized": "boolean",
    "as_of_date": "date"},
  "fhlb_gold.mpf_portfolio_summary": {
    "member_id": "string", "mpf_product": "string", "loan_count": "bigint",
    "total_current_balance": "decimal(28,2)", "weighted_avg_rate": "decimal(38,6)",
    "avg_ltv": "decimal(10,4)", "avg_credit_score": "int", "delinquent_loan_count": "bigint",
    "delinquency_rate": "double", "serious_delinquency_rate": "double", "as_of_date": "date"},
  "fhlb_gold.housing_market_reference": {
    "state": "string", "year": "int", "quarter": "int", "hpi_index": "decimal(9,4)",
    "hpi_yoy_pct": "decimal(15,4)", "is_declining": "boolean"},
  "fhlb_silver.fhfa_hpi": {
    "state": "string", "year": "int", "quarter": "int",
    "hpi_index": "decimal(9,4)", "hpi_yoy_pct": "decimal(15,4)"},
}

for base, coltypes in TABLES.items():
    fqn = f"{CATALOG}.{base}"
    src = f"{VOLUME_PATH}/{base}.csv.gz"
    raw = spark.read.option("header", True).csv(src)   # all columns read as string
    cast_exprs = [f"CAST(`{c}` AS {t}) AS {c}" for c, t in coltypes.items()]
    raw.selectExpr(*cast_exprs).write.mode("overwrite").saveAsTable(fqn)
    print(f"loaded {fqn}: {spark.table(fqn).count()} rows")

# COMMAND ----------

# ---- 3. grants so analysts can READ the governed gold/silver data products ----
spark.sql(f"GRANT USE CATALOG ON CATALOG {CATALOG} TO {GRANT_TO}")
for s in ["fhlb_gold", "fhlb_silver"]:
    spark.sql(f"GRANT USE SCHEMA, SELECT ON SCHEMA {CATALOG}.{s} TO {GRANT_TO}")
print("✓ Setup complete. Attendees set CATALOG =", repr(CATALOG),
      "in each notebook's CONFIG cell and start at 00_WORKSHOP_GUIDE.")

# COMMAND ----------

# ---- Verify: the headline numbers should match the workshop story ----
display(spark.sql(f"""
  SELECT member_name, ROUND(share_of_advance_book*100,1) AS pct_of_book
  FROM {CATALOG}.fhlb_gold.portfolio_concentration
  ORDER BY share_of_advance_book DESC LIMIT 3
"""))
# Expected: Midwest Savings Bank ~24.3%  (top-5 sum to ~62%)

# COMMAND ----------

# Teardown after the workshop:  DROP CATALOG fhlb_workshop CASCADE;
