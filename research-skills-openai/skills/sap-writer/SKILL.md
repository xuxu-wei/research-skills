---
name: sap-writer
description: "Draft or revise a versioned SAP from approved endpoints, design, data structure, preflight findings, and revision instructions."
---
# sap-writer

## Role

Draft or revise an explicitly requested Statistical Analysis Plan after methodology/statistics preflight permits it. Do not evaluate the SAP, score the proposal, or invent statistical facts.

## Required Inputs

Require explicit SAP authorization, approved preflight, context/proposal, endpoint/metric/analysis target, population, available data and structure, user goal/constraints, and current SAP path/version for revision. Stop when authorization or preflight is missing/blocked, endpoints/population/primary route are undefined, data cannot support the route, or completion requires invented information.

## Invariants

- SAP is optional and never starts by default.
- Work against an explicit `sap_file_path`; never overwrite a prior version.
- Align question, estimand/target, endpoint, population, data, method, preflight, and target output.
- Separate prespecified confirmatory, secondary/supportive, post hoc, and exploratory analyses.
- Mark unresolved inputs instead of inventing endpoint, sample size, analysis population, data structure, model, covariates, or feasibility.
- Do not certify or evaluate your own SAP.

## Procedure

1. Confirm SAP scope and qualifying preflight status.
2. Establish source/new path, version, linked proposal/context, preflight reference, change type, and unresolved issues.
3. Define objective, estimand/analysis target, hypotheses, endpoints/metrics, populations/analysis sets, data provenance/derivations, exposure/intervention/predictor/comparator, covariates, and primary analysis.
4. Add prespecified secondary, separately labeled post hoc/exploratory, missing-data, sensitivity, subgroup, multiplicity, power/sample-size when supported, software, reproducibility, assumptions, and limitations.
5. For clinical data, define source, index/baseline/follow-up/assessment windows, endpoint ascertainment/coding/validation, censoring, competing risks, clustering, provider/site effects, and key bias controls when applicable.
6. Identify clinically relevant demographic, disease/severity, treatment/care, comorbidity, and socioeconomic features; distinguish descriptive-only, candidate confounder/covariate, effect modifier/subgroup, stratification factor, and unavailable/unresolved.
7. In revision mode, change only specified items, create a new SAP version, and record a specific delta/change summary plus unresolved issues.
8. Return paths, versions, lineage, linked inputs, concise change summary, unresolved issues, and `SAP evaluation | re-evaluation` route; do not return a quality decision.

## Output Contract

```yaml
sap_handoff:
  source_skill: sap-writer
  sap_file_path:
  sap_version:
  based_on: []
  change_type: initial | substantive | language_only | formatting_only
  linked_proposal_path:
  preflight_report_path:
  change_summary: []
  unresolved_issues: []
  next_route: evaluation | re-evaluation
```

## Conditional Resources

- Read `references/rules-sap-writing.md` when defining required sections and prohibited inventions.
- Read `references/rules-endpoint-analysis-alignment.md` when linking question, estimand, endpoint, population, and primary analysis.
- Read `references/rules-missing-data-sensitivity.md` when specifying missingness and robustness.
- Read `references/rules-clinical-data-analysis.md` for clinical source, windows, ascertainment, bias, and interpretation.
- Read `references/rules-clinical-feature-descriptives.md` when planning population descriptors and feature roles.
- Read `references/rules-prespecified-vs-exploratory.md` when separating confirmatory and exploratory analyses.
- Read `references/policy-sap-file-maintenance.md` when assigning versions, lineage, and change summaries.
- Read `references/schema-sap.md` when validating structure.
- Use `templates/template-sap.md` when producing the SAP artifact.

## Completion Check

Confirm explicit authorization/preflight, path/version, endpoint/population/primary route, data-method alignment, missing-data/sensitivity plans, prespecification separation, clinical details when applicable, visible unknowns, no invented facts, and a separate evaluator handoff.
