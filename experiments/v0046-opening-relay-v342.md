# v342 — reversible primary-attacker economy relay

Date: 2026-08-20

## Hypothesis and scope

Top-team winners keep roughly five Builders productive while still applying
pressure.  v0046's primary fixed attacker never enters the Defender route FSM,
so a cramped opening can leave only the non-attacker Defenders converting ore.
v342 tested a per-unit multitask relay: the primary attacker could seek one
visible local ore source, invoke the existing Harvester/CHAIN FSM once, then
return permanently to its unchanged sentinel/sabotage lane.  Repair 1 limited
the route to a short visible source near the Core; repair 2 additionally
reserved the relay for compact maps where control-first openings are viable.

Allowed production scope was `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, and one focused relay test file.  No Store
schema, global four-route lease, fixed identity change, route geometry,
baseline snapshot, package, platform, or live-state change was allowed to
remain.

## Validation

- Initial focused coverage was **39/39**; repair 1 was **39/39**; repair 2 was
  **40/40**.  Compileall passed after each version.
- Initial 15-map screen was command/delivery-clean but **4-11 candidate-A**,
  with **75,370 vs 84,640 Ti**, zero TLE/suspicious rows, and max p99/peak
  **1,419/4,925 us**.  Report:
  `reports/iter-opening-relay-v342-screen-analysis.json`.
- Repair 1 limited the route to a six-step local source and recovered **8-7**,
  but collection was **73,460 vs 84,720 Ti**.  Report:
  `reports/iter-opening-relay-v342-repair1-screen-analysis.json`.
- Repair 2 made the relay compact-map-only and remained **8-7**, delivery-clean
  but at **85,010 vs 91,110 Ti**; max p99/peak was **1,347/5,328 us**.  Report:
  `reports/iter-opening-relay-v342-repair2-screen-analysis.json`.
- `make static` retained the inherited repository profile (15 obsolete-module
  imports and two navigation assertions).  Rollback focused coverage was
  **35/35**, compileall passed, and rollback smoke was **4/4** at
  `reports/local-20260820T082358Z`.

## Decision and rollback

Reject v342 after two bounded repairs.  The initial screen was decisively
negative, and although both repairs reached 8-7, neither produced a meaningful
conversion edge; no 60-game gate was justified.  Restore exact recursive
production parity with immutable v0046; proof is
`reports/iter-opening-relay-v342-rollback-source-parity.diff`.
No promotion, package, upload, activation, or live transition occurred; live
state remains v108 `active_observing` with v107 known-good.

## Follow-up

Do not retry a fixed-attacker economy relay unchanged.  The next experiment
should address the observed one/zero-Harvester openings through a genuinely
different mechanism—local route-site reservation and path viability—while
keeping continuous offense available and preserving the v0046 rollback.
