# Session 3 — Analyst Enablement: Dashboards & Genie (hands-on)

> **⌨️ Hands-on** — attendees at their own keyboards, building their own Genie space and dashboard. **This is the one hands-on lab of the day.**

**Time:** 1:15–2:30 PM (~75 min) · **Format:** hands-on lab (attendees at keyboards)
**Presenters/coaches:** Databricks team · **Audience:** FHLB-Topeka analysts, BI developers,
data-savvy business users, the Innovation team, and selected platform partners
**Notebooks:** `notebooks/00_WORKSHOP_GUIDE` → `01_explore_uc` → `02_sql_analysis` →
`03_genie_space` → `04_dashboard`

> **What every attendee leaves with:** their **own governed Genie space** and their **own
> AI/BI dashboard**, each answering a *real* FHLB-Topeka business question on governed data.
> That is the "analyst enablement" outcome — and the deliberate first step on FHLB-Topeka's
> stated path of **foundation-building before broad Genie exposure.**

---

# Part A — Facilitator notes (read before the room does)

**The goal, in one line.** Prove that an FHLB-Topeka analyst can go from *governed data* to
*a business answer* — in SQL, in plain-English Genie, and on a dashboard — in ~75 minutes,
with governance already underneath.

**Why this matters to FHLB-Topeka (say it up front):** the Bank wants analysts and business
users self-serving on advances, collateral, MPF, and housing — *without* waiting on
engineering (which is capacity-constrained) and *without* ungoverned spreadsheets. This is the
controlled, repeatable pattern for that.

**Timing (honest):**

| Module | Buffered | Fast room | Where it can overrun |
|---|---|---|---|
| 01 explore UC | 12 min | 8 min | people exploring the Catalog UI |
| 02 SQL beats | 18 min | 12 min | — (reference cells always run) |
| 03 **your Genie space** | 30 min | 22 min | **the swing factor** — space creation + curation |
| 04 dashboard | 15 min | 10 min | first-time viz building |

**The two unblock phrases** (say them whenever someone stalls):
1. *"Run the reference cell"* — every answer cell is runnable against governed gold, so a
   broken attempt never blocks anyone.
2. *"Name it `firstname-lastname`"* — the #1 stumble in a shared workspace is duplicate Genie
   space / dashboard names. Enforce the naming from the first minute.

**Where people get stuck (and the fix):**
- *Genie answer ≠ SQL number* → that's the teaching moment: curate the space (add an
  instruction + a trusted question), re-ask. Expect it to settle on **~24.3%**.
- *"Table not found"* → wrong catalog (Mode B) — set the **`catalog` widget** at the top of the
  notebook to the workshop catalog and re-run. The verify cell lists what's present.
- *Dashboard viz won't render* → run the dataset query on its own in the SQL editor first.
- *Empty map* → aggregate to one point per state, not per row.

**Prereqs (confirm before the session):** each attendee needs workspace access + attach-to-
serverless, a running **serverless SQL warehouse**, the **Databricks SQL** entitlement (Genie +
dashboards), and read grants on `fhlb_gold` / `fhlb_silver`. Full list + copy-paste GRANT block:
`instructor/ATTENDEE_REQUIREMENTS.md`. Mode A points at the live catalog already; Mode B needs
`00_LOAD_DATA` run once first.

**Success measures for the session:**
- ☐ Every attendee has a **named Genie space** answering ≥3 FHLB business questions correctly.
- ☐ Every attendee has a **published dashboard** with the concentration + housing views.
- ☐ The room can state the requirements for promoting a space from prototype → controlled pilot
  (captured as input to Session 5).

---

# Part B — Participant walkthrough ("this is how you do it")

Work top to bottom. Each step is **Do → ✅ You should see → 👉 Now try**. When something
misbehaves, the **⚠️ Unblock** note gets you moving in seconds. You are **read-only on the
data** — the things you *build* are your own Genie space and dashboard.

## The story you're going to uncover (the hook)
FHLB-Topeka's advance book is **$1.38B across 37 active members** — and it's **concentrated**.
You'll find the single member holding ~a quarter of it, the member who's *undercollateralized*,
where credit risk actually lives in MPF, and how district housing has moved. Every number you
see is real and validated.

---

## Step 0 · Open the guide (2 min)
**Do:** open `00_WORKSHOP_GUIDE`. Skim the data story, the three rules, and the module map.
**✅ You should see:** the medallion picture and the "what's in today's data" numbers.
**Remember the rules:** (1) you're read-only on data; (2) name your own objects
`firstname-lastname`; (3) it's illustrative, not production data.

---

## Step 1 · Explore the governed data in Unity Catalog — `01_explore_uc` (12 min)
*Business lens:* before you trust a number, you can see where it comes from — that's the
governance a Risk or Credit analyst needs.

**Do:** run the **config** and **verify** cells.
**✅ You should see:** `✓ All 5 analyst gold tables are readable.`
⚠️ **Unblock:** if it lists missing tables, set the **`catalog` widget** (top of the notebook, Mode B) and re-run.

