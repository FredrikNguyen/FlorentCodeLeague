PYTHON ?= python

refresh-start:
	$(PYTHON) scripts/refresh_start_here.py

project-state:
	$(PYTHON) scripts/set_project_state.py --show

handoff:
	$(PYTHON) scripts/build_chatgpt_bundle.py

.PHONY: refresh-start project-state handoff doctor sync-maps lint static smoke eval-regression eval-local remote-gate live-snapshot package codex codex-doctor setup-codex-v1 verify-luna live-bootstrap live-baseline live-status live-autopilot release-live

doctor:
	$(PYTHON) scripts/doctor.py

sync-maps:
	FCODE_NO_UPDATE_CHECK=1 fcode maps sync

lint:
	uv run ruff check .

static:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) -m compileall -q bots/candidate bots/baseline

smoke:
	$(PYTHON) scripts/run_local_matrix.py --config configs/eval_smoke.toml --limit 4

eval-regression:
	$(PYTHON) scripts/run_local_matrix.py --config configs/eval_regression.toml

eval-local:
	$(PYTHON) scripts/run_local_matrix.py --config configs/eval_matrix.toml

remote-gate:
	$(PYTHON) scripts/remote_gate.py

live-snapshot:
	$(PYTHON) scripts/capture_live.py --label manual

package:
	@test -n "$(SLUG)" || (echo "Usage: make package SLUG=short-name" && exit 2)
	$(PYTHON) scripts/package_candidate.py --slug "$(SLUG)"

codex:
	@test -n "$(TASK)" || (echo 'Usage: make codex TASK="..."' && exit 2)
	./scripts/codex_task.sh "$(TASK)"


codex-doctor:
	$(PYTHON) scripts/codex_luna_doctor.py

setup-codex-v1:
	$(PYTHON) scripts/setup_codex_v1_catalog.py

verify-luna:
	@test -n "$(TASK)" || (echo 'Usage: make verify-luna TASK="..."' && exit 2)
	$(PYTHON) scripts/codex_task.py "$(TASK)"

live-bootstrap:
	$(PYTHON) scripts/live_operator.py bootstrap

live-baseline:
	$(PYTHON) scripts/live_autopilot.py --force-observe

live-status:
	$(PYTHON) scripts/live_operator.py status

live-autopilot:
	$(PYTHON) scripts/live_autopilot.py

release-live:
	@test -n "$(SLUG)" || (echo 'Usage: make release-live SLUG="..."' && exit 2)
	$(PYTHON) scripts/release_candidate.py --slug "$(SLUG)"
