# v280 fixed-attacker replacement — rejected

- Parent/local comparator: immutable `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`.
- Replay basis: latest rated v107 match `5f60bd33-ec8d-4275-92bb-fafbbf24cd77`; active B lost Antler and Drumlin with no surviving forward Sentinel, while the opponents had four and twelve. The active side also ended those games with 5/7 Harvesters and 8/12 living Builders versus 7/11 and 4/5.
- Hypothesis: after confirmed death of a designated fixed attacker, the Core should grant that attacker slot one replacement spawn so the pressure lane cannot disappear after attrition.
- Temporary files: `bots/candidate/main.py`, `bots/candidate/bot/core_role.py`, and `tests/test_candidate_attacker_replacement.py`.
- Focused tests: **37/37** initial; compileall passed; `make static` retained the inherited exit 2 (obsolete deleted-module imports and two navigation fast-path assertions); smoke **4/4** command-clean.
- Seed-172 15-map screen: **8-7**, **50,470/48,290 Ti**, **118/114 Harvesters**, **49/50 Sentinels**, delivery **15/15 vs 15/15**, zero TLE/suspicious rows (`reports/local-20260819T140915Z`, analysis `reports/iter-v280-attacker-replacement/screen-172-analysis.json`).
- Rotated seed-175 15-map screen: **7-8**, **53,230/58,550 Ti**, **104/111 Harvesters**, **48/41 Sentinels**, delivery **15/15 vs 15/15**, zero TLE/suspicious rows (`reports/local-20260819T141116Z`, analysis `reports/iter-v280-attacker-replacement/screen-175-analysis.json`).
- Paired result: **15-15**, **103,700/110,840 Ti**, **222/225 Harvesters**, **97/91 Sentinels**, max p99/peak **1,429/3,809 us**. The extra replacement pressure did not translate into a repeatable win edge, so no repair or long gate was run.
- Decision: reject. Candidate source was restored recursively byte-identically to v0044 (`reports/iter-v280-attacker-replacement/rollback-source.diff` is zero lines). Rollback focused coverage **34/34**, compileall passed, static retained exit 2, and rollback smoke **4/4** (`reports/local-20260819T141333Z`). No promotion, package, upload, activation, or live transition occurred.
- Live state: v107 remains active-observing; v105 remains the user-requested rollback target. No platform state was changed by v280.
