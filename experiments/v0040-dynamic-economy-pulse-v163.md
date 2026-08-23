# v163 staggered dynamic economy pulse

## Objective

Increase reliable Harvester/path conversion after the initial three-route
economy without sending the entire dynamic workforce off offense. Top-team
replays show substantially more Harvesters and Conveyors than the current
candidate; v162 showed that diverting a fixed attacker is too coarse.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Allowed source: `bots/candidate/bot/dynamic.py` and
  `bots/candidate/bot/constants.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No fixed-attacker handoff, route geometry/facing, Builder spawning, ammo,
home-defense turret cap, forward Sentinel/barrier/Launcher behavior, Store
layout, map-specific branch, baseline/archive, package, upload, activation, or
live-state change.

## Hypothesis and bounded behavior

- When completed routes are below `ECONOMY_STRONG_CHAINS`, and ordinary visible
  ore is not already selecting `TASK_HARVEST`, a deterministic phase based on
  Builder id starts a short economy pulse.
- A pulse holds `TASK_HARVEST` for six rounds, allowing the existing Defender
  SCOUT/CHAIN loop to explore and connect a source instead of abandoning the
  economy after one no-ore observation.
- The period spreads pulses across dynamic workers; after five routes, normal
  offense/repair/advance selection is restored.

## Done criteria

- Focused tests cover phase selection, route bounds, and six-round lease expiry.
- Compileall passes; static is checked and inherited failures are recorded;
  smoke is command-clean.
- The 24-game all-map screen has a material paired win-rate edge over v0040,
  no command/TLE/suspicious-output failures, and no severe delivery collapse.
- Only a qualifying screen advances to the 60-game release matrix. A failed
  screen or release gate requires exact v0040 rollback and no platform action.

## Attempt 1 and repair 1

- Attempt 1 passed focused **21/21**, compileall, and smoke **4/4**; static
  retained inherited failures. The 24-game screen was **6-18** versus v0040,
  candidate Ti **76,770** vs **93,330**, candidate no-delivery **0** vs **1**,
  and zero command/TLE/suspicious-output failures (`reports/local-20260818T005258Z`).
  The six-round pulses were too disruptive across the route-3-to-5 window.
- Repair 1 narrows the pulse to exactly three completed routes, uses a
  16-round phase period, and leases the Defender loop for three rounds. The
  focused suite and second 24-game screen are required before any release gate.

Repair 1 passed focused **27/27**, compileall, and smoke **4/4**; static
retained the inherited failures. The screen improved to **17-7** versus v0040,
candidate Ti **105,870** versus **72,280**, candidate no-delivery **0** versus
comparator **1**, and zero command/TLE/suspicious-output failures
(`reports/local-20260818T005605Z`). Per-map wins were Royale 2-0, Midgard 2-0,
Drumlin 2-0, Icefloe 2-0, and Fjordgate 2-0; the edge is material enough for
the reduced 60-game release gate.

The 60-game release gate reversed the edge to **24-36**, candidate Ti **250,630**
versus **286,480**, candidate no-delivery **1** versus **0**, with zero TLE or
suspicious-output rows and max p99/peak **1,405/5,060 us**
(`reports/local-20260818T005905Z`). Release losses clustered on Antler,
Frostgate, Glacierkeep, Midgard, Ragnarok, Royale, Valkyrie, and Yulerune.

Repair 2 added a low-liquidity gate: a three-route pulse was eligible only when
the bank was below two current Harvester costs. Focused tests passed **27/27**,
compileall passed, smoke was **4/4**, and static retained the inherited
failures. The shortened 24-game screen fell to **12-12** versus v0040, although
candidate collected Ti **68,060** versus **36,170** and both sides were
command-clean with no TLE or suspicious-output rows
(`reports/local-20260818T010720Z`). It did not recover the release reversal.

The bounded repair budget is exhausted. v163 is **rejected**; the candidate was
restored to exact v0040 Python parity (zero recursive diff lines in
`reports/iter-v163-dynamic-economy-pulse/rollback-source-diff.txt`). Rollback
focused checks passed **26/26**, compileall passed, and rollback smoke was
**4/4** (`reports/local-20260818T011058Z`). No 60-game gate, promotion,
package, upload, activation, or live-state change occurred.
