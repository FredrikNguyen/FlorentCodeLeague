# Candidate bot instructions

## Workflow

- Use the current Luna XHigh session directly.
- Do not spawn subagents.
- Read `docs/START_HERE.md`, `docs/CURRENT_PLAN.md`, and only the game
  documentation relevant to the requested change.
- Implement, run focused tests, inspect the diff, and fix discovered defects
  in the same session.
- Do not run the full map matrix unless this is explicitly a release candidate.

## Runtime invariants

- `main.py` must expose `Player`.
- Use pure Python supported by the competition sandbox.
- Keep all per-unit work bounded and below the 10 ms turn limit.
- Builder movement must be cardinal.
- Gate actions through the matching `can_*` method.
- Respect move/action exclusivity.
- Query current costs through the Controller API.
- Account for the Global Store's one-round write delay.
- Never allow an exception to escape `run()`.
- Preserve deterministic behavior for a fixed seed.
- Avoid large allocations, repeated full-map scans, deep copies, recursion,
  and verbose runtime logging.

## Testing

For ordinary changes:

1. Run relevant unit tests.
2. Run `make static`.
3. Run `make smoke` for behavior changes.

Run `make eval-regression` only at an experiment checkpoint.

Run the full local matrix and remote gate only for a release candidate.

Store full output under `reports/`; return only a concise summary and paths.