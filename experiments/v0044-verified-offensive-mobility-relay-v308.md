# v308 — verified offensive mobility relay

## Objective and evidence

v107 live losses and the saved top-team audit expose a structural omission:
the candidate dispatches no `EntityType.LAUNCHER`, while winner replays place
Launchers in 8/15 games and the Yulerune loss ended with one candidate
Harvester/no delivery against an opponent with two Launchers.  Test whether a
single verified mobility relay lets the permanent offensive Builder cross the
front faster without stealing the route workforce.

## Allowed files and non-goals

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py` only for named relay limits
- one focused `tests/test_candidate_launcher_relay.py`
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, durable state, and reports

No baseline/archive, Store schema, Core economy/spawn, route FSM, dynamic task
selector, Sentinel/Gunner/Barrier policy, package, upload, activation, or
live-state change is allowed.  The Launcher may only act after its legality
gate and may only choose strict-progress visible passable destinations.

## Validation plan

Run the focused relay plus existing candidate economy/defense/route tests,
compileall, `make static`, `make smoke`, then the configured 15-map regression
screen against immutable v0044.  If the screen is negative, allow one small
relay-only repair and then restore exact source parity.  No release gate or
platform operation is justified by this experiment alone.

## Status

Approved for implementation; results and rollback evidence will be appended
below without rewriting this record.

## Repair 1 scope

The initial 15-map screen placed only one Launcher and finished 5-10 against
v0044, so the front-distance gate was not exercising the mobility architecture
on enough maps.  The single bounded repair removes only that geometric build
gate: after the first paying route and the same reserve check, the permanent
Attacker may stage its one Launcher wherever it is, while the Launcher still
requires a visible passable strict-progress destination and `can_launch`.
No new unit may be picked up, no Store/economy/route policy changes, and no
second repair are permitted.

## Validation and decision

- Initial focused relay plus existing economy/defense/route coverage passed
  **37/37**; compileall passed; `make static` retained the inherited 15
  obsolete-import errors and two navigation assertions; smoke was **4/4** at
  `reports/local-20260819T220959Z`.  The initial 15-map screen was command-
  clean but **5–10**, with **56,250/66,690 Ti**, 14/15 candidate deliveries,
  and one candidate Launcher at `reports/local-20260819T221018Z`.
- Repair coverage passed **38/38**, compileall passed, static retained the
  same inherited profile, and smoke was **4/4** at
  `reports/local-20260819T221331Z`.  The repair screen was command- and
  delivery-clean at **7–8**, **56,360/55,140 Ti**, 15/15 deliveries, and
  average first delivery **28.7 vs 38.9** turns at
  `reports/local-20260819T221350Z`.
- The independent seed-173 screen was command- and delivery-clean but
  regressed to **6–9**, **45,980/53,320 Ti**, with 15/15 deliveries and
  four candidate Launchers at `reports/local-20260819T221608Z`.

The mobility edge was not repeatable, so v308 is **rejected** without a long
gate or release.  The temporary production changes and focused test were
removed.  Rollback focused coverage passed **34/34**, compileall passed,
static retained the inherited profile, rollback smoke was **4/4** at
`reports/local-20260819T221855Z`, and recursive production-source parity with
immutable v0044 is zero at
`reports/iter-v308-launcher-relay/rollback-source-parity.diff`.  No package,
upload, activation, or live-state transition occurred; live v107 and v105
rollback state are unchanged.
