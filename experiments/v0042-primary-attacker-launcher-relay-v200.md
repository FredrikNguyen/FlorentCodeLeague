# v200 — reserve-gated primary-attacker Launcher relay

## Objective

Test the early unit-control phase seen in high-ranking replays: let only the
designated primary attacker build a small, dynamic-price Launcher relay, then
let each Launcher throw that attacker to a visible, passable tile that makes
strict progress toward the enemy Core. Route workers were never eligible for
the relay, and the build gate reserved one Harvester plus two Conveyor links.

## Scope and non-goals

- Temporary source: `bots/candidate/main.py`,
  `bots/candidate/bot/attacker.py`, and
  `bots/candidate/bot/constants.py`.
- Temporary focused coverage: `tests/test_candidate_launcher_relay.py`.
- Regression schedule: `configs/eval_regression.toml` screen seed 165.
- No ore/route selector, dynamic task policy, hijacking, sabotage, Sentinel or
  Barrier cap, home-Gunner, ammo, baseline/archive/package, upload, activation,
  or live-state change.

## Validation and replay evidence

- Initial focused coverage was **27/27**, compileall passed, `make static`
  retained only the inherited failures, and smoke was **4/4** at
  `reports/local-20260818T125545Z`.
- The initial seed-165 15-map screen was **6-9** against exact v0042. It was
  15/15 command-clean with zero TLE, suspicious-output, or no-delivery rows;
  max p99/peak were **1,219/5,803 us**. Replay inspection confirmed real
  Launcher/launch events (protobuf field 16 with the primary Builder actor),
  but the candidate built three Launchers on every map, had a first-launcher
  turn of about 2 and a first-delivery mean of about 33, and still lost route
  stock to v0042. Reports: `reports/local-20260818T125715Z` and
  `reports/iter-v200-launcher-relay-replay-analysis.json`.
- One bounded repair reduced the relay cap from three Launchers to one. Repair
  focused coverage remained **27/27**, compileall passed, static retained only
  inherited failures, and smoke was **4/4** at
  `reports/local-20260818T130213Z`. The repaired seed-165 screen fell to
  **5-10**, remained 15/15 command-clean with zero TLE, suspicious-output, or
  no-delivery rows, and max p99/peak were **1,360/6,231 us**. One Launcher per
  candidate map did not create a win-rate edge. Reports:
  `reports/local-20260818T130242Z` and
  `reports/iter-v200-launcher-relay-repair-replay-analysis.json`.

## Decision and rollback

Reject v200 after the permitted repair. The replay event requirement was met,
but the mobility phase did not convert into a paired win-rate improvement and
its first-delivery lag exposed the route-liquidity cost. No release gate,
package, upload, activation, or live transition was justified. The temporary
source and focused test were removed; candidate Python is recursively
byte-identical to immutable v0042. Rollback nearest-defense coverage was
**23/23**, compileall passed, `make static` retained the same inherited exit 2,
and rollback smoke was **4/4** at `reports/local-20260818T130820Z`.

## Replay-backed follow-up

High-ranking replays support early mobility only when it follows a fast route
shell: winners combined first delivery around round 21 with roughly five
Harvesters, fourteen Barriers, and three Launchers. v200's relay was not a
drop-in replacement for that shell. The next hypothesis must explain and fix
the opening delivery/stock gap before another Launcher selector is attempted.
