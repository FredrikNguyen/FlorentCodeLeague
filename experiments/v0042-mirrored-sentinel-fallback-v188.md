# v188 delayed mirrored-Sentinel fallback — rejected 2026-08-18

## Objective

On long geometry, let only a fixed attacker place a single forward Sentinel at
the symmetric enemy-Core estimate after the stage-2 round, three completed
routes, and a dynamic Sentinel-plus-attack reserve. This targeted maps where
the v0042 release analysis showed fewer Sentinels and weaker wins than the
comparator while direct Core sighting was delayed.

## Scope and non-goals

- Temporary changes were limited to `bots/candidate/bot/attacker.py`, one
  focused Sentinel test, and the rotated `screen_seed` in
  `configs/eval_regression.toml`.
- Cramped-map behavior, dynamic-worker Sentinel behavior, confirmed-intel
  placement, routes, workforce, barriers, Launcher/Splitter behavior, baseline
  snapshots, packaging, upload, activation, and live state were not changed.

## Validation

- Focused checks were **25/25**, candidate compileall passed, and smoke was
  **4/4 command-clean**. `make static` retained the inherited 15 obsolete
  module import errors and two navigation fast-path assertions.
- The seed-157 15-game all-map screen was **4-11**, 15/15 command-clean, with
  candidate/comparator collection **53,060/89,570 Ti**. Replay analysis found
  no TLE or suspicious output. Report: `reports/local-20260818T093130Z`;
  analysis: `reports/iter-v188-mirrored-sentinel/replay-analysis.json`.
- Replay review showed no candidate Sentinel on several losses and reduced
  Harvester counts on games where the fallback did fire; it did not provide a
  reliable long-map pressure edge.

## Decision and rollback

Reject after the decisively negative screen; no repair was warranted because
the causal failure was early economy displacement rather than a placement
detail. The temporary attacker logic and test were removed; candidate
`attacker.py` is byte-identical to immutable v0042. Rollback focused checks
were **28/28**, compileall passed, and rollback smoke was **4/4**:

- `reports/iter-v188-mirrored-sentinel/rollback-focused.log`
- `reports/iter-v188-mirrored-sentinel/rollback-compileall.log`
- `reports/iter-v188-mirrored-sentinel/rollback-smoke.log`

No release gate, package, remote gate, upload, activation, or baseline
transition occurred. The 15-map quick screen remains the routine gate and the
release gate remains 60 games. Platform v105 is still active-observing with
v101 as rollback.
