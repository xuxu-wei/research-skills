#!/usr/bin/env python3
"""Validate the current cross-workflow reader-readiness architecture.

This suite is intentionally independent of historical Roadmap phase fixtures.
It checks only source contracts introduced or relied upon by the current change.
"""

from __future__ import annotations

import json
import re
import tempfile
from copy import deepcopy
from pathlib import Path

import yaml

from test_openai_phase4_scenarios import (
    ScenarioEngine,
    ScenarioViolation,
    package_requirement_condition_met,
    validate_proposal_background_authority_bundle,
)


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def ordered(text: str, *markers: str) -> bool:
    cursor = -1
    for marker in markers:
        cursor = text.find(marker, cursor + 1)
        if cursor < 0:
            return False
    return True


def logical_ref(artifact_id: str) -> dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "version": "v001",
        "path": f"artifacts/{artifact_id}-v001.yaml",
    }


def functional_path_outline() -> dict[str, object]:
    return {
        "primary_mode": "systematic",
        "organizing_axis": "causal chain",
        "one_sentence_argument_logic": "Move from the field gap to the study need.",
        "opening": {
            "macro_context": "The field depends on reliable measurement.",
            "high_value_real_or_scientific_problem": "Current measurements are unstable.",
            "breadth_or_importance": "The instability affects the target population.",
            "project_core_bottleneck": "The causal source of instability is unresolved.",
        },
        "current_status_units": [
            {
                "unit_id": "status-01",
                "heading": "Measurement instability",
                "entry_claim": "Existing measurements vary across settings.",
                "evidence_scope": ["cross-setting validation studies"],
                "gap_or_constraint": "The causal source of variation is unknown.",
                "project_landing": "Research aim 1 isolates that source.",
                "exit_handoff": "This motivates the planned causal comparison.",
            }
        ],
        "mappings": {
            "research_content": ["aim-1"],
            "research_route": ["measure", "compare", "validate"],
            "key_technical_or_scientific_problems": ["source-of-variation"],
        },
        "synthesis": {
            "project_summary": "The project resolves the measurement gap.",
            "route_or_method": "It compares settings and validates the mechanism.",
            "innovation_position": "It links variation to a testable mechanism.",
            "significance": "The result supports reliable inference.",
            "transition_policy": "Proceed from the established gap to the design rationale.",
        },
        "evidence_requirements": ["validation evidence"],
    }


def proposal_authority_bundle(mode: str) -> list[dict[str, object]]:
    selection_ref = logical_ref("background-selection")
    plan = {
        "artifact_role": "proposal_content_plan",
        "schema": "proposal-content-plan.v2",
        "artifact_id": "content-plan",
        "version_id": "v001",
        "path": "artifacts/content-plan-v001.yaml",
        "source_skill": "proposal-drafter",
        "created_by_instance_id": "proposal-planner-001",
        "frozen": True,
        "based_on": [],
        "background_argumentation": {
            "selection_source": "user" if mode != "bypass" else "user_explicit",
            "selection_mode": mode,
            "user_authorization_text": "Use this background argumentation path.",
            "selected_path_ref": selection_ref if mode != "bypass" else logical_ref("proposal-context"),
        },
    }
    if mode == "option_selection":
        selected_option = functional_path_outline()
        selected_option["option_id"] = "bg-path-01"
        second_option = functional_path_outline()
        second_option["option_id"] = "bg-path-02"
        second_option["primary_mode"] = "progressive"
        second_option["organizing_axis"] = "inferential sequence"
        second_option["one_sentence_argument_logic"] = "Narrow from measurement variation to the causal comparison."
        return [
            {
                "artifact_role": "proposal_background_path_options",
                "schema": "proposal-background-path-options.v1",
                "artifact_id": "background-options",
                "version_id": "v001",
                "path": "artifacts/background-options-v001.yaml",
                "source_skill": "proposal-drafter",
                "created_by_instance_id": "candidate-planner-001",
                "frozen": True,
                "based_on": [],
                "option_count": 2,
                "options": [selected_option, second_option],
            },
            {
                "artifact_role": "proposal_background_path_selection",
                "schema": "proposal-background-path-selection.v1",
                "artifact_id": "background-selection",
                "version_id": "v001",
                "path": "artifacts/background-selection-v001.yaml",
                "source_skill": "proposal-orchestrator",
                "created_by_instance_id": "proposal-orchestrator-001",
                "frozen": True,
                "based_on": ["background-options@v001"],
                "selection_source": "user",
                "selection_mode": mode,
                "user_authorization_text": "Use this background argumentation path.",
                "selected_option_id": "bg-path-01",
                "accepted_sole_path": None,
                "options_ref": logical_ref("background-options"),
            },
            plan,
        ]
    if mode == "sole_path_acceptance":
        return [
            {
                "artifact_role": "proposal_background_path_selection",
                "schema": "proposal-background-path-selection.v1",
                "artifact_id": "background-selection",
                "version_id": "v001",
                "path": "artifacts/background-selection-v001.yaml",
                "source_skill": "proposal-orchestrator",
                "created_by_instance_id": "proposal-orchestrator-001",
                "frozen": True,
                "based_on": [],
                "selection_source": "user",
                "selection_mode": mode,
                "user_authorization_text": "Use this background argumentation path.",
                "selected_option_id": None,
                "accepted_sole_path": functional_path_outline(),
                "options_ref": None,
            },
            plan,
        ]
    if mode == "bypass":
        return [plan]
    raise AssertionError(f"unsupported test mode: {mode}")


