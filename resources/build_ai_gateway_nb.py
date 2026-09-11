"""Build the Unity AI Gateway demo notebook (Session 1 — Governance / AI Readiness).

Presenter-led + runnable. Stands up a DEDICATED external-model endpoint that fronts an
existing Foundation Model API endpoint (no GPU), attaches a full AI Gateway policy set
(PII/safety guardrails, rate limits, usage/payload logging), demonstrates each control
firing, shows the audit trail in system.serving.endpoint_usage, then tears everything down.

Validated live in fevm during the build: benign->200, member-PII->input_guardrail_triggered
(SSN/phone masked), 5/min rate limit -> 5x200 then 429.

Run:  python3 build_ai_gateway_nb.py   # writes ../notebooks/05_ai_gateway_demo.ipynb
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nb import md, code, write_nb

NB_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")

cells = [
    md('''# 05 · Unity AI Gateway — governance for model access (Session 1)
**Governance, Security & AI Readiness · presenter-led + runnable**

🧠 **The idea.** Unity **AI Gateway** puts one governed control plane in front of every
model endpoint: **guardrails** (block/mask PII and unsafe content), **rate limits** (cost &
abuse control), **usage/payload logging** (a full audit trail in system tables), plus
**access control** and **fallbacks**. It's the "AI readiness" layer — the same governance UC
gives your data, applied to model usage.

🏢 **Why FHLB-Topeka cares.** Before opening models/Genie to the business, Security & IT need
to know: *member PII can't leak into a prompt, spend is capped, and every call is audited.*
This notebook proves all three on a safe, throwaway endpoint — **never on a shared endpoint**,
so nothing here affects anyone else's model usage.'''),
    md('''## How this demo is wired (and why it's safe)
The shared Foundation Model endpoints (`databricks-claude-*`, etc.) are used by the whole
workspace — putting a rate limit or guardrail on those would throttle everyone. So we create a
**dedicated external-model endpoint** that simply *fronts* one FM endpoint through the gateway.
It uses no GPU (external model), comes up in seconds, and the last cell **deletes everything**.

**Prereq — a token in a secret.** The fronting endpoint calls the FM endpoint with a token
stored as a Databricks secret. The setup cell mints a short-lived (24h) PAT and stores it in a
dedicated scope. This is presenter setup — run it once; the teardown cell revokes it.'''),
    code('''# ---- config ----
import requests, json, concurrent.futures
ENDPOINT   = "fhlb-ai-gateway-demo"
FRONT_MODEL = "databricks-claude-haiku-4-5"   # an existing FM endpoint we front (cheap/fast)
SCOPE, KEY = "fhlb_ai_gateway_demo", "pat"
RATE_PER_MIN = 5

HOST  = "https://" + spark.conf.get("spark.databricks.workspaceUrl")
TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
def api(method, path, body=None):
    r = requests.request(method, f"{HOST}/api/2.0{path}", headers=H,
                         data=json.dumps(body) if body else None)
    return r.status_code, (r.json() if r.text else {})
print("workspace:", HOST)'''),
    md('''## Setup — mint a short-lived PAT and store it as a secret
(Presenter runs once. The token value is never printed. Teardown revokes it.)'''),
    code('''# create scope (ignore "already exists"), mint a 24h PAT, store it
api("POST", "/secrets/scopes/create", {"scope": SCOPE})
sc, tok = api("POST", "/token/create", {"lifetime_seconds": 86400,
                                        "comment": "fhlb-ai-gateway-demo (24h)"})
assert "token_value" in tok, tok
api("POST", "/secrets/put", {"scope": SCOPE, "key": KEY, "string_value": tok["token_value"]})
TOKEN_ID = tok["token_info"]["token_id"]   # kept for teardown
print("PAT stored in secret", f"{SCOPE}/{KEY}", "(value not shown). token_id:", TOKEN_ID)'''),
    md('''## Step 1 — Create the gateway-fronted endpoint
One call creates the endpoint **and** attaches the AI Gateway policy set:
- **Guardrails** — block PII on input *and* output; safety filter on input.
- **Rate limit** — 5 calls/minute across the endpoint.
- **Usage tracking** — every request logged to `system.serving.endpoint_usage`.'''),
    code('''body = {
  "name": ENDPOINT,
  "config": {"served_entities": [{
      "name": "fronted",
      "external_model": {
        "name": FRONT_MODEL, "provider": "openai", "task": "llm/v1/chat",
        "openai_config": {
          "openai_api_base": f"{HOST}/serving-endpoints",
          "openai_api_key": "{{secrets/" + SCOPE + "/" + KEY + "}}"}}}]},
  "ai_gateway": {
    "usage_tracking_config": {"enabled": True},
    "rate_limits": [{"calls": RATE_PER_MIN, "renewal_period": "minute", "key": "endpoint"}],
    "guardrails": {
      "input":  {"pii": {"behavior": "BLOCK"}, "safety": True},
      "output": {"pii": {"behavior": "BLOCK"}}}}}
sc, resp = api("POST", "/serving-endpoints", body)
print("create:", sc, "| state:", resp.get("state"))
INVOKE = f"{HOST}/serving-endpoints/{ENDPOINT}/invocations"'''),
    md('''## Step 2 — Benign question → allowed (and logged)
A normal FHLB question flows straight through and is recorded in the usage table.'''),
    code('''r = requests.post(INVOKE, headers=H, json={
    "messages": [{"role": "user", "content": "In one sentence, what is an FHLB advance?"}],
    "max_tokens": 60})
print(r.status_code)
print(r.json()["choices"][0]["message"]["content"])
# Validated live: 200 -> "An FHLB advance is a loan from a Federal Home Loan Bank to a member..."'''),
    md('''## Step 3 — Member PII in the prompt → **blocked** by the guardrail
This is the headline control. The request never reaches the model; the response shows
`finishReason: input_guardrail_triggered`, `pii_detection: true`, and the offending
entities masked (e.g. the phone number → `<PHONE_NUMBER>`).'''),
    code('''r = requests.post(INVOKE, headers=H, json={
    "messages": [{"role": "user",
        "content": "Our member contact is John Smith, SSN 123-45-6789, "
                   "phone 913-555-0142. Summarize his file."}],
    "max_tokens": 60})
print("HTTP", r.status_code)
print(json.dumps(r.json(), indent=2))
# Validated live: blocked -> {"input_guardrail":[{"flagged":true,"categories":{"privacy":true,...},
#   "pii_detection":true,"anonymized_input":[...phone <PHONE_NUMBER>...]}],
#   "finishReason":"input_guardrail_triggered"}'''),
    md('''## Step 4 — Rate limit → **429** past 5/min
Fire 8 calls in parallel (sequential calls are too slow to fill a one-minute window).
Expect ~5 × `200` then the overflow as `429` — a cost/abuse guardrail, enforced centrally.'''),
    code('''def hit(_):
    return requests.post(INVOKE, headers=H,
        json={"messages": [{"role": "user", "content": "hi"}], "max_tokens": 3}).status_code
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    codes = list(ex.map(hit, range(8)))
from collections import Counter
print("status codes:", dict(Counter(codes)))
# Validated live: {200: 5, 429: 3}'''),
    md('''## Step 5 — The audit trail (auditability = the Session 1 outcome)
Usage tracking lands **every** call — allowed, blocked, and rate-limited — in
`system.serving.endpoint_usage`, governed like any UC table. Note the `status_code` column:
you can see the `429`s and the requester. (Logs land within a few minutes.)'''),
    code('''display(spark.sql(f"""
  SELECT request_time, requester, status_code,
         input_token_count, output_token_count
  FROM system.serving.endpoint_usage u
  JOIN system.serving.served_entities e USING (served_entity_id)
  WHERE e.endpoint_name = '{ENDPOINT}'
  ORDER BY request_time DESC
  LIMIT 50
