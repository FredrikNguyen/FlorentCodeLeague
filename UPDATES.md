# Florent Code League development and live updates

This file is the durable handoff between Codex sessions. It is append-only except for the **Current state** table, which automation may refresh.

## Current state

| Field | Value |
|---|---|
| Workflow phase | active_observing |
| Working candidate | `bots/candidate` |
| Current active platform version | 10 |
| Last known-good platform version | 2 |
| Previous active platform version | 8 |
| Last known-good live score | unknown |
| Current candidate live score | unknown |
| Last deployment | 2026-08-06T12:53:19Z |
| Last observation | 2026-08-06T13:14:35Z |
| Last decision | observation captured |

Machine-readable state: [`state/live_state.json`](state/live_state.json).

## Score definition

The primary live score is the mean fractional score over rated five-game series during a version's observation window:

```text
series score = our game wins / 5
live score   = mean(series score)
```

Also record rating delta and opponent-adjusted residual when available. Reliability failures override score and trigger immediate rollback.

## Append-only update log

<!-- Automation appends newest entries immediately below this comment. -->

### Platform v10 live performance review — 2026-08-06T13:15:30Z

- Fresh observation report reports/live-observe-20260806T131416Z confirms platform v10 remains active and ready. Team status is rating 1215.73, rank 51/103, and 3-7 over the last ten rated series.
- The first two v10-rated series are complete: 3-2 versus Leviathan (wins on atoll, heart, snowflake; losses on eider and fjordgate, with the fifth ending by core_destroyed) and 0-5 versus Albert And Einstein (saga, atoll, lighthouse, hive, antler; four losses ended by core_destroyed).
- This is 3-7 games across only two series: live performance is currently volatile/weak, but the sample is too small for rollback or promotion. v2 remains the rollback target and the local v0008 baseline is unchanged.


### Live observation captured — 2026-08-06T13:14:35Z

- Active version: 10
- Report: reports/live-observe-20260806T131416Z


### Reviewer-only final winner review and activation — 2026-08-06T12:55:14Z

- Unseen challengers v8 and v9 were downloaded/extracted under reports/reviewer-workflow-20260806T1202Z/ without unit, static, smoke, or other challenger test suites. Archive hashes are v8 `f639e177d4ef54d93e9f656f24c38f2284de6ee855eaaa462d2c8cf892aff0b7` and v9 `02f0c0ec8a01fa80caf17d1dc28d06a8d8f151978d35c9001e10059edc3b0e8b`. v8 was rejected before games in all 48 invocations because bot/builder.py contains a disallowed finally block (reports/local-20260806T124537Z). v9 completed its direct battle but lost to the retained baseline: 168,600 versus 174,450 collected titanium, ratio 0.9665, 18/48 wins, zero command failures/stderr/exception/TLE markers (reports/local-20260806T124555Z).
- The retained local v0008 winner remained best after all direct comparisons. Winner-only validation had make static 146/146 plus compileall, make smoke 4/4 (reports/local-20260806T122712Z), and the release matrix 210/210 command-clean (reports/local-20260806T122741Z): 953,940 versus 748,370 collected titanium against the immutable v0006 comparator, ratio 1.2747, 110/210 wins, 120/210 positive-or-equal rows, zero failures/stderr/exception/TLE markers, runner wall p99 6.2904 s/game (CPU p99 not exposed).
- Winner review found strong maps atoll, aurora, pinch, runestone, sprint, and vault, but material regressions on showdown (0/8,050), quarry (2,000/15,500), twins (20,050/42,300), and longship (25,750/27,250); route-count/first-delivery telemetry and controller CPU p99 remain unavailable.
- Package artifacts/submissions/v0008_reviewer-current-best_20260806-1209_3f2505d7.zip was uploaded through the guarded live operator as platform version 10 (SHA-256 8e15f02b880c1b0688d6d55d0f351a5ed9edc3029effa7113a2ceafc44eea52e) and activated. Previous active version 8 and known-good rollback version 2 are preserved; deployment report is reports/live-deploy-20260806T125258Z and state/live_state.json is active_observing.
- Post-activation observation reports/live-observe-20260806T125327Z confirms active version 10, ready status, team rating 1242.52, rank 48/103, recent record 4-6. No completed ladder series references version 10 yet; the available completed matches predate activation, so no live score is claimed.
- Status: REVIEW COMPLETE — v0008 retained as local baseline and activated as platform v10; continue reviewer-only live observation and keep v2 available for rollback.


### Live observation captured — 2026-08-06T12:53:44Z

- Active version: 10
- Report: reports/live-observe-20260806T125327Z


### Candidate activated — 2026-08-06T12:53:19Z

- Version: 10
- Previous/rollback: 2
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260806T125258Z


### Candidate uploaded — 2026-08-06T12:53:18Z

- Candidate: v0008-reviewer-current-best-20260806
- Version: 10
- Rollback target: 2
- Report: reports/live-deploy-20260806T125258Z


### Live state bootstrapped — 2026-08-06T12:52:48Z

- Active version: 8
- Report: reports/live-bootstrap-20260806T125229Z


### Live observation captured — 2026-08-06T12:25:25Z

- Active version: 6
- Report: reports/live-observe-20260806T122500Z

### Reviewer-only submission comparison workflow — 2026-08-06T12:25:25Z

