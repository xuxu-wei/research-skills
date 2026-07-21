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

## Claim-to-source bindings

Treat an atomic claim, not a sentence, as the citation unit. A supported atomic
claim must bind one to five directly relevant works. One work may support more
than one claim, but every binding keeps the locator that supports that claim.

```yaml
claim_id: C001
claim: ""
supporting_sources:
  - reference_id: R001
    locator: ""
    source_role: direct_support
opposing_sources:
  - reference_id: R002
    locator: ""
    source_role: direct_contradiction
```

Use `direct_support | direct_contradiction | background_only |
negative_search_result` as source roles. Background sources and negative search
results do not count toward the one-to-five direct-support limit. Record a
negative search with its query or search-ledger locator rather than inventing a
reference record.

- `single-source` requires exactly one direct-support binding. Use `supported`
  for two to five concordant direct-support bindings; use `weak` or
  `conflicting` when source quality or direction requires it.
- `unverified` may have no direct-support binding. Never label a zero-source
  claim `supported` or `single-source`.
- If more than five works support one claim, cite at most five of the most
  direct, authoritative, and representative works and retain the wider set in
  the Evidence Map or search log. If the works support different propositions,
  split the claim instead of hiding that heterogeneity.
- When one sentence contains several independently testable clauses, assign a
  claim ID to each clause and place each clickable reference group immediately
  after the clause it supports. Do not put one undifferentiated reference group
  at the sentence end unless every listed work supports the whole sentence.
- Never compress several works into a pseudo-reference such as `R001-R003`.
  Each linked ID must resolve to exactly one reference record.

When supplied material mentions a work without a full reference, infer a
candidate from author or team, year, journal, title fragment, topic, method,
finding, and citation relationships. Use `inferred_unique_match` only after
identity verification. Use `inferred_series_match` for a clearly identifiable
series and create one record per work. Preserve ambiguous candidates instead of
choosing silently.
