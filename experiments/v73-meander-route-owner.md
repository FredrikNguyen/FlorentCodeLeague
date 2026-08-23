# v73 25x15 route-owner continuity

## Scope

- Parent: `bots/versions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03`.
- Hypothesis: on the 25x15 geometry, a pre-income route owner must ignore
  non-adjacent Builder-rush alerts while free workers respond, preserving the
  first funded route.
- Allowed runtime file: `bots/candidate/bot/builder.py`.
- Test file: `tests/test_candidate_bootstrap_defense.py`.
- Diagnostic tooling: `scripts/analyze_replay.py` and its focused test.
- Non-goals: no spending, workforce, navigation, offense, general defense, or
  behavior changes on any other geometry.

## Evidence before change

- Platform v73 lost both sampled `meander` games.
- Immutable v0015 collected zero on both sides of two exact live seeds.
- Replay analysis of the rejected broad owner-protection experiment shows its
  25x15 candidate established Harvesters at turns 12-13 and first delivery at
  turns 17-18; unchanged v0015 built only 1-3 Conveyors and never delivered.
- Immutable v0015 self-mirror on `meander`, `saga`, and `snowflake` scored 8-10;
  `snowflake` alone was 2-4 despite identical source on both sides. The old
  protected-map rejection therefore measured runner/side variance, not a causal
  change on those geometries. Report: `reports/local-20260809T203800Z`.

## Gate

- Focused tests must cover immediate contact, non-adjacent alerts, post-income,
  free workers, and explicit 24x24/26x26 non-target geometries.
- Both 25x15 sides must establish a Harvester and delivery in replay analysis.
- `saga` and `snowflake` must remain source-path-inactive and within the measured
  immutable self-mirror variance.
- Run focused tests, `make static`, smoke, a targeted matrix, diff review, and
  remote gate before packaging.

## Results

- Focused tests: 4/4 passed, including analyzer coverage; compileall passed.
- Smoke: 4/4 command-clean, report `reports/local-20260809T204830Z`.
- Targeted replay set: 18/18 command-clean, 13-5 paired wins, 70,190 versus
  35,020 titanium (ratio 2.0037); report
  `reports/v73-meander-route-owner/summary.md`.
- All six meander sides built a Harvester at turn 12/13 and delivered at turn
  17/18. Replay analysis found zero TLE markers, zero suspicious output, and a
  maximum callback time of 7,235 microseconds.
- `make static` retains only the inherited pre-v69 API/obsolete production-line
  failures documented in the prior checkpoint; no new failure is attributable
  to this geometry-only patch.

### Remote gate and package

- The guarded five-map server test completed at
  `reports/remote-20260809T204654Z` with match
  `5c664cfa-5162-4bce-a117-487f92aafa8c`.
- The candidate won 3-2 against immutable v0015 on `meander`, `moonrise`,
  `snowflake`, `saga`, and `lighthouse`; all five games completed without a
  server error, resignation, or reported TLE.
- The passing candidate is frozen as v0016 at
  `bots/versions/v0016_meander-route-owner_20260809-2058_eeafad8f` and
  `artifacts/submissions/v0016_meander-route-owner_20260809-2058_eeafad8f.zip`.
- Archive SHA-256:
  `7c83de94e62aeceff3f57b2ef1c46539533c64c9b19690a072c620d7aff07d8f`.

### Selected regression checkpoint

- `make eval-regression` completed all 54 requested games command-clean against
  immutable v0015 on nine maps, three seeds, and both side orders. Report:
  `reports/local-20260809T210356Z`.
- The candidate won 30-24, with zero TLE markers and zero suspicious output,
  and collected 112,260 titanium versus 99,790 (ratio 1.1250). Maximum
  observed callback time was 7,726 microseconds.
- Map evidence is mixed but clears the aggregate guard: `aurora` was 6-0 for
  the candidate with 49,170 versus 36,040 titanium, while source-path-active
  `sweden` (25x15) was 3-3 with 11,880 versus 12,540 titanium.
- The corrected attribution assigns each replay's titanium by its filename
  (`candidate-A`/`candidate-B`), not by the winner side; the initial 0.9511
  figure was a diagnostics error.

## Status

The focused local gate, remote test, package checks, and selected 54-game
regression passed. The package was subsequently uploaded as platform v75 after
the v73 observation was interrupted and an unrelated v74 upload was rejected.
v72 remains the known-good rollback.

### Full release gate

- The 210-game, 21-map release matrix completed 106-104 with 424,170 titanium
  versus 425,080 (ratio 0.9979) and zero command failures; report
  `reports/local-20260809T205017Z`.
- Across 3,505,948 replay bot calls, every per-replay p99 was at most 4.164 ms,
  the maximum call was 7.270 ms, and there were zero TLE or suspicious-output
  signals.
- Legacy `sweden` shares the 25x15 dimensions and was therefore source-active;
  it finished 5-5 with 19,800 versus 20,900 titanium. The strict meander gain,
  aggregate 0.9979 collection ratio, selected-regression win, and remote win
  clear the bounded release gate. Summary:
  `reports/v73-meander-route-owner/release-summary.md`.

## Live continuation

- The third rated v73 series was a 1-4 loss to PromptNPray (version unknown),
  with losses on saga, fjordgate, lighthouse, and heart and the sole win on
  archipelago. It was reliability-clean and changed the observation window to
  2-1 by series, 8-7 by games, score 0.5333, adjusted residual +0.0217, net
  +2.08 Elo, rating 1385.17, rank 49/116. Evidence:
  `reports/live-observe-20260809T204432Z`.
- This remains below the 12-series decision minimum. v73 stays active and v72
  stays the rollback; the v0016 package is ready but not uploaded.
- A guarded observation capture at `reports/live-observe-20260809T205737Z`
  found no new rated series; the live window remains 3 of 12.
- The next guarded capture at `reports/live-observe-20260809T210321Z`
  recorded DNS failures for ladder, match, and submission queries, so it
  produced no additional rated-series evidence and left v73 at 3 of 12.
- A further capture at `reports/live-observe-20260809T212019Z` had the same
  DNS failure for live queries; v73 remains active at 3 of 12 and v72 remains
  the rollback target.
- Connectivity recovered at `reports/live-observe-20260809T212442Z`. After
  seven rated series, v73 is 4-3 by series and 17-18 by games, with score
  0.4857, adjusted residual -0.0151, net -3.38 Elo, rating 1379.71, rank
  49/116, and zero reliability failures. It remains below the 12-series gate.
- v73 ultimately reached nine reliability-clean series: 6-3 by series, 23-22
  by games, score 0.5111, adjusted residual +0.0079, and net +2.28 Elo. An
  externally uploaded platform v74 became active before v73 reached the
  12-series minimum, so v73 was not promoted. Evidence:
  `reports/live-observe-20260809T213951Z`.
- The unrelated v74 source did not match any v0014-v0016 snapshot. In a full
  20-game smoke comparison it lost 7-13 to v0016 and trailed 13,133-19,339
  titanium with no command or reliability failure. Reports:
  `reports/live-v74-identification/` and `reports/local-20260809T215313Z`.
- v74 was rolled back to protected v72, then the release-gated archive was
  uploaded and activated as platform v75, named
  `v0016-meander-route-owner-eeafad8f`. Initial observation report:
  `reports/live-observe-20260809T215618Z`. v75 has no completed rated series
  yet; v72 remains its rollback target.