- User directive: from this checkpoint onward, Codex acts only as a reviewer. Compare the current local bot first, then pull ready platform submissions not previously reviewed and pit each against the strongest retained baseline. Do not run unit, static, smoke, or other test suites on challenger submissions. Run winner-only validation and review after the comparison series; activate the winner and retain it as the future baseline when authorized.
- First comparison: current `bots/candidate` versus `bots/versions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7`, report `reports/local-20260806T120456Z`, candidate **203,670** versus comparator **179,210** collected titanium (ratio **1.1365**), **21/48** wins, zero command failures/stderr. The winner was snapshotted as `bots/versions/v0008_reviewer-current-best_20260806-1209_3f2505d7` and is now the configured local baseline.
- Previously unseen ready platform submissions downloaded without code tests: v4 (`02efe306be3d9209372d6c1ef3f28fdddb91250312f0c6f26999461a98d0797d`), v5 (`5e0ca6729f81efc340049455e4c04520d1513c81333c81540a8d36a117121b0f`), v6 (`a98c94fc0cbf0f5c748fe07557444b71f826d8df6fb12f29c0c59e0b577fe0df`), and v7 (`4a344705277eb61dad0b1f493c601b6a51bcc7de0978a36b4af4920525094011`). Archives and extraction directories are under `reports/reviewer-workflow-20260806T1202Z/`.
- Direct comparisons against the retained v0008 baseline: v4 **106,770/141,810 = 0.7529**, **18/48** wins (`reports/local-20260806T120935Z`); v5 **115,590/157,440 = 0.7342**, **15/48** wins (`reports/local-20260806T121407Z`); v6 **115,700/158,160 = 0.7315**, **15/48** wins (`reports/local-20260806T121917Z`). All completed with zero command failures/stderr; no challenger test suites were run.
- v7 was rejected at the battle harness boundary: all 48 invocations failed validation because `bot/builder.py` contains a disallowed `finally` block (`reports/local-20260806T122423Z`). It was not tested further.
- Live review snapshot: `reports/live-observe-20260806T122500Z`; the platform currently reports active official version **6**, rating **1279.89**, rank **46/103**, recent record **7–3** over the last ten series. The three newest completed series were **3–2**, **5–0**, and **0–5** (8/15 games); no live series has evaluated the new local v0008 winner yet.
- Status: **COMPARISON COMPLETE — v0008 RETAINED; WINNER-ONLY VALIDATION AND ACTIVATION PENDING**.


### Iteration 1 — Four-route economy expansion — passed 2026-08-06T11:17:04Z

- Objective/scope: remove the three-project ceiling, preserve route 0, authorize at most two secondary route projects after a fresh route-0 delivery heartbeat, and keep delayed Store assignment deterministic. Allowed files were `bots/candidate/bot/{comms,core,economy,builder,feature_flags}.py`, expansion/economy/communication/route/player tests, evaluation configs, and the current plan. Navigation, combat, turret, launcher, redundancy, snapshots, and platform operations were non-goals.
- Files changed in this checkpoint: `docs/CURRENT_PLAN.md`; candidate `comms.py`, `core.py`, `economy.py`, `builder.py`, `feature_flags.py`; `tests/test_candidate_comms.py`, `test_candidate_economy.py`, `test_candidate_economy_logistics.py`, `test_candidate_expansion.py`, `test_candidate_player.py`; and `configs/eval_regression.toml`, `eval_smoke.toml`, `eval_matrix.toml`.
- Behavior: Store schema 4 adds `PROJECT_3` at slot 13 and `CLAIM_3` at slot 15; project/claim codecs and ownership validation cover all four indices. Core protects route 0, counts delayed assignments toward the two-secondary limit, retains failed ore for a bounded cooldown, and computes 5/6/7 Builder demand for bootstrap/expansion/four-route maintenance. Builders retain their own project reservation at the four-project cap and release delayed ore collisions to the higher project index.
- Tests: focused economy/comms/route/player/expansion **63/63 passed**; `make static` **139/139 plus compileall**; `make smoke` **4/4 command-clean** (`reports/local-20260806T111646Z`); paired previous-iteration checkpoint **48/48 command-clean**, zero stderr/runtime failures (`reports/local-20260806T111704Z`). Full details: `reports/local-20260806T111704Z/iteration1-summary.md`.
- Metrics against the immutable workspace Iteration 7 comparator `bots/versions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7`: candidate **230,970** versus comparator **188,320** collected titanium (ratio **1.2265**), candidate wins **27/48**, collection-positive **27/48**. Runner wall-clock p99 was **4.621 s/game**; controller CPU p99 is not exposed by the local runner. All games completed normally under the 10 ms turn limit.
- Remaining risks: route-count and first-delivery telemetry are not emitted by the runner; map-level collection variance remains; active platform version was not changed. Iteration 2 work-intent/idling changes have not started.
- Iteration status: **ITERATION 1 PASSED — READY FOR ITERATION 2**.

### Remote gate result — 2026-08-06T10:20:30Z

- Match `51a5362b-28b0-4b03-a198-fbb6df4ec73c` completed unrated **2–3** against the immutable v0005 comparator. The candidate won `crossfire` and `vault`; the comparator won `sprint`, `bridge`, and `aurora`.
- All five games reached 1,000 turns and ended by `titanium_collected`; no resignation, exception, TLE, or platform error was reported. Evidence summary: `reports/remote-20260806T095713Z/result.md`.
- This remote result does not alter the already active version 3; automatic rollback remains guarded by the configured live observation policy.

### Final release and activation — 2026-08-06T10:19:39Z

- Final review repair: corrected direct offensive-target scoring so callers can apply the stale-target TTL; the focused suite, static/compileall, smoke, selected 48-game regression, and the full release matrix were rerun afterward and remained clean.
- Final evidence: focused/static **135/135** plus compileall; final smoke **4/4** (`reports/local-20260806T102140Z`); selected previous-iteration regression **48/48** (`reports/local-20260806T100021Z`); release matrix **210/210** (`reports/local-20260806T100335Z`). Candidate collection was **856,350** versus **778,320** comparator (ratio **1.1003**), with **125/210** wins and zero command failures/stderr/exception/TLE markers.
- Package: [`v0006_iter7-integrated-20260806_20260806-1018_3f2505d7.zip`](artifacts/submissions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7.zip), SHA-256 `2c119f48ec23880cd0a11b0747f03995c180ca8c3228096efdb55e9e4e5141bb`; manifest records 18 files and 45,536 archive bytes.
- Platform action authorized by the user: bootstrapped ready active version **2** as rollback target, uploaded candidate `v0006-iter7-integrated-20260806`, received ready version **3**, and activated it. Deployment evidence: `reports/live-deploy-20260806T101840Z`; current state: `state/live_state.json` is `active_observing`, active **3**, rollback **2**.
- Post-activation verification: observation captured active version 3 at `reports/live-observe-20260806T101924Z`; no live score is claimed yet because the observation window has not produced rated series.
- Remaining risks: map-level local variance (bridge/showdown/vase), remote gate match `51a5362b-28b0-4b03-a198-fbb6df4ec73c` remains queued, and live score/reliability evidence is pending the configured observation window. Automatic rollback remains enabled with version 2 as the known-good target.
- Release status: **ACTIVATED — OBSERVING**.

