# v374 late mirrored-Core Sentinel fallback — rejected

## Objective and scope

Starting from immutable v0046, v374 tested one late pressure recovery path for
losses that reached the opposing half without direct enemy-Core intel.  Once
five completed routes and the shared `PRESSURE` phase were visible, only the
primary fixed attacker could spend one Sentinel aimed at the rotationally
mirrored Core estimate.  The gate preserved the dynamic-price cost of one
replacement Harvester plus two Conveyor links, and a per-attacker one-shot
flag prevented a guessed coordinate from becoming a production loop.

Allowed production files were `bots/candidate/main.py` and
`bots/candidate/bot/attacker.py`; focused coverage was limited to
`tests/test_candidate_nearest_defense.py`.  Route geometry, opening economy,
Store schema, Sentinel pool limits after direct intel, baseline snapshots,
packaging, upload, activation, and live state were non-goals.

## Validation

- Focused coverage: **27/27**; candidate compileall passed.
- `make static`: inherited exit 2 only (15 obsolete-module imports and two
  navigation fast-path assertions); no v374-specific static failure.
- Smoke: **4/4** command-clean at `reports/local-20260820T205908Z`.
- First rotated 15-map/30-game screen (`screen_seed=467`) was command-clean
  with zero TLE/suspicious-output rows but only **15–15**.  Candidate had
  **29/30** first deliveries versus 30/30 for v0046, collected
  **117,390 vs 132,130 Ti**, and ended with **1.10 vs 1.93** surviving
  Sentinels on average.  Replay diagnostics are in
  `reports/iter-v374-late-mirrored-sentinel/analysis.json`; raw games are in
  `reports/local-20260820T205940Z`.

The required 9–6 first-screen floor failed, so no second screen or 60-game
release matrix was justified.  The fallback did not create a repeatable
pressure edge and its collection/delivery profile regressed; broadening the
guessed-Core gate would be an ungrounded repair.

## Rollback and decision

The temporary state, helper, focused test, and screen config were removed.
Candidate production is recursively byte-identical to immutable v0046; the
parity proof is empty at
`reports/iter-v374-late-mirrored-sentinel/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T210338Z`.

Reject v374.  Immutable v0046 remains the comparator and no baseline, package,
upload, activation, promotion, or live-state transition occurred.

## Next direction

The zero-Sentinel loss pattern remains, but a guessed late Core target is not
the fix.  The next hypothesis must use a fresh, directly observable action or
resource-conversion signal and retain the 9–6, delivery, reliability, and
protected-map floors.
