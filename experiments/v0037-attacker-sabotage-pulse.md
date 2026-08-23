# v0037 fixed-attacker sabotage pulse

Date: 2026-08-17

## Hypothesis

After three completed routes, a confirmed enemy Core, one live forward
Sentinel, and the fixed reserve, a fixed attacker can spend its otherwise idle
siege-shell turns destroying one visible enemy Harvester or logistics tile,
then return to the direct siege lane. The nearest designated attacker owns the
pulse so two attackers do not queue on one target.

## Evidence

- Focused: 23/23; compile passed; smoke 4/4.
- 24 games: 13-11, 73,670-64,560 collected titanium, zero versus one
  no-delivery rows.
- 54 games: 30-24, 237,770-173,000 collected titanium, zero versus two
  no-delivery rows.
- 210 games: 116-94, 1,105,440-968,650 collected titanium (1.1412x), five
  versus eight no-delivery rows.
- Reliability: zero command failures, TLEs, or suspicious output; matrix max
  p99 1.536 ms and peak 4.944 ms.

Reports: `reports/iter-attacker-sabotage-pulse-v126/`,
`reports/local-20260817T082021Z`, `reports/local-20260817T082245Z`, and
`reports/local-20260817T082829Z`.

## Decision

Promote locally as v0037 and use it as the next immutable comparator. Do not
upload or activate until the next experiment addresses the slower first
delivery and weak Auroraveil/Royale/Yulerune floors.
