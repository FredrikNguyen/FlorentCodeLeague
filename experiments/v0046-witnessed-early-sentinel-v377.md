# v377 witnessed early Sentinel shell — rejected

## Objective and scope

Starting from immutable v0046, v377 allowed one extra early forward Sentinel
only after the first forward Sentinel was freshly observed and the live bank
could still afford that Sentinel plus one Harvester and two Conveyor links.
The normal one-Sentinel opening cap, route policy, Builder targets, Launcher,
Barrier, Store schema, and baseline were otherwise unchanged.  Production
scope was `bots/candidate/bot/attacker.py`; focused coverage was temporary
coverage in `tests/test_candidate_nearest_defense.py`.

## Validation

- Focused coverage passed **27/27**, compileall passed, `make smoke` was **4/4**
  at `reports/local-20260820T213419Z`, and static retained only the inherited
  workspace failures (15 obsolete imports and two navigation assertions).
- The first rotated all-15-map/30-game screen (`screen_seed=503`) was
  command-clean but only **15–15**, with 30/30 candidate and baseline
  deliveries and zero TLE/suspicious rows.  Candidate collection was
  **155,840 Ti** aggregate, first delivery averaged **33.3** rounds, and
  average surviving units were 7.0 Harvesters, 1.3 Sentinels, 2.13 Gunners,
  and 8.67 Builders.  Raw games are under
  `reports/local-20260820T213456Z`; diagnostics are in
  `reports/iter-v377-witnessed-early-sentinel/analysis.json`.

The 9–6 first-screen floor failed, so no second screen or release matrix was
justified.

## Rollback and decision

The temporary reserve helper, focused test, and screen configs were removed.
Candidate production is recursively byte-identical to immutable v0046; the
empty proof is at
`reports/iter-v377-witnessed-early-sentinel/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T213908Z`.  No baseline, package, upload,
activation, promotion, or live-state transition occurred.

Reject v377.  The witnessed reserve did not create a repeatable win-rate edge;
the next iteration must use a distinct conversion mechanism rather than
raising the early Sentinel cap.
