# Florent Code League development and live updates

This file is the durable handoff between Codex sessions. It is append-only except for the **Current state** table, which automation may refresh.

## Current state

| Field | Value |
|---|---|
| Workflow phase | active_observing |
| Working candidate | `bots/candidate` |
| Current active platform version | 73 |
| Last known-good platform version | 72 |
| Previous active platform version | 72 |
| Last known-good live score | 0.6416666666666667 |
| Current candidate live score | unknown |
| Last deployment | 2026-08-09T20:12:41Z |
| Last observation | 2026-08-09T20:13:19Z |
| Last decision | observation captured |

Machine-readable state: [`state/live_state.json`](state/live_state.json).

## Score definition

The primary live score is the mean fractional score over rated five-game series during a version's observation window:

```text
series score = our game wins / 5
live score   = mean(series score)
```

Also record rating delta and opponent-adjusted residual when available. Reliability failures override score and trigger immediate rollback.

## Append-only update log

<!-- Automation appends newest entries immediately below this comment. -->

### Live observation captured — 2026-08-09T20:13:19Z

- Active version: 73
- Report: reports/live-observe-20260809T201259Z


### Candidate activated — 2026-08-09T20:12:41Z

- Version: 73
- Previous/rollback: 72
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260809T201220Z


### Candidate uploaded — 2026-08-09T20:12:41Z

- Candidate: v0015-close-contact-bootstrap-defense-7dd72f03
- Version: 73
- Rollback target: 72
- Report: reports/live-deploy-20260809T201220Z


### Live candidate promoted — 2026-08-09T20:12:03Z

- Version: 72
- Live score: 0.6416666666666667
- Adjusted score: 0.11343448790107642
- Reason: 24 rated series: 18-6 series, 77-43 games, +87.12 Elo, positive opponent-adjusted residual, zero reliability failures


### Live observation captured — 2026-08-09T20:11:36Z

- Active version: 72
- Report: reports/live-observe-20260809T201118Z


### Live observation captured — 2026-08-09T20:10:16Z

- Active version: 72
- Report: reports/live-observe-20260809T200957Z


### Live observation captured — 2026-08-09T20:02:56Z

- Active version: 72
- Report: reports/live-observe-20260809T200236Z


### Live observation captured — 2026-08-09T19:57:17Z

- Active version: 72
- Report: reports/live-observe-20260809T195658Z


### Live observation captured — 2026-08-09T19:43:06Z

- Active version: 72
- Report: reports/live-observe-20260809T194245Z


### Live observation captured — 2026-08-09T19:37:09Z

- Active version: 72
- Report: reports/live-observe-20260809T193650Z


### Live score evaluated — 2026-08-09T19:20:39Z

- Version: 72
- Series: 19
- Score: 0.631578947368421
- Adjusted score: 0.106507331898
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: v72 is 14-5 in series and 60-35 in games with +64.76 Elo and positive opponent-adjusted residual, but only 19 of the required 24 series are complete


### Live observation captured — 2026-08-09T19:19:49Z

- Active version: 72
- Report: reports/live-observe-20260809T191930Z


### Live score evaluated — 2026-08-09T19:15:58Z

- Version: 72
- Series: 18
- Score: 0.6333333333333333
- Adjusted score: 0.106737896
- Reliability failures: 0
- Proposed decision: keep_observing
- Reason: v72 is 13-5 in series and 57-33 in games with +61.48 Elo and positive opponent-adjusted residual, but only 18 of the required 24 series are complete


### Live observation captured — 2026-08-09T19:10:47Z

- Active version: 72
- Report: reports/live-observe-20260809T191026Z


### Live observation captured — 2026-08-09T19:09:18Z

- Active version: 72
- Report: reports/live-observe-20260809T190900Z


### Live observation captured — 2026-08-09T19:07:54Z

- Active version: 72
- Report: reports/live-observe-20260809T190753Z


### Live observation captured — 2026-08-09T19:06:34Z

- Active version: 72
- Report: reports/live-observe-20260809T190615Z


### v0015 close-contact bootstrap defense packaged — 2026-08-09T19:04:30Z

- Files changed: `bots/candidate/bot/builder.py`, `tests/test_candidate_bootstrap_defense.py`, `experiments/v72-close-contact-bootstrap-defense.md`; rejected global variant recorded in `experiments/v72-single-bootstrap-defense.md`.
- Focused tests: 9/9 passed after self-review; compileall passed; smoke 4/4 command-clean. Logs: `reports/v72-close-contact-bootstrap-defense/` and `reports/local-20260809T184659Z`.
- Current-pool gate: recomputed 51-39 over 90 paired games, titanium 171,550 versus 168,040 (ratio 1.0209), zero command failures. Reports: `reports/local-20260809T184216Z`, `reports/local-20260809T184730Z`, and affected-map replacement `reports/local-20260809T185644Z`.
- Replay timing: 680,738 candidate calls, p99 2.975 ms, max 7.511 ms, zero TLEs.
- Remote gate: 4-1 and reliability-clean against immutable v0014; match `a4fdd82b-f5c1-449c-a809-473cdbdfde31`, report `reports/remote-20260809T190000Z`.
- Package: `artifacts/submissions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03.zip`, SHA-256 `fa5ec52b970998434ae80598e296ec6d7aca0afa872e26f26338f1e8ae8fcb1e`.
- Live: platform v72 remains active at 1358.24 Elo, rank 50/116; its 17-series sample is 13-4 series, 55-30 games, +62.27 Elo. Deployment waits for the configured 24-series known-good promotion threshold.
- Remaining risk: `make static` reproduces the inherited pre-v69 API/obsolete line-cap failures; meander remains side-sensitive locally.
- Iteration status: release gates passed and packaged; waiting for deterministic live observation unlock before upload/activation.

### Live observation captured — 2026-08-09T19:02:50Z

- Active version: 72
- Report: reports/live-observe-20260809T190227Z


### Live observation captured — 2026-08-09T18:24:04Z

- Active version: 72
- Report: reports/live-observe-20260809T182346Z


### Canonical-opening v0014 promoted and deployed as platform v72 — 2026-08-09T16:08:12Z

- Parent/baseline: immutable v0013/v69. Runtime change: `bots/candidate/bot/core.py` canonicalizes equal-score Core spawn and first-visible-ore ordering for current live geometries; ambiguous 16x16 and 25x25 layouts use observable Core quadrants. Focused coverage: `tests/test_candidate_opening_orientation.py`; experiment: `experiments/v69-canonical-opening.md`.
- Current synced 15-map pool, seeds 1/19/101, both sides: 61-29-0 (`+32/90`), titanium 178030 versus 142840 (ratio `1.2463`), 90/90 commands clean. Main reports: `reports/local-20260809T152902Z`, `reports/local-20260809T154538Z`; final 25x25 replacement: `reports/local-20260809T155537Z`.
- Old protected compatibility, recomputed from changed-map reruns: 27-21-0 (`+6/48`), titanium 130860 versus 108690 (ratio `1.2040`), no 0-6 map. Sources: `reports/local-20260809T153449Z`, `reports/local-20260809T154403Z`, `reports/local-20260809T155828Z`, and `reports/local-20260809T155537Z`.
- Validation: focused release suite 36/36; smoke 4/4; compile/package checks passed; archive 17 files/94125 bytes, SHA-256 `998c86506afdef96624348801aaf4dc8cb5dcac1a6e31bb3397a7cdbe36a70f3`. Full `make static` remains blocked by inherited pre-v69 API tests and its obsolete 3200-line assertion; log: `reports/release-v69-canonical-opening/static.log`.
- Remote gate `1c260f12-1141-41e0-a0c7-58e27090c771` was reliability-clean but 2-3 unpaired; exact server seeds scored 8-2 locally when side-swapped. Treat server/local outcome variance and future map-pool drift as observation risks.
- Packaged immutable baseline: `bots/versions/v0014_canonical-opening_20260809-1606_7dd72f03`; archive: `artifacts/submissions/v0014_canonical-opening_20260809-1606_7dd72f03.zip`.
- Platform v72 (`v0014-canonical-opening-7dd72f03`) is ready and active; v69 is ready and recorded as rollback. Initial snapshot: rating `1278.0199`, rank `58/116`, recent record `6-4`, with no v72-specific ladder series yet (`reports/live-observe-20260809T160750Z`). Status: LOCAL PROMOTION PASSED; LIVE ACTIVE_OBSERVING.

### Live observation captured — 2026-08-09T16:08:12Z

- Active version: 72
- Report: reports/live-observe-20260809T160750Z


### Candidate activated — 2026-08-09T16:07:37Z

- Version: 72
- Previous/rollback: 69
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260809T160717Z


### Candidate uploaded — 2026-08-09T16:07:36Z

- Candidate: v0014-canonical-opening-7dd72f03
- Version: 72
- Rollback target: 69
- Report: reports/live-deploy-20260809T160717Z


### Live candidate promoted — 2026-08-09T16:07:00Z

- Version: 69
- Live score: None
- Adjusted score: None
- Reason: v69 active platform comparator and immutable local baseline


### Live state bootstrapped — 2026-08-09T16:07:00Z

- Active version: 69
- Report: reports/live-bootstrap-20260809T160640Z


### Outcome-first reviewer comparison of new uploads v68 through v71 — 2026-08-09T14:45:07Z

- v68-v71 were downloaded under `reports/reviewer-new-uploads-20260809T142353Z/`; archive SHA-256 values and submission IDs are recorded in `experiments/reviewer-v68-v71-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v68 lost 3-45-0 (score `-42/48`) with zero candidate collection and 0-6 on every protected map except showdown (report `reports/local-20260809T142433Z`).
- v69 won 30-18-0 (score `+12/48`) with collection 252030 versus 241340 (ratio `1.0443`), no core outcomes, and no protected-map collapse (report `reports/local-20260809T143232Z`). It is preserved as immutable local baseline v0013.
- v70 won 25-23-0 (score `+2/48`) with collection ratio `0.9141` and collapsed 0-6 on string (report `reports/local-20260809T143248Z`).
- v71 lost 3-45-0 (score `-42/48`) with zero candidate collection and 0-6 on every protected map except showdown (report `reports/local-20260809T143303Z`).
- Status: v69 BASELINE PROMOTED; v68/v70/v71 REVIEWED — REJECTED. All 192 commands were clean. No platform activation was performed; v69 package/snapshot: `v0013_reviewer-v69-platform-winner_20260809-1444_7dd72f03`. Detailed record: `experiments/reviewer-v68-v71-20260809.md`.
- Final live observation shows v70 active externally, rating `1239.1252`, rank `59/116`, `555` matches, and recent record `0-10` (report `reports/live-observe-20260809T144444Z`).

### Live observation captured — 2026-08-09T14:45:07Z

- Active version: 70
- Report: reports/live-observe-20260809T144444Z


### Live observation captured — 2026-08-09T14:24:12Z

- Active version: 68
- Report: reports/live-observe-20260809T142353Z


### Outcome-first reviewer comparison of new uploads v66 and v67 — 2026-08-09T12:30:44Z

- v66 and v67 were downloaded under `reports/reviewer-new-uploads-20260809T121134Z/`; archive SHA-256 values and submission IDs are recorded in `experiments/reviewer-v66-v67-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v66 lost 21-27-0 (score `-6/48`) with collection 274720 versus 234200 (ratio `1.1730`), but collapsed 0-6 on aurora and strait (report `reports/local-20260809T121212Z`).
- v67 won 29-19-0 (score `+10/48`) with collection 282270 versus 309800 (ratio `0.9111`), but collapsed 0-6 on showdown (report `reports/local-20260809T122051Z`).
- Status: v66/v67 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 96 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v66-v67-20260809.md`.
- Final live observation shows v67 active externally, rating `1413.7503`, rank `45/114`, `542` matches, and recent record `6-4` (report `reports/live-observe-20260809T123025Z`).

### Live observation captured — 2026-08-09T12:30:44Z

- Active version: 67
- Report: reports/live-observe-20260809T123025Z


### Live observation captured — 2026-08-09T12:11:53Z

- Active version: 66
- Report: reports/live-observe-20260809T121134Z


### Outcome-first reviewer comparison of new uploads v64 and v65 — 2026-08-09T11:37:05Z

- v64 and v65 were downloaded under `reports/reviewer-new-uploads-20260809T110801Z/`; archive SHA-256 values and submission IDs are recorded in `experiments/reviewer-v64-v65-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v64 tied 24-24-0 (score `0/48`) with collection 291040 versus 293460 (ratio `0.9918`) and collapsed 0-6 on showdown (report `reports/local-20260809T111159Z`).
- v65 lost 15-33-0 (score `-18/48`) with collection 283890 versus 340840 (ratio `0.8329`) and collapsed 0-6 on crossfire, hive, and strait (report `reports/local-20260809T112215Z`).
- Status: v64/v65 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 96 valid commands were clean. An accidental v64 21-map release-matrix attempt was interrupted at game 14 and excluded (`reports/local-20260809T110854Z`). No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v64-v65-20260809.md`.
- Final live observation shows v65 active externally, rating `1422.3962`, rank `43/114`, `536` matches, and recent record `6-4` (report `reports/live-observe-20260809T113642Z`).

### Live observation captured — 2026-08-09T11:37:05Z

- Active version: 65
- Report: reports/live-observe-20260809T113642Z


### Live observation captured — 2026-08-09T11:08:24Z

- Active version: 65
- Report: reports/live-observe-20260809T110801Z


### Outcome-first reviewer comparison of new uploads v61 through v63 — 2026-08-09T10:14:14Z

- v61, v62, and v63 were downloaded under `reports/reviewer-new-uploads-20260809T094851Z/`; archive SHA-256 values are recorded in `experiments/reviewer-v61-v63-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v61 lost 21-27-0 (score `-6/48`) with collection 260930 versus 307940 (ratio `0.8473`) and collapsed 0-6 showdown/crossfire/hive (report `reports/local-20260809T094937Z`).
- v62 was the raw-outcome batch winner at 27-21-0 (score `+6/48`) with collection 302000 versus 307890 (ratio `0.9809`), but collapsed 0-6 twins and lost crossfire 1-5 (report `reports/local-20260809T100320Z`).
- v63 tied 24-24-0 (score `0/48`) with collection 293730 versus 293510 (ratio `1.0007`), but collapsed 0-6 showdown (report `reports/local-20260809T094944Z`).
- Status: v61/v62/v63 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 144 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v61-v63-20260809.md`.
- Final live observation shows v63 active externally, rating `1435.0250`, rank `43/113`, `528` matches, and recent record `6-4` (report `reports/live-observe-20260809T101349Z`). Final submission refresh found no v64+ upload.

### Live observation captured — 2026-08-09T10:14:14Z

- Active version: 63
- Report: reports/live-observe-20260809T101349Z


### Live observation captured — 2026-08-09T09:49:09Z

- Active version: 63
- Report: reports/live-observe-20260809T094851Z


### Outcome-first reviewer comparison of requested upload v60 — 2026-08-09T00:01:39Z

- v60 was downloaded under `reports/reviewer-new-uploads-20260808T234833Z/`; archive SHA-256 is recorded in `experiments/reviewer-v60-20260809.md`.
- v60 was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v60 was command-clean and won 30-18-0 (paired score `+12/48`) with collection 306710 versus 304490 (ratio `1.0073`) and six core wins, but collapsed 0-6 on hive and strait. Runner wall-clock p99/max was 28.3621/28.3621 seconds.
- Status: v60 REVIEWED — REJECTED by the hard map-floor guard; v0012/v28 remains the local immutable baseline. All 48 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v60-20260809.md`.
- Final live observation shows v60 active externally, rating `1413.3087`, rank `46/113`, `467` matches, and recent record `3-7` (report `reports/live-observe-20260809T000120Z`). Final submission refresh found no v61+ upload. v59 remains unevaluated after its interrupted partial matrix.

