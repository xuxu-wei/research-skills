---
name: pubmed
description: "Use when searching PubMed for biomedical papers by keyword, author, journal, MeSH term, or PMID. Fetch metadata and abstracts via NCBI E-utilities REST API."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, pubmed, biomedical, papers, ncbi, entrez, medicine]
    related_skills: [arxiv]
---

# PubMed Search

Search and retrieve biomedical literature from PubMed via the NCBI E-utilities REST API. No API key, no dependencies — just curl.

## Quick Reference

| Action | Command |
|--------|---------|
| Search + fetch (pipeline) | `python3 scripts/search.py "Wei Xuxu[Author]" --max 5 \| python3 scripts/fetch.py` |
| Search by keyword | `python3 scripts/search.py "GRPO reinforcement learning" --max 10` |
| Search with date filter | `python3 scripts/search.py "LLM clinical" --mindate 2024/01/01 --max 20` |
| Fetch by PMID | `python3 scripts/fetch.py 42062541` |
| Search JSON output | `python3 scripts/search.py "cancer immunotherapy" --max 10 --json` |
| Raw curl (no scripts) | `curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=GRPO+reinforcement+learning&retmax=10"` |
| Rate limit | 3 req/sec without API key; 10 req/sec with key (`&api_key=YOUR_KEY`) |

## The Two-Step Flow

PubMed via E-utilities is a two-step process:

1. **esearch** → returns a list of PMIDs matching your query
2. **efetch** → takes PMIDs and returns full metadata (title, authors, abstract, journal, DOI, MeSH terms)

Do NOT skip esearch. Always search first, then fetch the top N results.

## Step 1: Search (esearch)

### Basic keyword search

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=immune+checkpoint+inhibitor+colorectal+cancer&retmax=20"
```

### Search field qualifiers

PubMed supports tagged search terms. Use `[Field]` suffixes:

| Qualifier | Searches | Example |
|-----------|----------|---------|
| `[Author]` | Author name | `Wei Xuxu[Author]` |
| `[Journal]` | Journal name | `Nature[Journal]` |
| `[Title]` | Title words | `reinforcement learning[Title]` |
| `[Title/Abstract]` | Title or abstract | `GRPO[Title/Abstract]` |
| `[MeSH Terms]` | MeSH subject headings | `Immunotherapy[MeSH Terms]` |
| `[All Fields]` | All fields (default) | `deep learning[All Fields]` |
| `[PMID]` | Specific PMID | `42062541[PMID]` |
| `[DOI]` | DOI string | `10.1038/s41746-026-02685-4[DOI]` |

### Compound queries

```bash
# Author + keyword
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Wei+Xuxu[Author]+AND+evidence-based+medicine[Title/Abstract]&retmax=20"

# Journal + date range
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Lancet[Journal]+AND+2024[pdat]&retmax=20"

# MeSH + keyword
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Diabetes+Mellitus[MeSH+Terms]+AND+metformin[Title/Abstract]&retmax=20"
```

### Boolean operators

```
# AND (default between terms separated by space or +)
term=cancer+AND+immunotherapy

# OR
term=cancer+OR+tumor

# NOT
term=cancer+NOT+lung
```

### Date filtering

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=LLM+clinical+decision&retmax=20&mindate=2024/01/01&maxdate=2025/12/31&datetype=pdat"
```

`datetype` options: `pdat` (publication date), `edat` (entrez date), `mdat` (modification date).

### Pagination

```bash
# Next page of results
curl -s "...&retstart=20&retmax=20"
```

### Parse esearch output to extract PMIDs

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=..." | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
count = root.find('Count').text
ids = [e.text for e in root.findall('.//Id')]
print(f'Total results: {count}')
print(f'PMIDs: {\", \".join(ids)}')
"
```

## Step 2: Fetch Details (efetch)

### Full XML (recommended for parsing)

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42062541&retmode=xml" | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
for article in root.findall('.//PubmedArticle'):
    pmid = article.find('.//PMID').text
    title = article.find('.//ArticleTitle').text or '(no title)'
    title = title.replace('\n', ' ').strip()
    
    # Authors
    authors = []
    for a in article.findall('.//Author'):
        ln = a.find('./LastName')
        fn = a.find('./ForeName')
        if ln is not None:
            authors.append(f\"{ln.text} {fn.text[:1] if fn is not None else ''}\")
    author_str = ', '.join(authors)
    
    # Journal info
    journal = article.find('.//Journal/Title')
    year = article.find('.//PubDate/Year')
    journal_str = f\"{journal.text} ({year.text})\" if journal is not None and year is not None else 'N/A'
    
    # DOI
    doi_el = article.find('.//ArticleId[@IdType=\"doi\"]')
    doi = doi_el.text if doi_el is not None else 'N/A'
    
    # Abstract
    abs_parts = article.findall('.//AbstractText')
    abstract = ' '.join(p.text or '' for p in abs_parts)[:500] if abs_parts else 'N/A'
    
    # MeSH terms
    mesh_terms = [m.find('DescriptorName').text for m in article.findall('.//MeshHeading') if m.find('DescriptorName') is not None]
    
    print(f'PMID: {pmid}')
    print(f'Title: {title}')
    print(f'Authors: {author_str}')
    print(f'Journal: {journal_str}')
    print(f'DOI: {doi}')
    print(f'Abstract: {abstract}...')
    if mesh_terms:
        print(f'MeSH: {\"; \".join(mesh_terms[:8])}')
    print('---')
"
```

