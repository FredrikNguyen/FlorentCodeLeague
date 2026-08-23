# v304 post-shell Dynamic Barrier support

## Hypothesis

After the existing fixed attackers establish a forward Sentinel shell, one
Dynamic Builder already at the enemy Core approach can spend one Barrier on a
local cage without travelling or taking route liquidity.  A three-route gate,
confirmed Core intel, one observed Sentinel, nearest-worker ownership, and a
Harvester-plus-two-Conveyor replacement reserve were intended to keep the
support action safe.

## Scope

Only `bots/candidate/bot/dynamic.py` and focused nearest-defense coverage were
changed.  The experiment did not alter opening routes, roles, Store schema,
fixed-attacker policy, Launcher behavior, infiltration priorities, navigation,
maps, packaging, upload, activation, or live state.  v105 remained the
operational rollback target and immutable local v0044 was the comparator.

## Validation

- Focused nearest-defense, seeded-route, and economy suite: **36/36 pass**.
- `python -m compileall -q bots/candidate`: **pass**.
- `make static`: inherited failure (15 obsolete removed-module imports and two
  navigation fast-path assertions); no new v304-specific failure identified.
- `make smoke`: **4/4 command-clean**, report
  `reports/local-20260819T204656Z`.
- Required 15-map regression screen: **15/15 command-clean**, report
  `reports/local-20260819T204728Z`; replay analysis is in
  `reports/iter-v304-post-shell-barrier/replay-analysis.json`.

## Decision

Reject.  The candidate finished **8–7**, which did not improve the prior
screen, and collected **86,380 vs 90,890 Ti** (candidate −4,510).  Every side
delivered in all 15 games, with max p99/peak execution **1,345/4,592 us** and
zero TLE or suspicious output, but the candidate ended with fewer live
Barriers (**30 vs 55**) and Sentinels (**12 vs 32**).  The intended support
action therefore supplied no repeatable win-rate, shell-survival, or
collection edge; no longer gate or repair was justified.

The temporary production hook and tests were removed.  Recursive source parity
with immutable v0044 is proven by the empty
`reports/iter-v304-post-shell-barrier/rollback-source-parity.diff`.
Rollback focused coverage was **34/34**, compileall passed, static retained
the inherited profile, and rollback smoke was **4/4 command-clean** at
`reports/local-20260819T205110Z`.  Live v107 remains `active_observing`; no
promotion, package, upload, activation, or live transition occurred.

## Remaining risk

The local schedule did not establish a reliable positive post-shell support
case, and the lower shell counts suggest that a Dynamic Builder's opportunity
cost or the existing attacker shell policy—not simply a missing Barrier call—
is the limiting factor.  Future work should inspect a distinct phase/mechanic
against v0044 rather than widening this hook.
