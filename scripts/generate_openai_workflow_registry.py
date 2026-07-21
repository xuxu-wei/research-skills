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

LEGACY_SKILL_NAME_ALIASES = {
    "academic-deep-search": "focused-literature-synthesizer",
    "research-opportunity-mapper": "research-landscape-mapper",
}
LEGACY_ARTIFACT_ROLE_ALIASES = {
    "focused_academic_synthesis": "focused_literature_synthesis",
}

REVIEWERS = {
    "academic-language-assessor",
    "idea-narrative-assessor",
    "research-narrative-assessor",
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
    "research-landscape-mapper",
    "focused-literature-synthesizer",
}
RESEARCH_POLISHER_ENTRY = "research-polisher-orchestrator"
PERSONAL_IMPLICIT_ENTRY_SKILLS = PUBLIC_ENTRY_SKILLS - {RESEARCH_POLISHER_ENTRY}

# These skills originate in the OpenAI plugin rather than the maintained
# Hermes profile. Keep their package and dependency declarations explicit so
# registry generation never infers a nonexistent Hermes source directory.
OPENAI_NATIVE_SKILLS = {
    "focused-literature-synthesizer": {
        "package": "research",
        "related_skills": ["research-landscape-mapper"],
    },
    "research-landscape-mapper": {
        "package": "research",
        "related_skills": [
            "focused-literature-synthesizer",
            "research-idea-orchestrator",
            "proposal-orchestrator",
            "article-literature-grounder",
            "perspective-claim-evidence-curator",
            "research-polisher-orchestrator",
        ],
    },
    "idea-narrative-assessor": {
        "package": "research-idea",
        "related_skills": [
            "academic-language-assessor",
            "multi-path-idea-generator",
            "research-context-builder",
            "research-idea-orchestrator",
        ],
    },
    "research-narrative-assessor": {
        "package": "research",
        "related_skills": [
            "academic-language-assessor",
            "article-drafter",
            "article-orchestrator",
            "perspective-drafter",
            "perspective-orchestrator",
            "proposal-drafter",
            "proposal-orchestrator",
            "research-idea-orchestrator",
        ],
    },
    "research-polisher-orchestrator": {
        "package": "research-polisher",
        "related_skills": [
            "focused-literature-synthesizer",
            "article-architect",
            "article-context-builder",
            "medical-journal-review",
            "methodology-statistics-preflight",
            "research-landscape-mapper",
            "research-polisher-methodology-publishability-reviewer",
            "research-polisher-plan-assembler",
            "research-polisher-strategy-reviewer",
        ],
    },
    "research-polisher-strategy-reviewer": {
        "package": "research-polisher",
        "related_skills": [
            "research-landscape-mapper",
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
    "multi-path-idea-generator": (
        "frozen_context_evidence_opportunities_routing_decision_current_dossiers_and_applicable_revision_plan_or_approved_editorial_repair_writer_brief_or_preflight_approved_working_assumptions",
        "versioned_complete_idea_dossiers_revision_delta_and_proposed_navigation_metadata",
    ),
    "idea-evaluator": (
        "one_frozen_complete_idea_dossier_only",
        "idea_evaluation_report",
    ),
    "idea-narrative-assessor": (
        "one_current_idea_dossier_and_reader_handoff_or_preservation_comparison_bundle",
        "narrative_assessment_and_yaml_repair_plan_or_content_preservation_report",
    ),
    "research-narrative-assessor": (
        "one_frozen_current_artifact_or_reader_bundle_and_reader_handoff_or_preservation_comparison_bundle",
        "narrative_assessment_and_yaml_repair_plan_or_content_preservation_report",
    ),
    "idea-portfolio-assembler": (
        "evaluated_current_idea_dossiers_applicable_candidate_journal_matches_medical_reviews_index_lineage_findings_and_dissent",
        "pi_navigation_or_comparison_handoff_package",
    ),
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
    "article-literature-grounder": {"focused-literature-synthesizer"},
    "article-cover-letter": {"perspective-orchestrator", "perspective-final-compositor"},
    "perspective-orchestrator": {"article-cover-letter"},
    "perspective-final-compositor": {"article-cover-letter"},
    "research-idea-orchestrator": {"idea-narrative-assessor", "research-narrative-assessor", "medical-journal-review", "focused-literature-synthesizer"},
    "proposal-orchestrator": {"research-narrative-assessor", "medical-journal-review", "focused-literature-synthesizer"},
    "perspective-orchestrator": {"research-narrative-assessor", "medical-journal-review", "focused-literature-synthesizer"},
    "perspective-claim-evidence-curator": {"focused-literature-synthesizer"},
    "article-orchestrator": {"research-narrative-assessor", "medical-journal-review"},
    "idea-portfolio-assembler": {"medical-journal-review"},
    "academic-language-assessor": {"idea-narrative-assessor", "research-narrative-assessor", "research-idea-orchestrator", "proposal-orchestrator", "perspective-orchestrator", "article-orchestrator"},
}

# workflow, source, destination, dispatch mode, trigger, input contract,
# output contract, failure route
WORKFLOW_EDGES = [
    ("idea", "research-idea-orchestrator", "research-context-builder", "orchestrated", "context_required", "user_inputs_and_constraints", "research_context_brief_and_direction_clarity_signal", "clarification_required"),
    ("idea", "research-idea-orchestrator", "research-landscape-mapper", "orchestrated", "major_evidence_or_novelty_landscape_change", "context_sources_scope_and_current_dossier_when_remapping", "evidence_opportunity_maps_and_direction_support_signals", "evidence_mapping_pending"),
    ("idea", "research-idea-orchestrator", "focused-literature-synthesizer", "orchestrated", "bounded_two_to_five_paper_synthesis_required", "one_bounded_question_scope_and_source_constraints", "focused_literature_synthesis", "evidence_mapping_pending"),
    ("idea", "research-idea-orchestrator", "multi-path-idea-generator", "orchestrated", "routing_decision_ready_or_revision_authorized", "frozen_context_evidence_opportunities_routing_decision_current_dossiers_and_applicable_revision_plan_or_approved_editorial_repair_writer_brief_or_current_preflight_approved_working_assumptions", "versioned_complete_idea_dossiers_revision_delta_and_proposed_navigation_metadata", "generation_blocked"),
    ("idea", "research-idea-orchestrator", "methodology-statistics-preflight", "delegated", "method_or_endpoint_fit_needs_review", "frozen_complete_idea_dossiers_and_method_facts", "preflight_report_and_idea_handoff", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "research-narrative-assessor", "delegated", "scientific_revision_frozen_or_editorial_repair_completed", "one_current_idea_dossier_and_reader_handoff_or_preservation_comparison_bundle", "narrative_assessment_and_yaml_repair_plan_or_content_preservation_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "academic-language-assessor", "delegated", "scientific_revision_frozen_and_editorial_review_pending", "complete_current_idea_dossier_language_scope_and_reader_handoff", "language_assessment_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-evaluator", "delegated", "current_dossier_frozen_after_fresh_narrative_language_readiness_and_preservation_when_applicable", "one_frozen_complete_idea_dossier_only", "idea_evaluation_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "medical-journal-review", "delegated", "final_current_idea_evaluation_valid_and_domain_biomedical_or_clinical", "one_frozen_complete_idea_dossier_and_unscored_unranked_candidate_journal_match_brief_without_evaluator_material", "medical_journal_review_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-adversarial-review-panel", "delegated", "focused_direction_proposal_handoff_candidate_exists", "one_frozen_promoted_complete_idea_dossier_and_role_brief", "sealed_individual_adversarial_report", "independent_review_pending"),
    ("idea", "research-idea-orchestrator", "idea-portfolio-assembler", "orchestrated", "qualifying_focused_review_or_bounded_exploration_reviews_sealed", "evaluated_current_dossiers_applicable_candidate_journal_matches_medical_reviews_readiness_index_lineage_findings_and_dissent", "pi_navigation_or_comparison_handoff_package", "assembly_blocked"),
    ("idea", "research-idea-orchestrator", "proposal-orchestrator", "handoff", "focused_or_human_selected_direction_fresh_promote_and_handoff_gate_passed", "promoted_idea_package_with_section_14_and_unresolved_finding_locators", "proposal_workflow_state", "proposal_handoff_blocked"),

    ("proposal", "proposal-orchestrator", "proposal-context-brief-builder", "orchestrated", "context_brief_required", "idea_draft_call_and_constraints", "proposal_context_brief", "clarification_required"),
    ("proposal", "proposal-orchestrator", "research-landscape-mapper", "orchestrated", "major_core_claim_novelty_landscape_or_conflict_change", "context_sources_and_retrieval_scope", "evidence_and_opportunity_maps", "evidence_mapping_pending"),
    ("proposal", "proposal-orchestrator", "focused-literature-synthesizer", "orchestrated", "bounded_two_to_five_paper_synthesis_required", "one_bounded_question_scope_and_source_constraints", "focused_literature_synthesis", "evidence_mapping_pending"),
    ("proposal", "proposal-orchestrator", "proposal-readiness-triage", "delegated", "context_and_evidence_ready", "frozen_context_evidence_and_scope", "readiness_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "methodology-statistics-preflight", "delegated", "readiness_or_sap_requires_method_preflight", "frozen_design_endpoint_and_data_facts", "preflight_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-drafter", "delegated", "content_plan_required", "frozen_context_evidence_reader_handoff_and_constraints", "proposal_content_plan_yaml", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-drafter", "orchestrated", "content_plan_frozen_or_targeted_revision_authorized", "approved_context_evidence_content_plan_or_revision_plan_or_editorial_brief", "versioned_complete_proposal_and_action_conformance", "drafting_blocked"),
    ("proposal", "proposal-orchestrator", "proposal-refinement-controller", "orchestrated", "scientific_review_panel_or_editorial_readiness_requests_fixable_revision", "sealed_scientific_findings_or_single_editorial_brief_current_version_and_history", "revision_handoff", "revision_blocked"),
    ("proposal", "proposal-refinement-controller", "proposal-drafter", "orchestrated", "revision_plan_or_editorial_brief_frozen", "current_proposal_targeted_plan_or_editorial_brief_and_protected_register", "new_complete_proposal_version_delta_and_action_conformance", "drafting_blocked"),
    ("proposal", "proposal-orchestrator", "sap-writer", "orchestrated", "sap_requested_and_preflight_allows", "approved_design_endpoints_data_and_preflight", "versioned_sap", "sap_drafting_blocked"),
    ("proposal", "proposal-orchestrator", "sap-evaluator", "delegated", "sap_version_frozen", "frozen_sap_stable_rubric_and_facts", "sap_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "sap-refinement-controller", "orchestrated", "sap_evaluation_requests_revision", "sealed_sap_findings_and_current_version", "sap_revision_handoff", "sap_revision_blocked"),
    ("proposal", "sap-refinement-controller", "sap-writer", "orchestrated", "sap_revision_plan_frozen", "current_sap_and_targeted_plan", "new_sap_version_and_delta", "sap_drafting_blocked"),
    ("proposal", "sap-refinement-controller", "sap-evaluator", "delegated", "revised_sap_version_frozen", "latest_sap_stable_rubric_and_facts", "fresh_sap_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "research-narrative-assessor", "delegated", "scientific_revision_frozen_or_editorial_repair_completed", "one_current_proposal_and_reader_handoff_or_preservation_comparison_bundle", "narrative_assessment_and_yaml_repair_plan_or_content_preservation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "academic-language-assessor", "delegated", "scientific_revision_frozen_or_editorial_repair_completed", "complete_current_proposal_language_scope_and_reader_handoff", "language_assessment_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-evaluator", "delegated", "current_proposal_frozen_after_fresh_narrative_language_readiness_and_preservation", "one_final_proposal_stable_rubric_minimal_call_and_factual_inputs", "proposal_evaluation_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-review-panel", "delegated", "final_proposal_evaluation_passed_or_early_mock_explicit", "frozen_final_proposal_and_one_role_brief", "sealed_individual_panel_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "medical-journal-review", "delegated", "final_proposal_evaluation_complete_and_journal_matching_requested_or_applicable", "final_proposal_and_score_free_verified_journal_candidate_brief", "medical_journal_review_report", "independent_review_pending"),
    ("proposal", "proposal-orchestrator", "proposal-package-assembler", "orchestrated", "latest_version_has_qualifying_reviews", "evaluated_proposal_state_reviews_dissent_and_optional_sap", "human_review_proposal_package", "assembly_blocked"),

    ("article", "article-orchestrator", "article-readiness-triage", "delegated", "complete_material_inventory_and_minimal_intake_frozen", "frozen_minimal_intake_complete_material_inventory_semantic_authority_and_entry_scope", "article_readiness_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-context-builder", "orchestrated", "readiness_allows_context_build", "approved_intake_and_scope", "article_context_brief", "clarification_required"),
    ("article", "article-orchestrator", "article-literature-grounder", "orchestrated", "context_ready_and_grounding_required", "context_sources_and_scope", "literature_grounding_report", "grounding_blocked"),
    ("article", "article-literature-grounder", "research-landscape-mapper", "orchestrated", "major_grounding_novelty_landscape_or_conflict_change", "research_question_sources_and_scope", "evidence_map_and_limitations", "evidence_mapping_pending"),
    ("article", "article-literature-grounder", "focused-literature-synthesizer", "orchestrated", "bounded_two_to_five_paper_synthesis_required", "one_bounded_question_scope_and_source_constraints", "focused_literature_synthesis", "evidence_mapping_pending"),
    ("article", "article-orchestrator", "article-architect", "orchestrated", "context_and_grounding_ready", "frozen_context_grounding_and_results", "article_blueprint_and_evidence_contracts", "architecture_blocked"),
    ("article", "article-orchestrator", "methodology-statistics-preflight", "delegated", "quick_method_feasibility_screen_needed", "frozen_design_endpoint_and_data_facts", "preflight_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-methods-statistics-auditor", "delegated", "blueprint_and_method_inputs_frozen", "frozen_context_protocol_outputs_and_scope", "methods_statistics_audit_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-drafter", "orchestrated", "architecture_and_method_gate_allow_drafting", "approved_blueprint_evidence_audit_and_revision_plan", "versioned_manuscript_and_supplements", "drafting_blocked"),
    ("article", "article-orchestrator", "article-claim-auditor", "delegated", "manuscript_version_frozen", "frozen_manuscript_claim_matrix_and_evidence", "claim_audit_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-refinement-controller", "orchestrated", "scientific_audit_panel_or_editorial_readiness_requests_fixable_revision", "sealed_scientific_findings_or_single_editorial_brief_current_version_and_history", "revision_handoff", "revision_blocked"),
    ("article", "article-refinement-controller", "article-drafter", "orchestrated", "revision_plan_or_body_editorial_brief_frozen", "current_manuscript_targeted_plan_or_editorial_brief_and_protected_register", "new_complete_manuscript_version_delta_and_action_conformance", "drafting_blocked"),
    ("article", "article-orchestrator", "article-frontmatter-drafter", "orchestrated", "scientifically_current_manuscript_or_frontmatter_editorial_brief_ready", "current_manuscript_section_plan_journal_adapter_or_frontmatter_editorial_brief_and_protected_register", "versioned_complete_frontmatter_and_action_conformance", "frontmatter_blocked"),
    ("article", "article-orchestrator", "research-narrative-assessor", "delegated", "reader_bundle_frozen_or_editorial_repair_completed", "current_manuscript_frontmatter_reader_bundle_and_reader_handoff_or_preservation_comparison_bundle", "narrative_assessment_and_yaml_repair_plan_or_content_preservation_report", "independent_review_pending"),
    ("article", "article-orchestrator", "academic-language-assessor", "delegated", "reader_bundle_frozen_or_editorial_repair_completed", "complete_current_manuscript_frontmatter_language_scope_and_reader_handoff", "language_assessment_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-evaluator", "delegated", "reader_bundle_frozen_after_fresh_narrative_language_readiness_and_preservation", "final_manuscript_frontmatter_current_displays_stable_rubric_and_minimal_factual_or_outlet_constraints", "article_evaluation_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-review-panel", "delegated", "final_article_evaluation_passed_or_mock_review_explicit", "frozen_final_reader_bundle_and_one_role_brief", "sealed_individual_panel_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-cover-letter", "orchestrated", "frontmatter_and_manuscript_ready", "frozen_manuscript_frontmatter_and_journal_adapter", "cover_letter_and_quality_check", "cover_letter_blocked"),
    ("article", "article-orchestrator", "medical-journal-review", "delegated", "final_evaluation_complete_and_biomedical_review_or_journal_matching_requested", "final_article_score_free_verified_journal_candidate_brief_and_optional_cover_letter_without_evaluator_material", "medical_journal_review_report", "independent_review_pending"),
    ("article", "article-orchestrator", "article-submission-compositor", "delegated", "all_required_artifacts_and_reviews_frozen", "frozen_submission_artifacts_reviews_and_dissent", "verified_human_review_package", "independent_review_pending"),

    ("perspective", "perspective-orchestrator", "perspective-input-builder", "orchestrated", "input_brief_required", "user_thesis_outlet_evidence_and_constraints", "perspective_input_brief", "clarification_required"),
    ("perspective", "perspective-orchestrator", "perspective-claim-evidence-curator", "orchestrated", "input_brief_ready_or_claim_change_approved", "frozen_input_evidence_and_change_requests", "claim_ledger_and_evidence_artifacts", "curation_blocked"),
    ("perspective", "perspective-orchestrator", "research-landscape-mapper", "orchestrated", "major_discourse_novelty_landscape_or_conflict_change", "claims_sources_and_retrieval_scope", "evidence_map_and_limitations", "evidence_mapping_pending"),
    ("perspective", "perspective-claim-evidence-curator", "focused-literature-synthesizer", "orchestrated", "bounded_two_to_five_paper_synthesis_required", "one_bounded_question_scope_and_source_constraints", "focused_literature_synthesis", "evidence_mapping_pending"),
    ("perspective", "perspective-orchestrator", "perspective-argument-architect", "orchestrated", "claim_and_evidence_artifacts_ready", "frozen_input_claims_evidence_and_outlet", "argument_skeleton_and_paragraph_plan", "architecture_blocked"),
    ("perspective", "perspective-orchestrator", "perspective-drafter", "orchestrated", "argument_architecture_ready_revision_plan_or_editorial_brief_frozen", "approved_architecture_claims_revision_plan_or_editorial_brief_and_protected_register", "versioned_complete_perspective_paragraph_map_delta_and_action_conformance", "drafting_blocked"),
    ("perspective", "perspective-orchestrator", "perspective-refinement-controller", "orchestrated", "scientific_panel_or_editorial_readiness_requests_fixable_revision", "sealed_scientific_findings_or_single_editorial_brief_current_version_and_history", "revision_handoff", "revision_blocked"),
    ("perspective", "perspective-refinement-controller", "perspective-drafter", "orchestrated", "revision_plan_or_editorial_brief_frozen", "current_perspective_targeted_plan_or_editorial_brief_and_protected_register", "new_complete_perspective_version_delta_and_action_conformance", "drafting_blocked"),
    ("perspective", "perspective-orchestrator", "research-narrative-assessor", "delegated", "scientific_evaluation_and_applicable_panel_route_closed_or_editorial_repair_completed", "one_current_perspective_and_reader_handoff_or_preservation_comparison_bundle", "narrative_assessment_and_yaml_repair_plan_or_content_preservation_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "academic-language-assessor", "delegated", "scientific_evaluation_and_applicable_panel_route_closed_or_editorial_repair_completed", "complete_current_perspective_language_scope_and_reader_handoff", "language_assessment_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-evaluator", "delegated", "current_perspective_frozen_for_scientific_evaluation_or_post_editorial_final_evaluation", "stage_specific_scientific_package_or_one_final_perspective_stable_rubric_and_minimal_evidence_outlet_facts", "scientific_or_final_perspective_evaluation_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-review-panel", "delegated", "scientific_perspective_evaluation_passed_before_editorial_cycle", "frozen_scientifically_qualified_perspective_and_one_role_brief", "sealed_individual_panel_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "article-cover-letter", "orchestrated", "qualifying_perspective_cover_letter_requested", "frozen_perspective_outlet_core_argument_evidence_and_disclosures", "cover_letter_and_quality_check", "cover_letter_blocked"),
    ("perspective", "perspective-orchestrator", "medical-journal-review", "delegated", "final_evaluation_complete_and_biomedical_review_or_journal_matching_requested", "final_perspective_score_free_verified_journal_candidate_brief_and_optional_cover_letter_without_evaluator_material", "medical_journal_review_report", "independent_review_pending"),
    ("perspective", "perspective-orchestrator", "perspective-final-compositor", "delegated", "all_required_artifacts_and_reviews_frozen", "frozen_final_artifacts_reviews_and_dissent", "verified_human_review_package", "independent_review_pending"),

    ("research_polisher", "research-polisher-orchestrator", "article-context-builder", "orchestrated", "dossier_normalization_required", "frozen_research_assets_scope_and_constraints", "article_context_brief_for_research_polisher", "clarification_required"),
    ("research_polisher", "research-polisher-orchestrator", "research-landscape-mapper", "orchestrated", "major_core_positioning_novelty_landscape_or_conflict_change", "frozen_dossier_questions_sources_and_scope", "evidence_and_opportunity_maps", "evidence_mapping_pending"),
    ("research_polisher", "research-polisher-orchestrator", "focused-literature-synthesizer", "orchestrated", "bounded_two_to_five_paper_question_required", "one_bounded_question_scope_and_source_constraints", "focused_literature_synthesis", "evidence_mapping_pending"),
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
        "editorial_revision_required",
        "panel_pending",
        "packaging_pending",
    ],
    "pause_states": [
        "pending_review",
        "editorial_review_pending",
        "specialist_review_pending",
        "independent_review_pending",
        "direction_route_confirmation_required",
        "clarification_stop",
        "deep_research_handoff_required",
        "new_idea_required",
        "layout_migration_required",
    ],
    "terminal_states": [
        "stopped",
        "blocked",
        "no_defensible_direction",
        "no_defensible_option",
        "human_signoff_required",
        "human_direction_selection_required",
        "human_strategy_selection_required",
        "additional_work_required",
    ],
    "review_unavailable_state": "independent_review_pending",
    "fatal_finding_state": "blocked",
    "final_handoff_state": "human_signoff_required",
    "wildcard_transition_scope": "nonterminal_states_only",
    "resume_policy": {
        "independent_review_pending": "pending_review",
        "direction_route_confirmation_required": "preprocessing",
        "clarification_stop": "preprocessing",
        "deep_research_handoff_required": "preprocessing",
        "editorial_review_pending": "artifact_frozen",
        "new_idea_required": "preprocessing",
        "layout_migration_required": "preprocessing",
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
            "human_direction_selection_required",
            "human_strategy_selection_required",
        ],
    },
    "finding_gate": {
        "fatal_or_blocking_finding_prevents_accept": True,
        "fatal_or_blocking_finding_prevents_promoted": True,
        "fatal_or_blocking_finding_prevents_human_signoff": True,
        "fatal_or_blocking_finding_prevents_human_direction_selection": True,
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
        {"from": "artifact_frozen", "to": "editorial_review_pending", "trigger": "workflow_editorial_readiness_dispatched"},
        {"from": "editorial_review_pending", "to": "editorial_revision_required", "trigger": "workflow_editorial_revision_requested"},
        {"from": "editorial_revision_required", "to": "editorial_revision_required", "trigger": "editorial_scope_violation_requires_writer_repair"},
        {"from": "editorial_revision_required", "to": "revision_required", "trigger": "scientific_change_declared"},
        {"from": "editorial_revision_required", "to": "blocked", "trigger": "identity_drift_detected"},
        {"from": "editorial_revision_required", "to": "new_idea_required", "trigger": "idea_identity_drift_detected"},
        {"from": "editorial_revision_required", "to": "artifact_frozen", "trigger": "preserved_editorial_version_created"},
        {"from": "editorial_review_pending", "to": "artifact_frozen", "trigger": "workflow_editorial_readiness_passed"},
        {"from": "artifact_frozen", "to": "pending_review", "trigger": "independent_review_dispatched"},
        {"from": "pending_review", "to": "revision_required", "trigger": "fixable_revision_requested"},
        {"from": "revision_required", "to": "artifact_frozen", "trigger": "new_version_created"},
        {"from": "revision_required", "to": "new_idea_required", "trigger": "identity_drift_detected"},
        {"from": "preprocessing", "to": "layout_migration_required", "trigger": "legacy_idea_layout_detected"},
        {"from": "new_idea_required", "to": "preprocessing", "trigger": "explicit_new_identity_workflow_started"},
        {"from": "layout_migration_required", "to": "preprocessing", "trigger": "explicit_layout_migration_completed"},
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
            "to": "packaging_pending",
            "trigger": "bounded_exploration_reviews_complete",
            "requires": [
                "evidence_and_opportunity_remap_complete",
                "fresh_evaluation_complete_for_each_current_dossier",
                "no_unresolved_fatal_finding",
            ],
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
        {
            "from": "pending_review",
            "to": "specialist_review_pending",
            "trigger": "biomedical_idea_journal_review_dispatched",
            "requires": [
                "final_current_evaluation_valid",
                "current_dossier_biomedical_or_clinical",
                "candidate_journal_match_brief_current_unscored_unranked",
                "candidate_brief_contains_no_evaluator_material",
            ],
        },
        {
            "from": "specialist_review_pending",
            "to": "pending_review",
            "trigger": "biomedical_idea_journal_review_returned",
            "requires": [
                "fresh_medical_journal_review_current",
                "dossier_and_candidate_brief_logical_refs_match",
                "evaluator_report_not_visible_to_medical_reviewer",
            ],
        },
        {"from": "packaging_pending", "to": "human_signoff_required", "trigger": "package_verified"},
        {
            "from": "packaging_pending",
            "to": "human_direction_selection_required",
            "trigger": "bounded_exploration_comparison_handoff_verified",
            "requires": [
                "evidence_and_opportunity_remap_complete",
                "fresh_evaluation_complete_for_each_current_dossier",
                "no_unresolved_fatal_finding",
            ],
        },
        {
            "from": "human_direction_selection_required",
            "to": "preprocessing",
            "trigger": "human_selected_current_dossier",
            "requires": [
                "selected_current_dossier_logical_ref_match",
                "direction_profile_switched_to_focused_optimization",
            ],
        },
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
        {"from": "*", "to": "direction_route_confirmation_required", "trigger": "idea_direction_route_is_low_confidence_or_conflicted"},
        {"from": "*", "to": "clarification_stop", "trigger": "required_source_facts_missing_or_inconsistent"},
        {"from": "*", "to": "deep_research_handoff_required", "trigger": "inactive_deep_research_required"},
        {"from": "*", "to": "blocked", "trigger": "fatal_or_blocking_finding"},
        {"from": "*", "to": "no_defensible_direction", "trigger": "no_supported_current_or_alternative_idea_direction"},
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
        "primary_artifact_type": "idea_dossier",
        "entry_modes": ["standard", "resume_candidates", "portfolio_only"],
        "entry_gates": {
            "standard": ["context_frozen", "evidence_map_frozen", "routing_decision_frozen", "idea_dossier_versioned"],
            "resume_candidates": ["context_scope_validated", "evidence_scope_validated", "routing_decision_frozen", "idea_dossier_versioned"],
            "portfolio_only": ["latest_version_editorially_ready", "latest_version_independently_evaluated", "biomedical_journal_review_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
        },
        "scenario_entry_gate_contracts": {
            "standard": {
                "context_frozen": {"artifact_roles": ["research_context"]},
                "evidence_map_frozen": {"artifact_roles": ["evidence_map"]},
                "routing_decision_frozen": {"artifact_roles": ["idea_routing_decision"]},
                "idea_dossier_versioned": {"artifact_roles": ["idea_dossier"]},
            },
            "resume_candidates": {
                "context_scope_validated": {"artifact_roles": ["research_context"]},
                "evidence_scope_validated": {"artifact_roles": ["evidence_map"]},
                "routing_decision_frozen": {"artifact_roles": ["idea_routing_decision"]},
                "idea_dossier_versioned": {"artifact_roles": ["idea_dossier"]},
            },
            "portfolio_only": {
                "latest_version_editorially_ready": {
                    "artifact_roles": ["narrative_assessment", "language_assessment_report"],
                },
                "latest_version_independently_evaluated": {
                    "review_skill": "idea-evaluator",
                    "input_artifact_roles": ["idea_dossier"],
                },
                "biomedical_journal_review_complete_or_not_applicable": {
                    "conditional_artifact_roles": ["candidate_journal_match_brief", "medical_journal_review_report"],
                    "required_when": "current_dossier_biomedical_or_clinical",
                    "not_applicable_when": "current_dossier_not_biomedical_or_clinical",
                },
                "dissent_and_fatal_findings_indexed": {
                    "artifact_roles": ["review_finding_index"],
                },
            },
        },
        "before_panel": ["current_dossier_editorial_readiness_complete", "latest_version_independently_evaluated", "no_unresolved_fatal_finding"],
        "before_packaging": ["current_dossier_editorial_readiness_complete", "latest_version_independently_evaluated", "biomedical_journal_review_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
        "before_packaging_by_direction_profile": {
            "focused_optimization": ["adversarial_reports_complete_when_proposal_handoff_candidate"],
            "bounded_exploration": [
                "evidence_and_opportunity_remap_complete",
                "fresh_evaluation_complete_for_each_current_dossier",
            ],
        },
        "non_ready_modes": [],
        "final_package_skill": "idea-portfolio-assembler",
        "internal_direction_profiles": {
            "focused_optimization": {
                "current_dossier_count": 1,
                "revision_round_limit": 3,
                "adversarial_panel_required_before_handoff": True,
                "final_state": "human_signoff_required",
            },
            "bounded_exploration": {
                "current_dossier_count": {"minimum": 2, "maximum": 3},
                "optimization_round_limit_per_direction": 1,
                "evidence_and_opportunity_remap_after_optimization": True,
                "fresh_evaluator_per_current_dossier_after_remap": True,
                "structural_change_after_remap": "revision_required_no_automatic_second_optimization",
                "adversarial_panel_required_before_direction_selection": False,
                "final_state": "human_direction_selection_required",
            },
        },
        "routing_contract": {
            "decision_artifact_role": "idea_routing_decision",
            "clear_supported_direction": "focused_optimization",
            "underdefined_with_two_or_more_supported_directions": "bounded_exploration",
            "maximum_exploration_directions": 3,
            "no_supported_direction": "no_defensible_direction",
            "low_confidence_or_conflict": "direction_route_confirmation_required",
            "never_fill_direction_quota_with_unsupported_candidates": True,
        },
        "evaluation_dispatch_by_direction_profile": {
            "focused_optimization": {
                "eligible_artifact": "current_frozen_idea_dossier",
                "required_preconditions": [
                    "current_dossier_logical_ref_bound",
                    "fresh_narrative_editorially_eligible",
                    "fresh_full_dossier_language_editorially_eligible",
                    "scientific_content_preserved_when_editorially_repaired",
                    "artifact_index_complete",
                ],
            },
            "bounded_exploration": {
                "eligible_artifact": "terminal_current_idea_dossier_only",
                "required_preconditions": [
                    "exactly_one_bounded_optimization_complete_for_direction",
                    "evidence_and_opportunity_remap_complete_for_direction",
                    "post_remap_claim_sync_complete_for_direction",
                    "terminal_dossier_logical_ref_bound",
                    "fresh_narrative_editorially_eligible",
                    "fresh_full_dossier_language_editorially_eligible",
                    "scientific_content_preserved_when_editorially_repaired",
                    "artifact_index_complete",
                ],
                "initial_or_pre_remap_dossier_evaluation_forbidden": True,
            },
        },
        "biomedical_journal_review_contract": {
            "dispatch_after": "final_effective_current_version_evaluation",
            "applicability": "biomedical_or_clinical_domain_or_study_setting",
            "non_applicable_record_required": True,
            "state_while_waiting": "specialist_review_pending",
            "review_skill": "medical-journal-review",
            "reviewer_isolation_mode": "fresh_subagent",
            "candidate_brief_role": "candidate_journal_match_brief",
            "candidate_brief_source_skill": "research-idea-orchestrator",
            "candidate_brief_matching_source_skill": "idea-evaluator",
            "candidate_brief_materialized_by_skill": "research-idea-orchestrator",
            "candidate_brief_schema_version": "research-idea-journal-candidate-brief.v1",
            "candidate_outlets_unranked": True,
            "candidate_brief_scoring_present": False,
            "candidate_brief_publication_probability_present": False,
            "candidate_brief_evaluator_material_included": False,
            "reviewer_allowed_project_artifacts": ["current_complete_idea_dossier", "candidate_journal_match_brief"],
            "reviewer_forbidden_project_artifacts": ["idea_evaluation_report", "prior_scores", "prior_findings", "prior_decisions"],
            "medical_review_route": "idea_journal_match_editorial_review",
            "publication_probability_assessment": None,
            "logical_binding_fields": ["artifact_id", "version", "path"],
            "content_digest_required": False,
            "medical_review_changes_evaluator_score_or_decision": False,
        },
        "proposal_handoff_contract": {
            "eligible_direction_profiles": ["focused_optimization"],
            "required_current_evaluation_decision": "promote",
            "fresh_evaluation_required": True,
            "evaluated_dossier_logical_ref_must_match_current": True,
            "revise_then_promote_is_not_a_handoff_decision": True,
            "revise_then_promote_requires_revision_and_fresh_re_evaluation": True,
        },
    },
    "proposal": {
        "orchestrator": "proposal-orchestrator",
        "evaluator_skill": "proposal-evaluator",
        "primary_writer_skills": ["proposal-drafter"],
        "primary_artifact_creator_skills": ["proposal-drafter"],
        "primary_artifact_type": "proposal",
        "entry_modes": ["standard", "existing_draft", "draft_and_external_review", "package_only"],
        "entry_gates": {
            "standard": ["context_frozen", "readiness_passed", "proposal_content_plan_frozen", "proposal_versioned"],
            "existing_draft": ["minimal_state_created", "scope_limitations_recorded", "proposal_versioned"],
            "draft_and_external_review": ["minimal_state_created", "proposal_versioned", "external_review_qualified_or_fresh_evaluation_required"],
            "package_only": ["latest_version_editorially_ready", "latest_version_independently_evaluated", "required_panel_reports_complete", "biomedical_journal_review_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
        },
        "scenario_entry_gate_contracts": {
            "standard": {
                "context_frozen": {"artifact_roles": ["proposal_context"]},
                "readiness_passed": {
                    "review_skill": "proposal-readiness-triage",
                    "input_artifact_roles": ["proposal_context", "evidence_map"],
                },
                "proposal_content_plan_frozen": {"artifact_roles": ["proposal_content_plan"]},
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
                "latest_version_editorially_ready": {
                    "artifact_roles": ["narrative_assessment", "language_assessment_report"],
                },
                "latest_version_independently_evaluated": {
                    "review_skill": "proposal-evaluator",
                    "input_artifact_roles": ["proposal"],
                },
                "required_panel_reports_complete": {
                    "review_skill": "proposal-review-panel",
                    "input_artifact_roles": ["proposal"],
                },
                "biomedical_journal_review_complete_or_not_applicable": {
                    "conditional_artifact_roles": ["candidate_journal_match_brief", "medical_journal_review_report"],
                    "required_when": "current_proposal_biomedical_or_clinical",
                    "not_applicable_when": "current_proposal_not_biomedical_or_clinical",
                },
                "dissent_and_fatal_findings_indexed": {
                    "artifact_roles": ["review_finding_index"],
                },
            },
        },
        "before_panel": ["current_proposal_editorial_readiness_complete", "latest_version_independently_evaluated", "no_unresolved_fatal_finding"],
        "before_packaging": ["current_proposal_editorial_readiness_complete", "latest_version_independently_evaluated", "required_panel_reports_complete_or_not_applicable", "biomedical_journal_review_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
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
                    "input_artifact_roles": ["minimal_intake", "complete_material_inventory", "semantic_authority_record"],
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
                    "input_artifact_roles": ["minimal_intake", "complete_material_inventory", "semantic_authority_record"],
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
                    "input_artifact_roles": ["minimal_intake", "complete_material_inventory", "semantic_authority_record"],
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
                    "input_artifact_roles": ["minimal_intake", "complete_material_inventory", "semantic_authority_record"],
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
                    "input_artifact_roles": ["minimal_intake", "complete_material_inventory", "semantic_authority_record", "manuscript"],
                },
                "manuscript_versioned": {"artifact_roles": ["manuscript"]},
                "latest_version_independently_evaluated": {
                    "review_skill": "article-evaluator",
                    "input_artifact_roles": ["manuscript"],
                },
            },
        },
        "before_panel": ["current_reader_bundle_editorial_readiness_complete", "latest_version_independently_evaluated", "claim_audit_passed", "no_unresolved_fatal_finding"],
        "before_packaging": ["current_reader_bundle_editorial_readiness_complete", "latest_version_independently_evaluated", "required_panel_reports_complete_or_not_applicable", "biomedical_journal_review_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
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
        "before_panel": ["current_perspective_scientific_evaluation_complete", "no_unresolved_fatal_finding"],
        "before_packaging": ["current_perspective_editorial_readiness_complete", "final_perspective_evaluation_complete", "panel_reports_complete", "biomedical_journal_review_complete_or_not_applicable", "dissent_and_fatal_findings_indexed"],
        "evaluation_stage_contract": {
            "scientific": {
                "dispatch_before": "panel",
                "required_input_roles": ["perspective", "argument_architecture", "paragraph_map", "claim_ledger", "claim_evidence_matrix", "perspective_input_brief", "target_outlet_profile", "existing_discourse_baseline"],
                "prior_scores_or_decisions_visible": False,
            },
            "final": {
                "dispatch_after": ["applicable_panel_route_closed", "editorial_readiness_complete", "content_preservation_complete"],
                "required_input_roles": ["perspective", "minimal_evidence_outlet_facts"],
                "forbidden_input_roles": ["perspective_input_brief", "argument_architecture", "paragraph_map", "claim_ledger", "claim_evidence_matrix", "repair_brief", "content_preservation_report", "narrative_assessment", "language_assessment_report", "prior_evaluation", "panel_report"],
                "prior_scores_or_decisions_visible": False,
            },
        },
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
    "research-narrative-assessor": {
        "allowed": [
            "narrative_ready",
            "minor_narrative_revision",
            "major_narrative_revision",
            "clarification_required",
            "independent_review_pending",
            "scientific_content_preserved",
            "editorial_scope_violation",
            "identity_drift_detected",
            "scientific_change_declared",
        ],
        "pass": ["narrative_ready", "minor_narrative_revision", "scientific_content_preserved"],
        "revise": ["major_narrative_revision", "editorial_scope_violation"],
        "stop": ["clarification_required", "independent_review_pending", "identity_drift_detected", "scientific_change_declared"],
        "mode_specific_decisions": {
            "narrative": ["narrative_ready", "minor_narrative_revision", "major_narrative_revision", "clarification_required", "independent_review_pending"],
            "preservation": ["scientific_content_preserved", "editorial_scope_violation", "identity_drift_detected", "scientific_change_declared"],
        },
    },
    "idea-narrative-assessor": {
        "allowed": [
            "narrative_ready",
            "minor_narrative_revision",
            "major_narrative_revision",
            "clarification_required",
            "scientific_content_preserved",
            "editorial_scope_violation",
            "identity_drift_detected",
            "scientific_change_declared",
        ],
        "pass": ["narrative_ready", "minor_narrative_revision", "scientific_content_preserved"],
        "revise": ["major_narrative_revision", "editorial_scope_violation"],
        "stop": ["clarification_required", "identity_drift_detected", "scientific_change_declared"],
        "mode_specific_decisions": {
            "narrative": ["narrative_ready", "minor_narrative_revision", "major_narrative_revision", "clarification_required"],
            "preservation": ["scientific_content_preserved", "editorial_scope_violation", "identity_drift_detected", "scientific_change_declared"],
        },
    },
    "academic-language-assessor": {
        "allowed": ["submission_ready", "minor_language_revision", "major_language_revision", "needs_professional_editing", "clarification_required", "independent_review_pending"],
        "pass": ["submission_ready", "minor_language_revision"],
        "revise": ["major_language_revision", "needs_professional_editing"],
        "stop": ["clarification_required", "independent_review_pending"],
    },
    "medical-journal-review": {
        "allowed": ["support", "support_with_minor_revision", "major_revision_required", "redesign_required", "not_reviewable_with_current_materials", "fatal_flaw", "journal_candidates_confirmed", "journal_candidates_revised", "no_supported_journal_candidate"],
        "pass": ["support", "journal_candidates_confirmed", "journal_candidates_revised", "no_supported_journal_candidate"],
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
        "allowed": ["promote", "revise_then_promote", "revise", "reframe", "keep_as_backup", "reject"],
        "pass": ["promote"],
        "revise": ["revise_then_promote", "revise", "reframe"],
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
        "pass": ["pass", "conditionally_pass_with_author_verification"],
        "revise": ["requires_methods_clarification"],
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
        "allowed_roles": ["research_context", "evidence_map", "opportunity_map", "idea_routing_decision", "idea_index", "idea_dossier", "reference_ledger", "preflight_report", "protected_content_register", "narrative_assessment", "narrative_repair_plan", "language_assessment_report", "editorial_repair_writer_brief", "content_preservation_report", "evaluation_report", "candidate_journal_match_brief", "medical_journal_review_report", "panel_report", "revision_plan", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "research_context", "source_skill": "research-context-builder", "count": 1},
            {"artifact_role": "evidence_map", "source_skill": "research-landscape-mapper", "count": 1, "count_by_direction_profile": {"focused_optimization": 1, "bounded_exploration": {"minimum": 2, "maximum": 3}}},
            {"artifact_role": "opportunity_map", "source_skill": "research-landscape-mapper", "count_per_current_idea_node": 1, "required_when_direction_profile": "bounded_exploration"},
            {"artifact_role": "idea_routing_decision", "source_skill": "research-idea-orchestrator", "count": 1},
            {"artifact_role": "idea_index", "source_skills": ["research-idea-orchestrator", "external-input"], "count": 1},
            {"artifact_role": "idea_dossier", "source_skills": ["multi-path-idea-generator", "external-input"], "current_by_idea_index": True, "minimum_count": 1, "maximum_count": 3, "count_by_direction_profile": {"focused_optimization": 1, "bounded_exploration": {"minimum": 2, "maximum": 3}}},
            {"artifact_role": "reference_ledger", "source_skills": ["research-idea-orchestrator", "external-input"], "count_per_current_idea_node": 1},
            {"artifact_role": "narrative_assessment", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "count_must_equal_current_idea_dossier_count": True},
            {"artifact_role": "language_assessment_report", "source_skill": "academic-language-assessor", "current_primary_lineage": True, "count_must_equal_current_idea_dossier_count": True},
            {"artifact_role": "content_preservation_report", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "required_when_condition": "editorial_repair_occurred", "count_per_editorially_repaired_current_dossier": 1},
            {"artifact_role": "evaluation_report", "source_skill": "idea-evaluator", "current_primary_lineage": True, "count_must_equal_current_idea_dossier_count": True},
            {"artifact_role": "candidate_journal_match_brief", "source_skill": "research-idea-orchestrator", "matching_source_skill": "idea-evaluator", "materialized_by_skill": "research-idea-orchestrator", "schema_version": "research-idea-journal-candidate-brief.v1", "current_primary_lineage": True, "required_when_condition": "current_dossier_biomedical_or_clinical", "count_per_applicable_current_dossier": 1, "scoring_forbidden": True, "ranking_forbidden": True, "evaluator_material_forbidden": True},
            {"artifact_role": "medical_journal_review_report", "source_skill": "medical-journal-review", "current_primary_lineage": True, "required_when_condition": "current_dossier_biomedical_or_clinical", "count_per_applicable_current_dossier": 1, "fresh_review_required": True, "evaluator_report_visible": False},
            {"artifact_role": "panel_report", "source_skill": "idea-adversarial-review-panel", "all_panel_instances": True, "count_from_panel_roles": True, "required_when_condition": "proposal_handoff_candidate"},
            {"artifact_role": "revision_plan", "source_skill": "research-idea-orchestrator", "minimum_count": 0, "maximum_count": 3, "include_all_created": True, "count_by_direction_profile": {"focused_optimization": {"minimum": 0, "maximum": 3}, "bounded_exploration": {"minimum": 2, "maximum": 3}}},
            {"artifact_role": "narrative_repair_plan", "source_skill": "research-narrative-assessor", "minimum_count": 0, "include_all_created": True},
            {"artifact_role": "protected_content_register", "source_skill": "research-idea-orchestrator", "minimum_count": 0, "include_all_created": True},
            {"artifact_role": "editorial_repair_writer_brief", "source_skill": "research-idea-orchestrator", "minimum_count": 0, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "multi-path-idea-generator", "minimum_count": 0, "maximum_count": 6, "include_all_created": True, "count_by_direction_profile": {"focused_optimization": {"minimum": 0, "maximum": 3}, "bounded_exploration": {"minimum": 4, "maximum": 6}}},
        ],
    },
    "proposal": {
        "allowed_roles": ["proposal_context", "readiness_report", "proposal_content_plan", "proposal", "protected_content_register", "narrative_assessment", "narrative_repair_plan", "language_assessment_report", "editorial_repair_writer_brief", "content_preservation_report", "evaluation_report", "preflight_report", "sap", "panel_report", "candidate_journal_match_brief", "medical_journal_review_report", "revision_plan", "response_to_reviewers", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "proposal_context", "source_skill": "proposal-context-brief-builder", "count": 1},
            {"artifact_role": "readiness_report", "source_skill": "proposal-readiness-triage", "count": 1},
            {"artifact_role": "proposal_content_plan", "source_skill": "proposal-drafter", "count": 1, "fresh_planner_required": True},
            {"artifact_role": "proposal", "source_skills": ["proposal-drafter", "external-input"], "current_primary": True, "count": 1},
            {"artifact_role": "narrative_assessment", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "language_assessment_report", "source_skill": "academic-language-assessor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "content_preservation_report", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "required_when_condition": "editorial_repair_occurred", "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "proposal-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "preflight_report", "source_skill": "methodology-statistics-preflight", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "sap", "source_skill": "sap-writer", "latest_selected_artifact": True, "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "sap-evaluator", "selected_artifact_lineage_role": "sap", "exact_selected_artifact_lineage": True, "fresh_review_required": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "proposal-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "medical_journal_review_report", "source_skill": "medical-journal-review", "required_when_condition": "journal_matching_requested_or_biomedical_candidate_route", "fresh_review_required": True, "evaluator_report_visible": False},
            {"artifact_role": "revision_plan", "source_skill": "proposal-refinement-controller", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "response_to_reviewers", "source_skill": "proposal-drafter", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "proposal-drafter", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "article": {
        "allowed_roles": ["manuscript", "article_blueprint", "claim_evidence_matrix", "evidence_ledger", "readiness_report", "protected_content_register", "narrative_assessment", "narrative_repair_plan", "language_assessment_report", "editorial_repair_writer_brief", "content_preservation_report", "evaluation_report", "audit_report", "panel_report", "journal_adapter", "frontmatter", "candidate_journal_match_brief", "cover_letter", "quality_check", "medical_journal_review_report", "revision_plan", "response_to_reviewers", "revision_delta"],
        "required_inputs": [
            {"artifact_role": "manuscript", "source_skills": ["article-drafter", "external-input"], "current_primary": True, "count": 1},
            {"artifact_role": "article_blueprint", "source_skill": "article-architect", "count": 1},
            {"artifact_role": "claim_evidence_matrix", "source_skill": "article-architect", "count": 1},
            {"artifact_role": "evidence_ledger", "source_skill": "article-literature-grounder", "count": 1},
            {"artifact_role": "readiness_report", "source_skill": "article-readiness-triage", "count": 1},
            {"artifact_role": "narrative_assessment", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "language_assessment_report", "source_skill": "academic-language-assessor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "content_preservation_report", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "required_when_condition": "editorial_repair_occurred", "count": 1},
            {"artifact_role": "evaluation_report", "source_skill": "article-evaluator", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "audit_report", "source_skill": "article-methods-statistics-auditor", "count": 1},
            {"artifact_role": "audit_report", "source_skill": "article-claim-auditor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "panel_report", "source_skill": "article-review-panel", "all_panel_instances": True, "count_from_panel_roles": True},
            {"artifact_role": "journal_adapter", "source_skill": "article-architect", "count": 1},
            {"artifact_role": "frontmatter", "source_skill": "article-frontmatter-drafter", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "cover_letter", "source_skill": "article-cover-letter", "count": 1},
            {"artifact_role": "quality_check", "source_skill": "article-cover-letter", "count": 1},
            {"artifact_role": "revision_plan", "source_skill": "article-refinement-controller", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "response_to_reviewers", "source_skill": "article-drafter", "minimum_count": 1, "include_all_created": True},
            {"artifact_role": "revision_delta", "source_skill": "article-drafter", "minimum_count": 1, "include_all_created": True},
        ],
    },
    "perspective": {
        "allowed_roles": ["perspective", "target_outlet_profile", "claim_ledger", "claim_evidence_matrix", "evidence_limitations", "citation_risk_log", "contrary_evidence_log", "reference_list", "protected_content_register", "narrative_assessment", "narrative_repair_plan", "language_assessment_report", "editorial_repair_writer_brief", "content_preservation_report", "evaluation_report", "panel_report", "candidate_journal_match_brief", "cover_letter", "quality_check", "medical_journal_review_report"],
        "required_inputs": [
            {"artifact_role": "perspective", "source_skill": "perspective-drafter", "current_primary": True, "count": 1},
            {"artifact_role": "target_outlet_profile", "source_skill": "perspective-input-builder", "count": 1},
            {"artifact_role": "claim_ledger", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "claim_evidence_matrix", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "evidence_limitations", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "citation_risk_log", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "contrary_evidence_log", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "reference_list", "source_skill": "perspective-claim-evidence-curator", "count": 1},
            {"artifact_role": "narrative_assessment", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "language_assessment_report", "source_skill": "academic-language-assessor", "current_primary_lineage": True, "count": 1},
            {"artifact_role": "content_preservation_report", "source_skill": "research-narrative-assessor", "current_primary_lineage": True, "required_when_condition": "editorial_repair_occurred", "count": 1},
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
            {"artifact_role": "evidence_map", "source_skill": "research-landscape-mapper", "count": 1},
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
    "fixture_schema_version": 3,
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
        "frozen",
    ],
    "legacy_optional_lineage_fields": ["content_digest"],
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
    "workflow_review_extensions": {
        "idea-evaluator": {
            "required_fields": [
                "reviewed_dossier_ref",
                "complete_dossier_confirmed",
                "dossier_only_input_confirmed",
            ],
            "finding_required_fields": ["title", "dossier_locator"],
            "exact_input_artifact_count": 1,
            "allowed_input_artifact_roles": ["idea_dossier"],
        },
    },
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
            "research-idea-orchestrator": ["idea_routing_decision", "idea_index", "reference_ledger", "revision_plan", "protected_content_register", "editorial_repair_writer_brief", "candidate_journal_match_brief", "continuation_brief"],
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
            "research-landscape-mapper": ["evidence_map", "opportunity_map"],
            "focused-literature-synthesizer": ["focused_literature_synthesis"],
            "article-literature-grounder": ["evidence_ledger", "evidence_map", "literature_grounding_report"],
            "multi-path-idea-generator": ["idea_dossier", "revision_delta", "proposed_navigation_metadata"],
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
            "research-narrative-assessor": ["narrative_assessment", "narrative_repair_plan", "content_preservation_report"],
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
                    "resume_candidates": ["source_material", "user_constraints", "idea_dossier", "idea_index", "reference_ledger"],
                    "portfolio_only": ["source_material", "idea_dossier", "idea_index", "reference_ledger"],
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
    "workflow_conditional_final_states": {
        "idea": {
            "bounded_exploration": "human_direction_selection_required",
        },
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
    "idea_schema": "research-idea.v3",
    "idea_current_artifact": "complete_markdown_dossier",
    "idea_node_layout": "03_ideas/nodes/<idea-id>",
    "idea_tree_mode": "flat_nodes_with_parent_ids",
    "idea_dossier_layout": "03_ideas/nodes/<idea-id>/dossiers/idea-dossier-vNNN.md",
    "idea_dossier_change_types": ["create", "revise", "evidence_claim_sync", "editorial_reposition", "editorial_repair"],
    "idea_index_role": "idea_index",
    "idea_reference_ledger_role": "reference_ledger",
    "idea_routing_decision_role": "idea_routing_decision",
    "idea_legacy_schemas": ["research-idea.v1", "research-idea.v2"],
    "idea_legacy_layout_behavior": "layout_migration_required_read_only_no_automatic_rewrite",
    "core_identity_drift_behavior": "new_idea_required_no_automatic_branch",
    "idea_current_dossier_cardinality": {
        "focused_optimization": 1,
        "bounded_exploration": {"minimum": 2, "maximum": 3},
    },
    "idea_required_dossier_sections": [
        "title_summary_audience_and_positioning",
        "structured_abstract",
        "background_state_gap_significance_and_rationale",
        "research_question_objectives_and_core_hypotheses",
        "research_content_and_work_modules",
        "data_materials_and_existing_evidence_base",
        "study_design_and_methods",
        "key_technologies_and_implementation_points",
        "semi_structured_evidence_chains",
        "required_analyses_and_evidence",
        "expected_outputs_falsification_criteria_and_interpretation",
        "contribution_innovation_impact_applications_and_closest_work",
        "title_and_positioning_claim_support_table",
        "feasibility_resources_risks_alternatives_and_stop_conditions",
        "references",
    ],
    "idea_evidence_chain_contract": {
        "required_fields": [
            "input",
            "method_analysis_or_processing",
            "output",
            "supported_objective_or_claim",
        ],
        "every_major_objective_and_hypothesis_has_output": True,
        "every_output_traces_to_input_and_processing": True,
        "expected_outputs_must_not_be_presented_as_observed_results": True,
    },
    "idea_editorial_repositioning_contract": {
        "title_audience_and_positioning_changes_allowed": True,
        "added_work_required_for_supported_repositioning": False,
        "supported_editorial_repositioning_is_not_identity_drift": True,
        "editorial_change_creates_new_dossier_version": True,
        "editorial_change_requires_fresh_evaluation": True,
        "editorial_change_requires_content_preservation_and_fresh_readiness": True,
        "limitations_single_authority_section": "section_14",
        "limitations_omitted_elsewhere_unless_required_to_explain_immediate_reasoning": True,
        "reader_reasoning_chain_required": ["background", "current_state", "gap", "significance", "rationale"],
        "all_title_and_positioning_claims_must_be_supported_by_implementation": True,
        "claim_support_states": ["supported", "qualified", "unsupported"],
        "contribution_frames": ["scientific_discovery", "method", "validation", "replication", "application", "resource", "benchmark", "practical", "translational", "integration", "editorial_repositioning"],
        "qualified_claims_require_visible_qualifiers": True,
        "unsupported_claims_forbidden_in_title_summary_and_primary_positioning": True,
        "similar_work_does_not_automatically_require_new_work": True,
        "novel_method_data_or_discovery_claim_requires_real_increment": True,
    },
    "idea_internal_marker_policy": {
        "opaque_workflow_markers_forbidden_in_dossier_prose": True,
        "standard_academic_citations_allowed": True,
        "user_visible_internal_markers_require_human_label_and_ledger_resolution": True,
    },
    "idea_evaluator_project_input_contract": {
        "allowed_project_artifacts": ["current_complete_idea_dossier"],
        "exact_project_artifact_count": 1,
        "forbidden_project_artifacts": [
            "research_context",
            "evidence_map",
            "opportunity_map",
            "preflight_report",
            "reference_ledger",
            "prior_dossier",
            "revision_delta",
            "anonymous_must_fix_list",
            "prior_report",
            "prior_score",
            "prior_decision",
        ],
        "stable_rubric_is_skill_instruction_not_project_artifact": True,
        "readiness_reports_visible": False,
        "logical_binding_fields": ["artifact_id", "version", "path"],
        "content_digest_required": False,
    },
    "idea_biomedical_journal_review_contract": {
        "dispatch_after": "final_effective_current_version_evaluation",
        "applicability": "biomedical_or_clinical_domain_or_study_setting",
        "candidate_brief_artifact_role": "candidate_journal_match_brief",
        "candidate_brief_schema_version": "research-idea-journal-candidate-brief.v1",
        "candidate_brief_matching_source_skill": "idea-evaluator",
        "candidate_brief_materialized_by_skill": "research-idea-orchestrator",
        "candidate_brief_contains_unranked_outlets": True,
        "candidate_brief_scoring_forbidden": True,
        "candidate_brief_publication_probability_forbidden": True,
        "candidate_brief_evaluator_material_forbidden": True,
        "reviewer_skill": "medical-journal-review",
        "reviewer_reads_exactly": ["current_complete_idea_dossier", "candidate_journal_match_brief"],
        "reviewer_forbidden_inputs": ["idea_evaluation_report", "prior_scores", "prior_findings", "prior_decisions"],
        "reviewer_isolation_mode": "fresh_subagent",
        "review_route": "idea_journal_match_editorial_review",
        "publication_probability_assessment": None,
        "review_output_artifact_role": "medical_journal_review_report",
        "logical_binding_fields": ["artifact_id", "version", "path"],
        "content_digest_required": False,
    },
    "idea_editorial_readiness_contract": {
        "runs_after_scientific_revision_before_evaluation": True,
        "parallel_reviewers": ["research-narrative-assessor", "academic-language-assessor"],
        "editorially_eligible_narrative_decisions": ["narrative_ready", "minor_narrative_revision"],
        "editorially_eligible_language_decisions": ["submission_ready", "minor_language_revision"],
        "eligibility_requires_no_unresolved_major_narrative_finding": True,
        "eligibility_requires_no_unresolved_critical_or_major_language_finding": True,
        "idea_scope_overrides_global_language_minor_revision_action": True,
        "ordinary_repair_decisions": ["major_narrative_revision", "major_language_revision"],
        "clarification_required_route": "clarification_stop_then_fresh_assessment",
        "needs_professional_editing_route": "editorial_revision_required_external_language_support_then_fresh_assessment",
        "repair_plan_format": "yaml",
        "repair_requires_protected_content_register": True,
        "writer_interface_artifact_role": "editorial_repair_writer_brief",
        "writer_interface_source_skill": "research-idea-orchestrator",
        "writer_brief_construction_reads_exactly": ["current_idea_dossier", "narrative_assessment", "narrative_repair_plan", "language_assessment_report", "protected_content_register"],
        "writer_brief_requires_source_review_binding": True,
        "writer_brief_requires_source_coverage_validation": True,
        "writer_reads_exactly": ["current_idea_dossier", "editorial_repair_writer_brief", "protected_content_register"],
        "writer_forbidden_editorial_inputs": ["narrative_assessment", "narrative_repair_plan", "language_assessment_report"],
        "writer_brief_requires_all_blocking_findings_and_resolved_overlaps": True,
        "repair_requires_fresh_content_preservation_review": True,
        "repair_requires_fresh_narrative_and_language_reassessment": True,
        "evaluator_reads_editorial_artifacts": False,
        "record_only_minor_observation": {
            "single_report_path": "tests/idea-narrative-forward-0.9.0-preview.3/error-localization-report-r001.md",
            "required_conditions": [
                "severity_minor_or_suggestion",
                "localized_scope",
                "no_scientific_or_content_preservation_change",
                "no_decision_or_reader_eligibility_effect",
                "no_broad_recurrence",
            ],
            "required_fields": [
                "plugin_version",
                "observed_symptom",
                "suspected_diagnosis",
                "proposed_solution",
            ],
            "forbidden_followups": ["new_correction", "reproduction_attempt", "extra_test"],
            "blocking_exceptions": [
                "critical_or_major_finding",
                "content_drift",
                "decision_or_readiness_effect",
                "broad_contamination",
                "invalid_deterministic_result",
            ],
        },
        "repair_outcome_attribution_contract": {
            "required_when": "fresh_reassessment_retains_blocking_finding_or_explicit_diagnostic_run",
            "cardinality_when_required": 1,
            "successful_production_repair_may_omit": True,
            "fresh_reassessment_closed_is_optional_validation_receipt": True,
            "allowed": [
                "source_input_or_context_handoff_failure",
                "assessor_coverage_failure",
                "assessor_variance",
                "brief_normalization_failure",
                "writer_execution_failure",
                "writer_regression",
                "context_attention_failure",
                "workflow_contract_conflict",
                "fresh_reassessment_closed",
            ],
            "readable_fingerprint_fields": [
                "finding_level",
                "scientific_role",
                "normalized_locator",
                "failure_mode",
            ],
            "hash_forbidden": True,
            "context_attention_diagnostic_opt_in": True,
            "context_attention_failure_requires": [
                "explicit_brief_action_with_acceptance_test",
                "full_context_action_omitted_or_failed",
                "same_writer_instance_succeeds_in_deterministic_bounded_section_view",
                "no_better_supported_alternative_attribution",
            ],
        },
    },
    "proposal_current_artifact": "complete_proposal",
    "proposal_content_plan_role": "proposal_content_plan",
    "proposal_content_plan_required_before_new_full_draft": True,
    "proposal_reader_bundle": ["current_complete_proposal"],
    "article_schema": "research-article.v7",
    "article_current_artifact": "complete_canonical_markdown",
    "article_entry_material_contract": {
        "complete_inventory_required": True,
        "semantic_authority_must_be_explicit": True,
        "compatible_supporting_assets_retained": True,
        "filename_or_version_whitelist_must_not_hide_supplied_material": True,
    },
    "article_reader_bundle": ["current_complete_manuscript", "current_frontmatter", "current_required_displays"],
    "perspective_current_artifact": "complete_perspective",
    "perspective_content_plan_role": "argument_architecture_and_paragraph_map",
    "perspective_reader_bundle": ["current_complete_perspective"],
    "fresh_re_evaluation": {
        "scope": "all_complete_workflows",
        "allowed": ["current_complete_final_artifact_or_reader_bundle", "stable_rubric", "minimal_necessary_facts_or_outlet_constraints"],
        "forbidden": ["prior_artifact", "planning_or_context_artifact", "scientific_audit", "narrative_or_language_report", "repair_plan_or_brief", "protected_content_register", "content_preservation_report", "revision_delta", "anonymous_must_fix_list", "prior_report", "prior_score", "prior_decision"],
        "orchestrator_compares_sealed_rounds_after_return": True,
    },
}

CROSS_WORKFLOW_EDITORIAL_READINESS_POLICY = {
    "schema_version": 1,
    "workflows": ["idea", "proposal", "perspective", "article"],
    "macro_reviewer": "research-narrative-assessor",
    "meso_micro_reviewer": "academic-language-assessor",
    "reviewers_run_in_parallel_on_same_frozen_reader_artifact_or_bundle": True,
    "reviewer_role_separation": {
        "research-narrative-assessor": [
            "reader_reasoning_chain",
            "section_function",
            "progressive_disclosure",
            "cross_section_repetition",
            "positive_claim_and_caveat_balance",
            "title_summary_question_contribution_alignment",
        ],
        "academic-language-assessor": [
            "sentence_and_paragraph_language",
            "terminology_accessibility_and_consistency",
            "bilingual_term_drift",
            "unnatural_metaphor",
            "internal_workflow_language_leakage",
        ],
    },
    "terminology_policy": {
        "separate_terminology_skill_or_artifact_forbidden": True,
        "reviewer": "academic-language-assessor",
        "focused_verification_trigger": "a_core_term_is_uncertain_misleading_or_inaccessible_to_target_readers",
        "core_term_roles": ["title", "summary_or_abstract", "question", "objective", "contribution", "study_object", "measurement", "inference", "design", "interpretation"],
        "choice_priority": ["domain_standard", "cross_disciplinary_standard", "domain_comprehensible_plain_term", "necessary_coined_term"],
        "single_paper_is_insufficient_to_establish_standard_usage": True,
        "problem_output_requires": ["exact_locator", "exact_replacement_or_rewrite", "first_use_definition_when_needed", "supporting_evidence"],
    },
    "limitation_policy": {
        "one_complete_authoritative_location_per_document_or_distinct_argument_family": True,
        "omit_elsewhere": True,
        "cross_reference_or_pointer_elsewhere_forbidden": True,
        "exception": "repeat_only_when_the_limitation_itself_is_needed_to_advance_the_immediate_reasoning_and_omission_would_distort_it",
        "narrative_continuity_has_priority_over_defensive_repetition": True,
    },
    "repair_interface": {
        "raw_assessment_reports_visible_to_writer": False,
        "single_writer_brief_format": "yaml",
        "writer_brief_built_by_orchestrator": True,
        "writer_reads": ["current_complete_artifact_or_bundle", "editorial_repair_writer_brief", "protected_content_register"],
        "writer_uses_same_owner_for_bounded_section_passes": True,
        "multiple_fragment_writers_forbidden": True,
        "one_final_complete_artifact_required": True,
        "action_conformance_receipt_required": True,
    },
    "conditional_methodology_policy": {
        "conditional_pass_requires_specific_bounded_assumption": True,
        "writer_proceeds_under_passed_assumption": True,
        "assumption_recorded_once_in_contract_designated_assumptions_location": True,
        "assumption_is_visible_as_research_progression_risk": True,
        "unbounded_or_outcome_changing_uncertainty_cannot_conditionally_pass": True,
    },
    "preservation": {
        "protected_content_register_required_before_editorial_repair": True,
        "fresh_independent_preservation_review_required_after_repair": True,
        "only_scientific_content_preserved_may_continue": True,
        "scientific_change_must_return_to_scientific_review": True,
    },
    "fresh_readiness": {
        "fresh_narrative_and_language_reassessment_required_after_repair": True,
        "all_blocking_findings_must_close_before_final_evaluation": True,
    },
    "final_evaluator_isolation": {
        "allowed": ["current_final_reader_artifact_or_bundle", "stable_skill_rubric", "minimal_necessary_facts_or_outlet_constraints"],
        "forbidden": ["older_draft", "planning_or_context_artifact", "scientific_audit", "narrative_or_language_report", "repair_plan_or_writer_brief", "protected_content_register", "content_preservation_report", "revision_delta", "prior_evaluation_or_decision"],
        "exact_files_read_must_be_reported": True,
        "binding_fields": ["artifact_id", "version", "exact_path"],
        "sha_or_content_digest_required": False,
    },
    "logical_integrity": {
        "required": ["artifact_id", "version", "exact_path", "frozen_state", "complete_artifact_index", "unique_current_pointer"],
        "sha_or_content_digest_forbidden_in_new_llm_facing_artifacts": True,
        "legacy_digest_fields": "readable_but_ignored",
    },
    "context_attention_diagnosis": {
        "context_length_is_not_assumed_from_one_miss": True,
        "requires_same_writer_full_context_miss_and_bounded_view_success": True,
        "requires_input_assessor_and_brief_failures_excluded_first": True,
    },
    "simple_case_behavior": {
        "short_five_function_chain_allowed": True,
        "no_problem_returns_ready_without_repair": True,
        "terminology_verification_only_when_triggered": True,
        "long_term_table_or_repair_plan_not_forced": True,
    },
}

ARTICLE_DOCX_DELIVERY_POLICY = {
    "content_authority": "canonical_markdown",
    "primary_user_delivery_when_capable": "docx",
    "display_manifest": "04_blueprint/display-asset-manifest.yaml",
    "faithful_format_transform_only": True,
    "required_ready_gates": [
        "qualifying_markdown_logical_identity_and_current_pointer_match",
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
    values = [LEGACY_SKILL_NAME_ALIASES.get(value, value) for value in values]
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
    if name in {"research-landscape-mapper", "focused-literature-synthesizer"}:
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
        "schema_version: 6",
        f"plugin_version: {quote(plugin_version)}",
        "legacy_skill_name_aliases:",
        *[f"  {old}: {new}" for old, new in LEGACY_SKILL_NAME_ALIASES.items()],
        "legacy_artifact_role_aliases:",
        *[f"  {old}: {new}" for old, new in LEGACY_ARTIFACT_ROLE_ALIASES.items()],
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
        "cross_workflow_editorial_readiness_policy": CROSS_WORKFLOW_EDITORIAL_READINESS_POLICY,
        "article_docx_delivery_policy": ARTICLE_DOCX_DELIVERY_POLICY,
    }
    lines.extend(yaml.safe_dump(state_registry, sort_keys=False, allow_unicode=True).rstrip().splitlines())

    (PLUGIN / "workflow-registry.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote registry for {len(skill_files)} skills and {len(REVIEWERS)} reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
