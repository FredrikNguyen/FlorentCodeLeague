# v253 established-source Harvester hijack — rejected

## Objective and evidence

The latest attributable v106 ladder series was a 5-0 win over version 12
(`e3fc8421-f1de-4543-b529-1248a6c52030`). Replay analysis found our Conveyor
adjacent to an enemy Harvester in all five games (first contact on turns
29–477), while no opponent Conveyor reached our Harvesters. This supports
improving our existing infiltration selector, not adding a broad infiltrator
defense response.

The hypothesis was that, when several enemy Harvesters are visible, a source
with more visible enemy Conveyor/Splitter outlets is a better theft target than
an arbitrary source. The implementation was restricted to the dynamic
Harvester selector; route seeding, economy gates, fixed attackers, and defense
were unchanged.

## Exact scope

- `bots/candidate/bot/dynamic.py` — rank visible enemy Harvesters by opposing
  outlet count, then deterministic travel/tie-breakers;
- `tests/test_candidate_nearest_defense.py` — selector tests;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable reports.

No baseline/archive, package, upload, activation, or live-state operation was
performed.

## Validation

Initial selector (opposing outlets first):

- focused **28/28**, compileall passed, static retained the inherited 15
  obsolete-module import errors and two navigation fast-path assertions;
- smoke **4/4**, report `reports/local-20260819T051732Z`;
- 15-map screen **3-12** candidate-A, all command-clean; replay analysis
  `reports/iter-v253-established-source-hijack/screen-analysis.json`;
- same schedule with sides swapped: candidate **7-8**; report
  `reports/iter-v253-established-source-hijack/screen-swapped-analysis.json`.

The initial selector pulled workforce toward distant established sources and
under-produced Harvesters, so one bounded repair made travel distance primary
and outlet count only an equal-distance tie-breaker:

- repair focused **29/29**, compileall passed; repair static retained the same
  inherited failures; repair smoke **4/4**, report
  `reports/local-20260819T052258Z`;
- repaired 15-map order: **8-7** candidate-A; reversed order: **9-6**
  candidate-B, **17-13** aggregate over 30 games, all deliveries, zero TLE or
  suspicious rows; analyses are
  `reports/iter-v253-established-source-hijack/repair-screen-analysis.json`
  and `repair-screen-swapped-analysis.json`;
- release gate (`configs/eval_matrix.toml`): **30-30** over 60 games, all
  deliveries, zero TLE/suspicious rows, max p99/peak **1,548/4,579 us**;
  report `reports/iter-v253-established-source-hijack/release-analysis.json`
  and raw run `reports/local-20260819T052740Z`.

## Decision and rollback

Reject v253: the repaired selector did not beat exact v0043 at the release
gate. The source and tests were restored; recursive candidate parity with the
immutable v0043 snapshot is zero. Rollback focused coverage is **26/26**,
compileall passed, rollback smoke is **4/4** at
`reports/local-20260819T053521Z`. No package, remote gate, upload, activation,
or promotion occurred.

## Remaining risk and next direction

Our own Harvester infiltration is real and already effective in the current
baseline; the new ranking was not a reliable improvement. The broad
infiltrator-defense family remains unsupported by the observed replays. Keep
v0043/v106 active and choose a different causal conversion hypothesis only
after fresh live/replay evidence.
