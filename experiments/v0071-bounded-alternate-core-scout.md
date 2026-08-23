# v0071 — bounded alternate-Core scout

## Objective

Recover maps whose enemy Core is not at the 180-degree rotational mirror
without weakening the direct opening. The first fixed attacker remains on the
current direct symmetry lane. Only the designated second attacker may switch
to a bounded, deterministic horizontal/vertical counterpart search after a
no-sighting epoch; once either attacker sees the real Core, the existing store
intel immediately cancels the search for the whole team.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no guessed Sentinel placement, economy, route construction, workforce,
  ammo, turret, sabotage, hijack, or dynamic-task changes;
- no map-name catalog or fixed coordinates; counterparts derive only from the
  published Core position and map dimensions;
- the first attacker and all dynamic/defender workers retain their current
  target policy;
- no edits to `bots/baseline/` or immutable snapshots;
- no upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, `make smoke`, and `git diff
--check`, then the 54-game regression screen against immutable v0031. Run the
210-game matrix only for a strict, reliability-clean screen edge. Promote only
if paired win rate improves without delivery, collection, protected-map, or
reliability regressions; otherwise revert and retain v0031.

## Result

- Focused gate: 9/9 passed; compileall passed; smoke was 4/4
  command-clean; `git diff --check` passed; `make static` retained the
  inherited exit-2 obsolete-import result. Logs:
  `reports/iter-bounded-alternate-core-scout-v0071/`.
- The 54-game screen was **26/54 (48.1%)** candidate wins versus 28
  comparator wins, with collection **242,820 versus 246,690 (0.9843x)**.
  Both sides had zero no-delivery rows; command failures, TLEs, and
  suspicious output were zero. Max p99 was 1,330 us and peak callback 2,749
  us. Report `reports/local-20260814T233244Z`; analysis
  `reports/iter-bounded-alternate-core-scout-v0071/screen-analysis.json`.
- Status: **rejected at the screen gate**. The bounded counterpart search was
  cleaner than v0070 but did not improve paired wins or collection, so no full
  matrix was run. `main.py`, `attacker.py`, `constants.py`, and the focused
  tests were restored byte-identically to v0031; proof:
  `reports/iter-bounded-alternate-core-scout-v0071/revert-source-diff.txt`.
  No package, upload, activation, or baseline transition occurred.
