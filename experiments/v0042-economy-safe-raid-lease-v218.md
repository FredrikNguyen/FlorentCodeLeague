# v218 — economy-safe continuous raid lease (rejected)

## Replay basis and hypothesis

v217 showed that fresh fixed-attacker pressure before siege topology could
delay first delivery. v218 returned the offense lease to dynamic Builders,
but required visible harvest to be absent, the normal offense milestone, a
Harvester-cost replacement bank plus `IDLE_ATTACK_RESERVE`, confirmed shared
enemy-Core intel, and the existing loaded/nearest raid selector. The intent
was to preserve the opening economy while converting replaceable surplus into
continuous sabotage.

## Validation

Focused coverage was **6/6** in the new economy-safe module and **43/43** in
the root subset; compileall passed, smoke was **4/4** at
`reports/local-20260818T182237Z`, and static retained only the inherited exit
2 (15 obsolete deleted-module imports and two navigation fast-path
assertions). The rotated 15-map screen looked promising at **10-5**, with no
no-delivery rows, collection **58,130 vs 52,640 Ti**, mean first delivery
**54.53 vs 44.40**, and max p99/peak **1,430/5,828 us**.

The required 60-game release matrix was command-clean with zero TLE or
suspicious rows, but it finished **30-30**. Candidate collection was
**271,280 vs 284,390 Ti**, mean first delivery **29.14 vs 26.31**, and
no-delivery rows were **2 vs 1**. Map floors included Antler, Auroraveil,
Drumlin, Icefloe, and Midgard at **1-3**. The screen edge did not transfer,
so v218 failed the aggregate, delivery, and protected-map guards.

The exact pre-v218 `dynamic.py` snapshot was restored (SHA-256
`bcaa62c16403024e37a2149659160d04c01ec287d80679394d7bc8d7980651fd`), the
temporary focused test/config were removed, and rollback coverage was
**37/37** plus compileall. v0042 remains the immutable baseline. No
promotion, package, upload, activation, or live-state transition occurred.
Evidence: `reports/local-20260818T182307Z`,
`reports/local-20260818T182519Z`, and
`reports/iter-v218-economy-safe-raid/`.
