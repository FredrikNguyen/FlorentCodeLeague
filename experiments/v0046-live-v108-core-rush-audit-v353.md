# v353 live-v108 inbound Sentinel preemption

Date: 2026-08-20

## Replay evidence

Fresh observation (`reports/live-observe-20260820T131722Z`) found v108 at
16-17 rated series / 81-84 games. The 1-4 Jacobs Code loss
`6b0d70d1-6542-4d09-97f6-080a9ac2f0ef` is a distinct early Core-rush failure,
not the previously reviewed source-Sentinel attrition:

| Map | Core-kill turn | hostile relay / first Sentinel |
|---|---:|---|
| Drumlin | 40 | Launcher 10, thrown Builder 11, Sentinel 12 |
| Valkyrie | 76 | Launcher 1, Sentinel 14 |
| Auroraveil | v108 win at 665 | Launcher 4, Sentinel 6 |
| Drakkarfjord | 53 | five Sentinels from 35 |
| Icefloe | 34 | Launcher 14, thrown Builder 15, Sentinel 16 |

On Drumlin the opponent had no titanium delivery, but converted 266 ammunition
after the first turret and kept four direct Core lines firing. v108 had five
Builders by round four, but the nearest workers continued the route agenda;
Core heals began only after damage and never formed a durable healer group.

## Causal mechanism

The Core has vision radius squared 36. A Builder in that vision is an imminent
Core threat only when at least one currently visible, empty, bot-passable
cardinal neighbour can host a Sentinel whose fixed facing can hit one tile of
the Core footprint. That is both narrower and earlier than the existing
post-damage siege beacon. It remains valid under direct targeting: it does not
assume a wall, a body block, or a hostile target choice.

Use the existing `SLOT_CORE_SIEGE` encoding without claiming a new slot:
`missing_hp == 0` plus a nonzero packed position means a one-round-delayed
preemptive rally. Existing ordinary beacon content remains `missing_hp > 0`.
Workers that are not fixed attackers temporarily override even CHAIN work,
move to an adjacent Core stance, and hold it until the threat clears; once
damage lands, their existing `_heal_core` action has priority.

## Local diagnostic fixture

`experiments/.tmp-v353-live-rush-proxy/` is a private pure-Python opponent.
It walks one Builder forward, builds a Launcher only when it can throw into a
deep Sentinel staging band, then reproduces the first-anchor ammunition
conversion from the live replay. It is deliberately excluded from packaging
and promotion: it cannot reproduce the unavailable Jacobs Code placement
policy exactly. It is used only to verify signal timing and replay geometry.

Initial proxy evidence is retained under
`reports/live-v108-rush-proxy-v353r3-n91SRz`,
`reports/live-v108-rush-proxy-v353r4-dvJKes`, and
`reports/live-v108-rush-proxy-v353r5-yrGnVi`. The r5 replay produces a
five-Sentinel attack and gives the unmodified v0045 source repeated direct
Core damage; it is not scored as an evaluation result.

## Non-goals

Do not reopen generic early Gunner, counter-Sentinel, home-barrier, source
admission, Launcher quota/ejection, or ordinary route/fixed-role experiments.
Do not package, submit, activate, or change live state from this audit.

## Result

The first implementation rallied every non-attacker. In the private Drumlin
proxy it extended Core survival but held the route workforce indefinitely, so
the bounded repair reused the existing nearest-home responder rule and a local
radius. Focused coverage was 30/30, compileall passed, the known `make static`
profile was unchanged, and smoke was 4/4 command-clean.

The repair won the private rush fixture after 400 rounds while restoring
titanium delivery; immutable v0046 won its control fixture in 134 rounds. That
is mechanism evidence only. The explicit-v0046 15-map seed-172 screen
(`reports/local-20260820T135304Z`) was 8-7 with 81,630 vs 86,660 titanium,
zero command/TLE/suspicious rows, and one candidate Auroraveil no-delivery
row. It missed the 9-6 and protected-delivery gates. The candidate was restored
to exact v0046 source parity; rollback focused coverage was 26/26, compileall
passed, and smoke was 4/4 at `reports/local-20260820T135719Z`. No release,
submission, activation, or live-state change occurred.
