#!/usr/bin/env bash
# Local-only helper. Cloud Agents do not run sessionStart.
# Kept for desktop agents that may still use ~/.cursor/hooks.json.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$REPO_ROOT/.cursor/scripts/med_onc_session.py" --write-session --prompt "" --json >/dev/null 2>&1 || true
echo '{}'
exit 0