### Live observation captured — 2026-08-09T00:01:39Z

- Active version: 60
- Report: reports/live-observe-20260809T000120Z


### Live observation captured — 2026-08-08T23:48:51Z

- Active version: 60
- Report: reports/live-observe-20260808T234833Z


### Live observation captured — 2026-08-08T23:42:54Z

- Active version: 59
- Report: reports/live-observe-20260808T234236Z


### Outcome-first reviewer comparison of requested upload v58 — 2026-08-08T23:38:06Z

- v57 was intentionally skipped. v58 was downloaded under `reports/reviewer-new-uploads-20260808T232447Z/`; archive SHA-256 is recorded in `experiments/reviewer-v58-20260809.md`.
- v58 was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v58 was command-clean and won 27-21-0 (paired score `+6/48`) with collection 326730 versus 313960 (ratio `1.0407`), but collapsed 0-6 on twins and strait. Its runner wall-clock p99/max was 30.6348/30.6348 seconds.
- Status: v58 REVIEWED — REJECTED by the hard map-floor guard; v0012/v28 remains the local immutable baseline. All 48 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v58-20260809.md`.
- Final live observation shows v59 active externally, rating `1419.7381`, rank `45/113`, `465` matches, and recent record `5-5` (report `reports/live-observe-20260808T233806Z`). v59 appeared after the v58 review and was intentionally not evaluated; no v60+ upload was present.

### Live observation captured — 2026-08-08T23:38:29Z

- Active version: 59
- Report: reports/live-observe-20260808T233806Z


### Live observation captured — 2026-08-08T23:25:05Z

- Active version: 58
- Report: reports/live-observe-20260808T232447Z


### Outcome-first reviewer comparison of new uploads v54 through v56 — 2026-08-08T23:13:45Z

- Three unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T225637Z/`: v54, v55, and v56. Archive SHA-256 values are recorded in `experiments/reviewer-v54-v56-20260809.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v54 was command-clean but lost 14-34-0 (paired score `-20/48`) and collection 261640 versus 349020 (ratio `0.7496`), with 0-6 bridge/showdown/hive/aurora and 6-0 string (report `reports/local-20260808T225729Z`).
- v55 was command-clean but lost 13-35-0 (paired score `-22/48`) and collection 233500 versus 357470 (ratio `0.6532`), with three core losses, 0-6 bridge/showdown/hive/strait, and 4-2 aurora (report `reports/local-20260808T230122Z`).
- v56 was the batch best but still lost 21-27-0 (paired score `-6/48`) and collection 280440 versus 384350 (ratio `0.7296`); it won bridge 6-0 but collapsed 0-6 showdown/twins (report `reports/local-20260808T230127Z`).
- Status: v54/v55/v56 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 144 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v54-v56-20260809.md`.
- Final live observation shows v56 active externally, rating `1423.0620`, rank `44/113`, `462` matches, and recent record `6-4` (report `reports/live-observe-20260808T231328Z`). Final submission refresh found no v57 or later upload.

### Live observation captured — 2026-08-08T23:13:45Z

- Active version: 56
- Report: reports/live-observe-20260808T231328Z


### Live observation captured — 2026-08-08T22:56:58Z

- Active version: 56
- Report: reports/live-observe-20260808T225637Z


### Outcome-first reviewer comparison of new uploads v51 through v53 — 2026-08-08T11:03:38Z

- Three unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T103146Z/`: v51, v52, and v53. Archive SHA-256 values are recorded in `experiments/reviewer-v51-v53-20260808.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v51 was command-clean but lost 15-33-0 (paired score `-18/48`) and collection 241000 versus 323530 (ratio `0.7449`), with 0-6 showdown/crossfire/hive/aurora and 6-0 string (report `reports/local-20260808T103231Z`).
- v52 was command-clean but lost 16-32-0 (paired score `-16/48`) and collection 250220 versus 318650 (ratio `0.7853`); it won bridge/hive 6-0 but collapsed 0-6 twins/crossfire/aurora/strait, with runner wall-clock p99/max 32.6513/32.9255 seconds (report `reports/local-20260808T104218Z`).
- v53 was command-clean but lost 15-33-0 (paired score `-18/48`) and collection 240980 versus 323530 (ratio `0.7448`), matching v51's broad map collapses and 6-0 string lead (report `reports/local-20260808T105316Z`).
- Status: v51/v52/v53 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 144 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v51-v53-20260808.md`.
- Final live observation shows v52 active externally, v53 ready/inactive, rating `1387.2830`, rank `44/111`, `389` matches, and recent record `4-6` (report `reports/live-observe-20260808T110320Z`). Final submission refresh found no v54 or later upload.

### Live observation captured — 2026-08-08T11:03:38Z

- Active version: 52
- Report: reports/live-observe-20260808T110320Z


### Live observation captured — 2026-08-08T10:32:07Z

- Active version: 53
- Report: reports/live-observe-20260808T103146Z


### Reviewer refresh — no uploads newer than v50 — 2026-08-08T10:12:20Z

- Final submission refresh still shows v50 newest; no v51+ upload was available, so no new challenger download or 48-game matrix was run.
- The retained local baseline remains immutable v0012/v28. No source edits, upload, activation, or challenger test suite was performed.
- Fresh live observation shows v49 active externally at rating `1419.1461`, rank `43/111`, `384` matches, and a `7-3` recent ten-series record (report `reports/live-observe-20260808T101156Z`).

### Live observation captured — 2026-08-08T10:12:20Z

- Active version: 49
- Report: reports/live-observe-20260808T101156Z


### Outcome-first reviewer comparison of new uploads v47 through v50 — 2026-08-08T10:07:15Z

- Four unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T092716Z/` (v47/v48) and `reports/reviewer-new-uploads-20260808T094635Z/` (v49/v50). Archive SHA-256 values are recorded in `experiments/reviewer-v47-v50-20260808.md`.
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v47 was command-clean but lost 16-32-0 (paired score `-16/48`) and collection 211930 versus 321980 (ratio `0.6582`), with nine core losses and 0-6 showdown/twins/crossfire (report `reports/local-20260808T092838Z`).
- v48 was command-clean but lost 20-28-0 (paired score `-8/48`) and collection 244490 versus 322190 (ratio `0.7588`), with 0-6 showdown/twins (report `reports/local-20260808T093739Z`).
- v49 was command-clean but lost 21-27-0 (paired score `-6/48`) and collection 247220 versus 310620 (ratio `0.7959`); it won bridge 6-0 but collapsed 0-6 twins/string and had the slowest runner wall-clock p99/max (31.6368/32.0995 seconds) (report `reports/local-20260808T094719Z`).
- v50 was command-clean but lost 21-27-0 (paired score `-6/48`) and collection 280560 versus 355400 (ratio `0.7894`); it won showdown 6-0 but collapsed 0-6 crossfire/strait (report `reports/local-20260808T095716Z`).
- Status: v47/v48/v49/v50 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 192 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v47-v50-20260808.md`.
- Final live observation shows v49 active externally, v50 ready/inactive, rating `1417.7841`, rank `43/111`, `383` matches, and recent record `6-4` (report `reports/live-observe-20260808T100542Z`). Final submission refresh found no v51 or later upload.

### Live observation captured — 2026-08-08T10:06:01Z

- Active version: 49
- Report: reports/live-observe-20260808T100542Z


### Live observation captured — 2026-08-08T09:46:54Z

- Active version: 50
- Report: reports/live-observe-20260808T094635Z


### Live observation captured — 2026-08-08T09:27:34Z

- Active version: 48
- Report: reports/live-observe-20260808T092716Z


### Outcome-first reviewer comparison of new uploads v45 and v46 — 2026-08-08T09:03:53Z

- Two unseen uploads were downloaded under `reports/reviewer-new-uploads-20260808T084522Z/`: v45 (SHA-256 `8491f9602055ec7e40dbcf4899165bf4d12183dbeb16318824940b3e2b2e34d2`) and v46 (`fb8c609d1cc6975460b0e2052120ed55db0391396da493aec4d24a872e29b232`).
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v45 was command-clean but lost 19-29-0 (paired score `-10/48`) and collection 248600 versus 328020 (ratio `0.7579`); it collapsed 0-6 on bridge and strait (report `reports/local-20260808T084604Z`).
- v46 was command-clean but lost 13-35-0 (paired score `-22/48`) and collection 226640 versus 347820 (ratio `0.6516`); it had three candidate core wins but collapsed 0-6 on showdown, twins, crossfire, and string (report `reports/local-20260808T085453Z`).
- Status: v45/v46 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. All 96 commands were clean. No source edits, challenger tests, upload, or activation were performed. Detailed record: `experiments/reviewer-v45-v46-20260808.md`.
- Live observation shows v46 active externally at rating `1422.3161`, rank `43/111`, with recent record `3-7` (report `reports/live-observe-20260808T084522Z`). Final submission refresh found no v47 or later upload.

### Live observation captured — 2026-08-08T08:45:40Z

- Active version: 46
- Report: reports/live-observe-20260808T084522Z


### Outcome-first reviewer comparison of new uploads v43 and v44 — 2026-08-07T22:54:06Z

- Two unseen ready uploads were downloaded under `reports/reviewer-new-uploads-20260807T223624Z/`: v43 (SHA-256 `eace15c9fee38b7c2a2b017aa528d773d851c784f606c6369186fd0ab61ad74a`) and v44 (`8f1980d864943c823ba5b85f614c81e82897a91c6d90e18172c109866cd829a5`).
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v43 was command-clean but tied 24-24-0 (score `0/48`) and trailed collection 274820 versus 297500 (ratio `0.9238`); it won bridge/showdown/aurora but went 0-6 on twins/crossfire/string (report `reports/local-20260807T223704Z`).
- v44 was command-clean but lost 18-30-0 (score `-12/48`) and collection 239380 versus 343780 (ratio `0.6963`), with three core losses and 0-6 crossfire/string/aurora (report `reports/local-20260807T224539Z`). All 96 commands had empty stderr and no exception/TLE markers.
- Status: v43/v44 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed. Detailed record: `experiments/reviewer-v43-v44-20260808.md`.
- Live observation shows v44 active externally, rating `1456.0780`, rank `39/108`, `313` matches, and recent record `5-5` (report `reports/live-observe-20260807T223624Z`). Final submission refresh found no v45 or later upload.

### Live observation captured — 2026-08-07T22:36:42Z

- Active version: 44
- Report: reports/live-observe-20260807T223624Z


### Outcome-first reviewer comparison of new uploads v38 through v42 — 2026-08-07T22:31:42Z

- Five unseen ready uploads were downloaded under `reports/reviewer-new-uploads-20260807T214651Z/`: v38 (SHA-256 `ca27bbfb9438adb93e716eb9fd18af55185f0239b931d72c93345bedd4f59bc3`), v39 (`8dea1fbeccf462a470117595b1f6ff9595a6b9081d4315912594a9e92cce6a19`), v40 (`bad3919f7ba3af0a607c027828b454c256ace700e724d1ef0691a4c7286f05eb`), v41 (`50a2fb9aa5e415e3c7786d10814483d8e33e0e28ad7b2ca408c8f8a980a5f697`), and v42 (`42bfaab4a18ad373539884833e9c2e836a531a6eb1a99973afeb2539770680e5`).
- Each was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). Paired outcome is primary; reliability/map guards are hard; titanium collection is secondary.
- v38 was command-clean but lost 18-30-0 (score `-12/48`), collection ratio `0.7549`, no core wins, and 0-6 on showdown/hive (report `reports/local-20260807T214729Z`).
- v39 was command-clean but lost 13-35-0 (score `-22/48`), ratio `0.7212`, with three core losses and 0-6 on showdown/hive/aurora (report `reports/local-20260807T215633Z`).
- v40 was command-clean but lost 13-35-0 (score `-22/48`), ratio `0.7206`, with three core losses and the same 0-6 showdown/hive/aurora pattern (report `reports/local-20260807T220507Z`).
- v41 was closest but still lost 21-27-0 (score `-6/48`), ratio `0.9439`; it won all string/aurora games but lost 0-6 bridge/showdown/hive (report `reports/local-20260807T221344Z`).
- v42 was command-clean but lost 18-30-0 (score `-12/48`), ratio `0.8092`, with one core win versus three core losses and 0-6 showdown/twins (report `reports/local-20260807T222248Z`). All 240 commands had empty stderr and no exception/TLE markers.
- Status: v38/v39/v40/v41/v42 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed. Detailed record: `experiments/reviewer-v38-v42-20260807.md`.
- Live observation shows v42 active externally, rating `1444.2751`, rank `39/108`, `309` matches, and recent record `4-6` (report `reports/live-observe-20260807T214651Z`). Final submission refresh found no v43 or later upload.

### Live observation captured — 2026-08-07T21:47:10Z

- Active version: 42
- Report: reports/live-observe-20260807T214651Z


### Outcome-first reviewer comparison of new uploads v35 through v37 — 2026-08-07T14:15:27Z

- Three unseen ready uploads were found and downloaded under `reports/reviewer-new-uploads-20260807T134554Z/`: v35 (`c8bd27de-b622-495e-96ed-ce4b447012df`, SHA-256 `6a2e66fa60c4d746c2122975f58fddddf6ed186e30e45f657f9313a43c0bf78a`), v36 (`e236368b-1e0e-4f97-a127-f7c95282d917`, SHA-256 `813a3b5e3037005092bee10013c70ca6c14109c69da2714d98c08c514d607dc9`), and v37 (`22cee774-ff2a-4702-a1a8-688cc3d121fb`, SHA-256 `20da31812c4a9d888697062df025cd150f6eef01a437839988df74069531acc7`).
- Each candidate was compared against immutable v0012/v28 on the fixed 48-game side-swapped pool (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1/19/101`; `--tle 10`). The primary decision metric is paired outcome score; reliability/map guards are hard; titanium collection is secondary.
- v35 was command-clean but tied the primary outcome 24-24-0 (score `0/48`) and trailed collection 290480 versus 297110 (ratio `0.9777`), with no core wins (report `reports/local-20260807T134801Z`).
- v36 was command-clean but lost 14-34-0 (score `-20/48`) and collection 292090 versus 381820 (ratio `0.7650`), with no core wins (report `reports/local-20260807T135632Z`).
- v37 was command-clean but lost 18-30-0 (score `-12/48`) and collection 274270 versus 352330 (ratio `0.7784`); it had one core win to the baseline's zero, but went 0-6 on showdown and aurora (report `reports/local-20260807T140536Z`). All 144 commands had empty stderr and no exception/TLE markers.
- Status: v35/v36/v37 REVIEWED — REJECTED; v0012/v28 remains the local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer. Detailed record: `experiments/reviewer-v35-v37-20260807.md`.
- Fresh live observation shows v37 active externally, team rating `1459.6548`, rank `37/106`, `261` matches, and recent record `6-4` (report `reports/live-observe-20260807T134554Z`). This remains observation-only and does not change the local decision.
- Final read-only submission-list refresh after the matrix still showed v37 as the newest upload; no v38 or later candidate appeared (`reports/reviewer-new-uploads-20260807T134554Z/submissions-final.json`).

