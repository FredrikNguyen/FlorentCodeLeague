# v373 Heartbeat-gated siege ammo — rejected

Date: 2026-08-20

## Objective and scope

Starting from immutable v0046, v373 tested a resource-conversion contract for
the large `AMMO_BUFFER_SIEGE`: the Core would use it only while the delayed
economy phase was `PRESSURE` and a recent positive-income heartbeat existed.
Outside that state the existing 10-ammo floor and small buffer remained.  The
goal was to avoid stale forward-Sentinel counts consuming route capital after
the siege had gone quiet; replay evidence showed v0046 ending with more ammo
despite fewer placed Sentinels than its comparator.

Production scope was `bots/candidate/bot/core_role.py`; focused coverage used
`tests/test_candidate_nearest_defense.py`.  No route, task, spawning, turret,
Sentinel placement, Launcher/Barrier, Store schema, baseline, package, upload,
activation, or live state changed.

## Validation and decision

- Focused coverage passed **27/27**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained the inherited exit **2** (15 obsolete imports and
  two navigation assertions).
- The first rotated 30-game all-map screen (seed 461) was command/delivery/
  reliability-clean but **14–16**, with **135,430/145,190 Ti** collected and
  max p99/peak **1,234/5,788 us**.  Replay analysis is under
  `reports/local-20260820T204643Z` and
  `reports/iter-v373-heartbeat-siege-ammo/analysis.json`.

Reject v373 at the first-screen floor; no second screen or release gate was
justified.  The temporary source/test/config edits were removed and candidate
production is recursively byte-identical to immutable v0046 (empty
`rollback-source-parity.diff`).  Rollback focused coverage was **26/26**,
compileall passed, and rollback smoke was **4/4** at
`reports/local-20260820T205034Z`.  No promotion or live operation occurred.
