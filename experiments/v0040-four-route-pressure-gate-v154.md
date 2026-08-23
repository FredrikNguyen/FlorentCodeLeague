# v154 four-route pressure gate

## Objective

Require four completed Harvester routes before the scalable Dynamic workforce,
second permanent attacker, and forward Sentinel pressure are unlocked. The
first fixed attacker remains the early scout/pressure floor, while additional
workers keep building and repairing paths until the fourth route is proven.

## Comparator and scope

- Comparator: immutable `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Candidate scope: `bots/candidate/bot/constants.py` and focused gate tests.
- Non-goals: route geometry, navigation, fixed first-attacker behavior, Store
  protocol, defensive turret logic, baseline archives, and platform state.

## Done criteria

- Focused gate tests cover route counts 0–4 and second-attacker timing.
- Compileall and smoke are clean; static has no new failures.
- The 36-game all-map screen improves aggregate paired win rate over v0040
  without a delivery or reliability collapse.
- Only if the screen edge is material, run the 90-game release matrix.

## Initial screen

- Focused tests: **20/20**; compileall passed; smoke **4/4**; static retained
  the known inherited 15 obsolete-import errors and two navigation assertions.
- 36-game all-map screen: **18-18**, zero ties, candidate collection
  **158,070** versus **154,300**, candidate no-delivery **2** versus baseline
  **1**, zero command failures/TLE/suspicious output, max p99 **1,460 us**,
  peak **2,735 us**. Report `reports/local-20260817T220758Z`, analysis
  `reports/v154-screen36-analysis.json`.
- Decision: no release gate. One bounded repair will separate the Dynamic gate
  from the fixed attacker/Sentinel three-route timing.

## Repair 1 screen

Restored `OFFENSE_MIN_HARVESTERS = 3` for the fixed attacker/Sentinel shell and
introduced `DYNAMIC_OFFENSE_MIN_HARVESTERS = 4` for Dynamic task selection and
offense. Focused tests: **20/20**; compileall passed; smoke **4/4**; static
retained the inherited failures. The 36-game screen improved to **21-15**,
with candidate collection **178,200** versus **166,600**, zero no-delivery rows
for both sides, zero command failures/TLE/suspicious output, max p99
**1,357 us**, peak **5,538 us**. Report `reports/local-20260817T221347Z`,
analysis `reports/v154-repair1-screen36-analysis.json`.

The +6 paired-win edge is material enough for the 90-game release gate. Map
risks to retain in the gate review: Antler, Auroraveil, Fjordgate, and Royale
were 0-2; the aggregate gate remains primary with delivery/reliability vetoes.

## 90-game release gate and decision

The reduced release matrix covered all 15 maps, seeds 1/43/101, and both side
orders: **90/90 command-clean**. Repair 1 scored **42-48** against v0040,
with candidate collection **390,960** versus **428,030**, candidate
no-delivery **0** versus **1**, zero TLE/suspicious output, max p99
**1,460 us**, and peak **5,724 us**. Report `reports/local-20260817T221821Z`,
analysis `reports/v154-release90-analysis.json`.

The screen edge did not transfer to the release distribution, so v154 is
rejected and not archived or submitted. Candidate source was restored
byte-identically to v0040 and verified by recursive source diff. Rollback
focused tests were **20/20**, compileall passed, and rollback smoke was **4/4**
(`reports/local-20260817T222825Z`). Choose a new hypothesis; do not promote or
run platform operations for v154.
