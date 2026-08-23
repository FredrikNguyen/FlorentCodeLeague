# v143 route-sentry local Builder response — rejected

## Objective

Use Ragnarok loss evidence to let a Dynamic Builder already close to one of
our completed Harvesters answer a visible enemy Builder threatening that
remote asset. The response had to stay local and reuse the existing
`TASK_HOME_THREAT` strike path; v0038 remained the baseline unless paired
win-rate improved.

## Allowed files

- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, report artifacts, `UPDATES.md`, and durable state

## Non-goals

No new task class, opening workforce change, cross-map recall, route FSM or
navigation change, Store protocol, combat policy, Sentinel policy, baseline,
package, upload, activation, or live-state change.

## Hypothesis and implementation

The initial candidate recognized a route threat when a visible enemy Builder
was within distance squared 16 of an own Harvester and the Dynamic Builder was
within distance squared 36. Repair 1 narrowed that trigger to distance squared
2; repair 2 narrowed it to true orthogonal adjacency (distance squared 1).
Both retained the existing nearest-responder ownership and strike execution.

## Evidence

- Initial focused tests were 26/26, compileall passed, smoke was 4/4, and
  `make static` retained the inherited exit 2 (15 obsolete imports plus two
  navigation fast-path assertions). The 54-game screen was **28-26**, with
  193,060 versus 176,500 Ti, candidate no-delivery 1 versus comparator 0,
  zero command/TLE/suspicious-output failures, and max p99/peak 1,390/2,974
  us. Report: `reports/local-20260817T154912Z`.
- Repair 1 focused tests were 26/26, compileall passed, smoke was 4/4, and
  static retained the same inherited failure. The screen restored the
  control's **30-24** but did not improve its win rate; collection was
  206,200 versus 184,000 Ti, no-delivery 0 versus 2, zero reliability flags,
  and max p99/peak 1,514/4,260 us. Report:
  `reports/local-20260817T155802Z`.
- Repair 2 focused tests were 26/26, compileall passed, smoke was 4/4, and
  static retained the same inherited failure. The adjacent-only trigger
  regressed to **29-25**, collection 175,140 versus 166,600 Ti, no-delivery
  1 versus 1, zero reliability flags, and max p99/peak 1,319/5,736 us.
  Report: `reports/local-20260817T160350Z`.

## Decision and rollback

Reject after two bounded repairs: neither variant exceeded the v0038
30-24 short-screen control. The route-sentry code and tests were removed;
all production Python files under `bots/candidate` are byte-identical to the
immutable v0038 snapshot. Rollback focused tests were 16/16, compileall
passed, smoke was 4/4 command-clean, and static retained the inherited red
result. Rollback logs are under `reports/iter-v143-route-sentry/` and the
rollback smoke report is `reports/local-20260817T160905Z`.

## Remaining risk

The Ragnarok full-gate losses still show route ownership and sink-conversion
weaknesses, but a local Builder escort is not stable enough to retain. The
next experiment must select a different causal route/sink behavior and screen
it against v0038 without changing the global navigation contract.
