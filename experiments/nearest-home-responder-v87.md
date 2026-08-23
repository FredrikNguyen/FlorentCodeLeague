# Nearest home-responder allocation

## Objective

Reduce route starvation caused by several dynamic Builders independently
responding to the same visible home threat. Keep the current v87 economy,
workforce, navigation, and combat rules unchanged outside threat assignment.

## Hypothesis

Home-threat detection is local, so every dynamic Builder can select the same
enemy turret or harvester. If each responder deterministically yields to a
closer non-attacker Builder (distance, then entity id), one Builder owns the
response while the rest continue route work. Permanent attackers are excluded
from the comparison because they do not execute the home-threat task.

## Implementation

- `bots/candidate/bot/dynamic.py`: added `_is_nearest_home_responder()` and
  cleared duplicate `TASK_HOME_THREAT` assignments before movement or
  counter-Gunner construction.
- `tests/test_candidate_nearest_defense.py`: covers nearest selection and
  permanent-attacker exclusion.

## Evidence

- Focused tests: 2/2; static contract: 8/8; compileall: pass.
- Smoke: 4/4 command-clean, `reports/local-20260812T131542Z`.
- Two 48-game checkpoints versus exact active v87:
  - 27-21, 150,760-146,320 Ti, `reports/local-20260812T131553Z`;
  - 28-20, 158,460-121,830 Ti, `reports/local-20260812T131958Z`.
- Full 210-game gate: 128-82, 785,220-699,810 Ti (1.1220x),
  210/210 command-clean, zero TLE/suspicious output, max p99 1.469 ms,
  peak 2.728 ms, `reports/local-20260812T132348Z`.
- Remote server gate against the exact v87 artifact: candidate 3-2,
  match `b643b12e-6549-4564-a069-6b88a5ddf669`,
  `reports/remote-20260812T133953Z` and
  `reports/nearest-defense-remote-info-final.json`.

## Risks and decision

Jackpot is 3-7 in the full matrix and string/sweden/twins are 4-6; no map is
a 0-10 collapse. `make static` still reports the inherited 15 obsolete-import
errors from the retired pre-v86 test layout. The candidate is eligible for a
guarded package/deploy, with active v87 preserved as rollback.
