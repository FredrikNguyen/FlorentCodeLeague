# v255 ultra-cramped continuous pressure — rejected after one repair

## Replay basis and objective

The fresh v106 ladder snapshot showed a specific compact-map failure against
the higher-rated `arsonist duck` (match
`2a0d4a97-d6a3-466b-9f8b-250dbe0af39e`): on the 10x10 game our side delivered
at round 62 and placed zero Sentinels, while the opponent placed four and
destroyed our Core. The other four games in that series and the recent
20x20/30x30 samples did not show the same zero-Sentinel opening. This was
treated as a map-context pressure hypothesis, not a restart of the rejected
global offence-pulse or guessed-Core families.

## Bounded implementation

The candidate temporarily added one geometry threshold and a single
pre-route gate in `attacker.py`. Only the core-designated primary attacker
could buy one first Sentinel on an ultra-cramped board (ordinary mirrored-Core
distance plus maximum side 12), and only with a visible friendly Harvester and
dynamic-price liquidity for a Harvester, two Conveyors, and a cramped reserve.
The normal facing, `can_*`, site blacklist, route marker, and later pool gates
were unchanged. Focused coverage was **30/30**, candidate compileall passed,
`make static` retained only the inherited 15 obsolete-module imports and two
navigation fast-path assertions, and smoke was **4/4** at
`reports/local-20260819T054956Z`.

The 15-map screen at seed 172 was command/delivery-clean at **8-7**,
collection **63,720 vs 48,080 Ti**, zero TLE/suspicious rows, and max
p99/peak **1,434/4,829 us**. Because the one-order edge was not causal, the
side-swapped 30-game screen was run. It scored **16-14**, collection
**126,750 vs 113,370 Ti**, with one candidate no-delivery row (Fjordgate),
zero TLE/suspicious rows, and max p99/peak **1,368/4,922 us**. Map floors
included candidate **0-2** on Antler, Icefloe, and Valkyrie.

## Bounded repair

The only repair doubled the post-Sentinel cramped reserve while retaining all
other gates. Focused coverage remained **30/30**, compileall passed, static
retained the inherited profile, and smoke was **4/4** at
`reports/local-20260819T055758Z`. The repair side-swapped screen fell to
**14-16**, collection **124,720 vs 137,430 Ti**, with no candidate
no-delivery row but one comparator no-delivery row, zero TLE/suspicious rows,
and max p99/peak **1,549/2,706 us**. It still had candidate 0-2 floors on
Auroraveil, Drakkarfjord, and Drumlin. No release gate was justified.

## Decision and rollback

Reject v255. The narrow compact pressure edge did not survive side order, and
the reserve repair removed the candidate's only modest edge while lowering
collection. The temporary attacker/constants/test edits were removed. Exact
candidate parity with immutable v0043 is zero in
`reports/iter-v255-live-replay-audit/rollback-source.diff`; rollback focused
coverage was **26/26**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T060314Z`. No release gate, package, remote gate,
upload, activation, promotion, or live-state transition occurred.

## Evidence and follow-up

Live match metadata and replay downloads are under
`reports/iter-v255-live-replay-audit/`; the v106 snapshot is
`reports/live-manual-20260819T054455Z`. Keep v0043 active and close this
continuous-offence variant. A future offence hypothesis needs a causal
conversion or defense transition that is observable on both side orders, not
another pre-route Sentinel spend gate.
