# v205 — route-funded dynamic forward shell

## Objective

Use replay-observed post-delivery conversion: after three completed routes and
confirmed enemy-Core intel, let the nearest eligible dynamic Builder place a
bounded forward Barrier shell while reserving one Harvester and two Conveyors.
The permanent attacker and active route owners stayed unchanged.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/constants.py` and
  `bots/candidate/bot/dynamic.py`.
- Temporary focused coverage: `tests/test_candidate_dynamic_shell.py`.
- Regression schedule: `configs/eval_regression.toml`, rotated seed 170.
- No opening ore/route selection, failed-chain cleanup, primary attacker,
  Launcher, Sentinel/Gunner/ammo, hijack/sabotage ranking, route geometry,
  Store, baseline, package, upload, activation, or live-state change.

## Validation and replay evidence

- Initial focused coverage was **27/27**, compileall passed, static retained
  the inherited failures, and smoke was **4/4**. The seed-170 screen was
  **6-9**, command-clean with zero TLE/suspicious/no-delivery rows. The new
  task placed real Barriers, but candidate first delivery averaged **44.87**
  versus **22.73** for v0042 and collection was **77,410 vs 72,470 Ti**;
  candidate placed 60 Barriers versus 77. Max p99/peak were **1,299/4,754 us**.
  Reports: `reports/local-20260818T141745Z` and
  `reports/iter-v205-dynamic-shell-replay-analysis.json`.
- One bounded repair changed the phase contract rather than another route
  threshold: a dynamic Builder could claim the shell only while already within
  the forward zone, instead of walking from home. Focused coverage was
  **28/28**, compileall passed, static retained exit 2, and smoke was **4/4**.
  The same screen improved to **7-8**, with candidate first delivery **22.47**
  versus **28.00**, but collection was **62,470 vs 69,320 Ti** and Barrier
  stock was **52 vs 87**. It remained a paired win-rate regression; max
  p99/peak were **1,412/4,023 us**. Reports: `reports/local-20260818T142059Z`
  and `reports/iter-v205-dynamic-shell-repair-replay-analysis.json`.

## Decision and rollback

Reject v205 after the permitted repair: the structural assignment correction
recovered delivery timing but did not beat v0042 and converted less total
resource into durable pressure. The temporary source and test were removed;
candidate production files are recursively byte-identical to immutable v0042.
Rollback nearest-defense was **23/23**, compileall passed, static retained the
same inherited exit 2, and smoke was **4/4**. Logs are under
`reports/iter-v205-dynamic-shell-rollback-*`. No release gate, package,
upload, activation, or live transition was justified.

## Replay follow-up

The high-ranking replay lesson is not “raise a Barrier cap.” Winners combine a
fast route with a coordinated multi-unit assault: early Launchers reposition
Builders, Barriers deny repair access, and Sentinels supply damage while home
Gunners stay sparse. v205 proved that adding one dynamic shell task without a
shared assault phase is insufficient. The next experiment must change the
workforce/phase contract fundamentally—one explicitly coordinated forward
assault lane—rather than add another isolated priority or cost knob.
