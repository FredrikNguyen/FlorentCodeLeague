# v375 secondary-attacker siege relay — rejected

## Objective and scope

Starting from immutable v0046, v375 allowed only the designated secondary
fixed attacker to answer a non-crisis Core siege beacon.  The primary attacker
kept the existing offense lane, while all route owners and dynamic workers
kept their current policy.  Crisis beacons retained the existing override for
all roles.  The change used the existing `SLOT_CORE_SIEGE` signal and added no
Store slot, unit target, ammo rule, route behavior, or map branch.

Allowed production files were `bots/candidate/main.py` and
`bots/candidate/bot/attacker.py`; focused coverage was limited to
`tests/test_candidate_nearest_defense.py`.  Baseline snapshots, package,
upload, activation, and live state were out of scope.

## Validation

- Focused coverage: **27/27**; candidate compileall passed.
- `make static`: inherited exit 2 only (15 obsolete-module imports and two
  navigation fast-path assertions); no v375-specific static failure.
- Smoke: **4/4** command-clean at `reports/local-20260820T210835Z`.
- First rotated 15-map/30-game screen (`screen_seed=479`) was command-clean,
  delivery-complete (30/30 each), and zero TLE/suspicious-output rows, but
  candidate won only **10–20**.  Candidate collection was **153,820 vs
  194,560 Ti**, with average surviving Harvesters **6.63 vs 7.53** and
  Sentinels **0.80 vs 1.87**.  Diagnostics are in
  `reports/iter-v375-secondary-siege-relay/analysis.json`; raw games are in
  `reports/local-20260820T210907Z`.

The 9–6 first-screen floor failed decisively.  No second screen or release
matrix was justified; the narrower relay still pulled pressure/economy away
from the baseline in this schedule.

## Rollback and decision

The temporary ownership helper, main gate, focused test, and screen config were
removed.  Candidate production is recursively byte-identical to immutable
v0046; the parity proof is empty at
`reports/iter-v375-secondary-siege-relay/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T211301Z`.

Reject v375.  Immutable v0046 remains the comparator and no baseline, package,
upload, activation, promotion, or live-state transition occurred.

## Next direction

Do not widen the siege relay or revisit the rejected all-worker rally.  The next
experiment must target a different directly observable conversion bottleneck,
with the same delivery, reliability, and protected-map floors.
