# v69 second satellite after primary economy

## Scope

- Parent: `bots/versions/v0013_reviewer-v69-platform-winner_20260809-1444_7dd72f03`
- Candidate: `bots/candidate`
- Hypothesis: after all four primary routes maintain, electing a second frontier
  pioneer as soon as one extra worker and route are fully funded will turn idle
  surplus into additional Harvesters and improve the titanium tiebreak.
- Changed mechanism: lower only the post-four-route second-pioneer funding gate;
  preserve primary-route concurrency, defense interrupts, and verified-Core cap.

## Promotion gate

- At least 27 wins in the protected 48-game matrix against v69.
- Positive paired score, no 0-6 map, zero command/runtime failures.
- Aggregate collected titanium ratio at least 1.00.

## Result

- Focused tests: 2 passed.
- Protected matrix: `reports/local-20260809T151148Z`.
- Outcome: 24-24-0, paired score 0/48; every map was 3-3.
- Titanium: 112,030 versus 115,390, ratio 0.9709.
- Reliability: 48/48 commands clean.

## Status

Rejected. The second-pioneer funding gate was restored exactly to v69 behavior.
