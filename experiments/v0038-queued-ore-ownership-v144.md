# v144 queued-ore ownership — rejected

## Objective

Reduce same-ore/frontier pileups observed in v0038 replay losses. The visible
ore picker already yields to a closer Builder, but the delayed Store ore
ring-buffer did not: several Builders could chase the same advertised target.
Reuse the existing local distance/ID ownership rule for queued ore.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, report artifacts, `UPDATES.md`, and durable state

## Non-goals

No workforce threshold, route FSM, navigation, combat, Store layout, map branch,
baseline, package, upload, activation, or live-state change.

## Hypothesis and implementation

The initial variant applied `_yield_ore_to_closer_builder` to every queued ore
target. Repair 1 kept the rule disabled until one completed route was visible
(`SLOT_HARVESTER_COUNT > 0`) so the opening chain remained v0038 behavior.

## Evidence

- Initial focused tests were 17/17, compileall passed, smoke was 4/4, and
  `make static` retained the inherited exit 2 (15 obsolete imports plus two
  navigation fast-path assertions). The 54-game screen was **24-30**, with
  155,050 versus 220,820 Ti, no-delivery 1/1, zero command/TLE/suspicious-
  output failures, and max p99/peak 1,539/4,809 us. Report:
  `reports/local-20260817T162006Z`.
- Repair 1 focused tests were 17/17, compileall passed, smoke was 4/4, and
  static retained the same inherited failure. The screen improved to **26-28**
  but still lost the control, with 196,510 versus 174,000 Ti, no-delivery 1/0,
  zero reliability flags, and max p99/peak 1,427/5,091 us. Report:
  `reports/local-20260817T162533Z`.

## Decision and rollback

Reject after the initial screen and one bounded repair. The queued-ore
ownership rule and focused test were removed; all production Python files under
`bots/candidate` are byte-identical to immutable v0038. Rollback focused tests
were 16/16, compileall passed, smoke was 4/4 command-clean, and static retained
the inherited red result. Rollback logs are under
`reports/iter-v144-queued-ore/`; rollback smoke report:
`reports/local-20260817T163037Z`.

## Remaining risk

Queued-ore ownership is not a stable way to coordinate builders: the local
visibility rule suppresses useful work on elongated maps even when opening
behavior is preserved. Future work should use a different route-conversion or
map-context signal rather than adding another local reservation heuristic.
