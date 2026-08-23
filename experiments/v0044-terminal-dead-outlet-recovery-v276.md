# v276 terminal-dead Harvester outlet recovery — rejected

Date: 2026-08-19

## Objective and scope

The v275 Drakkarfjord replay delivered first at turn 601 versus 82 for the
comparator despite seven candidate Harvesters and 84 surviving Conveyors.
The bounded hypothesis was that a friendly Conveyor can remain geometrically
accepting to a Harvester while its visible output is terminal-dead. The
existing orphan check would then suppress its local seeded reconnect. The
allowed production scope was only `bots/candidate/bot/defender.py`; focused
coverage, this record, the plan, updates, and durable metadata were allowed.
No Store, route FSM, opening, workforce, combat, baseline, or platform change
was included.

## Implementation

The initial candidate treated a friendly Conveyor as non-healthy when it
accepted the Harvester but `_belt_output_status` classified its output as
`BELT_OUT_DEAD` (wall, enemy/non-accepting building, boundary, or verified
two-belt cycle). Unknown, gap, healthy-belt, Core, and Splitter outputs stayed
conservative. The existing adjacent `_try_reconnect_orphaned_harvester`
path performed the only recovery. A bounded repair restricted that new rule
to after `SLOT_HARVESTER_COUNT` became positive, preserving opening behavior.

## Evidence

- Initial focused **33/33**, compileall pass, smoke **4/4**; static retained
  inherited exit 2. Reports: `focused.log`, `compileall.log`, `static.log`,
  `smoke.log`.
- Initial seed-172 screen: **8-7**, collection **41,950/61,480 Ti**, delivery
  **15/15 vs 14/15**, zero command/TLE/suspicious rows. Replay analysis:
  `screen-172-replay-analysis.json`; matrix report:
  `reports/local-20260819T125549Z`.
- Initial seed-175 screen: **6-9**, collection **50,640/62,830 Ti**, delivery
  **15/15 vs 14/15**, zero command/TLE/suspicious rows. Replay analysis:
  `screen-175-replay-analysis.json`; matrix report:
  `reports/local-20260819T125830Z`.
- Initial aggregate: **14-16**, collection **92,590/124,310 Ti**; no release
  gate was justified.
- Repair focused **34/34**, compileall pass, smoke **4/4**; static retained
  the same inherited failures. Reports: `focused-repair.log`,
  `compileall-repair.log`, `static-repair.log`, `smoke-repair.log`.
- Repair seed-172: **5-10**, collection **61,780/59,960 Ti**, delivery
  **14/15 vs 15/15**, zero command/TLE/suspicious rows. Replay analysis:
  `screen-172-repair-replay-analysis.json`; matrix report:
  `reports/local-20260819T130111Z`.
- Repair seed-175: **6-9**, collection **69,050/77,780 Ti**, delivery
  **15/15 vs 15/15**, zero command/TLE/suspicious rows. Replay analysis:
  `screen-175-repair-replay-analysis.json`; matrix report:
  `reports/local-20260819T130237Z`.
- Repair aggregate: **11-19**, collection **130,830/137,740 Ti**. The
  hypothesis and repair are rejected; no long gate or release was run.

## Rollback and risks

The candidate source was restored recursively byte-identically to immutable
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`; the
zero-line proof is `reports/iter-v276-terminal-dead-outlet/rollback-source.diff`.
Rollback focused coverage was **31/31**, compileall passed, smoke **4/4**,
and static retained the inherited exit 2 (`rollback-focused.log`,
`rollback-compileall.log`, `rollback-smoke.log`, `rollback-static.log`). No
promotion, package, upload, activation, or live transition occurred. v0044
remains the local baseline. v105 remains the user-requested historical
rollback reference, while v101 is the guarded operational fallback because
v105's recorded result is 142/275 (51.64%). The latest durable observation
still has platform v105 active-observing at live score **0.5** with
`reports/live-observe-20260819T124953Z`; no new candidate was submitted.
