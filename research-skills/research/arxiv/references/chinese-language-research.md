# Chinese-Language Academic Research: Known Gaps & Workarounds

## The Problem

When profiling a Chinese researcher (e.g., 魏旭煦), the standard tools — Semantic Scholar, arXiv, PubMed, Google Scholar — **massively under-index Chinese-language publications** published in domestic journals (知网/CNKI, 万方, 维普).

This means:

- An author's Semantic Scholar profile may show 18 papers when they actually have 25+
- The missing papers are typically in Chinese-language journals (中医杂志, 中国中西医结合杂志, 中华中医药杂志, etc.)
- These papers may be first-author, core contributions that change the research portrait
- DOIs/PubMed IDs for Chinese journals are inconsistent — some have English abstracts, some don't

## Environment Constraints

From this Hermes Agent environment (Ubuntu server, likely behind GFW-style network restrictions):

| Source | Accessibility | Notes |
|--------|--------------|-------|
| Semantic Scholar API | ✅ Works (1 req/s) | Best starting point |
| arXiv API | ✅ Works (1 req/3s) | Limited to arXiv-hosted papers |
| PubMed | ✅ Works | Some overlap with Semantic Scholar |
| Google Scholar | ❌ Blocked/timed out | Route through Semantic Scholar instead |
| CNKI (知网) | ❌ Requires JS/cookies | curl returns 404; browser unavailable |
| Wanfang Data (万方) | ❌ Likely blocked | Similar restrictions |
| Baidu Scholar (百度学术) | ❌ Timed out / blocked | Requires China-based IP |
| Bing (cn.bing.com) | ⚠️ Partial | Returns captcha-limited pages |

## Workarounds

### 1. Ask the User Directly (Best Practice)

When the user corrects you about missing Chinese papers, **stop searching and ask**. They know their own publication list better than any database.

```
"你说得对，Semantic Scholar 对中文文献收录不全。
我这边无法直接访问知网/万方。
你能直接告诉我你的第一作者中文论文有哪些吗？
我补上后重新分析。"
```

### 2. Cross-Reference PubMed Central

Some Chinese journals are indexed in PubMed/PMC. Check:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Wei+Xuxu&retmax=20"
```

### 3. Look for DOI Links in Semantic Scholar Output

Some bilingual Chinese journals assign DOIs. If a paper has a DOI but no PubMed ID, check whether the DOI resolves to a Chinese journal (e.g., `10.53388/...`, `10.1007/s11655-...`).

### 4. When Presenting Results, Always Caveat

When describing a Chinese researcher's publication list based solely on Semantic Scholar:

> "这些是 Semantic Scholar 收录的英文/国际期刊论文。中文期刊论文（知网/万方等）未被收录，以下分析可能不完整。如果你能补充中文论文，我可以修正判断。"

## Key Takeaways

- **Always qualify scope**: state which databases you searched when profiling an author
- **Chinese authors likely have domestic publications** invisible to Western APIs
- **Don't over-interpret** an incomplete publication list as the full portrait
- **When corrected, don't re-search — just ask** the user to fill the gap
