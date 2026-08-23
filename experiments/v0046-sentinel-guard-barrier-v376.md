# v376 Sentinel guard Barrier — rejected

## Objective and scope

Starting from immutable v0046, v376 tested whether a forward Sentinel that
survived one observed round should receive one nearby, escape-safe Barrier.
The guard was one-shot per Sentinel, required a live-unit signal, dynamic
Barrier plus Harvester affordability, and never interrupted route state,
Sentinel pool policy, or ammo policy.  Production scope was limited to
`bots/candidate/main.py` and `bots/candidate/bot/attacker.py`; focused coverage
was temporary coverage in `tests/test_candidate_nearest_defense.py`.

## Validation

- Focused coverage was **27/27**; candidate compileall passed.  `make smoke`
  was **4/4** command-clean at `reports/local-20260820T211908Z` and static
  retained only the inherited workspace failures (15 obsolete imports and two
  navigation fast-path assertions).
- First rotated all-15-map screen (`screen_seed=487`) was **19-11**, with no
  command failures, no TLE/suspicious rows, and 30/30 candidate and baseline
  deliveries.  Candidate collected **195,000 Ti** in aggregate and averaged
  7.60 surviving Harvesters and 1.10 Sentinels.  Raw games and manifest are
  under `reports/local-20260820T211932Z`; diagnostics are in
  `reports/iter-v376-sentinel-guard-barrier/analysis-screen1.json`.
- The independent second screen (`screen_seed=491`) collapsed to **7-23**,
  still command- and delivery-clean.  Candidate collection fell to **130,720
  Ti** aggregate, averaging 5.33 Harvesters and 0.83 Sentinels.  Evidence is
  under `reports/local-20260820T212334Z` and
  `reports/iter-v376-sentinel-guard-barrier/analysis-screen2.json`.

The pair was **26-34**, below the 19-11 promotion floor.  The first-screen
edge was schedule variance and the Barrier spend did not reliably convert to
survivable pressure; no release matrix was justified.

## Rollback and decision

The temporary guard, focused test, and two screen configs were removed.
Candidate production is recursively byte-identical to immutable v0046; the
parity proof is empty at
`reports/iter-v376-sentinel-guard-barrier/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T212759Z`.  No baseline, package, upload,
activation, promotion, or live-state transition occurred.

Reject v376.  Keep v0046 as the comparator and do not widen Sentinel guard
construction without a new resource-conversion signal.
