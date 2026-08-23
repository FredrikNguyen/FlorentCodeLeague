# v386 verified conveyor-path merge — rejected

## Objective and scope

Starting from immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`,
v386 tested one distinct resource-conversion mechanism: a pending Harvester
chain frontier could feed into an adjacent friendly Conveyor only when the
complete visible downstream path was owned, acyclic, and proven to terminate
at our Core.  Unknown paths, Splitters, foreign buildings, and cycles stayed
on the conservative walk-to-Core route.

Allowed production scope was `bots/candidate/bot/defender.py`, with two
temporary deterministic tests in `tests/test_candidate_nearest_defense.py`
and a temporary rotated screen config.  Workforce, Store, roles, combat,
Sentinel retirement, baseline snapshots, package, upload, activation, and live
state were non-goals.

## Validation

- Focused candidate coverage passed **33/33**; candidate compileall passed.
  `make static` retained the inherited 15 obsolete-module imports and two
  navigation fast-path assertions; no v386-specific static error appeared.
- Candidate `make smoke` was **4/4** command-clean at
  `reports/local-20260820T234811Z`.
- The explicit immutable-v0046 rotated all-map screen (15 maps, both sides,
  `screen_seed=659`) was command-, delivery-, and reliability-clean but
  candidate trailed **7 wins to 9** baseline wins, with four paired games
  losing for both sides.  Collection was **71,800 vs 83,860 Ti**; first
  delivery was **15/15** for both, averaging **23.73 vs 29.93** rounds.
  There were zero TLE/suspicious rows and max p99/peak callback time was
  **1,243/5,698 us**.  Raw games are
  `reports/local-20260820T234852Z`; replay diagnostics are under
  `reports/iter-v386-conveyor-merge/replay-analysis.json`.

## Decision and rollback

Reject v386 without a long gate: safe visible merges did not improve wins and
reduced collection by 12,060 Ti.  The temporary merge logic, tests, and config
were removed.  Rollback focused coverage was **31/31**, compileall passed,
rollback smoke was **4/4** at `reports/local-20260820T235307Z`, and recursive
candidate parity with immutable v0046 is empty at
`reports/iter-v386-conveyor-merge/rollback-source-parity.diff`.

No promotion, release gate, package, upload, activation, or live transition
occurred.  Immutable v0046 remains the best baseline.

## Follow-up

Do not retry conveyor merging by widening the visibility/path bound.  The next
candidate must use a different replay-backed Harvester/Conveyor conversion
mechanism and preserve the delivery and reliability floors.
