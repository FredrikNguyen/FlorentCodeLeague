# v232 bounded post-route ore-denial lease

## Objective

Replay analysis of the exact v0042 baseline found unclaimed enemy-half ore
denial growing without a lifetime bound: the candidate placed 752 Barriers on
Glacierkeep and 296 on Midgard, versus roughly 7–20 per game in the available
top-team winners. That increases the shared cost scale and diverts dynamic
Builders from route/economy work. Test one structural change: after three
completed own routes, confirmed enemy-Core intel, and enough titanium to
replace one Harvester plus two Conveyors and the Barrier, each dynamic Builder
may make one successful enemy-half ore-denial placement, then permanently
returns to the normal pressure/repair loop.

## Scope and non-goals

Production scope is limited to `bots/candidate/main.py` and
`bots/candidate/bot/dynamic.py`, plus one focused legality/phase test. No Store,
route, fixed-attacker, turret, Launcher, map, baseline, package, upload, or
live-state changes are allowed.

## Validation contract

Run the focused tests, candidate compileall, `make static`, and `make smoke`,
then the rotated 15-map exact-v0042 screen. Record first delivery, collected
Ti, placed Barriers, wins, reliability, and protected-map outcomes. Permit at
most one bounded repair. Promote or run a 60-game gate only if the screen has
a clear paired edge and no reliability/delivery regression; otherwise restore
recursive v0042 parity.

## Repair 1

The initial 15-map screen was 8-7 with a collection edge of 84,750 versus
67,980 Ti and 67 versus 59 placed Barriers, but it introduced one candidate
no-delivery row on Royale (zero Harvesters). The bounded repair keeps the
post-route/reserve/one-shot gates and additionally requires the individual
Builder to have observed a friendly Harvester, Conveyor, or Splitter before
it can spend its denial lease. This guards against a stale delayed chain
counter authorizing pressure before a route exists.

## Result

The initial implementation passed **5/5** new tests plus **23/23** nearest-
defense coverage, compileall, and smoke **4/4**; static retained the inherited
exit 2. The rotated screen was **8-7**, collection **84,750 vs 67,980 Ti**,
Barriers **67 vs 59**, Harvesters **98 vs 119**, with one candidate
no-delivery row on Royale, zero TLE/suspicious rows, and max p99/peak
**1,496/3,130 us** (`reports/local-20260818T224718Z`; replay analysis in
`reports/iter-v232-bounded-ore-denial/replay-analysis.json`).

The one allowed repair required the denying Builder to have observed a
friendly route building. It passed **6/6** new plus **23/23** nearest-defense
tests (**29/29**), compileall, and smoke **4/4**, with the same inherited
static exit 2. Its screen fell to **7-8**, collection **69,560 vs 89,900 Ti**,
Barriers **52 vs 67**, Harvesters **98 vs 152**, and one candidate
no-delivery row on Drakkarfjord; max p99/peak was **1,319/3,005 us**, with
zero TLE/suspicious rows (`reports/local-20260818T225231Z`; replay analysis in
`reports/iter-v232-bounded-ore-denial/repair-replay-analysis.json`).

The hypothesis is rejected after the allowed repair. Temporary source/test
edits were removed; rollback focused coverage was **27/27**, compileall passed,
static retained exit 2, smoke was **4/4** at
`reports/local-20260818T225529Z`, and candidate Python is recursively
byte-identical to immutable v0042. No release gate or platform operation was
justified. Detailed logs and replay metrics are under
`reports/iter-v232-bounded-ore-denial/`.
