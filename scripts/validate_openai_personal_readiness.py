#!/usr/bin/env python3
"""Validate deterministic and owner-observed personal readiness evidence.

Repository fixtures may remain pending.  An ``owner_observed`` receipt is
accepted only when its schema, local files, hashes, Codex JSONL, independent
actors, and slot-specific evidence all agree.  Use ``--require-ready`` only
when intentionally promoting the current personal installation.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SCHEMA = REPO / "tests" / "openai_personal" / "owner-observed-receipts.schema.yaml"
RUN_INDEX_SCHEMA = REPO / "tests" / "openai_personal" / "runtime-run-index.schema.yaml"
RECEIPTS = REPO / "tests" / "openai_personal" / "current-version-owner-observed-receipts.yaml"
REPORT = PLUGIN / "reports" / "personal-readiness.json"

EXPECTED_DECLARED = {
    "academic-deep-search",
    "article-orchestrator",
    "perspective-orchestrator",
    "proposal-orchestrator",
    "research-idea-orchestrator",
    "research-opportunity-mapper",
    "research-polisher-orchestrator",
}
EXPECTED_IMPLICIT = EXPECTED_DECLARED - {"research-polisher-orchestrator"}
EXPECTED_WORKFLOWS = {"idea", "proposal", "article", "perspective", "research_polisher"}
EXPECTED_WORKFLOW_SLOTS = {
    "personal-idea-happy": ("idea", "human_signoff_required"),
    "personal-proposal-happy": ("proposal", "human_signoff_required"),
    "personal-article-happy": ("article", "human_signoff_required"),
    "personal-perspective-happy": ("perspective", "human_signoff_required"),
    "personal-research-polisher-happy": (
        "research_polisher",
        "human_strategy_selection_required",
    ),
}
EXPECTED_CONTROL_SLOTS = {
    "personal-reviewer-unavailable-control": "independent_review_pending",
    "personal-fatal-finding-control": "blocked_without_ready_state",
}
EXPECTED_RETRIEVAL_SLOTS = {
    "personal-search-current": "source_grounded_current_answer",
    "personal-search-exact": "source_grounded_exact_answer",
    "personal-search-narrow-academic": "source_grounded_narrow_academic_answer",
    "personal-deep-research-inactive": (
        "deep_research_handoff_required_with_continuation_package"
    ),
    "personal-deep-research-complete": (
        "handoff_completion_mapper_return_and_single_edge_resume"
    ),
}
EXPECTED_CONTROL_TYPE = {
    "personal-reviewer-unavailable-control": "reviewer_unavailable",
    "personal-fatal-finding-control": "fatal_digest_mismatch",
}
EXPECTED_SLOT_KINDS = {
    "personal-distribution-current": "distribution",
    **{slot_id: "workflow_happy" for slot_id in EXPECTED_WORKFLOW_SLOTS},
    **{slot_id: "workflow_control" for slot_id in EXPECTED_CONTROL_SLOTS},
    "personal-search-current": "search",
    "personal-search-exact": "search",
    "personal-search-narrow-academic": "search",
    "personal-deep-research-inactive": "deep_research_inactive",
    "personal-deep-research-complete": "deep_research_complete",
}
APPROVED_CODEX_CLI_VERSION = "0.144.4"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
GIT_COMMIT = re.compile(r"^[0-9a-f]{40}$")
READY_STATES = {
    "accept",
    "accepted",
    "promoted",
    "ready",
    "ready_for_human_signoff",
    "human_signoff_required",
    "human_strategy_selection_required",
}
QUALIFYING_REVIEW_DECISIONS = {
    "accept",
    "accepted",
    "approve",
    "approved",
    "cleared",
    "conditional_handoff",
    "handoff_ready",
    "no_blocking_findings",
    "pass",
    "passed",
    "proceed",
    "promote",
    "promoted",
    "publishable",
    "ready",
    "ready_for_human_selection",
    "retain",
    "retained",
    "strong_support",
    "support_with_minor_revision",
    "suitable",
    "verified",
}
HISTORICAL_REVIEW_STAGES = {
    "initial_evaluator",
    "supporting_pre_generation",
    "supporting_historical",
    "strategist_initial",
    "strategist_revision",
    "polisher_initial_final",
}
QUALIFYING_REVIEW_STAGES = {
    "fresh_reevaluator",
    "supporting_qualifying",
    "panel_reviewer",
    "final_verifier",
    "polisher_fresh_final",
}
REVIEW_STAGES = HISTORICAL_REVIEW_STAGES | QUALIFYING_REVIEW_STAGES
PRIVATE_ROOTS = (
    REPO / "tests" / "article" / ".phase7-8-runs",
    REPO / "tests" / "idea-to-proposal" / ".phase7-8-runs",
)


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silently overwritten mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)
REVIEW_ROLE_MARKERS = (
    "review",
    "evaluat",
    "audit",
    "assess",
    "triage",
    "panel",
    "verif",
    "preflight",
)
REVIEW_OUTPUT_MARKERS = REVIEW_ROLE_MARKERS + ("finding", "quality")
FORBIDDEN_REVIEW_INPUT_MARKERS = (
    "readme",
    "revision-delta",
    "revision_delta",
    "prior-score",
    "prior_score",
    "previous-version",
    "previous_version",
)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def raw_file_sha256(path: Path) -> str:
    """Hash an evidence file byte-for-byte."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_sha256(path: Path) -> str:
    """Hash tracked text canonically so Windows and Linux agree."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def skill_tree_sha256(skills_root: Path) -> str:
    """Hash installable skill paths and canonical content deterministically."""
    digest = hashlib.sha256()
    files = sorted(
        (path for path in skills_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(skills_root).as_posix(),
    )
    for path in files:
        relative = path.relative_to(skills_root).as_posix().encode("utf-8")
        content = path.read_bytes().replace(b"\r\n", b"\n")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
        digest.update(b"\0")
    return digest.hexdigest()


def _git_head(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().lower()


def _query_cli_version(cli_path: Path) -> str:
    result = subprocess.run(
        [str(cli_path), "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    output = " ".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    ).strip()
    match = re.fullmatch(r"codex-cli\s+(\S+)", output)
    if result.returncode != 0 or match is None:
        raise ValueError("CLI --version did not return 'codex-cli <version>'")
    return match.group(1)


def _schema_errors(document: Any, schema: dict[str, Any], label: str) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [f"{label}: schema is invalid: {exc.message}"]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return _validator_errors(document, validator, label)


def _validator_errors(
    document: Any, validator: Draft202012Validator, label: str
) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(document),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    ):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{label}: schema violation at {location}: {error.message}")
    return errors


def _embedded_run_index_schema(
    run_index_schema: dict[str, Any], receipt_schema: dict[str, Any]
) -> dict[str, Any]:
    """Embed shared receipt definitions so validation never fetches a URI."""
    embedded = copy.deepcopy(run_index_schema)
    embedded["$defs"] = copy.deepcopy(receipt_schema.get("$defs", {}))

    def rewrite(value: Any) -> None:
        if isinstance(value, dict):
            reference = value.get("$ref")
            prefix = "owner-observed-receipts.schema.yaml#/$defs/"
            if isinstance(reference, str) and reference.startswith(prefix):
                value["$ref"] = "#/$defs/" + reference[len(prefix) :]
            for child in value.values():
                rewrite(child)
        elif isinstance(value, list):
            for child in value:
                rewrite(child)

    rewrite(embedded)
    return embedded


def _resolve_repo_file(repo_root: Path, stored_path: Any, label: str) -> tuple[Path | None, list[str]]:
    if not isinstance(stored_path, str) or not stored_path.strip():
        return None, [f"{label}: path is missing"]
    candidate = Path(stored_path)
    if candidate.is_absolute():
        return None, [f"{label}: path must be repository-relative"]
    root = repo_root.resolve()
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root):
        return None, [f"{label}: path escapes the repository"]
    if not resolved.is_file():
        return None, [f"{label}: file does not exist: {stored_path}"]
    return resolved, []


def _validate_file_binding(
    value: Any,
    repo_root: Path,
    label: str,
) -> tuple[Path | None, list[str]]:
    if not isinstance(value, dict):
        return None, [f"{label}: file binding is malformed"]
    path, errors = _resolve_repo_file(repo_root, value.get("path"), label)
    digest = value.get("sha256")
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        errors.append(f"{label}: SHA-256 is malformed")
    elif path is not None and raw_file_sha256(path) != digest:
        errors.append(f"{label}: SHA-256 does not match file bytes")
    return path, errors


@functools.lru_cache(maxsize=None)
def _git_private_path_state(repo_root: str, relative: str) -> tuple[bool, bool]:
    """Return ignored/tracked state without repeating Git subprocesses per receipt."""
    root = Path(repo_root)
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", relative],
        cwd=root,
        check=False,
        capture_output=True,
    )
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", relative],
        cwd=root,
        check=False,
        capture_output=True,
    )
    return ignored.returncode == 0, tracked.returncode == 0


def _validate_private_path(
    path: Path | None,
    repo_root: Path,
    label: str,
    *,
    allow_private_inputs: bool = False,
) -> list[str]:
    if path is None:
        return []
    resolved = path.resolve()
    run_roots = (
        (repo_root / "tests" / "article" / ".phase7-8-runs").resolve(),
        (repo_root / "tests" / "idea-to-proposal" / ".phase7-8-runs").resolve(),
    )
    roots = run_roots
    if allow_private_inputs:
        roots = roots + (
            (repo_root / "tests" / "article").resolve(),
            (repo_root / "tests" / "idea-to-proposal").resolve(),
        )
    if not any(resolved.is_relative_to(root) for root in roots):
        return [f"{label}: observed evidence is outside allowed private run roots"]
    relative = resolved.relative_to(repo_root.resolve()).as_posix()
    ignored, tracked = _git_private_path_state(str(repo_root.resolve()), relative)
    if not ignored:
        return [f"{label}: observed evidence is not Git-ignored"]
    if tracked:
        return [f"{label}: observed evidence is tracked by Git"]
    return []


def _validate_artifact_binding(
    value: Any,
    repo_root: Path,
    label: str,
    *,
    require_digest: bool = True,
) -> tuple[Path | None, list[str]]:
    if not isinstance(value, dict):
        return None, [f"{label}: artifact binding is malformed"]
    errors: list[str] = []
    for field in ("artifact_id", "version"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            errors.append(f"{label}: {field} is missing")
    if require_digest:
        path, file_errors = _validate_file_binding(value, repo_root, label)
        errors.extend(file_errors)
    else:
        path, path_errors = _resolve_repo_file(repo_root, value.get("path"), label)
        errors.extend(path_errors)
    return path, errors


def _load_markdown_frontmatter(
    path: Path,
    label: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return None, [f"{label}: Markdown artifact cannot be read: {exc}"]
    if not lines or lines[0].strip() != "---":
        return None, [f"{label}: Markdown artifact lacks YAML frontmatter"]
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return None, [f"{label}: Markdown artifact frontmatter is not closed"]
    try:
        value = yaml.load("\n".join(lines[1:closing]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return None, [f"{label}: Markdown artifact frontmatter cannot be parsed: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{label}: Markdown artifact frontmatter must be a mapping"]
    return value, []


def _parse_datetime(value: Any, label: str) -> tuple[datetime | None, list[str]]:
    if not isinstance(value, str):
        return None, [f"{label}: timestamp is missing"]
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None, [f"{label}: timestamp is not RFC3339"]
    if parsed.tzinfo is None:
        return None, [f"{label}: timestamp must include a timezone"]
    return parsed, []


def _load_jsonl(path: Path, label: str) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON on line {line_number}: {exc.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{label}: line {line_number} is not a JSON object")
            continue
        outer = str(value.get("type", "unknown"))
        item = value.get("item")
        inner = str(item.get("type", "")) if isinstance(item, dict) else ""
        kind = f"{outer}:{inner}" if inner else outer
        value["__line_id"] = f"line-{line_number:06d}:{kind}"
        events.append(value)
    if not events:
        errors.append(f"{label}: JSONL contains no events")
    return events, errors


def _event_kind(event: dict[str, Any]) -> str:
    outer = str(event.get("type", ""))
    item = event.get("item")
    inner = str(item.get("type", "")) if isinstance(item, dict) else ""
    return f"{outer}:{inner}" if inner else outer


def _event_id(event: dict[str, Any]) -> str | None:
    for field in ("event_id", "id", "thread_id", "turn_id"):
        value = event.get(field)
        if isinstance(value, str) and value:
            return value
    item = event.get("item")
    if isinstance(item, dict):
        for field in ("event_id", "id"):
            value = item.get(field)
            if isinstance(value, str) and value:
                return value
    synthetic = event.get("__line_id")
    if isinstance(synthetic, str) and synthetic:
        return synthetic
    return None


def _is_completed_web_search(event: dict[str, Any]) -> bool:
    outer = str(event.get("type", ""))
    item = event.get("item")
    inner = str(item.get("type", "")) if isinstance(item, dict) else ""
    if outer == "item.completed" and inner == "web_search":
        return True
    if outer in {"web_search.completed", "web_search_completed"}:
        return True
    return outer == "web_search" and event.get("status") == "completed"


def _canonical_url(value: str) -> str:
    parts = urlsplit(value.strip())
    query = urlencode(
        sorted(
            (key, item)
            for key, item in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_")
        )
    )
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, query, "")
    )


@functools.lru_cache(maxsize=1)
def _reviewer_skill_names() -> frozenset[str]:
    try:
        registry = load_yaml(PLUGIN / "workflow-registry.yaml")
        return frozenset(
            str(item.get("name"))
            for item in registry.get("skills", [])
            if isinstance(item, dict) and item.get("requires_independent_subagent") is True
        )
    except (OSError, ValueError, yaml.YAMLError):
        return frozenset()


def _is_reviewer(actor: dict[str, Any]) -> bool:
    skill = str(actor.get("skill", "")).split(":")[-1]
    if skill in _reviewer_skill_names():
        return True
    role = str(actor.get("role", "")).lower()
    return any(marker in role for marker in REVIEW_ROLE_MARKERS)


def _load_structured_file(path: Path, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        value = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.suffix.lower() == ".json"
            else yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        )
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        return None, [f"{label}: structured evidence cannot be parsed: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{label}: structured evidence must be a mapping"]
    return value, []


def _load_review_record(path: Path, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    if path.suffix.lower() != ".md":
        return _load_structured_file(path, label)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return None, [f"{label}: review report cannot be read: {exc}"]
    if not lines or lines[0].strip() != "---":
        return None, [f"{label}: Markdown review lacks YAML frontmatter"]
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return None, [f"{label}: Markdown review frontmatter is not closed"]
    try:
        value = yaml.load("\n".join(lines[1:closing]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return None, [f"{label}: review frontmatter cannot be parsed: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{label}: review frontmatter must be a mapping"]
    return value, []


def _review_list(record: dict[str, Any], names: tuple[str, ...]) -> tuple[list[Any], bool]:
    for name in names:
        if name in record:
            value = record[name]
            return value if isinstance(value, list) else [], isinstance(value, list)
    return [], False


def _validate_review_report(
    report: dict[str, Any],
    actor: dict[str, Any],
    reviewed_artifacts: list[dict[str, Any]],
    workflow_id: str,
    ready_outcome: bool,
    repo_root: Path,
    label: str,
    *,
    require_digest: bool = True,
) -> tuple[list[str], list[Any]]:
    errors: list[str] = []
    path, path_errors = _validate_artifact_binding(
        report, repo_root, label, require_digest=require_digest
    )
    errors.extend(path_errors)
    if path is None:
        return errors, []
    record, record_errors = _load_review_record(path, label)
    errors.extend(record_errors)
    if record is None:
        return errors, []
    for field in (
        "review_id",
        "workflow_id",
        "reviewer_actor_id",
        "reviewer_skill",
        "reviewer_instance_id",
        "review_stage",
        "round_id",
        "review_scope",
        "reviewed_artifact_id",
        "reviewed_artifact_version",
        "reviewed_artifact_path",
        "report_artifact_id",
        "report_artifact_version",
        "report_artifact_path",
        "decision",
    ):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"{label}: {field} is missing")
    if require_digest and (
        not isinstance(record.get("reviewed_artifact_digest"), str)
        or not record["reviewed_artifact_digest"].strip()
    ):
        errors.append(f"{label}: reviewed_artifact_digest is missing")
    if record.get("workflow_id") != workflow_id:
        errors.append(f"{label}: workflow_id differs from the workflow receipt")
    if record.get("reviewer_actor_id") != actor.get("actor_id"):
        errors.append(f"{label}: reviewer_actor_id differs from the bound actor")
    if record.get("reviewer_skill") != actor.get("skill"):
        errors.append(f"{label}: reviewer_skill differs from the bound actor")
    if record.get("reviewer_instance_id") != actor.get("instance_id"):
        errors.append(f"{label}: reviewer_instance_id differs from the bound actor")
    review_stage = actor.get("review_stage")
    if record.get("review_stage") != review_stage:
        errors.append(f"{label}: review_stage differs from the bound actor")
    if record.get("files_read") != actor.get("files_read"):
        errors.append(f"{label}: files_read differs from the bound actor")
    if record.get("files_written") != actor.get("files_written"):
        errors.append(f"{label}: files_written differs from the bound actor")
    expected_input_ids = [artifact.get("artifact_id") for artifact in reviewed_artifacts]
    expected_input_versions = [artifact.get("version") for artifact in reviewed_artifacts]
    if record.get("input_artifact_ids") != expected_input_ids:
        errors.append(f"{label}: input_artifact_ids differ from bound files_read artifacts")
    if record.get("input_versions") != expected_input_versions:
        errors.append(f"{label}: input_versions differ from bound files_read artifacts")
    report_fields = {
        "report_artifact_id": report.get("artifact_id"),
        "report_artifact_version": report.get("version"),
        "report_artifact_path": report.get("path"),
    }
    for field, expected in report_fields.items():
        if record.get(field) != expected:
            errors.append(f"{label}: {field} differs from the report binding")
    reviewed_fields = {
        "reviewed_artifact_id": "artifact_id",
        "reviewed_artifact_version": "version",
        "reviewed_artifact_path": "path",
    }
    if require_digest:
        reviewed_fields["reviewed_artifact_digest"] = "sha256"
    matching_artifacts = [
        artifact
        for artifact in reviewed_artifacts
        if all(record.get(record_field) == artifact.get(binding_field)
               for record_field, binding_field in reviewed_fields.items())
    ]
    if len(matching_artifacts) != 1:
        mismatch = (
            "reviewed artifact digest differs from the frozen input"
            if require_digest
            else "reviewed artifact logical reference differs from the frozen input"
        )
        errors.append(f"{label}: {mismatch}")
    elif matching_artifacts[0].get("path") not in actor.get("files_read", []):
        errors.append(f"{label}: reviewed artifact is absent from reviewer files_read")
    if record.get("isolation_mode") != "fresh_subagent":
        errors.append(f"{label}: isolation_mode is not fresh_subagent")
    if record.get("source_edits_performed") is not False:
        errors.append(f"{label}: source_edits_performed must be false")
    for field in (
        "prior_scores_visible",
        "prior_versions_visible",
        "revision_delta_visible",
    ):
        if record.get(field) is not False:
            errors.append(f"{label}: {field} must be false")
    if record.get("complete_artifact_confirmed") is not True:
        errors.append(f"{label}: complete_artifact_confirmed must be true")
    findings, findings_valid = _review_list(record, ("findings",))
    fatal, fatal_valid = _review_list(record, ("fatal_findings",))
    blocking, blocking_valid = _review_list(record, ("blocking_findings",))
    dissent, dissent_valid = _review_list(record, ("dissent",))
    unresolved, unresolved_valid = _review_list(record, ("unresolved_issues",))
    for field, valid in (
        ("fatal_findings", fatal_valid),
        ("blocking_findings", blocking_valid),
        ("dissent", dissent_valid),
        ("unresolved_issues", unresolved_valid),
        ("findings", findings_valid),
    ):
        if not valid:
            errors.append(f"{label}: {field} list is missing or malformed")
    decision = str(record.get("decision", "")).strip().lower()
    if ready_outcome and (
        fatal or decision in {"reject", "rejected", "block", "blocked"}
    ):
        errors.append(
            f"{label}: fatal or terminal reject review conflicts with ready outcome"
        )
    if ready_outcome and review_stage in QUALIFYING_REVIEW_STAGES and (
        blocking or decision not in QUALIFYING_REVIEW_DECISIONS
    ):
        errors.append(
            f"{label}: qualifying blocking or non-qualifying decision conflicts with ready outcome"
        )
    return errors, dissent


def _artifact_key(
    value: dict[str, Any], *, logical_only: bool = False
) -> tuple[Any, ...]:
    fields = ("artifact_id", "version", "path")
    if not logical_only:
        fields = (*fields, "sha256")
    return tuple(value.get(field) for field in fields)


IDEA_IDENTITY_ANCHOR_FIELDS = (
    "primary_research_question",
    "primary_objective",
    "study_object",
    "core_data_or_evidence_base",
    "primary_unit_of_inference",
)


def _validate_idea_dossier_identity(
    artifact: dict[str, Any],
    path: Path,
    label: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    frontmatter, errors = _load_markdown_frontmatter(path, label)
    if frontmatter is None:
        return None, errors
    if frontmatter.get("schema_version") != "research-idea.v3":
        errors.append(f"{label}: schema_version is not research-idea.v3")
    for frontmatter_field, binding_field in (
        ("artifact_id", "artifact_id"),
        ("version_id", "version"),
    ):
        if frontmatter.get(frontmatter_field) != artifact.get(binding_field):
            errors.append(
                f"{label}: frontmatter {frontmatter_field} differs from the logical binding"
            )
    if "path" in frontmatter and frontmatter.get("path") != artifact.get("path"):
        errors.append(f"{label}: frontmatter path differs from the logical binding")
    if frontmatter.get("frozen") is not True:
        errors.append(f"{label}: dossier is not frozen")
    if not isinstance(frontmatter.get("idea_id"), str) or not frontmatter["idea_id"].strip():
        errors.append(f"{label}: idea_id is missing")
    anchor = frontmatter.get("identity_anchor")
    if not isinstance(anchor, dict):
        errors.append(f"{label}: identity_anchor is missing")
    else:
        for field in IDEA_IDENTITY_ANCHOR_FIELDS:
            if not isinstance(anchor.get(field), str) or not anchor[field].strip():
                errors.append(f"{label}: identity_anchor.{field} is missing")
    return frontmatter, errors


def _validate_idea_index_and_pointer(
    evidence: dict[str, Any],
    binding: dict[str, Any],
    repo_root: Path,
    revised: dict[str, Any],
    revised_frontmatter: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    index_binding = evidence.get("idea_index_artifact")
    pointer_binding = evidence.get("current_pointer_artifact")
    index_path, index_errors = _validate_artifact_binding(
        index_binding,
        repo_root,
        "personal-idea-happy.idea_index_artifact",
        require_digest=False,
    )
    pointer_path, pointer_errors = _validate_artifact_binding(
        pointer_binding,
        repo_root,
        "personal-idea-happy.current_pointer_artifact",
        require_digest=False,
    )
    errors.extend(index_errors + pointer_errors)
    if index_path is None or pointer_path is None:
        return errors

    pointer, pointer_parse_errors = _load_structured_file(
        pointer_path, "personal-idea-happy.current_pointer_artifact"
    )
    index_record, index_parse_errors = _load_structured_file(
        index_path, "personal-idea-happy.idea_index_artifact"
    )
    errors.extend(pointer_parse_errors + index_parse_errors)
    if pointer is None or index_record is None:
        return errors

    expected_pointer = {
        "current_dossier_id": revised.get("artifact_id"),
        "current_version": revised.get("version"),
        "current_path": revised.get("path"),
    }
    for field, expected in expected_pointer.items():
        if pointer.get(field) != expected:
            errors.append(f"personal-idea-happy: current pointer {field} differs from the revised dossier")
    if revised_frontmatter is not None:
        if pointer.get("idea_id") != revised_frontmatter.get("idea_id"):
            errors.append("personal-idea-happy: current pointer idea_id differs from dossier frontmatter")
        if pointer.get("identity_anchor") != revised_frontmatter.get("identity_anchor"):
            errors.append("personal-idea-happy: current pointer identity anchor differs from dossier frontmatter")
    if pointer.get("identity_status") != "preserved":
        errors.append("personal-idea-happy: current pointer does not preserve the Idea identity")

    evaluations = evidence.get("evaluation_artifacts", [])
    qualifying = evaluations[-1] if isinstance(evaluations, list) and evaluations else None
    qualifying_ref = pointer.get("qualifying_evaluation_ref")
    expected_qualifying_ref = (
        {
            "artifact_id": qualifying.get("artifact_id"),
            "version": qualifying.get("version"),
            "path": qualifying.get("path"),
        }
        if isinstance(qualifying, dict)
        else None
    )
    if qualifying_ref != expected_qualifying_ref:
        errors.append("personal-idea-happy: current pointer does not bind the fresh reassessment")

    index = index_record.get("idea_index")
    if not isinstance(index, dict):
        errors.append("personal-idea-happy: Idea index wrapper is missing")
        return errors
    if index.get("artifact_id") != index_binding.get("artifact_id"):
        errors.append("personal-idea-happy: Idea index frontmatter identity differs from its binding")
    if index.get("frozen") is not True:
        errors.append("personal-idea-happy: Idea index is not frozen")
    ideas = index.get("ideas")
    if not isinstance(ideas, list):
        errors.append("personal-idea-happy: Idea index entries are missing")
        return errors
    pointer_idea_id = pointer.get("idea_id")
    matching = [
        item for item in ideas
        if isinstance(item, dict) and item.get("idea_id") == pointer_idea_id
    ]
    if len(matching) != 1:
        errors.append("personal-idea-happy: Idea index lacks one unambiguous current entry")
        return errors
    entry = matching[0]
    expected_entry = {
        "dossier_id": revised.get("artifact_id"),
        "dossier_version": revised.get("version"),
        "dossier_path": revised.get("path"),
        "node_path": pointer_binding.get("path"),
    }
    for field, expected in expected_entry.items():
        if entry.get(field) != expected:
            errors.append(f"personal-idea-happy: Idea index {field} differs from the current pointer")
    return errors


def _normalized_artifact_path(value: dict[str, Any], repo_root: Path) -> str | None:
    stored = value.get("path")
    if not isinstance(stored, str) or not stored.strip():
        return None
    portable = stored.replace("\\", "/")
    return os.path.normcase(str((repo_root / Path(portable)).resolve()))


IDEA_DOSSIER_SECTIONS = (
    "Title, summary, audience, and positioning",
    "Structured abstract",
    "Background, current state, gap, significance, and rationale",
    "Research question, objectives, and core hypothesis",
    "Research content and work packages",
    "Data, materials, and existing evidence base",
    "Research design and methods",
    "Key techniques and implementation",
    "Evidence chains",
    "Required analyses and evidence",
    "Expected outputs, falsification criteria, and interpretations",
    "Contribution, innovation, impact, application, and closest-work comparison",
    "Title and positioning claim-support table",
    "Feasibility, resources, risks, alternatives, and stop conditions",
    "References",
)
PROFILE_SECTION_GROUPS: dict[str, tuple[tuple[str, ...], ...]] = {
    "proposal": (
        ("Executive summary", "摘要", "执行摘要"),
        ("Problem and gap", "研究问题与缺口", "问题与缺口"),
        ("Objectives", "研究目标", "目标"),
        ("Research plan", "研究计划", "研究内容与计划"),
        ("Methods", "研究方法", "方法"),
        ("Feasibility", "可行性", "可行性与资源"),
        ("Expected outputs", "预期产出", "预期结果"),
        ("References", "参考文献"),
    ),
    "article": (
        ("Abstract", "摘要"),
        ("Introduction", "引言"),
        ("Methods", "方法", "材料与方法"),
        ("Results", "结果"),
        ("Discussion", "讨论"),
        ("References", "参考文献"),
    ),
    "perspective": (
        ("Summary", "Abstract", "摘要", "概述"),
        ("Background and context", "背景与语境", "背景"),
        ("Central thesis and argument", "核心论点与论证", "核心论点"),
        ("Evidence and counterarguments", "证据与反方观点", "证据与异议"),
        ("Implications and impact", "启示与影响", "影响与意义"),
        ("Limitations", "局限性", "局限"),
        ("References", "参考文献"),
    ),
    "research_polisher": (
        ("Portfolio summary", "方案组合摘要"),
        ("Scientific significance strategies", "科学意义策略"),
        ("Practical value strategies", "实用价值策略"),
        ("Dissemination and editorial strategies", "传播与编辑策略"),
        ("Pareto trade-offs", "Pareto 权衡", "帕累托权衡"),
        ("Risks and stop conditions", "风险与停止条件"),
    ),
}
PLACEHOLDER_BODY = re.compile(
    r"^(?:tbd|todo|n/?a|none|placeholder|lorem ipsum|待补充|待定|占位)(?:[.!。！])?$",
    re.I,
)


def _markdown_h2_sections(text: str) -> tuple[list[str], dict[str, str]]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
    order: list[str] = []
    sections: dict[str, str] = {}
    for offset, match in enumerate(matches):
        heading = match.group(1).strip()
        end = matches[offset + 1].start() if offset + 1 < len(matches) else len(text)
        order.append(heading)
        sections[heading.casefold()] = text[match.end() : end].strip()
    return order, sections


def _profile_section(
    sections: dict[str, str], aliases: tuple[str, ...]
) -> tuple[str | None, str]:
    for alias in aliases:
        if alias.casefold() in sections:
            return alias, sections[alias.casefold()]
    return None, ""


def _substantive_section(body: str) -> bool:
    compact = " ".join(body.split()).strip()
    if not compact or PLACEHOLDER_BODY.fullmatch(compact) is not None:
        return False
    words = re.findall(r"[a-z]+", compact.casefold())
    if words and not any(
        word not in {"tbd", "todo", "none", "placeholder", "lorem", "ipsum"}
        for word in words
    ):
        return False
    cjk_count = len(re.findall(r"[\u3400-\u9fff]", compact))
    if cjk_count >= 6:
        return True
    alphanumeric_count = sum(character.isalnum() for character in compact)
    return alphanumeric_count >= 16 and len(words) >= 3


def _validate_profile_complete_artifact(
    profile: str, text: str, label: str
) -> list[str]:
    errors: list[str] = []
    h1 = re.findall(r"^# (?!#)(.+?)\s*$", text, re.M)
    if len(h1) != 1:
        errors.append(f"{label}: complete artifact must contain exactly one title")
    order, sections = _markdown_h2_sections(text)
    if profile == "idea":
        missing = [name for name in IDEA_DOSSIER_SECTIONS if name.casefold() not in sections]
        if missing:
            errors.append(f"{label}: Idea dossier lacks required section(s): {', '.join(missing)}")
        present_order = [name for name in IDEA_DOSSIER_SECTIONS if name.casefold() in sections]
        positions = [order.index(name) for name in present_order if name in order]
        if len(present_order) == len(IDEA_DOSSIER_SECTIONS) and positions != sorted(positions):
            errors.append(f"{label}: Idea dossier sections are out of order")
        if len(order) != len(IDEA_DOSSIER_SECTIONS):
            errors.append(f"{label}: Idea dossier must contain the complete fixed section set")
        for name in IDEA_DOSSIER_SECTIONS:
            body = sections.get(name.casefold(), "")
            if name.casefold() in sections and not _substantive_section(body):
                errors.append(f"{label}: Idea dossier section is empty or placeholder: {name}")
        overview = sections.get(IDEA_DOSSIER_SECTIONS[0].casefold(), "")
        for field in (
            "Title",
            "One-sentence complete-Idea summary",
            "Primary audience",
            "Positioning and contribution frame",
        ):
            if not re.search(rf"^- \*\*{re.escape(field)}:\*\*\s*\S", overview, re.M):
                errors.append(f"{label}: Idea dossier overview lacks {field}")
        abstract = sections.get(IDEA_DOSSIER_SECTIONS[1].casefold(), "")
        for field in (
            "Background and gap",
            "Objective and hypothesis",
            "Approach",
            "Expected result",
            "Contribution and impact",
        ):
            if not re.search(rf"^- \*\*{re.escape(field)}:\*\*\s*\S", abstract, re.M):
                errors.append(f"{label}: Idea dossier structured abstract lacks {field}")
        chains = sections.get("evidence chains", "")
        for field in ("Input", "Method / analysis / processing", "Output"):
            if not re.search(rf"^- \*\*{re.escape(field)}:\*\*\s*\S", chains, re.M):
                errors.append(f"{label}: Idea evidence chain lacks {field}")
        return errors

    groups = PROFILE_SECTION_GROUPS.get(profile)
    if groups is None:
        return [f"{label}: unsupported workflow completeness profile {profile}"]
    for aliases in groups:
        heading, body = _profile_section(sections, aliases)
        if heading is None:
            errors.append(f"{label}: {profile} artifact lacks required section {aliases[0]}")
        elif not _substantive_section(body):
            errors.append(f"{label}: {profile} section is empty or placeholder: {heading}")
    return errors


def _actor_by_id(actors: list[Any], actor_id: Any) -> dict[str, Any] | None:
    return next(
        (
            actor
            for actor in actors
            if isinstance(actor, dict) and actor.get("actor_id") == actor_id
        ),
        None,
    )


def _actor_by_instance(actors: list[Any], instance_id: Any) -> dict[str, Any] | None:
    return next(
        (
            actor
            for actor in actors
            if isinstance(actor, dict) and actor.get("instance_id") == instance_id
        ),
        None,
    )


def _validate_workflow_evidence(
    receipt: dict[str, Any],
    repo_root: Path,
    run_index: dict[str, Any] | None,
) -> list[str]:
    slot_id = str(receipt.get("slot_id"))
    binding = receipt.get("binding", {})
    evidence = binding.get("workflow_evidence") if isinstance(binding, dict) else None
    if not isinstance(evidence, dict):
        return [f"{slot_id}: complete workflow evidence is missing"]
    errors: list[str] = []
    profile = evidence.get("profile")
    idea_logical = profile == "idea"
    if evidence.get("profile") != receipt.get("workflow"):
        errors.append(f"{slot_id}: workflow evidence profile differs from the slot")
    before = evidence.get("source_inputs_before", [])
    after = evidence.get("source_inputs_after", [])
    frozen_review_inputs = evidence.get("frozen_review_inputs", [])
    if len(before) != len(after):
        errors.append(f"{slot_id}: source input before/after inventories differ")
    for offset, (initial, final) in enumerate(zip(before, after)):
        if _artifact_key(initial, logical_only=idea_logical) != _artifact_key(
            final, logical_only=idea_logical
        ):
            errors.append(f"{slot_id}: source input {offset} changed during the workflow")

    versions = evidence.get("version_artifacts", [])
    evaluations = evidence.get("evaluation_artifacts", [])
    panels = evidence.get("panel_or_compositor_artifacts", [])
    delta = evidence.get("revision_delta")
    state_artifact = evidence.get("state_artifact")
    compositor_verification = evidence.get("compositor_verification_artifact")
    idea_index_artifact = evidence.get("idea_index_artifact")
    current_pointer_artifact = evidence.get("current_pointer_artifact")
    review_contracts: list[
        tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], str]
    ] = []
    stage_artifacts = [
        *versions,
        delta,
        *evaluations,
        *panels,
        *([compositor_verification] if isinstance(compositor_verification, dict) else []),
        *([idea_index_artifact] if isinstance(idea_index_artifact, dict) else []),
        *([current_pointer_artifact] if isinstance(current_pointer_artifact, dict) else []),
        state_artifact,
    ]
    all_artifacts = {
        _artifact_key(artifact, logical_only=idea_logical)
        for artifact in binding.get("artifact_bindings", [])
        if isinstance(artifact, dict)
    }
    workflow_artifacts = [*before, *after, *stage_artifacts]
    private_input_count = len(before) + len(after)
    for offset, artifact in enumerate(workflow_artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"{slot_id}: workflow artifact {offset} is malformed")
            continue
        artifact_path, artifact_errors = _validate_artifact_binding(
            artifact,
            repo_root,
            f"{slot_id}.workflow_evidence.artifact[{offset}]",
            require_digest=not idea_logical,
        )
        errors.extend(artifact_errors)
        errors.extend(
            _validate_private_path(
                artifact_path,
                repo_root,
                f"{slot_id}.workflow_evidence.artifact[{offset}]",
                allow_private_inputs=offset < private_input_count,
            )
        )
        if (
            offset >= private_input_count
            and _artifact_key(artifact, logical_only=idea_logical) not in all_artifacts
        ):
            errors.append(f"{slot_id}: workflow artifact {offset} is absent from receipt artifacts")

    inputs = run_index.get("input_bindings", []) if isinstance(run_index, dict) else []
    outputs = run_index.get("output_bindings", []) if isinstance(run_index, dict) else []
    input_keys = {
        _artifact_key(item, logical_only=idea_logical)
        for item in inputs
        if isinstance(item, dict)
    }
    output_keys = {
        _artifact_key(item, logical_only=idea_logical)
        for item in outputs
        if isinstance(item, dict)
    }
    if not inputs or not outputs:
        errors.append(f"{slot_id}: run-index input/output bindings must both be non-empty")
    for artifact in before:
        if (
            isinstance(artifact, dict)
            and _artifact_key(artifact, logical_only=idea_logical) not in input_keys
        ):
            errors.append(f"{slot_id}: source input is absent from run-index inputs")
    for artifact in stage_artifacts:
        if (
            isinstance(artifact, dict)
            and _artifact_key(artifact, logical_only=idea_logical) not in output_keys
        ):
            errors.append(f"{slot_id}: workflow stage artifact is absent from run-index outputs")
    if any(key not in output_keys for key in all_artifacts):
        errors.append(f"{slot_id}: receipt workflow artifact is absent from run-index outputs")
    if idea_logical and all_artifacts != output_keys:
        errors.append(f"{slot_id}: complete logical artifact index differs from run-index outputs")
    if idea_logical:
        logical_artifacts = [
            artifact
            for artifact in binding.get("artifact_bindings", [])
            if isinstance(artifact, dict)
        ]
        logical_paths = [artifact.get("path") for artifact in logical_artifacts]
        logical_identities = [
            (artifact.get("artifact_id"), artifact.get("version"))
            for artifact in logical_artifacts
        ]
        if len(all_artifacts) != len(logical_artifacts):
            errors.append(f"{slot_id}: complete logical artifact index contains duplicate identities")
        if len(logical_identities) != len(set(logical_identities)):
            errors.append(f"{slot_id}: complete logical artifact index aliases an artifact identity")
        if len(logical_paths) != len(set(logical_paths)):
            errors.append(f"{slot_id}: complete logical artifact index aliases an artifact path")
    for offset, artifact in enumerate(frozen_review_inputs):
        if not isinstance(artifact, dict):
            errors.append(f"{slot_id}: frozen review input {offset} is malformed")
            continue
        path, artifact_errors = _validate_artifact_binding(
            artifact,
            repo_root,
            f"{slot_id}.frozen_review_inputs[{offset}]",
            require_digest=not idea_logical,
        )
        errors.extend(artifact_errors)
        errors.extend(
            _validate_private_path(
                path,
                repo_root,
                f"{slot_id}.frozen_review_inputs[{offset}]",
                allow_private_inputs=True,
            )
        )
        key = _artifact_key(artifact, logical_only=idea_logical)
        if key not in input_keys and key not in output_keys:
            errors.append(f"{slot_id}: frozen review input is absent from run-index bindings")
        if key in output_keys and key not in all_artifacts:
            errors.append(f"{slot_id}: generated frozen review input lacks receipt artifact binding")

    if len(versions) >= 2:
        initial, revised = versions[0], versions[-1]
        same_logical_version = (
            initial.get("path") == revised.get("path")
            or initial.get("version") == revised.get("version")
        )
        same_content_digest = (
            not idea_logical and initial.get("sha256") == revised.get("sha256")
        )
        if same_logical_version or same_content_digest:
            errors.append(f"{slot_id}: revised artifact is not a distinct substantive version")
        delta_path, _ = _validate_artifact_binding(
            delta,
            repo_root,
            f"{slot_id}.workflow_evidence.revision_delta",
            require_digest=not idea_logical,
        )
        if delta_path is not None and len(delta_path.read_text(encoding="utf-8").strip()) < 20:
            errors.append(f"{slot_id}: revision delta is not substantive")
        dossier_frontmatter: dict[str, Any] | None = None
        for label_name, artifact in (("initial", initial), ("revised", revised)):
            artifact_path, _ = _validate_artifact_binding(
                artifact,
                repo_root,
                f"{slot_id}.{label_name}_complete_artifact",
                require_digest=not idea_logical,
            )
            if artifact_path is not None:
                errors.extend(
                    _validate_profile_complete_artifact(
                        str(evidence.get("profile")),
                        artifact_path.read_text(encoding="utf-8").strip(),
                        f"{slot_id}: {label_name}",
                    )
                )
                if idea_logical:
                    current_frontmatter, identity_errors = _validate_idea_dossier_identity(
                        artifact,
                        artifact_path,
                        f"{slot_id}: {label_name}",
                    )
                    errors.extend(identity_errors)
                    if label_name == "revised":
                        dossier_frontmatter = current_frontmatter
        if idea_logical:
            errors.extend(
                _validate_idea_index_and_pointer(
                    evidence,
                    binding,
                    repo_root,
                    revised,
                    dossier_frontmatter,
                )
            )

    actors = binding.get("actor_bindings", [])
    generator_ids = evidence.get("generator_actor_ids", [])
    reviewer_ids = evidence.get("reviewer_actor_ids", [])
    assembler_ids = evidence.get("assembler_actor_ids", [])
    is_polisher = receipt.get("workflow") == "research_polisher"
    referenced_ids = [*generator_ids, *reviewer_ids, *assembler_ids]
    if not is_polisher and len(referenced_ids) != len(set(referenced_ids)):
        errors.append(f"{slot_id}: workflow role actor IDs are not distinct")
    generator_markers = ("assembl",) if is_polisher else ("generat", "draft")
    reviser_markers = ("assembl", "revis") if is_polisher else ("revis",)
    role_requirements = (
        (generator_ids[0] if len(generator_ids) > 0 else None, generator_markers, "generator"),
        (generator_ids[1] if len(generator_ids) > 1 else None, reviser_markers, "reviser"),
        (assembler_ids[0] if assembler_ids else None, ("assembl", "composit", "final"), "finalizer"),
    )
    for actor_id, markers, role_name in role_requirements:
        actor = _actor_by_id(actors, actor_id)
        if actor is None:
            errors.append(f"{slot_id}: {role_name} actor is absent")
        elif not any(marker in str(actor.get("role", "")).lower() for marker in markers):
            errors.append(f"{slot_id}: {role_name} actor role is invalid")
        elif role_name == "finalizer" and _is_reviewer(actor) and actor.get("isolation_mode") != "fresh_subagent":
            errors.append(f"{slot_id}: independent final compositor is not a fresh subagent")
    reviewer_actors = [_actor_by_id(actors, actor_id) for actor_id in reviewer_ids]
    if any(actor is None for actor in reviewer_actors):
        errors.append(f"{slot_id}: referenced reviewer actor is absent")
    reviewer_inventory = set(reviewer_ids) | set(assembler_ids)
    unmapped_reviewers = [
        actor
        for actor in actors
        if isinstance(actor, dict)
        and _is_reviewer(actor)
        and actor.get("actor_id") not in reviewer_inventory
    ]
    if unmapped_reviewers:
        errors.append(f"{slot_id}: reviewer actor is absent from reviewer/assembler inventory")
    for offset, actor in enumerate(actor for actor in reviewer_actors if actor is not None):
        if not _is_reviewer(actor) or actor.get("isolation_mode") != "fresh_subagent":
            errors.append(f"{slot_id}: reviewer actor {offset} is not an independent fresh reviewer")
    forbidden_exact = {
        artifact.get("path")
        for artifact in [delta, *evaluations, *panels]
        if isinstance(artifact, dict)
    }
    for offset, actor in enumerate(actor for actor in reviewer_actors if actor is not None):
        reads = set(actor.get("files_read", []))
        if reads & forbidden_exact or any(Path(path).name.lower() == "readme.md" for path in reads):
            errors.append(f"{slot_id}: reviewer {offset} read delta, prior review, panel, or README evidence")
        if any(
            path not in {artifact.get("path") for artifact in binding.get("artifact_bindings", []) if isinstance(artifact, dict)}
            for path in actor.get("files_written", [])
        ):
            errors.append(f"{slot_id}: reviewer {offset} output lacks artifact binding")

    write_expectations: list[tuple[dict[str, Any] | None, list[Any], str]] = []
    if len(generator_ids) >= 2 and len(versions) >= 2:
        write_expectations.extend(
            [
                (_actor_by_id(actors, generator_ids[0]), [versions[0]], "generator"),
                (_actor_by_id(actors, generator_ids[1]), [versions[-1], delta], "reviser"),
            ]
        )
    if not is_polisher and len(reviewer_actors) >= 4 and len(evaluations) >= 2:
        initial_path = versions[0].get("path") if versions else None
        revised_path = versions[-1].get("path") if versions else None
        valid_reviewers = [actor for actor in reviewer_actors if actor is not None]
        initial_evaluators = [
            actor for actor in valid_reviewers
            if actor.get("review_stage") == "initial_evaluator"
        ]
        fresh_evaluators = [
            actor for actor in valid_reviewers
            if actor.get("review_stage") == "fresh_reevaluator"
        ]
        panel_actors = [
            actor for actor in valid_reviewers
            if actor.get("review_stage") == "panel_reviewer"
        ]
        if len(initial_evaluators) != 1 or len(fresh_evaluators) != 1:
            errors.append(f"{slot_id}: workflow lacks distinct initial and fresh evaluators")
        initial_evaluator = initial_evaluators[0] if len(initial_evaluators) == 1 else None
        fresh_evaluator = fresh_evaluators[0] if len(fresh_evaluators) == 1 else None
        panel_pairs = [
            (artifact, writers[0])
            for artifact in panels
            if isinstance(artifact, dict)
            and len(
                (
                    writers := [
                        actor
                        for actor in panel_actors
                        if artifact.get("path") in actor.get("files_written", [])
                    ]
                )
            ) == 1
        ]
        if len(panel_actors) < 2 or len(panel_pairs) < 2 or len(panels) < 3:
            errors.append(f"{slot_id}: workflow lacks two panel reviewers and a final package")
        expected_reads = [
            (initial_evaluator, initial_path, "initial evaluator"),
            (fresh_evaluator, revised_path, "fresh re-evaluator"),
            *((actor, revised_path, "panel reviewer") for actor in panel_actors),
        ]
        for actor, expected_path, role_name in expected_reads:
            if actor is not None and expected_path not in actor.get("files_read", []):
                errors.append(f"{slot_id}: {role_name} did not read the required complete artifact")
        for actor in [fresh_evaluator, *panel_actors]:
            if actor is not None and initial_path in actor.get("files_read", []):
                errors.append(f"{slot_id}: fresh reviewer read the initial artifact version")
        if initial_evaluator is not None and evaluations[0].get("path") not in initial_evaluator.get("files_written", []):
            errors.append(f"{slot_id}: initial evaluator did not write the initial evaluation artifact")
        if fresh_evaluator is not None and evaluations[-1].get("path") not in fresh_evaluator.get("files_written", []):
            errors.append(f"{slot_id}: fresh re-evaluator did not write the fresh evaluation artifact")
        if initial_evaluator is not None and fresh_evaluator is not None:
            write_expectations.extend(
                [
                    (initial_evaluator, [evaluations[0]], "initial reviewer"),
                    (fresh_evaluator, [evaluations[-1]], "fresh re-evaluator"),
                ]
            )
        for offset, (artifact, actor) in enumerate(panel_pairs[:2]):
            write_expectations.append((actor, [artifact], f"panel reviewer {offset}"))
        artifacts_by_path = {
            artifact.get("path"): artifact
            for artifact in binding.get("artifact_bindings", [])
            if isinstance(artifact, dict)
        }
        readable_artifacts_by_path = {
            artifact.get("path"): artifact
            for artifact in [*before, *versions, *binding.get("artifact_bindings", [])]
            if isinstance(artifact, dict)
        }
        initial_generator = _actor_by_id(actors, generator_ids[0]) if generator_ids else None
        revision_generator = _actor_by_id(actors, generator_ids[1]) if len(generator_ids) > 1 else None
        for actor in valid_reviewers:
            stage = actor.get("review_stage")
            if stage not in {
                "supporting_pre_generation",
                "supporting_historical",
                "supporting_qualifying",
            }:
                continue
            reads = set(actor.get("files_read", []))
            writes = actor.get("files_written", [])
            if len(writes) != 1:
                errors.append(f"{slot_id}: {stage} reviewer must write exactly one report")
                continue
            report_path = writes[0]
            if stage == "supporting_pre_generation":
                if reads & {initial_path, revised_path}:
                    errors.append(f"{slot_id}: supporting_pre_generation reviewer read a version artifact")
                if initial_generator is None or report_path not in initial_generator.get("files_read", []):
                    errors.append(f"{slot_id}: pre-generation supporting report was not read by the initial generator")
            elif stage == "supporting_historical":
                if initial_path not in reads or revised_path in reads:
                    errors.append(f"{slot_id}: supporting_historical reviewer must read v001 and not v002")
                if revision_generator is None or report_path not in revision_generator.get("files_read", []):
                    errors.append(f"{slot_id}: historical supporting report was not read by the reviser")
            elif revised_path not in reads or initial_path in reads:
                errors.append(f"{slot_id}: supporting_qualifying reviewer must read v002 and not v001")
        for offset, actor in enumerate(valid_reviewers):
            reads = set(actor.get("files_read", []))
            if actor is initial_evaluator and (initial_path not in reads or revised_path in reads):
                errors.append(f"{slot_id}: initial evaluator does not bind only the initial complete version")
            if actor in [fresh_evaluator, *panel_actors] and (
                revised_path not in reads or initial_path in reads
            ):
                errors.append(f"{slot_id}: reviewer {offset} does not bind only the qualifying complete version")
            reviewed_artifacts = [
                readable_artifacts_by_path[path]
                for path in actor.get("files_read", [])
                if path in readable_artifacts_by_path
            ]
            if not reviewed_artifacts:
                errors.append(f"{slot_id}: supporting reviewer reads no bound artifact")
            reports = [
                artifacts_by_path[path]
                for path in actor.get("files_written", [])
                if path in artifacts_by_path
            ]
            if len(reports) != 1:
                errors.append(f"{slot_id}: reviewer {offset} must write exactly one typed report artifact")
                continue
            if reviewed_artifacts:
                review_contracts.append(
                    (actor, reports[0], reviewed_artifacts, f"reviewer {offset}")
                )
    if assembler_ids and panels:
        finalizer_artifacts = [panels[-1], state_artifact]
        if idea_logical:
            finalizer_artifacts.extend([idea_index_artifact, current_pointer_artifact])
        write_expectations.append(
            (_actor_by_id(actors, assembler_ids[0]), finalizer_artifacts, "finalizer")
        )
    for actor, artifacts, role_name in write_expectations:
        if actor is None:
            continue
        written = set(actor.get("files_written", []))
        for artifact in artifacts:
            if isinstance(artifact, dict) and artifact.get("path") not in written:
                errors.append(f"{slot_id}: {role_name} did not write its bound artifact")

    if evidence.get("fresh_evaluation_rounds", 0) < 2:
        errors.append(f"{slot_id}: workflow lacks initial and fresh re-evaluation rounds")
    if evidence.get("dissent_preserved") is not True:
        errors.append(f"{slot_id}: workflow does not preserve dissent")
    if evidence.get("terminal_state") != receipt.get("actual_outcome"):
        errors.append(f"{slot_id}: workflow terminal state differs from actual outcome")
    trace = evidence.get("status_trace", [])
    if not trace or trace[-1] != evidence.get("terminal_state"):
        errors.append(f"{slot_id}: workflow state trace does not reach the terminal state")
    state_path, _ = _validate_artifact_binding(
        state_artifact,
        repo_root,
        f"{slot_id}.workflow_evidence.state_artifact",
        require_digest=not idea_logical,
    )
    if state_path is not None:
        state, state_errors = _load_structured_file(state_path, f"{slot_id}.state_artifact")
        errors.extend(state_errors)
        if state is not None:
            expected_state = {
                "terminal_state": evidence.get("terminal_state"),
                "status_trace": trace,
                "dissent_preserved": True,
                "source_inputs_modified": False,
            }
            for field, expected in expected_state.items():
                if state.get(field) != expected:
                    errors.append(f"{slot_id}: state artifact {field} differs from receipt")

    matrix = evidence.get("polisher_matrix")
    if is_polisher:
        raw_paths = {
            path
            for artifact in before
            if isinstance(artifact, dict)
            and (path := _normalized_artifact_path(artifact, repo_root)) is not None
        }
        frozen_paths = {
            path
            for artifact in frozen_review_inputs
            if isinstance(artifact, dict)
            and (path := _normalized_artifact_path(artifact, repo_root)) is not None
        }
        if raw_paths & frozen_paths:
            errors.append(f"{slot_id}: Research Polisher dossier is incorrectly registered as raw source input")
        semantic_artifacts = [
            artifact
            for artifact in [
                *before,
                *after,
                *frozen_review_inputs,
                *versions,
                delta,
                *evaluations,
                *panels,
                compositor_verification,
                state_artifact,
            ]
            if isinstance(artifact, dict)
        ]
        identity_paths: dict[tuple[Any, Any], set[str]] = {}
        path_identities: dict[str, set[tuple[Any, Any]]] = {}
        for artifact in semantic_artifacts:
            normalized = _normalized_artifact_path(artifact, repo_root)
            identity = (artifact.get("artifact_id"), artifact.get("version"))
            if normalized is None:
                continue
            identity_paths.setdefault(identity, set()).add(normalized)
            path_identities.setdefault(normalized, set()).add(identity)
        if any(len(paths) > 1 for paths in identity_paths.values()):
            errors.append(f"{slot_id}: artifact identity aliases multiple normalized paths")
        if any(len(identities) > 1 for identities in path_identities.values()):
            errors.append(f"{slot_id}: normalized artifact path aliases multiple identities")
        if not isinstance(matrix, dict):
            errors.append(f"{slot_id}: Research Polisher matrix evidence is missing")
        else:
            expected_perspectives = {
                "scientific_significance",
                "practical_value",
                "dissemination_editorial",
            }
            expected_tiers = {"reposition_only", "small_extension", "moderate_extension"}
            perspectives = set(matrix.get("perspectives", []))
            tiers = set(matrix.get("tier_ids", []))
            cells = matrix.get("cells", [])
            combinations = {
                (cell.get("perspective"), cell.get("tier"))
                for cell in cells
                if isinstance(cell, dict)
            }
            if perspectives != expected_perspectives or tiers != expected_tiers:
                errors.append(f"{slot_id}: Research Polisher perspectives or tiers are incomplete")
            if combinations != {(p, t) for p in expected_perspectives for t in expected_tiers}:
                errors.append(f"{slot_id}: Research Polisher 3x3 matrix is incomplete")
            if any(
                not isinstance(cell, dict)
                or not _substantive_section(str(cell.get("content_summary", "")))
                for cell in cells
            ):
                errors.append(f"{slot_id}: Research Polisher matrix contains a placeholder option")
            strategist_ids = matrix.get("initial_strategist_instance_ids", [])
            strategist_actors = [_actor_by_instance(actors, instance) for instance in strategist_ids]
            if len(set(strategist_ids)) != 3 or any(actor is None for actor in strategist_actors):
                errors.append(f"{slot_id}: Research Polisher lacks three distinct strategists")
            for actor in (actor for actor in strategist_actors if actor is not None):
                if actor.get("isolation_mode") != "fresh_subagent":
                    errors.append(f"{slot_id}: Research Polisher strategist is not fresh")
                if actor.get("review_stage") != "strategist_initial":
                    errors.append(f"{slot_id}: Research Polisher strategist review_stage is invalid")
            revision_instance = matrix.get("revision_strategist_instance_id")
            initial_final_instance = matrix.get("initial_final_reviewer_instance_id")
            fresh_final_instance = matrix.get("fresh_final_reviewer_instance_id")
            isolated_instances = [
                *strategist_ids,
                revision_instance,
                initial_final_instance,
                fresh_final_instance,
            ]
            if len(isolated_instances) != len(set(isolated_instances)):
                errors.append(f"{slot_id}: Research Polisher reused a strategist or final reviewer")
            revision_actor = _actor_by_instance(actors, revision_instance)
            initial_final_actor = _actor_by_instance(actors, initial_final_instance)
            fresh_final_actor = _actor_by_instance(actors, fresh_final_instance)
            for role_name, actor in (
                ("revision strategist", revision_actor),
                ("initial final reviewer", initial_final_actor),
                ("fresh final reviewer", fresh_final_actor),
            ):
                if actor is None or actor.get("isolation_mode") != "fresh_subagent":
                    errors.append(f"{slot_id}: Research Polisher {role_name} is not fresh")
            if revision_actor is not None and revision_actor.get("review_stage") != "strategist_revision":
                errors.append(f"{slot_id}: Research Polisher revision strategist review_stage is invalid")
            if initial_final_actor is not None and initial_final_actor.get("review_stage") != "polisher_initial_final":
                errors.append(f"{slot_id}: Research Polisher initial final reviewer review_stage is invalid")
            if fresh_final_actor is not None and fresh_final_actor.get("review_stage") != "polisher_fresh_final":
                errors.append(f"{slot_id}: Research Polisher fresh final reviewer review_stage is invalid")
            if initial_final_actor is not None and not _is_reviewer(initial_final_actor):
                errors.append(f"{slot_id}: Research Polisher initial final reviewer role is invalid")
            if fresh_final_actor is not None and not _is_reviewer(fresh_final_actor):
                errors.append(f"{slot_id}: Research Polisher fresh final reviewer role is invalid")
            required_reviewer_actor_ids = {
                actor.get("actor_id")
                for actor in [*strategist_actors, revision_actor, initial_final_actor, fresh_final_actor]
                if actor is not None
            }
            if not required_reviewer_actor_ids.issubset(set(reviewer_ids)):
                errors.append(f"{slot_id}: Research Polisher reviewer inventory is incomplete")
            dossier_paths = {
                artifact.get("path")
                for artifact in frozen_review_inputs
                if isinstance(artifact, dict)
            }
            initial_path = versions[0].get("path") if versions else None
            revised_path = versions[-1].get("path") if versions else None
            for actor in (actor for actor in strategist_actors if actor is not None):
                if not dossier_paths.issubset(set(actor.get("files_read", []))):
                    errors.append(f"{slot_id}: Research Polisher strategist did not read the frozen dossier")
            if revision_actor is not None and not dossier_paths.issubset(set(revision_actor.get("files_read", []))):
                errors.append(f"{slot_id}: Research Polisher revision strategist did not read the frozen dossier")
            if initial_final_actor is not None and initial_path not in initial_final_actor.get("files_read", []):
                errors.append(f"{slot_id}: initial final reviewer did not read the initial portfolio")
            if fresh_final_actor is not None:
                if revised_path not in fresh_final_actor.get("files_read", []):
                    errors.append(f"{slot_id}: fresh final reviewer did not read the revised portfolio")
                if initial_path in fresh_final_actor.get("files_read", []):
                    errors.append(f"{slot_id}: fresh final reviewer read the prior portfolio")
            polisher_writes = [
                (initial_final_actor, evaluations[0] if evaluations else None, "initial final reviewer"),
                (fresh_final_actor, evaluations[-1] if evaluations else None, "fresh final reviewer"),
            ]
            for actor, artifact, role_name in polisher_writes:
                if actor is not None and isinstance(artifact, dict) and artifact.get("path") not in actor.get("files_written", []):
                    errors.append(f"{slot_id}: {role_name} did not write its evaluation")
            known_artifact_ids = {
                artifact.get("artifact_id")
                for artifact in binding.get("artifact_bindings", [])
                if isinstance(artifact, dict)
            }
            if any(
                isinstance(cell, dict) and cell.get("artifact_id") not in known_artifact_ids
                for cell in cells
            ):
                errors.append(f"{slot_id}: Research Polisher cell lacks bound provenance")
            artifact_by_id = {
                artifact.get("artifact_id"): artifact
                for artifact in binding.get("artifact_bindings", [])
                if isinstance(artifact, dict)
            }
            strategy_report_paths: set[str] = set()
            for perspective, actor in zip(matrix.get("perspectives", []), strategist_actors):
                if actor is None:
                    continue
                paths = {
                    artifact_by_id[cell.get("artifact_id")].get("path")
                    for cell in cells
                    if isinstance(cell, dict)
                    and cell.get("perspective") == perspective
                    and cell.get("artifact_id") in artifact_by_id
                }
                strategy_report_paths.update(path for path in paths if isinstance(path, str))
                if paths and not paths.issubset(set(actor.get("files_written", []))):
                    errors.append(f"{slot_id}: Research Polisher strategist provenance is incomplete")
            initial_assembler = _actor_by_id(actors, generator_ids[0]) if generator_ids else None
            revision_assembler = _actor_by_id(actors, generator_ids[1]) if len(generator_ids) > 1 else None
            if initial_assembler is not None and not strategy_report_paths.issubset(
                set(initial_assembler.get("files_read", []))
            ):
                errors.append(f"{slot_id}: initial assembler did not read all strategist reports")
            revision_report_paths = set(revision_actor.get("files_written", [])) if revision_actor else set()
            if revision_assembler is not None and not revision_report_paths.issubset(
                set(revision_assembler.get("files_read", []))
            ):
                errors.append(f"{slot_id}: revision assembler did not read the revision strategist report")
            artifacts_by_path = {
                artifact.get("path"): artifact
                for artifact in binding.get("artifact_bindings", [])
                if isinstance(artifact, dict)
            }
            dossier_artifacts = [
                artifact for artifact in frozen_review_inputs if isinstance(artifact, dict)
            ]
            for offset, actor in enumerate(actor for actor in strategist_actors if actor is not None):
                report = next(
                    (
                        artifacts_by_path.get(path)
                        for path in actor.get("files_written", [])
                        if artifacts_by_path.get(path) is not None
                    ),
                    None,
                )
                if isinstance(report, dict) and dossier_artifacts:
                    review_contracts.append(
                        (actor, report, dossier_artifacts, f"strategist {offset}")
                    )
            revision_report = next(
                (
                    artifacts_by_path.get(path)
                    for path in revision_actor.get("files_written", [])
                    if artifacts_by_path.get(path) is not None
                ),
                None,
            ) if revision_actor else None
            if revision_actor is not None and isinstance(revision_report, dict) and dossier_artifacts:
                review_contracts.append(
                    (revision_actor, revision_report, dossier_artifacts, "revision strategist")
                )
            if initial_final_actor is not None and evaluations and versions:
                review_contracts.append(
                    (
                        initial_final_actor,
                        evaluations[0],
                        [versions[0]],
                        "initial final reviewer",
                    )
                )
            if fresh_final_actor is not None and evaluations and versions:
                review_contracts.append(
                    (
                        fresh_final_actor,
                        evaluations[-1],
                        [versions[-1]],
                        "fresh final reviewer",
                    )
                )
    elif matrix is not None:
        errors.append(f"{slot_id}: non-Polisher workflow carries Polisher matrix evidence")
    typed_assembler_ids: set[str] = set()
    artifacts_by_path = {
        artifact.get("path"): artifact
        for artifact in binding.get("artifact_bindings", [])
        if isinstance(artifact, dict)
    }
    for assembler_id in assembler_ids:
        assembler = _actor_by_id(actors, assembler_id)
        if assembler is None or not _is_reviewer(assembler):
            continue
        typed_assembler_ids.add(assembler_id)
        if assembler.get("review_stage") != "final_verifier":
            errors.append(f"{slot_id}: independent compositor review_stage is invalid")
        if not isinstance(compositor_verification, dict):
            errors.append(
                f"{slot_id}: independent compositor lacks explicit verification artifact"
            )
            continue
        if compositor_verification.get("path") not in assembler.get("files_written", []):
            errors.append(f"{slot_id}: independent compositor did not write its explicit verification artifact")
        revised_path = versions[-1].get("path") if versions else None
        if revised_path not in assembler.get("files_read", []):
            errors.append(f"{slot_id}: independent compositor did not read the qualifying artifact")
        readable = {
            artifact.get("path"): artifact
            for artifact in [*before, *versions, *binding.get("artifact_bindings", [])]
            if isinstance(artifact, dict)
        }
        reviewed_artifacts = [
            readable[path]
            for path in assembler.get("files_read", [])
            if path in readable
        ]
        if reviewed_artifacts:
            review_contracts.append(
                (
                    assembler,
                    compositor_verification,
                    reviewed_artifacts,
                    "independent compositor",
                )
            )
    if isinstance(compositor_verification, dict) and not typed_assembler_ids:
        errors.append(f"{slot_id}: compositor verification artifact lacks an independent compositor")
    contracted_reviewer_ids = {
        actor.get("actor_id")
        for actor, _report, _artifacts, _role_name in review_contracts
    }
    missing_contracts = (set(reviewer_ids) | typed_assembler_ids) - contracted_reviewer_ids
    if missing_contracts:
        errors.append(f"{slot_id}: reviewer inventory lacks typed report coverage")
    visible_dissent: list[Any] = []
    for actor, report, reviewed_artifacts, role_name in review_contracts:
        if not reviewed_artifacts:
            errors.append(f"{slot_id}: {role_name} reviewed artifact binding is missing")
            continue
        report_errors, dissent = _validate_review_report(
            report,
            actor,
            reviewed_artifacts,
            slot_id,
            receipt.get("actual_outcome") in READY_STATES,
            repo_root,
            f"{slot_id}.{role_name}.review_report",
            require_digest=not idea_logical,
        )
        errors.extend(report_errors)
        visible_dissent.extend(dissent)
    if visible_dissent and panels:
        final_path, _ = _validate_artifact_binding(
            panels[-1],
            repo_root,
            f"{slot_id}.final_package",
            require_digest=not idea_logical,
        )
        final_text = final_path.read_text(encoding="utf-8") if final_path is not None else ""
        if any(str(item) not in final_text for item in visible_dissent):
            errors.append(f"{slot_id}: reviewer dissent is absent from the final package")
    return errors


def _validate_source_identity(
    source: Any,
    repo_root: Path,
    plugin_root: Path,
    plugin_version: str,
    label: str,
) -> list[str]:
    if not isinstance(source, dict):
        return [f"{label}: source identity is missing"]
    errors: list[str] = []
    git_commit = source.get("git_commit")
    if not isinstance(git_commit, str) or not GIT_COMMIT.fullmatch(git_commit):
        errors.append(f"{label}: git_commit is malformed")
    else:
        try:
            if git_commit != _git_head(repo_root):
                errors.append(f"{label}: git_commit differs from repository HEAD")
        except (OSError, subprocess.CalledProcessError):
            errors.append(f"{label}: repository HEAD cannot be resolved")
    if source.get("marketplace_revision") != git_commit:
        errors.append(f"{label}: marketplace revision differs from git_commit")

    marketplace_value = source.get("marketplace_metadata_path")
    marketplace_path = (
        Path(marketplace_value).expanduser().resolve()
        if isinstance(marketplace_value, str)
        else None
    )
    marketplace: dict[str, Any] | None = None
    if marketplace_path is None or not marketplace_path.is_file():
        errors.append(f"{label}: marketplace metadata file does not exist")
    else:
        if source.get("marketplace_metadata_sha256") != raw_file_sha256(marketplace_path):
            errors.append(f"{label}: marketplace metadata SHA-256 differs from file bytes")
        try:
            marketplace = load_json(marketplace_path)
        except (OSError, ValueError, json.JSONDecodeError):
            errors.append(f"{label}: marketplace metadata cannot be read")
    if marketplace is not None:
        if marketplace.get("revision") != source.get("marketplace_revision"):
            errors.append(f"{label}: marketplace metadata revision differs")
        if marketplace.get("source") != source.get("marketplace_source"):
            errors.append(f"{label}: marketplace metadata source differs")
        if marketplace.get("ref_name") != source.get("marketplace_ref"):
            errors.append(f"{label}: marketplace metadata ref differs")
        if marketplace.get("source_type") != "git":
            errors.append(f"{label}: marketplace metadata is not Git-backed")
    if source.get("marketplace_source") != "https://github.com/xuxu-wei/research-skills.git":
        errors.append(f"{label}: marketplace source is not the approved personal repository")
    if source.get("marketplace_ref") != "main":
        errors.append(f"{label}: marketplace ref is not main")

    configured_home = os.environ.get("CODEX_HOME")
    active_codex_home = (
        Path(configured_home).expanduser().resolve()
        if configured_home
        else (Path.home() / ".codex").resolve()
    )
    config_value = source.get("config_path")
    config_path = Path(config_value).expanduser().resolve() if isinstance(config_value, str) else None
    if config_path != (active_codex_home / "config.toml").resolve():
        errors.append(f"{label}: config_path is not the active CODEX_HOME config.toml")
    config: dict[str, Any] | None = None
    if config_path is None or not config_path.is_file():
        errors.append(f"{label}: Codex config file does not exist")
    else:
        if source.get("config_sha256") != raw_file_sha256(config_path):
            errors.append(f"{label}: Codex config SHA-256 differs from file bytes")
        try:
            with config_path.open("rb") as handle:
                config = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError):
            errors.append(f"{label}: Codex config cannot be parsed")
    if config is not None and config.get("model") != source.get("model"):
        errors.append(f"{label}: configured model differs from source identity")

    manifest = plugin_root / ".codex-plugin" / "plugin.json"
    registry = plugin_root / "workflow-registry.yaml"
    source_expected = {
        "manifest_sha256": file_sha256(manifest),
        "registry_sha256": file_sha256(registry),
        "skill_tree_sha256": skill_tree_sha256(plugin_root / "skills"),
    }
    for field, expected in source_expected.items():
        if source.get(field) != expected:
            errors.append(f"{label}: {field} differs from the repository")
    installable_paths = [
        str((plugin_root / ".codex-plugin" / "plugin.json").relative_to(repo_root)),
        str((plugin_root / "workflow-registry.yaml").relative_to(repo_root)),
        str((plugin_root / "skills").relative_to(repo_root)),
    ]
    dirty = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *installable_paths],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *installable_paths],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if dirty.returncode != 0 or untracked.stdout.strip():
        errors.append(f"{label}: installable plugin tree has uncommitted changes")

    cache_value = source.get("installed_cache_path")
    cache = Path(cache_value).expanduser().resolve() if isinstance(cache_value, str) else None
    if cache is None or not cache.is_dir():
        errors.append(f"{label}: installed cache directory does not exist")
    else:
        cache_manifest = cache / ".codex-plugin" / "plugin.json"
        cache_registry = cache / "workflow-registry.yaml"
        cache_skills = cache / "skills"
        if not cache_manifest.is_file() or not cache_registry.is_file() or not cache_skills.is_dir():
            errors.append(f"{label}: installed cache is not a complete plugin")
        else:
            installed_expected = {
                "installed_manifest_sha256": file_sha256(cache_manifest),
                "installed_registry_sha256": file_sha256(cache_registry),
                "installed_skill_tree_sha256": skill_tree_sha256(cache_skills),
            }
            for field, expected in installed_expected.items():
                if source.get(field) != expected:
                    errors.append(f"{label}: {field} differs from installed cache")
            paired = (
                ("manifest_sha256", "installed_manifest_sha256"),
                ("registry_sha256", "installed_registry_sha256"),
                ("skill_tree_sha256", "installed_skill_tree_sha256"),
            )
            for source_field, installed_field in paired:
                if source.get(source_field) != source.get(installed_field):
                    errors.append(f"{label}: source and installed {source_field} differ")
            try:
                if load_json(cache_manifest).get("version") != plugin_version:
                    errors.append(f"{label}: installed cache plugin version differs")
            except (OSError, ValueError, json.JSONDecodeError):
                errors.append(f"{label}: installed manifest cannot be read")
    if config_path is not None:
        codex_home = active_codex_home
        expected_cache = (
            codex_home
            / "plugins"
            / "cache"
            / "xuxu-research-preview"
            / "research-skills-openai"
            / plugin_version
        ).resolve()
        if cache is not None and cache != expected_cache:
            errors.append(f"{label}: installed cache path differs from the personal plugin cache")
        if marketplace_path is not None and not marketplace_path.is_relative_to(codex_home):
            errors.append(f"{label}: marketplace metadata is outside the config CODEX_HOME")

    cli_value = source.get("cli_path")
    cli = Path(cli_value).expanduser().resolve() if isinstance(cli_value, str) else None
    active_cli_value = shutil.which("codex")
    active_cli = Path(active_cli_value).resolve() if active_cli_value else None
    if active_cli is None:
        errors.append(f"{label}: active Codex CLI cannot be resolved from PATH")
    elif cli != active_cli:
        errors.append(f"{label}: CLI path is not the active Codex CLI from PATH")
    if source.get("cli_version") != APPROVED_CODEX_CLI_VERSION:
        errors.append(f"{label}: CLI version differs from the approved frozen version")
    if cli is None or not cli.is_file():
        errors.append(f"{label}: CLI path does not exist")
    else:
        cli_digest = source.get("cli_sha256")
        if not isinstance(cli_digest, str) or not SHA256.fullmatch(cli_digest):
            errors.append(f"{label}: CLI SHA-256 is malformed")
        elif raw_file_sha256(cli) != cli_digest:
            errors.append(f"{label}: CLI SHA-256 differs from executable bytes")
        try:
            if source.get("cli_version") != _query_cli_version(cli):
                errors.append(f"{label}: CLI --version output differs from source identity")
        except (OSError, subprocess.SubprocessError, ValueError):
            errors.append(f"{label}: CLI --version could not be executed")
    for field in ("cli_version", "model"):
        if not isinstance(source.get(field), str) or not source[field].strip():
            errors.append(f"{label}: {field} is missing")
    return errors


def deterministic_checks() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    schema = load_yaml(SCHEMA)
    run_index_schema = load_yaml(RUN_INDEX_SCHEMA)
    if schema.get("$id") != "openai-personal-owner-observed-receipts/v2":
        errors.append("personal owner-observed receipt schema ID is invalid")
    if run_index_schema.get("$id") != "openai-personal-runtime-run-index/v1":
        errors.append("personal runtime run-index schema ID is invalid")
    try:
        Draft202012Validator.check_schema(schema)
        Draft202012Validator.check_schema(run_index_schema)
    except SchemaError as exc:
        errors.append(f"personal JSON Schema is invalid: {exc.message}")

    manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
    registry_path = PLUGIN / "workflow-registry.yaml"
    manifest = load_json(manifest_path)
    registry = load_yaml(registry_path)
    plugin_version = str(manifest.get("version", ""))
    if registry.get("plugin_version") != plugin_version:
        errors.append("manifest and workflow registry versions differ")

    skills = registry.get("skills", [])
    if not isinstance(skills, list) or len(skills) != 50:
        errors.append("registry must contain exactly 50 skills")
        skills = []
    reviewer_count = sum(
        1
        for item in skills
        if isinstance(item, dict) and item.get("requires_independent_subagent") is True
    )
    if reviewer_count != 21:
        errors.append(f"registry must contain 21 independent reviewers, found {reviewer_count}")

    policy = registry.get("public_entry_policy", {})
    declared = set(policy.get("declared_entries", [])) if isinstance(policy, dict) else set()
    implicit = set(policy.get("implicit_active_entries", [])) if isinstance(policy, dict) else set()
    if declared != EXPECTED_DECLARED:
        errors.append("declared entry set differs from the personal profile")
    if implicit != EXPECTED_IMPLICIT:
        errors.append("implicit entry set differs from the fixed personal profile")
    explicit_only = policy.get("explicit_only_entries", {}) if isinstance(policy, dict) else {}
    polisher = explicit_only.get("research-polisher-orchestrator", {}) if isinstance(explicit_only, dict) else {}
    if (
        not isinstance(polisher, dict)
        or polisher.get("status") != "explicit_only_personal_routing_policy"
        or polisher.get("change_authority") != "owner_only"
    ):
        errors.append("Research Polisher is not fixed to the owner-only explicit routing policy")

    edges = registry.get("workflow_edges", [])
    workflows = {
        item.get("workflow")
        for item in edges
        if isinstance(item, dict) and isinstance(item.get("workflow"), str)
    }
    if workflows != EXPECTED_WORKFLOWS:
        errors.append("registry workflow set differs from the five personal workflows")

    phase4 = load_json(PLUGIN / "reports" / "phase4-scenario-results.json")
    phase7 = load_json(PLUGIN / "reports" / "phase7-mode-results.json")
    phase8 = load_json(PLUGIN / "reports" / "phase8-corpus-results.json")
    for label, report in (("phase4", phase4), ("phase7", phase7), ("phase8", phase8)):
        if report.get("plugin_version") != plugin_version:
            errors.append(f"{label} report version differs from the plugin")

    p4 = phase4.get("summary", {})
    if p4.get("workflows_passed") != 5 or p4.get("negative_guards_rejected") != 63:
        errors.append("Phase 4 deterministic baseline must remain 5 workflows and 63 negatives")

    p7 = phase7.get("summary", {})
    if (
        p7.get("declared_entry_modes") != 17
        or p7.get("positive_modes_passed") != 17
        or p7.get("false_ready_count") != 0
        or p7.get("runtime_contract_complete_workflows_verified") != 5
    ):
        errors.append("Phase 7 deterministic baseline must remain 17/17 modes, five workflows, false-ready zero")

    corpus = phase8.get("corpus", {})
    metrics = corpus.get("metrics", {}) if isinstance(corpus, dict) else {}
    required_metrics = (
        "dissent_preservation_percent",
        "fatal_or_blocking_finding_recall_percent",
        "lineage_compliance_percent",
        "major_finding_recall_percent",
        "reviewer_edit_boundary_compliance_percent",
        "reviewer_isolation_compliance_percent",
    )
    if corpus.get("case_count") != 20 or metrics.get("false_ready_count") != 0:
        errors.append("Phase 8 corpus must remain 20 cases with false-ready zero")
    if any(metrics.get(name) != 100.0 for name in required_metrics):
        errors.append("Phase 8 personal quality metrics must remain at 100 percent")

    return (
        {
            "plugin_version": plugin_version,
            "manifest_sha256": file_sha256(manifest_path),
            "registry_sha256": file_sha256(registry_path),
            "receipt_schema_sha256": file_sha256(SCHEMA),
            "run_index_schema_sha256": file_sha256(RUN_INDEX_SCHEMA),
            "skill_tree_sha256": skill_tree_sha256(PLUGIN / "skills"),
            "skill_count": len(skills),
            "independent_reviewer_count": reviewer_count,
            "declared_entry_count": len(declared),
            "implicit_entry_count": len(implicit),
            "workflow_count": len(workflows),
            "entry_mode_count": p7.get("declared_entry_modes"),
            "phase4_workflows_passed": p4.get("workflows_passed"),
            "phase4_negative_guards_rejected": p4.get("negative_guards_rejected"),
            "phase8_case_count": corpus.get("case_count"),
            "phase8_false_ready_count": metrics.get("false_ready_count"),
        },
        errors,
    )


def _validate_actor_paths(actor: dict[str, Any], repo_root: Path, label: str) -> list[str]:
    errors: list[str] = []
    for field in ("files_read", "files_written"):
        values = actor.get(field, [])
        if not isinstance(values, list):
            continue
        for offset, value in enumerate(values):
            path, path_errors = _resolve_repo_file(repo_root, value, f"{label}.{field}[{offset}]")
            errors.extend(path_errors)
            if field == "files_written":
                errors.extend(
                    _validate_private_path(path, repo_root, f"{label}.{field}[{offset}]")
                )
    is_reviewer = _is_reviewer(actor)
    review_stage = actor.get("review_stage")
    if not is_reviewer:
        if review_stage != "not_applicable":
            errors.append(f"{label}: non-reviewer review_stage must be not_applicable")
        return errors
    if review_stage not in REVIEW_STAGES:
        errors.append(f"{label}: reviewer review_stage is not a recognized reviewer stage")
    if actor.get("isolation_mode") != "fresh_subagent":
        errors.append(f"{label}: reviewer is not a fresh subagent")
    for field in (
        "prior_scores_visible",
        "prior_versions_visible",
        "revision_delta_visible",
        "source_edits_performed",
    ):
        if actor.get(field) is not False:
            errors.append(f"{label}: reviewer isolation flag {field} must be false")
    read_paths = [str(path).lower() for path in actor.get("files_read", [])]
    if any(marker in path for path in read_paths for marker in FORBIDDEN_REVIEW_INPUT_MARKERS):
        errors.append(f"{label}: reviewer read forbidden prior/delta/navigation material")
    writes = [str(path).lower() for path in actor.get("files_written", [])]
    if not writes:
        errors.append(f"{label}: reviewer wrote no evaluation or verification report")
    skill = str(actor.get("skill", "")).lower()
    allowed_markers = REVIEW_OUTPUT_MARKERS
    if "compositor" in skill:
        allowed_markers = allowed_markers + ("package", "manifest", "index", "final")
    if writes and any(not any(marker in path for marker in allowed_markers) for path in writes):
        errors.append(f"{label}: reviewer wrote outside evaluation/verification report paths")
    return errors


def _validate_run_index(
    binding: dict[str, Any],
    runtime: dict[str, Any],
    repo_root: Path,
    run_index_validator: Draft202012Validator,
    label: str,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    workflow_evidence = binding.get("workflow_evidence")
    idea_logical = (
        isinstance(workflow_evidence, dict)
        and workflow_evidence.get("profile") == "idea"
    )
    run_index_path, file_errors = _validate_file_binding(
        runtime.get("run_index"), repo_root, f"{label}.runtime_evidence.run_index"
    )
    errors.extend(file_errors)
    errors.extend(_validate_private_path(run_index_path, repo_root, f"{label}.run_index"))
    if run_index_path is None:
        return None, [], errors
    try:
        run_index = load_yaml(run_index_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return None, [], errors + [f"{label}: run-index cannot be read: {exc}"]
    errors.extend(_validator_errors(run_index, run_index_validator, f"{label}.run_index"))

    for field in (
        "slot_id",
        "task_id",
        "session_id",
        "plugin_version",
        "source_identity",
        "started_at",
        "completed_at",
    ):
        expected = binding.get(field) if field != "slot_id" else label
        if run_index.get(field) != expected:
            errors.append(f"{label}: run-index {field} differs from receipt")
    if run_index.get("exit_code") != runtime.get("exit_code"):
        errors.append(f"{label}: run-index exit_code differs from receipt")
    command = run_index.get("command", {})
    cwd_value = command.get("cwd") if isinstance(command, dict) else None
    if not isinstance(cwd_value, str):
        errors.append(f"{label}: run-index cwd is missing")
    else:
        cwd = Path(cwd_value)
        cwd = cwd.resolve() if cwd.is_absolute() else (repo_root / cwd).resolve()
        if not cwd.is_relative_to(repo_root.resolve()) or not cwd.is_dir():
            errors.append(f"{label}: run-index cwd is outside the repository or missing")

    files = run_index.get("files", {})
    for field in ("prompt", "jsonl", "stderr", "final_message"):
        if not isinstance(files, dict) or files.get(field) != runtime.get(field):
            errors.append(f"{label}: run-index {field} binding differs from receipt")
    if run_index.get("actor_bindings") != binding.get("actor_bindings"):
        errors.append(f"{label}: run-index actor bindings differ from receipt")

    for group in ("input_bindings", "output_bindings"):
        values = run_index.get(group, [])
        if isinstance(values, list):
            keys = [
                _artifact_key(value, logical_only=idea_logical)
                for value in values
                if isinstance(value, dict)
            ]
            if len(keys) != len(set(keys)):
                errors.append(f"{label}: run-index {group} contains duplicate artifact bindings")
            for offset, value in enumerate(values):
                path, item_errors = _validate_artifact_binding(
                    value,
                    repo_root,
                    f"{label}.run_index.{group}[{offset}]",
                    require_digest=not idea_logical,
                )
                errors.extend(item_errors)
                errors.extend(
                    _validate_private_path(
                        path,
                        repo_root,
                        f"{label}.run_index.{group}[{offset}]",
                        allow_private_inputs=group == "input_bindings",
                    )
                )
    jsonl_binding = runtime.get("jsonl")
    jsonl_path, _ = _validate_file_binding(jsonl_binding, repo_root, f"{label}.runtime_evidence.jsonl")
    events: list[dict[str, Any]] = []
    if jsonl_path is not None:
        events, jsonl_errors = _load_jsonl(jsonl_path, f"{label}.runtime_evidence.jsonl")
        errors.extend(jsonl_errors)
    thread_events = [event for event in events if _event_kind(event).startswith("thread.started")]
    if not thread_events:
        errors.append(f"{label}: Codex JSONL lacks thread.started")
    elif not any(event.get("thread_id") == binding.get("session_id") for event in thread_events):
        errors.append(f"{label}: thread.started does not identify the receipt session")
    completed = [event for event in events if _event_kind(event).startswith("turn.completed")]
    if not completed:
        errors.append(f"{label}: Codex JSONL lacks turn.completed")

    summary = run_index.get("event_summary", {})
    event_ids = {_event_id(event) for event in events if _event_id(event)}
    if isinstance(summary, dict):
        thread_id = summary.get("thread_started_event_id")
        if thread_id not in event_ids:
            errors.append(f"{label}: summarized thread.started event is absent from JSONL")
        for field in ("turn_completed_event_ids", "web_search_event_ids"):
            values = summary.get(field, [])
            if isinstance(values, list) and any(value not in event_ids for value in values):
                errors.append(f"{label}: summarized {field} contains an event absent from JSONL")
        resume_ids = summary.get("resume_event_ids", [])
        command = run_index.get("command", {})
        argv = command.get("argv", []) if isinstance(command, dict) else []
        synthetic_resume = f"resume-command:{binding.get('session_id')}"
        if isinstance(resume_ids, list) and any(
            value not in event_ids
            and not (value == synthetic_resume and "resume" in argv and binding.get("session_id") in argv)
            for value in resume_ids
        ):
            errors.append(f"{label}: summarized resume command is not proven by JSONL/argv")
    return run_index, events, errors


def _load_standalone_run_index(
    file_binding: Any,
    repo_root: Path,
    run_index_validator: Draft202012Validator,
    label: str,
    *,
    expected: dict[str, Any],
) -> tuple[Path | None, dict[str, Any] | None, list[dict[str, Any]], list[str]]:
    path, errors = _validate_file_binding(file_binding, repo_root, label)
    errors.extend(_validate_private_path(path, repo_root, label))
    if path is None:
        return None, None, [], errors
    try:
        index = load_yaml(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return path, None, [], errors + [f"{label}: run-index cannot be parsed: {exc}"]
    errors.extend(_validator_errors(index, run_index_validator, label))
    for field in ("slot_id", "task_id", "session_id", "plugin_version", "source_identity"):
        if index.get(field) != expected.get(field):
            errors.append(f"{label}: {field} differs from the Deep Research origin")
    if index.get("exit_code") != 0:
        errors.append(f"{label}: exit_code is not zero")
    started, started_errors = _parse_datetime(index.get("started_at"), f"{label}.started_at")
    completed, completed_errors = _parse_datetime(index.get("completed_at"), f"{label}.completed_at")
    errors.extend(started_errors + completed_errors)
    if started is not None and completed is not None and started > completed:
        errors.append(f"{label}: completed_at precedes started_at")
    for field, value in index.get("files", {}).items():
        file_path, file_errors = _validate_file_binding(value, repo_root, f"{label}.files.{field}")
        errors.extend(file_errors)
        errors.extend(_validate_private_path(file_path, repo_root, f"{label}.files.{field}"))
    for group in ("input_bindings", "output_bindings"):
        values = index.get(group, [])
        keys = [_artifact_key(value) for value in values if isinstance(value, dict)]
        if len(keys) != len(set(keys)):
            errors.append(f"{label}: {group} contains duplicate artifact bindings")
        for offset, artifact in enumerate(values):
            artifact_path, artifact_errors = _validate_artifact_binding(
                artifact, repo_root, f"{label}.{group}[{offset}]"
            )
            errors.extend(artifact_errors)
            errors.extend(
                _validate_private_path(
                    artifact_path,
                    repo_root,
                    f"{label}.{group}[{offset}]",
                    allow_private_inputs=group == "input_bindings",
                )
            )
    jsonl_binding = index.get("files", {}).get("jsonl")
    jsonl_path, _ = _validate_file_binding(jsonl_binding, repo_root, f"{label}.files.jsonl")
    events: list[dict[str, Any]] = []
    if jsonl_path is not None:
        events, jsonl_errors = _load_jsonl(jsonl_path, f"{label}.files.jsonl")
        errors.extend(jsonl_errors)
    thread_events = [event for event in events if _event_kind(event).startswith("thread.started")]
    if not thread_events:
        errors.append(f"{label}: JSONL lacks thread.started")
    elif not any(event.get("thread_id") == index.get("session_id") for event in thread_events):
        errors.append(f"{label}: thread.started does not identify the run-index session")
    completed_events = [event for event in events if _event_kind(event).startswith("turn.completed")]
    if not completed_events:
        errors.append(f"{label}: JSONL lacks turn.completed")
    summary = index.get("event_summary", {})
    event_ids = {_event_id(event) for event in events if _event_id(event)}
    if not isinstance(summary, dict):
        errors.append(f"{label}: event_summary is missing")
    else:
        if summary.get("thread_started_event_id") != index.get("session_id"):
            errors.append(f"{label}: summarized thread.started event differs from session")
        for field in ("turn_completed_event_ids", "web_search_event_ids"):
            values = summary.get(field, [])
            if not isinstance(values, list) or any(value not in event_ids for value in values):
                errors.append(f"{label}: summarized {field} contains an event absent from JSONL")
        resume_ids = summary.get("resume_event_ids", [])
        command = index.get("command", {})
        argv = command.get("argv", []) if isinstance(command, dict) else []
        synthetic_resume = f"resume-command:{index.get('session_id')}"
        if not isinstance(resume_ids, list) or any(
            value not in event_ids
            and not (
                value == synthetic_resume
                and "resume" in argv
                and index.get("session_id") in argv
            )
            for value in resume_ids
        ):
            errors.append(f"{label}: summarized resume command is not proven by JSONL/argv")
    return path, index, events, errors


def _validate_observed_binding(
    receipt: dict[str, Any],
    plugin_version: str,
    repo_root: Path,
    plugin_root: Path,
    run_index_validator: Draft202012Validator,
    *,
    validate_source: bool,
) -> tuple[list[str], dict[str, Any] | None, list[dict[str, Any]]]:
    errors: list[str] = []
    slot_id = str(receipt.get("slot_id", "<unknown>"))
    binding = receipt.get("binding")
    if not isinstance(binding, dict):
        return [f"{slot_id}: binding is missing"], None, []
    if binding.get("plugin_version") != plugin_version:
        errors.append(f"{slot_id}: observed plugin version differs from the collection")
    if binding.get("owner_confirmed") is not True:
        errors.append(f"{slot_id}: owner confirmation is missing")

    started, started_errors = _parse_datetime(binding.get("started_at"), f"{slot_id}.started_at")
    completed, completed_errors = _parse_datetime(binding.get("completed_at"), f"{slot_id}.completed_at")
    errors.extend(started_errors + completed_errors)
    if started is not None and completed is not None and started > completed:
        errors.append(f"{slot_id}: completed_at precedes started_at")

    if validate_source:
        errors.extend(
            _validate_source_identity(
                binding.get("source_identity"), repo_root, plugin_root, plugin_version, slot_id
            )
        )
    artifacts = binding.get("artifact_bindings", [])
    idea_logical = receipt.get("workflow") == "idea"
    for offset, artifact in enumerate(artifacts if isinstance(artifacts, list) else []):
        artifact_path, artifact_errors = _validate_artifact_binding(
            artifact,
            repo_root,
            f"{slot_id}.artifact_bindings[{offset}]",
            require_digest=not idea_logical,
        )
        errors.extend(artifact_errors)
        if receipt.get("kind") == "distribution":
            errors.extend(
                _validate_private_path(
                    artifact_path, repo_root, f"{slot_id}.artifact_bindings[{offset}]"
                )
            )

    runtime = binding.get("runtime_evidence")
    if not isinstance(runtime, dict):
        return errors + [f"{slot_id}: runtime evidence is missing"], None, []
    runtime_paths: dict[str, Path] = {}
    for field in ("prompt", "jsonl", "stderr", "final_message"):
        runtime_path, field_errors = _validate_file_binding(
            runtime.get(field), repo_root, f"{slot_id}.runtime_evidence.{field}"
        )
        if runtime_path is not None:
            runtime_paths[field] = runtime_path
        errors.extend(field_errors)
        errors.extend(
            _validate_private_path(
                runtime_path, repo_root, f"{slot_id}.runtime_evidence.{field}"
            )
        )
    final_path = runtime_paths.get("final_message")
    if final_path is not None:
        final_text = final_path.read_text(encoding="utf-8")
        statuses = re.findall(
            r"(?mi)^\s*status\s*:\s*([^\s#]+)\s*$", final_text
        )
        if statuses != [receipt.get("actual_outcome")]:
            errors.append(f"{slot_id}: final message status differs from actual outcome")
    if runtime.get("exit_code") != 0:
        errors.append(f"{slot_id}: Codex runtime exit code is not zero")

    actors = binding.get("actor_bindings", [])
    reviewer_count = 0
    for offset, actor in enumerate(actors if isinstance(actors, list) else []):
        if isinstance(actor, dict):
            reviewer_count += int(_is_reviewer(actor))
            errors.extend(_validate_actor_paths(actor, repo_root, f"{slot_id}.actor_bindings[{offset}]"))
    if receipt.get("kind") == "workflow_happy" and reviewer_count < 2:
        errors.append(f"{slot_id}: happy workflow has fewer than two fresh independent reviewers")

    run_index, events, run_errors = _validate_run_index(
        {**binding, "slot_id": slot_id}, runtime, repo_root, run_index_validator, slot_id
    )
    errors.extend(run_errors)
    return errors, run_index, events


def _contains_ready_state(value: Any) -> bool:
    if isinstance(value, dict):
        state_keys = {
            "status",
            "state",
            "decision",
            "terminal_state",
            "actual_outcome",
            "status_trace",
            "state_trace",
        }
        return any(
            _contains_ready_state(item)
            for key, item in value.items()
            if str(key).lower() in state_keys
        )
    if isinstance(value, list):
        return any(_contains_ready_state(item) for item in value)
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if stripped in READY_STATES:
        return True
    state_line = re.compile(
        r"^\s*(?:status|state|decision|terminal_state|actual_outcome)\s*[:=]\s*([^\s#]+)",
        re.IGNORECASE,
    )
    return any(
        (match := state_line.match(line)) is not None and match.group(1) in READY_STATES
        for line in value.splitlines()
    )


def _validate_control(
    receipt: dict[str, Any],
    repo_root: Path,
    run_index: dict[str, Any] | None,
) -> list[str]:
    slot_id = str(receipt.get("slot_id"))
    binding = receipt.get("binding", {})
    evidence = binding.get("control_evidence") if isinstance(binding, dict) else None
    if not isinstance(evidence, dict):
        return [f"{slot_id}: control evidence is missing"]
    errors: list[str] = []
    if evidence.get("control_type") != EXPECTED_CONTROL_TYPE.get(slot_id):
        errors.append(f"{slot_id}: control type differs from the slot")
    if evidence.get("terminal_state") != receipt.get("actual_outcome"):
        errors.append(f"{slot_id}: control terminal state differs from actual outcome")
    trace = evidence.get("state_trace", [])
    if not isinstance(trace, list) or not trace or trace[-1] != evidence.get("terminal_state"):
        errors.append(f"{slot_id}: control state trace does not end at the terminal state")
    if evidence.get("ready_state_observed") is not False:
        errors.append(f"{slot_id}: control observed a ready state")
    if isinstance(trace, list) and any(state in READY_STATES for state in trace):
        errors.append(f"{slot_id}: control state trace contains a ready state")
    if evidence.get("source_inputs_modified") is not False:
        errors.append(f"{slot_id}: control modified source inputs")
    actors = binding.get("actor_bindings", []) if isinstance(binding, dict) else []
    command = run_index.get("command", {}) if isinstance(run_index, dict) else {}
    if evidence.get("control_type") == "reviewer_unavailable":
        if command.get("multi_agent_enabled") is not False:
            errors.append(f"{slot_id}: reviewer-unavailable control did not disable multi-agent")
        if any(isinstance(actor, dict) and _is_reviewer(actor) for actor in actors):
            errors.append(f"{slot_id}: reviewer-unavailable control contains a reviewer actor")

    before = evidence.get("source_inputs_before", [])
    after = evidence.get("source_inputs_after", [])
    if len(before) != len(after):
        errors.append(f"{slot_id}: control source input inventories differ")
    for offset, (initial, final) in enumerate(zip(before, after)):
        if _artifact_key(initial) != _artifact_key(final):
            errors.append(f"{slot_id}: control source input {offset} changed")
        for label_suffix, artifact in (("before", initial), ("after", final)):
            path, artifact_errors = _validate_artifact_binding(
                artifact, repo_root, f"{slot_id}.source_inputs_{label_suffix}[{offset}]"
            )
            errors.extend(artifact_errors)
            errors.extend(
                _validate_private_path(
                    path,
                    repo_root,
                    f"{slot_id}.source_inputs_{label_suffix}[{offset}]",
                    allow_private_inputs=True,
                )
            )
    input_keys = {
        _artifact_key(item)
        for item in (run_index.get("input_bindings", []) if isinstance(run_index, dict) else [])
        if isinstance(item, dict)
    }
    if not input_keys or any(
        isinstance(artifact, dict) and _artifact_key(artifact) not in input_keys
        for artifact in before
    ):
        errors.append(f"{slot_id}: control run-index does not bind all source inputs")

    state_artifact = evidence.get("state_artifact")
    state_path, state_errors = _validate_artifact_binding(
        state_artifact, repo_root, f"{slot_id}.control_state_artifact"
    )
    errors.extend(state_errors)
    errors.extend(_validate_private_path(state_path, repo_root, f"{slot_id}.control_state_artifact"))
    receipt_artifacts = {
        _artifact_key(item)
        for item in binding.get("artifact_bindings", [])
        if isinstance(item, dict)
    }
    output_keys = {
        _artifact_key(item)
        for item in (run_index.get("output_bindings", []) if isinstance(run_index, dict) else [])
        if isinstance(item, dict)
    }
    if isinstance(state_artifact, dict):
        key = _artifact_key(state_artifact)
        if key not in receipt_artifacts or key not in output_keys:
            errors.append(f"{slot_id}: control state artifact lacks receipt/run-index binding")
    state: dict[str, Any] | None = None
    if state_path is not None:
        state, structured_errors = _load_structured_file(state_path, f"{slot_id}.state_artifact")
        errors.extend(structured_errors)
        if state is not None:
            if state.get("status_trace") != trace or state.get("terminal_state") != evidence.get("terminal_state"):
                errors.append(f"{slot_id}: structured state artifact differs from control evidence")
            if _contains_ready_state(state):
                errors.append(f"{slot_id}: control state artifact contains a ready state")
    runtime = binding.get("runtime_evidence", {})
    final_path, _ = _validate_file_binding(
        runtime.get("final_message") if isinstance(runtime, dict) else None,
        repo_root,
        f"{slot_id}.final_message",
    )
    if final_path is not None and _contains_ready_state(final_path.read_text(encoding="utf-8")):
        errors.append(f"{slot_id}: control final message contains a ready state")

    mismatch = evidence.get("digest_mismatch_evidence")
    if evidence.get("control_type") == "fatal_digest_mismatch":
        if not isinstance(mismatch, dict):
            errors.append(f"{slot_id}: fatal control lacks digest mismatch evidence")
        else:
            expected = mismatch.get("expected_sha256")
            supplied = mismatch.get("supplied_sha256")
            post_run = mismatch.get("post_run_sha256")
            if supplied == expected or expected != post_run:
                errors.append(f"{slot_id}: fatal digest relationship is invalid")
            matched = next(
                (
                    artifact
                    for artifact in before
                    if isinstance(artifact, dict) and artifact.get("path") == mismatch.get("path")
                ),
                None,
            )
            if matched is None or matched.get("sha256") != expected:
                errors.append(f"{slot_id}: fatal expected digest is not bound to the source input")
    elif mismatch is not None:
        errors.append(f"{slot_id}: reviewer-unavailable control carries digest mismatch evidence")
    return errors


def _validate_distribution(
    receipt: dict[str, Any],
    repo_root: Path,
    run_index: dict[str, Any] | None,
) -> list[str]:
    slot_id = str(receipt.get("slot_id"))
    binding = receipt.get("binding", {})
    errors: list[str] = []
    artifacts = binding.get("artifact_bindings", []) if isinstance(binding, dict) else []
    if len(artifacts) != 1 or not isinstance(artifacts[0], dict):
        return [f"{slot_id}: distribution requires exactly one structured report"]
    report_binding = artifacts[0]
    report_path, report_errors = _validate_artifact_binding(
        report_binding, repo_root, f"{slot_id}.distribution_report"
    )
    errors.extend(report_errors)
    errors.extend(_validate_private_path(report_path, repo_root, f"{slot_id}.distribution_report"))
    outputs = run_index.get("output_bindings", []) if isinstance(run_index, dict) else []
    if report_binding not in outputs:
        errors.append(f"{slot_id}: distribution report is absent from run-index outputs")
    if report_path is None:
        return errors
    report, structured_errors = _load_structured_file(
        report_path, f"{slot_id}.distribution_report"
    )
    errors.extend(structured_errors)
    if report is None:
        return errors
    source = binding.get("source_identity", {})
    cache_value = source.get("installed_cache_path") if isinstance(source, dict) else None
    cache = Path(cache_value).resolve() if isinstance(cache_value, str) else None
    installed_registry: dict[str, Any] = {}
    installed_skills: set[str] = set()
    if cache is not None and cache.is_dir():
        try:
            installed_registry = load_yaml(cache / "workflow-registry.yaml")
            installed_skills = {
                path.parent.name for path in (cache / "skills").glob("*/SKILL.md")
            }
        except (OSError, ValueError, yaml.YAMLError):
            errors.append(f"{slot_id}: installed distribution cannot be inspected")
    registry_skills = installed_registry.get("skills", []) if isinstance(installed_registry, dict) else []
    reviewer_count = sum(
        1
        for skill in registry_skills
        if isinstance(skill, dict) and skill.get("requires_independent_subagent") is True
    )
    expected = {
        "plugin_version": binding.get("plugin_version"),
        "installed_enabled": True,
        "skill_count": len(installed_skills),
        "independent_reviewer_count": reviewer_count,
        "declared_entries": sorted(EXPECTED_DECLARED),
        "implicit_entries": sorted(EXPECTED_IMPLICIT),
        "explicit_only_entries": ["research-polisher-orchestrator"],
        "pubmed_present": "pubmed" in installed_skills,
        "explicit_polisher_resolved": True,
        "marketplace_source": source.get("marketplace_source") if isinstance(source, dict) else None,
        "marketplace_ref": source.get("marketplace_ref") if isinstance(source, dict) else None,
        "marketplace_revision": source.get("marketplace_revision") if isinstance(source, dict) else None,
    }
    for field, value in expected.items():
        if report.get(field) != value:
            errors.append(f"{slot_id}: distribution report {field} differs from installed evidence")
    if expected["skill_count"] != 50 or expected["independent_reviewer_count"] != 21:
        errors.append(f"{slot_id}: installed distribution count baseline differs from 50/21")
    if report.get("pubmed_present") is not False:
        errors.append(f"{slot_id}: distribution reports the removed pubmed skill")
    return errors


def _validate_search(
    receipt: dict[str, Any],
    repo_root: Path,
    run_index: dict[str, Any] | None,
    events: list[dict[str, Any]],
) -> list[str]:
    slot_id = str(receipt.get("slot_id"))
    binding = receipt.get("binding", {})
    evidence = binding.get("search_evidence") if isinstance(binding, dict) else None
    if not isinstance(evidence, dict):
        return [f"{slot_id}: Search evidence is missing"]
    errors: list[str] = []
    web_events = [event for event in events if _is_completed_web_search(event)]
    web_ids = {_event_id(event) for event in web_events if _event_id(event)}
    claimed_ids = set(evidence.get("event_ids", []))
    if evidence.get("web_search_event_count") != len(web_ids):
        errors.append(f"{slot_id}: Search event count differs from Codex JSONL")
    if not claimed_ids or claimed_ids != web_ids:
        errors.append(f"{slot_id}: claimed web_search events are absent from Codex JSONL")
    summary = run_index.get("event_summary", {}) if isinstance(run_index, dict) else {}
    if set(summary.get("web_search_event_ids", [])) != claimed_ids:
        errors.append(f"{slot_id}: run-index web_search events differ from receipt evidence")
    command = run_index.get("command", {}) if isinstance(run_index, dict) else {}
    if command.get("search_enabled") is not True:
        errors.append(f"{slot_id}: run-index does not prove Search was enabled")

    source_urls = set(binding.get("source_urls", []))
    opened = set(evidence.get("opened_urls", []))
    if not opened or not opened.issubset(source_urls):
        errors.append(f"{slot_id}: opened URLs are missing from source bindings")
    mappings = evidence.get("claim_mappings", [])
    records = evidence.get("source_records", [])
    record_ids = [
        record.get("source_id") for record in records if isinstance(record, dict)
    ]
    normalized_record_urls = [
        _canonical_url(str(record.get("url", "")))
        for record in records
        if isinstance(record, dict)
    ]
    if len(record_ids) != len(set(record_ids)):
        errors.append(f"{slot_id}: Search source record IDs must be unique")
    if len(normalized_record_urls) != len(set(normalized_record_urls)):
        errors.append(f"{slot_id}: Search source record URLs must be unique")
    record_by_id = {
        record.get("source_id"): record for record in records if isinstance(record, dict)
    }
    if set(record.get("url") for record in records if isinstance(record, dict)) != opened:
        errors.append(f"{slot_id}: source records do not exactly cover opened URLs")
    for offset, record in enumerate(records if isinstance(records, list) else []):
        event_ids = set(record.get("evidence_event_ids", [])) if isinstance(record, dict) else set()
        if not event_ids or not event_ids.issubset(claimed_ids):
            errors.append(f"{slot_id}: source record {offset} is not bound to Search events")
    for offset, mapping in enumerate(mappings if isinstance(mappings, list) else []):
        urls = set(mapping.get("source_urls", [])) if isinstance(mapping, dict) else set()
        if not urls or not urls.issubset(opened):
            errors.append(f"{slot_id}: claim mapping {offset} is not grounded in opened URLs")
        source_ids = set(mapping.get("source_record_ids", [])) if isinstance(mapping, dict) else set()
        if not source_ids or not source_ids.issubset(record_by_id):
            errors.append(f"{slot_id}: claim mapping {offset} lacks source-record provenance")
        elif urls != {record_by_id[source_id].get("url") for source_id in source_ids}:
            errors.append(f"{slot_id}: claim mapping {offset} URL and source-record bindings differ")

    allowed_primary = {"official_primary", "peer_reviewed_primary", "registry"}
    if slot_id in {"personal-search-current", "personal-search-exact"} and not any(
        isinstance(record, dict) and record.get("source_type") in allowed_primary
        for record in records
    ):
        errors.append(f"{slot_id}: current/exact Search lacks an authoritative or primary source")
    if slot_id == "personal-search-narrow-academic":
        if not 2 <= len(set(normalized_record_urls)) <= 5 or any(
            not isinstance(record, dict) or record.get("source_type") != "peer_reviewed_primary"
            for record in records
        ):
            errors.append(f"{slot_id}: narrow academic Search must use 2-5 primary papers")

    source_report = evidence.get("source_report")
    report_path, report_errors = _validate_artifact_binding(
        source_report, repo_root, f"{slot_id}.search_source_report"
    )
    errors.extend(report_errors)
    errors.extend(_validate_private_path(report_path, repo_root, f"{slot_id}.search_source_report"))
    receipt_artifacts = {
        _artifact_key(item)
        for item in binding.get("artifact_bindings", [])
        if isinstance(item, dict)
    }
    output_keys = {
        _artifact_key(item)
        for item in (run_index.get("output_bindings", []) if isinstance(run_index, dict) else [])
        if isinstance(item, dict)
    }
    if isinstance(source_report, dict):
        report_key = _artifact_key(source_report)
        if report_key not in receipt_artifacts or report_key not in output_keys:
            errors.append(f"{slot_id}: Search report lacks receipt/run-index binding")
    if report_path is not None:
        report, structured_errors = _load_structured_file(report_path, f"{slot_id}.source_report")
        errors.extend(structured_errors)
        if report is not None:
            expected_report = {
                "source_records": records,
                "claim_mappings": mappings,
                "opened_urls": evidence.get("opened_urls"),
                "event_ids": evidence.get("event_ids"),
            }
            for field, expected in expected_report.items():
                if report.get(field) != expected:
                    errors.append(f"{slot_id}: Search report {field} differs from receipt")
            rendered = report_path.read_text(encoding="utf-8")
            if any(url not in rendered for url in opened):
                errors.append(f"{slot_id}: Search report omits an opened URL")
            if any(
                isinstance(mapping, dict) and mapping.get("claim") not in rendered
                for mapping in mappings
            ):
                errors.append(f"{slot_id}: Search report omits a mapped claim")

    for offset, artifact in enumerate(binding.get("artifact_bindings", [])):
        if isinstance(artifact, dict):
            path, artifact_errors = _validate_artifact_binding(
                artifact, repo_root, f"{slot_id}.artifact_bindings[{offset}]"
            )
            errors.extend(artifact_errors)
            errors.extend(
                _validate_private_path(path, repo_root, f"{slot_id}.artifact_bindings[{offset}]")
            )
    return errors


def _validate_deep_research(
    receipt: dict[str, Any],
    repo_root: Path,
    run_index: dict[str, Any] | None,
    events: list[dict[str, Any]],
    run_index_validator: Draft202012Validator,
) -> tuple[list[str], str | None]:
    slot_id = str(receipt.get("slot_id"))
    binding = receipt.get("binding", {})
    evidence = binding.get("deep_research_evidence") if isinstance(binding, dict) else None
    if not isinstance(evidence, dict):
        return [f"{slot_id}: Deep Research evidence is missing"], None
    errors: list[str] = []
    mode = evidence.get("mode")
    expected_mode = (
        "inactive_handoff" if receipt.get("kind") == "deep_research_inactive" else "completed_resume"
    )
    if mode != expected_mode:
        errors.append(f"{slot_id}: Deep Research mode differs from the slot")
    artifacts = binding.get("artifact_bindings", [])
    artifact_keys = {
        _artifact_key(artifact) for artifact in artifacts if isinstance(artifact, dict)
    }
    evidence_artifacts = [
        evidence.get("pending_edge_ledger"),
        evidence.get("edge_ledger"),
        evidence.get("continuation_package"),
        evidence.get("returned_result"),
        evidence.get("mapper_artifact"),
    ]
    evidence_paths: dict[str, Path] = {}
    for name, artifact in zip(
        (
            "pending_edge_ledger",
            "edge_ledger",
            "continuation_package",
            "returned_result",
            "mapper_artifact",
        ),
        evidence_artifacts,
    ):
        if artifact is None:
            continue
        path, artifact_errors = _validate_artifact_binding(
            artifact, repo_root, f"{slot_id}.{name}"
        )
        errors.extend(artifact_errors)
        errors.extend(_validate_private_path(path, repo_root, f"{slot_id}.{name}"))
        if path is not None:
            evidence_paths[name] = path
        if isinstance(artifact, dict) and _artifact_key(artifact) not in artifact_keys:
            errors.append(f"{slot_id}: {name} is absent from receipt artifacts")

    origin_task = evidence.get("origin_task_id")
    origin_session = evidence.get("origin_session_id")
    expected_run_identity = {
        "slot_id": slot_id,
        "task_id": origin_task,
        "session_id": origin_session,
        "plugin_version": binding.get("plugin_version"),
        "source_identity": binding.get("source_identity"),
    }
    handoff_path, handoff, handoff_events, handoff_errors = _load_standalone_run_index(
        evidence.get("handoff_run_index"),
        repo_root,
        run_index_validator,
        f"{slot_id}.handoff_run_index",
        expected=expected_run_identity,
    )
    errors.extend(handoff_errors)
    resume_path: Path | None = None
    resume: dict[str, Any] | None = None
    if evidence.get("resume_run_index") is not None:
        resume_path, resume, _, resume_errors = _load_standalone_run_index(
            evidence.get("resume_run_index"),
            repo_root,
            run_index_validator,
            f"{slot_id}.resume_run_index",
            expected=expected_run_identity,
        )
        errors.extend(resume_errors)

    if origin_task != binding.get("task_id") or origin_session != binding.get("session_id"):
        errors.append(f"{slot_id}: Deep Research origin differs from receipt task/session")
    if isinstance(handoff, dict):
        if handoff.get("task_id") != origin_task or handoff.get("session_id") != origin_session:
            errors.append(f"{slot_id}: handoff run-index differs from origin task/session")
        if handoff.get("source_identity") != binding.get("source_identity"):
            errors.append(f"{slot_id}: handoff source identity differs from receipt")
        handoff_argv = handoff.get("command", {}).get("argv", [])
        if "resume" in handoff_argv:
            errors.append(f"{slot_id}: handoff run-index is already a resume command")
        if evidence.get("continuation_package") not in handoff.get("output_bindings", []):
            errors.append(f"{slot_id}: handoff output does not bind the continuation package")
        if evidence.get("pending_edge_ledger") not in handoff.get("output_bindings", []):
            errors.append(f"{slot_id}: handoff output omits the pending edge ledger")

    summary = run_index.get("event_summary", {}) if isinstance(run_index, dict) else {}
    summary_resume_ids = set(summary.get("resume_event_ids", []))
    claimed_resume_ids = set(evidence.get("resume_event_ids", []))
    if summary_resume_ids != claimed_resume_ids:
        errors.append(f"{slot_id}: run-index resume events differ from Deep Research evidence")

    if expected_mode == "inactive_handoff":
        command = run_index.get("command", {}) if isinstance(run_index, dict) else {}
        if command.get("search_enabled") is not False:
            errors.append(f"{slot_id}: inactive Deep Research control used Search")
        if any("web_search" in _event_kind(event) for event in events):
            errors.append(f"{slot_id}: inactive Deep Research JSONL contains web_search")
        if evidence.get("resume_count") != 0 or evidence.get("edge_consumed") is not False:
            errors.append(f"{slot_id}: inactive Deep Research edge was consumed")
        runtime_binding = binding.get("runtime_evidence", {}).get("run_index")
        if evidence.get("handoff_run_index") != runtime_binding or resume is not None:
            errors.append(f"{slot_id}: inactive Deep Research runtime is not the sole handoff run")
        if evidence.get("pending_edge_ledger") != evidence.get("edge_ledger"):
            errors.append(f"{slot_id}: inactive edge ledger differs from its pending version")
    else:
        if evidence.get("resume_session_id") != binding.get("session_id"):
            errors.append(f"{slot_id}: resume session differs from the original session")
        if (
            evidence.get("resume_count") != 1
            or len(claimed_resume_ids) != 1
            or evidence.get("edge_consumed") is not True
        ):
            errors.append(f"{slot_id}: completed Deep Research edge was not consumed exactly once")
        command = run_index.get("command", {}) if isinstance(run_index, dict) else {}
        argv = command.get("argv", []) if isinstance(command, dict) else []
        expected_resume_id = f"resume-command:{binding.get('session_id')}"
        if claimed_resume_ids != {expected_resume_id}:
            errors.append(f"{slot_id}: resume command ID is not reproducible from the session")
        if "resume" not in argv or binding.get("session_id") not in argv:
            errors.append(f"{slot_id}: run-index argv does not prove same-session resume")
        runtime_binding = binding.get("runtime_evidence", {}).get("run_index")
        if evidence.get("resume_run_index") != runtime_binding:
            errors.append(f"{slot_id}: completed Deep Research runtime is not the resume run-index")
        if not isinstance(resume, dict):
            errors.append(f"{slot_id}: completed Deep Research resume run-index is missing")
        else:
            if resume.get("task_id") != origin_task or resume.get("session_id") != origin_session:
                errors.append(f"{slot_id}: resume run-index differs from origin task/session")
            if resume.get("source_identity") != binding.get("source_identity"):
                errors.append(f"{slot_id}: resume source identity differs from receipt")
            resume_inputs = resume.get("input_bindings", [])
            resume_outputs = resume.get("output_bindings", [])
            for artifact in (evidence.get("continuation_package"), evidence.get("returned_result")):
                if artifact not in resume_inputs:
                    errors.append(f"{slot_id}: resume inputs omit continuation or returned result")
            if evidence.get("mapper_artifact") not in resume_outputs:
                errors.append(f"{slot_id}: resume output omits mapper artifact")
            if evidence.get("edge_ledger") not in resume_outputs:
                errors.append(f"{slot_id}: resume output omits the final edge ledger")

        pending_ledger_binding = evidence.get("pending_edge_ledger")
        final_ledger_binding = evidence.get("edge_ledger")
        if isinstance(pending_ledger_binding, dict) and isinstance(final_ledger_binding, dict):
            if pending_ledger_binding.get("artifact_id") != final_ledger_binding.get("artifact_id"):
                errors.append(f"{slot_id}: pending/final ledgers do not share lineage")
            if any(
                pending_ledger_binding.get(field) == final_ledger_binding.get(field)
                for field in ("version", "path", "sha256")
            ):
                errors.append(f"{slot_id}: consumed edge ledger is not a distinct new version")
        continuation_binding = evidence.get("continuation_package")
        returned_binding = evidence.get("returned_result")
        mapper_binding = evidence.get("mapper_artifact")
        content_pairs = (
            (continuation_binding, returned_binding),
            (continuation_binding, mapper_binding),
            (returned_binding, mapper_binding),
        )
        for left, right in content_pairs:
            if not isinstance(left, dict) or not isinstance(right, dict) or any(
                left.get(field) == right.get(field)
                for field in ("artifact_id", "path", "sha256")
            ):
                errors.append(f"{slot_id}: Deep Research content artifact roles are not distinct")
        for ledger_binding in (pending_ledger_binding, final_ledger_binding):
            for content_binding in (
                continuation_binding,
                returned_binding,
                mapper_binding,
            ):
                if not isinstance(ledger_binding, dict) or not isinstance(content_binding, dict) or any(
                    ledger_binding.get(field) == content_binding.get(field)
                    for field in ("path", "sha256")
                ):
                    errors.append(f"{slot_id}: Deep Research ledger/content roles overlap")

    pending_ledger_path = evidence_paths.get("pending_edge_ledger")
    if pending_ledger_path is not None:
        pending_ledger, pending_errors = _load_structured_file(
            pending_ledger_path, f"{slot_id}.pending_edge_ledger"
        )
        errors.extend(pending_errors)
        if pending_ledger is not None:
            expected_pending = {
                "pending_edge_id": evidence.get("pending_edge_id"),
                "origin_task_id": origin_task,
                "origin_session_id": origin_session,
                "continuation_package": evidence.get("continuation_package"),
                "returned_result": None,
                "mapper_artifact": None,
                "resume_event_ids": [],
                "resume_count": 0,
                "edge_consumed": False,
            }
            for field, expected in expected_pending.items():
                if pending_ledger.get(field) != expected:
                    errors.append(f"{slot_id}: pending edge ledger {field} differs from handoff state")

    ledger_path = evidence_paths.get("edge_ledger")
    if ledger_path is not None:
        ledger, ledger_errors = _load_structured_file(ledger_path, f"{slot_id}.edge_ledger")
        errors.extend(ledger_errors)
        if ledger is not None:
            expected_ledger = {
                "pending_edge_id": evidence.get("pending_edge_id"),
                "origin_task_id": origin_task,
                "origin_session_id": origin_session,
                "continuation_package": evidence.get("continuation_package"),
                "returned_result": evidence.get("returned_result"),
                "mapper_artifact": evidence.get("mapper_artifact"),
                "resume_event_ids": evidence.get("resume_event_ids"),
                "resume_count": evidence.get("resume_count"),
                "edge_consumed": evidence.get("edge_consumed"),
            }
            for field, expected in expected_ledger.items():
                if ledger.get(field) != expected:
                    errors.append(f"{slot_id}: edge ledger {field} differs from receipt")

    scan_paths = [
        path
        for path in (handoff_path, resume_path, pending_ledger_path, ledger_path)
        if path is not None
    ]
    if scan_paths:
        import os

        scan_root = Path(os.path.commonpath([str(path.parent) for path in scan_paths]))
        resume_count = 0
        for candidate in [*scan_root.rglob("*.json"), *scan_root.rglob("*.yaml"), *scan_root.rglob("*.yml")]:
            try:
                value = load_yaml(candidate)
            except (OSError, ValueError, yaml.YAMLError, UnicodeDecodeError):
                continue
            argv = value.get("command", {}).get("argv", []) if isinstance(value, dict) else []
            if (
                isinstance(value, dict)
                and value.get("session_id") == origin_session
                and "resume" in argv
                and origin_session in argv
            ):
                resume_count += 1
        expected_count = 0 if expected_mode == "inactive_handoff" else 1
        if resume_count != expected_count:
            errors.append(f"{slot_id}: private edge directory contains {resume_count} resume runs, expected {expected_count}")
    return errors, evidence.get("pending_edge_id") if isinstance(evidence.get("pending_edge_id"), str) else None


def validate_receipts(
    receipts: dict[str, Any],
    plugin_version: str,
    *,
    repo_root: Path = REPO,
    plugin_root: Path = PLUGIN,
    schema: dict[str, Any] | None = None,
    run_index_schema: dict[str, Any] | None = None,
    receipts_path: Path | None = None,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    schema = schema or load_yaml(SCHEMA)
    run_index_schema = _embedded_run_index_schema(
        run_index_schema or load_yaml(RUN_INDEX_SCHEMA), schema
    )
    Draft202012Validator.check_schema(run_index_schema)
    run_index_validator = Draft202012Validator(
        run_index_schema, format_checker=FormatChecker()
    )
    errors.extend(_schema_errors(receipts, schema, "owner receipts"))
    if receipts.get("schema_version") != 2:
        errors.append("personal receipt schema version must be 2")
    if receipts.get("profile") != "personal-owner":
        errors.append("personal receipt profile must be personal-owner")
    if receipts.get("evidence_level") != "owner_observed":
        errors.append("personal receipt evidence level must be owner_observed")
    if receipts.get("plugin_version") != plugin_version:
        errors.append("personal receipt version differs from the plugin")

    expected_groups: list[tuple[str, dict[str, Any]]] = [
        ("workflow_runs", EXPECTED_WORKFLOW_SLOTS),
        ("control_runs", EXPECTED_CONTROL_SLOTS),
        ("retrieval_runs", EXPECTED_RETRIEVAL_SLOTS),
    ]
    all_receipts: list[dict[str, Any]] = []
    for group_name, expected in expected_groups:
        values = receipts.get(group_name)
        if not isinstance(values, list):
            errors.append(f"{group_name} must be a list")
            continue
        indexed = {
            item.get("slot_id"): item
            for item in values
            if isinstance(item, dict) and isinstance(item.get("slot_id"), str)
        }
        if set(indexed) != set(expected):
            errors.append(f"{group_name} slot inventory differs from the personal contract")
        for slot_id, expectation in expected.items():
            item = indexed.get(slot_id)
            if not isinstance(item, dict):
                continue
            all_receipts.append(item)
            if item.get("kind") != EXPECTED_SLOT_KINDS[slot_id]:
                errors.append(f"{slot_id}: kind differs from the fixed slot contract")
            if group_name == "workflow_runs":
                workflow, outcome = expectation
                if item.get("workflow") != workflow:
                    errors.append(f"{slot_id}: workflow differs from the contract")
            else:
                outcome = expectation
            if item.get("expected_outcome") != outcome:
                errors.append(f"{slot_id}: expected outcome differs from the contract")

    distribution = receipts.get("distribution")
    if not isinstance(distribution, dict) or distribution.get("slot_id") != "personal-distribution-current":
        errors.append("current-version distribution slot is missing")
    else:
        if distribution.get("kind") != EXPECTED_SLOT_KINDS["personal-distribution-current"]:
            errors.append("personal-distribution-current: kind differs from the fixed slot contract")
        all_receipts.insert(0, distribution)

    observed_ids: list[str] = []
    pending_ids: list[str] = []
    task_ids: set[str] = set()
    session_ids: set[str] = set()
    actor_ids: set[str] = set()
    instance_ids: set[str] = set()
    source_identity: dict[str, Any] | None = None
    source_checked = False
    receipt_privacy_checked = False
    pending_edge_ids: set[str] = set()
    for item in all_receipts:
        slot_id = str(item.get("slot_id"))
        status = item.get("status")
        if status == "pending_owner_observation":
            pending_ids.append(slot_id)
            continue
        if status != "owner_observed":
            errors.append(f"{slot_id}: invalid personal observation status")
            continue
        observed_ids.append(slot_id)
        if not receipt_privacy_checked:
            if receipts_path is None:
                errors.append("owner-observed receipts require a private receipt file path")
            else:
                receipt_file, receipt_path_errors = _resolve_repo_file(
                    repo_root, receipts_path, "owner receipts"
                ) if not receipts_path.is_absolute() else (
                    receipts_path.resolve(),
                    [] if receipts_path.resolve().is_file() else ["owner receipts: file does not exist"],
                )
                errors.extend(receipt_path_errors)
                errors.extend(_validate_private_path(receipt_file, repo_root, "owner receipts"))
                if receipt_file is not None:
                    try:
                        if load_yaml(receipt_file) != receipts:
                            errors.append("owner receipts: file content differs from validated receipts")
                    except (OSError, ValueError, yaml.YAMLError):
                        errors.append("owner receipts: private receipt file cannot be parsed")
            receipt_privacy_checked = True
        if item.get("actual_outcome") != item.get("expected_outcome"):
            errors.append(f"{slot_id}: observed outcome does not match the accepted outcome")
        binding = item.get("binding", {})
        if isinstance(binding, dict):
            for field, seen in (("task_id", task_ids), ("session_id", session_ids)):
                value = binding.get(field)
                if isinstance(value, str):
                    if value in seen:
                        errors.append(f"{slot_id}: duplicate global {field}")
                    seen.add(value)
            current_source = binding.get("source_identity")
            if source_identity is None and isinstance(current_source, dict):
                source_identity = current_source
            elif current_source != source_identity:
                errors.append(f"{slot_id}: source identity differs from other observed slots")
            for actor in binding.get("actor_bindings", []):
                if not isinstance(actor, dict):
                    continue
                for field, seen in (("actor_id", actor_ids), ("instance_id", instance_ids)):
                    value = actor.get(field)
                    if isinstance(value, str):
                        if value in seen:
                            errors.append(f"{slot_id}: duplicate global {field}")
                        seen.add(value)

        binding_errors, run_index, events = _validate_observed_binding(
            item,
            plugin_version,
            repo_root,
            plugin_root,
            run_index_validator,
            validate_source=not source_checked,
        )
        source_checked = True
        errors.extend(binding_errors)
        kind = EXPECTED_SLOT_KINDS.get(slot_id)
        if kind == "distribution":
            errors.extend(_validate_distribution(item, repo_root, run_index))
        elif kind == "workflow_happy":
            errors.extend(_validate_workflow_evidence(item, repo_root, run_index))
        elif kind == "workflow_control":
            errors.extend(_validate_control(item, repo_root, run_index))
        elif kind == "search":
            errors.extend(_validate_search(item, repo_root, run_index, events))
        elif kind in {"deep_research_inactive", "deep_research_complete"}:
            dr_errors, edge_id = _validate_deep_research(
                item, repo_root, run_index, events, run_index_validator
            )
            errors.extend(dr_errors)
            if edge_id is not None:
                if edge_id in pending_edge_ids:
                    errors.append(f"{slot_id}: duplicate Deep Research pending edge ID")
                pending_edge_ids.add(edge_id)

    expected_total = 1 + len(EXPECTED_WORKFLOW_SLOTS) + len(EXPECTED_CONTROL_SLOTS) + len(EXPECTED_RETRIEVAL_SLOTS)
    if len(all_receipts) != expected_total:
        errors.append(f"personal receipt count must be {expected_total}")
    ready = len(observed_ids) == expected_total and not pending_ids and not errors
    return (
        {
            "expected_slot_count": expected_total,
            "owner_observed_slot_count": len(observed_ids),
            "pending_slot_count": len(pending_ids),
            "owner_observed_slots": sorted(observed_ids),
            "pending_slots": sorted(pending_ids),
            "status": "owner_observed_ready" if ready else "in_progress_owner_observation",
        },
        errors,
    )


def build_report(receipts_path: Path = RECEIPTS) -> tuple[dict[str, Any], list[str]]:
    deterministic, deterministic_errors = deterministic_checks()
    receipts = load_yaml(receipts_path)
    observation, receipt_errors = validate_receipts(
        receipts, deterministic["plugin_version"], receipts_path=receipts_path
    )
    errors = deterministic_errors + receipt_errors
    deterministic_status = (
        "deterministic_validated" if not deterministic_errors else "deterministic_validation_failed"
    )
    if errors:
        observation["status"] = "in_progress_owner_observation"
    report = {
        "schema_version": 2,
        "profile": "personal-owner",
        "plugin_version": deterministic["plugin_version"],
        "deterministic_status": deterministic_status,
        "personal_status": observation["status"],
        "deterministic_baseline": deterministic,
        "owner_observation": observation,
        "claims": {"automatic_external_submission": False},
        "errors": errors,
    }
    return report, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts", type=Path, default=RECEIPTS)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check-report", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args(argv)

    try:
        report, errors = build_report(args.receipts)
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        yaml.YAMLError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"Personal readiness validation failed: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8", newline="\n")
    if args.check_report:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != rendered:
            print("Personal readiness report is missing or stale", file=sys.stderr)
            return 1
    if errors:
        print("Personal readiness validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.require_ready and report["personal_status"] != "owner_observed_ready":
        print("Personal readiness remains in_progress_owner_observation", file=sys.stderr)
        return 1
    print(
        "Personal readiness validation passed: "
        f"{report['deterministic_status']}; {report['personal_status']}; "
        f"observed={report['owner_observation']['owner_observed_slot_count']}/"
        f"{report['owner_observation']['expected_slot_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
