#!/usr/bin/env python3
"""Generate personal-wiki HTML under site/ from pathways/ + inbox/.

Layout: pathways/{domain}/{disease}/{setting}/evidence.md
Example: pathways/gu/prostate/mHSPC/

Source of truth is markdown. Do not hand-edit site/.
"""

from __future__ import annotations

import base64
import html
import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATHWAYS = ROOT / "pathways"
INBOX = ROOT / "inbox"
SITE = ROOT / "site"
ASSETS = SITE / "assets"

WIKI_NAME = "MedOnc wiki"

DOMAIN_LABEL = {
    "gu": "GU oncology",
    "lung": "Lung",
    "heme": "Hematologic",
    "melanoma": "Melanoma / skin",
    "breast": "Breast",
}

DOMAIN_ORDER = ["gu", "lung", "heme", "melanoma", "breast"]

# Planned settings keyed by (domain, disease)
PLANNED: dict[tuple[str, str], list[str]] = {
    ("gu", "prostate"): ["Localized / adjuvant / salvage", "nmCRPC"],
    ("gu", "bladder"): ["Neoadjuvant MIBC"],
    ("gu", "variant-bladder"): ["Not started — add setting pages as evidence matures"],
    ("gu", "utuc"): ["Not started — add setting pages as evidence matures"],
    ("gu", "kidney"): [],
    ("gu", "testis"): ["Stage I / adjuvant / metastatic GCT"],
    ("lung", "nsclc"): ["Not started — add first setting page when ready"],
    ("heme", "aml"): ["Not started — add first setting page when ready"],
}

DISEASE_LABEL = {
    "prostate": "Prostate",
    "bladder": "Bladder / urothelial",
    "variant-bladder": "Variant bladder",
    "utuc": "UTUC",
    "kidney": "RCC",
    "testis": "Testis",
    "nsclc": "NSCLC",
    "aml": "AML",
}

DISEASE_ORDER = {
    "gu": ["prostate", "bladder", "variant-bladder", "utuc", "kidney", "testis"],
    "lung": ["nsclc"],
    "heme": ["aml"],
}

SETTING_LABEL = {
    ("gu", "bladder", "adjuvant-urothelial"): "Adjuvant urothelial",
    ("gu", "bladder", "mUC"): "Metastatic urothelial carcinoma",
    ("gu", "kidney", "adjuvant-ccrcc"): "Adjuvant clear-cell RCC",
    ("gu", "kidney", "mRCC"): "Metastatic RCC",
}

# Related: (domain, disease, setting) → list of (domain, disease, setting, label)
RELATED = {
    ("gu", "prostate", "mHSPC"): [("gu", "prostate", "mCRPC", "mCRPC")],
    ("gu", "prostate", "mCRPC"): [("gu", "prostate", "mHSPC", "mHSPC")],
    ("gu", "bladder", "mUC"): [("gu", "bladder", "adjuvant-urothelial", "Adjuvant urothelial")],
    ("gu", "bladder", "adjuvant-urothelial"): [("gu", "bladder", "mUC", "mUC")],
    ("gu", "kidney", "adjuvant-ccrcc"): [("gu", "kidney", "mRCC", "Metastatic RCC")],
    ("gu", "kidney", "mRCC"): [("gu", "kidney", "adjuvant-ccrcc", "Adjuvant clear-cell RCC")],
}

PHRASE_CONTROL_TOKEN = re.compile(
    r"\{\{(?P<kind>select|calc):(?P<body>[^{}]+)\}\}"
)
PHRASE_CONTROL_ID = re.compile(r"^[a-z][a-z0-9-]*$")
SUPPORTED_CALCULATORS = {"keynote-564"}


@dataclass(frozen=True)
class PhraseControl:
    id: str
    kind: str
    label: str
    token: str
    options: tuple[str, ...] = ()


@dataclass
class Article:
    domain: str
    disease: str
    setting: str
    title: str
    last_reviewed: str = ""
    next_review: str = ""
    status: str = ""
    purpose: str = ""
    evidence_body: str = ""
    evidence_html: str = ""
    trigger: str = ""
    phrase_lines: list[str] = field(default_factory=list)
    phrase_text: str = ""
    phrase_controls: list[PhraseControl] = field(default_factory=list)
    search_blob: str = ""

    @property
    def slug_path(self) -> str:
        return f"{self.domain}/{self.disease}/{self.setting.lower()}.html"

    @property
    def href(self) -> str:
        return self.slug_path

    @property
    def depth(self) -> int:
        return 2

    @property
    def active_key(self) -> str:
        return f"{self.domain}/{self.disease}/{self.setting}"

    @property
    def md_rel(self) -> str:
        return f"pathways/{self.domain}/{self.disease}/{self.setting}"
    @property
    def is_stale(self) -> bool:
        if not self.next_review:
            return False
        try:
            return date.fromisoformat(self.next_review) < date.today()
        except ValueError:
            return False

    @property
    def is_stub(self) -> bool:
        return "stub" in self.status.lower()


def parse_header_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines()[:20]:
        if ":" not in line or line.startswith("#") or line.startswith("##"):
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        if key in {
            "last reviewed",
            "next review",
            "owner",
            "purpose",
            "status",
        }:
            fields[key] = val.strip()
    return fields


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" rel="noreferrer">\1</a>',
        text,
    )
    return text


