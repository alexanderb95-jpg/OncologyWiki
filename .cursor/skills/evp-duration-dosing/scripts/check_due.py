#!/usr/bin/env python3
"""sessionStart helper: remind the agent if the EV+P evidence snapshot is due."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

LEDGER = Path.home() / ".cursor/skills/evp-duration-dosing/ledger.json"


def main() -> int:
    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        due = date.fromisoformat(str(data["next_due"]))
    except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError):
        sys.stdout.write("{}\n")
        return 0

    if date.today() < due:
        sys.stdout.write("{}\n")
        return 0

    last = data.get("last_refresh", "unknown")
    msg = (
        f"EV+P mUC duration/dosing snapshot is due (last_refresh {last}, "
        f"next_due {due.isoformat()}). Run the evp-duration-dosing skill with "
        "`.evpdose refresh`: re-query PubMed/congress, rewrite CURRENT-NOTE.txt "
        "and canvases/evp-muc-duration-dosing.canvas.tsx, then update ledger.json."
    )
    sys.stdout.write(json.dumps({"additional_context": msg}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
