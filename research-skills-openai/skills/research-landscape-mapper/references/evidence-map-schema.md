# Evidence Map Schema

This file defines the structured fields for Evidence Map outputs.

```yaml
evidence_map:
  schema_version: research-idea.v3
  consumer_workflow: idea | proposal | perspective | article | research_polisher
  output_profile: evidence_only | evidence_and_opportunity | idea_landscape
  retrieval_mode: auto | built_in_web_search | deep_research
  exploration_mode: standard | focused | divergent
  evidence_status: sufficient | partial | insufficient | unverified
  scope:
    research_domain: ""
    topic_or_idea: ""
    intended_output: ""
    downstream_task: idea_generation | idea_dossier_preparation | proposal_readiness | proposal_drafting | proposal_evaluation | perspective_grounding | article_grounding | research_polisher_positioning | methodology_preflight | other
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
          source_role: direct_support
      opposing_sources:
        - reference_id: R002
          locator: ""
          source_role: direct_contradiction
      background_sources:
        - reference_id: R003
          locator: ""
          source_role: background_only
      negative_search_results:
        - search_locator: ""
          source_role: negative_search_result
      evidence_confidence: high | moderate | low | speculative | not_verified
      novelty_verification: verified | partially_verified | unverified | disputed | not_applicable
      guideline_alignment: aligned | partially_aligned | conflicting | not_applicable | unverified
      limitations: []
      requires_manual_check: true | false
  contradictions: []
  evidence_limitations: []
  deep_research_return:  # omit when Deep Research was not used
    report_ref: {artifact_id: "", version: "", exact_path: ""}
    decision: accepted | revision_required | supplemental_search_required
    main_question_coverage: sufficient | partial | insufficient
    subquestion_coverage: sufficient | partial | insufficient
    claim_source_traceability: passed | failed
    citation_and_link_completeness: passed | failed
    closest_work_coverage: sufficient | partial | insufficient | not_applicable
    contrary_evidence_coverage: sufficient | partial | insufficient
    applicability_bounds_explicit: true | false
    novelty_evidence_usable: true | false
    unresolved_items: []
  repairability_assessment:  # required when the return is not accepted
    core_scientific_answer: usable | partially_usable | unusable
    evidence_landscape: recoverable | materially_incomplete | invalid
    source_identity_recoverability: high | moderate | low
    selected_route: deterministic_normalization | built_in_search_and_agent_repair | focused_literature_synthesis | second_deep_research
    severe_conditions_met: []
    prior_lower_cost_repairs_attempted: []
    route_reason: ""
    owner_approval_required: false
```

`support_status` describes whether the inspected sources support the claim;
`evidence_confidence` describes confidence in that evidence. Keep both fields.
Use `single-source` even when the sole source is strong, and use
`access-limited` when a necessary source cannot be inspected.

Each scientifically supported claim has one to five `direct_support` bindings:
use `single-source` for one and `supported` for two to five concordant sources.
Background and negative-search records do not count toward that limit. A sixth
direct-support binding requires representative-source selection or claim splitting. Every
linked reference ID resolves exactly once; source roles and locators apply to
the individual claim binding, not to the document as a whole.

Do not record planned but unperformed searches as verified evidence. Use the separate source verification log only when auditability, retrieval failure, source conflict, high-risk claims, or user request makes it necessary.
