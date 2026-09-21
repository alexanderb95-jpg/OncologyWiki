---
name: med-onc-research-synthesis
description: >-
  Expert-level medical oncology literature review and synthesis. Wraps
  medical-evidence-council with med-* agents, Canvas trial dashboard when useful,
  and explicit limitations/gaps/exploration sections. Use when med-onc triage routes
  to research_synthesis or user asks for research-grade evidence review.
---

# Med-Onc Research Synthesis

Deep, multi-reviewer literature synthesis for research work — manuscripts, grants, lab direction, and expert-level landscape mapping.

## When to use

- Triage routed to `research_synthesis`
- User asks for literature review, evidence council, synthesis with limitations
- User needs ongoing questions and areas for exploration identified

## Pipeline

```text
1. med-onc-triage → confirm research_synthesis
2. medical-evidence-council (full pipeline):
   a. Hypotheses dialog (default No)
   b. med-lead-scientist → source pack
   c. med-synthesizer → draft
   d. Parallel: med-scientific-reviewer, med-stats-reviewer, med-ui-reviewer
   e. Lead adjudication
   f. Pass B only if hypotheses Yes
3. Visual layer (when ≥2 trials or complex landscape):
   oncology-trial-dashboard Canvas OR evidence tables from council output
4. Research extensions section (this skill — always)
5. Optional KB append if user opted in
```

## Research extensions (always append after council package)

```markdown
## Ongoing questions
- … (each bullet cites gap in literature or unsettled endpoint)

## Areas for exploration
- … (testable next steps; label preclinical vs clinical feasibility)

## Methodological limitations across the field
- … (design heterogeneity, surrogate endpoints, immature OS, cross-trial comparison caveats)
```

## Visual output

| Deliverable | When |
|-------------|------|
| Canvas trial dashboard | ≥2 pivotal trials or user asks for dashboard |
| Comparative landscape table | Always when comparing interventions |
| Mermaid evidence map | Optional for mechanism or biomarker threads |

Canvas path: `canvases/<topic-slug>-research.canvas.tsx`.

## Hypotheses default

Default No on the council hypotheses dialog. Offer Yes only when the user explicitly wants integrative further-investigation proposals.

## Agents (user-global)

| Agent | Path |
|-------|------|
| Lead | `~/.cursor/agents/med-lead-scientist.md` |
| Synthesizer | `~/.cursor/agents/med-synthesizer.md` |
| Scientific | `~/.cursor/agents/med-scientific-reviewer.md` |
| Stats | `~/.cursor/agents/med-stats-reviewer.md` |
| UI | `~/.cursor/agents/med-ui-reviewer.md` |
| Hypothesizer | `~/.cursor/agents/med-hypothesizer.md` (opt-in only) |

## Invocation phrases

- "Med-onc research: [question]"
- "Research synthesis on [topic]"
- "Evidence council for [PICO question]"
- "Expert literature review: [topic] with limitations"

## Quality checklist

- [ ] Full council pipeline (synthesizer + three reviewers + adjudication)
- [ ] Research extensions section present
- [ ] No hallucinated PMIDs; abstract-only labeled
- [ ] No bold inside paragraph body text
- [ ] Hypotheses section only if user chose Yes