### Live observation captured — 2026-08-06T10:19:39Z

- Active version: 3
- Report: reports/live-observe-20260806T101924Z


### Candidate activated — 2026-08-06T10:18:55Z

- Version: 3
- Previous/rollback: 2
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260806T101840Z


### Candidate uploaded — 2026-08-06T10:18:55Z

- Candidate: v0006-iter7-integrated-20260806
- Version: 3
- Rollback target: 2
- Report: reports/live-deploy-20260806T101840Z


### Live state bootstrapped — 2026-08-06T10:18:21Z

- Active version: 2
- Report: reports/live-bootstrap-20260806T101807Z


### Live state bootstrapped — 2026-08-06T10:18:14Z

- Active version: 2
- Report: reports/live-bootstrap-20260806T101800Z


### Live state bootstrapped — 2026-08-06T10:17:27Z

- Active version: None
- Report: reports/live-bootstrap-20260806T101711Z


### Release gate — Iterations 4–7 complete; Iteration 3 user-authorized skip — 2026-08-06T09:58:31Z

- Scope/status: Iteration 3 was explicitly skipped by the user after the current plan classified 3R route reliability as passed. Iterations 4 (controlled multi-route economy), 5 (reactive defense), 6 (bounded offensive primitives), and 7 (integrated phase strategy) were implemented sequentially. Each iteration kept its documented non-goals and was validated before the next started.
- Files changed: `bots/candidate/bot/{builder,comms,core,defense,economy,feature_flags,navigation,offense,policy,turrets,types,world}.py`; focused tests for economy, expansion, defense, offense, route FSM, comms, policy, player, and static contracts; evaluation configs; `docs/CURRENT_PLAN.md`, `docs/NEXT_ITERATIONS_PLAN_UPDATED.md`, `docs/START_HERE.md`; `state/project_state.json` and this checkpoint log.
- Validation: focused/static suite **135/135** plus compileall passed; final smoke **4/4** command-clean (`reports/local-20260806T095636Z`); selected paired previous-iteration regression **48/48** command-clean with no stderr or exception/TLE markers (`reports/local-20260806T093757Z`); release matrix **210/210** command-clean with zero failures (`reports/local-20260806T094203Z`).
- Release metrics against immutable previous-best comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: candidate collected **856,350** versus **778,320** comparator titanium (ratio **1.1003**), candidate won **125/210** games and exceeded comparator collection on **125/210** rows. All games ended by the normal `titanium_collected` condition; no stderr, exception, or TLE markers were observed.
- Remote gate: the sandbox attempt failed DNS without changing platform state (`reports/remote-20260806T095701Z`); the authorized network retry succeeded in submitting remote test `51a5362b-28b0-4b03-a198-fbb6df4ec73c` (`reports/remote-20260806T095713Z`), currently queued when recorded.
- Remaining risks: several individual maps remain below the comparator (notably bridge, showdown, and vase), the remote test result is still queued, and live activation/observation remains pending rollback bootstrap. These are recorded before deployment; no claim of live success is made here.
- Iteration status: **RELEASE_READY_PENDING_LIVE_BOOTSTRAP**.

### NEXT Iteration 7 integrated phase strategy — passed 2026-08-06T09:57:00Z

- Objective/scope: integrate economy readiness, reactive defense overlays, offensive preparation/pressure, stable role allocation, and endgame spending guards. Allowed files were the strategy/policy/core/builder/comms/defense/offense/turret surfaces plus focused tests and feature flags. Navigation algorithms, Store schema, map-specific policy, and launcher activation were non-goals.
- Done criteria: deterministic phase transitions, persistent defenders, project-owner precedence, no early offensive spending, stale-target retreat, and launcher/feature isolation all passed in focused tests; selected previous-iteration regression remained command-clean and aggregate-positive.
- Files/tests: `bots/candidate/bot/policy.py`, `core.py`, `builder.py`, `comms.py`, `feature_flags.py`, `tests/test_candidate_world_policy.py`, `tests/test_candidate_comms.py`, `tests/test_candidate_route_fsm.py`, `tests/test_candidate_player.py`; focused/static/smoke and release-matrix evidence is recorded in the release-gate entry above.
- Metrics: selected 8-map/3-seed paired regression **48/48**, candidate **203,080** vs comparator **201,340** (ratio **1.0086**, all rows positive); full release matrix **210/210** command-clean.
- Remaining risks/status: map-level variance remains; Iteration 7 **PASSED** and release gate is ready once live rollback state is bootstrapped.

### NEXT Iteration 6 offensive primitives — passed 2026-08-06T09:56:00Z

- Objective/scope: add legal, bounded target selection, builder attacks only against enemy buildings, verified enemy-core publication, safe attack stances, forward-turret support, retreat/regroup guards, and late-game spending suppression. Defense construction, launcher enablement, and unrestricted early raids were non-goals.
- Done criteria: target hierarchy/core override, legality gates, forward support, stale-target retreat, and endgame suppression were covered by focused tests; the phase-enabled regression prevented early offensive spending.
- Files/tests: `bots/candidate/bot/offense.py`, offense sections of `builder.py`/`comms.py`, `tests/test_candidate_offense_endgame.py`, plus feature-flag and player regression coverage. Focused suite **135/135**, static/compileall, smoke, selected regression, and full matrix passed.
- Remaining risks/status: offensive pressure is intentionally gated behind stable economy and fresh verified targets; Iteration 6 **PASSED**.

### NEXT Iteration 5 reactive defense — passed 2026-08-06T09:55:00Z

- Objective/scope: implement threat reports with freshness, defense hysteresis, stable defender assignment, protected-asset fire priority, positive-gain Gunner rotation, and bounded ammo conversion. Economy route construction and offensive/launcher activation were non-goals.
- Done criteria: fresh core damage reaches critical mode, stale reports recover, defender choices remain stable, zero-value rotations spend nothing, and reserves survive all defense decisions.
- Files/tests: `bots/candidate/bot/{types,comms,defense,turrets,core}.py`, `tests/test_candidate_defense.py`, and related player/core combat tests. Focused suite **135/135**, static/compileall, smoke, selected regression, and full matrix passed.
- Remaining risks/status: defense is reactive and reserve-capped; Iteration 5 **PASSED**.

