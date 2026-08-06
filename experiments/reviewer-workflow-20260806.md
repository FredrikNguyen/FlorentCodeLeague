# Reviewer-only submission comparison — 2026-08-06

- Workflow directive: compare the current local bot first, then unseen ready platform submissions one at a time against the strongest retained baseline. Do not run unit/static/smoke tests on challengers. Run the full validation/review only for the final winner.
- Current first challenger: `bots/candidate` after the target-less delayed-claim repair.
- Initial comparator: `bots/versions/v0006_iter7-integrated-20260806_20260806-1018_3f2505d7`.
- Comparison matrix: selected 48 games (`bridge`, `showdown`, `twins`, `crossfire`, `hive`, `string`, `aurora`, `strait`; seeds `1`, `19`, `101`; both sides; `--tle 10`).
- First comparison report: `reports/local-20260806T120456Z`.
- Unseen ready platform submissions downloaded for sequential comparison: versions 4, 5, 6, and 7. Archives and hashes are recorded in `reports/reviewer-workflow-20260806T1202Z/`.
- Later-unseen ready submissions v8 and v9 were also downloaded there; v8 failed harness validation before games because of a disallowed `finally`, while v9 lost its direct comparison (report `reports/local-20260806T124555Z`). No challenger test suites were run.
- Retained winner: `bots/versions/v0008_reviewer-current-best_20260806-1209_3f2505d7`; winner-only release evidence is `reports/local-20260806T122741Z` (210/210 command-clean, 1.2747 collection ratio versus v0006).
- Authorized deployment: local v0008 archive activated as platform version 10 with platform version 8 as previous active and version 2 as rollback; deployment and first post-activation observation are `reports/live-deploy-20260806T125258Z` and `reports/live-observe-20260806T125327Z`. No v10-rated series existed at observation time.
