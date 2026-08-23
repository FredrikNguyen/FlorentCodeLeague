# Post-v76 heart route-owner continuity

## Hypothesis

Extend the pre-income route-owner Builder-rush guard from the proven 20x26 and
25x15 layouts to 28x20, because v76's live heart loss collected no titanium.

## Result

- Focused tests: 5/5 passed.
- Exact live heart seed: 2-0 and 8,470-0 titanium;
  `reports/local-20260810T003501Z`.
- Heart/eider screen: 15-5 and 57,660-15,950 titanium;
  `reports/local-20260810T003537Z`.
- Static retained only inherited failures; `reports/v77-heart-owner-static.log`.
- Smoke: 4/4 command-clean; `reports/local-20260810T003856Z`.
- Current-pool release matrix: 47-43 and 226,830-223,720 titanium, with zero
  reliability failures; `reports/local-20260810T004411Z` and
  `reports/v77-heart-owner-release-analysis.json`.
- Three-map confirmation outside the intended target was 15-15 but lost
  174,360-186,110 titanium. Drumlin alone lost 72,810-86,300;
  `reports/local-20260810T010110Z`.

## Decision

Rejected. The targeted heart gain did not produce a significant aggregate
improvement and retained a material titanium regression on drumlin. Candidate
source was restored exactly to immutable v0019; no package or platform version
was created.
