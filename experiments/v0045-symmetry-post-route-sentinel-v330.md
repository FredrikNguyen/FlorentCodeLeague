# v330 — symmetry-backed post-route Sentinel pressure (rejected)

## Objective and scope

Remote v108 replays showed games where the candidate delivered early but never
converted that income into a durable forward damage source.  Top-team winners
maintained several Sentinels and control buildings while the candidate often
waited for visual enemy-Core intel.  v330 tested one structural discovery
escape: after a completed route, an open-map attacker could place exactly one
reserve-backed Sentinel aimed at the map-symmetric enemy Core before visual
confirmation.  The placement still used `can_fire_from` and `can_build_sentinel`;
the guessed placement was never repeated after destruction.

Production scope was `bots/candidate/main.py` and
`bots/candidate/bot/attacker.py`, with two focused tests in
`tests/test_candidate_v319_launcher.py`.  No Store schema, route/workforce
policy, Launcher lifecycle, spending rule, baseline snapshot, package, upload,
activation, or live state changed.

## Validation

- Focused coverage passed **42/42**; compileall passed; smoke was **4/4** at
  `reports/local-20260820T040640Z`.  Static retained only the known inherited
  15 stale-module imports and two navigation fast-path assertions;
  `reports/iter-v330-symmetry-pressure-static.log`.
- The rotated 15-map screen was **9-6 candidate-A**, command-clean, with no
  TLE/suspicious rows; report `reports/local-20260820T040727Z` and replay
  analysis `reports/iter-v330-symmetry-pressure-replay-analysis.json`.
- The full 60-game gate was command-clean but **29-31 candidate-A**, with
  collection **307,210 vs 314,100 Ti**, one comparator no-delivery row, and
  max p99/peak **1,379/5,195 us**.  Reports are
  `reports/local-20260820T040930Z` and
  `reports/iter-v330-symmetry-pressure-release60-analysis.json`.

## Decision and rollback

Reject v330.  The screen edge did not survive the side-swapped map/seed gate,
so no remote gate, package, upload, promotion, or deployment was justified.
The temporary state, Sentinel predicate, and tests were removed; exact
recursive candidate production parity with immutable v0045 is restored.  The
rollback focused suite passed **40/40**, compileall passed, smoke was **4/4** at
`reports/local-20260820T041718Z`, and static retained the inherited profile at
`reports/iter-v330-symmetry-pressure-rollback-static.log`.  Platform v108
remains guarded `active_observing`.

## Remaining risk

Symmetry can identify a target but cannot solve the observed long-run workforce
and route-survival deficit.  The next structural candidate should coordinate a
real assault/relay wave or route redundancy rather than spend a blind fixed
facing turret.
