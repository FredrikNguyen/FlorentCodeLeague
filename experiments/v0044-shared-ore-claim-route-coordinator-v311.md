# v311 — shared ore-claim route coordinator

## Hypothesis

Top-team replays show multiple builders converting distinct routes in parallel,
while the v0044 candidate communicates only unowned ore positions.  A builder
that sees a remote source can therefore cause duplicate pursuits, leaving
other builders idle or delaying the first paying route.  Encoding a source,
builder id, and modulo-32 heartbeat in the existing four-slot ore ring should
make route ownership explicit without adding Store slots or changing combat
policy.

## Scope

The candidate adds a marked ore-claim codec, compatibility decoding for the
legacy position format, and a short lease lifecycle.  Defender/dynamic
builders publish claims only for sources currently inside their harvest range;
attackers publish unowned hints.  Owners refresh every few rounds, foreign
fresh claims are skipped, and stale entries can be replaced.  The existing
local nearest-builder tie-break, chain FSM, economy phases, and action gates
remain unchanged.

Changed production files:

- `bots/candidate/bot/util.py`
- `bots/candidate/bot/defender.py`
- `bots/candidate/bot/dynamic.py`
- `bots/candidate/main.py`

Focused coverage is in `tests/test_candidate_economy_phase.py`.

## Non-goals

No Store schema expansion, map-specific branch, unit-cost/spawn/combat change,
route geometry rewrite, baseline/archive edit, packaging, upload, activation,
or live-state mutation.

## Verification record and result

- Initial focused tests: 37/37 passed (`reports/v311-focused-tests.log`),
  compileall passed, static recorded the inherited profile, and smoke was 4/4
  (`reports/local-20260819T232622Z`).
- Initial rotated screen: 4–11, command-clean, with several losses converting
  only 3–5 Harvesters (`reports/local-20260819T232848Z`).
- One bounded repair restricted ownership to an active economy task, released
  claims on task exit, and favored the owner's current target. It passed 38/38
  focused tests, compileall, static's inherited profile, and smoke 4/4.
- Repair screen: 5–10, command-clean but with two candidate no-delivery rows
  (`reports/local-20260819T233334Z`). No long gate or promotion was justified.
- Rollback: all claim production/test edits removed; recursive source parity
  with immutable v0044 is empty (`reports/v311-rollback-source-parity.diff`,
  `reports/v311-rollback-main-parity.diff`). Rollback focused coverage is
  34/34, compileall passed, static retained the inherited profile, and smoke
  was 4/4 (`reports/local-20260819T233736Z`).
