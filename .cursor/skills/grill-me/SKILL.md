---
name: grill-me
description: Interrogate ideas before execution through structured clarification questions. Use when starting a project, defining requirements, writing a plan, or when the user wants deeper clarity before implementation.
---

# Grill Me

## Purpose

Improve task clarity before execution by asking focused, high-yield questions in short phases.

## Workflow

1. Ask questions in this order:
   - Objective: what outcome is required
   - Constraints: time, tools, scope, risks
   - Success criteria: how "done" is measured
   - Acceptance tests: concrete checks the result must pass
2. Keep each round concise (3-6 questions).
3. After each round, summarize assumptions and ask for correction.

## Stop Condition

Stop questioning when all are true:
- Objective is specific
- Constraints are clear enough to avoid rework
- Success criteria are testable
- At least one acceptance test is defined

Then provide a compact execution brief and proceed.

## Output Template

Use this structure when the stop condition is met:

```markdown
Execution Brief
- Goal:
- Constraints:
- Non-goals:
- Success criteria:
- Acceptance tests:
- Open risks:
```

## Guardrails

- Do not ask redundant questions.
- Prefer one sharp question over several vague ones.
- If user asks to proceed immediately, provide a short assumptions list and continue.
