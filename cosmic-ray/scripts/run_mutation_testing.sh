#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Ensuring clean source (reset any prior mutation artifacts)"
python scripts/restore_source.py

echo "==> Installing dependencies"
python -m pip install -e ".[dev]" -q

echo "==> Running pytest baseline"
python -m pytest tests -q

echo "==> Baseline (unmutated tests)"
cosmic-ray baseline cosmic-ray.toml

echo "==> Initializing mutation session"
rm -f session.sqlite
cosmic-ray init cosmic-ray.toml session.sqlite --force

echo "==> Executing mutations (this may take several minutes)"
cosmic-ray exec cosmic-ray.toml session.sqlite

echo "==> Restoring source (cosmic-ray may leave last mutant on disk)"
python scripts/restore_source.py
git diff --exit-code src/testable_demo/

echo "==> Exporting TESTABLE platform JSON and reports"
python scripts/export_testable_cosmic_ray.py --fail-on-gate

echo "==> Validating 100/100 mutation score gate"
python scripts/validate_metrics_gate.py --require-100

echo "==> Cosmic Ray summary"
cr-rate session.sqlite
cr-report session.sqlite --surviving-only || true
