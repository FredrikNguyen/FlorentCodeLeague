# v215 — raid-first offense lease (approved)

## Replay basis

The v214 seed-179 loss timeline showed the intel-backed advance lease moving
some builders forward but still leaving several maps with a single Sentinel and
long economy plateaus. The existing dynamic `_find_raid_target` already ranks
loaded enemy Conveyors/Splitters and Harvesters and assigns one nearest owner,
but v214's advance phase was selected before that selector, so a funded builder
could march past a visible income line without sabotaging it. Top-team replays
show the opposite conversion: break a loaded logistics tile, then resume the
pressure lane while the route owner keeps delivery alive.

## Approved bounded hypothesis

Keep the v214 shared-intel read and SCOUT offense lease contract, but place the
existing nearest-owner `TASK_RAID` decision before the `TASK_ADVANCE` fallback.
Only the existing economy, confirmed-Core, Sentinel/live-shell, titanium
reserve, nearest ownership, danger, and action-legality gates may authorize the
raid; once the target is gone, normal repair handoff and continuous advance
resume. Visible ore remains behind both raid and advance during the funded
phase. This is a priority/phase change, not a new raid primitive.

## Allowed files

- `bots/candidate/bot/dynamic.py` for shared intel and raid/advance ordering;
- one focused raid-first offense/ownership/legality test module;
- this experiment record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable
  report/state metadata.

## Non-goals

No new Store slot/schema, new sabotage/takeover primitive, weapon/Barrier/
Sentinel-cap change, reserve or cost tuning, route-chain rewrite,
permanent-role or fixed-attacker change, map branch, baseline/archive/package,
upload, activation, or live-state change. Do not interrupt urgent home threat,
belt/base repair, enemy Harvester hijack, or active CHAIN work.

## Done criteria

Focused tests prove loaded-raid precedence, no-raid advance fallback, shared
Core/milestone gates, nearest ownership, stale-target handoff, and legal fire/
movement. Candidate compileall, static, and smoke retain the inherited profile.
A fresh rotated 15-map screen against exact v0042 must be command-clean with no
TLE, suspicious-output, or new no-delivery rows and show a clear aggregate
win-rate edge without a protected-map collapse. Run the 60-game gate only after
that screen; otherwise restore the exact pre-v215 snapshot and do not promote.

## Implementation and gate result

Luna's session stalled before producing a durable patch; root completed the
same bounded reorder from the approved scope. Focused coverage was **5/5** in
the new raid-first module and **42/42** in the root subset, including
continuous-offense, launcher, nearest-defense, and seeded-route regressions.
Candidate compileall passed, `make smoke` was **4/4** at
`reports/local-20260818T174349Z`, and `make static` retained only the
inherited exit 2 (15 obsolete deleted-module imports and two navigation
fast-path assertions). The rotated 15-map screen was command- and
delivery-clean at **8-7** candidate-side, so the 60-game gate was run.

The release matrix was also command-clean and delivery-clean with zero TLE or
suspicious rows. Candidate won **32-28 (53.33%)** and collected
**286,570 vs 232,590 Ti**, with mean first delivery **27.51 vs 30.77**. The
edge was not reliable across maps: Ragnarok was **0-4**, and Fjordgate and
Glacierkeep were each **1-3**. Max p99/peak execution was **1,314/6,807 us**.
The protected-map/no-collapse criterion therefore failed despite the positive
aggregate and better collection.

The exact pre-v215 `dynamic.py` snapshot was restored (SHA-256
`bcaa62c16403024e37a2149659160d04c01ec287d80679394d7bc8d7980651fd`), the
temporary test/config were removed, and rollback coverage was **37/37** plus
compileall. v0042 remains the immutable baseline; no promotion, package,
upload, activation, or live-state transition occurred. Evidence:
`reports/local-20260818T174417Z`, `reports/local-20260818T174619Z`,
`reports/iter-v215-raid-first-offense/`, and this record.
