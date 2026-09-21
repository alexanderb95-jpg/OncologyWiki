# Oncology comparative landscape tables

Use when answering **contemporary management**, **standard of care**, or **trial comparison** questions in oncology (especially perioperative, adjuvant, or first-line systemic therapy).

## Mandatory table columns

Every **comparative landscape** table must name the full regimen in each arm. Do not use drug shorthand alone (e.g., "durvalumab" or "EVP") without dosing, sequence, and surgery/radiation context.

| Column | Required content |
|--------|------------------|
| Trial | Name + registry ID if available |
| Population | Eligibility in plain language (stage, line, cisplatin eligibility, N) |
| **Intervention arm** | Full sequence: neoadjuvant → local therapy → adjuvant; drugs, doses/cycles when published |
| **Control arm** | Full comparator regimen (not "standard of care" alone) |
| Primary endpoints | As defined in the trial |
| Key outcomes | EFS/OS/pCR (or trial-specific) with **both arms' values** |
| Key HR | With 95% CI when published |
| Evidence status | Published journal + PMID; or "reported, primary publication pending"; FDA/EMA label date if verified |

Optional columns: grade ≥3 TRAE rate, RC rate, follow-up duration.

### Bad vs good (intervention arm cell)

```text
# BAD
Intervention: Durvalumab

# GOOD
Intervention: Neoadjuvant durvalumab + gemcitabine-cisplatin ×4 → RC + PLND → adjuvant durvalumab ×8
```

```text
# BAD
Intervention: EV + pembro

# GOOD
Intervention: Neoadjuvant EV (1.25 mg/kg d1,8) + pembrolizumab (200 mg d1 q3wk) ×3 → RC + PLND → adjuvant EV ×6 + pembrolizumab ×14
```

## Recency gate (before answering "contemporary management")

For fast-moving indications, run **named-trial PubMed searches** in parallel before drafting recommendations. Do not rely on training data alone.

1. Search indication + `phase 3` + `sort: pub_date`
2. Search known trial acronyms (e.g., EV-303, KEYNOTE-905, EV-304, NIAGARA, CheckMate 274)
3. Search `[drug class] + perioperative OR neoadjuvant + [indication]` for the last 24 months
4. If a trial is cited in reviews but not yet in PubMed as primary publication, label outcomes **"reported; primary publication pending"** and cite the review or congress source explicitly
5. State regulatory status only when verified (FDA approval summary in PubMed, label, or society guideline)

## Canonical example: perioperative muscle-invasive bladder cancer (MIBC)

Last verified: 2026-07. Re-run PubMed before clinical use; this file is a checklist, not live guidance.

| Trial | Population | Intervention arm | Control arm | 2-y EFS | 2-y OS | pCR | Key HR | Evidence status |
|-------|------------|----------------|-------------|---------|--------|-----|--------|-----------------|
| EV-303 / KEYNOTE-905 | Cisplatin-ineligible or declined; cT2–T4aN0M0 or T1–T4aN1M0; N=344 | Neoadjuvant EV (1.25 mg/kg d1,8) + pembrolizumab (200 mg d1 q3wk) ×3 → RC + PLND → adjuvant EV ×6 + pembrolizumab ×14 | RC + PLND alone | 74.7% vs 39.4% | 79.7% vs 63.1% | 57.1% vs 8.6% | EFS HR 0.40; OS HR 0.50 | Vulsteke 2026 NEJM PMID 41707170; FDA perioperative EVP cisplatin-ineligible (Nov 2025 per Jang 2026 review PMID 42367727) |
| EV-304 / KEYNOTE-B15 | Cisplatin-eligible; cT2–T4aN0M0 or T1–T4aN1M0; N=808 | Neoadjuvant EV + pembrolizumab ×4 → RC + PLND → adjuvant EV ×5 + pembrolizumab ×13 | Neoadjuvant gemcitabine-cisplatin ×4 → RC + PLND (no adjuvant) | 79.4% vs 66.2% | 86.9% vs 81.3% | 55.8% vs 32.5% | EFS HR 0.53; OS HR 0.65 | Reported ASCO GU 2026; Jang 2026 Drugs Context PMID 42367727 — **primary journal publication pending** |
| NIAGARA | Cisplatin-eligible; cT2–T4aN0–1M0; N=1,063 | Neoadjuvant durvalumab + GC ×4 → RC → adjuvant durvalumab ×8 | Neoadjuvant GC ×4 → RC (no adjuvant) | 67.8% vs 59.8% | 82.2% vs 75.2% | 37.3% vs 27.5% | EFS HR 0.68; OS HR 0.75 | Powles 2024 NEJM PMID 39282910; FDA Mar 2025 |
| VESPER | cT2–T4aN0M0 neoadj subgroup | dd-MVAC q2wk ×6 perioperative | GC ×4 perioperative | 3-y PFS 66% vs 56% | 5-y OS 66% vs 57% | organ-confined <ypT3N0 77% vs 63% | PFS HR 0.70; OS HR 0.71 (neoadj) | Pfister 2024 Lancet Oncol PMID 38142702 |
| CheckMate 274 | High-risk post-RC ypT2–T4a and/or ypN+; N=709 | Adjuvant nivolumab 240 mg q2wk ×1 year | Placebo ×1 year | — | median OS 75.0 vs 50.1 mo (5-y update) | — | DFS HR 0.74; OS HR 0.83 (NS at 5 y) | Bajorin 2021 NEJM PMID 34077643; Galsky 2026 Ann Oncol PMID 41110694 |

### MIBC contemporary default pathways (after recency gate)

- **Cisplatin-ineligible, resectable:** perioperative EV + pembrolizumab → RC (EV-303 published).
- **Cisplatin-eligible, resectable:** perioperative EV + pembrolizumab (EV-304 reported, confirm primary pub) **or** durvalumab + GC perioperative (NIAGARA published).
- **High-risk post-RC without prior perioperative ICI:** adjuvant nivolumab (CheckMate 274).
- **Bladder preservation (selected):** trimodality 5-FU/mitomycin C + RT (BC2001); ICI combinations investigational.
- **Unresectable/metastatic:** nivolumab + GC (CheckMate 901) or EV + pembrolizumab (EV-302) — distinct from perioperative MIBC.

### MIBC with hydronephrosis (M0) — apply [onc-visit](../onc-visit/mibc-pathways.md)

Reports must include **Branch 0** before treatment selection:

1. Relieve obstruction (ureteric stent preferred; PCN if needed)
2. Restage after drainage
3. Reassess cisplatin eligibility (GFR, hearing, neuropathy, PS)
4. MDT review

Then:

- **RC-feasible:** RC-anchored pathway (NIAGARA or EV perioperative if eligible) — **not** default TMT
- **TMT not preferred** with tumor-related hydronephrosis (HK/IBCG consensus); if bladder preservation used, counsel inferior outcomes (meta HR ~1.65 OS)
- **PCN before NAC:** cite lower adequate NAC completion (Savin 2024 PMID 38267303) when relevant

Always append **Patient counseling: treatment regimens discussed** per [onc-visit](../onc-visit/SKILL.md).

Cross-trial comparisons are indirect unless a head-to-head trial exists; state this explicitly.

## PubMed search strings (MIBC perioperative)

```
EV-303 OR KEYNOTE-905 enfortumab vedotin pembrolizumab muscle invasive bladder
EV-304 OR KEYNOTE-B15 enfortumab vedotin pembrolizumab neoadjuvant bladder
NIAGARA durvalumab muscle invasive bladder NEJM
perioperative muscle invasive bladder cancer immunotherapy review
```

Sort by `pub_date` for contemporary management questions.
