# Source index and authority notes

**Last checked:** 2026-08-05

## Official Florent sources

- Documentation index: https://game.code.florent.vc/docs/florent-code-league
- CLI reference: https://game.code.florent.vc/docs/cli-reference
- Controller API: https://game.code.florent.vc/docs/robot-api
- Types/enums: https://game.code.florent.vc/docs/api-types
- Global Store: https://game.code.florent.vc/docs/global-comms
- Builder rules: https://game.code.florent.vc/docs/game-rules-builder-bot
- Turrets: https://game.code.florent.vc/docs/game-rules-turrets
- Conveyors/Splitters: https://game.code.florent.vc/docs/game-rules-conveyors
- Harvester: https://game.code.florent.vc/docs/game-rules-harvester
- Official AI context / AGENTS reference: https://game.code.florent.vc/docs/agents-md
- Tutorials index: https://game.code.florent.vc/tutorials/movement-sensing/01-welcome
- Combined strategy tutorial: https://game.code.florent.vc/tutorials/comms-strategy/03-putting-it-together
- Changelog: https://game.code.florent.vc/changelog
- Current map pool: https://game.code.florent.vc/maps
- Terms/fair play: https://game.code.florent.vc/terms

The docs index links all current reference pages. The tutorial sidebar links 24 steps across movement/sensing, harvesting, logistics, combat, and coordination.

## Official OpenAI/Codex sources

- Subagents/custom agents: https://developers.openai.com/codex/agent-configuration/subagents
- AGENTS.md behavior: https://developers.openai.com/codex/agent-configuration/agents-md
- Configuration reference: https://developers.openai.com/codex/config-reference
- Sample config: https://developers.openai.com/codex/config-file/config-sample
- Models: https://developers.openai.com/codex/models
- Non-interactive mode: https://developers.openai.com/codex/non-interactive-mode
- Security/approval modes: https://developers.openai.com/codex/agent-approvals-security

## Community workflow evidence

These are anecdotal, not authoritative product documentation:

- Sol for design/bug finding; Luna for coding:
  https://www.reddit.com/r/codex/comments/1v9yscf/anyone_actually_benefiting_using_terra_or_luna_if/
- Planner → Sol plan review → Luna implementation → Sol code review loop:
  https://www.reddit.com/r/ClaudeCode/comments/1uvjlmr/fable_56_is_absolute_peak/
- Bounded orchestration, sequential workers, parallel read-only review:
  https://www.reddit.com/r/codex/comments/1vcxuic/i_built_a_subagent_orchestration_setup_for_codex/
- Warning about Luna output/context growth:
  https://www.reddit.com/r/codex/comments/1uzrmai/important_detail_to_consider_when_talking_about/

## Precedence

For game mechanics:

```text
observed current engine > latest official changelog > current reference > tutorial prose > sample code
```

For Codex configuration:

```text
installed `codex --help`/validation > current official Codex docs > Reddit workflow reports
```

When a discrepancy appears, create a minimal test, record the result, and update this repository.

## Codex V1/V2 harness audit sources

- Official custom-agent configuration: https://developers.openai.com/codex/agent-configuration/subagents
- Official non-interactive mode: https://developers.openai.com/codex/non-interactive-mode
- Sol V2 hidden spawn metadata issue: https://github.com/openai/codex/issues/
- Sol/Terra V2 versus Luna V1 community reports and reversible catalog workaround: see the dated citations in the accompanying ChatGPT delivery and repository update record.

The workaround is treated as experimental and verified locally by `codex_luna_doctor.py`; process-isolated explicit-model workers remain the fallback.
