# Rejected: v72 defense plus narrow route-owner guards

## Hypothesis

The promoted v72 defense behavior might be safer than v0015's close-contact
defense suppression while retaining the narrow 25x15 and 20x26 route-owner
continuity guards.

## Scope

- Runtime comparison changed only `bots/candidate/bot/builder.py` relative to
  v72: persistent post-income state plus the two exact geometry guards.
- `tests/test_candidate_bootstrap_defense.py` covered the guards.
- No navigation, economy allocation, offense, Store, or other geometry change.

## Evidence

- Focused: 1/1 passed; compileall and diff checks passed.
- `make static`: inherited API/line-cap failures only.
- Smoke: 4/4 command-clean; report `reports/local-20260809T223653Z`.
- Targeted versus v72: `nordkap` 10-0 and 34,100-1,950 titanium;
  `meander` 5-5 but 26,700-zero titanium; report
  `reports/local-20260809T223335Z`.
- Direct current-pool decision matrix versus packaged v0018: 90/90
  command-clean but 34-56 and 170,360-194,320 titanium. The candidate was 0-6
  on `fjordgate`, `heart`, `moonrise`, and `nordkap`. Across 1,616,734 calls
  there were zero TLE/suspicious-output signals, maximum p99 3.821 ms, and
  maximum callback 8.335 ms. Report: `reports/local-20260809T223713Z`.

## Decision

Rejected. The runtime regression is strategic and outweighs the narrow target
gains. Candidate source was restored exactly to immutable v0018; no package,
upload, or activation was created from this experiment.
