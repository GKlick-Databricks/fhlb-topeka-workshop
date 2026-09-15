# SETUP — one-time, per delivery mode

Prereqs (both modes): a UC-enabled workspace; a **running serverless SQL warehouse**
(Medium + autoscale for ~15–40 attendees); serverless enabled for notebooks; the attendee
group has **Databricks SQL** entitlement (Genie + dashboards). See ATTENDEE_REQUIREMENTS.md.

---

## Mode A — live in our workspace (data already built)

Workspace `fevm-serverless-stable-6fhczt`, catalog `serverless_stable_6fhczt_catalog`,
schemas `fhlb_gold` / `fhlb_silver`. **No load step** — the data is already there. Do:

1. **Verify the 5 analyst gold tables + the HPI series exist and read.** Run in the SQL editor:
   ```sql
   SHOW TABLES IN serverless_stable_6fhczt_catalog.fhlb_gold;
   SELECT member_name, ROUND(share_of_advance_book*100,1) pct
   FROM serverless_stable_6fhczt_catalog.fhlb_gold.portfolio_concentration
   ORDER BY share_of_advance_book DESC LIMIT 3;   -- expect Midwest Savings Bank ~24.3
   SELECT COUNT(*) FROM serverless_stable_6fhczt_catalog.fhlb_silver.fhfa_hpi;  -- expect 10455
   ```
2. **Grant the attendee group read** (see the GRANT block in ATTENDEE_REQUIREMENTS.md).
3. **Confirm a serverless SQL warehouse is running** and attendees can attach to it.
4. Leave the `catalog` widget at its default `serverless_stable_6fhczt_catalog` in every notebook (Mode A).

> Note: this identity is **denied `CREATE CATALOG`** in fevm — fine for Mode A (nothing is created).
> For Mode B, either run on a target workspace where you're admin, or point the loader's `catalog`
> widget at an existing catalog you can write to (it reuses it instead of creating one).

---

## Mode B — portable zip (Free Edition or a demo workspace)

Stands the whole thing up with no access to fevm. The runner needs **`CREATE CATALOG`** on the target
workspace (workspace/metastore admin) **or** write access to an existing catalog they set in the
loader's `catalog` widget (`CREATE SCHEMA` on it) — the reason Mode B isn't created in fevm under our
identity.

1. **Import** the workshop zip into the target workspace (Workspace → Import → the .zip).
2. Open **`00_LOAD_DATA`**, set `CATALOG` (default `fhlb_workshop`) and `GRANT_TO` (the attendee
   group), and run the first cell — it creates the catalog, `fhlb_gold` / `fhlb_silver` schemas,
   and an upload volume, then prints the volume path.
3. **Upload the 6 files** from the zip's `data/` folder into that volume
   (`/Volumes/<CATALOG>/fhlb_gold/workshop_files`).
4. **Run All** the rest of `00_LOAD_DATA`. It loads each table (casting **by column name** —
   the shipped CSVs are alphabetical, so never switch it to a positional schema), applies grants,
   and prints a verify block.
5. **Verify** the printed headline shows **Midwest Savings Bank ~24.3%**. Expected row counts:
   member_advance_summary 40, portfolio_concentration 24, member_collateral_capacity 36,
   mpf_portfolio_summary 60, housing_market_reference 51, fhfa_hpi 10455.
6. Tell attendees to set the `catalog` widget to `<your value>` at the top of each notebook.

**Teardown:** `DROP CATALOG <CATALOG> CASCADE;`

The Mode B CSV round-trip (read + cast-by-name → the 24.3% headline, boolean/date casts, the
full 10,455-row HPI, and the M1011 106.6% flag) was verified end-to-end during the build.
