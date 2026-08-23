# v245 first-Harvester opening handoff

Date: 2026-08-19

## Hypothesis

Current v0042 replay timing showed its first Core-ring Conveyor around round 3
but first Harvester around round 10, while high-ranking winners placed their
first Harvester around round 4.7 and first Conveyor around round 6.5. When no
completed route existed, a Defender therefore tried an adjacent Harvester
before the opportunistic Core-ring Conveyor; if no ore was adjacent, the ring
fallback remained unchanged. Established routes kept the existing ring-first
order.

## Validation

- Focused opening-order/legality plus nearest-defense/seeded-route tests:
  **31/31** (`reports/iter-v245-opening-harvester/focused.log`).
- Candidate compileall: pass (`reports/iter-v245-opening-harvester/compileall.log`).
- `make static`: inherited exit 2; 15 obsolete deleted-module imports and two
  navigation fast-path assertions (`reports/iter-v245-opening-harvester/static.log`).
- Smoke: **4/4**, report `reports/local-20260819T022412Z`.
- Rotated 15-map screen: **4-11**, command-clean, zero TLE/suspicious rows,
  and 15/15 deliveries. Candidate collected **74,020 vs 96,440 Ti**,
  averaged **8.0 vs 9.0 Harvesters** and **2.27 vs 3.8 Sentinels**, and first
  delivery was **24.3 vs 21.4**. Raw report:
  `reports/local-20260819T022437Z`; parsed diagnostics:
  `reports/iter-v245-opening-harvester/replay-analysis.json`.

## Decision

Reject without a repair or longer gate. The conditional opening handoff did
not improve conversion enough to offset reduced mature workforce and
Sentinel pressure. Temporary source/test edits were removed and recursive
candidate parity with immutable v0042 is zero-line
(`reports/iter-v245-opening-harvester/rollback-source.diff`). Rollback focused
coverage was **27/27**, compileall passed, static retained inherited failures,
and rollback smoke was **4/4** at
`reports/local-20260819T022722Z`. No promotion, package, upload, activation,
or live-state transition occurred.