### MEDLINE format (simpler, line-oriented)

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42062541&rettype=medline&retmode=text"
```

Key fields: `PMID`, `TI` (title), `AB` (abstract), `AU` (authors), `DP` (date), `JT` (journal), `LID` (DOI), `MH` (MeSH).

### Fetch by PMID list

Max 200 PMIDs per request. For larger result sets, batch in groups of 200:

```bash
# Batch of PMIDs from esearch
PMIDS="42062541,41808319,39559736"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${PMIDS}&retmode=xml"
```

## Search Patterns (Cheat Sheet)

```bash
# Find all papers by an author
term="LASTNAME+FIRSTINITIAL[Author]"   # e.g., "Wei+X[Author]"

# Papers citing a specific PMID (via pubmed central references — limited)
# Better: use PubMed ID in the term and check Related Articles

# Find recent reviews on a topic
term="topic[Title/Abstract]+AND+review[Publication+Type]&mindate=2024/01/01&maxdate=2025/12/31&datetype=pdat"

# Find clinical trials
term="topic[Title/Abstract]+AND+Clinical+Trial[Publication+Type]"

# Find papers with a specific DOI
term="10.1038/s41746-026-02685-4[DOI]"

# Find free full-text articles
term="topic[Title/Abstract]+AND+free+full+text[sb]"
```

## Script-Based Workflow

Use the bundled scripts for composable search → fetch pipelines:

```bash
# One-liner: search author, get top 5 formatted
python3 scripts/search.py "Wei Xuxu[Author]" --max 5 | python3 scripts/fetch.py

# JSON for further processing
python3 scripts/search.py "GRPO[Title/Abstract]" --max 10 --json | jq '.pmids[]' -r | python3 scripts/fetch.py --json

# Date-filtered search
python3 scripts/search.py "evidence-based medicine[Title] AND Chinese medicine[MeSH Terms]" \
  --mindate 2024/01/01 --maxdate 2025/12/31 --max 20 | python3 scripts/fetch.py
```

### Raw curl (when scripts aren't available)

```bash
# Search
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Wei+Xuxu[Author]&retmax=10" | \
  python3 -c "import sys,xml.etree.ElementTree as ET; root=ET.parse(sys.stdin).getroot(); print(','.join(e.text for e in root.findall('.//Id')))"

# Fetch (pipe PMIDs from above)
PMIDS="42062541,41808319"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${PMIDS}&retmode=xml"
```

## Common Pitfalls

1. **Searching without field qualifiers** returns broad matches. Use `[Author]`, `[Title/Abstract]`, or `[MeSH Terms]` to narrow scope.

2. **Fetching too many PMIDs at once.** efetch limit is 200 PMIDs. For esearch results >200, batch them.

3. **Ignoring rate limits.** Without an API key, limit is 3 req/sec. NCBI may throttle or temporarily block if you exceed this. Add `sleep 1` between batch requests.

4. **Using + instead of %20 in query strings.** Both work, but in shell scripts, `+` between terms is fine. For complex queries with parentheses or quotes, use `--data-urlencode` with curl.

5. **Author name format ambiguity.** PubMed indexes authors as `LastName FirstInitials`. Search with `Wei X[Author]` not `Xuxu Wei[Author]`. For Chinese names, try both `Wei Xuxu[Author]` and `Wei X[Author]` (Full Author Name vs Author index).

6. **Missing abstracts.** Some PubMed records (e.g., very new "ahead of print" articles) lack abstracts. Check for `AbstractText` existence before accessing `.text`.

7. **XML encoding issues.** PubMed XML may contain HTML entities, math markup, or Unicode symbols in abstracts. Always use an XML parser — never regex.

## Verification Checklist

- [ ] esearch returns expected PMIDs with correct count
- [ ] efetch returns full metadata for each PMID
- [ ] Author search uses correct field qualifier `[Author]`
- [ ] Rate limit respected (sleep between batch requests if needed)
- [ ] Abstract extraction handles missing/null abstracts gracefully
- [ ] DOI extraction uses `ArticleId[@IdType="doi"]` not hardcoded position
