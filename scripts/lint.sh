#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== ruff ==="
ruff check warfront/ || true
echo "=== mypy ==="
mypy warfront/ --ignore-missing-imports || true
