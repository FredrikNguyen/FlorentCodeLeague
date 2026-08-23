# v209 — route-stall rendezvous lease feasibility checkpoint

## Objective and scope

Use two Luna workers in parallel: freeze the current candidate for a baseline
screen while a second worker attempts the one bounded replay-derived
route-stall Launcher rendezvous hypothesis. The proposed lease would name a
stalled route owner, require a dynamic Harvester-plus-two-Conveyors reserve,
and give one Launcher a short legal pickup/reposition window. No production
change was allowed if the coordination channel could not be represented safely
with the existing Store schema.

## Parallel evidence

- The evaluation worker snapshotted the candidate before any implementation
  edit at `/tmp/fcl-v208-snapshot.XhhR6m` (recursive hash
  `112f13daa8be...`) and ran the rotated seed-172 screen against exact v0042.
- The 15-game screen was **5-10** candidate-A wins, **15/15 command-clean**,
  delivery-clean (zero no-delivery rows), with zero TLE/suspicious output.
  Candidate collection was **44,120 vs 54,980 Ti**; max p99/peak was
  **1,312/5,174 us**. Report:
  `reports/parallel-v208-screen/replay-analysis.json`.
- This is the actual pre-edit worktree comparator. It differs from the older
  archived original-v208 screen (9-6) because the shared candidate already
  contains later unpromoted local changes; it is not evidence for promotion.

## Implementation result

The implementation worker inspected the current Store assignments and stopped
without production edits. All 16 slots are already owned: core coordinates,
siege beacon, ore cursor/ring, enemy Core, gunner cap, harvester/sentinel
counters, and fixed role IDs. A safe named lease would require reusing ore-ring
slots and guarding delayed writes in ore sharing, target selection, and idle
fallback. That is a Store-schema migration, not a bounded Launcher lifecycle
change, so it was rejected as out of scope. No focused implementation tests
were added and no source was changed by v209.

## Checkpoint checks

- Existing Launcher lifecycle focused tests: **5/5**;
  `reports/iter-v209-rendezvous-lease/focused.log`.
- Candidate compileall: **pass**;
  `reports/iter-v209-rendezvous-lease/compileall.log`.
- `make static`: **exit 2**, unchanged inherited deleted-module imports and
  two navigation fast-path assertions;
  `reports/iter-v209-rendezvous-lease/static.log`.
- `make smoke`: **4/4 command-clean**;
  `reports/iter-v209-rendezvous-lease/smoke.log` and
  `reports/local-20260818T152217Z`.

## Decision and next step

Do not promote, package, upload, activate, or alter the immutable v0042
baseline. Preserve the current candidate and both Luna reports. The next
hypothesis must either use an already-owned coordination signal with no Store
schema migration or return to replay analysis for a unit-control strategy that
does not require cross-unit leases. Keep the parallel snapshot-before-edit
workflow for subsequent iterations.
