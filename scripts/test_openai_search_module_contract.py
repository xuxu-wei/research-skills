#!/usr/bin/env python3
"""Check the v0.13.0-preview.1 landscape-search contracts."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
MAPPER = PLUGIN / "skills" / "research-landscape-mapper"
TEST_ROOT = REPO / "tests" / "test-search-module"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    manifest = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
    registry = yaml.safe_load(read(PLUGIN / "workflow-registry.yaml"))
    require(
        manifest["version"] == registry["plugin_version"] == "0.13.0-preview.1",
        "version mismatch",
    )

    mapper_skill = read(MAPPER / "SKILL.md")
    normalized_mapper_skill = " ".join(mapper_skill.split())
    for value in ("evidence_only", "evidence_and_opportunity", "idea_landscape"):
        require(value in mapper_skill, f"mapper missing output profile: {value}")
    require("validate_deep_research_package.py" in mapper_skill, "mapper missing package validator")
    require((MAPPER / "scripts" / "validate_deep_research_package.py").exists(), "package validator is missing")
    require("evidence_search.py" not in mapper_skill, "retired retrieval stub remains referenced")
    require(not (MAPPER / "scripts" / "evidence_search.py").exists(), "retired retrieval stub remains")
    require(
        not (MAPPER / "references" / "design-pattern-strategy-routing.md").exists(),
        "retired A/B routing reference remains",
    )
    for marker in (
        "Artifact Assembly",
        "source records in bounded groups",
        "claim/opportunity records in stable ID order",
        "retry only that incomplete artifact once",
        "do not wait for a separate final message",
    ):
        require(marker in normalized_mapper_skill, f"mapper missing persistence rule: {marker}")

    request_template = read(MAPPER / "templates" / "deep-research-request.md")
    require(len(request_template) <= 4000, "empty Deep Research request template is too long")
    required_headings = (
        "## Research objective and intended use",
        "## Core research question",
        "## Scope and boundaries",
        "## Known background and unresolved issues",
        "## Questions to answer",
        "## Search scope and source requirements",
        "## Analysis and synthesis requirements",
        "## Report structure",
        "## Citation and link requirements",
        "## Completion criteria",
    )
    positions = [request_template.find(heading) for heading in required_headings]
    require(all(position >= 0 for position in positions), "request template missing a required heading")
    require(positions == sorted(positions), "request headings are out of order")
    for residue in (
        "Workflow ID",
        "pending edge",
        "Plugin version",
        "artifact_id",
        "Resume target",
        "deep_research_handoff_required",
        "SHA256",
        "Digest",
    ):
        require(residue.lower() not in request_template.lower(), f"request template leaks {residue}")
    for marker in (
        "one to five",
        "atomic claim",
        "[R001](https://doi.org/{verified-doi-1})",
        "Do not move all references to the sentence end",
    ):
        require(marker in request_template, f"request template missing citation rule: {marker}")

    guide_template = read(MAPPER / "templates" / "deep-research-follow-up-guide.md")
    require("deep-research-request-vNNN.md" in guide_template, "guide missing request name")
    require("deep-research-report-vNNN.md" in guide_template, "guide missing report name")
    require(len(guide_template) <= 5000, "Deep Research follow-up guide is too long")

    workflow_expectations = {
        "research-idea-orchestrator": "output_profile: idea_landscape",
        "proposal-orchestrator": "output_profile: evidence_and_opportunity",
        "perspective-orchestrator": "output_profile: evidence_only",
        "article-orchestrator": "output_profile:",
        "research-polisher-orchestrator": "output_profile: evidence_and_opportunity",
    }
    for skill, marker in workflow_expectations.items():
        text = read(PLUGIN / "skills" / skill / "SKILL.md")
        require(marker in text, f"{skill} missing mapper output profile")
    require(
        "evidence_only" in read(PLUGIN / "skills" / "article-orchestrator" / "SKILL.md"),
        "article orchestrator missing evidence-only profile",
    )

    perspective_orchestrator = read(PLUGIN / "skills" / "perspective-orchestrator" / "SKILL.md")
    perspective_curator = read(PLUGIN / "skills" / "perspective-claim-evidence-curator" / "SKILL.md")
    input_builder = read(PLUGIN / "skills" / "perspective-input-builder" / "SKILL.md")
    delegate_briefs = read(
        PLUGIN / "skills" / "perspective-orchestrator" / "references" / "delegate-brief-templates.md"
    )
    for text, label in (
        (perspective_orchestrator, "perspective orchestrator"),
        (perspective_curator, "perspective curator"),
        (input_builder, "perspective input builder"),
        (delegate_briefs, "perspective delegate briefs"),
    ):
        require("hash" in text.lower() or "sha" in text.lower(), f"{label} missing no-hash rule")
    require("Batch 1" in perspective_curator and "Batch 4" in perspective_curator, "curator batching contract")
    require("Binding groups in Claim-ID order" in perspective_curator, "curator missing within-file staging")
    require("complete one file at a time" in perspective_curator, "curator missing one-file persistence")
    require("staged write order" in delegate_briefs, "missing staged curator delegate brief")
    require("no meaningful file progress" in perspective_orchestrator, "missing stale delegate recovery")
    require("without waiting for a separate" in perspective_orchestrator, "missing artifact-authoritative completion")
    idea_orchestrator = " ".join(
        read(PLUGIN / "skills" / "research-idea-orchestrator" / "SKILL.md").split()
    )
    require("retry only that incomplete artifact once" in idea_orchestrator, "idea mapper recovery missing")

    policy = registry.get("evidence_retrieval_policy", {})
    require(set(policy.get("output_profiles", {})) == {"evidence_only", "evidence_and_opportunity", "idea_landscape"}, "registry output profiles")
    assembly = policy.get("artifact_assembly", {})
    require(assembly.get("row_dense_artifacts_use_incremental_persistence") is True, "registry incremental persistence")
    require(assembly.get("freeze_only_after_read_only_consistency_check") is True, "registry final consistency check")
    require(
        assembly.get("completion_signal")
        == "passing_artifact_check_without_separate_delegate_final_message",
        "registry completion signal",
    )
    recovery = assembly.get("no_progress_recovery", {})
    require(recovery.get("scope") == "current_incomplete_artifact_or_batch_only", "registry recovery scope")
    require(recovery.get("fresh_retry_limit") == 1, "registry recovery retry limit")
    require(recovery.get("content_hash_required") is False, "registry recovery must not require hashes")
    claim_binding = policy.get("claim_source_binding", {})
    require(claim_binding.get("citation_unit") == "atomic_claim", "registry atomic-claim citation unit")
    require(claim_binding.get("direct_support_minimum") == 1, "registry direct-support minimum")
    require(claim_binding.get("direct_support_maximum") == 5, "registry direct-support maximum")
    require(claim_binding.get("zero_source_claim_cannot_be_supported") is True, "registry zero-source gate")
    require(claim_binding.get("clause_local_citation_binding") is True, "registry clause-local binding")
    continuation = policy.get("deep_research_continuation", {})
    require(continuation.get("request_is_exact_sendable_prompt") is True, "registry direct-send request")
    require(continuation.get("stored_hashes_or_digests") is False, "registry no-hash contract")
    require(continuation.get("request_hard_maximum_characters") == 12000, "registry request hard cap")
    repair = continuation.get("post_return_repair", {})
    require(
        repair.get("route_order")
        == [
            "deterministic_normalization",
            "built_in_search_and_agent_repair",
            "focused_literature_synthesis",
            "second_deep_research",
        ],
        "registry lower-cost repair order",
    )
    require(repair.get("second_deep_research_requires_owner_approval") is True, "second DR owner gate")
    require(repair.get("prepare_second_round_before_approval") is False, "no speculative second DR package")
    require(
        repair.get("citation_mechanics_alone_trigger_second_deep_research") is False,
        "citation mechanics must not trigger second DR",
    )

    citation_contract = read(MAPPER / "references" / "citation-record-contract.md")
    evidence_schema = read(MAPPER / "references" / "evidence-map-schema.md")
    deep_rules = " ".join(
        read(MAPPER / "references" / "deep-research-prompt-rules.md").split()
    )
    for marker in ("one to five", "direct_support", "direct_contradiction", "R001-R003"):
        require(marker in citation_contract, f"citation contract missing: {marker}")
    for marker in ("repairability_assessment", "built_in_search_and_agent_repair", "owner_approval_required"):
        require(marker in evidence_schema, f"evidence schema missing: {marker}")
    for marker in ("Post-return repair ladder", "owner approval", "Do not prepare a second-round package"):
        require(marker in deep_rules, f"Deep Research repair rule missing: {marker}")

    run_index = yaml.safe_load(read(TEST_ROOT / "test-run-index.yaml"))
    cases = {case["case_id"]: case for case in run_index["cases"]}
    require(len(cases) == 4, "search-module matrix must declare four cases")
    allowed_deep_status = {
        "prepared_retry",
        "running",
        "awaiting_deep_research_report",
        "resuming_after_deep_research",
        "completed",
        "stopped",
    }
    for case_id in ("perspective-deep-research", "idea-landscape-deep-research"):
        case = cases[case_id]
        require(case["status"] in allowed_deep_status, f"unexpected status: {case_id}")
        guide = TEST_ROOT / case_id / "follow-up-guide.md"
        require(guide.exists(), f"missing direct test guide: {case_id}")
        guide_text = read(guide)
        require(len(guide_text) <= 4000, f"test guide too long: {case_id}")
        for value in (case["workflow"], case["retrieval_mode"], case["input_path"], case["output_path"], case["session_name"]):
            require(str(value) in guide_text, f"test guide missing {value}: {case_id}")
        require("0.13.0" in guide_text and "+codex.local-*" in guide_text, f"test guide missing local version check: {case_id}")
        for forbidden in ("SHA", "content hash", "checksum", "digest"):
            require(forbidden in guide_text, f"test guide missing explicit no-{forbidden} rule: {case_id}")

    for case_id in ("perspective-web-search", "idea-landscape-web-search"):
        require(cases[case_id]["status"] == "planned_after_deep_research_cases_pass", f"{case_id} should remain planned")

    print("OpenAI search-module contract tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
