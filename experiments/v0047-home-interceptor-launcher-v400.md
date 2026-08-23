# v400 Home-interceptor Launcher pulse (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v400 tested a defensive control response for the replay shape seen on Royale,
Drakkarfjord, and Glacierkeep: after five completed routes, the nearest local
dynamic Builder facing a visible enemy Builder could build one reserve-funded
home Launcher to eject the infiltrator.  The initial candidate capped visible
home Launchers at two (including the opening relay).  The bounded repair also
required the Core's current defense designation, a target within squared
distance 25 of our Core, and round <= 240.  The helper preserved a Harvester,
two Conveyor links, and the fixed attack reserve before spending Launcher cost.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage was
temporary additions to `tests/test_candidate_nearest_defense.py`.  Route FSM,
Harvester selection, spawning, Store schema, fixed attackers, Sentinel and
Barrier policy, package, upload, activation, and live state were non-goals.

## Validation

- Initial focused coverage was **35/35**, compileall passed, smoke was **4/4**;
  `make static` retained the inherited 15 obsolete-module imports and two
  navigation fast-path assertions.  Logs are in
  `reports/iter-v400-home-launcher/`.
- Initial rotated all-map screen (`screen_seed=1429`) was **17-13**, with
  **30/30** candidate and comparator deliveries, zero command failures/TLEs/
  suspicious rows, max p99/peak **1,321/5,707 us**, and collection
  **150,050/150,030 Ti**.  Raw games are under
  `reports/local-20260821T050118Z` and diagnostics are in
  `reports/iter-v400-home-launcher/replay-analysis.json`.
- Replay review found a lifecycle defect in the initial cap: Royale placed six
  candidate Launchers over a long game as destroyed visible relays reopened
  the count.  This was the one bounded repair allowed by the iteration.
- Repair focused coverage remained **35/35**, compileall and smoke **4/4**;
  static retained the same inherited profile.  The rotated repair screen
  (`screen_seed=1451`) tied **15-15**, with **30/30** deliveries and zero
  command/TLE/suspicious rows, max p99/peak **1,402/3,161 us**, and collection
  **182,140/152,670 Ti**.  Candidate Launcher placements were bounded to at
  most two per replay.  Raw games are under
  `reports/local-20260821T050624Z`; diagnostics are in
  `reports/iter-v400-home-launcher/repair-replay-analysis.json`.

## Decision and rollback

Reject v400: the initial 17-13 edge missed the 19-11 screen floor, and the
bounded lifecycle repair tied 15-15.  Temporary production and focused-test
edits were removed; recursive candidate production parity with immutable v0047
is exact.  Rollback focused coverage was **32/32**, compileall passed, smoke
was **4/4** at `reports/local-20260821T051053Z`, and static retained only the
known inherited failures.  No release, package, remote gate, upload,
activation, or baseline transition occurred.

## Remaining risk

The opening Launcher remains useful, but a threat-triggered second home relay
did not convert the local infiltration signal into a repeatable win edge.  The
next candidate must use a distinct conversion or defensive-topology mechanism
and must compare against immutable v0047; do not widen this Launcher quota.
