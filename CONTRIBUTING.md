# Contributing

Keep changes small, measurable, and reversible.

1. Read `docs/START_HERE.md` and the nearest `AGENTS.md`.
2. Start from `bots/candidate/`; never edit the retained version snapshot.
3. Test one hypothesis against the baseline recorded in
   `state/project_state.json`.
4. Run focused tests, `make static`, and at most `make smoke` for an ordinary
   change. Broader gates belong at experiment or release checkpoints.
5. Keep generated maps, replays, reports, packages, and handoff packets out of
   Git. Record concise durable evidence in an experiment note and `UPDATES.md`.
6. Inspect the complete diff before committing. Do not include credentials or
   authenticated platform output.

Live upload, activation, promotion, and rollback are operator actions. Follow
`docs/SUBMISSION_AND_VERSIONING.md` and `docs/LIVE_AUTOPILOT.md` before using
those workflows.
