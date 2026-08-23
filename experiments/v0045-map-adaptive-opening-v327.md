# v327 map-adaptive opening handoff

## Objective

Test a structural opening profile inspired by top-team replays: on open maps,
temporarily let the permanent primary attacker run the Defender route FSM until
the first completed Harvester chain; retain the v319 Launcher/control opening
on compact maps. A repair required two visible local ore deposits before the
handoff.

## Scope

Production: `bots/candidate/bot/attacker.py`. Focused coverage extended
`tests/test_candidate_v319_launcher.py`. The baseline was immutable
`bots/versions/v0045_opening-launcher-relay_20260820-0229_eeafad8f`.

## Evidence and decision

- Focused coverage: 43/43; compileall passed; smoke 4/4.
- Initial 15-map screen: 7-8, command-clean, report
  `reports/local-20260820T033316Z`.
- Ore-density repair screen: 6-9, command-clean, report
  `reports/local-20260820T033652Z`.
- Replay diagnostics: `reports/iter-v327-map-adaptive-opening/`.

Reject v327. The borrowed route owner delayed or reduced conversion on several
open maps despite improving a few first-delivery rows. Both variants were
removed; candidate production parity with v0045 is zero. No release, upload,
activation, or live-state transition occurred.
