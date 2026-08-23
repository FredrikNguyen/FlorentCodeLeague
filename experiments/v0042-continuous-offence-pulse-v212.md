# v212 — continuous offence pulse (approved)

## Replay basis

The v211 release gate was rejected at 28-32 and its delivery-confirmation
repair fell to 3-12 on the rotated 15-map screen. The relevant remaining
failure is not a missing economy selector: ready fixed attackers can reach a
full Sentinel shell, lose their current logistics target, and spend turns
without a concrete next pressure action. Top-team samples instead alternate
Core pressure, loaded-belt/Harvester sabotage, and forward Barrier/Sentinel
work. Existing attacker fallback and nearest-target helpers are the only
mechanisms in scope for this experiment.

## Approved bounded hypothesis

After a legal offensive action or a confirmed stale target, keep a designated
attacker in a short offense-pulse phase. It must choose the next visible
pressure target (prioritizing loaded logistics/Harvesters, then the confirmed
Core lane) or a strict-progress reposition before returning to its normal Core
pressure loop. Preserve existing economy, reserve, nearest-attacker, danger,
and action-legality gates. Dynamic Builders are unchanged.

## Allowed files

- `bots/candidate/bot/attacker.py`;
- one focused offense-pulse/legality test module;
- one existing tuning constant only if essential;
- this record, `UPDATES.md`, `docs/CURRENT_PLAN.md`, and durable report/state
  metadata.

## Non-goals

No new Store slot/schema, Launcher lifecycle, Sentinel-cap change, route
milestone or VERIFY behavior, economy gate, dynamic-builder priority rewrite,
map branch, Barrier/Gunner/ammo policy, baseline/archive/package, upload,
activation, or live-state change.

## Done criteria

Focused tests cover phase advancement after an action, stale-target recovery,
nearest-attacker ownership, action legality, and strict-progress reposition;
compileall/static/smoke retain the inherited profile. A fresh Luna snapshot
screen covers all 15 configured maps, is command-clean with no TLE,
suspicious-output, or new no-delivery rows, and has a clear paired win-rate
edge over exact v0042. Run the 60-game gate only after that edge; otherwise
allow one bounded repair and restore exact pre-v212 parity.

## Implementation and gate result

The Luna implementation added a lazy one-step local pulse in `attacker.py` and
five focused tests. Root checks passed: **45/45** focused regression/contract
tests, candidate compileall, and smoke **4/4**. `make static` retained only
the inherited deleted-module imports and two navigation fast-path assertions.
The pre-edit seed-177 snapshot was **4-11**, with one candidate no-delivery
row; evidence is in `reports/parallel-v212-screen/summary.md`.

The edited seed-177 screen reversed to **11-4**, 15/15 command-clean and
delivery-clean, collection **55,420 vs 48,550 Ti**, mean first delivery
**28.80 vs 30.33**, and max p99/peak **1,513/3,250 us**. This justified the
release gate. The complete 60-game endpoint-seed/both-side gate was
command-clean with zero TLE/suspicious rows and scored **33-27** candidate-side
(55.0%), collection **220,550 vs 224,920 Ti**, candidate no-delivery **1** vs
baseline **2**, first-delivery mean **35.90 vs 27.40**, and max p99/peak
**1,473/3,873 us**. Map splits were Antler 2-2, Archipelago 3-1, Auroraveil
2-2, Drakkarfjord 2-2, Drumlin 3-1, Fjordgate 2-2, Frostgate 1-3,
Glacierkeep 3-1, Icefloe 0-4, Midgard 4-0, Nordkap 1-3, Ragnarok 3-1,
Royale 2-2, Valkyrie 2-2, Yulerune 3-1.

The aggregate edge is promising, but the Icefloe 0-4 protected-map collapse,
three additional 1-3 floors, slower delivery, and lower collection fail the
reliability/map-floor promotion guard. v212 is **rejected for promotion**;
v0042 remains the baseline. No package, upload, activation, or live-state
transition occurred. Full reports:
`reports/local-20260818T163712Z`,
`reports/iter-v212-continuous-offence/release-replay-analysis.json`,
`reports/local-20260818T163452Z`, and
`reports/iter-v212-continuous-offence/edited-screen-replay-analysis.json`.

Replay direction for the next hypothesis: v212 losses frequently had zero or
one surviving Sentinel and two-to-five Harvesters, especially Icefloe,
Drakkarfjord, Royale, and Nordkap. The next change must make pressure
map/context-adaptive without merely increasing pulse frequency or spending
more reserve.
