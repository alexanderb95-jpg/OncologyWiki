---
name: med-onc-clinical-reference
description: >-
  OpenEvidence-like clinical reference for medical oncology — fast visit-ready
  answers with guidelines, trial data, and patient counseling. Uses
  medical-evidence-search + onc-visit; optional compact Canvas. Use for board
  study, clinic, tumor board prep, or when med-onc triage routes to clinical_reference.
---

# Med-Onc Clinical Reference

Visit-ready, high-fidelity clinical reference for an academic oncology fellow. Optimized for real-time use (clinic, board study, quick tumor board prep).

## When to use

- Triage routed to `clinical_reference`
- User asks for guidelines, SOC, counseling language, or trial landmarks for a scenario
- User wants OpenEvidence-like density — scannable tables first, prose second

## Pipeline (run in order)

```text
1. med-onc-triage (if not already run) → confirm clinical_reference
2. medical-evidence-search → PubMed/guideline retrieval + verification
3. onc-visit → report structure + patient counseling footer
4. Optional visual → compact Canvas OR markdown tables (see Visual output)
```

## Speed vs fidelity

| Priority | Behavior |
|----------|----------|
| Latency | Lead with a 3–5 line verdict + one summary table |
| Fidelity | No claim without PMID/guideline anchor; state abstract-only when applicable |
| Counseling | Full onc-visit footer for every regimen discussed |

## Mandatory output sections

1. One-line clinical answer (evidence only)
2. Guideline / trial anchor table (source | recommendation or outcome | citation)
3. Management pathway in prose (every algorithm branch — see onc-visit)
4. Comparative landscape table when comparing regimens (full intervention and control arms)
5. Patient counseling: treatment regimens discussed (onc-visit footer, always last)

## Visual output

Choose one based on complexity:

| Scenario | Output |
|----------|--------|
| Single pathway, 1–2 regimens | Markdown tables in chat (default) |
| Multi-regimen trial comparison | Compact Canvas using oncology-trial-dashboard patterns (StudyBlock, chips, NoKm when needed) — only if user wants Canvas |
| Decision algorithm | Mermaid flowchart + matching prose (every node in text) |

For Canvas: copy patterns from `oncology-trial-dashboard` template if available in workspace; otherwise use canvas SDK with compact chips. Canvas path: `canvases/<topic-slug>-clinical-ref.canvas.tsx`. Prefer the GU clinic HTML wiki for persistence (below).

## GU / MedOnc wiki (persistence)

Canonical store: `/Users/Alex/Projects/GU-clinic` (Projects sidebar; GU under `pathways/gu/`).

When the user says `save to knowledge base` / `KB yes` for a clinical topic:

1. Update `pathways/{domain}/{disease}/{setting}/evidence.md` (and `dotphrase.md` if counseling text changed). GU domain = `gu`.
2. Bump Last reviewed, Next review (~90 days), Changelog.
3. Run `python3 scripts/build_wiki.py` in GU-clinic.
4. Point them to `site/index.html` (or `site/gu/{disease}/{setting}.html`).

Open phrases: `Open MedOnc wiki`, `Open GU clinic wiki`, `Open med-onc KB`, `Review stale KB` → open/regenerate `site/index.html` in GU-clinic.

Do **not** write OneNote paste blocks, append to `~/.cursor/med-onc-kb`, or edit `/Users/Alex/Projects/MedOnc-wiki` (pointer only).

## Invocation phrases

- "Med-onc clinical: [question]"
- "Clinical reference for [indication/scenario]"
- "Visit-ready: [question]"
- "Board study quick ref: [topic]"
- "Open MedOnc wiki" / "Open GU clinic wiki" / "Open med-onc KB"

## Quality checklist

- [ ] medical-evidence-search completed; contemporary SOC trials searched by name when relevant
- [ ] onc-visit structure and counseling footer present
- [ ] No bold inside paragraph body text
- [ ] Limitations stated (abstract-only, indirect comparisons, guideline version/date)
- [ ] KB append only if user opted in; wiki rebuilt after GU saves
