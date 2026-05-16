# Idea Schema

本文件管理 `multi-path-idea-generator` 输出候选 idea 的字段定义。共享 canonical contract 见 `research-idea-orchestrator/references/artifact-contracts.md` 的 Candidate Idea。

## Required fields

```yaml
ideas:
  - schema_version: "research-idea.v1"
    idea_id: ""
    previous_ids: []
    source_skill: "multi-path-idea-generator"
    created_round: 1
    origin_round: 1
    revision_round: 0
    status: draft
    title: ""
    one_sentence_summary: ""
    research_question: ""
    hypothesis_or_objective: ""
    endpoint_or_metric: ""
    data_source_or_evidence_base: ""
    minimal_experiment_or_analysis: ""
    value_claim: ""
    novelty_claim:
      text: ""
      confidence: high | moderate | low | speculative | unverified
    supporting_opportunity_ids: []
    generation_paths: []
    assumptions_and_uncertainties: []
    risks_or_objections: []
    lineage:
      lineage_id: ""
      parent_idea_ids: []
      variant_type: original | expanded | refined | merged | reframed | salvaged
      changes_from_parent: []
```

## Field rules

- `idea_id` may be provisional only inside generator output; orchestrator must normalize it before preflight, evaluation, adversarial review, or portfolio assembly.
- Canonical IDs must follow `research-idea-orchestrator/references/idea-id-and-lineage-rules.md`.
- If a provisional ID is normalized, record it in `previous_ids`.
- `generation_paths` must contain at least one valid path from `generation-paths.md`.
- `supporting_opportunity_ids` should reference the Opportunity Map.
- `novelty_claim` must obey `novelty-claim-rules.md`.
- `lineage.parent_idea_ids` is required for revisions, merges, reframes, or salvage attempts.
