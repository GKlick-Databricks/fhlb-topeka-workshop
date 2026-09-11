# GOTCHAS — read before you build

Hard-won lessons from delivering real Databricks workshops. Each one cost time (some cost it *live, in
front of people*). Bake the fixes in from the start.

## Packaging & delivery

- **Zip MUST include directory entries.** Python's `zipfile.write(path, arcname)` writes only file
  entries; Databricks' workspace zip import creates subfolders **only from explicit directory entries**,
  so `resources/`, `07_app/`, `data/` silently vanish on import (top-level notebooks come through, folders
  don't). Fix: also write `z.writestr(zipfile.ZipInfo(dir + "/"), "")` for the root and every subdir — or
  use the `zip -r` CLI. `resources/zip_workshop.py` does this correctly. Verify with `zipinfo -1 file.zip | grep '/$'`.
- **A `.xlsx`/native-sheet distinction bites Google Sheets read/write** (if you stage RFP-style docs):
  uploaded `.xlsx` can't be read/written via the Sheets API — download & parse, or convert to native.
- **Ship data as gzipped CSV for portable mode.** ~350k rows → ~27 MB gz. Over email limits (25 MB) — use
  a Drive/Slack link, not an attachment. The tiny notebook-only participant zip is emailable.

## Isolation & the prefix (the #1 live failure)

- **Two mechanisms for the prefix will drift.** If `03` (the Lakeflow pipeline) takes the prefix from a
  **manually-typed pipeline config** (`spark.conf.get("user_prefix", ...)`) while `04`/`05`/etc. **auto-derive**
  it from `current_user()`, they disagree whenever someone's email local-part ≠ `firstname.lastname`. The
  consumer notebook then looks for a table that doesn't exist → `TABLE_OR_VIEW_NOT_FOUND`.
- **Always add the prefix guard** (in `templates/config_snippets.py`): a manual `USER_PREFIX = ""` override
  at the top, and if the expected table is missing, **list the prefixes that DO exist** and tell the user
  to set theirs — instead of a raw stack trace. This is the difference between a 10-second fix and a stalled room.
- Keeping the manual pipeline-config step can be a deliberate teaching choice (participants see the pipeline
  Settings) — just pair it with the guard.

## Notebook execution traps

- **`spark.catalog.clearCache()` is NOT allowed on serverless** (`NOT_SUPPORTED_WITH_SERVERLESS`). Don't use
  it to force fresh reads; rely on `.count()` triggering a scan.
- **Spark `ROUND(...)` returns a `Decimal`.** `hi = spark.sql("SELECT ROUND(...)").first()[0]` then
  `abs(hi - 63.2)` throws `TypeError: unsupported operand 'decimal.Decimal' and 'float'`. Wrap `float(hi)`.
  Sweep every Python cell that pulls a rounded scalar and compares it to a float.
- **`current_catalog()` may default to `hive_metastore`** on a session even when UC works via fully-qualified
  names. Prefer fully-qualified 3-part names, or run `USE CATALOG <cat>` up front.
- **`<details>` HTML reveals don't render/collapse in Databricks notebooks.** For "try then check", use a
  runnable answer cell labeled clearly, or a commented answer the learner uncomments — not `<details>`.

## Lakeflow / DLT pipeline

- **`@dlt.expect_or_warn` does not exist.** Warn/retain = `@dlt.expect(name, constraint)`; only
  `*_or_drop` / `*_or_fail` take suffixes.
- **Read upstream pipeline tables with `spark.read.table("cat.sch.tbl")`, not `dlt.read(<fqn>)`** (unreliable
  in UC pipelines).
- **Fully-qualified 3-part `@dlt.table(name="cat.schema.table")` publishes across multiple schemas from one
  pipeline** (default publishing mode) — verified working (silver + gold from one pipeline). It also lets
  Lakeflow infer build order from `spark.read.table(...)` references. **Test it by actually running a pipeline**,
  don't assume.
- **`@dlt` cells error if Run on an interactive cluster** ("DLT module not supported"). Add a "read before you
  run" note; provide a plain-SQL `03b` fallback that builds identical tables in ~30s.
- **Pipeline-managed tables vs regular tables collide on the same name.** If you build the 4 tables with the
  pipeline AND with `03b`, whichever runs second errors. Document: pick one path; to switch, delete the pipeline
  (or DROP the regular tables).
- **Dimensions need a UNIQUE key.** If the airport/lookup dim has duplicate keys, the LEFT JOIN fans out the
  fact and inflates every downstream number. Dedup (`QUALIFY row_number() OVER (PARTITION BY key ...) = 1`) — it
  may "work" on a clean sample by luck and break on the customer's real data.

## COPY INTO (portable loader)

- **COPY INTO into a typed table fails to auto-cast CSV strings** → `DELTA_FAILED_TO_MERGE_FIELDS`. Fixes:
  (a) cast in a subquery: `COPY INTO t FROM (SELECT CAST(id AS BIGINT) id, ... FROM '<path>') FILEFORMAT=CSV
  FORMAT_OPTIONS('header'='true')`, or (b) load into a schemaless table with `inferSchema`/`mergeSchema`.
- **COPY INTO is idempotent** — re-running skips already-loaded files (`num_affected_rows: 0`). Good for
  resume-on-failure at high file counts. (Empirically ~63× faster to read a consolidated Delta table than
  hundreds/thousands of small CSVs — the file *count* is the bottleneck, not data volume.)

## Databricks Apps (stretch module 07)

- **Apps run as their own service principal (SP).** Even before OBO, you authorize the SP to the app's
  **resources** (e.g., the SQL warehouse in `app.yaml`) — that's the "on your behalf" prompt you approve as
  owner. It's mandatory and separate from user auth.
- **On-Behalf-Of-User (OBO)** is additive: declare `user_api_scopes`, enable User authorization, and each
  viewer consents on first open. Gotchas: the app env has BOTH the SP creds and the forwarded user token →
  `WorkspaceClient(host, token, auth_type="pat")` to force token-only (else "more than one auth method").
  The user token needs the `sql` scope → redeploy + re-consent, or you get `Invalid scope`.
- **`app.yaml` env overrides the UI on every deploy** — a `WORKSHOP_USER_PREFIX: "changeme"` in app.yaml
  will reset the app to `changeme` and all panels fail. Set it in both places, and guard for `changeme`.
- **App names allow hyphens only** (`jane-doe-...`), unlike table prefixes (underscores).
- **Maps: aggregate to ~one point per entity, not one per row.** A point map with ~300k markers chokes; group
  to airports/sites (size by count, color by severity).

## Content honesty & timing

- **Validate live; the story must be TRUE.** Re-run every ranking query against the real data. Beware
  metric-sensitivity: "most damaging by *any* damage" vs "by *serious* damage" can flip the #1 answer — pick the
  metric deliberately and keep queries, prose, and answer key consistent.
- **Trim partial periods** (e.g., the current year is under-reported → a trend chart cliffs; filter it out with a note).
- **Stated per-module times are optimistic for beginners.** The pipeline module is the big variable; setup/UC
  are the most padded. Give an honest range (buffered vs fast room) and treat stretch modules as the overflow
  that prevents dead air. See `TIMING.md`.
- **After editing a "master", re-sync the "participant" copy and re-diff before zipping** — it's easy to ship a
  stale participant notebook.
