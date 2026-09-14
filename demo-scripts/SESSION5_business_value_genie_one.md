# Session 5 — Business Value, Use-Case Prioritization & Next Steps

**Time:** 4:00–5:00 PM (60 min) · **Presenters:** Gabe / Zoeb · **Format:** Presenter-led demo + working session
**Audience:** Business stakeholders, decision makers, product & operations leaders, Innovation team, technical sponsors

> **The idea.** The day has moved from foundations (governance) to enablement (dashboards + Genie) to
> serving (Lakebase). This session closes the loop: show a business leader asking the platform a plain
> question and getting a trustworthy answer via **Genie One**, then convert that "wow" into a prioritized,
> owned roadmap. We deliberately sequence **foundation-building before broad Genie exposure** — this
> session names the path, it doesn't hand the keys to everyone tomorrow.

---

## Facilitator notes / prep

- Mixed room, most senior of the day. **Lead with business questions, not features.** Every Genie query
  should map to a decision someone in the room actually makes.
- Genie answers are live — rehearse the exact questions in the dry run (see instructor/DRY_RUN.md) and
  confirm the numbers match the story bank, because a business SME *will* sanity-check the top member.
- Pre-open: **Genie One** in the workspace pointed at the FHLB gold tables (or the "FHLB — Advances &
  Collateral" space as a fallback if Genie One isn't scoped in time). Have the prioritization matrix on a
  shared screen / whiteboard ready to fill live.
- Keep it honest: this is illustrative data. The *questions* and the *roadmap* are what's real for FHLB.

### Who's in the room — what's in it for each
- **Business stakeholders / decision-makers** — answers to the decisions they own (concentration limits,
  collateral calls, credit policy, stress posture) in seconds, from numbers the risk team would compute.
- **Product & operations leaders** — a path to **fewer manual/batch report requests** and faster turnaround
  for the front line, without adding headcount.
- **Innovation team** — a repeatable "governed pilot → controlled exposure" blueprint they can champion.
- **Technical sponsors** — confidence that broad enablement is **sequenced behind governance**, not ahead
  of it — the foundation-building-first posture FHLB-Topeka asked for.

---

## Run-of-show

| Min | Block | Outcome it drives |
|---|---|---|
| 0–5 | Reconnect the day to business decisions | Framing |
| 5–20 | Genie One demo on the FHLB use case | "Ask the data" proof |
| 20–30 | Validate priority questions, personas, decisions | Confirmed personas + questions |
| 30–45 | Prioritize candidate use cases (live matrix) | Prioritized backlog + first pilot |
| 45–55 | Phased adoption path + success measures | Phased roadmap |
| 55–60 | Owners + next checkpoint | Named owners + next steps |

---

## 1. Reconnect the day to decisions (0–5 min)

**Say:** "This morning we made the platform *trustworthy* — governed access, classification, lineage,
audit. This afternoon we made it *usable* — dashboards and Genie for analysts — and *serveable* —
Lakebase for applications. The reason all of that matters is the next five minutes: a leader asking a
question in plain English and getting an answer they can act on, grounded in governed data."

## 2. Genie One demo on the FHLB use case (5–20 min)

**Do:** Open Genie One and ask these in order, pausing to connect each answer to a decision. Expected
answers are grounded in today's validated numbers — read them back and let a SME confirm.

1. **"Which members drive our advance concentration?"**
   → Midwest Savings Bank (NE) is **24.3% of the $1.38B book ($335M)**; **top 5 members = 62%.**
   *Decision:* concentration limits, funding diversification, member outreach.
2. **"Which members are undercollateralized?"**
   → Member **M1011 at 106.6% utilization** stands out; portfolio average is a healthy ~30%.
   *Decision:* collateral calls, risk review.
3. **"Are any members carrying stale collateral valuations?"**
   → **7 members** have stale market values. *Decision:* revaluation / data-quality remediation.
4. **"How is housing holding up in our district?"**
   → District (CO/KS/NE/OK) HPI ran from **58.8 (1975) to 569.4 (2026)**, dipped in the 2008 crisis,
   steep 2020–2023 run. *Decision:* collateral haircut assumptions, stress posture.
5. **"Which MPF product has the highest delinquency?"**
   → **MPF Xtra at 5.71%** vs MPF 35 at 3.21%; overall 4.76% (0.88% serious), avg FICO 719.
   *Decision:* product mix, credit policy.

**Say:** "Notice three things: it answered in seconds, it answered from *governed* gold tables so the
number is the same one the risk team would compute, and every answer maps to a decision an executive in
this room owns. That's the difference between a chatbot and a governed analytics assistant."

**Say (governance reminder):** "Genie only reads what the asker is already permitted to read. Broad
exposure is a *governance* decision, not a technical one — which is exactly why we sequence it."

## 3. Validate priority questions, personas, decisions (20–30 min)

Work the room. For each persona, capture their top 1–2 recurring questions and the decision behind it:

| Persona | Recurring question | Decision it supports |
|---|---|---|
| Risk / Credit | _(capture)_ | concentration limits, collateral calls |
| Member Services / Relationship | _(capture)_ | member outreach, product cross-sell |
| Finance / Treasury | _(capture)_ | funding, maturity/liquidity |
| Innovation / Product | _(capture)_ | new data products, portal features |
| Executive / Board | _(capture)_ | risk appetite, strategy |

**Ask:** "Of these, which three questions, answered reliably, would change a decision this quarter?"
Those become the pilot's target questions.

## 4. Prioritize candidate use cases — live matrix (30–45 min)

Fill this on the screen with the room. Score each 1 (low) – 5 (high); readiness/governance/effort where
higher = easier/lower-cost.

| Candidate use case | Business value | Data readiness | Governance ease | Low effort | Priority |
|---|---|---|---|---|---|
| Advance concentration & funding-risk monitoring | | | | | |
| Collateral capacity & undercollateralization alerts | | | | | |
| District housing / HPI-driven collateral stress view | | | | | |
| MPF credit-quality & delinquency by product | | | | | |
| Member 360 relationship scorecard (self-service) | | | | | |
| Member-facing portal (Lakebase/GraphQL, from Session 4) | | | | | |
| Genie self-service for analysts (from Session 3) | | | | | |

**Guidance to say:** "Recommended first pilot is the one that's highest value *and* already data-ready
*and* low governance risk. Given today's data, **advance concentration / collateral risk monitoring** is
the natural first pilot — the gold tables exist, the questions are executive-relevant, and it's
internal-only so governance is straightforward. Analyst Genie self-service (Session 3) is the enabling
capability underneath it. It also **directly relieves two of your stated pains**: it **displaces manual,
batch-built risk reports** (freeing your limited engineering capacity) and it proves the governed pattern
before you take on broader change like reducing ADF reliance in the pipeline estate (Session 2B)."

## 5. Phased adoption path + success measures (45–55 min)

**Say — the phased path (foundations before broad exposure):**

1. **Platform foundations** — UC governance, classification, AI Gateway prereqs (Session 1 action list).
   *Success:* classification taxonomy enforced; system-table access stood up; AI Gateway policy agreed.
2. **Governed technical pilot** — the first prioritized use case on governed gold tables, curated Genie
   space, validated numbers. *Success:* pilot questions answered correctly and repeatably; sign-off from
   a risk/finance SME.
3. **Analyst enablement** — the Session 3 pattern rolled to a defined analyst group; self-service Genie +
   dashboards on curated domains. *Success:* N analysts building their own spaces; reduced ad-hoc report
   requests.
4. **Controlled business exposure** — broaden Genie/dashboards to business users on approved domains with
   sharing + retention policy in place. *Success:* leaders self-serve the priority questions; adoption +
   trust metrics.

**Capture success measures** for the first pilot specifically (e.g. "top-5 concentration answerable in
<10s by a non-analyst," "collateral-stale list refreshed weekly," "zero governance exceptions").

## 6. Owners + next checkpoint (55–60 min)

| Workstream | Owner | Next step | Checkpoint |
|---|---|---|---|
| Data & pipelines (target-state, Lakeflow Connect) | _(capture)_ | from Session 2B | |
| Governance & AI readiness | _(capture)_ | from Session 1 action list | |
| Platform / workspace + system-table access | _(capture)_ | | |
| Application databases (Lakebase/GraphQL) | _(capture)_ | from Session 4 | |
| Analyst enablement & Genie pilot | _(capture)_ | first pilot use case | |

**Close:** "Agree the recommended first pilot, its owner, and the date of the next checkpoint after this
engagement. Everything else on the roadmap sequences behind foundations — that's deliberate."

---

## Likely Q&A

- **"Can we trust Genie's numbers?"** Yes when the space is *curated* — governed tables, defined metrics,
  validated sample questions. That curation is the pilot work; ungoverned Genie on raw data is where
  trust breaks, which is why we sequence.
- **"When can everyone have Genie?"** After foundations + a governed pilot prove it. Broad exposure is a
  governance decision (domains, sharing, retention), not a switch.
- **"What's the fastest path to value?"** The first prioritized pilot on data that already exists —
  concentration/collateral monitoring — because the gold tables and governance are already there.
- **"How do we measure success?"** The pilot success measures captured above — answerability, freshness,
  zero governance exceptions, adoption.
- **"What do we owe you before the next session?"** The pre-work items: AI Gateway confirmation, workspace
  for demos, candidate app profile (Session 4), and the priority questions confirmed here.

## Outcomes (agenda checklist)

- [ ] **Prioritized use-case backlog + recommended first pilot** — the matrix, with concentration/collateral
      monitoring as the likely first pilot.
- [ ] **Phased roadmap** across data, governance, platform, application databases, and business enablement.
- [ ] **Named owners + concrete next steps** — the workstream table + agreed next checkpoint.

---
**End of day.** Thank participants; confirm the follow-up owner sends the consolidated action list from
all five sessions within the engagement window.
