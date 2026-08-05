# Test instructions

- Use the current Luna XHigh session directly.
- Do not spawn subagents.
- Add the smallest deterministic test that proves the requested behavior.
- Prefer unit tests and fixtures over full game runs.
- Do not access the network or authenticated Florent account.
- Do not upload, activate, or consume remote-test quota.
- Run focused tests first.
- Run `make static` after meaningful code changes.
- Run smoke matches only for behavioral bot changes.
- Run regression and release matrices only when explicitly required.
- Keep generated logs and replays out of model context; summarize results and
  reference their paths.