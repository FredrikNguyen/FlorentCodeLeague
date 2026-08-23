# Florent Code League development and live updates

### Repository cleanup and v0047 retention — 2026-08-23

- Retained immutable `bots/versions/v0047_pressure-economy-steward_20260821-0200_eeafad8f`
  as the only local version snapshot and confirmed that `bots/candidate/` is its
  exact production copy. Replaced the older flat-layout `bots/baseline/`
  executable with the same v0047 package layout while preserving its strategy
  Markdown. The rejected v411 candidate remains documented but is not promoted
  or deployed.
- Removed obsolete starter/planning ZIP archives, v0001–v0046 snapshot
  directories, generated replay payloads, cache directories, replay-diagnosis
  output, and experiment `.tmp-*` entries. Human-readable experiment Markdown,
  `UPDATES.md`, state files, and ignored reports were preserved for provenance.
- Updated `README.md`, `.gitignore`, `docs/REPOSITORY_STRUCTURE.md`, and the
  evaluation configs so the current release of record is explicit and generated
  artifacts do not return to the worktree. Full details are in
  `docs/REPOSITORY_CLEANUP.md`.
- Retired the old unit-test suite that imported the removed pre-v0047 module
  layout; current v0047-focused coverage is **36/36**. `make static` is now
  **67/67** with compileall passing, and `make smoke` is **4/4** command-clean
  (`reports/cleanup-20260823-static.log`,
  `reports/local-20260823T073457Z`).
- This was a repository/documentation checkpoint only: no bot behavior, package,
  upload, activation, or live-state transition was performed. The final staged
  diff review and publish commit remain required.

### v411 Route-conversion priority rejected — 2026-08-21

- Compared a narrow dynamic task-allocation rule against immutable v0047:
  after three completed routes, a funded visible Harvester opportunity could
  outrank a non-Core-ring belt repair during OPENING/CONVERTING.  Core-ring,
  crisis, pressure, fixed-attacker, route-FSM, and Store behavior were
  unchanged.
- The first 15-map screen was **5-10** and included a candidate no-delivery
  Royale.  A bounded repair that restored the original ordering before three
  routes and required an actual route opportunity reached only **6-9**, with
  another candidate no-delivery Icefloe.  Neither met the 9-6 promotion floor.
- Candidate focused coverage was **34/34** initially and **35/35** after the
  repair; rollback was **32/32**.  Compileall passed, smoke was **4/4** for
  both candidate states, and rollback smoke against v0047 was **4/4**.
  `make static` retained the inherited 15 import failures and two navigation
  assertions.
- Reject v411.  Temporary source/test/config edits were removed and recursive
  production parity with immutable v0047 is exact.  No release, package,
  upload, activation, or baseline transition occurred.  Evidence:
  `experiments/v0047-route-conversion-priority-v411.md`,
  `reports/iter-v411-route-conversion/`,
  `reports/local-20260821T085543Z`, and
  `reports/local-20260821T085912Z`.

### v410 Large-board dynamic route floor rejected — 2026-08-21

- Compared a geometry-conditioned dynamic-builder economy floor against
  immutable v0047.  On boards at least 30×30, optional raid/advance work
  waited for five completed routes unless a forward Sentinel witness existed;
  fixed attackers and short-board behavior were unchanged.  A bounded repair
  allowed the first Sentinel at three routes so it could publish that witness.
- The initial all-map screen was **8-7**; the side-balanced 30-game screen was
  **17-13**, both command-clean.  The complete 60-game endpoint-seed/both-side
  gate tied **30-30**, with **336,640 vs 332,380 Ti**, zero command/TLE/
  suspicious rows, and no delivery command failures.  Replay review found
  fewer dynamic Sentinels on Midgard/Ragnarok under the delayed gate.
- The bounded Sentinel repair passed **39/39** focused tests, compileall, and
  smoke **4/4**, but its independent screen tied **15-15**.  Rollback passed
  **36/36**, compileall, and smoke **4/4**; `make static` retained the
  inherited 15 obsolete imports plus two navigation assertions.
- Reject v410 and repair; temporary source/test/config edits were removed and
  recursive production parity with v0047 is exact.  No package, remote gate,
  upload, activation, or baseline transition occurred.  Evidence:
  `experiments/v0047-large-board-dynamic-floor-v410.md`,
  `reports/local-20260821T081545Z`, `reports/local-20260821T081855Z`,
  `reports/local-20260821T082232Z`, `reports/local-20260821T083128Z`, and
  `reports/local-20260821T083655Z`; v0047 remains the baseline.

### v409 Pre-Sentinel crisis attacker economy recovery rejected — 2026-08-21

- Compared one role-flexibility rule against immutable v0047: before any
  forward Sentinel existed, a fixed attacker could temporarily run the economy
  FSM during Core-published `CRISIS`, but only when the bank could not afford a
  Harvester.  Active chains were preserved and discretionary hijack/turret/
  siege work was suppressed during recovery.
- The broad initial screen (`screen_seed=211`) regressed to **10-20** despite
  30/30 deliveries and zero command/TLE/suspicious rows; collection was
  **178,070 vs 196,030 Ti**.  The one bounded repair required actual Harvester
  unaffordability and reached **19-11** on `screen_seed=223`, with 30/30
  deliveries, collection **181,780 vs 161,290 Ti**, and zero reliability rows.
- The required 60-game endpoint-seed/both-side gate was **30-30**, with
  60/60 deliveries for both sides, zero TLE/suspicious rows, collection
  **311,540 vs 304,910 Ti**, and max p99/peak **1,511/4,200 us**.  Antler,
  Auroraveil, Drumlin, Frostgate, and Valkyrie were each 1-3; Royale was 4-0.
- Reject v409.  Temporary production/test/config edits were removed and
  recursive candidate parity with v0047 is exact.  Rollback focused coverage
  was **36/36**, compileall passed, smoke was **4/4**, and `make static`
  retained the inherited exit-2 profile.  Evidence:
  `experiments/v0047-crisis-attacker-economy-recovery-v409.md`,
  `reports/iter-v409-crisis-attacker-*.log`,
  `reports/local-20260821T074304Z`, `reports/local-20260821T074746Z`, and
  `reports/local-20260821T075204Z`.  No release, package, remote, upload,
  activation, or baseline transition occurred; v0047 remains the baseline.

### v408 Confirmed-dead fixed-attacker handoff rejected — 2026-08-21T11:00:00+02:00

- Compared a confirmed-dead fixed-attacker lifecycle handoff against immutable
  v0047.  After the three-route offense milestone, the Core could assign a
  dead attacker slot to an existing non-floor Builder; that Builder promoted
  only between routes, so no replacement spawn or opening spend changed.
- The initial rotated 30-game screen (`screen_seed=188`) was **17-13**, below
  the 19-11 floor.  Both sides delivered **30/30**; collection was
  **163,450 vs 172,840 Ti**, max p99/peak was **1,564/6,489 us**, and command,
  TLE, and suspicious-output counts were zero.  Replay counts showed more
  Harvesters but fewer Conveyors, Barriers, and Sentinels for the candidate.
- The one bounded repair deferred the handoff until the three-route milestone.
  Focused coverage stayed **36/36**, compileall passed, smoke was **4/4**, and
  scoped diff-check passed.  The rotated repair screen (`screen_seed=199`)
  regressed to **13-17**, with **30/30** deliveries, **123,940 vs 141,790 Ti**,
  max p99/peak **1,457/2,721 us**, and zero command/TLE/suspicious rows.
- Reject v408.  Temporary source/test/config edits were removed and recursive
  production parity with v0047 is exact.  Rollback focused coverage was
  **36/36**, compileall passed, rollback smoke was **4/4**, and rollback
  `make static` retained the inherited 15 obsolete imports plus two navigation
  assertions.  Evidence: `experiments/v0047-confirmed-attacker-handoff-v408.md`,
  `reports/iter-v408-attacker-handoff/`, `reports/local-20260821T071921Z`, and
  `reports/local-20260821T072452Z`.  No release, package, remote, upload,
  activation, or baseline transition occurred; v0047 remains the baseline.

### v407 Source Harvester Barrier guard rejected — 2026-08-21T09:35:00+02:00

- Compared a narrow source-protection Barrier lease against immutable v0047:
  after the economy threshold, one nearest non-fixed Builder could protect a
  connected friendly Harvester only when a visible enemy Builder was nearby;
  output-side, Core-ring, route-reserve, Store, and task ordering were
  unchanged.
- The broad rotated 30-game screen (`screen_seed=1717`) was **14-16**.  The
  bounded repair reached **19-11** with 30/30 deliveries and collection
  **162,350 vs 164,450 Ti**.  The required 60-game release gate was only
  **31-29**, with 60/60 deliveries and collection **289,390 vs 319,690 Ti**;
  max p99/peak was **1,473/2,117 us**, with zero command/TLE/suspicious rows.
- Focused candidate tests were **29/29**; rollback coverage was **26/26**;
  compileall passed and smoke was **4/4**.  `make static` retained the
  inherited exit-2 profile (15 obsolete imports plus two navigation
  assertions).  Raw release games are `reports/local-20260821T064925Z`;
  diagnostics are under `reports/iter-v407-source-barrier/`.
- Reject v407: the release gate was not a significant, repeatable win-rate
  improvement and collection regressed.  Temporary edits/config were removed;
  recursive production parity with v0047 is exact.  Keep v0047 as baseline;
  no package, remote, upload, activation, or live operation occurred.
  Evidence: `experiments/v0047-source-harvester-barrier-v407.md`.

### v406 Pressure connected-source takeover priority rejected — 2026-08-21T09:10:00+02:00

- Compared a pressure-only connected-source takeover against immutable v0047:
  after five routes and a Core `PRESSURE` signal, one nearest dynamic Builder
  could prefer a visible enemy Harvester with an existing hostile conveyor or
  splitter outlet before local belt repair, only with replacement-route and
  fixed-attack reserves funded. Opening/converting/crisis behavior was
  unchanged.
- The rotated 30-game screen (`screen_seed=1693`) was **14-16**, below the
  19-11 floor.  Candidate/comparator deliveries were **30/29**; collection
  was **119,440 vs 127,250 Ti**; Harvesters/Conveyors placed were
  **249/2,790 vs 243/2,665**; and max p99/peak was **1,294/5,636 us** with
  zero command/TLE/suspicious rows.  Antler, Drakkarfjord, Fjordgate,
  Nordkap, Ragnarok, and Yulerune were candidate 0-2 losses.
- Candidate focused tests were **28/28**; rollback coverage was **26/26**;
  compileall and smoke **4/4** passed.  `make static` retained the inherited
  exit-2 profile.  Raw games are `reports/local-20260821T062203Z`; diagnostics
  are under `reports/iter-v406-pressure-takeover/`.
- Reject v406 without repair.  Temporary edits/config were removed and exact
  recursive production parity with v0047 was confirmed.  Keep v0047 as the
  baseline; no package, remote, upload, activation, or live operation.
  Evidence: `experiments/v0047-pressure-connected-takeover-v406.md`.

### v405 Post-delivery dynamic Core-cage lease rejected — 2026-08-21T08:45:00+02:00

- Compared a narrow late offensive-Barrier lease against immutable v0047:
  after five completed routes, `PRESSURE`, confirmed enemy-Core intel, and an
  observed forward Sentinel, one nearest non-fixed dynamic Builder could claim
  a visible cage site.  Fixed attacker cage, route ordering, Store, spawning,
  ammo, and live policy were unchanged.
- The rotated 30-game screen (`screen_seed=1663`) was **13-17**, below the
  19-11 floor.  Deliveries were **30/30** on both sides; collection was
  **145,760 vs 154,720 Ti**; max p99/peak was **1,378/5,587 us**; and all
  command/TLE/suspicious counts were zero.  Drakkarfjord, Drumlin, Midgard,
  and Nordkap were candidate 0-2 losses; Barrier placements were 166 vs 185.
- Candidate focused tests were **28/28**; rollback coverage was **26/26**;
  compileall and smoke **4/4** passed.  `make static` retained the inherited
  exit-2 profile.  Raw games are `reports/local-20260821T061249Z`; diagnostics
  are under `reports/iter-v405-siege-cage/`.
- Reject v405 without repair.  Temporary edits/config were removed and exact
  recursive production parity with v0047 was confirmed.  Keep v0047 as the
  baseline; no package, remote, upload, activation, or live operation.
  Evidence: `experiments/v0047-siege-cage-lease-v405.md`.

### v404 Preemptive Sentinel beacon response rejected — 2026-08-21T08:25:00+02:00

- Compared a narrow Core-beacon response against immutable v0047: a dynamic
  Builder could claim a Core-visible enemy Sentinel encoded with zero missing
  Core HP before ordinary siege damage.  The beacon writer, route ordering,
  fixed roles, and topology were unchanged.
- The first rotated 30-game screen (`screen_seed=1621`) was **17-13** with
  30/30 deliveries, **145,240 vs 107,000 Ti**, zero command/TLE/suspicious
  rows, and max p99/peak **1,365/3,672 us**.  The independent repeat was
  **13-17** with **30/29** deliveries, **110,100 vs 125,370 Ti**, zero
  command/TLE/suspicious rows, and max p99/peak **1,449/6,165 us**.  The
  repeat's Drakkarfjord, Drumlin, Icefloe, and Yulerune rows were candidate
  0-2 losses.
- Candidate focused coverage was **33/33**; rollback coverage was **26/26**;
  compileall and smoke **4/4** passed.  `make static` retained the inherited
  exit-2 profile.  Raw games are `reports/local-20260821T054731Z` and
  `reports/local-20260821T055101Z`; diagnostics are under
  `reports/iter-v404-preemptive-sentinel/`.
- Reject v404 without repair.  Temporary edits/config were removed and exact
  recursive production parity with v0047 was confirmed.  Keep v0047 as the
  baseline; no package, remote, upload, activation, or live operation.
  Evidence: `experiments/v0047-preemptive-sentinel-v404.md`.

### v403 Economy-before-generic-repair priority rejected — 2026-08-21T08:05:00+02:00

- Compared a phase-scoped task-order change against immutable v0047: opening,
  converting, or crisis dynamic workers chose Harvester/route work before
  generic damaged-building repair, while home threats, belt gaps, hijacks, and
  pressure-phase repair ordering were unchanged.
- The rotated 30-game screen (`screen_seed=1571`) was **12-18**, below the
  19-11 floor.  Deliveries were **30/30** on both sides, max p99/peak was
  **1,372/3,021 us**, collection was **158,770 vs 158,750 Ti**, and
  command/TLE/suspicious counts were zero.  Royale, Fjordgate, Ragnarok, and
  Midgard were protected 0-2 losses.
- Focused tests were **34/34** for the candidate and **32/32** after rollback;
  compileall and smoke **4/4** passed, while static retained the inherited
  exit-2 profile.  Raw games are `reports/local-20260821T053841Z`; diagnostics
  are under `reports/iter-v403-economy-repair-priority/`.
- Reject v403 without repair.  Temporary edits/config were removed and exact
  recursive production parity with v0047 was confirmed.  Keep v0047 as the
  baseline; no package, remote, upload, activation, or live operation.
  Evidence: `experiments/v0047-economy-before-repair-v403.md`.

### v402 Map-aware opening Launcher gate rejected — 2026-08-21T07:45:00+02:00

- Compared a map-aware primary-attacker control gate against immutable v0047:
  the existing one-home Launcher stayed immediate on cramped maps but waited
  for one completed route on longer maps.  Route FSM, Store, spawning,
  dynamic tasks, turret policy, package, upload, activation, and live state
  were out of scope.
- The rotated 30-game screen (`screen_seed=1523`) was **11-19**, below the
  19-11 floor.  Deliveries were **30/30** candidate versus **29/30**
  comparator; collection was **117,970 vs 156,310 Ti**, max p99/peak was
  **1,352/5,032 us**, and command/TLE/suspicious counts were zero.  Frostgate,
  Midgard, Yulerune, Drumlin, Antler, and Valkyrie were protected losses.
- Focused tests were **34/34** for the candidate and **32/32** after rollback;
  compileall passed, smoke was **4/4** at
  `reports/local-20260821T053407Z`, and static retained the inherited exit-2
  profile.  Raw games are `reports/local-20260821T053005Z`; diagnostics are
  under `reports/iter-v402-map-launcher-gate/`.
- Reject v402 without repair.  Temporary edits/config were removed and exact
  recursive production parity with v0047 was confirmed.  Keep v0047 as the
  baseline; no package, remote, upload, activation, or live operation.
  Evidence: `experiments/v0047-map-aware-launcher-gate-v402.md`.

### v401 Post-raid return lease rejected — 2026-08-21T07:25:00+02:00

- Compared a confirmed-raid return-to-Core lifecycle lease against immutable
  v0047.  A dynamic Builder that fired on an enemy logistics target would
  return home before selecting another task; route, Store, spawning, fixed
  roles, turret policy, packaging, and live state were out of scope.
- The rotated 30-game all-map screen (`screen_seed=1471`) was **14-16**, below
  the 19-11 floor.  Deliveries were **30/30** candidate versus **29/30**
  comparator; collection was **141,560 vs 134,870 Ti**, max p99/peak was
  **1,451/6,672 us**, and command/TLE/suspicious counts were zero.  Drumlin,
  Frostgate, Glacierkeep, Ragnarok, and Royale remained protected losses.
- Focused tests were **35/35** for the candidate and **32/32** after rollback;
  compileall passed, smoke was **4/4** at
  `reports/local-20260821T052232Z`, and static retained the inherited exit-2
  profile.  Raw games are `reports/local-20260821T051704Z`; diagnostics are
  under `reports/iter-v401-post-raid-return/`.
- Reject v401 without repair.  Temporary edits/config were removed and exact
  recursive production parity with v0047 was confirmed.  Keep v0047 as the
  baseline; no package, remote, upload, activation, or live operation.
  Evidence: `experiments/v0047-post-raid-return-v401.md`.

### v400 Home-interceptor Launcher pulse rejected — 2026-08-21T07:12:00+02:00

- Compared a reserve-backed defensive Launcher pulse against immutable v0047:
  after five completed routes, the nearest local dynamic Builder could answer
  a visible enemy Builder inside home.  The initial visible cap allowed up to
  two home Launchers (including the opening relay); the bounded repair also
  required the Core's defense designation, target distance squared <=25, and
  round <=240.  No route, Store, spawn, fixed-role, Sentinel, Barrier,
  package, upload, activation, or live-state policy was retained.
- The initial rotated 30-game screen (`screen_seed=1429`) was **17-13** with
  30/30 deliveries and zero command/TLE/suspicious rows; collection was
  **150,050 vs 150,030 Ti**, max p99/peak **1,321/5,707 us**, and Royale
  placed six candidate Launchers after destroyed relays reopened the visible
  cap.  Repair (`screen_seed=1451`) tied **15-15**, stayed 30/30 delivery- and
  runtime-clean, collected **182,140 vs 152,670 Ti**, and limited placements
  to at most two.  Raw matrices are `reports/local-20260821T050118Z` and
  `reports/local-20260821T050624Z`; diagnostics are under
  `reports/iter-v400-home-launcher/`.
- Focused coverage was **35/35** for both attempts and **32/32** after
  rollback; compileall passed; rollback smoke was **4/4** at
  `reports/local-20260821T051053Z`; static retained the inherited exit-2
  profile.  Temporary edits were removed and recursive candidate parity with
  immutable v0047 is exact.  Reject v400, keep v0047 as baseline, and skip
  release, package, remote, upload, activation, and live operations.

### v399 Pressure-capacity recovery lease rejected — 2026-08-21T06:52:00+02:00

- Compared a bounded live-capacity recovery lease against immutable v0047:
  after the historical route counter reached `PRESSURE`, up to two nearest
  non-fixed home-side dynamic Builders could stay on SCOUT/CHAIN work when
  local Harvesters were depleted and the bank could not fund a replacement
  route plus the fixed attack reserve.  Repair 1 narrowed this to zero visible
  local Harvesters.  No route geometry, Store, spawning, combat, package,
  upload, activation, or live-state change was retained.
- Initial rotated 30-game screen (`screen_seed=1361`) was **9–21** with
  30/30 deliveries; Repair 1 (`screen_seed=1373`) was **13–17** with 29/30
  candidate deliveries.  Collection was **128,030 vs 165,800 Ti** initially
  and **124,370 vs 137,680 Ti** after repair.  Both were command-, TLE-, and
  suspicious-clean; raw runs are `reports/local-20260821T044004Z` and
  `reports/local-20260821T044446Z`.
- Focused coverage was **37/37** for both attempts and **36/36** after
  rollback; compileall passed; rollback smoke was **4/4** at
  `reports/local-20260821T044849Z`; static retained the inherited exit-2
  profile.  Temporary edits were removed and recursive candidate parity with
  v0047 is exact.  Reject v399, keep v0047 as baseline, and skip release,
  remote, package, upload, activation, and live operations.  Evidence:
  `experiments/v0047-pressure-recovery-v399.md` and
  `reports/iter-v399-pressure-recovery/`.

### v398 Surplus-aware pressure conversion rejected — 2026-08-21T06:24:00+02:00

- Compared a bounded pressure-phase workforce change against immutable v0047:
  non-steward dynamic Builders could leave visible-ore harvesting only when a
  replacement-route/attack reserve was funded; Repair 1 additionally required
  a larger bank and an actionable loaded-raid or ore-denial target.  No route,
  Store, spawning, combat, package, upload, activation, or live-state change
  was made.
- The initial rotated 30-game screen (`screen_seed=1291`) was **12–18**;
  Repair 1 was **15–15**.  Both delivered 30/30 with zero TLE/suspicious rows,
  but missed the **19–11** promotion floor.  Raw reports are
  `reports/local-20260821T041348Z` and `reports/local-20260821T041830Z`.
- Focused tests were **37/37** for both attempts and **36/36** after rollback;
  compileall passed; rollback smoke was **4/4** at
  `reports/local-20260821T042332Z`; `make static` retained only the inherited
  exit-2 profile.  Temporary edits were removed and recursive candidate parity
  with v0047 is exact.  Reject v398, keep v0047 as baseline, and skip release,
  remote, package, upload, activation, and live operations.  Evidence:
  `experiments/v0047-surplus-pressure-v398.md` and
  `reports/iter-v398-surplus-pressure/`.

### v397 Fixed-role resilience after confirmed Builder loss rejected — 2026-08-21T06:09:00+02:00

- Compared a bounded repair of stale fixed attacker/defender Store slots after
  Core-confirmed Builder death against immutable v0047.  Repair 1 selected a
  nearest known-live economy steward or farthest pressure worker and cleared
  stale chain state on attacker promotion; no Store schema, route geometry,
  package, upload, activation, or live-state change was made.
- The initial all-map 30-game screen was **16–14** (`screen_seed=1183`);
  Repair 1 reached **19–11**, but an independent rotated screen was **17–13**
  (`screen_seed=1229`).  All screens were 30/30 delivery-clean with zero
  TLE/suspicious rows.  The 60-game release gate was **29–31** with 58/60
  candidate deliveries versus 60/60 comparator, below the 33–27 floor; Royale
  was 0–4.  Raw reports: `reports/local-20260821T034711Z`,
  `reports/local-20260821T035218Z`, `reports/local-20260821T035605Z`, and
  `reports/local-20260821T035952Z`.
- Focused tests were **38/38** for both candidate attempts and **36/36** after
  rollback; compileall passed and rollback smoke was **4/4** at
  `reports/local-20260821T040746Z`.  `make static` retained only the inherited
  exit-2 profile.  Temporary edits were removed and recursive candidate parity
  with v0047 is exact.  Reject v397; keep immutable v0047 as baseline and skip
  package, remote, upload, activation, and live operations.  Evidence:
  `experiments/v0047-role-resilience-v397.md` and
  `reports/iter-v397-role-resilience/`.

### v396 Visible route-health orphan repair rejected — 2026-08-21T05:34:00+02:00

- Compared a bounded fully-visible Conveyor-suffix health check against
  immutable v0047.  A visible dead/cyclic suffix could seed one alternate
  first hop through the existing orphan repair; Repair 1 also enabled the
  check in published `PRESSURE`.  Splitters, unseen suffixes, Store schema,
  spawning, combat, prices, package, upload, activation, and live state were
  untouched.
- The initial rotated 30-game all-map screen (`screen_seed=1163`) was
  **15–15**.  Repair 1 (`screen_seed=1171`) reached **17–13**, still below
  the **19–11** promotion floor.  Both were command-, TLE-, and
  suspicious-output-clean; raw reports are
  `reports/local-20260821T031836Z` and `reports/local-20260821T032512Z`.
- Focused coverage was **39/39** for each attempt, rollback coverage was
  **36/36**, compileall passed, and rollback smoke was **4/4** at
  `reports/local-20260821T033007Z`.  `make static` retained only the known
  inherited exit-2 profile.  Temporary source/test/config edits were removed;
  recursive candidate production parity with v0047 is exact.
- Reject v396 after two unsuccessful screens; skip release/remote/package/live
  operations and keep v0047 as baseline.  Replay evidence, including the
  remaining Glacierkeep route-conversion risk, is in
  `experiments/v0047-visible-route-health-v396.md` and
  `reports/iter-v396-route-health/`.

### v395 Pending-route commit before survival flee rejected — 2026-08-21T05:59:00+02:00

- Compared both variants against immutable v0047.  The initial rule let a
  chain Builder commit an adjacent pending Conveyor before fleeing a visible
  turret line; Repair 1 limited that exception to a verified final
  Core-feeding segment.  No Store, spending, spawning, combat, package,
  upload, activation, or live-state change was made.
- The initial rotated all-map 30-game screen (`screen_seed=1103`) was
  **13–17**, with 28/30 candidate deliveries versus 30/30 comparator and zero
  TLE/suspicious rows (max p99/peak 1,340/3,543 us).  Replay review found the
  mid-route commit kept exposed Builders alive for too little route value.
- Repair 1 (`screen_seed=1129`) reached **15–15**, with 29/30 candidate
  deliveries versus 30/30 comparator and zero TLE/suspicious rows (max
  p99/peak 1,246/5,981 us).  Both screens missed the **19–11** promotion
  floor, so no long gate or release operation was run.
- Focused coverage was **33/33** for each attempt, compileall passed, and
  rollback coverage was **32/32**.  `make smoke` was **4/4** after rollback at
  `reports/local-20260821T025903Z`; `make static` retained the inherited
  exit-2 profile.  Temporary source/test/config edits were removed and
  recursive candidate parity with v0047 is exact.  Reject v395; v0047 remains
  the baseline.  Evidence: `experiments/v0047-route-commit-before-flee-v395.md`
  and `reports/iter-v395-route-commit/`.

### v394 Crisis first-hop recovery rejected — 2026-08-21T04:45:00+02:00

- Compared both variants against immutable v0047.  The bounded rule allowed a
  nearby Harvester with a visibly terminal accepting first-hop Conveyor to
  seed one alternate belt only during late `CRISIS`; Repair 1 additionally
  required three historical routes.  No other strategy or live state changed.
- Initial all-map rotated screen (seed 977) was **14–16**; Repair 1 (seed 1031)
  was **12–18**.  Both were **30/30** candidate-delivery and
  command/TLE/suspicious-clean, but both missed the **19–11** promotion floor.
  Raw reports are `reports/local-20260821T023355Z` and
  `reports/local-20260821T023748Z`.
- Focused coverage was **27/27** for each candidate and rollback coverage was
  **32/32**; compileall passed.  Rollback `make smoke` was **4/4** at
  `reports/local-20260821T024137Z`; static retained the inherited exit-2
  profile.  Reject v394 after two repairs, restore exact v0047 parity, and
  skip release/remote/package/live operations.  Full evidence:
  `experiments/v0047-crisis-first-hop-recovery-v394.md` and
  `reports/iter-v394-crisis-first-hop/`.

### v393 Pending-route recovery rejected — 2026-08-21T04:30:00+02:00

- Compared both attempts against immutable v0047.  The bounded change retained
  a pending conveyor obligation after a survival flee and navigated back to it;
  Repair 1 limited that return to four tiles.  No unrelated strategy or live
  state changed.
- Initial all-map rotated screen (seed 887) was **17–13**, with **30/30**
  candidate deliveries and zero command/TLE/suspicious rows.  Repair 1 (seed
  941) was also **17–13**, with **29/30** candidate deliveries; both missed the
  **19–11** promotion floor.  Raw reports are
  `reports/local-20260821T021600Z` and `reports/local-20260821T022012Z`.
- Focused coverage was **27/27** for each attempt and rollback coverage was
  **32/32**; compileall passed.  `make smoke` was **4/4** at
  `reports/local-20260821T022431Z`; static retained the inherited exit-2
  profile.  Reject v393 after two unsuccessful repairs, restore exact v0047
  candidate parity, and skip release/remote/package/live operations.  Full
  evidence: `experiments/v0047-pending-route-recovery-v393.md` and
  `reports/iter-v393-pending-route-recovery/`.

### v392 Pressure-phase economy steward promoted — 2026-08-21T04:04:00+02:00

- Starting from immutable v0046, v392 kept one nearest home-side dynamic
  Builder on SCOUT/CHAIN economy work during healthy `PRESSURE`; forward
  dynamic workers retained raid/denial/advance behavior.  Focused coverage was
  **32/32**, compileall passed, smoke was **4/4**, and static retained only the
  inherited 15 obsolete imports and two navigation assertions.
- Rotated screens against v0046 were **19–11** (seed 797) and **15–15** (seed
  809), both **30/30** delivery-clean and command/TLE/suspicious-clean; the
  pair was **34–26**.  The pinned 60-game gate was **35–25**, with candidate
  delivery **59/60** vs baseline **60/60**, zero command/TLE/suspicious rows,
  max p99/peak **1,310/3,361 us**, and **324,040/237,410 Ti** collection.  One
  Glacierkeep seed-1 no-delivery row remains a follow-up risk.
- The server gate `dbe3b194-6997-4ade-920e-3a211b9a666e` completed **3–2** for
  the candidate.  Package
  `artifacts/submissions/v0047_pressure-economy-steward_20260821-0200_eeafad8f.zip`
  has SHA-256
  `949553700817bbedd2000562a769927fd8a0f05c6849db6f57c86ce7c811e578`.
  Promote v0047 as the new local baseline; no live activation occurred.
  Evidence is under `experiments/v0047-pressure-economy-steward-v392.md` and
  `reports/iter-v392-pressure-steward/`.

### v391 Confirmed-enemy-Core home-Gunner shell rejected — 2026-08-21T06:45:00+02:00

- Starting from immutable v0046, v391 tested an early three-Gunner home shell
  after one completed route and confirmed enemy-Core intel.  The first run
  exposed an undefined route-count local and was invalid at **0–30**; the
  candidate was repaired before strategy evidence was counted.
- Repair 1 passed focused coverage **28/28**, compileall, smoke **4/4**, and
  produced a clean all-map 30-game screen of **13–17** (seed 787), with
  **159,840/191,320 Ti**, **30/30** deliveries, max p99/peak **1,436/5,733 us**,
  and zero TLE/suspicious rows.  Repair 2 excluded fixed attackers from home
  defense designation, passed **29/29**, and scored **12–18** with
  **160,370/157,040 Ti**, **30/30** deliveries, max p99/peak **1,380/4,598 us**,
  and zero TLE/suspicious rows.
- Reject v391 after both bounded repairs; neither valid screen met the 9–6
  floor.  Temporary source/tests/config were removed, rollback coverage was
  **26/26**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260821T013135Z`, and recursive parity with v0046 is empty.
  Static retains the inherited exit-2 profile.  Evidence is under
  `experiments/v0046-confirmed-core-gunner-shell-v391.md` and
  `reports/iter-v391-confirmed-core-shell/`; no promotion or platform operation
  occurred and v0046 remains the best baseline.

### v390 Fixed-attacker Launcher sabotage rejected — 2026-08-21T06:05:00+02:00

- Starting from immutable v0046, v390 let the designated fixed attacker target
  enemy Launchers as a control-denial pulse while dynamic raiders stayed on
  logistics.  Focused coverage was **33/33**, compileall passed, smoke was
  **4/4**, and static retained the inherited candidate import/assertion
  failures.
- The initial rotated all-map 30-game screen (seed 761) was
  command/reliability-clean but **16–14**, collecting **151,080/166,770 Ti**
  and delivering **30/29**; max p99/peak was **1,390/5,415 us** with zero
  TLE/suspicious rows.  Repair 1 kept loaded logistics ahead of Launchers and
  reached **18–12** (seed 769; **156,540/138,530 Ti**, **30/30** deliveries),
  still below the **19–11** floor.  Repair 2 delayed Launcher detours until
  four routes and returned to **16–14** (seed 773; **166,680/157,120 Ti**,
  **30/30** deliveries; max p99/peak **1,426/5,692 us**).
- Reject v390 after the two bounded repairs.  Temporary source/test/config
  edits were removed; rollback coverage was **31/31**, compileall passed,
  rollback smoke was **4/4** at `reports/local-20260821T005947Z`, and
  recursive candidate parity with v0046 is empty.  Evidence is under
  `reports/iter-v390-launcher-sabotage/` with raw runs at
  `reports/local-20260821T004552Z`, `reports/local-20260821T005026Z`, and
  `reports/local-20260821T005433Z`.  No promotion, package, upload,
  activation, or live transition occurred; v0046 remains the best baseline.

### v389 Gunner threat-class rotation priority rejected — 2026-08-21T03:42:00+02:00

- Starting from immutable v0046, v389 changed only home-Gunner target
  acquisition: enemy Sentinels/Launchers/Gunners outranked nearer harmless
  logistics when selecting a new facing.  Focused coverage was **32/32**,
  compileall passed, smoke **4/4**, and static retained only the inherited
  15 obsolete imports and two navigation assertions.
- The rotated all-map 30-game screen (seed 727) was command/reliability-clean
  but tied **15–15** against v0046.  Candidate/baseline collection was
  **114,480/102,230 Ti**, deliveries **30/29**, max p99/peak **1,400/4,930 us**,
  and TLE/suspicious rows were zero.  Reports are under
  `reports/iter-v389-gunner-priority/`; raw games are at
  `reports/local-20260821T003514Z`.
- Reject v389 without a second screen or long gate.  Temporary source/test/
  config edits were removed; rollback coverage was **31/31**, compileall
  passed, rollback smoke **4/4** at `reports/local-20260821T003917Z`, and the
  candidate source is back to exact v0046 parity.  No promotion, package,
  upload, activation, or live transition occurred.

### v388 Core route-health recovery lease rejected — 2026-08-21T02:45:00+02:00

- Starting from immutable v0046, v388 added a Core-published recovery phase
  after the strong-chain milestone when the home end appeared depleted.  One
  nearest dynamic Builder resumed route conversion while fixed attackers and
  the rest of the pressure pool stayed active.  Production scope was limited
  to the economy phase channel and its dynamic lease, with 32/32 focused
  coverage.
- The initial rotated 30-game screen (seed 691) was reliability-clean but
  **16–14**, with **181,180/195,850 Ti** and **30/29** first deliveries.  One
  bounded repair narrowed the trigger to an empty visible home end; its fresh
  screen (seed 709) improved to **17–13**, fixed Glacierkeep to 2–0, and
  collected **139,430/112,660 Ti**, but still missed the **19–11** promotion
  floor.  Repair max p99/peak was **1,369/3,651 us**, with zero TLE/suspicious
  rows.  Reports are under `reports/iter-v388-route-health/` and raw runs are
  `reports/local-20260821T001804Z` and `reports/local-20260821T002346Z`.
- Reject v388 without a second screen or long gate.  Temporary source/test/
  config edits were removed; rollback focused coverage was **31/31**,
  compileall passed, candidate source parity with v0046 is empty, and no
  promotion/package/upload/activation/live transition occurred.  Immutable
  v0046 remains the best baseline.

### v387 pressure-phase local-route recovery rejected — 2026-08-21T02:35:00+02:00

- Starting from immutable v0046, v387 tested a bounded recovery lease based on
  live-v108 losses with only one or two surviving Harvesters.  During healthy
  `PRESSURE`, exactly one nearest home dynamic Builder resumed route work when
  no friendly Harvester was visible in the Core home radius, only with enough
  dynamically priced titanium for a Harvester, two Conveyor links, and the
  fixed attack reserve.  The read-only live capture is preserved at
  `reports/live-continuation-v386-20260820T235823Z`.
- Focused coverage was **32/32**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete imports and two
  navigation assertions.  The rotated all-map 30-game screen
  (`screen_seed=673`) was command-, delivery-, and reliability-clean:
  candidate won **16–14**, both sides delivered **15/15**, average first
  delivery was **22.73/23.73** rounds, and collection was
  **96,720/79,960 Ti** candidate versus baseline.  Max p99/peak was
  **1,406/6,432 us**, with zero TLE/suspicious rows.  Evidence is under
  `reports/iter-v387-local-recovery/` and raw games at
  `reports/local-20260821T000204Z`.
- Reject v387 without a second screen or long gate: 16–14 misses the 19–11
  paired-screen promotion floor despite higher collection.  Temporary
  source/test/config were removed; rollback focused coverage was **31/31**,
  compileall passed, rollback smoke was **4/4** at
  `reports/local-20260821T000627Z`, and recursive parity with immutable v0046
  is empty.  No promotion, package, upload, activation, or live transition
  occurred; v0046 remains the best baseline.

### v386 verified conveyor-path merge rejected — 2026-08-21T02:10:00+02:00

- Starting from immutable v0046, v386 tested a bounded resource-conversion
  change: a pending Harvester chain frontier could merge into an adjacent
  friendly Conveyor only when the complete visible downstream path was owned,
  acyclic, and proven to terminate at our Core.  Unknown paths, Splitters,
  foreign buildings, and cycles kept the conservative route behavior.
- Focused coverage was **33/33**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete imports and two
  navigation assertions.  The rotated all-map 30-game screen
  (`screen_seed=659`) was command-, delivery-, and reliability-clean but
  candidate trailed **7 wins to 9** baseline wins, with four paired games
  losing for both sides.  Collection was **71,800/83,860 Ti** candidate versus
  baseline; first delivery was **15/15** on both sides, averaging
  **23.73/29.93** rounds.  Max p99/peak was **1,243/5,698 us**, with zero
  TLE/suspicious rows.  Evidence is under
  `reports/iter-v386-conveyor-merge/` and raw games at
  `reports/local-20260820T234852Z`.
- Reject v386 without a long gate: safe visible merges did not improve wins and
  reduced collection by 12,060 Ti.  Temporary source/tests/config were
  removed; rollback focused coverage was **31/31**, compileall passed, rollback
  smoke was **4/4** at `reports/local-20260820T235307Z`, and recursive parity
  with immutable v0046 is empty.  No promotion, package, upload, activation,
  or live transition occurred; v0046 remains the best baseline.

### v385 stale forward-Sentinel retirement rejected — 2026-08-21T01:40:00+02:00

- Starting from immutable v0046, v385 tested a bounded unit-reuse policy: the
  owning attacker could destroy a mature forward Sentinel at 10 HP or less
  after preflighting a different legal Core-facing site.  Routes, workforce,
  Store, opening Launcher, Barrier cage, ammo, baseline, and platform policy
  were unchanged.
- Focused coverage was **33/33**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete imports and two
  navigation assertions.  The rotated 15-map/30-game seed-647 screen was
  command-, delivery-, and reliability-clean but **15–15**, with
  **138,160 vs 173,590 Ti** collected, **30/30** deliveries on both sides,
  zero TLE/suspicious rows, and max p99/peak **1,350/2,508 us**.  Candidate
  survivors were **203 Harvesters/45 Sentinels** versus **208/34** for v0046.
  Reports are under `reports/iter-v385-sentinel-retirement/` and raw games at
  `reports/local-20260820T233341Z`.
- Reject v385 without the long gate: more Sentinels did not improve wins and
  cost 35,430 Ti of collection.  Temporary source/tests/config were removed;
  rollback focused coverage was **31/31**, compileall passed, rollback smoke
  was **4/4** at `reports/local-20260820T233832Z`, and recursive parity with
  immutable v0046 is empty.  No promotion, package, upload, activation, or
  live transition occurred.

### v384 liquidity-backed late workforce expansion rejected — 2026-08-21T01:20:00+02:00

- Starting from immutable v0046, v384 gated the existing late Builder target
  on five completed routes, a fresh income heartbeat, and a 250-Ti liquidity
  floor.  Focused coverage was **32/32**, compileall passed, smoke **4/4**,
  and static retained only the inherited 15 obsolete imports and two
  navigation assertions.
- Rotated all-map screens were **19–11** (seed 599) and **20–10** (seed 613),
  both 30/30 delivery-clean with zero TLE/suspicious rows.  Candidate versus
  baseline collection was **153,640/128,480 Ti** and **160,350/150,150 Ti**.
- The complete 60-game endpoint-seed gate regressed to **29–31**.  Candidate
  delivered **60/60 vs 58/60**, but collected **312,030/320,120 Ti** and had
  fewer surviving Harvesters/Sentinels (**398/63 vs 423/81**); max p99/peak
  was **1,542/5,867 us**.  The one bounded 350-Ti repair tied **15–15** and
  collected **127,220/141,240 Ti**.  Reports are under
  `reports/iter-v384-late-workforce/` with raw runs at
  `reports/local-20260820T225934Z`, `reports/local-20260820T230318Z`,
  `reports/local-20260820T230731Z`, and `reports/local-20260820T231547Z`.
- v384 was rejected; temporary source/test/config edits were removed,
  rollback focused coverage was **31/31**, compileall passed, rollback smoke
  was **4/4** at `reports/local-20260820T231949Z`, and candidate parity with
  immutable v0046 is empty.  No promotion, package, upload, activation, or
  live transition occurred.

### v383 post-ramp five-Builder replenishment rejected — 2026-08-20T23:58:00+02:00

- Starting from immutable v0046, v383 waived the Core's normal spawn reserve
  after the initial ramp while living Builders were below five.  Route,
  economy phase, combat, Store, baseline, and platform policy stayed unchanged.
- Focused nearest-defense coverage was **27/27**, economy-phase **5/5**,
  compileall passed, smoke was **4/4**, and static retained the inherited 15
  obsolete-module imports plus two navigation assertions.  The rotated
  all-15-map/30-game screen (`screen_seed=583`) was command-clean but only
  **13–17**, with **29/30 vs 30/30** deliveries and **121,170 vs 151,160 Ti**;
  placed/alive Builders/Harvesters were **235/172 vs 265/212**.  TLE and
  suspicious rows were zero; max p99/peak was **1,432/3,732 us**.  Reports:
  `reports/iter-v383-replenishment/` and `reports/local-20260820T224541Z`.
- The candidate was rejected without a second screen, release, package,
  upload, activation, or live operation.  Temporary source/test/config edits
  were removed; rollback focused coverage was **27/27**, compileall passed,
  rollback smoke was **4/4** at `reports/local-20260820T224918Z`, and the
  recursive candidate parity proof is empty at
  `reports/iter-v383-replenishment/rollback-source-parity.diff`.  Immutable
  v0046 remains the baseline.

### v382 wall-aware visible-frontier navigation rejected — 2026-08-20T23:55:00+02:00

- Starting from immutable v0046, v382 changed only the visible navigation
  frontier: a reachable BFS path-length plus Manhattan-remainder score was
  tested against the old Euclidean-only selection.  A deterministic
  wall-corridor test covered the new behavior; economy, route, roles, combat,
  Store, baseline, and platform policy stayed unchanged.
- Targeted coverage passed **3/3**, nearest-defense **26/26**, compileall
  passed, smoke was **4/4**, and `make static` retained the inherited 15
  obsolete-module imports plus two navigation assertions.  The rotated
  all-15-map/30-game screen (`screen_seed=571`) was command-clean but only
  **13–17** against v0046, with **29/30 vs 30/30** deliveries and
  **144,740 vs 166,860 Ti**; TLE/suspicious rows were zero and max p99/peak
  was **1,247/2,621 us**.  Reports: `reports/iter-v382-wall-aware/` and
  `reports/local-20260820T223504Z`.
- The candidate was rejected without a second screen, release, package,
  upload, activation, or live operation.  Temporary source/test/config edits
  were removed; rollback focused coverage was **26/26**, compileall passed,
  rollback smoke was **4/4** at `reports/local-20260820T223858Z`, and the
  recursive candidate parity proof is empty at
  `reports/iter-v382-wall-aware/rollback-source-parity.diff`.  Immutable v0046
  remains the baseline.

### v381 Sabotage-first attacker ordering rejected — 2026-08-20T00:35:00+02:00

- Starting from immutable v0046, v381 moved the fixed attacker's enemy
  logistics raid before its enemy-Core Barrier cage, matching the intended
  resource-interruption ordering.  Route, Store, Sentinel, Launcher, dynamic
  workforce, baseline, and live policy were unchanged.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete-module imports plus two navigation
  fast-path assertions.  The rotated all-15-map/30-game screen
  (`screen_seed=559`) was command- and delivery-clean but **16–14**, with
  30/30 first deliveries, zero TLE/suspicious rows, **111,230 Ti** candidate
  collection, and max p99/peak **1,590/3,081 us**.  Evidence is under
  `reports/iter-v381-sabotage-first/` and
  `reports/local-20260820T221235Z`.
- The first-screen promotion floor failed, so no second screen, release
  matrix, package, upload, activation, or live transition ran.  The temporary
  ordering and focused test were removed; rollback focused coverage was
  **27/27**, compileall passed, rollback smoke **4/4** at
  `reports/local-20260820T221702Z`, and candidate parity with immutable v0046
  is empty.  Immutable v0046 remains the baseline.

### v380 Core-payback ore ranking rejected — 2026-08-20T00:15:00+02:00

- Starting from immutable v0046, v380 ranked visible uncovered ore by shortest
  profitable Core route before local Builder travel distance, retaining all
  existing claim, danger, blacklist, and harvest-range guards.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  The all-15-map/30-game screen (`screen_seed=547`) was
  command-clean but **14–16**, with 29/30 candidate first deliveries,
  zero TLE/suspicious rows, and **141,680 Ti** candidate collection.  Evidence
  is under `reports/iter-v380-core-payback-ore/` and
  `reports/local-20260820T220148Z`.
- The first-screen floor failed, so no second screen, release matrix, or
  platform operation ran.  The temporary source/test/config was removed;
  rollback focused coverage was **26/26**, compileall passed, rollback smoke
  **4/4** at `reports/local-20260820T220516Z`, and candidate parity with v0046
  is empty.  Immutable v0046 remains the baseline.

### v379 Occupied chain-frontier repoint rejected — 2026-08-20T00:05:00+02:00

- Starting from immutable v0046, v379 let a chain repair an occupied friendly
  Conveyor at its pending frontier when the existing belt visibly faced the
  wrong way.  Ownership, dynamic price, adjacency, destroy, and rebuild
  checks were required; foreign buildings and arbitrary joins stayed blocked.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  The all-15-map/30-game screen (`screen_seed=533`) was
  command-clean but **15–15**, with 30/30 deliveries, zero TLE/suspicious
  rows, and **163,420 Ti** candidate collection.  Evidence is under
  `reports/iter-v379-chain-repoint/` and
  `reports/local-20260820T215233Z`.
- The first-screen floor failed, so no second screen, release matrix, or
  platform operation ran.  The temporary source/test/config was removed;
  rollback focused coverage was **26/26**, compileall passed, rollback smoke
  **4/4** at `reports/local-20260820T215714Z`, and candidate parity with v0046
  is empty.  Immutable v0046 remains the baseline.

### v378 Core-ring sink join rejected — 2026-08-20T23:55:00+02:00

- Starting from immutable v0046, v378 allowed a pending route Conveyor to feed
  into a visible friendly Conveyor only when that belt's output was verified
  to enter the Core directly.  Arbitrary joins, BFS, workforce, combat,
  Store, and baseline policy stayed unchanged.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  The all-15-map/30-game screen (`screen_seed=521`) was
  command-clean but **9–21**, with **106,330 Ti** candidate collection and no
  delivery/TLE/suspicious rows.  Evidence is under
  `reports/iter-v378-core-ring-sink/` and
  `reports/local-20260820T214409Z`.
- The first-screen floor failed decisively, so no second screen, release
  matrix, or platform operation ran.  The temporary source/test/config was
  removed; rollback focused coverage was **26/26**, compileall passed,
  rollback smoke **4/4** at `reports/local-20260820T214732Z`, and candidate
  parity with v0046 is empty.  Immutable v0046 remains the baseline.

### v377 Witnessed early Sentinel shell rejected — 2026-08-20T23:50:00+02:00

- Starting from immutable v0046, v377 allowed one extra early forward Sentinel
  only after a live first Sentinel was observed and a dynamic reserve still
  covered that Sentinel plus one Harvester and two Conveyor links.  Route,
  workforce, Launcher, Barrier, and Store policies stayed unchanged.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  The rotated all-15-map/30-game screen (`screen_seed=503`) was
  **15–15**, with 30/30 deliveries, zero command failures/TLE/suspicious rows,
  and **155,840 Ti** candidate collection.  Evidence is under
  `reports/iter-v377-witnessed-early-sentinel/` and
  `reports/local-20260820T213456Z`.
- The 9–6 first-screen floor failed, so no second screen, release matrix, or
  platform operation ran.  The temporary source/test/config was removed;
  rollback focused coverage was **26/26**, compileall passed, rollback smoke
  **4/4** at `reports/local-20260820T213908Z`, and candidate parity with v0046
  is empty.  Immutable v0046 remains the baseline.

### v376 Sentinel guard Barrier rejected — 2026-08-20T23:35:00+02:00

- Starting from immutable v0046, v376 allowed one nearby escape-safe Barrier
  after a forward Sentinel was observed alive for one round.  It required a
  Harvester reserve and left route, ammo, pool, and baseline policy unchanged.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  Screen 1 (`screen_seed=487`) was **19–11**; screen 2
  (`screen_seed=491`) was **7–23**.  Both were command- and delivery-clean;
  evidence is under `reports/iter-v376-sentinel-guard-barrier/`, with raw
  runs at `reports/local-20260820T211932Z` and
  `reports/local-20260820T212334Z`.
- The paired result **26–34** failed the 19–11 promotion floor.  The candidate
  collected **130,720 Ti** on screen 2 and averaged 5.33 Harvesters and 0.83
  Sentinels; no release matrix or platform action was justified.
- The temporary source/test/config was removed.  Rollback focused coverage was
  **26/26**, compileall passed, rollback smoke **4/4** at
  `reports/local-20260820T212759Z`, and candidate parity with v0046 is empty.
  Immutable v0046 remains the baseline.

### v375 Secondary-attacker siege relay rejected — 2026-08-20T23:45:00+02:00

- Starting from immutable v0046, v375 allowed only the designated secondary
  fixed attacker to answer a non-crisis Core siege beacon.  The primary
  attacker, route owners, and dynamic workforce retained their current lanes;
  crisis handling was unchanged.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited failures.  The rotated 15-map/30-game screen
  (`screen_seed=479`) was command- and delivery-clean with zero TLE/suspicious
  rows but regressed to **10–20**.  Candidate collected **153,820 vs
  194,560 Ti**, with average surviving Harvesters **6.63 vs 7.53** and
  Sentinels **0.80 vs 1.87**.  Evidence is under
  `reports/iter-v375-secondary-siege-relay/` and
  `reports/local-20260820T210907Z`.
- The 9–6 floor failed, so no second screen or release matrix ran.  Temporary
  source/test/config were removed; rollback focused coverage was **26/26**,
  compileall passed, and smoke **4/4** at
  `reports/local-20260820T211301Z`.  Candidate parity with immutable v0046 is
  empty.  No promotion, package, upload, activation, or live transition
  occurred.

### v374 Late mirrored-Core Sentinel fallback rejected — 2026-08-20T23:25:00+02:00

- Starting from immutable v0046, v374 allowed only the primary fixed attacker
  to place one late Sentinel at the rotationally mirrored Core estimate after
  five completed routes and a shared `PRESSURE` phase without direct Core
  intel.  A replacement Harvester plus two Conveyor links stayed reserved and
  the fallback was one-shot.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and
  `make static` retained only the inherited failures.  The rotated 15-map,
  30-game screen (`screen_seed=467`) was **15–15**, with zero command/TLE/
  suspicious-output rows; candidate delivered 29/30 versus 30/30 and
  collected **117,390 vs 132,130 Ti**.  Average surviving Sentinels were
  **1.10 vs 1.93**.  Diagnostics are under
  `reports/iter-v374-late-mirrored-sentinel/` and
  `reports/local-20260820T205940Z`.
- The 9–6 first-screen floor failed, so no second screen or release matrix
  ran.  Temporary source/test/config were removed; rollback focused coverage
  was **26/26**, compileall passed, and smoke **4/4** at
  `reports/local-20260820T210338Z`.  Candidate parity with immutable v0046 is
  empty.  No promotion, package, upload, activation, or live transition
  occurred.

### v373 Heartbeat-gated siege ammo rejected — 2026-08-20T23:05:00+02:00

- Starting from immutable v0046, v373 limited the large siege ammo buffer to a
  recent-income `PRESSURE` phase while retaining the normal ammo floor/small
  buffer.
- Focused coverage was **27/27**, compileall passed, smoke **4/4**, and static
  retained only the inherited failures.  The first rotated 30-game all-map
  screen (`screen_seed=461`) was **14–16**, with all deliveries and runtime
  rows clean; collection was **135,430 vs 145,190 Ti**.
- The 9–6 floor failed, so no second screen or release matrix ran.  Evidence is
  under `reports/iter-v373-heartbeat-siege-ammo/` and
  `reports/local-20260820T204643Z`.
- v373 was rolled back to exact v0046 parity; no baseline, package, upload,
  activation, or live-state transition occurred.

### v372 Damaged-Harvester repair priority rejected — 2026-08-20T22:45:00+02:00

- Starting from immutable v0046, v372 prioritized repair of a visible damaged
  friendly Harvester ahead of enemy-Harvester hijack; no other production
  policy changed.
- Focused coverage was **27/27**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained only the inherited 15 obsolete imports plus two
  navigation assertions.  Rotated screens were **18–12** (seed 443) and
  **15–15** (seed 449), combined **33–27**, with clean deliveries and runtime.
- The v0046-pinned 60-game gate was command-clean and delivery-complete but
  regressed **25–35**; collected titanium was **279,900 vs 327,020** and mean
  first delivery **34.05 vs 26.52** rounds.  Evidence is under
  `reports/iter-v372-damaged-harvester-priority/` and
  `reports/local-20260820T203356Z`.
- v372 was rejected and rolled back to exact v0046 parity.  No baseline,
  package, upload, activation, or live-state transition occurred.

### v371 Orphan-only opening hijack rejected — 2026-08-20T23:05:00+02:00

- Starting from immutable v0046, v371 allowed opening hijack only for a
  visible enemy Harvester with no friendly Conveyor/Splitter outlet; connected
  sources remained pressure-gated.
- Focused coverage was **37/37**, compileall passed, and the 15-map/30-game
  paired screen (`screen_seed=431`) was **12-18**, with zero command failures
  and no delivery, TLE, or suspicious-output failures. Replay diagnostics are
  under `reports/local-20260820T201314Z/analysis.json`; the 9-6 first-screen
  floor failed.
- The candidate was rolled back to exact v0046 parity; rollback focused
  coverage was **35/35**, smoke **4/4** at
  `reports/local-20260820T201857Z`, and parity is recorded in
  `reports/local-20260820T201314Z/rollback-source-parity.diff`.
- `make static` retained only the inherited 15 obsolete-module imports and two
  navigation fast-path assertions. No release, upload, activation, or live
  baseline transition ran. Next: investigate a distinct endgame/resource-
  conversion or defensive-mechanic hypothesis against v0046.

### v370 Route-priority hijack gating rejected — 2026-08-20T22:45:00+02:00

- Starting from immutable v0046, v370 moved dynamic enemy-Harvester hijacking
  below the economy task during opening/converting/crisis, while retaining
  hijack in pressure when no local ore was available.
- Focused coverage was **37/37**, compileall passed, and the 15-map/30-game
  paired screen (`screen_seed=419`) was **14-16**, with zero command failures
  and no delivery, TLE, or suspicious-output failures. Replay diagnostics are
  under `reports/local-20260820T200558Z/analysis.json`; the first-screen 9-6
  floor failed.
- The candidate was rolled back to exact v0046 parity; rollback focused
  coverage was **35/35**, smoke **4/4** at
  `reports/local-20260820T200958Z`, and parity is recorded in
  `reports/local-20260820T200558Z/rollback-source-parity.diff`.
- `make static` retained only the inherited 15 obsolete-module imports and two
  navigation fast-path assertions. No release, upload, activation, or live
  baseline transition ran. Next: choose a distinct resource-to-pressure or
  defensive response hypothesis against v0046.

### v369 Dynamic Sentinel ownership rejected — 2026-08-20T22:25:00+02:00

- Starting from immutable v0046, v369 stopped dynamic Builders from buying
  forward Sentinels so fixed attackers alone owned the shared siege pool;
  dynamic workers remained on routes, repairs, hijacks, raids, and harassment.
- Focused coverage was **36/36**, compileall passed, and the 15-map/30-game
  paired screen (`screen_seed=413`) was **15-15**, with zero command failures
  and no delivery, TLE, or suspicious-output failures. Replay diagnostics are
  under `reports/local-20260820T195648Z/analysis.json`.
- Fixed attackers still produced replacement churn in some losses, so the
  ownership rule had no aggregate edge. The candidate was rolled back to exact
  v0046 parity; rollback focused coverage was **35/35**, smoke **4/4** at
  `reports/local-20260820T200226Z`, and parity is recorded in
  `reports/local-20260820T195648Z/rollback-source-parity.diff`.
- `make static` retained only the inherited 15 obsolete-module imports and two
  navigation fast-path assertions. No release, upload, activation, or live
  baseline transition ran. Next: test a distinct route-throughput/resource
  conversion hypothesis against v0046.

### v368 Reactive home Barrier response rejected — 2026-08-20T22:10:00+02:00

- Starting from immutable v0046, v368 tested one owner-only reactive Barrier:
  the permanent Defender could build one cheap home choke before three paying
  routes, only for a visible enemy Builder/turret inside the existing home
  radius and only with a dynamic Harvester plus two conveyor links reserved.
  The one bounded repair narrowed the trigger to enemy Builders because the
  existing v0046 turret/siege response already handles visible turrets.
- Initial focused coverage was **38/38**, compileall passed, smoke **4/4**, and
  static retained only the inherited 15 obsolete-module imports and two
  navigation assertions.  Screen 1 (`screen_seed=401`) was **9-6**, all 15
  candidate rows delivered, zero TLE/suspicious rows, max p99/peak
  **1,207/4,876 us**.  Screen 2 (`screen_seed=409`) was **7-8**, also
  delivery/reliability-clean, max p99/peak **1,374/2,773 us**; pair **16-14**.
- The repair passed **39/39**, compileall, and smoke **4/4**, but screen 2 fell
  to **6-9** (all deliveries, zero TLE/suspicious, max p99/peak
  **1,197/2,181 us**); repaired pair **15-15**.  v368 is rejected and rolled
  back.  No release matrix, remote gate, package, upload, activation, or live
  baseline change ran.
- Exact v0046 parity and rollback checks are recorded under
  `reports/iter-v368-reactive-home-barrier/`; screen reports are
  `reports/local-20260820T193344Z`, `reports/local-20260820T193600Z`, and
  `reports/local-20260820T193904Z`.

### v367 Deterministic Core spawn ordering rejected — 2026-08-20T21:25:00+02:00

- Starting from immutable v0046, v367 replaced only the Core's unseeded
  `random.shuffle` over the existing legal spawn ring with a deterministic
  round-robin cursor.  The ring geometry, role contract, route/economy/combat
  policy, baseline, and live policy stayed unchanged.
- Focused deterministic/economy/seeded/defense coverage was **37/37**,
  compileall passed, the initial smoke was **4/4** command-clean, and
  `make static` retained only the inherited 15 obsolete-module imports and two
  navigation assertions.  Screen 1 (`screen_seed=347`) was **5-10** with
  15/15 candidate deliveries, zero TLE/suspicious rows, max p99 1195 us, and
  max peak 4250 us, so the 9-6 first-screen floor failed and no repair or
  second screen ran.
- v367 is rejected and rolled back.  Candidate source was restored to exact
  recursive v0046 parity (empty proof at
  `reports/iter-v367-deterministic-spawn-order/rollback-source-parity.diff`);
  the temporary test/config were removed.  Rollback focused tests were
  **35/35**, compileall passed, rollback smoke was **4/4**, and no release
  matrix, remote gate, package, upload, activation, or baseline update ran.
  Reports: `reports/iter-v367-deterministic-spawn-order/`,
  `reports/local-20260820T191002Z`, and `reports/local-20260820T191211Z`.
- As a variance control, immutable v0046 played itself on the identical
  `screen_seed=347` schedule and scored **6-9**, with 15/15 deliveries and
  **77,190 vs 86,160 Ti** across the two identical process roles.  This
  confirms the one-sided quick screen is noisy, but it does not rescue v367's
  5-10 result or justify changing the comparator.  Control evidence is
  `reports/local-20260820T192137Z` and
  `reports/iter-v367-deterministic-spawn-order/control-screen347-analysis.json`.

### v366 Verified route joins rejected — 2026-08-20T21:15:00+02:00

- Starting from immutable v0046, v366 tested a conservative route-conversion
  change: after one completed route, a pending chain tile could join a visible
  friendly conveyor only when a bounded orientation walk reached the Core;
  splitters, cycles, unknown tiles, wrong-team buildings, and pre-milestone
  joins were rejected.  Opening, economy, combat, Store, baseline, and live
  policy otherwise stayed unchanged.
- Focused coverage was **39/39**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete-module imports and two
  navigation assertions.  Screen 1 (`screen_seed=331`) was **2-13** with
  15/15 candidate deliveries and zero TLE/suspicious rows, so the first-screen
  floor failed and no repair or second screen ran.
- v366 is rejected and rolled back.  Candidate source was restored to exact
  recursive v0046 parity (empty proof at
  `reports/iter-v366-verified-route-joins/rollback-source-parity.diff`);
  temporary route-join test/config were removed.  Rollback focused tests were
  **35/35**, compileall passed, rollback smoke was **4/4**, and no release
  matrix, remote gate, package, upload, activation, or baseline update ran.
  Reports: `reports/iter-v366-verified-route-joins/` and
  `reports/local-20260820T185908Z`.

### v365 Radial frontier probes rejected — 2026-08-20T21:00:00+02:00

- Starting from immutable v0046, v365 replaced only the first no-intel
  exploration calls with a deterministic cardinal/diagonal frontier ring;
  the original stride explorer, route/economy/combat policy, Store, baseline,
  and live policy remained unchanged.
- Focused coverage was **38/38** before and after the one bounded repair;
  compileall passed, smoke was **4/4** on both passes, and `make static`
  retained only the inherited 15 obsolete-module imports and two navigation
  assertions.  Screen 1 (`screen_seed=307`) was **5-10** with 15/15 candidate
  deliveries and zero TLE/suspicious rows.  The repair reduced the ring to one
  four-tile probe; screen 2 (`screen_seed=317`) was **6-9** with 15/15
  deliveries and zero TLE/suspicious rows.  The pair was **11-19**, failing
  the **19-11** gate.
- v365 is rejected after its one repair.  Candidate source was restored to
  exact recursive v0046 parity (empty proof at
  `reports/iter-v365-radial-frontier-probes/rollback-source-parity.diff`);
  temporary source/tests/configs were removed.  Rollback focused tests were
  **35/35**, compileall passed, rollback smoke was **4/4**, and no release
  matrix, remote gate, package, upload, activation, or baseline update ran.
  Reports: `reports/iter-v365-radial-frontier-probes/`,
  `reports/local-20260820T184802Z`, and `reports/local-20260820T185058Z`.

### v364 Spawn-side opening lanes rejected — 2026-08-20T20:45:00+02:00

- Starting from immutable v0046, v364 gave the first no-intel prospecting
  calls a short cardinal lane based on each Builder's actual spawn side
  relative to the Core, then returned to the unchanged frontier explorer.
  No route, economy, combat, Store, map literal, baseline, or live policy was
  changed.
- Focused coverage was **39/39** before and after the one bounded repair;
  compileall passed, smoke was **4/4** on both passes, and `make static`
  retained only the inherited 15 obsolete-module imports and two navigation
  assertions.  Screen 1 (`screen_seed=281`) was **8-7** with 15/15 candidate
  deliveries and zero TLE/suspicious rows.  The repair shortened the lane
  budget from four to two calls; screen 2 (`screen_seed=293`) was **7-8** with
  15/15 deliveries and zero TLE/suspicious rows.  The pair was **15-15**, so
  v364 missed the **19-11** promotion gate.
- v364 is rejected after its one repair.  Candidate source was restored to
  exact recursive v0046 parity (empty proof at
  `reports/iter-v364-spawn-side-opening-lanes/rollback-source-parity.diff`);
  temporary source/tests/configs were removed.  Rollback focused tests were
  **35/35**, compileall passed, rollback smoke was **4/4**, and no release
  matrix, remote gate, package, upload, activation, or baseline update ran.
  Reports: `reports/iter-v364-spawn-side-opening-lanes/`,
  `reports/local-20260820T183415Z`, and `reports/local-20260820T183826Z`.

### v363 Core-side opening prospecting rejected — 2026-08-20T20:35:00+02:00

- Starting from immutable v0046, v363 tested bounded deterministic cardinal
  waypoints from the own Core toward a strongly outer-board direction when no
  visible or advertised ore existed.  Builder id/cursor rotation, distance
  progression, visible blocker checks, and the existing grid fallback were
  kept deterministic; no economy, route, combat, Store, baseline, or live
  policy changed.
- Focused coverage was **39/39** initially and **40/40** after the one bounded
  repair.  Compileall passed, both smoke runs were **4/4** command-clean, and
  `make static` retained only the inherited 15 obsolete imports plus two
  navigation fast-path assertions (exit 2).  Screen 1 (seed 263) was **7-8**
  with 15/15 positive candidate collection rows at
  `reports/local-20260820T181133Z`.
- The repair tightened outer-ray eligibility for half-cell centre ties.
  Screen 2 (seed 271) reached **9-6** at
  `reports/local-20260820T181729Z`, but had one candidate no-delivery row.
  The pair was **16-14**, failing both the **19-11** pair gate and the hard
  delivery gate.  Screen replays and diagnostics are under
  `reports/iter-v363-home-side-prospecting/`.
- v363 is rejected after its one repair.  Candidate source was restored to
  exact recursive v0046 parity (empty proof at
  `reports/iter-v363-home-side-prospecting/rollback-source-parity.diff`);
  rollback focused/compileall/smoke passed, with rollback smoke at
  `reports/local-20260820T182055Z`.  No 60-game matrix, remote gate, package,
  upload, activation, or baseline update ran.

### v362 compact loaded-raid handoff rejected — 2026-08-20T20:00:00+02:00

- Starting from immutable v0046 and fresh v108 replay evidence, v362 let one
  nearest dynamic Builder raid visible loaded enemy logistics during compact
  `CONVERTING` phase after the three-route threshold.  The one bounded repair
  required a dynamically priced Harvester plus two conveyor links to remain
  available in addition to the attack reserve, preventing the raid from
  consuming route liquidity.
- Focused coverage was **33/33** before and after repair, compileall passed,
  smoke was **4/4**, and static retained only the inherited 15 obsolete
  imports plus two navigation assertions.  Seed-233 scored **10-5** with
  15/15 deliveries; seed-239 scored **9-6** with 14/15 deliveries.  The pair
  was **19-11** and both screens were command/TLE/suspicious-clean, but Royale
  seed 43 had no candidate delivery and therefore failed the hard delivery
  gate.
- v362 is rejected after its one allowed repair.  Candidate source was restored
  exactly to immutable v0046 (empty parity proof at
  `reports/iter-v362-compact-pressure-loaded-raid/rollback-source-parity.diff`);
  the temporary source/test/config were removed.  Rollback checks passed; no
  release matrix, remote gate, package, upload, activation, or baseline update
  ran.  Reports: `reports/iter-v362-compact-pressure-loaded-raid/`,
  `reports/local-20260820T174114Z`, `reports/local-20260820T174552Z`, and
  `reports/local-20260820T174753Z`.

### v361 designated-defense action order rejected — 2026-08-20T19:35:00+02:00

- Starting from exact v0046, v361 gave the Core-designated Defender a bounded
  chance to build its legal home Gunner before a new Harvester.  One repair
  required a dynamically priced Harvester plus two conveyor links to remain in
  reserve; the old Gunner fallback and all placement guards stayed intact.
- Focused coverage was **32/32**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  The initial rotated screen at
  `reports/local-20260820T171547Z` was **5-10**; the repaired screen at
  `reports/local-20260820T172138Z` improved to **8-7**, but missed the **9-6**
  first-screen floor.  Both were command/TLE/suspicious/delivery-clean; the
  repaired screen had zero TLEs/suspicious rows, all 15 candidate deliveries,
  and maximum p99/peak **1,333/3,174 us**.
- v361 is rejected after its one allowed repair.  Candidate production source
  was restored exactly to immutable v0046 (empty parity proof at
  `reports/iter-v361-designated-defense-action-order/rollback-source-parity.diff`);
  rollback focused coverage was **31/31**, compileall passed, and rollback
  smoke was **4/4**.  No second screen, release matrix, remote gate, package,
  upload, activation, or baseline update ran.

### v360 pressure-phase home-defense shell rejected — 2026-08-20T19:20:00+02:00

- Starting from exact v0046, v360 used the existing healthy `PRESSURE` phase to
  raise the home-Gunner target to the existing five-unit lifetime cap even
  without a visible enemy, preserving dynamic prices, route-tile exclusions,
  and one-builder designation.  The repair kept one Harvester plus two
  conveyor links reserved while forming that shell.
- Focused coverage was **32/32**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions.  The first rotated v0046 screen was **7-8** at
  `reports/local-20260820T170539Z`; the repaired screen was **6-9** at
  `reports/local-20260820T170802Z`.  Both were reliability- and delivery-clean.
- v360 is rejected after one bounded repair.  Candidate source was restored
  exactly to immutable v0046 (empty parity proof at
  `reports/iter-v360-pressure-phase-home-defense/rollback-source-parity.diff`);
  rollback focused coverage was **31/31**, rollback smoke **4/4** at
  `reports/local-20260820T171057Z`, and compileall passed.  No release matrix,
  remote gate, baseline update, package, upload, or activation ran.

### v359 healthy-pressure workforce handoff rejected — 2026-08-20T19:05:00+02:00

- Fresh v108 observation remained active at rating **1564.21**, rank **42/129**,
  with a recent **5-5** record.  Downloaded loss/top-team samples are under
  `reports/live-v108-followup-20260820T164909Z/`; they show both
  one-to-two-Harvester no-delivery openings and long games with 20+ Harvesters
  and hundreds of Conveyors but too little combat conversion.
- v359 made the Core's healthy `PRESSURE` phase a real dynamic-worker handoff:
  after five completed routes and a recent income heartbeat, workers stopped
  chasing arbitrary visible ore and used the existing raid/defense/advance
  ladder.  Opening/converting/crisis and low-liquidity recovery stayed intact.
  The one repair kept the Core-designated defender in the normal Defender FSM
  so home Gunner/repair work was not skipped.
- Focused coverage was **32/32** initially and **33/33** after repair;
  compileall passed.  The initial v0046-pinned rotated screen was **6-9** at
  `reports/local-20260820T165529Z`; the repaired screen was **8-7** at
  `reports/local-20260820T165810Z`.  Both were command/TLE/suspicious/
  delivery-clean, but the combined **14-16** missed the **19-11** gate.
- v359 is rejected after the one bounded repair.  Candidate source was restored
  exactly to immutable v0046 (empty parity proof at
  `reports/iter-v359-healthy-pressure-handoff-v359/rollback-source-parity.diff`);
  rollback focused coverage was **31/31**, rollback smoke **4/4** at
  `reports/local-20260820T170039Z`, and compileall passed.  `make static` is
  still the inherited exit 2 (15 obsolete imports plus two navigation
  assertions).  No release matrix, remote gate, baseline update, package,
  upload, or activation ran.

### v358 archival long gate confirmed rejection — 2026-08-20T18:45:00+02:00

- At the user's request, the exact v358 source was reconstructed from the
  archived patch sequence in an isolated `/tmp` bot; `bots/candidate` stayed
  recursively identical to immutable v0046.  The explicit 60-game,
  v0046-pinned all-map/both-side gate is recorded at
  `reports/local-20260820T163725Z` and source evidence at
  `reports/iter-v358-wall-exit-target-gating/v358-reconstructed-source.diff`.
- v358 scored **30-30**, below the **33-27** release floor.  It was
  reliability-clean: 60/60 command-clean, 60/60 candidate deliveries, zero
  TLEs, zero suspicious rows, max p99/peak **1,414/5,123 us**.  Collection was
  **331,420 vs 346,570 Ti** (v358 vs v0046); Yulerune was **0-4** while Midgard
  was **4-0**.  The earlier 9-6 screen therefore did not generalize, so no
  remote gate, package, upload, activation, or promotion is justified.
- Post-gate checks on the untouched repository candidate were `make smoke`
  **4/4** command-clean (`reports/local-20260820T164656Z`) and `make static`
  exit **2** with only the inherited 15 obsolete imports and two navigation
  fast-path assertions (`reports/iter-v358-wall-exit-target-gating/` logs).

### v358 local wall-exit target gating rejected; v0046 retained — 2026-08-20T18:22:56+02:00

- Live-v108 replay inspection found a fixed attacker oscillating at the
  Yulerune central wall.  v358 tested a visible static-wall exit subgoal; its
  one allowed repair added a visible staging waypoint when the actual opening
  was outside Builder vision.  Scope stayed within candidate attacker state,
  constants, and focused geometry tests.  Full record:
  `experiments/v0046-wall-exit-target-gating-v358.md`.
- Focused coverage was **28/28** initially and **29/29** after repair;
  compileall passed, smoke was **4/4**, and `make static` retained only the
  inherited 15 obsolete-module imports and two stale navigation assertions.
  The repaired immutable-v0046 screen was **9-6** at
  `reports/local-20260820T161525Z`; the required second rotated screen was
  **8-7** at `reports/local-20260820T161752Z`, for a pair of **17-13**.
  Both screens were command/TLE/suspicious/delivery-clean.
- v358 missed the **19-11** pair gate and is rejected after its single repair.
  Candidate source is recursively identical to immutable v0046 at
  `reports/iter-v358-wall-exit-target-gating/rollback-source-parity.diff`;
  rollback focused coverage is **26/26**, compileall passed, and rollback
  smoke is **4/4** at `reports/local-20260820T162140Z`.  No release matrix,
  remote gate, package, upload, activation, or promotion ran; live v108
  remains `active_observing`.
- A fresh read-only live capture at `reports/live-observe-20260820T162527Z`
  still showed v108 active/ready, platform rating **1575.90**, rank **40/129**,
  and a recent **5-5** record.  No live transition was performed.

### v357 forward Launcher rescue rejected; v0046 retained — 2026-08-20T17:55:00+02:00

- Live-v108 Yulerune tracing confirmed that the primary attacker was stalled
  behind the central wall and that the rescue trigger never fired: a home
  Launcher six tiles away was incorrectly treated as nearby even though it
  can only pick up an adjacent Builder.  v357 tested one reserve-backed
  forward Launcher after a measured stall and applied one bounded repair to
  use the real pickup range.  Full record:
  `experiments/v0046-forward-launcher-rescue-v357.md`.
- Focused coverage was **28/28**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete imports and two
  navigation assertions.  The immutable-v0046 seed-179 screen was **5-10**
  initially and **7-8** after repair, with zero command/TLE/suspicious/
  delivery failures.  A sampled repaired Yulerune run won and placed three
  candidate Launchers, but the required first-screen floor is **9-6**.
- v357 is rejected and rolled back.  Recursive production parity is empty at
  `reports/iter-v357-forward-launcher-rescue/rollback-source-parity.diff`;
  rollback focused coverage is **26/26**, compileall passed, and rollback
  smoke is **4/4** at `reports/local-20260820T154942Z`.  No rotated screen,
  release matrix, remote gate, package, upload, activation, or promotion ran;
  immutable v0046 remains the baseline and live v108 remains
  `active_observing`.

### v356 persistent frontier escape rejected; v0046 retained — 2026-08-20T17:30:00+02:00

- Fresh live-v108 Yulerune evidence showed the fixed attacker stalled behind
  a static central wall.  v356 tested one bounded edge-lane waypoint after a
  real approach stall, with one allowed repair accepting the Core's published
  converting/pressure economy phase when the delayed Harvester counter was
  still zero.  Scope stayed within attacker state, constants, and focused
  tests; no navigation rewrite, economy policy, Store schema, baseline, or
  platform operation changed.  Full record:
  `experiments/v0046-persistent-frontier-escape-v356.md`.
- Initial focused coverage was **30/30** and the repair was **31/31**;
  compileall passed, smoke was **4/4**, and `make static` retained only the
  inherited 15 obsolete imports plus two navigation assertions.  The explicit
  immutable-v0046 15-map screen was **6-9** initially and **6-9** after the
  repair (zero command failures, TLEs, suspicious output, or candidate
  delivery failures).  Yulerune collection improved but the win floor did not.
- v356 is rejected at the first-screen gate and rolled back.  Production
  source parity is empty at
  `reports/iter-v356-persistent-frontier/rollback-source-parity.diff`;
  rollback focused coverage is **26/26**, compileall passed, and rollback
  smoke is **4/4** at `reports/local-20260820T152205Z`.  No second screen,
  60-game matrix, remote gate, package, upload, activation, or promotion ran;
  immutable v0046 remains the local baseline and live v108 remains
  `active_observing`.

### v355 stalled-attacker breach window rejected; v0046 retained — 2026-08-20T17:00:00+02:00

- Fresh live-v108 Yulerune evidence showed the primary attacker oscillating
  around `(11,9)/(11,10)` behind a static central wall while an enemy Sentinel
  covered the approach.  v355 tested one bounded attacker-local breach after
  stagnation and a paying route, with a single outer-row flank repair.  Scope
  was limited to attacker state, navigation danger filtering, constants, and
  focused tests; no Launcher, route, Store, baseline, or platform policy was
  changed.  Full record: `experiments/v0046-stalled-attacker-breach-v355.md`.
- The initial explicit immutable-v0046 seed-172 screen was **6-9**.  The one
  allowed repair was focused **30/30**, compileall-clean, smoke **4/4**, and
  static-clean relative to the inherited profile, but the screen reached only
  **8-7**.  The Yulerune diagnostic still oscillated at `(8,9)/(8,10)`;
  zero command/TLE/suspicious rows does not offset the missed 9-6 floor.
- v355 is rejected and rolled back.  Recursive production parity is empty at
  `reports/iter-v355-stalled-attacker-breach/rollback-source-parity.diff`;
  rollback focused coverage is **26/26**, compileall passed, and rollback
  smoke is **4/4** at `reports/local-20260820T145838Z`.  `make static` remains
  the inherited exit-2 profile (15 obsolete imports and two stale navigation
  assertions), with no v355-specific failure.  The 60-game matrix, remote
  gate, package, upload, activation, and promotion did not run; immutable
  v0046 remains the baseline and live v108 remains `active_observing`.

### v354 compact first-Sentinel budget contract rejected; v0046 retained — 2026-08-20T16:30:00+02:00

- Fresh v108 and top-ladder replay audit found a compact-map control-timing
  gap after real delivery: live v108 built its first Sentinel at rounds
  94/28/never on Frostgate/Icefloe/Yulerune while Askar did so at 9/20/56.
  v354 temporarily held the *dynamically queried* Sentinel price against
  stage-two Builder spawning only after verified income, on cramped geometry,
  and only until a first Sentinel/threat/expiry release condition.
- Focused coverage was **28/28**, compileall passed, and smoke was **4/4**.
  `make static` retained exactly the inherited 15 stale imports and two
  navigation assertions.  The explicit-v0046 rotated 15-map seed-173 screen
  was reliability-clean with all candidate deliveries and **94,680 vs 78,240
  Ti**, but only **8-7**.  Frostgate/Icefloe Sentinel timing improved to
  **54 vs 112** and **20 vs 28**, while Yulerune still had none.
- The 8-7 result misses the clear 9-6 screen gate, so no 60-game matrix,
  remote gate, package, upload, activation, or promotion ran.  The temporary
  Core/test code was removed; source parity with immutable v0046 is empty,
  rollback focused coverage is **26/26**, compileall passed, and rollback
  smoke is **4/4** at `reports/local-20260820T142459Z`.  Full record:
  `experiments/v0046-compact-first-sentinel-reserve-v354.md`.

### v353 inbound Sentinel preemption rejected; v0046 retained — 2026-08-20T16:00:00+02:00

- Fresh v108 evidence identified a distinct forward-Launcher/three-to-five
  Sentinel Core rush in Jacobs Code losses. The temporary Core-visible staging
  alert and the one-responder repair both passed focused coverage (30/30),
  compileall, and smoke 4/4; `make static` retained only the inherited 15
  obsolete imports plus two stale navigation expectations.
- The private rush fixture is diagnostic only. The release comparator was the
  explicit immutable-v0046 all-map screen at
  `reports/local-20260820T135304Z`: **8-7**, candidate collection **81,630 vs
  86,660 Ti**, zero command/TLE/suspicious rows, but one candidate Auroraveil
  no-delivery row. That misses the required 9-6 screen floor and protected-map
  delivery guard, so no rotated second screen, 60-game/remote gate, package,
  upload, activation, or promotion ran.
- All temporary production/test changes were removed. Candidate source is
  recursively identical to immutable v0046 (excluding caches); rollback
  focused coverage is **26/26**, compileall passed, and rollback smoke is 4/4
  at `reports/local-20260820T135719Z`. Keep the replay causal finding but do
  not retry broad or nearest-only Sentinel preemption unchanged.

### v350 per-Builder mission scheduler rejected; v0046 retained — 2026-08-20T14:20:00+02:00

- The v108 live audit isolated a conversion fault rather than a runtime fault:
  its fresh 0-5 Askar City loss had zero TLE/suspicious output, but v108 often
  had 31-60 conveyors and only 1-3 Harvesters; Auroraveil delivered no titanium.
  Raw evidence is `reports/live-v108-scheduler-audit-20260820T115830Z`; the
  fresh platform snapshot is `reports/live-v108-final-audit-20260820T121432Z`
  (v108 active/ready, 1578.12, rank 40/129, recent 8-2).
- v350 tested a fundamental per-Builder route/pressure mission scheduler with
  an explicit fallback for released workers.  Repair 1 admitted visible enemy
  Harvesters as route sources; repair 2 deferred pressure until four verified
  home routes.  The v0046 all-map screens were **6-9**, **8-7**, and **6-9**;
  every candidate row delivered and had zero TLE/suspicious output, but repair
  2 regressed first delivery on Auroraveil **302 vs 28**, Glacierkeep **93 vs
  38**, and Royale **100 vs 22**.  Full record:
  `experiments/v0046-mission-scheduler-v350.md` and
  `reports/local-20260820T120014Z`, `reports/local-20260820T120336Z`,
  `reports/local-20260820T120632Z`.
- Focused coverage reached **44/44**, compileall passed, rollback focused
  coverage was **35/35**, and rollback smoke was **4/4 command-clean**.
  `make static` remains the inherited exit 2 from 15 obsolete imports and two
  navigation assertions.  Reject after two bounded repairs and restore exact
  v0046 source parity (`reports/iter-v350-final-source-parity.diff` is empty).
  No release gate, package, upload, activation, or live transition occurred.
  Next work is one local opening source-admission contract, not another
  scheduler/lifecycle variant; deployment remains blocked while v108 is
  `active_observing`.

### v349 phase-aware role/task contract rejected; v0046 retained — 2026-08-20T14:00:00+02:00

- v349 tested a fundamental role/task contract on immutable v0046 after
  auditing official top-team source and replays.  The candidate temporarily
  lent a fixed attacker to the existing Harvester/CHAIN route FSM during
  opening or recovery, required it to finish an active chain, and returned it
  to pressure when map state proved enemy-core intel or live pressure.  The
  first candidate lent both fixed attackers; repair 1 preserved a continuous
  primary pressure lane and attempted to lend only the second fixed attacker;
  source audit found that the Core does not designate that second attacker
  until three completed routes.  Repair 2 made the primary a local route owner
  only before three routes and until confirmed enemy-core intel, and skipped
  hijack/turret detours during that route mission.  Scope was
  `bots/candidate/main.py`, `bots/candidate/bot/defender.py`,
  `bots/candidate/bot/dynamic.py`, `bots/candidate/bot/attacker.py`, and one
  focused role/task test.  Full record:
  `experiments/v0046-role-contract-v349.md`.
- Focused coverage was **11/11** initially and **12/12** for each repair;
  rollback was **31/31**.  Compileall passed throughout.  Inherited
  `make static` stayed exit 2 with the obsolete candidate-module imports and
  two navigation assertions; smoke was **4/4 command-clean** for every
  candidate and rollback.  All initial/repair-1 rows delivered; repair 2 had
  one baseline no-delivery row, zero TLE/suspicious output, and max p99/peak
  callback time **1,318/5,496 us**.
- The initial seed-172 screen was **3-12**, **68,400 vs 114,340 Ti**.
  Repair 1 was **1-14**, **65,130 vs 97,790 Ti** on seed-172 and **8-7**,
  **77,190 vs 69,090 Ti** on seed-173.  Repair 2 was **7-8**,
  **57,610 vs 93,780 Ti** on seed-172 and **6-9**, **64,010 vs 77,710 Ti**
  on seed-173.  Reports are `reports/local-20260820T112204Z`,
  `reports/local-20260820T112553Z`, `reports/local-20260820T112751Z`,
  `reports/local-20260820T113409Z`, and `reports/local-20260820T113555Z`.
- Reject v349 after two bounded repairs: no repeatable win-rate/conversion
  edge and the best repair had a large collection deficit.  Restore exact
  v0046 source parity (`reports/iter-role-contract-v349-rollback-source-parity.diff`).
  No release gate, promotion, package, upload, activation, or live transition
  occurred; live v108 remains `active_observing` and immutable v0046 remains
  the local baseline.

Next work must not retry this fixed-attacker handoff unchanged.  The next
  fundamental experiment needs a true per-Builder mission scheduler: explicit
  route-owner completion, visible loaded-logistics sabotage, nearest home
  defense, and a concrete fallback for every released unit, while preserving
  the protected-map and delivery gates.

### v348 sink/path lifecycle rejected; v0046 retained — 2026-08-20T13:07:00+02:00

- v348 tested a route-sink lifecycle rewrite on immutable v0046 after the
  v347 Royale/Auroraveil replay audit: bound chain travel/build rounds, retain
  a failed Harvester origin, and open a short recovery window before buying a
  replacement source.  Repair 1 traced the visible fixed-output frontier and
  seeded its first gap; repair 2 made that recovery adjacent-only after the
  cross-map repair regressed the workforce.  Scope was
  `bots/candidate/bot/defender.py` and one temporary sink-lifecycle test; no
  Store, Core spawn, identity, attacker, baseline, package, platform, or live
  change remained.  Full record: `experiments/v0046-sink-lifecycle-v348.md`.
- Focused coverage was **34/34**, **35/35**, and **35/35**; rollback was
  **31/31**.  Compileall passed throughout.  Inherited `make static` stayed
  exit 2 with the obsolete candidate-module imports and two navigation
  assertions; smoke was **4/4 command-clean** for every candidate and
  rollback.  All 30 rows in both repairs delivered, with zero TLE/suspicious
  output; repair-2 max p99/peak callback time was **1,364/4,959 us**.
- Initial screens were seed-173 **10-5** / **83,570 vs 79,780 Ti** and
  seed-179 **7-8** / **57,430 vs 61,710 Ti** (combined **17-13** but
  **141,000 vs 141,490 Ti**).  Repair 1 fell to **6-9** and **5-10**
  (combined **11-19**).  Repair 2 restored conversion at **9-6** /
  **90,550 vs 74,230 Ti** and **6-9** / **109,330 vs 109,970 Ti** (combined
  **15-15**, despite **199,880 vs 184,200 Ti**).  The win-rate edge was not
  repeatable, so reject v348 after two bounded repairs and restore exact v0046
  source parity (`reports/iter-sink-lifecycle-v348-rollback-source-parity.diff`).
  No release gate, promotion, package, upload, activation, or live transition
  occurred; live v108 remains `active_observing`.

Next work must not retry the timer/frontier repair unchanged.  Reinspect
top-team route throughput and resource-to-pressure timing before a complete
role/task rewrite; preserve the no-idle fallback and protected-map gates.

### v347 per-builder route commit rejected; v0046 retained — 2026-08-20T12:42:00+02:00

- v347 replaced v346's global lease with a per-Builder concrete route
  commitment after auditing Royale/Auroraveil/Fjordgate and top-team route
  timing.  Early Defenders selected a visible/advertised ore mission before
  hijack; the mission released on stale/no-progress, visible route capacity,
  or low liquidity, returning to the existing sabotage/repair fallback.  Scope
  was `bots/candidate/bot/defender.py` and one temporary route-commit test; no
  Store, Core spawn, identity, attacker, baseline, package, platform, or live
  change remained.
- Focused coverage was **37/37**, **37/37**, and **39/39**; rollback was
  **31/31**.  Compileall passed.  Inherited `make static` stayed exit 2 with
  obsolete-module imports and two navigation assertions; smoke was **4/4**
  command-clean for every candidate and rollback.  Full record and report
  paths are in `experiments/v0046-route-commit-v347.md`.
- Initial seed-173 was **4-11** with one candidate no-delivery row.  Repair 1
  became delivery-clean at **9-6** / **68,750 vs 77,590 Ti** on seed-173 and
  **7-8** / **75,830 vs 76,080 Ti** on seed-179 (combined **16-14**).
  Repair 2 was delivery-clean at **7-8** / **85,130 vs 83,060 Ti** and **8-7**
  / **62,710 vs 63,290 Ti** (combined **15-15**, only **+1,490 Ti**).  The
  edge was not repeatable enough for promotion, so v347 was rejected after two
  repairs and exact v0046 source parity was restored.  No release gate,
  promotion, package, upload, activation, or live transition occurred; live
  v108 remains `active_observing`.

Next work should study the route FSM's sink/path lifecycle: verify the first
conveyor direction and repair a broken chain before buying another source,
while preserving loaded-logistics sabotage and nearest home defense.  Do not
retry v347's opening priority or v346's global lease unchanged.

### v346 map-aware workforce lease rejected; v0046 retained — 2026-08-20T12:19:43+02:00

- v346 tested a map-aware route-owner lease on immutable v0046 after
  inspecting seed-179 long-board losses and top-team economy/control timing.
  One/two locally nearest dynamic Builders stayed on route conversion until a
  map-scaled target; surplus Builders retained hijack, sabotage, repair, and
  home-defense work.  Repair 1 enforced the lease inside the Defender FSM;
  repair 2 made it an all-phase route-owner lifecycle and tried a local
  Harvester before optional Core-ring upkeep.  Scope was
  `bots/candidate/bot/defender.py`, `bots/candidate/bot/dynamic.py`, and one
  temporary focused test.  No Store, Core spawn, identity, baseline, package,
  platform, or live-state change remained.
- Focused coverage was **36/36**, **37/37**, and **39/39**; rollback was
  **31/31**.  Compileall passed throughout.  Inherited `make static` stayed
  exit 2 with obsolete-module imports and two navigation assertions; smoke was
  **4/4** for each repair and rollback.  Reports are recorded in
  `experiments/v0046-workforce-lease-v346.md`.
- Repair 1 screens were **6-9** and **7-8** (seed-173/179), combined **13-17**
  and **161,550 vs 175,030 Ti**.  Repair 2 screens were **6-9** and **6-9**,
  combined **12-18** and **154,610 vs 161,490 Ti**; all 30 candidate rows
  delivered with zero candidate TLE/suspicious rows.  The candidate never
  earned a repeatable win-rate/conversion edge, so the lease was rejected after
  both bounded repairs and exact v0046 source parity was restored.  No release
  gate, promotion, package, upload, activation, or live transition occurred;
  live v108 remains `active_observing`.

Next work must not retry a global or phase-only workforce lease.  Use a
verified route-commit state machine with concrete visible ore/path progress,
release stale/no-progress commitments, and allow the same unit to alternate
between route construction and reachable sabotage/defense.

### v345 delivery-proof control handoff rejected; v0046 retained — 2026-08-20T11:49:00+02:00

- v345 tested a top-team-informed delivery-proof handoff on immutable v0046.
  A dynamic Builder could take one nearest-owner enemy-Core Barrier turn only
  after the Core phase proved a live route and a forward Sentinel existed;
  repair 1 restored the fixed attacker’s original Barrier path after the
  proof was found too conservative, and repair 2 restricted only the new
  dynamic handoff to stable `PRESSURE`.  Scope was
  `bots/candidate/bot/attacker.py`, `bots/candidate/bot/dynamic.py`, and one
  focused delivery-proof test.  No Store, route, identity, baseline,
  package, platform, or live-state change remained.
- Initial valid screens were seed-173 **7-8** (**62,450 vs 74,800 Ti**) and
  seed-179 **3-12** (**41,600 vs 59,250 Ti**).  Repair 1 reached seed-173
  **7-8** (**71,470 vs 75,100 Ti**) and seed-179 **9-6** (**55,200 vs 50,570
  Ti**), delivery-clean on all 30 candidate rows.  Repair 2 reached seed-173
  **8-7** (**92,170 vs 75,570 Ti**) but seed-179 fell to **6-9**
  (**75,210 vs 81,470 Ti**); its combined result was **14-16** despite
  **167,380 vs 157,040 Ti**.  The concurrent first screen's report-id
  collision is retained as `reports/local-20260820T093045Z` but was not
  scored.  Full record: `experiments/v0046-delivery-proof-v345.md`.
- Focused repair coverage was **34/34**, compileall passed, inherited
  `make static` stayed exit 2 with the known 15 obsolete-module imports and
  two navigation assertions, and smoke was **4/4**.  After the second
  bounded repair, exact v0046 source parity was restored and rollback
  focused coverage was **31/31**; rollback compileall passed and rollback
  smoke was **4/4** at `reports/local-20260820T094817Z`.  No release gate,
  promotion, package, upload, activation, or live transition occurred.

Next work must be a genuinely different workforce architecture: inspect the
seed-179 long-board Harvester/conveyor deficit and top-team economy/control
split, then test an explicit map-aware economy/pressure lease that keeps route
owners productive while surplus builders sabotage or defend.  Do not retry a
Barrier or phase-threshold variant without new causal replay evidence.

### v344 map-aware reserve-backed control shell rejected; v0046 retained — 2026-08-20T11:20:00+02:00

- v344 tested a structural phase rewrite on immutable v0046 after inspecting
  top-team control-first/economy-first replays: the primary attacker could
  fund one fresh-intel compact-map Sentinel/Barrier pulse only behind a full
  route/workforce/offense reserve, and one pressure-phase dynamic Builder
  could hand off a local Barrier before returning to raids.  Larger maps,
  stale intel, low liquidity, siege, and home threats released the phase.
  Scope was `bots/candidate/bot/attacker.py`,
  `bots/candidate/bot/dynamic.py`, and one focused test; no Store, route,
  identity, baseline, package, platform, or live-state change remained.
- Initial focused coverage was **38/38**, compileall passed, and seed-179 was
  **7-8** with **60,410 vs 52,310 Ti**; rotated seed-173 exposed **4-11**,
  **47,720 vs 78,360 Ti**, and two candidate no-delivery rows.  Repair 1
  added a round-20 settling window and reached **7-8**, delivery-clean, at
  **67,690 vs 68,750 Ti**.  Repair 2 delayed Barrier spending until a route
  completed and reached **8-7** at **82,480 vs 70,930 Ti** on seed-173 and
  **8-7** at **70,690 vs 63,450 Ti** on seed-179; both were delivery-clean.
  Reports are under `reports/iter-control-shell-v344-*`.
- The 60-game endpoint/side gate was command-clean at **38-22** and
  **370,960 vs 329,100 Ti** (+41,860), max p99/peak **1,368/5,938 us**, with
  zero TLE/suspicious rows.  It nevertheless contained one candidate-side
  Icefloe no-delivery game while v0046 delivered, so the protected-map
  promotion guard rejects it.  Restore exact v0046 parity using the zero-byte
  proofs `reports/iter-control-shell-v344-rollback-attacker.diff` and
  `reports/iter-control-shell-v344-rollback-dynamic.diff`.
- Rollback focused coverage was **31/31**, compileall passed, static retained
  the inherited 15 obsolete-module imports plus two navigation assertions,
  and rollback smoke was **4/4** at `reports/local-20260820T091439Z`.  No
  promotion, package, upload, activation, or live transition occurred; live
  state remains v108 `active_observing` with v107 known-good.  Full record:
  `experiments/v0046-control-shell-v344.md`.

Next work must not retry the compact control pulse unchanged.  Add a verified
delivery/route-health proof to the next control-phase rewrite before changing
another spend threshold.

### v343 local route-site reservation/BFS rejected; v0046 retained — 2026-08-20T10:44:00+02:00

- v343 tested a structural local Defender contract on immutable v0046: a
  Builder reserved its visible ore target and a visible-only BFS preflight
  checked for a currently reachable Core-facing path.  Repair 1 softened
  distant reservations; repair 2 restored strict ownership with an uncertain
  adjacent fallback.  Scope was `bots/candidate/bot/defender.py` and one
  focused route-site test; no attacker/role, Store, opening, combat, baseline,
  package, platform, or live-state change was kept.
- Focused coverage passed **40/40**, **41/41**, and **41/41**; compileall passed.
  The seed-173 screen was **8-7** and **83,130 vs 61,370 Ti**, but the rotated
  seed-172 screen was **5-10**, had one candidate no-delivery Drakkarfjord row,
  and **67,530 vs 84,110 Ti**.  Repair 1 regressed to **2-13** and
  **49,520 vs 91,090 Ti**; repair 2 restored delivery cleanliness but only
  reached **7-8** and **79,460 vs 89,810 Ti**.  Analyses are
  `reports/iter-route-site-v343-screen-analysis.json`,
  `reports/iter-route-site-v343-rotated-screen-analysis.json`,
  `reports/iter-route-site-v343-repair1-screen-analysis.json`, and
  `reports/iter-route-site-v343-repair2-screen-analysis.json`.
- Reject v343 after two bounded repairs and restore exact recursive v0046
  parity (`reports/iter-route-site-v343-rollback-source-parity.diff`).
  Rollback focused coverage was **35/35**, compileall passed, static retained
  the inherited 15 obsolete imports plus two navigation assertions, and smoke
  was **4/4** at `reports/local-20260820T084012Z`.  No promotion, package,
  upload, activation, or live transition occurred.  Full record:
  `experiments/v0046-route-site-v343.md`.

Next work must move beyond isolated opening routing.  Reinspect top-team
control-shell and loaded-logistics pulse timing, then test a bounded
conversion/pressure phase that keeps defense active while repeatedly
sabotaging reachable enemy logistics.

### v342 reversible primary-attacker economy relay rejected; v0046 retained — 2026-08-20T10:24:00+02:00

- v342 tested a fundamentally different per-unit multitask policy on immutable
  v0046: only the primary fixed attacker could borrow the existing Harvester /
  CHAIN FSM once, then return permanently to its sentinel/sabotage lane.  A
  repair restricted the source to six Core steps; a second made the relay
  compact-map-only.  Scope was `bots/candidate/main.py`,
  `bots/candidate/bot/attacker.py`, and one focused relay test; no Store
  schema, global four-route lease, fixed identity, route geometry, baseline,
  package, platform, or live-state change was kept.
- Focused coverage passed **39/39**, **39/39**, and **40/40** across the
  initial version and two repairs; compileall passed.  The initial screen was
  **4-11 candidate-A** with **75,370 vs 84,640 Ti**.  Repair 1 reached **8-7**
  but collected **73,460 vs 84,720 Ti**; repair 2 remained **8-7** at
  **85,010 vs 91,110 Ti**.  All screen rows delivered and had zero
  TLE/suspicious output; analyses are
  `reports/iter-opening-relay-v342-screen-analysis.json`,
  `reports/iter-opening-relay-v342-repair1-screen-analysis.json`, and
  `reports/iter-opening-relay-v342-repair2-screen-analysis.json`.
- Reject v342 after two bounded repairs; no long gate was justified.  Restore
  exact recursive v0046 parity
  (`reports/iter-opening-relay-v342-rollback-source-parity.diff`).  Rollback
  focused coverage was **35/35**, compileall passed, static retained the
  inherited 15 obsolete imports plus two navigation assertions, and smoke was
  **4/4** at `reports/local-20260820T082358Z`.  No promotion, package, upload,
  activation, or live transition occurred.  Full record:
  `experiments/v0046-opening-relay-v342.md`.

Next work must not retry the fixed-attacker relay unchanged.  Test a distinct
local route-site reservation/path-viability mechanism that keeps continuous
offense available while preventing one/zero-Harvester openings.

### v341 local route-frontier reacquisition rejected; v0046 retained — 2026-08-20T10:08:00+02:00

- v341 tested a structural local Builder-FSM contract on immutable v0046:
  after danger or Launcher displacement, a pending conveyor frontier could be
  reacquired for three rounds without a shared Store heartbeat.  Repair 2
  limited that lease to two cardinal steps and retained CHAIN mode for a local
  replan.  Only `bots/candidate/bot/defender.py` and focused defense tests were
  in scope; no Store, opening, role, combat, baseline, package, platform, or
  live-state change was kept.
- Initial focused coverage was **37/37**, repair 1 **37/37**, and repair 2
  **38/38**; compileall passed.  The initial screen was **8-7** but had two
  candidate no-delivery rows.  Repair 1 was delivery-clean at **8-7** and the
  rotated screen was delivery-clean at **7-8**, with candidate collection
  edges of **+4,340 Ti** and **+2,560 Ti**.  Reports are
  `reports/iter-route-frontier-v341-screen-analysis.json`,
  `reports/iter-route-frontier-v341-repair1-screen-analysis.json`,
  `reports/iter-route-frontier-v341-rotated-screen-analysis.json`, and
  `reports/iter-route-frontier-v341-repair2-screen-analysis.json`.
- The required 60-game endpoint/side gate was command-clean but rejected at
  **25-35 candidate wins** and **274,330 vs 296,920 Ti**.  Candidate delivered
  all 60 while the baseline had three no-delivery rows; max p99/peak was
  **1,425/4,775 us**, with zero TLE/suspicious rows.  Full analysis:
  `reports/iter-route-frontier-v341-release-analysis.json`.
- Reject v341 after two bounded repairs and restore exact recursive v0046
  parity (`reports/iter-route-frontier-v341-rollback-source-parity.diff`).
  Rollback focused coverage was **35/35**, compileall passed, static retained
  the inherited 15 obsolete imports plus two navigation assertions, and
  rollback smoke was **4/4** at `reports/local-20260820T080712Z`.  No
  promotion, package, upload, activation, or live transition occurred.  Full
  record: `experiments/v0046-route-frontier-v341.md`.

Next work must not retry pending-tile reacquisition alone.  Reinspect the
Fjordgate/Nordkap opening losses and top-team workforce conversion, then test
a reversible one-route economy relay for the primary fixed attacker before it
returns to continuous pressure; do not introduce a global four-route lease.

### v340 packed chain-heartbeat ownership rejected; v0046 retained — 2026-08-20T09:39:00+02:00

- v340 tested a structural shared chain-progress signal on immutable v0046:
  slot 11 kept the completed-route count in low bits and published a short
  active-chain owner/round lease in high bits.  Opening duplicate recovery was
  suppressed, the lease owner could recover itself, and mature recovery was
  released after delivery.  No opening spend, route geometry, role policy,
  combat policy, baseline, package, platform, or live-state change was kept.
- Focused coverage passed **38/38**, **39/39**, and **40/40** across the initial
  version and two bounded repairs; compileall passed.  The screens were
  **3-12**, **7-8**, and **8-7 candidate-A**.  Repair 2 delivered on every
  screen game and collected **95,540 vs 82,670 Ti**; replay analyses are
  `reports/iter-chain-heartbeat-v340-screen-analysis.json`,
  `reports/iter-chain-heartbeat-v340-repair1-screen-analysis.json`, and
  `reports/iter-chain-heartbeat-v340-repair2-screen-analysis.json`.
- The 60-game endpoint/side gate was command-clean at **32-28**, but candidate
  collection was **295,840 vs 309,120 Ti** and one candidate-side-B
  Drakkarfjord game had no delivery while v0046 delivered.  Max p99/peak was
  **1,425/5,540 us**, with zero TLE/suspicious rows.  Full analysis is
  `reports/iter-chain-heartbeat-v340-release-analysis.json`.
- Reject v340 after two bounded repairs and restore exact recursive v0046
  parity (`reports/iter-chain-heartbeat-v340-rollback-source-parity.diff`).
  Rollback focused coverage was **35/35**, compileall passed, static retained
  the inherited 15 obsolete imports plus two navigation assertions, and smoke
  was **4/4** at `reports/local-20260820T073829Z`.  No promotion, package,
  upload, activation, or live transition occurred.  Full record:
  `experiments/v0046-chain-heartbeat-v340.md`.

Next work must avoid a shared slot-11 heartbeat.  Reinspect top-team replays
and redesign route ownership locally through the existing Builder FSM so one
frontier advances without blocking independent harvesters or mature repairs.

### v339 bounded route-health sink proof rejected; v0046 retained — 2026-08-20T09:08:50+02:00

- v339 tested a structural fixed-output route proof on immutable v0046 after
  the Glacierkeep no-delivery diagnosis.  A visible Conveyor walk was
  classified as Core-connected, proven dead, or unobservable; mature routes
  could merge into a proven sink and mature orphan Harvesters could request a
  local recovery seed.  The opening guard in the one repair preserved the
  legacy Core-only chain until one completed route.  No role, spending,
  navigation, combat, Store, baseline, package, platform, or live-state policy
  changed.
- Focused route/defense/economy coverage was **39/39** before and after the
  repair; compileall passed.  The initial and repaired 15-map screens were
  both **7-8 candidate-A**, zero TLE/suspicious rows.  The repaired screen's
  max p99/peak callback time was **1,296/3,175 us**; replay reports are
  `reports/iter-route-health-v339-screen-analysis.json` and
  `reports/iter-route-health-v339-repair1-screen-analysis.json`.
- Reject v339 because topology proof did not produce a repeatable paired edge
  and the initial version reduced opening Harvesters on several maps.  Restore
  exact immutable v0046 source parity; rollback focused coverage was **35/35**,
  compileall passed, `make static` retained its inherited 15 obsolete imports
  plus two navigation assertions, and rollback `make smoke` was **4/4** at
  `reports/local-20260820T070806Z`.  No 60-game gate, promotion, package,
  upload, activation, or live transition occurred.  Full record:
  `experiments/v0046-route-health-sink-proof-v339.md`.

### v338 defect-driven utility ownership rejected; v0046 retained — 2026-08-20T06:47:00Z

- v338 tested a structural nearest-responder contract on immutable v0046:
  only the closest visible dynamic Builder could claim a belt gap or damaged
  home building, and the claim released when the local evidence changed.  A
  first repair gated Harvester hijack to `PRESSURE`; a second repair made live
  `HARVEST` outrank damaged-building maintenance.  Opening spend, route
  geometry, fixed roles, Launcher behavior, and live state were unchanged.
- Focused coverage was **35/35**, **36/36**, and **37/37** across the initial
  version and two repairs; compileall passed throughout.  `make static` kept
  the inherited 15 obsolete imports and two navigation assertions.  Smoke was
  command-clean (20-game initial/repair-1 runs and 4-game repair-2 run).
- The screens were **7-8**, **5-10**, and **10-5 candidate-A** respectively;
  repair 2 had zero TLE/suspicious rows and max p99 **1,298 us**
  (`reports/local-20260820T063408Z`).  The 60-game gate was **33-27**, with
  collection **292,950 vs 283,710 Ti**, max p99/peak **1,436/4,903 us**, and
  zero TLE/suspicious rows (`reports/local-20260820T063701Z`).
- Reject v338 because one candidate Glacierkeep game had no titanium delivery
  while v0046 delivered; the reliability guard outweighs the aggregate edge.
  Candidate source was restored to exact v0046 parity; rollback focused tests
  passed **31/31**, compileall passed, static retained its inherited profile,
  and rollback smoke was **4/4** (`reports/local-20260820T064600Z`).  No
  promotion, package, upload, activation, or live-state transition occurred.
  Full record: `experiments/v0046-defect-driven-utility-owner-v338.md`.

### v337 Launcher dynamic insertion rejected; v0046 retained — 2026-08-20T06:15:31Z

- v337 tested a structural pressure conversion from top-team replay evidence:
  the existing home Launcher could insert one forward non-floor Builder after
  a reserve-backed three-chain economy.  Opening production, route geometry,
  fixed attackers, Store schema, and live state were unchanged.
- Initial focused coverage was **12/12**, compileall passed, smoke was **4/4**,
  and `make static` retained the inherited 15 obsolete imports plus two
  navigation assertions.  The 15-map screen was command-clean but **6-9**;
  replay analysis found no TLE/suspicious rows and showed late-economy deficits
  (`reports/local-20260820T055522Z`,
  `reports/iter-v337-launcher-insert-replay-analysis.json`).
- Repair 1 excluded the permanent defender from relay pickup: focused **13/13**,
  compileall passed, smoke **20/20**, screen **5-10**
  (`reports/local-20260820T060351Z`).  Repair 2 required five completed chains
  plus a recorded forward Sentinel: focused **13/13**, compileall passed,
  smoke **20/20**, screen **6-9**, max p99 **1,298 us**
  (`reports/local-20260820T060808Z`,
  `reports/iter-v337-launcher-insert-repair2-replay-analysis.json`).
- Reject v337 after two bounded repairs.  Restore exact recursive candidate
  parity with immutable v0046; rollback focused/compileall checks passed,
  static retained the inherited profile, and rollback smoke was **20/20**
  command-clean (`reports/local-20260820T061148Z`).  No package, upload,
  activation, promotion, or live-state transition occurred.  Next work must
  verify a local defect or explicit task signal before taking a route Builder.

### v336 finite utility lease rejected; v0046 retained — 2026-08-20T05:48:00Z

- v336 tested a structural workforce handoff from top-team behavior: the Core
  chose one non-fixed Builder from its living roster, published its id and
  lease epoch in the high bits of the unused Gunner-cap slot, and gave that
  Builder a 24-round economy/repair duty before rotating it.  Local threats and
  belt repairs remained higher priority; opening spend and route geometry were
  unchanged.
- Initial focused coverage passed **33/33**, compileall passed, smoke **4/4**,
  and static retained the inherited 15 obsolete imports plus two navigation
  assertions.  The first screen was command-clean but **0-15** because the Core
  caught a `NameError` before spawning; replay analysis, rather than process rc,
  exposed the defect (`reports/iter-v336-utility-screen.log`).
- Repair 1 fixed the undefined Core count.  Focused coverage stayed **33/33**,
  smoke **4/4**, but the screen was **2-13**, collection **66,240 vs 125,170
  Ti**, first delivery **36.1 vs 25.4** turns
  (`reports/local-20260820T054013Z`).
- Repair 2 moved the lease from healthy `PRESSURE` to sub-five-chain
  `CONVERTING`.  Focused coverage was **33/33**, smoke **4/4**, and the screen
  improved only to **4-11**, collection **73,220 vs 79,090 Ti**, first delivery
  **32.7 vs 96.8** turns (`reports/local-20260820T054434Z`).
- Reject v336 after the two bounded repair attempts.  Restore exact recursive
  production parity with immutable v0046; rollback focused coverage passed
  **31/31**, compileall passed, static retained the same inherited profile,
  and rollback smoke was **4/4** at `reports/local-20260820T054757Z`.
  No package, upload, activation, or live-state transition occurred.  The next
  hypothesis must lease only a verified local defect and release immediately,
  not force a timed economy worker.

### v335 post-delivery siege phase promoted to local v0046 — 2026-08-20T05:31:00Z

- Top-team replays show that winners convert a healthy five-route economy into
  a deeper control shell instead of leaving the attacker at the fixed six-
  Barrier cage.  v335 added a phase-gated cap of twelve known enemy-Core
  Barriers, enabled only when the Core publishes `PRESSURE` with at least five
  Harvesters.  Opening routes, Launcher relay, and crisis recovery were left
  unchanged.
- The first screen was **7-8**, so one bounded repair removed an unused
  Defender-side Harvester suppression predicate while retaining the cage
  transition.  Repair focused coverage passed **39/39**, compileall passed,
  and smoke was **4/4**.  The repair screen was **10-5**, with collection
  **90,010 vs 72,070 Ti**, and no command/reliability failures
  (`reports/local-20260820T051749Z`).
- The complete 60-game gate was **33-27 candidate-A**, collection
  **307,900 vs 306,930 Ti**, with zero command failures, TLEs, or suspicious
  rows; max p99/peak was **1,436/5,241 us**
  (`reports/local-20260820T052022Z` and
  `reports/iter-v335-pressure-siege-repair1-gate-replay-analysis.json`).
- Review removed the dead helper and its two tests; focused cleanup tests
  passed, compileall passed, and smoke remained **4/4**
  (`reports/iter-v335-pressure-siege-cleanup-*`,
  `reports/local-20260820T052916Z`).  `make static` still has the inherited
  15 obsolete-module errors and two navigation assertions.
- Promote the candidate as immutable local baseline
  `bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`
  (archive SHA-256
  `18a7923be08838a242fc0fc44d38a3794ab2dae7d7baabb7580459b1594c6a30`).
  Keep v0045 as rollback; no upload, activation, or live-state transition was
  performed.  The margin is modest and several maps remain resource-loss
  risks, so the next rewrite must coordinate finite route repair, defense, and
  siege utility states rather than merely raising another cap.

### v334 coordinated three-Launcher relay rejected; v0045 retained — 2026-08-20T05:09:22Z

- Top-team winner replays averaged about five Builders, five Harvesters,
  fourteen Barriers, three Launchers, and three-to-four Sentinels.  v334 tested
  one structural composition change: two fixed attackers plus one deterministic
  local dynamic support Builder could establish up to three visible home
  Launchers, while preserving the first-route/liquidity reserve.
- Focused coverage passed **39/39**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete imports and two
  navigation fast-path assertions.  Logs:
  `reports/iter-v334-launcher-coordination-focused.log`,
  `reports/iter-v334-launcher-coordination-compileall.log`,
  `reports/iter-v334-launcher-coordination-static.log`,
  `reports/local-20260820T050249Z`.
- The rotated 15-map screen against immutable v0045 was command-clean but
  **4-11 candidate-A** with mean collection about **3,962 vs 5,103 Ti** and
  first delivery **34.2 vs 30.5** rounds.  Replay analysis showed one Launcher
  on nearly every map and an unstable five-Launcher overbuild on Yulerune:
  `reports/local-20260820T050329Z` and
  `reports/iter-v334-launcher-coordination-replay-analysis.json`.
- Reject v334; exact v0045 production parity was restored.  Rollback focused
  coverage was **36/36**, compileall passed, and rollback smoke was **4/4** at
  `reports/local-20260820T050843Z`.  No longer gate, release, package, upload,
  activation, or live-state transition occurred.  The next hypothesis must
  target finite route conversion/defensive topology rather than Launcher-count
  expansion.

### v333 nearest enemy-Harvester owner rejected; v0045 retained — 2026-08-20T07:15:00Z

- v333 added a deterministic local infiltration contract from the top-team
  replay hypothesis: fixed attackers never claim visible enemy Harvesters, and
  only the nearest visible non-attacker Builder may seed a hijack (stable id
  tie-break).  The rule covered both Dynamic selection and Defender SCOUT
  hijack; no Store lease or route rewrite was introduced.
- Focused coverage passed **41/41**, compileall passed, smoke was **4/4**
  (`reports/local-20260820T044614Z`), and static retained only the inherited
  failures (`reports/iter-v333-hijack-owner-static.log`).
- The 15-map screen was command-clean but **7-8 candidate-A**, collection
  **58,500 vs 73,080 Ti**, deliveries **14 vs 15**, and max p99/peak
  **1,470/5,707 us** (`reports/local-20260820T044649Z`,
  `reports/iter-v333-hijack-owner-replay-analysis.json`).
- Reject v333 and restore exact recursive v0045 parity; rollback focused
  coverage passed **40/40** (`reports/iter-v333-hijack-owner-rollback-focused.log`).
  No long gate, package, upload, promotion, activation, or live-state change
  occurred.  The next rewrite targets idle workforce conversion and route
  survival with a finite utility/state policy.

### v332 compact-map twin Launcher relay rejected; v0045 retained — 2026-08-20T06:55:00Z

- v332 tested a finite map-adaptive control squad from top-team traces: on
  compact maps the Core designated the first stage-2 Builder as a second fixed
  attacker, and each fixed attacker could build one reserve-backed home
  Launcher.  Wide maps retained the proven three-route gate; route FSM,
  dynamic tasks, Sentinel/Gunner spending, and Store schema were unchanged.
- Focused coverage passed **42/42**, compileall passed, smoke was **4/4**
  (`reports/local-20260820T043753Z`), and static retained only the known
  inherited failures (`reports/iter-v332-twin-relay-static.log`).
- The rotated 15-map screen was command/reliability-clean but **7-8
  candidate-A**, with collection **76,630 vs 76,540 Ti** and deliveries **15
  vs 13**.  Max p99/peak was **1,301/2,775 us**
  (`reports/local-20260820T043832Z`,
  `reports/iter-v332-twin-relay-replay-analysis.json`).
- Reject v332 and restore exact recursive v0045 parity; rollback focused
  coverage passed **40/40** (`reports/iter-v332-twin-relay-rollback-focused.log`).
  No long gate, package, upload, promotion, activation, or live-state change
  occurred.  The next rewrite targets deterministic ownership of visible
  enemy-Harvester infiltration rather than more Launcher count.

### v331 coordinated pressure-owner assault lane rejected; v0045 retained — 2026-08-20T06:35:00Z

- v331 tested a fundamental coordination contract motivated by top-team
  pressure waves: the Core published one deterministic dynamic Builder as a
  pressure owner through unused high bits of `SLOT_GUNNER_CAP` during the
  `PRESSURE` phase.  That owner could attack loaded enemy logistics or advance
  toward the enemy Core, while CHAIN work, fixed attackers, turret cap, Store
  size, spending, and map policy stayed unchanged.
- Focused coverage passed **43/43**, compileall passed, and smoke was **4/4**
  (`reports/local-20260820T042832Z`).  `make static` retained only the known
  inherited 15 obsolete-module imports and two navigation fast-path
  assertions (`reports/iter-v331-pressure-owner-static.log`).
- The rotated 15-map screen was command/reliability-clean but **4-11
  candidate-A** against immutable v0045.  Collection was **42,460 vs 60,840
  Ti**, all 15 rows delivered, and max p99/peak was **1,332/4,350 us**
  (`reports/local-20260820T042906Z`,
  `reports/iter-v331-pressure-owner-replay-analysis.json`).
- Reject v331 and restore exact recursive v0045 parity; rollback focused
  coverage passed **40/40** (`reports/iter-v331-pressure-owner-rollback-focused.log`).
  No 60-game gate, remote gate, package, upload, promotion, activation, or
  live-state change occurred.  The next experiment must use bounded squad or
  relay ownership with explicit return/release conditions; a single owner can
  strand route throughput.

### v330 symmetry-backed post-route Sentinel rejected at 60-game gate; v0045 retained — 2026-08-20T06:20:00Z

- v330 tested a structural discovery escape motivated by remote v108 losses and
  top-team pressure: after one completed route, an open-map attacker could
  place exactly one reserve-backed Sentinel at the symmetric enemy-Core target
  before visual confirmation.  Placement remained gated by `can_fire_from` and
  `can_build_sentinel`; no other production policy changed.
- Focused coverage passed **42/42**, compileall passed, smoke **4/4**, and the
  rotated 15-map screen was **9-6**, all command-clean
  (`reports/iter-v330-symmetry-pressure/` and
  `reports/local-20260820T040727Z`).  Static retained the known inherited
  stale imports and two navigation fast-path assertions.
- The full 60-game side-swapped gate was **29-31**, collection **307,210 vs
  314,100 Ti**, with zero candidate no-delivery rows and no TLE/suspicious
  rows (`reports/local-20260820T040930Z` and
  `reports/iter-v330-symmetry-pressure-release60-analysis.json`).
- Reject v330 and restore exact immutable v0045 production parity.  Rollback
  focused coverage was **40/40**, compileall passed, smoke **4/4**, and no
  remote gate, package, upload, promotion, activation, or live-state change
  occurred.  The next experiment must address coordinated assault/relay waves
  or route redundancy, not another blind fixed-facing turret.


### v329 crisis route-owner experiment rejected; v0045 retained — 2026-08-20T06:05:00Z

- v329 gave only the permanent economy Defender a bounded homeward sweep when
  the Core published `ECONOMY_PHASE_CRISIS`, reusing existing orphan reconnect,
  belt repair, Core-ring, heal, and navigation gates.  It was a lifecycle
  experiment, not a spending or unit-count change.
- Focused coverage passed **42/42**, compileall passed, smoke was **4/4**, and
  `make static` retained only the known inherited stale imports and two
  navigation fast-path assertions.  The rotated screen was **9-6** and the
  60-game local gate was **34-26**, both command-clean
  (`reports/iter-v329-crisis-route-owner/`).
- The required remote five-game gate failed **2-3** in match
  `7487346c-f8ce-4f6d-bcbd-250a24099d01` (`rated:false`); replay analysis shows
  route-survival and pressure-conversion losses despite an early delivery in
  one game.  Reject v329 and restore exact immutable v0045 production parity.
- No package, upload, activation, promotion, or live-state change occurred.
  Platform v108 remains guarded `active_observing`; the next hypothesis must
  coordinate sustained Launcher/Sentinel/Barrier pressure rather than pull a
  single worker home during crisis.


### v327/v328 structural opening experiments rejected; v0045 retained — 2026-08-20T03:45:00Z

- Top-team traces split openings into economy-first and control-first families,
  so v327 temporarily made the permanent primary attacker a route owner on
  open maps until the first completed chain.  The initial rotated 15-map
  screen was **7-8**; a local-ore repair was **6-9**.  Both were
  command-clean, but neither established an edge over immutable v0045
  (`reports/local-20260820T033316Z`, `reports/local-20260820T033652Z`).
- v328 tested the opposite structural family: one dynamic-price,
  reserve-backed early Sentinel on compact maps before route payback.  It was
  command-clean but only **5-10** on the same screen
  (`reports/local-20260820T034059Z`).  More early control units did not
  convert into wins.
- Focused tests passed for both variants (43/43 and 42/42), compileall passed,
  smoke was 4/4, and `make static` retained only the repository's known stale
  imports and two navigation fast-path assertions.  Both production changes
  and temporary tests were removed; recursive candidate production parity
  with v0045 is zero.  No package, upload, activation, or live transition
  occurred.  Experiment records: `experiments/v0045-map-adaptive-opening-v327.md`
  and `experiments/v0045-compact-early-sentinel-v328.md`.
- Keep active platform v108 under its existing guarded observation; the local
  v0045/v319 baseline remains the rollback-safe development baseline.  The
  next structural hypothesis should address route throughput/redundancy or
  route ownership, not add more opening spend.

### v319 opening Launcher relay retained after 60-game gate — 2026-08-20T02:18:11Z

- Top-team opening traces showed immediate Launcher control/mobility while the
  live v107 loss set showed our builders spending the opening walking or
  trailing low-conversion belts.  v319 added one real Launcher lifecycle on
  top of immutable v0044: the primary attacker can build one reserve-backed
  home Launcher in SCOUT, which ejects nearby enemy Builders away from our Core
  or throws a designated attacker only on strict progress toward the enemy
  Core.  Store, route, workforce, other combat units, baseline, package,
  upload, activation, and live state were unchanged.
- Focused coverage was **40/40**, compileall passed, smoke was **4/4**, and
  static retained the inherited 15 obsolete-module imports plus two navigation
  fast-path assertions (`reports/iter-v319-opening-launcher/`).
- The rotated 15-map screen was command/delivery-clean at **7-8** candidate-A
  versus the frozen v0044 screen's **4-11**, with collection
  **88,610/94,020 Ti** (`reports/local-20260820T020932Z`).
- The full 60-game map/seed/side gate was **36-24 candidate wins**, collection
  **304,340/255,830 Ti**, no map at 0-4, and zero TLE/suspicious rows
  (`reports/local-20260820T021233Z`).  Candidate Launchers appeared at turn 2
  in all 60 games; no reliability failures were observed.
- Retain v319 as the strongest local candidate.  No package, upload, activation,
  live promotion, or baseline snapshot transition was performed in this
  checkpoint.  Experiment: `experiments/v0044-opening-launcher-relay-v319.md`.

### v318 visible route-commitment gate rejected and rolled back — 2026-08-20T01:48:53Z

- Top-team and live v107 replay evidence showed a structural one-Harvester/
  many-Conveyor conversion failure.  v318 added a bounded visible passability
  probe before the first Harvester commitment, requiring a Core-ring path within
  the existing CHAIN slack; unknown vision and the proven chain walker retained
  the old behavior.  No Store, workforce, role/task, combat, baseline, package,
  upload, activation, or live-state logic changed.
- Initial focused coverage was **37/37**, compileall passed, smoke was **4/4**
  (`reports/local-20260820T013431Z`), and static retained the inherited 15
  obsolete-module imports plus two navigation assertions.  The 15-map screen
  was command/delivery-clean at **9-6**, collection **56,580/48,250 Ti**, all
  15 candidate deliveries, zero TLE/suspicious rows, max p99/peak
  **1,378/2,076 us** (`reports/local-20260820T013500Z`).
- The 60-game gate was command-clean but only **32-28** candidate wins,
  **313,260/315,860 Ti**, one no-delivery row per side, and weak Yulerune
  (**0-4**) and Frostgate (**1-3**) floors (`reports/local-20260820T013718Z`,
  replay analysis `reports/iter-v318-route-commitment/release60-analysis.json`).
- The one allowed repair limited the probe to the first route.  Focused coverage
  was **38/38**, compileall passed, static retained the inherited profile, and
  smoke was **4/4** (`reports/local-20260820T014542Z`), but the rotated screen
  regressed to **6-9** with **73,820/85,940 Ti** and zero reliability failures
  (`reports/local-20260820T014615Z`).
- Reject v318 after the repair.  The temporary probe/test were removed and
  candidate Defender parity with immutable v0044 was restored.  Rollback
  focused coverage was **34/34**, compileall passed, static retained the
  inherited exit-2 profile, and rollback smoke was **4/4**
  (`reports/local-20260820T014853Z`).  No promotion or platform operation
  occurred.  Experiment: `experiments/v0044-visible-route-commitment-gate-v318.md`.

### v317 bounded Core-facing route planner rejected and rolled back — 2026-08-20T01:26:06Z

- Top-team deliberate route geometry motivated a bounded replacement for the
  v0044 CHAIN walker.  A fully visible cardinal BFS planned Core-facing links,
  waited through transient Builder occupancy, and fell back on uncertainty;
  source selection, Store, spending, workforce, roles/tasks, combat, package,
  upload, activation, and live state were unchanged.
- Initial planner/seed/economy/defense coverage was **39/39**, compileall
  passed, smoke **4/4** (`reports/local-20260820T012000Z`), and static retained
  the inherited 15 stale imports plus two navigation assertions.  The 15-map
  screen was command-clean but **2-13**, collection **44,160/61,230 Ti**, zero
  no-delivery/TLE/suspicious rows (`reports/local-20260820T012025Z`).
- One planner-only repair activated BFS only for obstacle detours.  Focused
  remained **39/39**, smoke **4/4** (`reports/local-20260820T012311Z`), but the
  screen was only **8-7**, collection **45,280/59,000 Ti**, still with zero
  no-delivery/TLE/suspicious rows (`reports/local-20260820T012333Z`).
- Reject v317 after the repair without a long gate.  Temporary BFS state,
  executor, and focused test were removed; recursive parity with immutable
  v0044 is zero at
  `reports/iter-v317-planned-route-rollback-source-parity.diff` and
  `rollback-main-parity.diff`.  Rollback focused coverage **34/34**,
  compileall passed, static retained the inherited profile, and rollback smoke
  **4/4** (`reports/local-20260820T012606Z`).  No promotion or platform
  operation occurred.  Experiment:
  `experiments/v0044-bounded-core-facing-route-planner-v317.md`.

### v316 verified source-route reuse rejected at release gate — 2026-08-20T01:14:08Z

- Top-team route ownership and the live many-conveyors/low-source failure
  motivated a bounded source-side reuse lifecycle.  After one completed route,
  a Builder could attach a new Harvester to a fully visible fixed-output belt
  only when a directed walk reached our Core; unknown/gap/cycle/Splitter
  routes fell back to the existing chain.  No Store, role/task, combat,
  navigation, package, upload, activation, or live state changed.
- Initial focused route/seed/economy/defense coverage was **37/37**,
  compileall passed, smoke **4/4** (`reports/local-20260820T010212Z`), and
  static retained the inherited 15 stale imports plus two navigation
  assertions.  The 15-map screen was **6-9**, collection **69,490/78,790 Ti**,
  command-clean with zero candidate no-delivery/TLE/suspicious rows
  (`reports/local-20260820T010238Z`).
- One reuse-only repair restricted the handoff to exactly the second route.
  Focused remained **37/37**, smoke was **4/4** (`reports/local-20260820T010449Z`),
  and the screen reached **8-7**, collection **93,840/81,370 Ti**, with zero
  no-delivery/TLE/suspicious rows (`reports/local-20260820T010509Z`).
- The 60-game release gate reversed the apparent edge: **24-36**, collection
  **260,460/289,270 Ti**, one comparator no-delivery and zero candidate
  TLE/suspicious rows, max p99/peak **1,540/5,506 us**
  (`reports/local-20260820T010727Z`).  Reject v316 at the long gate.  Temporary
  helper/test edits were removed; recursive parity with immutable v0044 is
  zero at `reports/iter-v316-route-reuse-rollback-source-parity.diff` and
  `rollback-main-parity.diff`.  Rollback focused coverage **34/34**,
  compileall passed, static retained the inherited profile, and rollback smoke
  **4/4** (`reports/local-20260820T011408Z`).  No promotion or platform
  operation occurred.  Experiment:
  `experiments/v0044-verified-source-route-reuse-v316.md`.

### v315 verified route-first lifecycle rejected and rolled back — 2026-08-20T00:55:45Z

- Top-team parallel route conversion and fresh one-Harvester/many-Conveyor
  losses motivated a structural first-route lifecycle.  On long boards a
  non-attacker reserved an ore tile, laid a Core-facing conveyor chain, then
  returned to build the Harvester; short boards and later routes stayed on
  v0044.  No Store, combat, role/task, package, upload, activation, or live
  state changed.
- Initial route/seed/economy/defense focused coverage was **38/38**,
  compileall passed, smoke was **4/4** (`reports/local-20260820T004941Z`),
  and static retained the inherited 15 stale-import errors plus two navigation
  assertions.  The 15-map screen was command-clean at **7-8**, collection
  **63,600/59,690 Ti**, zero no-delivery/TLE/suspicious rows, and max
  p99/peak **1,196/5,542 us** (`reports/local-20260820T005003Z`).
- One lifecycle-only repair limited route-first to early-distance sources.
  Focused remained **38/38**, smoke was **4/4** (`reports/local-20260820T005245Z`),
  but the screen was only **8-7**, collection **69,210/72,620 Ti**, with one
  candidate no-delivery row (`reports/local-20260820T005310Z`).
- Reject v315 without a long gate.  Temporary source/test edits were removed;
  recursive parity with immutable v0044 is zero at
  `reports/iter-v315-route-first-rollback-source-parity.diff` and
  `rollback-main-parity.diff`.  Rollback focused coverage was **34/34**,
  compileall passed, static retained the inherited profile, and rollback
  smoke was **4/4** (`reports/local-20260820T005545Z`).  No release or platform
  operation occurred.  Experiment:
  `experiments/v0044-verified-route-first-lifecycle-v315.md`.

### v314 opening-economy contract rejected and rolled back — 2026-08-20T00:41:07Z

- Fresh live replay evidence showed a one-Harvester/18-Conveyor/no-delivery
  failure.  v314 made dynamic Builders prefer the existing Harvester-to-chain
  loop during Core OPENING/CONVERTING/CRISIS phases, preserving home threats and
  active repairs; no Store, route geometry, combat, or platform policy changed.
- Initial focused coverage was **33/33**, compileall passed, smoke was **4/4**
  (`reports/local-20260820T003358Z`), and `make static` retained the inherited
  15 stale-import errors plus two navigation assertions.
- The 15-map screen was command/delivery-clean but **3-12**, collecting
  **34,850/60,110 Ti** (`reports/local-20260820T003507Z`).  One bounded repair
  restricted the contract to CRISIS; focused remained **33/33**, smoke was
  **4/4** (`reports/local-20260820T003734Z`), but the screen only reached
  **7-8** with one candidate no-delivery row and **57,070/70,210 Ti**
  (`reports/local-20260820T003751Z`).
- Reject v314.  Temporary code/tests were removed and recursive parity with
  immutable v0044 is zero (`reports/iter-v314-opening-economy/rollback-source-parity.diff`,
  `rollback-main-parity.diff`).  Rollback focused was **30/30**, compileall
  passed, rollback smoke was **4/4** (`reports/local-20260820T004107Z`), and
  static remains the inherited exit-2 profile.  No release, upload, activation,
  or live transition occurred; next risk is route-first/verified-sink
  construction, not another global role/lease/Launcher handoff.

### v306 coordinated phase/role-lease Launcher rewrite — rejected after one bounded repair — 2026-08-19

- Top-team replay audit showed two opening architectures: control-first teams
  use early Launchers/Barriers while retaining a small route, while
  economy-first teams run parallel route owners and deliver early.  v306
  implemented a deterministic map-context phase/lease coordinator, dispatched
  Launchers, and added strict `can_launch`/progress checks.
- The initial candidate passed **42/42** focused tests, compileall, smoke
  **4/4**, and all 15 scheduled games were command-clean, but lost **3–12** to
  immutable v0044 at `reports/local-20260819T212347Z`.
- One bounded repair required three completed routes before assault leases and
  one completed route before a control Launcher.  It passed **44/44** focused
  tests, compileall, smoke **4/4** at `reports/local-20260819T213041Z`, and
  remained command-clean, but only reached **6–9**, collected **67,830 vs
  85,270 Ti**, and had no delivery on GlacierKeep and Royale.  Replay analysis
  is `reports/iter-v306-architecture-audit-repair/replay-analysis.json`.
- Reject v306.  The temporary dispatcher, Launcher lifecycle, identifiers,
  and focused test were removed; recursive production parity with immutable
  v0044 is zero at
  `reports/iter-v306-architecture-audit-repair/rollback-source-parity.diff`.
  Rollback focused coverage was **34/34**, compileall passed, static retained
  the inherited 15 obsolete imports plus two navigation assertions, and
  rollback smoke was **4/4** at `reports/local-20260819T213523Z`.
- No long gate, package, upload, activation, or live transition occurred.
  v105 remains the operational rollback target and live v107 remains
  `active_observing`.  Experiment:
  `experiments/v0044-coordinated-phase-launcher-v306.md`.

### v305 crisis-only primary-attacker income rescue — rejected after bounded repair — 2026-08-19

- Fresh v107 loss evidence suggested a narrow crisis handoff: only the
  designated primary attacker could re-enter the existing Defender economy
  loop while the delayed Store phase was `ECONOMY_PHASE_CRISIS` and the Core
  siege beacon had no missing HP.  Normal attacker, dynamic-worker, route,
  Store, and live policy remained unchanged.
- The initial candidate passed **37/37** focused tests, compileall, and smoke
  **4/4** at `reports/local-20260819T210054Z`, but its 15-map screen collapsed
  to **2–13** with collection **40,970/87,230 Ti** (candidate/comparator),
  despite mean first delivery **21.67/24.47** turns.
- One bounded repair capped each crisis episode at a 24-round pulse.  It
  passed **38/38** focused tests, compileall, and smoke **4/4** at
  `reports/local-20260819T210413Z`; the screen improved to **7–8** with
  collection **76,530/87,670 Ti**, first delivery **30.67/31.53**, and zero
  TLE/suspicious rows (max p99/peak **1,515/5,794 us**), but no paired edge.
- Reject v305 after the allowed repair.  Temporary production/test edits were
  removed; candidate production parity with immutable v0044 is zero at
  `reports/iter-v305-crisis-primary-attacker/rollback-source-parity.diff`.
  Rollback focused coverage was **34/34**, compileall passed, static retained
  the inherited 15 obsolete imports plus two navigation assertions, and
  rollback smoke was **4/4** at `reports/local-20260819T210827Z`.
- No longer gate, package, upload, activation, or live transition occurred.
  v105 remains the operational rollback target and live v107 remains
  `active_observing`.  Experiment:
  `experiments/v0044-crisis-primary-attacker-income-rescue-v305.md`.

### v304 post-shell Dynamic Barrier support — rejected at first screen — 2026-08-19

- After three completed routes, confirmed enemy-Core intel, one observed
  Sentinel, and a replacement-route reserve, one nearest Dynamic Builder could
  invoke the existing escape-safe Core Barrier builder once; opening,
  fixed-attacker, Launcher, Store, and live policy were unchanged.
- Focused nearest-defense/seeded-route/economy coverage passed **36/36**,
  compileall passed, smoke was **4/4** at
  `reports/local-20260819T204656Z`, and static retained the inherited 15
  obsolete imports plus two navigation assertions.
- The required 15-map screen was command/delivery-clean but only **8–7**,
  with candidate/comparator collection **86,380/90,890 Ti** and mean first
  delivery **24.47/21.93** turns.  Replay analysis showed max p99/peak
  **1,345/4,592 us**, zero TLE/suspicious rows, and fewer live candidate
  Barriers (**30/55**) and Sentinels (**12/32**).
- Reject without repair or release.  The temporary hook/tests were removed;
  recursive source parity to immutable v0044 is zero at
  `reports/iter-v304-post-shell-barrier/rollback-source-parity.diff`.
  Rollback focused coverage was **34/34**, compileall passed, static retained
  the inherited profile, and rollback smoke was **4/4** at
  `reports/local-20260819T205110Z`.  v105 remains rollback, live v107 remains
  `active_observing`, and no package/upload/activation/live transition occurred.
  Experiment: `experiments/v0044-post-shell-dynamic-barrier-support-v304.md`.

### v303 emergency anti-Launcher home defense — rejected after independent screen — 2026-08-19

- Fresh v107 replays showed early enemy Launchers reaching the home area before
  a completed route.  v303 allowed the existing Core-designated defender to
  build one normal home Gunner before the first route only for a visible enemy
  Launcher inside the existing home radius.
- Initial focused nearest-defense/seeded-route/economy coverage passed
  **36/36**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T202610Z`, and static retained the inherited 15
  obsolete imports plus two navigation assertions.  The initial screen was
  command-clean but **5-10**, collection **51,970/64,840 Ti**; no local
  comparator Launcher was placed, so the branch was not exercised.
- The one bounded repair prevented a second pre-route home Gunner.  Focused
  coverage was **37/37**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T202953Z`, and the repair screen was **8-7** with
  all deliveries and collection **69,010/55,030 Ti**.  An independent screen
  reversed to **6-9**, collection **55,430/64,320 Ti**, with 14/15 first
  deliveries per side; zero TLE/suspicious rows on both screens.
- Reject v303.  Temporary source/tests were removed; recursive parity with
  immutable v0044 is zero at
  `reports/iter-v303-anti-launcher/rollback-source-parity.diff`.  Rollback
  focused coverage was **34/34**, compileall passed, and rollback smoke was
  **4/4** at `reports/local-20260819T203405Z`.  No package, upload, activation,
  or live transition occurred.  v105 remains the operational rollback and
  live v107 remains `active_observing`.  Experiment:
  `experiments/v0044-emergency-anti-launcher-home-defense-v303.md`.

### v302 four-route fixed-attacker economy gate — rejected at first screen — 2026-08-19

- Fresh v107 losses showed the fixed attackers leaving the opening route loop
  with only one-to-three paying Harvesters.  v302 temporarily kept both fixed
  attackers on the existing Defender economy/chain loop until four completed
  routes, then restored the unchanged attack lane.
- Focused nearest-defense/seeded-route/economy coverage passed **35/35**,
  compileall passed, and smoke was four command-clean games at
  `reports/local-20260819T201111Z`.  `make static` retained the inherited 15
  obsolete imports and two navigation assertions.
- The required 15-map screen against immutable v0044 was command-clean but
  negative at **4–11**, with candidate/comparator collection
  **57,920/62,450 Ti** and first delivery **15/15 vs 14/15**.  Replay analysis
  found zero TLE/suspicious rows and max p99/peak **1,391/2,469 us**.
- Reject without repair or release.  Temporary production/test edits were
  removed; recursive source parity with v0044 is zero at
  `reports/iter-v302-four-route/rollback-source-parity.diff`.  Rollback
  focused coverage was **34/34**, compileall passed, and rollback smoke was
  four command-clean games at `reports/local-20260819T201446Z`.  No package,
  upload, activation, or live transition occurred.  v105 remains the
  operational rollback target and live v107 remains `active_observing`.
  Experiment: `experiments/v0044-four-route-fixed-attacker-economy-v302.md`.

### v301 large-board opening Gunner guard — rejected at first screen — 2026-08-19

- Fresh v107 losses on long boards ended before the candidate's round-150
  home-defense window, while opponents had one-to-two Gunners by rounds
  35–60.  v301 allowed exactly one reserve-backed pre-route Gunner after round
  36 only when the board dimensions summed to at least 40; compact maps and
  post-route policy were unchanged.
- Focused nearest-defense/seeded-route/economy coverage passed **38/38**,
  compileall passed, and smoke was **4/4** at
  `reports/local-20260819T195749Z`.  `make static` retained the inherited
  15 obsolete imports and two navigation assertions.
- The 15-map screen against immutable v0044 was command/delivery-clean but
  negative at **7-8**, with candidate/comparator collection
  **75,760/81,020 Ti** and mean first delivery **34.73/27.47** turns.  All
  rows delivered; zero TLE/suspicious rows; max p99/peak **1,492/2,465 us**.
  Evidence: `reports/local-20260819T195814Z` and
  `reports/iter-v301-opening-guard/replay-analysis.log`.
- Reject without repair or release.  The temporary guard/tests were removed;
  the three production files are byte-identical to immutable v0044 (empty
  `reports/iter-v301-opening-guard/rollback-source-parity.diff`).  Rollback
  focused coverage was **34/34**, compileall passed, and rollback smoke was
  **4/4** at `reports/local-20260819T200115Z`.  No package, upload, activation,
  or live transition occurred; v105 remains the operational rollback target
  and live v107 remains `active_observing`.  Experiment:
  `experiments/v0044-large-board-opening-guard-v301.md`.

### v300 verified conveyor-route merge — rejected at first screen — 2026-08-19

- Fresh v107 losses showed late route conversion after Conveyor links were
  removed.  v300 added one strict merge proof: a pending chain tile could feed
  a friendly Conveyor only when its visible fixed-output path reached a
  friendly Core without cycles, enemy/unknown tiles, or Splitter ambiguity.
- The four new merge tests plus nearest-defense/seeded-route/economy coverage
  passed **38/38**, compileall passed, and smoke was **4/4** at
  `reports/local-20260819T194050Z`.  `make static` retained the inherited
  15 obsolete imports and two navigation assertions.
- The 15-map screen against immutable v0044 was command- and delivery-clean
  but negative at **6-9**, with candidate/comparator collection
  **49,920/50,550 Ti** and mean first delivery **30.33/21.53** turns.  There
  were zero no-delivery, TLE, or suspicious rows; max p99/peak was
  **1,465/5,278 us**.  Evidence: `reports/local-20260819T194119Z` and
  `reports/iter-v300-route-merge/replay-analysis.log`.
- Reject without repair or release.  The temporary helper/test were removed;
  candidate `defender.py` is byte-identical to immutable v0044 (empty
  `reports/iter-v300-route-merge/rollback-source-parity.diff`).  Rollback
  focused coverage was **34/34**, compileall passed, and rollback smoke was
  **4/4** at `reports/local-20260819T194550Z`.  No package, upload, activation,
  or live transition occurred; v105 remains the operational rollback target
  and live v107 remains `active_observing`.  Experiment:
  `experiments/v0044-verified-conveyor-route-merge-v300.md`.

### v299 heartbeat-driven permanent route recovery — rejected at first screen — 2026-08-19

- Fresh v107 replay losses showed completed routes going quiet after Conveyor
  removal while the permanent defender continued scouting.  v299 tested one
  bounded heartbeat response: only the Core-designated permanent defender,
  after a completed route and during existing `CONVERTING`/`CRISIS`, returned
  home and repaired at most one visible gap, with bounded blocked expiry.
- Focused coverage passed **39/39**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T192240Z`, and static retained only the inherited 15
  removed-module imports and two navigation assertions.
- The rotated seed-174 screen was command-clean but had one candidate
  no-delivery row: candidate-A finished **8–7** and collected
  **66,440/74,880 Ti** (`reports/local-20260819T192317Z`).  Replay analysis
  showed max p99/peak **1,247/2,456 us**, zero TLE/suspicious rows, and no
  delivery-health edge.
- Reject v299 without repair, release, promotion, package, upload, activation,
  or live transition.  The temporary sweep/test were removed; rollback focused
  coverage was **34/34**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T192608Z`, and recursive candidate-source parity with
  immutable v0044 is zero at
  `reports/iter-v299-route-recovery/rollback-source-parity.diff`.  Full
  record: `experiments/v0044-heartbeat-permanent-route-recovery-v299.md`.
  v105 remains the operational rollback target; live v107 remains
  active-observing.

### v298 opening-economy role handoff — rejected after independent screen — 2026-08-19

- Fresh v107 losses showed pre-route economy-floor Builders remaining permanent
  defenders after a route completed.  v298 tested one bounded lifecycle change:
  only those temporary opening defenders entered the existing dynamic task pool
  after delayed `SLOT_HARVESTER_COUNT` confirmation; the Core-designated
  permanent defender was unchanged.
- Focused coverage passed **34/34**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T190925Z`, and `make static` retained only the
  inherited 15 removed-module imports and two navigation assertions.
- The required seed-172 screen was command/delivery-clean at **8–7** with
  **69,170/72,440 Ti** (`reports/local-20260819T190949Z`).  The independent
  seed-173 screen regressed to **6–9** with **56,090/71,300 Ti**
  (`reports/local-20260819T191136Z`); both sides delivered in all 15 games.
  Replay analysis remained within the inherited budget (seed 172 max
  p99/peak **1,419/4,765 us**; seed 173 **1,304/2,985 us**) with zero TLE or
  suspicious rows.
- Reject v298 without repair, release, promotion, package, upload, activation,
  or live transition.  The temporary code/test were removed; rollback focused
  coverage was **34/34**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T191411Z`, and recursive candidate-source parity with
  immutable v0044 is zero at
  `reports/iter-v298-role-handoff/rollback-source-parity.diff`.  Full record:
  `experiments/v0044-opening-economy-role-handoff-v298.md`.  v105 remains the
  operational rollback target; live v107 remains active-observing.

### v297 large-board workforce-first pressure gate — rejected — 2026-08-19

- Fresh v107 replays showed large-board losses with only 4–7 surviving
  Builders and 1–4 Harvesters versus opponents retaining 8–13 Builders and
  8–13 Harvesters.  v297 tested one map-contextual gate: dynamic pressure and
  new forward Sentinels waited for a global Core-plus-eight roster on boards
  whose dimensions summed to at least 40; compact maps and all route/defense
  behavior were unchanged.
- Focused coverage passed **28/28**, compileall passed, and smoke was **4/4**
  at `reports/local-20260819T184448Z`; static retained the inherited 15
  obsolete imports and two navigation assertions.
- The rotated 15-map screen at `reports/local-20260819T184522Z` was
  command/delivery-clean (**15/15** first deliveries for both sides), with
  zero TLE/suspicious rows, but candidate-A lost **7–8** and collected
  **71,430 vs 71,130 Ti**.  Maximum p99 was **1,392 us** and maximum peak
  callback time **6,258 us**.  The collection edge was not a repeatable
  strategic edge, so v297 failed its first-screen criteria.
- v297 was rejected without repair, release, promotion, package, upload,
  activation, or live-state transition.  Temporary code/tests were removed;
  rollback focused coverage passed **26/26**, compileall passed, rollback
  smoke was **4/4** at `reports/local-20260819T185022Z`, and recursive
  production-source parity with immutable v0044 is zero diff at
  `reports/iter-v297-workforce-first/parity-after-revert.diff`.  Full record:
  `experiments/v0044-large-board-workforce-first-v297.md`.  v105 remains the
  operational rollback target; live v107 remains active-observing.

### v296 teamwide Sentinel spend ledger — rejected at release gate — 2026-08-19

- Fresh v107 replays showed repeated Sentinel replacement churn alongside
  Harvester attrition.  v296 packed a capped lifetime Sentinel-placement
  ledger into the high bits of `SLOT_SENTINEL_COUNT`, preserving legacy live
  count reads and leaving geometry, routes, workforce, and combat priorities
  unchanged.
- Focused coverage passed **33/33**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T181456Z`, and static retained the inherited exit 2.
  The first two rotated 15-map screens were **8–7** and **10–5**, with
  **80,440/69,080 Ti** and **76,630/66,300 Ti**, clean delivery, and zero
  TLE/suspicious rows.
- The complete 60-game release gate at `reports/local-20260819T182124Z` was
  not repeatable: candidate-A won **31–29**, collected **258,830/272,900 Ti**,
  and delivered first on **60/60 vs 59/60**.  Nordkap was **0–4** and
  Icefloe/Drakkarfjord were each **1–3**; all rows were command-clean with
  zero TLE/suspicious output and max p99 **1,494 us**.
- v296 was rejected without repair, promotion, package, upload, activation,
  or live-state transition.  Temporary code/tests were removed; rollback
  focused coverage passed **26/26**, compileall passed, rollback smoke was
  **4/4** at `reports/local-20260819T182838Z`, static retained exit 2, and
  recursive candidate-source parity with immutable v0044 is zero diff at
  `reports/iter-v296-sentinel-ledger/parity-after-revert.diff`.  Full record:
  `experiments/v0044-teamwide-sentinel-spend-ledger-v296.md`.  v105 remains
  the operational rollback target; live v107 was untouched.

### v295 central route-recovery lease — rejected — 2026-08-19

- Fresh v107 losses still ended with one-to-four Harvesters while opponents had
  seven-to-twelve.  v295 centrally reused the delayed `SLOT_DEFENDER_ID` as a
  route lease after five historical routes when no home Gunner purchase was
  pending.  The nearest visible non-fixed Builder was selected; a high-bit
  marker preserved the low-bit Gunner cap and distinguished the lease from
  turret designation.
- Focused coverage passed **32/32**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T180329Z`, and static retained inherited exit 2.  The
  first 15-map screen was command-clean but collapsed to **1–14**, collection
  **49,010/86,520 Ti**, and delivery **14/15 vs 15/15**.  Harvester survival
  included Auroraveil **3/7**, Ragnarok **1/11**, and Royale **0/9**.
- The lease starved rather than recovered the economy, so v295 was rejected at
  the first screen without repair, independent screen, release gate,
  promotion, package, upload, activation, or live-state transition.
- Temporary production/test edits were removed.  Rollback focused coverage
  passed **30/30**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T180637Z`, static retained exit 2, and recursive
  production-source parity with immutable v0044 is zero diff at
  `reports/iter-v295-route-lease-parity-after-revert.diff`.  Full record:
  `experiments/v0044-central-route-recovery-lease-v295.md`; reports:
  `reports/iter-v295-route-lease-*`.  v105 remains the operational rollback
  target; live v107 was untouched.

### v294 throughput-aware economy handoff — rejected — 2026-08-19

- v107's Auroraveil loss showed positive lifetime income despite ending with
  one own Harvester and **5,120 Ti** versus nine Harvesters and **14,430 Ti**
  for the opponent.  v294 tested one bounded fix: a full eight-round rolling
  sum of positive net income had to reach **50 Ti** before a strong historical
  route count could publish PRESSURE; otherwise the dynamic workforce stayed
  in CONVERTING.  Route geometry, workforce targets, tasks, combat, Store
  layout, baseline, and platform state were unchanged.
- Focused coverage was **32/32**, compileall passed, smoke was **4/4** at
  `reports/local-20260819T175026Z`, and static retained the inherited exit 2
  (15 obsolete imports plus two navigation assertions).  The first 15-map
  screen was **9–6** with **60,380/57,560 Ti** and **14/15 vs 15/15** first
  delivery, but included a candidate Royale no-delivery loss.
- The independent all-map screen regressed to **6–9** and
  **56,060/82,440 Ti**, despite **15/15 vs 15/15** delivery.  The initial edge
  was not repeatable, so v294 was rejected without repair, promotion, package,
  upload, activation, or live-state transition.
- The rolling-window code and tests were removed.  Rollback focused coverage
  passed **30/30**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T175524Z`, static retained exit 2, and recursive
  production-source parity with immutable v0044 is zero diff at
  `reports/iter-v294-throughput-handoff/parity-after-revert.diff`.  Full
  record: `experiments/v0044-throughput-aware-economy-v294.md`; reports:
  `reports/iter-v294-throughput-handoff/`.  v105 remains the operational
  rollback target; live v107 was untouched.

### v293 spawn-ring workforce reservation — rejected — 2026-08-19

- Fresh v107 Auroraveil evidence showed five candidate Builders by turn 4,
  no later Builder placements, and core-ring Conveyors filling the same spawn
  ring while the opponent reached 9–13 Builders.  v293 temporarily packed the
  Core workforce target/living count into unused high bits of the legacy
  `SLOT_GUNNER_CAP` slot and deferred optional ring construction while the
  wave was pending.
- Initial focused coverage was **33/33**, compileall passed, and smoke was
  command-clean, but the 15-map screen
  `reports/local-20260819T173239Z` was **5–10** vs v0044 with candidate
  delivery **13/15**.  One bounded repair retained two verified ring links;
  focused coverage stayed **33/33** and `reports/local-20260819T173557Z`
  reached **8–7** with **15/15** delivery, but collection was **42,080 vs
  61,670 Ti**.
- The independent all-map seed screen
  `reports/local-20260819T173801Z` regressed to **5–10** with collection
  **49,810 vs 80,070 Ti**.  The one-game edge was therefore not repeatable;
  v293 was rejected without repair beyond the bounded attempt, release gate,
  package, upload, activation, or live-state transition.
- The signal, gates, and tests were removed.  Recursive production-source
  parity with immutable v0044 is zero diff at
  `reports/iter-v293-spawn-ring/parity-after-revert.diff`.  Rollback focused
  coverage passed **30/30**, compileall passed, rollback smoke was
  command-clean at `reports/local-20260819T174055Z`, and `make static` retains
  the inherited deleted-module imports plus two navigation fast-path
  assertions.  Full record: `experiments/v0044-spawn-ring-workforce-v293.md`;
  reports: `reports/iter-v293-spawn-ring/`.  v105 remains the operational
  rollback target; live v107 was untouched.

### v292 home route-blocker response — rejected — 2026-08-19

- Fresh v107 loss replays showed the candidate ending long boards with only
  1–4 surviving Harvesters while opponents had 6–13; one Glacierkeep replay
  showed an infiltrator replacing destroyed home Conveyors with Barriers.
  v292 added one narrow response: an enemy Barrier became a home threat only
  when a visible friendly Conveyor pointed directly into that tile.  The
  existing nearest-responder and legal Builder-fire path handled the target;
  ordinary Barriers, route/workforce phases, and fixed attackers were unchanged.
- Focused route/defense coverage passed **29/29**, the economy-phase subset
  passed **4/4**, compileall passed, and smoke was **4/4** at
  `reports/local-20260819T171217Z`.  `make static` retained the inherited
  exit 2 from 15 obsolete deleted-module imports and two navigation
  fast-path assertions.
- The rotated 15-map screen `reports/local-20260819T171251Z` was command-clean
  with zero TLEs or suspicious rows, but candidate-A won **7-8** against v0044,
  collected **60,370/46,680 Ti**, and delivered on **14/15 vs 15/15** rows;
  Royale was the candidate no-delivery row.  Maximum p99/peak was
  **1,336/2,412 us**.  No repeatable win-rate or protected-map edge was shown,
  so v292 was rejected without repair or release gate.
- The temporary predicate and three tests were removed.  Rollback focused
  coverage passed **30/30**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T171526Z`, static retained exit 2, and recursive
  production-source parity with immutable v0044 was zero diff.  No package,
  upload, activation, or live transition occurred.  Full record:
  `experiments/v0044-home-route-blocker-v292.md`; reports:
  `reports/iter-v292-route-blocker/`.  v0044 remains local baseline; v107
  remains active-observing and v105 remains the operational rollback target.

### v291 opening hijack signal gate — rejected — 2026-08-19

- v0044 replay evidence suggested the opening Defender could chase an empty
  hostile Harvester and strand the first route worker.  The bounded candidate
  gated only pre-route takeover on a visible carried stack or valid hostile
  accepting Conveyor/Splitter; post-route takeover was unchanged.
- Focused coverage passed **38/38**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained inherited exit 2.  The 15-map screen was
  command/delivery-clean with zero TLEs or suspicious rows, but candidate-A
  won **7-8**, matching v0044's **7-8** reference; Ti was **52,220/57,840**
  versus **47,370/60,630** for the comparator.  Maximum p99/peak was
  **1,417/4,533 us**.
- The resource shift did not add wins or establish a repeatable protected-map
  edge, so v291 was rejected without repair or release gate.  The temporary
  predicate/tests were removed; rollback focused coverage was **34/34**,
  compileall passed, rollback smoke **4/4**, static retained exit 2, and
  recursive production-source parity to immutable v0044 was zero diff.  No
  package, upload, activation, or live transition occurred.
- Full record: `experiments/v0044-opening-hijack-signal-v291.md`; reports:
  `reports/iter-v291-opening-hijack-signal/`.  v0044 remains local baseline;
  v107 remains active-observing and v105 remains the operational rollback.

### v290 teamwide Core intel relay — rejected — 2026-08-19

- Fresh v107 losses suggested that an economic Builder seeing the enemy Core
  could relay its packed position to the fixed attacker through the existing
  delayed Store slot.  The bounded candidate added that observation-only
  relay; routes, workforce, tasks, spending, Sentinel policy, and live state
  were unchanged.
- Focused coverage was **37/37**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained the inherited exit 2.  The 15-map screen was
  command/delivery-clean with no TLE or suspicious rows, but candidate-A won
  **7-8**, collected **47,370/60,630 Ti**, placed **39/54 Sentinels**, and had
  **1/0** no-delivery rows; max p99/peak was **1,310/5,563 us**.
- The relay had no repeatable edge and regressed collection, so v290 was
  rejected without repair or release gate.  The temporary call/helper/tests
  were removed; rollback focused coverage was **34/34**, compileall passed,
  smoke **4/4**, static retained exit 2, and recursive production-source
  parity to immutable v0044 was zero diff.  No package, upload, activation,
  or live transition occurred.
- Full record: `experiments/v0044-teamwide-core-intel-relay-v290.md`; reports:
  `reports/iter-v290-core-intel-relay/`.  v0044 remains local baseline; v107
  remains active-observing and v105 remains the operational rollback target.

### v289 opening takeover firewall — rejected — 2026-08-19

- Fresh v107 loss replays and the v288 protected-map screen showed small own
  opening economies while winners had more Harvesters and a forward shell.
  v289 temporarily gated both enemy-Harvester takeover entry points—the
  Dynamic `TASK_HIJACK` selector and the permanent Defender's direct seeded
  route—until one own route was completed and a Harvester-plus-two-Conveyor
  reserve was funded. Spawn targets, route FSM, fixed attackers, turrets,
  Store layout, and platform state were unchanged.
- Focused coverage passed **36/36**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained inherited exit 2. The first one-sided
  15-map screen was command-clean but failed **5-10**, collection
  **38,880/61,220 Ti**, Harvesters **98/133**, Sentinels **31/57**, and max
  p99/peak **1,443/2,133 us**. An independent rerun already in flight was
  **10-5**, collection **49,210/47,190 Ti**, Harvesters **114/109**, Sentinels
  **54/33**, and max p99/peak **1,281/4,572 us**; both had zero side-swapped
  pairs and were only probes.
- The required 60-game both-side release gate was command-clean with zero
  TLE/suspicious rows but regressed to **20-40**, collection
  **247,270/326,030 Ti**, Harvesters **476/487**, Sentinels **186/261**, and
  Builders **542/561** candidate/comparator. Each side had one analyzer
  no-delivery row; max p99/peak was **1,497/4,681 us**.
- The quick result was an outlier and the firewall suppressed useful pressure;
  v289 is rejected without repair or promotion. Temporary source/tests were
  removed; rollback focused coverage was **34/34**, compileall passed, smoke
  **4/4**, static retained exit 2, and recursive source parity to immutable
  v0044 is zero diff. No package, upload, activation, or live transition
  occurred. Full record: `experiments/v0044-opening-takeover-firewall-v289.md`;
  reports: `reports/iter-v289-opening-takeover/`.
- v0044 remains local baseline. v107 remains active-observing and v105 remains
  the user-requested operational rollback target.

### v288 pressure-phase dynamic forward lease — rejected — 2026-08-19

- Replay evidence suggested a healthy `PRESSURE` phase could leave every
  dynamic Builder harvesting while fixed attackers lacked a forward shell.
  v288 temporarily leased the existing `TASK_ADVANCE` lane to exactly one
  nearest non-fixed Builder after three routes and until the early Sentinel
  target was observed.  Fixed roles, routes, Store layout, prices, and
  Sentinel placement rules were unchanged.
- Focused coverage passed **34/34**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained inherited exit 2 (15 obsolete-module
  imports and two navigation assertions).  The first rotated 15-map screen
  was command/delivery-clean with no TLEs or suspicious rows, but candidate-A
  won only **9-6** while collecting **82,570/88,150 Ti** and placing
  **47/56** Sentinels.  Mean first delivery was **28.7/50.4** turns, but the
  manifest had zero side-swapped pairs and protected economy collapses
  included Fjordgate **40/5,890 Ti** and Valkyrie **360/7,230 Ti**.  Maximum
  p99 was **1,455 us**; no reliability failure occurred.
- The one-sided win edge was not repeatable and the targeted forward-shell /
  collection gate failed.  No repair or second screen was run.  Temporary
  source/tests were removed; rollback focused coverage was **30/30**,
  compileall passed, rollback smoke **4/4**, static retained exit 2, and
  recursive dynamic source parity to immutable v0044 was zero diff.  No
  promotion, package, upload, activation, or live-state transition occurred.
  Full record: `experiments/v0044-pressure-phase-dynamic-forward-lease-v288.md`;
  reports: `reports/iter-v288-pressure-lease/`.
- v0044 remains the local baseline. v107 remains active-observing and v105
  remains the user-requested operational rollback target.

### v287 adaptive alternate-Core probe — rejected — 2026-08-19

- Fresh v107 losses had four-to-eight Harvesters but zero or one forward
  Sentinel. v287 kept the rotational Core prior first, then tried at most two
  aspect-ordered alternate probes only after arrival and a bounded 12-round
  unconfirmed epoch; confirmed intel stopped the search. Economy, routes,
  roles, reserves, tasks, and live state were unchanged.
- Focused coverage passed **36/36**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained inherited exit 2 (15 obsolete imports
  and two navigation assertions). The first seed-172 screen was command and
  delivery clean but regressed to **5-10**, collection **71,010/85,180 Ti**,
  Sentinels **70/76**, and first-delivery means **31.8/69.3** turns with one
  144-turn candidate row. There were no command failures, TLEs, suspicious
  rows, or delivery failures.
- The alternate probe therefore failed its first-screen gate; no repair,
  second screen, long gate, promotion, package, upload, activation, or live
  transition was justified. Temporary source/tests were removed. Rollback
  focused coverage was **34/34**, compileall passed, rollback smoke was
  **4/4**, static retained exit 2, and recursive source parity to immutable
  v0044 was zero diff. Full record:
  `experiments/v0044-adaptive-core-probe-v287.md`; reports:
  `reports/iter-v287-adaptive-core-probe/`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v286 income-backed second-attacker release — rejected — 2026-08-19

- The v107 loss audit showed a first route without enough early forward
  pressure. v286 temporarily designated the first stage-two Builder as a
  second fixed attacker after positive Core income, but only after reserving
  a replacement Harvester route, two Conveyors, and the existing offense
  reserve. Roles, routes, Sentinel gates, tasks, and live state were unchanged.
- Focused coverage passed **35/35**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained inherited exit 2. The first seed-172
  screen was command/delivery-clean at **8-7**, collection **94,930/92,240
  Ti**, but first-delivery means were **41.4/22.6** turns and Sentinels
  **46/64** versus the comparator. Zero TLE/suspicious/delivery failures.
- The first-screen gate failed because the win/collection edge was not
  repeatable and forward pressure regressed. The temporary Core/test changes
  were removed; rollback focused coverage was **34/34**, compileall passed,
  rollback smoke **4/4**, static retained exit 2, and recursive source parity
  to immutable v0044 was zero diff. No second screen, repair, promotion,
  package, upload, activation, or live transition occurred. Full record:
  `experiments/v0044-income-backed-second-attacker-v286.md`; reports:
  `reports/iter-v286-income-second-attacker/`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v285 positive-income first Sentinel transition — rejected — 2026-08-19

- The fresh v107 losses showed four-to-six candidate Harvesters but zero or
  one Sentinel in short Midgard/Yulerune/Frostgate games. v285 changed the
  Core's existing phase publication to expose `CONVERTING` after a positive
  net-income heartbeat even while the delayed route counter was zero, and let
  the existing first-Sentinel path use that phase only with a dynamic reserve
  for one replacement Harvester plus two Conveyors. Geometry, pool, placement,
  routes, and later Sentinel behavior were unchanged.
- Focused coverage passed **35/35**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained inherited exit 2. Seed 172 was clean at
  **8-7**, collection **81,400/71,380 Ti**, Harvesters **117/120**, Sentinels
  **48/56**, and first-delivery means **24.60/21.00** turns. Max p99/peak was
  **1,459/4,660 us** with zero TLE/suspicious rows; first Sentinel placement
  remained late or absent on several candidate losses.
- The first screen therefore failed the required opening-shell/conversion
  edge. No second screen or repair was run. Temporary Core/attacker/test
  changes were removed; candidate production Python is recursively parity-
  checked against immutable v0044. Rollback focused coverage was **34/34**,
  compileall passed, rollback smoke **4/4**, and static retained exit 2. No
  promotion, package, upload, activation, or live transition occurred. Full
  record: `experiments/v0044-positive-income-first-sentinel-v285.md`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v284 post-economy direct-Core sighting — rejected — 2026-08-19

- The fresh v107 loss audit showed funded Dynamic Builders reaching the final
  advance phase with too few forward Sentinels. v284 therefore invoked the
  existing direct/store enemy-Core intel helper only inside
  `TASK_ADVANCE` when no confirmed position existed, preferring that confirmed
  position over a stale task target. Startup, task selection, Defender,
  Sentinel rules, routes, and fixed attackers were unchanged.
- Focused coverage passed **36/36**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained the inherited exit 2 (15 obsolete
  imports plus two navigation assertions). Seed 172 was **7-8** with
  **57,280/54,970 Ti**, Harvesters **97/119**, Sentinels **47/48**, and first
  delivery means **29.80/22.87**. Seed 175 was **8-7** with
  **73,770/61,250 Ti**, Harvesters **113/126**, Sentinels **38/54**, and first
  delivery means **28.00/24.47**.
- Both screens were command/delivery-clean with zero TLE/suspicious rows, but
  the pair was **15-15**: collection **131,050/116,220 Ti**, Harvesters
  **210/245**, Sentinels **85/102**, and first-delivery means **28.90/23.67**.
  The recurring collection edge did not become a win or Sentinel/conversion
  edge, so no repair or long gate was justified.
- The temporary hook and tests were removed; candidate production Python is
  recursively parity-checked against immutable v0044 (excluding caches).
  Rollback focused coverage was **34/34**, compileall passed, rollback smoke
  **4/4**, and static retained exit 2. No promotion, package, upload,
  activation, or live transition occurred. Full record:
  `experiments/v0044-post-economy-direct-core-v284.md` and
  `reports/iter-v284-direct-core/`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v283 post-economy dynamic confirmed-Core consumption — rejected — 2026-08-19

- The fresh v107 match/loss audit showed four-to-eight candidate Harvesters but
  zero or one Sentinel on several losses, while opponents had three-to-six.
  v283 therefore let a Dynamic Builder read a valid `SLOT_ENEMY_CORE` position
  only inside its existing final `TASK_ADVANCE`, so confirmed intel could feed
  the existing Sentinel gate without changing early Defender decisions or
  publishing new intel.
- Focused coverage was **36/36**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained inherited exit 2. Seed 172 was **9-6** with
  **71,790/58,280 Ti**, Harvesters **109/106**, and Sentinels **44/40**;
  seed 175 reversed to **5-10** with **66,040/79,550 Ti**, Harvesters
  **94/138**, and Sentinels **37/46**. Both screens were delivery-clean with
  zero TLE/suspicious rows.
- The paired result was **14-16**, collection **137,830/137,830 Ti**,
  Harvesters **203/244**, Sentinels **81/86**, and delivery **30/30 vs
  30/30**. The post-economy intel read did not produce a repeatable edge, so
  no repair or long gate was justified.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **34/34**, compileall passed, rollback smoke
  **4/4**, and static retained exit 2. No promotion, package, upload,
  activation, or live transition occurred. Full record:
  `experiments/v0044-post-economy-confirmed-core-v283.md` and
  `reports/iter-v283-confirmed-core-*`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v282 watched forward-Sentinel repair lease — rejected — 2026-08-19

- Fresh v107 Drumlin evidence showed four placed forward Sentinels with none
  alive at the end. v282 therefore let the owning attacker heal its most
  recent visible, adjacent, damaged Sentinel during the existing 20-round
  lifetime watch, then resume the normal core lane. Placement, route,
  economy, roles, and non-watched units were unchanged.
- Focused coverage was **36/36**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained inherited exit 2. Seed 172 was **7-8** with
  **61,940/54,540 Ti**, Harvesters **113/110**, and Sentinels **48/46**;
  seed 175 was **6-9** with **47,570/63,330 Ti**, Harvesters **106/125**, and
  Sentinels **34/53**. Both screens were delivery-clean and had zero
  TLE/suspicious rows.
- The paired result was **13-17**, collection **109,510/117,870 Ti**,
  Harvesters **219/235**, Sentinels **82/99**, and delivery **30/30 vs
  30/30**. The support lease did not produce a repeatable edge, so no repair
  or long gate was justified.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **34/34**, compileall passed, rollback smoke
  **4/4**, and static retained exit 2. No promotion, package, upload,
  activation, or live transition occurred. Full record:
  `experiments/v0044-watched-sentinel-repair-v282.md` and
  `reports/iter-v282-sentinel-support-*`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v281 compact visible-income first Sentinel — rejected — 2026-08-19

- Fresh active-v107 loss evidence showed compact Antler with no forward
  Sentinel despite a first Harvester on turn 8, and Drumlin with four placed
  Sentinels that all died. v281 therefore allowed exactly one early Sentinel on
  cramped symmetric boards when a fixed attacker directly saw a friendly
  Harvester and the bank could still fund a replacement route plus the fixed
  offense reserve. Non-cramped maps and later Sentinel gates were unchanged.
- Focused nearest-defense/economy-phase/seeded-route coverage was **37/37**,
  compileall passed, `make smoke` was **4/4**, and `make static` retained the
  inherited exit 2. Seed 172 screened **8-7** (**77,280/66,570 Ti**), but the
  independent seed 175 screen reversed to **5-10** (**39,090/55,300 Ti**).
  Both screens were runtime-clean; candidate first delivery was **15/15** and
  **14/15** versus **15/15** for the comparator.
- The paired result was **13-17**, collection **116,370/121,870 Ti**,
  Harvesters **198/270**, Sentinels **75/98**, and delivery **29/30 vs
  30/30**. The timing proof is rejected without repair or long gate.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **34/34**, compileall passed, rollback smoke
  **4/4**, and static retained exit 2. No promotion, package, upload,
  activation, or live transition occurred. Full record:
  `experiments/v0044-compact-visible-sentinel-v281.md` and
  `reports/iter-v281-compact-sentinel/`.
- v0044 remains the local baseline. v107 remains active-observing and v105 is
  the user-requested operational rollback target.

### v280 fixed-attacker replacement — rejected — 2026-08-19

- Latest rated v107 match `5f60bd33-ec8d-4275-92bb-fafbbf24cd77` showed the
  active bot losing Antler and Drumlin without a surviving forward Sentinel,
  while the opponents had four and twelve. v280 therefore tested one-shot
  reassignment of a confirmed-dead fixed attacker to the next Core spawn.
- Focused coverage was **37/37**, compileall passed, `make static` retained
  inherited exit 2, and smoke was **4/4**. Seed 172 screened **8-7** with
  **50,470/48,290 Ti**, **118/114 Harvesters**, and **49/50 Sentinels**;
  seed 175 screened **7-8** with **53,230/58,550 Ti**, **104/111 Harvesters**,
  and **48/41 Sentinels**. Both screens were delivery-clean (**15/15 vs
  15/15**) with zero TLE/suspicious rows.
- The paired result was **15-15**, **103,700/110,840 Ti**, **222/225
  Harvesters**, and **97/91 Sentinels**. The replacement floor did not produce
  a repeatable win edge, so no repair or long gate was justified.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **34/34**, compileall passed, smoke **4/4**,
  and static retained exit 2. No promotion, package, upload, activation, or
  live transition occurred. Full record:
  `experiments/v0044-fixed-attacker-replacement-v280.md` and
  `reports/iter-v280-attacker-replacement/`.
- v0044 remains the local baseline. v107 is still active-observing and v105
  remains the user-requested operational rollback target.

### v105 rollback target selected — 2026-08-19

- Fresh platform status and submission-list checks confirmed that v105 is
  still present, `ready`, and available for activation. The platform’s actual
  active submission is v107; the stale local active-version value was refreshed
  with `scripts/live_operator.py observe` (`reports/live-observe-20260819T135856Z`).
- At the user’s direction, `state/live_state.json` now records **v105** as the
  rollback target, with its recorded 0.5 live score and +0.079182 adjusted
  residual. v101 is retained as the previous fallback reference; v107 remains
  active-observing and no activation or rollback transition was performed.
- Candidate source and the v0044 local baseline were not changed. Evidence and
  raw status/list output are under `reports/rollback-reference-v105-20260819T135832Z/`.

### v279 visible claimed-ore target handoff — rejected after one repair — 2026-08-19

- Replay review found a plausible stale-target path: a Builder remembers ore,
  another Builder occupies it with a Harvester, and the first Builder keeps
  stopping one tile away. v279 first cleared any occupied visible ore target
  and immediately reused the existing picker.
- Focused coverage was **33/33**, compileall passed, `make static` retained
  inherited exit 2, and smoke was **4/4**. Seed 172 regressed to **5-10**,
  **62,810/98,080 Ti**, delivery **15/15 vs 15/15**, and Harvesters
  **105/129**, with zero TLE/suspicious rows.
- The one repair restricted invalidation to a visible friendly Harvester.
  Focused coverage remained **33/33**, compileall/static/smoke kept the same
  profile, and seed 172 was **4-11** (**64,120/64,410 Ti**) while seed 175 was
  **5-10** (**55,270/89,020 Ti**); both delivered **15/15 vs 15/15** and had
  zero TLE/suspicious rows. The repair pair was **9-21** and
  **119,390/153,430 Ti**.
- The hypothesis is rejected. Candidate source was restored recursively
  byte-identically to immutable v0044; rollback focused coverage was **31/31**,
  compileall passed, smoke **4/4**, and static retained exit 2. No release
  gate, promotion, package, upload, activation, or live transition occurred.
  Full record: `experiments/v0044-claimed-ore-target-handoff-v279.md` and
  `reports/iter-v279-claimed-ore-handoff/`.
- v0044 remains the local baseline. v105 remains the requested historical
  rollback reference at 142/275 (**51.64%**); v101 remains the guarded
  operational fallback.

### v278 long-board income-backed second Sentinel — rejected — 2026-08-19

- Fresh live v105 evidence showed a winner reaching three forward Sentinels
  with four Harvesters while the losing side had none. v278 therefore allowed
  a second early Sentinel only after one completed route, a Core converting or
  pressure phase, and a perimeter of at least 60.
- Focused coverage was **34/34**, compileall passed, `make static` retained
  inherited exit 2, and smoke was **4/4**. Seed 172 was **7-8** with
  **68,900/76,640 Ti**, delivery **15/15 vs 15/15**, and Sentinel placements
  **46/44**. Seed 175 was **7-8** with **43,120/51,100 Ti**, delivery
  **14/15 vs 15/15**, and placements **39/50**. The screens were command-clean;
  the second had one candidate no-delivery row and neither had TLE/suspicious
  output.
- The paired result was **14-16**, collection **112,020/127,740 Ti**, and
  delivery **29/30 vs 30/30**. Candidate route conversion regressed despite
  the extra Sentinel, so no repair or long gate was justified.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **31/31**, compileall passed, smoke **4/4**,
  and static retained exit 2. No release gate, promotion, package, upload,
  activation, or live transition occurred. Full record:
  `experiments/v0044-long-board-second-sentinel-v278.md` and
  `reports/iter-v278-long-board-sentinel/`.
- v0044 remains the local baseline. v105 remains the requested historical
  rollback reference at 142/275 (**51.64%**); v101 remains the guarded
  operational fallback.

### v277 large-board income-backed workforce relay — rejected after one repair — 2026-08-19

- Fresh live Drakkarfjord evidence showed the active v105 bot stopping at
  eight Builders and three Harvesters while the winner reached twelve of each.
  v277 raised the staged target from eight to ten only after the first route,
  a positive Core income heartbeat, and a board perimeter of at least 48.
- Focused coverage was **33/33**, compileall passed, `make static` retained
  inherited exit 2, and smoke was **4/4**. Seed 172 was **9-6** with
  **96,140/93,380 Ti**; seed 175 was **7-8** with **62,740/64,580 Ti**. Both
  were delivery-clean (**15/15 vs 15/15**) with zero TLE/suspicious rows, but
  the pair was only **16-14** and collection was nearly flat (**158,880 vs
  157,960 Ti**).
- The one bounded repair narrowed the perimeter threshold from 48 to 60.
  Focused coverage remained **33/33**, compileall passed, static retained
  exit 2, and smoke was **4/4**. Seed 172 was **10-5**
  (**71,850/61,710 Ti**) and seed 175 was **4-11** (**41,440/55,870 Ti**),
  both delivery-clean and reliability-clean. The repair pair was **14-16**
  with **113,290/117,580 Ti**, so the hypothesis was rejected.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **31/31**, compileall passed, smoke **4/4**,
  and static retained exit 2. No release gate, promotion, package, upload,
  activation, or live transition occurred. Full record:
  `experiments/v0044-large-board-income-workforce-v277.md` and
  `reports/iter-v277-large-board-workforce/`.
- v0044 remains the local baseline. v105 remains the requested historical
  rollback reference at recorded live score **0.5** (142/275, **51.64%**);
  v101 remains the guarded operational fallback.

### v276 terminal-dead Harvester outlet recovery — rejected after one repair — 2026-08-19

- v275's Drakkarfjord replay delivered first at turn 601 versus 82 for the
  comparator despite seven Harvesters and 84 surviving Conveyors. v276 tested
  whether a visibly terminal-dead Conveyor outlet was falsely counted as an
  accepting Harvester neighbor, allowing the existing adjacent orphan
  reconnect to seed a replacement branch.
- The initial rule passed focused **33/33**, compileall, and smoke **4/4**;
  static retained inherited failures. Seed 172 was **8-7** with
  **41,950/61,480 Ti** and delivery **15/15 vs 14/15**; seed 175 was **6-9**
  with **50,640/62,830 Ti** and delivery **15/15 vs 14/15**. Both screens
  were command-clean with zero TLE/suspicious rows, but the aggregate was
  **14-16** and collection regressed.
- The one bounded repair restricted the rule to after the first completed
  route. Focused coverage was **34/34**, compileall passed, smoke **4/4**, and
  static retained the same inherited failures. Seed 172 was **5-10** with
  **61,780/59,960 Ti** and delivery **14/15 vs 15/15**; seed 175 was **6-9**
  with **69,050/77,780 Ti** and delivery **15/15 vs 15/15**. The repaired
  aggregate was **11-19**, **130,830/137,740 Ti**, so the hypothesis was
  rejected.
- Candidate production source was restored recursively byte-identically to
  immutable v0044; rollback focused coverage was **31/31**, compileall passed,
  smoke **4/4**, and static retained exit 2. No release gate, promotion,
  package, upload, activation, or live transition occurred. Full record:
  `experiments/v0044-terminal-dead-outlet-recovery-v276.md` and
  `reports/iter-v276-terminal-dead-outlet/`.
- v0044 remains the local baseline. The refreshed live report observes v105
  at current score **0.5**; v105 remains the requested historical rollback
  reference while v101 stays the guarded operational fallback.

### v275 post-chain visible repair lease — rejected after one repair — 2026-08-19

- v274 replay audit showed geometrically complete routes later losing visible
  Conveyor links while their former owner immediately resumed scouting. v275
  gave a successful chain owner a short visible-gap repair lease while
  publishing the existing Harvester milestone immediately.
- Focused coverage was **34/34**, compileall passed, smoke **4/4**, and static
  retained inherited failures. The two rotated screens were **7-8** and **9-6**
  (combined **16-14**, **151,730 vs 145,170 Ti**, delivery **29/30 vs 30/30**),
  so the 60-game gate ran. It finished **28-32**, **242,800 vs 257,220 Ti**,
  delivery **58/60 vs 59/60**, max p99/peak **1,396/2,602 us**, and zero
  command/TLE/suspicious rows. Drakkarfjord, Fjordgate, Icefloe, Ragnarok,
  Royale, and Valkyrie each fell to **1-3**.
- The one bounded repair shortened the lease from 12 to 6 rounds. Seed 172
  was **8-7**, **53,710 vs 48,550 Ti**, delivery **14/15 vs 15/15**; seed 175
  was **7-8**, **69,500 vs 75,780 Ti**, delivery **15/15 vs 15/15**. The repair
  pair was **15-15** and **123,210 vs 124,330 Ti**, so the iteration stopped.
- Candidate source was restored recursively byte-identically to immutable v0044;
  rollback focused coverage was **31/31**, compileall passed, smoke **4/4**,
  and static retained exit 2. No promotion, package, upload, activation, or
  live transition occurred. Full record:
  `experiments/v0044-post-chain-repair-lease-v275.md` and
  `reports/iter-v275-post-chain-repair-lease/`.
- v0044 remains local baseline. v107 remains active-observing and v101 the
  guarded operational rollback; v105 remains only the requested known-bad
  historical reference (142/275, **51.64%**).

### v274 route-preserving opening receiver — rejected after one repair — 2026-08-19

- v107 GlacierKeep evidence and v273 diagnostics showed the Defender filling
  all eight Core-adjacent receiver Conveyors before the first Harvester route.
  v274 deferred Dynamic Builder ring errands until the first completed route
  and initially capped opportunistic receivers at two.
- Focused coverage was **34/34**, compileall passed, smoke **4/4**, and static
  retained the inherited failures. Initial screens were **6-9** (seed 172,
  **74,940 vs 72,780 Ti**, delivery **15/15 vs 14/15**) and **7-8** (seed 175,
  **60,140 vs 57,680 Ti**, delivery **15/15 vs 15/15**). Both were command- and
  reliability-clean, but the aggregate was **13-17**; long-board routes were
  sometimes much later.
- The single bounded repair raised the allowance to four receivers while
  retaining the no-Dynamic-ring-walk gate. Repair screens were **9-6** (seed
  172, **63,960 vs 55,990 Ti**) and **6-9** (seed 175, **63,280 vs 83,610 Ti**),
  both **15/15 vs 15/15** deliveries and zero TLE/suspicious rows. The paired
  result was **15-15**, so no release gate ran.
- The candidate source was restored recursively byte-identically to immutable
  v0044; rollback focused coverage was **31/31**, compileall passed, smoke
  **4/4**, and static retained the inherited exit 2. No promotion, package,
  upload, activation, or live transition occurred. Full record:
  `experiments/v0044-route-preserving-opening-receiver-v274.md` and
  `reports/iter-v274-opening-receiver/`.
- v0044 remains the local baseline. v107 remains active-observing; v101 is the
  guarded operational rollback because v105 is a known-bad historical
  reference (142/275, **51.64%**) despite the requested v105 rollback.

### v273 delivery-gated stage-two workforce — rejected — 2026-08-19

- Fresh v107 GlacierKeep evidence showed eight Builders, one non-delivering
  Harvester, and no usable titanium before the first route while the opponent
  had four Harvesters and a live delivery. v273 removed the fixed-round
  stage-two workforce fallback so reinforcement stayed route-gated.
- Focused unittest coverage was **32/32**, compileall passed, smoke was
  **4/4**, and `make static` retained the inherited failures. The pytest
  module was unavailable (`No module named pytest`), so the equivalent
  unittest subset was used.
- Seed 172 was **7-8** with **70,880 vs 74,440 Ti** and deliveries **15/15 vs
  14/15**; seed 175 was **7-8** with **41,960 vs 49,640 Ti** and deliveries
  **14/15 vs 15/15**. Both screens were command-clean with zero TLE/suspicious
  rows. The one allowed reserve-backed one-Builder repair produced seed 172
  **8-7**, **67,850 vs 64,320 Ti**, and seed 175 **6-9**, **51,930 vs 64,310
  Ti**, both **15/15 vs 15/15** deliveries. The repaired aggregate was still
  **14-16**, so no release gate ran.
- The candidate source was restored recursively byte-identically to immutable
  v0044; rollback focused coverage was **31/31**, compileall passed, smoke
  **4/4**, and static retained the inherited exit 2. No promotion, package,
  upload, activation, or live transition occurred. Full record:
  `experiments/v0044-delivery-gated-stage2-v273.md` and
  `reports/iter-v273-delivery-gated-workforce/`.
- v0044 remains the moving local baseline. v107 remains active-observing;
  v101 remains the guarded operational rollback because v105 is a known-bad
  historical reference (142/275, **51.64%**) despite the requested v105
  rollback reference.

### v272 two-responder active logistics infiltrator intercept — rejected — 2026-08-19

- v271 release replay analysis found more hostile Builder attacks on our home
  logistics in losses than wins. The candidate already hijacks/raids enemy
  logistics, so v272 isolated defense: a visible enemy Builder adjacent to a
  friendly Harvester, Conveyor, or Splitter could admit the two nearest
  non-attacker Builders to the existing home-threat strike task.
- The adjacency-only implementation passed focused **32/32**, compileall, and
  smoke **4/4**, with static retaining only inherited failures, but its screen
  was **3-12**, collection **44,390 vs 95,150 Ti**, and one candidate
  no-delivery row (`reports/local-20260819T113347Z`).
- The one bounded repair required the adjacent friendly route asset to be
  visibly damaged before admitting the second responder. Focused coverage was
  **33/33**, compileall passed, smoke **4/4**, and static retained the same
  inherited failures. Seed 175 was **8-7**, **74,850 vs 59,920 Ti**, deliveries
  **15/15 vs 14/15** (`reports/local-20260819T113706Z`); the fair seed-172
  repeat was **7-8**, **58,810 vs 57,280 Ti**, deliveries **14/15 vs 15/15**
  (`reports/local-20260819T113914Z`). Both were command-clean with zero
  TLE/suspicious rows; paired screens combined to **15-15** and **29/30**
  deliveries each.
- Reject v272. The repair removed the overreaction but did not beat the
  v0044 baseline, so no long gate, package, upload, activation, or live-state
  transition was justified. Candidate source was restored byte-identically to
  immutable v0044 (`reports/iter-v272-two-responder-infiltrator/rollback-source.diff`);
  rollback focused was **30/30**, compileall passed, smoke **4/4**, and static
  retained the inherited failures. Full record:
  `experiments/v0044-two-responder-active-infiltrator-v272.md`.
- Historical platform v105 remains a user-requested but known-bad reference
  (142/275 games, **51.64%**, previously rolled back to v101); v101 remains
  the guarded operational rollback while v107 is still active-observing.

### v271 income-heartbeat economy/offense handoff — promoted locally — 2026-08-19

- v106 loss replays showed dynamic Builders leaving the economy from a
  historical geometric route count even when the Core had not observed recent
  titanium income. v271 packs an economy phase into the high bits of the
  existing ore cursor, preserves those bits during ore advertisements, and
  keeps dynamic Builders on SCOUT/CHAIN until a strong route milestone plus a
  recent income heartbeat are both real. Fixed attackers, infiltration,
  Sentinel/Barrier policy, and route geometry are unchanged.
- Focused phase/nearest-defense coverage was **30/30**, compileall passed,
  smoke was **4/4**, and static retained only the inherited failures. Reports:
  `reports/iter-v271-income-heartbeat-handoff/focused.log`, `compileall.log`,
  `static.log`, and `smoke.log`.
- Independent all-map screens were **9-6** (seed 172) and **7-8** (seed 175),
  both delivery-clean with zero TLE/suspicious rows; combined collection was
  **113,590 vs 113,400 Ti**. Reports:
  `reports/local-20260819T105712Z` and `reports/local-20260819T105911Z`.
- The 60-game release gate was **33-27** candidate wins, collection
  **293,190 vs 269,970 Ti**, first delivery **60/60 vs 58/60**, mean delivery
  **30.67 vs 62.90 rounds**, zero command failures/TLE/suspicious rows, and
  max p99/peak **1,550/2,641 us**. Report:
  `reports/local-20260819T110125Z` with parsed diagnostics in
  `reports/iter-v271-income-heartbeat-handoff/release-60-analysis.json`.
- Promote v271 as the moving local baseline; retain immutable v0043 as
  rollback. Package/upload/activation remain separate guarded operations.
  Live v107 is now active-observing with v101 as the preserved rollback target.
- Remote sanity match `f1c597a2-1a7d-425a-b19b-8177ef1d6efe` finished **2-3**
  (candidate won sprint/vault; v0043 won bridge/crossfire/aurora), with no
  runtime error; records are under `reports/remote-20260819T111559Z`.
- Before deploying, live autopilot found v106 at **46/95** wins (0.4842) over
  19 rated series versus v101's 0.7000 and rolled it back safely to v101
  (`reports/live-rollback-20260819T111545Z`). The guarded v0044 package
  (`104a851d29678ca2b1cf6c8fae241196feb496aef3da733e5871d53531a618e4`) was
  then activated as platform **v107** at 2026-08-19T11:17:51Z; v101 remains
  rollback (`reports/live-deploy-20260819T111731Z`).

### v270 permanent-Defender home-route interceptor — rejected — 2026-08-19

- Fresh v106 replay evidence showed a real infiltration sequence: an enemy
  Builder removes a friendly home Conveyor and places an enemy Barrier on its
  exact output tile. v270 assigned only the permanent Defender to respond to a
  visible enemy Barrier on that exact home Conveyor output, preserving dynamic
  route workers. Enemy Barriers were attacked with `can_fire` (the rules do not
  permit `destroy` on enemy buildings); the existing belt repair rebuilt the
  empty tile after clearance.
- Focused coverage was **31/31**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two rolled-back
  navigation assertions. The configured 15-map screen was clean but **7-8**,
  **62,860 vs 75,850 Ti**, zero TLE/suspicious rows, max p99 **1,479 us**
  (`reports/local-20260819T103626Z`).
- The independent rotated screen was also **7-8**, **54,820 vs 61,510 Ti**,
  with one candidate no-delivery row and max p99 **1,393 us**
  (`reports/local-20260819T103844Z`). Reject v270 without a longer gate.
- Temporary source/tests/config were removed and exact v0043 parity is zero at
  `reports/iter-v270-permanent-defender-home-route-interceptor/rollback-source.diff`;
  rollback focused **26/26**, compileall passed, and smoke **4/4** at
  `reports/local-20260819T104118Z`. No promotion, package, upload, activation,
  or live-state operation occurred. Full record:
  `experiments/v0043-permanent-defender-home-route-interceptor-v270.md`.

### Next: observe v271 and inspect live conversion/reliability before the next hypothesis

- The income heartbeat produced a local release-scale edge without delivery or
  reliability regression. Preserve v0043 for rollback, package/submit v271
  through the guarded workflow, and use live evidence to decide whether the
  phase window needs a new structural follow-up.

### v269 cardinal navigation fast path — rejected — 2026-08-19

- Fresh v106 diagnostics found a live reliability failure: one Torsko game had
  **1,082** TLE callbacks and several Coreflood/Torsko rows reached p99
  execution of **6.8–10.0 ms**. v269 tried to avoid the full visible-tile BFS
  for clear cardinal movement and safe fleeing, retaining `can_move`, danger,
  visited-state, and BFS fallback semantics.
- Initial focused coverage was **32/32**, compileall passed, smoke **4/4**, and
  `make static` exited 2 only for the inherited 15 obsolete-module imports;
  the navigation fast-path assertions passed. The configured 15-map screen
  was command/delivery-clean but **7-8**, **80,420 vs 88,030 Ti**, with
  p99/peak **1,004/1,937 us** (`reports/local-20260819T101614Z`).
- Independent rotation was also clean but **5-10**, **100,660 vs 110,090 Ti**,
  p99/peak **1,032/2,409 us** (`reports/local-20260819T101827Z`). One bounded
  repair restricted the shortcut to row/column-aligned targets; focused was
  **31/31**, compileall passed, static retained the same imports, and smoke
  **4/4**, but its configured screen fell to **6-9**, **64,760 vs 75,140 Ti**
  (`reports/local-20260819T102222Z`). Reject v269 without a second rotation
  or long gate.
- Temporary source/tests were removed and exact v0043 parity is zero at
  `reports/iter-v269-navigation-fast-path/rollback-source.diff`; rollback
  focused **26/26**, compileall passed, and rollback smoke **4/4** at
  `reports/local-20260819T102500Z`. Full record:
  `experiments/v0043-navigation-fast-path-v269.md`. No promotion, package,
  upload, activation, or live-state operation occurred.

### Next: CPU-safe strategy hypothesis

- The live TLE evidence remains actionable, but this navigation shortcut did
  not preserve local route outcomes. The next candidate must optimize a
  measured hot path without changing established route choices, or address a
  different repeated conversion failure; keep v0043 as baseline.

### v268 route-owner infiltrator repair — rejected — 2026-08-19

- Fresh v106 replay evidence showed an own home Conveyor removed and an enemy
  Barrier placed on the same pending output tile on the next round. v268 kept
  the existing chain owner and, only for a visible enemy Barrier on that exact
  pending tile inside the home-threat radius, destroyed it and rebuilt the
  Core-facing Conveyor in place. No dynamic task, Store signal, generic
  pursuit, hijack, purchase, or offensive selector changed.
- Focused coverage was **31/31**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions. The configured 15-map screen was command-clean at **10-5**,
  collecting **85,400 vs 60,420 Ti** (`reports/local-20260819T100316Z`).
- The independent rotated screen reversed to **4-11**, collecting **53,320 vs
  73,590 Ti**, also command-clean with zero TLE/suspicious rows
  (`reports/local-20260819T100509Z`). Reject v268: the first-screen edge is
  not repeatable. Temporary code/tests were removed and exact v0043 parity is
  zero lines at `reports/iter-v268-route-owner/rollback-source.diff`;
  rollback focused was **26/26**, compileall passed, and rollback smoke was
  **4/4** at `reports/local-20260819T100805Z`. Full record:
  `experiments/v0043-route-owner-infiltrator-repair-v268.md`. No promotion,
  package, upload, activation, or live-state operation occurred.

### Next: fresh infiltration audit

- Preserve the remove-then-replace event as evidence, but do not tune the
  rejected route-owner radius/facing. The next candidate must be a different
  bounded infiltration or anti-infiltration mechanism, protect first delivery,
  and pass an independent screen before any longer gate or promotion.

### v267 causal home-route infiltrator blocker — rejected — 2026-08-19

- Fresh v106 replays repeatedly showed an own home Conveyor removed and an
  enemy Barrier placed on the same tile the next round. v267 isolated that
  event: the nearest dynamic Builder could destroy only a visible enemy Barrier
  blocking the output of a visible home Conveyor, then rebuild the route. No
  generic enemy-Builder chase, ordinary Barrier response, hijack, or purchase
  policy changed.
- Focused coverage was **29/29**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions. The initial 15-map screen was command/delivery/reliability-clean
  at **7-8**, **76,570 vs 75,570 Ti**; five candidate causal blocker sequences
  were observed (`reports/local-20260819T094922Z` and
  `reports/iter-v267-infiltration-blocker/blocker-audit.txt`).
- The independent rotation reversed to **6-9**, collected **48,070 vs 68,740
  Ti**, and added one candidate no-delivery row; zero TLE/suspicious rows
  (`reports/local-20260819T095225Z`). Reject v267 without a longer gate.
  Temporary code/tests were removed and exact v0043 source parity is zero
  lines at `reports/iter-v267-infiltration-blocker/rollback-source.diff`;
  rollback focused was **26/26**, compileall passed, and rollback smoke **4/4**.
  Full record: `experiments/v0043-causal-infiltrator-blocker-v267.md`. No
  promotion, package, upload, activation, or live-state operation occurred.

### v266 post-delivery Launcher courier — rejected — 2026-08-19

- Top-team replay correlation motivated a bounded second-attacker courier:
  after three completed routes, confirmed enemy Core, and one forward Sentinel,
  it could build at most three dynamically reserved Launchers and throw only
  itself to a passable tile with strict Core-distance progress. Opening
  economy, primary pressure, routes, and infiltration policy were unchanged.
- Focused coverage was **31/31**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained only the inherited 15 obsolete imports plus two
  navigation assertions. The exact-v0043 15-map screen was command-clean with
  zero TLE/suspicious rows, but lost **7-8** and collected **55,290 vs 67,200
  Ti**; only four candidate Launchers were built. Raw report:
  `reports/local-20260819T093411Z`.
- Reject v266 without a longer gate. Temporary Launcher code/tests were removed
  and rollback focused was **26/26** with compileall pass; confirm exact v0043
  parity before the next hypothesis. Full record:
  `experiments/v0043-post-delivery-launcher-courier-v266.md`. No promotion,
  package, upload, activation, or live-state operation occurred.

### v265 secondary logistics landmark — rejected — 2026-08-19

- Fresh attributable v106 losses showed fixed attackers reaching the opposing
  half with Harvesters but no confirmed Core or forward Sentinel. v265 let only
  the designated secondary attacker follow the output tile of a visible enemy
  Conveyor as a navigation landmark; the primary lane, economy, Sentinel
  gates, and all infiltration behavior were unchanged.
- Focused coverage was **30/30**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete-module imports and two navigation
  assertions. The configured 15-map screen was command-clean at **8-7** but
  collected **69,730 vs 79,350 Ti** and had one candidate no-delivery row
  (`reports/local-20260819T091027Z`).
- The independent rotated screen reversed to **7-8**, collected **63,840 vs
  60,190 Ti**, and was delivery/reliability-clean
  (`reports/local-20260819T091300Z`). Across both screens the candidate was
  **15-15** and collected **133,570 vs 139,540 Ti**; no repeatable improvement
  justified a repair or longer gate.
- Reject v265 and restore exact v0043. Rollback focused was **26/26**,
  compileall passed, static retained the same inherited failures, and rollback
  smoke was **4/4** at `reports/local-20260819T091605Z`. Source parity is zero
  at `reports/iter-v265-secondary-landmark/rollback-source.diff`; the complete
  record is `experiments/v0043-secondary-logistics-landmark-v265.md`. No
  package, upload, activation, promotion, or live-state operation occurred.

### v264 visible-route viability guard — rejected — 2026-08-19

- The v263 Valkyrie replay showed the first two Harvesters committed to a
  fully visible disconnected frontier. v264 added a conservative opening BFS:
  reject and expire only a source whose visible component cannot reach a Core
  facing tile; unseen terrain remained permissive. Mature routes, the chain
  FSM, ranking, roles, combat, and infiltration were unchanged.
- Focused coverage was **31/31**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete imports and two
  navigation assertions. The initial exact-v0043 15-map screen was clean but
  **6-9**, **85,110 vs 82,620 Ti**, **118 vs 133 Harvesters**, all deliveries,
  and zero TLE/suspicious rows (`reports/local-20260819T084526Z`).
- An independent 15-map rotation was also process-clean and all-delivery, but
  only **7-8**, **66,600 vs 70,900 Ti**, and **119 vs 117 Harvesters**
  (`reports/local-20260819T084820Z`). The collection edge did not repeat and
  there was no win-rate edge, so reject without repair or long gate.
- The temporary guard/tests were removed and exact v0043 parity is recorded at
  `reports/iter-v264-visible-route-viability/rollback-source.diff` (empty).
  Rollback focused was **26/26**, compileall passed, static retained the same
  inherited failures, and rollback smoke was **4/4** at
  `reports/local-20260819T085326Z`. No promotion or platform operation.
  Full record: `experiments/v0043-visible-route-viability-v264.md`.

### v263 bounded dynamic economy rotation — rejected — 2026-08-19

- Fresh v106 Coreflood/Torsko losses showed dynamic Builders leaving the
  economy after three to five routes while the Harvester curve stalled at
  four to six. v263 added one bounded per-Builder SCOUT/CHAIN rotation after a
  stale `TASK_ADVANCE`, gated below six completed routes and after all higher-
  priority response/raid work. Fixed attackers and the route FSM were left
  unchanged; this was not an infiltration change.
- Focused coverage was **30/30**, candidate compileall passed, smoke was
  **4/4**, and `make static` retained only the inherited 15 obsolete imports
  and two navigation assertions. The exact-v0043 15-map screen was clean at
  the process level but lost **4-11**, collected **53,550 vs 73,790 Ti**, placed
  **91 vs 147 Harvesters**, and delivered **14/15 vs 15/15**. There were zero
  TLE/suspicious rows; max p99/peak were **1,440/4,963 us**. Report:
  `reports/local-20260819T083440Z`; replay diagnostics:
  `reports/iter-v263-bounded-economy-rotation/replay-analysis.json`.
- Reject without repair or long gate. The pulse did not restore conversion and
  introduced a Valkyrie no-delivery row. Temporary source/tests were removed;
  recursive v0043 parity is exact at
  `reports/iter-v263-bounded-economy-rotation/rollback-source.diff` (empty).
  Rollback focused was **26/26**, compileall passed, and rollback smoke was
  **4/4** at `reports/local-20260819T083806Z`. No package, upload, activation,
  promotion, or live-state operation occurred. Full record:
  `experiments/v0043-bounded-economy-rotation-v263.md`.

### v262 visit-aware nearby frontier discovery — rejected after one repair — 2026-08-19

- v262 replaced only the SCOUT no-ore pseudo-random stride with visit-aware
  nearby frontier ordering. Focused coverage was **29/29**, compileall passed,
  smoke **4/4**, and static retained the inherited 15 obsolete imports plus
  two navigation assertions. The initial exact-v0043 15-map screen regressed
  to **3-12**, **44,400 vs 82,070 Ti**, despite zero TLE/suspicious rows;
  Glacierkeep and Archipelago showed **2 vs 11** and **6 vs 12** Harvesters
  (`reports/local-20260819T080653Z`).
- One replay-confirmed repair rotated equal visit/geometric shells per Builder.
  It reached **8-7**, **86,990 vs 98,820 Ti**, all deliveries, and zero
  TLE/suspicious rows (`reports/local-20260819T081242Z`), but the independent
  all-15-map rotation fell to **4-11**, **48,270 vs 77,650 Ti**
  (`reports/local-20260819T081508Z`). No repeatable edge existed.
- Reject v262 and restore exact immutable v0043. Rollback focused was **26/26**,
  compileall passed, smoke **4/4** (`reports/local-20260819T081813Z`), and
  `reports/iter-v262-frontier-discovery/rollback-source.diff` is empty. No
  long gate, package, upload, activation, promotion, or live-state operation.
  Full record: `experiments/v0043-frontier-discovery-v262.md`.

### v261 economy-gated home-Gunner cap — rejected — 2026-08-19

- Fresh v260/live replay evidence showed our side sometimes spending four home
  Gunners with four Harvesters while the opponent reached 19 Harvesters. v261
  kept the two-Gunner floor and real-siege response, but delayed the five-
  Gunner ordinary-contact cap until five completed routes; routes, roles,
  offense, and Store behavior were unchanged.
- Focused coverage was **29/29**, compileall passed, smoke **4/4**, and static
  retained the inherited 15 obsolete-module imports plus two navigation
  assertions. The exact-v0043 15-map screen was command-clean at **6-9**, with
  **69,440 vs 81,410 Ti**, zero TLE/suspicious rows, and no controlled cap or
  siege event (`reports/local-20260819T075756Z`).
- Reject v261 without a repair or long gate: the lower turret spend supplied no
  repeatable win/collection edge. Temporary source/tests were removed;
  recursive v0043 parity is exact at
  `reports/iter-v261-gunner-cap/rollback-source.diff`. Rollback focused was
  **26/26**, compileall passed, smoke **4/4** at
  `reports/local-20260819T080048Z`. No release, package, upload, activation,
  promotion, or live transition. Full record:
  `experiments/v0043-economy-gated-gunner-cap-v261.md`.

### v259 event-gated chain detour — rejected after one repair — 2026-08-19

- Fresh v106 Big O losses showed route conversion failures alongside enemy
  Barrier incursions. v259 let an active chain take one danger-safe cardinal
  detour only after direct navigation failed at a visible blocker, preserving
  the existing chain FSM; it did not target infiltrators or change economy,
  roles, or purchases.
- Initial focused coverage was **29/29**, compileall passed, smoke **4/4**, and
  static retained the inherited failures. The exact-v0043 15-map screen was
  **7-8**, all deliveries, **64,130 vs 63,950 Ti**, zero TLE/suspicious rows,
  max p99/peak **1,292/4,974 us** (`reports/local-20260819T072434Z`). Replay
  inspection found real Barrier/conveyor frontier interactions, so one repair
  was allowed.
- The repair narrowed the trigger to enemy Barrier or wall only. Focused
  coverage was **30/30**, compileall passed, and smoke **4/4**, but the screen
  fell to **4-11**, with delivery **14/15 vs 15/15**, collection
  **65,480 vs 93,640 Ti**, zero TLE/suspicious rows, and max p99/peak
  **1,438/2,636 us** (`reports/local-20260819T072856Z`). Reject v259; the
  repair introduced a no-delivery row and no win-rate/collection edge.
- Temporary source/tests were removed and candidate parity with immutable v0043
  is exact (`reports/iter-v259-chain-detour/rollback-source.diff`). Rollback
  focused was **26/26**, compileall passed, and rollback smoke **4/4** at
  `reports/local-20260819T073136Z`. No release gate, promotion, package,
  upload, activation, or live transition occurred. Full record:
  `experiments/v0043-chain-detour-v259.md`.

### v258 pre-route home infiltrator interception — rejected — 2026-08-19

- Fresh live Glacierkeep evidence showed an opponent Builder destroying our
  early home conveyors and replacing the vacated tiles with Barriers at
  `(13,3)`, `(15,4)`, `(16,3)`, and `(14,4)`. v258 gave the permanent
  Defender a SCOUT-only intercept against a visible enemy Builder inside the
  home radius, but only before three completed routes and while a friendly
  home logistics building remained. Active chains and all offense/hijack
  behavior were unchanged.
- Focused coverage was **30/30**, compileall passed, `make smoke` was **4/4**,
  and `make static` retained the inherited failures. The exact-v0043 rotated
  15-map screen was **7-8**, all 15 sides delivered, **62,270 vs 68,370 Ti**,
  zero TLE/suspicious rows, and max p99/peak **1,508/3,059 us**. Raw report:
  `reports/local-20260819T070825Z`; parsed diagnostics:
  `reports/iter-v258-home-infiltrator/screen15-analysis.json`.
- No controlled screen pairing showed an actual infiltrator event, so no
  repair or longer gate was justified. Reject v258; temporary source/tests
  were removed and candidate parity with immutable v0043 is exact. Rollback
  focused was **26/26**, compileall passed, and rollback smoke was **4/4** at
  `reports/local-20260819T071408Z`; parity evidence is
  `reports/iter-v258-home-infiltrator/rollback-source.diff`. No release,
  package, upload, activation, promotion, or live transition. Full record:
  `experiments/v0043-home-infiltrator-intercept-v258.md`.

### v257 bounded dynamic task rechecks — rejected after one repair — 2026-08-19

- Fresh v106 replay refresh found live reliability failures: 63 TLEs on Midgard
  and 1,082 on Nordkap in the newest 2-3 TRRR series. v257 throttled dynamic
  detector scans to a two-round cadence after commitment and stopped
  targetless `TASK_HARVEST` from resetting its task clock; priorities, routes,
  infiltration, and combat policy were unchanged.
- Initial focused coverage was **28/28**, compileall passed, smoke **4/4**, and
  static retained the inherited failures. The exact-v0043 15-map screen was
  **8-7**, all deliveries, **82,510 vs 72,920 Ti**, zero TLE/suspicious rows
  (`reports/local-20260819T064302Z`). The independent 30-game screen was
  **17-13**, all deliveries, **126,510 vs 117,880 Ti**, zero TLE/suspicious
  rows, but Glacierkeep, Archipelago, and Nordkap fell to **0-2**.
- The one bounded repair kept targetless harvest valid through the generic
  timeout. Focused coverage was **29/29**, compileall/static/smoke stayed at
  the same profile, and the screen improved to **18-12**, **135,000 vs
  114,300 Ti**, with 29/30 deliveries and zero TLE/suspicious rows; Archipelago
  and Nordkap recovered, but Glacierkeep remained **0-2**.
- Reject v257 because the protected Glacierkeep collapse blocks promotion.
  Temporary source/tests are being removed; v0043 remains the baseline. No
  long gate, package, upload, activation, promotion, or live transition.
  Full record: `experiments/v0043-task-recheck-v257.md`.

### v256 first-route Gunner-ray shield — rejected after one repair — 2026-08-19

- Fresh v106 SmartFridge replay evidence showed a no-delivery loss with our
  first route ending at `(6,1)` behind an opponent Gunner corridor; no enemy
  Conveyor reached one of our Harvesters. v256 therefore tested one
  reserve-funded Barrier shield only during the ordinary first Harvester
  chain, requiring the immediate next route tile to be in a visible Gunner
  ray. Sentinel danger, seeded routes, hijack selection, and fixed offense
  were unchanged.
- Initial focused coverage was **30/30**, compileall passed, smoke **4/4**,
  and static retained the inherited failures. The seed-172 15-map screen was
  **9-6**, all deliveries, **96,940 vs 82,650 Ti**, zero TLE/suspicious rows
  (`reports/local-20260819T062009Z`). The independent side-swapped 30-game
  screen reversed to **12-18**, with one candidate no-delivery row and
  **89,420 vs 93,580 Ti** (`reports/local-20260819T062305Z`).
- The one permitted repair retained focused **30/30**, compileall/static,
  and smoke **4/4**; its screen was **17-13**, all deliveries,
  **120,840 vs 109,970 Ti**, zero TLE/suspicious rows, but Archipelago,
  Auroraveil, Drakkarfjord, and Yulerune all collapsed to **0-2**
  (`reports/local-20260819T062730Z`). Reject v256; protected-map regression
  blocks promotion despite the aggregate edge.
- Temporary source/tests were removed; rollback focused was **26/26**,
  compileall passed, rollback smoke **4/4**, and recursive source parity with
  immutable v0043 is zero at
  `reports/iter-v256-gunner-ray-shield/rollback-source.diff`. No release
  gate, package, remote test, upload, activation, promotion, or live-state
  transition. Full record:
  `experiments/v0043-gunner-ray-shield-v256.md`.

### v255 ultra-cramped continuous pressure — rejected after one repair — 2026-08-19

- Fresh v106 replay evidence from higher-rated `arsonist duck` showed one
  10x10 loss where our first delivery was round 62 with zero Sentinels while
  the opponent placed four. v255 allowed only the primary fixed attacker to
  buy one pre-route Sentinel on ultra-cramped geometry, with a visible
  Harvester and dynamic-price reserve; all normal route, facing, legality,
  and later-pool gates stayed unchanged.
- Focused coverage was **30/30**, compileall passed, smoke **4/4**, and static
  retained only the inherited 15 obsolete imports plus two navigation
  assertions. The 15-map screen was **8-7**, all deliveries, **63,720 vs
  48,080 Ti**, zero TLE/suspicious rows. A side-swapped 30-game screen was
  **16-14**, **126,750 vs 113,370 Ti**, with one candidate no-delivery row and
  candidate **0-2** floors on Antler, Icefloe, and Valkyrie.
- One bounded repair doubled the cramped reserve. It retained focused **30/30**,
  compileall, static, and smoke **4/4**, but the side-swapped screen fell to
  **14-16** and **124,720 vs 137,430 Ti**; no release gate was justified.
- Reject v255. Temporary source/tests were removed; rollback focused was
  **26/26**, compileall passed, rollback smoke **4/4**, and recursive source
  parity with immutable v0043 was zero (`reports/iter-v255-live-replay-audit/`
  and `reports/local-20260819T060314Z`). No package, upload, activation,
  promotion, or live-state transition. Full record:
  `experiments/v0043-ultra-cramped-pressure-v255.md`.

### v253 established-source Harvester hijack — rejected — 2026-08-19

- Fresh live evidence showed v106 winning **5-0** over version 12 in match
  `e3fc8421-f1de-4543-b529-1248a6c52030`; our Conveyor reached an enemy
  Harvester in all five games, while no opponent Conveyor reached ours. v253
  therefore changed only dynamic Harvester ranking: prefer a visible enemy
  Conveyor/Splitter-connected source, while preserving route, economy, fixed
  attacker, and defense behavior.
- The initial selector passed focused **28/28**, compileall, smoke **4/4**, and
  static retained the inherited 15 obsolete-module imports plus two navigation
  assertions, but screened **3-12** candidate-A and **7-8** in the reverse
  order. Replay analyses and reports are under
  `reports/iter-v253-established-source-hijack/`.
- One bounded repair made nearest travel primary and outlet count an
  equal-distance tie-breaker. It passed focused **29/29**, compileall, smoke
  **4/4**, and the same static profile; screens were **8-7** and **9-6** for
  **17-13** aggregate over 30 games, all deliveries, zero TLE/suspicious rows.
- The 60-game endpoint/side-swap release gate tied **30-30**, all deliveries,
  zero TLE/suspicious rows, max p99/peak **1,548/4,579 us**. Reject v253;
  source/tests were removed and recursive candidate parity with immutable v0043
  is zero. Rollback focused **26/26**, compileall passed, rollback smoke
  **4/4** at `reports/local-20260819T053521Z`. No package, remote gate,
  upload, activation, or promotion. Full record:
  `experiments/v0043-established-source-hijack-v253.md`.

### v252 guarded mirrored-Core first Sentinel — rejected after one repair — 2026-08-19

- To address the direct v106 long-map loss shape, v252 allowed one first
  Sentinel at the rotationally mirrored enemy-Core estimate before direct
  intel, but only in range with a visible friendly Harvester and dynamic
  reserve for a Harvester plus two Conveyors. Later pool, route, raid, hijack,
  and defense behavior stayed unchanged.
- Focused coverage was **30/30**, compileall passed, static retained the
  inherited 15 obsolete-import errors plus two navigation assertions, and
  smoke was **4/4** (`reports/local-20260819T045933Z`). Seed-172 screen:
  **10-5**, **65,380 vs 56,410 Ti**, all deliveries; independent seed-173:
  **4-11**, **53,900 vs 66,980 Ti**, all deliveries. Reports:
  `reports/iter-v252-mirrored-sentinel-*` and raw runs
  `reports/local-20260819T045955Z`, `reports/local-20260819T050143Z`.
- The one bounded repair required two visible Harvesters. Focused **30/30**,
  compileall, static, and smoke **4/4** remained clean, but seed-172 fell to
  **6-9**, **62,300 vs 72,990 Ti**, with one no-delivery row
  (`reports/local-20260819T050439Z`). Reject v252; rollback focused was
  **26/26**, compileall passed, rollback smoke **4/4** at
  `reports/local-20260819T050708Z`, and candidate parity with v0043 is zero.
  No release, package, upload, activation, or promotion. Full record:
  `experiments/v0043-guarded-mirrored-core-sentinel-v252.md`.

### v251 visible-Harvester proof for first Sentinel — rejected — 2026-08-19

- Direct v106 losses reached the opposing half with two-to-four Harvesters but
  no Sentinels on four long maps. v251 allowed the first fixed-attacker
  Sentinel when the Store completion marker was zero only if a visible friendly
  Harvester, directly confirmed enemy Core, and a Harvester-plus-two-Conveyor
  reserve were all present.
- Focused coverage was **29/29**, compileall passed, static retained only the
  inherited 15 obsolete-import errors and two navigation assertions, and smoke
  was **4/4** (`reports/local-20260819T044906Z`). Seed-172 screen: **8-7**,
  **58,520 vs 55,330 Ti**, all deliveries; independent seed-173: **7-8**,
  **66,630 vs 81,120 Ti**, one comparator no-delivery row. Reports:
  `reports/iter-v251-visible-harvester-sentinel/` and raw runs
  `reports/local-20260819T044934Z`, `reports/local-20260819T045143Z`.
- Reject v251 because the small first-screen edge reversed and collection
  regressed. Temporary source/tests were removed; rollback focused was
  **26/26**, compileall passed, rollback smoke **4/4** at
  `reports/local-20260819T045508Z`, and recursive candidate parity with v0043
  is zero. No release, package, upload, activation, or promotion. Full record:
  `experiments/v0043-visible-harvester-sentinel-proof-v251.md`.

### v250 siege-triggered early home Gunner — rejected — 2026-08-19

- A narrow response to the pre-v106 rush sample allowed the designated home
  Defender to build one route-free Gunner only for a visible enemy offensive
  turret near the Core or an active siege beacon. Harvester, two-Conveyor, and
  idle-attacker reserves remained hard gates; no infiltration or offense lane
  changed.
- Focused coverage was **29/29**, compileall passed, smoke was **4/4**, and
  static retained the inherited 15 obsolete-import errors plus two navigation
  assertions. Seed-172 screen: **10-5**; independent seed-173 screen:
  **5-10**. Reports: `reports/iter-v250-early-home-gunner/` and raw runs
  `reports/local-20260819T043258Z`, `reports/local-20260819T043443Z`.
- Temporary source/tests were removed; rollback focused was **26/26**,
  compileall passed, smoke was **4/4**, and candidate parity with the v0043
  snapshot was zero. No release, package, upload, activation, or promotion.
  Full record: `experiments/v0043-siege-triggered-home-gunner-v250.md`.

### v106 live replay refresh — direct loss evidence — 2026-08-19

- The first attributable v106 ladder series completed as Team B **1-4** versus
  Banminary v83, match `9c66c9bc-a75c-46ad-9733-a1b03c007ac5` (rating delta
  **-11.32**). Replay info, five `.replay26` files, and parsed diagnostics are
  under `reports/iter-v251-live-check/9c66c9bc/`.
- v106 losses on Icefloe, Midgard, Glacierkeep, and Drakkarfjord reached the
  opposing half with two-to-four Harvesters but placed **zero Sentinels**;
  Drakkarfjord also had no delivery. The cramped Fjordgate win placed three
  Sentinels early. This is direct evidence for a stale/over-strict offense
  transition, not a broad infiltrator frequency signal.

### v249 liquidity-backed dynamic economy floor — promoted locally — 2026-08-19

- Fresh live loss replays pointed to route attrition and low resource
  conversion, not frequent enemy-Builder infiltration. v249 kept fixed
  attackers on their continuous Core/sabotage lane and reserved one nearby
  dynamic Builder for harvest/exploration through five completed routes only
  while the bank could not fund a replacement Harvester, two short Conveyor
  links, and the fixed offense reserve. A rich bank released normal raids.
- The initial floor passed **25/25** focused tests, compileall, and smoke
  **4/4**; static retained the inherited 15 deleted-module import errors and
  two navigation fast-path assertions. Two all-map screens were **10-5** and
  **7-8**, with combined collection **191,110 vs 133,540 Ti** and no command,
  delivery, TLE, or suspicious-output failures. Reports:
  `reports/local-20260819T035235Z`, `reports/local-20260819T035441Z`, and
  `reports/iter-v249-liquidity-floor/replay-analysis.json`.
- The initial 60-game gate tied **30-30** (291,610 vs 293,760 Ti), so it was
  not promoted. One bounded repair assigned the low-bank floor to exactly one
  nearest dynamic owner. Repair focused coverage was **26/26**, compileall
  passed, static retained the same inherited failures, and smoke was **4/4** at
  `reports/local-20260819T040512Z`.
- The repair screen was **7-8**, **59,780 vs 48,790 Ti**, command/delivery
  clean. The final 60-game endpoint/side-swap gate was command-clean at
  **35-25 (58.3%)**, **277,160 vs 241,120 Ti**, **7.87 vs 7.63** Harvesters
  per game, one candidate no-delivery row, zero TLE/suspicious rows, max
  p99/peak **1,545/4,433 us**, and no 0-4 map floor. Reports:
  `reports/local-20260819T040658Z` and
  `reports/iter-v249-liquidity-floor/repair-release-replay-analysis.json`.
- The remote five-map gate returned match
  `3e05d451-0447-4b4c-b28a-0103a7b430de` with a successful command record at
  `reports/remote-20260819T041421Z`. The repair was archived as v0043 and
  uploaded as platform version **106** (`v0043-liquidity-backed-dynamic-floor-eeafad8f`),
  which became active at **2026-08-19T04:16:32Z**. The local live state is
  `active_observing`; platform 101 remains the rollback target and the
  observation snapshot is `reports/live-observe-20260819T041709Z`. The
  guarded explicit activation confirmation returned `already_active: true` at
  `reports/activation-20260819T041911Z`. Full record:
  `experiments/v0042-liquidity-backed-dynamic-floor-v249.md`.

### v248 attacker objective progress watchdog — rejected — 2026-08-19

- To test continuous offence without touching economy or infiltration policy,
  v248 added a bounded watchdog for an explicit remembered enemy logistics
  target: if distance and visible target HP did not improve, the attacker
  cleared the target and replanned through the existing pressure ladder.
- The initial version incorrectly armed from the guessed Core lane. Focused
  tests were **26/26**, compileall passed, smoke **4/4**, and static retained
  the inherited 15 obsolete-module import errors plus two navigation fast-path
  assertions. The rotated screen was **4-11**, collection **45,350 vs 85,840
  Ti**. Raw report: `reports/local-20260819T031952Z`; analysis:
  `reports/iter-v248-offense-watchdog/screen-replay-analysis.json`.
- Repair 1 restricted the watchdog to explicit logistics targets. It passed
  **26/26**, compileall, and smoke **4/4**, but screened **6-9** with
  **73,700 vs 81,180 Ti**. Raw report: `reports/local-20260819T032259Z`;
  analysis: `reports/iter-v248-offense-watchdog/repair-replay-analysis.json`.
- Repair 2 cleared a stalled target and let the existing priority ladder choose
  the next action. It passed **26/26**, compileall, and smoke **4/4**; the
  screen was **12-3**, **88,900 vs 54,970 Ti**, with zero TLE/suspicious rows.
  Raw report: `reports/local-20260819T032555Z`; analysis:
  `reports/iter-v248-offense-watchdog/repair2-replay-analysis.json`.
- The 60-game release gate was command-clean but failed promotion: candidate
  **24-36 (40%)**, **246,020 vs 273,550 Ti**, zero TLE/suspicious rows, max
  p99/peak **1,526/4,618 us**. Raw report:
  `reports/local-20260819T032755Z`; analysis:
  `reports/iter-v248-offense-watchdog/release-replay-analysis.json`.
- Reject v248 after the two bounded repairs. Temporary source/test hunks were
  removed; candidate attacker source is byte-identical to immutable v0042
  (`reports/iter-v248-offense-watchdog/rollback-source.diff`). Rollback
  focused coverage was **23/23**, compileall passed, rollback smoke **4/4** at
  `reports/local-20260819T033635Z`, and no promotion/package/upload/
  activation/live transition occurred. Full record:
  `experiments/v0042-offense-progress-watchdog-v248.md`.

### v247 low-liquidity recovery — rejected — 2026-08-19

- Live v105 Drakkarfjord evidence showed the candidate ending with three
  Harvesters, no forward Sentinel, and 10 Ti after its route was disrupted.
  v247 tested a guarded return to the existing SCOUT/CHAIN economy loop after
  the historical three-route milestone when the bank could not afford one
  Harvester and no forward Sentinel had been observed. Opening, route,
  fixed-role, and infiltration selectors were unchanged.
- Initial focused coverage was **29/29**, compileall passed, smoke was **4/4**,
  and `make static` retained the inherited 15 obsolete-import errors plus two
  navigation fast-path assertions. The rotated 15-map screen was
  command-clean with zero TLE/suspicious rows but finished **6-9**, collection
  **76,540 vs 84,860 Ti**. Raw report:
  `reports/local-20260819T025422Z`; replay analysis:
  `reports/iter-v247-low-liquidity-recovery/initial-replay-analysis.json`.
- The single-owner repair passed **31/31**, compileall, and smoke **4/4** but
  fell to **5-10**, collection **48,040 vs 60,730 Ti**, and added a candidate
  no-delivery Royale row. Raw report:
  `reports/local-20260819T025805Z`; replay analysis:
  `reports/iter-v247-low-liquidity-recovery/repair-replay-analysis.json`.
- Reject v247 after the two bounded attempts. Temporary edits were removed;
  recursive candidate parity with immutable v0042 is zero-line at
  `reports/iter-v247-low-liquidity-recovery/rollback-source.diff`. Rollback
  focused coverage was **27/27**, compileall passed, rollback smoke was **4/4**
  at `reports/local-20260819T030033Z`, and no release/package/upload/
  activation/live transition occurred. The v224–v242 infiltration family
  remains closed pending new replay causality. Full record:
  `experiments/v0042-low-liquidity-recovery-v247.md`.

### v246 topology-aware home Barrier response — rejected — 2026-08-19

- The live v105 Drakkarfjord loss showed enemy Barriers occupying the Core
  ring and blocking friendly Conveyor outputs. v246 tested a narrow structural
  defense: a dynamic Builder could select only a visible enemy Barrier on the
  Core ring or directly in a friendly Conveyor's output, then reuse the legal
  existing strike/movement path. Ordinary Barriers, active chains, and all
  economy/offense policy were unchanged.
- Focused coverage passed **30/30** before rollback (26 nearest-defense tests
  plus seeded-route coverage), compileall passed, smoke was **4/4**, and static
  retained the inherited failures (15 obsolete deleted-module imports plus two
  navigation fast-path assertions). The rotated 15-map screen was
  command/delivery-clean with zero TLE/suspicious rows, but candidate-A lost
  **6-9**, collected **73,120 vs 73,780 Ti**, and delivered on all 15 maps;
  max p99/peak callback time was **1,467/4,917 us**. Raw report:
  `reports/local-20260819T023956Z`; parsed diagnostics:
  `reports/iter-v246-home-barrier/replay-analysis.json`.
- Reject v246 without a repair or long gate. Temporary source/test edits were
  removed; recursive candidate parity with immutable v0042 is zero-line at
  `reports/iter-v246-home-barrier/rollback-source.diff`. Rollback focused
  coverage was **27/27**, rollback compileall passed, and post-rollback smoke
  was **4/4** at `reports/local-20260819T024516Z`. No promotion, package,
  upload, activation, or live-state transition occurred. The replay
  blocker is real, but this response did not create a repeatable win-rate or
  collection edge; choose a different mature-workforce/pressure-conversion
  hypothesis next. Full record:
  `experiments/v0042-topology-aware-home-barrier-v246.md`.

### v245 first-Harvester opening handoff — rejected — 2026-08-19

- Fresh replay timing showed current v0042 placing its first Core-ring
  Conveyor around round 3 and first Harvester around round 10.4, while the
  top-team sample placed first Harvesters around round 4.7 and first
  Conveyors around round 6.5. v245 tested a conditional phase handoff: with
  zero completed routes, an adjacent eligible Harvester could preempt the
  opportunistic ring build; with no adjacent ore, or after route 1, behavior
  stayed unchanged.
- Focused coverage passed **31/31**, compileall passed, smoke was **4/4**, and
  static retained the inherited exit 2 (15 obsolete deleted-module imports
  plus two navigation fast-path assertions). The first all-map screen was
  command-clean with zero TLE/suspicious rows and 15/15 deliveries, but
  candidate-A lost **4-11**, collected **74,020 vs 96,440 Ti**, averaged
  **8.0 vs 9.0 Harvesters** and **2.27 vs 3.8 Sentinels**, and first delivery
  was **24.3 vs 21.4**. Raw report:
  `reports/local-20260819T022437Z`; replay analysis:
  `reports/iter-v245-opening-harvester/replay-analysis.json`.
- Reject v245 without a repair or longer gate. Temporary source/test edits
  were removed; recursive candidate parity with immutable v0042 is zero-line
  at `reports/iter-v245-opening-harvester/rollback-source.diff`. Rollback
  focused coverage was **27/27**, compileall passed, static retained the
  inherited failures, and rollback smoke was **4/4** at
  `reports/local-20260819T022722Z`. No promotion, package, upload, activation,
  or live-state transition occurred. Full record:
  `experiments/v0042-first-harvester-opening-handoff-v245.md`.

### v244 large-board economy floor — rejected — 2026-08-19

- Live v105 was rolled back to v101 after 55 rated series at 51.64% versus
  the known-good 70%; selected Drakkarfjord losses showed the candidate with
  only 3 Harvesters and 36 live Conveyors versus 12 and 153 for its opponent.
  v244 therefore tested a map-adaptive economy floor: four completed routes
  before scalable offense on boards with width-plus-height at least 48, while
  compact maps retained the three-route floor and the first fixed attacker
  kept its early pressure lane.
- Focused coverage passed **28/28**, compileall passed, smoke was **4/4**, and
  static retained the inherited exit 2 (15 obsolete deleted-module imports
  plus two navigation fast-path assertions). The rotated 15-map screen was
  command-clean with zero TLE/suspicious rows, but candidate-A lost **7-8**,
  collected **72,010 vs 74,240 Ti**, and had one no-delivery row while the
  baseline delivered on all 15. Raw report:
  `reports/local-20260819T021241Z`; replay analysis:
  `reports/iter-v244-large-board-economy/replay-analysis.json`.
- Reject v244 without a repair or long gate. The extra floor delayed economy
  conversion rather than protecting it: Glacierkeep was **210 vs 1,120 Ti**
  with first delivery **226 vs 70**, and Archipelago was **7,880 vs 18,800 Ti**.
  Temporary edits were removed; recursive candidate parity with immutable v0042
  is zero-line at `reports/iter-v244-large-board-economy/rollback-source.diff`.
  Rollback focused coverage was **27/27**, compileall passed, static retained
  the inherited failures, and rollback smoke was **4/4** at
  `reports/local-20260819T021545Z`. No promotion, package, upload, activation,
  or live-state transition occurred. Full record:
  `experiments/v0042-large-board-economy-floor-v244.md`.

### v243 opening route-context ore ranking — rejected — 2026-08-19

- Glacierkeep replay evidence suggested that a nearest-builder opening ore
  could require a long wall detour. v243 therefore ranked visible ore by
  approach plus twice the Core distance only before three completed routes and
  on boards with width-plus-height at least 48; compact maps and established
  economies retained nearest-ore selection.
- Focused route-context plus nearest-defense/seeded-route coverage passed
  **31/31**, compileall passed, smoke was **4/4**, and static retained the
  inherited exit 2 (15 obsolete deleted-module imports plus two navigation
  assertions). The rotated 15-map screen was command-clean with zero
  TLE/suspicious rows but candidate-A lost **4-11**, collected **62,240 vs
  73,780 Ti**, placed **99 vs 134 Harvesters**, and first-delivery mean was
  **28.2 vs 22.4**. Raw report: `reports/local-20260819T015537Z`; replay
  analysis: `reports/iter-v243-opening-route-context/replay-analysis.json`.
- Reject v243 without a repair or long gate. The temporary source/test edits
  were removed; recursive parity with immutable v0042 is zero-line. Rollback
  coverage was **27/27**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T015759Z`, and no promotion/package/upload/
  activation/live transition occurred. Full record:
  `experiments/v0042-opening-route-context-v243.md`.

### v242 immediate connected-source hijack — rejected — 2026-08-19

- The own-infiltration hypothesis was narrowed to a dynamic Builder that was
  already adjacent to a visible enemy Harvester with a hostile Conveyor or
  Splitter outlet. It could seed one accepting Conveyor only when it was the
  nearest non-fixed Builder and dynamic prices left a Harvester-plus-two-
  Conveyor reserve; it never walked off-route and did not alter the fixed
  attacker's lane.
- New legality/ownership checks plus nearest-defense/seeded-route coverage
  passed **30/30**, compileall passed, smoke was **4/4**, and static retained
  the inherited exit 2 (15 obsolete-module imports plus two navigation
  assertions). The rotated 15-map screen was command/delivery-clean with zero
  TLE/suspicious rows, but candidate-A lost **5-10**, collected **85,780 vs
  88,400 Ti**, and placed fewer Harvesters (**116 vs 123**), Conveyors
  (**1,510 vs 1,855**), Sentinels (**55 vs 68**), and Barriers (**60 vs 91**).
  Both sides delivered on all 15 rows. Raw report:
  `reports/local-20260819T013838Z`; replay analysis:
  `reports/iter-v242-immediate-hijack/replay-analysis.json`.
- Reject v242 without a repair or long gate. The temporary source/test edits
  were removed and recursive source parity with immutable v0042 is zero-line.
  Rollback coverage was **27/27**, compileall passed, rollback smoke was
  **4/4** (`reports/local-20260819T014208Z`), and rollback static retained
  the inherited failures. No promotion, package, upload, activation, or live
  transition occurred. Full record:
  `experiments/v0042-immediate-connected-hijack-v242.md`.

### v241 reactive inward infiltrator Barrier — rejected — 2026-08-19

- The replay audit showed route-radius enemy Builders were uncommon, so this
  was a deliberately narrow defense experiment rather than another broad
  infiltrator lease. A selected home-threat responder could place one Barrier
  on the enemy Builder's cardinal inward tile only after one completed route,
  with a Harvester-plus-two-Conveyors reserve; Core-ring and live-belt safety
  checks remained mandatory. No opening, Store, route, workforce, turret,
  Launcher, or offensive infiltration policy changed.
- Focused coverage was **31/31**, compileall passed, smoke was **4/4**, and
  static retained the inherited 15 obsolete-module imports plus two navigation
  assertions (`reports/iter-v241-infiltrator-barrier/static.log`). The rotated
  15-map screen was command/delivery-clean with zero TLE/suspicious rows, but
  candidate-A lost **7-8** and collected **67,990 vs 93,250 Ti**. Barrier
  placements averaged **4.67 vs 4.07**; there was no paired win or collection
  edge. Raw report: `reports/local-20260819T012111Z`; parsed diagnostics:
  `reports/iter-v241-infiltrator-barrier/replay-analysis.json`.
- Reject v241 without a repair or long gate. Temporary source/test edits were
  removed; candidate Python is recursively byte-identical to immutable v0042.
  Rollback focused coverage was **27/27**, compileall passed, rollback smoke
  was **4/4** (`reports/local-20260819T012415Z`), and rollback static retained
  the inherited failures. No promotion, package, upload, activation, or live
  transition occurred. Full record:
  `experiments/v0042-reactive-infiltrator-barrier-v241.md`.

### v240 map-scaled late route rescue — rejected — 2026-08-19

- The infiltration audit and v229/v233/v235/v236/v237 results did not support
  another generic infiltrator branch. v240 instead tested a map-scaled
  last-mile rescue: after a late zero-route/zero-Sentinel signal and a dynamic
  Harvester-plus-two-Conveyor reserve, only the primary attacker returned home
  and reused the existing orphan/Harvester/CHAIN FSM.
- Focused coverage was **6/6** new and **33/33** combined; compileall passed,
  smoke was **4/4**, and static retained the inherited 15 obsolete-module
  imports plus two navigation assertions. The seed-173 15-map screen was
  command-clean with zero candidate no-delivery/TLE/suspicious rows, but was
  **7-8**, collection **64,280 vs 74,780 Ti**, and first-delivery mean
  **37.67 vs 89.47** (`reports/local-20260819T010427Z`; analysis
  `reports/iter-v240-route-rescue/replay-analysis.json`). The delivery mean
  improved because the baseline had one no-delivery row, but there was no
  paired win-rate or collection edge.
- Reject v240 without a repair or long gate. Temporary source/test/screen
  config edits were removed; candidate source is recursively byte-identical
  to immutable v0042. Rollback focused coverage was **27/27**, compileall
  passed, static retained its inherited failures, and rollback smoke was
  **4/4** at `reports/local-20260819T010805Z`. No promotion, package, upload,
  activation, or live-state transition occurred. Full record:
  `experiments/v0042-map-scaled-route-rescue-v240.md`.

### v239 early primary-attacker Launcher lifecycle — rejected after one repair — 2026-08-19

- Top-team replays showed Launchers on rounds 1/3/5 in 8/15 winners, while
  v0042 never created one. v239 allowed only the primary attacker to buy one
  through round 8 with a dynamic Harvester-plus-two-Conveyors reserve; its
  lifecycle launched only friendly Builders to legal passable tiles with
  strict distance progress toward the mirrored/confirmed enemy Core.
- The initial implementation passed **31/31**, compileall, and smoke **4/4**,
  then lost the rotated 15-map screen **4-11**, collecting **24,160 vs 50,060
  Ti** and delivering at mean **41.2 vs 25.6**. It placed one Launcher on
  every candidate map (rounds 2-3), with zero command/TLE/suspicious faults
  (`reports/local-20260819T004432Z`; analysis in
  `reports/iter-v239-early-primary-launcher/replay-analysis.json`).
- The one causal repair restricted pickups to designated fixed attackers.
  Focused coverage remained **31/31**, static retained the inherited exit 2,
  and smoke was **4/4**. The same screen improved to **8-7**, collection
  **77,840 vs 64,800 Ti**, and first delivery **25.2 vs 51.1**, but the
  independent rotated screen reversed to **7-8**, collection **65,020 vs
  75,940 Ti**, with one candidate no-delivery row and delivery **99.9 vs
  21.1** (`reports/local-20260819T004914Z`; analysis
  `replay-analysis-repair-rotated.json`).
- Reject v239. The early Launcher did not produce a repeatable edge and harmed
  opening delivery; no 60-game gate, promotion, package, upload, activation,
  or live-state transition occurred. Temporary source/test/config edits were
  removed, screen seed 172 restored, and candidate Python is recursively
  byte-identical to immutable v0042. Rollback coverage was **27/27**,
  compileall passed, rollback smoke **4/4**, and static retained exit 2. Full
  record: `experiments/v0042-early-primary-launcher-v239.md`.

### v238 deterministic action tie-breakers — rejected — 2026-08-19

- The baseline self-control was 5–10 on the same 15-map schedule, so v238
  tested whether process-global Python randomness was masking real progress.
  It replaced only spawn-ring ordering, the attacker's far-exploration
  fallback, and exact-center home-Gunner facing with a local round/unit hash;
  no economy, route, combat, Store, map, or live policy changed.
- Focused coverage passed **30/30**, compileall passed, `make smoke` was
  **4/4**, and `make static` retained the inherited exit 2 (15 missing
  legacy-module imports plus two navigation fast-path assertions). The rotated
  15-map screen was command-clean but candidate-A lost **4–11**, collecting
  **41,110 vs 79,350 Ti**, with first-delivery mean **32.13 vs 28.07** and
  zero candidate TLE/suspicious rows (`reports/local-20260819T003515Z`; replay
  analysis `reports/iter-v238-deterministic-action-tiebreakers/replay-analysis.json`).
- Reject v238. Deterministic spawn ordering reproduced the earlier v193
  regression; all temporary source/test edits were removed and recursive
  source parity with immutable v0042 is zero-line. Rollback coverage was
  **27/27**, compileall passed, and no 60-game gate, promotion, package,
  upload, activation, or live-state transition occurred. Full record:
  `experiments/v0042-deterministic-action-tiebreakers-v238.md`.

### v237 Gunner infiltrator target priority — rejected after one repair — 2026-08-19

- The hypothesis used existing home Gunners as an anti-infiltrator response:
  a hostile Builder in the current firing line was preferred only when
  `can_fire` confirmed legality, with normal nearest-building targeting kept
  as fallback. No task, purchase, route, workforce, Store, map, or live policy
  changed.
- The broad implementation passed **30/30** focused tests, compileall and
  smoke **4/4**, and inherited static exit 2. Its first 15-map screen was
  **9-6**, collecting **77,910 vs 62,100 Ti**, with 15/15 first delivery on
  both sides (`reports/local-20260819T001506Z`). Seed 173 reversed to **6-9**,
  **62,730 vs 70,710 Ti**, with zero candidate TLE/suspicious rows
  (`reports/local-20260819T001736Z`).
- The one repair limited priority to the exact nearest target tile. Focused
  coverage was **31/31**, compileall/smoke **4/4**, static unchanged, and seed
  174 was **7-8**, **70,140 vs 70,830 Ti**, with one baseline no-delivery row
  and zero candidate TLE/suspicious rows (`reports/local-20260819T002020Z`).
- Reject v237. Temporary source/test edits were removed; rollback coverage was
  **27/27**, compileall passed, static retained exit 2, rollback smoke was
  **4/4** at `reports/local-20260819T002228Z`, and candidate Python is
  recursively byte-identical to immutable v0042. No 60-game gate, promotion,
  package, upload, activation, or live-state transition occurred.

### v236 Sentinel infiltrator target priority — rejected — 2026-08-19

- The defensive hypothesis reordered the existing Sentinel occupancy checks so
  an enemy Builder on a hostile Conveyor/Splitter would be fired at before the
  infrastructure underneath it. No Builder task, economy, route, weapon,
  Store, map, or live policy changed.
- Focused coverage passed **30/30**, compileall passed, smoke was **4/4**, and
  static retained the inherited exit 2 (15 obsolete-module errors plus two
  navigation fast-path assertions). The rotated 15-map screen was
  command-clean but only **6-9** for candidate-A; all 15 rows delivered and
  candidate TLE/suspicious counts were zero. Sentinel placements averaged
  **2.67** versus **3.87** for v0042, with no protected-map or
  infiltration-response edge (`reports/local-20260819T000615Z`, analysis
  `reports/iter-v236-sentinel-infiltrator-target-priority/replay-analysis.json`).
- The no-detour edit was removed without a repair. Rollback coverage was
  **27/27**, compileall passed, rollback smoke was **4/4** at
  `reports/local-20260819T000956Z`, and candidate Python is recursively
  byte-identical to immutable v0042. No 60-game gate, promotion, package,
  upload, activation, or live-state transition occurred. The next defense
  hypothesis must cover a more common failure surface than Sentinel tile
  overlap.

### v235 loaded-source forward infiltration — rejected after one repair — 2026-08-19

- The hypothesis tested the offensive infiltration idea with a live-stack
  signal: a visible enemy Harvester had to feed an accepting hostile
  Conveyor/Splitter carrying a resource stack, while the Builder retained a
  Harvester/two-Conveyor replacement reserve. The initial variant additionally
  required three own routes and an already-forward Builder; no fixed attacker,
  Store, route FSM, Launcher, or home-threat policy changed.
- Initial focused coverage was **29/29**, compileall passed, smoke was **4/4**,
  and static retained the inherited exit 2. The rotated 15-map screen was
  command/delivery-clean but only **4-11**, collecting **72,570 vs 82,460 Ti**
  and with one baseline no-delivery row; candidate TLE/suspicious rows were
  zero and max p99/peak was **1,359/5,629 us** (`reports/local-20260818T234949Z`,
  analysis `reports/iter-v235-loaded-source-forward-infiltration/replay-analysis.json`).
- The one bounded repair removed the route/half-map gate but retained the
  loaded/accepting outlet, duplicate-claim, and replacement-liquidity checks.
  Focused coverage stayed **29/29**, compileall/smoke stayed clean, and static
  was unchanged. The screen improved only to **6-9**, with collection
  **64,300 vs 76,380 Ti**, first-delivery mean **42.9 vs 24.3**, and Sentinels
  **25 vs 70**; no candidate no-delivery/TLE/suspicious rows occurred, max
  p99/peak **1,278/5,235 us** (`reports/local-20260818T235403Z`, analysis
  `reports/iter-v235-loaded-source-forward-infiltration/repair-replay-analysis.json`).
- Reject v235 after the allowed repair. Temporary dynamic/defender/test edits
  were removed; rollback coverage was **27/27**, compileall passed, static
  retained exit 2, and rollback smoke was **4/4** at
  `reports/local-20260818T235702Z`. Candidate Python is recursively
  byte-identical to immutable v0042. No 60-game gate, promotion, package,
  upload, activation, or live-state transition occurred. The next hypothesis
  must be a different workforce/pressure mechanism, not another infiltration
  selector without new causal replay evidence.

### v234 local orphan-Harvester reconnect — rejected after one repair — 2026-08-19

- The hypothesis exposed the existing local `_try_reconnect_orphaned_harvester`
  FSM to the dynamic selector after three completed routes, so a visible own
  Harvester without an accepting Conveyor/Splitter could claim one nearest
  local repair site. No route geometry, workforce, hijack/raid, combat, or
  Store policy changed.
- The initial implementation passed **31/31** focused tests, compileall and
  diff checks, smoke **4/4**, and inherited static exit 2. Its rotated 15-map
  screen lost **6-9**, collecting **87,470/90,670 Ti** (candidate/baseline),
  with first delivery **15/15 vs 15/15**, zero candidate no-delivery/TLE/
  suspicious rows, and max p99/peak **1,386/3,054 us**
  (`reports/local-20260818T232404Z`; analysis in
  `reports/iter-v234-local-orphan-harvester-reconnect/`).
- The one bounded repair limited the site to squared radius two. Focused
  coverage stayed **31/31**, compileall/smoke stayed clean, and static was
  unchanged, but the screen was **7-8**, collection **73,410/73,040 Ti**,
  first delivery **14/15 vs 15/15**, and one candidate no-delivery Valkyrie
  row; TLE/suspicious rows were zero and max p99/peak **1,483/3,654 us**
  (`reports/local-20260818T232702Z`). No 60-game gate was justified.
- Temporary source/test edits were removed. Rollback coverage was **27/27**,
  compileall passed, static retained exit 2, rollback smoke was **4/4** at
  `reports/local-20260818T233251Z`, and candidate Python is recursively
  byte-identical to immutable v0042. No promotion, package, upload,
  activation, or live-state transition occurred. Full record:
  `experiments/v0042-local-orphan-harvester-reconnect-v234.md`.

### v233 legal home-infiltrator block — rejected after one repair — 2026-08-19

- The current v0042 home-threat selector can see an enemy Builder but its
  generic strike path cannot legally damage Builder units. v233 tested a
  nearest-responder body-block on a visible, Core-facing, passable tile, with
  no Launcher, Barrier purchase, Store, route, workforce, or offensive-policy
  change. Focused coverage was **28/28**, compileall and diff checks passed,
  smoke was **4/4**, and static retained the inherited exit 2.
- The initial 15-map screen was command- and delivery-clean at **7-8**;
  collection was **42,760/64,350 Ti** (candidate/baseline), first delivery
  was **15/15 vs 15/15**, and candidate no-delivery/TLE/suspicious rows were
  **0/0/0**. Max p99/peak was **1,413/5,204 us** (`reports/local-20260818T230717Z`,
  analysis `reports/iter-v233-legal-home-infiltrator-block/initial-replay-analysis.json`).
- The one repair restricted blocking to an already-adjacent responder so a
  route worker would not chase a local threat. Focused coverage was **29/29**,
  compileall/smoke stayed clean, static was unchanged, but the screen fell to
  **6-9**, collection **75,560/84,330 Ti**, first delivery **15/15 vs 15/15**,
  and zero candidate no-delivery/TLE/suspicious rows; max p99/peak was
  **1,454/3,081 us** (`reports/local-20260818T231051Z`, analysis
  `reports/iter-v233-legal-home-infiltrator-block/repair-replay-analysis.json`).
- The hypothesis is rejected after the allowed repair. Temporary source/test
  edits were removed; rollback coverage was **27/27**, compileall passed,
  static retained exit 2, and rollback smoke was **4/4** at
  `reports/local-20260818T231454Z`. Candidate Python is recursively
  byte-identical to immutable v0042. No 60-game gate, promotion, package,
  upload, activation, or live transition occurred. Full record:
  `experiments/v0042-legal-home-infiltrator-block-v233.md` and
  `reports/iter-v233-legal-home-infiltrator-block/`.

### v232 bounded post-route ore-denial lease — rejected after one repair — 2026-08-19

- Replay evidence showed the exact v0042 baseline could place hundreds of
  unclaimed enemy-half Barriers (752 on Glacierkeep and 296 on Midgard in the
  saved sample), while top-team winners used a small shell. The candidate
  therefore changed `TASK_ORE_DENIAL` into one post-route lease per dynamic
  Builder, gated on three completed routes, confirmed enemy-Core intel, and a
  Harvester/two-Conveyor replacement reserve. No Store, route, fixed-attacker,
  or turret policy changed.
- The initial implementation passed **5/5** new tests plus **23/23**
  nearest-defense coverage, compileall, and smoke **4/4**; static retained
  the inherited exit 2. Its 15-map screen was **8-7**, collection
  **84,750/67,980 Ti**, Barriers **67/59**, Harvesters **98/119**, with one
  candidate no-delivery Royale row, zero TLE/suspicious rows, and max
  p99/peak **1,496/3,130 us** (`reports/local-20260818T224718Z`; parsed
  analysis `reports/iter-v232-bounded-ore-denial/replay-analysis.json`).
- The one repair additionally required the Builder to have observed a friendly
  Harvester/Conveyor/Splitter before spending its lease. Focused coverage was
  **6/6** new plus **23/23** nearest-defense (**29/29**), compileall/smoke
  stayed clean, and static was unchanged, but the screen fell to **7-8** with
  collection **69,560/89,900 Ti**, Barriers **52/67**, Harvesters **98/152**,
  and one candidate no-delivery Drakkarfjord row; max p99/peak was
  **1,319/3,005 us**, zero TLE/suspicious (`reports/local-20260818T225231Z`;
  parsed `reports/iter-v232-bounded-ore-denial/repair-replay-analysis.json`).
- The lease is rejected. Temporary source/test edits were removed; rollback
  focused coverage was **27/27**, compileall passed, static retained exit 2,
  smoke was **4/4** (`reports/local-20260818T225529Z`), and candidate Python
  is recursively byte-identical to immutable v0042. No 60-game gate,
  promotion, package, upload, activation, or live transition occurred. Full
  record: `experiments/v0042-bounded-ore-denial-lease-v232.md` and
  `reports/iter-v232-bounded-ore-denial/`.

### v231 unit-count loss replacement — rejected after one repair — 2026-08-19

- The workforce hypothesis used the authoritative team `get_unit_count()` as
  a delayed signal for an off-screen Builder death, while preserving the
  existing opening/reinforcement targets, reserve, role assignment, and unit
  cap. Focused coverage was **27/27**, compileall passed, smoke was **4/4**,
  and static retained the inherited exit 2.
- The initial 15-map screen was command/delivery-clean at **8-7**, but
  collection was **83,820/94,770 Ti** and placed Harvesters were
  **114/129** (candidate/baseline). There were zero TLE/suspicious rows; max
  p99/peak was **1,412/3,618 us** (`reports/local-20260818T222707Z`, replay
  analysis `reports/iter-v231-unit-count/replay-analysis.json`).
- The one allowed repair shortened confirmation from three rounds to two.
  Focused coverage stayed **27/27**, compileall/smoke stayed clean, static was
  unchanged, but the screen regressed to **6-9**, collection
  **41,870/56,710 Ti**, and Harvesters **92/127**, with zero TLE/suspicious
  rows (`reports/local-20260818T223103Z`, analysis
  `reports/iter-v231-unit-count/repair-replay-analysis.json`). The aggregate
  count cannot distinguish a dead Builder from a dead turret and is rejected.
- Temporary source/test were removed. Rollback focused coverage was **23/23**,
  compileall passed, static retained the inherited exit 2, smoke was **4/4**
  at `reports/local-20260818T223333Z`, and candidate Python is recursively
  byte-identical to immutable v0042 (`reports/iter-v231-unit-count/rollback/`).
  No 60-game gate, promotion, package, upload, activation, or live transition
  occurred. Next work must use a different workforce/pressure signal.

### v230 forward-infiltration lease — rejected after one repair — 2026-08-18

- Replay review found enemy Builder infiltration too infrequent to justify
  another dedicated defense loop: the v224 audit measured only 1–2
  pre-delivery route entries in the small loss/top-team samples, while the
  v225–v229 defensive/counter-infiltration variants had no paired win-rate
  edge. v230 therefore tested the offensive half: an already-forward Dynamic
  Builder with confirmed enemy-Core intel, three completed routes, and one
  live Sentinel could claim the existing local logistics raid before ordinary
  visible-ore work. Home workers, active chains, hijack, Launcher, and fixed
  attackers were unchanged.
- The initial implementation passed **5/5** new tests plus **28/28** in the
  nearest-defense subset, compileall, and smoke **4/4**; static retained the
  inherited exit 2. The 15-map screen was command/delivery-clean but lost
  **6-9**, collecting **59,020/73,950 Ti**, with zero no-delivery/TLE/
  suspicious rows (`reports/local-20260818T220818Z`; parsed analysis in
  `reports/iter-v230-forward-infiltration/regression-analysis.json`).
- The one bounded repair required the complete three-Sentinel shell before
  this lease could preempt harvesting. Focused coverage was **29/29**,
  compileall/smoke stayed clean, static was unchanged, and the screen again
  lost **6-9**, collecting **50,130/55,130 Ti**, with zero no-delivery/TLE/
  suspicious rows (`reports/local-20260818T221149Z`; analysis in
  `reports/iter-v230-forward-infiltration/repair-regression-analysis.json`).
- The temporary source/test were removed. Rollback focused coverage was
  **27/27**, compileall passed, static retained the inherited result, and
  smoke was **4/4** at `reports/local-20260818T221345Z`; candidate Python is
  recursively byte-identical to immutable v0042. No release gate, promotion,
  package, upload, activation, or live-state transition occurred. Choose a
  different workforce/pressure mechanism; do not widen the rejected raid
  lease or repeat the recent infiltration-defense branch without new evidence.

### v229 home-interceptor Launcher — rejected after one repair — 2026-08-18

- Replay-backed hypothesis: after three completed routes and a dynamic
  Harvester/conveyor reserve, the designated Defender could build one reactive
  home Launcher only for a live enemy Builder intruder; the Launcher would
  exile an adjacent enemy Builder to a farther legal tile. No opening,
  sabotage, hijack, or offensive Launcher policy changed.
- Focused legality/ownership coverage was **27/27**, compileall passed, smoke
  was **4/4**, and `make static` retained the inherited exit 2 (15 obsolete
  imports plus two navigation fast-path assertions).
- The initial rotated 15-map screen was command-clean but lost **6-9** against
  exact v0042, with collection **50,040 vs 60,620 Ti**, first-delivery mean
  **26.07 vs 28.07**, zero candidate no-delivery/TLE/suspicious rows, and four
  candidate Launcher placements (`reports/local-20260818T214418Z`). This was
  not a paired edge, so no release gate ran.
- The one bounded repair required the intruder to be inside the tighter Core
  radius and adjacent to the prospective build site. Focused coverage stayed
  **27/27**, compileall passed, repair static retained the inherited exit 2,
  and repair smoke was **4/4** at `reports/local-20260818T215650Z`; the
  repaired screen again lost **6-9** with
  the same **50,040 vs 60,620 Ti** and **26.07 vs 28.07** first-delivery means;
  no Launcher placement occurred (`reports/local-20260818T214923Z`).
- The temporary source, state, and test were removed. Rollback focused coverage
  was **27/27**, compileall passed, static retained the inherited exit 2, and
  rollback smoke was **4/4** at `reports/local-20260818T215408Z`. Candidate
  Python is recursively byte-identical to immutable v0042. No promotion,
  package, upload, activation, or live-state transition occurred. Full
  evidence: `experiments/v0042-home-interceptor-launcher-v229.md` and
  `reports/iter-v229-home-interceptor/`.

### v228 archived v208 post-route Launcher lifecycle — rejected at release gate — 2026-08-18

- The exact archived v208 candidate was restored as a release candidate after
  replay review confirmed its earlier **9-6** 15-map screen and observed
  Launcher movement events. It adds only the one-shot post-route Launcher
  lifecycle and exception-safe Launcher dispatch; v0042 remains the immutable
  comparator and moving baseline.
- Focused coverage was **28/28**, compileall passed, smoke **4/4**, and static
  retained the inherited exit 2. The rotated screen was **10-5**, delivery-
  clean, with collection **86,000 vs 67,600 Ti**, mean first delivery
  **31.0 vs 36.33**, and four Launcher placements
  (`reports/local-20260818T211807Z`).
- The 60-game gate was command-clean with zero TLE/suspicious rows but tied
  **30-30**, collection **247,680 vs 232,270 Ti**, candidate/baseline
  no-delivery **1/1**, mean first delivery **43.0 vs 40.08**, and
  Archipelago/Icefloe **2-2** each across four games. Max p99/peak were
  **1,595/5,250 us**
  (`reports/local-20260818T212023Z`).
- The archived source and temporary test/config were removed. Rollback focused
  was **23/23**, compileall passed, static retained the inherited result,
  smoke was **4/4** at `reports/local-20260818T212634Z`, and candidate Python
  is recursively byte-identical to v0042. No promotion, package, upload,
  activation, or live-state transition occurred. Full record:
  `experiments/v0042-post-route-launcher-lifecycle-v228.md`.

### v227 delivery-gated counter-infiltration — rejected after one repair — 2026-08-18

- Replay evidence suggested that dynamic counter-infiltration could steal
  opening workforce before the first own route. The candidate therefore gated
  the existing hijack FSM on one completed route plus a dynamic Harvester/two-
  Conveyor reserve, and assigned one nearest non-attacker owner; no new
  primitive or Store state was added.
- Focused coverage was **31/31**, compileall passed, smoke **4/4**, and static
  retained the inherited failures. Seed 172 was command/delivery-clean at
  **8-7**, collection **48,980/56,390 Ti**, first delivery **27.27/85.20**
  because the baseline had one no-delivery row, and zero candidate
  no-delivery/TLE/suspicious rows (`reports/local-20260818T205827Z`).
- A rotated seed-173 screen reversed to **7-8**, collection
  **74,190/91,380 Ti**, first delivery **89.60/23.80**, with one candidate
  no-delivery row (`reports/local-20260818T210032Z`). The one allowed repair
  permitted a funded steal after round 20 only when no own ore was visible or
  advised. It remained **7-8**, but collection became **64,250/63,620 Ti**,
  first delivery **23.13/27.20**, and no-delivery was **0/0**
  (`reports/local-20260818T210403Z`). No 60-game gate was justified.
- The phase gate, fallback, ownership logic, and temporary test were removed.
  Final rollback focused coverage was **27/27**, compileall passed, static kept
  the inherited result, and smoke was **4/4**
  (`reports/local-20260818T210643Z`). Candidate Python is recursively
  byte-identical to immutable v0042; no promotion, package, upload,
  activation, or live-state transition occurred. Full record:
  `experiments/v0042-delivery-gated-counter-infiltration-v227.md`.

### v226 vector-gated infiltrator intercept — rejected after two bounded repairs — 2026-08-18

- Replay review showed a response-latency proxy (v0042 route median 22 rounds
  versus top-team side-A median 6), but pre-delivery entries were rare. The
  candidate therefore tested a local, vector-confirmed enemy-Builder response:
  one inward movement observation, route-radius proximity, one completed route,
  nearest non-attacker ownership, and short expiry; no Store or unit-policy
  change.
- Focused coverage was **33/33**, compileall passed, smoke **4/4**, and static
  retained only the inherited deleted-module imports and navigation assertions.
  The 15-map screen was command/delivery-clean at **7-8**, collection
  **66,100/77,270 Ti**, mean first delivery **29.93/26.73**, zero TLE or
  suspicious rows (`reports/local-20260818T203054Z`).
- The first bounded repair added a one-Harvester-plus-one-Conveyor reserve;
  focused coverage was **34/34**, compileall/smoke stayed clean, but the screen
  remained **7-8** and collection fell to **54,070/68,580 Ti**
  (`reports/local-20260818T203358Z`).
- The second bounded repair moved interception below ordinary harvesting and
  narrowed its local radius to squared 9. Focused coverage was **32/32**,
  compileall/smoke stayed clean, but the screen remained **7-8** with
  **74,980/83,750 Ti** and mean first delivery **36.87/35.07**
  (`reports/local-20260818T204230Z`). Both repairs were command/delivery-clean
  with zero TLE/suspicious rows, so no 60-game gate was justified.
- After the two allowed repairs, both source variants and the temporary test
  were removed. Final rollback focused coverage was **27/27**, compileall
  passed, static kept the inherited result, and smoke was **4/4**
  (`reports/local-20260818T204703Z`). Every candidate Python file matches
  immutable v0042 byte-for-byte; no promotion, package, upload, activation, or
  live-state transition occurred. Full record:
  `experiments/v0042-vector-gated-infiltrator-intercept-v226.md`.

### v224 infiltration containment audit — completed; v225 queued — 2026-08-18

- The read-only v2 parser measured enemy Builder entries into our active route
  (Harvester/Conveyor/Splitter radius) and Core radius, separating pre-delivery
  route entries from normal late assaults. Replay positions cannot prove
  attack/build/hijack intent or assignment, so the response metric is an
  explicitly weak proxy.
- In the saved v84-loss sample, side A had pre-delivery route entries in
  **2/13** games with a response median of **22** rounds; side B had **1/13**
  with median **19**. In the saved top-team sample, both sides were **2/15**;
  route-response medians were **6** and **14**, and side A had no pre-delivery
  Core entries. The rejected v223 candidate had pre-delivery route entries in
  **6/15** games with median **34**, versus v0042's **5/15** and **27** in the
  same screen.
- This supports a protected opening economy rather than another local
  route-sentry or Launcher/ejection loop. The audit changed no production
  Python and left v0042 as the immutable baseline. Full record and table:
  `experiments/v0042-infiltration-containment-audit-v224.md` and
  `reports/iter-v224-infiltration-audit/summary.json`.
- Next bounded hypothesis (v225): before the first completed Harvester chain,
  keep the fixed attacker from crossing the geometric midline toward the enemy
  Core; preserve the cramped-map exception and all post-chain Sentinel/Core/
  sabotage gates. No dynamic threat detector, Store change, Launcher policy,
  route rewrite, package, upload, activation, or live-state edit is in scope.

### v225 protected-midline infiltration lease — rejected after repair — 2026-08-18

- The attacker-only lease passed **6/6** new focused tests and **33/33** in
  the nearest-defense/seeded-route subset; compileall passed, static retained
  the inherited 15 obsolete imports plus two navigation assertions, and smoke
  was **4/4**. The initial 15-map screen was **9-6**, command/delivery-clean,
  with **98,490 vs 71,020 Ti**, zero TLE/suspicious rows, and no protected-map
  0-4 collapse, so the 60-game gate ran.
- The 60-game endpoint-seed/both-side gate was command-clean but finished
  **29-31**, collection **239,120 vs 268,690 Ti**, delivery **58/60 vs 59/60**,
  and Drumlin **0-4**. The single allowed repair released the lease after
  confirmed enemy-Core intel; focused coverage stayed **6/6** new and **33/33**
  subset, compileall passed, static retained the same inherited profile, and
  smoke was **4/4**, but its screen fell to **5-10** with **63,740 vs 76,780 Ti**.
- No second repair or release gate was justified. The temporary lease and test
  were removed; candidate `attacker.py` matches v0042 byte-for-byte at
  SHA-256 `afa559f98a0694ab6c3355538098a0c845768413652124e08fc9b1035487a01a`.
  Rollback focused coverage was **27/27**, compileall passed, and rollback
  smoke was **4/4** at `reports/local-20260818T201638Z`. v0042 remains the
  baseline; no promotion, package, upload, activation, or live transition.
  Evidence: `experiments/v0042-infiltration-containment-audit-v224.md`,
  `reports/iter-v225-protected-midline/`, and the three screen/release report
  directories under `reports/local-*` recorded in the experiment file.

### v223 Sentinel-survival reset — rejected at screen — 2026-08-18

- The candidate attacker was reset to immutable v0042, then Luna added only
  visible enemy-turret fire-line rejection, a legal non-fire-line escape check,
  and deterministic farther-Core standoff selection for forward Sentinel sites.
  Existing dynamic pricing, economy/pool, blacklist/watch, `can_fire_from`, and
  `can_build_sentinel` gates were preserved; the v212/v222 pulse/Launcher hooks
  were removed. Untouched attacker methods are AST-equal to v0042.
- Focused coverage was **30/30**, compileall passed, `make static` retained the
  inherited 15 obsolete imports and two navigation assertions, and smoke was
  **4/4 command-clean** (`reports/local-20260818T193744Z`).
- The rotated 15-map seed-189 screen was command/delivery-clean with zero
  TLE/suspicious rows, but candidate-side lost **5-10** and collected
  **46,490 vs 67,930 Ti**. Mean first delivery was **32.13 vs 37.53**;
  candidate no-delivery was **0**. Candidate placed only **1.8 vs 3.9**
  Sentinels on average and finished with **0.7 vs 1.9** alive, so the safety
  filter suppressed rather than improved the forward shell.
- The hypothesis failed on its first screen; no 60-game gate, repair,
  promotion, package, upload, activation, or live transition is justified.
  The safe-site hunk and temporary test were removed; candidate `attacker.py`
  was restored byte-for-byte to v0042, post-rollback focused coverage was
  **33/33**, compileall passed, and rollback smoke was **4/4** at
  `reports/local-20260818T194338Z`. v0042 remains the immutable baseline. Full record:
  `experiments/v0042-sentinel-survival-reset-v223.md`; reports:
  `reports/iter-v223-sentinel-survival-reset/` and
  `reports/local-20260818T193828Z`.

### Next bounded work — v224 infiltration containment audit

- The next step is read-only replay analysis, not another production knob.
  Measure enemy Builder entry into our Core/Harvester/conveyor corridors,
  first-response delay, route/first-delivery impact, and whether our own
  infiltration produces a measurable conversion. Use the current baseline and
  the saved top-team sample, then choose one bounded defensive or offensive
  implementation hypothesis.
- Do not edit candidate Python, Store/schema, Launcher/teleport, turret,
  Sentinel/Barrier, raid, route, baseline, package, upload, activation, or live
  state during the audit. Avoid repeating v143 local route-sentry and the
  rejected v198/v208 Launcher/ejection loops without new causal evidence.

### v221 dimension-adaptive raid lease — rejected at release gate — 2026-08-18

- The bounded dynamic-builder branch admitted the existing loaded logistics
  raid only on compact boards and preserved harvest/advance on large geometry;
  no fixed-attacker, Store, cost, unit-cap, or platform surface changed.
- Focused coverage passed **7/7** new tests and **44/44** in the root subset;
  compileall passed, smoke was **4/4**, and `make static` retained only the
  inherited 15 obsolete imports plus two navigation assertions. The seed-187
  rotated screen was command- and delivery-clean at **8-7**, collection
  **77,110 vs 77,400 Ti**, max p99/peak **1,436/2,729 us**.
- The 60-game endpoint-seed/both-side release gate was command-clean with zero
  TLE/suspicious rows but finished **27-33**, collection **283,140 vs 290,860
  Ti**, candidate no-delivery **3** versus **1**, and max p99/peak
  **1,503/5,395 us**. Nordkap was **0-4**. The compact-only exception did not
  repair long-board pressure, so v221 was rejected.
- The exact pre-v221 dynamic SHA-256 was restored
  (`bcaa62c16403024e37a2149659160d04c01ec287d80679394d7bc8d7980651fd`), the
  temporary test/config removed, rollback focused coverage was **37/37**, and
  rollback smoke was **4/4** (`reports/local-20260818T190732Z`). v0042 remains
  baseline; no promotion, package, upload, activation, or live transition.
  Full record: `experiments/v0042-dimension-adaptive-raid-v221.md`; reports:
  `reports/local-20260818T185744Z` and
  `reports/iter-v221-dimension-adaptive-raid/`.

### v222 rotating secondary pressure lease — rejected at screen — 2026-08-18

- Luna implemented the strict role split: the primary fixed attacker stayed on
  the Core/sentinel lane, while only the designated second attacker could take
  one reserve-gated economy sabotage cycle and then return. Root review found
  no legality or ownership violation; the new tests passed **6/6** and the root
  focused subset **43/43**.
- Compileall passed, smoke was **4/4** at `reports/local-20260818T192030Z`,
  and static retained only the inherited 15 obsolete imports and two
  navigation assertions. The seed-188 15-map screen was command-clean with
  zero TLE/suspicious rows but lost **1-14**, collected **41,340 vs 75,000 Ti**,
  had mean first delivery **91.93 vs 27.87**, and no-delivery **1 vs 0**.
  Seven maps placed no candidate Sentinel and most others only one; max
  p99/peak was **1,402/4,036 us**. No release gate or repair was justified.
- The exact pre-v222 attacker SHA-256 was restored
  (`e450ce16dbfae8d581373ee398eea1b6fb9e898bd0925ea2d6c721de77295183`), the
  temporary test/config removed, rollback focused coverage was **37/37**, and
  rollback smoke was **4/4** at `reports/local-20260818T192409Z`. v0042 remains
  baseline; no promotion, package, upload, activation, or live transition.
  Record: `experiments/v0042-rotating-secondary-pressure-v222.md`; reports:
  `reports/local-20260818T192113Z` and
  `reports/iter-v222-rotating-secondary-pressure/`.

### Next bounded experiment — v223 sentinel-survival reset

- Stop layering unpromoted raid/pulse code. Reset `bots/candidate/bot/attacker.py`
  to exact v0042 behavior, then test only a replay-backed safe-standoff
  Sentinel placement/replacement-reserve strategy. The goal is a live forward
  shell that enables continuous offense, not another economy-target selector.
- Luna owns only the attacker placement change and focused Sentinel safety
  tests. No dynamic priority, sabotage lease, new Store schema, cost/cap,
  Launcher policy, map branch, package, upload, activation, or live-state edit
  is allowed.


### v215 raid-first offense lease — rejected at release gate — 2026-08-18

- The bounded reorder let a dynamic Builder select the existing nearest-owner
  loaded Conveyor/Splitter/Harvester raid before its confirmed-Core advance
  fallback, while preserving home threat, belt/base repair, hijack, and CHAIN
  priorities. Luna's session stalled, so root completed the same scoped patch;
  no new primitive, reserve, Store slot, or unit cap was introduced.
- Focused coverage was **5/5** in the raid-first module and **42/42** in the
  root subset; candidate compileall passed, smoke was **4/4** at
  `reports/local-20260818T174349Z`, and static retained the inherited exit 2
  (15 obsolete deleted-module imports plus two navigation assertions).
- The rotated all-map screen was command- and delivery-clean at **8-7**, so
  the 60-game gate ran. It was also command- and delivery-clean with zero
  TLE/suspicious rows: **32-28 (53.33%)**, collection **286,570 vs 232,590
  Ti**, mean first delivery **27.51 vs 30.77**, max p99/peak
  **1,314/6,807 us**. Ragnarok was **0-4**, with Fjordgate and Glacierkeep
  **1-3** each; the protected-map guard therefore failed despite the positive
  aggregate.
- The exact pre-v215 `dynamic.py` hash was restored, temporary test/config
  files were removed, and rollback coverage was **37/37** plus compileall.
  v0042 remains the baseline; no promotion, package, upload, activation, or
  live transition occurred. Evidence: `experiments/v0042-raid-first-offense-
  lease-v215.md`, `reports/local-20260818T174619Z`, and
  `reports/iter-v215-raid-first-offense/`.

### Next bounded experiment — v216 pressure-lane raid lease

- Continue the offense/sabotage direction, but require at least four completed
  routes and confirmed enemy-Core intel before a dynamic Builder raids. The
  existing loaded logistics target must also be on a strict forward pressure
  lane toward the enemy Core; off-lane targets leave the Builder on harvest or
  advance. This directly tests whether v215's Ragnarok economy collapse came
  from chasing visible but strategically lateral logistics.
- Luna owns only the dynamic branch and focused priority/legality tests. No
  new Store schema, primitive, reserve, Sentinel cap, fixed-attacker, map-name
  branch, package, upload, activation, or live-state edit is allowed before
  the rotated screen and release guard.

### v216 pressure-lane raid lease — rejected at 15-map screen — 2026-08-18

- To address v215's Ragnarok 0-4 collapse, the bounded dynamic lease required
  four completed routes, SCOUT mode, confirmed enemy-Core intel, a nearest
  owner, a loaded Conveyor/Splitter, and strict progress toward the Core before
  raiding ahead of visible harvest. Protected home/repair/hijack/CHAIN tasks
  and the old no-ore fallback were unchanged.
- Root completed the patch after the Luna session stalled. Focused coverage
  was **8/8** in the new module and **45/45** in the root subset; compileall
  passed, smoke was **4/4** at `reports/local-20260818T180400Z`, and static
  retained the inherited exit 2 (15 obsolete imports plus two navigation
  assertions).
- The rotated 15-map screen was command-clean with zero TLE/suspicious rows,
  but lost **6-9** candidate-side. Collection was **47,400 vs 66,380 Ti**,
  mean first delivery **45.21 vs 38.07**, and max p99/peak **1,585/5,693 us**;
  Icefloe and Nordkap were both losses. The aggregate and protected-map gates
  failed, so no release matrix ran.
- The exact pre-v216 dynamic hash was restored, temporary test/config files
  were removed, rollback was **37/37** plus compileall, and v0042 remains the
  immutable baseline. No promotion, package, upload, activation, or live
  transition occurred. Evidence: `experiments/v0042-pressure-lane-raid-
  v216.md`, `reports/local-20260818T180436Z`, and
  `reports/iter-v216-pressure-lane-raid/`.

### Next bounded experiment — v217 continuous fixed-attacker pressure lease

- Keep dynamic Builders on their existing economy policy and build on the
  already-designated fixed-attacker pulse: after legal sabotage or a stale
  target, choose the next loaded logistics/Harvester target, a Core shot, or
  one strict-progress step. This preserves continuous offense without another
  global dynamic-worker diversion.
- Scope is only `bots/candidate/bot/attacker.py`, one focused test module, and
  durable records. No new Store schema, primitive, reserve/cap, route, map
  branch, package, upload, activation, or live-state change is allowed before
  the rotated screen and release guard.

### v217 continuous fixed-attacker pressure lease — rejected at screen — 2026-08-18

- The bounded attacker-only phase reorder let pending/visible pressure run
  before Launcher/Core-barrier topology while preserving the existing reserve,
  Sentinel, ownership, and legality gates. Focused coverage was **5/5** in the
  new module and **42/42** in the root subset; compileall passed, smoke was
  **4/4** at `reports/local-20260818T181203Z`, and static retained inherited
  failures.
- Seed-182 was command- and delivery-clean at **8-7**, but collection was
  **52,850 vs 74,180 Ti**, mean first delivery **78.13 vs 26.53**, and three
  candidate losses first delivered at rounds 121, 589, and 257. A bounded
  repair retained only pending-pulse priority; seed-183 stayed command-clean
  at **7-8**, collection **81,780 vs 91,470 Ti**, first delivery
  **23.13 vs 29.27**, max p99/peak **1,362/4,924 us**, with protected
  Icefloe/Nordkap/Ragnarok losses. Neither screen earned a release gate.
- Exact pre-v217 `attacker.py` parity was restored, temporary test/config
  files were removed, rollback was **37/37** plus compileall, and v0042
  remains baseline. No promotion, package, upload, activation, or live
  transition occurred. Evidence:
  `experiments/v0042-continuous-fixed-attacker-pressure-v217.md`,
  `reports/local-20260818T181237Z`, and
  `reports/local-20260818T181610Z`.

### Next bounded experiment — v218 economy-safe continuous raid lease

- Return to dynamic sabotage only when it is economically replaceable: keep
  visible harvest ahead while ore is available, and admit one nearest loaded
  logistics raid after the offense milestone, a Harvester-cost replacement
  bank plus the existing attack reserve, and confirmed enemy-Core intel. The
  target then hands off to the existing advance/repair loop.
- Scope is only `bots/candidate/bot/dynamic.py`, one focused test module, and
  durable records. No fixed-attacker, Store-schema, primitive, Sentinel-cap,
  route, map branch, package, upload, activation, or live-state edit is allowed
  before the rotated screen and release guard.

### v218 economy-safe continuous raid lease — rejected at release gate — 2026-08-18

- v218 admitted one dynamic loaded-logistics raid only after visible harvest
  was unavailable, the normal offense milestone was complete, confirmed Core
  intel existed, and the bank could replace a Harvester while retaining the
  existing attack reserve. Focused coverage was **6/6** in the new module and
  **43/43** in the root subset; compileall passed, smoke was **4/4** at
  `reports/local-20260818T182237Z`, and static retained inherited failures.
- The rotated screen was **10-5**, command/delivery-clean with no no-delivery
  rows, collection **58,130 vs 52,640 Ti**, and max p99/peak **1,430/5,828
  us**, so the release gate ran. The 60-game matrix was command/delivery-clean
  with zero TLE/suspicious rows but finished **30-30**; collection was
  **271,280 vs 284,390 Ti**, mean first delivery **29.14 vs 26.31**, and
  no-delivery rows **2 vs 1**. Antler, Auroraveil, Drumlin, Icefloe, and
  Midgard were **1-3** floors. The screen edge did not transfer.
- Exact pre-v218 dynamic parity was restored, temporary test/config files were
  removed, rollback was **37/37** plus compileall, and v0042 remains baseline.
  No promotion, package, upload, activation, or live transition occurred.
  Evidence: `experiments/v0042-economy-safe-raid-lease-v218.md`,
  `reports/local-20260818T182307Z`, `reports/local-20260818T182519Z`, and
  `reports/iter-v218-economy-safe-raid/`.

### Next bounded experiment — v219 defensive-to-offensive ore denial lease

- When no local ore is available and the offense milestone plus replacement
  bank is real, let one dynamic Builder place the existing enemy-half ore-
  denial Barrier before raid/advance. This denies future opponent income more
  cheaply than chasing an unreliable loaded belt, then returns to the existing
  pressure path; visible harvest and protected tasks remain ahead.
- Scope is only `bots/candidate/bot/dynamic.py`, one focused test module, and
  durable records. No fixed-attacker, Store-schema, primitive, cap, route,
  map-branch, package, upload, activation, or live-state change is allowed
  before the rotated screen and release guard.

### v219 defensive-to-offensive ore denial lease — rejected at screen — 2026-08-18

- The bounded dynamic lease placed one existing enemy-half ore-denial Barrier
  only when no local/advised ore was available, the offense milestone and a
  Harvester-plus-Barrier replacement bank were real, and enemy-Core intel was
  confirmed. Focused coverage was **7/7** in the new module and **44/44** in
  the root subset; compileall passed, smoke was **4/4** at
  `reports/local-20260818T183618Z`, and static retained inherited failures.
- The rotated 15-map screen was command-clean with zero TLE/suspicious rows,
  but candidate-side lost **6-9**, collected **38,600 vs 68,300 Ti**, and had
  one candidate no-delivery row. The aggregate and delivery gates failed, so
  no release matrix ran.
- Exact pre-v219 dynamic parity was restored, temporary test/config files were
  removed, rollback was **37/37** plus compileall, and v0042 remains baseline.
  No promotion, package, upload, activation, or live transition occurred.
  Evidence: `experiments/v0042-ore-denial-pressure-v219.md`,
  `reports/local-20260818T183650Z`, and
  `reports/iter-v219-ore-denial-pressure/`.

### Next bounded experiment — v220 corridor-loaded raid lease

- Keep active loaded sabotage, but admit it only when the
  Builder-to-target-to-confirmed-Core route detour is short. This allows
  useful lateral logistics pressure while preventing v215's off-lane chase;
  visible ore can continue for other workers and protected tasks remain ahead.
- Scope is only `bots/candidate/bot/dynamic.py`, one focused corridor/raid
  module, and durable records. No passive Barrier priority, fixed-attacker,
  Store-schema, primitive, cost/cap, route, map branch, package, upload,
  activation, or live-state change is allowed before the rotated screen and
  release guard.

### v220 corridor-loaded raid lease — rejected at release gate — 2026-08-18

- The bounded active raid lease required the Builder-to-target-to-confirmed-
  Core Manhattan detour to be at most six tiles, retaining existing reserve,
  loaded, nearest, and legality gates while allowing visible ore for other
  workers. Focused coverage was **8/8** in the new module and **45/45** in the
  root subset; compileall passed, smoke was **4/4** at
  `reports/local-20260818T184201Z`, and static retained inherited failures.
- The rotated screen was **8-7**, command/delivery-clean with no no-delivery
  rows, collection **81,430 vs 66,320 Ti**, mean first delivery **24.53 vs
  26.00**, max p99/peak **1,407/5,276 us**, so the 60-game gate ran. The gate
  was command-clean with zero TLE/suspicious rows but finished **24-36**;
  collection **262,580 vs 300,390 Ti**, first delivery **28.00 vs 30.35**, no-
  delivery **1 vs 0**, and Drakkarfjord/Glacierkeep **0-4** floors.
- Exact pre-v220 dynamic parity was restored, temporary test/config files were
  removed, rollback was **37/37** plus compileall, and v0042 remains baseline.
  No promotion, package, upload, activation, or live transition occurred.
  Evidence: `experiments/v0042-corridor-loaded-raid-v220.md`,
  `reports/local-20260818T184229Z`, `reports/local-20260818T184443Z`, and
  `reports/iter-v220-corridor-raid/`.

### Next bounded experiment — v221 dimension-adaptive raid lease

- Preserve active loaded raids on compact boards but keep dynamic Builders on
  economy/advance on large geometry, using width/height context rather than
  map names. This directly targets the 30x30 Drakkarfjord/Glacierkeep
  collapse without another passive Barrier or fixed-attacker diversion.
- Scope is only `bots/candidate/bot/dynamic.py`, one focused dimension-adaptive
  module, and durable records. No map-name branch, Store schema, primitive,
  cost/cap, route, package, upload, activation, or live-state edit is allowed
  before the rotated screen and release guard.

### v214 intel-backed offense lease — rejected at screen — 2026-08-18

- Fresh v213 loss replays showed route-preserving but under-converted states:
  several maps ended with few/no surviving Sentinels and a smaller pressure
  shell than the opponent. Luna therefore added one bounded dynamic phase:
  consume the existing Store-slot-9 enemy-Core sighting and, after
  `OFFENSE_MIN_HARVESTERS` in SCOUT mode, select `TASK_ADVANCE` before visible
  ore. Home threat, belt/base repair, Harvester hijack, and active CHAIN work
  stayed ahead; no Store/weapon/reserve/cap changes were made.
- Focused v214 coverage was **4/4** in Luna's run and **41/41** in the root
  subset; candidate compileall passed. `make smoke` was **4/4** at
  `reports/local-20260818T172547Z`. `make static` retained the inherited exit
  2 (15 obsolete deleted-module import errors and two navigation fast-path
  failures), with no v214-specific failure. Logs are in
  `reports/iter-v214-intel-backed-offense/`.
- The rotated seed-179 all-map screen was command-clean and delivery-clean:
  **7-8** candidate-side across all 15 maps, zero TLE/suspicious/no-delivery
  rows, collection **73,200 vs 76,060 Ti**, mean first delivery **24.87 vs
  21.47**, and max p99/peak **1,354/2,926 us**. Icefloe and Nordkap were both
  wins, but the required aggregate edge failed, so no 60-game gate ran.
- Reject and restore the exact pre-v214 dynamic source (hash matches the
  snapshot), remove the temporary focused test/config, and keep v0042 as the
  immutable baseline. Rollback verification was **37/37** focused tests plus
  candidate compileall. No promotion, package, upload, activation, or live
  transition occurred. Evidence:
  `experiments/v0042-intel-backed-offense-lease-v214.md`,
  `reports/local-20260818T172622Z/manifest.json`,
  `reports/iter-v214-intel-backed-offense/edited-screen-replay-analysis.json`,
  and `state/project_state.json`.

### v213 adaptive pressure handoff — rejected at screen — 2026-08-18

- Luna added only a bounded fixed-attacker handoff in `attacker.py` plus five
  focused tests. It repairs the nearest visible damaged Harvester/Conveyor/
  Splitter only when the forward Sentinel shell or three-Harvester floor is
  absent, preserves nearest ownership, danger-safe movement, and existing
  action-legality gates, then returns to the v212 pressure pulse when the
  shell recovers. Focused coverage was **5/5** and candidate compileall passed.
- `make static` retained the inherited exit 2 from obsolete deleted-module
  imports and two navigation fast-path assertions; no v213-specific failure.
  `make smoke` was **4/4** (`reports/local-20260818T170106Z`).
- The rotated all-map seed-178 screen was command-clean and delivery-clean:
  **8-7** candidate-side, zero TLE/suspicious/no-delivery rows, collection
  **94,090 vs 100,370 Ti**, mean first delivery **28.4 vs 30.0**, and max
  p99/peak **1,388/2,557 us**. It improved the exact v212 snapshot's 5-10
  result, but Nordkap remained **0-1** and the required Icefloe/Nordkap floor
  did not improve; collection also regressed versus v0042.
- Reject and roll back to the exact pre-v213 attacker hash; remove the focused
  test. v0042 remains baseline. No 60-game gate, package, upload, activation,
  promotion, or live-state change. Evidence:
  `experiments/v0042-adaptive-pressure-handoff-v213.md`,
  `reports/local-20260818T170142Z`, and
  `reports/iter-v213-adaptive-pressure/edited-screen-replay-analysis.json`
  plus the captured inherited-static log
  `reports/iter-v213-adaptive-pressure/static.log`.

### v212 continuous offence pulse — gate positive, promotion held — 2026-08-18

- Luna implemented a bounded one-step fixed-attacker offense pulse in
  `attacker.py`: after legal fire/stale-target transitions, the designated
  nearest attacker selects loaded logistics/Harvester pressure, confirmed-Core
  pressure, or one danger-safe strict-progress cardinal step. Existing
  Harvester, Sentinel, reserve, and legality gates remain. Focused coverage was
  **45/45**, compileall passed, smoke **4/4**, and static retained only the
  inherited failures.
- The immutable snapshot screen (seed 177) was **4-11**, with one candidate
  no-delivery row. The edited screen reversed to **11-4**, delivery-clean, with
  collection **55,420 vs 48,550 Ti**, first delivery **28.80 vs 30.33**, and
  max p99/peak **1,513/3,250 us**. Reports:
  `reports/parallel-v212-screen/` and `reports/local-20260818T163452Z`.
- The required 60-game endpoint-seed/both-side gate was command-clean,
  zero-TLE/suspicious, and **33-27 (55.0%)** candidate-side. Collection was
  **220,550 vs 224,920 Ti**, first delivery **35.90 vs 27.40**, max p99/peak
  **1,473/3,873 us**, and no-delivery rows were **1 vs 2**. Map floors included
  Icefloe **0-4**, Frostgate/Nordkap **1-3**; therefore the aggregate edge is
  not promoted under the protected-map guard. Full evidence:
  `reports/local-20260818T163712Z` and
  `reports/iter-v212-continuous-offence/release-replay-analysis.json`.
- v0042 remains baseline. No package, upload, activation, or live transition.
  Next work must make pressure map/context-adaptive without simply increasing
  pulse frequency or spending more reserve; v212 source remains unpromoted for
  the next bounded experiment.

### v211 delivery-confirmed route milestone rejected — 2026-08-18

- Luna implemented a local eight-round VERIFY phase after geometric Conveyor
  completion, retaining the exact terminal identity and delaying the existing
  Harvester Store milestone until a positive sink observation. Focused
  verification coverage was **5/5**, the root regression subset **45/45**,
  compileall passed, and smoke was **4/4**. `make static` retained only the
  inherited exit 2 from obsolete deleted-module imports and two navigation
  fast-path assertions.
- The fair seed-176 15-map screen was **3-12** against exact v0042,
  command-clean and delivery-clean, with zero TLE/suspicious rows. Collection
  was **52,520 vs 89,840 Ti** and mean first delivery **23.93 vs 23.20**;
  max p99/peak were **1,291/2,327 us**. The edited candidate was decisively
  negative, so no 60-game gate ran.
- The exact pre-v211 candidate snapshot was restored (main.py and defender.py
  hashes match), and the temporary test/config were removed. v0042 remains
  baseline; no promotion, package, upload, activation, or live transition.
  Evidence: `experiments/v0042-delivery-confirmed-route-milestone-v211.md`,
  `reports/local-20260818T161743Z`, and
  `reports/iter-v211-verify-milestone/`.

### Next bounded direction — continuous offence pulse

- Replay losses show ready fixed attackers reaching a full Sentinel shell with
  no valid economy target, while top teams keep alternating Core pressure,
  loaded-belt/Harvester sabotage, and forward Barrier/Sentinel work. The next
  hypothesis is a bounded offense pulse: after a legal offensive action or a
  confirmed stale target, a funded fixed attacker must choose the next visible
  pressure action or a strict-progress reposition before returning to the Core
  lane. Dynamic Builders keep their economy/repair gates; this is not a global
  offense-priority rewrite.
- The implementation scope is limited to the existing attacker offense state,
  one bounded phase/target test, and tuning constants only if required. No new
  Store slot/schema, Launcher lifecycle, Sentinel cap, route milestone,
  economy gate, map branch, baseline, package, upload, activation, or live
  state changes are allowed.
- First run a Luna snapshot screen against exact v0042 on all 15 maps. Require
  command-clean execution, no new no-delivery rows, and a clear aggregate
  win-rate edge before any 60-game release gate; otherwise perform at most one
  bounded repair and restore exact parity. Continuous offense must beat the
  current v0042 baseline, not merely improve collection or unit counts.

### v210 replay audit — sentinel-witnessed local pressure phase — 2026-08-18

- The fresh seed-173 screen of the exact pre-edit candidate was **7-8**,
  command-clean and delivery-clean, so no long gate was run. Losses showed a
  pressure stock gap on several maps (fewer Barriers/Sentinels than the paired
  winner), while O(1) winners often used no Launcher. Replay audit:
  `experiments/.tmp-existing-signal-replay/existing-sentinel-phase.md`.
- Approved next hypothesis: use existing delayed `SLOT_SENTINEL_COUNT` plus
  the existing Harvester offense gate as a pressure witness; let only an
  already-forward dynamic Builder perform one local, escape-safe Barrier or
  pressure action, then return to its prior task. No new Store slot, lease,
  Launcher lifecycle, opener, or cap change is allowed.
- The seed-173 screen artifacts are under
  `reports/parallel-v209-seed173/` (`reports/local-20260818T152624Z`), with
  zero TLE/suspicious/no-delivery rows and collection **48,910 vs 47,880 Ti**.
  v0042 remains the immutable baseline; implementation and any long gate await
  the bounded v210 candidate screen.

### v210 sentinel-witnessed pressure phase rejected — 2026-08-18

- Luna implementation used existing delayed `SLOT_SENTINEL_COUNT` plus the
  Harvester offense gate to give an already-forward dynamic Builder one local,
  escape-safe Core-cage/pressure event. Focused coverage was **32/32** and
  compileall passed. The first attempt hit the platform's forbidden-`finally`
  validator; the bounded syntax repair passed `make smoke` **4/4**. Static
  retained the inherited exit **2**. Logs:
  `reports/iter-v210-sentinel-pressure/`.
- The exact pre-edit candidate scored **3-12** on seed 174 (15/15 clean,
  delivery-clean, collection **77,640/97,200 Ti**). The repaired candidate
  improved to **6-9** (15/15 clean, delivery-clean, collection
  **79,560/78,740 Ti**) but was not a positive paired screen, so no 60-game
  gate was run. Raw reports:
  `reports/parallel-v210-screen/replay-analysis.json` and
  `reports/iter-v210-sentinel-pressure/edited-screen-replay-analysis.json`.
- Reject and roll back: both owned source files match the exact pre-v210
  snapshot, the temporary support test was removed, rollback focused coverage
  was **28/28**, and rollback compileall passed. v0042 remains baseline; no
  promotion, package, upload, activation, or live transition occurred.
- Lesson: the pressure gap is real, but an unbudgeted per-Builder witness did
  not convert into a positive screen. Next work must use fresh replay causality
  and existing Store ownership, not this selector or a Store-schema migration.

### v211 release-gate result and replay direction — 2026-08-18

- The promising seed-175 screen (10-5) justified the complete endpoint-seed,
  both-side 60-game gate against exact v0042. It finished **28-32** for the
  candidate, command-clean with zero TLE/suspicious rows, collection
  **279,380 vs 300,630 Ti**, candidate first-delivery mean **38.54 vs 54.42**
  among delivered games, and one candidate no-delivery row versus zero for
  v0042. Max p99/peak were **1,562/5,475 us**. Full raw report:
  `reports/local-20260818T155712Z`; replay reduction:
  `reports/iter-v211-release-gate-replay-analysis.json`; gate log:
  `reports/iter-v211-release-gate.log`.
- Reject the gate and keep v0042 as baseline. Map floors were strong on
  Ragnarok (**4-0**) and Valkyrie (**3-1**) but weak on Royale (**0-4**),
  Antler/Archipelago/Icefloe/Nordkap (**1-3** each). Do not promote or
  package/upload/activate this candidate.
- The parallel Luna loss audit groups failures into delayed first delivery,
  false geometric route milestones, and post-milestone collection plateaus.
  It proposes a delivery-confirmed local VERIFY phase before publishing the
  existing Harvester milestone; record:
  `experiments/.tmp-v211-replay-audit/audit.md`. Continuous offense remains a
  queued follow-up after this verification phase, not an unbounded task-priority
  change in the same checkpoint.

### v209 parallel Launcher-lease feasibility checkpoint — 2026-08-18

- Two Luna workers ran in parallel: one froze the current candidate before
  edits and screened it against exact v0042; the other attempted the bounded
  replay-derived route-stall rendezvous lease. The snapshot screen was **5-10**
  over 15 maps, **15/15 command-clean**, delivery-clean, with zero
  TLE/suspicious output, collection **44,120 vs 54,980 Ti**, and max p99/peak
  **1,312/5,174 us**. Evidence:
  `reports/parallel-v208-screen/replay-analysis.json` and
  `experiments/v0042-route-stall-rendezvous-v209.md`.
- The implementation worker made no production edits after finding all 16
  Store slots already assigned. A safe named lease would require an ore-ring
  schema/read/write migration plus delayed-write guards, outside this bounded
  iteration. No promotion, release gate, package, upload, activation, or live
  state transition occurred; v0042 remains immutable baseline.
- Existing Launcher focused coverage remained **5/5**, candidate compileall
  passed, `make static` retained its inherited exit **2**, and `make smoke`
  was **4/4 command-clean**. Logs are under
  `reports/iter-v209-rendezvous-lease/` (smoke replay:
  `reports/local-20260818T152217Z`).
- The parallel protocol is now documented in `AGENTS.md`: snapshot first,
  one production writer, root reconciliation, and no unsafe Store widening.
  Next work must use an existing signal or a non-lease unit-control idea.

### v208 post-route Launcher lifecycle — 2026-08-18

- Implemented a fundamentally new Launcher lifecycle in `main.py` and
  `attacker.py`: one fixed attacker may build one dynamic-price Launcher only
  after three completed routes, a confirmed enemy Core, one live forward
  Sentinel, and reserves for one Harvester plus two Conveyors. The Launcher
  accepts either-team adjacent Builders and selects only legal, passable,
  strict-progress ally insertions or enemy ejections. Focused coverage was
  **5/5**, compileall passed, and smoke was **4/4**.
- The original rotated seed-172 15-map screen was **9-6** against exact v0042,
  command-clean with zero TLE/suspicious/no-delivery rows. Candidate first
  delivery averaged **22.67 vs 28.67**, max p99/peak were **1457/2166 us**,
  and three maps placed Launchers; two had a field-16 jump from a Launcher
  tile within the documented throw radius. Full evidence:
  `reports/iter-v208-launcher-lifecycle/replay-analysis.json`,
  `reports/local-20260818T144551Z`, and
  `experiments/v0042-post-route-launcher-lifecycle-v208.md`.
- Two bounded repairs were rejected and removed: replay indicator
  instrumentation fell to **7-8** (`reports/local-20260818T145245Z`), and a
  one-round attacker rendezvous hold fell to **5-10** with delivery **37.47 vs
  28.13** (`reports/local-20260818T145801Z`). Final focused/compile/static/
  smoke logs are under `reports/iter-v208-launcher-lifecycle/`; static remains
  the inherited 15 deleted-module imports plus two navigation assertions.
- Keep the original v208 source as an **unpromoted local candidate** while
  v0042 remains the immutable baseline. No release gate, package, upload,
  activation, or live-state transition occurred. The next experiment should
  address top-team repeated Launcher relay/rendezvous timing rather than
  retune this late one-shot gate.

### v207 Launcher/unit-control replay audit — 2026-08-18

- Read-only audit of 15 high-ranking replays and the v206 seed-171 repair
  screen. Top winners placed Launchers in **8/15** games and averaged **3.27**
  versus **0.40** for paired losers; winner means were 5.0 Harvesters, 13.7
  Barriers, 3.6 Sentinels, and first delivery round 21.1.
- The compact replay field 16 is an actor id plus a two-coordinate Builder
  position event; no unambiguous Launcher action field was found. Both v206
  and v0042 placed zero Launchers on seed 171, so v206 did not exercise the
  mobility mechanism seen in the top sample. Report:
  `reports/iter-v207-launcher-lifecycle-audit.json`.
- Decision: implement a bounded post-route Launcher lifecycle next—one fixed
  attacker may build one forward Launcher after a proven route/Sentinel reserve,
  and the Launcher must perform a legal pickup plus strict-progress destination
  selection. Do not infer success from placement alone. Full scope is in
  `docs/CURRENT_PLAN.md` and the v208 experiment record to be created during
  implementation.

### v206 coordinated forward assault rejected — 2026-08-18

- Replay evidence showed top teams use a coordinated forward lane, not an
  isolated Barrier task. v206 added one dynamic support Builder that could
  alternate Barrier/Sentinel actions only near a fixed attacker and confirmed
  enemy Core. Focused coverage was **27/27**, compileall passed, static kept
  inherited failures, and smoke was **4/4**.
- The rotated seed-171 screen was **6-9**, command-clean with no TLE,
  suspicious-output, or no-delivery rows; delivery was **24.0 vs 36.4** and
  Harvesters **142 vs 119**, but pressure/collection lagged (**58 vs 67
  Barriers**, **36 vs 46 Sentinels**, **74,750 vs 85,530 Ti**). The one repair
  front-loaded a Sentinel when the lane had no damage source; checks were
  **28/28**, compileall/smoke clean, static inherited red, but the same screen
  stayed **6-9** and added an Icefloe no-delivery row. Reports:
  `reports/local-20260818T142738Z`,
  `reports/iter-v206-forward-assault-replay-analysis.json`,
  `reports/local-20260818T143031Z`, and
  `reports/iter-v206-forward-assault-repair-replay-analysis.json`.
- Reject v206 after the permitted repair. Candidate source is recursively
  identical to immutable v0042; rollback nearest-defense was **23/23**,
  compileall passed, static retained exit 2, and rollback smoke was **4/4**.
  Record: `experiments/v0042-coordinated-forward-assault-v206.md`. No release
  gate, package, upload, activation, or live transition occurred.
- The next step is a fresh raw Launcher/unit-control replay audit before any
  new source edit; it is recorded in `docs/CURRENT_PLAN.md`.

### v205 route-funded dynamic forward shell rejected — 2026-08-18

- Replay review found high-ranking winners convert a fast route into a
  coordinated forward shell (Barriers plus Sentinel/Launcher pressure), while
  v0042's comparator side averaged 8.0 Harvesters, 4.3 Barriers, 2.5 Gunners,
  and no Launchers. v205 added a reserve-gated dynamic Builder shell after
  three completed routes. Focused coverage was **27/27**, compileall passed,
  static retained inherited failures, and smoke was **4/4**.
- The rotated seed-170 screen was **6-9**, command-clean with zero
  TLE/suspicious/no-delivery rows, but first delivery regressed to **44.87 vs
  22.73** for v0042. A structural repair restricted shell assignment to
  Builders already in the forward zone; focused coverage was **28/28**, smoke
  **4/4**, and static remained inherited red. The same screen improved to
  **7-8** and first delivery **22.47 vs 28.00**, but collection/Barrier stock
  fell to **62,470 vs 69,320 Ti** and **52 vs 87**.
- Reject v205 after the permitted repair. Candidate source is recursively
  identical to immutable v0042; rollback nearest-defense was **23/23**,
  compileall passed, static retained exit 2, and rollback smoke was **4/4**.
  Reports: `reports/local-20260818T141745Z`,
  `reports/iter-v205-dynamic-shell-replay-analysis.json`,
  `reports/local-20260818T142059Z`, and
  `reports/iter-v205-dynamic-shell-repair-replay-analysis.json`. Record:
  `experiments/v0042-route-funded-dynamic-forward-shell-v205.md`. No release
  gate, package, upload, activation, or live transition occurred.
- The next iteration is a fundamental coordinated forward-assault phase, not
  another shell distance/cost knob; details are in `docs/CURRENT_PLAN.md`.

### v203 route-preserving early forward cage rejected — 2026-08-18

- Replay review found that v202 losses often had 0–1 Barriers while
  high-ranking winners placed 7–20 around the confirmed enemy Core in rounds
  7–30, frequently before their first Sentinel. v203 removed the existing
  completed-route prerequisite from the attacker’s cage while retaining the
  dynamic one-Harvester reserve, six-site cap, escape-safe placement, and
  confirmed-Core requirement. Focused coverage was **28/28**, compileall
  passed, static retained only inherited failures, and smoke was **4/4**.
- The rotated seed-168 15-map screen was **6-9**, 15/15 command-clean with
  zero TLE/suspicious output, but introduced a candidate no-delivery
  Drakkarfjord row. Replay events confirmed real forward cages, with candidate
  Barrier totals reaching 4–12 on several maps; max p99/peak were
  **1496/5601 us** (`reports/local-20260818T134721Z`,
  `reports/iter-v203-forward-cage-replay-analysis.json`).
- The one permitted repair limited pre-route construction to three sites.
  Focused coverage was **29/29**, compileall passed, smoke was **4/4**, and
  static retained inherited exit 2. The identical screen stayed **6-9** and
  moved the no-delivery row to Royale; max p99/peak were **1666/4544 us**
  (`reports/local-20260818T134949Z`,
  `reports/iter-v203-forward-cage-repair-replay-analysis.json`).
- Reject v203 and roll back. Candidate Python is recursively identical to
  immutable v0042; rollback nearest-defense was **23/23**, compileall passed,
  static retained inherited exit 2, and rollback smoke was **4/4**
  (`reports/local-20260818T135203Z`). No release gate, package, upload,
  activation, or baseline transition occurred. Early Barrier topology alone
  is insufficient; the next hypothesis must couple pressure to live route
  health or use another workforce without starving delivery. Full record:
  `experiments/v0042-route-preserving-forward-cage-v203.md`.

### v202 cramped-map pressure exception rejected — 2026-08-18

- Replay/top-team evidence showed compact Core geometry needs immediate
  pressure, but winners also convert that pressure into an early route shell.
  v202 kept the primary attacker on v0042 offense on mirrored-Core distances
  within `CRAMPED_CORE_DIST` and retained the bounded v201 economy handoff on
  wider maps. Focused coverage was **27/27**, compileall passed, static kept
  only inherited failures, and smoke was **4/4**.
- The rotated seed-167 15-map screen was **9-6**, command-clean with zero TLE
  or suspicious output, but Royale (Core distance 14) had one Harvester and no
  candidate delivery (`reports/local-20260818T133357Z`,
  `reports/iter-v202-cramped-opening-replay-analysis.json`).
- The one permitted repair kept compact-map pressure through the early window,
  then handed the primary attacker to economy at round 24 when no completed
  route existed. Focused coverage was **28/28**, smoke **4/4**, compileall
  passed, and static retained the inherited exit 2. The identical screen
  removed the no-delivery row but fell to **5-10**; max p99/peak were
  **1300/2466 us** (`reports/local-20260818T133817Z`,
  `reports/iter-v202-cramped-opening-repair-replay-analysis.json`).
- Reject v202 and roll back. Candidate Python is recursively identical to
  immutable v0042; rollback nearest-defense was **23/23**, compileall passed,
  static retained inherited exit 2, and rollback smoke was **4/4**
  (`reports/local-20260818T134031Z`). No release gate, package, upload,
  activation, or baseline transition occurred. The next hypothesis must tie
  early route/Barrier conversion to live state rather than Core distance plus
  a fixed round fallback. Full record:
  `experiments/v0042-cramped-map-pressure-exception-v202.md`.

### v201 primary-attacker opening economy handoff rejected — 2026-08-18

- Replay evidence showed v200's primary attacker spent the opening on Launcher
  construction while top winners secured a fast route/Barrier shell first. v201
  temporarily lent only that primary attacker to the economic Builder FSM until
  one completed route or a bounded map-scaled deadline. Focused coverage was
  **4/4**, compileall passed, static retained only inherited failures, and
  smoke was **4/4**.
- A diagnostic old-seed-165 repeat was **7-8** with candidate first delivery
  **21.36**, but the planned rotated seed-166 screen was **5-10**, with first
  delivery **40.27** versus **27.73** for v0042. It was 15/15 command-clean
  with zero TLE/suspicious/no-delivery rows; max p99/peak **1521/2822 us**
  (`reports/local-20260818T132001Z`,
  `reports/iter-v201-primary-opening-replay-analysis-seed166.json`). Royale
  placed its first Harvester at round 248 and delivered at 324.
- The one bounded repair kept the primary in economy until two completed routes.
  Seed 166 improved to **6-9**, first delivery **26.93** versus **28.13**, but
  still failed the paired win gate and retained Harvester/Barrier stock gaps;
  max p99/peak **1514/4648 us** (`reports/local-20260818T132318Z`,
  `reports/iter-v201-primary-opening-replay-analysis-repair-seed166.json`).
- Reject v201 and roll back. Candidate Python is recursively identical to
  immutable v0042; rollback nearest-defense was **23/23**, compileall passed,
  static retained inherited exit 2, and rollback smoke was **4/4**
  (`reports/local-20260818T132539Z`). No release gate, package, upload,
  activation, or baseline transition occurred. The next hypothesis must target
  the remaining route-stock/Royale map-state failure without repeating the
  primary handoff or standalone Launcher relay.

### v200 primary-attacker Launcher relay rejected — 2026-08-18

- Implemented the replay-backed early mobility phase: only the designated
  primary attacker could build a reserve-gated Launcher relay, and each
  Launcher could throw that attacker to a legal passable tile making progress
  toward the enemy Core. Focused coverage was **27/27**, compileall passed,
  static retained only inherited failures, and smoke was **4/4**
  (`reports/local-20260818T125545Z`).
- The seed-165 15-map screen was **6-9** against exact v0042, 15/15
  command-clean with zero TLE/suspicious/no-delivery rows. Replay inspection
  confirmed real Launcher/launch events, but the candidate built three
  Launchers on every map, first delivery averaged about round 33, and it did
  not produce a win-rate edge (`reports/local-20260818T125715Z`,
  `reports/iter-v200-launcher-relay-replay-analysis.json`).
- The one permitted repair reduced the cap to one Launcher. Focused/compileall/
  static/smoke remained clean, but the screen fell to **5-10** with the same
  reliability floors (`reports/local-20260818T130242Z`,
  `reports/iter-v200-launcher-relay-repair-replay-analysis.json`).
- Reject v200 and roll back. Candidate source is recursively identical to
  immutable v0042; rollback nearest-defense coverage was **23/23**, compileall
  passed, static retained the same inherited exit 2, and rollback smoke was
  **4/4** (`reports/local-20260818T130820Z`). No release gate, package, upload,
  activation, or baseline transition occurred. Top-team evidence remains an
  early route shell first (fast delivery plus Harvester/Barrier stock), with
  Launcher mobility layered on afterward; the next hypothesis must address
  v200's opening delivery gap before another Launcher selector.

### v198 replay/top-team audit — hypothesis recorded — 2026-08-18

- Parsed the v197 initial and half-HP-repair losses, the saved live-v100 loss
  sample, and 15 high-ranking replays before editing candidate source. v197's
  first Harvester averaged rounds **16.3/17.2** versus v0042's **9.5/10.1**;
  its loss rows had roughly **5.6/5.9 Harvesters** versus **7.9/9.0** for the
  comparator and ended with materially less titanium. The direct raid,
  takeover, and support selectors are therefore closed.
- Top-team winners delivered by mean round **21.1**, averaged **5.0
  Harvesters**, **13.7 Barriers**, **3.3 Launchers**, and **3.6 Sentinels**;
  losers averaged **3.1 Harvesters**, **8.9 Barriers**, and **0.4 Launchers**.
  The winning replay pattern is an early route shell plus Launcher
  mobility/control, followed by Sentinel/Barrier pressure.
- Recorded one bounded v198 hypothesis in
  `experiments/v0042-replay-top-team-audit-v198.md`: after three completed
  routes, one confirmed forward Sentinel, confirmed enemy-Core intel, and a
  dynamic Launcher-plus-Harvester reserve, the designated primary attacker
  may build one forward Launcher to eject one adjacent enemy Builder farther
  from that Core. It never diverts our route workforce or inserts our own
  Builder. No candidate source has been changed yet; v0042 remains the exact
  baseline. Audit report: `reports/iter-v198-replay-audit.json`.

### v198 forward Launcher ejection rejected — 2026-08-18

- Implemented the recorded one-shot forward enemy-Builder ejection mechanic.
  Focused coverage was **26/26**, compileall passed, static retained only the
  inherited failures, and smoke was **4/4**. The first seed-162 screen was
  **11-4**, but its only Launcher appeared at the end of a Royale replay and
  never ejected a Builder (`reports/local-20260818T122934Z`).
- The independent seed-163 all-map screen was **7-8**, with no TLE,
  suspicious-output, or no-delivery rows; its only Launcher likewise appeared
  at the end of an Archipelago replay and produced no ejection
  (`reports/local-20260818T123246Z`). Max p99/peak were **1385/2384 us**.
- Reject v198: the apparent first-screen edge was non-causal and did not
  repeat. The temporary `main.py`/`attacker.py`/focused test changes are being
  removed; no release gate, package, upload, activation, or baseline change is
  justified. Full record: `experiments/v0042-replay-top-team-audit-v198.md`.

### Next v199 direction — failure-adaptive liquidity phase

- The v197 and v198 replay evidence points to a conditional failure mode, not
  a missing late target: v0042 losses sometimes spend repeated forward
  Sentinels while current titanium falls below a replacement Harvester and
  short-route reserve. The approved v199 hypothesis is a narrow circuit
  breaker after **two observed short-lived Sentinel deaths**; it blocks only
  another replacement while dynamic prices say the route reserve is missing,
  then resumes automatically after recovery. It does not change the first
  Sentinel, healthy pressure, or any Launcher behavior.
- Source remains exact v0042 parity until the v199 hypothesis is implemented;
  no release gate or platform operation is authorized for rejected v198.

### v195 enemy-resource hijack rejected — 2026-08-18

- Tested a late, reserve-funded hijack transition against the exact v0042
  baseline. The initial ownership-aware orphan-only version passed focused
  **27/27**, compileall, smoke **4/4**, and scored **6-9** on the seed-162
  all-map screen with one A-side no-delivery row (`reports/local-20260818T112546Z`).
- The one bounded repair allowed a parallel accepting Conveyor beside an
  enemy-connected Harvester, while rejecting any source already drained by our
  belt. Focused coverage was **31/31**, smoke **4/4**, static retained only
  inherited failures, and the screen improved to **7-8** with zero A-side
  no-delivery/TLE/suspicious rows; max p99 was **1496 us**
  (`reports/local-20260818T113100Z`).
- Reject: v0042 still won the paired screen **8-7**. Candidate source was
  restored recursively identical to immutable v0042. No 60-game gate, package,
  upload, activation, or baseline transition occurred. Full record:
  `experiments/v0042-enemy-resource-hijack-v195.md`.

### v196 sabotage-then-takeover rejected — 2026-08-18

- Tested a late, reserve-funded fixed-attacker transition that selected a
  visible enemy-fed Conveyor, legally fired on it until the tile was empty,
  and then attempted to seed a Core-facing accepting Conveyor. Focused
  coverage was **30/30**, compileall passed, smoke was **4/4**, and static
  retained only the inherited failures. The seed-162 all-map screen was
  **7-8**, 15/15 command-clean, with zero candidate no-delivery/TLE/suspicious
  rows and max p99 **1413 us** (`reports/local-20260818T114458Z`).
- One bounded repair gave reclaim priority over the optional Core cage barrier.
  Focused coverage was **32/32**, compileall passed, smoke was **4/4**, and
  the screen remained **7-8** with zero candidate no-delivery/TLE/suspicious
  rows and max p99 **1319 us** (`reports/local-20260818T114931Z`).
- Reject: neither destroy-then-reclaim nor its priority repair beat v0042.
  Candidate source was restored recursively identical to immutable v0042;
  rollback focused tests were **27/27**, compileall passed, and smoke was
  **4/4** (`reports/local-20260818T115418Z`). No 60-game gate, package,
  upload, activation, or baseline transition occurred. Full record:
  `experiments/v0042-sabotage-then-takeover-v196.md`.

### v197 forward-support handoff rejected — 2026-08-18

- Tested one map-aware, reserve-gated dynamic-worker handoff: after confirmed
  enemy-Core intel, three completed routes, and a live forward Sentinel, the
  nearest dynamic Builder could walk to and heal a damaged friendly forward
  Sentinel or Core-side Barrier. Focused coverage was **33/33**, compileall
  passed, smoke was **4/4**, and static retained only inherited failures. The
  seed-162 screen was **6-9**, 15/15 command-clean, zero TLE/suspicious rows,
  max p99/peak **1415/3103 us** (`reports/local-20260818T120418Z`).
- One bounded repair required at least half HP damage before dispatching the
  worker, avoiding light-chip detours. Focused coverage stayed **33/33**,
  compileall/static/smoke stayed clean, but the screen fell to **5-10** with
  zero TLE/suspicious rows and max p99/peak **1382/3052 us**
  (`reports/local-20260818T120705Z`).
- Reject: forward repair did not beat v0042. Candidate source was restored
  recursively identical; rollback focused tests were **27/27**, compileall
  passed, and rollback smoke was **4/4** (`reports/local-20260818T121003Z`).
  No 60-game gate, package, upload, activation, or baseline transition
  occurred. Full record: `experiments/v0042-forward-support-handoff-v197.md`.

### Next direction — new mechanic/phase review

- The local offence/sabotage/support branch is closed after v195 parallel
  outlet, v196 destroy/reclaim, and v197 forward-repair variants all failed to
  beat v0042. Inspect the v197 losses and current rules before selecting a
  fundamentally different map-context workforce/route phase hypothesis or a
  carefully isolated unit-control experiment; do not add another steal,
  repair, or barrier selector without new causal evidence.

### v194 late-game offensive staging rejected — 2026-08-18

- Tested a bounded forward-frontier lifecycle: with a full six-site enemy-Core
  Barrier cage, an attacker could destroy one visible adjacent obsolete site
  and immediately build a legal replacement at least two distance-squared
  points closer to the confirmed Core. Rotation required a live forward
  Sentinel, three completed routes, a preserved Harvester reserve, and a
  replacement preflight; the original cage cap and opening economy were
  unchanged.
- Initial focused coverage was **40/40**, repair **41/41**, rollback **38/38**;
  compileall passed and smoke was **4/4** throughout. `make static` retained
  only inherited failures. Seed-162 screens were **6-9** with
  **51,350/64,890 Ti** and one candidate no-delivery row, then **6-9** with
  **81,650/87,800 Ti** and no candidate no-delivery row. Both were 15/15
  command-clean with zero TLE/suspicious-output rows.
- Reject after the bounded repair. Temporary attacker/constant/tests were
  removed and candidate source is recursively identical to immutable v0042.
  Full record: `experiments/v0042-late-game-offensive-staging-v194.md`; reports
  are under `reports/iter-v194-offense-staging/`. No release, package, upload,
  activation, or baseline transition occurred.

### v193 gate follow-up — exact 9-6 repair rejected at 60 games

- The exact v193 repair source was reconstructed only for the requested full
  matrix. The 60-game endpoint-seed gate was **29-31**, candidate/comparator
  titanium **291,120/322,530**, with 60/60 command-clean games and no
  no-delivery rows (`reports/local-20260818T110738Z`). Weak 1-3 floors occurred
  on Auroraveil, Fjordgate, Frostgate, Midgard, and Nordkap.
- The temporary spawn helper was removed again; candidate parity with immutable
  v0042 is exact. No promotion or platform transition occurred.

### v193 confirmed-enemy spawn ordering rejected — 2026-08-18

- Tested role-aware ordering of the Core spawn ring only when an enemy Core was
  directly visible: fixed attackers favored the outward lane and the permanent
  defender favored the home side. With no confirmed geometry, the prior
  shuffled opening was preserved. Economy, routes, combat, workforce,
  navigation, and live state were unchanged.
- Focused coverage was **42/42**, compileall passed, smoke was **4/4**, and
  `make static` retained only inherited missing legacy modules and two
  navigation fast-path assertions. The seed-161 initial screen was **6-9**
  (**62,680/89,480 Ti**); repair 1 was **8-7** (**85,120/78,390 Ti**, one
  candidate zero-delivery row); the same-schedule repeat was **9-6**
  (**74,060/82,360 Ti**). All 45 games were command-clean and replay analysis
  found no TLE or suspicious-output rows.
- Reject after one bounded repair plus a repeat and the requested 60-game gate:
  the direct-enemy case is rare, the apparent edge was not stable, and the
  full matrix was 29-31 with weak map floors. Temporary helper/tests were
  removed; candidate source is recursively identical to immutable v0042.
  Reports and rollback logs are under `reports/iter-v193-deterministic-spawn/`;
  full record: `experiments/v0042-deterministic-spawn-order-v193.md`. No
  release, package, upload, activation, or baseline transition occurred.

### Next direction — enemy-resource hijacking

- The next isolated experiment will verify ownership, direction, and Core sink
  before seeding or repairing a Conveyor path to a visible enemy Harvester, or
  overtaking a severed enemy route. It must preserve Harvester, replacement,
  and home-defense reserves and remain separate from the rejected v194 cage
  rotation.

### v192 map-aware chain slack rejected — 2026-08-18

- Tested a bounded route-initialization change: larger boards received at most
  one additional chain-slack block so wall/chokepoint detours would not end a
  legitimate Harvester route early. Navigation, route facing, ore ranking,
  workforce, combat, baseline, package, and live behavior were unchanged. The
  quick screen stayed at its map-complete minimum of **15 games**; the release
  gate stayed **60**.
- Focused related coverage was **41/41** for the initial and repaired
  variants, rollback coverage was **38/38**, compileall passed, smoke was
  **4/4**, and static retained only inherited missing legacy modules plus two
  navigation fast-path assertions. Replay analysis found zero TLE or
  suspicious-output rows; max p99/peak was **1391/2812 us** initially and
  **1301/2767 us** after repair.
- Seed-160 initial screen: **5-10**, candidate/comparator Ti
  **84,590/100,040** (`reports/local-20260818T102648Z`). The single bounded
  repair halved the large-map cap and scored **6-9**, Ti
  **80,480/89,600** (`reports/local-20260818T102941Z`). Both screens were
  15/15 command-clean.
- Reject after one bounded repair without a 60-game gate. Temporary source and
  test edits were removed; candidate parity with immutable v0042 is exact.
  Rollback logs are under `reports/iter-v192-chain-slack/`; full record:
  `experiments/v0042-map-aware-chain-slack-v192.md`. No release, package,
  upload, activation, or baseline transition occurred.

### v191 opening ore conversion score rejected — 2026-08-18

- Tested a bounded map-context opening change: during the first three completed
  routes, visible and advertised ore was ranked by Builder approach plus Core
  distance with a small visible-access penalty; mature targeting remained the
  nearest-source policy. No chain, workforce, combat, Launcher, barrier,
  Store, baseline, or live code changed. The quick screen stayed at its
  minimum 15 games (one per configured map); the release gate stayed 60.
- Focused related coverage was **35/35** for both attempts, compileall passed,
  smoke was **4/4**, and static retained only the inherited missing legacy
  modules plus two navigation fast-path assertions.
- Initial seed-159 screen: **7-8**, candidate/comparator Ti **75,380/80,290**
  (0.9388x), one candidate no-delivery game, and zero command/TLE/suspicious
  output failures (`reports/local-20260818T101340Z`). Repair 1 reduced the
  route/access weights but remained **7-8**, with Ti **79,190/69,720** and
  command-clean replays (`reports/local-20260818T101626Z`).
- Reject after the bounded repair without a 60-game gate. Temporary defender
  and test edits were removed; candidate parity with immutable v0042 is exact.
  Rollback logs: `reports/iter-v191-opening-ore-score/rollback-*`; experiment
  record: `experiments/v0042-opening-ore-conversion-score-v191.md`. No package,
  upload, activation, or baseline transition occurred.

### v190 late no-delivery harvest-range recovery rejected — 2026-08-18

- Tested a map-size-aware recovery from the early ore-radius cap only when no
  completed Harvester route existed by round 80. Repair 1 additionally required
  the bank to fund an estimated Harvester-plus-conveyor route and one
  replacement Harvester. Focused checks were **31/31**, compileall passed,
  smoke was **4/4**, and static retained only inherited failures.
- Initial seed-158 screen was **6-9**; repair 1 recovered it to **8-7**. The
  independent seed-159 rotation reversed to **7-8**. All 45 games were
  command-clean with no TLE or suspicious-output records. Reports:
  `reports/local-20260818T095623Z`, `reports/local-20260818T095905Z`, and
  `reports/local-20260818T100048Z`; replay analysis is under
  `reports/iter-v190-harvest-recovery/`.
- Reject after one bounded repair. Temporary constants/defender/test changes
  were removed; candidate source is recursively identical to immutable v0042.
  Rollback focused checks passed, compileall passed, static remained inherited
  red, and rollback smoke was **4/4** (`reports/iter-v190-harvest-recovery/rollback-*`).
  No release, package, remote gate, upload, activation, or baseline transition
  occurred. Full record: `experiments/v0042-late-harvest-range-recovery-v190.md`.

### v189 failed-attacker-navigation fallback rejected — 2026-08-18

- Tested a control-flow change where a fixed attacker that could not advance
  toward the enemy Core under the current danger map fell through to its
  existing heal/sabotage/reposition fallback instead of returning a ready
  turn idle. Direct navigation, economy, Sentinel, barrier, and workforce
  behavior were unchanged. Focused coverage was **8/8**, compileall passed,
  smoke was **4/4**, and static retained only the inherited failures.
- Seed-157's 15-game all-map screen was **8-7**, command-clean, with no TLE or
  suspicious output (`reports/local-20260818T094342Z`; replay analysis in
  `reports/iter-v189-attacker-navigation/replay-analysis.json`). The rotated
  seed-158 screen reversed to **7-8**, also 15/15 command-clean
  (`reports/local-20260818T094537Z`; analysis in
  `reports/iter-v189-attacker-navigation/replay-analysis-rotated.json`).
- Reject without a release gate. Temporary attacker/test changes were removed;
  candidate source is recursively identical to immutable v0042. Rollback
  focused checks passed, compileall passed, static remained inherited red, and
  rollback smoke was **4/4** (`reports/iter-v189-attacker-navigation/rollback-*`).
  No release, package, remote gate, upload, activation, or baseline transition
  occurred. Full record: `experiments/v0042-attacker-navigation-fallback-v189.md`.

### v188 delayed mirrored-Sentinel fallback rejected — 2026-08-18

- Tested a fixed-attacker-only fallback that could place one Sentinel at the
  symmetric enemy-Core estimate after round 20, three completed routes, and a
  dynamic 110-Ti Sentinel-plus-attack reserve. Focused checks were **25/25**,
  compileall passed, smoke was **4/4**, and static retained the inherited
  failures.
- The seed-157 15-game all-map screen was **4-11**, command-clean, with
  **53,060/89,570 Ti** collected. Replay analysis showed no TLE or suspicious
  output and confirmed early-economy displacement on several losses:
  `reports/local-20260818T093130Z` and
  `reports/iter-v188-mirrored-sentinel/replay-analysis.json`.
- Reject without repair. Temporary attacker/test changes were removed;
  candidate `attacker.py` is byte-identical to v0042. Rollback focused checks
  were **28/28**, compileall passed, static remained inherited red, and
  rollback smoke was **4/4** (`reports/iter-v188-mirrored-sentinel/rollback-*`,
  `reports/local-20260818T093406Z`). No release, package, remote gate, upload,
  activation, or baseline transition occurred.

### v187 fixed-defender pressure handoff rejected — 2026-08-18

- Tested releasing only the permanent economy defender after five completed
  routes, when no ore, home threat, active chain, or home-Gunner assignment
  remained. Focused checks were **26/26**, compileall passed, smoke was **4/4**,
  and static retained the inherited 15 obsolete-module imports plus two
  navigation assertions.
- Seed-154's 15-game all-map screen was **10-5**, command-clean, with
  **69,160/72,000 Ti** collected; the independent seed-155 rotation reversed
  to **7-8** with **58,380/68,220 Ti**. Reports:
  `reports/local-20260818T091314Z` and `reports/local-20260818T091550Z`.
- Repair 1 required a dynamic 400-Ti-class bank before handoff. Focused,
  compileall, and smoke checks stayed clean, but seed 156 fell to **5-10**
  with **50,660/66,180 Ti** (`reports/local-20260818T091925Z`).
- Reject after one bounded repair. Temporary source/test changes were removed;
  candidate `main.py` is byte-identical to v0042. Rollback focused checks were
  **28/28**, compileall passed, static remained inherited red, and rollback
  smoke was **4/4** (`reports/iter-v187-defender-pressure/rollback-*`,
  `reports/local-20260818T092129Z`). No release, package, remote gate, upload,
  activation, or baseline transition occurred.

### v182 home-economy scout rejected after tied release and two repairs — 2026-08-18

- Tested a deterministic nearest home-side dynamic Builder that stayed in the
  harvest/exploration loop after the three-route milestone. Focused checks
  were **22/22**, compileall and smoke **4/4** passed; the 18-game all-map
  screen scored **12-6**, collection **64,180 vs 67,110** (0.9563x), with
  zero candidate no-delivery rows and mean placed Harvesters **8.00 vs 7.28**
  (`reports/local-20260818T064845Z`; analysis
  `reports/iter-v182-home-economy-scout-replay-analysis.json`).
- The required 60-game release gate was command-clean but tied **30-30**,
  collection **321,370 vs 316,160** (1.0165x), with one candidate no-delivery
  row and weak floors on Glacierkeep **0-4**, Icefloe **0-4**, Nordkap **1-3**,
  and Frostgate **1-3** (`reports/local-20260818T065043Z`; analysis
  `reports/iter-v182-home-economy-scout-release60-replay-analysis.json`).
- Repair 1 disabled the scout on cramped maps. Focused **23/23**, compileall,
  and smoke **4/4** passed, but the screen fell to **8-10**, collection
  **72,430 vs 73,540** (0.9849x), with one candidate no-delivery row
  (`reports/local-20260818T065835Z`; analysis
  `reports/iter-v182-home-economy-scout-repair1-replay-analysis.json`).
- Repair 2 retained the scout only below three visible home Harvesters.
  Focused **24/24**, compileall, and smoke **4/4** passed; the screen stayed
  **8-10**, collection **72,680 vs 78,210** (0.9293x), with no candidate
  no-delivery rows (`reports/local-20260818T070148Z`; analysis
  `reports/iter-v182-home-economy-scout-repair2-replay-analysis.json`).
- v182 is **rejected**. The temporary logic/tests were removed; recursive
  candidate-v0040 parity is **0 diff lines**, rollback focused checks passed
  **20/20**, compileall passed, and rollback smoke was **4/4**
  (`reports/iter-v182-rollback-source-diff.txt`,
  `reports/local-20260818T070441Z`; record
  `experiments/v0040-home-economy-scout-v182.md`). No remote gate, package,
  upload, activation, or baseline transition occurred.

### v181 verified conveyor-route join rejected after two repairs — 2026-08-18

- Tested a bounded route-conversion optimization: a Harvester chain could join
  a visible friendly Conveyor path only when forward inspection proved that
  path reached our Core. Focused checks were **22/22**, compileall passed, and
  smoke was **4/4**, but the 18-game all-map screen regressed to **8-10**,
  collection **66,030 vs 80,180** (0.8235x), with one candidate no-delivery
  row (`reports/local-20260818T063536Z`; analysis
  `reports/iter-v181-verified-route-join-replay-analysis.json`).
- Repair 1 kept direct routing until three completed routes. Focused checks
  were **23/23**, compileall and smoke **4/4** passed; the screen remained
  **8-10**, collection **83,570 vs 81,340** (1.0274x), with one candidate
  no-delivery row (`reports/local-20260818T063857Z`; analysis
  `reports/iter-v181-verified-route-join-repair1-replay-analysis.json`).
- Repair 2 limited joins to four verified conveyor hops. Focused checks stayed
  **23/23**, compileall and smoke **4/4** passed, but the screen fell to
  **7-11**, collection **64,060 vs 70,110** (0.9137x), again with one
  candidate no-delivery row (`reports/local-20260818T064129Z`; analysis
  `reports/iter-v181-verified-route-join-repair2-replay-analysis.json`).
- v181 is **rejected**. The temporary helper/tests were removed; recursive
  candidate-v0040 parity is **0 diff lines**, rollback focused checks passed
  **20/20**, compileall passed, and rollback smoke was **4/4**
  (`reports/iter-v181-rollback-source-diff.txt`,
  `reports/iter-v181-rollback-focused.log`,
  `reports/local-20260818T064408Z`; record
  `experiments/v0040-verified-route-join-v181.md`). No release, remote,
  package, upload, activation, or baseline transition occurred.

### v180 home-local Harvester recovery rejected after release reversal — 2026-08-18

- Tested whether a home-local dynamic Builder should rebuild the economy when
  the lifetime `SLOT_HARVESTER_COUNT` threshold had been reached but fewer
  than two friendly Harvesters remained visible. The initial variant passed
  focused **21/21**, compileall, and smoke **4/4**; its 21-game all-map screen
  was **11-10**, collection **86,710 vs 87,920** (0.9862x), with no-delivery
  **0/0** (`reports/local-20260818T060909Z`).
- Repair 1 widened the visible floor to two Harvesters. Focused checks stayed
  **21/21**, smoke **4/4**, and the screen became **11-10**, collection
  **132,130 vs 128,210** (1.0306x), no-delivery **0/1**
  (`reports/local-20260818T061232Z`). The required 60-game release gate then
  reversed to **28-32**, collection **266,200 vs 294,540** (0.9038x),
  no-delivery **0/1**, max p99/peak **1,596/5,060 us**
  (`reports/local-20260818T061518Z`).
- Repair 2 added a low-resource guard so recovery only triggers below two
  Harvester costs. Focused checks remained **21/21**, compileall passed, smoke
  **4/4**, but the screen was only **10-11**, collection **95,280 vs 95,260**
  (1.0002x), no-delivery **0/0** (`reports/local-20260818T062254Z`).
- v180 is **rejected** after the release reversal and two bounded repairs. The
  temporary source and test changes were removed; recursive candidate-v0040
  parity is **0 diff lines**, rollback focused checks passed **20/20**,
  compileall passed, and rollback smoke was **4/4**
  (`reports/iter-v180-rollback-source-diff.txt`,
  `reports/iter-v180-rollback-focused.log`,
  `reports/local-20260818T062740Z`; record
  `experiments/v0040-home-harvester-recovery-v180.md`). No remote gate,
  package, upload, activation, or baseline transition occurred.

### Evaluation screen trimmed to 18 all-map games — 2026-08-18

- The routine fast screen now runs **18 games**: one primary game on each of
  the 15 configured maps plus three deterministic side-order repeats. This
  reduces iteration time modestly while retaining complete map coverage and
  side-order sampling. The release gate remains the unchanged **60-game**,
  two-endpoint-seed, both-side matrix.

### v179 pre-route Core-ring deferral rejected after release reversal — 2026-08-18

- Tested deferring opportunistic Core-ring maintenance before the first
  completed route so early Builder actions could convert Harvesters. The
  initial variant also deferred dynamic ring-gap claims; focused checks were
  **21/21**, compileall passed, smoke **4/4**, and the 21-game screen fell to
  **7-14**, collection **79,270 vs 88,410** (0.8966x), with one candidate
  no-delivery row and **136 vs 187** placed Harvesters
  (`reports/local-20260818T054730Z`).
- Repair 1 restored dynamic ring-gap claims while keeping only the defender
  opportunistic deferral. Focused checks stayed **21/21**, smoke **4/4**, and
  the screen improved to **12-9**, collection **104,890 vs 99,730** (1.0517x),
  with zero no-delivery rows (`reports/local-20260818T055026Z`). Its 60-game
  release matrix was **32-28**, collection **268,070 vs 264,930** (1.0119x),
  but had **2/0** candidate/comparator no-delivery rows and weak protected-map
  floors; max p99/peak was **1,496/5,849 us**
  (`reports/local-20260818T055306Z`).
- Repair 2 enabled the deferral only on larger maps, retaining immediate ring
  maintenance on cramped maps. Focused checks remained **21/21**, compileall
  passed, smoke **4/4**, but the screen fell to **6-15**, collection
  **68,200 vs 91,450** (0.7458x), with one candidate no-delivery row
  (`reports/local-20260818T060050Z`).
- v179 is **rejected** after the release reversal and two bounded screens. The
  temporary changes were removed; recursive candidate-v0040 parity is **0
  diff lines**, rollback focused checks passed **20/20**, compileall passed,
  and rollback smoke was **4/4** (`reports/local-20260818T060334Z`, record
  `experiments/v0040-pre-route-ring-deferral-v179.md`). No remote gate,
  package, upload, activation, or baseline transition occurred.

### v178 reactive home-Builder blocker rejected after two repairs — 2026-08-18

- Tested a bounded response for the concrete idle case where `_find_home_threat`
  selects an enemy Builder that a friendly Builder cannot legally fire at.
  The initial variant placed at most two reserve-gated home Barriers per
  responder; it passed focused **22/22**, compileall, and smoke **4/4**, but the
  21-game all-map screen fell to **7-14**, collection **84,480 vs 108,260**
  (0.7803x), with zero command/no-delivery failures (`reports/local-20260818T052427Z`).
- A baseline-vs-itself control on the same schedule was **11-10** and
  **105,260 vs 111,360** titanium (`reports/local-20260818T053049Z`), confirming
  the regression was real. Repair 1 narrowed the blocker to one site at the
  Core perimeter; focused checks stayed **22/22**, smoke **4/4**, and the
  screen reached **10-11** with **71,610 vs 82,720** titanium
  (`reports/local-20260818T053410Z`).
- Repair 2 removed paid Barrier construction and kept only a movement handoff
  at the Core perimeter. Focused checks stayed **22/22**, compileall and smoke
  **4/4** passed, and the screen was **11-10**, **100,300 vs 97,560** titanium,
  max p99/peak **1,320/2,625 us** (`reports/local-20260818T053722Z`). This only
  matched the control and was not a material improvement.
- v178 is **rejected** after both bounded repairs. The temporary logic/tests
  were removed; recursive candidate-v0040 source parity is **0 diff lines**,
  rollback focused checks passed **20/20**, compileall passed, and rollback
  smoke was **4/4** (`reports/local-20260818T054043Z`, record
  `experiments/v0040-home-builder-blocker-v178.md`). No 60-game release,
  remote gate, package, upload, activation, or baseline transition occurred.

### v177 enemy-logistics breadcrumb scout rejected at the 21-game screen — 2026-08-18

- Tested a movement-only Core-confirmation scout for the fixed attacker. When
  a visible enemy logistics tile was closer than the 180-degree mirror guess,
  the attacker approached it without firing, building, or changing route,
  workforce, Sentinel, or Store policy.
- Initial v177 passed focused checks **22/22**, compileall, and smoke **4/4**;
  static retained only the inherited 15 obsolete-import errors and two
  navigation assertions. The 21-game all-map screen regressed to **9-12**,
  collection **89,170 vs 98,320**, with zero no-delivery rows
  (`reports/local-20260818T051245Z`).
- Repair 1 restricted the breadcrumb to visible enemy Harvesters and added a
  belt-only negative test. Focused checks were **23/23**, compileall passed,
  smoke was **4/4**, and the screen reached **10-11**, collection
  **107,350 vs 119,980**, with zero candidate no-delivery rows versus one for
  v0040 (`reports/local-20260818T051621Z`).
- v177 is **rejected** after both bounded screens: the movement-only scout did
  not create a material paired win edge or collection improvement. Source and
  tests were rolled back; candidate recursive source parity with v0040 is
  **0 diff lines**, rollback focused checks passed **20/20**, compileall
  passed, and rollback smoke was **4/4** (`reports/local-20260818T051939Z`
  and `experiments/v0040-logistics-breadcrumb-v177.md`). No 60-game release,
  remote gate, package, upload, activation, or baseline transition occurred.

### v176 pre-confirmation loaded-logistics raid rejected at the 60-game gate — 2026-08-18

- Tested one bounded early sabotage pulse for the fixed attacker: before enemy
  Core confirmation, a surplus attacker could fire at a visible loaded
  Conveyor/Splitter, then resume the direct lane. The initial variant also
  accepted Harvesters; it changed no route, workforce, Store, Sentinel, or
  economy-handoff policy.
- Initial focused checks were **22/22**, compileall passed, smoke was **4/4**,
  and static retained only the inherited 15 obsolete-import errors and two
  navigation assertions. The 21-game all-map screen regressed to **5-16**,
  with one candidate no-delivery row and collection **56,780 vs 92,220**
  (`reports/local-20260818T045041Z`).
- Repair 1 restricted the pulse to loaded Conveyor/Splitter tiles and added a
  Harvester-skip test. Focused checks were **23/23**, compileall passed, smoke
  was **4/4**, and the screen recovered to **12-9** with zero no-delivery rows;
  collection was **127,260 vs 122,410** (`reports/local-20260818T045415Z`).
- The required 60-game release gate regressed to **29-31**, collection
  **274,290 vs 317,820** (ratio **0.863**), and one candidate no-delivery row.
  All 60 commands were clean with zero TLE/suspicious-output rows; max
  p99/peak was **1,503/4,723 us** (`reports/local-20260818T045802Z`).
- v176 is **rejected**. Both source and tests were rolled back; candidate
  recursive source parity with v0040 is **0 diff lines**, rollback focused
  checks passed **20/20**, compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260818T050521Z` and
  `experiments/v0040-preconfirmation-raid-v176.md`). No release, remote,
  package, upload, activation, or baseline transition occurred.

### v175 temporary second-wave economy anchor rejected at the 21-game screen — 2026-08-18

- Tested a single designated stage-2 Builder kept on route work while the
  economy grew, then released into the dynamic pool. The change was motivated
  by v174's server losses showing fewer Harvesters/resources, but it did not
  alter route geometry or global liquidity policy.
- Initial v175 passed focused checks **21/21**, compileall, and smoke **4/4**;
  `make static` retained only the inherited 15 obsolete-import errors and two
  navigation fast-path assertions. The 21-game all-map screen regressed to
  **8-13**, with zero no-delivery rows, collection **124,840 vs 144,500**, and
  max p99/peak **1,445/5,190 us** (`reports/local-20260818T043505Z` and
  `reports/iter-v175-economy-anchor-screen-replay-analysis.json`).
- Repair 1 released the anchor after three routes. Focused checks stayed
  **21/21**, compileall passed, smoke was **4/4**, and the screen fell to
  **7-14** with one candidate no-delivery row; collection was
  **120,390 vs 146,750** (`reports/local-20260818T043909Z` and
  `reports/iter-v175-economy-anchor-repair1-screen-replay-analysis.json`).
- v175 is **rejected** after both bounded attempts. Candidate source is exact
  recursive v0040 parity (**0 diff lines**); rollback focused checks passed
  **20/20**, compileall passed, rollback smoke was **4/4**, and no release,
  remote, package, upload, activation, or baseline transition occurred.
  Rollback evidence is under `reports/iter-v175-economy-anchor-*` and the
  experiment record is `experiments/v0040-economy-anchor-v175.md`.

### v174 blocked-attack economy rejoin rejected at the remote gate — 2026-08-18

- Tested a structural, one-time handoff for a fixed attacker that repeatedly
  received no legal step toward an unconfirmed enemy Core: after round 80 and
  eight stalled navigation turns it could rejoin the existing economy loop,
  then resume direct pressure. The initial 21-game screen was **12-9**; the
  bounded pre-route repair reached **13-8** with no candidate no-delivery rows.
  Focused checks were **23/23**, compileall passed, smoke was **4/4**, and
  static retained only the inherited failures.
- The repair passed the 60-game all-map local gate **34-26** versus v0040,
  with zero no-delivery rows on either side, zero TLE/suspicious-output/
  command failures, and max p99/peak **1,534/2,608 us**
  (`reports/local-20260818T041313Z`).
- The server gate then completed **1-4** for the candidate on sprint, bridge,
  crossfire, vault, and aurora (match `d766ba27-6560-4434-a9eb-15a74fe33279`).
  Remote replays show a portable workforce/resource deficit on the four losses;
  evidence is under `reports/remote-20260818T041945Z` and
  `reports/iter-v174-blocked-attack-rejoin-remote-replay-analysis.json`.
- v174 is **rejected**. All temporary source and test edits were removed;
  candidate is exact recursive v0040 parity (**0 diff lines**). Rollback
  focused checks passed **20/20**, compileall passed, rollback smoke was
  **4/4**, and no package, upload, activation, or baseline transition occurred.

### v173 quiet-defense retirement rejected at the 60-game gate — 2026-08-18

- Tested the bounded unit-lifecycle strategy requested for late-game reuse:
  after five routes, three intact home Gunners, a rich bank, and 80 quiet
  rounds on a non-cramped map, one Core-marked Builder could destroy the
  farthest home Gunner and unlock one late Builder. Focused checks were
  **23/23**, compileall passed, smoke was **4/4**, and static retained only
  inherited failures.
- The 21-game all-map screen was a material **15-6**, with resources
  **3,953 vs 2,685**, living Harvesters **7.29 vs 6.29**, and zero candidate
  no-delivery rows (`reports/local-20260818T033838Z`). The required 60-game
  release gate then tied **30-30**; resources were **4,464 vs 4,435** and each
  side had one no-delivery row (`reports/local-20260818T034101Z`).
- Repair 1 canceled a pending retirement when a new home threat appeared; its
  screen fell to **9-12** with Harvesters **5.95 vs 8.19**. v173 is rejected,
  all lifecycle code/tests were removed, and candidate source restored exact
  recursive v0040 parity (**0 diff lines**). Rollback focused checks passed
  **20/20**, compileall passed, rollback smoke was **4/4**, and no release or
  platform operation occurred.

### v172 Core-ring sink merge rejected after two 21-game screens — 2026-08-18

- Tested a bounded route-continuity change: a pending chain link could finish
  into a visible friendly Conveyor only when that Conveyor's actual facing was
  verified directly into our Core. Arbitrary conveyor tails stayed rejected.
  Focused checks were **21/21**, compileall passed, smoke was **4/4**, and
  static retained only inherited failures.
- The initial screen was command-clean and **11-10** versus v0040, with first
  delivery **21.9 vs 29.6** and final resources **4,051 vs 3,556**; the one-win
  edge was not material (`reports/local-20260818T032223Z` and
  `reports/iter-v172-core-ring-sink-screen-replay-analysis.json`).
- Repair 1 restricted the merge to games with one completed route; it fell to
  **9-12** despite resources **5,069 vs 4,931** and first delivery **22.3 vs
  24.9** (`reports/local-20260818T032533Z`). v172 is rejected and both source
  and test changes were removed. Candidate restored exact recursive v0040
  parity (**0 diff lines**); rollback focused checks passed **20/20**,
  compileall passed, and rollback smoke was **4/4**. No release or platform
  operation occurred.

### v171 guarded idle-Harvester chain handoff rejected at the 21-game screen — 2026-08-18

- Tested one early-only repair to the idle fallback: below three completed
  routes, an adjacent-ore opportunity reused the normal Harvester-chain
  initializer; the shipped direct fallback remained unchanged at three or
  more routes. Focused checks were **21/21**, compileall passed, smoke was
  **4/4**, and static retained only the known inherited failures.
- The rotated 21-game all-map screen was command-clean but regressed to
  **9-12** versus v0040. Mean final resources were **3,170 vs 3,976** and
  living Harvesters **6.10 vs 7.57**; mean first delivery was **22.9 vs 23.4**.
  There were zero command, TLE, suspicious-output, or candidate no-delivery
  failures (`reports/local-20260818T031345Z` and
  `reports/iter-v171-guarded-idle-harvester-chain-screen-replay-analysis.json`).
- v171 is rejected without a repair or 60-game gate. The branch, import, and
  focused test were removed; candidate source restored exact recursive v0040
  parity (**0 diff lines**). Rollback focused checks passed **20/20**,
  compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260818T031703Z`). No release, package, remote match,
  upload, activation, or baseline transition occurred.

### v170 early route-site ranking rejected at the 21-game screen — 2026-08-18

- Tested map-context selection of the shortest Core-distance adjacent ore site
  during the first three routes, replacing only the fixed compass ordering.
  Focused checks were **21/21**, compileall passed, smoke was **4/4**, and
  static retained only inherited failures.
- The 21-game all-map screen was **11-10** versus v0040 with zero
  no-delivery/TLE/suspicious-output rows. Candidate mean Harvesters were
  **8.00 vs 8.43**, first delivery **29.5 vs 22.6**, and Sentinels **3.14 vs
  4.00**; max p99/peak was **1,415/5,395 us** (`reports/local-20260818T030353Z`
  and `reports/iter-v170-early-route-site-ranking-screen-replay-analysis.json`).
- v170 is rejected as a tie-level result; no repair or 60-game gate was run.
  The ranking and test were removed, candidate source restored exact recursive
  v0040 parity (**0 diff lines**), rollback focused checks passed **20/20**,
  compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260818T030659Z`). No release, remote, package, upload,
  activation, or baseline transition occurred.

### v169 staged workforce expansion rejected at the 21-game screen — 2026-08-18

- Tested raising only the post-route living-Builder target from 8 to 10 to
  address v0040 losses with 3–4 Harvesters against winners with 8–15. Focused
  checks were **21/21**, compileall passed, smoke was **4/4**, and static kept
  only the inherited 15 obsolete imports plus two navigation assertions.
- The initial unguarded expansion scored **7-14** on the 21-game all-map
  screen, with one candidate no-delivery game versus zero for v0040. Candidate
  mean Harvesters were **6.86 vs 9.48** and max p99/peak was **1,494/3,180
  us** (`reports/local-20260818T025040Z` and
  `reports/iter-v169-stage2-workforce-screen-replay-analysis.json`).
- Bounded repair 1 preserved the existing eight-Builder wave after route 1 and
  unlocked ten only after route 2. Focused checks remained **22/22**, smoke was
  **4/4**, and the screen recovered to **12-9**, but still had one candidate
  no-delivery game versus zero for v0040; mean Harvesters were **7.38 vs 8.05**
  (`reports/local-20260818T025446Z` and
  `reports/iter-v169-stage2-workforce-repair1-screen-replay-analysis.json`).
- v169 is rejected without a 60-game gate, remote test, package, upload,
  activation, or baseline transition. The staged target and tests were removed;
  candidate source restored exact recursive v0040 parity (**0 diff lines**).
  Rollback focused checks passed **20/20**, compileall passed, and rollback
  smoke was **4/4** (`reports/local-20260818T025809Z`).

### Routine quick screen reduced to 21 all-map games — 2026-08-18

- Reduced only the routine screen from **24 to 21 games**: one seeded
  candidate-A comparison on each of the 15 configured maps, plus six
  deterministic candidate-B side-order repeats selected from the same rotated
  `screen_seed`. Every map remains represented on every screen; side coverage
  continues to rotate across iterations.
- The complete **60-game** release gate (15 maps x endpoint seeds `1` and
  `101` x both sides) is unchanged. The optional **120-game** audit remains
  available for stochastic or tie-heavy candidates, and the historical 210-game
  matrix remains archival rather than routine.
- No bot source, immutable baseline, live state, package, upload, or activation
  changed. Schedule-focused validation and the first command-clean 21-game
  run are recorded in `reports/evaluation-policy-20260818-quick21.md`.

### v168 shared Core intel rejected at short screen — 2026-08-18

- Tested publishing visible enemy-Core sightings from Defender and Dynamic
  workers through the existing `SLOT_ENEMY_CORE` helper. Focused checks were
  **27/27**, compileall passed, smoke was command-clean, and static retained
  only the inherited 15 obsolete imports plus two navigation assertions.
- The unguarded hook was command-clean with zero TLE/suspicious-output rows and
  zero candidate no-delivery games, but the 24-game screen collapsed to **5-19**
  versus v0040. Candidate first delivery averaged **32.5 vs 25.7** turns,
  Harvesters **6.67 vs 8.25**, and Sentinels **2.54 vs 3.54**
  (`reports/local-20260818T022819Z` and
  `reports/iter-v168-shared-core-intel-screen-replay-analysis.json`). Early
  intel changed remote-ore/advance decisions before the economy was funded.
- Bounded repair 1 gated publication on three completed routes. Focused checks
  remained **27/27**, smoke was command-clean, and the screen recovered to
  **12-12** with zero candidate no-delivery games; first delivery was **24.9
  vs 42.1** and Sentinel counts **2.79 vs 2.75**
  (`reports/local-20260818T023212Z` and
  `reports/iter-v168-shared-core-intel-repair1-screen-replay-analysis.json`).
- v168 is rejected without a 60-game gate, release, package, upload,
  activation, or baseline transition. Both hooks and tests were rolled back to
  exact recursive v0040 parity (**0 diff lines**); rollback focused checks
  passed **25/25**, compileall passed, and rollback smoke was command-clean
  (`reports/local-20260818T023459Z`). Live v104 remains unchanged.

### v167 adaptive Sentinel pool rejected at short screen — 2026-08-18

- Tested a resource-backed intermediate Sentinel pool: after confirmed enemy
  Core intel and a Harvester-plus-Sentinel reserve, the attacker could build a
  second forward Sentinel before the existing five-chain three-Sentinel target.
  Focused checks were **28/28**, compileall passed, smoke was command-clean,
  and static retained only the inherited 15 obsolete imports plus two
  navigation assertions.
- The initial two-route variant tied v0040 **12-12** across the shortened
  24-game all-map screen. It had zero candidate no-delivery games, Sentinel
  placements **3.29 vs 3.04**, but first-delivery mean **45.1 vs 28.6**;
  replay evidence showed the extra turrets did not convert to wins
  (`reports/local-20260818T021330Z` and
  `reports/iter-v167-adaptive-sentinel-pool-screen-replay-analysis.json`).
- Bounded repair 1 lowered the intermediate route threshold from two to one.
  Focused checks remained **28/28**, smoke was command-clean, and the screen
  again tied **12-12** with zero candidate no-delivery games; first-delivery
  mean was **28.5 vs 25.0** and Sentinel placements **3.04 vs 3.88**
  (`reports/local-20260818T021713Z` and
  `reports/iter-v167-adaptive-sentinel-pool-repair1-screen-replay-analysis.json`).
- v167 is rejected without a 60-game gate, release, package, upload,
  activation, or baseline transition. The pool and tests were rolled back to
  exact recursive v0040 parity (**0 diff lines**); rollback focused checks
  passed **25/25**, compileall passed, and rollback smoke was command-clean
  (`reports/local-20260818T022030Z`). The next experiment must improve
  confirmed-Core timing or route workforce rather than another Sentinel-count
  ramp; live v104 remains unchanged.

### v166 chain danger recovery rejected at short screen — 2026-08-18

- Tested a bounded chain-FSM recovery for late first deliveries: after four
  consecutive no-progress turns under turret-line avoidance, a route made one
  emergency Core-directed navigation attempt without the danger set. Focused
  checks were **27/27**, compileall passed, static reproduced only the
  inherited failures, and smoke was **4/4** (`reports/local-20260818T015913Z`).
- The initial shortened 24-game all-map screen tied v0040 **12-12** with zero
  candidate no-delivery games and zero TLE/suspicious-output rows. Candidate
  mean first delivery improved to **24.1** turns versus **29.0** for v0040,
  but the win-rate tie did not qualify for release
  (`reports/local-20260818T015936Z`).
- Bounded repair 1 triggered the same single crossing after two stalled turns.
  Focused checks remained **27/27**, smoke was **4/4**
  (`reports/local-20260818T020255Z`), and the screen was **13-11** with zero
  candidate no-delivery/TLE/suspicious-output rows; mean first delivery was
  **30.8** versus **29.5** for v0040 (`reports/local-20260818T020318Z`).
- v166 is rejected without a 60-game release, remote gate, package, upload,
  activation, or baseline transition. The emergency branch was removed and
  source parity restored to v0040 (**0 diff lines**). Rollback focused checks
  passed **26/26**, compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260818T020635Z`). Live v104 remains unchanged.


### v165 opening workforce floor rejected at release gate — 2026-08-18

- Tested keeping non-designated Builders in the economy/Defender role until
  three completed routes, motivated by v164's remote replay deficit of only
  **1/4/6/4/5** Harvesters versus v0040's **5/7/9/4/7**. The initial focused
  checks were **27/27**, compileall passed, static reproduced the inherited 15
  obsolete imports plus two navigation assertions, and smoke was **4/4**.
- The initial shortened 24-game all-map screen scored **13-11** versus v0040;
  replay review found candidate-side zero-delivery losses on Royale and
  Drakkarfjord, so it did not advance.
- Bounded repair 1 kept the floor through two routes instead. Focused checks
  remained **27/27**, smoke was **4/4** (`reports/local-20260818T014310Z`),
  and the 24-game screen improved to **14-10** with zero candidate-side
  no-delivery games (`reports/local-20260818T014335Z`).
- The reduced 60-game release matrix then reversed to **26-34** against v0040.
  All 60 games were command-clean with zero TLE/suspicious-output rows; max
  replay p99/peak was **1,418/5,459 us** (`reports/local-20260818T014615Z`).
  No remote gate, package, upload, activation, or baseline transition was
  attempted.
- The role-floor change and its repair were rolled back to exact recursive
  v0040 parity (**0 diff lines**). Rollback focused checks were **26/26**,
  compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260818T015305Z`). The next experiment must target a
  different opening failure mode; live v104 remains unchanged.


### v164 idle Harvester chain handoff passes local release gate — 2026-08-18

- The idle fallback now reuses `_try_build_harvester`, so an adjacent-ore
  conversion initializes `MODE_CHAIN` and the normal route state instead of
  leaving a disconnected Harvester. The complete source diff is limited to
  that handoff; bot modules otherwise remain parity-clean with v0040.
- Focused checks passed **27/27**, compileall passed, smoke was **4/4**, and
  static retained only the inherited 15 obsolete imports plus two navigation
  assertions. The shortened 24-game screen scored **15-9** with candidate Ti
  **73,780** vs **50,260**, zero no-delivery rows, and max p99/peak
  **1,364/2,917 us** (`reports/local-20260818T011701Z`).
- The 60-game release matrix scored **39-21** against v0040, candidate Ti
  **167,950** vs **152,700**, one no-delivery row per side, zero command/TLE/
  suspicious-output rows, and max p99/peak **1,517/5,024 us**
  (`reports/local-20260818T011957Z`). v164 was only a provisional local edge;
- immutable archiving completed as v0041 (archive SHA-256
  `86571e966782e597eea98a1dcdd033459f71b8b25f5723970a3699961c87e9d4`).
- The guarded remote match `fc3d1bcf-38a3-4bd4-994d-ab9b98860b8a` then scored
  **1-4** for v164 against v0040 on sprint/bridge/crossfire/vault/aurora.
  Remote replay analysis showed the candidate placing only **1/4/6/4/5**
  Harvesters versus v0040's **5/7/9/4/7**. Evidence is under
  `reports/iter-v164-idle-harvester-chain-remote-replays/` and
  `reports/iter-v164-idle-harvester-chain-remote-replay-analysis.json`.
- v164 is rejected at the remote gate; v0041 remains an immutable rejected
  artifact. No upload, activation, or live-state change occurred. The next
  iteration returns to v0040 and targets the opening workforce floor.

### v163 dynamic economy pulse rejected after release reversal and bounded repair — 2026-08-18

- The staggered economy pulse initially failed the shortened all-map screen
  (**6-18**); repair 1 narrowed it to the exact three-route transition and
  improved the screen to **17-7**, but the reduced 60-game release gate
  reversed to **24-36** (`reports/local-20260818T005905Z`).
- Repair 2 added a low-liquidity check (bank below two current Harvester costs)
  before pulsing. Focused checks were **27/27**, compileall passed, smoke was
  **4/4**, and static retained only inherited failures. The 24-game screen was
  **12-12**, candidate Ti **68,060** versus comparator **36,170**, with zero
  command/TLE/suspicious-output failures (`reports/local-20260818T010720Z`).
- v163 is rejected after its two bounded repairs. Candidate source was restored
  to exact v0040 parity (**0 diff lines**), rollback focused checks were
  **26/26**, compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260818T011058Z`). No release re-run, promotion, package,
  upload, activation, or live-state change occurred. The next experiment must
  target a different failure mode than dynamic economy pulse timing.

### v163 dynamic economy pulse rejected at initial screen — 2026-08-18

- The first v163 variant added six-round, phase-spread economy leases for
  dynamic Builders between three and five completed routes. Focused tests were
  **21/21**, compileall passed, smoke **4/4**, and static retained inherited
  failures. The 24-game all-map screen scored **6-18** versus v0040 (candidate
  Ti **76,770** vs **93,330**, candidate no-delivery **0** vs comparator **1**;
  zero command/TLE/suspicious-output failures), report
  `reports/local-20260818T005258Z`.
- The pulse was too broad and is under one bounded repair: exactly three
  routes, 16-round phase spacing, three-round lease. No 60-game gate, baseline
  change, package, upload, activation, or live operation was attempted for the
  initial screen.
- Repair 1 passed **27/27** focused checks, compileall, and smoke **4/4**; the
  24-game screen improved to **17-7**, candidate Ti **105,870** vs **72,280**,
  candidate no-delivery **0** vs **1**, and zero command/TLE/suspicious-output
  failures (`reports/local-20260818T005605Z`). It advances to the reduced
  60-game release gate. That gate reversed to **24-36** (candidate Ti
  **250,630** vs **286,480**, no-delivery **1** vs **0**; zero TLE/suspicious
  output, max p99/peak **1,405/5,060 us**, `reports/local-20260818T005905Z`).
  Repair 2 adds a low-liquidity gate (bank below two current Harvester costs)
  as the final bounded v163 attempt; no promotion or platform operation yet.

### v162 primary-attacker economy handoff: initial screen tied — 2026-08-18

- The first v162 variant let only the primary fixed attacker join the existing
  Defender SCOUT/CHAIN loop from round 28 while zero routes were complete,
  stopping at the first route or round 180. Focused tests were **21/21**,
  compileall passed, smoke was **4/4**, and static retained the inherited
  failures. The 24-game all-map screen tied v0040 **12-12**, with candidate Ti
  **95,540** versus **100,530**, zero no-delivery rows, and zero command/TLE/
  suspicious-output failures (`reports/local-20260818T003927Z`).
- Replay review showed better early delivery on Royale/Drakkarfjord but a
  severe Auroraveil delay (first delivery 126 versus 27 turns) and Nordkap
  remained **0-2**. Repair 1 now blocks the handoff after confirmed enemy-Core
  intel; its second screen fell to **11-13** (candidate Ti **118,000** vs
  **124,210**), with zero no-delivery/reliability failures. v162 is rejected
  after the bounded repair; candidate Python was restored byte-identically to
  v0040, rollback focused tests were **20/20**, compileall passed, and rollback
  smoke was **4/4** (`reports/local-20260818T004839Z`). No 60-game gate,
  baseline change, package, upload, activation, or live operation.

### Quick all-map screen reduced to 24 games — 2026-08-18

- The routine screen now runs **24 games**: one seeded candidate-A game on all
  15 configured maps, plus nine deterministic candidate-B side-order repeats.
  `screen_seed` selects both the map/seed pairs and the repeated side orders,
  so every map remains represented while side coverage rotates between
  iterations. The release gate remains the complete 60-game matrix (15 maps ×
  endpoint seeds `1`/`101` × both sides).
- The former 210-game matrix is now an archival reference. An optional
  120-game audit (four rotating seeds × both sides) is reserved for stochastic
  or tie-heavy candidates; it is not part of the routine loop.
- Schedule tests passed **6/6** and the new helper rejects under-covered or
  over-sized schedules. No bot source, baseline, live state, package, upload,
  or activation changed. Validation report:
  `reports/evaluation-policy-20260818-quick24.md`.

### v161 geometry-adaptive Sentinel economy gate rejected at release gate — 2026-08-18

- Tested retaining one-route first-Sentinel pressure only on cramped geometry
  and requiring two completed routes on non-cramped maps. The 30-game all-map
  screen scored **21-9** versus immutable v0040 (candidate Ti **124,530** vs
  **90,520**; no-delivery **1** vs **0**). The 60-game release matrix then
  reversed to **27-33** (candidate Ti **218,890** vs **249,190**; no-delivery
  **0** vs **1**), with Nordkap and Royale both **0-4**.
- Both gates were command-clean with zero TLE/suspicious rows; screen max
  p99/peak was **1,415/5,912 us**. Focused tests were **22/22** before the
  gate and **20/20** after rollback; compileall passed; final smoke was **4/4**
  (`reports/local-20260818T002120Z`). Static retained only inherited failures.
- v161 is **rejected at the release gate** and restored to exact v0040 parity
  (`reports/v161-rollback-source-diff.txt`). No package, upload, activation, or
  baseline transition occurred. Full evidence:
  `reports/evaluation-v161-geometry-adaptive-sentinel.md`.

### v160 turret-line-safe Sentinel placement rejected and rolled back — 2026-08-18

- Tested skipping forward Sentinel sites inside currently observed enemy
  Gunner/Sentinel fire lines, preserving the existing pool, economy, route, and
  cage thresholds. The initial 30-game all-map screen scored **10-20** versus
  immutable v0040 (candidate Ti **109,590** vs **129,900**; no-delivery **0** vs
  **1**). A bounded repair restored the original first-Sentinel timing and
  vetoed only replacement sites per Builder; it scored **11-19** (Ti
  **142,970** vs **128,300**; no-delivery **1** vs **0**).
- Both screens covered all 15 maps, were command-clean with zero TLE/suspicious
  rows, and stayed below the CPU budget (max p99/peak **1,435/3,854 us** and
  **1,392/4,553 us**). Focused tests were **22/22** before rollback and
  **20/20** after; compileall passed; final smoke was **4/4**
  (`reports/local-20260818T000743Z`). Static retained only the inherited
  obsolete-import and navigation fast-path failures.
- v160 is **rejected** and restored to exact recursive v0040 parity
  (`reports/v160-rollback-source-diff.txt`). No 60-game gate, package, upload,
  activation, or baseline transition occurred. Full evidence:
  `reports/evaluation-v160-turret-line-safe-sentinel.md`.

### v159 home barrier shell rejected and rolled back — 2026-08-18

- Tested a geometry-derived shell that let one nearest Dynamic worker build up
  to four safe outer-Core barriers after a route/resource milestone. No route,
  combat, attack, or enemy-target logic changed. The initial 30-game all-map
  screen scored **13-17** against immutable v0040 (candidate Ti **144,240** vs
  **175,500**; no-delivery **0** vs **1**). Repair 1 capped the shell at two
  sites and tied **15-15** (Ti **147,170** vs **126,100**; no-delivery **0** vs
  **0**); repair 2 required three completed routes and fell to **9-21** (Ti
  **127,040** vs **147,350**; no-delivery **0** vs **0**).
- All 90 screen games were command-clean with zero TLE/suspicious rows and
  stayed below the local CPU budget. The candidate source was restored to exact
  recursive v0040 parity after the two allowed repairs; rollback focused tests
  were **20/20**, compileall passed, scoped `git diff --check` passed, and
  `make smoke` was **4/4** (`reports/local-20260817T235010Z`). Full evidence:
  `reports/evaluation-v159-home-barrier.md` and
  `experiments/v0040-home-barrier-shell-v159.md`.
- v159 is **rejected**. The 60-game release gate, package, upload, activation,
  and baseline transition were not attempted. The moving baseline remains
  `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`; live
  platform v104 remains unchanged with no fresh observed series.

### Routine evaluation policy reduced to 30/60 all-scenario games — 2026-08-18

- The routine fast screen is now **30 games**: one stratified map/seed pair for
  each of the 15 configured maps, played in both side orders. `screen_seed`
  remains rotated and recorded, so the selected seed per map still varies
  reproducibly across iterations.
- The routine release gate is now **60 games**: all 15 maps, endpoint seeds
  `1` and `101`, and both side orders. The historical **210-game** matrix is
  retained only as an optional audit for tie-heavy or stochastic hypotheses.
  The 4-game smoke diagnostic is unchanged.
- Schedule tests passed **5/5**; a direct schedule probe confirmed 15/15 map
  coverage, 30 screen games, and 60 release games. `make smoke` was **4/4**
  command-clean (`reports/local-20260817T232515Z`). `make static` retained the
  known inherited repository failures (obsolete candidate imports and two
  navigation fast-path assertions); the policy itself introduces no new
  source or runtime change. Details: `reports/evaluation-policy-20260817.md`.
- No candidate source, immutable baseline, package, upload, activation, or live
  state changed. Future promotion decisions use the 30-game screen first and
  the 60-game gate only for materially positive release candidates.

### v158 graded home-defense cap rejected after two reduced screens — 2026-08-18

- Tested a graded Core defense policy against immutable v0040: after the first
  economy milestone, visible Gunner/Sentinel/Launcher contact retained the
  five-Gunner cap while remote non-siege contact received at most four. The
  focused defense suite was **21/21**, compileall passed, smoke was **4/4**, and
  `make static` retained only the inherited 15 obsolete-import errors plus two
  navigation fast-path assertions. Reports: `reports/v158-*`.
- Initial 36-game all-map screen: **19-17** versus v0040, candidate collection
  **170,900** versus **158,100**, candidate no-delivery **1** versus **0**,
  zero command failures/TLE/suspicious output, max p99 **1,447 us**, peak
  **5,021 us** (`reports/local-20260817T230801Z`,
  `reports/v158-screen36-summary.json`). The +2 margin was not material and
  did not justify the 90-game gate.
- Repair 1 restored the five-Gunner emergency only for non-siege contact within
  squared distance eight of the Core, leaving remote logistics at four. Tests,
  compileall, static, and smoke remained unchanged. The second screen again
  scored **19-17**, with collection **193,220** versus **200,910**, one
  no-delivery row for each side, zero runtime failures, max p99 **1,487 us**,
  and peak **5,267 us** (`reports/local-20260817T231300Z`,
  `reports/v158-repair1-screen36-summary.json`).
- v158 is **rejected after two bounded attempts**. Candidate source and the
  focused fixture were restored byte-identically to v0040; rollback focused
  tests were **20/20**, compileall passed, and rollback smoke was **4/4**
  (`reports/v158-rollback-source-diff.txt`,
  `reports/local-20260817T231807Z`). No 90-game gate, archive, package,
  upload, activation, or baseline transition occurred.

### v157 siege-only Gunner escalation rejected at the reduced screen — 2026-08-18

- Tested restricting the maximum home-Gunner cap to visible enemy siege turrets
  instead of any visible enemy building or Builder, while preserving the
  minimum shell, emergency timing, reserves, routes, and offense. Focused tests
  were **26/26**, compileall passed, smoke was **4/4**, and `make static`
  retained only the inherited 15 obsolete-import errors plus two navigation
  assertions.
- The 36-game all-map screen scored **14-22** versus immutable v0040. Both
  sides delivered in every game; candidate collection was **120,220** versus
  **159,930**, with zero command failures/TLE/suspicious output, max p99
  **1,423 us**, and peak callback **3,333 us**. Reports:
  `reports/local-20260817T225452Z`, `reports/v157-screen36-analysis.json`, and
  `reports/v157-screen36-summary.json`.
- v157 is **rejected**; the Core policy and test fixture were restored,
  recursive Python parity was verified, rollback focused tests were **25/25**,
  compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260817T225859Z`). No 90-game gate or platform operation
  occurred.

### v156 forward Launcher insertion rejected at the reduced screen — 2026-08-18

- Tested one tightly gated forward Launcher: only the primary fixed attacker,
  only after three completed routes and confirmed enemy-Core intel, with a
  replacement-Harvester reserve and a passable insertion tile. Focused tests
  were **29/29**, compileall passed, smoke was **4/4**, and `make static`
  retained only the inherited 15 obsolete-import errors plus two navigation
  assertions.
- The 36-game all-map screen scored **16-20** versus immutable v0040. The
  candidate placed one Launcher, collected **150,880** versus **165,170**, and
  had zero no-delivery rows versus one for v0040; all commands were clean with
  zero TLE/suspicious output, max p99 **1,503 us**, and peak callback
  **4,948 us**. Reports: `reports/local-20260817T224558Z`,
  `reports/v156-screen36-analysis.json`, and
  `reports/v156-screen36-summary.json`.
- v156 is **rejected**; candidate source and the focused Launcher test were
  removed/restored, recursive Python parity was verified, rollback focused
  tests were **25/25**, compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260817T225056Z`). No 90-game gate or platform operation
  occurred.

### v155 offensive cage depth rejected at the reduced screen — 2026-08-18

- Tested increasing the confirmed enemy-Core barrier cage from six to ten
  tiles, matching the barrier-heavy top-team replay pattern while preserving
  the existing route reserve, escape-safety, and Sentinel gates. Focused tests
  were **25/25**, compileall passed, smoke was **4/4**, and `make static`
  retained only the inherited 15 obsolete-import errors plus two navigation
  assertions.
- The 36-game all-map screen scored **16-20** versus immutable v0040. Both
  sides delivered in every game; candidate collection was **167,280** versus
  **179,160**, with zero command failures/TLE/suspicious output, max p99
  **1,381 us**, and peak callback **3,415 us**. Losses clustered on Antler,
  Auroraveil, Drakkarfjord, Fjordgate, Nordkap, Ragnarok, and Royale. Reports:
  `reports/local-20260817T223421Z`, `reports/v155-screen36-analysis.json`, and
  `reports/v155-screen36-summary.json`.
- v155 is **rejected**; the candidate cap and test fixture were restored to
  v0040, recursive Python parity was verified, rollback focused tests were
  **25/25**, compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260817T223903Z`). No 90-game gate or platform operation
  occurred.

### Routine release gate reduced to 90 games — 2026-08-17

- The routine release matrix now runs **15 configured current maps × 3
  deterministic seeds (`1`, `43`, `101`) × 2 side orders = 90 games**. Every
  configured map and both candidate side orders remain covered; the historical
  210-game matrix is retained as an optional audit, not the default iteration
  gate.
- The fast stratified screen is now **18 reproducible map/seed pairs (36 games
  with side swaps)**, every map represented at least once, with a rotating
  `screen_seed`. This keeps the checkpoint map-aware while removing 33% of
  its former cost and 57% of the routine long-gate games.
- Updated `configs/eval_matrix.toml`, `AGENTS.md`, `docs/EVALUATION_PLAN.md`,
  `docs/CURRENT_PLAN.md`, and the release-matrix schedule test. No bot source,
  baseline archive, or live submission changed. Validation report:
  `reports/iter-v153-low-liquidity/release-matrix-policy.log`.

### v153 low-liquidity economy guard rejected at 36-game screen — 2026-08-17

- The candidate kept Dynamic workers in harvest/exploration after three routes
  whenever the bank could not fund one Harvester plus two Conveyor links.
  Focused tests were **22/22**, compileall passed, smoke was **4/4**, and the
  known inherited static failures remained unchanged.
- The reduced all-map screen was **16-20** against immutable v0040, with all
  36 games command-clean, zero TLE/suspicious output, zero no-delivery rows for
  either side, candidate collection **142,340** versus **173,660**, max p99
  **1,469 us**, and peak callback **3,064 us**. Every configured map appeared;
  the largest losses were Fjordgate, Nordkap, Royale, Valkyrie, and Frostgate.
- Status: initial v153 variant rejected; no 90-game gate, archive, package,
  upload, activation, or baseline transition. Two bounded repairs remain
  before restoring v0040. Evidence: `experiments/v0040-low-liquidity-economy-recovery-v153.md`,
  `reports/local-20260817T214644Z`, and
  `reports/iter-v153-low-liquidity/screen36-analysis.json`.

### v153 repair 1 improves collection but remains below release threshold — 2026-08-17

- Repair 1 reduced the low-liquidity reserve from two Conveyor links to one,
  allowing pressure to resume sooner when the bank was tight but not critically
  empty. Focused tests **22/22**, compileall, and smoke **4/4** remained clean;
  static retained the same inherited failures.
- The second 36-game screen improved to **19-17** versus v0040, with candidate
  collection **205,020** versus **188,060** and candidate no-delivery **0** vs
  comparator **2**. All games were command-clean with zero TLE/suspicious
  output; max p99 **1,441 us**, peak **5,708 us**. Evidence:
  `reports/local-20260817T215314Z` and
  `reports/iter-v153-low-liquidity/repair1-screen36-analysis.json`.
- The +2 edge is encouraging but not a material release signal. One bounded
  repair remains: once the enemy Core is confirmed, keep low-liquidity workers
  available for actionable pressure instead of exploration. No 90-game gate or
  baseline transition yet.

### v153 repair 2 rejected; candidate restored to v0040 — 2026-08-17

- Repair 2 bypassed the low-liquidity exploration handoff after a confirmed
  enemy-Core sighting. Focused tests **23/23**, compileall, and smoke **4/4**
  passed; static retained the same 15 obsolete-import errors and two inherited
  navigation assertions.
- The final 36-game screen stayed **19-17**, with candidate collection
  **181,490** versus **167,360**, one candidate no-delivery row versus zero,
  zero command failures/TLE/suspicious output, max p99 **1,541 us**, and peak
  **2,745 us** (`reports/local-20260817T215858Z`; analysis
  `reports/iter-v153-low-liquidity/repair2-screen36-analysis.json`). It did not
  improve paired wins over repair 1 and introduced a delivery regression.
- After two bounded repairs, v153 is **rejected**. Candidate Python source is
  restored byte-identically to immutable v0040; rollback focused tests were
  **20/20**, compileall passed, and rollback smoke was **4/4**
  (`reports/local-20260817T220345Z`). No 90-game gate, archive, package,
  upload, activation, or baseline transition occurred.

### v154 four-route pressure gate ties at 36-game screen — 2026-08-18

- v154 raised `OFFENSE_MIN_HARVESTERS` from three to four, delaying scalable
  Dynamic pressure, the second attacker, and Sentinel pressure until a fourth
  completed route. Focused tests **20/20**, compileall, and smoke **4/4**
  passed; static retained the known inherited result.
- The all-map 36-game screen tied **18-18**, with candidate collection
  **158,070** versus **154,300**, candidate no-delivery **2** versus baseline
  **1**, zero command failures/TLE/suspicious output, max p99 **1,460 us**, and
  peak **2,735 us** (`reports/local-20260817T220758Z`; analysis
  `reports/v154-screen36-analysis.json`). Map losses clustered on
  Archipelago, Icefloe, and Yulerune.
- Status: no 90-game gate or promotion. Repair 1 will keep the four-route gate
  only for Dynamic workers while restoring the fixed attacker's three-route
  timing.

### v154 repair 1 advances to 90-game release gate — 2026-08-18

- Repair 1 restored the fixed attacker's and Sentinel shell's three-route
  timing while holding Dynamic task selection and scalable offense until four
  completed routes. Focused tests **20/20**, compileall, and smoke **4/4**
  passed; static retained the known inherited result.
- The 36-game all-map screen improved to **21-15**, candidate collection
  **178,200** versus **166,600**, zero no-delivery rows for both sides, zero
  command failures/TLE/suspicious output, max p99 **1,357 us**, and peak
  **5,538 us** (`reports/local-20260817T221347Z`; analysis
  `reports/v154-repair1-screen36-analysis.json`).
- Status: positive screen; run the reduced **90-game** release matrix next.
  Known screen regressions (Antler, Auroraveil, Fjordgate, Royale) remain
  release-review risks. No baseline/archive/platform change yet.

### v154 rejected at reduced 90-game release gate; v0040 retained — 2026-08-18

- The 90-game matrix covered all 15 configured maps, seeds **1/43/101**, and
  both side orders; all **90/90** commands were clean. v154 repair 1 scored
  **42-48** versus v0040, with candidate collection **390,960** versus
  **428,030**, candidate no-delivery **0** versus **1**, zero TLE/suspicious
  output, max p99 **1,460 us**, and peak **5,724 us** (`reports/local-20260817T221821Z`;
  analysis `reports/v154-release90-analysis.json`).
- The positive 36-game edge did not transfer to the release distribution.
  v154 is **rejected**, not archived, packaged, uploaded, activated, or
  promoted. Candidate Python source was restored byte-identically to v0040;
  rollback focused **20/20**, compileall passed, and rollback smoke **4/4**
  (`reports/local-20260817T222825Z`).

### v0075 route-continuity experiment rejected — 2026-08-15

- Tested deterministic nearest-Builder repair ownership plus pressure preemption against immutable v0034. Initial screen: **22-32**, 249,830-275,210 titanium. Repair 1 limited immediate interruption to `ADVANCE`: **29-25**, 258,300-237,120, but the four-win edge was insufficient for the full gate. Final ownership-only repair: **23-31**, 225,340-265,560.
- All three screens were 54/54 command-clean with zero no-delivery rows, TLEs, or suspicious output. Focused suites passed 18/18, 19/19, and 19/19; each smoke was 4/4 command-clean. `make static` consistently retained the inherited 15 obsolete-import failures. Evidence: `experiments/v0075-route-continuity.md`, `reports/local-20260815T155900Z`, `reports/local-20260815T160833Z`, and `reports/local-20260815T161700Z`.
- The local visibility-based ownership rule is not stable enough: one Builder can suppress another without a shared route-distress assignment. After two bounded repairs, Iteration B is rejected and Iteration C is blocked. Candidate production source is restored byte-identically to v0034; rollback smoke was 4/4 command-clean (`reports/local-20260815T162556Z`). No full matrix, package, upload, or activation was performed.

### v0034 four-route economy gate promoted locally — 2026-08-15

- Delayed the second fixed attacker and dynamic pressure until four completed Harvester routes while preserving the first scout and urgent defense/repair/hijack work. Focused tests passed 12/12, compileall passed, and smoke was 4/4 command-clean; `make static` retained the inherited 15 obsolete-import failures.
- The 54-game screen versus v0032 finished **32-22 (59.3%)**, with 249,640 versus 215,880 titanium and zero candidate no-delivery rows (`reports/local-20260815T151644Z`).
- The full 210-game gate finished **112-98 (53.3%)**, with 1,045,020 versus 1,027,770 titanium, zero candidate no-delivery rows versus two, and zero command failures/TLE/suspicious output (`reports/local-20260815T152315Z`). Weak maps remain Jackpot 1-9, Showdown 2-8, Fjord 3-7, Pinch 4-6, Twins 4-6, and Vault 3-7.
- Promoted immutable baseline: `bots/versions/v0034_four-route-economy-gate_20260815-1549_eeafad8f`; package SHA-256 `a54f4191dfe1ea7a3ac0b73e5e77ab43edad7daad1b689f460e95a09040e6542`. No upload or activation was performed. Iteration B will target broken-route continuity without changing the Store protocol.

### v0032 uploaded to platform as version 100 — 2026-08-15

- Upload-only command succeeded for `v0032-nearest-threat-task-claim-eeafad8f`; platform ID `33e0c15f-913f-4d29-a9e9-02b6f0b34bf5`, status `ready`. Upload report: `reports/upload-20260815T121536Z/upload.json`; command log: `reports/upload-v0032-command.log`.
- A post-upload submission/status check reports version 100 as the active submission. No explicit activation command was issued; `scripts/live_operator.py observe` recorded the platform state in `reports/live-observe-20260815T121610Z` and preserved v99 as the previous active version and v72 as last known-good.

### v0032 nearest-threat task claim promoted locally — 2026-08-15

- Reaffirmed v0032 as the moving local baseline after the sequential long gate: **123/210 wins (58.6%)** versus v0031, while v0033 only tied v0032 **105/210 (50.0%)** and was rejected.
- Frozen archive: `bots/versions/v0032_nearest-threat-task-claim_20260815-0438_eeafad8f`; package SHA-256: `c380df83f42d0502b2b23bcaa8ba3edab03dbec071d9aafe6f013d4ecd9fe022`.
- `configs/eval_matrix.toml`, `configs/eval_regression.toml`, `configs/eval_smoke.toml`, `state/project_state.json`, and `docs/START_HERE.md` point to v0032. No upload or activation was performed.

### Sequential long validation retained v0032 baseline — 2026-08-15

- Ran the requested 210-game matrices sequentially with the same 21 maps, five seeds, side swaps, and 10 ms TLE: v0032 versus v0031 completed **123-87 (58.6%)**; v0033 versus v0032 completed **105-105 (50.0%)**.
- Both runs were 210/210 command-clean with zero TLEs and zero suspicious-output markers. Replay analysis reports max p99 callback times of 1,414 us (v0032) and 1,516 us (v0033); candidate no-delivery rows were 2 and 6 respectively. Full analyses: `reports/local-20260815T050845Z/full-analysis.json` and `reports/local-20260815T053203Z/full-analysis.json`.
- Post-decision smoke against the retained v0032 baseline was **4/4 command-clean** (`reports/local-20260815T060150Z`; raw log `reports/long-validation-smoke.log`). Config parsing, JSON validation, and `git diff --check` also passed.
- `make static` exited 2 on the repository's known 15 obsolete test imports (`reports/long-validation-static.log`); no new runtime/TLE issue was introduced by this validation.
- The earlier 54-game v0033 screen edge did not survive the long comparison, so v0033 is **not promoted**. The evaluation configs and durable state now retain `bots/versions/v0032_nearest-threat-task-claim_20260815-0438_eeafad8f` as the moving local baseline; the v0033 archive remains immutable for replay review. No upload or activation was performed.
- Raw runner logs: `reports/long-v0032-v0031-rerun.log` and `reports/long-v0033-v0032.log`. Remaining risk: v0032 still has map-specific regressions and needs route-conversion/loss replay analysis before the next bounded strategy change.

### v0073 quiet-defense turret retirement and workforce reuse promoted locally — 2026-08-15

- Baseline before this experiment: immutable `bots/versions/v0032_nearest-threat-task-claim_20260815-0438_eeafad8f`; no platform operation performed.
- Hypothesis: after a long quiet, mature defense, encode one Builder ID in the Store marker so that Builder can destroy exactly one intact outer home Gunner; after the Core observes the removal, use the freed unit-cap slot for one extra late Builder. Experiment record: `experiments/v0073-turret-retirement-workforce-reuse.md`.
- Focused tests passed 11/11; compileall passed; smoke was 4/4 command-clean; `git diff --check` passed. `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-turret-retirement-v0073/`.
- 54-game screen: **34/54 (63.0%)** candidate wins versus 20 comparator wins, collection 258,030 versus 255,210 (1.0110x), zero no-delivery rows for either side, zero command failures/TLE/suspicious output, max p99 1,323 us and peak callback 4,760 us (`reports/local-20260815T044840Z`, analysis `reports/iter-turret-retirement-v0073/screen-analysis.json`). Every map was at least even; String, Bridge, Longship, and Vault showed the clearest gains.
- Status: **promotion 3 accepted locally** under the moving win-rate policy. The aggregate +14-win edge justified acceptance despite collection being nearly flat; the candidate was archived as the new moving baseline. No upload or activation was performed.

### v0072 nearest home-threat task claim promoted locally — 2026-08-15

- Baseline before this experiment: immutable `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; no platform operation performed.
- Hypothesis: assign a visible home threat only to the nearest eligible non-attacker during task selection, so other Builders continue to useful work instead of claiming and discarding the same task at execution time. Experiment record: `experiments/v0072-nearest-threat-task-claim.md`.
- Focused tests passed 8/8; compileall passed; smoke was 4/4 command-clean; `git diff --check` passed. `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-nearest-threat-task-claim-v0072/`.
- 54-game screen: **42/54 (77.8%)** candidate wins versus 12 comparator wins, collection 287,380 versus 194,600 (1.4768x), zero no-delivery rows, zero command failures/TLE/suspicious output, max p99 1,482 us and peak callback 2,766 us (`reports/local-20260814T234501Z`).
- Full 210-game matrix: **121/210 (57.6%)** candidate wins versus 89 comparator wins, collection 1,062,460 versus 923,170 (1.1509x), four candidate no-delivery rows versus three comparator rows, zero command failures/TLE/suspicious output, max p99 1,490 us and peak callback 3,386 us (`reports/local-20260814T235305Z`, analysis `reports/iter-nearest-threat-task-claim-v0072/full-analysis.json`).
- Status: **promotion 2 accepted locally** under the moving win-rate policy. The aggregate gain over v0031 was large enough to accept despite localized Aurora/Bridge/Longship/Runestone/String regressions. The candidate was archived as the new moving baseline; no package upload or activation was performed beyond the local immutable archive.

### v0071 bounded alternate-Core scout rejected — 2026-08-15

- Baseline: immutable `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; no platform operation performed.
- Hypothesis: keep the first attacker on the direct symmetry lane, and after a bounded no-sighting epoch let only the second attacker probe horizontal/vertical counterparts to discover a non-rotational enemy Core without placing a guessed Sentinel.
- Focused gate: 9/9 passed; compileall passed; smoke 4/4 command-clean; `git diff --check` passed; `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-bounded-alternate-core-scout-v0071/`.
- 54-game screen: **26/54 (48.1%)** candidate wins versus 28 comparator wins, collection 242,820 versus 246,690 (0.9843x), zero no-delivery rows for either side, zero command failures/TLE/suspicious output, max p99 1,330 us and peak callback 2,749 us. Report `reports/local-20260814T233244Z`; analysis `reports/iter-bounded-alternate-core-scout-v0071/screen-analysis.json`.
- Status: **rejected at the screen gate**; the bounded alternate-Core scout was reliability-clean but did not beat v0031 on paired wins or collection. Candidate sources and tests were restored byte-identically (`reports/iter-bounded-alternate-core-scout-v0071/revert-source-diff.txt`). No full matrix, package, upload, activation, or baseline transition occurred.

### v0070 cramped-map early sentinel shell rejected — 2026-08-15

- Baseline: immutable `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; no platform operation performed.
- Hypothesis: after the first route on compact boards only, add a second early forward Sentinel while retaining the one-Sentinel economy-first opening on long boards.
- Focused gate: 9/9 passed before the screen and 7/7 after rollback; compileall passed; smoke 4/4 command-clean; `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-cramped-early-sentinel-shell-v0070/`.
- 54-game screen: **21/54 (38.9%)** candidate wins versus 33 comparator wins, collection 210,430 versus 248,230 (0.8477x), one candidate no-delivery row versus none for the comparator, zero command failures/TLE/suspicious output, max p99 1,467 us and peak callback 3,026 us. Report `reports/local-20260814T231336Z`; analysis `reports/iter-cramped-early-sentinel-shell-v0070/screen-analysis.json`.
- Status: **rejected at the screen gate**; the compact-map second-Sentinel shell hurt paired wins, collection, and delivery. Source and focused tests were restored byte-identically to v0031 (`reports/iter-cramped-early-sentinel-shell-v0070/revert-source-diff.txt`). No full matrix, package, upload, activation, or baseline transition occurred.

### v0069 loaded attacker sabotage rejected — 2026-08-15

- Baseline: immutable `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; no platform operation performed.
- Hypothesis: let a fixed attacker destroy a currently loaded enemy conveyor/splitter already in vision, then resume the direct sentinel/core lane; empty and unseen logistics remained excluded.
- Focused gate: 9/9 passed; compileall passed; smoke 4/4 command-clean; `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-loaded-attacker-sabotage-v0069/`.
- 54-game screen: **23/54 (42.6%)** candidate wins versus 31 comparator wins, collection 228,660 versus 235,770 (0.9698x), one candidate no-delivery row versus none for the comparator, zero TLE/suspicious output/command failures, max p99 1,403 us and peak callback 2,758 us. Report `reports/local-20260814T230109Z`; analysis `reports/iter-loaded-attacker-sabotage-v0069/screen-analysis.json`.
- Status: **rejected at the screen gate**; the fixed-attacker sabotage pulse hurt win rate, collection, and delivery. Source was reverted byte-identically to v0031 (`reports/iter-loaded-attacker-sabotage-v0069/revert-source-diff.txt`). No full matrix, package, upload, activation, or baseline transition occurred.

### v0068 remote soft-threat lease rejected — 2026-08-15

- Baseline: immutable `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; no platform operation performed.
- Hypothesis: record confirmed turret ownership and expire an unseen non-turret home-threat task after a bounded lease, avoiding a stale priority-0 commitment while preserving turret stickiness.
- Focused gate: 9/9 passed; compileall passed; smoke 4/4 command-clean; `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-remote-soft-threat-lease-v0068/`.
- 54-game screen: **24/54 (44.4%)** candidate wins versus 30 comparator wins, collection 231,330 versus 255,610 (0.9050x), zero candidate/comparator no-delivery rows, zero TLE/suspicious output/command failures, max p99 1,332 us and peak callback 2,575 us. Report `reports/local-20260814T225021Z`; analysis `reports/iter-remote-soft-threat-lease-v0068/screen-analysis.json`.
- Status: **rejected at the screen gate**; the lease hurt both paired wins and collection. Source files were reverted byte-identically to v0031 (`reports/iter-remote-soft-threat-lease-v0068/revert-source-diff.txt`). No full matrix, package, upload, activation, or baseline transition occurred.

### v0067 soft home-threat stall handoff rejected — 2026-08-15

- Baseline: immutable `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; no platform operation performed.
- Hypothesis: clear a stalled non-turret `TASK_HOME_THREAT` after danger-aware and ordinary navigation both fail, while keeping turret threats sticky so the worker can return to productive work.
- Focused gate: 9/9 passed; compileall passed; smoke 4/4 command-clean; `make static` retained the inherited exit-2 obsolete-import result. Logs: `reports/iter-soft-home-threat-stall-v0067/`.
- 54-game screen: **26/54 (48.1%)** candidate wins versus 28 comparator wins, collection 229,270 versus 232,810 (0.9848x), zero candidate/comparator no-delivery rows, zero TLE/suspicious output/command failures, max p99 1,287 us and peak callback 2,633 us. Report `reports/local-20260814T223822Z`; analysis `reports/iter-soft-home-threat-stall-v0067/screen-analysis.json`.
- Status: **rejected at the screen gate**; lower win rate and collection did not justify a full matrix. Candidate source was reverted byte-identically to v0031 (`reports/iter-soft-home-threat-stall-v0067/revert-diff.txt`). No package, upload, activation, or baseline transition occurred.

### v87 comparator experiments rejected — 2026-08-12

- Baseline: exact active v87 artifact, SHA-256 `0c59d375548f427371f14eb48ec58eea761b63a9164e72753f3cc9ee6489b4`; no platform operation performed.
- Rejected early-only local ore ownership: 27-27, 191,740-204,420 titanium (0.938x), all 54 games reliability-clean; report `reports/local-20260812T085133Z`, replay analysis `reports/early-only-ore-ownership-v87-analysis.json`.
- Rejected diagonal Gunner facing: first 30-24 / 0.979x, repeat 25-29 / 0.929x; reports `reports/local-20260812T085837Z` and `reports/local-20260812T090248Z`, analyses `reports/diagonal-gunner-v87-analysis.json` and `reports/diagonal-gunner-v87-repeat-analysis.json`.
- Rejected four-harvester dynamic-offense gate: 26-28, 203,190-211,600 titanium (0.960x), zero TLE/suspicious output, p99 1.185 ms, peak callback 4.228 ms; report `reports/local-20260812T090825Z`, analysis `reports/four-harvester-offense-gate-v87-analysis.json`.
- Focused static contract (8/8), compileall, and smoke (4/4, `reports/local-20260812T090811Z`) pass. `make static` remains blocked by known obsolete legacy-import tests; it was not used as a passing gate.
- Unit review: there is no teleport unit; a Launcher throws an adjacent friendly or enemy Builder. Barriers are already used for enemy-ore denial; Splitters are supported as conveyor sinks but require a delivered-throughput experiment before enabling. No speculative unit behavior was retained.
- Current candidate is restored to full local ore ownership and the three-harvester offense gate. Neither new hypothesis earned promotion; next work must diagnose its durable v87 map losses before another bounded change.

This file is the durable handoff between Codex sessions. It is append-only except for the **Current state** table, which automation may refresh.

## Current state

| Field | Value |
|---|---|
| Workflow phase | active_observing |
| Working candidate | `bots/candidate` |
| Current local baseline | `bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f` |
| Current active platform version | 109 |
| Last known-good platform version | 107 |
| Previous active platform version | 107 |
| Last known-good live score | 0.5128205128205128 |
| Current candidate live score | 0.6 |
| Last deployment | 2026-08-20T02:30:55Z |
| Last observation | 2026-08-20T18:25:06Z |
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

### Pinned Ruff public-readiness follow-up — 2026-08-23T08:17:09Z

- Added Ruff 0.16.4 to the uv development lock and exposed `make lint`.
- Ruff checks maintained harness and tests; immutable baseline/version and upload-shaped bot trees remain excluded from mechanical rewrites.
- Removed unused imports and assignments, normalized import ordering and UTC usage, and simplified equivalent subprocess capture without changing bot code or live state.
- Validation: make lint passed; make static passed 67/67 plus compileall; make doctor passed; git diff check passed.


### Public-readiness audit — 2026-08-23T07:56:59Z

- Scope: repository hygiene, documentation, metadata, secret/history screening, deterministic checks, and Git remote parity; bot and live platform state were not changed.
- Removed: obsolete root starter main.py, v0001 docs submission, generated egg-info and ChatGPT packets/context, stale iteration packet, and accumulated rejected content from docs/CURRENT_PLAN.md.
- Updated: README.md, .gitignore, .gitattributes, CONTRIBUTING.md, SECURITY.md, docs/{CURRENT_PLAN,REPOSITORY_CLEANUP,REPOSITORY_STRUCTURE,SELF_REVIEW,START_HERE}.md, scripts/project_context.py, and state/project_state.json.
- Checks: startup-context 6/6; make static 67/67 plus compileall; make doctor passed with fcode 2.3.4, Codex CLI 0.147.0, Git, and 43 synced maps.
- Security: current tree and all reachable commits had no common private-key/token signatures; no tracked private home paths were found; git fsck was clean.
- Local artifacts: 92 ignored superseded submission/platform files were moved to `/tmp/fcl-public-audit-FRNano`; the v0047 ZIP and manifest were retained.
- Risk: no open-source license has been selected; public visibility is ready, but reuse rights remain reserved until the owner chooses a license.


### Live observation captured — 2026-08-20T18:25:06Z

- Active version: 109
- Report: reports/live-observe-20260820T182446Z


### Live observation captured — 2026-08-20T17:55:11Z

- Active version: 109
- Report: reports/live-observe-20260820T175449Z


### Live observation captured — 2026-08-20T17:29:24Z

- Active version: 108
- Report: reports/live-observe-20260820T172904Z


### Live observation captured — 2026-08-20T16:49:31Z

- Active version: 108
- Report: reports/live-observe-20260820T164909Z


### Live observation captured — 2026-08-20T16:25:50Z

- Active version: 108
- Report: reports/live-observe-20260820T162527Z


### Live observation captured — 2026-08-20T14:04:59Z

- Active version: 108
- Report: reports/live-observe-20260820T140438Z


### Live observation captured — 2026-08-20T13:17:42Z

- Active version: 108
- Report: reports/live-observe-20260820T131722Z


### v352 source-Sentinel interceptor rejected in self-review; v0046 retained — 2026-08-20

- Live v108 replay inspection found a concrete post-source failure: enemy
  Sentinels removed active Harvesters on Nordkap, Icefloe, and Yulerune before
  their routes converted.  The first local response considered one correctly
  faced Sentinel between a threatened source and the hostile turret.
- It passed temporary focused coverage **30/30**, then failed the mechanics
  review before a matrix: Sentinel fire is not blocked by intervening units,
  target choice belongs to the opponent, and the opening Core guarantees only
  10 ammo while killing a 40-HP Sentinel requires three 10-ammo shots.
  A line interceptor could therefore spend 30 Ti without saving the source.
- The temporary code/test were removed rather than repaired by parameters.
  Source parity with immutable v0046 is empty at
  `reports/iter-v352-source-sentinel-interceptor/rollback-source-parity.diff`;
  rollback focused coverage was **26/26**, compileall passed, inherited static
  retained only the 15 stale imports/two navigation assertions, and smoke was
  **4/4 command-clean** at `reports/local-20260820T130712Z`.
- No candidate screen, release matrix, remote gate, package, upload,
  activation, promotion, or live-state change occurred.  Full record:
  `experiments/v0046-source-sentinel-interceptor-v352.md`.  Next work must
  identify a preemption mechanism that still works against deliberate direct
  Harvester targeting and the 10-ammo opening floor.

### v351 opening source-admission rejected; v0046 retained — 2026-08-20T14:46:30+02:00

- Fresh v108 replay evidence remains a conversion fault, not a runtime fault:
  the Askar City loss was zero-TLE/zero-suspicious but spent 31–60 Conveyors
  for 1–3 Harvesters and had an Auroraveil no-delivery row.  v351 tested only
  a visible, local opening source-to-Core admission rule in
  `bots/candidate/bot/defender.py`; it did not alter the Store, Core, roles,
  attacker/dynamic policy, immutable baseline, package, or live state.
- The initial two-cell runway version was **5-10** against immutable v0046 on
  the seed-172 all-map screen despite 15/15 deliveries and zero TLE/suspicious
  rows (`reports/local-20260820T123157Z`).  Its Ragnarok first delivery was
  **193 vs 10**.  The single replay-backed repair admitted a one-cell exit,
  restored Ragnarok to **9 vs 9**, but still lost **7-8** and collected
  57,100 vs 63,700 Ti (`reports/local-20260820T123902Z`).
- Focused coverage passed **39/39** then **40/40**; compileall and smoke were
  clean.  Static has only the known inherited 15 obsolete imports and two
  navigation assertions.  Neither screen met the required **9-6** first gate,
  so no rotated screen, 60-game matrix, remote gate, package, upload,
  activation, or promotion ran.  Full evidence:
  `experiments/v0046-source-admission-v351.md`.
- Candidate source was restored exactly to immutable v0046; parity proof is
  the empty `reports/iter-v351-final-source-parity.diff`.  Rollback focused
  tests passed **35/35**, compileall passed, and smoke was **4/4** at
  `reports/local-20260820T124302Z`.  Next work must establish a new
  post-source conversion causal event from replay evidence; do not repeat
  source-admission/runway/staging/heading variants.

### Live score evaluated — 2026-08-20T03:06:04Z

- Version: 108
- Series: 2
- Score: 0.6
- Adjusted score: 0.12642394898760037
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: Active v108 has two confidently attributed rated post-activation series: 1-1 by series and 6-4 by games, for a 0.6000 fractional live score. Mean opponent-Elo expected score was 0.473576, giving residual +0.126424; rating rose 8.091133. Rank-before evidence is unavailable. All 104 raw command records succeeded with empty stderr, all 108 submissions were ready, and all 100 prefetched matches were complete with no match errors, resignations, crashes, submission errors, obvious TLEs, or exceptions. Despite promising results, two series are below the 12-series minimum.


### Live observation captured — 2026-08-20T03:04:01Z

- Active version: 108
- Report: reports/live-observe-20260820T030338Z


### Live score evaluated — 2026-08-20T02:34:01Z

- Version: 108
- Series: 0
- Score: None
- Adjusted score: None
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: Active v108 has zero attributable post-activation series, below the 12-series minimum. All 100 prefetched matches predate activation and use v101/v105/v106/v107; the latest was v107 and ended 15m50s before activation. Rating therefore remained 1582.2632; rank-before is unavailable. No opponent-Elo expected score or residual is computable. All 104 command records succeeded with empty stderr, all 108 submissions were ready, and no match errors, resignations, crashes, TLEs, or exceptions were found.


### Live observation captured — 2026-08-20T02:31:58Z

- Active version: 108
- Report: reports/live-observe-20260820T023136Z


### Candidate activated — 2026-08-20T02:30:55Z

- Version: 108
- Previous/rollback: 107
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260820T023034Z


### Candidate uploaded — 2026-08-20T02:30:55Z

- Candidate: v0045-opening-launcher-relay-eeafad8f
- Version: 108
- Rollback target: 107
- Report: reports/live-deploy-20260820T023034Z


### Live candidate promoted — 2026-08-20T02:29:31Z

- Version: 107
- Live score: 0.5128205128205128
- Adjusted score: 0.010270719982161428
- Reason: Active v107 has 100/195 wins across 39 explicitly attributed rated ladder series after activation, exceeding the preferred 24-series window. Six interleaved v105 series were excluded. Mean Elo-expected score was 0.502550, yielding residual +0.010271; v107-series Elo deltas total +12.8179. The overall rating boundary rose 20.1253 because excluded v105 series contributed separately. Raw score exceeds the recorded known-good 0.5000, adjusted performance is positive, and no clear regression exists. All 104 command records succeeded with empty stderr; all 107 submissions were ready, and 100 complete match-info records showed no submission errors, match errors, resignations, crashes, obvious TLEs, or exceptions. Rank-before evidence is unavailable; current raw status rank is 38.


### Live score evaluated — 2026-08-20T02:29:31Z

- Version: 107
- Series: 39
- Score: 0.5128205128205128
- Adjusted score: 0.010270719982161428
- Reliability failures: 0
- Proposed decision: promote
- Reason: Active v107 has 100/195 wins across 39 explicitly attributed rated ladder series after activation, exceeding the preferred 24-series window. Six interleaved v105 series were excluded. Mean Elo-expected score was 0.502550, yielding residual +0.010271; v107-series Elo deltas total +12.8179. The overall rating boundary rose 20.1253 because excluded v105 series contributed separately. Raw score exceeds the recorded known-good 0.5000, adjusted performance is positive, and no clear regression exists. All 104 command records succeeded with empty stderr; all 107 submissions were ready, and 100 complete match-info records showed no submission errors, match errors, resignations, crashes, obvious TLEs, or exceptions. Rank-before evidence is unavailable; current raw status rank is 38.


### Live observation captured — 2026-08-20T02:25:39Z

- Active version: 107
- Report: reports/live-observe-20260820T022518Z


### v313 phase-adaptive runtime roles rejected and rolled back — 2026-08-20T00:22:49Z

- Top-team evidence motivated a structural runtime-role handoff: the existing Core economy phase temporarily sent ungraduated attackers and dynamic Builders through SCOUT/CHAIN conversion, with per-Builder graduation after a completed route; the permanent Defender floor stayed fixed.  The official v15 source was benchmarked separately and lost 1-14 to v0044 (`reports/local-20260820T000931Z`), so it was not copied.
- Files changed during the experiment: `bots/candidate/main.py`, `bots/candidate/bot/defender.py`, `bots/candidate/bot/constants.py`, and `tests/test_candidate_runtime_roles.py`; immutable v0044 and `bots/baseline/` were untouched.
- Initial checks: focused **38/38**, compileall pass, `make static` inherited 15 obsolete imports plus 2 navigation assertions, smoke **4/4** at `reports/local-20260820T001627Z`.
- Initial 15-map screen: **4-11** candidate-A, 14/15 candidate deliveries, collection **55,840/76,200 Ti**, first-delivery means **25.50/23.33**, zero TLE/suspicious; report `reports/local-20260820T001658Z`.
- One bounded repair released the primary attacker after four completed routes except during CRISIS.  Checks were **40/40**, compileall pass, static inherited profile, smoke **4/4** at `reports/local-20260820T001945Z`; repair screen was **6-9**, 15/15 deliveries both sides, collection **74,290/94,870 Ti**, first-delivery means **26.07/37.13**, max p99/peak **1,328/3,021 us**, report `reports/local-20260820T002007Z`.
- Decision: reject after the permitted repair; the win-rate edge did not appear and collection remained behind v0044.  No long gate, package, upload, activation, or live transition.
- Rollback: recursive production parity with immutable v0044 is empty at `reports/iter-v313-runtime-role/rollback-source-parity.diff` and `rollback-main-parity.diff`; rollback focused **34/34**, compileall pass, static inherited exit 2, smoke **4/4** at `reports/local-20260820T002249Z`.  Local baseline, live v107, and guarded v105 rollback are unchanged.

### v311 shared ore-claim route coordinator rejected — 2026-08-19T23:38:32Z

- Hypothesis: top-team-style expiring ore ownership would coordinate distinct parallel harvest routes using the existing four ore advertisement slots; permanent attackers remained unowned publishers.
- Files changed: bots/candidate/bot/util.py, bot/defender.py, bot/dynamic.py, main.py, and tests/test_candidate_economy_phase.py during the experiment; all claim edits/tests were removed on rollback. Immutable v0044 baseline was untouched.
- Initial checks: focused 37/37, compileall pass, make static inherited 15 obsolete-module imports plus 2 navigation assertions, smoke 4/4; report reports/local-20260819T232622Z.
- Initial rotated 15-map screen: 4-11 candidate-A, command-clean; several losses converted only 3-5 Harvesters; report reports/local-20260819T232848Z.
- Bounded repair tied leases to active economy tasks, released them on exit, and favored the owner target; focused 38/38, compileall pass, static inherited profile, smoke 4/4.
- Repair screen: 5-10 candidate-A, command-clean but two candidate no-delivery rows; report reports/local-20260819T233334Z. No long gate or promotion.
- Rollback: production source recursively matches immutable v0044 (empty reports/v311-rollback-source-parity.diff and reports/v311-rollback-main-parity.diff); rollback focused 34/34, compileall pass, static inherited profile, smoke 4/4 at reports/local-20260819T233736Z.
- Remaining risk: unscoped visibility-based claims can starve routes under delayed Store writes; do not retry this protocol without a stronger assignment/commitment lifecycle. Live v107 and v105 rollback are unchanged.


### v310 shared siege-cage pressure lease rejected and rolled back — 2026-08-19T23:08:33Z

- Hypothesis: after the three-route/Sentinel shell, dynamic pressure Builders should share the existing reserve-backed enemy-Core Barrier cage before spending low-efficiency Builder fire, matching top-team topology pressure.
- Initial 15-map screen: 8-7 candidate-A, 15/15 command/delivery-clean, no TLE/suspicious output; candidate barriers were active on 12/15 games. Report: reports/local-20260819T225438Z.
- 60-game endpoint gate: 31-29 (51.7%), 60/60 command-clean; candidate Barrier mean 4.43 versus comparator 4.40, but Archipelago and Nordkap floors collapsed. Report: reports/local-20260819T225630Z.
- Bounded repair restricted cage construction to pressure workers already within enemy-Core cage radius; focused repair was 37/37 and smoke 4/4, but screen regressed to 5-10. Report: reports/local-20260819T230356Z.
- Decision: reject after one repair; removed dynamic cage branch and temporary tests, restored zero recursive production-source diff to immutable v0044. No package, upload, activation, or live-state change.
- Remaining risks: inherited make static profile remains 15 obsolete removed-module import errors plus two navigation fast-path assertions; live v107 remains active_observing at 0.5125 with v105 rollback.


### v309 compact control opening rejected and rolled back — 2026-08-19T22:48:55Z

- Hypothesis: on cramped maps, a reserve-backed primary Launcher plus an early Sentinel would reproduce top-team control-first pressure without disturbing wide-map economy.
- Initial 15-map screen: 3-12 candidate-A versus immutable v0044; command-clean but compact losses showed only two Harvesters and delayed/empty delivery. Report: reports/local-20260819T223320Z.
- Bounded repair delayed Launcher construction until three completed routes; focused subset was 39/39, compileall passed, smoke was 4/4, and the repair screen recovered to 9-6 with no TLE/suspicious output. Report: reports/local-20260819T223741Z.
- Release-sized 60-game endpoint gate was 31-29 (51.7%), all 60 command-clean; the Launcher did not materially activate, so no repeatable control edge was shown. Report: reports/local-20260819T224021Z.
- Decision: reject after one repair; removed v309 production/test additions and restored zero recursive source diff to immutable v0044. No package, upload, activation, or live-state change.
- Remaining risks: inherited make static profile remains 15 obsolete removed-module import errors plus two navigation fast-path assertions; live v107 remains active_observing at 0.5125 with v105 rollback.


### v308 verified offensive mobility relay rejected — 2026-08-19T22:20:26Z

- Live/top-team evidence motivated a bounded Launcher relay: one reserve-backed Launcher per permanent Attacker after the first paying route, with strict visible progress and can_launch gates; route owners and the permanent Defender were never eligible.
- Initial relay coverage 37/37, compileall pass, inherited make static profile, smoke 4/4 at reports/local-20260819T220959Z; the 15-map screen was 5-10, 56,250/66,690 Ti, 14/15 candidate deliveries at reports/local-20260819T221018Z.
- One permitted repair removed only the front-distance build gate. Coverage 38/38, compileall pass, smoke 4/4 at reports/local-20260819T221331Z; screen improved to 7-8, 56,360/55,140 Ti, 15/15 deliveries, first delivery 28.7 vs 38.9 turns at reports/local-20260819T221350Z.
- Independent seed-173 screen regressed to 6-9, 45,980/53,320 Ti, despite 15/15 deliveries at reports/local-20260819T221608Z; the edge was not repeatable.
- Reject v308. Relay source/test removed; rollback focused tests 34/34, compileall pass, static retains inherited failures, rollback smoke 4/4 at reports/local-20260819T221855Z, and production parity with immutable v0044 is zero at reports/iter-v308-launcher-relay/rollback-source-parity.diff.
- No long gate, package, upload, activation, or live transition. Live v107 remains active_observing at 0.5125 with v105 as operational rollback; experiment: experiments/v0044-verified-offensive-mobility-relay-v308.md.


### v307 map-relative route-lane ownership rejected — 2026-08-19T21:57:13Z

- Top-team replay evidence motivated a structural route-lane scheduler: non-attacker Builders preferred deterministic Core-relative ore sectors with nearest-source fallback.
- Initial screen was 7-8 with 51,620/56,520 Ti and 15/15 first delivery on both sides; report reports/local-20260819T215002Z and analysis reports/iter-route-lane-screen-analysis.json.
- One bounded detour/opening repair regressed to 4-11 with 35,210/57,340 Ti; report reports/local-20260819T215304Z and analysis reports/iter-route-lane-repair-screen-analysis.json.
- Reject v307. Lane code and focused test were removed; production parity with immutable v0044 is zero at reports/iter-route-lane-rollback-source.diff.
- Rollback focused tests 34/34, compileall passed, smoke 4/4 at reports/local-20260819T215601Z; make static retains inherited 15 stale imports and two navigation assertions at reports/iter-route-lane-rollback-static.log.
- No long gate, package, upload, activation, or live transition. Live v107 remains active_observing; v105 remains operational rollback.
- Experiment: experiments/v0044-route-lane-ownership-v307.md.


### Live observation captured — 2026-08-19T18:55:39Z

- Active version: 107
- Report: reports/live-observe-20260819T185520Z


### Live score evaluated — 2026-08-19T18:40:23Z

- Version: 107
- Series: 16
- Score: 0.5125
- Adjusted score: 0.0232120242887135
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: Active v107 has 41/80 game wins across 16 explicitly attributed rated series after its 2026-08-19T11:17:51Z activation: raw score 0.5125, mean Elo-expected score 0.489288, and residual +0.023212. Explicit v105 series interleaved in the capture were excluded. The rating boundary rose 19.1920 Elo; v107-series deltas sum to +11.8846 because of those interleaved excluded matches. Rank-before evidence is unavailable; current rank is 37. All 104 command records succeeded with empty stderr, all 107 submissions are ready, and 100 complete prefetched matches show no submission errors, match errors, resignations, crashes, obvious TLEs, or exceptions. The 12-series minimum is met, but the raw score is not a clear regression and 16 series remain below the preferred 24-series promotion window, so keep observing.


### Live observation captured — 2026-08-19T18:37:33Z

- Active version: 107
- Report: reports/live-observe-20260819T183712Z


### Live observation captured — 2026-08-19T14:39:22Z

- Active version: 107
- Report: reports/live-observe-20260819T143902Z


### Live observation captured — 2026-08-19T13:59:16Z

- Active version: 107
- Report: reports/live-observe-20260819T135856Z


### Live score evaluated — 2026-08-19T12:52:42Z

- Version: 105
- Series: 2
- Score: 0.5
- Adjusted score: 0.079182153224668
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Raw status identifies v105 as currently active, but state/live_state.json's 2026-08-19T11:17:51Z activation timestamp belongs to v107. Therefore the current v105 reactivation time is uncertain. Only the two newest contiguous v105 series following the last v107 series are confidently attributable: 2-3 and 3-2, fractional scores 0.4 and 0.6, for 5/10 games and live score 0.5. Mean opponent-Elo expected score was 0.420817846775332, giving residual +0.079182153224668; rating moved +5.067657806378747. Rank-before evidence is unavailable; current rank is 37. All 104 raw command records succeeded with empty stderr; 100 prefetched matches show no match errors, resignations, crashes, obvious TLEs, exceptions, or submission errors. Historical v105 evidence predates this uncertain reactivation and is excluded. Two series are below the policy minimum of 12, so neither promotion nor score-based rollback is justified.


### Live observation captured — 2026-08-19T12:50:13Z

- Active version: 105
- Report: reports/live-observe-20260819T124953Z


### Live score evaluated — 2026-08-19T11:48:35Z

- Version: 107
- Series: 1
- Score: 0.2
- Adjusted score: -0.186130390418975
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: One rated series is confidently attributed to active v107 after its 2026-08-19T11:17:51Z activation: a 1-4 loss to diverge. Opponent-Elo expected score was 0.386130, yielding residual -0.186130 and rating movement -5.956172. Rank-before evidence is unavailable; current rank is 37. All 104 raw command records succeeded with empty stderr; the active submission is ready, and 100 prefetched match records show no match errors, resignations, crashes, obvious TLEs, or exceptions. One series is below the policy minimum of 12, so neither promotion nor score-based rollback is justified.


### Live observation captured — 2026-08-19T11:46:40Z

- Active version: 107
- Report: reports/live-observe-20260819T114622Z


### Live score evaluated — 2026-08-19T11:22:58Z

- Version: 107
- Series: 0
- Score: None
- Adjusted score: None
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: Active v107 was activated at 2026-08-19T11:17:51Z, but the snapshot contains no ladder series created or completed after activation and no matches attributed to v107. The newest series, 34a80e36-7756-4ef4-813a-13e6b1b2c387, completed 39 seconds before activation and explicitly used v106, so it is excluded. Rating movement is 0.0; opponent-Elo expected score and residual are unavailable without attributed series. All 104 command records succeeded with empty stderr; the active submission is ready, and 100 prefetched match-info records contain no match errors or resign messages. With 0 of the required 12 series and no reliability defect, continue observing.


### Live observation captured — 2026-08-19T11:21:03Z

- Active version: 107
- Report: reports/live-observe-20260819T112045Z


### Candidate activated — 2026-08-19T11:17:51Z

- Version: 107
- Previous/rollback: 101
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260819T111731Z


### Candidate uploaded — 2026-08-19T11:17:50Z

- Candidate: v0044-income-heartbeat-handoff-20260819-1110-eeafad8f
- Version: 107
- Rollback target: 101
- Report: reports/live-deploy-20260819T111731Z


### Automatic rollback — 2026-08-19T11:15:45Z

- Failed candidate version: 106
- Reactivated: 101
- Reason: Active version 106 has 46/95 game wins across 19 confidently attributed rated ladder series after its 2026-08-19T04:16:32Z activation. Raw score 0.4842 is 0.2158 below the known-good 0.70 and below the 0.65 rollback threshold. Mean Elo-expected score was 0.4994, giving residual -0.0152; rating moved -16.6551. The 12-series minimum is met, and all 104 captured command records were successful with no match errors, resign messages, obvious TLEs, exceptions, crashes, or submission errors. This is a clear score regression despite clean reliability.
- Report: reports/live-rollback-20260819T111545Z


### Live score evaluated — 2026-08-19T11:15:45Z

- Version: 106
- Series: 19
- Score: 0.48421052631579
- Adjusted score: -0.015224644720789
- Reliability failures: 0
- Proposed decision: rollback
- Reason: Active version 106 has 46/95 game wins across 19 confidently attributed rated ladder series after its 2026-08-19T04:16:32Z activation. Raw score 0.4842 is 0.2158 below the known-good 0.70 and below the 0.65 rollback threshold. Mean Elo-expected score was 0.4994, giving residual -0.0152; rating moved -16.6551. The 12-series minimum is met, and all 104 captured command records were successful with no match errors, resign messages, obvious TLEs, exceptions, crashes, or submission errors. This is a clear score regression despite clean reliability.


### Live observation captured — 2026-08-19T11:12:30Z

- Active version: 106
- Report: reports/live-observe-20260819T111212Z


### Live observation captured — 2026-08-19T07:16:11Z

- Active version: 106
- Report: reports/live-observe-20260819T071550Z


### Live observation captured — 2026-08-19T06:37:58Z

- Active version: 106
- Report: reports/live-observe-20260819T063735Z


### Live observation captured — 2026-08-19T04:17:34Z

- Active version: 106
- Report: reports/live-observe-20260819T041709Z


### Automatic rollback — 2026-08-19T02:06:00Z

- Failed candidate version: 105
- Reactivated: 101
- Reason: Version 105 has 55 confidently attributed rated series after its 2026-08-18T07:38:47Z activation: 142/275 games (0.5164), 31-24 by series. Elo expectation was 0.5038, yielding mean residual +0.0125; rating rose 22.06 Elo. Nevertheless, the raw score is 0.1836 below the last-known-good score of 0.7000, clearly exceeding the policy's 0.05 rollback margin; no comparable known-good adjusted score exists. All 104 command records succeeded, version 105 is ready, and the 100 prefetched matches were complete with no submission errors, match errors, resignations, obvious TLEs, crashes, or exceptions.
- Report: reports/live-rollback-20260819T020600Z


### Live score evaluated — 2026-08-19T02:06:00Z

- Version: 105
- Series: 55
- Score: 0.5163636363636364
- Adjusted score: 0.01253372683936
- Reliability failures: 0
- Proposed decision: rollback
- Reason: Version 105 has 55 confidently attributed rated series after its 2026-08-18T07:38:47Z activation: 142/275 games (0.5164), 31-24 by series. Elo expectation was 0.5038, yielding mean residual +0.0125; rating rose 22.06 Elo. Nevertheless, the raw score is 0.1836 below the last-known-good score of 0.7000, clearly exceeding the policy's 0.05 rollback margin; no comparable known-good adjusted score exists. All 104 command records succeeded, version 105 is ready, and the 100 prefetched matches were complete with no submission errors, match errors, resignations, obvious TLEs, crashes, or exceptions.


### Live observation captured — 2026-08-19T02:02:23Z

- Active version: 105
- Report: reports/live-observe-20260819T020159Z


### v186 targeted enemy-Core repair-access barrier rejected — 2026-08-18T09:02:00Z

- Tested a bounded offensive-topology change: when an enemy Builder was visible
  near a confirmed enemy Core, the existing six-site barrier cage ranked legal
  Core repair-ring entries adjacent to that Builder before falling back to the
  old nearest-site policy. No Launcher, route/economy, Sentinel timing,
  home-defense, navigation, Store, baseline, package, or live behavior changed.
- Focused cage/nearest-defense tests passed **29/29**, candidate compileall
  passed, smoke was **4/4**, and `make static` retained only the inherited 15
  obsolete imports plus two navigation fast-path assertions. Logs are under
  `reports/iter-v186-repair-access/`.
- The first 15-game all-map screen (seed 153) was **8-7**, command-clean, with
  candidate titanium **72,390 vs 63,990** (`reports/local-20260818T085825Z`).
  The required rotated screen (seed 154) reversed to **6-9**, still 15/15
  command-clean, with titanium **39,170 vs 58,300**
  (`reports/local-20260818T090058Z`).
- v186 is **rejected** after the rotated screen. Temporary attacker/test edits
  were removed; candidate source is byte-identical to immutable v0042. Rollback
  focused tests, compileall, and smoke passed; no 60-game gate, package,
  remote gate, upload, activation, or baseline transition occurred. Full
  record: `experiments/v0042-repair-access-barrier-v186.md`.

### v185 mature-route Splitter redundancy rejected — 2026-08-18T08:50:00Z

- Tested one new logistics capability: after three completed routes, an
  adjacent Builder could replace a verified Core-ring gap with a dynamic-price
  Splitter only when an upstream Conveyor fed it and a second Core-facing
  branch was already present or could be completed immediately. No opening,
  combat, workforce, navigation, baseline, package, or live policy changed.
- Initial focused checks were **30/30**, compileall passed, smoke **4/4**, and
  static retained only the inherited 15 obsolete imports plus two navigation
  assertions. The 15-game all-map screen was **8-7**, command-clean; only two
  candidate Splitters were placed (`reports/local-20260818T083022Z`).
- Repair 1 allowed one empty Core-facing branch to be completed after the
  junction. Focused checks were **31/31**, compileall passed, smoke **4/4**,
  and the screen was **9-6** with no reliability failures. Its required
  60-game release gate was **32-28 (53.33%)**, zero no-delivery/TLE/suspicious
  rows, max p99/peak **1,407/5,101 us**, but weak 1-3 floors on Antler,
  Archipelago, and Icefloe (`reports/local-20260818T083616Z`).
- Repair 2 lowered only the surplus reserve from 80 to 30. Focused checks
  remained **31/31**, compileall passed, smoke **4/4**, and the screen fell to
  **7-8** with one candidate no-delivery row (`reports/local-20260818T084335Z`).
- v185 is **rejected** after both bounded repairs. Temporary source/tests were
  removed; candidate `main.py`, `bot/constants.py`, and `bot/defender.py` are
  byte-identical to immutable v0042. Rollback checks passed **33/33**,
  compileall passed, rollback smoke **4/4**, static remains inherited-red, and
  no package, upload, activation, or baseline transition occurred. Full record:
  `experiments/v0042-splitter-core-redundancy-v185.md`; rollback logs are under
  `reports/iter-v185-splitter-rollback-*`.

### Quick screen reduced to 15 all-map games — 2026-08-18T08:22:00Z

- The routine screen now runs **15 games**, one stratified candidate-A pair for
  each configured map. This removes only the redundant 16th side-order repeat;
  the complete **60-game** release gate remains unchanged with both sides and
  endpoint seeds.
- Schedule tests passed **6/6**. The actual reduced regression was **15/15
  command-clean**, represented all 15 maps, and produced a 7-8 candidate-side
  result against the byte-identical v0042 snapshot. Report:
  `reports/local-20260818T081919Z`.
- Smoke passed **4/4** (`reports/local-20260818T081858Z`). `make static` remains
  exit 2 only from the inherited 15 obsolete test imports and two navigation
  fast-path assertions; log: `reports/policy-quick15-static.log`.
- No bot source, baseline snapshot, package, upload, activation, or live state
  changed. Full record: `experiments/evaluation-policy-quick15.md`; policy
  validation: `reports/evaluation-policy-20260818-quick15.md`.

### v184 short-chain-first opening economy rejected — 2026-08-18T08:09:00Z

- Hypothesis: during the first three completed routes, select ore with an estimated Builder-travel-plus-Core-route cost to improve first delivery; after three routes, keep the local-nearest policy. The quick gate was also reduced modestly from 18 to 16 games while retaining all 15 maps and one seeded side-order repeat; the release gate remains 60 games.
- Allowed bot scope was limited to `bots/candidate/bot/defender.py` and a temporary focused target-selection test. No combat, workforce, route-FSM, Store, baseline, package, or live changes were retained.
- Initial 16-game screen: **4-12**, all maps represented and 16/16 command-clean (`reports/local-20260818T075636Z`). Repair 1: **7-9**, 16/16 command-clean (`reports/local-20260818T075927Z`). Repair 2: **6-10**, 16/16 command-clean (`reports/local-20260818T080334Z`). Neither repair produced a material aggregate edge or reliable first-delivery improvement; no 60-game gate was run.
- Focused tests were 8/8 initially, 9/9 after repair 2, and 38/38 after rollback. Compileall passed throughout. Smoke was 4/4 command-clean for each repair and rollback. `make static` retained only the inherited 15 obsolete-import errors and two navigation fast-path assertions; no new v184 defect remained.
- Candidate Python source was restored byte-identically to immutable v0042 (`reports/iter-v184-rollback-source-diff.txt`); rollback evidence is in `reports/iter-v184-rollback-focused.log`, `reports/iter-v184-rollback-compileall.log`, `reports/iter-v184-rollback-static.log`, and `reports/iter-v184-rollback-smoke.log`. No release package, upload, activation, or baseline transition occurred. Platform v105 and rollback v101 are unchanged.
- Full record: `experiments/v0042-short-chain-first-v184.md`. Durable state records the failed iteration, metrics, report paths, remaining risks, and the 16-game quick-screen policy.

### v183 low-liquidity Gunner retirement promoted and activated — 2026-08-18T07:40:41Z

- Tested one bounded liquidity conversion: after four completed routes, below the next Harvester cost, and with no visible home threat or Core siege beacon, an already-adjacent surplus home Gunner may be legally destroyed; the three-Gunner floor and nearest-responder guard remain.
- Focused coverage passed 23/23; compileall passed; smoke was 4/4 command-clean. make static remains exit 2 only from the inherited 15 obsolete imports and 2 navigation fast-path assertions. Reports: reports/iter-v183-low-liquidity-gunner/final-focused.log, final-compileall.log, final-static.log, final-smoke.log.
- The shortened all-map screen required 18 games and ended 10-8 after two bounded repairs. The 60-game release gate completed 60/60 command-clean at 35-25 (58.33%), no ties, one no-delivery row per side, max p99/peak 1,500/5,361 us. Release report: reports/local-20260818T072713Z; replay analysis: reports/iter-v183-low-liquidity-gunner/release-analysis.json.
- Remote gate match a036c379-15c9-4c1a-ac5b-c25e5bb9881f completed 4-1 (sprint, bridge, crossfire, vault wins; aurora loss); evidence: reports/remote-20260818T073513Z and reports/iter-v183-low-liquidity-gunner/remote-match-info-4.json.
- The fresh v104 live observation was 103/190 games (0.542) across 38 series versus preserved v101 score 0.700, so the guarded operator rolled back v104 to v101 before deployment. Package v0042_low-liquidity-gunner_20260818-0737_eeafad8f.zip (SHA-256 ed2a6bc1c801ef224921bde802f23e692e135bbf6cd507e373149e1289bb26c0) uploaded as platform version 105 and activated for observation; rollback target remains v101. Reports: reports/live-pre-v183-deploy-20260818T073745Z, reports/live-rollback-20260818T073818Z, reports/live-deploy-20260818T073828Z.
- The immutable local baseline and all three evaluation configs now point to bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f. The post-activation snapshot `reports/live-post-v183-activation-20260818T074634Z` confirms v105 is active but has no new rated series yet. Remaining risks are lower aggregate titanium than v0040, weak local fjordgate/midgard floors, and live v105 requiring observation before promotion.


### Candidate activated — 2026-08-18T07:38:47Z

- Version: 105
- Previous/rollback: 101
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260818T073828Z


### Candidate uploaded — 2026-08-18T07:38:47Z

- Candidate: v0042-low-liquidity-gunner-20260818-0737-eeafad8f
- Version: 105
- Rollback target: 101
- Report: reports/live-deploy-20260818T073828Z


### Automatic rollback — 2026-08-18T07:38:18Z

- Failed candidate version: 104
- Reactivated: 101
- Reason: v104 observation: 103/190 game wins (0.542) across 38 series, below last-known-good v101 score 0.700; fresh evidence reports/live-pre-v183-deploy-20260818T073745Z
- Report: reports/live-rollback-20260818T073818Z


### Stratified all-map regression screen adopted — 2026-08-17

- The 54-game regression screen previously used a fixed nine-map subset and
  omitted six maps from early decisions. It now samples **27 side-swapped
  map/seed pairs** from the complete 15-map pool, guarantees every map appears
  at least once, and records a reproducible rotating `screen_seed` in the
  matrix manifest.
- The 210-game release gate remains the complete seven-seed, all-map matrix.
  Schedule generation is covered by three focused tests for map coverage,
  reproducibility/rotation, and invalid pair counts. Implementation:
  `scripts/common.py`, `scripts/run_local_matrix.py`,
  `configs/eval_regression.toml`, and `tests/test_eval_schedule.py`.
  The manifest probe was command-clean with all 15 maps in 27 pairs
  (`reports/local-20260817T212419Z`); unchanged smoke was **4/4**
  (`reports/local-20260817T212439Z`). `make static` retains the known
  inherited result (`reports/v153-screen-policy-static.log`).

### v152 resource-backed idle handoff rejected at long gate — 2026-08-17

- Objective: release a ready, resource-backed dynamic Builder from a targeted
  no-progress task and immediately reassign it to route repair, defense,
  advance, or a verified logistics raid. Scope was dynamic task execution,
  constants, task state initialization, and focused tests; Store protocol,
  chains, navigation, fixed roles, caps, maps, and platform state were
  non-goals. Comparator was immutable v0040.
- Initial handoff screen: **27-27**; repair 1 (two-round trigger): **27-27**;
  repair 2 (funded handoff prefers a verified raid): **30-24**. All screens
  were command-clean; focused suites were 21/21, 21/21, and 22/22; compileall
  and smoke were clean. Reports: `reports/local-20260817T203728Z`,
  `reports/local-20260817T204310Z`, and `reports/local-20260817T204905Z`.
- The full 210-game gate then scored **88-122** versus v0040, command-clean,
  with candidate and comparator delivering in 208/210 games. Replay reliability
  was zero TLE/suspicious output, max p99 **1,491 us**, peak **5,674 us**
  (`reports/local-20260817T205428Z`).
- Status: **rejected at long gate** after the two bounded repairs. Candidate
  source and focused tests were restored byte-identically to v0040; rollback
  focused **20/20**, compileall passed, rollback smoke **4/4**
  (`reports/local-20260817T211734Z`). No archive, package, upload, activation,
  or baseline transition. Detailed record:
  `experiments/v0040-resource-backed-idle-handoff-v152.md`.

### v151 opening Harvester sink marker rejected at long gate — 2026-08-17

- Objective: verify a bounded visible Conveyor path for an opening Harvester
  that already appeared to have an accepting neighbor, so short loops or
  terminal buildings could be reseeded. Scope was defender logic plus focused
  tests; ordinary facing, economy, navigation, combat, workforce, Store, and
  platform state were non-goals. Comparator was immutable v0040.
- Initial screen: **31-23** candidate wins, zero command failures/stderr and
  no candidate no-delivery rows (`reports/local-20260817T194541Z`). Repair 1
  guarded active visible gaps and scored **30-24**; repair 2 treated all gaps
  as unknown and tied **27-27** (`reports/local-20260817T195332Z`,
  `reports/local-20260817T195957Z`). Focused tests were 21/21, then 22/22 for
  repairs; compileall and smoke 4/4 passed; static retained inherited errors.
- The strongest initial variant then ran the full 210-game gate: **99-111**
  against v0040, command-clean, candidate no-delivery **3** versus comparator
  **4**, max p99 **1,476 us**, zero TLE/suspicious output
  (`reports/local-20260817T200602Z`).
- Status: **rejected at long gate** despite the screen win. Candidate Python
  and tests restored byte-identically to v0040; rollback focused **20/20**,
  compileall passed, rollback smoke **4/4** (`reports/local-20260817T202833Z`).
  No package/upload/activation or baseline transition. Detailed record:
  `experiments/v0040-harvester-route-progress-marker-v151.md`.

### v150 Harvester route-verification rejected after two screens — 2026-08-17

- Objective: use the existing homeward repair ranking only for a first-route
  conveyor detour, based on the fresh v102 Atlas/TRRR/Landers live-loss review,
  while preserving v0040's ordinary forward chain behavior. Scope was
  `bots/candidate/bot/defender.py` plus one focused fixture; economy,
  navigation, combat, workforce, Store, and platform state were non-goals.
- Attempt 1 applied the ranking to every pending link: focused **21/21**,
  compileall passed, smoke **4/4**, static retained inherited failures, and
  the 54-game screen was **13-41** versus v0040. Repair 1 limited it to
  non-monotonic detours: **23-31**. Repair 2 limited it to the first pending
  link: **25-29**. All screens were command-clean with zero stderr; no long
  gate was run. Reports: `reports/iter-v150-harvester-route-verification/`,
  `reports/local-20260817T192242Z`, `reports/local-20260817T192903Z`, and
  `reports/local-20260817T193459Z`.
- Status: **rejected after two bounded repairs**. Candidate Python and tests
  are restored byte-identically to v0040; rollback focused **20/20**,
  compileall passed, rollback smoke **4/4**, and static remains the known
  inherited red result. No package/upload/activation or baseline transition.
  Detailed record: `experiments/v0040-harvester-route-verification-v150.md`.

### Live observation captured — 2026-08-17T18:59:23Z

- Active version: 104
- Report: reports/live-observe-20260817T185904Z

### v149 route-seal rejected after two screens — 2026-08-17

- Hypothesis: recognize directed conveyor cycles longer than the existing
  mutual two-cycle check so the opening repair path could recover the
  Glacierkeep seed-149 no-delivery topology. Scope was candidate defender and
  dynamic belt-gap selection plus focused tests; no economy, navigation,
  combat, workforce, Store, or platform changes were retained.
- Attempt 1 added a bounded 64-node visible cycle walk to belt status. Focused
  **22/22**, compileall, and smoke **4/4** passed; the 54-game screen was
  **25-29** versus v0040, one candidate no-delivery, zero command failures/TLEs,
  max p99 1,507 us (`reports/local-20260817T190156Z`).
- Repair 1 restricted the walk to dynamic belt-gap selection. Focused **22/22**,
  compileall, and smoke **4/4** stayed clean; the screen improved to **28-26**
  but remained below v0040’s 36-18 control, with three candidate no-delivery
  rows and max p99 1,473 us (`reports/local-20260817T191038Z`).
- Live v102 losses were also reviewed: Atlas v76, TRRR v40, and Landers v93
  showed early/no delivery, lower Harvester/conveyor conversion, and repeated
  TRRR TLEs. Replays and compact analysis are under
  `reports/live-v102-replays/` and `reports/iter-v149-route-seal/`.
- Status: **rejected after two bounded attempts**; candidate restored
  byte-identically to v0040. Rollback focused **20/20**, compileall passed,
  rollback smoke **4/4** (`reports/local-20260817T191654Z`). No package or
  platform operation was performed for v149. Detailed record:
  `experiments/v0040-route-seal-v149.md`.


### v148 shared route progress promoted locally — 2026-08-17

- Hypothesis: the designated home defender was spending the opening bank on a
  Gunner before any Harvester route completed, creating zero-Harvester shells
  on cramped maps. Scope was one `SLOT_HARVESTER_COUNT` gate in
  `bots/candidate/bot/defender.py` plus focused coverage; navigation, route
  construction, workforce, Store layout, attacker behavior, and platform
  operations were non-goals. Detailed record:
  `experiments/v0040-shared-route-progress-v148.md`.
- Focused tests passed **20/20**, compileall passed, and smoke was **4/4** with
  zero command failures (`reports/iter-v148-shared-route-progress/` and
  `reports/local-20260817T182520Z`). `make static` retained the inherited
  15 obsolete-module import errors and two navigation fast-path assertions.
- The 54-game checkpoint scored **36-18** against v0039 (the control's prior
  screen was 30-24), with zero command failures, zero candidate no-delivery
  rows, and max p99 1,498 us (`reports/local-20260817T182542Z`).
- The 210-game gate scored **120-90 (57.1%)** against v0039, with zero command
  failures/TLEs/suspicious output, candidate no-delivery **1** versus
  comparator **2**, and max candidate p99 **1,615 us**. One Glacierkeep seed
  149 loss still built four Harvesters and 125 disconnected conveyors without
  delivery; its topology audit is the next hypothesis
  (`reports/local-20260817T183119Z`,
  `reports/iter-v148-shared-route-progress/long-replay-analysis.json`).
- Status: **promoted as the moving local baseline**. Immutable snapshot and
  package: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`,
  archive SHA-256 `f38a563bde5acbd5d02da9b4c6acaa82da8bf0fc7efbc5e1672cc2addcce576e`.
  All three evaluation configs now compare against v0040. The archive was
  uploaded as platform version **104** (`8ebb41eb-fe2f-4402-af1a-ea4051b53b6c`);
  the platform reports it `ready` and active, and the observation snapshot is
  `reports/live-observe-20260817T185904Z`.

### v147 opening route-pressure rejected — 2026-08-17

- Hypothesis: multiple pre-income Builders were spending the opening bank on
  disconnected partial Harvester chains; reserve new opening Harvesters for a
  shared route owner, with one low-balance repair variant. Scope stayed in
  `bots/candidate/bot/defender.py`, its focused test, reports, and durable
  metadata; no baseline/package/platform operation occurred.
- Initial variant: focused **20/20**, compileall passed, smoke **4/4**, and
  static retained the inherited 15 obsolete imports plus two navigation
  assertions. The 54-game screen was **29-25**, 212,210-197,920 Ti, with
  candidate no-delivery **3** versus comparator **0**
  (`reports/local-20260817T180645Z`; analysis
  `reports/iter-v147-route-pressure/screen-analysis.json`).
- Repair 1 restricted the owner gate to balances below one Harvester plus
  three Conveyor costs. Focused **20/20**, compileall, and smoke **4/4** stayed
  clean; the screen regressed to **28-26**, 200,220-205,930 Ti, and no-delivery
  **1/1** (`reports/local-20260817T181418Z`; analysis
  `reports/iter-v147-route-pressure/repair1-analysis.json`).
- Status: **rejected after two bounded attempts**; no 210-game gate or package
  was run. Candidate production Python was restored byte-identically to v0039;
  rollback focused tests were **18/18**, compileall passed, rollback smoke was
  **4/4** (`reports/local-20260817T181959Z`), and v0039 remains the comparator.
  Detailed record: `experiments/v0039-route-sink-pressure-v147.md`.

### v146 post-route Harvester sink repair promoted locally — 2026-08-17

- Hypothesis: `_try_reconnect_orphaned_harvester` incorrectly considered any
  adjacent friendly Conveyor/Splitter an accepting outlet, including a
  Conveyor facing into the Harvester. Direction-aware sink validation plus
  post-route eligibility was scoped to `bots/candidate/bot/defender.py` and
  `tests/test_candidate_nearest_defense.py`; no platform operation occurred.
- Focused tests were **18/18**, compileall passed, smoke was **4/4** at
  `reports/local-20260817T172343Z`, and `make static` retained the inherited
  exit 2 from 15 obsolete imports plus two navigation assertions.
- The 54-game screen scored **30-24**, with 223,490 vs 209,840 collected Ti,
  zero candidate no-delivery vs one comparator, zero TLE/suspicious output,
  and max p99/peak 1,490/5,590 us (`reports/local-20260817T172407Z`).
- The 210-game gate scored **121-89** (57.6%), with 1,027,120 vs 852,170
  collected Ti. Replay analysis was reliability-clean: zero TLE/suspicious
  output, max p99/peak 1,476/5,651 us, three no-delivery games per side,
  mean first delivery 32.3 vs 38.0 turns
  (`reports/local-20260817T172948Z`,
  `reports/iter-v146-post-route-sink/long-replay-analysis.json`).
- Status: **locally promoted** as immutable
  `bots/versions/v0039_post-route-sink-v146_20260817-1752_eeafad8f`; the
  v0039 package SHA256 is
  `14a6f24bf37fd8b95ff98387d1bea6011ed7e6defaed3355bf1c15e9d9c28282`.
  `configs/eval_smoke.toml`, `eval_regression.toml`, and `eval_matrix.toml`
  now compare against v0039. v0038 remains the prior rollback snapshot; no
  upload, activation, or live-state change was made. Detailed record:
  `experiments/v0038-post-route-sink-v146.md`.

### v145 first-route funding rejected — 2026-08-17

- Hypothesis: reserve one dynamic Conveyor cost before a low-balance opening
  Harvester, except when a visible friendly Conveyor/Splitter sink already
  exists. Scope was limited to `bots/candidate/bot/defender.py`, its focused
  test, reports, and durable metadata; no navigation, combat, Store layout,
  baseline, package, upload, activation, or live-state change.
- Initial screen: **25-29**, 184,080-224,870 collected Ti
  (`reports/local-20260817T164139Z`). Repair 1 improved the 54-game screen to
  **30-24**, 203,670-206,630 Ti (`reports/local-20260817T164834Z`).
- The 210-game release-sized matrix remained **99-111** (47.1%),
  902,520-895,540 collected Ti, with five candidate no-delivery games versus
  zero comparator no-delivery games. Replay analysis was reliability-clean:
  zero TLE/suspicious output, max p99/peak 1,496/5,538 us
  (`reports/local-20260817T165424Z`,
  `reports/iter-v145-route-funding/long-replay-analysis.json`).
- Focused tests were 17/17 initially, 18/18 for repair 1, and 16/16 after
  rollback; compileall passed throughout; smoke was 4/4 for both variants and
  rollback. `make static` retained the inherited exit 2 from 15 obsolete
  imports plus two navigation assertions.
- Status: **rejected after one bounded repair and the long gate**. Candidate
  production Python is byte-identical to immutable
  `bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f`; detailed
  record: `experiments/v0038-route-funding-v145.md`.

### v143 route-sentry response rejected — 2026-08-17

- Hypothesis: after a completed route, a Dynamic Builder already close to our
  Harvester should answer a visible enemy Builder locally, reusing the
  existing nearest `TASK_HOME_THREAT` strike path. Allowed files were
  `bots/candidate/bot/constants.py`, `bots/candidate/bot/dynamic.py`, and
  `tests/test_candidate_nearest_defense.py`; no navigation, Store, workforce,
  baseline, package, upload, activation, or live-state change was made.
- Initial 54-game screen: **28-26**, 193,060-176,500 Ti, candidate no-delivery
  1 versus comparator 0, zero command/TLE/suspicious-output failures, max
  p99/peak 1,390/2,974 us (`reports/local-20260817T154912Z`). Repair 1
  narrowed the trigger and restored the control's **30-24** but did not beat
  it (206,200-184,000 Ti; no-delivery 0/2; max p99/peak 1,514/4,260 us;
  `reports/local-20260817T155802Z`). Repair 2 required true adjacency and
  scored **29-25** (175,140-166,600 Ti; no-delivery 1/1; max p99/peak
  1,319/5,736 us; `reports/local-20260817T160350Z`). All 54-game runs were
  command-clean with zero TLE/suspicious-output flags.
- Focused tests were 26/26 for the initial candidate and both repairs;
  compileall passed; each smoke was 4/4. `make static` retained the inherited
  exit 2 from 15 obsolete imports plus two navigation fast-path assertions.
  After rollback, focused tests were 16/16, compileall passed, and smoke was
  4/4 command-clean (`reports/iter-v143-route-sentry/rollback-*`,
  `reports/local-20260817T160905Z`).
- Status: **rejected after two bounded repairs**. Candidate production Python
  is byte-identical to immutable baseline
  `bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f`; no full
  matrix, package, upload, activation, or baseline transition occurred.
  Detailed record: `experiments/v0038-route-sentry-v143.md`.

### v144 queued-ore ownership rejected — 2026-08-17

- Hypothesis: queued Store ore lacked the visible-ore branch's nearest-Builder
  ownership rule, causing stale/frontier pileups. Allowed files were
  `bots/candidate/bot/defender.py` and `tests/test_candidate_nearest_defense.py`;
  no workforce, route FSM, navigation, combat, Store layout, baseline,
  package, upload, activation, or live-state change was made.
- Initial 54-game screen: **24-30**, 155,050-220,820 Ti, no-delivery 1/1,
  zero command/TLE/suspicious-output failures, max p99/peak 1,539/4,809 us
  (`reports/local-20260817T162006Z`). Repair 1 gated ownership until one
  completed route and scored **26-28**, 196,510-174,000 Ti, no-delivery 1/0,
  zero reliability flags, max p99/peak 1,427/5,091 us
  (`reports/local-20260817T162533Z`).
- Focused tests were 17/17 for the initial variant and repair; compileall
  passed; each smoke was 4/4. `make static` retained the inherited exit 2
  from 15 obsolete imports plus two navigation fast-path assertions. Rollback
  focused tests were 16/16, compileall passed, and smoke was 4/4 command-clean
  (`reports/iter-v144-queued-ore/rollback-*`,
  `reports/local-20260817T163037Z`).
- Status: **rejected after one bounded repair**. Candidate production Python
  is byte-identical to immutable baseline
  `bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f`; no full
  matrix, package, upload, activation, or baseline transition occurred.
  Detailed record: `experiments/v0038-queued-ore-ownership-v144.md`.

### Candidate activated — 2026-08-16T11:39:31Z

- Version: 102
- Previous/rollback: 101
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260816T113911Z


### Candidate uploaded — 2026-08-16T11:39:31Z

- Candidate: v0036-seeded-route-safety-eeafad8f
- Version: 102
- Rollback target: 101
- Report: reports/live-deploy-20260816T113911Z


### v0036 seeded-route safety release candidate — 2026-08-16T11:37:37Z

- Guarded seeded-route recovery against unseen, empty, enemy, or non-Conveyor replacement tiles before get_direction; stale state returns through _end_seeded_route to SCOUT. Focused route plus enemy-Core cage suites passed 9/9, static contract 8/8, and candidate compileall passed.
- Smoke was 4/4 command-clean (reports/local-20260816T105124Z); exact v101 screens were 9/12 and 7/12 (reports/local-20260816T105150Z and reports/local-20260816T105317Z); Continue54 was 31/54 with zero command failures (reports/local-20260816T105457Z).
- Full 210-game current-map gate was 122-88 (58.1%) with 1,238,420 versus 1,096,410 Ti, five versus seven no-delivery rows, zero command failures/TLE/suspicious output, max p99 1,437 us, and peak callback 5,912 us (reports/local-20260816T110158Z; summary reports/iter-seeded-route-safety-v0036/full-analysis.json).
- Pinned remote gate was 2-3 but reliability-clean (reports/remote-20260816T113107Z); the unrated test was ephemeral only. Local package v0036_seeded-route-safety_20260816-1134_eeafad8f has SHA-256 676cbe6c340011ca9dc3ef460ad40fc81827f79d9438336329b446dfff769cb4.
- Status: local release candidate; no upload, activation, or live-state operation. Known risks are remote 2-3, antler/yulerune 6-8 floors, inherited make static failures, and pre-existing dirty-tree source differences versus immutable v0035.


### Live candidate promoted — 2026-08-16T11:36:36Z

- Version: 101
- Live score: 0.7
- Adjusted score: None
- Reason: User-designated current baseline v101; fresh status shows 7-3 recent record, rating 1526.53, rank 39; preserve as rollback before v0036 deployment


### Live observation captured — 2026-08-16T11:35:47Z

- Active version: 101
- Report: reports/live-observe-20260816T113527Z


### Live observation captured — 2026-08-16T01:04:52Z

- Active version: 101
- Report: reports/live-observe-20260816T010429Z


### Live observation captured — 2026-08-15T21:42:22Z

- Active version: 101
- Report: reports/live-observe-20260815T214157Z


### Live observation captured — 2026-08-15T21:18:38Z

- Active version: 101
- Report: reports/live-observe-20260815T211812Z


### Candidate activated — 2026-08-15T21:17:00Z

- Version: 101
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260815T211641Z


### Candidate uploaded — 2026-08-15T21:17:00Z

- Candidate: v0035-enemy-core-cage-eeafad8f
- Version: 101
- Rollback target: 72
- Report: reports/live-deploy-20260815T211641Z


### Live observation captured — 2026-08-15T20:04:05Z

- Active version: 100
- Report: reports/live-observe-20260815T200347Z


### Automatic rollback — 2026-08-15T19:52:15Z

- Failed candidate version: 100
- Reactivated: 72
- Reason: v100 live replay audit found 27 TLE events in two losses (p99 up to 7.622 ms, peak above 10 ms); reliability gate overrides +17.99 Elo drift
- Report: reports/live-rollback-20260815T195215Z


### Live observation captured — 2026-08-15T19:50:26Z

- Active version: 100
- Report: reports/live-observe-20260815T195008Z


### Live observation captured — 2026-08-15T12:16:30Z

- Active version: 100
- Report: reports/live-observe-20260815T121610Z


### v0066 frontier fallback repair rejected — 2026-08-15

- Objective: retain v0065's unseen-frontier preference while falling back to the prior visible exploration set when no unseen harvestable-area tile exists. Experiment record: `experiments/v0066-frontier-fallback-repair.md`.
- Focused tests passed 9/9 before the screen and 7/7 after rollback; compileall passed; smoke was 4/4 command-clean; `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports. Logs are under `reports/iter-frontier-fallback-repair-v0066/`.
- 54-game screen: **28/54 (51.9%)** candidate wins versus 26 comparator wins, collection 223,220 versus 222,530 (1.0031x), one candidate no-delivery row versus none for the comparator, zero TLE/suspicious output/command failures, p99 max 1,300 us and peak callback 2,874 us (`reports/local-20260814T222535Z`, analysis `reports/iter-frontier-fallback-repair-v0066/screen-analysis.json`).
- Status: **rejected at the screen gate**; the margin was not a strict clean edge and delivery was worse, so no 210-game matrix was run. Candidate sources were restored byte-identically to immutable v0031 (`reports/iter-frontier-fallback-repair-v0066/revert-diff.txt`); rollback logs are in the same directory. No package, upload, activation, or baseline transition occurred.

### v0065 unseen-frontier prospecting rejected — 2026-08-15

- Objective: make no-ore prospecting skip already-visible empty tiles so economic builders reveal new terrain instead of spending movement rounds without finding ore. Experiment record: `experiments/v0065-unseen-frontier-prospecting.md`.
- Focused tests passed 8/8 before the gate and 7/7 after rollback; compileall passed; smoke was 4/4 command-clean; `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports. Logs are under `reports/iter-unseen-frontier-prospecting-v0065/`.
- 54-game screen: **31/54 (57.4%)** candidate wins versus 23 comparator wins, collection 242,400 versus 224,380 (1.0803x), zero no-delivery/TLE/suspicious-output/command failures; p99 max 1,319 us and peak callback 2,543 us (`reports/local-20260814T215135Z`, analysis `reports/iter-unseen-frontier-prospecting-v0065/screen-analysis.json`).
- Full 21-map/5-seed/side-swapped gate: **106/210 (50.5%)** candidate wins versus 104 comparator wins, collection 946,510 versus 918,940 (1.0300x), six candidate no-delivery rows versus three comparator rows, zero TLE/suspicious output, p99 max 1,544 us, peak callback 3,166 us (`reports/local-20260814T215823Z`, analysis `reports/iter-unseen-frontier-prospecting-v0065/full-analysis.json`). v0031's retained baseline result was 114/210.
- Status: **rejected at the full gate**; the screen edge did not survive the full map distribution and delivery floor. Candidate sources were restored byte-identically to immutable v0031 (`reports/iter-unseen-frontier-prospecting-v0065/revert-diff.txt`); rollback logs are in the same directory. No package, upload, activation, or baseline transition occurred.

### v0064 locality-ranked raid recovery rejected — 2026-08-14

- Objective: replace v0061's fixed belt-first post-raid handoff with a deterministic nearest visible belt-gap or damaged-home repair. Experiment record: `experiments/v0064-locality-ranked-raid-recovery.md`.
- Focused tests passed 8/8 before the matrix and 7/7 after rollback; candidate compileall passed; smoke was 4/4 command-clean; `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports. Logs are under `reports/iter-locality-ranked-raid-recovery-v0064/`.
- Six-map screen: **19/36 (52.8%)**, collection 205,940 versus 177,620 (1.1594x), zero no-delivery/TLE/suspicious-output/command failures; p99 max 1,307 us and peak callback 2,673 us (`reports/local-20260814T211424Z`).
- Full 21-map/5-seed/side-swapped gate: **103/210 (49.0%)** candidate wins versus 107 comparator wins, collection 920,820 versus 948,170 (0.9712x), four candidate no-delivery rows versus one comparator row, zero TLE/suspicious output, p99 max 1,531 us, peak callback 3,246 us (`reports/local-20260814T211938Z`, analysis `reports/iter-locality-ranked-raid-recovery-v0064/full-analysis.json`).
- Status: **rejected at the full gate**; v0064's local-distance handoff did not preserve v0031's win-rate or delivery floor. Candidate sources were restored byte-identically to immutable v0031 (`reports/iter-locality-ranked-raid-recovery-v0064/revert-diff.txt`); rollback focused/smoke logs are in the same report directory. No package, upload, activation, or baseline transition occurred.

### v0064 locality-ranked raid recovery ready — 2026-08-14

- The v0063 resource-backed economy floor was rejected at the screen gate and reverted; v0031 remains the comparator. The next hypothesis changes only the v0061 raid terminal handoff: choose the nearest visible damaged-home repair or belt-gap repair rather than hard-coding belt-first, so a raider does not walk across the map for a lower-value repair.
- No v0064 code or test result exists yet. Its allowed files are `bots/candidate/bot/dynamic.py`, `tests/test_candidate_nearest_defense.py`, this experiment record, `UPDATES.md`, and `state/project_state.json`; fixed attackers, spending, navigation, Core spawning, and platform state are non-goals.

### v0063 resource-backed economy floor rejected — 2026-08-14

- Objective: make the four-route economy lock conditional on actual bank pressure, reserving only a harvester, two conveyor seed tiles, and the fixed 80-Ti attack reserve. Rich-bank workers could still hijack/raid. Experiment record: `experiments/v0063-resource-backed-economy-floor.md`.
- Focused tests passed 8/8, compileall passed, smoke was 4/4 command-clean, and `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports; static contract checks passed. Logs are under `reports/iter-resource-backed-economy-floor-v0063/`.
- Six-map screen: **18/36 (50.0%)**, collection 169,580 versus 171,480 (0.9889x), zero no-delivery/TLE/suspicious-output/command failures; p99 max 1,264 us and peak callback 2,671 us (`reports/local-20260814T210650Z`). String fell to 1/6 and Fjord to 2/6.
- Status: **rejected at the screen gate**. Candidate sources were reverted byte-identically to v0031 (`reports/iter-resource-backed-economy-floor-v0063/revert-diff.txt`); no full matrix, package, upload, activation, or baseline transition occurred. The next hypothesis must target a different failure mode than economy-floor ordering.

### v0062 staged economy-floor contract rejected — 2026-08-14

- Objective: keep dynamic builders on harvest/exploration until four completed routes, while preserving home threats and critical belt repair as higher priorities. The experiment record is `experiments/v0062-economy-floor-contract.md`; only `constants.py`, `dynamic.py`, and its focused test changed.
- Focused tests passed 8/8, compileall passed, smoke was 4/4 command-clean, and `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports; static contract checks passed. Logs are under `reports/iter-economy-floor-contract-v0062/`.
- Six-map screen: **22/36 (61.1%)**, collection 215,670 versus 203,470 (1.0600x), zero no-delivery, TLE, suspicious-output, or command failures; p99 max 1,282 us and peak callback 2,616 us (`reports/local-20260814T203114Z`).
- Full 21-map/5-seed/side-swapped gate: **102/210 (48.6%)** candidate wins versus 108 comparator wins, collection 933,810 versus 942,010 (0.9913x), three candidate no-delivery rows, zero TLE/suspicious output, p99 max 1,463 us, and peak callback 3,362 us (`reports/local-20260814T203650Z`, analysis `reports/iter-economy-floor-contract-v0062/full-analysis.json`). Atoll, Runestone, Showdown, and Vault each fell to 3/10.
- Status: **rejected at the full reliability/win-rate/map/collection gate** despite the screen edge. The candidate was reverted and is byte-identical to immutable v0031 (`reports/iter-economy-floor-contract-v0062/revert-diff.txt`); no package, upload, activation, or baseline transition occurred. The next hypothesis must make the economy floor resource/state adaptive rather than unconditional.

### v0061 bounded raid-recovery pulse promoted locally — 2026-08-14

- Objective: when a dynamic raid target is confirmed gone, hand the builder to one visible belt-gap or damaged-home repair before returning to the normal task pool. The change is bounded to the raid terminal transition; fixed opening attackers, target scoring, and CHAIN mode are unchanged. Experiment record: `experiments/v0061-bounded-raid-recovery-pulse.md`.
- Focused tests passed 7/7, candidate compileall passed, smoke was 4/4 command-clean, and `git diff --check` passed. `make static` retains the inherited exit-2 result from 15 obsolete imports; its contract checks still pass. Logs are under `reports/iter-bounded-raid-recovery-pulse-v0061/`.
- Six-map screen: **26/36 (72.2%)**, collection 211,480 versus 176,300 (1.1995x), zero command/runtime failures, no-delivery rows, TLEs, or suspicious output; p99 max 1,354 us and peak callback 3,151 us (`reports/local-20260814T195312Z`).
- Full 21-map/5-seed/side-swapped gate: **114/210 (54.3%)** candidate wins versus 96 comparator wins, collection 944,340 versus 888,240 (1.0632x), 210/210 command-clean, two candidate no-delivery rows, zero TLE/suspicious output, p99 max 1,444 us, peak callback 2,761 us (`reports/local-20260814T195823Z`, analysis `reports/iter-bounded-raid-recovery-pulse-v0061/full-analysis.json`). No map had zero candidate wins; the screen's prior weak-map profile improved.
- Status: **promotion 1 accepted locally** on paired win-rate improvement with clean reliability, delivery, collection, and map floors. Candidate archived as `bots/versions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f`; package SHA-256 is `d58bcc244d607573375feb666f80179bac96fba2fac93127f70a5e799293aecc` (`artifacts/submissions/v0031_bounded-raid-recovery-pulse_20260814-2025_eeafad8f.zip`). Evaluation configs and the moving baseline now point to v0031. No upload or activation was performed; remaining risk is low-frequency Sweden/route-conversion variance.

### v0060 urgent route-health preemption rejected — 2026-08-14

- Objective: allow visible home threats and broken conveyor outputs to interrupt a stale dynamic task before the normal commitment floor. The experiment changed only `_maybe_switch_task` and its focused test; no target scoring, route FSM, raid, Core, or spending policy changed. Record: `experiments/v0060-urgent-route-health-preemption.md`.
- The candidate was screened after focused tests, compileall, smoke, and diff checks passed; `make static` retained the inherited 15 obsolete-import errors. Screen report and preserved analysis: `reports/local-20260814T194535Z`, `reports/iter-urgent-route-health-preemption-v0060/screen-analysis.json`.
- Screen result: **14/36 (38.9%)**, collection 160,130 versus 199,950 (0.8009x), zero command failures, no-delivery rows, TLEs, or suspicious output; p99 max 1,339 us and peak 2,715 us.
- Status: **rejected at screen gate**; immediate preemption disrupted the existing task FSM. The change was reverted and the candidate Python tree is byte-identical to v0030 (`/tmp/v0060-revert-diff.txt`). No full matrix, package, upload, activation, or baseline transition occurred.

### v0059 shell-funded logistics pulse rejected — 2026-08-14

- Objective: after five completed routes and an observed three-sentinel shell, let fixed attackers take a bounded visible logistics raid before returning to the direct Core lane. This was a structural role handoff, not an opening threshold change. Experiment record: `experiments/v0059-shell-funded-logistics-pulse.md`.
- Candidate files were `bots/candidate/bot/attacker.py` and `tests/test_candidate_nearest_defense.py`; the temporary pulse and test were reverted. The candidate Python tree is byte-identical to v0030 (`/tmp/v0059-revert-diff.txt`).
- Focused tests passed 7/7 before the gate; after rollback 6/6, compileall passed, smoke was 4/4 command-clean, and `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports. Reports are under `reports/iter-shell-funded-logistics-pulse-v0059/`.
- Six-map screen: **21/36 (58.3%)**, collection 191,840 versus 177,420 (1.0813x), zero command failures, no-delivery rows, TLEs, or suspicious output (`reports/local-20260814T190952Z`). The full 210-game gate then fell to **92/210 (43.8%)**, collection 902,020 versus 932,860 (0.9669x), with four candidate no-delivery rows; runtime remained clean, p99 max 1,439 us and peak 3,330 us (`reports/local-20260814T191448Z`, `reports/iter-shell-funded-logistics-pulse-v0059/full-analysis.json`).
- Status: **rejected at the full gate**. The late raid disrupted route conversion on the broad matrix despite a strong protected-map screen; no package, upload, activation, or baseline transition occurred. v0030 remains the moving-best baseline.

### v0058 aspect-aware Core search rejected — 2026-08-14

- Objective: let the designated second attacker search symmetry-derived Core counterparts in an aspect-aware order while preserving the first attacker's direct lane. No economy, route, workforce, ammo, turret, or confirmed-intel policy changed. Experiment record: `experiments/v0058-aspect-aware-core-search.md`.
- Candidate files were `bots/candidate/main.py`, `bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and `tests/test_candidate_core_search.py`; all temporary changes were reverted after review. The candidate Python tree is byte-identical to `bots/versions/v0030_loaded-raid-best_20260814-1109_eeafad8f` (`/tmp/v0058-revert-diff.txt`).
- Focused tests passed 11/11, compileall passed, smoke was 4/4 command-clean, and `git diff --check` passed. `make static` retained the inherited exit-2 result from 15 obsolete imports; its contract tests passed. Logs and the preserved full analysis are under `reports/iter-aspect-aware-core-search-v0058/`.
- The six-map screen was 21/36 (58.3%), collection 213,690 versus 167,750 (1.2739x), with zero command failures, no-delivery rows, TLEs, or suspicious output (`reports/local-20260814T183048Z`). The strict full matrix was command-clean but only **108/210 (51.4%)**, with 1,016,340 versus 959,640 titanium (1.0591x); maximum p99 was 1,500 us and peak callback 3,241 us (`reports/local-20260814T183544Z`, `reports/iter-aspect-aware-core-search-v0058/full-analysis.json`).
- Status: **rejected at the full win-rate/map gate**; the screen edge did not survive the full matrix and did not establish a sufficiently strong moving-best promotion. No package, upload, activation, or baseline transition occurred; v0030 remains the baseline. The next hypothesis must alter conversion/defense behavior rather than search order alone.

### v0057 direct-probe Core search rejected — 2026-08-14

- Objective: preserve the direct 180-degree lane for the designated second attacker and only begin alternate symmetry search after a bounded direct probe. This was intended to retain correct-map pressure while recovering non-mirror layouts; no economy, route, ammo, workforce, or turret policy changed. Experiment record: `experiments/v0057-confirm-before-core-search.md`.
- Candidate files were `bots/candidate/main.py`, `bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and `tests/test_candidate_core_search.py`; all were reverted after the screen. The candidate Python tree is byte-identical to v0030.
- Focused tests passed 10/10, compileall passed, smoke was 4/4 command-clean, and `git diff --check` passed. `make static` remains the inherited exit-2 failure from 15 obsolete imports. Logs are under `reports/iter-confirm-before-core-search-v0057/` and smoke report `reports/local-20260814T182105Z`.
- Six-map screen against v0030: **15/36 (41.7%)**, collection 156,590 versus 164,800 (0.9502x), zero command failures, no-delivery rows, TLEs, or suspicious output; report `reports/local-20260814T182140Z`. Map results: Strait 4/6, Sweden 2/6, Twins 3/6, String 3/6, Vault 2/6, Fjord 1/6.
- Status: **rejected at screen gate**; no full matrix, package, upload, activation, or baseline transition. v0030 remains the moving-best baseline.

### v0056 dual-attacker core search rejected — 2026-08-14

- Objective: stop both fixed attackers from committing to the same unverified 180-degree Core guess. Only the designated second attacker visited bounded vertical, horizontal, and rotational counterparts; confirmed Core intel immediately ended the search. No economy, route, ammo, workforce, sentinel-safety, or turret thresholds changed. Experiment record: `experiments/v0056-dual-core-search.md`.
- Files changed for the candidate were `bots/candidate/main.py`, `bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and `tests/test_candidate_core_search.py`; all were reverted after review. The candidate Python tree is byte-identical to v0030 (`reports/iter-dual-core-search-v0056/revert-focused.log` and the source comparison).
- The three new core-search tests and six attacker-regression tests passed before the gate; the restored candidate's focused suite is 6/6 (`reports/iter-dual-core-search-v0056/focused.log`, `reports/iter-dual-core-search-v0056/revert-focused.log`); compileall passed; smoke was 4/4 (`reports/local-20260814T174304Z`). `make static` remains the inherited exit-2 failure from 15 obsolete imports (`reports/iter-dual-core-search-v0056/static.log`); static contract tests passed within that run. `git diff --check` passed.
- Six-map screen: 20/36 (55.6%), up from v0055's 19/36, with zero command failures; report `reports/local-20260814T174347Z`. Full 21-map/5-seed gate: **115/210 (54.8%)**, only +3 wins over v0055's 112/210, but candidate collection fell from 1,003,930 to 987,640, no-delivery rows rose 2→4, and map floors regressed on Bridge (6→3), Crossfire (7→5), Fjord (7→6), Runestone (7→5), Vault (8→5), and others. Full report `reports/local-20260814T174901Z`; replay analysis `reports/iter-dual-core-search-v0056/full-analysis.json`.
- Reliability stayed command-clean: zero failures/TLEs/suspicious output, max p99 1,507 us, peak callback 3,139 us. Status: **rejected at the full reliability/map/collection gate**; v0030 remains the moving-best baseline. No package, upload, activation, or baseline transition.

### v0055 orphaned-Harvester reconnect rejected — 2026-08-14

- Objective: reconnect an owned Harvester after its complete outbound belt was destroyed. The implementation added a local orphan detector, guarded it until the first delivery/mid-game, skipped sources with a nearby Builder, and reused the existing seeded-route FSM after placing one replacement conveyor.
- Weak-map screen against moving best v0030: 19/36 (52.8%), with zero command failures, TLEs, or suspicious outputs. Map results: Strait 3/6, Sweden 3/6, Twins 3/6, String 1/6, Vault 4/6, Fjord 5/6. Candidate collection was 183,560 versus 190,700 (0.9626x); report `reports/local-20260814T170531Z`, replay analysis `reports/iter-orphaned-harvester-v0055/screen-analysis.json`.
- Full 21-map gate: **112/210 (53.3%)**, below v0030's retained result. Collection was 1,003,930 versus 979,790 (1.0246x), but two candidate rows had no delivery and map floors regressed on Quarry (3/10), Showdown (3/10), Sweden (3/10), and Skerry (4/10). Report `reports/local-20260814T171034Z`, replay analysis `reports/iter-orphaned-harvester-v0055/full-analysis.json`.
- Reliability stayed clean: zero command failures, TLEs, or suspicious outputs; maximum p99 was 1,476 us and peak callback 4,010 us. Focused tests 17/17 and compileall passed before rollback; restored focused tests and compileall passed (`reports/iter-orphaned-harvester-v0055/revert-focused.log`, `revert-compile.log`). Smoke was 4/4 after rollback (`revert-smoke.log`); `make static` remains the inherited exit-2 obsolete-import failure (`revert-static.log`).
- All bot edits were reverted; candidate Python sources are byte-identical to v0030. No package, upload, activation, or baseline transition. Status: rejected on the full win-rate gate. Experiment record: `experiments/v0055-orphaned-harvester-repair.md`.

### v0053 stalled-builder recovery watchdog rejected — 2026-08-14

- Objective: recover a Builder that repeatedly finished a ready turn without a legal action or move, while protecting an in-progress conveyor route. The bounded watchdog cleared only local stale intent after eight consecutive stationary ready turns; economy, combat priorities, navigation, and map logic were unchanged.
- Weak-map screen against the moving best v0030 (Strait, Sweden, Twins, String, Vault, Fjord; three seeds and side swaps): **18/36 (50.0%)**, a tie rather than an improvement. Map results were Strait 3/6, Sweden 4/6, Twins 2/6, String 3/6, Vault 4/6, Fjord 2/6. Candidate collection was 188,010 versus 194,080 for the comparator (0.9687x). Matrix report: `reports/local-20260814T151731Z`; replay analysis: `reports/iter-stalled-builder-v0053-screen-analysis.json`.
- Reliability was clean: zero command failures, TLEs, or suspicious outputs; maximum replay p99 was 1,387 us and peak callback 3,178 us. Smoke was 4/4 command-clean (`reports/iter-stalled-builder-v0053/smoke.log`); focused tests were 17/17 before rollback and 15/15 after rollback (`reports/iter-stalled-builder-v0053/revert-focused.log`); candidate compileall passed (`reports/iter-stalled-builder-v0053/revert-compile.log`). `make static` remains the inherited exit-2 failure from 15 obsolete imports (`reports/iter-stalled-builder-v0053/static.log`).
- The watchdog changes were reverted, the candidate Python tree was restored byte-identically to v0030, and no package/upload/activation occurred. Status: rejected at the screen gate; v0030 remains the moving best baseline. Experiment record: `experiments/v0053-stalled-builder-recovery.md`.

### Moving-best baseline policy reaffirmed — 2026-08-14

- The comparator is a moving pointer to the strongest reliability-clean local bot by win rate. Every accepted candidate must be archived immutably, then `baseline_path`, the evaluation configs, and the next experiment's comparator are repointed to that snapshot.
- A rejected candidate never changes the pointer. The current best remains `bots/versions/v0030_loaded-raid-best_20260814-1109_eeafad8f`; v0049, v0050, and v0051 were rejected at their screen gates, so no baseline transition is warranted yet.
- This policy supersedes any stale fixed-baseline wording; collection is diagnostic, while win rate and reliability/map floors decide promotion.

### v0051 dynamic sentinel-pressure claim rejected — 2026-08-14

- Hypothesis: after five completed routes and with a sentinel deficit, the nearest dynamic builder should claim an advance/sentinel lane before routine harvesting, while other dynamic builders retain economy and repair priorities.
- Weak-map screen (Strait, Sweden, Twins, String, Vault, Fjord; three seeds and side swaps): 17/36 (47.2%) against v0030, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-sentinel-pressure-v0051-screen-analysis.json`; matrix report: `reports/local-20260814T150313Z`.
- The temporary `_sentinel_pressure_task` branch in `bots/candidate/bot/dynamic.py` was reverted. Revert checks: focused unittest 15/15 (`reports/iter-sentinel-pressure-v0051-revert-unittest.log`), compileall passed (`reports/iter-sentinel-pressure-v0051-revert-compile.log`), smoke 4/4 (`reports/iter-sentinel-pressure-v0051-revert-smoke.log`), and the source diff against v0030 was empty. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-sentinel-pressure-v0051-revert-static.log`).
- Status: rejected at the screen gate; no full matrix, package, upload, activation, or baseline transition. v0030 remains the best local baseline.

### v0050 first-attacker opening-economy handoff rejected — 2026-08-14

- Hypothesis: let the first fixed attacker run the defender economy loop until one completed route, then return it to the direct sentinel/core lane, so the opening combat floor cannot consume the only early route worker.
- Weak-map screen (Sprint, String, Sweden, Twins, Vase, Strait; three seeds and side swaps): 18/36 (50.0%) against v0030, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-first-attacker-economy-v0050-screen-analysis.json`; matrix report: `reports/local-20260814T145434Z`. The screen did raise average harvesters on several maps but did not improve win rate.
- The temporary change to `bots/candidate/bot/attacker.py` was reverted. Revert checks: focused unittest 15/15 (`reports/iter-first-attacker-economy-v0050-revert-unittest.log`), compileall passed (`reports/iter-first-attacker-economy-v0050-revert-compile.log`), smoke 4/4 (`reports/iter-first-attacker-economy-v0050-revert-smoke.log`), and the source diff against v0030 was empty. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-first-attacker-economy-v0050-revert-static.log`).
- Status: rejected at the screen gate; no full matrix, package, upload, activation, or baseline transition. v0030 remains the best local baseline.

### v0049 map-context enemy-core targeting rejected — 2026-08-14

- Objective: repair the enemy-core target on the fixed map geometries where the old one-size-fits-all mirror sends attackers away from the real 2x2 core, with the goal of restoring sentinel pressure without changing economy, unit caps, ammo, or live state.
- Variant 1 used a dimensions/core-anchor catalog plus a corrected footprint mirror. It was reliability-clean but tied the comparator at 31/54 in `reports/local-20260814T143306Z`; replay analysis: `reports/iter-core-context-v0030-focused-replay-analysis.json`.
- Variant 2 additionally allowed pre-vision sentinel placement only for cataloged map counterparts. It regressed to 25/54 in `reports/local-20260814T144117Z`; replay analysis: `reports/iter-core-context-v0049-focused-r2-replay-analysis.json`. Both slices had zero command failures, TLEs, suspicious output, and no-delivery rows; variant-2 max p99 was 1,419 us and peak callback 2,913 us.
- Both temporary edits to `bots/candidate/bot/attacker.py` and `tests/test_candidate_nearest_defense.py` were reverted. Revert checks: focused unittest 15/15 (`reports/iter-core-context-v0049-revert-unittest.log`), compileall passed (`reports/iter-core-context-v0049-revert-compile.log`), smoke 4/4 (`reports/iter-core-context-v0049-revert-smoke.log`), `git diff --check` passed, and the candidate Python tree is byte-identical to v0030 (`reports/iter-core-context-v0049-revert-diff.log`). `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-core-context-v0049-revert-static.log`).
- Status: rejected after two bounded variants; v0030 remains the best local baseline. No full matrix, package, upload, activation, or baseline transition. The edge-map missing-sentinel behavior needs a separate placement/path hypothesis.

### v0048 endgame delivery phase rejected — 2026-08-14

- Hypothesis: after round 850, dynamic builders should preserve delivery and repairs instead of opening new paid raid/advance work, while the existing home-threat and repair priorities remain unchanged.
- Full 21-map gate against immutable v0030: 115/210 wins (54.8%), with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-endgame-delivery-v0030-full-replay-analysis.json`; matrix report: `reports/local-20260814T140055Z`. The candidate had two no-delivery rows; maximum p99 callback was 1,460 us and peak callback was 2,819 us. The focused slice had been 35/54 (64.8%), but the full map matrix did not sustain that edge.
- The temporary `ENDGAME_ROUND` branch in `bots/candidate/bot/constants.py` and `bots/candidate/bot/dynamic.py` was reverted after the full gate failed to beat v0030. Revert checks: focused unittest 15/15 (`reports/iter-endgame-delivery-revert-unittest.log`), compileall passed (`reports/iter-endgame-delivery-revert-compile.log`), smoke 4/4 (`reports/iter-endgame-delivery-revert-smoke.log`), and the candidate Python tree is byte-identical to v0030 (`reports/iter-endgame-delivery-revert-diff.log`). `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-endgame-delivery-revert-static.log`).
- Status: rejected; v0030 remains the best local baseline and the candidate was not packaged, uploaded, activated, or promoted. Next work must use a distinct structural hypothesis and update the baseline only after a full reliability-clean win-rate improvement.

### v0047 map-adaptive late workforce rejected — 2026-08-14

- Hypothesis: after five completed routes and a rich bank, large/corridor maps should expand the late workforce from 12 to 14 builders so routing, repairs, and siege can run concurrently; compact maps stay at 12.
- Focused comparison against immutable v0030: 21/54 (38.9%) in `reports/local-20260814T133914Z`, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-map-late-workforce-v0030-focused-replay-analysis.json`; max p99 1,311 us and peak callback 2,742 us. Builder count rose, but conversion and map floors regressed sharply (Atoll 0/6, String 1/6).
- The temporary `bots/candidate/bot/core_role.py` expansion was reverted. Revert checks: focused unittest 15/15 (`reports/iter-map-late-workforce-revert-unittest.log`), compileall passed (`reports/iter-map-late-workforce-revert-compile.log`), smoke 4/4 (`reports/iter-map-late-workforce-revert-smoke.log`), `git diff --check` passed. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-map-late-workforce-revert-static.log`).
- Status: rejected; v0030 remains the immutable local baseline. No full matrix, package, upload, activation, or baseline transition.

### v0046 bounded chain recovery rejected — 2026-08-14

- Hypothesis: retain a pending conveyor for at most three safe turns when a danger flee leaves the builder within two tiles, instead of abandoning the segment immediately. The bounded retry was intended to preserve delivery without the broad vase-only route retry.
- Focused comparison against immutable v0030: 25/54 (46.3%) in `reports/local-20260814T132919Z`, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-bounded-chain-recovery-v0030-focused-replay-analysis.json`; max p99 1,418 us and peak callback 2,862 us. No-delivery rows fell to zero in this slice, but sentinels and win rate fell.
- The temporary `bots/candidate/bot/defender.py` recovery was reverted. Revert checks: focused unittest 15/15 (`reports/iter-bounded-chain-recovery-revert-unittest.log`), compileall passed (`reports/iter-bounded-chain-recovery-revert-compile.log`), smoke 4/4 (`reports/iter-bounded-chain-recovery-revert-smoke.log`), `git diff --check` passed. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-bounded-chain-recovery-revert-static.log`).
- Status: rejected; v0030 remains the immutable local baseline. No full matrix, package, upload, activation, or baseline transition.

### v0045 second-attacker siege handoff rejected — 2026-08-14

- Hypothesis: during a sustained but non-crisis core siege, the second permanent attacker should return home while the first attacker continues the direct offensive lane.
- Focused comparison against immutable v0030: 26/54 (48.1%) in `reports/local-20260814T132033Z`, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-second-attacker-siege-v0030-focused-replay-analysis.json`; max p99 1,254 us and peak callback 2,761 us.
- The temporary `bots/candidate/main.py` role handoff was reverted. Revert checks: focused unittest 15/15 (`reports/iter-second-attacker-siege-revert-unittest.log`), compileall passed (`reports/iter-second-attacker-siege-revert-compile.log`), smoke 4/4 (`reports/iter-second-attacker-siege-revert-smoke.log`), `git diff --check` passed. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-second-attacker-siege-revert-static.log`).
- Status: rejected; the direct combat shell remains v0030. No full matrix, package, upload, activation, or baseline transition.

### v0044 four-route economy floor rejected — 2026-08-14

- Hypothesis: keep dynamic builders in the economy state until four completed routes, preserving a fourth harvester/path before raids and advance tasks. No fixed-role or combat logic changed.
- Focused slice: 30/54 (55.6%) versus immutable v0030, zero reliability flags; report `reports/local-20260814T124620Z`, replay analysis `reports/iter-four-route-floor-v0030-focused-replay-analysis.json`.
- Required full 21-map gate: 106/210 (50.5%) versus v0030, zero command failures, TLEs, or suspicious output; max p99 1,477 us and peak callback 3,658 us. Replay analysis: `reports/iter-four-route-floor-v0030-full-replay-analysis.json`. Map floors regressed on Crossfire, Fjord, Hive, Pinch, Runestone, and Vault; the candidate had four no-delivery games.
- The temporary changes to `bots/candidate/bot/dynamic.py` and `tests/test_candidate_nearest_defense.py` were reverted. Revert checks: focused unittest 15/15 (`reports/iter-four-route-floor-revert-unittest.log`), compileall passed (`reports/iter-four-route-floor-revert-compile.log`), smoke 4/4 (`reports/iter-four-route-floor-revert-smoke.log`), `git diff --check` passed. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-four-route-floor-revert-static.log`).
- Status: rejected; v0030 remains the immutable local baseline. No package, upload, activation, or baseline transition.

### v0043 frontline loaded-belt sabotage rejected — 2026-08-14

- Hypothesis: once the economy has three completed routes, a fixed attacker could break one visibly loaded enemy conveyor/splitter within sentinel range of the enemy core, then return to the direct siege lane. Empty logistics, harvesters, and pre-delivery detours remained excluded.
- Focused comparison against the immutable best baseline v0030: 27/54 (50.0%) in `reports/local-20260814T123628Z`, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-frontline-sabotage-v0030-focused-replay-analysis.json`; max p99 1,394 us and peak callback 2,791 us.
- The temporary changes to `bots/candidate/bot/attacker.py` and `tests/test_candidate_nearest_defense.py` were reverted after the slice failed to beat v0030. Revert checks: focused unittest 15/15 (`reports/iter-frontline-sabotage-revert-unittest.log`), compileall passed (`reports/iter-frontline-sabotage-revert-compile.log`), smoke 4/4 (`reports/iter-frontline-sabotage-revert-smoke.log`), `git diff --check` passed. `make static` remains the inherited exit-2 obsolete-import failure (`reports/iter-frontline-sabotage-revert-static.log`).
- Status: rejected; v0030 remains the local baseline and the candidate is byte-identical to it. No package, upload, activation, or baseline transition. Platform v99 remains `active_observing` with no attributed matches.

### v0042 vase route-retry rejection — 2026-08-14

- Hypothesis: the 11×16 vase topology needs a contextual chain repair that retains an owed conveyor after a danger flee and safely walks back, while leaving all other maps unchanged.
- Affected slice: vase/skerry 11/20 versus v0030, compared with a same-baseline control at 7/20; no-delivery rows fell from four to two in the slice. This was not accepted on the slice alone.
- Full release gate `reports/local-20260814T120541Z` scored 102/210 (48.6%) versus v0030, with zero command failures, TLEs, or suspicious output. Replay analysis: `reports/iter-vase-route-retry-v0030-full-replay-analysis.json`; map regressions included pinch, quarry, skerry, string, and several other floors.
- The temporary `bots/candidate/bot/defender.py` retry was reverted. Revert checks: focused unittest 15/15 (`reports/iter-vase-route-retry-revert-unittest.log`), compileall passed (`reports/iter-vase-route-retry-revert-compile.log`), `git diff --check` passed, smoke 4/4 (`reports/iter-vase-route-retry-revert-smoke.log`). No package, upload, or activation.
- Status: rejected; v0030 remains the immutable baseline. Platform v99 is still `active_observing` with no attributed matches.

### v0041 fixed-attacker barrier fallback rejected — 2026-08-14

- Hypothesis: top-team enemy-ore barriers could be reproduced by letting a fixed attacker place one adjacent enemy-half barrier on an otherwise idle, surplus-funded turn after direct attacks and sabotage.
- Rejected after the focused 54-game run `reports/local-20260814T114733Z`: candidate 25/54 (46.3%) against the immutable v0030 baseline, with zero command failures, TLEs, or suspicious replay output. Replay analysis: `reports/iter-attacker-ore-barrier-v0030-focused-replay-analysis.json`.
- The temporary changes to `bots/candidate/main.py` and `bots/candidate/bot/attacker.py` were reverted. Revert checks: focused unittest 15/15 (`reports/iter-attacker-ore-barrier-revert-unittest.log`), compileall passed (`reports/iter-attacker-ore-barrier-revert-compile.log`), `git diff --check` passed, smoke 4/4 (`reports/iter-attacker-ore-barrier-revert-smoke.log`). `make static` remains the known exit-2 inherited obsolete-import failure (`reports/iter-attacker-ore-barrier-static.log`).
- Status: rejected; no full matrix, package, upload, or activation. v0030 remains the comparator and platform v99 remains `active_observing` with no attributed matches.

### v0040 baseline freeze and hijack-priority rejection — 2026-08-14

- Baseline policy update: the strongest measured local bot is now frozen as the comparator after each accepted release. The current immutable baseline is `bots/versions/v0030_loaded-raid-best_20260814-1109_eeafad8f`, packaged as `artifacts/submissions/v0030_loaded-raid-best_20260814-1109_eeafad8f.zip` (SHA-256 `b49089228926753e9897c5bd584d7aa6881e43b4398cfda28cb036e8be0f6963`). Regression, matrix, and smoke configs point to this snapshot.
- Rejected hypothesis: after three completed routes, dynamic builders would prioritize visible enemy Harvester hijacks ahead of routine belt repair. Only `bots/candidate/bot/dynamic.py` changed; the patch was reverted after full replay review.
- Evidence: focused run `reports/local-20260814T111406Z` scored 30/54 (55.6%), but the full 210-game release matrix `reports/local-20260814T112034Z` scored 104/210 (49.5%) against v0030. Map floors fell on longship, string, showdown, and fjord. Replay analysis: `reports/iter-hijack-priority-v0030-full-replay-analysis.json`; zero command failures, TLEs, or suspicious outputs.
- Validation after revert: focused unittest 15/15 (`reports/iter-hijack-priority-revert-unittest.log`), compileall passed (`reports/iter-hijack-priority-revert-compile.log`), `git diff --check` passed, smoke 4/4 (`reports/iter-hijack-priority-revert-smoke.log`), and `make static` remains the known exit-2 inherited obsolete-import failure. No upload or activation was performed; platform v99 remains `active_observing` with no attributed matches.
- Status: rejected; v0030 retained as baseline. Remaining risks are map-specific conversion losses, unproven v99 live performance, and the inherited static-import failures.

### Live observation captured — 2026-08-14T06:11:34Z

- Active version: 99
- Report: reports/live-observe-20260814T061113Z


### Live observation captured — 2026-08-14T04:36:03Z

- Active version: 99
- Report: reports/live-observe-20260814T043544Z


### Candidate activated — 2026-08-14T04:18:34Z

- Version: 99
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260814T041804Z


### Candidate uploaded — 2026-08-14T04:18:33Z

- Candidate: v0029-first-delivery-loaded-sabotage-eeafad8f
- Version: 99
- Rollback target: 72
- Report: reports/live-deploy-20260814T041804Z


### Live observation captured — 2026-08-14T02:11:28Z

- Active version: 72
- Report: reports/live-observe-20260814T021103Z


### Live observation captured — 2026-08-14T01:09:37Z

- Active version: 72
- Report: reports/live-observe-20260814T010918Z


### Automatic rollback — 2026-08-13T23:58:34Z

- Failed candidate version: 98
- Reactivated: 72
- Reason: 17 attributable v98 ladder series: 40-45 games (0.4706) versus protected v72 score 0.6417; rating fell to 1491.26; no reliability failure detected
- Report: reports/live-rollback-20260813T235833Z


### Live observation captured — 2026-08-13T23:58:06Z

- Active version: 98
- Report: reports/live-observe-20260813T235743Z


### Live observation captured — 2026-08-13T23:14:49Z

- Active version: 98
- Report: reports/live-observe-20260813T231424Z


### Live observation captured — 2026-08-13T22:22:35Z

- Active version: 98
- Report: reports/live-observe-20260813T222216Z


### v0032 early two-sentinel shell — 2026-08-13T18:32:45Z

- Objective: prioritize winning combat tempo over ore totals by keeping a two-sentinel shell online while economy and dynamic workers continue harvesting, routing, and raiding.
- Change: only `bots/candidate/bot/constants.py` changed; `SENTINEL_POOL_TARGET_EARLY` increased from 1 to 2 after replay-guided v97 losses.
- Full release matrix: candidate 114/210 wins versus immutable v97's 96/210; all 210 games command-clean. Candidate collected 937790 titanium versus 858760, but win rate is the selection criterion. Report: `reports/local-20260813T180421Z`; analysis: `reports/local-early-two-sentinels-v97-210-analysis.json`.
- Focused slices: 29/48 wins in each of two disjoint slices (58/96 total), zero command failures. Candidate replay reliability: p99 max 1534 us, median 1006 us, peak 2920 us, zero TLE/suspicious output; two candidate games had no delivery.
- Final checks: unittest focused defense suite 6/6 (`reports/final-v0032-focused-unittest.log`); pytest unavailable in the environment; compileall and diff-check passed; smoke 4/4 command-clean (`reports/local-20260813T183012Z`). `make static` exits 2 on 15 inherited obsolete pre-v86 imports (`reports/final-v0032-static.log`).
- Package: `artifacts/submissions/v0027_early-two-sentinel-shell_20260813-1831_eeafad8f.zip`, SHA-256 `2fdf4af5742a40b3ed824b288c3b13939c824151d99b0e9f5e661cb378bff6e3`; immutable snapshot `bots/versions/v0027_early-two-sentinel-shell_20260813-1831_eeafad8f`.
- Live: v97 was rolled back to v72 before deployment; v0032 uploaded as platform v98 (`ddfbf167-3471-442d-9514-d74bd3a04c20`), ready and active. Post-activation observation has zero attributed v98 matches, so live superiority remains unproven. Reports: `reports/rollback-before-v0032.log`, `reports/deploy-v0032-early-two-sentinel.log`, `reports/live-observe-20260813T183227Z`.
- Status: accepted and active_observing; retain v72 as last-known-good rollback. Remaining risks are map-specific losses, zero attributable live series, and the inherited static-import failures.

### Live observation captured — 2026-08-13T18:32:45Z

- Active version: 98
- Report: reports/live-observe-20260813T183227Z


### Candidate activated — 2026-08-13T18:32:15Z

- Version: 98
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260813T183155Z


### Candidate uploaded — 2026-08-13T18:32:15Z

- Candidate: v0027-early-two-sentinel-shell-eeafad8f
- Version: 98
- Rollback target: 72
- Report: reports/live-deploy-20260813T183155Z


### Automatic rollback — 2026-08-13T18:31:50Z

- Failed candidate version: 97
- Reactivated: 72
- Reason: Superseded by locally gated v0032 early-two-sentinel-shell
- Report: reports/live-rollback-20260813T183149Z


### Live observation captured — 2026-08-13T14:30:16Z

- Active version: 97
- Report: reports/live-observe-20260813T142950Z


### v0031 upload and live activation observed — 2026-08-13T13:10:40Z

- Pre-upload source-of-truth check reconciled the stale local state: platform listed v95 active, v96 inactive, v72 last known-good; report reports/live-bootstrap-20260813T130903Z.
- Uploaded artifacts/submissions/v0026_direct-siege-role-split_20260813-1308_eeafad8f.zip through the upload-only wrapper; platform returned version 97, submission fb5db5ab-e6a5-46ef-b973-af6c1fb671f4, ready. Upload report: reports/upload-v0031-direct-siege.log.
- A follow-up platform list showed v97 isActive=true and v95 isActive=false despite the upload-only wrapper. Live state is reconciled to active version 97, previous active 95, immediate rollback 95, and last known-good 72; status report: reports/status-v97-after-upload.json.
- Read-only live observation completed at reports/live-observe-20260813T130948Z. No live matches are attributed to v97 yet; do not claim live improvement from the local 174/210 result.


### Live observation captured — 2026-08-13T13:10:07Z

- Active version: 97
- Report: reports/live-observe-20260813T130948Z


### Live state bootstrapped — 2026-08-13T13:09:22Z

- Active version: 95
- Report: reports/live-bootstrap-20260813T130903Z


### v0031 direct-siege role split accepted locally — 2026-08-13T13:07:14Z

- Objective: use fresh v95 losses and Pivot/top-team replays to protect the first combat shell by keeping fixed attackers on the direct core/sentinel lane while economy and dynamic builders retain hijack/raid work.
- Accepted change: bots/candidate/bot/attacker.py removes the fixed-attacker opening harvester hijack; tests/test_candidate_nearest_defense.py records the ownership and combat-shell boundary. Experiment record: experiments/v0031-direct-siege-role-split.md.
- Focused comparison: 40/48 versus the actual 39/48 current-candidate reference; full 21-map matrix: 174/210 versus 172/210, all 210 command-clean. Reports: reports/local-20260813T121855Z and reports/local-20260813T122504Z.
- Validation: focused 6/6, compileall, git diff --check, smoke 4/4 (reports/local-20260813T124257Z), regression 50/54 and 54/54 command-clean (reports/local-20260813T124554Z).
- make static remains blocked only by 15 inherited obsolete pre-v86 imports (reports/static-20260813T1245-direct-siege.log); candidate-focused tests pass. Rejected structural variants remain local reports and were not copied.
- Status: accepted local release candidate; String and Vault remain risks, and live superiority is unproven. Package and platform upload are the next guarded steps; retain the current active version for rollback.


### v0030 dynamic raid-recovery cycle rejected — 2026-08-12

- Objective: use live replay evidence to make raiders alternate between a bounded logistics sabotage pulse and a home defense/build phase without weakening the economy. Reviewed the latest v95 loss set (`replays/live-latest-v95-edb000ab/`) and top-team sets (`replays/top-live-20260812-sporks-pivot/`, `replays/top-live-20260812-clankers-sporks/`).
- Attempt 1 added a `TASK_RECOVER` home pulse after each dynamic raid and blocked raids during a core siege. Against downloaded v95: **21–33**, 262,220–333,480 titanium, zero command failures, max replay p99 1,377 µs; report `reports/local-20260812T213830Z`.
- Repair attempt 2 restored harvest-before-raid ordering, required four completed routes plus a harvester-cost surplus, and gave fixed attackers a return-home/build pulse. Against v95: **16–38**, 251,170–322,830 titanium, zero command failures, max replay p99 1,533 µs; report `reports/local-20260812T214855Z`.
- Focused tests passed for both attempts; smoke was command-clean at `reports/local-20260812T213811Z` and `reports/local-20260812T214837Z`. `make static` remains blocked by the inherited 15 obsolete pre-v86 imports (`reports/v0030-raid-recovery-static.log`, `reports/v0031-raid-recovery-attacker-static.log`).
- Decision: both bounded repairs were rejected after the second failure. Temporary bot edits were removed; `bots/candidate` is restored byte-identically to the downloaded v96 source. Final smoke/compile/diff checks passed (`reports/local-20260812T215759Z`). No submission or live-state transition occurred. Experiment record: `experiments/v0030-dynamic-raid-recovery-cycle.md`.
- Remaining risk: v96 still has no attributable ladder series in the current snapshot, and the v95 comparator remains stronger in the quick local sample. The next hypothesis should target workforce/route conversion rather than more raid timing gates.

### Quick v96-v95 comparison — 2026-08-12

- Objective: benchmark the current v96 source (`bots/candidate`) against the downloaded official v95 submission with side swaps on the fixed short pool (9 maps × 3 seeds × 2 sides = 54 games). v95 archive SHA-256: `df5f2b6c4b2eb723c6886a44e0acb0a6cf6ff7e770619ee4512656467bfadfff`.
- Result: v96 lost **24–30** to v95 (44.44% wins). Candidate titanium was 276,940 versus v95's 283,710 (0.9761×). Per-map records: sprint 0–6, string 3–3, bridge 4–2, crossfire 1–5, atoll 2–4, sweden 3–3, longship 3–3, vault 5–1, aurora 3–3.
- Reliability: 54/54 command-clean, zero TLE markers, zero suspicious output, and maximum replay p99 1,441 µs. First titanium delivery was present in all games (v96 mean turn 15.3; v95 mean turn 17.5). Report: `reports/local-20260812T212247Z`; runner log: `reports/v0029-v95-quick-bench.log`.
- Decision: v96 is **not promoted over v95** by this quick win-primary comparison. No upload, activation, or live-state change was performed; v96 remains the active observed submission pending ladder evidence, while v95 is retained locally as a stronger comparator for the next iteration.

### v0029 dynamic logistics raid — 2026-08-12

- Objective and evidence: review v94 live losses plus top sporks/Pivot and Clankers/sporks replays, then convert surplus resources into targeted enemy logistics sabotage without weakening the opening route. Findings are recorded in `reports/live-v94-strategy-analysis.txt` and `reports/top-live-strategy-summary.txt`.
- Implementation: after three completed harvester chains, the nearest dynamic Builder can claim one visible enemy Harvester, Splitter, or Conveyor and use the existing safe cardinal attack path; the 80-Ti reserve blocks raids below the economy floor. Stale or replaced targets are rejected. Files changed: `bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, `bots/candidate/bot/dynamic.py`, `tests/test_candidate_nearest_defense.py`, and `experiments/v0029-dynamic-logistics-raid.md`. Baseline and immutable snapshots were not edited.
- Full local gate against exact v0024: **128-82**, 210/210 command-clean, candidate 913,730 vs baseline 771,210 titanium (1.1848x), max replay p99 1,371 us. Map record and delivery diagnostics are in `experiments/v0029-dynamic-logistics-raid.md`; report `reports/local-20260812T205222Z`.
- Tests: focused 21/21, compileall, and `git diff --check` passed; `make smoke` 4/4 passed (`reports/local-20260812T211302Z`). `make static` remains blocked by the same 15 obsolete pre-v86 test imports (`reports/v0029-dynamic-logistics-raid-static.log`).
- Package/upload: `artifacts/submissions/v0025_v0029-dynamic-logistics-raid_20260812-2113_eeafad8f.zip`, SHA-256 `45978c428499d93de8d6ab0366eddbba95dbf3c9460e76e39d0e751e2ca484f3`; upload created platform version **96**, submission `d1c915c2-282f-409a-ae7b-29f159c47c57`, status ready and `isActive=true` despite the upload-only wrapper. State is reconciled in `state/live_state.json`; v94 is the immediate rollback and v72 remains last known-good.
- Platform verification: `fcode submission download 96` succeeded; the downloaded 10-file source (`artifacts/platform/v96-v0029/submission.zip`, 189,117 unpacked bytes) is byte-identical to the immutable v0025 snapshot (`reports/download-v96.log`).
- Remaining risk: first titanium delivery averaged turn 62 and was missing in 9/210 games versus v0024's 4/210. The latest ladder list contains no v96 series yet (the newest completed result is v95 from before/around the upload); do not claim live improvement until v96 observation evidence exists.

### v0024 bootstrap economy and deterministic frontier — 2026-08-12

- Objective: prevent pre-income dynamic Builders from spending the opening on ring/advance work, distribute exploration deterministically, and beat exact v0023 before the release matrix.
- Files changed: `bots/candidate/main.py`, `bots/candidate/bot/defender.py`, `experiments/v0024-bootstrap-deterministic-frontier.md`, `UPDATES.md`, `state/project_state.json`, and refreshed `docs/START_HERE.md`. No baseline or immutable snapshot was overwritten; no submission or activation was performed.
- Strategy: Builders assigned during the zero-chain bootstrap all use the Defender economy loop; later spawns remain dynamic. Exploration uses a bounded per-Builder cursor over map geometry instead of the shared process-global random stream. The cursor scan is capped by map area and retains existing danger/progress/blacklist guards.
- Protected evidence: first 48-game checkpoint 29–19 and independent repeat 31–17 against v0023; pooled 60–36 (62.5%) with zero command failures. Reports: `reports/local-20260812T171311Z` and `reports/local-20260812T171648Z`.
- Full 210-game gate: 122–88 (58.095% candidate wins), candidate titanium 876,380 vs baseline 797,940 (1.0983x); map floors include atoll 4–6, fjord 3–7, quarry 3–7, sprint 8–2, vase 7–3. Candidate first delivery was missing in 5 games versus 8 for v0023.
- Reliability: 210/210 command-clean, zero TLE markers, zero suspicious output, maximum replay p99 1,462 us, peak callback 2,956 us. Summary and replay analysis: `reports/local-20260812T172029Z/bootstrap-deterministic-explore-v0023-210-summary.json` and `reports/local-20260812T172029Z/replay-analysis.json`.
- Tests: focused 18/18, compileall, and `git diff --check` passed; `make smoke` 4/4 passed (`reports/local-20260812T173907Z`). `make static` remains blocked by 15 inherited obsolete pre-v86 imports (`reports/bootstrap-deterministic-explore-v0023-static.log`).
- Risks/status: route delivery still fails on a small vase/sprint subset and collection trails v0023 on atoll/fjord/quarry; this is a **new local best over v0023**, retained in `bots/candidate`, not yet submitted or activated.

### Workforce-first v87 full matrix — 2026-08-12

- Objective: compare the restored workforce-first candidate against the exact previous-best v87 artifact on the full release matrix; wins are primary and collection is diagnostic.
- Files changed: `bots/candidate/main.py`, `bots/candidate/bot/constants.py`, `bots/candidate/bot/core_role.py`, `bots/candidate/bot/defender.py`, `bots/candidate/bot/dynamic.py`, `tests/test_candidate_nearest_defense.py`, `tests/test_analyze_replay.py`, `scripts/analyze_replay.py` (entity-ID deduplicated placement parsing), `UPDATES.md`, `state/project_state.json`, and refreshed `docs/START_HERE.md`.
- Baseline: `/tmp/fcl-v87-5Jy7qX`, SHA-256 `0c59d375548f427371f14eb48ec58eea761b63a9164e72753f3cc9ee6489b4ad`.
- Result: 143–67–0 over 210 games (68.095% candidate wins); candidate titanium 751,210 vs 638,090 (+17.728%). Map floors: jackpot 3–7, sprint 4–6, pinch/strait/twins 5–5; no map collapsed to zero wins.
- Reliability: 210/210 command-clean, zero TLE, zero suspicious output, maximum replay p99 1,333 µs. Focused tests 12/12 passed, compileall passed, `git diff --check` passed, smoke 4/4 command-clean (`reports/local-20260812T142830Z`).
- Reports: `reports/local-20260812T143141Z`, `reports/local-20260812T143141Z/replay-analysis.json`, `reports/local-20260812T143141Z/workforce-first-v87-210-summary.json`, `reports/workforce-first-v87-210.log`, `reports/workforce-first-static.log`.
- `make static` remains blocked only by the inherited 15 obsolete legacy-import tests; candidate-focused contract/compile checks pass. Status: candidate is the new local win-primary best; no package, submission, or activation was performed in this benchmark step. Remaining risk is opening variance on jackpot/sprint and delayed first delivery on bridge/showdown.

### Workforce-first candidate submitted — 2026-08-12

- Package: `artifacts/submissions/v0023_workforce-first-v87_20260812-1454_eeafad8f.zip`; SHA-256 `49644d24e1584458c6dff43b92ef71c2653eb30ad8c910c63b87177bdef9ad6d`; manifest records 10 files and 182,882 unpacked bytes.
- Platform: upload created version **93**, submission ID `7bfc1636-7b4f-4884-a634-02037f712704`, name `v0023-workforce-first-v87-eeafad8f`, status `ready`.
- The platform status/list reports v93 as active and v92 as previous, despite no explicit activation command; this observed state is recorded in `state/live_state.json`. No remote gate was run.
- Reports: `reports/package-v0023-workforce-first.log`, `reports/upload-20260812T145453Z/upload.json`, `reports/submission-v0023-status.json`, and `reports/status-after-v0023-upload.json`.

### Live observation captured — 2026-08-12T13:58:31Z

- Active version: 92
- Report: reports/live-observe-20260812T135812Z


### Live observation captured — 2026-08-12T13:45:25Z

- Active version: 92
- Report: reports/live-observe-20260812T134506Z


### Candidate activated — 2026-08-12T13:44:44Z

- Version: 92
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260812T134424Z


### Candidate uploaded — 2026-08-12T13:44:44Z

- Candidate: v0022-nearest-home-responder-eeafad8f
- Version: 92
- Rollback target: 72
- Report: reports/live-deploy-20260812T134424Z


### Nearest home-responder strategy — release candidate — 2026-08-12

- Fundamental change: dynamic Builders now deterministically yield a shared home-threat task to the nearest non-attacker Builder (distance, then id), preventing duplicate counter-Gunner construction and keeping the remaining workers on route work. Files: `bots/candidate/bot/dynamic.py`, `tests/test_candidate_nearest_defense.py`; experiment: `experiments/nearest-home-responder-v87.md`.
- Exact active v87 local evidence: two 48-game checkpoints were 27-21 and 28-20; pooled 55-41 with 1.153x titanium. Full 210-game gate was **128-82**, `785220-699810` titanium (1.1220x), zero command failures/TLE/suspicious output, max p99 1.469 ms, peak 2.728 ms: `reports/local-20260812T132348Z`, analysis `reports/nearest-defense-v87-full-replay-analysis.json`.
- Focused tests 2/2, source contract 8/8, compile passed, smoke 4/4 (`reports/local-20260812T131542Z`). `make static` remains blocked by the known 15 obsolete pre-v86 imports (`reports/nearest-defense-static-final.log`).
- Required server/live gate completed before packaging: candidate won **3-2** against the exact v87 artifact, match `b643b12e-6549-4564-a069-6b88a5ddf669`; reports `reports/remote-20260812T133953Z` and `reports/nearest-defense-remote-info-final.json`. Live status was reconciled to active v87 at `reports/live-observe-20260812T134125Z`.
- Release decision: eligible for guarded packaging and deployment with v87 preserved as rollback. Remaining risk is map variance (jackpot 3-7; string/sweden/twins 4-6), with no 0-10 map collapse.
- The deploy guard initially found stale local state for an externally superseded v88 observation; fresh `fcode status` confirmed v87 active. State was reconciled to `idle` without a live activation or rollback, preserving v72 as known-good and v87 as current rollback context.

### Live observation captured — 2026-08-12T13:41:43Z

- Active version: 87
- Report: reports/live-observe-20260812T134125Z


### v87 economy and workforce follow-up rejected — 2026-08-12

- Comparator: exact active platform v87 archive (`0c59d375…6489b4`); candidate restored after every isolated trial. No remote gate, submission, activation, or live-state change occurred.
- Rejected counter-Gunner duplication suppression after the 210-game release matrix: 116-94 but only `1.0095x` titanium and four 3-7 map results; `reports/local-20260812T115001Z`, `reports/deduplicated-counter-gunner-v87-full-replay-analysis.json`.
- Rejected four-harvester offense gate after conflicting 48-game repeats (28-20 / `1.2216x`, then 23-25 / `0.9560x`): `reports/local-20260812T121050Z`, `reports/local-20260812T121347Z`.
- Rejected first-attacker economy conversion (22-26 / `0.8218x`), early eight-worker expansion at three routes (20-28 / `0.9055x`) and four routes (18-30 / `0.8885x`), six-worker stage two (18-30 / `0.6760x`), delayed second attacker (23-25 / `0.8129x`), four-worker opening (24-24 / `0.7735x`), lower ammo floor (19-29 / `0.9555x`), and round-40 stage-two fallback (22-26 / `1.0383x`).
- Validation of restored candidate: static contract 8/8 and compile passed; smoke 4/4 command-clean at `reports/local-20260812T124729Z`. `make static` remains blocked by 15 obsolete test imports for the removed candidate architecture.
- Next task: capture fresh live v87 loss signatures by map, then test one executable map-agnostic route-throughput or repair hypothesis. Do not deploy without a robust local promotion and a clean remote gate.

### v87-v88 combined policy checkpoint — 2026-08-12T08:18:00Z

- Downloaded and benchmarked platform v87 and v88 artifacts: v87 won 117-93
  and 1.139x titanium across the fixed 210-game pool.
- Replayed v88's 1-4 live loss plus current top-team matches. The retained
  candidate combines v87's income/idle discipline and mature workforce with
  v88's visible-ore ownership guard.
- Selected gate: 33-21, 1.1860x titanium, zero TLE/suspicious output;
  `reports/local-20260812T074500Z`.
- Full confirmation versus v88: 112-98, `750460-694890` titanium (1.0800x),
  210/210 command-clean, p99 <= 1.483 ms; `reports/local-20260812T074937Z`.
- Rejected: no ownership (23-31), four-builder opening (30-24), and
  seven-builder mature cap (26-28). No package, upload, or activation.
- Full record: `experiments/v87-v88-combined-policy.md`. `make static` remains
  blocked only by 15 stale imports from the former candidate layout.

### v88 route-ownership submitted and active — 2026-08-12T02:19:33Z

- Packaged immutable local `v0021_v86-route-ownership_20260812-0218_eeafad8f`
  (archive SHA-256 `7c89830c150e22f6fc9e4b0434d04d68b57cd530236610c556a22e11aa19774f`).
- Release gate: 210/210 local commands clean, **159-51**, `526580-310950`
  titanium (1.6935x), zero TLE/suspicious replay output, max p99 1.220 ms,
  peak 4.969 ms: `reports/local-20260812T021018Z`.
- Remote gate match `4e859320-2a29-4396-9690-a6d5425b56fd` completed 3-2 for the
  candidate: `reports/remote-20260812T021052Z`.
- Uploaded as platform v88, `v0021-v86-route-ownership-eeafad8f`; upload
  report: `reports/upload-20260812T021856Z/upload.json`. Although the upload
  wrapper does not activate, the platform reported v88 active immediately.
  Captured confirmation: `reports/live-observe-20260812T021908Z`.
- State reconciled to active v88 with v87 retained as prior active and v72 as
  known-good rollback. Observe v88 to the 12-series minimum before any score
  decision. The legacy static suite remains incompatible with the v86 layout;
  its focused source-contract checks pass.

### Live observation captured — 2026-08-12T02:19:33Z

- Active version: 88
- Report: reports/live-observe-20260812T021908Z


### Live observation captured — 2026-08-12T02:13:12Z

- Active version: 87
- Report: reports/live-observe-20260812T021248Z


### v86 route-ownership checkpoint — 2026-08-12T02:10:00Z

- Rebased the mutable candidate on the downloaded current platform v86 source;
  source archive SHA-256 `54ff398a2f7cde0d2082e138513704a898d86359a213cc5b872fd4c4d5efdf6c`.
- Reviewed v84 losses and current top-team replays. The useful common pattern
  is connected independent economy, not a raw worker cap: two attempted
  five-worker variants lost to v86 (28-26 and 26-28).
- Retained only a local, visibility-bounded ore-ownership guard: closest
  economic Builder wins; ties use the lower ID; permanent attackers never
  reserve an ore.
- Final repaired direct matrix versus v84: **38-16**, `170340-106540`
  titanium (1.5988x), 54/54 command-clean, zero TLE/suspicious replay output,
  p99 <= 1.055 ms, peak <= 3.606 ms. Reports:
  `reports/local-20260812T020304Z` and
  `reports/v86-route-ownership-v84-final-replay-analysis.json`.
- Smoke passed 4/4: `reports/local-20260812T020254Z`. `make static` is still
  blocked solely by 14 legacy tests that import the removed pre-v86 candidate
  architecture; `reports/v86-route-ownership-final-static-recheck.log`.
- Release is intentionally blocked pending v86-native focused tests and a
  larger confirmation against v86. Full record:
  `experiments/v86-route-ownership.md`.

### Reviewer comparison of platform v83-v85 — 2026-08-12T01:26:09Z

- Read-only review completed; no upload, activation, rollback, baseline replacement,
  or source edit was performed.
- v82 remains the retained local baseline and strongest supported live sample:
  14 series, 43-27 games, raw score `0.6142857143`, adjusted residual
  `+0.0785054177`, net `+35.1704 Elo`.
- v83: three live series, 10-5 games, adjusted `+0.1706516199`; local
  54-game result 33-21 and `118150-80950` titanium. Evidence is too small for
  promotion.
- v84: active externally with one live series, a 2-3 result, adjusted
  `+0.0564558579`; local challenger result 34-20 and `107640-72540` titanium.
  The one-game local edge does not clear the live evidence gate.
- v85: no live series and a 0-54 local result (`0-49300` titanium); 51/54
  games emitted repeated `OverflowError: out of range integral type conversion
  attempted` markers despite zero process return codes, so it is rejected for
  hidden runtime failure.
- All three local runs completed 54/54 process commands with zero
  candidate-attributed TLE/suspicious replay events; v85's hidden OverflowError
  markers are recorded above. Reports: `experiments/reviewer-v83-v85.md`,
  `reports/live-observe-20260812T011509Z`, `reports/local-20260812T011619Z`,
  `reports/local-20260812T012008Z`, and `reports/local-20260812T012143Z`.
- Next: observe active v84 to the 12-series minimum while preserving v82 and
  v72 as the guarded rollback target.

### Live score evaluated — 2026-08-12T01:25:59Z

- Version: 84
- Series: 1
- Score: 0.4
- Adjusted score: 0.05645585787278834
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Active v84 has one reliability-clean rated series, a 2-3 game result against Ouroboros, with adjusted residual +0.05646 and net +1.81 Elo; this is below the 12-series minimum.


### Live observation captured — 2026-08-12T01:15:28Z

- Active version: 84
- Report: reports/live-observe-20260812T011509Z


### Platform v82 promoted to local baseline — 2026-08-12T01:11:00Z

- Copied the downloaded active v82 source into `bots/baseline` and immutable
  snapshot `bots/versions/v0020_platform-v82_20260812-0111_eeafad8f`.
- Package manifest: `artifacts/submissions/v0020_platform-v82_20260812-0111_eeafad8f.manifest.json`;
  package SHA-256 `642a3b6cea9e07aa50a250dda3cf547e7f5a3763b529ae281b176044f4978788`.
- Updated all evaluation configs to compare against `bots/baseline`.
- At promotion time, live activation was unchanged: v82 remained active and
  v72 remained the rollback target. The seven-series evidence was provisional
  below the 12-series minimum; later external activation moved the platform to
  v84.
- Full record: `experiments/promote-v82-baseline.md`.

### Live score evaluated — 2026-08-11T21:33:39Z

- Version: 82
- Series: 7
- Score: 0.7142857142857143
- Adjusted score: 0.15200235063720857
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Active platform v82 is 5-2 by series and 25-10 by games across seven reliability-clean series, with adjusted residual +0.15200 and net +34.05 Elo; this is below the 12-series minimum.


### Live observation captured — 2026-08-11T21:23:48Z

- Active version: 82
- Report: reports/live-observe-20260811T212328Z


### Live score evaluated — 2026-08-10T01:10:34Z

- Version: 76
- Series: 6
- Score: 0.5666666666666667
- Adjusted score: 0.07228552064370689
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Six reliability-clean rated series are below the 12-series minimum: v76 is 3-3 by series and 17-13 by games, with adjusted residual +0.07229 and net +13.88 Elo.


### Live observation captured — 2026-08-10T01:08:40Z

- Active version: 76
- Report: reports/live-observe-20260810T010814Z


### Live score evaluated — 2026-08-10T00:34:27Z

- Version: 76
- Series: 2
- Score: 0.5
- Adjusted score: 0.016888109166547316
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Two reliability-clean rated series are below the 12-series minimum: v76 is 1-1 by series and 5-5 by games, with adjusted residual +0.01689 and net +1.08 Elo.


### Live observation captured — 2026-08-10T00:34:05Z

- Active version: 76
- Report: reports/live-observe-20260810T003339Z


### v76 first live series and rejected moonrise guard — 2026-08-10T00:25:00Z

- v76 opened 2-3 against Mimercraft for -2.972 Elo: wins on `saga` and
  `meander`; losses on `nordkap`, `moonrise`, and `antler`. Raw score 0.4,
  adjusted residual -0.092866, rank 51; observation remains below 12 series.
- Replay attribution found zero v76 TLEs (maximum v76 p99 6.196 ms, maximum
  callback 7.277 ms); all reported overruns belonged to the opponent. Evidence:
  `reports/v76-first-series-replay-analysis.json` and
  `reports/live-observe-20260810T002240Z`.
- A bounded 21x8 route-owner guard made both exact-live-seed sides deliver on
  turn 13, but lost collection 1,290-2,680; the five-seed gate was 5-5 and
  6,450-13,400. Rejected and restored exactly to immutable v0019; report:
  `experiments/post-v76-moonrise-route-owner.md`.

### Live score evaluated — 2026-08-10T00:23:21Z

- Version: 76
- Series: 1
- Score: 0.4
- Adjusted score: -0.09286592918996561
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: One reliability-clean rated series is below the 12-series minimum: v76 opened 2-3 against Mimercraft for -2.97 Elo; v76 itself had zero TLEs, while all replay overruns belonged to the opponent.


### Live observation captured — 2026-08-10T00:22:58Z

- Active version: 76
- Report: reports/live-observe-20260810T002240Z


### v0019 pre-four-route defense owner release — 2026-08-10T00:04:00Z

- Files: `bots/candidate/bot/builder.py`,
  `tests/test_candidate_bootstrap_defense.py`,
  `experiments/v76-pre-four-defense-owner.md`, v0019 snapshot/archive/manifest,
  reports, `UPDATES.md`, `state/project_state.json`, and `state/live_state.json`.
- Focused tests 5/5 and smoke 4/4 passed. `make static` retains only inherited
  obsolete API/navigation/source-line-budget failures; log:
  `reports/pre-four-defense-final-static.log`.
- Final current-pool gate: 90/90 command-clean, 59-31 and 213,690-128,370
  titanium versus immutable v0018; 1,601,652 calls, zero TLE/suspicious output,
  p99 <=4.357 ms and max callback 7.627 ms;
  `reports/local-20260809T233906Z`.
- Snowflake confirmation: 7-3 and 47,200-32,940 titanium;
  `reports/local-20260809T235438Z`. Remote gate passed 3-2 in match
  `c2cf4cd4-6eea-460f-89e3-949791febba2`;
  `reports/remote-20260809T235805Z`.
- Package: `artifacts/submissions/v0019_pre-four-defense-owner_20260810-0000_eeafad8f.zip`,
  SHA-256 `514fb3d9d451ab94d51b6d04b587d2b98a416c11da97b3b88301eec8b252f2be`.
- v75 was rolled back after 12 series at 3-9 series, 22-38 games, raw 0.3667,
  adjusted -0.118842, and -45.635 Elo. Platform v76 is now ready/active with
  v72 retained as rollback; observation status: active, 0/12 series.
- Remaining risks: remote gain was only 3-2; layout protection is intentionally
  pool-specific; static remains blocked by inherited tests; live behavior must
  clear the 12-series minimum before promotion.

### Candidate activated — 2026-08-10T00:03:07Z

- Version: 76
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260810T000246Z


### Candidate uploaded — 2026-08-10T00:03:07Z

- Candidate: v0019-pre-four-defense-owner-eeafad8f
- Version: 76
- Rollback target: 72
- Report: reports/live-deploy-20260810T000246Z


### Automatic rollback — 2026-08-10T00:02:30Z

- Failed candidate version: 75
- Reactivated: 72
- Reason: At the 12-series minimum, v75 is 3-9 by series and 22-38 by games, with raw score 0.3667, adjusted residual -0.118842, and net -45.635 Elo; both score measures materially trail v72.
- Report: reports/live-rollback-20260810T000230Z


### Live score evaluated — 2026-08-10T00:02:30Z

- Version: 75
- Series: 12
- Score: 0.36666666666666664
- Adjusted score: -0.11884200010174177
- Reliability failures: 0
- Proposed decision: rollback
- Reason: At the 12-series minimum, v75 is 3-9 by series and 22-38 by games, with raw score 0.3667, adjusted residual -0.118842, and net -45.635 Elo; both score measures materially trail v72.


### Live observation captured — 2026-08-10T00:01:16Z

- Active version: 75
- Report: reports/live-observe-20260810T000050Z


### v0018 nordkap route-owner release gate — 2026-08-09T22:54:00Z

- Files: `bots/candidate/bot/builder.py`,
  `tests/test_candidate_bootstrap_defense.py`, analyzer-backed reports,
  experiment/state documentation, v0018 snapshot/archive/manifest.
- Focused 3/3 and compileall passed; smoke 4/4 command-clean. `make static`
  retains only inherited API and obsolete line-cap failures.
- Target: 10-0 on `nordkap`, 17,750-3,000 titanium, delivery turns 11-12,
  zero TLEs, p99 <=2.900 ms; `reports/local-20260809T221120Z`.
- Current-pool release: 90/90 command-clean, 48-42 overall; source-active
  `nordkap` 6-0 and 10,650-1,800. Source-inactive maps were 42-42; aggregate
  titanium skew came from the known immutable `snowflake` side variance.
- Remote target passed on side B in match
  `b7a4dbe1-022e-4319-bb8b-62a347d10b7f`. Release CPU across 1,521,490 calls:
  p99 <=3.795 ms, max 7.157 ms, zero TLE/suspicious output.
- Package: `v0018_nordkap-route-owner_20260809-2231_eeafad8f.zip`, SHA-256
  `8cafb5ce16682f2ba1e9f7bcb5fbf5488b6f8d2c443d42f3848e55e6eb84f9b7`.
- Status: PASSED and packaged; deployment remains locked while v75 is at 5/12.

### Rejected v72-defense narrow-guard fallback — 2026-08-09T22:54:00Z

- Focused 1/1, compileall, smoke 4/4, and 90/90 decision games were
  command-clean; `make static` retained inherited failures only.
- Target gains did not generalize: the v72-defense candidate lost 34-56 and
  170,360-194,320 titanium to v0018, including 0-6 on `fjordgate`, `heart`,
  `moonrise`, and `nordkap`; report `reports/local-20260809T223713Z`.
- Candidate source was restored byte-for-byte to immutable v0018. No package or
  live operation was created from the rejected experiment.

### Live score evaluated — 2026-08-09T22:53:29Z

- Version: 75
- Series: 5
- Score: 0.32
- Adjusted score: -0.15096785293475
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Five reliability-clean rated series are below the 12-series minimum: v75 is 1-4 by series and 7-18 by games with net -24.15 Elo.


### Live observation captured — 2026-08-09T22:52:56Z

- Active version: 75
- Report: reports/live-observe-20260809T225231Z


### Live score evaluated — 2026-08-09T22:10:55Z

- Version: 75
- Series: 1
- Score: 0.8
- Adjusted score: 0.243181738026849
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: One reliability-clean rated series is below the 12-series minimum: v75 opened 4-1 over Innovex for +7.78 Elo; nordkap remained the sole loss.


### Live observation captured — 2026-08-09T22:10:37Z

- Active version: 75
- Report: reports/live-observe-20260809T221018Z


### Live observation captured — 2026-08-09T21:56:36Z

- Active version: 75
- Report: reports/live-observe-20260809T215618Z


### Candidate activated — 2026-08-09T21:56:13Z

- Version: 75
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260809T215553Z


### Candidate uploaded — 2026-08-09T21:56:12Z

- Candidate: v0016-meander-route-owner-eeafad8f
- Version: 75
- Rollback target: 72
- Report: reports/live-deploy-20260809T215553Z


### Automatic rollback — 2026-08-09T21:55:53Z

- Failed candidate version: 74
- Reactivated: 72
- Reason: external v74 rejected: lost 7-13 and 13133-19339 titanium to release-gated v0016 in full smoke; live start 3-2 with negative 0.157 Elo
- Report: reports/live-rollback-20260809T215553Z


### Live score evaluated — 2026-08-09T21:40:42Z

- Version: 74
- Series: 9
- Score: 0.5111111111111111
- Adjusted score: 0.007923623427457708
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Nine reliability-clean rated series are below the 12-series minimum: v73 is 6-3 by series and 23-22 by games with net +2.28 Elo.


### Live observation captured — 2026-08-09T21:40:09Z

- Active version: 74
- Report: reports/live-observe-20260809T213951Z


### Live score evaluated — 2026-08-09T21:28:54Z

- Version: 73
- Series: 8
- Score: 0.5
- Adjusted score: 0.0060582299655678185
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Eight reliability-clean rated series are below the 12-series minimum: v73 is 5-3 by series and 20-20 by games with net +1.55 Elo.


### Live observation captured — 2026-08-09T21:28:26Z

- Active version: 73
- Report: reports/live-observe-20260809T212808Z


### v0016 full release gate passed — 2026-08-09T21:26:00Z

- Full matrix: 210/210 command-clean, 106-104, 424,170 versus 425,080 titanium;
  report `reports/local-20260809T205017Z`.
- Replay CPU: 3,505,948 bot calls, maximum per-replay p99 4.164 ms, maximum
  call 7.270 ms, zero TLE or suspicious-output signals.
- Strict improvement: meander 10-0 across five seeds and both sides, 18,050
  versus zero titanium; Harvester by turn 12-13 and delivery by turn 17-18.
- Remote: 3-2 including the meander win; match
  `5c664cfa-5162-4bce-a117-487f92aafa8c`.
- Selected artifact: `v0016_meander-route-owner_20260809-2058_eeafad8f.zip`,
  SHA-256 `7c83de94e62aeceff3f57b2ef1c46539533c64c9b19690a072c620d7aff07d8f`.
  The later v0017 archive is byte-identical and remains unused.
- Deployment remains locked while platform v73 has only 7 of 12 minimum rated
  series; v72 remains the known-good rollback.

### Live score evaluated — 2026-08-09T21:25:42Z

- Version: 73
- Series: 7
- Score: 0.4857142857142857
- Adjusted score: -0.015069244937769153
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Seven reliability-clean rated series are below the 12-series minimum: v73 is 4-3 by series and 17-18 by games with net -3.38 Elo; meander is 0-2 live.


### Live observation captured — 2026-08-09T21:25:00Z

- Active version: 73
- Report: reports/live-observe-20260809T212442Z


### Live observation captured — 2026-08-09T21:20:20Z

- Active version: 73
- Report: reports/live-observe-20260809T212019Z


### Live observation captured — 2026-08-09T21:03:21Z

- Active version: 73
- Report: reports/live-observe-20260809T210321Z


### Live observation captured — 2026-08-09T20:57:38Z

- Active version: 73
- Report: reports/live-observe-20260809T205737Z


### v0016 remote gate and package — 2026-08-09T20:58:36Z

- Candidate: the exact 25x15 meander route-owner patch from
  `experiments/v73-meander-route-owner.md`.
- Remote gate: match `5c664cfa-5162-4bce-a117-487f92aafa8c`, candidate won
  3-2 against immutable v0015 on meander, moonrise, snowflake, saga, and
  lighthouse; all games completed without a server error or reported TLE.
  Evidence: `reports/remote-20260809T204654Z`.
- Package: v0016 at
  `artifacts/submissions/v0016_meander-route-owner_20260809-2058_eeafad8f.zip`,
  SHA-256 `7c83de94e62aeceff3f57b2ef1c46539533c64c9b19690a072c620d7aff07d8f`.
- Live safety: v73 remains active at 3/12 rated series with v72 rollback;
  observation capture `reports/live-observe-20260809T205737Z` found no new
  series, so v0016 was not uploaded or activated.


### v0016 selected regression hold — 2026-08-09T21:13:30Z

- The nine-map regression completed 54/54 command-clean against immutable v0015:
  candidate 30-24, 103,370 versus 108,680 titanium (0.9511x), zero TLE or
  suspicious-output markers, and 7,726 microseconds maximum callback.
- Evidence: `reports/local-20260809T210356Z`.
- Decision: hold v0016; the focused meander gain and remote 3-2 are outweighed
  by the aggregate collection regression. Platform v73 remains active at 3/12
  rated series with v72 rollback; v0016 remains packaged but inactive.


### Correction: v0016 selected regression attribution — 2026-08-09T21:19:00Z

- The preceding hold entry used the replay winner side when summing titanium,
  which swapped candidate and comparator on candidate-loss rows.
- Recomputed from the filename-side assignment in all 54 replay files:
  candidate 30-24, 112,260 versus 99,790 titanium (1.1250x), zero TLE or
  suspicious-output markers, peak callback 7,726 microseconds.
- Correct decision: the selected regression passes; v0016 is ready for guarded
  deployment after the active v73 observation resolves. Source evidence remains
  `reports/local-20260809T210356Z`.
- Aurora self-mirror was 6/6 command-clean and 3-3 by side (peak callback
  7,868 microseconds), confirming side variance; evidence:
  `reports/local-20260809T211550Z`.


### v73 meander route-owner continuity local gate — 2026-08-09T20:49:00Z

- Hypothesis: on the exact 25x15 geometry, a pre-income route owner ignores
  non-adjacent Builder-rush alerts while free workers respond; all other map
  geometries and post-income behavior remain unchanged.
- Files: `bots/candidate/bot/builder.py`,
  `tests/test_candidate_bootstrap_defense.py`, `scripts/analyze_replay.py`,
  `tests/test_analyze_replay.py`, and `experiments/v73-meander-route-owner.md`.
- Focused tests: 4/4 passed; compileall passed. Smoke: 4/4 command-clean,
  `reports/local-20260809T204830Z`.
- Targeted replay gate: 18/18 command-clean, candidate 13-5, titanium
  70,190 versus 35,020 (2.0037x), with meander first delivery on all six
  sides at turns 17-18. Full report: `reports/v73-meander-route-owner/summary.md`.
- Replay diagnostics: zero TLE markers, zero suspicious output, maximum
  callback 7,235 microseconds. `make static` retains inherited pre-v69 API and
  obsolete production-line failures; no new patch failure was observed.
- Status: local gate passed; remote gate and packaging deferred while the fcode
  API fails DNS. Platform v73 remains active and v72 remains rollback.

### Live score evaluated — 2026-08-09T20:45:20Z

- Version: 73
- Series: 3
- Score: 0.5333333333333333
- Adjusted score: 0.02170532257701781
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Three reliability-clean rated series are below the 12-series minimum: v73 is 2-1 by series and 8-7 by games with net +2.08 Elo.


### Live observation captured — 2026-08-09T20:44:56Z

- Active version: 73
- Report: reports/live-observe-20260809T204432Z


### Live score evaluated — 2026-08-09T20:31:39Z

- Version: 73
- Series: 2
- Score: 0.4
- Adjusted score: -0.06925831322457321
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: Two reliability-clean rated series are below the 12-series minimum: v73 is 1-1 by series and 4-6 by games with net -4.43 Elo.


### Live observation captured — 2026-08-09T20:31:14Z

- Active version: 73
- Report: reports/live-observe-20260809T203050Z


### Live observation captured — 2026-08-09T20:22:17Z

- Active version: 73
- Report: reports/live-observe-20260809T202159Z


### Live score evaluated — 2026-08-09T20:21:38Z

- Version: 73
- Series: 1
- Score: 0.2
- Adjusted score: -0.21182875985886485
- Reliability failures: 0
- Proposed decision: insufficient_data
- Reason: One reliability-clean rated series is below the 12-series minimum: v73 lost 1-4 to the one piece, with no match error or game resignation.


### Live observation captured — 2026-08-09T20:21:02Z

- Active version: 73
- Report: reports/live-observe-20260809T202043Z


### Live observation captured — 2026-08-09T20:15:32Z

- Active version: 73
- Report: reports/live-observe-20260809T201513Z


### Live observation captured — 2026-08-09T20:14:57Z

- Active version: 73
- Report: reports/live-observe-20260809T201437Z


### Live observation captured — 2026-08-09T20:13:19Z

- Active version: 73
- Report: reports/live-observe-20260809T201259Z


### Candidate activated — 2026-08-09T20:12:41Z

- Version: 73
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260809T201220Z


### Candidate uploaded — 2026-08-09T20:12:41Z

- Candidate: v0015-close-contact-bootstrap-defense-7dd72f03
- Version: 73
- Rollback target: 72
- Report: reports/live-deploy-20260809T201220Z


### Live candidate promoted — 2026-08-09T20:12:03Z

- Version: 72
- Live score: 0.6416666666666667
- Adjusted score: 0.11343448790107642
- Reason: 24 rated series: 18-6 series, 77-43 games, +87.12 Elo, positive opponent-adjusted residual, zero reliability failures


### Live observation captured — 2026-08-09T20:11:36Z

- Active version: 72
- Report: reports/live-observe-20260809T201118Z


### Live observation captured — 2026-08-09T20:10:16Z

- Active version: 72
- Report: reports/live-observe-20260809T200957Z


### Live observation captured — 2026-08-09T20:02:56Z

- Active version: 72
- Report: reports/live-observe-20260809T200236Z


### Live observation captured — 2026-08-09T19:57:17Z

- Active version: 72
- Report: reports/live-observe-20260809T195658Z


### Live observation captured — 2026-08-09T19:43:06Z

- Active version: 72
- Report: reports/live-observe-20260809T194245Z


### Live observation captured — 2026-08-09T19:37:09Z

- Active version: 72
- Report: reports/live-observe-20260809T193650Z


### Live score evaluated — 2026-08-09T19:20:39Z

- Version: 72
- Series: 19
- Score: 0.631578947368421
- Adjusted score: 0.106507331898
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: v72 is 14-5 in series and 60-35 in games with +64.76 Elo and positive opponent-adjusted residual, but only 19 of the required 24 series are complete


### Live observation captured — 2026-08-09T19:19:49Z

- Active version: 72
- Report: reports/live-observe-20260809T191930Z


### Live score evaluated — 2026-08-09T19:15:58Z

- Version: 72
- Series: 18
- Score: 0.6333333333333333
- Adjusted score: 0.106737896
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: v72 is 13-5 in series and 57-33 in games with +61.48 Elo and positive opponent-adjusted residual, but only 18 of the required 24 series are complete


### Live observation captured — 2026-08-09T19:10:47Z

- Active version: 72
- Report: reports/live-observe-20260809T191026Z


### Live observation captured — 2026-08-09T19:09:18Z

- Active version: 72
- Report: reports/live-observe-20260809T190900Z


### Live observation captured — 2026-08-09T19:07:54Z

- Active version: 72
- Report: reports/live-observe-20260809T190753Z


### Live observation captured — 2026-08-09T19:06:34Z

- Active version: 72
- Report: reports/live-observe-20260809T190615Z


### v0015 close-contact bootstrap defense packaged — 2026-08-09T19:04:30Z

- Files changed: `bots/candidate/bot/builder.py`, `tests/test_candidate_bootstrap_defense.py`, `experiments/v72-close-contact-bootstrap-defense.md`; rejected global variant recorded in `experiments/v72-single-bootstrap-defense.md`.
- Focused tests: 9/9 passed after self-review; compileall passed; smoke 4/4 command-clean. Logs: `reports/v72-close-contact-bootstrap-defense/` and `reports/local-20260809T184659Z`.
- Current-pool gate: recomputed 51-39 over 90 paired games, titanium 171,550 versus 168,040 (ratio 1.0209), zero command failures. Reports: `reports/local-20260809T184216Z`, `reports/local-20260809T184730Z`, and affected-map replacement `reports/local-20260809T185644Z`.
- Replay timing: 680,738 candidate calls, p99 2.975 ms, max 7.511 ms, zero TLEs.
- Remote gate: 4-1 and reliability-clean against immutable v0014; match `a4fdd82b-f5c1-449c-a809-473cdbdfde31`, report `reports/remote-20260809T190000Z`.
- Package: `artifacts/submissions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03.zip`, SHA-256 `fa5ec52b970998434ae80598e296ec6d7aca0afa872e26f26338f1e8ae8fcb1e`.
- Live: platform v72 remains active at 1358.24 Elo, rank 50/116; its 17-series sample is 13-4 series, 55-30 games, +62.27 Elo. Deployment waits for the configured 24-series known-good promotion threshold.
- Remaining risk: `make static` reproduces the inherited pre-v69 API/obsolete line-cap failures; meander remains side-sensitive locally.
- Iteration status: release gates passed and packaged; waiting for deterministic live observation unlock before upload/activation.

### Live observation captured — 2026-08-09T19:02:50Z

- Active version: 72
- Report: reports/live-observe-20260809T190227Z


### Live observation captured — 2026-08-09T18:24:04Z

- Active version: 72
- Report: reports/live-observe-20260809T182346Z


### Canonical-opening v0014 promoted and deployed as platform v72 — 2026-08-09T16:08:12Z

- Parent/baseline: immutable v0013/v69. Runtime change: `bots/candidate/bot/core.py` canonicalizes equal-score Core spawn and first-visible-ore ordering for current live geometries; ambiguous 16x16 and 25x25 layouts use observable Core quadrants. Focused coverage: `tests/test_candidate_opening_orientation.py`; experiment: `experiments/v69-canonical-opening.md`.
- Current synced 15-map pool, seeds 1/19/101, both sides: 61-29-0 (`+32/90`), titanium 178030 versus 142840 (ratio `1.2463`), 90/90 commands clean. Main reports: `reports/local-20260809T152902Z`, `reports/local-20260809T154538Z`; final 25x25 replacement: `reports/local-20260809T155537Z`.
- Old protected compatibility, recomputed from changed-map reruns: 27-21-0 (`+6/48`), titanium 130860 versus 108690 (ratio `1.2040`), no 0-6 map. Sources: `reports/local-20260809T153449Z`, `reports/local-20260809T154403Z`, `reports/local-20260809T155828Z`, and `reports/local-20260809T155537Z`.
- Validation: focused release suite 36/36; smoke 4/4; compile/package checks passed; archive 17 files/94125 bytes, SHA-256 `998c86506afdef96624348801aaf4dc8cb5dcac1a6e31bb3397a7cdbe36a70f3`. Full `make static` remains blocked by inherited pre-v69 API tests and its obsolete 3200-line assertion; log: `reports/release-v69-canonical-opening/static.log`.
- Remote gate `1c260f12-1141-41e0-a0c7-58e27090c771` was reliability-clean but 2-3 unpaired; exact server seeds scored 8-2 locally when side-swapped. Treat server/local outcome variance and future map-pool drift as observation risks.
- Packaged immutable baseline: `bots/versions/v0014_canonical-opening_20260809-1606_7dd72f03`; archive: `artifacts/submissions/v0014_canonical-opening_20260809-1606_7dd72f03.zip`.
- Platform v72 (`v0014-canonical-opening-7dd72f03`) is ready and active; v69 is ready and recorded as rollback. Initial snapshot: rating `1278.0199`, rank `58/116`, recent record `6-4`, with no v72-specific ladder series yet (`reports/live-observe-20260809T160750Z`). Status: LOCAL PROMOTION PASSED; LIVE ACTIVE_OBSERVING.

### Live observation captured — 2026-08-09T16:08:12Z

- Active version: 72
- Report: reports/live-observe-20260809T160750Z


### Candidate activated — 2026-08-09T16:07:37Z

- Version: 72
- Previous/rollback: 69
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260809T160717Z


### Candidate uploaded — 2026-08-09T16:07:36Z

- Candidate: v0014-canonical-opening-7dd72f03
- Version: 72
- Rollback target: 69
- Report: reports/live-deploy-20260809T160717Z


### Live candidate promoted — 2026-08-09T16:07:00Z

- Version: 69
- Live score: None
- Adjusted score: None
- Reason: v69 active platform comparator and immutable local baseline


### Live state bootstrapped — 2026-08-09T16:07:00Z

- Active version: 69
- Report: reports/live-bootstrap-20260809T160640Z


### Outcome-first reviewer comparison of new uploads v68 through v71 — 2026-08-09T14:45:07Z

- v68-v71 were downloaded under `reports/reviewer-new-uploads-20260809T142353Z/`; archive SHA-256 values and submission IDs are recorded in `experiments/reviewer-v68-v71-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v68 lost 3-45-0 (score `-42/48`) with zero candidate collection and 0-6 on every protected map except showdown (report `reports/local-20260809T142433Z`).
- v69 won 30-18-0 (score `+12/48`) with collection 252030 versus 241340 (ratio `1.0443`), no core outcomes, and no protected-map collapse (report `reports/local-20260809T143232Z`). It is preserved as immutable local baseline v0013.
- v70 won 25-23-0 (score `+2/48`) with collection ratio `0.9141` and collapsed 0-6 on string (report `reports/local-20260809T143248Z`).
- v71 lost 3-45-0 (score `-42/48`) with zero candidate collection and 0-6 on every protected map except showdown (report `reports/local-20260809T143303Z`).
- Status: v69 BASELINE PROMOTED; v68/v70/v71 REVIEWED — REJECTED. All 192 commands were clean. No platform activation was performed; v69 package/snapshot: `v0013_reviewer-v69-platform-winner_20260809-1444_7dd72f03`. Detailed record: `experiments/reviewer-v68-v71-20260809.md`.
- Final live observation shows v70 active externally, rating `1239.1252`, rank `59/116`, `555` matches, and recent record `0-10` (report `reports/live-observe-20260809T144444Z`).

### Live observation captured — 2026-08-09T14:45:07Z

- Active version: 70
- Report: reports/live-observe-20260809T144444Z


### Live observation captured — 2026-08-09T14:24:12Z

- Active version: 68
- Report: reports/live-observe-20260809T142353Z


### Outcome-first reviewer comparison of new uploads v66 and v67 — 2026-08-09T12:30:44Z

- v66 and v67 were downloaded under `reports/reviewer-new-uploads-20260809T121134Z/`; archive SHA-256 values and submission IDs are recorded in `experiments/reviewer-v66-v67-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v66 lost 21-27-0 (score `-6/48`) with collection 274720 versus 234200 (ratio `1.1730`), but collapsed 0-6 on aurora and strait (report `reports/local-20260809T121212Z`).
- v67 won 29-19-0 (score `+10/48`) with collection 282270 versus 309800 (ratio `0.9111`), but collapsed 0-6 on showdown (report `reports/local-20260809T122051Z`).
- Status: v66/v67 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 96 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v66-v67-20260809.md`.
- Final live observation shows v67 active externally, rating `1413.7503`, rank `45/114`, `542` matches, and recent record `6-4` (report `reports/live-observe-20260809T123025Z`).

### Live observation captured — 2026-08-09T12:30:44Z

- Active version: 67
- Report: reports/live-observe-20260809T123025Z


### Live observation captured — 2026-08-09T12:11:53Z

- Active version: 66
- Report: reports/live-observe-20260809T121134Z


### Outcome-first reviewer comparison of new uploads v64 and v65 — 2026-08-09T11:37:05Z

- v64 and v65 were downloaded under `reports/reviewer-new-uploads-20260809T110801Z/`; archive SHA-256 values and submission IDs are recorded in `experiments/reviewer-v64-v65-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v64 tied 24-24-0 (score `0/48`) with collection 291040 versus 293460 (ratio `0.9918`) and collapsed 0-6 on showdown (report `reports/local-20260809T111159Z`).
- v65 lost 15-33-0 (score `-18/48`) with collection 283890 versus 340840 (ratio `0.8329`) and collapsed 0-6 on crossfire, hive, and strait (report `reports/local-20260809T112215Z`).
- Status: v64/v65 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 96 valid commands were clean. An accidental v64 21-map release-matrix attempt was interrupted at game 14 and excluded (`reports/local-20260809T110854Z`). No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v64-v65-20260809.md`.
- Final live observation shows v65 active externally, rating `1422.3962`, rank `43/114`, `536` matches, and recent record `6-4` (report `reports/live-observe-20260809T113642Z`).

### Live observation captured — 2026-08-09T11:37:05Z

- Active version: 65
- Report: reports/live-observe-20260809T113642Z


### Live observation captured — 2026-08-09T11:08:24Z

- Active version: 65
- Report: reports/live-observe-20260809T110801Z


### Outcome-first reviewer comparison of new uploads v61 through v63 — 2026-08-09T10:14:14Z

- v61, v62, and v63 were downloaded under `reports/reviewer-new-uploads-20260809T094851Z/`; archive SHA-256 values are recorded in `experiments/reviewer-v61-v63-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v61 lost 21-27-0 (score `-6/48`) with collection 260930 versus 307940 (ratio `0.8473`) and collapsed 0-6 showdown/crossfire/hive (report `reports/local-20260809T094937Z`).
- v62 was the raw-outcome batch winner at 27-21-0 (score `+6/48`) with collection 302000 versus 307890 (ratio `0.9809`), but collapsed 0-6 twins and lost crossfire 1-5 (report `reports/local-20260809T100320Z`).
- v63 tied 24-24-0 (score `0/48`) with collection 293730 versus 293510 (ratio `1.0007`), but collapsed 0-6 showdown (report `reports/local-20260809T094944Z`).
- Status: v61/v62/v63 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 144 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v61-v63-20260809.md`.
- Final live observation shows v63 active externally, rating `1435.0250`, rank `43/113`, `528` matches, and recent record `6-4` (report `reports/live-observe-20260809T101349Z`). Final submission refresh found no v64+ upload.

### Live observation captured — 2026-08-09T10:14:14Z

- Active version: 63
- Report: reports/live-observe-20260809T101349Z


### Live observation captured — 2026-08-09T09:49:09Z

- Active version: 63
- Report: reports/live-observe-20260809T094851Z


### Outcome-first reviewer comparison of requested upload v60 — 2026-08-09T00:01:39Z

- v60 was downloaded under `reports/reviewer-new-uploads-20260808T234833Z/`; archive SHA-256 is recorded in `experiments/reviewer-v60-20260809.md`.
- v60 was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v60 was command-clean and won 30-18-0 (paired score `+12/48`) with collection 306710 versus 304490 (ratio `1.0073`) and six core wins, but collapsed 0-6 on hive and strait. Runner wall-clock p99/max was 28.3621/28.3621 seconds.
- Status: v60 REVIEWED — REJECTED by the hard map-floor guard; v0012/v28 remains the local immutable baseline. All 48 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v60-20260809.md`.
- Final live observation shows v60 active externally, rating `1413.3087`, rank `46/113`, `467` matches, and recent record `3-7` (report `reports/live-observe-20260809T000120Z`). Final submission refresh found no v61+ upload. v59 remains unevaluated after its interrupted partial matrix.

### Live observation captured — 2026-08-09T00:01:39Z

- Active version: 60
- Report: reports/live-observe-20260809T000120Z


### Live observation captured — 2026-08-08T23:48:51Z

- Active version: 60
- Report: reports/live-observe-20260808T234833Z


### Live observation captured — 2026-08-08T23:42:54Z

- Active version: 59
- Report: reports/live-observe-20260808T234236Z


### Outcome-first reviewer comparison of requested upload v58 — 2026-08-08T23:38:06Z

- v57 was intentionally skipped. v58 was downloaded under `reports/reviewer-new-uploads-20260808T232447Z/`; archive SHA-256 is recorded in `experiments/reviewer-v58-20260809.md`.
- v58 was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v58 was command-clean and won 27-21-0 (paired score `+6/48`) with collection 326730 versus 313960 (ratio `1.0407`), but collapsed 0-6 on twins and strait. Its runner wall-clock p99/max was 30.6348/30.6348 seconds.
- Status: v58 REVIEWED — REJECTED by the hard map-floor guard; v0012/v28 remains the local immutable baseline. All 48 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v58-20260809.md`.
- Final live observation shows v59 active externally, rating `1419.7381`, rank `45/113`, `465` matches, and recent record `5-5` (report `reports/live-observe-20260808T233806Z`). v59 appeared after the v58 review and was intentionally not evaluated; no v60+ upload was present.

### Live observation captured — 2026-08-08T23:38:29Z

- Active version: 59
- Report: reports/live-observe-20260808T233806Z


### Live observation captured — 2026-08-08T23:25:05Z

- Active version: 58
- Report: reports/live-observe-20260808T232447Z


### Outcome-first reviewer comparison of new uploads v54 through v56 — 2026-08-08T23:13:45Z

- Three unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T225637Z/`: v54, v55, and v56. Archive SHA-256 values are recorded in `experiments/reviewer-v54-v56-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v54 was command-clean but lost 14-34-0 (paired score `-20/48`) and collection 261640 versus 349020 (ratio `0.7496`), with 0-6 bridge/showdown/hive/aurora and 6-0 string (report `reports/local-20260808T225729Z`).
- v55 was command-clean but lost 13-35-0 (paired score `-22/48`) and collection 233500 versus 357470 (ratio `0.6532`), with three core losses, 0-6 bridge/showdown/hive/strait, and 4-2 aurora (report `reports/local-20260808T230122Z`).
- v56 was the batch best but still lost 21-27-0 (paired score `-6/48`) and collection 280440 versus 384350 (ratio `0.7296`); it won bridge 6-0 but collapsed 0-6 showdown/twins (report `reports/local-20260808T230127Z`).
- Status: v54/v55/v56 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 144 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v54-v56-20260809.md`.
- Final live observation shows v56 active externally, rating `1423.0620`, rank `44/113`, `462` matches, and recent record `6-4` (report `reports/live-observe-20260808T231328Z`). Final submission refresh found no v57 or later upload.

### Live observation captured — 2026-08-08T23:13:45Z

- Active version: 56
- Report: reports/live-observe-20260808T231328Z


### Live observation captured — 2026-08-08T22:56:58Z

- Active version: 56
- Report: reports/live-observe-20260808T225637Z


### Outcome-first reviewer comparison of new uploads v51 through v53 — 2026-08-08T11:03:38Z

- Three unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T103146Z/`: v51, v52, and v53. Archive SHA-256 values are recorded in `experiments/reviewer-v51-v53-20260808.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v51 was command-clean but lost 15-33-0 (paired score `-18/48`) and collection 241000 versus 323530 (ratio `0.7449`), with 0-6 showdown/crossfire/hive/aurora and 6-0 string (report `reports/local-20260808T103231Z`).
- v52 was command-clean but lost 16-32-0 (paired score `-16/48`) and collection 250220 versus 318650 (ratio `0.7853`); it won bridge/hive 6-0 but collapsed 0-6 twins/crossfire/aurora/strait, with runner wall-clock p99/max 32.6513/32.9255 seconds (report `reports/local-20260808T104218Z`).
- v53 was command-clean but lost 15-33-0 (paired score `-18/48`) and collection 240980 versus 323530 (ratio `0.7448`), matching v51's broad map collapses and 6-0 string lead (report `reports/local-20260808T105316Z`).
- Status: v51/v52/v53 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 144 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v51-v53-20260808.md`.
- Final live observation shows v52 active externally, v53 ready/inactive, rating `1387.2830`, rank `44/111`, `389` matches, and recent record `4-6` (report `reports/live-observe-20260808T110320Z`). Final submission refresh found no v54 or later upload.

### Live observation captured — 2026-08-08T11:03:38Z

- Active version: 52
- Report: reports/live-observe-20260808T110320Z


### Live observation captured — 2026-08-08T10:32:07Z

- Active version: 53
- Report: reports/live-observe-20260808T103146Z


### Reviewer refresh — no uploads newer than v50 — 2026-08-08T10:12:20Z

- Final submission refresh still shows v50 newest; no v51+ upload was available, so no new challenger download or 48-game matrix was run.
- The retained local baseline remains immutable v0012/v28. No source edits, upload, activation, or challenger test suite was performed.
- Fresh live observation shows v49 active externally at rating `1419.1461`, rank `43/111`, `384` matches, and a `7-3` recent ten-series record (report `reports/live-observe-20260808T101156Z`).

### Live observation captured — 2026-08-08T10:12:20Z

- Active version: 49
- Report: reports/live-observe-20260808T101156Z


### Outcome-first reviewer comparison of new uploads v47 through v50 — 2026-08-08T10:07:15Z

- Four unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T092716Z/` (v47/v48) and `reports/reviewer-new-uploads-20260808T094635Z/` (v49/v50). Archive SHA-256 values are recorded in `experiments/reviewer-v47-v50-20260808.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v47 was command-clean but lost 16-32-0 (paired score `-16/48`) and collection 211930 versus 321980 (ratio `0.6582`), with nine core losses and 0-6 showdown/twins/crossfire (report `reports/local-20260808T092838Z`).
- v48 was command-clean but lost 20-28-0 (paired score `-8/48`) and collection 244490 versus 322190 (ratio `0.7588`), with 0-6 showdown/twins (report `reports/local-20260808T093739Z`).
- v49 was command-clean but lost 21-27-0 (paired score `-6/48`) and collection 247220 versus 310620 (ratio `0.7959`); it won bridge 6-0 but collapsed 0-6 twins/string and had the slowest runner wall-clock p99/max (31.6368/32.0995 seconds) (report `reports/local-20260808T094719Z`).
- v50 was command-clean but lost 21-27-0 (paired score `-6/48`) and collection 280560 versus 355400 (ratio `0.7894`); it won showdown 6-0 but collapsed 0-6 crossfire/strait (report `reports/local-20260808T095716Z`).
- Status: v47/v48/v49/v50 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 192 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v47-v50-20260808.md`.
- Final live observation shows v49 active externally, v50 ready/inactive, rating `1417.7841`, rank `43/111`, `383` matches, and recent record `6-4` (report `reports/live-observe-20260808T100542Z`). Final submission refresh found no v51 or later upload.

### Live observation captured — 2026-08-08T10:06:01Z

- Active version: 49
- Report: reports/live-observe-20260808T100542Z


### Live observation captured — 2026-08-08T09:46:54Z

- Active version: 50
- Report: reports/live-observe-20260808T094635Z


### Live observation captured — 2026-08-08T09:27:34Z

- Active version: 48
- Report: reports/live-observe-20260808T092716Z


### Outcome-first reviewer comparison of new uploads v45 and v46 — 2026-08-08T09:03:53Z

- Two unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T084522Z/`: v45 (SHA-256 `8491f9602055ec7e40dbcf4899165bf4d12183dbeb16318824940b3e2b2e34d2`) and v46 (`fb8c609d1cc6975460b0e2052120ed55db0391396da493aec4d24a872e29b232`).
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v45 was command-clean but lost 19-29-0 (paired score `-10/48`) and collection 248600 versus 328020 (ratio `0.7579`); it collapsed 0-6 on bridge and strait (report `reports/local-20260808T084604Z`).
- v46 was command-clean but lost 13-35-0 (paired score `-22/48`) and collection 226640 versus 347820 (ratio `0.6516`); it had three candidate core wins but collapsed 0-6 on showdown, twins, crossfire, and string (report `reports/local-20260808T085453Z`).
- Status: v45/v46 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 96 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v45-v46-20260808.md`.
- Live observation shows v46 active externally at rating `1422.3161`, rank `43/111`, with recent record `3-7` (report `reports/live-observe-20260808T084522Z`). Final submission refresh found no v47 or later upload.

### Live observation captured — 2026-08-08T08:45:40Z

- Active version: 46
- Report: reports/live-observe-20260808T084522Z


### Outcome-first reviewer comparison of new uploads v43 and v44 — 2026-08-07T22:54:06Z

- Two unseen ready uploads were downloaded under `reports/reviewer-new-uploads-20260807T223624Z/`: v43 (SHA-256 `eace15c9fee38b7c2a2b017aa528d773d851c784f606c6369186fd0ab61ad74a`) and v44 (`8f1980d864943c823ba5b85f614c81e82897a91c6d90e18172c109866cd829a5`).
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v43 was command-clean but tied 24-24-0 (score `0/48`) and trailed collection 274820 versus 297500 (ratio `0.9238`); it won bridge/showdown/aurora but went 0-6 on twins/crossfire/string (report `reports/local-20260807T223704Z`).
- v44 was command-clean but lost 18-30-0 (score `-12/48`) and collection 239380 versus 343780 (ratio `0.6963`), with three core losses and 0-6 crossfire/string/aurora (report `reports/local-20260807T224539Z`). All 96 commands had empty stderr and no exception/TLE markers.
- Status: v43/v44 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed. Detailed record: `experiments/reviewer-v43-v44-20260808.md`.
- Live observation shows v44 active externally, rating `1456.0780`, rank `39/108`, `313` matches, and recent record `5-5` (report `reports/live-observe-20260807T223624Z`). Final submission refresh found no v45 or later upload.

### Live observation captured — 2026-08-07T22:36:42Z

- Active version: 44
- Report: reports/live-observe-20260807T223624Z


### Outcome-first reviewer comparison of new uploads v38 through v42 — 2026-08-07T22:31:42Z

- Five unseen ready uploads were downloaded under `reports/reviewer-new-uploads-20260807T214651Z/`: v38 (SHA-256 `ca27bbfb9438adb93e716eb9fd18af55185f0239b931d72c93345bedd4f59bc3`), v39 (`8dea1fbeccf462a470117595b1f6ff9595a6b9081d4315912594a9e92cce6a19`), v40 (`bad3919f7ba3af0a607c027828b454c256ace700e724d1ef0691a4c7286f05eb`), v41 (`50a2fb9aa5e415e3c7786d10814483d8e33e0e28ad7b2ca408c8f8a980a5f697`), and v42 (`42bfaab4a18ad373539884833e9c2e836a531a6eb1a99973afeb2539770680e5`).
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v38 was command-clean but lost 18-30-0 (score `-12/48`), collection ratio `0.7549`, no core wins, and 0-6 on showdown/hive (report `reports/local-20260807T214729Z`).
- v39 was command-clean but lost 13-35-0 (score `-22/48`), ratio `0.7212`, with three core losses and 0-6 on showdown/hive/aurora (report `reports/local-20260807T215633Z`).
- v40 was command-clean but lost 13-35-0 (score `-22/48`), ratio `0.7206`, with three core losses and the same 0-6 showdown/hive/aurora pattern (report `reports/local-20260807T220507Z`).
- v41 was closest but still lost 21-27-0 (score `-6/48`), ratio `0.9439`; it won all string/aurora games but lost 0-6 bridge/showdown/hive (report `reports/local-20260807T221344Z`).
- v42 was command-clean but lost 18-30-0 (score `-12/48`), ratio `0.8092`, with one core win versus three core losses and 0-6 showdown/twins (report `reports/local-20260807T222248Z`). All 240 commands had empty stderr and no exception/TLE markers.
- Status: v38/v39/v40/v41/v42 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed. Detailed record: `experiments/reviewer-v38-v42-20260807.md`.
- Live observation shows v42 active externally, rating `1444.2751`, rank `39/108`, `309` matches, and recent record `4-6` (report `reports/live-observe-20260807T214651Z`). Final submission refresh found no v43 or later upload.

### Live observation captured — 2026-08-07T21:47:10Z

- Active version: 42
- Report: reports/live-observe-20260807T214651Z


### Outcome-first reviewer comparison of new uploads v35 through v37 — 2026-08-07T14:15:27Z

- Three unseen ready uploads were found and downloaded under `reports/reviewer-new-uploads-20260807T134554Z/`: v35 (`c8bd27de-b622-495e-96ed-ce4b447012df`, SHA-256 `6a2e66fa60c4d746c2122975f58fddddf6ed186e30e45f657f9313a43c0bf78a`), v36 (`e236368b-1e0e-4f97-a127-f7c95282d917`, SHA-256 `813a3b5e3037005092bee10013c70ca6c14109c69da2714d98c08c514d607dc9`), and v37 (`22cee774-ff2a-4702-a1a8-688cc3d121fb`, SHA-256 `20da31812c4a9d888697062df025cd150f6eef01a437839988df74069531acc7`).
- Each candidate was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). The primary decision metric is paired outcome score; reliability/map guards are hard; titanium collection is secondary.
- v35 was command-clean but tied the primary outcome 24-24-0 (score `0/48`) and trailed collection 290480 versus 297110 (ratio `0.9777`), with no core wins (report `reports/local-20260807T134801Z`).
- v36 was command-clean but lost 14-34-0 (score `-20/48`) and collection 292090 versus 381820 (ratio `0.7650`), with no core wins (report `reports/local-20260807T135632Z`).
- v37 was command-clean but lost 18-30-0 (score `-12/48`) and collection 274270 versus 352330 (ratio `0.7784`); it had one core win to the baseline's zero, but went 0-6 on showdown and aurora (report `reports/local-20260807T140536Z`). All 144 commands had empty stderr and no exception/TLE markers.
- Status: v35/v36/v37 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer. Detailed record: `experiments/reviewer-v35-v37-20260807.md`.
- Fresh live observation shows v37 active externally, team rating `1459.6548`, rank `37/106`, `261` matches, and recent record `6-4` (report `reports/live-observe-20260807T134554Z`). This remains observation-only and does not change the local decision.
- Final read-only submission-list refresh after the matrix still showed v37 as the newest upload; no v38 or later candidate appeared (`reports/reviewer-new-uploads-20260807T134554Z/submissions-final.json`).

### Live observation captured — 2026-08-07T13:46:14Z

- Active version: 37
- Report: reports/live-observe-20260807T134554Z


### Outcome-first reviewer comparison of new uploads v33 and v34 — 2026-08-07T12:16:29Z

- The reviewer rule is now outcome-first: paired game result (+1/0/-1) is primary, reliability and map floors are guards, and titanium collection is secondary margin; the full 210-game/55% gate remains deferred in this reviewer-only screening pass.
- New unseen uploads v33 (id 3dd459a2-2432-4572-b739-ef6f869eb593, platform name 2) and v34 (id b266e6a4-6d89-46de-9b9c-239a4fcb1f7c, platform name 1) were downloaded with fcode under reports/reviewer-new-uploads-20260807T115121Z/. Archive SHA-256 values: v33 eb038fccc0311f860ef4288ba32c83acb57328dbf18d9255c66c320fbad13a00; v34 0351d675d0db1449766a54b92e1a4233260bd2357278dc23003df885a1a2d980.
- v33 direct battle against retained v0012/v28 was command-clean but lost on the primary outcome metric: 20-28-0, paired score -8/48, with 266940 versus 354480 collected titanium (ratio 0.7530); it led bridge and strait but went 0-6 on crossfire and twins and had no core wins (report reports/local-20260807T115214Z).
- v34 direct battle against the same v0012/v28 baseline was command-clean but lost: 12-36-0, paired score -24/48, with 232610 versus 302070 collected titanium (ratio 0.7701); it led only aurora and hive, had one candidate core win against six baseline core wins, and runner wall p99/max 36.9351/37.0020 seconds (report reports/local-20260807T120117Z).
- Fresh live observation reports v33 active externally with platform name 2 and v34 ready/inactive with platform name 1; team rating 1458.8214, rank 37/105, 250 matches, and 6-4 over the last ten series. The newest completed v33 series was a 1-4 loss versus The Bisons; no v34-specific series was visible (report reports/live-observe-20260807T115121Z).
- Status: v33/v34 REVIEWED — REJECTED under the outcome-first rule; v0012/v28 retained as local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform v33 remains pre-existing.


### Live observation captured — 2026-08-07T11:51:40Z

- Active version: 33
- Report: reports/live-observe-20260807T115121Z


### Reviewer comparison of new uploads v31 and v32 — 2026-08-07T11:44:32Z

- New unseen uploads v31 (id 4e739154-d792-4cdb-8184-de55c1df67b4, platform name 2) and v32 (id b18c7ce3-a2d8-4e9d-973b-e964acf9862b, platform name 1) were downloaded with fcode under reports/reviewer-new-uploads-20260807T111917Z/. Archive SHA-256 values: v31 9d32fd7268d4064397ae5566aadfa71b8a43b9ce202ff8f0fd62944361260802; v32 b1b3bd7fec430b4fa63c76961711d55d6e9bb3107d0153bbf7531dff7e70961d.
- v31 direct battle against retained v0012/v28 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 264120 versus 314810 collected titanium, ratio 0.8390, 26/48 wins and no ties (report reports/local-20260807T111956Z). It led bridge, aurora, hive, and strait but collapsed on twins, crossfire, showdown, and string; no core wins.
- v32 direct battle against the same v0012/v28 baseline was command-clean but lost: 232910 versus 302050 collected titanium, ratio 0.7711, 12/48 wins and no ties (report reports/local-20260807T112918Z). It led only aurora and hive, suffered six core-destruction losses, and had runner wall p99/max 37.0890/37.2008 seconds.
- Fresh live observation reports v31 active externally with platform name 2 and v32 ready/inactive with platform name 1; team rating 1454.2884, rank 37/105, 246 matches, and 5-5 over the last ten series. No completed v31/v32-specific series was visible; the latest completed visible matches still used v30 (report reports/live-observe-20260807T111917Z).
- Status: v31/v32 REVIEWED — REJECTED; v0012/v28 retained as local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform v31 remains pre-existing.


### Live observation captured — 2026-08-07T11:19:38Z

- Active version: 31
- Report: reports/live-observe-20260807T111917Z


### Reviewer comparison of new uploads v27 through v30 — 2026-08-07T11:01:11Z

- New ready uploads v27 (id 2a5ce2f2-36a3-4d42-958a-7d0c37aa0c22), v28 (id 744fcf8a-227f-4813-9d95-e030ea11058c), v29 (id cc441a04-f7f0-4cc1-9e0e-90449d413e1a), and v30 (id 67f3da13-04b9-4d5c-9a3b-f412f8d8eb6e) were downloaded with fcode under reports/reviewer-new-uploads-20260807T101605Z/. Archive SHA-256 values: v27 c3be16e40be4f6705c3d3e107bb247f6b98f22f99bb38a54dfcbaea16a05b43b; v28 b0d31171ab63db311a74e614113370fec21d15c7e8b6d3bfcf24d26f9470eb8d; v29 9703169531048031023a7dea7bfe5a50a38ef3c02a8d7b9452001d7fdbe9fc6c; v30 c10ec08d21d63b81b3f6f11def1f8cc0550932bf6a173bb5da50f5f092df3fe0.
- v27 direct battle against retained v0011/v23 was command-clean but lost: 315910 versus 325110 collected titanium, ratio 0.9717, 18/48 wins and no ties (report reports/local-20260807T101651Z). It led bridge/showdown/twins/crossfire but lost aurora and strait.
- v28 direct battle against retained v0011/v23 was command-clean and won: 379720 versus 301460 collected titanium, ratio 1.2596, 24/48 wins and no ties (report reports/local-20260807T102644Z). It led showdown/twins/crossfire/hive/aurora/strait; bridge was near-even and string was its main weakness.
- v29 direct battle against the promoted v0012/v28 baseline was command-clean but lost: 299420 versus 376850 collected titanium, ratio 0.7945, 24/48 wins and no ties (report reports/local-20260807T103632Z). It led only aurora and regressed heavily on twins/showdown.
- v30 direct battle against the same v0012/v28 baseline was command-clean but lost: 232380 versus 303350 collected titanium, ratio 0.7660, 12/48 wins and no ties (report reports/local-20260807T104536Z). It led only aurora, collapsed on bridge/showdown/string/strait, lost six core-destruction games, and had runner wall p99/max 35.2974/35.3263 seconds.
- Winner validation for v28 passed: all 16 Python files AST-parsed with one explicit main.py Player class; immutable snapshot bots/versions/v0012_reviewer-v28-platform-winner_20260807-1035_7dd72f03 and package artifacts/submissions/v0012_reviewer-v28-platform-winner_20260807-1035_7dd72f03.zip were created, package SHA-256 02647f175571e7c3d8aa3fdc9f15e6d038bb496072b74227fd0d5290b344d669, and packaged smoke was 4/4 command-clean (reports/local-20260807T103603Z).
- Fresh live observation reports v30 active and ready externally, v27/v28/v29 ready/inactive, team rating 1474.5293, rank 35/105, 240 matches, and 5-5 over the last ten series. The latest completed series used v29 (1-4 versus I Stone); no completed v30-specific series was visible (report reports/live-observe-20260807T101605Z).
- Status: v28 REVIEWED — PROMOTED TO LOCAL IMMUTABLE BASELINE; v27/v29/v30 REVIEWED — REJECTED. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform v30 remains pre-existing.


### Live observation captured — 2026-08-07T10:16:25Z

- Active version: 30
- Report: reports/live-observe-20260807T101605Z


### Reviewer comparison of new uploads v25 and v26 — 2026-08-07T00:39:10Z

- New ready uploads v25 (id e1f69d69-c77c-4666-a54e-a9edb07445c4, uploaded 2026-08-06T23:29:37.305Z) and v26 (id 5c6e0acf-1788-4e30-add2-0f6cb20ef72f, uploaded 2026-08-06T23:42:14.200Z) were downloaded with fcode under reports/reviewer-new-uploads-20260807T002021Z/. Archive SHA-256 values: v25 48f24f52a9c5d04a35371570bc97c441a311ce6583d5b7b4c2abdb7945ab41b5; v26 7692706930af73c43db3855e71189e030f59773f6867895578c99987a96b5cef.
- v25 direct battle against retained v0011/v23 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 219190 versus 253790 collected titanium, ratio 0.8637, 21/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260807T002102Z). v25 improved hive and aurora and recorded three core-destruction wins, but collapsed on showdown and string.
- v26 direct battle against the same v0011/v23 baseline was command-clean but lost: 226630 versus 265380 collected titanium, ratio 0.8540, 20/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260807T002942Z). v26 led hive and aurora but collapsed on bridge, showdown, string, and strait; it had no core-destruction wins.
- Fresh live observation reports v26 active and ready externally, v25 ready/inactive, team rating 1402.8394, rank 39/104, 177 matches, and 4-6 over the last ten series. The latest completed series was v25 losing 0-5 to the one piece; no completed v26-specific series was visible (report reports/live-observe-20260807T002021Z).
- Status: v25 and v26 REVIEWED — REJECTED FOR BASELINE; immutable v0011/v23 remains the local reviewer baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; the external platform remains on pre-existing v26.


### Live observation captured — 2026-08-07T00:20:40Z

- Active version: 26
- Report: reports/live-observe-20260807T002021Z


### Reviewer comparison of new uploads v23 and v24 — 2026-08-06T23:43:53Z

- New ready uploads v23 (id 2ba7a808-3fff-42de-b6de-b6c4d847eaa8, uploaded 2026-08-06T22:38:42.481Z) and v24 (id c8f72d03-f751-4f49-a269-b6606f728afa, uploaded 2026-08-06T22:48:45.615Z) were downloaded with fcode under reports/reviewer-new-uploads-20260807T232604Z/ and reports/reviewer-new-uploads-20260807T233108Z/. Archive SHA-256 values: v23 92f66a5311048cdd45ba7313f367ac6a26af173bd814d0a5dc0fbbd40d1f9122; v24 79a90d0c0fb1e94fb4933c0c7f05e2e675e55b959d0e8172058c962818de8292.
- v23 direct battle against retained v0010/v20 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean and won the collection gate: 240680 versus 228650 collected titanium, ratio 1.0526, 17/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T232644Z). v23 led bridge, showdown, twins, crossfire, and strait, but regressed on hive, aurora, and string and lost the raw game count 17-31. All 17 wins were by titanium collection; v23 had 19 collection losses and 12 core-destruction losses, with no core-destruction wins.
- v24 direct battle against the same v0010/v20 baseline was command-clean but lost: 152540 versus 168170 collected titanium, ratio 0.9071, 22/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T233452Z). v24 led bridge, crossfire, and strait narrowly but collapsed on showdown, twins, and string.
- Winner validation for v23 passed: all 16 Python files AST-parsed with one explicit main.py Player class; immutable snapshot bots/versions/v0011_reviewer-v23-platform-winner_20260806-2342_7dd72f03 and package artifacts/submissions/v0011_reviewer-v23-platform-winner_20260806-2342_7dd72f03.zip were created, package SHA-256 723bcf98f10366036b3208dfc45e6fac31a541978d2bc17464f806f476dd5657, and packaged smoke was 4/4 command-clean (reports/local-20260806T234216Z).
- Fresh live observation reports v23 active and ready externally, v24 ready/inactive, and team status rating 1425.6293, rank 37/104, 172 matches, and 6-4 over the last ten series. The latest observed v23 series was a 5-0 win over Kvarnholmen (reports/live-observe-20260806T233108Z).
- Status: v23 REVIEWED — PROMOTED TO LOCAL IMMUTABLE BASELINE; v24 REVIEWED — REJECTED. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform state remains v23.


### Live observation captured — 2026-08-06T23:31:25Z

- Active version: 23
- Report: reports/live-observe-20260806T233108Z


### Live observation captured — 2026-08-06T23:26:25Z

- Active version: 23
- Report: reports/live-observe-20260806T232604Z


### Reviewer comparison of new uploads v21 and v22 — 2026-08-06T23:22:50Z

- New ready uploads v21 (id 36a7ff00-8cd5-4409-9698-57162b62cb8b, uploaded 2026-08-06T22:16:46.027Z; active externally at inspection) and v22 (id 948bffc1-0de9-4796-9557-88fa570f2a41, uploaded 2026-08-06T22:27:25.733Z; ready/inactive) were downloaded with fcode under reports/reviewer-new-uploads-20260807T231003Z/. Archive SHA-256 values: v21 6571049205e79ca3444c862518ef9e36ef9e1f02885a97c6198d19b671d74da6; v22 b2a6016af031ae3a0163d429c855c44f18dc6ea1f10bb88ed0e83ed0f6aee115.
- v21 direct battle against retained v0010/v20 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 136,150 versus 167,650 collected titanium, ratio 0.8121, 22/48 wins with three ties; zero stderr/exception/TLE markers (report reports/local-20260806T231050Z). v21 led crossfire, hive, and twins, but regressed sharply on bridge, showdown, and string.
- v22 direct battle against the same retained v0010/v20 baseline was command-clean but lost: 124,880 versus 131,640 collected titanium, ratio 0.9486, 15/48 wins with six ties; zero stderr/exception/TLE markers (report reports/local-20260806T231630Z). v22 led aurora, bridge, and strait, but collapsed on crossfire and string and tied all six showdown games.
- Fresh live observation reports v21 active externally at rating 1421.4360, rank 37/104, 170 matches, and 7-3 over the last ten series. Its latest series beat Bean counters 3-2 across moonrise/eider/hive/archipelago/drumlin; v22 remains inactive. Report: reports/live-observe-20260806T231003Z.
- Status: v21 and v22 REVIEWED — REJECTED FOR BASELINE; immutable v0010/v20 remains the local reviewer baseline. No challenger suites, source edits, upload, or activation were performed.


### Live observation captured — 2026-08-06T23:10:21Z

- Active version: 21
- Report: reports/live-observe-20260806T231003Z


### Live observation after v19 activation — 2026-08-06T22:33:42Z

- Fresh read-only fcode observation reports active external version 19; v20 is ready but inactive. Report: reports/live-observe-20260806T221248Z.
- Current team status is rating 1384.7777, rank 40/104, 163 matches, and 6-4 over the last ten series. The latest v19 series beat Prompt Engineers Anonymous 5-0, with wins on jackpot, atoll, snowflake, nordkap, and fjordgate; jackpot and fjordgate ended by core destruction, while the other three ended by titanium collection or storage.
- This live result is promising but is only one v19 series and does not override the 48-game local comparison, where v19 lost to v0010/v20. No platform activation was performed by the reviewer.


### Reviewer comparison of new uploads v19 and v20 — 2026-08-06T22:31:37Z

- New ready uploads v19 (id 1ce9f9d8-fe24-404f-bfa4-b2e71fde4847, uploaded 2026-08-06T21:09:15.569Z; active externally at inspection) and v20 (id 572e0c76-8d06-4358-baee-af765a702b57, uploaded 2026-08-06T21:24:58.819Z; ready/inactive) were downloaded with fcode under reports/reviewer-new-uploads-20260807T221248Z/. Archive SHA-256 values: v19 b2095202ae968aed014a4fbdfe24776925227d0e8147fc071fe4b9e85db38af8; v20 d4b63a0f5164f98a7db31f0348d6b91690b1cd1a27779c99c231e999a1392e91.
- v19 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 109,890 versus 132,150 collected titanium, ratio 0.8316, 24/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T221414Z). v19 led bridge, showdown, and string, but trailed heavily on crossfire, hive, and strait.
- v20 direct battle against the same retained v0009/v14 baseline was command-clean and won: 187,750 versus 102,100 collected titanium, ratio 1.8389, 32/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T222101Z). v20 led bridge, showdown, twins, crossfire, hive, aurora, and strait, with string as its only losing map.
- Winner validation passed: all 16 Python files AST-parsed with an explicit main.py Player class; immutable package v0010_reviewer-v20-platform-winner_20260806-2229_7dd72f03 is 16 files/200,497 unpacked bytes/50,894 archive bytes with SHA-256 ebe54c75e3ad7abf0338b393b820d81e354e51f7c1577d8edf9ee1796232be29; packaged smoke was 4/4 command-clean (reports/local-20260806T222949Z).
- v20 runner wall-clock p99/max were 19.7662/19.9528 seconds per game; the local runner does not expose controller CPU p99. No bot-source edits, new upload, or activation was performed by the reviewer; the platform remains externally active on v19.
- Status: v19 rejected as local comparator; v20 retained as the new immutable local reviewer baseline pending separate live observation.


### Live observation captured — 2026-08-06T22:13:15Z

- Active version: 19
- Report: reports/live-observe-20260806T221248Z


### Live observation after v17/v18 review — 2026-08-06T17:26:43Z

- Fresh read-only fcode observation reports active external version 16 (V0011_scenario); v17 and v18 are ready but inactive. Report: reports/live-observe-20260806T172454Z.
- Current team status is rating 1355.6550, rank 40/103, 132 matches, and 6-4 over the last ten series. The two newest v16 series were 1-4 versus PromptNPray and 1-4 versus Atlas; no activation was performed by the reviewer.
- The latest Atlas series ended on titanium collection in fjordgate, snowflake, heart, and drumlin, with one v16 core-destruction win on moonrise at turn 771. The PromptNPray series likewise had one v16 moonrise core-destruction win and four collection losses.


### Live observation captured — 2026-08-06T17:25:12Z

- Active version: 16
- Report: reports/live-observe-20260806T172454Z


### Reviewer comparison of new uploads v17 and v18 — 2026-08-06T17:24:36Z

- New ready uploads v17 (id 87faf1eb-e97d-42b4-b962-dade8d3136a4, uploaded 2026-08-06T15:52:09.262Z) and v18 (id 550767b7-1414-4df8-9263-a5a7494505cd, uploaded 2026-08-06T15:55:58.939Z) were downloaded without challenger unit/static/smoke suites under reports/reviewer-new-uploads-20260806T171055Z/. Archive SHA-256 values: v17 2d206bf71d08ebf99272e486c7dcaf55e1eabad84d14f91fae263de5f9606d43; v18 2644278a8ba91a56cdc96ea249b92e05b27183aee02b62ed99e148f36b1656c2.
- v17 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 91,970 versus 95,310 collected titanium, ratio 0.9650, 24/48 wins and 27/48 positive-or-equal with three ties; zero stderr/exception/TLE markers (report reports/local-20260806T171101Z). v17 led bridge, aurora, and strait, but trailed crossfire, hive, twins, and string; showdown was a 5,070 versus 0 candidate-side total.
- v18 direct battle against the same retained v0009/v14 baseline was command-clean but lost: 94,830 versus 101,280 collected titanium, ratio 0.9363, 21/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T171729Z). v18 led bridge, showdown, twins, crossfire, and hive, but was weak on aurora, strait, and especially string.
- Runner wall-clock p99/max were 13.5050/13.5812 seconds for v17 and 20.9226/21.0511 seconds for v18; the local runner does not expose controller CPU p99. No challenger tests, activation, upload, or bot-source changes were performed.
- Status: v17 and v18 REVIEWED — REJECTED FOR BASELINE; immutable v0009/v14 remains the reviewer baseline.


### Live observation captured after v16 review — 2026-08-06T15:17:49Z

- Active version: 14; report: reports/live-observe-20260806T151713Z
- Current team status: rating **1260.25**, rank **47/103**, recent record **7-3** over the last ten series. The latest v14 series was **1-4** versus StarTrekker; v15 and v16 remain inactive.


### Live observation captured — 2026-08-06T15:17:31Z

- Active version: 14
- Report: reports/live-observe-20260806T151713Z


### Reviewer comparison of new upload v16 — 2026-08-06T15:16:12Z

- New ready upload v16 `V0011_scenario` was downloaded without challenger unit/static/smoke suites under `reports/reviewer-new-uploads-20260806T150832Z/`; archive SHA-256 is `9ddf84c43dad24e22957fbdc8355b43b4b592e74eaa3e040534898ed565f07bf`.
- v16 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: **117,480** versus **150,840** collected titanium, ratio **0.7788**, **15/48** wins (**18/48** positive-or-equal with three ties), zero stderr/exception/TLE markers (report `reports/local-20260806T150838Z`). v16 led bridge and aurora, was close on crossfire, and trailed heavily on showdown, hive, string, twins, and strait.
- The platform remains on active v14; at inspection the team was rating **1272.87**, rank **47/103**, and **8-2** over the last ten series. No v16 activation or source change was performed.
- Status: **v16 REVIEWED — REJECTED FOR BASELINE; v0009/v14 RETAINED.**


### Live observation captured after v15 review — 2026-08-06T15:00:38Z

- Active version: 14; report: reports/live-observe-20260806T145957Z
- Current team status: rating **1257.64**, rank **47/103**, recent record **7-3** over the last ten series. The latest v14 series in the snapshot was **4-1** versus Klarum; v15 remained inactive.


### Live observation captured — 2026-08-06T15:00:21Z

- Active version: 14
- Report: reports/live-observe-20260806T145957Z


### Reviewer comparison of new upload v15 — 2026-08-06T14:59:02Z

- New ready upload v15 `V0009_farmfirst` was downloaded without challenger unit/static/smoke suites under `reports/reviewer-new-uploads-20260806T144942Z/`; archive SHA-256 is `d9d9cf06da71f9d8cdc43ea0c68acb3baba192434576f91666cafa543f8ab4e4`.
- v15 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: **192,530** versus **250,080** collected titanium, ratio **0.7699**, **15/48** wins, zero stderr/exception/TLE markers (report `reports/local-20260806T144947Z`). v15 led bridge and string, was roughly even on strait, and trailed heavily on showdown, twins, hive, aurora, and crossfire.
- The platform remains on active v14; no v15 activation or source change was performed. v0009/v14 remains the local reviewer baseline.
- Status: **v15 REVIEWED — REJECTED FOR BASELINE; v0009/v14 RETAINED.**


### Reviewer comparison of new uploads v13 and v14 — 2026-08-06T14:47:10Z

- New ready uploads v13 `V0008mapaware` and v14 `V0010_runtimeapi` were downloaded without challenger unit/static/smoke suites under `reports/reviewer-new-uploads-20260806T142952Z/`. Archive SHA-256 values: v13 `c5cd172375b9e7ebf1d993556294bbe8b0e35bc68a09ef2eed20e901d0740c1b`, v14 `622f0ca76d2ed2b49ae94a2d91a67829aa809634751728986d5049aa2de497c1`.
- v13 direct battle against v0008 was command-clean but lost: **139,590** versus **182,280** collected titanium, ratio **0.7658**, **18/48** wins, zero stderr/exception/TLE markers (report `reports/local-20260806T142959Z`). It was especially weak on showdown (0), crossfire, string, and twins; only hive was strongly positive.
- v14 direct battle against v0008 was command-clean and won: **105,350** versus **74,860** collected titanium, ratio **1.4073**, **29/48** wins, zero stderr/exception/TLE markers (report `reports/local-20260806T143942Z`). v14 led crossfire, hive, strait, string, and twins; it trailed on bridge, aurora, and showdown.
- Fresh live observation `reports/live-observe-20260806T144506Z` shows v14 active and ready with rating **1244.95**, rank **48/103**, recent record **7-3**. Its newest completed series was **5-0** versus 1337; all five games ended by `core_destroyed` between 322 and 900 turns. This is promising but still only one v14 series.
- The winning v14 archive was snapshotted as immutable local baseline `bots/versions/v0009_reviewer-v14-platform-winner_20260806-1446_7dd72f03`; package SHA-256 `b013b1214b7832a30600166985e5a569515bb593509bb5d4773a95f66c6c6a11` and manifest are under `artifacts/submissions/`. No bot source was edited and no activation was performed by the reviewer; v14 was already externally active.
- Status: **NEW-UPLOAD REVIEW COMPLETE — v0009/v14 retained as baseline; continue live observation for map and reliability variance.**


### Live observation captured — 2026-08-06T14:45:24Z

- Active version: 14
- Report: reports/live-observe-20260806T144506Z


### Reviewer comparison of new uploads v11 and v12 — 2026-08-06T14:18:28Z

- New ready uploads were reviewed without challenger unit, static, smoke, or other test suites: v11 `v0007_mass-build` (archive SHA-256 `74095a3bdedfe4e0fa645c450d061447a54449a78a5e14aa4fd28148ac15c1c9`) and v12 `V0009workforce` (archive SHA-256 `45b1e8df3ba7f79ed9a8e8ac1a862a0f2fc18090b2977b4f49ff299c29b218a4`); downloads/extractions are under `reports/reviewer-new-uploads-20260806T1329Z/`.
- v11 direct battle against retained local v0008 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean: **177,820** versus **182,070** collected titanium, ratio **0.9767**, **24/48** wins and **24/48** positive-or-equal rows, zero stderr/exception/TLE markers (report `reports/local-20260806T140632Z`). v11 was not retained as baseline.
- v12 was harness-invalid before gameplay in all 48 invocations: `bot/builder.py:1884` contains a forbidden `finally` block (rc 10/11; report `reports/local-20260806T141621Z`). No score was assigned and no challenger tests were run. The platform also recorded a rated v12 0-5 compilation-error series versus OpenSverige before returning to active v11.
- Fresh platform observation `reports/live-observe-20260806T141701Z` shows v11 currently active and ready, rating **1220.75**, rank **51/103**, recent record **4-6**. Its only completed rated series was **2-3** versus Kvarnholmen (lighthouse/snowflake/moonrise/drumlin/archipelago; two core-destroyed wins, three titanium losses). This is weak live evidence and does not displace the local v0008 baseline or authorize activation.
- Status: **NEW-UPLOAD REVIEW COMPLETE — v0008 retained; v11/v12 not promoted; no bot source changes.**


### Live observation captured — 2026-08-06T14:17:24Z

- Active version: 11
- Report: reports/live-observe-20260806T141701Z


### External platform version switch observed — 2026-08-06T13:26:50Z

- Fresh report reports/live-observe-20260806T132442Z shows platform version 9 active and ready; this differs from the reviewer-activated v10. No v9 activation was performed in this workflow, so the switch is recorded as external and v9 is not treated as the approved winner.
- The latest completed ladder series is 5-0 for 1337 over Kleos while Kleos was still on version 8. The two recorded v10 series remain 3-2 versus Leviathan and 0-5 versus Albert And Einstein; no completed series in the latest 100 references v9.
- Current team status is rating 1200.84, rank 52/103, and 3-7 over the last ten series. Local baselines, tests, the v10 package, and the draft PR are unchanged; no platform reactivation was performed.


### Live observation captured — 2026-08-06T13:25:04Z

- Active version: 9
- Report: reports/live-observe-20260806T132442Z


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


### v99 loaded-belt sabotage checkpoint — 2026-08-14

- Parent/local baseline: immutable platform v98 snapshot
  `bots/versions/v0027_early-two-sentinel-shell_20260813-1831_eeafad8f`; live
  rollback remains v72.
- Changed file: `bots/candidate/bot/attacker.py`; loaded conveyor/splitter
  targets now receive a 200-point urgency bonus while harvester/splitter/
  conveyor base priorities remain 300/250/200.
- Win-rate metric: prefilter 36-18 (66.7%) in
  `reports/local-20260814T030907Z`; full 21-map release gate 116-94
  (55.24%), 0 ties, 0 command failures in
  `reports/local-20260814T031536Z`.
- Replay report: `reports/iter-v99-loaded-sabotage-replay-analysis.json`;
  wins averaged 7.16 placed harvesters versus 5.68 in losses.  Bridge,
  sprint, and vault were the weakest maps at 3-7 each.
- Checks: Python compile passed; `make smoke` passed 4/4 in
  `reports/local-20260814T031517Z`; `make static` remains non-green only
  because of 15 inherited obsolete test-import errors, recorded in
  `reports/iter-v99-loaded-sabotage-static.log`.
- Status: release candidate pending remote gate/package.  Risks are weak
  cramped-map floors and persistent side asymmetry.  Next hypothesis is a
  first-delivered-route gate for forward Sentinel placement, retaining this
  loaded-line raid priority.


### v99 remote gate rejected — 2026-08-14

- Remote test `9d20d76b-1b17-40b8-8b5d-763a49df0eff` completed 1-4 against
  v98 on sprint, bridge, crossfire, vault, and aurora; no server reliability
  error was reported.  Evidence: `reports/remote-v99-loaded-sabotage.log`,
  `reports/remote-v99-loaded-sabotage-match.json`.
- Downloaded and analyzed all five server replays under
  `reports/remote-v99-loaded-sabotage-replays/`; the losses showed late
  delivery on sprint (157), an economy deficit on bridge (4 versus 6
  harvesters), and lower loaded throughput on the larger maps.  This is a
  transfer failure, not a local crash/TLE.
- Immutable package preserved for audit:
  `artifacts/submissions/v0028_loaded-belt-sabotage_20260814-0344_eeafad8f.zip`
  (SHA-256 `7a448fae4be4e8a734bb7d3f73340d37deafd0a9219f001e751a4d82e3e38b0b`).
- Decision: do not activate v99.  Keep v98 as the comparator and v72 as live
  rollback; repair the route-first opening before another remote gate.


### v100 promoted for live observation — 2026-08-14

- Candidate package: `artifacts/submissions/v0029_first-delivery-loaded-sabotage_20260814-0417_eeafad8f.zip`
  (SHA-256 `38674d1ded5e25426dd89d674ff9655d53c7a05c05fda36b2aa02e76728a8992`).
- Guarded operator uploaded and activated platform version 99 under
  `v0029-first-delivery-loaded-sabotage-eeafad8f`; report
  `reports/live-deploy-20260814T041804Z`.  Previous active v98 and rollback v72
  are preserved.  State is `active_observing`; no live score is claimed yet.
- Immediate status/capture passed: `reports/live-status-v100-first-delivery.log`
  and `reports/live-post-v100-first-delivery-20260814T041906Z`.
- Remaining live risk: the capture predates the first v99 ladder match.  Wait
  for attributable v99 series before any live promotion/rollback decision.


### v101 first-route danger bypass rejected — 2026-08-14

- Hypothesis: let a builder's first conveyor chain ignore visible turret danger
  until the first completed chain, preventing no-delivery stalls on vase.
- Affected-map slice improved to 9-11 on vase/skerry
  (`reports/local-20260814T043000Z`), but the remote server gate
  `2d189f7f-e0ef-4fff-9402-1d31046d02d8` scored 2-3 versus v98.  The remote
  replay set is preserved under
  `reports/remote-v101-first-route-danger-replays/`; first deliveries were
  early, but sprint/crossfire/vault combat losses outweighed the route gain.
- No full matrix, package, or deployment was performed.  The candidate was
  restored byte-for-byte to the active v100 source (only the loaded-belt
  attacker change remains versus v98).  Keep platform v99 active observing
  with v72 rollback.


### v100 first live series reviewed — 2026-08-14

- Attributable platform v99 match `18052b89-514b-405a-ab32-be8a9420e76b`
  scored 2-3 against version 18 (Dino); no reliability error was reported.
- Replays and diagnostics are preserved in
  `reports/live-v99-first-series-replays/` and
  `reports/live-v99-first-series-replay-analysis.json`.  The three losses had
  first delivery at turns 18, none, and 19; wins delivered at turns 28 and
  53.  This confirms the remaining narrow-map route risk but is only one
  five-game series, below the 12-series rollback threshold.
- `python scripts/live_operator.py observe` captured
  `reports/live-observe-20260814T043544Z`; state remains `active_observing`,
  with v72 retained as rollback and no live promotion claim.


### v102 pending-chain retry rejected — 2026-08-14

- Hypothesis: retain an owed conveyor tile and navigate back after a danger
  flee instead of dropping the pending link.  The vase/skerry slice was
  10-10 (`reports/local-20260814T043649Z`), improving connectivity locally.
- Remote gate `89d60236-b0d6-4852-b047-92fe7cde66c8` scored 2-3 against v98;
  server replays and diagnostics are preserved under
  `reports/remote-v102-chain-pending-retry-replays/`.  The retry changed the
  combat/economy balance on sprint, crossfire, and vault and did not transfer.
- No full matrix, package, or deployment.  The candidate was restored exactly
  to v100; platform v99 remains active observing.
### v101 enemy-Core barrier cage activated — 2026-08-15

- Fresh top-team replay analysis found offensive Barrier cages in both Jython
  and O(1); the first home-Launcher experiment was rejected 1-3 and reverted.
- The resource-backed cage beat exact platform-v100 source 31-23 on the
  strengthened 54-game screen and 124-86 on the current 210-game matrix.
- Reliability: zero TLEs/suspicious output across 210 replays, max p99 1.477
  ms, peak 6.439 ms. Corrected current-map remote gate won 4-1 (match
  `84cb4c94-7a02-4631-a6c7-c4f2b21e6905`).
- Package: `artifacts/submissions/v0035_enemy-core-cage_20260815-2116_eeafad8f.zip`,
  SHA-256 `2c20aa8860d4c9528f613067ad650d20c0ed4156d3202453f51bbcb6ab9d76c7`.
- Guarded operator uploaded and activated platform v101 as
  `v0035-enemy-core-cage-eeafad8f`; v100 remains the previous active rollback
  candidate. Remaining strategic risk: auroraveil was 4-10 locally.


### Core-ring sink handoff rejected — 2026-08-16

- Hypothesis: let a pending conveyor finish into a visible friendly, non-Splitter
  conveyor whose output is visibly the Core, using strict back-side geometry.
  Scope was limited to `_best_feed_direction` in
  `bots/candidate/bot/defender.py` plus one focused test module.
- Focused checks passed (9 tests plus 5 subtests), compile passed, and smoke was
  4/4 command-clean (`reports/iter-core-ring-sink-v113`). Static remained the
  inherited exit-2 result from obsolete imports and stale contract assertions.
- The 24-game paired screen against immutable v0036 was command-clean but tied
  the prior candidate at 11-13; candidate delivery averaged 72.7 versus 73.8
  for the comparator, with no reliability errors (`reports/local-20260816T211040Z`;
  replay diagnostics in `reports/iter-core-ring-sink-v113/replay-analysis.json`).
- Decision: reject at the short screen and revert the helper and focused test.
  Rollback compile/focused/smoke passed; rollback smoke is
  `reports/local-20260816T211538Z`. No long gate, package, upload, or activation.


### Core-ring side-entry rejected after release gate — 2026-08-16

- Separate hypothesis: admit legal side-entry into a visible friendly ordinary
  Conveyor whose output visibly reaches the Core, while rejecting the output
  side. Luna implementation was attempted but stopped after it failed to finish
  within the bounded handoff; root completed and reviewed the same isolated
  patch in `bots/candidate/bot/defender.py` with a focused test module.
- Pre-screen checks passed for the candidate (9 focused tests plus 2 subtests,
  compile, and 4/4 smoke); `make static` retained the inherited exit-2 result
  from obsolete imports/stale assertions.
- The 24-game screen won 19-5, and the 54-game screen won 30-24, both
  command-clean. The release matrix was also command-clean but only 107-103;
  candidate replay diagnostics showed 7 no-delivery games versus 3 for v0036,
  delivery mean 66.7 versus 43.7, max p99 1.505 ms, and no TLE/suspicious
  output (`reports/local-20260816T213154Z` and
  `reports/iter-core-ring-side-entry-v114/matrix210-replay-analysis.json`).
- One bounded repair rejected occupied pending tiles before sink admission.
  Its 24-game screen fell to 12-12 (delivery mean 77.2 versus 88.7), so the
  entire side-entry iteration was reverted. Rollback compile/focused/smoke
  passed (`reports/iter-core-ring-side-entry-v114/rollback`; smoke report
  `reports/local-20260816T215859Z`). No package, upload, activation, or live
  baseline change.


### Bounded Launcher relay rejected — 2026-08-16

- Hypothesis: add one reserve-gated Launcher near home and dispatch only a
  designated attacker to a visible passable tile beside the confirmed enemy
  Core. This introduced a Launcher dispatch branch and an idle-turn build hook;
  economy, route, Store schema, and sentinel policy were otherwise unchanged.
- Focused checks passed (8 tests), compile passed, smoke was 4/4 command-clean,
  and static retained the inherited exit-2 obsolete-import/stale-contract
  failures (`reports/iter-bounded-launcher-relay-v115`).
- The 24-game screen was 16-8 with zero no-delivery games and 0.8 Launchers per
  candidate replay, but the 54-game gate fell to 22-32. Candidate delivery
  averaged 73.2 versus 29.6 for v0036, with 2 versus 0 no-delivery games;
  reliability was clean (max p99 1.342 ms, zero TLE/suspicious output) in
  `reports/local-20260816T221302Z` and
  `reports/iter-bounded-launcher-relay-v115/screen54-replay-analysis.json`.
- Decision: reject at the 54-game gate and revert all Launcher code/test files.
  Rollback compile/focused/smoke passed (`reports/iter-bounded-launcher-relay-v115/rollback`;
  smoke `reports/local-20260816T221853Z`). No 210 matrix, package, upload,
  activation, or live baseline change.


### Offensive Core-side Launcher ejection rejected — 2026-08-17

- Hypothesis: after a delivered route and a forward Sentinel, let a permanent
  attacker build at most two Launchers beside a confirmed enemy Core; each
  Launcher ejects the nearest visible enemy Builder to a legal tile farther
  from that Core. No home relay, route policy, Store schema, or Sentinel policy
  change was included.
- Focused tests passed 13/13, candidate compile passed, and `make smoke` was
  4/4 command-clean. `make static` retained the inherited exit-2 result from
  obsolete imports and stale contract assertions. Evidence is under
  `reports/iter-offensive-launcher-ejection-v116/`.
- The 24-game paired screen was command-clean but candidate won only 10-14
  (41.7%) against immutable v0036. Candidate first-delivery mean was 46.8
  turns versus 34.6 for the comparator, with 0 versus 1 no-delivery games;
  five Launchers were placed across three rows. Reliability was clean (zero
  TLE/suspicious output, maximum p99 1.354 ms, peak 2.510 ms). Replays and
  diagnostics are preserved in `reports/local-20260816T223419Z` and
  `reports/iter-offensive-launcher-ejection-v116/replay-analysis-24.json`.
- Decision: reject at the short screen and revert the Launcher implementation
  and focused tests. The three evaluation configs were corrected to compare
  against the immutable v0036 archive; rollback source now matches that
  archive byte-for-byte. No 54/210 gate, package, upload, activation, or live
  baseline change was performed.


### Four-route scalable-offense gate rejected — 2026-08-17

- Hypothesis: require four completed harvester paths, rather than three, before
  dynamic builders may raid/advance, the Core may designate its second
  permanent attacker, or the siege ammo buffer may engage. The change was
  isolated to `OFFENSE_MIN_HARVESTERS` in `bots/candidate/bot/constants.py`;
  existing fixed-attacker behavior and route construction were unchanged.
- Focused checks passed 21/21 and compile passed. `make smoke` was 4/4
  command-clean. `make static` still had the inherited obsolete-module errors
  plus two unrelated navigation fast-path assertion failures. Reports are in
  `reports/iter-four-route-offense-gate-v117/`.
- The 24-game screen improved to 13-11 against v0036, with candidate delivery
  mean 37.6 versus 37.4 turns and one versus zero no-delivery rows. The
  required 54-game checkpoint regressed to 23-31. Candidate delivery mean was
  29.2 versus 39.3 for the comparator; reliability was clean (zero TLE or
  suspicious output, max p99 1.395 ms, peak 5.724 ms). Replay diagnostics are
  `reports/iter-four-route-offense-gate-v117/replay-analysis-24.json` and
  `reports/iter-four-route-offense-gate-v117/replay-analysis-54.json`.
- Decision: reject at the 54-game checkpoint and restore v0036 exactly. Rollback
  focused/compile/smoke checks passed under
  `reports/iter-four-route-offense-gate-v117/rollback/`. No 210-game gate,
  package, upload, activation, or live baseline change was performed.


### Dynamic-only four-route economy floor rejected — 2026-08-17

- Hypothesis: preserve v0036's three-route gate for the fixed attacker, second
  attacker, and siege ammo, while keeping only scalable Dynamic builders in
  `TASK_HARVEST` until route four. Higher-priority home threat, belt repair,
  hijack, and base repair remained unchanged.
- Candidate scope was `bots/candidate/bot/constants.py` and
  `bots/candidate/bot/dynamic.py` with focused assertions in
  `tests/test_candidate_nearest_defense.py`. Focused checks passed 21/21,
  compile passed, and smoke was 4/4 command-clean. Static retained the
  inherited obsolete-import errors and two navigation fast-path assertions.
- The 24-game screen was 13-11 against v0036 (candidate delivery mean 25.6
  versus 31.1 turns, two versus one no-delivery rows), but the 54-game
  checkpoint fell to 21-33. Glacierkeep was 0-6 and Auroraveil 1-5; candidate
  delivery mean was 31.1 versus 30.9, with two no-delivery rows per side.
  Reliability stayed clean: zero TLE/suspicious output, max p99 1.409 ms,
  peak 5.022 ms. Reports: `reports/iter-dynamic-four-route-floor-v118/`,
  `reports/local-20260816T225849Z`, and `reports/local-20260816T230158Z`.
- Decision: reject at the 54-game checkpoint and restore v0036 source and
  focused tests byte-for-byte. Rollback checks are under
  `reports/iter-dynamic-four-route-floor-v118/rollback/`. No 210-game gate,
  package, upload, activation, or live baseline change was performed.


### Map-context dynamic economy floor rejected — 2026-08-17

- Hypothesis: apply a four-route economy floor only to Dynamic workers on
  cramped maps, while retaining v0036's three-route pressure floor on long
  maps. Fixed attacker, second-attacker, siege, route construction, and Store
  behavior were unchanged.
- Focused checks passed 22/22, candidate compile passed, and smoke was 4/4
  command-clean. Static retained the repository's inherited exit-2 result
  (obsolete imports plus two navigation fast-path assertions). The candidate
  screen and rollback evidence are under
  `reports/iter-map-context-dynamic-floor-v119/`.
- The 24-game paired screen fell to 11-13 against immutable v0036 (45.8%).
  Candidate first delivery averaged 28.0 versus 33.5 turns for the comparator,
  with zero versus two no-delivery rows. Reliability was clean: zero
  TLE/suspicious output, maximum p99 1.369 ms, and peak 4.924 ms.
- Decision: reject at the short screen and restore candidate source/tests to
  v0036 behavior. Rollback focused/compile/smoke passed under
  `reports/iter-map-context-dynamic-floor-v119/rollback/`. No 54/210 matrix,
  package, upload, activation, or live baseline change was performed.


### Funded Harvester hijack gate rejected — 2026-08-17

- Hypothesis: stop Dynamic workers from selecting an impossible pre-Core
  Harvester hijack, and otherwise allow only one nearest claimant after the
  three-route floor with a dynamic Harvester-cost replacement reserve. Known-
  Core seeded routes and fixed attacker pressure were unchanged.
- Focused checks passed 25/25, compile passed, and smoke was 4/4
  command-clean. Static retained the inherited exit-2 result from 15 obsolete
  imports and two navigation fast-path assertions. Evidence is under
  `reports/iter-funded-hijack-gate-v120/`.
- The 24-game paired screen fell to 10-14 (41.7%) against immutable v0036.
  Candidate first-delivery averaged 61.5 versus 34.4 turns for the comparator;
  both sides had zero command failures and no TLE/suspicious output, with
  maximum p99 1.294 ms and peak 6.459 ms.
- Decision: reject at the short screen and restore candidate source/tests to
  v0036 behavior. Rollback focused/compile/smoke passed under
  `reports/iter-funded-hijack-gate-v120/rollback/`. No 54/210 matrix,
  package, upload, activation, or live baseline change was performed.


### Pre-Core hijack idle guard rejected — 2026-08-17

- Hypothesis: prevent Dynamic workers from selecting a seeded Harvester hijack
  until the shared home-Core position is known, because the executor cannot
  choose a legal conveyor facing before that point. No economy, reserve,
  attacker, or route policy changed.
- Focused checks passed 23/23, compile passed, and smoke was 4/4
  command-clean. Static retained the inherited exit-2 obsolete-import and
  navigation assertion failures. Evidence is under
  `reports/iter-precore-hijack-idle-guard-v121/`.
- The 24-game paired screen fell to 9-15 (37.5%) against immutable v0036.
  Candidate first-delivery averaged 29.0 versus 39.6 turns for the comparator;
  reliability was clean (zero TLE/suspicious output, max p99 1.156 ms, peak
  4.912 ms).
- Decision: reject at the short screen and restore candidate source/tests to
  v0036 behavior. Rollback focused/compile/smoke passed under
  `reports/iter-precore-hijack-idle-guard-v121/rollback/`. No 54/210 matrix,
  package, upload, activation, or live baseline change was performed.


### Wealth-backed unknown-Core Harvester raid rejected — 2026-08-17

- Hypothesis: after one completed route, let the nearest Dynamic builder raid a
  visible enemy Harvester before enemy-Core confirmation, but only while the
  balance can replace a Harvester and preserve the fixed attack reserve. Known-
  Core loaded-belt raids and all fixed attacker, route, Store, and Sentinel
  policies were unchanged.
- Scope was limited to `_find_raid_target` in
  `bots/candidate/bot/dynamic.py` and focused assertions in
  `tests/test_candidate_nearest_defense.py`. Focused checks passed 27/27,
  compile passed, and smoke was 4/4 command-clean. `make static` retained the
  inherited exit-2 obsolete-import and navigation fast-path failures. Reports
  are under `reports/iter-wealth-backed-harvester-raid-v123/`.
- The 24-game screen was 18-6 against immutable v0036 (candidate delivery mean
  27.2 versus 29.0 turns, one versus zero no-delivery rows), but the required
  54-game checkpoint tied 27-27. Candidate delivery averaged 32.1 versus 38.5
  turns and collection was 228560 versus 225090; Auroraveil fell 1-5. All 54
  games were command-clean with zero TLE/suspicious output, maximum p99 1.455
  ms, and peak 5.731 ms.
- Decision: reject at the 54-game gate and restore candidate source/tests to
  v0036 byte-for-byte. Rollback focused/compile/smoke passed under the same
  report directory (`rollback-smoke` report `reports/local-20260817T001126Z`).
  No 210-game gate, package, upload, activation, or live baseline change was
  performed.


### Turret-retirement workforce reuse rejected — 2026-08-17

- Hypothesis: after a non-cramped defense has been quiet for 80 rounds beyond
  round 400, five completed routes, a rich bank, and at least three intact
  home Gunners, authorize one nearest non-attacker Builder to legally destroy
  the outermost Gunner and spend the freed cap on one late Builder. The
  marker was one-shot and deterministic; normal route, Sentinel, Launcher,
  cage, and Store behavior otherwise remained on v0036.
- Scope was limited to the candidate lifecycle/task modules and focused
  nearest-defense tests. The first focused suite passed 25/25, compile passed,
  and smoke was 4/4 command-clean. Review found a Core/Builder equal-distance
  Gunner tie mismatch; repair 1 aligned the lower entity-id tie-break and
  passed 26/26 focused tests. Repair 2 cancelled an outstanding marker when
  danger appeared and made the Builder abort a destroy under danger; the final
  focused suite passed 27/27 and compile passed. Reports are under
  `reports/iter-turret-retirement-v124/`.
- The initial 24-game screen was 10-14; repair 1 was 9-15; repair 2 remained
  9-15 against immutable v0036. The final candidate delivery mean was 30.1
  versus 28.8 turns for the comparator, with zero no-delivery games on both
  sides. Reliability was clean (zero TLE/suspicious output, maximum p99
  1.407 ms, peak 2.359 ms). Replay analysis is
  `reports/iter-turret-retirement-v124/replay-analysis-24-final.json`; the
  initial and repair-1 diagnostics are preserved alongside it.
- `make static` retained the inherited exit-2 result from 15 obsolete imports,
  stale assertions, and two navigation fast-path failures. Final smoke was
  4/4 command-clean. No 54/210 gate, package, upload, activation, or live
  operation was performed.
- Decision: reject after two bounded repair attempts. The retirement changes
  were removed with `apply_patch`; candidate source files now compare
  byte-for-byte with immutable v0036. Rollback focused/compile/smoke passed;
  rollback smoke is `reports/local-20260817T004101Z`. Baseline and live state
  remain unchanged.


### Defensive Launcher exile rejected — 2026-08-17

- Hypothesis: after one completed route and a protected Harvester reserve, the
  nearest Dynamic home responder may build at most one visible defensive
  Launcher beside a confirmed enemy Builder, then the Launcher exiles that
  intruder to a legal far/passable tile. No offensive Launcher policy or route,
  Sentinel, Gunner, or Store policy changed.
- Scope was limited to `bots/candidate/main.py`,
  `bots/candidate/bot/constants.py`, `bots/candidate/bot/dynamic.py`, and a
  focused Launcher test file. Focused checks passed 26/26, compile passed, and
  smoke was 4/4 command-clean. `make static` retained the inherited exit-2
  obsolete-module imports plus two navigation fast-path assertions. Reports
  are under `reports/iter-defensive-launcher-v125/`.
- The 24-game paired screen against immutable v0036 was 9-15 (37.5%). The
  candidate placed five Launchers; they appeared in both wins and losses, so
  the response showed no reliable gain. Candidate first delivery averaged
  21.7 versus 20.8 turns for the comparator, with zero no-delivery rows on
  both sides. Reliability was clean: zero TLE/suspicious output, maximum p99
  1.377 ms, peak 4.891 ms. Replay report: `reports/local-20260817T081054Z`.
- Decision: reject at the short screen. The Launcher code and focused test
  file were removed with `apply_patch`; all candidate source modules compare
  byte-for-byte with immutable v0036, and rollback focused tests passed 21/21.
  No 54/210 gate, package, upload, activation, or live baseline change was
  performed. Continue with the next bounded strategy iteration.


### Fixed-attacker sabotage pulse promoted locally — 2026-08-17

- Hypothesis: once three routes, a confirmed enemy Core, one live forward
  Sentinel, and the fixed combat reserve are present, let the nearer designated
  attacker claim one visible enemy Harvester/conveyor/splitter, destroy it,
  and resume the direct siege lane. This activates the previously disabled
  `_try_sabotage_with_attacker` hook; no Launcher, route, economy threshold, or
  dynamic-worker policy changed.
- Scope was limited to `bots/candidate/bot/attacker.py` and focused ownership/
  gate assertions in `tests/test_candidate_nearest_defense.py`. Focused checks
  passed 23/23, compile passed, smoke was 4/4 command-clean, and static kept
  the inherited exit-2 obsolete-module/navigation failures. Reports are under
  `reports/iter-attacker-sabotage-pulse-v126/`.
- The 24-game screen was 13-11 against immutable v0036 (73,670 versus 64,560
  collected titanium; candidate first delivery 22.7 versus 29.0 turns; zero
  versus one no-delivery). The 54-game checkpoint was 30-24 (237,770 versus
  173,000 collected; zero versus two no-delivery). Reliability was clean in
  both screens (zero TLE/suspicious output; max p99 1.468 ms on the short and
  1.390 ms on the 54-game run).
- Release matrix: 116-94 across 210 games (55.2%), 1,105,440 versus 968,650
  collected titanium (1.1412x), five versus eight no-delivery rows, zero
  command failures/TLE/suspicious output, max p99 1.536 ms and peak 4.944 ms.
  Map floors were uneven (Auroraveil 6/14, Royale 5/14, Yulerune 5/14), so
  those remain the next iteration's risk targets.
- Decision: archive and promote locally as immutable
  `bots/versions/v0037_attacker-sabotage-pulse_20260817-0851_eeafad8f`; update
  all evaluation configs and `state/project_state.json` to that baseline.
  Archive SHA-256 is
  `d27132e1ae514fa90a5d0ce844204a4914ac2d62680a2248953e52e6979a94c4`.
  No upload or activation was performed; platform state remains unchanged.


### Late economy steward rejected — 2026-08-17

- Hypothesis: after the three-route opening gate, lease one visible non-floor
  dynamic Builder back to the harvest/explore loop so route/Harvester attrition
  cannot leave the team permanently in raid/advance mode. The first candidate
  used round 180; the bounded repair delayed the lease to round 300.
- Scope was limited to `bots/candidate/bot/constants.py`,
  `bots/candidate/bot/dynamic.py`, and focused assertions in
  `tests/test_candidate_nearest_defense.py`. Focused checks passed 26/26,
  compile passed, smoke was 4/4 command-clean, and `make static` retained the
  inherited exit-2 obsolete-import/navigation failures.
- The initial 24-game screen tied 12-12 and collected 76,660 versus 81,170
  for immutable v0037. After the one bounded repair, the repeated screen was
  13-11 but collected 92,210 versus 98,710. Both screens were reliability
  clean (zero command failures/TLE/suspicious output; max p99 1.427 ms and
  1.381 ms respectively). Reports are under
  `reports/iter-economy-steward-v127/` and local runs are
  `reports/local-20260817T090215Z`, `reports/local-20260817T090237Z`,
  `reports/local-20260817T090659Z`, and `reports/local-20260817T090731Z`.
- Decision: reject after the bounded repair. The steward changes were removed;
  candidate source compares byte-for-byte with immutable v0037. Rollback
  focused/compile/smoke passed (23/23, compile clean, 4/4;
  `reports/local-20260817T091120Z`). No 54/210 gate, package, upload,
  activation, or live baseline change was performed. Continue with a bounded
  route-continuity/conversion hypothesis.


### Pre-route Core-ring maintenance rejected — 2026-08-17

- Hypothesis: defer long-distance Dynamic ring-repair tasks until one
  Harvester chain has completed, so the opening workforce spends its movement
  and action budget on the first route. The adjacent idle fallback remained
  available in repair 1.
- Scope was limited to `bots/candidate/main.py`,
  `bots/candidate/bot/defender.py`, `bots/candidate/bot/dynamic.py`, and one
  focused assertion. Focused checks passed 24/24, compile passed, smoke was
  4/4 command-clean, and `make static` retained the inherited exit-2
  obsolete-import/navigation failures.
- Initial 24-game screen: 13-11 and 94,670-87,670 collected titanium. The
  54-game checkpoint regressed 24-30 (168,460-165,630 collection) with first
  delivery 52.5 versus 37.6 turns. Repair 1 restored adjacent ring fallback;
  its 24-game screen was 14-10 but its 54-game checkpoint fell to 20-34 with
  137,780-186,410 collection and first delivery 63.7 versus 36.5 turns. All
  runs were reliability-clean (zero command failures/TLE/suspicious output;
  max p99 below 1.5 ms). Reports are under
  `reports/iter-route-opening-v128/`; release reports are
  `reports/local-20260817T091630Z`, `reports/local-20260817T091914Z`,
  `reports/local-20260817T092517Z`, and `reports/local-20260817T092757Z`.
- Decision: reject after the bounded repair. Candidate source and tests were
  restored byte-for-byte to immutable v0037; rollback focused/compile/smoke
  passed (23/23, compile clean, 4/4; `reports/local-20260817T093403Z`). No
  package, 210-game gate, upload, activation, or live baseline change was
  performed. Continue with a bounded pre-delivery conversion hypothesis.


### Pre-delivery conversion reserve rejected — 2026-08-17

- Hypothesis: preserve the first route's capital by reserving one Harvester
  and four conveyor costs before any completed route; the bounded repair also
  withheld discretionary Core ammo floor/buffer conversion until a route or a
  live threat was visible.
- Scope was limited to `bots/candidate/bot/core_role.py`, focused Core tests,
  and `reports/iter-opening-conversion-v129/`. Focused checks passed 25/25
  initially and 26/26 after repair; rollback passed 23/23. Compileall passed;
  `make static` retained the inherited exit-2 obsolete-import/navigation
  failures; smoke was 4/4 for both candidates and rollback.
- Initial 24-game screen: 13-11, 73,400-53,670 collected titanium, zero versus
  two no-delivery rows, and first delivery 25.8 versus 19.2 turns. The initial
  54-game checkpoint was 30-24 and 181,240-174,660 collection, with two versus
  four no-delivery rows and first delivery 33.7 versus 28.5 turns. Repair 1
  tied the 24-game screen 12-12 (110,010-100,920 collection; zero versus one
  no-delivery row; first delivery 23.8 versus 24.0), so no repair 54-game gate
  was run. All runs were reliability-clean (zero command failures/TLE/
  suspicious output; max p99 below 1.6 ms). Reports and replay analyses are
  under `reports/iter-opening-conversion-v129/`.
- Decision: reject after the bounded repair and restore candidate source
  byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed;
  the rollback smoke report is `reports/local-20260817T095344Z`. No 210-game
  gate, package, upload, activation, or live baseline change was performed.
  Continue with a different replay-backed conversion/defense hypothesis.


### Ammo consumer contract rejected — 2026-08-17

- Hypothesis: v0037 losses commonly ended without a live forward Sentinel but
  with more ammo than wins, so Core conversion should require a known friendly
  Gunner/Sentinel consumer. Repair 1 retained that floor guard while restoring
  the established threat/prestock buffer and allowing the floor during a
  visible threat.
- Scope was limited to `bots/candidate/bot/core_role.py`, focused Core tests,
  and the `reports/iter-ammo-consumer-v130-*` logs. Focused checks passed 26/26 for both
  variants and 23/23 after rollback; compileall passed; `make static` retained
  the inherited exit-2 obsolete-import/navigation failures; smoke was 4/4 for
  both variants and rollback.
- Initial 24-game screen: 9-15, 84,400-89,660 collected titanium, one versus
  zero no-delivery rows, first delivery 35.8 versus 26.1 turns, zero command
  failures/TLE/suspicious output, maximum p99 1,584 us. Repair 1 improved the
  same 24-game slice to 15-9 (94,110-88,790 collection, zero versus one
  no-delivery row, first delivery 25.6 versus 41.0 turns, zero reliability
  failures; maximum p99 1,415 us), so it advanced to the 54-game checkpoint.
- Repair 1 54-game checkpoint: 25-29, 151,620-167,020 collection, zero versus
  two no-delivery rows, first delivery 41.6 versus 42.8 turns, zero
  command/TLE/suspicious-output failures, and maximum p99 1,362 us. Map floors
  were archipelago 2/6 and nordkap 1/6, so the short edge was rejected. Replay
  analyses and runner logs use the `reports/iter-ammo-consumer-v130-*` paths; local
  reports are `reports/local-20260817T100103Z`,
  `reports/local-20260817T100517Z`, and
  `reports/local-20260817T100759Z`.
- Decision: reject after two bounded attempts and restore candidate source
  byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed;
  rollback smoke is `reports/local-20260817T101344Z`. No 210-game gate,
  package, upload, activation, or live baseline change was performed.
  Continue with a different replay-backed structural hypothesis.


### Second-attacker economy rejoin rejected — 2026-08-17

- Hypothesis: when three routes were already complete but the second fixed
  attacker still had no confirmed Core/Sentinel progress, reassign it to the
  existing Defender economy/repair loop after round 120. The first attacker
  stayed on the direct lane; the repair disabled this handoff on cramped maps.
- Scope was limited to `bots/candidate/bot/attacker.py`,
  `bots/candidate/bot/constants.py`, focused attacker tests, and the
  `reports/iter-attacker-economy-rejoin-v131-*` logs. Focused checks passed
  24/24 for both variants and 23/23 after rollback; compileall passed;
  `make static` retained inherited obsolete-import/navigation failures; smoke
  was 4/4 for both variants and rollback.
- Initial 24-game screen: 9-15, 68,960-91,640 collection, zero no-delivery
  rows, first delivery 26.3 versus 24.8 turns, zero reliability failures,
  maximum p99 1,480 us. Repair 1 scored 8-16 (84,010-117,540 collection,
  zero no-delivery rows, first delivery 27.5 versus 23.3 turns, zero
  reliability failures, maximum p99 1,441 us); map floors included fjordgate
  0/4 and ragnarok 1/4. Replay analyses are
  `reports/iter-attacker-economy-rejoin-v131-replay-analysis-24.json` and its
  `-repair1` counterpart; local reports are
  `reports/local-20260817T102213Z` and `reports/local-20260817T102616Z`.
- Decision: reject after two bounded attempts and restore candidate source
  byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed;
  rollback smoke is `reports/local-20260817T102958Z`. No 54/210 gate, package,
  upload, activation, or live baseline change was performed. Continue with a
  different replay-backed structural hypothesis.


### Confirmed enemy-Core intel for flexible builders rejected — 2026-08-17

- Hypothesis: dynamic and Defender builders should consume the fixed-attacker's
  confirmed enemy-Core position through the delayed Store, instead of using a
  symmetry guess for advance/raid/denial. The initial variant also published a
  directly visible Core from the generic helper; repair 1 removed that generic
  publication after the first screen showed an economy collapse.
- Scope was limited to `bots/candidate/bot/attacker.py`, two focused intel
  assertions in `tests/test_candidate_nearest_defense.py`, and
  `reports/iter-enemy-core-intel-v132/`. Initial and repair focused checks were
  21/21, compileall passed, `make smoke` was 4/4 for both, and `make static`
  retained the inherited 15 obsolete-module import errors plus two navigation
  fast-path assertions.
- Initial 24-game screen: 8-16, 68,100-90,410 collected titanium, zero command
  failures, and pronounced Glacierkeep/Archipelago economy collapse; report
  `reports/local-20260817T103832Z`. Repair 1 recovered the same slice to 14-10
  and 85,250-72,670 collection with zero no-delivery/reliability failures;
  report `reports/local-20260817T104300Z`.
- Repair 1 54-game checkpoint regressed to 23-31, 153,670-181,620 collection,
  three versus comparator no-delivery rows, zero command failures/TLE/
  suspicious output, max p99 1,466 us, and peak callback 5,234 us. Report
  `reports/local-20260817T104525Z`; replay analysis is
  `reports/iter-enemy-core-intel-v132/replay-analysis-54-repair1.json`.
- Decision: reject after two bounded attempts and restore candidate source
  byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed
  (19/19, compile clean, 4/4; rollback smoke
  `reports/local-20260817T105120Z`). No 210-game gate, package, upload,
  activation, or live baseline change was performed. Continue with a different
  replay-backed structural hypothesis.


### Failed-route reconnect rejected — 2026-08-17

- Tested a source-local retry for a Builder that abandoned a substantial own
  Harvester chain: initial 54-game screen **29-25** with 204,470-204,200 Ti and
  two versus four no-delivery rows, but the release-sized 210-game gate
  regressed to **100-110** with 924,790-941,070 Ti. Reliability stayed clean;
  both runs had zero command failures/TLE/suspicious output and maxima of 1,470
  us p99 / 5,424 us peak. Evidence is in
  `reports/local-20260817T110346Z` and `reports/local-20260817T110945Z`.
- Repair 1 limited the retry to the opening before any completed route. Its
  focused suite was 26/26, compileall passed, smoke was 4/4, but the 54-game
  screen fell to **26-28**, 207,910-217,000 Ti, and two versus one no-delivery
  rows (`reports/local-20260817T113144Z`). Static retained the inherited
  obsolete-import/navigation failures.
- Rejected after two bounded variants. Candidate source is restored exactly to
  immutable v0037; rollback focused tests were 23/23, compileall passed, and
  rollback smoke was 4/4 (`reports/local-20260817T113900Z`). No new baseline,
  package, upload, activation, or live-state change was made. Experiment:
  `experiments/v0037-failed-route-reconnect-v133.md`.


### Adjacent-only orphan Harvester seed promoted locally — 2026-08-17

- Hypothesis: before the first completed route, let only the nearest visible
  non-attacker Builder seed one legal Conveyor beside a completely disconnected
  own Harvester. The responder never crosses the map; it must already be next
  to the seed tile, and a nearby chain owner suppresses duplicate claims.
  Scope was limited to `bots/candidate/bot/defender.py`,
  `tests/test_candidate_nearest_defense.py`, one experiment record, and
  checkpoint metadata. No Store, navigation, combat, Launcher/Sentinel, map
  branch, baseline source, upload, or activation change was included.
- Initial 54-game screen regressed to **25-29** with one candidate
  no-delivery row (`reports/local-20260817T114906Z`). The bounded adjacent-only
  repair improved the screen to **34-20**, 222,150 versus 216,300 Ti, one
  candidate no-delivery row, zero command failures/TLE/suspicious output, and
  max p99/peak 1,487/5,692 us (`reports/local-20260817T115537Z`).
- Full 21-map, seven-seed, side-swapped gate finished **125-85 (59.52%)**
  versus immutable v0037, 956,730 versus 875,000 Ti (1.0934x), three candidate
  no-delivery rows versus none, 210/210 command-clean, zero TLE/suspicious
  output, max p99 1,487 us, and peak callback 5,692 us
  (`reports/local-20260817T120039Z`). Ragnarok remains the main floor risk at
  4-10; Auroraveil, Glacierkeep, and Midgard are each 7-7.
- Final focused tests passed **25/25**, compileall passed, smoke was **4/4**
  (`reports/local-20260817T122257Z`), and static retained the inherited 15
  obsolete imports plus two navigation fast-path assertions. The complete
  source diff is `reports/iter-orphan-local-seed-v134-final-source.diff`.
- Decision: accept the paired win-rate gain and archive the candidate as moving
  local baseline `bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f`.
  Package SHA-256 is
  `90a339d9ad846aa6e74631246bf0affdddc551cffcb5cc2fdc08f9acef17c6b0`.
  The live platform remains unchanged at active version 102; no upload or
  activation was performed. Next iteration should diagnose the Ragnarok loss
  cluster without weakening the adjacent-only opening guard.


### Confirmed-Core pressure handoff rejected — 2026-08-17

- Hypothesis: after three completed routes and a confirmed enemy Core, stop
  dynamic Builders from harvesting every visible ore tile once the bank can
  fund a Sentinel/raid reserve; keep the permanent Defender on economy duty so
  the pool converts resources into pressure. Repair 1 retained one full next-
  Harvester cost in that reserve. Scope was limited to
  `bots/candidate/bot/dynamic.py`, two focused tests, and checkpoint metadata.
- Initial 54-game screen: **29-25**, candidate 212,640 versus comparator
  221,450 Ti (0.9602x), two candidate no-delivery rows, zero command/TLE/
  suspicious-output failures, max p99 1,420 us, peak 4,734 us. Ragnarok
  improved to 4-2, but the edge was not clear enough for a 210-game gate.
  Report: `reports/local-20260817T123159Z`.
- Repair 1 focused/compile/smoke passed (27/27, compile clean, 4/4); static
  retained the inherited failures. The screen regressed to **25-29**, with
  zero candidate no-delivery rows, 154,510 candidate Ti, Auroraveil **0-6**,
  and Ragnarok **6-0** (`reports/local-20260817T123913Z`).
- Decision: reject after two bounded variants and restore candidate production
  files byte-for-byte to v0038. Rollback focused tests passed 25/25, compileall
  passed, and smoke was 4/4 (`reports/local-20260817T124500Z`). No 210-game
  gate, package, upload, activation, or live-state transition occurred.
  Experiment: `experiments/v0038-confirmed-core-pressure-v135.md`.


### Loaded-raid task priority rejected — 2026-08-17

- Hypothesis: after the three-route economy gate, a dynamic Builder should
  claim a concrete visible enemy logistics raid before returning to harvest;
  the bounded repair allowed that preemption only for a loaded conveyor or
  splitter. The existing nearest-responder and forward-shell gates remained
  unchanged.
- Scope was limited to `bots/candidate/bot/dynamic.py`, one focused task-order
  test, and checkpoint metadata. Initial and repair focused checks passed
  17/17, rollback focused checks passed 16/16, compileall passed for both
  variants and rollback, and smoke was 4/4 command-clean for each. `make
  static` retained the inherited exit-2 result: 15 obsolete imports plus two
  navigation fast-path assertions.
- Initial 54-game screen: **29-25**, 194,620 versus 175,570 collected Ti
  (1.1085x), zero command/TLE/suspicious-output failures. Map results were
  fjordgate 3-3, antler 5-1, icefloe 3-3, archipelago 1-5, nordkap 2-4,
  drakkarfjord 4-2, glacierkeep 4-2, auroraveil 3-3, and ragnarok 4-2;
  report `reports/local-20260817T125258Z`.
- Repair 1 regressed to **23-31**, 203,530 versus 239,790 Ti (0.8488x),
  including nordkap 1-5, drakkarfjord 1-5, and auroraveil 2-4; report
  `reports/local-20260817T125839Z`. No 210-game gate was warranted.
- Decision: reject after the initial screen and one bounded repair. Candidate
  production Python is byte-identical to v0038 after rollback; rollback
  evidence is `reports/iter-v136-loaded-raid-priority-rollback-focused.log`.
  No package, upload, activation, or live-state change occurred. Experiment:
  `experiments/v0038-loaded-raid-priority-v136.md`.


### Economy workforce floor rejected — 2026-08-17

- Hypothesis: keep newly spawned non-attacker Builders in the Defender economy
  loop until three completed routes, because weak Ragnarok openings often had
  only two-to-five Harvesters. Repair 1 released the floor early when the bank
  was already rich. Scope was limited to `bots/candidate/main.py`, the focused
  role test, and checkpoint metadata.
- Initial focused checks passed 17/17, compileall passed, smoke was 4/4, and
  static retained the inherited exit-2 obsolete-import/navigation failures.
  The 54-game screen was **31-23**, 240,960 versus 181,520 Ti (1.3275x), zero
  no-delivery rows, and zero command/TLE/suspicious-output failures; report
  `reports/local-20260817T131522Z`.
- The 210-game release-sized matrix was reliability-clean (210/210,
  zero TLE/suspicious output, max p99 1,484 us, peak 5,325 us) but only
  **107-103**, 865,280 versus 887,780 Ti (0.9747x). Midgard and Royale were
  each 3-11; Ragnarok improved to 9-5. Report `reports/local-20260817T132105Z`.
- Repair 1 focused/compile/smoke passed (17/17, clean, 4/4); the 54-game
  screen regressed to **25-29**, 159,270 versus 172,480 Ti (0.9234x), with
  Auroraveil 1-5 and Archipelago/Nordkap 2-4. Report:
  `reports/local-20260817T134339Z`.
- Decision: reject after the long-gate regression and one bounded repair.
  Rollback focused/compile/smoke passed (16/16, clean, 4/4; report
  `reports/local-20260817T134854Z`), static remained inherited red, and all
  candidate Python sources are byte-identical to v0038. No package, upload,
  activation, or live-state change occurred. Experiment:
  `experiments/v0038-economy-workforce-floor-v137.md`.


### Verified local Conveyor merge rejected — 2026-08-17

- Hypothesis: a chain segment could safely join an existing friendly Conveyor
  when a bounded, fully visible directed walk proved that the tail reached our
  Core. Splitters, unseen tails, gaps, and cycles were excluded. Scope was
  limited to `bots/candidate/bot/defender.py`,
  `tests/test_candidate_seeded_route.py`, and checkpoint metadata; no
  workforce, role, combat, navigation, Store, map, baseline, or platform
  change was included.
- Initial v138 focused checks passed **22/22**, compileall passed, smoke was
  **4/4**, and static retained the inherited exit-2 result. The 54-game screen
  regressed to **23-31**, with candidate/comparator collection
  **161,860/158,180 Ti**; Icefloe was **0-6** and Drakkarfjord **2-4**.
  Replay report: `reports/local-20260817T135748Z`.
- Repair 1 allowed joins only after one completed route. Focused checks remained
  **22/22**, compileall and smoke remained clean, and the screen recovered only
  to **27-27** with **185,510/178,720 Ti**; candidate no-delivery rows were
  **2** versus comparator **0**. Report: `reports/local-20260817T140404Z`.
- Both screens were command-clean with zero TLE/suspicious-output rows, but the
  repair was neutral and introduced a delivery reliability regression. Reject
  after two bounded attempts and restore candidate production sources and
  focused tests byte-for-byte to v0038. Rollback focused tests were **20/20**,
  compileall passed, smoke was **4/4**, and static remained inherited red;
  rollback report: `reports/local-20260817T140925Z`. No 210-game gate, package,
  upload, activation, or live baseline change was performed. Experiment:
  `experiments/v0038-verified-local-merge-v138.md`.


### Map-adaptive frontier exploration rejected — 2026-08-17

- Hypothesis: when no visible or advertised ore existed, a Builder should target
  a visible passable tile adjacent to an unseen cardinal neighbor, rather than
  an arbitrary unseen coordinate. Scope was limited to
  `bots/candidate/bot/defender.py`, `tests/test_candidate_seeded_route.py`, and
  checkpoint metadata; no role, economy gate, route, combat, navigation, Store,
  baseline, or platform change was included.
- Initial v139 focused checks passed **21/21**, compileall passed, smoke was
  **4/4**, and static retained the inherited exit-2 result. The 54-game screen
  was **25-29**, with candidate/comparator collection **209,390/195,880 Ti**
  and candidate no-delivery **2** versus comparator **0**. Nordkap improved to
  5-1, but Antler and Glacierkeep fell to 1-5. Report:
  `reports/local-20260817T141419Z`.
- Repair 1 kept the v0038 arbitrary opening picker until one completed route,
  then enabled frontier preference. Focused checks remained **21/21**,
  compileall and smoke stayed clean, but the screen fell to **21-33** with
  **151,350/197,980 Ti** and candidate no-delivery **2** versus 0; Archipelago
  was 0-6 and Nordkap 1-5. Report: `reports/local-20260817T142004Z`.
- Reject after two bounded attempts. Candidate production Python and focused
  tests are byte-identical to v0038; rollback focused tests were **21/21**,
  compileall passed, smoke was **4/4**, and static remained inherited red.
  Rollback report: `reports/local-20260817T142504Z`. No 210-game gate, package,
  upload, activation, or live baseline change was performed. Experiment:
  `experiments/v0038-frontier-exploration-v139.md`.


### Ore-claim handoff rejected — 2026-08-17

- Hypothesis: after three completed routes, a closer non-attacker Builder may
  already be committed to raid/repair/advance, so it should not suppress an
  eligible Builder's visible ore claim. Scope was limited to
  `bots/candidate/bot/defender.py`, `tests/test_candidate_seeded_route.py`, and
  checkpoint metadata; no role/task priority, workforce, route, exploration,
  combat, Store, baseline, or platform change was included.
- Initial post-milestone no-yield variant passed focused **21/21**, compileall,
  smoke **4/4**, and retained the inherited static exit 2. The 54-game screen
  was **27-27**, candidate/comparator collection **215,170/208,250 Ti**, with
  no-delivery **2/2**. Report: `reports/local-20260817T142848Z`.
- Repair 1 disabled yielding only at exactly the three-route transition. Checks
  remained **21/21**, compileall/smoke stayed clean, and the screen was **28-26**
  with **180,530/152,770 Ti**, but candidate no-delivery was **1** versus 0.
  Report: `reports/local-20260817T143431Z`.
- Reject after two bounded attempts: the two-game edge is not significant and
  the repair adds a delivery regression. Candidate production Python and tests
  are byte-identical to v0038; rollback focused tests were **21/21**, compileall
  passed, smoke was **4/4**, and static remained inherited red. Rollback report:
  `reports/local-20260817T143937Z`. No 210-game gate, package, upload,
  activation, or live baseline change was performed. Experiment:
  `experiments/v0038-ore-claim-handoff-v140.md`.


### Chain-pending recovery rejected — 2026-08-17

- Hypothesis: when danger-flee displacement made a pending conveyor tile no
  longer adjacent, retain the pending segment and navigate back under the
  current danger map instead of dropping the link. Scope was limited to
  `bots/candidate/bot/defender.py`, `tests/test_candidate_seeded_route.py`, and
  checkpoint metadata; no route merging, workforce/role/task, exploration,
  combat, Store, baseline, or platform change was included.
- Initial recovery passed focused **21/21**, compileall, smoke **4/4**, and
  retained inherited static exit 2. The 54-game screen was **26-28**, candidate/
  comparator collection **220,810/200,280 Ti**, no-delivery **1/1**. Report:
  `reports/local-20260817T144253Z`.
- Repair 1 limited recovery to pending tiles within squared distance 16. Checks
  remained **21/21**, compileall/smoke stayed clean, and the screen improved to
  **29-25** with **198,520/204,950 Ti**, no-delivery **0/0**, and Ragnarok 6-0;
  the four-game edge was not significant and collection regressed. Report:
  `reports/local-20260817T144837Z`.
- Reject after two bounded attempts. Candidate production Python and tests are
  byte-identical to v0038; rollback focused tests were **21/21**, compileall
  passed, smoke was **4/4**, and static remained inherited red. Rollback report:
  `reports/local-20260817T145408Z`. No 210-game gate, package, upload,
  activation, or live baseline change was performed. Experiment:
  `experiments/v0038-chain-pending-recovery-v141.md`.


### Chain-only non-progress detour rejected — 2026-08-17

- Hypothesis: a chain Builder may need a bounded safe detour when every visible
  tile is temporarily farther from Core than its current tile. v142 added an
  opt-in navigation mode with a four-round chain-local budget; repair 1 kept it
  only before the first completed route. Scope was limited to the navigation,
  defender, constants, and focused route/navigation tests; no economy, role,
  combat, Store, baseline, package, upload, activation, or live-state change.
- Initial checks passed focused **26/26**, compileall, and smoke **4/4**;
  `make static` retained the inherited exit-2 result. The 54-game screen was
  **30-24**, candidate/comparator **187,240/165,450 Ti**, no-delivery **1/3**,
  zero command/TLE/suspicious-output failures, and max p99/peak
  **1,441/4,841 us** (`reports/local-20260817T150550Z`).
- The required 210-game gate was reliability-clean but regressed to **99-111**,
  **913,170/922,400 Ti**, and candidate/comparator no-delivery **8/2**; max
  p99/peak was **1,500/5,426 us**. Report and analysis:
  `reports/local-20260817T151133Z` and
  `reports/iter-v142-chain-detour/full210-analysis.log`.
- Repair 1 checks again passed focused **26/26**, compileall, and smoke **4/4**;
  its 54-game screen regressed to **24-30**, **181,190/206,990 Ti**, and
  no-delivery **1/1**, with zero command/TLE/suspicious-output failures and
  max p99/peak **1,449/5,654 us** (`reports/local-20260817T153443Z`).
- Reject after the long-gate regression and one bounded repair. Candidate
  production Python and temporary tests were restored byte-for-byte to v0038;
  rollback focused tests were **25/25**, compileall passed, smoke **4/4**, and
  static remained inherited red (`reports/iter-v142-chain-detour/rollback-*`,
  `reports/local-20260817T154031Z`). No package, upload, activation, or
  baseline transition occurred. Experiment:
  `experiments/v0038-chain-detour-v142.md`.
### v199 short-lived Sentinel liquidity circuit rejected — 2026-08-18

- Added a failure-adaptive circuit that required two confirmed short-lived
  forward-Sentinel deaths before preserving a dynamic Harvester/two-link
  reserve; it did not alter the opening or healthy Sentinel pressure.
- Focused **25/25**, compileall pass, static retained inherited exit 2, and
  smoke **4/4** (`reports/local-20260818T124013Z`). The rotated 15-map seed-164
  screen was **6-9**, 15/15 command-clean, no TLE/suspicious/no-delivery rows,
  max p99/peak **1,559/4,175 us** (`reports/local-20260818T124056Z`, replay
  analysis `reports/iter-v199-sentinel-liquidity-replay-analysis.json`).
- Reject and roll back: candidate source is recursively identical to immutable
  v0042; rollback focused nearest-defense **23/23**, compileall pass, and
  rollback smoke **4/4** (`reports/local-20260818T124900Z`). No release gate,
  package, upload, activation, or live transition.
- Replay follow-up: top-team winners repeatedly built Launchers at rounds 1/3/5
  and offensive Barriers before later Sentinel pressure, while this baseline
  placed no Launchers. The next isolated hypothesis is a reserve-gated,
  primary-attacker Launcher relay; details are in
  `experiments/v0042-short-lived-sentinel-circuit-breaker-v199.md` and
  `docs/CURRENT_PLAN.md`.
