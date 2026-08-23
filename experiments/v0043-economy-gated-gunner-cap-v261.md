# v261 economy-gated home-Gunner cap — rejected

## Replay basis and objective

The v260 screen and the fresh Coreflood loss showed an economy/defense trade:
our side could hold four home Gunners with four Harvesters while the opponent
reached 19 Harvesters from a similar Builder count. The retained Core policy
raised its threat cap to five after the three-route milestone for any visible
enemy building, not only an offensive turret. v261 separated ordinary contact
from a real siege: ordinary contact could not expand the cap until
`ECONOMY_STRONG_CHAINS` (five completed routes), while a visible Gunner,
Sentinel, or Launcher retained a one-extra-Gunner immediate exception.

## Validation

- Focused coverage was **29/29**, candidate/baseline compileall passed, and
  `make smoke` was **4/4**. `make static` retained the inherited 15 obsolete
  deleted-module import errors and two navigation fast-path assertions.
- The exact-v0043 rotated 15-map screen was command-clean at **6-9**, with
  candidate/baseline collection **69,440/81,410 Ti**, zero TLE/suspicious rows,
  and raw report `reports/local-20260819T075756Z`. Replay diagnostics are in
  that report's `replays/` directory.
- No screen replay supplied a controlled cap/siege event that justified the
  one allowed repair. The lower Gunner count did not convert into a paired
  win or collection edge; losses still showed workforce/route divergence.

## Decision and rollback

Reject v261 without a repair or longer gate. Temporary cap/test edits were
removed. Candidate source is recursively byte-identical to immutable v0043 at
`reports/iter-v261-gunner-cap/rollback-source.diff` (empty); rollback focused
coverage was **26/26**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T080048Z`. No release gate, package, upload,
activation, promotion, or live-state transition occurred.

## Remaining risk and next direction

Home-Gunner spend is not the sole conversion bottleneck. The loss rows retain
long chains and too few Harvesters, so the next experiment should change how a
SCOUT discovers and commits to nearby ore rather than changing another turret
knob. Preserve the Coreflood siphon evidence for a future loaded-target raid.
