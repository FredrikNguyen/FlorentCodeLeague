# v273 delivery-gated stage-two workforce — rejected

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 live replays showed a GlacierKeep opening in which our side had
eight Builders, one non-delivering Harvester, and no meaningful titanium while
the opponent held four Builders, four Harvesters, and a live route. v273
tested whether the fixed `STAGE2_FALLBACK_ROUND` was admitting too much
workforce before a route had proved that the opening could convert resources.

Allowed production files were `bots/candidate/bot/core_role.py` and
`bots/candidate/bot/constants.py`, plus focused nearest-defense/workforce
coverage and durable records. Route geometry, chain recovery, selectors,
combat, Store schema, packaging, upload, activation, and live-state changes
were out of scope.

## Implementation and checks

The initial candidate removed the fixed-round fallback and kept stage two
route-gated by `HARVESTER_MILESTONE`. The focused unittest subset passed
32/32; `compileall` passed; smoke was 4/4; and `make static` retained the
inherited deleted-module imports and two navigation fast-path assertions.
The pytest module was unavailable in the environment (`No module named
pytest`), so the equivalent unittest subset was used.

Initial screens against exact
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f` were
command-clean with zero TLE/suspicious rows:

| screen | candidate wins | collection Ti | first delivery | max p99/peak us |
| --- | ---: | ---: | ---: | ---: |
| seed 172 | 7-8 | 70,880 vs 74,440 | 15/15 vs 14/15 | 1,507/2,685 |
| seed 175 | 7-8 | 41,960 vs 49,640 | 14/15 vs 15/15 | 1,375/2,639 |

The combined result was 14-16, with no repeatable win edge.

## Bounded repair and decision

The one permitted repair restored a route-gated stage-two decision but allowed
at most one reserve-backed pre-route Builder when the bank could still fund a
Builder, Harvester, four links, and the spawn reserve. It passed focused
coverage 32/32, compileall, and smoke 4/4; static retained the same inherited
failures. The repair screens remained command/reliability-clean:

| screen | candidate wins | collection Ti | first delivery | max p99/peak us |
| --- | ---: | ---: | ---: | ---: |
| seed 172 | 8-7 | 67,850 vs 64,320 | 15/15 vs 15/15 | 1,257/3,930 |
| seed 175 | 6-9 | 51,930 vs 64,310 | 15/15 vs 15/15 | 1,413/2,287 |

The repaired aggregate was also 14-16 and reduced collection by 10,980 Ti
versus the baseline across the two screens. It therefore failed the done
criterion for a repeatable aggregate improvement. No 60-game gate, remote
gate, archive, package, submission, activation, or live transition was run.

The candidate source was restored exactly to the immutable v0044 snapshot;
the recursive source diff is empty. Rollback coverage passed 31/31, compileall
passed, smoke was 4/4, and static retained the inherited exit 2. Reports:

- `reports/live-observe-20260819T114622Z`
- `reports/live-v107-diagnosis/`
- `reports/iter-v273-delivery-gated-workforce/`
- `reports/local-20260819T115500Z`
- `reports/local-20260819T115729Z`
- `reports/local-20260819T120042Z`
- `reports/local-20260819T120255Z`
- `reports/local-20260819T120649Z`

v0044 remains the moving local baseline. Platform v107 remains
`active_observing`; v101 is still the guarded operational rollback because
the user-requested v105 historical submission is known bad (142/275, 51.64%).
The next hypothesis should change route ordering rather than add another
workforce timing knob.
