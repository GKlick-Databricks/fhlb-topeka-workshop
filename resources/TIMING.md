# Timing — plan honestly

Stated per-module times are **optimistic for beginners** and **padded on setup/UC**. Give a range and use
the stretch modules as overflow so a fast room never sits idle.

## Reference (a ~4-hour, beginner "Core" build)
| Module | Buffered / mixed beginners | Fast / technical room |
|---|---|---|
| 01 setup | 20m (buffer for access/stragglers) | ~10m |
| 02 explore UC | 35m | ~20–25m |
| 03 pipeline | 60m ⚠️ biggest variable | 45–60m (build + run + investigate) |
| 04 SQL | 40m | ~30m |
| 05 Genie | 25m | ~20m |
| 06 dashboard | 35m | ~30m |
| **Core** | **~3h35m** | **~2h45–3h** |
| + close/wrap | ~20m | ~20m |

- A **2-hour** cut = the same Core, streamlined (shorter UC, tighter pipeline, app/ML→stretch); expect it to
  actually land ~2h15–20 to finish the dashboard. Say so; don't pretend it's a clean 2:00.
- The **pipeline module is the swing factor.** For a hard stop, demo Path 1 once and have everyone Run-All the
  SQL fallback (~30s). Protect time for Genie + dashboard + the close.
- **Fast rooms finish Core early** — that's expected. Queue the stretch (app → gold-buildout → ML → treasure
  hunt) so there's always a next thing. The workshop is deliberately over-provisioned.
- **Live friction costs real minutes** (prefix config, picking UC-enabled/serverless compute, access). Budget
  for it; the prefix guard + fallbacks are what keep it from stalling.
- If lunch is a real break (not working), it's on top of the content time.
