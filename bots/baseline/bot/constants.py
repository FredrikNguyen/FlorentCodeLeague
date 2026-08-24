"""All tuning knobs, direction tables, and communication-store slot
assignments in one place — this is the file to edit when balancing the bot.

Communication store slots (all single-writer unless noted):
  0  SLOT_CORE_X          Core X position PLUS 1 (written by the core every round)
  1  SLOT_CORE_Y          Core Y position PLUS 1
       Both carry a +1 offset, same convention as util.pack_pos: an unwritten
       slot reads 0, so a raw 0 can't be told apart from a real coordinate 0.
       A core at (0, 0) therefore looked permanently unpublished and every
       builder ran with core_pos=None all match — no conveyors, no core ring,
       no harvest range limit. See main._read_core_pos.
  2  SLOT_DEFENDER_ID      Id of the Builder designated to build the next
                           home-defense Gunner (core)
  3  SLOT_CORE_SIEGE      Core distress beacon (core-authoritative): missing HP
                          packed with the position of the enemy turret nearest
                          our core. See SLOT_CORE_SIEGE below.
  4  SLOT_ORE_CURSOR      Packed economy phase (high bits) plus the
                          round-robin write cursor (low bits) into the ore
                          ring-buffer
  5-8 ORE ring-buffer     Up to 4 advertised uncovered-ore locations
  9  SLOT_ENEMY_CORE      Packed position of the enemy core, once spotted by
                          anyone (multi-writer, but idempotent enough: whoever
                          sees it writes the same tile, so a same-round race
                          just costs a round of latency, never a wrong value)
  10 SLOT_GUNNER_CAP      Core-authoritative dynamic home-turret cap (2-5)
  11 SLOT_HARVESTER_COUNT Completed harvester chains (multi-writer, see below)
  12 SLOT_PERMA_ATTACKER_ID Id of the first builder ever spawned — always an
                            attacker, regardless of the harvester milestone
                            (core-only, written once)
  13 SLOT_SECOND_ATTACKER_ID Id of the first builder spawned once the stage-2
                            reinforcement wave unlocks — also always an
                            attacker, to reinforce the first (core-only,
                            written once)
  14 SLOT_SENTINEL_COUNT   Forward sentinels observed near the enemy core, so
                            the core knows to bank siege ammo (multi-writer,
                            see below)
  15 SLOT_PERMA_DEFENDER_ID Id of the one builder permanently on economy duty
                            — the defender floor (core-only, written once:
                            the second builder ever spawned)

THE STORE IS FULL (slots 0-15 all assigned). Slot 3 used to be
SLOT_GUNNER_COUNT — written every round by the core and never read by
anything — and has been reclaimed for SLOT_CORE_SIEGE, which is read by
every builder.

NOTE: store writes are buffered until the next round, so a read-modify-write
"counter" incremented by several units in the same round is always wrong — every
writer sees the same stale value. Slots 2, 3, 10, 12 and 13 are therefore
written by the core only, and the home-turret cap is serialised through a
single designated builder. SLOT_HARVESTER_COUNT and SLOT_SENTINEL_COUNT are the
deliberate exceptions: any defender may increment the former on completing a
chain, and any attacker may write the latter on placing the sentinel, so a
same-round race with another unit doing the same thing just costs a round of
latency (an under-count, or briefly two attackers both trying to build one),
never a wrong value. Both are coarse "has this happened yet" signals, not
hard caps, so that's fine.

Because a store write from round R isn't visible until round R+1, a freshly
spawned unit's very first round can never see a designation the core made for
it that same round (e.g. SLOT_PERMA_ATTACKER_ID for the builder just spawned).
Builders therefore defer their one-time role decision by exactly one round
after spawning (see main.py's _run_builder) rather than deciding immediately.
"""

from fcode import Direction

# All directions except CENTRE — useful for turret facing (allows diagonals).
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

# Cardinal directions only — builder movement, harvester/conveyor adjacency, and
# conveyor facing are all cardinal. Compass: (0, 0) is the map's NORTHWEST corner,
# so NORTH = (0, -1) (toward row 0) and EAST = (1, 0).
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

