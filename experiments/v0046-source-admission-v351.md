# v0046 opening source-admission — v351 rejected

Date: 2026-08-20

## Objective and live basis

The fresh platform-v108 Askar City loss was reliability-clean but exposed an
economic conversion problem: on several maps the bot kept 31–60 Conveyors and
only 1–3 Harvesters, including an Auroraveil game with no titanium delivery.
The first local source at `(13, 7)` had a visibly blocked Core-facing outlet,
so v351 tested whether an opening Builder should prove a local exit before
committing to the Harvester and long chain.

## Scope

The candidate-only scope was `bots/candidate/bot/defender.py` plus the
temporary focused `tests/test_candidate_source_admission.py`.  It did not
alter the Store, Core spawn/phase policy, fixed roles, attacker/dynamic logic,
immutable v0046, package, platform, or live state.  The implementation used
only visible, adjacent source facts; it did not retain a reservation or run
the rejected v343 visible-corridor BFS.

## Results

- Initial two-cell source runway admission passed focused coverage **39/39**,
  compileall, and smoke **4/4** (`reports/local-20260820T123111Z`).  Its
  v0046-pinned all-map seed-172 screen was only **5-10**, despite 15/15
  candidate deliveries and zero command/TLE/suspicious failures.  It collected
  103,960 vs 100,910 titanium, showing that extra path spending was not a
  win-rate edge.  The report is `reports/local-20260820T123157Z`; analysis is
  `reports/iter-v351-source-admission-screen-seed172-analysis.json`.
- Replay review isolated an overly strict admission failure: on Ragnarok, the
  candidate delayed first delivery to turn **193** versus v0046's turn **10**.
  Repair 1 therefore accepted one legal Core-progressing exit while retaining
  immediate-block rejection.  Focused coverage was **40/40**, compileall and
  smoke were clean (`reports/local-20260820T123834Z`); static remained only
  the inherited 15 obsolete imports and two navigation assertions.
- Repair 1 restored Ragnarok first delivery to **9 vs 9**, but the same
  all-map seed-172 v0046 screen was still **7-8**, collecting 57,100 vs
  63,700 titanium.  All 15 candidate rows delivered and had zero TLE or
  suspicious output; max p99/peak was 1,149/2,088 us.  Evidence:
  `reports/local-20260820T123902Z` and
  `reports/iter-v351-source-admission-repair1-screen-seed172-analysis.json`.

## Decision and rollback

Reject v351 after the replay-backed repair.  The current visible BFS already
avoids impassable first moves; adding a source-side admission rule delayed or
redirected too many otherwise productive openings.  Neither screen reached
the required **9-6** threshold, so there was no rotated screen, 60-game
matrix, remote gate, package, upload, activation, or promotion.

Candidate production source was restored exactly to immutable v0046.  The
recursive parity proof (excluding generated caches) is the empty
`reports/iter-v351-final-source-parity.diff`.  Rollback focused coverage was
**35/35**, compileall passed, and smoke was **4/4** at
`reports/local-20260820T124302Z`.

## Next risk

Do not retry opening source admission, same-direction runway checks, staging,
or an opening-direction override as a variation.  The remaining live problem
is post-source conversion: determine from replay evidence why completed-looking
chains do not retain Harvester capacity or turn into pressure at the right
time, without rewriting ordinary chain geometry or reusing the rejected route
verification family.
