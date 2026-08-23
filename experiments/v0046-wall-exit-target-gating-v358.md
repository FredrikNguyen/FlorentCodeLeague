# v358 wall-exit target gating — rejected

Date: 2026-08-20

## Hypothesis

Live v108 Yulerune showed a fixed attacker oscillating behind a visible static
central wall.  v358 added a bounded, target-specific wall-exit subgoal using
only visible passable tiles and the normal navigation/can-move path.  When the
opening was outside the Builder's 20-square vision, one allowed repair added a
visible staging waypoint so the next window could reveal more terrain.

## Scope

Temporary changes were limited to `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and
`tests/test_candidate_nearest_defense.py`.  No baseline, Store schema,
economy, unit policy, package, upload, activation, or live state was changed.

## Evidence

- Initial focused coverage: **28/28**; compileall passed; smoke **4/4**.
- Initial immutable-v0046 15-map screen (seed 181): **8-7**, reliability-clean.
- One bounded repair added vision-fringe staging.  Focused coverage became
  **29/29**; compileall passed; `make smoke` was **4/4**.  `make static`
  retained only the inherited 15 obsolete-module import errors and two stale
  navigation assertions.
- Repaired first rotated screen (seed 183) was **9-6**, command/TLE/
  suspicious/delivery-clean: `reports/local-20260820T161525Z`.
- Required second rotated screen (seed 191) was **8-7**, also reliability-clean:
  `reports/local-20260820T161752Z`.  The two-screen aggregate was **17-13**,
  below the **19-11** pair gate.

## Decision and rollback

The candidate failed the pair gate after the one permitted repair.  v358 is
rejected; no release-gate matrix, remote gate, package, upload, activation,
or promotion ran at the time of rollback.  Candidate production source was
restored to exact recursive v0046 parity (excluding generated caches); evidence
is
`reports/iter-v358-wall-exit-target-gating/rollback-source-parity.diff` (empty).
Rollback focused coverage is **26/26**, compileall passed, inherited static
profile remains exit 2, and rollback smoke is **4/4** at
`reports/local-20260820T162140Z`.

## User-requested archival long gate

The exact v358 source was reconstructed from the archived patch sequence in an
isolated directory; the repository candidate remained at v0046 parity.  The
explicit 60-game v0046-pinned all-map/both-side matrix was
`reports/local-20260820T163725Z`:

- **30-30** candidate wins, below the **33-27** release floor;
- **60/60** candidate deliveries, zero command failures, zero TLEs, and zero
  suspicious-output rows;
- maximum p99/peak bot time **1,414/5,123 us**;
- candidate collected **331,420 Ti** versus **346,570 Ti** for v0046;
- map floor: **Yulerune 0-4** (Midgard was 4-0; no other map exceeded 3-1).

The long gate confirms the 9-6 screen was not a reliable general improvement;
v358 remains rejected and was not copied back into the candidate.

The post-gate repository smoke was **4/4** at
`reports/local-20260820T164656Z`.  `make static` remains the inherited exit-2
profile (15 obsolete-module import errors and two navigation fast-path
assertion failures), with no new v358-specific source change; logs are
`reports/iter-v358-wall-exit-target-gating/post-long-rollback-smoke.log` and
`post-long-rollback-static.log`.

## Fresh live snapshot

The read-only observation at
`reports/live-observe-20260820T162527Z` still showed v108 active and ready.
The current platform status was rating **1575.90**, rank **40/129**, and a
recent **5-5** record.  The live operator remained `active_observing`; no
upload, activation, rollback, or promotion was requested or performed.

## Remaining risk

The live-v108 wall stall remains a real topology failure, but a local
wall-facing waypoint is not reliably better than v0046 across rotated maps.
Future work must use a new hypothesis and retain strict visible-information and
pair reliability gates; do not revive this implementation unchanged.
