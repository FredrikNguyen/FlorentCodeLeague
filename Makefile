PYTHON ?= uv run python

.PHONY: doctor sync-maps lint static check smoke eval-regression eval-local remote-gate live-snapshot package

doctor:
	$(PYTHON) scripts/doctor.py

sync-maps:
	FCODE_NO_UPDATE_CHECK=1 uv run fcode maps sync

lint:
	uv run ruff check .

static:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) -m compileall -q bots/candidate bots/baseline scripts tests

check: lint static

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
