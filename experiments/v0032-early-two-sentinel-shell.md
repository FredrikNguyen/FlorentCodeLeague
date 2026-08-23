# v0032 early two-sentinel shell

## Objective

Improve win rate against the immutable v97 direct-siege bot by preserving an
early combat shell on maps where the opponent converts its opening titanium
into sentinels quickly. Resource totals are secondary to actually winning the
game, but the change must not introduce command failures or protected-map
losses.

## Evidence and hypothesis

The live v97 replay set repeatedly showed a delayed combat shell: our side
often built many builders/conveyors and only one sentinel while the opponent
had 3--10 sentinels or gunners. The local v97 matrix also showed the same
failure mode. The bounded hypothesis is that the early sentinel pool should
target two pieces rather than one; this keeps the first defensive/offensive
shell intact without imposing a broad economy gate.

## Change

Changed only `SENTINEL_POOL_TARGET_EARLY` in
`bots/candidate/bot/constants.py` from `1` to `2`. No route, unit, economy,
or map-specific behavior was changed.

## Comparison and decision

The candidate won 58/96 in two disjoint focused slices and 114/210 in the
full 21-map release matrix against immutable v97, versus v97's 96/210 paired
wins. Every full-matrix process completed cleanly. This is accepted because
the user prioritizes substantially higher win rate even when the winning side
has less ore/titanium; resource collection is retained as a diagnostic, not
the selection objective.

## Validation

- Focused defense tests: 6/6 passed; `reports/final-v0032-focused-unittest.log`.
- `python -m pytest` was unavailable in the environment (`No module named
  pytest`); `unittest` is the equivalent focused run used here.
- Candidate compileall: passed; `reports/final-v0032-compile.log`.
- `make smoke`: 4/4 command-clean; `reports/local-20260813T183012Z`.
- Full release matrix: 210/210 command-clean, 114/210 wins; manifest and
  replays under `reports/local-20260813T180421Z`, replay analysis under
  `reports/local-early-two-sentinels-v97-210-analysis.json`.
- `make static`: exit 2 on 15 inherited obsolete pre-v86 test imports; the
  candidate-focused tests and compile check pass; `reports/final-v0032-static.log`.
- `git diff --check`: passed; `reports/final-v0032-diff-check.log`.

## Risks and next step

The full-matrix edge is real but modest, and live superiority is not yet
attributable. The candidate can be uploaded with v97 retained as the previous
active target and v72 retained as the guarded last-known-good rollback.