def parse_phrase_controls(phrase_text: str) -> list[PhraseControl]:
    """Parse optional interactive control annotations in a dot phrase."""
    controls: dict[str, PhraseControl] = {}
    for match in PHRASE_CONTROL_TOKEN.finditer(phrase_text):
        kind = match.group("kind")
        token = match.group(0)
        parts = [part.strip() for part in match.group("body").split("|")]
        control_id = parts[0] if parts else ""
        if not PHRASE_CONTROL_ID.fullmatch(control_id):
            raise ValueError(f"Invalid phrase-control id: {control_id!r}")

        if kind == "select":
            if len(parts) < 3 or not all(parts[1:]):
                raise ValueError(
                    "A select phrase control needs an id, label, and at least one option"
                )
            control = PhraseControl(
                id=control_id,
                kind=kind,
                label=parts[1],
                token=token,
                options=tuple(parts[2:]),
            )
        else:
            if len(parts) != 2 or not parts[1]:
                raise ValueError(
                    "A calculator phrase control needs an id and a display label"
                )
            if control_id not in SUPPORTED_CALCULATORS:
                raise ValueError(f"Unsupported phrase calculator: {control_id}")
            control = PhraseControl(
                id=control_id,
                kind=kind,
                label=parts[1],
                token=token,
            )

        existing = controls.get(control.id)
        if existing and existing != control:
            raise ValueError(
                f"Phrase control {control.id!r} must use the same annotation each time"
            )
        controls[control.id] = control
    return list(controls.values())


def render_phrase_line(line: str, controls: list[PhraseControl]) -> str:
    """Render phrase Markdown while replacing annotations with live value slots."""
    controls_by_token = {control.token: control for control in controls}
    parts: list[str] = []
    cursor = 0
    for match in PHRASE_CONTROL_TOKEN.finditer(line):
        parts.append(md_inline(line[cursor : match.start()]))
        control = controls_by_token[match.group(0)]
        parts.append(
            '<span class="phrase-fill-in" '
            f'data-phrase-control="{html.escape(control.id, quote=True)}">'
            "Not selected</span>"
        )
        cursor = match.end()
    parts.append(md_inline(line[cursor:]))
    return "".join(parts)


