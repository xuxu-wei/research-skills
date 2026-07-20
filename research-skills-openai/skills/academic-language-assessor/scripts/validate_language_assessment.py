#!/usr/bin/env python3
"""Validate machine provenance and decision consistency in a language report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


DECISIONS = {
    "submission_ready",
    "minor_language_revision",
    "major_language_revision",
    "needs_professional_editing",
    "independent_review_pending",
    "clarification_required",
}
SEVERITIES = {"critical", "major", "minor", "suggestion"}
ACTIONABLE = {"critical", "major", "minor"}
FINDING_KINDS = {"language", "terminology"}
FINDING_LEVELS = {"meso", "micro"}
FINDING_SCOPES = {"concept_cluster", "occurrence"}
COVERAGE_PASSES = (
    "reader_entry",
    "core_scientific_role",
    "terminology_concordance",
    "local_language",
)
COMPLETED_DECISIONS = {
    "submission_ready",
    "minor_language_revision",
    "major_language_revision",
    "needs_professional_editing",
}
FINGERPRINT_PART_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN_KEY_PARTS = ("sha", "hash", "digest")
FORBIDDEN_FILE_PREFIXES = ("research-skills/",)
IDEA_SCOPE = "complete_idea_dossier"
BLOCKING_ACTION_FIELDS = {
    "dossier_locator",
    "current_problem",
    "target_state",
    "required_change_or_replacement",
    "content_to_preserve",
    "acceptance_test",
}
TERMINOLOGY_ACTION_FIELDS = {
    "term_or_phrase",
    "recommended_form_or_plain_description",
    "evidence_basis",
    "first_use_definition",
}
GENERIC_LOCATORS = {
    "throughout",
    "full dossier",
    "complete dossier",
    "entire dossier",
    "全文",
    "完整 dossier",
    "完整dossier",
}


class ValidationError(ValueError):
    """The report violates its deterministic output contract."""


def load_frontmatter(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---"):
        raise ValidationError("report must start with YAML frontmatter")
    parts = raw.split("---", 2)
    if len(parts) != 3:
        raise ValidationError("report frontmatter is not terminated")
    try:
        payload = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValidationError("frontmatter must be an object")
    return payload


def _check_forbidden_keys(value: Any, location: str = "frontmatter") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if any(part in normalized for part in FORBIDDEN_KEY_PARTS):
                raise ValidationError(f"{location}: forbidden provenance key '{key}'")
            _check_forbidden_keys(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _check_forbidden_keys(child, f"{location}[{index}]")


def _file_path(item: Any) -> str | None:
    if isinstance(item, str) and item.strip():
        return item.strip()
    if isinstance(item, dict) and isinstance(item.get("path"), str) and item["path"].strip():
        return item["path"].strip()
    return None


def _logical_ref(value: Any, label: str) -> tuple[str, str, str]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an artifact reference object")
    result: list[str] = []
    for field in ("artifact_id", "version", "path"):
        item = value.get(field)
        if not isinstance(item, str) or not item.strip():
            raise ValidationError(f"{label}.{field} must be nonempty")
        result.append(item.strip())
    return result[0], result[1], result[2].replace("\\", "/").lstrip("./")


def _reader_handoff(value: Any) -> tuple[str, str, str | None]:
    if not isinstance(value, dict):
        raise ValidationError("reader_handoff must be an object")
    artifact_id = value.get("artifact_id")
    version = value.get("version")
    path = value.get("path")
    if not isinstance(artifact_id, str) or not artifact_id.strip():
        raise ValidationError("reader_handoff.artifact_id must be nonempty")
    if not isinstance(version, str) or not version.strip():
        raise ValidationError("reader_handoff.version must be nonempty")
    if path is not None and (not isinstance(path, str) or not path.strip()):
        raise ValidationError("reader_handoff.path must be null or a nonempty path")
    normalized_path = path.replace("\\", "/").lstrip("./") if path else None
    return artifact_id.strip(), version.strip(), normalized_path


def _nonempty_action_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(item, str) and item.strip() for item in value)
    return False


def _validate_coverage_receipt(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != set(COVERAGE_PASSES):
        raise ValidationError(
            "coverage_receipt must contain exactly the four required completion passes"
        )
    for pass_name in COVERAGE_PASSES:
        receipt = value[pass_name]
        if not isinstance(receipt, dict):
            raise ValidationError(f"coverage_receipt.{pass_name} must be an object")
        if receipt.get("status") != "completed":
            raise ValidationError(
                f"coverage_receipt.{pass_name}.status must be completed"
            )
        count = receipt.get("reviewed_count")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValidationError(
                f"coverage_receipt.{pass_name}.reviewed_count must be a nonnegative integer"
            )
        basis = receipt.get("basis")
        if not isinstance(basis, str) or not basis.strip():
            raise ValidationError(f"coverage_receipt.{pass_name}.basis must be nonempty")


def _validate_finding_identity(finding: dict[str, Any], index: int) -> str:
    level = finding.get("finding_level")
    if level not in FINDING_LEVELS:
        raise ValidationError(f"findings[{index}] must use finding_level meso or micro")
    scope = finding.get("finding_scope")
    if scope is not None and scope not in FINDING_SCOPES:
        raise ValidationError(f"findings[{index}] has an invalid finding_scope")

    components: list[str] = []
    for field in ("scientific_role", "normalized_locator", "failure_mode"):
        value = finding.get(field)
        if not isinstance(value, str) or not FINGERPRINT_PART_RE.fullmatch(value):
            raise ValidationError(
                f"findings[{index}].{field} must be a readable lowercase kebab-case key"
            )
        components.append(value)
    expected = "|".join((level, *components))
    if finding.get("fingerprint") != expected:
        raise ValidationError(
            f"findings[{index}].fingerprint must equal "
            "finding_level|scientific_role|normalized_locator|failure_mode"
        )
    return expected


def validate_report(data: dict[str, Any]) -> None:
    _check_forbidden_keys(data)
    required = {
        "review_id",
        "reviewer_skill",
        "reviewer_instance_id",
        "workflow_id",
        "round_id",
        "input_artifact_ids",
        "input_versions",
        "scope",
        "files_read",
        "isolation_mode",
        "prior_scores_visible",
        "source_edits_performed",
        "decision",
        "findings",
        "unresolved_issues",
    }
    missing = sorted(required - set(data))
    if missing:
        raise ValidationError(f"missing frontmatter fields: {', '.join(missing)}")
    if data["reviewer_skill"] != "academic-language-assessor":
        raise ValidationError("reviewer_skill must be academic-language-assessor")
    if data["isolation_mode"] != "fresh_subagent":
        raise ValidationError("isolation_mode must be fresh_subagent")
    if data["prior_scores_visible"] is not False or data["source_edits_performed"] is not False:
        raise ValidationError("prior scores and source edits must both be false")

    decision = data["decision"]
    if not isinstance(decision, str) or decision not in DECISIONS:
        raise ValidationError("decision must be one allowed scalar enum value")
    ids = data["input_artifact_ids"]
    versions = data["input_versions"]
    if not isinstance(ids, list) or not ids or not isinstance(versions, list) or len(ids) != len(versions):
        raise ValidationError("input artifact IDs and versions must be nonempty parallel lists")
    files = data["files_read"]
    if not isinstance(files, list) or not files or any(_file_path(item) is None for item in files):
        raise ValidationError("files_read must be a nonempty list of paths or path objects")
    file_paths = [_file_path(item).replace("\\", "/").lstrip("./") for item in files]
    if len(file_paths) != len(set(file_paths)):
        raise ValidationError("files_read must not contain duplicate paths")
    if any(path.startswith(FORBIDDEN_FILE_PREFIXES) for path in file_paths):
        raise ValidationError("files_read includes a forbidden sibling-platform path")

    if data["scope"] == IDEA_SCOPE:
        dossier_id, dossier_version, dossier_path = _logical_ref(
            data.get("dossier_ref"), "dossier_ref"
        )
        handoff_id, handoff_version, handoff_path = _reader_handoff(
            data.get("reader_handoff")
        )
        expected_inputs = [(dossier_id, dossier_version)]
        if handoff_path is not None:
            expected_inputs.append((handoff_id, handoff_version))
        if list(zip(ids, versions)) != expected_inputs:
            raise ValidationError(
                "Idea input IDs/versions must bind the current dossier and any file-backed reader handoff"
            )
        if dossier_path not in file_paths or (
            handoff_path is not None and handoff_path not in file_paths
        ):
            raise ValidationError(
                "Idea dossier and file-backed reader handoff paths must occur in files_read"
            )
        dossier_reads = [
            path
            for path in file_paths
            if re.search(r"(?:^|/)idea-dossier-v[^/]+\.md$", path, re.IGNORECASE)
        ]
        if dossier_reads != [dossier_path]:
            raise ValidationError("Idea language review must read exactly one bound dossier version")
        instruction_prefix = "research-skills-openai/skills/academic-language-assessor/"
        for path in file_paths:
            if path.startswith(instruction_prefix) or path in {
                "AGENTS.md",
                "research-skills-openai/AGENTS.md",
                dossier_path,
            }:
                continue
            if handoff_path is not None and path == handoff_path:
                continue
            if path.startswith(("https://", "http://")):
                continue
            raise ValidationError(
                f"Idea language review read an unbound project artifact: {path}"
            )
        if decision in COMPLETED_DECISIONS:
            _validate_coverage_receipt(data.get("coverage_receipt"))

    findings = data["findings"]
    if not isinstance(findings, list):
        raise ValidationError("findings must be a list")
    finding_ids: set[str] = set()
    finding_fingerprints: set[str] = set()
    actionable_ids: set[str] = set()
    severities: set[str] = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"findings[{index}] must be an object")
        finding_id = finding.get("finding_id", finding.get("id"))
        severity = finding.get("severity")
        if not isinstance(finding_id, str) or not finding_id.strip() or finding_id in finding_ids:
            raise ValidationError(f"findings[{index}] has a missing or duplicate ID")
        if severity not in SEVERITIES:
            raise ValidationError(f"findings[{index}] has an invalid severity")
        finding_ids.add(finding_id)
        severities.add(severity)
        if data["scope"] == IDEA_SCOPE:
            fingerprint = _validate_finding_identity(finding, index)
            if fingerprint in finding_fingerprints:
                raise ValidationError(f"findings[{index}] has a duplicate fingerprint")
            finding_fingerprints.add(fingerprint)
        finding_kind = finding.get("finding_kind")
        if data["scope"] == IDEA_SCOPE and finding_kind not in FINDING_KINDS:
            raise ValidationError(
                f"findings[{index}] must classify finding_kind as language or terminology"
            )
        if finding_kind is not None and finding_kind not in FINDING_KINDS:
            raise ValidationError(f"findings[{index}] has an invalid finding_kind")
        if finding_kind == "terminology":
            if severity not in ACTIONABLE:
                raise ValidationError(
                    f"findings[{index}]: persist only actionable terminology findings"
                )
            missing_term_action = sorted(
                field
                for field in TERMINOLOGY_ACTION_FIELDS
                if not _nonempty_action_value(finding.get(field))
            )
            if missing_term_action:
                raise ValidationError(
                    f"findings[{index}] lacks focused terminology action fields: "
                    + ", ".join(missing_term_action)
                )
            competing = finding.get("competing_forms_and_locators")
            if not isinstance(competing, list) or any(
                not isinstance(item, str) or not item.strip() for item in competing
            ):
                raise ValidationError(
                    f"findings[{index}] must provide competing_forms_and_locators as a list"
                )
        if severity in ACTIONABLE:
            actionable_ids.add(finding_id)
        if severity in ACTIONABLE:
            missing_action = sorted(
                field
                for field in BLOCKING_ACTION_FIELDS
                if not _nonempty_action_value(finding.get(field))
            )
            if missing_action:
                raise ValidationError(
                    f"findings[{index}] lacks executable repair fields: "
                    + ", ".join(missing_action)
                )
            locator = finding["dossier_locator"]
            locator_values = [locator] if isinstance(locator, str) else locator
            if all(item.strip().lower() in GENERIC_LOCATORS for item in locator_values):
                raise ValidationError(
                    f"findings[{index}] uses only an unbounded dossier locator"
                )

    unresolved = data["unresolved_issues"]
    if not isinstance(unresolved, list) or any(not isinstance(item, str) for item in unresolved):
        raise ValidationError("unresolved_issues must be a list of finding IDs")
    unresolved_ids = set(unresolved)
    if len(unresolved) != len(unresolved_ids) or not unresolved_ids <= finding_ids:
        raise ValidationError("unresolved_issues contains duplicates or unknown IDs")
    if not actionable_ids <= unresolved_ids:
        raise ValidationError("every actionable finding must be unresolved")

    if "critical" in severities and decision != "needs_professional_editing":
        raise ValidationError("a critical finding requires needs_professional_editing")
    if "major" in severities and decision not in {
        "major_language_revision",
        "needs_professional_editing",
        "clarification_required",
    }:
        raise ValidationError("a major finding requires a major-or-worse decision")
    if decision == "submission_ready" and actionable_ids:
        raise ValidationError("submission_ready cannot contain actionable findings")
    if decision == "minor_language_revision" and severities & {"critical", "major"}:
        raise ValidationError("minor_language_revision cannot contain critical or major findings")
    if decision == "independent_review_pending" and findings:
        raise ValidationError("independent_review_pending cannot contain language findings")
    if decision == "clarification_required" and not actionable_ids:
        raise ValidationError("clarification_required must identify an actionable missing input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        validate_report(load_frontmatter(args.report))
    except (OSError, ValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("PASS: language assessment report is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
