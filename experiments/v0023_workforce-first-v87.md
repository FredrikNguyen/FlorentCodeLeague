# v0023 workforce-first v87 comparator

- Parent: `v0022_nearest-home-responder_20260812-1343_eeafad8f` / active platform v92.
- Hypothesis: keeping a bounded workforce-first opening (six living Builders after one completed chain or round 24), retiring remote counter-Gunner construction, and accounting for home Gunner lifetime placements improves win-primary performance without reliability regressions.
- Exact changed files: `bots/candidate/main.py`, `bots/candidate/bot/constants.py`, `bots/candidate/bot/core_role.py`, `bots/candidate/bot/defender.py`, `bots/candidate/bot/dynamic.py`, `tests/test_candidate_nearest_defense.py`, `tests/test_analyze_replay.py`, and `scripts/analyze_replay.py`.
- Git: `eeafad8f` at packaging time; working tree dirty with unrelated pre-existing changes. `fcode --version`: 2.3.6.
- Local release matrix: 21 maps x 5 seeds x 2 side orders, exact v87 artifact SHA-256 `0c59d375548f427371f14eb48ec58eea761b63a9164e72753f3cc9ee6489b4ad`; 143-67-0, 751,210 vs 638,090 titanium, zero command/TLE/suspicious failures. Evidence: `reports/local-20260812T143141Z/workforce-first-v87-210-summary.json`.
- Validation: focused 18/18, compileall passed, smoke 4/4 command-clean; `make static` remains blocked by 15 inherited obsolete legacy-import tests.
- Remote gate: not run in this upload step.
- Platform submission and activation: to be recorded after upload; activation is intentionally separate and not requested here.
- Decision: upload the locally strongest candidate; retain v87 as comparator/rollback context until a separate live decision.
