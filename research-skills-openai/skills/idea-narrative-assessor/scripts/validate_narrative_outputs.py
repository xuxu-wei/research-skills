#!/usr/bin/env python3
"""Validate Idea narrative assessment, repair plan, and preservation outputs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


NARRATIVE_DECISIONS = {
    "narrative_ready",
    "minor_narrative_revision",
    "major_narrative_revision",
    "clarification_required",
}
PRESERVATION_DECISIONS = {
    "scientific_content_preserved",
    "editorial_scope_violation",
    "identity_drift_detected",
    "scientific_change_declared",
}
OPERATIONS = {
    "replace",
    "define",
    "move",
    "split",
    "merge",
    "delete",
    "reorder",
    "add_bridge",
    "consolidate",
}
REMOVAL_DETAIL_OPERATIONS = {
    "replace",
    "move",
    "merge",
    "delete",
    "reorder",
    "consolidate",
}
ACTION_FIELDS = {
    "action_id",
    "addresses_findings",
    "priority",
    "dossier_locator",
    "operation",
    "current_problem",
    "target_state",
    "required_content_or_function",
    "content_to_preserve",
    "content_to_remove_or_move",
    "destination_if_moved",
    "dependencies",
    "acceptance_test",
}
PROTECTED_CATEGORY_GROUPS = (
    {"identity_and_question"},
    {"object_scope_and_boundaries"},
    {"inputs_and_resources"},
    {"design_analysis_and_validation", "design_analysis_and_inference"},
    {"claims_and_evidence_status"},
    {"assumptions_limitations_and_contingencies", "assumptions_and_limitations"},
    {"unsupported_claim_classes"},
)
PROTECTED_CATEGORIES = set().union(*PROTECTED_CATEGORY_GROUPS)
PROTECTED_CATEGORY_CANONICAL = (
    "identity_and_question",
    "object_scope_and_boundaries",
    "inputs_and_resources",
    "design_analysis_and_inference",
    "claims_and_evidence_status",
    "assumptions_and_limitations",
    "unsupported_claim_classes",
)
PROTECTED_CATEGORY_ALIASES = {
    alias: canonical
    for canonical, aliases in zip(PROTECTED_CATEGORY_CANONICAL, PROTECTED_CATEGORY_GROUPS)
    for alias in aliases
}
REQUIRED_SOURCE_PRESENT_CATEGORIES = set(PROTECTED_CATEGORY_CANONICAL[:5])
IDENTITY_ANCHOR_FIELDS = {
    "primary_research_question",
    "primary_objective",
    "study_object",
    "core_data_or_evidence_base",
    "primary_unit_of_inference",
}
REGISTER_SCHEMA_V1 = "research-idea-protected-content-register.v1"
REGISTER_SCHEMA_V2 = "research-idea-protected-content-register.v2"


class ValidationError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: expected a YAML mapping")
    return data


def load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError(f"{path}: missing YAML frontmatter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValidationError(f"{path}: unclosed YAML frontmatter") from exc
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: frontmatter must be a mapping")
    return data


def require_nonempty(value: Any, label: str) -> None:
    if value is None or value == "" or value == [] or value == {}:
        raise ValidationError(f"{label}: must be nonempty")


def validate_artifact_ref(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValidationError(f"{label}: expected mapping")
    for field in ("artifact_id", "version", "path"):
        require_nonempty(value.get(field), f"{label}.{field}")


def validate_input_identity_lists(
    data: dict[str, Any],
    refs: list[dict[str, Any]],
    label: str,
) -> None:
    expected_ids = [ref["artifact_id"] for ref in refs]
    expected_versions = [ref["version"] for ref in refs]
    if data.get("input_artifact_ids") != expected_ids:
        raise ValidationError(f"{label}.input_artifact_ids: must match declared logical inputs")
    if data.get("input_versions") != expected_versions:
        raise ValidationError(f"{label}.input_versions: must match declared logical inputs")


def validate_locator(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValidationError(f"{label}: must be a structured locator, not a line number")
    require_nonempty(value.get("section_heading"), f"{label}.section_heading")
    if not (value.get("content_anchor") or value.get("subsection_heading")):
        raise ValidationError(f"{label}: needs a subsection or recognizable content anchor")


def validate_reviewer_provenance(data: dict[str, Any], label: str) -> None:
    for field in ("review_id", "reviewer_instance_id", "workflow_id", "round_id"):
        require_nonempty(data.get(field), f"{label}.{field}")
    if data.get("reviewer_skill") != "idea-narrative-assessor":
        raise ValidationError(f"{label}.reviewer_skill: invalid value")
    for field in ("input_artifact_ids", "input_versions"):
        if not isinstance(data.get(field), list) or not data[field]:
            raise ValidationError(f"{label}.{field}: expected nonempty list")
    if data.get("isolation_mode") != "fresh_subagent":
        raise ValidationError(f"{label}.isolation_mode: must be fresh_subagent")
    if data.get("prior_scores_visible") is not False:
        raise ValidationError(f"{label}.prior_scores_visible: must be false")
    if data.get("source_edits_performed") is not False:
        raise ValidationError(f"{label}.source_edits_performed: must be false")
    if not isinstance(data.get("unresolved_issues"), list):
        raise ValidationError(f"{label}.unresolved_issues: expected list")


def validate_assessment(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    validate_reviewer_provenance(data, "assessment")
    if data.get("decision") not in NARRATIVE_DECISIONS:
        raise ValidationError("assessment.decision: invalid value")
    validate_artifact_ref(data.get("input_dossier"), "assessment.input_dossier")
    if data.get("forbidden_project_artifacts_read") is not False:
        raise ValidationError("assessment: forbidden project artifacts must not be read")
    files_read = data.get("files_read")
    if not isinstance(files_read, list) or not files_read:
        raise ValidationError("assessment.files_read: expected nonempty list")
    allowed_paths = {data["input_dossier"]["path"]}
    reader_handoff = data.get("reader_handoff")
    if not isinstance(reader_handoff, dict):
        raise ValidationError("assessment.reader_handoff: expected mapping")
    for field in ("artifact_id", "version"):
        require_nonempty(reader_handoff.get(field), f"assessment.reader_handoff.{field}")
    declared_refs = [data["input_dossier"]]
    if reader_handoff.get("path"):
        allowed_paths.add(reader_handoff["path"])
        declared_refs.append(reader_handoff)
    validate_input_identity_lists(data, declared_refs, "assessment")
    if data["input_dossier"]["path"] not in files_read:
        raise ValidationError("assessment.files_read: current dossier is missing")
    if len(files_read) != len(set(files_read)) or set(files_read) != allowed_paths:
        raise ValidationError("assessment.files_read: must contain exactly the declared file inputs")
    findings = data.get("findings")
    if not isinstance(findings, list):
        raise ValidationError("assessment.findings: expected list")
    by_id: dict[str, dict[str, Any]] = {}
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"assessment.findings[{index}]: expected mapping")
        finding_id = finding.get("finding_id")
        require_nonempty(finding_id, f"assessment.findings[{index}].finding_id")
        if finding_id in by_id:
            raise ValidationError(f"assessment: duplicate finding ID {finding_id}")
        if finding.get("severity") not in {"minor", "major", "clarification"}:
            raise ValidationError(f"assessment finding {finding_id}: invalid severity")
        validate_locator(finding.get("dossier_locator"), f"assessment finding {finding_id}.dossier_locator")
        for field in ("category", "observed_evidence", "current_reader_effect", "target_function"):
            require_nonempty(finding.get(field), f"assessment finding {finding_id}.{field}")
        by_id[str(finding_id)] = finding
    if data["decision"] == "narrative_ready" and findings:
        raise ValidationError("narrative_ready assessment must have no findings")
    if data["decision"] == "major_narrative_revision" and not any(
        finding.get("severity") == "major" for finding in findings
    ):
        raise ValidationError("major_narrative_revision requires a major finding")
    return by_id


def ensure_acyclic(actions: dict[str, dict[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(action_id: str) -> None:
        if action_id in visiting:
            raise ValidationError("repair plan action dependencies contain a cycle")
        if action_id in visited:
            return
        visiting.add(action_id)
        for dependency in actions[action_id].get("dependencies", []):
            if dependency not in actions:
                raise ValidationError(f"repair action {action_id}: unknown dependency {dependency}")
            visit(dependency)
        visiting.remove(action_id)
        visited.add(action_id)

    for action_id in actions:
        visit(action_id)


def validate_plan(data: dict[str, Any], findings: dict[str, dict[str, Any]]) -> None:
    if data.get("decision") not in NARRATIVE_DECISIONS:
        raise ValidationError("plan.decision: invalid value")
    validate_artifact_ref(data.get("source_artifact"), "plan.source_artifact")
    actions_value = data.get("actions")
    if not isinstance(actions_value, list):
        raise ValidationError("plan.actions: expected list")
    actions: dict[str, dict[str, Any]] = {}
    covered: set[str] = set()
    for index, action in enumerate(actions_value):
        if not isinstance(action, dict):
            raise ValidationError(f"plan.actions[{index}]: expected mapping")
        missing = ACTION_FIELDS - set(action)
        if missing:
            raise ValidationError(f"plan.actions[{index}]: missing {sorted(missing)}")
        extra = set(action) - ACTION_FIELDS
        if extra:
            raise ValidationError(f"plan.actions[{index}]: unknown fields {sorted(extra)}")
        action_id = action.get("action_id")
        require_nonempty(action_id, f"plan.actions[{index}].action_id")
        if action_id in actions:
            raise ValidationError(f"plan: duplicate action ID {action_id}")
        if action.get("operation") not in OPERATIONS:
            raise ValidationError(f"repair action {action_id}: invalid operation")
        validate_locator(action.get("dossier_locator"), f"repair action {action_id}.dossier_locator")
        for field in (
            "addresses_findings",
            "priority",
            "current_problem",
            "target_state",
            "required_content_or_function",
            "content_to_preserve",
            "acceptance_test",
        ):
            require_nonempty(action.get(field), f"repair action {action_id}.{field}")
        for field in ("addresses_findings", "content_to_preserve"):
            if not isinstance(action.get(field), list):
                raise ValidationError(f"repair action {action_id}.{field}: expected list")
        if not isinstance(action.get("content_to_remove_or_move"), list):
            raise ValidationError(f"repair action {action_id}.content_to_remove_or_move: expected list")
        if action["operation"] in REMOVAL_DETAIL_OPERATIONS and not action["content_to_remove_or_move"]:
            raise ValidationError(
                f"repair action {action_id}.content_to_remove_or_move: "
                f"{action['operation']} requires specific content to remove, move, or replace"
            )
        if not isinstance(action.get("dependencies"), list):
            raise ValidationError(f"repair action {action_id}.dependencies: expected list")
        if action["operation"] == "move":
            require_nonempty(action.get("destination_if_moved"), f"repair action {action_id}.destination_if_moved")
        for finding_id in action["addresses_findings"]:
            if finding_id not in findings:
                raise ValidationError(f"repair action {action_id}: unknown finding {finding_id}")
            covered.add(finding_id)
        actions[str(action_id)] = action
    if data["decision"] == "narrative_ready" and actions:
        raise ValidationError("narrative_ready plan must have no actions")
    if data["decision"] not in {"narrative_ready", "clarification_required"} and not actions:
        raise ValidationError("revision decision requires at least one repair action")
    if data["decision"] == "clarification_required" and not data.get("clarifications_required"):
        raise ValidationError("clarification_required plan must name required clarifications")
    uncovered = {
        finding_id
        for finding_id, finding in findings.items()
        if finding.get("severity") == "major" and finding_id not in covered
    }
    if uncovered:
        raise ValidationError(f"major findings without repair actions: {sorted(uncovered)}")
    ensure_acyclic(actions)


def _validate_protected_items(data: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], set[str]]:
    validate_artifact_ref(data.get("source_artifact"), "register.source_artifact")
    items = data.get("protected_items")
    if not isinstance(items, list) or not items:
        raise ValidationError("register.protected_items: expected nonempty list")
    items_by_id: dict[str, dict[str, Any]] = {}
    categories: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"register.protected_items[{index}]: expected mapping")
        for field in ("protected_id", "category", "source_locator", "protected_content", "required_revised_disposition"):
            require_nonempty(item.get(field), f"register.protected_items[{index}].{field}")
        if item.get("source_context_locator") is not None:
            require_nonempty(
                item.get("source_context_locator"),
                f"register.protected_items[{index}].source_context_locator",
            )
        identifier = str(item["protected_id"])
        if identifier in items_by_id:
            raise ValidationError(f"register: duplicate protected ID {identifier}")
        items_by_id[identifier] = item
        categories.add(str(item["category"]))
    unknown = categories - PROTECTED_CATEGORIES
    if unknown:
        raise ValidationError(f"register: unknown protected categories {sorted(unknown)}")
    return items_by_id, categories


def _validate_v2_register_coverage(
    data: dict[str, Any],
    items_by_id: dict[str, dict[str, Any]],
) -> None:
    identity_anchor = data.get("identity_anchor")
    if not isinstance(identity_anchor, dict) or set(identity_anchor) != IDENTITY_ANCHOR_FIELDS:
        raise ValidationError(
            "register.identity_anchor: must contain exactly the five dossier identity fields"
        )
    for field in sorted(IDENTITY_ANCHOR_FIELDS):
        require_nonempty(identity_anchor.get(field), f"register.identity_anchor.{field}")

    coverage = data.get("category_coverage")
    if not isinstance(coverage, list):
        raise ValidationError("register.category_coverage: expected list")
    coverage_by_category: dict[str, dict[str, Any]] = {}
    referenced_ids: set[str] = set()
    for index, entry in enumerate(coverage):
        if not isinstance(entry, dict):
            raise ValidationError(f"register.category_coverage[{index}]: expected mapping")
        category = entry.get("category")
        if category not in PROTECTED_CATEGORY_CANONICAL:
            raise ValidationError(
                f"register.category_coverage[{index}].category: invalid canonical category"
            )
        if category in coverage_by_category:
            raise ValidationError(f"register.category_coverage: duplicate category {category}")
        source_status = entry.get("source_status")
        if source_status not in {"source_present", "source_absent"}:
            raise ValidationError(
                f"register.category_coverage[{index}].source_status: invalid value"
            )
        protected_ids = entry.get("protected_item_ids")
        if not isinstance(protected_ids, list) or any(
            not isinstance(item_id, str) or not item_id.strip() for item_id in protected_ids
        ):
            raise ValidationError(
                f"register.category_coverage[{index}].protected_item_ids: expected a string list"
            )
        if len(protected_ids) != len(set(protected_ids)):
            raise ValidationError(
                f"register.category_coverage[{index}].protected_item_ids: duplicate ID"
            )
        reason = entry.get("not_applicable_reason")
        if source_status == "source_present":
            if not protected_ids:
                raise ValidationError(
                    f"register.category_coverage[{index}]: source_present requires protected items"
                )
            if reason is not None and reason != "":
                raise ValidationError(
                    f"register.category_coverage[{index}]: source_present cannot have a not-applicable reason"
                )
        else:
            if category in REQUIRED_SOURCE_PRESENT_CATEGORIES:
                raise ValidationError(
                    f"register.category_coverage[{index}]: {category} must be source_present"
                )
            if protected_ids:
                raise ValidationError(
                    f"register.category_coverage[{index}]: source_absent cannot reference protected items"
                )
            require_nonempty(
                reason,
                f"register.category_coverage[{index}].not_applicable_reason",
            )
        for protected_id in protected_ids:
            if protected_id not in items_by_id:
                raise ValidationError(
                    f"register.category_coverage[{index}]: unknown protected ID {protected_id}"
                )
            item_category = PROTECTED_CATEGORY_ALIASES[str(items_by_id[protected_id]["category"])]
            if item_category != category:
                raise ValidationError(
                    f"register.category_coverage[{index}]: protected ID {protected_id} has category {item_category}"
                )
            if protected_id in referenced_ids:
                raise ValidationError(
                    f"register.category_coverage: protected ID {protected_id} is referenced more than once"
                )
            referenced_ids.add(protected_id)
        coverage_by_category[str(category)] = entry

    if set(coverage_by_category) != set(PROTECTED_CATEGORY_CANONICAL):
        missing = sorted(set(PROTECTED_CATEGORY_CANONICAL) - set(coverage_by_category))
        extra = sorted(set(coverage_by_category) - set(PROTECTED_CATEGORY_CANONICAL))
        raise ValidationError(
            f"register.category_coverage: category mismatch; missing={missing}, extra={extra}"
        )
    if referenced_ids != set(items_by_id):
        missing = sorted(set(items_by_id) - referenced_ids)
        raise ValidationError(
            f"register.category_coverage: source-present protected items are not covered: {missing}"
        )


def validate_register(data: dict[str, Any]) -> None:
    items_by_id, categories = _validate_protected_items(data)
    schema_version = data.get("schema_version")
    if schema_version == REGISTER_SCHEMA_V2:
        require_nonempty(data.get("register_version"), "register.register_version")
        _validate_v2_register_coverage(data, items_by_id)
    elif schema_version == REGISTER_SCHEMA_V1:
        # Historical v1 registers represented category coverage by requiring one
        # protected item in every category. Keep them valid as immutable lineage.
        missing_groups = [sorted(group) for group in PROTECTED_CATEGORY_GROUPS if not group & categories]
        if missing_groups:
            raise ValidationError(
                f"register: missing protected category groups {missing_groups}"
            )
    else:
        raise ValidationError("register.schema_version: unsupported value")
    operations = data.get("permitted_editorial_operations")
    if not isinstance(operations, list) or not OPERATIONS.issubset(set(operations)):
        raise ValidationError("register: permitted editorial operations are incomplete")
    prohibited = data.get("prohibited_changes")
    if not isinstance(prohibited, list) or not prohibited:
        raise ValidationError("register.prohibited_changes: expected nonempty list")


def validate_preservation(
    data: dict[str, Any],
    register: dict[str, Any],
    register_path: Path,
) -> None:
    validate_reviewer_provenance(data, "preservation")
    if data.get("decision") not in PRESERVATION_DECISIONS:
        raise ValidationError("preservation.decision: invalid value")
    if not isinstance(data.get("findings"), list):
        raise ValidationError("preservation.findings: expected list")
    inputs = data.get("inputs")
    if not isinstance(inputs, dict):
        raise ValidationError("preservation.inputs: expected mapping")
    for name in ("prior_dossier", "revised_dossier", "protected_content_register", "revision_delta"):
        validate_artifact_ref(inputs.get(name), f"preservation.inputs.{name}")
    unknown_inputs = set(inputs) - {
        "prior_dossier",
        "revised_dossier",
        "protected_content_register",
        "revision_delta",
    }
    if unknown_inputs:
        raise ValidationError(f"preservation.inputs: unknown inputs {sorted(unknown_inputs)}")
    declared_refs = [
        inputs["prior_dossier"],
        inputs["revised_dossier"],
        inputs["protected_content_register"],
        inputs["revision_delta"],
    ]
    validate_input_identity_lists(data, declared_refs, "preservation")
    register_ref = inputs["protected_content_register"]
    if register_ref["artifact_id"] != register.get("register_id"):
        raise ValidationError("preservation.inputs.protected_content_register: register ID mismatch")
    if Path(str(register_ref["path"])).resolve() != register_path.resolve():
        raise ValidationError("preservation.inputs.protected_content_register: register path mismatch")
    if register.get("source_artifact") != inputs["prior_dossier"]:
        raise ValidationError("preservation: register source does not match the prior dossier")
    allowed_paths = {
        value["path"] for value in inputs.values() if isinstance(value, dict) and value.get("path")
    }
    files_read = data.get("files_read")
    if not isinstance(files_read, list) or set(files_read) != allowed_paths or len(files_read) != len(set(files_read)):
        raise ValidationError("preservation.files_read: must contain exactly the declared input paths")
    checks = data.get("protected_item_checks")
    if not isinstance(checks, list) or not checks:
        raise ValidationError("preservation.protected_item_checks: expected nonempty list")
    expected_ids = {str(item["protected_id"]) for item in register["protected_items"]}
    checked_ids: set[str] = set()
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise ValidationError(f"preservation.protected_item_checks[{index}]: expected mapping")
        for field in ("protected_id", "prior_locator", "revised_locator", "semantic_status", "evidence"):
            require_nonempty(check.get(field), f"preservation check {index}.{field}")
        protected_id = str(check["protected_id"])
        if protected_id in checked_ids:
            raise ValidationError(f"preservation: duplicate protected ID {protected_id}")
        checked_ids.add(protected_id)
        if check.get("semantic_status") not in {"preserved", "changed", "missing", "unclear"}:
            raise ValidationError(f"preservation check {index}.semantic_status: invalid value")
    if checked_ids != expected_ids:
        missing = sorted(expected_ids - checked_ids)
        unknown = sorted(checked_ids - expected_ids)
        raise ValidationError(
            f"preservation: protected ID coverage mismatch; missing={missing}, unknown={unknown}"
        )
    if data["decision"] == "scientific_content_preserved":
        if any(check.get("semantic_status") != "preserved" for check in checks):
            raise ValidationError("scientific_content_preserved requires every item to be preserved")
        if data.get("undeclared_scientific_changes"):
            raise ValidationError("scientific_content_preserved cannot include undeclared scientific changes")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assessment", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--preservation", type=Path)
    parser.add_argument("--register", type=Path)
    args = parser.parse_args()

    if args.preservation:
        if args.assessment or args.plan:
            parser.error("--preservation cannot be combined with --assessment/--plan")
        if not args.register:
            parser.error("--preservation requires --register")
        register = load_yaml(args.register)
        validate_register(register)
        validate_preservation(load_frontmatter(args.preservation), register, args.register)
        print("PASS: content-preservation output is valid and covers the frozen register")
        return 0
    if args.register:
        if args.assessment or args.plan:
            parser.error("--register cannot be combined with --assessment/--plan")
        validate_register(load_yaml(args.register))
        print("PASS: protected-content register is valid")
        return 0
    if not args.assessment or not args.plan:
        parser.error("provide --assessment and --plan, or provide --preservation with --register")
    assessment = load_frontmatter(args.assessment)
    findings = validate_assessment(assessment)
    plan = load_yaml(args.plan)
    if plan.get("decision") != assessment.get("decision"):
        raise ValidationError("assessment and plan decisions do not match")
    if plan.get("assessment_id") != assessment.get("assessment_id"):
        raise ValidationError("assessment and plan IDs do not match")
    if plan.get("source_artifact") != assessment.get("input_dossier"):
        raise ValidationError("assessment and plan source artifacts do not match")
    validate_plan(plan, findings)
    print("PASS: narrative assessment and repair plan are valid")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
