# GU clinic (MedOnc wiki)

Cursor project under **Projects → GU-clinic** for living oncology clinic notes.

GU pathways live here; lung/heme/etc. can be added under `pathways/` later without a new project.

## Open the wiki

```bash
open site/index.html
```

After edits: `python3 scripts/build_wiki.py`

## Layout

```
pathways/gu/{disease}/{setting}/
  evidence.md
  dotphrase.md

# Later examples (same project):
# pathways/lung/nsclc/...
# pathways/heme/aml/...

inbox/
site/          # generated HTML — do not hand-edit
scripts/
```

Open this folder: `/Users/Alex/Projects/GU-clinic`  
(`~/Documents/GU-clinic` is a symlink to the same tree.)

Sister product (biomarker / methylation): `/Users/Alex/Documents/EpiAI`.

## Updating

- Edit markdown; bump **Last reviewed**, **Next review**, **Changelog**.
- `save to knowledge base` in clinical chats writes here (opt-in).
- Inbox: `python3 scripts/inbox_refresh.py` → review → promote → rebuild.

## Not

- OneNote / Notion / Canvas
- Separate MedOnc-wiki project (that folder is a pointer back here)
- PHI / patient chart
