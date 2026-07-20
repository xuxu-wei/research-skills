#!/usr/bin/env python3
"""Unit tests for the generic narrative-output validator."""

from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


MODULE_PATH = Path(__file__).with_name("validate_narrative_outputs.py")
SPEC = importlib.util.spec_from_file_location("narrative_validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def ref(artifact_id: str, version: str, path: str) -> dict[str, str]:
    return {"artifact_id": artifact_id, "version": version, "path": path}


def assessment(profile: str = "proposal", decision: str = "major_narrative_revision") -> dict:
    findings = []
    if decision not in {"narrative_ready", "independent_review_pending"}:
        findings = [
            {
                "finding_id": "NAR-001",
                "severity": "major" if decision == "major_narrative_revision" else "minor",
                "category": "reader_reasoning_chain",
                "artifact_locator": {"section_heading": "Introduction", "subsection_heading": None, "content_anchor": "opening"},
                "observed_evidence": "The gap is not stated.",
                "current_reader_effect": "The rationale is unclear.",
                "target_function": "State the unresolved gap before the objective.",
            }
        ]
    return {
        "schema_version": "research-narrative-assessment.v1",
        "assessment_id": "assessment-001",
        "review_id": "review-001",
        "reviewer_skill": "research-narrative-assessor",
        "reviewer_instance_id": "fresh-001",
        "workflow_id": "workflow-001",
        "round_id": "round-001",
        "profile": profile,
        "input_artifact_ids": ["artifact-001"],
        "input_versions": ["v001"],
        "input_artifact": ref("artifact-001", "v001", "artifact.md"),
        "input_component_refs": [],
        "reader_handoff": {"artifact_id": "embedded-reader-handoff", "version": "embedded", "path": None},
        "files_read": ["artifact.md"],
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "source_edits_performed": False,
        "decision": decision,
        "findings": findings,
        "unresolved_issues": [],
    }


def plan(source: dict) -> dict:
    actions = []
    if source["decision"] not in {"narrative_ready", "clarification_required", "independent_review_pending"}:
        actions = [
            {
                "action_id": "NRP-001",
                "addresses_findings": ["NAR-001"],
                "priority": "major",
                "artifact_locator": {"section_heading": "Introduction", "subsection_heading": None, "content_anchor": "opening"},
                "counterargument_or_boundary_family": None,
                "operation": "add_bridge",
                "current_problem": "The gap is absent.",
                "target_state": "The gap precedes the objective.",
                "required_content_or_function": "Connect current knowledge to the unresolved question.",
                "verified_term_replacement": None,
                "content_to_preserve": ["The objective and evidence state."],
                "content_to_remove_or_move": [],
                "destination_if_moved": None,
                "dependencies": [],
                "acceptance_test": "A new reader can identify the gap before the objective.",
            }
        ]
    return {
        "schema_version": "research-narrative-repair-plan.v1",
        "plan_id": "plan-001",
        "assessment_id": source["assessment_id"],
        "profile": source["profile"],
        "source_artifact": source["input_artifact"],
        "decision": source["decision"],
        "clarifications_required": ["Clarify the intended reader."] if source["decision"] == "clarification_required" else [],
        "actions": actions,
    }


def register() -> dict:
    categories = sorted(validator.CATEGORIES)
    coverage = []
    for category in categories:
        if category == "identity_and_question":
            coverage.append({"category": category, "source_status": "source_present", "protected_item_ids": ["PCR-001"], "not_applicable_reason": None})
        else:
            coverage.append({"category": category, "source_status": "source_absent", "protected_item_ids": [], "not_applicable_reason": "Not present in source."})
    return {
        "schema_version": "research-protected-content-register.v1",
        "register_id": "register-001",
        "register_version": "v001",
        "profile": "proposal",
        "source_artifact": ref("artifact-001", "v001", "prior.md"),
        "identity_anchors": [{"anchor_id": "ID-001", "kind": "question", "value": "Question", "source_locator": "Introduction: opening"}],
        "category_coverage": coverage,
        "protected_items": [
            {
                "protected_id": "PCR-001",
                "category": "identity_and_question",
                "source_locator": "Introduction: opening",
                "family_id": None,
                "protected_content": "Question",
                "required_disposition": "retained_same_meaning",
            }
        ],
        "permitted_editorial_operations": sorted(validator.OPERATIONS),
        "prohibited_changes": ["change_identity"],
    }


class ValidatorTests(unittest.TestCase):
    def test_assessment_and_plan_pass(self) -> None:
        source = assessment()
        findings = validator.validate_assessment(source)
        validator.validate_plan(plan(source), source, findings)

    def test_ready_has_empty_plan(self) -> None:
        source = assessment(decision="narrative_ready")
        findings = validator.validate_assessment(source)
        validator.validate_plan(plan(source), source, findings)

    def test_files_read_isolation_rejected(self) -> None:
        source = assessment()
        source["files_read"].append("prior-evaluation.md")
        with self.assertRaises(validator.ValidationError):
            validator.validate_assessment(source)

    def test_uncovered_major_rejected(self) -> None:
        source = assessment()
        findings = validator.validate_assessment(source)
        broken = plan(source)
        broken["actions"] = []
        with self.assertRaises(validator.ValidationError):
            validator.validate_plan(broken, source, findings)

    def test_dependency_cycle_rejected(self) -> None:
        source = assessment()
        findings = validator.validate_assessment(source)
        broken = plan(source)
        broken["actions"][0]["dependencies"] = ["NRP-001"]
        with self.assertRaises(validator.ValidationError):
            validator.validate_plan(broken, source, findings)

    def test_perspective_boundary_requires_family(self) -> None:
        source = assessment(profile="perspective")
        source["findings"][0]["category"] = "counterargument_boundary_authority"
        findings = validator.validate_assessment(source)
        with self.assertRaises(validator.ValidationError):
            validator.validate_plan(plan(source), source, findings)

    def test_hash_field_rejected(self) -> None:
        with self.assertRaises(validator.ValidationError):
            validator.reject_hash_fields({"content_digest": "x"}, "fixture")

    def test_register_and_preservation_pass(self) -> None:
        source_register = register()
        validator.validate_register(source_register)
        with tempfile.TemporaryDirectory() as temp:
            register_path = Path(temp) / "protected-content-register.yaml"
            register_path.write_text(yaml.safe_dump(source_register), encoding="utf-8")
            preservation = {
                "schema_version": "research-content-preservation-check.v1",
                "check_id": "check-001",
                "review_id": "review-002",
                "reviewer_skill": "research-narrative-assessor",
                "reviewer_instance_id": "fresh-002",
                "workflow_id": "workflow-001",
                "round_id": "round-002",
                "profile": "proposal",
                "input_artifact_ids": ["artifact-001", "artifact-002", "register-001", "delta-001"],
                "input_versions": ["v001", "v002", "v001", "v001"],
                "inputs": {
                    "prior_artifact": ref("artifact-001", "v001", "prior.md"),
                    "revised_artifact": ref("artifact-002", "v002", "revised.md"),
                    "protected_content_register": ref("register-001", "v001", str(register_path)),
                    "revision_delta": ref("delta-001", "v001", "delta.yaml"),
                },
                "files_read": ["prior.md", "revised.md", str(register_path), "delta.yaml"],
                "isolation_mode": "fresh_subagent",
                "prior_scores_visible": False,
                "source_edits_performed": False,
                "decision": "scientific_content_preserved",
                "protected_item_checks": [{"protected_id": "PCR-001", "prior_locator": "Introduction", "revised_locator": "Introduction", "semantic_status": "preserved", "evidence": "Same meaning."}],
                "undeclared_scientific_changes": [],
                "findings": [],
                "unresolved_issues": [],
            }
            validator.validate_preservation(preservation, source_register, register_path)
            broken = copy.deepcopy(preservation)
            broken["protected_item_checks"][0]["semantic_status"] = "changed"
            with self.assertRaises(validator.ValidationError):
                validator.validate_preservation(broken, source_register, register_path)


if __name__ == "__main__":
    unittest.main()
