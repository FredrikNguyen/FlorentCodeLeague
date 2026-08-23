# v230 forward-infiltration lease — rejected after one repair

## Hypothesis

The replay gap is not frequent enemy Builder infiltration: the v224 audit
found only 1–2 pre-delivery route entries in the small loss/top-team samples,
and the v225–v229 defensive/counter-infiltration variants did not transfer to
win rate. The stronger repeated signal is that losing rows have a weak
forward shell and low workforce while top teams convert already-forward
Builders into pressure.

After the team has at least `OFFENSE_MIN_HARVESTERS` completed routes, a
confirmed enemy-Core sighting, and one live forward Sentinel, a Dynamic Builder
that is already closer to the enemy Core than our own Core may select the
existing visible logistics raid before ordinary visible-ore harvesting. The
existing nearest-owner, loaded-target, reserve, cardinal navigation, and
`can_fire` gates remain the execution path. A home-side Builder is unchanged;
it never walks across the map solely to satisfy this lease.

## Scope

- `bots/candidate/bot/dynamic.py`;
- one focused forward-infiltration priority test module;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable state/report
  metadata.

## Non-goals

No home infiltrator defense, Launcher/teleport, hijack/takeover, route or ore
selection, Store schema, weapon/cost/cap tuning, map branch, fixed-attacker
change, package, upload, activation, or live-state change.

## Validation and decision

The initial implementation passed **5/5** new focused tests plus the existing
nearest-defense subset (**28/28**), compileall, and smoke **4/4**; `make
static` retained the inherited exit 2. The 15-map screen was command- and
delivery-clean with zero TLE/suspicious rows, but finished **6-9** and
collected **59,020 vs 73,950 Ti**. First-delivery and unit/pressure rows showed
the same low-workforce loss pattern, so no release gate was justified. Raw
report: `reports/local-20260818T220818Z` and parsed metrics in
`reports/iter-v230-forward-infiltration/regression-analysis.json`.

The one bounded repair required the complete three-Sentinel shell before a
forward raid could preempt harvesting. It passed **29/29** focused tests,
compileall, and smoke **4/4**; static retained the same inherited exit 2. The
rotated screen remained **6-9**, collected **50,130 vs 55,130 Ti**, and had no
candidate no-delivery/TLE/suspicious rows (`reports/local-20260818T221149Z`,
analysis `reports/iter-v230-forward-infiltration/repair-regression-analysis.json`).

The lease and focused test were removed after the permitted repair. Rollback
coverage passed **27/27**, compileall passed, static retained the inherited
profile, smoke was **4/4**, and candidate Python is recursively byte-identical
to immutable v0042 (`reports/local-20260818T221345Z`). No release gate,
promotion, package, upload, activation, or live transition occurred. The
already-forward raid lease is rejected; do not widen it without new replay
evidence. The infiltration branch is now closed in favor of a different
workforce/pressure mechanism.
