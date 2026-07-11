# Opportunity Map Schema

This file defines the structured fields for Opportunity Map outputs.

```yaml
opportunity_map:
  - opportunity_id: O1
    type: gap | value | method | data | metric | failure | theory | benchmark | taxonomy | implementation
    title: ""
    description: ""
    supporting_claim_ids: []
    supporting_sources: []
    evidence_confidence: high | moderate | low | speculative | not_verified
    novelty_risk: low | medium | high | unverified
    guideline_alignment: aligned | partially_aligned | conflicting | not_applicable | unverified
    why_it_matters: ""
    feasibility_concerns: []
    recommended_generation_paths: []
    downstream_notes:
      for_generator: ""
      for_preflight: ""
      for_evaluator: ""
```

Each opportunity must point back to evidence or be marked `not_verified`. Do not write a full research idea.
