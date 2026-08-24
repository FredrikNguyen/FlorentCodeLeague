# Strategy and architecture

Karrigan is an economy-first control bot with fixed strategic floors and a
dynamic workforce. Every game unit receives its own persistent `Player`
instance; coordination between units uses the game's delayed 16-slot Global
Store and visible map state.

## Source layout

```text
main.py             Player class, persistent state, and entity dispatch
bot/constants.py    tuning values, roles, task identifiers, and Store layout
bot/core_role.py    workforce staging, economy phase, ammunition, home defense
bot/defender.py     ore discovery, Harvesters, Conveyors, route repair
bot/attacker.py     enemy-Core search, Sentinels, sabotage, siege support
bot/dynamic.py      per-round task selection for flexible builders
bot/navigation.py   bounded cardinal pathfinding and danger avoidance
bot/util.py         coordinate packing and geometry helpers
```

`Player` composes the role mixins with the shared navigation layer. Exceptions
are contained at the entry point because an escaping exception permanently
destroys the affected unit.

## Workforce

The Core grows the team in two stages so early Builder costs do not starve the
first Harvester routes. It tracks living Builders, replaces confirmed losses,
and assigns three fixed roles:

- the first and first reinforcement Builders are permanent attackers;
- the second Builder is the permanent defender;
- every other Builder belongs to the dynamic pool.

The fixed defender protects a minimum economy and the fixed attackers prevent
all workers from converging on defensive or construction work. Dynamic Builders
choose a fresh task whenever their previous task ends or becomes invalid.

## Economy and logistics

Defenders publish visible ore, claim a source, build a Harvester, and construct
a directed Conveyor chain to the Core. Route state is explicit and bounded:
blocked frontiers are retried, invalid seeds are discarded, broken local belts
can be repaired, and disconnected Harvesters can receive a new accepting sink.

The Core publishes an economy phase derived from completed routes, observed
income, and available titanium:

- opening: establish the first working routes;
- converting: restore or extend delivery capacity;
- pressure: preserve one economy steward while releasing surplus workers;
- crisis: prioritize recovery and liquidity.

This phase controls workforce expansion, turret spending, and whether dynamic
Builders may leave economic work for offense.

## Defense

The Core sizes home defense from map geometry, economy, and visible threats. A
single designated Builder owns each requested turret build to avoid duplicate
spending. Builders can repair adjacent friendly structures and respond to shared
home-threat assignments. Surplus home Gunners may be retired during sustained
low liquidity, while a minimum defensive floor remains.

Gunners rotate only when a useful firing line exists. Sentinels are placed with
validated, permanent facings. Ammunition is converted from titanium according to
current demand rather than a fixed unconditional buffer.

## Offense

Permanent attackers search deterministically for the enemy Core, establish a
forward Sentinel pool, and then attack loaded Harvesters, Conveyors, and
Splitters. They can add barriers around enemy territory and use a Launcher relay
when the economy supports it.

Dynamic Builders join pressure only after the route and liquidity gates open.
Their task order adapts among home defense, route repair, source expansion,
sabotage, and forward support. A deterministic advance task provides useful
movement when no higher-priority action is available.

## Safety and performance

- Builder movement is cardinal and bounded by local path-search limits.
- Every build, move, attack, heal, destroy, launch, spawn, and conversion is
  guarded by its matching `can_*` predicate.
- Dynamic prices are read from the controller.
- Store values remain non-negative integers within the 16-slot limit.
- Fixed seeds produce deterministic decisions.
- Local evaluation enforces `--tle 10`.