# --- Communication store slot assignments (see module docstring above) ---
SLOT_CORE_X = 0
SLOT_CORE_Y = 1
SLOT_DEFENDER_ID = 2      # core-only: next home-defense Gunner builder
SLOT_CORE_SIEGE = 3       # core-only: packed (missing core HP, sieging-turret pos)
SLOT_ORE_CURSOR = 4
SLOT_ORE_QUEUE_BASE = 5   # a ring-buffer occupying slots 5, 6, 7, 8
ORE_QUEUE_LEN = 4
# SLOT_ORE_CURSOR is already a shared delayed channel. Keep its four low bits
# compatible with the old cursor (the ring is length four) and use the high
# bits for a small Core-published economy phase. Builders preserve those bits
# whenever they advance the cursor, so an ore advertisement cannot erase the
# income heartbeat.
ORE_CURSOR_MASK = ORE_QUEUE_LEN - 1
ECONOMY_PHASE_SHIFT = 2
# Zero means "the Core has not published a phase yet" and preserves the
# legacy route-count behavior for lightweight fixtures/old delayed state.
ECONOMY_PHASE_MASK = 0b111 << ECONOMY_PHASE_SHIFT
ECONOMY_PHASE_OPENING = 1
ECONOMY_PHASE_CONVERTING = 2
ECONOMY_PHASE_PRESSURE = 3
ECONOMY_PHASE_CRISIS = 4
SLOT_ENEMY_CORE = 9       # packed position, written by whichever attacker spots it
SLOT_GUNNER_CAP = 10      # core-only: dynamic home-turret cap, 2-5
SLOT_HARVESTER_COUNT = 11 # completed harvester chains (deliberately multi-writer)
SLOT_PERMA_ATTACKER_ID = 12    # core-only: id of the first (always-on) attacker
SLOT_SECOND_ATTACKER_ID = 13   # core-only: id of the stage-2 reinforcement attacker
SLOT_SENTINEL_COUNT = 14       # forward sentinels seen near enemy core (multi-writer)
SLOT_PERMA_DEFENDER_ID = 15    # core-only: id of the one always-on defender (floor)

# How many LIVING builder bots the core aims to keep fielded (not a lifetime
# total — see core_role._prune_dead_builders, which tracks who's actually
# still alive so combat losses get replaced). Staged in two waves rather than
# one flat target:
#
#   living < INITIAL_BUILDER_TARGET (3)      -> the starting roster: the
#     permanent attacker (SLOT_PERMA_ATTACKER_ID) plus 2 defenders.
#   harvester count >= HARVESTER_MILESTONE   -> unlocks a second wave up to
#     REINFORCEMENT_BUILDER_TARGET (6); the first builder spawned in that
#     wave is also always an attacker (SLOT_SECOND_ATTACKER_ID), reinforcing
#     the first.
#
# Keep the opening workforce small until a chain proves that the economy can
# repay the global scale increase, while a bounded round fallback prevents a
# stalled first route from freezing the whole workforce.
INITIAL_BUILDER_TARGET = 5
REINFORCEMENT_BUILDER_TARGET = 8
SPAWN_RESERVE = 40             # keep at least this much Ti spare after spawning


# Hard floor: always try to replace COMBAT LOSSES back up to this many living
# builders, bypassing SPAWN_RESERVE (though not the raw cost — we still can't
# spawn what we can't afford) if attrition drops us below it after we've once
# reached our initial roster (core_role tracks this via self.ramp_established
# — the bypass deliberately does NOT apply during the very first ramp-up to
# INITIAL_BUILDER_TARGET, only to replacing losses afterward, so it can't
# reproduce the same early-overspend problem staging above just fixed).
# Without this floor at all, a team that already had a full roster and then
# lost bots to combat had no way to ever spawn again once past whatever the
# flat lifetime cap used to be, which is exactly how a team ended up stuck at
# 1 living builder for the rest of a game.
MIN_BUILDERS_ALIVE = 3

# Global ammo buffer the core maintains. Ammo is ONE shared team-wide pool
# feeding home gunners and forward sentinels alike.
#
# The two numbers differ by an order of magnitude because the consumers do:
# a gunner shot is 2 ammo, a SENTINEL shot is 10. A full 3-sentinel pool
# firing on reload-3 burns ~10 ammo/round sustained, and killing a 500 HP
# core at 18 dmg/shot takes ~28 sentinel shots ≈ 280 ammo. Running the siege
# dry is the difference between sentinels that win the game and sentinels
# that are expensive scenery, so once any forward sentinel exists
# (SLOT_SENTINEL_COUNT) the core switches to the siege buffer.
#
# PRESTOCK_ROUND is early enough that ammo is banked before the first
# sentinel lands rather than after — banking is 1:1 titanium, so the cost is
# real, but arriving late wastes the sentinel's whole early-game window.
AMMO_BUFFER = 30
AMMO_BUFFER_SIEGE = 150
AMMO_PRESTOCK_ROUND = 40

# Hard floor, topped up EVERY round regardless of round number or threat —
# 10 ammo is one sentinel shot or five gunner shots. The point is that a
# turret is never sitting there unable to fire because the buffer logic
# hadn't unlocked yet: every other ammo rule here is gated on something
# (round >= PRESTOCK, a visible threat, sentinels existing), and all of
# those gates can be shut at the exact moment a turret first needs a shot.
AMMO_FLOOR = 10

