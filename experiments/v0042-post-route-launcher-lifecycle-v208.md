# v208 — post-route Launcher lifecycle

## Hypothesis and scope

Replay audit v207 found Launchers in 8/15 high-ranking winners versus 2/15
losers, while v0042 never ran a Launcher. v208 adds one reserve-funded,
post-route Launcher to the fixed attacker only after three completed routes, a
confirmed enemy Core, and one live forward Sentinel. The Launcher scans the
eight adjacent tiles, accepts either-team Builders, and launches only to a
passable destination with strict progress toward the enemy Core (ally) or
strict retreat from it (enemy). Every action is gated by `can_*`, dynamic
prices, cooldown, visibility, and a no-progress fallback.

Allowed production files were `bots/candidate/main.py` and
`bots/candidate/bot/attacker.py`; one focused lifecycle test, the rotated
regression seed, this record, durable updates/state, and reports were also in
scope. No opening economy, Store schema, turret policy, Barrier/Sentinel caps,
map branches, package, upload, activation, or live state were changed.

## Validation

- Focused lifecycle tests: **5/5** (`reports/iter-v208-launcher-lifecycle/final-focused.log`).
- Candidate compileall: **pass** (`reports/iter-v208-launcher-lifecycle/final-compileall.log`).
- `make static`: **exit 2**, unchanged inherited 15 deleted-module imports and
  two navigation fast-path assertions (`reports/iter-v208-launcher-lifecycle/final-static.log`).
- Smoke: **4/4 command-clean** (`reports/iter-v208-launcher-lifecycle/final-smoke.log`).
- Rotated 15-map screen, seed 172, initial v208 source: **9–6** against exact
  v0042, all 15 candidate deliveries present, mean first delivery **22.67 vs
  28.67**, max p99/peak **1457/2166 us**, zero TLE/suspicious output. Three maps
  placed a Launcher; two had a replay field-16 jump from the Launcher tile to a
  destination within the documented radius, consistent with a legal lifecycle
  event. Full report: `reports/iter-v208-launcher-lifecycle/replay-analysis.json`;
  raw screen: `reports/local-20260818T144551Z`.

## Repair attempts and decision

The first bounded repair added a replay indicator line after `launch`; the
rerun fell to **7–8** (`reports/local-20260818T145245Z`) and was removed. The
second bounded repair held the constructing attacker for one round so a newly
created Launcher could rendezvous; it fell to **5–10** with mean delivery
**37.47 vs 28.13** (`reports/local-20260818T145801Z`) and was removed. Their
focused/compile/static/smoke logs are retained under the same report folder.

Retain the original v208 source as an **unpromoted local candidate** because
the initial screen beats v0042, but do not package, upload, activate, or change
the immutable baseline without a release-gate result and clearer replay
causality. The next hypothesis should address top-team repeated Launcher
relay/rendezvous timing rather than retuning this late one-shot gate.
