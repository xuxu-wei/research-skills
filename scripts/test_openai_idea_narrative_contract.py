#!/usr/bin/env python3
"""Deterministic contracts for Idea editorial readiness and repair."""

from __future__ import annotations

import copy
import importlib.util
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from test_openai_phase4_scenarios import (
    FIXTURE_ROOT,
    PLUGIN,
    SCHEMA_PATH,
    ScenarioEngine,
    ScenarioViolation,
    load_yaml,
    require,
)


REPO = Path(__file__).resolve().parents[1]


def load_narrative_validator() -> Any:
    path = (
        PLUGIN
        / "skills"
        / "idea-narrative-assessor"
        / "scripts"
        / "validate_narrative_outputs.py"
    )
    spec = importlib.util.spec_from_file_location("idea_narrative_output_validator", path)
    require(spec is not None and spec.loader is not None, "idea_editorial_validator", "module spec")
    sys.dont_write_bytecode = True
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_repair_action_guards(validator: Any) -> None:
    findings = {"NAR-001": {"finding_id": "NAR-001", "severity": "major"}}
    plan = {
        "decision": "major_narrative_revision",
        "source_artifact": {
            "artifact_id": "idea-dossier-v003",
            "version": "v003",
            "path": "dossiers/idea-dossier-v003.md",
        },
        "clarifications_required": [],
        "actions": [
            {
                "action_id": "NRP-001",
                "addresses_findings": ["NAR-001"],
                "priority": "major",
                "dossier_locator": {
                    "section_heading": "Background",
                    "subsection_heading": "Gap",
                    "content_anchor": "Current gap paragraph",
                },
                "operation": "consolidate",
                "current_problem": "The same boundary is repeated.",
                "target_state": "One authoritative statement remains.",
                "required_content_or_function": "Preserve the boundary once.",
                "content_to_preserve": ["The scientific boundary."],
                "content_to_remove_or_move": ["Duplicate boundary paragraphs."],
                "destination_if_moved": "Authoritative limitations subsection",
                "dependencies": [],
                "acceptance_test": "The boundary appears completely in one location only.",
            }
        ],
    }
    validator.validate_plan(plan, findings)
    incomplete = copy.deepcopy(plan)
    incomplete["actions"][0]["content_to_remove_or_move"] = []
    try:
        validator.validate_plan(incomplete, findings)
    except validator.ValidationError:
        return
    raise AssertionError("repair-plan validator accepted a non-executable consolidation")


def validate_assessment_identity_guard(validator: Any) -> None:
    dossier = {
        "artifact_id": "idea-dossier-v003",
        "version": "v003",
        "path": "dossiers/idea-dossier-v003.md",
    }
    handoff = {
        "artifact_id": "reader-handoff-v001",
        "version": "v001",
        "path": "context/reader-handoff-v001.yaml",
    }
    assessment = {
        "review_id": "narrative-assessment-r001",
        "reviewer_skill": "idea-narrative-assessor",
        "reviewer_instance_id": "fresh-narrative-r001",
        "workflow_id": "wf-assessment-test",
        "round_id": "round-001",
        "input_artifact_ids": [dossier["artifact_id"], handoff["artifact_id"]],
        "input_versions": [dossier["version"], handoff["version"]],
        "input_dossier": dossier,
        "reader_handoff": handoff,
        "files_read": [dossier["path"], handoff["path"]],
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "forbidden_project_artifacts_read": False,
        "source_edits_performed": False,
        "decision": "narrative_ready",
        "findings": [],
        "unresolved_issues": [],
    }
    validator.validate_assessment(assessment)
    mismatched = copy.deepcopy(assessment)
    mismatched["input_versions"][1] = "v999"
    try:
        validator.validate_assessment(mismatched)
    except validator.ValidationError:
        return
    raise AssertionError("narrative validator accepted mismatched input identities")


