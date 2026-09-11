# FHLB-Topeka In-Person Day — Agenda → Assets

**Date:** September 17, 2026 · **Time:** 8:00 AM–5:00 PM
**Databricks team:** Gordon Heil, Brice Giesbrecht, Gabe Klick, Zoeb Zavery

This package maps the in-person-day agenda to concrete, ready-to-run assets. Every demo and
exercise runs on **real FHFA public data + a synthetic FHLB core-banking book** — clearly
illustrative, **not FHLB-Topeka production data**. Every number is validated against the live
gold tables (see `instructor/DATA_DICTIONARY.md`).

| Time | Session | Format | Asset in this package |
|---|---|---|---|
| 8:00–8:15 | Welcome, objectives & introductions | — | — |
| 8:15–9:00 | **S1 · Governance, Security & AI Readiness** | Presenter demo | `demo-scripts/SESSION1_governance_ai_readiness.md` |
| 9:00–10:30 | S2A · Data & Platform Deep Dive — Current State | Discussion | *(facilitation, not built here)* |
| 10:30–10:45 | Break | — | — |
| 10:45–12:15 | S2B · Data & Platform Deep Dive — Target State | Discussion | *(facilitation, not built here)* |
| 12:15–1:15 | Lunch | — | — |
| 1:15–2:30 | **S3 · Analyst Enablement — Dashboards & Genie** | **Hands-on lab** | `notebooks/00–04` (5 notebooks) |
| 2:30–3:45 | **S4 · Lakebase & GraphQL for App Databases** | Presenter demo | `demo-scripts/SESSION4_lakebase_graphql.md` |
| 3:45–4:00 | Break | — | — |
| 4:00–5:00 | **S5 · Business Value, Prioritization & Next Steps** | Demo + working session | `demo-scripts/SESSION5_business_value_genie_one.md` |

## The hands-on lab (Session 3)
Attendees run five notebooks and leave with **their own Genie space and dashboard**:

1. `00_WORKSHOP_GUIDE` — big picture, the data story, the rules.
2. `01_explore_uc` — explore the governed gold data products in Unity Catalog.
3. `02_sql_analysis` — the four story beats in SQL (concentration, collateral, credit, housing).
4. `03_genie_space` — **create your own Genie space and ask in plain English** (the core exercise).
5. `04_dashboard` — build/refine an AI/BI dashboard.

Attendees are **read-only** on the data; the artifacts they build are a Genie space + a
dashboard, each named `firstname-lastname` so a shared workspace stays de-conflicted.

## Two delivery modes (both included)
- **Mode A — live in our workspace** (`fevm-serverless-stable-6fhczt`, catalog
  `serverless_stable_6fhczt_catalog`): the data + apps + Genie spaces already exist. See
  `instructor/SETUP.md`.
- **Mode B — portable**: `notebooks/00_LOAD_DATA.py` stands the lab up in any workspace
  (incl. Free Edition) from the 6 gzipped CSVs in `data/`, driven by one `CATALOG` value.
  **Round-trip verified** — the headline numbers reproduce exactly from the shipped data.

## The validated story (the hook)
- **Advance book $1.38B across 37 active members — and concentrated:** Midwest Savings Bank (NE)
  alone is **24.3% ($335M)**; the top 5 are **~62%**.
- **Collateral averages ~30% utilization (healthy) — but one member (M1011) is at 106.6%
  (undercollateralized), and 7 carry stale valuations.** Averages hide the members that matter.
- **MPF delinquency 4.76% overall — but 5.71% for MPF Xtra vs 3.21% for MPF 35.**
- **District housing (CO/KS/NE/OK) HPI ran 58.8 (1975) → 569.4 (2026)** with a 2008 dip and a
  steep 2020–23 climb.

See `README.md` for how to run it and `instructor/` for setup, runbook, answer key, and more.
