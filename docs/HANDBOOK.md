# Alex’s Med-Onc Handbook

This guide covers the personal handbook’s source, review, and publishing path. Website builds do not constitute a clinical review.

## Where things live

- Canonical handbook source: `/Users/Alex/Projects/GU-clinic/pathways/`
- Private Site checkout: `/Users/Alex/Projects/med-onc-handbook-site/`
- Maintain `AGENTS.md` and handbook docs in GU-clinic. The sync script copies them to the Site checkout for deployment.
- Local page: `site/index.html` · [Private website](https://alex-med-onc-handbook.airyshell9.chatgpt.site)
- Hosting identity: `.openai/hosting.json` in the Site checkout. Reuse that project and preserve its private audience.

## Before editing

Read `AGENTS.md`, `.cursor/rules/evidence-briefs.mdc`, `.cursor/rules/dot-phrases.mdc`, `docs/EDITORIAL_PREFERENCES.md`, and `.cursor/skills/handbook-feedback/SKILL.md`. Clinical changes require primary-source verification, a claim-to-source record, the actual review scope, and the paired `evidence.md` and `dotphrase.md` where relevant. Keep numbered citations and decision-relevant qualifications beside the claims. `site/` and `public/` are generated output.

Handbook edit requests and owner comments marked **Implement edit** authorize the requested revision after verification. Suggestions and drafts remain proposals until requested for implementation. For chapter structure and evidence details, use the rules above and `data/handbook-structure.json`. For independent specialist and editorial review, use `docs/REVIEW_WORKFLOW.md`. A clinical publication requires both approvals on the final content hash and a passing `scripts/validate_reviews.py` gate. Track research requests in `docs/RESEARCH_TASKS.md`.

## Build and publish

1. In GU-clinic, run `python3 -m unittest discover -s tests -v` and `python3 scripts/build_wiki.py`.
2. In GU-clinic, run `python3 scripts/sync_handbook_site.py /Users/Alex/Projects/med-onc-handbook-site`.
3. In the Site checkout, run `python3 scripts/build_handbook_site.py` and follow the installed Sites publishing workflow for the existing private project.
4. Confirm the deployment result and inspect the hosted page. A local build or queued panel open does not confirm a hosted update.

Before local edits following a cloud run, reconcile the current Site source with GU-clinic as described in `docs/CLOUD_IMPLEMENTATION.md`. Keep `.openai/handbook-sync.json` intact. That document also covers the cloud comment-implementation workflow. `docs/SCHEDULED_REVIEW.md` covers unattended evidence reviews.
