# v224 infiltration containment audit — completed; v225 rejected

## Objective

Separate enemy Builder infiltration defense from our own counter-infiltration
using saved replay positions before changing production code. The audit was
intended to identify a causal gap that was not a repeat of the rejected v143
local route-sentry or the v198/v208 Launcher/ejection loops.

## Inputs and method

The read-only parser in `scripts/analyze_replay.py` was used to produce
`reports/iter-v224-infiltration-audit/summary.json`. A route entry is a Builder
within squared distance 2 of a live Harvester/Conveyor/Splitter; a Core entry
is within squared distance 25 of the opposing Core. The response proxy is the
first opposing Builder movement strictly after an entry within Chebyshev
distance 2. Replay positions do not reveal whether a Builder attacked, built,
hijacked, or was intentionally assigned to respond, so these are proxies rather
than causal labels.

## Evidence

- Saved v84-loss/top-team sample, side A: route pre-delivery in **2/13** games,
  median route-response proxy **22** rounds; side B: **1/13**, median **19**.
- Saved top-team sample, route pre-delivery was **2/15** for each side; route
  response medians were **6** (A) and **14** (B). Core pre-delivery entries were
  absent for A and present in only **2/15** B games.
- Rejected v223 screen: candidate route pre-delivery in **6/15** games,
  response median **34**; v0042 comparator **5/15**, median **27**. This was
  recorded before the exact v0042 rollback and is not promotion evidence.

## Decision

The evidence supports protecting the opening route before fixed-attacker
infiltration, not a broad route-sentry response. v225 therefore tests one
attacker-owned midline lease: before the first completed Harvester chain, a
fixed attacker cannot cross toward the enemy Core; compact maps retain their
existing exception, and the existing post-chain Sentinel/Core/sabotage policy
is unchanged. No dynamic threat detector, Store change, Launcher loop, or
route rewrite is included.

## Limitations and risks

The samples are small and side identity is not a perfect proxy for one exact
bot revision. The route-radius detector can include a Builder merely passing
through logistics, and the response proxy can credit an unrelated movement.
The midline lease may give up useful early pressure on cramped or asymmetric
maps, so a rotated 15-map screen must be command/delivery-clean and protect
map floors before any release gate.

## v225 implementation outcome

The queued attacker-only lease was implemented and tested. Before the first
completed Harvester chain it kept the fixed attacker on its geometric own
half, while preserving the cramped-board exception and existing post-chain
policy. One bounded repair released the lease after confirmed enemy-Core
intel, so a stalled route could not hold offense forever.

- Initial focused coverage: **6/6** new tests and **33/33** focused subset;
  compileall pass; static inherited; smoke **4/4**.
- Initial screen: **9-6**, delivery-clean, **98,490 vs 71,020 Ti**; zero
  TLE/suspicious rows. Release gate: **29-31**, **239,120 vs 268,690 Ti**,
  delivery **58/60 vs 59/60**, Drumlin **0-4**.
- Confirmed-intel repair: focused **6/6** new and **33/33** subset,
  compileall pass, static inherited, smoke **4/4**; screen **5-10**,
  delivery-clean, **63,740 vs 76,780 Ti**. No second repair was attempted.

## Decision and rollback

Reject v225. Both the initial release gate and the one repair failed to show a
reliable improvement; the repair was materially worse. The temporary lease and
test were removed. Candidate `attacker.py` is byte-identical to v0042
(`afa559f98a0694ab6c3355538098a0c845768413652124e08fc9b1035487a01a`).
Rollback focused coverage was **27/27**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260818T201638Z`. No promotion, package,
upload, activation, or live transition occurred.

## Status

v224 audit complete; v225 implementation rejected; v0042 remains the
immutable baseline. Preserve the replay evidence and choose a different
causal hypothesis before the next source edit.
