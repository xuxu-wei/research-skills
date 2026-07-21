# Citation Record Contract

Use one record per cited work on every retrieval route:

```yaml
reference_id: R001
citation_gbt7714_2015: ""
canonical_url: ""
identifiers: {doi: "", pmid: "", pmcid: "", isbn: ""}
identification_status: explicitly_identified | inferred_unique_match | inferred_series_match | ambiguous_candidates | not_found
verification_status: verified | unverified | access_limited
original_source_locator: ""
verification_date: ""
```

Retain a complete GB/T 7714—2015 citation and a clickable canonical link for
every formal reference. A URL does not replace the citation, and a citation does
not replace the URL.

When supplied material mentions a work without a full reference, infer a
candidate from author or team, year, journal, title fragment, topic, method,
finding, and citation relationships. Use `inferred_unique_match` only after
identity verification. Use `inferred_series_match` for a clearly identifiable
series and create one record per work. Preserve ambiguous candidates instead of
choosing silently.
