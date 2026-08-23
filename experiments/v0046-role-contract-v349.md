# v349 phase-aware role/task contract — rejected, v0046 retained

Date: 2026-08-20

## Objective and evidence

The official top-team source/replay audit showed a structural gap in v0046:
winning bots keep a shared route-building workforce productive until income is
real, then convert surplus Builders into repeated loaded-logistics pressure and
nearest-home defense.  v0046's fixed attackers were combat-only for life.  The
candidate tested one phase-aware role contract rather than another numeric
opening knob: a fixed attacker could temporarily enter the existing
Harvester/CHAIN FSM during opening or recovery, finish any chain it started,
and return to the existing attacker lane once pressure was live.

The audit also found that the official source architecture is not drop-in
compatible with this branch: a direct v14 Sporks screen was 0-15 with many
no-delivery games (`reports/iter-role-contract-v349-sporks-screen-seed173-analysis.json`).
The implementation therefore adapted the role/task idea without importing its
Store schema or Core policy.

## Scope and implementation

Allowed production scope was `bots/candidate/main.py`,
`bots/candidate/bot/defender.py`, `bots/candidate/bot/dynamic.py`,
`bots/candidate/bot/attacker.py`, and one focused role/task test.  The first
candidate lent both fixed attackers while the route count/phase was below the
pressure threshold.  Repair 1 preserved a continuous primary pressure lane
and attempted to lend only the Core-designated second attacker.  Replay/source
inspection showed that the Core does not designate that second attacker until
three completed routes, so this branch was effectively inactive.  Repair 2
made the primary a local route owner only before three routes and until
confirmed enemy-core intel, and skipped hijack/turret detours while that route
mission was active.

Store schema, Core spawn policy, fixed identities, immutable snapshots,
package, platform, live state, and deployment were non-goals and were not
kept.

## Validation

- Focused role/phase/seeded-route coverage was **11/11** for the initial
  candidate and **12/12** for each repair.  Rollback focused coverage was
  **31/31** for the inherited economy/nearest suite.  Compileall passed for
  every candidate and rollback.
- The inherited `make static` profile remained exit 2: 15 obsolete candidate
  module imports and two navigation fast-path assertions.  No new static
  failure was introduced.  Smoke was **4/4 command-clean** for every
  candidate and rollback.
- Initial screen (seed 172) was **3-12**, **68,400 vs 114,340 Ti**;
  delivery-clean, max p99/peak **1,306/5,164 us**.  Report:
  `reports/local-20260820T112204Z`.
- Repair 1 was **1-14**, **65,130 vs 97,790 Ti** on seed 172 and **8-7**,
  **77,190 vs 69,090 Ti** on seed 173.  Both were delivery-clean with zero
  TLE/suspicious rows; max p99/peak was **1,323/1,872 us** and
  **1,180/4,614 us**.  Reports:
  `reports/local-20260820T112553Z` and `reports/local-20260820T112751Z`.
- Repair 2 was **7-8**, **57,610 vs 93,780 Ti** on seed 172 and **6-9**,
  **64,010 vs 77,710 Ti** on seed 173.  The seed-172 rotation had one
  baseline no-delivery row; candidate rows were otherwise delivery-clean,
  with zero TLE/suspicious output.  Max p99/peak was **1,305/5,496 us** and
  **1,318/2,239 us**.  Reports:
  `reports/local-20260820T113409Z` and `reports/local-20260820T113555Z`.

## Decision and rollback

Reject v349 after the two permitted repairs: neither rotation produced a
repeatable aggregate win-rate or conversion edge, and the best repair had a
large collection deficit.  Restore candidate production source byte-for-byte
to immutable v0046; proof is the empty
`reports/iter-role-contract-v349-rollback-source-parity.diff`.  Rollback
compileall passed, rollback focused checks passed, inherited static remained
exit 2, and rollback smoke was **4/4** at
`reports/iter-role-contract-v349-rollback-smoke.log`.

No release gate, promotion, package, upload, activation, or live transition
occurred.  Local baseline remains immutable v0046; live v108 remains
`active_observing` with v107 as the known-good rollback target.

## Remaining risk and next direction

The role contract was too coarse for this workforce: borrowing a fixed
attacker either removed too much early pressure or failed to add enough route
throughput.  The next experiment should not retry this handoff unchanged.
Use the top-team evidence to design a true per-Builder mission scheduler with
explicit route-owner completion, visible loaded-logistics raid fallback, and
nearest home-defense response, while preserving map coverage and protected
map gates.  Do not alter the Store schema or Core spawn policy until a local
role/task candidate demonstrates a repeatable edge.
