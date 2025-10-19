.PHONY: setup sim_smoke test report pil lint

PY=python

setup:
\t$(PY) -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt || true
\t@echo ">> Done. Activate venv: source .venv/bin/activate"

sim_smoke:
\t@mkdir -p results
\t@echo '{"status":"placeholder","note":"fill sim later"}' > results/metrics.json
\t@echo ">> sim_smoke done. See results/metrics.json"

test:
\tpytest -q

report:
\t@echo ">> Placeholder: generate PDF/CSV later"

pil:
\t@echo ">> Placeholder: build/run controller C in PIL later"

lint:
\t@echo ">> Placeholder: add ruff/flake8 later"
