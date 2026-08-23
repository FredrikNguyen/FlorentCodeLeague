# v0073 — quiet-defense turret retirement and workforce reuse

## Objective

Use the game's legal `destroy()` action to retire exactly one surplus home
Gunner after a long, successful defensive window, then spend the freed unit
capacity on one additional Builder. The experiment targets late-game unit-cap
and workforce waste without changing turret damage, Sentinel placement, route
construction, or threat response.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/core_role.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- `tests/candidate_fakes.py` only for the destroy/visibility fixture needed by
  the focused test;
- this record, `UPDATES.md`, and `state/project_state.json`.

## Non-goals

- no edits to `bots/baseline/` or immutable version snapshots;
- no Sentinel, Launcher, attack-target, route-FSM, navigation, or ammo-policy
  changes;
- no turret relocation or automatic rebuild after retirement;
- no retirement on cramped maps, before the economy is established, while a
  home threat is visible, or more than once per game;
- no platform upload, activation, or live-state change.

## Hypothesis

Once five completed routes, a rich bank, and a long threat-free interval prove
that the home shell has done its job, one outer home Gunner has lower marginal
value than a mobile Builder. A deterministic nearest Builder can destroy that
Gunner, and the Core can raise its late workforce target by one only after the
retirement is observed. The marker is one-round delayed through the existing
Store slot and cannot authorize a second retirement.

## Done criteria

- Focused tests prove the retirement marker is emitted only after the quiet,
  rich, non-cramped gate; the nearest eligible Builder destroys one adjacent
  friendly Gunner; and no second retirement is selected after completion.
- Existing v0072 nearest-threat and route behavior tests remain green.
- `make static`, compileall, `make smoke`, and `git diff --check` complete with
  the known inherited static result documented separately.
- The paired screen against v0032 is command-clean, has p99 below 8 ms, and
  materially improves win rate or collection without a delivery collapse. A
  broad map regression is acceptable only if the aggregate win-rate gain is
  clearly substantial under the moving-baseline policy.

## Result

- Focused lifecycle and regression tests passed 11/11; candidate compileall
  passed; `make smoke` was 4/4 command-clean; `git diff --check` passed.
  `make static` retained the inherited exit-2 obsolete-import result. Final
  logs are under `reports/iter-turret-retirement-v0073/`.
- The 54-game paired screen against v0032 was **34/54 candidate wins versus
  20 comparator wins** (63.0% versus 37.0%), with 258,030 versus 255,210
  collected titanium (1.0110x), zero no-delivery rows for either side, zero
  command failures/TLE/suspicious output, max p99 1,323 us, and peak callback
  4,760 us. Report: `reports/local-20260815T044840Z`; replay analysis:
  `reports/iter-turret-retirement-v0073/screen-analysis.json`.
- Map wins were at least even everywhere: Sprint 3-3, String 5-1, Bridge 4-2,
  Crossfire 3-3, Atoll 3-3, Sweden 4-2, Longship 5-1, Vault 4-2, and Aurora
  3-3. The candidate's post-round-400 replay stream contains no delivery
  collapse and remains under the local CPU budget.
- Status: **promotion 3 accepted locally** under the moving win-rate policy.
  The 14-win margin is substantial enough to accept. The immutable archive is
  `bots/versions/v0033_turret-retirement-workforce-reuse_20260815-0458_eeafad8f`
  with package SHA-256
  `4cea9045227bfa1ef9b0251c88078d01a4d0260b1374ef5f41f03d15d2507145`; no
  upload or activation was performed.
