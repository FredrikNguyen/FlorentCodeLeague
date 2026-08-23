# v297 — large-board workforce-first pressure gate

## Hypothesis and scope

Fresh v107 replay losses repeatedly showed the candidate retaining only 4–7
Builders and 1–4 Harvesters while the opponent retained 8–13 Builders and
8–13 Harvesters.  v297 tested a map-contextual gate: on boards with
`width + height >= 40`, dynamic pressure and new forward Sentinel placement
waited until the global roster reached Core plus eight units.  Compact maps,
the Core spawn target, route FSM, Sentinel geometry, ammo, and defense policy
were unchanged.

The temporary production edits were limited to `constants.py`, `util.py`,
`attacker.py`, and `dynamic.py`; focused coverage was limited to
`tests/test_candidate_nearest_defense.py`.  No package, upload, activation,
or live-state transition was attempted.

## Evidence

- Focused coverage: **28/28**; compileall passed; smoke was **4/4**
  command-clean at `reports/local-20260819T184448Z`.
- `make static` retained the inherited repository failures: 15 obsolete
  candidate-module imports and two navigation fast-path assertions.
- The rotated 15-map screen at `reports/local-20260819T184522Z` was
  command/delivery-clean (**15/15** first deliveries for both sides), with
  zero TLE or suspicious rows, but the candidate lost **7–8** and collected
  **71,430 vs 71,130 Ti**.  Maximum p99 was **1,392 us** and maximum peak
  callback time **6,258 us**.
- The small collection edge was not a repeatable win-rate or workforce edge;
  several large-board rows still ended with materially fewer Harvesters.
  The first-screen done criteria therefore failed.

## Decision and rollback

Reject v297 at the first screen.  The temporary gate and tests were removed;
candidate production Python is recursively identical to immutable
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`, proven
by the empty `reports/iter-v297-workforce-first/parity-after-revert.diff`.
Rollback focused coverage is **26/26**, compileall passes, and rollback smoke
is **4/4** at `reports/local-20260819T185022Z`.  The rollback static log is
`reports/iter-v297-workforce-first/rollback-static.log` and retains only the
known inherited failures.

v105 remains the operational rollback target.  Live v107 remains
`active_observing`; no promotion or platform operation is justified by v297.
