# v289 opening takeover firewall — rejected

Date: 2026-08-19

## Objective and scope

Fresh v107 losses and the v288 protected-map screen showed a recurring small
opening workforce: our side often had one or zero Harvesters while the winner
already had a larger route shell.  The candidate had two enemy-Harvester
takeover entry points before own income was proven: Dynamic task selection and
the permanent Defender's direct seeded-route call.  v289 gated both behind one
completed own route plus a reserve for one Harvester and two Conveyors.  No
spawn, route FSM, attacker, turret, Store, or platform behavior was changed.

Temporary source/test scope was `bots/candidate/bot/dynamic.py`,
`bots/candidate/bot/defender.py`, and the focused additions in
`tests/test_candidate_nearest_defense.py`.

## Validation

- Initial focused coverage: **36/36**.
- Candidate compileall: pass.
- `make static`: inherited **exit 2** (15 obsolete-module imports and two
  navigation assertions).
- Initial `make smoke`: **4/4**, report `reports/local-20260819T161246Z`.
- First 15-map screen: `reports/local-20260819T161320Z`, analysis
  `reports/iter-v289-opening-takeover/screen-first-analysis.json`.
- First screen: command-clean, no TLE/suspicious rows, candidate-A **5-10**,
  collection **38,880/61,220 Ti**, Harvesters **98/133**, Sentinels **31/57**,
  max p99/peak **1,443/2,133 us**, and zero swapped pairs.
- An independent rerun already in flight was `reports/local-20260819T161437Z`,
  analysis `reports/iter-v289-opening-takeover/screen-analysis.json`; it was
  candidate-A **10-5**, collection **49,210/47,190 Ti**, Harvesters **114/109**,
  Sentinels **54/33**, max p99/peak **1,281/4,572 us**, and also had zero
  swapped pairs.  Neither one-sided probe was promotion evidence.
- Required 60-game gate: `reports/local-20260819T161657Z`, analysis
  `reports/iter-v289-opening-takeover/release-analysis.json`.
- Release gate: command-clean, zero TLE/suspicious rows, but **20-40**;
  collection **247,270/326,030 Ti**, Harvesters **476/487**, Sentinels
  **186/261**, Builders **542/561**, and one analyzer no-delivery row per
  side.  Max p99/peak was **1,497/4,681 us**.

## Decision and rollback

The one-sided quick screen was an outlier.  Both-side release evidence shows
the firewall suppresses too much useful pressure/takeover activity and does
not improve the opening economy.  Reject v289 without a repair or promotion.

The temporary gates and tests were removed.  Rollback focused coverage was
**34/34**, rollback compileall passed, rollback static retained exit 2, and
rollback smoke was **4/4** (`reports/local-20260819T162353Z`).  Recursive
candidate production-source parity with immutable
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f` is zero
diff at `reports/iter-v289-opening-takeover/rollback-source-parity.diff`.
No package, upload, activation, or live-state transition occurred.

v0044 remains the local baseline.  v107 remains active-observing and v105
remains the user-requested operational rollback target.
