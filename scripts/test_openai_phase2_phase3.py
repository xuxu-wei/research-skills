#!/usr/bin/env python3
"""Deterministic contract tests for Roadmap Phase 2 and Phase 3."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
REGISTRY = PLUGIN / "workflow-registry.yaml"
REPORTS = PLUGIN / "reports"

WORKFLOWS = {"idea", "proposal", "article", "perspective"}
EXPECTED_ENTRY_MODES = {
    "idea": {"standard", "resume_candidates", "portfolio_only"},
    "proposal": {"standard", "existing_draft", "draft_and_external_review", "package_only"},
    "article": {"standard", "fast_track_draft", "fast_track_draft_and_evaluation", "blueprint_only", "section_specific", "submission_only"},
    "perspective": {"lite", "standard", "full"},
}
CANONICAL_STATES = {
    "pending_review",
    "independent_review_pending",
    "blocked",
    "stopped",
    "human_signoff_required",
}
FINAL_SKILLS = {
    "idea": "idea-portfolio-assembler",
    "proposal": "proposal-package-assembler",
    "article": "article-submission-compositor",
    "perspective": "perspective-final-compositor",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_handoff_report() -> dict:
    text = read(REPORTS / "phase2-deep-research-handoff-smoke.md")
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    require(match is not None, "Deep Research smoke report lacks YAML continuation package")
    return yaml.safe_load(match.group(1))


def phase2_tests(registry: dict) -> None:
    mapper = read(SKILLS / "research-opportunity-mapper" / "SKILL.md")
    narrow = read(SKILLS / "academic-deep-search" / "SKILL.md")
    require("single owner of broad retrieval policy" in mapper, "mapper is not the declared broad-retrieval owner")
    require("Built-in Search" in mapper and "open them" in mapper, "mapper lacks built-in Search open/verify route")
    require("Deep Research" in mapper and "deep_research_handoff_required" in mapper, "mapper lacks Deep Research pause route")
    require("Local scripts are never the default" in mapper, "mapper does not demote local scripts")
    require("2-5" in narrow and "route to `research-opportunity-mapper`" in narrow, "academic deep search exceeds narrow 2-5-paper scope")
    require("Do not broaden this skill into Deep Research" in narrow, "academic deep search still owns broad synthesis")

    for workflow in WORKFLOWS:
        orchestrator = read(SKILLS / f"{workflow if workflow != 'idea' else 'research-idea'}-orchestrator" / "SKILL.md")
        for forbidden in ("built-in Search", "Deep Research", "evidence_search.py", "local retrieval script"):
            require(forbidden not in orchestrator, f"{workflow} orchestrator owns retrieval policy residue: {forbidden}")

    installed = {entry["name"] for entry in registry["skills"]}
    for entry in registry["skills"]:
        for related in entry.get("related_skills", []):
            require(related in installed, f"dangling related skill: {entry['name']} -> {related}")
            require(related not in {"pubmed", "arxiv", "llm-wiki"}, f"deleted/external retrieval dependency remains: {related}")

    search_report = read(REPORTS / "phase2-targeted-search-smoke.md")
    for expected in (
        "Capability: ChatGPT/Codex built-in Search",
        "Local retrieval scripts used: no",
        "equator-network.org/reporting-guidelines/consort",
        "consort-spirit.org/published-statements",
        "Status: `targeted_search_verified`",
    ):
        require(expected in search_report, f"targeted Search smoke evidence missing: {expected}")

    handoff = load_handoff_report()
    required_fields = {
        "workflow_id",
        "round_id",
        "handoff_status",
        "research_question",
        "downstream_decision",
        "exploration_mode",
        "scope",
        "date_window",
        "languages",
        "geographies",
        "required_source_classes",
        "preferred_domains",
        "excluded_sources",
        "queries",
        "claims_to_verify",
        "evidence_table_fields",
        "citation_requirements",
        "current_evidence_summary",
        "included_artifact_ids",
        "known_limitations",
        "return_contract",
    }
    require(required_fields <= set(handoff), f"Deep Research continuation fields missing: {sorted(required_fields - set(handoff))}")
    require(handoff["handoff_status"] == "deep_research_handoff_required", "inactive Deep Research did not pause")


def resolve_ready_state(*, changed: bool, current_version: str, evaluated_version: str | None, fatal: bool, reviewer_available: bool) -> str:
    if not reviewer_available:
        return "independent_review_pending"
    if fatal:
        return "blocked"
    if changed and evaluated_version != current_version:
        return "pending_review"
    return "human_signoff_required"


def phase3_tests(registry: dict) -> None:
    policy = registry.get("workflow_state_policy", {})
    machines = registry.get("workflow_state_machines", {})
    require(set(machines) == WORKFLOWS, "registry must define exactly four workflow state machines")
    policy_states = set(policy.get("active_states", [])) | set(policy.get("pause_states", [])) | set(policy.get("terminal_states", []))
    require(CANONICAL_STATES <= policy_states, f"canonical workflow states missing: {sorted(CANONICAL_STATES - policy_states)}")
    require(policy.get("review_unavailable_state") == "independent_review_pending", "reviewer unavailability state is wrong")
    require(policy.get("fatal_finding_state") == "blocked", "fatal finding state is wrong")
    require(policy.get("final_handoff_state") == "human_signoff_required", "human sign-off state is wrong")

    version_gate = policy.get("version_gate", {})
    for field in ("changed_artifact_requires_new_version", "evaluator_instance_must_be_fresh", "evaluated_version_must_equal_current_version"):
        require(version_gate.get(field) is True, f"version gate disabled: {field}")
    require(version_gate.get("prior_scores_visible_to_fresh_evaluator") is False, "fresh evaluator can see prior scores")

    finding_gate = policy.get("finding_gate", {})
    for field in ("fatal_or_blocking_finding_prevents_accept", "fatal_or_blocking_finding_prevents_promoted", "fatal_or_blocking_finding_prevents_human_signoff", "panel_dissent_must_remain_visible"):
        require(finding_gate.get(field) is True, f"finding gate disabled: {field}")

    concurrency = policy.get("concurrency_policy", {})
    require(concurrency.get("phase_level_delegation_allowed") is True, "phase delegation is not allowed")
    require(concurrency.get("single_writer_per_source_artifact") is True, "single-writer rule missing")
    require(concurrency.get("concurrent_writes_to_same_source_artifact") is False, "concurrent source writes are allowed")

    transitions = {(item["from"], item["to"], item["trigger"]) for item in policy.get("lifecycle_transitions", [])}
    for required in (
        ("revision_required", "artifact_frozen", "new_version_created"),
        ("*", "independent_review_pending", "required_reviewer_unavailable"),
        ("*", "blocked", "fatal_or_blocking_finding"),
        ("packaging_pending", "human_signoff_required", "package_verified"),
    ):
        require(required in transitions, f"lifecycle transition missing: {required}")

    for workflow, machine in machines.items():
        require(set(machine.get("entry_modes", [])) == EXPECTED_ENTRY_MODES[workflow], f"{workflow} entry modes are incomplete")
        require(set(machine.get("entry_gates", {})) == EXPECTED_ENTRY_MODES[workflow], f"{workflow} entry gates do not cover every mode")
        require("latest_version_independently_evaluated" in machine.get("before_panel", []), f"{workflow} panel bypasses current-version evaluation")
        require("latest_version_independently_evaluated" in machine.get("before_packaging", []), f"{workflow} package bypasses current-version evaluation")
        require("dissent_and_fatal_findings_indexed" in machine.get("before_packaging", []), f"{workflow} package drops dissent/fatal findings")
        require(machine.get("final_package_skill") == FINAL_SKILLS[workflow], f"{workflow} final package skill mismatch")

        orchestrator = read(SKILLS / machine["orchestrator"] / "SKILL.md")
        for state in CANONICAL_STATES:
            require(state in orchestrator, f"{workflow} orchestrator lacks canonical state {state}")
        require("one writer" in orchestrator and "concurrent writes" in orchestrator, f"{workflow} orchestrator lacks single-writer contract")
        require("new version" in orchestrator and "evaluator" in orchestrator, f"{workflow} orchestrator lacks new-version/fresh-evaluator gate")

        final_skill = read(SKILLS / machine["final_package_skill"] / "SKILL.md")
        for state in ("blocked", "independent_review_pending", "human_signoff_required"):
            require(state in final_skill, f"{workflow} final package skill lacks state {state}")
        require("fatal" in final_skill.lower() and "dissent" in final_skill.lower(), f"{workflow} final package does not preserve fatal findings/dissent")

    article_submission = machines["article"]["entry_gates"]["submission_only"]
    require("latest_version_independently_evaluated" in article_submission, "article submission-only bypasses evaluation")
    require(set(machines["article"]["non_ready_modes"]) == {"blueprint_only", "section_specific"}, "article non-ready modes are wrong")

    perspective_compositor = read(SKILLS / "perspective-final-compositor" / "SKILL.md")
    require("text-identical" in perspective_compositor, "Perspective compositor may change final prose")
    require("Do not edit" in perspective_compositor, "Perspective compositor source-edit prohibition missing")

    require(resolve_ready_state(changed=True, current_version="v2", evaluated_version="v1", fatal=False, reviewer_available=True) == "pending_review", "changed artifact reached ready without fresh evaluation")
    require(resolve_ready_state(changed=False, current_version="v2", evaluated_version="v2", fatal=True, reviewer_available=True) == "blocked", "fatal finding did not block")
    require(resolve_ready_state(changed=False, current_version="v2", evaluated_version="v2", fatal=False, reviewer_available=False) == "independent_review_pending", "reviewer unavailability did not pause")
    require(resolve_ready_state(changed=True, current_version="v2", evaluated_version="v2", fatal=False, reviewer_available=True) == "human_signoff_required", "valid current-version evaluation did not reach human sign-off")


def main() -> int:
    registry = yaml.safe_load(read(REGISTRY))
    require(registry.get("schema_version") == 3, "workflow registry schema must be 3")
    phase2_tests(registry)
    phase3_tests(registry)
    print("Phase 2/3 contract tests passed")
    print("workflows: 4")
    print("targeted Search smoke: verified")
    print("Deep Research inactive smoke: deep_research_handoff_required")
    print("state-machine transition cases: 4/4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
