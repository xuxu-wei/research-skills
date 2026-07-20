#!/usr/bin/env python3
"""Unit tests for the editorial-repair writer-brief validator."""

from __future__ import annotations

import copy
import unittest

from validate_editorial_repair_writer_brief import (
    ValidationError,
    validate_brief,
    validate_register_binding,
    validate_source_coverage,
)


BRIEF_PATH = "briefs/editorial-repair-writer-brief-r001.yaml"
NARRATIVE_ASSESSMENT_PATH = "reviews/narrative-assessment-r001.md"
NARRATIVE_PLAN_PATH = "reviews/narrative-repair-plan-r001.yaml"
LANGUAGE_ASSESSMENT_PATH = "reviews/language-assessment-r001.md"


def source_ref() -> dict:
    return {
        "artifact_id": "idea-dossier-v001",
        "version": "v001",
        "path": "dossiers/idea-dossier-v001.md",
    }


def valid_register() -> dict:
    return {
        "schema_version": "research-idea-protected-content-register.v2",
        "register_id": "protected-content-register-v001",
        "register_version": "v001",
        "source_artifact": source_ref(),
    }


def valid_action(
    repair_item_id: str,
    addresses: list[str],
    operation: str = "replace",
) -> dict:
    return {
        "repair_item_id": repair_item_id,
        "source_item_ids": [
            repair_item_id,
            *(finding_id for finding_id in addresses if finding_id != repair_item_id),
        ],
        "addresses_finding_ids": addresses,
        "locator": "Section 3 > Gap",
        "operation": operation,
        "problem": "The section does not perform its reader-facing function.",
        "target": "The section states the missing knowledge before the design response.",
        "required_function_or_term": "State the evidence gap in direct disciplinary language.",
        "content_to_preserve": {"protected_ids": ["PCR-001"]},
        "delete_move_disposition": "Remove repeated caveats; retain the boundary once.",
        "destination": [],
        "dependencies": [],
        "acceptance_test": "A reader identifies the gap without reading a later section.",
    }


def valid_brief() -> dict:
    first = valid_action("NRP-001", ["NAR-001"], "split")
    second = valid_action("NRP-002", ["NAR-002"], "consolidate")
    second["locator"] = "Sections 7 and 14"
    second["dependencies"] = ["NRP-001"]
    language = valid_action("LANG-001", ["LANG-001"], "define")
    return {
        "schema_version": "research-idea-editorial-repair-writer-brief.v1",
        "brief_id": "editorial-repair-writer-brief-r001",
        "workflow_id": "idea-workflow-001",
        "round_id": "r001",
        "active_plugin_version": "0.9.0-preview.3",
        "role": "Perform one editorial-only repair without changing science.",
        "source_artifact": source_ref(),
        "protected_content_register": {
            "register_id": "protected-content-register-v001",
            "version": "v001",
            "path": "state/protected-content-register-v001.yaml",
        },
        "source_review_binding": {
            "narrative_assessment": {
                "artifact_id": "narrative-assessment-r001",
                "version": "r001",
                "path": NARRATIVE_ASSESSMENT_PATH,
            },
            "narrative_repair_plan": {
                "artifact_id": "narrative-repair-plan-r001",
                "version": "r001",
                "path": NARRATIVE_PLAN_PATH,
            },
            "language_assessment": {
                "artifact_id": "language-assessment-r001",
                "version": "r001",
                "path": LANGUAGE_ASSESSMENT_PATH,
            },
        },
        "included_repair_item_ids": ["NRP-001", "NRP-002", "LANG-001"],
        "omitted_reported_nonblocking_findings": [
            {
                "finding_id": "LANG-002",
                "rationale": "This suggestion is outside the bounded repair.",
            }
        ],
        "included_nonblocking_finding_rationale": {
            "NAR-002": "The minor finding overlaps the required section repair."
        },
        "overlap_dispositions": [
            {
                "finding_ids": ["NRP-001", "LANG-001"],
                "disposition": "Combine the narrative function with the wording constraint.",
            }
        ],
        "identified_overlaps": [
            {"finding_ids": ["NRP-001", "LANG-001"]}
        ],
        "unresolved_overlaps": [],
        "all_overlaps_resolved": True,
        "normalized_repair_actions": [first, second, language],
        "writer_access": {
            "allowed_reads": [
                "dossiers/idea-dossier-v001.md",
                BRIEF_PATH,
                "state/protected-content-register-v001.yaml",
            ],
            "forbidden_reads": [
                "any narrative or language assessment report",
                "any assessor repair plan",
                "any revision delta",
                "any preflight",
                "any evaluation",
            ],
            "allowed_writes": {
                "complete_dossier": {
                    "artifact_id": "idea-dossier-v002",
                    "version": "v002",
                    "path": "dossiers/idea-dossier-v002.md",
                    "change_type": "editorial_repair",
                },
                "revision_delta": {
                    "artifact_id": "revision-delta-v001-to-v002",
                    "version": "v001-to-v002",
                    "path": "revisions/revision-delta-v001-to-v002.md",
                    "change_type": "editorial_repair_delta",
                },
            },
        },
        "mandatory_whole_dossier_checks": {
            "not_new_findings": True,
            "checks": [
                {
                    "check": "core-term concordance",
                    "instruction": "Scan first use and all competing forms.",
                    "acceptance": "One reader-facing form remains for each role.",
                }
            ],
        },
        "execution_and_handoff": {
            "section_passes": ["sections 1-4", "sections 5-14", "whole dossier"],
            "single_complete_target_dossier": True,
            "partial_artifacts_forbidden": True,
            "pre_freeze_action_compliance_required": True,
            "delta_after_dossier_freeze_only": True,
            "delta_requirements": [
                "map every included repair item",
                "map every protected item",
            ],
        },
    }


