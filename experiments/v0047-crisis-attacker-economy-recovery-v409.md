# v409 pre-Sentinel crisis attacker economy recovery — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable
`v0047_pressure-economy-steward_20260821-0200_eeafad8f`, v409 tested one
role-flexibility contract from the v0047 loss audit.  When the Core published
`CRISIS`, no forward Sentinel was recorded, and the bank could not afford the
next Harvester, a fixed attacker temporarily entered the existing economy FSM.
Active chains always finished first.  The crisis path suppressed enemy-
Harvester hijacks, ore turrets, Gunners, siege Barriers, Launcher work, and
idle enemy chip attacks; normal pressure resumed after the crisis condition
cleared or a Sentinel existed.

Production scope was limited to `bots/candidate/bot/attacker.py`,
`bots/candidate/bot/defender.py`, and `bots/candidate/main.py`, with temporary
legality/phase coverage in `tests/test_candidate_crisis_attacker.py` and
temporary screen/release configs.  Route geometry, Store schema, prices,
spawning, Sentinel placement, baseline snapshots, package, upload, activation,
and live state were non-goals.

## Validation

- Broad candidate focused coverage was **41/41**, then **42/42** after the one
  bounded repair; compileall passed and smoke was **4/4** for both attempts.
  `make static` retained the inherited exit-2 profile (15 obsolete imports and
  two navigation assertions), with no v409-specific failure.
- Initial 30-game all-map screen (`screen_seed=211`) was **10-20**, with
  30/30 deliveries on both sides, zero command/TLE/suspicious rows, collection
  **178,070 vs 196,030 Ti**, and max p99/peak **1,367/6,432 us**.
- The bounded repair required actual Harvester unaffordability in addition to
  the shared CRISIS/no-Sentinel signal.  Its independent screen
  (`screen_seed=223`) reached **19-11**, 30/30 deliveries, zero
  command/TLE/suspicious rows, collection **181,780 vs 161,290 Ti**, and max
  p99/peak **1,381/5,969 us**.  This cleared the short-screen floor but was
  not sufficient for promotion.
- The complete 60-game endpoint-seed/both-side gate was **30-30**, with
  **60/60** deliveries on both sides, zero TLE/suspicious rows, max p99/peak
  **1,511/4,200 us**, and collection **311,540 vs 304,910 Ti**.  Map splits
  included Antler, Auroraveil, Drumlin, Frostgate, and Valkyrie at 1-3;
  Royale was 4-0.  Raw evidence is
  `reports/local-20260821T075204Z`.

## Decision and rollback

Reject v409: the release gate tied and did not establish a reliable win-rate
edge over v0047 despite the repaired screen.  Temporary source/test/config
edits were removed; recursive candidate production parity with immutable v0047
is exact at `reports/iter-v409-crisis-attacker-rollback-source-parity.diff`.
Rollback focused coverage was **36/36**, compileall passed, rollback smoke was
**4/4**, and rollback static retained the inherited failures.  No release
package, remote gate, upload, activation, or baseline transition occurred.

The evidence rules out a broad fixed-attacker crisis handoff as a reliable
conversion fix.  Keep v0047 as the moving baseline; the next hypothesis must
target map-conditioned route/pressure conversion without removing the fixed
attacker from its pressure lane during ordinary income quiet periods.
