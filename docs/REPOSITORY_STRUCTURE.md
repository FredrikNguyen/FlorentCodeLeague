# Repository structure

```text
.
├── AGENTS.md
├── UPDATES.md
├── GAME_RULES.md
├── README.md
├── Makefile
├── pyproject.toml
├── fcode.toml.example
├── .codex/
│   ├── config.toml
│   ├── agents/
│   │   ├── sol-planner.toml
│   │   ├── luna-implementer.toml
│   │   └── sol-reviewer.toml
│   └── skills/
│       └── fcl-orchestration/
│           └── SKILL.md
├── bots/
│   ├── baseline/
│   │   └── main.py
│   ├── candidate/
│   │   ├── AGENTS.md
│   │   ├── main.py
│   │   └── bot/
│   │       ├── __init__.py
│   │       ├── player.py
│   │       ├── comms.py
│   │       └── navigation.py
│   └── versions/
│       └── .gitkeep
├── configs/
│   ├── codex_harness.toml
│   ├── eval_smoke.toml
│   ├── eval_regression.toml
│   ├── eval_matrix.toml
│   └── live_policy.toml
├── docs/
│   ├── START_HERE.md
│   ├── CODEX_HARNESS.md
│   ├── LIVE_AUTOPILOT.md
│   ├── SUBMISSION_AND_VERSIONING.md
│   ├── EVALUATION_PLAN.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── REPOSITORY_STRUCTURE.md
│   ├── PROJECT_CONSIDERATIONS.md
│   ├── SELF_REVIEW.md
│   └── SOURCE_INDEX.md
├── experiments/
│   └── TEMPLATE.md
├── state/
│   ├── project_state.json
│   ├── live_state.json
│   └── codex_runtime.json          # generated, ignored
├── schemas/
│   └── live_decision.schema.json
├── scripts/
│   ├── AGENTS.md
│   ├── project_context.py
│   ├── refresh_start_here.py
│   ├── set_project_state.py
│   ├── update_log.py
│   ├── codex_task.py
│   ├── codex_task.sh
│   ├── codex_luna_doctor.py
│   ├── setup_codex_v1_catalog.py
│   ├── codex_v1.sh
│   ├── codex_v2_visible.sh
│   ├── doctor.py
│   ├── common.py
│   ├── run_local_matrix.py
│   ├── remote_gate.py
│   ├── package_candidate.py
│   ├── submit_candidate.py
│   ├── activate_submission.py
│   ├── capture_live.py
│   ├── release_candidate.py
│   ├── live_operator.py
│   └── live_autopilot.py
├── tests/
│   ├── AGENTS.md
│   ├── test_static_contract.py
│   ├── test_harness_contract.py
│   └── test_startup_context.py
├── maps/
│   └── .gitkeep
├── replays/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
└── artifacts/
    ├── platform/
    │   └── .gitkeep
    └── submissions/
        └── .gitkeep
```

## Instruction hierarchy

- Root `AGENTS.md` defines the mandatory session bootstrap, orchestration, global game invariants, and live-operation authority.
- `bots/candidate/AGENTS.md` adds game-runtime, packaging, and candidate-testing rules.
- `scripts/AGENTS.md` adds tooling, state, credentials, and platform-write rules.
- `tests/AGENTS.md` requires deterministic offline tests and forbids real platform operations.
- Codex must read the nearest applicable instruction file for every path it changes.

## Cross-session sources

- `state/project_state.json`: authoritative current milestone, hypothesis, experiment, next task, and recent Codex report.
- `state/live_state.json`: authoritative upload, activation, observation, promotion, and rollback state.
- `UPDATES.md`: human-readable append-only implementation and live history.
- `docs/START_HERE.md`: generated concise view used at the start of every session.

Use `scripts/set_project_state.py` to change development focus and `make refresh-start` to regenerate the startup view. Live-state scripts regenerate it automatically.

## Ownership

### Root guidance

- `AGENTS.md`: short durable routing and invariants Codex always loads.
- `GAME_RULES.md`: current mechanics snapshot.
- `README.md`: operator entry point.
- `UPDATES.md`: durable historical handoff.

### `.codex/`

Native custom-agent configuration plus the orchestration skill. Model/reasoning changes must be deliberate and validated through a harness report.

### `bots/baseline/`

Frozen comparator corresponding to the currently trusted local baseline. Never edit it during an experiment.

### `bots/candidate/`

Only mutable bot implementation. It must be a self-contained uploadable directory with `main.py`.

### `bots/versions/`

Immutable snapshots created by `package_candidate.py`. Never hand-edit a snapshot.

### `configs/`

Evaluation, harness, and live-operation policies. Bot runtime must not depend on repository configs unless copied into the submission.

### `experiments/`

One human-readable hypothesis/result record per candidate version.

### `scripts/`

Operator and automation tooling. Only the primary Sol/operator executes platform writes under live policy; Luna may implement but not operate them.

### `reports/`

Generated evaluation and harness evidence, grouped by run ID.

### `maps/`

Synced platform maps. `fcode maps sync` updates/adds but does not remove retired maps.

### `artifacts/`

Packaged submissions and downloaded platform copies. Hash these for provenance.

## Growth rules

Add a module when it owns a coherent policy/state machine, can be tested independently, reduces coupling, and has a stable boundary. Keep startup guidance concise: detailed material belongs in `docs/`, while `AGENTS.md` should route agents to exactly what they need.