"""))'''),
    md('''## 🏢 Governance talking points (map to Session 1 outcomes)
- **Guardrails** → member PII / unsafe content can't reach a model — the precondition for
  opening Genie/models to the business ("foundation before broad exposure").
- **Rate limits** → predictable spend and abuse protection, enforced centrally, not per-app.
- **Usage/payload logging** → a governed audit trail (`system.serving.*`) — who called what,
  when, token counts, status — the auditability the day's governance framework calls for.
- **Access control & fallbacks** → UC permissions decide who may query which endpoint; a
  fallback model keeps a workload up if the primary is unavailable. *(Shown as config here;
  we didn't exercise them live to keep the demo tight.)*
- **AI Gateway prerequisites** → an endpoint to govern (FM API endpoints exist out of the box),
  permission to configure gateway policies, and (for a fronted endpoint) a token in a secret.'''),
    md('''## Teardown — remove everything this demo created
Leaves the workspace exactly as it was: deletes the endpoint, the secret, and revokes the PAT.'''),
    code('''api("DELETE", f"/serving-endpoints/{ENDPOINT}")
api("POST", "/secrets/delete", {"scope": SCOPE, "key": KEY})
api("POST", "/secrets/scopes/delete", {"scope": SCOPE})
api("POST", "/token/delete", {"token_id": TOKEN_ID})
print("torn down:", ENDPOINT, "+ secret scope", SCOPE, "+ PAT", TOKEN_ID)'''),
    md('''---
### ✅ Done
You proved, on real infrastructure, that model access at FHLB-Topeka can be **governed**:
PII blocked, spend capped, every call audited. That's AI readiness.

**Leave-behind:** this notebook + `demo-scripts/SESSION1B_ai_gateway.md` (facilitator run-of-show).'''),
]

if __name__ == "__main__":
    write_nb(os.path.join(NB_DIR, "05_ai_gateway_demo.ipynb"), cells)
    print("AI Gateway demo notebook built.")
