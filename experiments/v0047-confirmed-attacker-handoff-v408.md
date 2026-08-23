# v408 confirmed-dead fixed-attacker handoff — rejected

Date: 2026-08-21

## Objective and evidence

The v0047 release-loss audit showed materially more Builder deaths and fewer
forward Sentinels on losses than on wins.  v408 tested whether a confirmed-dead
fixed-attacker Store slot could be handed to an already-fielded non-floor
Builder, without spawning a replacement or changing the Store layout.  The
handoff was delayed until the three-route offense milestone and never
interrupted an active CHAIN; the promoted Builder cleared its dynamic task and
entered the existing attacker policy only while in SCOUT mode.

## Scope and non-goals

- `bots/candidate/bot/core_role.py` and `bots/candidate/main.py` were the
  temporary production scope;
- `tests/test_candidate_attacker_reassignment.py` covered confirmed-death,
  delayed-opening, promotion, chain preservation, and permanent-Defender
  guards;
- `experiments/.tmp-v408-attacker-handoff.toml` supplied the rotated screen.

No opening spend, route FSM, Harvester selection, Sentinel/Barrier/Launcher
purchase policy, Store schema, baseline snapshot, package, upload, activation,
or live state was intended to change.

## Validation

- Initial focused coverage was **36/36**, candidate compileall passed, and the
  v0047 smoke was **4/4** command-clean (`reports/iter-v408-attacker-handoff/`).
  `make static` retained the inherited exit-2 profile: 15 obsolete imports and
  two navigation fast-path assertions.
- The rotated 30-game screen (`screen_seed=188`) was **17-13**, with 30/30
  deliveries on both sides, zero command failures/TLEs/suspicious rows,
  collection **163,450 vs 172,840 Ti**, and max p99/peak **1,564/6,489 us**.
  Raw games are `reports/local-20260821T071921Z`.
- Replay counts showed the candidate converted more Harvesters but placed
  fewer Conveyors, Barriers, and Sentinels than v0047, so the handoff was
  deferred behind the three-route milestone as the one bounded repair.
- Repair focused coverage remained **36/36**, compileall passed, smoke was
  **4/4**, and scoped `git diff --check` passed.  The rotated 30-game repair
  screen (`screen_seed=199`) fell to **13-17**, with 30/30 deliveries,
  zero command failures/TLEs/suspicious rows, collection **123,940 vs
  141,790 Ti**, and max p99/peak **1,457/2,721 us**.  Raw games are
  `reports/local-20260821T072452Z`.

## Decision and rollback

Reject v408 after the two allowed screens; neither met the 19-11 paired
promotion floor and the repair regressed.  The temporary production/test/config
edits were removed.  Recursive candidate parity with immutable v0047 is zero
(`reports/iter-v408-attacker-handoff/rollback-source-parity.diff`).  Rollback
focused coverage was **36/36**, compileall passed, rollback smoke was **4/4**,
and rollback static retained the same inherited failures.  No release gate,
package, remote gate, upload, activation, or baseline transition occurred.

The confirmed-death role gap remains an observed but unproven risk; future
work should target route conversion or pressure allocation without promoting
economy workers into attackers during a live match.
