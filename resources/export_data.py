"""Export the 6 analyst tables from fevm as gzipped CSV for Mode B (portable).

Runs the CLI query tool per table, converts JSON -> gzipped CSV under ../data/.
Row data never touches the assistant's context — only a summary is printed.
"""
import csv, gzip, io, json, os, subprocess, sys

PROFILE = "fevm"
CAT = "serverless_stable_6fhczt_catalog"
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA, exist_ok=True)

# (fully-qualified source table, output basename) — basename encodes schema.table
TABLES = [
    ("fhlb_gold.member_advance_summary",    "fhlb_gold.member_advance_summary"),
    ("fhlb_gold.portfolio_concentration",   "fhlb_gold.portfolio_concentration"),
    ("fhlb_gold.member_collateral_capacity","fhlb_gold.member_collateral_capacity"),
    ("fhlb_gold.mpf_portfolio_summary",     "fhlb_gold.mpf_portfolio_summary"),
    ("fhlb_gold.housing_market_reference",  "fhlb_gold.housing_market_reference"),
    ("fhlb_silver.fhfa_hpi",                "fhlb_silver.fhfa_hpi"),
]

for src, base in TABLES:
    out = subprocess.run(
        ["databricks", "experimental", "aitools", "tools", "query",
         f"SELECT * FROM {CAT}.{src}", "--profile", PROFILE],
        capture_output=True, text=True)
    rows = json.loads(out.stdout)
    if not rows:
        print(f"WARN {src}: 0 rows"); continue
    cols = list(rows[0].keys())
    path = os.path.join(DATA, base + ".csv.gz")
    with gzip.open(path, "wt", newline="") as gz:
        w = csv.DictWriter(gz, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {base}.csv.gz  ·  {len(rows)} rows  ·  {os.path.getsize(path)//1024 or 1} KB  ·  cols: {len(cols)}")

print("\nData export complete.")
