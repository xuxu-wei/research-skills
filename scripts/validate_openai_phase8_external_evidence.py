#!/usr/bin/env python3
"""Validate real Phase 8 reviewer and native-research evidence bundles.

The command-line path has no synthetic or offline promotion mode.  It accepts
two frozen receipt collections and exactly twelve immutable GitHub Release
mini-bundles: six fresh reviewer runs and six retrieval executions.  Every
bundle is integrity-checked, live-requeried through the registered Preview
verifier, materialized from snapshotted bytes into a fresh workspace, and then
rechecked by the Phase 8 semantic validators.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping, Sequence

import yaml

if __name__ == "__main__":
    # Keep the issuer identity stable when the trusted validator is run as a CLI.
    sys.modules.setdefault("validate_openai_phase8_external_evidence", sys.modules[__name__])

from generate_openai_release_ledger import (
    normalized_file_digest,
    normalized_skill_tree_digest,
)
from openai_preview_evidence import (
    CAPTURE_EXPORT_KINDS,
    PREVIEW_ATTESTED,
    EvidenceValidationError,
    EvidenceValidationResult,
    normalize_sha256,
    sha256_bytes,
    validate_evidence_bundle,
)


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
PHASE8_VERIFIER_PATH = REPO / "tests" / "openai_phase8" / "verify_preview_evidence.py"
PREVIEW_ADAPTER_ID = "github_release_asset_preview_v1"
WORKSPACE_MANIFEST_SCHEMA = "openai-phase8-workspace-manifest/v1"
RESULT_SCHEMA = "openai-phase8-external-evidence-validation/v1"
EXPECTED_REVIEWER_SLOTS = 6
EXPECTED_RETRIEVAL_SLOTS = 6
EXPECTED_BUNDLES = EXPECTED_REVIEWER_SLOTS + EXPECTED_RETRIEVAL_SLOTS
FRESHNESS_DAYS = 90
FUTURE_SKEW = timedelta(minutes=5)
IDENTITY_FIELDS = {
    "plugin_version",
    "source_commit",
    "manifest_sha256",
    "registry_sha256",
    "skill_tree_sha256",
}
ORACLE_TOKENS = {
    "accept",
    "accepted",
    "blocked",
    "fatal",
    "fixable",
    "happy",
    "oracle",
    "pass",
    "passed",
    "promoted",
    "reject",
    "rejected",
    "revision",
    "score",
}
WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)


class Phase8ExternalEvidenceError(ValueError):
    """Stable fail-closed error for the external Phase 8 evidence path."""

    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


class _ExternalValidatorIssuerCapability:
    """Uncloneable authority owned by this committed external verifier module."""

    __slots__ = ()

    def __reduce_ex__(self, _protocol: int) -> Any:
        raise TypeError("external validator issuer capability cannot be serialized")

    def __copy__(self) -> Any:
        raise TypeError("external validator issuer capability cannot be copied")

    def __deepcopy__(self, _memo: Any) -> Any:
        raise TypeError("external validator issuer capability cannot be copied")


_PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY = (
    _ExternalValidatorIssuerCapability()
)


@dataclass(frozen=True)
class SourceSnapshot:
    path: Path
    payload: bytes
    digest: str


@dataclass(frozen=True)
class AssetSnapshot:
    asset_id: int
    name: str
    evidence_kind: str
    digest: str
    size: int
    payload: bytes
    source_path: Path


@dataclass(frozen=True)
class WorkspaceFile:
    logical_path: str
    asset_id: int
    digest: str
    payload: bytes


@dataclass(frozen=True)
class Slot:
    kind: str
    slot_id: str
    execution_id: str
    captured_at: str
    raw_path: str
    subject: Mapping[str, Any]


@dataclass(frozen=True)
class BundleSnapshot:
    bundle_id: str
    slot: Slot
    collection_anchor: bool
    index_path: Path
    index_document: Mapping[str, Any]
    index_bytes: bytes
    assets: Mapping[int, AssetSnapshot]
    envelope: Mapping[str, Any]
    envelope_bytes: bytes
    integrity: EvidenceValidationResult
    collection_witness: bool
    witnessed_collection_paths: Mapping[str, str]
    workspace_files: tuple[WorkspaceFile, ...]


LiveVerifier = Callable[[Mapping[str, Any]], Mapping[str, Any]]
RequestBuilder = Callable[..., Mapping[str, Any]]
SemanticValidator = Callable[..., Mapping[str, Any]]


def _fail(code: str, path: str, message: str) -> None:
    raise Phase8ExternalEvidenceError(code, path, message)


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("invalid_document", path, "expected an object")
    return value


def _sequence(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail("invalid_document", path, "expected an array")
    return value


def _read(path: Path, label: str) -> bytes:
    if path.is_symlink():
        _fail("symlink_rejected", label, str(path))
    try:
        if not path.is_file():
            _fail("file_missing", label, str(path))
        return path.read_bytes()
    except OSError as exc:
        _fail("file_read_failed", label, f"{type(exc).__name__}: {exc}")


def _snapshot(path: Path, label: str) -> SourceSnapshot:
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        _fail("file_missing", label, f"{type(exc).__name__}: {exc}")
    payload = _read(resolved, label)
    return SourceSnapshot(resolved, payload, sha256_bytes(payload))


def _parse(payload: bytes, path: str) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(payload)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("invalid_document", path, str(exc))
    return _mapping(value, path)


def _inside(root: Path, candidate: Path, label: str, *, exists: bool = True) -> Path:
    try:
        resolved = candidate.resolve(strict=exists)
        resolved.relative_to(root)
    except (OSError, ValueError):
        _fail("path_escape", label, str(candidate))
    return resolved


def _logical_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        _fail("logical_path_not_canonical", label, repr(value))
    logical = PurePosixPath(value)
    if logical.is_absolute() or logical.as_posix() != value or any(
        part in {"", ".", ".."} for part in logical.parts
    ):
        _fail("logical_path_not_canonical", label, value)
    for part in logical.parts:
        if (
            part.endswith((" ", "."))
            or any(character in part for character in '<>"|?*')
            or part.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES
        ):
            _fail("logical_path_not_portable", label, value)
    return value


def _identifier(value: Any, label: str, *, reject_oracle: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("slot_identifier", label, repr(value))
    if reject_oracle:
        leaked = set(re.findall(r"[a-z0-9]+", value.lower())).intersection(ORACLE_TOKENS)
        if leaked:
            _fail("reviewer_outcome_oracle", label, str(sorted(leaked)))
    return value


def _timestamp(value: Any, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        _fail("invalid_timestamp", label, str(value))
    if parsed.tzinfo is None:
        _fail("invalid_timestamp", label, "timezone is required")
    parsed = parsed.astimezone(timezone.utc)
    now = datetime.now(timezone.utc)
    if parsed > now + FUTURE_SKEW:
        _fail("future_evidence", label, parsed.isoformat())
    if now - parsed > timedelta(days=FRESHNESS_DAYS):
        _fail("stale_evidence", label, parsed.isoformat())
    return parsed


def _normalized_identity(document: Mapping[str, Any]) -> dict[str, str]:
    candidate = _mapping(document.get("source_identity", document), "expected_source_identity")
    if set(candidate) != IDENTITY_FIELDS:
        _fail("source_identity_fields", "expected_source_identity", str(sorted(candidate)))
    commit = str(candidate.get("source_commit", "")).lower()
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        _fail("source_identity_commit", "expected_source_identity.source_commit", commit)
    version = candidate.get("plugin_version")
    if not isinstance(version, str) or not version:
        _fail("source_identity_version", "expected_source_identity.plugin_version", repr(version))
    normalized = {"plugin_version": version, "source_commit": commit}
    for field in IDENTITY_FIELDS - {"plugin_version", "source_commit"}:
        try:
            normalized[field] = normalize_sha256(candidate[field], f"expected_source_identity.{field}")
        except EvidenceValidationError as exc:
            _fail(exc.code, exc.path, exc.message)
    return normalized


def current_checkout_source_identity() -> dict[str, str]:
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if process.returncode != 0:
        _fail("checkout_head_unavailable", "local_checkout", process.stderr.strip())
    commit = process.stdout.strip().lower()
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        _fail("checkout_head_invalid", "local_checkout", commit)
    manifest = PLUGIN / ".codex-plugin" / "plugin.json"
    registry = PLUGIN / "workflow-registry.yaml"
    manifest_document = _parse(_read(manifest, "plugin_manifest"), "plugin_manifest")
    registry_document = _parse(_read(registry, "workflow_registry"), "workflow_registry")
    version = manifest_document.get("version")
    if not isinstance(version, str) or registry_document.get("plugin_version") != version:
        _fail("plugin_version_mismatch", "workflow_registry", str(version))
    _, skill_digest = normalized_skill_tree_digest(PLUGIN / "skills")
    return {
        "plugin_version": version,
        "source_commit": commit,
        "manifest_sha256": f"sha256:{normalized_file_digest(manifest)}",
        "registry_sha256": f"sha256:{normalized_file_digest(registry)}",
        "skill_tree_sha256": f"sha256:{skill_digest}",
    }


def _assert_committed_source_identity(identity: Mapping[str, str]) -> None:
    """Require the frozen commit to contain the exact installable plugin tree."""
    import test_openai_phase8_corpus as phase8

    committed = phase8.committed_contract_identity(identity["source_commit"])
    expected = _phase8_identity(identity)
    if committed != expected:
        _fail(
            "source_commit_tree_mismatch",
            "expected_source_identity.source_commit",
            "the commit does not contain the manifest, registry, and skill tree",
        )


def _phase8_identity(identity: Mapping[str, str]) -> dict[str, str]:
    return {
        "source_commit": identity["source_commit"],
        "manifest_digest": identity["manifest_sha256"],
        "registry_digest": identity["registry_sha256"],
        "skill_tree_digest": identity["skill_tree_sha256"],
    }


def _assert_subject_identity(subject: Mapping[str, Any], identity: Mapping[str, str], label: str) -> None:
    if subject.get("plugin_version") != identity["plugin_version"]:
        _fail("mixed_release_evidence", label, "plugin version mismatch")
    for field, expected in _phase8_identity(identity).items():
        if subject.get(field) != expected:
            _fail("mixed_release_evidence", f"{label}.{field}", str(subject.get(field)))


def _reviewer_slots(collection: Mapping[str, Any], identity: Mapping[str, str]) -> dict[str, Slot]:
    if collection.get("evidence_class") != "preview_attested_platform_fresh_subagent_receipts":
        _fail("reviewer_evidence_class", "reviewer_receipts.evidence_class", str(collection.get("evidence_class")))
    _assert_subject_identity(collection, identity, "reviewer_receipts")
    _timestamp(collection.get("captured_at"), "reviewer_receipts.captured_at")
    cases = _sequence(collection.get("cases"), "reviewer_receipts.cases")
    if len(cases) != 3 or {str(item.get("case_id", "")).lower().removeprefix("case-") for item in cases if isinstance(item, Mapping)} != {"a01", "a02", "a03"}:
        _fail("reviewer_case_coverage", "reviewer_receipts.cases", "A01, A02, and A03 are required")
    slots: dict[str, Slot] = {}
    for case_offset, value in enumerate(cases):
        case = _mapping(value, f"reviewer_receipts.cases[{case_offset}]")
        runs = _sequence(case.get("runs"), f"reviewer_receipts.cases[{case_offset}].runs")
        if len(runs) != 2:
            _fail("reviewer_repeat_count", str(case.get("case_id")), str(len(runs)))
        for run_offset, run_value in enumerate(runs):
            run = _mapping(run_value, f"reviewer_receipts.cases[{case_offset}].runs[{run_offset}]")
            slot_id = _identifier(run.get("run_id"), "reviewer.run_id", reject_oracle=True)
            if slot_id in slots:
                _fail("duplicate_slot", "reviewer.run_id", slot_id)
            contract = _mapping(run.get("review_contract"), f"reviewer.{slot_id}.review_contract")
            _identifier(contract.get("reviewer_instance_id"), f"reviewer.{slot_id}.instance_id", reject_oracle=True)
            execution_id = _identifier(run.get("delegated_thread_id"), f"reviewer.{slot_id}.delegated_thread_id", reject_oracle=True)
            raw_path = _logical_path(run.get("raw_transport_output_path"), f"reviewer.{slot_id}.raw_path")
            slots[slot_id] = Slot(
                kind="reviewer",
                slot_id=slot_id,
                execution_id=execution_id,
                captured_at=str(collection.get("captured_at")),
                raw_path=raw_path,
                subject=run,
            )
    if len(slots) != EXPECTED_REVIEWER_SLOTS:
        _fail("reviewer_slot_count", "reviewer_receipts", str(len(slots)))
    return slots


def _retrieval_slots(collection: Mapping[str, Any], identity: Mapping[str, str]) -> dict[str, Slot]:
    if collection.get("evidence_class") != "preview_attested_platform_retrieval_receipts":
        _fail("retrieval_evidence_class", "retrieval_receipts.evidence_class", str(collection.get("evidence_class")))
    receipts = _sequence(collection.get("receipts"), "retrieval_receipts.receipts")
    if len(receipts) != EXPECTED_RETRIEVAL_SLOTS:
        _fail("retrieval_slot_count", "retrieval_receipts.receipts", str(len(receipts)))
    counts: dict[str, int] = {}
    slots: dict[str, Slot] = {}
    for offset, value in enumerate(receipts):
        receipt = _mapping(value, f"retrieval_receipts.receipts[{offset}]")
        _assert_subject_identity(receipt, identity, f"retrieval_receipts.receipts[{offset}]")
        _timestamp(receipt.get("captured_at"), f"retrieval_receipts.receipts[{offset}].captured_at")
        kind = str(receipt.get("kind", ""))
        counts[kind] = counts.get(kind, 0) + 1
        slot_id = _identifier(receipt.get("receipt_id"), "retrieval.receipt_id")
        if slot_id in slots:
            _fail("duplicate_slot", "retrieval.receipt_id", slot_id)
        slots[slot_id] = Slot(
            kind="retrieval",
            slot_id=slot_id,
            execution_id=_identifier(receipt.get("task_id"), f"retrieval.{slot_id}.task_id"),
            captured_at=str(receipt.get("captured_at")),
            raw_path=_logical_path(receipt.get("platform_receipt_or_export_path"), f"retrieval.{slot_id}.platform_export"),
            subject=receipt,
        )
    expected = {"search": 3, "deep_research_completed": 2, "deep_research_inactive_control": 1}
    if counts != expected:
        _fail("retrieval_distribution", "retrieval_receipts.receipts", str(counts))
    return slots


def _assert_slot_independence(slots: Mapping[str, Slot]) -> None:
    if len(slots) != EXPECTED_BUNDLES:
        _fail("phase8_slot_count", "receipt_collections", str(len(slots)))
    execution_ids = [slot.execution_id for slot in slots.values()]
    if len(execution_ids) != len(set(execution_ids)):
        _fail(
            "execution_id_reused",
            "receipt_collections",
            "all 12 executions must be independent",
        )


def _required_workspace_paths(
    reviewer: Mapping[str, Any], retrieval: Mapping[str, Any], reviewer_collection_path: str, retrieval_collection_path: str
) -> set[str]:
    paths = {reviewer_collection_path, retrieval_collection_path}
    paths.add(_logical_path(reviewer.get("platform_task_or_delegation_export_path"), "reviewer.platform_export"))
    for case_value in _sequence(reviewer.get("cases"), "reviewer.cases"):
        case = _mapping(case_value, "reviewer.case")
        paths.add(_logical_path(case.get("input_path"), "reviewer.input_path"))
        for run_value in _sequence(case.get("runs"), "reviewer.case.runs"):
            run = _mapping(run_value, "reviewer.run")
            for field in (
                "blind_bundle_path",
                "dispatch_prompt_path",
                "raw_transport_output_path",
                "platform_read_scope_export_path",
            ):
                paths.add(_logical_path(run.get(field), f"reviewer.run.{field}"))
            contract = _mapping(run.get("review_contract"), "reviewer.run.review_contract")
            for field in ("files_read", "files_written"):
                for value in _sequence(contract.get(field), f"reviewer.run.review_contract.{field}"):
                    paths.add(_logical_path(value, f"reviewer.run.review_contract.{field}"))
    path_fields = {
        "search": ("platform_receipt_or_export_path", "raw_search_output_path", "citation_export_path"),
        "deep_research_completed": (
            "platform_receipt_or_export_path",
            "raw_deep_research_output_path",
            "citation_export_path",
            "handoff_artifact",
            "user_start_event_path",
            "provider_run_completed_path",
            "mapper_return_artifact",
            "resume_receipt_path",
        ),
        "deep_research_inactive_control": (
            "platform_receipt_or_export_path",
            "capability_state_export_path",
            "continuation_artifact",
        ),
    }
    for value in _sequence(retrieval.get("receipts"), "retrieval.receipts"):
        receipt = _mapping(value, "retrieval.receipt")
        for path in _sequence(receipt.get("artifact_paths"), "retrieval.receipt.artifact_paths"):
            paths.add(_logical_path(path, "retrieval.receipt.artifact_path"))
        for field in path_fields.get(str(receipt.get("kind")), ()):
            paths.add(_logical_path(receipt.get(field), f"retrieval.receipt.{field}"))
        for item in _sequence(receipt.get("evidence_artifacts", []), "retrieval.receipt.evidence_artifacts"):
            paths.add(_logical_path(_mapping(item, "retrieval.evidence_artifact").get("path"), "retrieval.evidence_artifact.path"))
    return paths


def _safe_pattern(pattern: str) -> str:
    if not pattern or "\\" in pattern or "\x00" in pattern or Path(pattern).is_absolute() or any(part == ".." for part in PurePosixPath(pattern).parts):
        _fail("unsafe_asset_index_pattern", "asset_index_pattern", repr(pattern))
    return pattern


def _discover_indexes(root: Path, pattern: str) -> list[Path]:
    try:
        candidates = list(root.glob(_safe_pattern(pattern)))
    except (OSError, ValueError) as exc:
        _fail("invalid_asset_index_pattern", "asset_index_pattern", str(exc))
    indexes: list[Path] = []
    for offset, candidate in enumerate(candidates):
        resolved = _inside(root, candidate, f"asset_indexes[{offset}]")
        if (
            resolved.suffix.lower() != ".json"
            or candidate.is_symlink()
            or resolved.parent != root
        ):
            _fail("asset_index_invalid", f"asset_indexes[{offset}]", str(candidate))
        indexes.append(resolved)
    if len(indexes) != EXPECTED_BUNDLES or len(set(indexes)) != len(indexes):
        _fail("phase8_bundle_count", "asset_indexes", f"expected {EXPECTED_BUNDLES}, found {len(indexes)}")
    return sorted(indexes, key=lambda item: item.as_posix().casefold())


def _load_assets(root: Path, index_path: Path, index: Mapping[str, Any]) -> dict[int, AssetSnapshot]:
    assets: dict[int, AssetSnapshot] = {}
    for offset, value in enumerate(_sequence(index.get("assets"), f"{index_path}.assets")):
        record = _mapping(value, f"{index_path}.assets[{offset}]")
        asset_id = record.get("asset_id")
        name = record.get("name")
        if isinstance(asset_id, bool) or not isinstance(asset_id, int) or asset_id <= 0:
            _fail("asset_id", f"{index_path}.assets[{offset}]", str(asset_id))
        if not isinstance(name, str) or not name or Path(name).name != name or name in {".", ".."}:
            _fail("asset_name", f"{index_path}.assets[{offset}]", repr(name))
        source = _inside(root, index_path.parent / name, f"asset[{asset_id}]")
        if source.parent != index_path.parent or source.is_symlink():
            _fail("asset_path_escape", f"asset[{asset_id}]", name)
        payload = _read(source, f"asset[{asset_id}]")
        digest = sha256_bytes(payload)
        if record.get("sha256") != digest or record.get("size") != len(payload):
            _fail("asset_digest_or_size", f"asset[{asset_id}]", name)
        if asset_id in assets:
            _fail("duplicate_asset_id", f"asset[{asset_id}]", name)
        assets[asset_id] = AssetSnapshot(asset_id, name, str(record.get("evidence_kind", "")), digest, len(payload), payload, source)
    return assets


def _manifest_asset(assets: Mapping[int, AssetSnapshot], label: str) -> tuple[AssetSnapshot, Mapping[str, Any]]:
    found: list[tuple[AssetSnapshot, Mapping[str, Any]]] = []
    for asset in assets.values():
        if asset.evidence_kind != "supporting_file":
            continue
        try:
            document = yaml.safe_load(asset.payload)
        except (UnicodeDecodeError, yaml.YAMLError):
            continue
        if isinstance(document, Mapping) and document.get("schema_version") == WORKSPACE_MANIFEST_SCHEMA:
            found.append((asset, document))
    if len(found) != 1:
        _fail("workspace_manifest_count", label, str(len(found)))
    return found[0]


def _binding(value: Any, assets: Mapping[int, AssetSnapshot], label: str) -> tuple[str, AssetSnapshot]:
    item = _mapping(value, label)
    if set(item) != {"logical_path", "asset_id", "sha256", "size"}:
        _fail("workspace_binding_fields", label, str(sorted(item)))
    logical = _logical_path(item.get("logical_path"), f"{label}.logical_path")
    asset = assets.get(item.get("asset_id"))
    if asset is None or item.get("sha256") != asset.digest or item.get("size") != asset.size:
        _fail("workspace_binding", label, logical)
    return logical, asset


def _load_bundle(
    *,
    root: Path,
    index_path: Path,
    index: Mapping[str, Any],
    index_bytes: bytes,
    assets: Mapping[int, AssetSnapshot],
    slots: Mapping[str, Slot],
    reviewer_bytes: bytes,
    retrieval_bytes: bytes,
    identity: Mapping[str, str],
) -> BundleSnapshot:
    manifest_asset, manifest = _manifest_asset(assets, str(index_path))
    required_fields = {
        "schema_version",
        "bundle_id",
        "slot_kind",
        "slot_id",
        "collection_anchor",
        "collection_witness",
        "source_identity",
        "files",
    }
    if set(manifest) != required_fields:
        _fail("workspace_manifest_fields", str(index_path), str(sorted(manifest)))
    slot_id = _identifier(manifest.get("slot_id"), f"{index_path}.slot_id", reject_oracle=manifest.get("slot_kind") == "reviewer")
    slot = slots.get(slot_id)
    if slot is None or manifest.get("slot_kind") != slot.kind:
        _fail("mixed_slot_bundle", str(index_path), slot_id)
    if dict(_mapping(manifest.get("source_identity"), f"{index_path}.source_identity")) != dict(identity):
        _fail("mixed_release_evidence", str(index_path), slot_id)
    anchor = manifest.get("collection_anchor")
    if not isinstance(anchor, bool) or (slot.kind == "retrieval" and anchor):
        _fail("collection_anchor", str(index_path), repr(anchor))
    collection_witness = manifest.get("collection_witness")
    if not isinstance(collection_witness, bool) or (collection_witness and anchor):
        _fail("collection_witness", str(index_path), repr(collection_witness))
    workspace: list[WorkspaceFile] = []
    consumed = {manifest_asset.asset_id}
    for offset, value in enumerate(_sequence(manifest.get("files"), f"{index_path}.files")):
        logical, asset = _binding(value, assets, f"{index_path}.files[{offset}]")
        if asset.asset_id in consumed:
            _fail("workspace_asset_reused", str(index_path), str(asset.asset_id))
        consumed.add(asset.asset_id)
        workspace.append(WorkspaceFile(logical, asset.asset_id, asset.digest, asset.payload))
    witnessed_collection_paths: dict[str, str] = {}
    for kind, payload in (
        ("reviewer", reviewer_bytes),
        ("retrieval", retrieval_bytes),
    ):
        matches = [item.logical_path for item in workspace if item.payload == payload]
        if collection_witness:
            if len(matches) != 1:
                _fail(
                    "collection_witness_binding",
                    str(index_path),
                    f"{kind}: expected one collection asset, found {len(matches)}",
                )
            witnessed_collection_paths[kind] = matches[0]
        elif matches:
            _fail(
                "collection_witness_binding",
                str(index_path),
                f"{kind}: collection bytes appear outside the sole witness bundle",
            )
    envelope_assets = [item for item in assets.values() if item.evidence_kind == "evidence_envelope"]
    report_assets = [item for item in assets.values() if item.evidence_kind == "verifier_report"]
    if len(envelope_assets) != 1 or len(report_assets) != 1:
        _fail("envelope_report_count", str(index_path), "one envelope and report are required")
    consumed.update({envelope_assets[0].asset_id, report_assets[0].asset_id})
    if consumed != set(assets):
        _fail("indexed_asset_not_consumed", str(index_path), str(sorted(set(assets) - consumed)))
    envelope = _parse(envelope_assets[0].payload, f"{index_path}.envelope")

    def fetch(record: Mapping[str, Any]) -> bytes:
        asset = assets.get(record.get("asset_id"))
        if asset is None:
            _fail("asset_fetch_unindexed", str(index_path), str(record.get("asset_id")))
        return asset.payload

    try:
        integrity = validate_evidence_bundle(
            envelope,
            index,
            fetch,
            envelope_bytes=envelope_assets[0].payload,
            expected_source_identity=identity,
            index_bytes=index_bytes,
        )
    except EvidenceValidationError as exc:
        _fail(exc.code, f"{index_path}:{exc.path}", exc.message)
    raw_file = next(
        (item for item in workspace if item.asset_id == integrity.raw_export_asset_id),
        None,
    )
    expected_raw = slot.raw_path
    if slot.kind == "reviewer" and anchor:
        expected_raw = _logical_path(
            _parse(reviewer_bytes, "reviewer_receipts").get("platform_task_or_delegation_export_path"),
            "reviewer.platform_export",
        )
    if (
        raw_file is None
        or raw_file.logical_path != expected_raw
        or raw_file.logical_path
        != assets[raw_file.asset_id].source_path.relative_to(root).as_posix()
        or assets[raw_file.asset_id].evidence_kind not in CAPTURE_EXPORT_KINDS
    ):
        _fail("slot_raw_export_binding", str(index_path), f"{slot_id}: {expected_raw}")
    capture = _mapping(envelope.get("capture"), f"{index_path}.envelope.capture")
    if (
        capture.get("task_or_thread_id") != slot.execution_id
        or _timestamp(capture.get("captured_at"), f"{slot_id}.envelope_capture")
        != _timestamp(slot.captured_at, f"{slot_id}.collection_capture")
    ):
        _fail("slot_execution_binding", str(index_path), slot_id)
    return BundleSnapshot(
        bundle_id=_identifier(manifest.get("bundle_id"), f"{index_path}.bundle_id", reject_oracle=slot.kind == "reviewer"),
        slot=slot,
        collection_anchor=anchor,
        index_path=index_path,
        index_document=index,
        index_bytes=index_bytes,
        assets=assets,
        envelope=envelope,
        envelope_bytes=envelope_assets[0].payload,
        integrity=integrity,
        collection_witness=collection_witness,
        witnessed_collection_paths=witnessed_collection_paths,
        workspace_files=tuple(workspace),
    )


def _attestation_paths_match(subject: Mapping[str, Any], bundle: BundleSnapshot, root: Path) -> None:
    attestation = _mapping(subject.get("preview_attestation"), f"{bundle.slot.slot_id}.preview_attestation")
    envelope_asset = next(item for item in bundle.assets.values() if item.evidence_kind == "evidence_envelope")
    expected = {
        "adapter_id": PREVIEW_ADAPTER_ID,
        "envelope_path": envelope_asset.source_path.relative_to(root).as_posix(),
        "envelope_digest": envelope_asset.digest,
        "release_asset_index_path": bundle.index_path.relative_to(root).as_posix(),
        "release_asset_index_digest": sha256_bytes(bundle.index_bytes),
        "raw_export_path": next(
            item.logical_path
            for item in bundle.workspace_files
            if item.asset_id == bundle.integrity.raw_export_asset_id
        ),
        "raw_export_digest": bundle.integrity.raw_export_sha256,
        "synthetic_test_only": False,
    }
    mismatched = sorted(field for field, value in expected.items() if attestation.get(field) != value)
    if mismatched:
        _fail("embedded_attestation_mismatch", bundle.slot.slot_id, str(mismatched))


def _request_for_bundle(module: Any, bundle: BundleSnapshot, identity: Mapping[str, str]) -> Mapping[str, Any]:
    envelope_name = next(item.name for item in bundle.assets.values() if item.evidence_kind == "evidence_envelope")
    with tempfile.TemporaryDirectory(prefix="phase8-external-identity-") as directory:
        identity_path = Path(directory) / "source-identity.json"
        identity_path.write_text(json.dumps(dict(identity), sort_keys=True), encoding="utf-8", newline="\n")
        return module.build_request_from_bundle(
            evidence_root=bundle.index_path.parent,
            asset_index_path=bundle.index_path.name,
            envelope_path=envelope_name,
            expected_source_identity_path=identity_path,
        )


def _validate_live_result(bundle: BundleSnapshot, result: Mapping[str, Any], identity: Mapping[str, str]) -> None:
    integrity = _mapping(result.get("integrity_result"), f"{bundle.slot.slot_id}.integrity_result")
    live = _mapping(result.get("live_verifier"), f"{bundle.slot.slot_id}.live_verifier")
    gate = _mapping(result.get("gate_eligibility"), f"{bundle.slot.slot_id}.gate_eligibility")
    artifact_digests = _mapping(
        result.get("artifact_digests"),
        f"{bundle.slot.slot_id}.artifact_digests",
    )
    verified_assets = _sequence(
        result.get("verified_assets"),
        f"{bundle.slot.slot_id}.verified_assets",
    )
    verified_by_id = {
        item.get("asset_id"): item
        for item in verified_assets
        if isinstance(item, Mapping)
    }
    asset_contract = all(
        isinstance(verified_by_id.get(asset_id), Mapping)
        and verified_by_id[asset_id].get("name") == asset.name
        and verified_by_id[asset_id].get("sha256") == asset.digest
        and verified_by_id[asset_id].get("size") == asset.size
        and verified_by_id[asset_id].get("evidence_kind") == asset.evidence_kind
        and verified_by_id[asset_id].get("state") == "uploaded"
        and str(verified_by_id[asset_id].get("api_url", "")).startswith(
            "https://api.github.com/"
        )
        for asset_id, asset in bundle.assets.items()
    )
    index_witnesses = [
        item
        for item in verified_assets
        if isinstance(item, Mapping)
        and item.get("evidence_kind") == "release_asset_index"
    ]
    index_contract = (
        len(index_witnesses) == 1
        and index_witnesses[0].get("sha256")
        == bundle.integrity.release_asset_index_sha256
        and index_witnesses[0].get("size") == len(bundle.index_bytes)
        and index_witnesses[0].get("state") == "uploaded"
        and str(index_witnesses[0].get("api_url", "")).startswith(
            "https://api.github.com/"
        )
        and len(verified_assets) == len(bundle.assets) + 1
    )
    valid = (
        result.get("schema_version") == 3
        and result.get("verdict") == PREVIEW_ATTESTED
        and result.get("adapter_id") == PREVIEW_ADAPTER_ID
        and result.get("source_identity") == dict(identity)
        and result.get("integrity_valid") is True
        and result.get("gate_eligible") is True
        and result.get("counts_as_preview_attested") is True
        and result.get("counts_as_provider_verified") is False
        and result.get("provider_verified") is False
        and result.get("synthetic_self_test") is False
        and integrity.get("evidence_id") == bundle.integrity.evidence_id
        and integrity.get("raw_export_asset_id")
        == bundle.integrity.raw_export_asset_id
        and integrity.get("raw_export_sha256") == bundle.integrity.raw_export_sha256
        and integrity.get("envelope_asset_id")
        == bundle.integrity.evidence_envelope_asset_id
        and integrity.get("envelope_sha256") == bundle.integrity.evidence_envelope_sha256
        and integrity.get("verifier_report_asset_id")
        == bundle.integrity.verifier_report_asset_id
        and integrity.get("verifier_report_sha256") == bundle.integrity.verifier_report_sha256
        and integrity.get("release_asset_index_sha256") == bundle.integrity.release_asset_index_sha256
        and artifact_digests
        == {
            "raw_export_sha256": bundle.integrity.raw_export_sha256,
            "evidence_envelope_sha256": bundle.integrity.evidence_envelope_sha256,
            "verifier_report_sha256": bundle.integrity.verifier_report_sha256,
            "release_asset_index_sha256": bundle.integrity.release_asset_index_sha256,
        }
        and asset_contract
        and index_contract
        and live.get("adapter_id") == PREVIEW_ADAPTER_ID
        and live.get("live_requery") is True
        and live.get("independent") is True
        and isinstance(live.get("verifier_workflow_run_id"), int)
        and live.get("verifier_workflow_run_id") > 0
        and str(live.get("verifier_run_url", "")).startswith("https://github.com/")
        and gate.get("eligible") is True
        and gate.get("level") == PREVIEW_ATTESTED
        and gate.get("determined_by") == "registered_live_verifier"
        and gate.get("provider_authenticated") is False
    )
    _timestamp(live.get("verified_at"), f"{bundle.slot.slot_id}.verified_at")
    if not valid:
        _fail("live_preview_verification_failed", bundle.slot.slot_id, "v3 gate contract mismatch")


def _inventory(root: Path) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            _fail("symlink_rejected", "evidence_root", str(path))
        if path.is_file():
            resolved = _inside(root, path, "evidence_root.inventory")
            result[resolved] = sha256_bytes(_read(resolved, "evidence_root.inventory"))
    return result


def _assert_sources_unchanged(snapshots: Mapping[Path, SourceSnapshot], inventory: Mapping[Path, str], root: Path, stage: str) -> None:
    if _inventory(root) != dict(inventory):
        _fail("source_inventory_changed", stage, str(root))
    for snapshot in snapshots.values():
        payload = _read(snapshot.path, stage)
        if payload != snapshot.payload or sha256_bytes(payload) != snapshot.digest:
            _fail("source_changed_during_validation", stage, str(snapshot.path))


def _materialize(
    root: Path,
    workspace: Path,
    bundles: Sequence[BundleSnapshot],
) -> dict[str, str]:
    expected: dict[str, bytes] = {}
    for bundle in bundles:
        expected[bundle.index_path.relative_to(root).as_posix()] = bundle.index_bytes
        for asset in bundle.assets.values():
            expected[asset.source_path.relative_to(root).as_posix()] = asset.payload
        for item in bundle.workspace_files:
            existing = expected.get(item.logical_path)
            if existing is not None and existing != item.payload:
                _fail("workspace_path_conflict", item.logical_path, bundle.slot.slot_id)
            expected[item.logical_path] = item.payload
    for logical, payload in expected.items():
        target = _inside(workspace, workspace / Path(*PurePosixPath(logical).parts), f"workspace.{logical}", exists=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != payload:
            _fail("workspace_materialization_collision", logical, str(target))
        target.write_bytes(payload)
    return {logical: sha256_bytes(payload) for logical, payload in expected.items()}


def _load_phase8_verifier() -> Any:
    spec = importlib.util.spec_from_file_location("_phase8_external_live_verifier", PHASE8_VERIFIER_PATH)
    if spec is None or spec.loader is None:
        _fail("phase8_verifier_unavailable", "phase8_verifier", str(PHASE8_VERIFIER_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _default_semantic_validator(
    *,
    workspace_root: Path,
    reviewer_receipts_path: Path,
    retrieval_receipts_path: Path,
    source_identity: Mapping[str, str],
    validated_live_records: Sequence[Any],
) -> Mapping[str, Any]:
    import test_openai_phase8_corpus as phase8

    with phase8.phase8_external_preview_session(
        workspace_root=workspace_root,
        reviewer_receipts_path=reviewer_receipts_path,
        retrieval_receipts_path=retrieval_receipts_path,
        source_identity=_phase8_identity(source_identity),
        records=validated_live_records,
        issuer_capability=_PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY,
    ) as capability:
        report = phase8.run_all(
            live_repeat_path=reviewer_receipts_path,
            retrieval_receipts_path=retrieval_receipts_path,
            evidence_root=workspace_root,
            external_preview_capability=capability,
        )
        phase8.require_complete_preview_attested(report)
    return {
        "reviewer": report["live_fresh_repeat"],
        "retrieval": report["retrieval"],
        "phase8_report": report,
    }


def _validate_semantic_result(semantic: Mapping[str, Any]) -> Mapping[str, int]:
    import test_openai_phase8_corpus as phase8

    reviewer_result = _mapping(semantic.get("reviewer"), "semantic.reviewer")
    retrieval_result = _mapping(semantic.get("retrieval"), "semantic.retrieval")
    phase8_report = _mapping(semantic.get("phase8_report"), "semantic.phase8_report")
    try:
        phase8.require_complete_preview_attested(phase8_report)
    except Exception as exc:
        _fail(
            "phase8_semantic_result_incomplete",
            "semantic.phase8_report",
            f"{type(exc).__name__}: {exc}",
        )
    distribution = retrieval_result.get("preview_attested_current_receipts_by_kind")
    if not (
        reviewer_result.get("preview_attested_review_count") == EXPECTED_REVIEWER_SLOTS
        and reviewer_result.get("unique_reviewer_instance_count") == EXPECTED_REVIEWER_SLOTS
        and reviewer_result.get("preview_gate_status") == "completed"
        and reviewer_result.get("verified_live_review_count") == 0
        and retrieval_result.get("preview_attested_current_receipts") == EXPECTED_RETRIEVAL_SLOTS
        and distribution
        == {
            "deep_research_completed": 2,
            "deep_research_inactive_control": 1,
            "search": 3,
        }
        and retrieval_result.get("preview_gate_status") == "completed"
        and retrieval_result.get("completed_current_receipts") == 0
        and retrieval_result.get("pending_receipts") == 0
        and retrieval_result.get("stale_receipts") == 0
    ):
        _fail(
            "phase8_semantic_result_incomplete",
            "semantic_validator",
            str(semantic),
        )
    return _mapping(distribution, "semantic.retrieval.distribution")


def validate_external_phase8_evidence(
    *,
    evidence_root: Path,
    reviewer_receipts_path: Path,
    retrieval_receipts_path: Path,
    expected_source_identity_path: Path,
    asset_index_pattern: str,
    live_verifier: LiveVerifier,
    request_builder: RequestBuilder,
    semantic_validator: SemanticValidator,
) -> dict[str, Any]:
    if getattr(live_verifier, "adapter_id", None) != PREVIEW_ADAPTER_ID:
        _fail(
            "preview_adapter_not_registered",
            "live_verifier",
            str(getattr(live_verifier, "adapter_id", None)),
        )
    if evidence_root.is_symlink():
        _fail("symlink_rejected", "evidence_root", str(evidence_root))
    try:
        root = evidence_root.resolve(strict=True)
    except OSError as exc:
        _fail("evidence_root_missing", "evidence_root", str(exc))
    if not root.is_dir():
        _fail("evidence_root_missing", "evidence_root", str(root))
    reviewer_snapshot = _snapshot(reviewer_receipts_path, "reviewer_receipts")
    retrieval_snapshot = _snapshot(retrieval_receipts_path, "retrieval_receipts")
    identity_snapshot = _snapshot(expected_source_identity_path, "expected_source_identity")
    reviewer = _parse(reviewer_snapshot.payload, "reviewer_receipts")
    retrieval = _parse(retrieval_snapshot.payload, "retrieval_receipts")
    identity = _normalized_identity(_parse(identity_snapshot.payload, "expected_source_identity"))
    actual_identity = current_checkout_source_identity()
    if identity != actual_identity:
        _fail("local_source_identity_mismatch", "expected_source_identity", str(sorted(field for field in IDENTITY_FIELDS if identity.get(field) != actual_identity.get(field))))
    _assert_committed_source_identity(identity)
    reviewer_slots = _reviewer_slots(reviewer, identity)
    retrieval_slots = _retrieval_slots(retrieval, identity)
    if set(reviewer_slots).intersection(retrieval_slots):
        _fail("duplicate_slot", "receipt_collections", "reviewer and retrieval IDs overlap")
    slots = {**reviewer_slots, **retrieval_slots}
    _assert_slot_independence(slots)

    indexes = _discover_indexes(root, asset_index_pattern)
    source_snapshots: dict[Path, SourceSnapshot] = {
        reviewer_snapshot.path: reviewer_snapshot,
        retrieval_snapshot.path: retrieval_snapshot,
        identity_snapshot.path: identity_snapshot,
    }
    preloaded: list[tuple[Path, Mapping[str, Any], bytes, dict[int, AssetSnapshot]]] = []
    indexed_paths: set[Path] = set()
    for index_path in indexes:
        index_snapshot = _snapshot(index_path, "asset_index")
        source_snapshots[index_path] = index_snapshot
        index = _parse(index_snapshot.payload, str(index_path))
        assets = _load_assets(root, index_path, index)
        for asset in assets.values():
            if asset.source_path in indexed_paths:
                _fail("asset_file_reused_across_bundles", "asset", str(asset.source_path))
            indexed_paths.add(asset.source_path)
            source_snapshots[asset.source_path] = SourceSnapshot(asset.source_path, asset.payload, asset.digest)
        preloaded.append((index_path, index, index_snapshot.payload, assets))
    initial_inventory = _inventory(root)
    allowed = set(indexes) | indexed_paths
    for control in (reviewer_snapshot.path, retrieval_snapshot.path, identity_snapshot.path):
        try:
            control.relative_to(root)
        except ValueError:
            continue
        allowed.add(control)
    extra = set(initial_inventory) - allowed
    if extra:
        _fail("unindexed_evidence_file", "evidence_root", str(sorted(map(str, extra))))

    bundles: list[BundleSnapshot] = []
    bundle_ids: set[str] = set()
    bound_slots: set[str] = set()
    anchors: list[BundleSnapshot] = []
    collection_witnesses: list[BundleSnapshot] = []
    evidence_ids: set[str] = set()
    release_asset_ids: set[int] = set()
    for index_path, index, index_bytes, assets in preloaded:
        bundle = _load_bundle(
            root=root,
            index_path=index_path,
            index=index,
            index_bytes=index_bytes,
            assets=assets,
            slots=slots,
            reviewer_bytes=reviewer_snapshot.payload,
            retrieval_bytes=retrieval_snapshot.payload,
            identity=identity,
        )
        if bundle.bundle_id.casefold() in bundle_ids or bundle.slot.slot_id in bound_slots:
            _fail("duplicate_bundle_or_slot", str(index_path), bundle.slot.slot_id)
        if bundle.integrity.evidence_id in evidence_ids:
            _fail("duplicate_evidence_id", str(index_path), bundle.integrity.evidence_id)
        repeated_asset_ids = release_asset_ids.intersection(bundle.assets)
        if repeated_asset_ids:
            _fail("release_asset_id_reused", str(index_path), str(sorted(repeated_asset_ids)))
        bundle_ids.add(bundle.bundle_id.casefold())
        bound_slots.add(bundle.slot.slot_id)
        evidence_ids.add(bundle.integrity.evidence_id)
        release_asset_ids.update(bundle.assets)
        if bundle.collection_anchor:
            anchors.append(bundle)
        if bundle.collection_witness:
            collection_witnesses.append(bundle)
        bundles.append(bundle)
    if bound_slots != set(slots):
        _fail("phase8_slot_coverage", "asset_indexes", f"missing={sorted(set(slots) - bound_slots)}")
    if len(anchors) != 1 or anchors[0].slot.kind != "reviewer":
        _fail("collection_anchor_count", "workspace_manifests", str(len(anchors)))
    if (
        len(collection_witnesses) != 1
        or collection_witnesses[0].slot.kind != "reviewer"
        or collection_witnesses[0].collection_anchor
        or set(collection_witnesses[0].witnessed_collection_paths)
        != {"reviewer", "retrieval"}
    ):
        _fail(
            "collection_witness_count",
            "workspace_manifests",
            str(len(collection_witnesses)),
        )
    _attestation_paths_match(reviewer, anchors[0], root)
    for bundle in bundles:
        if bundle.slot.kind == "retrieval":
            _attestation_paths_match(bundle.slot.subject, bundle, root)

    reviewer_collection_path = collection_witnesses[0].witnessed_collection_paths[
        "reviewer"
    ]
    retrieval_collection_path = collection_witnesses[0].witnessed_collection_paths[
        "retrieval"
    ]
    expected_workspace = _required_workspace_paths(
        reviewer, retrieval, reviewer_collection_path, retrieval_collection_path
    )
    actual_workspace = {
        item.logical_path for bundle in bundles for item in bundle.workspace_files
    }
    if actual_workspace != expected_workspace:
        _fail("workspace_path_coverage", "workspace_manifests", f"missing={sorted(expected_workspace - actual_workspace)} extra={sorted(actual_workspace - expected_workspace)}")

    _assert_sources_unchanged(source_snapshots, initial_inventory, root, "before_live_verification")
    import test_openai_phase8_corpus as phase8

    validated_live_records: list[Any] = []
    for bundle in bundles:
        try:
            request = request_builder(bundle=bundle, identity=identity)
            result = _mapping(live_verifier(request), bundle.slot.slot_id)
            _validate_live_result(
                bundle,
                result,
                identity,
            )
            live = _mapping(
                result.get("live_verifier"),
                f"{bundle.slot.slot_id}.live_verifier",
            )
            validated_live_records.append(
                phase8.make_validated_phase8_live_slot(
                    slot_id=bundle.slot.slot_id,
                    slot_kind=bundle.slot.kind,
                    execution_id=bundle.slot.execution_id,
                    subject=bundle.slot.subject,
                    live_result=result,
                    evidence_id=bundle.integrity.evidence_id,
                    verifier_workflow_run_id=live["verifier_workflow_run_id"],
                    verified_at=str(live["verified_at"]),
                    issuer_capability=_PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY,
                )
            )
        except Exception as exc:
            _assert_sources_unchanged(source_snapshots, initial_inventory, root, "failed_live_verification")
            _fail("live_preview_verification_failed", bundle.slot.slot_id, f"{type(exc).__name__}: {exc}")
    _assert_sources_unchanged(source_snapshots, initial_inventory, root, "after_live_verification")

    with tempfile.TemporaryDirectory(prefix="phase8-attested-workspace-") as directory:
        workspace = Path(directory).resolve()
        materialized = _materialize(
            root,
            workspace,
            bundles,
        )
        before = {
            path.relative_to(workspace).as_posix(): sha256_bytes(path.read_bytes())
            for path in workspace.rglob("*")
            if path.is_file()
        }
        if before != materialized:
            _fail("workspace_materialization_inventory", "temporary_workspace", "unexpected files")
        try:
            semantic = semantic_validator(
                workspace_root=workspace,
                reviewer_receipts_path=workspace / reviewer_collection_path,
                retrieval_receipts_path=workspace / retrieval_collection_path,
                source_identity=identity,
                validated_live_records=tuple(validated_live_records),
            )
        except Exception as exc:
            failed_after = {
                path.relative_to(workspace).as_posix(): sha256_bytes(path.read_bytes())
                for path in workspace.rglob("*")
                if path.is_file()
            }
            if failed_after != before:
                _fail(
                    "temporary_workspace_changed",
                    "semantic_validator",
                    "workspace changed before semantic failure",
                )
            _assert_sources_unchanged(
                source_snapshots,
                initial_inventory,
                root,
                "failed_semantic_validation",
            )
            _fail("phase8_semantic_validation_failed", "semantic_validator", f"{type(exc).__name__}: {exc}")
        after = {
            path.relative_to(workspace).as_posix(): sha256_bytes(path.read_bytes())
            for path in workspace.rglob("*")
            if path.is_file()
        }
        if after != before:
            _fail("temporary_workspace_changed", "semantic_validator", "workspace bytes or inventory changed")
    semantic = _mapping(semantic, "semantic")
    distribution = _validate_semantic_result(semantic)
    phase8_report = dict(
        _mapping(semantic.get("phase8_report"), "semantic.phase8_report")
    )
    _assert_sources_unchanged(source_snapshots, initial_inventory, root, "after_semantic_validation")
    if current_checkout_source_identity() != identity:
        _fail("local_source_changed", "local_checkout", "plugin source identity changed")
    live_record_by_slot = {item.slot_id: item for item in validated_live_records}
    live_slot_results: list[dict[str, Any]] = []
    for bundle in sorted(bundles, key=lambda item: item.slot.slot_id):
        item = live_record_by_slot[bundle.slot.slot_id]
        release_identity = _mapping(
            bundle.index_document.get("github_release"),
            f"{bundle.index_path}.github_release",
        )
        live_slot_results.append(
            {
                "slot_id": item.slot_id,
                "slot_kind": item.slot_kind,
                "execution_id": item.execution_id,
                "subject_digest": item.subject_digest,
                "live_result_digest": item.live_result_digest,
                "evidence_id": item.evidence_id,
                "verifier_workflow_run_id": item.verifier_workflow_run_id,
                "verified_at": item.verified_at,
                "release": dict(release_identity),
                "asset_index": {
                    "name": bundle.index_path.name,
                    "size": len(bundle.index_bytes),
                    "sha256": sha256_bytes(bundle.index_bytes),
                },
                "assets": [
                    {
                        "asset_id": asset.asset_id,
                        "name": asset.name,
                        "size": asset.size,
                        "sha256": asset.digest,
                        "evidence_kind": asset.evidence_kind,
                    }
                    for asset in sorted(
                        bundle.assets.values(), key=lambda candidate: candidate.asset_id
                    )
                ],
            }
        )
    return {
        "schema_version": RESULT_SCHEMA,
        "accepted": True,
        "verification_level": PREVIEW_ATTESTED,
        "provider_verified": False,
        "adapter_id": PREVIEW_ADAPTER_ID,
        "source_identity": identity,
        "bundle_count": len(bundles),
        "reviewer_slot_count": EXPECTED_REVIEWER_SLOTS,
        "retrieval_slot_count": EXPECTED_RETRIEVAL_SLOTS,
        "retrieval_distribution": distribution,
        "live_requery_count": len(bundles),
        "source_immutability_verified": True,
        "temporary_workspace_immutability_verified": True,
        "phase8_report": phase8_report,
        "phase8_report_digest": phase8.external_preview_document_digest(
            phase8_report
        ),
        "phase_status": phase8_report["phase_status"],
        "live_slot_results": live_slot_results,
    }


def build_attested_phase8_report(**validation_arguments: Any) -> dict[str, Any]:
    """Run all live checks and return the report built inside that same session."""
    result = validate_external_phase8_evidence(**validation_arguments)
    return dict(_mapping(result.get("phase8_report"), "phase8_report"))


def _write_report_atomic(path: Path, report: Mapping[str, Any]) -> None:
    target = path.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with tempfile.TemporaryDirectory(prefix="phase8-report-", dir=target.parent) as directory:
        temporary = Path(directory) / target.name
        temporary.write_text(rendered, encoding="utf-8", newline="\n")
        temporary.replace(target)


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise Phase8ExternalEvidenceError("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description="Validate real Phase 8 external evidence")
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--reviewer-receipts", required=True)
    parser.add_argument("--retrieval-receipts", required=True)
    parser.add_argument("--expected-source-identity", required=True)
    parser.add_argument("--asset-index-pattern", required=True)
    parser.add_argument(
        "--report-output",
        help="Atomically write the report built inside the live verification session",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        verifier_module = _load_phase8_verifier()
        identity_document = _parse(_read(Path(args.expected_source_identity), "expected_source_identity"), "expected_source_identity")
        identity = _normalized_identity(identity_document)
        result = validate_external_phase8_evidence(
            evidence_root=Path(args.evidence_root),
            reviewer_receipts_path=Path(args.reviewer_receipts),
            retrieval_receipts_path=Path(args.retrieval_receipts),
            expected_source_identity_path=Path(args.expected_source_identity),
            asset_index_pattern=args.asset_index_pattern,
            live_verifier=verifier_module.verify,
            request_builder=lambda *, bundle, identity: _request_for_bundle(verifier_module, bundle, identity),
            semantic_validator=_default_semantic_validator,
        )
        report = _mapping(result.get("phase8_report"), "phase8_report")
        if args.report_output:
            _write_report_atomic(Path(args.report_output), report)
        output = dict(result)
        output.pop("phase8_report", None)
        output["phase8_report_written"] = bool(args.report_output)
        if args.report_output:
            output["phase8_report_output"] = str(Path(args.report_output))
    except Phase8ExternalEvidenceError as exc:
        output = {"schema_version": RESULT_SCHEMA, "accepted": False, "error": {"code": exc.code, "path": exc.path, "message": exc.message}}
        code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        output = {"schema_version": RESULT_SCHEMA, "accepted": False, "error": {"code": "internal_error", "path": "cli", "message": f"{type(exc).__name__}: {exc}"}}
        code = 3
    else:
        code = 0
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
