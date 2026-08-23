# v249 liquidity-backed dynamic economy floor — promoted locally

## Objective and hypothesis

Fresh v105 loss replays showed repeated route attrition and weak resource
conversion (especially on Drakkarfjord), while route-radius enemy-Builder
infiltration was rare. The candidate therefore keeps fixed attackers on their
existing continuous Core/sabotage lane, but reserves one nearby dynamic
Builder for harvest/exploration through five completed routes when the bank
cannot fund a replacement Harvester, two short Conveyor links, and the fixed
offense reserve. A rich bank releases the dynamic pool to the normal raid/
advance ladder immediately.

This is a liquidity-backed route-resilience lease, not a broad infiltrator
detector or a global economy lock.

## Scope and non-goals

Changed only:

- `bots/candidate/bot/constants.py` — add `DYNAMIC_ECONOMY_FLOOR = 5`;
- `bots/candidate/bot/dynamic.py` — state-aware `_should_harvest` and a
  deterministic nearest dynamic owner for the low-bank lease;
- `tests/test_candidate_nearest_defense.py` — focused floor and ownership
  coverage;
- this record, plan/state/update metadata, and reports.

No Store schema, route FSM, fixed-attacker lane, infiltration/hijack primitive,
weapon policy, map branch, baseline source edit, or live operation was part of
the hypothesis.

## Validation

- Initial focused coverage: **25/25**; candidate compileall passed; smoke
  **4/4** command-clean (`reports/local-20260819T035210Z`). Static retained
  the inherited 15 deleted-module import errors and two navigation fast-path
  assertions (`reports/iter-v249-liquidity-floor/static.log`).
- Initial 15-map screen: **10–5** candidate-A, **88,300 vs 64,910 Ti**, zero
  command failures/TLE/suspicious rows. An independent all-map screen was
  **7–8**, **102,810 vs 68,630 Ti**, also command/delivery clean. Reports:
  `reports/local-20260819T035235Z` and `reports/local-20260819T035441Z`;
  combined replay diagnostics are in
  `reports/iter-v249-liquidity-floor/replay-analysis.json`.
- First 60-game gate: command-clean **30–30**, **291,610 vs 293,760 Ti**,
  zero TLE/suspicious rows, max p99/peak **1,567/5,134 us**. This tied and was
  not promotable.

## Bounded repair

The initial floor applied to every dynamic Builder during a low-bank phase.
The one allowed repair kept the same phase and budget contract but assigned
it to exactly one nearest dynamic Builder, excluding fixed attacker/defender
IDs. Focused coverage became **26/26**, compileall passed, static retained
the same inherited failures, and smoke remained **4/4** at
`reports/local-20260819T040512Z`.

The repair screen was **7–8**, **59,780 vs 48,790 Ti**, command/delivery clean
with no TLE/suspicious rows (`reports/local-20260819T040534Z`). The final
60-game endpoint/side-swap gate was command-clean and **35–25 (58.3%)** for
the candidate, **277,160 vs 241,120 Ti**, with **7.87 vs 7.63** Harvesters per
game, one candidate no-delivery row, zero TLE/suspicious rows, max p99/peak
**1,545/4,433 us**, and no 0–4 map floor. Full evidence:
`reports/local-20260819T040658Z` and
`reports/iter-v249-liquidity-floor/repair-release-replay-analysis.json`.

The remote five-map gate returned match `3e05d451-0447-4b4c-b28a-0103a7b430de`
with a successful command record at `reports/remote-20260819T041421Z`.

## Decision and risks

Promote this repair locally as the new moving baseline candidate. The
aggregate win-rate edge clears the 55%/positive-paired-score rule and all
runtime gates are clean. The one no-delivery row and 1–3 floors on Antler,
Drumlin, Midgard, Valkyrie, and Yulerune remain risks. The package was uploaded
as platform version **106** (`v0043-liquidity-backed-dynamic-floor-eeafad8f`)
and the platform made it active at **2026-08-19T04:16:32Z**. The local live
state is `active_observing` with platform **101** preserved as rollback; the
observation snapshot is `reports/live-observe-20260819T041709Z`. The guarded
explicit activation confirmation returned `already_active: true` at
`reports/activation-20260819T041911Z`.
