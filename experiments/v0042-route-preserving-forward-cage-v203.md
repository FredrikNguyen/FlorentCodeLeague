# v203 — route-preserving early forward cage

## Replay basis and objective

The v202 repair losses commonly had zero or one Barrier despite having a route
workforce. The high-ranking replay set showed winners placing roughly 7–20
Barriers around the confirmed enemy Core in rounds 7–30, often before their
first Sentinel, while their Harvesters and deliveries still arrived. v203
removed the completed-route prerequisite from the existing attacker cage, but
kept its dynamic one-Harvester reserve, six-site cap, escape-safe placement,
and confirmed-Core requirement. No route worker was diverted.

## Scope

- Temporary source: `bots/candidate/bot/attacker.py`.
- Temporary focused coverage: `tests/test_candidate_enemy_core_cage.py`.
- Regression screen: all 15 maps with `configs/eval_regression.toml` rotated
  from seed 167 to seed 168.
- No primary-attacker handoff, Launcher, Sentinel, route, dynamic-task,
  hijack, sabotage, turret, ammo, baseline, package, upload, activation, or
  live-state change.

## Validation and replay evidence

- The initial pre-route cage gate passed focused **28/28**, compileall, static
  with only inherited failures, and smoke **4/4**. The seed-168 screen was
  **6-9**, 15/15 command-clean with zero TLE/suspicious output, but introduced
  a candidate no-delivery Drakkarfjord row. Replay events confirmed the new
  cage was real: candidate Barrier totals reached 4–12 on several maps. Max
  p99/peak were **1,496/5,601 us**. Report:
  `reports/local-20260818T134721Z`; analysis:
  `reports/iter-v203-forward-cage-replay-analysis.json`.
- One bounded repair limited pre-route cage construction to half the existing
  cap (three sites), restoring the full cap after a completed route. Focused
  coverage was **29/29**, compileall passed, static retained the inherited
  exit 2, and smoke was **4/4**. The identical seed-168 screen remained
  **6-9** and moved the no-delivery row to Royale. It was 15/15
  command-clean with zero TLE/suspicious output; max p99/peak were
  **1,666/4,544 us**. Report:
  `reports/local-20260818T134949Z`; analysis:
  `reports/iter-v203-forward-cage-repair-replay-analysis.json`.

## Decision and rollback

Reject v203 after the permitted repair. The cage event was causal but did not
produce a paired win-rate edge, and both versions introduced a no-delivery
outlier. Restore candidate source to recursive parity with immutable v0042.
Rollback nearest-defense was **23/23**, compileall passed, static retained the
inherited exit 2, and rollback smoke was **4/4** at
`reports/local-20260818T135203Z`. No release gate, package, upload, activation,
or baseline transition occurred.

## Replay conclusion

Early Barrier topology alone is not enough: the attacker reaches the cage too
late on some maps, while spending its reserve can still starve route delivery.
Future replay work should couple forward pressure to a live delivery/route
health signal or another unit that can act without consuming the primary lane.
