# Evidence Map Schema

This file defines the structured fields for Evidence Map outputs.

```yaml
evidence_map:
  schema_version: research-idea.v3
  evidence_status: sufficient | partial | insufficient | unverified
  scope:
    research_domain: ""
    topic_or_idea: ""
    intended_output: ""
    downstream_task: idea_generation | idea_dossier_preparation | proposal_readiness | proposal_drafting | proposal_evaluation | methodology_preflight | other
  evidence_acquisition_note: ""  # optional; use only for reuse, retrieval failure, evidence limitation, or audit request
  source_summary:
    user_provided_sources: []
    retrieval_routes_executed: []
    retrieved_or_available_sources: []
    inaccessible_or_missing_sources: []
  references:
    - reference_id: R001
      citation_gbt7714_2015: ""
      canonical_url: ""
      identifiers: {doi: "", pmid: "", pmcid: "", isbn: ""}
      identification_status: explicitly_identified | inferred_unique_match | inferred_series_match | ambiguous_candidates | not_found
      verification_status: verified | unverified | access_limited
      original_source_locator: ""
      verification_date: ""
  key_claims:
    - claim_id: C1
      label: ""
      claim: ""
      claim_type: background | gap | value | method | data | metric | guideline | implementation | other
      support_status: supported | weak | conflicting | single-source | unverified | access-limited
      supporting_sources:
        - reference_id: R001
          locator: ""
      opposing_sources: []
      evidence_confidence: high | moderate | low | speculative | not_verified
      novelty_verification: verified | partially_verified | unverified | disputed | not_applicable
      guideline_alignment: aligned | partially_aligned | conflicting | not_applicable | unverified
      limitations: []
      requires_manual_check: true | false
  contradictions: []
  evidence_limitations: []
```

`support_status` describes whether the inspected sources support the claim;
`evidence_confidence` describes confidence in that evidence. Keep both fields.
Use `single-source` even when the sole source is strong, and use
`access-limited` when a necessary source cannot be inspected.

Do not record planned but unperformed searches as verified evidence. Use the separate source verification log only when auditability, retrieval failure, source conflict, high-risk claims, or user request makes it necessary.
