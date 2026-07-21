# Idea Direction Routing Signals

Load this reference only when Evidence/Opportunity Maps feed an Idea workflow.
The mapper describes the evidence landscape; the orchestrator applies the route.

```yaml
idea_direction_evidence:
  current_direction_value: supported | uncertain | unsupported
  evidence_confidence: high | moderate | low
  distinct_supported_directions:
    - title:
      rationale:
      supporting_claims: []
      evidence_confidence: high | moderate | low
      feasibility_note:
      closest_to_current_direction: true | false
  conflicts_or_ties: []
  negative_searches: []
  recommended_route: focused_optimization | bounded_exploration | direction_route_confirmation_required | no_defensible_direction
  recommendation_rationale:
```

- A supported direction needs a readable rationale and at least moderate
  evidence confidence. List two or three only when they are substantively
  distinct; never fill a quota.
- `supported` means the direction has defensible scientific, practical, method,
  validation, resource, or editorial value. It does not assert high quality or
  promotion readiness.
- Recommend owner confirmation for low-confidence signals, unresolved conflict,
  or more than three directions that remain tied after user priority, relevance,
  evidence confidence, feasibility, and distinctness.

For a bounded-exploration remap, add:

```yaml
direction_remap:
  dossier_ref:
  evidence_claim_sync:
    background_updates: []
    citation_updates: []
    closest_work_updates: []
    claim_qualifier_updates: []
    title_or_audience_updates: []
    summary_abstract_positioning_updates: []
    claim_support_row_updates: []
  structural_change_required: true | false
  structural_change_reason:
```

The mapper does not modify the dossier. Structural changes route to
`revision_required`; non-structural notes may be integrated into a complete new
dossier before its one terminal evaluator.
