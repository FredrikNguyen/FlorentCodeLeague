# v220 — corridor-loaded raid lease (rejected)

## Replay basis and hypothesis

v219 showed that passive enemy-half Barriers diverted dynamic Builders and
collapsed collection. v220 returned to active loaded sabotage, but admitted a
raid only when the Builder-to-target-to-confirmed-Core Manhattan route had at
most six tiles of detour. This was intended to keep useful lateral pressure
while avoiding v215's arbitrary off-lane chase; visible ore remained available
to other workers, and all existing reserve/intel/loaded/nearest gates stayed
in force.

## Validation

Focused coverage was **8/8** in the new corridor module and **45/45** in the
root subset; compileall passed, smoke was **4/4** at
`reports/local-20260818T184201Z`, and static retained only inherited failures.
The rotated screen was command-clean and delivery-clean at **8-7**, with no
no-delivery rows, collection **81,430 vs 66,320 Ti**, mean first delivery
**24.53 vs 26.00**, and max p99/peak **1,407/5,276 us**. The 60-game matrix
was command-clean with zero TLE/suspicious rows but finished **24-36**;
collection was **262,580 vs 300,390 Ti**, mean first delivery **28.00 vs
30.35**, and no-delivery rows **1 vs 0**. Drakkarfjord and Glacierkeep were
both **0-4**, so the release and protected-map guards failed.

The exact pre-v220 `dynamic.py` snapshot was restored (SHA-256
`bcaa62c16403024e37a2149659160d04c01ec287d80679394d7bc8d7980651fd`), the
temporary test/config were removed, and rollback coverage was **37/37** plus
compileall. v0042 remains the immutable baseline. No promotion, package,
upload, activation, or live-state transition occurred. Evidence:
`reports/local-20260818T184229Z`, `reports/local-20260818T184443Z`, and
`reports/iter-v220-corridor-raid/`.
