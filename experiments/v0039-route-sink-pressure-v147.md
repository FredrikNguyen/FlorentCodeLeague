# v147 opening route-pressure experiment — rejected

## Objective

Reduce opening no-delivery losses by preventing multiple pre-income Builders
from spending the opening titanium bank on disconnected partial Harvester
chains. The frozen comparator was the locally promoted v0039 post-route sink
repair snapshot.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, reports, `UPDATES.md`, and durable state

## Non-goals

No route merge, navigation, combat, Store-layout, workforce, Launcher,
baseline, package, upload, activation, or live-state changes.

## Hypothesis and attempts

The replay audit identified three v0039 full-matrix no-delivery losses where
several opening workers started independent chains before any route reached the
Core. The initial variant allowed only the Core-designated permanent defender
to build a new Harvester while the completed-route counter was zero. Repair 1
kept that gate only below one Harvester plus three Conveyor costs, allowing
parallel exploration while the bank was healthy.

## Evidence

- Initial focused tests: **20/20**, compileall passed, `make static` retained
  the inherited 15 obsolete-import failures plus two navigation assertions,
  and smoke was 4/4 (`reports/local-20260817T180609Z`).
- Initial 54-game screen: **29-25**, candidate/comparator collection
  **212,210/197,920 Ti**, candidate/comparator no-delivery **3/0**, zero
  command failures/TLE/suspicious output (`reports/local-20260817T180645Z`,
  analysis `reports/iter-v147-route-pressure/screen-analysis.json`).
- Repair 1 focused tests: **20/20**, compileall passed, static retained the
  same inherited failure, and smoke was 4/4 (`reports/local-20260817T181350Z`).
- Repair 1 54-game screen: **28-26**, candidate/comparator collection
  **200,220/205,930 Ti**, no-delivery **1/1**, zero command failures/TLE/
  suspicious output (`reports/local-20260817T181418Z`, analysis
  `reports/iter-v147-route-pressure/repair1-analysis.json`).

## Decision and rollback

Reject after the required two bounded repair attempts. Neither screen beat the
v0039 comparator (v146 was 30-24 with candidate no-delivery 0/1), so no long
gate or package was run. The candidate was restored byte-identically to
`bots/versions/v0039_post-route-sink-v146_20260817-1752_eeafad8f`; rollback
focused tests were **18/18**, compileall passed, and rollback smoke was 4/4
(`reports/iter-v147-route-pressure/rollback-smoke.log`, report
`reports/local-20260817T181959Z`).

## Remaining risk

The three v0039 no-delivery losses remain. A future route-pressure change needs
shared route-progress evidence rather than a Builder-local opening owner gate.
