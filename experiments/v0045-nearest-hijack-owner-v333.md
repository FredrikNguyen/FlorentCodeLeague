# v333 — deterministic nearest enemy-Harvester owner (rejected)

## Objective and scope

Top-team replays use enemy logistics as a pressure source, while our dynamic
workers independently select the same visible enemy Harvester and can duplicate
the same hijack detour.  v333 added a local ownership contract: fixed attackers
never claim an enemy source, and among visible non-attacker Builders only the
nearest (stable id tie-break) may seed a hijack.  The rule was applied both to
the Dynamic task detector and the Defender's direct SCOUT hijack path; no Store
lease or cross-map claim was introduced.

Production scope was `bots/candidate/bot/dynamic.py` and
`bots/candidate/bot/defender.py`, with one focused ownership test in
`tests/test_candidate_nearest_defense.py`.  Route FSM, spending, Launchers,
Sentinels, baseline snapshots, package, upload, activation, and live state
were out of scope.

## Validation

- Focused coverage passed **41/41**, compileall passed, and smoke was **4/4**
  at `reports/local-20260820T044614Z`.
- `make static` retained the inherited 15 obsolete-module imports and two
  navigation fast-path assertions; no v333-specific failure appeared
  (`reports/iter-v333-hijack-owner-static.log`).
- The rotated 15-map screen was command-clean but **7-8 candidate-A**;
  collection was **58,500 vs 73,080 Ti**, deliveries **14 vs 15**, and max
  p99/peak was **1,470/5,707 us**.  Reports are
  `reports/local-20260820T044649Z` and
  `reports/iter-v333-hijack-owner-replay-analysis.json`.

## Decision and rollback

Reject v333: visible-source ownership did not create a paired win-rate edge
and reduced aggregate collection.  Remove the temporary helper/call sites and
test; recursive candidate production parity with immutable v0045 is exact, and
rollback focused coverage passed **40/40** at
`reports/iter-v333-hijack-owner-rollback-focused.log`.  No long gate, package,
upload, promotion, activation, or live transition occurred.

## Remaining risk

Duplicate hijack selection is not the dominant loss cause.  The next
fundamental change should target idle workforce conversion and route survival,
using a finite utility/state policy rather than another local ownership gate.
