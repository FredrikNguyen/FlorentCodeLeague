# v362 compact post-delivery loaded-raid handoff

## Objective and replay basis

Keep immutable v0046 as the only comparator and address the fresh v108
conversion losses without retrying the rejected whole-workforce pressure
handoff.  The latest live sample at
`reports/live-v108-replays-20260820T172904Z/` shows 0-5 to Atlas v86 and 1-4
to CtrlAltDefeat v132 while the bot keeps many Harvesters/Conveyors and leaves
loaded enemy logistics largely untouched.  The v0046 baseline also loses its
compact Royale/Drakkarfjord/Icefloe samples through the same resource-to-
pressure gap.

## Hypothesis and scope

During the Core's delayed `CONVERTING` phase, after three completed routes and
only on a compact map, let the existing nearest-responder selector give one
dynamic Builder priority to a visible loaded enemy Harvester/Conveyor/Splitter
raid before the normal harvest task.  The target still requires the existing
first-Sentinel/funding gates and disappears if no loaded logistics is visible;
all other dynamic Builders, route geometry, fixed attackers, and defense stay
unchanged.

Allowed production/test scope is `bots/candidate/bot/dynamic.py` and
`tests/test_candidate_economy_phase.py`.  Documentation, durable state, and
read-only live/replay reports are also recorded.  No Store schema, Core spawn
target, sentinel pool, barrier cap, navigation, baseline snapshot, package,
upload, activation, or live-state transition is part of v362.

## Validation

Focused coverage was **33/33** before and after the one reserve repair;
compileall passed, `make smoke` was **4/4**, and `make static` retained only
the inherited 15 obsolete imports plus two navigation assertions.  The seed
233 screen was **10-5**, 15/15 deliveries, and reliability-clean.  The seed
239 screen was **9-6** and reliability-clean but delivered on only 14/15
maps: Royale seed 43 ended at zero candidate titanium.  Although the combined
score was exactly **19-11**, the hard delivery gate failed.

The candidate source was restored to exact v0046 parity after the one allowed
repair.  No release matrix, remote gate, package, upload, activation, or
baseline update ran.

## Decision

**Rejected.** The reserve guard improved the first screen, but the rotated
second screen exposed a no-delivery opening.  Keep immutable v0046 as the
baseline and use the saved replay evidence to design the next bounded
hypothesis; do not retry this handoff unchanged.
