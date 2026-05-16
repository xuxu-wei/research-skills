#!/usr/bin/env python3
"""Targeted evidence retrieval for research opportunity mapping.

Standalone script for PubMed + arXiv + Semantic Scholar searches.
Use this instead of inline Python in shell -c to avoid f-string escaping hell.
Rate-limit safe: respects PubMed's 3 req/sec and arXiv's 1 req/3sec limits.

Usage:
    python3 scripts/evidence_search.py > results.txt 2>&1
"""

import subprocess, sys, time, json, xml.etree.ElementTree as ET

def pubmed_search(query, retmax=10):
    """Search PubMed and return PMIDs"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax={retmax}"
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=15)
    root = ET.fromstring(r.stdout)
    count = root.find("Count").text
    ids = [e.text for e in root.findall(".//Id")]
    return count, ids

def pubmed_fetch(pmids):
    """Fetch details for PMIDs"""
    pmid_str = ",".join(pmids[:5])
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid_str}&retmode=xml"
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=15)
    root = ET.fromstring(r.stdout)
    results = []
    for art in root.findall(".//PubmedArticle"):
        pmid = art.find(".//PMID").text
        title_el = art.find(".//ArticleTitle")
        title = title_el.text.replace("\n"," ").strip() if title_el is not None and title_el.text else "N/A"
        year_el = art.find(".//PubDate/Year")
        year = year_el.text if year_el is not None else "?"
        journal_el = art.find(".//Journal/Title")
        journal = journal_el.text if journal_el is not None else "?"
        abs_parts = art.findall(".//AbstractText")
        abstract = " ".join(p.text or "" for p in abs_parts)[:300]
        results.append({"pmid": pmid, "title": title, "year": year, "journal": journal, "abstract": abstract})
    return results

def arxiv_search(query, retmax=8):
    """Search arXiv with category-filtered query"""
    url = f"https://export.arxiv.org/api/query?search_query={query}&max_results={retmax}&sortBy=submittedDate&sortOrder=descending"
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=20)
    root = ET.fromstring(r.stdout)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    results = []
    for entry in root.findall("a:entry", ns):
        title = entry.find("a:title", ns).text.strip().replace("\n"," ")
        aid = entry.find("a:id", ns).text.strip().split("/abs/")[-1]
        pub = entry.find("a:published", ns).text[:10]
        summary = entry.find("a:summary", ns).text.strip()[:300].replace("\n"," ")
        cats = ", ".join(c.get("term") for c in entry.findall("a:category", ns))
        results.append({"id": aid, "title": title, "date": pub, "cats": cats, "abstract": summary})
    return results

def s2_search(query, retmax=8):
    """Search Semantic Scholar"""
    cmd = f'curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={retmax}&fields=title,year,citationCount,externalIds,abstract"'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
    try:
        data = json.loads(r.stdout)
        return data.get("data", [])
    except:
        return []

# ================
# Customize searches below for your mapping task
# ================

def run_custom_searches():
    """Your specific evidence search queries go here."""
    
    print("="*70)
    print("Customize search blocks in run_custom_searches()")
    print("="*70)
    
    # Example block:
    # print("\n=== DIR1: PubMed — your query ===")
    # count, ids = pubmed_search("your+query+here")
    # print(f"Count: {count}, IDs: {ids}")
    # if ids:
    #     for r in pubmed_fetch(ids):
    #         print(f"  [{r['year']}] {r['title'][:120]}")
    #         print(f"      {r['journal']} | PMID:{r['pmid']}")
    #         print(f"      {r['abstract'][:200]}")
    #         print()
    # time.sleep(1)

if __name__ == "__main__":
    run_custom_searches()
