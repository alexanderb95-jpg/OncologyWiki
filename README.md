# GU clinic

Cursor workspace for **living GU oncology clinic notes**:

1. **Dot phrases** — Epic-style `#` triggers you revise over time
2. **Evidence briefs** — UpToDate-style 60-second skims beside each phrase, also refreshed over time

Open this folder in Cursor: `/Users/Alex/Projects/GU-clinic`

## Layout

Each clinical setting is its own folder:

```
pathways/{disease}/{setting}/
  dotphrase.md   # note text for Epic
  evidence.md    # clinic evidence overview
```

Current settings: prostate `mHSPC`, `mCRPC`; bladder `adjuvant-urothelial`, `mUC`; kidney `mRCC`.

See `PATHWAYS.md` for coverage checklist. Sister product project (biomarker / methylation skills): `/Users/Alex/Documents/EpiAI`.

## Updating over time

- Edit `dotphrase.md` whenever counseling or orders change.
- Edit `evidence.md` when practice changes; bump **Last reviewed** and **Changelog**.
- A Monday 8am routine (**GU clinic evidence refresh**) re-checks briefs and pings you only when something material changed.
