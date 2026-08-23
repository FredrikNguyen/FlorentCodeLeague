# AGENTS.md

## Mission

Build the strongest reliable Florent Code League bot through small, measurable, reversible experiments while minimizing model usage.

## Default workflow: one Luna session

- The repository defaults to **`gpt-5.6-luna` with `xhigh` reasoning**.
- Work as one implementation agent: inspect, implement, run focused tests, inspect the diff, fix defects, and summarize.
- **Do not spawn subagents** and do not start Sol planner/reviewer processes unless the user explicitly asks.
- Sol planning normally happens in standard ChatGPT using `artifacts/chatgpt/PLANNING_PACKET.md`, outside the Codex agentic pool.
- Sol review is optional and normally reserved for release candidates, architecture rewrites, unexplained regressions, or explicit user requests.

## Baseline comparison and promotion

- Every candidate is compared directly against the immutable moving baseline
  recorded in `state/project_state.json`; do not compare it to an older control
  or infer improvement from a standalone score.
- Paired aggregate win rate is the primary promotion metric. A clear positive
  margin in the direct 15-game screen (and a materially positive result in the
  60-game gate) is sufficient even when one or two maps regress; localized map
  regressions are recorded as risks rather than an automatic veto.
- The 15-game screen uses one deterministic stratified-random pair for each
  configured map. `screen_seed` is rotated per iteration and retained in the
  report manifest, so map/seed selection cannot be tuned to a fixed subset.
  Side-order coverage remains in the 60-game gate: all 15 configured maps,
  endpoint deterministic seeds `1` and `101`, and both side orders. Historical
  210-game runs remain archival evidence, not routine work.
- Reliability remains a hard safeguard: command failures, escaped exceptions,
  TLEs, suspicious output, or a severe delivery/no-delivery collapse block
  promotion regardless of aggregate wins.
- When the aggregate result qualifies, archive the candidate as the new
  immutable baseline, update all evaluation configs and durable state, then
  package/upload through the guarded submission workflow. Keep the prior
  baseline available for rollback and observe the live submission before the
  next experiment.

## Parallel Luna evaluation

- The root agent remains the orchestrator and owns the durable checkpoint.
- For an explicitly requested parallel iteration, start one Luna worker from
  an immutable copy of the current candidate to run the baseline screen or
  replay analysis, and a separate Luna worker for the single production
  hypothesis. The test worker must snapshot before the implementation worker
  edits the shared candidate.
- Only one worker may write production candidate files for an iteration.
  Workers must state their owned files, preserve unrelated dirty work, and
  leave plans/state/baseline/version snapshots to the root agent.
- Reconcile the snapshot result and implementation result before promotion;
  a parallel screen is evidence for the exact pre-edit candidate, not proof
  of the edited candidate. If the implementation cannot preserve the Store
  schema or another invariant, stop and record the blocker instead of widening
  the iteration.

## Startup context

At the start of a session:

1. Read `docs/START_HERE.md`.
2. Read the nearest nested `AGENTS.md` for files you will change.
3. Run `git status --short` and inspect the relevant diff.
4. When asked to implement an external plan, read `docs/CURRENT_PLAN.md`.
5. Read only the source files and document sections needed for the task.

Do **not** read every long document automatically: `GAME_RULES.md`, `UPDATES.md`, the implementation roadmap, evaluation plan, and deployment docs are conditional. `docs/START_HERE.md` routes you to them when necessary.

Task-specific required reading is listed in `docs/START_HERE.md`; load only the source and document sections needed for the task.

## Task execution

For a normal change:

1. State a compact hypothesis and exact scope.
2. Modify only the needed files.
3. Run focused unit/static checks and at most the smoke tier unless broader testing is necessary for the hypothesis.
4. Inspect `git diff` yourself and correct obvious issues in the same session.
5. Keep the final report under 16 lines: change, tests, result, risks, and next step.
6. Let the deterministic wrapper record the run in `UPDATES.md` and `state/project_state.json`.

Use broader gates only at these points:

- **Experiment checkpoint:** `make eval-regression`
- **Release candidate:** `make eval-local`, `make remote-gate`, optional external Sol review
- **Live release:** deterministic release/live scripts after the release gate

Never paste full logs into model context. Save logs under `reports/` and report only concise summaries plus paths.

## External planning handoff

To obtain a Sol High plan in regular ChatGPT:

```bash
make chatgpt-plan REQUEST="<exact planning question>"
```

Upload **one file**:

```text
artifacts/chatgpt/PLANNING_PACKET.md
```

It contains the planning prompt, current state, concise rules and architecture, candidate source, recent updates, and current diff. Copy the returned plan into `docs/CURRENT_PLAN.md`, then run:

```bash
make luna-plan
```

## Context and compaction discipline

- When a coherent milestone is complete, run `make handoff` to refresh the durable handoff and ChatGPT packet.
- Prefer a fresh Codex session for a different experiment.
- Use `/compact` only when continuing the same experiment and context is becoming large.
- Compaction does not recover spent usage; durable short handoffs are the main optimization.

## Core game invariants

- `main.py` exports `Player`; submission code is pure Python.
- Gate every game action with its matching `can_*` call.
- Builder movement is cardinal only; build/attack/heal/destroy are orthogonally adjacent.
- A Builder cannot move and act in the same round.
- An escaping exception permanently destroys that unit.
- Query dynamic prices with `ct.get_*_cost()`.
- The Global Store has 16 non-negative integer slots with one-round-delayed writes.
- Keep work bounded and target local p99 CPU below 8 ms with `--tle 10`.
- Preserve deterministic fixed-seed behavior unless randomness is the experiment.

## Change discipline

- One hypothesis per candidate.
- Never edit `bots/baseline/` during an experiment.
- Never overwrite immutable `bots/versions/` snapshots.
- Keep `docs/CURRENT_PLAN.md` limited to the currently approved external plan.
- Update durable state before ending a meaningful milestone.

## Live operations

Live monitoring, score comparison, promotion, and rollback are deterministic Python operations. Do not repeatedly invoke a model to poll the ladder.

Before platform operations, read `scripts/AGENTS.md`, `docs/SUBMISSION_AND_VERSIONING.md`, `docs/LIVE_AUTOPILOT.md`, and fresh `state/live_state.json`.
