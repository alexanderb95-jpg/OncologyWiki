# Med-Onc Handbook agent guide

This repository is the canonical source for Alex's personal Med-Onc Handbook. Edit clinical content in `pathways/{domain}/{disease}/{setting}/evidence.md` and the paired `dotphrase.md`. `site/` is generated output. The separate Site checkout is a deployment copy, not a second place to maintain handbook instructions. Read `docs/HANDBOOK.md` for the project map and workflow.

- Keep one page per disease setting. `inbox/` holds unreviewed material and is never promoted automatically.
- Follow `.cursor/rules/evidence-briefs.mdc`, `.cursor/rules/dot-phrases.mdc`, and `docs/EDITORIAL_PREFERENCES.md` for clinical content and presentation. Keep guideline references, sources, source-reported comparison tables, and paired counseling with the relevant chapter. Never invent trial statistics or present interpolated values as reported data.
- Verify clinical edits against primary sources, record the exact review scope, and update review dates and the changelog only for content actually reviewed. Presentation-only changes leave clinical review dates unchanged.
- Explicit handbook edit requests and Alex's **Implement edit** comments authorize the requested revision after source verification. Suggestions and drafts remain proposals.
- Before clinical publication, follow `docs/REVIEW_WORKFLOW.md`. Independent disease-and-indication specialist and journal-editor reviews must approve the final evidence, phrase, and audit hash. An author cannot approve their own work. Run `scripts/validate_reviews.py`; a failed gate holds publication.
- Independent reviewer subagents and bounded clinical authorship delegation are authorized under `docs/REVIEW_WORKFLOW.md`. Never fabricate reviewer identities or reuse approvals after the reviewed content changes.
- For cloud implementation and local reconciliation, follow `docs/CLOUD_IMPLEMENTATION.md`. Preserve `.openai/handbook-sync.json` and the existing private Site identity and audience.
- Before handbook authoring, retrieval, or review, read `docs/EDITORIAL_PREFERENCES.md` and apply `.cursor/skills/handbook-feedback/SKILL.md`. Track requested studies in `docs/RESEARCH_TASKS.md`.
- After source edits, run `python3 scripts/build_wiki.py`. Use `scripts/sync_handbook_site.py` to copy this repository's instructions, docs, and generated pages to the Site checkout.

The cloud checkout includes `.cursor/skills/`, `.cursor/rules/`, and `.cursor/hooks.json`. Keep its local instructions usable without laptop paths; `docs/HANDBOOK.md` and `docs/CLOUD_IMPLEMENTATION.md` describe the supported workflows.