def render_phrase_tools(art: Article) -> str:
    """Render author-declared selects and calculator mounts for a phrase."""
    if not art.phrase_controls:
        return ""

    metadata = [
        {
            "id": control.id,
            "kind": control.kind,
            "label": control.label,
            "token": control.token,
            "options": list(control.options),
        }
        for control in art.phrase_controls
    ]
    controls_b64 = base64.b64encode(
        json.dumps(metadata, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    template_b64 = base64.b64encode(art.phrase_text.encode("utf-8")).decode("ascii")
    controls_html: list[str] = []
    for control in art.phrase_controls:
        escaped_id = html.escape(control.id, quote=True)
        escaped_label = html.escape(control.label)
        if control.kind == "select":
            options = "".join(
                f'<option value="{html.escape(option, quote=True)}">'
                f"{html.escape(option)}</option>"
                for option in control.options
            )
            controls_html.append(
                f"""<div class="phrase-control">
  <label for="phrase-control-{escaped_id}">{escaped_label}</label>
  <select id="phrase-control-{escaped_id}" data-phrase-control-id="{escaped_id}">
    <option value="">Select…</option>{options}
  </select>
</div>"""
            )
        else:
            controls_html.append(
                f"""<section class="phrase-control phrase-calculator"
  data-calculator-id="{escaped_id}" data-phrase-control-id="{escaped_id}">
  <h4>{escaped_label}</h4>
  <p class="calculator-note">Uses the published trial definition; it does not determine treatment suitability or timing.</p>
  <div class="calculator-fields"></div>
  <p class="calculator-result" aria-live="polite">Complete calculator fields</p>
</section>"""
            )

    return f"""<section class="phrase-tools" aria-label="Epic phrase helpers"
  data-phrase-controls-b64="{controls_b64}"
  data-phrase-template-b64="{template_b64}">
  <h3>Phrase helpers</h3>
  <p class="phrase-tools-note">Choose the documented category before copying the phrase.</p>
  <div class="phrase-tools-grid">
    {"".join(controls_html)}
  </div>
</section>"""


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_divider(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def render_table(
    header: list[str], rows: list[list[str]], *, css_class: str = ""
) -> str:
    header_html = "".join(f"<th>{md_inline(cell)}</th>" for cell in header)
    rows_html = "\n".join(
        "<tr>" + "".join(f"<td>{md_inline(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    class_suffix = f" {css_class}" if css_class else ""
    return (
        f'<div class="table-wrap{class_suffix}"><table><thead><tr>'
        f"{header_html}</tr></thead><tbody>{rows_html}</tbody></table></div>"
    )


def render_bullet_list(items: list[tuple[int, str]]) -> str:
    """Render a contiguous Markdown bullet block, including nested bullets."""
    index = 0

    def render_level(indent: int) -> str:
        nonlocal index
        parts = ["<ul>"]
        while index < len(items):
            item_indent, text = items[index]
            if item_indent < indent:
                break
            if item_indent > indent:
                raise ValueError("Nested bullet does not have a parent")
            index += 1
            children = ""
            if index < len(items) and items[index][0] > item_indent:
                children = render_level(items[index][0])
            parts.append(f"<li>{md_inline(text)}{children}</li>")
        parts.append("</ul>")
        return "".join(parts)

    return render_level(items[0][0])


def md_block_to_html(block: str) -> str:
    """Minimal markdown → HTML for tables, figures, and concise evidence pages."""
    lines = block.splitlines()
    out: list[str] = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        if not line.strip():
            i += 1
            continue
        css_class = ""
        if line.strip() == "<!-- .cross_trial -->":
            css_class = "cross_trial"
            i += 1
            if i >= len(lines):
                continue
            raw = lines[i]
            line = raw.rstrip()
        if (
            i + 1 < len(lines)
            and "|" in line
            and is_table_divider(lines[i + 1].rstrip())
        ):
            header = table_cells(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(table_cells(lines[i]))
                i += 1
            out.append(render_table(header, rows, css_class=css_class))
            continue
        if line.startswith("### "):
            out.append(f"<h3>{md_inline(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("## "):
            out.append(f"<h2 id=\"{slugify(line[3:])}\">{md_inline(line[3:].strip())}</h2>")
            i += 1
            continue
        image = re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)\)", line)
        if image:
            alt, src = image.groups()
            if src.startswith("/") or ".." in Path(src).parts:
                raise ValueError(f"Figure source must be a relative path: {src}")
            out.append(
                '<figure class="evidence-figure">'
                f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}">'
                "</figure>"
            )
            i += 1
            continue
        bullet = re.match(r"^(\s*)[-*]\s+(.+)", line)
        if bullet:
            items: list[tuple[int, str]] = []
            while i < len(lines):
                nested = re.match(r"^(\s*)[-*]\s+(.+)", lines[i].rstrip())
                if not nested:
                    break
                indent = len(nested.group(1).replace("\t", "  "))
                items.append((indent, nested.group(2)))
                i += 1
            out.append(render_bullet_list(items))
            continue
        out.append(f"<p>{md_inline(line)}</p>")
        i += 1
    return "\n".join(out)


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def collect_section_headings(block: str) -> list[tuple[str, str]]:
    """Collect (id, title) for each Markdown ## heading in an evidence body."""
    headings: list[tuple[str, str]] = []
    for line in block.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            headings.append((slugify(title), title))
    return headings


def render_section_toc(
    headings: list[tuple[str, str]], *, has_phrase: bool
) -> str:
    """Compact sticky in-page TOC for handbook chapter navigation."""
    items = list(headings)
    if has_phrase:
        insert_at = len(items)
        for i, (hid, _) in enumerate(items):
            if hid in {"guideline-references", "sources", "changelog"}:
                insert_at = i
                break
        items.insert(insert_at, ("dotphrase", "Epic phrase"))
    if not items:
        return ""
    links = "".join(
        f'<a href="#{html.escape(hid, quote=True)}">{html.escape(title)}</a>'
        for hid, title in items
    )
    return (
        '<nav class="section-toc" aria-label="On this page">'
        '<span class="section-toc-label">On this page</span>'
        f'<div class="section-toc-links">{links}</div>'
        "</nav>"
    )


def load_articles() -> list[Article]:
    articles: list[Article] = []
    if not PATHWAYS.exists():
        return articles
    for domain_dir in sorted(PATHWAYS.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("."):
            continue
        domain = domain_dir.name
        for disease_dir in sorted(domain_dir.iterdir()):
            if not disease_dir.is_dir() or disease_dir.name.startswith("."):
                continue
            # Skip non-pathway files like PATHWAYS.md sitting in domain root
            disease = disease_dir.name
            for setting_dir in sorted(disease_dir.iterdir()):
                if not setting_dir.is_dir():
                    continue
                evid = setting_dir / "evidence.md"
                phrase = setting_dir / "dotphrase.md"
                if not evid.exists():
                    continue
                text = evid.read_text(encoding="utf-8")
                fields = parse_header_fields(text)
                title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
                title = title_m.group(1).strip() if title_m else setting_dir.name

                body_start = 0
                for line in text.splitlines():
                    if line.startswith("## "):
                        body_start = text.find(line)
                        break
                body = text[body_start:] if body_start else text

                trigger = ""
                phrase_lines: list[str] = []
                phrase_text = ""
                phrase_controls: list[PhraseControl] = []
                if phrase.exists():
                    ptext = phrase.read_text(encoding="utf-8").strip()
                    plines = ptext.splitlines()
                    if plines:
                        trigger = plines[0].strip()
                        phrase_lines = [ln for ln in plines[1:] if ln.strip()]
                        phrase_text = "\n".join(plines)
                        phrase_controls = parse_phrase_controls(phrase_text)

                art = Article(
                    domain=domain,
                    disease=disease,
                    setting=setting_dir.name,
                    title=title,
                    last_reviewed=fields.get("last reviewed", ""),
                    next_review=fields.get("next review", ""),
                    status=fields.get("status", ""),
                    purpose=fields.get("purpose", ""),
                    evidence_body=body,
                    evidence_html=md_block_to_html(body),
                    trigger=trigger,
                    phrase_lines=phrase_lines,
                    phrase_text=phrase_text,
                    phrase_controls=phrase_controls,
                )
                art.search_blob = " ".join(
                    [
                        art.title,
                        art.domain,
                        art.disease,
                        art.setting,
                        art.status,
                        art.evidence_body,
                        art.phrase_text,
                    ]
                ).lower()
                articles.append(art)
    return articles


def article_setting_label(article: Article) -> str:
    return SETTING_LABEL.get(
        (article.domain, article.disease, article.setting), article.setting
    )


def list_inbox() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    if not INBOX.exists():
        return items
    for path in sorted(INBOX.glob("*.md"), reverse=True):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else path.stem
        preview = ""
        for line in text.splitlines():
            if line.startswith("- ") or line.startswith("* "):
                preview = line.lstrip("-* ").strip()
                break
        items.append(
            {
                "name": path.name,
                "title": title,
                "preview": preview[:160],
                "href": "inbox.html#" + path.stem,
                "body": text,
            }
        )
    return items


def wiki_shell(
    title: str,
    body: str,
    *,
    depth: int,
    active: str | None,
    nav_html: str,
    search_json: str,
) -> str:
    prefix = "../" * depth if depth else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {WIKI_NAME}</title>
<link rel="stylesheet" href="{prefix}assets/wiki.css">
<script defer src="{prefix}assets/wiki.js"></script>
</head>
<body>
<div class="wiki">
<aside class="sidebar">
  <div class="brand"><a href="{prefix}index.html">{WIKI_NAME}</a></div>
  <label class="search-label" for="wiki-search">Search</label>
  <input id="wiki-search" type="search" placeholder="Disease, trial, drug…" autocomplete="off">
  <div id="search-results" class="search-results" hidden></div>
  <nav class="nav" aria-label="Topics">
{nav_html}
  </nav>
  <p class="sidebar-foot"><a href="{prefix}inbox.html">Inbox</a> · <a href="{prefix}index.html">Home</a></p>
</aside>
<main class="main">
{body}
</main>
</div>
<script type="application/json" id="wiki-index">{search_json}</script>
</body>
</html>
"""


def build_nav(articles: list[Article], active: str | None, depth: int) -> str:
    prefix = "../" * depth if depth else ""
    by_key: dict[tuple[str, str], list[Article]] = defaultdict(list)
    domains_present: set[str] = set()
    for a in articles:
        by_key[(a.domain, a.disease)].append(a)
        domains_present.add(a.domain)
    for domain, disease in PLANNED:
        domains_present.add(domain)

    parts: list[str] = []
    for domain in DOMAIN_ORDER:
        if domain not in domains_present:
            continue
        dlabel = DOMAIN_LABEL.get(domain, domain.title())
        parts.append(f'    <div class="nav-domain">{html.escape(dlabel)}</div>')
        diseases = DISEASE_ORDER.get(domain, [])
        # Include any unexpected diseases that have articles
        extra = sorted({d for (dom, d) in by_key if dom == domain} - set(diseases))
        for disease in diseases + extra:
            arts = by_key.get((domain, disease), [])
            planned = PLANNED.get((domain, disease), [])
            if not arts and not planned:
                continue
            label = DISEASE_LABEL.get(disease, disease)
            parts.append(
                f'    <div class="nav-group"><div class="nav-disease">{html.escape(label)}</div><ul>'
            )
            for a in arts:
                cls = "active" if active == a.active_key else ""
                stale = ' <span class="pill stale">stale</span>' if a.is_stale else ""
                stub = ' <span class="pill stub">stub</span>' if a.is_stub else ""
                parts.append(
                    f'      <li class="{cls}"><a href="{prefix}{a.href}">{html.escape(article_setting_label(a))}</a>{stale}{stub}</li>'
                )
            for label_p in planned:
                parts.append(
                    f'      <li class="planned"><span>{html.escape(label_p)}</span> '
                    f'<span class="pill muted">not started</span></li>'
                )
            parts.append("    </ul></div>")
    return "\n".join(parts)


def search_index_json(articles: list[Article], depth: int) -> str:
    prefix = "../" * depth if depth else ""
    rows = [
        {
            "title": a.title,
            "href": prefix + a.href,
            "domain": a.domain,
            "disease": a.disease,
            "setting": a.setting,
            "blob": a.search_blob[:4000],
        }
        for a in articles
    ]
    return json.dumps(rows, ensure_ascii=False)


def render_home(articles: list[Article], inbox: list[dict[str, str]]) -> str:
    stale = [a for a in articles if a.is_stale]
    stubs = [a for a in articles if a.is_stub]
    nav = build_nav(articles, None, 0)
    sjson = search_index_json(articles, 0)

    start_bits: list[str] = []
    if inbox:
        start_bits.append(
            f'<li><a href="inbox.html"><strong>{len(inbox)}</strong> inbox item(s)</a> awaiting review</li>'
        )
    else:
        start_bits.append("<li>Inbox empty</li>")
    if stale:
        for a in stale:
            start_bits.append(
                f'<li class="warn"><a href="{a.href}">{html.escape(a.setting)}</a> — '
                f'next review {html.escape(a.next_review)} (overdue)</li>'
            )
    else:
        start_bits.append("<li>No articles past next-review date</li>")

    cards: list[str] = []
    by_domain: dict[str, list[Article]] = defaultdict(list)
    for a in articles:
        by_domain[a.domain].append(a)

    for domain in DOMAIN_ORDER:
        arts = by_domain.get(domain, [])
        planned_diseases = {d for (dom, d) in PLANNED if dom == domain}
        if not arts and not planned_diseases:
            continue
        dlabel = DOMAIN_LABEL.get(domain, domain.title())
        cards.append(f'<section class="home-section"><h2>{html.escape(dlabel)}</h2>')
        diseases = DISEASE_ORDER.get(domain, [])
        extra = sorted({a.disease for a in arts} - set(diseases))
        for disease in diseases + extra:
            disease_arts = [a for a in arts if a.disease == disease]
            planned = PLANNED.get((domain, disease), [])
            if not disease_arts and not planned:
                continue
            label = DISEASE_LABEL.get(disease, disease)
            cards.append(f'<h3 class="disease-h">{html.escape(label)}</h3><ul class="article-list">')
            for a in disease_arts:
                meta = []
                if a.last_reviewed:
                    meta.append(f"reviewed {html.escape(a.last_reviewed)}")
                if a.is_stub:
                    meta.append("stub")
                if a.is_stale:
                    meta.append("stale")
                meta_s = " · ".join(meta)
                cards.append(
                    f'<li><a href="{a.href}"><strong>{html.escape(article_setting_label(a))}</strong></a>'
                    f'<span class="meta">{meta_s}</span>'
                    f'<div class="blurb">{html.escape(a.purpose)}</div></li>'
                )
            for label_p in planned:
                cards.append(
                    f'<li class="planned"><strong>{html.escape(label_p)}</strong>'
                    f'<span class="meta">not started</span></li>'
                )
            cards.append("</ul>")
        cards.append("</section>")

    stubs_note = (
        f'<p class="lede">{len(stubs)} of {len(articles)} articles still marked stub — '
        "expand before relying on them in clinic.</p>"
        if stubs
        else ""
    )

    body = f"""
<header class="page-head">
  <h1>{WIKI_NAME}</h1>
  <p class="lede">Personal oncology notes for clinic — evidence pages and Epic phrases.
  Domains under <code>pathways/</code> (GU first; lung/heme ready when you add them).
  Markdown is canonical; this site is generated.</p>
  {stubs_note}
</header>
<section class="start-here">
  <h2>Start here</h2>
  <ul>
    {"".join(start_bits)}
  </ul>
</section>
{"".join(cards)}
<p class="gen-note">Generated {html.escape(datetime.now().strftime("%Y-%m-%d %H:%M"))}. Run
<code>python3 scripts/build_wiki.py</code> after edits.</p>
"""
    return wiki_shell("Home", body, depth=0, active=None, nav_html=nav, search_json=sjson)


def render_article(art: Article, articles: list[Article]) -> str:
    depth = art.depth
    nav = build_nav(articles, art.active_key, depth)
    sjson = search_index_json(articles, depth)
    prefix = "../" * depth

    badges: list[str] = []
    if art.is_stub:
        badges.append('<span class="pill stub">stub</span>')
    if art.is_stale:
        badges.append('<span class="pill stale">stale</span>')
    badge_html = " ".join(badges)

    related = RELATED.get((art.domain, art.disease, art.setting), [])
    related_html = ""
    if related:
        links = []
        for dom, d, s, label in related:
            links.append(
                f'<a href="{prefix}{dom}/{d}/{s.lower()}.html">{html.escape(label)}</a>'
            )
        related_html = (
            '<nav class="related"><span>See also:</span> ' + " · ".join(links) + "</nav>"
        )

    phrase_block = ""
    if art.phrase_text:
        b64 = base64.b64encode(art.phrase_text.encode("utf-8")).decode("ascii")
        lis = "".join(
            f"<li>{render_phrase_line(ln.lstrip('- ').strip(), art.phrase_controls)}</li>"
            for ln in art.phrase_lines
        )
        phrase_tools = render_phrase_tools(art)
        phrase_tools_block = f"  {phrase_tools}\n" if phrase_tools else ""
        phrase_block = f"""
<section class="phrase" id="dotphrase">
  <div class="phrase-head">
    <h2>Epic phrase</h2>
    <button type="button" class="copy-btn" data-copy-b64="{b64}">Copy</button>
  </div>
  <p class="trigger"><code>{html.escape(art.trigger)}</code></p>
{phrase_tools_block}  <ul class="phrase-body">{lis}</ul>
  <p class="src"><a href="{prefix}../{art.md_rel}/dotphrase.md">Edit markdown</a></p>
</section>
"""

    evidence_rest = art.evidence_html
    references_marker = '<h2 id="guideline-references">'
    if phrase_block and references_marker in evidence_rest:
        clinical_content, bottom_references = evidence_rest.split(
            references_marker, maxsplit=1
        )
        evidence_rest = f"{clinical_content}{phrase_block}{references_marker}{bottom_references}"
        phrase_block = ""
    dlabel = DOMAIN_LABEL.get(art.domain, art.domain)
    dislabel = DISEASE_LABEL.get(art.disease, art.disease)
    section_toc = render_section_toc(
        collect_section_headings(art.evidence_body),
        has_phrase=bool(art.phrase_text),
    )

    body = f"""
<article>
<header class="page-head">
  <p class="crumb"><a href="{prefix}index.html">Home</a> /
  {html.escape(dlabel)} / {html.escape(dislabel)} / {html.escape(article_setting_label(art))}</p>
  <h1>{html.escape(art.title)} {badge_html}</h1>
  <p class="meta-line">
    Last reviewed: <strong>{html.escape(art.last_reviewed or "—")}</strong>
    · Next review: <strong>{html.escape(art.next_review or "—")}</strong>
  </p>
  <p class="status-line">{html.escape(art.status)}</p>
  {related_html}
</header>
{section_toc}

<section class="evidence" id="evidence">
  <h2 class="sr-only">Evidence page</h2>
  {evidence_rest}
  <p class="src"><a href="{prefix}../{art.md_rel}/evidence.md">Edit evidence markdown</a></p>
</section>

{phrase_block}
</article>
"""
    return wiki_shell(
        art.title, body, depth=depth, active=art.active_key, nav_html=nav, search_json=sjson
    )


def render_inbox(articles: list[Article], inbox: list[dict[str, str]]) -> str:
    nav = build_nav(articles, "inbox", 0)
    sjson = search_index_json(articles, 0)
    if not inbox:
        items_html = "<p>Inbox is empty. Monthly PubMed refresh writes here; promote into pathway evidence after review.</p>"
    else:
        blocks = []
        for item in inbox:
            body_html = md_block_to_html(item["body"])
            blocks.append(
                f'<section class="inbox-item" id="{html.escape(Path(item["name"]).stem)}">'
                f'<h2>{html.escape(item["title"])}</h2>'
                f'<p class="meta"><code>{html.escape(item["name"])}</code></p>'
                f"{body_html}</section>"
            )
        items_html = "\n".join(blocks)

    body = f"""
<header class="page-head">
  <h1>Inbox</h1>
  <p class="lede">Unreviewed deltas. Do not trust these as clinic SOC until promoted into
  <code>pathways/.../evidence.md</code>.</p>
</header>
{items_html}
"""
    return wiki_shell("Inbox", body, depth=0, active="inbox", nav_html=nav, search_json=sjson)


CSS = """\
:root {
  --bg: #f3f4f6;
  --paper: #ffffff;
  --ink: #1a1d23;
  --muted: #5c6570;
  --line: #d8dce3;
  --accent: #1d4ed8;
  --warn: #b45309;
  --stub: #4b5563;
  --sidebar-w: 15.5rem;
  --font: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  --sans: var(--font);
}
* { box-sizing: border-box; }
html { font-size: 15.5px; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font);
  line-height: 1.4;
}
.wiki { display: flex; min-height: 100vh; }
.sidebar {
  width: var(--sidebar-w);
  flex-shrink: 0;
  padding: 1rem 0.85rem 1.75rem;
  border-right: 1px solid var(--line);
  background: #eef0f3;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.brand { font-family: var(--sans); font-weight: 650; font-size: 0.92rem; margin-bottom: 0.85rem; }
.brand a { color: var(--ink); text-decoration: none; }
.search-label { font-family: var(--sans); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
#wiki-search {
  width: 100%;
  margin: 0.2rem 0 0.65rem;
  padding: 0.35rem 0.45rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  font: inherit;
  background: var(--paper);
}
.search-results {
  font-family: var(--sans);
  font-size: 0.82rem;
  margin-bottom: 0.65rem;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 3px;
  max-height: 12rem;
  overflow: auto;
}
.search-results a {
  display: block;
  padding: 0.3rem 0.45rem;
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid var(--line);
}
.search-results a:last-child { border-bottom: 0; }
.nav-group { margin-bottom: 0.65rem; }
.nav-domain {
  font-family: var(--sans);
  font-size: 0.76rem;
  font-weight: 650;
  letter-spacing: 0.02em;
  margin: 0.85rem 0 0.3rem;
  color: var(--ink);
}
.nav-domain:first-child { margin-top: 0; }
.nav-disease {
  font-family: var(--sans);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
  margin-bottom: 0.2rem;
}
.disease-h { font-size: 0.95rem; margin: 0.85rem 0 0.2rem; color: var(--muted); font-family: var(--sans); font-weight: 600; }
.nav ul { list-style: none; margin: 0; padding: 0; }
.nav li { margin: 0.12rem 0; font-size: 0.88rem; }
.nav a { color: var(--ink); text-decoration: none; }
.nav a:hover { color: var(--accent); }
.nav li.active > a { font-weight: 650; color: var(--accent); }
.nav li.planned { color: var(--muted); font-size: 0.82rem; }
.sidebar-foot { font-family: var(--sans); font-size: 0.78rem; color: var(--muted); margin-top: 1.25rem; }
.sidebar-foot a { color: var(--muted); }
.main {
  flex: 1;
  max-width: 58rem;
  padding: 1.25rem 1.75rem 2.5rem;
  background: var(--paper);
  min-height: 100vh;
  border-right: 1px solid var(--line);
}
.page-head h1 { font-size: 1.45rem; line-height: 1.2; margin: 0.15rem 0 0.35rem; font-weight: 650; }
.lede { color: var(--muted); margin-top: 0; }
.crumb { font-family: var(--sans); font-size: 0.76rem; color: var(--muted); margin: 0; }
.crumb a { color: var(--muted); }
.meta-line, .status-line, .meta { font-family: var(--sans); font-size: 0.8rem; color: var(--muted); }
.section-toc {
  position: sticky;
  top: 0;
  z-index: 5;
  margin: 0.65rem 0 0.85rem;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  background: #f8f9fb;
  font-family: var(--sans);
  font-size: 0.76rem;
  line-height: 1.3;
}
.section-toc-label {
  display: block;
  font-size: 0.65rem;
  font-weight: 650;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  margin-bottom: 0.25rem;
}
.section-toc-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem 0.55rem;
}
.section-toc-links a {
  color: var(--accent);
  text-decoration: none;
  white-space: nowrap;
}
.section-toc-links a:hover { text-decoration: underline; }
.pill {
  font-family: var(--sans);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 0.08rem 0.3rem;
  border-radius: 2px;
  border: 1px solid var(--line);
  color: var(--stub);
  vertical-align: middle;
}
.pill.stale { color: var(--warn); border-color: #fcd34d; background: #fffbeb; }
.pill.stub { background: #f3f4f6; }
.pill.muted { color: var(--muted); }
.start-here, .home-section { margin: 1.4rem 0; }
.start-here { padding: 0.65rem 0.85rem; border: 1px solid var(--line); border-radius: 3px; background: #f8f9fb; }
.start-here h2, .home-section h2 { font-size: 1.05rem; margin-top: 0; }
.article-list { list-style: none; padding: 0; margin: 0; }
.article-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--line);
}
.article-list .meta { display: block; margin-top: 0.1rem; }
.article-list .blurb { font-size: 0.88rem; color: var(--muted); }
.article-list li.planned { opacity: 0.65; }
.evidence h2 { font-size: 1.05rem; margin-top: 1.35rem; border-bottom: 1px solid var(--line); padding-bottom: 0.2rem; }
.evidence h3 { font-size: 0.95rem; margin-top: 1rem; }
.evidence ul, .phrase-body, .start-here ul { padding-left: 1.1rem; }
.evidence li, .phrase-body li { margin: 0.18rem 0; }
.table-wrap { overflow-x: auto; margin: 0.55rem 0 0.95rem; }
.evidence table { width: 100%; border-collapse: collapse; font-family: var(--sans); font-size: 0.74rem; line-height: 1.32; }
.evidence th, .evidence td { border: 1px solid var(--line); padding: 0.28rem 0.4rem; text-align: left; vertical-align: top; }
.evidence th { background: #e8ebf0; font-weight: 700; color: #111827; }
.table-wrap.cross_trial {
  padding: 0.25rem;
  border: 1px solid #bfdbfe;
  border-left: 4px solid var(--accent);
  border-radius: 3px;
  background: #eff6ff;
}
.table-wrap.cross_trial table { min-width: 64rem; background: var(--paper); }
.table-wrap.cross_trial th { background: #dbeafe; color: #1e3a8a; }
.table-wrap.cross_trial td:first-child {
  min-width: 8rem;
  font-weight: 650;
  color: #1e3a8a;
  background: #f8fbff;
}
.table-wrap.cross_trial tbody tr:nth-child(even) td { background: #fcfdff; }
.table-wrap.cross_trial tbody tr:hover td { background: #f0f7ff; }
.evidence-figure { margin: 0.7rem 0 1rem; padding: 0.5rem; border: 1px solid var(--line); background: #f8f9fb; }
.evidence-figure img { display: block; width: 100%; height: auto; }
.related { font-family: var(--sans); font-size: 0.8rem; margin: 0.55rem 0 0; }
.related a { color: var(--accent); }
.phrase {
  margin-top: 1.75rem;
  padding-top: 0.85rem;
  border-top: 2px solid var(--line);
}
.phrase-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.phrase-head h2 { margin: 0; font-size: 1.05rem; }
.trigger { font-family: var(--sans); }
.phrase-tools {
  margin: 0.85rem 0;
  padding: 0.75rem 0.85rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  background: #f8f9fb;
  font-family: var(--sans);
}
.phrase-tools h3, .phrase-calculator h4 { margin: 0; font-size: 0.9rem; }
.phrase-tools-note, .calculator-note, .calculator-result {
  margin: 0.3rem 0 0;
  color: var(--muted);
  font-size: 0.76rem;
}
.phrase-tools-grid { display: grid; gap: 0.7rem; margin-top: 0.7rem; }
.phrase-control { display: grid; gap: 0.25rem; }
.phrase-control label, .calculator-field label { font-size: 0.78rem; font-weight: 650; }
.phrase-control select, .calculator-field select {
  width: 100%;
  padding: 0.35rem 0.45rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  color: var(--ink);
  background: var(--paper);
  font: inherit;
}
.phrase-calculator {
  padding: 0.7rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  background: var(--paper);
}
.calculator-fields { display: grid; gap: 0.55rem; margin-top: 0.65rem; }
.calculator-field { display: grid; gap: 0.25rem; }
.calculator-result { color: var(--ink); font-weight: 650; }
.phrase-fill-in {
  color: var(--accent);
  font-family: var(--sans);
  font-size: 0.92em;
  font-weight: 650;
}
.copy-btn {
  font-family: var(--sans);
  font-size: 0.76rem;
  padding: 0.3rem 0.6rem;
  border: 1px solid var(--line);
  background: var(--bg);
  border-radius: 3px;
  cursor: pointer;
}
.copy-btn:hover { border-color: var(--accent); color: var(--accent); }
.copy-btn.copied { border-color: #15803d; color: #15803d; }
.src { font-family: var(--sans); font-size: 0.76rem; color: var(--muted); }
.src a { color: var(--muted); }
.gen-note { font-family: var(--sans); font-size: 0.72rem; color: var(--muted); margin-top: 2rem; }
.inbox-item { margin: 1.25rem 0; padding-bottom: 0.85rem; border-bottom: 1px solid var(--line); }
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0,0,0,0); border: 0;
}
code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; }
@media (max-width: 800px) {
  .wiki { flex-direction: column; }
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
  .main { border-right: 0; max-width: none; padding: 1rem; }
  .section-toc { position: static; }
}
"""

JS = r"""
(function () {
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c];
    });
  }

  function decodeB64(b64) {
    try {
      const bin = atob(b64);
      if (typeof TextDecoder !== "undefined") {
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        return new TextDecoder("utf-8").decode(bytes);
      }
      return decodeURIComponent(escape(bin));
    } catch (e) {
      return "";
    }
  }

  function decodeB64Json(b64) {
    try { return JSON.parse(decodeB64(b64)); } catch (e) { return []; }
  }

  function setupSearch() {
    const input = document.getElementById("wiki-search");
    const results = document.getElementById("search-results");
    const indexEl = document.getElementById("wiki-index");
    if (!input || !results || !indexEl) return;
    let index = [];
    try { index = JSON.parse(indexEl.textContent || "[]"); } catch (e) { index = []; }

    function run() {
      const q = (input.value || "").trim().toLowerCase();
      if (q.length < 2) {
        results.hidden = true;
        results.innerHTML = "";
        return;
      }
      const hits = index.filter(function (row) {
        return (row.blob || "").indexOf(q) !== -1 || (row.title || "").toLowerCase().indexOf(q) !== -1;
      }).slice(0, 12);
      if (!hits.length) {
        results.hidden = false;
        results.innerHTML = "<div style='padding:0.4rem 0.5rem;color:#78716c'>No matches</div>";
        return;
      }
      results.hidden = false;
      results.innerHTML = hits.map(function (h) {
        return '<a href="' + h.href + '">' + escapeHtml(h.title) + "</a>";
      }).join("");
    }

    input.addEventListener("input", run);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        input.value = "";
        run();
      }
    });
  }

  const KEYNOTE_564_FIELDS = [
    {
      id: "histology",
      label: "Clear-cell component",
      options: [
        ["", "Select…"],
        ["clear-cell", "Confirmed clear-cell component"],
        ["non-clear-cell", "Non-clear-cell or not confirmed"]
      ]
    },
    {
      id: "pt-stage",
      label: "Pathologic T stage",
      options: [
        ["", "Select…"],
        ["pt1", "pT1"],
        ["pt2", "pT2"],
        ["pt3", "pT3"],
        ["pt4", "pT4"],
        ["unknown", "pTx / unknown / other"]
      ]
    },
    {
      id: "grade",
      label: "Grade",
      options: [
        ["", "Select…"],
        ["grade-1-3", "Grade 1–3"],
        ["grade-4", "Grade 4"],
        ["unknown", "Unknown / not reported"]
      ]
    },
    {
      id: "sarcomatoid",
      label: "Sarcomatoid features",
      options: [
        ["", "Select…"],
        ["absent", "Absent"],
        ["present", "Present"],
        ["unknown", "Unknown / not reported"]
      ]
    },
    {
      id: "n-stage",
      label: "Pathologic N stage",
      options: [
        ["", "Select…"],
        ["n0", "N0"],
        ["n-plus", "N+"],
        ["unknown", "Unknown / not reported"]
      ]
    },
    {
      id: "m1-ned",
      label: "M1 NED status and timing",
      options: [
        ["", "Select…"],
        ["m0", "M0 (no M1 NED)"],
        ["qualifying", "Qualifying M1 NED: resected at nephrectomy or within 1 year"],
        ["nonqualifying", "M1 disease: M1 NED criteria or timing not met"],
        ["unknown", "Unknown / not documented"]
      ]
    }
  ];

  function incomplete(detail) {
    return detail ? "Incomplete — " + detail : "Complete calculator fields";
  }

  function keynote564Category(values) {
    if (!values.histology || !values["m1-ned"]) {
      return incomplete("select histology and M1 NED status");
    }
    if (values.histology !== "clear-cell") return "Not eligible";
    if (values["m1-ned"] === "qualifying") return "M1 NED";
    if (values["m1-ned"] === "nonqualifying") return "Not eligible";
    if (values["m1-ned"] === "unknown") return incomplete("document M1 NED status and timing");
    if (!values["n-stage"]) return incomplete("select pathologic N stage");
    if (values["n-stage"] === "n-plus") return "High risk";
    if (values["n-stage"] === "unknown") return incomplete("document pathologic N stage");
    if (!values["pt-stage"]) return incomplete("select pathologic T stage");
    if (values["pt-stage"] === "pt4") return "High risk";
    if (values["pt-stage"] === "pt3") return "Intermediate-high risk";
    if (values["pt-stage"] === "pt1") return "Not eligible";
    if (values["pt-stage"] === "unknown") return incomplete("document pathologic T stage");
    if (values["grade"] === "grade-4" || values.sarcomatoid === "present") {
      return "Intermediate-high risk";
    }
    if (!values.grade || !values.sarcomatoid) {
      return incomplete("select grade and sarcomatoid features");
    }
    if (values.grade === "unknown" || values.sarcomatoid === "unknown") {
      return incomplete("document grade and sarcomatoid features");
    }
    return "Not eligible";
  }

  function mountKeynote564Calculator(root, setPhraseValue) {
    const fieldsEl = root.querySelector(".calculator-fields");
    const resultEl = root.querySelector(".calculator-result");
    if (!fieldsEl || !resultEl) return;
    const values = {};
    KEYNOTE_564_FIELDS.forEach(function (field) {
      const wrapper = document.createElement("div");
      wrapper.className = "calculator-field";
      const label = document.createElement("label");
      const select = document.createElement("select");
      const selectId = "calculator-keynote-564-" + field.id;
      label.htmlFor = selectId;
      label.textContent = field.label;
      select.id = selectId;
      select.setAttribute("data-calculator-field", field.id);
      field.options.forEach(function (optionSpec) {
        const option = document.createElement("option");
        option.value = optionSpec[0];
        option.textContent = optionSpec[1];
        select.appendChild(option);
      });
      select.addEventListener("input", function () {
        values[field.id] = select.value;
        update();
      });
      wrapper.appendChild(label);
      wrapper.appendChild(select);
      fieldsEl.appendChild(wrapper);
    });

    function update() {
      const category = keynote564Category(values);
      resultEl.textContent = category;
      setPhraseValue(category);
    }
    update();
  }

  function setupPhraseTools() {
    const toolsets = document.querySelectorAll(".phrase-tools");
    toolsets.forEach(function (tools) {
      const controls = decodeB64Json(tools.getAttribute("data-phrase-controls-b64") || "");
      const template = decodeB64(tools.getAttribute("data-phrase-template-b64") || "");
      const values = {};

      function setPhraseValue(controlId, value) {
        values[controlId] = value;
        const phrase = tools.closest(".phrase");
        if (!phrase) return;
        phrase.querySelectorAll("[data-phrase-control]").forEach(function (slot) {
          if (slot.getAttribute("data-phrase-control") === controlId) {
            slot.textContent = value;
          }
        });
      }

      controls.forEach(function (control) {
        setPhraseValue(control.id, "Not selected");
        const controlEl = tools.querySelector(
          '[data-phrase-control-id="' + control.id + '"]'
        );
        if (!controlEl) return;
        if (control.kind === "select") {
          controlEl.addEventListener("input", function () {
            setPhraseValue(control.id, controlEl.value || "Not selected");
          });
          return;
        }
        if (control.kind === "calc" && control.id === "keynote-564") {
          mountKeynote564Calculator(controlEl, function (value) {
            setPhraseValue(control.id, value);
          });
        }
      });

      tools.getPhraseText = function () {
        return controls.reduce(function (text, control) {
          return text.split(control.token).join(values[control.id] || "Not selected");
        }, template);
      };
    });
  }

  function fallbackCopy(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }

  function setupCopy() {
    document.addEventListener("click", function (e) {
      const btn = e.target.closest(".copy-btn");
      if (!btn) return;
      const phrase = btn.closest(".phrase");
      const tools = phrase && phrase.querySelector(".phrase-tools");
      const text = tools && typeof tools.getPhraseText === "function"
        ? tools.getPhraseText()
        : decodeB64(btn.getAttribute("data-copy-b64") || "");
      const done = function () {
        btn.classList.add("copied");
        btn.textContent = "Copied";
        setTimeout(function () {
          btn.classList.remove("copied");
          btn.textContent = "Copy";
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () {
          fallbackCopy(text); done();
        });
      } else {
        fallbackCopy(text); done();
      }
    });
  }

  setupSearch();
  setupPhraseTools();
  setupCopy();
})();
"""


def main() -> int:
    articles = load_articles()
    inbox = list_inbox()

    if SITE.exists():
        # Clear generated output but keep structure.
        for p in SITE.rglob("*"):
            if p.is_file() and p.suffix in {
                ".html",
                ".css",
                ".js",
                ".svg",
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
            }:
                p.unlink()

    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "wiki.css").write_text(CSS, encoding="utf-8")
    (ASSETS / "wiki.js").write_text(JS, encoding="utf-8")

    (SITE / "index.html").write_text(render_home(articles, inbox), encoding="utf-8")
    (SITE / "inbox.html").write_text(render_inbox(articles, inbox), encoding="utf-8")

    for art in articles:
        out_dir = SITE / art.domain / art.disease
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{art.setting.lower()}.html").write_text(
            render_article(art, articles), encoding="utf-8"
        )
        source_figures = PATHWAYS / art.domain / art.disease / art.setting / "figures"
        if source_figures.is_dir():
            shutil.copytree(source_figures, out_dir / "figures", dirs_exist_ok=True)

    print(f"Built {len(articles)} articles + home + inbox → {SITE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
