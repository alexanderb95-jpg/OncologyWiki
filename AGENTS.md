# GU clinic — agent guide

This repo is the **personal oncology wiki** (GU first). Markdown is canonical; `site/` is generated HTML.

## Structure

```
pathways/{domain}/{disease}/{setting}/
  evidence.md
  dotphrase.md
```

- Domains today: `gu`. Planned: `lung`, `heme`, …
- `inbox/` — unreviewed captures (never auto-promoted)
- `site/` — generated wiki. Do not hand-edit.

## Do

- Prefer counseling → decision → labs/NGS → procedures → meds → referrals → follow-up
- Never invent trial statistics
- Bump Last reviewed, Next review, Changelog on evidence edits
- After edits: `python3 scripts/build_wiki.py`
- EpiAI stays at `/Users/Alex/Documents/EpiAI`

## Knowledge base save

Only when user says `save to knowledge base` / `KB yes`. Write under this repo, then rebuild.

## Do not

- PHI
- Write OneNote or `~/.cursor/med-onc-kb` (archive)
- Hand-edit `site/*.html`
- Use `/Users/Alex/Projects/MedOnc-wiki` for new notes (pointer only)
