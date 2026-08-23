# v328 compact-map early Sentinel

## Objective

Test the other top-team opening family: on genuinely compact maps, allow one
reserve-backed forward Sentinel before the first completed route; keep the
existing route-payback gate on open maps. The reserve covered one Harvester and
two short Conveyor links at dynamic prices.

## Scope

Production: `bots/candidate/bot/attacker.py`. Focused coverage extended
`tests/test_candidate_v319_launcher.py`. The baseline was immutable
`bots/versions/v0045_opening-launcher-relay_20260820-0229_eeafad8f`.

## Evidence and decision

- Focused coverage: 42/42; compileall passed; smoke 4/4.
- 15-map screen: 5-10, command-clean, report
  `reports/local-20260820T034059Z`.
- Replay diagnostics: `reports/iter-v328-early-control/`.

Reject v328. Compact-map Sentinel counts rose, but the extra early spend did
not convert into wins and materially trailed v0045. The temporary gate and
tests were removed; candidate production parity with v0045 is zero. No
release, upload, activation, or live-state transition occurred.
