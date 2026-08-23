# v343 — local route-site reservation and path viability

Date: 2026-08-20

## Hypothesis and scope

v342 showed that a fixed-attacker relay delays pressure, while the opening
losses still contain one/zero effective Harvesters.  Replay inspection found
that Builders can compete for visible ore and commit to a source without any
currently visible path toward a Core sink.  v343 reused each Builder's
existing target as a local site reservation and added a visible-only BFS from
the source's legal conveyor neighbours to a Core-facing tile.  Unknown
long-range terrain remained eligible.  Repair 1 allowed distant reservations
to yield to adjacent sources; repair 2 restored strict reservations but used
an uncertain adjacent source as a last local fallback.

Allowed production scope was `bots/candidate/bot/defender.py`, with one focused
route-site test file.  No attacker/role policy, Store schema, opening spend,
fixed identity, combat, route geometry, baseline, package, platform, or
live-state change was allowed to remain.

## Validation

- Initial focused coverage was **40/40**; repair 1 was **41/41**; repair 2 was
  **41/41**.  Compileall passed after each version.
- Initial seed-173 screen was delivery-clean at **8-7 candidate-A**, with
  **83,130 vs 61,370 Ti** (+21,760), zero TLE/suspicious rows, and max
  p99/peak **1,354/5,481 us**.  Report:
  `reports/iter-route-site-v343-screen-analysis.json`.
- The required rotated seed-172 screen exposed a regression: **5-10**, one
  candidate no-delivery Drakkarfjord row, **67,530 vs 84,110 Ti**, max
  p99/peak **1,473/6,031 us**.  Report:
  `reports/iter-route-site-v343-rotated-screen-analysis.json`.
- Repair 1 was **2-13** and **49,520 vs 91,090 Ti**.  Repair 2 restored
  delivery cleanliness but only reached **7-8** and **79,460 vs 89,810 Ti**;
  its max p99/peak was **1,416/4,937 us**.  Reports:
  `reports/iter-route-site-v343-repair1-screen-analysis.json` and
  `reports/iter-route-site-v343-repair2-screen-analysis.json`.
- Rollback focused coverage was **35/35**, compileall passed, `make static`
  retained the inherited 15 obsolete-module imports plus two navigation
  assertions, and rollback smoke was **4/4** at
  `reports/local-20260820T084012Z`.

## Decision and rollback

Reject v343 after the two permitted bounded repairs.  The initial positive
screen was contradicted by the rotated screen; neither repair produced a
repeatable win-rate or conversion edge, and one version introduced a
no-delivery row.  Restore exact recursive v0046 parity; proof is
`reports/iter-route-site-v343-rollback-source-parity.diff`.
No promotion, package, upload, activation, or live transition occurred; live
state remains v108 `active_observing` with v107 known-good.

## Follow-up

Do not retry target reservation/BFS as a standalone opening fix.  The next
fundamental experiment should study the conversion/pressure phase itself:
top-team winners keep a control shell active while repeatedly pulsing loaded
logistics, whereas v0046 often spends its first resources on route work and
then idles or arrives after the opponent's shell is established.
