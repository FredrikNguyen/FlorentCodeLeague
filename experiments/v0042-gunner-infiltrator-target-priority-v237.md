# v237 Gunner infiltrator target priority — rejected after one repair

## Hypothesis

Gunners are the existing, already-funded home response with more opportunities
to see an infiltrator than a forward Sentinel. A hostile Builder can stand on a
Conveyor/Splitter and become the valuable target in the current firing line.
Prefer that Builder only when `can_fire` confirms the target is legal; retain
the engine's nearest occupied tile and all existing rotation behavior otherwise.

## Scope

- `bots/candidate/main.py` (Gunner target selection only);
- one focused Gunner targeting test module;
- durable plan, update, and state metadata.

## Non-goals

No Builder task, body-block, route/workforce/hijack/raid, turret purchase/cap,
ammo, Sentinel, Launcher, Barrier, Store, map, baseline/archive, package,
upload, activation, or live-state change.

## Validation and decision

The broad selector passed **30/30** focused tests, compileall and smoke
**4/4**, with static retaining the inherited exit 2. Its first 15-map screen
was **9-6**, collecting **77,910 vs 62,100 Ti**, and both sides delivered on
all 15 rows (`reports/local-20260819T001506Z`; analysis in
`reports/iter-v237-gunner-infiltrator-priority/replay-analysis.json`). An
independent seed-173 screen reversed to **6-9**, **62,730 vs 70,710 Ti**, with
zero candidate TLE/suspicious rows (`reports/local-20260819T001736Z`; analysis
`replay-analysis-173.json`).

The one bounded repair restricted the override to the exact nearest target
tile, requiring a shared hostile Builder/building overlap. Focused coverage
was **31/31**, compileall and smoke **4/4**, static was unchanged, and seed
174 was only **7-8**, collecting **70,140 vs 70,830 Ti**; candidate delivered
15/15 while baseline delivered 14/15, and candidate TLE/suspicious counts were
zero (`reports/local-20260819T002020Z`; analysis `replay-analysis-174.json`).

The hypothesis is rejected after its allowed repair. Temporary source/test
edits were removed; rollback coverage passed **27/27**, compileall passed,
static retained exit 2, rollback smoke was **4/4**, and candidate Python is
recursively byte-identical to immutable v0042 (`reports/local-20260819T002228Z`).
No 60-game gate, promotion, package, upload, activation, or live-state
transition occurred.
