---
name: article-readiness-triage
description: "Assess whether a research study has the minimum conditions to enter the manuscript writing system. Determines readiness status, recommended article type, blocking and nonblocking gaps, target journal realism, and recommended route. Does not normalize input, build context, or draft manuscript content."
---
# article-readiness-triage

## Purpose

Use this skill BEFORE any manuscript writing begins. It answers one question: **does this research have the minimum conditions to be written into a manuscript?**

This skill does NOT normalize input (that is `article-context-builder`'s job), retrieve literature, audit methods, or draft content.

## Core Rules

- Judge readiness, not quality. A study can be "ready to write" even if its results are modest.
- Block only when writing would be impossible or irresponsible: missing primary results, unclear research question, undefined study design.
- Distinguish between what writing CAN fix (missing Methods details, unclear structure) and what writing CANNOT fix (no primary endpoint data, study design cannot support inference).
- Be conservative about target journal realism: "Nature with n=20 convenience sample" should be flagged as mismatch.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread. Never perform this review in the generator, drafter, revision, or orchestrator context.
- Receive frozen artifact IDs, file paths, and versions. Treat every source artifact as read-only.
- Write only the readiness review report. Do not edit, rewrite, polish, or fix any source artifact.
- Do not access parent hidden reasoning, expected answers, or outputs from other reviewers.
- Report `files_read` and `review_scope` in the review report, together with the standard review identity and isolation fields.
- Include `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `review_scope`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.
- If a fresh independent subagent or delegated thread cannot be established, return `independent_review_pending` plus a self-contained continuation brief and stop. Never review inline.

```yaml
review_id:
reviewer_skill: article-readiness-triage
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

## Inputs

- `minimal_intake_summary`: study_topic, apparent_study_type, available_materials, stated_target_journal, obvious_missing_items.

## Outputs

Structured Readiness Report (see `references/schema-readiness-report.md` for full schema):

- `readiness_status`: ready | conditionally_ready | not_ready | wrong_article_type
- `recommended_article_type`: original_article | brief_report | research_letter | methods_article | data_descriptor | case_report | review | other
- `minimum_inputs_present`: boolean flags for research_question, study_design, primary_results, methods_details, figures_tables, references
- `blocking_gaps`: what is missing and what action is required
- `nonblocking_gaps`: what is missing but can be managed during writing
- `target_journal_realism`: realistic | ambitious_but_possible | mismatch
- `recommended_route`: blueprint | methods_preflight | data_analysis | literature_review | stop

## Workflow

### 1. Confirm Scope

Verify this is a readiness triage, not context building, literature review, or manuscript evaluation.

### 2. Assess Minimum Inputs

Check each of the seven minimum input categories:

| Input | Required for |
|-------|-------------|
| research_question | All article types |
| study_design | All article types |
| primary_results | All article types (must have results to write results) |
| methods_details | All article types (must describe what was done) |
| figures_tables | Original articles; may be minimal for brief reports |
| references | Introduction and Discussion need literature context |

### 3. Identify Blocking Gaps

A gap is **blocking** if manuscript writing cannot responsibly begin without it:

- Primary results are missing or unclear
- Research question cannot be stated
- Study design is undefined
- Primary endpoint/outcome is not defined
- The study design fundamentally cannot support the intended inference

For each blocking gap, specify `required_action`: data_analysis | experiment | literature_review | methods_documentation | user_clarification.

### 4. Identify Nonblocking Gaps

A gap is **nonblocking** if it can be addressed during writing:

- Methods section missing some details (can be filled in during drafting)
- Literature context not fully prepared (can be supplemented during grounding)
- Some secondary analyses incomplete (can be noted as pending)
- Figures/tables in draft form (can be refined)

For each nonblocking gap, suggest a `mitigation`.

### 5. Determine Article Type

Based on study design, evidence strength, and material volume:

| Condition | Recommended Type |
|-----------|-----------------|
| Full study with multiple analyses, multiple endpoints, detailed methods | original_article |
| Single clear finding, simple design, limited analyses | brief_report |
| Preliminary or exploratory analysis, small sample | research_letter |
| Primary contribution is a new method or tool | methods_article |
| Primary contribution is a dataset or resource | data_descriptor |
| Single case or small case series | case_report |
| No original data — synthesis of existing literature | review |

### 6. Assess Target Journal Realism

Cross-check the stated target journal against study characteristics:

- Sample size vs. journal norms
- Study design complexity vs. journal expectations
- Novelty vs. journal threshold
- Article type availability at the target journal

Three levels:
- `realistic`: Study type and scope match journal norms
- `ambitious_but_possible`: Not typical but not impossible
- `mismatch`: Clear discrepancy (e.g., case report for Nature)

### 7. Determine Recommended Route

- `blueprint`: Ready to enter the article architecture phase.
- `methods_preflight`: Methods clarity concerns → run `methodology-statistics-preflight` first.
- `data_analysis`: Results not yet in analyzable form → user must complete analysis.
- `literature_review`: Literature context too thin → user must provide or `article-literature-grounder` must search.
- `stop`: Blocking gap that cannot be resolved within the writing system.

## Stop Conditions

Return with an incomplete report (not a forced "ready") if:
- `minimal_intake_summary` is empty
- No study topic can be identified
- User explicitly asks to evaluate quality rather than readiness

## Pitfalls

- Do not confuse "study has limitations" with "study is not ready to write." All studies have limitations.
- Do not recommend `original_article` for a single-table finding that fits a research letter.
- Do not pass a study with no primary results just because the user wants to start writing.
- Do not lower the bar to keep the workflow moving.
- Do not normalize raw input into a context brief — that is context-builder's job.

## Verification

- All seven minimum input categories explicitly assessed
- Each blocking gap has a `required_action`
- Article type recommendation matches study characteristics
- Target journal realism is assessed, not assumed
- Recommended route is specific, not just "proceed"

## References

- `references/schema-readiness-report.md`: Full YAML schema for the readiness report output.
- `article-orchestrator/references/artifact-contracts.md`: Canonical artifact contracts.
