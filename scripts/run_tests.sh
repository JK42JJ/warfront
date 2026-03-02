#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pytest warfront/tests/ -v --tb=short ${1:-}
