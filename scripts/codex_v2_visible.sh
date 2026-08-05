#!/usr/bin/env bash
set -euo pipefail
exec codex \
  --config 'features.multi_agent_v2.hide_spawn_agent_metadata=false' \
  --config 'features.multi_agent_v2.tool_namespace="agents"' \
  "$@"
