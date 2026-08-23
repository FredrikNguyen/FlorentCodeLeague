# v233 legal home-infiltrator block — rejected after one repair

## Hypothesis

The retained v0042 dynamic policy detects an enemy Builder inside the home
threat radius but sends it through the generic strike path. Builder attacks
can only damage adjacent buildings, so this target is not a legal fire target;
the responder can sit beside the infiltrator for the task commitment window
without blocking its route or doing useful work. A single nearest responder
should instead occupy a safe cardinal staging tile between the infiltrator and
our Core. If geometry or turret fire makes that impossible, the response must
be abandoned immediately so the Builder can return to economy work.

## Scope

- `bots/candidate/bot/dynamic.py`;
- one focused infiltrator-block test module;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable state/report
  metadata.

No Launcher, Barrier purchase, Store, route, workforce, turret, Sentinel,
hijack, raid, or offensive-infiltration behavior changes.

## Evidence basis

The v224 replay audit found pre-delivery route-radius enemy-Builder entries in
only **2/13** saved loss/top-team games and **2/15** per side in the top-team
sample, so a broad sentry or opening detour is not justified. The v225–v230
protected-midline, vector-intercept, delivery-gated counter-infiltration,
Launcher-interceptor, and forward-infiltration variants all failed their local
gates. This experiment therefore fixes the existing illegal-action branch
without adding a new proactive infiltration policy.

## Validation and decision

The initial body-block implementation passed **28/28** focused tests,
compileall, and `git diff --check`; `make smoke` was **4/4** command-clean.
`make static` retained the inherited exit 2 from 15 obsolete deleted-module
imports and two navigation fast-path assertions. Its rotated 15-map screen
was command- and delivery-clean at **7-8**, with collection **42,760 vs
64,350 Ti**, first delivery **15/15 vs 15/15**, zero candidate
no-delivery/TLE/suspicious rows, and max p99/peak **1,413/5,204 us**. The raw
report is `reports/local-20260818T230717Z`; parsed diagnostics are preserved
under `reports/iter-v233-legal-home-infiltrator-block/`.

The one bounded repair restricted the body-block to a responder already
adjacent to the enemy Builder, avoiding a route-worker chase. Focused coverage
was **29/29**, compileall and smoke **4/4** stayed clean, and static retained
the inherited result. The rotated screen fell to **6-9**, with collection
**75,560 vs 84,330 Ti**, first delivery **15/15 vs 15/15**, zero candidate
no-delivery/TLE/suspicious rows, and max p99/peak **1,454/3,081 us**. The raw
report is `reports/local-20260818T231051Z`.

Neither screen supplied a repeatable paired win-rate, collection, or response
edge, so no 60-game gate was justified. The temporary source and focused test
were removed; candidate Python is recursively byte-identical to immutable
v0042. Rollback focused coverage was **27/27**, compileall passed, and rollback
smoke was **4/4**. No promotion, package, upload, activation, or live-state
transition occurred. The local baseline remains v0042; choose a different
phase/mechanic rather than widening this infiltration response.