### NEXT Iteration 4 controlled multi-route economy — passed 2026-08-06T09:54:00Z

- Objective/scope: extend the proven first route to sequential profitable expansion with project-local FSM/heartbeats, payback and liquidity guards, deterministic ore ranking, and productive-idle behavior. Combat, defense construction, offensive behavior, launchers, and navigation algorithm changes were non-goals.
- Done criteria: first-route health always precedes secondary assignment, one project builds at a time, failed routes replan without invalidating healthy routes, and economic reserves remain bounded.
- Files/tests: `bots/candidate/bot/{economy,core,builder,comms,types,feature_flags}.py`, `tests/test_candidate_economy.py`, `tests/test_candidate_expansion.py`, `tests/test_candidate_route_fsm.py`, and static budget contract. Focused suite **135/135**, static/compileall, smoke, selected regression, and full matrix passed.
- Metrics: selected paired regression **48/48** command-clean and aggregate-positive versus the previous iteration comparator; full release matrix later confirmed **856,350 / 778,320 = 1.1003** aggregate collection.
- Remaining risks/status: per-map output variance is retained for release review; Iteration 4 **PASSED**.

### NEXT Iteration 3R comparator-scaling diagnosis — blocked 2026-08-06T00:16:11Z

- Objective/scope: restate the post-repair6 divergence, compare one seed-1 A-side trace for each selected map, and apply at most one evidence-scoped first-route Builder/logistics/navigation/world repair. Allowed files were that first-route surface, focused tests, and checkpoint metadata. Iteration 4, secondary expansion, combat, Store changes, and comparator replacement were non-goals. The done criteria were deterministic classification, focused/static/smoke/exact-regression validation, and every 3R promotion gate.
- Files changed: no production bot or test source changed in this diagnosis. Added the offline diagnosis summary `reports/route-iteration3r-diagnosis-20260806T0009/summary.md`; checkpoint logs/config are under `reports/route-iteration3r-repair7-20260806T0013/`. Temporary trace copies were removed; trace artifacts remain under the diagnosis report.
- Differential evidence: the candidate built one own Harvester and reached first delivery/`MAINTAIN` on all five sampled maps (`sprint` 16, `string` 12, `bridge` 24, `vault` 12, `aurora` 16). The frozen comparator built 3, 2, 2, 2, and 2 own Harvesters respectively. Candidate collections were 2,470/2,480/2,450/2,480/2,470 versus comparator 7,410/4,910/4,800/4,960/2,660. The candidate's secondary-expansion gate is explicitly false and claim slots other than 0 are rejected.
- Tests/results: focused **72/72** (`focused.log`); `make static` **118/118** plus compileall (`static.log`); `make smoke` **4/4**, report `reports/local-20260806T001359Z` (`smoke.log`); exact selected regression **36/36**, report `reports/local-20260806T001611Z` (`regression.log`), zero nonzero returns/stderr and no exception/TLE output markers. The unrelated default `make eval-regression` attempt (9 maps, seeds 1/19/101) completed 54/54 and is preserved in `regression-default-9map.log` with report `reports/local-20260806T001417Z`.
- Metrics versus immutable comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: candidate collection **88,950** versus **170,960** (52.0297%, below the required 90% / 153,864); candidate mean **2,470.8** versus comparator **4,748.9**; proxy **36/36** positive; candidate wins **3/36**. A one-Harvester upper bound is 90,000 Ti (`2.5 * 1000 * 36`), so the measured candidate is near the isolation ceiling. Route churn remains unmeasured.
- Decision/risk: no admissible repair exists within Iteration 3's explicit “do not add a second Harvester” rule that can satisfy the aggregate gate against this multi-route comparator. Enabling secondary expansion would violate the plan; changing the frozen comparator would invalidate the baseline. The comparator-scaling conflict is deterministic and recorded in `reports/route-iteration3r-diagnosis-20260806T0009/summary.md`.
- Review/status: `git diff --check` and complete-diff self-review are required at checkpoint. Iteration 3R remains **BLOCKED**; do not start Iteration 4 until the plan/baseline conflict receives an explicitly scoped decision.

### NEXT Iteration 3R ore-occupancy checkpoint — blocked 2026-08-06T00:02:28Z

- Objective/scope: trace the live bridge adjacent/build transition and apply one bounded repair only. The first divergence was a non-target Builder following the unreachable `(0,0)` waypoint onto the selected ore tile; the route Builder then could not build the Harvester. The repair skips known ore tiles during non-target movement. No economy policy, Store, combat, expansion, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/builder.py` and `tests/test_candidate_route_fsm.py`; pre-edit traces and replays are under `reports/route-iteration3r-diagnosis-20260805T2354/`, checkpoint logs under `reports/route-iteration3r-repair6-20260805T2354/`.
- Tests/results: focused 72/72; `make static` 118/118 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260806T000101Z`. Regression report: `reports/local-20260806T000228Z`.
- Metrics versus the immutable Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: proxy improved to 36/36 (100%), bridge improved to 6/6, candidate wins 3/36, and collection improved to 88,950 total / 2,470.8 mean versus comparator 170,960 total / 4,748.9 mean (52.0% aggregate, below 90%). Full 21-map matrix was not run.
- Differential evidence: the repair removes the persistent bridge ore blocker and produces a Harvester on both sides, but the remaining aggregate throughput/output gap is unresolved. Summary: `reports/route-iteration3r-repair6-20260805T2354/summary.md`.
- Remaining risk/next plan: route churn remains unmeasured; classify post-delivery output, acknowledgement, repair, or multi-route divergence before another edit. Plan: `reports/route-iteration3r-repair6-20260805T2354/next-diagnosis-plan.md`.
- Review/status: Iteration 3R is **BLOCKED** because the comparator aggregate gate failed despite proxy/bridge recovery. Stop here and do not start Iteration 4.

### NEXT Iteration 3R adjacent-stance checkpoint — blocked 2026-08-05T23:43:00Z