# Titanium the FLOOR rule may never convert. This is separate from
# AMMO_ECONOMY_RESERVE (which only ever guarded the *buffer* rule) and it is
# the single most expensive line in this file's history.
#
# The floor used to run on `budget = resources` — literally the whole
# balance, reserving nothing. Combined with forward sentinels, which drain
# 10 ammo per shot continuously, that made a ratchet: sentinel fires -> ammo
# drops below 10 -> the core converts EVERY titanium we own into ammo ->
# balance 0 -> sentinel fires again. Measured over 21 ladder games (the
# `replays/` set, vs opponents that actually pressure us):
#
#   titanium collected all game        7,430
#   titanium converted to ammo        10,725   (more than we ever earned)
#   ...of it converted while under 60 Ti  7,995  (75%)
#   turns spent below 20 Ti (a harvester)  61% of all turns
#   games where we collected ZERO titanium  7 of 21
#
# At a zero balance the bot can neither build a harvester (20 Ti) nor HEAL
# (1 Ti), so one unreserved constant caused both the economic deadlock and
# the defensive collapse — our core was healed for 510 HP across those 21
# games while enemy cores were healed for 9,352.
#
# The reserve is small on purpose: the floor's job (a turret is never dry)
# is real, and this only stops it taking the last scraps. Note the exchange
# rates that make the reserve correct — 1 Ti of healing is 4 HP, 1 Ti of
# ammo through a sentinel is 1.8 HP of damage, so titanium held back for
# repairs outperforms titanium spent on shooting whenever we are the one
# being attacked.
AMMO_FLOOR_RESERVE = 25

# Consecutive rounds with a balance below one harvester's price before the
# core treats itself as economically deadlocked and stops feeding the ammo
# floor entirely until it can afford a harvester again. A healthy game dips
# under this briefly all the time (that is just spending), so the threshold
# is about telling "spending" apart from "stuck": on the ladder replays the
# stuck games sat under the line for 100+ consecutive rounds.
DEADLOCK_POOR_ROUNDS = 12

# --- Measured, mirror matches against the pre-fix bot, both seats, 33 maps ---
# Every row is several independent 66-game sweeps pooled. `random.*` is not
# reseeded by --seed, so each sweep is a genuinely fresh sample; 1 sigma at
# n=330 is ~2.8 points, so read anything under ~6 points between two rows as
# a tie. The control row is the baseline played against ITSELF and is the
# reference for what 50% looks like in this harness.
#
#   control: baseline v baseline              102/198 = 51.5%
#   flat reserve of 25                        115/198 = 58.1%   (+1.3 sigma)
#   need-based reserve                        209/330 = 63.3%   (+3.0 sigma)
#   need-based + deadlock streak              198/330 = 60.0%   (+2.2 sigma)
#   ...and head to head, streak v no-streak   112/198 = 56.6%
#
# The last two rows are a tie against the baseline (0.85 sigma apart) and the
# streak version wins the direct comparison, which is why it ships. Do not
# read the 63.3% as evidence that dropping the streak is better.
#
# Mechanism deltas over the same games (per 1000 turns, which matters because
# the fixes roughly double game length and every raw total moves with it):
#
#                              baseline   shipped
#   titanium -> ammo               1512       995
#   ammo as a share of all Ti       19%       13%
#   our core healed                  91      1713
#   core damage dealt              2063      1390    <-- the cost
#   turns below 20 Ti               27%       10%
#
# The offence loss is real and was the reason for making the reserve
# need-based rather than flat (a flat 25 cut damage dealt to 1136). It is
# paid for by durability: heal is 4 HP per titanium against a builder's
# 1 HP per titanium of attack, so titanium held back for repair beats
# titanium spent on shooting whenever we are the side being attacked.

# Home defense: turrets are secondary to economy on most maps — only start
# considering one once the game has run a while and we have titanium to spare
# beyond running the economy, cap the count low, and keep them off a ring close
# around the core so they never block a belt tile. The core recomputes the
# live cap (MIN_GUNNERS..MAX_GUNNERS_CAP) every round from economy + visible
# threat in core_role._update_defense — see SLOT_GUNNER_CAP above.
MIN_GUNNERS = 2
MAX_GUNNERS_CAP = 5
GUNNER_MIN_ROUND = 150
ECONOMY_RESERVE = 60
ECONOMY_RICH_THRESHOLD = 400    # global Ti banked beyond reserve -> afford more turrets
GUNNER_NEAR_CORE_DIST_SQ = 18
GUNNER_MIN_CORE_DIST_SQ = 8

# On small/cramped maps (enemy core within a short walk — see _is_cramped) combat,
# not economy, decides the match: a starved turret cap left us defenseless for
# most of the game empirically, so both the cap and the timing shift.
CRAMPED_CORE_DIST = 20          # core-to-core Manhattan distance considered "close"
GUNNER_MIN_ROUND_CRAMPED = 0
ECONOMY_RESERVE_CRAMPED = 30

