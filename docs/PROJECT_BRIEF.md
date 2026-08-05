# Florent Code League project brief

## Objective

Build a reliable Python bot that establishes titanium delivery, adapts to map geometry, protects its Core, and converts economic advantage into enemy-Core pressure.

## Match constraints

- Two teams on an 8×8 to 30×30 grid.
- Destroy the enemy Core to win; maximum 1000 rounds.
- Ladder series contain five games.
- Approximately 10 ms CPU per unit per round on the ladder.
- An uncaught exception permanently destroys the affected unit.
- Builders move cardinally and cannot move and act in the same round.
- Build, attack, heal, and destroy target orthogonally adjacent tiles.
- Prices scale with currently live entities; query costs through the API.
- Team communication is 16 delayed integer Store slots.

## Main systems

- **Core:** Builder spawning, global budget, ammunition conversion.
- **Builders:** sensing, movement, construction, healing, sabotage.
- **Economy:** ore discovery, Harvester placement, payback-aware expansion.
- **Logistics:** directed Conveyors, Splitters, Core last mile, route repair.
- **Combat:** Gunner, Sentinel, Launcher, barriers, ammunition budgeting.
- **Coordination:** per-unit state plus a small versioned Store protocol.

## Current implementation direction

1. Safe deterministic dispatch and fallback behavior.
2. Versioned shared coordinate protocol.
3. Bounded cached cardinal BFS and stale-path recovery.
4. Verified Harvester-to-Core delivery route.
5. Payback-aware expansion and route repair.
6. Defense/ammo policy, then offense and map-adaptive openings.

## Engineering priorities

1. No illegal actions or escaping exceptions.
2. Bounded tail CPU.
3. End-to-end delivered titanium, not merely placed structures.
4. Deterministic paired evaluation across maps, seeds, and sides.
5. One isolated hypothesis per candidate and instant rollback to known-good live version.

## Workflow

- Sol High in ordinary ChatGPT creates an occasional bounded plan from the generated planning packet.
- Luna XHigh in Codex implements, tests, and self-reviews in one session.
- Deterministic Python scripts run broad evaluation, package, submit, monitor, score, promote, and roll back.
- External Sol review is optional and used primarily for release candidates or difficult regressions.
