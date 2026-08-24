# Florent Code League bot

This is a complete Python bot for the Florent Code League. It builds a
scalable titanium economy, maintains conveyor routes, adapts builders to the
current map state, defends its Core, and converts surplus capacity into sustained
pressure on the opponent.

The repository contains the submission-ready bot, an identical frozen comparator,
local evaluation tools, focused tests, and guarded package/upload commands. It
does not include private match data, generated reports, submission archives, or
the internal experiment history used to develop the bot.

## Strategy

- The Core grows the workforce in stages, preserves construction liquidity, and
  supplies ammunition only when the economy and threat state justify it.
- One permanent defender protects the economic floor while two permanent
  attackers maintain pressure; remaining builders choose tasks dynamically.
- Defenders discover ore, build Harvesters, connect directed Conveyor chains,
  repair broken routes, and reinforce home defense.
- Attackers scout for the enemy Core, deploy forward Sentinels, sabotage loaded
  logistics, and cage valuable enemy territory.
- Dynamic builders switch among economy, repair, defense, raiding, and forward
  support instead of remaining idle after their original task ends.
- All movement and work are deterministic, bounded, and guarded by the matching
  `can_*` API call.

See [the strategy guide](docs/STRATEGY.md) for the architecture and Store
protocol.

## Repository layout

```text
bots/candidate/   submission-ready bot
bots/baseline/    frozen comparator for local evaluation
configs/          smoke, regression, and release matrices
scripts/          evaluation, replay, package, upload, and activation tools
tests/            deterministic offline tests
docs/             strategy, evaluation, submission, and game references
```

## Setup

Requirements: Python 3.12 or 3.13, [`uv`](https://docs.astral.sh/uv/), and the
Florent Code League CLI.

```bash
uv sync
uv run fcode login
make sync-maps
make check
```

`make check` runs the pinned Ruff lint gate, 51 focused tests, and Python
compilation checks. Synced maps, reports, replays, packages, credentials, caches,
and local experiment data are ignored by Git.

## Run and evaluate

```bash
make smoke            # four quick local games
make eval-regression  # 15-map screening gate
make eval-local       # 60-game release matrix
make remote-gate      # server-side validation
```

All local matrices enforce the ladder's 10 ms limit and compare both side
orders where applicable. Reports are written under `reports/`.

To inspect a single replay:

```bash
uv run fcode run bots/candidate bots/baseline MAP --seed 1 --tle 10 \
  --replay replays/example.replay26
uv run fcode watch replays/example.replay26
```

## Package and submit

```bash
make package SLUG=release
uv run python scripts/submit_candidate.py artifacts/submissions/FILE.zip \
  --name florent-bot-release --confirm
uv run python scripts/activate_submission.py VERSION --confirm
```

Packaging creates an ignored immutable snapshot, ZIP, and SHA-256 manifest.
Upload and activation are deliberately separate commands and both platform
writes require explicit confirmation. See
[submission and versioning](docs/SUBMISSION_AND_VERSIONING.md) for details.

## Documentation

- [Strategy and architecture](docs/STRATEGY.md)
- [Evaluation methodology](docs/EVALUATION_PLAN.md)
- [Submission and versioning](docs/SUBMISSION_AND_VERSIONING.md)
- [Repository structure](docs/REPOSITORY_STRUCTURE.md)
- [Game rules snapshot](GAME_RULES.md)
- [Official source index](docs/SOURCE_INDEX.md)

## License

Copyright © 2026 Fredrik Nguyen. This is source-available competition code;
no permission to reuse or redistribute it is granted. See [LICENSE](LICENSE).