# Conveyor-chain tuning.
CHAIN_SLACK = 8            # tiles of detour allowed over the straight-line length
CHAIN_BLOCKED_LIMIT = 20   # give up a chain after this many stalled rounds

# --- Belt output classification (defender._belt_output_status) ---
# What a conveyor's own output tile can do with a stack. The distinction that
# matters is DEAD vs GAP: a GAP is one missing tile away from working and the
# repair task already handled it, while DEAD means the belt is pointed at
# something that will NEVER accept a stack, so everything upstream of it is
# delivering into nowhere.
#
# Measured on 8 fresh replays (final frames, our team): only 4% of belts were
# terminally misdirected — 6 mutual loops, 2 into walls, 7 severed — but each
# defect strands roughly SEVEN belts behind it. Simulating a repair of just
# those took harvester connectivity from 78% to 95% and live belts from 51%
# to 66%. On vault it was the difference between 2/6 and 6/6 harvesters
# delivering.
#
# VERIFIED, not assumed: across ~79,000 resource-move events in recorded
# replays, stacks are only ever delivered into a CONVEYOR or a CORE.
# Harvesters appear exclusively as move SOURCES, never destinations — so a
# conveyor aimed at a harvester really is a dead end, as are barriers and
# turrets. Walls matter separately because is_tile_empty() reports False for
# a wall, so a belt aimed into one is invisible to the "output tile is empty"
# severed-belt check that existed before.
BELT_OUT_UNKNOWN = 0   # out of vision — never act on this
BELT_OUT_CORE = 1      # delivers home
BELT_OUT_BELT = 2      # feeds another friendly conveyor/splitter
BELT_OUT_GAP = 3       # buildable empty tile: severed, one build from fixed
BELT_OUT_DEAD = 4      # wall, off-map, non-accepting building, or mutual loop

# MEASURED OUTCOME of acting on this classification (repair by re-pointing,
# plus refusing to lay a known-dead tile in the first place). 66 games each,
# 33 maps x both seats vs bots/friend:
#   harvesters connected to the core   72% -> 84%
#   conveyors on a live route          47% -> 57%   (stranded 1040 -> 710)
#   mutual loops                        20 -> 0
#   belts aimed into a building          5 -> 0
#   belts aimed into an empty tile      34 -> 22
# Win rate moved 73.9% -> 75.3% across 396 games, which is only ~0.4 sigma —
# treat the win-rate change as unproven and the connectivity change as real.
# Fewer harvesters get built per game afterwards (8.8 -> 7.3), which is NOT
# economy suppression: mean game length fell from 623 to 542 turns, so the
# same win rate is being reached sooner.

# Harvesting: only plant a harvester within (w+h)*HARVEST_RANGE_FRAC Manhattan
# tiles of the core, so its chain can reach home before the enemy contests it.
HARVEST_RANGE_FRAC = 0.5

# --- Early economy protection ---
# While the team has fewer than this many completed chains, the economy is
# hand-to-mouth and everything else has to get out of its way. Measured
# baseline before this existed: chains stalled flat at 2.0 from round 75 to
# 125 with titanium pinned at 14-20, because a scaled harvester costs ~35
# and we simply never accumulated that much.
ECONOMY_PRIORITY_CHAINS = 3
# Dynamic workers can release into raids after the normal three-route opening
# only when the bank is healthy.  If the team has three or four recorded
# routes but cannot currently fund a replacement Harvester, two short links,
# and the fixed offense reserve, keep them exploring/harvesting until this
# floor is reached.  This is deliberately separate from
# ECONOMY_PRIORITY_CHAINS: the latter also controls early route geometry and
# the Core's ammo reserve, while this is only a liquidity-backed workforce
# handoff.  It protects against route cuts/infiltration without suppressing
# continuous pressure when the bank can actually replace a lost route.
DYNAMIC_ECONOMY_FLOOR = 5
# Keep dynamic workers on the economy until a larger route base exists. This
# is intentionally separate from OFFENSE_MIN_HARVESTERS: the permanent
# attacker can pressure at three while the scalable pool keeps finding ore.
# Two drains, both fixed by ECONOMY_PRIORITY_CHAINS:
#
# 1. Chain LENGTH. A harvester is only worth what it delivers, and a chain
#    costs ~1 conveyor per tile AND two rounds per tile to lay (move, then
#    build). HARVEST_RANGE_FRAC allows ore up to (w+h)/2 manhattan away — on
#    a 30x30 map that is a 30-tile chain: ~90 Ti and ~60 rounds before the
#    first stack moves. Early on we cap it far shorter, so the first chains
#    are cheap and start paying immediately; the long-range ore is still
#    there later once we can afford it.
EARLY_HARVEST_RANGE = 12
#
# 2. Panic turrets. _update_defense normally jumps the gunner cap straight to
#    MAX_GUNNERS_CAP and drops the economy reserve the moment ANY enemy is
#    visible near the core — a single passing scout could therefore buy five
#    turrets out of the harvester budget. Below the threshold we hold the cap
#    at MIN_GUNNERS and keep the reserve, so early defence stays proportionate.

