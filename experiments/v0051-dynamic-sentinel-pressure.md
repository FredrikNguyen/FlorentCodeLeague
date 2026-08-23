# v0051 dynamic sentinel-pressure claim

## Objective

After five completed routes, give only the nearest dynamic builder a concrete
sentinel/advance task when the forward pool is below target, so the scalable
workforce converts surplus income into pressure instead of harvesting forever.

## Evidence

The six-map screen (Strait, Sweden, Twins, String, Vault, and Fjord; seeds
1/19/101 with side swaps) scored 17/36 (47.2%) against immutable v0030. It
was command-clean with no TLE or suspicious-output markers. Report:
`reports/local-20260814T150313Z`; replay analysis:
`reports/iter-sentinel-pressure-v0051-screen-analysis.json`.

## Decision

Rejected at the screen gate. The temporary dynamic task branch was removed,
focused tests/compileall/smoke passed after revert, and the candidate Python
tree remains byte-identical to v0030. No full matrix, package, upload,
activation, or baseline transition was performed.