def validate_preservation_coverage_guards() -> None:
    validator = load_narrative_validator()
    validate_repair_action_guards(validator)
    validate_assessment_identity_guard(validator)
    categories = list(validator.PROTECTED_CATEGORY_CANONICAL[:5])
    with tempfile.TemporaryDirectory(prefix="openai-idea-preservation-validator-") as temp:
        root = Path(temp)
        register_path = root / "protected-content-register.yaml"
        prior = {
            "artifact_id": "idea-dossier-v003",
            "version": "v003",
            "path": "dossiers/idea-dossier-v003.md",
        }
        register = {
            "schema_version": "research-idea-protected-content-register.v2",
            "register_id": "protected-register-v003",
            "register_version": "v001",
            "source_artifact": prior,
            "identity_anchor": {
                "primary_research_question": "Can the defined study answer its primary question?",
                "primary_objective": "Complete the stated primary objective.",
                "study_object": "The defined study object.",
                "core_data_or_evidence_base": "The stated evidence base.",
                "primary_unit_of_inference": "The stated unit of inference.",
            },
            "category_coverage": [
                {
                    "category": category,
                    "source_status": "source_present",
                    "protected_item_ids": [f"PCR-{index:03d}"],
                    "not_applicable_reason": None,
                }
                for index, category in enumerate(categories, 1)
            ]
            + [
                {
                    "category": category,
                    "source_status": "source_absent",
                    "protected_item_ids": [],
                    "not_applicable_reason": (
                        "The frozen source contains no item in this category."
                    ),
                }
                for category in validator.PROTECTED_CATEGORY_CANONICAL[5:]
            ],
            "protected_items": [
                {
                    "protected_id": f"PCR-{index:03d}",
                    "category": category,
                    "source_locator": f"Section {index}",
                    "protected_content": f"Protected content {index}",
                    "required_revised_disposition": "retained_same_meaning",
                }
                for index, category in enumerate(categories, 1)
            ],
            "permitted_editorial_operations": sorted(validator.OPERATIONS),
            "prohibited_changes": ["change_study_identity_or_core_question"],
        }
        register["protected_items"][0]["source_context_locator"] = (
            "user-input-v001.md > binding objective"
        )
        register_path.write_text(
            yaml.safe_dump(register, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        revised = {
            "artifact_id": "idea-dossier-v004",
            "version": "v004",
            "path": "dossiers/idea-dossier-v004.md",
        }
        register_ref = {
            "artifact_id": register["register_id"],
            "version": "v001",
            "path": str(register_path),
        }
        delta = {
            "artifact_id": "revision-delta-v003-to-v004",
            "version": "v001",
            "path": "revisions/revision-delta-v003-to-v004.md",
        }
        inputs = {
            "prior_dossier": prior,
            "revised_dossier": revised,
            "protected_content_register": register_ref,
            "revision_delta": delta,
        }
        report = {
            "review_id": "content-preservation-r001",
            "reviewer_skill": "idea-narrative-assessor",
            "reviewer_instance_id": "fresh-preservation-r001",
            "workflow_id": "wf-preservation-test",
            "round_id": "round-001",
            "input_artifact_ids": [value["artifact_id"] for value in inputs.values()],
            "input_versions": [value["version"] for value in inputs.values()],
            "inputs": inputs,
            "files_read": [value["path"] for value in inputs.values()],
            "isolation_mode": "fresh_subagent",
            "prior_scores_visible": False,
            "source_edits_performed": False,
            "decision": "scientific_content_preserved",
            "protected_item_checks": [
                {
                    "protected_id": item["protected_id"],
                    "prior_locator": item["source_locator"],
                    "revised_locator": f"Revised {item['source_locator']}",
                    "semantic_status": "preserved",
                    "evidence": "Same bounded meaning and strength.",
                }
                for item in register["protected_items"]
            ],
            "undeclared_scientific_changes": [],
            "findings": [],
            "unresolved_issues": [],
        }
        validator.validate_register(register)
        validator.validate_preservation(report, register, register_path)

        missing_register_version = copy.deepcopy(register)
        missing_register_version.pop("register_version")
        try:
            validator.validate_register(missing_register_version)
        except validator.ValidationError:
            pass
        else:
            raise AssertionError("v2 register validator accepted a missing logical version")

        missing_anchor = copy.deepcopy(register)
        missing_anchor["identity_anchor"].pop("primary_objective")
        try:
            validator.validate_register(missing_anchor)
        except validator.ValidationError:
            pass
        else:
            raise AssertionError("register validator accepted fewer than five identity anchors")

        fictitious_absent_item = copy.deepcopy(register)
        absent_entry = fictitious_absent_item["category_coverage"][-1]
        absent_entry["protected_item_ids"] = ["PCR-999"]
        fictitious_absent_item["protected_items"].append(
            {
                "protected_id": "PCR-999",
                "category": "unsupported_claim_classes",
                "source_locator": "Invented locator",
                "protected_content": "Invented unsupported claim.",
                "required_revised_disposition": "retained_same_boundary",
            }
        )
        try:
            validator.validate_register(fictitious_absent_item)
        except validator.ValidationError:
            pass
        else:
            raise AssertionError(
                "register validator accepted a fictitious locator for a source-absent category"
            )

        empty_context_locator = copy.deepcopy(register)
        empty_context_locator["protected_items"][0]["source_context_locator"] = ""
        try:
            validator.validate_register(empty_context_locator)
        except validator.ValidationError:
            pass
        else:
            raise AssertionError("register validator accepted an empty context locator")

        negative_cases = []
        partial = copy.deepcopy(report)
        partial["protected_item_checks"].pop()
        negative_cases.append(partial)
        duplicate = copy.deepcopy(report)
        duplicate["protected_item_checks"].append(copy.deepcopy(duplicate["protected_item_checks"][0]))
        negative_cases.append(duplicate)
        unknown = copy.deepcopy(report)
        unknown["protected_item_checks"][0]["protected_id"] = "PCR-UNKNOWN"
        negative_cases.append(unknown)
        extra_input = copy.deepcopy(report)
        extra_input["inputs"]["language_actions"] = {
            "artifact_id": "language-actions",
            "version": "v001",
            "path": "reviews/language-actions.md",
        }
        extra_input["files_read"].append("reviews/language-actions.md")
        negative_cases.append(extra_input)
        wrong_source = copy.deepcopy(report)
        wrong_source["inputs"]["prior_dossier"]["version"] = "v002"
        negative_cases.append(wrong_source)
        wrong_provenance = copy.deepcopy(report)
        wrong_provenance["input_versions"][0] = "v002"
        negative_cases.append(wrong_provenance)
        for case in negative_cases:
            try:
                validator.validate_preservation(case, register, register_path)
            except validator.ValidationError:
                continue
            raise AssertionError("preservation validator accepted incomplete or mismatched coverage")


def artifact(
    registry: dict[str, Any],
    *,
    artifact_id: str,
    version: str,
    round_id: str,
    source_skill: str,
    actor: str,
    based_on: list[str],
    change_type: str,
    path: str,
    role: str,
    content: str = "fixture content",
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "version_id": version,
        "workflow_id": "wf-phase4-idea-001",
        "round_id": round_id,
        "plugin_version": registry["plugin_version"],
        "source_skill": source_skill,
        "created_by_instance_id": actor,
        "based_on": based_on,
        "change_type": change_type,
        "path": path,
        "status": "final",
        "content_digest": "computed",
        "frozen": True,
        "artifact_role": role,
        "content": content,
    }


def review_event(
    registry: dict[str, Any],
    *,
    event_id: str,
    actor: str,
    destination: str,
    reviewer_role: str,
    review_id: str,
    round_id: str,
    inputs: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    decision: str,
    findings: list[dict[str, Any]] | None = None,
    extra_report: dict[str, Any] | None = None,
    expected_state_after: str,
) -> dict[str, Any]:
    edge = next(
        edge
        for edge in registry["workflow_edges"]
        if edge["workflow"] == "idea"
        and edge["source"] == "research-idea-orchestrator"
        and edge["destination"] == destination
    )
    input_ids = [item["artifact_id"] for item in inputs]
    input_versions = [item["version_id"] for item in inputs]
    input_paths = [item["path"] for item in inputs]
    report = {
        "review_id": review_id,
        "reviewer_skill": destination,
        "reviewer_instance_id": actor,
        "reviewer_role": reviewer_role,
        "review_scope": "fixture editorial contract",
        "workflow_id": "wf-phase4-idea-001",
        "round_id": round_id,
        "input_artifact_ids": input_ids,
        "input_versions": input_versions,
        "files_read": input_paths,
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "source_edits_performed": False,
        "decision": decision,
        "findings": findings or [],
        "unresolved_issues": [item["finding_id"] for item in findings or []],
    }
    if extra_report:
        report.update(extra_report)
    return {
        "event_id": event_id,
        "type": "review",
        "actor_instance_id": actor,
        "source_skill": "research-idea-orchestrator",
        "destination_skill": destination,
        "dispatch_mode": edge["dispatch_mode"],
        "trigger": edge["trigger"],
        "allowed_read_paths": input_paths,
        "allowed_write_paths": [item["path"] for item in outputs],
        "input_artifact_ids": input_ids,
        "input_versions": input_versions,
        "review_report": report,
        "outputs": outputs,
        "expected_state_after": expected_state_after,
    }


def build_editorial_repair_fixture(registry: dict[str, Any]) -> dict[str, Any]:
    base = copy.deepcopy(load_yaml(FIXTURE_ROOT / "idea.yaml"))
    prefix = copy.deepcopy(base["events"][:3])
    dossier = prefix[0]["outputs"][0]
    context = next(item for item in base["initial_artifacts"] if item["artifact_id"] == "idea-context-v1")
    dossier_ref = f"{dossier['artifact_id']}@{dossier['version_id']}"

    first_assessment = artifact(
        registry,
        artifact_id="idea-narrative-901",
        version="nr901",
        round_id="editorial-001",
        source_skill="idea-narrative-assessor",
        actor="idea-narrative-901",
        based_on=[dossier_ref],
        change_type="narrative_assessment",
        path="03_ideas/nodes/idea-001/reviews/narrative-assessment-r901.md",
        role="narrative_assessment",
    )
    first_plan = artifact(
        registry,
        artifact_id="idea-narrative-plan-901",
        version="nrp901",
        round_id="editorial-001",
        source_skill="idea-narrative-assessor",
        actor="idea-narrative-901",
        based_on=[dossier_ref, "idea-narrative-901@nr901"],
        change_type="narrative_repair_plan",
        path="03_ideas/nodes/idea-001/reviews/narrative-repair-plan-r901.yaml",
        role="narrative_repair_plan",
    )
    narrative_finding = {
        "finding_id": "narrative-major-901",
        "title": "Reader reasoning chain is incomplete",
        "dossier_locator": "Section 3",
        "source_review_id": "idea-narrative-r901",
        "severity": "major",
        "blocking": False,
        "fixability": "fixable",
        "status": "routed_to_revision",
        "owner": "multi-path-idea-generator",
        "route": "targeted_revision",
    }
    initial_narrative = review_event(
        registry,
        event_id="idea-narrative-r901",
        actor="idea-narrative-901",
        destination="idea-narrative-assessor",
        reviewer_role="narrative",
        review_id="idea-narrative-r901",
        round_id="editorial-001",
        inputs=[dossier, context],
        outputs=[first_assessment, first_plan],
        decision="major_narrative_revision",
        findings=[narrative_finding],
        expected_state_after="editorial_review_pending",
    )

    first_language = artifact(
        registry,
        artifact_id="idea-language-901",
        version="lr901",
        round_id="editorial-001",
        source_skill="academic-language-assessor",
        actor="idea-language-901",
        based_on=[dossier_ref],
        change_type="language_assessment",
        path="03_ideas/nodes/idea-001/reviews/language-assessment-r901.md",
        role="language_assessment_report",
    )
    initial_language = review_event(
        registry,
        event_id="idea-language-r901",
        actor="idea-language-901",
        destination="academic-language-assessor",
        reviewer_role="language",
        review_id="idea-language-r901",
        round_id="editorial-001",
        inputs=[dossier, context],
        outputs=[first_language],
        decision="submission_ready",
        expected_state_after="editorial_revision_required",
    )

    protected = artifact(
        registry,
        artifact_id="idea-protected-901",
        version="pcr901",
        round_id="editorial-001",
        source_skill="research-idea-orchestrator",
        actor="research-idea-orchestrator-901",
        based_on=[dossier_ref],
        change_type="protected_content_freeze",
        path="03_ideas/nodes/idea-001/revisions/round-editorial-001/protected-content-register.yaml",
        role="protected_content_register",
    )
    protect_event = {
        "event_id": "idea-protect-r901",
        "type": "orchestrator_record",
        "actor_instance_id": "research-idea-orchestrator-901",
        "source_skill": "research-idea-orchestrator",
        "allowed_read_paths": [dossier["path"]],
        "allowed_write_paths": [protected["path"]],
        "input_artifact_ids": [dossier["artifact_id"]],
        "input_versions": [dossier["version_id"]],
        "outputs": [protected],
        "expected_state_after": "editorial_revision_required",
    }

    writer_brief = artifact(
        registry,
        artifact_id="idea-editorial-writer-brief-901",
        version="ewb901",
        round_id="editorial-001",
        source_skill="research-idea-orchestrator",
        actor="research-idea-orchestrator-901",
        based_on=[
            dossier_ref,
            "idea-narrative-901@nr901",
            "idea-narrative-plan-901@nrp901",
            "idea-language-901@lr901",
            "idea-protected-901@pcr901",
        ],
        change_type="editorial_repair_writer_brief",
        path="03_ideas/nodes/idea-001/revisions/round-editorial-001/editorial-repair-writer-brief-r901.yaml",
        role="editorial_repair_writer_brief",
    )
    writer_brief_inputs = [dossier, first_assessment, first_plan, first_language, protected]
    writer_brief_event = {
        "event_id": "idea-editorial-writer-brief-r901",
        "type": "orchestrator_record",
        "actor_instance_id": "research-idea-orchestrator-901",
        "source_skill": "research-idea-orchestrator",
        "allowed_read_paths": [item["path"] for item in writer_brief_inputs],
        "allowed_write_paths": [writer_brief["path"]],
        "input_artifact_ids": [item["artifact_id"] for item in writer_brief_inputs],
        "input_versions": [item["version_id"] for item in writer_brief_inputs],
        "outputs": [writer_brief],
        "expected_state_after": "editorial_revision_required",
    }

    repaired = artifact(
        registry,
        artifact_id="ideas-v1-editorial",
        version="v001e",
        round_id="editorial-001",
        source_skill="multi-path-idea-generator",
        actor="idea-editorial-writer-901",
        based_on=[
            dossier_ref,
            "idea-editorial-writer-brief-901@ewb901",
            "idea-protected-901@pcr901",
        ],
        change_type="editorial_repair",
        path="03_ideas/nodes/idea-001/dossiers/idea-dossier-v001e.md",
        role="idea_dossier",
        content="complete editorial repair dossier",
    )
    repaired_ref = f"{repaired['artifact_id']}@{repaired['version_id']}"
    repair_delta = artifact(
        registry,
        artifact_id="idea-editorial-delta-901",
        version="erd901",
        round_id="editorial-001",
        source_skill="multi-path-idea-generator",
        actor="idea-editorial-writer-901",
        based_on=[
            dossier_ref,
            "idea-editorial-writer-brief-901@ewb901",
            "idea-protected-901@pcr901",
            repaired_ref,
        ],
        change_type="editorial_repair_delta",
        path="03_ideas/nodes/idea-001/revisions/round-editorial-001/revision-delta.md",
        role="revision_delta",
    )
    generator_edge = next(
        edge
        for edge in registry["workflow_edges"]
        if edge["workflow"] == "idea"
        and edge["source"] == "research-idea-orchestrator"
        and edge["destination"] == "multi-path-idea-generator"
    )
    repair_inputs = [dossier, writer_brief, protected]
    repair_event = {
        "event_id": "idea-editorial-repair-901",
        "type": "produce",
        "actor_instance_id": "idea-editorial-writer-901",
        "source_skill": "research-idea-orchestrator",
        "destination_skill": "multi-path-idea-generator",
        "dispatch_mode": generator_edge["dispatch_mode"],
        "trigger": generator_edge["trigger"],
        "allowed_read_paths": [item["path"] for item in repair_inputs],
        "allowed_write_paths": [repaired["path"], repair_delta["path"]],
        "input_artifact_ids": [item["artifact_id"] for item in repair_inputs],
        "input_versions": [item["version_id"] for item in repair_inputs],
        "outputs": [repaired, repair_delta],
        "expected_state_after": "artifact_frozen",
    }

    preservation = artifact(
        registry,
        artifact_id="idea-preservation-901",
        version="cpr901",
        round_id="editorial-001",
        source_skill="idea-narrative-assessor",
        actor="idea-preservation-reviewer-901",
        based_on=[dossier_ref, repaired_ref, "idea-protected-901@pcr901", "idea-editorial-delta-901@erd901"],
        change_type="content_preservation_review",
        path="03_ideas/nodes/idea-001/reviews/content-preservation-r901.md",
        role="content_preservation_report",
    )
    preservation_event = review_event(
        registry,
        event_id="idea-preservation-r901",
        actor="idea-preservation-reviewer-901",
        destination="idea-narrative-assessor",
        reviewer_role="content-preservation",
        review_id="idea-preservation-r901",
        round_id="editorial-001",
        inputs=[dossier, repaired, protected, repair_delta],
        outputs=[preservation],
        decision="scientific_content_preserved",
        expected_state_after="artifact_frozen",
    )

    fresh_assessment = artifact(
        registry,
        artifact_id="idea-narrative-902",
        version="nr902",
        round_id="editorial-002",
        source_skill="idea-narrative-assessor",
        actor="idea-narrative-902",
        based_on=[repaired_ref],
        change_type="narrative_assessment",
        path="03_ideas/nodes/idea-001/reviews/narrative-assessment-r902.md",
        role="narrative_assessment",
    )
    fresh_plan = artifact(
        registry,
        artifact_id="idea-narrative-plan-902",
        version="nrp902",
        round_id="editorial-002",
        source_skill="idea-narrative-assessor",
        actor="idea-narrative-902",
        based_on=[repaired_ref, "idea-narrative-902@nr902"],
        change_type="narrative_repair_plan",
        path="03_ideas/nodes/idea-001/reviews/narrative-repair-plan-r902.yaml",
        role="narrative_repair_plan",
    )
    fresh_narrative = review_event(
        registry,
        event_id="idea-narrative-r902",
        actor="idea-narrative-902",
        destination="idea-narrative-assessor",
        reviewer_role="narrative",
        review_id="idea-narrative-r902",
        round_id="editorial-002",
        inputs=[repaired, context],
        outputs=[fresh_assessment, fresh_plan],
        decision="narrative_ready",
        expected_state_after="editorial_review_pending",
    )
    fresh_language_report = artifact(
        registry,
        artifact_id="idea-language-902",
        version="lr902",
        round_id="editorial-002",
        source_skill="academic-language-assessor",
        actor="idea-language-902",
        based_on=[repaired_ref],
        change_type="language_assessment",
        path="03_ideas/nodes/idea-001/reviews/language-assessment-r902.md",
        role="language_assessment_report",
    )
    fresh_language = review_event(
        registry,
        event_id="idea-language-r902",
        actor="idea-language-902",
        destination="academic-language-assessor",
        reviewer_role="language",
        review_id="idea-language-r902",
        round_id="editorial-002",
        inputs=[repaired, context],
        outputs=[fresh_language_report],
        decision="submission_ready",
        expected_state_after="artifact_frozen",
    )

    evaluation = artifact(
        registry,
        artifact_id="idea-eval-902",
        version="er902",
        round_id="editorial-002",
        source_skill="idea-evaluator",
        actor="idea-evaluator-902",
        based_on=[repaired_ref],
        change_type="evaluation",
        path="03_ideas/nodes/idea-001/reviews/evaluation-r902.md",
        role="evaluation_report",
    )
    evaluator_event = review_event(
        registry,
        event_id="idea-evaluate-r902",
        actor="idea-evaluator-902",
        destination="idea-evaluator",
        reviewer_role="evaluator",
        review_id="idea-eval-r902",
        round_id="editorial-002",
        inputs=[repaired],
        outputs=[evaluation],
        decision="promote",
        extra_report={
            "reviewed_dossier_ref": {
                "artifact_id": repaired["artifact_id"],
                "version": repaired["version_id"],
                "path": repaired["path"],
            },
            "complete_dossier_confirmed": True,
            "dossier_only_input_confirmed": True,
            "identity_drift_detected": False,
            "prior_versions_visible": False,
            "revision_delta_visible": False,
        },
        expected_state_after="panel_pending",
    )

    base["fixture_id"] = "idea-editorial-repair-contract"
    base["events"] = prefix + [
        initial_narrative,
        initial_language,
        protect_event,
        writer_brief_event,
        repair_event,
        preservation_event,
        fresh_narrative,
        fresh_language,
        evaluator_event,
    ]
    base["expected"] = {
        "final_state": "panel_pending",
        "primary_versions": ["v001", "v001e"],
        "evaluator_instances": ["idea-evaluator-902"],
        "lifecycle_triggers": [
            "entry_gate_passed",
            "versioned_artifact_created",
            "idea_editorial_readiness_dispatched",
            "idea_editorial_revision_requested",
            "preserved_editorial_version_created",
            "idea_editorial_readiness_dispatched",
            "idea_editorial_readiness_passed",
            "independent_review_dispatched",
            "latest_version_accepted",
        ],
        "panel_role_instances": {},
        "dissent_ids": [],
        "required_destinations_in_order": [
            "multi-path-idea-generator",
            "idea-narrative-assessor",
            "academic-language-assessor",
            "multi-path-idea-generator",
            "idea-narrative-assessor",
            "idea-narrative-assessor",
            "academic-language-assessor",
            "idea-evaluator",
        ],
    }
    return base


def run_fixture(registry: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    schema = load_yaml(SCHEMA_PATH)
    with tempfile.TemporaryDirectory(prefix="openai-idea-editorial-contract-") as temp:
        return ScenarioEngine(fixture, registry, schema, Path(temp)).run()


def assert_rejected(
    registry: dict[str, Any],
    fixture: dict[str, Any],
    expected_error: str,
) -> None:
    try:
        run_fixture(registry, fixture)
    except ScenarioViolation as exc:
        require(exc.code == expected_error, "idea_editorial_negative", f"{expected_error}: {exc.code}")
    else:
        raise AssertionError(f"fixture should have failed with {expected_error}")


def validate_static_contracts(registry: dict[str, Any]) -> None:
    require(registry["plugin_version"] == "0.10.0", "idea_editorial_static", "version")
    require(len(registry["skills"]) == 50, "idea_editorial_static", "skill count")
    require(
        sum(item["role"] == "reviewer" for item in registry["skills"]) == 21,
        "idea_editorial_static",
        "reviewer count",
    )
    contract = registry["artifact_completeness_policy"]["idea_editorial_readiness_contract"]
    require(contract["repair_plan_format"] == "yaml", "idea_editorial_static", "repair plan format")
    require(contract["evaluator_reads_editorial_artifacts"] is False, "idea_editorial_static", "evaluator isolation")
    require(
        contract["writer_interface_artifact_role"] == "editorial_repair_writer_brief"
        and contract["writer_interface_source_skill"] == "research-idea-orchestrator"
        and contract["writer_brief_construction_reads_exactly"]
        == [
            "current_idea_dossier",
            "narrative_assessment",
            "narrative_repair_plan",
            "language_assessment_report",
            "protected_content_register",
        ]
        and contract["writer_brief_requires_source_review_binding"] is True
        and contract["writer_brief_requires_source_coverage_validation"] is True
        and contract["writer_reads_exactly"]
        == ["current_idea_dossier", "editorial_repair_writer_brief", "protected_content_register"]
        and contract["writer_forbidden_editorial_inputs"]
        == ["narrative_assessment", "narrative_repair_plan", "language_assessment_report"],
        "idea_editorial_static",
        "single writer interface registry contract",
    )
    require(
        contract["editorially_eligible_narrative_decisions"]
        == ["narrative_ready", "minor_narrative_revision"]
        and contract["editorially_eligible_language_decisions"]
        == ["submission_ready", "minor_language_revision"]
        and contract["ordinary_repair_decisions"]
        == ["major_narrative_revision", "major_language_revision"],
        "idea_editorial_static",
        "minor eligibility and major-only repair routing",
    )
    require(
        contract["clarification_required_route"]
        == "clarification_stop_then_fresh_assessment"
        and contract["needs_professional_editing_route"]
        == "editorial_revision_required_external_language_support_then_fresh_assessment",
        "idea_editorial_static",
        "non-writer stop routing",
    )
    minor_observation = contract["record_only_minor_observation"]
    require(
        minor_observation["single_report_path"]
        == "tests/idea-narrative-forward-0.9.0-preview.3/error-localization-report-r001.md"
        and minor_observation["required_conditions"]
        == [
            "severity_minor_or_suggestion",
            "localized_scope",
            "no_scientific_or_content_preservation_change",
            "no_decision_or_reader_eligibility_effect",
            "no_broad_recurrence",
        ]
        and minor_observation["required_fields"]
        == ["plugin_version", "observed_symptom", "suspected_diagnosis", "proposed_solution"]
        and minor_observation["forbidden_followups"]
        == ["new_correction", "reproduction_attempt", "extra_test"]
        and minor_observation["blocking_exceptions"]
        == [
            "critical_or_major_finding",
            "content_drift",
            "decision_or_readiness_effect",
            "broad_contamination",
            "invalid_deterministic_result",
        ],
        "idea_editorial_static",
        "single record-only minor-observation report contract",
    )
    actor_outputs = registry["scenario_eval_contract"]["runtime_artifact_role_contract"][
        "actor_output_roles_by_skill"
    ]
    require(
        "protected_content_register" in actor_outputs["research-idea-orchestrator"]
        and "editorial_repair_writer_brief"
        in actor_outputs["research-idea-orchestrator"],
        "idea_editorial_static",
        "orchestrator protected register output authorization",
    )
    package_requirements = registry["scenario_eval_contract"]["package_input_contracts"]["idea"]["required_inputs"]
    preservation = next(item for item in package_requirements if item["artifact_role"] == "content_preservation_report")
    writer_brief_requirement = next(
        item
        for item in package_requirements
        if item["artifact_role"] == "editorial_repair_writer_brief"
    )
    require(
        preservation.get("count_per_editorially_repaired_current_dossier") == 1,
        "idea_editorial_static",
        "preservation cardinality",
    )
    require(
        writer_brief_requirement["source_skill"] == "research-idea-orchestrator"
        and writer_brief_requirement["include_all_created"] is True,
        "idea_editorial_static",
        "writer brief package lineage",
    )
    generator_edge = next(
        edge
        for edge in registry["workflow_edges"]
        if edge["workflow"] == "idea"
        and edge["source"] == "research-idea-orchestrator"
        and edge["destination"] == "multi-path-idea-generator"
    )
    require(
        "approved_editorial_repair_writer_brief" in generator_edge["input_contract"]
        and "narrative_repair_plan" not in generator_edge["input_contract"],
        "idea_editorial_static",
        "generator receives approved writer brief, not assessor plan",
    )
    require(
        "editorial_repair" in registry["artifact_completeness_policy"]["idea_dossier_change_types"],
        "idea_editorial_static",
        "editorial repair change type",
    )
    generator_handoff = (
        PLUGIN
        / "skills"
        / "multi-path-idea-generator"
        / "references"
        / "downstream-handoff-rules.md"
    ).read_text(encoding="utf-8-sig")
    normalized_generator_handoff = " ".join(generator_handoff.split())
    require(
        "change_type: editorial_repair" in generator_handoff
        and "change_type: editorial_repair_delta" in generator_handoff
        and "every frozen included repair item ID" in generator_handoff
        and "acceptance-test evidence in the delta" in generator_handoff
        and "summary as an index to its `source_locator`" in generator_handoff
        and "map every `protected_id`" in generator_handoff
        and "temporary role-based list from the new title" in normalized_generator_handoff
        and "unambiguous modifier attachment" in normalized_generator_handoff
        and "compact concordance check" in normalized_generator_handoff
        and "result of an all-occurrence scan" in normalized_generator_handoff
        and "replacement invents another compressed label" in normalized_generator_handoff
        and "unresolved critical or major language finding blocks persistence" in normalized_generator_handoff
        and "Consistency does not require repeating a definition" in normalized_generator_handoff
        and "sequential component that begins only after a primary study succeeds"
        in normalized_generator_handoff
        and "parallel, adaptive, iterative, nested, or multiple dependent components"
        in normalized_generator_handoff
        and "design-faithful placement map" in normalized_generator_handoff
        and "bounded internal passes" in normalized_generator_handoff
        and "Never persist section fragments or split authorship across writers"
        in normalized_generator_handoff
        and "compact verification index" in normalized_generator_handoff
        and "never carries its full entry conditions, alternative branches, stopping branch"
        in normalized_generator_handoff
        and "Traceability, symmetry, and a mandatory section are not reasons"
        in normalized_generator_handoff
        and "Do not compute, request, report, or persist a content hash"
        in normalized_generator_handoff
        and "Do not create or finalize the delta until the final whole-dossier scan"
        in normalized_generator_handoff
        and "Any later dossier edit invalidates the delta"
        in normalized_generator_handoff,
        "idea_editorial_static",
        "editorial repair lineage types",
    )
    generator_skill = (
        PLUGIN / "skills" / "multi-path-idea-generator" / "SKILL.md"
    ).read_text(encoding="utf-8-sig")
    delegate_briefs = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "references"
        / "delegate-brief-templates.md"
    ).read_text(encoding="utf-8-sig")
    normalized_delegate_briefs = " ".join(delegate_briefs.split())
    require(
        "Never inherit a legacy input artifact's plugin version" in generator_skill
        and "Do not compute, request, report, or persist SHA/content hashes"
        in generator_skill
        and "a path-only lineage entry is invalid" in generator_skill
        and "complete `working_assumption` objects" in generator_skill
        and "Never invent the assumed value" in generator_skill
        and "Active plugin version: <PLUGIN_VERSION>" in delegate_briefs
        and "path-only lineage is invalid" in delegate_briefs
        and "current preflight report or a" in delegate_briefs
        and "Never choose or complete an" in delegate_briefs
        and "never the prior dossier's legacy version" in delegate_briefs
        and "map every frozen included repair item ID" in delegate_briefs
        and "an included action lacks" in delegate_briefs
        and "Forbidden reads: <narrative/language reports, assessor repair plan"
        in delegate_briefs
        and "Normalized repair actions:" in delegate_briefs
        and "Use\nonly the normalized repair actions in this brief"
        in delegate_briefs
        and "bounded section groups" in delegate_briefs
        and "different writers must not author" in delegate_briefs
        and "independent fragments" in delegate_briefs
        and "Keep the delta compact" in delegate_briefs
        and "Do not create or finalize the delta until the whole-dossier scan"
        in normalized_delegate_briefs
        and "Any later dossier edit invalidates the delta" in normalized_delegate_briefs
        and "Do not\ncompute, request, report, or persist a SHA/content hash"
        in delegate_briefs,
        "idea_editorial_static",
        "active plugin-version binding",
    )
    assumption_rules = (
        PLUGIN
        / "skills"
        / "methodology-statistics-preflight"
        / "references"
        / "working-assumption-rules.md"
    ).read_text(encoding="utf-8-sig")
    normalized_assumption_rules = " ".join(assumption_rules.split())
    require(
        "at least one minimally viable scientific route already exists" in normalized_assumption_rules
        and "if the assumption is false, a bounded adjustment remains possible" in normalized_assumption_rules
        and "must not select among statistical, measurement, or design specifications" in normalized_assumption_rules
        and "explicitly and conditionally accepted in the current methodology/statistics preflight report" in normalized_assumption_rules
        and "may only carry that approved assumption verbatim" in normalized_assumption_rules
        and "neither can create or approve one" in normalized_assumption_rules
        and "may complete the plan as if the stated assumption holds" in normalized_assumption_rules
        and "must not phrase it as verified evidence" in normalized_assumption_rules,
        "idea_editorial_static",
        "bounded working-assumption route",
    )
    dossier_quality = (
        PLUGIN
        / "skills"
        / "multi-path-idea-generator"
        / "references"
        / "generation-quality-gates.md"
    ).read_text(encoding="utf-8-sig")
    require(
        "one authoritative location in section 14 for complete limitations and working"
        in dossier_quality
        and "design-specific stopping logic only in Methods" in dossier_quality,
        "idea_editorial_static",
        "separate limitation/assumption and design-logic authorities",
    )
    normalized_dossier_quality = " ".join(dossier_quality.split())
    require(
        "this pass must cover every occurrence of each core role" in normalized_dossier_quality
        and "must reject newly invented compressed replacement labels" in normalized_dossier_quality
        and "not an eligibility/alternative/stop decision tree" in normalized_dossier_quality
        and "optional placement pattern" in normalized_dossier_quality
        and "other architectures use a design-faithful placement map"
        in normalized_dossier_quality
        and "never use broad traceability as a reason to mention it everywhere"
        in normalized_dossier_quality
        and "contract-fixed scaffold labels remain unchanged" in normalized_dossier_quality
        and "what a prior version did or did not read" in normalized_dossier_quality,
        "idea_editorial_static",
        "whole-dossier terminology repair check",
    )
    endpoint_checks = (
        PLUGIN
        / "skills"
        / "methodology-statistics-preflight"
        / "references"
        / "endpoint-metric-checks.md"
    ).read_text(encoding="utf-8-sig")
    normalized_endpoint_checks = " ".join(endpoint_checks.split())
    require(
        "method detail matched to Idea-stage evidence" in normalized_dossier_quality
        and "unsupported universal thresholds" in normalized_dossier_quality
        and "scientifically different primary metrics" in normalized_dossier_quality
        and "Do not force every systems, identification, or multi-task study"
        in normalized_endpoint_checks
        and "metric A or metric B" in normalized_endpoint_checks,
        "idea_editorial_static",
        "idea-stage method specificity without invented protocol detail",
    )
    narrative_skill = (
        PLUGIN / "skills" / "idea-narrative-assessor" / "SKILL.md"
    ).read_text(encoding="utf-8-sig")
    narrative_rubric = (
        PLUGIN
        / "skills"
        / "idea-narrative-assessor"
        / "references"
        / "narrative-rubric.md"
    ).read_text(encoding="utf-8-sig")
    narrative_patterns = (
        PLUGIN
        / "skills"
        / "idea-narrative-assessor"
        / "references"
        / "narrative-error-patterns.md"
    ).read_text(encoding="utf-8-sig")
    normalized_narrative_rubric = " ".join(narrative_rubric.split())
    require(
        "Never retain a\n  pointer or cross-reference to section 14" in dossier_quality
        and "Never leave a pointer or\ncross-reference to the authoritative section"
        in narrative_rubric,
        "idea_editorial_static",
        "no limitation cross-section pointers",
    )
    require(
        "Keep narrative prominence proportional" in normalized_narrative_rubric
        and "one technical authority location" in normalized_narrative_rubric
        and "implementation objects, records, or interfaces" in normalized_narrative_rubric
        and "Conditional extension crowds out the core" in narrative_patterns,
        "idea_editorial_static",
        "proportionate conditional-extension narrative",
    )
    dossier_contract = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "references"
        / "idea-dossier-contract.md"
    ).read_text(encoding="utf-8-sig")
    normalized_dossier_contract = " ".join(dossier_contract.split())
    require(
        "do not expose machine enum tokens in reader-facing prose or tables" in normalized_dossier_contract
        and "list it once under section 14's `Working assumptions`" in normalized_dossier_contract
        and "must not introduce additional unresolved specifications absent from that list" in normalized_dossier_contract,
        "idea_editorial_static",
        "reader-language states and unified pending specifications",
    )
    require(
        "Optional placement pattern for a sequential downstream component"
        in normalized_dossier_contract
        and "parallel, adaptive, iterative, nested, or multiple dependent components"
        in normalized_dossier_contract
        and "Absence from a section is valid" in normalized_dossier_contract
        and "Conditional scientific purpose only" in normalized_dossier_contract
        and "The sole complete authority for eligibility, operations, mutually exclusive alternatives"
        in normalized_dossier_contract
        and "append a final prose recap" in normalized_dossier_contract
        and "not from repeated prose or fixed cardinalities" in normalized_dossier_contract
        and "Design eligibility, mutually exclusive analysis alternatives" in normalized_dossier_contract
        and "Section 14 must not restate either decision tree" in normalized_dossier_contract,
        "idea_editorial_static",
        "contingent component section projection",
    )
    artifact_contracts = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "references"
        / "artifact-contracts.md"
    ).read_text(encoding="utf-8-sig")
    require(
        "evidence_limitations_ref:" not in artifact_contracts,
        "idea_editorial_static",
        "no empty limitations pointer",
    )
    dossier_template = (
        PLUGIN / "skills" / "multi-path-idea-generator" / "templates" / "idea-dossier.md"
    ).read_text(encoding="utf-8-sig")
    round_contract = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "references"
        / "workflow-manifest.md"
    ).read_text(encoding="utf-8-sig")
    round_template = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "templates"
        / "round-manifest.md"
    ).read_text(encoding="utf-8-sig")
    require(
        "version_id: v001\npath:" in dossier_template
        and "workflow_id:" in round_contract
        and "artifact_index_path:" in round_contract
        and "workflow_status:" in round_contract
        and round_template.startswith("---\n")
        and "workflow_id:" in round_template
        and "plugin_version:" in round_template
        and "current_artifact_version:" in round_template
        and "latest_evaluated_version:" in round_template
        and "failure_route:" in round_template,
        "idea_editorial_static",
        "dossier and round-manifest template bindings",
    )
    preflight_templates = [
        (
            PLUGIN
            / "skills"
            / "methodology-statistics-preflight"
            / "templates"
            / name
        ).read_text(encoding="utf-8-sig")
        for name in (
            "template-methodology-statistics-preflight-report.md",
            "template-preflight-failure-report.md",
        )
    ]
    for preflight_template in preflight_templates:
        require(
            preflight_template.startswith("---\n")
            and "reviewer_skill: methodology-statistics-preflight" in preflight_template
            and "reviewer_instance_id:" in preflight_template
            and "input_artifact_ids: []" in preflight_template
            and "input_versions: []" in preflight_template
            and "files_read: []" in preflight_template
            and "isolation_mode: fresh_subagent" in preflight_template,
            "idea_editorial_static",
            "preflight template provenance",
        )
    editorial_readiness = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "references"
        / "editorial-readiness-and-preservation.md"
    ).read_text(encoding="utf-8-sig")
    normalized_editorial_readiness = " ".join(editorial_readiness.split())
    orchestrator_skill = (
        PLUGIN / "skills" / "research-idea-orchestrator" / "SKILL.md"
    ).read_text(encoding="utf-8-sig")
    writer_brief_validator = (
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "scripts"
        / "validate_editorial_repair_writer_brief.py"
    ).read_text(encoding="utf-8-sig")
    require(
        "Minor findings remain visible but do not by themselves force another repair cycle"
        in normalized_editorial_readiness
        and "narrative decision is `narrative_ready` or `minor_narrative_revision`"
        in normalized_editorial_readiness
        and "language decision is `submission_ready` or `minor_language_revision`"
        in normalized_editorial_readiness
        and "unsupported completion claim blocks preservation review"
        in normalized_editorial_readiness,
        "idea_editorial_static",
        "major-only editorial repair trigger",
    )
    require(
        "freeze `protected-content-register.yaml` and `included_repair_item_ids`"
        in normalized_editorial_readiness
        and "Do not give the writer incompatible prescriptions to interpret"
        in normalized_editorial_readiness
        and "keep the narrative action's required rhetorical function"
        in normalized_editorial_readiness
        and "keep the language action's reader-facing wording"
        in normalized_editorial_readiness,
        "idea_editorial_static",
        "frozen repair scope and action-conflict resolution",
    )
    require(
        "the approved brief is the sole writer-facing repair interface"
        in normalized_editorial_readiness
        and "not writer inputs" in normalized_editorial_readiness,
        "idea_editorial_static",
        "single normalized writer-facing repair interface",
    )
    require(
        "Before the target dossier is frozen" in editorial_readiness
        and "returns the still-unfrozen candidate to the same writer"
        in normalized_editorial_readiness
        and "Do not dispatch preservation or readiness reviewers yet"
        in normalized_editorial_readiness
        and "pre_freeze_action_compliance_required" in writer_brief_validator,
        "idea_editorial_static",
        "pre-freeze writer-action compliance before independent review",
    )
    require(
        "localized omitted action or instruction deviation"
        in normalized_editorial_readiness
        and "continue without a new correction, reproduction attempt, or extra test"
        in normalized_editorial_readiness
        and "plugin version, observed symptom, suspected diagnosis, and proposed solution"
        in normalized_editorial_readiness
        and "tests/idea-narrative-forward-0.9.0-preview.3/error-localization-report-r001.md"
        in editorial_readiness
        and "Do not create a case-specific minor-issue report"
        in normalized_editorial_readiness,
        "idea_editorial_static",
        "low-impact minor execution deviations are recorded without retry",
    )
    require(
        "copy every `identity_anchor` frontmatter value verbatim"
        in normalized_editorial_readiness,
        "idea_editorial_static",
        "editorial writer preserves machine identity verbatim",
    )
    require(
        "included_repair_item_ids" in editorial_readiness
        and "source narrative assessment, narrative plan, and language assessment"
        in normalized_editorial_readiness
        and "--narrative-assessment" in editorial_readiness
        and "--narrative-plan" in editorial_readiness
        and "--language-assessment" in editorial_readiness
        and "--protected-register" in editorial_readiness
        and "An ancestral lineage register" in editorial_readiness
        and "scripts/validate_editorial_repair_writer_brief.py" in orchestrator_skill
        and "validate_source_coverage" in writer_brief_validator
        and "validate_register_binding" in writer_brief_validator
        and "legacy mixed-semantics key is forbidden" in writer_brief_validator,
        "idea_editorial_static",
        "writer brief source coverage and canonical repair-item IDs",
    )
    preservation_contract = (
        PLUGIN
        / "skills"
        / "idea-narrative-assessor"
        / "references"
        / "content-preservation-contract.md"
    ).read_text(encoding="utf-8-sig")
    normalized_preservation_contract = " ".join(preservation_contract.split())
    require(
        "Every `source_locator` must resolve inside the register's `source_artifact`"
        in normalized_preservation_contract
        and "any binding user/context value that must survive repair is copied explicitly into `protected_content`"
        in normalized_preservation_contract
        and "source_context_locator" in normalized_preservation_contract
        and "must not reclassify it as an undeclared scientific addition"
        in normalized_preservation_contract
        and "`protected_content` is not a category summary"
        in normalized_preservation_contract
        and "split it into additional protected items"
        in normalized_preservation_contract
        and "record shared prerequisites separately from each branch's own eligibility"
        in normalized_preservation_contract
        and "Never turn a condition for one branch into a prerequisite for the whole component"
        in normalized_preservation_contract
        and "never omit a fallback" in normalized_preservation_contract
        and "`retained_once_at_authority_location` requires one complete occurrence"
        in normalized_preservation_contract
        and "preservation does not require the complete branch logic or limitation family to recur"
        in normalized_preservation_contract
        and "require identical values" in normalized_preservation_contract
        and "paraphrasing it fails preservation" in normalized_preservation_contract,
        "idea_editorial_static",
        "writer-resolvable protected locators",
    )
    language_skill = (
        PLUGIN / "skills" / "academic-language-assessor" / "SKILL.md"
    ).read_text(encoding="utf-8-sig")
    terminology_review = (
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "references"
        / "terminology-review.md"
    ).read_text(encoding="utf-8-sig")
    language_hard_gates = (
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "references"
        / "language-hard-gates.md"
    ).read_text(encoding="utf-8-sig")
    language_rubric = (
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "references"
        / "language-assessment-rubric.md"
    ).read_text(encoding="utf-8-sig")
    chinese_conventions = (
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "references"
        / "chinese-academic-language-conventions.md"
    ).read_text(encoding="utf-8-sig")
    language_candidate_scanner = (
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "scripts"
        / "scan_idea_language_candidates.py"
    ).read_text(encoding="utf-8-sig")
    normalized_language_skill = " ".join(language_skill.split())
    normalized_terminology_review = " ".join(terminology_review.split())
    normalized_language_hard_gates = " ".join(language_hard_gates.split())
    language_template = (
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "templates"
        / "language-assessment-report.md"
    ).read_text(encoding="utf-8-sig")
    require(
        "first-use" in normalized_language_skill
        and "compound-title" in normalized_language_skill
        and "scaffolding" in normalized_language_skill
        and "transient whole-dossier concordance"
        in normalized_language_skill
        and "Never replace one unverified compact label with another"
        in normalized_language_skill
        and "Every actionable finding (`critical`, `major`, or `minor`) needs all repair"
        in normalized_language_skill
        and "scripts/scan_idea_language_candidates.py <dossier>"
        in normalized_language_skill
        and "do not sample or stop after the first findings" in normalized_language_skill
        and "complete the four coverage passes defined by the rubric"
        in normalized_language_skill
        and all(
            coverage_name in normalized_language_skill
            for coverage_name in (
                "reader_entry",
                "core_scientific_role",
                "terminology_concordance",
                "local_language",
            )
        )
        and "Do not persist the scan or report a candidate without reader-grounded evidence"
        in normalized_language_skill
        and "Never use sibling-platform counterparts" in normalized_language_skill
        and "Separately inspect every scanner candidate classified as a mixed-language or internal token"
        in normalized_terminology_review,
        "idea_editorial_static",
        "language scaffolding boundary",
    )
    require(
        "why a definition is needed and where it belongs"
        in " ".join(narrative_skill.split())
        and "owns verified wording, standardity, translation, and replacement"
        in " ".join(narrative_skill.split()),
        "idea_editorial_static",
        "terminology placement versus wording ownership",
    )
    require(
        "The five-part reasoning chain, section order, section function"
        in " ".join(language_rubric.split())
        and "For non-Idea artifacts" in " ".join(chinese_conventions.split())
        and "narrative assessment owns that placement"
        in " ".join(chinese_conventions.split()),
        "idea_editorial_static",
        "narrative versus language flow and limitation ownership",
    )
    normalized_language_rubric = " ".join(language_rubric.split())
    require(
        "Finding severity and bounded reporting" in normalized_language_rubric
        and "materially wrong reading" in normalized_language_rubric
        and "Finding count is never a quality target" in normalized_language_rubric
        and "supporting diagnostic, implementation label, secondary outcome"
        in normalized_language_rubric
        and "Do not construct a gate failure by adding three unrelated minor"
        in normalized_language_hard_gates,
        "idea_editorial_static",
        "reader-impact severity calibration",
    )
    require(
        "central study object's head noun and role across title, summary, question, and contribution"
        in normalized_language_rubric
        and "study object, fitted model, representation output, and structural relation distinct"
        in normalized_language_rubric
        and "distinguishes the partition dimension"
        in normalized_language_rubric
        and "model recalibration, updating, adaptation, or refitting"
        in normalized_language_rubric,
        "idea_editorial_static",
        "central-object and validation-setting terminology coverage",
    )
    require(
        "scientifically distinct estimands, metrics" in normalized_language_skill
        and "different estimands, metrics, model definitions"
        in normalized_language_rubric
        and "do not present one alternative as a language replacement"
        in normalized_language_rubric.lower(),
        "idea_editorial_static",
        "language versus scientific-choice boundary",
    )
    require(
        "GROUP_READER_ENTRY" in language_candidate_scanner
        and "GROUP_COMPACT_LABEL" in language_candidate_scanner
        and "GROUP_TOKEN" in language_candidate_scanner
        and "read_text" in language_candidate_scanner
        and "write_text" not in language_candidate_scanner
        and all(
            case_term not in language_candidate_scanner
            for case_term in (
                "脓毒症",
                "RCT",
                "零边",
                "可观测性",
                "不变量",
                "失败图",
                "投影",
                "扰动",
                "候选",
                "降级",
                "弃权",
            )
        ),
        "idea_editorial_static",
        "bounded generic read-only language candidate scan",
    )
    require(
        "15 H2 headings" in normalized_language_skill
        and "do not score, translate, rename, or report them"
        in normalized_language_skill
        and "Their required scaffold occurrence is exempt"
        in normalized_terminology_review
        and "never count or translate them for this gate"
        in normalized_language_hard_gates,
        "idea_editorial_static",
        "fixed scaffold cannot become a language finding",
    )
    require(
        "Do not use the absence of an exact full-title string" in normalized_terminology_review
        and "semantic head" in normalized_terminology_review
        and "parse modifier attachment in every compound title phrase"
        in normalized_terminology_review
        and "Re-parse every proposed title replacement" in normalized_terminology_review
        and "Never replace an unverified compact label with another compact label"
        in normalized_terminology_review
        and "standard in only one target subfield but have a misleading everyday or cross-disciplinary reading"
        in normalized_terminology_review
        and "scientifically distinct objects, assessments, failure states, and actions"
        in normalized_terminology_review
        and "alternately names a diagnostic result, a decision"
        in normalized_terminology_review
        and "the actor or trigger, the affected object"
        in normalized_terminology_review
        and "standard in only one target subfield"
        in normalized_terminology_review
        and "eligibility, alternative-analysis, stopping, or interpretation consequence"
        in normalized_terminology_review
        and "another undefined compact label" in normalized_terminology_review
        and "Treat project-specific stage labels and technical validation labels as core"
        in normalized_terminology_review
        and "non-blocking schema handoff" in normalized_terminology_review
        and "Do not equate deferred operational detail" in normalized_terminology_review
        and "do not choose an option for the writer" in normalized_terminology_review
        and "identifies the pending specification" in normalized_terminology_review
        and "without prescribing which other reasoning locations" in normalized_terminology_review
        and "every reader-facing name" in normalized_terminology_review
        and "project-management or software metaphors" in normalized_terminology_review
        and "actual core scientific roles present in the dossier"
        in normalized_terminology_review
        and "Do not impose model, validation, branching, parameter-update, or failure-output roles"
        in normalized_terminology_review
        and "First use means the first reader-facing use of the compact label"
        in normalized_terminology_review
        and "Do not force a technical definition into the summary"
        in normalized_terminology_review
        and "not a term register or new artifact" in normalized_terminology_review,
        "idea_editorial_static",
        "focused terminology false-positive guards",
    )
    require(
        "actor--operation--object--criterion check" in normalized_terminology_review
        and "every named measurement or target quantity" in normalized_terminology_review
        and "every other compact role phrase" in normalized_terminology_review
        and "grammatical object remains an undefined project label"
        in normalized_terminology_review
        and "compact-label group is an attention aid, not a blacklist"
        in normalized_terminology_review
        and "named result or output that controls a scientific interpretation"
        in normalized_terminology_review
        and "A clearly prospective publication or dissemination target"
        in " ".join(chinese_conventions.split())
        and "Do not let a tone edit silently weaken"
        in " ".join(chinese_conventions.split()),
        "idea_editorial_static",
        "reader-entry operand coverage and prospective-target protection",
    )
    normalized_language_template = " ".join(language_template.split())
    require(
        "Preserve the semantic cardinality and format of contract-fixed fields"
        in normalized_terminology_review
        and "contract-fixed sentence count, field cardinality"
        in normalized_language_template,
        "idea_editorial_static",
        "language repairs preserve scaffold cardinality",
    )
    require(
        "finding_kind: <language | terminology>" in normalized_language_template
        and "recommended_form_or_plain_description" in normalized_language_template
        and "evidence_basis" in normalized_language_template
        and "first_use_definition" in normalized_language_template
        and "competing_forms_and_locators" in normalized_language_template
        and "any other core scientific role only when it actually occurs"
        not in normalized_language_template
        and "hypothesis target quantity" in normalized_language_template
        and "failure or negative-result output" in normalized_language_template
        and "do not persist the complete temporary list" in normalized_language_template,
        "idea_editorial_static",
        "complete-Idea terminology role coverage",
    )
    require(
        "Gate failure requires positive evidence" in normalized_language_hard_gates
        and "does not fail this gate merely because its formula" in normalized_language_hard_gates
        and "Future or prospective language for genuinely planned actions"
        in normalized_language_hard_gates
        and "Tense systematically contradicts the artifact's declared study status"
        in normalized_language_hard_gates,
        "idea_editorial_static",
        "terminology hard-gate evidence",
    )
    require(
        language_template.startswith("---\n")
        and "input_artifact_ids: []" in language_template
        and "scope: <complete_idea_dossier | complete_artifact | named_sections>" in language_template
        and "dossier_ref:" in language_template
        and "reader_handoff:" in language_template
        and "files_read: []" in language_template,
        "idea_editorial_static",
        "language report machine provenance",
    )
    state_policy = registry["workflow_state_policy"]
    classified_states = set(
        state_policy["active_states"]
        + state_policy["pause_states"]
        + state_policy["terminal_states"]
    )
    require(
        {"new_idea_required", "layout_migration_required"} <= classified_states
        and state_policy["resume_policy"]["new_idea_required"] == "preprocessing"
        and state_policy["resume_policy"]["layout_migration_required"] == "preprocessing",
        "idea_editorial_static",
        "identity and layout state classification",
    )
    transitions = {
        (item["from"], item["to"], item["trigger"])
        for item in state_policy["lifecycle_transitions"]
    }
    require(
        (
            "editorial_revision_required",
            "revision_required",
            "scientific_change_declared",
        )
        in transitions
        and (
            "editorial_revision_required",
            "new_idea_required",
            "identity_drift_detected",
        )
        in transitions
        and (
            "editorial_revision_required",
            "editorial_revision_required",
            "editorial_scope_violation_requires_writer_repair",
        )
        in transitions,
        "idea_editorial_static",
        "preservation failure routing",
    )
    language_decisions = registry["scenario_eval_contract"]["review_decision_contracts"][
        "academic-language-assessor"
    ]
    require(
        {"clarification_required", "independent_review_pending"}
        <= set(language_decisions["allowed"])
        and {"clarification_required", "independent_review_pending"}
        <= set(language_decisions["stop"]),
        "idea_editorial_static",
        "language operational decisions",
    )
    narrative_output_contract = (
        PLUGIN
        / "skills"
        / "idea-narrative-assessor"
        / "references"
        / "output-and-isolation-contract.md"
    ).read_text(encoding="utf-8-sig")
    normalized_narrative_output_contract = " ".join(narrative_output_contract.split())
    require(
        "do not delete or rename any of the 15 required H2 sections" in normalized_narrative_output_contract
        and "Evidence chains and Claim-Support remain mandatory" in normalized_narrative_output_contract
        and "Do not replace deleted limitation prose with pointers or cross-references" in normalized_narrative_output_contract
        and "minimum content remain in every affected required section" in normalized_narrative_output_contract,
        "idea_editorial_static",
        "schema-preserving narrative repair",
    )

    llm_contract_roots = [
        PLUGIN / "skills" / name
        for name in (
            "research-idea-orchestrator",
            "research-context-builder",
            "research-opportunity-mapper",
            "multi-path-idea-generator",
            "methodology-statistics-preflight",
            "idea-narrative-assessor",
            "idea-evaluator",
            "academic-language-assessor",
            "medical-journal-review",
            "idea-adversarial-review-panel",
            "idea-portfolio-assembler",
        )
    ]
    forbidden_schema_tokens = (
        "reviewed_dossier_digest",
        "current_artifact_digest",
        "dossier_digest:",
        "SHA-256 digests",
        "input_sha256",
        "sha256:",
        "content_digest:",
    )
    for root in llm_contract_roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}:
                text = path.read_text(encoding="utf-8-sig")
                for token in forbidden_schema_tokens:
                    require(token not in text, "idea_editorial_static", f"{path}: {token}")

    production_roots = [
        PLUGIN / "skills" / name
        for name in (
            "research-idea-orchestrator",
            "research-context-builder",
            "research-opportunity-mapper",
            "multi-path-idea-generator",
            "methodology-statistics-preflight",
            "idea-evaluator",
            "academic-language-assessor",
            "medical-journal-review",
            "idea-portfolio-assembler",
            "idea-narrative-assessor",
            "idea-adversarial-review-panel",
        )
    ]
    fixture_specific_tokens = (
        "sepsis",
        "脓毒症",
        "EXIT-SEP",
        "XBJ-SCAP",
        "MIMIC",
        "eICU",
        "digital twin",
        "数字孪生",
        "rct individual-level data",
        "individual-level rct data",
        "阶段三不能挽救阶段二失败",
        "stage iii cannot rescue stage ii failure",
        "观测投影",
        "投影可观测",
        "零边",
    )
    for root in production_roots:
        paths = root.rglob("*") if root.is_dir() else [root]
        for path in paths:
            if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".py"}:
                text = path.read_text(encoding="utf-8-sig").lower()
                for token in fixture_specific_tokens:
                    require(token.lower() not in text, "idea_editorial_static", f"{path}: {token}")


