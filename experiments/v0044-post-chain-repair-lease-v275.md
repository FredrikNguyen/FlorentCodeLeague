# v275 post-chain visible repair lease — rejected after one repair

Date: 2026-08-19

## Hypothesis and scope

The v274 replay audit showed routes that finished geometrically and later lost
visible Conveyor links while their former chain owner immediately resumed
scouting. v275 gave a successful chain owner a bounded local repair lease. The
existing Harvester milestone was published immediately; the lease only used
the existing visible gap classifier and cardinal navigator. No Store schema,
route search rewrite, combat policy, or platform operation was included.

## Initial candidate and release gate

Focused coverage passed **34/34**, compileall passed, smoke **4/4**, and static
retained the inherited failures. Both rotated screens against exact v0044 were
command-clean with zero TLE/suspicious rows:

| screen | candidate wins | collection Ti | first delivery |
| --- | ---: | ---: | ---: |
| seed 172 | 7-8 | 73,120 vs 77,010 | 15/15 vs 15/15 |
| seed 175 | 9-6 | 78,610 vs 68,160 | 14/15 vs 15/15 |

The pair was **16-14** with a **+6,560 Ti** candidate collection edge, so the
60-game release gate ran. It was command-clean but finished **28-32**,
collection **242,800 vs 257,220 Ti**, first delivery **58/60 vs 59/60**, and
zero TLE/suspicious rows (max p99/peak **1,396/2,602 us**). Map results were
especially weak on Drakkarfjord (**1-3**), Fjordgate (**1-3**), Icefloe
(**1-3**), Ragnarok (**1-3**), Royale (**1-3**), and Valkyrie (**1-3**).
No promotion or package/upload/activation was justified.

## One bounded repair

The repair shortened the lease from 12 to 6 rounds to limit diversion from
ordinary defense and offense. Focused coverage remained **34/34**, compileall
passed, smoke **4/4**, and static retained the inherited failures. The repair
seed-172 screen was **8-7**, **53,710 vs 48,550 Ti**, delivery **14/15 vs
15/15**; the independent seed-175 screen was **7-8**, **69,500 vs 75,780 Ti**,
delivery **15/15 vs 15/15**. The repaired pair was **15-15** with collection
**123,210 vs 124,330 Ti**, so the one-repair policy stopped the iteration.

The candidate source was restored recursively to exact v0044 parity; the
rollback source diff has zero lines. Rollback focused coverage passed **31/31**,
compileall passed, smoke **4/4**, and static retained exit 2. Evidence is in
`reports/iter-v275-post-chain-repair-lease/` and these matrices:

- `reports/local-20260819T123129Z` (initial seed 172)
- `reports/local-20260819T123337Z` (initial seed 175)
- `reports/local-20260819T123550Z` (60-game gate)
- `reports/local-20260819T124244Z` (repair seed 172)
- `reports/local-20260819T124458Z` (repair seed 175)
- `reports/local-20260819T124808Z` (rollback smoke)

v0044 remains the moving local baseline. v107 remains active-observing;
v101 remains the guarded operational rollback because the requested v105
historical reference is known bad at 142/275 (51.64%). The lease did not
reliably improve map floors; the next experiment should target a different
route-health signal rather than lengthen this lease.