# Exploration: pick targets at least this far away so bots actually travel out.
EXPLORE_MIN_DIST_SQ = 16

# Navigation: abandon a target after this many rounds without getting closer
# (escapes walls/traps we can't path around), and keep unreachable targets
# blacklisted for a while so we don't immediately re-pick them.
NAV_GIVEUP = 14
BLACKLIST_ROUNDS = 40
VISITED_MAX = 600

# Builder roles (chosen once, for life) and the DEFENDER economy sub-mode.
# DYNAMIC builders keep their role for life too — what changes round to round
# is which TASK_* they're pursuing (see dynamic.py). Only the three floor
# roles (2 attackers + 1 defender) are fixed designations; everyone else is
# dynamic. See DESIGN_dynamic_builders.md.
ROLE_DEFENDER = 0
ROLE_ATTACKER = 1
ROLE_DYNAMIC = 2
MODE_SCOUT = 0
MODE_CHAIN = 1

# --- Dynamic-builder task priorities (LOWER number = HIGHER priority) ---
# Strict discrete ordering, which is what gives us tie-hysteresis for free:
# a task is preempted only by a *strictly* smaller number, never an equal
# one, so two near-tied options can't trade places round after round.
TASK_HOME_THREAT = 0    # enemy near our core: turret > harvester > anything
TASK_HIJACK = 1         # put our belt beside an enemy harvester and steal output
TASK_BELT_REPAIR = 2    # gap in our conveyor network (a dead belt = zero income)
TASK_HARVEST = 3        # the normal economy loop (delegates to defender.py)
TASK_BASE_REPAIR = 4    # heal a damaged friendly building at home
TASK_RETIRE_GUNNER = 5  # remove a surplus home Gunner under low liquidity
TASK_RAID = 6           # destroy a visible enemy logistics building
TASK_ORE_DENIAL = 7     # barrier an ore tile on the enemy's half
TASK_ADVANCE = 8        # nothing local applies: march on the enemy core
TASK_NONE = 99          # no task held

# NOTE on BASE_REPAIR sitting BELOW harvest: it was tried above harvest and
# measured worse (win rate 25-8 -> 21-12, median titanium collected
# 2730 -> 2070). Healing preserves income; harvesting *adds* it, so expansion
# should win whenever ore is actually available. Since HARVEST only fires
# when there's ore to take, keeping repair below it means "maintain the base
# when there's nothing better to do", not "never maintain the base".

# Answering an enemy turret by SHOOTING it with builder-fire is a losing
# trade and was observed to be far too slow: a builder deals 2 dmg/hit, so a
# 30 HP sentinel takes 15 consecutive rounds parked inside its kill zone,
# while a gunner shooting back kills the 40 HP builder in 4. Building a
# counter-gunner instead flips it — 10 dmg/shot on reload 1 kills that
# sentinel in 3 — and, crucially, the builder is free to walk away
# immediately instead of being pinned. Range is the gunner's own r²=13.
COUNTER_TURRET_RANGE_SQ = 13

# Stickiness. Tasks primarily end on their own termination condition
# (target achieved / confirmed gone), not on a clock — TASK_MAX_ROUNDS is
# only a backstop so a builder can't chase one thing forever. COMMIT_FLOOR
# is the residual anti-flicker damper for a higher-priority target blinking
# in and out of vision; it is id-varied (floor = MIN + id % SPREAD, so 3/4/5)
# so builders re-evaluate on different rounds instead of switching in
# lockstep — the response-threshold trick from swarm task allocation.
COMMIT_FLOOR_MIN = 3
COMMIT_FLOOR_SPREAD = 3
TASK_MAX_ROUNDS = 40

# How close to our own core an enemy has to be to count as a "home threat".
# Was 100 (a 10-tile radius), which on most maps reaches past the midline —
# combined with counting every enemy belt as a threat, dynamic builders spent
# 48% of their rounds on HOME_THREAT and never once advanced or denied ore.
# 49 (7 tiles) is our base and its immediate approaches, which is what
# "defend home" should actually mean. Only turrets, harvesters and enemy
# builders qualify — see _find_home_threat.
HOME_THREAT_RADIUS_SQ = 49

