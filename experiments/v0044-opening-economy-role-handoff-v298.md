# v298 — opening-economy role handoff

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 losses showed that builders assigned to the pre-route economy floor
remain `ROLE_DEFENDER` for life, even after a completed route should let them
use the existing dynamic repair/harvest/hijack/pressure selector.  v298 added
one lifecycle handoff: only that temporary opening-floor population becomes
dynamic after the delayed `SLOT_HARVESTER_COUNT` confirms a completed route.
The Core-designated permanent defender and all later role assignments remain
unchanged.  Production scope was limited to `bots/candidate/main.py`; focused
coverage was one temporary role-handoff module.

## Validation and evidence

- New focused coverage passed **34/34** including the handoff, existing phase,
  nearest-defense, and seeded-route suites.  Compileall passed.  `make smoke`
  was **4/4** command-clean at `reports/local-20260819T190925Z`.
- `make static` retained the inherited repository state: 15 imports of removed
  legacy candidate modules and two navigation fast-path assertions.  The new
  role test passed; no new static failure was introduced.  Full output is
  `reports/iter-v298-role-handoff/static.log`.
- The required all-map seed-172 screen was command/delivery-clean with zero
  TLE or suspicious rows, but finished **8–7** for the candidate-A side and
  collected **69,170 vs 72,440 Ti** (`reports/local-20260819T190949Z`).  Replay
  analysis found max p99/peak callback times of **1,419/4,765 us**.
- The independent rotated seed-173 screen was also command/delivery-clean with
  zero TLE or suspicious rows, but regressed to **6–9** and collected
  **56,090 vs 71,300 Ti** (`reports/local-20260819T191136Z`).  Replay analysis
  found max p99/peak callback times of **1,304/2,985 us**.  Both screens had
  15/15 candidate deliveries; the first edge was not repeatable.  Detailed
  replay summaries are in
  `reports/iter-v298-role-handoff/screen172-replay-analysis.log` and
  `screen173-replay-analysis.log`.

## Decision and rollback

Reject v298 without repair or release.  The temporary role handoff and test
were removed; candidate production source is recursively byte-identical to
immutable `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`,
proven by the empty `reports/iter-v298-role-handoff/rollback-source-parity.diff`.
Rollback focused coverage passed **34/34**, compileall passed, and rollback
smoke was **4/4** at `reports/local-20260819T191411Z`.  No 60-game gate,
package, upload, activation, or live transition was justified.  v105 remains
the operational rollback target and live v107 remains `active_observing`.
