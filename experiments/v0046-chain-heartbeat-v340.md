# v340 — packed chain-heartbeat ownership signal

Date: 2026-08-20

## Hypothesis and scope

v339 showed that a visible route sink proof cannot tell an active opening
frontier from a dead mature route.  v340 tested a shared, bounded ownership
signal without changing route geometry: slot 11 retained the completed-route
count in its low bits and carried an active Builder id/round lease in its high
bits.  A fresh opening lease suppressed duplicate orphan recovery; the owner
could recover its own stalled route, and mature recovery was released after a
route had delivered.  Heartbeat renewal was guarded against overwriting a
different fresh owner because Store writes are delayed and last-writer-wins.

Allowed production files were `bots/candidate/bot/constants.py`,
`main.py`, `bot/core_role.py`, `bot/defender.py`, `bot/dynamic.py`, and
`bot/attacker.py`, with focused coverage in
`tests/test_candidate_nearest_defense.py`.  No baseline or immutable snapshot,
opening spend, role policy, navigation, combat policy, package, platform, or
live-state file was changed.

## Validation

- Initial focused coverage was **38/38**; repair 1 was **39/39**; repair 2 was
  **40/40**.  Compileall passed after each version.
- Initial 15-map screen: **3-12 candidate-A**, with zero command/TLE/suspicious
  rows.  Repair 1 restored **7-8**.  Repair 2 reached **8-7**, delivered on
  all 15 games, and collected **95,540 vs 82,670 Ti**.  Reports:
  `reports/iter-chain-heartbeat-v340-screen-analysis.json`,
  `reports/iter-chain-heartbeat-v340-repair1-screen-analysis.json`, and
  `reports/iter-chain-heartbeat-v340-repair2-screen-analysis.json`.
- The required 60-game endpoint/side gate was command-clean at **32-28**,
  but collection was **295,840 vs 309,120 Ti**.  One candidate-side-B
  Drakkarfjord game had no candidate titanium delivery while v0046 delivered.
  Max p99/peak callback time was **1,425/5,540 us**; TLE and suspicious rows
  were zero.  Full analysis:
  `reports/iter-chain-heartbeat-v340-release-analysis.json`.
- `make static` retained the inherited repository profile (15 obsolete-module
  import errors and two navigation fast-path assertions).  Rollback `make
  smoke` was **4/4 command-clean** at
  `reports/local-20260820T073829Z`.  Rollback focused coverage was **35/35**
  and compileall passed.

## Decision and rollback

Reject v340 after the two permitted bounded repairs.  The aggregate 32-28
  edge is not releasable because it loses aggregate collection and introduces
  a no-delivery row.  Restore recursive production parity with immutable v0046;
  proof is `reports/iter-chain-heartbeat-v340-rollback-source-parity.diff`.
  No 60-game promotion, package, upload, activation, or live transition
  occurred; live state remains v108 `active_observing` with v107 known-good.

## Follow-up

Do not retry a shared heartbeat in slot 11: delayed multi-writer Store updates
make the ownership lease contend with completed-route progress.  The next
fundamental rewrite should keep route progress local and deterministic—one
Builder must own a visible route frontier through its existing FSM, while
other Builders continue harvesting or repairing independently—without adding a
new shared Store field or a global opening lock.  Reinspect top-team replays
for route throughput and late resource conversion before editing.