def valid_sources() -> tuple[dict, dict, dict]:
    narrative = {
        "assessment_id": "narrative-assessment-r001",
        "round_id": "r001",
        "workflow_id": "idea-workflow-001",
        "decision": "major_narrative_revision",
        "input_dossier": source_ref(),
        "findings": [
            {"finding_id": "NAR-001", "severity": "major"},
            {"finding_id": "NAR-002", "severity": "minor"},
        ],
        "unresolved_issues": [],
    }
    plan = {
        "plan_id": "narrative-repair-plan-r001",
        "assessment_id": "narrative-assessment-r001",
        "source_artifact": source_ref(),
        "actions": [
            {"action_id": "NRP-001", "addresses_findings": ["NAR-001"]},
            {"action_id": "NRP-002", "addresses_findings": ["NAR-002"]},
        ],
    }
    language = {
        "review_id": "language-assessment-r001",
        "round_id": "r001",
        "workflow_id": "idea-workflow-001",
        "decision": "major_language_revision",
        "dossier_ref": source_ref(),
        "findings": [
            {"finding_id": "LANG-001", "severity": "major"},
            {"finding_id": "LANG-002", "severity": "suggestion"},
        ],
        "unresolved_issues": ["LANG-001"],
    }
    return narrative, plan, language


def validate_with_sources(
    brief: dict,
    narrative: dict | None = None,
    plan: dict | None = None,
    language: dict | None = None,
) -> None:
    defaults = valid_sources()
    validate_source_coverage(
        brief,
        narrative if narrative is not None else defaults[0],
        plan if plan is not None else defaults[1],
        language if language is not None else defaults[2],
        narrative_assessment_path=NARRATIVE_ASSESSMENT_PATH,
        narrative_plan_path=NARRATIVE_PLAN_PATH,
        language_assessment_path=LANGUAGE_ASSESSMENT_PATH,
        brief_path=BRIEF_PATH,
    )


