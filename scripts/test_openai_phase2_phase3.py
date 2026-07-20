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

WORKFLOWS = {"idea", "proposal", "article", "perspective", "research_polisher"}
EXPECTED_ENTRY_MODES = {
    "idea": {"standard", "resume_candidates", "portfolio_only"},
    "proposal": {"standard", "existing_draft", "draft_and_external_review", "package_only"},
    "article": {"standard", "fast_track_draft", "fast_track_draft_and_evaluation", "blueprint_only", "section_specific", "submission_only"},
    "perspective": {"lite", "standard", "full"},
    "research_polisher": {"standard"},
}
CANONICAL_STATES = {
    "pending_review",
    "independent_review_pending",
    "blocked",
    "stopped",
    "human_signoff_required",
    "human_strategy_selection_required",
}
FINAL_SKILLS = {
    "idea": "idea-portfolio-assembler",
    "proposal": "proposal-package-assembler",
    "article": "article-submission-compositor",
    "perspective": "perspective-final-compositor",
    "research_polisher": "research-polisher-plan-assembler",
}
ORCHESTRATORS = {
    "idea": "research-idea-orchestrator",
    "proposal": "proposal-orchestrator",
    "article": "article-orchestrator",
    "perspective": "perspective-orchestrator",
    "research_polisher": "research-polisher-orchestrator",
}
IDEA_NON_BYPASS_GATES = {
    "current_dossier_editorial_readiness_complete",
    "latest_version_independently_evaluated",
    "biomedical_journal_review_complete_or_not_applicable",
    "dissent_and_fatal_findings_indexed",
    "idea-portfolio-assembler",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_idea_mode_contract(registry: dict, skill_text: str) -> None:
    machine = registry["workflow_state_machines"]["idea"]
    match = re.search(
        r"<!-- idea-entry-mode-contract:start -->\s*```yaml\s*(.*?)\s*```\s*<!-- idea-entry-mode-contract:end -->",
        skill_text,
        re.S,
    )
    require(match is not None, "idea orchestrator lacks its machine-readable entry-mode contract")
    contract = yaml.safe_load(match.group(1))
    require(isinstance(contract, dict), "idea orchestrator entry-mode contract is not a mapping")
    require(contract.get("entry_modes") == machine.get("entry_modes"), "idea registry/SKILL entry modes differ")
    require(contract.get("entry_gates") == machine.get("entry_gates"), "idea registry/SKILL entry gates differ")
    require(
        set(contract.get("non_bypass_gates", [])) == IDEA_NON_BYPASS_GATES,
        "idea SKILL does not preserve evaluation, finding-index, and assembly gates",
    )
    require(
        machine.get("final_package_skill") in contract["non_bypass_gates"],
        "idea SKILL assembly gate differs from the registry final package skill",
    )
    require(
        "latest_version_independently_evaluated" in machine.get("before_panel", []),
        "idea panel can run without current-version independent evaluation",
    )
    require(
        {"latest_version_independently_evaluated", "dissent_and_fatal_findings_indexed"}
        <= set(machine.get("before_packaging", [])),
        "idea packaging gates omit evaluation or finding indexing",
    )
    profile_gates = machine.get("before_packaging_by_direction_profile", {})
    require(
        contract.get("entry_gates_by_route") == profile_gates,
        "idea SKILL route-specific entry gates differ from registry packaging gates",
    )
    require(
        contract.get("non_bypass_gates_by_route") == profile_gates,
        "idea SKILL route-specific non-bypass gates differ from registry packaging gates",
    )
    require(
        "adversarial_reports_complete_when_proposal_handoff_candidate"
        in profile_gates.get("focused_optimization", []),
        "focused Proposal handoff can bypass the adversarial panel",
    )
    require(
        {
            "evidence_and_opportunity_remap_complete",
            "fresh_evaluation_complete_for_each_current_dossier",
        }
        <= set(profile_gates.get("bounded_exploration", [])),
        "bounded exploration packaging can bypass remap or terminal evaluation",
    )
    require(
        not any("adversarial" in gate for gate in profile_gates.get("bounded_exploration", [])),
        "bounded exploration incorrectly requires a preselection panel",
    )
    panel = next(entry for entry in registry["skills"] if entry["name"] == "idea-adversarial-review-panel")
    require(panel.get("requires_independent_subagent") is True, "idea panel roles are not independently delegated")
    panel_edges = [
        edge
        for edge in registry["workflow_edges"]
        if edge.get("workflow") == "idea" and edge.get("destination") == "idea-adversarial-review-panel"
    ]
    require(
        len(panel_edges) == 1 and panel_edges[0].get("dispatch_mode") == "delegated",
        "idea orchestrator-to-panel edge is not delegated",
    )


def idea_mode_contract_mutation_tests(registry: dict, skill_text: str) -> None:
    mutations = {
        "missing mode": skill_text.replace("  - portfolio_only\n", "", 1),
        "missing gate": skill_text.replace("    - evidence_map_frozen\n", "", 1),
        "missing bounded route gate": skill_text.replace(
            "    - evidence_and_opportunity_remap_complete\n", "", 1
        ),
    }
    for label, mutated in mutations.items():
        require(mutated != skill_text, f"idea contract mutation fixture was ineffective: {label}")
        try:
            validate_idea_mode_contract(registry, mutated)
        except AssertionError:
            continue
        raise AssertionError(f"idea contract validator accepted mutation: {label}")


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
        orchestrator = read(SKILLS / ORCHESTRATORS[workflow] / "SKILL.md")
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
        "Status: `self_attested_search_snapshot_validated`",
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


def resolve_ready_state(*, changed: bool, current_version: str, evaluated_version: str | None, fatal: bool, reviewer_available: bool, final_state: str = "human_signoff_required") -> str:
    if not reviewer_available:
        return "independent_review_pending"
    if fatal:
        return "blocked"
    if changed and evaluated_version != current_version:
        return "pending_review"
    return final_state


def phase3_tests(registry: dict) -> None:
    policy = registry.get("workflow_state_policy", {})
    machines = registry.get("workflow_state_machines", {})
    require(set(machines) == WORKFLOWS, "registry workflow state-machine set is incomplete")
    policy_states = set(policy.get("active_states", [])) | set(policy.get("pause_states", [])) | set(policy.get("terminal_states", []))
    require(CANONICAL_STATES <= policy_states, f"canonical workflow states missing: {sorted(CANONICAL_STATES - policy_states)}")
    require(policy.get("review_unavailable_state") == "independent_review_pending", "reviewer unavailability state is wrong")
    require(policy.get("fatal_finding_state") == "blocked", "fatal finding state is wrong")
    require(policy.get("final_handoff_state") == "human_signoff_required", "human sign-off state is wrong")
    require(
        registry.get("scenario_eval_contract", {})
        .get("workflow_final_states", {})
        .get("research_polisher")
        == "human_strategy_selection_required",
        "Research Polisher final handoff state is wrong",
    )

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
        ("packaging_pending", "human_strategy_selection_required", "selection_dossier_verified"),
    ):
        require(required in transitions, f"lifecycle transition missing: {required}")

    for workflow, machine in machines.items():
        require(set(machine.get("entry_modes", [])) == EXPECTED_ENTRY_MODES[workflow], f"{workflow} entry modes are incomplete")
        require(set(machine.get("entry_gates", {})) == EXPECTED_ENTRY_MODES[workflow], f"{workflow} entry gates do not cover every mode")
        if machine.get("post_evaluation_panel_required", True):
            require("latest_version_independently_evaluated" in machine.get("before_panel", []), f"{workflow} panel bypasses current-version evaluation")
        else:
            require(
                machine.get("workflow_profile") == "reviewer_matrix_assemble_evaluate"
                and machine.get("strategy_reviewer_roles")
                == ["scientific_significance", "practical_value", "dissemination_editorial"]
                and machine.get("effort_tiers")
                == ["reposition_only", "small_extension", "moderate_extension"],
                f"{workflow} reviewer-matrix profile is incomplete",
            )
        require("latest_version_independently_evaluated" in machine.get("before_packaging", []), f"{workflow} package bypasses current-version evaluation")
        require("dissent_and_fatal_findings_indexed" in machine.get("before_packaging", []), f"{workflow} package drops dissent/fatal findings")
        require(machine.get("final_package_skill") == FINAL_SKILLS[workflow], f"{workflow} final package skill mismatch")

        orchestrator = read(SKILLS / machine["orchestrator"] / "SKILL.md")
        required_states = CANONICAL_STATES - {
            "human_strategy_selection_required"
            if workflow != "research_polisher"
            else "human_signoff_required"
        }
        for state in required_states:
            require(state in orchestrator, f"{workflow} orchestrator lacks canonical state {state}")
        require(
            "one writer" in orchestrator
            and re.search(r"concurrent(?: source)? writes", orchestrator),
            f"{workflow} orchestrator lacks single-writer contract",
        )
        require(
            re.search(
                r"new (?:\w+ )?version|version the result|creates? a (?:\w+ )?version",
                orchestrator,
                re.I,
            )
            and "evaluator" in orchestrator,
            f"{workflow} orchestrator lacks new-version/fresh-evaluator gate",
        )

        final_skill = read(SKILLS / machine["final_package_skill"] / "SKILL.md")
        final_state = machine.get("final_state", "human_signoff_required")
        if workflow == "research_polisher":
            for state in ("independent_review_pending", final_state):
                require(state in final_skill, f"{workflow} final package skill lacks state {state}")
        else:
            for state in ("blocked", "independent_review_pending", final_state):
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
    require(
        resolve_ready_state(
            changed=True,
            current_version="v2",
            evaluated_version="v2",
            fatal=False,
            reviewer_available=True,
            final_state="human_strategy_selection_required",
        )
        == "human_strategy_selection_required",
        "valid Research Polisher evaluation did not reach human selection",
    )

    idea_orchestrator = read(SKILLS / "research-idea-orchestrator" / "SKILL.md")
    validate_idea_mode_contract(registry, idea_orchestrator)
    idea_mode_contract_mutation_tests(registry, idea_orchestrator)


def main() -> int:
    registry = yaml.safe_load(read(REGISTRY))
    require(registry.get("schema_version") == 5, "workflow registry schema must be 5")
    phase2_tests(registry)
    phase3_tests(registry)
    print("Phase 2/3 contract tests passed")
    print(f"workflows: {len(WORKFLOWS)}")
    print("targeted Search smoke: self-attested snapshot validated (non-gating)")
    print("Deep Research inactive smoke: deep_research_handoff_required")
    print("state-machine transition cases: 5/5")
    print("idea registry/SKILL mutation guards: 3/3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
