# Session 1 — Governance, Security & AI Readiness

**Time:** 8:15–9:00 AM (45 min) · **Presenters:** Gabe / Zoeb · **Format:** Presenter-led demo
**Audience:** Security, Innovation, Platform, and IT teams

> **The idea.** Governance is the foundation everything else in the day rests on. Before FHLB-Topeka
> opens Genie to analysts (Session 3) or serves data to applications (Session 4), we show that Unity
> Catalog gives one control plane for access, classification, lineage, and audit — and that the same
> plane governs AI. We prove it on the FHLB demo estate, then translate to their environment.
>
> **Why now, for them.** Today that governance is spread across SQL Server, Snowflake, ~8 internal APIs,
> ADF/Tidal orchestration, and CSV/file shares — no shared taxonomy, no single audit trail. FHLB-Topeka's
> own stated priority is **foundation-building before broad Genie exposure**: this session *is* that
> foundation, and it's also what makes the Session 2B target-state (fewer hand-built loads, less ADF
> reliance) safe to standardize on.

---

## Facilitator notes / prep

- **⚠️ 45 minutes is tight for BOTH Unity Catalog and Unity AI Gateway.** (The agenda authors flagged
  this.) Decision to make in the room in the first 2 minutes: either (a) go deep on UC governance and
  give AI Gateway a 5-minute "here's what it is + prereqs" close, or (b) split AI Gateway into a
  dedicated follow-up session. **Recommended:** option (a) today — land UC hard, tee up AI Gateway as a
  named next step with an owner. Say this out loud so Security knows AI Gateway isn't being skipped,
  it's being sequenced.
