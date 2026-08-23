# v213 — adaptive pressure handoff (approved)

## Replay basis

The v212 continuous-offence pulse scored **33-27** in the 60-game gate, but
losses repeatedly had zero or one surviving Sentinel, only two-to-five
Harvesters, and late/no delivery on Icefloe, Drakkarfjord, Royale, and Nordkap.
The pulse is useful on some maps but commits pressure without a live shell or
adequate conversion. v0042 remains the release baseline; the current v212
candidate is the local challenger.

## Approved bounded hypothesis

Use existing observations to make the fixed-attacker pressure state adaptive.
When delivery is late or no forward Sentinel is alive, one designated attacker
hands off to the nearest safe route/economy support lane; when a recent delivery
and live forward Sentinel are visible again, it re-enters the existing offense
pulse. Preserve reserve, nearest ownership, danger, and action-legality gates.

## Allowed files

- `bots/candidate/bot/attacker.py`;
- one focused adaptive-handoff test module;
- one existing signal constant only if essential;
- this record, `UPDATES.md`, `docs/CURRENT_PLAN.md`, and report/state metadata.

## Non-goals

No Store schema/slot, new delivery milestone, Launcher/Sentinel cap change,
map-name branch, fixed reserve increase, dynamic-builder rewrite, route
geometry, baseline/archive/package, upload, activation, or live-state change.

## Done criteria

Focused tests cover late-delivery handoff, live-Sentinel continuation, nearest
fixed-attacker ownership, danger/legality gates, and re-entry to offense;
compileall/static/smoke retain the inherited profile. A fresh all-map screen
must be command-clean and delivery-clean, improve the Icefloe/Nordkap floor,
and retain a clear aggregate edge over exact v0042 and the v212 candidate.
Run the 60-game gate only after that screen; otherwise restore exact pre-v213
parity and do not promote.

## Implementation and screen result

Luna added only `_adaptive_pressure_handoff` in `bots/candidate/bot/attacker.py`
and five focused tests in `tests/test_candidate_adaptive_pressure.py`. The
handoff is limited to a designated nearest fixed attacker, visible damaged
Harvester/Conveyor/Splitter repair, strict-progress danger-safe movement, and
the existing live-Sentinel/three-Harvester return gate. Focused coverage was
**5/5** and candidate compileall passed. `make smoke` was **4/4**;
`make static` retained the inherited exit 2 (obsolete deleted-module imports
and two navigation fast-path assertions) with no v213-specific failure.

The fixed seed-178 all-map screen was command-clean and delivery-clean (**8-7**
candidate-side, 0 TLE, 0 suspicious output, 0 no-delivery rows), improving on
the exact v212 snapshot's **5-10**. However, collection trailed v0042
(**94,090 vs 100,370 Ti**), and the protected Nordkap floor remained **0-1**;
Icefloe was **1-0**, not an improvement over the prior v212 screen. Mean first
delivery was **28.4 vs 30.0** rounds and max p99/peak were **1,388/2,557 us**.
Because the required Icefloe/Nordkap floor and clear paired edge were not
both satisfied, no 60-game gate was run.

## Decision

Reject v213 and restore exact pre-v213 parity. The adaptive handoff is not
promoted, packaged, uploaded, activated, or made the baseline; v0042 remains
the immutable baseline. Preserve the screen artifacts in
`reports/local-20260818T170142Z`,
`reports/iter-v213-adaptive-pressure/edited-screen-replay-analysis.json`, and
`reports/iter-v213-adaptive-pressure/static.log`.
