# Post-v73 bootstrap-owner focus

## Scope

- Parent: `bots/versions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03`.
- Hypothesis: on close-specialized pre-income maps, route-owning Builders should
  ignore non-adjacent Builder-rush alerts while free workers respond, preserving
  the first funded route without suppressing immediate-contact defense.
- Changed runtime file: `bots/candidate/bot/builder.py`.

## Results

- Focused tests: 3/3 passed; log:
  `reports/v73-bootstrap-owner-defense/focused-final.log`.
- Smoke: 4/4 command-clean; report: `reports/local-20260809T192900Z`.
- Final 15-map paired matrix, seeds 1/19/101: 59-31, titanium 192,330
  versus 166,720, zero command failures; report:
  `reports/local-20260809T195826Z`.
- The target improved: `meander` was 6-0 with 10,830 titanium versus zero.
- Protected-map regressions remained: `snowflake` was 2-4 with a 9,460
  titanium deficit, and `saga` was 2-4 with a 1,150 deficit.
- `make static` still fails only on the inherited pre-v69 API suite and obsolete
  production line cap; log: `reports/v73-bootstrap-owner-defense/static.log`.

## Decision

Rejected after two bounded repair passes because the final scoped matrix failed
the protected-map guard. Do not package or deploy this candidate. Platform v73
remains the deployed v0015 parent, with platform v72 as rollback.