### Live observation captured — 2026-08-07T13:46:14Z

- Active version: 37
- Report: reports/live-observe-20260807T134554Z


### Outcome-first reviewer comparison of new uploads v33 and v34 — 2026-08-07T12:16:29Z

- The reviewer rule is now outcome-first: paired game result (+1/0/-1) is primary, reliability and map floors are guards, and titanium collection is secondary margin; the full 210-game/55% gate remains deferred in this reviewer-only screening pass.
- New unseen uploads v33 (id 3dd459a2-2432-4572-b739-ef6f869eb593, platform name 2) and v34 (id b266e6a4-6d89-46de-9b9c-239a4fcb1f7c, platform name 1) were downloaded with fcode under reports/reviewer-new-uploads-20260807T115121Z/. Archive SHA-256 values: v33 eb038fccc0311f860ef4288ba32c83acb57328dbf18d9255c66c320fbad13a00; v34 0351d675d0db1449766a54b92e1a4233260bd2357278dc23003df885a1a2d980.
- v33 direct battle against retained v0012/v28 was command-clean but lost on the primary outcome metric: 20-28-0, paired score -8/48, with 266940 versus 354480 collected titanium (ratio 0.7530); it led bridge and strait but went 0-6 on crossfire and twins and had no core wins (report reports/local-20260807T115214Z).
- v34 direct battle against the same v0012/v28 baseline was command-clean but lost: 12-36-0, paired score -24/48, with 232610 versus 302070 collected titanium (ratio 0.7701); it led only aurora and hive, had one candidate core win against six baseline core wins, and runner wall p99/max 36.9351/37.0020 seconds (report reports/local-20260807T120117Z).
- Fresh live observation reports v33 active externally with platform name 2 and v34 ready/inactive with platform name 1; team rating 1458.8214, rank 37/105, 250 matches, and 6-4 over the last ten series. The newest completed v33 series was a 1-4 loss versus The Bisons; no v34-specific series was visible (report reports/live-observe-20260807T115121Z).
- Status: v33/v34 REVIEWED — REJECTED under the outcome-first rule; v0012/v28 retained as local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform v33 remains pre-existing.


### Live observation captured — 2026-08-07T11:51:40Z

- Active version: 33
- Report: reports/live-observe-20260807T115121Z


### Reviewer comparison of new uploads v31 and v32 — 2026-08-07T11:44:32Z

- New unseen uploads v31 (id 4e739154-d792-4cdb-8184-de55c1df67b4, platform name 2) and v32 (id b18c7ce3-a2d8-4e9d-973b-e964acf9862b, platform name 1) were downloaded with fcode under reports/reviewer-new-uploads-20260807T111917Z/. Archive SHA-256 values: v31 9d32fd7268d4064397ae5566aadfa71b8a43b9ce202ff8f0fd62944361260802; v32 b1b3bd7fec430b4fa63c76961711d55d6e9bb3107d0153bbf7531dff7e70961d.
- v31 direct battle against retained v0012/v28 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 264120 versus 314810 collected titanium, ratio 0.8390, 26/48 wins and no ties (report reports/local-20260807T111956Z). It led bridge, aurora, hive, and strait but collapsed on twins, crossfire, showdown, and string; no core wins.
- v32 direct battle against the same v0012/v28 baseline was command-clean but lost: 232910 versus 302050 collected titanium, ratio 0.7711, 12/48 wins and no ties (report reports/local-20260807T112918Z). It led only aurora and hive, suffered six core-destruction losses, and had runner wall p99/max 37.0890/37.2008 seconds.
- Fresh live observation reports v31 active externally with platform name 2 and v32 ready/inactive with platform name 1; team rating 1454.2884, rank 37/105, 246 matches, and 5-5 over the last ten series. No completed v31/v32-specific series was visible; the latest completed visible matches still used v30 (report reports/live-observe-20260807T111917Z).
- Status: v31/v32 REVIEWED — REJECTED; v0012/v28 retained as local immutable baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform v31 remains pre-existing.


### Live observation captured — 2026-08-07T11:19:38Z

- Active version: 31
- Report: reports/live-observe-20260807T111917Z


### Reviewer comparison of new uploads v27 through v30 — 2026-08-07T11:01:11Z

- New ready uploads v27 (id 2a5ce2f2-36a3-4d42-958a-7d0c37aa0c22), v28 (id 744fcf8a-227f-4813-9d95-e030ea11058c), v29 (id cc441a04-f7f0-4cc1-9e0e-90449d413e1a), and v30 (id 67f3da13-04b9-4d5c-9a3b-f412f8d8eb6e) were downloaded with fcode under reports/reviewer-new-uploads-20260807T101605Z/. Archive SHA-256 values: v27 c3be16e40be4f6705c3d3e107bb247f6b98f22f99bb38a54dfcbaea16a05b43b; v28 b0d31171ab63db311a74e614113370fec21d15c7e8b6d3bfcf24d26f9470eb8d; v29 9703169531048031023a7dea7bfe5a50a38ef3c02a8d7b9452001d7fdbe9fc6c; v30 c10ec08d21d63b81b3f6f11def1f8cc0550932bf6a173bb5da50f5f092df3fe0.
- v27 direct battle against retained v0011/v23 was command-clean but lost: 315910 versus 325110 collected titanium, ratio 0.9717, 18/48 wins and no ties (report reports/local-20260807T101651Z). It led bridge/showdown/twins/crossfire but lost aurora and strait.
- v28 direct battle against retained v0011/v23 was command-clean and won: 379720 versus 301460 collected titanium, ratio 1.2596, 24/48 wins and no ties (report reports/local-20260807T102644Z). It led showdown/twins/crossfire/hive/aurora/strait; bridge was near-even and string was its main weakness.
- v29 direct battle against the promoted v0012/v28 baseline was command-clean but lost: 299420 versus 376850 collected titanium, ratio 0.7945, 24/48 wins and no ties (report reports/local-20260807T103632Z). It led only aurora and regressed heavily on twins/showdown.
- v30 direct battle against the same v0012/v28 baseline was command-clean but lost: 232380 versus 303350 collected titanium, ratio 0.7660, 12/48 wins and no ties (report reports/local-20260807T104536Z). It led only aurora, collapsed on bridge/showdown/string/strait, lost six core-destruction games, and had runner wall p99/max 35.2974/35.3263 seconds.
- Winner validation for v28 passed: all 16 Python files AST-parsed with one explicit main.py Player class; immutable snapshot bots/versions/v0012_reviewer-v28-platform-winner_20260807-1035_7dd72f03 and package artifacts/submissions/v0012_reviewer-v28-platform-winner_20260807-1035_7dd72f03.zip were created, package SHA-256 02647f175571e7c3d8aa3fdc9f15e6d038bb496072b74227fd0d5290b344d669, and packaged smoke was 4/4 command-clean (reports/local-20260807T103603Z).
- Fresh live observation reports v30 active and ready externally, v27/v28/v29 ready/inactive, team rating 1474.5293, rank 35/105, 240 matches, and 5-5 over the last ten series. The latest completed series used v29 (1-4 versus I Stone); no completed v30-specific series was visible (report reports/live-observe-20260807T101605Z).
- Status: v28 REVIEWED — PROMOTED TO LOCAL IMMUTABLE BASELINE; v27/v29/v30 REVIEWED — REJECTED. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform v30 remains pre-existing.


### Live observation captured — 2026-08-07T10:16:25Z

- Active version: 30
- Report: reports/live-observe-20260807T101605Z


### Reviewer comparison of new uploads v25 and v26 — 2026-08-07T00:39:10Z

- New ready uploads v25 (id e1f69d69-c77c-4666-a54e-a9edb07445c4, uploaded 2026-08-06T23:29:37.305Z) and v26 (id 5c6e0acf-1788-4e30-add2-0f6cb20ef72f, uploaded 2026-08-06T23:42:14.200Z) were downloaded with fcode under reports/reviewer-new-uploads-20260807T002021Z/. Archive SHA-256 values: v25 48f24f52a9c5d04a35371570bc97c441a311ce6583d5b7b4c2abdb7945ab41b5; v26 7692706930af73c43db3855e71189e030f59773f6867895578c99987a96b5cef.
- v25 direct battle against retained v0011/v23 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 219190 versus 253790 collected titanium, ratio 0.8637, 21/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260807T002102Z). v25 improved hive and aurora and recorded three core-destruction wins, but collapsed on showdown and string.
- v26 direct battle against the same v0011/v23 baseline was command-clean but lost: 226630 versus 265380 collected titanium, ratio 0.8540, 20/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260807T002942Z). v26 led hive and aurora but collapsed on bridge, showdown, string, and strait; it had no core-destruction wins.
- Fresh live observation reports v26 active and ready externally, v25 ready/inactive, team rating 1402.8394, rank 39/104, 177 matches, and 4-6 over the last ten series. The latest completed series was v25 losing 0-5 to the one piece; no completed v26-specific series was visible (report reports/live-observe-20260807T002021Z).
- Status: v25 and v26 REVIEWED — REJECTED FOR BASELINE; immutable v0011/v23 remains the local reviewer baseline. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; the external platform remains on pre-existing v26.


