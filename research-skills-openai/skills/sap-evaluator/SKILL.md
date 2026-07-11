---
name: sap-evaluator
description: "Evaluate a Statistical Analysis Plan file as an isolated independent methodology/statistics evaluator. Assesses clarity, feasibility, completion, methodological rigor, endpoint-analysis alignment, data-method fit, clinical data analysis readiness, prespecified versus exploratory analysis separation, missing data handling, sensitivity analyses, and reproducibility. Does not evaluate novelty or impact and does not rewrite SAP."
---
# sap-evaluator

## Independent Execution Contract

- Run this skill only in a fresh independent subagent or delegated thread. Never run it in the context that generated, drafted, or revised the artifact being evaluated.
- Require frozen input artifact IDs, file paths, and versions before evaluation. Treat all source artifacts as read-only.
- Write only a SAP evaluation report. Do not draft, rewrite, polish, fix, or otherwise modify any evaluated source.
- Do not use the parent task's hidden reasoning, expected answer, or any other evaluator/reviewer output.
- Report the exact files read and the evaluation scope in the review report.
- If a fresh independent execution context cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline review, and never emit `accept` or another passing decision.

### Required Review Report Provenance

Every report must contain: `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.

## When to Use

Use this skill when a SAP file has been generated or revised by `sap-writer`, or when the user explicitly asks for SAP review.

This skill evaluates SAP methodology, statistics, and executability. It does not evaluate proposal novelty, impact, or overall research value.

## Core Principles

- Must run as an isolated independent methodology/statistics evaluator subagent.
- Evaluate only the frozen SAP file and supplied context.
- Do not write, revise, or rewrite SAP content.
- Do not rely on `sap-writer` hidden reasoning.
- Evaluate Clarity, Feasibility, Completion, Methodological Rigor, Endpoint-Analysis Alignment, Data-Method Fit, Clinical Data Readiness, Clinical Feature Descriptives, Prespecification Discipline, Missing Data Handling, Sensitivity/Robustness, and Reproducibility.
- Check SAP hard gates and SAP fatal flaws.
- Return exactly one decision: `accept`, `revise`, `reject`, or `stop_no_gain`.

## Inputs

Usually supplied by `proposal-orchestrator` or `sap-refinement-controller`:

- `sap_file_path`
- `sap_version`
- `proposal_file_path`, if available
- proposal context brief
- methodology/statistics preflight report
- endpoint, outcome, or metric definitions
- available data description
- study population or analysis population
- user goal and target output
- user constraints
- anonymized prior must-fix issue list without scores or decision, if re-evaluation
- SAP revision delta report, if re-evaluation

If `sap_file_path` is missing, stop and return an input-gap report.

## Outputs

Return a SAP evaluation report with:

- overall decision;
- scores by SAP evaluation dimension;
- hard gate status;
- SAP fatal flaws, if any;
- major strengths;
- major weaknesses;
- methodological concerns;
- endpoint-analysis alignment concerns;
- data-method fit concerns;
- missing data and sensitivity analysis concerns;
- clinical data source/window/endpoint ascertainment concerns;
- clinically important feature and descriptive statistics concerns;
- prespecified versus post hoc/exploratory analysis concerns;
- reproducibility concerns;
- revision priorities;
- rationale for `accept`, `revise`, `reject`, or `stop_no_gain`.

Do not output a revised SAP.

## Procedure

### 1. Confirm Evaluation Scope

Confirm the evaluation object is a SAP file, not proposal, idea, full protocol, or review panel summary.

If the task asks for proposal novelty, impact, or overall proposal value, return a scope mismatch and route to `proposal-evaluator`.

### 2. Read SAP File and Context

Evaluate based on:

- SAP file;
- methodology/statistics preflight report;
- proposal file or context brief;
- endpoint/outcome/metric definitions;
- data description;
- user goal and constraints;
- anonymized prior must-fix issue list and SAP delta report, if re-evaluation. Do not read a prior score or decision.

Do not strengthen the SAP by assuming unstated facts.

### 3. Evaluate Core Dimensions

Assess:

- Clarity: endpoint, population, variables, analyses, and assumptions are clear.
- Feasibility: data, variables, sample, timeline, and resources can support the analysis.
- Completion: SAP includes the components required to execute the analysis.
- Methodological rigor: design, model, comparisons, adjustment, assumptions, and bias control are defensible.
- Endpoint-analysis alignment: endpoint or metric matches the primary analysis.
- Data-method fit: data type and structure fit the statistical method.
- Clinical data readiness: data source, index date, baseline/follow-up windows, endpoint ascertainment, coding, and clinical interpretation rules are adequate when relevant.
- Clinical feature descriptives: the SAP identifies clinically important population features and plans descriptive statistics even for relevant features not included in the primary model.
- Prespecification discipline: prespecified primary/secondary analyses are separated from post hoc and exploratory analyses.
- Missing data handling: strategy is explicit and suitable.
- Sensitivity / robustness: checks are sufficient for the main conclusion.
- Reproducibility: software, versions, analysis sets, and decision rules are sufficient.

### 4. Check Hard Gates and Fatal Flaws

Check for:

- undefined primary endpoint;
- unclear analysis population;
- missing primary analysis route;
- method-endpoint mismatch;
- data structure that cannot support the primary analysis;
- missing clinical data source, index date, measurement window, or endpoint ascertainment when required for clinical data analysis;
- absent descriptive statistics plan for clinically important baseline, disease, severity, treatment, comorbidity, care-context, or socioeconomic features when required to characterize the study population;
- confirmatory claims based on post hoc or exploratory analyses;
- undefined prespecification status when the SAP uses hypothesis-testing or confirmatory language;
- inadequate confounding or covariate control;
- missing data plan when missingness could affect conclusions;
- missing sensitivity analysis when the primary conclusion is fragile;
- SAP/proposal/context mismatch;
- untestable or non-executable key assumptions.

### 5. Assess Alignment With Preflight

Check whether preflight risks and blockers are handled, whether SAP introduces new data-method mismatch, and whether uncertainty from preflight was turned into unsupported certainty.

### 6. Decide Next Action

Return:

- `accept`: SAP can proceed to final package or human statistician review.
- `revise`: clear repairable issues remain; route to `sap-refinement-controller`.
- `reject`: fatal methodological flaw or endpoint/data/method basis fails.
- `stop_no_gain`: re-evaluation only; revision did not improve methodological executability.

### 7. Re-evaluation Rules

For SAP revision re-evaluation, compare the frozen previous and current SAP versions. Use only the anonymized must-fix list and revision delta for issue resolution; do not read the prior evaluator's scores, rationale, or decision.

Judge whether prior issues were resolved, new issues were introduced, and whether changes were substantive rather than formatting-only.

## Delegation Rules

This skill should be explicitly assigned by `proposal-orchestrator` or `sap-refinement-controller` to a fresh independent subagent or delegated thread.

The subagent must receive complete task context: SAP file path, context brief or proposal, preflight report, endpoint/metric definitions, data description, and relevant version/delta reports.

During evaluation, do not call `sap-writer`, `proposal-drafter`, `proposal-evaluator`, or review panel roles.

## Stop Conditions

- Missing `sap_file_path`.
- SAP file cannot be read.
- Input object is not SAP.
- Task asks for proposal novelty, impact, or overall proposal value.
- Missing preflight report prevents methodological risk assessment.
- Missing context prevents SAP alignment assessment.
- User asks evaluator to rewrite SAP.

If limited evaluation is still possible, state the scope limitation.

## Pitfalls

- Do not modify SAP.
- Do not treat statistical terminology as methodological rigor.
- Do not ignore endpoint-analysis mismatch.
- Do not ignore data-method mismatch.
- Do not treat missing data and sensitivity analysis as decorative.
- Do not relax hard gates to keep workflow moving.
- Do not assume sample size, variables, or model feasibility from unstated data.

## Verification

- Evaluation is SAP-only.
- Proposal novelty and impact were not scored.
- SAP dimensions were covered.
- Endpoint-analysis alignment and data-method fit were checked.
- Missing data and sensitivity analysis were checked.
- Clinical data readiness was checked when relevant.
- Clinical feature descriptives were checked when relevant.
- Prespecified versus post hoc/exploratory separation was checked.
- Hard gates and fatal flaws were checked.
- One decision was returned.
- SAP was not modified.

## References

- `references/rubric-sap-evaluation.md`: defines SAP evaluation dimensions, scoring anchors, and weights.
- `references/gates-sap-hard-gates.md`: defines minimum SAP gates and gate failure handling.
- `references/criteria-sap-fatal-flaws.md`: defines SAP fatal flaws and repairability.
- `references/policy-sap-re-evaluation.md`: defines SAP re-evaluation, version comparison, and `stop_no_gain`.
- `references/policy-endpoint-analysis-alignment.md`: defines endpoint, metric, analysis population, and primary analysis alignment checks.
- `references/policy-data-method-fit.md`: defines data type, data structure, and statistical method fit checks.
- `references/schema-sap-evaluation-report.md`: defines SAP evaluation report structure.
- `templates/template-sap-evaluation-report.md`: output template for SAP evaluation.
