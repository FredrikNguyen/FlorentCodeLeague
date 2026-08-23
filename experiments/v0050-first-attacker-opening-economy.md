# v0050 first-attacker opening-economy handoff

## Objective

Test whether temporarily assigning the first fixed attacker to the defender
economy loop until one completed route improves the weak-map conversion losses,
then returning it to the direct sentinel/core lane.

## Evidence

The six-map screen (Sprint, String, Sweden, Twins, Vase, and Strait; seeds
1/19/101 with side swaps) scored 18/36 (50.0%) against immutable v0030. The
run was command-clean with no TLE or suspicious-output markers. Report:
`reports/local-20260814T145434Z`; replay analysis:
`reports/iter-first-attacker-economy-v0050-screen-analysis.json`.

## Decision

Rejected at the screen gate. The temporary `attacker.py` change was removed,
focused tests/compileall/smoke passed after revert, and the candidate Python
tree remains byte-identical to v0030. No full matrix, package, upload,
activation, or baseline transition was performed.
