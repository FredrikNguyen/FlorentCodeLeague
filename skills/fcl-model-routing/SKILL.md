---
name: fcl-model-routing
description: "Choose the lowest-cost reliable model route for Florent Code League work: use Luna Max for ordinary implementation, tests, and bounded diagnostics; use Sol Medium only for heavy review, cross-map regression fixes, release gates, or ambiguous strategy changes. Use this skill before delegating or selecting a model for FCL work."
---

# FCL model routing

Use this routing policy after reading the repository's `AGENTS.md` and the
current startup/state files. It changes model selection, not the required
Sol-review evidence or platform safety rules.

## Routing

- **Luna Max**: routine implementation packets, small focused fixes, tests,
  static checks, benchmark runs, and bounded read-only diagnosis.
- **Sol Medium**: independent review of a real diff, remediation of review
  findings, full-matrix or cross-map regression analysis, policy/mechanics
  disputes, packaging/release decisions, and any change that could trade one
  map's reliability for another's.

For a heavy task, keep Sol Medium as the reviewer/operator and use Luna Max
for the bounded implementation packet. For an ordinary task, Luna Max may do
the implementation directly, but still record the requested evidence and
never claim a Luna invocation unless the harness manifest proves it.

## Guardrails

1. Preserve the repository's required Sol → Luna → Sol workflow whenever the
   task is non-trivial; this skill only selects the preferred model tier.
2. Do not silently substitute a different model when the requested model is
   unavailable. Stop the delegation attempt, record the exact error, and
   report that evidence is missing.
3. Keep implementation scope bounded, run the relevant tests, and compare all
   maps against the last known-good result before accepting a fix.
4. Sol/Luna agents never upload, activate, promote, or roll back live
   versions; those actions remain with the primary operator under policy.
