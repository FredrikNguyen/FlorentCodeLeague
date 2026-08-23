# v0049 map-context enemy-core targeting

## Objective

Test whether the fixed map set's non-universal core symmetries explain the
missing forward sentinels and losses on Strait, Sweden, Twins, Vase, Bridge,
Longship, and Showdown.

## Scope

The experiment was limited to `bots/candidate/bot/attacker.py` and the focused
nearest-defense test. The immutable comparator was
`bots/versions/v0030_loaded-raid-best_20260814-1109_eeafad8f`.

## Variants and evidence

1. A dimensions/core-anchor catalog plus a corrected 2x2-footprint mirror was
   reliability-clean but tied v0030 at 31/54. Report:
   `reports/local-20260814T143306Z`; analysis:
   `reports/iter-core-context-v0030-focused-replay-analysis.json`.
2. Allowing pre-vision sentinel placement only for cataloged counterparts
   regressed to 25/54. Report: `reports/local-20260814T144117Z`; analysis:
   `reports/iter-core-context-v0049-focused-r2-replay-analysis.json`.

Both variants had zero command failures, TLEs, suspicious output, and no
no-delivery rows. The second variant's maximum p99 callback was 1,419 us and
peak callback was 2,913 us.

## Decision

Rejected after two bounded variants. All temporary source and test edits were
removed; the candidate Python tree is byte-identical to v0030. Revert evidence
is in `reports/iter-core-context-v0049-revert-*`. No full matrix, package,
upload, activation, or baseline transition was performed.

## Follow-up

The edge-map sentinel deficit is not explained by target coordinates alone.
Any future placement/path hypothesis must preserve the v0030 baseline and prove
an improvement on the focused gate before a full matrix is allowed.
