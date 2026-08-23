# v199 — short-lived Sentinel liquidity circuit breaker

## Objective

Protect route liquidity after repeated, confirmed forward-Sentinel deaths. The
candidate temporarily blocked another Sentinel only after one attacker observed
two Sentinels die before `SENTINEL_MIN_LIFETIME`, and only while dynamic prices
could not fund a Harvester, two Conveyor links, and the replacement Sentinel.

## Scope and non-goals

- Temporary source: `bots/candidate/main.py`,
  `bots/candidate/bot/attacker.py`, and `bots/candidate/bot/constants.py`.
- Temporary focused coverage: `tests/test_candidate_sentinel_liquidity.py`.
- No Launcher, route/ore, dynamic-task, barrier, hijack, sabotage, ammo,
  baseline, package, upload, activation, or live-state changes.

## Validation

- Focused coverage was **25/25**; the dynamic-price low-bank and recovered-bank
  gates were both exercised. Compileall passed. `make static` retained only
  the inherited 15 obsolete-import errors and two navigation assertions.
- Smoke was **4/4** command-clean at
  `reports/local-20260818T124013Z`; replay analysis is in
  `reports/iter-v199-sentinel-liquidity-smoke-analysis.json`.
- The rotated 15-map screen at seed 164 was **6-9** against exact v0042,
  15/15 command-clean, with zero TLE or suspicious-output rows, no
  no-delivery rows, and max p99/peak **1,559/4,175 us**. Replay analysis:
  `reports/iter-v199-sentinel-liquidity-replay-analysis.json` and report
  `reports/local-20260818T124056Z`.
- Replay review found the expected liquidity symptom remained: candidate
  losses averaged fewer Harvesters/Barriers than v0042 and the candidate had
  no Launchers, while high-ranking winners repeatedly built early Launchers
  (rounds 1, 3, 5) and offensive Barriers before later Sentinel pressure.

## Decision and rollback

Reject v199 without a release gate. The 6-9 screen is a direct regression and
does not justify another reserve repair. The temporary constant, counter, gate,
and focused test were removed. Candidate Python is recursively byte-identical
to immutable v0042; rollback nearest-defense coverage was **23/23**, compileall
passed, and rollback smoke was **4/4** at
`reports/local-20260818T124900Z`. No package, upload, activation, or baseline
transition occurred.

## Replay-backed follow-up

The next bounded hypothesis should address the missing early unit-control
phase, not widen the rejected late ejection or Sentinel reserve: test a small,
reserve-gated Launcher relay for the designated primary attacker, with legal
passable destinations and a strict unit/route reserve. Keep it isolated from
ore selection, hijacking, and barrier-cap changes, and compare its actual
Launcher/launch events against the top-team pattern before deciding promotion.
