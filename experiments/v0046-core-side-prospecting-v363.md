# v363 Core-side opening prospecting — rejected

Date: 2026-08-20

## Objective

Address the recorded late-ore/no-delivery losses on Royale, Glacierkeep,
Frostgate, and other edge-oriented openings without changing the economy FSM,
route builder, combat policy, Store schema, or immutable baseline.  When no
visible or advertised ore exists, v363 tried a bounded deterministic cardinal
waypoint ray from the own Core toward a sufficiently strong outer-board vector.
Builder id and prospect cursor rotated the ray; distance advanced in cycles.
Visible walls/occupied blockers and blacklisted waypoints were skipped, and
the existing grid-stride exploration remained the fallback when no outer ray
was unambiguous.

## Scope and non-goals

Allowed candidate files were `bots/candidate/bot/defender.py` and
`bots/candidate/bot/constants.py`; focused coverage was added temporarily in
`tests/test_candidate_core_prospecting.py`.  Documentation, reports, and
durable state were updated.  No baseline snapshot, Store slot, route FSM,
unit cap, combat policy, map literal, package, upload, activation, or live
state was changed.

## Evidence

- Initial focused coverage was **39/39**; repair coverage was **40/40**.
  Candidate compileall passed.  Both smoke runs were **4/4** command-clean.
  `make static` retained only the inherited 15 obsolete-module imports and
  two navigation fast-path assertions (exit 2).
- Rotated screen 1 (`reports/local-20260820T181133Z`, screen seed 263) was
  **7-8**, command/TLE/suspicious-clean, with **15/15** candidate positive
  collection rows.  The eight losses included Frostgate, Valkyrie, Icefloe,
  Ragnarok, Archipelago, Midgard, Fjordgate, and Antler; the replay analysis
  is `reports/iter-v363-home-side-prospecting/screen1-analysis.json`.
- One bounded repair tightened the outer-ray eligibility to avoid treating a
  half-cell centre tie as an outer direction.  Rotated screen 2
  (`reports/local-20260820T181729Z`, screen seed 271) reached **9-6**, but
  contained one candidate no-delivery row.  The pair therefore finished
  **16-14** and failed both the **19-11** pair gate and the hard delivery gate.
- Screen replays were reliability-clean; the screen logs and all replay
  diagnostics are under `reports/iter-v363-home-side-prospecting/`.

## Decision and rollback

The hypothesis is rejected after the one permitted repair.  Candidate source
was restored to exact recursive v0046 parity; the proof is the empty
`reports/iter-v363-home-side-prospecting/rollback-source-parity.diff`.
Rollback compileall and the 35-test focused suite passed, and rollback smoke
was **4/4** at `reports/local-20260820T182055Z`.  No 60-game release matrix,
remote gate, package, upload, activation, or baseline update ran.  Immutable
v0046 remains the comparator.

## Remaining risk

The opening losses remain dominated by route/workforce conversion rather than
one universal Core-side ray.  Future work should compare actual ore/topology
observations before choosing a prospecting direction, and must not re-enable
this implementation unchanged.
