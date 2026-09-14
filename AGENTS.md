# GU clinic — agent guide

This repo holds **Epic-style GU oncology dot phrases** plus **living evidence briefs** for quick clinic review.

## Structure

- `pathways/{disease}/{setting}/dotphrase.md` — note template; first line is the `#Trigger`
- `pathways/{disease}/{setting}/evidence.md` — UpToDate-like skim for that setting
- Keep phrase and evidence aligned when SOC changes

## Do

- Use `***` blanks in phrases for variable details
- Prefer counseling → decision → labs/NGS → procedures → meds → referrals → follow-up
- On evidence updates: never invent HRs/p-values; verify against NCCN / primary sources
- Bump `Last reviewed` and append `Changelog` on every evidence edit
- For methylation / EpiAI product skills, use sister project `/Users/Alex/Documents/EpiAI` — do not merge trees

## Do not

- Put PHI, MRNs, or secrets here
- Fabricate trial statistics
- Turn this into a second EpiAI HTML/product repo
