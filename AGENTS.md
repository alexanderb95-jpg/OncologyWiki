# GU clinic — agent guide

This repo is the **personal oncology wiki** (GU first). Markdown is canonical; `site/` is generated HTML.

## Structure

```
pathways/{domain}/{disease}/{setting}/
  evidence.md
  dotphrase.md
  figures/                 # optional source-recreated figure assets
```

- One wiki page covers one disease + setting; keep disease trees split into setting pages.
- Domains today: `gu`, `cellular` (Gene / cellular therapy overview). Planned: `lung`, `heme`, …
- `inbox/` — unreviewed captures (never auto-promoted)
- `site/` — generated wiki. Do not hand-edit.

## Do

- Use a clean OneNote-style hierarchy: disease → setting, short named sections, nested bullets, and tables only for structured comparisons.
- Keep clinical content first. Place brief **Guideline references** for the exact setting (NCCN, EAU, ESMO, AUA/ASCO/SUO as applicable) and **Sources** at the bottom, after the paired Epic phrase; include a guideline category/strength only when verified.
- Include comparison tables for standard options and trial tables for landmark evidence. For practice-changing survival endpoints, add full source-recreated KM curves using reported data; digitize a published curve only when necessary and label it as an approximate reconstruction. Never reuse copyrighted journal artwork or present interpolated values as reported data.
- Do not use a **Bottom line** section.
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
