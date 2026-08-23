# v201 — primary-attacker opening economy handoff

## Replay basis and objective

The v200 relay replay showed a causal opening trade: its primary attacker built
three Launchers and first delivery averaged about round 33, while high-ranking
winners paired early delivery (about round 21) with a route/Barrier shell before
mobility. v201 temporarily lent only the designated primary attacker to the
normal economic Builder FSM, then returned it to offense after a completed
Harvester route or a bounded map-scaled deadline. Active chains were allowed to
finish. No other role or combat selector changed.

## Scope

- Temporary source: `bots/candidate/main.py` and one opening-phase constant in
  `bots/candidate/bot/constants.py`.
- Temporary focused coverage: `tests/test_candidate_primary_opening.py`.
- Regression screen: all 15 maps with `configs/eval_regression.toml` rotated
  from seed 165 to seed 166.
- No Launcher, hijack, sabotage, route-geometry, turret, ammo, baseline,
  package, upload, activation, or live-state change.

## Validation and replay evidence

- Initial phase-target-one implementation passed focused **4/4**, compileall,
  static with only inherited failures, and smoke **4/4**. A diagnostic repeat
  on the old seed 165 scored **7-8**, with first delivery **21.36** for the
  candidate versus **47.27** for the paired side; this was not used as the
  rotated decision because the config had not yet moved off seed 165. Report:
  `reports/local-20260818T131711Z` and analysis
  `reports/iter-v201-primary-opening-replay-analysis.json`.
- The planned seed-166 screen scored **5-10**, 15/15 command-clean, with zero
  TLE/suspicious/no-delivery rows. Candidate first delivery was **40.27**
  versus **27.73** for v0042; max p99/peak were **1,521/2,822 us**. Royale
  placed its first Harvester at round **248** and delivered at **324**. Report:
  `reports/local-20260818T132001Z` and analysis
  `reports/iter-v201-primary-opening-replay-analysis-seed166.json`.
- One bounded repair kept the primary in the economy phase until two completed
  routes. Focused/compileall/static/smoke stayed clean; seed 166 improved to
  **6-9**, first delivery **26.93** versus **28.13**, but still trailed in
  Harvester/Barrier stock and failed the paired win gate. Max p99/peak were
  **1,514/4,648 us**. Report:
  `reports/local-20260818T132318Z` and analysis
  `reports/iter-v201-primary-opening-replay-analysis-repair-seed166.json`.

## Decision and rollback

Reject v201 after the permitted repair. The handoff improved delivery in the
repair but did not convert it into a paired win-rate edge; its losses still
showed fewer Barriers/Harvesters and one severe late/no-delivery Royale row.
Temporary source and focused tests were removed. Candidate Python is
recursively byte-identical to immutable v0042; rollback nearest-defense was
**23/23**, compileall passed, static retained the inherited exit 2, and rollback
smoke was **4/4** at `reports/local-20260818T132539Z`. No release gate, package,
upload, activation, or baseline transition occurred.

## Next replay question

The next hypothesis must address why the workforce still under-builds Barriers
and additional Harvesters after a fast first delivery, and why Royale can defer
its first route to round 248. Do not retry the same primary-attacker handoff or
standalone Launcher relay without a new causal map-state mechanism.
