"""Build the FHLB-Topeka Session 3 hands-on notebooks (Analyst Enablement).

Arc (analyst-enablement slice of the workshop-builder method):
  00 guide -> 01 explore governed UC gold tables -> 02 SQL story beats
  -> 03 create YOUR OWN Genie space + ask -> 04 build/refine a dashboard

Attendees do NOT build the medallion pipeline (it already exists in fevm); the
"your own" artifacts here are a Genie space and a dashboard, each named
firstname-lastname so a shared workspace stays de-conflicted.

Run:  python3 build_notebooks.py            # writes ../notebooks/*.ipynb
Every number in prose/answers is grounded in live gold tables (see DATA_DICTIONARY).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nb import md, code, sql, write_nb

NB_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")

# --- the ONE knob: repoints Mode A (live fevm) <-> Mode B (portable) ---
CONFIG = '''# ============================================================
#  WORKSHOP CONFIG  —  the only cell you may need to edit
# ============================================================
# Mode A (live, our workspace):  serverless_stable_6fhczt_catalog
# Mode B (portable / Free Edition): set CATALOG to the catalog 00_LOAD_DATA created
CATALOG = "serverless_stable_6fhczt_catalog"

GOLD   = f"{CATALOG}.fhlb_gold"     # governed, analyst-ready data products (read-only)
SILVER = f"{CATALOG}.fhlb_silver"   # cleaned/typed layer (we use the HPI time series here)

spark.sql(f"USE CATALOG {CATALOG}")
print(f"Catalog: {CATALOG}  ·  gold: {GOLD}")
'''

VERIFY = '''# ---- Verify you can read the governed gold data products ----
# You are an ANALYST here: you READ curated gold tables and build your own Genie
# space + dashboard. You do not create or drop tables. If a table is missing, tell
# your facilitator (Mode B: the 00_LOAD_DATA loader may not have finished).
expected = ["member_advance_summary", "portfolio_concentration",
            "member_collateral_capacity", "mpf_portfolio_summary",
            "housing_market_reference"]
present = {r.tableName for r in spark.sql(f"SHOW TABLES IN {GOLD}").collect()}
missing = [t for t in expected if t not in present]
if missing:
    print("⚠️  Missing gold tables:", missing)
    print("    Present:", sorted(present))
    print("    Mode A: check CATALOG in the config cell. Mode B: re-run 00_LOAD_DATA.")
else:
    print("✓ All 5 analyst gold tables are readable. You're good to go.")
'''


def guide():
    cells = [
        md('''# 00 · FHLB-Topeka Analyst Enablement — Workshop Guide
**Session 3 · Dashboards & Genie Spaces · ~75 min · hands-on**

🧠 **The big picture.** You already have a governed lakehouse: raw regulatory + book
data flows Bronze → Silver → **Gold**, and the gold layer is a set of *analyst-ready
data products*. Today you don't build pipelines — you **put those data products to
work**: explore them in Unity Catalog, ask them questions in SQL, spin up **your own
Genie space** to ask in plain English, and assemble a dashboard. This is the exact
path from "governed data" to "an analyst answering a business question in minutes."

🏢 **Why FHLB-Topeka cares.** Advances, collateral, MPF, and housing-market context are
the questions the Bank lives on: *who concentrates our advance book, who is
undercollateralized, how is district housing holding up.* If an analyst can answer
those from governed gold — with lineage, classification, and audit already in place —
that's the enablement win this day is about.'''),
        md('''## The data you'll use (all real, all validated today)

Roughly **92% of the raw data is real public regulatory data** (FHFA House Price Index,
FHFA FHLBank member acquisitions / PUDB, Federal Reserve DFAST stress paths); the
remaining **~8% is a synthetic core-banking book** (members, advances, collateral, MPF
loans) standing in for FHLB-Topeka's own systems. Everything is illustrative — **not
FHLB-Topeka production data.**

The 5 gold **data products** you'll query:

| Table (`fhlb_gold.*`) | One-liner |
|---|---|
| `member_advance_summary` | Per-member outstanding advances, rate, maturity |
| `portfolio_concentration` | Each member's share of the total advance book |
| `member_collateral_capacity` | Lendable value, utilization, undercollateralization |
| `mpf_portfolio_summary` | MPF loan delinquency, FICO, LTV by member & product |
| `housing_market_reference` | Point-in-time HPI snapshot by state |

Plus `fhlb_silver.fhfa_hpi` for the **HPI time series** (trends over time).'''),
        md('''## 👀 What's in today's data — the story (validated live)

- **The advance book is $1.38B across 37 active members — and it's concentrated.**
  **Midwest Savings Bank (NE) alone is 24.3% ($335M)** of the entire book; the **top 5
  members are ~62%.** Concentration is the headline risk you can see immediately.
- **Collateral looks healthy on average (~30% utilization) — but one member (M1011) is
  undercollateralized at 106.6%**, and **7 members carry stale collateral valuations.**
  Averages hide the members that matter.
- **MPF delinquency is 4.76% overall (0.88% serious), avg FICO 719 — but it varies by
  product: MPF Xtra runs 5.71%, MPF 35 only 3.21%.**
- **District housing (CO/KS/NE/OK) HPI ran 58.8 (1975) → 569.4 (2026)** — with a visible
  dip through the 2008 crisis and a steep 2020–2023 climb.

Keep these in mind — you'll rediscover each one yourself.'''),
        md('''## The three rules (shared workspace)
1. **You are read-only on the data.** Explore and query gold; don't create or drop tables.
2. **Name your own objects `firstname-lastname`** — your Genie space and your dashboard.
   That keeps 20+ people from colliding in one workspace.
3. **It's all illustrative.** Never present these numbers as FHLB-Topeka production figures.

## Using Genie (read this once)
- **Data questions go to a full-screen Genie space** you open in its own browser tab.
  It answers from the governed tables you add as assets, and it's a real, curated asset
  you can keep and share — that's what you'll build in module 03.
- The in-notebook ✨ assistant is for **writing code** (it reads your cells) — a different
  thing. When we say "ask Genie," we mean the full-screen space.

## Module map
| # | Module | ~min |
|---|---|---|
| 01 | Explore the governed gold data products in Unity Catalog | 15 |
| 02 | Ask the data questions in SQL (the story beats) | 20 |
| 03 | **Create YOUR OWN Genie space and ask in plain English** | 25 |
| 04 | Build / refine a dashboard | 15 |

**Next:** open `01_explore_uc`.'''),
    ]
    write_nb(os.path.join(NB_DIR, "00_WORKSHOP_GUIDE.ipynb"), cells)


def explore():
    cells = [
        md('''# 01 · Explore the governed gold data products
**Session 3 · step 1 of 4 · ~15 min**

🧠 **The idea.** Before you query anything, learn to *see* what's governed and how it's
organized. Unity Catalog is the single place where every table, its schema, its lineage,
and its access live. An analyst who can navigate UC never has to ask "where does this
number come from?" — they can look.

🏢 **Why FHLB-Topeka cares.** Governed, discoverable data is the prerequisite the day
opens with (Session 1). This is that governance, from the analyst's seat.'''),
        code(CONFIG),
        code(VERIFY),
        md('''## Exercise 1 — three ways to inspect a data product

You'll inspect `member_advance_summary` three ways. **Predict first:** how many columns
do you think an "advance summary" needs to answer *who owes us how much, at what rate,
maturing when*? Jot a number, then check.

**Way 1 — the Catalog UI (click).** In the left nav open **Catalog**, expand
`serverless_stable_6fhczt_catalog` → `fhlb_gold` → `member_advance_summary`. Look at the
**Columns**, **Sample Data**, **Details**, and **Lineage** tabs. Lineage shows this gold
product was built from silver — that's your provenance.'''),
        code('''# Way 2 — describe the schema from code
display(spark.sql(f"DESCRIBE TABLE {GOLD}.member_advance_summary"))'''),
        sql('''-- Way 3 — peek at the data (SQL). Was your column-count prediction close?
SELECT * FROM fhlb_gold.member_advance_summary LIMIT 10'''),
        md('''👀 **Insight.** One governed table already answers "who / how much / what rate /
maturing when" per member. That's what "gold data product" means — modeled for a question,
not a raw dump.'''),
        md('''## Exercise 2 — what else is on the shelf?
List every gold data product, then pick one you haven't seen and describe it.'''),
        sql('''SHOW TABLES IN fhlb_gold'''),
        code('''# Your turn: change the table name and run.
tbl = "member_collateral_capacity"   # <- try portfolio_concentration, mpf_portfolio_summary, ...
display(spark.sql(f"DESCRIBE TABLE {GOLD}.{tbl}"))'''),
        md('''## 🧑‍💻 Your Turn
- Find the table that would answer **"which members are undercollateralized?"** (hint: capacity).
- Open its **Lineage** tab in the Catalog UI — what silver table feeds it?

## ⚠️ Fallback
If the Catalog UI is slow, `DESCRIBE TABLE` and `SHOW TABLES IN fhlb_gold` from code give
you the same structure in seconds.

## 🌟 Optional
Run `DESCRIBE HISTORY fhlb_gold.member_advance_summary` — every write to a governed Delta
table is versioned and auditable.

---
### ✅ Done
**Next:** open `02_sql_analysis`.'''),
    ]
    write_nb(os.path.join(NB_DIR, "01_explore_uc.ipynb"), cells)


def sql_analysis():
    cells = [
        md('''# 02 · Ask the data questions in SQL
**Session 3 · step 2 of 4 · ~20 min**

🧠 **The idea.** Governed gold means the hard modeling is done — so an analyst's SQL is
short and reads like the business question. We'll land the four story beats: **concentration,
collateral, credit (MPF), and housing.** Try each yourself; a reference answer follows.

🏢 **Why FHLB-Topeka cares.** These are the Bank's standing questions. Answering them from
governed gold in a few lines is exactly the "analyst enablement" outcome for the day.'''),
        code(CONFIG),
        md('''## Beat 1 — Concentration: who dominates the advance book?
**Predict-then-check:** what share do you think the single largest member holds? 5%? 15%? 25%?'''),
        sql('''-- Try it: rank members by outstanding advances and show each one's share of the book.
-- (portfolio_concentration already has share_of_advance_book.)
-- Write your query, then compare to the reference below.
'''),
        sql('''-- ▼ Reference answer — compare after you try
SELECT member_name, state,
       ROUND(total_outstanding_par/1e6, 1)  AS outstanding_$m,
       ROUND(share_of_advance_book*100, 1)  AS pct_of_book
FROM fhlb_gold.portfolio_concentration
ORDER BY total_outstanding_par DESC
LIMIT 5'''),
        md('''👀 **Insight.** **Midwest Savings Bank (NE) ≈ 24.3% ($335M)** of a **$1.38B** book;
the **top 5 ≈ 62%.** One member is nearly a quarter of the book — that's concentration risk
you'd want a limit and a dashboard tile on.'''),
        md('''## Beat 2 — Collateral: who's undercollateralized?
Averages say ~30% utilization (healthy). Averages lie. Find the exceptions.'''),
        sql('''-- Try it: which members have collateral utilization over 100% (advances > lendable value)?
-- table: fhlb_gold.member_collateral_capacity, column: collateral_utilization_pct (a ratio, 1.0 = 100%)
'''),
        sql('''-- ▼ Reference answer
SELECT member_id,
       ROUND(collateral_utilization_pct*100, 1) AS utilization_pct,
       ROUND(total_outstanding_par/1e6, 1)      AS advances_$m,
       ROUND(total_lendable_value/1e6, 1)       AS lendable_$m,
       is_undercollateralized,
       CASE WHEN stale_market_value > 0 THEN 'STALE' ELSE '' END AS valuation_flag
FROM fhlb_gold.member_collateral_capacity
ORDER BY collateral_utilization_pct DESC
LIMIT 8'''),
        md('''👀 **Insight.** **M1011 is undercollateralized at ~106.6%** — advances exceed lendable
value. And **7 members carry a stale market value** on collateral: a data-quality signal that
is itself a risk (you may be lending against a valuation that's out of date).'''),
        md('''## Beat 3 — Credit: is MPF delinquency uniform, or by product?'''),
        sql('''-- ▼ Reference answer — delinquency by MPF product
SELECT mpf_product,
       SUM(loan_count)                       AS loans,
       ROUND(AVG(delinquency_rate)*100, 2)   AS delinquency_pct,
       ROUND(AVG(serious_delinquency_rate)*100, 2) AS serious_pct,
       ROUND(AVG(avg_credit_score))          AS avg_fico
FROM fhlb_gold.mpf_portfolio_summary
GROUP BY mpf_product
ORDER BY delinquency_pct DESC'''),
        md('''👀 **Insight.** Overall delinquency is **4.76%**, but it's **not uniform**:
**MPF Xtra ≈ 5.71%** vs **MPF 35 ≈ 3.21%.** Product mix, not just the headline, drives credit risk.'''),
        md('''## Beat 4 — Housing: the district's HPI trend (from the silver time series)
The gold `housing_market_reference` is a *point-in-time* snapshot. For a trend, use the
silver HPI time series.'''),
        sql('''-- ▼ Reference answer — district (CO/KS/NE/OK) average HPI by year
SELECT year, ROUND(AVG(hpi_index), 1) AS avg_hpi
FROM fhlb_silver.fhfa_hpi
WHERE state IN ('CO','KS','NE','OK')
GROUP BY year
ORDER BY year'''),
        md('''👀 **Insight.** District HPI ran **58.8 (1975) → 569.4 (2026)**, with a visible **dip
through 2008–2011** and a steep **2020–2023** climb. Note we trend on complete years — the newest
partial period can read flat/0% YoY and should be labeled, not charted as a cliff.'''),
        md('''## 🧑‍💻 Your Turn (pick your path)
- **SQL:** join `member_advance_summary` to `member_collateral_capacity` — is the most
  *concentrated* member also well-collateralized?
- **Or skip ahead:** you'll ask exactly these in plain English in module 03.

## ⚠️ Fallback
Every reference cell above is runnable as-is against governed gold — run them if your own
query misbehaves.

## 🌟 Optional
Rank members by `par_maturing_90d` (from `member_advance_summary`) — who has the most
advances rolling off in the next quarter?

---
### ✅ Done
**Next:** open `03_genie_space` — now you'll ask these in plain English.'''),
    ]
    write_nb(os.path.join(NB_DIR, "02_sql_analysis.ipynb"), cells)


def genie_space():
    cells = [
        md('''# 03 · Create YOUR OWN Genie space and ask in plain English
**Session 3 · step 3 of 4 · ~25 min · the main hands-on**

🧠 **The idea.** A **Genie space** lets a business user ask questions in plain English and
get governed SQL + answers back — *without writing SQL.* But a good Genie space isn't
automatic: you choose the right tables, add instructions and example questions, and curate
it. In this module **you build your own** and feel what makes it answer well vs. poorly.

🏢 **Why FHLB-Topeka cares.** The day's working assumption is *foundation-building before
broad Genie exposure.* Building a space yourself — on governed data, scoped and curated — is
exactly that foundation: you learn the pattern before you hand it to the business.'''),
        md('''## Step 1 — Create the space (name it after yourself)
1. Left nav → **Genie** → **New** (or **Genie** from the SQL editor).
2. **Name it `firstname-lastname FHLB Advances`** (use *your* name — many of us share this
   workspace, so unique names keep spaces from colliding).
3. Pick your **SQL warehouse** when prompted.

## Step 2 — Add the right tables as assets
Add these governed gold tables (Genie answers only from what you add):
- `fhlb_gold.portfolio_concentration`
- `fhlb_gold.member_advance_summary`
- `fhlb_gold.member_collateral_capacity`
- `fhlb_gold.mpf_portfolio_summary`

**Why these four:** they carry the concentration, maturity, collateral, and credit story.
Leaving raw/irrelevant tables out is a *feature* — a tight space answers better.'''),
        md('''## Step 3 — Ask, in plain English
Open the space full-screen (its own tab) and ask these. Compare each answer to what you
found in SQL (module 02) — **the numbers should match.**

1. *"Which members have the largest outstanding advances?"*
2. *"What share of the total advance book does the top member hold?"*
3. *"Which members are undercollateralized?"*
4. *"What is the MPF delinquency rate by product?"*

👀 **Watch for:** does Genie pick the right table? Does its number match your SQL? When it's
off, that's your cue to **curate** (next step).'''),
        md('''## Step 4 — Curate: make it answer better
This is the skill. In the space's settings:
- **General instructions** — add business context, e.g.
  *"Advances are outstanding par in USD. 'Concentration' = a member's share_of_advance_book.
  A member is undercollateralized when collateral_utilization_pct > 1.0. Numbers are
  illustrative, not production."*
- **Example / trusted questions (SQL snippets)** — save your module-02 queries as trusted
  answers (e.g. the top-5 concentration query). Genie reuses them and generalizes.
- **Column descriptions & synonyms** — teach it that "the book" = the advance book, "delinquent"
  maps to `delinquency_rate`.

Re-ask question 2 ("what share does the top member hold?") after adding instructions — it
should now reliably return **~24.3% (Midwest Savings Bank).**'''),
        md('''## Step 5 — (Optional) verify a Genie answer against SQL, right here
Genie should agree with governed SQL. If you want to prove it, run the matching query in a
cell and eyeball it against Genie's answer.'''),
        sql('''-- The "top member's share" ground truth (should match your Genie answer: ~24.3%)
SELECT member_name, ROUND(share_of_advance_book*100,1) AS pct_of_book
FROM fhlb_gold.portfolio_concentration
ORDER BY share_of_advance_book DESC
LIMIT 1'''),
        md('''## 🧑‍💻 Your Turn
- Add **one general instruction** and **one trusted question**, then ask a question you *didn't*
  seed and see if curation helped it generalize.
- Ask a deliberately **ambiguous** question ("who's risky?") and watch how Genie interprets it —
  then tighten your instructions so it picks a definition.

## ⚠️ Fallback / governance notes
- If Genie returns a number that doesn't match SQL, trust the SQL and curate the space —
  that gap *is* the lesson.
- **Sharing is governed:** a Genie space respects Unity Catalog permissions — a viewer only
  ever sees data they're already entitled to. That's why "foundation before broad exposure"
  works: the governance is already underneath.

## 🌟 Optional
Create a **second** space on housing (`housing_market_reference` + `fhlb_silver.fhfa_hpi`) and
ask *"how has district housing changed since 2008?"* — compare curated vs. uncurated answers.

---
### ✅ Done
**Next:** open `04_dashboard` — turn these answers into a shareable view.'''),
    ]
    write_nb(os.path.join(NB_DIR, "03_genie_space.ipynb"), cells)


def dashboard():
    cells = [
        md('''# 04 · Build / refine a dashboard
**Session 3 · step 4 of 4 · ~15 min**

🧠 **The idea.** Genie answers *ad-hoc* questions; a dashboard answers the *standing* ones
at a glance and can be shared/scheduled. Same governed gold tables underneath — so the
dashboard, the Genie space, and the SQL all agree by construction.

🏢 **Why FHLB-Topeka cares.** A concentration + collateral + housing view is the kind of
monitoring the Bank wants standing, governed, and shareable — not rebuilt in a spreadsheet
each week.'''),
        code(CONFIG),
        md('''## Step 1 — Start an AI/BI dashboard (name it after yourself)
1. Left nav → **Dashboards** → **Create dashboard**.
2. **Name it `firstname-lastname FHLB Monitor`.**
3. You'll add a **dataset** (a SQL query) and then **visualizations** on top of it.

## Step 2 — Dataset: the concentration view
In the dashboard's **Data** tab, add a dataset with this query (this is your module-02
Beat 1, lightly shaped for charting):'''),
        sql('''SELECT member_name, state,
       ROUND(total_outstanding_par/1e6, 1) AS outstanding_$m,
       ROUND(share_of_advance_book*100, 1) AS pct_of_book
FROM fhlb_gold.portfolio_concentration
ORDER BY total_outstanding_par DESC'''),
        md('''## Step 3 — Add three visualizations
On the **Canvas**:
1. **Bar chart** — `member_name` (x) by `outstanding_$m` (y). Sort descending. This *is* the
   concentration story: the first bar (Midwest Savings Bank) towers.
2. **Counter / KPI** — the top member's `pct_of_book` (≈ **24.3%**). Add a second counter for
   total book (**$1,382M**).
3. **Housing line chart** — add a second dataset (the district HPI trend from module 02, Beat 4)
   and plot `avg_hpi` over `year`. Label the newest partial period so it doesn't read as a cliff.

💡 **Ask Genie (tie it together).** Anything you can chart, you can also ask your space — a
dashboard tile and a Genie answer on the same governed table will match. That's the analyst
enablement promise in one sentence.'''),
        md('''## Step 4 — A geo/aggregated angle (optional)
If you add a map, **aggregate to one point per state**, not per member/row — a per-row map
chokes and misleads. Group advances by `state` and size/color by the total. (You already have
`state` on `portfolio_concentration`.)'''),
        sql('''-- dataset for a state-level map or bar: advances by state
SELECT state, ROUND(SUM(total_outstanding_par)/1e6, 1) AS outstanding_$m,
       COUNT(*) AS members
FROM fhlb_gold.portfolio_concentration
GROUP BY state
ORDER BY outstanding_$m DESC'''),
        md('''## 🧑‍💻 Your Turn
- Add a **collateral tile**: a counter for the count of undercollateralized members (should be **1**)
  and one for members with **stale valuations** (**7**). (Source: `member_collateral_capacity`.)
- **Publish** your dashboard and open the viewer — note it respects UC permissions, like Genie.

## ⚠️ Fallback
If a viz won't render, check the dataset query runs on its own in the SQL editor first — a
dashboard viz is only ever as good as its dataset query.

## 🌟 Optional / Going deeper
- Add an **MPF-by-product** bar (delinquency_pct by product) — the Xtra vs 35 spread.
- Add a **filter** on `state` and watch every tile update together.

---
### ✅ Done — you've gone governed-data → SQL → your own Genie space → dashboard.
**Wrap:** bring your Genie space + dashboard to the Session 5 discussion — they're inputs to
the use-case prioritization.'''),
    ]
    write_nb(os.path.join(NB_DIR, "04_dashboard.ipynb"), cells)


if __name__ == "__main__":
    guide()
    explore()
    sql_analysis()
    genie_space()
    dashboard()
    print("\nAll Session 3 hands-on notebooks built.")
