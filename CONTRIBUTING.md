# Contributing

Keep each change focused and compare behavior directly with `bots/baseline/`.

1. Create the environment with `uv sync` and sync maps with `make sync-maps`.
2. Change only `bots/candidate/` for strategy experiments.
3. Add or update a focused deterministic test.
4. Run `make check` and `make smoke`.
5. Use `make eval-regression` before proposing a strategic change and
   `make eval-local` for a release candidate.
6. Inspect the full diff and keep generated maps, reports, replays, snapshots,
   packages, credentials, and local experiment notes out of Git.

Do not upload or activate a submission as part of an ordinary contribution.
Platform writes require explicit operator confirmation.
