# v341 — local route-frontier reacquisition

Date: 2026-08-20

## Hypothesis and scope

Top-team opening replays showed that a Builder which loses its pending
conveyor tile can leave a Harvester with a dead trail while the rest of the
workforce keeps scouting.  v341 tested a local Builder-FSM frontier lease:
when danger or a Launcher displacement made the pending tile non-adjacent,
the same Builder briefly navigated back to that exact tile instead of
discarding it.  The final repair made that lease strictly local: a frontier
more than two cardinal steps away was released immediately while retaining
CHAIN mode for a fresh local replan.

Allowed production scope was `bots/candidate/bot/defender.py`, with focused
coverage in `tests/test_candidate_nearest_defense.py`.  No Store schema,
opening spend, fixed roles, combat policy, route geometry, baseline snapshot,
package, platform, or live-state change was allowed to remain.

## Validation

- Initial focused coverage was **37/37**; repair 1 was **37/37**; repair 2 was
  **38/38**.  Compileall passed after each version.
- Initial 15-map screen was **8-7 candidate-A**, but AuroraVeil and Valkyrie
  had no candidate delivery.  Candidate collection was **88,510 vs 88,280
  Ti**.  Report: `reports/iter-route-frontier-v341-screen-analysis.json`.
- Repair 1 restored delivery on all 15 maps and collected **62,720 vs 58,380
  Ti** at **8-7 candidate-A**.  Report:
  `reports/iter-route-frontier-v341-repair1-screen-analysis.json`.
- A rotated repair-1 screen was also delivery-clean at **7-8 candidate-A**,
  with **68,660 vs 66,100 Ti**, zero TLE/suspicious rows, and max
  p99/peak **1,323/2,462 us**.  Report:
  `reports/iter-route-frontier-v341-rotated-screen-analysis.json`.
- The 60-game endpoint/side gate was command-clean but rejected at **25-35**
  candidate wins and **274,330 vs 296,920 Ti**.  Candidate delivered all 60;
  the baseline failed to deliver on three Glacierkeep/Valkyrie rows.  Max
  p99/peak was **1,425/4,775 us**, with zero TLE/suspicious rows.  Report:
  `reports/iter-route-frontier-v341-release-analysis.json`.
- Repair 2's final 15-map screen was delivery-clean but regressed to **6-9**
  and **61,730 vs 72,740 Ti**, with max p99/peak **1,280/3,947 us**.  Report:
  `reports/iter-route-frontier-v341-repair2-screen-analysis.json`.
- Rollback focused coverage was **35/35**, compileall passed, `make static`
  retained the inherited repository profile (15 obsolete-module imports and
  two navigation assertions), and rollback smoke was **4/4** at
  `reports/local-20260820T080712Z`.

## Decision and rollback

Reject v341 after the two permitted bounded repairs.  Neither local
reacquisition policy produced a repeatable win-rate edge, and the release
gate lost both wins and aggregate collection despite candidate-side delivery
being reliable.  Restore exact recursive production parity with immutable
v0046; proof is
`reports/iter-route-frontier-v341-rollback-source-parity.diff`.
No promotion, package, upload, activation, or live transition occurred; live
state remains v108 `active_observing` with v107 known-good.

## Follow-up

Do not revisit pending-tile reacquisition as a standalone improvement.  The
loss concentration is opening conversion, especially Fjordgate/Nordkap rows
that reach one or zero Harvesters before pressure begins.  The next
fundamental experiment should coordinate a map-aware opening workforce and
route budget from visible ore/path evidence, then release workers into
defense or offense only after the economy has a verified four-route floor.
