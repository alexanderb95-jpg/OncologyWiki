# Cloud Agents — skills / rules / hooks

Committed in this repo so OncologyWiki Cloud Agents always see them:

| Kind | Path |
|------|------|
| Skills | `.cursor/skills/*/SKILL.md` |
| Rules | `.cursor/rules/*.mdc` |
| Hooks | `.cursor/hooks.json` + `.cursor/hooks/*.sh` |
| Guide | `AGENTS.md` |

## Also turn on (you, once)

**Settings → Agents → Sync Skills for Cloud Agents**

That syncs the rest of `~/.cursor/skills/` (AWS, etc.) privately to your cloud runs.
It does **not** sync hooks or `~/.agents/skills/`.

## Limits

- Cloud hooks: command-based only; no `sessionStart` / `sessionEnd`
- Push before starting a cloud agent (it clones remote, not dirty local files)
