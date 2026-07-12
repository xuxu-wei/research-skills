---
name: sap-refinement-controller
description: "Plan targeted SAP revision after evaluation, route writing to sap-writer, preserve lineage, and require fresh evaluation."
---
# sap-refinement-controller

## When to Use

Use this skill when `sap-evaluator` returns `revise` for a SAP file and the issues are potentially repairable.

This skill controls the SAP revision loop. It does not write the SAP itself and does not evaluate its own revisions.

## Core Principles

- SAP revision must be file-centered around `sap_file_path` and `sap_version`.
- Every revision must target specific SAP evaluator findings.
- `sap-writer` performs SAP edits; this controller manages the revision plan, version lineage, delta report, and re-evaluation.
- Every revised SAP must be evaluated by a fresh isolated `sap-evaluator` subagent.
- Do not continue revising when endpoint, data structure, analysis population, or primary analysis route remains undefined.
- Default maximum SAP revision rounds: 2.

## Inputs

- `sap_file_path`
- `sap_version`
- SAP evaluation report
- methodology/statistics preflight report
- proposal context brief or linked proposal file
- endpoint, outcome, metric, and analysis population definitions
- available data description
- user goal and constraints
- previous SAP revision history, if any
- maximum SAP revision rounds, default 2

If `sap_file_path`, the SAP evaluation report, or the preflight report is missing, stop and return a missing-input report.

## Outputs

- SAP revision plan
- updated `sap_file_path`
- updated `sap_version`
- SAP revision delta report
- independent SAP re-evaluation report
- next decision: `accept`, `revise`, `reject`, or `stop_no_gain`
- unresolved SAP issues

## Procedure

### 1. Confirm Revision Eligibility

Continue only when the SAP evaluator decision is `revise`.

Stop when the evaluator reports an unrepairable fatal flaw, the preflight report blocks SAP work, or the requested revision requires inventing endpoint, sample size, analysis population, data structure, or statistical model details.

### 2. Build SAP Revision Plan

Group evaluator findings into:

- must-fix methodological issues;
- endpoint-analysis alignment issues;
- data-method fit issues;
- missing data or sensitivity analysis issues;
- reproducibility issues;
- issues requiring user or statistician confirmation.

For each fix, state the target SAP section, intended change, required source artifact, and whether the issue can be fixed without new user input.

### 3. Coordinate SAP Update

Hand the plan to `sap-writer` with:

- current `sap_file_path`;
- current `sap_version`;
- SAP evaluation report;
- SAP revision plan;
- preflight report;
- proposal/context references;
- required output: updated SAP file, change summary, and unresolved SAP issues.

`sap-writer` must preserve version lineage and must not declare the revised SAP accepted.

### 4. Require SAP Delta Report

After the update, produce or require a SAP delta report covering:

- evaluator concerns addressed;
- concerns not addressed;
- new assumptions introduced;
- changes to endpoint, analysis population, primary model, missing data, sensitivity analysis, or reproducibility plan;
- remaining issues needing human statistician review.

### 5. Delegate Independent Re-evaluation

Explicitly assign a new `sap-evaluator` instance to a fresh independent subagent or delegated thread. Do not re-use the prior evaluator or evaluate inline.

The re-evaluation brief must include the updated and previous frozen SAP files/versions, an anonymized prior must-fix issue list, SAP delta report, preflight report, endpoint/metric definitions, data description, and user constraints. It must exclude the prior scores, rationale, and decision.

### 6. Decide Loop Outcome

Use the independent SAP re-evaluation report to route:

- `accept`: return to `proposal-orchestrator` for package assembly or human statistician review.
- `revise`: continue only if below the maximum revision rounds and remaining issues are repairable.
- `reject`: stop when a fatal methodological flaw remains.
- `stop_no_gain`: stop when revisions improve wording but not endpoint-analysis alignment, data-method fit, or executable analysis detail.

### 7. Handoff

Return:

- current `sap_file_path`;
- current `sap_version`;
- latest SAP evaluation report;
- SAP revision delta report;
- SAP revision round count;
- unresolved SAP issues;
- recommended next step.

## Stop Conditions

- Missing SAP file path, SAP evaluation report, or preflight report.
- Preflight blocks SAP work.
- Key endpoint, analysis population, data structure, or primary analysis route remains undefined.
- Revision would require inventing statistical details.
- Maximum SAP revision rounds reached.
- Re-evaluation returns `reject` or `stop_no_gain`.

## Pitfalls

- Do not rewrite SAP content in this controller.
- Do not let `sap-writer` self-evaluate.
- Do not treat a more complete-looking SAP as methodologically valid.
- Do not continue adding statistical terminology when endpoint-analysis alignment is still broken.
- Do not package SAP materials as accepted when the latest SAP version has not been independently evaluated.

## Verification

- `sap_file_path` and `sap_version` are explicit.
- SAP evaluation report is present.
- Revision plan maps each action to evaluator findings.
- SAP delta report exists.
- Re-evaluation was performed by an isolated `sap-evaluator`.
- Next decision is explicit.
- Unresolved SAP issues are preserved.

## References

- `../sap-evaluator/references/policy-sap-re-evaluation.md`: governs SAP re-evaluation, version comparison, and `stop_no_gain`.
- `../sap-evaluator/references/policy-endpoint-analysis-alignment.md`: defines endpoint-analysis alignment checks used to prioritize SAP fixes.
- `../sap-evaluator/references/policy-data-method-fit.md`: defines data-method fit checks used to prioritize SAP fixes.
- `../sap-writer/references/policy-sap-file-maintenance.md`: governs SAP file paths, version lineage, change summaries, and unresolved SAP issues.