- Objective/scope: reproduce the adjacent-stance oscillation and apply one bounded navigation repair only. A fake one-cell scenario showed an empty adjacent-goal set caused `Navigator._fallback()` to raise and adjacent movement to enter arbitrary fallback. No economy, Store, combat, expansion, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/navigation.py`, `bots/candidate/bot/builder.py`, and `tests/test_candidate_builder_navigation.py`; logs and reports are under `reports/route-iteration3r-repair5-20260805T2343/`.
- Tests/results: focused 71/71; `make static` 117/117 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260805T234438Z`. Regression report: `reports/local-20260805T234458Z`.
- Metrics versus the latest passed Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: collection/first-delivery proxy remained 30/36 (83.3%), candidate wins 0/36, candidate collection 74,310 total / 2,064.2 mean versus comparator 191,360 total / 5,315.6 mean (38.8% aggregate), and `bridge` remained 0/6. No row-level improvement; full 21-map matrix was not run.
- Differential evidence: the synthetic no-goal adjacent case now waits for two turns and moves when the Builder leaves, but the live bridge category is unchanged. The next diagnosis must capture nonempty-goal path rejection, cooldown, or another occupancy conflict before further editing. Summary: `reports/route-iteration3r-repair5-20260805T2343/summary.md`.
- Remaining risk/next plan: `reports/route-iteration3r-repair5-20260805T2343/next-diagnosis-plan.md`; route churn remains unproven by the replay harness.
- Review/status: `git diff --check` passed and no diagnostic markers remain; Iteration 3R is **BLOCKED** because the promotion gate failed after this repair. Stop here and do not start Iteration 4.


### NEXT Iteration 3R post-repair navigation checkpoint — blocked 2026-08-05T23:36:00Z

- Objective/scope: trace the first post-repair `bridge` divergence and apply one bounded navigation/layout repair only. The trace showed completed Conveyor routes followed by adjacent-stance oscillation when a friendly Builder occupied a passable route cell. No Core spawning, Store, combat, expansion, advanced spending, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/world.py` and `tests/test_candidate_world_policy.py`; diagnostic traces and checkpoint reports are under `reports/route-iteration3r-diagnosis-20260806T0000/` and `reports/route-iteration3r-repair4-20260805T2336/`.
- Tests/results: focused 70/70; `make static` 116/116 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260805T233655Z`. Regression report: `reports/local-20260805T233713Z`.
- Metrics versus the latest passed Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: collection/first-delivery proxy remained 30/36 (83.3%), candidate wins 0/36, candidate collection 74,310 total / 2,064.2 mean versus comparator 191,360 total / 5,315.6 mean (38.8% aggregate), and `bridge` remained 0/6. No row-level improvement; full 21-map matrix was not run.
- Differential evidence: candidate Builder 3/4 completed the five-cell route but never built the Harvester; a friendly Builder occupied the final Conveyor/stance cell and the adjacent Navigator oscillated. The comparator delivered around rounds 12–16. Trace summary: `reports/route-iteration3r-repair4-20260805T2336/summary.md`.
- Remaining risk/next plan: the cell is now classified as navigation-blocked while remaining route-layout-passable, but the FSM still needs a bounded wait/alternative-stanza diagnosis. Next plan: `reports/route-iteration3r-repair4-20260805T2336/next-diagnosis-plan.md`.
- Review/status: `git diff --check` passed; temporary diagnostic copies were removed; Iteration 3R is **BLOCKED** because the promotion gate failed after this repair. Stop here and do not start Iteration 4.


### NEXT Iteration 3R newly scoped repair checkpoint — blocked 2026-08-05T23:23:00Z

- Objective/scope: diagnose the remaining `bridge` route divergence. One bounded repair was allowed in the Builder route planner/build FSM: ignore friendly transient Builder occupancy during static layout search, wait for a friendly Builder to clear the next build cell, and retain bounded replan/failure handling. No Core spawning, Store, combat, expansion, advanced spending, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/builder.py` and `tests/test_candidate_route_fsm.py`; logs and checkpoint reports are under `reports/route-iteration3r-repair3-20260805T2323/`.
- Tests/results: focused 69/69; `make static` 115/115 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260805T232347Z`. Regression report: `reports/local-20260805T232406Z`.
- Metrics versus the latest passed Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: collection/first-delivery proxy remained 30/36 (83.3%), candidate wins 0/36, candidate collection 74,310 total / 2,064.2 mean versus comparator 191,360 total / 5,315.6 mean (38.8% aggregate), and `bridge` remained 0/6. No row-level improvement; full 21-map matrix was not run.
- Differential evidence: deterministic fake-controller coverage proves static route stability and temporary wait/recovery with two friendly Builders in a one-cell corridor, but the live `bridge` category did not improve. The next diagnosis must trace whether the first blocked build cell is a Builder-FSM deadlock or a separate earlier divergence; report: `reports/route-iteration3r-repair3-20260805T2323/summary.md`.
- Remaining risk/next plan: `reports/route-iteration3r-repair3-20260805T2323/next-diagnosis-plan.md`. Route churn remains unproven by the exact replay harness.
- Review/status: `git diff --check` passed; diagnostic markers were removed from submitted source; Iteration 3R is **BLOCKED** because the promotion gate failed after this repair. Stop here and do not start Iteration 4.


### NEXT Iteration 3R bounded repair checkpoint — blocked 2026-08-05T23:10:00Z

- Objective/scope: diagnose the earliest route divergence and repair only the first-route Builder/economy path. Two bounded repairs were applied: ignore the current Builder's own tile during route planning, and move scouts to deterministic waypoints instead of parking on known ore. No Core spawning, Store, combat, second Harvester, advanced spending, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/builder.py` and `tests/test_candidate_route_fsm.py`; diagnostic traces and checkpoint reports are under `reports/route-iteration3r-diagnosis-20260806T0100/` and `reports/route-iteration3r-repair2-20260805T2310/`.
- Tests/results: focused 68/68; `make static` 114/114 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr. Smoke report: `reports/local-20260805T230907Z`. Regression report: `reports/local-20260805T230927Z`.
- Metrics: collection/first-delivery proxy improved from 12/36 to 30/36 (83.3%), still below 34/36; candidate wins 0/36; candidate mean collection 2,064.2 versus 5,315.6 for the current paired Iteration 2 comparator (38.8% aggregate, below 90%); `bridge` remained 0/6. No comparator row improved. All isolation flags remain false; full 21-map matrix was not run.
- Differential evidence: self-Builder occupancy was the first `string` divergence; scout occupancy of the ore tile caused the next `vault`/`string` Harvester-build denial; after both repairs, `bridge` still fails because transient Builder occupancy makes route search return no route even though the static-layout probe succeeds. Trace rows and classifications are in `reports/route-iteration3r-repair2-20260805T2310/summary.md`.
- Remaining risk/next plan: transient Builder occupancy must be separated from static route-layout planning while retaining bounded enemy/permanent-obstacle handling. New diagnosis plan: `reports/route-iteration3r-repair2-20260805T2310/next-diagnosis-plan.md`.
- Review/status: focused/static/smoke/regression logs are preserved, `git diff --check` passed at checkpoint, and Iteration 3R is **BLOCKED after two bounded repairs**. Do not start Iteration 4.


