# v193 — confirmed-enemy spawn ordering

## Objective

Test whether fixed attacker and defender Builders should use a role-aware
spawn-ring order when an enemy Core is directly visible, while preserving the
existing opening when no enemy geometry is confirmed.

## Scope and non-goals

The temporary change was limited to `bots/candidate/bot/core_role.py`, one
focused spawn-order test module, and the rotated quick-screen seed. Economy,
routes, combat, workforce, navigation, costs, baseline, archive, and live
state were out of scope.

## Evidence

- Focused tests: 42/42; compileall passed; smoke was 4/4 command-clean.
- `make static` exited 2 on inherited missing legacy modules and two
  navigation fast-path assertions; no v193-specific failure was observed.
- Seed-161 initial screen: 6-9, candidate/comparator titanium 62,680/89,480,
  15/15 command-clean (`reports/local-20260818T104146Z`).
- Repair 1 restored the prior shuffled opening when enemy geometry was absent:
  8-7, titanium 85,120/78,390, one candidate zero-delivery row
  (`reports/local-20260818T104637Z`).
- Same-schedule repeat: 9-6, titanium 74,060/82,360, no zero-delivery rows
  (`reports/local-20260818T104907Z`).
- The exact repair source was reconstructed for the requested release gate.
  The 60-game endpoint-seed matrix was **29-31**, titanium **291,120/322,530**,
  with zero no-delivery rows and 60/60 command-clean games
  (`reports/local-20260818T110738Z`). Per-map floors included 1-3 on
  Auroraveil, Fjordgate, Frostgate, Midgard, and Nordkap.
- All replay analyses reported zero TLE/suspicious-output rows; reports are
  under `reports/iter-v193-deterministic-spawn/`.

## Decision

Reject. The direct-enemy case is rare and the apparent repair edge was not
stable across the repeated screen; the two repair screens combined to 17-13
with slightly lower total titanium, and the requested 60-game gate was 29-31
with lower collection and weak map floors. The helper and focused tests were
removed, and `bots/candidate` is recursively identical to immutable v0042. No
release, package, upload, activation, or baseline transition occurred.

## Follow-up

The next isolated hypothesis is late-game offensive staging: ration forward
offensive units, retire an obsolete live offensive position only when a safe
replacement is ready, and advance the pressure frontier one confirmed stage at
a time. It must not change opening economy or be mixed into this checkpoint.
