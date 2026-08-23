# v309 — compact control-first opening

## Objective and evidence

The active v107 replay evidence shows a compact-map control failure: Yulerune
reached six Builders but only one Harvester and no delivery, while the winning
side used early Launchers/Sentinels; AuroraVeil delivered at round 150 versus
24.  The top-team audit records early control-first openings on 8/15 winner
replays.  v308 already rejected an all-map post-route Launcher relay, so this
experiment couples the unit-control action to the compact opening only.

## Allowed files and non-goals

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py` for named compact-opening limits
- one focused `tests/test_candidate_compact_control.py`
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, durable state, and reports

No baseline/archive, Store schema, route FSM/selection, dynamic task policy,
Builder spawn target, Barrier/Gunner/ammo policy, wide-map behavior, package,
upload, activation, or live-state change is allowed.  All construction and
Launcher actions require their matching legality gates and strict visible
progress destinations.

## Validation plan

Run the focused compact-control tests plus the current route/defense subset,
compileall, `make static`, `make smoke`, then the configured rotated 15-map
screen against immutable v0044.  If the screen is negative, allow one
compact-control-only repair and then restore exact source parity.  No release
gate or platform operation is justified by this experiment alone.

## Status

Rejected after one bounded repair; source rolled back to exact immutable v0044
parity and no release/live operation performed.

## Validation and decision

- Focused compact-control/route/defense subset: **39/39** after the repair;
  `reports/iter-v309-compact-control/focused-repair.log`.
- Candidate compileall and smoke: compileall passed; smoke was **4/4** at
  `reports/local-20260819T223705Z`.
- `make static`: retained the inherited profile of 15 obsolete removed-module
  imports and two navigation fast-path assertions; no v309-specific failure.
- Initial rotated screen: **3–12**, command-clean, with compact delayed
  delivery; `reports/local-20260819T223320Z` and
  `reports/iter-v309-compact-control/replay-analysis.json`.
- Bounded repair screen: **9–6**, command/delivery-clean; no TLE or suspicious
  output; `reports/local-20260819T223741Z` and
  `reports/iter-v309-compact-control/replay-analysis-repair.json`.
- 60-game endpoint gate: **31–29 (51.7%)**, 60/60 command-clean;
  `reports/local-20260819T224021Z`.
- Decision: reject.  The repair recovered economy but did not establish a
  repeatable aggregate or map-conditioned edge, and the new Launcher path did
  not activate materially.  Candidate production source was restored to exact
  v0044 parity; v0044 remains the baseline and v105 remains the live rollback.
