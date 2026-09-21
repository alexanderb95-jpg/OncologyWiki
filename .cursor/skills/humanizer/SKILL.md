---
name: humanizer
description: Detect and revise common AI-writing artifacts while preserving meaning and author intent. Use when polishing drafts, making writing sound natural, or preparing publication-ready prose. Defaults to publication pass.
---

# Humanizer

## Default Mode

Default to `publication` pass unless the user explicitly requests `light`.

## Modes

### publication (default)

Use for formal, publication-ready prose:
- tighten verbosity
- reduce mechanical cadence
- remove vague attribution
- keep claims precise and verifiable
- preserve technical meaning

### light (opt-in)

Use for minimal edits:
- preserve original voice and structure
- only fix obvious AI tells and awkward phrasing

## AI-Pattern Checks

Check and revise:
- overused em dashes and stacked asides
- repetitive sentence openings and rhythm
- triple-stacked adjective strings
- double-negative constructions
- vague attribution ("experts say", "studies show") without source context
- filler transitions and generic qualifiers

## Editing Workflow

1. Identify high-impact issues first.
2. Rewrite with the selected pass.
3. Return:
   - revised text
   - short change log (3-6 bullets)
4. If factual claims are uncertain, flag them instead of inventing support.

## Constraints

- Never change core meaning.
- Keep domain terminology intact.
- Avoid slang unless user requests it.
- Maintain professional tone in `publication` mode.

## Quick Prompt Triggers

Apply this skill when requests include:
- "humanize this"
- "make this less AI"
- "tighten this draft"
- "publication-ready rewrite"

## Additional Resources

- Examples: [examples.md](examples.md)