# Completed harvester chains that mark "the economy is established". Used for
# two things deliberately kept in lockstep, since "we have income to spare" is
# the same condition either way: it unlocks the stage-2 builder wave in
# core_role.py, and the first builder of that wave becomes the second
# permanent attacker. Gated on real chains (SLOT_HARVESTER_COUNT) rather than
# a round number, so a slow economy doesn't get raided empty and a fast one
# doesn't sit around idle.
#
# There is no longer a "1-in-N spawns becomes an attacker" rule: every builder
# beyond the three fixed floor roles is DYNAMIC and decides what to do by task
# priority instead (see the TASK_* block above and dynamic.py).
HARVESTER_MILESTONE = 1

# How close (dist_sq to the enemy core's reported anchor tile) counts as
# "close enough to switch from travelling to punching the core directly" —
# the core is a 2x2 footprint, so a tile orthogonally adjacent to its far
# corner can be up to dist_sq 5 from the anchor tile get_position() reports.
# This gates BUILDER-FIRE harassment only, never sentinel placement.
HARASS_RANGE_SQ = 5

# Forward sentinels: the actual win condition. A sentinel's attack radius is
# r²=32 — SIX TIMES the harassment range above — and can_fire_from() was
# verified empirically to be purely geometric, NOT vision-gated (it returns
# True for an aligned target at dist_sq 25, past a builder's own r²=20
# vision, and False only past 32). So a builder can plant a sentinel aimed
# at a core it knows about but cannot currently see, from real standoff
# distance. Gating placement on the much tighter HARASS_RANGE_SQ — as an
# earlier version did — threw away almost all of that reach and forced
# attackers to walk into point-blank danger to build anything.
#
# We aim for a maintained pool of SENTINEL_POOL_TARGET (matching STRATEGY.md).
# The count is re-observed every round rather than latched, so a destroyed
# sentinel is naturally replaced.
SENTINEL_RANGE_SQ = 32
SENTINEL_POOL_TARGET = 3

# --- Forward-sentinel site memory (the treadmill brake) ---
# The pool target above says how many sentinels we WANT. This says where we
# refuse to keep putting them.
#
# Measured from lost-game replays (see replays/, decoded and analysed round by
# round):
#   snowflake, 1000 rounds: 143 sentinels built, 142 destroyed, MEAN LIFETIME
#     5 ROUNDS, and 140 of the 143 on the exact same tile (20,18). Sentinel
#     cost plus the ammo they burned came to ~7300 Ti of a ~16550 lifetime
#     budget — 44% — and we lost that game on the titanium tiebreak.
#   drumlin, 632 rounds: 41 sentinels, all lost, same ~5-round rhythm;
#     ~4400 Ti of a ~6120 budget, 72%.
#
# The fix that WORKS is narrow: ban the individual tile that ate a short-lived
# sentinel. The placement search is deterministic given the same geometry, so
# without a memory it re-derives the same doomed tile forever; with one, the
# attacker is pushed to a different approach angle instead of feeding the same
# kill zone.
#
# TUNING HISTORY — and this one matters, because the obvious reading of those
# replay numbers is WRONG. Sweeps of 66 games each (33 maps x both seats)
# vs bots/friend, zero errors throughout:
#
#   baseline (no changes)                        179/264  67.8%  median Ti ~1000
#   + the two core bugs fixed only               183/264  69.3%  median Ti ~1140
#   + tile blacklist  (SHIPPED)                  195/264  73.9%  median Ti ~1140
#   + generous lifetime ammo cap on top          138/198  69.7%  median Ti ~1700
#   + surplus reserve, harvester gate, rate cap  148/264  56.1%  median Ti ~2900
#
# That last row was the first attempt: gate forward sentinels behind 120 Ti of
# surplus, 3 completed chains, and a 50-round replant cooldown. It TRIPLED
# median titanium collected and cost 13 points of win rate — roughly 4 sigma,
# not noise. Economy is not the objective function; killing the core is. The
# heavy gates suppressed the strategy that actually closes games, and we
# out-collected opponents into tiebreak losses instead of killing them.
#
# The error behind it is worth remembering: the replays analysed were a sample
# of LOSSES ONLY, so of course the sentinel strategy looked wasteful in them.
# Nothing in that sample showed what it was winning elsewhere. Diagnose from a
# biased sample, verify the fix on the full distribution.
#
# The lifetime ammo cap is a genuinely open question rather than a settled no:
# it measured neutral-to-slightly-negative, which suggests the ammo really was
# buying something even in games we lost. Left out for now.
SENTINEL_MIN_LIFETIME = 20
SENTINEL_SITE_BLACKLIST = 250

