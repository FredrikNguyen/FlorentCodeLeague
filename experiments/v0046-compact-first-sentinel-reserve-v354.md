# v354 compact first-Sentinel budget contract — rejected

## Causal basis

The fresh v108/Askar City replays showed successful compact-map delivery but
late or absent forward Sentinels: Frostgate delivery/Sentinel was 13/94,
Icefloe 20/28, and Yulerune 18/never.  Askar established its first Sentinel at
9/20/56.  The bounded hypothesis was that stage-two Builder spawning could
consume a dynamically priced Sentinel reserve after the five-worker opening.

## Scope

Temporary production scope was only `bots/candidate/bot/core_role.py`, with
focused coverage in `tests/test_candidate_nearest_defense.py`.  After a real
income heartbeat, a cramped-map Core with its initial roster alive would keep
the live Sentinel price before a stage-two spawn until a forward Sentinel,
home threat, open geometry, or two-board-span deadline released the reserve.
No Store, route, attacker, Launcher, placement, ammo, baseline, or platform
logic was changed.

## Evidence

- Focused temporary coverage: **28/28**; candidate compileall passed.
- `make static`: only the inherited 15 obsolete-module import errors and two
  navigation fast-path assertions; no v354-specific error
  (`reports/iter-v354-compact-first-sentinel-reserve/static.log`).
- Temporary smoke: **4/4 command-clean** at
  `reports/local-20260820T141934Z`.
- Explicit immutable-v0046 rotated all-map screen (seed 173): **8-7**,
  collection **94,680 vs 78,240 Ti**, all candidate rows delivered, zero
  command/TLE/suspicious rows, max replay p99 **1,163 us**
  (`reports/local-20260820T142122Z`; parsed diagnostics at
  `reports/iter-v354-compact-first-sentinel-reserve/screen-replay-analysis.json`).
- Compact timing moved in the intended direction on Frostgate (**54 vs 112**)
  and Icefloe (**20 vs 28**) first Sentinel, but Yulerune remained no-Sentinel
  for both sides.  That mechanism metric did not create the required 9-6
  aggregate win edge.

## Decision and rollback

Reject after the first screen.  The implementation had no focused defect, so
changing the reserve amount/window/predicate would be an ungrounded tuning
repair.  No 60-game matrix, remote gate, package, submission, activation, or
promotion ran.  Candidate production was restored exactly to immutable v0046:
the recursive parity proof is empty at
`reports/iter-v354-compact-first-sentinel-reserve/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4 command-clean** at `reports/local-20260820T142459Z`.

## Remaining risk

The first-Sentinel timing signal is real but not sufficient to improve the
whole-map win rate.  A later experiment must identify a different causal
conversion path, rather than varying this Core reserve in place.  v108 remains
in guarded live observation; immutable v0046 remains the local baseline.