### Live observation captured — 2026-08-07T00:20:40Z

- Active version: 26
- Report: reports/live-observe-20260807T002021Z


### Reviewer comparison of new uploads v23 and v24 — 2026-08-06T23:43:53Z

- New ready uploads v23 (id 2ba7a808-3fff-42de-b6de-b6c4d847eaa8, uploaded 2026-08-06T22:38:42.481Z) and v24 (id c8f72d03-f751-4f49-a269-b6606f728afa, uploaded 2026-08-06T22:48:45.615Z) were downloaded with fcode under reports/reviewer-new-uploads-20260807T232604Z/ and reports/reviewer-new-uploads-20260807T233108Z/. Archive SHA-256 values: v23 92f66a5311048cdd45ba7313f367ac6a26af173bd814d0a5dc0fbbd40d1f9122; v24 79a90d0c0fb1e94fb4933c0c7f05e2e675e55b959d0e8172058c962818de8292.
- v23 direct battle against retained v0010/v20 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean and won the collection gate: 240680 versus 228650 collected titanium, ratio 1.0526, 17/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T232644Z). v23 led bridge, showdown, twins, crossfire, and strait, but regressed on hive, aurora, and string and lost the raw game count 17-31. All 17 wins were by titanium collection; v23 had 19 collection losses and 12 core-destruction losses, with no core-destruction wins.
- v24 direct battle against the same v0010/v20 baseline was command-clean but lost: 152540 versus 168170 collected titanium, ratio 0.9071, 22/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T233452Z). v24 led bridge, crossfire, and strait narrowly but collapsed on showdown, twins, and string.
- Winner validation for v23 passed: all 16 Python files AST-parsed with one explicit main.py Player class; immutable snapshot bots/versions/v0011_reviewer-v23-platform-winner_20260806-2342_7dd72f03 and package artifacts/submissions/v0011_reviewer-v23-platform-winner_20260806-2342_7dd72f03.zip were created, package SHA-256 723bcf98f10366036b3208dfc45e6fac31a541978d2bc17464f806f476dd5657, and packaged smoke was 4/4 command-clean (reports/local-20260806T234216Z).
- Fresh live observation reports v23 active and ready externally, v24 ready/inactive, and team status rating 1425.6293, rank 37/104, 172 matches, and 6-4 over the last ten series. The latest observed v23 series was a 5-0 win over Kvarnholmen (reports/live-observe-20260806T233108Z).
- Status: v23 REVIEWED — PROMOTED TO LOCAL IMMUTABLE BASELINE; v24 REVIEWED — REJECTED. No bot source edits, challenger suites, upload, or activation were performed by the reviewer; external platform state remains v23.


### Live observation captured — 2026-08-06T23:31:25Z

- Active version: 23
- Report: reports/live-observe-20260806T233108Z


### Live observation captured — 2026-08-06T23:26:25Z

- Active version: 23
- Report: reports/live-observe-20260806T232604Z


### Reviewer comparison of new uploads v21 and v22 — 2026-08-06T23:22:50Z

- New ready uploads v21 (id 36a7ff00-8cd5-4409-9698-57162b62cb8b, uploaded 2026-08-06T22:16:46.027Z; active externally at inspection) and v22 (id 948bffc1-0de9-4796-9557-88fa570f2a41, uploaded 2026-08-06T22:27:25.733Z; ready/inactive) were downloaded with fcode under reports/reviewer-new-uploads-20260807T231003Z/. Archive SHA-256 values: v21 6571049205e79ca3444c862518ef9e36ef9e1f02885a97c6198d19b671d74da6; v22 b2a6016af031ae3a0163d429c855c44f18dc6ea1f10bb88ed0e83ed0f6aee115.
- v21 direct battle against retained v0010/v20 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 136,150 versus 167,650 collected titanium, ratio 0.8121, 22/48 wins with three ties; zero stderr/exception/TLE markers (report reports/local-20260806T231050Z). v21 led crossfire, hive, and twins, but regressed sharply on bridge, showdown, and string.
- v22 direct battle against the same retained v0010/v20 baseline was command-clean but lost: 124,880 versus 131,640 collected titanium, ratio 0.9486, 15/48 wins with six ties; zero stderr/exception/TLE markers (report reports/local-20260806T231630Z). v22 led aurora, bridge, and strait, but collapsed on crossfire and string and tied all six showdown games.
- Fresh live observation reports v21 active externally at rating 1421.4360, rank 37/104, 170 matches, and 7-3 over the last ten series. Its latest series beat Bean counters 3-2 across moonrise/eider/hive/archipelago/drumlin; v22 remains inactive. Report: reports/live-observe-20260806T231003Z.
- Status: v21 and v22 REVIEWED — REJECTED FOR BASELINE; immutable v0010/v20 remains the local reviewer baseline. No challenger suites, source edits, upload, or activation were performed.


### Live observation captured — 2026-08-06T23:10:21Z

- Active version: 21
- Report: reports/live-observe-20260806T231003Z


### Live observation after v19 activation — 2026-08-06T22:33:42Z

- Fresh read-only fcode observation reports active external version 19; v20 is ready but inactive. Report: reports/live-observe-20260806T221248Z.
- Current team status is rating 1384.7777, rank 40/104, 163 matches, and 6-4 over the last ten series. The latest v19 series beat Prompt Engineers Anonymous 5-0, with wins on jackpot, atoll, snowflake, nordkap, and fjordgate; jackpot and fjordgate ended by core destruction, while the other three ended by titanium collection or storage.
- This live result is promising but is only one v19 series and does not override the 48-game local comparison, where v19 lost to v0010/v20. No platform activation was performed by the reviewer.


### Reviewer comparison of new uploads v19 and v20 — 2026-08-06T22:31:37Z

- New ready uploads v19 (id 1ce9f9d8-fe24-404f-bfa4-b2e71fde4847, uploaded 2026-08-06T21:09:15.569Z; active externally at inspection) and v20 (id 572e0c76-8d06-4358-baee-af765a702b57, uploaded 2026-08-06T21:24:58.819Z; ready/inactive) were downloaded with fcode under reports/reviewer-new-uploads-20260807T221248Z/. Archive SHA-256 values: v19 b2095202ae968aed014a4fbdfe24776925227d0e8147fc071fe4b9e85db38af8; v20 d4b63a0f5164f98a7db31f0348d6b91690b1cd1a27779c99c231e999a1392e91.
- v19 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 109,890 versus 132,150 collected titanium, ratio 0.8316, 24/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T221414Z). v19 led bridge, showdown, and string, but trailed heavily on crossfire, hive, and strait.
- v20 direct battle against the same retained v0009/v14 baseline was command-clean and won: 187,750 versus 102,100 collected titanium, ratio 1.8389, 32/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T222101Z). v20 led bridge, showdown, twins, crossfire, hive, aurora, and strait, with string as its only losing map.
- Winner validation passed: all 16 Python files AST-parsed with an explicit main.py Player class; immutable package v0010_reviewer-v20-platform-winner_20260806-2229_7dd72f03 is 16 files/200,497 unpacked bytes/50,894 archive bytes with SHA-256 ebe54c75e3ad7abf0338b393b820d81e354e51f7c1577d8edf9ee1796232be29; packaged smoke was 4/4 command-clean (reports/local-20260806T222949Z).
- v20 runner wall-clock p99/max were 19.7662/19.9528 seconds per game; the local runner does not expose controller CPU p99. No bot-source edits, new upload, or activation was performed by the reviewer; the platform remains externally active on v19.
- Status: v19 rejected as local comparator; v20 retained as the new immutable local reviewer baseline pending separate live observation.


### Live observation captured — 2026-08-06T22:13:15Z

- Active version: 19
- Report: reports/live-observe-20260806T221248Z


### Live observation after v17/v18 review — 2026-08-06T17:26:43Z

- Fresh read-only fcode observation reports active external version 16 (V0011_scenario); v17 and v18 are ready but inactive. Report: reports/live-observe-20260806T172454Z.
- Current team status is rating 1355.6550, rank 40/103, 132 matches, and 6-4 over the last ten series. The two newest v16 series were 1-4 versus PromptNPray and 1-4 versus Atlas; no activation was performed by the reviewer.
- The latest Atlas series ended on titanium collection in fjordgate, snowflake, heart, and drumlin, with one v16 core-destruction win on moonrise at turn 771. The PromptNPray series likewise had one v16 moonrise core-destruction win and four collection losses.


### Live observation captured — 2026-08-06T17:25:12Z

- Active version: 16
- Report: reports/live-observe-20260806T172454Z


### Reviewer comparison of new uploads v17 and v18 — 2026-08-06T17:24:36Z

- New ready uploads v17 (id 87faf1eb-e97d-42b4-b962-dade8d3136a4, uploaded 2026-08-06T15:52:09.262Z) and v18 (id 550767b7-1414-4df8-9263-a5a7494505cd, uploaded 2026-08-06T15:55:58.939Z) were downloaded without challenger unit/static/smoke suites under reports/reviewer-new-uploads-20260806T171055Z/. Archive SHA-256 values: v17 2d206bf71d08ebf99272e486c7dcaf55e1eabad84d14f91fae263de5f9606d43; v18 2644278a8ba91a56cdc96ea249b92e05b27183aee02b62ed99e148f36b1656c2.
- v17 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: 91,970 versus 95,310 collected titanium, ratio 0.9650, 24/48 wins and 27/48 positive-or-equal with three ties; zero stderr/exception/TLE markers (report reports/local-20260806T171101Z). v17 led bridge, aurora, and strait, but trailed crossfire, hive, twins, and string; showdown was a 5,070 versus 0 candidate-side total.
- v18 direct battle against the same retained v0009/v14 baseline was command-clean but lost: 94,830 versus 101,280 collected titanium, ratio 0.9363, 21/48 wins and no ties; zero stderr/exception/TLE markers (report reports/local-20260806T171729Z). v18 led bridge, showdown, twins, crossfire, and hive, but was weak on aurora, strait, and especially string.
- Runner wall-clock p99/max were 13.5050/13.5812 seconds for v17 and 20.9226/21.0511 seconds for v18; the local runner does not expose controller CPU p99. No challenger tests, activation, upload, or bot-source changes were performed.
- Status: v17 and v18 REVIEWED — REJECTED FOR BASELINE; immutable v0009/v14 remains the reviewer baseline.


### Live observation captured after v16 review — 2026-08-06T15:17:49Z

- Active version: 14; report: reports/live-observe-20260806T151713Z
- Current team status: rating **1260.25**, rank **47/103**, recent record **7-3** over the last ten series. The latest v14 series was **1-4** versus StarTrekker; v15 and v16 remain inactive.


### Live observation captured — 2026-08-06T15:17:31Z

- Active version: 14
- Report: reports/live-observe-20260806T151713Z


### Reviewer comparison of new upload v16 — 2026-08-06T15:16:12Z

- New ready upload v16 `V0011_scenario` was downloaded without challenger unit/static/smoke suites under `reports/reviewer-new-uploads-20260806T150832Z/`; archive SHA-256 is `9ddf84c43dad24e22957fbdc8355b43b4b592e74eaa3e040534898ed565f07bf`.
- v16 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: **117,480** versus **150,840** collected titanium, ratio **0.7788**, **15/48** wins (**18/48** positive-or-equal with three ties), zero stderr/exception/TLE markers (report `reports/local-20260806T150838Z`). v16 led bridge and aurora, was close on crossfire, and trailed heavily on showdown, hive, string, twins, and strait.
- The platform remains on active v14; at inspection the team was rating **1272.87**, rank **47/103**, and **8-2** over the last ten series. No v16 activation or source change was performed.
- Status: **v16 REVIEWED — REJECTED FOR BASELINE; v0009/v14 RETAINED.**


### Live observation captured after v15 review — 2026-08-06T15:00:38Z

- Active version: 14; report: reports/live-observe-20260806T145957Z
- Current team status: rating **1257.64**, rank **47/103**, recent record **7-3** over the last ten series. The latest v14 series in the snapshot was **4-1** versus Klarum; v15 remained inactive.


### Live observation captured — 2026-08-06T15:00:21Z

- Active version: 14
- Report: reports/live-observe-20260806T145957Z


### Reviewer comparison of new upload v15 — 2026-08-06T14:59:02Z

- New ready upload v15 `V0009_farmfirst` was downloaded without challenger unit/static/smoke suites under `reports/reviewer-new-uploads-20260806T144942Z/`; archive SHA-256 is `d9d9cf06da71f9d8cdc43ea0c68acb3baba192434576f91666cafa543f8ab4e4`.
- v15 direct battle against retained v0009/v14 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean but lost: **192,530** versus **250,080** collected titanium, ratio **0.7699**, **15/48** wins, zero stderr/exception/TLE markers (report `reports/local-20260806T144947Z`). v15 led bridge and string, was roughly even on strait, and trailed heavily on showdown, twins, hive, aurora, and crossfire.
- The platform remains on active v14; no v15 activation or source change was performed. v0009/v14 remains the local reviewer baseline.
- Status: **v15 REVIEWED — REJECTED FOR BASELINE; v0009/v14 RETAINED.**


### Reviewer comparison of new uploads v13 and v14 — 2026-08-06T14:47:10Z

