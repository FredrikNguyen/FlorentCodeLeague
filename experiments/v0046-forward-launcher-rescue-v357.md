# v357 forward Launcher rescue — rejected

Date: 2026-08-20

## Objective

Use the fresh live-v108 Yulerune replay to test one distinct, bounded answer to
the primary attacker oscillating behind the central wall.  After a measured
approach stall and a paying economy signal, the fixed attacker could build one
adjacent, reserve-backed Launcher.  The existing Launcher controller remained
responsible for the `can_launch`-gated, strictly Core-closing throw.

The comparator was immutable
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`.
Live evidence is retained at `reports/live-observe-20260820T140438Z`.

## Scope and implementation

The temporary candidate touched `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and
focused coverage in `tests/test_candidate_nearest_defense.py`.  The single
bounded repair corrected an observed gating defect: a home Launcher six tiles
away was treated as nearby even though the controller can only pick up an
adjacent Builder.  The repair used the actual Chebyshev-adjacent pickup range;
it did not change destination selection, navigation, economy, Store, or unit
targets.

## Results

- Temporary focused coverage was **28/28**, compileall passed, and smoke was
  **4/4**.  `make static` retained the inherited exit-2 profile (15 obsolete
  imports and two stale navigation assertions); no v357-specific static
  failure appeared.
- The initial immutable-v0046 15-map seed-179 screen was **5-10**.
- The one allowed pickup-range repair was command-clean and moved the sampled
  Yulerune run to three candidate Launchers and a candidate win, but the same
  15-map screen was only **7-8**.  There were zero command failures, TLEs,
  suspicious outputs, or candidate delivery failures.
- The required **9-6** first-screen floor was not met.  No rotated screen,
  60-game release matrix, remote gate, package, upload, activation, or
  promotion ran.

## Rollback and evidence

The temporary source and test changes were removed.  Recursive production
parity with immutable v0046 is empty at
`reports/iter-v357-forward-launcher-rescue/rollback-source-parity.diff`.
Rollback focused coverage is **26/26**
(`rollback-focused.log`), compileall is clean (`rollback-compileall.log`),
and rollback smoke is **4/4** at `reports/local-20260820T154942Z`
(`rollback-smoke.log`).  The final static profile remains the inherited
exit-2 result in `rollback-static.log`.

## Decision and remaining risk

Reject v357 and retain immutable v0046 as the local baseline.  The repair
proved that the home-relay proximity guard was overbroad, but the rescue did
not clear the reliability screen.  The live v108 observation remains
`active_observing`; no platform state changed.  Future work needs a distinct
wall-aware mechanism and must preserve the same 9-6, rotated-pair, 60-game,
remote-gate, and live-policy checks.
