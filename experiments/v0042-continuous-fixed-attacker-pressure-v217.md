# v217 — continuous fixed-attacker pressure lease (rejected)

## Replay basis

The v215 dynamic raid-first gate won 32-28 in its release matrix but had a
Ragnarok 0-4 collapse. v216's geometry gate was too restrictive and fell to
6-9. The next hypothesis kept dynamic Builders unchanged and moved the
existing fixed-attacker pulse ahead of Launcher/Core-barrier topology so a
ready attacker would convert a legal sabotage or stale-target transition
before spending its action on siege setup.

## Bounded implementation

The temporary `attacker.py` change placed the existing
`_continue_offense_pulse` and `_try_sabotage_with_attacker` phase before the
existing Launcher and enemy-Core Barrier builders, with no new gates,
resources, Store slots, units, or map branches. Focused coverage was **5/5**
in the new order/legality module and **42/42** in the root subset; compileall
passed, smoke was **4/4** at `reports/local-20260818T181203Z`, and static
retained the inherited exit 2.

The first rotated 15-map screen (seed 182) was command-clean and delivery-
clean with zero TLE/suspicious rows at **8-7**, but collection was only
**52,850 vs 74,180 Ti** and mean first delivery was **78.13 vs 26.53**. Three
candidate losses first delivered at rounds 121, 589, and 257. The bounded
repair retained only pending-pulse priority and left fresh sabotage behind
topology. Its independent seed-183 screen stayed command-clean at **7-8**,
collection **81,780 vs 91,470 Ti**, mean first delivery **23.13 vs 29.27**,
max p99/peak **1,362/4,924 us**, and protected Icefloe/Nordkap/Ragnarok
losses. Neither screen earned a release gate.

The exact pre-v217 `attacker.py` snapshot was restored (SHA-256
`e450ce16dbfae8d581373ee398eea1b6fb9e898bd0925ea2d6c721de77295183`), the
temporary test/config were removed, and rollback coverage was **37/37** plus
compileall. v0042 remains the immutable baseline. No promotion, package,
upload, activation, or live-state transition occurred. Evidence:
`reports/local-20260818T181237Z`,
`reports/local-20260818T181610Z`, and
`reports/iter-v217-fixed-attacker-pressure/`.
