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
    "research-polisher-strategy-reviewer",
    "research-polisher-methodology-publishability-reviewer",
}

VERIFIER_COMPOSITORS = {
    "article-submission-compositor",
    "perspective-final-compositor",
}

PUBLIC_ENTRY_SKILLS = {
    "research-idea-orchestrator",
    "proposal-orchestrator",
    "article-orchestrator",
    "perspective-orchestrator",
    "research-polisher-orchestrator",
    "research-opportunity-mapper",
    "academic-deep-search",
}
RESEARCH_POLISHER_ENTRY = "research-polisher-orchestrator"
PERSONAL_IMPLICIT_ENTRY_SKILLS = PUBLIC_ENTRY_SKILLS - {RESEARCH_POLISHER_ENTRY}

# These skills originate in the OpenAI plugin rather than the maintained
# Hermes profile. Keep their package and dependency declarations explicit so
# registry generation never infers a nonexistent Hermes source directory.
OPENAI_NATIVE_SKILLS = {
    "research-polisher-orchestrator": {
        "package": "research-polisher",
        "related_skills": [
            "academic-deep-search",
            "article-architect",
            "article-context-builder",
            "medical-journal-review",
            "methodology-statistics-preflight",
            "research-opportunity-mapper",
            "research-polisher-methodology-publishability-reviewer",
            "research-polisher-plan-assembler",
            "research-polisher-strategy-reviewer",
        ],
    },
    "research-polisher-strategy-reviewer": {
        "package": "research-polisher",
        "related_skills": [
            "research-opportunity-mapper",
            "research-polisher-orchestrator",
        ],
    },
    "research-polisher-plan-assembler": {
        "package": "research-polisher",
        "related_skills": [
            "research-polisher-methodology-publishability-reviewer",
            "research-polisher-orchestrator",
            "research-polisher-strategy-reviewer",
        ],
    },
    "research-polisher-methodology-publishability-reviewer": {
        "package": "research-polisher",
        "related_skills": [
            "medical-journal-review",
            "methodology-statistics-preflight",
            "research-polisher-orchestrator",
            "research-polisher-plan-assembler",
        ],
    },
}

SKILL_IO_OVERRIDES = {
    "article-cover-letter": (
        "frozen_qualifying_article_or_perspective_outlet_evidence_and_disclosures",
        "versioned_cover_letter_and_mechanical_quality_check",
    ),
    "research-polisher-orchestrator": (
        "completed_or_near_complete_research_assets_and_constraints",
        "research_polisher_workflow_state_and_human_selection_handoff",
    ),
    "research-polisher-strategy-reviewer": (
        "frozen_research_polisher_dossier_evidence_optional_verified_target_adapter_one_lens_and_optional_anonymous_must_fix_brief",
        "research_polisher_strategy_report",
    ),
    "research-polisher-plan-assembler": (
        "sealed_strategy_reports_anonymous_portfolio_evaluation_sealed_provenance_requested_specialist_reports_and_current_lineage_by_mode",
        "research_polisher_candidate_portfolio_revision_brief_specialist_findings_bundle_or_selection_dossier",
    ),
    "research-polisher-methodology-publishability-reviewer": (
        "frozen_research_polisher_dossier_necessary_evidence_anonymous_candidate_portfolio_optional_verified_target_adapter_and_sanitized_specialist_findings_bundle",
        "research_polisher_evaluation_report",
    ),
}

RELATED_SKILL_ADDITIONS = {
    "article-cover-letter": {"perspective-orchestrator", "perspective-final-compositor"},
    "perspective-orchestrator": {"article-cover-letter"},
    "perspective-final-compositor": {"article-cover-letter"},
}