- New ready uploads v13 `V0008mapaware` and v14 `V0010_runtimeapi` were downloaded without challenger unit/static/smoke suites under `reports/reviewer-new-uploads-20260806T142952Z/`. Archive SHA-256 values: v13 `c5cd172375b9e7ebf1d993556294bbe8b0e35bc68a09ef2eed20e901d0740c1b`, v14 `622f0ca76d2ed2b49ae94a2d91a67829aa809634751728986d5049aa2de497c1`.
- v13 direct battle against v0008 was command-clean but lost: **139,590** versus **182,280** collected titanium, ratio **0.7658**, **18/48** wins, zero stderr/exception/TLE markers (report `reports/local-20260806T142959Z`). It was especially weak on showdown (0), crossfire, string, and twins; only hive was strongly positive.
- v14 direct battle against v0008 was command-clean and won: **105,350** versus **74,860** collected titanium, ratio **1.4073**, **29/48** wins, zero stderr/exception/TLE markers (report `reports/local-20260806T143942Z`). v14 led crossfire, hive, strait, string, and twins; it trailed on bridge, aurora, and showdown.
- Fresh live observation `reports/live-observe-20260806T144506Z` shows v14 active and ready with rating **1244.95**, rank **48/103**, recent record **7-3**. Its newest completed series was **5-0** versus 1337; all five games ended by `core_destroyed` between 322 and 900 turns. This is promising but still only one v14 series.
- The winning v14 archive was snapshotted as immutable local baseline `bots/versions/v0009_reviewer-v14-platform-winner_20260806-1446_7dd72f03`; package SHA-256 `b013b1214b7832a30600166985e5a569515bb593509bb5d4773a95f66c6c6a11` and manifest are under `artifacts/submissions/`. No bot source was edited and no activation was performed by the reviewer; v14 was already externally active.
- Status: **NEW-UPLOAD REVIEW COMPLETE — v0009/v14 retained as baseline; continue live observation for map and reliability variance.**


### Live observation captured — 2026-08-06T14:45:24Z

- Active version: 14
- Report: reports/live-observe-20260806T144506Z


### Reviewer comparison of new uploads v11 and v12 — 2026-08-06T14:18:28Z

- New ready uploads were reviewed without challenger unit, static, smoke, or other test suites: v11 `v0007_mass-build` (archive SHA-256 `74095a3bdedfe4e0fa645c450d061447a54449a78a5e14aa4fd28148ac15c1c9`) and v12 `V0009workforce` (archive SHA-256 `45b1e8df3ba7f79ed9a8e8ac1a862a0f2fc18090b2977b4f49ff299c29b218a4`); downloads/extractions are under `reports/reviewer-new-uploads-20260806T1329Z/`.
- v11 direct battle against retained local v0008 on bridge/showdown/twins/crossfire/hive/string/aurora/strait with seeds 1/19/101 was command-clean: **177,820** versus **182,070** collected titanium, ratio **0.9767**, **24/48** wins and **24/48** positive-or-equal rows, zero stderr/exception/TLE markers (report `reports/local-20260806T140632Z`). v11 was not retained as baseline.
- v12 was harness-invalid before gameplay in all 48 invocations: `bot/builder.py:1884` contains a forbidden `finally` block (rc 10/11; report `reports/local-20260806T141621Z`). No score was assigned and no challenger tests were run. The platform also recorded a rated v12 0-5 compilation-error series versus OpenSverige before returning to active v11.
- Fresh platform observation `reports/live-observe-20260806T141701Z` shows v11 currently active and ready, rating **1220.75**, rank **51/103**, recent record **4-6**. Its only completed rated series was **2-3** versus Kvarnholmen (lighthouse/snowflake/moonrise/drumlin/archipelago; two core-destroyed wins, three titanium losses). This is weak live evidence and does not displace the local v0008 baseline or authorize activation.
- Status: **NEW-UPLOAD REVIEW COMPLETE — v0008 retained; v11/v12 not promoted; no bot source changes.**


### Live observation captured — 2026-08-06T14:17:24Z

- Active version: 11
- Report: reports/live-observe-20260806T141701Z


### External platform version switch observed — 2026-08-06T13:26:50Z

- Fresh report reports/live-observe-20260806T132442Z shows platform version 9 active and ready; this differs from the reviewer-activated v10. No v9 activation was performed in this workflow, so the switch is recorded as external and v9 is not treated as the approved winner.
- The latest completed ladder series is 5-0 for 1337 over Kleos while Kleos was still on version 8. The two recorded v10 series remain 3-2 versus Leviathan and 0-5 versus Albert And Einstein; no completed series in the latest 100 references v9.
- Current team status is rating 1200.84, rank 52/103, and 3-7 over the last ten series. Local baselines, tests, the v10 package, and the draft PR are unchanged; no platform reactivation was performed.


### Live observation captured — 2026-08-06T13:25:04Z

- Active version: 9
- Report: reports/live-observe-20260806T132442Z


### Platform v10 live performance review — 2026-08-06T13:15:30Z

- Fresh observation report reports/live-observe-20260806T131416Z confirms platform v10 remains active and ready. Team status is rating 1215.73, rank 51/103, and 3-7 over the last ten rated series.
- The first two v10-rated series are complete: 3-2 versus Leviathan (wins on atoll, heart, snowflake; losses on eider and fjordgate, with the fifth ending by core_destroyed) and 0-5 versus Albert And Einstein (saga, atoll, lighthouse, hive, antler; four losses ended by core_destroyed).
- This is 3-7 games across only two series: live performance is currently volatile/weak, but the sample is too small for rollback or promotion. v2 remains the rollback target and the local v0008 baseline is unchanged.


### Live observation captured — 2026-08-06T13:14:35Z

- Active version: 10
- Report: reports/live-observe-20260806T131416Z


### Reviewer-only final winner review and activation — 2026-08-06T12:55:14Z

- Unseen challengers v8 and v9 were downloaded/extracted under reports/reviewer-workflow-20260806T1202Z/ without unit, static, smoke, or other challenger test suites. Archive hashes are v8 `f639e177d4ef54d93e9f656f24c38f2284de6ee855eaaa462d2c8cf892aff0b7` and v9 `02f0c0ec8a01fa80caf17d1dc28d06a8d8f151978d35c9001e10059edc3b0e8b`. v8 was rejected before games in all 48 invocations because bot/builder.py contains a disallowed finally block (reports/local-20260806T124537Z). v9 completed its direct battle but lost to the retained baseline: 168,600 versus 174,450 collected titanium, ratio 0.9665, 18/48 wins, zero command failures/stderr/exception/TLE markers (reports/local-20260806T124555Z).
- The retained local v0008 winner remained best after all direct comparisons. Winner-only validation had make static 146/146 plus compileall, make smoke 4/4 (reports/local-20260806T122712Z), and the release matrix 210/210 command-clean (reports/local-20260806T122741Z): 953,940 versus 748,370 collected titanium against the immutable v0006 comparator, ratio 1.2747, 110/210 wins, 120/210 positive-or-equal rows, zero failures/stderr/exception/TLE markers, runner wall p99 6.2904 s/game (CPU p99 not exposed).
- Winner review found strong maps atoll, aurora, pinch, runestone, sprint, and vault, but material regressions on showdown (0/8,050), quarry (2,000/15,500), twins (20,050/42,300), and longship (25,750/27,250); route-count/first-delivery telemetry and controller CPU p99 remain unavailable.
- Package artifacts/submissions/v0008_reviewer-current-best_20260806-1209_3f2505d7.zip was uploaded through the guarded live operator as platform version 10 (SHA-256 8e15f02b880c1b0688d6d55d0f351a5ed9edc3029effa7113a2ceafc44eea52e) and activated. Previous active version 8 and known-good rollback version 2 are preserved; deployment report is reports/live-deploy-20260806T125258Z and state/live_state.json is active_observing.
- Post-activation observation reports/live-observe-20260806T125327Z confirms active version 10, ready status, team rating 1242.52, rank 48/103, recent record 4-6. No completed ladder series references version 10 yet; the available completed matches predate activation, so no live score is claimed.
- Status: REVIEW COMPLETE — v0008 retained as local baseline and activated as platform v10; continue reviewer-only live observation and keep v2 available for rollback.


### Live observation captured — 2026-08-06T12:53:44Z

- Active version: 10
- Report: reports/live-observe-20260806T125327Z


### Candidate activated — 2026-08-06T12:53:19Z

- Version: 10
- Previous/rollback: 2
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260806T125258Z


### Candidate uploaded — 2026-08-06T12:53:18Z

- Candidate: v0008-reviewer-current-best-20260806
- Version: 10
- Rollback target: 2
- Report: reports/live-deploy-20260806T125258Z


### Live state bootstrapped — 2026-08-06T12:52:48Z

- Active version: 8
- Report: reports/live-bootstrap-20260806T125229Z


### Live observation captured — 2026-08-06T12:25:25Z

- Active version: 6
- Report: reports/live-observe-20260806T122500Z

### Reviewer-only submission comparison workflow — 2026-08-06T12:25:25Z

- User directive: from this checkpoint onward, Codex acts only as a reviewer. Compare the current local bot first, then pull ready platform submissions not previously reviewed and pit each against the strongest retained baseline. Do not run unit, static, smoke, or other test suites on challenger submissions. Run winner-only validation and review after the comparison series; activate the winner and retain it as the future baseline when authorized.
- First comparison: current `bots/candidate` versus `bots/versions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7`, report `reports/local-20260806T120456Z`, candidate **203,670** versus comparator **179,210** collected titanium (ratio **1.1365**), **21/48** wins, zero command failures/stderr. The winner was snapshotted as `bots/versions/v0008_reviewer-current-best_20260806-1209_3f2505d7` and is now the configured local baseline.
- Previously unseen ready platform submissions downloaded without code tests: v4 (`02efe306be3d9209372d6c1ef3f28fdddb91250312f0c6f26999461a98d0797d`), v5 (`5e0ca6729f81efc340049455e4c04520d1513c81333c81540a8d36a117121b0f`), v6 (`a98c94fc0cbf0f5c748fe07557444b71f826d8df6fb12f29c0c59e0b577fe0df`), and v7 (`4a344705277eb61dad0b1f493c601b6a51bcc7de0978a36b4af4920525094011`). Archives and extraction directories are under `reports/reviewer-workflow-20260806T1202Z/`.
- Direct comparisons against the retained v0008 baseline: v4 **106,770/141,810 = 0.7529**, **18/48** wins (`reports/local-20260806T120935Z`); v5 **115,590/157,440 = 0.7342**, **15/48** wins (`reports/local-20260806T121407Z`); v6 **115,700/158,160 = 0.7315**, **15/48** wins (`reports/local-20260806T121917Z`). All completed with zero command failures/stderr; no challenger test suites were run.
- v7 was rejected at the battle harness boundary: all 48 invocations failed validation because `bot/builder.py` contains a disallowed `finally` block (`reports/local-20260806T122423Z`). It was not tested further.
- Live review snapshot: `reports/live-observe-20260806T122500Z`; the platform currently reports active official version **6**, rating **1279.89**, rank **46/103**, recent record **7–3** over the last ten series. The three newest completed series were **3–2**, **5–0**, and **0–5** (8/15 games); no live series has evaluated the new local v0008 winner yet.
- Status: **COMPARISON COMPLETE — v0008 RETAINED; WINNER-ONLY VALIDATION AND ACTIVATION PENDING**.


### Iteration 1 — Four-route economy expansion — passed 2026-08-06T11:17:04Z

- Objective/scope: remove the three-project ceiling, preserve route 0, authorize at most two secondary route projects after a fresh route-0 delivery heartbeat, and keep delayed Store assignment deterministic. Allowed files were `bots/candidate/bot/{comms,core,economy,builder,feature_flags}.py`, expansion/economy/communication/route/player tests, evaluation configs, and the current plan. Navigation, combat, turret, launcher, redundancy, snapshots, and platform operations were non-goals.
- Files changed in this checkpoint: `docs/CURRENT_PLAN.md`; candidate `comms.py`, `core.py`, `economy.py`, `builder.py`, `feature_flags.py`; `tests/test_candidate_comms.py`, `test_candidate_economy.py`, `test_candidate_economy_logistics.py`, `test_candidate_expansion.py`, `test_candidate_player.py`; and `configs/eval_regression.toml`, `eval_smoke.toml`, `eval_matrix.toml`.
- Behavior: Store schema 4 adds `PROJECT_3` at slot 13 and `CLAIM_3` at slot 15; project/claim codecs and ownership validation cover all four indices. Core protects route 0, counts delayed assignments toward the two-secondary limit, retains failed ore for a bounded cooldown, and computes 5/6/7 Builder demand for bootstrap/expansion/four-route maintenance. Builders retain their own project reservation at the four-project cap and release delayed ore collisions to the higher project index.
- Tests: focused economy/comms/route/player/expansion **63/63 passed**; `make static` **139/139 plus compileall**; `make smoke` **4/4 command-clean** (`reports/local-20260806T111646Z`); paired previous-iteration checkpoint **48/48 command-clean**, zero stderr/runtime failures (`reports/local-20260806T111704Z`). Full details: `reports/local-20260806T111704Z/iteration1-summary.md`.
- Metrics against the immutable workspace Iteration 7 comparator `bots/versions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7`: candidate **230,970** versus comparator **188,320** collected titanium (ratio **1.2265**), candidate wins **27/48**, collection-positive **27/48**. Runner wall-clock p99 was **4.621 s/game**; controller CPU p99 is not exposed by the local runner. All games completed normally under the 10 ms turn limit.
- Remaining risks: route-count and first-delivery telemetry are not emitted by the runner; map-level collection variance remains; active platform version was not changed. Iteration 2 work-intent/idling changes have not started.
- Iteration status: **ITERATION 1 PASSED — READY FOR ITERATION 2**.

