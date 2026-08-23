# Evaluation plan

## Objective

Determine whether a candidate is stronger, safer, and more robust than the current baseline while using remote-test and ladder opportunities efficiently.

The unit of comparison is a **paired experiment**:

- same map;
- same deterministic seed where local;
- both side orders;
- candidate versus frozen baseline;
- one isolated hypothesis.

## Evaluation layers

### Layer 0 — static contract

Run on every change:

```bash
make static
```

Checks:

- valid Python syntax;
- `main.py` exists and exports/imports `Player`;
- no forbidden/native files;
- package limits;
- no obvious `direction_to` Builder movement;
- no hard-coded obsolete Gunner constants in strategy code;
- Store indices in 0–15;
- unit tests.

### Layer 1 — smoke and visual diagnosis

Use a small, fast all-map checkpoint before the release gate:

- `sprint`
- `string`
- `duel`
- `bridge`
- `crossfire`

For each change, run 15 stratified map/seed pairs (all 15 configured maps
exactly once). This is the minimum meaningful quick screen: it preserves map
coverage while dropping the redundant side-order repeat. Side-order coverage
remains in the complete release gate; rotate `screen_seed` across iterations
so the selected map/seed pair for each map is not fixed.
The smoke maps below remain useful for visual inspection when a replay audit
needs named compact/medium cases:

- candidate vs baseline;
- candidate on both sides;
- at least two seeds;
- `--tle 10`;
- replay saved.

Visual checklist:

- Core can spawn without blocking itself.
- Builders leave the spawn ring.
- No repeated illegal target.
- Ore discovery is shared.
- Harvester has a valid output.
- Conveyor arrows form a connected path.
- Last mile reaches Core.
- Builders do not oscillate/pile up indefinitely.
- Turrets face useful lines.
- Ammo conversion precedes expected shots.
- No unexplained unit disappearance.
- CPU/debug output is reasonable.

### Layer 2 — local map matrix

Default config groups:

- very small: sprint, string, duel;
- compact: bridge, showdown, vase;
- medium square: crossfire, atoll, jackpot, fjord;
- large: aurora, hive, longship, quarry, vault;
- tall/wide special: strait, sweden, pinch.

Run:

- every current map for release candidates;
- two endpoint deterministic seeds (`1`, `101`) selected to span the fixed
  seed range;
- both side orders;
- baseline and ablation opponents.

Minimum release matrix: `15 current maps × 2 endpoint seeds (1, 101) × 2
sides = 60 games`. This remains complete map and side-order coverage for the
configured pool while cutting the routine gate by 71% from the historical
210-game run. If a tie-heavy or stochastic hypothesis needs extra confidence,
use an optional 120-game audit (four rotating seeds × both sides); the old
210-game matrix is archival evidence rather than a routine requirement.

Use more seeds for stochastic or tie-heavy policies.

### Layer 3 — remote server test

Use only after local pass.

Purpose:

- server CPU/TLE validation;
- packaging/import validation;
- architecture-specific behavior;
- five representative maps.

Suggested first gate:

```text
sprint, bridge, crossfire, vault, aurora
```

Rotate map selection so all map classes receive remote coverage over time.

Current limit: 5 remote test matches per 10 minutes per account.

### Layer 4 — shadow/live comparison

Before activation:

- upload without activating;
- confirm `ready`;
- preserve prior active version;
- capture pre-activation status/ladder/matches.

After activation:

- observe a fixed number of series or a fixed time window;
- do not make unrelated changes during the window;
- download replays for losses and surprising wins;
- compare map-conditioned results;
- roll back on reliability failures.

A practical initial decision window is 20–30 series, but confidence depends on effect size and opponent mix. Large reliability failures need no statistical waiting.

## Primary metrics

### Outcome

- **series score:** games won / 5;
- **game win rate;**
- **series win rate** (score > 0.5);
- **draw/tiebreak rate;**
- **Elo delta per series;**
- **rating and rank change;**
- **opponent-adjusted residual:** actual series score minus Elo expected score.

Use Wilson intervals for game win rates. Do not report 60% from ten games as a stable improvement.

### Reliability guardrails

- crashes/exception deaths;
- local nonzero process exits;
- TLE/turn-skip evidence;
- games with no Builder spawned;
- games with no delivered Harvester output;
- state-machine permanent stalls;
- missing/invalid replay;
- package/server rejection.

Any systematic crash/TLE is a blocker even if aggregate win rate rises.

## Economy metrics

Measure from replay analysis or explicit offline instrumentation:

