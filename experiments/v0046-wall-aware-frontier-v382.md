# v382 wall-aware visible-frontier navigation — rejected

## Objective and scope

Fresh live and local replay review showed late conversion on obstacle-heavy
maps.  Starting from immutable v0046, v382 changed only
`bots/candidate/bot/navigation.py`: visible frontier selection briefly used
the BFS path length plus Manhattan remainder instead of Euclidean closeness
alone.  The intent was to keep route builders on a reachable wall-side
corridor.  One deterministic wall-corridor unit test was added temporarily.

Non-goals were economy, route construction, roles, combat, unit spending,
Store layout, baseline snapshots, packaging, submission, activation, and live
state.

## Validation

- Targeted wall/blocked/danger navigation checks passed **3/3**; nearest-defense
  coverage passed **26/26**; compileall passed.
- `make static` retained the inherited repository profile: 15 obsolete-module
  import errors and two pre-existing navigation fast-path assertions.  The
  v382-specific wall test passed.
- Smoke was **4/4** command-clean at
  `reports/local-20260820T223420Z`.
- The rotated all-15-map/30-game paired screen (`screen_seed=571`) was
  command-clean but only **13–17**.  Candidate delivered **29/30** versus
  **30/30**, collected **144,740 vs 166,860 Ti**, and had zero TLE or
  suspicious-output rows; max p99/peak was **1,247/2,621 us**.  Raw games and
  per-game diagnostics are in `reports/local-20260820T223504Z` and
  `reports/iter-v382-wall-aware/analysis.json`.

The candidate lost both conversion and win-rate floors, so no second screen,
release gate, package, upload, activation, or live operation was justified.

## Rollback and decision

The temporary navigation and test changes were removed.  Rollback focused
coverage passed **26/26**, compileall passed, rollback smoke was **4/4** at
`reports/local-20260820T223858Z`, and recursive candidate parity with immutable
v0046 is empty at `reports/iter-v382-wall-aware/rollback-source-parity.diff`.

Reject v382.  Immutable v0046 remains the local baseline; the next experiment
must use a distinct replay-backed conversion or defensive hypothesis rather
than another generic navigation score.
