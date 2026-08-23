# v234 local orphan-Harvester reconnect — rejected after one repair

## Hypothesis

After three completed routes, the dynamic selector can see a friendly
Harvester that has no accepting Conveyor/Splitter neighbor but still fall
through to raid or advance because it only treats visible ore as an economy
signal. The Defender already owns a legal local reconnect FSM; expose that FSM
as one nearest-owner task for a visible disconnected source. This is not a
global Harvester-count floor, a distant scout, or a new route builder.

## Scope

- `bots/candidate/bot/constants.py`;
- `bots/candidate/bot/dynamic.py`;
- one focused orphan-reconnect test module;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable state/report
  metadata.

No opening ore ranking, CHAIN geometry/facing, Store schema, workforce,
hijack/raid target ranking, combat, Launcher, Sentinel, Barrier, package,
upload, activation, or live-state behavior changes.

## Evidence basis

The v211 replay audit found geometric route-completion false progress and
post-delivery collection plateaus, while the v204 cleanup/retry and v150/v181
route-join variants showed that rewriting ordinary chain geometry is harmful.
The retained code has a local `_try_reconnect_orphaned_harvester` path, but
`DynamicMixin._best_task` never selects it once `SLOT_HARVESTER_COUNT` reaches
the offense threshold unless fresh ore is visible. v234 tests only the missing
selector handoff and delegates execution to that existing FSM.

## Validation record

The initial implementation passed **31/31** focused tests, candidate
compileall, and `git diff --check`; `make smoke` was **4/4** at
`reports/local-20260818T232333Z`. `make static` retained the inherited exit 2
(obsolete imports for deleted legacy candidate modules plus two existing
navigation fast-path assertions). The 15-map screen
(`reports/local-20260818T232404Z`) was **6-9**, with collection
**87,470/90,670 Ti** (candidate/baseline), first delivery **15/15 vs 15/15**,
zero candidate no-delivery/TLE/suspicious rows, and max p99/peak
**1,386/3,054 us**.

The one bounded repair restricted the reconnect site to squared radius two.
Focused tests remained **31/31**, compileall and smoke **4/4** stayed clean,
and static was unchanged. The repaired screen
(`reports/local-20260818T232702Z`) was **7-8**, with collection
**73,410/73,040 Ti**, first delivery **14/15 vs 15/15**, one candidate
no-delivery on Valkyrie, zero TLE/suspicious rows, and max p99/peak
**1,483/3,654 us**.

The candidate had no repeatable win-rate or delivery-safe edge, so v234 was
rejected without a 60-game gate. Temporary `constants.py`, `dynamic.py`, and
focused-test edits were removed. Final rollback coverage was **27/27** for
the nearest-defense and seeded-route suites; compileall passed, static retained
exit 2, rollback smoke was **4/4** at
`reports/local-20260818T233251Z`, and candidate Python is recursively
byte-identical to immutable v0042. No promotion, package, upload, activation,
or live-state transition occurred.

## Decision

Reject the dynamic orphan-reconnect selector. It spent worker turns on local
repair without improving paired wins and the locality repair broke first
delivery on Valkyrie. Preserve v0042 and choose a different structural
workforce or pressure signal for the next experiment.
