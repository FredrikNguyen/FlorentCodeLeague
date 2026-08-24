# Evaluation

Candidates are compared directly with the frozen `bots/baseline/` using the
same maps and deterministic seeds. Game win rate is the primary metric;
reliability failures override aggregate results.

## Gates

### Static

```bash
make check
```

This runs Ruff, focused unit tests, submission contract checks, and Python
compilation over the maintained source.

### Smoke

```bash
make smoke
```

Four quick games verify that both bot trees load, commands complete, and the
configured 10 ms limit is respected.

### Regression screen

```bash
make eval-regression
```

The screen selects one reproducible map/seed pair for each of the 15 configured
maps. Rotating `screen_seed` changes the selected seed without dropping map
coverage.

### Release matrix

```bash
make eval-local
```

The release matrix runs all 15 maps with endpoint seeds `1` and `101` in both
side orders: 60 games total. This is the primary local promotion gate.

### Remote gate

```bash
make remote-gate
```

The remote gate uses the official server test command on representative maps.
It should run only after local gates pass because account quotas apply.

## Decision rules

A candidate is promotable when it has a material direct win-rate advantage and
no systematic reliability defect. Record and inspect:

- wins, losses, draws, and side-order splits;
- command failures, exceptions, suspicious output, and TLE evidence;
- first delivery and games with no delivery;
- titanium collected and surviving economy/combat units;
- map-specific regressions and replay-visible causes.

One or two localized map regressions may be acceptable when the direct aggregate
gain is clear. Crashes, repeated timeouts, invalid actions, or severe delivery
collapse block promotion regardless of win rate.

Generated JSON, logs, and replays are written below `reports/` and `replays/` and
are intentionally not tracked.
