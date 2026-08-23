# v222 rotating secondary pressure lease — rejected at screen

## Objective and scope

Keep the primary fixed attacker on the direct Core/sentinel lane and let only
the designated second attacker perform one reserve-gated visible logistics
sabotage cycle, then return toward the confirmed Core. The temporary scope was
`bots/candidate/bot/attacker.py` plus one focused ownership/legality test
module and checkpoint metadata. No dynamic-builder, Store, cost, Sentinel-cap,
Launcher, map, package, upload, activation, or live-state change was allowed.

## Validation

The Luna implementation and root review passed **6/6** new focused tests and
the existing root subset passed **43/43**; candidate compileall passed, smoke
was **4/4** (`reports/local-20260818T192030Z`), and `git diff --check` was
clean. `make static` retained the inherited exit-2 profile: 15 obsolete
deleted-module imports and two navigation fast-path assertions, with no
v222-specific static failure.

The rotated 15-map screen (seed 188) was command-clean with zero TLE or
suspicious output, but it lost **1-14** against v0042. Candidate collection was
**41,340 vs 75,000 Ti**, mean first delivery **91.93 vs 27.87 rounds**, and
candidate no-delivery was **1** versus **0**. The candidate placed no forward
Sentinel on seven maps and only one on most others, so the role split starved
the very pressure shell it was intended to sustain. Max p99/peak were
**1,402/4,036 us**.

## Decision and rollback

Reject v222 without a release gate or repair attempt. The exact pre-v222
attacker source was restored byte-identically to
`e450ce16dbfae8d581373ee398eea1b6fb9e898bd0925ea2d6c721de77295183`;
the temporary test and screen config were removed. Rollback focused coverage
was **37/37**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260818T192409Z`. v0042 remains the immutable baseline; no
promotion, package, upload, activation, or live transition occurred.

Evidence: `reports/local-20260818T192113Z`,
`reports/iter-v222-rotating-secondary-pressure/`, and this record.
