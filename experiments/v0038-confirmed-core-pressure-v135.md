# v135 confirmed-Core pressure handoff

## Objective and scope

Test a structural economy-to-pressure handoff for dynamic Builders. The v0038
loss replay cluster showed healthy conveyor counts but too few forward
Sentinels/defensive structures, while `_should_harvest` continued to return
`TASK_HARVEST` whenever any visible ore existed. After three completed routes,
a confirmed enemy Core, and enough bank for the Sentinel/raid reserve, the
candidate temporarily handed dynamic workers to the normal raid/advance path;
the permanent Defender remained the economy floor. Repair 1 added one full
Harvester cost to that pressure reserve. No map branch, Store schema,
navigation, Launcher/Sentinel primitive, baseline source, package, upload, or
activation change was included.

Allowed source/test files were `bots/candidate/bot/dynamic.py` and
`tests/test_candidate_nearest_defense.py`; this record and checkpoint metadata
were the only other changes.

## Evidence

- Initial focused tests exposed a mixin-probe initialization defect; replacing
  direct `self.enemy_core_known` access with `getattr` fixed it. Corrected
  focused suite: 27/27; compileall passed; smoke 4/4; static retained the
  inherited 15 obsolete imports plus two navigation assertions.
- Initial 54-game screen: **29-25**, candidate 212,640 versus comparator
  221,450 Ti (0.9602x), two candidate no-delivery rows, zero command/TLE/
  suspicious-output failures, max p99 1,420 us and peak 4,734 us. Ragnarok
  improved to 4-2, but the overall edge and collection regression were not a
  clear release signal. Report: `reports/local-20260817T123159Z`.
- Repair 1 added the next-Harvester reserve. Focused tests remained 27/27,
  compileall passed, smoke was 4/4, and static was unchanged. The screen fell
  to **25-29**, with no candidate no-delivery rows, candidate collection
  154,510 Ti, and Auroraveil at **0-6** while Ragnarok rose to **6-0**.
  Report: `reports/local-20260817T123913Z`.
- Rollback restored every candidate production file byte-for-byte to immutable
  v0038. Rollback focused tests: 25/25; compileall passed; smoke 4/4 at
  `reports/local-20260817T124500Z`.

## Decision

Reject v135 after its initial screen and one bounded repair. The phase handoff
is too aggressive on maps with delayed Core confirmation/long routes despite
the Ragnarok gain. v0038 remains the moving local baseline; no new package,
upload, activation, or live-state transition occurred.
