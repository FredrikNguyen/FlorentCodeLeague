# v279 visible claimed-ore target handoff — rejected after one repair

Date: 2026-08-19

## Objective and scope

The v278 replay family exposed a route-conversion gap: the candidate placed
only 92 Harvesters versus 150 for the comparator on seed 172.  The baseline
SCOUT loop can remember an ore target, have another Builder occupy it with a
Harvester, and then keep stopping one tile away because the environment still
reports ore.  v279 tested immediate target reselection for that visible stale
claim.  The initial implementation invalidated any occupied visible ore; the
one bounded repair restricted it to a visible friendly Harvester.  Only
`bots/candidate/bot/defender.py` and focused nearest-defense tests changed.

## Evidence

- Initial focused coverage was **33/33**, compileall passed, `make static`
  retained inherited exit 2, and smoke was **4/4**.  Seed 172 report
  `reports/local-20260819T134640Z` was **5-10**, collection
  **62,810/98,080 Ti**, delivery **15/15 vs 15/15**, and placed
  **105/129 Harvesters**.  It was command- and reliability-clean with zero
  TLE/suspicious rows, but the negative screen justified the bounded repair.
- The repair focused suite remained **33/33**, compileall passed, static kept
  the inherited failures, and smoke remained **4/4**.  Seed 172 report
  `reports/local-20260819T134902Z` was **4-11**, collection
  **64,120/64,410 Ti**, delivery **15/15 vs 15/15**, and Harvesters
  **109/126**, with zero TLE/suspicious rows.
- Repair seed 175 report `reports/local-20260819T135031Z` was **5-10**,
  collection **55,270/89,020 Ti**, delivery **15/15 vs 15/15**, and
  Harvesters **109/115**, with zero TLE/suspicious rows.  The repaired pair
  was **9-21** and **119,390/153,430 Ti**, so the target handoff is rejected.

## Rollback and risks

The candidate source was restored recursively byte-identically to immutable
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`;
`reports/iter-v279-claimed-ore-handoff/rollback-source-parity.diff` is zero
bytes.  Rollback focused coverage was **31/31**, compileall passed, smoke was
**4/4**, and static retained exit 2.  No release gate, promotion, package,
upload, activation, or live transition occurred.  The stale-target behavior is
mechanically plausible but not a transferable win hypothesis; do not re-add it
without event-level replay evidence.  v0044 remains the local baseline. v105
remains the requested historical rollback reference only; v101 remains the
guarded operational fallback because v105's recorded result is 142/275
(51.64%).
