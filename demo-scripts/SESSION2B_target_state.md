# Session 2B — Data & Platform Deep Dive: Target State

> **🗣️ Conversational** — facilitated working session. Attendees discuss and shape the target state; **no keyboards on the platform.**

**Time:** 10:45 AM–12:15 PM (90 min) · **Presenters:** Brice / Gabe / Zoeb · **Format:** Working session
**Audience:** Platform, Citizen, IT, data engineering, and architecture teams

> **The idea.** Take the confirmed current state from 2A and map a pragmatic target: **declarative
> pipelines** to kill the imperative sprawl and standardize Silver/Gold, **Lakeflow Connect** to
> streamline ingestion (and cut ADF), and an honest position on **SDP-META**. Deliverable is a
> prioritized recommendation set + an agreed Lakeflow Connect direction + owners.

---

## Facilitator notes / prep

- This session **decides direction**, it doesn't build. Keep a running "recommendation + owner" list.
- Anchor every recommendation to a 2A pain point so it lands as *their* problem being solved.
- **Be honest on maturity and roadmap.** Several items below are marked **⚠️ CONFIRM** — these are claims
  I could not fully verify for the customer's Azure environment or are roadmap/futures we must not invent.
  Treat them as live questions for the room / product team, not assertions.

---

## Run-of-show

| Min | Block | Drives |
|---|---|---|
| 0–5 | Recap 2A: pains → what we'll address | Framing |
| 5–25 | **SDP-META** — concerns, honest framing, open questions | Position + open items |
| 25–50 | **Declarative pipelines** — imperative→declarative, standardization, less code | Standardization + code-reduction rec |
| 50–70 | **Lakeflow Connect** strategy per source type (+ custom connector, on-prem) | Agreed ingestion direction |
| 70–82 | **Reducing ADF** + retiring the dispatcher/50-trigger workaround | Orchestration rec |
| 82–90 | **Phased migration** of the ~94 loads + owners | Roadmap + responsibilities |

---

## 1. SDP-META — the metadata-driven framework question (5–25 min)

**What we heard:** FHLB is evaluating SDP-META (Pavan has demoed it). Real concerns: (a) running it **at
scale**, (b) **maintainability** since it's **not native** to Databricks, (c) it's a **Databricks Labs
open-source** project — reliance on it is a top concern, (d) will Databricks **absorb it into the base
product**, (e) are there **alternatives** with similar functionality.

**Honest framing to give:**
- SDP-META is a **metadata/config-driven layer that generates declarative pipelines** — the value is
  exactly what FHLB wants: define a load as metadata, not hand-written imperative code, and standardize
  Silver/Gold by construction. The concept is sound and aligns with the target state.
- **⚠️ CONFIRM (roadmap):** Whether Databricks plans to **absorb SDP-META into the native product** — I
  could **not verify any public or internal roadmap** for this. **Do not promise absorption.** Raise it
  directly with Pavan / the Lakeflow product team as a formal open question. What we'd need to confirm:
  official support status, any productization intent, and a support SLA if adopted.
- **Databricks Labs = community/experimental support**, not enterprise-supported product. That is the
  crux of their maintainability concern and it's legitimate. Frame the decision as: *do you take on
  ownership of an OSS layer (with the code-generation leverage it gives) vs. wait for / use native
  capabilities?*

