# Tooling and deployment instructions

## Workflow

- Use the current Luna XHigh session directly.
- Do not spawn subagents.
- Prefer deterministic Python logic over model-based decisions.
- Do not ask a model to poll matches, calculate scores, or repeatedly inspect
  deployment state.
- Save full command output to `reports/` and summarize it concisely.

## Platform operations

- Treat `state/live_state.json` as the machine-readable deployment source of truth.
- Treat `UPDATES.md` as the human-readable history.
- Preserve the previous active and last known-good versions before activation.
- Upload, activation, observation, promotion, and rollback may be performed by
  the approved live-operator scripts.
- Never issue raw destructive platform commands when a guarded repository
  script already exists.
- Never print, commit, or copy authentication credentials.
- Ensure operations are resumable across sessions.
- Keep upload and activation as separate recorded transitions.
- Rollback must remain possible after every activation.

## Testing

- Unit-test JSON parsing and state transitions with fixtures.
- Mock external commands in tests.
- Do not consume remote-test quota or alter the live platform during unit tests.