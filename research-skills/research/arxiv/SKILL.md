---
name: arxiv
description: "Search arXiv papers by keyword, author, category, or ID."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Research, Arxiv, Papers, Academic, Science, API]
    related_skills: [ocr-and-documents]
---

# arXiv Research

Search and retrieve academic papers from arXiv via their free REST API. No API key, no dependencies — just curl.

## Quick Reference

| Action | Command |
|--------|---------|
| Search papers | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
| Get specific paper | `curl "https://export.arxiv.org/api/query?id_list=2402.03300"` |
| Read abstract (web) | `web_extract(urls=["https://arxiv.org/abs/2402.03300"])` |
| Read full paper (PDF) | `web_extract(urls=["https://arxiv.org/pdf/2402.03300"])` |

## Searching Papers

The API returns Atom XML. Parse with `grep`/`sed` or pipe through `python3` for clean output.

### Basic search

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5"
```

### Clean output (parse XML to readable format)

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=submittedDate&sortOrder=descending" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for i, entry in enumerate(root.findall('a:entry', ns)):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    published = entry.find('a:published', ns).text[:10]
    authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    summary = entry.find('a:summary', ns).text.strip()[:200]
    cats = ', '.join(c.get('term') for c in entry.findall('a:category', ns))
    print(f'{i+1}. [{arxiv_id}] {title}')
    print(f'   Authors: {authors}')
    print(f'   Published: {published} | Categories: {cats}')
    print(f'   Abstract: {summary}...')
    print(f'   PDF: https://arxiv.org/pdf/{arxiv_id}')
    print()
"
```

## Search Query Syntax

| Prefix | Searches | Example |
|--------|----------|---------|
| `all:` | All fields | `all:transformer+attention` |
| `ti:` | Title | `ti:large+language+models` |
| `au:` | Author | `au:vaswani` |
| `abs:` | Abstract | `abs:reinforcement+learning` |
| `cat:` | Category | `cat:cs.AI` |
| `co:` | Comment | `co:accepted+NeurIPS` |

### Boolean operators

```
# AND (default when using +)
search_query=all:transformer+attention

# OR
search_query=all:GPT+OR+all:BERT

# AND NOT
search_query=all:language+model+ANDNOT+all:vision

# Exact phrase
search_query=ti:"chain+of+thought"

# Combined
search_query=au:hinton+AND+cat:cs.LG
```

## Sort and Pagination

| Parameter | Options |
|-----------|---------|
| `sortBy` | `relevance`, `lastUpdatedDate`, `submittedDate` |
| `sortOrder` | `ascending`, `descending` |
| `start` | Result offset (0-based) |
| `max_results` | Number of results (default 10, max 30000) |

```bash
# Latest 10 papers in cs.AI
curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10"
```

## Fetching Specific Papers

```bash
# By arXiv ID
curl -s "https://export.arxiv.org/api/query?id_list=2402.03300"

# Multiple papers
curl -s "https://export.arxiv.org/api/query?id_list=2402.03300,2401.12345,2403.00001"
```

## BibTeX Generation

After fetching metadata for a paper, generate a BibTeX entry:

{% raw %}
```bash
curl -s "https://export.arxiv.org/api/query?id_list=1706.03762" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
root = ET.parse(sys.stdin).getroot()
entry = root.find('a:entry', ns)
if entry is None: sys.exit('Paper not found')
title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
authors = ' and '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
year = entry.find('a:published', ns).text[:4]
raw_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
cat = entry.find('arxiv:primary_category', ns)
primary = cat.get('term') if cat is not None else 'cs.LG'
last_name = entry.find('a:author', ns).find('a:name', ns).text.split()[-1]
print(f'@article{{{last_name}{year}_{raw_id.replace(\".\", \"\")},')
print(f'  title     = {{{title}}},')
print(f'  author    = {{{authors}}},')
print(f'  year      = {{{year}}},')
print(f'  eprint    = {{{raw_id}}},')
print(f'  archivePrefix = {{arXiv}},')
print(f'  primaryClass  = {{{primary}}},')
print(f'  url       = {{https://arxiv.org/abs/{raw_id}}}')
print('}')
"
```
{% endraw %}

## Reading Paper Content

After finding a paper, read it:

```
# Abstract page (fast, metadata + abstract)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper (PDF → markdown via Firecrawl)
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
```

For local PDF processing, see the `ocr-and-documents` skill.

## Non-arXiv Journal Access

When a paper is not on arXiv, use Semantic Scholar search first (returns JSON, handles natural-language queries), then follow the journal-specific access pattern:

