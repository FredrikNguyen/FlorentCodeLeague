# v214 — intel-backed offense lease (approved)

## Replay basis

The rejected v213 handoff screen stayed command-clean but its losses exposed a
different failure from the fixed-attacker pulse: on Nordkap, Antler, Royale,
Auroraveil, Archipelago, and Yulerune the candidate kept a route/economy base
but ended with few or no surviving Sentinels and a much smaller defensive or
forward shell than the opponent. The current dynamic task picker also never
consumes the shared enemy-Core store signal; after a route is complete it can
continue selecting visible ore and never reach the existing dynamic Sentinel
conversion path. Top-team replays show the stronger pattern: preserve a small
economy floor, then keep several builders converting the bank into sustained
pressure while the route owner continues delivery.

## Approved bounded hypothesis

Add an intel-backed post-economy offense phase to the existing dynamic role.
Dynamic builders must first consume the already-published enemy-Core sighting.
Once `OFFENSE_MIN_HARVESTERS` is met and that sighting is confirmed, a dynamic
builder in SCOUT mode selects `TASK_ADVANCE` before the ordinary visible-ore
task. Existing higher-priority home threat, belt/base repair, enemy Harvester
hijack, and active CHAIN-mode route work remain unchanged. The existing
`_execute_advance` Sentinel/harass gates are the only pressure actions; no new
weapon, reserve, Store slot, or map branch is introduced.

## Allowed files

- `bots/candidate/bot/dynamic.py` for the shared-intel read and phase ordering;
- one focused dynamic offense-lease/legality test module;
- this experiment record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable
  report/state metadata.

## Non-goals

No new Store slot/schema, new weapon or Barrier policy, Sentinel-cap or reserve
tuning, route-chain rewrite, permanent-role assignment change, fixed-attacker
change, map-name branch, baseline/archive/package, upload, activation, or
live-state change. Do not interrupt an active `MODE_CHAIN` route or an urgent
home-threat/repair/hijack task.

## Done criteria

Focused tests prove shared-Core intel is consumed, the offense lease wins only
after the route milestone and outside CHAIN mode, protected tasks still outrank
it, and all selected actions remain legal. Candidate compileall, static, and
smoke retain the inherited profile. A fresh rotated 15-map screen against the
exact v0042 baseline must be command-clean with no TLE, suspicious-output, or
new no-delivery rows and show a clear aggregate edge without a new protected-
map collapse. Run the 60-game gate only after that screen; otherwise restore
the exact pre-v214 snapshot and do not promote.

## Implementation and gate result

Luna added the bounded `_intel_offense_target` helper and four focused tests.
The helper consumed the existing Store-slot-9 sighting only in SCOUT mode and
only after `OFFENSE_MIN_HARVESTERS`; active CHAIN work and the four protected
task classes remained ahead of it. Focused coverage was **4/4** in Luna's run
and **41/41** in the root regression subset after the implementation; candidate
compileall passed. `make smoke` was **4/4** command-clean at
`reports/local-20260818T172547Z`. `make static` retained the inherited failure
profile (91 discovered tests: 15 obsolete deleted-module import errors and two
navigation fast-path failures), with no v214-specific failure.

The rotated seed-179 all-map screen was command-clean and delivery-clean at
**7-8** candidate-side across all 15 maps, with zero TLE/suspicious-output and
zero no-delivery rows. Candidate collection was **73,200 vs 76,060 Ti**,
mean first delivery **24.87 vs 21.47 rounds**, and max p99/peak execution
**1,354/2,926 us**. Candidate wins were Valkyrie, Frostgate, Auroraveil,
Yulerune, Glacierkeep, Icefloe, and Nordkap; the aggregate edge criterion did
not pass, so the 60-game gate was not run. Screen evidence is in
`reports/local-20260818T172622Z/manifest.json`,
`reports/local-20260818T172622Z/games.json`,
`reports/iter-v214-intel-backed-offense/edited-screen-replay-analysis.json`,
and the focused/static/smoke logs in the same report directory.

## Decision

Reject v214 and restore the exact pre-edit v212 candidate. The dynamic source
hash matches `/tmp/florent-v214-preedit-20260818T171827Z/candidate`; the focused
test and temporary screen config were removed. v0042 remains the immutable
baseline; no release gate, promotion, package, upload, activation, or live
transition occurred.

Rollback verification passed **37/37** retained focused tests and candidate
compileall; the dynamic source hash exactly matches the pre-v214 snapshot.
