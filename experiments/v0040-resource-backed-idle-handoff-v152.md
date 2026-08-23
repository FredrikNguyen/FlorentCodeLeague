# v0040 resource-backed idle handoff — v152

Date: 2026-08-17

## Objective

Convert a ready, resource-backed dynamic Builder that is stuck on a targeted
task into another useful local task. The change used a short per-unit lease:
after repeated no-action/no-move rounds with at least the existing 80-Ti
reserve, the Builder released its target, re-picked ordinary work, and in the
final repair preferred a verified logistics raid over the economy fallback.
The Store protocol and fixed role assignments were unchanged.

## Allowed files and non-goals

Allowed source files were `bots/candidate/bot/dynamic.py`,
`bots/candidate/bot/constants.py`, and the dynamic task initialization in
`bots/candidate/main.py`, plus focused coverage in
`tests/test_candidate_nearest_defense.py`. Evaluation configs, this record,
`UPDATES.md`, and durable state were bookkeeping only.

Non-goals were Store slots, conveyor/harvester chain construction, ordinary
task ordering, navigation, fixed attacker/defender roles, unit caps, map
selection, platform state, and live deployment.

## Implementation and bounded repairs

1. Initial handoff: targeted tasks accumulated three ready no-progress rounds,
   set an eight-round local target lease, re-picked, and executed the
   replacement immediately. Focused **21/21**, compileall passed, smoke **4/4**,
   and `make static` retained the inherited 15 obsolete import errors plus two
   navigation fast-path failures. The 54-game screen was **27-27** against
   immutable v0040 (`reports/local-20260817T203728Z`).
2. Repair 1 reduced the trigger to two ready rounds while retaining the 80-Ti
   reserve and eight-round lease. Focused **21/21**, compileall passed, smoke
   **4/4**; the screen remained **27-27** (`reports/local-20260817T204310Z`).
3. Repair 2 made only the handoff selector prefer a verified logistics raid
   before the ordinary harvest fallback. Focused **22/22**, compileall passed,
   smoke **4/4**, and the screen improved to **30-24**, command-clean with no
   stderr (`reports/local-20260817T204905Z`). Final static was recorded in
   `reports/iter-v152-static-final.log` and retained the known inherited red
   result.

## Long gate

The full 210-game matrix was command-clean but reversed the screen edge:
candidate **88-122** versus v0040 (−34 games). Per-map results were:

```text
antler 5-9          archipelago 2-12   auroraveil 4-10
drakkarfjord 5-9   drumlin 6-8        fjordgate 6-8
frostgate 9-5      glacierkeep 4-10   icefloe 5-9
midgard 4-10       nordkap 7-7       ragnarok 4-10
royale 6-8         valkyrie 10-4     yulerune 11-3
```

Replay reliability was clean: zero command failures, zero TLEs, zero
suspicious-output markers, maximum p99 callback **1,491 us**, maximum peak
callback **5,674 us**. Both sides delivered in 208/210 games; candidate and
comparator each had two no-delivery rows. Full report:
`reports/local-20260817T205428Z`.

## Decision and rollback

v152 is **rejected at the long gate**. The screen edge is not durable across
the complete map distribution, so no archive, package, upload, activation, or
baseline transition was performed. `bots/candidate/main.py`,
`bots/candidate/bot/dynamic.py`, and `bots/candidate/bot/constants.py` were
restored byte-identically to
`bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`; focused
rollback coverage is **20/20**, compileall passes, and rollback smoke is
**4/4** (`reports/local-20260817T211734Z`).

## Remaining risk

The screen/long divergence shows that converting stalled dynamic Builders to
raid work can improve a short sample while damaging long-map economy or
defensive timing. The next iteration must begin from v0040 and first inspect
the long-gate loss replays before proposing another bounded change.
