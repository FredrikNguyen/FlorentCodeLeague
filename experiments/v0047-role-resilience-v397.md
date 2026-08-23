# v397 Fixed-role resilience after confirmed Builder loss (rejected)

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v397 tested whether the Core's fixed attacker/defender Store designations could
be restored after `_prune_dead_builders` confirmed a Builder was destroyed.
The initial candidate repaired stale nonzero slots with deterministic unused
live Builder ids (defender first).  The bounded repair selected the nearest
known-live worker for the economy floor and the farthest known-live worker for
attacker pressure, and reset stale chain state when a worker became an
attacker.  Temporary production scope was `bots/candidate/bot/core_role.py`
and `bots/candidate/main.py`, with focused coverage in
`tests/test_candidate_economy_phase.py`; no Store schema, route geometry,
prices, map branches, baseline/archive, package, upload, activation, or live
state changed.

## Evidence

- Focused coverage was **38/38** for the initial candidate and repair; rollback
  coverage was **36/36**.  Candidate compileall passed for all attempts and
  rollback.  Smoke was **4/4** for the candidate and rollback.
- `make static` remained the inherited **exit 2** profile (15 obsolete import
  errors and two navigation fast-path assertions); no v397-specific failure
  appeared.  Logs are under `reports/iter-v397-role-resilience/`.
- Initial rotated all-map screen (`screen_seed=1183`) was **16–14**, with
  30/30 candidate deliveries, zero TLE/suspicious rows, and max p99/peak
  **1,309/4,813 us** (`reports/local-20260821T034711Z`).
- Bounded repair screen on the same schedule was **19–11**, with 30/30
  deliveries, zero TLE/suspicious rows, and max p99/peak **1,294/4,352 us**
  (`reports/local-20260821T035218Z`).
- Independent rotated screen (`screen_seed=1229`) was **17–13**, with 30/30
  deliveries, zero TLE/suspicious rows, and max p99/peak **1,292/5,603 us**
  (`reports/local-20260821T035605Z`).
- The 60-game release gate on endpoint seeds `[1, 101]` was **29–31**, below
  the **33–27** release floor.  Candidate delivery was **58/60** versus the
  comparator's 60/60; TLE/suspicious rows were zero and max p99/peak was
  **1,450/5,077 us** (`reports/local-20260821T035952Z`).  Royale was 0–4.

## Decision and rollback

The independent screen and release gate did not establish a reliable edge over
v0047.  v397 is rejected; both repairs were bounded and no further attempt is
authorized in this iteration.  Temporary source, test, and config edits were
removed.  Recursive production parity with immutable v0047 is exact; focused
rollback tests, compileall, and smoke passed.  No release package, remote gate,
upload, activation, or baseline transition occurred.  Keep v0047 as baseline
and do not revive this role-slot reassignment unchanged.

## Reports

- `reports/iter-v397-role-resilience/`
- `reports/local-20260821T034711Z`
- `reports/local-20260821T035218Z`
- `reports/local-20260821T035605Z`
- `reports/local-20260821T035952Z`
- `reports/local-20260821T040746Z`
