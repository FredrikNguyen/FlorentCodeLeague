# v235 loaded-source forward infiltration lease — rejected after one repair

## Hypothesis

The retained bot already has a legal enemy-Harvester hijack, but it can claim
an unseen/empty income opportunity during the route phase. A forward-only lease
that requires a live loaded accepting hostile outlet should convert a real
enemy stack while keeping the home economy and fixed defender on productive
work. It is a new target-quality/phase contract, not another sabotage or
takeover sequence.

## Scope

- `bots/candidate/bot/dynamic.py`;
- `bots/candidate/bot/defender.py`;
- one focused infiltration test module;
- durable plan, update, and state metadata.

## Non-goals

No new Store state, opening route/workforce/combat policy, Launcher or Barrier
response, fixed-attacker change, map branch, baseline/archive, package, upload,
activation, or live-state operation.

## Validation

- Initial implementation added a route/half-map/liquidity lease plus a visible
  loaded accepting hostile outlet detector. Focused coverage was **29/29**;
  compileall passed; `make static` retained the inherited exit 2; smoke was
  **4/4** command-clean. The rotated 15-map screen was command- and
  delivery-clean but only **4-11** candidate-side, collecting **72,570 vs
  82,460 Ti**, with one baseline no-delivery row and max p99/peak
  **1,359/5,629 us**. Raw report: `reports/local-20260818T234949Z`; parsed
  diagnostics: `reports/iter-v235-loaded-source-forward-infiltration/replay-analysis.json`.
- The one bounded repair removed only the route/half-map gate after the first
  screen showed reduced forward pressure, retaining loaded/accepting outlet,
  duplicate-claim suppression, and Harvester-plus-two-Conveyor liquidity
  checks. Focused coverage remained **29/29**, compileall passed, static kept
  the inherited failures, and smoke was **4/4**. The same 15-map screen was
  **6-9**, collection **64,300 vs 76,380 Ti**, first delivery mean **42.9 vs
  24.3**, and Sentinels **25 vs 70**; no candidate no-delivery/TLE/suspicious
  rows occurred, with max p99/peak **1,278/5,235 us**. Raw report:
  `reports/local-20260818T235403Z`; parsed diagnostics:
  `reports/iter-v235-loaded-source-forward-infiltration/repair-replay-analysis.json`.

## Decision and rollback

Reject v235. Neither the strict forward lease nor the loaded-source repair
created a paired edge; both reduced collection and the repair materially
reduced forward Sentinels. The temporary dynamic/defender changes and focused
test were removed. Candidate source is recursively byte-identical to immutable
v0042. Rollback coverage passed **27/27**, compileall passed, `make static`
retained the inherited exit 2, and rollback smoke was **4/4** at
`reports/local-20260818T235702Z`. No 60-game gate, promotion, package, upload,
activation, or live-state operation occurred. Keep loaded-source filtering as
a future audit idea, but choose a different structural workforce/pressure
hypothesis next.
