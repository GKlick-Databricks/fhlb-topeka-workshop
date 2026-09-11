# DATA DICTIONARY — FHLB-Topeka Analyst Enablement workshop

All figures validated live against the source workspace (`fevm-serverless-stable-6fhczt`,
catalog `serverless_stable_6fhczt_catalog`) and re-verified end-to-end through the Mode B
shipped CSVs. **Everything here is illustrative — not FHLB-Topeka production data.**

## Real vs. synthetic split

| Source | Rows | Share | What it is |
|---|---|---|---|
| FHFA House Price Index (HPI) | 10,455 | | Real public regulatory data |
| FHFA FHLBank member acquisitions (PUDB) | 46,981 | | Real public regulatory data |
| Federal Reserve DFAST stress paths | 26 | | Real public regulatory data |
| **Real regulatory subtotal** | **57,462** | **~92%** | Market/regulatory context |
| Synthetic members | 80 | | Stand-in core-banking book |
| Synthetic advances | 194 | | Stand-in core-banking book |
| Synthetic collateral | 458 | | Stand-in core-banking book |
| Synthetic MPF loans | 4,000 | | Stand-in core-banking book |
| **Synthetic book subtotal** | **4,732** | **~8%** | The "bank's book" |

The synthetic rows are the Bank's *book* (members / advances / collateral / MPF); the real
rows are the *market and regulatory context* around it.

## The 6 tables the analyst uses (shipped in Mode B)

Attendees are **read-only** on all of these.

### `fhlb_gold.member_advance_summary` — 40 rows (37 active)
Per-member outstanding advances, rate, and maturity.

| Column | Type | Notes |
|---|---|---|
| member_id | string | e.g. `M1011` |
| member_name | string | e.g. `Midwest Savings Bank` |
| charter_type | string | e.g. `commercial bank`, `cdfi` |
| state | string | 2-letter |
| is_active | boolean | 37 of 40 rows are active |
| advance_count | bigint | number of advances |
| total_outstanding_par | decimal(28,2) | outstanding par, USD |
| weighted_avg_rate | decimal(38,6) | e.g. `0.045391` = 4.54% |
| par_maturing_90d | decimal(28,2) | par rolling off in 90 days |
| next_maturity_date | date | |
| as_of_date | date | snapshot date |

### `fhlb_gold.portfolio_concentration` — 24 rows
Each member's share of the total advance book (the concentration story).

| Column | Type | Notes |
|---|---|---|
| member_id | string | |
| member_name | string | |
| state | string | |
| total_outstanding_par | decimal(28,2) | |
| share_of_advance_book | decimal(35,6) | ratio; `0.243` = 24.3% |
| as_of_date | date | |

### `fhlb_gold.member_collateral_capacity` — 36 rows
Lendable value, utilization, and undercollateralization.

| Column | Type | Notes |
|---|---|---|
| member_id | string | |
| position_count | bigint | collateral positions |
| total_market_value | decimal(28,2) | |
| total_lendable_value | double | after haircuts |
| stale_market_value | decimal(28,2) | **> 0 flags a stale valuation** (7 members) |
| total_outstanding_par | decimal(28,2) | |
| excess_capacity | double | lendable − advances |
| collateral_utilization_pct | double | **ratio; 1.0 = 100%.** > 1.0 = undercollateralized |
| is_undercollateralized | boolean | true for M1011 |
| as_of_date | date | |

### `fhlb_gold.mpf_portfolio_summary` — 60 rows (member × product)
MPF loan delinquency, credit, and LTV by member and product.

| Column | Type | Notes |
|---|---|---|
| member_id | string | |
| mpf_product | string | `Original`, `Xtra`, `Direct`, `Government`, `35` |
| loan_count | bigint | |
| total_current_balance | decimal(28,2) | |
| weighted_avg_rate | decimal(38,6) | |
| avg_ltv | decimal(10,4) | ratio; ~0.70 |
| avg_credit_score | int | FICO |
| delinquent_loan_count | bigint | |
| delinquency_rate | double | ratio; `0.0476` = 4.76% |
| serious_delinquency_rate | double | ratio; `0.0088` = 0.88% |
| as_of_date | date | |

### `fhlb_gold.housing_market_reference` — 51 rows (states + DC)
**Point-in-time HPI snapshot (2026 Q1).** Use for a state cross-section, **not** a trend.

| Column | Type | Notes |
|---|---|---|
| state | string | |
| year | int | 2026 |
| quarter | int | 1 |
| hpi_index | decimal(9,4) | |
| hpi_yoy_pct | decimal(15,4) | **reads 0.0 here — see partial-period note** |
| is_declining | boolean | |

### `fhlb_silver.fhfa_hpi` — 10,455 rows (1975–2026)
**The HPI time series.** Use this for trends over time.

| Column | Type | Notes |
|---|---|---|
| state | string | |
| year | int | 1975–2026 |
| quarter | int | 1–4 |
| hpi_index | decimal(9,4) | |
| hpi_yoy_pct | decimal(15,4) | |

## Validated headline numbers

- **Advance book: $1.38B** ($1,381,768,447.27) across **37 active members**.
- **Concentration:** Midwest Savings Bank (NE) **24.3%** ($335.2M); Prairie Bank (OK) 13.1%
  ($181.5M); Commerce National Bank (CO) 9.5%; Golden Plains State Bank (OK) 7.6%; Peoples
  Bank & Trust (NE) 7.5%. **Top-5 = 62.0%.**
- **Collateral:** avg utilization ~30%; **M1011 undercollateralized at 106.6%** (next is
  M1033 at 83.2%); **7 members carry a stale valuation** (`stale_market_value > 0`).
- **MPF:** overall **4.76% delinquency** (0.88% serious), avg **FICO 719**, avg **LTV ~70%**.
  By product: **Xtra 5.71%** (highest), Government 5.66%, Original 5.05%, Direct 4.15%,
  **MPF 35 3.21%** (lowest).
- **HPI district (CO/KS/NE/OK):** avg index **58.8 (1975) → 569.4 (2026)**; dip through the
  2008 crisis (262.5 in 2007 → 252.1 in 2011), steep climb 2020–2023 (382.2 → 521.5).

## Working with real data — read before you present a number

- **HPI point-in-time vs. time series.** `gold.housing_market_reference` is a *snapshot* of
  2026 Q1. Its `hpi_yoy_pct` reads **0.0** because there is no prior quarter in that table to
  difference against — **not** because prices are flat. Any *trend* must come from
  `silver.fhfa_hpi`, which holds the full 1975–2026 series.
- **Partial periods.** The newest period is under-reported and will read flat / 0% YoY.
  Trend on **complete years** and label the latest point, or a chart cliffs misleadingly.
- **Stale collateral valuations are themselves a risk.** `stale_market_value > 0` on 7
  members means you may be measuring capacity against an out-of-date mark — call it out
  rather than smoothing it away.
- **Averages hide the members that matter.** Collateral averages ~30% (healthy) while one
  member sits at 106.6%. Always show the tail, not just the mean.
