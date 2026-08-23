# Florent Code League bot workspace

A competition-ready workspace for developing, testing, reviewing, versioning, and submitting a Florent Code League bot.

**Rules snapshot:** verified against the public documentation, tutorials, changelog, and map-pool page on **2026-08-05**. The platform can change during the competition, so run `make sync-maps` and review the changelog before promoting a submission.

## Current release of record

The trusted local comparator is the immutable **v0047 pressure-economy steward** at
`bots/versions/v0047_pressure-economy-steward_20260821-0200_eeafad8f`. The mutable
`bots/candidate/` tree is an exact production copy of that snapshot after the
rejected v411 experiment was rolled back. Older local snapshots are intentionally
not retained; their hypotheses and results remain in `experiments/`, `UPDATES.md`,
and the ignored `reports/` evidence directories.

The platform observation state in `state/live_state.json` is historical operational
evidence and is not the local comparison baseline. Do not infer a new promotion or
activation from packaging alone.

## Start here

1. Install Python 3.12 or 3.13.
2. Install and authenticate the game CLI:
   ```bash
   python -m pip install --upgrade fcode
   fcode login
   ```
3. Install Codex and authenticate it:
   ```bash
   codex login
   ```
4. Run the local checks:
   ```bash
   make refresh-start
   make doctor
   make codex-doctor
   make setup-codex-v1
   make sync-maps
   make smoke
   make eval-regression
   make eval-local
   ```
   The evaluation configs pin the v0047 comparator. Keep the short smoke and
   all-map regression checks reproducible before considering a new candidate.
5. Open Codex in this repository and use:
   ```text
   Use the FCL orchestration protocol. Implement the next approved milestone from
   docs/IMPLEMENTATION_PLAN.md. Sol must plan, Luna must implement, and Sol must
   review the diff and test evidence before the task is considered complete.
   ```
6. You do not need to tell Codex to reread the repository in each new chat. Root and nested `AGENTS.md` files route it through `docs/START_HERE.md`, durable state, and only the relevant detailed documents.

7. After an approved candidate passes the release and remote gates, an operator
can package and deploy it with:
   ```bash
   make release-live SLUG=my-change
   ```
   Live commands are platform writes. Run them only after reviewing
   `scripts/AGENTS.md`, `docs/SUBMISSION_AND_VERSIONING.md`,
   `docs/LIVE_AUTOPILOT.md`, and fresh `state/live_state.json`.

## Working agreement

- Change one bounded hypothesis at a time and compare it with the current release
  of record before promotion.
- Keep `bots/baseline/` and `bots/versions/` immutable during experiments. The
  retained v0047 snapshot is the rollback source; `bots/candidate/` is the only
  mutable upload tree.
- Save human-readable experiment notes and metrics. Generated replays, caches,
  temporary experiment configs, and handoff archives are ignored by Git.
- A failed candidate is rolled back to exact v0047 parity; it is not silently
  promoted because of a single aggregate result.

## Key documents

- [`docs/START_HERE.md`](docs/START_HERE.md): generated concise startup context for every new Codex session.
- [`state/project_state.json`](state/project_state.json): machine-readable current milestone, hypothesis, experiment, and next task.
- [`UPDATES.md`](UPDATES.md): durable cross-session change, deployment, score, and rollback history.
- [`GAME_RULES.md`](GAME_RULES.md): current rules, entities, API, map pool, tutorial lessons, and known tutorial traps.
- [`AGENTS.md`](AGENTS.md): compact permanent instructions loaded by Codex.
- [`docs/CODEX_HARNESS.md`](docs/CODEX_HARNESS.md): verified native-V1/process-fallback Sol → Luna → Sol orchestration.
- [`docs/LIVE_AUTOPILOT.md`](docs/LIVE_AUTOPILOT.md): autonomous resumable upload, activation, observation, promotion, and rollback.
- [`docs/SUBMISSION_AND_VERSIONING.md`](docs/SUBMISSION_AND_VERSIONING.md): exact CLI and immutable-version workflow.
- [`docs/EVALUATION_PLAN.md`](docs/EVALUATION_PLAN.md): local, remote, and live-ladder evaluation with metrics and gates.
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md): staged bot architecture and strategy roadmap.
- [`docs/REPOSITORY_STRUCTURE.md`](docs/REPOSITORY_STRUCTURE.md): repository map and ownership.
- [`docs/REPOSITORY_CLEANUP.md`](docs/REPOSITORY_CLEANUP.md): retained release, cleanup scope, and verification record.
- [`docs/PROJECT_CONSIDERATIONS.md`](docs/PROJECT_CONSIDERATIONS.md): risks, anti-patterns, and extra recommendations.
- [`docs/SELF_REVIEW.md`](docs/SELF_REVIEW.md): verification performed, limitations, and unresolved checks.
- [`docs/SOURCE_INDEX.md`](docs/SOURCE_INDEX.md): public sources and authority rules.

## Safety defaults

- Autonomous live operations are enabled by policy only after `live-bootstrap` records a rollback target.
- Upload, activation, observation, promotion, and rollback are durable across sessions.
- Local evaluation runs both sides, multiple maps, and deterministic seeds.
- The working candidate is never treated as an immutable release.
- All game actions must be gated by their matching `can_*` predicate.
- Costs are queried through the API rather than hard-coded.
- Uncaught exceptions are treated as fatal because they permanently destroy that unit.
- Local tests enforce the ladder's 10 ms per-unit, per-round CPU limit.

## Important current balance note

The **2026-08-04** changelog changed Gunner and Sentinel balance. Current values include:

- Gunner: 25 HP, 20 Ti base cost, 7 damage, 4 ammo/shot, +20% scale.
- Sentinel: 40 HP, 30 Ti base cost, 18 damage, 10 ammo/shot, 2-round reload.

Do not copy old snippets that assume 10-damage, 10-Ti, 2-ammo Gunners or 3-round Sentinel reloads.
