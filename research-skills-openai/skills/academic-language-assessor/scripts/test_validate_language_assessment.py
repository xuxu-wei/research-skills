#!/usr/bin/env python3
"""Unit tests for language-assessment output validation."""

from __future__ import annotations

import copy
import unittest

from validate_language_assessment import ValidationError, validate_report


def valid_report() -> dict:
    return {
        "review_id": "language-r001",
        "reviewer_skill": "academic-language-assessor",
        "reviewer_instance_id": "fresh-language-r001",
        "workflow_id": "workflow-001",
        "round_id": "r001",
        "input_artifact_ids": ["dossier-v001", "reader-handoff-v001"],
        "input_versions": ["v001", "v001"],
        "scope": "complete_idea_dossier",
        "dossier_ref": {
            "artifact_id": "dossier-v001",
            "version": "v001",
            "path": "dossiers/idea-dossier-v001.md",
        },
        "reader_handoff": {
            "artifact_id": "reader-handoff-v001",
            "version": "v001",
            "path": "inputs/reader-handoff.yaml",
        },
        "files_read": [
            "dossiers/idea-dossier-v001.md",
            "inputs/reader-handoff.yaml",
        ],
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "source_edits_performed": False,
        "decision": "submission_ready",
        "coverage_receipt": {
            "reader_entry": {
                "status": "completed",
                "reviewed_count": 4,
                "basis": "All bounded reader-entry units were reviewed.",
            },
            "core_scientific_role": {
                "status": "completed",
                "reviewed_count": 3,
                "basis": "All scientific roles present in the dossier were reviewed.",
            },
            "terminology_concordance": {
                "status": "completed",
                "reviewed_count": 0,
                "basis": "No terminology cluster triggered whole-dossier concordance.",
            },
            "local_language": {
                "status": "completed",
                "reviewed_count": 12,
                "basis": "Every in-scope reader-facing unit was reviewed.",
            },
        },
        "findings": [],
        "unresolved_issues": [],
    }


def finding_identity(
    *,
    level: str = "meso",
    role: str = "primary-outcome",
    locator: str = "title-and-summary",
    failure_mode: str = "ambiguous-core-term",
) -> dict:
    return {
        "finding_level": level,
        "finding_scope": "concept_cluster" if level == "meso" else "occurrence",
        "scientific_role": role,
        "normalized_locator": locator,
        "failure_mode": failure_mode,
        "fingerprint": f"{level}|{role}|{locator}|{failure_mode}",
    }