### NEXT Iteration 3 bounded repair audit — blocked 2026-08-05T22:31:09Z

- Objective/scope remained the single verified Harvester-to-Core route. Two bounded repairs were applied only in the allowed route/economy/test surface: fresh project heartbeats keep an active claim alive, and occupied Builder-bot tiles are route obstacles. No Core spawning, combat, second Harvester, advanced spending, or Iteration 4 work was added.
- Tests/results: focused 43/43; `make static` 112/112 plus compileall; `make smoke` 4/4; selected regression 36/36 command-clean with zero stderr. Logs and return codes are under `reports/route-iteration3-repair2-20260805T2230/`.
- Reports/replays: smoke `reports/local-20260805T223109Z`; regression `reports/local-20260805T223130Z`; summary `reports/route-iteration3-repair2-20260805T2230/summary.md`.
- Metrics: first-delivery/collection proxy remained 12/36 (33.3%); candidate wins 0/36; mean collected titanium 824.2 versus 4,778.1 for the current-best Iteration 2 snapshot; no row-level improvement. All five isolation flags remain false; full 21-map matrix was not run.
- Review/status: `git diff --check` passed and the complete diff was self-reviewed. Both resumed-audit repair attempts passed their focused tests but failed to improve the promotion metric. Iteration 3 remains **BLOCKED**; do not start Iteration 4 without a newly scoped diagnosis/plan.


### NEXT Iteration 3 first-route checkpoint — blocked 2026-08-05T22:15:15Z

- Objective/scope: implement only the first Harvester-to-Core route FSM, route-local delivery acknowledgement, bounded repair, and explicit advanced-feature isolation. No second Harvester, combat targeting, defense, launchers, raids, or Iteration 4 work was started.
- Files changed: `bots/candidate/bot/builder.py`, `bots/candidate/bot/feature_flags.py`, `tests/test_candidate_route_fsm.py`, `tests/test_candidate_player.py`, baseline-policy configs, immutable comparator snapshot `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`, and durable state/report metadata.
- Tests/results: focused 41/41; `make static` 110/110 plus compileall; `make smoke` 4/4 against the current-best snapshot; selected regression 36/36 command-clean with zero stderr. Smoke report: `reports/local-20260805T221515Z`. Regression report: `reports/local-20260805T221103Z`.
- Metrics: first-delivery/collection proxy 12/36 (33.3%) versus the required 95%; candidate mean collected titanium 825.8 versus 4,778.1 for the previous-best snapshot, with no candidate win or row-level collection improvement. All five advanced flags remain false. Full 21-map matrix was not run.
- Review/blocker: `git diff --check` passed. A deterministic trace shows the builder releases its active route when assignment generation reaches age 32 even though the project heartbeat is current; this happens before final-link verification and Harvester construction. Two bounded repairs (scouting progression and verification fallback) did not clear the gate, so no further repair or next iteration was started.
- Baseline policy: regression/smoke/matrix configs now point to the latest passed Iteration 2 snapshot; a future passed iteration must replace that snapshot/config baseline before its successor is evaluated.
- Reports: `reports/route-iteration3-20260805T2200/summary.md`, `previous-best-regression.txt`, `current-best-smoke.txt`, focused/static/smoke/regression logs; comparator source manifest digest `c39eefc81e84539a44a929810dac8726f95863767f20d6ef5e9282fb58860ecc`.
- Iteration status: **BLOCKED**; resume Iteration 3 only with the bounded claim/project-heartbeat freshness repair, then re-run all gates before considering Iteration 4.


### NEXT Iteration 2 Store protocol checkpoint — 2026-08-05T21:40:28Z

- Files changed: bots/candidate/bot/types.py, comms.py, core.py, builder.py, tests/test_candidate_comms.py, tests/test_candidate_player.py, plus durable state/report metadata.
- Tests/results: focused Store/Core/player suite 41/41 passed; make static 98/98 plus compileall passed; make smoke 4/4; regression 24/24 command-clean with zero stderr.
- Reports: reports/store-iteration2-20260805T2140/summary.md, focused.log, static.log, static.rc, smoke-summary.txt, regression-summary.txt; regression metadata/replays at reports/local-20260805T213612Z.
- Metrics: schema version 3; all 30x30 coordinates round-tripped; delayed assignment/project writes covered; active project cap remained 3; no duplicate ownership observed; candidate stayed at 1,800 production lines.
- Remaining risks: full 21-map matrix deferred; first-delivery reliability and Iterations 3-5 remain unimplemented; no platform operation performed.
- Iteration status: PASSED; proceed to the separately scoped Iteration 3 checkpoint.


### NEXT Iterations Plan Iteration 1 validation — 2026-08-05T21:11:47Z

- Objective: validate adjacent legal stances, active per-unit path reuse, bounded deterministic replanning, navigation/layout epoch separation, and non-consuming destroy semantics. No source edits were made; the existing CURRENT_PLAN implementation remains a separate v0004 checkpoint.
- Allowed surface reviewed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, and focused navigation/action tests. Non-goals remained Store layout, economy thresholds, role assignment, combat priorities, and Core budget policy.
- Tests: focused Iteration 1 suite 34/34; make static 97/97 plus compileall; make smoke 4/4 command-clean; required regression subset 24/24 command-clean with no stderr.
- Reports: reports/iteration1-validation-20260805T2120/summary.md, focused.log, static.log, smoke.log, regression-summary.txt, complete v0003-to-candidate.diff, and v0004-to-candidate.diff; local regression report reports/local-20260805T210935Z and smoke report reports/local-20260805T210923Z.
- Metrics: active-path tests cover one BFS/replan followed by cache hits, epoch/goal invalidation, blocked-step retry, adjacent-target exclusion, CPU cutoff, and oscillation fallback; no exception, TLE, or command-failure indicators.
- Self-review: source comparison against v0004 is identical apart from generated __pycache__ bytecode; no defects were found and no repair was needed. Full 21-map matrix remains deferred to the release gate.
- Iteration status: PASSED; Iteration 2 is now the next implementation checkpoint.


