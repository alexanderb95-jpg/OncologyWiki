---
name: medical-evidence-search
description: Retrieves high-fidelity medical evidence from peer-reviewed publications with source verification. Prioritizes PubMed sources, high impact factor journals, and recent articles. Use when answering medical questions, verifying clinical information, providing evidence-based recommendations, contemporary oncology management or trial-landscape questions, or when the user asks about medical literature, clinical guidelines, or research findings.
---

# Medical Evidence Search

## Core Principles

**Fidelity is paramount.** Always prioritize accuracy and verifiability over speed or convenience.

**CRITICAL: NO HALLUCINATION RULE**
- **Never invent, infer, or assume information not explicitly found in source text**
- **Only state what is directly verifiable from retrieved sources**
- **If information is not found in sources, explicitly state "Not found in available sources"**
- **Do not extrapolate beyond what the source text explicitly states**
- **When in doubt, acknowledge uncertainty rather than speculating**

1. **Source verification**: Every medical claim must be backed by peer-reviewed sources with verifiable text
2. **Text-based verification**: Only disclose information that can be directly quoted or verified from source text
3. **Impact prioritization**: Prefer high impact factor journals and professional society guidelines (see [journal-tiers.md](journal-tiers.md))
4. **Recency prioritization**: Prefer recent publications (last 5 years) unless older evidence is foundational
5. **Multiple sources**: When possible, cite multiple independent sources for key claims
6. **Transparent sourcing**: Always provide full citations with DOI/PMID when available

## Text Verification Requirements

**MANDATORY: All information must be verifiable in source text**

1. **Retrieve full text when possible**:
   - Use `mcp_web_fetch` to retrieve full article content
   - Read beyond abstracts when available
   - **For every PubMed article, always attempt to open the PMC full-text link first (if present) before relying on abstract-only data**
   - If direct PMC webpage fetch fails, attempt alternate NCBI routes (e.g., E-utilities `efetch` for `db=pmc`) before concluding full text is unavailable
   - If PMC/full text still cannot be retrieved, explicitly state that only abstract-level data were available

2. **Quote directly when making specific claims**:
   - For key findings, include direct quotes from source text
   - Use quotation marks for verbatim text
   - Cite the exact location (section, page, paragraph) when available

3. **Never infer beyond source text**:
   - If a study doesn't report a specific outcome, state "Not reported" not "No effect"
   - If methodology is unclear, state "Methodology not clearly described" not infer details
   - If numbers are missing, state "Data not provided" not estimate

4. **Verification process**:
   - Before stating any claim, verify it appears in the retrieved source text
   - If you cannot find the information in source text, explicitly state: "This information was not found in the available sources"
   - When multiple sources conflict, present all perspectives with citations

## Search Strategy

### Primary Sources (in order of preference)

1. **PubMed/PMC** - Always start here for peer-reviewed literature
2. **High impact journals** - NEJM, JAMA, Lancet, Nature Medicine, BMJ, etc.
3. **Specialty journals** - Domain-specific high-impact journals
4. **Clinical guidelines** - NCCN, professional society guidelines
5. **Regulatory sources** - FDA, CDC, WHO when relevant

### Search Approach

When searching for medical evidence:

1. **Use specific medical terminology** - Use MeSH terms, official drug names, ICD codes when relevant
2. **Combine search terms strategically**:
   - `[condition] AND [intervention] AND [outcome]`
   - Use PubMed filters: `[term] AND (systematic review[Title/Abstract] OR meta-analysis[Title/Abstract])`
3. **Apply filters in order of priority**:
   - Publication date: Last 5 years (unless foundational evidence needed)
   - Article type: Systematic reviews, meta-analyses, RCTs, then observational studies
   - Journal impact: Filter by high-impact journals when possible
4. **Verify findings** - Cross-check key claims with multiple sources

### Recency gate for contemporary oncology management

When the user asks for **current**, **contemporary**, or **standard-of-care** management (especially perioperative, adjuvant, or first-line systemic therapy):

