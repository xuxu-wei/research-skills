#!/usr/bin/env python3
"""Validate an editorial-repair writer brief and optional source-review coverage."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import yaml


SCHEMA_VERSION = "research-idea-editorial-repair-writer-brief.v1"
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
ACTION_FIELDS = {
    "repair_item_id",
    "source_item_ids",
    "addresses_finding_ids",
    "locator",
    "operation",
    "problem",
    "target",
    "required_function_or_term",
    "content_to_preserve",
    "delete_move_disposition",
    "destination",
    "dependencies",
    "acceptance_test",
}
SOURCE_BINDING_KEYS = {
    "narrative_assessment",
    "narrative_repair_plan",
    "language_assessment",
}
BLOCKING_SEVERITIES = {"critical", "major"}
NONBLOCKING_SEVERITIES = {"minor", "suggestion"}
SOURCE_SEVERITIES = BLOCKING_SEVERITIES | NONBLOCKING_SEVERITIES | {"clarification"}
ACTIONABLE_SEVERITIES = {"critical", "major", "minor"}
NARRATIVE_ORDINARY_DECISIONS = {
    "narrative_ready",
    "minor_narrative_revision",
    "major_narrative_revision",
}
LANGUAGE_ORDINARY_DECISIONS = {
    "submission_ready",
    "minor_language_revision",
    "major_language_revision",
}
LANGUAGE_NON_ORDINARY_DECISIONS = {
    "clarification_required",
    "independent_review_pending",
    "needs_professional_editing",
}
FORBIDDEN_KEY_PARTS = ("hash", "digest", "checksum")
CRYPTOGRAPHIC_KEY_PATTERN = re.compile(
    r"(?:^|_)(?:sha(?:1|224|256|384|512)?|md5)(?:$|_)"
)
FORBIDDEN_ALLOWED_READ_MARKERS = (
    "assessment",
    "repair-plan",
    "repair_plan",
    "preflight",
    "evaluation",
    "revision-delta",
    "revision_delta",
)
REQUIRED_FORBIDDEN_READ_CATEGORIES = {
    "assessment": re.compile(r"assessment|narrative[^\n]*report|language[^\n]*report"),
    "plan": re.compile(r"\bplan\b|计划"),
    "delta": re.compile(r"\bdelta\b|修订差异"),
    "preflight": re.compile(r"\bpreflight\b|方法学预检"),
    "evaluation": re.compile(r"\bevaluation\b|评估报告"),
}


class ValidationError(ValueError):
    """Raised when a writer brief violates its deterministic contract."""


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label}: expected mapping")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{label}: expected list")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label}: expected nonempty string")
    return value


def _strings(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    items = _list(value, label)
    if not allow_empty and not items:
        raise ValidationError(f"{label}: must be nonempty")
    for index, item in enumerate(items):
        _text(item, f"{label}[{index}]")
    if len(items) != len(set(items)):
        raise ValidationError(f"{label}: duplicate values are forbidden")
    return items


def _relative_path(value: Any, label: str) -> str:
    path = _text(value, label)
    if path != path.strip() or "\\" in path:
        raise ValidationError(f"{label}: use a normalized path with '/' separators")
    if path.startswith("/") or re.match(r"^[A-Za-z]:", path) or "://" in path:
        raise ValidationError(f"{label}: must be a repository-relative path")
    if any(part in {"", ".", ".."} for part in path.split("/")):
        raise ValidationError(f"{label}: empty, '.' and '..' path parts are forbidden")
    if PurePosixPath(path).as_posix() != path:
        raise ValidationError(f"{label}: path is not normalized")
    return path


def _repository_path(path_value: str | Path, label: str) -> str:
    path = Path(path_value)
    if path.is_absolute():
        try:
            value = path.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except ValueError as exc:
            raise ValidationError(f"{label}: file must be inside the current repository") from exc
    else:
        value = path.as_posix()
        while value.startswith("./"):
            value = value[2:]
    return _relative_path(value, label)


def _walk_keys(value: Any, trail: str = "brief") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_trail = f"{trail}.{key}"
            yield str(key), child_trail
            yield from _walk_keys(child, child_trail)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_keys(child, f"{trail}[{index}]")


def _reject_integrity_hash_keys(data: dict[str, Any]) -> None:
    for key, trail in _walk_keys(data):
        normalized = key.casefold().replace("-", "_")
        if any(part in normalized for part in FORBIDDEN_KEY_PARTS) or (
            CRYPTOGRAPHIC_KEY_PATTERN.search(normalized)
        ):
            raise ValidationError(f"{trail}: hash/digest/checksum keys are forbidden")


def _artifact_ref(value: Any, label: str, id_field: str) -> dict[str, str]:
    ref = _mapping(value, label)
    return {
        id_field: _text(ref.get(id_field), f"{label}.{id_field}"),
        "version": _text(ref.get("version"), f"{label}.version"),
        "path": _relative_path(ref.get("path"), f"{label}.path"),
    }


def _source_review_binding(data: dict[str, Any]) -> dict[str, dict[str, str]]:
    binding = _mapping(data.get("source_review_binding"), "source_review_binding")
    if set(binding) != SOURCE_BINDING_KEYS:
        raise ValidationError(
            "source_review_binding: must contain exactly narrative_assessment, "
            "narrative_repair_plan, and language_assessment"
        )
    return {
        key: _artifact_ref(binding[key], f"source_review_binding.{key}", "artifact_id")
        for key in sorted(SOURCE_BINDING_KEYS)
    }


def _omission_ids(data: dict[str, Any]) -> tuple[set[str], set[str]]:
    omissions = _list(
        data.get("omitted_reported_nonblocking_findings"),
        "omitted_reported_nonblocking_findings",
    )
    rationales: dict[str, str] = {}
    omitted_ids: list[str] = []
    for index, item in enumerate(omissions):
        label = f"omitted_reported_nonblocking_findings[{index}]"
        if isinstance(item, str):
            finding_id = _text(item, label)
        elif isinstance(item, dict):
            finding_id = _text(item.get("finding_id"), f"{label}.finding_id")
            rationales[finding_id] = _text(item.get("rationale"), f"{label}.rationale")
        else:
            raise ValidationError(f"{label}: expected source finding ID or mapping")
        omitted_ids.append(finding_id)
    if len(omitted_ids) != len(set(omitted_ids)):
        raise ValidationError("omitted_reported_nonblocking_findings: duplicate IDs")

    rationale_fields = [
        field
        for field in ("omitted_nonblocking_finding_rationale", "omitted_finding_rationale")
        if field in data
    ]
    if len(rationale_fields) > 1:
        raise ValidationError("omitted findings: use only one omission-rationale mapping")
    separate = _mapping(
        data.get(rationale_fields[0], {}) if rationale_fields else {},
        rationale_fields[0] if rationale_fields else "omission rationale",
    )
    for finding_id, rationale in separate.items():
        finding_id = _text(finding_id, "omission rationale key")
        _text(rationale, f"omission rationale.{finding_id}")
        if finding_id in rationales:
            raise ValidationError(f"omission rationale.{finding_id}: declared twice")
        rationales[finding_id] = rationale
    if set(rationales) != set(omitted_ids):
        raise ValidationError("omitted findings: IDs and rationales must match exactly")

    included_rationale = _mapping(
        data.get("included_nonblocking_finding_rationale", {}),
        "included_nonblocking_finding_rationale",
    )
    for finding_id, rationale in included_rationale.items():
        finding_id = _text(finding_id, "included_nonblocking_finding_rationale key")
        _text(rationale, f"included_nonblocking_finding_rationale.{finding_id}")
    if set(included_rationale).intersection(omitted_ids):
        raise ValidationError("nonblocking source findings cannot be both included and omitted")
    return set(omitted_ids), set(included_rationale)


def _actions(
    data: dict[str, Any], included_ids: set[str]
) -> dict[str, dict[str, Any]]:
    actions_value = _list(data.get("normalized_repair_actions"), "normalized_repair_actions")
    actions: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(actions_value):
        label = f"normalized_repair_actions[{index}]"
        action = _mapping(value, label)
        if "finding_id" in action or "source_ids" in action:
            raise ValidationError(
                f"{label}: legacy finding_id/source_ids keys are forbidden; use repair-item keys"
            )
        missing = sorted(ACTION_FIELDS - set(action))
        if missing:
            raise ValidationError(f"{label}: missing fields: {', '.join(missing)}")
        repair_item_id = _text(action.get("repair_item_id"), f"{label}.repair_item_id")
        if repair_item_id in actions:
            raise ValidationError(f"normalized_repair_actions: duplicate {repair_item_id}")
        source_item_ids = _strings(action.get("source_item_ids"), f"{label}.source_item_ids")
        if source_item_ids[0] != repair_item_id:
            raise ValidationError(
                f"{label}.source_item_ids: source repair item ID must be first"
            )
        _strings(action.get("addresses_finding_ids"), f"{label}.addresses_finding_ids")
        _text(action.get("locator"), f"{label}.locator")
        operation = _text(action.get("operation"), f"{label}.operation")
        if operation not in OPERATIONS:
            raise ValidationError(f"{label}.operation: invalid value {operation!r}")
        for field in (
            "problem",
            "target",
            "required_function_or_term",
            "delete_move_disposition",
            "acceptance_test",
        ):
            _text(action.get(field), f"{label}.{field}")
        preserved = _mapping(action.get("content_to_preserve"), f"{label}.content_to_preserve")
        _strings(
            preserved.get("protected_ids"),
            f"{label}.content_to_preserve.protected_ids",
            allow_empty=True,
        )
        destination = action.get("destination")
        if destination is not None and not isinstance(destination, (str, list)):
            raise ValidationError(f"{label}.destination: expected string, list, or null")
        if isinstance(destination, list):
            _strings(destination, f"{label}.destination", allow_empty=True)
        if operation == "move" and destination in (None, "", []):
            raise ValidationError(f"{label}.destination: move requires a destination")
        dependencies = _strings(
            action.get("dependencies"), f"{label}.dependencies", allow_empty=True
        )
        unknown = sorted(set(dependencies) - included_ids)
        if unknown or repair_item_id in dependencies:
            raise ValidationError(f"{label}.dependencies: unknown or self dependency")
        actions[repair_item_id] = action
    if set(actions) != included_ids:
        raise ValidationError(
            "normalized_repair_actions: action IDs must equal included_repair_item_ids"
        )
    return actions


def _overlap_group(
    value: Any, label: str, included_ids: set[str], *, disposition: bool
) -> frozenset[str]:
    group = _mapping(value, label)
    ids = _strings(group.get("finding_ids"), f"{label}.finding_ids")
    if len(ids) < 2 or not set(ids) <= included_ids:
        raise ValidationError(f"{label}.finding_ids: need at least two known repair items")
    if disposition:
        _text(group.get("disposition"), f"{label}.disposition")
    return frozenset(ids)


def _overlaps(data: dict[str, Any], included_ids: set[str]) -> None:
    dispositions = [
        _overlap_group(value, f"overlap_dispositions[{index}]", included_ids, disposition=True)
        for index, value in enumerate(_list(data.get("overlap_dispositions"), "overlap_dispositions"))
    ]
    if len(dispositions) != len(set(dispositions)):
        raise ValidationError("overlap_dispositions: duplicate groups")
    identified = _list(data.get("identified_overlaps", []), "identified_overlaps")
    for index, value in enumerate(identified):
        conflict = _overlap_group(
            value, f"identified_overlaps[{index}]", included_ids, disposition=False
        )
        if not any(conflict <= resolved for resolved in dispositions):
            raise ValidationError(f"identified_overlaps[{index}]: uncovered conflict")
    if _list(data.get("unresolved_overlaps", []), "unresolved_overlaps"):
        raise ValidationError("unresolved_overlaps: approved brief cannot contain conflicts")
    if data.get("all_overlaps_resolved") is not True:
        raise ValidationError("all_overlaps_resolved: must be true")


def _writer_access(
    data: dict[str, Any],
    brief_path: str,
    source_ref: dict[str, str],
    register_ref: dict[str, str],
) -> None:
    access = _mapping(data.get("writer_access"), "writer_access")
    allowed_reads = _strings(access.get("allowed_reads"), "writer_access.allowed_reads")
    for index, path in enumerate(allowed_reads):
        _relative_path(path, f"writer_access.allowed_reads[{index}]")
        if any(marker in path.casefold() for marker in FORBIDDEN_ALLOWED_READ_MARKERS):
            raise ValidationError(f"writer_access.allowed_reads[{index}]: forbidden review/history input")
    expected_reads = {source_ref["path"], register_ref["path"], brief_path}
    if set(allowed_reads) != expected_reads:
        raise ValidationError(
            "writer_access.allowed_reads: must contain exactly source dossier, brief, and register"
        )
    forbidden = _strings(access.get("forbidden_reads"), "writer_access.forbidden_reads")
    combined = "\n".join(forbidden).casefold()
    for category, pattern in REQUIRED_FORBIDDEN_READ_CATEGORIES.items():
        if not pattern.search(combined):
            raise ValidationError(f"writer_access.forbidden_reads: missing {category} exclusion")

    writes = _mapping(access.get("allowed_writes"), "writer_access.allowed_writes")
    if set(writes) != {"complete_dossier", "revision_delta"}:
        raise ValidationError(
            "writer_access.allowed_writes: expected only complete_dossier and revision_delta"
        )
    dossier = _artifact_ref(
        writes["complete_dossier"], "writer_access.allowed_writes.complete_dossier", "artifact_id"
    )
    delta = _artifact_ref(
        writes["revision_delta"], "writer_access.allowed_writes.revision_delta", "artifact_id"
    )
    if writes["complete_dossier"].get("change_type") != "editorial_repair":
        raise ValidationError("complete_dossier.change_type: must be editorial_repair")
    if writes["revision_delta"].get("change_type") != "editorial_repair_delta":
        raise ValidationError("revision_delta.change_type: must be editorial_repair_delta")
    if dossier["path"] == delta["path"] or {dossier["path"], delta["path"]} & expected_reads:
        raise ValidationError("writer_access.allowed_writes: outputs must be distinct and not overwrite inputs")
    if (
        dossier["version"] == source_ref["version"]
        or dossier["artifact_id"] == source_ref["artifact_id"]
    ):
        raise ValidationError("complete_dossier: must have a new logical identity and version")


def _execution(data: dict[str, Any]) -> None:
    execution = _mapping(data.get("execution_and_handoff"), "execution_and_handoff")
    for field in (
        "single_complete_target_dossier",
        "partial_artifacts_forbidden",
        "delta_after_dossier_freeze_only",
    ):
        if execution.get(field) is not True:
            raise ValidationError(f"execution_and_handoff.{field}: must be true")
    if "pre_freeze_action_compliance_required" in execution and (
        execution.get("pre_freeze_action_compliance_required") is not True
    ):
        raise ValidationError(
            "execution_and_handoff.pre_freeze_action_compliance_required: "
            "must be true when declared"
        )
    if data.get("active_plugin_version") == "0.10.0" and (
        "pre_freeze_action_compliance_required" not in execution
    ):
        raise ValidationError(
            "execution_and_handoff.pre_freeze_action_compliance_required: "
            "must be true for 0.10.0 briefs"
        )
    _strings(execution.get("section_passes"), "execution_and_handoff.section_passes")
    _strings(execution.get("delta_requirements"), "execution_and_handoff.delta_requirements")


def _mandatory_checks(data: dict[str, Any]) -> None:
    mandatory = _mapping(
        data.get("mandatory_whole_dossier_checks"), "mandatory_whole_dossier_checks"
    )
    if mandatory.get("not_new_findings") is not True:
        raise ValidationError("mandatory_whole_dossier_checks.not_new_findings: must be true")
    checks = _list(mandatory.get("checks"), "mandatory_whole_dossier_checks.checks")
    if not checks:
        raise ValidationError("mandatory_whole_dossier_checks.checks: must be nonempty")
    forbidden_keys = {"finding_id", "finding_ids", "new_findings", "severity"}
    for index, value in enumerate(checks):
        check = _mapping(value, f"mandatory_whole_dossier_checks.checks[{index}]")
        if forbidden_keys & set(check):
            raise ValidationError(f"mandatory_whole_dossier_checks.checks[{index}]: new finding")
        for field in ("check", "instruction", "acceptance"):
            _text(check.get(field), f"mandatory_whole_dossier_checks.checks[{index}].{field}")


def validate_brief(data: dict[str, Any], brief_path: str | Path) -> dict[str, Any]:
    """Validate internal consistency without claiming source-review coverage."""

    if not isinstance(data, dict):
        raise ValidationError("brief: expected YAML mapping")
    _reject_integrity_hash_keys(data)
    if "included_finding_ids" in data:
        raise ValidationError(
            "included_finding_ids: legacy mixed-semantics key is forbidden; "
            "use included_repair_item_ids"
        )
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValidationError(f"schema_version: must be {SCHEMA_VERSION}")
    for field in ("brief_id", "workflow_id", "round_id", "active_plugin_version", "role"):
        _text(data.get(field), field)
    source_ref = _artifact_ref(data.get("source_artifact"), "source_artifact", "artifact_id")
    register_ref = _artifact_ref(
        data.get("protected_content_register"), "protected_content_register", "register_id"
    )
    bindings = _source_review_binding(data)
    included = set(_strings(data.get("included_repair_item_ids"), "included_repair_item_ids"))
    actions = _actions(data, included)
    omitted_findings, included_nonblocking = _omission_ids(data)
    addressed = {
        finding_id
        for action in actions.values()
        for finding_id in action["addresses_finding_ids"]
    }
    if not included_nonblocking <= addressed:
        raise ValidationError(
            "included_nonblocking_finding_rationale: every source finding must be addressed"
        )
    if omitted_findings & addressed:
        raise ValidationError("omitted source findings must not be addressed by included repair items")
    _overlaps(data, included)
    brief_repository_path = _repository_path(brief_path, "brief path")
    _writer_access(data, brief_repository_path, source_ref, register_ref)
    review_paths = {binding["path"] for binding in bindings.values()}
    if review_paths & set(data["writer_access"]["allowed_reads"]):
        raise ValidationError("writer_access.allowed_reads: source reviews must remain audit-only")
    _execution(data)
    _mandatory_checks(data)
    return {
        "source_ref": source_ref,
        "register_ref": register_ref,
        "bindings": bindings,
        "included": included,
        "actions": actions,
        "omitted_findings": omitted_findings,
        "included_nonblocking": included_nonblocking,
    }


def validate_register_binding(
    data: dict[str, Any], register: dict[str, Any], register_path: str | Path
) -> None:
    """Confirm that the frozen register belongs to this exact repair source."""

    source_ref = _artifact_ref(data.get("source_artifact"), "source_artifact", "artifact_id")
    register_ref = _artifact_ref(
        data.get("protected_content_register"), "protected_content_register", "register_id"
    )
    actual_path = _repository_path(register_path, "protected register path")
    if actual_path != register_ref["path"]:
        raise ValidationError("protected register: actual path does not match brief binding")
    if _text(register.get("register_id"), "register.register_id") != register_ref["register_id"]:
        raise ValidationError("protected register: register ID does not match brief binding")
    register_version = register.get("register_version", register.get("version"))
    if _text(register_version, "register.register_version") != register_ref["version"]:
        raise ValidationError("protected register: version does not match brief binding")
    register_source = _artifact_ref(
        register.get("source_artifact"), "register.source_artifact", "artifact_id"
    )
    if register_source != source_ref:
        raise ValidationError(
            "protected register: source artifact must equal the dossier supplied to the writer"
        )


def _frontmatter(path: Path) -> dict[str, Any]:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"{path}: cannot read source review: {exc}") from exc
    if not lines or lines[0].strip() != "---":
        raise ValidationError(f"{path}: missing YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValidationError(f"{path}: unclosed YAML frontmatter") from exc
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML frontmatter: {exc}") from exc
    return _mapping(data, f"{path} frontmatter")


def _yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValidationError(f"{path}: cannot read valid YAML: {exc}") from exc
    return _mapping(data, str(path))


def _findings(report: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(_list(report.get("findings"), f"{label}.findings")):
        finding = _mapping(value, f"{label}.findings[{index}]")
        finding_id = _text(
            finding.get("finding_id", finding.get("id")),
            f"{label}.findings[{index}].finding_id",
        )
        if finding_id in result:
            raise ValidationError(f"{label}.findings: duplicate {finding_id}")
        severity = _text(finding.get("severity"), f"{label}.findings[{index}].severity")
        if severity not in SOURCE_SEVERITIES:
            raise ValidationError(f"{label}.findings[{index}].severity: invalid value")
        result[finding_id] = finding
    return result


def _ordinary_decision_guards(
    narrative_assessment: dict[str, Any], language_assessment: dict[str, Any]
) -> tuple[str, str]:
    narrative_decision = _text(
        narrative_assessment.get("decision"), "narrative assessment.decision"
    )
    if narrative_decision == "clarification_required":
        raise ValidationError(
            "narrative assessment.decision: clarification_required cannot freeze an ordinary writer brief"
        )
    if narrative_decision not in NARRATIVE_ORDINARY_DECISIONS:
        raise ValidationError("narrative assessment.decision: invalid value")

    language_decision = _text(
        language_assessment.get("decision"), "language assessment.decision"
    )
    if language_decision in LANGUAGE_NON_ORDINARY_DECISIONS:
        raise ValidationError(
            f"language assessment.decision: {language_decision} cannot freeze an ordinary writer brief"
        )
    if language_decision not in LANGUAGE_ORDINARY_DECISIONS:
        raise ValidationError("language assessment.decision: invalid value")
    return narrative_decision, language_decision


def _unresolved_source_issues(
    report: dict[str, Any],
    findings: dict[str, dict[str, Any]],
    covered_finding_ids: set[str],
    label: str,
    *,
    ready: bool,
) -> None:
    unresolved = set(
        _strings(report.get("unresolved_issues"), f"{label}.unresolved_issues", allow_empty=True)
    )
    if ready and unresolved:
        raise ValidationError(f"{label}.unresolved_issues: ready report must be empty")
    unknown = unresolved - set(findings)
    if unknown:
        raise ValidationError(
            f"{label}.unresolved_issues: unknown finding IDs: {', '.join(sorted(unknown))}"
        )
    non_actionable = {
        finding_id
        for finding_id in unresolved
        if findings[finding_id]["severity"] not in ACTIONABLE_SEVERITIES
    }
    if non_actionable:
        raise ValidationError(
            f"{label}.unresolved_issues: non-actionable finding IDs: "
            + ", ".join(sorted(non_actionable))
        )
    uncovered = unresolved - covered_finding_ids
    if uncovered:
        raise ValidationError(
            f"{label}.unresolved_issues: actionable findings are not included/covered: "
            + ", ".join(sorted(uncovered))
        )


def _plan_actions(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(_list(plan.get("actions"), "narrative plan.actions")):
        action = _mapping(value, f"narrative plan.actions[{index}]")
        action_id = _text(action.get("action_id"), f"narrative plan.actions[{index}].action_id")
        if action_id in result:
            raise ValidationError(f"narrative plan.actions: duplicate {action_id}")
        _strings(action.get("addresses_findings"), f"narrative plan action {action_id}.addresses_findings")
        result[action_id] = action
    return result


def _payload_identity(payload: dict[str, Any], fields: tuple[str, ...], label: str) -> str:
    for field in fields:
        value = payload.get(field)
        if isinstance(value, str) and value.strip():
            return value
    raise ValidationError(f"{label}: missing logical artifact identity")


def _check_bound_source(
    binding: dict[str, str],
    payload: dict[str, Any],
    actual_path: str | Path,
    identity_fields: tuple[str, ...],
    label: str,
) -> str:
    actual_repository_path = _repository_path(actual_path, f"{label} path")
    if binding["path"] != actual_repository_path:
        raise ValidationError(f"source_review_binding.{label}.path: does not match CLI source")
    identity = _payload_identity(payload, identity_fields, label)
    if binding["artifact_id"] != identity:
        raise ValidationError(f"source_review_binding.{label}.artifact_id: identity mismatch")
    declared_versions = {
        value
        for field in ("version", "round_id")
        if isinstance((value := payload.get(field)), str) and value.strip()
    }
    if declared_versions:
        if binding["version"] not in declared_versions:
            raise ValidationError(f"source_review_binding.{label}.version: version mismatch")
    elif not identity.endswith(f"-{binding['version']}"):
        raise ValidationError(
            f"source_review_binding.{label}.version: not declared by or encoded in source identity"
        )
    return identity


def _same_source_artifact(value: Any, source_ref: dict[str, str], label: str) -> None:
    ref = _artifact_ref(value, label, "artifact_id")
    if ref != source_ref:
        raise ValidationError(f"{label}: source dossier binding mismatch")


def validate_source_coverage(
    data: dict[str, Any],
    narrative_assessment: dict[str, Any],
    narrative_plan: dict[str, Any],
    language_assessment: dict[str, Any],
    *,
    narrative_assessment_path: str | Path,
    narrative_plan_path: str | Path,
    language_assessment_path: str | Path,
    brief_path: str | Path,
) -> None:
    """Validate source identities and complete blocking/nonblocking disposition."""

    state = validate_brief(data, brief_path)
    bindings = state["bindings"]
    narrative_identity = _check_bound_source(
        bindings["narrative_assessment"],
        narrative_assessment,
        narrative_assessment_path,
        ("assessment_id", "artifact_id"),
        "narrative_assessment",
    )
    _check_bound_source(
        bindings["narrative_repair_plan"],
        narrative_plan,
        narrative_plan_path,
        ("plan_id", "artifact_id"),
        "narrative_repair_plan",
    )
    _check_bound_source(
        bindings["language_assessment"],
        language_assessment,
        language_assessment_path,
        ("review_id", "assessment_id", "artifact_id"),
        "language_assessment",
    )
    if narrative_plan.get("assessment_id") != narrative_identity:
        raise ValidationError("narrative plan.assessment_id: does not bind the narrative assessment")
    for label, report in (
        ("narrative assessment", narrative_assessment),
        ("language assessment", language_assessment),
    ):
        if report.get("workflow_id") != data.get("workflow_id"):
            raise ValidationError(f"{label}.workflow_id: does not match writer brief")
    _same_source_artifact(
        narrative_assessment.get("input_dossier"), state["source_ref"], "narrative assessment.input_dossier"
    )
    _same_source_artifact(
        narrative_plan.get("source_artifact"), state["source_ref"], "narrative plan.source_artifact"
    )
    _same_source_artifact(
        language_assessment.get("dossier_ref"), state["source_ref"], "language assessment.dossier_ref"
    )

    narrative_decision, language_decision = _ordinary_decision_guards(
        narrative_assessment, language_assessment
    )
    narrative_findings = _findings(narrative_assessment, "narrative assessment")
    language_findings = _findings(language_assessment, "language assessment")
    if set(narrative_findings) & set(language_findings):
        raise ValidationError("source findings: narrative and language IDs must be distinct")
    plan_actions = _plan_actions(narrative_plan)
    if set(plan_actions) & set(language_findings):
        raise ValidationError("source repair items: narrative action and language finding IDs collide")
    known_items = set(plan_actions) | set(language_findings)
    unknown_items = state["included"] - known_items
    if unknown_items:
        raise ValidationError(
            "included_repair_item_ids: unknown source items: " + ", ".join(sorted(unknown_items))
        )

    included_narrative_actions = state["included"] & set(plan_actions)
    covered_narrative = {
        finding_id
        for action_id in included_narrative_actions
        for finding_id in plan_actions[action_id]["addresses_findings"]
    }
    blocking_narrative = {
        finding_id
        for finding_id, finding in narrative_findings.items()
        if finding["severity"] in BLOCKING_SEVERITIES
    }
    if not blocking_narrative <= covered_narrative:
        raise ValidationError("source coverage: critical/major narrative finding is not covered")
    blocking_language = {
        finding_id
        for finding_id, finding in language_findings.items()
        if finding["severity"] in BLOCKING_SEVERITIES
    }
    if not blocking_language <= state["included"]:
        raise ValidationError("source coverage: critical/major language finding is not included")

    _unresolved_source_issues(
        narrative_assessment,
        narrative_findings,
        covered_narrative | state["omitted_findings"],
        "narrative assessment",
        ready=narrative_decision == "narrative_ready",
    )
    _unresolved_source_issues(
        language_assessment,
        language_findings,
        (state["included"] & set(language_findings)) | state["omitted_findings"],
        "language assessment",
        ready=language_decision == "submission_ready",
    )

    for repair_item_id, action in state["actions"].items():
        if repair_item_id in plan_actions:
            expected_order = plan_actions[repair_item_id]["addresses_findings"]
        else:
            expected_order = [repair_item_id]
        if action["addresses_finding_ids"] != expected_order:
            raise ValidationError(
                f"normalized repair action {repair_item_id}: addresses_finding_ids source mismatch"
            )
        expected_source_items = [
            repair_item_id,
            *(finding_id for finding_id in expected_order if finding_id != repair_item_id),
        ]
        if action["source_item_ids"] != expected_source_items:
            raise ValidationError(
                f"normalized repair action {repair_item_id}: source_item_ids source mismatch"
            )

    all_findings = {**narrative_findings, **language_findings}
    nonblocking = {
        finding_id
        for finding_id, finding in all_findings.items()
        if finding["severity"] in NONBLOCKING_SEVERITIES
    }
    dispositions = state["included_nonblocking"] | state["omitted_findings"]
    if dispositions != nonblocking:
        raise ValidationError(
            "source coverage: every minor/suggestion finding needs exactly one included or omitted disposition"
        )
    for finding_id in state["included_nonblocking"]:
        if finding_id not in nonblocking:
            raise ValidationError(f"included nonblocking source finding {finding_id}: unresolved or blocking")
        executed = (
            finding_id in covered_narrative
            if finding_id in narrative_findings
            else finding_id in state["included"]
        )
        if not executed:
            raise ValidationError(f"included nonblocking source finding {finding_id}: no included repair item")
    for finding_id in state["omitted_findings"]:
        if finding_id not in nonblocking:
            raise ValidationError(f"omitted source finding {finding_id}: unresolved or blocking")
        executed = (
            finding_id in covered_narrative
            if finding_id in narrative_findings
            else finding_id in state["included"]
        )
        if executed:
            raise ValidationError(f"omitted source finding {finding_id}: covered by included repair item")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    parser.add_argument("--narrative-assessment", type=Path)
    parser.add_argument("--narrative-plan", type=Path)
    parser.add_argument("--language-assessment", type=Path)
    parser.add_argument("--protected-register", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_paths = (
        args.narrative_assessment,
        args.narrative_plan,
        args.language_assessment,
    )
    try:
        data = _yaml(args.brief)
        if any(source_paths) and not all(source_paths):
            raise ValidationError(
                "source coverage options must be supplied together: --narrative-assessment, "
                "--narrative-plan, --language-assessment"
            )
        if all(source_paths) and args.protected_register is None:
            raise ValidationError(
                "source coverage validation also requires --protected-register"
            )
        if all(source_paths):
            validate_source_coverage(
                data,
                _frontmatter(args.narrative_assessment),
                _yaml(args.narrative_plan),
                _frontmatter(args.language_assessment),
                narrative_assessment_path=args.narrative_assessment,
                narrative_plan_path=args.narrative_plan,
                language_assessment_path=args.language_assessment,
                brief_path=args.brief,
            )
            validate_register_binding(data, _yaml(args.protected_register), args.protected_register)
            print("PASS: writer brief internal consistency and source-review coverage are valid")
        else:
            validate_brief(data, args.brief)
            if args.protected_register is not None:
                validate_register_binding(data, _yaml(args.protected_register), args.protected_register)
            print("PASS: writer brief internal consistency is valid; source coverage not checked")
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
