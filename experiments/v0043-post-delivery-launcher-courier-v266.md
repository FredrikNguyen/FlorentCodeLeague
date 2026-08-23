# v266 post-delivery Launcher courier — rejected

## Objective

Top-team replays showed more Launchers on winning sides, so v266 tested a
bounded, post-delivery use of the designated second attacker as a mobility
courier. The primary attacker, opening economy, route policy, and combat shell
were unchanged. The courier could build at most three dynamically priced
Launchers only after three completed routes, confirmed enemy-Core intel, and a
live forward Sentinel; a Launcher could throw only that friendly courier to a
passable tile that strictly reduced squared distance to the confirmed Core.

## Validation

- Focused implementation coverage: **31/31**;
  `reports/local-20260819T093340Z` (the focused command was rerun directly and
  passed; the make-static run also recorded all 31 candidate tests passing).
- Candidate compileall passed before rollback. `make static` retained the
  inherited 15 obsolete-module import errors and two navigation fast-path
  assertions. `make smoke` was **4/4** command-clean at
  `reports/local-20260819T093340Z`.
- Rotated 15-map screen against exact v0043 was command-clean with zero TLE or
  suspicious rows, but the candidate won **7-8** and collected **55,290 vs
  67,200 Ti**. Only four candidate Launchers were built (three on Drakkarfjord,
  one on Valkyrie); there was no repeatable pressure or collection edge.
  Raw report: `reports/local-20260819T093411Z`; replay diagnostics were
  generated in `/tmp/v266-analyze.json` during review.

## Decision and rollback

The screen failed the plan's repeatable-edge criterion, so v266 is rejected
without a longer gate, package, upload, activation, or live operation. The
temporary Launcher state, dispatch, policy, constant, and tests were removed;
focused rollback was **26/26** and candidate compileall passed. The next
working tree check must confirm recursive source parity with exact v0043 before
the next hypothesis.

## Risk and follow-up

Launcher correlation in top-team replays is not causal evidence for this
uncoordinated courier: the phase gates rarely activated and the four relays did
not improve outcomes. Generic infiltration remains unproven; any next
anti-infiltration or takeover experiment must first identify a replay with a
causal enemy-Builder event and isolate one response.
