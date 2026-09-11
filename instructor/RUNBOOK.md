# RUNBOOK — FHLB-Topeka in-person day (Sep 17, 2026, 8:00 AM–5:00 PM)

Databricks team: Gordon Heil, Brice Giesbrecht, Gabe Klick, Zoeb Zavery.
Only **Session 3** is hands-on (the 5 notebooks); Sessions 1/4/5 are presenter-led demos
(see `../demo-scripts/`); 2A/2B are discussion (no build assets).

## Timeline

| Time | Session | Lead | Format |
|---|---|---|---|
| 8:00–8:15 | Welcome, objectives & introductions | All | — |
| 8:15–9:00 | S1 · Governance, Security & AI Readiness | Gabe/Zoeb | Demo (`SESSION1_...md`) |
| 9:00–10:30 | S2A · Data & Platform Deep Dive — Current State | Brice/Gabe/Zoeb | Discussion |
| 10:30–10:45 | Break | — | — |
| 10:45–12:15 | S2B · Data & Platform Deep Dive — Target State | Brice/Gabe/Zoeb | Discussion |
| 12:15–1:15 | Lunch | — | — |
| 1:15–2:30 | **S3 · Analyst Enablement — Dashboards & Genie** | **Gabe/Zoeb** | **HANDS-ON (5 notebooks)** |
| 2:30–3:45 | S4 · Lakebase & GraphQL | Gabe/Zoeb | Demo (`SESSION4_...md`) |
| 3:45–4:00 | Break | — | — |
| 4:00–5:00 | S5 · Business Value & Genie One | Gabe/Zoeb | Demo (`SESSION5_...md`) |

## Session 3 timing (the 75-min hands-on) — plan honestly

| Module | Buffered / mixed room | Fast / technical room |
|---|---|---|
| 01 explore UC gold | 15m | ~10m |
| 02 SQL story beats | 20m | ~15m |
| 03 **create your own Genie space** ⚠️ biggest variable | 25m | ~20m |
| 04 dashboard | 15m | ~12m |
| **Total** | **~75m** | **~57m** |

- **Genie-space creation is the swing factor** (module 03) — first-timers spend time finding
  the New button, picking a warehouse, and adding assets. If the clock is tight, demo the
  *create + add assets* steps once from the front, then let everyone do the *ask + curate*
  loop. Protect time for module 04 and the wrap.
- Per workshop-builder's TIMING.md: stated per-module times are optimistic for beginners;
  setup/explore are the most padded. Fast rooms finish early — queue the 🌟 Optional items
  (second Genie space on housing; MPF-by-product bar; state filter) so no one sits idle.
- Live friction costs real minutes (warehouse attach, SQL entitlement, first Genie space).
  Budget for it; the fallbacks below are what keep the room moving.

## The two unblock phrases (say them out loud)

1. **"Run the reference cell."** Every module-02 answer cell runs as-is against governed gold —
   if someone's own query misbehaves, they run the ▼ Reference answer and keep going.
2. **"Name it firstname-lastname."** The only isolation in this workshop is unique names for
   your **Genie space** and **dashboard** — repeat it so people don't collide in the shared
   workspace.

## Common stumbles → fixes (full list in TROUBLESHOOTING.md)

- Genie's number ≠ SQL → **curate the space** (add a general instruction + a trusted question).
  This gap *is* the lesson, not a failure.
- Two people name a space the same → enforce `firstname-lastname`.
- HPI trend looks flat at the end → that's the partial 2026 period; trend on complete years
  from `silver.fhfa_hpi`, not the gold snapshot.
- Dashboard viz won't render → run its dataset query standalone in the SQL editor first.

## Live-teaching tips

- **Lead with the idea, then the mechanics** — each module opens with 🧠 *The idea* and 🏢
  *Why FHLB-Topeka cares*; read those before clicking.
- **Predict-then-check** — module 02 asks people to guess the top member's share before
  revealing 24.3%. Let them guess; the surprise lands the concentration story.
- **"It's all Genie."** Data questions go to a full-screen Genie *space*; the in-notebook ✨
  is for writing code. Don't call the space "the assistant."
- **Tie it together at the close** — the SQL, the Genie space, and the dashboard all read the
  same governed gold, so they agree by construction. That one sentence is the enablement pitch,
  and it's the bridge into Session 5 (bring your space + dashboard as inputs to prioritization).
