# v359 — healthy-pressure workforce handoff

## Objective and replay basis

Keep immutable v0046 as the comparator.  Fresh v108 metadata and the replay
sample in `reports/live-v108-followup-20260820T164909Z/` show both underbuilt
openings (one or two Harvesters, no delivery) and over-converted long games
(20+ Harvesters and hundreds of Conveyors with too little combat).  The Core's
existing delayed economy phase provides a shared lifecycle signal without a
new Store slot.

## Hypothesis and scope

When the Core publishes healthy `PRESSURE`—five completed routes plus a recent
positive-income heartbeat—dynamic Builders should stop treating every visible
ore tile as a new route mission.  They should instead flow through the existing
raid, home-defense, repair, denial, and advance priorities.  `OPENING`,
`CONVERTING`, and `CRISIS` remain economy-first, and the existing liquidity
floor can still retain one local route-recovery owner.

Allowed production/test scope is `bots/candidate/bot/dynamic.py` and
`tests/test_candidate_economy_phase.py`; immutable v0046, Store layout, Core
spawning, route geometry, fixed attackers, and platform state are unchanged.

## Implementation

The final branch of `_should_harvest` now returns false in
`ECONOMY_PHASE_PRESSURE` after the existing offense and low-liquidity gates.
The phase's delayed income heartbeat therefore becomes a real handoff instead
of a signal that still admits arbitrary visible ore.  A focused test proves
that visible ore is rejected in pressure and accepted again in converting.

## Validation

- Focused coverage was **32/32** before the one repair and **33/33** after;
  compileall passed throughout.  Rollback coverage was **31/31**.
- The initial v0046-pinned rotated screen at
  `reports/local-20260820T165529Z` was **6-9** candidate-A.  It was
  command/TLE/suspicious/delivery-clean.
- The one focused repair preserved the Core-designated defender inside the
  pressure handoff.  Its rotated screen at
  `reports/local-20260820T165810Z` was **8-7**, also reliability-clean.  The
  combined pair was **14-16**, below the required **19-11**.
- Post-rollback `make smoke` was **4/4 command-clean** at
  `reports/local-20260820T170039Z`.  `make static` remains the inherited exit
  2 with 15 obsolete imports and two navigation assertions; its log is
  `reports/iter-v359-healthy-pressure-handoff-v359/rollback-static.log`.

## Decision and rollback

Reject v359 after the single bounded repair.  The pressure handoff reduced
some route over-conversion but did not produce a repeatable win-rate edge and
underbuilt the combat shell on several maps.  No 60-game release matrix,
remote gate, package, upload, activation, or baseline update ran.

Candidate production source was restored exactly to immutable v0046; the
recursive source parity proof is the empty
`reports/iter-v359-healthy-pressure-handoff-v359/rollback-source-parity.diff`.
The v0046 comparator remains the baseline for the next hypothesis.
