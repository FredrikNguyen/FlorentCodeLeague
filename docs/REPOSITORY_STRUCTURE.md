# Repository structure

```text
.
├── bots/
│   ├── candidate/       submission-ready implementation
│   └── baseline/        frozen local comparator
├── configs/             smoke, regression, and release matrices
├── docs/                public strategy and operator documentation
├── scripts/             evaluation, replay, package, and platform wrappers
├── tests/               deterministic unit and contract tests
├── GAME_RULES.md        dated game/API reference snapshot
├── Makefile             supported development commands
├── fcode.toml           local CLI defaults
├── pyproject.toml       Python and Ruff configuration
└── uv.lock              reproducible dependencies
```

## Bot trees

`bots/candidate/` is the only tree changed during strategy development.
`bots/baseline/` is an identical frozen comparator in this public release. Both
are self-contained bot directories with a `main.py` entry point and local
`bot/` package.

## Generated directories

The following paths are created locally and ignored:

- `maps/`: maps downloaded by `fcode maps sync`;
- `reports/`: evaluation and platform JSON/log output;
- `replays/`: local and downloaded replay files;
- `artifacts/`: packaged submissions and platform downloads;
- `bots/versions/`: immutable package snapshots;
- `experiments/` and `state/`: optional private development records.

The public repository intentionally excludes authenticated account data,
historical experiment notes, model/agent configuration, and generated handoff
material.
