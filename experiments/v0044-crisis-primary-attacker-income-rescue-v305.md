# v305 crisis-only primary-attacker income rescue

## Hypothesis and scope

Fresh v107 losses showed route collapse after income went quiet: Yulerune
ended with one Harvester and no delivery, AuroraVeil delivered first at turn
150, and GlacierKeep/Drakkarfjord trailed the opponent's first delivery.  v305
let the designated primary attacker call the existing Defender economy loop
while the delayed shared phase was `ECONOMY_PHASE_CRISIS` and the Core's siege
beacon showed no missing HP.  Normal opening/converting/pressure phases,
dynamic workers, the second attacker, routes, and all unit policies were
unchanged.

## Validation

- Initial focused nearest-defense/seeded-route/economy suite: **37/37**;
  compileall passed; smoke **4/4** at `reports/local-20260819T210054Z`.
- Static retained the inherited 15 obsolete-module imports and two navigation
  fast-path assertions.
- Initial 15-map screen was command-clean but catastrophic at **2-13**;
  collection was **40,970 vs 87,230 Ti**.  First-delivery mean improved to
  **21.67 vs 24.47**, all rows delivered, and replay reliability was zero TLE/
  suspicious with max p99/peak **1,421/5,431 us**.
- One bounded repair capped each crisis episode to a 24-round rescue pulse.
  Repair focused coverage: **38/38**; compileall passed; static retained the
  inherited profile; repair smoke **4/4** at `reports/local-20260819T210413Z`.
- Repair screen was command/delivery-clean at **7-8**, collection
  **76,530 vs 87,670 Ti**, first-delivery mean **30.67 vs 31.53**, zero
  TLE/suspicious rows, max p99/peak **1,515/5,794 us**.  The repair recovered
  Yulerune, AuroraVeil, GlacierKeep, Nordkap, Ragnarok, and Archipelago, but
  still had no aggregate edge.

## Decision and rollback

Reject v305 after its single bounded lifecycle repair.  The unbounded crisis
handoff is unsafe, and the 24-round pulse does not beat immutable v0044.
Temporary attacker/constant/test edits were removed; recursive production
parity is proven by the empty
`reports/iter-v305-crisis-primary-attacker/rollback-source-parity.diff`.
Rollback focused coverage was **34/34**, compileall passed, static retained
the inherited profile, and rollback smoke was **4/4** at
`reports/local-20260819T210827Z`.  No longer gate, promotion, package,
upload, activation, or live transition occurred.  Live v107 remains
`active_observing`; v105 remains the operational rollback target.

## Follow-up evidence

The repair's map profile suggests the crisis pulse is useful only as a
route-loss rescue after income has been established, not as a general opening
role switch.  A future experiment may test that narrower route-count/phase
contract, but must preserve the exact v0044 baseline until it produces a
repeatable paired edge.
