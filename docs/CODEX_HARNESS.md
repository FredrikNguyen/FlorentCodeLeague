# Cost-efficient Codex workflow

## Default

The repository now uses **one Codex worker**:

```text
GPT-5.6 Luna · XHigh
    → inspect
    → implement
    → focused tests
    → self-review diff
    → concise handoff
```

No subagent orchestration is enabled by default. This avoids repeated Sol planning/review calls, duplicated context reads, and the V1/V2 subagent-routing failure mode.

## Planning

Use Sol High in ordinary ChatGPT only for meaningful strategy or architecture work:

```bash
make chatgpt-plan REQUEST="<exact planning question>"
```

Upload `artifacts/chatgpt/PLANNING_PACKET.md`. The planning request is embedded at the top. Save the resulting bounded plan into `docs/CURRENT_PLAN.md` and run:

```bash
make luna-plan
```

For a small obvious fix, skip external planning and use:

```bash
make luna TASK="Fix <precise defect> and run the focused tests"
```

## Why Luna XHigh by default

Luna performs implementation, tests, debugging, and a first-pass review in one context. XHigh is intentionally the default because the bot has coupled state machines, pathfinding, economy, and strict legality/CPU constraints. For documentation-only work you may override it manually with a lower effort, but the repository does not spawn another model to decide that.

## Testing tiers

### Routine change

- relevant unit tests;
- syntax/static checks;
- up to four smoke games when behavior changes.

### Experiment checkpoint

- regression subset;
- paired side swaps and deterministic seeds;
- summarized report only.

### Release candidate

- full map matrix;
- remote gate;
- optional external Sol review using `artifacts/chatgpt/RELEASE_REVIEW_PACKET.md`;
- package and deploy.

## Compaction

Use `/compact` only to continue the same experiment after context grows. Before compacting or opening a new session:

```bash
make handoff
```

This refreshes `docs/START_HERE.md` and both ChatGPT packets. A fresh session plus a small handoff is preferred when moving to a different experiment.

## Evidence

Each `make luna` or `make luna-plan` run writes:

```text
reports/luna-<timestamp>/
  events.jsonl
  events.jsonl.stderr
  final.md
  manifest.json
```

The deterministic wrapper records the model, effort, task, exit code, report path, and compact final summary in `UPDATES.md` and project state.
