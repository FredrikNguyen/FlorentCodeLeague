# v207 — fresh Launcher/unit-control replay audit

## Scope

Read-only audit after v206. No candidate source, baseline, package, platform,
or live-state files were changed. Inputs were the 15 saved high-ranking
replays and the v206 repair seed-171 screen.

## Findings

- High-ranking winners placed Launchers in **8/15** games and averaged **3.27**
  Launchers, versus **2/15** and **0.40** for paired losers. Winner means were
  **5.0 Harvesters, 13.7 Barriers, 3.6 Sentinels**, and first delivery round
  **21.1**; loser means were **3.1, 8.9, 0.9**, and **276.5** (the latter
  includes no-delivery games as 999).
- The compact replay encoding's update field 16 contains an actor id and a
  two-coordinate Builder position event. It does not expose an unambiguous
  Launcher action record in these files. Field-16 movement volume therefore
  cannot be used to claim that a Launcher fired.
- On the v206 seed-171 repair screen both candidate and v0042 placed **zero
  Launchers**. The candidate's mean field-16 position-event count was 104.4
  versus 122.1 for the comparator, but candidate first delivery included one
  no-delivery row (mean 94.1 with that row mapped to 999) versus 29.7. The
  movement difference is not causal evidence.

Report: `reports/iter-v207-launcher-lifecycle-audit.json`.

## Causal conclusion

The repeatable gap is not another Barrier priority: the strongest winners have
a real Launcher lifecycle, while v0042 never creates or runs one. Earlier v198
and v200 selectors were late or diverted opening liquidity, so the next source
hypothesis must implement a lifecycle-safe Launcher unit (build, legal pickup,
destination progress, cooldown, and failure recovery) behind a proven delivery
reserve, with instrumentation based on observed placements/actions rather than
an inferred replay field.
