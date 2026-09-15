# ATTENDEE REQUIREMENTS — Session 3 hands-on

Only Session 3 needs attendees at keyboards. Sessions 1/4/5 are watch-along demos.

## Per attendee

- **Workspace access** with the ability to **attach to serverless** (notebooks) and
  **run on a serverless SQL warehouse**.
- **Databricks SQL entitlement** — required to open **Genie** and create **dashboards**.
- **Create a Genie space** and **create a dashboard** (these are personal assets they build).
- **Read access** to the governed data (grant block below).
- **No table-create needed** — attendees are read-only on the data; they never build tables.

## Compute

- A **running serverless SQL warehouse** (Medium, autoscale) sized for the room (~15–40).
- Serverless enabled for notebooks.

## Grant block (run once as admin)

Replace the group and, for Mode B, the catalog name.

```sql
-- Mode A: catalog = serverless_stable_6fhczt_catalog
-- Mode B: catalog = whatever 00_LOAD_DATA created (default fhlb_workshop)
GRANT USE CATALOG ON CATALOG serverless_stable_6fhczt_catalog TO `account users`;
GRANT USE SCHEMA, SELECT ON SCHEMA serverless_stable_6fhczt_catalog.fhlb_gold   TO `account users`;
GRANT USE SCHEMA, SELECT ON SCHEMA serverless_stable_6fhczt_catalog.fhlb_silver TO `account users`;
```

A Genie space and a dashboard both **respect these UC grants** — a viewer only ever sees data
they're already entitled to. That's the governance foundation Session 1 sets up.

## Mode B additional requirement

The person who runs `00_LOAD_DATA` needs **either** `CREATE CATALOG` (workspace / metastore admin)
**or** write access to an **existing** catalog they point the loader at (`CREATE SCHEMA` on it — set
the `catalog` widget). Our fevm identity is denied `CREATE CATALOG`, which is why Mode B runs on a
target (Free Edition / demo) workspace **or** against an existing catalog you can write to.
