# v153 low-liquidity economy recovery

## Objective

Keep a Dynamic Builder in the economy/exploration loop after three completed
routes when the current titanium bank cannot fund one replacement Harvester and
two short Conveyor links. The goal is to avoid workforce starvation on long
maps while preserving pressure when the bank is healthy.

## Comparator and scope

- Comparator: immutable `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Candidate scope: `bots/candidate/bot/constants.py`,
  `bots/candidate/bot/dynamic.py`, and focused nearest-defense tests.
- Non-goals: navigation, fixed roles, Store protocol, route FSM, caps, maps,
  baseline archives, and platform state.

## Validation

- Focused candidate suite before the screen: 22/22.
- Compileall: pass.
- `make static`: known inherited failure (15 obsolete imports and two
  navigation fast-path assertions), report `reports/iter-v153-low-liquidity/static.log`.
- Smoke: 4/4 command-clean, report `reports/local-20260817T214043Z`.
- New evaluation policy validation: schedule tests 5/5,
  `reports/iter-v153-low-liquidity/release-matrix-policy.log`.
- Fast all-map screen: **16-20** candidate wins, zero ties, zero command
  failures/TLE/suspicious output, zero no-delivery rows for both sides,
  candidate collection 142,340 versus 173,660, max p99 1,469 us, peak 3,064
  us. Reports `reports/local-20260817T214644Z` and
  `reports/iter-v153-low-liquidity/screen36-analysis.json`.

### Bounded repair 1

Reduced the low-liquidity reserve from one Harvester plus two Conveyor links
to one Harvester plus one link, allowing pressure to resume sooner when the
bank is tight but not critically empty. Focused tests remained **22/22**,
compileall passed, static retained the same inherited failures, and smoke was
**4/4** (`reports/local-20260817T215251Z`). The second 36-game screen improved
to **19-17**, with candidate collection **205,020** versus **188,060**;
zero candidate no-delivery rows versus two for the comparator, zero command
failures/TLE/suspicious output, max p99 **1,441 us**, peak **5,708 us**.
Report: `reports/local-20260817T215314Z`, analysis
`reports/iter-v153-low-liquidity/repair1-screen36-analysis.json`.

Repair 1 is a positive but narrow edge, not sufficient by itself for the
90-game gate. One bounded repair remains: prevent the low-bank exploration
handoff after a confirmed enemy-Core sighting, when the team has actionable
offensive work.

### Bounded repair 2 and final decision

After a confirmed enemy-Core sighting, bypassed the low-liquidity exploration
handoff so Dynamic workers could keep pressure. Focused tests were **23/23**,
compileall passed, static retained the same inherited failures, and smoke was
**4/4** (`reports/local-20260817T215832Z`). The final 36-game screen remained
**19-17**, with candidate collection **181,490** versus **167,360** and one
candidate no-delivery row versus zero for the comparator; runtime was clean
(max p99 **1,541 us**, peak **2,745 us**). Report:
`reports/local-20260817T215858Z`, analysis
`reports/iter-v153-low-liquidity/repair2-screen36-analysis.json`.

The second repair did not improve paired wins over repair 1 and introduced a
delivery regression. After the two allowed repairs, v153 is rejected and the
candidate source is restored byte-identically to v0040 (verified by recursive
source diff). Rollback focused tests were **20/20**, compileall passed, and
rollback smoke was **4/4** (`reports/local-20260817T220345Z`). No 90-game gate,
archive, package, upload, activation, or baseline transition occurred.

## Decision

The initial v153 guard is rejected at the 36-game screen: it lost aggregate
win rate and 18% of collection despite clean delivery and runtime. Do not run
the 90-game gate until a bounded repair produces a material screen edge.
Preserve the v0040 archive as the moving baseline. At most two repairs are
allowed before restoring the candidate to v0040 and choosing a new hypothesis.

## Evaluation policy

Routine release validation is 90 games: all 15 configured maps, seeds 1/43/101,
and both side orders. The fast checkpoint is 36 games: an 18-pair deterministic
stratified schedule with every map represented and both side orders.
