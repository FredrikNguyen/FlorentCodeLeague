# v0030 dynamic raid-recovery cycle — rejected

## Objective

Use the live replay evidence to make logistics raiders alternate between a
bounded sabotage pulse and a home defense/build phase, while preserving the
current v96 source as the rollback candidate.

## Replay evidence

- The newest attributable ladder match was the prior v95 submission against
  Kings College Munich (`edb000ab-87a1-41d9-9ae3-4c7e58354be7`), which v95 lost
  1–4. Its losses showed both early route collapse (one harvester and delivery
  at turn 108) and late non-conversion (18 harvesters but only four gunners
  against an opponent with 26 gunners). Replays are in
  `replays/live-latest-v95-edb000ab/`.
- The top-team replay set showed delivery around turns 7–15, a small but real
  defensive shell, and repeated logistics pressure rather than an unbounded
  attacker march. Sources reviewed: `replays/top-live-20260812-sporks-pivot/`
  and `replays/top-live-20260812-clankers-sporks/`.

## Candidate and bounded repairs

1. Added `TASK_RECOVER`: after a dynamic Builder destroyed or lost a raid
   target, it returned to the home ring for 12 rounds; raid selection was
   suppressed while the core siege beacon was active.
   - Result against v95: **21–33**, 262,220–333,480 titanium, zero command
     failures, max replay p99 1,377 µs (`reports/local-20260812T213830Z`).
2. Repair: restored harvest-before-raid ordering, required four completed
   routes and a harvester-cost surplus for raids, and gave fixed attackers the
   same return-home/build pulse.
   - Result against v95: **16–38**, 251,170–322,830 titanium, zero command
     failures, max replay p99 1,533 µs (`reports/local-20260812T214855Z`).

Focused raid-cycle tests passed during both attempts; smoke was command-clean
(`reports/local-20260812T213811Z`, `reports/local-20260812T214837Z`). `make
static` remains blocked by the repository's inherited 15 obsolete pre-v86 test
imports (`reports/v0030-raid-recovery-static.log`,
`reports/v0031-raid-recovery-attacker-static.log`).

## Decision

Both bounded repairs regressed the retained v95 comparator. The temporary
changes were removed with `apply_patch`; `bots/candidate` is byte-identical to
the downloaded v96 source again. Final restored smoke/compile/diff checks pass
(`reports/local-20260812T215759Z`). No package, upload, activation, or live
state transition was performed. The next experiment should change workforce
allocation/route conversion rather than add more raid timing gates.
