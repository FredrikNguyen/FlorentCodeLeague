# v347 per-builder route commit — rejected, v0046 retained

Date: 2026-08-20

## Objective and scope

Build on immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`
with a different mechanism from v346's global lease: a Defender would commit
to a concrete visible/advertised ore mission while the opening economy was
below three completed chains, keep that mission while it had a verified Core
sink, and release it on stale/no-progress, visible capacity, or low liquidity.
Released Builders returned to the existing hijack/repair/fallback ladder.

Allowed production scope was `bots/candidate/bot/defender.py` and the
temporary focused `tests/test_candidate_route_commit.py`.  Store schema, Core
spawn policy, fixed identities, route geometry, attacker policy, immutable
snapshots, package, platform, and live state were non-goals.

## Replay basis and implementation

The v346 loss audit (`reports/iter-route-commit-v347-replay-audit.json`) found
late first Harvesters on Royale/Auroraveil and repeated low-conversion rows.
Top-team winners generally established a small route shell before spending
surplus on control.  The initial v347 action order gave every early Defender a
per-unit route commitment before enemy-harvester hijack and selected a target
before spending its first ready turn.  Repair 1 required a concrete
visible/advertised ore target and a local four-source capacity, preventing
Fjordgate's 19-Harvester overcommit and restoring delivery.  Repair 2
generalized capacity to one visible source beyond completed routes and released
when the bank could not fund a Harvester plus two path links.

## Validation

- Initial focused coverage was **37/37**; repair 1 **37/37**; repair 2
  **39/39**.  Rollback coverage was **31/31**.  Compileall passed for every
  candidate and rollback.  `make static` retained the inherited profile
  (obsolete candidate-module imports plus two navigation fast-path
  assertions); no new production-budget failure appeared.
- Smoke was **4/4 command-clean** for initial, repair 1, repair 2, and
  rollback at `reports/local-20260820T102631Z`,
  `reports/local-20260820T103029Z`, `reports/local-20260820T103548Z`, and
  `reports/local-20260820T104021Z`.
- Initial seed-173 was **4-11 candidate-A**, **51,680 vs 88,430 Ti**, with one
  candidate no-delivery row.  Repair 1 corrected the overcommit and reached
  **9-6**, delivery-clean, at **68,750 vs 77,590 Ti** on seed-173 and **7-8**,
  delivery-clean, at **75,830 vs 76,080 Ti** on seed-179; combined repair-1
  result was **16-14**, **144,580 vs 153,670 Ti**.  Reports:
  `reports/iter-route-commit-v347-screen-seed173-analysis.json`,
  `reports/iter-route-commit-v347-repair1-screen-seed173-analysis.json`, and
  `reports/iter-route-commit-v347-repair1-screen-seed179-analysis.json`.
- Repair 2 was **7-8**, **85,130 vs 83,060 Ti** on seed-173 and **8-7**,
  **62,710 vs 63,290 Ti** on seed-179.  Both rotations were delivery-clean
  with zero candidate TLE/suspicious rows, but the combined result was
  **15-15**, only **147,840 vs 146,350 Ti**.  Reports:
  `reports/iter-route-commit-v347-repair2-screen-seed173-analysis.json` and
  `reports/iter-route-commit-v347-repair2-screen-seed179-analysis.json`.

## Decision and rollback

Reject v347 after the two permitted repairs.  The action-order rewrite fixed
one pathological opening, but the win-rate edge did not repeat and the final
collection edge was only **1,490 Ti** across 30 games.  Restore
`bots/candidate/bot/defender.py` byte-for-byte to immutable v0046 and delete
the temporary focused test; `reports/iter-route-commit-v347-rollback-source-parity.diff`
is empty when generated caches are excluded.  No release gate,
promotion, package, upload, activation, or live transition occurred.  Live
v108 remains `active_observing`; immutable v0046 remains the local baseline.

## Remaining risk and next direction

Route ownership is not the only conversion bottleneck: even with concrete
missions, Royale/Auroraveil can build a source and still deliver late or lose
most of its workforce.  The next hypothesis should move to the route FSM's
sink/path lifecycle—verify the first conveyor direction and recover a broken
chain before buying another source—while preserving the existing loaded-
logistics sabotage and home-defense fallbacks.  Do not retry v347's opening
priority or a global lease unchanged.