**Do:** Exercise 1 — inspect `member_advance_summary` three ways: the **Catalog UI**
(Catalog → your catalog → `fhlb_gold` → the table → Columns / Sample Data / **Lineage**), then
`DESCRIBE TABLE`, then `SELECT * … LIMIT 10`.
**✅ You should see:** one governed table already answers *who owes us how much, at what rate,
maturing when* — and the **Lineage** tab shows it was built from silver (your provenance).
**👉 Now try:** find the table that answers *"which members are undercollateralized?"* (hint:
capacity) and open its Lineage tab.

---

## Step 2 · Ask the data questions in SQL — `02_sql_analysis` (18 min)
*Each "beat" is a real FHLB decision. Try each yourself, then run the reference cell to check.*

**Beat 1 — Concentration** *(owner: Risk / Treasury — sets member exposure limits).*
**Do:** run the concentration query.
**✅ You should see:** **Midwest Savings Bank (NE) ≈ 24.3% ($335M)** of the book; **top 5 ≈ 62%**.
*Decision it drives:* is one member too large a share of the book?

**Beat 2 — Collateral** *(owner: Credit / Collateral risk).*
**Do:** run the utilization query.
**✅ You should see:** **M1011 undercollateralized at ~106.6%** and **7 members with stale
collateral valuations**. *Averages (~30%) hide the members that matter.*

**Beat 3 — MPF credit** *(owner: Credit / MPF program).*
**✅ You should see:** overall delinquency **4.76%**, but **MPF Xtra 5.71%** vs **MPF 35 3.21%** —
product mix, not the headline, drives risk.

**Beat 4 — District housing** *(owner: Risk / Strategy).*
**✅ You should see:** CO/KS/NE/OK HPI **58.8 (1975) → 569.4 (2026)**, with a 2008 dip.
**👉 Now try:** join `member_advance_summary` to `member_collateral_capacity` — is the most
*concentrated* member also well-collateralized?
⚠️ **Unblock:** every reference cell runs as-is against governed gold — run it if your own query misbehaves.

---

## Step 3 · Create YOUR OWN Genie space — `03_genie_space` (30 min · the centerpiece)
*This is the skill FHLB-Topeka wants to build before opening Genie to the business: a governed,
curated space an analyst owns.*

**Do — create it:** Genie → **New** → **name it `firstname-lastname FHLB Advances`** (your name!)
→ pick your SQL warehouse.
⚠️ **Unblock:** unique name = no collisions with the 20 others in the room.

**Do — add the right tables:** add exactly these four gold tables as assets:
`portfolio_concentration`, `member_advance_summary`, `member_collateral_capacity`,
`mpf_portfolio_summary`. *(Leaving irrelevant tables out is a feature — a tight space answers better.)*

**Do — ask in plain English** (open the space full-screen, its own tab):
1. *"Which members have the largest outstanding advances?"*
2. *"What share of the total advance book does the top member hold?"*
3. *"Which members are undercollateralized?"*
4. *"What is the MPF delinquency rate by product?"*
**✅ You should see:** answers that **match your SQL from Step 2** (esp. **~24.3%** for Q2).

**Do — curate it** (the real skill): in space settings add
- a **general instruction**: *"Advances are outstanding par in USD. 'Concentration' = a member's
  share_of_advance_book. A member is undercollateralized when collateral_utilization_pct > 1.0.
  Numbers are illustrative, not production."*
- a **trusted question**: save your Beat-1 top-5 concentration query.
**✅ You should see:** re-asking Q2 now reliably returns **~24.3% (Midwest Savings Bank)**.
**👉 Now try:** ask a deliberately **ambiguous** question ("who's risky?"), watch Genie interpret
it, then tighten your instructions so it picks a definition.
⚠️ **Unblock / governance:** if Genie disagrees with SQL, trust the SQL and curate — that gap *is*
the lesson. A Genie space respects Unity Catalog permissions, so a viewer only ever sees data
they're already entitled to (that's why "foundation before broad exposure" works).

---

## Step 4 · Build YOUR dashboard — `04_dashboard` (15 min)
*Genie answers ad-hoc questions; a dashboard answers the standing ones a Risk or Treasury lead
watches every week.*

**Do:** Dashboards → **Create** → **name it `firstname-lastname FHLB Monitor`**. Add a dataset
using the concentration query, then add:
1. a **bar** — `member_name` by `outstanding_$m` (the first bar, Midwest Savings Bank, towers);
2. **KPI counters** — top member share (**≈24.3%**) and total book (**$1,382M**);
3. a **housing line** — district HPI over year (label the newest partial period so it isn't a cliff).
**✅ You should see:** the concentration story in one glance.
**👉 Now try:** add a collateral tile — count of undercollateralized members (**1**) and members
with stale valuations (**7**) — then **publish** and open the viewer (it respects UC permissions, like Genie).
⚠️ **Unblock:** if a viz won't render, run its dataset query on its own in the SQL editor first.

---

## ✅ You're done — and here's what you built
Governed data → SQL → **your own Genie space** → **your own dashboard**, all answering real
FHLB-Topeka questions (concentration, collateral, credit, housing) on governed data.

**Bring your Genie space + dashboard to Session 5** — they're the concrete inputs to the
use-case prioritization and the "prototype → controlled pilot" discussion.
