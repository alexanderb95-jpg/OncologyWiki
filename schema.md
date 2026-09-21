# MedOnc wiki schema

Canonical knowledge is markdown. HTML under `site/` is generated.

## Pathway folder

```
pathways/{domain}/{disease}/{setting}/
  evidence.md
  dotphrase.md
```

| Level | Examples |
|-------|----------|
| domain | `gu`, `lung`, `heme` |
| disease | `prostate`, `bladder`, `nsclc`, `aml` |
| setting | `mHSPC`, `mCRPC`, `mUC` |

## Evidence header fields

| Field | Example |
|-------|---------|
| Last reviewed | `2026-09-14` |
| Next review | `2026-12-14` (~90 days) |
| Owner / Purpose / Status | as in briefs |

Required sections: Who this applies to, Standard options, Landmark evidence, Biomarkers, Upcoming trial results, Toxicity, Guideline references, Sources, Changelog. Do not add a Bottom line section.

## Inbox

`inbox/YYYY-MM-DD.md` — high-yield PubMed only. Never auto-promote.

## Build

```bash
python3 scripts/build_wiki.py
```