### NEXT Iterations Plan Iteration 0 reconciliation — 2026-08-05T21:08:46Z

- Files changed: .codex/config.toml; .codex/agents/sol-planner.toml; .codex/agents/luna-implementer.toml; .codex/agents/sol-reviewer.toml; AGENTS.md; scripts/codex_task.py; Makefile; generated artifacts/chatgpt planning packets; report/state metadata. No candidate behavior changes were made in this iteration.
- Source/archive evidence: v0003 archive SHA-256 fd757d1c6ff72c8e5e45bad37b6201700c599f9aa83caeeadf7d22b21adb6608; immutable v0003 snapshot retained; intentional current-plan delta is separately packaged as v0004_navigation-iteration1 SHA-256 59e579333548bd8e41dfe1f13f78900138a09192476ca20cc67d057e85051c56.
- Tests: harness/startup focused tests 16/16; make static 97/97 plus compileall; make smoke 4/4; Iteration 0 regression 20/20 command-clean; make handoff passed.
- Reports and packets: reports/reconcile-iteration0-20260805T/summary.md, source-hashes.txt, static.log, smoke.log, regression artifacts under reports/local-20260805T210359Z, and artifacts/chatgpt/PLANNING_PACKET.md plus RELEASE_REVIEW_PACKET.md.
- Metrics: zero command failures, exceptions, or TLE indicators in smoke/regression; packet source matches the candidate; v0003 remains recoverable; no additional strategy/economy/navigation changes mixed into this checkpoint.
- Remaining risks: Iteration 1 in the external plan duplicates the already-completed current-plan navigation checkpoint, so it must be validated as a separate no-op checkpoint before Iteration 2; no full 21-map matrix was run.
- Iteration status: PASSED; proceed only to the separate Iteration 1 validation checkpoint.


### Current-plan navigation checkpoint — 2026-08-05T21:00:41Z

- Status: behavior checkpoint passed; next-plan iterations are paused because make static exits 2 on pre-existing harness/startup failures outside the approved scope.
- Files changed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, tests/test_candidate_navigation.py, tests/test_candidate_actions.py, tests/test_candidate_builder_navigation.py.
- Focused tests: 34/34 passed; compileall passed. Full logs: reports/navigation-20260805T2110/focused.log and compileall.log.
- make static: exit 2; candidate/static-contract checks passed, with 4 harness failures and 3 missing-agent errors. Full log: reports/navigation-20260805T2110/make-static.log.
- make smoke: 4/4 games, zero command failures; report: reports/local-20260805T205901Z.
- Regression subset: 24/24 games, zero command failures/stderr; report: reports/local-20260805T205908Z.
- Metrics: active path one BFS and two cache hits over a three-step route; goal/epoch/blocked-step invalidations replan once; candidate production count is 1,800 lines.
- Behavior unchanged deliberately: Store/economy/budget/roles/defense/offense/opening policy. Remaining risk: static harness state must be repaired before NEXT_ITERATIONS_PLAN Iteration 0 can start.
- Report: reports/navigation-20260805T2110/summary.md


### Live battle observation — 2026-08-05T19:31:39Z

- Platform reports submission `v0003-entrypoint-class-2de8371f` as numeric version `1`, `ready`, and active for Kleos.
- Eight rated ladder series are complete: one win and seven losses. The newest series beat Git Glam 3–2 (+4.041 Elo), raising the rating to `1402.3331784619274` and placing Kleos at rank `39/102`.
- The newest series reached the 1000-turn titanium-collection limit on all five maps: wins on `crossfire`, `sweden`, and `skerry`; losses on `twins` and `runestone`. No match error or resignation was reported.
- Previous Powerpuff Girls 0–5 ended by `core_destroyed` on all five maps after 266–317 turns; no platform/runtime error was reported.
- Replay-level comparison: the Git Glam series first produced HP events at turns 325–766 and no core destruction; the Powerpuff series first produced HP events at turns 12–87 and destroyed the Kleos core in every game. The current weakness is collection/economy on `twins` and `runestone`, not a submission/runtime failure.
- Battle descriptions from the decoded replay streams:
  - Git Glam `crossfire`: Kleos stayed at 4 builders, 2 harvesters, and 4 conveyors while Git Glam expanded to 13 builders, 4 harvesters, 13 conveyors, and a full turret mix; no core damage, Kleos won the 1000-turn collection finish.
  - Git Glam `sweden`: first HP event at turn 458; Kleos reached 5 builders, 2 harvesters, and 13 conveyors, with sustained turret/resource activity and no core damage; Kleos won by collection.
  - Git Glam `twins`: first HP event at turn 454; Kleos stayed at 4 builders, 1 harvester, and 4 conveyors while Git Glam grew to 27 builders, 5 harvesters, 20 conveyors, and heavy defense; Git Glam won collection without destroying the core.
  - Git Glam `runestone`: first HP event at turn 622; Kleos recorded 85 conveyor placements and 70 later removals, indicating route churn or repair activity; Git Glam’s larger 28-builder/42-conveyor footprint won collection.
  - Git Glam `skerry`: first HP event at turn 766; Kleos finished with 4 builders, 3 harvesters, and 6 conveyors, survived without core damage, and won collection.
  - Powerpuff `duel`, `sweden`, `longship`, `hive`, and `quarry`: first HP events came at turns 12, 87, 29, 37, and 48 respectively; Powerpuff scaled substantial gunner/harvester/conveyor forces and destroyed the Kleos core at turns 273, 285, 271, 266, and 317.
- Full notes and per-map descriptions: `reports/live-battles-20260805T193139Z.md`; raw capture: `reports/live-latest-battles-20260805T193139Z/`; newest replays: `replays/live-c17b2501-20260805/`.

### Codex cap-replan fix — 2026-08-05T17:37:04Z

