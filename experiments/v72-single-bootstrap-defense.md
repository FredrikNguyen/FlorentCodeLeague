# v72 single bootstrap defense

## Scope

- Parent: `bots/versions/v0014_canonical-opening_20260809-1606_7dd72f03`.
- Hypothesis: live opening collapses are amplified by several Builders buying
  independent emergency structures before the first producer; allowing one
  designated free Defender one bootstrap structure preserves a response while
  keeping the primary route and the rest of the workforce on economy.
- Changed runtime file: `bots/candidate/bot/builder.py`.
- Non-goals: no phase, route, workforce, navigation, post-income combat, or
  opening-orientation changes.

## Gate

- Focused tests prove only the first free Defender may build once before income,
  primary owners cannot build, and normal defense resumes after first income.
- Beat immutable v0014 on a paired current-map checkpoint with no command error,
  no new map collapse, and non-regressing aggregate titanium.
- Preserve smoke reliability and inspect the complete runtime diff before any
  release decision.

## Results

- Focused invariant/orientation tests: 9/9 passed before rejection; log:
  `reports/v72-single-bootstrap-defense/focused.log`.
- Six live-trouble-map checkpoint: 24-12, titanium 32,220 versus 30,120,
  command-clean; report: `reports/local-20260809T183033Z`.
- Full current-pool seed-1 checkpoint: 14-16, titanium 63,050 versus 77,470
  (ratio 0.8139), command-clean; report: `reports/local-20260809T183503Z`.
- New 0-2 collapses on `hive`, `jackpot`, `lighthouse`, and `snowflake`
  violated the widening gate.

## Status

Rejected. The candidate runtime was restored exactly to immutable v0014.
