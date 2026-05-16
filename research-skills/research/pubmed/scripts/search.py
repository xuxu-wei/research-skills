#!/usr/bin/env python3
"""
PubMed Search — query NCBI E-utilities esearch, return PMIDs.

Usage:
    python3 search.py "Wei Xuxu[Author]" --max 20
    python3 search.py "GRPO reinforcement learning" --max 10 --mindate 2024/01/01
    python3 search.py "diabetes[MeSH Terms] AND metformin[Title]" --max 50 --json

Output modes:
    --json   → {"count": N, "pmids": [...], "query_translation": "..."}
    default  → plain text: one PMID per line
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def search(query: str, retmax: int = 20, retstart: int = 0,
           mindate: str = None, maxdate: str = None,
           datetype: str = "pdat",
           api_key: str = None) -> dict:
    """Search PubMed, return dict with count and PMIDs."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retstart": retstart,
    }
    if mindate:
        params["mindate"] = mindate
    if maxdate:
        params["maxdate"] = maxdate
    if datetype:
        params["datetype"] = datetype
    if api_key:
        params["api_key"] = api_key

    url = ESEARCH_URL + "?" + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            root = ET.parse(resp).getroot()
    except Exception as e:
        return {"error": str(e), "count": 0, "pmids": []}

    count_el = root.find("Count")
    count = int(count_el.text) if count_el is not None else 0

    pmids = [el.text for el in root.findall(".//Id") if el.text]

    # Extract query translation for debugging
    qt_el = root.find("QueryTranslation")
    query_translation = qt_el.text if qt_el is not None else query

    return {
        "count": count,
        "pmids": pmids,
        "query_translation": query_translation,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Search PubMed via NCBI E-utilities esearch"
    )
    parser.add_argument("query", help="Search query (supports [Author], [Title/Abstract], etc.)")
    parser.add_argument("--max", type=int, default=20, dest="retmax",
                        help="Max results to return (default: 20)")
    parser.add_argument("--start", type=int, default=0, dest="retstart",
                        help="Result offset for pagination (default: 0)")
    parser.add_argument("--mindate", default=None,
                        help="Earliest publication date (YYYY/MM/DD)")
    parser.add_argument("--maxdate", default=None,
                        help="Latest publication date (YYYY/MM/DD)")
    parser.add_argument("--datetype", default="pdat",
                        choices=["pdat", "edat", "mdat"],
                        help="Date type: pdat=publication, edat=entrez, mdat=modification")
    parser.add_argument("--api-key", default=None, dest="api_key",
                        help="NCBI API key (optional, increases rate limit)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of plain PMID list")

    args = parser.parse_args()

    result = search(
        query=args.query,
        retmax=args.retmax,
        retstart=args.retstart,
        mindate=args.mindate,
        maxdate=args.maxdate,
        datetype=args.datetype,
        api_key=args.api_key,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("error"):
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        # Print count to stderr so pipe still captures clean PMID list
        print(f"# {result['count']} results (showing {len(result['pmids'])})", file=sys.stderr)
        for pmid in result["pmids"]:
            print(pmid)


if __name__ == "__main__":
    main()
