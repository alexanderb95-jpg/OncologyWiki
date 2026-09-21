---
name: medical-evidence-council
description: >-
  Multi-role medical evidence council for independent literature questions (not
  StemAI workflows). Runs lead retrieval, synthesizer draft, and parallel
  scientific/stats/UI review, then lead adjudication. Hypotheses are opt-in via
  a clickable Yes/No dialog (default No). Use when the user asks for medical
  evidence council, multi-reviewer evidence search, evidence council,
  multi-agent medical literature review, to review medical or clinical
  evidence, to review a literature package, or names med-lead-scientist,
  med-synthesizer, med-scientific-reviewer, med-stats-reviewer,
  med-ui-reviewer, or med-hypothesizer.
---

# Medical Evidence Council

Independent of StemAI knit/render pipelines. Builds on `medical-evidence-search` for PubMed fidelity. Coordinates user-level agents in `~/.cursor/agents/med-*.md`.

## When to use

- User says “medical evidence council”, “evidence council”, “multi-reviewer evidence”, or similar
- User wants higher-fidelity medical literature synthesis than a single pass
- Do **not** use for ordinary one-shot medical questions unless they ask for the council — prefer `medical-evidence-search` alone

## Agents

| Agent | File | Role |
|-------|------|------|
| Lead scientist | `med-lead-scientist` | Retrieve source pack; adjudicate; own final package |
| Synthesizer | `med-synthesizer` | Coherent draft from source pack only |
| Scientific reviewer | `med-scientific-reviewer` | Claim–source audit |
| Stats reviewer | `med-stats-reviewer` | Design / N / endpoints / both-arm outcomes |
| UI reviewer | `med-ui-reviewer` | MD-facing presentation |
| Hypothesizer | `med-hypothesizer` | Pass A / Pass B **only if user chose Yes** |

## Mandatory first step — hypotheses dialog (default No)

Before retrieval, show a **clickable** choice (Cursor dialog / `cursor_dialog` questions UI — not buried in prose):

- Prompt: `Include hypothesis generation (search-shaping + integrative further-investigation proposals)?`
- Options: **No** (default) | **Yes**

| Choice | Behavior |
|--------|----------|
| **No** (default) | Skip hypothesizer entirely (no Pass A, no Pass B). Final package = verdict + evidence + limitations + adjudication. Do not mention residual hypotheses. |
| **Yes** | Run Pass A before retrieval; Pass B after adjudication; Pass B only under **Further investigation**. |

If the dialog cannot be shown, treat as **No** and state that briefly. Never silently run the hypothesizer.

Record `hypotheses_opt_in: true|false` for the rest of the run.

## Pipeline

```text
1. Clarify PICO-style question (one short ask if ambiguous)
2. Hypotheses dialog (default No) → record choice
3. If Yes: Hypothesizer Pass A → competing framings + PubMed search strings
4. Lead retrieves with medical-evidence-search → source pack
5. Synthesizer drafts narrative + tables from source pack only
6. Parallel reviews: Scientific + Stats + UI
7. Lead adjudicates final evidence package
8. If Yes only: Hypothesizer Pass B → Scientific short re-check of Pass B
               → append Further investigation
9. If No: stop after step 7
```

### Parallel reviews (step 6)

Launch three `Task` subagents (`subagent_type: generalPurpose`) in parallel, each given:

- The clinical question
- The source pack
- The synthesizer draft
- The matching role prompt from `~/.cursor/agents/med-scientific-reviewer.md`, `med-stats-reviewer.md`, or `med-ui-reviewer.md`

If Task is unavailable, run the three reviewer checklists yourself in sequence using those agent files as system prompts — still do not skip any reviewer role.

### Lead vs synthesizer

- Lead = retrieval, pipeline control, adjudication, final wording ownership
- Synthesizer = first coherent draft only; no new PMIDs outside the pack
- Never skip the synthesizer step

## Final user-facing shape

Always:

1. Short verdict (evidence only)
2. Evidence table(s)
3. Limitations and gaps
4. Brief adjudication log (kept / downgraded / removed)

Only if `hypotheses_opt_in` is Yes:

5. **Further investigation** — ranked integrative hypotheses from Pass B (clearly labeled; never mixed into verdict)

## Fidelity gates (non-negotiable)

- Apply `medical-evidence-search` for retrieval and claim verification
- No hallucinated PMIDs or findings
- No bold inside paragraph body text
- Quantify or qualify; distinguish preclinical vs clinical; abstract-only vs full-text
- Contemporary oncology management: named-trial PubMed search before SOC claims
- Pass B items are hypotheses for further investigation, not conclusions

## @-invoke without full council

User may invoke a single role (e.g. `@med-synthesizer`, `@med-scientific-reviewer`, `@med-hypothesizer`) on an existing draft. In that case:

- Do not force the full pipeline
- For `@med-hypothesizer` alone, ask Pass A vs Pass B if unclear
- Do not invent a “Further investigation” section after a No council run unless the user newly opts in or @-invokes the hypothesizer

## Out of scope

- StemAI Rmd/HTML knit workflows
- Wet-lab or clinical validation claims beyond what sources state
- Always-on hypothesizer (default is No)
