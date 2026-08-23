# v132 — confirmed enemy-Core intel for flexible builders (rejected)

## Objective

Let dynamic and defender builders consume the fixed-attacker's confirmed
enemy-Core position through the delayed Store, so flexible roles can advance,
raid, and deny ore against the real target instead of a symmetry guess. The
initial variant also let any role publish a directly visible enemy Core; that
was removed in repair 1 after the short screen showed an economy collapse.

## Scope

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- `reports/iter-enemy-core-intel-v132/`

No route FSM, constants, workforce quotas, ammo policy, navigation algorithm,
baseline archive, package, upload, activation, or live state was changed.

## Evidence

- Initial focused tests passed 21/21, compileall passed, `make smoke` was 4/4
  command-clean (`reports/local-20260817T103801Z`), and `make static` retained
  the inherited 15 obsolete-module import errors plus two navigation assertions.
- Initial 24-game screen: **8-16**, candidate 68,100 versus comparator 90,410
  collected titanium, zero command failures, and replay evidence of severe
  Glacierkeep/Archipelago workforce and delivery collapse. Report:
  `reports/local-20260817T103832Z`.
- Repair 1 kept only delayed Store consumption and removed generic direct-Core
  publication. Focused tests passed 21/21, compileall passed, smoke was 4/4
  (`reports/local-20260817T104235Z`), and static retained the same inherited
  failures. The 24-game screen recovered to **14-10**, 85,250 versus 72,670
  collected titanium, zero no-delivery rows, and zero reliability failures.
  Report: `reports/local-20260817T104300Z`.
- Repair 1 54-game checkpoint then regressed to **23-31**, 153,670 versus
  181,620 collected titanium. It had zero command failures/TLE/suspicious
  output, max p99 1,466 us, peak callback 5,234 us, and three candidate
  no-delivery rows. Report: `reports/local-20260817T104525Z`; replay analysis:
  `reports/iter-enemy-core-intel-v132/replay-analysis-54-repair1.json`.

## Decision

Reject after two bounded attempts. The Store-intel edits and two focused tests
were removed with `apply_patch`; candidate source now compares byte-for-byte
with immutable v0037. Rollback focused tests passed 19/19, compileall passed,
and rollback smoke was 4/4 (`reports/local-20260817T105120Z`). No package,
upload, activation, or live baseline change was performed.

## Next hypothesis

Use a different replay-backed structural change; do not reintroduce generic
flexible-builder Core targeting without a shared economic commitment guard.
