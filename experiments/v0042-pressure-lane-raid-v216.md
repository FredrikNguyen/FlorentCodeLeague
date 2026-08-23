# v216 — pressure-lane raid lease (rejected)

## Replay basis

The v215 release gate had a positive aggregate but collapsed on Ragnarok
(0-4), with additional 1-3 floors on Fjordgate and Glacierkeep. Its raid-first
lease could pull a dynamic Builder toward a visible logistics tile before the
economy was robust or before the target supported the Core pressure lane.

## Bounded hypothesis

Require four completed routes (one beyond `OFFENSE_MIN_HARVESTERS`), SCOUT
mode, confirmed shared enemy-Core intel, one nearest dynamic owner, a loaded
Conveyor/Splitter target, and strict squared-distance progress toward the Core
before placing the continuous raid lease ahead of visible harvest. Protected
home tasks and CHAIN behavior remain unchanged; the existing post-harvest raid
fallback, attacker, reserve, and unit policies are untouched.

## Validation

Root implemented the scoped branch after the Luna session stalled. Focused
coverage was **8/8** in the new pressure-lane module and **45/45** in the
root subset, compileall passed, smoke was **4/4** at
`reports/local-20260818T180400Z`, and static retained the inherited exit 2
(15 obsolete deleted-module imports and two navigation fast-path assertions).

The rotated 15-map screen was command-clean with zero TLE or suspicious rows,
but candidate-side lost **6-9**. Collection was **47,400 vs 66,380 Ti**, mean
first delivery **45.21 vs 38.07**, and max p99/peak **1,585/5,693 us**. Icefloe
and Nordkap were both losses. The required aggregate and protected-map gates
failed, so no 60-game release matrix ran.

The exact pre-v216 `dynamic.py` snapshot was restored (SHA-256
`bcaa62c16403024e37a2149659160d04c01ec287d80679394d7bc8d7980651fd`), the
temporary test/config were removed, and rollback coverage was **37/37** plus
compileall. v0042 remains the immutable baseline. No promotion, package,
upload, activation, or live-state transition occurred. Evidence:
`reports/local-20260818T180436Z`,
`reports/iter-v216-pressure-lane-raid/`, and this record.
