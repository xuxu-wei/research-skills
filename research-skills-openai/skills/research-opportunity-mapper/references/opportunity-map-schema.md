# Opportunity Map Schema

```yaml
opportunity_map:
  schema_version: research-idea.v3
  scientific_gap:
    unanswered_problem:
    missing_knowledge_or_evidence:
    consequence:
    supporting_sources: []
  novelty_positioning:
    closest_work: []
    overlap:
    differentiation:
    novelty_risk: low | medium | high | unverified
  reader_reasoning_handoff:
    background:
    current_state:
    gap:
    significance:
    rationale:
  opportunities:
    - opportunity_id: O1
      title:
      type: gap | value | method | data | metric | failure | theory | benchmark | taxonomy | implementation
      description:
      supporting_claims:
        - claim_id:
          label:
      supporting_sources:
        - citation:
          original_source:
          locator:
      evidence_confidence: high | moderate | low | speculative | not_verified
      novelty_risk: low | medium | high | unverified
      why_it_matters:
      feasibility_concerns: []
      recommended_generation_paths: []
  idea_direction_evidence: {}
```

Every ID must have a readable title/label and resolve to evidence or be marked
`not_verified`. `scientific_gap` states the unanswered problem and missing
knowledge/evidence; `novelty_positioning` separately compares the direction
with its closest work. Neither may substitute for the other. For Idea work,
populate every `reader_reasoning_handoff` function from mapped evidence or mark
the unresolved link explicitly. Populate `idea_direction_evidence` only for an
Idea workflow; follow `idea-direction-routing-signals.md`. Do not write a
research Idea or a terminology verdict.
