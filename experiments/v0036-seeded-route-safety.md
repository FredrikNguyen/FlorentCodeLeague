# v0036 — seeded-route replacement safety

## Objective

Prevent a Builder's seeded conveyor-route recovery from dying permanently when
the remembered seed tile is empty, enemy-owned, or replaced by a building that
has no direction.

## Hypothesis

`_run_seeded_route` can retain a stale `route_seed` after another unit replaces
the seed conveyor. Calling `get_direction` on a Barrier or Gunner raises; the
top-level exception handler swallows the failure, leaving the Builder in a
retry loop. Requiring a visible, friendly `EntityType.CONVEYOR` before reading
its direction should clear stale state and return the Builder to `SCOUT`, while
preserving valid conveyor continuation.

## Scoped implementation

- `bots/candidate/bot/defender.py`: validate seed visibility, existence, team,
  and entity type before `get_direction`; stale routes call the existing
  `_end_seeded_route` recovery path.
- `tests/test_candidate_seeded_route.py`: four focused cases for same-team
  replacement, enemy replacement, empty seed, and valid conveyor continuation.
- No Store, siege, Launcher, economy, navigation, attacker, or baseline changes
  were made for this hypothesis.

## Validation

- Focused route plus enemy-Core cage suites: **9/9**;
  `reports/iter-seeded-route-safety-v0036/focused.log`.
- Static contract: **8/8**;
  `reports/iter-seeded-route-safety-v0036/static-contract.log`.
- Candidate compileall: passed;
  `reports/iter-seeded-route-safety-v0036/compileall.log`.
- Smoke: **4/4 command-clean**;
  `reports/local-20260816T105124Z`.
- Exact v101 six-map screens: seed 1 **9/12**
  (`reports/local-20260816T105150Z`), seed 19 **7/12**
  (`reports/local-20260816T105317Z`); pooled **16/24**, no command failures.
- Continue54: **31/54**, zero command failures;
  `reports/local-20260816T105457Z`.
- Full current 15-map × 7-seed × side-swapped matrix: **122-88 (58.1%)**,
  exact two-sided binomial p=0.0225; paired side-swap decisive pairs were
  36 candidate sweeps versus 19 baseline sweeps (50 splits, sign p=0.0300).
  Candidate collection was **1,238,420 vs 1,096,410 Ti (1.1295x)**; five
  candidate no-delivery games versus seven baseline; zero command failures,
  TLEs, or suspicious output; max p99 **1,437 us**, peak **5,912 us**.
  Report: `reports/local-20260816T110158Z`; summary:
  `reports/iter-seeded-route-safety-v0036/full-analysis.json`.
- Full-matrix map floors (candidate-baseline): antler 6-8, archipelago 11-3,
  auroraveil 7-7, drakkarfjord 7-7, drumlin 9-5, fjordgate 7-7,
  frostgate 7-7, glacierkeep 9-5, icefloe 11-3, midgard 9-5,
  nordkap 9-5, ragnarok 7-7, royale 10-4, valkyrie 7-7, yulerune 6-8.
- Pinned remote test: **2-3**, zero TLE/suspicious output, candidate 17,210
  versus baseline 23,310 Ti, both sides zero no-delivery; max p99 **2,490 us**,
  peak **3,402 us**. It was an unrated ephemeral test only (no persistent
  submission upload or activation). Reports:
  `reports/remote-20260816T113107Z`,
  `reports/iter-seeded-route-safety-v0036/remote-summary.json`.
- `make static` remains the inherited worktree failure (65 tests, 5 failures,
  15 obsolete-module import errors); log:
  `reports/iter-seeded-route-safety-v0036/make-static.log`.

## Decision and risks

This is a **local release candidate** under the win-rate-first policy. The
long local edge is materially positive and reliability-clean, but the remote
gate is a 2-3 caution and antler/yulerune are 6-8 map regressions. The package
was created without platform operations:

`artifacts/submissions/v0036_seeded-route-safety_20260816-1134_eeafad8f.zip`

SHA-256: `676cbe6c340011ca9dc3ef460ad40fc81827f79d9438336329b446dfff769cb4`.

The direct diff against immutable v0035 also shows pre-existing dirty-tree
differences (a removed defender comment and a `core_role.py` loop `break`), not
part of this seed-guard hypothesis; they remain a release-review risk because
the package snapshots the current candidate tree. The full static target is
blocked by unrelated deleted legacy modules. No upload, activation, or live
state operation was performed.
