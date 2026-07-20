#!/usr/bin/env python3
"""Static checks for the Idea biomedical journal-review route."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "research-skills-openai"
GENERATOR = ROOT / "scripts" / "generate_openai_workflow_registry.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_generator():
    spec = importlib.util.spec_from_file_location("openai_registry_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load registry generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    errors: list[str] = []
    module = load_generator()

    edges = [
        edge
        for edge in module.WORKFLOW_EDGES
        if edge[0] == "idea" and edge[2] == "medical-journal-review"
    ]
    require(len(edges) == 1, "Idea workflow must have exactly one medical-journal-review edge", errors)
    if edges:
        edge = edges[0]
        require(edge[3] == "delegated", "Idea medical review must be delegated", errors)
        require("final_current_idea_evaluation_valid" in edge[4], "medical review must follow final valid evaluation", errors)
        require("unscored_unranked_candidate_journal_match_brief" in edge[5], "edge must require an unscored, unranked candidate brief", errors)
        require("without_evaluator_material" in edge[5], "medical-review input contract must exclude evaluator material", errors)

    transitions = module.WORKFLOW_STATE_POLICY["lifecycle_transitions"]
    transition_keys = {
        (item["from"], item["to"], item["trigger"])
        for item in transitions
    }
    require(
        ("pending_review", "specialist_review_pending", "biomedical_idea_journal_review_dispatched") in transition_keys,
        "Idea medical review must reuse specialist_review_pending",
        errors,
    )
    require(
        ("specialist_review_pending", "pending_review", "biomedical_idea_journal_review_returned") in transition_keys,
        "Idea medical review must return through the existing review state",
        errors,
    )

    idea_machine = module.WORKFLOW_STATE_MACHINES["idea"]
    contract = idea_machine.get("biomedical_journal_review_contract", {})
    require(contract.get("review_skill") == "medical-journal-review", "journal contract reviewer is wrong", errors)
    require(contract.get("reviewer_isolation_mode") == "fresh_subagent", "journal reviewer is not fresh", errors)
    require(
        contract.get("candidate_brief_schema_version")
        == "research-idea-journal-candidate-brief.v1",
        "journal candidate schema differs from evaluator contract",
        errors,
    )
    require(
        contract.get("candidate_brief_matching_source_skill") == "idea-evaluator",
        "journal matching is not attributed to idea-evaluator",
        errors,
    )
    require(
        contract.get("candidate_brief_materialized_by_skill") == "research-idea-orchestrator",
        "candidate-brief materializer is not explicit",
        errors,
    )
    require(contract.get("candidate_brief_scoring_present") is False, "candidate brief may contain scoring", errors)
    require(contract.get("candidate_brief_evaluator_material_included") is False, "candidate brief may contain evaluator material", errors)
    require(contract.get("content_digest_required") is False, "Idea journal route must use logical refs without digests", errors)
    require(
        contract.get("medical_review_route") == "idea_journal_match_editorial_review",
        "Idea medical review route is ambiguous",
        errors,
    )
    require(
        "publication_probability_assessment" in contract
        and contract["publication_probability_assessment"] is None,
        "Idea journal route must keep publication probability null",
        errors,
    )
    require(
        "biomedical_journal_review_complete_or_not_applicable" in idea_machine.get("before_packaging", []),
        "Idea packaging can bypass applicable journal review",
        errors,
    )

    package = module.PACKAGE_INPUT_CONTRACTS["idea"]
    roles = {item["artifact_role"] for item in package["required_inputs"]}
    require("candidate_journal_match_brief" in roles, "package omits candidate journal match", errors)
    require("medical_journal_review_report" in roles, "package omits medical journal review", errors)

    orchestrator_outputs = module.SCENARIO_EVAL_CONTRACT["runtime_artifact_role_contract"][
        "actor_output_roles_by_skill"
    ]["research-idea-orchestrator"]
    require(
        "candidate_journal_match_brief" in orchestrator_outputs,
        "candidate journal match is not registered as an orchestrator output role",
        errors,
    )

    completeness = module.ARTIFACT_COMPLETENESS_POLICY["idea_biomedical_journal_review_contract"]
    require(
        completeness.get("candidate_brief_schema_version")
        == "research-idea-journal-candidate-brief.v1",
        "completeness policy uses another candidate schema",
        errors,
    )
    require(
        completeness.get("review_route") == "idea_journal_match_editorial_review",
        "completeness policy uses another medical-review route",
        errors,
    )
    require(
        completeness.get("reviewer_reads_exactly")
        == ["current_complete_idea_dossier", "candidate_journal_match_brief"],
        "medical reviewer read set is not exact",
        errors,
    )
    require(
        "idea_evaluation_report" in completeness.get("reviewer_forbidden_inputs", []),
        "medical reviewer is not forbidden from evaluator report",
        errors,
    )

    orchestrator = read(PLUGIN / "skills/research-idea-orchestrator/SKILL.md")
    artifact_contracts = read(
        PLUGIN
        / "skills/research-idea-orchestrator/references/journal-review-and-portfolio-artifacts.md"
    )
    evaluator_matching = read(
        PLUGIN / "skills/idea-evaluator/references/journal-matching-contract.md"
    )
    medical_route = read(
        PLUGIN
        / "skills/medical-journal-review/references/idea-journal-match-editorial-route.md"
    )
    medical_template = read(
        PLUGIN / "skills/medical-journal-review/templates/idea-journal-match-review.md"
    )
    normalized_evaluator_matching = " ".join(evaluator_matching.split())
    normalized_medical_route = " ".join(medical_route.split())
    delegate_briefs = read(PLUGIN / "skills/research-idea-orchestrator/references/delegate-brief-templates.md")
    if10 = read(PLUGIN / "skills/research-idea-orchestrator/references/if10-evaluation-gate.md")
    portfolio = read(PLUGIN / "skills/idea-portfolio-assembler/templates/research-idea-portfolio.md")
    attribution = read(PLUGIN / "skills/research-idea-orchestrator/references/editorial-readiness-and-preservation.md")

    for token in ("unscored", "unranked", "medical-journal-review", "specialist_review_pending"):
        require(token in orchestrator, f"orchestrator omits {token}", errors)
    for token in (
        "schema_version: research-idea-journal-candidate-brief.v1",
        "source_dossier_ref:",
        "evaluation_fields_included: false",
        "scoring_present: false",
        "ranking_present: false",
        "publication_probability_present: false",
        "candidates:",
    ):
        require(token in artifact_contracts, f"candidate brief contract omits {token}", errors)
        require(token in evaluator_matching, f"evaluator candidate contract omits {token}", errors)
    for token in (
        "source_status: usable | discarded_disallowed_content",
        "discarded_disallowed_content",
        "does not invalidate the already frozen evaluation",
        "if it was used, discard the evaluator instance",
    ):
        require(token in normalized_evaluator_matching, f"redirect-contamination rule omits {token}", errors)
    for token in (
        "discarded_disallowed_content",
        "do not use or cite it",
        "Discard the reviewer instance only if",
    ):
        require(token in normalized_medical_route, f"medical redirect rule omits {token}", errors)
    journal_section = artifact_contracts.split("## Lineage and portfolio navigation", 1)[0]
    for legacy_token in (
        "schema_version: research-idea.v3",
        "candidate_outlets:",
        "review_route: design_and_editorial_journal_fit",
        "reviewed_dossier_ref:",
        "journal_fit:",
    ):
        require(legacy_token not in journal_section, f"legacy journal schema remains: {legacy_token}", errors)
    require("Allowed project reads: exactly the dossier and candidate brief above" in delegate_briefs, "delegate read isolation is missing", errors)
    require("Do not open the idea-evaluator report" in delegate_briefs, "delegate does not forbid evaluator report", errors)
    for token in (
        "idea_journal_match_editorial_review",
        "reviewed_idea_ref:",
        "candidate_brief_ref:",
        "publication_probability_assessment: null",
    ):
        require(token in delegate_briefs, f"delegate brief omits dedicated Idea field {token}", errors)
        require(token in medical_route, f"medical route omits dedicated Idea field {token}", errors)
        require(token in medical_template, f"medical template omits dedicated Idea field {token}", errors)
    require(
        "unless the medical-journal-review contract" not in delegate_briefs,
        "Idea journal route conditionally enables publication probability",
        errors,
    )
    require("recommend a specific journal" not in if10, "IF>10 gate still contains the specific-journal prohibition", errors)
    require("Candidate journal-match link" in portfolio, "portfolio omits journal-match link", errors)
    require("Medical journal review link" in portfolio, "portfolio omits medical-review link", errors)

    allowed_attributions = [
        "source_input_or_context_handoff_failure",
        "assessor_coverage_failure",
        "assessor_variance",
        "brief_normalization_failure",
        "writer_execution_failure",
        "writer_regression",
        "context_attention_failure",
        "workflow_contract_conflict",
        "fresh_reassessment_closed",
    ]
    for token in allowed_attributions:
        require(token in attribution, f"repair attribution omits {token}", errors)
    attribution_contract = module.ARTIFACT_COMPLETENESS_POLICY[
        "idea_editorial_readiness_contract"
    ]["repair_outcome_attribution_contract"]
    require(
        attribution_contract.get("successful_production_repair_may_omit") is True,
        "successful production repair is forced to persist attribution",
        errors,
    )
    require(
        attribution_contract.get("context_attention_diagnostic_opt_in") is True,
        "same-writer context-attention experiment is not opt-in",
        errors,
    )
    for token in ("finding_level", "scientific_role", "normalized_locator", "failure_mode"):
        require(token in attribution, f"readable failure fingerprint omits {token}", errors)
    require("same writer instance" in attribution, "context-attention attribution lacks same-writer control", errors)
    require("deterministic bounded section view" in attribution, "context-attention attribution lacks bounded-view success control", errors)
    require("successful production repair may leave" in attribution, "successful repair cannot omit attribution", errors)
    require("opt-in diagnostic run" in attribution, "context-attention experiment is mandatory", errors)
    require("compute or store a hash" in attribution, "failure fingerprint does not forbid hashes", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: Idea biomedical journal-review and repair-attribution contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
