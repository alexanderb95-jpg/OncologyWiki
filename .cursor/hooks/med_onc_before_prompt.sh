#!/usr/bin/env bash
# beforeSubmitPrompt: detect med-onc mode (fail-open). Cloud-safe: repo-relative.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

input="$(cat)"
prompt="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("prompt",""))' <<<"$input" 2>/dev/null || true)"

lower="$(printf '%s' "$prompt" | tr '[:upper:]' '[:lower:]')"

if [[ "$lower" != *"med-onc"* && "$lower" != *"clinical reference"* && "$lower" != *"research synthesis"* \
   && "$lower" != *"evidence council"* && "$lower" != *"onc visit"* && "$lower" != *"board study"* \
   && "$lower" != *"patient counseling"* && "$lower" != *"knowledge base"* \
   && "$lower" != *".evpdose"* && "$lower" != *"evpdose"* && "$lower" != *"evp duration"* \
   && "$lower" != *"evp dosing"* && "$lower" != *"ev+p duration"* \
   && "$lower" != *"oncologywiki"* && "$lower" != *"gu clinic"* ]]; then
  echo '{}'
  exit 0
fi

python3 .cursor/scripts/med_onc_session.py --write-session --prompt "$prompt" --json >/dev/null 2>&1 || true

echo '{}'
exit 0
