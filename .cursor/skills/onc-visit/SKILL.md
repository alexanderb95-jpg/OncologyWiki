---
name: onc-visit
description: Structures oncology clinical management answers for MD/clinician use — decision algorithms, evidence tables, and patient-counseling regimens (dosing, administration, side effects). Use when the user asks about cancer treatment management, perioperative/adjuvant/systemic therapy pathways, bladder preservation, hydronephrosis, inoperable disease, or wants visit-ready counseling language. Always pair with medical-evidence-search for PubMed verification first.
---

# Onc Visit

Produce **visit-ready oncology management reports** for clinician counseling. Evidence retrieval and verification remain in [medical-evidence-search](../medical-evidence-search/SKILL.md); this skill governs **structure, decision logic, and patient-facing regimen detail**.

## When to use

Apply **after** PubMed/guideline evidence is gathered (or in parallel):

- Locally advanced / muscle-invasive / metastatic cancer management questions
- Perioperative, bladder-preservation, or inoperable pathways
- Any scenario where an algorithm was discussed — **every algorithm branch must appear in the written report**
- User wants dosing, administration route, or side-effect counseling language

## Workflow

1. **Run medical-evidence-search first** — no regimen detail without verified source (trial, label, or guideline summary in PubMed).
2. **Classify the clinical scenario** using [mibc-pathways.md](mibc-pathways.md) (or indication-specific pathway file if added later).
3. **Draft the report** using [report-template.md](report-template.md).
4. **Append counseling regimens** for every regimen recommended or discussed as an alternative — use [regimen-counseling.md](regimen-counseling.md).
5. **Self-check** against the checklist below before sending.

## Mandatory report sections (in order)

Do not skip sections because they were shown in a diagram elsewhere. **If it is in the algorithm, it must be in the prose.**

1. **Clinical framing** — stage, resectability, M0 vs M1, key adverse prognostic features (e.g., hydronephrosis unilateral vs bilateral).
2. **What the prognostic feature implies** — cite verified outcomes (HR/OR) when available.
3. **Immediate / pre-definitive steps** — e.g., relieve obstruction (ureteric stent vs PCN), restage after drainage, reassess cisplatin eligibility (GFR, hearing, neuropathy, PS). Include PCN-related NAC delivery caveats when sourced.
4. **Preferred pathway** — full sequence (neoadjuvant → local → adjuvant), not drug shorthand alone.
5. **Alternative pathways** — RC-ineligible, declined RC, trial options; label evidence strength.
6. **What NOT to do** — e.g., perioperative ICI trials that require RC when patient is inoperable; TMT when consensus lists contraindications.
7. **Surveillance / salvage** — follow-up intensity; salvage cystectomy or second-line triggers when applicable.
8. **Summary decision table** — patient profile | preferred approach | rationale | evidence.
9. **Patient counseling: treatment regimens discussed** — **always last section** (see below).

## Algorithm fidelity rule

When you provide a mermaid or flowchart:

- Every node must have a corresponding paragraph or table row in the report.
- **Pre-treatment nodes are mandatory**, including:
  - Obstruction relief (stent/PCN)
  - Restaging after drainage
  - Cisplatin / carboplatin eligibility reassessment
  - MDT review
- Branch labels in the figure must match branch headers in the text (e.g., "RC feasible" vs "RC unfit").

## Patient counseling section (required footer)

End every onc-visit report with:

```markdown
## Patient counseling: treatment regimens discussed

*(For shared decision-making; verify against current label and institutional protocol.)*

### [Regimen name — e.g., NIAGARA perioperative pathway]
- **What it is:** …
- **Schedule / dosing:** … (only from verified sources)
- **How it is given:** route, infusion setting, cycle length, duration
- **Expected benefits:** trial outcomes in plain language
- **Common side effects:** …
- **Serious risks / monitoring:** …
- **Practical considerations:** fertility, hydration, premeds, when to call
- **Evidence:** Author Year (Journal) PMID …
```

Include **every regimen** mentioned as recommended or reasonable alternative. Omit regimens only discussed as historical or not applicable.

Field rules — see [regimen-counseling.md](regimen-counseling.md):

- **Dosing:** use published trial or label doses; if not in retrieved text, state "dose not verified in retrieved sources."
- **Side effects:** grade ≥3 rates from trial when available; otherwise common AEs explicitly listed in source.
- **Administration:** IV vs oral, inpatient vs outpatient, typical visit frequency.
- **Do not invent** supportive care details not in sources.

## MIBC-specific checkpoints

For muscle-invasive bladder cancer, cross-check [mibc-pathways.md](mibc-pathways.md):

| Scenario | Preferred pathway | TMT / bladder preservation |
|----------|-------------------|----------------------------|
| Resectable, cisplatin-fit | Perioperative GC ± durvalumab or EV+pembro → RC | Only if favorable selection (no hydronephrosis, unifocal cT2, etc.) |
| M0 + hydronephrosis | Drain → restage → RC-anchored multimodal if operable | **Not preferred** (consensus); high-risk if used |
| Inoperable M0 | Definitive chemoRT or NAC→CRT if fit; not perioperative ICI→RC | Suboptimal candidate |
| Unresectable / M1 | EV+pembro or platinum/IO per eligibility | Not curative intent |

Hydronephrosis counseling must mention **worse prognosis independent of modality** and **bilateral worse than unilateral** when sourced.

## Quality checklist

Before sending:

- [ ] medical-evidence-search workflow completed; PMIDs on key claims
- [ ] Every algorithm branch is written out (not diagram-only)
- [ ] Pre-definitive steps included when obstruction, renal function, or staging uncertainty present
- [ ] Full regimen sequences in management section (not "durvalumab" alone)
- [ ] **Patient counseling** footer lists all discussed regimens with dosing, route, side effects
- [ ] Dosing/AEs traceable to retrieved text or labeled unverified
- [ ] Cross-trial comparisons labeled indirect where applicable

## Additional resources

- Report skeleton: [report-template.md](report-template.md)
- Counseling fields and MIBC regimen anchors: [regimen-counseling.md](regimen-counseling.md)
- MIBC decision branches (hydronephrosis, inoperable, advanced): [mibc-pathways.md](mibc-pathways.md)
- Trial landscape tables: [../medical-evidence-search/oncology-landscape-tables.md](../medical-evidence-search/oncology-landscape-tables.md)
