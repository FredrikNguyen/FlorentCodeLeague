# v334 coordinated three-Launcher relay — rejected

Date: 2026-08-20

## Objective and replay basis

The top-team winner sample averaged roughly five Builders, five Harvesters,
fourteen Barriers, three Launchers, and three-to-four Sentinels, while the
retained v0045 sample averaged one Launcher and substantially more route
workforce.  v334 tested one structural part of that composition: distribute a
home Launcher relay across the two fixed attackers and one local dynamic
support Builder instead of letting only the primary attacker own the relay.

## Scope

Production scope was limited to `bots/candidate/main.py`,
`bots/candidate/bot/constants.py`, `bots/candidate/bot/attacker.py`, and
`bots/candidate/bot/dynamic.py`; focused additions were in
`tests/test_candidate_v319_launcher.py`.  The relay cap was three visible own
Launchers near the Core.  The primary relay retained its existing opening
reserve; the second fixed attacker required one completed route; the dynamic
support claimant required one completed route, a deterministic local-ID
ownership check, and a Harvester/two-Conveyor/offensive reserve.  Existing
Launcher actions, route FSM, spawning, Sentinel/Gunner/Barrier policy, Store
layout, baseline snapshots, and platform state were non-goals.

## Validation

- Focused relay, nearest-defense, and economy coverage passed **39/39**;
  `reports/iter-v334-launcher-coordination-focused.log`.
- Candidate compileall passed;
  `reports/iter-v334-launcher-coordination-compileall.log`.
- `make static` retained the inherited repository profile: **15** obsolete
  removed-module imports and **2** navigation fast-path assertions; no
  v334-specific error appeared in
  `reports/iter-v334-launcher-coordination-static.log`.
- Smoke was **4/4 command-clean** at
  `reports/local-20260820T050249Z`.
- The rotated 15-map screen against immutable v0045 was command-clean but
  decisively negative: **4-11 candidate-A**, mean collection about
  **3,962 vs 5,103 Ti**, mean first delivery **34.2 vs 30.5** rounds.  The
  replay set is `reports/local-20260820T050329Z`; parsed diagnostics are in
  `reports/iter-v334-launcher-coordination-replay-analysis.json`.

Replay inspection found the intended relay did not form reliably: almost every
map still had one candidate Launcher, while Yulerune overbuilt five.  The
extra relay did not compensate for lower Harvester/conveyor conversion and
introduced an unstable duplicate-claim shape.

## Decision and rollback

Reject v334 without a repair or longer gate.  The temporary source and focused
tests were removed; production source is recursively byte-identical to
immutable v0045 (excluding generated `__pycache__` artifacts).  Rollback
focused coverage passed **36/36** at
`reports/iter-v334-launcher-coordination-rollback-focused.log`, rollback
compileall passed, and rollback smoke was **4/4** at
`reports/local-20260820T050843Z` (`reports/iter-v334-launcher-coordination-rollback-smoke.log`).
No package, upload, activation, promotion, or live-state transition occurred.

## Remaining risk

Launcher count alone is not the missing control primitive.  The next
experiment must address route conversion and defensive topology with explicit
finite ownership/expiry, not widen this relay quota or let multiple local
workers race a delayed global state.
