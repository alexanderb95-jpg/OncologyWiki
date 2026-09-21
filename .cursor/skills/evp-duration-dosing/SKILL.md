---
name: evp-duration-dosing
description: >-
  Produces a succinct EPIC SmartPhrase (.evpdose) and evidence table for
  enfortumab vedotin plus pembrolizumab (EV+P, EVP) duration and dosing in
  metastatic / locally advanced urothelial carcinoma (mUC, la/mUC). Re-retrieves
  PubMed and congress evidence on a 6-month cadence. Use when the user types
  .evpdose, .evpduration, EV+P duration, EVP dosing, how long to continue EV,
  3 vs 6 cycles EV+P, EV RDI, stop EV after response, or asks for an Epic note
  on holding or dose-reducing EV+P.
---

# EV+P duration / dosing (mUC) — `.evpdose`

Personal clinic skill. Not perioperative MIBC (KEYNOTE-905 / B15). Those cycle counts are neoadjuvant vs adjuvant sandwich, not metastatic induction.

Follow [medical-evidence-search](../medical-evidence-search/SKILL.md). Do not invent numbers. Label **published journal** vs **congress / secondary**.

## Triggers

| User types | Action |
|---|---|
| `.evpdose` | Paste-ready EPIC note + canvas table from current ledger if <6 months old; otherwise full refresh |
| `.evpdose refresh` | Always re-run PubMed/congress searches, rewrite note + canvas + ledger |
| `.evpduration` | Same as `.evpdose` |
| Automation / calendar tick | Same as `.evpdose refresh` |

Epic SmartPhrase name to create in Hyperspace: **`.evpdose`**

## Workflow

Copy and track:

```
- [ ] Named PubMed searches from pubmed-queries.md (sort pub_date)
- [ ] Fetch abstracts; PMC full text when PMCID exists
- [ ] Congress: ASCO / ASCO GU / ESMO EV-302 updates, UNITE, RDI
- [ ] Secondary news (e.g. GU Oncology Now) only as a pointer to the abstract — never as the primary number source
- [ ] Diff vs ledger.json tracked_pmids
- [ ] Rewrite CURRENT-NOTE.txt (ASCII, Epic-safe)
- [ ] Rewrite canvases/evp-muc-duration-dosing.canvas.tsx
- [ ] Update ledger.json (last_refresh, next_due = +6 months, tracked_pmids)
```

Skip the council unless the user asks for a full evidence review.

## Output (this order)

1. **EPIC note** — fenced `text` block, contents of `CURRENT-NOTE.txt`. No markdown inside the fence. Epic wildcards stay as `***choice***`.
2. **Canvas** — write/update `/Users/Alex/.cursor/projects/Users-Alex-Documents-EpiAI/canvases/evp-muc-duration-dosing.canvas.tsx`. Chat must markdown-link that absolute path. Do not dump the evidence table as a markdown table in chat.
3. **Delta** — 3–8 bullets: new PMIDs, changed numbers, still-missing RCT.
4. **Next due** — ISO date from ledger.

Do not append onc-visit counseling. This is MDM paste, not a visit pathway.

## Clinical claims that must survive every refresh

State these only if still true in retrieved text; otherwise replace with the new source wording:

- No randomized 3-vs-6-cycle EV+P trial in mUC.
- EV-302 protocol: EV 1.25 mg/kg D1/D8 + pembrolizumab 200 mg D1 q21d to PD/toxicity; pembrolizumab cap ~35 cycles; no EV cycle cap.
- First PR clusters around first restaging (~3 cycles / ~2 months). CR often later; many CRs convert from PR with more EV.
- On-treatment EV reductions after early cycles are not the same question as starting below 1.25 mg/kg.
- Stopping EV for CR/toxicity and continuing pembrolizumab is selected-patient observational practice, not a tested de-escalation protocol.

## Files

| File | Role |
|---|---|
| [pubmed-queries.md](pubmed-queries.md) | Mandatory search strings |
| [epic-note-template.md](epic-note-template.md) | Structure of CURRENT-NOTE.txt |
| [CURRENT-NOTE.txt](CURRENT-NOTE.txt) | Latest paste-ready SmartPhrase |
| [ledger.json](ledger.json) | Dates + PMID inventory |
| [scripts/check_due.py](scripts/check_due.py) | sessionStart overdue injector |

## Canvas rules

Path: `/Users/Alex/.cursor/projects/Users-Alex-Documents-EpiAI/canvases/evp-muc-duration-dosing.canvas.tsx`

Read `~/.cursor/skills-cursor/canvas/SKILL.md` before editing. Import only from `cursor/canvas`. Embed data inline. Caption every table with source and snapshot date.

## 6-month automation (already wired)

- Calendar: recurring every 6 months on `alexanderb95@gmail.com` (title contains `.evpdose`).
- sessionStart hook: if `ledger.json` `next_due` is today or past, injects a refresh reminder.
- Cursor Automations: scheduled cloud run with prompt `.evpdose refresh`.

Do not start a local 6-month `sleep` loop. If calendar or automation is missing on refresh, recreate them and say so.

## Quality bar

- Every number in the EPIC note is in a retrieved abstract, PMC section, or congress abstract text.
- Congress rows say `congress` in the table status column.
- GU Oncology Now / OncLive / Pharmacy Times are secondary; cite the underlying abstract ID.
- If a prior ledger number cannot be re-found, drop it rather than carry it forward.