### Remote gate result — 2026-08-06T10:20:30Z

- Match `51a5362b-28b0-4b03-a198-fbb6df4ec73c` completed unrated **2–3** against the immutable v0005 comparator. The candidate won `crossfire` and `vault`; the comparator won `sprint`, `bridge`, and `aurora`.
- All five games reached 1,000 turns and ended by `titanium_collected`; no resignation, exception, TLE, or platform error was reported. Evidence summary: `reports/remote-20260806T095713Z/result.md`.
- This remote result does not alter the already active version 3; automatic rollback remains guarded by the configured live observation policy.

### Final release and activation — 2026-08-06T10:19:39Z

- Final review repair: corrected direct offensive-target scoring so callers can apply the stale-target TTL; the focused suite, static/compileall, smoke, selected 48-game regression, and the full release matrix were rerun afterward and remained clean.
- Final evidence: focused/static **135/135** plus compileall; final smoke **4/4** (`reports/local-20260806T102140Z`); selected previous-iteration regression **48/48** (`reports/local-20260806T100021Z`); release matrix **210/210** (`reports/local-20260806T100335Z`). Candidate collection was **856,350** versus **778,320** comparator (ratio **1.1003**), with **125/210** wins and zero command failures/stderr/exception/TLE markers.
- Package: [`v0006_iter7-integrated-20260806_20260806-1018_3f2505d7.zip`](artifacts/submissions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7.zip), SHA-256 `2c119f48ec23880cd0a11b0747f03995c180ca8c3228096efdb55e9e4e5141bb`; manifest records 18 files and 45,536 archive bytes.
- Platform action authorized by the user: bootstrapped ready active version **2** as rollback target, uploaded candidate `v0006-iter7-integrated-20260806`, received ready version **3**, and activated it. Deployment evidence: `reports/live-deploy-20260806T101840Z`; current state: `state/live_state.json` is `active_observing`, active **3**, rollback **2**.
- Post-activation verification: observation captured active version 3 at `reports/live-observe-20260806T101924Z`; no live score is claimed yet because the observation window has not produced rated series.
- Remaining risks: map-level local variance (bridge/showdown/vase), remote gate match `51a5362b-28b0-4b03-a198-fbb6df4ec73c` remains queued, and live score/reliability evidence is pending the configured observation window. Automatic rollback remains enabled with version 2 as the known-good target.
- Release status: **ACTIVATED — OBSERVING**.

### Live observation captured — 2026-08-06T10:19:39Z

- Active version: 3
- Report: reports/live-observe-20260806T101924Z


### Candidate activated — 2026-08-06T10:18:55Z

- Version: 3
- Previous/rollback: 2
- Observation state persisted in state/live_state.json
- Report: reports/live-deploy-20260806T101840Z


### Candidate uploaded — 2026-08-06T10:18:55Z

- Candidate: v0006-iter7-integrated-20260806
- Version: 3
- Rollback target: 2
- Report: reports/live-deploy-20260806T101840Z


### Live state bootstrapped — 2026-08-06T10:18:21Z

- Active version: 2
- Report: reports/live-bootstrap-20260806T101807Z


### Live state bootstrapped — 2026-08-06T10:18:14Z

- Active version: 2
- Report: reports/live-bootstrap-20260806T101800Z


### Live state bootstrapped — 2026-08-06T10:17:27Z

- Active version: None
- Report: reports/live-bootstrap-20260806T101711Z


### Release gate — Iterations 4–7 complete; Iteration 3 user-authorized skip — 2026-08-06T09:58:31Z

- Scope/status: Iteration 3 was explicitly skipped by the user after the current plan classified 3R route reliability as passed. Iterations 4 (controlled multi-route economy), 5 (reactive defense), 6 (bounded offensive primitives), and 7 (integrated phase strategy) were implemented sequentially. Each iteration kept its documented non-goals and was validated before the next started.
- Files changed: `bots/candidate/bot/{builder,comms,core,defense,economy,feature_flags,navigation,offense,policy,turrets,types,world}.py`; focused tests for economy, expansion, defense, offense, route FSM, comms, policy, player, and static contracts; evaluation configs; `docs/CURRENT_PLAN.md`, `docs/NEXT_ITERATIONS_PLAN_UPDATED.md`, `docs/START_HERE.md`; `state/project_state.json` and this checkpoint log.
- Validation: focused/static suite **135/135** plus compileall passed; final smoke **4/4** command-clean (`reports/local-20260806T095636Z`); selected paired previous-iteration regression **48/48** command-clean with no stderr or exception/TLE markers (`reports/local-20260806T093757Z`); release matrix **210/210** command-clean with zero failures (`reports/local-20260806T094203Z`).
- Release metrics against immutable previous-best comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: candidate collected **856,350** versus **778,320** comparator titanium (ratio **1.1003**), candidate won **125/210** games and exceeded comparator collection on **125/210** rows. All games ended by the normal `titanium_collected` condition; no stderr, exception, or TLE markers were observed.
- Remote gate: the sandbox attempt failed DNS without changing platform state (`reports/remote-20260806T095701Z`); the authorized network retry succeeded in submitting remote test `51a5362b-28b0-4b03-a198-fbb6df4ec73c` (`reports/remote-20260806T095713Z`), currently queued when recorded.
- Remaining risks: several individual maps remain below the comparator (notably bridge, showdown, and vase), the remote test result is still queued, and live activation/observation remains pending rollback bootstrap. These are recorded before deployment; no claim of live success is made here.
- Iteration status: **RELEASE_READY_PENDING_LIVE_BOOTSTRAP**.

### NEXT Iteration 7 integrated phase strategy — passed 2026-08-06T09:57:00Z

- Objective/scope: integrate economy readiness, reactive defense overlays, offensive preparation/pressure, stable role allocation, and endgame spending guards. Allowed files were the strategy/policy/core/builder/comms/defense/offense/turret surfaces plus focused tests and feature flags. Navigation algorithms, Store schema, map-specific policy, and launcher activation were non-goals.
- Done criteria: deterministic phase transitions, persistent defenders, project-owner precedence, no early offensive spending, stale-target retreat, and launcher/feature isolation all passed in focused tests; selected previous-iteration regression remained command-clean and aggregate-positive.
- Files/tests: `bots/candidate/bot/policy.py`, `core.py`, `builder.py`, `comms.py`, `feature_flags.py`, `tests/test_candidate_world_policy.py`, `tests/test_candidate_comms.py`, `tests/test_candidate_route_fsm.py`, `tests/test_candidate_player.py`; focused/static/smoke and release-matrix evidence is recorded in the release-gate entry above.
- Metrics: selected 8-map/3-seed paired regression **48/48**, candidate **203,080** vs comparator **201,340** (ratio **1.0086**, all rows positive); full release matrix **210/210** command-clean.
- Remaining risks/status: map-level variance remains; Iteration 7 **PASSED** and release gate is ready once live rollback state is bootstrapped.

### NEXT Iteration 6 offensive primitives — passed 2026-08-06T09:56:00Z

- Objective/scope: add legal, bounded target selection, builder attacks only against enemy buildings, verified enemy-core publication, safe attack stances, forward-turret support, retreat/regroup guards, and late-game spending suppression. Defense construction, launcher enablement, and unrestricted early raids were non-goals.
- Done criteria: target hierarchy/core override, legality gates, forward support, stale-target retreat, and endgame suppression were covered by focused tests; the phase-enabled regression prevented early offensive spending.
- Files/tests: `bots/candidate/bot/offense.py`, offense sections of `builder.py`/`comms.py`, `tests/test_candidate_offense_endgame.py`, plus feature-flag and player regression coverage. Focused suite **135/135**, static/compileall, smoke, selected regression, and full matrix passed.
- Remaining risks/status: offensive pressure is intentionally gated behind stable economy and fresh verified targets; Iteration 6 **PASSED**.

### NEXT Iteration 5 reactive defense — passed 2026-08-06T09:55:00Z

- Objective/scope: implement threat reports with freshness, defense hysteresis, stable defender assignment, protected-asset fire priority, positive-gain Gunner rotation, and bounded ammo conversion. Economy route construction and offensive/launcher activation were non-goals.
- Done criteria: fresh core damage reaches critical mode, stale reports recover, defender choices remain stable, zero-value rotations spend nothing, and reserves survive all defense decisions.
- Files/tests: `bots/candidate/bot/{types,comms,defense,turrets,core}.py`, `tests/test_candidate_defense.py`, and related player/core combat tests. Focused suite **135/135**, static/compileall, smoke, selected regression, and full matrix passed.
- Remaining risks/status: defense is reactive and reserve-capped; Iteration 5 **PASSED**.

### NEXT Iteration 4 controlled multi-route economy — passed 2026-08-06T09:54:00Z

- Objective/scope: extend the proven first route to sequential profitable expansion with project-local FSM/heartbeats, payback and liquidity guards, deterministic ore ranking, and productive-idle behavior. Combat, defense construction, offensive behavior, launchers, and navigation algorithm changes were non-goals.
- Done criteria: first-route health always precedes secondary assignment, one project builds at a time, failed routes replan without invalidating healthy routes, and economic reserves remain bounded.
- Files/tests: `bots/candidate/bot/{economy,core,builder,comms,types,feature_flags}.py`, `tests/test_candidate_economy.py`, `tests/test_candidate_expansion.py`, `tests/test_candidate_route_fsm.py`, and static budget contract. Focused suite **135/135**, static/compileall, smoke, selected regression, and full matrix passed.
- Metrics: selected paired regression **48/48** command-clean and aggregate-positive versus the previous iteration comparator; full release matrix later confirmed **856,350 / 778,320 = 1.1003** aggregate collection.
- Remaining risks/status: per-map output variance is retained for release review; Iteration 4 **PASSED**.

### NEXT Iteration 3R comparator-scaling diagnosis — blocked 2026-08-06T00:16:11Z

- Objective/scope: restate the post-repair6 divergence, compare one seed-1 A-side trace for each selected map, and apply at most one evidence-scoped first-route Builder/logistics/navigation/world repair. Allowed files were that first-route surface, focused tests, and checkpoint metadata. Iteration 4, secondary expansion, combat, Store changes, and comparator replacement were non-goals. The done criteria were deterministic classification, focused/static/smoke/exact-regression validation, and every 3R promotion gate.
- Files changed: no production bot or test source changed in this diagnosis. Added the offline diagnosis summary `reports/route-iteration3r-diagnosis-20260806T0009/summary.md`; checkpoint logs/config are under `reports/route-iteration3r-repair7-20260806T0013/`. Temporary trace copies were removed; trace artifacts remain under the diagnosis report.
- Differential evidence: the candidate built one own Harvester and reached first delivery/`MAINTAIN` on all five sampled maps (`sprint` 16, `string` 12, `bridge` 24, `vault` 12, `aurora` 16). The frozen comparator built 3, 2, 2, 2, and 2 own Harvesters respectively. Candidate collections were 2,470/2,480/2,450/2,480/2,470 versus comparator 7,410/4,910/4,800/4,960/2,660. The candidate's secondary-expansion gate is explicitly false and claim slots other than 0 are rejected.
- Tests/results: focused **72/72** (`focused.log`); `make static` **118/118** plus compileall (`static.log`); `make smoke` **4/4**, report `reports/local-20260806T001359Z` (`smoke.log`); exact selected regression **36/36**, report `reports/local-20260806T001611Z` (`regression.log`), zero nonzero returns/stderr and no exception/TLE output markers. The unrelated default `make eval-regression` attempt (9 maps, seeds 1/19/101) completed 54/54 and is preserved in `regression-default-9map.log` with report `reports/local-20260806T001417Z`.
- Metrics versus immutable comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: candidate collection **88,950** versus **170,960** (52.0297%, below the required 90% / 153,864); candidate mean **2,470.8** versus comparator **4,748.9**; proxy **36/36** positive; candidate wins **3/36**. A one-Harvester upper bound is 90,000 Ti (`2.5 * 1000 * 36`), so the measured candidate is near the isolation ceiling. Route churn remains unmeasured.
- Decision/risk: no admissible repair exists within Iteration 3's explicit “do not add a second Harvester” rule that can satisfy the aggregate gate against this multi-route comparator. Enabling secondary expansion would violate the plan; changing the frozen comparator would invalidate the baseline. The comparator-scaling conflict is deterministic and recorded in `reports/route-iteration3r-diagnosis-20260806T0009/summary.md`.
- Review/status: `git diff --check` and complete-diff self-review are required at checkpoint. Iteration 3R remains **BLOCKED**; do not start Iteration 4 until the plan/baseline conflict receives an explicitly scoped decision.

### NEXT Iteration 3R ore-occupancy checkpoint — blocked 2026-08-06T00:02:28Z

