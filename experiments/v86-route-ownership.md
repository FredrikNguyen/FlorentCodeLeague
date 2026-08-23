# v86 route ownership

## Scope and hypothesis

Base the mutable candidate on the current platform v86 download
(`artifacts/submissions/live-versions/v86.zip`, SHA-256
`54ff398a2f7cde0d2082e138513704a898d86359a213cc5b872fd4c4d5efdf6c`).
Live loss and top-team replay review showed that raw worker-count expansion
caused route contention; a local closest-worker, then lowest-id ore owner
should stop duplicate harvest attempts without needing an additional delayed
Store claim slot.

## Evidence reviewed

- v84's 2-3 loss to Ouroboros: v84 placed 6-8 Harvesters but also 220/415
  Gunners on the two titanium-tiebreak losses; the opponent held 4-5 working
  Harvesters and collected 11,980/11,340 Ti.
- Sporks' 5-0 against Erebus and Clankers' 4-1 against Sporks: winners
  consistently fielded 5-23 Builders, 4-28 Harvesters, connected conveyors,
  and defeated every game by core destruction. Analysis:
  `reports/v84-losses-top-team-replay-analysis.json`.
- v86 already adds core-siege healing, idle fallback, staged spawning, and a
  one-sentinel early pool. Direct v86 versus v84 was 31-23, command-clean:
  `reports/local-20260812T013508Z`.

## Rejected workforce variants

- Five → eight → ten worker staging: 28-26 and 1.0705x Ti against v86;
  `reports/local-20260812T014225Z`.
- Five-worker opening alone: 26-28 and 0.9247x Ti against v86;
  `reports/local-20260812T014737Z`.

Both variants increased contention rather than productive route coverage.

## Retained change

`bots/candidate/bot/defender.py` now yields a visible ore to a closer friendly
economic Builder, resolving equal distance by lower entity id. Permanent
attackers are explicitly excluded, since they do not build Harvesters. The
guard is local and visibility-bounded, avoiding Store write-delay races.

## Validation

- Compileall: passed.
- Smoke: 4/4 command-clean; `reports/local-20260812T020254Z`.
- Route ownership versus v86: 30-24, 1.0243x Ti, zero TLE/suspicious output;
  `reports/local-20260812T015229Z`. This is supportive but not itself a
  promotion margin; sweden regressed 1-5.
- Direct versus v84 after the attacker exclusion repair: 38-16, 1.5988x Ti,
  54/54 command-clean, zero replay TLE/suspicious output, p99 <= 1.055 ms,
  peak <= 3.606 ms; `reports/local-20260812T020304Z` and
  `reports/v86-route-ownership-v84-final-replay-analysis.json`.
- Earlier direct confirmation before that repair: 36-18 and 35-19; these
  support the direction but are not substituted for the repaired final run.

## Release gate and platform submission

The full local release matrix completed 210/210 command-clean games: 159-51,
526,580-310,950 titanium (1.6935x), zero replay TLE/suspicious-output events,
maximum p99 1.220 ms and peak callback 4.969 ms. Report:
`reports/local-20260812T021018Z`. The five-map remote gate completed 3-2 for
the candidate (match `4e859320-2a29-4396-9690-a6d5425b56fd`):
`reports/remote-20260812T021052Z`.

The frozen package is
`artifacts/submissions/v0021_v86-route-ownership_20260812-0218_eeafad8f.zip`
(SHA-256 `7c89830c150e22f6fc9e4b0434d04d68b57cd530236610c556a22e11aa19774f`).
It uploaded as platform v88, `v0021-v86-route-ownership-eeafad8f`. The
platform reported v88 active immediately after upload; its captured state is
`reports/live-observe-20260812T021908Z`. v87 remains the prior active version
and v72 the known-good rollback target.

## Remaining risks

`make static` remains blocked by 14 legacy tests importing the removed
pre-v86 architecture, although the focused source-contract suite passes. The
exact repaired candidate's earlier v86 comparison was only 30-24 and regressed
on sweden, so observe v88 through the 12-series minimum and do not promote it
over the known-good rollback target without v86-native tests and fresh live
evidence.
