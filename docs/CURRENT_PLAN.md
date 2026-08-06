# CURRENT_PLAN — Four-Route Economy-First Workforce

## Summary

Continue exclusively from `bots/candidate`; platform v4 is out of scope.

The current bot is capped at three route projects, initially requests too few Builders, expands sequentially, permits offense after two routes, and computes Core role assignments that Builders never consume.

The next candidate must:

- Rush four distinct, functioning Harvester routes.
- Build up to two new routes concurrently after route 0 delivers.
- Give every Builder a persistent useful work intent.
- Delay discretionary defense and all offense until four routes are stable.
- Permit early defense only against a fresh critical threat.

## Iteration 1 — Four-route expansion

Objective: remove the three-route ceiling and reach four healthy Harvesters without sacrificing route 0.

Allowed files:

- `bots/candidate/bot/comms.py`
- `bots/candidate/bot/core.py`
- `bots/candidate/bot/economy.py`
- Expansion-specific sections of `builder.py` and `types.py`
- Corresponding communication, economy, route, expansion, and player tests
- `configs/eval_regression.toml`

Implementation:

- Introduce `PROJECT_COUNT = 4`; replace every hard-coded three-project range and limit.
- Increment the Store schema to version 4.
- Use Store slot 13 for `PROJECT_3` and slot 15 for `CLAIM_3`; stop treating those slots as unused budget/epoch storage.
- Extend project codecs, ownership validation, heartbeat handling, stale-claim recovery, and delayed-write tests to project index 3.
- Preserve route 0 as the protected primary route.
- Build route 0 alone. After its first confirmed delivery and fresh heartbeat, allow at most two projects among routes 1–3 to be planning/building simultaneously.
- When either secondary project stabilizes or fails, immediately consider the next unclaimed profitable ore.
- Resolve delayed-write ore collisions deterministically: lower project index retains the ore; the other project retargets.
- Target four distinct reachable ore deposits. Only lower the target when every reachable tile has been explored and all remaining ore has failed three bounded route searches.
- Request five Builders until route 0 is healthy, six while expanding toward four routes, and seven after four routes stabilize.
- Reserve active route completion and repair costs before spawning or starting another project. Query all current costs through the Controller API.

Non-goals:

- No navigation rewrite.
- No combat, turret, launcher, or target-priority changes.
- No route redundancy or shared conveyor merging.
- No edits to `bots/baseline` or existing version snapshots.

Done criteria:

- Focused tests cover all four slots, stale claims, delayed writes, collisions, and independent project failure.
- An integration fixture with four reachable ores reaches four `MAINTAIN` projects.
- Route 0 remains healthy while two secondary routes are under construction.
- Never more than two secondary projects build concurrently.
- `make static` and `make smoke` pass.
- The selected paired matrix is command-clean, has local p99 below 8 ms, and collects at least 102% of the workspace Iteration 7 snapshot.

## Iteration 2 — Eliminate avoidable Builder idling

Objective: every Builder has a persistent economic or scouting responsibility and attempts useful movement or a legal action whenever one exists.

Allowed files:

- `bots/candidate/bot/builder.py`
- `bots/candidate/bot/types.py`
- Builder-policy sections of `policy.py`
- Relevant route FSM, navigation, policy, and player tests

Implementation:

- Add an internal `WorkIntent` with: `ROUTE_OWNER`, `REPAIR_ROUTE`, `DISCOVER_ORE`, `PATROL_LOGISTICS`, `CRITICAL_DEFENSE`, `ATTACK_PREPARATION`, and `ATTACK`.
- Resolve intent every turn in this order:
  1. Fresh critical threat.
  2. Owned route repair.
  3. Owned route planning/construction.
  4. Harvester construction and delivery verification.
  5. Exploration of an unknown reachable frontier.
  6. Patrol of the stalest healthy route.
  7. Non-blocking staging beside the Core or a route junction.