- Objective/scope: trace the live bridge adjacent/build transition and apply one bounded repair only. The first divergence was a non-target Builder following the unreachable `(0,0)` waypoint onto the selected ore tile; the route Builder then could not build the Harvester. The repair skips known ore tiles during non-target movement. No economy policy, Store, combat, expansion, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/builder.py` and `tests/test_candidate_route_fsm.py`; pre-edit traces and replays are under `reports/route-iteration3r-diagnosis-20260805T2354/`, checkpoint logs under `reports/route-iteration3r-repair6-20260805T2354/`.
- Tests/results: focused 72/72; `make static` 118/118 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260806T000101Z`. Regression report: `reports/local-20260806T000228Z`.
- Metrics versus the immutable Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: proxy improved to 36/36 (100%), bridge improved to 6/6, candidate wins 3/36, and collection improved to 88,950 total / 2,470.8 mean versus comparator 170,960 total / 4,748.9 mean (52.0% aggregate, below 90%). Full 21-map matrix was not run.
- Differential evidence: the repair removes the persistent bridge ore blocker and produces a Harvester on both sides, but the remaining aggregate throughput/output gap is unresolved. Summary: `reports/route-iteration3r-repair6-20260805T2354/summary.md`.
- Remaining risk/next plan: route churn remains unmeasured; classify post-delivery output, acknowledgement, repair, or multi-route divergence before another edit. Plan: `reports/route-iteration3r-repair6-20260805T2354/next-diagnosis-plan.md`.
- Review/status: Iteration 3R is **BLOCKED** because the comparator aggregate gate failed despite proxy/bridge recovery. Stop here and do not start Iteration 4.

### NEXT Iteration 3R adjacent-stance checkpoint — blocked 2026-08-05T23:43:00Z

- Objective/scope: reproduce the adjacent-stance oscillation and apply one bounded navigation repair only. A fake one-cell scenario showed an empty adjacent-goal set caused `Navigator._fallback()` to raise and adjacent movement to enter arbitrary fallback. No economy, Store, combat, expansion, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/navigation.py`, `bots/candidate/bot/builder.py`, and `tests/test_candidate_builder_navigation.py`; logs and reports are under `reports/route-iteration3r-repair5-20260805T2343/`.
- Tests/results: focused 71/71; `make static` 117/117 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260805T234438Z`. Regression report: `reports/local-20260805T234458Z`.
- Metrics versus the latest passed Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: collection/first-delivery proxy remained 30/36 (83.3%), candidate wins 0/36, candidate collection 74,310 total / 2,064.2 mean versus comparator 191,360 total / 5,315.6 mean (38.8% aggregate), and `bridge` remained 0/6. No row-level improvement; full 21-map matrix was not run.
- Differential evidence: the synthetic no-goal adjacent case now waits for two turns and moves when the Builder leaves, but the live bridge category is unchanged. The next diagnosis must capture nonempty-goal path rejection, cooldown, or another occupancy conflict before further editing. Summary: `reports/route-iteration3r-repair5-20260805T2343/summary.md`.
- Remaining risk/next plan: `reports/route-iteration3r-repair5-20260805T2343/next-diagnosis-plan.md`; route churn remains unproven by the replay harness.
- Review/status: `git diff --check` passed and no diagnostic markers remain; Iteration 3R is **BLOCKED** because the promotion gate failed after this repair. Stop here and do not start Iteration 4.


### NEXT Iteration 3R post-repair navigation checkpoint — blocked 2026-08-05T23:36:00Z

- Objective/scope: trace the first post-repair `bridge` divergence and apply one bounded navigation/layout repair only. The trace showed completed Conveyor routes followed by adjacent-stance oscillation when a friendly Builder occupied a passable route cell. No Core spawning, Store, combat, expansion, advanced spending, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/world.py` and `tests/test_candidate_world_policy.py`; diagnostic traces and checkpoint reports are under `reports/route-iteration3r-diagnosis-20260806T0000/` and `reports/route-iteration3r-repair4-20260805T2336/`.
- Tests/results: focused 70/70; `make static` 116/116 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260805T233655Z`. Regression report: `reports/local-20260805T233713Z`.
- Metrics versus the latest passed Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: collection/first-delivery proxy remained 30/36 (83.3%), candidate wins 0/36, candidate collection 74,310 total / 2,064.2 mean versus comparator 191,360 total / 5,315.6 mean (38.8% aggregate), and `bridge` remained 0/6. No row-level improvement; full 21-map matrix was not run.
- Differential evidence: candidate Builder 3/4 completed the five-cell route but never built the Harvester; a friendly Builder occupied the final Conveyor/stance cell and the adjacent Navigator oscillated. The comparator delivered around rounds 12–16. Trace summary: `reports/route-iteration3r-repair4-20260805T2336/summary.md`.
- Remaining risk/next plan: the cell is now classified as navigation-blocked while remaining route-layout-passable, but the FSM still needs a bounded wait/alternative-stanza diagnosis. Next plan: `reports/route-iteration3r-repair4-20260805T2336/next-diagnosis-plan.md`.
- Review/status: `git diff --check` passed; temporary diagnostic copies were removed; Iteration 3R is **BLOCKED** because the promotion gate failed after this repair. Stop here and do not start Iteration 4.


### NEXT Iteration 3R newly scoped repair checkpoint — blocked 2026-08-05T23:23:00Z

