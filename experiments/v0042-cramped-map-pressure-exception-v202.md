# v202 — cramped-map pressure exception

## Replay basis and objective

The v201 seed-166 losses showed that compact maps need early pressure, while
high-ranking winners still converted that pressure into a route shell. v202
kept the designated primary attacker on the immutable v0042 offense when the
mirrored Core distance was within `CRAMPED_CORE_DIST`; on wider maps it used
the v201 bounded opening economy handoff. No map-name branch or combat policy
changed.

## Scope

- Temporary source: `bots/candidate/main.py` and one opening-phase constant in
  `bots/candidate/bot/constants.py`.
- Temporary focused coverage: `tests/test_candidate_cramped_opening.py`.
- Regression screen: all 15 maps with `configs/eval_regression.toml` rotated
  from seed 166 to seed 167.
- No Launcher, Barrier, hijack, sabotage, route-geometry, turret, ammo,
  baseline, package, upload, activation, or live-state change.

## Validation and replay evidence

- The initial map-context implementation passed focused **27/27** combined
  phase/nearest-defense coverage, compileall, static with only inherited
  failures, and smoke **4/4**. The seed-167 screen was **9-6** for the
  candidate and 15/15 command-clean with zero TLE/suspicious output, but
  Royale (Core distance 14) had only one Harvester and no candidate delivery.
  Candidate first delivery was missing on one row; max p99/peak were
  **1,242/2,881 us**. Report:
  `reports/local-20260818T133357Z`; analysis:
  `reports/iter-v202-cramped-opening-replay-analysis.json`.
- One bounded repair preserved the initial compact-map pressure window, then
  lent the primary attacker to economy at round 24 when no completed route
  existed. Focused coverage was **28/28**, compileall passed, static retained
  the inherited exit 2, and smoke was **4/4**. The identical seed-167 screen
  removed the no-delivery row but fell to **5-10**. It was 15/15
  command-clean with zero TLE/suspicious output; max p99/peak were
  **1,300/2,466 us**. Report:
  `reports/local-20260818T133817Z`; analysis:
  `reports/iter-v202-cramped-opening-repair-replay-analysis.json`.

## Decision and rollback

Reject v202 after the permitted repair. The compact-map exception produced a
non-causal **9-6** first screen, and the route-failure fallback repaired
reliability but lost the paired edge at **5-10**. Restore candidate Python to
recursive parity with immutable v0042. Rollback nearest-defense was **23/23**,
compileall passed, static retained the inherited exit 2, and rollback smoke
was **4/4** at `reports/local-20260818T134031Z`. No release gate, package,
upload, activation, or baseline transition occurred.

## Replay conclusion

Pressure and route conversion must be coordinated by live route/Barrier state,
not only by Core distance and a fixed round fallback. Keep v0042 as the local
baseline and use the next replay/top-team hypothesis to improve early route
stock without repeating a primary-attacker phase handoff.
