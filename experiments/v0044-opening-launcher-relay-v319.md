# v319 opening Launcher relay

## Parent and hypothesis

Parent: immutable `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`.

Top-team replay inspection showed a control-first opening that establishes a
Launcher almost immediately, then uses it as a mobility/control primitive while
the economy comes online.  Live v107 losses showed the opposite failure shape:
builders spent the opening walking or trailing disconnected belts while enemy
control units reached the home corridor.  The hypothesis was that one
reserve-backed home Launcher owned by the primary attacker would convert that
opening mobility gap without replacing the proven economy FSM.

The opening timing and unit mix came from
`reports/iter-v306-architecture-audit/top-team-opening-analysis.json` and
`reports/top-teams-20260815-analysis.json`; the live counterexamples came from
`reports/live-v107-refresh/analysis.json`.

## Scope

Production changes were limited to `bots/candidate/main.py` and
`bots/candidate/bot/attacker.py`.  Focused coverage was added in
`tests/test_candidate_v319_launcher.py`.  The change adds a real Launcher
dispatch lifecycle: a designated primary attacker can build at most one
dynamic-price Launcher while in SCOUT near home, preserving one Harvester and
two Conveyor costs; the Launcher first ejects a nearby enemy Builder away from
our Core, otherwise it throws only a designated fixed attacker to a bounded
strict-progress destination toward the enemy Core.  Every build and launch is
guarded by its matching `can_*` call, and scans/destination search are bounded.

Non-goals were Store/schema, route construction, source selection, workforce or
task policy, Sentinel/Barrier/Gunner behavior, baseline snapshots, package,
upload, activation, and live state.

## Evidence

- Focused launcher plus nearest-defense/seeded-route/economy coverage: **40/40**
  (`reports/iter-v319-opening-launcher/focused.log`).
- Candidate compileall: pass (`reports/iter-v319-opening-launcher/compileall.log`).
- `make static`: inherited exit 2 from 15 obsolete removed-module imports and
  two navigation fast-path assertions; no new launcher failure
  (`reports/iter-v319-opening-launcher/static.log`).
- Smoke: **4/4 command-clean**
  (`reports/iter-v319-opening-launcher/smoke.log`).
- Rotated 15-map screen: **7-8 candidate-A**, command/delivery-clean, versus
  the frozen v0044 screen's **4-11**; collection **88,610/94,020 Ti**
  (`reports/local-20260820T020932Z`, analysis in
  `reports/iter-v319-opening-launcher/replay-analysis.json`).
- Full 60-game map/seed/side gate: **36-24 candidate wins**, collection
  **304,340/255,830 Ti**, no map at 0-4, and zero TLE/suspicious rows
  (`reports/local-20260820T021233Z`, analysis in
  `reports/iter-v319-opening-launcher/release60-analysis.json`).
- Candidate Launchers appeared in all 60 gate games at turn 2; first delivery
  and Harvester counts remained live and map-dependent rather than being
  hard-coded.

## Decision and risks

Retain v319 as the strongest local candidate after the release gate.  It is a
structural improvement over v0044, not a tuning-only change, and is not
rolled back.  It is not uploaded or activated in this checkpoint because
platform operations are outside this iteration's scope.  Remaining risks are
that the fixed one-relay policy may spend early titanium on maps where v0044
already had a strong opening, and that Launcher throws are not yet context-
aware of route ownership or defensive task state.  Any next experiment should
start from this retained candidate and change one distinct control/economy
contract at a time.
