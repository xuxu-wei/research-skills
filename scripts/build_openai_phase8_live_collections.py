#!/usr/bin/env python3
"""Mechanically build Phase 8 collections and workspace manifests from R v2.

The builder never allocates Release asset IDs.  A complete build requires an
external binding document populated from GitHub API responses.  If any capture
is non-counting (currently all twelve slots, because no platform-origin
capture adapter is registered), the builder emits only a pending inventory and
no accept-capable collections.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

from normalize_openai_preview_capture import (
    CaptureNormalizationError,
    StagingRoot,
    _mapping,
    _sequence,
    _strict_json,
    _string,
    canonical_json_bytes,
    canonical_relative,
    parse_clock,
)
from openai_preview_capture_contracts import (
    PHASE8_NORMALIZED_CAPTURE_SCHEMA,
    validate_normalized_capture,
)
from openai_preview_evidence import normalize_sha256, sha256_bytes


REPO = Path(__file__).resolve().parents[1]
SCHEDULER_MANIFEST = REPO / "tests" / "openai_phase8" / "live-inputs" / "manifest.yaml"
PLAN_SCHEMA = "openai-phase8-live-collection-plan/v1"
ASSET_BINDINGS_SCHEMA = "openai-phase8-github-asset-bindings/v1"
WORKSPACE_MANIFEST_SCHEMA = "openai-phase8-workspace-manifest/v1"
PENDING_SCHEMA = "openai-phase8-live-collection-pending/v1"
REVIEWER_COLLECTION_SCHEMA = "openai-phase8-reviewer-receipt-collection/v2"
RETRIEVAL_COLLECTION_SCHEMA = "openai-phase8-retrieval-receipt-collection/v2"
RESULT_SCHEMA = "openai-phase8-live-collection-build-result/v1"
EXPECTED_DISTRIBUTION = {
    "reviewer": 6,
    "search": 3,
    "deep_research_completed": 2,
    "deep_research_inactive_control": 1,
}
IDENTITY_FIELDS = {
    "plugin_version", "source_commit", "manifest_sha256", "registry_sha256", "skill_tree_sha256"
}


class CollectionBuildError(ValueError):
    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


def _fail(code: str, path: str, message: str) -> None:
    raise CollectionBuildError(code, path, message)


def _identifier(value: Any, path: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}", value) is None:
        _fail("invalid_identifier", path, repr(value))
    return value


def _positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("invalid_asset_id", path, repr(value))
    return value


def _digest(value: Any, path: str) -> str:
    try:
        return normalize_sha256(value, path)
    except Exception as exc:
        _fail("invalid_sha256", path, str(exc))


def _load_json(path: Path, label: str) -> tuple[Mapping[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        _fail("file_read_failed", label, str(exc))
    try:
        return _mapping(_strict_json(payload, label), label), payload
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)


def _phase8_identity(identity: Mapping[str, Any]) -> dict[str, str]:
    return {
        "plugin_version": str(identity["plugin_version"]),
        "source_commit": str(identity["source_commit"]),
        "manifest_digest": str(identity["manifest_sha256"]),
        "registry_digest": str(identity["registry_sha256"]),
        "skill_tree_digest": str(identity["skill_tree_sha256"]),
    }


@dataclass(frozen=True)
class Capture:
    slot_id: str
    kind: str
    case_id: str
    repeat_index: int | None
    path: Path
    payload: bytes
    document: Mapping[str, Any]
    validated: Mapping[str, Any]

    @property
    def task(self) -> Mapping[str, Any]:
        return _mapping(self.validated["task_export"], f"{self.slot_id}.task_export")

    @property
    def identity(self) -> Mapping[str, Any]:
        return _mapping(self.validated["source_identity"], f"{self.slot_id}.source_identity")


def _scheduler_slots() -> Mapping[str, Mapping[str, Any]]:
    try:
        manifest = yaml.safe_load(SCHEDULER_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("scheduler_manifest_unavailable", str(SCHEDULER_MANIFEST), str(exc))
    root = _mapping(manifest, "scheduler_manifest")
    values = _sequence(root.get("slots"), "scheduler_manifest.slots")
    result = {str(item.get("slot")): _mapping(item, "scheduler_manifest.slot") for item in values if isinstance(item, Mapping)}
    if len(values) != 12 or len(result) != 12:
        _fail("scheduler_slot_count", "scheduler_manifest.slots", str(len(result)))
    return result


def load_captures(
    *, root: Path, plan: Mapping[str, Any], now: datetime, verify_checkout: bool
) -> list[Capture]:
    if plan.get("schema_version") != PLAN_SCHEMA:
        _fail("unsupported_plan_schema", "plan.schema_version", repr(plan.get("schema_version")))
    records = _sequence(plan.get("captures"), "plan.captures")
    if len(records) != 12:
        _fail("capture_count", "plan.captures", str(len(records)))
    scheduler = _scheduler_slots()
    captures: list[Capture] = []
    seen_paths: set[Path] = set()
    seen_slots: set[str] = set()
    identity: Mapping[str, Any] | None = None
    for offset, value in enumerate(records):
        record = _mapping(value, f"plan.captures[{offset}]")
        if set(record) != {"slot_id", "path"}:
            _fail("capture_plan_fields", f"plan.captures[{offset}]", str(sorted(record)))
        slot_id = _identifier(record.get("slot_id"), f"plan.captures[{offset}].slot_id")
        if slot_id in seen_slots or slot_id not in scheduler:
            _fail("capture_slot_reused_or_unknown", f"plan.captures[{offset}].slot_id", slot_id)
        relative = _string(record.get("path"), f"plan.captures[{offset}].path")
        try:
            canonical_relative(relative, f"plan.captures[{offset}].path")
        except CaptureNormalizationError as exc:
            _fail(exc.code, exc.path, exc.message)
        path = (root / Path(*PurePosixPath(relative).parts)).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            _fail("path_escape", f"plan.captures[{offset}].path", relative)
        if not path.is_file() or path.is_symlink() or path in seen_paths:
            _fail("capture_path_unavailable_or_reused", f"plan.captures[{offset}].path", relative)
        document, payload = _load_json(path, f"capture.{slot_id}")
        if document.get("normalization_schema") != PHASE8_NORMALIZED_CAPTURE_SCHEMA:
            _fail("phase8_capture_required", f"capture.{slot_id}.normalization_schema", repr(document.get("normalization_schema")))
        try:
            validated = validate_normalized_capture(document, now=now, verify_checkout=verify_checkout)
        except CaptureNormalizationError as exc:
            _fail(exc.code, f"capture.{slot_id}:{exc.path}", exc.message)
        except ValueError as exc:
            _fail("capture_dispatch_failed", f"capture.{slot_id}", str(exc))
        if validated.get("slot_id") != slot_id:
            _fail("capture_slot_mismatch", f"capture.{slot_id}", repr(validated.get("slot_id")))
        slot = scheduler[slot_id]
        if validated.get("profile") != slot.get("capture_profile") or document.get("capture", {}).get("slot_id") != slot_id:
            _fail("capture_profile_mismatch", f"capture.{slot_id}", repr(validated.get("profile")))
        current_identity = _mapping(validated.get("source_identity"), f"capture.{slot_id}.source_identity")
        if identity is None:
            identity = current_identity
        elif dict(current_identity) != dict(identity):
            _fail("mixed_release_capture", f"capture.{slot_id}.source_identity", slot_id)
        repeat = slot.get("repeat_index")
        if repeat is not None and (isinstance(repeat, bool) or not isinstance(repeat, int)):
            _fail("invalid_repeat_index", f"scheduler.{slot_id}.repeat_index", repr(repeat))
        captures.append(Capture(slot_id, str(slot["kind"]), str(slot["case_id"]), repeat, path, payload, document, validated))
        seen_paths.add(path)
        seen_slots.add(slot_id)
    if seen_slots != set(scheduler):
        _fail("capture_slot_coverage", "plan.captures", str(sorted(set(scheduler) - seen_slots)))
    distribution = Counter(item.kind for item in captures)
    if dict(distribution) != EXPECTED_DISTRIBUTION:
        _fail("capture_distribution", "plan.captures", str(dict(distribution)))
    reviewer_parents = [str(item.document.get("parent_task_or_thread_id")) for item in captures if item.kind == "reviewer"]
    reviewer_times = [str(item.document.get("captured_at")) for item in captures if item.kind == "reviewer"]
    if len(reviewer_parents) != len(set(reviewer_parents)):
        _fail("reviewer_parent_task_reused", "captures", repr(reviewer_parents))
    if len(reviewer_times) != len(set(reviewer_times)):
        _fail("reviewer_capture_timestamp_reused", "captures", "each reviewer run needs its own platform timestamp")
    return captures


def pending_inventory(captures: Sequence[Capture]) -> dict[str, Any]:
    pending = [
        {
            "slot_id": item.slot_id,
            "kind": item.kind,
            "capture_status": item.validated["capture_status"],
            "reason": (
                "no_concrete_deep_research_export_adapter"
                if item.kind == "deep_research_completed"
                else "no_registered_platform_capture_adapter"
            ),
        }
        for item in captures
        if item.validated.get("live_collection_eligible") is not True
    ]
    return {
        "schema_version": PENDING_SCHEMA,
        "complete": False,
        "gate_eligible": False,
        "provider_verified": False,
        "counts_as_preview_acceptance": False,
        "source_identity": dict(captures[0].identity) if captures else None,
        "eligible_slot_count": len(captures) - len(pending),
        "required_slot_count": 12,
        "pending_slots": pending,
        "next_required_action": "register_concrete_platform_capture_adapter_then_recapture",
    }


def _asset_binding(value: Any, path: str) -> dict[str, Any]:
    record = _mapping(value, path)
    if set(record) != {"logical_path", "asset_id", "sha256", "size"}:
        _fail("asset_binding_fields", path, str(sorted(record)))
    logical = _string(record.get("logical_path"), f"{path}.logical_path")
    try:
        canonical_relative(logical, f"{path}.logical_path")
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    return {
        "logical_path": logical,
        "asset_id": _positive_int(record.get("asset_id"), f"{path}.asset_id"),
        "sha256": _digest(record.get("sha256"), f"{path}.sha256"),
        "size": _positive_int(record.get("size"), f"{path}.size"),
    }


def _capture_asset_map(capture: Capture, value: Any, path: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    record = _mapping(value, path)
    required = {"bundle_id", "normalized_capture", "source_files", "preview_attestation"}
    if set(record) != required:
        _fail("slot_asset_binding_fields", path, str(sorted(record)))
    normalized = _asset_binding(record.get("normalized_capture"), f"{path}.normalized_capture")
    if normalized["sha256"] != sha256_bytes(capture.payload) or normalized["size"] != len(capture.payload):
        _fail("normalized_capture_asset_mismatch", path, capture.slot_id)
    decoded = _mapping(capture.validated.get("decoded_source_files"), f"{capture.slot_id}.decoded_sources")
    sources_value = _mapping(record.get("source_files"), f"{path}.source_files")
    if set(sources_value) != set(decoded):
        _fail("source_asset_coverage", f"{path}.source_files", f"missing={sorted(set(decoded)-set(sources_value))} extra={sorted(set(sources_value)-set(decoded))}")
    sources: dict[str, dict[str, Any]] = {}
    for logical, payload in decoded.items():
        binding = _asset_binding(sources_value[logical], f"{path}.source_files.{logical}")
        if binding["sha256"] != sha256_bytes(payload) or binding["size"] != len(payload):
            _fail("source_asset_mismatch", f"{path}.source_files.{logical}", str(logical))
        sources[str(logical)] = binding
    attestation = _mapping(record.get("preview_attestation"), f"{path}.preview_attestation")
    required_attestation = {
        "adapter_id", "envelope_path", "envelope_digest", "release_asset_index_path",
        "release_asset_index_digest", "raw_export_path", "raw_export_digest", "synthetic_test_only",
    }
    if set(attestation) != required_attestation or attestation.get("synthetic_test_only") is not False:
        _fail("preview_attestation_fields", f"{path}.preview_attestation", str(sorted(attestation)))
    if attestation.get("adapter_id") != "github_release_asset_preview_v1":
        _fail("preview_attestation_adapter", f"{path}.preview_attestation.adapter_id", repr(attestation.get("adapter_id")))
    for field in ("envelope_path", "release_asset_index_path", "raw_export_path"):
        logical = _string(attestation.get(field), f"{path}.preview_attestation.{field}")
        try:
            canonical_relative(logical, f"{path}.preview_attestation.{field}")
        except CaptureNormalizationError as exc:
            _fail(exc.code, exc.path, exc.message)
    for field in ("envelope_digest", "release_asset_index_digest", "raw_export_digest"):
        _digest(attestation.get(field), f"{path}.preview_attestation.{field}")
    if attestation.get("raw_export_path") != normalized["logical_path"] or attestation.get("raw_export_digest") != normalized["sha256"]:
        _fail("preview_attestation_raw_binding", f"{path}.preview_attestation", capture.slot_id)
    return {"bundle_id": _identifier(record.get("bundle_id"), f"{path}.bundle_id"), "normalized": normalized, "attestation": dict(attestation)}, sources


def validate_asset_bindings(captures: Sequence[Capture], document: Mapping[str, Any]) -> dict[str, Any]:
    required_fields = {
        "schema_version", "synthetic_test_only", "source_identity", "slots",
        "collections", "collection_anchor_slot", "collection_witness_slot",
    }
    if set(document) != required_fields or document.get("schema_version") != ASSET_BINDINGS_SCHEMA or document.get("synthetic_test_only") is not False:
        _fail("asset_bindings_schema", "asset_bindings", repr(document.get("schema_version")))
    identity = _mapping(document.get("source_identity"), "asset_bindings.source_identity")
    if set(identity) != IDENTITY_FIELDS or dict(identity) != dict(captures[0].identity):
        _fail("asset_bindings_source_identity", "asset_bindings.source_identity", repr(identity))
    slots_value = _mapping(document.get("slots"), "asset_bindings.slots")
    if set(slots_value) != {item.slot_id for item in captures}:
        _fail("asset_binding_slot_coverage", "asset_bindings.slots", str(sorted(slots_value)))
    slot_bindings: dict[str, Any] = {}
    asset_ids: set[int] = set()
    logical_bindings: dict[str, tuple[int, str, int]] = {}
    for capture in captures:
        control, sources = _capture_asset_map(capture, slots_value[capture.slot_id], f"asset_bindings.slots.{capture.slot_id}")
        for binding in [control["normalized"], *sources.values()]:
            asset_id = binding["asset_id"]
            if asset_id in asset_ids:
                _fail("asset_id_reused", f"asset_bindings.slots.{capture.slot_id}", str(asset_id))
            asset_ids.add(asset_id)
            logical = binding["logical_path"]
            identity_tuple = (asset_id, binding["sha256"], binding["size"])
            if logical in logical_bindings and logical_bindings[logical] != identity_tuple:
                _fail("logical_path_conflict", f"asset_bindings.slots.{capture.slot_id}", logical)
            logical_bindings[logical] = identity_tuple
        slot_bindings[capture.slot_id] = {**control, "sources": sources}
    collections = _mapping(document.get("collections"), "asset_bindings.collections")
    if set(collections) != {"reviewer", "retrieval"}:
        _fail("collection_asset_coverage", "asset_bindings.collections", str(sorted(collections)))
    collection_bindings = {name: _asset_binding(value, f"asset_bindings.collections.{name}") for name, value in collections.items()}
    for binding in collection_bindings.values():
        if binding["asset_id"] in asset_ids:
            _fail("asset_id_reused", "asset_bindings.collections", str(binding["asset_id"]))
        asset_ids.add(binding["asset_id"])
    anchor = _identifier(document.get("collection_anchor_slot"), "asset_bindings.collection_anchor_slot")
    witness = _identifier(document.get("collection_witness_slot"), "asset_bindings.collection_witness_slot")
    by_slot = {item.slot_id: item for item in captures}
    if anchor == witness or anchor not in by_slot or witness not in by_slot or by_slot[anchor].kind != "reviewer" or by_slot[witness].kind != "reviewer":
        _fail("collection_anchor_witness", "asset_bindings", f"{anchor}/{witness}")
    return {"slots": slot_bindings, "collections": collection_bindings, "anchor": anchor, "witness": witness}


def _mapped_source(bindings: Mapping[str, Any], source_path: str) -> str:
    return str(_mapping(_mapping(bindings.get("sources"), "bindings.sources").get(source_path), f"bindings.sources.{source_path}")["logical_path"])


def _platform_export_path(capture: Capture, bindings: Mapping[str, Any]) -> str:
    provenance = _mapping(capture.document.get("capture_provenance"), f"{capture.slot_id}.capture_provenance")
    id_bindings = _mapping(provenance.get("id_bindings"), f"{capture.slot_id}.capture_provenance.id_bindings")
    source_paths = {str(_mapping(item, "id_binding").get("source_path")) for item in id_bindings.values()}
    if len(source_paths) != 1:
        _fail("platform_export_path_count", capture.slot_id, str(sorted(source_paths)))
    return _mapped_source(bindings, next(iter(source_paths)))


def assemble_collections(
    captures: Sequence[Capture],
    assets: Mapping[str, Any],
    *,
    synthetic_test_only: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Pure schema assembly; it does not establish capture eligibility.

    The production wrapper below performs the 12/12 live-eligibility gate.
    Tests may call this helper with in-memory records only; its synthetic flag
    is retained in the output and such output is rejected by the external
    runner.
    """
    identity = dict(captures[0].identity)
    reviewer_cases: dict[str, list[dict[str, Any]]] = defaultdict(list)
    retrieval_receipts: list[dict[str, Any]] = []
    for capture in sorted(captures, key=lambda item: item.slot_id):
        bound = _mapping(_mapping(assets.get("slots"), "assets.slots").get(capture.slot_id), f"assets.slots.{capture.slot_id}")
        task = capture.task
        normalized_path = str(_mapping(bound.get("normalized"), "bound.normalized")["logical_path"])
        attestation = dict(_mapping(bound.get("attestation"), "bound.attestation"))
        if capture.kind == "reviewer":
            run = _mapping(_mapping(task.get("slot_payload"), "slot_payload").get("reviewer_run"), "reviewer_run")
            scope = _mapping(run.get("platform_scope"), "reviewer_run.platform_scope")
            reviewer_cases[capture.case_id].append({
                "run_id": capture.slot_id,
                "platform_run_id": run["run_id"],
                "parent_task_or_thread_id": task["parent_task_or_thread_id"],
                "captured_at": task["captured_at"],
                "delegated_thread_id": run["delegated_thread_id"],
                "normalized_capture_path": normalized_path,
                "raw_transport_output_path": _mapped_source(bound, run["raw_transport_output"]["path"]),
                "blind_bundle_path": _mapped_source(bound, run["blind_bundle"]["path"]),
                "dispatch_prompt_path": _mapped_source(bound, run["dispatch_prompt"]["path"]),
                "platform_read_scope_export_path": _platform_export_path(capture, bound),
                "scope_authority": "platform_derived",
                "review_contract": {
                    "reviewer_skill": run["reviewer_skill"],
                    "reviewer_instance_id": run["reviewer_instance_id"],
                    "reviewer_instance_created_at": run["reviewer_instance_created_at"],
                    "platform_receipt_id": run["platform_receipt_id"],
                    "files_read": [_mapped_source(bound, path) for path in scope["files_read"]],
                    "files_written": [_mapped_source(bound, path) for path in scope["files_written"]],
                    "source_edits_performed": False,
                },
                "preview_attestation": attestation,
            })
            continue
        retrieval = _mapping(_mapping(task.get("slot_payload"), "slot_payload").get("retrieval"), "retrieval")
        receipt: dict[str, Any] = {
            "receipt_id": capture.slot_id,
            "kind": capture.kind,
            **_phase8_identity(identity),
            "captured_at": task["captured_at"],
            "task_id": task["task_id"],
            "normalized_capture_path": normalized_path,
            "platform_receipt_or_export_path": _platform_export_path(capture, bound),
            "preview_attestation": attestation,
            "artifact_paths": [],
            "evidence_artifacts": [],
        }
        if capture.kind == "search":
            receipt.update({
                "question_class": retrieval["question_class"],
                "query": retrieval["query"],
                "query_or_request_digest": retrieval["query_or_request_digest"],
                "tool_id": retrieval["tool_id"],
                "tool_run_id": retrieval["tool_run_id"],
                "raw_search_output_path": _mapped_source(bound, retrieval["raw_search_output"]["path"]),
                "citation_export_path": _mapped_source(bound, retrieval["citation_export"]["path"]),
                "opened_sources": retrieval["opened_sources"],
                "material_claim_trace": retrieval["material_claim_trace"],
                "local_retrieval_fallback": False,
            })
        elif capture.kind == "deep_research_inactive_control":
            receipt.update({
                "capability_state": retrieval["capability_state"],
                "capability_state_export_path": _mapped_source(bound, retrieval["capability_state_export"]["path"]),
                "handoff_artifact": _mapped_source(bound, retrieval["handoff_artifact"]["path"]),
                "continuation_artifact": _mapped_source(bound, retrieval["continuation_artifact"]["path"]),
                "pending_edge_id": retrieval["pending_edge_id"],
                "workflow_paused": True,
                "downstream_evidence_map_created": False,
                "inline_simulation": False,
            })
        elif capture.kind == "deep_research_completed":
            receipt.update({
                "deep_research_session_id": retrieval["deep_research_session_id"],
                "deep_research_run_id": retrieval["deep_research_run_id"],
                "provider_completion_receipt_id": retrieval["provider_completion_receipt_id"],
                "provider_completion_status": retrieval["provider_completion_status"],
                "pending_edge_id": retrieval["pending_edge_id"],
                "raw_deep_research_output_path": _mapped_source(bound, retrieval["raw_deep_research_output"]["path"]),
                "citation_export_path": _mapped_source(bound, retrieval["citation_export"]["path"]),
                "handoff_artifact": _mapped_source(bound, retrieval["handoff_artifact"]["path"]),
                "user_start_event_path": _mapped_source(bound, retrieval["user_start_event"]["path"]),
                "provider_run_completed_path": _platform_export_path(capture, bound),
                "mapper_return_artifact": _mapped_source(bound, retrieval["mapper_return_artifact"]["path"]),
                "resume_receipt_path": _mapped_source(bound, retrieval["resume_receipt"]["path"]),
                "opened_sources": retrieval["opened_sources"],
                "material_claim_trace": retrieval["material_claim_trace"],
                "evidence_artifacts": [
                    {
                        **item,
                        "path": _mapped_source(bound, item["path"]),
                    }
                    for item in retrieval["mapper_return_evidence_artifacts"]
                ],
                "event_timestamps": retrieval["event_timestamps"],
                "inline_simulation": False,
            })
        else:
            _fail("unsupported_capture_kind", capture.slot_id, capture.kind)
        retrieval_receipts.append(receipt)
    cases: list[dict[str, Any]] = []
    scheduler = _scheduler_slots()
    for case_id, runs in sorted(reviewer_cases.items()):
        slot = next(item for item in scheduler.values() if item.get("case_id") == case_id)
        first_capture = next(item for item in captures if item.case_id == case_id and item.kind == "reviewer")
        input_path = first_capture.validated["scheduler_binding"]["input"]["path"]
        first_bound = assets["slots"][first_capture.slot_id]
        cases.append({"case_id": f"case-{case_id}", "input_path": _mapped_source(first_bound, input_path), "runs": sorted(runs, key=lambda item: item["run_id"])})
    reviewer = {
        "schema_version": REVIEWER_COLLECTION_SCHEMA,
        "collection_id": "phase8-current-reviewer-receipts",
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": synthetic_test_only,
        "evidence_class": "preview_attested_platform_fresh_subagent_receipts",
        **_phase8_identity(identity),
        "cases": cases,
    }
    retrieval = {
        "schema_version": RETRIEVAL_COLLECTION_SCHEMA,
        "collection_id": "phase8-current-retrieval-receipts",
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": synthetic_test_only,
        "evidence_class": "preview_attested_platform_retrieval_receipts",
        "receipts": sorted(retrieval_receipts, key=lambda item: item["receipt_id"]),
    }
    return reviewer, retrieval


