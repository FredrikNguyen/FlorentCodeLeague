# v228 archived v208 post-route Launcher lifecycle

## Objective

Evaluate the exact archived v208 candidate as a release candidate against the
immutable v0042 baseline. v208 is the only previously unpromoted candidate with
a documented positive 15-map screen (**9-6**) and observed Launcher movement
events; it was never run through the required 60-game gate.

## Allowed files

- `bots/candidate/main.py` (restored exact archived v208 dispatch/state);
- `bots/candidate/bot/attacker.py` (restored exact archived v208 Launcher
  build/lifecycle);
- one focused v228 Launcher lifecycle test module;
- this experiment record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable
  report/state metadata.

## Non-goals

No new Launcher tuning, opening economy, route FSM, Store schema, workforce or
role policy, Sentinel/Barrier/Gunner/ammo policy, map branch, baseline/archive,
package, upload, activation, or live-state change before the release gate.

## Done criteria

Focused lifecycle/legality tests, compileall, `make static`, and `make smoke`
must retain the inherited runtime profile. The exact v208 candidate must first
pass a fresh 15-map screen against v0042 with no command, delivery, TLE, or
suspicious-output regression. Only then may the complete 60-game map/endpoint-
seed/both-side gate run. Promote only if that gate has a clear paired win-rate
edge with no protected-map or reliability failure; otherwise remove the
temporary source/test and restore exact v0042 parity.

## Source basis

The archived source is `/tmp/fcl-v208-snapshot.XhhR6m`, whose only production
changes from v0042 are a one-shot post-route Launcher purchase by the
designated fixed attacker and an exception-safe Launcher dispatcher. Its prior
screen/replay evidence is retained at `reports/local-20260818T144551Z` and
`reports/iter-v208-launcher-lifecycle/replay-analysis.json`.

## Validation

- Focused v228 lifecycle plus nearest-defense coverage passed **28/28**;
  compileall passed; `make smoke` was **4/4** command-clean at
  `reports/local-20260818T211736Z`; `make static` retained the inherited exit
  2 (15 obsolete imports and two navigation assertions), with no v228-specific
  failure. Logs are under `reports/iter-v228-archived-v208/`.
- The rotated 15-map screen was **10-5** with all deliveries present, zero
  command/TLE/suspicious rows, collection **86,000 vs 67,600 Ti**, mean first
  delivery **31.0 vs 36.33**, and four candidate Launcher placements. Raw
  report: `reports/local-20260818T211807Z`; parsed replay data:
  `reports/iter-v228-archived-v208/replay-analysis.json`.
- The required 60-game endpoint-seed/both-side gate was command-clean with
  zero TLE/suspicious rows but finished **30-30**, collection
  **247,680 vs 232,270 Ti**, candidate/baseline no-delivery **1/1**, and
  maximum p99/peak **1,595/5,250 us**. Candidate mean first delivery was
  **43.0 vs 40.08**; Archipelago and Icefloe were each **2-2** across four
  games, so no protected-map floor was cleared.
  Raw report: `reports/local-20260818T212023Z`; parsed replay data:
  `reports/iter-v228-archived-v208/release-analysis.json`.

## Decision and rollback

The positive short screen did not transfer to a release edge in the complete
gate. The archived
v208 source and temporary focused test/config were removed; candidate Python
is recursively byte-identical to immutable v0042. Rollback focused coverage
was **23/23**, rollback compileall passed, rollback static retained the
inherited exit 2, and rollback smoke was **4/4** at
`reports/local-20260818T212634Z`. No promotion, package, upload, activation,
or live-state transition occurred. Do not retry the one-shot Launcher relay
without new causal evidence for a release-scale win-rate edge.
