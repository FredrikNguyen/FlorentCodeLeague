# v0075 — route continuity after the fourth route

## Objective

Assign a visible broken route to the nearest free dynamic Builder, never
interrupt an in-progress chain owner, and restore pressure after the repair.
The Store protocol, path construction, combat targeting, and fixed roles stay
unchanged.

## Initial implementation

- Added deterministic nearest-distance and entity-ID ownership for visible
  repairs, excluding both fixed attackers and the permanent defender.
- Made a visible owned repair immediately preempt `RAID`, `ORE_DENIAL`, or
  `ADVANCE`, bypassing their ordinary commitment floor.
- Preserved the existing completed-raid-to-repair handoff and the `MODE_CHAIN`
  early return.

## Initial validation and decision

- Focused tests: **18/18 passed**
  (`reports/iter-route-continuity-v0075-focused.log`); compileall and
  `git diff --check` passed.
- `make static` retained the inherited exit-2 result from 15 obsolete-module
  imports (`reports/iter-route-continuity-v0075-static.log`).
- Smoke: **4/4 command-clean** (`reports/local-20260815T155825Z`; raw log
  `reports/iter-route-continuity-v0075-smoke.log`).
- 54-game screen versus v0034: **22-32**, 249,830 versus 275,210 collected
  titanium, zero no-delivery rows, zero command failures/TLE/suspicious output,
  max p99 1,331 us and peak callback 4,116 us
  (`reports/local-20260815T155900Z`; paired analysis
  `reports/iter-route-continuity-v0075/screen-paired-analysis.json`).
- Map results: Atoll 5-1, String 4-2, Aurora/Crossfire 3-3, Sweden/Vault 2-4,
  and Bridge/Longship/Sprint 1-5.

**Initial implementation rejected; no full matrix.** The broad immediate
preemption interrupts valuable active pressure. Repair attempt 1 retains
nearest repair ownership and the completed-raid handoff, but permits immediate
interruption only from the open-ended `ADVANCE` fallback. Active `RAID` and
`ORE_DENIAL` keep their normal commitment.

## Repair attempt 1

- Focused tests passed **19/19**; compileall and `git diff --check` passed.
  `make static` retained the inherited 15-import exit-2 result. Smoke was
  **4/4 command-clean** (`reports/local-20260815T160801Z`).
- The independent 54-game screen recovered to **29-25**, with 258,300 versus
  237,120 titanium (1.0893x), zero no-delivery rows, zero command
  failures/TLE/suspicious output, max p99 1,348 us, and peak callback 6,209 us
  (`reports/local-20260815T160833Z`; analysis
  `reports/iter-route-continuity-v0075/repair1-screen-paired-analysis.json`).
- Map results: Aurora/Bridge/Longship/Sprint/String 4-2, Atoll/Sweden 3-3,
  Crossfire 2-4, and Vault 1-5.

**Repair attempt 1 not promoted; no full matrix.** The four-win margin is not
material enough for a release gate. Final repair attempt 2 removes the special
immediate-preemption branch entirely and isolates nearest repair ownership
under the existing priority and commitment rules.

## Repair attempt 2 and final decision

- Focused tests passed **19/19**; compileall and `git diff --check` passed.
  `make static` retained the inherited 15-import exit-2 result. Smoke was
  **4/4 command-clean** (`reports/local-20260815T161638Z`).
- The final 54-game screen lost **23-31**, with 225,340 versus 265,560
  titanium (0.8486x), zero no-delivery rows, zero command
  failures/TLE/suspicious output, max p99 1,234 us, and peak callback 4,808 us
  (`reports/local-20260815T161700Z`; analysis
  `reports/iter-route-continuity-v0075/repair2-screen-paired-analysis.json`).
- Map results: String 5-1; Bridge/Longship/Sweden 3-3; and
  Atoll/Aurora/Crossfire/Sprint 2-4, Vault 1-5.

**Iteration B rejected after two bounded repair attempts.** No version,
package, full matrix, upload, or activation was created. Candidate production
source was restored byte-identically to immutable v0034; the original 12
focused tests, compileall, and `git diff --check` pass after rollback
(`reports/iter-route-continuity-v0075-rollback-focused.log`); rollback smoke is
also **4/4 command-clean** (`reports/local-20260815T162556Z`). Iteration C is
blocked by its gate. The evidence rejects local nearest-repair ownership as a
stable improvement: visibility differs by Builder, so independent ownership
decisions can suppress useful repairers without a shared assignment protocol.
