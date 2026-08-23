# Post-v76 fjordgate route-owner continuity

## Hypothesis

Extend the pre-income route-owner Builder-rush guard to the 10x10 fjordgate
layout, because v76 recorded zero titanium delivery on fjordgate in two live
series.

## Validation

- Focused tests: 5/5 passed.
- Exact live fjordgate seeds: 4-0 and 1,500-0 titanium;
  `reports/local-20260810T011149Z`.
- Standard five-seed fjordgate screen: 10-0 and 3,750-0 titanium;
  `reports/local-20260810T011222Z`.
- Smoke: 4/4 command-clean; `reports/local-20260810T011318Z`.
- Static retained the inherited obsolete API/navigation and line-budget
  failures; the changed focused test passed.
- Full 21-map matrix against immutable v0019: 109-101 and 691,900-663,540
  titanium, with 210/210 command-clean games;
  `reports/local-20260810T011343Z`.
- Downloaded active platform v82 beat this candidate on the 54-game regression
  pool, 34-20 and 149,030-146,450 titanium; zero command failures;
  `reports/local-20260811T212700Z`.

## Decision

Keep the 10x10 guard in the working candidate for further comparison, but do
not package or activate it yet. Active platform v82 is the provisional live and
local winner; it still needs at least 12 live series and a full-map local gate
before becoming the repository baseline.