def expect_authority_failure(
    artifacts: list[dict[str, object]],
    mode: str,
    label: str,
) -> None:
    try:
        validate_proposal_background_authority_bundle(
            artifacts,
            authority_mode=mode,
            new_full_proposal=True,
        )
    except ScenarioViolation:
        return
    raise AssertionError(f"malformed proposal authority accepted: {label}")


def run_entry_consumer(
    registry: dict[str, object],
    artifacts: list[dict[str, object]],
    mode: str,
) -> None:
    entry_roles = {
        "proposal_background_path_options",
        "proposal_background_path_selection",
        "proposal_content_plan",
    }
    if mode in {"option_selection", "sole_path_acceptance"}:
        entry_roles.remove("proposal_content_plan")
    authority = [
        deepcopy(artifact)
        for artifact in artifacts
        if artifact.get("artifact_role") in entry_roles
    ]
    for artifact in authority:
        artifact.setdefault("content_digest", "sha256:test")
    fixture = {
        "workflow": "proposal",
        "workflow_id": "proposal-authority-consumer-test",
        "entry_mode": "standard",
        "proposal_background_authority_mode": mode,
        "entry_gate_receipts": {
            "background_path_authority_frozen": {
                "artifact_ids": [artifact["artifact_id"] for artifact in authority],
            }
        },
    }
    with tempfile.TemporaryDirectory(prefix="proposal-entry-consumer-") as raw:
        engine = ScenarioEngine(fixture, deepcopy(registry), {}, Path(raw))
        engine.artifacts = {str(artifact["artifact_id"]): artifact for artifact in authority}
        engine.current_primary = {
            "artifact_id": "proposal-current",
            "version_id": "v001",
        }
        engine.process_entry_gate({"event_id": "entry-authority-test"})


def run_package_consumer(
    registry: dict[str, object],
    artifacts: list[dict[str, object]],
    mode: str,
) -> None:
    isolated_registry = deepcopy(registry)
    isolated_registry["workflow_state_machines"]["proposal"]["post_evaluation_panel_required"] = False
    package_contract = isolated_registry["scenario_eval_contract"]["package_input_contracts"]["proposal"]
    authority_roles = {
        "proposal_background_path_options",
        "proposal_background_path_selection",
        "proposal_content_plan",
        "proposal",
    }
    package_contract["allowed_roles"] = sorted(authority_roles)
    package_contract["required_inputs"] = [
        requirement
        for requirement in package_contract["required_inputs"]
        if requirement["artifact_role"] in authority_roles
    ]

    proposal = {
        "artifact_id": "proposal-current",
        "version_id": "v001",
        "artifact_role": "proposal",
        "path": "artifacts/proposal-current-v001.md",
        "source_skill": "proposal-drafter",
        "created_by_instance_id": "proposal-writer-001",
        "frozen": True,
        "based_on": [],
    }
    inputs = [deepcopy(artifact) for artifact in artifacts] + [proposal]
    fixture = {
        "workflow": "proposal",
        "workflow_id": "proposal-authority-consumer-test",
        "entry_mode": "standard",
        "proposal_background_authority_mode": mode,
        "new_full_proposal": True,
    }
    with tempfile.TemporaryDirectory(prefix="proposal-package-consumer-") as raw:
        engine = ScenarioEngine(fixture, isolated_registry, {}, Path(raw))
        engine.artifacts = {str(artifact["artifact_id"]): artifact for artifact in inputs}
        engine.current_primary = proposal
        engine.latest_evaluated_version = "v001"
        engine.entry_gate_verified = True
        engine.validate_ready_for_package(
            {
                "event_id": "package-authority-test",
                "input_artifact_ids": [artifact["artifact_id"] for artifact in inputs],
                "new_full_proposal": True,
                "preserved_dissent_ids": [],
                "artifact_index_dissent_ids": [],
                "automatic_external_submission": False,
            }
        )


