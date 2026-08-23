# Post-v76 moonrise route-owner continuity

## Hypothesis

Extend the pre-income route-owner Builder-rush guard from the proven 20x26 and
25x15 layouts to 21x8, because v76's first live moonrise game built one Conveyor
but no Harvester and collected zero titanium.

## Result

- Focused tests: 5/5 passed.
- Exact live seed: both seats built a Harvester on turn 10 and delivered on turn
  13, but the candidate went only 1-1 and collected 1,290 versus 2,680 titanium;
  `reports/local-20260810T002353Z`.
- Five standard seeds: 10/10 command-clean, 5-5, but 6,450 versus 13,400
  titanium; `reports/local-20260810T002426Z`.

## Decision

Rejected. The symptom fix did not beat immutable v0019 and materially reduced
collection. Candidate source was restored exactly to v0019; no package or live
operation was created.
