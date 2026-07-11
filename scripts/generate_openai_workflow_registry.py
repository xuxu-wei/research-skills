#!/usr/bin/env python3
"""Generate the machine-auditable registry for the OpenAI research plugin."""

from __future__ import annotations

import json
import re
from pathlib import Path


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
    ("idea", "research-idea-orchestrator", "multi-path-idea-generator", "orchestrated", "context_and_opportunity_map_ready", "frozen_context_and_opportunity_artifacts", "versioned_candidate_set", "generation_blocked"),
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
        "schema_version: 2",
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

    (PLUGIN / "workflow-registry.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote registry for {len(skill_files)} skills and {len(REVIEWERS)} reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
