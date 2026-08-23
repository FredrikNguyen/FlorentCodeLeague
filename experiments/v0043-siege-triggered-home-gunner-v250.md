# v250 — siege-triggered early home Gunner — rejected

## Objective and evidence

The pre-v106 c884 loss sample contained small enemy Launcher/Sentinel rushes,
so this iteration tested one route-free home response: allow the designated
defender to build exactly one early Gunner only when a visible enemy offensive
turret was already near the Core or the Core's siege beacon was active. The
existing Harvester, two-Conveyor, and idle-attacker reserves remained hard
gates. No infiltrator selector, hijack route, fixed attacker, or economy loop
was changed.

## Scope

- `bots/candidate/bot/defender.py`;
- `tests/test_candidate_nearest_defense.py`;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable metadata.

## Validation

- Initial focused coverage: **29/29**; candidate compileall passed; smoke was
  **4/4** command-clean. `make static` retained the inherited 15 obsolete
  deleted-module imports and two navigation fast-path assertions.
- Seed-172 all-map screen: **10-5** candidate-A, command/delivery-clean with
  zero TLE/suspicious rows (`reports/local-20260819T043258Z`, parsed at
  `reports/iter-v250-early-home-gunner/screen-replay-analysis.json`).
- Independent seed-173 screen: **5-10** candidate-A, still command-clean but
  with no repeatable edge (`reports/local-20260819T043443Z`, parsed at
  `reports/iter-v250-early-home-gunner/screen173-replay-analysis.json`).
- After rollback, focused coverage was **26/26**, compileall passed, smoke was
  **4/4**, and recursive candidate/source parity with the v0043 snapshot was
  zero (`reports/iter-v250-early-home-gunner/rollback-source.diff`).

## Decision

Reject v250 after the independent screen. The route-free Gunner response did
not reliably convert the observed rush signal into wins and is not evidence
for reopening the broad infiltrator-defense family. v0043 remains the local
baseline and active platform v106; no package, upload, activation, or live
state transition was made for v250.

## Live follow-up

The first attributable v106 ladder series later completed as platform Team B:
**1-4** versus Banminary v83 (`9c66c9bc-a75c-46ad-9733-a1b03c007ac5`). The
five downloaded games are under
`reports/iter-v251-live-check/9c66c9bc/`. v106 losses on Icefloe, Midgard,
Glacierkeep, and Drakkarfjord showed the bot reaching the opposing half with
two-to-four Harvesters but **zero Sentinels**, including a no-delivery
Drakkarfjord game; the cramped Fjordgate win built three Sentinels early. This
points to a stale/over-strict offense transition, not a frequent infiltrator.