def main() -> int:
    registry = load_yaml(PLUGIN / "workflow-registry.yaml")
    validate_static_contracts(registry)
    validate_preservation_coverage_guards()
    fixture = build_editorial_repair_fixture(registry)
    result = run_fixture(registry, copy.deepcopy(fixture))
    require(result["final_state"] == "panel_pending", "idea_editorial_fixture", "final state")

    missing_register = copy.deepcopy(fixture)
    repair = next(item for item in missing_register["events"] if item["event_id"] == "idea-editorial-repair-901")
    index = repair["input_artifact_ids"].index("idea-protected-901")
    repair["input_artifact_ids"].pop(index)
    repair["input_versions"].pop(index)
    repair["allowed_read_paths"].remove(
        "03_ideas/nodes/idea-001/revisions/round-editorial-001/protected-content-register.yaml"
    )
    assert_rejected(registry, missing_register, "protected_content_register_missing")

    missing_writer_brief = copy.deepcopy(fixture)
    repair = next(item for item in missing_writer_brief["events"] if item["event_id"] == "idea-editorial-repair-901")
    index = repair["input_artifact_ids"].index("idea-editorial-writer-brief-901")
    repair["input_artifact_ids"].pop(index)
    repair["input_versions"].pop(index)
    repair["allowed_read_paths"].remove(
        "03_ideas/nodes/idea-001/revisions/round-editorial-001/editorial-repair-writer-brief-r901.yaml"
    )
    assert_rejected(registry, missing_writer_brief, "editorial_writer_brief_missing")

    report_exposed_to_writer = copy.deepcopy(fixture)
    repair = next(item for item in report_exposed_to_writer["events"] if item["event_id"] == "idea-editorial-repair-901")
    repair["input_artifact_ids"].append("idea-language-901")
    repair["input_versions"].append("lr901")
    repair["allowed_read_paths"].append(
        "03_ideas/nodes/idea-001/reviews/language-assessment-r901.md"
    )
    assert_rejected(registry, report_exposed_to_writer, "editorial_writer_isolation")

    missing_preservation = copy.deepcopy(fixture)
    missing_preservation["events"] = [
        item for item in missing_preservation["events"] if item["event_id"] != "idea-preservation-r901"
    ]
    assert_rejected(registry, missing_preservation, "content_preservation_missing")

    preservation_substitutes_narrative = copy.deepcopy(fixture)
    preservation_substitutes_narrative["events"] = [
        item for item in preservation_substitutes_narrative["events"] if item["event_id"] != "idea-narrative-r902"
    ]
    assert_rejected(registry, preservation_substitutes_narrative, "state_transition")

    print("OpenAI Idea narrative contract tests passed")
    print("editorial repair path: narrative+language -> protected register -> approved writer brief -> repair -> preservation -> fresh readiness -> evaluator")
    print(
        "negative guards: missing register, missing writer brief, report exposure, missing preservation, preservation cannot replace narrative, "
        "incomplete/duplicate/unknown preservation coverage"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