- While incremental route planning is incomplete, move the owner toward a valid tile adjacent to its ore when a safe legal step exists.
- Replace corner wandering with deterministic frontier exploration. When a waypoint is reached or unreachable, select the next frontier during the same turn.
- Unassigned Builders must scout for future ore before four routes exist. They must not build unrequested Harvesters, duplicate a claim, or obstruct a route cell.
- After exploration is complete, unassigned Builders patrol the stalest route and repair visible damage when legal.
- “No idle” means maintaining a useful intent and attempting a legal move/action when available; it does not require wasteful titanium spending.

Non-goals:

- No new Store slots.
- No paid attacks or discretionary defensive construction.
- No change to the bounded route-search algorithm.

Done criteria:

- Focused fixtures demonstrate each work intent and fallback transition.
- When a legal frontier or patrol move exists, an unassigned Builder does not finish without attempting it.
- Route owners never abandon their projects to scout.
- Builders do not collide on the same ore or construction cell.
- `make static` and `make smoke` pass.
- The selected paired matrix remains command-clean and improves aggregate collection over the Iteration 1 checkpoint.

## Iteration 3 — Economy-gated defense and offense

Objective: retain four productive routes while converting surplus Builders into defense or pressure.

Allowed files:

- Strategy sections of `core.py`, `builder.py`, and `policy.py`
- Critical-threat gating in `defense.py`
- Relevant policy, defense, offense, and player tests

Implementation:

- Require four healthy routes with fresh delivery heartbeats for eight consecutive rounds before entering attack preparation.
- If exhaustive exploration proves fewer than four reachable ores, require every reachable route to be healthy instead.
- Before this gate:
  - Suppress raids, forward structures, discretionary turrets, standing ammo conversion, and normal defense diversion.
  - Permit defense only for a fresh critical threat near the Core or an active route.
  - Assign the nearest free Builder first; interrupt a route owner only if no free Builder can respond.
- Remove the unused Core-only role map as an attack-readiness signal.
- Make roles observable and authoritative through project ownership plus global strategy:
  - Project owners remain economy/repair workers.
  - Free Builders scout during attack preparation.
  - Free Builders defend during a critical alert.
  - Free Builders become raiders during offensive pressure and siege units only during a verified Core window.
- Attack readiness must use the actual count of free Builders, not whether a dictionary is non-empty.
- Recovery immediately returns all offensive Builders to scouting, route patrol, or defense while any route is broken.

Non-goals:

- Do not enable Launchers.
- Do not change turret fire targeting.
- Do not introduce speculative Core attacks without a fresh verified target.
- Do not pull healthy route owners into ordinary combat.

Done criteria:

- Tests prove offense cannot begin at one, two, or three healthy routes.
- Tests prove a critical early threat can trigger bounded defense without releasing route claims.
- Tests prove four stable routes plus a free Builder enter attack preparation and then offense after target verification.
- Recovery cancels offense when a route breaks.
- `make static`, `make smoke`, and focused combat regression pass.
- Collection remains at least 98% of the Iteration 2 checkpoint while controlled combat fixtures show actual attack progress.

## Evaluation and checkpoint policy

For every iteration:

1. Restate objective, allowed files, non-goals, and done criteria.
2. Inspect the repository and existing diff before editing.
3. Implement only that iteration.
4. Run focused tests, `make static`, `make smoke`, then the selected paired regression.
5. Self-review the complete diff and repair defects.
6. Stop after two unsuccessful bounded repair attempts.
7. Update `UPDATES.md` and `state/project_state.json` with files, tests, reports, metrics, risks, and status.
8. Snapshot a passing candidate and use it as the next iteration’s comparator.

Use this 48-game checkpoint matrix:

- Maps: `bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`
- Seeds: `1`, `19`, `101`
- Both sides
- `--tle 10`

Do not run the full 21-map matrix until all three iterations pass. At the release gate, compare against the latest passing snapshot, require zero command/runtime failures, p99 below 8 ms, non-regressing aggregate titanium, and at least one strict collection or combat improvement. Packaging, submission, activation, and rollback remain separate operations and are not authorized by this plan.
