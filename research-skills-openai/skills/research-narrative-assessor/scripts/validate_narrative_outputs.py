#!/usr/bin/env python3
"""Validate generic narrative assessment, repair, and preservation artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


PROFILES = {"idea", "proposal", "perspective", "article"}
NARRATIVE_DECISIONS = {
    "narrative_ready",
    "minor_narrative_revision",
    "major_narrative_revision",
    "clarification_required",
    "independent_review_pending",
}
PRESERVATION_DECISIONS = {
    "scientific_content_preserved",
    "editorial_scope_violation",
    "identity_drift_detected",
    "scientific_change_declared",
}
OPERATIONS = {"replace", "define", "move", "split", "merge", "delete", "reorder", "add_bridge", "consolidate"}
FINDING_CATEGORIES = {
    "reader_reasoning_chain",
    "section_function",
    "progressive_disclosure",
    "core_element_alignment",
    "authority_and_repetition",
    "counterargument_boundary_authority",
    "navigation_and_backtracking",
    "reader_baseline",
}
ACTION_FIELDS = {
    "action_id",
    "addresses_findings",
    "priority",
    "artifact_locator",
    "counterargument_or_boundary_family",
    "operation",
    "current_problem",
    "target_state",
    "required_content_or_function",
    "verified_term_replacement",
    "content_to_preserve",
    "content_to_remove_or_move",
    "destination_if_moved",
    "dependencies",
    "acceptance_test",
}
CATEGORIES = {
    "identity_and_question",
    "object_scope_and_boundaries",
    "inputs_and_resources",
    "design_analysis_and_inference",
    "claims_and_evidence_status",
    "assumptions_limitations_and_counterarguments",
    "unsupported_claim_classes",
    "source_intent_and_binding_constraints",
}
DISPOSITIONS = {
    "retained_same_meaning",
    "retained_same_strength",
    "retained_once_at_authority",
    "retained_at_family_authority",
}


class ValidationError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected YAML mapping")
    reject_hash_fields(value, str(path))
    return value


def load_frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError(f"{path}: missing YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValidationError(f"{path}: unclosed YAML frontmatter") from exc
    value = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: frontmatter must be a mapping")
    reject_hash_fields(value, str(path))
    return value


def reject_hash_fields(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            if "sha256" in normalized or "digest" in normalized:
                raise ValidationError(f"{label}: persisted hash field is forbidden: {key}")
            reject_hash_fields(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_hash_fields(child, f"{label}[{index}]")


def nonempty(value: Any, label: str) -> None:
    if value is None or value == "" or value == [] or value == {}:
        raise ValidationError(f"{label}: must be nonempty")


def artifact_ref(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label}: expected mapping")
    if set(value) != {"artifact_id", "version", "path"}:
        raise ValidationError(f"{label}: expected artifact_id, version, and path")
    for field in ("artifact_id", "version", "path"):
        nonempty(value.get(field), f"{label}.{field}")
    return value


def locator(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValidationError(f"{label}: expected structured locator")
    nonempty(value.get("section_heading"), f"{label}.section_heading")
    if not value.get("subsection_heading") and not value.get("content_anchor"):
        raise ValidationError(f"{label}: needs subsection_heading or content_anchor")


def reviewer_provenance(data: dict[str, Any], label: str) -> None:
    for field in ("review_id", "reviewer_instance_id", "workflow_id", "round_id"):
        nonempty(data.get(field), f"{label}.{field}")
    if data.get("reviewer_skill") != "research-narrative-assessor":
        raise ValidationError(f"{label}.reviewer_skill: invalid")
    if data.get("profile") not in PROFILES:
        raise ValidationError(f"{label}.profile: invalid")
    if data.get("isolation_mode") != "fresh_subagent":
        raise ValidationError(f"{label}.isolation_mode: must be fresh_subagent")
    if data.get("prior_scores_visible") is not False or data.get("source_edits_performed") is not False:
        raise ValidationError(f"{label}: isolation booleans are invalid")
    for field in ("input_artifact_ids", "input_versions", "files_read", "unresolved_issues"):
        if not isinstance(data.get(field), list):
            raise ValidationError(f"{label}.{field}: expected list")


def exact_declared_inputs(data: dict[str, Any], refs: list[dict[str, Any]], label: str) -> None:
    ids = [item["artifact_id"] for item in refs]
    versions = [item["version"] for item in refs]
    paths = [item["path"] for item in refs]
    if data.get("input_artifact_ids") != ids or data.get("input_versions") != versions:
        raise ValidationError(f"{label}: logical input lists do not match declared refs")
    if data.get("files_read") != paths or len(paths) != len(set(paths)):
        raise ValidationError(f"{label}.files_read: must exactly match declared paths in order")


def validate_assessment(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    reviewer_provenance(data, "assessment")
    if data.get("schema_version") != "research-narrative-assessment.v1":
        raise ValidationError("assessment.schema_version: invalid")
    if data.get("decision") not in NARRATIVE_DECISIONS:
        raise ValidationError("assessment.decision: invalid")
    refs = [artifact_ref(data.get("input_artifact"), "assessment.input_artifact")]
    components = data.get("input_component_refs")
    if not isinstance(components, list):
        raise ValidationError("assessment.input_component_refs: expected list")
    refs.extend(artifact_ref(item, f"assessment.input_component_refs[{index}]") for index, item in enumerate(components))
    handoff = data.get("reader_handoff")
    if not isinstance(handoff, dict) or set(handoff) != {"artifact_id", "version", "path"}:
        raise ValidationError("assessment.reader_handoff: invalid")
    nonempty(handoff.get("artifact_id"), "assessment.reader_handoff.artifact_id")
    nonempty(handoff.get("version"), "assessment.reader_handoff.version")
    if handoff.get("path"):
        refs.append(artifact_ref(handoff, "assessment.reader_handoff"))
    exact_declared_inputs(data, refs, "assessment")
    findings = data.get("findings")
    if not isinstance(findings, list):
        raise ValidationError("assessment.findings: expected list")
    by_id: dict[str, dict[str, Any]] = {}
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"assessment.findings[{index}]: expected mapping")
        finding_id = str(finding.get("finding_id", ""))
        nonempty(finding_id, f"assessment.findings[{index}].finding_id")
        if finding_id in by_id:
            raise ValidationError(f"assessment: duplicate finding {finding_id}")
        if finding.get("severity") not in {"minor", "major", "clarification"}:
            raise ValidationError(f"assessment finding {finding_id}: invalid severity")
        if finding.get("category") not in FINDING_CATEGORIES:
            raise ValidationError(f"assessment finding {finding_id}: invalid category")
        locator(finding.get("artifact_locator"), f"assessment finding {finding_id}.artifact_locator")
        for field in ("observed_evidence", "current_reader_effect", "target_function"):
            nonempty(finding.get(field), f"assessment finding {finding_id}.{field}")
        by_id[finding_id] = finding
    if data["decision"] in {"narrative_ready", "independent_review_pending"} and findings:
        raise ValidationError(f"{data['decision']} must not contain findings")
    if data["decision"] == "major_narrative_revision" and not any(item["severity"] == "major" for item in findings):
        raise ValidationError("major_narrative_revision requires a major finding")
    return by_id


def acyclic(actions: dict[str, dict[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(action_id: str) -> None:
        if action_id in visiting:
            raise ValidationError("repair action dependency cycle")
        if action_id in visited:
            return
        visiting.add(action_id)
        for dependency in actions[action_id]["dependencies"]:
            if dependency not in actions:
                raise ValidationError(f"repair action {action_id}: unknown dependency {dependency}")
            visit(dependency)
        visiting.remove(action_id)
        visited.add(action_id)

    for action_id in actions:
        visit(action_id)


def validate_plan(data: dict[str, Any], assessment: dict[str, Any], findings: dict[str, dict[str, Any]]) -> None:
    if data.get("schema_version") != "research-narrative-repair-plan.v1":
        raise ValidationError("plan.schema_version: invalid")
    if data.get("profile") != assessment.get("profile") or data.get("decision") != assessment.get("decision"):
        raise ValidationError("plan: profile or decision does not match assessment")
    if data.get("assessment_id") != assessment.get("assessment_id"):
        raise ValidationError("plan.assessment_id: mismatch")
    if artifact_ref(data.get("source_artifact"), "plan.source_artifact") != assessment.get("input_artifact"):
        raise ValidationError("plan.source_artifact: mismatch")
    actions_value = data.get("actions")
    if not isinstance(actions_value, list):
        raise ValidationError("plan.actions: expected list")
    actions: dict[str, dict[str, Any]] = {}
    covered: set[str] = set()
    for index, action in enumerate(actions_value):
        if not isinstance(action, dict) or set(action) != ACTION_FIELDS:
            raise ValidationError(f"plan.actions[{index}]: fields do not match contract")
        action_id = str(action.get("action_id", ""))
        nonempty(action_id, f"plan.actions[{index}].action_id")
        if action_id in actions:
            raise ValidationError(f"plan: duplicate action {action_id}")
        if action.get("operation") not in OPERATIONS:
            raise ValidationError(f"repair action {action_id}: invalid operation")
        locator(action.get("artifact_locator"), f"repair action {action_id}.artifact_locator")
        for field in ("addresses_findings", "content_to_preserve", "content_to_remove_or_move", "dependencies"):
            if not isinstance(action.get(field), list):
                raise ValidationError(f"repair action {action_id}.{field}: expected list")
        for field in ("addresses_findings", "priority", "current_problem", "target_state", "required_content_or_function", "content_to_preserve", "acceptance_test"):
            nonempty(action.get(field), f"repair action {action_id}.{field}")
        if action["operation"] in {"replace", "move", "merge", "delete", "reorder", "consolidate"} and not action["content_to_remove_or_move"]:
            raise ValidationError(f"repair action {action_id}: operation needs removal/move detail")
        if action["operation"] == "move":
            nonempty(action.get("destination_if_moved"), f"repair action {action_id}.destination_if_moved")
        if assessment["profile"] == "perspective" and action.get("counterargument_or_boundary_family") is None and any(
            findings.get(fid, {}).get("category") == "counterargument_boundary_authority" for fid in action["addresses_findings"]
        ):
            raise ValidationError(f"repair action {action_id}: Perspective boundary family required")
        for finding_id in action["addresses_findings"]:
            if finding_id not in findings:
                raise ValidationError(f"repair action {action_id}: unknown finding {finding_id}")
            covered.add(finding_id)
        actions[action_id] = action
    if data["decision"] in {"narrative_ready", "independent_review_pending"} and actions:
        raise ValidationError(f"{data['decision']} plan must have no actions")
    if data["decision"] not in {"narrative_ready", "clarification_required", "independent_review_pending"} and not actions:
        raise ValidationError("revision decision requires actions")
    if data["decision"] == "clarification_required" and not data.get("clarifications_required"):
        raise ValidationError("clarification_required must name clarifications")
    missing = {key for key, finding in findings.items() if finding["severity"] == "major" and key not in covered}
    if missing:
        raise ValidationError(f"major findings without actions: {sorted(missing)}")
    acyclic(actions)


def validate_register(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if data.get("schema_version") != "research-protected-content-register.v1":
        raise ValidationError("register.schema_version: invalid")
    for field in ("register_id", "register_version"):
        nonempty(data.get(field), f"register.{field}")
    if data.get("profile") not in PROFILES:
        raise ValidationError("register.profile: invalid")
    artifact_ref(data.get("source_artifact"), "register.source_artifact")
    anchors = data.get("identity_anchors")
    if not isinstance(anchors, list) or not anchors:
        raise ValidationError("register.identity_anchors: expected nonempty list")
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            raise ValidationError(f"register.identity_anchors[{index}]: expected mapping")
        for field in ("anchor_id", "kind", "value", "source_locator"):
            nonempty(anchor.get(field), f"register.identity_anchors[{index}].{field}")
    items_value = data.get("protected_items")
    if not isinstance(items_value, list) or not items_value:
        raise ValidationError("register.protected_items: expected nonempty list")
    items: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items_value):
        if not isinstance(item, dict):
            raise ValidationError(f"register.protected_items[{index}]: expected mapping")
        for field in ("protected_id", "category", "source_locator", "protected_content", "required_disposition"):
            nonempty(item.get(field), f"register.protected_items[{index}].{field}")
        item_id = str(item["protected_id"])
        if item_id in items or item["category"] not in CATEGORIES or item["required_disposition"] not in DISPOSITIONS:
            raise ValidationError(f"register.protected_items[{index}]: duplicate or invalid enum")
        if data["profile"] == "perspective" and item["category"] == "assumptions_limitations_and_counterarguments" and not item.get("family_id"):
            raise ValidationError(f"register protected item {item_id}: Perspective family_id required")
        items[item_id] = item
    coverage = data.get("category_coverage")
    if not isinstance(coverage, list) or {entry.get("category") for entry in coverage if isinstance(entry, dict)} != CATEGORIES:
        raise ValidationError("register.category_coverage: must enumerate every category exactly once")
    referenced: set[str] = set()
    for entry in coverage:
        category = entry["category"]
        status = entry.get("source_status")
        ids = entry.get("protected_item_ids")
        if status not in {"source_present", "source_absent"} or not isinstance(ids, list):
            raise ValidationError(f"register coverage {category}: invalid status or IDs")
        if status == "source_present" and (not ids or entry.get("not_applicable_reason")):
            raise ValidationError(f"register coverage {category}: source_present contract")
        if status == "source_absent" and (ids or not entry.get("not_applicable_reason")):
            raise ValidationError(f"register coverage {category}: source_absent contract")
        for item_id in ids:
            if item_id not in items or items[item_id]["category"] != category or item_id in referenced:
                raise ValidationError(f"register coverage {category}: invalid item {item_id}")
            referenced.add(item_id)
    if referenced != set(items):
        raise ValidationError("register.category_coverage: protected-item coverage mismatch")
    if not isinstance(data.get("permitted_editorial_operations"), list) or set(data["permitted_editorial_operations"]) != OPERATIONS:
        raise ValidationError("register.permitted_editorial_operations: invalid")
    if not isinstance(data.get("prohibited_changes"), list) or not data["prohibited_changes"]:
        raise ValidationError("register.prohibited_changes: expected nonempty list")
    return items


def validate_preservation(data: dict[str, Any], register: dict[str, Any], register_path: Path) -> None:
    reviewer_provenance(data, "preservation")
    if data.get("schema_version") != "research-content-preservation-check.v1" or data.get("decision") not in PRESERVATION_DECISIONS:
        raise ValidationError("preservation: invalid schema or decision")
    inputs = data.get("inputs")
    expected_names = {"prior_artifact", "revised_artifact", "protected_content_register", "revision_delta"}
    if not isinstance(inputs, dict) or set(inputs) != expected_names:
        raise ValidationError("preservation.inputs: invalid")
    refs = [artifact_ref(inputs[name], f"preservation.inputs.{name}") for name in ("prior_artifact", "revised_artifact", "protected_content_register", "revision_delta")]
    exact_declared_inputs(data, refs, "preservation")
    if register.get("source_artifact") != inputs["prior_artifact"]:
        raise ValidationError("preservation: register source mismatch")
    register_ref = inputs["protected_content_register"]
    if register_ref["artifact_id"] != register.get("register_id") or register_ref["version"] != register.get("register_version"):
        raise ValidationError("preservation: register identity mismatch")
    if Path(str(register_ref["path"])).resolve() != register_path.resolve():
        raise ValidationError("preservation: register path mismatch")
    items = {str(item["protected_id"]): item for item in register["protected_items"]}
    checks = data.get("protected_item_checks")
    if not isinstance(checks, list):
        raise ValidationError("preservation.protected_item_checks: expected list")
    checked: set[str] = set()
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise ValidationError(f"preservation.protected_item_checks[{index}]: expected mapping")
        for field in ("protected_id", "prior_locator", "revised_locator", "semantic_status", "evidence"):
            nonempty(check.get(field), f"preservation.protected_item_checks[{index}].{field}")
        item_id = str(check["protected_id"])
        if item_id not in items or item_id in checked or check["semantic_status"] not in {"preserved", "changed", "missing", "unclear"}:
            raise ValidationError(f"preservation check {index}: invalid item or status")
        checked.add(item_id)
    if checked != set(items):
        raise ValidationError("preservation: protected-item coverage mismatch")
    if data["decision"] == "scientific_content_preserved" and (
        any(check["semantic_status"] != "preserved" for check in checks) or data.get("undeclared_scientific_changes")
    ):
        raise ValidationError("scientific_content_preserved requires all items preserved and no undeclared change")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assessment", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--register", type=Path)
    parser.add_argument("--preservation", type=Path)
    args = parser.parse_args()
    if args.assessment or args.plan:
        if not args.assessment or not args.plan or args.register or args.preservation:
            parser.error("assessment mode requires exactly --assessment and --plan")
        assessment = load_frontmatter(args.assessment)
        findings = validate_assessment(assessment)
        validate_plan(load_yaml(args.plan), assessment, findings)
        print("PASS: narrative assessment and YAML repair plan are valid")
        return 0
    if args.preservation:
        if not args.register:
            parser.error("--preservation requires --register")
        register = load_yaml(args.register)
        validate_register(register)
        validate_preservation(load_frontmatter(args.preservation), register, args.register)
        print("PASS: content preservation covers the frozen register")
        return 0
    if args.register:
        validate_register(load_yaml(args.register))
        print("PASS: protected-content register is valid")
        return 0
    parser.error("provide --assessment/--plan, --register, or --preservation/--register")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