- Fixed blocked-route replanning for a Builder that already owns one of the three shared project reservations: admission now counts only other projects while preserving the owner's reservation, so it cannot deadlock at the cap or create a fourth project.
- Added Player.run coverage for reserved replanning at the shared cap and strengthened the unreserved fourth-project rejection test.
- Validation: independent Sol review `APPROVED`; focused unit suite 33/33; smoke 4/4; regression 54/54; full matrix 210/210 command-clean, 205/210 wins versus 165/210 prior, with bridge and string 10/10 and no non-target map regression; benchmark p99 6.246564 ms, max 6.830654 ms.
- Remote gate was attempted but DNS was unavailable; no platform upload or activation was performed. Luna harness compatibility remains unavailable (`native_luna_compatible: False`).
- Submission archive: `artifacts/submissions/v0002_cap-replan_20260805-1736_2de8371f.zip` (SHA-256 `5f3118ba1d25c98fc890f76b895ab6c68adc5a51b4a4feeffa9ea52c81edd9c2`).

### Codex implementation task — 2026-08-05T11:23:01Z

- Task: Implement only the final Sol review blocker in reports/codex-20260805T084146Z/review-2.md: derive a team-wide active-project count from authoritative live shared state using a delayed-Store-safe Core/Builder protocol; apply that count before route admission and every new_project discretionary spend; add a real Player.run test with three independently owned active projects, without directly assigning BuilderStateData.active_projects, proving a fourth route and Splitter/Barrier/Launcher/turret projects are rejected. Preserve baseline, configs, maps, README, unrelated files, and the existing successful remediation. Use the required Sol planner -> Luna implementer -> Sol reviewer workflow, run the exact focused retest plus make static, make smoke, make eval-regression, make eval-local, and the benchmark. Do not perform platform operations. Produce truthful process-fallback evidence with exact agent IDs/models/exit codes.
- Backend: process-fallback
- Luna evidence recorded: False
- Outcome: planner failed
- Report: reports/codex-20260805T112300Z


### Codex implementation task — 2026-08-05T11:22:46Z

- Task: Implement only the final Sol review blocker in reports/codex-20260805T084146Z/review-2.md: derive a team-wide active-project count from authoritative live shared state using a delayed-Store-safe Core/Builder protocol; apply that count before route admission and every new_project discretionary spend; add a real Player.run test with three independently owned active projects, without directly assigning BuilderStateData.active_projects, proving a fourth route and Splitter/Barrier/Launcher/turret projects are rejected. Preserve baseline, configs, maps, README, unrelated files, and the existing successful remediation. Use the required Sol planner -> Luna implementer -> Sol reviewer workflow, run the exact focused retest plus make static, make smoke, make eval-regression, make eval-local, and the benchmark. Do not perform platform operations. Produce truthful native-v1 evidence with exact agent IDs/models/exit codes and stop after the allowed review limit.
- Backend: native-v1
- Luna evidence recorded: False
- Outcome: native V1 did not provide complete Luna/approval evidence
- Report: reports/codex-20260805T112246Z


### Codex implementation task — 2026-08-05T11:13:58Z

- Task: Resume the existing integrated candidate remediation. Read reports/codex-20260805T010045Z/review-1.md and implement only its four concrete findings: (1) verify the single-map bounded route planner and blocked-step CPU path, (2) make delivery/repair/claim-heartbeat/reassignment transitions executable through real Builder/Core handlers, (3) wire payback/reserve, Splitter/Barrier/Launcher, threat/opening, and late-game policies into live handlers with legality and fresh-target guards, and (4) produce truthful native Sol-Luna-Sol evidence. The current tree already contains a Luna remediation attempt; do not broaden scope or revert it. Preserve baseline, versions, README, state/UPDATES/startup, configs, maps, and unrelated files. Run the exact reviewer retests, make static, make smoke, make eval-regression, make eval-local, and the expanded benchmark; use existing full-matrix reports only if hashes match, otherwise rerun. No platform operations. The final report must use backend native-v1, name exact agent IDs/models/exit codes, and have an independent sol_reviewer verdict.
- Backend: native-v1
- Luna evidence recorded: False
- Outcome: APPROVED
- Report: reports/codex-20260805T084146Z


### Verification-only Sol-Luna-Sol harness probe approved — 2026-08-05T00:54:23Z

- sol_planner produced a bounded read-only packet; luna_implementer reported `# Florent Code League bot workspace`; sol_reviewer returned `APPROVED`.
- Native multi-agent evidence records `gpt-5.6-sol` for planning/review and `gpt-5.6-luna` for implementation inspection.
- Before/after status, diff, protected hashes, and full repository fingerprints matched; no source, configuration, live-state, or platform changes occurred.
- Evidence: `reports/codex-20260805T004253Z`.


### Session startup and scoped document routing added — 2026-08-05T00:25:00Z

- Added generated `docs/START_HERE.md` plus machine-readable `state/project_state.json` for cross-session development focus.
- Root `AGENTS.md` now requires a startup bootstrap but routes agents to detailed documents conditionally instead of loading everything every time.
- Added nested instructions for `bots/candidate/`, `scripts/`, and `tests/`.
- Updated Sol planner, Luna implementer, and Sol reviewer instructions to read startup state and nearest nested guidance.
- Added project-state/update scripts, automatic startup-summary refresh, Make targets, and regression tests.
- Resolved the orchestration-skill conflict: Luna implementation tasks cannot deploy, while the approved primary Sol/operator live workflow remains authorized by policy.


### Codex harness and live operator audited — 2026-08-05

- Found that the original custom-agent TOML did not prove Luna execution under the current Sol/Terra V2 versus Luna V1 mismatch.
- Added a reversible native-V1 route and an explicit process-isolated Sol → Luna Max → Sol fallback with exact command evidence.
- Added autonomous resumable upload, activation, live scoring, promotion, and rollback using `state/live_state.json`.
- Separated V1 and V2 configuration modes to avoid a boolean/table key conflict.
- Kept Sol as the only live reviewer/operator; Luna implements code but cannot modify live state or perform platform writes.


### Repository initialized — 2026-08-05

- Created the rules reference, Codex harness, starter bot, local/remote evaluation scripts, and submission workflow.
- Initial live state is unknown because no authenticated `fcode` session was available when the repository was generated.