- **Pre-open in browser tabs (before attendees walk in):**
  1. Catalog Explorer → `serverless_stable_6fhczt_catalog` → the four schemas.
  2. Governance Console app: `fhlb-governance` (https://fhlb-governance-7474644368732926.aws.databricksapps.com).
  3. A gold table's **Lineage** tab (e.g. `fhlb_gold.member_advance_summary`).
  4. Catalog Explorer → a column with the `classification` tag applied.
- **Framing to repeat:** "This is illustrative demo data — real FHFA public data plus a synthetic
  member book — not FHLB-Topeka production. The *governance pattern* is what transfers."
- **This is a demo, not a lab** — nobody's at a keyboard. Keep it a guided tour; invite Security to
  interrupt with "how would that map to us?" — those interrupts ARE the outcome (the action list).

- **Who's in the room & what's in it for them** (tie each beat back to these):

  | Team | What they get from Session 1 |
  |---|---|
  | **Security / Compliance** | Sensitive data classified with a *closed* value set; every query auditable; and (S1b) member PII that can't leak into a model prompt. |
  | **IT** | One access model + one immutable audit across the whole estate — not separate grants on SQL Server, Snowflake, the internal APIs, and file shares. |
  | **Platform** | One control plane (access, classification, lineage, audit, cost) instead of a tool-by-tool patchwork — less to operate given limited engineer capacity. |
  | **Innovation** | A governed, *safe* path to Genie/model adoption — the foundation that lets them say "yes" to the business without opening a data-leak risk. |

- **The decisions this governance protects** — say this so it doesn't read as "IT plumbing." The gold
  products under these grants answer FHLB-Topeka's real questions, each with an owner: **advance
  concentration** (Risk/Treasury), **undercollateralized members + stale collateral valuations**
  (Credit/Collateral risk), **MPF delinquency by product** (Credit/MPF program), **district
  (CO/KS/NE/OK) housing exposure** (Risk/Strategy). Governance is what lets those answers be trusted,
  audited, and shared without over-exposing the underlying member data.

---

## Run-of-show

| Min | Block | Outcome it drives |
|---|---|---|
| 0–3 | Framing + the four-schema medallion | Shared vocabulary |
| 3–15 | UC access control + classification | Access model + data-classification standard |
| 15–25 | Lineage + auditability | Traceability + audit story |
| 25–35 | Governance Console app (the artifact) | "One pane" proof; cost + estate |
| 35–43 | AI readiness: AI Gateway + Genie Space governance | AI responsibilities + prereqs |
| 43–45 | Action list capture | Named owners |

---

## 1. Framing + catalog organization (0–3 min)

**Do:** Catalog Explorer → `serverless_stable_6fhczt_catalog`. Show the four schemas:
`fhlb_bronze`, `fhlb_silver`, `fhlb_gold`, `fhlb_ops`.

**Say:** "Everything is organized as a medallion inside one governed catalog. Bronze is raw as-landed —
real FHFA public data (house-price index, the FHLBank public-use database, Fed DFAST scenarios) plus a
small synthetic member book. Silver is conformed. Gold is the products analysts and apps actually touch.
`ops` is our operational + governance rollups. Every object here has one owner, one set of grants, one
audit trail — that's the whole point of Unity Catalog: **one control plane, not one per tool.**"

**Numbers to anchor:** bronze is ~92% real regulatory data (HPI 10,455 rows, PUDB 46,981, DFAST 26) and
~8% synthetic book (80 members, 194 advances, 458 collateral positions, 4,000 MPF loans).

## 2. Access control + data classification (3–15 min)

**Do:**
- On `fhlb_gold`, open **Permissions**. Show grants are at catalog / schema / table level to groups, not
  individuals. Point out the app service principals hold *scoped* grants (e.g. Member 360's SP can
  `SELECT` on `fhlb_gold` but not the raw bronze).
- Open a table with PII-ish columns and show the **`classification`** column tag. State the governed
  allowed values explicitly: **`confidential`, `restricted`, `public`, `internal`** — it's a *governed
  tag*, so those are the only permitted values; nobody can free-type a fifth.

**Say:** "Two things Security cares about are both native here. First, **access is grants to groups plus
service principals**, inheriting down the hierarchy — grant on the schema, every table follows. Second,
**classification is a governed tag with a closed value set** — you can't tag something `super-secret`;
it must be one of confidential / restricted / public / internal. That's how you make a classification
*standard* enforceable instead of a spreadsheet nobody updates."

**Ask them:** "What's your classification taxonomy today, and is it *enforced* or just documented — and
does it hold consistently across SQL Server, Snowflake, the internal APIs, and your file/CSV sources?"
(Capture — the value is a single taxonomy that survives the move off those siloed systems in Session 2B.)

## 3. Lineage + auditability (15–25 min)

**Do:**
- On `fhlb_gold.member_advance_summary`, open the **Lineage** tab. Walk upstream: gold ← silver ←
  bronze ← the source file. Note column-level lineage.
- Mention the system tables behind it: `system.access.table_lineage`, `system.access.column_lineage`,
  and `system.access.audit` for who-queried-what.

**Say:** "Lineage isn't something we maintained — UC captured it automatically as the pipelines ran. For
a regulated institution that's the difference between 'we think this number comes from HPI' and a
column-level graph you can hand an examiner. And `system.access.audit` is the immutable record of every
query, by every principal, including the apps."

**Note (honest):** the app service principals **cannot** be granted `SELECT` on `system.*` directly
(that needs an account admin). Our Governance Console works around this by materializing rollups from
`system.*` as the deploying identity into `fhlb_ops.gov_*` tables. Say so — it's a real prereq for their
own build: "someone with account-admin scope has to stand up the system-table access once."

## 4. The Governance Console app — the artifact (25–35 min)

**Do:** Open **fhlb-governance**. Walk the tabs:
- **Estate overview** — schemas, tables, classification coverage (gaps highlighted).
- **Access & audit** — recent access, denied/failed attempts, from `system.access.audit`.
- **Lineage** — the table/column lineage rollups.
- **Cost** — DBU/spend attributed to the demo compute only.
- **Review & actions** — governance decisions (acknowledge / request remediation / escalate) written to
  an append-only `governance_actions` audit table.

**Say:** "This is a Databricks App any of your teams could build — it's just Streamlit over the system
tables. The point isn't this specific app; it's that governance data is *queryable data*. You can build
your own cockpit. Note the cost tab is **scoped to the demo assets** — account-wide it was 4,117 usage
rows; filtered to this demo it's 7. Scoping matters so a governance view doesn't leak the whole account."

**Ask them:** "Who owns the estate view today? Is there a single place your Security team sees
classification gaps and denied access?" (Capture — likely an action item.)

## 5. AI readiness — AI Gateway + Genie Space governance (35–43 min)

> Keep this tight (see facilitator note). Goal: establish that **AI is governed by the same plane**, and
> capture the prerequisites, not to configure it live.

**Say (AI Gateway):** "Unity AI Gateway puts the same governance in front of model endpoints:
- **Policy enforcement** — rate limits, allowed models, PII/guardrails at the gateway, not per-app.
- **Model access controls** — who/which SP can call which model, as UC grants.
- **Monitoring** — usage, cost, and payload logging in system tables, same as data.
**Prerequisites for FHLB-Topeka:** confirm AI Gateway is enabled on the workspace; decide the allowed
model list; decide logging/retention posture with Security. That's a pre-work item — can we confirm
before or shortly after today?"

**Say (Genie Space governance — sets up Session 3):** "When we open Genie in Session 3, it inherits
UC grants — Genie can only read what the user could already read. Governance decisions to make:
**data domains** (which gold tables belong in which space), **retention** of the question/answer log,
**quality standards** (curated metric definitions and sample questions so answers are trustworthy), and
**controlled sharing** (who the space is shared to). We deliberately keep Genie to a *foundation-building*
scope first — analysts and prototyping — before broad business exposure. Session 5 shows where that
leads."

## 6. Action list capture (43–45 min)

Close by reading back the captured items and assigning owners. Target artifact:

| Action | Owner | Due |
|---|---|---|
| Confirm AI Gateway enablement + allowed-model policy | Security + Platform | pre-pilot |
| Define/enforce classification taxonomy (map to UC governed tag) | Data Governance | pre-pilot |
| Stand up system-table access (account admin) for governance cockpit | Platform + account admin | pre-pilot |
| Decide Genie Space domains, retention, sharing policy | Innovation + Security | before Session 3 pilot |
| Name a single owner for the estate/access governance view | Security | this week |

---

## Likely Q&A

- **"Can Genie see data a user shouldn't?"** No — Genie executes as the user against UC; grants are the
  ceiling. Nothing bypasses the catalog.
- **"Is lineage reliable enough for an examiner?"** It's system-captured at column level from actual
  query execution, not hand-maintained — that's stronger than most documented lineage. Pair it with the
  audit log for the full chain.
- **"Where does AI Gateway logging live and who can see it?"** System tables, governed by UC grants —
  you decide retention and who reads it, same model as `system.access.audit`.
- **"How is this different from what we do with SQL Server permissions today?"** One plane across all
  data + AI + apps + BI, with inheritance, governed tags, automatic lineage, and an immutable audit —
  versus per-system, per-tool access models that don't share a taxonomy or an audit trail.
- **"Does classification tagging scale to thousands of columns?"** Tags inherit and can be applied
  programmatically; the governed value set keeps it consistent. Start with a policy for the taxonomy,
  then automate application.

## Outcomes (agenda checklist) — with success measures

- [ ] **Shared governance framework** — UC as one control plane for access, classification, lineage, audit.
      *Success measure:* agreement to standardize the estate under one catalog + governed classification tag.
- [ ] **Defined data, platform, security, and AI responsibilities** — who owns grants, tags, system-table
      access, AI Gateway policy, and Genie Space governance. *Success measure:* every row in the action
      table below has a **named owner** (role/team) and a due milestone.
- [ ] **Initial access & policy action list with owners** — the table above, filled and assigned.
      *Success measure:* a target for **classification coverage** (e.g. 100% of gold columns tagged) and
      **audit coverage** (model + data access both landing in system tables) before the Session 3 pilot.
- [ ] **Foundation-first confirmed** — explicit agreement that governance + AI Gateway prerequisites land
      *before* broad Genie exposure (Session 3 is the analyst/prototyping foundation, Session 5 the path forward).

---
**Next:** 9:00 — Session 2A, Data & Platform Deep Dive (Current State).
