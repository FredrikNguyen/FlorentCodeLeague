# v350 per-Builder mission scheduler — rejected, v0046 retained

Date: 2026-08-20

## Objective and live evidence

v108's fresh ladder loss to Askar City, match
`23ac1188-4a68-4c2e-a12a-f8dd36bf9916`, was a 0-5 loss without a TLE or
suspicious output.  The replay analysis showed an economic conversion fault,
not an execution-budget fault: on several maps v108 had 31-60 conveyors but
only 1-3 live Harvesters.  On Auroraveil it made no titanium delivery; the
opponent delivered on turn 23.  Nordkap delivered on turn 105 while the
opponent delivered on turn 15.  Royale had 60 conveyors and two Harvesters
against five opponent Harvesters.  The raw capture and replay analysis are in
`reports/live-v108-scheduler-audit-20260820T115830Z`.

The candidate therefore tested a structural per-Builder mission scheduler.
Route missions were meant to retain a Builder until a concrete Harvester/route
outcome; completed or invalid missions transitioned the Builder to visible
pressure or home defense, with an explicit fallback rather than an idle role.
This was deliberately a role/lifecycle rewrite, not a parameter change.

## Scope and implementation

Allowed production scope was `bots/candidate/main.py`,
`bots/candidate/bot/defender.py`, and `bots/candidate/bot/dynamic.py`, plus a
temporary focused scheduler test.  The initial candidate recorded local route
and pressure missions, shifted completed dynamic routes into pressure, and
returned them to route work after a pressure/support outcome.  The route owner
also skipped hijack and turret detours while actively building its route.

Repair 1 admitted an affordable, visible enemy Harvester as a route source.
Repair 2 delayed the pressure transition until four verified normal home
routes, matching the opening workforce floor.  Store schema, Core spawn
policy, fixed identities, immutable snapshots, package, platform, and live
state were non-goals.  All temporary production and test changes were removed
after the second repair failed.

## Validation

- Focused scheduler/economy/route coverage passed **40/40**, **41/41**,
  **43/43**, and **44/44** through the candidate and repairs.  Rollback
  coverage passed **35/35**.  Compileall passed throughout.
- `make static` remains an inherited exit 2: 15 obsolete candidate-module
  imports and two navigation fast-path assertions.  It did not reveal a new
  v350 production failure.  Rollback smoke was **4/4 command-clean** at
  `reports/local-20260820T121048Z` (that smoke configuration still uses the
  older v0044 comparator, so it is only a submission-path check).
- Initial all-map screen, against immutable v0046 on screen seed 172, was
  **6-9** with delivery in all 15 rows, zero TLE/suspicious output, and max
  p99/peak **1,433/2,827 us**:
  `reports/local-20260820T120014Z`.  Auroraveil first delivery regressed from
  v0046's turn 31 to turn 117.
- Repair 1 was **8-7**, delivery-clean, with zero TLE/suspicious output and
  max p99/peak **1,389/5,595 us**:
  `reports/local-20260820T120336Z`.  That one-map margin was not a sufficient
  or repeatable edge.
- Repair 2 was **6-9**, delivery-clean, with zero TLE/suspicious output and
  max p99/peak **1,262/2,329 us**:
  `reports/local-20260820T120632Z`.  It created severe long-map conversion
  regressions: Auroraveil first delivery **302 vs 28**, Glacierkeep **93 vs
  38**, and Royale **100 vs 22** turns against v0046.

## Decision and rollback

Reject v350 after the two permitted bounded repairs.  Neither version produced
a repeatable aggregate win-rate edge, and the four-route repair made the
specific live failure class substantially worse.  Candidate production source
was restored exactly to immutable v0046; the recursive source parity proof is
the empty `reports/iter-v350-final-source-parity.diff` (excluding generated
`__pycache__` directories).  Rollback focused and compileall logs are
`reports/iter-v350-mission-scheduler-rollback-focused.log` and
`reports/iter-v350-mission-scheduler-rollback-compileall.log`.

No release gate, promotion, package, upload, activation, or live transition
occurred.  A fresh read-only capture at
`reports/live-v108-final-audit-20260820T121432Z` confirms that platform v108
(`v0045-opening-launcher-relay-eeafad8f`) remains ready and active at 1578.12,
rank 40/129, with an 8-2 recent record.  Its durable live state remains
`active_observing`, so deployment is also blocked by policy until that
observation is resolved.

## Remaining risk and next direction

Do not retry v350's scheduler, visible-hijack ordering, or four-route threshold
as another variation.  The next bounded experiment must inspect the current
long-map loss replays and introduce one local, vision-safe opening
source-admission rule: do not commit the opening workforce to a route that
cannot promptly form a Core-facing delivery path; keep exploring or choose a
nearer viable source instead.  It must not reintroduce v343's BFS/reservation
mechanism unchanged, alter Store/Core/fixed identities, or spend on pressure
before real route income and home safety are proven.