1. Run **named-trial PubMed searches in parallel** before drafting (trial acronym + drug names + indication), sorted by `pub_date`
2. Do **not** answer from training data alone for fast-moving fields (e.g., perioperative MIBC, metastatic UC ADC+ICI)
3. If a pivotal trial was recently published or presented, it must appear in the comparative landscape table or the response must state it was searched and not found
4. Label evidence tier explicitly: **published primary journal** vs **reported (congress/review; primary publication pending)** vs **FDA/guideline only**

See [oncology-landscape-tables.md](oncology-landscape-tables.md) for MIBC perioperative checklist and search strings.

## Citation Format

Always provide citations in this format:

```
**Author et al. (Year).** Title. *Journal Name*. DOI: [doi] | PMID: [pmid]
```

**Example:**
```
**Powles et al. (2024).** ctDNA response assessment in metastatic urothelial carcinoma. *Nature Medicine*. DOI: 10.1038/s41591-024-03091-7 | PMID: [if available]
```

For multiple citations, list them in order of:
1. Impact factor (highest first)
2. Recency (most recent first)
3. Relevance to the specific question

## When to Use This Skill

Apply this skill when:
- User asks medical/clinical questions
- Verifying medical information
- Providing evidence-based recommendations
- Discussing treatment options or clinical guidelines
- Interpreting research findings
- Writing medical content that requires citations
- User mentions "evidence", "literature", "studies", "research", "publications"

## Optional Companion: Onc Visit (clinical management + counseling)

When the user asks for **oncology treatment management**, **clinical pathways**, **perioperative/adjuvant recommendations**, or **patient counseling** (dosing, administration, side effects), invoke [onc-visit](../onc-visit/SKILL.md) **after** evidence retrieval to format the answer.

Onc-visit requires:
- Every **algorithm branch** written in prose (including pre-definitive steps: obstruction relief, restaging, cisplatin reassessment)
- A final section **"Patient counseling: treatment regimens discussed"** with dosing, route, side effects for each regimen mentioned
- MIBC hydronephrosis / inoperable branches per [mibc-pathways.md](../onc-visit/mibc-pathways.md)

Do not skip onc-visit formatting because a diagram was already shown in chat.

## Optional Companion: PaperQA2 (Opt-In)

Use the companion skill [paperqa2-medical](../paperqa2-medical/SKILL.md) only when deeper full-text synthesis is needed.

Invoke the companion only if one or more are true:
- The question needs methods/results/discussion details not usually available in abstracts
- The answer requires synthesis across multiple full-text papers with claim-level traceability
- The task asks for contradiction mapping across studies
- Baseline PubMed/PMC workflow fails to retrieve enough full text for a high-priority question

- This is **optional** and should not replace the PubMed/PMC-first workflow
- Treat any PaperQA2 output as draft extraction that still requires source-text verification
- If direct verification is not possible, state that explicitly and do not present the claim as established fact
- If the companion skill is removed, continue with this skill's baseline workflow unchanged

## Workflow

1. **Identify the medical question** - Extract key terms (condition, intervention, outcome)
2. **Search PubMed first** - Use web_search with specific PubMed queries
3. **Retrieve and read source text** - Use mcp_web_fetch or read actual article content, not just abstracts
   - For PubMed-indexed papers, this step must include a PMC full-text attempt when a PMCID/PMC link exists
   - Optionally invoke [paperqa2-medical](../paperqa2-medical/SKILL.md) for deep full-text extraction across many papers, then verify every retained claim against retrievable source text
4. **Extract only explicit information** - Only state facts that are directly stated in the retrieved text
5. **Prioritize results**:
   - High impact journals first
   - Recent publications (last 5 years) first
   - Systematic reviews/meta-analyses over single studies
6. **Verify key claims** - Cross-reference with additional sources, ensuring each claim is in source text
7. **Format response**:
   - Lead with the answer/evidence (only if found in sources)
   - **When able, include summary tables** (see Summary Tables below)
   - Support with citations and direct quotes when possible
   - Note any limitations or conflicting evidence
   - Indicate strength of evidence (RCT vs observational, etc.)
   - **If information is not found, explicitly state this rather than inferring**
   - **For oncology management answers:** apply [onc-visit](../onc-visit/SKILL.md) report structure and counseling footer

## Summary Tables

