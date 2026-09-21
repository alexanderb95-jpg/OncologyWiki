#!/usr/bin/env python3
"""Lightweight med-onc session context for project hooks (cloud-safe)."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURSOR = Path(__file__).resolve().parents[1]
SESSION = CURSOR / "med_onc_session_context.md"

KB_OPT_IN = re.compile(
    r"save to knowledge base|append to master|\bKB yes\b", re.I
)

def infer_mode(prompt: str) -> str:
    p = prompt.lower()
    if any(x in p for x in (".evpdose", "evpdose", "evp duration", "evp dosing", "ev+p duration")):
        return "evp_duration_dosing"
    if any(x in p for x in ("research synthesis", "evidence council", "literature review", "systematic")):
        return "research_synthesis"
    if any(x in p for x in ("clinical reference", "onc visit", "patient counseling", "guideline", "soc", "board study", "visit-ready", "med-onc clinical")):
        return "clinical_reference"
    if "med-onc" in p:
        return "clinical_reference"
    return "single_shot"

def write_session(prompt: str) -> dict:
    mode = infer_mode(prompt)
    kb = bool(KB_OPT_IN.search(prompt or ""))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    excerpt = (prompt or "").replace("\n", " ")[:240]
    SESSION.write_text(
        f"# med-onc session\n\n"
        f"- updated: {stamp}\n"
        f"- mode: {mode}\n"
        f"- topic: gu\n"
        f"- kb_opt_in: {'true' if kb else 'false'}\n"
        f"- prompt_excerpt: {excerpt}\n"
        f"- wiki: {ROOT}\n",
        encoding="utf-8",
    )
    return {"mode": mode, "kb_opt_in": kb, "wiki": str(ROOT)}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-session", action="store_true")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.write_session:
        out = write_session(args.prompt)
        if args.json:
            print(json.dumps(out))
        return 0
    print("{}", end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
