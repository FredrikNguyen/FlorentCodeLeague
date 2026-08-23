# v395 pending-route commit before survival flee (rejected)

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward`, v395 tested a narrow
route-commit hypothesis: when a chain Builder was standing in a visible enemy
turret line on the round after moving, it could commit an already-adjacent
pending Conveyor before taking the normal survival detour. The repair narrowed
that exception to a pending tile that was verified to feed directly into the
own Core. The production experiment touched only `main.py` and `bot/defender.py`
plus one deterministic focused regression in
`tests/test_candidate_nearest_defense.py`; the temporary screen config was
removed after rollback. Store schema, spending, spawning, combat targets,
route topology, packaging, upload, activation, and live state were out of
scope.

## Evidence

The initial rotated 30-game all-map screen (`screen_seed=1103`) scored **13-17**
for the candidate against v0047. The candidate delivered in 28/30 games versus
30/30 for the comparator; command returns were clean and replay diagnostics
reported zero TLE and suspicious-output rows (max p99/peak 1,340/3,543 us).
Replay inspection showed losses with reduced Harvester/workforce conversion:
the exception kept exposed Builders in turret lines for non-final route links,
so the survival trade was larger than the route value.

Repair 1 restricted the exception to a verified final Core-feeding pending
segment. Its fresh rotated 30-game screen (`screen_seed=1129`) improved to
**15-15**, with 29/30 candidate deliveries versus 30/30 for v0047 and zero
TLE/suspicious rows (max p99/peak 1,246/5,981 us). It still missed the **19-11**
promotion floor, so no second screen, long gate, release gate, package, remote
gate, baseline transition, or live operation was justified.

## Validation and rollback

Focused coverage passed **33/33** for both candidate attempts; compileall
passed; `make smoke` was **4/4** for both attempts and again **4/4** after
rollback (`reports/local-20260821T025903Z`). `make static` retained the known
repository exit-2 profile (obsolete deleted-module imports and two navigation
assertions) with no v395-specific failure. After removing the helper, dispatch
call, regression, and temporary config, recursive production parity with
immutable v0047 was exact (`rollback-source-parity.diff`).

Reject v395 after the two unsuccessful screens. Keep v0047 as the strongest
local baseline and do not revive the survival-commit exception unchanged.

## Reports

- `reports/iter-v395-route-commit/`
- `reports/local-20260821T025054Z`
- `reports/local-20260821T025528Z`
- `reports/local-20260821T025903Z`
