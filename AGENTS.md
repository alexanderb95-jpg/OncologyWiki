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

## Cloud Agents

This repo is self-contained for cloud:

- Skills: `.cursor/skills/` (med-onc + evidence stack)
- Rules: `.cursor/rules/*.mdc`
- Hooks: `.cursor/hooks.json` (command hooks: `beforeSubmitPrompt`, `stop`)
- Guide: this `AGENTS.md`

For **personal** skills still only in `~/.cursor/skills/` (e.g. AWS packs): turn on
**Settings → Agents → Sync Skills for Cloud Agents**. Synced skills stay private to you.

Do not rely on laptop `~/.cursor/hooks.json` or `~/.cursor/med-onc-kb` in the cloud VM.
