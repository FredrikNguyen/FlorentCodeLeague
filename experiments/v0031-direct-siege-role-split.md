# v0031 direct-siege role split

## Objective

Use the fresh v95 loss replays and Pivot/top-team replays to remove the
opening role conflict that left our guaranteed attacker routing stolen output
while opponents built their first sentinels. The permanent attacker must stay
on the direct core/sentinel lane; economy and dynamic builders retain
harvester hijack and logistics work.

## Evidence and hypothesis

The five v95 losses had 0--2 friendly sentinels by turns 3--64 while the
opponents had 2--8. The local current candidate's focused losses showed the
same pattern: median 4 harvesters/1 sentinel versus 8 harvesters/3 sentinels
in wins. Pivot winners opened with 4--8 builders, 7--16 harvesters, a small
gunner shell, and 3--6 barriers. The accepted hypothesis is that role
ownership, rather than another raid or price threshold, must protect the
first combat shell.

## Change

`bots/candidate/bot/attacker.py` no longer calls
`_try_hijack_enemy_harvester()` from `_run_attacker()`. Fixed attackers now
discover the core, plant verified forward sentinels, and siege directly;
defenders and dynamic workers still perform hijacks and raids. The focused
contract tests were updated to encode this ownership boundary and to require a
combat shell before a dynamic raid.

## Comparison and decision

The fresh current-candidate checkpoint was 172/210 over the full 21-map
matrix. The direct-siege branch scored 40/48 versus the same `bots/baseline`
pool and 174/210 over the full matrix, all command-clean. Its map changes were
Aurora 3->7, Bridge 7->9, and Showdown 7->10; String moved 7->6 and Vault
remained 5/10. It is a small but reproducible local improvement, not a claim
of live superiority.

The following structural variants were rejected against the actual 39/48
focused reference: defender-only opening shell 38/48, first-route assault
handoff 37/48, early gunner shell 36/48, compact-map workforce 37/48,
no-early-hijack 39/48, compact phase-budget workforce 40/48 (neutral), and
direct attacker symmetry sentinel 36/48. Their reports remain under
`reports/` and were not copied into the candidate.

## Validation

- Focused role/defense tests: 6/6 passed (`tests/test_candidate_nearest_defense.py`).
- Compileall and `git diff --check`: passed.
- `make smoke`: 4/4 command-clean, `reports/local-20260813T124257Z`.
- `make eval-regression`: 54/54 command-clean, 50/54 wins,
  `reports/local-20260813T124554Z`.
- Full release matrix: 210/210 command-clean, 174/210 wins,
  `reports/local-20260813T122504Z`.
- `make static`: exit 2 only because 15 inherited tests import deleted
  pre-v86 modules; candidate-focused tests and compile checks pass,
  `reports/static-20260813T1245-direct-siege.log`.

## Risks and next step

The gain is modest and String/Vault remain weak; full-matrix collection and
live ladder behavior are not proof of one another. Keep the accepted snapshot
as the local baseline for the next experiment, upload it only after the
release artifact is inspected, and retain the currently active platform
version as rollback until fresh live evidence exists.
