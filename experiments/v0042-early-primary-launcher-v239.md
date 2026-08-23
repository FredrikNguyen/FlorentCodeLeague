# v239 — early primary-attacker Launcher lifecycle (rejected after one repair)

## Replay basis and objective

The top-team replay audit found a Launcher on rounds 1/3/5 in 8/15 winners,
while v0042 never created one. The earlier v208 lifecycle was deliberately
post-route and tied its 60-game gate, so v239 tested a different structural
hypothesis: let only the primary attacker buy one early Launcher, preserving a
dynamic Harvester-plus-two-Conveyors reserve, and let the Launcher throw only
friendly Builders to legal passable tiles with strict distance progress toward
the mirrored/confirmed enemy Core.

## Validation

- Initial focused coverage: **31/31**; compileall passed; `make static`
  retained the inherited exit 2; smoke **4/4**
  (`reports/local-20260819T004413Z`).
- Initial rotated 15-map screen: candidate-A **4–11**, collection
  **24,160 vs 50,060 Ti**, first delivery mean **41.2 vs 25.6**. It placed one
  Launcher on every candidate map (first placement rounds 2–3), but the early
  Launcher correlated with severe economy/pressure loss. All rows were
  command-clean with zero TLE/suspicious output
  (`reports/local-20260819T004432Z`; analysis in
  `reports/iter-v239-early-primary-launcher/replay-analysis.json`).
- One bounded repair restricted Launcher pickup to the designated fixed
  attacker IDs so an economy Defender could not be thrown away from ore.
  Focused coverage stayed **31/31**, compileall/static/smoke retained the same
  profile, and the same screen improved to **8–7**, collection
  **77,840 vs 64,800 Ti**, first delivery mean **25.2 vs 51.1**, with zero
  reliability faults (`reports/local-20260819T004704Z`; analysis
  `replay-analysis-repair.json`).
- Independent rotated repair screen: **7–8**, collection **65,020 vs 75,940
  Ti**, one candidate no-delivery row (Royale), first delivery mean **99.9 vs
  21.1** with no-delivery mapped to 999, and zero TLE/suspicious rows
  (`reports/local-20260819T004914Z`; analysis
  `replay-analysis-repair-rotated.json`). Max p99/peak was **1,391/3,714 us**
  on the first repair and **1,391/2,997 us** on the rotated screen.

## Decision and rollback

Reject v239. The unrestricted lifecycle clearly damaged the economy; the
attacker-only repair produced one encouraging 8–7 screen but reversed to 7–8
with a no-delivery loss. No 60-game gate, promotion, package, upload,
activation, or live-state transition was justified. The temporary Launcher
logic, state flag, constant, and focused test were removed; the original
screen seed 172 was restored; candidate source is recursively byte-identical
to immutable v0042 (`rollback-source.diff`). Rollback focused coverage was
**27/27**, compileall passed, rollback smoke **4/4**, and static retained exit
2 (`reports/iter-v239-early-primary-launcher/`).

## Follow-up

Do not retry an early Launcher purchase without a new causal placement/launch
design that protects first delivery. The top-team correlation is not enough to
justify adding a unit that repeatedly diverts the opening workforce; return to
high-frequency route/resource conversion or map-state pressure evidence.
