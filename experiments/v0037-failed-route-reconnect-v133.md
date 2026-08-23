# v133 failed-route reconnect rejected — 2026-08-17

## Objective and scope

The v0037 replay review found five no-delivery losses with a live Harvester
and a long conveyor trunk. The hypothesis was that the Builder owning a failed
chain should retain its source position and get one bounded, source-local seed
retry instead of abandoning the orphaned Harvester. The candidate changed only
`bots/candidate/main.py`, `bots/candidate/bot/constants.py`,
`bots/candidate/bot/defender.py`, and the focused nearest-defense tests. The
retry required at least four laid links, expired after 60 rounds, and repair 1
allowed it only before any completed route was visible in the Store.

No baseline snapshot, platform state, package, upload, or activation was
changed.

## Validation

- Initial focused route/defense/cage/seed suites passed 27/27; compileall
  passed; `make smoke` was 4/4 (`reports/local-20260817T110256Z`). `make
  static` retained the inherited 15 obsolete-import errors and two navigation
  fast-path assertions (`reports/iter-failed-route-reconnect-v133-static.log`).
- Initial 54-game screen versus immutable v0037: **29-25**, 204,470-204,200
  collected titanium, two versus four no-delivery rows, zero command/TLE/
  suspicious-output failures, maximum p99 1,470 us and peak callback 5,424 us.
  Runner report: `reports/local-20260817T110346Z`.
- The release-sized 210-game gate then regressed to **100-110**,
  924,790-941,070 titanium, two versus five no-delivery rows, zero reliability
  failures, maximum p99 1,470 us and peak callback 5,424 us. Map regressions
  were strongest on frostgate (4-10), glacierkeep (5-9), nordkap (4-10), and
  fjordgate (6-8). Runner report: `reports/local-20260817T110945Z`.
- Repair 1 added the first-delivery-only guard. Focused tests passed 26/26,
  compileall passed, `make smoke` was 4/4 (`reports/local-20260817T113117Z`),
  and static remained inherited red. The 54-game screen regressed to **26-28**,
  207,910-217,000 titanium, two versus one no-delivery rows, max p99 1,494 us,
  peak 5,777 us, and zero reliability failures. Runner report:
  `reports/local-20260817T113144Z`.

## Decision and rollback

Rejected after the initial candidate plus one bounded repair. Delivery timing
improved (candidate mean first delivery was 30.05 turns versus 40.55 for the
comparator in the 210-game run), but the source-local detour cost too many
wins on protected maps. Candidate Python sources are restored byte-for-byte to
`bots/versions/v0037_attacker-sabotage-pulse_20260817-0851_eeafad8f`; rollback
focused tests passed 23/23, compileall passed, rollback smoke was 4/4
(`reports/local-20260817T113900Z`), and static remains the inherited failure
(`reports/iter-failed-route-reconnect-v133-rollback-static.log`).

The next iteration must target a different structural lever; do not retune
source-local orphan retries without new replay evidence.