class LanguageAssessmentValidatorTests(unittest.TestCase):
    def test_ready_report_passes(self) -> None:
        validate_report(valid_report())

    def test_object_decision_fails(self) -> None:
        report = valid_report()
        report["decision"] = {"overall": "minor_language_revision"}
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_major_finding_requires_major_decision(self) -> None:
        report = valid_report()
        report["decision"] = "minor_language_revision"
        report["findings"] = [{"id": "L001", "severity": "major"}]
        report["unresolved_issues"] = ["L001"]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_minor_finding_prevents_ready(self) -> None:
        report = valid_report()
        report["findings"] = [{"id": "L001", "severity": "minor"}]
        report["unresolved_issues"] = ["L001"]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_suggestion_can_remain_ready(self) -> None:
        report = valid_report()
        report["findings"] = [
            {
                "id": "L001",
                "severity": "suggestion",
                "finding_kind": "language",
                **finding_identity(level="micro", role="local-expression", failure_mode="wordy-expression"),
            }
        ]
        validate_report(report)

    def test_completed_idea_requires_all_four_coverage_passes(self) -> None:
        report = valid_report()
        report["coverage_receipt"].pop("local_language")
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_coverage_pass_requires_nonnegative_count_and_basis(self) -> None:
        report = valid_report()
        report["coverage_receipt"]["reader_entry"]["status"] = "pass"
        with self.assertRaises(ValidationError):
            validate_report(report)
        report = valid_report()
        report["coverage_receipt"]["terminology_concordance"]["reviewed_count"] = -1
        with self.assertRaises(ValidationError):
            validate_report(report)
        report = valid_report()
        report["coverage_receipt"]["reader_entry"]["basis"] = ""
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_independent_review_stop_may_omit_coverage_receipt(self) -> None:
        report = valid_report()
        report["decision"] = "independent_review_pending"
        report.pop("coverage_receipt")
        validate_report(report)

    def test_digest_key_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["input_digest"] = "forbidden"
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_sibling_platform_skill_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["files_read"].append(
            "research-skills/research/academic-language-assessor/SKILL.md"
        )
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_duplicate_file_path_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["files_read"].append("dossiers/idea-dossier-v001.md")
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_idea_binding_path_mismatch_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["dossier_ref"]["path"] = "dossiers/idea-dossier-v002.md"
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_prior_idea_dossier_read_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["files_read"].append("dossiers/idea-dossier-v000.md")
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_embedded_reader_handoff_passes_without_fictitious_file(self) -> None:
        report = copy.deepcopy(valid_report())
        report["input_artifact_ids"] = ["dossier-v001"]
        report["input_versions"] = ["v001"]
        report["reader_handoff"] = {
            "artifact_id": "embedded-reader-handoff",
            "version": "embedded",
            "path": None,
        }
        report["files_read"] = ["dossiers/idea-dossier-v001.md"]
        validate_report(report)

    def test_idea_prior_review_read_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["files_read"].append("reviews/preflight-r001.md")
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_blocking_finding_requires_executable_fields(self) -> None:
        report = copy.deepcopy(valid_report())
        report["decision"] = "major_language_revision"
        report["findings"] = [{"finding_id": "L001", "severity": "major"}]
        report["unresolved_issues"] = ["L001"]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_minor_finding_requires_executable_fields(self) -> None:
        report = copy.deepcopy(valid_report())
        report["decision"] = "minor_language_revision"
        report["findings"] = [
            {"finding_id": "L001", "severity": "minor", "finding_kind": "language"}
        ]
        report["unresolved_issues"] = ["L001"]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_executable_blocking_finding_passes(self) -> None:
        report = copy.deepcopy(valid_report())
        report["decision"] = "major_language_revision"
        report["findings"] = [
            {
                "finding_id": "L001",
                "severity": "major",
                "finding_kind": "terminology",
                "category": "terminology",
                "dossier_locator": "Title and summary",
                "current_problem": "The term is ambiguous.",
                "target_state": "The referent is explicit.",
                "required_change_or_replacement": "Use the verified descriptive term.",
                "content_to_preserve": "Claim strength and study object.",
                "acceptance_test": "A target reader identifies the referent at first use.",
                "term_or_phrase": "opaque label",
                "recommended_form_or_plain_description": "direct descriptive term",
                "evidence_basis": "Two independent domain sources and the reader baseline.",
                "first_use_definition": "Directly name the measured object at first use.",
                "competing_forms_and_locators": ["opaque label — Title and summary"],
                **finding_identity(),
            }
        ]
        report["unresolved_issues"] = ["L001"]
        validate_report(report)

    def test_terminology_finding_requires_focused_action(self) -> None:
        report = copy.deepcopy(valid_report())
        report["decision"] = "major_language_revision"
        report["findings"] = [
            {
                "finding_id": "L001",
                "severity": "major",
                "finding_kind": "terminology",
                "category": "terminology",
                "dossier_locator": "Title and summary",
                "current_problem": "The term is ambiguous.",
                "target_state": "The referent is explicit.",
                "required_change_or_replacement": "Use a direct descriptive term.",
                "content_to_preserve": "Claim strength and study object.",
                "acceptance_test": "The referent is clear at first use.",
            }
        ]
        report["unresolved_issues"] = ["L001"]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_acceptable_terminology_candidate_is_not_persisted_as_suggestion(self) -> None:
        report = copy.deepcopy(valid_report())
        report["findings"] = [
            {
                "finding_id": "L001",
                "severity": "suggestion",
                "finding_kind": "terminology",
                "term_or_phrase": "RMSE",
                "recommended_form_or_plain_description": "RMSE",
                "evidence_basis": "Standard and defined at first use.",
                "first_use_definition": "Root mean squared error (RMSE).",
                "competing_forms_and_locators": [],
                **finding_identity(level="micro", role="error-measure"),
            }
        ]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_macro_finding_level_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["findings"] = [
            {
                "finding_id": "L001",
                "severity": "suggestion",
                "finding_kind": "language",
                **finding_identity(level="macro"),
            }
        ]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_fingerprint_must_match_readable_components(self) -> None:
        report = copy.deepcopy(valid_report())
        identity = finding_identity()
        identity["fingerprint"] = "opaque-generated-value"
        report["findings"] = [
            {
                "finding_id": "L001",
                "severity": "suggestion",
                "finding_kind": "language",
                **identity,
            }
        ]
        with self.assertRaises(ValidationError):
            validate_report(report)

    def test_duplicate_fingerprint_fails(self) -> None:
        report = copy.deepcopy(valid_report())
        report["findings"] = [
            {
                "finding_id": finding_id,
                "severity": "suggestion",
                "finding_kind": "language",
                **finding_identity(),
            }
            for finding_id in ("L001", "L002")
        ]
        with self.assertRaises(ValidationError):
            validate_report(report)


if __name__ == "__main__":
    unittest.main()
