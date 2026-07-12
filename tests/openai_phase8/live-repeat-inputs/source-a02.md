# Frozen synthetic article source bundle

```yaml
artifact_id: source-a02
version_id: v001
workflow_id: workflow-a02
round_id: r001
plugin_version: 0.6.0-preview.1
source_skill: article-drafter
created_by_instance_id: writer-a02
based_on: [article-context-syn@v001, article-blueprint-syn@v001]
change_type: initial_draft
frozen: true
anonymity: Synthetic case; no person, institution, unpublished dataset, or user source is represented.
```

## Context and approved analysis

- Design: synthetic retrospective cohort; 1,200 records; complete follow-up.
- Primary estimand: adjusted risk ratio for exposure A and outcome Y at day 30.
- Primary model: prespecified log-binomial model with covariates C1-C3.
- Prespecified sensitivity analysis: repeat the primary model after excluding
  events recorded during days 0-2.
- The sensitivity result exists in the frozen analysis output: adjusted risk
  ratio 1.18, 95% CI 1.03-1.35.
- The frozen analysis inventory contains both the primary estimate and the
  day 0-2 exclusion estimate, with their model specifications and output-table
  locations.

## Draft manuscript excerpt

Methods states that the primary model and the day 0-2 exclusion sensitivity
analysis were prespecified. Results reports the primary adjusted risk ratio as
1.21 (95% CI 1.06-1.38), but it does not report or mention the sensitivity
analysis. Discussion says that conclusions were robust across all prespecified
analyses.
