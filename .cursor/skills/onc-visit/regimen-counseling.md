# Regimen Counseling Templates (Onc Visit)

Populate **only** from retrieved trial, label, or guideline text. Use plain language suitable for patient counseling. One subsection per regimen **discussed** in the visit report.

---

## Template (copy per regimen)

```markdown
### [Regimen name]
- **What it is:** One-sentence mechanism + intent (curative vs bladder-preserving vs palliative)
- **Schedule / dosing:** Drug, dose, days, cycle length, number of cycles, maintenance duration
- **How it is given:** IV infusion / oral; outpatient vs inpatient; typical time per visit; premedications if in source
- **Expected benefits:** Trial endpoint in plain language (e.g., "2-year survival ~82% vs 75% with chemotherapy and surgery alone")
- **Common side effects:** List from trial safety table or label
- **Serious risks / monitoring:** Grade ≥3 AEs, immune-related AEs, labs, cardiac/pulmonary monitoring
- **Practical considerations:** Hydration for cisplatin, fertility preservation, stent/PCN care, when to call clinic
- **Evidence:** Author Year (Journal) PMID …
```

If any field is missing from sources: `Not verified in retrieved sources.`

---

## MIBC anchor regimens (verify doses in PubMed before use)

### NIAGARA — perioperative durvalumab + gemcitabine–cisplatin → RC → adjuvant durvalumab

| Field | Trial-verified detail (Powles 2024 NEJM PMID 39282910) |
|-------|--------------------------------------------------------|
| Schedule | Neoadjuvant durvalumab + GC ×4 q3wk → RC (within ~12 wk of randomization) → adjuvant durvalumab q4wk ×8 (up to ~8 mo post-surgery) |
| GC | Gemcitabine 1000 mg/m² d1,8 + cisplatin 70 mg/m² d1 q3wk ×4 |
| Durvalumab | 1120 mg q3wk with neoadjuvant; 1120 mg q4wk adjuvant |
| Route | IV |
| Key outcomes | 24-mo EFS 67.8% vs 59.8%; OS 82.2% vs 75.2% |
| Grade ≥3 TRAEs | 57.0% vs 56.8% (similar overall) |
| Counseling | Requires RC; not for inoperable disease; discuss pCR 37.3% vs 27.5% |

### EV-303 — perioperative enfortumab vedotin + pembrolizumab → RC (cisplatin-ineligible)

| Field | Published detail (Vulsteke 2026 NEJM PMID 41707170 — verify current label) |
|-------|-------------------------------------------------------------------------------|
| Neoadjuvant | EV 1.25 mg/kg IV d1,8 + pembrolizumab 200 mg IV d1 q3wk ×3 → RC + PLND |
| Adjuvant | EV ×6 + pembrolizumab ×14 q3wk |
| Key outcomes | 2-y EFS 74.7% vs 39.4% (RC alone); OS 79.7% vs 63.1% |
| Counseling | Peripheral neuropathy, rash, hyperglycemia (EV); immune-related AEs (pembro); requires RC |

### BC2001 trimodality — 5-FU + mitomycin C + radiotherapy

| Field | Trial detail (James 2012 NEJM PMID 22512481; Hall 2022 10-y update PMID 35577644) |
|-------|-------------------------------------------------------------------------------------|
| RT | 55 Gy/20 fx or 64 Gy/32 fx to whole bladder |
| Chemo | 5-FU 500 mg/m²/d on RT d1–5 and 16–20 + mitomycin C 12 mg/m² d1 |
| Route | 5-FU IV infusion on radiation days; MMC IV d1 |
| Key outcomes | Improved locoregional control (HR ~0.61–0.68 long-term); 5-y OS ~48% chemoRT vs 35% RT alone (primary trial) |
| Common AEs | Grade 3–4 during treatment ~36% chemoRT vs 27.5% RT alone |
| Counseling | Bladder preserved; lifelong cystoscopic surveillance; ~14% 5-y salvage cystectomy rate with chemoRT; **worse outcomes if hydronephrosis present** |

### Hypofractionated TMT schedule (preferred RT fractionation)

| Field | Choudhury meta-analysis of BC2001/BCON (cited HK consensus PMID 40406240) |
|-------|-------------------------------------------------------------------------------|
| Schedule | **55 Gy in 20 fractions over 4 weeks** to whole bladder with concurrent radiosensitizer |
| Counseling | Non-inferior toxicity vs 64 Gy/32 fx; lower invasive locoregional recurrence vs longer schedule |

### NAC → CRT (bladder preservation, selected cisplatin-fit)

