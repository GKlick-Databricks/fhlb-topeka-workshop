# TROUBLESHOOTING — symptoms → fixes

Hard-won traps (from workshop-builder's GOTCHAS.md + this build), mapped to what the room
will actually see.

## Mode B setup

- **`CREATE CATALOG` fails / "PERMISSION_DENIED".** The runner isn't a workspace/metastore admin
  (**our fevm identity is denied `CREATE CATALOG`**). Two options: (a) run Mode B on a **target**
  workspace where you *are* admin, or (b) **point the loader at an existing catalog you can write
  to** — set the `catalog` widget at the top of `00_LOAD_DATA` to that catalog (you need
  `CREATE SCHEMA` on it). The loader now catches the failed create and **reuses the existing
  catalog automatically**. Not a bug in the loader.
- **Loaded columns are all null / wrong types after editing the loader.** The shipped CSVs have
  their columns in **alphabetical** order (that's how the export tool emits them). `00_LOAD_DATA`
  therefore reads every column as string and **casts BY NAME**, never by position. If someone
  "optimizes" it to `spark.read.schema(<positional DDL>).csv(...)`, Spark maps by position and
  silently mistypes everything. Keep the by-name `selectExpr` cast.
- **A table loads 0 rows.** The `data/*.csv.gz` file wasn't uploaded to the volume, or went to
  the wrong path. Re-check `/Volumes/<CATALOG>/fhlb_gold/workshop_files` has all 6 files.

## Genie (module 03)

- **Genie's answer doesn't match the SQL.** Expected before curation — **trust the SQL and
  curate the space**: add a general instruction (advances = outstanding par; concentration =
  `share_of_advance_book`; undercollateralized = `collateral_utilization_pct > 1.0`) and save a
  trusted question (the top-5 concentration query). Re-ask; Q2 should settle on ~24.3%. The gap
  *is* the teaching moment.
- **Two attendees' spaces collide / can't tell them apart.** Everyone must name their space
  `firstname-lastname FHLB Advances`. Same for dashboards (`firstname-lastname FHLB Monitor`).
- **A viewer sees no data in a shared space.** Genie respects UC grants — they need
  `SELECT` on `fhlb_gold`. Apply the ATTENDEE_REQUIREMENTS grant block.

## SQL / data interpretation

- **HPI trend looks flat/0% at the end.** The latest period (2026 Q1) is a **partial period**,
  and `gold.housing_market_reference` is only that snapshot (its `hpi_yoy_pct` = 0.0 by
  construction). Trend on **complete years** from `silver.fhfa_hpi` (module 02, Beat 4). Never
  chart the gold snapshot as a time series.
- **"The #1 riskiest member" flips depending on the question.** Concentration (Midwest Savings
  Bank, 24.3%) and undercollateralization (M1011, 106.6%) are **different lenses** — pick the
  metric deliberately and keep prose, queries, and Genie instructions consistent.
- **`TypeError: unsupported operand 'decimal.Decimal' and 'float'`** in a Python cell. Spark
  `ROUND(...)` returns a `Decimal`; wrap it as `float(x)` before comparing to a float literal.

## Dashboard (module 04)

- **A visualization won't render.** Run its **dataset query standalone** in the SQL editor
  first — a viz is only ever as good as its dataset query.
- **A map chokes or looks wrong.** Aggregate to **one point per state** (the module-04 state
  rollup), not one per member/row.

## Compute / access (any module)

- **Can't run a cell / no warehouse.** Attendee needs a **running serverless SQL warehouse** and
  attach-to-serverless; SQL cells need the warehouse, Python cells need serverless notebook compute.
- **Can't open Genie or create a dashboard.** Missing **Databricks SQL** entitlement — fix on the
  account before the day (see DRY_RUN.md step 4).