def expect_consumer_failure(
    registry: dict[str, object],
    artifacts: list[dict[str, object]],
    mode: str,
    label: str,
    *,
    entry: bool = False,
) -> None:
    consumer = run_entry_consumer if entry else run_package_consumer
    try:
        consumer(registry, artifacts, mode)
    except ScenarioViolation:
        return
    raise AssertionError(f"malformed proposal authority accepted by {'entry' if entry else 'package'} consumer: {label}")


def main() -> int:
    manifest = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
    registry = yaml.safe_load(read(PLUGIN / "workflow-registry.yaml"))
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    reviewers = [item for item in registry["skills"] if item.get("requires_independent_subagent")]

    require(manifest["version"] == "0.14.0", "manifest version")
    require(registry["plugin_version"] == "0.14.0", "registry version")
    require(registry["schema_version"] == 6, "registry schema")
    require(len(skill_files) == 51, "skill count")
    require(len(reviewers) == 22, "reviewer count")

    perspective_machine = registry["workflow_state_machines"]["perspective"]
    require(
        perspective_machine["before_panel"]
        == ["current_perspective_scientific_evaluation_complete", "no_unresolved_fatal_finding"],
        "Perspective scientific evaluation precedes panel",
    )
    require(
        "final_perspective_evaluation_complete" in perspective_machine["before_packaging"],
        "Perspective final evaluation precedes packaging",
    )
    stage_contract = perspective_machine["evaluation_stage_contract"]
    require(stage_contract["scientific"]["dispatch_before"] == "panel", "Perspective scientific evaluator stage")
    require(
        stage_contract["final"]["dispatch_after"]
        == ["applicable_panel_route_closed", "editorial_readiness_complete", "content_preservation_complete"],
        "Perspective final evaluator stage",
    )
    perspective_edges = [edge for edge in registry["workflow_edges"] if edge["workflow"] == "perspective"]
    panel_edge = next(edge for edge in perspective_edges if edge["destination"] == "perspective-review-panel")
    require("scientific_perspective_evaluation_passed" in panel_edge["trigger"], "Perspective panel trigger")

    shared = registry["cross_workflow_editorial_readiness_policy"]
    require(shared["workflows"] == ["idea", "proposal", "perspective", "article"], "workflow scope")
    require(shared["macro_reviewer"] == "research-narrative-assessor", "macro reviewer")
    require(shared["meso_micro_reviewer"] == "academic-language-assessor", "language reviewer")
    require(shared["reviewers_run_in_parallel_on_same_frozen_reader_artifact_or_bundle"], "parallel readiness")
    require(shared["repair_interface"]["single_writer_brief_format"] == "yaml", "YAML writer brief")
    require(shared["repair_interface"]["raw_assessment_reports_visible_to_writer"] is False, "raw reports sealed")
    require(shared["repair_interface"]["writer_uses_same_owner_for_bounded_section_passes"], "same writer bounded passes")
    require(shared["repair_interface"]["multiple_fragment_writers_forbidden"], "no fragmented writers")
    require(shared["preservation"]["fresh_independent_preservation_review_required_after_repair"], "fresh preservation review")
    require(shared["fresh_readiness"]["fresh_narrative_and_language_reassessment_required_after_repair"], "fresh readiness reassessment")
    require(shared["logical_integrity"]["sha_or_content_digest_forbidden_in_new_llm_facing_artifacts"], "no LLM-facing hashes")
    require(shared["logical_integrity"]["legacy_digest_fields"] == "readable_but_ignored", "legacy digest compatibility")

    limitation = shared["limitation_policy"]
    require(limitation["omit_elsewhere"], "limitations omitted outside authority")
    require(limitation["cross_reference_or_pointer_elsewhere_forbidden"], "no limitation pointers")
    require("advance_the_immediate_reasoning" in limitation["exception"], "narrow limitation exception")

    terminology = shared["terminology_policy"]
    require(terminology["reviewer"] == "academic-language-assessor", "language owns terminology")
    require(terminology["separate_terminology_skill_or_artifact_forbidden"], "no separate terminology interface")
    require(terminology["single_paper_is_insufficient_to_establish_standard_usage"], "standardity evidence threshold")
    require(
        set(terminology["core_term_roles"])
        == {"title", "summary_or_abstract", "question", "objective", "contribution", "study_object", "measurement", "inference", "design", "interpretation"},
        "core-term definition",
    )

    narrative = read(SKILLS / "research-narrative-assessor" / "SKILL.md")
    profiles_text = read(SKILLS / "research-narrative-assessor" / "references" / "profiles.md")
    for profile in ("Idea", "Proposal", "Perspective", "Article"):
        require(profile in profiles_text, f"narrative profile {profile}")
    for decision in (
        "narrative_ready",
        "minor_narrative_revision",
        "major_narrative_revision",
        "clarification_required",
        "independent_review_pending",
    ):
        require(decision in narrative, f"narrative decision {decision}")
    require("narrative-repair-plan-rNNN.yaml" in narrative, "YAML repair output")
    require("content-preservation" in narrative.lower(), "preservation mode")
    shared_source = "\n".join(
        read(path)
        for path in (SKILLS / "research-narrative-assessor").rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".py"}
    )
    require("tests/" not in shared_source and "tests\\" not in shared_source, "shared assessor embeds a fixture path")
    progressive_examples = read(
        SKILLS / "research-narrative-assessor" / "references" / "progressive-error-examples.md"
    )
    normalized_examples = " ".join(progressive_examples.split())
    for generalization_guard in (
        "Do not match literal phrases",
        "Positive boundary:",
        "Error boundary:",
        "no simpler faithful route exists",
    ):
        require(
            generalization_guard in normalized_examples,
            f"shared assessor example generalization guard: {generalization_guard}",
        )

    perspective_examples = "\n".join(
        read(path)
        for path in (
            SKILLS / "perspective-input-builder" / "SKILL.md",
            SKILLS / "perspective-input-builder" / "templates" / "perspective-input-template.md",
            SKILLS / "perspective-argument-architect" / "references" / "contestability-constraints.md",
            SKILLS / "perspective-claim-evidence-curator" / "references" / "evidence-grading.md",
        )
    )
    for leaked_example in ("AI 辅助", "中药复方", "多中心 RCT", "降低了 30%", "某些传染病", "Nature Medicine", "Lancet Digital Health"):
        require(leaked_example not in perspective_examples, f"Perspective example specialization: {leaked_example}")

    language = read(SKILLS / "academic-language-assessor" / "SKILL.md")
    terminology_ref = read(SKILLS / "academic-language-assessor" / "references" / "terminology-review.md")
    require("exact recommended" in (language + terminology_ref).lower(), "terminology replacement is executable")
    require("first-use" in (language + terminology_ref).lower(), "first-use guidance")
    require("one paper" in terminology_ref.lower(), "single-paper safeguard")
    require("term-register" not in (language + terminology_ref), "no term-register artifact")

    orchestrators = {
        "idea": (SKILLS / "research-idea-orchestrator" / "SKILL.md", "Establish editorial readiness", "**Evaluate.**"),
        "proposal": (SKILLS / "proposal-orchestrator" / "SKILL.md", "**Assess and normalize.**", "**Run blind final evaluation.**"),
        "perspective": (SKILLS / "perspective-orchestrator" / "SKILL.md", "STEP 9: Editorial Quality Cycle", "STEP 10: Final Evaluator"),
        "article": (SKILLS / "article-orchestrator" / "SKILL.md", "**Assess readiness.**", "**Evaluate the delivery object.**"),
    }
    for workflow, (path, readiness_marker, final_marker) in orchestrators.items():
        text = read(path)
        require("research-narrative-assessor" in text, f"{workflow} narrative route")
        require("academic-language-assessor" in text, f"{workflow} language route")
        require(ordered(text, readiness_marker, final_marker), f"{workflow} readiness precedes final evaluator")
        require("medical-journal-review" in text, f"{workflow} journal review route")

    proposal_drafter = read(SKILLS / "proposal-drafter" / "SKILL.md")
    require("proposal-content-plan" in proposal_drafter, "proposal content plan")
    require("fresh" in proposal_drafter.lower() and "writer" in proposal_drafter.lower(), "separate proposal planner/writer")

    options_template = yaml.safe_load(read(SKILLS / "proposal-drafter" / "templates" / "template-proposal-background-path-options.yaml"))
    selection_template = yaml.safe_load(read(SKILLS / "proposal-orchestrator" / "templates" / "template-proposal-background-path-selection.yaml"))
    content_plan_template = yaml.safe_load(read(SKILLS / "proposal-drafter" / "templates" / "template-proposal-content-plan.yaml"))
    require(options_template["schema"] == "proposal-background-path-options.v1", "proposal background options schema")
    require(options_template["option_count"] in (2, 3), "proposal background option count")
    require(options_template["recommendation"] is None, "proposal options have no recommendation")
    require(options_template["ranking"] is None, "proposal options have no ranking")
    require(options_template["selection_status"] == "human_background_path_selection_required", "proposal options selection stop")
    require(selection_template["schema"] == "proposal-background-path-selection.v1", "proposal background selection schema")
    require(selection_template["selection_source"] == "user", "proposal selection is human")
    require(
        {"selection_mode", "user_authorization_text", "accepted_sole_path"} <= set(selection_template),
        "proposal sole-path acceptance shape",
    )
    require(selection_template["selection_mode"] is None, "proposal selection mode must be chosen explicitly")
    require(selection_template["selected_option_id"] is None, "proposal option branch defaults null")
    require(selection_template["accepted_sole_path"] is None, "proposal sole-path branch defaults null")
    require(selection_template["options_ref"] is None, "proposal options reference defaults null")
    require(content_plan_template["schema"] == "proposal-content-plan.v2", "proposal content plan v2")
    require(
        set((content_plan_template["background_argumentation"] or {}).keys())
        >= {"selection_source", "selection_mode", "user_authorization_text", "selected_path_ref", "primary_mode", "opening", "argument_units", "synthesis"},
        "proposal v2 background contract",
    )

    proposal_policy = registry["artifact_completeness_policy"]["proposal_background_argumentation_contract"]
    require(
        proposal_policy["default_sequence"]
        == [
            "readiness",
            "candidate_background_path_planning",
            "human_background_path_selection",
            "formal_content_planning",
            "complete_proposal_writing",
            "independent_evaluation",
        ],
        "proposal background default sequence",
    )
    option_policy = proposal_policy["options_artifact"]
    require(option_policy["minimum_options"] == 2 and option_policy["maximum_options"] == 3, "registry candidate cardinality")
    require(option_policy["recommendation"] is None and option_policy["ranking"] is None, "registry neutral options")
    require(option_policy["score_forbidden"], "registry forbids option scores")
    require(option_policy["fabricated_alternative_forbidden"], "registry forbids fake options")
    require(
        proposal_policy["selection_bypass_sources"] == ["user_explicit", "binding_constraint"],
        "proposal candidate bypass authority",
    )
    require(
        proposal_policy["selection_artifact"]["hybrid_request_route"] == "new_candidate_background_path_round",
        "proposal hybrid returns to candidates",
    )
    selection_modes = proposal_policy["selection_artifact"]["selection_modes"]
    require(set(selection_modes) == {"option_selection", "sole_path_acceptance"}, "proposal selection authority modes")
    require(selection_modes["sole_path_acceptance"]["options_ref"] is None, "sole-path acceptance has no options ref")
    require(selection_modes["sole_path_acceptance"]["user_acceptance_required"], "sole-path acceptance is user authorized")
    require(
        selection_modes["option_selection"]["options_ref_must_resolve_to_packaged_options_artifact"],
        "proposal options reference must resolve",
    )
    require(
        selection_modes["option_selection"]["selected_option_id_must_resolve_exactly_once_in_referenced_options"],
        "proposal selected option must resolve exactly once",
    )
    require(
        selection_modes["sole_path_acceptance"]["accepted_outline_must_be_functionally_complete"],
        "proposal accepted sole path must be complete",
    )
    require(
        proposal_policy["content_plan"]["required_schema_for_new_full_proposal"] == "proposal-content-plan.v2",
        "registry v2 new proposal plan",
    )
    require(proposal_policy["content_plan"]["legacy_v1_readable"], "registry v1 history readable")
    require(
        proposal_policy["content_plan"]["existing_draft_targeted_revision_requires_migration"] is False,
        "existing proposal does not require v2 migration",
    )
    selection_binding = proposal_policy["content_plan"]["selection_authority_binding"]
    require(
        selection_binding["selected_path_ref_must_resolve_to_frozen_selection_artifact"],
        "proposal plan must resolve the frozen selection",
    )
    require(
        selection_binding["user_authorization_text_must_match_selection_exactly"],
        "proposal plan must preserve exact user authorization",
    )
    require(
        proposal_policy["instance_separation"]["pairwise_distinct_instance_ids_required"],
        "candidate planner/formal planner/writer separation",
    )
    evaluator_policy = proposal_policy["blind_final_evaluator"]
    require(
        evaluator_policy["forbidden_project_artifact_roles"]
        == ["proposal_background_path_options", "proposal_background_path_selection", "proposal_content_plan"],
        "proposal final evaluator path isolation",
    )
    require(evaluator_policy["fixed_mode_names_headings_numbering_or_literal_transition_are_hard_gates"] is False, "functional evaluator gate")
    require(evaluator_policy["functional_absence_or_gap_to_rationale_break_is_clarity_failure"], "functional Clarity failure")

    proposal_edges = [edge for edge in registry["workflow_edges"] if edge["workflow"] == "proposal" and edge["destination"] == "proposal-drafter"]
    proposal_triggers = {edge["trigger"] for edge in proposal_edges}
    require("background_path_options_required" in proposal_triggers, "proposal candidate planner edge")
    require("background_path_selection_recorded_or_user_explicit_or_binding_constraint" in proposal_triggers, "proposal formal planner edge")
    proposal_state = registry["workflow_state_policy"]
    require("human_background_path_selection_required" in proposal_state["pause_states"], "proposal human selection pause")
    require(
        proposal_state["resume_policy"]["human_background_path_selection_required"] == "planning",
        "proposal human selection resume",
    )
    proposal_transitions = {
        (item["from"], item["to"], item["trigger"])
        for item in proposal_state["lifecycle_transitions"]
    }
    required_proposal_transitions = {
        ("preprocessing", "planning", "proposal_readiness_passed_and_background_planning_started"),
        ("planning", "human_background_path_selection_required", "proposal_background_path_options_frozen"),
        ("planning", "human_background_path_selection_required", "sole_background_path_requires_user_acceptance_or_constraint"),
        ("human_background_path_selection_required", "planning", "user_background_path_selected_and_selection_artifact_frozen"),
        ("human_background_path_selection_required", "planning", "user_accepts_sole_background_path_and_selection_artifact_frozen"),
        ("human_background_path_selection_required", "planning", "user_supplies_additional_background_organizing_constraint"),
        ("planning", "artifact_frozen", "proposal_content_plan_v2_frozen"),
        ("artifact_frozen", "writing", "full_proposal_writer_dispatched"),
        ("writing", "artifact_frozen", "complete_proposal_version_frozen"),
    }
    require(required_proposal_transitions <= proposal_transitions, "proposal planning lifecycle reachability")
    require(
        "human_background_path_selection_required"
        not in proposal_state["version_gate"]["required_before_states"],
        "proposal pre-writing human selection is not an evaluated-version gate",
    )
    proposal_state_schema = read(
        SKILLS / "proposal-orchestrator" / "references" / "workflow-state-schema.md"
    )
    require("clarification_stop" in proposal_state_schema, "proposal lifecycle target is declared")
    require("editorial_revision_required" in proposal_state_schema, "proposal editorial revision state is aligned")
    require("specialist_review_pending" in proposal_state_schema, "proposal specialist review state is aligned")
    require("editorial_repair_required" not in proposal_state_schema, "obsolete editorial state is absent")
    require("journal_review_pending" not in proposal_state_schema, "obsolete journal state is absent")

    authority_gate = registry["workflow_state_machines"]["proposal"]["scenario_entry_gate_contracts"]["standard"]["background_path_authority_frozen"]
    authority_modes = authority_gate["authority_modes"]
    require(
        authority_modes["option_selection"]["required_artifact_roles"]
        == ["proposal_background_path_options", "proposal_background_path_selection"],
        "proposal option-selection authority gate",
    )
    require(
        authority_modes["sole_path_acceptance"]["required_artifact_roles"]
        == ["proposal_background_path_selection"]
        and authority_modes["sole_path_acceptance"]["forbidden_artifact_roles"]
        == ["proposal_background_path_options"],
        "proposal sole-path authority gate",
    )
    require(
        authority_modes["bypass"]["required_artifact_roles"] == ["proposal_content_plan"]
        and set(authority_modes["bypass"]["forbidden_artifact_roles"])
        == {"proposal_background_path_options", "proposal_background_path_selection"},
        "proposal bypass authority gate",
    )
    require(
        authority_modes["bypass"]["required_schema"] == "proposal-content-plan.v2",
        "proposal bypass entry gate enforces v2 plan",
    )

    for mode in ("option_selection", "sole_path_acceptance", "bypass"):
        valid_bundle = proposal_authority_bundle(mode)
        validate_proposal_background_authority_bundle(
            valid_bundle,
            authority_mode=mode,
            new_full_proposal=True,
        )
        run_entry_consumer(registry, valid_bundle, mode)
        run_package_consumer(registry, valid_bundle, mode)

    mixed_sole = proposal_authority_bundle("sole_path_acceptance")
    mixed_sole.insert(0, deepcopy(proposal_authority_bundle("option_selection")[0]))
    expect_authority_failure(mixed_sole, "sole_path_acceptance", "sole path with options artifact")
    expect_consumer_failure(registry, mixed_sole, "sole_path_acceptance", "sole path with options artifact", entry=True)
    expect_consumer_failure(registry, mixed_sole, "sole_path_acceptance", "sole path with options artifact")

    wrong_mode = deepcopy(proposal_authority_bundle("option_selection"))
    wrong_mode[1]["selection_mode"] = "sole_path_acceptance"
    expect_authority_failure(wrong_mode, "option_selection", "selection mode mismatch")
    expect_consumer_failure(registry, wrong_mode, "option_selection", "selection mode mismatch", entry=True)
    expect_consumer_failure(registry, wrong_mode, "option_selection", "selection mode mismatch")

    wrong_source = deepcopy(proposal_authority_bundle("option_selection"))
    wrong_source[1]["selection_source"] = "binding_constraint"
    expect_authority_failure(wrong_source, "option_selection", "selection source mismatch")
    expect_consumer_failure(registry, wrong_source, "option_selection", "selection source mismatch", entry=True)
    expect_consumer_failure(registry, wrong_source, "option_selection", "selection source mismatch")

    empty_authorization = deepcopy(proposal_authority_bundle("option_selection"))
    empty_authorization[1]["user_authorization_text"] = "  "
    expect_authority_failure(empty_authorization, "option_selection", "empty user authorization")
    expect_consumer_failure(registry, empty_authorization, "option_selection", "empty user authorization", entry=True)
    expect_consumer_failure(registry, empty_authorization, "option_selection", "empty user authorization")

    mixed_option_branch = deepcopy(proposal_authority_bundle("option_selection"))
    mixed_option_branch[1]["accepted_sole_path"] = {"primary_mode": "systematic"}
    expect_authority_failure(mixed_option_branch, "option_selection", "both selection branches populated")
    expect_consumer_failure(registry, mixed_option_branch, "option_selection", "both selection branches populated", entry=True)
    expect_consumer_failure(registry, mixed_option_branch, "option_selection", "both selection branches populated")

    wrong_options_ref = deepcopy(proposal_authority_bundle("option_selection"))
    wrong_options_ref[1]["options_ref"] = logical_ref("missing-options")
    expect_consumer_failure(registry, wrong_options_ref, "option_selection", "unresolved options reference", entry=True)
    expect_consumer_failure(registry, wrong_options_ref, "option_selection", "unresolved options reference")

    missing_selected_option = deepcopy(proposal_authority_bundle("option_selection"))
    missing_selected_option[1]["selected_option_id"] = "missing-option"
    expect_consumer_failure(registry, missing_selected_option, "option_selection", "unresolved selected option", entry=True)
    expect_consumer_failure(registry, missing_selected_option, "option_selection", "unresolved selected option")

    one_option_only = deepcopy(proposal_authority_bundle("option_selection"))
    one_option_only[0]["options"] = one_option_only[0]["options"][:1]
    one_option_only[0]["option_count"] = 1
    expect_consumer_failure(registry, one_option_only, "option_selection", "one option must use sole-path route", entry=True)
    expect_consumer_failure(registry, one_option_only, "option_selection", "one option must use sole-path route")

    wrong_option_count = deepcopy(proposal_authority_bundle("option_selection"))
    wrong_option_count[0]["option_count"] = 3
    expect_consumer_failure(registry, wrong_option_count, "option_selection", "option count mismatch", entry=True)
    expect_consumer_failure(registry, wrong_option_count, "option_selection", "option count mismatch")

    wrong_plan_ref = deepcopy(proposal_authority_bundle("option_selection"))
    wrong_plan_ref[2]["background_argumentation"]["selected_path_ref"] = logical_ref("unrelated-selection")
    expect_consumer_failure(registry, wrong_plan_ref, "option_selection", "unresolved plan selected-path reference")

    mismatched_plan_authorization = deepcopy(proposal_authority_bundle("option_selection"))
    mismatched_plan_authorization[2]["background_argumentation"]["user_authorization_text"] = "Different authorization."
    expect_consumer_failure(registry, mismatched_plan_authorization, "option_selection", "plan authorization mismatch")

    incomplete_sole_path = deepcopy(proposal_authority_bundle("sole_path_acceptance"))
    incomplete_sole_path[0]["accepted_sole_path"]["current_status_units"] = []
    expect_consumer_failure(registry, incomplete_sole_path, "sole_path_acceptance", "incomplete sole path", entry=True)
    expect_consumer_failure(registry, incomplete_sole_path, "sole_path_acceptance", "incomplete sole path")

    empty_list_entries = (
        ("evidence scope", lambda bundle: bundle[0]["accepted_sole_path"]["current_status_units"][0].__setitem__("evidence_scope", [""])),
        ("research-content mapping", lambda bundle: bundle[0]["accepted_sole_path"]["mappings"].__setitem__("research_content", [""])),
        ("evidence requirements", lambda bundle: bundle[0]["accepted_sole_path"].__setitem__("evidence_requirements", [""])),
    )
    for label, mutate in empty_list_entries:
        malformed_sole = deepcopy(proposal_authority_bundle("sole_path_acceptance"))
        mutate(malformed_sole)
        expect_consumer_failure(registry, malformed_sole, "sole_path_acceptance", f"empty {label}", entry=True)
        expect_consumer_failure(registry, malformed_sole, "sole_path_acceptance", f"empty {label}")

    bypass_with_selection = proposal_authority_bundle("bypass") + [
        deepcopy(proposal_authority_bundle("option_selection")[1])
    ]
    expect_authority_failure(bypass_with_selection, "bypass", "bypass with selection artifact")
    expect_consumer_failure(registry, bypass_with_selection, "bypass", "bypass with selection artifact", entry=True)
    expect_consumer_failure(registry, bypass_with_selection, "bypass", "bypass with selection artifact")

    legacy_new_plan = deepcopy(proposal_authority_bundle("bypass"))
    legacy_new_plan[0]["schema"] = "proposal-content-plan.v1"
    expect_authority_failure(legacy_new_plan, "bypass", "new full proposal with v1 plan")
    expect_consumer_failure(registry, legacy_new_plan, "bypass", "new full proposal with v1 plan", entry=True)
    expect_consumer_failure(registry, legacy_new_plan, "bypass", "new full proposal with v1 plan")

    condition_args = {
        "workflow": "proposal",
        "entry_mode": "standard",
        "new_full_proposal": True,
        "editorial_repair_occurred": False,
        "proposal_handoff_candidate": False,
        "current_dossier_biomedical_or_clinical": False,
        "journal_matching_requested": False,
        "biomedical_candidate_route": False,
    }
    require(
        package_requirement_condition_met(
            "standard_default_candidate_route",
            proposal_background_authority_mode="option_selection",
            **condition_args,
        ),
        "scenario verifier recognizes option-selection package condition",
    )
    require(
        not package_requirement_condition_met(
            "standard_default_candidate_route",
            proposal_background_authority_mode="sole_path_acceptance",
            **condition_args,
        ),
        "sole-path package forbids options artifact",
    )
    for mode in ("option_selection", "sole_path_acceptance"):
        require(
            package_requirement_condition_met(
                "background_options_selected_or_sole_path_accepted",
                proposal_background_authority_mode=mode,
                **condition_args,
            ),
            f"scenario verifier recognizes {mode}",
        )
    require(
        not package_requirement_condition_met(
            "background_options_selected_or_sole_path_accepted",
            proposal_background_authority_mode="bypass",
            **condition_args,
        ),
        "bypass package forbids selection artifact",
    )
    require(
        package_requirement_condition_met(
            "new_full_proposal",
            proposal_background_authority_mode="bypass",
            **condition_args,
        ),
        "scenario verifier recognizes new full proposal",
    )
    try:
        package_requirement_condition_met(
            "unsupported_condition",
            proposal_background_authority_mode="option_selection",
            **condition_args,
        )
    except ScenarioViolation as exc:
        require(exc.code == "package_input_contract", "unsupported package condition error code")
    else:
        raise AssertionError("unsupported package condition accepted")

    perspective_architect = read(SKILLS / "perspective-argument-architect" / "SKILL.md")
    require("paragraph" in perspective_architect.lower() and "reader" in perspective_architect.lower(), "perspective reader-facing architecture")

    article_context = read(SKILLS / "article-context-builder" / "SKILL.md")
    article_readiness = read(SKILLS / "article-readiness-triage" / "SKILL.md")
    for marker in ("complete material inventory", "semantic authority"):
        require(marker in (article_context + article_readiness).lower(), f"article input discovery: {marker}")
    require("every supplied file" in article_context.lower(), "article intake cannot hide supplied material")

    evaluator_markers = {
        "idea": ("only project artifact", "other reviewer output", "prior versions", "deltas", "prior scores/decisions"),
        "proposal": ("final proposal", "context/readiness report", "repair brief", "delta", "prior evaluation"),
        "perspective": ("final perspective alone", "narrative/language report", "repair brief", "revision delta", "previous draft"),
        "article": ("final manuscript", "narrative and language assessors", "repair briefs", "deltas", "prior evaluations"),
    }
    for workflow, evaluator_name in (
        ("idea", "idea-evaluator"),
        ("proposal", "proposal-evaluator"),
        ("perspective", "perspective-evaluator"),
        ("article", "article-evaluator"),
    ):
        text = " ".join(read(SKILLS / evaluator_name / "SKILL.md").lower().split())
        require("files_read" in text, f"{workflow} evaluator files_read")
        require("current" in text and "complete" in text, f"{workflow} final current artifact")
        require(all(term in text for term in evaluator_markers[workflow]), f"{workflow} evaluator forbidden history")

    # New interfaces use readable logical identity. Legacy compatibility prose may
    # mention digests, but no newly produced field may serialize one.
    interface_roots = [
        SKILLS / "research-narrative-assessor",
        SKILLS / "proposal-orchestrator",
        SKILLS / "perspective-orchestrator",
        SKILLS / "article-orchestrator",
    ]
    serialized_field = re.compile(r"(?im)^\s*[a-z0-9_-]*(?:sha256|content_digest|source_digest|file_digest)\s*:")
    for root in interface_roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}:
                require(not serialized_field.search(read(path)), f"new persisted digest field: {path.relative_to(REPO)}")

    print("cross-workflow narrative contract: 51 skills, 22 reviewers, all guards passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
