# v398 Surplus-aware pressure conversion (rejected)

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v398 tested whether healthy `PRESSURE` should release non-steward dynamic
Builders from visible-ore harvesting once the bank could fund a replacement
route and the fixed attack reserve.  The bounded repair required a larger bank
and a concrete loaded-raid or ore-denial target before releasing them; without
an actionable target the worker stayed on economy.  Temporary production scope
was `bots/candidate/bot/dynamic.py` with focused coverage in
`tests/test_candidate_economy_phase.py`; no route geometry, Store schema,
spawning, combat targeting, map branches, baseline/archive, package, upload,
activation, or live state changed.

## Evidence

- Focused coverage was **37/37** for both candidate attempts and **36/36**
  after rollback.  Compileall passed for all attempts and rollback.  Smoke was
  **4/4** for the candidate and rollback.
- `make static` retained the inherited **exit 2** profile (15 obsolete import
  errors and two navigation fast-path assertions); no v398-specific failure
  appeared.  Logs are under `reports/iter-v398-surplus-pressure/`.
- Initial rotated all-map screen (`screen_seed=1291`) regressed to **12–18**,
  with 30/30 candidate deliveries, zero TLE/suspicious rows, and max p99/peak
  **1,242/2,804 us** (`reports/local-20260821T041348Z`).
- Bounded repair screen was **15–15**, with 30/30 deliveries, zero
  TLE/suspicious rows, and max p99/peak **1,391/5,384 us**
  (`reports/local-20260821T041830Z`).

## Decision and rollback

The first change starved maps by sending workers into `ADVANCE` without an
actionable target; the repair prevented that starvation but did not establish
an edge.  v398 is rejected after its bounded repair.  Temporary source, test,
and config edits were removed.  Recursive production parity with immutable
v0047 is exact; focused rollback tests, compileall, and smoke passed.  No
release gate, package, remote gate, upload, activation, or baseline transition
occurred.  Keep v0047 as baseline and do not revive this pressure-release rule
unchanged.

## Reports

- `reports/iter-v398-surplus-pressure/`
- `reports/local-20260821T041348Z`
- `reports/local-20260821T041830Z`
- `reports/local-20260821T041321Z`
- `reports/local-20260821T041759Z`
- `reports/local-20260821T042332Z`
