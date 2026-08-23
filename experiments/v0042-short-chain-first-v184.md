# v184 short-chain-first opening economy

## Objective

Reduce first-delivery delays on maps where the closest visible ore is far from
the Core. During the opening three completed routes, rank visible and
advertised ore by estimated Core distance first, then Builder distance; return
to local-nearest ore once the economy is mature.

## Comparator and scope

- Comparator: immutable `bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f`.
- Allowed bot files: `bots/candidate/bot/defender.py` and its focused test.
- Evaluation workflow: `configs/eval_regression.toml` and
  `tests/test_eval_schedule.py` reduce the quick screen from 18 to 16 games:
  all 15 maps plus one seeded side-order repeat. The release gate remains 60
  games with both sides and endpoint seeds.
- Non-goals: combat, Launcher/Splitter behavior, home defense, navigation,
  Store schema, baseline/archive files, and live operations before a passing
  release gate.

## Done criteria

- Opening target selection has focused coverage for short-Core-route and
  mature-local-nearest behavior.
- Focused tests, compileall, smoke, and static checks are recorded; static may
  retain only the known inherited failures.
- The 16-game screen covers every configured map, is command-clean, and shows
  a material aggregate win-rate or first-delivery/no-delivery improvement.
- Only a positive screen advances to the 60-game release gate. A failed screen
  gets at most two bounded repairs, then candidate source returns byte-identical
  to v0042 and the rollback is recorded.

## Result

Rejected after the initial **4-12** 16-game screen, repair 1 (**7-9**), and
repair 2 (**6-10**). All 16 games in each run were command-clean and every
configured map was represented, but neither repair produced a material
aggregate edge or reliable first-delivery improvement. The candidate source
was restored byte-identically to v0042 (`reports/iter-v184-rollback-source-diff.txt`).

Validation records:

- Focused target/schedule tests: 8/8 initially and 9/9 after repair 2;
  rollback focused suite 38/38.
- Compileall passed for every repair and rollback.
- `make smoke` was 4/4 command-clean for every repair and rollback.
- `make static` retained only the inherited 15 obsolete-import errors and two
  navigation fast-path assertions; no new v184 static defect remained after
  rollback.
- Initial screen: `reports/local-20260818T075636Z` and
  `reports/iter-v184-short-chain-screen.log`.
- Repair 1 screen: `reports/local-20260818T075927Z` and
  `reports/iter-v184-short-chain-repair1-screen.log`.
- Repair 2 screen: `reports/local-20260818T080334Z` and
  `reports/iter-v184-short-chain-repair2-screen.log`.
- Rollback checks: `reports/iter-v184-rollback-focused.log`,
  `reports/iter-v184-rollback-compileall.log`,
  `reports/iter-v184-rollback-static.log`,
  `reports/iter-v184-rollback-smoke.log`.
- Final post-rollback confirmation: focused 38/38,
  `reports/iter-v184-final-focused.log`; compileall passed,
  `reports/iter-v184-final-compileall.log`; smoke 4/4,
  `reports/iter-v184-final-smoke.log` (matrix report
  `reports/local-20260818T081246Z`).

No 60-game release gate, package, upload, activation, or baseline transition
occurred. The 16-game all-map quick-screen policy remains in place; the
immutable v0042 bot and platform v105 are unchanged.
