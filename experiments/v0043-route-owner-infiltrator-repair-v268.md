# v268 — route-owner repair of confirmed home infiltration

## Hypothesis

Fresh v106 replays repeatedly showed an own home Conveyor being removed and an
enemy Barrier appearing on the same pending output tile one round later. v267
assigned a generic nearby dynamic Builder to repair that tile, but the
independent screen showed route displacement and a no-delivery row. v268 kept
the existing chain owner and, only for a visible enemy Barrier on its exact
pending tile inside `HOME_THREAT_RADIUS_SQ`, destroyed the blocker and rebuilt
the Core-facing Conveyor in place.

## Scope

Only `bots/candidate/bot/defender.py` and focused nearest-defense tests were
changed during the candidate. No Store signal, dynamic task, purchase policy,
offensive selector, baseline snapshot, or platform operation was touched.

## Validation

- Focused candidate suite: **31/31 passed** (`reports/iter-v268-route-owner/`)
- Candidate compileall: passed
- `make static`: exit 2 with the inherited 15 obsolete-module import errors and
  two navigation fast-path assertion failures (`static.log`)
- Smoke: 4/4 command-clean, `reports/local-20260819T100250Z`
- Configured 15-map screen (`screen_seed=172`): **10-5**, candidate collected
  **85,400** vs baseline **60,420** Ti, command-clean,
  `reports/local-20260819T100316Z`
- Independent rotated 15-map screen (`screen_seed=174`): **4-11**, candidate
  collected **53,320** vs baseline **73,590** Ti, command-clean,
  `reports/local-20260819T100509Z`

## Decision

Reject. The apparent first-screen edge is not repeatable and fails the
collection edge on rotation. The temporary code and tests were removed;
recursive candidate/source parity with the frozen v0043 baseline is zero lines
at `reports/iter-v268-route-owner/rollback-source.diff`. Rollback focused
tests passed **26/26**, compileall passed, and rollback smoke was 4/4 at
`reports/local-20260819T100805Z`.

## Risk / next step

The route-owner response is mechanically legal but too sparse to explain the
screen reversal; do not tune its radius or facing. Preserve the replay event
as evidence and test a different fundamental infiltration hypothesis only
after a fresh replay audit, with first delivery protected and an independent
screen required before promotion.
