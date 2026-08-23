# v223 Sentinel-survival reset

Date: 2026-08-18

## Objective

Reset the candidate attacker to the immutable v0042 attacker and test one
replay-backed structural change: choose a forward Sentinel site outside visible
enemy turret fire lines, retain a legal safe exit after construction, and keep
the existing dynamic-cost, economy, pool, blacklist, and watch gates. The
hypothesis was that a durable forward shell would make continuous offense more
reliable without another economy-target detour.

## Scope

- `bots/candidate/bot/attacker.py`;
- `tests/test_candidate_sentinel_survival.py`;
- focused reports and durable iteration metadata.

The attacker was reset to the v0042 snapshot before the change. No dynamic
builder, Store, Launcher, route, map, cost, cap, package, upload, activation,
or live-state logic changed.

## Implementation and review

Luna added only `_visible_enemy_turret_fire_lines` and
`_sentinel_safe_exit_count`, then changed Sentinel candidate selection to reject
visible fire-line sites, require one legal non-fire-line cardinal exit, and rank
legal aligned sites by farther Core standoff with deterministic ties. Existing
`can_fire_from`, `can_build_sentinel`, dynamic pricing, pool, blacklist, and
watch behavior remain gated. Untouched `AttackerMixin` methods are AST-equal to
the v0042 snapshot; candidate attacker SHA is
`96d111d1e61ebded283885fcf50ebc673e8f1428dc525c7e61710a0ac0ba5aa8` versus
v0042 `afa559f98a0694ab6c3355538098a0c845768413652124e08fc9b1035487a01a`.

## Validation

- focused Sentinel and nearest-defense tests: **30/30**;
- compileall: **pass**;
- `make static`: **exit 2**, unchanged inherited profile (15 obsolete
  deleted-module imports and two navigation fast-path assertions);
- `make smoke`: **4/4 command-clean**, report
  `reports/local-20260818T193744Z`;
- rotated 15-map screen, seed **189**: **5-10** candidate-side,
  command/delivery-clean, zero TLE/suspicious rows, collection
  **46,490 vs 67,930 Ti**, mean first delivery **32.13 vs 37.53**, candidate
  no-delivery **0**, max p99/peak **1,327/2,882 us**. Candidate placed
  **1.8 vs 3.9** Sentinels on average and finished with **0.7 vs 1.9** alive;
  it did not improve Sentinel survival or win rate.

## Decision

Rejected at the screen. The safety filter was conservative enough to suppress
the forward shell on several maps without producing a delivery or survival
benefit. No 60-game gate, promotion, package, upload, activation, or live
transition was justified. The immutable v0042 archive remains the baseline;
the candidate-only experiment should not be reused as a starting point without
new replay evidence.

Evidence: `reports/iter-v223-sentinel-survival-reset/`,
`reports/local-20260818T193828Z`.

## Rollback

Because the screen failed, the safe-site hunk and its temporary focused test
were removed. Candidate `attacker.py` now matches the immutable v0042 attacker
byte-for-byte (`afa559f98a0694ab6c3355538098a0c845768413652124e08fc9b1035487a01a`).
Post-rollback focused coverage was **33/33**, compileall passed, and smoke was
**4/4 command-clean** at `reports/local-20260818T194338Z`.
