# Review platform submissions v83-v85

## Scope

Read-only review of ready platform versions v83, v84, and v85 against the v82
baseline. No upload, activation, rollback, or source edits were performed.

## Live evidence

- v82: now 14 series, 43-27 games, raw 0.6143, adjusted +0.07851, net +35.17
  Elo; this remains the strongest supported live baseline.
- v83: 3 series, 10-5 games, raw 0.6667, adjusted +0.17065, net +16.38 Elo.
  Candidate-side replay audit: zero TLEs/suspicious output; opponent had 2,238
  TLEs. Evidence: `reports/live-observe-20260812T011509Z` and
  `replays/live-v83`.
- v84: 1 series, 2-3 games, raw 0.4, adjusted +0.05646, net +1.81 Elo.
  Candidate-side replay audit: zero TLEs/suspicious output; opponent had 13
  TLEs. Evidence: `reports/live-v84` and
  `reports/live-observe-20260812T011509Z/live-v84-decision.json`.
- v85: no live series yet; no live performance evidence. Its local report has
  repeated `OverflowError: out of range integral type conversion attempted`
  markers in 51/54 games despite zero process return codes; the 0-54 result is
  therefore a hidden runtime-failure rejection, not a strategic loss.

## Local comparison against v82

- v83: 33-21 games, 118,150-80,950 titanium;
  `reports/local-20260812T011619Z`.
- v84: 34-20 games, 107,640-72,540 titanium;
  `reports/local-20260812T012008Z`.
- v85: 0-54 games, 0-49,300 titanium, with 51/54 games containing the
  `OverflowError` marker; immediate rejection;
  `reports/local-20260812T012143Z`.
- All local runs completed 54/54 process commands. Candidate-side replay audits
  found zero TLEs and suspicious output, but v85's captured stderr contains the
  OverflowError markers described above.

## Decision

Keep v82 as baseline. v84 is the current local challenger by one game over v83,
but its live sample is only one series; v83 has a better early live residual but
only three series. Do not promote either until a larger live/local confirmation
supports the gain. Reject v85 because its local process-clean result masks
repeated OverflowError runtime failures; reconsider only with a corrected source.
