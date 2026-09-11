# DRY RUN — rehearse 2–5 days before Sep 17

Do this on the **target** delivery workspace(s), not just fevm. It is the first place Mode B
gets a real `CREATE CATALOG` test, because our fevm identity can't create catalogs.

## 1. Stand up the data

- **Mode A (fevm):** run the SETUP.md verify block — confirm the 5 gold tables read, the HPI
  series is 10,455 rows, and the concentration headline shows Midwest Savings Bank ~24.3%.
- **Mode B (Free Edition / demo workspace):** run `00_LOAD_DATA` **in a fresh catalog** end to
  end — create catalog → upload the 6 `data/*.csv.gz` → Run All → confirm the printed verify
  shows ~24.3% and the expected row counts (40 / 24 / 36 / 60 / 51 / 10455). This proves the
  zip is truly self-contained. Then `DROP CATALOG <name> CASCADE;` and (optionally) re-run once
  more to confirm it stands up clean from scratch.

## 2. Walk the 5 notebooks as an attendee

Import them, set `CATALOG`, and actually run each module — don't just skim:

- **01** — open the Catalog UI, check a Lineage tab renders.
- **02** — run each ▼ Reference cell; confirm the numbers match ANSWER_KEY.md
  (24.3% / 62% top-5 / M1011 106.6% / Xtra 5.71% vs 35 3.21% / HPI 58.8→569.4).
- **03** — **actually create a Genie space**, add the 4 tables, ask the 4 questions, add an
  instruction + a trusted question, and confirm curation makes Q2 return ~24.3%. Time this
  module specifically — it's the day's swing factor.
- **04** — **actually build a dashboard**: bar + KPI counters + HPI line; confirm the
  collateral tiles read 1 undercollateralized / 7 stale.

## 3. Time it and note overruns

Record real per-module minutes against RUNBOOK.md. If module 03 runs long, plan to demo the
create-space steps from the front and let the room do the ask + curate loop.

## 4. Confirm entitlements on real attendee accounts

Have one non-admin test account: attach to serverless, open Genie, create a dashboard, and
read the gold tables. Fix any missing Databricks SQL entitlement or grant **before** the day —
entitlement gaps are the classic Session-3 time sink.

## 5. Demo dry run (Sessions 1/4/5)

Click through each demo script end to end on the actual workspace: the Governance Console app
(S1), the Genie One questions (S5), and the Lakebase/GraphQL talk track + diagram (S4). Confirm
any app URLs load and the Genie spaces you'll show are reachable.
