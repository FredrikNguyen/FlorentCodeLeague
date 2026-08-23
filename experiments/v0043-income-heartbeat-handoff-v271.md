# v271 income-heartbeat economy/offense handoff — promoted

## Parent and hypothesis

- Parent immutable baseline: `bots/versions/v0043_liquidity-backed-dynamic-floor_20260819-0415_eeafad8f`.
- Candidate: `bots/candidate`.
- Engine: `fcode 2.3.4`.
- Git HEAD at implementation: `eeafad8f6207fcccb135311659aa55ca6c690a64` (dirty worktree; unrelated user changes preserved).

The v106 loss audit showed repeated early conversion failure: a historical
geometric `SLOT_HARVESTER_COUNT` milestone released dynamic Builders while
the Core had not seen recent positive titanium income. The hypothesis was to
publish a conservative economy phase in the high bits of the existing ore
cursor. Dynamic Builders remain on the existing SCOUT/CHAIN route loop during
OPENING, CONVERTING, and CRISIS; only a real route milestone plus a recent
income heartbeat unlocks the existing pressure/hijack/raid priorities.

## Exact scope

Changed production files:

- `bots/candidate/bot/constants.py` — phase values, cursor packing, and the
  eight-round income heartbeat window;
- `bots/candidate/main.py` — Core-only quiet-round state;
- `bots/candidate/bot/core_role.py` — phase publication from existing resource
  accounting;
- `bots/candidate/bot/dynamic.py` — phase-aware economy lease;
- `bots/candidate/bot/defender.py` — preserve phase bits when advertising ore.

Focused coverage: `tests/test_candidate_economy_phase.py`. No new Store slot,
route geometry, infiltrator selector, fixed-attacker policy, purchase policy,
map branch, baseline source, package logic, or live-state logic was changed.

## Validation

- Focused phase plus nearest-defense tests: **30/30**;
  `reports/iter-v271-income-heartbeat-handoff/focused.log`.
- Candidate compileall: **pass**;
  `reports/iter-v271-income-heartbeat-handoff/compileall.log`.
- `make static`: inherited exit **2** only (15 obsolete deleted-module
  imports and two rolled-back navigation assertions); no v271-specific error;
  `reports/iter-v271-income-heartbeat-handoff/static.log`.
- `make smoke`: **4/4 command-clean**;
  `reports/iter-v271-income-heartbeat-handoff/smoke.log` and
  `reports/local-20260819T105628Z`.
- Screen seed 172: **9–6**, candidate/baseline collection **59,540/56,930
  Ti**, first delivery **15/15 vs 15/15**, max p99/peak **1,415/5,818 us**;
  `reports/local-20260819T105712Z` and
  `reports/iter-v271-income-heartbeat-handoff/screen-172-analysis.json`.
- Independent screen seed 175: **7–8**, collection **54,050/56,470 Ti**,
  first delivery **15/15 vs 15/15**, max p99/peak **1,296/2,345 us**;
  `reports/local-20260819T105911Z` and
  `reports/iter-v271-income-heartbeat-handoff/screen-175-analysis.json`.
- Combined screens: **16–14** candidate wins, no candidate no-delivery,
  TLE, or suspicious rows; collection **113,590/113,400 Ti**.
- Release gate: **33–27** over 60 games, candidate collection
  **293,190/269,970 Ti**, first delivery **60/60 vs 58/60**, mean delivery
  **30.67/62.90 rounds**, zero command failures/TLE/suspicious rows, max
  p99/peak **1,550/2,641 us**;
  `reports/local-20260819T110125Z` and
  `reports/iter-v271-income-heartbeat-handoff/release-60-analysis.json`.

## Decision

Promote v271 as the moving local baseline. The 60-game gate meets the 55%
win-rate rule with a clean reliability profile, better collection, and two
fewer baseline no-delivery games. Antler and Midgard remain 1–3 map risks;
Auroraveil is 4–0 and the other maps are no worse than 2–2. Preserve v0043
as the rollback snapshot. Package/upload/activation are separate guarded
steps and must retain v101 as the live rollback target.

## Remote and live operation

- Remote gate match `f1c597a2-1a7d-425a-b19b-8177ef1d6efe` finished **2–3**
  (candidate wins sprint and vault; v0043 wins bridge, crossfire, and
  aurora). It was a small, non-rated sanity check with no runtime errors;
  records are `reports/remote-20260819T111559Z` and
  `reports/iter-v271-income-heartbeat-handoff/remote-match-info-final.json`.
- Before deployment, the deterministic live observer found active v106 at
  **46/95** wins (0.4842) across 19 rated series versus v101's 0.7000,
  clean reliability, and rolled it back to v101. Evidence:
  `reports/live-observe-20260819T111212Z` and
  `reports/live-rollback-20260819T111545Z`.
- Package `v0044_income-heartbeat-handoff_20260819-1110_eeafad8f.zip` has
  SHA-256 `104a851d29678ca2b1cf6c8fae241196feb496aef3da733e5871d53531a618e4`.
  Guarded deployment activated platform **v107** at 2026-08-19T11:17:51Z,
  with v101 preserved as rollback; report:
  `reports/live-deploy-20260819T111731Z`.

## Remaining risks and follow-up

- The aggregate edge is material but not dominant; live observation must test
  whether the income heartbeat transfers beyond the local opponent.
- The phase is conservative when net income is masked by simultaneous spending;
  inspect live conversion and no-delivery rows before changing the window.
- `make static` remains blocked by inherited deleted-module imports and the
  rolled-back navigation assertions.
