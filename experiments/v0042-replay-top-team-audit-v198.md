# v198 replay and top-team audit — hypothesis checkpoint

## Objective

Inspect the v197 loss replays, the live v100 loss sample, and the saved
high-ranking replays before changing the v0042 candidate. Record one new,
bounded mechanic hypothesis and keep the candidate source unchanged during
the audit.

## Evidence reviewed

- v197 initial replay set: `reports/iter-v197-forward-support-replay-analysis.json`.
  The temporary support bot scored **6-9**. Across all 15 games its first
  Harvester averaged round **16.3** versus **9.5** for v0042. In its nine
  losses it placed **5.56 Harvesters**, **3.57 Barriers**, and **2.00
  Sentinels** on average versus v0042's **7.89**, **6.12**, and **4.25**;
  mean final titanium was **3,243 versus 4,912**.
- v197 half-HP repair: `reports/iter-v197-forward-support-replay-analysis-repair1.json`.
  The repair fell to **5-10**. Its first Harvester averaged round **17.2**
  versus **10.1** for v0042; its ten losses averaged **5.9 Harvesters** and
  **4.75 Barriers** versus **9.0** and **6.44**, with final titanium
  **2,247 versus 5,496**.
- The live v100 loss sample (`reports/live-v100-losses-20260815-analysis.json`)
  repeats the same causal shape: losing sides often had late or missing first
  delivery, fewer Harvesters, and many fewer Barriers/Launchers than the
  winner. One representative loss delivered at round **114** with 4
  Harvesters while the winner delivered at round **20** with 9 Harvesters,
  2 Barriers, and a Launcher.
- The 15 saved top-team replays (`reports/top-teams-20260815-analysis.json`)
  show winners placing the first Harvester by mean round **7.7**, delivering
  by mean round **21.1**, and averaging **5.0 Harvesters**, **13.7 Barriers**,
  **3.3 Launchers**, and **3.6 Sentinels**. Losers averaged **3.1
  Harvesters**, **8.9 Barriers**, **0.4 Launchers**, and **0.9 Sentinels**.
  Launchers appear early (often round 1), while Sentinels arrive after the
  economy shell; this is mobility/control, not a replacement for route work.

## Causal conclusion

The rejected v195–v197 local raid, takeover, and repair selectors did not fail
because the bot needed another target priority. They pulled workforce or
liquidity away from the route phase: every v197 loss family shows delayed first
Harvester placement and a lower Harvester/Barrier stock than the comparator.
The top-team difference is a missing unit-control phase: v0042 has no
`EntityType.LAUNCHER` policy at all, while the strongest replay winners use
Launchers to control Builder positioning and keep offensive Barriers/Sentinels
effective after delivery is established.

## Selected v198 hypothesis

Add one **forward enemy-Builder ejection Launcher** as a post-economy phase,
not a mobility detour: only the designated primary attacker may build it after
three completed routes, one confirmed forward Sentinel, a confirmed enemy Core,
and a dynamic Launcher-plus-Harvester reserve. The Launcher may throw one
adjacent enemy Builder to a verified bot-passable tile farther from that Core;
it never throws our workforce, builds a fleet, or runs before the route phase.
This is distinct from the rejected v156 own-attacker insertion and the old home
Launcher/ejection experiments because it uses the current v0042 attacker only
for a single confirmed-Core repair-denial action.

## Scope and done criteria

- Allowed source: `bots/candidate/main.py` and
  `bots/candidate/bot/attacker.py`; one focused Launcher-control test module;
  configs, this record, `UPDATES.md`, and durable report/state files.
- Non-goals: opening route/ore policy, dynamic task priorities, hijacking,
  Sentinel/barrier caps, home Gunners, Launcher insertion of our own Builders,
  baseline/archive/package/live changes.
- Focused tests, compileall, static, smoke, and the 15-map screen must be
  command-clean with no TLE/suspicious output. A positive screen must beat the
  exact v0042 baseline without a new no-delivery row; one bounded repair is
  allowed. Otherwise restore exact v0042 parity and stop the iteration.

## Validation and decision

- Focused coverage was **26/26** for the new Launcher/ejection checks plus the
  nearest-defense regressions; compileall passed. `make static` retained the
  inherited **15 obsolete-import errors and two navigation assertions**; the
  new module had no static failure. Smoke was command-clean (**4/4** report
  `reports/local-20260818T122905Z`; replay analysis
  `reports/iter-v198-forward-launcher/smoke-analysis.json`).
- The first seed-162 screen looked positive at **11-4**, with no command,
  TLE, suspicious-output, or no-delivery rows and max p99/peak
  **1481/4864 us** (`reports/local-20260818T122934Z`). Replay inspection found
  only one Launcher, built at the end of a Royale game; it never produced a
  recorded ejection, so the apparent edge was not causal evidence.
- An independent rotated seed-163 all-map screen was **7-8**, also 15/15
  command-clean with no TLE/suspicious/no-delivery rows and max p99/peak
  **1385/2384 us** (`reports/local-20260818T123246Z`). It placed one Launcher
  at the end of an Archipelago game and again showed no ejection.

Reject v198: the unit-control branch did not produce a causal Launcher action
or a repeatable paired win-rate edge. The temporary source and focused test
were removed; the next experiment must use a new replay-backed phase
hypothesis rather than widening this late ejection selector. No release gate,
package, upload, activation, or baseline transition is justified.
