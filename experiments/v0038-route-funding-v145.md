# v145 first-route funding guard — rejected

## Objective

Prevent a low-balance opening Harvester from entering `CHAIN` with no
Titanium left for its first Conveyor, while allowing a Harvester to join an
already visible friendly sink.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, report artifacts, `UPDATES.md`, and durable state

## Non-goals

No navigation, combat, workforce, Store-layout, map branch, baseline, package,
upload, activation, or live-state changes.

## Hypothesis and implementation

The initial variant reserved one dynamic Conveyor cost whenever no completed
Harvester chain was visible. Repair 1 kept that reserve only when no visible
friendly Conveyor/Splitter sink existed, so low-balance Harvesters could join
an established local network. Both variants used `get_*_cost()` and retained
the existing legality gates.

## Evidence

- Initial focused tests were 17/17, compileall passed, smoke was 4/4, and
  `make static` retained the inherited exit 2 (15 obsolete imports plus two
  navigation fast-path assertions). The 54-game screen was **25-29**, with
  184,080 versus 224,870 collected Ti, zero command failures, and report
  `reports/local-20260817T164139Z`.
- Repair 1 focused tests were 18/18, compileall passed, smoke was 4/4, and
  static retained the same inherited failure. The screen was **30-24** with
  203,670 versus 206,630 collected Ti and report
  `reports/local-20260817T164834Z`.
- The release-sized 210-game matrix for the repaired variant was command
  clean but scored **99-111** (47.1%), with 902,520 versus 895,540 collected
  Ti. Replay analysis recorded zero TLE/suspicious-output flags, max p99
  1,496 us, max peak 5,538 us, five candidate no-delivery games versus zero
  for the comparator, and mean first delivery 35.1 versus 31.9 turns.
  Reports: `reports/local-20260817T165424Z` and
  `reports/iter-v145-route-funding/long-replay-analysis.json`.

## Decision and rollback

Reject after one bounded repair and the long gate. The route-funding guard
and focused tests were removed; every production Python file under
`bots/candidate` is byte-identical to immutable v0038. Rollback focused tests
were 16/16 and parity was exact. No package, upload, activation, or baseline
transition occurred.

## Remaining risk

The first-route failure is not explained by a one-Conveyor affordability
reserve: the long run preserved total Ti but delayed delivery and increased
no-delivery outcomes. Future work should inspect route sink conversion or
map-context dispatch directly rather than withholding Harvester purchases.

## Score definition

The primary local comparison is paired game win rate against the frozen v0038
baseline. Reliability failures override score and trigger rollback.
