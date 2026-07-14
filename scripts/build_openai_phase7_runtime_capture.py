#!/usr/bin/env python3
"""Derive Phase 7 receipts, collections, and workspace manifests from captures.

All commands are non-gating.  ``receipt`` derives one candidate receipt only
from a normalized task export and its digest-bound actor, artifact, and file
access documents.  ``collection`` assembles exactly the ten required slots.
``workspace-manifest`` runs only after those files and the collection have real
GitHub draft-Release asset API objects; it never invents an asset ID.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

from build_openai_preview_mini_bundle import _asset_snapshot, _release_snapshot
from normalize_openai_preview_capture import (
    CaptureNormalizationError,
    SCHEDULER_BINDING_SCHEMA,
    SCHEDULER_MANIFEST_REPOSITORY_PATH,
    StagingRoot,
    _identifier,
    _mapping,
    _strict_json,
    _strict_yaml_mapping,
    canonical_json_bytes,
    canonical_relative,
    frozen_source_identity,
    parse_clock,
    require_distinct_paths,
    validate_normalized_capture,
)
from openai_preview_evidence import PREVIEW_ATTESTED, sha256_bytes


REPO = Path(__file__).resolve().parents[1]
RUNTIME_SCHEMA_PATH = REPO / "tests" / "openai_phase7" / "runtime-receipts.schema.yaml"
REGISTRY_PATH = REPO / "research-skills-openai" / "workflow-registry.yaml"
RECEIPT_PLAN_SCHEMA = "openai-phase7-receipt-plan/v1"
WORKSPACE_ASSET_MAP_SCHEMA = "openai-phase7-workspace-asset-map/v1"
WORKSPACE_MANIFEST_SCHEMA = "openai-phase7-workspace-manifest/v1"
RESULT_SCHEMA = "openai-phase7-runtime-capture-build-result/v1"


class RuntimeCaptureBuildError(ValueError):
    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


def _fail(code: str, path: str, message: str) -> None:
    raise RuntimeCaptureBuildError(code, path, message)


def _read_json(path: Path, label: str) -> tuple[Mapping[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        _fail("file_read_failed", label, str(exc))
    try:
        return _mapping(_strict_json(payload, label), label), payload
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)


def _runtime_contract() -> Mapping[str, Any]:
    try:
        document = yaml.safe_load(RUNTIME_SCHEMA_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("runtime_schema_invalid", "runtime_schema", str(exc))
    return _mapping(document, "runtime_schema")


def _registered_workflow_edges(workflow: str) -> set[tuple[str, str, str, str]]:
    try:
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("workflow_registry_invalid", "workflow_registry", str(exc))
    document = _mapping(registry, "workflow_registry")
    edges = document.get("workflow_edges")
    if not isinstance(edges, list):
        _fail("workflow_registry_invalid", "workflow_registry.workflow_edges", "expected array")
    return {
        (
            str(edge.get("source")),
            str(edge.get("destination")),
            str(edge.get("dispatch_mode")),
            str(edge.get("trigger")),
        )
        for value in edges
        for edge in [_mapping(value, "workflow_registry.workflow_edges[]")]
        if edge.get("workflow") == workflow
    }


def _binding(document: Mapping[str, Any], field: str, payload: bytes, label: str) -> Mapping[str, Any]:
    binding = _mapping(document.get(field), f"R.{field}")
    if binding.get("sha256") != sha256_bytes(payload):
        _fail("supporting_digest_mismatch", f"R.{field}.sha256", label)
    logical_path = binding.get("path")
    if not isinstance(logical_path, str):
        _fail("supporting_path_invalid", f"R.{field}.path", repr(logical_path))
    canonical_relative(logical_path, f"R.{field}.path")
    return binding


def _identity_document(
    document: Mapping[str, Any],
    *,
    normalized: Mapping[str, Any],
    label: str,
) -> None:
    if document.get("schema_version") != 1:
        _fail("supporting_schema", f"{label}.schema_version", repr(document.get("schema_version")))
    expected = {
        "task_id": normalized["capture"]["task_or_thread_id"],
        "plugin_version": normalized["source_identity"]["plugin_version"],
        "registry_sha256": normalized["source_identity"]["registry_sha256"],
        "source_commit": normalized["source_identity"]["source_commit"],
    }
    for field in ("task_id", "plugin_version", "registry_sha256", "source_commit"):
        if document.get(field) != expected[field]:
            _fail("supporting_identity_mismatch", f"{label}.{field}", repr(document.get(field)))


def _validate_actor_and_scheduler_binding(
    *,
    raw: Mapping[str, Any],
    normalized: Mapping[str, Any],
    actor_manifest: Mapping[str, Any],
    reads: list[Any],
    writes: list[Any],
) -> Mapping[str, Any]:
    scheduler = _mapping(normalized.get("scheduler_binding"), "R.scheduler_binding")
    if scheduler.get("schema") != SCHEDULER_BINDING_SCHEMA:
        _fail("scheduler_binding_schema", "R.scheduler_binding.schema", repr(scheduler.get("schema")))
    if (
        scheduler.get("workflow") != raw.get("workflow")
        or scheduler.get("case_kind") != raw.get("case_kind")
        or scheduler.get("entry_mode") != raw.get("entry_mode")
        or raw.get("entry_mode")
        != _mapping(raw.get("scheduler_input"), "R.scheduler_input").get("entry_mode")
    ):
        _fail("scheduler_receipt_classification_mismatch", "R.scheduler_binding", "workflow/case/entry mode differs")
    parent_id = _identifier(
        raw.get("parent_task_or_thread_id"),
        "R.parent_task_or_thread_id",
    )
    if parent_id != raw.get("task_id") or scheduler.get("parent_task_or_thread_id") != parent_id:
        _fail("scheduler_parent_mismatch", "R.parent_task_or_thread_id", parent_id)
    child_values = raw.get("observable_child_or_delegate_ids")
    if not isinstance(child_values, list):
        _fail("scheduler_child_ids_invalid", "R.observable_child_or_delegate_ids", "expected array")
    child_ids = {
        _identifier(value, f"R.observable_child_or_delegate_ids[{offset}]")
        for offset, value in enumerate(child_values)
    }
    if len(child_ids) != len(child_values) or list(child_values) != scheduler.get("observable_child_or_delegate_ids"):
        _fail("scheduler_child_ids_mismatch", "R.observable_child_or_delegate_ids", repr(child_values))
    actor_values = actor_manifest.get("actors")
    if not isinstance(actor_values, list) or not actor_values:
        _fail("actor_manifest_empty", "actor_manifest.actors", "at least one actor is required")
    delegated_actor_ids: set[str] = set()
    all_actor_ids: set[str] = set()
    registered_edges = _registered_workflow_edges(str(raw.get("workflow")))
    for offset, value in enumerate(actor_values):
        actor = _mapping(value, f"actor_manifest.actors[{offset}]")
        actor_id = _identifier(actor.get("instance_id"), f"actor_manifest.actors[{offset}].instance_id")
        if actor_id in all_actor_ids or actor_id == parent_id:
            _fail("actor_instance_id_reused", f"actor_manifest.actors[{offset}].instance_id", actor_id)
        all_actor_ids.add(actor_id)
        dispatch_mode = actor.get("dispatch_mode")
        isolation_mode = actor.get("isolation_mode")
        if actor.get("role") == "orchestrator":
            if dispatch_mode is not None or isolation_mode is not None:
                _fail("root_actor_dispatch_invalid", f"actor_manifest.actors[{offset}]", actor_id)
            continue
        edge_identity = (
            str(actor.get("dispatch_source")),
            str(actor.get("skill")),
            str(dispatch_mode),
            str(actor.get("dispatch_trigger")),
        )
        if edge_identity not in registered_edges:
            _fail(
                "actor_dispatch_edge_mismatch",
                f"actor_manifest.actors[{offset}]",
                repr(edge_identity),
            )
        if dispatch_mode == "delegated":
            if isolation_mode != "fresh_subagent":
                _fail("delegated_actor_isolation_missing", f"actor_manifest.actors[{offset}]", actor_id)
            delegated_actor_ids.add(actor_id)
        elif isolation_mode == "fresh_subagent":
            _fail("orchestrated_actor_claims_fresh_subagent", f"actor_manifest.actors[{offset}]", actor_id)
    if child_ids != delegated_actor_ids:
        _fail(
            "observable_child_actor_mismatch",
            "actor_manifest.actors",
            f"declared={sorted(child_ids)} actors={sorted(delegated_actor_ids)}",
        )

    source = _mapping(scheduler.get("source"), "R.scheduler_binding.source")
    source_digest = str(source.get("sha256"))
    source_name = Path(str(source.get("path"))).name.casefold()
    matched_read_paths: set[str] = set()
    for offset, value in enumerate(reads):
        record = _mapping(value, f"file_access.reads[{offset}]")
        path = str(record.get("path"))
        if record.get("sha256") == source_digest and Path(path).name.casefold() == source_name:
            if record.get("sha256_before") != source_digest or record.get("sha256_after") != source_digest:
                _fail("scheduler_source_not_frozen", f"file_access.reads[{offset}]", path)
            matched_read_paths.add(path.casefold())
    if not matched_read_paths:
        _fail(
            "scheduler_source_not_read",
            "file_access.reads",
            f"no read binds {source.get('path')} at {source_digest}",
        )
    for offset, value in enumerate(writes):
        record = _mapping(value, f"file_access.writes[{offset}]")
        if str(record.get("path")).casefold() in matched_read_paths:
            _fail("scheduler_source_write_detected", f"file_access.writes[{offset}].path", str(record.get("path")))
    return scheduler


def build_receipt(
    *,
    staging: StagingRoot,
    raw_export: str,
    task_logical_path: str,
    actor_manifest: str,
    artifact_index: str,
    file_access: str,
    output: str,
    now: datetime,
) -> tuple[Path, Mapping[str, Any]]:
    paths = {
        "R": staging.input_file(raw_export, "cli.raw_export"),
        "actor_manifest": staging.input_file(actor_manifest, "cli.actor_manifest"),
        "artifact_index": staging.input_file(artifact_index, "cli.artifact_index"),
        "file_access": staging.input_file(file_access, "cli.file_access"),
    }
    output_path = staging.output_file(output, "cli.output")
    require_distinct_paths([*paths.values(), output_path], "receipt_inputs_and_output")
    raw, raw_bytes = _read_json(paths["R"], "R")
    try:
        normalized = validate_normalized_capture(raw, now=now, verify_checkout=True)
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    support: dict[str, Mapping[str, Any]] = {}
    support_bytes: dict[str, bytes] = {}
    for field in ("actor_manifest", "artifact_index", "file_access"):
        support[field], support_bytes[field] = _read_json(paths[field], field)
        _identity_document(support[field], normalized=normalized, label=field)
        if support[field].get("workflow") != raw.get("workflow"):
            _fail("supporting_workflow_mismatch", f"{field}.workflow", repr(support[field].get("workflow")))
        _binding(raw, field, support_bytes[field], field)
    artifacts = support["artifact_index"].get("artifacts")
    reads = support["file_access"].get("reads")
    writes = support["file_access"].get("writes")
    unchanged = support["file_access"].get("source_artifact_hashes_unchanged")
    if not isinstance(artifacts, list) or not isinstance(reads, list) or not isinstance(writes, list):
        _fail("supporting_collection_invalid", "supporting", "artifacts/reads/writes must be arrays")
    if unchanged is not True:
        _fail("source_immutability_unverified", "file_access.source_artifact_hashes_unchanged", repr(unchanged))
    for group, values in (("reads", reads), ("writes", writes)):
        for offset, value in enumerate(values):
            record = _mapping(value, f"file_access.{group}[{offset}]")
            for field in ("actor_instance_id", "path", "sha256"):
                if field not in record:
                    _fail("file_access_field_missing", f"file_access.{group}[{offset}].{field}", "required")
            canonical_relative(str(record["path"]), f"file_access.{group}[{offset}].path")
    scheduler_binding = _validate_actor_and_scheduler_binding(
        raw=raw,
        normalized=normalized,
        actor_manifest=support["actor_manifest"],
        reads=reads,
        writes=writes,
    )
    for field in ("lineage", "review_state", "control_evidence"):
        _mapping(raw.get(field), f"R.{field}")
    contract = _runtime_contract()
    workflow = raw.get("workflow")
    case_kind = raw.get("case_kind")
    contracts = contract.get("x-phase7-contract", {}).get("workflow_case_contracts", {})
    case = contracts.get(workflow, {}).get(case_kind) if isinstance(contracts, Mapping) else None
    if not isinstance(case, Mapping):
        _fail("workflow_case_contract_missing", "R.workflow", f"{workflow}/{case_kind}")
    expected_state = case.get("expected_final_state")
    if raw.get("final_state") != expected_state:
        _fail("final_state_contract_mismatch", "R.final_state", repr(raw.get("final_state")))
    task_path = task_logical_path
    canonical_relative(task_path, "cli.task_logical_path")
    receipt = {
        "receipt_id": normalized["evidence_id"],
        "workflow": workflow,
        "entry_mode": scheduler_binding["entry_mode"],
        "case_kind": case_kind,
        "expected_final_state": expected_state,
        "status": "verified",
        "binding": {
            "plugin_version": normalized["source_identity"]["plugin_version"],
            "registry_sha256": normalized["source_identity"]["registry_sha256"],
            "source_commit": normalized["source_identity"]["source_commit"],
            "task_export": {
                "platform": raw["platform"],
                "task_id": raw["task_id"],
                "entry_mode": scheduler_binding["entry_mode"],
                "path": task_path,
                "sha256": sha256_bytes(raw_bytes),
            },
            "actor_manifest": dict(raw["actor_manifest"]),
            "artifact_index": dict(raw["artifact_index"]),
            "file_access": dict(raw["file_access"]),
            "scheduler_input": dict(scheduler_binding),
        },
        "file_access": {
            "reads": reads,
            "writes": writes,
            "source_artifact_hashes_unchanged": True,
        },
        "lineage": dict(raw["lineage"]),
        "review_state": dict(raw["review_state"]),
        "control_evidence": dict(raw["control_evidence"]),
        "final_state": raw["final_state"],
        "automatic_external_submission": raw["automatic_external_submission"],
        "reason": "Machine-derived capture candidate; acceptance requires the external verifier chain.",
    }
    output_path.write_bytes(canonical_json_bytes(receipt))
    return output_path, receipt


def _validate_collection_scheduler_bindings(
    *,
    manifest_path: Path,
    receipts: list[Mapping[str, Any]],
) -> None:
    repository_manifest = REPO / SCHEDULER_MANIFEST_REPOSITORY_PATH
    try:
        manifest_bytes = manifest_path.read_bytes()
        repository_bytes = repository_manifest.read_bytes()
    except OSError as exc:
        _fail("scheduler_manifest_unavailable", "scheduler_manifest", str(exc))
    if manifest_bytes != repository_bytes:
        _fail("scheduler_manifest_not_committed", "scheduler_manifest", SCHEDULER_MANIFEST_REPOSITORY_PATH)
    identity = frozen_source_identity()
    manifest = _strict_yaml_mapping(manifest_bytes, "scheduler_manifest")
    slots = manifest.get("slots")
    if not isinstance(slots, list) or len(slots) != 10:
        _fail("scheduler_slot_count", "scheduler_manifest.slots", "exactly ten slots are required")
    plugin = _mapping(manifest.get("plugin_binding"), "scheduler_manifest.plugin_binding")
    if (
        plugin.get("plugin_name") != "research-skills-openai"
        or plugin.get("plugin_version") != identity["plugin_version"]
    ):
        _fail("scheduler_plugin_binding_mismatch", "scheduler_manifest.plugin_binding", repr(plugin))
    by_execution: dict[str, Mapping[str, Any]] = {}
    for offset, value in enumerate(slots):
        slot = _mapping(value, f"scheduler_manifest.slots[{offset}]")
        execution_id = _identifier(slot.get("execution_id"), f"scheduler_manifest.slots[{offset}].execution_id")
        if execution_id in by_execution:
            _fail("scheduler_execution_reused", f"scheduler_manifest.slots[{offset}]", execution_id)
        by_execution[execution_id] = slot

    manifest_digest = sha256_bytes(manifest_bytes)
    seen_slots: set[str] = set()
    seen_executions: set[str] = set()
    parent_ids: set[str] = set()
    child_ids: set[str] = set()
    scheduler_fields = {
        "schema",
        "manifest_schema",
        "manifest_repository_path",
        "manifest_sha256",
        "pack_id",
        "slot",
        "execution_id",
        "workflow",
        "case_kind",
        "public_entry",
        "entry_mode",
        "capture_profile",
        "plugin",
        "source",
        "launch_prompt",
        "parent_task_or_thread_id",
        "observable_child_or_delegate_ids",
        "platform_child_id_binding",
        "platform_user_message_binding",
        "manifest_visible_to_task",
        "manifest_visible_to_reviewers",
    }
    for offset, receipt in enumerate(receipts):
        binding = _mapping(receipt.get("binding"), f"receipts[{offset}].binding")
        scheduler = _mapping(binding.get("scheduler_input"), f"receipts[{offset}].binding.scheduler_input")
        if set(scheduler) != scheduler_fields or scheduler.get("schema") != SCHEDULER_BINDING_SCHEMA:
            _fail("scheduler_binding_fields", f"receipts[{offset}].binding.scheduler_input", "unexpected or missing fields")
        execution_id = _identifier(scheduler.get("execution_id"), f"receipts[{offset}].scheduler.execution_id")
        slot = by_execution.get(execution_id)
        if slot is None:
            _fail("scheduler_execution_not_found", f"receipts[{offset}].scheduler.execution_id", execution_id)
        slot_id = str(slot.get("slot"))
        if execution_id in seen_executions or slot_id in seen_slots:
            _fail("scheduler_slot_reused", f"receipts[{offset}].binding.scheduler_input", execution_id)
        seen_executions.add(execution_id)
        seen_slots.add(slot_id)
        expected = {
            "manifest_repository_path": SCHEDULER_MANIFEST_REPOSITORY_PATH,
            "manifest_sha256": manifest_digest,
            "pack_id": manifest.get("pack_id"),
            "slot": slot.get("slot"),
            "workflow": slot.get("workflow"),
            "case_kind": slot.get("case_kind"),
            "public_entry": slot.get("public_entry"),
            "entry_mode": slot.get("entry_mode"),
            "capture_profile": slot.get("capture_profile"),
            "manifest_visible_to_task": False,
            "manifest_visible_to_reviewers": False,
            "platform_child_id_binding": "structured_delegation_items_exact",
            "platform_user_message_binding": "single_exact_launch_prompt",
        }
        for field, value in expected.items():
            if scheduler.get(field) != value:
                _fail("scheduler_binding_mismatch", f"receipts[{offset}].scheduler.{field}", repr(scheduler.get(field)))
        if (
            receipt.get("workflow") != slot.get("workflow")
            or receipt.get("entry_mode") != slot.get("entry_mode")
            or receipt.get("case_kind") != slot.get("case_kind")
        ):
            _fail("scheduler_receipt_classification_mismatch", f"receipts[{offset}]", execution_id)
        if scheduler.get("source") != {"path": slot.get("source_path"), "sha256": slot.get("source_sha256")}:
            _fail("scheduler_source_binding_mismatch", f"receipts[{offset}].scheduler.source", execution_id)
        if scheduler.get("launch_prompt") != {"path": slot.get("prompt_path"), "sha256": slot.get("prompt_sha256")}:
            _fail("scheduler_prompt_binding_mismatch", f"receipts[{offset}].scheduler.launch_prompt", execution_id)
        if scheduler.get("plugin") != {
            "name": "research-skills-openai",
            "version": identity["plugin_version"],
            "source_commit": identity["source_commit"],
            "registry_sha256": identity["registry_sha256"],
        }:
            _fail("scheduler_plugin_binding_mismatch", f"receipts[{offset}].scheduler.plugin", execution_id)
        task = _mapping(binding.get("task_export"), f"receipts[{offset}].binding.task_export")
        if task.get("entry_mode") != slot.get("entry_mode"):
            _fail(
                "scheduler_task_entry_mode_mismatch",
                f"receipts[{offset}].binding.task_export.entry_mode",
                repr(task.get("entry_mode")),
            )
        task_path = str(task.get("path"))
        canonical_relative(task_path, f"receipts[{offset}].binding.task_export.path")
        if len(PurePosixPath(task_path).parts) < 2 or PurePosixPath(task_path).parts[:2] != ("runs", execution_id):
            _fail("scheduler_task_path_mismatch", f"receipts[{offset}].binding.task_export.path", task_path)
        parent = _identifier(scheduler.get("parent_task_or_thread_id"), f"receipts[{offset}].scheduler.parent")
        if task.get("task_id") != parent or parent in parent_ids:
            _fail("scheduler_parent_reused", f"receipts[{offset}].scheduler.parent", parent)
        parent_ids.add(parent)
        children = scheduler.get("observable_child_or_delegate_ids")
        if not isinstance(children, list) or not children:
            _fail("scheduler_child_ids_invalid", f"receipts[{offset}].scheduler.children", repr(children))
        for child_offset, child_value in enumerate(children):
            child = _identifier(child_value, f"receipts[{offset}].scheduler.children[{child_offset}]")
            if child in child_ids or child in parent_ids:
                _fail("scheduler_child_id_reused", f"receipts[{offset}].scheduler.children[{child_offset}]", child)
            child_ids.add(child)
    if seen_executions != set(by_execution) or len(seen_slots) != 10:
        _fail("scheduler_slot_coverage", "receipts", f"found {sorted(seen_executions)}")
    if parent_ids.intersection(child_ids):
        _fail("scheduler_parent_child_overlap", "receipts", repr(sorted(parent_ids.intersection(child_ids))))


def build_collection(
    *,
    staging: StagingRoot,
    plan_path_value: str,
    scheduler_manifest: str,
    output: str,
) -> tuple[Path, Mapping[str, Any]]:
    plan_path = staging.input_file(plan_path_value, "cli.plan")
    manifest_path = staging.input_file(scheduler_manifest, "cli.scheduler_manifest")
    output_path = staging.output_file(output, "cli.output")
    plan, _ = _read_json(plan_path, "plan")
    if plan.get("schema_version") != RECEIPT_PLAN_SCHEMA or set(plan) != {"schema_version", "receipts"}:
        _fail("receipt_plan_invalid", "plan", "schema and receipts are required")
    values = plan.get("receipts")
    if not isinstance(values, list) or len(values) != 10:
        _fail("receipt_count", "plan.receipts", f"expected 10, found {len(values) if isinstance(values, list) else 'non-array'}")
    receipt_paths = [
        staging.input_file(str(value), f"plan.receipts[{offset}]")
        for offset, value in enumerate(values)
    ]
    require_distinct_paths(
        [plan_path, manifest_path, *receipt_paths, output_path],
        "collection_inputs_and_output",
    )
    receipts = [_read_json(path, f"receipts[{offset}]")[0] for offset, path in enumerate(receipt_paths)]
    _validate_collection_scheduler_bindings(manifest_path=manifest_path, receipts=receipts)
    schema = _runtime_contract()
    required_pairs = [tuple(value) for value in schema["x-phase7-contract"]["required_workflow_case_pairs"]]
    actual_pairs = [(item.get("workflow"), item.get("case_kind")) for item in receipts]
    if sorted(actual_pairs) != sorted(required_pairs):
        _fail("receipt_pair_coverage", "receipts", str(actual_pairs))
    ids = [item.get("receipt_id") for item in receipts]
    tasks = [item.get("binding", {}).get("task_export", {}).get("task_id") for item in receipts]
    paths = [item.get("binding", {}).get("task_export", {}).get("path") for item in receipts]
    digests = [item.get("binding", {}).get("task_export", {}).get("sha256") for item in receipts]
    for label, values_ in (("receipt_id", ids), ("task_id", tasks), ("task_path", paths), ("task_digest", digests)):
        if any(value is None for value in values_) or len(values_) != len(set(values_)):
            _fail("receipt_identity_reused", f"receipts.{label}", str(values_))
    for field in ("actor_manifest", "artifact_index", "file_access"):
        support_paths = [item.get("binding", {}).get(field, {}).get("path") for item in receipts]
        support_digests = [item.get("binding", {}).get(field, {}).get("sha256") for item in receipts]
        for label, values_ in ((f"{field}_path", support_paths), (f"{field}_digest", support_digests)):
            if any(value is None for value in values_) or len(values_) != len(set(values_)):
                _fail("receipt_support_reused", f"receipts.{label}", str(values_))
    source_bindings = {
        (
            item["binding"]["plugin_version"],
            item["binding"]["registry_sha256"],
            item["binding"]["source_commit"],
        )
        for item in receipts
    }
    if len(source_bindings) != 1 or any(item.get("status") != "verified" for item in receipts):
        _fail("collection_source_or_status_mismatch", "receipts", str(source_bindings))
    collection = {
        "schema_version": 2,
        "evidence_kind": "current_version_durable_runtime_receipts",
        "platform_trust": {
            "adapter_status": "configured",
            "adapter_id": "github_release_asset_preview_v1",
            "verification_level": PREVIEW_ATTESTED,
            "provider_authenticated": False,
            "reason": "Candidate claims are accepted only after immutable Release and live GitHub re-query.",
        },
        "receipts": receipts,
    }
    output_path.write_bytes(canonical_json_bytes(collection))
    return output_path, collection


def _required_workspace_paths(receipt: Mapping[str, Any], task: Mapping[str, Any], artifact: Mapping[str, Any]) -> set[str]:
    binding = _mapping(receipt.get("binding"), "receipt.binding")
    required = {
        str(binding["task_export"]["path"]),
        str(binding["actor_manifest"]["path"]),
        str(binding["artifact_index"]["path"]),
        str(_mapping(task.get("file_access"), "R.file_access")["path"]),
    }
    for item in artifact.get("artifacts", []):
        required.add(str(_mapping(item, "artifact_index.artifacts[]")["path"]))
    access = _mapping(receipt.get("file_access"), "receipt.file_access")
    for group in ("reads", "writes"):
        for item in access.get(group, []):
            required.add(str(_mapping(item, f"receipt.file_access.{group}[]")["path"]))
    for value in required:
        canonical_relative(value, "workspace.required_path")
    return required


def build_workspace_manifest(
    *,
    staging: StagingRoot,
    collection_path_value: str,
    receipt_id: str,
    asset_map_path_value: str,
    release_snapshot: str,
    output: str,
    now: datetime,
) -> tuple[Path, Mapping[str, Any]]:
    collection_path = staging.input_file(collection_path_value, "cli.collection")
    asset_map_path = staging.input_file(asset_map_path_value, "cli.asset_map")
    release_path = staging.input_file(release_snapshot, "cli.release_snapshot")
    output_path = staging.output_file(output, "cli.output")
    collection, collection_bytes = _read_json(collection_path, "runtime_receipts")
    matches = [item for item in collection.get("receipts", []) if isinstance(item, Mapping) and item.get("receipt_id") == receipt_id]
    if len(matches) != 1:
        _fail("receipt_not_unique", "cli.receipt_id", receipt_id)
    receipt = matches[0]
    asset_map, _ = _read_json(asset_map_path, "asset_map")
    if asset_map.get("schema_version") != WORKSPACE_ASSET_MAP_SCHEMA or set(asset_map) != {"schema_version", "bundle_id", "runtime_receipts", "files"}:
        _fail("workspace_asset_map_invalid", "asset_map", "unexpected fields or schema")
    release_document, _ = _read_json(release_path, "github_release")
    release = _release_snapshot(release_document, now=now)
    records = [asset_map.get("runtime_receipts"), *(asset_map.get("files") or [])]
    if not isinstance(asset_map.get("files"), list):
        _fail("workspace_asset_map_invalid", "asset_map.files", "expected array")
    bindings: list[dict[str, Any]] = []
    control_paths = [collection_path, asset_map_path, release_path, output_path]
    data_paths: list[Path] = []
    seen_ids: set[int] = set()
    seen_logical: set[str] = set()
    task_document: Mapping[str, Any] | None = None
    artifact_document: Mapping[str, Any] | None = None
    for offset, value in enumerate(records):
        label = "asset_map.runtime_receipts" if offset == 0 else f"asset_map.files[{offset - 1}]"
        record = _mapping(value, label)
        if set(record) != {"logical_path", "path", "github_asset_snapshot"}:
            _fail("workspace_asset_record_fields", label, "expected logical_path, path, github_asset_snapshot")
        logical_path = str(record["logical_path"])
        canonical_relative(logical_path, f"{label}.logical_path")
        asset_path = staging.input_file(str(record["path"]), f"{label}.path")
        snapshot_path = staging.input_file(str(record["github_asset_snapshot"]), f"{label}.github_asset_snapshot")
        if offset == 0:
            if asset_path != collection_path:
                _fail("collection_asset_path_mismatch", f"{label}.path", str(asset_path))
            data_paths.append(snapshot_path)
        else:
            data_paths.extend((asset_path, snapshot_path))
        snapshot, _ = _read_json(snapshot_path, f"{label}.github_asset")
        asset = _asset_snapshot(
            snapshot,
            local_payload=asset_path.read_bytes(),
            local_name=asset_path.name,
            repository=release["repository"],
            release_assets=release["assets"],
            now=now,
            label=f"{label}.github_asset",
        )
        key = logical_path.casefold()
        if key in seen_logical or asset["asset_id"] in seen_ids:
            _fail("workspace_path_or_asset_reused", label, logical_path)
        seen_logical.add(key)
        seen_ids.add(asset["asset_id"])
        bindings.append(
            {
                "logical_path": logical_path,
                "asset_id": asset["asset_id"],
                "sha256": asset["sha256"],
                "size": asset["size"],
            }
        )
        if logical_path == receipt["binding"]["task_export"]["path"]:
            task_document, _ = _read_json(asset_path, "workspace.R")
        if logical_path == receipt["binding"]["artifact_index"]["path"]:
            artifact_document, _ = _read_json(asset_path, "workspace.artifact_index")
    require_distinct_paths([*control_paths, *data_paths], "workspace_inputs_and_output")
    if bindings[0]["sha256"] != sha256_bytes(collection_bytes):
        _fail("collection_asset_mismatch", "asset_map.runtime_receipts", receipt_id)
    if task_document is None or artifact_document is None:
        _fail("workspace_core_file_missing", "asset_map.files", receipt_id)
    required = _required_workspace_paths(receipt, task_document, artifact_document)
    actual = {item["logical_path"] for item in bindings[1:]}
    if actual != required:
        _fail("workspace_path_coverage", "asset_map.files", f"missing={sorted(required-actual)} extra={sorted(actual-required)}")
    try:
        normalized = validate_normalized_capture(task_document, now=now, verify_checkout=True)
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    manifest = {
        "schema_version": WORKSPACE_MANIFEST_SCHEMA,
        "bundle_id": str(asset_map["bundle_id"]),
        "receipt_id": receipt_id,
        "source_identity": normalized["source_identity"],
        "runtime_receipts": bindings[0],
        "files": bindings[1:],
    }
    output_path.write_bytes(canonical_json_bytes(manifest))
    return output_path, manifest


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _fail("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)
    receipt = subs.add_parser("receipt")
    receipt.add_argument("--staging-root", type=Path, required=True)
    receipt.add_argument("--raw-export", required=True)
    receipt.add_argument("--task-logical-path", required=True)
    receipt.add_argument("--actor-manifest", required=True)
    receipt.add_argument("--artifact-index", required=True)
    receipt.add_argument("--file-access", required=True)
    receipt.add_argument("--output", required=True)
    receipt.add_argument("--now")
    collection = subs.add_parser("collection")
    collection.add_argument("--staging-root", type=Path, required=True)
    collection.add_argument("--plan", required=True)
    collection.add_argument("--scheduler-manifest", required=True)
    collection.add_argument("--output", required=True)
    workspace = subs.add_parser("workspace-manifest")
    workspace.add_argument("--staging-root", type=Path, required=True)
    workspace.add_argument("--collection", required=True)
    workspace.add_argument("--receipt-id", required=True)
    workspace.add_argument("--asset-map", required=True)
    workspace.add_argument("--release-snapshot", required=True)
    workspace.add_argument("--output", required=True)
    workspace.add_argument("--now")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        staging = StagingRoot(args.staging_root)
        if args.command == "receipt":
            output, document = build_receipt(
                staging=staging,
                raw_export=args.raw_export,
                task_logical_path=args.task_logical_path,
                actor_manifest=args.actor_manifest,
                artifact_index=args.artifact_index,
                file_access=args.file_access,
                output=args.output,
                now=parse_clock(args.now),
            )
            node = "receipt"
            evidence_id = document["receipt_id"]
        elif args.command == "collection":
            output, document = build_collection(
                staging=staging,
                plan_path_value=args.plan,
                scheduler_manifest=args.scheduler_manifest,
                output=args.output,
            )
            node = "collection"
            evidence_id = "phase7-ten-slot-collection"
        else:
            output, document = build_workspace_manifest(
                staging=staging,
                collection_path_value=args.collection,
                receipt_id=args.receipt_id,
                asset_map_path_value=args.asset_map,
                release_snapshot=args.release_snapshot,
                output=args.output,
                now=parse_clock(args.now),
            )
            node = "workspace_manifest"
            evidence_id = document["receipt_id"]
        result = {
            "schema_version": RESULT_SCHEMA,
            "built": True,
            "node": node,
            "gate_eligible": False,
            "accepted": False,
            "evidence_id": evidence_id,
            "output": str(output),
            "sha256": sha256_bytes(output.read_bytes()),
        }
    except CaptureNormalizationError as exc:
        error = RuntimeCaptureBuildError(exc.code, exc.path, exc.message)
        result = {"schema_version": RESULT_SCHEMA, "built": False, "gate_eligible": False, "accepted": False, "error": {"code": error.code, "path": error.path, "message": error.message}}
        return_code = 2 if error.code == "invalid_cli_arguments" else 1
    except RuntimeCaptureBuildError as error:
        result = {"schema_version": RESULT_SCHEMA, "built": False, "gate_eligible": False, "accepted": False, "error": {"code": error.code, "path": error.path, "message": error.message}}
        return_code = 2 if error.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        result = {"schema_version": RESULT_SCHEMA, "built": False, "gate_eligible": False, "accepted": False, "error": {"code": "internal_error", "path": "cli", "message": f"{type(exc).__name__}: {exc}"}}
        return_code = 3
    else:
        return_code = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