# --- Economy-before-offense gate ---
# Completed harvester chains the TEAM needs before any dynamic builder is
# allowed to go on offense (advance / deny ore / plant sentinels).
#
# This exists because of a real failure: a dynamic builder only picked
# TASK_HARVEST when ore was *already visible or advertised*, whereas a
# DEFENDER with no ore in sight goes and EXPLORES for some. So the moment
# ore wasn't literally in view, the entire dynamic pool fell through to
# TASK_ADVANCE and marched off to attack — permanently, since they were then
# far from home and never saw ore again. The bot built sentinels and
# attacked well while never building an economy, then lost on resources.
#
# Below this threshold, dynamic builders behave exactly like defenders
# (including exploring for ore). Above it, the normal task priority applies
# and harvesting still outranks denial/advance whenever ore is actually
# available. The FIRST fixed attacker is unaffected — early scouting and
# pressure from exactly one builder is deliberate — but the second is now
# gated on this too, so the offensive budget grows only once there's a base
# worth defending.
#
# Tuning history — 33-map sweeps vs bots/friend, all with zero errors:
#   no gate -> besieges well, never builds an economy, loses on resources
#   gate 3  -> 25-8 (median Ti 2730) before counter-turret/base-repair
#              existed; 22-11 (2540) after adding them
#   gate 4  -> 22-11 (2410)
#   gate 5  -> 21-12 (2070), with base-repair mistakenly above harvest
#
# CAVEAT, and it matters: bot code calls random.* and --seed does NOT reseed
# it, so every sweep is a fresh sample. At 33 games and p≈0.7 the standard
# deviation is ~2.6 wins, so all the 21-25 results above sit within roughly
# one sigma of each other — a single sweep cannot distinguish them. Only the
# "no gate" failure is clearly outside the noise. Read these as "nothing
# here is obviously broken", NOT as a ranking, and re-run several sweeps
# before believing any 2-3 win difference.
OFFENSE_MIN_HARVESTERS = 3

# Titanium the core keeps OUT of ammo conversion so banking siege ammo can
# never starve harvester/conveyor construction. Ammo is converted 1:1, so
# without this the 150-ammo siege buffer is 150 Ti straight off the economy.
AMMO_ECONOMY_RESERVE = 100

# --- Lifetime ammo budget: TRIED AND NOT SHIPPED ---
# AMMO_ECONOMY_RESERVE above is a floor on the BALANCE, not a cap on total
# spend, and against a continuous drain a balance floor does nothing: the core
# tops the buffer back up every time a turret fires, income trickles back over
# the floor, and it converts again, forever.
#
# Measured on fjordgate (10x10, replays c774cbdb_game_1 and ea1582_game_3):
# the cores see each other by round ~6, so the "threat" branch is permanently
# live; three forward sentinels fired continuously; the core converted 31
# times for 461 titanium — 92% OF THAT GAME'S ENTIRE LIFETIME BUDGET — and we
# finished with zero harvesters, zero titanium mined, and a dead core. The
# sister game spent 68% the same way.
#
# A cumulative cap scaled by harvester count (40 + 40/harvester, and again at
# a much more generous 200 + 100/harvester) fixed that spending pattern and
# did NOT convert into wins — 69.7% with it versus 73.9% without, over 198 and
# 264 games respectively. Best current reading: the ammo was buying real
# damage even in the games we lost, and starving it just makes us lose more
# slowly. Left unimplemented deliberately; revisit with a cap keyed on
# something better than harvester count if the pattern shows up again.


# --- Core siege response (SLOT_CORE_SIEGE) ---
# Five straight losses to the top ladder team, every one of them by
# core_destroyed, with these numbers:
#
#   game   dmg to OUR core   we healed it   dmg to THEIR core   they healed it
#     1          504               0               504                504
#     2          962             450               234                232
#     3          936             432                90                 88
#     4          666             152               324                324
#     5          504               0               270                268
#
# They healed back 100% of everything we ever did to their core. We healed
# back 0% in two of the five. Healing is 4 HP per titanium and an enemy
# sentinel converts 10 of THEIR ammo into 18 damage every 2 rounds, so
# out-sustaining a besieging sentinel costs about 2.5 Ti/round — trivially
# affordable, and we simply never did it.
#
# The reason we never did it is a VISION mismatch, not a policy one.
# _heal_core (main.py) has always been able to heal, but only opportunistically
# — if a builder happened to already be standing next to the core. And
# TASK_HOME_THREAT is detected from the BUILDER's own vision (r^2=20), while
# the besieging sentinels in those games sat at dist_sq 25-32 from our core,
# outside it. The CORE sees r^2=36 and could see them the whole time; it just
# had nowhere to say so. SLOT_CORE_SIEGE is that channel.
#
# Note the geometry that makes answering a sentinel cheap: a sentinel CANNOT
# ROTATE, so its fire line is fixed for life. A builder approaching from off
# that line is never in danger (_danger_tiles already models the line exactly),
# and 15 rounds of builder-fire — 30 Ti — removes it permanently.
CORE_SIEGE_HP = 20             # missing core HP before the beacon lights up
CORE_SIEGE_CRISIS_HP = 150     # ...before even chaining builders abandon their work
CORE_SIEGE_RECALL_SQ = 400     # how far out (dist_sq) a builder answers the beacon
# Packing: value = missing_hp * SIEGE_HP_SHIFT + pack_pos(turret) (0 if none).
# pack_pos is ((x+1) << 16) | (y+1), so it needs 21 bits on the largest legal
# map (30x30 -> 2,031,647). Shifting by exactly 21 keeps the whole packed
# value under 2^31 for the maximum 500 missing HP, so the slot stays safe
# even if the engine stores it as a 32-bit signed integer.
SIEGE_HP_SHIFT = 1 << 21