**Alternatives / similar functionality to discuss (so they're not solely reliant on SDP-META):**
- **Native Lakeflow (Spark) Declarative Pipelines** for the declarative transform layer (Section 2) — the
  standardization engine itself is native.
- **A lightweight in-house metadata-driven generator** over native declarative pipelines + **Databricks
  Asset Bundles (DABs)** for CI/CD — you own less code than SDP-META but keep the metadata-driven pattern.
  ⚠️ CONFIRM scope/effort with their engineers.
- **Lakeflow Connect** managed connectors (Section 3) remove whole classes of hand-written ingestion, so
  the amount of pipeline SDP-META would need to generate shrinks.
- **Platform architecture considerations when adopting any non-native OSS layer:** version pinning &
  upgrade cadence, who owns forks/patches, testing against DBR upgrades, blast radius if it breaks, and an
  exit path back to native. Recommend an explicit "own-it checklist" before standardizing on SDP-META.

**Capture:** the SDP-META decision as an **open item with an owner** + the roadmap question routed to product.

## 2. Declarative pipelines — the imperative→declarative answer (25–50 min)

**Maps to pains #1 (imperative sprawl), #3 (no standardization), #4 (code volume).**

**Say:**
- **Lakeflow Spark Declarative Pipelines** (the productized evolution of DLT) let you declare *what* each
  table is (source → transform → target) and the platform handles orchestration, dependencies,
  incremental processing, and retries — **materially less code than imperative notebooks**.
- **Enforceable standardization** comes from **expectations** (data-quality constraints declared on each
  dataset) and a consistent Bronze→Silver→Gold pattern — this is the "enforceable Silver/Gold standard"
  they asked for, expressed as code the platform enforces, not convention.
- **Less to maintain:** fewer lines, declared dependencies instead of hand-wired orchestration, and
  built-in observability — directly addresses limited engineer capacity.
- Cite: Databricks docs → Lakeflow Declarative Pipelines / expectations. ⚠️ CONFIRM exact feature names
  against the workspace version live (product naming has moved from "DLT" → "Lakeflow Declarative
  Pipelines").

**Do (optional):** show the FHLB demo's own gold tables and note they're the kind of standardized output
a declarative pipeline produces; if a pipeline exists in the workspace, show its graph + an expectation.

## 3. Lakeflow Connect — ingestion strategy per source type (50–70 min)

**Maps to pains #2 (ADF reliance), #4 (code volume). Agenda outcome: agreed Lakeflow Connect direction.**

**Grounded capability (Databricks docs, Lakeflow Connect overview):**
- **Managed connectors** named in docs include **Salesforce, HubSpot, Jira, Workday** (SaaS);
  **MySQL, PostgreSQL, SQL Server** (database/CDC); **RabbitMQ** (streaming); **Google Drive, SharePoint**
  (file sources). Release states vary — **⚠️ CONFIRM GA/Preview per connector** in the target workspace.
- **Custom connectors are supported**: *"If no managed or community connector supports your source, you
  can build your own custom connector and run it in your workspace."* — directly enables their
  **internal-API custom connector** ask.
- **Database connectors include an ingestion gateway** (+ staging) for continuous CDC, and the gateway can
  run in the customer's own network for private connectivity.

**Per-source recommendation (confirm live):**
| FHLB source | Recommendation | Notes / ⚠️ CONFIRM |
|---|---|---|
| ~8 internal APIs | **Build a custom Lakeflow Connect connector** to standardize the pattern | Replaces N bespoke notebooks with one connector pattern; scope with their API auth/pagination |
| External APIs | Same custom-connector pattern (or managed if one fits) | |
| Snowflake (Loan Performance) | Evaluate a **managed DB connector / query federation**; semi-annual = simple scheduled ingest | ⚠️ CONFIRM Snowflake-specific connector vs. federation for their volume |
| CSV deliveries → ADLS | **File-based ingestion + file events** (see §4); regular sources = strong custom/managed fit | They already have the ADLS container — no major limitation |
| Future on-prem SQL Server | **Lakeflow Connect SQL Server connector** (gateway-based CDC) **or Lakehouse Federation** (live, no copy) | Gateway runs on **Databricks compute in your VNet**, connecting **outbound** to the DB — **no SHIR-style on-prem agent exists**. Needs a hybrid network path: **⚠️ CONFIRM the Azure connectivity (ExpressRoute / site-to-site VPN into the VNet)** + that classic compute is used (serverless egress to on-prem is constrained). Lower priority per customer. |
| Streaming (future) | General overview only — Structured Streaming + declarative pipelines cover it when latency needs grow | Latency not stringent today ("ready by a time of day") |

**On-prem "SHIR equivalent" — the honest answer:** the customer explicitly wants ADF-SHIR-like on-prem
reach. **There is no drop-in SHIR equivalent.** ADF's Self-Hosted Integration Runtime is an agent you
install *inside* the on-prem network that dials outbound; Databricks instead connects **from its own
compute to the source** — the Lakeflow Connect ingestion gateway runs on **Databricks classic compute in
your VNet**, not on-prem. So the requirement becomes a **networking** one, not an agent: give Databricks
a route to the DB. ⚠️ **CONFIRM** the Azure path (**ExpressRoute or site-to-site VPN into the VNet** +
firewall) and that **classic compute** is used (serverless egress to on-prem is constrained). Named follow-up.

## 4. Reducing ADF + retiring the dispatcher / 50-trigger workaround (70–82 min)

**Maps to pain #2 and the 2A dispatcher story.**

**Say — the concrete win:**
- The **50 file-arrival-trigger limit only applies when file events are NOT enabled** on the external
  location. **Enabling file events on the ADLS external location removes that documented limit** — which
  likely **retires the self-built dispatcher notebook** entirely. *(Databricks docs: file-arrival
  triggers.)* **⚠️ CONFIRM** their dispatcher has no logic beyond fan-out we'd need to preserve, and test
  file-events enablement on their location.
- As file-driven and API loads move to **Lakeflow Connect + declarative pipelines + Databricks-native
  scheduling/triggers**, the **ADF + Tidal** trigger layer shrinks to only what genuinely needs external
  orchestration — reducing (not necessarily eliminating day one) ADF reliance.

## 5. Phased migration sketch for the ~94 loads (82–90 min)

A straw sequence to react to (not a commitment):
1. **Quick win:** enable **file events** on the ADLS location → retire the dispatcher; lift the 50-trigger cap.
2. **Standardize a template:** one **declarative pipeline** pattern with expectations for a representative
   CSV load; prove the code-reduction + standardization.
3. **Custom connector** for internal APIs; migrate the ~8 API loads onto it.
4. **Convert highest-toil imperative loads** to declarative in waves; measure lines-of-code + maintenance delta.
5. **Reduce ADF/Tidal** to residual external-orchestration only; revisit SDP-META decision with real data.

## Outcome (agenda checklist)
- [ ] **Prioritized recommendations** for ingestion, orchestration, catalog structure, and pipeline standardization.
- [ ] **Agreed Lakeflow Connect direction** (custom connector for APIs; file events for CSV; DB connector for future on-prem).
- [ ] **Implementation responsibilities** — owner against each recommendation and each ⚠️ CONFIRM item.

---
**Next:** 12:15 — Lunch, then 1:15 Session 3 (Analyst Enablement — hands-on).