### Search cascade (fastest to most specific)
```bash
# 1. Semantic Scholar by title (finds DOI, journal, authors even for paywalled papers)
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TITLE&limit=5&fields=title,authors,year,citationCount,externalIds,isOpenAccess"

# 2. Crossref by DOI (license, funders, reference count)
curl -s "https://api.crossref.org/works/DOI" | python3 -m json.tool

# 3. PubMed E-utilities (abstract XML, author affiliations)
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID&rettype=abstract&retmode=xml"

# 4. PMC ID converter (check for open-access PMC version)
curl -s "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=PMID&format=json"
```

### Elsevier / The Lancet / ScienceDirect

Lancet.com uses aggressive Cloudflare bot detection — use the browser tool (browser_navigate) instead of curl for accessing article pages. ScienceDirect is more permissive and can be read via browser.

**Supplementary material download**: Elsevier CDN hosts supplements at a predictable URL pattern regardless of subscription status:
```bash
# Replace hyphens with dots in PII: S2589-7500(26)00005-1 → S2589750026000051
# Pattern: https://ars.els-cdn.com/content/image/1-s2.0-{PII_DOTTED}-mmc1.pdf
curl -sL -o supplement.pdf "https://ars.els-cdn.com/content/image/1-s2.0-S2589750026000051-mmc1.pdf"
```
Main PDFs require institutional authentication (403 without subscription). For CC-BY papers without institutional access, extract full text from the ScienceDirect HTML page via `browser_console` with `document.body.innerText`.

**PII conversion**: `S2589-7500(26)00005-1` → replace all hyphens with dots → `S2589750026000051`.

### PDF text extraction

Install pymupdf for reliable PDF text extraction (handles multi-column, Unicode):
```bash
pip install --break-system-packages pymupdf  # one-time
python3 -c "
import fitz
doc = fitz.open('file.pdf')
for page in doc:
    print(page.get_text())
"
```

### Code/prompt availability check

For papers asking about code/data availability:
1. Read the article's "Data sharing" or "Data availability" statement (bottom of article)
2. Search GitHub for the paper title or author names
3. Check supplementary materials for prompt templates, code snippets, or repository links
4. Comment-type articles in clinical journals rarely have code repositories — prompts are more likely in supplementary appendices

## Common Categories

| Category | Field |
|----------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.LG` | Machine Learning |
| `cs.CR` | Cryptography and Security |
| `stat.ML` | Machine Learning (Statistics) |
| `math.OC` | Optimization and Control |
| `physics.comp-ph` | Computational Physics |

Full list: https://arxiv.org/category_taxonomy

## Helper Script

The `scripts/search_arxiv.py` script handles XML parsing and provides clean output:

```bash
python scripts/search_arxiv.py "GRPO reinforcement learning"
python scripts/search_arxiv.py "transformer attention" --max 10 --sort date
python scripts/search_arxiv.py --author "Yann LeCun" --max 5
python scripts/search_arxiv.py --category cs.AI --sort date
python scripts/search_arxiv.py --id 2402.03300
python scripts/search_arxiv.py --id 2402.03300,2401.12345
```

No dependencies — uses only Python stdlib.

---

## Semantic Scholar (Citations, Related Papers, Author Profiles)

arXiv doesn't provide citation data or recommendations. Use the **Semantic Scholar API** for that — free, no key needed for basic use (1 req/sec), returns JSON.

### Get paper details + citations

```bash
# By arXiv ID
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=title,authors,citationCount,referenceCount,influentialCitationCount,year,abstract" | python3 -m json.tool

# By Semantic Scholar paper ID or DOI
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example?fields=title,citationCount"
```

### Get citations OF a paper (who cited it)

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool
```

### Get references FROM a paper (what it cites)

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool
```

### Search papers (alternative to arXiv search, returns JSON)

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=GRPO+reinforcement+learning&limit=5&fields=title,authors,year,citationCount,externalIds" | python3 -m json.tool
```

### Get paper recommendations

```bash
curl -s -X POST "https://api.semanticscholar.org/recommendations/v1/papers/" \
  -H "Content-Type: application/json" \
  -d '{"positivePaperIds": ["arXiv:2402.03300"], "negativePaperIds": []}' | python3 -m json.tool
```

### Author profile

```bash
# Search for an author by name
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&fields=name,hIndex,citationCount,paperCount,affiliations" | python3 -m json.tool
```

### List an author's papers (by author ID)

After finding an author's ID from the search above, get their full publication list:

