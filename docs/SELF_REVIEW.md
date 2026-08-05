# Artifact self-review

**Review date:** 2026-08-05

## Checks completed

- Public rules, API, tutorials, changelog, and map-pool facts were cross-checked.
- The August 4 Gunner/Sentinel rebalance is reflected consistently.
- Known stale tutorial patterns are explicitly marked.
- The primary Codex model is pinned to `gpt-5.6-sol` at medium reasoning.
- Planner and reviewer are read-only Sol-medium custom agents.
- The only writable implementation role is Luna-max.
- Direct upload and activation scripts require `--confirm`; the autonomous live operator is separately authorized through `configs/live_policy.toml`.
- Python source parses successfully.
- All TOML files parse successfully.
- Static contract test suite passes.
- Candidate directory is far below documented file/size limits.
- Local evaluation enforces `--tle 10`, side swaps, deterministic seeds, and replay retention.
- Release evaluation covers all 21 current maps.
- Immutable snapshots are byte-for-byte the source used to build the ZIP; manifest is external.

## Deliberate limitations

The environment used to create this repository was not authenticated to the user's Florent account. Therefore I did **not**:

- run actual local `fcode` games;
- sync the binary map files;
- run Graviton remote tests;
- inspect authenticated leaderboard/submission data;
- upload or activate anything.

The scripts are designed to perform those operations locally after `fcode login`.

## Facts requiring an engine/platform check

1. Main rules say the first timeout tiebreaker is titanium “collected,” while one official AI-context wording has said “delivered to Core.” Optimize real delivery either way, and confirm the match JSON field.
2. Store reads are snapshot-consistent and writes are delayed. Do not assume same-slot multi-writer increments are atomic; verify exact resolution before using them.
3. `model_reasoning_effort = "max"` is supported in current Codex subagent guidance for eligible models/accounts, but older CLI/config references may only validate through `xhigh`. Update Codex; use `xhigh` only as a documented fallback.
4. Replay field names are not guessed. The harness stores raw JSON/replays; add a parser after inspecting current outputs.

## Review outcome

The repository is ready as a **development harness and detailed plan**, not as a finished competitive bot. The included candidate is intentionally a safe starter. The recommended first implementation package is safe dispatch + shared coordinate protocol + bounded cached BFS, followed by a verified end-to-end Harvester-to-Core delivery route.


## 2026-08-05 Codex/live-operations revision

- The previous custom-agent declaration was found insufficient to prove Luna execution because of the current Sol/Terra V2 versus Luna V1 mismatch.
- Added a reversible invocation-scoped V1 catalog route and an explicit process-isolated Sol/Luna/Sol fallback.
- Added exact model/command evidence manifests.
- Added autonomous resumable upload, activation, observation, promotion, and rollback with `UPDATES.md` and machine state.
- The artifact environment still lacks authenticated Codex/FCL access, so native routing and live operations must be exercised on the user's machine with the included doctor/bootstrap commands.


## Final harness validation

- 21 static/unit contract tests pass.
- All Python source parses successfully.
- All TOML and JSON configuration parses.
- Shell launchers pass `bash -n`.
- A fake-Codex integration verified explicit process invocations in this exact order: `gpt-5.6-sol` medium read-only → `gpt-5.6-luna` max workspace-write → `gpt-5.6-sol` medium read-only, with an approved manifest.
- A fake-FCL integration verified bootstrap, immutable packaging, upload, ready polling, activation, cross-session observation state, score evaluation, and automatic reactivation of the previous known-good version.
- Match details are prefetched by the trusted Python operator; the Sol live reviewer runs read-only and cannot activate submissions directly.
- The real installed Codex model catalog and authenticated Florent account still need to be checked on the user's machine with `make codex-doctor`, `make setup-codex-v1`, and `make live-bootstrap`.


## Startup-context review

- Root `AGENTS.md` now requires a deterministic startup sequence instead of reading every long document.
- `docs/START_HERE.md` is generated from machine-readable project and live state.
- Nested instruction files exist for candidate code, scripts, and tests.
- Sol planner, Luna implementer, and Sol reviewer explicitly read startup state and nearest nested instructions.
- Approved Codex tasks record their task/outcome/report in project state.
- Live-state and update-log changes regenerate the startup summary.
- Tests verify the instruction hierarchy and generated handoff contract.
