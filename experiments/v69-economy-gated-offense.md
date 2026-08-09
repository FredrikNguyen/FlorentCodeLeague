# v69 economy-gated offense

## Scope

- Parent: `bots/versions/v0013_reviewer-v69-platform-winner_20260809-1444_7dd72f03`
- Candidate: `bots/candidate`
- Hypothesis: delaying discretionary offense until all four Store-backed routes
  are maintaining will prevent early Core sightings from diverting the free
  workforce and improve paired outcomes without weakening reliability.
- Strategy change: require `maintaining_routes >= route_target` for both verified
  Core and non-Core offensive phase transitions; retain the round-700 endgame
  fallback and reactive defense.

## Promotion gate

- At least 27 wins in the 48-game protected matrix against v69.
- Positive paired score, no 0-6 map, and no command/runtime failures.
- Aggregate collected titanium does not regress materially.
- Focused tests, static, smoke, regression, release matrix, and remote gate pass.

## Result

- Focused tests: 3 passed.
- Protected matrix: `reports/local-20260809T150256Z`.
- Outcome: 21-27-0, paired score -6/48.
- Titanium: 105,030 versus 122,070, ratio 0.8604.
- Reliability: 48/48 commands clean.
- Map failure: `twins` 0-6; all other maps 3-3.

## Status

Rejected. The verified-Core transition was restored exactly to v69 behavior.