**When the evidence allows**, present main points in markdown tables so key findings are easy to scan. Use tables when you have:
- Multiple studies or sources with comparable outcomes (e.g. study | design | main finding | citation)
- Guideline recommendations or criteria (e.g. recommendation | level/source | citation)
- Treatment/regimen options with evidence (e.g. intervention | outcome | source)
- Any structured comparison where rows and columns add clarity

**Rules for summary tables:**
- Include only information explicitly stated in retrieved source text
- Every cell that states a finding must be traceable to a cited source (citation column or footnote)
- Use clear column headers (e.g. Study, Design, Main finding, Citation)
- If data are not comparable or only one source applies, use a narrative summary instead of forcing a table
- Prefer one main summary table; add a second table only if it serves a distinct purpose (e.g. studies table + guidelines table)

### Comparative landscape tables (oncology trials)

When comparing trials or regimens for an indication, use a **comparative landscape** table — not a drug-name-only summary.

**Required columns:**

| Trial | Population | **Intervention arm** | **Control arm** | Key outcomes (both arms) | Key HR | Evidence status |

**Intervention arm / Control arm rules (mandatory):**
- Write the **full regimen sequence** (e.g., neoadjuvant drugs + cycles → surgery/RT → adjuvant drugs + cycles)
- Include doses or schedule when published in the source
- Never use bare drug labels ("durvalumab", "EVP", "GC") as the sole cell content
- Control arm must name the actual comparator regimen, not "SOC" or "placebo" without context

**Outcome columns:** Report values for **both arms** (e.g., `74.7% vs 39.4%`), not intervention-only.

**Evidence status column:** Published journal + PMID; or `reported, primary publication pending` with secondary source; FDA/EMA date only if verified.

Full template and MIBC perioperative canonical rows: [oncology-landscape-tables.md](oncology-landscape-tables.md).

### Investor slide tables (MD audience)

When the user wants a **brevity table for investors or slides** (not a full literature matrix), follow the user rule `medical-investor-evidence-tables.mdc`:

- **Columns:** Strategic lever | Opportunity | Evidence | Source
- **One row per lever**; slide-ready density (not one row per paper)
- **Sources:** `Author Year (Journal)` only in the table; 1–2 anchors per row
- **Evidence cell:** mechanism + payload + cancer type + setting; plain language; ADC-specific vs adjacent precedent labeled in prose
- Verify every claim via PubMed before inclusion; trim redundant citations

## Quality Checklist

Before providing medical information, verify:
- [ ] **All claims are directly verifiable from source text (not inferred or assumed)**
- [ ] **Source text has been read/retrieved, not just abstract or summary**
- [ ] All claims are backed by peer-reviewed sources with verifiable text
- [ ] Citations include journal name, year, and DOI/PMID
- [ ] **When multiple sources or structured findings exist, a summary table is included**
- [ ] **Comparative landscape tables include full Intervention arm and Control arm columns (not drug shorthand alone)**
- [ ] **Contemporary oncology answers: named phase 3 trials searched by pub_date before recommending standard of care**
- [ ] High-impact sources are prioritized
- [ ] Recent evidence is prioritized (unless foundational)
- [ ] Multiple sources cited for key claims when possible
- [ ] Limitations or conflicting evidence are noted
- [ ] Clinical context is appropriate (not overgeneralizing)
- [ ] **If information is missing, this is explicitly stated rather than inferred**
- [ ] **Oncology management: onc-visit applied; algorithm branches in prose; counseling regimens footer present**

## Limitations and Disclaimers

- **Never state information that cannot be verified in source text**
- Always note when evidence is limited or conflicting
- Distinguish between strong evidence (RCTs, meta-analyses) and weaker evidence (case reports, observational studies)
- Note when recommendations are based on guidelines vs. individual studies
- Acknowledge when information may be outdated or superseded
- **Explicitly state when information is not available rather than making assumptions**
- **If a source doesn't contain the requested information, say so clearly**

## Additional Resources

- For journal impact factor tiers, see [journal-tiers.md](journal-tiers.md)
- For PubMed search strategies, see [pubmed-strategies.md](pubmed-strategies.md)
- For oncology comparative landscape table format and MIBC perioperative trial checklist, see [oncology-landscape-tables.md](oncology-landscape-tables.md)
