# PubMed Search Strategies

## Effective Search Patterns

### Basic Structure
```
[condition/disease] AND [intervention/treatment] AND [outcome]
```

### Advanced Patterns

**For systematic reviews:**
```
[condition] AND [intervention] AND (systematic review[Title/Abstract] OR meta-analysis[Title/Abstract])
```

**For recent high-impact studies:**
```
[condition] AND [intervention] AND ("New England Journal of Medicine"[Journal] OR "Lancet"[Journal] OR "JAMA"[Journal] OR "Nature Medicine"[Journal])
```

**For specific outcomes:**
```
[condition] AND [intervention] AND (survival[Title/Abstract] OR mortality[Title/Abstract] OR progression[Title/Abstract])
```

**For specific study types:**
```
[condition] AND [intervention] AND (randomized controlled trial[Publication Type] OR clinical trial[Publication Type])
```

## PubMed Filters

### Publication Date
- Last 5 years: `("2019"[Publication Date] : "2025"[Publication Date])`
- Last 3 years: `("2022"[Publication Date] : "2025"[Publication Date])`
- Last year: `("2024"[Publication Date] : "2025"[Publication Date])`

### Article Types
- Systematic reviews: `systematic review[Filter]`
- Meta-analyses: `meta-analysis[Filter]`
- Clinical trials: `clinical trial[Filter]`
- Randomized controlled trials: `randomized controlled trial[Filter]`

### Journal Categories
- Core clinical journals: `core clinical journals[Filter]`
- MEDLINE: `medline[Filter]`

## Combining Filters

Example comprehensive search:
```
(bladder cancer OR urothelial carcinoma) AND (ctDNA OR circulating tumor DNA) AND (survival OR prognosis) AND ("2019"[Publication Date] : "2025"[Publication Date]) AND (systematic review[Filter] OR meta-analysis[Filter])
```

## MeSH Terms

Use Medical Subject Headings (MeSH) for more precise searches:
- `"Urinary Bladder Neoplasms"[MeSH Terms]`
- `"Circulating Tumor DNA"[MeSH Terms]`
- `"Survival Analysis"[MeSH Terms]`

## Search Tips

1. **Start broad, then narrow** - Begin with general terms, then add filters
2. **Use quotes for exact phrases** - `"circulating tumor DNA"` vs `circulating tumor DNA`
3. **Use Boolean operators** - AND, OR, NOT
4. **Check related articles** - Use PubMed's "Similar articles" feature
5. **Review citations** - Check "Cited by" for more recent work
6. **Use Clinical Queries** - PubMed's specialized search filters for clinical questions

## Named-trial searches (contemporary oncology)

For standard-of-care or trial-landscape questions, search trial acronyms directly (often faster than generic queries):

```text
EV-303 OR KEYNOTE-905 enfortumab vedotin pembrolizumab bladder
NIAGARA durvalumab muscle invasive bladder
CheckMate 274 nivolumab adjuvant urothelial
```

Sort by `pub_date`. Compare results against the comparative landscape checklist in [oncology-landscape-tables.md](oncology-landscape-tables.md).

## Verification Steps

After finding articles:
1. Check the abstract for relevance
2. Verify the journal impact factor
3. Check publication date
4. Review study design (RCT > cohort > case-control > case series)
5. Look for systematic reviews/meta-analyses on the same topic
6. Cross-reference with clinical guidelines if available
