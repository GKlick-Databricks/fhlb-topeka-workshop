# ANSWER KEY — Session 3 hands-on (the 5 notebooks)

Every answer is grounded in live-validated numbers. Where a different metric cut changes
the ranking, it's flagged. Notebook cells labeled "▼ Reference answer" are runnable as-is.

## 01 · Explore the governed gold data products

- **"How many columns does an advance summary need?"** (predict-then-check) — 11:
  member_id, member_name, charter_type, state, is_active, advance_count,
  total_outstanding_par, weighted_avg_rate, par_maturing_90d, next_maturity_date, as_of_date.
- **"Which table answers *which members are undercollateralized?*"** →
  `fhlb_gold.member_collateral_capacity` (column `is_undercollateralized` / `collateral_utilization_pct`).
- **Lineage of `member_collateral_capacity`** → built from the silver collateral +
  advances tables (show the Lineage tab). Point out lineage = provenance for every number.

## 02 · SQL story beats

**Beat 1 — Concentration** (`ORDER BY total_outstanding_par DESC LIMIT 5` on
`portfolio_concentration`):

| member_name | state | outstanding_$m | pct_of_book |
|---|---|---|---|
| Midwest Savings Bank | NE | 335.2 | 24.3 |
| Prairie Bank | OK | 181.5 | 13.1 |
| Commerce National Bank | CO | 131.3 | 9.5 |
| Golden Plains State Bank | OK | 105.1 | 7.6 |
| Peoples Bank & Trust | NE | 103.5 | 7.5 |

Total book **$1.38B**; **top-5 = 62.0%**; top member **24.3%**.

**Beat 2 — Collateral** (`ORDER BY collateral_utilization_pct DESC` on
`member_collateral_capacity`): top row is **M1011 at 106.6%, is_undercollateralized = true**
(advances > lendable value); next is **M1033 at 83.2%** (not flagged). **7 members** show
`valuation_flag = STALE` (`stale_market_value > 0`). Portfolio average utilization ≈ 30%.

**Beat 3 — MPF by product** (`GROUP BY mpf_product`, ordered by delinquency desc):

| mpf_product | delinquency_pct | serious_pct | avg_fico |
|---|---|---|---|
| Xtra | 5.71 (highest) | 0.77 | 717 |
| Government | 5.66 | 0.79 | 719 |
| Original | 5.05 | 1.33 | 714 |
| Direct | 4.15 | 0.80 | 728 |
| 35 | 3.21 (lowest) | 0.72 | 716 |

Overall **4.76%** delinquency, **0.88%** serious, avg **FICO 719**. Point: the headline is
uniform-looking; the **product mix** (Xtra vs 35) is where the risk lives.

**Beat 4 — HPI district trend** (`silver.fhfa_hpi`, states CO/KS/NE/OK, avg by year):
runs **58.8 (1975) → 569.4 (2026)**, with a dip 2007 (262.5) → 2011 (252.1) and a steep
2020 (382.2) → 2023 (521.5) climb. **Do not** use `gold.housing_market_reference` for this —
it's a 2026-Q1 snapshot and its YoY reads 0.0 (partial period).

**Your Turn (join):** the most concentrated member (Midwest Savings Bank) — join
`member_advance_summary` to `member_collateral_capacity` on `member_id`; it is **not** the
undercollateralized one (M1011 is a different, smaller member). Teaching point: concentration
risk and collateral risk are distinct lenses.

**Optional (maturity):** `ORDER BY par_maturing_90d DESC` on `member_advance_summary` — the
top member has the most par rolling off (e.g. Prairie Bank shows ~$77M maturing in 90 days).

## 03 · Create YOUR OWN Genie space

There is no single "right" answer — the point is the build + curation loop. Expected outcomes:

1. *"Which members have the largest outstanding advances?"* → Midwest Savings Bank, Prairie
   Bank, Commerce National Bank … (matches Beat 1).
2. *"What share does the top member hold?"* → **~24.3%** (Midwest Savings Bank). If Genie is
   off before curation, that's the teachable moment.
3. *"Which members are undercollateralized?"* → **M1011** (utilization > 100%).
4. *"MPF delinquency by product?"* → Xtra highest (5.71%), MPF 35 lowest (3.21%).

**Curation checkpoint:** after adding the general instruction (advances = outstanding par;
concentration = share_of_advance_book; undercollateralized = utilization > 1.0) and a trusted
question (the top-5 concentration query), re-asking Q2 should reliably return ~24.3%.
The ground-truth cell (Step 5) returns `Midwest Savings Bank | 24.3`.

**Governance point to land:** a Genie space respects Unity Catalog permissions — a viewer
only sees data they're already entitled to. That is *why* "foundation before broad exposure"
is safe.

## 04 · Build / refine a dashboard

- **Bar chart** (member_name × outstanding_$m, desc) — Midwest Savings Bank's bar towers.
- **KPI counters** — top member share **24.3%**; total book **$1,382M**.
- **Housing line** (avg_hpi × year, from Beat 4) — label the 2026 partial period.
- **Your Turn collateral tiles** — undercollateralized members = **1**; stale valuations = **7**.
- **State rollup** (advances by `state`) — NE and OK lead (Midwest Savings Bank + Peoples
  Bank & Trust are NE; Prairie Bank + Golden Plains are OK).
- **Optional MPF bar** — delinquency_pct by product reproduces the Xtra-vs-35 spread.

Every tile is sourced from the same governed gold tables as the SQL and the Genie space, so
all three **agree by construction** — that's the enablement message.
