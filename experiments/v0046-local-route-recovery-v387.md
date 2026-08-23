# v387 pressure-phase local-route recovery — rejected

## Objective and scope

Starting from immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`,
v387 tested a bounded recovery lease motivated by live-v108 losses where only
one or two Harvesters survived while opponents retained 8–13.  During healthy
`PRESSURE`, exactly one nearest home dynamic Builder could stay in the normal
economy loop when no friendly Harvester was visible in the Core home radius,
but only when the bank covered a dynamically priced Harvester, two Conveyor
links, and the fixed attack reserve.  Distant workers and fixed attackers were
unchanged.

Allowed production scope was `bots/candidate/bot/dynamic.py`, with one
temporary economy-phase test in `tests/test_candidate_economy_phase.py` and a
temporary rotated screen config.  Store layout, route geometry, combat,
baseline snapshots, package, upload, activation, and live state were
non-goals.  The read-only live capture used for diagnosis is preserved at
`reports/live-continuation-v386-20260820T235823Z`.

## Validation

- Focused candidate coverage passed **32/32**; candidate compileall passed.
  `make static` retained the inherited 15 obsolete-module imports and two
  navigation fast-path assertions; no v387-specific static error appeared.
- Candidate `make smoke` was **4/4** command-clean at
  `reports/local-20260821T000130Z`.
- The explicit immutable-v0046 rotated all-map screen (15 maps, both sides,
  `screen_seed=673`) was command-, delivery-, and reliability-clean.  The
  candidate won **16–14** games, with **15/15** first deliveries on both sides,
  average first delivery **22.73/23.73** rounds, and collection
  **96,720/79,960 Ti** candidate versus baseline.  Max p99/peak callback time
  was **1,406/6,432 us**, with zero TLE or suspicious rows.  Raw games are
  `reports/local-20260821T000204Z`; replay diagnostics are under
  `reports/iter-v387-local-recovery/replay-analysis.json`.

## Decision and rollback

Reject v387 without a second screen or long gate.  The 16–14 edge and higher
collection do not clear the 19–11 paired-screen promotion floor, so the result
is not a significant improvement.  The temporary recovery logic, test, and
config were removed.  Rollback focused coverage was **31/31**, compileall
passed, rollback smoke was **4/4** at `reports/local-20260821T000627Z`, and
recursive candidate parity with immutable v0046 is empty at
`reports/iter-v387-local-recovery/rollback-source-parity.diff`.

No promotion, release gate, package, upload, activation, or live transition
occurred.  Immutable v0046 remains the best baseline.

## Follow-up

Do not promote this recovery lease on collection alone.  The next candidate
must address the remaining map-dependent pressure conversion with a distinct
mechanism and clear the paired win-rate floor while preserving delivery and
reliability.
