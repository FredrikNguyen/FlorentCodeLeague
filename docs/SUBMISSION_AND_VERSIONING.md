# Bot versioning, testing, submission, and activation

## Principles

1. `bots/candidate/` is mutable working code.
2. `bots/baseline/` is the local known-good comparator.
3. `bots/versions/<version>/` is immutable.
4. A platform upload creates a version but does not become the ladder bot until activated.
5. Never activate based on one local match.
6. Preserve enough metadata to reproduce every platform version.

## Version identity

Use:

```text
vNNNN_<slug>_<YYYYMMDD-HHMM>_<short-git-sha>
```

Example:

```text
v0042_bfs-cache_20260805-0210_a1b2c3d
```

Submission display name:

```text
v0042-bfs-cache-a1b2c3d
```

Experiment record:

```text
experiments/v0042-bfs-cache.md
```

Record:

- parent version;
- hypothesis;
- exact changed files;
- git SHA and dirty status;
- current `fcode --version`;
- map-pool snapshot;
- local matrix;
- remote test IDs/results;
- platform submission version;
- activation time;
- ladder before/after snapshots;
- decision: promote, hold, or revert.

## Initial setup

```bash
python -m pip install --upgrade fcode
fcode login
fcode starter . --yes --maps --no-bot
fcode maps sync
fcode status
```

If `starter` would overwrite repository files, skip it and only use `maps sync`.

Set this in automation to prevent an update notice contaminating JSON:

```bash
export FCODE_NO_UPDATE_CHECK=1
```

## Local development loop

Fast smoke:

```bash
fcode run bots/candidate bots/baseline sprint --seed 1 --tle 10 \
  --replay replays/smoke.replay26
fcode watch replays/smoke.replay26
```

Mirror test:

```bash
fcode run bots/candidate bots/candidate duel --seed 7 --tle 10 \
  --replay replays/mirror.replay26
```

Matrix:

```bash
python scripts/run_local_matrix.py \
  --candidate bots/candidate \
  --baseline bots/baseline \
  --config configs/eval_matrix.toml
```

The matrix runs both side orders. A candidate that only works as Team A is not ready.

## Remote server gate

Remote tests use server hardware and enforce the server time limit:

```bash
python scripts/remote_gate.py \
  --candidate bots/candidate \
  --baseline bots/baseline
```

Underlying CLI:

```bash
fcode match test bots/candidate bots/baseline sprint duel crossfire vault aurora --json
```

Current shared limit is 5 remote test matches per 10 minutes per account. Spend remote tests after local static/smoke/matrix gates, not during every edit.

## Create immutable package

```bash
python scripts/package_candidate.py \
  --slug bfs-cache \
  --experiment experiments/v0042-bfs-cache.md
```

This creates:

- an immutable copy under `bots/versions/`;
- a ZIP under `artifacts/submissions/`;
- a manifest with hashes and source metadata.

Check documented platform limits:

- archive <= 5 MB;
- unpacked <= 50 MB;
- <= 500 files;
- no native extensions;
- no path traversal;
- `main.py` exposes `Player`.

## Upload without activation

Preferred guarded wrapper:

```bash
python scripts/submit_candidate.py \
  artifacts/submissions/v0042_bfs-cache_....zip \
  --name v0042-bfs-cache-a1b2c3d \
  --confirm
```

Direct CLI:

```bash
fcode submission upload artifacts/submissions/<file>.zip \
  --name v0042-bfs-cache-a1b2c3d --json
```

Then inspect:

```bash
fcode submission list --json
```

Wait for `ready`. Do not activate `processing`, `flagged`, `rejected`, or `error`.

## Unrated challenge before ladder activation

An unrated match uses your currently active submission, so it is ideal for testing an already-uploaded active candidate only when you are intentionally willing to expose it as active. It can target a team and optionally pin the opponent version from a source match:

```bash
fcode team search "opponent"
fcode match unrated OPPONENT_ID \
  --map sprint --map crossfire --map vault --json
```

or:

```bash
fcode match unrated OPPONENT_ID --match SOURCE_MATCH_ID --json
```

For a not-yet-active local candidate, use `fcode match test` instead.

## Activate explicitly

Guarded wrapper:

```bash
python scripts/activate_submission.py VERSION --confirm
```

Direct CLI:

```bash
fcode submission activate VERSION --json
fcode status --json
```

Immediately record the active version and ladder snapshot.

## Observe live performance

```bash
python scripts/capture_live.py --label post-v0042
```

Underlying commands:

```bash
fcode status --json
fcode ladder --around --json
fcode match list --mine --type ladder --limit 100 --json
```

For a match:

```bash
fcode match info MATCH_ID --json
fcode match replay MATCH_ID --game 1 \
  --output replays/live/MATCH_ID_game_1.replay26
fcode match watch MATCH_ID --game 1
```

## Rollback

Because old ready submissions remain available:

```bash
fcode submission activate PREVIOUS_VERSION --json
fcode status --json
```

Rollback triggers:

- illegal-action/exception deaths;
- TLE evidence;
- severe map-class failure;
- statistically meaningful drop versus the preserved baseline;
- economy deadlock;
- activation mismatch or packaging defect.

Do not “fix forward” on the live ladder when a known-good version is available.

## Rename/download

```bash
fcode submission rename VERSION NEW_NAME
fcode submission download VERSION --output artifacts/platform/vVERSION.zip
```

Download and hash important platform versions so local and server artifacts can be compared.

## Efficient cadence

A good daily cadence:

1. one hypothesis;
2. focused tests;
3. local matrix;
4. Sol review;
5. remote test only if local gate passes;
6. package/upload;
7. activate only during an observation window;
8. collect enough ladder series;
9. promote to baseline or roll back.

Avoid rapid activation churn. Ladder opponents and maps add variance, so one series rarely identifies causality.


## Autonomous mode

The user has now authorized autonomous live operations. Prefer `scripts/live_operator.py` over the older guarded one-shot upload/activation wrappers because it records the rollback target, processing state, activation time, scores, and decisions across sessions. See `docs/LIVE_AUTOPILOT.md`.
