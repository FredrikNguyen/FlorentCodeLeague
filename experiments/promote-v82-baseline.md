# Promote platform v82 as local baseline

## Decision

Promote the downloaded active platform v82 bot to the immutable repository
baseline for future comparisons. Keep platform v72 as the live rollback target;
this local baseline change does not alter live activation.

## Evidence

- Active platform: v82, ready and active.
- Live window: 7 series, 25-10 games, raw score 0.7143, opponent-adjusted
  residual +0.1520, net +34.05 Elo, rank 53.
- Live replay audit: 183,030 candidate calls, zero candidate TLEs or suspicious
  outputs, p99 0.735 ms, peak 1.474 ms;
  `replays/live-v82` and `reports/live-observe-20260811T212328Z`.
- Local comparison against the former working candidate: 34-20 and
  149,030-146,450 titanium over 54 regression games, zero command failures;
  `reports/local-20260811T212700Z`.
- Baseline smoke: 4/4 command-clean;
  `reports/local-20260812T011209Z`.
- `make static` was rerun and retained the repository's inherited 14 obsolete
  API/navigation import failures plus two known contract failures; full log:
  `reports/baseline-promotion-static.log`.
- Source archive: `artifacts/submissions/live-v82.zip`, SHA-256
  `ea5d6b06fc9d2a73b4723c1616fd9d81bdf03e232aafc87910426706f2e2722d`.

## Limits

The live sample is below the 12-series observation minimum, so v82 is the
current local baseline and provisional live winner rather than a statistically
final promotion. Continue observing v82 and retain v72 for rollback.
