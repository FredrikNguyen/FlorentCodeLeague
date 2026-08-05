# v0001 — integrated Milestones 1–9 candidate

Parent: `2de8371f`
API: `fcode 2.3.4`
Candidate: `bots/candidate`

The user explicitly requested a combined cadence covering Milestones 1–9 and all 13 backlog capabilities; this umbrella experiment intentionally evaluates their integrated effect as one release candidate.

## Hypothesis

A deterministic architecture combining bounded cardinal navigation, verified Core-outward delivery, explicit Store ownership, payback/reserve gates, route repair, adaptive defense/offense, geometry-derived openings, and late-game tiebreak policy will produce positive paired performance against the frozen baseline without legality, determinism, reliability, or CPU regressions.

## Evaluation

- Primary metric: candidate score in the 210-game local matrix.
- Required threshold: score ≥ 0.55, paired mean > 0, worst map ≥ 0.30.
- Economy guardrail: every map has a candidate-side game with collected titanium > 0.
- CPU guardrail: benchmark p99 < 8 ms and no matrix command failures with `--tle 10`.
- Reliability guardrail: no escaped exceptions, illegal actions, invalid replays, permanent stalls, or package-contract failures.
- Map snapshot: `atoll`, `aurora`, `bridge`, `crossfire`, `duel`, `fjord`, `hive`, `jackpot`, `longship`, `pinch`, `quarry`, `runestone`, `showdown`, `skerry`, `sprint`, `strait`, `string`, `sweden`, `twins`, `vase`, `vault`.

## Scope and guardrails

Only the packet-allowed candidate production modules, candidate tests/benchmark, this experiment record, and `reports/codex-20260805T010045Z/` evidence are changed. `bots/baseline/`, `bots/versions/`, README, maps, configs, state files, startup files, UPDATES.md, scripts, and unrelated dirty/untracked files remain protected. No remote or platform operation is performed.

## Implementation summary

The candidate adds the fixed schema-2 Store codecs and ownership table; legality-gated `TurnActions`; static/dynamic world memory; bounded cached BFS with invalidation and fallback; Core-outward route planning and verification; claims, payback, reserves, and route-health helpers; Core spawning and ammo deficit budgeting; stable roles and observed opening/phase selection; threat-aware defense; sabotage/rally/Launcher scoring; current-rule turret handlers; and safe all-entity dispatch.

## Local results

All required local checks completed successfully. The full matrix report is `reports/local-20260805T073308Z/`:

- 210/210 commands returned zero; candidate won 157/210 games for score `0.747619`.
- Paired mean was `0.495238` across 105 map-seed pairs (`+1` for both wins, `0` for a split, `-1` for both losses).
- Worst map score was `0.50`; all 21 maps had candidate-side titanium collection.
- Candidate-side collected titanium was positive in 190/210 games, totaling 367,700; every map had at least one positive-collection candidate-side game.
- Win conditions were 157 `titanium_collected`, 20 `titanium_stored`, and 33 `core_destroyed` results.
- The final CPU benchmark reported p99 `6.604627 ms` and max `6.956455 ms`, below the 8 ms threshold.

Focused/static/smoke/regression/benchmark logs, parsed matrix metrics, reliability evidence, protected hashes, and the review are stored under `reports/codex-20260805T010045Z/`.