class EditorialRepairWriterBriefValidatorTests(unittest.TestCase):
    def assert_invalid(self, brief: dict) -> None:
        with self.assertRaises(ValidationError):
            validate_brief(brief, BRIEF_PATH)

    def test_valid_internal_consistency_passes(self) -> None:
        validate_brief(valid_brief(), BRIEF_PATH)

    def test_matching_protected_register_binding_passes(self) -> None:
        validate_register_binding(
            valid_brief(),
            valid_register(),
            "state/protected-content-register-v001.yaml",
        )

    def test_ancestral_protected_register_source_fails(self) -> None:
        register = valid_register()
        register["source_artifact"] = {
            "artifact_id": "idea-dossier-v000",
            "version": "v000",
            "path": "dossiers/idea-dossier-v000.md",
        }
        with self.assertRaises(ValidationError):
            validate_register_binding(
                valid_brief(),
                register,
                "state/protected-content-register-v001.yaml",
            )

    def test_non_mapping_fails(self) -> None:
        with self.assertRaises(ValidationError):
            validate_brief([], BRIEF_PATH)  # type: ignore[arg-type]

    def test_wrong_schema_version_fails(self) -> None:
        brief = valid_brief()
        brief["schema_version"] = "research-idea-editorial-repair-writer-brief.v2"
        self.assert_invalid(brief)

    def test_legacy_top_level_finding_ids_fail(self) -> None:
        brief = valid_brief()
        brief["included_finding_ids"] = brief["included_repair_item_ids"]
        self.assert_invalid(brief)

    def test_legacy_normalized_action_id_fails(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["finding_id"] = "NRP-001"
        self.assert_invalid(brief)

    def test_legacy_source_ids_fail(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["source_ids"] = ["NRP-001", "NAR-001"]
        self.assert_invalid(brief)

    def test_source_review_binding_is_required(self) -> None:
        brief = valid_brief()
        del brief["source_review_binding"]
        self.assert_invalid(brief)

    def test_duplicate_included_repair_item_fails(self) -> None:
        brief = valid_brief()
        brief["included_repair_item_ids"].append("NRP-001")
        self.assert_invalid(brief)

    def test_omitted_finding_without_rationale_fails(self) -> None:
        brief = valid_brief()
        brief["omitted_reported_nonblocking_findings"] = ["LANG-002"]
        self.assert_invalid(brief)

    def test_included_nonblocking_finding_must_be_addressed(self) -> None:
        brief = valid_brief()
        brief["included_nonblocking_finding_rationale"] = {"NAR-999": "Unknown source."}
        self.assert_invalid(brief)

    def test_missing_normalized_action_fails(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"].pop()
        self.assert_invalid(brief)

    def test_source_item_ids_must_match_repair_item(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["source_item_ids"] = ["NAR-001", "NRP-001"]
        self.assert_invalid(brief)

    def test_addresses_finding_ids_are_required(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["addresses_finding_ids"] = []
        self.assert_invalid(brief)

    def test_invalid_operation_fails(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["operation"] = "polish"
        self.assert_invalid(brief)

    def test_unknown_dependency_fails(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["dependencies"] = ["NRP-999"]
        self.assert_invalid(brief)

    def test_overlap_with_unknown_repair_item_fails(self) -> None:
        brief = valid_brief()
        brief["overlap_dispositions"][0]["finding_ids"] = ["NRP-001", "NRP-999"]
        self.assert_invalid(brief)

    def test_identified_overlap_without_disposition_fails(self) -> None:
        brief = valid_brief()
        brief["overlap_dispositions"] = []
        self.assert_invalid(brief)

    def test_unresolved_overlap_fails(self) -> None:
        brief = valid_brief()
        brief["unresolved_overlaps"] = [{"finding_ids": ["NRP-001", "LANG-001"]}]
        self.assert_invalid(brief)

    def test_extra_allowed_read_fails(self) -> None:
        brief = valid_brief()
        brief["writer_access"]["allowed_reads"].append(LANGUAGE_ASSESSMENT_PATH)
        self.assert_invalid(brief)

    def test_forbidden_read_category_must_be_explicit(self) -> None:
        brief = valid_brief()
        brief["writer_access"]["forbidden_reads"] = [
            item for item in brief["writer_access"]["forbidden_reads"] if "preflight" not in item
        ]
        self.assert_invalid(brief)

    def test_noncanonical_paths_fail(self) -> None:
        for path in ("dossiers\\idea-dossier-v001.md", "/tmp/idea-dossier-v001.md"):
            with self.subTest(path=path):
                brief = valid_brief()
                brief["source_artifact"]["path"] = path
                self.assert_invalid(brief)

    def test_output_must_be_new_and_not_overwrite_input(self) -> None:
        brief = valid_brief()
        output = brief["writer_access"]["allowed_writes"]["complete_dossier"]
        output["version"] = "v001"
        output["path"] = "dossiers/idea-dossier-v001.md"
        self.assert_invalid(brief)

    def test_hash_key_fails_at_any_depth(self) -> None:
        brief = copy.deepcopy(valid_brief())
        brief["writer_access"]["allowed_writes"]["complete_dossier"]["sha256"] = "forbidden"
        self.assert_invalid(brief)

    def test_execution_order_flags_are_required(self) -> None:
        for field in (
            "single_complete_target_dossier",
            "partial_artifacts_forbidden",
            "pre_freeze_action_compliance_required",
            "delta_after_dossier_freeze_only",
        ):
            with self.subTest(field=field):
                brief = valid_brief()
                brief["execution_and_handoff"][field] = False
                self.assert_invalid(brief)

    def test_v010_brief_requires_pre_freeze_action_compliance(self) -> None:
        brief = valid_brief()
        brief["active_plugin_version"] = "0.10.0"
        brief["execution_and_handoff"].pop("pre_freeze_action_compliance_required")
        self.assert_invalid(brief)

    def test_mandatory_check_cannot_introduce_findings(self) -> None:
        brief = valid_brief()
        brief["mandatory_whole_dossier_checks"]["checks"][0]["finding_id"] = "NEW-001"
        self.assert_invalid(brief)

    def test_three_source_coverage_passes(self) -> None:
        validate_with_sources(valid_brief())

    def test_source_binding_identity_mismatch_fails(self) -> None:
        brief = valid_brief()
        brief["source_review_binding"]["language_assessment"]["artifact_id"] = "wrong"
        with self.assertRaises(ValidationError):
            validate_with_sources(brief)

    def test_source_binding_path_mismatch_fails(self) -> None:
        brief = valid_brief()
        brief["source_review_binding"]["narrative_repair_plan"]["path"] = "reviews/other.yaml"
        with self.assertRaises(ValidationError):
            validate_with_sources(brief)

    def test_uncovered_major_narrative_finding_fails(self) -> None:
        narrative, plan, language = valid_sources()
        narrative["findings"].append({"finding_id": "NAR-003", "severity": "major"})
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)

    def test_missing_major_language_repair_item_fails(self) -> None:
        narrative, plan, language = valid_sources()
        language["findings"].append({"finding_id": "LANG-003", "severity": "critical"})
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)

    def test_normalized_addresses_must_match_source_action(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["addresses_finding_ids"] = ["NAR-002"]
        with self.assertRaises(ValidationError):
            validate_with_sources(brief)

    def test_normalized_source_items_must_match_source_action(self) -> None:
        brief = valid_brief()
        brief["normalized_repair_actions"][0]["source_item_ids"] = [
            "NRP-001",
            "NAR-999",
        ]
        with self.assertRaises(ValidationError):
            validate_with_sources(brief)

    def test_every_source_nonblocking_finding_needs_disposition(self) -> None:
        brief = valid_brief()
        brief["omitted_reported_nonblocking_findings"] = []
        with self.assertRaises(ValidationError):
            validate_with_sources(brief)

    def test_nonblocking_disposition_must_resolve_to_source(self) -> None:
        brief = valid_brief()
        brief["omitted_reported_nonblocking_findings"] = [
            {"finding_id": "LANG-999", "rationale": "Unknown source finding."}
        ]
        with self.assertRaises(ValidationError):
            validate_with_sources(brief)

    def test_source_reports_must_bind_same_dossier(self) -> None:
        narrative, plan, language = valid_sources()
        language["dossier_ref"]["version"] = "v000"
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)

    def test_narrative_ready_path_passes(self) -> None:
        brief = valid_brief()
        brief["included_repair_item_ids"] = ["LANG-001"]
        brief["normalized_repair_actions"] = [
            action
            for action in brief["normalized_repair_actions"]
            if action["repair_item_id"] == "LANG-001"
        ]
        brief["included_nonblocking_finding_rationale"] = {}
        brief["overlap_dispositions"] = []
        brief["identified_overlaps"] = []
        narrative, plan, language = valid_sources()
        narrative["decision"] = "narrative_ready"
        narrative["findings"] = []
        narrative["unresolved_issues"] = []
        plan["actions"] = []
        validate_with_sources(brief, narrative, plan, language)

    def test_language_ready_path_passes(self) -> None:
        brief = valid_brief()
        brief["included_repair_item_ids"] = ["NRP-001", "NRP-002"]
        brief["normalized_repair_actions"] = [
            action
            for action in brief["normalized_repair_actions"]
            if action["repair_item_id"].startswith("NRP-")
        ]
        brief["omitted_reported_nonblocking_findings"] = []
        brief["overlap_dispositions"] = []
        brief["identified_overlaps"] = []
        narrative, plan, language = valid_sources()
        language["decision"] = "submission_ready"
        language["findings"] = []
        language["unresolved_issues"] = []
        validate_with_sources(brief, narrative, plan, language)

    def test_language_minor_path_with_included_unresolved_finding_passes(self) -> None:
        brief = valid_brief()
        brief["included_nonblocking_finding_rationale"]["LANG-001"] = (
            "The minor language repair is deliberately included."
        )
        narrative, plan, language = valid_sources()
        language["decision"] = "minor_language_revision"
        language["findings"][0]["severity"] = "minor"
        validate_with_sources(brief, narrative, plan, language)

    def test_covered_narrative_unresolved_finding_passes(self) -> None:
        narrative, plan, language = valid_sources()
        narrative["unresolved_issues"] = ["NAR-001"]
        validate_with_sources(valid_brief(), narrative, plan, language)

    def test_narrative_clarification_decision_fails(self) -> None:
        narrative, plan, language = valid_sources()
        narrative["decision"] = "clarification_required"
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)

    def test_nonordinary_language_decisions_fail(self) -> None:
        for decision in (
            "clarification_required",
            "independent_review_pending",
            "needs_professional_editing",
        ):
            with self.subTest(decision=decision):
                narrative, plan, language = valid_sources()
                language["decision"] = decision
                with self.assertRaises(ValidationError):
                    validate_with_sources(valid_brief(), narrative, plan, language)

    def test_unknown_unresolved_issue_fails(self) -> None:
        narrative, plan, language = valid_sources()
        language["unresolved_issues"].append("LANG-999")
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)

    def test_nonactionable_unresolved_issue_fails(self) -> None:
        narrative, plan, language = valid_sources()
        language["unresolved_issues"].append("LANG-002")
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)

    def test_omitted_minor_unresolved_issue_passes(self) -> None:
        brief = valid_brief()
        brief["omitted_reported_nonblocking_findings"].append(
            {
                "finding_id": "LANG-003",
                "rationale": "The minor item was not selected for repair.",
            }
        )
        narrative, plan, language = valid_sources()
        language["findings"].append({"finding_id": "LANG-003", "severity": "minor"})
        language["unresolved_issues"].append("LANG-003")
        validate_with_sources(brief, narrative, plan, language)

    def test_ready_report_with_unresolved_issue_fails(self) -> None:
        narrative, plan, language = valid_sources()
        language["decision"] = "submission_ready"
        with self.assertRaises(ValidationError):
            validate_with_sources(valid_brief(), narrative, plan, language)


if __name__ == "__main__":
    unittest.main()
