# Evidence Map Schema

This file defines the structured fields for Evidence Map outputs.

```yaml
evidence_map:
  evidence_status: sufficient | partial | insufficient | unverified
  scope:
    research_domain: ""
    topic_or_idea: ""
    intended_output: ""
    downstream_task: idea_generation | idea_evaluation | proposal_readiness | proposal_drafting | proposal_evaluation | methodology_preflight | other
  evidence_acquisition_note: ""  # optional; use only for reuse, retrieval failure, evidence limitation, or audit request
  source_summary:
    user_provided_sources: []
    retrieval_routes_executed: []
    retrieved_or_available_sources: []
    inaccessible_or_missing_sources: []
  key_claims:
    - claim_id: C1
      claim: ""
      claim_type: background | gap | value | method | data | metric | guideline | implementation | other
      supporting_sources: []
      opposing_sources: []
      evidence_confidence: high | moderate | low | speculative | not_verified
      novelty_verification: verified | partially_verified | unverified | disputed | not_applicable
      guideline_alignment: aligned | partially_aligned | conflicting | not_applicable | unverified
      limitations: []
      requires_manual_check: true | false
  contradictions: []
  evidence_limitations: []
```

Do not record planned but unperformed searches as verified evidence. Use the separate source verification log only when auditability, retrieval failure, source conflict, high-risk claims, or user request makes it necessary.
