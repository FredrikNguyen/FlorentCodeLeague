#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="$ROOT/state/codex_runtime.json"
if [[ ! -f "$STATE" ]]; then
  echo "Missing $STATE. Run: python scripts/setup_codex_v1_catalog.py" >&2
  exit 2
fi
CATALOG="$(python -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["catalog_path"])' "$STATE")"
if [[ ! -f "$CATALOG" ]]; then
  echo "Configured V1 catalog is missing: $CATALOG" >&2
  exit 2
fi
exec codex \
  --config "model_catalog_json=\"$CATALOG\"" \
  --config 'features.multi_agent=true' \
  --config 'features.multi_agent_v2=false' \
  "$@"
