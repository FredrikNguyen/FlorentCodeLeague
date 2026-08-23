# v211 — delivery-confirmed route milestone (approved)

## Gate context and replay diagnosis

The current unpromoted candidate produced a promising seed-175 screen (**10-5**)
and therefore ran the complete 60-game endpoint-seed/both-side gate against
exact v0042. The gate was **28-32** candidate-side, command-clean with zero
TLE/suspicious rows, collection **279,380 vs 300,630 Ti**, candidate first
delivery mean **38.54 vs 54.42** among delivered games, and one candidate
no-delivery row versus zero for v0042. Max p99/peak were **1,562/5,475 us**.
Full reports are `reports/local-20260818T155712Z`,
`reports/iter-v211-release-gate-replay-analysis.json`, and
`reports/iter-v211-release-gate.log`. Keep v0042 baseline; do not promote.

The parallel Luna replay audit found three recurring loss shapes: delayed first
delivery on Glacierkeep/Drakkarfjord, conversion deficits and extra Gunners,
and collection plateaus after a geometric route completion on Icefloe/Drumlin/
Archipelago/Drakkarfjord. The likely causal contract is that
`defender._end_chain(success=True)` publishes `SLOT_HARVESTER_COUNT` from
geometry before the terminal sink has carried resource. Evidence and the
proposed scope are in `experiments/.tmp-v211-replay-audit/audit.md`.

## Implementation result

The Luna implementation added the bounded local VERIFY state, exact terminal
identity/Core-facing validation, delayed existing-slot publication, and an
eight-round timeout. Focused verification coverage was **5/5** after a
same-round idle-fallback guard; the root regression subset was **45/45** and
candidate compileall passed. `make smoke` remained **4/4**; `make static`
retained the inherited exit 2 (obsolete deleted-module imports and two
navigation fast-path assertions), with no new verification-specific error.

The fair edited seed-176 all-map screen was **3-12** against exact v0042,
15/15 command-clean, delivery-clean, and had zero TLE/suspicious rows. It
collected **52,520 vs 89,840 Ti**, with mean first delivery **23.93 vs 23.20**
rounds and max p99/peak **1,291/2,327 us**. This is decisively negative and did
not meet the positive-screen gate; the partial interrupted run is retained at
`reports/local-20260818T161619Z`, and the complete edited run is
`reports/local-20260818T161743Z` with reduction
`reports/iter-v211-verify-milestone/edited-screen-replay-analysis.json`.
The exact pre-v211 snapshot was restored and the temporary test/config were
removed. v211 is rejected; no 60-game gate, promotion, package, upload,
activation, or live-state transition occurred.

## Approved bounded hypothesis

After a geometric chain finish, keep that local Builder in a six-to-eight-round
VERIFY phase. Inspect the already-visible terminal/Core-ring Conveyor using
existing stored-resource APIs; publish the existing Harvester milestone only
after a nonzero sink observation. On timeout, return to existing route/repair
behavior without cleanup, chain rewrite, or new coordination. Continuous
offense is explicitly queued as a separate follow-up after this phase clears a
paired screen.

Allowed production files are `bots/candidate/main.py` and
`bots/candidate/bot/defender.py`, plus one focused verification test and one
timeout constant if necessary. No Store schema/slot reuse, lease, Launcher or
Sentinel selector, offense-priority rewrite, economy/geometry/map branch,
baseline/archive/package, upload, activation, or live-state change.

## Done criteria

Focused tests must cover delayed existing-slot publication, positive sink
confirmation, timeout, and one-round Store visibility; compileall/static/smoke
must retain the inherited profile. The rotated 15-map screen against exact
v0042 must be command-clean, add no no-delivery row, keep first delivery within
two rounds of v0042, and remove the post-milestone false-progress signature on
at least three plateaued maps. Run the 60-game gate only after a clear paired
screen edge; otherwise restore exact pre-v211 parity.