| Field | Princess Margaret series (Jiang 2019 PMID 30686350) |
|-------|---------------------------------------------------|
| NAC | Gemcitabine–cisplatin ×2–4 |
| CRT | EBRT 60–66 Gy/6 wk + concurrent cisplatin 40 mg/m² weekly |
| Outcomes | 2-y OS 74%; 2-y bladder-intact DFS 64%; salvage cystectomy 14% |
| Counseling | Retrospective; baseline hydronephrosis associated with worse OS |

### CheckMate 274 — adjuvant nivolumab post-RC

| Field | Bajorin 2021 NEJM PMID 34077643 |
|-------|----------------------------------|
| Population | ypT2–4a and/or ypN+ after neoadjuvant chemo, or pT3–4a/pN+ without neoadjuvant |
| Schedule | Nivolumab 240 mg IV q2wk ×1 year |
| Key outcomes | DFS HR 0.70; median DFS 20.8 vs 10.8 mo |
| Counseling | Immune-related AEs; not substitute for perioperative pathway if durvalumab already given |

### EV-302 — first-line enfortumab vedotin + pembrolizumab (unresectable/mUC)

| Field | Powles 2024 NEJM PMID 38446675 |
|-------|--------------------------------|
| Schedule | EV 1.25 mg/kg d1,8 + pembro 200 mg d1 q3wk until progression/toxicity (median 12 cycles in trial) |
| Key outcomes | OS 31.5 vs 16.1 mo (HR 0.47); PFS 12.5 vs 6.3 mo |
| Grade ≥3 TRAEs | 55.9% vs 69.5% (chemo comparator arm) |
| Counseling | For unresectable/metastatic disease; neuropathy/diabetes caution with EV |

### CheckMate 901 — nivolumab + gemcitabine–cisplatin (unresectable/mUC, cisplatin-eligible)

| Field | van der Heijden 2023 NEJM PMID 37870949 |
|-------|------------------------------------------|
| Schedule | Nivolumab 360 mg + GC q3wk ×6 → nivolumab 480 mg q4wk up to 2 y |
| GC | Standard gemcitabine–cisplatin |
| Key outcomes | OS 21.7 vs 18.9 mo (HR 0.78); ORR 57.6% vs 43.1% |
| Grade ≥3 TRAEs | 61.8% vs 51.7% |
| Counseling | Hydration for cisplatin; immune-related AEs |

### JAVELIN Bladder 100 — GC → avelumab maintenance

| Field | Verify in PubMed before counseling |
|-------|-----------------------------------|
| Sequence | Gemcitabine–cisplatin or gemcitabine–carboplatin ×4–6 → if no progression, avelumab maintenance |
| Key outcomes | OS HR 0.69 vs BSC after chemo (maintenance phase) |
| Counseling | Only if no progression after platinum; infusion q2wk maintenance |

---

## Hydronephrosis-specific counseling points

Include when obstruction is present:

1. **Why kidney drainage comes first** — protect renal function and clarify treatment options.
2. **Stent vs nephrostomy** — stent preferred when feasible; PCN may complicate chemotherapy delivery.
3. **Prognosis** — hydronephrosis marks more advanced disease and worse outcomes with any modality; bilateral worse than unilateral.
4. **TMT** — consensus **not preferred** with tumor-related hydronephrosis; if bladder preservation pursued, frame as higher-risk.
5. **After drainage** — repeat imaging and recheck whether cisplatin can be used safely.

---

## Side-effect clusters (use when trial tables not retrieved)

Only use generic clusters if specific trial rates unavailable — label as "class effects; verify grade ≥3 rates in trial":

| Agent class | Common | Serious / monitor |
|-------------|--------|-------------------|
| Cisplatin | Nausea, fatigue, low blood counts | Nephrotoxicity, ototoxicity, neuropathy — hydration, audiometry |
| Durvalumab / nivolumab / pembrolizumab | Fatigue, rash, thyroid dysfunction | Pneumonitis, colitis, hepatitis, endocrinopathies — report dyspnea, diarrhea |
| Enfortumab vedotin | Fatigue, rash, peripheral neuropathy, alopecia | Hyperglycemia, skin reactions; neuropathy may require hold/dose modify |
| 5-FU / mitomycin C (with RT) | Cystitis, diarrhea, skin reaction in field | Myelosuppression (MMC), hand-foot (5-FU) |
| Radiotherapy | Urinary frequency, dysuria, fatigue | Late bladder fibrosis, hematuria; pelvic bone effects |

Always prefer **trial-reported** grade ≥3 rates when available in retrieved text.
