#!/usr/bin/env python3
"""High-yield PubMed delta → inbox/ only (never auto-promotes into evidence.md).

Usage:
  python3 scripts/inbox_refresh.py
  python3 scripts/inbox_refresh.py --json
  python3 scripts/inbox_refresh.py --no-build

Optional: set NCBI_EMAIL in the environment (or ~/.cursor/med-onc.env).
"""

from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
SCRIPTS = Path(__file__).resolve().parent

TOPICS: dict[str, str] = {
    "prostate-mhspc": (
        "(metastatic hormone sensitive prostate cancer[Title/Abstract] OR mHSPC[Title/Abstract]) "
        'AND (NEJM[Journal] OR Lancet[Journal] OR "Lancet Oncol"[Journal] OR '
        '"J Clin Oncol"[Journal] OR "Eur Urol"[Journal] OR JAMA[Journal])'
    ),
    "prostate-mcrpc": (
        "(metastatic castration resistant prostate cancer[Title/Abstract] OR mCRPC[Title/Abstract]) "
        'AND (NEJM[Journal] OR Lancet[Journal] OR "Lancet Oncol"[Journal] OR '
        '"J Clin Oncol"[Journal] OR "Eur Urol"[Journal] OR JAMA[Journal])'
    ),
    "bladder-muc": (
        '(metastatic urothelial[Title/Abstract] OR "advanced urothelial"[Title/Abstract]) '
        'AND (NEJM[Journal] OR Lancet[Journal] OR "Lancet Oncol"[Journal] OR '
        '"J Clin Oncol"[Journal] OR "Eur Urol"[Journal] OR JAMA[Journal])'
    ),
    "bladder-adjuvant": (
        "(adjuvant[Title/Abstract] AND (urothelial[Title/Abstract] OR bladder cancer[Title/Abstract])) "
        'AND (NEJM[Journal] OR Lancet[Journal] OR "Lancet Oncol"[Journal] OR '
        '"J Clin Oncol"[Journal] OR "Eur Urol"[Journal])'
    ),
    "kidney-mrcc": (
        "(metastatic renal cell[Title/Abstract] OR mRCC[Title/Abstract]) "
        'AND (NEJM[Journal] OR Lancet[Journal] OR "Lancet Oncol"[Journal] OR '
        '"J Clin Oncol"[Journal] OR "Eur Urol"[Journal] OR JAMA[Journal])'
    ),
}


def load_email() -> str:
    if os.environ.get("NCBI_EMAIL"):
        return os.environ["NCBI_EMAIL"].strip()
    env_path = Path.home() / ".cursor" / "med-onc.env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("NCBI_EMAIL="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def pubmed_search(query: str, days: int, email: str) -> list[dict[str, str]]:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    params = {
        "db": "pubmed",
        "term": f"{query} AND ({days}days[PDat])",
        "retmax": "10",
        "retmode": "json",
        "sort": "pub_date",
    }
    if email:
        params["email"] = email
    url = f"{base}/esearch.fcgi?{urlencode(params)}"
    try:
        with urlopen(Request(url, headers={"User-Agent": "gu-clinic-wiki/1.0"}), timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError):
        return []

    ids = payload.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    summary_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
    if email:
        summary_params["email"] = email
    url2 = f"{base}/esummary.fcgi?{urlencode(summary_params)}"
    try:
        with urlopen(Request(url2, headers={"User-Agent": "gu-clinic-wiki/1.0"}), timeout=30) as resp:
            summary = json.loads(resp.read().decode())
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError):
        return [{"pmid": i, "title": "", "pubdate": "", "source": ""} for i in ids]

    result = []
    docs = summary.get("result", {})
    for pmid in ids:
        doc = docs.get(pmid, {})
        result.append(
            {
                "pmid": pmid,
                "title": doc.get("title", ""),
                "pubdate": doc.get("pubdate", ""),
                "source": doc.get("source", ""),
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="GU clinic wiki — inbox PubMed refresh")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-build", action="store_true", help="Skip regenerating site/")
    args = parser.parse_args()

    email = load_email()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report: dict = {"date": today, "topics": {}, "inbox_file": None}

    lines = [
        f"# Inbox delta {today}",
        "",
        "High-yield PubMed hits only (selected journals). **Do not** promote into evidence without review.",
        "",
    ]
    total = 0
    for slug, query in TOPICS.items():
        hits = pubmed_search(query, args.days, email)
        report["topics"][slug] = {"count": len(hits)}
        lines.append(f"## {slug}")
        lines.append("")
        if not hits:
            lines.append("- No hits in window (or NCBI unreachable).")
        else:
            for h in hits:
                title = (h.get("title") or "").replace("\n", " ").strip()
                src = h.get("source") or ""
                lines.append(
                    f"- PMID {h['pmid']} ({h.get('pubdate', '')}; {src}): {title}"
                )
                total += 1
        lines.append("")

    INBOX.mkdir(parents=True, exist_ok=True)
    out = INBOX / f"{today}.md"
    if out.exists():
        out.write_text(
            out.read_text(encoding="utf-8").rstrip()
            + "\n\n---\n\n"
            + "\n".join(lines)
            + "\n",
            encoding="utf-8",
        )
    else:
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report["inbox_file"] = str(out)
    report["total_hits"] = total

    if not args.no_build:
        sys.argv = [str(SCRIPTS / "build_wiki.py")]
        runpy.run_path(str(SCRIPTS / "build_wiki.py"), run_name="__main__")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Wrote {out} ({total} hits). Promote into pathways/ after review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
