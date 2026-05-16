# SAP Evaluation Report Schema

Use this schema as a structural checklist, not as executable code.

## Required Sections

- Metadata
  - sap_file_path
  - sap_version
  - proposal_file_path, if available
  - evaluator_role
  - evaluation_type
- Scope Check
  - object_evaluated
  - scope_match
  - limitations
- Scores
  - clarity
  - feasibility
  - completion
  - methodological_rigor
  - endpoint_analysis_alignment
  - data_method_fit
  - clinical_data_readiness
  - clinical_feature_descriptives
  - prespecification_discipline
  - missing_data_handling
  - sensitivity_robustness
  - reproducibility
- Hard Gates
  - gate_status
  - failed_gates
- Fatal Flaws
  - flaw
  - location
  - severity
  - repairability
- Findings
  - major_strengths
  - major_weaknesses
  - methodological_concerns
  - alignment_concerns
  - data_method_fit_concerns
  - clinical_data_concerns
  - clinical_feature_descriptive_concerns
  - prespecification_concerns
  - missing_data_concerns
  - sensitivity_analysis_concerns
  - reproducibility_concerns
- Decision
  - accept | revise | reject | stop_no_gain
  - rationale
- Revision Priorities
- Re-evaluation Notes, if applicable
