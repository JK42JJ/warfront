#!/usr/bin/env bash
# Migrate .warfront_progress.json to SQLite
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -c "
from warfront.data.progress import migrate_from_json, init_db
init_db()
n = migrate_from_json()
print(f'Migrated {n} records to SQLite')
"
