#!/usr/bin/env python3
"""
PubMed Fetch — fetch paper details via NCBI E-utilities efetch.

Usage:
    # From PMID list on command line
    python3 fetch.py 42062541

    # From stdin (pipe from search.py)
    python3 search.py "GRPO[Title/Abstract]" --max 5 | python3 fetch.py

    # Batch fetch
    python3 fetch.py 42062541 41808319 39559736

    # JSON output
    python3 fetch.py 42062541 --json

Output modes:
    --json     → list of paper dicts (structured)
    default    → human-readable formatted text
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch(pmids: list[str], api_key: str = None) -> list[dict]:
    """Fetch PubMed article details for a list of PMIDs. Max 200 per call."""
    if not pmids:
        return []

    pmids = pmids[:200]  # hard cap

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    if api_key:
        params["api_key"] = api_key

    url = EFETCH_URL + "?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            root = ET.parse(resp).getroot()
    except Exception as e:
        return [{"pmid": pmid, "error": str(e)} for pmid in pmids]

    papers = []
    for article in root.findall(".//PubmedArticle"):
        paper = _parse_article(article)
        papers.append(paper)

    # Some PMIDs may not have been returned — mark them
    returned_ids = {p["pmid"] for p in papers}
    for pmid in pmids:
        if pmid not in returned_ids:
            papers.append({"pmid": pmid, "error": "not found in efetch response"})

    return papers


def _parse_article(article) -> dict:
    """Parse a single PubmedArticle element into a dict."""
    pmid_el = article.find(".//PMID")
    pmid = pmid_el.text if pmid_el is not None else "UNKNOWN"

    title_el = article.find(".//ArticleTitle")
    title = title_el.text if title_el is not None else "(no title)"
    title = " ".join(title.replace("\n", " ").split())

    # Authors
    authors = []
    for a in article.findall(".//Author"):
        ln = a.find("LastName")
        fn = a.find("ForeName")
        if ln is not None and ln.text:
            init = fn.text[:1] if (fn is not None and fn.text) else ""
            authors.append(f"{ln.text} {init}" if init else ln.text)

    # Journal
    journal_el = article.find(".//Journal/Title")
    journal = journal_el.text if journal_el is not None else None

    year_el = article.find(".//PubDate/Year")
    year = year_el.text if year_el is not None else None

    # DOI
    doi = None
    for aid in article.findall(".//ArticleId"):
        if aid.get("IdType") == "doi":
            doi = aid.text
            break

    # Abstract
    abs_parts = article.findall(".//AbstractText")
    abstract = " ".join(p.text or "" for p in abs_parts).strip() if abs_parts else None

    # MeSH terms
    mesh_terms = []
    for mh in article.findall(".//MeshHeading"):
        dn = mh.find("DescriptorName")
        if dn is not None and dn.text:
            mesh_terms.append(dn.text)

    # Publication types
    pub_types = [
        pt.text for pt in article.findall(".//PublicationType")
        if pt is not None and pt.text
    ]

    # PMID list (for articles with multiple PMIDs / version history)
    alt_pmids = []
    for pid in article.findall(".//OtherID"):
        if pid.get("Source") == "NLM":
            alt_pmids.append(pid.text)

    return {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "doi": doi,
        "abstract": abstract,
        "mesh_terms": mesh_terms,
        "pub_types": pub_types,
    }


def format_paper(paper: dict) -> str:
    """Format a paper dict as human-readable text."""
    if "error" in paper:
        return f"PMID: {paper['pmid']}  ERROR: {paper['error']}\n"

    lines = [f"PMID: {paper['pmid']}"]
    lines.append(f"  {paper['title']}")

    authors = ", ".join(paper["authors"]) if paper["authors"] else "N/A"
    lines.append(f"  {authors}")

    j = paper.get("journal") or "?"
    y = paper.get("year") or "?"
    doi_str = f"  |  DOI: {paper['doi']}" if paper.get("doi") else ""
    lines.append(f"  {j} ({y}){doi_str}")

    if paper.get("abstract"):
        abs_text = paper["abstract"]
        if len(abs_text) > 500:
            abs_text = abs_text[:497] + "..."
        lines.append(f"  Abstract: {abs_text}")

    if paper.get("mesh_terms"):
        lines.append(f"  MeSH: {'; '.join(paper['mesh_terms'][:8])}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed article details via NCBI E-utilities efetch"
    )
    parser.add_argument("pmids", nargs="*",
                        help="PubMed IDs (space-separated). If omitted, read from stdin.")
    parser.add_argument("--api-key", default=None, dest="api_key",
                        help="NCBI API key (optional)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of formatted text")

    args = parser.parse_args()

    pmids = args.pmids
    if not pmids:
        # Read PMIDs from stdin (one per line, strip whitespace)
        stdin_text = sys.stdin.read().strip()
        pmids = [line.strip() for line in stdin_text.splitlines() if line.strip()]

    if not pmids:
        print("Error: No PMIDs provided.", file=sys.stderr)
        sys.exit(1)

    papers = fetch(pmids, args.api_key)

    if args.json:
        print(json.dumps(papers, indent=2, ensure_ascii=False))
    else:
        for i, paper in enumerate(papers):
            if i > 0:
                print()
                print("---")
                print()
            print(format_paper(paper))


if __name__ == "__main__":
    main()
