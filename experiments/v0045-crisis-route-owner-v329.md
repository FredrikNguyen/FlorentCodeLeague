# v329 — permanent Defender crisis route owner (rejected)

## Objective and scope

Remote v108 losses still showed a structural conversion failure after the
opening Launcher relay: the permanent economy Builder kept exploring while
Core income was quiet, so no unit owned a bounded route-health recovery pass.
This experiment gave only the permanent Defender a crisis-phase homeward sweep.
It reused the existing orphan reconnect, belt repair, Core-ring, heal, and
navigation gates; no new Store slot, spending rule, unit type, role assignment,
or combat policy was added.  Production scope was `bots/candidate/bot/defender.py`
with focused coverage in `tests/test_candidate_nearest_defense.py`.

## Validation

- Focused route/defense/launcher/economy coverage passed **42/42**;
  `reports/iter-v329-crisis-route-owner/focused.log`.
- Candidate compileall passed and smoke was **4/4** at
  `reports/local-20260820T035001Z`; the static check retained only the known
  inherited stale imports and two navigation fast-path assertions
  (`reports/iter-v329-crisis-route-owner/static.log`).
- The rotated 15-map screen was **9-6 candidate-A**, command-clean, with one
  candidate no-delivery row; `reports/local-20260820T034822Z` and
  `reports/iter-v329-crisis-route-owner/replay-analysis.json`.
- The 60-game local gate was **34-26 candidate-A**, command-clean, with zero
  TLE/suspicious rows and max p99/peak **1,390/5,912 us**;
  `reports/local-20260820T035034Z` and
  `reports/iter-v329-crisis-route-owner/release60-analysis.json`.
- The required remote five-game gate was **2-3 candidate-A** in match
  `7487346c-f8ce-4f6d-bcbd-250a24099d01` (`rated:false`), report
  `reports/remote-20260820T035633Z`.  Replay diagnostics are in
  `reports/iter-v329-crisis-route-owner/remote-replay-analysis.json`.
  Losses included a long 10x10 game where the candidate had an early delivery
  but ended with one live Harvester versus the opponent's two, and a 16x16
  game where the candidate collected 2,200 Ti versus 3,650 Ti for the winner.

## Decision and rollback

Reject v329.  The local edge did not transfer to the remote gate, and the
crisis owner did not solve route survival or pressure conversion.  The
temporary Defender method/imports and focused tests were removed; recursive
candidate production parity with immutable v0045 is zero.  No package, upload,
activation, promotion, or live-state change was made.  v0045 remains the local
baseline and platform v108 remains guarded `active_observing`.

## Remaining risk

The decisive gap is not a missing crisis callback but insufficient coordinated
front pressure: top-team winners sustain multiple Launchers, Sentinels, and
Barriers while converting routes.  The next experiment must change offensive
unit ownership/relay behavior, not repeat a global homeward pull.
