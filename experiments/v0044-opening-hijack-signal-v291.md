# v291 opening hijack signal gate — rejected

Date: 2026-08-19

## Hypothesis

On the first route, refusing a visible hostile Harvester with no carried stack
and no valid hostile accepting outlet would keep a route worker from chasing a
dead source.  A loaded source or a source with a same-team accepting
Conveyor/Splitter would remain eligible.  After one own route, existing
takeover behavior would remain unchanged.

## Scope

- Candidate: `bots/candidate/bot/defender.py`
- Focused coverage: `tests/test_candidate_nearest_defense.py`
- Comparator: `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`
- No baseline/archive, platform, or live-state mutation.

## Validation

- Focused candidate tests: **38/38 pass**.
- Candidate compileall: pass.
- `make static`: exit **2**, inherited 15 obsolete-module import errors and
  two navigation fast-path assertions.
- `make smoke`: **4/4 command-clean**.
- 15-map screen: `reports/local-20260819T165550Z`; command-clean, all rows
  delivered, zero TLEs and suspicious rows; candidate-A **7-8**.
- Screen totals: candidate-A/B **52,220/57,840 Ti**; maximum p99/peak
  **1,417/4,533 us**.
- Comparator reference: `reports/local-20260819T163848Z`; candidate-A/B
  **7-8**, **47,370/60,630 Ti**.

## Decision

Reject.  The gate changed map outcomes and shifted resources but did not
increase aggregate win rate or establish a repeatable protected-map edge.
The temporary predicate and tests were removed without repair.

## Rollback evidence

- Focused rollback tests: **34/34 pass**.
- Rollback compileall: pass.
- Rollback `make static`: inherited exit **2**.
- Rollback `make smoke`: **4/4 command-clean**; report
  `reports/local-20260819T165857Z`.
- Recursive production-source parity against v0044: zero diff;
  `reports/iter-v291-opening-hijack-signal/parity-after.diff`.
- Live state unchanged: v107 active-observing; v105 remains rollback target.

Reports: `reports/iter-v291-opening-hijack-signal/`.
