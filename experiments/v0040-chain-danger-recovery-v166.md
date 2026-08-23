# v0040 chain danger recovery — v166

Date: 2026-08-18

## Objective

Reduce late or missing first deliveries on compact and blocked maps. The v165
release replay audit showed candidate first-delivery turns of **126/152** on
Royale, **62/89** on Auroraveil/Glacierkeep, and a candidate-side no-delivery
loss on the same failure cluster. The current chain FSM gives up after
conservative enemy turret-line avoidance returns no step for 20 rounds, even
when the Builder is not currently standing in the line and an emergency
crossing could finish a paying route.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/main.py`, `bots/candidate/bot/defender.py`, and
  `bots/candidate/bot/constants.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No Builder role/spawn policy, ore target ranking, chain geometry/slack,
combat target selection, ammo, Store layout, map-specific branch, baseline or
archive, package, upload, activation, or live-state change.

## Hypothesis and implementation

After four consecutive no-progress chain turns, make exactly one emergency
navigation attempt toward the Core without the visible turret-line avoidance
set. The normal safe path remains preferred before and after that attempt; a
successful move resets the stall counter, while a failed attempt does not
repeat until a later stalled episode. This keeps the route FSM and verified
Core sink unchanged while giving an otherwise stalled paying route a chance to
cross a dangerous tile and complete.

## Done criteria

- Focused coverage proves the emergency bypass occurs only at the four-stall
  boundary and normal chain navigation still receives the danger set before
  and after it; existing role/route tests remain green.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The shortened 24-game all-map screen materially improves aggregate paired
  win rate over v0040, without systematic TLE/suspicious output or candidate
  delivery collapse. Only a qualifying screen advances to the 60-game gate.
- A failed screen or release requires exact v0040 rollback and no platform
  operation. Remote comparison is attempted only after a qualifying release.

## Validation and decision

Pending. Record the focused checks, screen/release replay delivery metrics,
rollback or promotion, and any remaining route-risk evidence here.

The initial four-stall variant passed focused checks **27/27**, compileall,
static with only inherited failures, and command-clean smoke. Its shortened
24-game screen tied v0040 **12-12** with zero candidate no-delivery games and
zero TLE/suspicious-output rows; candidate mean first delivery improved to
**24.1** turns versus the comparator's **29.0**
(`reports/local-20260818T015936Z` and
`reports/iter-v166-chain-danger-recovery-screen-replay-analysis.json`). The
tie does not qualify for release. Bounded repair 1 lowers the emergency
boundary to two stalled turns to test whether the route opportunity is being
missed before the previous threshold.

Repair 1 passed focused checks **27/27**, compileall, static with only the
inherited failures, and command-clean smoke
(`reports/local-20260818T020255Z`). The 24-game screen scored **13-11** with
zero candidate no-delivery games, zero TLE/suspicious-output rows, and mean
candidate first delivery **30.8** turns versus **29.5** for v0040
(`reports/local-20260818T020318Z` and
`reports/iter-v166-chain-danger-recovery-repair1-screen-replay-analysis.json`).
It is rejected without a release gate.

The emergency crossing and threshold were rolled back to exact recursive v0040
parity (**0 diff lines**;
`reports/iter-v166-chain-danger-recovery-rollback-source-diff.txt`). Rollback
focused checks passed **26/26**, compileall passed, and rollback smoke was
**4/4** (`reports/local-20260818T020635Z`). No package, remote match, upload,
activation, or baseline transition occurred. The next experiment must target a
different route or combat failure mode rather than danger-bypass timing.
