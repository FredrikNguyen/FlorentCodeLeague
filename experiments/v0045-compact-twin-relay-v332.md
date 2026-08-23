# v332 — compact-map twin Launcher relay (rejected)

## Objective and scope

Top-team control-first openings commonly show two or three Launchers while
our v0045 opening owns only one.  v332 tested a finite, map-adaptive squad:
on compact maps the Core designated the first stage-2 Builder as the second
fixed attacker, and each fixed attacker could build one reserve-backed home
Launcher.  Wide maps retained the proven three-route gate.  The pair never
changed route FSM, dynamic task priorities, Sentinel/Gunner spending, or Store
schema.

Production scope was `bots/candidate/bot/core_role.py` and
`bots/candidate/bot/attacker.py`, with focused additions to
`tests/test_candidate_v319_launcher.py`.  Baseline snapshots, package,
upload, activation, and live state were out of scope.

## Validation

- Focused coverage passed **42/42**, compileall passed, and smoke was **4/4**
  at `reports/local-20260820T043753Z`.
- `make static` retained the inherited 15 obsolete-module imports and two
  navigation fast-path assertions; no v332-specific static failure appeared
  (`reports/iter-v332-twin-relay-static.log`).
- The rotated 15-map screen was command/reliability-clean at **7-8
  candidate-A**.  Collection was **76,630 vs 76,540 Ti**, candidate delivered
  on all 15 rows versus 13 comparator deliveries, and max p99/peak was
  **1,301/2,775 us**.  Reports are
  `reports/local-20260820T043832Z` and
  `reports/iter-v332-twin-relay-replay-analysis.json`.

## Decision and rollback

Reject v332: the second relay improved a few compact pressure rows but did not
produce a material paired win-rate edge and still collapsed on several maps.
The temporary designation, relay logic, and tests were removed.  Recursive
candidate production parity with immutable v0045 is exact; rollback focused
coverage passed **40/40** at
`reports/iter-v332-twin-relay-rollback-focused.log`.  No long gate, remote
gate, package, upload, promotion, activation, or live transition occurred.

## Remaining risk

Launcher count alone is not the missing coordination primitive.  The next
experiment should stop duplicate infiltration attempts and assign one visible
enemy source to one nearest Builder, preserving route workers while making
steal/sabotage purposeful.
