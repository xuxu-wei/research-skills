#!/usr/bin/env python3
"""Generate the machine-auditable registry for the OpenAI research plugin."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
HERMES_SKILLS = REPO / "research-skills"

REVIEWERS = {
    "academic-language-assessor",
    "medical-journal-review",
    "methodology-statistics-preflight",
    "idea-evaluator",
    "idea-adversarial-review-panel",
    "proposal-readiness-triage",
    "proposal-evaluator",
    "proposal-review-panel",
    "sap-evaluator",
    "article-readiness-triage",
    "article-methods-statistics-auditor",
    "article-claim-auditor",
    "article-evaluator",
    "article-review-panel",
    "article-submission-compositor",
    "perspective-evaluator",
    "perspective-review-panel",
    "perspective-final-compositor",
}

VERIFIER_COMPOSITORS = {
    "article-submission-compositor",
    "perspective-final-compositor",
}

IMPLICIT = {
    "research-idea-orchestrator",
    "proposal-orchestrator",
    "article-orchestrator",
    "perspective-orchestrator",
    "research-opportunity-mapper",
    "academic-deep-search",
}

# workflow, source, destination, dispatch mode, trigger, input contract,
# output contract, failure route
WORKFLOW_EDGES = [
    ("idea", "research-idea-orchestrator", "research-context-builder", "orchestrated", "context_required", "user_inputs_and_constraints", "research_context_brief", "clarification_required"),
    ("idea", "research-idea-orchestrator", "research-opportunity-mapper", "orchestrated", "evidence_or_opportunity_map_required", "context_sources_and_scope", "evidence_and_opportunity_maps", "evidence_mapping_pending"),
    ("idea", "research-idea-orchestrator", "multi-path-idea-generator", "orchestrated", "context_and_opportunity_map_ready_or_revision_authorized", "frozen_context_opportunity_current_candidates_and_revision_plan", "versioned_candidate_set_and_delta", "generation_blocked"),
    ("idea", "research-idea-orchestrator", "methodology-statistics-preflight", "delegated", "method_or_endpoint_fit_needs_review", "frozen_candidates_and_method_facts", "preflight_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-evaluator", "delegated", "candidate_set_frozen_or_revised", "frozen_candidates_stable_rubric_and_facts", "idea_evaluation_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-adversarial-review-panel", "delegated", "proposal_handoff_candidate_exists", "frozen_promoted_candidates_and_role_brief", "sealed_individual_adversarial_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "academic-language-assessor", "delegated", "external_facing_portfolio_language_check", "frozen_portfolio_text_and_language_scope", "language_assessment_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-portfolio-assembler", "orchestrated", "evaluation_and_adversarial_reports_sealed", "evaluated_candidates_lineage_and_dissent", "pi_review_portfolio", "assembly_blocked"),
    ("idea", "research-idea-orchestrator", "proposal-orchestrator", "handoff", "proposal_handoff_gate_passed", "promoted_idea_package_and_limitations", "proposal_workflow_state", "proposal_handoff_blocked"),

    ("proposal", "proposal-orchestrator", "proposal-context-brief-builder", "orchestrated", "context_brief_required", "idea_draft_call_and_constraints", "proposal_context_brief", "clarification_required"),
    ("proposal", "proposal-orchestrator", "research-opportunity-mapper", "orchestrated", "broad_or_stale_evidence_required", "context_sources_and_retrieval_scope", "evidence_and_opportunity_maps", "evidence_mapping_pending"),
    ("proposal", "proposal-orchestrator", "proposal-readiness-triage", "delegated", "context_and_evidence_ready", "frozen_context_evidence_and_scope", "readiness_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "methodology-statistics-preflight", "delegated", "readiness_or_sap_requires_method_preflight", "frozen_design_endpoint_and_data_facts", "preflight_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-drafter", "orchestrated", "readiness_passed_or_targeted_revision_authorized", "approved_context_evidence_structure_or_revision_plan", "versioned_proposal", "drafting_blocked"),
    ("proposal", "proposal-orchestrator", "proposal-evaluator", "delegated", "proposal_version_frozen", "frozen_proposal_stable_rubric_and_facts", "proposal_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-refinement-controller", "orchestrated", "evaluation_or_panel_requests_fixable_revision", "sealed_findings_current_version_and_history", "revision_handoff", "revision_blocked"),
    ("proposal", "proposal-refinement-controller", "proposal-drafter", "orchestrated", "revision_plan_frozen", "current_proposal_and_targeted_revision_plan", "new_proposal_version_and_delta", "drafting_blocked"),
    ("proposal", "proposal-refinement-controller", "proposal-evaluator", "delegated", "revised_proposal_version_frozen", "latest_proposal_stable_rubric_facts_and_optional_anonymous_issues", "fresh_proposal_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "sap-writer", "orchestrated", "sap_requested_and_preflight_allows", "approved_design_endpoints_data_and_preflight", "versioned_sap", "sap_drafting_blocked"),
    ("proposal", "proposal-orchestrator", "sap-evaluator", "delegated", "sap_version_frozen", "frozen_sap_stable_rubric_and_facts", "sap_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "sap-refinement-controller", "orchestrated", "sap_evaluation_requests_revision", "sealed_sap_findings_and_current_version", "sap_revision_handoff", "sap_revision_blocked"),
    ("proposal", "sap-refinement-controller", "sap-writer", "orchestrated", "sap_revision_plan_frozen", "current_sap_and_targeted_plan", "new_sap_version_and_delta", "sap_drafting_blocked"),
    ("proposal", "sap-refinement-controller", "sap-evaluator", "delegated", "revised_sap_version_frozen", "latest_sap_stable_rubric_and_facts", "fresh_sap_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-review-panel", "delegated", "proposal_evaluation_passed_or_early_mock_explicit", "frozen_proposal_and_one_role_brief", "sealed_individual_panel_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "academic-language-assessor", "delegated", "final_proposal_language_check", "frozen_proposal_and_language_scope", "language_assessment_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-package-assembler", "orchestrated", "latest_version_has_qualifying_reviews", "evaluated_proposal_state_reviews_dissent_and_optional_sap", "human_review_proposal_package", "assembly_blocked"),

    ("article", "article-orchestrator", "article-readiness-triage", "delegated", "minimal_intake_frozen", "frozen_minimal_intake_and_entry_scope", "article_readiness_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-context-builder", "orchestrated", "readiness_allows_context_build", "approved_intake_and_scope", "article_context_brief", "clarification_required"),
    ("article", "article-orchestrator", "article-literature-grounder", "orchestrated", "context_ready_and_grounding_required", "context_sources_and_scope", "literature_grounding_report", "grounding_blocked"),
    ("article", "article-literature-grounder", "research-opportunity-mapper", "orchestrated", "broad_stale_or_conflicting_evidence", "research_question_sources_and_scope", "evidence_map_and_limitations", "evidence_mapping_pending"),
    ("article", "article-orchestrator", "article-architect", "orchestrated", "context_and_grounding_ready", "frozen_context_grounding_and_results", "article_blueprint_and_evidence_contracts", "architecture_blocked"),
    ("article", "article-orchestrator", "methodology-statistics-preflight", "delegated", "quick_method_feasibility_screen_needed", "frozen_design_endpoint_and_data_facts", "preflight_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-methods-statistics-auditor", "delegated", "blueprint_and_method_inputs_frozen", "frozen_context_protocol_outputs_and_scope", "methods_statistics_audit_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-drafter", "orchestrated", "architecture_and_method_gate_allow_drafting", "approved_blueprint_evidence_audit_and_revision_plan", "versioned_manuscript_and_supplements", "drafting_blocked"),
    ("article", "article-orchestrator", "article-claim-auditor", "delegated", "manuscript_version_frozen", "frozen_manuscript_claim_matrix_and_evidence", "claim_audit_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-evaluator", "delegated", "manuscript_version_frozen_or_revised", "frozen_manuscript_stable_rubric_and_facts", "article_evaluation_report", "independent_review_pending"),
    ("article", "article-orchestrator", "academic-language-assessor", "delegated", "language_check_required", "frozen_manuscript_and_language_scope", "language_assessment_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-refinement-controller", "orchestrated", "audit_evaluation_or_panel_requests_fixable_revision", "sealed_findings_current_version_and_history", "revision_handoff", "revision_blocked"),
    ("article", "article-refinement-controller", "article-drafter", "orchestrated", "revision_plan_frozen", "current_manuscript_and_targeted_plan", "new_manuscript_version_and_delta", "drafting_blocked"),
    ("article", "article-refinement-controller", "article-evaluator", "delegated", "revised_manuscript_version_frozen", "latest_manuscript_stable_rubric_facts_and_optional_anonymous_issues", "fresh_article_evaluation_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-review-panel", "delegated", "article_evaluation_passed_or_mock_review_explicit", "frozen_manuscript_and_one_role_brief", "sealed_individual_panel_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-frontmatter-drafter", "orchestrated", "evaluated_manuscript_ready_for_delivery", "frozen_manuscript_blueprint_and_journal_adapter", "versioned_frontmatter", "frontmatter_blocked"),
    ("article", "article-orchestrator", "article-cover-letter", "orchestrated", "frontmatter_and_manuscript_ready", "frozen_manuscript_frontmatter_and_journal_adapter", "cover_letter_and_quality_check", "cover_letter_blocked"),
    ("article", "article-orchestrator", "medical-journal-review", "delegated", "biomedical_cover_letter_review_required", "frozen_cover_letter_and_scope", "medical_journal_review_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-submission-compositor", "delegated", "all_required_artifacts_and_reviews_frozen", "frozen_submission_artifacts_reviews_and_dissent", "verified_human_review_package", "independent_review_pending"),

    ("perspective", "perspective-orchestrator", "perspective-input-builder", "orchestrated", "input_brief_required", "user_thesis_outlet_evidence_and_constraints", "perspective_input_brief", "clarification_required"),
    ("perspective", "perspective-orchestrator", "perspective-claim-evidence-curator", "orchestrated", "input_brief_ready_or_claim_change_approved", "frozen_input_evidence_and_change_requests", "claim_ledger_and_evidence_artifacts", "curation_blocked"),
    ("perspective", "perspective-orchestrator", "research-opportunity-mapper", "orchestrated", "standard_or_full_mode_has_broad_evidence_gap", "claims_sources_and_retrieval_scope", "evidence_map_and_limitations", "evidence_mapping_pending"),
    ("perspective", "perspective-orchestrator", "perspective-argument-architect", "orchestrated", "claim_and_evidence_artifacts_ready", "frozen_input_claims_evidence_and_outlet", "argument_skeleton_and_paragraph_plan", "architecture_blocked"),
    ("perspective", "perspective-orchestrator", "perspective-drafter", "orchestrated", "argument_architecture_ready_or_revision_plan_frozen", "approved_architecture_claims_and_revision_plan", "versioned_perspective_and_paragraph_map", "drafting_blocked"),
    ("perspective", "perspective-orchestrator", "perspective-evaluator", "delegated", "perspective_version_frozen_or_revised", "frozen_perspective_stable_rubric_and_facts", "perspective_evaluation_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-refinement-controller", "orchestrated", "evaluation_or_panel_requests_fixable_revision", "sealed_findings_current_version_and_history", "revision_handoff", "revision_blocked"),
    ("perspective", "perspective-refinement-controller", "perspective-drafter", "orchestrated", "revision_plan_frozen", "current_perspective_and_targeted_plan", "new_perspective_version_and_delta", "drafting_blocked"),
    ("perspective", "perspective-refinement-controller", "perspective-evaluator", "delegated", "revised_perspective_version_frozen", "latest_perspective_stable_rubric_facts_and_optional_anonymous_issues", "fresh_perspective_evaluation_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-review-panel", "delegated", "perspective_evaluation_passed", "frozen_perspective_and_one_role_brief", "sealed_individual_panel_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "academic-language-assessor", "delegated", "final_perspective_language_check", "frozen_perspective_and_language_scope", "language_assessment_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "medical-journal-review", "delegated", "biomedical_journal_review_required", "frozen_perspective_and_journal_scope", "medical_journal_review_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-final-compositor", "delegated", "all_required_artifacts_and_reviews_frozen", "frozen_final_artifacts_reviews_and_dissent", "verified_human_review_package", "independent_review_pending"),
]

WORKFLOW_STATE_POLICY = {
    "state_field": "workflow_state",
    "active_states": [
        "initialized",
        "preprocessing",
        "artifact_frozen",
        "revision_required",
        "panel_pending",
        "packaging_pending",
    ],
    "pause_states": ["pending_review", "independent_review_pending"],
    "terminal_states": ["stopped", "blocked", "human_signoff_required"],
    "review_unavailable_state": "independent_review_pending",
    "fatal_finding_state": "blocked",
    "final_handoff_state": "human_signoff_required",
    "wildcard_transition_scope": "nonterminal_states_only",
    "resume_policy": {
        "independent_review_pending": "pending_review",
    },
    "version_gate": {
        "changed_artifact_requires_new_version": True,
        "evaluator_instance_must_be_fresh": True,
        "evaluated_version_must_equal_current_version": True,
        "prior_scores_visible_to_fresh_evaluator": False,
        "required_before_states": ["panel_pending", "packaging_pending", "human_signoff_required"],
    },
    "finding_gate": {
        "fatal_or_blocking_finding_prevents_accept": True,
        "fatal_or_blocking_finding_prevents_promoted": True,
        "fatal_or_blocking_finding_prevents_human_signoff": True,
        "panel_dissent_must_remain_visible": True,
    },
    "concurrency_policy": {
        "phase_level_delegation_allowed": True,
        "single_writer_per_source_artifact": True,
        "concurrent_writes_to_same_source_artifact": False,
        "reviewer_inputs_read_only": True,
        "panel_reviewers_may_run_concurrently": True,
    },
    "lifecycle_transitions": [
        {"from": "initialized", "to": "preprocessing", "trigger": "entry_gate_passed"},
        {"from": "preprocessing", "to": "artifact_frozen", "trigger": "versioned_artifact_created"},
        {"from": "artifact_frozen", "to": "pending_review", "trigger": "independent_review_dispatched"},
        {"from": "pending_review", "to": "revision_required", "trigger": "fixable_revision_requested"},
        {"from": "revision_required", "to": "artifact_frozen", "trigger": "new_version_created"},
        {
            "from": "pending_review",
            "to": "panel_pending",
            "trigger": "latest_version_accepted",
            "requires": ["fresh_evaluation_current", "no_unresolved_fatal_finding"],
        },
        {
            "from": "pending_review",
            "to": "packaging_pending",
            "trigger": "panel_patch_latest_version_accepted",
            "requires": ["prior_panel_complete", "patch_scope_minor", "fresh_evaluation_current", "no_unresolved_fatal_finding"],
        },
        {
            "from": "panel_pending",
            "to": "revision_required",
            "trigger": "panel_requests_substantive_change",
            "requires": ["prior_panel_complete", "fresh_evaluation_current"],
        },
        {
            "from": "panel_pending",
            "to": "packaging_pending",
            "trigger": "panel_gate_passed",
            "requires": ["prior_panel_complete", "fresh_evaluation_current", "no_unresolved_fatal_finding"],
        },
        {"from": "packaging_pending", "to": "human_signoff_required", "trigger": "package_verified"},
        {"from": "*", "to": "independent_review_pending", "trigger": "required_reviewer_unavailable"},
        {"from": "*", "to": "blocked", "trigger": "fatal_or_blocking_finding"},
        {"from": "*", "to": "stopped", "trigger": "unfixable_no_gain_or_user_stop"},
        {"from": "independent_review_pending", "to": "pending_review", "trigger": "reviewer_delegation_resumed"},
    ],
}

WORKFLOW_STATE_MACHINES = {
    "idea": {
        "orchestrator": "research-idea-orchestrator",
        "evaluator_skill": "idea-evaluator",
        "primary_artifact_type": "candidate_idea_set",
        "entry_modes": ["standard", "resume_candidates", "portfolio_only"],
        "entry_gates": {
            "standard": ["context_frozen", "evidence_map_frozen", "candidate_set_versioned"],
            "resume_candidates": ["context_scope_validated", "evidence_scope_validated", "candidate_set_versioned"],
            "portfolio_only": ["latest_version_independently_evaluated", "adversarial_reports_complete", "dissent_and_fatal_findings_indexed"],
        },
        "scenario_entry_gate_contracts": {
            "standard": {
                "context_frozen": {"artifact_roles": ["research_context"]},
                "evidence_map_frozen": {"artifact_roles": ["evidence_map"]},
                "candidate_set_versioned": {"artifact_roles": ["candidate_idea_set"]},
            },
        },
        "before_panel": ["latest_version_independently_evaluated", "no_unresolved_fatal_finding"],
        "before_packaging": ["latest_version_independently_evaluated", "adversarial_reports_complete", "dissent_and_fatal_findings_indexed"],
        "non_ready_modes": [],
        "final_package_skill": "idea-portfolio-assembler",
    },
    "proposal": {
        "orchestrator": "proposal-orchestrator",
        "evaluator_skill": "proposal-evaluator",
        "primary_artifact_type": "proposal",
        "entry_modes": ["standard", "existing_draft", "draft_and_external_review", "package_only"],
        "entry_gates": {
            "standard": ["context_frozen", "readiness_passed", "proposal_versioned"],
            "existing_draft": ["minimal_state_created", "scope_limitations_recorded", "proposal_versioned"],
            "draft_and_external_review": ["minimal_state_created", "proposal_versioned", "external_review_qualified_or_fresh_evaluation_required"],
            "package_only": ["latest_version_independently_evaluated", "required_panel_reports_complete", "dissent_and_fatal_findings_indexed"],
        },
        "scenario_entry_gate_contracts": {
            "standard": {
                "context_frozen": {"artifact_roles": ["proposal_context"]},
                "readiness_passed": {
                    "review_skill": "proposal-readiness-triage",
                    "input_artifact_roles": ["proposal_context", "evidence_map"],
                },
                "proposal_versioned": {"artifact_roles": ["proposal"]},
            },
        },
        "before_panel": ["latest_version_independently_evaluated", "no_unresolved_fatal_finding"],
        "before_packaging": ["latest_version_independently_evaluated", "required_panel_reports_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
        "non_ready_modes": [],
        "final_package_skill": "proposal-package-assembler",
    },
    "article": {
        "orchestrator": "article-orchestrator",
        "evaluator_skill": "article-evaluator",
        "primary_artifact_type": "manuscript",
        "entry_modes": ["standard", "fast_track_draft", "fast_track_draft_and_evaluation", "blueprint_only", "section_specific", "submission_only"],
        "entry_gates": {
            "standard": ["readiness_passed", "context_frozen", "methods_gate_passed", "manuscript_versioned", "claim_audit_passed"],
            "fast_track_draft": ["readiness_passed", "minimal_backfill_validated", "manuscript_versioned", "claim_audit_passed"],
            "fast_track_draft_and_evaluation": ["readiness_passed", "manuscript_versioned", "external_review_qualified_or_fresh_evaluation_required"],
            "blueprint_only": ["readiness_passed", "context_frozen", "methods_gate_passed"],
            "section_specific": ["scoped_intake_frozen", "minimal_context_frozen"],
            "submission_only": ["submission_scope_readiness_passed", "manuscript_versioned", "latest_version_independently_evaluated"],
        },
        "scenario_entry_gate_contracts": {
            "standard": {
                "readiness_passed": {
                    "review_skill": "article-readiness-triage",
                    "input_artifact_roles": ["minimal_intake"],
                },
                "context_frozen": {"artifact_roles": ["article_context"]},
                "methods_gate_passed": {
                    "review_skill": "article-methods-statistics-auditor",
                    "input_artifact_roles": ["article_context", "method_facts"],
                },
                "manuscript_versioned": {"artifact_roles": ["manuscript"]},
                "claim_audit_passed": {
                    "review_skill": "article-claim-auditor",
                    "input_artifact_roles": [
                        "article_context",
                        "article_blueprint",
                        "claim_evidence_matrix",
                        "evidence_ledger",
                        "manuscript",
                    ],
                },
            },
        },
        "before_panel": ["latest_version_independently_evaluated", "claim_audit_passed", "no_unresolved_fatal_finding"],
        "before_packaging": ["latest_version_independently_evaluated", "required_panel_reports_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
        "non_ready_modes": ["blueprint_only", "section_specific"],
        "final_package_skill": "article-submission-compositor",
    },
    "perspective": {
        "orchestrator": "perspective-orchestrator",
        "evaluator_skill": "perspective-evaluator",
        "primary_artifact_type": "perspective",
        "entry_modes": ["lite", "standard", "full"],
        "entry_gates": {
            "lite": ["input_brief_frozen", "provisional_claims_frozen", "argument_architecture_frozen"],
            "standard": ["input_brief_frozen", "claim_evidence_artifacts_frozen", "argument_architecture_frozen", "perspective_versioned"],
            "full": ["input_brief_frozen", "claim_evidence_artifacts_frozen", "argument_architecture_frozen", "perspective_versioned"],
        },
        "scenario_entry_gate_contracts": {
            "full": {
                "input_brief_frozen": {"artifact_roles": ["perspective_input_brief"]},
                "claim_evidence_artifacts_frozen": {"artifact_roles": ["claim_ledger", "claim_evidence_matrix"]},
                "argument_architecture_frozen": {"artifact_roles": ["argument_architecture", "paragraph_map"]},
                "perspective_versioned": {"artifact_roles": ["perspective"]},
            },
        },
        "before_panel": ["latest_version_independently_evaluated", "no_unresolved_fatal_finding"],
        "before_packaging": ["latest_version_independently_evaluated", "panel_reports_complete", "dissent_and_fatal_findings_indexed"],
        "non_ready_modes": ["lite", "standard"],
        "final_package_skill": "perspective-final-compositor",
    },
}

REVIEW_DECISION_CONTRACTS = {
    "academic-language-assessor": {
        "allowed": ["submission_ready", "minor_language_revision", "major_language_revision", "needs_professional_editing"],
        "pass": ["submission_ready"],
        "revise": ["minor_language_revision", "major_language_revision"],
        "stop": ["needs_professional_editing"],
    },
    "medical-journal-review": {
        "allowed": ["support", "support_with_minor_revision", "major_revision_required", "redesign_required", "not_reviewable_with_current_materials", "fatal_flaw"],
        "pass": ["support"],
        "revise": ["support_with_minor_revision", "major_revision_required", "redesign_required"],
        "stop": ["not_reviewable_with_current_materials", "fatal_flaw"],
    },
    "methodology-statistics-preflight": {
        "allowed": ["pass", "revise_endpoint_or_metric", "revise_data_source", "revise_method", "revise_analysis_route", "needs_clarification", "blocked", "out_of_scope"],
        "pass": ["pass"],
        "revise": ["revise_endpoint_or_metric", "revise_data_source", "revise_method", "revise_analysis_route", "needs_clarification"],
        "stop": ["blocked", "out_of_scope"],
    },
    "idea-evaluator": {
        "allowed": ["promote", "revise_then_promote", "revise", "reframe", "merge", "keep_as_backup", "reject"],
        "pass": ["promote"],
        "revise": ["revise_then_promote", "revise", "reframe", "merge"],
        "stop": ["keep_as_backup", "reject"],
    },
    "idea-adversarial-review-panel": {
        "allowed": ["handoff_ready", "conditional_handoff", "return_to_evidence_mapping", "return_to_methodology_preflight", "return_to_generation_or_reframe", "return_to_independent_evaluation", "do_not_handoff"],
        "pass": ["handoff_ready", "conditional_handoff"],
        "revise": ["return_to_evidence_mapping", "return_to_methodology_preflight", "return_to_generation_or_reframe", "return_to_independent_evaluation"],
        "stop": ["do_not_handoff"],
    },
    "proposal-readiness-triage": {
        "allowed": ["ready_for_proposal", "needs_clarification", "needs_idea_refinement", "needs_methodology_preflight", "not_proposalizable_yet"],
        "pass": ["ready_for_proposal"],
        "revise": ["needs_clarification", "needs_idea_refinement", "needs_methodology_preflight"],
        "stop": ["not_proposalizable_yet"],
    },
    "proposal-evaluator": {
        "allowed": ["accept", "revise", "reject"],
        "pass": ["accept"],
        "revise": ["revise"],
        "stop": ["reject"],
    },
    "proposal-review-panel": {
        "allowed": ["strong_support", "support_with_minor_revision", "support_after_major_revision", "revise_and_resubmit", "not_ready", "reject_or_redesign"],
        "pass": ["strong_support"],
        "revise": ["support_with_minor_revision", "support_after_major_revision", "revise_and_resubmit"],
        "stop": ["not_ready", "reject_or_redesign"],
    },
    "sap-evaluator": {
        "allowed": ["accept", "revise", "reject"],
        "pass": ["accept"],
        "revise": ["revise"],
        "stop": ["reject"],
    },
    "article-readiness-triage": {
        "allowed": ["ready", "conditionally_ready", "not_ready", "wrong_article_type"],
        "pass": ["ready", "conditionally_ready"],
        "revise": [],
        "stop": ["not_ready", "wrong_article_type"],
    },
    "article-methods-statistics-auditor": {
        "allowed": ["pass", "conditionally_pass_with_author_verification", "requires_methods_clarification", "requires_reanalysis", "methodologically_blocked"],
        "pass": ["pass", "conditionally_pass_with_author_verification", "requires_methods_clarification"],
        "revise": [],
        "stop": ["requires_reanalysis", "methodologically_blocked"],
    },
    "article-claim-auditor": {
        "allowed": ["pass", "downscale_and_proceed", "revise_and_reaudit", "blocked"],
        "pass": ["pass", "downscale_and_proceed"],
        "revise": ["revise_and_reaudit"],
        "stop": ["blocked"],
    },
    "article-evaluator": {
        "allowed": ["accept", "revise", "reject"],
        "pass": ["accept"],
        "revise": ["revise"],
        "stop": ["reject"],
    },
    "article-review-panel": {
        "allowed": ["strong_support", "support_with_minor_revision", "support_after_major_revision", "revise_and_resubmit", "not_ready", "reject_or_redesign"],
        "pass": ["strong_support"],
        "revise": ["support_with_minor_revision", "support_after_major_revision", "revise_and_resubmit"],
        "stop": ["not_ready", "reject_or_redesign"],
    },
    "article-submission-compositor": {
        "allowed": ["human_signoff_required", "blocked", "stopped", "independent_review_pending"],
        "pass": ["human_signoff_required"],
        "revise": [],
        "stop": ["blocked", "stopped", "independent_review_pending"],
    },
    "perspective-evaluator": {
        "allowed": ["accept", "minor_revision", "major_revision_draft", "argument_rebuild", "thesis_redesign", "evidence_rebuild", "outlet_retarget", "reject_not_salvageable"],
        "pass": ["accept"],
        "revise": ["minor_revision", "major_revision_draft", "argument_rebuild", "thesis_redesign", "evidence_rebuild", "outlet_retarget"],
        "stop": ["reject_not_salvageable"],
    },
    "perspective-review-panel": {
        "allowed": ["strong_support", "support_with_minor_revision", "support_after_major_revision", "not_ready", "reject_or_redesign"],
        "pass": ["strong_support"],
        "revise": ["support_with_minor_revision", "support_after_major_revision"],
        "stop": ["not_ready", "reject_or_redesign"],
    },
    "perspective-final-compositor": {
        "allowed": ["human_signoff_required", "blocked", "stopped", "independent_review_pending"],
        "pass": ["human_signoff_required"],
        "revise": [],
        "stop": ["blocked", "stopped", "independent_review_pending"],
    },
}

PACKAGE_INPUT_CONTRACTS = {
    "idea": {
        "allowed_roles": ["research_context", "evidence_map", "candidate_idea_set", "evaluation_report", "panel_report", "revision_plan", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "research_context", "count": 1},
            {"artifact_role": "evidence_map", "count": 1},
            {"artifact_role": "candidate_idea_set", "current_primary": True, "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "idea-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "idea-adversarial-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "revision_plan", "source_skill": "research-idea-orchestrator", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "multi-path-idea-generator", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "proposal": {
        "allowed_roles": ["proposal_context", "readiness_report", "proposal", "evaluation_report", "preflight_report", "sap", "panel_report", "revision_plan", "response_to_reviewers", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "proposal_context", "count": 1},
            {"artifact_role": "readiness_report", "source_skill": "proposal-readiness-triage", "count": 1},
            {"artifact_role": "proposal", "current_primary": True, "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "proposal-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "preflight_report", "source_skill": "methodology-statistics-preflight", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "sap", "source_skill": "sap-writer", "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "sap-evaluator", "selected_artifact_lineage_role": "sap", "count": 1},
            {"artifact_role": "panel_report", "source_skill": "proposal-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "revision_plan", "source_skill": "proposal-refinement-controller", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "response_to_reviewers", "source_skill": "proposal-drafter", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "proposal-drafter", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "article": {
        "allowed_roles": ["manuscript", "article_blueprint", "claim_evidence_matrix", "evidence_ledger", "evaluation_report", "audit_report", "panel_report", "journal_adapter", "frontmatter", "cover_letter", "quality_check", "revision_plan", "response_to_reviewers", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "manuscript", "current_primary": True, "count": 1},
            {"artifact_role": "article_blueprint", "count": 1},
            {"artifact_role": "claim_evidence_matrix", "count": 1},
            {"artifact_role": "evidence_ledger", "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "article-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "audit_report", "source_skill": "article-methods-statistics-auditor", "count": 1},
            {"artifact_role": "audit_report", "source_skill": "article-claim-auditor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "article-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "journal_adapter", "count": 1},
            {"artifact_role": "frontmatter", "count": 1},
            {"artifact_role": "cover_letter", "count": 1},
            {"artifact_role": "quality_check", "count": 1},
            {"artifact_role": "revision_plan", "source_skill": "article-refinement-controller", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "response_to_reviewers", "source_skill": "article-drafter", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "article-drafter", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "perspective": {
        "allowed_roles": ["perspective", "target_outlet_profile", "claim_ledger", "claim_evidence_matrix", "evidence_limitations", "citation_risk_log", "contrary_evidence_log", "reference_list", "panel_summary", "artifact_index"],
        "required_inputs": [
            {"artifact_role": "perspective", "current_primary": True, "count": 1},
            {"artifact_role": "target_outlet_profile", "count": 1},
            {"artifact_role": "claim_ledger", "count": 1},
            {"artifact_role": "claim_evidence_matrix", "count": 1},
            {"artifact_role": "evidence_limitations", "count": 1},
            {"artifact_role": "citation_risk_log", "count": 1},
            {"artifact_role": "contrary_evidence_log", "count": 1},
            {"artifact_role": "reference_list", "count": 1},
            {"artifact_role": "panel_summary", "sealed_review_lineage": True, "count": 1},
            {"artifact_role": "artifact_index", "sealed_review_lineage": True, "count": 1},
        ],
    },
}

PANEL_CONTRACTS = {
    "idea": {
        "default_tier": "default_three",
        "modes": ["blind_handoff_review"],
        "tiers": {
            "default_three": ["novelty-gap", "feasibility-method", "pi-strategy"],
        },
        "mandatory_roles": ["novelty-gap", "feasibility-method", "pi-strategy"],
        "mode_forbidden_input_roles": {
            "blind_handoff_review": ["research_context", "evidence_map", "evaluation_report", "panel_report"],
        },
    },
    "proposal": {
        "default_tier": "standard_panel",
        "modes": ["blind_mock_review", "context_aware_internal_review"],
        "tiers": {
            "lightweight_panel": ["domain", "methodology-statistics", "submission-guard"],
            "standard_panel": ["broad-field", "domain", "methodology-statistics", "skeptical", "submission-guard"],
            "full_panel": ["broad-field", "domain", "methodology-statistics", "skeptical", "submission-guard", "cross-disciplinary-senior", "translational-end-user"],
        },
        "mandatory_roles": ["submission-guard"],
        "mode_forbidden_input_roles": {
            "blind_mock_review": ["proposal_context", "readiness_report", "evidence_map", "evaluation_report", "revision_plan", "revision_delta", "response_to_reviewers", "panel_report"],
            "context_aware_internal_review": ["evaluation_report", "panel_report"],
        },
        "minor_revision_decisions": ["support_with_minor_revision"],
        "substantive_revision_decisions": ["support_after_major_revision", "revise_and_resubmit"],
    },
    "article": {
        "default_tier": "lightweight_panel",
        "modes": ["blind_external_simulation"],
        "tiers": {
            "lightweight_panel": ["methodology-statistics", "evidence-claim", "submission-guard"],
            "standard_panel": ["methodology-statistics", "evidence-claim", "submission-guard", "clinical-domain-significance", "clarity-language"],
            "full_panel": ["methodology-statistics", "evidence-claim", "submission-guard", "clinical-domain-significance", "clarity-language", "internal-diagnostic-methodology", "evidence-retrieval-completeness"],
        },
        "mandatory_roles": ["submission-guard"],
        "mode_forbidden_input_roles": {
            "blind_external_simulation": ["article_context", "audit_report", "evaluation_report", "revision_plan", "revision_delta", "response_to_reviewers", "panel_report"],
        },
        "minor_revision_decisions": ["support_with_minor_revision"],
        "substantive_revision_decisions": ["support_after_major_revision", "revise_and_resubmit"],
    },
    "perspective": {
        "default_tier": "default_three",
        "modes": ["blind_external_simulation"],
        "tiers": {
            "default_three": ["counter-position", "evidence", "narrative"],
        },
        "mandatory_roles": ["counter-position", "evidence", "narrative"],
        "mode_forbidden_input_roles": {
            "blind_external_simulation": ["evaluation_report", "revision_plan", "revision_delta", "response_to_reviewers", "panel_report"],
        },
        "minor_revision_decisions": ["support_with_minor_revision"],
        "substantive_revision_decisions": ["support_after_major_revision"],
    },
}

SCENARIO_EVAL_CONTRACT = {
    "fixture_schema_version": 2,
    "required_workflows": ["idea", "proposal", "article", "perspective"],
    "required_lineage_fields": [
        "artifact_id",
        "version_id",
        "workflow_id",
        "round_id",
        "plugin_version",
        "source_skill",
        "created_by_instance_id",
        "based_on",
        "change_type",
        "path",
        "status",
        "content_digest",
        "frozen",
    ],
    "required_dispatch_fields": [
        "event_id",
        "source_skill",
        "destination_skill",
        "dispatch_mode",
        "trigger",
        "actor_instance_id",
        "allowed_read_paths",
        "allowed_write_paths",
        "input_artifact_ids",
        "input_versions",
    ],
    "required_review_fields": [
        "review_id",
        "reviewer_skill",
        "reviewer_instance_id",
        "reviewer_role",
        "review_scope",
        "workflow_id",
        "round_id",
        "input_artifact_ids",
        "input_versions",
        "files_read",
        "isolation_mode",
        "prior_scores_visible",
        "source_edits_performed",
        "decision",
        "findings",
        "unresolved_issues",
    ],
    "runtime_observation_fields": [
        "files_read",
        "actual_write_paths",
        "input_hashes_before",
        "input_hashes_after",
    ],
    "write_scope_policy": {
        "allowed_writes_are_exact_event_paths": True,
        "actual_writes_must_be_subset_of_allowed_writes": True,
        "input_artifacts_must_remain_hash_identical": True,
        "delegate_brief_paths_are_read_only": True,
    },
    "blindness_policy": {
        "forbidden_input_roles_for_evaluator_or_panel": [
            "parent_hidden_reasoning",
            "evaluation_report",
            "prior_evaluation",
            "prior_decision",
            "panel_report",
            "peer_review",
        ],
        "final_verifier_may_read_sealed_review_reports": True,
        "panel_peer_outputs_visible": False,
    },
    "reviewer_isolation_mode": "fresh_subagent",
    "reviewer_source_edits_allowed": False,
    "prior_scores_visible_to_fresh_reviewer": False,
    "reviewer_instance_must_differ_from_artifact_writer": True,
    "panel_role_instance_mapping_must_be_one_to_one": True,
    "review_decision_contracts": REVIEW_DECISION_CONTRACTS,
    "panel_contracts": PANEL_CONTRACTS,
    "package_input_contracts": PACKAGE_INPUT_CONTRACTS,
    "revision_artifact_contract": {
        "controller_output_role": "revision_plan",
        "drafter_required_output_roles": ["response_to_reviewers", "revision_delta"],
    },
    "verifier_compositor_outputs": {
        "article-submission-compositor": ["verification_report", "final_handoff_package"],
        "perspective-final-compositor": ["verification_report", "final_handoff_package"],
    },
    "final_state": "human_signoff_required",
    "automatic_external_submission": False,
}

CONTEXT_PROFILE_POLICY = {
    "measurement_unit": "characters",
    "interpretation": "conservative_initial-load_proxy_not_model_token_accounting",
    "initial_load_components": ["all_skill_descriptions", "selected_orchestrator_body"],
    "profiles": {
        "standard_32k": {
            "total_character_budget": 32000,
            "minimum_working_reserve": 16000,
            "sufficient_behavior": "continue_current_phase",
        },
        "degraded_16k": {
            "total_character_budget": 16000,
            "minimum_working_reserve": 4000,
            "insufficient_behavior": "context_handoff_required",
        },
    },
    "continuation_required_fields": [
        "workflow_id",
        "plugin_version",
        "entry_mode",
        "current_stage",
        "round_id",
        "runtime_status",
        "suspended_workflow_state",
        "current_artifact_id",
        "current_artifact_version",
        "current_artifact_path",
        "current_artifact_digest",
        "latest_qualifying_evaluation",
        "gate_receipts",
        "unresolved_finding_ids",
        "dissent_ids",
        "pending_edge",
        "isolation_requirements",
        "next_route",
    ],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def skill_name(path: Path) -> str:
    match = re.search(r"^name:\s*[\"']?([^\r\n\"']+)", read(path), re.M)
    if not match:
        raise ValueError(f"Missing skill name: {path}")
    return match.group(1).strip()


def related_skills(source_skill: Path, installed: set[str]) -> list[str]:
    if not source_skill.exists():
        return []
    text = read(source_skill)
    frontmatter_end = text.find("\n---", 4)
    frontmatter = text[4:frontmatter_end] if frontmatter_end >= 0 else ""
    match = re.search(
        r"^\s*related_skills:\s*(?:\[([^\]]*)\]|\n((?:\s+-[^\n]*\n?)+))",
        frontmatter,
        re.M,
    )
    if not match:
        return []
    if match.group(1) is not None:
        values = [item.strip().strip("'\"") for item in match.group(1).split(",")]
    else:
        values = re.findall(r"^\s+-\s+([A-Za-z0-9_-]+)\s*$", match.group(2), re.M)
    return sorted({value for value in values if value in installed})


def role_for(name: str) -> str:
    if name in REVIEWERS:
        return "reviewer"
    if name.endswith("orchestrator"):
        return "orchestrator"
    if "assembler" in name:
        return "assembler"
    if "refinement-controller" in name:
        return "controller"
    if "drafter" in name or name.endswith("writer"):
        return "drafter"
    if "generator" in name:
        return "generator"
    if name in {"research-opportunity-mapper", "academic-deep-search"}:
        return "retrieval"
    if any(token in name for token in ("builder", "curator", "architect", "grounder", "cover-letter")):
        return "builder"
    return "utility"


def io_contract(role: str) -> tuple[str, str]:
    contracts = {
        "reviewer": ("frozen_artifacts_and_review_brief", "review_or_verification_report"),
        "orchestrator": ("user_inputs_and_existing_workflow_artifacts", "workflow_state_and_final_handoff"),
        "assembler": ("evaluated_artifacts_and_workflow_state", "final_handoff_package"),
        "controller": ("evaluation_findings_and_current_artifact", "revision_plan_delta_and_routing"),
        "drafter": ("approved_context_evidence_and_revision_plan", "versioned_draft_artifact"),
        "generator": ("context_and_opportunity_artifacts", "candidate_artifact_set"),
        "retrieval": ("research_question_source_scope_and_existing_evidence", "source_grounded_retrieval_artifact"),
        "builder": ("approved_upstream_artifacts", "structured_builder_artifact"),
        "utility": ("task_specific_inputs", "task_specific_artifact"),
    }
    return contracts[role]


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> int:
    skill_files = sorted(SKILLS.rglob("SKILL.md"))
    names = {skill_name(path) for path in skill_files}
    if len(skill_files) != 45 or len(names) != 45:
        raise RuntimeError(f"Expected 45 unique skills, found {len(skill_files)} files and {len(names)} names")
    if not REVIEWERS <= names:
        raise RuntimeError(f"Reviewer registry references missing skills: {sorted(REVIEWERS - names)}")
    hermes_by_name = {
        skill_name(path): path
        for path in HERMES_SKILLS.rglob("SKILL.md")
        if skill_name(path) in names
    }
    missing_sources = names - set(hermes_by_name)
    if missing_sources:
        raise RuntimeError(f"Missing Hermes lineage sources: {sorted(missing_sources)}")
    manifest = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
    plugin_version = str(manifest["version"])

    lines = [
        "schema_version: 5",
        f"plugin_version: {quote(plugin_version)}",
        "review_execution:",
        "  isolation_mode: fresh_subagent",
        "  inline_fallback: false",
        "  prior_scores_visible_to_reviewer: false",
        "  source_artifacts_read_only: true",
        "skills:",
    ]
    for skill_md in skill_files:
        name = skill_name(skill_md)
        source_skill = hermes_by_name[name]
        source_relative = source_skill.parent.relative_to(HERMES_SKILLS)
        package = source_relative.parts[0]
        role = role_for(name)
        allowed_inputs, output = io_contract(role)
        if name in VERIFIER_COMPOSITORS:
            output = "verification_report_and_final_handoff_package"
        related = related_skills(source_skill, names)
        lines.extend(
            [
                f"  - name: {quote(name)}",
                f"    package: {quote(package)}",
                f"    role: {quote(role)}",
                f"    related_skills: [{', '.join(quote(item) for item in related)}]",
                f"    invocation_policy: {quote('implicit' if name in IMPLICIT else 'explicit_or_orchestrated')}",
                f"    requires_independent_subagent: {'true' if name in REVIEWERS else 'false'}",
                f"    allowed_input_artifacts: {quote(allowed_inputs)}",
                f"    output_artifact_type: {quote(output)}",
            ]
        )

    lines.append("workflow_edges:")
    for workflow, source, destination, dispatch, trigger, input_contract, output_contract, failure_route in WORKFLOW_EDGES:
        if source not in names or destination not in names:
            raise RuntimeError(f"Workflow edge references missing skill: {source} -> {destination}")
        lines.extend(
            [
                f"  - workflow: {quote(workflow)}",
                f"    source: {quote(source)}",
                f"    destination: {quote(destination)}",
                f"    dispatch_mode: {quote(dispatch)}",
                f"    trigger: {quote(trigger)}",
                f"    input_contract: {quote(input_contract)}",
                f"    output_contract: {quote(output_contract)}",
                f"    failure_route: {quote(failure_route)}",
            ]
        )

    state_registry = {
        "workflow_state_policy": WORKFLOW_STATE_POLICY,
        "workflow_state_machines": WORKFLOW_STATE_MACHINES,
        "scenario_eval_contract": SCENARIO_EVAL_CONTRACT,
        "context_profile_policy": CONTEXT_PROFILE_POLICY,
    }
    lines.extend(yaml.safe_dump(state_registry, sort_keys=False, allow_unicode=True).rstrip().splitlines())

    (PLUGIN / "workflow-registry.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote registry for {len(skill_files)} skills and {len(REVIEWERS)} reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
