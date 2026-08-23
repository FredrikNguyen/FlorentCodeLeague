# v236 Sentinel infiltrator target priority — rejected

## Hypothesis

Enemy Builders can stand on passable hostile logistics. The current Sentinel
finder examines the building first, so a tile containing both a hostile
Conveyor/Splitter and an enemy Builder is treated as infrastructure before the
unit that can continue the infiltration. Reordering the existing occupancy
checks should let the same legal long-range fire handle the Builder without a
new response task or economy detour.

## Scope

- `bots/candidate/main.py` (Sentinel target ordering only);
- one focused target-priority test module;
- durable plan, update, and state metadata.

## Non-goals

No new weapon, turret site/pool/ammo policy, Builder task, route/workforce,
hijack/raid, Launcher/Barrier, Store, map branch, baseline/archive, package,
upload, activation, or live-state change.

## Result

Focused coverage passed **30/30**, compileall passed, smoke was **4/4**, and
static retained the inherited exit 2 (15 obsolete-module errors plus two
navigation fast-path assertions). The rotated 15-map screen was command-clean
but **6-9** for candidate-A; all 15 rows delivered and candidate TLE/suspicious
counts were zero, but Sentinel placements averaged **2.67** versus **3.87** for
v0042 and no map or infiltration-response edge appeared. Full screen and
analysis are in `reports/local-20260819T000615Z` and
`reports/iter-v236-sentinel-infiltrator-target-priority/replay-analysis.json`.

The target-order edit was removed without a repair. Rollback coverage passed
**27/27**, compileall passed, rollback smoke was **4/4**, and the candidate
tree is recursively byte-identical to immutable v0042. Rollback evidence is in
`reports/iter-v236-sentinel-infiltrator-target-priority/rollback-focused.log`,
`rollback-compileall.log`, and `rollback-smoke.log` (smoke report
`reports/local-20260819T000956Z`). No promotion, package, upload, activation,
or live-state transition occurred.
