# v313 phase-adaptive runtime roles — rejected after one repair

Date: 2026-08-20

## Objective and hypothesis

The top-team audit showed a shared phase machine with explicit economy,
repair, raider, and siege roles.  The v0044 candidate instead made every
Builder's attacker/dynamic designation permanent.  v313 tested a structural
runtime handoff: the Core's existing delayed economy phase temporarily routed
ungraduated attackers and dynamic workers through the normal SCOUT/CHAIN
economy loop; a Builder graduated after completing its own route, while the
permanent Defender floor remained unchanged.  This was intended to convert
the opening workforce before pressure rather than leave workers in a dead-end
combat role.

The bounded repair released the designated primary attacker after four
completed routes (except during the Core's CRISIS phase), restoring one
offensive lane while leaving ungraduated dynamic workers on conversion.

## Scope and non-goals

Temporary production files were `bots/candidate/main.py`,
`bots/candidate/bot/defender.py`, and `bots/candidate/bot/constants.py`.
Focused coverage was `tests/test_candidate_runtime_roles.py` plus the
existing nearest-defense, economy-phase, and seeded-route suites.

No baseline or immutable snapshot, Store layout, route geometry, Launcher or
other unit purchase policy, map branch, package, upload, activation, or live
state changed.  The official v15 top-team source was benchmarked separately
as evidence (`reports/local-20260820T000931Z`) but was not copied into the
candidate; it lost 1-14 to v0044 on the one-sided 15-map diagnostic.

## Validation

- Initial focused coverage: **38/38**; candidate compileall passed.
- Initial `make static`: inherited exit **2** (15 obsolete removed-module
  imports and two navigation fast-path assertions); no v313-specific static
  error.
- Initial smoke: **4/4** command-clean at
  `reports/local-20260820T001627Z`.
- Initial rotated 15-map screen: **4-11** candidate-A, 14/15 candidate
  deliveries versus 15/15, zero TLE/suspicious rows, collection
  **55,840/76,200 Ti**, and first-delivery means **25.50/23.33** turns.
  Report: `reports/local-20260820T001658Z`.
- Bounded repair focused coverage: **40/40**; compileall passed; static kept
  the inherited profile; smoke was **4/4** at
  `reports/local-20260820T001945Z`.
- Repair screen: **6-9** candidate-A, 15/15 deliveries on both sides, zero
  TLE/suspicious rows, collection **74,290/94,870 Ti**, first-delivery means
  **26.07/37.13**, and max p99/peak callback times **1,328/3,021 us**.
  Report: `reports/local-20260820T002007Z`.

## Decision and rollback

The repair removed the no-delivery row and improved the first screen, but it
still lost the paired screen and trailed the comparator in collection and
delivery latency.  The hypothesis therefore failed the win-rate/economy
criterion after its one permitted repair; no long gate or release was run.

All temporary production and test edits were removed with `apply_patch`.
Recursive source parity with immutable v0044 is empty in
`reports/iter-v313-runtime-role/rollback-source-parity.diff` and
`rollback-main-parity.diff`.  Rollback focused coverage was **34/34**,
compileall passed, `make static` retained the inherited exit **2**, and
rollback smoke was **4/4** at `reports/local-20260820T002249Z`.

The current local baseline remains
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`.
Live v107 and the guarded v105 rollback are unchanged.  Do not repeat this
runtime-role handoff or the Launcher family without a new causal replay
signal; the next structural direction should address route conversion or
resource-to-pressure conversion without suppressing the opening workforce.