- Objective/scope: diagnose the remaining `bridge` route divergence. One bounded repair was allowed in the Builder route planner/build FSM: ignore friendly transient Builder occupancy during static layout search, wait for a friendly Builder to clear the next build cell, and retain bounded replan/failure handling. No Core spawning, Store, combat, expansion, advanced spending, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/builder.py` and `tests/test_candidate_route_fsm.py`; logs and checkpoint reports are under `reports/route-iteration3r-repair3-20260805T2323/`.
- Tests/results: focused 69/69; `make static` 115/115 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr and no exception/TLE markers. Smoke report: `reports/local-20260805T232347Z`. Regression report: `reports/local-20260805T232406Z`.
- Metrics versus the latest passed Iteration 2 comparator `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`: collection/first-delivery proxy remained 30/36 (83.3%), candidate wins 0/36, candidate collection 74,310 total / 2,064.2 mean versus comparator 191,360 total / 5,315.6 mean (38.8% aggregate), and `bridge` remained 0/6. No row-level improvement; full 21-map matrix was not run.
- Differential evidence: deterministic fake-controller coverage proves static route stability and temporary wait/recovery with two friendly Builders in a one-cell corridor, but the live `bridge` category did not improve. The next diagnosis must trace whether the first blocked build cell is a Builder-FSM deadlock or a separate earlier divergence; report: `reports/route-iteration3r-repair3-20260805T2323/summary.md`.
- Remaining risk/next plan: `reports/route-iteration3r-repair3-20260805T2323/next-diagnosis-plan.md`. Route churn remains unproven by the exact replay harness.
- Review/status: `git diff --check` passed; diagnostic markers were removed from submitted source; Iteration 3R is **BLOCKED** because the promotion gate failed after this repair. Stop here and do not start Iteration 4.


### NEXT Iteration 3R bounded repair checkpoint — blocked 2026-08-05T23:10:00Z

- Objective/scope: diagnose the earliest route divergence and repair only the first-route Builder/economy path. Two bounded repairs were applied: ignore the current Builder's own tile during route planning, and move scouts to deterministic waypoints instead of parking on known ore. No Core spawning, Store, combat, second Harvester, advanced spending, or Iteration 4 work was added.
- Files changed: `bots/candidate/bot/builder.py` and `tests/test_candidate_route_fsm.py`; diagnostic traces and checkpoint reports are under `reports/route-iteration3r-diagnosis-20260806T0100/` and `reports/route-iteration3r-repair2-20260805T2310/`.
- Tests/results: focused 68/68; `make static` 114/114 plus compileall; `make smoke` 4/4; exact selected regression 36/36 command-clean with zero stderr. Smoke report: `reports/local-20260805T230907Z`. Regression report: `reports/local-20260805T230927Z`.
- Metrics: collection/first-delivery proxy improved from 12/36 to 30/36 (83.3%), still below 34/36; candidate wins 0/36; candidate mean collection 2,064.2 versus 5,315.6 for the current paired Iteration 2 comparator (38.8% aggregate, below 90%); `bridge` remained 0/6. No comparator row improved. All isolation flags remain false; full 21-map matrix was not run.
- Differential evidence: self-Builder occupancy was the first `string` divergence; scout occupancy of the ore tile caused the next `vault`/`string` Harvester-build denial; after both repairs, `bridge` still fails because transient Builder occupancy makes route search return no route even though the static-layout probe succeeds. Trace rows and classifications are in `reports/route-iteration3r-repair2-20260805T2310/summary.md`.
- Remaining risk/next plan: transient Builder occupancy must be separated from static route-layout planning while retaining bounded enemy/permanent-obstacle handling. New diagnosis plan: `reports/route-iteration3r-repair2-20260805T2310/next-diagnosis-plan.md`.
- Review/status: focused/static/smoke/regression logs are preserved, `git diff --check` passed at checkpoint, and Iteration 3R is **BLOCKED after two bounded repairs**. Do not start Iteration 4.


### NEXT Iteration 3 bounded repair audit — blocked 2026-08-05T22:31:09Z

- Objective/scope remained the single verified Harvester-to-Core route. Two bounded repairs were applied only in the allowed route/economy/test surface: fresh project heartbeats keep an active claim alive, and occupied Builder-bot tiles are route obstacles. No Core spawning, combat, second Harvester, advanced spending, or Iteration 4 work was added.
- Tests/results: focused 43/43; `make static` 112/112 plus compileall; `make smoke` 4/4; selected regression 36/36 command-clean with zero stderr. Logs and return codes are under `reports/route-iteration3-repair2-20260805T2230/`.
- Reports/replays: smoke `reports/local-20260805T223109Z`; regression `reports/local-20260805T223130Z`; summary `reports/route-iteration3-repair2-20260805T2230/summary.md`.
- Metrics: first-delivery/collection proxy remained 12/36 (33.3%); candidate wins 0/36; mean collected titanium 824.2 versus 4,778.1 for the current-best Iteration 2 snapshot; no row-level improvement. All five isolation flags remain false; full 21-map matrix was not run.
- Review/status: `git diff --check` passed and the complete diff was self-reviewed. Both resumed-audit repair attempts passed their focused tests but failed to improve the promotion metric. Iteration 3 remains **BLOCKED**; do not start Iteration 4 without a newly scoped diagnosis/plan.


### NEXT Iteration 3 first-route checkpoint — blocked 2026-08-05T22:15:15Z

- Objective/scope: implement only the first Harvester-to-Core route FSM, route-local delivery acknowledgement, bounded repair, and explicit advanced-feature isolation. No second Harvester, combat targeting, defense, launchers, raids, or Iteration 4 work was started.
- Files changed: `bots/candidate/bot/builder.py`, `bots/candidate/bot/feature_flags.py`, `tests/test_candidate_route_fsm.py`, `tests/test_candidate_player.py`, baseline-policy configs, immutable comparator snapshot `bots/versions/v0005_store-iteration2_20260805-2140_2de8371f`, and durable state/report metadata.
- Tests/results: focused 41/41; `make static` 110/110 plus compileall; `make smoke` 4/4 against the current-best snapshot; selected regression 36/36 command-clean with zero stderr. Smoke report: `reports/local-20260805T221515Z`. Regression report: `reports/local-20260805T221103Z`.
- Metrics: first-delivery/collection proxy 12/36 (33.3%) versus the required 95%; candidate mean collected titanium 825.8 versus 4,778.1 for the previous-best snapshot, with no candidate win or row-level collection improvement. All five advanced flags remain false. Full 21-map matrix was not run.
- Review/blocker: `git diff --check` passed. A deterministic trace shows the builder releases its active route when assignment generation reaches age 32 even though the project heartbeat is current; this happens before final-link verification and Harvester construction. Two bounded repairs (scouting progression and verification fallback) did not clear the gate, so no further repair or next iteration was started.
- Baseline policy: regression/smoke/matrix configs now point to the latest passed Iteration 2 snapshot; a future passed iteration must replace that snapshot/config baseline before its successor is evaluated.
- Reports: `reports/route-iteration3-20260805T2200/summary.md`, `previous-best-regression.txt`, `current-best-smoke.txt`, focused/static/smoke/regression logs; comparator source manifest digest `c39eefc81e84539a44a929810dac8726f95863767f20d6ef5e9282fb58860ecc`.
- Iteration status: **BLOCKED**; resume Iteration 3 only with the bounded claim/project-heartbeat freshness repair, then re-run all gates before considering Iteration 4.


### NEXT Iteration 2 Store protocol checkpoint — 2026-08-05T21:40:28Z

- Files changed: bots/candidate/bot/types.py, comms.py, core.py, builder.py, tests/test_candidate_comms.py, tests/test_candidate_player.py, plus durable state/report metadata.
- Tests/results: focused Store/Core/player suite 41/41 passed; make static 98/98 plus compileall passed; make smoke 4/4; regression 24/24 command-clean with zero stderr.
- Reports: reports/store-iteration2-20260805T2140/summary.md, focused.log, static.log, static.rc, smoke-summary.txt, regression-summary.txt; regression metadata/replays at reports/local-20260805T213612Z.
- Metrics: schema version 3; all 30x30 coordinates round-tripped; delayed assignment/project writes covered; active project cap remained 3; no duplicate ownership observed; candidate stayed at 1,800 production lines.
- Remaining risks: full 21-map matrix deferred; first-delivery reliability and Iterations 3-5 remain unimplemented; no platform operation performed.
- Iteration status: PASSED; proceed to the separately scoped Iteration 3 checkpoint.


### NEXT Iterations Plan Iteration 1 validation — 2026-08-05T21:11:47Z

- Objective: validate adjacent legal stances, active per-unit path reuse, bounded deterministic replanning, navigation/layout epoch separation, and non-consuming destroy semantics. No source edits were made; the existing CURRENT_PLAN implementation remains a separate v0004 checkpoint.
- Allowed surface reviewed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, and focused navigation/action tests. Non-goals remained Store layout, economy thresholds, role assignment, combat priorities, and Core budget policy.
- Tests: focused Iteration 1 suite 34/34; make static 97/97 plus compileall; make smoke 4/4 command-clean; required regression subset 24/24 command-clean with no stderr.
- Reports: reports/iteration1-validation-20260805T2120/summary.md, focused.log, static.log, smoke.log, regression-summary.txt, complete v0003-to-candidate.diff, and v0004-to-candidate.diff; local regression report reports/local-20260805T210935Z and smoke report reports/local-20260805T210923Z.
- Metrics: active-path tests cover one BFS/replan followed by cache hits, epoch/goal invalidation, blocked-step retry, adjacent-target exclusion, CPU cutoff, and oscillation fallback; no exception, TLE, or command-failure indicators.
- Self-review: source comparison against v0004 is identical apart from generated __pycache__ bytecode; no defects were found and no repair was needed. Full 21-map matrix remains deferred to the release gate.
- Iteration status: PASSED; Iteration 2 is now the next implementation checkpoint.


### NEXT Iterations Plan Iteration 0 reconciliation — 2026-08-05T21:08:46Z

- Files changed: .codex/config.toml; .codex/agents/sol-planner.toml; .codex/agents/luna-implementer.toml; .codex/agents/sol-reviewer.toml; AGENTS.md; scripts/codex_task.py; Makefile; generated artifacts/chatgpt planning packets; report/state metadata. No candidate behavior changes were made in this iteration.
- Source/archive evidence: v0003 archive SHA-256 fd757d1c6ff72c8e5e45bad37b6201700c599f9aa83caeeadf7d22b21adb6608; immutable v0003 snapshot retained; intentional current-plan delta is separately packaged as v0004_navigation-iteration1 SHA-256 59e579333548bd8e41dfe1f13f78900138a09192476ca20cc67d057e85051c56.
- Tests: harness/startup focused tests 16/16; make static 97/97 plus compileall; make smoke 4/4; Iteration 0 regression 20/20 command-clean; make handoff passed.
- Reports and packets: reports/reconcile-iteration0-20260805T/summary.md, source-hashes.txt, static.log, smoke.log, regression artifacts under reports/local-20260805T210359Z, and artifacts/chatgpt/PLANNING_PACKET.md plus RELEASE_REVIEW_PACKET.md.
- Metrics: zero command failures, exceptions, or TLE indicators in smoke/regression; packet source matches the candidate; v0003 remains recoverable; no additional strategy/economy/navigation changes mixed into this checkpoint.
- Remaining risks: Iteration 1 in the external plan duplicates the already-completed current-plan navigation checkpoint, so it must be validated as a separate no-op checkpoint before Iteration 2; no full 21-map matrix was run.
- Iteration status: PASSED; proceed only to the separate Iteration 1 validation checkpoint.


### Current-plan navigation checkpoint — 2026-08-05T21:00:41Z

- Status: behavior checkpoint passed; next-plan iterations are paused because make static exits 2 on pre-existing harness/startup failures outside the approved scope.
- Files changed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, tests/test_candidate_navigation.py, tests/test_candidate_actions.py, tests/test_candidate_builder_navigation.py.
- Focused tests: 34/34 passed; compileall passed. Full logs: reports/navigation-20260805T2110/focused.log and compileall.log.
- make static: exit 2; candidate/static-contract checks passed, with 4 harness failures and 3 missing-agent errors. Full log: reports/navigation-20260805T2110/make-static.log.
- make smoke: 4/4 games, zero command failures; report: reports/local-20260805T205901Z.
- Regression subset: 24/24 games, zero command failures/stderr; report: reports/local-20260805T205908Z.
- Metrics: active path one BFS and two cache hits over a three-step route; goal/epoch/blocked-step invalidations replan once; candidate production count is 1,800 lines.
- Behavior unchanged deliberately: Store/economy/budget/roles/defense/offense/opening policy. Remaining risk: static harness state must be repaired before NEXT_ITERATIONS_PLAN Iteration 0 can start.
- Report: reports/navigation-20260805T2110/summary.md


### Live battle observation — 2026-08-05T19:31:39Z

- Platform reports submission `v0003-entrypoint-class-2de8371f` as numeric version `1`, `ready`, and active for Kleos.
- Eight rated ladder series are complete: one win and seven losses. The newest series beat Git Glam 3–2 (+4.041 Elo), raising the rating to `1402.3331784619274` and placing Kleos at rank `39/102`.
- The newest series reached the 1000-turn titanium-collection limit on all five maps: wins on `crossfire`, `sweden`, and `skerry`; losses on `twins` and `runestone`. No match error or resignation was reported.
- Previous Powerpuff Girls 0–5 ended by `core_destroyed` on all five maps after 266–317 turns; no platform/runtime error was reported.
- Replay-level comparison: the Git Glam series first produced HP events at turns 325–766 and no core destruction; the Powerpuff series first produced HP events at turns 12–87 and destroyed the Kleos core in every game. The current weakness is collection/economy on `twins` and `runestone`, not a submission/runtime failure.
- Battle descriptions from the decoded replay streams:
  - Git Glam `crossfire`: Kleos stayed at 4 builders, 2 harvesters, and 4 conveyors while Git Glam expanded to 13 builders, 4 harvesters, 13 conveyors, and a full turret mix; no core damage, Kleos won the 1000-turn collection finish.
  - Git Glam `sweden`: first HP event at turn 458; Kleos reached 5 builders, 2 harvesters, and 13 conveyors, with sustained turret/resource activity and no core damage; Kleos won by collection.
  - Git Glam `twins`: first HP event at turn 454; Kleos stayed at 4 builders, 1 harvester, and 4 conveyors while Git Glam grew to 27 builders, 5 harvesters, 20 conveyors, and heavy defense; Git Glam won collection without destroying the core.
  - Git Glam `runestone`: first HP event at turn 622; Kleos recorded 85 conveyor placements and 70 later removals, indicating route churn or repair activity; Git Glam’s larger 28-builder/42-conveyor footprint won collection.
  - Git Glam `skerry`: first HP event at turn 766; Kleos finished with 4 builders, 3 harvesters, and 6 conveyors, survived without core damage, and won collection.
  - Powerpuff `duel`, `sweden`, `longship`, `hive`, and `quarry`: first HP events came at turns 12, 87, 29, 37, and 48 respectively; Powerpuff scaled substantial gunner/harvester/conveyor forces and destroyed the Kleos core at turns 273, 285, 271, 266, and 317.
- Full notes and per-map descriptions: `reports/live-battles-20260805T193139Z.md`; raw capture: `reports/live-latest-battles-20260805T193139Z/`; newest replays: `replays/live-c17b2501-20260805/`.

### Codex cap-replan fix — 2026-08-05T17:37:04Z

- Fixed blocked-route replanning for a Builder that already owns one of the three shared project reservations: admission now counts only other projects while preserving the owner's reservation, so it cannot deadlock at the cap or create a fourth project.
- Added Player.run coverage for reserved replanning at the shared cap and strengthened the unreserved fourth-project rejection test.
- Validation: independent Sol review `APPROVED`; focused unit suite 33/33; smoke 4/4; regression 54/54; full matrix 210/210 command-clean, 205/210 wins versus 165/210 prior, with bridge and string 10/10 and no non-target map regression; benchmark p99 6.246564 ms, max 6.830654 ms.
- Remote gate was attempted but DNS was unavailable; no platform upload or activation was performed. Luna harness compatibility remains unavailable (`native_luna_compatible: False`).
- Submission archive: `artifacts/submissions/v0002_cap-replan_20260805-1736_2de8371f.zip` (SHA-256 `5f3118ba1d25c98fc890f76b895ab6c68adc5a51b4a4feeffa9ea52c81edd9c2`).

### Codex implementation task — 2026-08-05T11:23:01Z

- Task: Implement only the final Sol review blocker in reports/codex-20260805T084146Z/review-2.md: derive a team-wide active-project count from authoritative live shared state using a delayed-Store-safe Core/Builder protocol; apply that count before route admission and every new_project discretionary spend; add a real Player.run test with three independently owned active projects, without directly assigning BuilderStateData.active_projects, proving a fourth route and Splitter/Barrier/Launcher/turret projects are rejected. Preserve baseline, configs, maps, README, unrelated files, and the existing successful remediation. Use the required Sol planner -> Luna implementer -> Sol reviewer workflow, run the exact focused retest plus make static, make smoke, make eval-regression, make eval-local, and the benchmark. Do not perform platform operations. Produce truthful process-fallback evidence with exact agent IDs/models/exit codes.
- Backend: process-fallback
- Luna evidence recorded: False
- Outcome: planner failed
- Report: reports/codex-20260805T112300Z


### Codex implementation task — 2026-08-05T11:22:46Z

- Task: Implement only the final Sol review blocker in reports/codex-20260805T084146Z/review-2.md: derive a team-wide active-project count from authoritative live shared state using a delayed-Store-safe Core/Builder protocol; apply that count before route admission and every new_project discretionary spend; add a real Player.run test with three independently owned active projects, without directly assigning BuilderStateData.active_projects, proving a fourth route and Splitter/Barrier/Launcher/turret projects are rejected. Preserve baseline, configs, maps, README, unrelated files, and the existing successful remediation. Use the required Sol planner -> Luna implementer -> Sol reviewer workflow, run the exact focused retest plus make static, make smoke, make eval-regression, make eval-local, and the benchmark. Do not perform platform operations. Produce truthful native-v1 evidence with exact agent IDs/models/exit codes and stop after the allowed review limit.
- Backend: native-v1
- Luna evidence recorded: False
- Outcome: native V1 did not provide complete Luna/approval evidence
- Report: reports/codex-20260805T112246Z


### Codex implementation task — 2026-08-05T11:13:58Z

- Task: Resume the existing integrated candidate remediation. Read reports/codex-20260805T010045Z/review-1.md and implement only its four concrete findings: (1) verify the single-map bounded route planner and blocked-step CPU path, (2) make delivery/repair/claim-heartbeat/reassignment transitions executable through real Builder/Core handlers, (3) wire payback/reserve, Splitter/Barrier/Launcher, threat/opening, and late-game policies into live handlers with legality and fresh-target guards, and (4) produce truthful native Sol-Luna-Sol evidence. The current tree already contains a Luna remediation attempt; do not broaden scope or revert it. Preserve baseline, versions, README, state/UPDATES/startup, configs, maps, and unrelated files. Run the exact reviewer retests, make static, make smoke, make eval-regression, make eval-local, and the expanded benchmark; use existing full-matrix reports only if hashes match, otherwise rerun. No platform operations. The final report must use backend native-v1, name exact agent IDs/models/exit codes, and have an independent sol_reviewer verdict.
- Backend: native-v1
- Luna evidence recorded: False
- Outcome: APPROVED
- Report: reports/codex-20260805T084146Z


### Verification-only Sol-Luna-Sol harness probe approved — 2026-08-05T00:54:23Z

- sol_planner produced a bounded read-only packet; luna_implementer reported `# Florent Code League bot workspace`; sol_reviewer returned `APPROVED`.
- Native multi-agent evidence records `gpt-5.6-sol` for planning/review and `gpt-5.6-luna` for implementation inspection.
- Before/after status, diff, protected hashes, and full repository fingerprints matched; no source, configuration, live-state, or platform changes occurred.
- Evidence: `reports/codex-20260805T004253Z`.


### Session startup and scoped document routing added — 2026-08-05T00:25:00Z

- Added generated `docs/START_HERE.md` plus machine-readable `state/project_state.json` for cross-session development focus.
- Root `AGENTS.md` now requires a startup bootstrap but routes agents to detailed documents conditionally instead of loading everything every time.
- Added nested instructions for `bots/candidate/`, `scripts/`, and `tests/`.
- Updated Sol planner, Luna implementer, and Sol reviewer instructions to read startup state and nearest nested guidance.
- Added project-state/update scripts, automatic startup-summary refresh, Make targets, and regression tests.
- Resolved the orchestration-skill conflict: Luna implementation tasks cannot deploy, while the approved primary Sol/operator live workflow remains authorized by policy.


### Codex harness and live operator audited — 2026-08-05

- Found that the original custom-agent TOML did not prove Luna execution under the current Sol/Terra V2 versus Luna V1 mismatch.
- Added a reversible native-V1 route and an explicit process-isolated Sol → Luna Max → Sol fallback with exact command evidence.
- Added autonomous resumable upload, activation, live scoring, promotion, and rollback using `state/live_state.json`.
- Separated V1 and V2 configuration modes to avoid a boolean/table key conflict.
- Kept Sol as the only live reviewer/operator; Luna implements code but cannot modify live state or perform platform writes.


### Repository initialized — 2026-08-05

- Created the rules reference, Codex harness, starter bot, local/remote evaluation scripts, and submission workflow.
- Initial live state is unknown because no authenticated `fcode` session was available when the repository was generated.
