# Opportunity Map Schema

```yaml
opportunity_map:
  schema_version: research-idea.v3
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
`not_verified`. Populate `idea_direction_evidence` only for an Idea workflow;
follow `idea-direction-routing-signals.md`. Do not write a research Idea.
