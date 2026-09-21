# Mandatory searches (every refresh)

Run in parallel via PubMed MCP. `sort: pub_date`. Date floor: 24 months before today, plus always re-fetch the landmark PMIDs in `ledger.json`.

## Named trials / landmarks

```
EV-302 KEYNOTE-A39 enfortumab pembrolizumab
EV-103 KEYNOTE-869 enfortumab pembrolizumab 5-year
enfortumab vedotin pembrolizumab (duration OR cycles) urothelial
enfortumab vedotin pembrolizumab (RDI OR "relative dose intensity" OR "dose intensity")
enfortumab vedotin pembrolizumab (discontinu* OR de-escalat* OR rechallenge) urothelial
UNITE enfortumab pembrolizumab (dose reduction OR "dose hold" OR "upfront")
```

## Congress (web + Europe PMC, not PubMed-only)

```
ASCO EV-302 3.5-year 4507
ASCO GU RDI-3 RDI-6 enfortumab pembrolizumab 689
UNITE enfortumab pembrolizumab dose 4565 696
```

## Secondary pointer (do not cite numbers from here alone)

```
https://www.guoncologynow.com/post/ev-p-demonstrates-sustained-efficacy-through-3-5-years-in-treatment-naive-la-muc
```

Use it only to locate the ASCO abstract. Numbers must match the abstract or the primary paper.

## Always re-fetch these PMIDs if still the current landmarks

- 38446675 — EV-302 NEJM 2024
- 42618453 — Li / Fox Chase EV discontinuation
- 42155320 — EV-103 5-year
- 42466532 — EV monotherapy TGI dose-modification model (context only; not EV+P)
