# v241 reactive inward infiltrator Barrier — rejected

## Objective and evidence

The user hypothesis was to improve defense against enemy infiltrators. The
existing replay audit showed route-radius enemy Builders were uncommon, and
v225/v226/v227/v229/v230/v233/v235/v236/v237 had already rejected broad
interception, body-blocking, hijack, Launcher, and turret-priority variants.
This iteration therefore tested one narrower response: when a visible enemy
Builder is already selected as a home threat, the nearest dynamic responder
may place one Barrier on the cardinal tile immediately inward toward our Core.

The response is reactive rather than an opening shell. It requires one
completed route and a live reserve for one Harvester plus two Conveyors, never
uses the Core footprint/ring, refuses to sever a friendly belt, and falls back
to the existing movement response when no legal site exists. No offensive
infiltration, Store, route, workforce, turret, or Launcher policy changed.

## Allowed files

- `bots/candidate/bot/dynamic.py`;
- `bots/candidate/bot/constants.py`;
- `tests/test_candidate_infiltrator_barrier.py`;
- this record, `UPDATES.md`, and durable state/report metadata.

## Validation

- New barrier plus nearest-defense/seeded-route focused coverage: **31/31**.
- Candidate and baseline compileall: passed.
- `make smoke`: **4/4** command-clean (`reports/local-20260819T012040Z`).
- `make static`: unchanged inherited exit 2: 15 obsolete deleted-module
  imports and two navigation fast-path assertions
  (`reports/iter-v241-infiltrator-barrier/static.log`).
- Rotated 15-map screen was command-clean with zero TLE/suspicious rows and
  all 15 deliveries on both sides, but candidate-A lost **7-8** and collected
  **67,990 vs 93,250 Ti**. Candidate placed **4.67** Barriers per game versus
  **4.07** for v0042; this did not produce a paired win or collection edge.
  Maximum p99/peak callback time was **1,368/5,083 us**. Raw report:
  `reports/local-20260819T012111Z`; parsed replay diagnostics:
  `reports/iter-v241-infiltrator-barrier/replay-analysis.json`.

## Decision and rollback

The barrier event did not convert into a screen edge, so no repair or 60-game
gate was justified. Temporary source and focused test were removed. Candidate
Python source is recursively byte-identical to immutable v0042 (zero lines in
`reports/iter-v241-infiltrator-barrier/rollback-source.diff`). Rollback focused
coverage was **27/27**, compileall passed, rollback smoke was **4/4** at
`reports/local-20260819T012415Z`, and rollback static retained the inherited
failures. No promotion, package, upload, activation, or live-state transition
occurred.

## Follow-up

Do not widen the infiltrator branch without new replay evidence. The current
baseline's larger loss is resource conversion, not a reproducible home-builder
infiltration signal; the next hypothesis should target a high-frequency
economy-to-pressure conversion that leaves the fixed attacker on its lane.