- titanium collected/delivered by rounds 50, 100, 250, 500, 1000;
- stored titanium at end;
- first Builder round;
- first ore sighting round;
- first Harvester build round;
- first emitted stack;
- first delivered stack;
- Harvester count over time;
- route construction cost;
- route length;
- route payback round;
- delivery throughput (Ti/round);
- idle Harvester output opportunities;
- titanium spent on Builders/infrastructure/turrets/ammo/heal/attack;
- unspent bank distribution;
- scale percent over time.

Derived:

```text
economic payback = first round cumulative delivered Ti exceeds infrastructure cost
delivery efficiency = delivered Ti / potential Harvester output
combat allocation = combat + ammo spend / total spend
```

## Logistics metrics

- broken route count and duration;
- number of single-point cut tiles;
- stack transit latency;
- maximum/mean conveyor occupancy;
- Harvester blocked-output rounds;
- Core last-mile blockage;
- redundant-path throughput after one branch is cut;
- Builder time spent constructing, repairing, or waiting;
- path replan count;
- congestion/pileup duration.

## Combat metrics

- enemy Core damage and kill round;
- own Core damage and survival round;
- first turret round;
- turret mix;
- valid firing opportunities;
- shots fired;
- ammo spent;
- damage per ammo;
- overkill;
- reload-idle versus no-target-idle versus no-ammo-idle;
- turret lifetime;
- Builder attack/heal efficiency;
- infrastructure destroyed;
- Launcher successful ally/enemy throws;
- enemy economy disruption before Core kill.

## Navigation and information metrics

- unique tiles observed by round;
- ore deposits discovered;
- enemy Core discovery round;
- stale-target moves;
- blocked-move streaks;
- oscillation count;
- average path stretch versus shortest known path;
- BFS/A* calls per unit/round;
- cache hit rate;
- frontier exhaustion;
- Store update age;
- conflicting same-slot writers.

## CPU metrics

- p50/p95/p99/max microseconds per entity type;
- worst map/round/unit;
- number of rounds above 8 ms;
- number at/above 10 ms;
- total calls to pathfinding and sensing helpers;
- debug-print volume.

Optimize tail latency. A pathfinder that is fast on average but spikes on congestion can lose units' turns.

## Stratification

Never inspect only aggregate score. Break results down by:

- map;
- map size class;
- symmetry/aspect;
- side A/B;
- seed;
- opponent;
- opponent rating bucket;
- opening selected;
- economic versus rush mode;
- win condition: Core kill versus tiebreak;
- game length.

## Statistical decision rule

For local paired games, define per-pair score:

```text
+1 candidate wins
 0 tie/equivalent outcome
-1 candidate loses
```

Report:

- mean paired score;
- bootstrap confidence interval across map-seed pairs;
- map-level win/loss count;
- worst-map delta;
- reliability counts.

Promotion gate example:

- no new crash/TLE;
- no map class below an agreed floor;
- paired mean > 0;
- at least 55% game score in the full local matrix or a clear metric gain for an early milestone;
- primary metric improves without guardrail regression;
- remote five-game score >= baseline expectation with no reliability defect;
- Sol review approved.

Early architecture milestones may promote internally based on deterministic capability metrics before win rate becomes meaningful.

## Ladder interpretation

Elo movement is noisy because:

- map selection is random;
- opponent mix changes;
- opponent versions change;
- each series contains only five games;
- scheduling is not a controlled A/B test.

Use:

```text
expected = 1 / (1 + 10 ** ((opponent_rating - our_rating) / 400))
residual = actual_series_score - expected
```

Aggregate residual by candidate version. Preserve the opponent rating and active version/match ID when available.

Do not compare “rating today versus yesterday” without accounting for opponents and number of series.

## Replay workflow

For every release candidate:

- retain all failures;
- retain representative wins;
- retain max-CPU cases;
- annotate first divergence from baseline;
- classify root cause:
  - information,
  - navigation,
  - economy,
  - logistics,
  - combat,
  - CPU,
  - illegal action,
  - coordination,
  - map-specific assumption.

Fix the earliest causal divergence, not the most visually dramatic late-game symptom.

## Efficient submission policy

1. Local static/smoke are unlimited and cheap.
2. Run the full local matrix in batches.
3. Use remote tests only for candidates that pass local gates.
4. Upload candidates without activating.
5. Activate one candidate at a time.
6. Keep a known-good ready version for instant rollback.
7. Gather a defined observation window.
8. Promote the winner to `bots/baseline/`.
9. Start the next experiment from that baseline.

## Artifacts

Each evaluation should produce:

```text
reports/<run-id>/
  manifest.json
  games.jsonl
  stdout/
  stderr/
  replays/
  summary.md
  failures.md
```

The included scripts create raw command records now. Add a replay-state parser only after verifying the official replay schema; do not guess field names.