# --- Sentinel pool ramp ---
# SENTINEL_POOL_TARGET (3) is what we want once there is an economy paying
# for it. Before that it is straightforwardly suicide: in the five losses
# above we planted 3-4 forward sentinels between rounds 4 and 36 — ~140 Ti of
# a 500 Ti opening — and in two of those games went on to collect ZERO
# titanium for the rest of the match. The winning bot planted exactly ONE
# early sentinel and spent everything else on harvesters (7-11 of them, to
# our 0-1).
#
# So the pool ramps rather than gating: the first sentinel is still built as
# early as ever, because the tuning history in this file is emphatic that
# heavy sentinel gates cost 13 points of win rate (see SENTINEL_SITE_BLACKLIST
# above) and early pressure is real. Only the first Sentinel is allowed before
# the larger five-chain economy is established; the existing second attacker
# remains on its proven schedule, isolating turret spend from delays to the
# combat workforce.
SENTINEL_POOL_TARGET_EARLY = 1

# A confirmed enemy Core may be ringed with a small barrier cage after the
# forward Sentinel opportunity has been handled. Sentinels shoot through
# barriers, while enemy Builders lose movement and repair access.
ENEMY_CORE_BARRIER_CAP = 6
# Once five routes and a recent income heartbeat prove that the economy is
# paying, the existing attacker can finish a deeper repair-denial cage. This
# is a phase transition, not a blind opening spend: crisis/quiet-income phases
# retain the smaller cap and route reserve.
SIEGE_BARRIER_CAP = 12

# --- Stage-2 spawn fallback ---
# REINFORCEMENT_BUILDER_TARGET unlocks on HARVESTER_MILESTONE completed
# chains, which deadlocks: the chains need titanium, the titanium needs
# builders, and a team that spent its opening elsewhere never reaches either.
# Measured in the five losses: 3 living builders for the whole game in three
# of them, against 5-12 for the opponent (who had five out by round 4).
#
# The fallback is a round number, not another economic condition, precisely
# so it cannot deadlock. It is safe because SPAWN_RESERVE still applies —
# this only ever fires with the titanium already banked — and because the
# early-overspend failure that motivated staging was about rounds 0-20, not
# round 24.
STAGE2_FALLBACK_ROUND = 20

# After five completed chains and a real bank, grow beyond the opening roster
# so independent routes can be extended and repaired concurrently.  The dual
# gate preserves the early cost-scale discipline.
ECONOMY_STRONG_CHAINS = 5
LATE_BUILDER_TARGET = 12

ORE_TURRET_MIN_ROUND = 40
ORE_TURRET_RESERVE = 120
ORE_TURRET_MAX_PER_BUILDER = 1

# Cap lifetime ammo conversion by observed income rather than current balance.
# A balance reserve cannot stop sentinels from continuously draining newly
# delivered titanium; this allowance grows only after income has been seen.
AMMO_LIFETIME_FRAC = 0.4
AMMO_LIFETIME_MIN = 175

# Builder fire is a last-resort, low-efficiency action.  It must leave enough
# titanium to continue route construction and recovery.
IDLE_ATTACK_RESERVE = 80

# A positive net-resource observation is the Core's only cheap team-wide
# delivery heartbeat. If it goes quiet for this many rounds, release the
# dynamic workforce back to route conversion even when the historical route
# counter is already high.
INCOME_HEARTBEAT_ROUNDS = 8


def pack_economy_cursor(phase: int, cursor: int) -> int:
    """Pack the Core phase and the delayed ore-ring cursor into slot 4."""
    return (phase << ECONOMY_PHASE_SHIFT) | (cursor & ORE_CURSOR_MASK)


def economy_phase_from_cursor(value: int) -> int:
    """Read the phase portion of the shared slot without touching its cursor."""
    return (value & ECONOMY_PHASE_MASK) >> ECONOMY_PHASE_SHIFT


def ore_cursor_from_packed(value: int) -> int:
    """Read the legacy ring cursor from the shared phase channel."""
    return value & ORE_CURSOR_MASK