# workflow, source, destination, dispatch mode, trigger, input contract,
# output contract, failure route
WORKFLOW_EDGES = [
    ("idea", "research-idea-orchestrator", "research-context-builder", "orchestrated", "context_required", "user_inputs_and_constraints", "research_context_brief", "clarification_required"),
    ("idea", "research-idea-orchestrator", "research-opportunity-mapper", "orchestrated", "evidence_or_opportunity_map_required", "context_sources_and_scope", "evidence_and_opportunity_maps", "evidence_mapping_pending"),
    ("idea", "research-idea-orchestrator", "multi-path-idea-generator", "orchestrated", "context_and_opportunity_map_ready_or_revision_authorized", "frozen_context_opportunity_current_complete_snapshots_and_revision_plan", "versioned_complete_snapshots_candidate_index_and_delta", "generation_blocked"),
    ("idea", "research-idea-orchestrator", "methodology-statistics-preflight", "delegated", "method_or_endpoint_fit_needs_review", "frozen_complete_snapshots_and_method_facts", "preflight_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-evaluator", "delegated", "candidate_set_frozen_or_revised", "one_frozen_complete_snapshot_stable_rubric_and_facts", "idea_evaluation_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-adversarial-review-panel", "delegated", "proposal_handoff_candidate_exists", "one_frozen_promoted_complete_snapshot_and_role_brief", "sealed_individual_adversarial_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "academic-language-assessor", "delegated", "external_facing_portfolio_language_check", "frozen_portfolio_text_and_language_scope", "language_assessment_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-portfolio-assembler", "orchestrated", "evaluation_and_adversarial_reports_sealed", "evaluated_complete_snapshots_lineage_and_dissent", "pi_review_portfolio", "assembly_blocked"),
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
    ("article", "article-orchestrator", "medical-journal-review", "delegated", "biomedical_review_or_publication_probability_requested", "frozen_cover_letter_target_outlet_and_declared_scope", "medical_journal_review_report", "independent_review_pending"),
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
    ("perspective", "perspective-orchestrator", "article-cover-letter", "orchestrated", "qualifying_perspective_cover_letter_requested", "frozen_perspective_outlet_core_argument_evidence_and_disclosures", "cover_letter_and_quality_check", "cover_letter_blocked"),
    ("perspective", "perspective-orchestrator", "medical-journal-review", "delegated", "biomedical_review_or_publication_probability_requested", "frozen_perspective_optional_cover_letter_target_outlet_and_declared_scope", "medical_journal_review_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "academic-language-assessor", "delegated", "final_perspective_language_check", "frozen_perspective_and_language_scope", "language_assessment_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-final-compositor", "delegated", "all_required_artifacts_and_reviews_frozen", "frozen_final_artifacts_reviews_and_dissent", "verified_human_review_package", "independent_review_pending"),

    ("research_polisher", "research-polisher-orchestrator", "article-context-builder", "orchestrated", "dossier_normalization_required", "frozen_research_assets_scope_and_constraints", "article_context_brief_for_research_polisher", "clarification_required"),
    ("research_polisher", "research-polisher-orchestrator", "research-opportunity-mapper", "orchestrated", "broad_positioning_evidence_required", "frozen_dossier_questions_sources_and_scope", "evidence_and_opportunity_maps", "evidence_mapping_pending"),
    ("research_polisher", "research-polisher-orchestrator", "academic-deep-search", "orchestrated", "bounded_two_to_five_paper_question_required", "one_bounded_question_scope_and_source_constraints", "focused_academic_synthesis", "evidence_mapping_pending"),
    ("research_polisher", "research-polisher-orchestrator", "research-polisher-strategy-reviewer", "delegated", "dossier_frozen_or_anonymous_revision_brief_ready", "frozen_dossier_evidence_one_lens_and_three_tiers", "sealed_research_polisher_strategy_report", "independent_review_pending"),
    ("research_polisher", "research-polisher-orchestrator", "research-polisher-plan-assembler", "orchestrated", "strategy_reports_evaluation_or_specialist_reports_ready", "sealed_strategy_reports_evaluation_or_current_requested_specialist_reports_with_lineage", "candidate_portfolio_revision_brief_sanitized_specialist_findings_or_selection_dossier", "assembly_blocked"),
    ("research_polisher", "research-polisher-orchestrator", "research-polisher-methodology-publishability-reviewer", "delegated", "candidate_portfolio_version_frozen_or_revised", "frozen_anonymous_candidate_portfolio_dossier_and_necessary_evidence", "research_polisher_evaluation_report", "independent_review_pending"),
    ("research_polisher", "research-polisher-orchestrator", "methodology-statistics-preflight", "delegated", "specialist_method_preflight_requested", "frozen_selected_option_and_method_facts", "preflight_report", "independent_review_pending"),
    ("research_polisher", "research-polisher-orchestrator", "medical-journal-review", "delegated", "biomedical_specialist_review_requested", "frozen_selected_option_research_facts_and_review_scope", "medical_journal_review_report", "independent_review_pending"),
    ("research_polisher", "research-polisher-orchestrator", "article-architect", "handoff", "human_selected_reposition_only_option", "selected_evaluator_qualified_repositioning_constraints", "article_blueprint_state", "handoff_blocked"),
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
    "pause_states": [
        "pending_review",
        "specialist_review_pending",
        "independent_review_pending",
        "clarification_stop",
        "deep_research_handoff_required",
    ],
    "terminal_states": [
        "stopped",
        "blocked",
        "no_defensible_option",
        "human_signoff_required",
        "human_strategy_selection_required",
        "additional_work_required",
    ],
    "review_unavailable_state": "independent_review_pending",
    "fatal_finding_state": "blocked",
    "final_handoff_state": "human_signoff_required",
    "wildcard_transition_scope": "nonterminal_states_only",
    "resume_policy": {
        "independent_review_pending": "pending_review",
        "clarification_stop": "preprocessing",
        "deep_research_handoff_required": "preprocessing",
    },
    "version_gate": {
        "changed_artifact_requires_new_version": True,
        "evaluator_instance_must_be_fresh": True,
        "evaluated_version_must_equal_current_version": True,
        "prior_scores_visible_to_fresh_evaluator": False,
        "required_before_states": [
            "panel_pending",
            "packaging_pending",
            "human_signoff_required",
            "human_strategy_selection_required",
        ],
    },
    "finding_gate": {
        "fatal_or_blocking_finding_prevents_accept": True,
        "fatal_or_blocking_finding_prevents_promoted": True,
        "fatal_or_blocking_finding_prevents_human_signoff": True,
        "fatal_or_blocking_finding_prevents_human_strategy_selection": True,
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
        {
            "from": "pending_review",
            "to": "packaging_pending",
            "trigger": "latest_strategy_portfolio_accepted",
            "requires": ["fresh_evaluation_current", "no_unresolved_fatal_finding"],
        },
        {
            "from": "pending_review",
            "to": "specialist_review_pending",
            "trigger": "specialist_review_requested",
            "requires": ["bounded_specialist_question", "evaluator_round_available"],
        },
        {
            "from": "specialist_review_pending",
            "to": "pending_review",
            "trigger": "sanitized_specialist_findings_ready",
            "requires": ["specialist_reports_current", "sanitized_findings_bundle_current", "fresh_evaluator_instance"],
        },
        {"from": "packaging_pending", "to": "human_signoff_required", "trigger": "package_verified"},
        {
            "from": "packaging_pending",
            "to": "human_strategy_selection_required",
            "trigger": "selection_dossier_verified",
        },
        {
            "from": "human_strategy_selection_required",
            "to": "additional_work_required",
            "trigger": "human_selected_extension_option",
            "requires": ["current_selection_dossier", "selected_option_is_small_or_moderate_extension"],
        },
        {"from": "*", "to": "independent_review_pending", "trigger": "required_reviewer_unavailable"},
        {"from": "*", "to": "clarification_stop", "trigger": "required_source_facts_missing_or_inconsistent"},
        {"from": "*", "to": "deep_research_handoff_required", "trigger": "inactive_deep_research_required"},
        {"from": "*", "to": "blocked", "trigger": "fatal_or_blocking_finding"},
        {"from": "*", "to": "no_defensible_option", "trigger": "no_defensible_strategy_remains"},
        {"from": "*", "to": "stopped", "trigger": "unfixable_no_gain_or_user_stop"},
        {"from": "independent_review_pending", "to": "pending_review", "trigger": "reviewer_delegation_resumed"},
    ],
}

WORKFLOW_STATE_MACHINES = {
    "idea": {
        "orchestrator": "research-idea-orchestrator",
        "evaluator_skill": "idea-evaluator",
        "primary_writer_skills": ["multi-path-idea-generator"],
        "primary_artifact_creator_skills": ["multi-path-idea-generator"],
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
            "resume_candidates": {
                "context_scope_validated": {"artifact_roles": ["research_context"]},
                "evidence_scope_validated": {"artifact_roles": ["evidence_map"]},
                "candidate_set_versioned": {"artifact_roles": ["candidate_idea_set"]},
            },
            "portfolio_only": {
                "latest_version_independently_evaluated": {
                    "review_skill": "idea-evaluator",
                    "input_artifact_roles": ["candidate_idea_set"],
                },
                "adversarial_reports_complete": {
                    "review_skill": "idea-adversarial-review-panel",
                    "input_artifact_roles": ["candidate_idea_set"],
                },
                "dissent_and_fatal_findings_indexed": {
                    "artifact_roles": ["review_finding_index"],
                },
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
        "primary_writer_skills": ["proposal-drafter"],
        "primary_artifact_creator_skills": ["proposal-drafter"],
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
            "existing_draft": {
                "minimal_state_created": {"artifact_roles": ["minimal_workflow_state"]},
                "scope_limitations_recorded": {"artifact_roles": ["scope_limitations"]},
                "proposal_versioned": {"artifact_roles": ["proposal"]},
            },
            "draft_and_external_review": {
                "minimal_state_created": {"artifact_roles": ["minimal_workflow_state"]},
                "proposal_versioned": {"artifact_roles": ["proposal"]},
                "external_review_qualified_or_fresh_evaluation_required": {
                    "review_skill": "proposal-evaluator",
                    "input_artifact_roles": ["proposal"],
                },
            },
            "package_only": {
                "latest_version_independently_evaluated": {
                    "review_skill": "proposal-evaluator",
                    "input_artifact_roles": ["proposal"],
                },
                "required_panel_reports_complete": {
                    "review_skill": "proposal-review-panel",
                    "input_artifact_roles": ["proposal"],
                },
                "dissent_and_fatal_findings_indexed": {
                    "artifact_roles": ["review_finding_index"],
                },
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
        "primary_writer_skills": ["article-drafter"],
        "primary_artifact_creator_skills": ["article-drafter"],
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
            "fast_track_draft": {
                "readiness_passed": {
                    "review_skill": "article-readiness-triage",
                    "input_artifact_roles": ["minimal_intake"],
                },
                "minimal_backfill_validated": {
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
            "fast_track_draft_and_evaluation": {
                "readiness_passed": {
                    "review_skill": "article-readiness-triage",
                    "input_artifact_roles": ["minimal_intake"],
                },
                "manuscript_versioned": {"artifact_roles": ["manuscript"]},
                "external_review_qualified_or_fresh_evaluation_required": {
                    "review_skill": "article-evaluator",
                    "input_artifact_roles": ["manuscript"],
                },
            },
            "blueprint_only": {
                "readiness_passed": {
                    "review_skill": "article-readiness-triage",
                    "input_artifact_roles": ["minimal_intake"],
                },
                "context_frozen": {"artifact_roles": ["article_context"]},
                "methods_gate_passed": {
                    "review_skill": "article-methods-statistics-auditor",
                    "input_artifact_roles": ["article_context", "method_facts"],
                },
            },
            "section_specific": {
                "scoped_intake_frozen": {"artifact_roles": ["scoped_intake"]},
                "minimal_context_frozen": {"artifact_roles": ["article_context"]},
            },
            "submission_only": {
                "submission_scope_readiness_passed": {
                    "review_skill": "article-readiness-triage",
                    "input_artifact_roles": ["minimal_intake", "manuscript"],
                },
                "manuscript_versioned": {"artifact_roles": ["manuscript"]},
                "latest_version_independently_evaluated": {
                    "review_skill": "article-evaluator",
                    "input_artifact_roles": ["manuscript"],
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
        "primary_writer_skills": ["perspective-drafter"],
        "primary_artifact_creator_skills": ["perspective-drafter"],
        "primary_artifact_type": "perspective",
        "entry_modes": ["lite", "standard", "full"],
        "entry_gates": {
            "lite": ["input_brief_frozen", "provisional_claims_frozen", "argument_architecture_frozen"],
            "standard": ["input_brief_frozen", "claim_evidence_artifacts_frozen", "argument_architecture_frozen", "perspective_versioned"],
            "full": ["input_brief_frozen", "claim_evidence_artifacts_frozen", "argument_architecture_frozen", "perspective_versioned"],
        },
        "scenario_entry_gate_contracts": {
            "lite": {
                "input_brief_frozen": {"artifact_roles": ["perspective_input_brief"]},
                "provisional_claims_frozen": {"artifact_roles": ["provisional_claim_ledger"]},
                "argument_architecture_frozen": {"artifact_roles": ["argument_architecture", "paragraph_map"]},
            },
            "standard": {
                "input_brief_frozen": {"artifact_roles": ["perspective_input_brief"]},
                "claim_evidence_artifacts_frozen": {"artifact_roles": ["claim_ledger", "claim_evidence_matrix"]},
                "argument_architecture_frozen": {"artifact_roles": ["argument_architecture", "paragraph_map"]},
                "perspective_versioned": {"artifact_roles": ["perspective"]},
            },
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
    "research_polisher": {
        "workflow_profile": "reviewer_matrix_assemble_evaluate",
        "orchestrator": "research-polisher-orchestrator",
        "strategy_reviewer_skill": "research-polisher-strategy-reviewer",
        "strategy_reviewer_roles": [
            "scientific_significance",
            "practical_value",
            "dissemination_editorial",
        ],
        "effort_tiers": [
            "reposition_only",
            "small_extension",
            "moderate_extension",
        ],
        "primary_assembler_skill": "research-polisher-plan-assembler",
        "evaluator_skill": "research-polisher-methodology-publishability-reviewer",
        "primary_writer_skills": [],
        "primary_artifact_creator_skills": ["research-polisher-plan-assembler"],
        "primary_artifact_type": "research_polisher_candidate_portfolio",
        "entry_modes": ["standard"],
        "entry_gates": {
            "standard": [
                "dossier_frozen",
                "strategy_matrix_complete",
                "candidate_portfolio_versioned",
            ],
        },
        "scenario_entry_gate_contracts": {
            "standard": {
                "dossier_frozen": {
                    "artifact_roles": ["research_polisher_dossier"],
                },
                "strategy_matrix_complete": {
                    "artifact_roles": ["strategy_report_manifest"],
                },
                "candidate_portfolio_versioned": {
                    "artifact_roles": ["research_polisher_candidate_portfolio"],
                },
            },
        },
        "before_strategy_assembly": [
            "three_strategy_roles_complete",
            "nine_matrix_cells_accounted",
            "dissent_and_conflicts_indexed",
        ],
        "before_evaluation": [
            "candidate_portfolio_versioned",
            "reviewer_identity_mapping_sealed",
        ],
        "before_panel": [],
        "before_packaging": [
            "latest_version_independently_evaluated",
            "dissent_and_fatal_findings_indexed",
        ],
        "post_evaluation_panel_required": False,
        "maximum_evaluator_rounds": 2,
        "conditional_specialist_review_skills": [
            "methodology-statistics-preflight",
            "medical-journal-review",
        ],
        "specialist_review_return_contract": {
            "state": "specialist_review_pending",
            "sanitizer_skill": "research-polisher-plan-assembler",
            "sanitized_artifact_type": "research_polisher_specialist_findings_bundle",
            "raw_specialist_reports_visible_to_final_reviewer": False,
            "requires_fresh_final_reviewer": True,
            "counts_as_evaluator_round": True,
        },
        "non_ready_modes": [],
        "final_package_skill": "research-polisher-plan-assembler",
        "final_state": "human_strategy_selection_required",
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
    "research-polisher-strategy-reviewer": {
        "allowed": [
            "matrix_complete",
            "matrix_complete_with_no_defensible_option",
            "clarification_required",
            "independent_review_pending",
        ],
        "pass": ["matrix_complete", "matrix_complete_with_no_defensible_option"],
        "revise": ["clarification_required"],
        "stop": ["independent_review_pending"],
    },
    "research-polisher-methodology-publishability-reviewer": {
        "allowed": [
            "ready_for_human_selection",
            "revision_required",
            "specialist_review_required",
            "no_defensible_option",
            "not_assessable",
            "independent_review_pending",
        ],
        "pass": ["ready_for_human_selection"],
        "revise": ["revision_required", "specialist_review_required"],
        "stop": [
            "no_defensible_option",
            "not_assessable",
            "independent_review_pending",
        ],
    },
}

PACKAGE_INPUT_CONTRACTS = {
    "idea": {
        "allowed_roles": ["research_context", "evidence_map", "candidate_idea_set", "evaluation_report", "panel_report", "revision_plan", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "research_context", "source_skill": "research-context-builder", "count": 1},
            {"artifact_role": "evidence_map", "source_skill": "research-opportunity-mapper", "count": 1},
            {"artifact_role": "candidate_idea_set", "source_skills": ["multi-path-idea-generator", "external-input"], "current_primary": True, "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "idea-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "idea-adversarial-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "revision_plan", "source_skill": "research-idea-orchestrator", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "multi-path-idea-generator", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "proposal": {
        "allowed_roles": ["proposal_context", "readiness_report", "proposal", "evaluation_report", "preflight_report", "sap", "panel_report", "revision_plan", "response_to_reviewers", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "proposal_context", "source_skill": "proposal-context-brief-builder", "count": 1},
            {"artifact_role": "readiness_report", "source_skill": "proposal-readiness-triage", "count": 1},
            {"artifact_role": "proposal", "source_skills": ["proposal-drafter", "external-input"], "current_primary": True, "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "proposal-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "preflight_report", "source_skill": "methodology-statistics-preflight", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "sap", "source_skill": "sap-writer", "latest_selected_artifact": True, "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "sap-evaluator", "selected_artifact_lineage_role": "sap", "exact_selected_artifact_lineage": True, "fresh_review_required": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "proposal-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "revision_plan", "source_skill": "proposal-refinement-controller", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "response_to_reviewers", "source_skill": "proposal-drafter", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "proposal-drafter", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "article": {
        "allowed_roles": ["manuscript", "article_blueprint", "claim_evidence_matrix", "evidence_ledger", "readiness_report", "evaluation_report", "audit_report", "panel_report", "journal_adapter", "frontmatter", "cover_letter", "quality_check", "medical_journal_review_report", "revision_plan", "response_to_reviewers", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "manuscript", "source_skills": ["article-drafter", "external-input"], "current_primary": True, "count": 1},
            {"artifact_role": "article_blueprint", "source_skill": "article-architect", "count": 1},
            {"artifact_role": "claim_evidence_matrix", "source_skill": "article-architect", "count": 1},
            {"artifact_role": "evidence_ledger", "source_skill": "article-literature-grounder", "count": 1},
            {"artifact_role": "readiness_report", "source_skill": "article-readiness-triage", "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "article-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "audit_report", "source_skill": "article-methods-statistics-auditor", "count": 1},
            {"artifact_role": "audit_report", "source_skill": "article-claim-auditor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "article-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "journal_adapter", "source_skill": "article-architect", "count": 1},
            {"artifact_role": "frontmatter", "source_skill": "article-frontmatter-drafter", "count": 1},
            {"artifact_role": "cover_letter", "source_skill": "article-cover-letter", "count": 1},
            {"artifact_role": "quality_check", "source_skill": "article-cover-letter", "count": 1},
            {"artifact_role": "revision_plan", "source_skill": "article-refinement-controller", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "response_to_reviewers", "source_skill": "article-drafter", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "article-drafter", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "perspective": {
        "allowed_roles": ["perspective", "target_outlet_profile", "claim_ledger", "claim_evidence_matrix", "evidence_limitations", "citation_risk_log", "contrary_evidence_log", "reference_list", "evaluation_report", "panel_report", "cover_letter", "quality_check", "medical_journal_review_report"],
        "required_inputs": [
            {"artifact_role": "perspective", "source_skill": "perspective-drafter", "current_primary": True, "count": 1},
            {"artifact_role": "target_outlet_profile", "source_skill": "perspective-input-builder", "count": 1},
            {"artifact_role": "claim_ledger", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "claim_evidence_matrix", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "evidence_limitations", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "citation_risk_log", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "contrary_evidence_log", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "reference_list", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "perspective-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "perspective-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
        ],
    },
    "research_polisher": {
        "allowed_roles": [
            "research_polisher_dossier",
            "evidence_map",
            "research_polisher_sealed_provenance",
            "research_polisher_candidate_portfolio",
            "research_polisher_evaluation_report",
            "research_polisher_specialist_findings_bundle",
            "research_polisher_review_finding_index",
            "research_polisher_revision_brief",
            "research_polisher_revision_delta",
        ],
        "required_inputs": [
            {"artifact_role": "research_polisher_dossier", "source_skill": "article-context-builder", "count": 1},
            {"artifact_role": "evidence_map", "source_skill": "research-opportunity-mapper", "count": 1},
            {
                "artifact_role": "research_polisher_sealed_provenance",
                "source_skill": "research-polisher-plan-assembler",
                "count": 1,
            },
            {
                "artifact_role": "research_polisher_candidate_portfolio",
                "source_skill": "research-polisher-plan-assembler",
                "current_primary": True,
                "count": 1,
            },
            {
                "artifact_role": "research_polisher_evaluation_report",
                "source_skill": "research-polisher-methodology-publishability-reviewer",
                "current_primary_lineage": True,
                "count": 1,
            },
            {
                "artifact_role": "research_polisher_specialist_findings_bundle",
                "source_skill": "research-polisher-plan-assembler",
                "minimum_count": 0,
                "include_all_created": True,
            },
            {
                "artifact_role": "research_polisher_review_finding_index",
                "source_skill": "research-polisher-plan-assembler",
                "count": 1,
            },
            {
                "artifact_role": "research_polisher_revision_brief",
                "source_skill": "research-polisher-plan-assembler",
                "minimum_count": 0,
                "include_all_created": True,
            },
            {
                "artifact_role": "research_polisher_revision_delta",
                "source_skill": "research-polisher-plan-assembler",
                "minimum_count": 0,
                "include_all_created": True,
            },
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
    "research_polisher": {
        "default_tier": "not_applicable",
        "modes": ["not_applicable"],
        "tiers": {"not_applicable": []},
        "mandatory_roles": [],
        "mode_forbidden_input_roles": {"not_applicable": []},
    },
}

REVIEW_GROUP_CONTRACTS = {
    "research_polisher": {
        "skill": "research-polisher-strategy-reviewer",
        "roles": [
            "scientific_significance",
            "practical_value",
            "dissemination_editorial",
        ],
        "effort_tiers": [
            "reposition_only",
            "small_extension",
            "moderate_extension",
        ],
        "required_instance_count": 3,
        "required_matrix_cell_count": 9,
        "instances_must_be_distinct": True,
        "peer_outputs_visible": False,
        "raw_reports_visible_to_final_evaluator": False,
        "manifest_artifact_role": "strategy_report_manifest",
    },
}

SCENARIO_EVAL_CONTRACT = {
    "fixture_schema_version": 2,
    "required_workflows": [
        "idea",
        "proposal",
        "article",
        "perspective",
        "research_polisher",
    ],
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
        "evaluator_may_read_prior_reviewer_outputs": False,
        "evaluator_prior_scores_visible": False,
        "runtime_evaluator_forbidden_source_actor_roles": [
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
            "verifier_compositor",
        ],
        "runtime_blind_reviewer_actor_roles": [
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
        ],
        "runtime_forbidden_oracle_artifact_roles": [
            "answer_key",
            "expected_decision",
            "expected_findings",
            "expected_score",
            "result_oracle",
            "review_oracle",
        ],
    },
    "runtime_actor_role_contract": {
        "allowed_roles": [
            "orchestrator",
            "writer",
            "evaluator",
            "panel",
            "builder",
            "retrieval",
            "controller",
            "assembler",
            "strategy_reviewer",
            "supporting_reviewer",
            "supporting_writer",
            "verifier_compositor",
        ],
        "registry_roles_by_actor_role": {
            "orchestrator": ["orchestrator"],
            "writer": ["drafter", "generator"],
            "evaluator": ["reviewer"],
            "panel": ["reviewer"],
            "builder": ["builder"],
            "retrieval": ["retrieval"],
            "controller": ["controller"],
            "assembler": ["assembler"],
            "strategy_reviewer": ["reviewer"],
            "supporting_reviewer": ["reviewer"],
            "supporting_writer": ["drafter"],
            "verifier_compositor": ["reviewer"],
        },
        "edge_derived_roles": {
            "supporting_reviewer": {
                "registry_role": "reviewer",
                "dispatch_mode": "delegated",
                "requires_independent_subagent": True,
                "isolation_mode": "fresh_subagent",
                "exclude_designated_reviewer_slots": True,
            },
            "supporting_writer": {
                "registry_role": "drafter",
                "dispatch_mode": "orchestrated",
                "exclude_primary_writer_skills": True,
            },
        },
        "independent_reviewer_actor_roles": [
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
            "verifier_compositor",
        ],
        "independent_reviewer_isolation_mode": "fresh_subagent",
        "edge_provenance_required_actor_roles": [
            "writer",
            "evaluator",
            "panel",
            "builder",
            "retrieval",
            "controller",
            "assembler",
            "strategy_reviewer",
            "supporting_reviewer",
            "supporting_writer",
            "verifier_compositor",
        ],
        "edge_provenance_required_fields": [
            "dispatch_source",
            "dispatch_mode",
            "dispatch_trigger",
        ],
        "root_actor_role": "orchestrator",
        "happy_required_roles": [
            "orchestrator",
            "writer",
            "evaluator",
            "panel",
        ],
        "happy_required_roles_by_workflow_profile": {
            "default": ["orchestrator", "writer", "evaluator", "panel"],
            "reviewer_matrix_assemble_evaluate": [
                "orchestrator",
                "strategy_reviewer",
                "assembler",
                "evaluator",
            ],
        },
        "finalizer_roles": ["assembler", "verifier_compositor"],
        "unknown_roles_rejected": True,
        "registry_role_mapping_enforced": True,
        "orchestrator_skill_must_match_workflow": True,
    },
    "reviewer_isolation_mode": "fresh_subagent",
    "reviewer_source_edits_allowed": False,
    "prior_scores_visible_to_fresh_reviewer": False,
    "reviewer_instance_must_differ_from_artifact_writer": True,
    "panel_role_instance_mapping_must_be_one_to_one": True,
    "review_decision_contracts": REVIEW_DECISION_CONTRACTS,
    "panel_contracts": PANEL_CONTRACTS,
    "review_group_contracts": REVIEW_GROUP_CONTRACTS,
    "package_input_contracts": PACKAGE_INPUT_CONTRACTS,
    "revision_artifact_contract": {
        "controller_output_role": "revision_plan",
        "drafter_required_output_roles": ["response_to_reviewers", "revision_delta"],
    },
    "verifier_compositor_outputs": {
        "article-submission-compositor": [
            "verification_report",
            "review_finding_index",
            "final_handoff_package",
        ],
        "perspective-final-compositor": [
            "verification_report",
            "review_finding_index",
            "panel_summary",
            "artifact_index",
            "final_handoff_package",
        ],
    },
    "runtime_artifact_role_contract": {
        "review_output_roles": [
            "evaluation_report",
            "research_polisher_evaluation_report",
            "research_polisher_strategy_report",
            "review_report",
            "audit_report",
            "panel_report",
            "verification_report",
            "readiness_report",
            "preflight_report",
            "language_assessment_report",
            "medical_journal_review_report",
        ],
        "assembler_outputs_by_skill": {
            "idea-portfolio-assembler": [
                "final_handoff_package",
                "review_finding_index",
            ],
            "proposal-package-assembler": [
                "final_handoff_package",
                "review_finding_index",
            ],
            "research-polisher-plan-assembler": [
                "research_polisher_sealed_provenance",
                "research_polisher_candidate_portfolio",
                "research_polisher_specialist_findings_bundle",
                "research_polisher_review_finding_index",
                "research_polisher_revision_brief",
                "research_polisher_revision_delta",
                "research_polisher_selection_dossier",
            ],
        },
        "supporting_writer_outputs_by_skill": {
            "sap-writer": ["sap"],
            "article-frontmatter-drafter": ["frontmatter"],
        },
        "research_polisher_review_outputs_by_actor_role_and_skill": {
            "strategy_reviewer": {
                "research-polisher-strategy-reviewer": [
                    "research_polisher_strategy_report"
                ],
            },
            "evaluator": {
                "research-polisher-methodology-publishability-reviewer": [
                    "research_polisher_evaluation_report"
                ],
            },
            "supporting_reviewer": {
                "methodology-statistics-preflight": ["preflight_report"],
                "medical-journal-review": ["medical_journal_review_report"],
            },
        },
        "research_polisher_strategy_matrix_contract": {
            "strategy_skill": "research-polisher-strategy-reviewer",
            "strategy_artifact_role": "research_polisher_strategy_report",
            "portfolio_skill": "research-polisher-plan-assembler",
            "portfolio_artifact_role": "research_polisher_candidate_portfolio",
            "strategy_roles": [
                "scientific_significance",
                "practical_value",
                "dissemination_editorial",
            ],
            "effort_tiers": [
                "reposition_only",
                "small_extension",
                "moderate_extension",
            ],
            "reports_per_portfolio": 3,
            "cells_per_report": 3,
            "total_matrix_cells": 9,
            "portfolio_binds_all_strategy_reports": True,
            "assembler_reads_all_strategy_reports": True,
            "generic_review_reports_do_not_satisfy_strategy_lineage": True,
            "required_option_fields": [
                "proposal_id",
                "effort_tier",
                "status",
                "positioning_change",
                "value_gain_mechanism",
                "claim_delta",
                "target_audience",
                "added_work_items",
                "resource_dependencies",
                "feasibility",
                "evidence_dependencies",
                "risks",
                "stop_conditions",
                "new_work_flags",
                "bounded_package",
                "independent_new_study",
                "core_design_rebuild",
            ],
            "new_work_flag_fields": [
                "new_analysis",
                "new_experiment",
                "new_data",
                "new_validation",
            ],
            "allowed_feasibility_ratings": ["certain", "high", "low", "unknown"],
            "proposed_extension_feasibility_ratings": ["certain", "high"],
            "reposition_requires_no_added_work": True,
            "extensions_must_be_bounded": True,
            "low_or_unknown_extension_requires_no_defensible_option": True,
        },
        "verification_report_contributes_review_findings": True,
        "runtime_review_report_contract": {
            "required_fields": [
                "decision",
                "findings",
                "unresolved_issues",
                "dissent_ids",
                "fatal_finding_ids",
                "unresolved_fatal_finding_ids",
            ],
            "finding_required_fields": [
                "id",
                "severity",
                "blocking",
                "resolved",
                "dissent",
            ],
            "allowed_severities": ["fatal", "major", "minor", "info"],
            "derived_index_fields": {
                "dissent_ids": "finding.dissent_true",
                "fatal_finding_ids": "finding.severity_fatal",
                "unresolved_fatal_finding_ids": "finding.severity_fatal_and_resolved_false",
                "unresolved_issues": "finding.blocking_true_and_resolved_false",
            },
            "decision_vocabulary_from_review_decision_contracts": True,
            "ready_actor_roles_require_pass_decision": [
                "evaluator",
                "panel",
                "strategy_reviewer",
                "supporting_reviewer",
                "verifier_compositor",
            ],
            "one_review_report_per_actor": True,
            "pass_decision_requires_no_unresolved_blocking_findings": True,
            "review_input_refs_must_equal_actual_read_artifact_refs": True,
        },
        "actor_output_roles_by_skill": {
            "research-idea-orchestrator": ["revision_plan", "continuation_brief"],
            "proposal-orchestrator": ["minimal_workflow_state", "continuation_brief"],
            "article-orchestrator": ["continuation_brief"],
            "perspective-orchestrator": ["continuation_brief"],
            "research-polisher-orchestrator": ["continuation_brief"],
            "research-context-builder": ["research_context"],
            "proposal-context-brief-builder": ["proposal_context"],
            "article-context-builder": ["article_context", "research_polisher_dossier"],
            "perspective-input-builder": ["perspective_input_brief", "target_outlet_profile"],
            "perspective-claim-evidence-curator": ["claim_ledger", "claim_evidence_matrix", "evidence_limitations", "citation_risk_log", "contrary_evidence_log", "reference_list", "provisional_claim_ledger"],
            "perspective-argument-architect": ["argument_architecture", "paragraph_map"],
            "research-opportunity-mapper": ["evidence_map", "opportunity_map"],
            "academic-deep-search": ["focused_academic_synthesis"],
            "article-literature-grounder": ["evidence_ledger", "evidence_map", "literature_grounding_report"],
            "multi-path-idea-generator": ["candidate_idea_set", "revision_delta"],
            "proposal-drafter": ["proposal", "response_to_reviewers", "revision_delta"],
            "sap-writer": ["sap"],
            "article-drafter": ["manuscript", "response_to_reviewers", "revision_delta"],
            "article-architect": ["article_blueprint", "claim_evidence_matrix", "journal_adapter"],
            "article-frontmatter-drafter": ["journal_adapter", "frontmatter"],
            "article-cover-letter": ["cover_letter", "quality_check"],
            "perspective-drafter": ["perspective", "response_to_reviewers", "revision_delta"],
            "proposal-refinement-controller": ["revision_plan"],
            "sap-refinement-controller": ["revision_plan"],
            "article-refinement-controller": ["revision_plan"],
            "perspective-refinement-controller": ["revision_plan"],
            "academic-language-assessor": ["language_assessment_report"],
            "medical-journal-review": ["medical_journal_review_report"],
            "methodology-statistics-preflight": ["preflight_report"],
            "idea-evaluator": ["evaluation_report"],
            "idea-adversarial-review-panel": ["panel_report"],
            "proposal-readiness-triage": ["readiness_report"],
            "proposal-evaluator": ["evaluation_report"],
            "proposal-review-panel": ["panel_report"],
            "sap-evaluator": ["evaluation_report"],
            "article-readiness-triage": ["readiness_report"],
            "article-methods-statistics-auditor": ["audit_report"],
            "article-claim-auditor": ["audit_report"],
            "article-evaluator": ["evaluation_report"],
            "article-review-panel": ["panel_report"],
            "perspective-evaluator": ["evaluation_report"],
            "perspective-review-panel": ["panel_report"],
            "research-polisher-strategy-reviewer": ["research_polisher_strategy_report"],
            "research-polisher-methodology-publishability-reviewer": ["research_polisher_evaluation_report"],
            "idea-portfolio-assembler": ["review_finding_index", "final_handoff_package"],
            "proposal-package-assembler": ["review_finding_index", "final_handoff_package"],
            "research-polisher-plan-assembler": ["research_polisher_sealed_provenance", "research_polisher_candidate_portfolio", "research_polisher_specialist_findings_bundle", "research_polisher_review_finding_index", "research_polisher_revision_brief", "research_polisher_revision_delta", "research_polisher_selection_dossier"],
            "article-submission-compositor": ["verification_report", "review_finding_index", "final_handoff_package"],
            "perspective-final-compositor": ["verification_report", "review_finding_index", "final_handoff_package", "panel_summary", "artifact_index"],
        },
        "verifier_compositor_internal_output_contracts": {
            "perspective-final-compositor": {
                "ordered_output_roles": [
                    "panel_summary",
                    "artifact_index",
                    "verification_report",
                    "review_finding_index",
                    "final_handoff_package",
                ],
                "final_output_role": "final_handoff_package",
                "internal_dependency_roles": [
                    "panel_summary",
                    "artifact_index",
                    "verification_report",
                    "review_finding_index",
                ],
                "creation_sequence_field": "creation_sequence",
                "internal_output_refs_field": "internal_output_refs",
                "internal_dependencies_are_not_file_reads": True,
                "single_instance_required": True,
            }
        },
        "external_input_contract": {
            "creator_sentinel": "external-input",
            "source_skill_sentinel": "external-input",
            "source_identity_field": "external_source_id",
            "source_identity_prefix": "external:",
            "allowed_artifact_roles_by_workflow_and_mode": {
                "idea": {
                    "standard": ["source_material", "user_constraints"],
                    "resume_candidates": ["source_material", "user_constraints", "candidate_idea_set"],
                    "portfolio_only": ["source_material", "candidate_idea_set"],
                },
                "proposal": {
                    "standard": ["source_material", "user_constraints", "call_text", "data_facts"],
                    "existing_draft": ["source_material", "user_constraints", "call_text", "data_facts", "proposal"],
                    "draft_and_external_review": ["source_material", "user_constraints", "proposal"],
                    "package_only": ["source_material", "proposal"],
                },
                "article": {
                    "standard": ["minimal_intake", "method_facts", "source_material", "results", "target_requirements"],
                    "fast_track_draft": ["minimal_intake", "method_facts", "source_material", "results", "manuscript", "target_requirements"],
                    "fast_track_draft_and_evaluation": ["minimal_intake", "source_material", "manuscript", "target_requirements"],
                    "blueprint_only": ["minimal_intake", "method_facts", "source_material", "results"],
                    "section_specific": ["scoped_intake", "source_material", "article_context"],
                    "submission_only": ["minimal_intake", "source_material", "manuscript", "target_requirements"],
                },
                "perspective": {
                    "lite": ["source_material", "user_thesis", "target_outlet_profile"],
                    "standard": ["source_material", "user_thesis", "target_outlet_profile"],
                    "full": ["source_material", "user_thesis", "target_outlet_profile"],
                },
                "research_polisher": {
                    "standard": ["research_assets", "source_material", "target_outlet_profile"],
                },
            },
            "external_primary_allowed_modes": {
                "idea": ["resume_candidates", "portfolio_only"],
                "proposal": ["existing_draft", "draft_and_external_review", "package_only"],
                "article": ["fast_track_draft", "fast_track_draft_and_evaluation", "submission_only"],
                "perspective": [],
                "research_polisher": [],
            },
            "external_generated_or_review_artifact_impersonation_rejected": True,
        },
        "entry_mode_bound_to_receipt_and_task_export": True,
        "finding_index_role_by_workflow": {
            "idea": "review_finding_index",
            "proposal": "review_finding_index",
            "article": "review_finding_index",
            "perspective": "review_finding_index",
            "research_polisher": "research_polisher_review_finding_index",
        },
    },
    "final_state": "human_signoff_required",
    "workflow_final_states": {
        "idea": "human_signoff_required",
        "proposal": "human_signoff_required",
        "article": "human_signoff_required",
        "perspective": "human_signoff_required",
        "research_polisher": "human_strategy_selection_required",
    },
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

ARTIFACT_COMPLETENESS_POLICY = {
    "idea_schema": "research-idea.v2",
    "idea_current_artifact": "complete_markdown_snapshot",
    "idea_node_layout": "03_ideas/nodes/<idea-id>",
    "idea_tree_mode": "flat_nodes_with_parent_ids",
    "idea_legacy_layout_behavior": "layout_migration_required_read_only",
    "core_identity_drift_behavior": "new_idea_required_no_automatic_branch",
    "proposal_current_artifact": "complete_proposal",
    "article_schema": "research-article.v6",
    "article_current_artifact": "complete_canonical_markdown",
    "fresh_re_evaluation": {
        "allowed": ["current_complete_artifact_and_digest", "stable_rubric", "necessary_facts", "anonymous_must_fix_list"],
        "forbidden": ["prior_artifact", "revision_delta", "prior_report", "prior_score", "prior_decision"],
        "orchestrator_compares_sealed_rounds_after_return": True,
    },
}

ARTICLE_DOCX_DELIVERY_POLICY = {
    "content_authority": "canonical_markdown",
    "primary_user_delivery_when_capable": "docx",
    "display_manifest": "04_blueprint/display-asset-manifest.yaml",
    "faithful_format_transform_only": True,
    "required_ready_gates": [
        "qualifying_markdown_digest_match",
        "required_display_assets_complete",
        "docx_content_parity_passed",
        "full_page_render_qa_passed",
    ],
    "fallback_states": ["docx_generation_pending", "docx_visual_qa_pending"],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def skill_name(path: Path) -> str:
    match = re.search(r"^name:\s*[\"']?([^\r\n\"']+)", read(path), re.M)
    if not match:
        raise ValueError(f"Missing skill name: {path}")
    return match.group(1).strip()


def allows_implicit_invocation(skill_md: Path) -> bool:
    openai_yaml = skill_md.parent / "agents" / "openai.yaml"
    document = yaml.safe_load(read(openai_yaml)) if openai_yaml.is_file() else None
    policy = document.get("policy", {}) if isinstance(document, dict) else {}
    value = policy.get("allow_implicit_invocation") if isinstance(policy, dict) else None
    if not isinstance(value, bool):
        raise ValueError(
            f"{openai_yaml}: policy.allow_implicit_invocation must be boolean"
        )
    return value


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
    if not skill_files or len(names) != len(skill_files):
        raise RuntimeError(
            f"Expected a non-empty unique skill set, found {len(skill_files)} files and {len(names)} names"
        )
    if not REVIEWERS <= names:
        raise RuntimeError(f"Reviewer registry references missing skills: {sorted(REVIEWERS - names)}")
    skill_files_by_name = {skill_name(path): path for path in skill_files}
    implicit = {
        name
        for name, skill_md in skill_files_by_name.items()
        if allows_implicit_invocation(skill_md)
    }
    non_public_implicit = implicit - PUBLIC_ENTRY_SKILLS
    if non_public_implicit:
        raise RuntimeError(
            "Only declared public entries may allow implicit invocation: "
            f"{sorted(non_public_implicit)}"
        )
    if implicit != PERSONAL_IMPLICIT_ENTRY_SKILLS:
        raise RuntimeError(
            "Personal routing requires exactly six implicit entries; Research "
            "Polisher must remain explicit-only"
        )
    hermes_by_name = {
        skill_name(path): path
        for path in HERMES_SKILLS.rglob("SKILL.md")
        if skill_name(path) in names
    }
    native_names = set(OPENAI_NATIVE_SKILLS)
    if native_names - names:
        raise RuntimeError(
            f"Declared OpenAI-native skills are missing: {sorted(native_names - names)}"
        )
    duplicate_origins = native_names & set(hermes_by_name)
    if duplicate_origins:
        raise RuntimeError(
            f"Skills cannot be both Hermes-adapted and OpenAI-native: {sorted(duplicate_origins)}"
        )
    missing_sources = names - set(hermes_by_name) - native_names
    if missing_sources:
        raise RuntimeError(
            f"Skills lack a Hermes source or OpenAI-native declaration: {sorted(missing_sources)}"
        )
    manifest = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
    plugin_version = str(manifest["version"])

    lines = [
        "schema_version: 5",
        f"plugin_version: {quote(plugin_version)}",
        "public_entry_policy:",
        "  declared_entries:",
        *[f"    - {name}" for name in sorted(PUBLIC_ENTRY_SKILLS)],
        "  implicit_active_entries:",
        *[f"    - {name}" for name in sorted(implicit)],
        "  explicit_only_entries:",
        "    research-polisher-orchestrator:",
        "      status: explicit_only_personal_routing_policy",
        "      change_authority: owner_only",
        "review_execution:",
        "  isolation_mode: fresh_subagent",
        "  inline_fallback: false",
        "  prior_scores_visible_to_reviewer: false",
        "  prior_versions_visible_to_reviewer: false",
        "  revision_deltas_visible_to_reviewer: false",
        "  source_artifacts_read_only: true",
        "skills:",
    ]
    for skill_md in skill_files:
        name = skill_name(skill_md)
        if name in OPENAI_NATIVE_SKILLS:
            native = OPENAI_NATIVE_SKILLS[name]
            package = str(native["package"])
            related = sorted(set(native["related_skills"]))
            unresolved = set(related) - names
            if unresolved:
                raise RuntimeError(
                    f"OpenAI-native skill {name} has unresolved related skills: {sorted(unresolved)}"
                )
        else:
            source_skill = hermes_by_name[name]
            source_relative = source_skill.parent.relative_to(HERMES_SKILLS)
            package = source_relative.parts[0]
            related = related_skills(source_skill, names)
        related = sorted(set(related) | RELATED_SKILL_ADDITIONS.get(name, set()))
        role = role_for(name)
        if name in SKILL_IO_OVERRIDES:
            allowed_inputs, output = SKILL_IO_OVERRIDES[name]
        else:
            allowed_inputs, output = io_contract(role)
        if name in VERIFIER_COMPOSITORS:
            output = "verification_report_and_final_handoff_package"
        lines.extend(
            [
                f"  - name: {quote(name)}",
                f"    package: {quote(package)}",
                f"    role: {quote(role)}",
                f"    related_skills: [{', '.join(quote(item) for item in related)}]",
                f"    invocation_policy: {quote('implicit' if name in implicit else 'explicit_or_orchestrated')}",
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
        "artifact_completeness_policy": ARTIFACT_COMPLETENESS_POLICY,
        "article_docx_delivery_policy": ARTICLE_DOCX_DELIVERY_POLICY,
    }
    lines.extend(yaml.safe_dump(state_registry, sort_keys=False, allow_unicode=True).rstrip().splitlines())

    (PLUGIN / "workflow-registry.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote registry for {len(skill_files)} skills and {len(REVIEWERS)} reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
