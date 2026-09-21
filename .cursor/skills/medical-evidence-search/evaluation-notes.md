# PaperQA2 Companion Pilot Evaluation

Date: 2026-05-24

## Scope

Quick benchmark comparing baseline `medical-evidence-search` versus hybrid workflow (`medical-evidence-search` + optional `paperqa2-medical` retrieval assist) on 10 representative oncology/epigenetic queries.

## Method

- For each query, captured top PubMed hit (`pubmed_search_articles`, maxResults=1).
- Baseline proxy metrics:
  - citation completeness (PMID/DOI present in top hit)
  - quote-verifiability proxy (top hit has retrievable full text via PMCID/PMC route)
- Hybrid proxy metrics:
  - same metrics after full-text chain attempt (`pubmed_fetch_fulltext` on collected PMIDs)
  - this chain includes PMC and fallback tiers available in current environment
- Notes:
  - This is a retrieval/verifiability pilot, not a treatment-effectiveness benchmark.
  - Unsupported-claim rate is estimated as a proxy from full-text availability (not direct hallucination scoring).

## Queries

1. small cell lung cancer azacitidine venetoclax
2. acute myeloid leukemia hypomethylating agent venetoclax resistance epigenetic
3. myelodysplastic syndrome decitabine venetoclax trial
4. tazemetostat combination lymphoma trial
5. DNMT inhibitor immune checkpoint lung cancer
6. BET inhibitor combination acute leukemia clinical trial
7. EZH2 inhibitor solid tumor combination trial
8. HDAC inhibitor immunotherapy non-small cell lung cancer
9. cell-free DNA methylation acute myeloid leukemia minimal residual disease
10. RCAN1 small cell lung cancer

## Results

- PubMed retrieval success (>=1 result): 9/10 queries
- Citation completeness among retrieved top hits:
  - PMID present: 9/9
  - DOI present: 9/9
- Baseline quote-verifiability proxy (full text retrievable via PMC path): 7/9 (77.8%)
- Hybrid quote-verifiability proxy (full-text chain in current environment): 7/9 (77.8%)
- Full-text unavailable for 2 PMIDs (33035459, 28631570) due no PMC counterpart + Europe PMC miss; Unpaywall fallback unavailable because `UNPAYWALL_EMAIL` is not configured

## Quality/Verifiability Interpretation

- Unsupported-claim risk proxy (no full text available): baseline 2/9 (22.2%), hybrid 2/9 (22.2%)
- In this pilot environment, hybrid did not increase unsupported-claim risk.
- Hybrid also did not improve full-text coverage yet; expected gains likely depend on enabling additional full-text sources and actual PaperQA2 runtime integration.

## Time-to-Answer Observation

- Hybrid adds one retrieval stage and is slower per query batch.
- Added latency is acceptable only when queries meet explicit trigger criteria in `paperqa2-medical`.

## Recommendation

Conditional GO for companion deployment:

- GO for opt-in use under defined trigger criteria and strict verification guardrails.
- Keep baseline as default.
- Priority next steps to unlock incremental value:
  1. Enable additional full-text fallback coverage in environment configuration.
  2. Run a second benchmark (10-20 clinically curated questions) after PaperQA2 runtime is wired.
  3. Add direct unsupported-claim adjudication (manual reviewer labels) for final go/no-go.
