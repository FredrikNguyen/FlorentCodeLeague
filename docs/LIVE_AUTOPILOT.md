# Autonomous live deployment and rollback

The user authorized Codex to upload, activate, observe, and roll back. The workflow is deliberately resumable across sessions.

## Durable files

- `UPDATES.md`: human-readable change and score history.
- `state/live_state.json`: machine-readable deployment state.
- `configs/live_policy.toml`: autonomous-operation and decision thresholds.
- `reports/live-*/`: raw CLI output, match evidence, and Sol decisions.

## First-time bootstrap

Authenticate normally, then record the current active version as the initial rollback target:

```bash
fcode login
make live-bootstrap
make live-baseline   # score the currently active known-good version when enough history exists
```

Do not deploy until `last_known_good_version` is populated.

## After an approved implementation

```bash
make package SLUG=my-change
python scripts/live_operator.py deploy \
  --archive artifacts/submissions/<version>.zip \
  --name <version-name>
```

The operator:

1. captures status, submissions, ladder, and recent matches;
2. refuses deployment if no rollback target exists;
3. uploads and identifies the new immutable version;
4. persists `uploaded_processing` state;
5. waits for `ready` up to policy timeout;
6. activates automatically;
7. persists the previous active version and activation time;
8. appends the event to `UPDATES.md`.

If processing outlives the session, the next session runs:

```bash
python scripts/live_operator.py resume
```

## Observation cycle

```bash
make live-autopilot
```

One cycle:

1. resumes a pending submission when necessary;
2. captures current ladder/match/submission data and prefetches match details with the trusted Python operator;
3. runs Sol medium read-only with a strict JSON output schema;
4. computes live fractional series score and opponent-adjusted evidence when available;
5. appends score, match IDs, rating/rank movement, and decision;
6. immediately rolls back reliability failures;
7. rolls back a clear score regression against the last known-good score;
8. promotes only after the preferred observation count and positive evidence;
9. otherwise persists `active_observing` for another session.

## Rollback

Automatic or manual:

```bash
python scripts/live_operator.py rollback --reason "TLE in live replay"
```

The operator activates `last_known_good_version`, records the failed candidate and reason, and leaves all old submissions intact.

## Decision policy

Defaults:

- minimum 12 series before score decisions;
- preferred 24 series for promotion;
- raw score rollback margin 0.05;
- adjusted score rollback margin 0.03 when both versions have comparable adjusted scores;
- any detected reliability failure can bypass the sample minimum and roll back immediately.

These are starting thresholds, not statistical guarantees. Elo and opponent mix are noisy, so preserve raw evidence and use map/opponent stratification before changing policy.

## Safety boundaries

- Deployment is blocked while another version is still under observation.
- A known rollback target is mandatory.
- Luna never performs platform writes.
- Old ready versions are never deleted.
- The live operator is deterministic and stateful; Sol supplies analysis, while Python enforces hard rollback rules.
