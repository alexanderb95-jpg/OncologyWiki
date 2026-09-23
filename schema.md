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
| domain | `gu`, `cellular`, `lung`, `heme` |
| disease | `prostate`, `bladder`, `gene-cellular`, `nsclc`, `aml` |
| setting | `mHSPC`, `mCRPC`, `mUC`, `overview` |

## Evidence header fields

| Field | Example |
|-------|---------|
| Last reviewed | `2026-09-14` |
| Next review | `2026-12-14` (~90 days) |
| Owner / Purpose / Status | as in briefs |

Required sections on **disease-setting** pages (e.g. GU): Who this applies to, Standard options, Landmark evidence, Biomarkers, Upcoming research, Toxicity, Guideline references, Sources, Changelog. Do not add a Bottom line section. Do **not** require a Gene and cellular therapy section on GU pages.

**Gene / cellular therapy** is a **standalone domain** at `pathways/cellular/gene-cellular/overview/` (nav label Gene / cellular therapy). Register domain/disease/setting labels in `scripts/build_wiki.py`. Cross-disease landscape page — not nested under GU.

## Inbox

`inbox/YYYY-MM-DD.md` — high-yield PubMed only. Never auto-promote.

## Build

```bash
python3 scripts/build_wiki.py
```
