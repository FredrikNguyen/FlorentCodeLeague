# v314 opening-economy contract — rejected after one bounded repair

Date: 2026-08-20

## Objective and replay basis

The latest v107 replay audit showed a severe conversion shape on Yulerune:
the candidate side had six Builders, 18 Conveyors, one Harvester, and no
delivery while the opponent used an early control shell.  The current dynamic
dispatcher could leave the economy loop for belt repair, hijack, or pressure
work as soon as the delayed Core phase changed, even though income was not yet
stable.  v314 tested a structural dispatcher contract: route conversion should
own the dynamic pool during the Core's early/recovery phases, with home threats
and active repairs preserved.

## Scope and non-goals

Temporary production scope was `bots/candidate/bot/dynamic.py`; focused
coverage was `tests/test_candidate_economy_phase.py`.  The experiment record,
plan, updates, state metadata, and reports were also allowed.  Store layout,
route geometry/FSM, Builder spawn targets, combat-unit policy, map branches,
baseline snapshots, packaging, platform state, and live operations were
non-goals.

## Implementation and validation

The initial candidate made `TASK_HARVEST` precede visible optional work during
OPENING/CONVERTING/CRISIS and handed stale pressure tasks back after their
commit floor.  Focused tests passed **33/33**, compileall passed, `make smoke`
was **4/4** command-clean at `reports/local-20260820T003358Z`, and `make static`
retained the inherited 15 removed-module import errors and two navigation
fast-path assertions (`static.log`).

The required 15-map screen was command-clean but lost **3-12** to immutable
v0044.  Candidate collection was **34,850 vs 60,110 Ti**, with all 15 rows
delivering; replay diagnostics are in
`reports/iter-v314-opening-economy/screen-analysis.json` and the matrix report
`reports/local-20260820T003507Z`.  Harvester counts were lower on most losses,
showing that broad phase ownership starved useful local repair/pressure rather
than creating independent paying routes.

The one permitted repair narrowed the contract to the exceptional CRISIS
phase, leaving normal OPENING/CONVERTING arbitration unchanged.  Focused
coverage remained **33/33**, compileall passed, smoke was **4/4** at
`reports/local-20260820T003734Z`, and static retained the same inherited
profile.  The repair screen improved to **7-8** but still had one candidate
no-delivery row and lower collection (**57,070 vs 70,210 Ti**); evidence is in
`reports/iter-v314-opening-economy/repair-screen-analysis.json` and
`reports/local-20260820T003751Z`.  It did not beat the comparator.

## Decision and rollback

Reject v314 after the allowed repair.  The temporary dispatcher and focused
tests were removed; candidate production source is byte-identical to
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`, proven
by the empty `rollback-source-parity.diff`.  Rollback focused coverage was
**30/30**, compileall passed, `make static` returned the inherited exit 2, and
rollback smoke was **4/4** at `reports/local-20260820T004107Z`.  No long gate,
promotion, package, upload, activation, or live-state transition occurred.

## Remaining risk

The live one-Harvester/many-Conveyor shape remains a route-construction failure
that task priority alone cannot solve.  The next experiment should test a
route-first or route-verification lifecycle that prevents paying resources
from being stranded before a source and a verified Core sink exist, without
repeating the rejected global role/lease/Launcher changes.
