#!/usr/bin/env bash
# stop: remind / no-op when kb_opt_in (fail-open). Does not write PHI.
# Cloud Agents: sessionStart/sessionEnd are unsupported; stop is OK.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SESSION_FILE="$REPO_ROOT/.cursor/med_onc_session_context.md"

if [[ ! -f "$SESSION_FILE" ]]; then
  echo '{}'
  exit 0
fi

kb_opt_in="$(grep -E '^- kb_opt_in:' "$SESSION_FILE" 2>/dev/null | sed 's/.*: *//' || true)"

if [[ "$kb_opt_in" != "true" ]]; then
  echo '{}'
  exit 0
fi

# Intent only — agent should have written pathways/ when user said save to KB.
# Rebuild wiki if scripts exist (ignore failures).
if [[ -f "$REPO_ROOT/scripts/build_wiki.py" ]]; then
  python3 "$REPO_ROOT/scripts/build_wiki.py" >/dev/null 2>&1 || true
fi

echo '{}'
exit 0
