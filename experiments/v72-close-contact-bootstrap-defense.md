# v72 close-contact bootstrap defense

## Scope

- Parent: `bots/versions/v0014_canonical-opening_20260809-1606_7dd72f03`.
- Hypothesis: redundant pre-income defensive construction is harmful on
  close-contact specialized geometries but useful on distant/balanced maps;
  narrow only the former to one designated free Defender and one structure.
- Changed runtime file: `bots/candidate/bot/builder.py`.
- Non-goals: no phase, route, workforce, navigation, post-income combat, or
  opening-orientation changes.

## Gate

- Focused tests cover close specialized, distant, balanced, and post-income
  behavior.
- Current-pool seed-1 checkpoint beats v0014 without the rejected experiment's
  `hive`, `jackpot`, `lighthouse`, or `snowflake` collapse.
- A passing candidate must then clear the wider paired release gates.

## Results

- Focused tests after self-review: 9/9 passed; log:
  `reports/v72-close-contact-bootstrap-defense/focused-after-review.log`.
- Smoke: 4/4 command-clean; report: `reports/local-20260809T184659Z`.
- Current 15-map pool, seeds 1/19/101, both sides, with the reviewed affected
  blocks recomputed: 51-39, titanium 171,550 versus 168,040 (ratio 1.0209),
  zero command failures.
- Matrix sources: `reports/local-20260809T184216Z`,
  `reports/local-20260809T184730Z`, replacing `eider`, `fjordgate`, and `heart`
  with `reports/local-20260809T185644Z` after the recovery-scope fix.
- Replay CPU across 680,738 candidate calls: p99 2.975 ms, max 7.511 ms,
  zero TLEs.
- Remote gate: 4-1, reliability-clean, match
  `a4fdd82b-f5c1-449c-a809-473cdbdfde31`; report:
  `reports/remote-20260809T190000Z`.
- `make static` still fails only on the inherited pre-v69 API suite and obsolete
  production line cap; log:
  `reports/v72-close-contact-bootstrap-defense/static.log`.

## Package

- Snapshot: `bots/versions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03`.
- Archive: `artifacts/submissions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03.zip`.
- SHA-256: `fa5ec52b970998434ae80598e296ec6d7aca0afa872e26f26338f1e8ae8fcb1e`.

## Status

Passed local and remote release gates; packaged and waiting for platform v72 to
reach the 24-series known-good promotion threshold before deployment.

## Live parent evidence

- At 18 observed series, platform v72 is 13-5 by series and 57-33 by games,
  with +61.481 Elo, a 0.6333 fractional game score, +0.1067 opponent-adjusted
  residual, and no observed reliability failure.
- Replay diagnosis confirms the hypothesized failure on `meander` and
  `moonrise`: v72 can build multiple Barriers and Launchers before establishing
  income, then die or remain economically starved. Summary:
  `reports/v72-live-diagnosis-20260809T1915Z/summary.md`.
