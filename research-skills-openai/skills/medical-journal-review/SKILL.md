---
name: medical-journal-review
description: "Independently review a frozen medical study, protocol, manuscript, or cover letter for editorial, methods, statistics, claims, and fit."
---
# Medical Journal Research Design Review

## Purpose

Independently assess a medical study, protocol, proposal, or manuscript from the perspective of a general medical journal editor, clinical epidemiologist, and statistical reviewer. Identify fatal flaws, important weaknesses, defensible claims, journal fit, and concrete redesign or revision priorities.

This skill evaluates existing artifacts. It does not draft, rewrite, polish, fabricate missing material, or promise publication.

## Independent Execution Contract

- Run this skill only in a fresh independent subagent or delegated thread. Never review an artifact in the agent context that generated, drafted, or revised it.
- Receive frozen artifact IDs, file paths, and versions. Treat every source artifact as read-only and write only the review report.
- Do not edit, rewrite, polish, repair, or directly modify the reviewed design, protocol, proposal, manuscript, tables, figures, or supplementary files.
- Do not use parent-thread hidden reasoning, expected conclusions, prior reviewer outputs, or prior scores. Base the review only on the frozen inputs and declared rubric.
- Report the exact files read, sections reviewed, missing materials, scope limitations, and independent reviewer instance identifier.
- If a fresh subagent cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline review.

## Inputs

Accept the available subset of:

- research question and intended claim;
- study type, population, exposure/intervention, comparator, outcomes, and time window;
- data source, sample size, protocol/SAP, analysis plan, and preliminary results;
- manuscript, tables, figures, appendices, and supplementary materials;
- target journal or journal tier;
- frozen artifact IDs and versions.

When a manuscript refers to supplementary material, inspect the supplied task files and artifact manifest. Do not search product-specific caches or assume that files uploaded together belong to the same manuscript. Verify association from title, authors, identifiers, or explicit manifest links.

If inputs are incomplete, distinguish what can be judged, what cannot be judged, the most important missing items, and how those gaps limit confidence.

## Review Route

Choose one route and record it in the report:

- **Design review**: research question, design-question fit, endpoint choice, comparator, bias, confounding, analysis route, and redesign options.
- **Editorial review**: importance, evidence gap, claim support, reporting completeness, journal fit, and revision priority. Load `references/12-step-editorial-review.md` when this route is selected.
- **Statistical review**: estimand/target, model-data fit, missing data, multiplicity, uncertainty, validation, sensitivity analyses, and interpretation. Load `references/bmj-statistical-review-standards.md` when this route is selected.

## Workflow

1. Record the frozen inputs, review route, target outlet, and scope limitations.
2. Identify study type, intended claim type, and primary decision the evidence is meant to support.
3. Summarize population, data, exposure/intervention, comparator, outcomes, timing, and analysis route.
4. Check design-question fit and whether the available evidence can support the stated claim.
5. Check endpoint, comparator, bias, confounding, missingness, multiplicity, validation, and uncertainty as applicable.
6. Inspect all supplied tables, figures, and supplementary materials before declaring an analysis absent.
7. Identify fatal flaws, major weaknesses, minor issues, and claims requiring downscaling.
8. Provide at least one feasible redesign or repair route when defects are reparable.
9. Assess target-journal fit without converting the score into publication probability.
10. Produce the structured report using `templates/review-report.md`. Use this resource only when producing its named artifact.

## Decision Labels

- `support`
- `support_with_minor_revision`
- `major_revision_required`
- `redesign_required`
- `not_reviewable_with_current_materials`
- `fatal_flaw`

## Report Contract

Every report must include:

```yaml
review_id:
reviewer_skill: medical-journal-review
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids:
input_versions:
files_read:
review_route:
review_scope:
scope_limitations:
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
fatal_flaws:
major_findings:
minor_findings:
claim_adjustments:
repair_or_redesign_options:
journal_fit:
unresolved_issues:
```

## Boundaries

- Do not draft or revise the reviewed artifact.
- Do not infer unreported analyses from filenames or narrative hints.
- Do not declare an analysis missing before checking supplied supplementary materials.
- Do not present observational or predictive findings as causal.
- Do not treat novelty of method as proof of clinical importance.
- Do not turn a structured score into a publication probability.
- Do not hide dissent, uncertainty, missing evidence, or fatal flaws.

## Verification

- Review ran in a fresh independent subagent.
- Artifact identifiers and versions are frozen and reported.
- All files read are listed.
- Study type and intended claim are explicit.
- Supplementary materials were checked when provided.
- Fatal flaws and scope limitations are visible.
- Recommendations are traceable to findings.
- Source artifacts were not modified.
