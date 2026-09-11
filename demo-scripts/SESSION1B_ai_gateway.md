# Session 1b — Unity AI Gateway (live demo)

**Slots into:** Session 1 — Governance, Security & AI Readiness (8:15–9:00) · **Presenters:** Gabe / Zoeb
**Audience:** Security, Innovation, Platform, IT
**Companion notebook:** `notebooks/05_ai_gateway_demo.ipynb` (runnable, self-tearing-down)

> The agenda flags that 45 min is tight for both UC governance *and* AI Gateway. This demo is
> built to run in **~8–10 min** as the AI-readiness capstone of Session 1 — or to lift into its
> own slot if you split AI Gateway out (the doc comments suggested that option).

---

## Why this matters (30-sec frame)
"Before we open models or Genie to the business, Security and IT need three guarantees:
**member PII can't leak into a prompt, spend is capped, and every call is audited.** Unity AI
Gateway gives you all three as one governed control plane in front of every model — the same
way Unity Catalog governs your data." Tie back to the Session 1 governance framework.

## What's been validated
Every step below was run live in `fevm-serverless-stable-6fhczt` during prep:
- benign question → **200**, answered;
- member PII (SSN + phone) → **blocked** (`input_guardrail_triggered`, phone masked to `<PHONE_NUMBER>`);
- 5/min rate limit → **5 × 200 then 429**;
- all calls logged to `system.serving.endpoint_usage`.

## Safety note (say it out loud)
"I'm **not** touching the shared Foundation Model endpoints — a rate limit there would throttle
the whole workspace. I've created a **dedicated, throwaway endpoint** that just fronts one FM
endpoint through the gateway, and the last cell deletes everything." (No GPU; comes up in seconds.)

---

## Run of show

| # | Do | Say / watch for | ~time |
|---|----|-----------------|-------|
| 0 | Run **config** + **setup** cells | "Minting a 24-hour token, storing it as a secret — presenter setup, revoked at the end." | 1 min |
| 1 | Run **create** cell | "One call stands up the endpoint *and* attaches the policy: guardrails, a 5/min rate limit, usage logging." Show `state: READY`. | 1 min |
| 2 | Run **Step 2** (benign) | "A normal FHLB question flows through — and it's now on the audit trail." | 1 min |
| 3 | Run **Step 3** (PII) — the money shot | "Watch what happens when a member's SSN and phone go into the prompt." Read out `finishReason: input_guardrail_triggered`, `pii_detection: true`, and the masked phone. **Pause here — this is the headline.** | 2 min |
| 4 | Run **Step 4** (rate limit) | "Fire 8 at once — five get through, the rest are 429'd. Cost and abuse control, enforced centrally." Show `{200: 5, 429: 3}`. | 1 min |
| 5 | Run **Step 5** (audit) | "Every call — allowed, blocked, rate-limited — lands in a governed system table with the requester and status code." Point at the `429` rows. (Logs land within a few minutes; if empty, note it populates shortly.) | 2 min |
| 6 | Talk to the **governance talking points** MD cell | Access control + fallbacks (shown as config), AI Gateway prerequisites. | 1 min |
| 7 | Run **teardown** | "And it's gone — endpoint, secret, token all removed." | 30 sec |

## Likely questions
- **"Does the guardrail see our data?"** PII detection runs in the gateway on the request/response
  text; blocked requests never reach the model. Discuss where guardrail processing runs and your
  data-residency requirements as a ⚠️ confirm item.
- **"Can we mask instead of block?"** Yes — guardrail behavior can mask/anonymize rather than
  hard-block; we set `BLOCK` for a clear demo. (Note the response already shows an `anonymized_input`.)
- **"Per-user rate limits?"** The limit key can be per-endpoint or per-user; we used per-endpoint.
- **"Which models can we govern this way?"** External-model, provisioned-throughput, and
  pay-per-token endpoints all support AI Gateway. FM API endpoints already have usage tracking on.
- **"How does this relate to Genie governance?"** Same principle — govern the access path; Genie
  respects UC permissions on the data, AI Gateway governs the model calls.

## AI Gateway prerequisites (the action-list input for Session 1)
- An endpoint to govern (FM API endpoints are pre-provisioned in every workspace).
- Permission to configure gateway policies on endpoints.
- For a fronted external-model endpoint: a token stored in a secret scope.
- Decide policy defaults: guardrail behavior (block vs mask), rate-limit keys/limits, and that
  usage tracking is on for auditability. Assign an **owner** for gateway policy + the audit review.

## Outcomes (Session 1 checklist)
- ☐ Demonstrated PII guardrail, rate limit, and audit logging on governed model access.
- ☐ Captured AI Gateway prerequisites + policy defaults with an owner.
- ☐ Confirmed the "govern the access path before broad exposure" principle for Genie/model rollout.
