#!/usr/bin/env bash
# Validate that all problem files have required header fields
set -euo pipefail
cd "$(dirname "$0")/.."
REQUIRED="MISSION TITLE DESC ALGO MODULE TIME_COMPLEXITY SPACE_COMPLEXITY DIFFICULTY"
ERRORS=0
for f in problems/*.py; do
    [ -f "$f" ] || continue
    for field in $REQUIRED; do
        if ! grep -q "^# $field:" "$f"; then
            echo "MISSING $field in $f"
            ERRORS=$((ERRORS+1))
        fi
    done
done
if [ $ERRORS -eq 0 ]; then
    echo "All problem headers valid!"
else
    echo "$ERRORS missing fields found"
    exit 1
fi