```bash
curl -s "https://api.semanticscholar.org/graph/v1/author/2844182/papers?limit=25&fields=title,year,venue,citationCount,externalIds,abstract" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data['data']:
    title = p.get('title','?')
    year = p.get('year','?')
    cites = p.get('citationCount',0)
    venue = p.get('venue','?')
    doi = p.get('externalIds',{}).get('DOI','')
    print(f'[{year}] {title}  (cited {cites})')
    print(f'       Venue: {venue}  DOI: {doi}')
    print()
"
```

**Common pitfalls when searching authors:**

- **Same-name disambiguation**: Search returns multiple authors with the same name. Compare `paperCount`, `hIndex`, `affiliations`, and co-author networks to identify the right one. Check paper titles to confirm field alignment.
- **Chinese/Korean/Japanese names**: arXiv's API (`au:`) often fails on CJK characters. Use Semantic Scholar instead. Try multiple romanizations: "Xuxu Wei", "Wei Xuxu", and the original characters.
- **Chinese-language publications are invisible to Western APIs**: Semantic Scholar, PubMed, and arXiv systematically miss papers published in Chinese domestic journals (CNKI/知网, Wanfang/万方). When profiling a Chinese author, your portrait will be incomplete. See `references/chinese-language-research.md` for known gaps, environment constraints, and workarounds.
- **When the user corrects you about missing Chinese papers**: stop searching and ask the user directly. They know their own publication list. Don't re-search — the databases are not accessible from this environment.
- **Institutional signal**: Authors with `affiliations: []` can be disambiguated by their consistent co-author network — look for recurring collaborator names across their papers.
- **Rate limit**: Semantic Scholar allows ~1 req/sec without API key. When you hit HTTP 429, sleep 1+ seconds before retrying. With an API key, 100 req/sec.

### Useful Semantic Scholar fields

`title`, `authors`, `year`, `abstract`, `citationCount`, `referenceCount`, `influentialCitationCount`, `isOpenAccess`, `openAccessPdf`, `fieldsOfStudy`, `publicationVenue`, `externalIds` (contains arXiv ID, DOI, etc.)

**Paper fields for author endpoint**: `title`, `year`, `venue`, `citationCount`, `externalIds`, `abstract`, `authors`, `openAccessPdf`, `publicationTypes`

---

## Complete Research Workflow

1. **Discover**: `python scripts/search_arxiv.py "your topic" --sort date --max 10`
2. **Assess impact**: `curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=citationCount,influentialCitationCount"`
3. **Read abstract**: `web_extract(urls=["https://arxiv.org/abs/ID"])`
4. **Read full paper**: `web_extract(urls=["https://arxiv.org/pdf/ID"])`
5. **Find related work**: `curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID/references?fields=title,citationCount&limit=20"`
6. **Get recommendations**: POST to Semantic Scholar recommendations endpoint
7. **Track authors**: Search author → list their papers → identify their research focus
   - `curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=NAME&fields=name,hIndex,paperCount"`
   - Then: `curl -s "https://api.semanticscholar.org/graph/v1/author/ID/papers?limit=50&fields=title,year,citationCount,abstract"`
   - Disambiguate same-name authors by co-author network and paper topics
8. **Check for Chinese-language gap**: If the author is Chinese, Semantic Scholar likely misses their domestic Chinese journals. Read `references/chinese-language-research.md` before presenting your analysis — and caveat accordingly.

## Rate Limits

| API | Rate | Auth |
|-----|------|------|
| arXiv | ~1 req / 3 seconds | None needed |
| Semantic Scholar | 1 req / second | None (100/sec with API key) |

## Notes

- arXiv returns Atom XML — use the helper script or parsing snippet for clean output
- Semantic Scholar returns JSON — pipe through `python3 -m json.tool` for readability
- arXiv IDs: old format (`hep-th/0601001`) vs new (`2402.03300`)
- PDF: `https://arxiv.org/pdf/{id}` — Abstract: `https://arxiv.org/abs/{id}`
- HTML (when available): `https://arxiv.org/html/{id}`
- For local PDF processing, see the `ocr-and-documents` skill

## ID Versioning

- `arxiv.org/abs/1706.03762` always resolves to the **latest** version
- `arxiv.org/abs/1706.03762v1` points to a **specific** immutable version
- When generating citations, preserve the version suffix you actually read to prevent citation drift (a later version may substantially change content)
- The API `<id>` field returns the versioned URL (e.g., `http://arxiv.org/abs/1706.03762v7`)

## Withdrawn Papers

Papers can be withdrawn after submission. When this happens:
- The `<summary>` field contains a withdrawal notice (look for "withdrawn" or "retracted")
- Metadata fields may be incomplete
- Always check the summary before treating a result as a valid paper