def build_collections(captures: Sequence[Capture], assets: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if len(captures) != 12 or Counter(item.kind for item in captures) != Counter(EXPECTED_DISTRIBUTION):
        _fail("phase8_capture_distribution", "captures", str(Counter(item.kind for item in captures)))
    if any(item.validated.get("live_collection_eligible") is not True for item in captures):
        _fail("phase8_capture_pending", "captures", "all twelve captures must be platform-derived and live-eligible")
    return assemble_collections(captures, assets, synthetic_test_only=False)


def build_workspace_manifests(
    captures: Sequence[Capture], assets: Mapping[str, Any],
    reviewer_bytes: bytes, retrieval_bytes: bytes,
    *,
    synthetic_test_only: bool = False,
) -> dict[str, dict[str, Any]]:
    collection_bindings = _mapping(assets.get("collections"), "assets.collections")
    for name, payload in (("reviewer", reviewer_bytes), ("retrieval", retrieval_bytes)):
        binding = _mapping(collection_bindings.get(name), f"assets.collections.{name}")
        if binding.get("sha256") != sha256_bytes(payload) or binding.get("size") != len(payload):
            _fail("collection_asset_bytes_mismatch", f"assets.collections.{name}", name)
    manifests: dict[str, dict[str, Any]] = {}
    for capture in captures:
        bound = _mapping(_mapping(assets.get("slots"), "assets.slots").get(capture.slot_id), f"assets.slots.{capture.slot_id}")
        files = [dict(_mapping(bound.get("normalized"), "bound.normalized")), *[dict(item) for item in _mapping(bound.get("sources"), "bound.sources").values()]]
        witness = capture.slot_id == assets.get("witness")
        if witness:
            files.extend([dict(collection_bindings["reviewer"]), dict(collection_bindings["retrieval"])])
        manifests[capture.slot_id] = {
            "schema_version": WORKSPACE_MANIFEST_SCHEMA,
            "counts_as_runtime_evidence": False,
            "synthetic_test_only": synthetic_test_only,
            "bundle_id": bound["bundle_id"],
            "slot_kind": "reviewer" if capture.kind == "reviewer" else "retrieval",
            "slot_id": capture.slot_id,
            "collection_anchor": capture.slot_id == assets.get("anchor"),
            "collection_witness": witness,
            "source_identity": dict(capture.identity),
            "files": sorted(files, key=lambda item: item["logical_path"]),
        }
    return manifests


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _fail("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("--staging-root", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--asset-bindings")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--now")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        staging = StagingRoot(args.staging_root)
        plan_path = staging.input_file(args.plan, "cli.plan")
        plan, _ = _load_json(plan_path, "plan")
        captures = load_captures(root=staging.root, plan=plan, now=parse_clock(args.now), verify_checkout=True)
        pending = pending_inventory(captures)
        if pending["pending_slots"]:
            output = staging.output_file(f"{args.output_dir}/phase8-pending.json", "cli.output_dir")
            output.write_bytes(canonical_json_bytes(pending))
            result = {"schema_version": RESULT_SCHEMA, "complete": False, "gate_eligible": False, "pending_slot_count": len(pending["pending_slots"]), "output": str(output)}
        else:
            if not args.asset_bindings:
                _fail("asset_bindings_required", "cli.asset_bindings", "complete captures require GitHub API asset bindings")
            asset_path = staging.input_file(args.asset_bindings, "cli.asset_bindings")
            asset_document, _ = _load_json(asset_path, "asset_bindings")
            assets = validate_asset_bindings(captures, asset_document)
            reviewer, retrieval = build_collections(captures, assets)
            reviewer_bytes = canonical_json_bytes(reviewer)
            retrieval_bytes = canonical_json_bytes(retrieval)
            manifests = build_workspace_manifests(captures, assets, reviewer_bytes, retrieval_bytes)
            outputs = {
                "reviewer": (f"{args.output_dir}/reviewer-receipts.json", reviewer_bytes),
                "retrieval": (f"{args.output_dir}/retrieval-receipts.json", retrieval_bytes),
                **{f"manifest:{slot_id}": (f"{args.output_dir}/workspace-manifests/{slot_id}.json", canonical_json_bytes(document)) for slot_id, document in manifests.items()},
            }
            written: dict[str, str] = {}
            for name, (relative, payload) in outputs.items():
                target = staging.output_file(relative, f"cli.output.{name}")
                target.write_bytes(payload)
                written[name] = str(target)
            result = {"schema_version": RESULT_SCHEMA, "complete": True, "gate_eligible": False, "outputs": written}
    except (CaptureNormalizationError, CollectionBuildError) as exc:
        code_name = exc.code if hasattr(exc, "code") else "capture_error"
        path = exc.path if hasattr(exc, "path") else "capture"
        message = exc.message if hasattr(exc, "message") else str(exc)
        result = {"schema_version": RESULT_SCHEMA, "complete": False, "gate_eligible": False, "error": {"code": code_name, "path": path, "message": message}}
        code = 2 if code_name == "invalid_cli_arguments" else 1
    except Exception as exc:
        result = {"schema_version": RESULT_SCHEMA, "complete": False, "gate_eligible": False, "error": {"code": "internal_error", "path": "cli", "message": f"{type(exc).__name__}: {exc}"}}
        code = 3
    else:
        code = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
