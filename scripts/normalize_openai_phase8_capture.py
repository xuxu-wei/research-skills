#!/usr/bin/env python3
"""Normalize one profile-aware Phase 8 capture into a self-contained R v2.

The adapter validates claims against machine-readable platform exports.  A
task-authored identifier, scope list, Markdown report, screenshot, PDF, or
filename is never an authority for a platform event.  Missing Deep Research
completion provenance may be retained only as an explicitly pending capture;
it cannot enter a live collection.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

from normalize_openai_preview_capture import (
    CaptureNormalizationError,
    StagingRoot,
    _identifier,
    _mapping,
    _sequence,
    _strict_json,
    _string,
    _timestamp,
    canonical_json_bytes,
    canonical_relative,
    parse_clock,
    require_distinct_paths,
)
from openai_preview_capture_contracts import (
    PHASE8_CAPTURE_ADAPTER_ID,
    PHASE8_NORMALIZED_CAPTURE_SCHEMA,
)
from openai_preview_evidence import normalize_sha256, sha256_bytes
from validate_openai_phase8_external_evidence import current_checkout_source_identity


REPO = Path(__file__).resolve().parents[1]
SCHEDULER_MANIFEST_PATH = "tests/openai_phase8/live-inputs/manifest.yaml"
SCHEDULER_SCHEMA = "phase8-scheduler-input-pack/v1"
TASK_EXPORT_SCHEMA = "openai-phase8-task-export/v2"
SOURCE_RECORD_SCHEMA = "openai-phase8-normalized-source/v1"
CAPTURE_SCHEMA_VERSION = 2
PROFILE_TO_KIND = {
    "phase8-reviewer-v1": "reviewer",
    "phase8-search-v1": "search",
    "phase8-deep-research-v1": "deep_research_completed",
    "phase8-deep-research-inactive-v1": "deep_research_inactive_control",
}
# No concrete ChatGPT/Codex platform-origin adapter is registered for the
# reviewer, Search, inactive-control, or completed Deep Research profiles.
# These labels identify structured *claims* that can be checked mechanically;
# they never establish platform origin or live-gate eligibility.  Adding a
# positive path requires a concrete capture endpoint/response schema, parser
# and code-digest binding, plus mutation tests.  There is intentionally no
# dormant positive parser.
UNTRUSTED_PLATFORM_CLAIM_TYPES = {
    "platform_export",
    "chatgpt_export",
    "compliance_record",
    "capability_export",
}
NON_PROVIDER_EXPORT_SUFFIXES = {".md", ".markdown", ".pdf", ".doc", ".docx"}
FROZEN_PATHS = (
    "research-skills-openai/.codex-plugin/plugin.json",
    "research-skills-openai/workflow-registry.yaml",
    "research-skills-openai/skills",
    SCHEDULER_MANIFEST_PATH,
    "tests/openai_phase8/live-inputs/inputs",
    "tests/openai_phase8/live-inputs/prompts",
    "scripts/openai_preview_capture_contracts.py",
    "scripts/normalize_openai_phase8_capture.py",
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _fail(code: str, path: str, message: str) -> None:
    raise CaptureNormalizationError(code, path, message)


def _bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        _fail("invalid_boolean", path, repr(value))
    return value


def _canonical_digest(value: Any, path: str) -> str:
    try:
        return normalize_sha256(value, path)
    except Exception as exc:
        _fail("invalid_sha256", path, str(exc))


def _positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("invalid_positive_integer", path, repr(value))
    return value


def _strict_yaml(payload: bytes, path: str) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(payload.decode("utf-8-sig"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("invalid_yaml", path, str(exc))
    return _mapping(value, path)


def _json_pointer(document: Any, pointer: str, path: str) -> Any:
    if pointer == "":
        return document
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        _fail("invalid_json_pointer", path, repr(pointer))
    current = document
    for offset, raw in enumerate(pointer.split("/")[1:]):
        token = raw.replace("~1", "/").replace("~0", "~")
        if "~" in token and re.search(r"~(?![01])", raw):
            _fail("invalid_json_pointer", path, pointer)
        if isinstance(current, Mapping):
            if token not in current:
                _fail("json_pointer_missing", path, f"{pointer} at segment {offset}")
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit() or (token.startswith("0") and token != "0"):
                _fail("json_pointer_index", path, pointer)
            index = int(token)
            if index >= len(current):
                _fail("json_pointer_missing", path, pointer)
            current = current[index]
        else:
            _fail("json_pointer_scalar", path, pointer)
    return current


def _value_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def _binding(value: Any, path: str) -> dict[str, Any]:
    record = _mapping(value, path)
    if set(record) != {"artifact_type", "path", "sha256", "size_bytes"}:
        _fail("artifact_binding_fields", path, str(sorted(record)))
    artifact_type = _identifier(record.get("artifact_type"), f"{path}.artifact_type")
    logical = _string(record.get("path"), f"{path}.path")
    canonical_relative(logical, f"{path}.path")
    digest = _canonical_digest(record.get("sha256"), f"{path}.sha256")
    size = _positive_int(record.get("size_bytes"), f"{path}.size_bytes")
    return {
        "artifact_type": artifact_type,
        "path": logical,
        "sha256": digest,
        "size_bytes": size,
    }


def _file_ref(value: Any, path: str, artifacts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    record = _binding(value, path)
    expected = artifacts.get(record["path"])
    if expected is None or dict(expected) != record:
        _fail("unbound_artifact_reference", path, record["path"])
    return record


def _source_record(payload: bytes) -> dict[str, Any]:
    return {
        "schema": SOURCE_RECORD_SCHEMA,
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
        "content_base64": base64.b64encode(payload).decode("ascii"),
    }


def _decode_sources(document: Mapping[str, Any]) -> dict[str, bytes]:
    records = _mapping(document.get("source_files"), "normalized_capture.source_files")
    decoded: dict[str, bytes] = {}
    for logical, value in records.items():
        canonical_relative(str(logical), f"normalized_capture.source_files.{logical}")
        record = _mapping(value, f"normalized_capture.source_files.{logical}")
        if set(record) != {"schema", "sha256", "size_bytes", "content_base64"} or record.get("schema") != SOURCE_RECORD_SCHEMA:
            _fail("normalized_source_fields", f"normalized_capture.source_files.{logical}", str(sorted(record)))
        encoded = record.get("content_base64")
        if not isinstance(encoded, str):
            _fail("invalid_base64", f"normalized_capture.source_files.{logical}", repr(encoded))
        try:
            payload = base64.b64decode(encoded, validate=True)
        except (ValueError, base64.binascii.Error):
            _fail("invalid_base64", f"normalized_capture.source_files.{logical}", "decode failed")
        if len(payload) != _positive_int(record.get("size_bytes"), f"normalized_capture.source_files.{logical}.size_bytes"):
            _fail("normalized_source_size_mismatch", f"normalized_capture.source_files.{logical}", str(len(payload)))
        if sha256_bytes(payload) != _canonical_digest(record.get("sha256"), f"normalized_capture.source_files.{logical}.sha256"):
            _fail("normalized_source_digest_mismatch", f"normalized_capture.source_files.{logical}", str(logical))
        decoded[str(logical)] = payload
    return decoded


def _structured_json_sources(
    artifacts: Mapping[str, Mapping[str, Any]], sources: Mapping[str, bytes]
) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for logical, record in artifacts.items():
        if record["artifact_type"] not in UNTRUSTED_PLATFORM_CLAIM_TYPES:
            continue
        if PurePosixPath(logical).suffix.lower() != ".json":
            _fail("platform_export_not_machine_readable_json", f"supporting_artifacts.{logical}", logical)
        result[logical] = _mapping(_strict_json(sources[logical], logical), logical)
    return result


def _resolve_platform_bindings(
    task: Mapping[str, Any],
    platform_documents: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
    raw = _mapping(task.get("platform_id_bindings"), "task-export.json.platform_id_bindings")
    resolved: dict[str, Any] = {}
    provenance: dict[str, dict[str, str]] = {}
    for name, value in raw.items():
        _identifier(name, f"task-export.json.platform_id_bindings.{name}")
        record = _mapping(value, f"task-export.json.platform_id_bindings.{name}")
        if set(record) != {"path", "json_pointer"}:
            _fail("platform_id_binding_fields", f"task-export.json.platform_id_bindings.{name}", str(sorted(record)))
        logical = _string(record.get("path"), f"task-export.json.platform_id_bindings.{name}.path")
        document = platform_documents.get(logical)
        if document is None:
            _fail("platform_id_binding_not_structured_export", f"task-export.json.platform_id_bindings.{name}.path", logical)
        pointer = _string(record.get("json_pointer"), f"task-export.json.platform_id_bindings.{name}.json_pointer")
        result = _json_pointer(document, pointer, f"task-export.json.platform_id_bindings.{name}.json_pointer")
        resolved[name] = result
        provenance[name] = {
            "source_path": logical,
            "json_pointer": pointer,
            "value_sha256": _value_digest(result),
        }
    return resolved, provenance


def _require_resolved(resolved: Mapping[str, Any], name: str, expected: Any, path: str) -> Any:
    if name not in resolved:
        _fail("platform_binding_missing", f"task-export.json.platform_id_bindings.{name}", path)
    actual = resolved[name]
    if actual != expected:
        _fail("platform_binding_mismatch", f"task-export.json.platform_id_bindings.{name}", f"expected {expected!r}, found {actual!r}")
    return actual


def _validate_scheduler(
    manifest: Mapping[str, Any],
    task: Mapping[str, Any],
    sources: Mapping[str, bytes],
    identity: Mapping[str, str],
) -> dict[str, Any]:
    if manifest.get("schema_version") != 1 or manifest.get("evidence_kind") != "scheduler_input_pack_only" or manifest.get("counts_as_runtime_evidence") is not False:
        _fail("scheduler_manifest_contract", "scheduler_manifest", "scheduler-only schema 1 pack required")
    visibility = manifest.get("task_visibility")
    if not isinstance(visibility, Mapping) or any(visibility.get(field) is not False for field in (
        "scheduler_manifest_visible_to_any_execution",
        "scheduler_labels_visible_to_any_execution",
        "expected_outcomes_visible_to_any_execution",
        "reviewer_launch_prompt_visible_to_delegate",
        "reviewer_peer_outputs_visible",
    )):
        _fail("scheduler_visibility_contract", "scheduler_manifest.task_visibility", repr(visibility))
    plugin = _mapping(manifest.get("plugin_binding"), "scheduler_manifest.plugin_binding")
    if plugin.get("plugin_name") != "research-skills-openai" or plugin.get("plugin_version") != identity["plugin_version"]:
        _fail("scheduler_plugin_binding", "scheduler_manifest.plugin_binding", repr(plugin))
    execution_id = _identifier(_mapping(task.get("scheduler_input"), "task-export.json.scheduler_input").get("execution_id"), "task-export.json.scheduler_input.execution_id")
    slots = _sequence(manifest.get("slots"), "scheduler_manifest.slots")
    selected = [item for item in slots if isinstance(item, Mapping) and item.get("execution_id") == execution_id]
    if len(slots) != 12 or len(selected) != 1:
        _fail("scheduler_slot_binding", "scheduler_manifest.slots", execution_id)
    slot = _mapping(selected[0], "scheduler_manifest.selected")
    scheduler = _mapping(task.get("scheduler_input"), "task-export.json.scheduler_input")
    required = {
        "execution_id", "input", "launch_prompt", "scheduler_manifest_visible",
        "scheduler_labels_visible", "expected_outcomes_visible",
    }
    if set(scheduler) != required:
        _fail("scheduler_input_fields", "task-export.json.scheduler_input", str(sorted(scheduler)))
    for flag in ("scheduler_manifest_visible", "scheduler_labels_visible", "expected_outcomes_visible"):
        if scheduler.get(flag) is not False:
            _fail("scheduler_oracle_visible", f"task-export.json.scheduler_input.{flag}", repr(scheduler.get(flag)))
    input_binding = _binding(scheduler.get("input"), "task-export.json.scheduler_input.input")
    prompt_binding = _binding(scheduler.get("launch_prompt"), "task-export.json.scheduler_input.launch_prompt")
    expected_input = {"path": slot.get("input_path"), "sha256": slot.get("input_sha256")}
    expected_prompt = {"path": slot.get("prompt_path"), "sha256": slot.get("prompt_sha256")}
    for actual, expected, label in ((input_binding, expected_input, "input"), (prompt_binding, expected_prompt, "launch_prompt")):
        if actual["path"] != expected["path"] or actual["sha256"] != expected["sha256"]:
            _fail("scheduler_input_mismatch", f"task-export.json.scheduler_input.{label}", repr(expected))
        payload = sources.get(actual["path"])
        if payload is None or len(payload) != actual["size_bytes"] or sha256_bytes(payload) != actual["sha256"]:
            _fail("scheduler_input_bytes_mismatch", f"task-export.json.scheduler_input.{label}", actual["path"])
    expected_values = {
        "slot_id": slot.get("slot"),
        "profile": slot.get("capture_profile"),
        "kind": slot.get("kind"),
    }
    for field, expected in expected_values.items():
        if task.get(field) != expected:
            _fail("scheduler_slot_classification", f"task-export.json.{field}", f"expected {expected!r}")
    return {
        "schema": SCHEDULER_SCHEMA,
        "manifest_repository_path": SCHEDULER_MANIFEST_PATH,
        "manifest_sha256": sha256_bytes((REPO / SCHEDULER_MANIFEST_PATH).read_bytes()),
        "pack_id": _identifier(manifest.get("pack_id"), "scheduler_manifest.pack_id"),
        "slot_id": str(slot["slot"]),
        "execution_id": execution_id,
        "profile": str(slot["capture_profile"]),
        "kind": str(slot["kind"]),
        "input": input_binding,
        "launch_prompt": prompt_binding,
        "manifest_visible": False,
        "expected_outcomes_visible": False,
    }


def _validate_sources(
    task: Mapping[str, Any], sources: Mapping[str, bytes]
) -> dict[str, dict[str, Any]]:
    values = _sequence(task.get("supporting_artifacts"), "task-export.json.supporting_artifacts")
    artifacts: dict[str, dict[str, Any]] = {}
    for offset, value in enumerate(values):
        record = _binding(value, f"task-export.json.supporting_artifacts[{offset}]")
        logical = record["path"]
        if logical in artifacts:
            _fail("supporting_artifact_reused", f"task-export.json.supporting_artifacts[{offset}]", logical)
        payload = sources.get(logical)
        if payload is None or len(payload) != record["size_bytes"] or sha256_bytes(payload) != record["sha256"]:
            _fail("supporting_artifact_bytes_mismatch", f"task-export.json.supporting_artifacts[{offset}]", logical)
        artifacts[logical] = record
    scheduler = _mapping(task.get("scheduler_input"), "task-export.json.scheduler_input")
    expected_sources = {"task-export.json", str(_mapping(scheduler.get("input"), "scheduler.input").get("path")), str(_mapping(scheduler.get("launch_prompt"), "scheduler.launch_prompt").get("path")), *artifacts}
    if set(sources) != expected_sources:
        _fail("normalized_source_inventory", "normalized_capture.source_files", f"missing={sorted(expected_sources-set(sources))} extra={sorted(set(sources)-expected_sources)}")
    return artifacts


def _common_contract(
    task: Mapping[str, Any],
    identity: Mapping[str, str],
    now: datetime,
) -> tuple[str, str, str]:
    required = {
        "schema_version", "platform", "surface", "evidence_kind", "export_id",
        "task_id", "parent_task_or_thread_id", "observable_child_or_delegate_ids",
        "captured_at", "automatic_external_submission", "plugin_version",
        "source_commit", "manifest_sha256", "registry_sha256", "skill_tree_sha256",
        "slot_id", "profile", "kind", "scheduler_input", "capability",
        "supporting_artifacts", "platform_id_bindings", "slot_payload",
    }
    if set(task) != required or task.get("schema_version") != TASK_EXPORT_SCHEMA:
        _fail("task_export_fields", "task-export.json", f"expected {sorted(required)}")
    profile = _identifier(task.get("profile"), "task-export.json.profile")
    kind = _identifier(task.get("kind"), "task-export.json.kind")
    if PROFILE_TO_KIND.get(profile) != kind:
        _fail("profile_kind_mismatch", "task-export.json", f"{profile}/{kind}")
    task_id = _identifier(task.get("task_id"), "task-export.json.task_id")
    _identifier(task.get("export_id"), "task-export.json.export_id")
    _identifier(task.get("parent_task_or_thread_id"), "task-export.json.parent_task_or_thread_id")
    children = [_identifier(item, f"task-export.json.observable_child_or_delegate_ids[{offset}]") for offset, item in enumerate(_sequence(task.get("observable_child_or_delegate_ids"), "task-export.json.observable_child_or_delegate_ids"))]
    if len(children) != len(set(children)) or task_id in children:
        _fail("child_id_reused", "task-export.json.observable_child_or_delegate_ids", repr(children))
    _timestamp(task.get("captured_at"), "task-export.json.captured_at", now=now)
    if task.get("automatic_external_submission") is not False:
        _fail("submission_boundary", "task-export.json.automatic_external_submission", repr(task.get("automatic_external_submission")))
    for field in ("plugin_version", "source_commit", "manifest_sha256", "registry_sha256", "skill_tree_sha256"):
        if task.get(field) != identity.get(field):
            _fail("source_identity_mismatch", f"task-export.json.{field}", repr(task.get(field)))
    capability = _mapping(task.get("capability"), "task-export.json.capability")
    if set(capability) != {"name", "state", "task_or_tool_run_ids"}:
        _fail("capability_fields", "task-export.json.capability", str(sorted(capability)))
    _identifier(capability.get("name"), "task-export.json.capability.name")
    _identifier(capability.get("state"), "task-export.json.capability.state")
    run_ids = [_identifier(item, f"task-export.json.capability.task_or_tool_run_ids[{offset}]") for offset, item in enumerate(_sequence(capability.get("task_or_tool_run_ids"), "task-export.json.capability.task_or_tool_run_ids"))]
    if len(run_ids) != len(set(run_ids)):
        _fail("capability_run_id_reused", "task-export.json.capability.task_or_tool_run_ids", repr(run_ids))
    return profile, kind, task_id


def _validate_reviewer(
    task: Mapping[str, Any], artifacts: Mapping[str, Mapping[str, Any]],
    resolved: Mapping[str, Any], now: datetime,
) -> tuple[bool, dict[str, Any]]:
    payload = _mapping(_mapping(task.get("slot_payload"), "task-export.json.slot_payload").get("reviewer_run"), "task-export.json.slot_payload.reviewer_run")
    required = {
        "run_id", "reviewer_skill", "delegated_thread_id", "reviewer_instance_id",
        "reviewer_instance_created_at", "platform_receipt_id", "blind_bundle",
        "dispatch_prompt", "raw_transport_output", "report", "scope_authority",
        "platform_scope", "isolation_mode", "prior_scores_visible",
        "peer_outputs_visible", "target_decision_visible", "source_edits_performed",
    }
    if set(payload) != required:
        _fail("reviewer_payload_fields", "task-export.json.slot_payload.reviewer_run", str(sorted(payload)))
    if task.get("platform") != "codex" or task.get("surface") != "codex":
        _fail("reviewer_platform", "task-export.json", repr((task.get("platform"), task.get("surface"))))
    parent = _identifier(task.get("parent_task_or_thread_id"), "task-export.json.parent_task_or_thread_id")
    delegated = _identifier(payload.get("delegated_thread_id"), "reviewer_run.delegated_thread_id")
    instance = _identifier(payload.get("reviewer_instance_id"), "reviewer_run.reviewer_instance_id")
    created = _timestamp(payload.get("reviewer_instance_created_at"), "reviewer_run.reviewer_instance_created_at", now=now)
    receipt = _identifier(payload.get("platform_receipt_id"), "reviewer_run.platform_receipt_id")
    children = list(task.get("observable_child_or_delegate_ids", []))
    if children != [delegated]:
        _fail("reviewer_child_inventory", "task-export.json.observable_child_or_delegate_ids", repr(children))
    file_refs = {
        name: _file_ref(payload.get(name), f"reviewer_run.{name}", artifacts)
        for name in ("blind_bundle", "dispatch_prompt", "raw_transport_output", "report")
    }
    expected_bindings = {
        "task_id": task["task_id"],
        "parent_task_or_thread_id": parent,
        "parent_delegation_child_id": delegated,
        "delegated_thread_id": delegated,
        "captured_child_thread_id": delegated,
        "reviewer_instance_id": instance,
        "reviewer_instance_created_at": created,
        "platform_receipt_id": receipt,
        "captured_at": task["captured_at"],
        "delegated_prompt_sha256": file_refs["dispatch_prompt"]["sha256"],
    }
    for name, expected in expected_bindings.items():
        _require_resolved(resolved, name, expected, "reviewer")
    if datetime.fromisoformat(created.replace("Z", "+00:00")) > datetime.fromisoformat(str(task["captured_at"]).replace("Z", "+00:00")):
        _fail("reviewer_instance_chronology", "reviewer_run.reviewer_instance_created_at", created)
    if payload.get("isolation_mode") != "fresh_subagent" or any(payload.get(field) is not False for field in ("prior_scores_visible", "peer_outputs_visible", "target_decision_visible", "source_edits_performed")):
        _fail("reviewer_isolation_contract", "reviewer_run", "fresh isolated read-only reviewer required")
    scope = _mapping(payload.get("platform_scope"), "reviewer_run.platform_scope")
    required_scope = {"files_read", "files_written", "input_digest_before", "input_digest_after", "source_edits_performed"}
    if set(scope) != required_scope:
        _fail("reviewer_scope_fields", "reviewer_run.platform_scope", str(sorted(scope)))
    authority = payload.get("scope_authority")
    if authority not in {"platform_derived", "task_recorded"}:
        _fail("reviewer_scope_authority", "reviewer_run.scope_authority", repr(authority))
    files_read = [_string(item, "reviewer_run.platform_scope.files_read") for item in _sequence(scope.get("files_read"), "reviewer_run.platform_scope.files_read")]
    files_written = [_string(item, "reviewer_run.platform_scope.files_written") for item in _sequence(scope.get("files_written"), "reviewer_run.platform_scope.files_written")]
    for value in (*files_read, *files_written):
        canonical_relative(value, "reviewer_run.platform_scope.file")
    report_path = _mapping(payload["report"], "reviewer_run.report")["path"]
    if files_written != [report_path] or scope.get("source_edits_performed") is not False:
        _fail("reviewer_write_scope", "reviewer_run.platform_scope", repr(files_written))
    before = _canonical_digest(scope.get("input_digest_before"), "reviewer_run.platform_scope.input_digest_before")
    after = _canonical_digest(scope.get("input_digest_after"), "reviewer_run.platform_scope.input_digest_after")
    scheduler_input = _mapping(_mapping(task["scheduler_input"], "scheduler_input")["input"], "scheduler_input.input")
    if before != after or before != scheduler_input.get("sha256"):
        _fail("reviewer_source_immutability", "reviewer_run.platform_scope", f"{before}/{after}")
    if scheduler_input.get("path") not in files_read or scheduler_input.get("path") in files_written:
        _fail("reviewer_source_access", "reviewer_run.platform_scope", str(scheduler_input.get("path")))
    platform_derived = authority == "platform_derived"
    if platform_derived:
        for name, expected in (
            ("files_read", files_read), ("files_written", files_written),
            ("input_digest_before", before), ("input_digest_after", after),
            ("source_edits_performed", False),
        ):
            _require_resolved(resolved, name, expected, "reviewer_scope")
    return platform_derived, dict(payload)


def _opened_sources_and_claims(retrieval: Mapping[str, Any]) -> tuple[list[Mapping[str, Any]], list[Mapping[str, Any]]]:
    opened = [_mapping(item, f"retrieval.opened_sources[{offset}]") for offset, item in enumerate(_sequence(retrieval.get("opened_sources"), "retrieval.opened_sources"))]
    if len(opened) < 2:
        _fail("insufficient_opened_sources", "retrieval.opened_sources", str(len(opened)))
    source_ids: set[str] = set()
    for offset, source in enumerate(opened):
        source_id = _identifier(source.get("source_id"), f"retrieval.opened_sources[{offset}].source_id")
        url = _string(source.get("url"), f"retrieval.opened_sources[{offset}].url")
        if not re.fullmatch(r"https://[^\s]+", url):
            _fail("noncanonical_source_url", f"retrieval.opened_sources[{offset}].url", url)
        if source.get("primary_or_authoritative") is not True or source.get("identity_verified") is not True or source_id in source_ids:
            _fail("source_identity_contract", f"retrieval.opened_sources[{offset}]", source_id)
        source_ids.add(source_id)
    claims = [_mapping(item, f"retrieval.material_claim_trace[{offset}]") for offset, item in enumerate(_sequence(retrieval.get("material_claim_trace"), "retrieval.material_claim_trace"))]
    if not claims:
        _fail("material_claim_trace_empty", "retrieval.material_claim_trace", "at least one material claim required")
    for offset, claim in enumerate(claims):
        _identifier(claim.get("claim_id"), f"retrieval.material_claim_trace[{offset}].claim_id")
        cited = [_identifier(item, f"retrieval.material_claim_trace[{offset}].source_ids") for item in _sequence(claim.get("source_ids"), f"retrieval.material_claim_trace[{offset}].source_ids")]
        if claim.get("material") is not True or not cited or not set(cited).issubset(source_ids):
            _fail("material_claim_untraced", f"retrieval.material_claim_trace[{offset}]", repr(cited))
    return opened, claims


def _require_self_contained_artifact(
    value: Any,
    *,
    artifacts: Mapping[str, Mapping[str, Any]],
    sources: Mapping[str, bytes],
    label: str,
    content_field: str,
) -> dict[str, Any]:
    record = _file_ref(value, label, artifacts)
    payload = sources[record["path"]]
    if PurePosixPath(record["path"]).suffix.lower() == ".json":
        document = _mapping(_strict_json(payload, record["path"]), record["path"])
    else:
        document = _strict_yaml(payload, record["path"])
    if document.get("schema_version") not in {1, "1"} or not isinstance(document.get(content_field), str) or not str(document.get(content_field)).strip():
        _fail("continuation_artifact_not_self_contained", label, f"requires schema_version and {content_field}")
    return record


def _validate_search(
    task: Mapping[str, Any], artifacts: Mapping[str, Mapping[str, Any]], resolved: Mapping[str, Any]
) -> tuple[bool, dict[str, Any]]:
    retrieval = _mapping(_mapping(task.get("slot_payload"), "task-export.json.slot_payload").get("retrieval"), "task-export.json.slot_payload.retrieval")
    if retrieval.get("kind") != "search" or task.get("surface") not in {"chatgpt", "codex"}:
        _fail("search_surface_or_kind", "retrieval", repr((task.get("surface"), retrieval.get("kind"))))
    for field in ("raw_search_output", "citation_export"):
        _file_ref(retrieval.get(field), f"retrieval.{field}", artifacts)
    query = _string(retrieval.get("query"), "retrieval.query")
    digest = _canonical_digest(retrieval.get("query_or_request_digest"), "retrieval.query_or_request_digest")
    if digest != sha256_bytes(query.encode("utf-8")):
        _fail("search_query_digest", "retrieval.query_or_request_digest", digest)
    opened, claims = _opened_sources_and_claims(retrieval)
    if retrieval.get("local_retrieval_fallback") is not False or retrieval.get("inline_simulation") is not False:
        _fail("search_native_capability", "retrieval", "native structured Search trace required")
    capability = _mapping(task.get("capability"), "task-export.json.capability")
    if capability.get("name") != "chatgpt_codex_builtin_search" or capability.get("state") != "active":
        _fail("search_capability", "task-export.json.capability", repr(capability))
    tool_id = _identifier(retrieval.get("tool_id"), "retrieval.tool_id")
    run_id = _identifier(retrieval.get("tool_run_id"), "retrieval.tool_run_id")
    if capability.get("task_or_tool_run_ids") != [tool_id, run_id]:
        _fail("search_tool_run_ids", "task-export.json.capability.task_or_tool_run_ids", repr(capability.get("task_or_tool_run_ids")))
    expected = {
        "task_id": task["task_id"], "captured_at": task["captured_at"],
        "search_tool_id": tool_id, "search_tool_run_id": run_id,
        "search_query": query, "opened_sources": opened,
        "citation_metadata": retrieval.get("citation_metadata"),
        "material_claim_trace": claims,
    }
    for name, value in expected.items():
        _require_resolved(resolved, name, value, "search")
    citations = _sequence(retrieval.get("citation_metadata"), "retrieval.citation_metadata")
    opened_ids = {item["source_id"] for item in opened}
    if not citations or any(not isinstance(item, Mapping) or item.get("source_id") not in opened_ids for item in citations):
        _fail("citation_metadata_unbound", "retrieval.citation_metadata", repr(citations))
    return True, dict(retrieval)


def _validate_deep_research(
    task: Mapping[str, Any], artifacts: Mapping[str, Mapping[str, Any]],
    sources: Mapping[str, bytes], _platform_documents: Mapping[str, Mapping[str, Any]], _resolved: Mapping[str, Any], _now: datetime,
) -> tuple[bool, dict[str, Any]]:
    retrieval = _mapping(_mapping(task.get("slot_payload"), "task-export.json.slot_payload").get("retrieval"), "task-export.json.slot_payload.retrieval")
    if retrieval.get("kind") != "deep_research_completed":
        _fail("deep_research_kind", "retrieval.kind", repr(retrieval.get("kind")))
    projection = _mapping(retrieval.get("completion_projection"), "retrieval.completion_projection")
    status = projection.get("status")
    if status == "pending":
        if set(projection) != {"status", "reason"} or not _string(projection.get("reason"), "retrieval.completion_projection.reason"):
            _fail("deep_research_pending_projection", "retrieval.completion_projection", repr(projection))
        _require_self_contained_artifact(
            retrieval.get("handoff_artifact"), artifacts=artifacts, sources=sources,
            label="retrieval.handoff_artifact", content_field="request",
        )
        _require_self_contained_artifact(
            retrieval.get("continuation_artifact"), artifacts=artifacts, sources=sources,
            label="retrieval.continuation_artifact", content_field="next_action",
        )
        _identifier(retrieval.get("pending_edge_id"), "retrieval.pending_edge_id")
        if retrieval.get("workflow_paused") is not True or retrieval.get("inline_simulation") is not False:
            _fail(
                "deep_research_pending_stop_contract",
                "retrieval",
                "pending completion projection must pause without inline simulation",
            )
        forbidden_claims = {"deep_research_session_id", "deep_research_run_id", "provider_completion_receipt_id", "provider_completion_status"}
        if forbidden_claims.intersection(retrieval):
            _fail("deep_research_pending_claims_completion", "retrieval", str(sorted(forbidden_claims.intersection(retrieval))))
        return False, dict(retrieval)
    if status != "platform_export_derived" or set(projection) != {"status", "source_path", "export_kind"}:
        _fail("deep_research_completion_projection", "retrieval.completion_projection", repr(projection))
    source_path = _string(projection.get("source_path"), "retrieval.completion_projection.source_path")
    if PurePosixPath(source_path).suffix.lower() in NON_PROVIDER_EXPORT_SUFFIXES:
        _fail("deep_research_report_not_completion_evidence", "retrieval.completion_projection.source_path", source_path)
    _fail(
        "deep_research_export_adapter_unavailable",
        "retrieval.completion_projection",
        "no concrete Deep Research event-export schema/parser is registered",
    )


def _validate_inactive(
    task: Mapping[str, Any], artifacts: Mapping[str, Mapping[str, Any]],
    sources: Mapping[str, bytes], platform_documents: Mapping[str, Mapping[str, Any]], resolved: Mapping[str, Any], now: datetime,
) -> tuple[bool, dict[str, Any]]:
    retrieval = _mapping(_mapping(task.get("slot_payload"), "task-export.json.slot_payload").get("retrieval"), "task-export.json.slot_payload.retrieval")
    if retrieval.get("kind") != "deep_research_inactive_control":
        _fail("inactive_kind", "retrieval.kind", repr(retrieval.get("kind")))
    capability_ref = _file_ref(retrieval.get("capability_state_export"), "retrieval.capability_state_export", artifacts)
    if capability_ref["artifact_type"] != "capability_export" or capability_ref["path"] not in platform_documents:
        _fail("inactive_capability_export", "retrieval.capability_state_export", capability_ref["path"])
    _require_self_contained_artifact(
        retrieval.get("handoff_artifact"), artifacts=artifacts, sources=sources,
        label="retrieval.handoff_artifact", content_field="request",
    )
    _require_self_contained_artifact(
        retrieval.get("continuation_artifact"), artifacts=artifacts, sources=sources,
        label="retrieval.continuation_artifact", content_field="next_action",
    )
    state = _identifier(retrieval.get("capability_state"), "retrieval.capability_state")
    if state not in {"inactive", "unavailable", "cannot_start"}:
        _fail("inactive_capability_state", "retrieval.capability_state", state)
    if retrieval.get("workflow_paused") is not True or retrieval.get("downstream_evidence_map_created") is not False or retrieval.get("inline_simulation") is not False:
        _fail("inactive_stop_contract", "retrieval", "workflow must pause without inline research or evidence map")
    _identifier(retrieval.get("pending_edge_id"), "retrieval.pending_edge_id")
    _require_resolved(resolved, "task_id", task["task_id"], "inactive")
    _require_resolved(resolved, "captured_at", task["captured_at"], "inactive")
    _require_resolved(resolved, "capability_state", state, "inactive")
    _timestamp(_require_resolved(resolved, "capability_observed_at", retrieval.get("capability_observed_at"), "inactive"), "retrieval.capability_observed_at", now=now)
    capability = _mapping(task.get("capability"), "task-export.json.capability")
    if capability.get("name") != "chatgpt_deep_research" or capability.get("state") != state or capability.get("task_or_tool_run_ids"):
        _fail("inactive_capability_contract", "task-export.json.capability", repr(capability))
    return True, dict(retrieval)


def _adapter_digest() -> str:
    digest = hashlib.sha256()
    for path in (Path(__file__).resolve(), REPO / "scripts" / "openai_preview_capture_contracts.py"):
        digest.update(path.relative_to(REPO).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def frozen_source_identity() -> dict[str, str]:
    try:
        diff = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *FROZEN_PATHS], cwd=REPO, check=False, capture_output=True, timeout=20)
        untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", *FROZEN_PATHS], cwd=REPO, check=True, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError) as exc:
        _fail("git_state_unavailable", "source_identity", f"{type(exc).__name__}: {exc}")
    if diff.returncode not in {0, 1} or diff.returncode == 1 or untracked.stdout.strip():
        _fail("installable_tree_dirty", "source_identity", "Phase 8 capture contract or frozen input pack differs from HEAD")
    return current_checkout_source_identity()


def _validate_derived(
    task: Mapping[str, Any], sources: Mapping[str, bytes], manifest: Mapping[str, Any],
    identity: Mapping[str, str], now: datetime,
) -> dict[str, Any]:
    profile, kind, task_id = _common_contract(task, identity, now)
    artifacts = _validate_sources(task, sources)
    scheduler_binding = _validate_scheduler(manifest, task, sources, identity)
    platform_documents = _structured_json_sources(artifacts, sources)
    resolved, id_provenance = _resolve_platform_bindings(task, platform_documents)
    pending_dr = profile == "phase8-deep-research-v1" and _mapping(_mapping(task["slot_payload"], "slot_payload").get("retrieval"), "slot_payload.retrieval").get("completion_projection", {}).get("status") == "pending"
    if not pending_dr:
        _require_resolved(resolved, "capture_export_id", task["export_id"], "common")
        _require_resolved(resolved, "task_id", task_id, "common")
        _require_resolved(resolved, "captured_at", task["captured_at"], "common")
    if profile == "phase8-reviewer-v1":
        claimed_platform_trace_complete, slot_payload = _validate_reviewer(task, artifacts, resolved, now)
    elif profile == "phase8-search-v1":
        claimed_platform_trace_complete, slot_payload = _validate_search(task, artifacts, resolved)
    elif profile == "phase8-deep-research-v1":
        claimed_platform_trace_complete, slot_payload = _validate_deep_research(task, artifacts, sources, platform_documents, resolved, now)
    else:
        claimed_platform_trace_complete, slot_payload = _validate_inactive(task, artifacts, sources, platform_documents, resolved, now)

    # A task-authored artifact label plus internally consistent JSON pointers
    # is not a platform capture adapter.  Keep all three currently unsupported
    # positive profiles non-counting even when their claim documents are
    # structurally complete.  Completed Deep Research is already fail-closed
    # inside its profile validator.
    live_eligible = (
        claimed_platform_trace_complete
        if profile == "phase8-deep-research-v1"
        else False
    )
    if live_eligible:
        capture_status = "platform_trace_complete"
    elif profile == "phase8-deep-research-v1":
        capture_status = "provider_completion_projection_pending"
    elif profile == "phase8-reviewer-v1" and not claimed_platform_trace_complete:
        capture_status = "task_recorded_scope_pending"
    else:
        capture_status = "platform_capture_adapter_pending"
    return {
        "profile": profile,
        "kind": kind,
        "task_id": task_id,
        "scheduler_binding": scheduler_binding,
        "artifacts": artifacts,
        "id_provenance": id_provenance,
        "slot_payload": slot_payload,
        "live_eligible": live_eligible,
        "capture_status": capture_status,
    }


def validate_normalized_capture(
    document: Mapping[str, Any], *, now: datetime, verify_checkout: bool = True
) -> Mapping[str, Any]:
    if document.get("schema_version") != CAPTURE_SCHEMA_VERSION or document.get("normalization_schema") != PHASE8_NORMALIZED_CAPTURE_SCHEMA:
        _fail("unsupported_schema", "normalized_capture.normalization_schema", repr(document.get("normalization_schema")))
    for field, expected in (("verification_level", "capture_only"), ("provider_verified", False), ("counts_as_preview_acceptance", False), ("synthetic_test_only", False)):
        if document.get(field) != expected:
            _fail("normalized_claim_mismatch", f"normalized_capture.{field}", repr(document.get(field)))
    evidence_id = _identifier(document.get("evidence_id"), "normalized_capture.evidence_id")
    captured_at = _timestamp(document.get("captured_at"), "normalized_capture.captured_at", now=now)
    identity = dict(_mapping(document.get("source_identity"), "normalized_capture.source_identity"))
    adapter = _mapping(document.get("capture_adapter"), "normalized_capture.capture_adapter")
    if adapter != {"adapter_id": PHASE8_CAPTURE_ADAPTER_ID, "adapter_code_sha256": _adapter_digest()}:
        _fail("capture_adapter_mismatch", "normalized_capture.capture_adapter", repr(adapter))
    sources = _decode_sources(document)
    task = _mapping(_strict_json(sources.get("task-export.json", b""), "task-export.json"), "task-export.json")
    try:
        repository_manifest = (REPO / SCHEDULER_MANIFEST_PATH).read_bytes()
    except OSError as exc:
        _fail("scheduler_manifest_unavailable", SCHEDULER_MANIFEST_PATH, str(exc))
    manifest = _strict_yaml(repository_manifest, "scheduler_manifest")
    derived = _validate_derived(task, sources, manifest, identity, now)
    if document.get("profile") != derived["profile"] or document.get("platform") != task.get("platform") or document.get("surface") != task.get("surface") or document.get("capture_export_id") != task.get("export_id") or document.get("task_id") != derived["task_id"] or document.get("parent_task_or_thread_id") != task.get("parent_task_or_thread_id") or document.get("observable_child_or_delegate_ids") != task.get("observable_child_or_delegate_ids") or document.get("captured_at") != task.get("captured_at"):
        _fail("normalized_capture_derivation_mismatch", "normalized_capture", evidence_id)
    if document.get("scheduler_binding") != derived["scheduler_binding"] or document.get("supporting_artifacts") != list(derived["artifacts"].values()) or document.get("slot_payload") != derived["slot_payload"] or document.get("capture_status") != derived["capture_status"] or document.get("live_collection_eligible") is not derived["live_eligible"]:
        _fail("normalized_payload_derivation_mismatch", "normalized_capture", evidence_id)
    provenance = _mapping(document.get("capture_provenance"), "normalized_capture.capture_provenance")
    if provenance.get("id_bindings") != derived["id_provenance"] or provenance.get("scope_classification") != ("platform_derived" if derived["live_eligible"] else "non_counting_pending"):
        _fail("normalized_provenance_mismatch", "normalized_capture.capture_provenance", evidence_id)
    capture = _mapping(document.get("capture"), "normalized_capture.capture")
    expected_capture = {
        "surface": str(task["surface"]),
        "task_or_thread_id": derived["task_id"],
        "evidence_kind": "task_export",
        "profile": derived["profile"],
        "slot_id": str(task["slot_id"]),
    }
    if dict(capture) != expected_capture:
        _fail("normalized_capture_projection", "normalized_capture.capture", repr(capture))
    if verify_checkout and identity != frozen_source_identity():
        _fail("source_identity_mismatch", "normalized_capture.source_identity", evidence_id)
    return {
        "evidence_id": evidence_id,
        "captured_at": captured_at,
        "source_identity": identity,
        "adapter": dict(adapter),
        "capture": expected_capture,
        "scheduler_binding": derived["scheduler_binding"],
        "profile": derived["profile"],
        "slot_id": str(task["slot_id"]),
        "live_collection_eligible": derived["live_eligible"],
        "capture_status": derived["capture_status"],
        "decoded_source_files": sources,
        "task_export": task,
    }


def normalize_capture(
    *, staging: StagingRoot, capture_root: str, task_export: str,
    scheduler_manifest: str, output: str, evidence_id: str, now: datetime,
    verify_checkout: bool = True,
) -> tuple[Path, Mapping[str, Any]]:
    root = staging.input_directory(capture_root, "cli.capture_root")
    task_path = staging.input_file(task_export, "cli.task_export")
    manifest_path = staging.input_file(scheduler_manifest, "cli.scheduler_manifest")
    output_path = staging.output_file(output, "cli.output")
    repository_manifest = REPO / SCHEDULER_MANIFEST_PATH
    if manifest_path.read_bytes() != repository_manifest.read_bytes():
        _fail("scheduler_manifest_not_committed", "cli.scheduler_manifest", SCHEDULER_MANIFEST_PATH)
    task = _mapping(_strict_json(task_path.read_bytes(), "task-export.json"), "task-export.json")
    identity = frozen_source_identity() if verify_checkout else current_checkout_source_identity()
    scheduler = _mapping(task.get("scheduler_input"), "task-export.json.scheduler_input")
    artifact_bindings = [_binding(value, f"task-export.json.supporting_artifacts[{offset}]") for offset, value in enumerate(_sequence(task.get("supporting_artifacts"), "task-export.json.supporting_artifacts"))]
    scheduler_bindings = [_binding(scheduler.get("input"), "task-export.json.scheduler_input.input"), _binding(scheduler.get("launch_prompt"), "task-export.json.scheduler_input.launch_prompt")]
    sources: dict[str, bytes] = {"task-export.json": task_path.read_bytes()}
    source_paths = [task_path, manifest_path, output_path]
    for record in [*scheduler_bindings, *artifact_bindings]:
        candidate = (root / Path(*PurePosixPath(record["path"]).parts)).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            _fail("path_escape", record["path"], str(candidate))
        if not candidate.is_file() or candidate.is_symlink():
            _fail("file_missing", record["path"], str(candidate))
        payload = candidate.read_bytes()
        if len(payload) != record["size_bytes"] or sha256_bytes(payload) != record["sha256"]:
            _fail("source_binding_mismatch", record["path"], str(candidate))
        sources[record["path"]] = payload
        source_paths.append(candidate)
    require_distinct_paths(source_paths, "phase8_capture_inputs_and_output")
    manifest = _strict_yaml(manifest_path.read_bytes(), "scheduler_manifest")
    derived = _validate_derived(task, sources, manifest, identity, now)
    normalized = {
        "schema_version": CAPTURE_SCHEMA_VERSION,
        "normalization_schema": PHASE8_NORMALIZED_CAPTURE_SCHEMA,
        "evidence_id": _identifier(evidence_id, "cli.evidence_id"),
        "verification_level": "capture_only",
        "provider_verified": False,
        "counts_as_preview_acceptance": False,
        "synthetic_test_only": False,
        "profile": derived["profile"],
        "platform": task["platform"],
        "surface": task["surface"],
        "capture_export_id": task["export_id"],
        "task_id": derived["task_id"],
        "parent_task_or_thread_id": task["parent_task_or_thread_id"],
        "observable_child_or_delegate_ids": task["observable_child_or_delegate_ids"],
        "captured_at": task["captured_at"],
        "source_identity": identity,
        "capture_status": derived["capture_status"],
        "live_collection_eligible": derived["live_eligible"],
        "capture_adapter": {"adapter_id": PHASE8_CAPTURE_ADAPTER_ID, "adapter_code_sha256": _adapter_digest()},
        "capture": {
            "surface": task["surface"], "task_or_thread_id": derived["task_id"],
            "evidence_kind": "task_export", "profile": derived["profile"], "slot_id": task["slot_id"],
        },
        "capture_provenance": {
            "id_bindings": derived["id_provenance"],
            "scope_classification": "platform_derived" if derived["live_eligible"] else "non_counting_pending",
        },
        "scheduler_binding": derived["scheduler_binding"],
        "supporting_artifacts": list(derived["artifacts"].values()),
        "slot_payload": derived["slot_payload"],
        "source_files": {logical: _source_record(payload) for logical, payload in sorted(sources.items())},
    }
    output_path.write_bytes(canonical_json_bytes(normalized))
    return output_path, normalized


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _fail("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("--staging-root", required=True)
    parser.add_argument("--capture-root", required=True)
    parser.add_argument("--task-export", required=True)
    parser.add_argument("--scheduler-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument("--now")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        output, normalized = normalize_capture(
            staging=StagingRoot(args.staging_root), capture_root=args.capture_root,
            task_export=args.task_export, scheduler_manifest=args.scheduler_manifest,
            output=args.output, evidence_id=args.evidence_id, now=parse_clock(args.now),
        )
        result = {
            "schema_version": "openai-phase8-capture-normalization-result/v1",
            "normalized": True,
            "gate_eligible": False,
            "live_collection_eligible": normalized["live_collection_eligible"],
            "capture_status": normalized["capture_status"],
            "output": str(output),
            "sha256": sha256_bytes(output.read_bytes()),
        }
    except CaptureNormalizationError as exc:
        result = {"schema_version": "openai-phase8-capture-normalization-result/v1", "normalized": False, "gate_eligible": False, "error": {"code": exc.code, "path": exc.path, "message": exc.message}}
        code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        result = {"schema_version": "openai-phase8-capture-normalization-result/v1", "normalized": False, "gate_eligible": False, "error": {"code": "internal_error", "path": "cli", "message": f"{type(exc).__name__}: {exc}"}}
        code = 3
    else:
        code = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
