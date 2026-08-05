# Additional project considerations

## 1. Rules are a moving dependency

The August 4 balance patch changed several opening-critical values one day before this snapshot. Treat the game rules like a fast-moving API:

- check changelog before evaluation/activation;
- sync maps;
- record `fcode --version`;
- run a small rule-contract match after updates;
- prefer getters and API geometry helpers;
- keep a dated rule snapshot.

## 2. Tutorials are educational, not production code

Current tutorial samples contain or historically contained:

- cardinal-movement mistakes;
- duplicate constants;
- old ammo concepts;
- old turret numbers;
- simplistic Store protocols;
- random movement;
- optimistic route state machines.

Use tutorials for concepts. Verify every snippet against current reference and changelog.

## 3. Preserve live safety

The active bot is an operational artifact, not a branch pointer.

- Keep prior ready version.
- Upload first, inspect status, activate separately.
- Activate only when available to observe.
- Roll back on reliability problems.
- Never let a Codex agent activate automatically.

## 4. Avoid false leaderboard conclusions

Rating is not a clean A/B metric. Opponents, maps, and their versions change. Use opponent-adjusted series residual, paired local tests, stratification, and replay root-cause analysis.

Do not chase every single ladder loss. Cluster failures first.

## 5. Optimize delivery, not structure count

A Harvester with no accepting output produces no useful income. More conveyors can add scale and attack surface. Core metrics should be delivered titanium, payback, uptime, and route recovery.

## 6. Cost scale couples every decision

Building a unit affects future prices. Compare strategies on total discounted value, not local base cost. A “cheap” Gunner carries +20% scale and 4-ammo recurring cost.

## 7. Global ammo is a capital-allocation problem

Over-conversion starves expansion; under-conversion idles turrets. Forecast demand, preserve emergency reserve, and separate no-target from no-ammo idle.

## 8. The Store is tiny and delayed

Sixteen integers are enough for a protocol, not a replicated world state.

- pack data;
- include epochs;
- use single writers;
- avoid atomic-counter assumptions;
- retain rich local state per unit;
- version the schema.

## 9. Unit IDs and execution order

Units execute in creation order and have persistent instance state. This can support deterministic role assignment, but relying on implicit ID arithmetic without tests can become brittle. Make role assignment observable in replays.

## 10. Pathfinding needs a congestion model

Shortest terrain path is not necessarily fastest:

- Builders block each other;
- turrets/Harvesters/Barriers are impassable;
- route-construction actions consume whole rounds;
- standing on conveyors is allowed;
- enemy structures can invalidate memory.

Start with BFS, then add reservations/penalties only when metrics show congestion.

## 11. Symmetry is a prior, not truth

Use map symmetry to prioritize scouting and estimate enemy direction. Confirm through sensing before expensive fixed-facing Sentinel placements or attacks.

## 12. Debugging itself can cause TLE

Limit prints and replay indicators. Gate them behind constants and sample rounds. Store raw replay analysis outside `run()`.

## 13. Defensive code can hide defects

A top-level exception catch preserves a unit, but silent repeated failure creates an inert army. Track a bounded error count, expose indicators, and switch to a known fallback.

## 14. Separate policy from mechanism

Mechanism:

- legal movement;
- route construction;
- target geometry;
- Store encoding.

Policy:

- which ore;
- how many Builders;
- when to expand;
- turret mix;
- when to attack.

This allows controlled experiments without rewriting legality-critical code.

## 15. Build an opponent corpus legally

Use public ladder identities, your own match replays, and permitted unrated challenges. Do not seek private code or exploit platform internals. Classify opponent behavior rather than overfitting to names.

## 16. Recommended next additions

After the baseline works:

- replay parser using a verified replay schema;
- HTML/Markdown evaluation dashboard;
- map feature extractor from `.map26`;
- regression replay suite;
- CPU profiler hooks;
- property tests for coordinate packing/path legality;
- scripted scenario maps through the map editor;
- automated changelog/map-pool drift check;
- GitHub CI for static/package tests;
- experiment registry linking git SHA ↔ platform version ↔ match IDs.

## 17. Immediate first work package

The strongest next task is:

```text
Implement Milestones 1 and 2 only:
safe dispatch, deterministic Builder exploration, versioned Store coordinate packing,
and cached cardinal BFS. Do not build combat or a full economy yet. Prove legality,
CPU bounds, map coverage, and fixed-seed determinism.
```

Then implement the minimum viable delivery route. A sophisticated combat policy built on broken navigation/logistics will be difficult to diagnose.

## 18. Subagent backend drift is an operational dependency

A custom-agent TOML does not prove the requested model executed. Preserve exact command/event evidence, run the Luna doctor after Codex updates, and use process isolation when native routing is incompatible.

## 19. Autonomous deployment needs durable state

Never hold the rollback target or observation window only in chat context. `UPDATES.md` and `state/live_state.json` are the release ledger. A later session must be able to resume processing, score the active candidate, or reactivate the last known-good version without reconstructing history.
