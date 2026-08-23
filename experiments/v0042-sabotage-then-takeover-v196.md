# v196 — sabotage-then-takeover

## Objective

Test one bounded offence/sabotage transition on top of immutable v0042: a
late, reserve-funded fixed attacker should legally fire on a visible enemy-fed
Conveyor, wait until the tile is empty, then seed a Core-facing accepting
Conveyor so the enemy Harvester output can be routed to our Core. The branch
was intended to turn the user’s sabotage/steal idea into an observable,
ownership-safe action rather than overwrite enemy infrastructure.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/attacker.py`.
- Temporary focused coverage: `tests/test_candidate_sabotage_reclaim.py`.
- No `main.py`, baseline snapshot, package, upload, activation, or live-state
  changes were allowed.
- Dynamic Conveyor/Harvester prices, source ownership, adjacency, action
  cooldowns, and replacement reserves were checked before each action.
- The bounded repair only reordered the verified reclaim attempt before the
  optional Core cage barrier; it did not add another steal path.

## Validation

- Initial focused coverage: **30/30**; compileall passed; `make static` retained
  only the inherited static failures; smoke was **4/4** command-clean.
- Initial seed-162 all-map screen: **7-8** candidate wins, 15/15
  command-clean, zero candidate no-delivery, TLE, or suspicious-output rows;
  max p99 was **1413 us**. Report: `reports/local-20260818T114458Z`.
- Bounded priority repair focused coverage: **32/32**; compileall passed;
  static retained the same inherited failures; smoke was **4/4** command-clean.
- Repair screen: **7-8** candidate wins, 15/15 command-clean, zero candidate
  no-delivery, TLE, or suspicious-output rows; max p99 was **1319 us**.
  Report: `reports/local-20260818T114931Z`.
- The rollback was verified with the baseline focused tests (**27/27**),
  compileall, smoke report `reports/local-20260818T115418Z`, and recursive
  candidate parity against
  `bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f`.

## Decision

Reject v196 and retain v0042. Neither the destroy-then-reclaim transition nor
the bounded priority repair beat the paired 15-game screen; therefore no
60-game gate, release, package, upload, activation, or baseline transition is
warranted. The direct enemy-Conveyor hijack branch has reached a local wall
after v195’s parallel outlet and v196’s verified destroy/reclaim variants.

## Next direction

Move to a different hypothesis: improve resource-to-offence/defence conversion
for an already idle builder using map-state and reserve gates, rather than
another enemy-route takeover variant. First inspect the current task ordering
and replay evidence, then implement one reversible handoff with focused legal
action tests.
