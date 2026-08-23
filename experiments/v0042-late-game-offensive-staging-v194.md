# v194 — late-game offensive staging

## Objective

Test a rationed, stepwise offensive frontier: once the six-site enemy-Core
Barrier cage is full, replace one visible obsolete forward Barrier with a legal
replacement only when the replacement is materially closer to the confirmed
Core, a live forward Sentinel supports the move, and the economy has at least
three completed routes.

## Scope and non-goals

Temporary changes were limited to `bots/candidate/bot/attacker.py`, one new
constant, focused staging tests, and the rotated quick-screen seed. Opening
Harvester/path construction, home defense, dynamic task priority, baseline,
package, and live state were out of scope. No Builder self-destruct was used.

## Evidence

- Initial focused coverage: 40/40; repair coverage: 41/41; rollback focused
  coverage: 38/38. Compileall passed throughout; smoke was 4/4 throughout.
- `make static` exited 2 on the inherited missing legacy modules and two
  navigation fast-path assertions; no v194-specific static failure appeared.
- Seed-162 initial screen: **6-9**, candidate/comparator titanium
  **51,350/64,890**, one candidate zero-delivery row
  (`reports/local-20260818T110035Z`). Replay counts confirmed the new path
  changed behavior (some games placed 7–8 Barriers rather than the six-site
  cap).
- The single bounded repair required three completed routes before rotation:
  **6-9**, titanium **81,650/87,800**, zero candidate no-delivery
  (`reports/local-20260818T110337Z`).
- Both 15-game screens were command-clean; replay analyses reported zero TLE
  and suspicious-output rows.

## Decision

Reject after one bounded repair. The repair removed the new no-delivery row but
did not improve paired wins or collection. Temporary attacker/constant/tests
were removed and candidate source was restored recursively identical to
immutable v0042. No release, package, upload, activation, or baseline
transition occurred.

## Follow-up

The next isolated experiment is enemy-resource hijacking: verify ownership and
direction, then seed or repair a Conveyor path to a visible enemy Harvester or
overtake a severed enemy route only when Core delivery and economy/defense
reserves remain safe. It must not be combined with this rejected frontier
rotation.
