# v127 — late economy steward (rejected)

## Objective

Recover from late route/Harvester attrition by leasing one visible, non-floor
dynamic Builder back to the harvest/explore loop after round 180, then delay
that lease to round 300 in the bounded repair. The hypothesis was motivated by
v0037 losses on Auroraveil, Royale, and Yulerune where the historical route
counter stayed high while only one to four Harvesters remained alive.

## Scope

- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- `reports/iter-economy-steward-v127/`

No fixed attacker, route executor, Store schema, baseline archive, package,
upload, activation, or live state was changed.

## Evidence

- Focused checks: 26/26 passed after one missing-import repair.
- Candidate compile: passed.
- `make smoke`: 4/4 command-clean (`reports/local-20260817T090215Z`).
- `make static`: inherited exit 2 from obsolete imports and two navigation
  fast-path assertions (`static.log`).
- Initial 24-game screen: 12-12, 76,660 versus 81,170 collected titanium;
  zero command failures/TLE/suspicious output; max p99 1,427 us.
- Repair 1 delayed the lease to round 300. Focused/compile/smoke passed again;
  the repeated 24-game screen was 13-11 but collected 92,210 versus 98,710;
  zero command failures/TLE/suspicious output; max p99 1,381 us.

## Decision

Reject. The repair did not show a significant win-rate or collection gain
over immutable v0037. The steward and tests were removed with `apply_patch`;
candidate source now compares byte-for-byte with the v0037 archive. Rollback
focused checks passed 23/23, compile passed, and rollback smoke was 4/4
(`reports/local-20260817T091120Z`). No 54/210 gate, package, upload, or live
operation was performed.

## Next hypothesis

Inspect why the weak maps lose after successful delivery and test one bounded
route-continuity/conversion change from v0037, preserving the fixed-attacker
sabotage pulse and requiring a short win-rate improvement before any longer
gate.
