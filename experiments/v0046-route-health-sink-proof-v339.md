# v339 — bounded route-health sink proof

Date: 2026-08-20

## Hypothesis and scope

The Glacierkeep no-delivery replay showed that an adjacent Conveyor can look
healthy while its downstream path ends at a visible gap.  Top-team replays
also showed that connected, rapidly expanding belts outperform many isolated
branches.  v339 tested one structural change on immutable v0046: trace a
bounded visible fixed-output Conveyor walk and classify it as Core-connected,
proven dead, or unobservable.  Mature routes could merge into a proven Core
path, and mature orphan Harvesters could request a local recovery seed.  An
opening guard was added after the first screen so incomplete first-route
frontiers retained the legacy Core-only behavior.

Production scope was `bots/candidate/bot/defender.py`; focused coverage was in
`tests/test_candidate_nearest_defense.py`.  No baseline/snapshot, Store schema,
role or spending policy, navigation, combat, package, upload, activation, or
live-state file was changed.

## Validation

- Initial focused route/defense/economy subset: **39/39**; compileall passed.
- Initial 15-map screen: **7-8 candidate-A**, zero TLE/suspicious rows.  The
  candidate lost its economy opening on several maps (for example, 3 versus
  15 placed Harvesters on Icefloe and 3 versus 6 on AuroraVeil), indicating
  that visible incomplete frontiers were being mistaken for repairable dead
  routes.  Replay analysis: `reports/iter-route-health-v339-screen-analysis.json`.
- Bounded repair: preserve legacy opening topology until one route is recorded;
  focused subset remained **39/39**, compileall passed, and the repeated screen
  remained **7-8 candidate-A**, with zero TLE/suspicious rows and max
  p99/peak callback time **1,296/3,175 us**.  Replay analysis:
  `reports/iter-route-health-v339-repair1-screen-analysis.json`.
- `make static` retained the inherited repository profile (15 obsolete-module
  import errors and two navigation fast-path assertions); no v339-specific
  static failure appeared.  `make smoke` was **4/4 command-clean** at
  `reports/local-20260820T070806Z`.

## Decision and rollback

Reject v339: the route proof was reliability-clean but had no repeatable paired
win-rate or collection edge after one bounded repair.  The candidate
`defender.py` was restored byte-identically to immutable v0046 (SHA-256
`99c9a0154174b272c8a3d249a9776f1554fd35161953b28a162bfaee81ae133c`), proven
by `reports/iter-route-health-v339-rollback-source-parity.diff`.  Rollback
focused coverage was **35/35**, compileall passed, static retained its
inherited profile, and rollback smoke was **4/4** at
`reports/local-20260820T070806Z`.  No 60-game gate, package, upload,
activation, promotion, or live transition occurred.

## Follow-up

Do not retry this sink verifier unchanged.  A future route experiment needs an
explicit shared chain-progress/ownership signal that distinguishes an active
frontier from a dead post-delivery route before enabling recovery; topology
proof alone is too eager during the opening.
